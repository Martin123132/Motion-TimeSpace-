from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_wave_flux_events_v4_20260929 import EulerianWaveFlux
from annular_wave_flux_form_v2_20260929 import PolynomialTrace
from annular_source_centered_quadrature_20260929 import CenteredLabelDensity
from annular_candidate_coordinate_covectors_20260921 import local_polynomials
from annular_physical_native_kernel_20260928 import decimals
from annular_native_position_precision_20260929 import chebyshev_value
from annular_native_time_current_20260928 import field_radii, primitive, profile
from annular_position_support_column_20260930 import native_position_probe
from decimal import Decimal
from types import SimpleNamespace
from time import perf_counter
import numpy as np


def quadratic(coefficients, local, width):
    value = coefficients[:, 0] + local * (coefficients[:, 1] + local * coefficients[:, 2])
    radial = (coefficients[:, 1] + 2 * local * coefficients[:, 2]) / width
    return value, radial


def density_rows(data, radius, values, radial, time, amount=0.):
    width = data['width'] + amount * (data['movement_right']-data['movement_left'])
    local = (data['local']*data['width']-amount*data['movement_left'])/width
    source = data['source'] + amount*data['source_change']
    gradient = quadratic(data['field']+amount*data['field_change'], local, width)[1]
    rate, rate_r = quadratic(data['rate']+amount*data['rate_change'], local, width)
    acceleration = quadratic(data['acceleration']+amount*data['acceleration_change'], local, width)[0]
    displacement = data['displacement_left']+(data['displacement_right']-data['displacement_left'])*local
    source_velocity = data['source_velocity']+amount*data['source_rate_change']
    speed = displacement*source_velocity
    speed_r = (data['displacement_right']-data['displacement_left'])*source_velocity/width
    speed_rate = displacement*(data['source_acceleration']+amount*data['source_acceleration_change'])
    test, test_r = quadratic(data['test'], local, width)
    eta = data['eta_left']+(data['eta_right']-data['eta_left'])*local
    eta_r = (data['eta_right']-data['eta_left'])/width
    metric = 1-2*values[0]/radius
    metric_r = -2*radial[0]/radius+2*values[0]/radius**2
    lapse = np.exp(values[1])
    alpha, beta = radius**2/(lapse*np.sqrt(metric)), radius**2*lapse*np.sqrt(metric)
    alpha_r = alpha*(2/radius-radial[1]-metric_r/(2*metric))
    beta_r = beta*(2/radius+radial[1]+metric_r/(2*metric))
    alpha_t = -alpha*(time[1]-time[0]/(radius*metric))
    temporal = rate-speed*gradient
    gradient_rate = rate_r-speed_r*gradient
    temporal_rate = acceleration-speed_rate*gradient-speed*gradient_rate
    alpha_dot = alpha_t+speed*alpha_r
    beta_dot = -beta*alpha_t/alpha+speed*beta_r
    momentum_rate = (alpha_dot+speed_r*alpha)*temporal+alpha*temporal_rate
    flux = alpha*speed*temporal+beta*gradient
    energy = (alpha*temporal**2+beta*gradient**2)/2
    energy_dot = (alpha_dot*temporal**2+beta_dot*gradient**2)/2
    energy_dot += alpha*temporal*temporal_rate+beta*gradient*gradient_rate
    force = momentum_rate*(test-gradient*eta)+flux*test_r-alpha*temporal*gradient_rate*eta
    force -= (alpha_r*temporal**2-beta_r*gradient**2)*eta/2
    force -= (energy+alpha*speed*temporal*gradient)*eta_r
    rows = [force]
    node_left = data['node_left']+amount*data['movement_left']
    node_right = data['node_right']+amount*data['movement_right']
    node_rates = data['rate']+amount*data['rate_change']
    for power in range(3):
        integral = ((radius-6)**(power+1)-(source-6)**(power+1))/(power+1)
        weighted_nodes = []
        for fraction in [0., .5, 1.]:
            node_radius = node_left+(node_right-node_left)*fraction
            node_rate = node_rates[:, 0]+fraction*(node_rates[:, 1]+fraction*node_rates[:, 2])
            weighted_nodes.append(node_rate*((node_radius-6)**(power+1)-(source-6)**(power+1))/(power+1))
        left, middle, right = weighted_nodes
        weighted = left*(1-local)*(1-2*local)+4*middle*local*(1-local)+right*local*(2*local-1)
        weighted_r = (left*(4*local-3)+middle*(4-8*local)+right*(4*local-1))/width
        current = -momentum_rate*weighted-flux*weighted_r
        current += (energy_dot+(speed_r+alpha_t/alpha)*energy)*integral+energy*speed*(radius-6)**power
        rows.append(current)
    return np.array(rows)


