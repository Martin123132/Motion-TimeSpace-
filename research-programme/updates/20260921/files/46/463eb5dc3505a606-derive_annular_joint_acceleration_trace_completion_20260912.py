import hashlib
import json
import traceback
from pathlib import Path

from navier_stokes_source_audit_20260908 import limit_process


def run():
    limit_process()
    import numpy as numerical
    from scipy.linalg import lstsq
    from annular_canonical_common_profile_aligned_20260912 import CommonProfile
    from annular_canonical_trace_projection_stable_20260911 import kernel_family
    from annular_cubic_lapse_reference_gravity_20260912 import evaluate_cubic_initial
    from annular_frozen_second_jet_complex_20260912 import FrozenSecondJet
    from annular_acceleration_trace_completion_20260912 import full_family_trace_extension

    root = Path(__file__).resolve().parents[1]
    intake = root / 'source-intake/navier-stokes/20260912'
    destination = intake / 'annular-acceleration-trace-completion-attempt02'
    destination.mkdir(exist_ok=False)
    report = {'state': 'running', 'checks': [], 'cases': [], 'inputs': {}, 'outputs': {}, 'valid_for_physics_claim': False, 'new_evolution': False, 'interval_certificate': False, 'new_initial_fields': False, 'phase_extension_explicit': True, 'memory_force_time_family_not_yet_completed': True}

    def own(path, table='inputs'):
        report[table][str(path.relative_to(root))] = hashlib.sha256(path.read_bytes()).hexdigest()

    def save():
        (destination / 'status.json').write_text(json.dumps(report, indent=2) + '\n')

    def check(name, passed, detail=None):
        report['checks'].append({'name': name, 'passed': bool(passed), 'detail': detail})
        save()
        if not passed:
            raise RuntimeError(name + ': ' + repr(detail))

    def archive(name, arrays):
        path = destination / (name + '.npz')
        numerical.savez_compressed(path, **arrays)
        with numerical.load(path, allow_pickle=False) as saved:
            check(name + '_finite_roundtrip', set(saved.files) == set(arrays) and all(numerical.isfinite(value).all() and numerical.array_equal(value, saved[key]) for key, value in arrays.items()))
        own(path, 'outputs')

    save()
    try:
        previous_path = intake / 'annular-frozen-second-jet-control-attempt02/status.json'
        prior = json.loads(previous_path.read_text())
        own(previous_path)
        check('independent_second_jet_control_complete', prior['state'] == 'complete')
        known = {}
        for table in ['inputs', 'outputs']:
            for name, expected in prior[table].items():
                if name not in known:
                    known[name] = hashlib.sha256((root / name).read_bytes()).hexdigest()
                if known[name] != expected:
                    raise RuntimeError('Changed evidence: ' + name)
                report['inputs'][name] = expected
        for name in ['annular_acceleration_trace_completion_20260912.py', Path(__file__).name]:
            path = root / 'scripts' / name
            compile(path.read_bytes(), str(path), 'exec')
            own(path)
            snapshot = destination / ('executed-' + name)
            snapshot.write_bytes(path.read_bytes())
            own(snapshot, 'outputs')
        common = CommonProfile(root)
        for branch in ['GR', 'metric_Gram']:
            print('Constructing 35-direction acceleration trace family: ' + branch, flush=True)
            model = FrozenSecondJet(common, branch)
            old_first = model.first
            old_frames = model.frames['mass']
            family, unused_primitive, unused_carrier = kernel_family(model.context, model.data, old_frames, old_first['P_rate_coeff'])
            for surface in family:
                values, rates = model.data[surface], model.rates[surface]
                factor = .1 * (values['F']**1.5 * (rates['pi'] * values['w'] + values['pi'] * rates['w']) - 3 * numerical.sqrt(values['F']) * rates['mu'] * values['pi'] * values['w'] / values['R'])
                bulk_family = values['eta'] * factor[:, None]
                bulk_family += .1 * (values['R'] * values['F']**1.5 * rates['P'])[:, None] * (values['F'][:, None] * values['eta_r'] - values['F_r'][:, None] * values['eta'] / 2)
                family[surface] = numerical.concatenate([family[surface], bulk_family], axis=1)
            extended, diagnostic = full_family_trace_extension(model.context, old_frames, family)
            check(branch + '_all_35_parent_directions_traces_pass', diagnostic['parent_family_dimension'] == 35 and diagnostic['all_kernel_family_trace_error'] < 1e-9 and diagnostic['all_old_moments_preserved_error'] < 1e-9, diagnostic)
            model.frames['mass'] = extended
            scalar_family = {}
            for surface in family:
                values, rates = model.data[surface], model.rates[surface]
                factor = numerical.sqrt(values['F']) * rates['pi'] / values['R']**2 - rates['mu'] * values['pi'] / (values['R']**3 * numerical.sqrt(values['F'])) + .1 * values['F']**1.5 * rates['P'] * values['w']
                scalar_family[surface] = values['eta'] * factor[:, None]
            scalar_extended, scalar_diagnostic = full_family_trace_extension(model.context, model.frames['scalar'], scalar_family)
            check(branch + '_all_19_scalar_acceleration_traces_pass', scalar_diagnostic['parent_family_dimension'] == 19 and scalar_diagnostic['all_kernel_family_trace_error'] < 1e-9, scalar_diagnostic)
            model.frames['scalar'] = scalar_extended
            model.first = evaluate_cubic_initial(extended, model.frames['scalar'], model.data, model.basis, model.weights, model.links, model.gram, model.context.system.outer_clock)
            first_change = max(float(abs(model.first[key] - old_first[key]).max()) for key in ['constraint', 'constraint_rate', 'mu_t_nodes', 'P_t_nodes', 'q_nodes'])
            record = {'branch': branch, 'completion': diagnostic, 'scalar_completion': scalar_diagnostic, 'first_change_max': first_change, 'first_C_max': float(abs(model.first['constraint']).max()), 'first_Cdot_max': float(abs(model.first['constraint_rate']).max()), 'first_Pdot_trace_max': float(abs(model.first['P_t_nodes'][[0, -1]]).max())}
            report['cases'].append(record)
            for surface in model.rates:
                model.rates[surface]['mu'] = extended[surface]['q'] @ model.first['mass_rate_coeff']
                model.rates[surface]['mu_r'] = extended[surface]['qr'] @ model.first['mass_rate_coeff']
                model.rates[surface]['P'] = extended[surface]['p'] @ model.first['P_rate_coeff']
            for surface in model.rates:
                model.rates[surface]['chi'] = scalar_extended[surface]['q'] @ model.first['q_coeff']
                model.rates[surface]['w'] = scalar_extended[surface]['qr'] @ model.first['q_coeff']
                model.rates[surface]['pi'] = scalar_extended[surface]['p'] @ model.first['pi_rate_coeff']
            model.prepare_links()
            candidate = model.candidate()
            base = model.evaluate(candidate)
            matrix = numerical.column_stack([model.evaluate(candidate.astype(complex) + 1e-25j * numerical.eye(19)[column])['compatibility'][-3:].imag / 1e-25 for column in range(19)])
            correction, unused_residual, rank, singular = lstsq(matrix, -base['compatibility'][-3:], cond=1e-12)
            result = model.evaluate(candidate + correction)
            higher = FrozenSecondJet(common, branch, higher=True)
            higher.frames['mass'] = extended
            higher.frames['scalar'] = scalar_extended
            higher.first = evaluate_cubic_initial(extended, higher.frames['scalar'], higher.data, higher.basis, higher.weights, higher.links, higher.gram, higher.context.system.outer_clock, surface='check', link_surface='links_check')
            for surface in higher.rates:
                higher.rates[surface]['mu'] = extended[surface]['q'] @ higher.first['mass_rate_coeff']
                higher.rates[surface]['mu_r'] = extended[surface]['qr'] @ higher.first['mass_rate_coeff']
                higher.rates[surface]['P'] = extended[surface]['p'] @ higher.first['P_rate_coeff']
            for surface in higher.rates:
                higher.rates[surface]['chi'] = scalar_extended[surface]['q'] @ higher.first['q_coeff']
                higher.rates[surface]['w'] = scalar_extended[surface]['qr'] @ higher.first['q_coeff']
                higher.rates[surface]['pi'] = scalar_extended[surface]['p'] @ higher.first['pi_rate_coeff']
            higher.prepare_links()
            checked = higher.evaluate(candidate + correction)
            record.update({'three_boundary_row_rank': int(rank), 'boundary_row_singular_values': singular.tolist(), 'candidate_Cddot_max': float(abs(base['constraint_second']).max()), 'corrected_Cddot_max': float(abs(result['constraint_second']).max()), 'higher_Cddot_max': float(abs(checked['constraint_second']).max()), 'corrected_Pddot_endpoints': result['nodes']['P'][[0, -1]].tolist(), 'corrected_clock_rate_error': float(result['clock_first']), 'inferred_drive_accelerations': result['inferred_drive_accelerations'].tolist(), 'lapse_rate_max': float(abs(model.data['quad']['eta'] @ result['lapse_rate_coefficients']).max()), 'finite_full_second_jet_gate': bool(abs(result['compatibility']).max() < 1e-10 and abs(checked['compatibility']).max() < 1e-10)})
            check(branch + '_retained_first_jet_gates', max(record['first_C_max'], record['first_Cdot_max'], record['first_Pdot_trace_max'], abs(model.first['mu_t_nodes'][0] - model.saved['boundary_velocity'][0]), abs(model.first['q_nodes'][-1] - model.saved['boundary_velocity'][2])) < 1e-10)
            archive(branch + '_extended_scalar_frames', {surface + '__' + kind: value for surface, parts in scalar_extended.items() for kind, value in parts.items()})
            archive(branch + '_first_jet', {key: value for key, value in model.first.items() if isinstance(value, numerical.ndarray)})
            archive(branch + '_extended_mass_frames', {surface + '__' + kind: value for surface, parts in extended.items() for kind, value in parts.items()})
            archive(branch + '_completed_second_jet', {**{key: value for key, value in result.items() if isinstance(value, numerical.ndarray)}, **{key + '_second_coefficients': value for key, value in result['second'].items()}})
            archive(branch + '_higher_second_jet', {key: value for key, value in checked.items() if isinstance(value, numerical.ndarray)})
            print(json.dumps(record), flush=True)
            save()
        check('no_python_cache', not (root / 'scripts/__pycache__').exists())
        report['state'] = 'complete'
        save()
    except Exception as error:
        report.update({'state': 'failed', 'error': repr(error), 'traceback': traceback.format_exc()})
        save()
        raise


if __name__ == '__main__':
    run()
