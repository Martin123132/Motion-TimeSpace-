from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_sparse_live_repaired_20260915 import SparseRepairedLiveSystem, SparseMaterial
from annular_repaired_live_geometry_20260915 import material_weight
from annular_repaired_live_current_20260915 import LiveTangent
from annular_live_barycentric_20260915 import BarycentricLiveContinuum
from annular_live_jump_aware_comparison_20260915 import sample_geometry_fast
from scipy.integrate import solve_ivp
import argparse
import json
import time
import numpy as np


def compare(system, coordinates, rates, clocks, geometry, oracle, target_geometry, label_order=6):
    material = SparseMaterial(system, coordinates)
    points, weights = np.polynomial.legendre.leggauss(label_order)
    labels, weights = points/2, weights*material_weight(points/2)/2
    difference, norm = 0., 0.
    source_errors, velocity_errors, clock_errors = [], [], []
    for label, weight in zip(labels, weights):
        interpolation = material.interpolation([label])[0]
        values, velocity = interpolation @ coordinates, interpolation @ rates
        target = target_geometry.material.values([label])[0]
        layer = system.layer(label, geometry)
        endpoints = np.unique(np.concatenate([layer.radii, [values[-1], target[0]], target_geometry.edges]))
        endpoints = endpoints[(endpoints >= layer.radii[0]) & (endpoints <= layer.radii[-1])]
        lengths = np.diff(endpoints)
        radius = (endpoints[:-1, None]+lengths[:, None]*layer.fractions).ravel()
        quadrature = (lengths[:, None]*layer.weights).ravel()
        cell, shape, radial, motion = layer.features(radius, values[-1])
        scalar = np.column_stack([values[cell], values[cell+1]])
        scalar_rate = np.column_stack([velocity[cell], velocity[cell+1]])
        temporal = np.sum(shape*scalar_rate, axis=1)+np.sum(motion*scalar, axis=1)*velocity[-1]
        gradient = np.sum(radial*scalar, axis=1)
        target_temporal, target_gradient = sample_geometry_fast(oracle, target_geometry, radius, np.full(len(radius), label))
        lapse, root = target_geometry.metric(radius)
        kinetic, stiffness = radius**2/(lapse*root), radius**2*lapse*root
        difference += weight*np.dot(quadrature, kinetic*(temporal-target_temporal)**2+stiffness*(gradient-target_gradient)**2)
        norm += weight*np.dot(quadrature, kinetic*target_temporal**2+stiffness*target_gradient**2)
        source_errors.append(abs(values[-1]-target[0]))
        lapse, root = target_geometry.metric(target[0])
        energy = np.sqrt(oracle.source_mass**2+root**2*target[1]**2)
        velocity_errors.append(abs(velocity[-1]-lapse*root**2*target[1]/energy))
        clock_errors.append(abs(interpolation @ clocks-target[2]))
    probes = np.unique(np.concatenate([np.linspace(5.21, 6.79, 257), np.linspace(6.015, 6.045, 101)]))
    target_mass = target_geometry.evaluate(probes, target_geometry.mass_coefficients)
    lapse, root = geometry.metric(probes)
    target_lapse, target_root = target_geometry.metric(probes)
    return dict(field_error=float(np.sqrt(difference/norm)), scalar_norm=float(norm),
                source_error=float(max(source_errors)), velocity_error=float(max(velocity_errors)), clock_error=float(max(clock_errors)),
                mass_error=float(np.max(abs(geometry.values(probes)[0]-target_mass))),
                lapse_error=float(np.max(abs(lapse-target_lapse))), root_error=float(np.max(abs(root-target_root))))


