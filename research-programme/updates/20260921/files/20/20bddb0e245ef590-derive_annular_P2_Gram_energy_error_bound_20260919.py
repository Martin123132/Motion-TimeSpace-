from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_P2_indexed_live_geometry_20260919 import IndexedGradedP2System, IndexedP2Material
from annular_P2_graded_source_20260919 import GradedSourceAction, scalar_pencil
from run_annular_P2_continuum_bridge_20260918 import checked_load
from run_annular_P2_saved_impulse_20260919 import own_core
from scipy.linalg import cho_factor, cho_solve, eigvalsh, solve_banded
import contextlib
import json
import numpy as np


def fixed_geometry_functional(layer, values, weights, weight_derivative):
    coordinates = np.append(values, layer.fixed_source_for_probe)
    data = layer.evaluate(0., coordinates, np.zeros_like(coordinates))
    projection = solve_banded((2, 2), data['mass_bands'], data['cross'], check_finite=False)
    factor, projected = layer.lifted @ values, layer.lifted @ projection
    value = -.5*(weight_derivative @ factor**2)+weights @ (factor*projected)
    return value, data, factor, projected


def functional_gradient(layer, values, weights, derivative):
    value, data, factor, projected = fixed_geometry_functional(layer, values, weights, derivative)
    gram_covector = layer.lifted.T @ (weights*factor)
    dual = solve_banded((2, 2), data['mass_bands'], gram_covector, check_finite=False)
    radius, jacobian, motion = layer.mapping(layer.reference_radius, layer.fixed_source_for_probe)
    kinetic_weights = layer.reference_weight*jacobian*radius**4/layer.coefficient(0., radius)
    dual_values = np.sum(layer.reference_shape*dual[layer.reference_indices], axis=1)
    adjoint = layer.assemble_quadratic(layer.reference_indices, layer.reference_radial
        *((-motion/jacobian)*kinetic_weights*dual_values)[:, None])
    gradient = -layer.lifted.T @ (derivative*factor)+adjoint+layer.lifted.T @ (weights*projected)
    return float(value), gradient


