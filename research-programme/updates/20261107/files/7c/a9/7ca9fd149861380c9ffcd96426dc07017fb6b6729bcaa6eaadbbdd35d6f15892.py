import os
os.environ['OPENBLAS_NUM_THREADS']='1'
os.environ['OMP_NUM_THREADS']='1'
os.environ['MKL_NUM_THREADS']='1'
import sys
sys.dont_write_bytecode=True
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parent
BRANCH,POST=ROOT.parent,ROOT.parent.parent
PARENT=BRANCH/'repaired-inner-radiation-gas-feedback-20261013'
sys.path.insert(0,str(PARENT))
import repair_common as inherited
from repair_common import np,math,json,linalg,special,interpolate,digest,write_json,modest,thermal_wave,infrared_ladder,read_prediction,read_npz,matching_weight,I3,check,norm
from repair_common import load_histories,profile_at,make_drivers,split_matrix,sparse,sparse_linalg,FreeFree,log_rule,NonlocalEmission,ShapeReadout,photon_norm,high_stencils,compact_defect,local_packet
PARENT_SEAL='b842963438325ec7e9d5b5e4856ca2f0a65393c40587c96ea80eef10806bfa45'
STARTED=datetime(2026,10,13,1,21,25,tzinfo=timezone.utc)


def ancestors():
    chain=inherited.ancestors()
    path=PARENT/'results/stage-integrity.json'
    assert digest(path)==PARENT_SEAL
    return {path:json.loads(path.read_text()),**chain}


def verify_source(path,chain):
    inherited.verify_source(path,chain)


def finish(folder,report,script,extra=()):
    paths={ROOT/'finer_common.py',ROOT/'ACCEPTANCE.md',ROOT/'DERIVATION.md',Path(script).resolve(),PARENT/'results/stage-integrity.json'}
    paths.update(Path(path).resolve() for path in extra)
    for module in list(sys.modules.values()):
        filename=getattr(module,'__file__',None)
        if filename:
            path=Path(filename).resolve()
            if path.suffix=='.py' and path.is_relative_to(BRANCH):
                paths.add(path)
    report.update(state='complete',finished_utc=datetime.now(timezone.utc).isoformat(),
        script_sha256=digest(script),input_hashes={str(path):digest(path) for path in sorted(paths)})
    report['count']=len(report['checks'])
    report['all_checks_passed']=all(bool(row['passed']) for row in report['checks'])
    write_json(folder/'status.json',report)
    (folder/'COMPLETE').write_text('complete\n',encoding='utf-8')


def positive_stencils(events,spacing,margin):
    offsets=np.arange(-margin,margin+1)
    bank=[]
    chemical,constant,minimum=0.,0.,1.
    for event in events:
        shifts=np.log(event['ratios'])
        lower=np.floor(shifts/spacing).astype(int)
        weight=-np.expm1(-(shifts-lower*spacing))/(-np.expm1(-spacing))
        minimum=min(minimum,float(min(weight.min(),(1-weight).min())))
        values=np.zeros(len(offsets))
        np.add.at(values,lower+margin,event['rates']*(1-weight))
        np.add.at(values,lower+1+margin,event['rates']*weight)
        values[margin]-=event['rates'].sum()
        eigenvalue=float(event['rates']@(-np.expm1(-shifts)))
        chemical=max(chemical,abs(float(values@np.exp(-offsets*spacing)+eigenvalue))/abs(eigenvalue))
        constant=max(constant,float(abs(values.sum())))
        bank.append(values)
    return offsets,np.array(bank),chemical,constant,minimum
