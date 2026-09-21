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
    from annular_canonical_rate_completion_20260911 import complete_phase
    from annular_cubic_lapse_reference_gravity_20260912 import evaluate_cubic_initial
    from annular_frozen_second_jet_complex_20260912 import FrozenSecondJet

    root = Path(__file__).resolve().parents[1]
    intake = root / 'source-intake/navier-stokes/20260912'
    source = intake / 'annular-acceleration-trace-completion-attempt02'
    ward_source = intake / 'annular-history-ward-attempt02'
    destination = intake / 'annular-scalar-ward-completion-attempt01'
    destination.mkdir(exist_ok=False)
    report = {'state': 'running', 'checks': [], 'cases': [], 'inputs': {}, 'outputs': {}, 'valid_for_physics_claim': False, 'new_evolution': False, 'full_second_jet_closed': False, 'interval_certificate': False, 'physical_fields_changed': False, 'phase_maps_extended_explicitly': True, 'frozen_gauge_family_not_transport_closed_by_assumption': True}

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

    def refresh(model):
        model.first = evaluate_cubic_initial(model.frames['mass'], model.frames['scalar'], model.data, model.basis, model.weights, model.links, model.gram, model.context.system.outer_clock, surface=model.surface, link_surface=model.link_surface)
        for surface in model.rates:
            mass, scalar = model.frames['mass'][surface], model.frames['scalar'][surface]
            model.rates[surface] = {'mu': mass['q'] @ model.first['mass_rate_coeff'], 'mu_r': mass['qr'] @ model.first['mass_rate_coeff'], 'P': mass['p'] @ model.first['P_rate_coeff'], 'pi': scalar['p'] @ model.first['pi_rate_coeff'], 'chi': scalar['q'] @ model.first['q_coeff'], 'w': scalar['qr'] @ model.first['q_coeff']}
        model.prepare_links()

    def metrics(model, result):
        first_error = max(float(abs(model.first[key]).max()) for key in ['constraint', 'constraint_rate'])
        first_error = max(first_error, float(abs(model.first['P_t_nodes'][[0, -1]]).max()), abs(model.first['mu_t_nodes'][0] - model.saved['boundary_velocity'][0]), abs(model.first['q_nodes'][-1] - model.saved['boundary_velocity'][2]))
        return {'C0_max': float(abs(result['constraint']).max()), 'C1_max': float(abs(result['constraint_first']).max()), 'C2_max': float(abs(result['constraint_second']).max()), 'P1_endpoints': model.first['P_t_nodes'][[0, -1]].tolist(), 'P2_endpoints': result['nodes']['P'][[0, -1]].tolist(), 'clock_rate': float(result['clock_first']), 'first_jet_gate': bool(first_error < 1e-10), 'first_jet_max': float(first_error), 'full_second_jet_gate': bool(first_error < 1e-10 and abs(result['compatibility']).max() < 1e-10), 'inferred_drive_accelerations_not_parent_owned': result['inferred_drive_accelerations'].tolist()}

    save()
    try:
        for prior_path in [ward_source / 'status.json', intake / 'annular-history-ward-symbolic-attempt01/status.json']:
            prior = json.loads(prior_path.read_text())
            check(prior_path.parent.name + '_complete', prior['state'] == 'complete' and all(row['passed'] for row in prior['checks']))
            inherited = dict(prior['inputs'])
            inherited.update(prior['outputs'])
            for name, expected in inherited.items():
                if name not in report['inputs'] and hashlib.sha256((root / name).read_bytes()).hexdigest() != expected:
                    raise RuntimeError('Changed evidence: ' + name)
                report['inputs'][name] = expected
            own(prior_path)
        own(Path(__file__))
        snapshot = destination / ('executed-' + Path(__file__).name)
        snapshot.write_bytes(Path(__file__).read_bytes())
        own(snapshot, 'outputs')
        common = CommonProfile(root)
        for branch in ['GR', 'metric_Gram']:
            print('One frozen scalar Ward-family completion: ' + branch, flush=True)
            model = FrozenSecondJet(common, branch)
            for phase in model.frames:
                raw = load_archive(source / (branch + '_extended_' + phase + '_frames.npz'))
                model.frames[phase] = {surface: {kind: raw[surface + '__' + kind] for kind in ['q', 'qr', 'p']} for surface in model.data}
            refresh(model)
            saved = load_archive(source / (branch + '_completed_second_jet.npz'))
            baseline = metrics(model, model.evaluate(saved['lapse_rate_coefficients']))
            gauge = load_archive(ward_source / (branch + '_primary_gauge_test_family.npz'))
            family = {}
            for surface in model.data:
                family[surface] = {kind: np.concatenate([gauge[surface + '__' + tier + '__' + key] for tier in ['gauge', 'gauge_first']], axis=1) for kind, key in [('q', 'chi'), ('qr', 'chi_r'), ('p', 'pi')]}
            original = model.frames['scalar']
            extended, diagnostic = complete_phase(original, family, model.context.reservoir, model.weights)
            retained = {}
            for kind in ['q', 'p']:
                coordinates, unused_residual, rank, singular = lstsq(np.sqrt(model.weights)[:, None] * extended['quad'][kind], np.sqrt(model.weights)[:, None] * original['quad'][kind], cond=1e-13)
                for surface in model.data:
                    denominator = max(1., float(abs(original[surface][kind]).max()))
                    retained[surface + '_' + kind] = float(abs(extended[surface][kind] @ coordinates - original[surface][kind]).max()) / denominator
                    if kind == 'q':
                        retained[surface + '_qr'] = float(abs(extended[surface]['qr'] @ coordinates - original[surface]['qr']).max()) / max(1., float(abs(original[surface]['qr']).max()))
            check(branch + '_all_original_scalar_spaces_retained', max(retained.values()) < 1e-8, retained)
            check(branch + '_whole_frozen_family_represented_not_selected_residual_fit', max(diagnostic['rate_reconstruction_errors'].values()) < 1e-7, diagnostic['rate_reconstruction_errors'])
            model.frames['scalar'] = extended
            refresh(model)
            same_lapse = model.evaluate(saved['lapse_rate_coefficients'])
            candidate = model.candidate()
            base = model.evaluate(candidate)
            boundary_matrix = np.column_stack([model.evaluate(candidate.astype(complex) + 1e-25j * np.eye(19)[column])['compatibility'][-3:].imag / 1e-25 for column in range(19)])
            correction, unused_residual, rank, singular = lstsq(boundary_matrix, -base['compatibility'][-3:], cond=1e-12)
            result = model.evaluate(candidate + correction)
            higher = FrozenSecondJet(common, branch, higher=True)
            higher.frames = model.frames
            refresh(higher)
            checked = higher.evaluate(result['lapse_rate_coefficients'])
            record = {'branch': branch, 'baseline': baseline, 'same_lapse_after_scalar_extension': metrics(model, same_lapse), 'primary_after_three_boundary_rows_only': metrics(model, result), 'higher': metrics(higher, checked), 'completion': diagnostic, 'original_span_errors': retained, 'boundary_row_rank': int(rank), 'boundary_row_singular_values': singular.tolist(), 'no_C2_fitting': True, 'single_frozen_gauge_family_update_only': True}
            report['cases'].append(record)
            for phase, frames in model.frames.items():
                archive(branch + '_extended_' + phase + '_frames', {surface + '__' + key: value for surface, maps in frames.items() for key, value in maps.items()})
            archive(branch + '_completed_second_jet', {**{key: value for key, value in result.items() if isinstance(value, np.ndarray)}, **{key + '_second_coefficients': value for key, value in result['second'].items()}})
            archive(branch + '_higher_second_jet', {key: value for key, value in checked.items() if isinstance(value, np.ndarray)})
            archive(branch + '_first_jet', {key: value for key, value in model.first.items() if isinstance(value, np.ndarray)})
            save()
            print(json.dumps({key: value for key, value in record.items() if key not in ['completion', 'original_span_errors']}), flush=True)
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
