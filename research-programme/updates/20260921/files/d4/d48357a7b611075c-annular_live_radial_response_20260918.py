from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_live_barycentric_20260915 import BarycentricDensity
from scipy.interpolate import PchipInterpolator
from scipy.integrate import solve_ivp
import numpy as np


class SnapshotLoads:
    def __init__(self, system, geometry, subdivisions=24):
        self.system, self.geometry = system, geometry
        self.edges = geometry.edges.copy()
        self.lower, self.upper = self.edges[[0, -1]]
        self.nodes = np.unique(np.concatenate([np.linspace(lower, upper, subdivisions+1)
            for lower, upper in zip(self.edges[:-1], self.edges[1:])]))
        density = BarycentricDensity(geometry.material, self.nodes, system.label_order)
        density.update(geometry.fields)
        energy = self.nodes**2*density.square/2
        if np.min(energy) < 0.:
            raise ValueError('Negative source-backed wave energy.')
        self.root_energy = PchipInterpolator(self.nodes, np.sqrt(energy))
        self.source_center = float(np.mean(geometry.material.source[:, 0]))
        self.width = system.width
        self.momentum_coefficients = geometry.material.coefficients[:, 1].copy()
        expected = self.source_center+self.width*system.labels
        if np.max(abs(expected-geometry.material.source[:, 0])) > 2e-12:
            raise ValueError('This initial-snapshot adapter requires the actual affine initial material map.')

    def energy(self, radius):
        return self.root_energy(np.asarray(radius))**2

    def source(self, radius, shift=0.):
        labels = (np.asarray(radius)-self.source_center-shift)/self.width
        selected = abs(labels) < .5
        density = np.where(selected, 6*(labels+.5)*(.5-labels)/self.width, 0.)
        momentum = np.polynomial.chebyshev.chebval(2*np.clip(labels, -.5, .5), self.momentum_coefficients)
        return density, momentum

    def directions(self, radius):
        radius = np.asarray(radius)
        density, unused = self.source(radius)
        energy_direction = self.energy(radius)*(1+.3*np.sin(2*radius))
        density_direction = density*(radius-self.source_center)/self.width
        momentum_direction = np.ones_like(radius)
        return energy_direction, density_direction, momentum_direction


def bump(radius, center, width, total):
    mapped = (np.asarray(radius)-center)/width
    return np.where(abs(mapped) < 1., total*15/(16*width)*(1-mapped**2)**2, 0.)


