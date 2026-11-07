import os
for variable in ['OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS']:
    os.environ[variable] = '1'
import sys
sys.dont_write_bytecode = True
from pathlib import Path
import json
import hashlib
import argparse
from datetime import datetime, timezone
ROOT = Path(__file__).resolve().parent
BRANCH = ROOT.parent
PARENT = BRANCH / 'curvature-history-isolation-20261020'
BANK = BRANCH / 'upper-outer-frequency-temperature-test-20261020'
PARENT_SHA = 'b257cd081330405a99686bebcb10535cc3f9f81af3f881feccc0a4b1b9da26f6'
STARTED = '2026-10-20T19:40:51+00:00'
sys.path.insert(0, str(BANK))
import stage176_frequency_common as saved
source, np, mp = saved.source, saved.np, saved.mp
import scipy.linalg as linear
TAGS = ['plus', 'minus', 'plus_half', 'minus_half']
OPPOSITE = dict(plus='minus', minus='plus', plus_half='minus_half', minus_half='plus_half')
TERMS = ['moving', 'fixed', 'mixed', 'history_curvature', 'history_dependent']


def checked(rows, name, value, tolerance=1e-10):
    value = float(value)
    rows.append(dict(name=name, value=value, tolerance=tolerance,
                     passed=bool(np.isfinite(value) and value < tolerance)))


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def authenticate():
    seal = PARENT / 'results/stage-integrity.json'
    assert saved.digest(seal) == PARENT_SHA
    parent = read(seal)
    paths = {str(PARENT/name): checksum for name, checksum in parent['file_hashes'].items()}
    paths.update(parent['consumed_and_immediate_rehashed'])
    paths[str(seal)] = PARENT_SHA
    for filename, checksum in paths.items():
        assert saved.digest(filename) == checksum, filename
    return paths


def old_path(tag, node):
    return BANK/'events'/tag/saved.angle_label(node['cosine'])/f"electron-{node['electron_index']:02d}.npz"


def new_path(tag, node):
    return ROOT/'events'/tag/saved.angle_label(node['cosine'])/f"electron-{node['electron_index']:02d}.npz"


def atomic_npz(path, **fields):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix('.tmp')
    with temporary.open('wb') as handle:
        np.savez_compressed(handle, **fields)
    temporary.replace(path)


def forbidden(*args, **kwargs):
    raise RuntimeError('Stage178 forbids real-emission or new virtual integration')


def guard():
    source.evaluate = source.models = saved.virtual = source.virtual = forbidden
    source.physics.weak.source.virtual_map = forbidden
    source.physics.FastSplit.real = forbidden


class HistoryGroup(source.PairedHistory):
    def __init__(self, parts):
        self.parts = parts
        self.basis = parts[0].basis
        self.gas = [value for part in parts for value in part.gas]
        self.inputs = list(dict.fromkeys(path for part in parts for path in part.inputs))

    def functions(self, frequency, chemical=False):
        values = [part.functions(frequency, chemical) for part in self.parts]
        return np.concatenate([values[0][..., :1], *[value[..., 1:] for value in values]], axis=-1)

    def derivatives(self, frequency, chemical=False):
        values = [part.derivatives(frequency, chemical) for part in self.parts]
        return np.concatenate([values[0][..., :1], *[value[..., 1:] for value in values]], axis=-1)


class LinearHistory:
    def __init__(self, parts, coefficients):
        self.parts, self.coefficients = parts, coefficients
        self.basis = parts[0].basis
        self.gas = sum(coefficient*np.array(part.gas) for part, coefficient in zip(parts, coefficients)).tolist()
        self.inputs = list(dict.fromkeys(path for part in parts for path in part.inputs))

    def functions(self, frequency, chemical=False):
        values = [part.functions(frequency, chemical) for part in self.parts]
        departures = sum(coefficient*value[..., 1:] for coefficient, value in zip(self.coefficients, values))
        return np.concatenate([values[0][..., :1], departures], axis=-1)

    def derivatives(self, frequency, chemical=False):
        values = [part.derivatives(frequency, chemical) for part in self.parts]
        departures = sum(coefficient*value[..., 1:] for coefficient, value in zip(self.coefficients, values))
        return np.concatenate([values[0][..., :1], departures], axis=-1)


