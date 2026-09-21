from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_covariant_cut_action_20260915 import CurvedCutAction, history_state
import numpy as np
import sympy as sp


def current_data(system, time):
    coordinates, rates, accelerations = history_state(system, time)
    data = system.evaluate(time, coordinates, rates)
    step = 1e-24
    moved_coordinates, moved_rates, unused = history_state(system, time+1j*step)
    moved = system.evaluate(time+1j*step, moved_coordinates, moved_rates)
    momentum_rate = moved['momenta'].imag/step
    wave_momentum_rate = moved['field_momenta'].imag/step
    scalar_euler = momentum_rate[:-1]-data['scalar_covector']
    wave_source_euler = wave_momentum_rate[-1]-system.source_covector(time, coordinates, rates, wave=True)
    dual_rate = system.density_dual_at(time+1j*step, moved_coordinates, moved_rates, data['radius']).imag/step
    node_dual_rate = moved['nodal_dual'].imag/step
    position, velocity = coordinates[-1], rates[-1]
    cell = np.searchsorted(system.radii, position)-1
    left_slope = -coordinates[cell]/(position-system.radii[cell])
    right_slope = coordinates[cell+1]/(system.radii[cell+1]-position)
    source_coefficient = system.coefficient(time, position)
    boundary_dual_jump = -(1+position**4*velocity**2/source_coefficient**2)*(left_slope**2-right_slope**2)/2
    boundary_term = source_coefficient*velocity*boundary_dual_jump
    bulk = np.dot(data['weight']*data['coefficient'], dual_rate)+data['nodal'] @ node_dual_rate
    noether = bulk+boundary_term+scalar_euler @ rates[:-1]+wave_source_euler*velocity
    return dict(data, coordinates=coordinates, rates=rates, accelerations=accelerations,
                scalar_euler=scalar_euler, wave_source_euler=wave_source_euler,
                dual_rate=dual_rate, node_dual_rate=node_dual_rate,
                momentum_rate=momentum_rate, noether_residual=noether,
                omitted_boundary_residual=noether-boundary_term, boundary_term=boundary_term)


def main():
    evidence = EvidenceRun('annular-covariant-cut-canonical-qualification-attempt01', __file__)
    try:
        radius, mass, coupling, dual = sp.symbols('R mu kappa Z', real=True)
        geometry = 1-2*mass/radius
        mass_radial = -coupling*radius**2*geometry*dual
        log_lapse_radial = mass/(radius**2*geometry)-coupling*radius*dual
        log_root_radial = (mass/radius**2-mass_radial/radius)/geometry
        evidence.check('bulk_radial_constraints_give_current_integrating_factor',
                       sp.simplify(log_root_radial-log_lapse_radial-2*coupling*radius*dual) == 0)
        mass_rate, dual_rate = sp.symbols('mu_t Z_t', real=True)
        time_derivative = -coupling*radius**2*(geometry*dual_rate-2*mass_rate*dual/radius)
        current_derivative = 2*coupling*radius*dual*mass_rate-coupling*radius**2*geometry*dual_rate
        evidence.check('conditional_bulk_mass_constraint_propagation_identity', sp.simplify(time_derivative-current_derivative) == 0)
        random = np.random.default_rng(15092026)
        for gram in [False, True]:
            system = CurvedCutAction(17, gram, order=10)
            branch = 'MTS' if gram else 'reference'
            for time in [-.15, 0., .15]:
                coordinates, rates, unused = history_state(system, time)
                data = current_data(system, time)
                direction = .02*random.normal(size=system.count+1)
                step = 2e-5
                action_derivative = (-system.evaluate(time, coordinates+2*step*direction, rates)['action']
                                     +8*system.evaluate(time, coordinates+step*direction, rates)['action']
                                     -8*system.evaluate(time, coordinates-step*direction, rates)['action']
                                     +system.evaluate(time, coordinates-2*step*direction, rates)['action'])/(12*step)
                target = data['scalar_covector'] @ direction[:-1]+system.source_covector(time, coordinates, rates)*direction[-1]
                rate_derivative = (system.evaluate(time, coordinates, rates+step*direction)['action']
                                   -system.evaluate(time, coordinates, rates-step*direction)['action'])/(2*step)
                inertia_schur = data['inertia'][-1, -1]-data['inertia'][-1, :-1] @ np.linalg.solve(data['inertia'][:-1, :-1], data['inertia'][:-1, -1])
                inertia_min = np.linalg.eigvalsh(data['inertia']).min()
                label = branch+str(time)
                evidence.check(label+'_independent_coordinate_and_velocity_action_variations',
                               abs(action_derivative-target) < 2e-9 and abs(rate_derivative-data['momenta'] @ direction) < 2e-9)
                evidence.check(label+'_strict_positive_inertia', inertia_min > 0 and inertia_schur > 0)
                displaced = system.evaluate(time, coordinates, rates.astype(complex)+1e-24j*direction)
                evidence.check(label+'_inertia_is_full_velocity_Hessian',
                               np.max(abs(displaced['momenta'].imag/1e-24-data['inertia'] @ direction)) < 2e-10)
                evidence.check(label+'_source_anchor_Noether_with_moving_interface_jump', abs(data['noether_residual']) < 2e-9)
                evidence.report['cases'].append(dict(branch=branch, time=time,
                    coordinate_variation_error=float(abs(action_derivative-target)),
                    velocity_variation_error=float(abs(rate_derivative-data['momenta'] @ direction)),
                    minimum_inertia=float(inertia_min), source_schur=float(inertia_schur),
                    noether_error=float(abs(data['noether_residual'])),
                    omitted_interface_jump_error=float(abs(data['omitted_boundary_residual']))))
        evidence.check('dropping_interface_jump_fails_both_branches', all(
            max(row['omitted_interface_jump_error'] for row in evidence.report['cases'] if row['branch'] == branch) > 1e-7
            for branch in ['reference', 'MTS']))
        evidence.report.update(scope='Manufactured curved histories; full repaired cut-cell canonical action and off-shell Noether tests.',
                               full_Gram_boundary_lift_retained=True,
                               positive_source_inertia_derived=True,
                               bulk_mass_propagation_identity_conditional_on_radial_and_Euler_equations=True,
                               live_repaired_gravity_evolution_completed=False,
                               arbitrary_spatial_diffeomorphism_invariance_proven=False,
                               unique_parent_boundary_selection_proven=False,
                               full_GR_limit_proven=False, valid_for_physics_claim=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
