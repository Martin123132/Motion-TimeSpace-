import math

import numpy as np
from scipy.integrate import solve_ivp

from annular_constrained_mass_relative_energy_20260914 import (
    uniform_constants, quadrature, phase_direction, density_energy)
from annular_finite_width_bulk_current_20260913 import shape_weight


def extended_constants():
    values = uniform_constants()
    radius, ceiling = values['radius_lower'], values['radius_upper']
    coupling, source, floor = values['coupling'], values['reservoir_L1'], values['chosen_F_floor']
    energy, mu = values['energy_ceiling'], values['coercivity']
    second, third = values['density_second'], values['density_third']
    fourth = 8*coupling*third/radius+coupling**2*source*(4*third+3*second**2)/(radius**2*floor**1.5)
    fourth += 18*coupling**3*source*second/(radius**3*floor**2.5)+15*coupling**4*source/(radius**4*floor**3.5)
    phase_fourth = 16*fourth*energy**2+48*third*energy+12*second
    clock_density_second = coupling**2*source*second/(radius**2*floor**1.5)+3*coupling**3*source/(radius**3*floor**2.5)
    clock_first = 2*values['log_clock_Lipschitz']*np.sqrt(energy)
    clock_second = 4*clock_density_second*energy+2*values['log_clock_Lipschitz']
    clock_mixed = clock_second+clock_first**2
    phase_second, phase_third = values['phase_second'], values['phase_third']
    beta = phase_second/2
    stabilizer = (phase_third**2/(2*mu)+1)/mu**2
    coefficient_square = 2.5*phase_third+3*clock_first*phase_second
    coefficient_cross = phase_fourth+3*clock_first*phase_third+clock_mixed*phase_second
    coefficient_quartic = clock_mixed*phase_third+2*stabilizer*values['tangent_rate']*beta**2.5
    higher_rate = 2*coefficient_square/mu+coefficient_cross*(1/mu+.5)+coefficient_quartic
    coefficient_min = radius**2*values['weight_lower']
    coefficient_max = ceiling**2*values['outer_clock_upper']
    length = ceiling-radius
    coefficient_variation = coefficient_max*(2*np.log(ceiling/radius)+
        2*values['actual_mass_ceiling']*length/(radius**2*floor)+coupling*source/(radius*np.sqrt(floor)))
    log_rate = (2*coupling/(radius*floor)+2*values['log_clock_Lipschitz'])*2*np.sqrt(energy)
    log_rate_variation = 2*coupling*np.sqrt(energy)*(2*length/(radius**2*floor**2)+coupling*source/(radius**2*floor**1.5))
    coefficient_rate_variation = coefficient_max*log_rate_variation+log_rate*coefficient_variation
    flux_acceleration = np.sqrt(2)*ceiling*(1/coefficient_min+coefficient_variation/coefficient_min**2)
    flux_velocity = np.sqrt(2)*ceiling*(coefficient_max*log_rate/coefficient_min**2+
        coefficient_rate_variation/coefficient_min**2+2*coefficient_max*log_rate*coefficient_variation/coefficient_min**3)
    forcing = ceiling**2/4*(flux_acceleration*np.sqrt(2/mu)+flux_velocity)**2
    bump_first, bump_second = values['bump_first_bound'], values['bump_second_bound']
    bump_third = (8*6**6/np.e**5+48*5**5/np.e**4+60*4**4/np.e**3+24*3**3/np.e**2)/.3**3
    mass = values['actual_mass_ceiling']
    physical_floor = values['actual_F_floor']
    metric_first = values['source_free_metric_first_bound']
    density_max = 1.5*ceiling**2*((.02*bump_first)**2+.004**2)
    mass_first = coupling*density_max
    metric_second = metric_first**2+2*mass_first/(radius**2*physical_floor**2)
    metric_second += 4*mass/(radius**3*physical_floor)+4*mass**2/(radius**4*physical_floor**2)
    stiffness_first = 2*ceiling+ceiling**2*metric_first
    stiffness_second = 2+4*ceiling*metric_first+ceiling**2*metric_second
    momentum_rate = ceiling**2*.02*bump_second+stiffness_first*.02*bump_first
    momentum_rate_gradient = ceiling**2*.02*bump_third+2*stiffness_first*.02*bump_second+stiffness_second*.02*bump_first
    velocity_initial = np.sqrt(values['reference_initial_energy_bound'])
    metric_rate = log_rate*velocity_initial
    mass_rate = 2*coupling*np.sqrt(energy)*velocity_initial
    metric_rate_gradient = metric_rate*metric_first+2*mass_rate/(radius**2*physical_floor**2)
    q_first = .004*(bump_first+metric_first)
    q_second = .004*(bump_second+2*metric_first*bump_first+metric_second)
    acceleration_scalar_gradient = .004*(metric_rate_gradient+metric_rate*bump_first)
    acceleration_scalar_gradient += (metric_first/radius**2+2/radius**3)*momentum_rate+momentum_rate_gradient/radius**2
    stiffness_rate = ceiling**2*metric_rate
    stiffness_rate_gradient = 2*ceiling*metric_rate+ceiling**2*metric_rate_gradient
    momentum_acceleration = ceiling**2*q_second+stiffness_first*q_first
    momentum_acceleration += stiffness_rate*.02*bump_second+stiffness_rate_gradient*.02*bump_first
    initial_acceleration = .5*ceiling**2*acceleration_scalar_gradient**2+.5*momentum_acceleration**2/radius**2
    initial_higher = beta*initial_acceleration+phase_third*values['reference_initial_energy_bound']*np.sqrt(initial_acceleration)
    initial_higher += stabilizer*values['tangent_initial_energy_bound']**2
    return dict(values, density_fourth=fourth, phase_fourth=phase_fourth, clock_density_second=clock_density_second,
        clock_phase_first=clock_first, clock_phase_second=clock_second, clock_phase_mixed=clock_mixed,
        higher_stabilizer=stabilizer,higher_rate=higher_rate,coefficient_min=coefficient_min,coefficient_max=coefficient_max,
        coefficient_variation_bound=coefficient_variation,log_rate_bound_multiplier=log_rate,
        log_rate_variation_multiplier=log_rate_variation,coefficient_rate_variation_multiplier=coefficient_rate_variation,
        flux_acceleration_constant=flux_acceleration,flux_velocity_constant=flux_velocity,
        forcing_h_Q_constant=forcing,bump_third_bound=bump_third,initial_acceleration_energy_bound=initial_acceleration,
        initial_higher_energy_bound=initial_higher)


