import argparse
import hashlib
import json
import sys
import traceback
from datetime import datetime, timezone
from pathlib import Path

from navier_stokes_source_audit_20260908 import limit_process


def run():
    limit_process()
    import numpy as numerical
    from annular_canonical_common_profile_aligned_20260912 import CommonProfile, RefinedContext, RefinedPreparation
    from annular_canonical_rate_completion_20260911 import evaluate_initial
    from annular_cubic_lapse_boundary_fixed_20260912 import CubicContext, CubicPreparation, CubicFields, evaluate_cubic_initial

    parser = argparse.ArgumentParser()
    parser.add_argument('--attempt', required=True)
    arguments = parser.parse_args()
    if not arguments.attempt.isalnum():
        raise ValueError('Fresh alphanumeric attempt required.')
    root = Path(__file__).resolve().parents[1]
    intake = root / 'source-intake/navier-stokes/20260912'
    directory = intake / ('annular-cubic-lapse-boundary-' + arguments.attempt)
    directory.mkdir(exist_ok=False)
    report = {'state': 'running', 'started_utc': datetime.now(timezone.utc).isoformat(), 'inputs': {}, 'outputs': {}, 'checks': [], 'cases': [], 'valid_for_physics_claim': False, 'new_evolution': False, 'interval_certificate': False, 'protocol': 'N16 only. Shared coarse free data and Kseed. Full P1 plus two global cubic lapse directions, old constraints retained plus two new rows. Two derived zero-endpoint mass lifts supply dependent mass coefficients. Natural-gradient corrected and enlarged uncorrected controls use same phase construction and boundary drives.'}

    def digest(path):
        return hashlib.sha256(path.read_bytes()).hexdigest()

    def own(path, table='inputs'):
        report[table][str(path.relative_to(root))] = digest(path)

    def save():
        (directory / 'status.json').write_text(json.dumps(report, indent=2) + '\n')

    def check(name, passed, detail=None, fatal=True):
        report['checks'].append({'name': name, 'passed': bool(passed), 'detail': detail})
        save()
        if fatal and not passed:
            raise RuntimeError(name + ': ' + repr(detail))

    def archive(name, arrays):
        path = directory / (name + '.npz')
        numerical.savez_compressed(path, **arrays)
        with numerical.load(path, allow_pickle=False) as saved:
            check(name + '_finite_roundtrip', set(saved.files) == set(arrays) and all(numerical.isfinite(value).all() and numerical.array_equal(value, saved[key]) for key, value in arrays.items()))
        own(path, 'outputs')

    save()
    try:
        previous_path = intake / 'annular-bounded-nonlinear-final-integrity.json'
        own(previous_path)
        previous = json.loads(previous_path.read_text())
        check('previous_seal_complete', previous['state'] == 'complete')
        for table in ['inputs', 'outputs']:
            for name, expected in previous[table].items():
                if digest(root / name) != expected:
                    raise RuntimeError('Changed source evidence: ' + name)
                report['inputs'][name] = expected
        for name in ['annular_cubic_lapse_boundary_fixed_20260912.py', Path(__file__).name]:
            path = root / 'scripts' / name
            compile(path.read_bytes(), str(path), 'exec')
            own(path)
            snapshot = directory / ('executed-' + name)
            snapshot.write_bytes(path.read_bytes())
            own(snapshot, 'outputs')
        common = CommonProfile(root)
        for branch in ['GR', 'metric_Gram']:
            replay_context = RefinedContext(common, 16, branch)
            unused_amplitudes, replay, unused_history = RefinedPreparation(replay_context).solve()
            generalized = evaluate_cubic_initial(replay['frames']['mass'], replay['frames']['scalar'], replay['data'], replay_context.basis, replay_context.weights, replay_context.links, replay_context.include_gram, replay_context.system.outer_clock)
            original = replay['actual']
            replay_error = max(float(abs(original[key] - generalized[key]).max()) for key in ['constraint', 'constraint_rate', 'gram_constraint_rate', 'mu_t_nodes', 'P_t_nodes', 'q_nodes'])
            check(branch + '_generalized_covectors_replay_original_P1', replay_error < 1e-13, replay_error)
            report.setdefault('original_replay', {})[branch] = {'C_max': float(abs(original['constraint']).max()), 'Cdot_max': float(abs(original['constraint_rate']).max()), 'Pdot_endpoints': original['P_t_nodes'][[0, -1]].tolist()}
            del replay_context, replay, generalized, original
            context = CubicContext(common, branch)
            eta = context.family.evaluate(context.points)[0]
            check(branch + '_nineteen_independent_lapse_directions', eta.shape[1] == 19 and numerical.linalg.matrix_rank(numerical.sqrt(context.weights)[:, None] * eta) == 19)
            extra_mass, unused_gradient = context.family.mass(context.basis.radii[[0, -1]])
            check(branch + '_two_mass_lifts_preserve_endpoint_values', abs(extra_mass).max() < 1e-12, extra_mass.tolist())
            for correction in [False, True]:
                label = branch + ('_corrected' if correction else '_enlarged_uncorrected')
                record = {'label': label, 'branch': branch, 'correction': correction, 'state': 'running', 'started_utc': datetime.now(timezone.utc).isoformat()}
                report['cases'].append(record)
                save()
                print('Starting ' + label, flush=True)
                try:
                    preparation = CubicPreparation(context, correction=correction)
                    amplitudes, prepared, history = preparation.solve()
                    actual, data, frames, selected = prepared['actual'], prepared['data'], prepared['frames'], prepared['saved']
                    higher = evaluate_cubic_initial(frames['mass'], frames['scalar'], data, context.basis, context.check_weights, context.check_links, context.include_gram, context.system.outer_clock, surface='check', link_surface='links_check')
                    record.update({'amplitudes': amplitudes.tolist(), 'lapse_gradient_amplitudes': selected['lapse_boundary_amplitudes'].tolist(), 'mass_lift_coefficients': selected['mass_lift_coefficients'].tolist(), 'mass_jacobian_condition': float(numerical.linalg.cond(preparation.mass_equations(selected)[1])), 'history': history, 'calls': preparation.calls, 'completion': prepared['completion'], 'trace_extension': prepared['extension'], 'outcomes': {}})
                    nodes = data['nodes']
                    energy = nodes['pi']**2 / (2 * nodes['R']**2) + nodes['R']**2 * nodes['w']**2 / 2
                    strong_Pdot = nodes['N'] / (.1 * numerical.sqrt(nodes['F'])) * (.1 * energy / nodes['R'] + nodes['mu'] / (nodes['R']**2 * nodes['F']) - nodes['N_r'] / nodes['N'])
                    for variant, result in [('primary', actual), ('higher', higher)]:
                        parent_flux = .1 * nodes['N'][[0, -1]] * nodes['F'][[0, -1]]**1.5 * nodes['pi'][[0, -1]] * nodes['w'][[0, -1]]
                        parent_flux += numerical.array([1., -1.]) * .1 * numerical.sqrt(nodes['F'][[0, -1]]) * result['q_nodes'][[0, -1]] * result['gram_scalar'][[0, -1]] / nodes['N'][[0, -1]]
                        record['outcomes'][variant] = {'C_max': float(abs(result['constraint']).max()), 'Cdot_max': float(abs(result['constraint_rate']).max()), 'C_original_rows': float(abs(result['constraint'][:17]).max()), 'C_new_rows': result['constraint'][-2:].tolist(), 'Cdot_new_rows': result['constraint_rate'][-2:].tolist(), 'mass_trace_gaps': (result['mu_t_nodes'][[0, -1]] - parent_flux).tolist(), 'mass_drive_gap': float(result['mu_t_nodes'][0] - selected['boundary_velocity'][0]), 'outer_q_gap': float(result['q_nodes'][-1] - selected['boundary_velocity'][2]), 'clock_gap': float(nodes['N'][-1] / numerical.sqrt(nodes['F'][-1]) - context.system.outer_clock), 'Pdot_endpoints': result['P_t_nodes'][[0, -1]].tolist(), 'strong_Pdot_endpoints': strong_Pdot[[0, -1]].tolist(), 'minimum_sampled_N': float(min(values['N'].min() for values in data.values())), 'minimum_sampled_F': float(min(values['F'].min() for values in data.values())), 'link_log_max': float(abs(result['endpoint_log']).max())}
                        archive(label + '_' + variant, {key: value for key, value in result.items() if isinstance(value, numerical.ndarray)})
                    archive(label + '_initial_data', {**selected, 'pi_boundary_amplitudes': amplitudes, 'radii': context.basis.radii, 'faces': context.basis.faces, 'lapse_extra_projection': context.family.projection, 'lapse_extra_transform': context.family.transform, 'mass_lift_scales': context.family.mass_scale, 'mass_lift_endpoint_drift': context.family.endpoint_drift, 'mass_lift_endpoint_origin': context.family.endpoint_origin})
                    archive(label + '_frames', {phase + '__' + surface + '__' + kind: value for phase, maps in frames.items() for surface, parts in maps.items() for kind, value in parts.items()})
                    archive(label + '_data', {surface + '__' + key: value for surface, values in data.items() for key, value in values.items()})
                    finite_gate = all(max(values['C_max'], values['Cdot_max'], abs(values['mass_drive_gap']), abs(values['outer_q_gap']), abs(values['clock_gap']), max(abs(value) for value in values['mass_trace_gaps'])) < 1e-10 for values in record['outcomes'].values())
                    record['finite_initial_gate'] = finite_gate
                    record['classical_P_trace_tangent_gate'] = max(abs(value) for values in record['outcomes'].values() for value in values['Pdot_endpoints']) < 1e-10
                    check(label + '_all_nineteen_constraints_and_drives', finite_gate, record['outcomes'], fatal=False)
                    check(label + '_all_original_phase_modes_retained', all(row['original_modes_removed'] == 0 for row in prepared['completion'].values()))
                    if correction:
                        check(label + '_exact_cubic_strong_boundary_law', max(abs(value) for value in strong_Pdot[[0, -1]]) < 1e-12)
                    record.update({'state': 'complete', 'completed_utc': datetime.now(timezone.utc).isoformat()})
                    print(json.dumps({'label': label, 'finite_gate': finite_gate, 'classical_P_trace_gate': record['classical_P_trace_tangent_gate'], 'outcomes': record['outcomes']}), flush=True)
                except Exception as error:
                    record.update({'state': 'failed', 'error': repr(error), 'traceback': traceback.format_exc()})
                    print(label + ' FAILED: ' + repr(error), flush=True)
                save()
        for module in tuple(sys.modules.values()):
            filename = getattr(module, '__file__', None)
            if filename:
                path = Path(filename).resolve()
                if path.parent == root / 'scripts' and path.suffix == '.py':
                    own(path)
        check('no_python_cache', not (root / 'scripts/__pycache__').exists())
        report['state'] = 'complete' if all(row['state'] == 'complete' for row in report['cases']) and all(row['passed'] for row in report['checks']) else 'complete_with_failures'
        report['completed_utc'] = datetime.now(timezone.utc).isoformat()
        save()
        print(json.dumps({'state': report['state'], 'checks': len(report['checks']), 'cases': [{key: row[key] for key in ['label', 'state']} for row in report['cases']]}), flush=True)
    except Exception as error:
        report.update({'state': 'failed', 'error': repr(error), 'traceback': traceback.format_exc()})
        save()
        raise


if __name__ == '__main__':
    run()