def main():
    own_core(1)
    evidence = EvidenceRun('annular-P2-Gram-energy-error-bound-attempt01', __file__)
    try:
        evidence.report.update(github_action=False, subagents_used=False,
            full_live_P2_force_convergence_proven=False, no_new_evolution=True,
            fixed_geometry_field_only_bound=True, current_full_scalar_energy_used=True,
            no_mode_clipping_or_truncation=True, evolving_metric_and_source_defects_not_bounded_here=True,
            hierarchical_defects_not_known_continuum_error=True)
        for branch in ['reference', 'MTS']:
            final_steps = 128 if branch == 'MTS' else 64
            final_folder = 'annular-P2-bulk513-MTS-time128-attempt01' if branch == 'MTS' else 'annular-P2-bulk513-evolution-reference-attempt01'
            final = checked_load(evidence, final_folder, 'steps'+str(final_steps)+'-accepted'+str(final_steps).zfill(3)+'.npz')
            earlier_steps = final_steps//2
            earlier = checked_load(evidence, 'annular-P2-bulk513-evolution-'+branch+'-attempt01',
                'steps'+str(earlier_steps)+'-accepted'+str(earlier_steps).zfill(3)+'.npz')
            coarse = checked_load(evidence, 'annular-P2-local-Gram-bound-attempt01', branch+'257-row-data.npz')
            system = IndexedGradedP2System(513, branch == 'MTS', 1e-5)
            rates, geometry = system.solve(*final['state'])
            interpolation = IndexedP2Material(system, final['state'][0]).interpolation(np.array([0.]))[0]
            coordinates = interpolation @ final['state'][0]
            layer = system.layer(0., geometry)
            layer.fixed_source_for_probe = coordinates[-1]
            radius, jacobian, unused = layer.mapping(layer.radii, coordinates[-1])
            weights = np.asarray(layer.sampling @ (layer.coefficient(0., radius)/jacobian))/layer.gram_spacing
            moved, changed_jacobian, unused = layer.mapping(layer.radii, complex(coordinates[-1], 1e-24))
            derivative = np.asarray(layer.sampling @ (layer.coefficient(0., moved)/changed_jacobian)).imag/(1e-24*layer.gram_spacing)
            mass, stiffness = scalar_pencil(layer, coordinates)
            factorization = cho_factor(stiffness, lower=True, check_finite=False)
            frequency = float(np.sqrt(eigvalsh(stiffness, mass, subset_by_index=[layer.count-1, layer.count-1], check_finite=False)[0]))
            probe_radius, unused, probe_motion = layer.mapping(layer.reference_radius, coordinates[-1])
            transport_bound = float(max(abs(probe_motion)*probe_radius**2/layer.coefficient(0., probe_radius)))
            shape_bound = float(np.max(abs(derivative)/weights, initial=0.))
            quadratic_bound = shape_bound/2+frequency*transport_bound if len(weights) else 0.
            force, gradient = functional_gradient(layer, coordinates[:-1], weights, derivative)
            random = np.random.default_rng(20260919)
            for trial in range(3):
                direction = random.normal(size=layer.count)
                direction /= np.sqrt(direction @ stiffness @ direction)
                changed = coordinates[:-1].astype(complex)+1j*1e-24*direction
                shifted = fixed_geometry_functional(layer, changed, weights, derivative)[0].imag/1e-24
                actual = float(gradient @ direction)
                evidence.check(branch+'_gradient_direction_'+str(trial), abs(shifted-actual) < 2e-10*max(1., abs(actual)))
            coarse_model = GradedSourceAction(257, branch == 'MTS', source_cap=2e-5)
            indices, shape, unused = coarse_model.features_quadratic(layer.radii)
            embedded = np.sum(shape*coarse['coordinates'][:-1][indices], axis=1)
            temporal = (interpolation @ earlier['state'][0])[:-1]
            results = []
            for name, base in [('spatial_hierarchy', embedded), ('time_step_halving', temporal)]:
                base_force, base_gradient = functional_gradient(layer, base, weights, derivative)
                error = coordinates[:-1]-base
                energy_squared = float(error @ stiffness @ error)
                dual_squared = float(base_gradient @ cho_solve(factorization, base_gradient, check_finite=False))
                evidence.check(branch+'_'+name+'_positive_energy_norms', energy_squared >= 0 and dual_squared >= 0)
                energy, gain = np.sqrt(energy_squared), np.sqrt(dual_squared)
                error_force = float(fixed_geometry_functional(layer, error, weights, derivative)[0])
                linear = float(base_gradient @ error)
                difference = force-base_force
                bound = gain*energy+quadratic_bound*energy_squared
                evidence.check(branch+'_'+name+'_exact_polarization', abs(difference-linear-error_force) < 2e-15)
                evidence.check(branch+'_'+name+'_dual_and_quadratic_bounds', abs(linear) <= gain*energy+2e-15
                    and abs(error_force) <= quadratic_bound*energy_squared+2e-15 and abs(difference) <= bound+2e-15)
                results.append(dict(kind=name, field_energy_norm=float(energy), force_energy_dual_gain=float(gain),
                    quadratic_operator_bound=float(quadratic_bound), energy_force_error_bound=float(bound),
                    measured_fixed_geometry_force_change=float(difference), linear_term=linear, quadratic_term=error_force,
                    base_force=base_force, valid_for_claim=False))
            row = dict(branch=branch, base_count=513, fine_steps=final_steps, compared_steps=earlier_steps,
                explicit_Gram_force=force, maximum_full_scalar_frequency=frequency,
                transport_mass_bound=transport_bound, relative_weight_shape_bound=shape_bound,
                retained_scalar_modes=layer.count, cases=results, valid_for_claim=False)
            evidence.report['cases'].append(row)
            evidence.save()
            print(json.dumps(row), flush=True)
        with (evidence.output/'completion.txt').open('w', encoding='utf-8') as stream, contextlib.redirect_stdout(stream):
            evidence.complete()
        evidence.own(evidence.output/'completion.txt', 'outputs')
        evidence.save()
        print(json.dumps(dict(state='complete', checks=len(evidence.report['checks']))), flush=True)
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
