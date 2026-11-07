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
PARENT=BRANCH/'terminal-colder-half-frozen-predictions-20261017'
sys.path.insert(0,str(PARENT))
from stage150_colder_common import *
import stage150_colder_common as stage150_parent
from resolved_redistribution import incoming_rule
ROOT=Path(__file__).resolve().parent
PARENT=BRANCH/'terminal-colder-half-frozen-predictions-20261017'
PARENT_SEAL='82d8b69b062e4fe9bc1f332019b9832c16b183f91f3f547c0c29f39d5ff33c52'
STARTED=datetime(2026,10,17,1,12,57,tzinfo=timezone.utc)
INHERITED_PAYLOADS=273496
FRACTIONS={'holdout':.9375}
PHASE=.75
COUNTS=[2048,4096]


def ancestors():
    chain=stage150_parent.ancestors()
    path=PARENT/'results/stage-integrity.json'
    assert digest(path)==PARENT_SEAL
    return {path:json.loads(path.read_text()),**chain}


def finish(folder,report,script,extra=()):
    paths={ROOT/'stage151_integration_common.py',ROOT/'ACCEPTANCE.md',ROOT/'DERIVATION.md',
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

COMPONENTS=['difference','virtual','state']
CASES={f'{route}-order{order}':(route,order) for route in ['local','cubic'] for order in [3,5]}


def integration_nodes(theta,order):
    representatives={}
    for node in stage150_parent.physical_nodes(theta,'expensive'):
        representatives[node['electron_index']]=node
    cosines,hard_weights=np.polynomial.legendre.leggauss(3)
    ordinal=0
    for electron_index,reference in representatives.items():
        for frequency,seed_weight in incoming_rule(order,1e-5,24.):
            for cosine,hard_weight in zip(cosines,hard_weights):
                node=dict(reference,index=ordinal,frequency=float(frequency),
                          seed_weight=float(seed_weight),cosine=float(cosine),hard_weight=float(hard_weight))
                yield node
                ordinal+=1


def event_signature(node):
    return (node['frequency'],node['cosine'],*node['velocity'])


def event_path(order,index):
    return ROOT/'runs'/f'order{order}'/'nodes'/f'{index//500:03d}'/f'{index:05d}.npz'


def central_source(data,phase,route):
    return stage150_parent.original_source(data,phase,route)+cold_bubble(phase,route)*data['defect_'+route]


def candidate_source(data,phase,case):
    route,order=CASES[case]
    return central_source(data,phase,route)+cold_bubble(phase,route)*data[f'delta{order}_total']
