from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_live_P2_current_20260918 import EvolvingP2System, LayerCurrent
from verify_annular_cut_transport_current_20260915 import direction, links
import numpy as np


class HistoryGeometry:
    edges = np.array([])

    def __init__(self, time):
        self.time = time

    def metric(self, radius):
        return Background().metric(self.time, radius)


class Background:
    def metric(self, time, radius):
        mass = .7+.002*(radius-6)+.001*time
        lapse = .92+.015*(radius-6)+.003*time+.002*time**2
        return lapse, np.sqrt(1-2*mass/radius)


def history(system, time):
    reference = system.model.radii
    base = (reference-system.model.anchor)*(.012+.004*np.sin(3*reference))
    first = .003*(reference-system.model.anchor)*np.cos(reference)
    second = .004*np.sin(reference-system.model.anchor)
    scalar = base+first*time+.5*second*time**2
    rates = first+second*time
    if np.ndim(time):
        return scalar, rates, second
    return np.append(scalar, 6.043+.05*time+.01*time**2), np.append(rates, .05+.02*time), np.append(second, .02)


def current_data(system, time):
    coordinates, rates, acceleration = history(system, time)
    return LayerCurrent(system.layer(.19, HistoryGeometry(time)), system.layer(.19, HistoryGeometry(time+1j*1e-24)),
        coordinates, rates, acceleration)


def finite_shift_action(system, time, amplitude):
    coordinates, rates, unused = history(system, time)
    layer = system.layer(.19, HistoryGeometry(time))
    radius, jacobian, displacement = layer.mapping(layer.reference_radius, coordinates[-1])
    nodes, node_jacobian, node_displacement = layer.mapping(layer.radii, coordinates[-1])
    targets = np.concatenate([radius, nodes])
    transported, clock = links(Background(), time, coordinates[-1], rates[-1], targets, amplitude)
    lapse, root = Background().metric(transported, targets)
    leading = direction(transported, targets)[0]
    connection = amplitude*leading/(1-amplitude**2*lapse**2*root**2*leading**2)
    coefficient = clock*targets**2*lapse*root*(1-amplitude**2*lapse**2*root**2*leading**2)
    scalar, scalar_rate, unused = history(system, transported[len(radius):])
    scalar_rate *= clock[len(radius):]+connection[len(radius):]*node_displacement*rates[-1]
    indices, shape, radial = layer.reference_indices, layer.reference_shape, layer.reference_radial
    reference_gradient = np.sum(radial*scalar[indices], axis=1)
    temporal = np.sum(shape*scalar_rate[indices], axis=1)-displacement*rates[-1]*reference_gradient/jacobian
    wave = np.dot(layer.reference_weight*jacobian*radius**4/coefficient[:len(radius)], temporal**2)/2
    wave -= np.dot(layer.reference_weight*coefficient[:len(radius)]/jacobian, reference_gradient**2)/2
    factor = layer.lifted @ scalar
    wave -= np.dot(layer.sampling @ (coefficient[len(radius):]/node_jacobian), factor**2)/(2*layer.gram_spacing)
    lapse, root = Background().metric(time, coordinates[-1])
    shift = amplitude*lapse**2*root**2*direction(time, coordinates[-1])[0]
    return wave-layer.source_mass*np.sqrt(lapse**2-(rates[-1]+shift)**2/root**2)


