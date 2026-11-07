from stage158_common import *
import argparse


def run(band,part,stop_at):
    proof=verify_packet(ROOT/'results/preflight')
    assert proof['all_checks_passed']
    manifest_path=ROOT/'results/preflight/events.json'
    assert digest(manifest_path)==proof['manifest_sha256']
    selected=[row for row in json.loads(manifest_path.read_text())['new'] if row['band']==band]
    selected=selected[part::2]
    folder=ROOT/'runs'/f'band{band}'/f'part{part}'
    if (folder/'COMPLETE').exists():
        assert verify_packet(folder)['all_checks_passed']
        return True
    if band==4:
        for earlier in [0,1]:
            assert verify_packet(ROOT/'runs/band3'/f'part{earlier}')['all_checks_passed']
    folder.mkdir(parents=True,exist_ok=True)
    config=dict(band=band,part=part,order=7,manifest_sha256=digest(manifest_path),
        evaluator_sha256=digest(ROOT/'stage158_common.py'),worker_sha256=digest(__file__),
        deadline=stop_at.isoformat())
    if (folder/'configuration.json').exists():
        saved=json.loads((folder/'configuration.json').read_text())
        assert {key:value for key,value in saved.items() if key!='deadline'}=={key:value for key,value in config.items() if key!='deadline'}
    else:
        write_json(folder/'configuration.json',config)
    inputs=[folder/'configuration.json',manifest_path,ROOT/'results/preflight/status.json']
    models={}
    started=time.monotonic()
    new_count=shared_count=0
    maximum_null=0.
    for ordinal,row in enumerate(selected):
        if datetime.now(timezone.utc)>=stop_at:
            write_json(folder/'progress.json',dict(state='paused_at_saved_node',completed_nodes=ordinal,total_nodes=len(selected),pid=os.getpid()))
            return False
        if row['reused_path']:
            shared_count+=1
        elif not event_path(row).exists():
            site=row['site']
            if site not in models:
                bundle=EpochBundle(FRACTIONS[site])
                models[site]=FastSplit(bundle,'difference')
                inputs.extend(bundle.inputs)
            parameters,weight=parameters_and_weight(row['theta'],row['node'])
            values,energy_null,scalar,loop_path=expensive_components(parameters,models[site])
            saved=dict(**values,event_energy_null=energy_null,loop_scalar=scalar,loop_path=str(loop_path),
                identity=json.dumps(row['node'],sort_keys=True),weight=weight)
            path=event_path(row)
            path.parent.mkdir(parents=True,exist_ok=True)
            temporary=path.with_suffix('.tmp')
            with temporary.open('wb') as handle:
                np.savez(handle,**saved)
            temporary.replace(path)
            new_count+=1
        saved,weight,path,loop_path=load_event(row)
        maximum_null=max(maximum_null,float(saved['event_energy_null']))
        inputs.extend([path,loop_path])
        elapsed=time.monotonic()-started
        progress=dict(state='running',band=band,part=part,completed_nodes=ordinal+1,total_nodes=len(selected),
            new_nodes_this_run=new_count,reused_values=shared_count,pid=os.getpid(),
            elapsed_seconds=elapsed,updated_utc=datetime.now(timezone.utc).isoformat())
        write_json(folder/'progress.json',progress)
        if (ordinal+1)%36==0:
            print(json.dumps(progress),flush=True)
    checks=[dict(name='All fixed-geometry band events evaluated or authenticated reused values',passed=True)]
    test(checks,'Independent event photon gas exchange',maximum_null,1e-10)
    finish(folder,dict(checks=checks,band=band,part=part,events=len(selected),reused_values=shared_count,
        new_nodes_this_run=new_count,elapsed_seconds=time.monotonic()-started),__file__,inputs)
    write_json(folder/'progress.json',dict(state='complete',completed_nodes=len(selected),total_nodes=len(selected),
        new_nodes_this_run=new_count,reused_values=shared_count,pid=os.getpid(),updated_utc=datetime.now(timezone.utc).isoformat()))
    return True


if __name__=='__main__':
    modest()
    parser=argparse.ArgumentParser()
    parser.add_argument('--band',type=int,choices=[3,4],required=True)
    parser.add_argument('--part',type=int,choices=[0,1],required=True)
    parser.add_argument('--stop-at',default='2026-10-18T20:00:00+00:00')
    args=parser.parse_args()
    if not run(args.band,args.part,datetime.fromisoformat(args.stop_at)):
        raise SystemExit(75)

