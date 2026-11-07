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
PARENT=BRANCH/'initial-source-response-sites-20261014'
INNER_PARENT=BRANCH/'inner-time-contraction-20261013'
COARSE_PARENT=BRANCH/'fixed-grid-time-refinement-20261013'
sys.path.insert(0,str(PARENT))
import response_sites_common as inherited
from response_sites_common import np,math,json,linalg,special,interpolate,digest,write_json,modest,thermal_wave,infrared_ladder,read_prediction,read_npz,matching_weight,I3,check,norm
from response_sites_common import load_histories,profile_at,make_drivers,split_matrix,sparse,sparse_linalg,FreeFree,log_rule,NonlocalEmission,ShapeReadout,photon_norm,high_stencils,compact_defect,local_packet,positive_stencils
PARENT_SEAL='d0928d10be2975e6ede4390e230717126ac9078c249965527b5d885a4e71a688'
STARTED=datetime(2026,10,14,3,54,26,tzinfo=timezone.utc)


def ancestors():
    chain=inherited.ancestors()
    path=PARENT/'results/stage-integrity.json'
    assert digest(path)==PARENT_SEAL
    return {path:json.loads(path.read_text()),**chain}


def verify_source(path,chain):
    inherited.verify_source(path,chain)


def finish(folder,report,script,extra=()):
    paths={ROOT/'quadrature_common.py',ROOT/'ACCEPTANCE.md',ROOT/'DERIVATION.md',Path(script).resolve(),PARENT/'results/stage-integrity.json'}
    paths.update(Path(path).resolve() for path in extra)
    for module in list(sys.modules.values()):
        filename=getattr(module,'__file__',None)
        if filename:
            path=Path(filename).resolve()
            if path.suffix=='.py' and path.is_relative_to(BRANCH):
                paths.add(path)
    report.setdefault('refined_intervals',[0])
    report.setdefault('pending_backgrounds',[])
    report.update(state='complete',finished_utc=datetime.now(timezone.utc).isoformat(),
        script_sha256=digest(script),input_hashes={str(path):digest(path) for path in sorted(paths)})
    report['count']=len(report['checks'])
    report['all_checks_passed']=all(bool(row['passed']) for row in report['checks'])
    write_json(folder/'status.json',report)
    (folder/'COMPLETE').write_text('complete\n',encoding='utf-8')


def refined_owner(model):
    assert model in ['heavy','cold']
    return BRANCH/'inner-time-heavy40960-20261013' if model=='heavy' else BRANCH/'inner-time-cold40960-20261013'


PROBE_INTERVALS=list(range(0,56,8))+list(range(56,64))
RESTART_STEPS=[0]
SAMPLE_STEPS=np.arange(0,641,20)
SOURCE_STEPS=SAMPLE_STEPS.copy()

ODD_STEPS=np.arange(20,640,40)
VARIANTS=['stable','event1','event2','frequency1','frequency2','joint']


def specification(upper,variant):
    order=8 if upper==.04 else 6
    return {'stable':(order,32),'event1':(order+2,32),'event2':(order+4,32),
        'frequency1':(order,64),'frequency2':(order,128),'joint':(order+2,64)}[variant]
