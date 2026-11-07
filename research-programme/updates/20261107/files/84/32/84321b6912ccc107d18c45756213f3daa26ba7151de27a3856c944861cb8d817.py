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
PARENT=BRANCH/'compton-source-quadrature-20261014'
SITES=BRANCH/'initial-source-response-sites-20261014'
sys.path.insert(0,str(PARENT))
import quadrature_common as inherited
from quadrature_common import np,math,json,linalg,interpolate,digest,write_json,modest,thermal_wave,infrared_ladder,read_npz,NonlocalEmission,compact_defect,local_packet,check,I3,norm,refined_owner,photon_norm
PARENT_SEAL='b84005f480377350b63f87cbacdb86a932afdb73accea805104a0ac8ada314b6'
STARTED=datetime(2026,10,14,9,39,15,tzinfo=timezone.utc)
PARTS=['total','operator','state','cross','moment','shape','moment_cross']


def ancestors():
    chain=inherited.ancestors()
    path=PARENT/'results/stage-integrity.json'
    assert digest(path)==PARENT_SEAL
    return {path:json.loads(path.read_text()),**chain}


def verify_source(path,chain):
    inherited.verify_source(path,chain)


def finish(folder,report,script,extra=()):
    paths={ROOT/'interpolation_common.py',ROOT/'ACCEPTANCE.md',ROOT/'DERIVATION.md',Path(script).resolve(),PARENT/'results/stage-integrity.json'}
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


def load_inputs(model,upper,basis):
    label=int(upper*1000)
    order=8 if upper==.04 else 6
    old_path=BRANCH/'direct-doppler-compton-feedback-20261012/results'/f'bank-o{order}-q32-m{label}/bank.npz'
    fresh_path=SITES/'results'/f'operator-m{label}/bank.npz'
    replay_path=SITES/'results'/f'replay-{model}-s00000/prediction.npz'
    source_folder=SITES/'results'/f'sites-{model}-m{label}'
    old,fresh,replay=map(read_npz,[old_path,fresh_path,replay_path])
    old_status=local_packet(old_path.parent)
    fresh_status=local_packet(fresh_path.parent)
    assert old_status['all_checks_passed'] and fresh_status['all_checks_passed']
    assert local_packet(replay_path.parent)['all_checks_passed']
    assert np.array_equal(fresh['frequency'],old['frequency'])
    assert np.array_equal(replay['saved_step_indices'],np.arange(0,641,20))
    coordinate=replay['coordinate']
    assert np.array_equal(coordinate[[0,-1]],old['coordinate'][:2])
    assert np.array_equal(fresh['coordinate'],coordinate[1:-1])
    operators=np.concatenate([old['adjoint'][:1],fresh['adjoint'],old['adjoint'][1:2]])
    moments=np.array([old_status['rows'][0]['energy_moment'],
        *[row['energy_moment'] for row in fresh_status['rows']],old_status['rows'][1]['energy_moment']])
    state=np.array([compact_defect(old['frequency'],replay['frequency'],values,upper) for values in replay['defect']])
    paths=[old_path,old_path.parent/'status.json',fresh_path,fresh_path.parent/'status.json',
        replay_path,replay_path.parent/'status.json',source_folder/'status.json']
    sources={}
    for name in ['direct-sites32-source','direct-sites32-response','direct-evaluated','assembled-evaluated']:
        path=source_folder/(name+'.npz')
        sources[name]=read_npz(path)
        paths.append(path)
    return dict(coordinate=coordinate,frequency=old['frequency'],weights=old['weights'],
        operators=operators,moments=moments,field=state,temperature=np.r_[old['temperature'][0],fresh['temperature'],old['temperature'][1]],
        sources=sources,inputs=paths)


def max_relative(difference,operands):
    scale=np.maximum(sum(abs(value) for value in operands).max(axis=0),1e-300)
    return float(np.max(abs(difference)/scale))
