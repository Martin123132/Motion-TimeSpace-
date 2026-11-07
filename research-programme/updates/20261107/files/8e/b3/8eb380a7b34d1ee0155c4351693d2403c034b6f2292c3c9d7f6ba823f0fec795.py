from derive_annular_source_gravity_20260914 import EvidenceRun
from derive_annular_support_map_constraints_20260927 import restore_case
from annular_physical_native_kernel_20260928 import NativeKernel, decimals, maximum
from annular_radial_Ward_moments_20260921 import test_functions
from decimal import Decimal, localcontext
from time import perf_counter
import argparse
import contextlib
import csv
import hashlib
import json
import numpy as np


ZERO = Decimal(0)
CHANNELS = ['field_transport', 'kernel_shape', 'metric_coefficient', 'total_shape',
            'source_force', 'old_source_force', 'source_current_weak', 'old_source_current_weak']


def physical_data(engine, loads, action, label):
    cardinal = np.asarray(action.cardinal(label)).ravel()
    source = Decimal.from_float(float(cardinal @ action.source))
    source_velocity = Decimal.from_float(float(cardinal @ action.velocity))
    label_decimal = Decimal.from_float(float(label))
    width = Decimal.from_float(float(action.owner.width))
    reference = np.array(engine.references, dtype=object)
    anchor = reference[engine.anchor]
    lower, upper = reference[0] + width * label_decimal, reference[-1] + width * label_decimal
    displacement = np.array([(point - reference[0]) / (anchor - reference[0]) if point <= anchor
        else (reference[-1] - point) / (reference[-1] - anchor) for point in reference], dtype=object)
    edges = np.array([lower + (source - lower) * fraction if point <= anchor else upper + (source - upper) * fraction
                      for point, fraction in zip(reference, displacement)], dtype=object)
    field = loads.coordinates[:, :-1].T @ decimals(cardinal)
    rate = decimals(loads.rates[:, :-1].T) @ decimals(cardinal)
    radius = np.asarray(edges[engine.native_edges], float)
    values, derivatives = action.solver.values(action.solution, radius)
    mass, log_lapse = values
    metric = 1 - 2 * mass / radius
    metric_radial = -2 * derivatives[0] / radius + 2 * mass / radius**2
    beta = radius**2 * np.exp(log_lapse) * np.sqrt(metric)
    beta_radial = beta * (2 / radius + derivatives[1] + metric_radial / (2 * metric))
    return dict(cardinal=cardinal, source=source, source_velocity=source_velocity,
                edges=edges, displacement=displacement, field=field, rate=rate,
                beta=decimals(beta), beta_radial=decimals(beta_radial))


def pinned_tests(edges, source):
    radius = np.asarray(edges, float)
    displacement = np.where(radius <= float(source), (radius - radius[0]) / (float(source) - radius[0]),
                             (radius[-1] - radius) / (radius[-1] - float(source)))
    values = test_functions(radius)[0]
    source_values = test_functions(float(source))[0]
    boundary = np.where(radius[None, :] <= float(source), values[:, :1], values[:, -1:])
    eta = values - displacement * source_values[:, None] - (1 - displacement) * boundary
    eta[:, [0, -1]] = 0.
    return decimals(eta)


