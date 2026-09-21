from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_decimal_transport_v2_20260919 import decimal_array
from decimal import Decimal, localcontext
import numpy as np


def centered(positive, negative, step):
    with localcontext() as context:
        context.prec = 64
        return np.asarray((decimal_array(positive)-decimal_array(negative))/(2*Decimal.from_float(step)), float)


def extrapolate(coarse, fine):
    return (4*fine-coarse)/3


def source_samples(owner, coordinates, rates, current):
    points, weights = np.polynomial.legendre.leggauss(48)
    labels = np.r_[points/2, owner.labels, 0.]
    cardinal = np.polynomial.chebyshev.chebvander(2*labels, owner.layer_degree) @ owner.layer_rule.inverse
    radius = cardinal @ np.asarray(coordinates[:, -1], float)
    velocity = cardinal @ rates[:, -1]
    values, derivatives = current['solver'].values(current['solution'], radius)
    mass, lapse = values[0], np.exp(values[1])
    metric = 1-2*mass/radius
    clock = np.sqrt(lapse**2-velocity**2/metric)
    return dict(labels=labels, cardinal=cardinal, weights=weights/2*6*(points/2+.5)*(.5-points/2),
        radius=radius, velocity=velocity, mass=mass, lapse=lapse, metric=metric, clock=clock,
        lapse_radial=lapse*derivatives[1], metric_radial=-2*derivatives[0]/radius+2*mass/radius**2,
        proper_velocity=velocity/clock)


def derivative_channels(positive, negative, step):
    result = {'acceleration':centered(positive['rates'], negative['rates'], step)}
    for name in ['lapse', 'metric', 'clock', 'proper_velocity']:
        result[name+'_dot'] = centered(positive[name], negative[name], step)
    return result


def physical_channels(base, derivatives):
    source_acceleration = base['cardinal'] @ derivatives['acceleration'][:, -1]
    velocity, lapse, metric, clock = [base[name] for name in ['velocity', 'lapse', 'metric', 'clock']]
    clock_chain = (lapse*derivatives['lapse_dot']-velocity*source_acceleration/metric+
        velocity**2*derivatives['metric_dot']/(2*metric**2))/clock
    proper = source_acceleration/clock**2-velocity*clock_chain/clock**3
    direct = derivatives['proper_velocity_dot']/clock
    metric_partial_time = derivatives['metric_dot']-velocity*base['metric_radial']
    geodesic = (-metric*lapse*base['lapse_radial']+velocity*metric_partial_time/metric+
        velocity**2*base['metric_radial']/(2*metric))/clock**2
    newton_proxy = -base['mass']/base['radius']**2
    return dict(source_acceleration=source_acceleration, clock_chain=clock_chain,
        proper_acceleration=proper, direct_proper_acceleration=direct,
        metric_partial_time=metric_partial_time, geodesic_acceleration=geodesic,
        geodesic_residual=proper-geodesic, newton_proxy=newton_proxy,
        newton_proxy_residual=proper-newton_proxy,
        omit_clock_response=source_acceleration/clock**2,
        omit_metric_time=(-metric*lapse*base['lapse_radial']+
            velocity**2*base['metric_radial']/(2*metric))/clock**2)


