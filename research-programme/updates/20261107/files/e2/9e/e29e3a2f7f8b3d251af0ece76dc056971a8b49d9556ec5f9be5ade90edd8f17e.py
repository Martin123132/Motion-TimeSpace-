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
PARENT=BRANCH/'predictor-anchor-order6-20261018'
sys.path.insert(0,str(PARENT))
from stage155_anchor_common import *
import stage155_anchor_common as stage155_parent
from repair_readout_cancellation import precise_readout
ROOT=Path(__file__).resolve().parent
PARENT=BRANCH/'predictor-anchor-order6-20261018'
SOURCE154=BRANCH/'predictor-anchor-integration-20261017'
PARENT_SEAL='3ff32935840f13f8ce1e3ab54f2a13f5779b770fb3046a5af150fc54dc1ed00c'
STARTED=datetime(2026,10,18,12,0,2,tzinfo=timezone.utc)
INHERITED_PAYLOADS=291614
SHAPE_CUTOFFS=[1e-8,1e-10,1e-12]
THRESHOLD=.01


def ancestors():
    chain=stage155_parent.ancestors()
    path=PARENT/'results/stage-integrity.json'
    assert digest(path)==PARENT_SEAL
    return {path:json.loads(path.read_text()),**chain}


def finish(folder,report,script,extra=()):
    paths={ROOT/'stage156_common.py',ROOT/'ACCEPTANCE.md',ROOT/'DERIVATION.md',
        Path(script).resolve(),PARENT/'results/stage-integrity.json'}
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


def location(stage,model,route,count):
    case=route+('-order5' if stage==STAGE151 else '-order6' if stage==SOURCE152 else '')
    return stage/'results/response'/f'{model}-{case}-{count}'


def planned_inputs():
    paths=[PARENT/'results/anchor-sources/source.npz',PARENT/'results/anchor-sources/status.json',
        PARENT/'NUMERICAL-SUMMARY.json',SOURCE154/'results/anchor-sources/status.json']
    for model in ['heavy','cold']:
        for route in ['local','cubic']:
            for count in COUNTS:
                for stage in [STAGE150,STAGE151,SOURCE152,SOURCE154,PARENT]:
                    folder=location(stage,model,route,count)
                    paths.extend([folder/'response.npz',folder/'status.json'])
                for match in [20,40]:
                    for stage in [STAGE150,PARENT]:
                        paths.append(stage/'results/comparison'/f'{model}-m{match}-{route}-{count}.npz')
    return sorted(set(paths))


def conditional_bound(error_norm,cold_norm,cold_radius,error_radius):
    lower=np.maximum(error_norm-error_radius,0)/(cold_norm+cold_radius)
    available=error_norm-error_radius-THRESHOLD*(cold_norm+cold_radius)
    return dict(relative_lower=lower.tolist(),
        unresolved_error_radius_allowance_to_keep_above1percent=available.tolist(),
        conditional=True,certified=False,unmeasured_endpoint_and_other_axis_radii=None)


def projected_shape(defect,directions,whiten,cutoff,checks,label):
    target=whiten(defect)
    vectors=np.asarray([whiten(value) for value in directions])
    records=[]
    for column in range(4):
        matrix=vectors[:,:,column].T
        lengths=np.linalg.norm(matrix,axis=0)
        normalized=matrix[:,lengths>0]/lengths[lengths>0]
        left,singular,right=np.linalg.svd(normalized,full_matrices=False)
        rank=int(np.sum(singular>cutoff*singular[0]))
        coordinates=left[:,:rank].T@target[:,column]
        projection=left[:,:rank]@coordinates
        residual=target[:,column]-projection
        denominator=np.linalg.norm(target[:,column])
        test(checks,'Projection Pythagoras:'+label+':'+str(cutoff)+':'+str(column),
            abs(np.linalg.norm(projection)**2+np.linalg.norm(residual)**2-denominator**2)/denominator**2,1e-10)
        test(checks,'Projection orthogonality:'+label+':'+str(cutoff)+':'+str(column),
            float(np.linalg.norm(left[:,:rank].T@residual))/denominator,1e-10)
        records.append(dict(rank=rank,singular_values=singular.tolist(),
            residual_fraction_of_defect=float(np.linalg.norm(residual)/denominator),
            projection_fraction_of_defect=float(np.linalg.norm(projection)/denominator)))
    return records
