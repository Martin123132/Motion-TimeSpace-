import numpy as np

from annular_compatible_h_evolution_20260914 import regular_chart_constants
from annular_covariant_scalar_action_20260912 import full_spatial_factors
from annular_gram_joint_action_20260909 import gram_matrices
from annular_finite_width_bulk_current_20260913 import shape_weight


def quadrature(order=32):
    points, weights = np.polynomial.legendre.leggauss(order)
    offsets = np.concatenate([-.25+.25*points, .25+.25*points])
    weights = np.concatenate([.25*weights, .25*weights])*shape_weight(offsets, 'beta22')
    return offsets, weights


def phase_direction(system, direction, offsets):
    values = system.grid.evaluate(system.grid.coefficients(system.unpack(direction)[0]), offsets)
    free = len(system.radii)-1
    zero = np.zeros(len(offsets), dtype=values.dtype)
    return np.column_stack([values[:, :free], zero]), np.column_stack([values[:, free:2*free], zero])


def fixed_source_direction(system, state):
    values, unused_clock = system.unpack(state)
    result = np.zeros_like(values)
    free = len(system.radii)-1
    result[:, :2*free] = values[:, :2*free]
    return system.pack(result, 0.)


def density_energy(system, direction, extra=False, order=32):
    offsets, weights = quadrature(order)
    scalar, momentum = phase_direction(system, direction, offsets)
    radius = system.radii[None, :]+system.width*offsets[:, None]
    factors, sampling = gram_matrices(len(system.radii)) if extra else full_spatial_factors(len(system.radii), False)
    amplitude = scalar @ factors.T
    local = np.sum((radius**2 @ sampling.T)*amplitude**2, axis=1)/system.spacing
    if not extra:
        local += np.sum(system.node_weights*momentum**2/radius**2, axis=1)
    return .5*weights @ local


def outer_data(geometry):
    data = geometry.metric(np.array([geometry.edges[-1]]))
    return data['mu'][0]/geometry.system.coupling, data['N'][0]/data['U'][0]


def mass_gradient(system, geometry, direction, order=32):
    offsets, weights = quadrature(order)
    data = geometry.layer(offsets)
    scalar, momentum = phase_direction(system, direction, offsets)
    unused_mass, outer_clock = outer_data(geometry)
    coefficient = data['N']*data['U']/outer_clock
    local = np.sum(system.node_weights*coefficient*data['p']*momentum/data['R']**2, axis=1)
    local += np.sum((data['R']**2*coefficient @ system.sampling.T)*data['A']*(scalar @ system.factors.T), axis=1)/system.spacing
    return weights @ local


def mass_hessian(system, time, state, direction, test, order=32):
    step = 1e-20
    geometry = system.geometry(time, state+1j*step*direction)
    return mass_gradient(system, geometry, test, order).imag/step


def uniform_constants():
    inherited = regular_chart_constants()
    radius, ceiling, coupling, reservoir, seed, floor = 4.9, 6.1, .1, .003, .8, .5
    mass = inherited['full_support_mass_upper_bound']
    physical_floor = inherited['F_lower_if_exact_mass_conserved']
    energy = (mass-seed)/(coupling*physical_floor)
    connecting_floor = 1-2*(seed+coupling*(energy+reservoir))/radius
    exponent = coupling*(2*energy/radius+reservoir/(radius*np.sqrt(floor)))
    weight = floor*np.exp(-exponent)
    outer_clock = np.exp(exponent)
    second = 4*coupling/radius+coupling**2*reservoir/(radius**2*floor**1.5)
    third = 6*coupling*second/radius+3*coupling**2*reservoir*second/(radius**2*floor**1.5)+3*coupling**3*reservoir/(radius**3*floor**2.5)
    log_clock = 2*coupling/radius+coupling**2*reservoir/(radius**2*floor**1.5)
    coercivity = weight-2*second*energy
    phase_second = 2+4*second*energy
    phase_third = 8*third*energy**1.5+12*second*np.sqrt(energy)
    delta_rate = outer_clock*(.5*phase_third+2*log_clock*phase_second*np.sqrt(energy))
    extra_rate = outer_clock*(2*second*np.sqrt(energy)+2*log_clock*phase_second*np.sqrt(energy))
    relative_rate = max(delta_rate/coercivity, extra_rate/weight)
    forcing = outer_clock/np.sqrt(weight)
    tangent_rate = .5*phase_third/coercivity**1.5+4*log_clock*np.sqrt(energy/coercivity)
    bump_first = 8/(.3*np.e)
    bump_second = (1024/np.e**3+216/np.e**2+8/np.e)/.3**2
    metric_first = 2*mass/(radius**2*physical_floor)
    q_first = .004*(bump_first+metric_first)
    stiffness_first = 2*ceiling+ceiling**2*metric_first
    momentum_rate_max = ceiling**2*.02*bump_second+stiffness_first*.02*bump_first
    reference_rate_initial = .5*ceiling**2*q_first**2+.5*momentum_rate_max**2/radius**2
    tangent_initial = (1+2*second*energy)*reference_rate_initial
    lifespan = 2/(tangent_rate*np.sqrt(tangent_initial))
    return dict(radius_lower=radius, radius_upper=ceiling, coupling=coupling, reservoir_L1=reservoir,
                actual_mass_ceiling=mass, actual_F_floor=physical_floor, energy_ceiling=energy,
                connecting_F_floor=connecting_floor, chosen_F_floor=floor, weight_lower=weight,
                outer_clock_upper=outer_clock, density_second=second, density_third=third,
                log_clock_Lipschitz=log_clock, coercivity=coercivity, phase_second=phase_second,
                phase_third=phase_third, delta_rate=delta_rate, extra_rate=extra_rate,
                relative_rate=relative_rate, forcing_coefficient=forcing, tangent_rate=tangent_rate,
                bump_first_bound=bump_first, bump_second_bound=bump_second,
                source_free_metric_first_bound=metric_first, reference_initial_energy_bound=reference_rate_initial,
                tangent_initial_energy_bound=tangent_initial, uniform_tangent_comparison_time=lifespan)