def symbolic_controls(evidence):
    import sympy as sp
    mass, lapse, metric = sp.symbols('mass lapse metric', positive=True)
    velocity, lapse_r, lapse_t, metric_r, metric_t = sp.symbols('velocity lapse_r lapse_t metric_r metric_t', real=True)
    clock = sp.sqrt(lapse**2-velocity**2/metric)
    action = -mass*clock
    momentum = sp.diff(action, velocity)
    force = sp.diff(action, lapse)*lapse_r+sp.diff(action, metric)*metric_r
    coordinate_acceleration = sp.simplify((force-sp.diff(momentum, lapse)*(lapse_t+velocity*lapse_r)-
        sp.diff(momentum, metric)*(metric_t+velocity*metric_r))/sp.diff(momentum, velocity))
    clock_rate = (lapse*(lapse_t+velocity*lapse_r)-velocity*coordinate_acceleration/metric+
        velocity**2*(metric_t+velocity*metric_r)/(2*metric**2))/clock
    proper = sp.simplify(coordinate_acceleration/clock**2-velocity*clock_rate/clock**3)
    geodesic = (-metric*lapse*lapse_r+velocity*metric_t/metric+velocity**2*metric_r/(2*metric))/clock**2
    evidence.check('dust_action_equals_time_dependent_radial_geodesic', sp.simplify(proper-geodesic) == 0)
    radius, mu = sp.symbols('radius mu', positive=True)
    schwarzschild = {metric:1-2*mu/radius, lapse:sp.sqrt(1-2*mu/radius),
        metric_r:2*mu/radius**2, lapse_r:mu/(radius**2*sp.sqrt(1-2*mu/radius)),
        metric_t:0, lapse_t:0}
    evidence.check('test_source_Schwarzschild_proper_radial_acceleration', sp.simplify(proper.subs(schwarzschild)+mu/radius**2) == 0)
    slow = coordinate_acceleration.subs(schwarzschild).subs(velocity, 0)
    evidence.check('test_source_Newton_weak_field_ratio', sp.limit(sp.simplify(slow/(-mu/radius**2)), mu, 0, dir='+') == 1)
    evidence.check('flat_static_clock_zero_radial_acceleration', sp.simplify(proper.subs({metric:1,lapse:1,
        metric_r:0,lapse_r:0,metric_t:0,lapse_t:0})) == 0)
    evidence.report['symbolic_reference'] = dict(coordinate_acceleration=str(coordinate_acceleration),
        proper_acceleration=str(proper), Schwarzschild_result='-mu/radius**2',
        Newton_limit='mu/radius -> 0 and velocity -> 0',
        test_source_metric_prescribed=True, numerical_MTS_match_not_assumed=True, valid_for_claim=False)


def analyze_probes(base, probes, steps):
    derivatives = [derivative_channels(probes[(index, 1)], probes[(index, -1)], step)
        for index, step in enumerate(steps)]
    richardson = [{key:extrapolate(derivatives[index][key], derivatives[index+1][key])
        for key in derivatives[0]} for index in range(2)]
    physical = [physical_channels(base, item) for item in richardson]
    rows = []
    for component, section in [('field', slice(None,-1)), ('source', slice(-1,None))]:
        first, second = [item['acceleration'][:, section] for item in richardson]
        discrepancy = float(np.max(abs(first-second)))
        signal = max(float(np.max(abs(second))), 1e-30)
        rows.append(dict(quantity='coordinate_acceleration_'+component, discrepancy=discrepancy,
            signal=signal, relative_difference=discrepancy/signal,
            tolerance=1e-8+2e-3*signal, passed=bool(discrepancy <= 1e-8+2e-3*signal), valid_for_claim=False))
    for name in ['proper_acceleration', 'geodesic_acceleration']:
        discrepancy = float(np.max(abs(physical[0][name]-physical[1][name])))
        signal = max(float(np.max(abs(physical[1][name]))), 1e-30)
        rows.append(dict(quantity=name, discrepancy=discrepancy, signal=signal,
            relative_difference=discrepancy/signal, tolerance=1e-8+2e-3*signal,
            passed=bool(discrepancy <= 1e-8+2e-3*signal), valid_for_claim=False))
    direct_error = float(np.max(abs(physical[1]['proper_acceleration']-physical[1]['direct_proper_acceleration'])))
    signal = max(float(np.max(abs(physical[1]['proper_acceleration']))), 1e-30)
    rows.append(dict(quantity='proper_chain_versus_direct_velocity_derivative', discrepancy=direct_error,
        signal=signal, relative_difference=direct_error/signal, tolerance=1e-8+2e-3*signal,
        passed=bool(direct_error <= 1e-8+2e-3*signal), valid_for_claim=False))
    return derivatives, richardson, physical, rows