def action(parameters, bundle, full, primitive, coefficient, weight):
    unused, product = full.born_data(parameters)
    high = coefficient*product
    low = np.zeros_like(high)
    with mp.workdps(80):
        unused, right = primitive.born_jumps(parameters)
        lower = np.array((mp.mpf(coefficient)*source.physics.outer(source.physics.exact_born_left(parameters), right)).tolist(), dtype=float)
        norm0, norm1 = [mp.mpf(float(value)) for value in bundle.basis.norms[:2]]
        mean = mp.mpf(float(bundle.basis.mean))
        for column in range(high.shape[-1]):
            energy, number, gas = [mp.mpf(float(value)) for value in lower[:, column]]
            for row, value in zip(source.LOW, [energy, number/norm0, (energy-mean*number)/norm1, gas]):
                high[row, column] = float(value)
                low[row, column] = float(value-mp.mpf(float(value)))
    return source.precise_combine([(high, low)], [-weight])


def prepare():
    assert not (ROOT/'configuration.json').exists()
    authenticated = authenticate()
    config = read(BANK/'configuration.json')
    assert config['source_prediction_tolerance'] == .01 and config['identity_tolerance'] == 1e-10
    selected = config['selected']
    assert len(selected) == 36
    own = dict(stage=178, started_utc=STARTED, parent_seal_sha256=PARENT_SHA,
               bank=str(BANK), incoming_frequency=config['incoming_frequency'],
               selected=selected, offsets=source.OFFSETS, expansion_span=config['expansion_span'],
               source_prediction_tolerance=.01, identity_tolerance=1e-10,
               post_test_diagnostic=True, real_emission_integrations=0, new_loop_integrations=0,
               prior_bookmark_normalized_sha256={str(path):hashlib.sha256(path.read_text(encoding='utf-8').encode('utf-8')).hexdigest()
                   for path in [BRANCH/'RESUME-CURRENT.md', BRANCH.parent/'CURRENT_LOCAL_RESUME.md']})
    saved.write_json(ROOT/'configuration.json', own)
    saved.write_json(ROOT/'authenticated-inputs.json', authenticated)
    saved.write_json(ROOT/'progress.json', dict(state='prepared', crossed_actions_expected=144))
    print(json.dumps(dict(prepared=True, authenticated=len(authenticated), crossed_actions_expected=144)), flush=True)


def evaluate(limit):
    config = read(ROOT/'configuration.json')
    guard()
    mp.mp.dps = 60
    contexts = {tag:source.context(source.START-offset/config['expansion_span']) for tag, offset in source.OFFSETS.items()}
    paths = {path for bundle, temperature in contexts.values() for path in bundle.inputs}
    checks = []
    for tag in TAGS:
        moving, theta = contexts[tag]
        anchor = contexts['anchor'][0]
        crossed = contexts[OPPOSITE[tag]][0]
        combined = HistoryGroup([moving, anchor, crossed])
        full = source.physics.FastSplit(combined, 'difference')
        primitive = source.physics.StableMoments(combined)
        for ordinal, selected in enumerate(config['selected']):
            path = new_path(tag, selected)
            if not path.exists():
                if limit <= 0:
                    saved.write_json(ROOT/'progress.json', dict(state='safe_restart', next_tag=tag, next_event=ordinal))
                    return
                original = old_path(tag, selected)
                with np.load(original) as packet:
                    assert float(packet['theta']) == theta
                    node = json.loads(str(packet['node']))
                    loop_path = Path(str(packet['loop_path']))
                    expected_weight = float(packet['weight'])
                parameters, weight = source.physics.parameters_and_weight(theta, node)
                assert weight == expected_weight
                loop = read(loop_path)
                assert loop['finite'] and loop['identity'] == source.physics.event_owner.inherited.virtual_identity(parameters)
                with mp.workdps(60):
                    vacuum = float(source.physics.weak.vacuum.finite_virtual_ratio(parameters['energy'], parameters['cosine'])
                                   +source.physics.weak.vacuum.soft_constant(parameters['energy'], parameters['cosine']))
                coefficient = .5*(vacuum+loop['scalar'])
                high, low = action(parameters, combined, full, primitive, coefficient, weight)
                grouped_high = np.stack(np.split(high, 3, axis=-1))
                grouped_low = np.stack(np.split(low, 3, axis=-1))
                atomic_npz(path, high=grouped_high, low=grouped_low, theta=theta,
                           offset=source.OFFSETS[tag], history_tags=np.array([tag, 'anchor', OPPOSITE[tag]]),
                           weight=weight, coefficient=coefficient, node=json.dumps(node, sort_keys=True),
                           original_path=str(original), original_sha256=saved.digest(original),
                           loop_path=str(loop_path), loop_sha256=saved.digest(loop_path),
                           finished_utc=datetime.now(timezone.utc).isoformat())
                limit -= 1
            with np.load(path) as packet:
                assert saved.digest(str(packet['original_path'])) == str(packet['original_sha256'])
                assert saved.digest(str(packet['loop_path'])) == str(packet['loop_sha256'])
                assert list(packet['history_tags']) == [tag, 'anchor', OPPOSITE[tag]]
                assert packet['high'].shape == packet['low'].shape == (3,98,4)
                assert np.isfinite(packet['high']).all() and np.isfinite(packet['low']).all()
                paths.update([path, Path(str(packet['original_path'])), Path(str(packet['loop_path']))])
            if (ordinal+1) % 6 == 0:
                saved.write_json(ROOT/'progress.json', dict(state='crossing', phase=tag, events_complete_in_phase=ordinal+1,
                                 crossed_actions_saved=len(list((ROOT/'events').rglob('electron-*.npz'))), pid=os.getpid()))
                print(json.dumps(dict(phase=tag, completed=ordinal+1, expected=36)), flush=True)
        for label, coefficients, expected_indices in [('sum',[1,1],[0,2]), ('difference',[1,-1],[0,2]), ('zero',[0,0],[0,2])]:
            combined_history = LinearHistory([moving,crossed], coefficients)
            linear_full = source.physics.FastSplit(combined_history,'difference')
            linear_primitive = source.physics.StableMoments(combined_history)
            with np.load(new_path(tag,config['selected'][0])) as packet:
                parameters, weight = source.physics.parameters_and_weight(theta,json.loads(str(packet['node'])))
                coefficient = float(packet['coefficient'])
                direct = action(parameters,combined_history,linear_full,linear_primitive,coefficient,weight)
                expected = source.precise_combine([(packet['high'][index],packet['low'][index]) for index in expected_indices],coefficients)
            residual = direct[0]+direct[1]-expected[0]-expected[1]
            scale = max(np.max(abs(direct[0])),np.max(abs(expected[0])),1e-300)
            checked(checks,tag+':Born linearity:'+label,np.max(abs(residual))/scale)
            del linear_full, linear_primitive
        del full, primitive
    saved.write_json(ROOT/'results/evaluation-status.json', dict(state='complete',checks=checks,
        all_checks_passed=all(row['passed'] for row in checks),
        input_hashes={str(path):saved.digest(path) for path in sorted(paths)},crossed_actions=144,
        reproduced_diagonal_actions=288, real_emission_integrations=0,new_loop_integrations=0))
    assert all(row['passed'] for row in checks)
    saved.write_json(ROOT/'progress.json',dict(state='crosses_complete',crossed_actions_saved=144))


