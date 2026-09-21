from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_repaired_live_geometry_20260915 import RepairedLiveSystem, MaterialState
from annular_repaired_live_current_20260915 import LiveTangent
from scipy.integrate import solve_ivp
import numpy as np
import time


def evolve(system, duration=.02, max_step=.005, wave=True):
    coordinates, momenta, initial_rates, initial_geometry = system.initial(wave=wave)
    canonical_size = 2*coordinates.size
    initial = np.concatenate([np.stack([coordinates, momenta]).ravel(), np.zeros(len(system.labels))])
    calls = 0

    def rhs(time_value, state):
        nonlocal calls
        calls += 1
        if calls > 2400:
            raise RuntimeError('Short-smoke RHS budget exceeded; retain this attempt.')
        position, momentum = state[:canonical_size].reshape(2, len(system.labels), system.count+1)
        velocity, geometry = system.solve(position, momentum)
        force = system.forces(position, velocity, geometry)
        lapse, root = geometry.metric(position[:, -1])
        clock = np.sqrt(lapse**2-velocity[:, -1]**2/root**2)
        return np.concatenate([np.stack([velocity, force]).ravel(), clock])

    trajectory = solve_ivp(rhs, (0., duration), initial, method='DOP853', rtol=2e-10, atol=2e-12,
                           max_step=max_step, t_eval=np.linspace(0., duration, 5))
    if not trajectory.success:
        raise RuntimeError(trajectory.message)
    coordinates, momenta = trajectory.y[:canonical_size, -1].reshape(2, len(system.labels), system.count+1)
    rates, geometry = system.solve(coordinates, momenta)
    return dict(trajectory=trajectory, coordinates=coordinates, momenta=momenta, rates=rates, geometry=geometry,
                initial_rates=initial_rates, initial_geometry=initial_geometry, initial_state=initial,
                canonical_size=canonical_size, rhs_calls=calls)


def dust_oracle(system, result):
    count = len(system.labels)
    initial_coordinates = result['initial_state'][:count*(system.count+1)].reshape(count, system.count+1)
    initial_radius = initial_coordinates[:, -1]
    initial_velocity = result['initial_rates'][:, -1]
    lapse, root = result['initial_geometry'].metric(initial_radius)
    initial_clock = np.sqrt(lapse**2-initial_velocity**2/root**2)
    initial_mass = result['initial_geometry'].values(initial_radius)[0]
    final_radius = result['coordinates'][:, -1]
    lapse, root = result['geometry'].metric(final_radius)
    final_clock = np.sqrt(lapse**2-result['rates'][:, -1]**2/root**2)
    final_speed = result['rates'][:, -1]/final_clock
    proper_times = result['trajectory'].y[result['canonical_size']:, -1]
    errors = []
    for index, duration in enumerate(proper_times):
        mass = initial_mass[index]
        solution = solve_ivp(lambda unused, state: [state[1], -mass/state[0]**2],
                             (0., duration), [initial_radius[index], initial_velocity[index]/initial_clock[index]],
                             method='DOP853', rtol=2e-12, atol=2e-14)
        errors.append([abs(solution.y[0, -1]-final_radius[index]), abs(solution.y[1, -1]-final_speed[index])])
    final_mass = result['geometry'].values(final_radius)[0]
    return dict(radius_error=float(np.max(np.array(errors)[:, 0])), proper_speed_error=float(np.max(np.array(errors)[:, 1])),
                advected_mass_error=float(np.max(abs(final_mass-initial_mass))))


