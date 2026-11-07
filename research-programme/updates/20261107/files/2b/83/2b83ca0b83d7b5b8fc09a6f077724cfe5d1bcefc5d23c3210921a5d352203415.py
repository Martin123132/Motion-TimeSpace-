from derive_annular_source_gravity_20260914 import EvidenceRun
from derive_annular_support_map_constraints_20260927 import restore_case
from annular_nested_physical_refinement_v3_20260922 import restore_refined
from annular_candidate_hamiltonian_20260921 import decimals
from annular_acceleration_archive_checks_v2_20261001 import verify_report
from analyze_annular_source_flat_state_20261002 import read_archive
from annular_physical_native_kernel_20260928 import NativeKernel, maximum
from annular_quadratic_core_20261002 import physical_edges
from annular_decimal_transport_v2_20260919 import decimal_array
from construct_annular_native_curvature_repair_v2_20261002 import quintic
from annular_high_order_native_20261003 import high_mesh, HighKernel
from decimal import Decimal, localcontext
from fractions import Fraction
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
    evidence = EvidenceRun('annular-high-order-repair-preparation-attempt01', __file__)
    deadline = perf_counter() + 1800
    try:
        evidence.own(evidence.root / 'DERIVATION-20261003-live-higher-order-curvature-repair.md')
        base = 'source-intake/navier-stokes/20260914/'
        parent = verify_report(evidence, base + 'annular-live-native-transmission-third-attempt02/status.json')
        seal = evidence.output.parent / 'annular-live-refinement-time-jet-integrity-20261002.json'
        evidence.own(seal)
        digests = json.loads(seal.read_text())['hashes']
        packet = json.loads((evidence.root / parent['packet_path']).read_text())
        state_path = next(row['path'] for row in parent['states'] if row['name'] == 'iteration0')
        state = read_archive(evidence.root / state_path)
        old = read_archive(evidence.root / next(row['path'] for row in parent['results'] if row['name'] == 'primary-16-64'))
        mesh = high_mesh(packet['gram_support'], packet['mesh']['anchor'])
        with localcontext() as context:
            context.prec = 64
            unused, original, sources = restore_case(evidence, digests, 'MTS-primary', 'third', deadline)
            loads, action = restore_refined(original.owner, state, packet['mesh'], packet, 'primary', deadline)
            old_engine = NativeKernel(packet['mesh'], packet['gram_support'], True)
            engine = HighKernel(mesh, mesh['gram_support'], True)
            source = decimals(state['coordinates'])[:, -1]
            coordinates = np.full((len(source), mesh['count'] + 1), Decimal(0), dtype=object)
            coordinates[:, -1] = source
            reference_nodes = np.array([Decimal(Fraction(value).numerator) / Decimal(Fraction(value).denominator) for value in mesh['nodes']], dtype=object)
            anchor = engine.references[engine.anchor]
            lower, upper = engine.references[0], engine.references[-1]
            fraction = np.where(reference_nodes <= anchor, (reference_nodes - lower) / (anchor - lower), (upper - reference_nodes) / (upper - anchor))
            native_indices = np.r_[old_engine.indices[:, 0], old_engine.indices[-1, 2]][old_engine.native_edges]
            polynomial_rows, targets = [], []
            for index, label in enumerate(action.owner.layer_rule.points / 2):
                edges = physical_edges(old_engine, source[index], label, action.owner.width)
                native = edges[old_engine.native_edges]
                field = loads.coordinates[index, :-1]
                atom = old_engine.atoms(edges, field)
                before = np.r_[atom['slope_left'][0], atom['slope_right'][old_engine.native_edges[1:] - 1]]
                after = np.r_[atom['slope_left'][old_engine.native_edges[:-1]], atom['slope_right'][-1]]
                previous = np.r_[atom['second'][0], atom['second'][old_engine.native_edges[1:] - 1]]
                following = np.r_[atom['second'][old_engine.native_edges[:-1]], atom['second'][-1]]
                radius = np.asarray(native, float)
                metric, derivatives = action.solver.values(action.solution, radius)
                radial_metric = 1 - 2 * metric[0] / radius
                radial_metric_derivative = -2 * derivatives[0] / radius + 2 * metric[0] / radius**2
                speed = decimal_array(np.exp(2 * metric[1]) * radial_metric)
                drift = speed * decimal_array(2 / radius + derivatives[1] + radial_metric_derivative / (2 * radial_metric))
                displacement = np.array([(point - edges[0]) / (source[index] - edges[0]) if point < source[index]
                    else (edges[-1] - point) / (edges[-1] - source[index]) for point in native], dtype=object)
                native_acceleration = displacement * Decimal.from_float(float(old['acceleration'][index, -1]))
                mean = (following + previous) / 2
                jump = -(drift + native_acceleration) * (after - before) / speed
                incoming, outgoing = mean - jump / 2, mean + jump / 2
                values = field[native_indices]
                polynomial = np.column_stack([quintic(native, values, before, after, incoming, outgoing), np.full(len(native) - 1, Decimal(0), dtype=object)])
                source_cell = int(np.searchsorted(native, source[index], side='right') - 1)
                source_local = (source[index] - native[source_cell]) / (native[source_cell + 1] - native[source_cell])
                source_value = sum((coefficient * source_local**power for power, coefficient in enumerate(polynomial[source_cell])), Decimal(0))
                polynomial[source_cell] -= source_value / (source_local**3 * (1 - source_local)**3) * np.array([0, 0, 0, 1, -3, 3, -1], dtype=object)
                physical_lower = lower + Decimal.from_float(float(action.owner.width)) * Decimal.from_float(float(label))
                physical_upper = upper + Decimal.from_float(float(action.owner.width)) * Decimal.from_float(float(label))
                physical_nodes = np.where(reference_nodes <= anchor, physical_lower + (source[index] - physical_lower) * fraction,
                    physical_upper + (source[index] - physical_upper) * fraction)
                selected = np.clip(np.searchsorted(native, physical_nodes, side='right') - 1, 0, len(native) - 2)
                local = (physical_nodes - native[selected]) / np.diff(native)[selected]
                evaluated = np.full(len(local), Decimal(0), dtype=object)
                for power in reversed(range(7)):
                    evaluated = evaluated * local + polynomial[selected, power]
                evaluated[engine.native_indices] = values
                coordinates[index, :-1] = evaluated
                new_edges = physical_edges(engine, source[index], label, action.owner.width)
                new_atom = engine.atoms(new_edges, evaluated)
                new_before = np.r_[new_atom['slope_left'][0], new_atom['slope_right'][engine.native_edges[1:] - 1]]
                new_after = np.r_[new_atom['slope_left'][engine.native_edges[:-1]], new_atom['slope_right'][-1]]
                new_previous = np.r_[new_atom['curvature_left'][0], new_atom['curvature_right'][engine.native_edges[1:] - 1]]
                new_following = np.r_[new_atom['curvature_left'][engine.native_edges[:-1]], new_atom['curvature_right'][-1]]
                jet_error = max(maximum(new_before - before), maximum(new_after - after), maximum(new_previous - incoming), maximum(new_following - outgoing))
                evidence.check('vertex' + str(index) + ':exact_high_order_native_jets', jet_error < Decimal('1e-30'), str(jet_error))
                evidence.check('vertex' + str(index) + ':same_native_samples', np.array_equal(evaluated[engine.native_indices], values))
                evidence.check('vertex' + str(index) + ':source_first_slope_continuity', abs(new_atom['slope_left'][engine.anchor] - new_atom['slope_right'][engine.anchor - 1]) < Decimal('1e-35'))
                polynomial_rows.append(np.asarray(polynomial, str))
                targets.append(np.asarray([values, before, after, incoming, outgoing], str))
        evidence.check('parent_material_vertices', len(source) == 15)
        evidence.check('unchanged_native_support', len(mesh['gram_support']) == 1094 and mesh['gram_support'] == packet['gram_support'])
        path = evidence.output / 'P6-initial.npz'
        np.savez_compressed(path, coordinates=np.asarray(coordinates, str), rates=np.zeros(coordinates.shape),
            polynomial=np.array(polynomial_rows), native_targets=np.array(targets), labels=action.owner.layer_rule.points / 2)
        evidence.own(path, 'outputs')
        mesh_path = evidence.output / 'P6-mesh.json'
        mesh_path.write_text(json.dumps(mesh) + '\n')
        evidence.own(mesh_path, 'outputs')
        evidence.report.update(mesh_path=str(mesh_path.relative_to(evidence.root)), initial_path=str(path.relative_to(evidence.root)),
            field_count=mesh['count'], degree=6, native_support=1094, material_vertices=15, own_metric_solved=False,
            full_acceleration_solved=False, github_action=False, subagents_used=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
