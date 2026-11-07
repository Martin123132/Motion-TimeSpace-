from quadrature_common import *
from paired_adjoint import stable_adjoint
from direct_common import tail,source_grid
import argparse
import hashlib
import time


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--upper',type=float,choices=[.04,.02],required=True)
    parser.add_argument('--variant',choices=VARIANTS,required=True)
    args=parser.parse_args()
    modest()
    label=int(args.upper*1000)
    folder=ROOT/'results'/f'bank-{args.variant}-m{label}'
    if (folder/'COMPLETE').exists():
        assert local_packet(folder)['all_checks_passed']
        print(json.dumps(dict(reused_complete=str(folder))),flush=True)
        return
    folder.mkdir(parents=True,exist_ok=True)
    started=time.monotonic()
    order,panels=specification(args.upper,args.variant)
    assert local_packet(ROOT/'results/arithmetic-proof')['all_checks_passed']
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    basis=ladder.basis
    backgrounds={model:thermal_wave.thermal.ThermalBackground(model) for model in ['heavy','cold']}
    parent_path=PARENT/'results'/f'operator-m{label}/bank.npz'
    parent=read_npz(parent_path)
    selected=np.flatnonzero(parent['steps']%40==20)
    assert np.array_equal(parent['steps'][selected],ODD_STEPS)
    coordinate=parent['coordinate'][selected]
    frequency,weights=source_grid(args.upper,panels)
    if panels==32:
        assert np.array_equal(frequency,parent['frequency']) and np.array_equal(weights,parent['weights'])
    inputs=[parent_path,parent_path.parent/'status.json',*ladder.inputs,
        ROOT/'results/arithmetic-proof/status.json',ROOT/'results/arithmetic-proof/comparison.npz',
        ROOT/'paired_adjoint.py']
    for background in backgrounds.values():
        inputs.extend([background.parent.source,background.native_constants])
    for step in ODD_STEPS:
        inputs.append(parent_path.parent/f'event-{step:05d}.npz')
    paths=set(inputs+[ROOT/'ACCEPTANCE.md',ROOT/'DERIVATION.md',ROOT/'quadrature_common.py',Path(__file__).resolve()])
    for module in list(sys.modules.values()):
        filename=getattr(module,'__file__',None)
        if filename:
            path=Path(filename).resolve()
            if path.suffix=='.py' and path.is_relative_to(BRANCH):
                paths.add(path)
    fingerprint={str(path):digest(path) for path in sorted(paths)}
    fingerprint_path=folder/'INPUTS.json'
    if fingerprint_path.exists():
        assert json.loads(fingerprint_path.read_text())==fingerprint
    else:
        write_json(fingerprint_path,fingerprint)
    fingerprint_hash=hashlib.sha256(json.dumps(fingerprint,sort_keys=True).encode()).hexdigest()
    adjoints,temperatures,checks,rows=[],[],[],[]
    deadline=os.environ.get('MTS_DEADLINE_UTC')
    deadline=datetime.fromisoformat(deadline) if deadline else None
    for step,position,parent_index in zip(ODD_STEPS,coordinate,selected):
        if (ROOT/'PAUSE-REQUESTED').exists() or (deadline and datetime.now(timezone.utc)>=deadline):
            write_json(folder/'progress.json',dict(state='yielded_pending',completed=len(rows),total=16))
            print(json.dumps(dict(safe_yield=True,folder=str(folder),completed=len(rows))),flush=True)
            raise SystemExit(75)
        receipt_path=folder/f'event-{step:05d}.json'
        event_path=folder/f'event-{step:05d}.npz'
        if receipt_path.exists():
            receipt=json.loads(receipt_path.read_text())
            assert receipt['input_fingerprint_sha256']==fingerprint_hash
            assert receipt['archive_sha256']==digest(event_path)
            event=read_npz(event_path)
            assert int(event['step'])==int(step)
            row,group=receipt['row'],receipt['checks']
            adjoint,theta=event['adjoint'],float(event['theta'])
        else:
            theta=backgrounds['heavy'].at(float(position))['thermal_parameter']
            assert theta==backgrounds['cold'].at(float(position))['thermal_parameter']
            ratios,rates=tail.jump_events(theta,order)
            adjoint,moment,diagnostics=stable_adjoint(basis,frequency,weights,ratios,rates)
            powers=np.arange(-4,5)
            mellin=np.sum((rates/ratios)[:,None]*np.expm1(np.log(ratios)[:,None]*powers),axis=0)
            symmetry=max(abs(mellin[index]-mellin[7-index]) for index in range(8))/np.linalg.norm(mellin)
            expected=weights*frequency*moment/(2*I3)
            energy=np.linalg.norm(basis.temperature@adjoint-expected)/np.linalg.norm(expected)
            group=[check(f'Pre-replacement energy:{step}',diagnostics['raw_energy_error'],1e-10),
                check(f'Mellin symmetry:{step}',symmetry,1e-8),
                check(f'Energy moment:{step}',energy,1e-10),
                check(f'Number invariant:{step}',np.max(abs(basis.chemical@adjoint)),1e-14),
                dict(name='Positive events:'+str(step),passed=bool(np.all(ratios>0) and np.all(rates>0)))]
            arithmetic_change=None
            if args.variant=='stable':
                old_event=read_npz(parent_path.parent/f'event-{step:05d}.npz')
                group.append(dict(name='Same events and analytic rows:'+str(step),passed=
                    np.array_equal(ratios,old_event['ratios']) and np.array_equal(rates,old_event['rates']) and
                    np.array_equal(adjoint[:2],parent['adjoint'][parent_index,:2])))
                arithmetic_change=float(np.linalg.norm(adjoint-parent['adjoint'][parent_index])/np.linalg.norm(parent['adjoint'][parent_index]))
            row=dict(step=int(step),coordinate=float(position),theta=theta,events=len(ratios),energy_moment=moment,
                arithmetic_operator_relative_change=arithmetic_change,diagnostics=diagnostics)
            np.savez_compressed(event_path,step=step,coordinate=position,theta=theta,ratios=ratios,rates=rates,
                frequency=frequency,weights=weights,adjoint=adjoint)
            write_json(receipt_path,dict(input_fingerprint_sha256=fingerprint_hash,archive_sha256=digest(event_path),
                row=row,checks=group))
            assert all(item['passed'] for item in group),(step,group)
        adjoints.append(adjoint)
        temperatures.append(theta)
        checks.extend(group)
        rows.append(row)
        write_json(folder/'progress.json',dict(state='running',completed=len(rows),total=16,seconds=time.monotonic()-started))
        if len(rows)%4==0:
            print(json.dumps(dict(variant=args.variant,upper=args.upper,completed=len(rows),seconds=time.monotonic()-started)),flush=True)
    np.savez_compressed(folder/'bank.npz',steps=ODD_STEPS,coordinate=coordinate,temperature=np.array(temperatures),
        frequency=frequency,weights=weights,adjoint=np.array(adjoints))
    chain=ancestors()
    for path in inputs:
        if not Path(path).is_relative_to(ROOT):
            verify_source(path,chain)
    finish(folder,dict(checks=checks,rows=rows,variant=args.variant,upper=args.upper,event_order=order,
        frequency_panel_order=panels,arithmetic='paired-rational-recurrence',new_temperature_evaluations=16,
        full_recoil_evaluations=0,seconds=time.monotonic()-started),__file__,[*inputs,fingerprint_path])
    assert all(item['passed'] for item in checks)


if __name__=='__main__':
    main()