class MassJet:
    def __init__(self, system, geometry, first_direction, second_direction):
        self.indices = [(first,total-first) for total in range(5) for first in range(total,-1,-1)]
        self.lookup = {index:place for place,index in enumerate(self.indices)}
        left, right, target = [], [], []
        for first, powers in enumerate(self.indices):
            for second, other in enumerate(self.indices):
                added = tuple(powers[index]+other[index] for index in range(2))
                if sum(added)<=4:
                    left.append(first)
                    right.append(second)
                    target.append(self.lookup[added])
        self.left,self.right,self.target = np.array(left),np.array(right),np.array(target)
        self.size = len(self.indices)
        self.clock_indices = [self.lookup[index] for index in [(1,0),(0,1),(2,0)]]
        seed = np.zeros(self.size-1+len(self.clock_indices))
        for piece in geometry.pieces:
            if piece['gap']:
                continue
            lower,upper = piece['lower'],piece['upper']
            node = int(np.argmin(abs(system.radii-(lower+upper)/2)))
            rule = system.radial_rule
            radii = (lower+upper)/2+(upper-lower)*rule.points/2
            offsets = (radii-system.radii[node])/system.width
            data = geometry.scalar(offsets)
            scalar_first,momentum_first = phase_direction(system,first_direction,offsets)
            scalar_second,momentum_second = phase_direction(system,second_direction,offsets)
            amplitude_first = scalar_first @ system.factors.T
            amplitude_second = scalar_second @ system.factors.T
            measure = shape_weight(offsets,system.shape)/system.width
            density = np.zeros((len(radii),self.size))
            factor_weight = system.sampling[:,node]
            density[:,0] = data['potential'][:,node]
            density[:,self.lookup[(1,0)]] = radii**2*((data['A']*amplitude_first) @ factor_weight)/system.spacing
            density[:,self.lookup[(0,1)]] = radii**2*((data['A']*amplitude_second) @ factor_weight)/system.spacing
            density[:,self.lookup[(2,0)]] = radii**2*(amplitude_first**2 @ factor_weight)/(2*system.spacing)
            density[:,self.lookup[(1,1)]] = radii**2*((amplitude_first*amplitude_second) @ factor_weight)/system.spacing
            density[:,self.lookup[(0,2)]] = radii**2*(amplitude_second**2 @ factor_weight)/(2*system.spacing)
            reservoir = np.zeros(len(radii))
            if node<len(system.radii)-1:
                weight = system.node_weights[node]/radii**2
                density[:,0] += weight*data['p'][:,node]**2/2
                density[:,self.lookup[(1,0)]] += weight*data['p'][:,node]*momentum_first[:,node]
                density[:,self.lookup[(0,1)]] += weight*data['p'][:,node]*momentum_second[:,node]
                density[:,self.lookup[(2,0)]] += weight*momentum_first[:,node]**2/2
                density[:,self.lookup[(1,1)]] += weight*momentum_first[:,node]*momentum_second[:,node]
                density[:,self.lookup[(0,2)]] += weight*momentum_second[:,node]**2/2
            else:
                reservoir = data['energy']*measure
            density *= measure[:,None]
            coefficients = rule.inverse @ np.column_stack([density,reservoir])

            def equation(radius, values):
                source_values = np.polynomial.chebyshev.chebval((2*radius-lower-upper)/(upper-lower),coefficients)
                root = geometry.metric(np.array([radius]))['U'][0]
                scaled = np.zeros(self.size)
                scaled[1:] = -2*values[:self.size-1]/(radius*root**2)
                root_series = np.zeros(self.size)
                inverse_series = np.zeros(self.size)
                power = np.zeros(self.size)
                power[0] = 1.
                root_factor,inverse_factor = 1.,1.
                for order in range(5):
                    root_series += root_factor*power
                    inverse_series += inverse_factor*power
                    power = self.multiply(power,scaled)
                    root_factor *= (.5-order)/(order+1)
                    inverse_factor *= (-.5-order)/(order+1)
                geometry_series = scaled.copy()
                geometry_series[0] = 1.
                mass_rate = system.coupling*(root**2*self.multiply(geometry_series,source_values[:self.size])+
                    root*root_series*source_values[-1])
                clock_rate = np.zeros(len(self.clock_indices))
                if lower>=system.radii[-1]-1e-12:
                    full_clock = system.coupling*(2*source_values[:self.size]+source_values[-1]*inverse_series/root)/radius
                    clock_rate = full_clock[self.clock_indices]
                return np.concatenate([mass_rate[1:],clock_rate])

            solution = solve_ivp(equation,(lower,upper),seed,method='DOP853',rtol=3e-11,atol=3e-13,max_step=(upper-lower)/4)
            if not solution.success:
                raise RuntimeError(solution.message)
            seed = solution.y[:,-1]
        self.mass = np.append(0.,seed[:self.size-1])/system.coupling
        self.clock = {index:seed[self.size-1+position]*math.factorial(self.indices[index][0])*math.factorial(self.indices[index][1])
                      for position,index in enumerate(self.clock_indices)}

    def multiply(self, first, second):
        return np.bincount(self.target,weights=first[self.left]*second[self.right],minlength=self.size)

    def derivative(self, first, second):
        return self.mass[self.lookup[(first,second)]]*math.factorial(first)*math.factorial(second)

    def clock_derivative(self, first, second):
        return self.clock[self.lookup[(first,second)]]


