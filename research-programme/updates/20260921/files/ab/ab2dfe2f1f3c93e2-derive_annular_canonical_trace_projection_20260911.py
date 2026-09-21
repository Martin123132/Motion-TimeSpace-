import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from navier_stokes_source_audit_20260908 import limit_process


def run():
    limit_process()
    import numpy as numerical
    from annular_canonical_trace_context_20260911 import TraceContext
    from annular_canonical_trace_projection_20260911 import kernel_family, trace_extension, gram_density_control
    from annular_canonical_rate_completion_20260911 import evaluate_initial

    parser = argparse.ArgumentParser()
    parser.add_argument('--attempt', required=True)
    arguments = parser.parse_args()
    if not arguments.attempt.isalnum():
        raise ValueError('Fresh alphanumeric attempt required.')
    root = Path(__file__).resolve().parents[1]
    intake = root / 'source-intake/navier-stokes/20260911'
    destination = intake / ('annular-canonical-trace-projection-' + arguments.attempt)
    destination.mkdir(exist_ok=False)
    report = {'state': 'running', 'started_utc': datetime.now(timezone.utc).isoformat(), 'inputs': {}, 'outputs': {}, 'checks': [], 'samples': [], 'valid_for_physics_claim': False, 'new_evolution': False, 'initial_data_refit': False, 'interval_certificate': False, 'protocol': 'Parent full-Gram cell-kernel family; two paired trace-dual extensions, preserving all old phase modes and weak equations. Natural reactions. Actual new momentum force and time links reevaluated, not held fixed. All checks refer to the frozen initial state, not nonlinear evolution.'}

    def digest(path):
        return hashlib.sha256(path.read_bytes()).hexdigest()

    def own(path, table='inputs'):
        report[table][str(path.relative_to(root))] = digest(path)

    def save():
        (destination / 'status.json').write_text(json.dumps(report, indent=2) + '\n')

    def check(name, passed, detail=None):
        report['checks'].append({'name': name, 'passed': bool(passed), 'detail': detail})
        save()
        if not passed:
            raise RuntimeError(name + ': ' + repr(detail))

    save()
    try:
        previous_path = intake / 'annular-canonical-rate-completion-final-integrity.json'
        own(previous_path)
        previous = json.loads(previous_path.read_text())
        check('previous_seal_complete', previous['state'] == 'complete')
        for table in ['inputs', 'outputs']:
            for name, expected in previous[table].items():
                if digest(root / name) != expected:
                    raise RuntimeError('Prior evidence changed: ' + name)
                report['inputs'][name] = expected
        for name in ['annular_canonical_trace_context_20260911.py', 'annular_canonical_trace_projection_20260911.py', Path(__file__).name]:
            path = root / 'scripts' / name
            compile(path.read_bytes(), str(path), 'exec')
            own(path)
            snapshot = destination / ('executed-' + name)
            snapshot.write_bytes(path.read_bytes())
            own(snapshot, 'outputs')
        for branch in ['GR', 'metric_Gram']:
            print('Constructing trace-preserving family for ' + branch, flush=True)
            context = TraceContext(root, branch)
            for path in [context.source_path, context.saved_path, context.parameter_path, context.reference_path]:
                own(path)
            data, frames, completion = context.build()
            baseline = evaluate_initial(frames['mass'], frames['scalar'], data, context.basis, context.weights, context.links, branch != 'GR', context.system.outer_clock)
            prior_arrays = intake / 'annular-canonical-rate-completion-attempt01' / ('N16_' + branch + '_completed.npz')
            with numerical.load(prior_arrays, allow_pickle=False) as archive:
                replay_error = float(abs(archive['constraint_rate'] - baseline['constraint_rate']).max())
            check(branch + '_previous_result_replay', replay_error < 1e-11, replay_error)
            family, primitive, unused_carrier = kernel_family(context, data, frames['mass'], baseline['P_rate_coeff'])
            extended, diagnostics = trace_extension(context, frames['mass'], family)
            actual = evaluate_initial(extended, frames['scalar'], data, context.basis, context.weights, context.links, branch != 'GR', context.system.outer_clock)
            higher = evaluate_initial(extended, frames['scalar'], data, context.basis, context.check_weights, context.check_links, branch != 'GR', context.system.outer_clock, surface='check', link_surface='links_check')
            actual_family, actual_primitive, unused_carrier = kernel_family(context, data, extended, actual['P_rate_coeff'])
            fixed_family_error = max(float(abs(actual_family[surface] - family[surface]).max()) for surface in family)
            record = {'branch': branch, 'completion': completion, 'extension': diagnostics, 'outcomes': {}, 'momentum_rate_change': float(abs(actual['P_t'] - baseline['P_t']).max()), 'added_momentum_rate_coeff_max': float(abs(actual['P_rate_coeff'][-2:]).max()), 'old_momentum_coeff_change': float(abs(actual['P_rate_coeff'][:-2] - baseline['P_rate_coeff']).max()), 'time_link_log_change': float(abs(actual['endpoint_log'] - baseline['endpoint_log']).max()), 'actual_kernel_family_change': fixed_family_error, 'imposed_inner_mass_drive': float(context.saved['boundary_velocity'][0]), 'imposed_outer_scalar_drive': float(context.saved['boundary_velocity'][2]), 'valid_for_physics_claim': False}
            report['samples'].append(record)
            if branch != 'GR':
                coefficients, density, controls = gram_density_control(context, data, actual, actual_family, actual_primitive)
                gram_load_from_bulk = extended['quad']['p'].T @ (context.weights * density)
                values = data['quad']
                bulk_rate = .1 * values['N'] * values['F']**1.5 * values['pi'] * values['w']
                actual_gram_load = extended['quad']['p'].T @ (context.weights * bulk_rate) - actual['mass_pair'] @ actual['mass_rate_coeff']
                controls['independent_link_vs_cell_weak_load_error'] = float(abs(gram_load_from_bulk - actual_gram_load).max())
                record['kernel_controls'] = controls
            for name, result in [('baseline', baseline), ('trace_completed', actual), ('overintegrated', higher)]:
                nodes = data['nodes']
                parent = .1 * nodes['N'][[0, -1]] * nodes['F'][[0, -1]]**1.5 * nodes['pi'][[0, -1]] * nodes['w'][[0, -1]]
                parent += numerical.array([1., -1.]) * .1 * numerical.sqrt(nodes['F'][[0, -1]]) * result['q_nodes'][[0, -1]] * result['gram_scalar'][[0, -1]] / nodes['N'][[0, -1]]
                gaps = result['mu_t_nodes'][[0, -1]] - parent
                predicted = numerical.zeros(nodes['R'].size)
                predicted[[0, -1]] = numerical.array([-1., 1.]) * gaps / (.1 * numerical.sqrt(nodes['F'][[0, -1]]))
                record['outcomes'][name] = {'constraint_max': float(abs(result['constraint']).max()), 'constraint_rate_max': float(abs(result['constraint_rate']).max()), 'interior_constraint_rate_max': float(abs(result['constraint_rate'][1:-1]).max()), 'mass_flux_trace_gaps': gaps.tolist(), 'parent_mass_fluxes': parent.tolist(), 'boundary_identity_error': float(abs(result['constraint_rate'] - predicted).max()), 'imposed_inner_mass_drive_gap': float(result['mu_t_nodes'][0] - context.saved['boundary_velocity'][0]), 'imposed_outer_scalar_drive_gap': float(result['q_nodes'][-1] - context.saved['boundary_velocity'][2])}
                selected = frames['mass'] if name == 'baseline' else extended
                surface = 'check' if name == 'overintegrated' else 'quad'
                arrays = {key: value for key, value in result.items() if isinstance(value, numerical.ndarray)}
                arrays.update({'mass_' + key: value for key, value in selected[surface].items()})
                arrays.update({'mass_nodes_' + key: value for key, value in selected['nodes'].items()})
                arrays.update({'scalar_' + key: value for key, value in frames['scalar'][surface].items()})
                arrays.update({'field_' + key: value for key, value in data[surface].items()})
                arrays.update({'weights': context.check_weights if surface == 'check' else context.weights, 'boundary_prediction': predicted, 'kernel_family': family[surface]})
                check(branch + '_' + name + '_finite', all(numerical.isfinite(value).all() for value in arrays.values()))
                path = destination / (branch + '_' + name + '.npz')
                numerical.savez_compressed(path, **arrays)
                with numerical.load(path, allow_pickle=False) as archive:
                    check(branch + '_' + name + '_roundtrip', set(archive.files) == set(arrays) and all(numerical.array_equal(archive[key], value) for key, value in arrays.items()))
                own(path, 'outputs')
            save()
            print(json.dumps(record), flush=True)
            check(branch + '_two_pairs_and_all_parent_kernel_modes', diagnostics['new_phase_dimension'] == frames['mass']['quad']['q'].shape[1] + 2 and diagnostics['no_parent_family_modes_discarded'])
            check(branch + '_canonical_pairing', diagnostics['block_pairing_error'] < 1e-8 and diagnostics['new_pairing_condition'] < 10, diagnostics)
            check(branch + '_full_family_traces_and_old_moments', max(diagnostics['all_kernel_family_trace_error'], diagnostics['all_old_moments_preserved_error']) < 1e-8)
            check(branch + '_node_silent_continuous_lifts', diagnostics['new_coordinate_interior_node_max'] < 1e-12)
            check(branch + '_momentum_transparency', record['momentum_rate_change'] < 1e-8 and fixed_family_error < 1e-10, record['momentum_rate_change'])
            check(branch + '_all_constraint_rate_rows', max(record['outcomes'][name]['constraint_rate_max'] for name in ['trace_completed', 'overintegrated']) < 1e-10)
            check(branch + '_same_frame_overintegration', float(abs(actual['constraint_rate'] - higher['constraint_rate']).max()) < 1e-10)
            if branch != 'GR':
                check('full_Gram_kernel_reconstruction', max(record['kernel_controls'].values()) < 1e-9, record['kernel_controls'])
                check('external_mass_drive_not_silently_refitted', abs(record['outcomes']['trace_completed']['imposed_inner_mass_drive_gap']) > 1e-9)
        for module in tuple(sys.modules.values()):
            filename = getattr(module, '__file__', None)
            if filename:
                path = Path(filename).resolve()
                if path.parent == root / 'scripts' and path.suffix == '.py':
                    own(path)
        check('no_python_cache', not (root / 'scripts/__pycache__').exists())
        report['state'] = 'complete'
        report['completed_utc'] = datetime.now(timezone.utc).isoformat()
        save()
        print('Trace projection completed.', flush=True)
    except Exception as error:
        report['state'] = 'failed'
        report['error'] = repr(error)
        save()
        raise


if __name__ == '__main__':
    run()
