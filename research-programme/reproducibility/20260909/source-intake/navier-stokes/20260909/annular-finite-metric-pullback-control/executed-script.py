import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from navier_stokes_source_audit_20260908 import limit_process


def run():
    limit_process()
    import numpy as numerical
    from annular_covariant_time_transport_20260909 import ReferenceGeometry, coordinate_map
    from annular_gram_joint_action_20260909 import principal_coefficient

    root = Path(__file__).resolve().parents[1]
    intake = root / 'source-intake/navier-stokes/20260909'
    destination = intake / 'annular-finite-metric-pullback-control'
    destination.mkdir(exist_ok=False)
    report = {'state': 'running', 'started_utc': datetime.now(timezone.utc).isoformat(), 'inputs': {}, 'checks': [], 'valid_for_physics_claim': False, 'scope': 'Independent finite metric pullback, including nonzero transformed beta before gauge restriction, verifies A and nonlinear principal time-density laws. This is time-reparametrization with R fixed, not arbitrary spacetime diffeomorphisms or discrete gravitational constraint closure.'}
    (destination / 'executed-script.py').write_bytes(Path(__file__).read_bytes())

    def save():
        (destination / 'status.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')

    def own(path):
        report['inputs'][str(path.relative_to(root))] = hashlib.sha256(path.read_bytes()).hexdigest()

    def verify(name, passed, detail=None):
        report['checks'].append({'name': name, 'passed': bool(passed), 'detail': detail})
        save()
        print(name + ': ' + str(bool(passed)), flush=True)

    save()
    try:
        for name in ['verify_annular_finite_metric_pullback_20260909.py', 'annular_covariant_time_transport_20260909.py', 'annular_gram_joint_action_20260909.py']:
            own(root / 'scripts' / name)
            compile((root / 'scripts' / name).read_bytes(), name, 'exec')
        prior_path = intake / 'annular-covariant-transport-scale-control/status.json'
        own(prior_path)
        prior = json.loads(prior_path.read_text())
        if prior['state'] != 'complete':
            raise ValueError('Prior controls must finish first')
        for name, digest in prior['inputs'].items():
            own(root / name)
            if report['inputs'][name] != digest:
                raise ValueError('Input changed: ' + name)
        for case_name in ['canonical', 'nonlinear_modulated']:
            path = intake / 'annular-constraint-correction-initial' / (case_name + '.json')
            own(path)
            reference = ReferenceGeometry(json.loads(path.read_text()))
            radius = numerical.linspace(4, 8, 129)
            for size in [-0.08, 0.08]:
                mapped, jacobian, radial_map, unused_second, unused_mixed = coordinate_map(numerical.full_like(radius, 0.18), radius, size)
                data = reference.fields(mapped, radius)
                scalar, velocity, unused_acceleration, gradient = data['scalar_ref']
                exponential = numerical.exp(data['shift_ref'][0])
                lapse = 1 - 2 * data['mass_ref'][0] / radius - reference.constants['Lambda'] * radius**2 / 3
                sigma = reference.sigma
                original_tt = -exponential**2 * lapse
                original_tr = exponential + sigma * original_tt
                original_rr = 2 * sigma * exponential + sigma**2 * original_tt
                transformed_tt = jacobian**2 * original_tt
                transformed_tr = jacobian * (original_tt * radial_map + original_tr)
                transformed_rr = original_tt * radial_map**2 + 2 * original_tr * radial_map + original_rr
                new_exponential = transformed_tr - sigma * transformed_tt
                new_lapse = -transformed_tt / new_exponential**2
                new_beta = transformed_rr - 2 * sigma * transformed_tr + sigma**2 * transformed_tt
                new_mass = radius * (1 - new_lapse - reference.constants['Lambda'] * radius**2 / 3) / 2
                primitive = numerical.stack([scalar, jacobian * velocity, gradient + radial_map * velocity, new_mass, numerical.log(new_exponential), new_beta])
                direct_density = principal_coefficient(primitive, radius, reference.constants, sigma)
                expected_density = jacobian * reference.matter(mapped, radius)[2]
                density_error = float(numerical.max(numerical.abs(direct_density - expected_density)))
                density_scale = float(numerical.max(numerical.abs(expected_density)))
                expected_connection = (reference.connection(mapped, radius)[0] + radial_map) / jacobian
                connection_error = float(numerical.max(numerical.abs(transformed_tr / transformed_tt - expected_connection)))
                tag = case_name + '_eta' + str(size)
                verify(tag + '_finite_ungauged_metric_produces_density_law', density_error < 2e-13 * density_scale, {'relative_error': density_error / density_scale, 'nonzero_beta_max': float(numerical.max(numerical.abs(new_beta)))})
                verify(tag + '_finite_metric_produces_connection_law', connection_error < 2e-13)
                primitive[5] = 0
                false_density = principal_coefficient(primitive, radius, reference.constants, sigma)
                false_error = float(numerical.max(numerical.abs(false_density - expected_density)))
                verify(tag + '_premature_beta_gauge_reset_is_detectably_wrong', false_error > 1000 * max(density_error, 1e-15), {'wrong_gauge_density_error': false_error})
        verify('all_inputs_unchanged', all(hashlib.sha256((root / name).read_bytes()).hexdigest() == digest for name, digest in report['inputs'].items()))
        verify('no_bytecode_cache', not (root / 'scripts/__pycache__').exists())
        report.update(passed=sum(check['passed'] for check in report['checks']), total=len(report['checks']), completed_utc=datetime.now(timezone.utc).isoformat())
        report['state'] = 'complete' if report['passed'] == report['total'] else 'failed'
        save()
    except Exception as error:
        report.update(state='failed', failure=repr(error), completed_utc=datetime.now(timezone.utc).isoformat())
        save()
        raise
    print(json.dumps({key: report[key] for key in ['state', 'passed', 'total', 'completed_utc']}), flush=True)
    if report['state'] != 'complete':
        raise SystemExit(1)
    (destination / 'COMPLETE').write_text(report['completed_utc'] + '\n')


if __name__ == '__main__':
    run()
