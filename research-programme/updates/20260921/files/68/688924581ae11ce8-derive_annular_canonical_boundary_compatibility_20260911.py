import hashlib
import json
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path

from navier_stokes_source_audit_20260908 import limit_process


def run():
    limit_process()
    import numpy as numerical
    from annular_gram_joint_action_20260909 import gram_matrices

    root = Path(__file__).resolve().parents[1]
    intake = root / 'source-intake/navier-stokes/20260911'
    destination = intake / 'annular-canonical-boundary-compatibility-attempt01'
    destination.mkdir(exist_ok=False)
    report = {'state': 'running', 'inputs': {}, 'outputs': {}, 'checks': [], 'factor_signs': [], 'boundary_data': [], 'valid_for_physics_claim': False, 'new_evolution': False, 'coefficient_scope': 'Exact rational signs of the stored floating-point factors and scalar samples, not an interval enclosure of independently rounded analytic factors.', 'conditional_lemma': 'For the canonical P=0 GR+scalar branch with continuous one-sided traces and no P-linear boundary source, prescribed mudot must equal kappa*R^2*F*q*w. For the Gram branch subtract its full oriented G_P trace; positivity of a Gram quadratic form alone does not fix its endpoint-force sign.'}

    def digest(path):
        return hashlib.sha256(path.read_bytes()).hexdigest()

    def own(path, table='inputs'):
        report[table][str(path.relative_to(root))] = digest(path)

    def check(name, passed, detail=None):
        report['checks'].append({'name': name, 'passed': bool(passed), 'detail': detail})
        if not passed:
            raise RuntimeError(name + ': ' + repr(detail))

    prior_path = intake / 'annular-canonical-mass-reduction-control-attempt01/status.json'
    own(prior_path)
    prior = json.loads(prior_path.read_text())
    check('prior_complete', prior['state'] == 'complete' and all(item['passed'] for item in prior['checks']))
    for table in ['inputs', 'outputs']:
        for name, expected in prior[table].items():
            if digest(root / name) != expected:
                raise RuntimeError('Completed evidence changed: ' + name)
            report['inputs'][name] = expected
    own(Path(__file__))
    snapshot = destination / ('executed-' + Path(__file__).name)
    snapshot.write_bytes(Path(__file__).read_bytes())
    own(snapshot, 'outputs')
    for sample in prior['samples']:
        boundary = sample['boundary_prediction']
        difference = Fraction(int(boundary['exact_mismatch_numerator']), int(boundary['exact_mismatch_denominator']))
        check(sample['label'] + '_exact_bulk_port_mismatch_recorded', float(difference) == boundary['prescribed_minus_bulk_flux'] and difference != 0)
        report['boundary_data'].append({'label': sample['label'], 'bulk_flux': boundary['bulk_flux_from_prescribed_scalar_velocity'], 'prescribed_flux': boundary['prescribed_inner_flux'], 'exact_difference': str(difference), 'relative_difference': boundary['relative_mismatch'], 'Gram_P_trace': boundary.get('Gram_P_force_inner_trace'), 'bulk_mismatch_is_GR_condition_not_a_Gram_exclusion': True})
    for mesh in [16, 32, 64]:
        source_path = root / 'source-intake/navier-stokes/20260910/annular-parent-root-residence-attempt02' / ('canonical_N' + str(mesh) + '_metric_Gram_sample0.npz')
        own(source_path)
        with numerical.load(source_path, allow_pickle=False) as archive:
            count = archive['basis_radii'].size
            configuration = archive['original_configuration'][:count]
        factors, sampling = gram_matrices(count)
        check('N' + str(mesh) + '_sampling_positive_normalized_and_zero_at_inner_endpoint', numerical.all(sampling >= 0) and numerical.all(sampling.sum(axis=1) == 1) and numerical.all(sampling[:, 0] == 0))
        selected = numerical.flatnonzero(factors[:, 0] != 0)
        rows = []
        for index in selected:
            amplitude = sum((Fraction.from_float(float(weight)) * Fraction.from_float(float(value)) for weight, value in zip(factors[index], configuration)), Fraction(0))
            product = -Fraction.from_float(float(factors[index, 0])) * amplitude
            rows.append({'factor': int(index), 'minus_B_inner_times_amplitude': float(product), 'exact_product': str(product), 'sign': 'positive' if product > 0 else 'negative' if product < 0 else 'zero'})
        positive = sum(row['sign'] == 'positive' for row in rows)
        negative = sum(row['sign'] == 'negative' for row in rows)
        report['factor_signs'].append({'mesh': mesh, 'contributing_factors': len(rows), 'positive_products': positive, 'negative_products': negative, 'unconditional_force_sign_from_these_products': 'positive' if positive and not negative else 'negative' if negative and not positive else 'not_sign_definite', 'rows': rows})
    report['state'] = 'complete'
    report['completed_utc'] = datetime.now(timezone.utc).isoformat()
    check('no_python_cache', not (root / 'scripts/__pycache__').exists())
    (destination / 'status.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'state': report['state'], 'checks': len(report['checks']), 'factor_signs': [{key: value for key, value in item.items() if key != 'rows'} for item in report['factor_signs']], 'boundary_data': report['boundary_data']}), flush=True)


if __name__ == '__main__':
    run()
