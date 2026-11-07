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
PARENT=BRANCH/'driven-low-frequency-turnover-20261012'
sys.path.insert(0,str(PARENT))
import turnover_common as inherited
from turnover_common import np,math,json,linalg,special,interpolate,digest,write_json,modest,thermal_wave,infrared_ladder,FreeFree,ShapeReadout
from window_transfer_common import EnergyCoordinates,NonlocalEmission,photon_norm
from nonlocal_dc import gould
PARENT_SEAL='40585b0e8b75e6ec5b8e8d9e7e93772c38309d399a598c7aa64981dee2670f79'
STARTED=datetime(2026,10,12,20,4,13,tzinfo=timezone.utc)
I3=math.pi**4/15
I4=4*I3


def ancestors():
    chain=inherited.ancestors()
    path=PARENT/'results/stage-integrity.json'
    assert digest(path)==PARENT_SEAL
    return {path:json.loads(path.read_text()),**chain}


def verify_source(path,chain):
    inherited.verify_source(path,chain)


def finish(folder,report,script,extra=()):
    paths={ROOT/'matched_feedback_common.py',ROOT/'ACCEPTANCE.md',ROOT/'DERIVATION.md',Path(script).resolve(),PARENT/'results/stage-integrity.json'}
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


def log_rule(edges,order):
    nodes,weights=special.roots_legendre(order)
    points,measures=[],[]
    for lower,upper in zip(edges[:-1],edges[1:]):
        if upper<=lower:
            continue
        half=math.log(upper/lower)/2
        local=np.exp(math.log(lower*upper)/2+half*nodes)
        points.append(local)
        measures.append(half*weights*local)
    return np.concatenate(points),np.concatenate(measures)


def matching_weight(frequency,upper):
    def smooth(coordinate):
        clipped=np.clip(coordinate,0,1)
        return clipped**3*(10-15*clipped+6*clipped**2)
    frequency=np.asarray(frequency)
    lower=smooth(np.log(frequency/2e-5)/math.log(2))
    higher=1-smooth(np.log(frequency/.01)/math.log(upper/.01))
    return lower*higher


def read_prediction(model,variant='fine'):
    folder={'fine':'invariant-half-time2-prediction','time':'invariant-half-prediction',
            'space':'invariant-prediction'}[variant]
    path=PARENT/folder/'runs'/f'{model}-main1280/prediction.npz'
    with np.load(path) as saved:
        prediction={key:saved[key].copy() for key in ['frequency','coordinate','slope','coefficient_knots','coefficient_bank','offsets']}
    baseline,window,inputs=inherited.load_histories(model)
    profiles=np.stack([inherited.profile_at(float(position),baseline,window)[:,:3] for position in prediction['coordinate']])
    gas=np.column_stack([np.interp(prediction['coordinate'],baseline['expansion'],baseline['temperature_scaled']),
        interpolate.interp1d(window['coordinate'],window['gas'][:,:2],axis=0)(prediction['coordinate'])])
    prediction['slope']=prediction['slope'][:,:,:3]
    return prediction,profiles,gas,[path,path.parent/'status.json',*inputs]


class CompactCorrection:
    def __init__(self,basis,frequency,upper):
        self.basis,self.frequency,self.upper=basis,frequency,upper
        self.entries={}

    def register(self,label,points):
        points=np.asarray(points)
        selected=(points>2e-5)&(points<self.upper)
        chosen=points[selected]
        self.entries[label]=(points,selected,chosen,self.basis.evaluate(chosen),matching_weight(chosen,self.upper))

    def at(self,label,spline,profile):
        points,selected,chosen,values,window=self.entries[label]
        result=np.zeros((len(points),profile.shape[1]))
        if len(chosen):
            result[selected]=window[:,None]*(chosen[:,None]*spline(np.log(chosen))-values@profile)
        return result
