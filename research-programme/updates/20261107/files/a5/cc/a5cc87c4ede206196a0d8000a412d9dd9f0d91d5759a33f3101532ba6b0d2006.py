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
PARENT=BRANCH/'matched-low-frequency-feedback-20261012'
sys.path.insert(0,str(PARENT))
import matched_feedback_common as inherited
from matched_feedback_common import np,math,json,linalg,special,interpolate,digest,write_json,modest,thermal_wave,infrared_ladder,NonlocalEmission,CompactCorrection,read_prediction,log_rule,matching_weight,photon_norm,I3
from turnover_common import tail
PARENT_SEAL='bfb6f1e4e41f32632f169cb67e305f67281d867f67214cca051f07719f7a8412'
STARTED=datetime(2026,10,12,21,32,48,tzinfo=timezone.utc)


def ancestors():
    chain=inherited.ancestors()
    path=PARENT/'results/stage-integrity.json'
    assert digest(path)==PARENT_SEAL
    return {path:json.loads(path.read_text()),**chain}


def verify_source(path,chain):
    inherited.verify_source(path,chain)


def finish(folder,report,script,extra=()):
    paths={ROOT/'direct_common.py',ROOT/'ACCEPTANCE.md',ROOT/'DERIVATION.md',Path(script).resolve(),PARENT/'results/stage-integrity.json'}
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


def check(name,value,limit):
    return dict(name=name,value=float(value),limit=limit,passed=bool(np.isfinite(value) and value<=limit))


def read_npz(path):
    with np.load(path) as archive:
        return {key:archive[key].copy() for key in archive.files}


def source_grid(upper,order):
    return log_rule([2e-5,4e-5,.0003,.001,.003,.01,upper],order)


def direct_adjoint(basis,frequency,weights,ratios,rates,chunk=32):
    initial=basis.evaluate(frequency)
    result=np.zeros_like(initial)
    for start in range(0,len(ratios),chunk):
        ratio=ratios[start:start+chunk]
        kernel=rates[start:start+chunk]/ratio
        shifted=basis.evaluate((ratio[:,None]*frequency).ravel()).reshape(len(ratio),len(frequency),basis.count)-initial
        inverse=basis.evaluate((frequency/ratio[:,None]).ravel()).reshape(len(ratio),len(frequency),basis.count)-initial
        result+=np.einsum('e,efk->fk',kernel,shifted+inverse/ratio[:,None,None])
    result[:,0]=0
    moment=float(np.sum(rates*(ratios-1)**2*(ratios+1)/ratios**3))
    result[:,1]=frequency*moment/basis.norms[1]
    return result.T*weights/(2*I3),moment


def dual_norm(value,basis):
    inverse=linalg.inv(basis.mass)
    return np.sqrt(np.maximum(np.einsum('...ik,ij,...jk->...k',value,inverse,value),0))

