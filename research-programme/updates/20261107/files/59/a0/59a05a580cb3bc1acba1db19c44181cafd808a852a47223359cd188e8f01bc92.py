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
PARENT=BRANCH/'direct-doppler-compton-feedback-20261012'
sys.path.insert(0,str(PARENT))
import direct_common as inherited
from direct_common import np,math,json,linalg,special,interpolate,digest,write_json,modest,thermal_wave,infrared_ladder,NonlocalEmission,read_prediction,log_rule,matching_weight,photon_norm,I3,check,read_npz,source_grid,dual_norm
PARENT_SEAL='76b490e06b2ad1861be375f0f82bb701a3490a41c87c7577d07e36a9512f1938'
STARTED=datetime(2026,10,12,22,52,29,tzinfo=timezone.utc)
UPPERS=[.04,.02]


def ancestors():
    chain=inherited.ancestors()
    path=PARENT/'results/stage-integrity.json'
    assert digest(path)==PARENT_SEAL
    return {path:json.loads(path.read_text()),**chain}


def verify_source(path,chain):
    inherited.verify_source(path,chain)


def finish(folder,report,script,extra=()):
    paths={ROOT/'join_common.py',ROOT/'ACCEPTANCE.md',ROOT/'DERIVATION.md',Path(script).resolve(),PARENT/'results/stage-integrity.json'}
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


def joint_grid(order):
    rules=[source_grid(upper,order) for upper in UPPERS]
    frequency=np.unique(np.concatenate([rule[0] for rule in rules]))
    measures=np.zeros((len(UPPERS),len(frequency)))
    for index,(upper,(points,weights)) in enumerate(zip(UPPERS,rules)):
        selection=np.searchsorted(frequency,points)
        assert np.array_equal(frequency[selection],points)
        measures[index,selection]=weights*matching_weight(points,upper)
    return frequency,measures


def direct_split(basis,frequency,measures,ratios,rates,spline,profile,initial_zero=False,chunk=24):
    initial=basis.evaluate(frequency)
    central=frequency[:,None]*spline(np.log(frequency))-initial@profile
    if initial_zero:
        central=np.zeros_like(central)
    bulk=np.zeros((len(UPPERS),basis.count,profile.shape[1]))
    joining=np.zeros_like(bulk)
    adjoint=np.zeros_like(initial)
    lower=float(frequency.min()*min(ratios.min(),1/ratios.max()))
    upper=float(frequency.max()*max(ratios.max(),1/ratios.min()))
    assert lower>=math.exp(spline.x[0]) and upper<=math.exp(spline.x[-1]),(lower,upper)
    for start in range(0,len(ratios),chunk):
        ratio=ratios[start:start+chunk]
        kernel=rates[start:start+chunk]/ratio
        for inverse in [False,True]:
            multiplier=1/ratio if inverse else ratio
            points=multiplier[:,None]*frequency
            values=basis.evaluate(points.ravel()).reshape(len(ratio),len(frequency),basis.count)
            shifted=points[:,:,None]*spline(np.log(points))-values@profile
            if initial_zero:
                shifted=np.zeros_like(shifted)
            difference=values-initial
            difference[:,:,0]=0
            difference[:,:,1]=frequency*(multiplier[:,None]-1)/basis.norms[1]
            coefficients=kernel/ratio if inverse else kernel
            adjoint+=np.einsum('e,efk->fk',coefficients,difference)
            bulk_integrand=np.einsum('e,efk,efc->fkc',coefficients,difference,shifted-central,optimize=True)
            join_integrand=np.einsum('e,efk,efc->fkc',coefficients,difference,shifted+central,optimize=True)
            bulk-=np.einsum('wf,fkc->wkc',measures,bulk_integrand)/(4*I3)
            joining+=np.einsum('wf,fkc->wkc',measures,join_integrand)/(4*I3)
    adjoint[:,0]=0
    moment=float(np.sum(rates*(ratios-1)**2*(ratios+1)/ratios**3))
    adjoint[:,1]=frequency*moment/basis.norms[1]
    total=np.einsum('wf,fk,fc->wkc',measures,adjoint,central,optimize=True)/(2*I3)
    return bulk,joining,total,dict(minimum_shifted_frequency=lower,maximum_shifted_frequency=upper)

