import numpy as np
from scipy.integrate import solve_ivp

from annular_live_exterior_response_20260913 import TimeFit
from annular_finite_width_bulk_current_20260913 import shape_weight


class FiniteFactorExteriorResponse:
    def __init__(self, system, response, samples, quadrature_order=48):
        self.system, self.response = system, response
        self.duration = response.duration
        self.times = samples['times']
        self.negative = system.grid.offsets < 0
        points, weights = np.polynomial.legendre.leggauss(quadrature_order)
        self.offsets = (points-1)/4
        self.weights = weights/4*shape_weight(self.offsets, system.shape)
        self.force_factors = np.flatnonzero(system.factors[:, 0] != 0)
        lower = np.minimum(system.anchor_base, system.target_base)[None, :]+system.width*self.offsets[:, None]
        upper = np.maximum(system.anchor_base, system.target_base)[None, :]+system.width*self.offsets[:, None]
        self.crossing = (lower < system.radii[0]) & (upper > system.radii[0])
        self.current_pairs = np.flatnonzero(self.crossing.any(axis=0))
        self.current_factors = np.unique(system.factor[self.current_pairs])
        self.current_nodes = np.unique(system.node[self.current_pairs])
        self.scalar_nodes = np.flatnonzero(np.any(system.factors[np.union1d(self.force_factors, self.current_factors)] != 0, axis=0))
        self.metric_nodes = np.union1d(self.current_nodes, np.flatnonzero(np.any(system.sampling[np.union1d(self.force_factors, self.current_factors)] != 0, axis=0)))
        collected = {name:[] for name in ['kinetic', 'stiffness', 'drive', 'endpoint', 'C', 'chi', 'q', 'reference_current']}
        self.force_algebra_error = 0.
        for time, state in zip(self.times, samples['reference_states'].T):
            evaluation = system.evaluate(time, state)
            data = evaluation['data']
            factor_column = system.factors[:, 0]
            remainder = data['A']-data['chi'][:, [0]]*factor_column
            kinetic = data['C'][:, 0]/data['R'][:, 0]**4
            stiffness = data['D'] @ factor_column**2/(system.node_weights[0]*system.spacing)
            drive = -((data['D']*remainder) @ factor_column)/(system.node_weights[0]*system.spacing)
            reconstructed = -stiffness*data['chi'][:, 0]+drive
            self.force_algebra_error = max(self.force_algebra_error, float(abs(reconstructed-data['Gchi'][:, 0]/system.node_weights[0]).max()))
            collected['kinetic'].append(kinetic[self.negative])
            collected['stiffness'].append(stiffness[self.negative])
            collected['drive'].append(drive[self.negative])
            collected['endpoint'].append(np.array([data['chi'][system.grid.degree, 0], data['p'][system.grid.degree, 0]]))
            layer = evaluation['geometry'].layer(self.offsets)
            for name in ['C', 'chi', 'q']:
                collected[name].append(layer[name])
            collected['reference_current'].append(evaluation['current'].evaluate(np.array([system.radii[0]]))[0])
        self.samples = {name:np.stack(values) for name, values in collected.items()}
        self.fits = {name:TimeFit(values, self.duration) for name, values in self.samples.items()}

    def equation(self, time, exterior, frozen=False):
        configuration, momentum = np.split(exterior, 2)
        selected_time = 0. if frozen else time
        return np.concatenate([self.fits['kinetic'](selected_time)*momentum,
                               -self.fits['stiffness'](selected_time)*configuration+self.fits['drive'](time)])

    def integrate(self, initial, frozen=False):
        solution = solve_ivp(lambda time, exterior:self.equation(time, exterior, frozen),
                             (0., self.duration), initial, method='DOP853', rtol=2e-12, atol=2e-14,
                             max_step=self.duration/8, dense_output=True)
        if not solution.success:
            raise RuntimeError(solution.message)
        return solution

    def current(self, time, exterior):
        system = self.system
        configuration, momentum = np.split(exterior, 2)
        endpoint = self.fits['endpoint'](time)
        values = np.column_stack([np.append(configuration, endpoint[0]), np.append(momentum, endpoint[1])])
        coefficients = system.grid.rule.inverse @ values
        left = np.polynomial.chebyshev.chebval(4*self.offsets+1, coefficients).T
        chi = self.fits['chi'](time).copy()
        coefficient = self.fits['C'](time)
        velocity = self.fits['q'](time).copy()
        chi[:, 0] = left[:, 0]
        velocity[:, 0] = coefficient[:, 0]*left[:, 1]/(system.radii[0]+system.width*self.offsets)**4
        amplitude = chi @ system.factors.T
        amplitude_rate = velocity @ system.factors.T
        density = coefficient @ system.sampling.T
        pair = amplitude[:, system.factor]*(system.spair*coefficient[:, system.node]*amplitude_rate[:, system.factor]
                                           -system.bpair*velocity[:, system.node]*density[:, system.factor])/system.spacing
        return self.weights @ ((pair*self.crossing) @ system.orientation)

    def run(self, samples):
        initial = samples['reference_states'][self.response.exterior, 0]
        solution = self.integrate(initial)
        frozen = self.integrate(initial, frozen=True)
        states = solution.sol(self.times)
        currents = np.array([self.current(time, states[:, index]) for index, time in enumerate(self.times)])
        expected = samples['reference_states'][self.response.exterior]
        record = {'force_factor_indices':self.force_factors.tolist(), 'crossing_factor_indices':self.current_factors.tolist(),
                  'scalar_node_indices':self.scalar_nodes.tolist(), 'metric_node_indices':self.metric_nodes.tolist(),
                  'crossing_pair_indices':self.current_pairs.tolist(),
                  'force_algebra_error':self.force_algebra_error,
                  'live_factor_state_error':float(abs(states-expected).max()),
                  'live_factor_current_error':float(abs(currents-samples['baseline_outputs'][:, 0]).max()),
                  'frozen_kinetic_stiffness_state_error':float(abs(frozen.sol(self.times)-expected).max()),
                  'metric_traces_supplied_from_coupled_solution':True,
                  'standalone_metric_closure_derived':False, 'one_point_trace_law_derived':False}
        arrays = dict(self.samples, factor_states=states, factor_currents=currents,
                      factor_frozen_states=frozen.sol(self.times), times=self.times)
        return record, arrays

