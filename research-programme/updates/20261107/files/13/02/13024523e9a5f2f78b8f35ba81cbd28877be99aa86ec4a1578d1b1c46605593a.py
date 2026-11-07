from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_C0_boundary_integral_20260930 import PositionIntegral, quadratic
from annular_source_centered_quadrature_20260929 import CenteredLabelDensity
from annular_native_position_precision_20260929 import DecimalMetric, chebyshev_value
from decimal import Decimal
from time import perf_counter
import numpy as np


def material_density_rows(data, radius, values, radial, time, amount=0.):
    width = data['width'] + amount * (data['movement_right']-data['movement_left'])
    local = data['local']
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


def metric_traces(solver, solution, offsets, anchor):
    evaluator = DecimalMetric(solver, solution)
    relative = solver.edges-anchor
    output = np.empty((2, 2, 2, len(offsets)), dtype=object)
    for side, ownership in enumerate(['left', 'right']):
        cells = np.clip(np.searchsorted(relative, offsets, side=ownership)-1, 0, len(solver.lengths)-1)
        for index, (offset, cell) in enumerate(zip(offsets, cells)):
            radius = Decimal.from_float(anchor)+Decimal.from_float(float(offset))
            coordinate = 2*(radius-evaluator.centers[cell])/evaluator.lengths[cell]
            for component in range(2):
                primitive, rhs, unused, constant = evaluator.coefficients(component, cell)
                output[side, 0, component, index] = constant+chebyshev_value(primitive, coordinate)
                output[side, 1, component, index] = chebyshev_value(rhs, coordinate)
    return output


def base_kinematics(data, radius):
    from annular_C0_boundary_integral_20260930 import quadratic
    local, width = data['local'], data['width']
    gradient = quadratic(data['field'], local, width)[1]
    rate, rate_r = quadratic(data['rate'], local, width)
    acceleration = quadratic(data['acceleration'], local, width)[0]
    displacement = data['displacement_left']+(data['displacement_right']-data['displacement_left'])*local
    speed = displacement*data['source_velocity']
    speed_r = (data['displacement_right']-data['displacement_left'])*data['source_velocity']/width
    test, test_r = quadratic(data['test'], local, width)
    eta = data['eta_left']+(data['eta_right']-data['eta_left'])*local
    temporal = rate-speed*gradient
    gradient_rate = rate_r-speed_r*gradient
    temporal_rate = acceleration-displacement*data['source_acceleration']*gradient-speed*gradient_rate
    packet = dict(gradient=gradient, temporal=temporal, gradient_rate=gradient_rate, temporal_rate=temporal_rate,
        speed=speed, speed_r=speed_r, test=test, test_r=test_r, eta=eta,
        eta_r=(data['eta_right']-data['eta_left'])/width)
    for power in range(3):
        packet['I'+str(power)] = ((radius-6)**(power+1)-(data['source']-6)**(power+1))/(power+1)
        packet['h'+str(power)] = (radius-6)**power
        nodes = []
        for fraction in [0., .5, 1.]:
            node_radius = data['node_left']+(data['node_right']-data['node_left'])*fraction
            node_rate = data['rate'][:, 0]+fraction*(data['rate'][:, 1]+fraction*data['rate'][:, 2])
            nodes.append(node_rate*((node_radius-6)**(power+1)-(data['source']-6)**(power+1))/(power+1))
        left, middle, right = nodes
        packet['V'+str(power)] = left*(1-local)*(1-2*local)+4*middle*local*(1-local)+right*local*(2*local-1)
        packet['Vr'+str(power)] = (left*(4*local-3)+middle*(4-8*local)+right*(4*local-1))/width
    return {key:np.array([Decimal.from_float(float(value)) for value in values], dtype=object) for key, values in packet.items()}


def decimal_density(kinematics, radius, values, radial, time):
    gradient, temporal, gradient_rate, temporal_rate, speed, speed_r, test, test_r, eta, eta_r = [kinematics[key]
        for key in ['gradient', 'temporal', 'gradient_rate', 'temporal_rate', 'speed', 'speed_r', 'test', 'test_r', 'eta', 'eta_r']]
    metric = 1-2*values[0]/radius
    metric_r = -2*radial[0]/radius+2*values[0]/radius**2
    lapse = np.exp(values[1])
    alpha, beta = radius**2/(lapse*np.sqrt(metric)), radius**2*lapse*np.sqrt(metric)
    alpha_r = alpha*(2/radius-radial[1]-metric_r/(2*metric))
    beta_r = beta*(2/radius+radial[1]+metric_r/(2*metric))
    alpha_t = -alpha*(time[1]-time[0]/(radius*metric))
    alpha_dot, beta_dot = alpha_t+speed*alpha_r, -beta*alpha_t/alpha+speed*beta_r
    momentum = (alpha_dot+speed_r*alpha)*temporal+alpha*temporal_rate
    flux = alpha*speed*temporal+beta*gradient
    energy = (alpha*temporal**2+beta*gradient**2)/2
    energy_dot = (alpha_dot*temporal**2+beta_dot*gradient**2)/2+alpha*temporal*temporal_rate+beta*gradient*gradient_rate
    force = momentum*(test-gradient*eta)+flux*test_r-alpha*temporal*gradient_rate*eta
    force -= (alpha_r*temporal**2-beta_r*gradient**2)*eta/2
    force -= (energy+alpha*speed*temporal*gradient)*eta_r
    rows = [force]
    for power in range(3):
        suffix = str(power)
        current = -momentum*kinematics['V'+suffix]-flux*kinematics['Vr'+suffix]
        current += (energy_dot+(speed_r+alpha_t/alpha)*energy)*kinematics['I'+suffix]
        current += energy*speed*kinematics['h'+suffix]
        rows.append(current)
    return np.array(rows, dtype=object)


