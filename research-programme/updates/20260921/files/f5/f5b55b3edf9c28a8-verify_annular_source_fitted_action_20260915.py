from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_source_fitted_action_20260915 import SourceFittedAction
from annular_sparse_repaired_cut_20260915 import SparseRepairedCut
from scipy.linalg import solve_banded
import numpy as np
import sympy as sp


def manufactured(system, time, position0=6.03, velocity0=.06):
    acceleration = .02
    position = position0+velocity0*time+acceleration*time**2/2
    velocity = velocity0+acceleration*time
    radius, jacobian, displacement = system.mapping(system.radii, position)
    offset = radius-position
    left = system.radii < system.anchor
    slope = np.where(left, .015+.003*time, -.01+.002*time)
    slope_rate = np.where(left, .003, .002)
    curvature = np.where(left, .004, -.003)
    cubic = np.where(left, -.002, .001)
    scalar = slope*offset+curvature*offset**2/2+cubic*offset**3/6
    gradient = slope+curvature*offset+cubic*offset**2/2
    rates = slope_rate*offset+gradient*(displacement-1)*velocity
    return np.append(scalar, position), np.append(rates, velocity)


def continuum_source_identity(system, time=0., position0=6.03, velocity0=.06):
    position = position0+velocity0*time+.01*time**2
    velocity = velocity0+.02*time
    acceleration = .02
    points, weights = np.polynomial.legendre.leggauss(32)
    bulk = 0.
    for side, (lower, upper) in enumerate([(system.radii[0], position), (position, system.radii[-1])]):
        radius = (lower+upper)/2+(upper-lower)*points/2
        measure = weights*(upper-lower)/2
        displacement = (radius-lower)/(upper-lower) if side == 0 else (upper-radius)/(upper-lower)
        offset = radius-position
        slope = [.015+.003*time, -.01+.002*time][side]
        slope_rate = [.003, .002][side]
        curvature, cubic = [.004, -.003][side], [-.002, .001][side]
        gradient = slope+curvature*offset+cubic*offset**2/2
        second = curvature+cubic*offset
        temporal = slope_rate*offset-velocity*gradient
        second_time = -2*velocity*slope_rate-acceleration*gradient+velocity**2*second
        coefficient = system.coefficient(time, radius)
        coefficient_radial = system.coefficient(time, radius+1e-24j).imag/1e-24
        coefficient_time = system.coefficient(time+1e-24j, radius).imag/1e-24
        temporal_coefficient = radius**4/coefficient
        temporal_coefficient_time = -radius**4*coefficient_time/coefficient**2
        euler = coefficient_radial*gradient+coefficient*second-temporal_coefficient*second_time-temporal_coefficient_time*temporal
        bulk += np.dot(measure, displacement*gradient*euler)
    coefficient = system.coefficient(time, position)
    pressure = .5*(coefficient-position**4*velocity**2/coefficient)*((.015+.003*time)**2-(-.01+.002*time)**2)
    return float(pressure-bulk), float(pressure), float(bulk)


