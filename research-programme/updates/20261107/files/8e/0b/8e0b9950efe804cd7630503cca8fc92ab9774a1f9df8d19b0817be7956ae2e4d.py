from __future__ import annotations
import os
for variable in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[variable]='1'
import sys
sys.dont_write_bytecode=True
from pathlib import Path
from datetime import datetime,timezone
import argparse,json,math,time,hashlib
ROOT=Path(__file__).resolve().parent
BRANCH=ROOT.parent
PARENT=BRANCH/'shared-seed-history-refinement-20261026'
sys.path.insert(0,str(PARENT))
import response222 as refined
import matching222 as precision
old=refined.old
np,mp,linear=old.np,old.mp,old.linear
read,write,save,packet,digest,check=old.read,old.write,old.save,old.packet,old.digest,old.check
matrix,parse,serial=precision.matrix,precision.parse,precision.serial
exact_pair,concatenate=precision.exact_pair,precision.concatenate
MODELS=('heavy','cold')
COUNTS=(2048,4096)
COMPONENTS=(0,4,5)
FIRST_FRACTION=.90234375
LAST_FRACTION=.90625
TARGET_FRACTION=.91015625
PARENT_SHA='4b922cfabddf01f9fd82f90d9a32c30c726a360a6f68550d2db251801d8607f0'
COLUMNS=[int(np.ravel_multi_index((profile,grid,component,join),(2,3,6,2))) for profile,grid in np.ndindex(2,2) for component in COMPONENTS for join in (0,1)]
LABELS=[dict(profile=old.PROFILES[profile],grid=('quarter','eighth')[grid],component=old.COMPONENTS[component],join=join)
        for profile,grid in np.ndindex(2,2) for component in COMPONENTS for join in (0,1)]
COLUMNS.append(int(np.ravel_multi_index((0,2,0,0),(2,3,6,2))))
LABELS.append(dict(profile='zero',grid='zero',component='zero',join=0))
WIDTH=len(COLUMNS)
NEGATIVE=[index for index,label in enumerate(LABELS) if label['profile']=='quadratic' and label['grid']=='eighth']

def now():
    return datetime.now(timezone.utc).isoformat()

def protocol():
    config=read(ROOT/'configuration.json')
    for name,value in config['protocol_hashes'].items():
        assert digest(ROOT/name)==value,name
    return config

def indices(count):
    return tuple(round((fraction-.75)*count/.25) for fraction in (FIRST_FRACTION,LAST_FRACTION,TARGET_FRACTION))

def prepare():
    assert not (ROOT/'configuration.json').exists()
    seal_path=PARENT/'results/stage-integrity.json'
    assert digest(seal_path)==PARENT_SHA
    seal=read(seal_path)
    assert seal['qualified']
    inputs=dict(seal['consumed_and_immediate_rehashed'])
    inputs.update({str(PARENT/name):value for name,value in seal['file_hashes'].items()})
    inputs[str(seal_path)]=PARENT_SHA
    for name,value in inputs.items():
        assert digest(name)==value,name
    rows=[]
    for model in MODELS:
        for count in COUNTS:
            system=old.matched.System(model,count,inputs)
            source_path=old.ROOT/f'responses/{model}-{count}/incoming.npz'
            incoming=packet(source_path)
            incoming_columns=[]
            for label in LABELS:
                if label['grid']=='zero':
                    incoming_columns.append(int(np.ravel_multi_index((0,2,0,0),(2,3,6,2))))
                else:
                    incoming_columns.append(int(np.ravel_multi_index((0,1,COMPONENTS[('baseline','MTS','total').index(label['component'])],label['join']),(2,3,6,2))))
            selected=incoming_columns+[column+old.WIDTH for column in incoming_columns]
            save(ROOT/f'frozen/{model}-{count}-incoming.npz',current=incoming['current'][:,selected],previous=incoming['previous'][:,selected],
                 original_columns=incoming_columns,source=str(source_path),fraction=FIRST_FRACTION)
            inputs[str(source_path)]=digest(source_path)
            expected=np.r_[1.,np.zeros(95)]
            check(rows,f'{model}:{count}:protected mass energy row',np.max(abs(system.coordinates.mass[0]-expected)),0,'integrity')
            check(rows,f'{model}:{count}:same step',system.step-.25*math.log(10)/count,1e-15,'integrity')
    config=dict(stage=223,turn_start='2026-10-26T10:43:45+00:00',frozen_at=now(),parent_sha256=PARENT_SHA,
        models=list(MODELS),counts=list(COUNTS),columns=COLUMNS,labels=LABELS,width=WIDTH,
        source_window=[FIRST_FRACTION,LAST_FRACTION],short_target=TARGET_FRACTION,
        source_prediction_tolerance=.01,identity_tolerance=1e-10,
        equation_gates=dict(photon=1e-7,gas=1e-8,spectral=1.,ledger=1e-7),
        working_digits=80,audit_digits=100,
        incoming_scope='Same stored quarter-history pair is a TEST INPUT for all histories; actual earlier eighth correction remains an explicit unknown',
        protocol_hashes={path.name:digest(path) for path in list(ROOT.glob('*.py'))+list(ROOT.glob('*.md'))},
        frozen_hashes={path.name:digest(path) for path in (ROOT/'frozen').glob('*.npz')},
        bookmarks={str(path):digest(path) for path in (BRANCH/'RESUME-CURRENT.md',BRANCH.parent/'CURRENT_LOCAL_RESUME.md')},
        bank_changed=False,global_curve_changed=False,response_grids_changed=False,tolerances_changed=False)
    write(ROOT/'inputs.json',inputs)
    write(ROOT/'configuration.json',config)
    write(ROOT/'results/preparation.json',dict(checks=rows,failed_checks=[row for row in rows if not row['passed']]))
    print(json.dumps(dict(state='frozen',inputs=len(inputs),width=WIDTH,window_steps={str(count):indices(count)[2]-indices(count)[0] for count in COUNTS})),flush=True)

