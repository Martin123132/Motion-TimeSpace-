import numpy as np
from scipy.integrate import solve_ivp

from annular_gram_joint_action_20260909 import gram_matrices
from annular_horizontal_clock_evolution_20260913 import ChebyshevRule, PolarGeometry, SplitGrid
from annular_finite_width_bulk_current_20260913 import shape_weight


class MatchedConstraintSystem:
    def __init__(self, count, gamma, degree=32, profile='smooth', reservoir_scale=1.):
        if count < 17 or not 0 <= gamma <= 1 or reservoir_scale < 0:
            raise ValueError('This family requires count>=17, 0<=gamma<=1, nonnegative reservoir.')
        self.radii = np.linspace(5., 6., count)
        self.spacing = 1./(count-1)
        self.width = self.spacing/2
        self.shape = 'beta22'
        self.coupling = .1
        self.lower_mass_seed = .8
        self.clock = np.array([1., 0.])
        self.proper_acceleration = 0.
        self.gamma = gamma
        self.profile = profile
        self.reservoir_scale = reservoir_scale
        self.grid = SplitGrid(16)
        self.radial_rule = ChebyshevRule(degree)
        self.node_weights = np.full(count, self.spacing)
        self.node_weights[[0, -1]] /= 2
        identity = np.eye(count)
        self.base_factors = np.diff(identity, axis=0)
        self.base_sampling = (identity[:-1]+identity[1:])/2
        self.extra_factors, self.extra_sampling = gram_matrices(count)
        self.factors = np.concatenate([self.base_factors, np.sqrt(gamma)*self.extra_factors])
        self.sampling = np.concatenate([self.base_sampling, self.extra_sampling])
        values = self.profiles(self.grid.offsets)
        self.source_profile = self.grid.coefficients(np.column_stack([values['chi'][:, -1], values['source_velocity']]))
        state = np.column_stack([values['chi'][:, :-1], values['p'][:, :-1], values['theta'], values['energy']])
        self.initial_state = np.concatenate([state.reshape(-1), [0.]])

    def unpack(self, state):
        return state[:-1].reshape(len(self.grid.offsets), 2*len(self.radii)), state[-1]

    def profiles(self, offsets):
        offsets = np.asarray(offsets).reshape(-1)
        radius = self.radii[None, :]+self.width*offsets[:, None]
        coordinate = radius-5.
        if self.profile == 'smooth':
            scalar = .04*np.sin(2*np.pi*coordinate)+.005*coordinate**3
        elif self.profile == 'bounded_energy_rough':
            scalar = np.broadcast_to(.04*self.spacing*(-1.)**np.arange(len(self.radii)), radius.shape).copy()
        else:
            raise ValueError(self.profile)
        velocity = .012*(1+.2*np.cos(np.pi*coordinate))
        momentum = radius**2*velocity
        momentum[:, -1] = 0.
        amplitude = scalar @ self.factors.T
        potential = radius**2*(amplitude**2 @ self.sampling)/(2*self.spacing)
        return {'R':radius, 'chi':scalar, 'p':momentum, 'A':amplitude, 'potential':potential,
                'theta':np.zeros(len(offsets)), 'energy':self.reservoir_scale*.003*(1+.1*np.cos(2*np.pi*offsets)),
                'source_velocity':velocity[:, -1]}

    def density_parts(self, offsets):
        data = self.profiles(offsets)
        radius = data['R']
        base = radius**2*((data['chi'] @ self.base_factors.T)**2 @ self.base_sampling)/(2*self.spacing)
        extra = radius**2*((data['chi'] @ self.extra_factors.T)**2 @ self.extra_sampling)/(2*self.spacing)
        free = self.node_weights[None, :]*data['p']**2/(2*radius**2)
        kinetic = np.zeros_like(radius)
        reservoir = np.zeros_like(radius)
        kinetic[:, -1] = self.node_weights[-1]*radius[:, -1]**2*data['source_velocity']**2/2
        reservoir[:, -1] = data['energy']
        measure = shape_weight(np.asarray(offsets), self.shape).reshape(-1, 1)/self.width
        return {key:measure*value for key, value in {'base':base+free, 'extra':extra, 'kinetic':kinetic, 'reservoir':reservoir}.items()}

    def integrated_densities(self, order=48):
        points, weights = np.polynomial.legendre.leggauss(order)
        parts = self.density_parts(points/2)
        return {key:float(self.width*(weights/2) @ value.sum(axis=1)) for key, value in parts.items()}

    def geometry(self):
        return ManufacturedGeometry(self, 0., self.initial_state)


class ManufacturedGeometry(PolarGeometry):
    def scalar(self, offsets):
        return self.system.profiles(offsets)