def main():
    evidence = EvidenceRun('annular-source-fitted-action-qualification-attempt01', __file__)
    try:
        inner, outer, anchor, reference, position, velocity = sp.symbols('a d bstar r b V', real=True)
        left_map = inner+(position-inner)*(reference-inner)/(anchor-inner)
        right_map = outer-(outer-position)*(outer-reference)/(outer-anchor)
        for label, mapping in [('left', left_map), ('right', right_map)]:
            jacobian, displacement = sp.diff(mapping, reference), sp.diff(mapping, position)
            evidence.check(label+'_geometric_conservation_identity', sp.simplify(sp.diff(jacobian, position)*velocity-sp.diff(displacement*velocity, reference)) == 0)
            evidence.check(label+'_source_trace_mapping', sp.simplify(mapping.subs(reference, anchor)-position) == 0)
        temporal, radial, temporal_coefficient, coefficient, jacobian, displacement = sp.symbols('phit phir A C J k', real=True)
        action = (temporal_coefficient*jacobian*(temporal-displacement*velocity*radial/jacobian)**2-coefficient*radial**2/jacobian)/2
        evidence.check('full_global_field_source_momentum_derived', sp.simplify(sp.diff(action, velocity)+temporal_coefficient*displacement*radial*(temporal-displacement*velocity*radial/jacobian)) == 0)
        evidence.check('physical_wave_energy_by_full_Legendre_transform', sp.simplify(temporal*sp.diff(action, temporal)+velocity*sp.diff(action, velocity)-action-(temporal_coefficient*jacobian*(temporal-displacement*velocity*radial/jacobian)**2+coefficient*radial**2/jacobian)/2) == 0)
        for gram in [False, True]:
            branch = 'MTS' if gram else 'reference'
            system = SourceFittedAction(33, gram)
            coordinates, rates = manufactured(system, 0.)
            coordinates[-1] = system.anchor
            rates[-1] = 0.
            old = SparseRepairedCut(33, gram, order=10, background_mass=.7)
            current, previous = system.evaluate(0., coordinates, rates), old.evaluate(0., coordinates, rates)
            evidence.check(branch+'_static_action_and_field_blocks_match', max(abs(current['action']-previous['action']), np.max(abs(current['scalar_covector']-previous['scalar_covector'])), np.max(abs(current['mass_bands']-previous['mass_bands']))) < 2e-13)
            evidence.check(branch+'_all_original_Gram_rows_retained', system.original.shape == old.original.shape and (system.original != old.original).nnz == 0)
            for location in [6.03, 6.04999999, 6.05, 6.05000001, 6.15]:
                coordinates, rates = manufactured(system, 0., location)
                data = system.evaluate(0., coordinates, rates)
                analytic = np.append(data['scalar_covector'], system.source_covector(0., coordinates, rates))
                coordinate_gradient, rate_gradient = [], []
                step = 1e-24
                for index in range(system.count+1):
                    changed = coordinates.astype(complex)
                    changed[index] += step*1j
                    coordinate_gradient.append(system.evaluate(0., changed, rates)['action'].imag/step)
                    changed_rate = rates.astype(complex)
                    changed_rate[index] += step*1j
                    rate_gradient.append(system.evaluate(0., coordinates, changed_rate)['action'].imag/step)
                inverse_cross = solve_banded((1, 1), data['mass_bands'], data['cross'])
                schur = data['source_inertia']-data['cross'] @ inverse_cross
                lapse, root = system.metric(0., location)
                proper_inertia = system.source_mass*lapse**2/(root**2*data['clock']**3)
                acceleration = system.acceleration(0., coordinates, rates)
                changed = system.evaluate(step*1j, coordinates+step*1j*rates, rates+step*1j*acceleration)
                residual = np.max(abs(changed['momenta'].imag/step-analytic))
                energy_rate = system.energy(0., coordinates+step*1j*rates, rates+step*1j*acceleration).imag/step
                row = dict(branch=branch, position=location, covector_error=float(np.max(abs(np.asarray(coordinate_gradient)-analytic))),
                           momentum_error=float(np.max(abs(np.asarray(rate_gradient)-data['momenta']))), schur=float(schur),
                           proper_inertia=float(proper_inertia), euler_residual=float(residual), energy_derivative=float(energy_rate),
                           minimum_jacobian=float(min(data['jacobian'])), source_field_momentum=float(data['field_momenta'][-1]))
                evidence.report['cases'].append(row)
                evidence.check(branch+str(location)+'_action_derivatives', row['covector_error'] < 3e-12 and row['momentum_error'] < 3e-13, row)
                evidence.check(branch+str(location)+'_positive_Schur_and_mapping', schur >= proper_inertia-2e-13 and row['minimum_jacobian'] > 0, row)
                evidence.check(branch+str(location)+'_full_EL_and_energy_identity', residual < 2e-11 and abs(energy_rate) < 2e-13, row)
            errors = []
            for count in [33, 65, 129, 257, 513, 1025]:
                refined = SourceFittedAction(count, gram)
                coordinates, rates = manufactured(refined, .12, 6.05)
                shifted_coordinates, shifted_rates = manufactured(refined, .12+1e-24j, 6.05)
                momentum_rate = refined.evaluate(.12+1e-24j, shifted_coordinates, shifted_rates)['field_momenta'][-1].imag/1e-24
                coordinate_force = refined.source_covector(.12, coordinates, rates, wave=True)
                target, pressure, bulk = continuum_source_identity(refined, .12, 6.05)
                error = abs(coordinate_force-momentum_rate-target)
                errors.append(float(error))
                evidence.report['cases'].append(dict(branch=branch, count=count, offshell_force=float(coordinate_force-momentum_rate),
                    continuum_offshell=target, boundary_pressure=pressure, bulk_euler_projection=bulk,
                    source_field_momentum_derivative=float(momentum_rate), error=float(error)))
            evidence.check(branch+'_offshell_source_chain_rule_converges', errors[-1] < 2e-7 and errors[-1] < errors[-2]/1.6, errors)
        evidence.report.update(scope='Derived source-fitted pullback and fixed-background variational discretization; not yet continuously averaged live gravity.',
            source_can_cross_old_physical_grid_nodes_without_chart_change=True,
            all_Gram_rows_retained=True, finite_Gram_extension_parent_uniqueness_proven=False,
            source_field_momentum_global_and_retained=True, new_chart_is_not_same_finite_cut_state=True,
            on_shell_pressure_identity_conditional_on_scalar_equation=True, live_source_fitted_geometry_qualified=False,
            original_live_benchmark_replaced=False,
            contextual_primary_source='https://arxiv.org/abs/2009.12768',
            contextual_source_use='ALE mapping precedent only; its DG stability theorem is not a theorem for this action.')
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
