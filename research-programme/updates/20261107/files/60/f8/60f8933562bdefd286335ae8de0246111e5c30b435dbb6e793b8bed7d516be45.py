from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_nonuniform_Gram_candidate_20260920 import template_rows
from annular_candidate_energy_current_20260921 import reconstructed_solver
from decimal import Decimal, localcontext
from fractions import Fraction
from datetime import datetime
from time import perf_counter
import argparse
import contextlib
import csv
import hashlib
import json
import numpy as np


ZERO = Decimal(0)


def archive(path):
    with np.load(path, allow_pickle=False) as data:
        return {key: data[key].copy() for key in data.files}


def decimal_array(values):
    return np.array([Decimal(str(value)) for value in np.asarray(values).ravel()], dtype=object).reshape(np.shape(values))


def maximum(values):
    return max(map(abs, np.asarray(values).ravel()), default=ZERO)


class DirectNodalKernel:
    def __init__(self, mesh, support, enabled):
        self.elements = np.array(mesh['elements'])
        lookup = {Fraction(value): index for index, value in enumerate(mesh['edges'])}
        self.native = np.array([lookup[Fraction(value)] for value in support])
        self.anchor = lookup[Fraction(mesh['anchor'])]
        self.enabled = enabled
        self.maps = []
        for mapping in template_rows(len(support)):
            coo = mapping.tocoo()
            self.maps.append((coo.row, coo.col, np.array([Decimal.from_float(float(value)) for value in coo.data], dtype=object), coo.shape))

    def apply(self, number, vector, transpose=False):
        row, column, values, shape = self.maps[number]
        if transpose:
            row, column, shape = column, row, shape[::-1]
        result = np.full(shape[0], ZERO, dtype=object)
        np.add.at(result, row, values * vector[column])
        return result

    def nodal_values(self, field):
        edges = np.full(len(self.elements) + 1, ZERO, dtype=object)
        first = self.elements[0, 0]
        edges[0] = field[first] if first >= 0 else ZERO
        for index, column in enumerate(self.elements[:, 2]):
            edges[index + 1] = field[column] if column >= 0 else ZERO
        return edges

    def source_jump(self, edges, field, edge_rate=None, field_rate=None):
        slopes, rates = [], []
        for cell, coefficients in [(self.anchor - 1, [1, -4, 3]), (self.anchor, [-3, 4, -1])]:
            width = edges[cell + 1] - edges[cell]
            numerator = sum((Decimal(coefficient) * field[column] for column, coefficient in zip(self.elements[cell], coefficients) if column >= 0), ZERO)
            slopes.append(numerator / width)
            if edge_rate is not None:
                rate = sum((Decimal(coefficient) * field_rate[column] for column, coefficient in zip(self.elements[cell], coefficients) if column >= 0), ZERO) / width
                rate -= slopes[-1] * (edge_rate[cell + 1] - edge_rate[cell]) / width
                rates.append(rate)
        return slopes[1] - slopes[0], None if edge_rate is None else rates[1] - rates[0]

    def evaluate(self, edges, field, beta, hinge=True, edge_rate=None, field_rate=None):
        positions = edges[self.native]
        values = self.nodal_values(field)[self.native]
        jump, jump_rate = self.source_jump(edges, field, edge_rate, field_rate)
        if not hinge:
            jump = ZERO
        hinge_values = np.array([max(position - edges[self.anchor], ZERO) for position in positions], dtype=object)
        compensated = values - jump * hinge_values
        if edge_rate is not None:
            velocities = edge_rate[self.native]
            hinge_rates = np.array([velocity - edge_rate[self.anchor] if position > edges[self.anchor] else ZERO
                                    for position, velocity in zip(positions, velocities)], dtype=object)
            compensated_rate = self.nodal_values(field_rate)[self.native] - jump_rate * hinge_values - jump * hinge_rates
        kernel = np.full(len(positions) - 3, ZERO, dtype=object)
        kernel_rate = kernel.copy()
        if self.enabled:
            for index in range(len(kernel)):
                points = positions[index:index + 4]
                width = (points[3] - points[0]) / 3
                if edge_rate is not None:
                    speed = velocities[index:index + 4]
                    width_rate = (speed[3] - speed[0]) / 3
                for local in range(4):
                    denominator = Decimal(1)
                    logarithm = Decimal('2.5') * width_rate / width if edge_rate is not None else ZERO
                    for other in range(4):
                        if local != other:
                            denominator *= points[local] - points[other]
                            if edge_rate is not None:
                                logarithm -= (speed[local] - speed[other]) / (points[local] - points[other])
                    coefficient = 6 * width**2 * width.sqrt() / denominator
                    kernel[index] += coefficient * compensated[index + local]
                    if edge_rate is not None:
                        kernel_rate[index] += coefficient * (compensated_rate[index + local] + logarithm * compensated[index + local])
        image = self.apply(0, kernel)
        weights = self.apply(1, beta)
        result = dict(image=image, energy=sum(weights * image**2 / 2, ZERO), load=self.apply(1, image**2 / 2, True))
        if edge_rate is not None:
            result['image_rate'] = self.apply(0, kernel_rate)
        return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--run', default='annular-native-shape-stress-attempt01')
    parser.add_argument('--label', default='annular-native-shape-stress-validation-attempt02')
    args = parser.parse_args()
    evidence = EvidenceRun(args.label, __file__)
    started, deadline = perf_counter(), perf_counter() + 2700
    try:
        parent_path = evidence.output.parent / args.run / 'status.json'
        parent = json.loads(parent_path.read_text())
        evidence.check('main_complete', parent['state'] == 'complete' and all(row['passed'] for row in parent['checks']))
        evidence.own(parent_path)
        evidence.own(evidence.output.parent / 'annular-native-shape-stress-validation-attempt01/status.json')
        evidence.own(evidence.root / 'DERIVATION-20260928-native-hinge-control-correction.md')
        digests = {}
        for category in ['inputs', 'outputs']:
            for relative, digest in parent[category].items():
                if relative in digests and digests[relative] != digest:
                    raise RuntimeError('Source hash conflict')
                digests[relative] = digest
        for relative, digest in digests.items():
            path = evidence.root / relative
            evidence.check('hash:' + relative, path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest() == digest)
            evidence.own(path)
        with (parent_path.parent / 'native-shape-and-current.csv').open(newline='') as handle:
            rows = list(csv.DictReader(handle))
        evidence.check('CSV_schema', len(rows) == 12 and all(None not in row and None not in row.values() for row in rows))
        finite_rows, current_rows = [], []
        material_replays, negative_hinge, negative_curvature = 0, False, False
        hinge_controls = []
        with localcontext() as context:
            context.prec = 80
            for case in parent['cases']:
                name = case['branch'] + '-' + case['level']
                print(json.dumps(dict(stage=name, seconds=perf_counter() - started)), flush=True)
                packet = json.loads((evidence.root / case['sources']['packet']).read_text())
                kernel = DirectNodalKernel(packet['mesh'], packet['gram_support'], case['branch'] == 'MTS-primary')
                solver, solution = reconstructed_solver(archive(evidence.root / case['sources']['state']))
                for path in case['material_paths']:
                    saved = archive(evidence.root / path)
                    order = len(saved['labels'])
                    labels, weights = np.polynomial.legendre.leggauss(order)
                    labels, weights = labels / 2, weights / 2
                    weights *= 6 * (labels + .5) * (.5 - labels)
                    evidence.check(name + ':quadrature:' + str(order), np.array_equal(labels, saved['labels']) and np.array_equal(weights, saved['weights']))
                    average = np.tensordot(weights, saved['values'], axes=(0, 0))
                    evidence.check(name + ':recombine:' + str(order), np.max(abs(average - saved['average'])) <= 2e-18)
                    material_replays += order
                for test in range(3):
                    row = next(row for row in rows if row['branch'] == case['branch'] and row['level'] == case['level'] and int(row['test']) == test)
                    for channel, value in zip(parent['channels'], average[:, test]):
                        evidence.check(name + ':CSV:' + str(test) + ':' + channel, abs(float(row[channel]) - value) <= 2e-18)
                for probe_index, path in enumerate(case['probe_paths']):
                    if perf_counter() > deadline:
                        raise RuntimeError('Safe validation boundary')
                    raw = archive(evidence.root / path)
                    edges, field, beta, beta_radial, displacement, rate = [decimal_array(raw[key]) for key in ['edges', 'field', 'beta', 'beta_radial', 'displacement', 'rate']]
                    source_velocity = Decimal(str(raw['source_velocity']))
                    edge_gradient, field_gradient, tests = [decimal_array(raw[key]) for key in ['edge_gradient', 'field_gradient', 'edge_tests']]
                    actual = kernel.evaluate(edges, field, beta, edge_rate=displacement * source_velocity, field_rate=np.full(len(field), ZERO, dtype=object))
                    reference_energy = Decimal(str(raw['energy']))
                    energy_scale = max(abs(reference_energy), Decimal('1e-80'))
                    image_scale = max(maximum(decimal_array(raw['image'])), Decimal('1e-80'))
                    evidence.check(path + ':independent_native_values', abs(actual['energy'] - reference_energy) <= Decimal('1e-30') * energy_scale
                                   and maximum(actual['image'] - decimal_array(raw['image'])) <= Decimal('1e-30') * image_scale)
                    image_rate_scale = max(maximum(decimal_array(raw['image_shape_rate'])), Decimal('1e-80'))
                    evidence.check(path + ':independent_geometry_tangent', maximum(actual['image_rate'] - decimal_array(raw['image_shape_rate'])) <= Decimal('1e-30') * image_rate_scale)
                    complex_radius = np.asarray(edges[kernel.native], float).astype(complex) + 1e-20j
                    values = solver.values(solution, complex_radius)[0]
                    complex_beta = complex_radius**2 * np.exp(values[1]) * np.sqrt(1 - 2 * values[0] / complex_radius)
                    derivative_error = np.max(abs(complex_beta.imag / 1e-20 - np.asarray(beta_radial, float)))
                    evidence.check(path + ':actual_metric_derivative', derivative_error <= 2e-10 * max(1., np.max(abs(np.asarray(beta_radial, float)))), float(derivative_error))
                    atom_power = beta * kernel.apply(1, actual['image'] * actual['image_rate'], True)
                    atom_power += beta_radial * displacement[kernel.native] * source_velocity * actual['load']
                    power_scale = max(maximum(atom_power), Decimal('1e-80'))
                    evidence.check(path + ':independent_atom_power', maximum(atom_power - decimal_array(raw['atom_power'])) <= Decimal('1e-30') * power_scale)
                    evidence.check(path + ':source_work', abs(sum(atom_power, ZERO) + Decimal(str(raw['source_force'])) * source_velocity) <= Decimal('1e-30') * power_scale)
                    no_hinge = kernel.evaluate(edges, field, beta, hinge=False)['energy']
                    evidence.check(path + ':hinge_negative_control_replay', abs(no_hinge - Decimal(str(raw['no_hinge_energy']))) <= Decimal('1e-30') * max(abs(no_hinge), energy_scale))
                    negative_hinge |= abs(no_hinge - reference_energy) > Decimal('1e-12') * energy_scale
                    negative_curvature |= abs(Decimal(str(raw['no_curvature_energy'])) - reference_energy) > Decimal('1e-12') * energy_scale
                    if case['branch'] == 'MTS-primary' and probe_index == 0:
                        control_field = np.full(len(field), ZERO, dtype=object)
                        control_field[kernel.elements[kernel.anchor, 1]] = Decimal(1)
                        jump, unused = kernel.source_jump(edges, control_field)
                        expected_jump = 4 / (edges[kernel.anchor + 1] - edges[kernel.anchor])
                        evidence.check(path + ':control_known_source_jump', jump == expected_jump)
                        compensated = kernel.evaluate(edges, control_field, beta)
                        uncompensated = kernel.evaluate(edges, control_field, beta, hinge=False)
                        points = edges[kernel.native]
                        hinge_response = np.full(len(points) - 3, ZERO, dtype=object)
                        for stencil in range(len(hinge_response)):
                            local_points = points[stencil:stencil + 4]
                            width = (local_points[3] - local_points[0]) / 3
                            for local in range(4):
                                denominator = Decimal(1)
                                for other in range(4):
                                    if other != local:
                                        denominator *= local_points[local] - local_points[other]
                                hinge_response[stencil] += 6 * width**2 * width.sqrt() / denominator * max(local_points[local] - edges[kernel.anchor], ZERO)
                        expected_difference = jump * kernel.apply(0, hinge_response)
                        measured_difference = uncompensated['image'] - compensated['image']
                        evidence.check(path + ':control_nonzero_source_hinge', maximum(expected_difference) > 0
                                       and maximum(measured_difference - expected_difference) <= Decimal('1e-30') * maximum(expected_difference))
                        hinge_controls.append(dict(level=case['level'], source_jump=str(jump),
                            maximum_missing_hinge_factor=str(maximum(expected_difference)),
                            compensated_energy=str(compensated['energy']), uncompensated_energy=str(uncompensated['energy'])))
                    events = sorted([(int(index), -power) for index, power in zip(kernel.native, atom_power)]
                                    + [(kernel.anchor, sum(atom_power, ZERO))])
                    current, weak = ZERO, np.full(3, ZERO, dtype=object)
                    for event_index, (edge_index, change) in enumerate(events):
                        current += change
                        if event_index + 1 < len(events):
                            next_edge = events[event_index + 1][0]
                            weak += current * (tests[:, next_edge] - tests[:, edge_index])
                    evidence.check(path + ':current_outside_zero', abs(current) <= Decimal('1e-30') * power_scale)
                    expected_weak = np.array([sum(atom_power * test[kernel.native], ZERO) for test in tests], dtype=object)
                    evidence.check(path + ':current_interval_primitive', maximum(weak - expected_weak) <= Decimal('1e-30') * power_scale)
                    for test in range(3):
                        current_rows.append(dict(branch=case['branch'], level=case['level'], probe=probe_index, test=test,
                            interval_current=float(weak[test]), atom_current=float(expected_weak[test])))
                    directions = [('shape' + str(test), tests[test], np.full(len(field), ZERO, dtype=object)) for test in range(3)]
                    directions += [('source', displacement, np.full(len(field), ZERO, dtype=object)),
                                   ('field_rate', np.full(len(edges), ZERO, dtype=object), rate),
                                   ('full_flow', displacement * source_velocity, rate),
                                   ('field_control', np.full(len(edges), ZERO, dtype=object),
                                    np.array([Decimal((index * 7) % 19 - 9) / 16 for index in range(len(field))], dtype=object))]
                    for direction_name, edge_direction, field_direction in directions:
                        beta_direction = beta_radial * edge_direction[kernel.native]
                        predicted = sum(edge_gradient * edge_direction, ZERO) + sum(field_gradient * field_direction, ZERO)
                        predicted += sum(actual['load'] * beta_direction, ZERO)
                        absolute_scale = sum(abs(edge_gradient * edge_direction), ZERO) + sum(abs(field_gradient * field_direction), ZERO)
                        absolute_scale += sum(abs(actual['load'] * beta_direction), ZERO)
                        limits = [width / abs(change) for width, change in zip(np.diff(edges), np.diff(edge_direction)) if change]
                        if maximum(beta_direction):
                            limits += [coefficient / abs(change) for coefficient, change in zip(beta, beta_direction) if change]
                        step = Decimal('0.001') * min(limits, default=Decimal(1))
                        differences = []
                        for resolution in range(3):
                            amount = step / (2**resolution)
                            plus = kernel.evaluate(edges + amount * edge_direction, field + amount * field_direction, beta + amount * beta_direction)['energy']
                            minus = kernel.evaluate(edges - amount * edge_direction, field - amount * field_direction, beta - amount * beta_direction)['energy']
                            differences.append((plus - minus) / (2 * amount))
                        extrapolated = (4 * differences[-1] - differences[-2]) / 3
                        error = abs(extrapolated - predicted)
                        tolerance = Decimal('1e-22') + Decimal('2e-7') * absolute_scale
                        evidence.check(path + ':rebuilt_real_variation:' + direction_name, error <= tolerance,
                                       dict(error=str(error), tolerance=str(tolerance)))
                        finite_rows.append(dict(branch=case['branch'], level=case['level'], probe=probe_index,
                            direction=direction_name, step=str(step), predicted=str(predicted), coarse=str(differences[0]),
                            middle=str(differences[1]), fine=str(differences[2]), extrapolated=str(extrapolated),
                            error=str(error), tolerance=str(tolerance)))
                    evidence.report['progress'] = dict(stage=name + ':probe' + str(probe_index), seconds=perf_counter() - started)
                    evidence.save()
                evidence.report['cases'].append(dict(branch=case['branch'], level=case['level'], probes=len(case['probe_paths'])))
            evidence.check('controlled_source_hinge_negative_tests', len(hinge_controls) == 2)
            evidence.check('actual_curvature_omission_changes_energy', negative_curvature)
        for filename, data in [('real-native-variations.csv', finite_rows), ('current-primitive-replay.csv', current_rows)]:
            path = evidence.output / filename
            with path.open('w', newline='', encoding='utf-8') as handle:
                writer = csv.DictWriter(handle, fieldnames=list(data[0]))
                writer.writeheader()
                writer.writerows(data)
            evidence.own(path, 'outputs')
        cutoff = datetime.fromisoformat(parent['protected_since']).timestamp()
        protected = evidence.root.parent / 'formalization-workbench'
        changed = [str(path.relative_to(protected)) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime >= cutoff]
        evidence.check('protected_workbench_mtime', not changed, changed)
        evidence.check('no_bytecode_cache', not (evidence.root / 'scripts/__pycache__').exists())
        for filename in ['annular_physical_native_kernel_20260928.py', 'derive_annular_native_shape_stress_20260928.py', 'validate_annular_native_shape_stress_v2_20260928.py']:
            path = evidence.root / 'scripts' / filename
            compile(path.read_text(), str(path), 'exec')
            evidence.check('compile:' + filename, True)
        evidence.report.update(seconds=perf_counter() - started, material_replays=material_replays,
            real_derivative_cases=len(finite_rows), real_signed_pairs=3 * len(finite_rows), current_weak_replays=len(current_rows),
            maximum_derivative_error=str(max(Decimal(row['error']) for row in finite_rows)),
            actual_kernel_and_hinge_differentiated=True, physics_claim=False,
            actual_hinge_energy_change_detected=negative_hinge, actual_curvature_energy_change_detected=negative_curvature,
            manufactured_hinge_controls=hinge_controls, correction='Actual seeds have no detectable hinge-omission energy change; explicit nonzero-jump controls replace the unjustified negative-control premise, not a derivative tolerance.')
        completion = evidence.output / 'completion.txt'
        with completion.open('w', encoding='utf-8') as handle, contextlib.redirect_stdout(handle):
            evidence.complete()
        evidence.own(completion, 'outputs')
        evidence.save()
        print(json.dumps(dict(state='complete', checks=len(evidence.report['checks']), seconds=evidence.report['seconds'],
                             real_derivative_cases=len(finite_rows), maximum_derivative_error=evidence.report['maximum_derivative_error'])), flush=True)
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()