def split(values):
    high=np.array([[float(values[row,column]) for column in range(values.cols)] for row in range(values.rows)])
    low=np.array([[float(values[row,column]-mp.mpf(float(values[row,column]))) for column in range(values.cols)] for row in range(values.rows)])
    return high,low

def to_twofold(values):
    high,low=split(values)
    return np.column_stack([high,low])

def norm(values):
    return mp.sqrt(mp.fsum(value*value for value in values))

def relative(first,second):
    return norm(first-second)/max(norm(second),mp.mpf('1e-300'))

def selected(values,columns):
    return concatenate([values[:,column:column+1] for column in columns])

def add_sources(first,second):
    return {key:first[key]+second[key] for key in first}

def zero_source(width):
    return dict(force=mp.matrix(96,width),spectral=mp.matrix(96,width),raw=mp.matrix(98,width),pair=mp.matrix(1,width),number=mp.matrix(1,width))

def source_at(model,count,index,system,rows):
    fine_index=index*(4096//count)
    values=refined.verify_source(model,fine_index)
    supplied=old.pair_source(values,system,rows,f'source{index}')
    columns=COLUMNS+[column+old.WIDTH for column in COLUMNS]
    exact={key:exact_pair(supplied[key][:,columns]) for key in ('force','spectral','original')}
    step=system.make_step(index)
    rate=mp.mpf(float(step['rate']))
    weighted={key:rate*exact[key] for key in ('force','spectral')}
    weighted['raw']=rate*exact['original']
    weighted['pair']=weighted['raw'][0:1,:]+weighted['raw'][97:98,:]
    weighted['number']=matrix(system.basis.chemical[None,:])*weighted['spectral']
    return weighted

def sub_source(source,columns):
    return {key:selected(value,columns) for key,value in source.items()}

def multi_source(parts):
    return {key:concatenate([source[key] for source in parts]) for key in parts[0]}

class Physical:
    def __init__(self,system,step,alpha=None):
        self.system=system
        self.step=step
        self.alpha=mp.mpf(float(step['alpha'])) if alpha is None else alpha
        self.heat=mp.mpf(float(step['heat']))
        self.rate=mp.mpf(float(step['rate']))
        self.mass=matrix(system.coordinates.mass)
        self.projected=self.rate*matrix(system.coordinates.tests@step['stiffness']@system.coordinates.transform)
        self.coupling=matrix(step['coupling'][:,None])
        self.operator=self.alpha*self.mass-self.projected
        self.factor,self.permutation=mp.mp.LU_decomp(self.operator)
        self.response=self.solve_matrix(self.coupling)
        self.denominator=self.heat*(self.alpha+1)+self.alpha*self.response[0]
        assert self.denominator>0
        self.transform=matrix(system.coordinates.transform)
        self.physical_mass=matrix(system.basis.mass)
        self.stiffness=matrix(step['stiffness'])
        self.temperature=matrix(system.basis.temperature[:,None])
        self.chemical=matrix(system.basis.chemical[None,:])
        self.number_operator=self.rate*self.chemical*self.stiffness*self.transform
        self.number_gas=(self.rate*self.chemical*self.stiffness*self.temperature)[0]

    def solve_matrix(self,rhs):
        result=mp.matrix(rhs.rows,rhs.cols)
        for column in range(rhs.cols):
            result[:,column]=mp.mp.U_solve(self.factor,mp.mp.L_solve(self.factor,rhs[:,column],self.permutation))
        return result

    def solve(self,history_term,source):
        free=self.solve_matrix(self.mass*history_term[:96,:]+source['force'])
        result=mp.matrix(100,history_term.cols)
        for column in range(result.cols):
            gas=(history_term[0,column]+self.heat*history_term[96,column]+source['pair'][column]-self.alpha*free[0,column])/self.denominator
            for row in range(96):
                result[row,column]=free[row,column]+self.response[row]*gas
            result[96,column]=gas
            result[97,column]=(history_term[97,column]+self.heat*gas)/self.alpha
            result[99,column]=(history_term[99,column]+source['pair'][column])/self.alpha
        number=self.number_operator*result[:96,:]-self.number_gas*result[96:97,:]+source['number']
        for column in range(result.cols):
            result[98,column]=(history_term[98,column]+number[column])/self.alpha
        return result

    def derivative(self,values):
        factor,permutation=mp.mp.LU_decomp(self.mass)
        rhs=self.projected*values[:96,:]+self.coupling*values[96:97,:]
        result=mp.matrix(100,values.cols)
        for column in range(values.cols):
            result[:96,column]=mp.mp.U_solve(factor,mp.mp.L_solve(factor,rhs[:,column],permutation))
            result[96,column]=-result[0,column]/self.heat-values[96,column]
            result[97,column]=self.heat*values[96,column]
        number=self.number_operator*values[:96,:]-self.number_gas*values[96:97,:]
        result[98:99,:]=number
        return result

    def diagnostics(self,updated,history_term,source,rows,label):
        photon=self.transform*updated[:96,:]
        history_photon=self.transform*history_term[:96,:]
        collision=self.rate*self.stiffness*(photon-self.temperature*updated[96:97,:])
        residual=self.physical_mass*(self.alpha*photon-history_photon)-collision-source['raw'][1:97,:]
        maximum=mp.mpf(0)
        for column in range(updated.cols):
            denominator=max(norm(self.physical_mass*history_photon[:,column]+source['raw'][1:97,column]),mp.mpf('1e-300'))
            maximum=max(maximum,norm(residual[:,column])/denominator)
        check(rows,label+':weak photon equation',maximum,1e-7,'equation')
        gas=self.heat*((self.alpha+1)*updated[96:97,:]-history_term[96:97,:])+self.temperature.T*collision-source['raw'][97:98,:]
        check(rows,label+':physical gas equation',max(abs(value) for value in gas),1e-8,'equation')
        energy=matrix(self.system.basis.energy[None,:])*photon
        allowance=[]
        for column in range(updated.cols):
            scale=mp.fsum(abs(mp.mpf(float(self.system.basis.energy[row]))*photon[row,column]) for row in range(96))
            allowance.append(abs(energy[column]-updated[0,column])/max(mp.mpf(256)*mp.mpf(float(np.finfo(float).eps))*scale,mp.mpf('1e-300')))
        check(rows,label+':protected spectral energy',max(allowance),1.,'equation')

def balances(values,system,rows,label):
    heat=mp.mpf(float(system.background.chi))
    photon=matrix(system.coordinates.transform)*values[:96,:]
    number=matrix(system.basis.number[None,:])*photon
    energy_ratios=[];number_ratios=[]
    for column in range(values.cols):
        error=values[0,column]+heat*values[96,column]+values[97,column]-values[99,column]
        scale=abs(values[0,column])+abs(heat*values[96,column])+abs(values[97,column])+abs(values[99,column])
        energy_ratios.append(abs(error)/max(scale,mp.mpf('1e-300')))
        number_ratios.append(abs(number[column]-values[98,column])/max(abs(number[column])+abs(values[98,column]),mp.mpf('1e-300')))
    check(rows,label+':energy/work/pair balance',max(energy_ratios),1e-7,'equation')
    check(rows,label+':number balance',max(number_ratios),1e-7,'equation')

def matching(values,system,rows,label):
    homogeneous=values[:,:WIDTH];joint=values[:,WIDTH:2*WIDTH];increment=values[:,2*WIDTH:]
    expected=homogeneous+increment
    for name,row in (('energy',0),('gas',96),('work',97),('number',98),('injection',99)):
        ratios=[abs(joint[row,column]-expected[row,column])/max(abs(expected[row,column]),mp.mpf('1e-300')) for column in range(WIDTH)]
        check(rows,label+':matching '+name,max(ratios),1e-10,'identity')
    check(rows,label+':matching photon',relative(matrix(system.coordinates.transform)*joint[:96,:],matrix(system.coordinates.transform)*expected[:96,:]),1e-10,'identity')
    check(rows,label+':zero control',max(abs(values[row,block*WIDTH+WIDTH-1]) for block in range(3) for row in range(100)),0,'identity')

def readout(folder,label,values,system):
    pairs=to_twofold(values)
    collapsed=old.matched.collapsed(pairs)
    reader=old.matched.saved.response.ShapeReadout(system.basis,canonical=True)
    shapes=reader.apply(system.coordinates.transform@collapsed[:96],collapsed[0])
    save(folder/f'{label}-readout.npz',**shapes,gas=collapsed[96],work=collapsed[97],number=collapsed[98],
         injection=collapsed[99],heat=system.background.chi,frequency=reader.frequency,measure=reader.measure)

if __name__=='__main__':
    prepare()

