from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_boundary_response_20260916 import field_matrices, nested_coordinates, split_vector
from derive_annular_trace_domain_20260916_v2 import analytic_quadrature_matrices
from annular_locally_refined_source_action_20260916 import LocallyRefinedSourceAction
from annular_quadratic_source_fitted_action_20260915 import QuadraticSourceFittedAction
import numpy as np


def relaxed_energy(system, field, position, weight_shift=None):
    matrices = field_matrices(system, position)
    weights = matrices['gram_weights']
    if weight_shift is not None:
        weights = weights+weight_shift
    values = system.original @ field
    hinge = system.lifted_hinge
    denominator = hinge @ (weights*hinge)
    trace = hinge @ (weights*values)/denominator
    residual = values-hinge*trace
    return residual @ (weights*residual)/2, trace, residual, weights


def main():
    evidence = EvidenceRun('annular-relaxed-trace-action-attempt01', __file__)
    try:
        intake = evidence.root/'source-intake/navier-stokes/20260914'
        for count, saved_splits in [(257, 8), (513, 4)]:
            coarse = QuadraticSourceFittedAction(count, True, background_mass=0.)
            saved_system = LocallyRefinedSourceAction(count, True, background_mass=0., source_splits=saved_splits)
            embedding, bubbles, retained, new = nested_coordinates(coarse, saved_system)
            path = intake/'annular-local-refinement-crossing-attempt02'/('MTS-'+str(count)+'.npz')
            evidence.own(path)
            saved = np.load(path)
            coordinates, rates = np.split(saved['states'][-1, :-1], 2)
            field, unused = split_vector(coordinates[:-1], embedding, retained, new)
            position = coordinates[-1]
            energy, trace, residual, weights = relaxed_energy(coarse, field, position)
            prefix = str(count)
            evidence.check(prefix+'_stationary_auxiliary_trace', abs(coarse.lifted_hinge @ (weights*residual)) < 2e-13)
            direction = np.sin(np.arange(coarse.count)*.47)
            step = 1e-24
            perturbed = relaxed_energy(coarse, field.astype(complex)+1j*step*direction, position)[0]
            field_partial = float(direction @ (coarse.original.T @ (weights*residual)))
            evidence.check(prefix+'_field_envelope_derivative', abs(perturbed.imag/step-field_partial) < 2e-10)
            perturbed = relaxed_energy(coarse, field, position+1j*step)[0]
            weight_derivative = field_matrices(coarse, position+1j*step)['gram_weights'].imag/step
            source_partial = float(residual @ (weight_derivative*residual)/2)
            evidence.check(prefix+'_source_envelope_derivative', abs(perturbed.imag/step-source_partial) < 2e-12)
            weight_direction = weights*np.cos(np.arange(len(weights))*.23)
            perturbed = relaxed_energy(coarse, field, position, 1j*step*weight_direction)[0]
            density_partial = float(weight_direction @ residual**2/2)
            evidence.check(prefix+'_weight_dual_retained', abs(perturbed.imag/step-density_partial) < 2e-12)
            trial_rows = []
            for splits in [2, 4, 8, 16, 32, 64]:
                system = LocallyRefinedSourceAction(count, True, background_mass=0., source_splits=splits)
                embedding, bubbles, retained, new = nested_coordinates(coarse, system)
                embedded = embedding @ field
                matrices = analytic_quadrature_matrices(system, position)
                source_edge = int(np.searchsorted(system.edges, system.anchor))
                width = system.edges[source_edge+1]-system.anchor
                layer = np.zeros(system.count)
                layer[system.element_indices[source_edge, 1]] = width/4
                target = relaxed_energy(system, embedded, position)[1]
                delta_trace = float(target-system.jump @ embedded)
                correction = delta_trace*layer
                recovered = embedded+correction
                factor = system.lifted @ recovered
                recovery_gram = float(factor @ (matrices['gram_weights']*factor)/2)
                bulk_difference = float(embedded @ (matrices['bulk'] @ correction)+correction @ (matrices['bulk'] @ correction)/2)
                correction_bulk = float(correction @ (matrices['bulk'] @ correction))
                embedded_bulk = float(embedded @ (matrices['bulk'] @ embedded))
                energy_bound = np.sqrt(max(0., embedded_bulk*correction_bulk))+correction_bulk/2
                evidence.check(prefix+'split'+str(splits)+'_same_samples_and_target_trace', np.max(abs(system.original @ correction), initial=0.) < 2e-14
                               and abs(system.jump @ recovered-target) < 2e-11)
                evidence.check(prefix+'split'+str(splits)+'_unchanged_Gram_attains_relaxed_value', abs(recovery_gram-energy) < 2e-14)
                evidence.check(prefix+'split'+str(splits)+'_bulk_recovery_error_bounded', abs(bulk_difference) <= energy_bound+2e-15)
                trial_rows.append(dict(source_splits=splits, layer_width=float(width), prescribed_trace_change=delta_trace,
                    correction_kinetic_norm_squared=float(correction @ (matrices['mass'] @ correction)),
                    bulk_energy_difference=bulk_difference, Gram_energy=recovery_gram, rigorous_bulk_Cauchy_bound=float(energy_bound)))
            evidence.report['cases'].append(dict(count=count, frozen_position=float(position), relaxed_Gram_energy=float(energy),
                relaxed_trace=float(trace), Gram_source_covector=float(-source_partial), recovery_sequence=trial_rows))
            evidence.save()
        evidence.report.update(scope='Static fixed-original-stencil relaxation with kinematic recovery sequences and exact field/source/weight derivatives. No altered dynamical trajectory or force improvement claimed.',
            unique_relaxation_under_stated_bulk_L2_topology=True, unique_parent_action_derived=False,
            finite_unrelaxed_action_changed=False, finite_trajectory_changed=False,
            moving_time_evolution_of_relaxed_action_tested=False, dynamic_convergence_to_relaxation_proven=False,
            no_new_fitted_parameter=True, source_current_must_still_be_retained=True)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()
