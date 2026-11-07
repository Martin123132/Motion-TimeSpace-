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
PARENT=BRANCH/'targeted-frequency-band-refinement-20261018'
sys.path.insert(0,str(PARENT))
from stage158_common import *
import stage158_common as parent158
ROOT=Path(__file__).resolve().parent
PARENT=BRANCH/'targeted-frequency-band-refinement-20261018'
PARENT_SEAL='4fc30220389ac3bfbdf0c651563b5e52c29b020e3088510e238fbd217b60ed65'
SOURCE155=BRANCH/'predictor-anchor-order6-20261018'
STARTED=datetime(2026,10,18,18,13,59,tzinfo=timezone.utc)
INHERITED_PAYLOADS=294461
SITES=['cold','warm','centre']
FRACTIONS={'cold':.9375,'warm':.8125,'centre':.875}
BANDS={3:(1.,3.)}
COMPONENTS=['difference','virtual','state']
source155=stage156_parent.stage155_parent


def ancestors():
    chain=parent158.ancestors()
    path=PARENT/'results/stage-integrity.json'
    assert digest(path)==PARENT_SEAL
    return {path:json.loads(path.read_text()),**chain}


def authenticate(paths,chain):
    hashes={}
    for value in set(paths):
        path=Path(value).resolve()
        if path in chain:
            assert json.loads(path.read_text())==chain[path]
        else:
            inherited.inherited.verify_source(path,chain)
        hashes[str(path)]=digest(path)
    return hashes


def finish(folder,report,script,extra=()):
    paths={ROOT/'stage159_common.py',ROOT/'ACCEPTANCE.md',ROOT/'DERIVATION.md',
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


def band_nodes(theta,order,panel):
    lower,upper=BANDS[panel]
    return [node for node in integration_nodes(theta,order) if lower<node['frequency']<upper]


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


def event_path(row):
    return ROOT/'runs'/f"band{row['band']}"/row['site']/'nodes'/f"{row['index']//500:03d}"/f"{row['index']:05d}.npz"


def load_event(row):
    path=Path(row['reused_path']) if row['reused_path'] else event_path(row)
    saved=read_npz(path)
    original=row['original_node'] if row['reused_path'] else row['node']
    assert json.loads(str(saved['identity']))==original
    assert event_signature(original)==event_signature(row['node'])
    parameters,weight=parameters_and_weight(row['theta'],row['node'])
    old_parameters,old_weight=parameters_and_weight(row['theta'],original)
    assert float(saved['weight'])==old_weight
    loop_path=Path(str(saved['loop_path']))
    loop=json.loads(loop_path.read_text())
    assert loop['identity']==event_owner.inherited.virtual_identity(parameters)
    assert loop['finite'] and loop['scalar']==float(saved['loop_scalar'])
    if not row['reused_path']:
        assert loop_path.is_relative_to(ROOT/'virtual-cache')
    for component in COMPONENTS:
        assert saved[component].shape==(98,4) and np.isfinite(saved[component]).all()
    return saved,weight,path,loop_path


def base_source(data,phase,route):
    return parent158.base_source(data,phase,route)+sum(site_basis(phase,route,site)*data[f'band{band}_{site}_total'] for band in [3,4] for site in SITES)


def site_basis(phase,route,site):
    return cold_bubble(phase,route) if site=='cold' else source155.response_basis(phase,route,site)


def source_scale(data):
    return dual_norm(data['actual'][1:-1],data['mass'])


def original_full(data,site):
    return data['after34_full'][SITES.index(site)]

def current_prediction(data,route):
    return data[route+'_diagnostic_prediction6']+sum(
        source155.predictor_basis(.75,route,site)*(original_full(data,site)-parent158.original_full(data,site))
        for site in ['warm','centre'])


def increment_source(data,phase,route,site):
    return site_basis(phase,route,site)*data['order8_'+site+'_total']

