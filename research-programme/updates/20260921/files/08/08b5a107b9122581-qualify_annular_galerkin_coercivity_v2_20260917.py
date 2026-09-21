from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_full_characteristic_field_20260917 import FullCharacteristicField
from annular_locally_refined_source_action_20260916 import LocallyRefinedSourceAction
from annular_flat_preassembled_flow_20260916 import FlatPreassembledFlow
from annular_characteristic_galerkin_defect_20260917 import nodal_reference, canonical_defect, mass_dual_norm
from annular_canonical_energy_20260917 import CanonicalEnergy, dense_bands
from run_annular_source_fitted_crossing_20260915 import initial
from scipy.linalg import eigh, solve_banded, solve
from fractions import Fraction
import argparse
import json
import numpy as np
import sympy as sp


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--label', required=True)
    options = parser.parse_args()
    evidence = EvidenceRun(options.label, __file__)
    try:
        evidence.report.update(original_action_unchanged=True, finite_future_trajectories_read=False,
            no_forward_trajectory_rerun=True, numerical_positivity_not_uniform_neighborhood_certificate=True,
            auxiliary_beta_not_an_action_term=True, full_parent_GR_limit_proven=False,
            instantaneous_force_convergence_proven=False, h0_numerically_certified=False,
            supersedes_failed_strict_sampling_check='annular-galerkin-coercivity-attempt01',
            stored_zero_sampling_entries_are_allowed=True)
        intake = evidence.root/'source-intake/navier-stokes/20260914'
        path = intake/'annular-coupled-galerkin-defect-attempt01/status.json'
        evidence.own(path)
        previous = json.loads(path.read_text())
        evidence.check('independent_residual_qualification_complete', previous['state'] == 'complete'
            and all(row['passed'] for row in previous['checks']))
        coordinate = sp.symbols('coordinate', real=True)
        basis = [(1-coordinate)*(1-2*coordinate), 4*coordinate*(1-coordinate), coordinate*(2*coordinate-1)]
        evidence.check('P2_reproduces_quadratics', all(sp.expand(sum(value*sp.Rational(index, 2)**power
            for index, value in enumerate(basis))-coordinate**power) == 0 for power in [0, 1, 2]))
        inverse_roots = [sp.diff(value, coordinate) for value in basis]
        evidence.check('P2_derivative_bound_by_endpoints', max(sum(abs(value.subs(coordinate, point)) for value in inverse_roots)
            for point in [0, 1]) == 8)
        evidence.check('dyadic_phase_cycle', {(Fraction(83*2**exponent, 160) % 1) for exponent in range(5, 13)}
            == {Fraction(index, 5) for index in [1, 2, 3, 4]})
        polynomial = sum(value*coefficient for value, coefficient in zip(basis, sp.symbols('a0 a1 a2')))
        coefficients = sp.symbols('a0 a1 a2')
        mass_exact = sp.hessian(sp.integrate(polynomial**2/2, (coordinate, 0, 1)), coefficients)
        stiffness_exact = sp.hessian(sp.integrate(sp.diff(polynomial, coordinate)**2/2, (coordinate, 0, 1)), coefficients)
        evidence.check('P2_inverse_constant_60', (60*mass_exact-stiffness_exact).is_positive_semidefinite)
        reference = FullCharacteristicField(tight=True)
        random = np.random.default_rng(9172026)
        for base_count in [33, 65, 129]:
            for gram in [False, True]:
                branch = 'MTS' if gram else 'reference'
                system = LocallyRefinedSourceAction(base_count, gram, background_mass=0., source_splits=8)
                model = FlatPreassembledFlow(system)
                energy = CanonicalEnergy(model)
                initial_state, unused = nodal_reference(system, reference, 0.)
                evidence.check(branch+str(base_count)+'_same_original_initial_data', np.max(abs(initial_state-initial(system))) < 2e-12)
                evidence.check(branch+str(base_count)+'_mesh_ratio_lower_bound', min(np.diff(system.edges))/system.gram_spacing > 1/40-2e-12)
                if gram:
                    evidence.check(branch+str(base_count)+'_nonnegative_partition_Gram_sampling', np.min(system.sampling.data) >= 0.
                        and np.max(abs(np.asarray(system.sampling.sum(axis=1)).ravel()-1.)) < 2e-14,
                        dict(minimum=float(np.min(system.sampling.data)), explicit_zeros=int(np.sum(system.sampling.data == 0.))))
                for instant in [0., .173, .4]:
                    state, derivative = nodal_reference(system, reference, instant)
                    data = energy.evaluate(state)
                    matrices = model.matrices(state[system.count])
                    bulk = dense_bands(matrices['bulk'])
                    square = dense_bands(matrices['square'])
                    actual_gram = (model.lifted_transpose @ model.lifted.multiply(matrices['gram'][:, None])).toarray()
                    field_schur = bulk+actual_gram-state[-2]**2*square
                    count = system.count
                    mass_inverse = solve_banded((2, 2), matrices['mass'], np.eye(count), check_finite=False)
                    metric = np.zeros((2*count+2, 2*count+2))
                    metric[:count, :count] = bulk
                    metric[count, count] = 1.
                    metric[count+1:2*count+1, count+1:2*count+1] = mass_inverse
                    metric[-1, -1] = 1.
                    retained = np.delete(np.arange(len(metric)), count)
                    fixed = data['hessian'][np.ix_(retained, retained)]
                    fixed_metric = metric[np.ix_(retained, retained)]
                    lowest = float(eigh(fixed, fixed_metric, eigvals_only=True, subset_by_index=[0, 0])[0])
                    wave_lower = float(eigh(field_schur, bulk, eigvals_only=True, subset_by_index=[0, 0])[0])
                    cross = data['hessian'][retained, count]
                    critical_beta = float(cross @ solve(fixed, cross, assume_a='pos')-data['hessian'][count, count])
                    beta = max(1., critical_beta+1.)
                    shifted = data['hessian'].copy()
                    shifted[count, count] += beta
                    shifted_lower = float(eigh(shifted, metric, eigvals_only=True, subset_by_index=[0, 0])[0])
                    trials = []
                    for unused in range(3):
                        variation = random.normal(size=2*count+2)
                        variation[count] = 0.
                        position_variation = variation[:count]
                        momentum_variation = variation[count+1:]
                        shifted_momentum = momentum_variation-data['mixed'][:, :count] @ position_variation
                        completed = position_variation @ field_schur @ position_variation
                        completed += shifted_momentum @ data['kinetic_inverse'] @ shifted_momentum
                        direct = variation @ data['hessian'] @ variation
                        trials.append(abs(completed-direct)/max(1., abs(direct)))
                    pushed = energy.lagrangian(state.astype(complex)+1e-25j*derivative)
                    residual = data['gradient']-pushed['momentum'].imag/1e-25
                    flow_residual, unused, unused2, unused3 = canonical_defect(model, state, derivative)
                    momentum_identity = mass_dual_norm(residual-flow_residual, matrices)
                    prefix = branch+str(base_count)+'_'+str(instant)
                    evidence.check(prefix+'_fixed_b_square_completion', max(trials) < 2e-12, float(max(trials)))
                    evidence.check(prefix+'_timelike_wave_coercivity', wave_lower >= 1-state[-2]**2-2e-9, wave_lower)
                    evidence.check(prefix+'_fixed_b_positive_generalized_margin', lowest > 1e-5, lowest)
                    evidence.check(prefix+'_source_shift_positive_sample', shifted_lower > 1e-5, shifted_lower)
                    evidence.check(prefix+'_independent_canonical_momentum_time_derivative', momentum_identity < 2e-8, momentum_identity)
                    evidence.report['cases'].append(dict(branch=branch, base_count=base_count, time=instant,
                        fixed_b_generalized_lower=lowest, source_schur_critical_beta=critical_beta,
                        demonstrated_sample_beta=beta, shifted_generalized_lower=shifted_lower,
                        timelike_wave_lower=wave_lower, momentum_identity_error=momentum_identity,
                        sampled_beta_not_a_uniform_neighborhood_certificate=True))
                    evidence.save()
                print(dict(branch=branch, base_count=base_count, state='qualified'), flush=True)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
