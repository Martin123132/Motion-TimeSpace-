from derive_annular_source_gravity_20260914 import EvidenceRun
from probe_annular_P2_joint_refinement_20260919 import endpoint_mass
import contextlib
import json
import numpy as np
import sympy as symbolic


def frozen_fixture(left_lengths, right_lengths):
    lengths = np.concatenate([np.asarray(left_lengths)[::-1], right_lengths])
    source = 2*len(left_lengths)
    node_count = 2*len(lengths)+1
    kinetic, slope, inertia, geometric_drive, wave_drive = 2.4, .01, .045, -.015, .21
    local = np.array([[4., 2., -1.], [2., 16., 2.], [-1., 2., 4.]])/30
    mass = np.zeros((node_count, node_count))
    for element, length in enumerate(lengths):
        nodes = slice(2*element, 2*element+3)
        mass[nodes, nodes] += kinetic*length*local
    free = np.delete(np.arange(node_count), source)
    reduced = mass[np.ix_(free, free)]
    integral_basis = mass[free] @ np.ones(node_count)
    integral = float(np.sum(mass))
    cross = -slope*integral_basis
    wave_inertia = slope**2*integral
    source_mass = float(mass[source, source]-mass[source, free] @ np.linalg.solve(reduced, mass[free, source]))
    projection = slope**2*source_mass
    recurrence = kinetic*(endpoint_mass(left_lengths)+endpoint_mass(right_lengths))
    coupled = np.block([[reduced, cross[:, None]], [cross[None, :], np.array([[inertia+wave_inertia]])]])
    scalar_force = slope*wave_drive*integral_basis
    raw_wave_force = -wave_drive*wave_inertia
    material_force = inertia*geometric_drive
    acceleration = np.linalg.solve(coupled, np.append(scalar_force, raw_wave_force+material_force))
    force = float(raw_wave_force-cross @ acceleration[:-1]-wave_inertia*acceleration[-1])
    predicted = -projection*(geometric_drive+wave_drive)/(1+projection/inertia)
    wave_source_Euler = float(cross @ acceleration[:-1]+wave_inertia*acceleration[-1]-raw_wave_force)
    return dict(source_mass_schur=source_mass, graded_recurrence_mass=recurrence,
        source_mass_error=abs(source_mass-recurrence), projection_inertia=projection,
        force=force, predicted_force=predicted, force_error=abs(force-predicted),
        source_acceleration=float(acceleration[-1]),
        dust_balance_error=abs(inertia*acceleration[-1]-material_force-force),
        Schur_subtraction_error=abs(wave_inertia-cross @ np.linalg.solve(reduced, cross)-projection),
        wrong_zero_wave_inertia_error=abs(force),
        wave_source_Euler_force_error=abs(force+wave_source_Euler),
        exact_frozen_quadratic_fixture_not_live_solution=True)