class MaterialPositionIntegral(PositionIntegral):
    def __init__(self, *args):
        super().__init__(*args)
        action, metric_time = args[0], args[7]
        self.base_trace_table = metric_traces(action.solver, action.solution, self.radial_cuts, self.anchor)
        self.time_trace_table = sum(metric_traces(item.solver, item.solution, self.radial_cuts, self.anchor)[:, 0]
            for item in getattr(metric_time, 'responses', (metric_time,)))
        self.maximum_metric_derivative_gap = 0.

    def material_rows(self, packet, offsets, amount):
        values, value_r, radial, radial_r = self.metric.evaluate(offsets, self.metric.cells(offsets))
        movement = packet['movement_left']+(packet['movement_right']-packet['movement_left'])*packet['local']
        dilation = (packet['movement_right']-packet['movement_left'])/packet['width']
        position_pairs = [item.evaluate(offsets, item.cells(offsets)) for item in self.responses]
        time_pairs = [item.evaluate(offsets, item.cells(offsets)) for item in self.time_traces]
        time = sum(pair[0] for pair in time_pairs)
        mixed = sum(item.evaluate(offsets, item.cells(offsets))[0] for item in self.mixed_traces)
        self.maximum_metric_derivative_gap = max(self.maximum_metric_derivative_gap, float(np.max(abs(value_r-radial))))
        moved_values = values+amount*(sum(pair[0] for pair in position_pairs)+value_r*movement)
        moved_radial = radial+amount*(sum(pair[2] for pair in position_pairs)+radial_r*movement)
        moved_time = time+amount*(mixed+sum(pair[1] for pair in time_pairs)*movement)
        rows = material_density_rows(packet, self.anchor+offsets+amount*movement, moved_values, moved_radial, moved_time, amount)
        return rows*(1+amount*dilation)

    def integrate_rows(self, radial_order, label_order, deadline, progress):
        totals = {name:np.zeros(4) for name in ['base', 'volume', 'radial_cut_atoms']}
        compensations = {name:np.zeros(4) for name in totals}

        def deposit(name, block):
            updated = totals[name]+block
            compensations[name] += np.where(abs(totals[name]) >= abs(block), (totals[name]-updated)+block, (block-updated)+totals[name])
            totals[name] = updated

        def guard(stage):
            if perf_counter() > deadline:
                raise RuntimeError('Safe material C0 boundary: '+stage)
            progress(stage)

        endpoints = np.concatenate([self.geometry.geometry(self.edges, label)[0] for label in [-.5, .5]])
        cuts = np.unique(np.r_[self.radial_cuts, endpoints])
        points, weights = np.polynomial.legendre.leggauss(radial_order)
        lengths = np.diff(cuts)
        radii = (cuts[:-1, None]+lengths[:, None]*(points+1)/2).ravel()
        measures = (lengths[:, None]*weights/2).ravel()
        for start in range(0, len(radii), 16):
            if start % 2048 == 0:
                guard('material-volume-'+str(radial_order)+':'+str(start)+'/'+str(len(radii)))
            section = slice(start, start+16)
            density = CenteredLabelDensity(self.action, radii[section], label_order)
            offsets = radii[section][density.indices]
            packet, active = self.packet(density.offsets, offsets)
            rows = self.material_rows(packet, offsets, 1e-25j)
            measure = measures[section][density.indices]*density.label_weights*active
            deposit('base', rows.real@measure)
            deposit('volume', (rows.imag/1e-25)@measure)
        maximum_jump, absolute_atoms = np.zeros(4), np.zeros(4)
        for start in range(0, len(self.radial_cuts), 8):
            if start % 256 == 0:
                guard('material-radial-cuts:'+str(start)+'/'+str(len(self.radial_cuts)))
            section = slice(start, start+8)
            density = CenteredLabelDensity(self.action, self.radial_cuts[section], label_order)
            offsets = self.radial_cuts[section][density.indices]
            packet, active = self.packet(density.offsets, offsets)
            columns = np.arange(len(self.radial_cuts))[section][density.indices]
            kinematics = base_kinematics(packet, self.anchor+offsets)
            radius = np.array([Decimal.from_float(self.anchor)+Decimal.from_float(float(value)) for value in offsets], dtype=object)
            traces = [decimal_density(kinematics, radius, self.base_trace_table[side, 0][:, columns],
                self.base_trace_table[side, 1][:, columns], self.time_trace_table[side][:, columns]) for side in [0, 1]]
            jump = np.asarray(traces[1]-traces[0], float)
            movement = packet['movement_left']+(packet['movement_right']-packet['movement_left'])*packet['local']
            measure = density.label_weights*movement*active
            deposit('radial_cut_atoms', jump@measure)
            absolute_atoms += abs(jump)@abs(measure)
            maximum_jump = np.maximum(maximum_jump, np.max(abs(jump), axis=1))
        output = {name:totals[name]+compensations[name] for name in totals}
        output.update(complete=output['volume']+output['radial_cut_atoms'], absolute_radial_cut_atoms=absolute_atoms,
            maximum_radial_density_jump=maximum_jump, metric_derivative_gap=np.array(self.maximum_metric_derivative_gap),
            quadrature=np.array([radial_order, label_order, len(radii), len(self.radial_cuts)]))
        return output



