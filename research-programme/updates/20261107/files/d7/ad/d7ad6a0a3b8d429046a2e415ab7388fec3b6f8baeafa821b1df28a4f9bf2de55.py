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
from decimal import Decimal, localcontext
from time import perf_counter
import ctypes
import json
import numpy as np


def main():
    kernel = ctypes.windll.kernel32
    kernel.GetCurrentProcess.restype = ctypes.c_void_p
    kernel.SetProcessAffinityMask.argtypes = [ctypes.c_void_p, ctypes.c_size_t]
    if not kernel.SetProcessAffinityMask(kernel.GetCurrentProcess(), 1 << 4):
        raise OSError('Affinity failed')
    evidence = EvidenceRun('annular-high-order-time-jet-attempt01', __file__)
    started, deadline = perf_counter(), perf_counter() + 7200
    try:
        base = 'source-intake/navier-stokes/20260914/'
        parent = verify_report(evidence, base + 'annular-high-order-live-primary-attempt02/status.json')
        evidence.check('live_initial_candidate', parent['state'] == 'complete' and parent['initial_candidate'])
        state = read_archive(evidence.root / parent['states'][0]['path'])
        high = next(row for row in parent['results'] if row['material'] == 64)
        acceleration = read_archive(evidence.root / high['path'])['acceleration']
        mesh = json.loads((evidence.root / parent['mesh_path']).read_text())
        seal = evidence.output.parent / 'annular-live-refinement-time-jet-integrity-20261002.json'
        evidence.own(seal)
        digests = json.loads(seal.read_text())['hashes']
        with localcontext() as context:
            context.prec = 64
            unused, original, sources = restore_case(evidence, digests, 'MTS-primary', 'third', deadline)
            owner = adapt_owner(original.owner, mesh)
            coordinates, exact_acceleration = decimals(state['coordinates']), decimal_array(acceleration)
        labels = np.unique(np.r_[-.5, np.polynomial.legendre.leggauss(9)[0] / 2, .5])
        amounts = [2e-8, 5e-9, 1.25e-9]
        evidence.report.update(probes=[], amounts=amounts, labels=labels.tolist(), degree=6,
            actual_acceleration_source=high['path'], includes_velocity_squared_radial_response=True,
            includes_moving_jump_velocity_squared=True, physical_trajectory=False,
            uniform_material_claim=False, github_action=False, subagents_used=False)
        def progress(stage):
            evidence.report['progress'] = dict(stage=stage, seconds=perf_counter() - started)
            evidence.save()
            print(json.dumps(evidence.report['progress']), flush=True)
            if perf_counter() > deadline:
                raise RuntimeError('Safe higher-order time-jet boundary')
        baseline = None
        estimates = []
        for number, amount in enumerate([0.] + amounts):
            progress('own radial jet ' + str(number))
            with localcontext() as context:
                context.prec = 64
                changed = coordinates + Decimal.from_float(amount) * exact_acceleration
            rates = np.sqrt(2 * amount) * acceleration
            loads, action = live_high(owner, changed, rates, mesh, 'primary', deadline)
            engine = loads.native_engine
            radial = float(np.max(abs(action.solver.residual(action.solution['state'], 'primary'))))
            evidence.check('jet' + str(number) + ':own_radial_constraint', radial < 8e-14, radial)
            shape_rows, acceleration_forms, fixed_field_forms, jumps, points = [], [], [], [], []
            with localcontext() as context:
                context.prec = 64
                for label in labels:
                    data = physical_data(engine, loads, action, label)
                    result = engine.evaluate(data['edges'], data['field'], data['beta'], data['beta_radial'])
                    movement = movements(engine, data['edges'], data['source'])
                    shape_rows.append(transport_shapes(engine, result, movement))
                    cardinal = decimal_array(data['cardinal'])
                    for field, target in [(coordinates[:, :-1].T @ cardinal, fixed_field_forms),
                            (exact_acceleration[:, :-1].T @ cardinal, acceleration_forms)]:
                        probe = engine.evaluate(data['edges'], field, data['beta'], data['beta_radial'])
                        target.append(transport_shapes(engine, probe, movement))
                    selected = engine.native_edges[1:-1]
                    atom = result['atoms']
                    before, after = atom['slope_right'][selected - 1], atom['slope_left'][selected]
                    load = result['field_gradient'][engine.native_indices[1:-1]]
                    radius = np.asarray(data['edges'][selected], float)
                    metric = action.solver.values(action.solution, radius)[0]
                    speed_square = np.exp(2 * metric[1]) * (1 - 2 * metric[0] / radius)
                    velocity = data['source_velocity'] * data['displacement'][selected]
                    alpha = data['beta'][1:-1] / decimal_array(speed_square)
                    coefficient = data['beta'][1:-1] - alpha * velocity**2
                    jumps.append(np.asarray(coefficient * (after - before) - load, float))
                    points.append(np.asarray(load * (before + after) / 2 + result['edge_gradient'][selected], float))
            shape_rows, acceleration_forms, fixed_field_forms, jumps, points = map(np.array,
                [shape_rows, acceleration_forms, fixed_field_forms, jumps, points])
            output = dict(shape=shape_rows, acceleration_form=acceleration_forms, fixed_field_form=fixed_field_forms,
                moving_jump=jumps, point_balance=points, labels=labels, amount=np.array(amount),
                coordinates=np.asarray(changed, str), rates=rates, edges=action.solver.edges, **action.solution)
            if amount == 0:
                baseline = dict(shape=shape_rows, jump=jumps, point=points)
                evidence.report.update(baseline_shape_max=float(np.max(abs(shape_rows))),
                    baseline_moving_jump_max=float(np.max(abs(jumps))), baseline_point_max=float(np.max(abs(points))))
            else:
                raw = (shape_rows - baseline['shape']) / amount
                corrected = raw - amount * acceleration_forms
                geometry = (fixed_field_forms - baseline['shape']) / amount
                moving = (jumps - baseline['jump']) / amount
                point = (points - baseline['point']) / amount
                output.update(raw=raw, corrected=corrected, geometry=geometry, moving_jump_second=moving, point_second=point)
                estimates.append(dict(shape=corrected, jump=moving, point=point))
            path = evidence.output / ('jet' + str(number) + '.npz')
            np.savez_compressed(path, **output)
            evidence.own(path, 'outputs')
            row = dict(amount=amount, path=str(path.relative_to(evidence.root)), radial_residual=radial, valid_for_claim=False)
            if amount:
                row.update(shape_second_max=float(np.max(abs(corrected))), geometry_second_max=float(np.max(abs(geometry))),
                    moving_jump_second_max=float(np.max(abs(moving))), point_second_max=float(np.max(abs(point))))
            evidence.report['probes'].append(row)
            evidence.save()
        witnesses = {}
        for name in ['shape', 'jump', 'point']:
            coarse = (4 * estimates[1][name] - estimates[0][name]) / 3
            fine = (4 * estimates[2][name] - estimates[1][name]) / 3
            index = np.unravel_index(np.argmax(abs(fine)), fine.shape)
            difference = float(np.max(abs(fine - coarse)))
            witnesses[name] = dict(maximum=float(np.max(abs(fine))), label=float(labels[index[0]]),
                column=int(index[1]), signed=float(fine[index]), Richardson_difference=difference,
                relative_step_difference=difference / float(np.max(abs(fine))) if np.max(abs(fine)) else None)
        evidence.report.update(seconds=perf_counter() - started, witnesses=witnesses, propagation_pass_claimed=False,
            result='Higher-order second jets computed from the complete coupled acceleration; not a time trajectory.')
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()

