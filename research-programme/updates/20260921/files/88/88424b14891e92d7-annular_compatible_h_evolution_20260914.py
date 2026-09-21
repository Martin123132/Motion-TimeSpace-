import numpy as np
from scipy.integrate import solve_ivp

from annular_covariant_scalar_action_20260912 import full_spatial_factors
from annular_gram_joint_action_20260909 import gram_matrices
from annular_horizontal_clock_evolution_20260913 import HorizontalEvolution, PolarGeometry, ChebyshevRule, SplitGrid
from annular_finite_width_bulk_current_20260913 import shape_weight


def compact_profile(radius):
    coordinate = (np.asarray(radius)-5.5)/.3
    selected = abs(coordinate)<1
    result = np.zeros_like(coordinate)
    result[selected] = np.exp(1-1/(1-coordinate[selected]**2))
    return result


class CompatibleEvolution(HorizontalEvolution):
    def __init__(self, count, gram, degree=8):
        if count<33:
            raise ValueError('This preparation requires at least33 nodes.')
        self.radii = np.linspace(5.,6.,count)
        self.spacing = 1/(count-1)
        self.width = self.spacing/2
        self.shape = 'beta22'
        self.coupling = .1
        self.lower_mass_seed = .8
        self.clock = np.array([1.,0.])
        self.proper_acceleration = 0.
        self.gram = bool(gram)
        self.grid = SplitGrid(degree)
        self.radial_rule = ChebyshevRule(2*degree+8)
        self.current_grid = SplitGrid(3*degree+12)
        self.node_weights = np.full(count,self.spacing)
        self.node_weights[[0,-1]] /= 2
        self.factors,self.sampling = full_spatial_factors(count,self.gram)
        self.factor,self.node = np.nonzero((self.factors!=0)|(self.sampling!=0))
        self.bpair = self.factors[self.factor,self.node]
        self.spair = self.sampling[self.factor,self.node]
        self.target_base = self.radii[self.node]
        self.anchor_base = (self.sampling @ self.radii)[self.factor]
        self.orientation = np.sign(self.target_base-self.anchor_base)
        radius = self.radii[None,:]+self.width*self.grid.offsets[:,None]
        bump = compact_profile(radius)
        scalar = .02*bump
        momentum = .004*radius**2*bump
        self.source_profile = self.grid.coefficients(np.zeros((len(self.grid.offsets),2)))
        values = np.column_stack([scalar[:,:-1],momentum[:,:-1],np.zeros(len(self.grid.offsets)),
                                  np.full(len(self.grid.offsets),.003)])
        self.initial_state = self.pack(values,0.)
        self.calls = 0

    def rhs(self,time,state):
        self.calls += 1
        geometry = PolarGeometry(self,time,state)
        data = geometry.layer(self.grid.offsets)
        values = np.column_stack([data['q'][:,:-1],data['Gchi'][:,:-1]/self.node_weights[:-1],
                                  data['N'][:,-1],np.zeros(len(self.grid.offsets))])
        return self.pack(values,geometry.metric(np.array([self.radii[0]]))['N'][0])

    def geometry(self,time,state):
        return PolarGeometry(self,time,state)

    def integrate(self,duration=.06,divisor=8,rtol=2e-11,atol=2e-13):
        result = solve_ivp(self.rhs,(0.,duration),self.initial_state,method='DOP853',
                           rtol=rtol,atol=atol,max_step=min(duration/divisor,self.spacing/4),dense_output=True)
        if not result.success:
            raise RuntimeError(result.message)
        return result


def gram_energy_triplet(system,geometry,order=24):
    points,weights = np.polynomial.legendre.leggauss(order)
    offsets = np.concatenate([-.25+.25*points,.25+.25*points])
    weights = np.concatenate([.25*weights,.25*weights])*shape_weight(offsets,system.shape)
    data = geometry.layer(offsets)
    factors,sampling = gram_matrices(len(system.radii))
    amplitude = data['chi'] @ factors.T
    rate = data['q'] @ factors.T
    coefficient = data['R']**2 @ sampling.T
    extra = weights @ np.sum(coefficient*amplitude**2,axis=1)/(2*system.spacing)
    rate_energy = weights @ np.sum(coefficient*rate**2,axis=1)/(2*system.spacing)
    derivative = weights @ np.sum(coefficient*amplitude*rate,axis=1)/system.spacing
    return np.array([extra,rate_energy,derivative],dtype=float)


def regular_chart_constants():
    gradient_bound = .02*8/(.3*np.e)
    gradient_integral = .6*gradient_bound**2
    base_plus_extra = 1.5*6.1**2*gradient_integral
    kinetic_bound = 6.1**2*.004**2/2
    total_mass_bound = .8+.1*(base_plus_extra+kinetic_bound+.003)
    return {'scalar_gradient_max_bound':float(gradient_bound),
            'scalar_gradient_integral_bound':float(gradient_integral),
            'initial_scalar_energy_upper_bound':float(base_plus_extra+kinetic_bound),
            'full_support_mass_upper_bound':float(total_mass_bound),
            'F_lower_if_exact_mass_conserved':float(1-2*total_mass_bound/4.9),
            'conditional_on_solution_existence_and_exact_conservation':True}


def trajectory_arrays(system,solution,duration=.06):
    times = np.linspace(0.,duration,17)
    offsets = np.linspace(-.5,.5,33)
    radii = np.linspace(5.,6.,129)
    states = solution.sol(times).T
    fields,profiles,energies,totals,minimums = [],[],[],[],[]
    for time,state in zip(times,states):
        geometry = system.geometry(time,state)
        metric = geometry.metric(radii)
        data = geometry.layer(offsets)
        fields.append(np.stack([metric['mu'],metric['log_N']]))
        profiles.append(np.stack([data['chi'],data['p']]))
        energies.append(gram_energy_triplet(system,geometry))
        totals.append(geometry.metric([geometry.edges[-1]])['mu'][0])
        minimums.append([geometry.minimum_F,float(data['N'].min()),float(data['energy'].min()),geometry.collocation_defect])
    return {'times':times,'states':states,'offsets':offsets,'radii':radii,
            'fields':np.array(fields),'profiles':np.array(profiles),'energies':np.array(energies),
            'total_mass':np.array(totals),'minimums_and_defect':np.array(minimums)}


def integrated_energy_rate(system,solution,duration,order):
    points,weights = np.polynomial.legendre.leggauss(order)
    integral = np.zeros(2)
    for time,weight in zip(duration*(points+1)/2,duration*weights/2):
        triplet = gram_energy_triplet(system,system.geometry(time,solution.sol(time)))
        integral += weight*np.array([triplet[2],np.sqrt(max(0.,triplet[1]))])
    return integral
