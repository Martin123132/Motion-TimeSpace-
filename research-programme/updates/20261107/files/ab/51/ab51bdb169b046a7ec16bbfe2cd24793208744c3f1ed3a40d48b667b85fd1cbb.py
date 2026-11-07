from derive_annular_source_gravity_20260914 import EvidenceRun
from derive_annular_support_map_constraints_20260927 import restore_case
from annular_nested_physical_refinement_v3_20260922 import adapt_owner, restore_refined
from annular_acceleration_archive_checks_v2_20261001 import verify_report
from annular_physical_native_kernel_20260928 import NativeKernel, maximum
from derive_annular_native_shape_stress_20260928 import physical_data
from analyze_annular_source_flat_state_20261002 import read_archive
from annular_decimal_transport_v2_20260919 import decimal_array
from decimal import Decimal, localcontext
from time import perf_counter
import ctypes
import json
import numpy as np


def quintic(native, values, incoming, outgoing, curvature_in, curvature_out):
    basis = np.array([[1, 0, 0, -10, 15, -6], [0, 0, 0, 10, -15, 6],
        [0, 1, 0, -6, 8, -3], [0, 0, 0, -4, 7, -3],
        [0, 0, 1, -3, 3, -1], [0, 0, 0, 1, -2, 1]], dtype=object)
    width = np.diff(native)
    data = np.column_stack([values[:-1], values[1:], width * outgoing[:-1], width * incoming[1:],
        width**2 * curvature_out[:-1] / 2, width**2 * curvature_in[1:] / 2])
    return data @ basis


