import numpy as np

from annular_finite_width_bulk_current_20260913 import shape_weight


class ChebyshevRule:
    def __init__(self, degree):
        self.degree = degree
        self.points = -np.cos(np.pi*np.arange(degree+1)/degree)
        self.inverse = np.linalg.inv(np.polynomial.chebyshev.chebvander(self.points, degree))
        primitives = np.polynomial.chebyshev.chebint(self.inverse, axis=0)
        self.integration = (np.polynomial.chebyshev.chebval(self.points, primitives)-np.polynomial.chebyshev.chebval(-1., primitives)[:, None]).T
        if abs(self.integration @ np.ones(degree+1)-self.points-1).max() > 1e-12:
            raise ValueError('Polynomial integration rule failed.')


class SplitGrid:
    def __init__(self, degree):
        self.rule = ChebyshevRule(degree)
        self.degree = degree
        self.offsets = np.concatenate([-.25+.25*self.rule.points, (.25+.25*self.rule.points)[1:]])
        self.weights = np.concatenate([.25*self.rule.integration[-1], (.25*self.rule.integration[-1])[1:]])
        self.weights[degree] += .25*self.rule.integration[-1, 0]

    def coefficients(self, values):
        return [self.rule.inverse @ values[:self.degree+1], self.rule.inverse @ values[self.degree:]]

    def evaluate(self, coefficients, offsets):
        offsets = np.asarray(offsets).reshape(-1)
        result = np.empty((len(offsets),)+coefficients[0].shape[1:], dtype=np.result_type(*coefficients))
        for index, center in enumerate([-.25, .25]):
            selected = offsets < 0 if index == 0 else offsets >= 0
            mapped = (offsets[selected]-center)/.25
            result[selected] = np.moveaxis(np.polynomial.chebyshev.chebval(mapped, coefficients[index]), -1, 0)
        return result


class LayerCurrent:
    def __init__(self, system, evaluator):
        self.system = system
        grid = system.current_grid
        coefficients = grid.coefficients(shape_weight(grid.offsets, system.shape)[:, None]*evaluator(grid.offsets))
        self.parts = []
        for index, (lower, upper) in enumerate([(-.5, 0.), (0., .5)]):
            primitive = np.polynomial.chebyshev.chebint(coefficients[index], axis=0)*.25
            self.parts.append((lower, upper, coefficients[index], primitive))

    def evaluate(self, radius):
        radius = np.asarray(radius).reshape(-1)
        system = self.system
        lower = (radius[:, None]-np.maximum(system.target_base, system.anchor_base))/system.width
        upper = (radius[:, None]-np.minimum(system.target_base, system.anchor_base))/system.width
        result = np.zeros_like(lower, dtype=np.result_type(self.parts[0][2]))
        for start, end, coefficients, primitive in self.parts:
            mapped_lower = (2*np.clip(lower, start, end)-start-end)/(end-start)
            mapped_upper = (2*np.clip(upper, start, end)-start-end)/(end-start)
            result += np.polynomial.chebyshev.chebval(mapped_upper, primitive, tensor=False)-np.polynomial.chebyshev.chebval(mapped_lower, primitive, tensor=False)
        return result @ system.orientation


