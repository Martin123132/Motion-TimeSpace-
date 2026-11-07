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
PARENT=BRANCH/'colder-cubic-discrepancy-separation-20261017'
sys.path.insert(0,str(PARENT))
from stage153_separation_common import *
import stage153_separation_common as stage153_parent
ROOT=Path(__file__).resolve().parent
PARENT=BRANCH/'colder-cubic-discrepancy-separation-20261017'
SOURCE152=BRANCH/'colder-temperature-order6-20261017'
STAGE148=BRANCH/'colder-terminal-physical-source-window-20261016'
PARENT_SEAL='9fb00ec3e694d44838d0e15823d9b6920ab552f7df8520ef02bf646b01f13e1d'
STARTED=datetime(2026,10,17,22,15,7,tzinfo=timezone.utc)
INHERITED_PAYLOADS=280334
ANCHORS={'warm':.8125,'centre':.875}
COMPONENTS=['difference','virtual','state']
COUNTS=[2048,4096]


def ancestors():
    chain=stage153_parent.ancestors()
    path=PARENT/'results/stage-integrity.json'
    assert digest(path)==PARENT_SEAL
    return {path:json.loads(path.read_text()),**chain}


def finish(folder,report,script,extra=()):
    paths={ROOT/'stage154_anchor_common.py',ROOT/'ACCEPTANCE.md',ROOT/'DERIVATION.md',
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


def event_path(anchor,index):
    return ROOT/'runs'/anchor/'nodes'/f'{index//500:03d}'/f'{index:05d}.npz'


def central_source(data,phase,route):
    return stage152_parent.candidate_source(data,phase,route+'-order6')


def predictor_basis(phase,route,anchor):
    warm=bubble(phase,route)
    return warm if anchor=='warm' else 4*phase*(1-phase)-.75*warm


def response_basis(phase,route,anchor):
    return predictor_basis(phase,route,anchor)-cold_bubble(phase,route)*predictor_basis(.75,route,anchor)


def delta_components(data,phase,route):
    return [response_basis(phase,route,anchor)*data[f'{anchor}_delta_{component}']
        for anchor in ANCHORS for component in COMPONENTS]
