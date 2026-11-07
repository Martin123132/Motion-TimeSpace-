from stage149_holdout_common import *
import argparse


def run(part,epoch,deadline,stop_at):
    folder=ROOT/'runs'/f'{part}-{epoch}'
    if (folder/'COMPLETE').exists():
        packet=verify_packet(folder)
        assert packet['all_checks_passed'] and packet['script_sha256']==digest(__file__)
        return True
    proof_path=ROOT/'results/preflight/status.json'
    proof=verify_packet(proof_path.parent)
    assert proof['all_checks_passed']
    frozen_path=proof_path.parent/'frozen-inputs.npz'
    assert digest(frozen_path)==proof['frozen_inputs_sha256']
    bundle=EpochBundle(FRACTIONS[epoch])
    theta=epoch_context(bundle)[0][0]['theta']
    assert theta==proof['epoch_contexts'][epoch][0]['theta']
    model=FastSplit(bundle,'difference') if part=='expensive' else SplitReal(bundle,'control')
    keys=['difference','virtual','state'] if part=='expensive' else ['control']
    nodes=list(physical_nodes(theta,part))
    config=dict(part=part,epoch=epoch,epoch_fraction=FRACTIONS[epoch],temperature=theta,
        history_column_order=COLUMN_NAMES,radial=2,polar=2,azimuthal=4,hard_order=3,
        soft_angular=4,panel_order=18,seed_order=4 if part=='expensive' else 128,
        physical_electrons=16,scalar_representatives=12,
        fingerprints={str(path):digest(path) for path in
        [Path(__file__),ROOT/'stage149_holdout_common.py',ROOT/'ACCEPTANCE.md',ROOT/'DERIVATION.md',proof_path]})
    folder.mkdir(parents=True,exist_ok=True)
    config_path=folder/'configuration.json'
    if config_path.exists():
        assert json.loads(config_path.read_text())==config
    else:
        write_json(config_path,config)
    totals={key:np.zeros((98,4)) for key in keys}
    inputs=[config_path,proof_path,frozen_path]
    started,maximum_null=time.monotonic(),0.
    computed=0
    for ordinal,node in enumerate(nodes):
        if time.monotonic()>=deadline or datetime.now(timezone.utc)>=stop_at:
            progress=dict(state='paused_at_saved_node',part=part,epoch=epoch,
                completed_nodes=ordinal,total_nodes=len(nodes),pid=os.getpid())
            write_json(folder/'progress.json',progress)
            print(json.dumps(progress),flush=True)
            return False
        path=folder/'nodes'/f"{node['index']//500:03d}"/f"{node['index']:05d}.npz"
        parameters,weight=parameters_and_weight(theta,node)
        if path.exists():
            saved=read_npz(path)
            assert json.loads(str(saved['identity']))==node
            assert abs(float(saved['weight'])/weight-1)<1e-14
        else:
            if part=='expensive':
                values,energy_null,scalar,loop_path=expensive_components(parameters,model)
                saved=dict(**values,event_energy_null=energy_null,loop_scalar=scalar,loop_path=str(loop_path))
            else:
                result=model.real(parameters,angular=4,radial=18,rule=PanelRule(.5))
                saved=dict(control=result['total'],event_energy_null=result['event_energy_null'])
            saved.update(identity=json.dumps(node,sort_keys=True),weight=weight)
            path.parent.mkdir(parents=True,exist_ok=True)
            temporary=path.with_suffix('.tmp')
            with temporary.open('wb') as handle:
                np.savez(handle,**saved)
            temporary.replace(path)
            computed+=1
        for key in keys:
            assert saved[key].shape==(98,4) and np.isfinite(saved[key]).all()
            totals[key]-=weight*saved[key]
        inputs.append(path)
        maximum_null=max(maximum_null,float(saved['event_energy_null']))
        if part=='expensive':
            loop_path=Path(str(saved['loop_path']))
            assert loop_path.is_relative_to(ROOT/'virtual-cache')
            loop=json.loads(loop_path.read_text())
            assert loop['identity']==event_owner.inherited.virtual_identity(parameters)
            assert loop['scalar']==float(saved['loop_scalar'])
            inputs.append(loop_path)
        elapsed=time.monotonic()-started
        progress=dict(state='running',part=part,epoch=epoch,completed_nodes=ordinal+1,
            total_nodes=len(nodes),new_nodes=computed,elapsed_seconds=elapsed,pid=os.getpid(),
            updated_utc=datetime.now(timezone.utc).isoformat(),
            estimated_remaining_seconds=(len(nodes)-ordinal-1)*elapsed/max(computed,1))
        write_json(folder/'progress.json',progress)
        if (ordinal+1)%max(1,len(nodes)//8)==0:
            print(json.dumps(progress),flush=True)
    np.savez(folder/'source.npz',**totals)
    checks=[dict(name='All96 modes,four profiles and independent gas retained',passed=True)]
    test(checks,'Actual event photon gas exchange',maximum_null)
    finish(folder,dict(checks=checks,configuration=config,nodes=len(nodes),
        elapsed_seconds=time.monotonic()-started,pilot_resolution=True,
        midpoint_coefficients_transplanted=False,new_parent_history=False),
        __file__,[*inputs,*bundle.inputs,folder/'source.npz'])
    write_json(folder/'progress.json',dict(state='complete',part=part,epoch=epoch,
        completed_nodes=len(nodes),total_nodes=len(nodes),pid=os.getpid(),
        updated_utc=datetime.now(timezone.utc).isoformat()))
    print(json.dumps(dict(state='complete',part=part,epoch=epoch,nodes=len(nodes))),flush=True)
    return True


if __name__=='__main__':
    modest()
    parser=argparse.ArgumentParser()
    parser.add_argument('--epoch',choices=sorted(FRACTIONS),required=True)
    parser.add_argument('--part',choices=['both','expensive','control'],default='both')
    parser.add_argument('--max-seconds',type=float,default=11000.)
    parser.add_argument('--stop-at',default='2026-10-17T00:50:00+00:00')
    parser.add_argument('--dry-run',action='store_true')
    args=parser.parse_args()
    if args.dry_run:
        print(json.dumps(dict(epoch=args.epoch,fraction=FRACTIONS[args.epoch],
            nodes={part:sum(1 for node in physical_nodes(.0001,part))
                   for part in ['expensive','control']},outputs_written=False)),flush=True)
    else:
        deadline=time.monotonic()+args.max_seconds
        stop_at=datetime.fromisoformat(args.stop_at)
        assert stop_at.tzinfo is not None
        for part in (['expensive','control'] if args.part=='both' else [args.part]):
            if not run(part,args.epoch,deadline,stop_at):
                raise SystemExit(75)
