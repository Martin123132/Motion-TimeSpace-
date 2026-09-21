import hashlib
import json
import sys
import traceback
from pathlib import Path

from navier_stokes_source_audit_20260908 import limit_process


def run():
    limit_process()
    import numpy as np
    from scipy.linalg import lstsq
    from annular_canonical_common_profile_aligned_20260912 import CommonProfile
    from annular_canonical_trace_context_20260911 import load_archive
    from annular_frozen_second_jet_complex_20260912 import FrozenSecondJet
    from annular_scalar_kinetic_pair_20260912 import refresh, build_pair, kinetic_acceleration_control

    root = Path(__file__).resolve().parents[1]
    intake = root / 'source-intake/navier-stokes/20260912'
    source = intake / 'annular-acceleration-trace-completion-attempt02'
    destination = intake / 'annular-scalar-kinetic-pair-attempt01'
    destination.mkdir(exist_ok=False)
    report = {'state': 'running', 'checks': [], 'cases': [], 'inputs': {}, 'outputs': {}, 'valid_for_physics_claim': False, 'new_evolution': False, 'full_second_jet_closed': False, 'interval_certificate': False, 'physical_initial_fields_changed': False, 'new_finite_scalar_momentum_space': True, 'old_momentum_modes_retained': False, 'coefficient_not_a_new_physical_coupling': True, 'old_working_branch_overwritten': False}

    def own(path, table='inputs'):
        report[table][str(path.relative_to(root))] = hashlib.sha256(path.read_bytes()).hexdigest()

    def save():
        (destination / 'status.json').write_text(json.dumps(report, indent=2) + '\n')

    def check(name, passed, detail=None):
        report['checks'].append({'name': name, 'passed': bool(passed), 'detail': detail})
        save()
        if not passed:
            raise RuntimeError(name + ': ' + repr(detail))

    def archive(name, values):
        path = destination / (name + '.npz')
        np.savez_compressed(path, **values)
        own(path, 'outputs')

    def metrics(model, result):
        first = max(float(abs(model.first[key]).max()) for key in ['constraint', 'constraint_rate'])
        first = max(first, float(abs(model.first['P_t_nodes'][[0, -1]]).max()), abs(model.first['mu_t_nodes'][0] - model.saved['boundary_velocity'][0]), abs(model.first['q_nodes'][-1] - model.saved['boundary_velocity'][2]))
        transform = np.eye(19)[:, list(range(1, 16)) + [17, 18]]
        transform[0] -= model.data['nodes']['eta'][0] @ transform
        transform[16] -= model.data['nodes']['eta'][-1] @ transform
        return {'C0_max': float(abs(result['constraint']).max()), 'C1_max': float(abs(result['constraint_first']).max()), 'C2_full19_max': float(abs(result['constraint_second']).max()), 'C2_compact17_max': float(abs(transform.T @ result['constraint_second']).max()), 'P1_endpoints': model.first['P_t_nodes'][[0, -1]].tolist(), 'P2_endpoints': result['nodes']['P'][[0, -1]].tolist(), 'clock_rate': float(result['clock_first']), 'first_jet_gate': bool(first < 1e-10), 'first_jet_max': float(first), 'full_second_jet_gate': bool(first < 1e-10 and abs(result['compatibility']).max() < 1e-10), 'inferred_drive_accelerations_not_parent_owned': result['inferred_drive_accelerations'].tolist()}

    save()
    try:
        prior_path = intake / 'annular-history-ward-final-integrity.json'
        prior = json.loads(prior_path.read_text())
        check('previous_Ward_derivation_complete', prior['state'] == 'complete' and prior['history_time_Ward_derived'] and not prior['full_second_jet_closed'])
        inherited = dict(prior['inputs'])
        inherited.update(prior['outputs'])
        for name, expected in inherited.items():
            if hashlib.sha256((root / name).read_bytes()).hexdigest() != expected:
                raise RuntimeError('Changed evidence: ' + name)
            report['inputs'][name] = expected
        own(prior_path)
        for path in [Path(__file__), root / 'scripts/annular_scalar_kinetic_pair_20260912.py']:
            compile(path.read_bytes(), str(path), 'exec')
            own(path)
            snapshot = destination / ('executed-' + path.name)
            snapshot.write_bytes(path.read_bytes())
            own(snapshot, 'outputs')
        common = CommonProfile(root)
        for branch in ['GR', 'metric_Gram']:
            print('Kinetic-matched scalar candidate: ' + branch, flush=True)
            model = FrozenSecondJet(common, branch)
            for phase in model.frames:
                raw = load_archive(source / (branch + '_extended_' + phase + '_frames.npz'))
                model.frames[phase] = {surface: {kind: raw[surface + '__' + kind] for kind in ['q', 'qr', 'p']} for surface in model.data}
            refresh(model)
            saved = load_archive(source / (branch + '_completed_second_jet.npz'))
            baseline_result = model.evaluate(saved['lapse_rate_coefficients'])
            baseline = metrics(model, baseline_result)
            baseline_control = kinetic_acceleration_control(model, baseline_result)
            original_first = {surface: {key: value.copy() for key, value in rates.items()} for surface, rates in model.rates.items()}
            frames, diagnostic = build_pair(model)
            check(branch + '_old_configuration_span_retained', max(diagnostic['old_configuration_span_errors'].values()) < 1e-8, diagnostic['old_configuration_span_errors'])
            check(branch + '_all_continuous_source_families_represented', max(diagnostic['family_reconstruction_errors'].values()) < 1e-8, diagnostic['family_reconstruction_errors'])
            check(branch + '_kinetic_matching_all_surfaces_and_SPD_pair', max(diagnostic['pointwise_kinetic_image_errors_all_surfaces'].values()) < 1e-12 and diagnostic['pair_identity_error'] < 1e-10 and diagnostic['pair_condition'] < 1.01)
            model.frames['scalar'] = frames
            refresh(model)
            unchanged = {key: max(float(abs(model.rates[surface][key] - original_first[surface][key]).max()) for surface in model.rates) for key in ['mu', 'P', 'chi']}
            check(branch + '_original_mass_P_and_scalar_velocity_retained', max(unchanged.values()) < 1e-8, unchanged)
            pair = model.first['scalar_pair']
            initial_coeff = np.linalg.solve(pair, frames['quad']['p'].T @ (model.weights * model.data['quad']['N'] * np.sqrt(model.data['quad']['F']) * model.data['quad']['pi'] / model.data['quad']['R']**2))
            reconstruction = {surface: float(abs(frames[surface]['p'] @ initial_coeff - model.data[surface]['pi']).max()) for surface in frames}
            check(branch + '_physical_initial_pi_exactly_represented_without_Kseed_refit', max(reconstruction.values()) < 1e-9, reconstruction)
            same_lapse = model.evaluate(saved['lapse_rate_coefficients'])
            candidate = model.candidate()
            base = model.evaluate(candidate)
            matrix = np.column_stack([model.evaluate(candidate.astype(complex) + 1e-25j * np.eye(19)[column])['compatibility'][-3:].imag / 1e-25 for column in range(19)])
            correction, unused_residual, rank, singular = lstsq(matrix, -base['compatibility'][-3:], cond=1e-12)
            result = model.evaluate(candidate + correction)
            higher = FrozenSecondJet(common, branch, higher=True)
            higher.frames = model.frames
            refresh(higher)
            checked = higher.evaluate(result['lapse_rate_coefficients'])
            control = kinetic_acceleration_control(model, result)
            higher_control = kinetic_acceleration_control(higher, checked)
            check(branch + '_scalar_acceleration_identity_both_quadratures', max(control['scalar_acceleration_projector_identity_error'], higher_control['scalar_acceleration_projector_identity_error']) < 1e-9)
            check(branch + '_whole_kinetic_rate_defect_removed_both_quadratures', max(control['kinetic_rate_defect_max'], higher_control['kinetic_rate_defect_max']) < 1e-9)
            record = {'branch': branch, 'baseline': baseline, 'baseline_kinetic_control': baseline_control, 'same_lapse': metrics(model, same_lapse), 'primary': metrics(model, result), 'higher': metrics(higher, checked), 'primary_kinetic_control': control, 'higher_kinetic_control': higher_control, 'construction': diagnostic, 'initial_rate_retention': unchanged, 'initial_pi_representation': reconstruction, 'boundary_row_rank': int(rank), 'boundary_row_singular_values': singular.tolist(), 'no_C2_fitting': True, 'old_scalar_momentum_space_deliberately_replaced_not_silently_preserved': True}
            report['cases'].append(record)
            for phase, maps in model.frames.items():
                archive(branch + '_extended_' + phase + '_frames', {surface + '__' + kind: value for surface, parts in maps.items() for kind, value in parts.items()})
            archive(branch + '_first_jet', {key: value for key, value in model.first.items() if isinstance(value, np.ndarray)})
            archive(branch + '_completed_second_jet', {**{key: value for key, value in result.items() if isinstance(value, np.ndarray)}, **{key + '_second_coefficients': value for key, value in result['second'].items()}})
            archive(branch + '_higher_second_jet', {key: value for key, value in checked.items() if isinstance(value, np.ndarray)})
            save()
            print(json.dumps({key: value for key, value in record.items() if key not in ['construction', 'initial_pi_representation']}), flush=True)
        for module in tuple(sys.modules.values()):
            filename = getattr(module, '__file__', None)
            if filename:
                path = Path(filename).resolve()
                if path.parent == root / 'scripts' and path.suffix == '.py':
                    own(path)
        check('no_python_cache', not (root / 'scripts/__pycache__').exists())
        report['state'] = 'complete'
        save()
    except Exception as error:
        report.update({'state': 'failed', 'error': repr(error), 'traceback': traceback.format_exc()})
        save()
        raise


if __name__ == '__main__':
    run()
