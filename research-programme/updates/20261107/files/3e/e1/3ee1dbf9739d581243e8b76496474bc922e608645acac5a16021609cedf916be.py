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
PARENT=BRANCH/'inner-time-cold40960-20261013'
INNER_PARENT=BRANCH/'inner-time-contraction-20261013'
COARSE_PARENT=BRANCH/'fixed-grid-time-refinement-20261013'
sys.path.insert(0,str(PARENT))
import cold40960_common as inherited
from cold40960_common import np,math,json,linalg,special,interpolate,digest,write_json,modest,thermal_wave,infrared_ladder,read_prediction,read_npz,matching_weight,I3,check,norm
from cold40960_common import load_histories,profile_at,make_drivers,split_matrix,sparse,sparse_linalg,FreeFree,log_rule,NonlocalEmission,ShapeReadout,photon_norm,high_stencils,compact_defect,local_packet,positive_stencils
PARENT_SEAL='a58ea07164e317e45c3822759105ed650646d51253c610f197b42692821d827b'
STARTED=datetime(2026,10,14,0,21,3,tzinfo=timezone.utc)


def ancestors():
    chain=inherited.ancestors()
    path=PARENT/'results/stage-integrity.json'
    assert digest(path)==PARENT_SEAL
    return {path:json.loads(path.read_text()),**chain}


def verify_source(path,chain):
    inherited.verify_source(path,chain)


def finish(folder,report,script,extra=()):
    paths={ROOT/'source_probe_common.py',ROOT/'ACCEPTANCE.md',ROOT/'DERIVATION.md',Path(script).resolve(),PARENT/'results/stage-integrity.json'}
    paths.update(Path(path).resolve() for path in extra)
    for module in list(sys.modules.values()):
        filename=getattr(module,'__file__',None)
        if filename:
            path=Path(filename).resolve()
            if path.suffix=='.py' and path.is_relative_to(BRANCH):
                paths.add(path)
    report.setdefault('sampled_intervals',list(range(0,56,8))+list(range(56,64)))
    report.setdefault('pending_backgrounds',[])
    report.update(state='complete',finished_utc=datetime.now(timezone.utc).isoformat(),
        script_sha256=digest(script),input_hashes={str(path):digest(path) for path in sorted(paths)})
    report['count']=len(report['checks'])
    report['all_checks_passed']=all(bool(row['passed']) for row in report['checks'])
    write_json(folder/'status.json',report)
    (folder/'COMPLETE').write_text('complete\n',encoding='utf-8')


def refined_owner(model):
    assert model in ['heavy','cold']
    return BRANCH/'inner-time-heavy40960-20261013' if model=='heavy' else PARENT


PROBE_INTERVALS=list(range(0,56,8))+list(range(56,64))
RESTART_STEPS=list(range(0,40960,5120))
