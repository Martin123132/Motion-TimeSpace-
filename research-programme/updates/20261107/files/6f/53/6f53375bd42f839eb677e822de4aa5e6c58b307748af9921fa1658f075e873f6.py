from __future__ import annotations
import os
for variable in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[variable]='1'
import sys
sys.dont_write_bytecode=True
from pathlib import Path
from datetime import datetime,timezone
import argparse,hashlib,json,math,time
ROOT=Path(__file__).resolve().parent
BRANCH=ROOT.parent
PARENT=BRANCH/'full-panel-short-history-response-20261026'
sys.path[:0]=[str(BRANCH/'farther-cold-operator-bridge-20261023')]
import evolve200 as evolution
np,mp= evolution.np,evolution.mp
history=evolution.history
read,write,save,packet,digest,check=evolution.read,evolution.write,evolution.save,evolution.packet,evolution.digest,evolution.check
PARENT_SHA='69d710e77dac74778ba881ddb860e3432da11eb9f31f86d71eeaa3989cc243fc'
MODELS=('heavy','cold')

def now():
    return datetime.now(timezone.utc).isoformat()

def protocol():
    config=read(ROOT/'configuration.json')
    for name,value in config['protocol_hashes'].items():
        assert digest(ROOT/name)==value,name
    return config

def prepare():
    assert not (ROOT/'configuration.json').exists()
    parent=PARENT/'results/stage-integrity.json'
    assert digest(parent)==PARENT_SHA
    seal=read(parent)
    inputs=dict(seal['consumed_and_immediate_rehashed'])
    inputs.update({str(PARENT/name):value for name,value in seal['file_hashes'].items()})
    inputs[str(parent)]=PARENT_SHA
    for name,value in inputs.items():
        assert digest(name)==value,name
    rows=[]
    schedules={}
    for model in MODELS:
        originals={grid:history.previous.corner.history(model,grid) for grid in ('half','quarter')}
        quarter=originals['quarter']
        start=float(quarter['expansion'][0])
        nominal=float(quarter['step'])/2
        previous_step=float(quarter['step'])*4
        warm_end=float(quarter['expansion'][-1])
        transition=float(read(evolution.PARENT/f'histories/{model}/quarter/complete.json')['coordinate'])
        end=.90625*math.log(10)
        coordinates=[]
        index=1
        while start+index*nominal < end-1e-14:
            coordinates.append(start+index*nominal)
            index+=1
        for boundary in (warm_end,transition,end):
            near=[value for value in coordinates if abs(value-boundary)<1e-14]
            if near:
                coordinates[coordinates.index(near[0])]=boundary
            else:
                coordinates.append(boundary)
        coordinates=sorted(coordinates)
        with mp.workdps(80):
            initial,older=history.seeds(model,'quarter')
            other,other_older=history.seeds(model,'half')
            serial=history.previous.serial_state
            assert serial(initial)==serial(other) and serial(older)==serial(other_older)
            for grid in ('half','quarter'):
                reference_path=history.directory(model,'candidate',grid)/'reference.json'
                reference=read(reference_path)
                assert reference['initial']==serial(initial) and reference['previous']==serial(older)
                inputs[str(reference_path)]=digest(reference_path)
            seed=dict(current=serial(initial),older=serial(older),coordinate=start,previous_coordinate=start-previous_step,
                      previous_step=previous_step,native_start_index=int(quarter['start_index']),
                      scope='Exact shared stored binary64 initial pair, lifted to 80 digits; pre-seed continuum error not certified')
            write(ROOT/f'frozen/{model}-seed.json',seed)
        check(rows,model+':same initial epoch',start-float(originals['half']['expansion'][0]),0,'integrity')
        check(rows,model+':half spacing',float(originals['half']['step'])-nominal*4,0,'integrity')
        schedules[model]=dict(start=start,warm_end=warm_end,transition=transition,end=end,nominal_step=nominal,
            previous_step=previous_step,coordinates=coordinates,updates=len(coordinates))
    for module in list(sys.modules.values()):
        name=getattr(module,'__file__',None)
        if name and Path(name).suffix=='.py' and Path(name).resolve().is_relative_to(BRANCH) and not Path(name).resolve().is_relative_to(ROOT):
            inputs[str(Path(name))]=digest(name)
    config=dict(stage=222,started_utc=now(),parent_sha256=PARENT_SHA,source_prediction_tolerance=.01,identity_tolerance=1e-10,
        working_digits=80,audit_digits=100,models=list(MODELS),schedules=schedules,
        protocol_hashes={name:digest(ROOT/name) for name in ('refine222.py','ACCEPTANCE.md','DERIVATION.md')},
        seed_hashes={model:digest(ROOT/f'frozen/{model}-seed.json') for model in MODELS},
        constraints='Original bank, response grids, source nodes, global temperature curve and gates unchanged',
        bookmarks={str(path):digest(path) for path in (BRANCH/'RESUME-CURRENT.md',BRANCH.parent/'CURRENT_LOCAL_RESUME.md')})
    write(ROOT/'inputs.json',inputs)
    write(ROOT/'configuration.json',config)
    write(ROOT/'results/seed-identity.json',dict(checks=rows,failed_checks=[row for row in rows if not row['passed']]))
    print(json.dumps(dict(state='frozen',inputs=len(inputs),updates={model:schedules[model]['updates'] for model in MODELS})),flush=True)

class Equation(evolution.Equation):
    def __init__(self,model,transition):
        super().__init__(model)
        self.transition=transition

    def stiffness(self,coordinate):
        if float(coordinate)<=self.transition:
            local=self.operator.background.at(float(coordinate))
            offset=float(np.log(local['thermal_parameter']/self.theta0))
            scattering=evolution.smooth.candidate(offset,self.frozen)
            damping=self.operator.emission.at(local['thermal_parameter'],'dcbr')
            rate=local['coefficient']/local['thermal_parameter']
            return evolution.smooth.corner.mp_matrix(rate*(scattering-damping))
        return super().stiffness(coordinate)

