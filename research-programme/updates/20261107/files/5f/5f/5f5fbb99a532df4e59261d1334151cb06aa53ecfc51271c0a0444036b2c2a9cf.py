from common223 import *

def prepare_tail():
    protocol()
    assert not (ROOT/'tail-configuration.json').exists()
    write(ROOT/'tail-configuration.json',dict(frozen_at=now(),script_sha256=digest(__file__),
        derivation_sha256=digest(ROOT/'TAIL-DERIVATION.md'),
        counts=[4096,2048],models=list(MODELS),working_digits=40,audit_digits=80,
        identity_tolerance=1e-10,comparison_tolerance=.01,initial_fraction=TARGET_FRACTION,final_fraction=1.,
        scope='Coupled propagation of the isolated interval contribution; no unknown incoming term is set to zero',
        bank_changed=False,grids_changed=False,curve_changed=False,tolerances_changed=False))

def tail_protocol():
    protocol()
    config=read(ROOT/'tail-configuration.json')
    assert digest(__file__)==config['script_sha256']
    assert digest(ROOT/'TAIL-DERIVATION.md')==config['derivation_sha256']
    return config

def parent_window(model,count):
    folder=ROOT/f'window/{model}-{count}'
    report=read(folder/'complete.json')
    assert not report['failed_checks'],report['failed_checks']
    for name,value in report['file_hashes'].items():
        assert digest(folder/name)==value,name
    return folder

def run_case(model,count,deadline):
    config=tail_protocol()
    source_folder=parent_window(model,count)
    inputs=read(ROOT/f'inputs-window-{model}-{count}.json')
    system=old.matched.System(model,count,inputs)
    start=indices(count)[2]
    folder=ROOT/f'tail/{model}-{count}'
    if (folder/'complete.json').exists():
        return
    began=time.monotonic()
    with mp.workdps(40):
        delta=mp.mpf(float(system.step))
        alpha=mp.mpf('1.5')/delta
        if (folder/'restart.json').exists():
            record=read(folder/'restart.json')
            assert record['runner_sha256']==digest(__file__)
            current=parse(record['current']);older=parse(record['older'])
            begin=record['index'];rows=record['checks']
        else:
            stored=packet(source_folder/f'step-{start}.npz')
            current=matrix(stored['high'][:,2*WIDTH:])+matrix(stored['low'][:,2*WIDTH:])
            older=matrix(stored['previous_high'][:,2*WIDTH:])+matrix(stored['previous_low'][:,2*WIDTH:])
            begin=start;rows=[]
        zero=zero_source(WIDTH)
        for index in range(begin+1,count+1):
            step=system.make_step(index)
            assert not step['restart']
            solver=Physical(system,step,alpha)
            history_term=(2*current-mp.mpf('.5')*older)/delta
            updated=solver.solve(history_term,zero)
            if index in (start+1,start+(count-start)//2,count) or index%128==0:
                solver.diagnostics(updated,history_term,zero,rows,f'tail{index}')
                with mp.workdps(80):
                    auditor=Physical(system,step,mp.mpf('1.5')/mp.mpf(float(system.step)))
                    audit=auditor.solve(history_term,zero)
                    for name,row in (('energy',0),('gas',96),('work',97),('number',98)):
                        ratios=[abs(audit[row,column]-updated[row,column])/max(abs(audit[row,column]),mp.mpf('1e-300')) for column in range(WIDTH)]
                        check(rows,f'tail{index}:40/80:'+name,max(ratios),1e-10,'identity')
                    check(rows,f'tail{index}:40/80 photon',relative(audit[:96,:],updated[:96,:]),1e-10,'identity')
            balances(updated,system,rows,f'tail{index}')
            check(rows,f'tail{index}:zero control',max(abs(value) for value in updated[:,WIDTH-1]),0,'identity')
            older,current=current,updated
            if index%16==0 or index==count:
                high,low=split(current);previous_high,previous_low=split(older)
                if index in (start+(count-start)//2,count):
                    save(folder/f'step-{index}.npz',high=high,low=low,previous_high=previous_high,previous_low=previous_low,index=index)
                write(folder/'restart.json',dict(index=index,current=serial(current),older=serial(older),checks=rows,runner_sha256=digest(__file__)))
                print(json.dumps(dict(model=model,count=count,index=index,target=count,seconds=time.monotonic()-began,
                    failed=sum(not row['passed'] for row in rows))),flush=True)
                if index<count and datetime.now(timezone.utc)>=deadline:
                    return
        readout(folder,'increment',current,system)
        failed=[row for row in rows if not row['passed']]
        write(folder/'complete.json',dict(model=model,count=count,checks=rows,failed_checks=failed,qualified=not failed,
            finished_at=now(),seconds=time.monotonic()-began,scope=config['scope'],
            file_hashes={path.name:digest(path) for path in folder.iterdir() if path.is_file() and path.name!='complete.json'}))
        write(ROOT/f'inputs-tail-{model}-{count}.json',inputs)
        print(json.dumps(dict(model=model,count=count,complete=True,checks=len(rows),failed=len(failed),seconds=time.monotonic()-began)),flush=True)

if __name__=='__main__':
    old.source.modest()
    parser=argparse.ArgumentParser()
    parser.add_argument('phase',choices=['prepare','run'])
    parser.add_argument('--model',choices=MODELS)
    parser.add_argument('--stop-at',default='2026-10-26T14:20:00+00:00')
    args=parser.parse_args()
    if args.phase=='prepare':
        prepare_tail()
    else:
        for count in (4096,2048):
            run_case(args.model,count,datetime.fromisoformat(args.stop_at))
            if not (ROOT/f'tail/{args.model}-{count}/complete.json').exists():
                break

