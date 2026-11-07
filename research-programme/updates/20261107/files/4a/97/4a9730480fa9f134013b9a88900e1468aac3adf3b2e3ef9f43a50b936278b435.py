from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_wave_flux_form_v2_20260929 import WaveFlux
from annular_source_centered_quadrature_20260929 import CenteredLabelDensity
from annular_position_time_loads_20260929 import MixedJet
from annular_position_reaction_20260929 import jet_exp
from time import perf_counter
import numpy as np


class EulerianWaveFlux(WaveFlux):
    def data_at(self, labels, offsets=None, cells=None, local=None):
        cardinal = self.action.cardinal(labels)
        source = cardinal @ (self.action.source-self.anchor)
        if local is None:
            jacobian = np.where(offsets < source,
                1+(source-self.action.owner.width*labels)/(-self.edges[0]),
                1-(source-self.action.owner.width*labels)/self.edges[-1])
            reference = (offsets-source)/jacobian
            cells = np.clip(np.searchsorted(self.edges, reference, side='right')-1, 0, len(self.widths)-1)
            local = (reference-self.edges[cells])/self.widths[cells]
        else:
            reference = self.edges[cells]+self.widths[cells]*local
            jacobian = np.where(self.edges[cells] < 0.,
                1+(source-self.action.owner.width*labels)/(-self.edges[0]),
                1-(source-self.action.owner.width*labels)/self.edges[-1])
        inner, outer = self.edges[0]+self.action.owner.width*labels, self.edges[-1]+self.action.owner.width*labels
        active = np.ones(len(labels), dtype=bool) if offsets is None else (offsets >= inner) & (offsets <= outer)
        mix = lambda coefficients: np.einsum('qpl,ql->qp', coefficients[cells], cardinal, optimize=False)
        return dict(cardinal=cardinal, source=source, jacobian=jacobian, cells=cells,
            local=local, reference=reference, active=active,
            velocity=cardinal @ self.action.velocity, source_mode=cardinal @ self.source_direction,
            source_rate=cardinal @ self.source_rate, gradient=mix(self.gradient),
            field_gradient=mix(self.field_gradient), rate=mix(self.rate), mode=mix(self.mode),
            edge_left=np.einsum('ql,lq->q', cardinal, self.edge_vertices[:, cells], optimize=False),
            edge_right=np.einsum('ql,lq->q', cardinal, self.edge_vertices[:, cells+1], optimize=False),
            edge_slope=np.einsum('ql,lq->q', cardinal, self.edge_slopes[:, cells], optimize=False))

    def evaluate(self, offsets, cells):
        coordinate = 2 * (offsets - self.centers[cells]) / self.lengths[cells]

        def polynomial(coefficients):
            return np.array([np.polynomial.chebyshev.chebval(coordinate,
                component[cells].T, tensor=False) for component in coefficients])

        value = self.solution['left'][:, cells] + polynomial(self.solution['primitives'])
        value_r = polynomial(self.value_derivative) * 2 / self.lengths[cells]
        rhs = polynomial(self.solution['rhs_coefficients'])
        rhs_r = polynomial(self.rhs_derivative) * 2 / self.lengths[cells]
        return value, value_r, rhs, rhs_r


