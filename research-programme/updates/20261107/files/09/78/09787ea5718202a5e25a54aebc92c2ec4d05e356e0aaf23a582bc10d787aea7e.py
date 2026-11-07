from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_candidate_canonical_response_20260920 import common_material
from annular_P2_indexed_live_geometry_20260919 import IndexedGradedP2System
from annular_nested_physical_refinement_v3_20260922 import adapt_owner, restore_refined
from annular_radial_Ward_moments_20260921 import test_functions
from decimal import Decimal, localcontext
from datetime import datetime
from time import perf_counter
from math import fsum
import contextlib
import csv
import hashlib
import json
import numpy as np


def explicit_factor(rows, field):
    with localcontext() as context:
        context.prec = 64
        return np.array([float(sum((Decimal(value) * field[int(column)] for column, value in row.items()), Decimal(0)))
                         for row in rows])


def main():
    evidence = EvidenceRun('annular-radial-shape-exchange-validation-attempt01', __file__)
    started, deadline = perf_counter(), perf_counter() + 3600
    try:
        intake = evidence.output.parent
        main_path = intake / 'annular-radial-shape-exchange-attempt01/status.json'
        parent = json.loads(main_path.read_text())
        evidence.own(main_path)
        evidence.check('main_completed', parent['state'] == 'complete' and all(row['passed'] for row in parent['checks']))
        evidence.check('both_full_third_grid_centres', len(parent['cases']) == 2
                       and all(row['count'] == 65655 and row['faces'] == 2187 for row in parent['cases']))
        digests = dict(parent['inputs'], **parent['outputs'])
        for relative, digest in digests.items():
            path = evidence.root / relative
            evidence.check('hash:' + relative, path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest() == digest)
            evidence.own(path)

        def read(relative):
            path = evidence.root / relative
            evidence.check('owned:' + relative, str(path.relative_to(evidence.root)) in digests)
            if path.suffix == '.json':
                return json.loads(path.read_text())
            with np.load(path, allow_pickle=False) as archive:
                return {key: archive[key].copy() for key in archive.files}

        variation_rows, replayed = [], 0
        for case in parent['cases']:
            name = case['branch']
            print(json.dumps(dict(stage=name + ':independent-replay', seconds=perf_counter() - started)), flush=True)
            generator = read(case['generator_path'])
            vector = np.concatenate([generator['vertices'], -generator['source_vertices'][:, :, None]], axis=2)
            canonical_work = np.array([fsum((vector[test] * generator['canonical_euler']).ravel()) for test in range(3)])
            evidence.check(name + ':canonical_contraction', np.max(abs(canonical_work - generator['canonical_work'])) < 2e-24)
            averages = []
            for relative in case['quadrature_paths']:
                raw = read(relative)
                average = np.empty(raw['average'].shape)
                for channel in range(average.shape[0]):
                    for test in range(3):
                        average[channel, test] = fsum(raw['weights'] * raw['values'][:, channel, test])
                evidence.check(relative + ':weighted_replay', np.max(abs(average - raw['average'])) < 2e-23)
                values = raw['values']
                evidence.check(relative + ':product_split', np.max(abs(values[:, 4] - values[:, 7:10].sum(axis=1))) <= 2e-16)
                evidence.check(relative + ':source_identity', np.max(abs(values[:, 14])) <= 2e-16)
                evidence.check(relative + ':shape_is_field_plus_support', np.max(abs(values[:, 6] - values[:, 4] - values[:, 5])) <= 2e-23)
                averages.append(average)
                replayed += len(raw['labels'])
            branch, extension = name.split('-')
            short = 'reference' if branch == 'reference' else name
            source = read(str((intake / ('annular-' + short + '-third-current-attempt02') / 'status.json').relative_to(evidence.root)))
            centre = source['centres'][0]
            old_components = read(source['summaries'][0]['component_path'])
            current_rate = old_components['components'][-1, 5:].sum(axis=0)
            reconstructed = averages[1][6] + current_rate + averages[1][10:16].sum(axis=0)
            table_rows = [row for row in parent['comparison'] if row['branch'] == name]
            evidence.check(name + ':whole_balance_replay', np.max(abs(reconstructed - [row['predicted'] for row in table_rows])) < 2e-23)
            evidence.check(name + ':whole_balance_matches_prior_components',
                           np.max(abs(reconstructed - old_components['components'][-1].sum(axis=0))) <= 2e-16)
            evidence.check(name + ':weak_projection_not_hidden', np.max(abs(averages[0][13] - canonical_work)) <= 2e-16)
            if branch == 'reference':
                evidence.check('empty_Gram_control_exact', np.max(abs(averages[1][4:10])) == 0.)
            original = read(str((intake / 'annular-candidate-initial-metric-attempt02' / (branch + '-velocity-owned-inputs.npz')).relative_to(evidence.root)))
            overlay = read(str((intake / 'annular-transfer-kernel-overlay-attempt01' / (branch + '-exact-common-overlay.json')).relative_to(evidence.root)))
            packet = read(str((intake / 'annular-resampled-third-grid-preparation-attempt01' / (name + '-third-action.json')).relative_to(evidence.root)))
            native = IndexedGradedP2System(257, branch == 'MTS', 2e-5)
            base, unused, unused2 = common_material(native, original, overlay)
            state = read(centre['state_path'])
            loads, action = restore_refined(adapt_owner(base, packet['mesh']), state, packet['mesh'], packet, extension, deadline)
            for relative in case['variation_paths']:
                raw = read(relative)
                label = float(raw['label'])
                cardinal = np.asarray(action.cardinal(label)).ravel()
                source_radius = float(cardinal @ action.source)
                geometry = action.geometry(action.knots, source_radius, label)
                xi, slope = test_functions(geometry['radius'])
                source_xi = test_functions(source_radius)[0]
                eta = xi - source_xi[:, None] * geometry['displacement']
                eta_slope = slope - source_xi[:, None] * geometry['jacobian_source'] / geometry['jacobian']
                direction = np.einsum('tln,l->tn', generator['vertices'], cardinal)
                with localcontext() as context:
                    context.prec = 64
                    weights = [Decimal.from_float(float(value)) for value in cardinal]
                    field = [sum((weights[layer] * Decimal(state['coordinates'][layer, node])
                                  for layer in range(len(weights))), Decimal(0)) for node in range(packet['count'])]
                steps = np.array([1e-3, 5e-4, 2.5e-4])
                for test in range(3):
                    potential_pairs = []
                    for step in steps:
                        pair = []
                        for sign in [-1, 1]:
                            amount = sign * step
                            moved_radius = geometry['radius'] + amount * eta[test]
                            moved_jacobian = geometry['jacobian'] * (1 + amount * eta_slope[test])
                            evidence.check(name + ':positive_deformed_jacobian:' + str(label) + ':' + str(test) + ':' + str(amount),
                                           np.min(moved_jacobian) > 0)
                            metric_values = action.solver.values(action.solution, moved_radius)[0]
                            gamma = moved_radius**2 * np.exp(metric_values[1]) * np.sqrt(1 - 2 * metric_values[0] / moved_radius) / moved_jacobian
                            with localcontext() as context:
                                context.prec = 64
                                shifted = [value + Decimal.from_float(float(amount)) * Decimal.from_float(float(delta))
                                           for value, delta in zip(field, direction[test])]
                            image = explicit_factor(packet['gram_factor']['rows'], shifted)
                            pair.append(float((action.sampling @ gamma) @ image**2 / 2))
                        potential_pairs.append(pair)
                    with localcontext() as context:
                        context.prec = 64
                        slopes = [(Decimal.from_float(pair[1]) - Decimal.from_float(pair[0])) /
                                  (2 * Decimal.from_float(float(step))) for pair, step in zip(potential_pairs, steps)]
                        derivatives = [float((4 * slopes[index + 1] - slopes[index]) / 3) for index in range(2)]
                    expected = float(raw['variations'][2 * test, 3])
                    error = abs(derivatives[-1] - expected)
                    tolerance = 2e-18 + 2e-8 * abs(expected)
                    evidence.check(name + ':fresh_real_potential_derivative:' + str(label) + ':' + str(test), error <= tolerance, error)
                    variation_rows.append(dict(branch=name, label=label, test=test, analytic=expected,
                        real_derivative=derivatives[-1], step_change=abs(derivatives[1] - derivatives[0]), error=error, tolerance=tolerance))
            evidence.report['cases'].append(dict(branch=name, replayed_labels=sum(len(read(path)['labels']) for path in case['quadrature_paths']),
                fresh_real_variations=9, seconds=perf_counter() - started))
        path = evidence.output / 'independent-real-variations.csv'
        with path.open('w', newline='', encoding='utf-8') as stream:
            writer = csv.DictWriter(stream, fieldnames=list(variation_rows[0]))
            writer.writeheader()
            writer.writerows(variation_rows)
        evidence.own(path, 'outputs')
        with path.open(newline='', encoding='utf-8') as stream:
            parsed = list(csv.DictReader(stream))
        evidence.check('variation_csv_clean', len(parsed) == 18 and all(None not in row and None not in row.values() for row in parsed))
        threshold = datetime.fromisoformat('2026-09-27T21:24:50+00:00').timestamp()
        changed = [str(path) for path in (evidence.root.parent / 'formalization-workbench').rglob('*')
                   if path.is_file() and path.stat().st_mtime >= threshold]
        evidence.check('protected_workbench_unchanged', not changed, changed)
        evidence.check('no_scripts_bytecode_cache', not (evidence.root / 'scripts/__pycache__').exists())
        evidence.report.update(seconds=perf_counter() - started, replayed_labels=replayed, real_variation_count=len(variation_rows),
            maximum_real_variation_error=max(row['error'] for row in variation_rows),
            main_scientific_passed=parent['science_passed'], main_scientific_total=parent['science_total'],
            protected_workbench_changed_count=len(changed), new_nonlinear_solves=0, github_action=False, subagents_used=False)
        with (evidence.output / 'completion.txt').open('w', encoding='utf-8') as stream, contextlib.redirect_stdout(stream):
            evidence.complete()
        evidence.own(evidence.output / 'completion.txt', 'outputs')
        evidence.save()
        print(json.dumps(dict(state='complete', checks=len(evidence.report['checks']), seconds=evidence.report['seconds'],
                              maximum_real_variation_error=evidence.report['maximum_real_variation_error'])), flush=True)
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