class PositionIntegral(EulerianWaveFlux):
    def __init__(self, action, directions, correction, mode_rate, acceleration, reaction, position, metric_time, mixed):
        super().__init__(action, directions, correction, mode_rate, position, stable_traces=False)
        self.polynomials = dict(field=action.polynomial, rate=action.rate_polynomial,
            field_change=local_polynomials(action.mesh, decimals((directions['field_vertices']-correction[:, :-1]).T))[0],
            rate_change=local_polynomials(action.mesh, decimals(mode_rate[:, :-1].T))[0],
            acceleration=local_polynomials(action.mesh, decimals(acceleration[:, :-1].T))[0],
            acceleration_change=local_polynomials(action.mesh, decimals(reaction[:, :-1].T))[0],
            test=local_polynomials(action.mesh, decimals(directions['field_vertices'].T))[0])
        self.acceleration, self.reaction = acceleration[:, -1], reaction[:, -1]
        self.time_traces = [PolynomialTrace(item.solver, item.solution, self.anchor)
            for item in getattr(metric_time, 'responses', (metric_time,))]
        self.mixed_traces = [PolynomialTrace(item.solver, item.solution, self.anchor)
            for item in getattr(mixed, 'responses', (mixed,))]
        self.radial_cuts = np.unique(np.concatenate([item.edges for item in
            [self.metric]+self.responses+self.time_traces+self.mixed_traces]))
        self.geometry = object.__new__(CenteredLabelDensity)
        self.geometry.action, self.geometry.anchor, self.geometry.references = action, self.anchor, self.edges
        self.geometry.source_coefficients = action.owner.layer_rule.inverse@(action.source-self.anchor)
        self.geometry.source_derivative = 2*np.polynomial.chebyshev.chebder(self.geometry.source_coefficients)

    def packet(self, labels, offsets, cells=None, local=None):
        cardinal = self.action.cardinal(labels)
        source_offset = cardinal@(self.action.source-self.anchor)
        if local is None:
            jacobian = np.where(offsets < source_offset,
                1+(source_offset-self.action.owner.width*labels)/(-self.edges[0]),
                1-(source_offset-self.action.owner.width*labels)/self.edges[-1])
            reference = (offsets-source_offset)/jacobian
            cells = np.clip(np.searchsorted(self.edges, reference, side='right')-1, 0, len(self.widths)-1)
            local = (reference-self.edges[cells])/self.widths[cells]
        else:
            jacobian = np.where(self.edges[cells] < 0.,
                1+(source_offset-self.action.owner.width*labels)/(-self.edges[0]),
                1-(source_offset-self.action.owner.width*labels)/self.edges[-1])
        displacement = np.where(self.edges < 0., 1+self.edges/(-self.edges[0]), 1-self.edges/self.edges[-1])
        eta_left = np.einsum('ql,lq->q', cardinal, self.edge_vertices[:, cells], optimize=False)
        eta_right = np.einsum('ql,lq->q', cardinal, self.edge_vertices[:, cells+1], optimize=False)
        source_change = cardinal@self.source_direction
        mapped_left = self.edges[cells]+displacement[cells]*source_offset+(1-displacement[cells])*self.action.owner.width*labels
        mapped_right = self.edges[cells+1]+displacement[cells+1]*source_offset+(1-displacement[cells+1])*self.action.owner.width*labels
        packet = {name:np.einsum('qpl,ql->qp', poly[cells], cardinal, optimize=False) for name, poly in self.polynomials.items()}
        packet.update(width=self.widths[cells]*jacobian, local=local,
            source=self.anchor+source_offset, source_change=source_change,
            source_velocity=cardinal@self.action.velocity, source_rate_change=cardinal@self.source_rate,
            source_acceleration=cardinal@self.acceleration, source_acceleration_change=cardinal@self.reaction,
            displacement_left=displacement[cells], displacement_right=displacement[cells+1],
            eta_left=eta_left, eta_right=eta_right,
            movement_left=eta_left+displacement[cells]*source_change,
            movement_right=eta_right+displacement[cells+1]*source_change,
            node_left=self.anchor+mapped_left, node_right=self.anchor+mapped_right)
        active = (offsets >= self.edges[0]+self.action.owner.width*labels)&(offsets <= self.edges[-1]+self.action.owner.width*labels)
        return packet, active

    def evaluate_rows(self, packet, offsets, amount=0.):
        values, unused, radial, unused2 = self.metric.evaluate(offsets, self.metric.cells(offsets))
        time = sum(item.evaluate(offsets, item.cells(offsets))[0] for item in self.time_traces)
        if amount != 0:
            position_pairs = [item.evaluate(offsets, item.cells(offsets)) for item in self.responses]
            values = values+amount*sum(pair[0] for pair in position_pairs)
            radial = radial+amount*sum(pair[2] for pair in position_pairs)
            time = time+amount*sum(item.evaluate(offsets, item.cells(offsets))[0] for item in self.mixed_traces)
        return density_rows(packet, self.anchor+offsets, values, radial, time, amount)

    def integrate_rows(self, radial_order, label_order, deadline, progress):
        total = {name:np.zeros(4) for name in ['base', 'volume', 'material_faces', 'outer']}
        compensation = {name:np.zeros(4) for name in total}

        def deposit(name, block):
            updated = total[name]+block
            compensation[name] += np.where(abs(total[name]) >= abs(block), (total[name]-updated)+block, (block-updated)+total[name])
            total[name] = updated

        def guard(stage):
            if perf_counter() > deadline:
                raise RuntimeError('Safe C0 wave boundary: '+stage)
            progress(stage)

        endpoints = np.concatenate([self.geometry.geometry(self.edges, label)[0] for label in [-.5, .5]])
        cuts = np.unique(np.r_[self.radial_cuts, endpoints])
        points, weights = np.polynomial.legendre.leggauss(radial_order)
        lengths = np.diff(cuts)
        radii = (cuts[:-1, None]+lengths[:, None]*(points+1)/2).ravel()
        measures = (lengths[:, None]*weights/2).ravel()
        for start in range(0, len(radii), 16):
            if start % 2048 == 0:
                guard('C0-volume-'+str(radial_order)+'/'+str(label_order)+':'+str(start)+'/'+str(len(radii)))
            section = slice(start, start+16)
            density = CenteredLabelDensity(self.action, radii[section], label_order)
            offsets = radii[section][density.indices]
            packet, active = self.packet(density.offsets, offsets)
            moved = self.evaluate_rows(packet, offsets, 1e-25j)
            measure = measures[section][density.indices]*density.label_weights*active
            deposit('base', moved.real@measure)
            deposit('volume', (moved.imag/1e-25)@measure)
        guard('C0-material-faces')
        faces, labels, measures, offsets = self.face_rule(label_order)
        max_jump = np.zeros(4)
        for start in range(0, len(labels), 2048):
            if start % 32768 == 0:
                guard('C0-faces:'+str(start)+'/'+str(len(labels)))
            section = slice(start, start+2048)
            face, label, measure, radius = faces[section], labels[section], measures[section], offsets[section]
            lower, upper = np.clip(face-1, 0, len(self.widths)-1), np.clip(face, 0, len(self.widths)-1)
            left = self.packet(label, radius, lower, np.ones(len(face)))[0]
            right = self.packet(label, radius, upper, np.zeros(len(face)))[0]
            left_rows, right_rows = self.evaluate_rows(left, radius), self.evaluate_rows(right, radius)
            inner, outer = face == 0, face == len(self.widths)
            movement = np.where(outer, left['movement_right'], right['movement_left'])
            jump = right_rows-left_rows
            max_jump = np.maximum(max_jump, np.max(abs(jump), axis=1))
            deposit('material_faces', -jump@(measure*movement*~(inner|outer)))
            deposit('outer', left_rows@(measure*movement*outer)-right_rows@(measure*movement*inner))
        result = {name:total[name]+compensation[name] for name in total}
        result['complete'] = result['volume']+result['material_faces']+result['outer']
        result['maximum_material_jump'] = max_jump
        result['quadrature'] = np.array([radial_order, label_order, len(radii), len(labels)])
        return result


