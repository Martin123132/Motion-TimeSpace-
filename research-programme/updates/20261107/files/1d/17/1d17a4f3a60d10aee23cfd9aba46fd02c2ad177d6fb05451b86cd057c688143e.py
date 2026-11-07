from transient_common import *
from direct_common import tail,direct_adjoint
import argparse
import time


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--upper',type=float,choices=[.04,.02],required=True)
    args=parser.parse_args()
    modest()
    folder=ROOT/'results'/f'operator-m{int(args.upper*1000)}'
    folder.mkdir(parents=True,exist_ok=False)
    started=time.monotonic()
    order=8 if args.upper==.04 else 6
    old_path=BRANCH/'direct-doppler-compton-feedback-20261012/results'/f'bank-o{order}-q32-m{int(args.upper*1000)}/bank.npz'
    old=read_npz(old_path)
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    basis=ladder.basis
    backgrounds={model:thermal_wave.thermal.ThermalBackground(model) for model in ['heavy','cold']}
    inputs=[old_path,*ladder.inputs]
    for background in backgrounds.values():
        inputs.extend([background.parent.source,background.native_constants])
    steps=SOURCE_STEPS[1:-1]
    prior_path=PARENT/'results'/f'operator-m{int(args.upper*1000)}/bank.npz'
    prior=read_npz(prior_path)
    inputs.extend([prior_path,prior_path.parent/'status.json'])
    start,end=old['coordinate'][[0,-1]]
    coordinates=start+(end-start)*steps/40960
    adjoints,temperatures,rows,checks=[],[],[],[]
    for step,coordinate in zip(steps,coordinates):
        theta=backgrounds['heavy'].at(float(coordinate))['thermal_parameter']
        assert theta==backgrounds['cold'].at(float(coordinate))['thermal_parameter']
        ratios,rates=tail.jump_events(theta,order)
        if int(step) in [160,320,480]:
            prior_event_path=prior_path.parent/f'event-{step:05d}.npz'
            prior_event=read_npz(prior_event_path)
            assert np.array_equal(ratios,prior_event['ratios']) and np.array_equal(rates,prior_event['rates'])
            inputs.append(prior_event_path)
            adjoint=prior['adjoint'][int(np.flatnonzero(prior['steps']==step)[0])].copy()
            moment=float(np.sum(rates*(ratios-1)**2*(ratios+1)/ratios**3))
        else:
            adjoint,moment=direct_adjoint(basis,old['frequency'],old['weights'],ratios,rates)
        powers=np.arange(-4,5)
        mellin=np.sum((rates/ratios)[:,None]*np.expm1(np.log(ratios)[:,None]*powers),axis=0)
        symmetry=max(abs(mellin[index]-mellin[7-index]) for index in range(8))/np.linalg.norm(mellin)
        expected=old['weights']*old['frequency']*moment/(2*I3)
        energy=np.linalg.norm(basis.temperature@adjoint-expected)/np.linalg.norm(expected)
        checks.extend([check(f'Mellin symmetry:{step}',symmetry,1e-8),
            check(f'Energy moment:{step}',energy,1e-10),
            check(f'Number invariant:{step}',np.max(abs(basis.chemical@adjoint)),1e-14)])
        checks.append(dict(name='Positive events:'+str(step),passed=bool(np.all(ratios>0) and np.all(rates>0))))
        np.savez_compressed(folder/f'event-{step:05d}.npz',step=step,coordinate=coordinate,theta=theta,
            ratios=ratios,rates=rates,adjoint=adjoint)
        adjoints.append(adjoint)
        temperatures.append(theta)
        rows.append(dict(step=int(step),coordinate=float(coordinate),theta=theta,events=len(ratios),energy_moment=moment,reused=int(step) in [160,320,480]))
        write_json(folder/'progress.json',dict(state='running',completed=len(rows),total=len(steps),seconds=time.monotonic()-started))
        if len(rows)%9==0:
            print(json.dumps(dict(upper=args.upper,completed=len(rows),total=len(steps),seconds=time.monotonic()-started)),flush=True)
    np.savez_compressed(folder/'bank.npz',steps=steps,coordinate=coordinates,temperature=np.array(temperatures),
        adjoint=np.array(adjoints),frequency=old['frequency'],weights=old['weights'])
    chain=ancestors()
    for path in inputs:
        verify_source(path,chain)
    finish(folder,dict(checks=checks,rows=rows,event_order=order,upper=args.upper,new_soft_temperature_evaluations=12,reused_temperature_evaluations=3,
        full_recoil_evaluations=0,shared_temperature_verified=True,seconds=time.monotonic()-started),__file__,inputs)
    assert all(row['passed'] for row in checks)


if __name__=='__main__':
    main()
