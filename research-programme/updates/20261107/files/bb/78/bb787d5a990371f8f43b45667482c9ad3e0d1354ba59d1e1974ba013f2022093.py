from derive_annular_source_gravity_20260914 import EvidenceRun
from derive_annular_support_map_constraints_20260927 import restore_case
from annular_acceleration_archive_checks_v2_20261001 import verify_report
from annular_high_order_native_v2_20261003 import adapt_owner, live_high
from annular_high_order_coupled_v2_20261003 import transport_shapes
from annular_source_flat_native_20261002 import movements
from annular_candidate_hamiltonian_20260921 import decimals
from annular_decimal_transport_v2_20260919 import decimal_array
from derive_annular_native_shape_stress_20260928 import physical_data
from analyze_annular_source_flat_state_20261002 import read_archive
from construct_annular_septic_response_20261003 import pin, metric_jets, third
from separate_annular_high_order_source_hinge_20261003 import hinge_transport
from decimal import Decimal, localcontext
from time import perf_counter
import json
import numpy as np


def main():
    pin(2)
    evidence = EvidenceRun('annular-septic-time-response-attempt01', __file__)
    started, deadline = perf_counter(), perf_counter() + 7200
    try:
        base = 'source-intake/navier-stokes/20260914/'
        parent = verify_report(evidence, base + 'annular-septic-live-primary-attempt01/status.json')
        previous = verify_report(evidence, base + 'annular-high-order-time-jet-attempt01/status.json')
        separated = verify_report(evidence, base + 'annular-high-order-source-hinge-separation-attempt01/status.json')
        evidence.check('coupled_solve_complete', parent['state'] == 'complete')
        state = read_archive(evidence.root / parent['states'][0]['path'])
        high = next(row for row in parent['results'] if row['material'] == 64)
        acceleration = read_archive(evidence.root / high['path'])['acceleration']
        mesh = json.loads((evidence.root / parent['mesh_path']).read_text())
        seal = evidence.output.parent / 'annular-high-order-source-separation-integrity-20261003.json'
        evidence.own(seal)
        seal_data = json.loads(seal.read_text())
        with localcontext() as context:
            context.prec = 64
            unused, original, sources = restore_case(evidence, seal_data['hashes'], 'MTS-primary', 'third', deadline)
            owner = adapt_owner(original.owner, mesh)
            coordinates, exact_acceleration = decimals(state['coordinates']), decimal_array(acceleration)
        labels = np.array(previous['labels'])
        amounts = previous['amounts']
        evidence.report.update(probes=[], amounts=amounts, labels=labels.tolist(), degree=7,
            inherited_initial_gates_passed=parent['initial_candidate'], actual_acceleration_source=high['path'],
            includes_velocity_squared_radial_response=True, includes_moving_jump_velocity_squared=True,
            physical_trajectory=False, uniform_material_claim=False, github_action=False, subagents_used=False)
        def progress(stage):
            evidence.report['progress'] = dict(stage=stage, seconds=perf_counter() - started)
            evidence.save()
            print(json.dumps(evidence.report['progress']), flush=True)
            if perf_counter() > deadline:
                raise RuntimeError('Safe septic time-response boundary')
        records, bulk_records = [], []
        for number, amount in enumerate([0.] + amounts):
            progress('own septic radial jet ' + str(number))
            with localcontext() as context:
                context.prec = 64
                changed = coordinates + Decimal.from_float(amount) * exact_acceleration
                rates = np.sqrt(2 * amount) * acceleration
                loads, action = live_high(owner, changed, rates, mesh, 'primary', deadline)
                engine = loads.native_engine
                radial = float(np.max(abs(action.solver.residual(action.solution['state'], 'primary'))))
                evidence.check('jet' + str(number) + ':own_radial_constraint', radial < 8e-14, radial)
                rows = {name: [] for name in ['shape', 'ordinary_shape', 'hinge_shape', 'jump', 'point', 'T', 'A', 'C', 'beta', 'J']}
                for label in labels:
                    data = physical_data(engine, loads, action, label)
                    result = engine.evaluate(data['edges'], data['field'], data['beta'], data['beta_radial'])
                    movement = movements(engine, data['edges'], data['source'])
                    atom = result['atoms']
                    selected = engine.native_edges[1:-1]
                    before, after = atom['slope_right'][selected - 1], atom['slope_left'][selected]
                    mean = np.r_[atom['slope_left'][0], (after + before) / 2, atom['slope_right'][-1]]
                    partial_point = result['native_field'] * mean + result['native_shape']
                    ordinary = np.asarray(partial_point @ movement[engine.native_edges], float)
                    channel = np.asarray(result['jump_covector'] * hinge_transport(engine, atom, movement), float)
                    full = transport_shapes(engine, result, movement)
                    scale = max(np.max(abs(full)), np.max(abs(ordinary)), np.max(abs(channel)), 1e-50)
                    chain_error = float(np.max(abs(full - ordinary - channel)) / scale)
                    evidence.check('jet' + str(number) + ':' + str(label) + ':source_chain_rule', chain_error < 2e-12, chain_error)
                    geometry = metric_jets(action.solver, action.solution, np.asarray(data['edges'][engine.native_edges], float))
                    velocity = data['source_velocity'] * data['displacement'][selected]
                    coefficient = data['beta'][1:-1] * (1 - velocity**2 / geometry['speed'][1:-1])
                    for key, value in [('shape', full), ('ordinary_shape', ordinary), ('hinge_shape', channel),
                            ('jump', coefficient * (after - before) - result['native_field'][1:-1]),
                            ('point', partial_point[1:-1]), ('T', result['jump_covector']), ('A', result['native_field']),
                            ('C', result['native_shape']), ('beta', data['beta']), ('J', result['source_jump'])]:
                        rows[key].append(np.asarray(value, float))
                    if number == 0:
                        cardinal = decimal_array(data['cardinal'])
                        field_acceleration = exact_acceleration[:, :-1].T @ cardinal
                        source_acceleration = sum(exact_acceleration[:, -1] * cardinal, Decimal(0))
                        acceleration_atom = engine.atoms(data['edges'], field_acceleration)
                        width_acceleration = np.diff(data['displacement']) * source_acceleration
                        weak_before = acceleration_atom['slope_right'][selected - 1] - before * width_acceleration[selected - 1] / atom['widths'][selected - 1]
                        weak_after = acceleration_atom['slope_left'][selected] - after * width_acceleration[selected] / atom['widths'][selected]
                        native_acceleration = data['displacement'][engine.native_edges] * source_acceleration
                        factor = geometry['speed_first'] + geometry['drift'] + native_acceleration
                        ell = third(atom)
                        strong_before = geometry['speed'][1:-1] * ell[selected - 1, 1] + factor[1:-1] * atom['curvature_right'][selected - 1] + geometry['drift_first'][1:-1] * before
                        strong_after = geometry['speed'][1:-1] * ell[selected, 0] + factor[1:-1] * atom['curvature_left'][selected] + geometry['drift_first'][1:-1] * after
                        material_before = geometry['speed'][1:-1] * atom['curvature_right'][selected - 1] + (geometry['drift'] + native_acceleration)[1:-1] * before
                        material_after = geometry['speed'][1:-1] * atom['curvature_left'][selected] + (geometry['drift'] + native_acceleration)[1:-1] * after
                        nodal = field_acceleration[engine.native_indices[1:-1]]
                        bulk_records.append(dict(label=float(label), weak_before=np.asarray(weak_before, float), weak_after=np.asarray(weak_after, float),
                            strong_before=np.asarray(strong_before, float), strong_after=np.asarray(strong_after, float),
                            nodal_acceleration=np.asarray(nodal, float), bulk_before=np.asarray(material_before, float), bulk_after=np.asarray(material_after, float)))
            arrays = {key: np.array(value) for key, value in rows.items()}
            records.append(arrays)
            path = evidence.output / ('jet' + str(number) + '.npz')
            np.savez_compressed(path, **arrays, labels=labels, amount=np.array(amount), coordinates=np.asarray(changed, str), rates=rates,
                edges=action.solver.edges, **action.solution)
            evidence.own(path, 'outputs')
            evidence.report['probes'].append(dict(amount=amount, path=str(path.relative_to(evidence.root)), radial_residual=radial, valid_for_claim=False))
            evidence.save()
        witnesses = {}
        for name in ['shape', 'ordinary_shape', 'hinge_shape', 'jump', 'point', 'T']:
            estimates = [(row[name] - records[0][name]) / amount for row, amount in zip(records[1:], amounts)]
            coarse = (4 * estimates[1] - estimates[0]) / 3
            fine = (4 * estimates[2] - estimates[1]) / 3
            index = np.unravel_index(np.argmax(abs(fine)), fine.shape)
            witnesses[name] = dict(maximum=float(np.max(abs(fine))), label=float(labels[index[0]]),
                column=int(index[1]) if len(index) > 1 else None, signed=float(fine[index]),
                Richardson_difference=float(np.max(abs(fine - coarse))), initial_maximum=float(np.max(abs(records[0][name]))))
        bulk_arrays = {key: np.array([row[key] for row in bulk_records]) for key in bulk_records[0]}
        path = evidence.output / 'strong-weak-response.npz'
        np.savez_compressed(path, **bulk_arrays)
        evidence.own(path, 'outputs')
        ratios = dict(shape=witnesses['shape']['maximum'] / previous['witnesses']['shape']['maximum'],
            ordinary_point=witnesses['point']['maximum'] / separated['witnesses']['ordinary_point']['maximum'],
            source=witnesses['T']['maximum'] / seal_data['source_slope_covector_second_jet']['second_maximum'])
        evidence.report.update(seconds=perf_counter() - started, witnesses=witnesses, P7_over_P6=ratios,
            all_three_improved=all(value < 1 for value in ratios.values()),
            slope_response_strong_weak_gap=float(max(np.max(abs(bulk_arrays['weak_before'] - bulk_arrays['strong_before'])), np.max(abs(bulk_arrays['weak_after'] - bulk_arrays['strong_after'])))),
            value_response_strong_weak_gap=float(max(np.max(abs(bulk_arrays['nodal_acceleration'] - bulk_arrays['bulk_before'])), np.max(abs(bulk_arrays['nodal_acceleration'] - bulk_arrays['bulk_after'])))),
            propagation_pass_claimed=False, result='New P7 complete-action response measured; inherited frozen target is not a fixed-point certificate.')
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
