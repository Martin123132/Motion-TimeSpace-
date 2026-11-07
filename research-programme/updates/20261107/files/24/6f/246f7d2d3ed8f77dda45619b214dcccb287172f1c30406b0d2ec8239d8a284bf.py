from stage162_common import *
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
    model=FastSplit(bundle,'difference')
    nodes=list(integration_nodes(theta,order))
    folder.mkdir(parents=True,exist_ok=True)
    config=dict(endpoint=endpoint,order=order,theta=theta,nodes=len(nodes),fraction=ENDPOINTS[endpoint],
        columns=COLUMN_NAMES,thread_count=1,cpu=int(os.environ['MTS_CPU']),
        fingerprints={str(path):digest(path) for path in [Path(__file__),ROOT/'stage162_common.py',
            ROOT/'ACCEPTANCE.md',ROOT/'DERIVATION.md',ROOT/'results/preflight/status.json']})
    if (folder/'configuration.json').exists():
        assert json.loads((folder/'configuration.json').read_text())==config
    else:
        write_json(folder/'configuration.json',config)
    inputs=[folder/'configuration.json',ROOT/'results/preflight/status.json',*bundle.inputs]
    started=time.monotonic()
    maximum_null=0.
    new_nodes=0
    totals={key:np.zeros((98,4)) for key in COMPONENTS}
    for ordinal,node in enumerate(nodes):
        if datetime.now(timezone.utc)>=stop_at:
            write_json(folder/'progress.json',dict(state='paused_at_saved_node',completed_nodes=ordinal,
                total_nodes=len(nodes),pid=os.getpid(),endpoint=endpoint,order=order))
            return False
        path=node_path162(endpoint,order,node['index'])
        parameters,weight=parameters_and_weight(theta,node)
        if not path.exists():
            values,energy_null,scalar,loop_path=expensive_components(parameters,model)
            saved=dict(**values,event_energy_null=energy_null,loop_scalar=scalar,loop_path=str(loop_path),
                identity=json.dumps(node,sort_keys=True),weight=weight)
            path.parent.mkdir(parents=True,exist_ok=True)
            temporary=path.with_suffix('.tmp')
            with temporary.open('wb') as handle:
                np.savez(handle,**saved)
            temporary.replace(path)
            new_nodes+=1
        saved,weight,path,loop_path=load_node162(endpoint,order,node,theta)
        maximum_null=max(maximum_null,float(saved['event_energy_null']))
        for component in COMPONENTS:
            totals[component]-=weight*saved[component]
        inputs.extend([path,loop_path])
        if (ordinal+1)%18==0 or ordinal+1==len(nodes):
            elapsed=time.monotonic()-started
            progress=dict(state='running',endpoint=endpoint,order=order,completed_nodes=ordinal+1,
                total_nodes=len(nodes),pid=os.getpid(),elapsed_seconds=elapsed,new_nodes=new_nodes,
                estimated_remaining_seconds=(len(nodes)-ordinal-1)*elapsed/max(new_nodes,1),
                updated_utc=datetime.now(timezone.utc).isoformat())
            write_json(folder/'progress.json',progress)
            if (ordinal+1)%126==0:
                print(json.dumps(progress),flush=True)
    np.savez_compressed(folder/'sequential.npz',**totals)
    checks=[]
    test(checks,'Independent event photon/gas exchange',maximum_null,1e-10)
    finish(folder,dict(checks=checks,endpoint=endpoint,order=order,nodes=len(nodes),
        elapsed_seconds=time.monotonic()-started),__file__,[*inputs,folder/'sequential.npz'])
    write_json(folder/'progress.json',dict(state='complete',endpoint=endpoint,order=order,
        completed_nodes=len(nodes),total_nodes=len(nodes),pid=os.getpid()))
    print(json.dumps(dict(endpoint=endpoint,order=order,complete=True,seconds=time.monotonic()-started)),flush=True)
    return True


if __name__=='__main__':
    modest()
    parser=argparse.ArgumentParser()
    parser.add_argument('--endpoint',choices=list(ENDPOINTS),required=True)
    parser.add_argument('--stop-at',default=DEADLINE)
    parser.add_argument('--dry-run',action='store_true')
    args=parser.parse_args()
    if args.dry_run:
        print(json.dumps(dict(endpoint=args.endpoint,orders=[5,6],events=2772,outputs_written=False)))
    else:
        for order in [5,6]:
            if not run(args.endpoint,order,datetime.fromisoformat(args.stop_at)):
                raise SystemExit(75)