def split_vectors(bank, crossed, digits):
    result = np.zeros((3,5,98,4))
    events = np.zeros((36,5,98,4))
    with mp.workdps(digits):
        for row, history in np.ndindex(98,4):
            contributions = [[] for unused in TERMS]
            for event in range(36):
                def old(tag, branch):
                    pair = bank[tag][event]
                    return mp.mpf(float(pair[0][branch,2,row,history]))+mp.mpf(float(pair[1][branch,2,row,history]))
                def cross(tag):
                    pair = crossed[tag][event]
                    return mp.mpf(float(pair[0][2,row,history]))+mp.mpf(float(pair[1][2,row,history]))
                at_width = []
                for plus, minus, inverse in [('plus','minus',10000),('plus_half','minus_half',40000)]:
                    diagonal_plus, diagonal_minus = old(plus,0), old(minus,0)
                    fixed_plus, fixed_minus = old(plus,1), old(minus,1)
                    cross_plus, cross_minus = cross(plus), cross(minus)
                    moving = inverse*(diagonal_plus-2*old('anchor',0)+diagonal_minus)
                    fixed = inverse*(fixed_plus-2*old('anchor',1)+fixed_minus)
                    mixed = inverse*(diagonal_plus-cross_plus-cross_minus+diagonal_minus)/2
                    history_curvature = inverse*(diagonal_plus+cross_plus+cross_minus+diagonal_minus-2*fixed_plus-2*fixed_minus)/2
                    at_width.append([moving,fixed,mixed,history_curvature,moving-fixed])
                for term in range(5):
                    values = [at_width[0][term],at_width[1][term],at_width[0][term]-at_width[1][term]]
                    contributions[term].append(values)
                    events[event,term,row,history] = float(values[2])
            for term in range(5):
                for order in range(3):
                    result[order,term,row,history] = float(mp.fsum(values[order] for values in contributions[term]))
    return result, events