def main():
    evidence = EvidenceRun('annular-P2-source-corner-scale-attempt01', __file__)
    try:
        evidence.report.update(github_action=False, subagents_used=False, no_forward_evolution=True,
            full_live_P2_force_convergence_proven=False,
            exact_frozen_mass_law_conditional_local_live_model=True,
            no_Gram_or_live_geometry_term_deleted_from_actual_runs=True)
        inertia, projection, dust_drive, wave_drive = symbolic.symbols('I Q G J', positive=True)
        acceleration = (dust_drive+wave_drive)/(inertia+projection)
        force = wave_drive-projection*acceleration
        evidence.check('exact_source_Schur_force', symbolic.simplify(force-(inertia*wave_drive-projection*dust_drive)/(inertia+projection)) == 0)
        geom_acc, forcing = symbolic.symbols('a_geo B', real=True)
        evidence.check('local_corner_inertial_response', symbolic.simplify(force.subs({dust_drive:inertia*geom_acc,
            wave_drive:-projection*forcing})+projection*(geom_acc+forcing)/(1+projection/inertia)) == 0)
        speed, velocity, acceleration, radial_ratio, time_ratio, slope = symbolic.symbols('s V A C_R_over_K K_t_over_K k', real=True)
        temporal2, mixed, spatial2, temporal1, spatial1 = symbolic.symbols('u_tt u_tx u_xx u_t u_x', real=True)
        transformed = temporal2-2*velocity*mixed+(velocity**2-speed**2)*spatial2-acceleration*(slope+spatial1)
        transformed += time_ratio*(temporal1-velocity*(slope+spatial1))-radial_ratio*(slope+spatial1)
        forcing_coefficient = acceleration+radial_ratio+velocity*time_ratio
        proposed = temporal2-2*velocity*mixed-(speed**2-velocity**2)*spatial2
        proposed -= forcing_coefficient*(slope+spatial1)-time_ratio*temporal1
        evidence.check('curved_moving_coordinate_wave_identity', symbolic.expand(transformed-proposed) == 0)
        time, position, drive = symbolic.symbols('t x D', real=True)
        solutions = [drive*(time**2-(time+position/(speed+velocity))**2)/2,
            drive*(time**2-(time-position/(speed-velocity))**2)/2]
        slopes = []
        for side, solution in enumerate(solutions):
            operator = symbolic.diff(solution, time, 2)-2*velocity*symbolic.diff(solution, time, position)
            operator -= (speed**2-velocity**2)*symbolic.diff(solution, position, 2)
            evidence.check('frozen_convected_corner_'+str(side), symbolic.simplify(operator-drive) == 0)
            evidence.check('zero_source_trace_'+str(side), symbolic.simplify(solution.subs(position, 0)) == 0)
            front = -(speed+velocity)*time if side == 0 else (speed-velocity)*time
            evidence.check('front_C1_matching_'+str(side), symbolic.simplify(solution.subs(position, front)-drive*time**2/2) == 0
                and symbolic.simplify(symbolic.diff(solution, position).subs(position, front)) == 0
                and symbolic.simplify(symbolic.diff(solution, time).subs(position, front)-drive*time) == 0)
            slopes.append(symbolic.diff(solution, position).subs(position, 0))
        radius, kinetic = symbolic.symbols('b K', positive=True)
        pressure_linear = kinetic*(speed**2-velocity**2)*slope*(slopes[0]-slopes[1])
        evidence.check('curved_frozen_continuum_pressure_slope', symbolic.simplify(
            pressure_linear.subs(kinetic, radius**2/speed)+2*radius**2*slope*drive*time) == 0)
        evidence.check('prior_flat_corner_recovered', symbolic.simplify(
            (-2*radius**2*slope*drive).subs(drive, 2*slope/radius)+4*radius*slope**2) == 0)
        configurations = [
            ('uniform', np.full(32, .02), np.full(32, .015)),
            ('uniform_half', np.full(32, .01), np.full(32, .0075)),
            ('graded', np.concatenate([4e-5*2**np.arange(10), np.full(8, .04)]),
                np.concatenate([3e-5*2**np.arange(10), np.full(8, .04)])),
        ]
        for name, left, right in configurations:
            row = frozen_fixture(left, right)
            row['configuration'] = name
            evidence.report['cases'].append(row)
            evidence.check(name+'_graded_mass_recursion', row['source_mass_error'] < 2e-14, row)
            evidence.check(name+'_exact_inertia_force', row['force_error'] < 2e-14 and row['dust_balance_error'] < 2e-14)
            evidence.check(name+'_positive_projection', row['projection_inertia'] > 0 and row['Schur_subtraction_error'] < 2e-14)
            evidence.check(name+'_no_projection_inertia_negative_control', row['wrong_zero_wave_inertia_error'] > 1e-12)
        log = evidence.output/'completion-log.txt'
        with log.open('w', encoding='utf-8') as stream, contextlib.redirect_stdout(stream):
            evidence.complete()
        evidence.own(log, 'outputs')
        evidence.save()
        print(json.dumps(dict(state='complete', checks=len(evidence.report['checks']), cases=evidence.report['cases'])), flush=True)
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
