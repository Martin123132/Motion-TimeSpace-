from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_C0_boundary_integral_20260930 import PositionIntegral, dust_event_atoms, metric_beta_jump
from annular_physical_native_kernel_20260928 import decimals
from annular_native_time_current_20260928 import field_radii, primitive, profile
from decimal import Decimal
from types import SimpleNamespace
from time import perf_counter
import numpy as np


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
        field_work = project(engine.tangent(data['edges'], data['field'], np.full(len(data['edges']), Decimal(0), dtype=object), weighted_rate))
        integral = primitive(native_radius, data['source'], power)
        beta_rows.append(-field_work+rate*integral+result['load']*velocity[engine.native_edges]*profile(native_radius, power))
        radial_rows.append(velocity[engine.native_edges]*result['load']*integral)
    return np.array(beta_rows, dtype=object), np.array(radial_rows, dtype=object)


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

