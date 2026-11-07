from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_position_time_loads_20260929 import MixedJet
from annular_position_reaction_20260929 import jet_exp
from annular_candidate_coordinate_covectors_20260921 import local_polynomials
from annular_physical_native_kernel_20260928 import decimals
from annular_source_centered_quadrature_20260929 import reference_offsets
from annular_native_position_precision_20260929 import DecimalMetric, chebyshev_value
from decimal import Decimal
from fractions import Fraction
from bisect import bisect_right
from time import perf_counter
import numpy as np


class PolynomialTrace:
    def __init__(self, solver, solution, anchor):
        self.edges = solver.edges - anchor
        self.centers = solver.centers - anchor
        self.lengths = solver.lengths
        self.solution = solution
        self.value_derivative = np.polynomial.chebyshev.chebder(solution['primitives'], axis=2)
        self.rhs_derivative = np.polynomial.chebyshev.chebder(solution['rhs_coefficients'], axis=2)

    def cells(self, offsets):
        return np.clip(np.searchsorted(self.edges, offsets, side='right') - 1, 0, len(self.lengths) - 1)

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

    def evaluate(self, data, offsets, cells, metric_cells, response_cells, local_override=None):
        jacobian, widths = data['jacobian'][cells], self.widths[cells]
        local = (offsets-data['mapped'][cells])/(widths*jacobian) if local_override is None else local_override
        reference = self.edges[cells]+widths*local
        displacement = np.where(self.edges[cells] < 0., 1+reference/(-self.edges[0]), 1-reference/self.edges[-1])
        displacement_xi = np.where(self.edges[cells] < 0., 1/(-self.edges[0]), -1/self.edges[-1])
        movement = (1-local)*data['edge'][cells]+local*data['edge'][cells+1]+displacement*data['source_mode']
        movement_r = (data['edge_slope'][cells]+displacement_xi*data['source_mode'])/jacobian
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
        gradient_reference = data['gradient'][cells, 0]+local*data['gradient'][cells, 1]
        gradient_direction = data['field_gradient'][cells, 0]+local*data['field_gradient'][cells, 1]
        gradient = gradient_reference/jacobian
        gradient_r = data['gradient'][cells, 1]/(widths*jacobian**2)
        gradient_change = gradient_direction/jacobian-gradient*movement_r
        gradient_change_r = data['field_gradient'][cells, 1]/(widths*jacobian**2)-gradient_r*movement_r
        gradient_jet = MixedJet(gradient, gradient_r, gradient_change, gradient_change_r)

        def quadratic(coefficients):
            selected = coefficients[cells]
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

    def fixed_label(self, label, radial_order, shape):
        data = self.label_data(label)
        cuts, cells, lengths, lower_local, upper_local, cut_is_radial = self.partition(data, label)
        middle = cuts[:-1]+lengths/2
        metric_cells = self.metric.cells(middle)
        response_cells = [item.cells(middle) for item in self.responses]
        points, weights = np.polynomial.legendre.leggauss(radial_order)
        offsets = (cuts[:-1, None]+lengths[:, None]*(points+1)/2).ravel()
        measure = (lengths[:, None]*weights/2).ravel()
        local = None if lower_local is None else (lower_local[:, None]
            +(upper_local-lower_local)[:, None]*(points+1)/2).ravel()
        interior = self.evaluate(data, offsets, np.repeat(cells, radial_order),
            np.repeat(metric_cells, radial_order), [np.repeat(item, radial_order) for item in response_cells], local)
        left = self.evaluate(data, cuts[:-1], cells, metric_cells, response_cells, lower_local)
        right = self.evaluate(data, cuts[1:], cells, metric_cells, response_cells, upper_local)
        result = {name: np.zeros(shape) for name in ['base_weak', 'base_volume', 'base_jumps', 'base_endpoints',
            'weak', 'volume', 'jumps', 'endpoints', 'moving_cuts', 'oracle_difference']}

        def deposit(name, cell_indices, factors):
            vector = np.zeros(shape[1])
            nodes = self.indices[cell_indices]
            for column in range(3):
                mask = nodes[:, column] >= 0
                np.add.at(vector, nodes[mask, column], factors[mask, column])
            result[name] += data['cardinal'][:, None]*vector[None, :]

        repeated = np.repeat(cells, radial_order)
        for name, scalar, test in [('base_weak', -interior['flux'], 'shape_r'),
                ('base_volume', interior['flux_r'], 'shape'), ('weak', -interior['change'], 'shape_r'),
                ('volume', interior['change_r'], 'shape'),
                ('oracle_difference', interior['change']-interior['oracle'], 'shape_r')]:
            deposit(name, repeated, (measure*scalar)[:, None]*interior[test])
        same_material = cells[:-1] == cells[1:]
        moving_mask = cut_is_radial & same_material
        stable = None
        if self.stable_traces:
            trace = {name: value[:-1][moving_mask] for name, value in right.items()
                if isinstance(value, np.ndarray) and value.ndim == 1}
            stable = self.stable_radial_jumps(cuts[1:-1][moving_mask], trace)
        for prefix, field in [('base_', 'flux'), ('', 'change')]:
            jumps = left[field][1:]-right[field][:-1]
            if stable is not None:
                jumps[moving_mask] = stable[0 if prefix else 1]
            mask = same_material
            deposit(prefix+'jumps', cells[1:][mask], jumps[mask, None]*left['shape'][1:][mask])
            mask = ~same_material
            deposit(prefix+'jumps', cells[1:][mask], left[field][1:][mask, None]*left['shape'][1:][mask])
            deposit(prefix+'jumps', cells[:-1][mask], -right[field][:-1][mask, None]*right['shape'][:-1][mask])
            deposit(prefix+'endpoints', cells[:1], left[field][:1, None]*left['shape'][:1])
            deposit(prefix+'endpoints', cells[-1:], -right[field][-1:, None]*right['shape'][-1:])
        jump = left['flux'][1:]-right['flux'][:-1]
        if stable is not None:
            jump[moving_mask] = stable[0]
        deposit('moving_cuts', cells[1:][moving_mask],
            (-jump[moving_mask]*left['movement'][1:][moving_mask])[:, None]*left['shape_r'][1:][moving_mask])
        diagnostics = dict(segments=len(middle), coincident_cuts=int(np.count_nonzero(cut_is_radial & ~same_material)),
            maximum_radial_flux_jump=float(np.max(np.abs(jump[moving_mask]), initial=0.)),
            maximum_radial_change_jump=float(np.max(np.abs(stable[1] if stable is not None else (left['change'][1:]-right['change'][:-1])[moving_mask]), initial=0.)),
            metric_derivative_gap=max(item['metric_derivative_gap'] for item in [interior, left, right]))
        return result, diagnostics

    def integrate(self, radial_order, label_order, shape, deadline, progress):
        labels, weights = np.polynomial.legendre.leggauss(label_order)
        labels, weights = labels/2, weights/2
        weights *= 6*(labels+.5)*(.5-labels)
        total, compensation, diagnostics = {}, {}, []
        for index, (label, weight) in enumerate(zip(labels, weights)):
            if perf_counter() > deadline:
                raise RuntimeError('Safe wave flux label boundary')
            result, diagnostic = self.fixed_label(label, radial_order, shape)
            diagnostics.append(diagnostic)
            for name, values in result.items():
                term = weight*values
                if name not in total:
                    total[name], compensation[name] = np.zeros_like(term), np.zeros_like(term)
                updated = total[name]+term
                compensation[name] += np.where(np.abs(total[name]) >= np.abs(term),
                    (total[name]-updated)+term, (term-updated)+total[name])
                total[name] = updated
            if index % 16 == 0:
                progress(str(radial_order)+'/'+str(label_order)+':'+str(index)+'/'+str(label_order))
        result = {name: total[name]+compensation[name] for name in total}
        result['base_flux'] = result['base_volume']+result['base_jumps']+result['base_endpoints']
        result['regular_flux'] = result['volume']+result['jumps']+result['endpoints']
        result['complete_flux'] = result['regular_flux']+result['moving_cuts']
        result['complete_weak'] = result['weak']+result['moving_cuts']
        return result, diagnostics