def analyse():
    config = read(ROOT/'configuration.json')
    authenticated = authenticate()
    assert authenticated == read(ROOT/'authenticated-inputs.json')
    evaluation = read(ROOT/'results/evaluation-status.json')
    assert evaluation['all_checks_passed']
    for filename, checksum in evaluation['input_hashes'].items():
        assert saved.digest(filename) == checksum, filename
        if not Path(filename).is_relative_to(ROOT):
            assert authenticated[filename] == checksum
    checks = list(evaluation['checks'])
    basis_path = source.ROOT/'results/preparation/basis.npz'
    with np.load(basis_path) as packet:
        mass, norms, mean = packet['mass'].copy(),packet['norms'].copy(),float(packet['mean'])
    factor = linear.cholesky(mass,lower=True)
    def whiten(values):
        photons = np.moveaxis(values[...,1:97,:],-2,-1)
        return linear.solve_triangular(factor,photons.reshape(-1,96).T,lower=True).T.reshape(photons.shape)
    def dot(first,second):
        return np.sum(whiten(first)*whiten(second),axis=-1)
    def length(values):
        return np.sqrt(np.maximum(dot(values,values),0))
    def identity(name,residual,scale):
        checked(checks,name,np.max(length(residual)/np.maximum(length(scale),1e-300)))
    bank, crossed = {}, {}
    paths = {basis_path, PARENT/'results/diagnostic-vectors.npz', PARENT/'results/source-metrics.json'}
    for tag in source.OFFSETS:
        bank[tag], crossed[tag] = [], []
        for node in config['selected']:
            original = old_path(tag,node)
            bank[tag].append(saved.read_pair(original))
            paths.add(original)
            if tag == 'anchor':
                continue
            path = new_path(tag,node)
            pair = saved.read_pair(path)
            crossed[tag].append(pair)
            old = bank[tag][-1]
            residual = pair[0][:2]+pair[1][:2]-old[0][:,2]-old[1][:,2]
            identity(tag+':'+saved.event_key(node)+':diagonal reproduction',residual,old[0][:,2]+old[1][:,2])
            values = pair[0]+pair[1]
            scale = np.maximum(np.maximum(abs(values[:,0]),abs(values[:,97])),1e-300)
            checked(checks,tag+':'+saved.event_key(node)+':energy gas exchange',np.max(abs(values[:,0]+values[:,97])/scale))
            moment = mean*norms[0]*values[:,1]+norms[1]*values[:,2]
            checked(checks,tag+':'+saved.event_key(node)+':photon energy coordinate',np.max(abs(moment-values[:,0])/scale))
            paths.add(path)
    print('Accumulating crossed decomposition at80 and100digits.',flush=True)
    vectors, event_vectors = split_vectors(bank,crossed,80)
    higher, higher_events = split_vectors(bank,crossed,100)
    identity('80 versus100 digit full decomposition',higher-vectors,vectors)
    identity('80 versus100 digit event decomposition',higher_events-event_vectors,event_vectors)
    for order,label in enumerate(['coarse','fine','discrepancy']):
        identity(label+':mixed plus history equals history-dependent',vectors[order,2]+vectors[order,3]-vectors[order,4],vectors[order,4])
        identity(label+':fixed plus history-dependent equals moving',vectors[order,1]+vectors[order,4]-vectors[order,0],vectors[order,0])
    with np.load(PARENT/'results/diagnostic-vectors.npz') as packet:
        parent_error = packet['curvature_error'].copy()
        parent_exact = packet['exact_reconstruction'].copy()
    identity('Moving virtual discrepancy equals saved diagnostic',vectors[2,0]-parent_error[0,2],parent_error[0,2])
    identity('Fixed virtual discrepancy equals saved diagnostic',vectors[2,1]-parent_error[1,2],parent_error[1,2])
    identity('Moving virtual curvatures equal saved diagnostic',vectors[:2,0]-parent_exact[:2,0,2],parent_exact[:2,0,2])
    nonvirtual = parent_error[0,1]+parent_error[0,3]
    complete_parts = [vectors[2,1],vectors[2,2],vectors[2,3],nonvirtual]
    identity('Complete matched discrepancy closes with untouched nonvirtual remainder',sum(complete_parts)-parent_error[0,4],parent_error[0,4])
    records = []
    for reference_label,reference in [('moving_virtual',parent_error[0,2]),('moving_matched',parent_error[0,4])]:
        denominator = np.maximum(dot(reference,reference),1e-300)
        for term,values in zip(['fixed_operator','mixed_operator_history','transmitted_history_curvature','nonvirtual_matched'],complete_parts):
            for history in range(4):
                records.append(dict(reference=reference_label,term=term,history=history,
                    signed_share=float(dot(values,reference)[history]/denominator[history]),
                    norm_ratio=float(length(values)[history]/max(length(reference)[history],1e-300))))
    width_records = []
    for order,label in enumerate(['coarse','fine','discrepancy']):
        reference = vectors[order,0]
        for term in range(1,4):
            for history in range(4):
                width_records.append(dict(width=label,term=TERMS[term],history=history,
                    signed_share=float(dot(vectors[order,term],reference)[history]/max(dot(reference,reference)[history],1e-300)),
                    norm_ratio=float(length(vectors[order,term])[history]/max(length(reference)[history],1e-300)),
                    norm=float(length(vectors[order,term])[history])))
    baseline = [row for row in read(PARENT/'results/source-metrics.json') if row['component'] in ['control','remainder','total']]
    for row in baseline:
        assert row['passed'] == (row['original_relative'] < .01)
    cancellation = sum(length(part) for part in complete_parts)/np.maximum(length(parent_error[0,4]),1e-300)
    saved.write_json(ROOT/'results/projection-shares.json',records)
    saved.write_json(ROOT/'results/width-decomposition.json',width_records)
    saved.write_json(ROOT/'results/saved-baseline-controls.json',baseline)
    atomic_npz(ROOT/'results/decomposition-vectors.npz',vectors=vectors,event_vectors=event_vectors,
        terms=np.array(TERMS),orders=np.array(['coarse','fine','discrepancy']),
        nonvirtual_matched=nonvirtual,matched_discrepancy=parent_error[0,4],cancellation_factor=cancellation)
    for filename,checksum in authenticated.items():
        assert saved.digest(filename) == checksum,filename
    code_paths = {*ROOT.glob('*.py'),ROOT/'configuration.json',ROOT/'ACCEPTANCE.md',ROOT/'DERIVATION.md'}
    for module in list(sys.modules.values()):
        filename = getattr(module,'__file__',None)
        if filename and Path(filename).suffix == '.py' and Path(filename).resolve().is_relative_to(BRANCH):
            path = Path(filename).resolve()
            code_paths.add(path)
            if not path.is_relative_to(ROOT):
                assert authenticated[str(path)] == saved.digest(path),path
    for path in ROOT.glob('*.py'):
        compile(path.read_text(encoding='utf-8'),str(path),'exec')
    assert not list(ROOT.rglob('__pycache__'))
    protected = BRANCH.parent.parent/'formalization-workbench'
    modified = [str(path) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime > datetime.fromisoformat(STARTED).timestamp()]
    checked(checks,'Protected workbench recent mtime guard',len(modified),.5)
    hashes = dict(evaluation['input_hashes'])
    hashes.update({str(path):saved.digest(path) for path in sorted(paths|code_paths)})
    status = dict(state='complete',stage=178,finished_utc=datetime.now(timezone.utc).isoformat(),
        checks=checks,count=len(checks),all_checks_passed=all(row['passed'] for row in checks),
        input_hashes=hashes,authenticated_parent_inputs=authenticated,
        crossed_actions=144,reproduced_diagonal_actions=288,reused_stencil_packets=180,
        real_emission_integrations=0,new_loop_integrations=0,source_prediction_tolerance=.01,identity_tolerance=1e-10,
        tolerances_changed=False,source_curve_changed=False,post_test_diagnostic=True,
        baseline_controls_reused=True,crossed_real_baseline_evaluated=False,
        interpolation_error_proved=False,new_node_matched_moving_curvature_gate_passed=False,
        cancellation_factor=cancellation.tolist(),protected_modified_file_count=len(modified),
        protected_check_scope='Mtime guard since '+STARTED+'; not a pre-turn content snapshot')
    saved.write_json(ROOT/'results/status.json',status)
    assert status['all_checks_passed'],'Keep failures; do not change tolerances'
    (ROOT/'results/COMPLETE').write_text('complete\n',encoding='utf-8')
    saved.write_json(ROOT/'progress.json',dict(state='analysis_complete',crossed_actions_saved=144))
    print(json.dumps(dict(checks=len(checks),all_passed=True,cancellation=cancellation.tolist(),
        worst_column_shares=[row for row in records if row['history']==1])),flush=True)


if __name__ == '__main__':
    source.modest()
    parser = argparse.ArgumentParser()
    parser.add_argument('phase',choices=['prepare','evaluate','analyse'])
    parser.add_argument('--max-new-events',type=int,default=144)
    args = parser.parse_args()
    if args.phase == 'prepare':
        prepare()
    elif args.phase == 'evaluate':
        evaluate(args.max_new_events)
    else:
        analyse()