def native_coefficient_rows(engine, data, field_test, edge_test):
    result = engine.evaluate(data['edges'], data['field'], data['beta'], adjoint=False)
    velocity = data['displacement']*data['source_velocity']
    project = lambda change:engine.apply('sampling', result['image']*change, True)
    force = project(engine.tangent(data['edges'], data['field'], edge_test, field_test))
    rate = project(engine.tangent(data['edges'], data['field'], velocity, data['rate']))
    node_radius = field_radii(SimpleNamespace(elements=engine.indices), data['edges'], engine.count)
    native_radius = data['edges'][engine.native_edges]
    beta_rows, radial_rows = [force], [result['load']*edge_test[engine.native_edges]]
    for power in range(3):
        weighted_rate = data['rate']*primitive(node_radius, data['source'], power)
        field_work = project(engine.tangent(data['edges'], data['field'], np.zeros(len(data['edges']), dtype=object), weighted_rate))
        integral = primitive(native_radius, data['source'], power)
        beta_rows.append(-field_work+rate*integral+result['load']*velocity[engine.native_edges]*profile(native_radius, power))
        radial_rows.append(velocity[engine.native_edges]*result['load']*integral)
    return np.array(beta_rows, dtype=object), np.array(radial_rows, dtype=object)


def metric_value_traces(precision, offset):
    evaluator = precision.metric
    anchor = float(precision.action.owner.model.anchor)
    relative = precision.action.solver.edges-anchor
    lower = int(np.searchsorted(relative, offset, side='left')-1)
    upper = int(np.searchsorted(relative, offset, side='right')-1)
    lower, upper = max(0, lower), min(len(relative)-2, upper)
    radius = Decimal.from_float(anchor)+Decimal.from_float(float(offset))
    coefficients = []
    for cell in [lower, upper]:
        coordinate = 2*(radius-evaluator.centers[cell])/evaluator.lengths[cell]
        values, radial = [], []
        for component in range(2):
            primitive_poly, rhs, unused, constant = evaluator.coefficients(component, cell)
            values.append(constant+chebyshev_value(primitive_poly, coordinate))
            radial.append(chebyshev_value(rhs, coordinate))
        coefficients.append((values, radial))
    return radius, coefficients