class PolarGeometry:
    def __init__(self, system, time, state):
        self.system = system
        self.state = state
        self.coefficients = system.grid.coefficients(system.unpack(state)[0])
        self.pieces = []
        self.collocation_defect = 0.
        self.minimum_F = 1.
        rule = system.radial_rule
        dtype = np.result_type(state, time)
        mass_seed = np.asarray(system.lower_mass_seed, dtype=dtype)[()]
        log_seed = np.asarray(0., dtype=dtype)[()]
        previous_end = system.radii[0]-system.width/2
        for node, center in enumerate(system.radii):
            band_start = center-system.width/2
            if band_start > previous_end:
                self.pieces.append({'lower':previous_end, 'upper':band_start, 'gap':True, 'mass':mass_seed, 'log_lapse':log_seed})
                log_seed += .5*np.log((1-2*mass_seed/band_start)/(1-2*mass_seed/previous_end))
            for half in [0, 1]:
                lower = center-system.width/2+half*system.width/2
                upper = lower+system.width/2
                radius = (lower+upper)/2+(upper-lower)*rule.points/2
                offsets = (radius-center)/system.width
                scalar = self.scalar(offsets)
                measure = shape_weight(offsets, system.shape)/system.width
                potential = scalar['potential'][:, node]*measure
                source = node == len(system.radii)-1
                if source:
                    kinetic = measure*system.node_weights[node]*radius**2*scalar['source_velocity']**2/2
                    reservoir = measure*scalar['energy']
                    fixed_density = potential
                else:
                    kinetic = np.zeros_like(radius, dtype=dtype)
                    reservoir = np.zeros_like(radius, dtype=dtype)
                    fixed_density = potential+measure*system.node_weights[node]*scalar['p'][:, node]**2/(2*radius**2)
                integration = (upper-lower)/2*rule.integration
                constant = system.coupling*(fixed_density+kinetic)
                linear = 2*system.coupling*fixed_density/radius
                matrix = np.eye(len(radius))+integration*linear[None, :]
                masses = np.linalg.solve(matrix, mass_seed+integration @ constant)
                if source:
                    for iteration in range(5):
                        geometry = 1-2*masses/radius
                        if geometry.real.min() <= .1:
                            raise ValueError('Polar chart is outside the declared regular pilot domain.')
                        residual = masses-mass_seed-integration @ (constant-linear*masses+system.coupling*np.sqrt(geometry)*reservoir)
                        jacobian = matrix+integration*(system.coupling*reservoir/(radius*np.sqrt(geometry)))[None, :]
                        masses -= np.linalg.solve(jacobian, residual)
                geometry = 1-2*masses/radius
                if geometry.real.min() <= .1:
                    raise ValueError('Polar chart is outside the declared regular pilot domain.')
                mass_gradient = constant-linear*masses+system.coupling*np.sqrt(geometry)*reservoir
                defect = abs(masses-mass_seed-integration @ mass_gradient).max()
                self.collocation_defect = max(self.collocation_defect, float(defect))
                self.minimum_F = min(self.minimum_F, float(geometry.real.min()))
                density = fixed_density+kinetic/geometry
                log_gradient = masses/(radius**2*geometry)+system.coupling*density/radius
                logs = log_seed+integration @ log_gradient
                self.pieces.append({'lower':lower, 'upper':upper, 'gap':False, 'mass':rule.inverse @ masses, 'log_lapse':rule.inverse @ logs})
                mass_seed, log_seed = masses[-1], logs[-1]
                previous_end = upper
        if self.collocation_defect > 1e-11:
            raise ValueError('Radial constraint collocation failed.')
        self.edges = np.array([piece['lower'] for piece in self.pieces]+[self.pieces[-1]['upper']])
        self.normalization = 0.
        outer = self.metric(np.array([system.radii[-1]]))
        self.normalization = np.log((system.clock[0]+system.clock[1]*time)*outer['U'][0])-outer['log_N'][0]

    def scalar(self, offsets):
        system = self.system
        offsets = np.asarray(offsets).reshape(-1)
        values = system.grid.evaluate(self.coefficients, offsets)
        profile = system.grid.evaluate(system.source_profile, offsets)
        free = len(system.radii)-1
        theta, energy = values[:, 2*free], values[:, 2*free+1]
        source_velocity = profile[:, 1]+system.proper_acceleration*theta
        chi = np.column_stack([values[:, :free], profile[:, 0]+profile[:, 1]*theta+.5*system.proper_acceleration*theta**2])
        momentum = np.column_stack([values[:, free:2*free], np.zeros_like(theta)])
        radius = system.radii[None, :]+system.width*offsets[:, None]
        amplitude = chi @ system.factors.T
        potential = radius**2*(amplitude**2 @ system.sampling)/(2*system.spacing)
        return {'R':radius, 'chi':chi, 'p':momentum, 'A':amplitude, 'potential':potential, 'theta':theta, 'energy':energy, 'source_velocity':source_velocity}

    def metric(self, radius):
        shape = np.shape(radius)
        radius = np.asarray(radius).reshape(-1)
        if radius.real.min() < self.edges[0]-1e-12 or radius.real.max() > self.edges[-1]+1e-12:
            raise ValueError('No extrapolation beyond retained scalar support.')
        indices = np.clip(np.searchsorted(self.edges, radius.real, side='right')-1, 0, len(self.pieces)-1)
        dtype = np.result_type(self.state, self.normalization)
        mass, log_lapse = np.empty(len(radius), dtype=dtype), np.empty(len(radius), dtype=dtype)
        for index in np.unique(indices):
            selected = indices == index
            piece = self.pieces[index]
            locations = radius[selected]
            if piece['gap']:
                mass[selected] = piece['mass']
                log_lapse[selected] = piece['log_lapse']+.5*np.log((1-2*piece['mass']/locations)/(1-2*piece['mass']/piece['lower']))
            else:
                mapped = (2*locations-piece['lower']-piece['upper'])/(piece['upper']-piece['lower'])
                mass[selected] = np.polynomial.chebyshev.chebval(mapped, piece['mass'])
                log_lapse[selected] = np.polynomial.chebyshev.chebval(mapped, piece['log_lapse'])
        log_lapse += self.normalization
        root_f = np.sqrt(1-2*mass/radius)
        return {key:value.reshape(shape) for key,value in {'mu':mass, 'U':root_f, 'N':np.exp(log_lapse), 'log_N':log_lapse}.items()}

    def layer(self, offsets):
        system = self.system
        data = self.scalar(offsets)
        fields = self.metric(data['R'])
        momentum = data['p'].copy()
        momentum[:, -1] = data['R'][:, -1]**2*data['source_velocity']/fields['U'][:, -1]
        coefficient = data['R']**2*fields['N']*fields['U']
        speed = coefficient*momentum/data['R']**4
        density = coefficient @ system.sampling.T
        amplitude_rate = speed @ system.factors.T
        force = -(data['A']*density) @ system.factors/system.spacing
        pair_current = data['A'][:, system.factor]*(system.spair*coefficient[:, system.node]*amplitude_rate[:, system.factor]-system.bpair*speed[:, system.node]*density[:, system.factor])/system.spacing
        return dict(data, **fields, p=momentum, q=speed, C=coefficient, D=density, Gchi=force, pair_current=pair_current)


