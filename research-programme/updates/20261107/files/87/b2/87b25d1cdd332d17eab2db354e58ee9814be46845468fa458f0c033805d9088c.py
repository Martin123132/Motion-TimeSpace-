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
PARENT=BRANCH/'inner-compton-coefficient-refinement-20261014'
sys.path.insert(0,str(PARENT))
import coefficient_common as inherited
from coefficient_common import np,math,json,linalg,interpolate,digest,write_json,modest,thermal_wave,infrared_ladder,read_npz,NonlocalEmission,compact_defect,local_packet,check,I3,norm,refined_owner,photon_norm,max_relative,sparse,sparse_linalg,FreeFree
from interpolation_common import load_inputs as load_operator_inputs
from paired_adjoint import stable_adjoint
PARENT_SEAL='14d30847a76311bd9f9e6ca0102aa82f0749d4433590e81e2cca3cb4eb9e4846'
STARTED=datetime(2026,10,14,10,35,14,tzinfo=timezone.utc)


def ancestors():
    chain=inherited.ancestors()
    path=PARENT/'results/stage-integrity.json'
    assert digest(path)==PARENT_SEAL
    return {path:json.loads(path.read_text()),**chain}


def verify_source(path,chain):
    inherited.verify_source(Path(path),chain)


def finish(folder,report,script,extra=()):
    paths={ROOT/'source_pair_common.py',ROOT/'ACCEPTANCE.md',ROOT/'DERIVATION.md',Path(script).resolve(),PARENT/'results/stage-integrity.json'}
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


def symbol(shift,rates,powers,eigenvalue=0.):
    return np.sum(rates[:,None]*np.expm1(shift[:,None]*powers[None,:]),axis=0)+eigenvalue


def source_symbol(shift,rates,powers):
    inverse=np.exp(-shift)
    return np.sum((rates*inverse/2)[:,None]*(np.expm1(shift[:,None]*powers[None,:])
        +inverse[:,None]*np.expm1(-shift[:,None]*powers[None,:])),axis=0)


def event_paths():
    old=BRANCH/'direct-doppler-compton-feedback-20261012/results/bank-o6-q32-m40'
    fresh=BRANCH/'initial-source-response-sites-20261014/results/operator-m20'
    return [old/'epoch-00.npz',*[fresh/f'event-{step:05d}.npz' for step in range(20,640,20)],old/'epoch-01.npz']


def physical_pairing(raw,offsets,spacing,eigenvalue):
    center=int(np.flatnonzero(offsets==0)[0])
    ratios=np.exp(offsets[center+1:]*spacing)
    forward=(raw[center+1:]+ratios**3*raw[:center][::-1])/2
    backward=forward/ratios**3
    unscaled=float(np.sum(forward*(ratios-1)**2*(ratios+1)/ratios**3))
    normalization=eigenvalue/unscaled
    result=np.zeros_like(raw)
    result[center+1:]=normalization*forward
    result[:center]=(normalization*backward)[::-1]
    result[center]=-np.sum(result)
    return result,normalization,unscaled
