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
PARENT=BRANCH/'independent-source-temperature-holdout-20261016'
sys.path.insert(0,str(PARENT))
import holdout_common as previous
from holdout_common import *
ROOT=Path(__file__).resolve().parent
PARENT=BRANCH/'independent-source-temperature-holdout-20261016'
PARENT_SEAL='0df3bad382de30b0bb3e3b7a899d349d302d6ee2512dab7cff2cc8a1d3dc55cb'
STARTED=datetime(2026,10,16,1,55,25,tzinfo=timezone.utc)
FRACTIONS={'colder':.6875}
ANCHORS=BRANCH/'adjacent-physical-source-window-20261015'
PHASE=.75
INHERITED_PAYLOADS=239872


def ancestors():
    chain=previous.ancestors()
    path=PARENT/'results/stage-integrity.json'
    assert digest(path)==PARENT_SEAL
    return {path:json.loads(path.read_text()),**chain}


def finish(folder,report,script,extra=()):
    paths={ROOT/'colder_common.py',ROOT/'ACCEPTANCE.md',ROOT/'DERIVATION.md',
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


def owned_loop(parameters):
    identity=event_owner.inherited.virtual_identity(parameters)
    key=hashlib.sha256(json.dumps(identity,sort_keys=True).encode()).hexdigest()
    path=ROOT/'virtual-cache'/key[:2]/(key+'.json')
    if path.exists():
        saved=json.loads(path.read_text())
        assert saved['identity']==identity and saved['finite']
    else:
        tensor,response=weak.source.virtual_map(parameters,2)
        saved=dict(identity=identity,scalar=float(response[0,0]),finite=bool(np.isfinite(response[0,0])))
        assert saved['finite']
        path.parent.mkdir(parents=True,exist_ok=True)
        temporary=path.with_suffix('.tmp')
        write_json(temporary,saved)
        temporary.replace(path)
    return saved['scalar'],path


def expensive_components(parameters,model):
    result=model.real(parameters,angular=4,radial=18,rule=PanelRule(.5))
    scalar,path=owned_loop(parameters)
    weak.vacuum.mp.mp.dps=60
    vacuum=float(weak.vacuum.finite_virtual_ratio(parameters['energy'],parameters['cosine'])
                 +weak.vacuum.soft_constant(parameters['energy'],parameters['cosine']))
    jump,product=model.born_data(parameters)
    return dict(difference=result['total'],virtual=.5*(vacuum+scalar)*product,
                state=model.state_correction(parameters)['total']),result['event_energy_null'],scalar,path


def bubble(phase,kind):
    if kind=='local':
        return 16*phase*(.5-phase) if 0<=phase<=.5 else 0.
    assert kind=='cubic'
    return (64/3)*phase*(phase-.5)*(phase-1)


def quadratic(source,phase):
    return (1-phase)*source['start']+phase*source['end']+4*phase*(1-phase)*source['curvature']

def cold_bubble(phase,kind):
    if kind=='local':
        return 16*(phase-.5)*(1-phase) if .5<=phase<=1 else 0.
    assert kind=='cubic'
    return -(128/3)*phase*(phase-.25)*(phase-.5)*(phase-1)


def forecast(anchors,warm_defect,phase,kind):
    return quadratic(anchors,phase)+bubble(phase,kind)*warm_defect
