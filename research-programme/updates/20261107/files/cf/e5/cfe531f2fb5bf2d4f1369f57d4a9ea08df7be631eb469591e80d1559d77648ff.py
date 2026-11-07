from __future__ import annotations
import os
for variable in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[variable]='1'
import sys
sys.dont_write_bytecode=True
from pathlib import Path
from datetime import datetime,timezone
import argparse
ROOT=Path(__file__).resolve().parent
BRANCH=ROOT.parent
PREVIOUS=BRANCH/'calibrated-stress-gravity-bound-20261026'
sys.path.insert(0,str(PREVIOUS))
import common225 as inherited
parent=inherited.parent
np,mp,math,json=inherited.np,inherited.mp,inherited.math,inherited.json
read,write,save,packet,digest,check=inherited.read,inherited.write,inherited.save,inherited.packet,inherited.digest,inherited.check
register,load=inherited.register,inherited.load
KINETIC=inherited.KINETIC
SEAL='1c5145131f77c6d5b6344b9a2badc244467261ae72c6a0938faf17c58fe1ca0f'
LABELS=parent.LABELS

def now():
    return datetime.now(timezone.utc).isoformat()

def prepare():
    assert not (ROOT/'configuration.json').exists()
    seal_path=PREVIOUS/'results/stage-integrity.json'
    assert digest(seal_path)==SEAL
    seal=read(seal_path)
    assert seal['qualified'] and seal['state']=='complete'
    inputs=dict(seal['consumed_and_immediate_rehashed'])
    inputs.update({str(PREVIOUS/name):value for name,value in seal['file_hashes'].items()})
    inputs[str(seal_path)]=SEAL
    for path,value in inputs.items():
        assert digest(path)==value,path
    for path,value in seal['bookmarks'].items():
        assert digest(path)==value,path
    write(ROOT/'inputs.json',inputs)
    write(ROOT/'configuration.json',dict(stage=226,turn_start='2026-10-26T15:52:59+00:00',prepared_at=now(),
        previous_goal_turn='progress',previous_seal=SEAL,models=list(parent.MODELS),counts=list(parent.COUNTS),
        identity_tolerance=1e-10,refinement_tolerance=.01,working_digits=80,
        source_window=[parent.FIRST_FRACTION,parent.LAST_FRACTION],tail_start=parent.TARGET_FRACTION,
        endpoint=1.,bank_changed=False,curve_changed=False,tolerances_changed=False,
        input_scope='Saved source nodes; explicit piecewise-linear numerical weak-forcing reconstruction; no claim of between-node continuum source accuracy',
        attribution='Zero incoming only for the named interval-generated component; independent earlier physical state remains explicit',
        protocol_hashes={path.name:digest(path) for path in ROOT.iterdir() if path.is_file() and path.suffix in ('.py','.md')}))
    print(json.dumps(dict(prepared=True,inputs=len(inputs))),flush=True)

def protocol():
    config=read(ROOT/'configuration.json')
    for name,value in config['protocol_hashes'].items():
        assert digest(ROOT/name)==value,name
    return config

def relative(actual,expected):
    return abs(actual-expected)/max(abs(expected),mp.mpf('1e-300'))

def integrals(coordinates,norms,injection,endpoint):
    area=mp.mpf(0);moment=mp.mpf(0);energy=mp.mpf(0)
    for index in range(len(coordinates)-1):
        first,second=coordinates[index:index+2]
        width=second-first
        left,right=norms[index:index+2]
        area+=width*(left+right)/2
        moment+=width*((endpoint-first)*(left+right)/2-width*(left/6+right/3))
        energy+=width*(abs(injection[index])+abs(injection[index+1]))/2
    return area,moment,energy

def forced_q(heat,defect,coordinates,norms,injection,endpoint):
    area,moment,energy=integrals(coordinates,norms,injection,endpoint)
    return heat*energy+heat**mp.mpf('1.5')*moment+heat*defect*area

def discrete_bounds(heat,spacing,norms,injection,defect):
    first_norm=spacing*(norms[0]+norms[1])/2
    upper=[mp.mpf(0),mp.sqrt(5)*first_norm]
    for value in norms[2:]:
        impulse=2*spacing*value
        upper.append(impulse+mp.sqrt(upper[-1]**2+impulse**2))
    first_density=spacing*(heat**mp.mpf('1.5')*first_norm+heat*abs(injection[0]+injection[1]))/2
    density=[mp.mpf(0)]
    for index in range(1,len(norms)):
        value=mp.mpf('1.5')*(1-mp.mpf(3)**(-index))*first_density
        for earlier in range(2,index+1):
            kernel=spacing*(1-mp.mpf(3)**(-(index-earlier+1)))
            value+=kernel*(heat**mp.mpf('1.5')*upper[earlier]+heat*abs(injection[earlier]))
        density.append(value+heat*defect*(first_norm if index==1 else upper[index]))
    return upper,density

if __name__=='__main__':
    parent.old.source.modest()
    prepare()