def main():
    evidence = EvidenceRun('annular-repaired-live-evolution-attempt01', __file__)
    results = {}
    try:
        cases = [(count, 8, 10, .005, True, .1, 'main') for count in [17, 33, 65]]
        cases += [(17, 8, 10, .0025, True, .1, 'halfstep'),
                  (17, 4, 10, .005, True, .1, 'layer4'),
                  (17, 8, 6, .005, True, .1, 'radial6'),
                  (17, 8, 10, .005, False, .1, 'dust'),
                  (17, 8, 10, .005, True, 0., 'no_backreaction')]
        for count, layer_degree, radial_degree, max_step, wave, coupling, label in cases:
            for gram in [False, True]:
                branch = 'MTS' if gram else 'reference'
                key = branch+'-'+str(count)+'-'+label
                started = time.perf_counter()
                system = RepairedLiveSystem(count, gram, layer_degree, radial_degree, coupling=coupling)
                result = evolve(system, max_step=max_step, wave=wave)
                raw = evidence.output/(key+'.npz')
                trajectory = result['trajectory']
                np.savez_compressed(raw, time=trajectory.t, state=trajectory.y, rates=result['rates'],
                                    radial_nodes=result['geometry'].nodes, mass=result['geometry'].mass_nodes,
                                    log_lapse=result['geometry'].log_lapse_nodes)
                evidence.own(raw, 'outputs')
                initial_mass = result['initial_geometry'].mass_nodes[-1, -1]
                masses = []
                for state in trajectory.y[:result['canonical_size']].T:
                    coordinates, momenta = state.reshape(2, len(system.labels), count+1)
                    unused, geometry = system.solve(coordinates, momenta)
                    masses.append(geometry.mass_nodes[-1, -1])
                radial = result['geometry'].off_grid_residual(result['rates'])
                material = MaterialState(system, result['coordinates'])
                local_position = result['coordinates'][:, -1]-system.width*system.labels
                phase = np.mod((local_position-system.base[0])/system.spacing, 1.)
                row = dict(key=key, branch=branch, scalar_count=count, layer_degree=layer_degree,
                           radial_degree=radial_degree, width=system.width, kappa=coupling, wave=wave,
                           duration=.02, max_step=max_step, rhs_calls=result['rhs_calls'],
                           final_middle_source=float(result['coordinates'][layer_degree//2, -1]),
                           minimum_material_jacobian=material.minimum_jacobian,
                           minimum_cell_margin=float(np.min(np.minimum(phase, 1-phase))),
                           exterior_mass_drift=float(np.max(abs(np.array(masses)-initial_mass))),
                           mass_radial_residual=radial[0], lapse_radial_residual=radial[1],
                           off_grid_momentum_residual=system.canonical_residual(result['coordinates'], result['momenta'], result['rates'], result['geometry'], True))
                if label in ['main', 'dust']:
                    tangent = LiveTangent(system, result['coordinates'], result['momenta'])
                    middle = result['coordinates'][layer_degree//2, -1]
                    targets = np.array([5.53, 5.995, 6.005, middle-.007, middle, middle+.007, 6.095, 6.47])
                    comparison = tangent.compare(targets)
                    row.update(current_error=comparison['error'], on_shell_current_error=comparison['on_shell_error'],
                               material_Euler_current_correction=comparison['current_euler_correction'])
                    current_path = evidence.output/(key+'-current.npz')
                    np.savez_compressed(current_path, **comparison)
                    evidence.own(current_path, 'outputs')
                if not wave:
                    row.update(dust_oracle= dust_oracle(system, result))
                row['seconds'] = time.perf_counter()-started
                evidence.report['cases'].append(row)
                evidence.save()
                print(row, flush=True)
                evidence.check(key+'_ordered_timelike_no_cell_crossing', row['minimum_material_jacobian'] > 0 and row['minimum_cell_margin'] > .15, row)
                evidence.check(key+'_independent_radial_residuals', max(radial) < 2e-8, row)
                evidence.check(key+'_unprojected_exterior_mass', row['exterior_mass_drift'] < 2e-9, row)
                evidence.check(key+'_material_off_grid_canonical_residual', row['off_grid_momentum_residual'] < 2e-8, row)
                if 'current_error' in row:
                    evidence.check(key+'_independent_temporal_equation', row['on_shell_current_error'] < 2e-8, row)
                if not wave:
                    evidence.check(key+'_independent_proper_time_GR_dust', max(row['dust_oracle'].values()) < 2e-8, row)
                results[key] = result
        for branch in ['reference', 'MTS']:
            main_state = results[branch+'-17-main']['trajectory'].y[:, -1]
            half_state = results[branch+'-17-halfstep']['trajectory'].y[:, -1]
            half_error = float(np.max(abs(main_state-half_state)))
            evidence.check(branch+'_whole_state_halfstep', half_error < 2e-9, half_error)
            radial_state = results[branch+'-17-radial6']['trajectory'].y[:, -1]
            radial_error = float(np.max(abs(main_state-radial_state)))
            evidence.check(branch+'_whole_state_radial_refinement', radial_error < 2e-8, radial_error)
            low = results[branch+'-17-layer4']
            high = results[branch+'-17-main']
            layer_error = float(np.max(abs(low['trajectory'].y[:low['canonical_size'], -1].reshape(2, 5, 18)
                                          -high['trajectory'].y[:high['canonical_size'], -1].reshape(2, 9, 18)[:, ::2])))
            evidence.check(branch+'_common_label_refinement', layer_error < 2e-8, layer_error)
        dust_difference = float(np.max(abs(results['reference-17-dust']['trajectory'].y-results['MTS-17-dust']['trajectory'].y)))
        evidence.check('reference_MTS_zero_wave_identical', dust_difference < 2e-12, dust_difference)
        evidence.report.update(repaired_live_geometry_and_canonical_matter_evolved=True,
                               energy_or_state_projection=False, finite_source_width_held_fixed=True,
                               source_cell_crossing=False, continuum_waveform_accuracy_qualified=False,
                               material_label_method='Collocation, qualified only by off-grid and refinement checks.',
                               source_boundary_law_uniquely_parent_selected=False,
                               full_GR_limit_proven=False, valid_for_physics_claim=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
