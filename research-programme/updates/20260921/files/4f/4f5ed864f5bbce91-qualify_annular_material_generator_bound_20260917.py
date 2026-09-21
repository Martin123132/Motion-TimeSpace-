from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_full_characteristic_field_20260917 import FullCharacteristicField
from annular_locally_refined_source_action_20260916 import LocallyRefinedSourceAction
from annular_flat_preassembled_flow_20260916 import FlatPreassembledFlow, band_product
from annular_characteristic_galerkin_defect_20260917 import nodal_reference, canonical_defect
from annular_matrix_free_adjoint_20260917 import MatrixFreeAdjoint
from annular_instantaneous_force_bridge_20260917 import canonical_momentum
from scipy.linalg import solve_banded
import argparse
import numpy as np
import sympy as sp


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--label', required=True)
    options = parser.parse_args()
    evidence = EvidenceRun(options.label, __file__)
    try:
        evidence.report.update(original_action_unchanged=True, finite_future_trajectories_read=False,
            no_nonlinear_finite_trajectory_rerun=True, old_peak_force_gates_unchanged=True,
            uniform_bound_is_analytic_not_inferred_from_samples=True, useful_h0_certified=False,
            internal_initial_window_force_proof=True, full_fixed_time_force_convergence_proven=False,
            source_field_momentum_retained=True, all_Gram_rows_retained=True)
        endpoint_margin = sp.Rational(1, 30)-sp.Rational(1, 50)*sp.Rational(5, 16)
        midpoint_margin = sp.Rational(2, 5)-sp.Rational(1, 50)*sp.Rational(5, 6)
        endpoint_ratio = sp.Rational(51, 50)*sp.Rational(1, 4)/endpoint_margin
        midpoint_ratio = sp.Rational(51, 50)*sp.Rational(2, 3)/midpoint_margin
        evidence.check('weighted_P2_endpoint_dominance', endpoint_margin == sp.Rational(13, 480))
        evidence.check('weighted_P2_midpoint_dominance', midpoint_margin == sp.Rational(23, 60))
        evidence.check('nodal_projection_sup_bound_ten', max(endpoint_ratio, midpoint_ratio) < 10)
        coordinate = sp.symbols('coordinate', real=True)
        basis = [1-3*coordinate+2*coordinate**2, 4*coordinate-4*coordinate**2, -coordinate+2*coordinate**2]
        absolute_integrals = [sp.integrate(basis[0], (coordinate, 0, sp.Rational(1, 2)))
            -sp.integrate(basis[0], (coordinate, sp.Rational(1, 2), 1)),
            sp.integrate(basis[1], (coordinate, 0, 1))]
        evidence.check('P2_absolute_basis_integrals', absolute_integrals == [sp.Rational(1, 4), sp.Rational(2, 3)])
        left_lebesgue = basis[0]+basis[1]-basis[2]
        right_lebesgue = -basis[0]+basis[1]+basis[2]
        evidence.check('P2_Lebesgue_maximum', sp.simplify(left_lebesgue-sp.Rational(5, 4)+4*(coordinate-sp.Rational(1, 4))**2) == 0
            and sp.simplify(right_lebesgue-sp.Rational(5, 4)+4*(coordinate-sp.Rational(3, 4))**2) == 0)
        evidence.report['exact_projection_majorants'] = dict(relative_density_variation_maximum='1/50',
            endpoint_dominance=str(endpoint_margin), midpoint_dominance=str(midpoint_margin),
            endpoint_load_ratio=str(endpoint_ratio), midpoint_load_ratio=str(midpoint_ratio), nodal_bound=10, function_bound=12.5)
        reference = FullCharacteristicField(tight=True)
        for base_count in [33, 65, 129, 257, 513, 1025, 2049]:
            for gram in [False, True]:
                branch = 'MTS' if gram else 'reference'
                system = LocallyRefinedSourceAction(base_count, gram, background_mass=0., source_splits=8)
                model = FlatPreassembledFlow(system)
                adjoint = MatrixFreeAdjoint(model)
                fixed = model.matrices(system.anchor)
                spacing = system.gram_spacing
                times = sorted(set([0., .25*spacing, spacing, 4*spacing, 6.4*spacing, .071, .173, .21, .317, .4]))
                probes = []
                for instant in times:
                    state, derivative = nodal_reference(system, reference, instant)
                    context = adjoint.context(state)
                    matrices = context['matrices']
                    test = context['inverse_cross']
                    projection_H1 = np.sqrt(max(0., test @ band_product(fixed['bulk'], test)))
                    covector = np.zeros_like(state)
                    covector[-2] = context['inertia']
                    momentum_gradient = adjoint.canonical_covector(state, covector, context)
                    count = system.count
                    generator_square = momentum_gradient[count+1:-1] @ band_product(fixed['bulk'], momentum_gradient[count+1:-1])
                    generator_square += momentum_gradient[-1]**2+momentum_gradient[count]**2
                    generator_square += momentum_gradient[:count] @ solve_banded((2, 2), fixed['mass'], momentum_gradient[:count], check_finite=False)
                    residual, gram_residual, unused, unused2 = canonical_defect(model, state, derivative)
                    momentum_rate = canonical_momentum(model, state.astype(complex)+1e-25j*derivative).imag/1e-25
                    canonical_rate = momentum_rate+residual
                    flow_square = state[count+1:-2] @ band_product(fixed['bulk'], state[count+1:-2])+state[-2]**2
                    flow_square += canonical_rate[:-1] @ solve_banded((2, 2), fixed['mass'], canonical_rate[:-1], check_finite=False)+canonical_rate[-1]**2
                    factor = model.lifted @ state[:count]
                    test_factor = model.lifted @ test
                    nodal_values = np.where(system.element_indices >= 0, state[:count][system.element_indices], 0.)
                    element_derivatives = np.column_stack([nodal_values @ np.array([-3., 4., -1.]),
                        nodal_values @ np.array([1., -4., 3.])])/np.diff(system.edges)[:, None]
                    unused, jacobians, unused2 = system.mapping(system.reference_radius, state[count])
                    function_sup_majorant = float(np.max(abs(element_derivatives))/min(jacobians))
                    radii, unused, unused2 = system.mapping(system.edges, state[count])
                    eta = float(max((radii[1:]/radii[:-1])**2-1))
                    nodal_bound_pass = max(abs(test)) <= 10*function_sup_majorant+2e-12
                    key = branch+str(base_count)+'_'+str(instant)
                    evidence.check(key+'_conditional_projection_max_bound', eta > .02 or nodal_bound_pass,
                        dict(relative_weight_variation=eta, within_analytic_weight_gate=eta <= .02))
                    mass_rows = band_product(abs(matrices['mass']), np.ones(count))
                    dominance = 2*matrices['mass'][2]-mass_rows
                    evidence.check(key+'_conditional_mass_row_dominance', eta > .02 or min(dominance) > 0.)
                    gram_projection = float(-test_factor @ (matrices['gram']*factor))
                    evidence.check(key+'_Gram_projected_work_identity', abs(test @ gram_residual[:-1]-gram_projection) < 2e-12)
                    evidence.check(key+'_finite_reference_generator', generator_square > 0 and np.isfinite(generator_square+flow_square))
                    probes.append(dict(time=float(instant), sqrt_h_projection_H1=float(np.sqrt(spacing)*projection_H1),
                        sqrt_h_material_generator_norm=float(np.sqrt(spacing*generator_square)),
                        reference_canonical_flow_norm=float(np.sqrt(max(0., flow_square))),
                        Gram_factor_l1_over_h_squared=float(sum(abs(factor))/spacing**2),
                        projected_Gram_work_over_h=gram_projection/spacing,
                        maximum_test_factor=float(np.max(abs(test_factor), initial=0.)),
                        relative_weight_variation=eta, nodal_projection_sup=float(max(abs(test)))))
                row = dict(branch=branch, base_count=base_count, h=spacing,
                    max_sqrt_h_material_generator=max(point['sqrt_h_material_generator_norm'] for point in probes),
                    max_sqrt_h_projection_H1=max(point['sqrt_h_projection_H1'] for point in probes),
                    max_reference_flow_norm=max(point['reference_canonical_flow_norm'] for point in probes),
                    max_Gram_factor_l1_over_h_squared=max(point['Gram_factor_l1_over_h_squared'] for point in probes), probes=probes)
                evidence.report['cases'].append(row)
                evidence.save()
                print({name: value for name, value in row.items() if name != 'probes'}, flush=True)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
