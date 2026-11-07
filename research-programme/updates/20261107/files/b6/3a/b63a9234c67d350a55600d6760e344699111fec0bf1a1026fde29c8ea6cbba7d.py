from direct_common import *
import time


def main():
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('--order',type=int,choices=[6,8],required=True)
    parser.add_argument('--panel',type=int,choices=[32,48],default=32)
    parser.add_argument('--upper',type=float,choices=[.02,.04],default=.04)
    args=parser.parse_args()
    modest()
    label=f'o{args.order}-q{args.panel}-m{int(args.upper*1000)}'
    folder=ROOT/'results'/('bank-'+label)
    folder.mkdir(parents=True,exist_ok=False)
    chain=ancestors()
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    basis=ladder.basis
    prediction,profiles,gas,inputs=read_prediction('heavy','fine')
    inputs.extend(ladder.inputs)
    backgrounds={model:thermal_wave.thermal.ThermalBackground(model) for model in ['heavy','cold']}
    for background in backgrounds.values():
        inputs.extend([background.parent.source,background.native_constants])
    for path in inputs:
        verify_source(path,chain)
    frequency,weights=source_grid(args.upper,args.panel)
    checks,rows=[],[]
    adjoints,temperatures=[],[]
    for epoch,position in enumerate(prediction['coordinate']):
        started=time.monotonic()
        theta=backgrounds['heavy'].at(float(position))['thermal_parameter']
        assert theta==backgrounds['cold'].at(float(position))['thermal_parameter']
        pilot=ROOT/'results/pilot'/f'e{epoch}-o{args.order}.npz'
        reused=pilot.exists() and args.panel==32 and args.upper==.04
        if reused:
            saved=read_npz(pilot)
            assert theta==float(saved['theta']) and np.array_equal(frequency,saved['frequency']) and np.array_equal(weights,saved['weights'])
            adjoint,ratios,rates=saved['adjoint'],saved['ratios'],saved['rates']
            moment=float(np.sum(rates*(ratios-1)**2*(ratios+1)/ratios**3))
            inputs.extend([pilot,pilot.parent/'status.json'])
        else:
            ratios,rates=tail.jump_events(theta,args.order)
            adjoint,moment=direct_adjoint(basis,frequency,weights,ratios,rates)
        assert np.isfinite(adjoint).all() and np.all(rates>0) and np.all(ratios>0)
        powers=np.arange(-4,5)
        mellin=np.sum((rates/ratios)[:,None]*np.expm1(np.log(ratios)[:,None]*powers),axis=0)
        symmetry=max(abs(mellin[index]-mellin[7-index]) for index in range(8))/np.linalg.norm(mellin)
        expected=weights*frequency*moment/(2*I3)
        energy_error=np.linalg.norm(basis.temperature@adjoint-expected)/np.linalg.norm(expected)
        checks.extend([check(f'Mellin symmetry:{epoch}',symmetry,1e-8),
            check(f'Analytic energy moment:{epoch}',energy_error,1e-10),
            check(f'Number invariant:{epoch}',np.max(abs(basis.chemical@adjoint)),1e-14)])
        np.savez_compressed(folder/f'epoch-{epoch:02d}.npz',theta=theta,ratios=ratios,rates=rates,adjoint=adjoint)
        adjoints.append(adjoint)
        temperatures.append(theta)
        row=dict(epoch=epoch,theta=theta,events=len(ratios),seconds=time.monotonic()-started,reused_pilot=reused,
            energy_moment=moment,mellin_symmetry=symmetry,energy_error=energy_error)
        rows.append(row)
        write_json(folder/'progress.json',dict(state='running',completed_epochs=epoch+1,total_epochs=len(prediction['coordinate']),latest=row))
        if epoch%8==0 or epoch==64:
            print(json.dumps(dict(bank=label,**row)),flush=True)
    np.savez_compressed(folder/'bank.npz',coordinate=prediction['coordinate'],temperature=np.array(temperatures),
        adjoint=np.array(adjoints),frequency=frequency,weights=weights)
    finish(folder,dict(checks=checks,rows=rows,event_order=args.order,quadrature_order=args.panel,match_upper=args.upper,
        same_temperatures_both_backgrounds=True,physical_shift_grid_deposition=False,
        new_soft_temperature_evaluations=sum(not row['reused_pilot'] for row in rows),
        full_recoil_evaluations=0),__file__,inputs)
    write_json(folder/'progress.json',dict(state='complete',completed_epochs=len(rows),total_epochs=len(rows)))


if __name__=='__main__':
    main()

