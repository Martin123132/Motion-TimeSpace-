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
PARENT=BRANCH/'physical-join-flux-decomposition-20261012'
sys.path.insert(0,str(PARENT))
import join_common as inherited
from join_common import np,math,json,linalg,special,interpolate,digest,write_json,modest,thermal_wave,infrared_ladder,read_prediction,read_npz,matching_weight,I3,check
from turnover_common import load_histories,profile_at,make_drivers,split_matrix,sparse,sparse_linalg
PARENT_SEAL='59f59e1456c175bda2c9a2be5accb81b41f5a3403ac78e5077444eb56d837fff'
STARTED=datetime(2026,10,12,23,52,5,tzinfo=timezone.utc)


def ancestors():
    chain=inherited.ancestors()
    path=PARENT/'results/stage-integrity.json'
    assert digest(path)==PARENT_SEAL
    return {path:json.loads(path.read_text()),**chain}


def verify_source(path,chain):
    inherited.verify_source(path,chain)


def finish(folder,report,script,extra=()):
    paths={ROOT/'overlap_common.py',ROOT/'ACCEPTANCE.md',ROOT/'DERIVATION.md',Path(script).resolve(),PARENT/'results/stage-integrity.json'}
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


def norm(value,measure):
    return np.sqrt(np.maximum(np.einsum('i,...ik,...ik->...k',measure,value,value),0))


def projected(value,basis):
    moment=np.einsum('fi,f,...fk->...ik',basis.values,basis.measure,value)
    coefficient=linalg.solve(basis.mass,moment.reshape(-1,basis.count,3).transpose(1,0,2).reshape(basis.count,-1),assume_a='pos')
    coefficient=coefficient.reshape(basis.count,-1,3).transpose(1,0,2).reshape(moment.shape)
    return value-np.einsum('fi,...ik->...fk',basis.values,coefficient)