def analytic_constants(spacing):
    lower, upper = 4.9, 6.1
    third_norm = .04**2*(2*np.pi)**6/2+.03**2
    first_norm_bound = (.04*2*np.pi)**2+2*.015**2*1.1**4
    extra_bound = 3*upper**2*spacing**4*third_norm/16
    uniform_extra_bound = 3*upper**2*(1/16)**4*third_norm/16
    combined_base_kinetic_bound = upper**2*(first_norm_bound+.0144**2)/2
    reservoir_bound = .0033
    mass_upper_bound = .8+.1*(combined_base_kinetic_bound+uniform_extra_bound+reservoir_bound)
    proven_F_lower = 1-2*mass_upper_bound/lower
    source_kinetic_bound = (1/16)*upper**2*.0144**2/4
    geometry_bounds = propagation_bounds(extra_bound, source_kinetic_bound)
    return dict(geometry_bounds, R_min=lower, R_max=upper, F_min=.5, F_max=1.,
                third_derivative_norm_squared=third_norm, first_derivative_norm_squared_bound=first_norm_bound,
                uniform_mass_upper_bound=mass_upper_bound, proven_uniform_F_lower=proven_F_lower,
                uniform_reservoir_integral_bound=reservoir_bound, uniform_source_kinetic_integral_bound=source_kinetic_bound)


def propagation_bounds(extra_integral, kinetic_integral, lower=4.9, outer=6., floor=.5):
    coupling = .1
    mass_bound = coupling*extra_integral
    log_bound = mass_bound/(lower*floor)
    log_bound += mass_bound*((1/lower-1/outer)+2*coupling*kinetic_integral/lower**2)/floor**2
    log_bound += coupling*extra_integral/lower
    return {'extra_integral_bound':extra_integral, 'mass_difference_bound':mass_bound,
            'log_lapse_difference_bound':log_bound, 'relative_lapse_difference_bound':-float(np.expm1(-log_bound)),
            'F_difference_bound':2*mass_bound/lower, 'U_difference_bound':mass_bound/(lower*np.sqrt(floor))}


class IndependentRadialPair:
    def __init__(self, system, rtol=2e-12, atol=2e-14, divisor=4):
        self.system = system
        self.pieces = []
        self.calls = 0
        state = np.array([system.lower_mass_seed, 0., 0., 0., 0.])
        previous = system.radii[0]-system.width/2
        for node, center in enumerate(system.radii):
            intervals = [(previous, center-system.width/2, None)]
            intervals += [(center-system.width/2, center, node), (center, center+system.width/2, node)]
            for lower, upper, selected in intervals:
                if upper <= lower:
                    continue
                span = upper-lower

                def equation(fraction, values):
                    self.calls += 1
                    radius = lower+span*fraction
                    if selected is None:
                        base, extra, kinetic, reservoir = 0., 0., 0., 0.
                    else:
                        parts = system.density_parts([(radius-center)/system.width])
                        base, extra, kinetic, reservoir = [parts[key][0, selected] for key in ['base', 'extra', 'kinetic', 'reservoir']]
                    mass, mass_difference, unused_log, unused_log_difference, unused_extra = values
                    base_F = 1-2*mass/radius
                    extra_F = base_F-2*mass_difference/radius
                    if min(base_F, extra_F) <= .1:
                        raise ValueError('Independent radial pair left the regular chart.')
                    coefficient = system.coupling*(2*base/radius+2*reservoir/(radius*(np.sqrt(base_F)+np.sqrt(extra_F))))
                    mass_rate = system.coupling*(base_F*base+kinetic+np.sqrt(base_F)*reservoir)
                    difference_rate = system.coupling*extra_F*extra-coefficient*mass_difference
                    log_rate = mass/(radius**2*base_F)+system.coupling*(base+kinetic/base_F)/radius
                    log_difference_rate = mass_difference*(1+2*system.coupling*kinetic)/(radius**2*base_F*extra_F)+system.coupling*extra/radius
                    return span*np.array([mass_rate, difference_rate, log_rate, log_difference_rate, extra])

                solution = solve_ivp(equation, (0., 1.), state, method='DOP853', rtol=rtol, atol=atol,
                                     max_step=1/divisor, dense_output=True)
                if not solution.success:
                    raise RuntimeError(solution.message)
                self.pieces.append((lower, upper, solution))
                state = solution.y[:, -1]
            previous = center+system.width/2
        self.edges = np.array([part[0] for part in self.pieces]+[self.pieces[-1][1]])
        outer = self.raw(np.array([system.radii[-1]]))[:, 0]
        base_F = 1-2*outer[0]/system.radii[-1]
        self.base_normalization = .5*np.log(base_F)-outer[2]
        self.delta_normalization = .5*np.log1p(-2*outer[1]/(system.radii[-1]*base_F))-outer[3]

    def raw(self, radii):
        radii = np.asarray(radii).reshape(-1)
        if radii.min() < self.edges[0]-1e-12 or radii.max() > self.edges[-1]+1e-12:
            raise ValueError('Independent pair does not extrapolate.')
        indices = np.clip(np.searchsorted(self.edges, radii, side='right')-1, 0, len(self.pieces)-1)
        output = np.empty((5, len(radii)))
        for index in np.unique(indices):
            selected = indices == index
            lower, upper, solution = self.pieces[index]
            output[:, selected] = solution.sol((radii[selected]-lower)/(upper-lower))
        return output

    def metric(self, radii):
        raw = self.raw(radii)
        return {'base_mass':raw[0], 'mass_difference':raw[1], 'base_log_N':raw[2]+self.base_normalization,
                'log_lapse_difference':raw[3]+self.delta_normalization, 'extra_cumulative':raw[4]}