def evolve(evidence, system, key, step_factor):
    coordinates, momenta, rates, initial_geometry = system.initial()
    size = 2*coordinates.size
    initial = np.concatenate([np.stack([coordinates, momenta]).ravel(), np.zeros(len(system.labels))])
    times = np.linspace(0., .02, 5)
    states = [initial]
    initial_cells = np.searchsorted(system.base, coordinates[:, -1]-system.width*system.labels)-1
    minimum_margin = 1.
    calls = 0
    started = time.perf_counter()

    def rhs(time_value, state):
        nonlocal minimum_margin, calls
        calls += 1
        positions, momenta = state[:size].reshape(2, len(system.labels), system.count+1)
        local = positions[:, -1]-system.width*system.labels
        cells = np.searchsorted(system.base, local)-1
        phase = (local-system.base[cells])/system.spacing
        minimum_margin = min(minimum_margin, float(np.min(np.minimum(phase, 1-phase))))
        if np.any(cells != initial_cells) or minimum_margin <= .15:
            raise ValueError('Unqualified source cell crossing or phase margin; preserve this attempt.')
        rates, geometry = system.solve(positions, momenta)
        force = system.forces(positions, rates, geometry)
        lapse, root = geometry.metric(positions[:, -1])
        clock = np.sqrt(lapse**2-rates[:, -1]**2/root**2)
        return np.concatenate([np.stack([rates, force]).ravel(), clock])

    max_step = min(.005, step_factor*system.spacing)
    for lower, upper in zip(times[:-1], times[1:]):
        if time.perf_counter()-started > 7200:
            raise RuntimeError('Safe per-case time budget reached; accepted intervals retained.')
        solution = solve_ivp(rhs, (lower, upper), states[-1], method='DOP853', rtol=2e-10, atol=2e-12,
                             max_step=max_step, first_step=min(max_step, upper-lower), t_eval=[upper])
        if not solution.success:
            raise RuntimeError(solution.message)
        states.append(solution.y[:, -1])
        path = evidence.output/(key+'-accepted-'+format(upper, '.3f')+'.npz')
        np.savez_compressed(path, time=upper, state=states[-1])
        evidence.own(path, 'outputs')
        evidence.report.update(active_case=key, accepted_time=float(upper), rhs_calls=calls)
        evidence.save()
        print(dict(case=key, accepted_time=upper, rhs_calls=calls, seconds=time.perf_counter()-started), flush=True)
    states = np.array(states)
    path = evidence.output/(key+'.npz')
    np.savez_compressed(path, time=times, state=states.T)
    evidence.own(path, 'outputs')
    return times, states, initial_geometry.mass_nodes[-1, -1], calls, minimum_margin, max_step


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--counts', nargs='+', type=int, required=True)
    parser.add_argument('--label', required=True)
    parser.add_argument('--step-factor', type=float, default=.25)
    parser.add_argument('--radial-degree', type=int, default=10)
    args = parser.parse_args()
    evidence = EvidenceRun(args.label, __file__)
    evidence.report['arguments'] = vars(args)
    evidence.report['prespecified_accuracy_gates'] = dict(field_relative=.005, source=5e-7, velocity=2e-5,
        clock=2e-7, radial=2e-8, mass_drift=2e-9, cell_margin=.15, force_absolute=2e-7, force_relative=.02)
    evidence.save()
    try:
        qualified = evidence.output.parent/'annular-sparse-live-equivalence-attempt01/status.json'
        evidence.own(qualified)
        evidence.check('sparse_dense_equivalence_precedes_refinement', json.loads(qualified.read_text())['state'] == 'complete')
        oracle_directory = evidence.output.parent/'annular-live-continuum-degree512-attempt01'
        evidence.own(oracle_directory/'status.json')
        evidence.check('independent_oracle_qualified', json.loads((oracle_directory/'status.json').read_text())['sampled_finite_time_continuum_accuracy_qualified'])
        path = oracle_directory/'degree512.npz'
        evidence.own(path)
        saved = np.load(path)
        oracle = BarycentricLiveContinuum(512, 8, 18, radial_spacing=.025, label_order=12)
        oracle_geometries = [oracle.solve(state) for state in saved['states']]
        target_force = float(oracle.rhs_with_geometry(saved['states'][-1])[2]['radiation'][4])
        for count in args.counts:
            for gram in [False, True]:
                branch = 'MTS' if gram else 'reference'
                key = branch+'-'+str(count)
                started = time.perf_counter()
                system = SparseRepairedLiveSystem(count, gram, 8, args.radial_degree)
                times, states, initial_mass, calls, margin, max_step = evolve(evidence, system, key, args.step_factor)
                evidence.check(key+'_same_physical_times', np.allclose(times, saved['times'], rtol=0., atol=1e-15))
                size = 2*9*(count+1)
                diagnostics, masses = [], []
                for time_value, state, target_geometry in zip(times, states, oracle_geometries):
                    coordinates, momenta = state[:size].reshape(2, 9, count+1)
                    rates, geometry = system.solve(coordinates, momenta)
                    row = compare(system, coordinates, rates, state[size:], geometry, oracle, target_geometry)
                    row['time'] = float(time_value)
                    diagnostics.append(row)
                    masses.append(geometry.mass_nodes[-1, -1])
                radial = geometry.off_grid_residual(rates)
                tangent = LiveTangent(system, coordinates, momenta)
                physical_force = float(-tangent.layer_data(0.)[7])
                half_tangent = LiveTangent(system, coordinates, momenta, difference_step=1e-5)
                force_step_difference = float(abs(physical_force+half_tangent.layer_data(0.)[7]))
                control = compare(system, coordinates, rates, states[-1, size:], geometry, oracle, oracle_geometries[-1], label_order=10)
                summary = dict(key=key, count=count, branch=branch, seconds=time.perf_counter()-started,
                    width=.02, coupling=.1, duration=.02, layer_degree=8, radial_degree=args.radial_degree, max_step=max_step,
                    initial_phase=float(np.mod((6.03-5.2)/system.spacing, 1.)), minimum_cell_margin=margin, rhs_calls=calls,
                    maximum_field_error=max(row['field_error'] for row in diagnostics), final_field_error=diagnostics[-1]['field_error'],
                    maximum_source_error=max(row['source_error'] for row in diagnostics), maximum_velocity_error=max(row['velocity_error'] for row in diagnostics),
                    maximum_clock_error=max(row['clock_error'] for row in diagnostics),
                    exterior_mass_drift=float(np.max(abs(np.array(masses)-initial_mass))), mass_radial_residual=radial[0], lapse_radial_residual=radial[1],
                    off_grid_canonical_residual=system.canonical_residual(coordinates, momenta, rates, geometry, True),
                    final_wave_force=physical_force, target_force=target_force, force_absolute_error=abs(physical_force-target_force),
                    force_relative_error=abs(physical_force-target_force)/abs(target_force), force_difference_step_change=force_step_difference,
                    label_quadrature_error_change=abs(control['field_error']-diagnostics[-1]['field_error']),
                    sparse_shape_bytes=int(geometry.density.shape.nbytes), valid_for_physics_claim=False)
                summary['strict_half_percent_waveform_gate'] = summary['maximum_field_error'] < .005
                summary['strict_force_gate'] = summary['force_absolute_error'] < 2e-7 and summary['force_relative_error'] < .02
                summary['source_clock_gate'] = summary['maximum_source_error'] < 5e-7 and summary['maximum_velocity_error'] < 2e-5 and summary['maximum_clock_error'] < 2e-7
                path = evidence.output/(key+'-diagnostics.json')
                path.write_text(json.dumps(dict(summary=summary, times=diagnostics), indent=2, allow_nan=False)+'\n', encoding='utf-8')
                evidence.own(path, 'outputs')
                evidence.report['cases'].append(summary)
                evidence.save()
                print(summary, flush=True)
                evidence.check(key+'_radial_constraints', max(radial) < 2e-8, summary)
                evidence.check(key+'_mass_drift', summary['exterior_mass_drift'] < 2e-9, summary)
                evidence.check(key+'_off_grid_canonical', summary['off_grid_canonical_residual'] < 2e-8, summary)
                evidence.check(key+'_quadrature_and_force_differentiation_control', max(summary['label_quadrature_error_change'], force_step_difference) < 1e-7, summary)
                evidence.check(key+'_finite_physical_diagnostics', all(np.isfinite(row['field_error']) and row['scalar_norm'] > 0 for row in diagnostics))
        evidence.report.update(same_gates_both_branches=True, finite_accuracy_failures_recorded_not_suppressed=True,
            all_Gram_factors_retained=True, moving_source_field_momentum_derivative_retained=True,
            same_original_preparation_width_domain_and_duration=True, energy_projection=False,
            uniform_phase_independent_convergence_proven=False,
            full_GR_limit_proven=False, valid_for_physics_claim=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