def metric_beta_jump(precision, offset):
    radius, traces = metric_value_traces(precision, offset)
    coefficients = []
    for values, radial in traces:
        metric = 1-2*values[0]/radius
        metric_r = -2*radial[0]/radius+2*values[0]/radius**2
        beta = radius**2*values[1].exp()*metric.sqrt()
        beta_r = beta*(2/radius+radial[1]+metric_r/(2*metric))
        coefficients.append(np.array([beta, beta_r], dtype=object))
    return coefficients[1]-coefficients[0]


def dust_event_atoms(precision, geometry):
    radial_cuts = precision.action.solver.edges[1:-1]-geometry.anchor
    ends = [geometry.geometry(0., label)[0] for label in [-.5, .5]]
    if ends[1] <= ends[0]:
        raise RuntimeError('Source events require monotone labels')
    selected = radial_cuts[(radial_cuts > ends[0])&(radial_cuts < ends[1])]
    labels = geometry.inverse(selected, np.zeros(len(selected)))
    total, absolute = np.zeros(3), np.zeros(3)
    mass = Decimal.from_float(float(precision.action.owner.source_mass))
    for offset, label in zip(selected, labels):
        cardinal = decimals(precision.action.cardinal(float(label)).ravel())
        velocity = sum(cardinal*decimals(precision.action.velocity), Decimal(0))
        movement = sum(cardinal*precision.decimal_source, Decimal(0))
        radius, traces = metric_value_traces(precision, float(offset))
        currents = []
        for values, unused in traces:
            lapse_squared = (2*values[1]).exp()
            metric = 1-2*values[0]/radius
            current = mass*lapse_squared*velocity/(lapse_squared-velocity**2/metric).sqrt()
            currents.append(np.array([current*(radius-6)**power for power in range(3)], dtype=object))
        slope = geometry.geometry(0., label)[1]
        atom = np.asarray(currents[1]-currents[0], float)*float(movement)*6*(label+.5)*(.5-label)/slope
        total += atom
        absolute += abs(atom)
    return dict(atoms=total, absolute_atoms=absolute, events=len(labels))


