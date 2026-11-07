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
PARENT=BRANCH/'spatial-shape-defect-correction-20261014'
sys.path.insert(0,str(PARENT))
import spatial_defect_common as inherited
from spatial_defect_common import np,math,json,linalg,interpolate,digest,write_json,modest,thermal_wave,infrared_ladder,read_npz,NonlocalEmission,compact_defect,local_packet,check,I3,norm,refined_owner,photon_norm,event_paths
from coefficient_common import sparse,sparse_linalg,FreeFree
from quadrature_common import load_histories,make_drivers
from paired_adjoint import stable_adjoint
PARENT_SEAL='44cb2ddb15515dd72526c22dc8a5329a1935b65716437c861a396a57c170a5e8'
P130=BRANCH/'source-adjoint-pairing-20261014'
P129=BRANCH/'inner-compton-coefficient-refinement-20261014'
SITES=BRANCH/'initial-source-response-sites-20261014'
STARTED=datetime(2026,10,14,11,38,11,tzinfo=timezone.utc)


def ancestors():
    chain=inherited.ancestors()
    path=PARENT/'results/stage-integrity.json'
    assert digest(path)==PARENT_SEAL
    return {path:json.loads(path.read_text()),**chain}


def verify_source(path,chain):
    inherited.verify_source(Path(path),chain)


def finish(folder,report,script,extra=()):
    paths={ROOT/'cubic_inner_common.py',ROOT/'ACCEPTANCE.md',ROOT/'DERIVATION.md',Path(script).resolve(),PARENT/'results/stage-integrity.json'}
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


def deposit_cubic(ratios,rates,offsets,spacing):
    shift=np.log(ratios)/spacing
    first=np.floor(shift).astype(int)-1
    locations=first[:,None]+np.arange(4)
    nodes=np.exp(-np.arange(4)*spacing)
    target=np.exp(-(shift-first)*spacing)
    weights=np.ones((len(ratios),4))
    for column in range(4):
        for other in range(4):
            if column!=other:
                weights[:,column]*=(target-nodes[other])/(nodes[column]-nodes[other])
    assert locations.min()>=offsets.min() and locations.max()<=offsets.max()
    raw=np.zeros(len(offsets))
    np.add.at(raw,(locations-offsets[0]).ravel(),(rates[:,None]*weights).ravel())
    errors=[]
    for power in range(4):
        expected=target**power
        errors.append(float(np.max(abs(weights@nodes**power-expected)/np.maximum(abs(expected),1e-300))))
    return raw,weights,errors


def pair_cubic(raw,offsets,spacing):
    center=int(np.flatnonzero(offsets==0)[0])
    ratios=np.exp(offsets[center+1:]*spacing)
    forward=(raw[center+1:]+ratios**3*raw[:center][::-1])/2
    result=np.zeros_like(raw)
    result[center+1:]=forward
    result[:center]=(forward/ratios**3)[::-1]
    result[center]=-np.sum(result)
    return result


def symbol_bound(stencil,offsets,spacing,eigenvalue,cells=8192):
    active=offsets>0
    locations=offsets[active]
    transformed=stencil[active]*np.exp(-1.5*locations*spacing)
    diagonal=float(stencil[offsets==0][0]+eigenvalue)
    angles=np.linspace(0,np.pi,cells+1)
    samples=diagonal+2*np.cos(angles[:,None]*locations)@transformed
    curvature=float(2*np.sum(locations**2*abs(transformed)))
    interpolation_bound=curvature*(np.pi/cells)**2/8
    roundoff_allowance=4096*np.finfo(float).eps*(abs(diagonal)+2*np.sum(abs(transformed)))
    upper=float(np.max(samples)+interpolation_bound+roundoff_allowance)
    return dict(sampled_max=float(np.max(samples)),curvature_bound=curvature,
        interpolation_remainder=interpolation_bound,roundoff_allowance=float(roundoff_allowance),
        upper_bound=upper,cells=cells,formal_interval_certificate=False)