class WaveFlux:
    def __init__(self, action, directions, correction, mode_rate, position, exact_partition=True, stable_traces=True):
        self.exact_partition, self.stable_traces = exact_partition, stable_traces
        self.action = action
        self.anchor = float(action.owner.model.anchor)
        self.edges = reference_offsets(action)
        self.widths = np.array([float(right-left) for left, right in zip(action.edges[:-1], action.edges[1:])])
        self.indices = np.asarray(action.mesh['elements'])
        self.gradient = action.gradient
        self.rate = action.rate_polynomial
        self.field_gradient = local_polynomials(action.mesh, decimals((directions['field_vertices']-correction[:, :-1]).T))[1]
        self.mode = local_polynomials(action.mesh, decimals(mode_rate[:, :-1].T))[0]
        self.source_direction = -correction[:, -1]
        self.source_rate = mode_rate[:, -1]
        self.edge_vertices = directions['edge_vertices']
        self.edge_slopes = np.asarray(np.diff(decimals(self.edge_vertices), axis=1) / decimals(self.widths)[None, :], float)
        self.metric = PolynomialTrace(action.solver, action.solution, self.anchor)
        self.responses = [PolynomialTrace(item.solver, item.solution, self.anchor)
            for item in getattr(position, 'responses', (position,))]
        self.radial_cuts = np.unique(np.concatenate([item.edges for item in [self.metric] + self.responses]))
        anchor_exact = Fraction(action.mesh['anchor'])
        fraction_decimal = lambda value: Decimal(value.numerator)/Decimal(value.denominator)
        self.exact_edges = [fraction_decimal(value-anchor_exact) for value in action.edges]
        self.exact_widths = [right-left for left, right in zip(self.exact_edges[:-1], self.exact_edges[1:])]
        self.exact_cuts = list(decimals(self.radial_cuts))
        self.trace_jumps = self.precise_trace_jumps(action, position) if stable_traces else None

    def precise_trace_jumps(self, action, position):
        solvers = [(action.solver, action.solution)] + [(item.solver, item.solution)
            for item in getattr(position, 'responses', (position,))]
        tables = []
        for solver, solution in solvers:
            evaluator = DecimalMetric(solver, solution)
            relative_edges = solver.edges-self.anchor
            left_cells = np.clip(np.searchsorted(relative_edges, self.radial_cuts, side='left')-1, 0, len(solver.lengths)-1)
            right_cells = np.clip(np.searchsorted(relative_edges, self.radial_cuts, side='right')-1, 0, len(solver.lengths)-1)
            table = np.zeros((2, 2, len(self.radial_cuts)))
            for index, (left_cell, right_cell) in enumerate(zip(left_cells, right_cells)):
                if left_cell == right_cell:
                    continue
                radius = Decimal.from_float(self.anchor)+self.exact_cuts[index]
                traces = []
                for cell in [left_cell, right_cell]:
                    coordinate = 2*(radius-evaluator.centers[cell])/evaluator.lengths[cell]
                    values, rhs_values = [], []
                    for component in range(2):
                        primitive, rhs, unused, constant = evaluator.coefficients(component, cell)
                        values.append(constant+chebyshev_value(primitive, coordinate))
                        rhs_values.append(chebyshev_value(rhs, coordinate))
                    traces.append(np.array([values, rhs_values], dtype=object))
                table[:, :, index] = np.asarray(traces[1]-traces[0], float)
            tables.append(table)
        return dict(metric=tables[0], position=sum(table[0] for table in tables[1:]))

    def partition(self, data, label):
        if not self.exact_partition:
            inner, outer = data['mapped'][[0, -1]]
            selected = self.radial_cuts[(self.radial_cuts > inner) & (self.radial_cuts < outer)]
            cuts = np.unique(np.r_[data['mapped'], selected])
            middle = cuts[:-1]+np.diff(cuts)/2
            cells = np.clip(np.searchsorted(data['mapped'], middle, side='right')-1, 0, len(self.widths)-1)
            return cuts, cells, np.diff(cuts), None, None, np.isin(cuts[1:-1], selected)
        source = Decimal.from_float(float(data['source']))
        width_label = Decimal.from_float(float(self.action.owner.width))*Decimal.from_float(float(label))
        jacobian = [1+(source-width_label)/(-self.exact_edges[0]) if edge < 0
            else 1-(source-width_label)/self.exact_edges[-1] for edge in self.exact_edges[:-1]]
        mapped = []
        for edge in self.exact_edges:
            displacement = 1+edge/(-self.exact_edges[0]) if edge < 0 else 1-edge/self.exact_edges[-1]
            mapped.append(edge+displacement*source+(1-displacement)*width_label)
        selected = [cut for cut in self.exact_cuts if mapped[0] < cut < mapped[-1]]
        selected_set = set(selected)
        cuts = sorted(set(mapped+selected))
        cells = np.array([min(max(bisect_right(mapped, (lower+upper)/2)-1, 0), len(self.widths)-1)
            for lower, upper in zip(cuts[:-1], cuts[1:])])
        lower_local = np.array([float((cut-mapped[cell])/(self.exact_widths[cell]*jacobian[cell]))
            for cut, cell in zip(cuts[:-1], cells)])
        upper_local = np.array([float((cut-mapped[cell])/(self.exact_widths[cell]*jacobian[cell]))
            for cut, cell in zip(cuts[1:], cells)])
        lengths = np.array([float(upper-lower) for lower, upper in zip(cuts[:-1], cuts[1:])])
        data['jacobian'] = np.array(jacobian, float)
        return np.array(cuts, float), cells, lengths, lower_local, upper_local, np.array([cut in selected_set for cut in cuts[1:-1]])

    def stable_radial_jumps(self, offsets, trace):
        indices = np.searchsorted(self.radial_cuts, offsets)
        if not np.array_equal(self.radial_cuts[indices], offsets):
            raise RuntimeError('Unregistered cut trace')
        value_jump = self.trace_jumps['metric'][0, :, indices].T
        rhs_jump = self.trace_jumps['metric'][1, :, indices].T
        position_jump = self.trace_jumps['position'][:, indices]
        radius, movement = trace['radius'], trace['movement']
        metric, metric_change = trace['metric'], trace['metric_change']
        metric_jump = -2*value_jump[0]/radius
        log_beta_jump = value_jump[1]+.5*np.log1p(metric_jump/metric)
        alpha_jump = trace['alpha']*np.expm1(-log_beta_jump)
        beta_jump = trace['beta']*np.expm1(log_beta_jump)
        variation_jump = position_jump+rhs_jump*movement
        metric_change_jump = -2*variation_jump[0]/radius+2*value_jump[0]*movement/radius**2
        ratio_change = (metric_change_jump-(metric_change/metric)*metric_jump)/(metric+metric_jump)
        log_change = variation_jump[1]+.5*ratio_change
        temporal, speed, gradient = trace['temporal'], trace['speed'], trace['gradient']
        alpha_coefficient = temporal*speed*(2*movement/radius-trace['nu_change']-.5*metric_change/metric)
        alpha_coefficient += trace['temporal_change']*speed+temporal*trace['speed_change']
        beta_coefficient = gradient*(2*movement/radius+trace['nu_change']+.5*metric_change/metric)+trace['gradient_change']
        flux_jump = alpha_jump*temporal*speed+beta_jump*gradient
        change_jump = alpha_jump*alpha_coefficient-(trace['alpha']+alpha_jump)*temporal*speed*log_change
        change_jump += beta_jump*beta_coefficient+(trace['beta']+beta_jump)*gradient*log_change
        return flux_jump, change_jump


    def label_data(self, label):
        cardinal = self.action.cardinal(label).ravel()
        source = cardinal @ (self.action.source - self.anchor)
        jacobian = np.where(self.edges[:-1] < 0.,
            1 + (source-self.action.owner.width*label)/(-self.edges[0]),
            1 - (source-self.action.owner.width*label)/self.edges[-1])
        displacement = np.where(self.edges < 0., 1+self.edges/(-self.edges[0]), 1-self.edges/self.edges[-1])
        mapped = self.edges + displacement*source + (1-displacement)*self.action.owner.width*label
        return dict(cardinal=cardinal, source=source, jacobian=jacobian, mapped=mapped,
            velocity=cardinal @ self.action.velocity, source_mode=cardinal @ self.source_direction,
            source_rate=cardinal @ self.source_rate,
            gradient=np.einsum('cpl,l->cp', self.gradient, cardinal, optimize=False),
            field_gradient=np.einsum('cpl,l->cp', self.field_gradient, cardinal, optimize=False),
            rate=np.einsum('cpl,l->cp', self.rate, cardinal, optimize=False),
            mode=np.einsum('cpl,l->cp', self.mode, cardinal, optimize=False),
            edge=self.edge_vertices.T @ cardinal, edge_slope=self.edge_slopes.T @ cardinal)

    def evaluate_many(self, data, offsets, metric_cells=None, response_cells=None):
        cells, local, reference = data['cells'], data['local'], data['reference']
        jacobian, widths = data['jacobian'], self.widths[cells]
        metric_cells = self.metric.cells(offsets) if metric_cells is None else metric_cells
        response_cells = [item.cells(offsets) for item in self.responses] if response_cells is None else response_cells
        displacement = np.where(self.edges[cells] < 0., 1+reference/(-self.edges[0]), 1-reference/self.edges[-1])
        displacement_xi = np.where(self.edges[cells] < 0., 1/(-self.edges[0]), -1/self.edges[-1])
        movement = (1-local)*data['edge_left']+local*data['edge_right']+displacement*data['source_mode']
        movement_r = (data['edge_slope']+displacement_xi*data['source_mode'])/jacobian
        radius = self.anchor+offsets
        values, value_r, rhs, rhs_r = self.metric.evaluate(offsets, metric_cells)
        response_pairs = [item.evaluate(offsets, selected)[:2] for item, selected in zip(self.responses, response_cells)]
        position = sum(pair[0] for pair in response_pairs)
        position_r = sum(pair[1] for pair in response_pairs)
        metric_jets = [MixedJet(values[index], value_r[index], position[index]+rhs[index]*movement,
            position_r[index]+rhs_r[index]*movement+rhs[index]*movement_r) for index in range(2)]
        radius_jet = MixedJet(radius, np.ones_like(radius), movement, movement_r)
        metric = 1-2*metric_jets[0]/radius_jet
        lapse = jet_exp(metric_jets[1])
        alpha, beta = radius_jet**2/(lapse*metric**.5), radius_jet**2*lapse*metric**.5
        gradient_reference = data['gradient'][:, 0]+local*data['gradient'][:, 1]
        gradient_direction = data['field_gradient'][:, 0]+local*data['field_gradient'][:, 1]
        gradient = gradient_reference/jacobian
        gradient_r = data['gradient'][:, 1]/(widths*jacobian**2)
        gradient_change = gradient_direction/jacobian-gradient*movement_r
        gradient_change_r = data['field_gradient'][:, 1]/(widths*jacobian**2)-gradient_r*movement_r
        gradient_jet = MixedJet(gradient, gradient_r, gradient_change, gradient_change_r)

        def quadratic(coefficients):
            selected = coefficients
            value = selected[:, 0]+local*(selected[:, 1]+local*selected[:, 2])
            radial = (selected[:, 1]+2*local*selected[:, 2])/(widths*jacobian)
            return value, radial

        rate, rate_r = quadratic(data['rate'])
        mode, mode_r = quadratic(data['mode'])
        rate_jet = MixedJet(rate, rate_r, mode, mode_r)
        speed_jet = MixedJet(displacement*data['velocity'], displacement_xi*data['velocity']/jacobian,
            displacement*data['source_rate'], displacement_xi*data['source_rate']/jacobian)
        temporal = rate_jet-speed_jet*gradient_jet
        flux = alpha*temporal*speed_jet+beta*gradient_jet
        amount = 1e-25j
        changed_radius = radius+amount*movement
        changed_values = values+amount*(position+rhs*movement)
        changed_metric = 1-2*changed_values[0]/changed_radius
        changed_lapse = np.exp(changed_values[1])
        changed_alpha = changed_radius**2/(changed_lapse*np.sqrt(changed_metric))
        changed_beta = changed_radius**2*changed_lapse*np.sqrt(changed_metric)
        changed_gradient = (gradient_reference+amount*gradient_direction)/(jacobian*(1+amount*movement_r))
        changed_speed = displacement*(data['velocity']+amount*data['source_rate'])
        changed_temporal = rate+amount*mode-changed_speed*changed_gradient
        oracle = (changed_alpha*changed_temporal*changed_speed+changed_beta*changed_gradient).imag/1e-25
        shape = np.column_stack([(1-local)*(1-2*local), 4*local*(1-local), local*(2*local-1)])
        shape_r = np.column_stack([4*local-3, 4-8*local, 4*local-1])/(widths*jacobian)[:, None]
        return dict(flux=flux.parts[0], flux_r=flux.parts[1], change=flux.parts[2], change_r=flux.parts[3],
            shape=shape, shape_r=shape_r, movement=movement, oracle=oracle,
            metric_derivative_gap=float(np.max(np.abs(value_r-rhs))), radius=radius,
            metric=metric.parts[0], metric_change=metric.parts[2], nu_change=metric_jets[1].parts[2],
            alpha=alpha.parts[0], beta=beta.parts[0], gradient=gradient, gradient_change=gradient_change,
            temporal=temporal.parts[0], temporal_change=temporal.parts[2],
            speed=speed_jet.parts[0], speed_change=speed_jet.parts[2])


    def face_rule(self, order):
        geometry = object.__new__(CenteredLabelDensity)
        geometry.action, geometry.anchor, geometry.references = self.action, self.anchor, self.edges
        geometry.source_coefficients = self.action.owner.layer_rule.inverse @ (self.action.source-self.anchor)
        geometry.source_derivative = 2*np.polynomial.chebyshev.chebder(geometry.source_coefficients)
        points, weights = np.polynomial.legendre.leggauss(order)
        face_indices, labels, measures, offsets = [], [], [], []
        for face, reference in enumerate(self.edges):
            ends = [geometry.geometry(reference, label)[0] for label in [-.5, .5]]
            if ends[1] < ends[0]:
                raise RuntimeError('Non-monotone material face requires a different label partition')
            selected = self.radial_cuts[(self.radial_cuts > ends[0]) & (self.radial_cuts < ends[1])]
            roots = geometry.inverse(selected, np.full(len(selected), reference)) if len(selected) else np.array([])
            cuts = np.unique(np.r_[-.5, roots, .5])
            sizes = np.diff(cuts)
            sample = (cuts[:-1, None]+sizes[:, None]*(points+1)/2).ravel()
            measure = (sizes[:, None]*weights/2).ravel()*6*(sample+.5)*(.5-sample)
            face_indices.append(np.full(len(sample), face))
            labels.append(sample)
            measures.append(measure)
            offsets.append(geometry.geometry(reference, sample)[0])
        return tuple(np.concatenate(items) for items in [face_indices, labels, measures, offsets])

    def integrate(self, radial_order, label_order, shape, deadline, progress):
        names = ['base_weak', 'base_volume', 'base_jumps', 'base_endpoints',
            'weak', 'volume', 'jumps', 'endpoints', 'moving_cuts', 'oracle_difference']
        total = {name: np.zeros(shape) for name in names}
        compensation = {name: np.zeros(shape) for name in names}
        diagnostics = dict(segments=0, coincident_cuts=0, maximum_radial_flux_jump=0.,
            maximum_radial_change_jump=0., metric_derivative_gap=0.)

        def deposit(name, data, factors):
            block = np.zeros(shape)
            nodes = self.indices[data['cells']]
            for column in range(3):
                selected = (nodes[:, column] >= 0) & data['active']
                weights = factors[selected, column, None]*data['cardinal'][selected]
                np.add.at(block.T, nodes[selected, column], weights)
            updated = total[name]+block
            compensation[name] += np.where(np.abs(total[name]) >= np.abs(block),
                (total[name]-updated)+block, (block-updated)+total[name])
            total[name] = updated

        def guard(stage):
            if perf_counter() > deadline:
                raise RuntimeError('Safe event-split wave flux boundary: '+stage)
            progress(stage)

        points, weights = np.polynomial.legendre.leggauss(radial_order)
        geometry = object.__new__(CenteredLabelDensity)
        geometry.action, geometry.anchor, geometry.references = self.action, self.anchor, self.edges
        geometry.source_coefficients = self.action.owner.layer_rule.inverse @ (self.action.source-self.anchor)
        geometry.source_derivative = 2*np.polynomial.chebyshev.chebder(geometry.source_coefficients)
        endpoints = np.concatenate([geometry.geometry(self.edges, label)[0] for label in [-.5, .5]])
        if min(endpoints) < self.radial_cuts[0] or max(endpoints) > self.radial_cuts[-1]:
            raise RuntimeError('Metric domain does not cover material support')
        volume_cuts = np.unique(np.r_[self.radial_cuts, endpoints])
        lengths = np.diff(volume_cuts)
        radii = (volume_cuts[:-1, None]+lengths[:, None]*(points+1)/2).ravel()
        measures = (lengths[:, None]*weights/2).ravel()
        for start in range(0, len(radii), 16):
            if start % 2048 == 0:
                guard('volume-'+str(radial_order)+'/'+str(label_order)+':'+str(start)+'/'+str(len(radii)))
            section = slice(start, start+16)
            density = CenteredLabelDensity(self.action, radii[section], label_order)
            offsets = radii[section][density.indices]
            data = self.data_at(density.offsets, offsets)
            packet = self.evaluate_many(data, offsets)
            measure = measures[section][density.indices]*density.label_weights*data['active']
            diagnostics['metric_derivative_gap'] = max(diagnostics['metric_derivative_gap'], packet['metric_derivative_gap'])
            for name, scalar, test in [('base_weak', -packet['flux'], 'shape_r'),
                    ('base_volume', packet['flux_r'], 'shape'), ('weak', -packet['change'], 'shape_r'),
                    ('volume', packet['change_r'], 'shape'),
                    ('oracle_difference', packet['change']-packet['oracle'], 'shape_r')]:
                deposit(name, data, (measure*scalar)[:, None]*packet[test])
        guard('material-faces')
        faces, labels, measures, offsets = self.face_rule(label_order)
        for start in range(0, len(labels), 4096):
            if start % 65536 == 0:
                guard('material-faces:'+str(start)+'/'+str(len(labels)))
            section = slice(start, start+4096)
            face, label, measure, radius = faces[section], labels[section], measures[section], offsets[section]
            lower = np.clip(face-1, 0, len(self.widths)-1)
            upper = np.clip(face, 0, len(self.widths)-1)
            lower_data = self.data_at(label, radius, lower, np.ones(len(face)))
            upper_data = self.data_at(label, radius, upper, np.zeros(len(face)))
            left = self.evaluate_many(lower_data, radius)
            right = self.evaluate_many(upper_data, radius)
            at_inner, at_outer = face == 0, face == len(self.widths)
            interior = ~(at_inner | at_outer)
            for prefix, field in [('base_', 'flux'), ('', 'change')]:
                jump = right[field]-left[field]
                factors = np.zeros((len(face), 3))
                factors[:, 0] = measure*jump*interior
                deposit(prefix+'jumps', upper_data, factors)
                factors = np.zeros((len(face), 3))
                factors[:, 0] = measure*right[field]*at_inner
                deposit(prefix+'endpoints', upper_data, factors)
                factors = np.zeros((len(face), 3))
                factors[:, 2] = -measure*left[field]*at_outer
                deposit(prefix+'endpoints', lower_data, factors)
        guard('radial-faces')
        radial_faces = self.radial_cuts[1:-1]
        for start in range(0, len(radial_faces), 16):
            if start % 512 == 0:
                guard('radial-faces:'+str(start)+'/'+str(len(radial_faces)))
            section = slice(start, start+16)
            density = CenteredLabelDensity(self.action, radial_faces[section], label_order)
            offsets = radial_faces[section][density.indices]
            data = self.data_at(density.offsets, offsets)
            metric_cells = np.clip(np.searchsorted(self.metric.edges, offsets, side='left')-1, 0, len(self.metric.lengths)-1)
            response_cells = [np.clip(np.searchsorted(item.edges, offsets, side='left')-1, 0, len(item.lengths)-1)
                for item in self.responses]
            packet = self.evaluate_many(data, offsets, metric_cells, response_cells)
            flux_jump, change_jump = self.stable_radial_jumps(offsets, packet)
            diagnostics['maximum_radial_flux_jump'] = max(diagnostics['maximum_radial_flux_jump'],
                float(np.max(np.abs(flux_jump[data['active']]), initial=0.)))
            diagnostics['maximum_radial_change_jump'] = max(diagnostics['maximum_radial_change_jump'],
                float(np.max(np.abs(change_jump[data['active']]), initial=0.)))
            measure = density.label_weights*data['active']
            deposit('base_jumps', data, (measure*flux_jump)[:, None]*packet['shape'])
            deposit('jumps', data, (measure*change_jump)[:, None]*packet['shape'])
            deposit('moving_cuts', data, (-measure*flux_jump*packet['movement'])[:, None]*packet['shape_r'])
        result = {name: total[name]+compensation[name] for name in names}
        result['base_flux'] = result['base_volume']+result['base_jumps']+result['base_endpoints']
        result['regular_flux'] = result['volume']+result['jumps']+result['endpoints']
        result['complete_flux'] = result['regular_flux']+result['moving_cuts']
        result['complete_weak'] = result['weak']+result['moving_cuts']
        return result, [diagnostics]
