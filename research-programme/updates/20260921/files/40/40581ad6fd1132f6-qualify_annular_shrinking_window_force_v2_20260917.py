from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_full_characteristic_field_20260917 import FullCharacteristicField
from annular_locally_refined_source_action_20260916 import LocallyRefinedSourceAction
from annular_flat_preassembled_flow_20260916 import FlatPreassembledFlow, band_product
from annular_characteristic_galerkin_defect_20260917 import nodal_reference, canonical_defect, mass_dual_norm
from annular_matrix_free_adjoint_20260917 import MatrixFreeAdjoint
from derive_annular_characteristic_source_20260917 import force
from run_annular_source_fitted_crossing_20260915 import initial
from scipy.linalg import solve_banded
from fractions import Fraction
import argparse
import numpy as np
import sympy as sp


def energy_dual_norm(covector, matrices, count):
    field, position = covector[:count], covector[count]
    momentum, source = covector[count+1:-1], covector[-1]
    square = field @ solve_banded((2, 2), matrices['bulk'], field, check_finite=False)+position**2
    square += momentum @ band_product(matrices['mass'], momentum)+source**2
    return float(np.sqrt(max(0., square)))


def canonical_poisson_ratio(covector, matrices, count):
    field, position = covector[:count], covector[count]
    momentum, source = covector[count+1:-1], covector[-1]
    image_square = momentum @ band_product(matrices['bulk'], momentum)+source**2
    image_square += field @ solve_banded((2, 2), matrices['mass'], field, check_finite=False)+position**2
    return float(np.sqrt(image_square)/energy_dual_norm(covector, matrices, count))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--label', required=True)
    options = parser.parse_args()
    evidence = EvidenceRun(options.label, __file__)
    try:
        evidence.report.update(original_action_unchanged=True, finite_future_trajectories_read=False,
            no_nonlinear_finite_trajectory_rerun=True, old_peak_force_gates_unchanged=True,
            full_fixed_time_force_convergence_proven=False, internal_shrinking_window_derivation=True,
            independently_reviewed_proof=False, useful_h0_certified=False, source_field_momentum_retained=True,
            Gram_removed=False, force_fit=False, numeric_checks_not_uniform_bound=True,
            supersedes_symbolic_domain_comparison_failure='annular-shrinking-window-force-attempt01')
        coordinate = sp.symbols('coordinate', real=True)
        basis = [1-3*coordinate+2*coordinate**2, 4*coordinate-4*coordinate**2, -coordinate+2*coordinate**2]
        local_mass = sp.Matrix([[sp.integrate(left*right, (coordinate, 0, 1)) for right in basis] for left in basis])
        local_stiffness = sp.Matrix([[sp.integrate(sp.diff(left, coordinate)*sp.diff(right, coordinate), (coordinate, 0, 1))
            for right in basis] for left in basis])
        eigenvalue = sp.symbols('eigenvalue')
        characteristic = sp.Poly((local_stiffness-eigenvalue*local_mass).det(), eigenvalue)
        expected = sp.Poly(eigenvalue*(eigenvalue-12)*(eigenvalue-60), eigenvalue)
        evidence.check('exact_P2_inverse_eigenvalues', sp.expand(characteristic.monic().as_expr()-expected.as_expr()) == 0)
        matrix = 60*local_mass-local_stiffness
        from itertools import combinations
        minors = [matrix.extract(indices, indices).det() for size in [1, 2, 3] for indices in combinations(range(3), size)]
        evidence.check('exact_P2_inverse_PSD_all_principal_minors', all(value >= 0 for value in minors))
        phases = []
        for exponent in range(5, 13):
            spacing = Fraction(8, 5*2**exponent)
            phase = (Fraction(603, 100)-Fraction(26, 5))/spacing
            phase -= phase.numerator//phase.denominator
            phases.append(str(phase))
            evidence.check('dyadic_phase_'+str(exponent), min(phase, 1-phase)/8 >= Fraction(1, 40))
        poisson_constant = 40*np.sqrt(60)*17/13
        evidence.report.update(exact_local_generalized_eigenvalues=[0, 12, 60], exact_source_phase_cycle=phases,
            fixed_geometry_poisson_numerator=poisson_constant, fixed_geometry_poisson_bound='40 sqrt(60) (17/13) / h',
            phase_argument='2^k is nonzero modulo5; every dyadic phase is in{1/5,2/5,3/5,4/5}; eight splits give min width h/40.')
        reference = FullCharacteristicField(tight=True)
        generator = np.random.default_rng(202609172003)
        for base_count in [33, 65, 129, 257, 513, 1025, 2049]:
            for gram in [False, True]:
                branch = 'MTS' if gram else 'reference'
                system = LocallyRefinedSourceAction(base_count, gram, background_mass=0., source_splits=8)
                model = FlatPreassembledFlow(system)
                adjoint = MatrixFreeAdjoint(model)
                fixed_matrices = model.matrices(system.anchor)
                key = branch+str(base_count)
                spacing = system.gram_spacing
                seed, unused = nodal_reference(system, reference, 0.)
                evidence.check(key+'_same_initial_data', max(abs(seed-initial(system))) < 2e-12)
                evidence.check(key+'_phase_minimum_cell', min(np.diff(system.edges))/spacing >= 1/40-3e-11)
                ratios = []
                for unused in range(3):
                    covector = generator.normal(size=2*system.count+2)
                    ratios.append(canonical_poisson_ratio(covector, fixed_matrices, system.count))
                evidence.check(key+'_Poisson_inverse_bound_probe', max(ratios) <= poisson_constant/spacing)
                probes = []
                for tau in [0., .25, 1., 4., 6.4]:
                    instant = spacing*tau
                    state, derivative = nodal_reference(system, reference, instant)
                    defect, gram_defect, matrices, unused = canonical_defect(model, state, derivative)
                    context = adjoint.context(state)
                    inertia, schur, cross = context['inertia'], context['value']['schur'], context['cross']
                    inverse_residual = solve_banded((2, 2), matrices['mass'], defect[:-1], check_finite=False)
                    projection = inertia/schur*(defect[-1]-cross @ inverse_residual)
                    actual_difference = float(context['value']['force']-force(instant, reference.source.sol(instant)))
                    scale = max(1., abs(actual_difference))
                    identity_error = float(abs(projection-actual_difference))
                    evidence.check(key+str(tau)+'_exact_material_defect_projection', identity_error < 2e-12*scale, identity_error)
                    momentum_gradient_v = np.zeros_like(state)
                    momentum_gradient_v[-2] = inertia
                    momentum_gradient = adjoint.canonical_covector(state, momentum_gradient_v, context)
                    dual_projection = momentum_gradient[system.count+1:] @ defect
                    evidence.check(key+str(tau)+'_canonical_momentum_projection', abs(dual_projection-projection) < 2e-12)
                    cross_norm = np.sqrt(max(0., cross @ context['inverse_cross']))
                    field_square = float(state[:system.count] @ band_product(matrices['square'], state[:system.count]))
                    evidence.check(key+str(tau)+'_positive_Schur_and_cross_bound',
                        schur >= inertia-2e-14 and cross_norm**2 <= field_square+2e-14)
                    projected_bound = float(inertia/schur*(abs(defect[-1])+cross_norm*np.sqrt(max(0., defect[:-1] @ inverse_residual))))
                    evidence.check(key+str(tau)+'_projected_residual_bound', abs(actual_difference) <= projected_bound+2e-12)
                    force_gradient = adjoint.canonical_covector(state, adjoint.force_gradient(state, context), context)
                    force_dual = energy_dual_norm(force_gradient, fixed_matrices, system.count)
                    momentum_dual = energy_dual_norm(momentum_gradient, fixed_matrices, system.count)
                    probes.append(dict(tau=tau, time=float(instant), reference_force_consistency_error=actual_difference,
                        material_defect_projection=float(projection), projection_identity_error=identity_error,
                        projected_residual_bound=projected_bound, total_defect_norm=mass_dual_norm(defect, matrices),
                        Gram_defect_norm=mass_dual_norm(gram_defect, matrices),
                        force_energy_dual_sensitivity=force_dual, h_times_force_sensitivity=spacing*force_dual,
                        momentum_energy_dual_sensitivity=momentum_dual, material_Schur_fraction=float(inertia/schur)))
                row = dict(branch=branch, base_count=base_count, h=spacing, maximum_sampled_Poisson_ratio=max(ratios),
                    maximum_force_consistency_error=max(abs(point['reference_force_consistency_error']) for point in probes),
                    maximum_h_force_sensitivity=max(point['h_times_force_sensitivity'] for point in probes),
                    maximum_momentum_sensitivity=max(point['momentum_energy_dual_sensitivity'] for point in probes), probes=probes)
                evidence.report['cases'].append(row)
                evidence.save()
                print({name: value for name, value in row.items() if name != 'probes'}, flush=True)
        for filename in ['DERIVATION-20260917-coupled-Galerkin-defect-and-flat-nonlinear-limit.md',
                'DERIVATION-20260917-initial-corner-response-and-frozen-action-prediction.md']:
            evidence.own(evidence.root/filename)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
