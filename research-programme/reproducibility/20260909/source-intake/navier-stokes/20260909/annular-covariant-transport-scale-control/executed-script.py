import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from navier_stokes_source_audit_20260908 import limit_process


def run():
    limit_process()
    import numpy as numerical
    from annular_covariant_time_transport_20260909 import ReferenceGeometry, factor_action
    from sbp4_compatible_second_operator_20260909 import norm_weights

    root = Path(__file__).resolve().parents[1]
    intake = root / 'source-intake/navier-stokes/20260909'
    destination = intake / 'annular-covariant-transport-scale-control'
    destination.mkdir(exist_ok=False)
    report = {'state': 'running', 'started_utc': datetime.now(timezone.utc).isoformat(), 'inputs': {}, 'checks': [], 'samples': [], 'valid_for_physics_claim': False, 'scope': 'Bounded fixed N128/256/512 profile-only quadrature, NOT an evolution or repair of the old failed coupled smoke. Measure the completed finite-connection correction against its own leading horizontal principal quadratic form and check predicted smooth-profile O(h^4) action scaling. The comparator is not a full Hamiltonian or a ghost/constraint test.'}
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
        for name in ['derive_annular_covariant_transport_scale_20260909.py', 'annular_covariant_time_transport_20260909.py']:
            own(root / 'scripts' / name)
            compile((root / 'scripts' / name).read_bytes(), name, 'exec')
        prior_path = intake / 'annular-transport-anchor-and-resolution-controls/status.json'
        own(prior_path)
        previous = json.loads(prior_path.read_text())
        verify('prior_covariant_transport_checks_complete', previous['state'] == 'complete' and previous['passed'] == previous['total'])
        for name, digest in previous['inputs'].items():
            own(root / name)
            if report['inputs'][name] != digest:
                raise ValueError('Changed input: ' + name)
        for case_name in ['canonical', 'nonlinear_modulated']:
            path = intake / 'annular-constraint-correction-initial' / (case_name + '.json')
            own(path)
            reference = ReferenceGeometry(json.loads(path.read_text()))
            values = []
            for intervals in [128, 256, 512]:
                report['active_job'] = case_name + '_profile_N' + str(intervals)
                save()
                radii = numerical.linspace(4, 8, intervals + 1)
                spacing = 4 / intervals
                transported = factor_action(reference, 0.18, radii)
                correction = float(transported['value'].sum())
                times = numerical.full_like(radii, 0.18)
                data = reference.fields(times, radii)
                unused_scalar, velocity, coefficient = reference.matter(times, radii)
                connection = reference.connection(times, radii)[0]
                horizontal_gradient = data['scalar_ref'][3] - connection * velocity
                leading = float(numerical.dot(spacing * norm_weights(radii.size), coefficient * horizontal_gradient**2) / 2)
                verify(case_name + '_N' + str(intervals) + '_positive_bounded_profile_quadratic_forms', leading > 0 and correction > 0 and numerical.isfinite(correction))
                row = {'case': case_name, 'intervals': intervals, 'spacing': spacing, 'transported_Gram_density': correction, 'leading_horizontal_principal_quadrature': leading, 'correction_over_leading': correction / leading, 'correction_over_h4': correction / spacing**4, 'full_Hamiltonian_or_stability_test': False}
                report['samples'].append(row)
                values.append(correction)
                save()
            ratios = [values[index] / values[index + 1] for index in range(2)]
            verify(case_name + '_predicted_fourth_order_profile_scaling', all(10 < value < 22 for value in ratios), {'ratios': ratios, 'observed_orders': [float(numerical.log2(value)) for value in ratios], 'uniform_evolved_solution_bound': False})
        verify('all_inputs_unchanged', all(hashlib.sha256((root / name).read_bytes()).hexdigest() == digest for name, digest in report['inputs'].items()))
        verify('no_bytecode_cache', not (root / 'scripts/__pycache__').exists())
        report.update(passed=sum(check['passed'] for check in report['checks']), total=len(report['checks']), completed_utc=datetime.now(timezone.utc).isoformat(), active_job=None)
        report['state'] = 'complete' if report['passed'] == report['total'] else 'failed'
        save()
    except Exception as error:
        report.update(state='failed', failure=repr(error), completed_utc=datetime.now(timezone.utc).isoformat(), active_job=None)
        save()
        raise
    print(json.dumps({key: report[key] for key in ['state', 'passed', 'total', 'completed_utc']}), flush=True)
    if report['state'] != 'complete':
        raise SystemExit(1)
    (destination / 'COMPLETE').write_text(report['completed_utc'] + '\n')


if __name__ == '__main__':
    run()
