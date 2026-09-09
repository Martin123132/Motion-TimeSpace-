import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from navier_stokes_source_audit_20260908 import limit_process


def run():
    limit_process()
    import numpy as numerical
    import sympy as symbolic
    from annular_adm_mixed_action_20260909 import MixedActionBasis, coefficient_jets, real_linear
    from annular_adm_clock_quadratic_20260909 import FactorLinks
    from annular_constraint_routhian_20260909 import ConstraintRouthian
    from annular_metric_time_links_20260909 import MetricLinkRouthian, MetricLinkWardIdentity, metric_link_matrix, finite_metric_link_potential

    root = Path(__file__).resolve().parents[1]
    intake = root / 'source-intake/navier-stokes/20260909'
    source = intake / 'annular-constraint-routhian-derived'
    destination = intake / 'annular-metric-time-links-derived'
    destination.mkdir(exist_ok=False)
    report = {'state': 'running', 'started_utc': datetime.now(timezone.utc).isoformat(), 'inputs': {}, 'outputs': {}, 'checks': [], 'samples': [], 'valid_for_physics_claim': False, 'scope': 'Explicit alternative finite action: compute the time connection from the reconstructed ADM metric BEFORE integrating links, rather than interpolating nodal samples of that connection. Derive and test its first shift variation, recompute the constraint tangent, and compare both candidates with unchanged GR and initial data. No fitted compensating source; no automatic inheritance of full quadratic/Dirac or evolution stability claims.'}
    (destination / 'executed-script.py').write_bytes(Path(__file__).read_bytes())

    def save():
        (destination / 'status.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')

    def own(path):
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        report['inputs'][str(path.relative_to(root))] = digest
        return digest

    def verify(name, passed, detail=None):
        report['checks'].append({'name': name, 'passed': bool(passed), 'detail': detail})
        save()
        print(name + ': ' + str(bool(passed)), flush=True)

    def maximum(value):
        return float(numerical.max(numerical.abs(value)))

    save()
    try:
        prior_path = intake / 'annular-local-Ward-identity-derived-validated/status.json'
        own(prior_path)
        prior = json.loads(prior_path.read_text())
        verify('full_Ward_derivation_complete', prior['state'] == 'complete' and prior['passed'] == prior['total'])
        verify('all_Ward_sources_and_residuals_unchanged', all(own(root / name) == digest for name, digest in {**prior['inputs'], **prior['outputs']}.items()))
        for name in ['annular_metric_time_links_20260909.py', 'derive_annular_metric_time_links_20260909.py']:
            path = root / 'scripts' / name
            own(path)
            compile(path.read_bytes(), str(path), 'exec')
        for case_name in ['canonical', 'nonlinear_modulated']:
            case = json.loads((intake / 'annular-constraint-correction-initial' / (case_name + '.json')).read_text())
            constants = {name: float(symbolic.sympify(value)) for name, value in case['parameters'].items()}
            kappa = float(symbolic.sympify(case['normalization_kappa']))
            for intervals in [16, 32, 64]:
                tag = case_name + '_N' + str(intervals)
                report['active_job'] = tag
                save()
                with numerical.load(source / (tag + '_Gram.npz')) as loaded:
                    old = {name: loaded[name].copy() for name in loaded.files}
                basis = MixedActionBasis(old['radius'])
                system = MetricLinkRouthian(basis, old['scalar'], old['defect'], old['defect_time'], constants, kappa, old['momentum'], old['outer_clock'][0])
                legacy = ConstraintRouthian(basis, old['scalar'], old['defect'], old['defect_time'], constants, kappa, old['momentum'], old['outer_clock'][0])
                new_static = system.evaluate(old['corrected'], True)
                old_static = legacy.evaluate(old['corrected'], True)
                verify(tag + '_initial_action_gradient_and_Hessian_unchanged_at_zero_shift', all(numerical.array_equal(first, second) for first, second in zip(new_static, old_static)))
                verify(tag + '_GR_control_completely_unchanged', all(numerical.array_equal(first, second) for first, second in zip(system.shift_mass_velocity(old['corrected'], False), legacy.shift_mass_velocity(old['corrected'], False))))
                matrix4, matrix8 = metric_link_matrix(system, old['corrected'], order=4), metric_link_matrix(system, old['corrected'], order=8)
                verify(tag + '_metric_link_integral_quadrature_control', maximum(matrix4 - matrix8) < 1e-13, {'maximum_difference': maximum(matrix4 - matrix8)})
                tangent = system.constraint_tangent(old['corrected'], True, old['defect_acceleration'], old['endpoint_acceleration'], old['outer_clock'][1])
                updated = {name: value.copy() for name, value in old.items()}
                updated.update(tangent)
                identity = MetricLinkWardIdentity(system, updated)
                ward = identity.evaluate(True)
                verify(tag + '_new_shift_current_solved_without_projection', maximum(tangent['pairing'] @ tangent['shift_mass_speed'] + tangent['matter_shift'] - tangent['Gram_shift']) < 1e-14)
                verify(tag + '_new_constraint_tangent_satisfies_all_free_derivative_rows', maximum(tangent['constraint_derivative_residual']) < 1e-11)
                verify(tag + '_new_link_action_full_Ward_identity', maximum(ward['identity_error']) < 2e-11)
                verify(tag + '_direct_metric_connection_is_not_old_nodal_interpolation', maximum(matrix8 - super(MetricLinkWardIdentity, identity).connection_transport()) > 1e-6)
                if intervals == 16:
                    links = FactorLinks(basis.radii)
                    probe = 0.02 * numerical.sin(23 * basis.faces)

                    def boundary(time):
                        state = identity.state(time)
                        node_mass = real_linear(basis.face_to_node, state['packed'][system.slices[0]])
                        coefficient = coefficient_jets(state['scalar_time'], state['gradient_node'], node_mass, state['packed'][system.slices[1]], basis.radii, constants)[0]
                        factor_scalar = links.collect(links.tweight * state['scalar'][links.node])
                        displacement = real_linear(metric_link_matrix(system, state['packed']), probe)
                        return numerical.dot(factor_scalar**2 / (2 * basis.spacing), links.collect(links.sweight * coefficient[links.node] * displacement))

                    boundary_rate = boundary(1j * 1e-25).imag / 1e-25
                    reduced = numerical.dot(tangent['Gram_shift'], probe)
                    for amplitude in [0.001, 0.0005]:
                        raw = (finite_metric_link_potential(system, updated, probe, amplitude) - finite_metric_link_potential(system, updated, probe, -amplitude)) / (2 * amplitude)
                        error = abs(raw - boundary_rate - reduced)
                        verify(tag + '_independent_nonlinear_metric_flow_action_variation_' + str(amplitude), error < 2e-4 * max(abs(raw), abs(boundary_rate), abs(reduced), 1e-25) + 1e-15, {'raw': float(raw), 'time_boundary': float(boundary_rate), 'reduced': float(reduced), 'error': float(error)})
                old_error = maximum(old['packed_speed'][system.slices[0]] - old['shift_mass_speed'])
                new_error = maximum(tangent['packed_speed'][system.slices[0]] - tangent['shift_mass_speed'])
                with numerical.load(source / (tag + '_GR.npz')) as control:
                    gr_error = maximum(control['packed_speed'][system.slices[0]] - control['shift_mass_speed'])
                report['samples'].append({'case': case_name, 'intervals': intervals, 'GR_mass_rate_mismatch_max': gr_error, 'old_Gram_mass_rate_mismatch_max': old_error, 'metric_link_mass_rate_mismatch_max': new_error, 'metric_link_to_old_error_ratio': new_error / old_error, 'metric_link_to_GR_error_ratio': new_error / gr_error, 'new_shift_weak_residual_max': maximum(tangent['shift_residual']), 'new_Ward_identity_error': maximum(ward['identity_error']), 'new_Gram_link_remainder_max': maximum(ward['Gram_link_remainder']), 'all_shift_rows_closed': maximum(tangent['shift_residual']) < 1e-10, 'physical_candidate_promoted': False})
                artifact = destination / (tag + '.npz')
                numerical.savez_compressed(artifact, radius=basis.radii, faces=basis.faces, metric_link_matrix=matrix8, **tangent, **{'Ward_' + name: value for name, value in ward.items()})
                report['outputs'][str(artifact.relative_to(root))] = hashlib.sha256(artifact.read_bytes()).hexdigest()
                save()
        verify('all_owned_inputs_unchanged', all(hashlib.sha256((root / name).read_bytes()).hexdigest() == digest for name, digest in report['inputs'].items()))
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
