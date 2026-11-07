from refine222 import *
sys.path.insert(0,str(PARENT))
import response221 as old
from types import SimpleNamespace

def matrix(values):
    return mp.matrix([[mp.mpf(float(value)) for value in row] for row in values])

def exact_pair(values):
    width=values.shape[1]//2
    return matrix(values[:,:width])+matrix(values[:,width:])

def serial(values):
    return [[str(values[row,column]) for column in range(values.cols)] for row in range(values.rows)]

def parse(values):
    return mp.matrix([[mp.mpf(value) for value in row] for row in values])

def selected_columns():
    total=[int(np.ravel_multi_index((profile,grid,5,join),(2,3,6,2))) for profile,grid,join in np.ndindex(2,2,2)]
    controls=[int(np.ravel_multi_index((0,1,component,join),(2,3,6,2))) for component in (0,4) for join in (0,1)]
    return total+controls

def prepare_matching():
    protocol()
    path=ROOT/'matching-configuration.json'
    assert not path.exists()
    write(path,dict(frozen_at=now(),script_sha256=digest(__file__),derivation_sha256=digest(ROOT/'MATCHING-DERIVATION.md'),
        columns=selected_columns(),counts=[2048,4096],working_digits=80,audit_digits=100,
        identity_tolerance=1e-10,old_diagnosis_sha256=digest(PARENT/'results/matching-roundoff-diagnosis.json'),
        scope='All eight total columns plus four quadratic-quarter baseline/MTS controls, each independently joint/homogeneous/increment',
        startup='unchanged original BDF2, not causal-start candidate'))

def matching_protocol():
    protocol()
    config=read(ROOT/'matching-configuration.json')
    assert digest(__file__)==config['script_sha256']
    assert digest(ROOT/'MATCHING-DERIVATION.md')==config['derivation_sha256']
    assert digest(PARENT/'results/matching-roundoff-diagnosis.json')==config['old_diagnosis_sha256']
    return config

def concatenate(parts):
    result=mp.matrix(parts[0].rows,sum(part.cols for part in parts))
    offset=0
    for part in parts:
        result[:,offset:offset+part.cols]=part
        offset+=part.cols
    return result

class Precise:
    def __init__(self,system,step):
        self.system=system
        self.step=step
        self.alpha=mp.mpf(float(step['alpha']))
        self.rate=mp.mpf(float(step['rate']))
        self.heat=mp.mpf(float(step['heat']))
        self.delta=mp.mpf(float(system.step))
        self.mass=matrix(system.coordinates.mass)
        projected=system.coordinates.tests@step['stiffness']@system.coordinates.transform
        binary=step['alpha']*system.coordinates.mass-step['rate']*projected
        self.operator=matrix(binary)
        self.decomposition,self.permutation=mp.mp.LU_decomp(self.operator)
        self.response=self.solve(matrix(step['coupling'][:,None]))
        self.denominator=self.heat*(self.alpha+1)+self.alpha*self.response[0]
        assert self.denominator>0
        self.chemical=matrix(system.basis.chemical[None,:])
        self.stiffness=matrix(step['stiffness'])
        self.transform=matrix(system.coordinates.transform)
        self.temperature=matrix(system.basis.temperature[:,None])
        self.number_operator=self.chemical*self.stiffness*self.transform
        self.number_gas=(self.chemical*self.stiffness*self.temperature)[0]

    def solve(self,rhs):
        result=mp.matrix(rhs.rows,rhs.cols)
        for column in range(rhs.cols):
            result[:,column]=mp.mp.U_solve(self.decomposition,mp.mp.L_solve(self.decomposition,rhs[:,column],self.permutation))
        return result

    def advance(self,current,older,force,spectral,pair):
        history_term=(2*current-mp.mpf('.5')*older)/self.delta
        free=self.solve(self.mass*history_term[:96,:]+self.rate*force)
        output=mp.matrix(100,current.cols)
        for column in range(current.cols):
            gas=(history_term[0,column]-self.alpha*free[0,column]+self.heat*history_term[96,column]+self.rate*pair[column])/self.denominator
            for row in range(96):
                output[row,column]=free[row,column]+self.response[row]*gas
            output[0,column]=(history_term[0,column]+self.heat*history_term[96,column]-self.heat*(self.alpha+1)*gas+self.rate*pair[column])/self.alpha
            output[96,column]=gas
            output[97,column]=(history_term[97,column]+self.heat*gas)/self.alpha
            output[99,column]=(history_term[99,column]+self.rate*pair[column])/self.alpha
        number=self.number_operator*output[:96,:]-self.number_gas*output[96:97,:]+self.chemical*spectral
        for column in range(current.cols):
            output[98,column]=(history_term[98,column]+self.rate*number[column])/self.alpha
        return output

def check_matching(values,width,rows,label):
    records=[]
    for field,row in (('energy',0),('gas',96),('work',97),('number',98),('injection',99)):
        for column in range(width):
            joint=values[row,column]
            expected=values[row,width+column]+values[row,2*width+column]
            scale=max(abs(expected),mp.mpf('1e-300'))
            relative=abs(joint-expected)/scale
            check(rows,f'{label}:{field}:{column}',relative,1e-10,'identity')
            records.append(float(relative))
    return max(records)