class RadialResponse:
    def __init__(self, loads, energy_parameter=0., momentum_parameter=0., density_parameter=0.,
            mass_parameter=0., shift=0., extra=None, tangent=False, method='DOP853', tight=False):
        self.loads = loads
        self.coupling = loads.system.coupling
        self.source_mass = loads.system.source_mass+mass_parameter
        self.parameters = energy_parameter, momentum_parameter, density_parameter
        self.shift, self.extra, self.tangent = shift, extra, tangent
        self.edges = loads.edges.copy()
        source_edges = loads.source_center+shift+loads.width*np.array([-.5, .5])
        self.edges = np.unique(np.concatenate([self.edges, source_edges]))
        if extra is not None:
            self.edges = np.unique(np.concatenate([self.edges, [extra[0]-extra[1], extra[0]+extra[1]]]))
        if min(self.edges) < loads.lower or max(self.edges) > loads.upper:
            raise ValueError('Load support left the original radial domain.')
        self.solutions = []
        value = np.array([loads.system.central_mass, 0., 0., 0., 0., 0.])
        tolerance = 2e-13 if tight else 2e-12
        for lower, upper in zip(self.edges[:-1], self.edges[1:]):
            solution = solve_ivp(self.rhs, (lower, upper), value, method=method, dense_output=True,
                rtol=tolerance, atol=tolerance/100, max_step=(upper-lower)/5)
            if not solution.success:
                raise RuntimeError(solution.message)
            self.solutions.append(solution)
            value = solution.y[:, -1]
        self.final = value
        final_metric = 1-2*value[0]/loads.upper
        self.lapse_shift = .5*np.log(final_metric)-value[1]
        self.lapse_variation_shift = -value[3]/(loads.upper*final_metric)-value[4]
        self.hamiltonian = value[0]/self.coupling

    def inputs(self, radius):
        energy = self.loads.energy(radius)
        density, momentum = self.loads.source(radius, self.shift)
        energy_direction, density_direction, momentum_direction = self.loads.directions(radius)
        energy += self.parameters[0]*energy_direction
        density += self.parameters[2]*density_direction
        momentum += self.parameters[1]*momentum_direction
        if self.extra is not None:
            energy += bump(radius, *self.extra)
        if np.min(energy) < -1e-15 or np.min(density) < -1e-12:
            raise ValueError('Directional test left the nonnegative density domain.')
        return energy, density, momentum, energy_direction, density_direction, momentum_direction

    def coefficients(self, radius, mass):
        energy, density, momentum, energy_direction, density_direction, momentum_direction = self.inputs(radius)
        metric = 1-2*mass/radius
        if np.min(metric) <= 0.:
            raise ValueError('Radial response left the untrapped branch.')
        source_mass, coupling = self.source_mass, self.coupling
        loading = np.sqrt(metric*(source_mass**2+metric*momentum**2))
        loading_mass = -(source_mass**2+2*metric*momentum**2)/(radius*loading)
        loading_momentum = metric**2*momentum/loading
        damping = coupling*(2*energy/radius-density*loading_mass)
        mass_rhs = coupling*(metric*energy+loading*density)
        lapse_rhs = mass/(radius**2*metric)+coupling*energy/radius
        lapse_rhs += coupling*density*metric*momentum**2/(radius*loading)
        speed_log_radial = 2*mass/(radius**2*metric)-coupling*source_mass**2*density/(radius*loading)
        return dict(energy=energy, density=density, momentum=momentum, metric=metric, loading=loading,
            loading_mass=loading_mass, loading_momentum=loading_momentum, damping=damping,
            mass_rhs=mass_rhs, lapse_rhs=lapse_rhs, speed_log_radial=speed_log_radial,
            energy_direction=energy_direction, density_direction=density_direction, momentum_direction=momentum_direction)

    def rhs(self, radius, state):
        mass, unused, unused2, mass_first, unused3, mass_second = state
        data = self.coefficients(radius, mass)
        metric, loading, density, momentum = [data[name] for name in ['metric', 'loading', 'density', 'momentum']]
        coupling, source_mass = self.coupling, self.source_mass
        if not self.tangent:
            return np.array([data['mass_rhs'], data['lapse_rhs'], data['damping'], 0., 0., 0.])
        energy_direction, density_direction, momentum_direction = [data[name] for name in ['energy_direction', 'density_direction', 'momentum_direction']]
        loading_mm = -source_mass**4/(radius**2*loading**3)
        loading_mp = -metric**2*momentum*(3*source_mass**2+2*metric*momentum**2)/(radius*loading**3)
        loading_pp = metric**3*source_mass**2/loading**3
        mass_first_rhs = -data['damping']*mass_first+coupling*(metric*energy_direction
            +loading*density_direction+density*data['loading_momentum']*momentum_direction)
        lapse_mass = 1/(radius**2*metric**2)-coupling*density*metric*source_mass**2*momentum**2/(radius**2*loading**3)
        lapse_momentum = coupling*density*metric**2*momentum*(2*source_mass**2+metric*momentum**2)/(radius*loading**3)
        lapse_first_rhs = lapse_mass*mass_first+coupling*energy_direction/radius
        lapse_first_rhs += coupling*metric*momentum**2*density_direction/(radius*loading)+lapse_momentum*momentum_direction
        mass_second_rhs = -data['damping']*mass_second+coupling*(-4*mass_first*energy_direction/radius
            +density*(loading_mm*mass_first**2+2*loading_mp*mass_first*momentum_direction+loading_pp*momentum_direction**2)
            +2*density_direction*(data['loading_mass']*mass_first+data['loading_momentum']*momentum_direction))
        return np.array([data['mass_rhs'], data['lapse_rhs'], data['damping'], mass_first_rhs, lapse_first_rhs, mass_second_rhs])

    def sample(self, radius):
        radius = np.atleast_1d(radius)
        labels = np.clip(np.searchsorted(self.edges, radius, side='right')-1, 0, len(self.solutions)-1)
        values = np.empty((6, len(radius)))
        for index, solution in enumerate(self.solutions):
            selected = labels == index
            if np.any(selected):
                values[:, selected] = solution.sol(radius[selected])
        data = self.coefficients(radius, values[0])
        lapse = np.exp(values[1]+self.lapse_shift)
        root = np.sqrt(data['metric'])
        speed = lapse*root
        lapse_first = values[4]+self.lapse_variation_shift
        speed_first = speed*(lapse_first-values[3]/(radius*data['metric']))
        raw_speed_radial = speed*(data['lapse_rhs']+(values[0]/radius**2-data['mass_rhs']/radius)/data['metric'])
        data.update(radius=radius, mass=values[0], log_lapse=values[1]+self.lapse_shift,
            lapse=lapse, root=root, speed=speed, speed_radial=raw_speed_radial,
            cancelled_speed_radial=speed*data['speed_log_radial'],
            eta=np.exp(values[2]-self.final[2]), mass_first=values[3], mass_second=values[5],
            log_lapse_first=lapse_first, speed_first=speed_first)
        return data


