from common223 import *

def history_term(current,older,step):
    return (2*current-mp.mpf('.5')*older)/step

def run_case(model,count,deadline):
    config=protocol()
    folder=ROOT/f'window/{model}-{count}'
    if (folder/'complete.json').exists():
        return
    inputs=read(ROOT/'inputs.json')
    system=old.matched.System(model,count,inputs)
    start,stop,target=indices(count)
    midpoint=start+(stop-start)//2
    began=time.monotonic()
    with mp.workdps(80):
        delta=mp.mpf(float(system.step))
        alpha_b=mp.mpf('1.5')/delta
        alpha_t=2/delta
        seeds=packet(ROOT/f'frozen/{model}-{count}-incoming.npz')
        rows=[]
        if (folder/'restart.json').exists():
            record=read(folder/'restart.json')
            assert record['runner_sha256']==digest(__file__)
            current,older=parse(record['current']),parse(record['older'])
            wrong=None if record['wrong'] is None else parse(record['wrong'])
            wrong_old=None if record['wrong_old'] is None else parse(record['wrong_old'])
            erased=None if record['erased'] is None else parse(record['erased'])
            erased_old=None if record['erased_old'] is None else parse(record['erased_old'])
            rows=record['checks'];begin=record['index']
        else:
            incoming=exact_pair(seeds['current']);previous=exact_pair(seeds['previous'])
            current=concatenate([incoming,incoming,mp.matrix(100,WIDTH)])
            older=concatenate([previous,previous,mp.matrix(100,WIDTH)])
            wrong=wrong_old=erased=erased_old=None
            begin=start
        for index in range(begin+1,target+1):
            step=system.make_step(index)
            normal=Physical(system,step,alpha_b)
            source=source_at(model,count,index,system,rows) if index<=stop else zero_source(WIDTH)
            ordinary_history=history_term(current,older,delta)
            if index==start+1:
                source0=source_at(model,count,start,system,rows)
                total_source=add_sources(source0,source)
                homogeneous=normal.solve(ordinary_history[:,:WIDTH],zero_source(WIDTH))
                trap=Physical(system,step,alpha_t)
                joint_history=ordinary_history[:,WIDTH:2*WIDTH]+(alpha_t-alpha_b)*homogeneous
                joint=trap.solve(joint_history,total_source)
                increment=trap.solve(mp.matrix(100,WIDTH),total_source)
                updated=concatenate([homogeneous,joint,increment])
                trap.diagnostics(increment,mp.matrix(100,WIDTH),total_source,rows,'left boundary')
                active_solver=trap
            elif index==stop+1:
                homogeneous=normal.solve(ordinary_history[:,:WIDTH],zero_source(WIDTH))
                previous_generator=Physical(system,system.make_step(stop),alpha_b)
                trap=Physical(system,step,alpha_t)
                increment_rhs=alpha_t*current[:,2*WIDTH:]+previous_generator.derivative(current[:,2*WIDTH:])
                difference=current[:,WIDTH:2*WIDTH]-current[:,:WIDTH]
                joint_rhs=ordinary_history[:,:WIDTH]+(alpha_t-alpha_b)*homogeneous+alpha_t*difference+previous_generator.derivative(difference)
                joint=trap.solve(joint_rhs,zero_source(WIDTH))
                increment=trap.solve(increment_rhs,zero_source(WIDTH))
                updated=concatenate([homogeneous,joint,increment])
                trap.diagnostics(increment,increment_rhs,zero_source(WIDTH),rows,'right boundary')
                wrong_old=selected(current[:,2*WIDTH:],NEGATIVE)
                wrong=normal.solve(history_term(wrong_old,selected(older[:,2*WIDTH:],NEGATIVE),delta),zero_source(len(NEGATIVE)))
                active_solver=trap
            else:
                sources=multi_source([zero_source(WIDTH),source,source])
                updated=normal.solve(ordinary_history,sources)
                if index in (midpoint,stop,target):
                    normal.diagnostics(updated[:,2*WIDTH:],ordinary_history[:,2*WIDTH:],source,rows,f'step{index}')
                active_solver=normal
                if wrong is not None:
                    new_wrong=normal.solve(history_term(wrong,wrong_old,delta),zero_source(len(NEGATIVE)))
                    wrong_old,wrong=wrong,new_wrong
            if erased is not None:
                if index==stop+1:
                    rhs=alpha_t*erased+previous_generator.derivative(erased)
                    new_erased=trap.solve(rhs,zero_source(len(NEGATIVE)))
                else:
                    new_erased=normal.solve(history_term(erased,erased_old,delta),sub_source(source,NEGATIVE))
                erased_old,erased=erased,new_erased
            if index in (start+1,stop+1,target):
                with mp.workdps(100):
                    if index==start+1:
                        auditor=Physical(system,step,alpha_t)
                        audit=auditor.solve(mp.matrix(100,WIDTH),total_source)
                    elif index==stop+1:
                        auditor=Physical(system,step,alpha_t)
                        audit=auditor.solve(increment_rhs,zero_source(WIDTH))
                    else:
                        auditor=Physical(system,step,alpha_b)
                        audit=auditor.solve(ordinary_history[:,2*WIDTH:],source)
                    check(rows,f'step{index}:80/100 increment photon',relative(audit[:96,:],updated[:96,2*WIDTH:]),1e-10,'identity')
                    for name,row in (('energy',0),('gas',96),('work',97),('number',98)):
                        ratios=[abs(audit[row,column]-updated[row,2*WIDTH+column])/max(abs(audit[row,column]),mp.mpf('1e-300')) for column in range(WIDTH)]
                        check(rows,f'step{index}:80/100 '+name,max(ratios),1e-10,'identity')
            older,current=current,updated
            matching(current,system,rows,f'step{index}')
            balances(current[:,2*WIDTH:],system,rows,f'step{index}:increment')
            balances(current[:,WIDTH:2*WIDTH],system,rows,f'step{index}:joint')
            if index==midpoint:
                erased=selected(current[:,2*WIDTH:],NEGATIVE)
                erased_old=erased.copy()
            if index in (start+1,midpoint,stop,stop+1,target):
                high,low=split(current);previous_high,previous_low=split(older)
                save(folder/f'step-{index}.npz',high=high,low=low,previous_high=previous_high,previous_low=previous_low,index=index)
            if index%8==0 or index==target:
                write(folder/'restart.json',dict(index=index,current=serial(current),older=serial(older),checks=rows,
                    wrong=None if wrong is None else serial(wrong),wrong_old=None if wrong_old is None else serial(wrong_old),
                    erased=None if erased is None else serial(erased),erased_old=None if erased_old is None else serial(erased_old),
                    runner_sha256=digest(__file__)))
                print(json.dumps(dict(model=model,count=count,index=index,target=target,seconds=time.monotonic()-began,
                    failed=sum(not row['passed'] for row in rows))),flush=True)
                if index<target and datetime.now(timezone.utc)>=deadline:
                    return
        for label,value in (('increment',current[:,2*WIDTH:]),('homogeneous',current[:,:WIDTH]),('joint',current[:,WIDTH:2*WIDTH])):
            readout(folder,label,value,system)
        reference=selected(current[:,2*WIDTH:],NEGATIVE)
        negative_records=[]
        for name,value in (('naive_exit',wrong),('erased_previous',erased)):
            error=relative(value,reference)
            check(rows,name+' detected',int(error<=mp.mpf('1e-10')),0,'negative_control')
            high,low=split(value);save(folder/f'negative-{name}.npz',high=high,low=low,columns=NEGATIVE)
            for component in ('baseline','MTS','total'):
                columns=[position for position,column in enumerate(NEGATIVE) if LABELS[column]['component']==component]
                difference=relative(selected(value,columns),selected(reference,columns))
                check(rows,name+':'+component+' detected',int(difference<=mp.mpf('1e-10')),0,'negative_control')
                negative_records.append(dict(kind=name,component=component,relative=float(difference)))
        failed=[row for row in rows if not row['passed']]
        write(folder/'complete.json',dict(model=model,count=count,checks=rows,failed_checks=failed,qualified=not failed,
            negative_records=negative_records,finished_at=now(),seconds=time.monotonic()-began,
            file_hashes={path.name:digest(path) for path in folder.iterdir() if path.is_file() and path.name!='complete.json'}))
        write(ROOT/f'inputs-window-{model}-{count}.json',inputs)
        print(json.dumps(dict(model=model,count=count,complete=True,checks=len(rows),failed=len(failed),seconds=time.monotonic()-began)),flush=True)

if __name__=='__main__':
    old.source.modest()
    parser=argparse.ArgumentParser()
    parser.add_argument('--model',choices=MODELS,required=True)
    parser.add_argument('--stop-at',default='2026-10-26T14:20:00+00:00')
    args=parser.parse_args()
    for count in COUNTS:
        run_case(args.model,count,datetime.fromisoformat(args.stop_at))
        if not (ROOT/f'window/{args.model}-{count}/complete.json').exists():
            break

