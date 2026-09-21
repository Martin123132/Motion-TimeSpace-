from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_exponential_transport_20260919 import SavedCentralBasis
from annular_P2_indexed_live_geometry_20260919 import IndexedGradedP2System
from annular_P2_Gram_row_bounds_20260919 import row_bounds
from derive_annular_P2_Gram_energy_error_bound_20260919 import functional_gradient, fixed_geometry_functional
from run_annular_P2_continuum_bridge_20260918 import checked_load
from run_annular_P2_saved_impulse_20260919 import trajectory, own_core
from time import perf_counter
import argparse
import contextlib
import json
import numpy as np


def central_flow(system, state, center):
    rates, geometry = system.solve(*state)
    layer = system.layer(system.labels[center], geometry)
    data = layer.evaluate(0., state[0, center], rates[center])
    source_force = layer.source_covector(0., state[0, center], rates[center])
    force = np.append(data['scalar_covector'], source_force)
    return np.stack([rates[center], force]), rates[center], layer


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--branch', choices=['reference', 'MTS'], required=True)
    options = parser.parse_args()
    own_core(0 if options.branch == 'MTS' else 1)
    evidence = EvidenceRun('annular-live-exponential-transport-'+options.branch+'-attempt01', __file__)
    try:
        started = perf_counter()
        fine_steps = 128 if options.branch == 'MTS' else 64
        coarse_steps = fine_steps//2
        intervals = coarse_steps
        evidence.report.update(github_action=False, subagents_used=False, full_live_P2_force_convergence_proven=False,
            branch=options.branch, no_new_evolution=True, full_live_geometry_reconstructed=True,
            all_scalar_modes_retained=True, no_dense_nonlinear_jacobian=True,
            frozen_linear_split_not_frozen_geometry_dynamics=True,
            terminal_Gram_field_covector_not_complete_physical_force_adjoint=True,
            full_global_state_used_for_central_rhs=True, observed_temporal_hierarchy_not_continuum_error=True,
            defect_not_an_integrator_error_certificate=True, initial_and_terminal_geometry_terms_retained=True,
            maximum_wall_seconds=6600., fine_steps=fine_steps, coarse_steps=coarse_steps,
            sample_intervals=intervals, duration=4e-5)
        prerequisite_path = evidence.output.parent/'annular-exponential-transport-algebra-attempt01/status.json'
        prerequisite = json.loads(prerequisite_path.read_text())
        evidence.own(prerequisite_path)
        evidence.check('independent_oscillatory_controls_complete', prerequisite['state'] == 'complete'
            and all(row['passed'] for row in prerequisite['checks']))
        unused, fine_times, fine_states = trajectory(evidence, options.branch, 513, fine_steps)
        unused, coarse_times, coarse_states = trajectory(evidence, options.branch, 513, coarse_steps)
        saved = checked_load(evidence, 'annular-P2-bulk513-evolution-'+options.branch+'-attempt01', 'frozen-canonical-basis.npz')
        system = IndexedGradedP2System(513, options.branch == 'MTS', 1e-5)
        center = int(np.argmin(abs(system.labels)))
        basis = SavedCentralBasis(saved, center)
        evidence.check('same_full_initial_preparation', np.array_equal(saved['initial'], fine_states[0])
            and np.array_equal(saved['initial'], coarse_states[0]))
        evidence.check('all1072scalar_modes_and_source_block_retained', len(basis.frequency) == 1073
            and np.all(basis.frequency[:-1] > 0) and basis.frequency[-1] == 0)
        evidence.report.update(center_label_index=center, center_label=float(system.labels[center]),
            maximum_scalar_frequency=float(max(basis.frequency)))
        times = np.linspace(0., evidence.report['duration'], intervals+1)
        errors, remainders, scalar_samples = [], [], []
        for index, instant in enumerate(times):
            if perf_counter()-started > evidence.report['maximum_wall_seconds']:
                raise RuntimeError('Safe wall budget reached; accepted reconstructions retained.')
            fine_index, coarse_index = index*fine_steps//intervals, index*coarse_steps//intervals
            fine_state, coarse_state = fine_states[fine_index], coarse_states[coarse_index]
            evidence.check('sample'+str(index)+'_matched_saved_times', abs(fine_times[fine_index]-instant) < 1e-18
                and abs(coarse_times[coarse_index]-instant) < 1e-18)
            fine_flow, fine_velocity, fine_layer = central_flow(system, fine_state, center)
            if np.array_equal(fine_state, coarse_state):
                coarse_flow, coarse_velocity, coarse_layer = fine_flow, fine_velocity, fine_layer
            else:
                coarse_flow, coarse_velocity, coarse_layer = central_flow(system, coarse_state, center)
            physical_error = fine_state[:, center]-coarse_state[:, center]
            error = basis.encode(physical_error)
            flow_difference = basis.encode(fine_flow-coarse_flow)
            linear = basis.linear(error)
            remainder = flow_difference-linear
            roundtrip = float(np.linalg.norm(basis.decode(error)-physical_error)/max(np.linalg.norm(physical_error), 1e-30))
            reconstruction = float(np.linalg.norm(linear+remainder-flow_difference)/max(np.linalg.norm(flow_difference), 1e-30))
            evidence.check('sample'+str(index)+'_full_coordinate_and_rhs_reconstruction', roundtrip < 3e-10
                and reconstruction < 3e-10 and np.all(np.isfinite(remainder)), dict(roundtrip=roundtrip, rhs=reconstruction))
            row = dict(time=float(instant), modal_error_norm=float(np.linalg.norm(error)),
                modal_full_flow_difference_norm=float(np.linalg.norm(flow_difference)),
                modal_linear_difference_norm=float(np.linalg.norm(linear)),
                modal_remainder_difference_norm=float(np.linalg.norm(remainder)),
                remainder_subtraction_scale=float(np.linalg.norm(flow_difference)+np.linalg.norm(linear)),
                roundtrip_error=roundtrip, rhs_reconstruction_error=reconstruction, valid_for_claim=False)
            path = evidence.output/('sample'+str(index).zfill(3)+'.npz')
            np.savez_compressed(path, time=instant, modal_error=error, modal_remainder=remainder,
                modal_flow_difference=flow_difference, physical_error=physical_error)
            evidence.own(path, 'outputs')
            errors.append(error)
            remainders.append(remainder)
            scalar_samples.append(row)
            evidence.report.update(samples=scalar_samples, accepted_samples=len(scalar_samples),
                accepted_time=float(instant), seconds=perf_counter()-started)
            evidence.save()
            if index % 8 == 0:
                print(json.dumps(dict(branch=options.branch, sample=index, seconds=perf_counter()-started,
                    error_norm=row['modal_error_norm'], remainder_norm=row['modal_remainder_difference_norm'])), flush=True)
        fine_values, coarse_values = fine_states[-1, 0, center], coarse_states[-1, 0, center]
        fine_report, fine_rows = row_bounds(fine_layer, fine_values, fine_velocity)
        coarse_report, coarse_rows = row_bounds(coarse_layer, coarse_values, coarse_velocity)
        fine_layer.fixed_source_for_probe = fine_values[-1]
        radius, jacobian, unused = fine_layer.mapping(fine_layer.radii, complex(fine_values[-1], 1e-24))
        weights = fine_rows['weights']
        derivative = np.asarray(fine_layer.sampling @ (fine_layer.coefficient(0., radius)/jacobian)).imag/(1e-24*fine_layer.gram_spacing)
        midpoint = (fine_values[:-1]+coarse_values[:-1])/2
        unused, gradient = functional_gradient(fine_layer, midpoint, weights, derivative)
        source_mask = fine_rows['source_rows']
        unused, source_gradient = functional_gradient(fine_layer, midpoint, weights*source_mask, derivative*source_mask)
        frozen_coarse = float(fixed_geometry_functional(fine_layer, coarse_values[:-1], weights, derivative)[0])
        geometry_change = frozen_coarse-coarse_report['explicit_drive']
        direct_difference = fine_report['explicit_drive']-coarse_report['explicit_drive']
        terminal_covector = basis.field_covector(gradient)
        terminal_pairing = float(np.sum(terminal_covector*errors[-1]))
        evidence.check('terminal_covector_matches_physical_Gram_secant', abs(terminal_pairing+geometry_change-direct_difference) < 3e-15)
        probe = np.random.default_rng(20260919).normal(size=terminal_covector.shape)
        probe[:, -1] = 0.
        probe /= np.linalg.norm(probe)
        covectors = dict(all_Gram_rows=terminal_covector, source_Gram_rows=basis.field_covector(source_gradient),
            remaining_Gram_rows=basis.field_covector(gradient-source_gradient), unit_modal_algebra_control=probe)
        errors, remainders = np.array(errors), np.array(remainders)
        for name, covector in covectors.items():
            for subdivisions in [8, 16, 32, 64]:
                if subdivisions > intervals:
                    continue
                row = basis.budget(times, errors, remainders, covector, intervals//subdivisions)
                row.update(observable=name, covector_norm=float(np.linalg.norm(covector)), valid_for_claim=False)
                evidence.check(name+'_'+str(subdivisions)+'_discrete_dual_identity', row['endpoint_reconstruction_error']
                    < 3e-12*max(abs(row['endpoint_pairing']), row['forcing_absolute_interval_bound'],
                        row['defect_absolute_interval_bound'], 1e-15))
                evidence.report['cases'].append(row)
        evidence.report.update(terminal_direct_Gram_difference=direct_difference,
            terminal_fixed_geometry_pairing=terminal_pairing, terminal_geometry_correction=geometry_change,
            terminal_Gram_reconstruction_error=abs(terminal_pairing+geometry_change-direct_difference),
            prior_instantaneous_and_impulse_mismatches_unchanged=True)
        path = evidence.output/'terminal-covectors.npz'
        np.savez_compressed(path, frequency=basis.frequency, **covectors)
        evidence.own(path, 'outputs')
        with (evidence.output/'completion.txt').open('w', encoding='utf-8') as stream, contextlib.redirect_stdout(stream):
            evidence.complete()
        evidence.own(evidence.output/'completion.txt', 'outputs')
        evidence.save()
        print(json.dumps(dict(state='complete', branch=options.branch, checks=len(evidence.report['checks']),
            seconds=perf_counter()-started, budgets=[row for row in evidence.report['cases'] if row['observable'] == 'all_Gram_rows'])), flush=True)
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
