from derive_annular_source_gravity_20260914 import EvidenceRun
from derive_annular_support_map_constraints_20260927 import restore_case, load_owned
from annular_joint_first_tangent_20260922 import MomentumMetricResponse, MetricResponse
from annular_candidate_energy_current_20260921 import reconstructed_solver
from annular_support_shift_jet_20260928 import wave_current, finite_wave_current, perturb, interpolate, integrals
from annular_moving_Legendre_current_20260921 import samples
from scipy.sparse import load_npz
from decimal import localcontext
from time import perf_counter
import contextlib
import csv
import hashlib
import json
import numpy as np


def main():
    evidence = EvidenceRun('annular-live-support-acceleration-validation-attempt01', __file__)
    started, deadline = perf_counter(), perf_counter() + 3600
    try:
        parent_path = evidence.output.parent / 'annular-live-support-acceleration-attempt01/status.json'
        parent = json.loads(parent_path.read_text())
        evidence.own(parent_path)
        evidence.check('main_complete', parent['state'] == 'complete' and all(row['passed'] for row in parent['checks']))
        digests, bad = {}, []
        for category in ['inputs', 'outputs']:
            for relative, expected in parent[category].items():
                path = evidence.root / relative
                if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
                    bad.append(relative)
                else:
                    digests[str(path.relative_to(evidence.root))] = expected
                    evidence.own(path)
        evidence.check('main_hashes_unchanged', not bad, bad)
        read = lambda relative: load_owned(evidence, digests, evidence.root / relative)
        rows = []
        with localcontext() as context:
            context.prec = 70
            for case in parent['cases']:
                name = case['branch'] + '-' + case['level']
                print(json.dumps(dict(stage=name, seconds=perf_counter() - started)), flush=True)
                loads, action, sources = restore_case(evidence, digests, case['branch'], case['level'], deadline)
                directions = read(case['direction_path'])
                projection = read(case['paths']['projection'])
                correction = projection['correction']
                archived = read(case['paths']['live_response'])
                solver, solution = reconstructed_solver(archived)
                response = MetricResponse(solver, solution, archived['forcing'], 0., [])
                momentum = MomentumMetricResponse(action, deadline, lambda unused: None)
                analytic = momentum.accumulate(response.values)
                numerical = momentum.accumulate(response.values, 1e-20)
                error = float(np.max(abs(analytic - numerical)))
                scale = max(float(np.max(abs(analytic))), 1e-300)
                evidence.check(name + ':metric_momentum_complex', error <= 2e-11 * scale + 1e-30, dict(error=error, scale=scale))
                evidence.check(name + ':metric_momentum_replay', np.max(abs(analytic - projection['metric_momentum'])) <= 1e-28)
                owner = read(sources['parent'])
                centre = next(row for row in owner['centres'] if row.get('route') == 'resampled') if case['level'] == 'fine' else owner['centres'][0]
                matrix = load_npz(evidence.root / centre['matrix_path'])
                residual = projection['fixed_coupling'] - (matrix @ correction.ravel()).reshape(correction.shape) + analytic
                evidence.check(name + ':old_Euler_replay', np.max(abs(residual - projection['old_Euler_residual'])) <= 1e-28)
                original = read(case['paths']['original_material48'])
                compensated = read(case['paths']['compensated_material48'])
                alternate = original['average'][-1] - float(projection['fixed_coupling'].ravel() @ correction.ravel())
                alternate -= case['summary']['cross_support_old'] + float(correction.ravel() @ residual.ravel())
                discrepancy = float(alternate - compensated['average'][-1])
                evidence.check(name + ':independent_projected_coefficient', abs(discrepancy) <= 2e-8 * abs(compensated['average'][-1]) + 1e-26, discrepancy)
                for relative in case['prior_probe_paths']:
                    if '-original-' not in relative:
                        continue
                    packet = read(relative)
                    label = float(packet['label'])
                    sampled = samples(action, label, 12)
                    cardinal = sampled['cardinal']
                    source_correction = float(cardinal @ correction[:, -1])
                    direction = {key[len('direction_'):]: value for key, value in packet.items() if key.startswith('direction_')}
                    direction['node_rate'] = direction['node_rate'] - cardinal @ correction[:, :-1]
                    direction['rate'], direction['rate_r'] = interpolate(packet, direction['node_rate'])
                    geometry = sampled['geometry']
                    direction['speed'] = direction['speed'] - geometry['displacement'] * source_correction
                    direction['speed_r'] = direction['speed_r'] - geometry['jacobian_source'] / geometry['jacobian'] * source_correction
                    nodal_geometry = action.geometry(action.knots, sampled['source'], label)
                    direction['node_speed'] = direction['node_speed'] - nodal_geometry['displacement'] * source_correction
                    direction['source_velocity'] = -source_correction
                    variation = response.values(packet['radius'])
                    ratio = variation[0] / (packet['radius'] * geometry['metric']) - variation[1]
                    temporal = packet['rate'] - packet['speed'] * packet['gradient']
                    defect = direction['rate'] - direction['speed'] * packet['gradient']
                    for power in range(3):
                        integral = integrals(packet['radius'], packet['source'], power)
                        weighted = interpolate(packet, packet['node_rate'] * integrals(packet['node_radius'], packet['source'], power))[0]
                        expected = packet['measure'] @ (packet['alpha'] * (defect + temporal * ratio) * (temporal * integral - weighted))
                        changed = perturb(packet, direction, 1e-20j, True)
                        changed['alpha_t'] = packet['alpha_t'] + 1e-20j * packet['alpha'] * ratio
                        complex_value = wave_current(changed, power).imag / 1e-20
                        tolerance = 2e-23 + 1e-6 * abs(expected)
                        evidence.check(name + ':current_complex:' + str(label) + ':' + str(power), abs(complex_value - expected) <= tolerance, float(complex_value - expected))
                        estimates = []
                        acceleration_scale = max(1e6, abs(case['summary']['conditional_linear_amplitude']))
                        for step in [acceleration_scale, acceleration_scale / 2, acceleration_scale / 4]:
                            pair = []
                            for sign in [1, -1]:
                                changed = perturb(packet, direction, sign * step, True)
                                changed['alpha_t'] = packet['alpha_t'] + sign * step * packet['alpha'] * ratio
                                pair.append(finite_wave_current(changed, power)[2])
                            estimates.append((pair[0] - pair[1]) / (2 * step))
                        finite = (4 * estimates[2] - estimates[1]) / 3
                        error = finite - expected
                        evidence.check(name + ':raw_endpoint_derivative:' + str(label) + ':' + str(power), abs(error) <= tolerance, float(error))
                        rows.append(dict(branch=case['branch'], level=case['level'], label=label, power=power,
                            predicted=float(expected), complex=float(complex_value), finite=float(finite),
                            complex_difference=float(complex_value - expected), finite_difference=float(error),
                            acceleration_scale=acceleration_scale, tolerance=float(tolerance)))
                del momentum, matrix
        path = evidence.output / 'independent-live-current-checks.csv'
        with path.open('w', newline='', encoding='utf-8') as stream:
            writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
        evidence.own(path, 'outputs')
        evidence.report.update(seconds=perf_counter() - started, checked_rows=len(rows), new_trajectories=0)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    with contextlib.redirect_stderr(__import__('sys').stdout):
        main()