def main():
    kernel = ctypes.windll.kernel32
    kernel.GetCurrentProcess.restype = ctypes.c_void_p
    kernel.SetProcessAffinityMask.argtypes = [ctypes.c_void_p, ctypes.c_size_t]
    if not kernel.SetProcessAffinityMask(kernel.GetCurrentProcess(), 1 << 4):
        raise OSError('Affinity failed')
    evidence = EvidenceRun('annular-native-curvature-repair-attempt02', __file__)
    deadline = perf_counter() + 1800
    try:
        evidence.own(evidence.root / 'DERIVATION-20261002-native-curvature-corner-repair.md')
        evidence.own(evidence.root / 'DERIVATION-20261002-quintic-source-anchor-lift.md')
        base = 'source-intake/navier-stokes/20260914/'
        seal = evidence.output.parent / 'annular-quadratic-transmission-integrity-20261002.json'
        evidence.own(seal)
        digests = json.loads(seal.read_text())['hashes']
        with localcontext() as context:
            context.prec = 64
            unused, original, sources = restore_case(evidence, digests, 'MTS-primary', 'third', deadline)
        labels = np.unique(np.r_[-.5, np.polynomial.legendre.leggauss(9)[0] / 2, .5])
        for level, authority in [('third', 'annular-live-native-transmission-third-attempt02'),
                                 ('fourth', 'annular-live-native-transmission-fourth-primary-attempt03')]:
            report = verify_report(evidence, base + authority + '/status.json')
            evidence.check(level + ':complete_authority', report['state'] == 'complete')
            packet = json.loads((evidence.root / report['packet_path']).read_text())
            state_path = next(row['path'] for row in report['states'] if row['name'] == 'iteration0') if level == 'third' else report['state_path']
            state = read_archive(evidence.root / state_path)
            high = next(row for row in report['results'] if row['name'] == 'primary-16-64')
            acceleration = read_archive(evidence.root / high['path'])['acceleration']
            coefficients, old_corners, new_corners, native_rows, energy_rows, target_jets = [], [], [], [], [], []
            with localcontext() as context:
                context.prec = 64
                owner = adapt_owner(original.owner, packet['mesh'])
                loads, action = restore_refined(owner, state, packet['mesh'], packet, 'primary', deadline)
                engine = NativeKernel(packet['mesh'], packet['gram_support'], True)
                native_indices = np.r_[engine.indices[:, 0], engine.indices[-1, 2]][engine.native_edges]
                for label in labels:
                    data = physical_data(engine, loads, action, label)
                    atoms = engine.atoms(data['edges'], data['field'])
                    native = data['edges'][engine.native_edges]
                    before = np.r_[atoms['slope_left'][0], atoms['slope_right'][engine.native_edges[1:] - 1]]
                    after = np.r_[atoms['slope_left'][engine.native_edges[:-1]], atoms['slope_right'][-1]]
                    curv_before = np.r_[atoms['second'][0], atoms['second'][engine.native_edges[1:] - 1]]
                    curv_after = np.r_[atoms['second'][engine.native_edges[:-1]], atoms['second'][-1]]
                    metric, unused = action.solver.values(action.solution, np.asarray(native, float))
                    speed_square = decimal_array(np.exp(2 * metric[1]) * (1 - 2 * metric[0] / np.asarray(native, float)))
                    drift = speed_square * data['beta_radial'] / data['beta']
                    source_acceleration = Decimal.from_float(float(data['cardinal'] @ acceleration[:, -1]))
                    knot_acceleration = data['displacement'][engine.native_edges] * source_acceleration
                    old = speed_square * (curv_after - curv_before) + (drift + knot_acceleration) * (after - before)
                    mean = (curv_after + curv_before) / 2
                    target = -(drift + knot_acceleration) * (after - before) / speed_square
                    new_before, new_after = mean - target / 2, mean + target / 2
                    values = data['field'][native_indices]
                    polynomial = np.column_stack([quintic(native, values, before, after, new_before, new_after), np.full(len(native) - 1, Decimal(0), dtype=object)])
                    width = np.diff(native)
                    source_cell = int(np.searchsorted(native, data['source'], side='right') - 1)
                    source_local = (data['source'] - native[source_cell]) / width[source_cell]
                    initial_source = sum((coefficient * source_local**power for power, coefficient in enumerate(polynomial[source_cell])), Decimal(0))
                    source_bubble = source_local**3 * (1 - source_local)**3
                    evidence.check(level + ':' + str(label) + ':interior_source_anchor', source_bubble > 0)
                    polynomial[source_cell] -= initial_source / source_bubble * np.array([0, 0, 0, 1, -3, 3, -1], dtype=object)
                    powers = np.arange(7)
                    value_error = max(maximum(polynomial[:, 0] - values[:-1]), maximum(np.sum(polynomial, axis=1) - values[1:]))
                    slope_error = max(maximum(polynomial[:, 1] / width - after[:-1]), maximum(np.sum(polynomial * powers, axis=1) / width - before[1:]))
                    curve_error = max(maximum(2 * polynomial[:, 2] / width**2 - new_after[:-1]),
                        maximum(np.sum(polynomial * powers * (powers - 1), axis=1) / width**2 - new_before[1:]))
                    repaired = speed_square * (new_after - new_before) + (drift + knot_acceleration) * (after - before)
                    evidence.check(level + ':' + str(label) + ':quintic_boundary_jets', value_error < Decimal('1e-40') and slope_error < Decimal('1e-35') and curve_error < Decimal('1e-30'),
                        dict(value=str(value_error), slope=str(slope_error), curvature=str(curve_error)))
                    evidence.check(level + ':' + str(label) + ':frozen_corner_repaired', maximum(repaired[1:-1]) < Decimal('1e-35'), str(maximum(repaired[1:-1])))
                    source_cell = int(np.searchsorted(native, data['source'], side='right') - 1)
                    source_local = (data['source'] - native[source_cell]) / width[source_cell]
                    source_value = sum((coefficient * source_local**power for power, coefficient in enumerate(polynomial[source_cell])), Decimal(0))
                    evidence.check(level + ':' + str(label) + ':source_value_retained', abs(source_value) < Decimal('1e-45'), str(source_value))
                    coefficients.append(np.asarray(polynomial, str))
                    native_rows.append(np.asarray(native, str))
                    old_corners.append(np.asarray(old[1:-1], float))
                    new_corners.append(np.asarray(repaired[1:-1], float))
                    target_jets.append(np.asarray([values, before, after, new_before, new_after], str))
                    energy = []
                    for order in [12, 20]:
                        nodes, weights = np.polynomial.legendre.leggauss(order)
                        native_float = np.asarray(native, float)
                        cuts = np.unique(np.r_[native_float, action.solver.edges])
                        cuts = cuts[(cuts >= native_float[0]) & (cuts <= native_float[-1])]
                        radius = ((cuts[:-1] + cuts[1:])[:, None] + np.diff(cuts)[:, None] * nodes) / 2
                        measure = np.diff(cuts)[:, None] * weights / 2
                        cells = np.clip(np.searchsorted(native_float, radius.ravel(), side='right') - 1, 0, len(native_float) - 2)
                        local = (radius.ravel() - native_float[cells]) / np.asarray(width, float)[cells]
                        derivative = np.asarray(polynomial, float)[:, 1:] * np.arange(1, 7)
                        slope = np.polynomial.polynomial.polyval(local, derivative[cells].T, tensor=False) / np.asarray(width, float)[cells]
                        metric_at, unused = action.solver.values(action.solution, radius.ravel())
                        beta = radius.ravel()**2 * np.exp(metric_at[1]) * np.sqrt(1 - 2 * metric_at[0] / radius.ravel())
                        energy.append(float(measure.ravel() @ (beta * slope**2 / 2)))
                    evidence.check(level + ':' + str(label) + ':wave_energy_quadrature', abs(energy[0] - energy[1]) < 1e-11 * max(energy))
                    energy_rows.append(energy)
            path = evidence.output / (level + '-quintic.npz')
            np.savez_compressed(path, coefficients=np.array(coefficients), native=np.array(native_rows), labels=labels,
                old_corners=old_corners, new_corners=new_corners, target_jets=np.array(target_jets), wave_energy=energy_rows)
            evidence.own(path, 'outputs')
            evidence.report['cases'].append(dict(level=level, path=str(path.relative_to(evidence.root)),
                old_corner_max=float(np.max(abs(np.asarray(old_corners)))), repaired_corner_max=float(np.max(abs(np.asarray(new_corners)))),
                maximum_wave_energy=float(np.max(energy_rows)), frozen_metric=True, own_new_metric_solved=False,
                live_coupled_acceleration_recomputed=False, initial_profile_changed=True, native_values_and_first_slopes_preserved=True,
                second_order_shape_preservation_solved=False, valid_for_claim=False))
            evidence.save()
        evidence.report.update(github_action=False, subagents_used=False, physical_trajectory_computed=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
