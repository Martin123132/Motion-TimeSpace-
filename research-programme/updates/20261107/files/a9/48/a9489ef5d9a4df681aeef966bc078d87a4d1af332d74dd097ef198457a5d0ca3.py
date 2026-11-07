from derive_annular_source_gravity_20260914 import EvidenceRun
from validate_annular_native_shape_stress_v2_20260928 import DirectNodalKernel, archive, decimal_array, maximum
from annular_candidate_energy_current_20260921 import reconstructed_solver
from decimal import Decimal, localcontext
from datetime import datetime
from fractions import Fraction
from time import perf_counter
import contextlib
import csv
import hashlib
import json
import numpy as np
import sympy as sp


ZERO = Decimal(0)


def positions_and_columns(kernel, edges, count):
    positions = np.full(count, ZERO, dtype=object)
    edge_columns = np.r_[kernel.elements[0, 0], kernel.elements[:, 2]]
    for cell, columns in enumerate(kernel.elements):
        for column, point in zip(columns, [edges[cell], (edges[cell] + edges[cell + 1]) / 2, edges[cell + 1]]):
            if column >= 0:
                positions[column] = point
    return positions, edge_columns


def direct_gradient(kernel, edges, field, beta, result):
    gradient = np.full(len(field), ZERO, dtype=object)
    if not kernel.enabled:
        return gradient
    weights = kernel.apply(1, beta)
    kernel_covector = kernel.apply(0, weights * result['image'], True)
    points = edges[kernel.native]
    native_covector = np.full(len(points), ZERO, dtype=object)
    for index, dual in enumerate(kernel_covector):
        stencil = points[index:index + 4]
        width = (stencil[3] - stencil[0]) / 3
        for local in range(4):
            denominator = Decimal(1)
            for other in range(4):
                if local != other:
                    denominator *= stencil[local] - stencil[other]
            native_covector[index + local] += dual * 6 * width**2 * width.sqrt() / denominator
    unused, edge_columns = positions_and_columns(kernel, edges, len(field))
    for edge, dual in zip(kernel.native, native_covector):
        if edge_columns[edge] >= 0:
            gradient[edge_columns[edge]] += dual
    hinge = np.array([max(point - edges[kernel.anchor], ZERO) for point in points], dtype=object)
    jump_covector = sum(native_covector * hinge, ZERO)
    for cell, coefficients in [(kernel.anchor - 1, [-1, 4, -3]), (kernel.anchor, [-3, 4, -1])]:
        width = edges[cell + 1] - edges[cell]
        for column, coefficient in zip(kernel.elements[cell], coefficients):
            if column >= 0:
                gradient[column] -= jump_covector * int(coefficient) / width
    return gradient


def interval_moments(source, field_positions, field_power, native_positions, atom_power, local_power):
    coefficients = list(zip(field_positions, -field_power)) + list(zip(native_positions, atom_power))
    events = [(point, -value) for point, value in coefficients]
    events.append((source, sum((value for point, value in coefficients), ZERO)))
    events.sort(key=lambda item: item[0])
    moments = np.full(3, ZERO, dtype=object)
    current = ZERO
    for index, (point, change) in enumerate(events):
        current += change
        if index + 1 < len(events):
            endpoint = events[index + 1][0]
            for power in range(3):
                moments[power] += current * ((endpoint - 6)**(power + 1) - (point - 6)**(power + 1)) / (power + 1)
    for power in range(3):
        values = np.full(len(native_positions), Decimal(1), dtype=object) if not power else (native_positions - 6)**power
        moments[power] += sum(local_power * values, ZERO)
    return moments, current