class HorizontalEvolution:
    def __init__(self, model, driver, clock, degree=12):
        self.grid = SplitGrid(degree)
        self.current_grid = SplitGrid(3*degree+12)
        self.radial_rule = ChebyshevRule(2*degree+8)
        for name in ['radii','spacing','width','shape','coupling','node_weights','factors','sampling','factor','node','bpair','spair','target_base','anchor_base','orientation']:
            setattr(self, name, getattr(model, name))
        self.clock = np.asarray(clock)
        self.proper_acceleration = driver.proper_acceleration
        self.lower_mass_seed = float(model.metric(np.array([model.edges[0]]))['mu'][0])
        initial = model.initial_scalar(self.grid.offsets)
        metric = model.metric(initial['R'])
        self.source_profile = self.grid.coefficients(np.column_stack([initial['chi'][:, -1], metric['U'][:, -1]*initial['p'][:, -1]/initial['R'][:, -1]**2]))
        self.initial_state = self.pack(np.column_stack([initial['chi'][:, :-1], initial['p'][:, :-1], np.zeros(len(self.grid.offsets)), np.full(len(self.grid.offsets), model.reservoir_energy)]), 0.)
        self.calls = 0

    def pack(self, values, inner_clock):
        return np.concatenate([np.asarray(values).reshape(-1), np.atleast_1d(inner_clock)])

    def unpack(self, state):
        return state[:-1].reshape(len(self.grid.offsets), 2*len(self.radii)), state[-1]

    def evaluate(self, time, state):
        geometry = PolarGeometry(self, time, state)
        current = LayerCurrent(self, lambda offsets:geometry.layer(offsets)['pair_current'])
        data = geometry.layer(self.grid.offsets)
        source_current = current.evaluate(data['R'][:, -1])
        source_mass_rate = -self.coupling*data['U'][:, -1]*source_current/data['N'][:, -1]
        source_p_rate = data['R'][:, -1]**2*self.proper_acceleration*data['N'][:, -1]/data['U'][:, -1]
        source_p_rate += data['R'][:, -1]*data['source_velocity']*source_mass_rate/data['U'][:, -1]**3
        source_force = self.node_weights[-1]*source_p_rate-data['Gchi'][:, -1]
        energy_rate = -source_force*data['source_velocity']
        values = np.column_stack([data['q'][:, :-1], data['Gchi'][:, :-1]/self.node_weights[:-1], data['N'][:, -1], energy_rate])
        inner_clock_rate = geometry.metric(np.array([self.radii[0]]))['N'][0]
        return {'geometry':geometry, 'current':current, 'data':data, 'source_p_rate':source_p_rate, 'source_force':source_force,
                'energy_rate':energy_rate, 'rhs':self.pack(values, inner_clock_rate)}

    def rhs(self, time, state):
        self.calls += 1
        return self.evaluate(time, state)['rhs']

    def mass_flux(self, evaluation, radius):
        fields = evaluation['geometry'].metric(radius)
        return -self.coupling*fields['U']*evaluation['current'].evaluate(radius)/fields['N']

    def differential_control(self, time, state, evaluation, radius):
        step = 1e-20
        perturbed = self.evaluate(time+1j*step, state+1j*step*evaluation['rhs'])
        metric_rate = {key:value.imag/step for key,value in perturbed['geometry'].metric(radius).items()}
        flux_rate = self.mass_flux(perturbed, radius).imag/step
        return {'metric_rate':metric_rate, 'mass_flux_rate':flux_rate, 'perturbed':perturbed,
                'mass_equation_error':float(abs(metric_rate['mu']-self.mass_flux(evaluation, radius)).max())}

    def source_at(self, evaluation, offsets):
        data = evaluation['geometry'].layer(offsets)
        mass_rate = self.mass_flux(evaluation, data['R'][:, -1])
        momentum_rate = data['R'][:, -1]**2*self.proper_acceleration*data['N'][:, -1]/data['U'][:, -1]
        momentum_rate += data['R'][:, -1]*data['source_velocity']*mass_rate/data['U'][:, -1]**3
        force = self.node_weights[-1]*momentum_rate-data['Gchi'][:, -1]
        return data, force

    def temporal_work(self, solution, end_time, order=8):
        points, weights = np.polynomial.legendre.leggauss(36)
        offsets = np.concatenate([-.25+.25*points, .25+.25*points])
        layer_weights = np.concatenate([.25*weights, .25*weights])*shape_weight(offsets, self.shape)
        radial_fraction = (self.radii-self.radii[0])/(self.radii[-1]-self.radii[0])
        direction = .01*(1+.3*np.sin(np.pi*radial_fraction))[None, :]*(1+.2*offsets[:, None])
        clock_direction = .02*(1+offsets)
        time_points, time_weights = np.polynomial.legendre.leggauss(order)
        integral, omitted_clock_work = 0., 0.
        for fraction, weight in zip((time_points+1)/2, end_time*time_weights/2):
            time = fraction*end_time
            evaluation = self.evaluate(time, solution.sol(time))
            data, force = self.source_at(evaluation, offsets)
            raw = (data['p']*self.node_weights*direction/end_time+fraction*data['Gchi']*direction).sum(axis=1)
            raw += force*fraction*direction[:, -1]+data['energy']*clock_direction/end_time-force*data['source_velocity']*fraction*clock_direction
            integral += weight*(layer_weights @ raw)
            omitted_clock_work += weight*(layer_weights @ (data['energy']*clock_direction/end_time-force*data['source_velocity']*fraction*clock_direction))
        last = self.evaluate(end_time, solution.sol(end_time))
        data = last['geometry'].layer(offsets)
        boundary = layer_weights @ ((data['p']*self.node_weights*direction).sum(axis=1)+data['energy']*clock_direction)
        return {'raw_variation':float(integral), 'endpoint_work':float(boundary), 'error':float(abs(integral-boundary)),
                'omitted_clock_work_error':float(abs(integral-omitted_clock_work-boundary))}
