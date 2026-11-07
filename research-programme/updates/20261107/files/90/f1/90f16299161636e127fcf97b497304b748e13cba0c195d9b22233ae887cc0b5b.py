from direct_common import *
import time


def main():
    modest()
    folder=ROOT/'results/pilot'
    folder.mkdir(parents=True,exist_ok=False)
    chain=ancestors()
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    basis=ladder.basis
    prediction,profiles,gas,inputs=read_prediction('heavy','fine')
    inputs.extend(ladder.inputs)
    for path in inputs:
        verify_source(path,chain)
    background=thermal_wave.thermal.ThermalBackground('heavy')
    frequency,weights=source_grid(.04,32)
    rows,checks=[],[]
    for epoch in [0,32,64]:
        theta=background.at(float(prediction['coordinate'][epoch]))['thermal_parameter']
        old=None
        for order in [6,8]:
            started=time.monotonic()
            ratios,rates=tail.jump_events(theta,order)
            adjoint,moment=direct_adjoint(basis,frequency,weights,ratios,rates)
            elapsed=time.monotonic()-started
            powers=np.arange(-4,5)
            mellin=np.sum((rates/ratios)[:,None]*np.expm1(np.log(ratios)[:,None]*powers),axis=0)
            symmetry=max(abs(mellin[index]-mellin[7-index]) for index in range(8))/np.linalg.norm(mellin)
            checks.append(check(f'Mellin symmetry e{epoch}o{order}',symmetry,1e-8))
            checks.append(check(f'Number test e{epoch}o{order}',np.max(abs(basis.chemical@adjoint)),1e-14))
            np.savez_compressed(folder/f'e{epoch}-o{order}.npz',adjoint=adjoint,ratios=ratios,rates=rates,frequency=frequency,weights=weights,theta=theta,mellin=mellin)
            row=dict(epoch=epoch,theta=theta,order=order,events=len(ratios),seconds=elapsed,energy_moment=moment,mellin_symmetry=symmetry)
            if old is not None:
                row['adjoint_relative_refinement']=float(np.linalg.norm(adjoint-old)/np.linalg.norm(adjoint))
            old=adjoint
            rows.append(row)
            print(json.dumps(row),flush=True)
    finish(folder,dict(checks=checks,rows=rows),__file__,inputs+[background.parent.source,background.native_constants])


if __name__=='__main__':
    main()

