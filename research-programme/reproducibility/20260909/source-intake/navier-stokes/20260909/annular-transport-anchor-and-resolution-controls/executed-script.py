import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from navier_stokes_source_audit_20260908 import limit_process


def run():
    limit_process()
    import numpy as numerical
    from annular_covariant_time_transport_20260909 import ReferenceGeometry, factor_action, layout, transport
    from annular_mixed_grid_basis_20260909 import mixed_basis

    root = Path(__file__).resolve().parents[1]
    intake = root / 'source-intake/navier-stokes/20260909'
    destination = intake / 'annular-transport-anchor-and-resolution-controls'
    destination.mkdir(exist_ok=False)
    report = {'state': 'running', 'started_utc': datetime.now(timezone.utc).isoformat(), 'checks': [], 'inputs': {}, 'samples': [], 'valid_for_physics_claim': False, 'scope': 'Anchor independence under corresponding time-boundary transport; actual changed Gram density versus the old chart-fixed term; exact fixed-basis product-defect bound and controlled approximation, not a demand that every GR discretization have exact lattice diffeomorphism symmetry. No coupled constraint/evolution/causality/horizon/calibration certificate.'}
    (destination / 'executed-script.py').write_bytes(Path(__file__).read_bytes())

    def save():
        (destination / 'status.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')

    def own(path):
        report['inputs'][str(path.relative_to(root))] = hashlib.sha256(path.read_bytes()).hexdigest()

    def verify(name, passed, detail=None):
        report['checks'].append({'name': name, 'passed': bool(passed), 'detail': detail})
        save()
        print(name + ': ' + str(bool(passed)), flush=True)

    def maximum(value):
        return float(numerical.max(numerical.abs(value)))

    save()
    try:
        for name in ['derive_annular_transport_anchor_and_resolution_controls_20260909.py', 'annular_covariant_time_transport_20260909.py', 'annular_mixed_grid_basis_20260909.py']:
            own(root / 'scripts' / name)
            compile((root / 'scripts' / name).read_bytes(), name, 'exec')
        prior_path = intake / 'annular-covariant-transport-and-mixed-basis-derived/status.json'
        own(prior_path)
        prior = json.loads(prior_path.read_text())
        verify('prior_transport_and_mixed_basis_terminal_and_passed', prior['state'] == 'complete' and prior['passed'] == prior['total'])
        for name, digest in {**prior['inputs'], **prior['outputs']}.items():
            path = root / name
            own(path)
            if report['inputs'][name] != digest:
                raise ValueError('Input changed: ' + name)
        for case_name in ['canonical', 'nonlinear_modulated']:
            case_path = intake / 'annular-constraint-correction-initial' / (case_name + '.json')
            own(case_path)
            reference = ReferenceGeometry(json.loads(case_path.read_text()))
            radii = numerical.linspace(4, 8, 129)
            spacing = float(radii[1] - radii[0])
            factors, sampling, factor_index, node_index, old_anchors = layout(radii)
            base = factor_action(reference, 0.18, radii)
            new_anchors = old_anchors + 0.2 * spacing
            anchor_link, unused_count = transport(reference, numerical.full_like(old_anchors, 0.18), old_anchors, new_anchors)
            endpoints, unused_count = transport(reference, anchor_link[0][factor_index], new_anchors[factor_index], radii[node_index])
            scalar, velocity, density = reference.matter(endpoints[0], radii[node_index])
            factor_scalar = numerical.bincount(factor_index, weights=factors[factor_index, node_index] * scalar, minlength=factors.shape[0])
            factor_density = numerical.bincount(factor_index, weights=sampling[factor_index, node_index] * density * endpoints[1], minlength=factors.shape[0])
            new_value = factor_density * factor_scalar**2 / (2 * spacing)
            verify(case_name + '_anchor_link_composition_on_same_events', maximum(endpoints[0] - base['transport'][0]) < 2e-10 and maximum(endpoints[1] * anchor_link[1][factor_index] - base['transport'][1]) < 2e-10)
            error = maximum(anchor_link[1] * new_value - base['value'])
            verify(case_name + '_reanchoring_preserves_action_density_with_Jacobian', error < 2e-7 * maximum(base['value']) + 1e-20, {'relative_error': error / maximum(base['value'])})
            scalar, velocity, coefficient = reference.matter(numerical.full_like(radii, 0.18), radii)
            old_value = float(numerical.sum((sampling @ coefficient) * (factors @ scalar)**2) / (2 * spacing))
            transported_value = float(base['value'].sum())
            verify(case_name + '_new_finite_background_not_relabelled_as_old_germ', old_value > 0 and transported_value > 0 and abs(transported_value - old_value) > 1e-10 * max(old_value, transported_value))
            report['samples'].append({'case': case_name, 'time': 0.18, 'intervals': 128, 'old_equal_coordinate_time_Gram_density': old_value, 'full_horizontal_transport_Gram_density': transported_value, 'ratio': transported_value / old_value, 'same_semidiscrete_operator': False, 'old_Hessian_or_evolution_pass_inherited': False})
            save()

        errors = []
        for intervals in [32, 64, 128]:
            radii = numerical.linspace(4, 8, intervals + 1)
            faces, unused_weights, projection, unused_shift, unused_incidence = mixed_basis(radii)
            first, second = numerical.sin(faces), numerical.cos(1.2 * faces)
            defect = projection @ (first * second) - (projection @ first) * (projection @ second)
            bound = 1.2 * numerical.max(numerical.diff(faces))**2 / 4
            verify('N' + str(intervals) + '_Lipschitz_product_commutator_bound', maximum(defect) <= bound + 2e-15, {'max_defect': maximum(defect), 'analytic_bound': float(bound)})
            errors.append(maximum(defect))
        ratios = [errors[index] / errors[index + 1] for index in range(2)]
        verify('fixed_basis_defect_is_second_order_in_this_control', min(ratios) > 3, {'errors': errors, 'ratios': ratios, 'uniform_parent_constraint_estimate': False})
        report['basis_defect'] = {'formula': 'I(fg)-(If)(Ig)=theta(1-theta)(f_R-f_L)(g_R-g_L)', 'bound': 'abs(defect)<=element_length^2*Lip(f)*Lip(g)/4', 'interpretation': 'Exact finite-grid diffeomorphism closure is not required for continuum viability. A convergent, stable constraint estimate with matched boundary/source controls is still required; this scalar product estimate alone does not supply it.'}
        verify('no_bytecode_cache', not (root / 'scripts/__pycache__').exists())
        verify('all_owned_sources_unchanged', all(hashlib.sha256((root / name).read_bytes()).hexdigest() == digest for name, digest in report['inputs'].items()))
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