def run_case(model,count,deadline):
    config=matching_protocol()
    columns=config['columns']
    width=len(columns)
    folder=ROOT/f'precise-matching/{model}-{count}'
    if (folder/'complete.json').exists():
        return
    rows=[];inputs=read(ROOT/'inputs.json')
    system=old.matched.System(model,count,inputs)
    incoming=packet(PARENT/f'responses/{model}-{count}/incoming.npz')
    chosen=columns+[column+old.WIDTH for column in columns]
    start=int(incoming['index']);stop=round((old.STOP-.75)*count/.25)
    failures=[record for record in read(PARENT/'results/matching-roundoff-diagnosis.json')['records'] if record['model']==model and record['count']==count]
    audit_indices={record['index'] for record in failures}|{stop}
    began=time.monotonic()
    with mp.workdps(80):
        if (folder/'restart.json').exists():
            saved=read(folder/'restart.json')
            current=parse(saved['current']);older=parse(saved['older']);begin=saved['index']
            records=saved['records'];rows=saved['checks']
        else:
            initial=exact_pair(incoming['current'][:,chosen])
            previous=exact_pair(incoming['previous'][:,chosen])
            current=concatenate([initial,initial,mp.matrix(100,width)])
            older=concatenate([previous,previous,mp.matrix(100,width)])
            begin=start;records=[]
        for index in range(begin+1,stop+1):
            step=system.make_step(index)
            assert not step['restart']
            values,report=old.verify_point(model,index*(old.FINE//count))
            source=old.pair_source(values,system,rows,f'{index}:source')
            original=exact_pair(source['original'][:,chosen])
            force_single=exact_pair(source['force'][:,chosen])
            spectral_single=exact_pair(source['spectral'][:,chosen])
            force=concatenate([force_single,mp.matrix(96,width),force_single])
            spectral=concatenate([spectral_single,mp.matrix(96,width),spectral_single])
            pair_single=original[0:1,:]+original[97:98,:]
            pair=concatenate([pair_single,mp.matrix(1,width),pair_single])
            solver=Precise(system,step)
            updated=solver.advance(current,older,force,spectral,pair)
            maximum=check_matching(updated,width,rows,f'step{index}')
            if index in audit_indices:
                with mp.workdps(100):
                    audit_solver=Precise(system,step)
                    audit=audit_solver.advance(current,older,force,spectral,pair)
                    for field,row in (('energy',0),('gas',96),('work',97),('number',98)):
                        ratios=[abs(updated[row,column]-audit[row,column])/max(abs(audit[row,column]),mp.mpf('1e-300')) for column in range(updated.cols)]
                        check(rows,f'{index}:80/100:{field}',max(ratios),1e-10,'identity')
                for record in failures:
                    if record['index']!=index:
                        continue
                    column=columns.index(record['column'])
                    row=0 if record['field']=='energy' else 96
                    new_joint=updated[row,column]
                    new_split=updated[row,width+column]+updated[row,2*width+column]
                    records.append(dict(original=record,precise_joint=str(new_joint),precise_split=str(new_split),
                        precise_matching_relative=float(abs(new_joint-new_split)/max(abs(new_split),mp.mpf('1e-300'))),
                        binary_joint_change_relative=float(abs(mp.mpf(record['actual'])-new_joint)/max(abs(new_joint),mp.mpf('1e-300'))),
                        binary_split_change_relative=float(abs(mp.mpf(record['expected'])-new_split)/max(abs(new_split),mp.mpf('1e-300')))))
            older,current=current,updated
            if index%8==0 or index==stop:
                write(folder/'restart.json',dict(index=index,current=serial(current),older=serial(older),checks=rows,records=records,runner_sha256=digest(__file__)))
                print(json.dumps(dict(model=model,count=count,index=index,stop=stop,seconds=time.monotonic()-began,matching=maximum)),flush=True)
                if index<stop and datetime.now(timezone.utc)>=deadline:
                    print(json.dumps(dict(model=model,count=count,state='safe_restart',index=index)),flush=True)
                    return
        expected=current[96,width]+current[96,2*width]
        negative=abs((current[96,0]+mp.mpf('1e-6')*expected)-expected)/max(abs(expected),mp.mpf('1e-300'))
        check(rows,'independent joint corruption detected',int(negative<=mp.mpf('1e-10')),0,'negative_control')
        for scope,offset in (('joint',0),('homogeneous',width),('increment',2*width)):
            state=current[:,offset:offset+width]
            high=np.array([[float(state[row,column]) for column in range(width)] for row in range(100)])
            low=np.array([[float(state[row,column]-mp.mpf(float(state[row,column]))) for column in range(width)] for row in range(100)])
            save(folder/f'{scope}.npz',high=high,low=low,columns=columns)
    failed=[row for row in rows if not row['passed']]
    write(folder/'complete.json',dict(model=model,count=count,checks=rows,failed_checks=failed,qualified=not failed,records=records,
        original_failed_records_retested=len(records),seconds=time.monotonic()-began,
        scope=config['scope'],file_hashes={path.name:digest(path) for path in folder.iterdir() if path.is_file() and path.name!='complete.json'}))
    write(ROOT/f'inputs-matching-{model}-{count}.json',inputs)
    print(json.dumps(dict(model=model,count=count,complete=True,checks=len(rows),failed=len(failed),old_failures_retested=len(records))),flush=True)

if __name__=='__main__':
    old.source.modest()
    parser=argparse.ArgumentParser()
    parser.add_argument('phase',choices=['prepare','run'])
    parser.add_argument('--model',choices=MODELS)
    parser.add_argument('--stop-at',default='2026-10-26T12:00:00+00:00')
    args=parser.parse_args()
    if args.phase=='prepare':
        prepare_matching()
    else:
        for count in (2048,4096):
            run_case(args.model,count,datetime.fromisoformat(args.stop_at))
            if not (ROOT/f'precise-matching/{args.model}-{count}/complete.json').exists():
                break

