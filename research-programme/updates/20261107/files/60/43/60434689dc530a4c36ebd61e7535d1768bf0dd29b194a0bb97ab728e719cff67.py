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
PARENT=BRANCH/'temperature-source-interpolation-20261014'
SITES=BRANCH/'initial-source-response-sites-20261014'
sys.path.insert(0,str(PARENT))
import interpolation_common as inherited
from interpolation_common import np,math,json,linalg,interpolate,digest,write_json,modest,thermal_wave,infrared_ladder,read_npz,NonlocalEmission,compact_defect,local_packet,check,I3,norm,refined_owner,photon_norm,max_relative
from quadrature_common import positive_stencils,high_stencils,load_histories,make_drivers,sparse,sparse_linalg,FreeFree
PARENT_SEAL='6fcdb40ba9751bc558d53163920339c15c4fab2e21b77e6d9c86254f57d03799'
STARTED=datetime(2026,10,14,9,51,52,tzinfo=timezone.utc)


def ancestors():
    chain=inherited.ancestors()
    path=PARENT/'results/stage-integrity.json'
    assert digest(path)==PARENT_SEAL
    return {path:json.loads(path.read_text()),**chain}


def verify_source(path,chain):
    inherited.verify_source(path,chain)


def finish(folder,report,script,extra=()):
    paths={ROOT/'coefficient_common.py',ROOT/'ACCEPTANCE.md',ROOT/'DERIVATION.md',Path(script).resolve(),PARENT/'results/stage-integrity.json'}
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
