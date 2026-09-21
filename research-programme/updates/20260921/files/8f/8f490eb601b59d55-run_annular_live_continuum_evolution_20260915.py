from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_live_continuum_characteristics_20260915 import LiveContinuumCharacteristics, ContinuumDensity
from scipy.integrate import solve_ivp
import numpy as np
import time


def proper_acceleration_test(system, state, step=2e-5):
    flow, geometry, forces = system.rhs_with_geometry(state)
    source = geometry.material.source
    position, momentum = source[:, 0], source[:, 1]
    lapse, root = geometry.metric(position)
    energy = np.sqrt(system.source_mass**2+root**2*momentum**2)
    ratio = root*momentum/energy
    proper_speeds = []
    for multiple in [-2, -1, 1, 2]:
        adjacent = system.solve(state+multiple*step*flow)
        adjacent_source = adjacent.material.source
        unused, adjacent_root = adjacent.metric(adjacent_source[:, 0])
        proper_speeds.append(adjacent_root**2*adjacent_source[:, 1]/system.source_mass)
    measured = (proper_speeds[0]-8*proper_speeds[1]+8*proper_speeds[2]-proper_speeds[3])/(12*step*forces['clock'])
    density = ContinuumDensity(geometry.material, position, system.label_order+4)
    density.update(geometry.fields)
    rest_density = root**2*((1+ratio**2)*density.square+4*ratio*density.cross)/(2*(1-ratio**2))
    mass = geometry.evaluate(position, geometry.mass_coefficients)
    expected = -mass/position**2-system.coupling*position*rest_density
    expected += forces['radiation']*root**2/(system.source_mass*forces['clock'])
    return dict(measured=measured, expected=expected, error=float(np.max(abs(measured-expected))))


def evolve(system, max_step=.0025):
    state, initial_geometry = system.initial()
    calls = 0

    def rhs(time_value, values):
        nonlocal calls
        calls += 1
        if calls > 12000:
            raise RuntimeError('Bounded continuum smoke exceeded12000 RHS evaluations.')
        return system.rhs(time_value, values)

    trajectory = solve_ivp(rhs, (0., .02), state, method='DOP853', rtol=2e-10, atol=2e-12,
                           max_step=max_step, t_eval=np.linspace(0., .02, 5))
    if not trajectory.success or len(trajectory.t) != 5:
        raise RuntimeError('Continuum smoke trajectory failed: '+trajectory.message)
    return trajectory, initial_geometry, calls


def main():
    evidence = EvidenceRun('annular-live-continuum-evolution-attempt01', __file__)
    results = {}
    try:
        cases = [(64, 4, 14, .0025, .1, True, 'main'), (96, 4, 14, .0025, .1, True, 'main'),
                 (192, 4, 14, .0025, .1, True, 'main'), (96, 8, 14, .0025, .1, True, 'layer8'),
                 (96, 4, 18, .0025, .1, True, 'radial18'), (64, 4, 14, .0005, .1, True, 'halfstep'),
                 (64, 4, 14, .0025, .1, False, 'dust'), (64, 4, 14, .0025, 0., True, 'no_backreaction')]
        for degree, layer, radial, max_step, coupling, wave, label in cases:
            started = time.perf_counter()
            system = LiveContinuumCharacteristics(degree, layer, radial, radial_spacing=.05, coupling=coupling, wave=wave)
            trajectory, initial_geometry, calls = evolve(system, max_step)
            key = 'degree'+str(degree)+'-'+label
            current = system.current_test(trajectory.y[:, -1])
            acceleration = proper_acceleration_test(system, trajectory.y[:, -1])
            geometries = [system.solve(state) for state in trajectory.y.T]
            geometry = geometries[-1]
            radial_residual = geometry.check_radial()
            mass_drift = max(abs(item.mass_nodes[-1, -1]-initial_geometry.mass_nodes[-1, -1]) for item in geometries)
            raw = evidence.output/(key+'.npz')
            np.savez_compressed(raw, times=trajectory.t, states=trajectory.y.T, radial_nodes=geometry.nodes,
                                mass=geometry.mass_nodes, log_lapse=geometry.log_lapse_nodes,
                                current_radius=current['targets'], mass_time=current['derivative'], current=current['current'],
                                measured_acceleration=acceleration['measured'], expected_acceleration=acceleration['expected'])
            evidence.own(raw, 'outputs')
            row = dict(key=key, degree=degree, layer_degree=layer, radial_degree=radial, radial_spacing=.05,
                       label_order=8, coupling=coupling, wave=wave, width=.02, duration=.02,
                       max_step=max_step, rhs_calls=calls, seconds=time.perf_counter()-started,
                       minimum_material_jacobian=geometry.material.minimum_jacobian,
                       mass_exterior=float(geometry.mass_nodes[-1, -1]), exterior_mass_drift=float(mass_drift),
                       mass_radial_residual=radial_residual[0], lapse_radial_residual=radial_residual[1],
                       current_error=current['error'], proper_acceleration_error=acceleration['error'])
            evidence.report['cases'].append(row)
            evidence.save()
            print(row, flush=True)
            evidence.check(key+'_finite_ordered_trajectory', np.all(np.isfinite(trajectory.y)) and row['minimum_material_jacobian'] > 0, row)
            evidence.check(key+'_unprojected_exterior_mass', mass_drift < 2e-9, row)
            evidence.check(key+'_independent_radial_constraints', max(radial_residual) < 2e-8, row)
            evidence.check(key+'_independent_mass_time_current', current['error'] < 2e-8, row)
            evidence.check(key+'_derived_proper_acceleration', acceleration['error'] < 2e-7, row)
            results[key] = trajectory.y[:, -1]
        for label in ['radial18', 'layer8']:
            base = results['degree96-main']
            refined = results['degree96-'+label]
            if label == 'layer8':
                fine = LiveContinuumCharacteristics(96, 8)
                coarse = LiveContinuumCharacteristics(96, 4)
                fields, source = fine.unpack(refined)
                refined = coarse.pack(fields[::2], source[::2])
            difference = float(np.max(abs(refined-base)))
            evidence.check(label+'_whole_state_control', difference < 2e-7, difference)
        difference = float(np.max(abs(results['degree64-main']-results['degree64-halfstep'])))
        evidence.check('whole_state_halfstep', difference < 2e-8, difference)
        evidence.report.update(independent_common_live_geometry_continuum_evolved=True,
                               continuum_scalar_resolution_not_yet_qualified=True,
                               same_original_repaired_live_preparation=True, finite_width_held_fixed=True,
                               energy_or_state_projection=False, full_GR_limit_proven=False,
                               material_label_method='Polynomial collocation with continuous weighted density quadrature; not exact finite-label Galerkin.')
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
