from stage165_common import *
from precise_soft_shifts import PreciseSoftShifts
import argparse


def run(endpoint):
    folder=ROOT/'runs/refined'/endpoint
    folder.mkdir(parents=True,exist_ok=True)
    assert not (folder/'COMPLETE').exists()
    proof=verify_packet(ROOT/'results/preflight')
    probe=verify_packet(ROOT/'results/precise-shift-probe')
    assert probe['all_checks_passed']
    bundle=EpochBundle(ENDPOINTS[endpoint])
    theta=proof['contexts'][endpoint][0]['theta']
    inputs=[ROOT/'results/preflight/status.json',ROOT/'results/precise-shift-probe/status.json',ROOT/'PRECISE-SHIFT-DERIVATION.md',*bundle.inputs]
    selected=[]
    for order in [4,5,6]:
        for node in integration_nodes(theta,order):
            path=moment_path(endpoint,order,node['index'])
            event=read_npz(path)
            inputs.append(path)
            if np.any(event['difference'][0]+event['difference'][-1]!=0):
                selected.append((order,node,path))
    configuration=dict(endpoint=endpoint,selected_nodes=[dict(order=order,index=node['index']) for order,node,path in selected],digits=80,
        selector='Any nonzero independent rounded real-event pair,all columns equally',
        hashes={str(path):digest(path) for path in [Path(__file__),ROOT/'precise_soft_shifts.py',ROOT/'PRECISE-SHIFT-DERIVATION.md']})
    if (folder/'configuration.json').exists():
        assert json.loads((folder/'configuration.json').read_text())==configuration
    else:
        write_json(folder/'configuration.json',configuration)
    inputs.append(folder/'configuration.json')
    checks=[]
    before=time.monotonic()
    for ordinal,(order,node,path) in enumerate(selected):
        if datetime.now(timezone.utc)>=datetime.fromisoformat(DEADLINE):
            write_json(folder/'progress.json',dict(state='paused_at_saved_node',completed=ordinal,total=len(selected)))
            raise SystemExit(75)
        target=folder/f'order{order}'/'nodes'/f'{node["index"]//500:03d}'/f'{node["index"]:05d}.npz'
        old=read_npz(path)
        if not target.exists():
            parameters,weight=parameters_and_weight(theta,node)
            model=PreciseSoftShifts(bundle,80)
            result=model.real(parameters,angular=4,radial=18,rule=PanelRule(.5))
            candidate=dict(old)
            candidate.update(difference=result['total'],base_path=str(path),base_sha256=digest(path),
                precise_shift_pair=model.maximum_precise_pair,direction_repair=model.maximum_direction_repair)
            target.parent.mkdir(parents=True,exist_ok=True)
            temporary=target.with_suffix('.tmp')
            with temporary.open('wb') as handle:
                np.savez(handle,**candidate)
            temporary.replace(target)
        candidate=read_npz(target)
        assert str(candidate['base_sha256'])==digest(path)
        assert np.array_equal(candidate['state'],old['state']) and np.array_equal(candidate['virtual'],old['virtual'])
        tag=f'{endpoint}:{order}:{node["index"]}'
        close(checks,'Refined real-source equivalence:'+tag,candidate['difference'],old['difference'],1e-10)
        test(checks,'Independent precise real shifts:'+tag,float(candidate['precise_shift_pair']),1e-10)
        test(checks,'Unit directions retained to rounding:'+tag,float(candidate['direction_repair']),1e-14)
        test(checks,'Independent refined real moment:'+tag,float(max(abs(candidate['difference'][0]+candidate['difference'][-1])/np.maximum(abs(candidate['difference'][0]),1e-300))),1e-10)
        inputs.append(target)
        if (ordinal+1)%20==0 or ordinal+1==len(selected):
            elapsed=time.monotonic()-before
            progress=dict(state='running',endpoint=endpoint,completed=ordinal+1,total=len(selected),elapsed_seconds=elapsed,
                remaining_seconds=elapsed*(len(selected)-ordinal-1)/(ordinal+1),pid=os.getpid())
            write_json(folder/'progress.json',progress)
            print(json.dumps(progress),flush=True)
    finish(folder,dict(checks=checks,endpoint=endpoint,selected_events=len(selected),elapsed_seconds=time.monotonic()-before,
        projection_used=False,temperature_curve_changed=False),__file__,inputs)
    assert all(row['passed'] for row in checks)


if __name__=='__main__':
    modest()
    parser=argparse.ArgumentParser()
    parser.add_argument('--endpoint',choices=list(ENDPOINTS),required=True)
    args=parser.parse_args()
    run(args.endpoint)
