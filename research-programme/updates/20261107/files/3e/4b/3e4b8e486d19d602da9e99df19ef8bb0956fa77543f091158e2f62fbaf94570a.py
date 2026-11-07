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
PARENT=BRANCH/'incoming-band820-order7-20261018'
sys.path.insert(0,str(PARENT))
from stage161_common import *
import stage161_common as parent161
from decimal import Decimal,localcontext
ROOT=Path(__file__).resolve().parent
PARENT=BRANCH/'incoming-band820-order7-20261018'
PARENT_SEAL='4f10abd94425f32b11d3f04e89b57de13e2b76cce9d8136db8ce579a9cf0ff4b'
STARTED=datetime(2026,10,18,22,14,52,tzinfo=timezone.utc)
INHERITED_PAYLOADS=297712
ENDPOINTS={'start':.75,'end':1.}
DEADLINE='2026-10-19T02:00:00+00:00'
OLD_BANKS={
    'start':BRANCH/'adjacent-physical-source-window-20261015/runs/expensive-end',
    'end':BRANCH/'colder-terminal-physical-source-window-20261016/runs/expensive-end'}
OLD_SOURCES={
    'start':BRANCH/'saved-event-precision-repair-20261016/results/reaggregation/end/source.npz',
    'end':BRANCH/'colder-terminal-physical-source-window-20261016/results/terminal-sources/source.npz'}


def ancestors():
    chain=parent161.ancestors()
    path=PARENT/'results/stage-integrity.json'
    assert digest(path)==PARENT_SEAL
    return {path:json.loads(path.read_text()),**chain}


def finish(folder,report,script,extra=()):
    paths={ROOT/'stage162_common.py',ROOT/'ACCEPTANCE.md',ROOT/'DERIVATION.md',
        Path(script).resolve(),PARENT/'results/stage-integrity.json'}
    paths.update(Path(path).resolve() for path in extra)
    for module in list(sys.modules.values()):
        filename=getattr(module,'__file__',None)
        if filename:
            path=Path(filename).resolve()
            if path.suffix=='.py' and path.is_relative_to(BRANCH):
                paths.add(path)
    report.update(state='complete',finished_utc=datetime.now(timezone.utc).isoformat(),
        input_hashes={str(path):digest(path) for path in sorted(paths)})
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


def endpoint_basis(phase,route,endpoint):
    warm=bubble(phase,route)
    if endpoint=='start':
        return (1-phase)*(1-2*phase)-.375*warm
    return phase*(2*phase-1)+.125*warm


def endpoint_response_basis(phase,route,endpoint):
    return endpoint_basis(phase,route,endpoint)-cold_bubble(phase,route)*endpoint_basis(.75,route,endpoint)


def endpoint_component(data,endpoint,component):
    return data[component] if endpoint=='start' else data['end_'+component]


def endpoint_full(data,endpoint):
    return data['remainder'] if endpoint=='start' else data['end']


def node_path162(endpoint,order,index):
    if order==4:
        return OLD_BANKS[endpoint]/'nodes'/f'{index//500:03d}'/f'{index:05d}.npz'
    return ROOT/'runs'/endpoint/f'order{order}'/'nodes'/f'{index//500:03d}'/f'{index:05d}.npz'


def load_node162(endpoint,order,node,theta):
    path=node_path162(endpoint,order,node['index'])
    saved=read_npz(path)
    assert json.loads(str(saved['identity']))==node
    parameters,weight=parameters_and_weight(theta,node)
    assert float(saved['weight'])==weight and weight>0
    loop_path=Path(str(saved['loop_path']))
    loop=json.loads(loop_path.read_text())
    assert loop['identity']==event_owner.inherited.virtual_identity(parameters)
    assert loop['finite'] and loop['scalar']==float(saved['loop_scalar'])
    for component in COMPONENTS:
        assert saved[component].shape==(98,4) and np.isfinite(saved[component]).all()
    return saved,weight,path,loop_path


def old_prediction162(data,route):
    increment=data['after_band820_full']-data['after_order8_full']
    return parent161.current_prediction(data,route)+sum(
        source155.predictor_basis(.75,route,site)*increment[SITES.index(site)] for site in ['warm','centre'])