def verify_restart(folder,record,seed_sha):
    chain=seed_sha
    stop=0
    for path in sorted((folder/'blocks').glob('*.json')):
        block=read(path)
        if block['stop']>record['done']:
            continue
        assert block['start']==stop and block['previous_chain']==chain
        assert not block['failed_checks']
        chain=hashlib.sha256((chain+digest(path)).encode()).hexdigest()
        stop=block['stop']
    assert stop==record['done'] and chain==record['chain']

def run(model,seconds):
    config=protocol()
    schedule=config['schedules'][model]
    coordinates=schedule['coordinates']
    folder=ROOT/f'histories/{model}/eighth'
    seed_path=ROOT/f'frozen/{model}-seed.json'
    seed_sha=digest(seed_path)
    assert seed_sha==config['seed_hashes'][model]
    if (folder/'complete.json').exists():
        record=read(folder/'complete.json')
        verify_restart(folder,record,seed_sha)
        print(json.dumps(dict(model=model,reused=True)),flush=True)
        return
    if (folder/'restart.json').exists():
        record=read(folder/'restart.json')
        verify_restart(folder,record,seed_sha)
    else:
        seed=read(seed_path)
        record=dict(done=0,total=len(coordinates),current=seed['current'],older=seed['older'],
            coordinate=seed['coordinate'],previous_coordinate=seed['previous_coordinate'],
            last_step=seed['previous_step'],chain=seed_sha,runner_sha256=digest(__file__))
    assert record['runner_sha256']==digest(__file__)
    began=time.monotonic()
    write(ROOT/f'workers/{model}.json',dict(state='running',pid=os.getpid(),started_at=now()))
    with mp.workdps(80):
        equation=Equation(model,schedule['transition'])
        current,older=history.parse_state(record['current']),history.parse_state(record['older'])
        before=float(record['coordinate'])
        last_step=mp.mpf(record['last_step'])
        states,diagnostics,rows=[],[],[]
        block_start=record['done']
        for ordinal in range(record['done'],len(coordinates)):
            coordinate=coordinates[ordinal]
            delta=mp.mpf(coordinate)-mp.mpf(before)
            updated,diagnostic=equation.advance(current,older,mp.mpf(coordinate),delta,last_step)
            local_rows=history.identity_rows([dict(diagnostic,ordinal=ordinal+1)])
            if ordinal==0 or ordinal==len(coordinates)-1:
                with mp.workdps(100):
                    audit_equation=Equation(model,schedule['transition'])
                    audit,unused=audit_equation.advance(current,older,mp.mpf(coordinate),delta,last_step)
                    norm=lambda vector:mp.sqrt(mp.fsum(value*value for value in vector))
                    check(local_rows,'80/100 profile',norm(audit['profile']-updated['profile'])/norm(audit['profile']),1e-10)
                    check(local_rows,'80/100 gas',(audit['gas']-updated['gas'])/max(abs(audit['gas']),mp.mpf('1e-90')),1e-10)
            rows.extend(local_rows)
            assert all(row['passed'] for row in local_rows),local_rows
            older,current=current,updated
            previous_coordinate,before=before,coordinate
            last_step=delta
            states.append(dict(coordinate=coordinate,state=history.previous.serial_state(current)))
            diagnostics.append(diagnostic)
            final=ordinal==len(coordinates)-1
            if len(states)==8 or final:
                block_path=folder/f'blocks/{block_start:04d}-{ordinal+1:04d}.json'
                write(block_path,dict(start=block_start,stop=ordinal+1,previous_chain=record['chain'],
                    states=states,diagnostics=diagnostics,checks=rows,failed_checks=[row for row in rows if not row['passed']]))
                chain=hashlib.sha256((record['chain']+digest(block_path)).encode()).hexdigest()
                record=dict(done=ordinal+1,total=len(coordinates),current=history.previous.serial_state(current),
                    older=history.previous.serial_state(older),coordinate=coordinate,previous_coordinate=previous_coordinate,
                    last_step=str(last_step),chain=chain,runner_sha256=digest(__file__),seed_sha256=seed_sha,
                    nominal_step=schedule['nominal_step'],elapsed_session_seconds=time.monotonic()-began)
                write(folder/'restart.json',record)
                write(ROOT/f'workers/{model}.json',dict(state='running',pid=os.getpid(),done=ordinal+1,total=len(coordinates),updated_at=now()))
                print(json.dumps(dict(model=model,done=ordinal+1,total=len(coordinates),seconds=time.monotonic()-began)),flush=True)
                states,diagnostics,rows=[],[],[]
                block_start=ordinal+1
                if final:
                    record.update(failed_checks=[],finished_at=now())
                    write(folder/'complete.json',record)
                    break
                if time.monotonic()-began>=seconds:
                    break
    write(ROOT/f'workers/{model}.json',dict(state='finished' if record['done']==len(coordinates) else 'safe_restart',
        pid=os.getpid(),done=record['done'],total=len(coordinates),finished_at=now()))
    print(json.dumps(dict(model=model,state='finished' if record['done']==len(coordinates) else 'safe_restart')),flush=True)

if __name__=='__main__':
    evolution.previous.source.modest()
    parser=argparse.ArgumentParser()
    parser.add_argument('phase',choices=['prepare','run'])
    parser.add_argument('--model',choices=MODELS)
    parser.add_argument('--seconds',type=float,default=6500)
    args=parser.parse_args()
    if args.phase=='prepare':
        prepare()
    else:
        run(args.model,args.seconds)

