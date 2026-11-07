import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT.parent/'endpoint-soft-subtraction-20261019'))
from stage164_common import *
import stage164_common as parent164
from probe_state_roundoff import PreciseBornCorrelated,precise_state,exact_born_left,outer
from stable_moments import StableMoments
import mpmath as mp
ROOT=Path(__file__).resolve().parent
PARENT=ROOT.parent/'endpoint-soft-subtraction-20261019'
PARENT_SEAL='e3d92bb7a4f5bd6703499ba145a297ee740c20b08f8165aa48b14ecdf2e7d391'
INHERITED_PAYLOADS=324284
STARTED=datetime(2026,10,19,13,18,55,tzinfo=timezone.utc)
DEADLINE='2026-10-19T16:50:00+00:00'


def ancestors():
    chain=parent164.ancestors()
    path=PARENT/'results/stage-integrity.json'
    assert digest(path)==PARENT_SEAL
    return {path:json.loads(path.read_text()),**chain}


def finish(folder,report,script,extra=()):
    paths={ROOT/'stage165_common.py',ROOT/'ACCEPTANCE.md',ROOT/'DERIVATION.md',Path(script).resolve(),PARENT/'results/stage-integrity.json'}
    paths.update(Path(path).resolve() for path in extra)
    for module in list(sys.modules.values()):
        filename=getattr(module,'__file__',None)
        if filename:
            path=Path(filename).resolve()
            if path.suffix=='.py' and path.is_relative_to(BRANCH):
                paths.add(path)
    report.update(state='complete',finished_utc=datetime.now(timezone.utc).isoformat(),input_hashes={str(path):digest(path) for path in sorted(paths)})
    report['count']=len(report['checks'])
    report['all_checks_passed']=all(bool(row['passed']) for row in report['checks'])
    write_json(folder/'status.json',report)
    (folder/'COMPLETE').write_text('complete\n',encoding='utf-8')


def moment_path(endpoint,order,index):
    return ROOT/'runs'/endpoint/f'order{order}'/'nodes'/f'{index//500:03d}'/f'{index:05d}.npz'


def repaired_event(endpoint,order,node,theta,real_model,state_model):
    parameters,weight=parameters_and_weight(theta,node)
    original_path=parent164.moment_path(endpoint,order,node['index'])
    original=read_npz(original_path)
    old,unused,raw_path,loop_path=parent162.load_node162(endpoint,order,node,theta)
    with mp.workdps(60):
        vacuum=float(weak.vacuum.finite_virtual_ratio(parameters['energy'],parameters['cosine'])+weak.vacuum.soft_constant(parameters['energy'],parameters['cosine']))
    coefficient=.5*(vacuum+float(old['loop_scalar']))
    with mp.workdps(80):
        unused,right=state_model.born_jumps(parameters)
        virtual_mp=mp.mpf(coefficient)*outer(exact_born_left(parameters),right)
        virtual=np.array(virtual_mp.tolist(),dtype=float)
        virtual_pair=max(float(abs(virtual_mp[0,column]+virtual_mp[2,column])/max(abs(virtual_mp[0,column]),mp.mpf('1e-300'))) for column in range(4))
    state,state_identity=precise_state(parameters,state_model,80)
    real=real_model.real(parameters,angular=4,radial=18,rule=PanelRule(.5))
    values=dict(difference=real['total'],virtual=virtual,state=state['total'])
    equivalence={key:float(np.max(abs(value-original[key]))/max(np.max(abs(original[key])),1e-300)) for key,value in values.items()}
    return dict(**values,weight=weight,identity=json.dumps(node,sort_keys=True),parent_path=str(original_path),parent_sha256=digest(original_path),
        raw_path=str(raw_path),raw_sha256=digest(raw_path),loop_path=str(loop_path),loop_sha256=digest(loop_path),loop_scalar=float(old['loop_scalar']),
        vacuum_coefficient=vacuum,virtual_coefficient=coefficient,virtual_pair_exact=virtual_pair,state_pair_exact=max(state_identity.values()),
        equivalence=json.dumps(equivalence,sort_keys=True),event_energy_null=real['event_energy_null'],shift_energy_null=real['shift_energy_null'])
