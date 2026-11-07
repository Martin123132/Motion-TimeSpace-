from common223 import *

def replay(model,count):
    protocol()
    folder=ROOT/f'window/{model}-{count}'
    target_folder=ROOT/f'restart-check/{model}-{count}'
    if (target_folder/'complete.json').exists():
        return
    start,stop,target=indices(count)
    midpoint=start+(stop-start)//2
    inputs=read(ROOT/f'inputs-window-{model}-{count}.json')
    system=old.matched.System(model,count,inputs)
    stored=packet(folder/f'step-{midpoint}.npz')
    rows=[]
    with mp.workdps(80):
        current=matrix(stored['high'][:,2*WIDTH:])+matrix(stored['low'][:,2*WIDTH:])
        older=matrix(stored['previous_high'][:,2*WIDTH:])+matrix(stored['previous_low'][:,2*WIDTH:])
        delta=mp.mpf(float(system.step))
        for index in range(midpoint+1,target+1):
            step=system.make_step(index)
            source=source_at(model,count,index,system,rows) if index<=stop else zero_source(WIDTH)
            if index==stop+1:
                before=Physical(system,system.make_step(stop),mp.mpf('1.5')/delta)
                solver=Physical(system,step,2/delta)
                history_term=2/delta*current+before.derivative(current)
            else:
                solver=Physical(system,step,mp.mpf('1.5')/delta)
                history_term=(2*current-mp.mpf('.5')*older)/delta
            updated=solver.solve(history_term,source)
            older,current=current,updated
        terminal=packet(folder/f'step-{target}.npz')
        expected=matrix(terminal['high'][:,2*WIDTH:])+matrix(terminal['low'][:,2*WIDTH:])
        transform=matrix(system.coordinates.transform)
        for column in range(WIDTH):
            check(rows,f'photon column{column}',relative(transform*current[:96,column],transform*expected[:96,column]),1e-10,'identity')
            for name,row in (('energy',0),('gas',96),('work',97),('number',98)):
                check(rows,f'{name} column{column}',abs(current[row,column]-expected[row,column])/max(abs(expected[row,column]),mp.mpf('1e-300')),1e-10,'identity')
        high,low=split(current)
        save(target_folder/'replayed.npz',high=high,low=low)
    write(target_folder/'complete.json',dict(model=model,count=count,checks=rows,failed_checks=[row for row in rows if not row['passed']],
        source_checkpoint=str(folder/f'step-{midpoint}.npz'),target_checkpoint=str(folder/f'step-{target}.npz'),
        file_hashes={'replayed.npz':digest(target_folder/'replayed.npz')},script_sha256=digest(__file__)))
    print(json.dumps(dict(model=model,count=count,restart_checks=len(rows),failed=sum(not row['passed'] for row in rows))),flush=True)

if __name__=='__main__':
    old.source.modest()
    parser=argparse.ArgumentParser()
    parser.add_argument('--model',required=True,choices=MODELS)
    args=parser.parse_args()
    for count in COUNTS:
        replay(args.model,count)