def native_event_atoms(precision, directions, geometry, deadline, progress):
    engine, action = precision.native, precision.action
    if not engine.enabled:
        return dict(atoms=np.zeros(4), absolute_atoms=np.zeros(4), events=0, largest_beta_jump=np.zeros(2))
    radial_cuts = action.solver.edges[1:-1]-geometry.anchor
    total, absolute = np.zeros(4), np.zeros(4)
    events, largest = 0, np.zeros(2)
    jump_cache = {}
    for native_index, edge in enumerate(engine.native_edges):
        reference = geometry.references[edge]
        ends = [geometry.geometry(reference, label)[0] for label in [-.5, .5]]
        if ends[1] <= ends[0]:
            raise RuntimeError('Native cut events require a monotone label map')
        selected = radial_cuts[(radial_cuts > ends[0])&(radial_cuts < ends[1])]
        labels = geometry.inverse(selected, np.full(len(selected), reference))
        for offset, label in zip(selected, labels):
            if perf_counter() > deadline:
                raise RuntimeError('Safe native C0 event boundary')
            data, unused, movement, unused2, unused3 = precision.packet(float(label), 'decimal_tangents')
            cardinal = data['cardinal']
            field_test, edge_test = cardinal@decimals(directions['field_vertices']), cardinal@decimals(directions['edge_vertices'])
            beta_rows, radial_rows = native_coefficient_rows(engine, data, field_test, edge_test)
            if float(offset) not in jump_cache:
                jump_cache[float(offset)] = metric_beta_jump(precision, float(offset))
            jump = jump_cache[float(offset)]
            trace_jump = np.asarray(beta_rows[:, native_index]*jump[0]+radial_rows[:, native_index]*jump[1], float)
            slope = geometry.geometry(reference, label)[1]
            weight = 6*(label+.5)*(.5-label)
            atom = trace_jump*float(movement[edge])*weight/slope
            total += atom
            absolute += abs(atom)
            largest = np.maximum(largest, np.asarray(abs(jump), float))
            events += 1
            if events % 64 == 0:
                progress('C0-native-events:'+str(events))
    return dict(atoms=total, absolute_atoms=absolute, events=events, largest_beta_jump=largest)
