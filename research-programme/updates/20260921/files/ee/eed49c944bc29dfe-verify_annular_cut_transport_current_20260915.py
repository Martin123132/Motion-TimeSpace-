from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_covariant_cut_action_v2_20260915 import CurvedCutAction, history, history_state
from qualify_annular_covariant_cut_20260915 import current_data
from scipy.integrate import solve_ivp
import numpy as np


def direction(time, radius):
    envelope = (1-(time/.2)**2)**3
    envelope_time = -6*time/.2**2*(1-(time/.2)**2)**2
    offset = radius-6
    spatial = .1+.05*offset+.02*offset**2
    primitive = .1*offset+.025*offset**2+(.02/3)*offset**3
    return envelope*spatial, envelope, envelope_time, primitive


def links(system, time, position, velocity, targets, amplitude):
    def connection(local_time, radius):
        lapse, root = system.metric(local_time, radius)
        leading = direction(local_time, radius)[0]
        return amplitude*leading/(1-amplitude**2*lapse**2*root**2*leading**2)
    distance = targets-position
    initial = np.concatenate([np.full(len(targets), time),
                              np.full(len(targets), 1-connection(time, position)*velocity)])
    def rhs(fraction, packed):
        transported, jacobian = np.split(packed, 2)
        radius = position+fraction*distance
        value = connection(transported, radius)
        temporal = connection(transported+1e-24j, radius).imag/1e-24
        return np.concatenate([distance*value, distance*temporal*jacobian])
    solution = solve_ivp(rhs, (0., 1.), initial, method='DOP853', rtol=2e-12, atol=2e-14, max_step=.2)
    if not solution.success:
        raise RuntimeError(solution.message)
    transported, jacobian = np.split(solution.y[:, -1], 2)
    if np.min(jacobian) <= 0:
        raise ValueError('Horizontal leaf clock became singular.')
    return transported, jacobian


def shifted_action(system, time, amplitude):
    coordinates, rates, unused = history_state(system, time)
    position, velocity = coordinates[-1], rates[-1]
    radius, unused_weight = system.mesh(position)
    targets = np.concatenate([radius, system.radii])
    transported, jacobian = links(system, time, position, velocity, targets, amplitude)
    lapse, root = system.metric(transported, targets)
    leading = direction(transported, targets)[0]
    coefficient = jacobian*targets**2*lapse*root*(1-amplitude**2*lapse**2*root**2*leading**2)
    scalar, scalar_rate, unused = history(transported[len(radius):], system.radii)
    coordinates[:-1] = scalar
    rates[:-1] = jacobian[len(radius):]*scalar_rate
    source_lapse, source_root = system.metric(time, position)
    shift = amplitude*source_lapse**2*source_root**2*direction(time, position)[0]
    pulled = (coefficient[:len(radius)], coefficient[len(radius):], source_lapse, source_root, shift)
    return system.evaluate(time, coordinates, rates, pulled)['action']


def variation_pair(system, time):
    data = current_data(system, time)
    coordinates, rates = data['coordinates'], data['rates']
    position, velocity = coordinates[-1], rates[-1]
    targets = np.concatenate([data['radius'], system.radii])
    source_direction, envelope, envelope_time, primitive_source = direction(time, position)
    primitive = direction(time, targets)[3]
    variation = envelope*(primitive-primitive_source)
    variation_time = envelope_time*(primitive-primitive_source)-velocity*source_direction
    missing_anchor_time = envelope_time*(primitive-primitive_source)
    points = len(data['radius'])
    coefficient = np.concatenate([data['coefficient'], data['nodal']])
    coefficient_time = system.coefficient(time+1e-24j, targets).imag/1e-24
    dual_weight = np.concatenate([data['weight']*data['density_dual'], data['nodal_dual']])
    scalar_variation = rates[:-1]*variation[points:]
    scalar_rate_variation = data['accelerations'][:-1]*variation[points:]+rates[:-1]*variation_time[points:]
    raw = data['scalar_covector'] @ scalar_variation+data['momenta'][:-1] @ scalar_rate_variation
    raw += dual_weight @ (coefficient_time*variation+coefficient*variation_time)
    source_lapse, source_root = system.metric(time, position)
    source_term = data['material_momentum']*source_lapse**2*source_root**2*source_direction
    raw += source_term
    adjoint = -data['scalar_euler'] @ scalar_variation
    adjoint -= np.dot(data['weight']*data['coefficient']*data['dual_rate'], variation[:points])
    adjoint -= np.dot(data['nodal']*data['node_dual_rate'], variation[points:])
    adjoint += source_term
    wrong = raw+data['momenta'][:-1] @ (rates[:-1]*(missing_anchor_time-variation_time)[points:])
    wrong += dual_weight @ (coefficient*(missing_anchor_time-variation_time))
    return float(raw), float(adjoint), float(wrong)