def reference_acceleration(system,time,state):
    velocity = system.rhs(time,state)
    acceleration = system.rhs(time,state+1j*1e-20*velocity).imag/1e-20
    return velocity,acceleration


def higher_energy(jet, constants):
    tangent = .5*jet.derivative(2,0)
    value = .5*jet.derivative(0,2)+jet.derivative(2,1)+constants['higher_stabilizer']*tangent**2
    clock_first = jet.clock_derivative(1,0)
    clock_mixed = jet.clock_derivative(2,0)+jet.clock_derivative(0,1)-clock_first**2
    tangent_rate = .5*jet.derivative(3,0)+2*clock_first*tangent
    terms = np.array([
        2.5*jet.derivative(1,2),jet.derivative(3,1),2*clock_first*jet.derivative(2,1),
        clock_mixed*jet.derivative(3,0),2*clock_first*jet.derivative(0,2),
        clock_mixed*jet.derivative(1,1),2*constants['higher_stabilizer']*tangent*tangent_rate])
    return float(value),terms


def flux_control(system,time,state,velocity,acceleration,constants,order=32):
    offsets,weights = quadrature(order)
    geometry = system.geometry(time,state)
    data = geometry.layer(offsets)
    moved = system.geometry(time,state+1j*1e-20*velocity).layer(offsets)
    q_value,p_rate = phase_direction(system,velocity,offsets)
    unused_scalar,p_acceleration = phase_direction(system,acceleration,offsets)
    coefficient = (data['C'][:,:-1]+data['C'][:,1:])/2
    coefficient_rate = (moved['C'][:,:-1]+moved['C'][:,1:]).imag/(2e-20)
    flux = np.cumsum(system.node_weights[:-1]*p_rate[:,:-1],axis=1)
    flux_rate = np.cumsum(system.node_weights[:-1]*p_acceleration[:,:-1],axis=1)
    direct_flux = coefficient*np.diff(data['chi'],axis=1)/system.spacing
    gradient = flux_rate/coefficient-coefficient_rate*flux/coefficient**2
    direct_gradient = np.diff(q_value,axis=1)/system.spacing
    variation = np.sum(abs(np.diff(gradient,axis=1)),axis=1)
    local_bound = (weights @ variation**2)**.5
    velocity_energy = float(density_energy(system,velocity))
    acceleration_energy = float(density_energy(system,acceleration))
    analytic_bound = constants['flux_acceleration_constant']*np.sqrt(acceleration_energy)+constants['flux_velocity_constant']*velocity_energy
    extra = float(density_energy(system,velocity,extra=True))
    second_difference_bound = constants['radius_upper']**2/(4*system.spacing)*float(weights @ np.sum(np.diff(q_value,n=2,axis=1)**2,axis=1))
    variation_bound = constants['radius_upper']**2*system.spacing*local_bound**2/4
    return dict(velocity_energy=velocity_energy,acceleration_energy=acceleration_energy,Gram_velocity_energy=extra,
        flux_error=float(abs(flux-direct_flux).max()),differentiated_flux_error=float(abs(gradient-direct_gradient).max()),
        gradient_variation_norm=float(local_bound),gradient_variation_bound=float(analytic_bound),
        second_difference_Gram_bound=second_difference_bound,variation_Gram_bound=float(variation_bound),
        analytic_Gram_bound=float(constants['radius_upper']**2*system.spacing*analytic_bound**2/4))