def integration_nodes(edges, order=8):
    nodes, weights = np.polynomial.legendre.leggauss(order)
    radii = ((edges[:-1, None]+edges[1:, None])/2+np.diff(edges)[:, None]*nodes/2).ravel()
    measure = (np.diff(edges)[:, None]*weights/2).ravel()
    return radii, measure


def adjoint_integrals(solution):
    edges = np.unique(np.concatenate([solution.edges, solution.loads.nodes]))
    radius, measure = integration_nodes(edges)
    data = solution.sample(radius)
    density, momentum, metric, loading = [data[name] for name in ['density', 'momentum', 'metric', 'loading']]
    energy = loading/data['root']
    velocity = data['lapse']*metric*momentum/energy
    clock = data['lapse']*solution.source_mass/energy
    gravity_gradient = data['lapse']*(energy*data['lapse_rhs']
        +momentum**2/energy*(data['mass']/radius**2-data['mass_rhs']/radius))
    gravity_reduced = data['lapse']*data['mass']/radius**2*(energy/metric+momentum**2/energy)
    gravity_reduced += solution.coupling*data['lapse']*solution.source_mass**2*data['energy']/(radius*energy)
    terms = dict(wave=float(measure @ (data['speed']*data['energy_direction'])),
        source_density=float(measure @ (data['eta']*loading*data['density_direction'])),
        momentum=float(measure @ (density*velocity*data['momentum_direction'])),
        rest_mass=float(measure @ (density*clock)), translation=float(measure @ (density*gravity_gradient)))
    terms.update(gradient_reduction_error=float(max(abs(gravity_gradient-gravity_reduced))),
        adjoint_metric_identity=float(max(abs(data['eta']-data['lapse']/data['root']))),
        speed_cancellation_error=float(max(abs(data['speed_radial']-data['cancelled_speed_radial']))),
        density_integral=float(measure @ density), wave_energy_integral=float(measure @ data['energy']),
        minimum_metric=float(min(metric)), minimum_wave_speed=float(min(data['speed'])),
        maximum_source_ratio=float(max(abs(data['root']*momentum/energy))))
    return terms