def time_pullback(system, time):
    coordinates, rates, unused = history_state(system, time)
    position, velocity = coordinates[-1], rates[-1]
    offset = position-6
    scale = np.exp(.08*offset)
    displacement = .1*offset+.02*offset**2
    new_time = (time-displacement)/scale
    radial_time = .08*scale*new_time+.1+.04*offset
    source_clock = scale/(1-velocity*radial_time)
    radius, unused_weight = system.mesh(position)
    targets = np.concatenate([radius, system.radii, [position]])
    offsets = targets-6
    local_scale = np.exp(.08*offsets)
    local_time = (time-(.1*offsets+.02*offsets**2))/local_scale
    local_radial = .08*local_scale*local_time+.1+.04*offsets
    lapse, root = system.metric(time, targets)
    metric_rr = 1/root**2-lapse**2*local_radial**2
    cross = -local_scale*lapse**2*local_radial
    shifted = cross/metric_rr
    new_root = 1/np.sqrt(metric_rr)
    new_lapse = np.sqrt(local_scale**2*lapse**2+cross**2/metric_rr)
    new_coefficient = targets**2*new_lapse*new_root*(1-shifted**2/(new_lapse**2*new_root**2))
    pulled_coefficient = source_clock/local_scale*new_coefficient
    pulled = (pulled_coefficient[:len(radius)], pulled_coefficient[len(radius):-1], new_lapse[-1], new_root[-1], shifted[-1])
    actual = system.evaluate(new_time, coordinates, rates*source_clock, pulled)
    original = system.evaluate(time, coordinates, rates)
    bad_pulled = (new_coefficient[:len(radius)], new_coefficient[len(radius):-1], new_lapse[-1], new_root[-1], shifted[-1])
    wrong = system.evaluate(new_time, coordinates, rates*source_clock, bad_pulled)
    return dict(action_error=float(abs(actual['action']-source_clock*original['action'])),
                proper_clock_error=float(abs(actual['clock']-source_clock*original['clock'])),
                omitted_link_J_error=float(abs(wrong['action']-source_clock*original['action'])),
                minimum_chart_rr=float(metric_rr.min()), maximum_nonzero_shift=float(np.max(abs(shifted))))


def main():
    evidence = EvidenceRun('annular-cut-transport-and-current-attempt01', __file__)
    try:
        for gram in [False, True]:
            system = CurvedCutAction(17, gram, order=10)
            branch = 'MTS' if gram else 'reference'
            for time in [-.15, 0., .15]:
                row = dict(branch=branch, time=time, **time_pullback(system, time))
                evidence.check(branch+str(time)+'_full_moving_action_time_covariance',
                               row['action_error'] < 2e-11 and row['proper_clock_error'] < 2e-12
                               and row['minimum_chart_rr'] > 0 and row['maximum_nonzero_shift'] > .01)
                evidence.check(branch+str(time)+'_untransported_density_control_fails', row['omitted_link_J_error'] > 1e-7)
                evidence.report['cases'].append(row)
            points, weights = np.polynomial.legendre.leggauss(20)
            times, weights = .2*points, .2*weights
            variations = np.array([variation_pair(system, time) for time in times])
            raw, adjoint, wrong = weights @ variations
            step = .0002
            action = {amplitude: sum(weight*shifted_action(system, time, amplitude) for time, weight in zip(times, weights))
                      for amplitude in [-2*step, -step, step, 2*step]}
            difference = (-action[2*step]+8*action[step]-8*action[-step]+action[-2*step])/(12*step)
            evidence.check(branch+'_independent_nonzero_shift_action_difference', abs(difference-raw) < 2e-9,
                           dict(difference=float(difference), derived=float(raw), error=float(abs(difference-raw))))
            evidence.check(branch+'_bulk_current_adjoint_including_moving_anchor', abs(raw-adjoint) < 2e-9,
                           dict(raw=float(raw), adjoint=float(adjoint), error=float(abs(raw-adjoint))))
            evidence.check(branch+'_frozen_source_anchor_control_fails', abs(wrong-raw) > 1e-7, float(abs(wrong-raw)))
        evidence.report.update(scope='Full repaired curved-history action, physical time pullback, and independent P=0 shift-current first variation.',
                               finite_nonzero_shift_action_used=True,
                               old_trace_multiplier_absent=True,
                               moving_anchor_factor_retained=True,
                               time_boundary_terms_vanish_by_compact_variation=True,
                               canonical_parent_factor='delta c = kappa U/N delta P; delta beta = kappa N U^3 delta P at P=0.',
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
