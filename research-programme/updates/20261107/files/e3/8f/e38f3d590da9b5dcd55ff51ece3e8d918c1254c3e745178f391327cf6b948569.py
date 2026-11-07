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
PARENT=BRANCH/'collision-derived-overlap-20261013'
sys.path.insert(0,str(PARENT))
import overlap_common as inherited
from overlap_common import np,math,json,linalg,special,interpolate,digest,write_json,modest,thermal_wave,infrared_ladder,read_prediction,read_npz,matching_weight,I3,check,norm
from turnover_common import load_histories,profile_at,make_drivers,split_matrix,sparse,sparse_linalg,FreeFree
from matched_feedback_common import log_rule,NonlocalEmission,ShapeReadout,photon_norm
from solve_balanced_overlap import high_stencils
PARENT_SEAL='76a847b4666ded68c0a074be31b96e30342f0f04ae087951dc423e98f425bae9'
STARTED=datetime(2026,10,13,0,25,1,tzinfo=timezone.utc)


def ancestors():
    chain=inherited.ancestors()
    path=PARENT/'results/stage-integrity.json'
    assert digest(path)==PARENT_SEAL
    return {path:json.loads(path.read_text()),**chain}


def verify_source(path,chain):
    inherited.verify_source(path,chain)


def finish(folder,report,script,extra=()):
    paths={ROOT/'repair_common.py',ROOT/'ACCEPTANCE.md',ROOT/'DERIVATION.md',Path(script).resolve(),PARENT/'results/stage-integrity.json'}
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


def local_packet(folder):
    status=folder/'status.json'
    packet=json.loads(status.read_text())
    assert packet['state']=='complete' and (folder/'COMPLETE').exists()
    for path,sha in packet['input_hashes'].items():
        assert digest(path)==sha,path
    return packet


def compact_defect(points,grid,values,upper):
    points=np.asarray(points)
    result=np.zeros((len(points),values.shape[1]))
    chosen=(points>2e-5)&(points<upper)
    if np.any(chosen):
        selected=points[chosen]
        spline=interpolate.CubicSpline(np.log(grid),values,axis=0,extrapolate=False)
        result[chosen]=selected[:,None]*matching_weight(selected,upper)[:,None]*spline(np.log(selected))
    return result
