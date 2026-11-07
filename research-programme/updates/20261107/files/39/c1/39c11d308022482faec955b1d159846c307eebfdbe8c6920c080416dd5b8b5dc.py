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
PARENT=BRANCH/'colder-temperature-order6-20261017'
sys.path.insert(0,str(PARENT))
from stage152_order6_common import *
import stage152_order6_common as stage152_parent
from fractions import Fraction
ROOT=Path(__file__).resolve().parent
PARENT=BRANCH/'colder-temperature-order6-20261017'
STAGE151=BRANCH/'colder-temperature-integration-check-20261017'
STAGE150=BRANCH/'terminal-colder-half-frozen-predictions-20261017'
STAGE149=BRANCH/'terminal-window-independent-temperature-20261016'
PARENT_SEAL='d6ebd9d4528c6e58904180635427e288bb66b221c5cb1f6b5ff191f59e1c645e'
STARTED=datetime(2026,10,17,17,24,32,tzinfo=timezone.utc)
INHERITED_PAYLOADS=280273


def ancestors():
    chain=stage152_parent.ancestors()
    path=PARENT/'results/stage-integrity.json'
    assert digest(path)==PARENT_SEAL
    return {path:json.loads(path.read_text()),**chain}


def finish(folder,report,script,extra=()):
    paths={ROOT/'stage153_separation_common.py',ROOT/'ACCEPTANCE.md',ROOT/'DERIVATION.md',
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


def close(checks,label,actual,expected,tolerance=1e-10):
    actual,expected=np.asarray(actual),np.asarray(expected)
    scale=max(float(np.max(abs(expected))),1e-300)
    test(checks,label,float(np.max(abs(actual-expected)))/scale,tolerance)


def state_norm(values,mass):
    return np.sqrt(np.maximum(np.einsum('...ik,ij,...jk->...k',values,mass,values),0.))


def response_location(stage,model,route,count):
    case=route if stage==STAGE150 else route+('-order5' if stage==STAGE151 else '-order6')
    return stage/'results/response'/f'{model}-{case}-{count}'


def comparison_path(stage,model,route,count,match):
    case=route if stage==STAGE150 else route+('-order5' if stage==STAGE151 else '-order6')
    return stage/'results/comparison'/f'{model}-m{match}-{case}-{count}.npz'


def planned_inputs():
    paths=[PARENT/'results/integration-source/source.npz',PARENT/'results/integration-source/status.json',
        STAGE149/'results/holdout-source/source.npz']
    for model in ['heavy','cold']:
        for route in ['local','cubic']:
            for count in COUNTS:
                for stage in [STAGE150,STAGE151,PARENT]:
                    location=response_location(stage,model,route,count)
                    paths.extend([location/'status.json',location/'response.npz'])
                for match in [20,40]:
                    for stage in [STAGE150,PARENT]:
                        paths.append(comparison_path(stage,model,route,count,match))
    return sorted(set(paths))


def ball_diagnostics(defect,source_norm,radius):
    lower=np.maximum(defect-radius,0.)
    return dict(radius=radius.tolist(),residual_lower_fixed_reference=lower.tolist(),
        relative_lower_with_source_shift=(lower/(source_norm+radius)).tolist(),
        explicitly_conditional=True,certified_radius=False)
