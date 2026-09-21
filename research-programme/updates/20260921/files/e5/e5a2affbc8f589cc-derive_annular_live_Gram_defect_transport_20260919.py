from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_P2_indexed_live_geometry_20260919 import IndexedGradedP2System, IndexedP2Material
from annular_live_P2_canonical_v2_20260918 import inverse_momenta
from annular_P2_Gram_row_bounds_20260919 import row_bounds
from derive_annular_P2_Gram_energy_error_bound_20260919 import functional_gradient, fixed_geometry_functional
from run_annular_P2_saved_impulse_20260919 import trajectory, own_core
from time import perf_counter
import argparse
import contextlib
import json
import numpy as np


def transport_budget(times, fields, gradients, momentum_rates, configuration_rates, geometry_defects, stride):
    indices = np.arange(0, len(times), stride)
    selected_times = times[indices]
    error, covectors = fields[indices], gradients[indices]
    momentum, configuration = momentum_rates[indices], configuration_rates[indices]
    intervals = np.diff(selected_times)[:, None]
    average_gradient = (covectors[1:]+covectors[:-1])/2
    average_error = (error[1:]+error[:-1])/2
    momentum_increment = intervals*(momentum[1:]+momentum[:-1])/2
    configuration_increment = intervals*(configuration[1:]+configuration[:-1])/2
    path_defect = np.diff(error, axis=0)-momentum_increment-configuration_increment
    components = dict(momentum_fed=average_gradient*momentum_increment,
        configuration_metric_fed=average_gradient*configuration_increment,
        reconstructed_path_quadrature=average_gradient*path_defect,
        moving_covector=np.diff(covectors, axis=0)*average_error)
    signed = {name:float(np.sum(values)) for name, values in components.items()}
    absolute = {name:float(np.sum(abs(values))) for name, values in components.items()}
    initial = float(covectors[0] @ error[0]+geometry_defects[0])
    endpoint = float(covectors[-1] @ error[-1]+geometry_defects[-1])
    geometric_change = float(geometry_defects[-1]-geometry_defects[0])
    reconstructed = initial+sum(signed.values())+geometric_change
    return dict(sample_intervals=len(indices)-1, stride=stride,
        initial_difference=initial, endpoint_difference=endpoint,
        terminal_geometry_change=geometric_change, signed_terms=signed,
        absolute_nodal_bounds=absolute, reconstructed_endpoint=reconstructed,
        reconstruction_error=abs(reconstructed-endpoint),
        endpoint_bound=abs(initial)+sum(absolute.values())+abs(geometric_change),
        omitted_geometry_and_covector_prediction=initial+signed['momentum_fed']+signed['reconstructed_path_quadrature'],
        path_quadrature_defect_is_not_an_ODE_error_certificate=True, valid_for_claim=False)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--branch', choices=['reference', 'MTS'], required=True)
    options = parser.parse_args()
    own_core(0 if options.branch == 'MTS' else 1)
    evidence = EvidenceRun('annular-live-Gram-defect-transport-'+options.branch+'-attempt01', __file__)
    try:
        started = perf_counter()
        fine_steps = 128 if options.branch == 'MTS' else 64
        coarse_steps = fine_steps//2
        evidence.report.update(github_action=False, subagents_used=False, branch=options.branch,
            full_live_P2_force_convergence_proven=False, exact_moving_covector_identity_not_a_full_adjoint_solve=True,
            no_new_trajectory_evolution=True, changing_geometry_reconstructed_on_both_actual_paths=True,
            all_Gram_rows_retained=True, retained_full_canonical_state=True, temporal_hierarchy_not_continuum_error=True,
            maximum_wall_seconds=5400., base_count=513, fine_steps=fine_steps, coarse_steps=coarse_steps,
            momentum_counterfactual_is_not_an_evolved_state=True,
            quadrature_defect_not_identified_as_integrator_error=True,
            geometry_and_initial_data_terms_not_discarded=True)
        unused, fine_times, fine_states = trajectory(evidence, options.branch, 513, fine_steps)
        unused, coarse_times, coarse_states = trajectory(evidence, options.branch, 513, coarse_steps)
        system = IndexedGradedP2System(513, options.branch == 'MTS', 1e-5)
        times = np.linspace(0., 4e-5, 33)
        fields, gradients, source_gradients = [], [], []
        momentum_rates, configuration_rates, geometry_defects, source_geometry_defects = [], [], [], []
        scalar_samples = []
        for index, instant in enumerate(times):
            if perf_counter()-started > evidence.report['maximum_wall_seconds']:
                raise RuntimeError('Safe wall budget reached; all completed transport samples retained.')
            fine_index, coarse_index = index*fine_steps//32, index*coarse_steps//32
            fine_state, coarse_state = fine_states[fine_index], coarse_states[coarse_index]
            evidence.check('sample'+str(index)+'_matched_actual_times',
                abs(fine_times[fine_index]-instant) < 1e-18 and abs(coarse_times[coarse_index]-instant) < 1e-18)
            fine_rates, fine_geometry = system.solve(*fine_state)
            if np.array_equal(fine_state, coarse_state):
                coarse_rates, coarse_geometry = fine_rates, fine_geometry
            else:
                coarse_rates, coarse_geometry = system.solve(*coarse_state)
            interpolation = IndexedP2Material(system, fine_state[0]).interpolation(np.array([0.]))[0]
            fine_values, coarse_values = interpolation @ fine_state[0], interpolation @ coarse_state[0]
            fine_velocity, coarse_velocity = interpolation @ fine_rates, interpolation @ coarse_rates
            coarse_momentum = interpolation @ coarse_state[1]
            fine_layer, coarse_layer = system.layer(0., fine_geometry), system.layer(0., coarse_geometry)
            fine_layer.fixed_source_for_probe = fine_values[-1]
            fine_report, fine_rows = row_bounds(fine_layer, fine_values, fine_velocity)
            coarse_report, coarse_rows = row_bounds(coarse_layer, coarse_values, coarse_velocity)
            weights = fine_rows['weights']
            nodes, jacobian, unused = fine_layer.mapping(fine_layer.radii, complex(fine_values[-1], 1e-24))
            derivative = np.asarray(fine_layer.sampling @ (fine_layer.coefficient(0., nodes)/jacobian)).imag/(1e-24*fine_layer.gram_spacing)
            midpoint = (fine_values[:-1]+coarse_values[:-1])/2
            unused, gradient = functional_gradient(fine_layer, midpoint, weights, derivative)
            source_mask = fine_rows['source_rows']
            unused, source_gradient = functional_gradient(fine_layer, midpoint, weights*source_mask, derivative*source_mask)
            frozen_coarse = float(fixed_geometry_functional(fine_layer, coarse_values[:-1], weights, derivative)[0])
            frozen_coarse_source = float(fixed_geometry_functional(fine_layer, coarse_values[:-1], weights*source_mask, derivative*source_mask)[0])
            fine_source = sum(fine_rows['shape_rows'][source_mask])+sum(fine_rows['projected_rows'][source_mask])
            coarse_mask = coarse_rows['source_rows']
            coarse_source = sum(coarse_rows['shape_rows'][coarse_mask])+sum(coarse_rows['projected_rows'][coarse_mask])
            difference = fine_values[:-1]-coarse_values[:-1]
            geometry_difference = frozen_coarse-coarse_report['explicit_drive']
            source_geometry_difference = frozen_coarse_source-coarse_source
            direct_difference = fine_report['explicit_drive']-coarse_report['explicit_drive']
            direct_source_difference = fine_source-coarse_source
            evidence.check('sample'+str(index)+'_quadratic_secant_including_geometry',
                abs(gradient @ difference+geometry_difference-direct_difference) < 3e-15
                and abs(source_gradient @ difference+source_geometry_difference-direct_source_difference) < 3e-15)
            counterfactual_rates, diagnostic = inverse_momenta(fine_layer, fine_values, coarse_momentum)
            momentum_rate = fine_velocity[:-1]-counterfactual_rates[:-1]
            configuration_rate = counterfactual_rates[:-1]-coarse_velocity[:-1]
            evidence.check('sample'+str(index)+'_exact_velocity_split',
                np.max(abs(momentum_rate+configuration_rate-(fine_velocity[:-1]-coarse_velocity[:-1]))) < 2e-18
                and diagnostic['timelike_ratio'] < 1 and diagnostic['total_schur'] > 0)
            sample = dict(time=float(instant), actual_fine_drive=fine_report['explicit_drive'],
                actual_coarse_drive=coarse_report['explicit_drive'], direct_drive_difference=direct_difference,
                fixed_fine_geometry_field_difference=float(gradient @ difference),
                terminal_configuration_metric_difference=float(geometry_difference),
                gradient_field_pairing_error=float(abs(gradient @ difference+geometry_difference-direct_difference)),
                source_drive_difference=float(direct_source_difference),
                field_difference_maximum=float(np.max(abs(difference))),
                source_position_difference=float(fine_values[-1]-coarse_values[-1]),
                momentum_fed_rate_maximum=float(np.max(abs(momentum_rate))),
                configuration_metric_fed_rate_maximum=float(np.max(abs(configuration_rate))),
                counterfactual_timelike_ratio=diagnostic['timelike_ratio'], valid_for_claim=False)
            path = evidence.output/('sample'+str(index).zfill(3)+'.npz')
            np.savez_compressed(path, time=instant, field_difference=difference, gradient=gradient,
                source_gradient=source_gradient, momentum_rate=momentum_rate, configuration_rate=configuration_rate,
                geometry_difference=geometry_difference, source_geometry_difference=source_geometry_difference)
            evidence.own(path, 'outputs')
            fields.append(difference)
            gradients.append(gradient)
            source_gradients.append(source_gradient)
            momentum_rates.append(momentum_rate)
            configuration_rates.append(configuration_rate)
            geometry_defects.append(geometry_difference)
            source_geometry_defects.append(source_geometry_difference)
            scalar_samples.append(sample)
            evidence.report.update(samples=scalar_samples, accepted_samples=len(scalar_samples),
                accepted_time=float(instant), seconds=perf_counter()-started)
            evidence.save()
            if index % 4 == 0:
                print(json.dumps(dict(branch=options.branch, sample=index, seconds=perf_counter()-started,
                    actual_Gram_force_difference=direct_difference)), flush=True)
        fields, gradients, source_gradients, momentum_rates, configuration_rates, geometry_defects, source_geometry_defects = [
            np.array(values) for values in [fields, gradients, source_gradients, momentum_rates, configuration_rates, geometry_defects, source_geometry_defects]]
        for name, covector, geometric in [('all_rows', gradients, geometry_defects),
                ('source_rows', source_gradients, source_geometry_defects),
                ('remaining_rows', gradients-source_gradients, geometry_defects-source_geometry_defects)]:
            for stride in [4, 2, 1]:
                row = transport_budget(times, fields, covector, momentum_rates, configuration_rates, geometric, stride)
                row['partition'] = name
                evidence.check(name+'_'+str(stride)+'_transport_product_identity', row['reconstruction_error'] < 3e-15
                    and abs(row['endpoint_difference']) <= row['endpoint_bound']+3e-15)
                evidence.report['cases'].append(row)
        evidence.check('33_actual_saved_time_nodes_and_9_partitioned_budgets', len(scalar_samples) == 33 and len(evidence.report['cases']) == 9)
        with (evidence.output/'completion.txt').open('w', encoding='utf-8') as stream, contextlib.redirect_stdout(stream):
            evidence.complete()
        evidence.own(evidence.output/'completion.txt', 'outputs')
        evidence.save()
        print(json.dumps(dict(state='complete', branch=options.branch, checks=len(evidence.report['checks']),
            seconds=perf_counter()-started, budgets=evidence.report['cases'])), flush=True)
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
