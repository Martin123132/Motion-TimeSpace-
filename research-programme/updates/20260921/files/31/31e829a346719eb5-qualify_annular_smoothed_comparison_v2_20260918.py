from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_smoothed_comparison_20260918 import (canonical_state, canonical_flow, inverse_legendre,
    energy_norm, comparison_diagnostics, comparison_corrector, averaged_path)
from annular_full_characteristic_field_20260917 import FullCharacteristicField
from annular_locally_refined_source_action_20260916 import LocallyRefinedSourceAction
from annular_flat_preassembled_flow_20260916 import FlatPreassembledFlow
from annular_characteristic_galerkin_defect_20260917 import nodal_reference
import argparse
import numpy as np
import sympy as sp


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--label', required=True)
    parser.add_argument('--grids', nargs='+', type=int, default=[129, 257, 513, 1025])
    options = parser.parse_args()
    evidence = EvidenceRun(options.label, __file__)
    try:
        evidence.report.update(original_action_unchanged=True, original_initial_data_unchanged=True,
            comparison_path_only=True, finite_future_trajectories_read=False,
            no_nonlinear_finite_trajectory_rerun=True, old_peak_force_gates_unchanged=True,
            all_Gram_rows_retained=True, source_field_momentum_retained=True,
            uniform_bounds_not_inferred_from_samples=True, useful_h0_certified=False,
            independently_reviewed_proof=False, time_integration_error_certified=False,
            supersedes_support_count_checker_failure='annular-smoothed-comparison-attempt01')
        beta = sp.Rational(4, 5)
        rate = min(beta, 1-beta/2, 2*beta-1)
        evidence.check('balanced_nonlinear_smoothing_exponents', rate == sp.Rational(3, 5))
        evidence.check('force_exponents_positive', rate-sp.Rational(1, 2) == sp.Rational(1, 10)
            and 2*rate-1 == sp.Rational(1, 5))
        horizon, epsilon, instant = sp.symbols('horizon epsilon instant', positive=True)
        center = epsilon+(1-2*epsilon/horizon)*instant
        evidence.check('inward_average_endpoint_windows', sp.simplify(center.subs(instant, 0)-epsilon/2) == epsilon/2
            and sp.simplify(center.subs(instant, horizon)+epsilon/2) == horizon-epsilon/2)
        evidence.report['derived_exponents'] = dict(epsilon='4/5', accumulated_energy='3/5',
            linear_force='1/10', nonlinear_force='1/5', stationary_corrector='3/2')
        for phase in [sp.Rational(1, 5), sp.Rational(2, 5), sp.Rational(3, 5), sp.Rational(4, 5)]:
            raw_support = []
            for start in range(-5, 6):
                value = sum(coefficient*max(sp.Rational(start+offset)-phase, 0)**2/2
                    for offset, coefficient in enumerate([-1, 3, -3, 1]))
                if value != 0:
                    raw_support.append(start)
            adjacent_support = set(raw_support) | {start-1 for start in raw_support}
            evidence.check('exact_stationary_support_phase_'+str(phase), len(raw_support) == 3 and len(adjacent_support) == 4)
        reference = FullCharacteristicField(tight=True)
        for base_count in options.grids:
            for gram in [False, True]:
                branch = 'MTS' if gram else 'reference'
                system = LocallyRefinedSourceAction(base_count, gram, background_mass=0., source_splits=8)
                model = FlatPreassembledFlow(system)
                spacing = system.gram_spacing
                width = spacing**.8
                key = branch+str(base_count)
                hinge = np.maximum(system.radii-system.anchor, 0.)
                kink = hinge**2/2
                evidence.check(key+'_hinge_annihilation', np.max(abs(model.lifted @ hinge), initial=0.) < 2e-12)
                evidence.check(key+'_quadratic_kink_zero_first_jump', abs(system.jump @ kink) < 2e-12)
                global_quadratic = (system.radii-system.anchor)**2/2
                evidence.check(key+'_global_quadratic_annihilation', np.max(abs(model.lifted @ global_quadratic), initial=0.) < 2e-12)
                factor = model.lifted @ kink
                evidence.check(key+'_stationary_kink_local_support', np.count_nonzero(abs(factor) > 2e-12) <= 7)
                probes = []
                for time in [0., .071, .195, .21, .4]:
                    ordinary, ordinary_arrays = comparison_diagnostics(model, reference, time, width, 6)
                    tight, tight_arrays = comparison_diagnostics(model, reference, time, width, 10)
                    prefix = key+'_'+str(time)
                    differences = {name: energy_norm(model, tight_arrays[name]-ordinary_arrays[name]) for name in tight_arrays}
                    evidence.check(prefix+'_quadrature_control', max(differences.values()) < 2e-8, differences)
                    evidence.check(prefix+'_normalized_inside_original_horizon', abs(tight['total_weight']-1) < 2e-11
                        and 0 < tight['window_lower'] < tight['window_upper'] < .4)
                    evidence.check(prefix+'_exact_corrector_linear_cancellation', tight['linear_identity_error'] < 2e-10
                        and tight['elliptic_relative_residual'] < 2e-9, tight['linear_identity_error'])
                    evidence.check(prefix+'_nonlinear_defect_decomposition', tight['decomposition_error'] < 2e-10)
                    state = inverse_legendre(model, tight_arrays['canonical'])
                    evidence.check(prefix+'_inverse_kinetic_map', energy_norm(model,
                        canonical_state(model, state)-tight_arrays['canonical']) < 2e-10)
                    nonlinear_flow = model.evaluate(state)['flow']
                    pushed = canonical_state(model, state.astype(complex)+1e-25j*nonlinear_flow).imag/1e-25
                    evidence.check(prefix+'_independent_canonical_flow', energy_norm(model, pushed-canonical_flow(model, state)) < 2e-9)
                    compression = 1-2*width/.4
                    lower_state, unused = nodal_reference(system, reference, tight['window_lower'])
                    upper_state, unused = nodal_reference(system, reference, tight['window_upper'])
                    boundary_rate = compression/width*(canonical_state(model, upper_state)-canonical_state(model, lower_state))
                    boundary_error = energy_norm(model, boundary_rate-tight_arrays['derivative'])
                    evidence.check(prefix+'_averaged_path_derivative_boundary_identity', boundary_error < 2e-8, boundary_error)
                    tight.update(quadrature_control=differences, averaged_derivative_boundary_error=boundary_error,
                        scaled_corrector=tight['correction_norm']/spacing**1.5,
                        scaled_corrector_rate=tight['correction_rate_norm']/spacing**1.5,
                        scaled_regular_residual=tight['regular_residual_norm']/(spacing/np.sqrt(width)+width*np.sqrt(spacing)+spacing),
                        scaled_commutator=tight['commutator_norm']*spacing/width**2)
                    if time == .21:
                        data = averaged_path(model, reference, time, width, 10)
                        step = 1e-5
                        corrections = []
                        for sign in [-1., 1.]:
                            moved = comparison_corrector(model, data['canonical']+sign*step*data['derivative'], data['derivative'],
                                data['stationary']+sign*step*data['stationary_rate'], data['stationary_rate'])
                            corrections.append(moved['correction'])
                        numeric_rate = (corrections[1]-corrections[0])/(2*step)
                        rate_error = energy_norm(model, numeric_rate-tight_arrays['correction_rate'])
                        evidence.check(prefix+'_independent_corrector_time_derivative',
                            rate_error < 2e-11+2e-8*energy_norm(model, tight_arrays['correction_rate']), rate_error)
                        tight['corrector_time_derivative_error'] = rate_error
                    probes.append(tight)
                    evidence.save()
                row = dict(branch=branch, base_count=base_count, h=spacing, epsilon=width, probes=probes,
                    max_corrected_residual=max(point['corrected_residual_norm'] for point in probes),
                    max_scaled_corrected_residual=max(point['corrected_residual_ratio'] for point in probes),
                    max_scaled_corrector=max(point['scaled_corrector'] for point in probes),
                    max_scaled_corrector_rate=max(point['scaled_corrector_rate'] for point in probes),
                    max_scaled_regular_residual=max(point['scaled_regular_residual'] for point in probes),
                    max_scaled_commutator=max(point['scaled_commutator'] for point in probes))
                evidence.report['cases'].append(row)
                evidence.save()
                print({name: value for name, value in row.items() if name != 'probes'}, flush=True)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()