def main():
    evidence = EvidenceRun('annular-native-time-current-validation-attempt01', __file__)
    started = perf_counter()
    try:
        parent_path = evidence.output.parent / 'annular-native-time-current-attempt01/status.json'
        parent = json.loads(parent_path.read_text())
        evidence.check('time_current_complete', parent['state'] == 'complete' and all(row['passed'] for row in parent['checks']))
        evidence.own(parent_path)
        digests = {}
        for category in ['inputs', 'outputs']:
            for relative, digest in parent[category].items():
                if relative in digests and digests[relative] != digest:
                    raise RuntimeError('Conflicting source digests')
                digests[relative] = digest
        for relative, digest in digests.items():
            path = evidence.root / relative
            evidence.check('hash:' + relative, path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest() == digest)
            evidence.own(path)
        tables = {}
        for filename, count in [('native-current-comparison.csv', 36), ('native-time-variations.csv', 144), ('wave-areal-momentum.csv', 72)]:
            with (parent_path.parent / filename).open(newline='') as handle:
                rows = list(csv.DictReader(handle))
            evidence.check('CSV:' + filename, len(rows) == count and all(None not in row and None not in row.values() for row in rows))
            tables[filename] = rows
        sources = json.loads((evidence.output.parent / 'annular-native-shape-stress-attempt01/status.json').read_text())
        replay_rows, wave_comparisons = [], []
        with localcontext() as context:
            context.prec = 84
            for case in sources['cases']:
                packet = json.loads((evidence.root / case['sources']['packet']).read_text())
                kernel = DirectNodalKernel(packet['mesh'], packet['gram_support'], case['branch'] == 'MTS-primary')
                solver, solution = reconstructed_solver(archive(evidence.root / case['sources']['state']))
                reference_edges = np.array([Decimal(Fraction(value).numerator) / Decimal(Fraction(value).denominator) for value in packet['mesh']['edges']], dtype=object)
                print(json.dumps(dict(stage=case['branch'] + '-' + case['level'], seconds=perf_counter() - started)), flush=True)
                for probe, path in enumerate(case['probe_paths']):
                    raw = archive(evidence.root / path)
                    edges, field, rate, beta, beta_r, displacement = [decimal_array(raw[name]) for name in ['edges', 'field', 'rate', 'beta', 'beta_radial', 'displacement']]
                    source_speed = Decimal(str(raw['source_velocity']))
                    mesh_speed = source_speed * displacement
                    result = kernel.evaluate(edges, field, beta, edge_rate=mesh_speed, field_rate=rate)
                    gradient = direct_gradient(kernel, edges, field, beta, result)
                    evidence.check(path + ':independent_direct_field_covector', maximum(gradient - decimal_array(raw['field_gradient'])) <= Decimal('1e-30') * max(maximum(gradient), Decimal('1e-80')))
                    field_positions, unused = positions_and_columns(kernel, edges, len(field))
                    atoms = beta * kernel.apply(1, result['image'] * result['image_rate'], True)
                    atoms += beta_r * mesh_speed[kernel.native] * result['load']
                    local_power = beta * result['load'] * mesh_speed[kernel.native]
                    measured, tail = interval_moments(edges[kernel.anchor], field_positions, gradient * rate, edges[kernel.native], atoms, local_power)
                    scale = max(sum(abs(gradient * rate), ZERO), sum(abs(atoms), ZERO), sum(abs(local_power), ZERO), Decimal('1e-80'))
                    evidence.check(path + ':current_outside_support', abs(tail) <= Decimal('1e-30') * scale)
                    jacobians = np.diff(edges) / np.diff(reference_edges)
                    jacobian_rates = np.diff(mesh_speed) / np.diff(reference_edges)
                    jacobian = np.array([jacobians[min(index, len(jacobians) - 1)] for index in kernel.native], dtype=object)
                    jacobian_rate = np.array([jacobian_rates[min(index, len(jacobian_rates) - 1)] for index in kernel.native], dtype=object)
                    gamma = beta / jacobian
                    original = kernel.evaluate(reference_edges, field, gamma, edge_rate=np.full(len(edges), ZERO, dtype=object), field_rate=rate)
                    original_gradient = direct_gradient(kernel, reference_edges, field, gamma, original)
                    original_atoms = gamma * kernel.apply(1, original['image'] * original['image_rate'], True)
                    original_atoms += (beta_r * mesh_speed[kernel.native] / jacobian - beta * jacobian_rate / jacobian**2) * original['load']
                    old_measured, unused = interval_moments(edges[kernel.anchor], field_positions, original_gradient * rate, edges[kernel.native], original_atoms,
                                                          gamma * original['load'] * mesh_speed[kernel.native])
                    for power in range(3):
                        row = next(row for row in tables['native-current-comparison.csv'] if row['branch'] == case['branch'] and row['level'] == case['level'] and int(row['probe']) == probe and int(row['power']) == power)
                        error = abs(measured[power] - Decimal(row['new_current']))
                        old_error = abs(old_measured[power] - Decimal(row['old_current']))
                        evidence.check(path + ':independent_interval_current:' + str(power), max(error, old_error) <= Decimal('1e-30') * scale)
                        replay_rows.append(dict(branch=case['branch'], level=case['level'], probe=probe, power=power,
                            independent_current=str(measured[power]), independent_old_current=str(old_measured[power]),
                            new_error=str(error), old_error=str(old_error)))
                    values = solver.values(solution, np.array([float(edges[kernel.anchor])]))[0]
                    lapse = Decimal.from_float(float(np.exp(values[1, 0])))
                    metric = Decimal.from_float(float(1 - 2 * values[0, 0] / float(edges[kernel.anchor])))
                    clock = (lapse**2 - source_speed**2 / metric).sqrt()
                    for area_r in [Decimal('0.8'), Decimal('1.2')]:
                        for area_t in [Decimal('-0.002'), Decimal('0.002')]:
                            speed = area_t + area_r * source_speed
                            shift = -area_t
                            changed = (lapse**2 - (speed + shift)**2 / (metric * area_r**2)).sqrt()
                            evidence.check(path + ':finite_source_clock:' + str(area_r) + ':' + str(area_t), abs(changed - clock) <= Decimal('1e-70'))
            for row in tables['native-time-variations.csv']:
                error = abs(Decimal(row['extrapolated']) - Decimal(row['predicted']))
                identity = Decimal(row['raw']) - Decimal(row['current']) - Decimal(row['boundary_rate'])
                evidence.check('replay_derivative:' + str(len(evidence.report['checks'])), error <= Decimal(row['tolerance']) and abs(identity) < Decimal('1e-60'))
            for row in tables['wave-areal-momentum.csv']:
                error = abs(Decimal(row['measured']) - Decimal(row['predicted']))
                evidence.check('wave_derivative:' + str(len(evidence.report['checks'])), error <= Decimal(row['tolerance']))
                if row['order'] == '12':
                    other = next(other for other in tables['wave-areal-momentum.csv'] if all(other[key] == row[key] for key in ['branch', 'level', 'probe', 'test']) and other['order'] == '8')
                    difference = Decimal(row['predicted']) - Decimal(other['predicted'])
                    wave_comparisons.append(dict(branch=row['branch'], level=row['level'], probe=row['probe'], test=row['test'],
                        order8=other['predicted'], order12=row['predicted'], difference=str(difference)))
        time = sp.symbols('t', real=True)
        momentum, shift_current = time + 2 * time**3, 3 * time**2
        generator = (1 - time**2)**2
        compact_work = sp.integrate((momentum - shift_current) * sp.diff(generator, time), (time, -1, 1))
        euler_work = -sp.integrate(sp.diff(momentum - shift_current, time) * generator, (time, -1, 1))
        evidence.check('areal_momentum_temporal_IBP_sign_control', sp.simplify(compact_work - euler_work) == 0)
        omitted_current = -sp.integrate(sp.diff(momentum, time) * generator, (time, -1, 1))
        shifted_generator = (1 + time) * generator
        omitted_difference = sp.integrate(sp.diff(shift_current, time) * shifted_generator, (time, -1, 1))
        evidence.check('missing_time_current_control_can_be_excited', omitted_difference != 0)
        for filename, rows in [('independent-current-replay.csv', replay_rows), ('wave-momentum-quadrature.csv', wave_comparisons)]:
            path = evidence.output / filename
            with path.open('w', newline='', encoding='utf-8') as handle:
                writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
                writer.writeheader()
                writer.writerows(rows)
            evidence.own(path, 'outputs')
        cutoff = datetime.fromisoformat(parent['protected_since']).timestamp()
        protected = evidence.root.parent / 'formalization-workbench'
        changes = [str(path.relative_to(protected)) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime >= cutoff]
        evidence.check('protected_workbench_mtime', not changes, changes)
        evidence.check('no_bytecode_cache', not (evidence.root / 'scripts/__pycache__').exists())
        for name in ['annular_native_time_current_20260928.py', 'derive_annular_native_time_current_20260928.py', 'validate_annular_native_time_current_20260928.py']:
            path = evidence.root / 'scripts' / name
            compile(path.read_text(), str(path), 'exec')
            evidence.check('compile:' + name, True)
        evidence.report.update(seconds=perf_counter() - started, independent_current_replays=len(replay_rows),
            wave_quadrature_comparisons=len(wave_comparisons),
            maximum_current_replay_error=str(max(Decimal(row['new_error']) for row in replay_rows)),
            maximum_wave_quadrature_difference=str(max(abs(Decimal(row['difference'])) for row in wave_comparisons)),
            source_clock_chart_tests=48, physics_claim=False)
        completion = evidence.output / 'completion.txt'
        with completion.open('w', encoding='utf-8') as handle, contextlib.redirect_stdout(handle):
            evidence.complete()
        evidence.own(completion, 'outputs')
        evidence.save()
        print(json.dumps({key:evidence.report[key] for key in ['state', 'seconds', 'independent_current_replays', 'maximum_current_replay_error', 'maximum_wave_quadrature_difference']}), flush=True)
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
