from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_support_shift_jet_20260928 import make_packet, wave_blocks, finite_wave_current, perturb, interpolate, integrals
from annular_directional_coupled_Euler_20260928 import restore_flow, layer
from derive_annular_support_map_constraints_20260927 import restore_case, load_owned
from derive_annular_native_shape_stress_20260928 import physical_data, nodal_transport
from annular_physical_native_kernel_20260928 import NativeKernel, decimals
from annular_moving_Legendre_current_20260921 import samples
from annular_radial_Ward_moments_20260921 import prepare
from decimal import Decimal, localcontext
from time import perf_counter
import contextlib
import csv
import hashlib
import json
import numpy as np
import sympy as sp


def transport_rate(engine, loads, action, edge_vertices, evidence, name):
    results = []
    for index, label in enumerate(action.owner.layer_rule.points / 2):
        data = physical_data(engine, loads, action, label)
        atoms = engine.atoms(data['edges'], data['field'])
        rates = engine.atoms(data['edges'], data['rate'])
        strain = np.diff(data['displacement'] * data['source_velocity']) / np.diff(data['edges'])
        derivative = {key: rates[key] - atoms[key] * strain for key in ['slope_left', 'slope_right']}
        edge_direction = decimals(edge_vertices[index])
        derived = 2 * nodal_transport(engine, dict(atoms=derivative), edge_direction)
        estimates = []
        for step in [Decimal('.0001'), Decimal('.00005'), Decimal('.000025')]:
            pair = []
            for sign in [1, -1]:
                moved_edges = data['edges'] + sign * step * data['displacement'] * data['source_velocity']
                moved_field = data['field'] + sign * step * data['rate']
                pair.append(nodal_transport(engine, dict(atoms=engine.atoms(moved_edges, moved_field)), edge_direction))
            estimates.append((pair[0] - pair[1]) / step)
        finite = (4 * estimates[2] - estimates[1]) / 3
        error, scale = max(abs(finite - derived)), max(abs(derived))
        evidence.check(name + ':independent_transport_rate:' + str(index),
            error <= Decimal('1e-24') + Decimal('1e-10') * scale,
            dict(error=str(error), scale=str(scale)))
        results.append(np.asarray(derived, float))
    return np.array(results)


def correction(packet, acceleration_nodes, power):
    accel, unused = interpolate(packet, acceleration_nodes)
    temporal = packet['rate'] - packet['speed'] * packet['gradient']
    integral = integrals(packet['radius'], packet['source'], power)
    weighted = interpolate(packet, packet['node_rate'] * integrals(packet['node_radius'], packet['source'], power))[0]
    return packet['measure'] @ (packet['alpha'] * accel * (temporal * integral - weighted))


def completed_packet(packet, direction, acceleration_nodes, amount):
    moved = perturb(packet, direction, amount)
    accel, accel_r = interpolate(packet, acceleration_nodes)
    moved['acceleration'] = packet['acceleration'] + amount * accel
    moved['acceleration_r'] = packet['acceleration_r'] + amount * accel_r
    moved['node_acceleration'] = packet['node_acceleration'] + amount * acceleration_nodes
    return moved


