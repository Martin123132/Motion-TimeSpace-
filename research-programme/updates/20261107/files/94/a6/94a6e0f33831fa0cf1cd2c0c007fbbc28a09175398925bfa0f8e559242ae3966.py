from stage165_common import *
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
    real_model,state_model=PreciseBornCorrelated(bundle),StableMoments(bundle)
    nodes=list(integration_nodes(theta,order))
    folder.mkdir(parents=True,exist_ok=True)
    config=dict(endpoint=endpoint,order=order,theta=theta,nodes=len(nodes),cpu=int(os.environ['MTS_CPU']),threads=1,
        fingerprints={str(path):digest(path) for path in [Path(__file__),ROOT/'stage165_common.py',
            ROOT/'ACCEPTANCE.md',ROOT/'DERIVATION.md',ROOT/'results/preflight/status.json',PARENT/'probe_state_roundoff.py']})
    if (folder/'configuration.json').exists():
        assert json.loads((folder/'configuration.json').read_text())==config
    else:
        write_json(folder/'configuration.json',config)
    inputs=[folder/'configuration.json',ROOT/'results/preflight/status.json',*bundle.inputs]
    started=time.monotonic()
    maximum_null=maximum_shift=maximum_state=maximum_virtual=0.
    equivalence={component:0. for component in COMPONENTS}
    new_nodes=0
    for ordinal,node in enumerate(nodes):
        if datetime.now(timezone.utc)>=stop_at:
            write_json(folder/'progress.json',dict(state='paused_at_saved_node',completed_nodes=ordinal,total_nodes=len(nodes),pid=os.getpid()))
            return False
        original_path=parent164.moment_path(endpoint,order,node['index'])
        original=read_npz(original_path)
        parameters,weight=parameters_and_weight(theta,node)
        assert json.loads(str(original['identity']))==node and float(original['weight'])==weight
        path=moment_path(endpoint,order,node['index'])
        if not path.exists():
            before=time.monotonic()
            saved=repaired_event(endpoint,order,node,theta,real_model,state_model)
            saved['seconds']=time.monotonic()-before
            path.parent.mkdir(parents=True,exist_ok=True)
            temporary=path.with_suffix('.tmp')
            with temporary.open('wb') as handle:
                np.savez(handle,**saved)
            temporary.replace(path)
            new_nodes+=1
        saved=read_npz(path)
        assert json.loads(str(saved['identity']))==node and float(saved['weight'])==weight
        assert str(saved['parent_sha256'])==digest(original_path)
        assert all(saved[key].shape==(3,4) and np.isfinite(saved[key]).all() for key in COMPONENTS)
        maximum_state=max(maximum_state,float(saved['state_pair_exact']))
        maximum_virtual=max(maximum_virtual,float(saved['virtual_pair_exact']))
        for component,value in json.loads(str(saved['equivalence'])).items():
            equivalence[component]=max(equivalence[component],value)
        for prefix in ['raw','loop']:
            assert digest(str(saved[prefix+'_path']))==str(saved[prefix+'_sha256'])
            inputs.append(Path(str(saved[prefix+'_path'])))
        maximum_null=max(maximum_null,float(saved['event_energy_null']))
        maximum_shift=max(maximum_shift,float(saved['shift_energy_null']))
        inputs.extend([path,original_path])
        if (ordinal+1)%36==0 or ordinal+1==len(nodes):
            elapsed=time.monotonic()-started
            progress=dict(state='running',endpoint=endpoint,order=order,completed_nodes=ordinal+1,total_nodes=len(nodes),
                pid=os.getpid(),elapsed_seconds=elapsed,new_nodes=new_nodes,
                estimated_remaining_seconds=(len(nodes)-ordinal-1)*elapsed/max(new_nodes,1),updated_utc=datetime.now(timezone.utc).isoformat())
            write_json(folder/'progress.json',progress)
            if (ordinal+1)%252==0:
                print(json.dumps(progress),flush=True)
    checks=[]
    test(checks,'Independent real-event absolute exchange',maximum_null,1e-10)
    test(checks,'Independent soft-shift absolute exchange',maximum_shift,1e-10)
    test(checks,'Independent80digit state energy',maximum_state,1e-10)
    test(checks,'Independent80digit virtual energy',maximum_virtual,1e-10)
    for component,value in equivalence.items():
        test(checks,'Source equivalence:'+component,value,1e-10)
    checks.append(dict(name='All event identities,weights,parent hashes and saved expensive virtual coefficients',passed=True))
    finish(folder,dict(checks=checks,endpoint=endpoint,order=order,nodes=len(nodes),new_nodes=new_nodes,
        elapsed_seconds=time.monotonic()-started,equivalence=equivalence),__file__,inputs)
    write_json(folder/'progress.json',dict(state='complete',endpoint=endpoint,order=order,completed_nodes=len(nodes),total_nodes=len(nodes),pid=os.getpid()))
    assert all(row['passed'] for row in checks)
    print(json.dumps(dict(endpoint=endpoint,order=order,complete=True)),flush=True)
    return True


if __name__=='__main__':
    modest()
    parser=argparse.ArgumentParser()
    parser.add_argument('--endpoint',choices=list(ENDPOINTS),required=True)
    parser.add_argument('--stop-at',default=DEADLINE)
    parser.add_argument('--dry-run',action='store_true')
    args=parser.parse_args()
    if args.dry_run:
        print(json.dumps(dict(endpoint=args.endpoint,events=3780,orders=[4,5,6],outputs_written=False)))
    else:
        for order in [4,5,6]:
            if not run(args.endpoint,order,datetime.fromisoformat(args.stop_at)):
                raise SystemExit(75)