def nodal_transport(engine, result, edge_test):
    atoms = result['atoms']
    gradient, displacement, counts = [np.full(engine.count, ZERO, dtype=object) for unused in range(3)]
    for cell, indices in enumerate(engine.indices):
        slopes = [atoms['slope_left'][cell], (atoms['slope_left'][cell] + atoms['slope_right'][cell]) / 2,
                  atoms['slope_right'][cell]]
        movements = [edge_test[cell], (edge_test[cell] + edge_test[cell + 1]) / 2, edge_test[cell + 1]]
        for column, slope, movement in zip(indices, slopes, movements):
            if column >= 0:
                gradient[column] += slope
                displacement[column] += movement
                counts[column] += 1
    return gradient * displacement / counts**2


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--label', default='annular-native-shape-stress-attempt01')
    parser.add_argument('--max-seconds', type=float, default=9000)
    args = parser.parse_args()
    evidence = EvidenceRun(args.label, __file__)
    started, deadline = perf_counter(), perf_counter() + args.max_seconds
    try:
        evidence.report.update(scope='Physical native-radius Gram candidate: complete shape covectors and source-anchored current exchange.',
            candidate_only=True, original_live_action_unchanged=True, new_nonlinear_solves=0, full_current_residual_recomputed=False,
            github_action=False, subagents_used=False, protected_since='2026-09-27T23:03:41+00:00', channels=CHANNELS)
        evidence.own(evidence.root / 'DERIVATION-20260928-native-kernel-shape-stress.md')
        authority_path = evidence.output.parent / 'annular-geometric-pullback-validation-attempt01/status.json'
        authority = json.loads(authority_path.read_text())
        evidence.check('authority_complete', authority['state'] == 'complete' and all(row['passed'] for row in authority['checks']))
        evidence.own(authority_path)
        digests = {}
        for category in ['inputs', 'outputs']:
            for relative, digest in authority[category].items():
                if relative in digests and digests[relative] != digest:
                    raise ValueError('Source digest conflict')
                digests[relative] = digest
        for relative, digest in digests.items():
            path = evidence.root / relative
            evidence.check('hash:' + relative, path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest() == digest)
            evidence.own(path)

        def progress(stage):
            evidence.report['progress'] = dict(stage=stage, seconds=perf_counter() - started)
            evidence.save()
            print(json.dumps(evidence.report['progress']), flush=True)
            if perf_counter() > deadline:
                raise RuntimeError('Safe runtime boundary; completed data retained')

        def save(name, **arrays):
            path = evidence.output / (name + '.npz')
            np.savez_compressed(path, **arrays)
            evidence.own(path, 'outputs')
            return str(path.relative_to(evidence.root))

        rows = []
        with localcontext() as context:
            context.prec = 72
            for branch in ['reference-reference', 'MTS-primary']:
                for level in ['fine', 'third']:
                    name = branch + '-' + level
                    progress(name + ':restore')
                    loads, action, sources = restore_case(evidence, digests, branch, level, deadline)
                    packet = json.loads((evidence.root / sources['packet']).read_text())
                    engine = NativeKernel(action.mesh, packet['gram_support'], branch == 'MTS-primary')
                    evidence.check(name + ':physical_anchor_matches', abs(float(engine.references[engine.anchor]) - action.owner.model.anchor) < 1e-14)
                    material_paths, probe_paths, averages, energy_errors = [], [], [], []
                    for order in [48, 64]:
                        labels, weights = np.polynomial.legendre.leggauss(order)
                        labels, weights = labels / 2, weights / 2
                        weights *= 6 * (labels + .5) * (.5 - labels)
                        values, baseline_errors = [], []
                        for index, label in enumerate(labels):
                            if index % 8 == 0:
                                progress(name + ':material' + str(order) + ':label' + str(index))
                            data = physical_data(engine, loads, action, label)
                            result = engine.evaluate(data['edges'], data['field'], data['beta'])
                            energy = result['energy']
                            scale = max(abs(energy), Decimal('1e-80'))
                            evidence.check(name + ':translation:' + str(order) + ':' + str(index),
                                abs(sum(result['edge_gradient'], ZERO)) <= Decimal('1e-35') * scale)
                            evidence.check(name + ':dilation:' + str(order) + ':' + str(index),
                                abs(sum(result['edge_gradient'] * data['edges'], ZERO) + energy) <= Decimal('1e-35') * scale)
                            evidence.check(name + ':field_homogeneity:' + str(order) + ':' + str(index),
                                abs(sum(result['field_gradient'] * data['field'], ZERO) - 2 * energy) <= Decimal('1e-35') * scale)
                            original = action.factor_values @ data['cardinal']
                            old_geometry = action.geometry(action.knots, float(data['source']), label)
                            original_energy = float((action.sampling @ old_geometry['gradient']) @ original**2 / 2)
                            baseline_error = abs(float(energy) - original_energy)
                            evidence.check(name + ':seed_potential:' + str(order) + ':' + str(index),
                                baseline_error <= 1e-24 + 1e-8 * abs(original_energy), baseline_error)
                            baseline_errors.append([float(energy), original_energy, baseline_error])
                            geometry_rate = data['displacement'] * data['source_velocity']
                            image_shape_rate = engine.tangent(data['edges'], data['field'], geometry_rate, np.full(engine.count, ZERO, dtype=object))
                            image_field_rate = engine.tangent(data['edges'], data['field'], np.full(len(data['edges']), ZERO, dtype=object), data['rate'])
                            kernel_power = data['beta'] * engine.apply('sampling', result['image'] * image_shape_rate, True)
                            coefficient_power = data['beta_radial'] * geometry_rate[engine.native_edges] * result['load']
                            atom_power = kernel_power + coefficient_power
                            field_rate = data['beta'] * engine.apply('sampling', result['image'] * image_field_rate, True)
                            source_gradient = sum(result['edge_gradient'] * data['displacement'], ZERO)
                            source_gradient += sum(result['load'] * data['beta_radial'] * data['displacement'][engine.native_edges], ZERO)
                            source_force = -source_gradient
                            power_scale = max(maximum(atom_power), abs(source_force * data['source_velocity']), Decimal('1e-80'))
                            evidence.check(name + ':source_power:' + str(order) + ':' + str(index),
                                abs(sum(atom_power, ZERO) + source_force * data['source_velocity']) <= Decimal('1e-35') * power_scale)
                            evidence.check(name + ':field_power:' + str(order) + ':' + str(index),
                                abs(sum(field_rate, ZERO) - sum(result['field_gradient'] * data['rate'], ZERO)) <= Decimal('1e-35') * max(maximum(field_rate), Decimal('1e-80')))
                            old_load = np.asarray(action.sampling.T @ (original**2 / 2)).ravel()
                            old_power = decimals(old_geometry['gradient_source'] * float(data['source_velocity']) * old_load)
                            old_source_force = -sum(decimals(old_geometry['gradient_source'] * old_load), ZERO)
                            edge_tests = pinned_tests(data['edges'], data['source'])
                            evidence.check(name + ':pinned_tests:' + str(order) + ':' + str(index),
                                maximum(edge_tests[:, [0, engine.anchor, -1]]) <= Decimal('2e-14'))
                            channels = np.zeros((len(CHANNELS), 3))
                            for test in range(3):
                                field_test = nodal_transport(engine, result, edge_tests[test])
                                field_work = sum(result['field_gradient'] * field_test, ZERO)
                                shape_work = sum(result['edge_gradient'] * edge_tests[test], ZERO)
                                coefficient_work = sum(result['load'] * data['beta_radial'] * edge_tests[test, engine.native_edges], ZERO)
                                weak_stress = -np.cumsum(result['edge_gradient'])[:-1]
                                evidence.check(name + ':stress:' + str(order) + ':' + str(index) + ':' + str(test),
                                    abs(sum(weak_stress * np.diff(edge_tests[test]), ZERO) - shape_work) <= Decimal('1e-35') * max(abs(shape_work), scale))
                                current_weak = sum(atom_power * edge_tests[test, engine.native_edges], ZERO)
                                old_eta = pinned_tests(np.r_[data['edges'][0], np.array([Decimal.from_float(float(radius)) for radius in old_geometry['radius']], dtype=object), data['edges'][-1]], data['source'])[test, 1:-1]
                                old_current_weak = sum(old_power * old_eta, ZERO)
                                channels[:, test] = list(map(float, [field_work, shape_work, coefficient_work, field_work + shape_work + coefficient_work,
                                                                  source_force, old_source_force, current_weak, old_current_weak]))
                            values.append(channels)
                            if order == 64 and index in [0, 31, 63]:
                                no_hinge = engine.evaluate(data['edges'], data['field'], data['beta'], adjoint=False, hinge=False)
                                no_curvature = engine.evaluate(data['edges'], data['field'], data['beta'], adjoint=False, curvature=False)
                                probe_paths.append(save(name + '-probe' + str(index), label=np.array(label),
                                    edges=data['edges'].astype(str), field=data['field'].astype(str), rate=data['rate'].astype(str),
                                    beta=data['beta'].astype(str), beta_radial=data['beta_radial'].astype(str),
                                    displacement=data['displacement'].astype(str), source_velocity=np.array(str(data['source_velocity'])),
                                    edge_tests=edge_tests.astype(str), image=result['image'].astype(str), load=result['load'].astype(str),
                                    field_gradient=result['field_gradient'].astype(str), edge_gradient=result['edge_gradient'].astype(str),
                                    native_gradient=result['native_gradient'].astype(str), interface_gradient=result['interface_gradient'].astype(str),
                                    atom_power=atom_power.astype(str), kernel_power=kernel_power.astype(str), coefficient_power=coefficient_power.astype(str),
                                    image_shape_rate=image_shape_rate.astype(str), energy=np.array(str(energy)),
                                    no_hinge_energy=np.array(str(no_hinge['energy'])), no_curvature_energy=np.array(str(no_curvature['energy'])),
                                    source_force=np.array(str(source_force)), channels=channels))
                        values = np.array(values)
                        average = np.einsum('l,lct->ct', weights, values)
                        material_paths.append(save(name + '-material' + str(order), labels=labels, weights=weights, values=values,
                                                   average=average, baseline=np.array(baseline_errors)))
                        averages.append(average)
                        energy_errors.extend(baseline_errors)
                    for test in range(3):
                        row = dict(branch=branch, level=level, test=test)
                        row.update({key: averages[-1][channel, test] for channel, key in enumerate(CHANNELS)})
                        row['source_force_change'] = row['source_force'] - row['old_source_force']
                        row['source_current_change'] = row['source_current_weak'] - row['old_source_current_weak']
                        row['quadrature_total_shape_change'] = averages[-1][3, test] - averages[0][3, test]
                        rows.append(row)
                    evidence.report['cases'].append(dict(branch=branch, level=level, sources=sources,
                        material_paths=material_paths, probe_paths=probe_paths, field_count=engine.count,
                        interfaces=len(engine.references) - 2, native_knots=len(engine.native_edges),
                        maximum_seed_energy_error=max(row[2] for row in energy_errors)))
                    evidence.save()
        path = evidence.output / 'native-shape-and-current.csv'
        with path.open('w', newline='', encoding='utf-8') as handle:
            writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
        evidence.own(path, 'outputs')
        evidence.report.update(seconds=perf_counter() - started, physical_covectors_constructed=True,
            source_current_exchange_constructed=True, parent_uniqueness_proven=False)
        completion = evidence.output / 'completion.txt'
        with completion.open('w', encoding='utf-8') as handle, contextlib.redirect_stdout(handle):
            evidence.complete()
        evidence.own(completion, 'outputs')
        evidence.save()
        print(json.dumps(dict(state='complete', checks=len(evidence.report['checks']), seconds=evidence.report['seconds'], rows=rows)), flush=True)
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