def variation_pair(system, time):
    current = current_data(system, time)
    layer, data = current.layer, current.data
    position, velocity = current.coordinates[-1], current.rates[-1]
    targets = np.concatenate([data['radius'], current.nodes, current.edges])
    source_direction, envelope, envelope_time, source_primitive = direction(time, position)
    primitive = direction(time, targets)[3]
    shift_time = envelope*(primitive-source_primitive)
    shift_time_fixed_dot = envelope_time*(primitive-source_primitive)-velocity*source_direction
    regular_count, node_count = len(data['radius']), len(current.nodes)
    node_slice = slice(regular_count, regular_count+node_count)
    node_shift = shift_time[node_slice]
    moving_clock = current.node_speed*direction(time, current.nodes)[0]
    delta_scalar = current.rates[:-1]*node_shift
    delta_rate = current.acceleration[:-1]*node_shift+current.rates[:-1]*(shift_time_fixed_dot[node_slice]+moving_clock)
    coefficient = layer.coefficient(0., targets)
    changed = system.layer(.19, HistoryGeometry(time+1j*1e-24))
    coefficient_time = changed.coefficient(0., targets).imag/1e-24
    delta_coefficient = coefficient_time*shift_time+coefficient*shift_time_fixed_dot
    raw = data['scalar_covector'] @ delta_scalar+data['momenta'][:-1] @ delta_rate
    raw += (data['weight']*data['density_dual']) @ delta_coefficient[:regular_count]
    raw += data['nodal_dual'] @ delta_coefficient[node_slice]
    lapse, root = Background().metric(time, position)
    source = data['material_momentum']*lapse**2*root**2*source_direction
    raw += source
    regular = data['weight'] @ (current.regular_work(data['radius'])*shift_time[:regular_count])
    atoms = current.atom_work @ node_shift
    atom_delta_prime = (current.atom_dual*current.node_speed*data['nodal']) @ direction(time, current.nodes)[0]
    boundaries = current.edge_work @ shift_time[regular_count+node_count:]
    adjoint = -current.euler @ delta_scalar-regular-atoms-atom_delta_prime-boundaries+source
    wrong_clock = raw-data['momenta'][:-1] @ (current.rates[:-1]*moving_clock)
    wrong_transport = adjoint+current.atom_transport_work @ node_shift+atom_delta_prime+boundaries
    return np.array([raw, adjoint, wrong_clock, wrong_transport]), current.noether()


def main():
    evidence = EvidenceRun('annular-P2-moving-shift-variation-attempt01', __file__)
    try:
        evidence.report.update(no_forward_evolution=True, github_action=False, subagents_used=False,
            explicit_source_anchored_horizontal_extension=True, unique_parent_shift_extension_proven=False,
            arbitrary_time_coordinate_covariance_proven=False, moving_P2_edges_and_Gram_atoms_retained=True,
            current_not_defined_from_radial_mass_derivative=True, finite_nonzero_shift_action_tested=True)
        points, weights = np.polynomial.legendre.leggauss(24)
        times, weights = .2*points, .2*weights
        for gram in [False, True]:
            system = EvolvingP2System(17, gram)
            branch = 'MTS' if gram else 'reference'
            samples = [variation_pair(system, time) for time in times]
            raw, adjoint, wrong_clock, wrong_transport = weights @ np.array([row[0] for row in samples])
            noether = max(row[1]['residual'] for row in samples)
            omitted = max(row[1]['without_moving_transport'] for row in samples)
            step = .0002
            action = [sum(weight*finite_shift_action(system, time, amplitude) for time, weight in zip(times, weights))
                for amplitude in [-2*step, -step, step, 2*step]]
            finite = (action[0]-8*action[1]+8*action[2]-action[3])/(12*step)
            coordinates, rates, unused = history(system, 0.)
            baseline = system.layer(.19, HistoryGeometry(0.)).evaluate(0., coordinates, rates)['action']
            row = dict(branch=branch, finite=float(finite), raw=float(raw), adjoint=float(adjoint),
                finite_error=float(abs(finite-raw)), adjoint_error=float(abs(raw-adjoint)),
                noether_error=noether, omitted_transport_noether_error=omitted,
                wrong_node_clock_error=float(abs(raw-wrong_clock)), wrong_transport_error=float(abs(adjoint-wrong_transport)))
            evidence.report['cases'].append(row)
            print(row, flush=True)
            evidence.check(branch+'_zero_shift_is_actual_retained_P2_action', abs(finite_shift_action(system, 0., 0.)-baseline) < 2e-13)
            evidence.check(branch+'_whole_layer_moving_Noether_identity', noether < 2e-10, noether)
            evidence.check(branch+'_nonzero_shift_action_derivative', row['finite_error'] < 2e-9, row['finite_error'])
            evidence.check(branch+'_current_integration_by_parts', row['adjoint_error'] < 2e-9, row['adjoint_error'])
            evidence.check(branch+'_missing_moving_node_clock_detected', row['wrong_node_clock_error'] > 1e-10, row['wrong_node_clock_error'])
            evidence.check(branch+'_missing_moving_transport_detected', omitted > 1e-9 and row['wrong_transport_error'] > 1e-10, row['wrong_transport_error'])
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