def main():
    evidence = EvidenceRun('annular-geometric-support-jet-attempt01', __file__)
    started, deadline = perf_counter(), perf_counter() + 7200
    try:
        evidence.own(evidence.root / 'DERIVATION-20260928-geometric-support-jet-completion.md')
        parent_path = evidence.output.parent / 'annular-support-shift-jet-attempt01/status.json'
        parent = json.loads(parent_path.read_text())
        evidence.own(parent_path)
        evidence.check('frozen_jet_stage_complete', parent['state'] == 'complete' and all(row['passed'] for row in parent['checks']))
        digests, bad = {}, []
        for category in ['inputs', 'outputs']:
            for relative, digest in parent[category].items():
                path = evidence.root / relative
                if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != digest:
                    bad.append(relative)
                else:
                    evidence.own(path)
                    digests[str(path.relative_to(evidence.root))] = digest
        evidence.check('frozen_jet_inputs_unchanged', not bad, bad)
        read = lambda relative: load_owned(evidence, digests, evidence.root / relative)
        time = sp.symbols('time')
        amplitude, transport = sp.Function('s')(time), sp.Function('z')(time)
        changed_accel = sp.diff(amplitude * transport, time, 2).subs({amplitude: 0, sp.diff(amplitude, time): 1, sp.diff(amplitude, time, 2): 0})
        evidence.check('factor_two_geometric_chain_rule', sp.expand(changed_accel - 2 * sp.diff(transport, time)) == 0)
        eta, gradient_t, gradient_r, speed = sp.symbols('eta gdot g_R W')
        delta_temporal_t = 2 * eta * gradient_t - eta * gradient_t - speed * eta * gradient_r
        evidence.check('Eulerian_temporal_rate_invariant_on_smooth_patch', sp.expand(delta_temporal_t - eta * (gradient_t - speed * gradient_r)) == 0)

        def save(name, **arrays):
            path = evidence.output / (name + '.npz')
            np.savez_compressed(path, **arrays)
            evidence.own(path, 'outputs')
            return str(path.relative_to(evidence.root))

        summaries, variations, spatial_rows = [], [], []
        with localcontext() as context:
            context.prec = 70
            for case in parent['cases']:
                name = case['branch'] + '-' + case['level']
                print(json.dumps(dict(stage=name, seconds=perf_counter() - started)), flush=True)
                loads, action, sources = restore_case(evidence, digests, case['branch'], case['level'], deadline)
                mesh = read(sources['packet'])
                engine = NativeKernel(mesh['mesh'], mesh['gram_support'], case['branch'] == 'MTS-primary')
                flow, tangent, unused = restore_flow(evidence, digests, action, sources, case['level'])
                acceleration = flow['accelerations'][-1]
                polynomial, unused = prepare(action, loads, acceleration)
                directions = read(case['direction_path'])
                acceleration_vertices = transport_rate(engine, loads, action, directions['edge_vertices'], evidence, name)
                vertex_path = save(name + '-derived-acceleration', vertices=acceleration_vertices)
                paths, means = [], []
                for order, previous_path in zip([48, 64], case['material_paths']):
                    previous = read(previous_path)
                    values = []
                    for index, label in enumerate(previous['labels']):
                        if index % 16 == 0:
                            print(json.dumps(dict(stage=name + ':material' + str(order) + ':' + str(index), seconds=perf_counter() - started)), flush=True)
                            if perf_counter() > deadline:
                                raise RuntimeError('Safe completed-layer runtime boundary')
                        unused, raw, unused = layer(engine, loads, action, tangent, acceleration, polynomial,
                            directions['edge_vertices'], directions['field_vertices'], label, 12)
                        data = physical_data(engine, loads, action, label)
                        sampled = samples(action, label, 12)
                        cardinal = data['cardinal']
                        field_direction, edge_direction = cardinal @ directions['field_vertices'], cardinal @ directions['edge_vertices']
                        packet, direction = make_packet(engine, data, raw, sampled, acceleration, field_direction, edge_direction, 0.)
                        acceleration_nodes = cardinal @ acceleration_vertices
                        local = []
                        for power in range(3):
                            extra = correction(packet, acceleration_nodes, power)
                            frozen = previous['values'][index, 0, power]
                            combined = frozen[0] + extra
                            local.append([frozen[0], extra, combined, frozen[1], combined + frozen[1], frozen[4], frozen[8]])
                            if order == 64 and index == 31:
                                estimates = []
                                for step in [.1, .05, .025]:
                                    pair = [finite_wave_current(completed_packet(packet, direction, acceleration_nodes, sign * step), power)[2] for sign in [1, -1]]
                                    estimates.append((pair[0] - pair[1]) / (2 * step))
                                finite = (4 * estimates[2] - estimates[1]) / 3
                                error = finite - combined
                                evidence.check(name + ':completed_mixed_action:' + str(power), abs(error) <= 2e-14 + 1e-6 * abs(combined), float(error))
                                variations.append(dict(branch=case['branch'], level=case['level'], power=power,
                                    analytic=float(combined), finite=float(finite), difference=float(error)))
                        values.append(local)
                        if order == 64 and index == 31:
                            unused, raw8, unused = layer(engine, loads, action, tangent, acceleration, polynomial,
                                directions['edge_vertices'], directions['field_vertices'], label, 8)
                            sampled8 = samples(action, label, 8)
                            packet8, direction8 = make_packet(engine, data, raw8, sampled8, acceleration, field_direction, edge_direction, 0.)
                            for power in range(3):
                                total8 = wave_blocks(packet8, direction8, power)[0] + correction(packet8, acceleration_nodes, power)
                                difference = float(total8 - local[power][2])
                                evidence.check(name + ':spatial8_12:' + str(power), abs(difference) <= 2e-15, difference)
                                spatial_rows.append(dict(branch=case['branch'], level=case['level'], power=power, difference=difference))
                    values = np.array(values)
                    average = np.tensordot(previous['weights'], values, axes=(0, 0))
                    means.append(average)
                    paths.append(save(name + '-material' + str(order), labels=previous['labels'], weights=previous['weights'], values=values, average=average,
                        channels=np.array(['frozen_wave', 'derived_acceleration_correction', 'completed_wave', 'Gram', 'completed_total', 'amplitude_acceleration_coefficient', 'minimal_wave_control'])))
                    for power in range(3):
                        summaries.append(dict(branch=case['branch'], level=case['level'], material_order=order, power=power,
                            **dict(zip(['frozen_wave', 'derived_acceleration_correction', 'completed_wave', 'Gram', 'completed_total', 'amplitude_acceleration_coefficient', 'minimal_wave_control'], map(float, average[power])))))
                evidence.check(name + ':material48_64', np.max(abs(means[1] - means[0])) <= 2e-15, float(np.max(abs(means[1] - means[0]))))
                evidence.report['cases'].append(dict(branch=case['branch'], level=case['level'], vertex_path=vertex_path, material_paths=paths))
                evidence.save()
        for filename, rows in [('completed-support-shift-blocks.csv', summaries), ('completed-mixed-action-checks.csv', variations), ('completed-spatial-quadrature.csv', spatial_rows)]:
            path = evidence.output / filename
            with path.open('w', newline='', encoding='utf-8') as stream:
                writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
                writer.writeheader()
                writer.writerows(rows)
            evidence.own(path, 'outputs')
        evidence.report.update(seconds=perf_counter() - started, summaries=summaries, new_nonlinear_solves=0,
            new_trajectories=0, github_action=False, optimized_projection_time_derivative_computed=False,
            scope='Original direction only, with derived geometric acceleration completion; support force and metric constraints not refitted')
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    with contextlib.redirect_stderr(__import__('sys').stdout):
        main()
