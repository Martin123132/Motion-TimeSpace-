from __future__ import annotations
import os
for variable in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[variable]='1'
import sys
sys.dont_write_bytecode=True
from pathlib import Path
import json, math, hashlib, time
from datetime import datetime, timezone
ROOT=Path(__file__).resolve().parent
BRANCH=ROOT.parent
PARENT=BRANCH/'upper-edge-repaired-source-panel-20261022'
sys.path[:0]=[str(PARENT),str(BRANCH/'final-spectrum-uncertainty-20261019')]
import source_stage196 as panel
import stage167_common as response
import numpy as np
from scipy import linalg
from decimal import Decimal, localcontext
SEAL='c45d397eeccedd8a3b28f174dc687585ab4ba8e867ad2cd6cd9254068da9b9e1'
TAGS=['minus','minus_half','anchor','plus_half','plus']
OFFSETS=np.array([-.01,-.005,0.,.005,.01])
VERSIONS=['original','bank-half-delta','bank-quarter-delta','candidate-half-delta','candidate-quarter-delta','candidate-quarter']
KINDS=['baseline','MTS','total']
LABELS=[f'{version}:{kind}:join{join}' for version in VERSIONS for kind in KINDS for join in (0,1)]+['zero']

def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))

def write(path,value):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    temporary=path.with_suffix(path.suffix+'.partial')
    temporary.write_text(json.dumps(value,indent=2,allow_nan=False)+'\n',encoding='utf-8')
    temporary.replace(path)

def save(path,**values):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    temporary=path.with_suffix('.partial')
    with temporary.open('wb') as stream:
        np.savez_compressed(stream,**values)
    temporary.replace(path)

def packet(path):
    with np.load(path,allow_pickle=False) as archive:
        return {name:archive[name].copy() for name in archive.files}

def check(rows,name,value,limit,category='numerical'):
    value=float(abs(value))
    rows.append(dict(name=name,value=value if math.isfinite(value) else None,limit=limit,
                     passed=bool(math.isfinite(value) and value<=limit),category=category))

def parts_sum(high,low):
    shape=high.shape[1:]
    upper=np.empty(shape);lower=np.empty(shape)
    for index in np.ndindex(shape):
        terms=[float(value) for value in high[(slice(None),)+index]]
        terms.extend(float(value) for value in low[(slice(None),)+index])
        value=math.fsum(terms)
        upper[index]=value;lower[index]=math.fsum([*terms,-value])
    return upper,lower

def register(inputs,path,expected=None):
    path=Path(path).resolve();value=digest(path)
    if expected is not None:
        assert value==expected,str(path)
    if str(path) in inputs:
        assert inputs[str(path)]==value,str(path)
    inputs[str(path)]=value
    return path

def register_modules(inputs):
    for module in list(sys.modules.values()):
        name=getattr(module,'__file__',None)
        if name:
            path=Path(name).resolve()
            if path.suffix=='.py' and path.is_relative_to(BRANCH) and not path.is_relative_to(ROOT):
                register(inputs,path)

def setup(model,inputs):
    ladder=response.infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    background=response.thermal_wave.thermal.ThermalBackground(model)
    emission=response.NonlocalEmission(ladder.basis,background,'nonlocal-leading',BRANCH/'infrared-source-domain-20261008/banks/s960-i256')
    for path in [*ladder.inputs,*emission.inputs,background.parent.source,background.native_constants]:
        register(inputs,path)
    register_modules(inputs)
    return ladder,background,emission

def frozen():
    config=read(ROOT/'configuration.json')
    for name,value in config['protocol_hashes'].items():
        assert digest(ROOT/name)==value,name
    return config
