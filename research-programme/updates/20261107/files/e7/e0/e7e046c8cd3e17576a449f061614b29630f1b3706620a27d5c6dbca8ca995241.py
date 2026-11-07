import argparse
from history_frequency_common import *


def run(part,epoch,deadline):
    folder=ROOT/'runs'/f'{part}-{epoch}'
    if (folder/'COMPLETE').exists():
        report=json.loads((folder/'status.json').read_text())
        assert report['all_checks_passed'] and report['script_sha256']==digest(__file__)
        for path,expected in report['input_hashes'].items():
            assert digest(path)==expected,path
        return True
    proof_path=ROOT/'results/frequency-preflight/status.json'
    proof=json.loads(proof_path.read_text())
    assert proof['all_checks_passed']
    baseline_path=PARENT/'results/holdout-sources/source.npz'
    assert digest(baseline_path)==proof['baseline_sha256']
    for path,expected in proof['input_hashes'].items():
        assert digest(path)==expected,path
    bundle=EpochBundle(FRACTIONS[epoch])
    theta=epoch_context(bundle)[0][0]['theta']
    assert theta==proof['epoch_contexts'][epoch][0][0]['theta']
    model=FastSplit(bundle,'difference') if part=='expensive' else SplitReal(bundle,'control')
    keys=['difference','virtual','state'] if part=='expensive' else ['control']
    nodes=list(physical_nodes(theta,part))
    config=dict(part=part,epoch=epoch,epoch_fraction=FRACTIONS[epoch],temperature=theta,
        history_column_order=['heldout-heavy-join1','heldout-heavy-join2','heldout-cold-join1','heldout-cold-join2'],
        radial=2,polar=2,azimuthal=4,hard_order=3,soft_angular=4,panel_order=18,
        seed_order=3,physical_electrons=16,scalar_representatives=12,
        fingerprints={str(path):digest(path) for path in [Path(__file__),ROOT/'history_frequency_common.py',ROOT/'ACCEPTANCE.md',proof_path]})
    folder.mkdir(parents=True,exist_ok=True)
    config_path=folder/'configuration.json'
    if config_path.exists():
        assert json.loads(config_path.read_text())==config
    else:
        write_json(config_path,config)
    totals={key:np.zeros((98,4)) for key in keys}
    inputs=[config_path,proof_path,baseline_path]
    started,maximum_null=time.monotonic(),0.
    for ordinal,node in enumerate(nodes):
        if time.monotonic()>=deadline:
            progress=dict(state='paused_at_saved_node',part=part,epoch=epoch,completed_nodes=ordinal,total_nodes=len(nodes),pid=os.getpid())
            write_json(folder/'progress.json',progress)
            print(json.dumps(progress),flush=True)
            return False
        path=folder/'nodes'/f"{node['index']//500:03d}"/f"{node['index']:05d}.npz"
        parameters,weight=parameters_and_weight(theta,node)
        if path.exists():
            with np.load(path) as archive:
                saved={key:archive[key] for key in archive.files}
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
        for key in keys:
            assert saved[key].shape==(98,4) and np.isfinite(saved[key]).all()
            totals[key]-=weight*saved[key]
        inputs.append(path)
        maximum_null=max(maximum_null,float(saved['event_energy_null']))
        if part=='expensive':
            loop_path=Path(str(saved['loop_path']))
            loop=json.loads(loop_path.read_text())
            assert loop['identity']==inherited.virtual_identity(parameters)
            assert loop['scalar']==float(saved['loop_scalar'])
            inputs.append(loop_path)
        progress=dict(state='running',part=part,epoch=epoch,completed_nodes=ordinal+1,total_nodes=len(nodes),
            elapsed_seconds=time.monotonic()-started,pid=os.getpid())
        write_json(folder/'progress.json',progress)
        if (ordinal+1)%max(1,len(nodes)//4)==0:
            print(json.dumps(progress),flush=True)
    np.savez(folder/'source.npz',**totals)
    checks=[dict(name='All96 modes,four withheld profiles and independent gas retained',passed=True),
        dict(name='Actual event photon/gas exchange',value=maximum_null,passed=maximum_null<1e-10)]
    finish(folder,dict(checks=checks,configuration=config,nodes=len(nodes),elapsed_seconds=time.monotonic()-started,
        pilot_resolution=True,midpoint_coefficients_transplanted=False,new_parent_history=False),__file__,[*inputs,*bundle.inputs])
    print(json.dumps(dict(state='complete',part=part,epoch=epoch,nodes=len(nodes),checks=checks)),flush=True)
    return True


if __name__=='__main__':
    modest()
    parser=argparse.ArgumentParser()
    parser.add_argument('--epoch',choices=sorted(FRACTIONS),required=True)
    parser.add_argument('--parts',nargs='+',choices=['expensive'],default=['expensive'])
    parser.add_argument('--max-seconds',type=float,default=8500.)
    parser.add_argument('--dry-run',action='store_true')
    arguments=parser.parse_args()
    if arguments.dry_run:
        print(json.dumps(dict(epoch=arguments.epoch,nodes={part:sum(1 for node in physical_nodes(.0002,part)) for part in arguments.parts},outputs_written=False)))
        raise SystemExit(0)
    deadline=time.monotonic()+arguments.max_seconds
    for part in arguments.parts:
        if not run(part,arguments.epoch,deadline):
            raise SystemExit(75)



