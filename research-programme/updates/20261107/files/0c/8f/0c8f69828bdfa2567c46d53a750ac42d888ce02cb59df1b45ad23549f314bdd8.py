from stage163_common import *
from stable_moments import StableMoments,components
import argparse


def run(endpoint,order,stop_at):
    folder=ROOT/'runs'/endpoint/f'order{order}'
    if (folder/'COMPLETE').exists():
        assert verify_packet(folder)['all_checks_passed']
        return True
    proof=verify_packet(ROOT/'results/preflight')
    assert proof['all_checks_passed']
    bundle=EpochBundle(ENDPOINTS[endpoint])
    theta=epoch_context(bundle)[0][0]['theta']
    assert theta==proof['contexts'][endpoint][0]['theta']
    model=StableMoments(bundle)
    nodes=list(integration_nodes(theta,order))
    folder.mkdir(parents=True,exist_ok=True)
    config=dict(endpoint=endpoint,order=order,theta=theta,nodes=len(nodes),cpu=int(os.environ['MTS_CPU']),
        threads=1,primitive_moments=['photon_energy','photon_number','independent_electron_energy'],
        fingerprints={str(path):digest(path) for path in [Path(__file__),ROOT/'stage163_common.py',
            ROOT/'stable_moments.py',ROOT/'ACCEPTANCE.md',ROOT/'DERIVATION.md',ROOT/'results/preflight/status.json']})
    if (folder/'configuration.json').exists():
        assert json.loads((folder/'configuration.json').read_text())==config
    else:
        write_json(folder/'configuration.json',config)
    inputs=[folder/'configuration.json',ROOT/'results/preflight/status.json',*bundle.inputs]
    started=time.monotonic()
    maximum_null=0.
    new_nodes=0
    for ordinal,node in enumerate(nodes):
        if datetime.now(timezone.utc)>=stop_at:
            write_json(folder/'progress.json',dict(state='paused_at_saved_node',completed_nodes=ordinal,
                total_nodes=len(nodes),pid=os.getpid(),endpoint=endpoint,order=order))
            return False
        old,weight,old_path,loop_path=parent162.load_node162(endpoint,order,node,theta)
        parameters,unused=parameters_and_weight(theta,node)
        path=moment_path(endpoint,order,node['index'])
        if not path.exists():
            before=time.monotonic()
            values,energy_null=components(parameters,model,float(old['loop_scalar']))
            saved=dict(**values,event_energy_null=energy_null,identity=json.dumps(node,sort_keys=True),weight=weight,
                old_path=str(old_path),old_sha256=digest(old_path),loop_path=str(loop_path),loop_sha256=digest(loop_path),
                seconds=time.monotonic()-before)
            path.parent.mkdir(parents=True,exist_ok=True)
            temporary=path.with_suffix('.tmp')
            with temporary.open('wb') as handle:
                np.savez(handle,**saved)
            temporary.replace(path)
            new_nodes+=1
        saved=read_npz(path)
        assert json.loads(str(saved['identity']))==node
        assert float(saved['weight'])==weight
        assert str(saved['old_sha256'])==digest(old_path)
        assert str(saved['loop_sha256'])==digest(loop_path)
        assert all(saved[key].shape==(3,4) and np.isfinite(saved[key]).all() for key in COMPONENTS)
        maximum_null=max(maximum_null,float(saved['event_energy_null']))
        inputs.extend([path,old_path,loop_path])
        if (ordinal+1)%36==0 or ordinal+1==len(nodes):
            elapsed=time.monotonic()-started
            progress=dict(state='running',endpoint=endpoint,order=order,completed_nodes=ordinal+1,
                total_nodes=len(nodes),pid=os.getpid(),elapsed_seconds=elapsed,new_nodes=new_nodes,
                estimated_remaining_seconds=(len(nodes)-ordinal-1)*elapsed/max(new_nodes,1),
                updated_utc=datetime.now(timezone.utc).isoformat())
            write_json(folder/'progress.json',progress)
            if (ordinal+1)%252==0:
                print(json.dumps(progress),flush=True)
    checks=[]
    test(checks,'Independent real-event photon/gas absolute defect',maximum_null,1e-10)
    checks.append(dict(name='All saved identities,weights,source hashes and primitive shapes match',passed=True))
    finish(folder,dict(checks=checks,endpoint=endpoint,order=order,nodes=len(nodes),new_nodes=new_nodes,
        elapsed_seconds=time.monotonic()-started,virtual_coefficients_reused=True),__file__,inputs)
    write_json(folder/'progress.json',dict(state='complete',endpoint=endpoint,order=order,
        completed_nodes=len(nodes),total_nodes=len(nodes),pid=os.getpid()))
    print(json.dumps(dict(endpoint=endpoint,order=order,complete=True,seconds=time.monotonic()-started)),flush=True)
    assert all(row['passed'] for row in checks)
    return True


if __name__=='__main__':
    modest()
    parser=argparse.ArgumentParser()
    parser.add_argument('--endpoint',choices=list(ENDPOINTS),required=True)
    parser.add_argument('--stop-at',default=DEADLINE)
    parser.add_argument('--dry-run',action='store_true')
    args=parser.parse_args()
    if args.dry_run:
        print(json.dumps(dict(endpoint=args.endpoint,orders=[4,5,6],events=3780,outputs_written=False)))
    else:
        for order in [4,5,6]:
            if not run(args.endpoint,order,datetime.fromisoformat(args.stop_at)):
                raise SystemExit(75)
