from derive_annular_source_gravity_20260914 import EvidenceRun
from derive_annular_support_map_constraints_20260927 import restore_case, load_owned
from annular_candidate_energy_current_20260921 import reconstructed_solver
from annular_moving_Legendre_current_20260921 import samples
from decimal import localcontext
from time import perf_counter
import contextlib
import csv
import hashlib
import json
import numpy as np


def main():
    evidence = EvidenceRun('annular-support-metric-feedback-bound-attempt01', __file__)
    started, deadline = perf_counter(), perf_counter() + 1800
    try:
        parent_path = evidence.output.parent / 'annular-live-support-acceleration-attempt01/status.json'
        parent = json.loads(parent_path.read_text())
        evidence.own(parent_path)
        evidence.check('live_response_complete', parent['state'] == 'complete' and all(row['passed'] for row in parent['checks']))
        digests, bad = {}, []
        for category in ['inputs', 'outputs']:
            for relative, expected in parent[category].items():
                path = evidence.root / relative
                if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
                    bad.append(relative)
                else:
                    digests[str(path.relative_to(evidence.root))] = expected
                    evidence.own(path)
        evidence.check('parent_inputs_unchanged', not bad, bad)
        read = lambda relative: load_owned(evidence, digests, evidence.root / relative)
        rows = []
        with localcontext() as context:
            context.prec = 70
            for case in parent['cases']:
                name = case['branch'] + '-' + case['level']
                print(json.dumps(dict(stage=name, seconds=perf_counter() - started)), flush=True)
                loads, action, unused = restore_case(evidence, digests, case['branch'], case['level'], deadline)
                archive = read(case['paths']['live_response'])
                solver, solution = reconstructed_solver(archive)
                bounds = []
                for order in [48, 64]:
                    packet = read(case['paths']['compensated_material' + str(order)])
                    dual_norms = []
                    for label in packet['labels']:
                        if perf_counter() > deadline:
                            raise RuntimeError('Safe positive-norm feedback-bound boundary')
                        sampled = samples(action, label, 12)
                        geometry = sampled['geometry']
                        radius, metric = geometry['radius'], geometry['metric']
                        variation = solver.values(solution, radius)[0]
                        ratio = variation[0] / (radius * metric) - variation[1]
                        measure = sampled['quadrature']['measure'] * geometry['kinetic']
                        dual_norms.append(float(measure @ (sampled['temporal'] * ratio)**2))
                    dual_norms = np.array(dual_norms)
                    dual_norm = float(packet['weights'] @ dual_norms)
                    wave_norm = float(packet['average'][0])
                    dust_absolute = float(packet['weights'] @ abs(packet['totals'][:, 3]))
                    upper_bound = np.sqrt(wave_norm * dual_norm) + dust_absolute
                    actual = float(packet['average'][2] + packet['average'][3])
                    evidence.check(name + ':positive_finite:' + str(order), np.isfinite(upper_bound) and min(wave_norm, dual_norm, dust_absolute) >= 0)
                    evidence.check(name + ':Cauchy_Schwarz_bound:' + str(order), abs(actual) <= upper_bound,
                        dict(actual=actual, upper_bound=float(upper_bound)))
                    bounds.append(float(upper_bound))
                    rows.append(dict(branch=case['branch'], level=case['level'], material_order=order,
                        wave_defect_norm=wave_norm, metric_dual_norm=dual_norm, dust_absolute_bound=dust_absolute,
                        metric_feedback_bound=float(upper_bound), actual_metric_feedback=actual,
                        feedback_bound_over_projected_coefficient=float(upper_bound / abs(packet['average'][-1]))))
                    path = evidence.output / (name + '-material' + str(order) + '.npz')
                    np.savez_compressed(path, labels=packet['labels'], weights=packet['weights'], dual_norms=dual_norms)
                    evidence.own(path, 'outputs')
                evidence.check(name + ':bound_quadrature', abs(bounds[1] - bounds[0]) <= 2e-6 * max(bounds) + 1e-40,
                    abs(bounds[1] - bounds[0]))
        path = evidence.output / 'metric-feedback-positive-bound.csv'
        with path.open('w', newline='', encoding='utf-8') as stream:
            writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
        evidence.own(path, 'outputs')
        evidence.report.update(seconds=perf_counter() - started,
            derived_bound='abs(integral alpha*T*r*d + dust_metric) <= sqrt(integral alpha*d^2 * integral alpha*(T*r)^2) + integral abs(dust_metric)',
            scope='Positive quadrature norm bound for the four represented compensated directions, not a universal operator or continuum bound',
            new_trajectories=0, github_action=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    with contextlib.redirect_stderr(__import__('sys').stdout):
        main()
