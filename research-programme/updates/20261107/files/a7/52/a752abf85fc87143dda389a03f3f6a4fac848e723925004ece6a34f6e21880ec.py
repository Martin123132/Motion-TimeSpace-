from derive_annular_source_gravity_20260914 import EvidenceRun
from derive_annular_support_map_constraints_20260927 import restore_case, load_owned
from annular_directional_coupled_Euler_20260928 import restore_flow
from derive_annular_instantaneous_support_trial_v3_20260928 import evaluate
from annular_joint_first_tangent_20260922 import ProbeMetricRate, MetricResponse
from annular_joint_flow_derivative_20260922 import JointMetricTangent
from annular_precise_union_gravity_20260928 import gravity_on_union
from annular_candidate_energy_current_20260921 import reconstructed_solver
from annular_physical_native_kernel_20260928 import NativeKernel
from annular_radial_Ward_moments_20260921 import prepare
from decimal import localcontext
from time import perf_counter
import contextlib
import csv
import hashlib
import json
import numpy as np


def main():
    evidence = EvidenceRun('annular-archived-probe-baseline-comparison-attempt01', __file__)
    started, deadline = perf_counter(), perf_counter() + 5400
    try:
        evidence.own(evidence.root / 'DERIVATION-20260928-archived-probe-baseline-control.md')
        parent_path = evidence.output.parent / 'annular-live-support-acceleration-attempt01/status.json'
        trial_path = evidence.output.parent / 'annular-instantaneous-support-trial-attempt03/status.json'
        parent, trial = json.loads(parent_path.read_text()), json.loads(trial_path.read_text())
        evidence.own(parent_path)
        evidence.own(trial_path)
        evidence.check('live_response_complete', parent['state'] == 'complete' and all(row['passed'] for row in parent['checks']))
        evidence.check('trial_precision_failure_preserved', trial['state'] == 'failed'
            and 'MTS-primary-third:independent_shift_amplitude:48:0' in trial['error'])
        digests, bad = {}, []
        for packet in [parent, trial]:
            for category in ['inputs', 'outputs']:
                for relative, expected in packet[category].items():
                    if relative in digests:
                        continue
                    path = evidence.root / relative
                    if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
                        bad.append(relative)
                    else:
                        digests[relative] = expected
                        evidence.own(path)
        evidence.check('parent_hashes_unchanged', not bad, bad)
        read = lambda relative: load_owned(evidence, digests, evidence.root / relative)

        def progress(stage):
            evidence.report['progress'] = dict(stage=stage, seconds=perf_counter() - started)
            evidence.save()
            print(json.dumps(evidence.report['progress']), flush=True)
            if perf_counter() > deadline:
                raise RuntimeError('Safe archived-probe comparison boundary')

        rows = []
        with localcontext() as context:
            context.prec = 70
            for case in parent['cases']:
                name = case['branch'] + '-' + case['level']
                progress(name + ':restore')
                loads, action, sources = restore_case(evidence, digests, case['branch'], case['level'], deadline)
                mesh = read(sources['packet'])
                engine = NativeKernel(mesh['mesh'], mesh['gram_support'], case['branch'] == 'MTS-primary')
                flow, original, unused = restore_flow(evidence, digests, action, sources, case['level'])
                coordinate = ProbeMetricRate(original.coordinate_rate.actions, original.coordinate_rate.steps[:2])
                tangent = JointMetricTangent(coordinate, original.velocity_responses[:1])
                acceleration = flow['accelerations'][0]
                evidence.check(name + ':earlier_jet_replay', np.max(abs(tangent.values(flow['radius'])[0] - flow['metric_rate'][0])) <= 2e-18)
                coordinate.cache.clear()
                polynomial, unused = prepare(action, loads, acceleration)
                later_acceleration = flow['accelerations'][-1]
                later_polynomial, unused = prepare(action, loads, later_acceleration)
                directions = read(case['direction_path'])
                correction = read(case['paths']['projection'])['correction']
                archive = read(case['paths']['live_response'])
                solver, solution = reconstructed_solver(archive)
                response = MetricResponse(solver, solution, archive['forcing'], 0., [])
                gravity, union_edges = gravity_on_union(action, tangent, 32)
                gravity24, unused_edges = gravity_on_union(action, tangent, 24)
                evidence.check(name + ':baseline_gravity_quadrature', np.max(abs(gravity - gravity24)) <= 2e-17,
                    float(np.max(abs(gravity - gravity24))))
                averages, later_averages, paths = [], [], []
                previous_prefix = str(trial_path.parent.relative_to(evidence.root))
                later_gravity_packet = read(previous_prefix + '/' + name + '-baseline-gravity.npz')
                later_gravity = later_gravity_packet['gravity32']
                evidence.check(name + ':saved_later_gravity_passed', any(row['name'] == name + ':baseline_gravity_quadrature' and row['passed'] for row in trial['checks']))
                response_gravity = read(previous_prefix + '/' + name + '-material48.npz')['gravity_change']
                for order in [48, 64]:
                    labels, weights = np.polynomial.legendre.leggauss(order)
                    labels, weights = labels / 2, weights / 2
                    weights *= 6 * (labels + .5) * (.5 - labels)
                    currents, forces, later_currents = [], [], []
                    later_path = evidence.root / previous_prefix / (name + '-material' + str(order) + '.npz')
                    later_key = str(later_path.relative_to(evidence.root))
                    cached_later = read(later_key) if later_key in digests else None
                    for index, label in enumerate(labels):
                        if index % 16 == 0:
                            progress(name + ':material' + str(order) + ':' + str(index))
                        force, current = evaluate(engine, loads, action, tangent, acceleration, polynomial,
                            directions, correction, response, 0., label, 12)
                        forces.append(force)
                        currents.append(current)
                        if cached_later is None:
                            unused_force, late_current = evaluate(engine, loads, action, original, later_acceleration,
                                later_polynomial, directions, correction, response, 0., label, 12)
                            later_currents.append(late_current)
                            if order == 64 and index == 31:
                                unused_force, coarse_current = evaluate(engine, loads, action, original, later_acceleration,
                                    later_polynomial, directions, correction, response, 0., label, 8)
                                evidence.check(name + ':completed_later_spatial8_12', np.max(abs(late_current - coarse_current)) <= 2e-16,
                                    float(np.max(abs(late_current - coarse_current))))
                    currents, forces = np.array(currents), np.array(forces)
                    average = np.tensordot(weights, currents, axes=(0, 0))
                    averages.append(average)
                    later_average = cached_later['averaged_current'] if cached_later is not None else np.tensordot(weights, np.array(later_currents), axes=(0, 0))
                    later_averages.append(later_average[:, :4])
                    early_total = gravity + average[:, 3]
                    late_total = later_gravity + later_average[:, 3]
                    response_packet = read(case['paths']['compensated_material' + str(order)])
                    affine_change = case['summary']['conditional_linear_amplitude'] * (response_packet['current'][:, -1] + response_gravity)
                    candidate_total = late_total + affine_change
                    for power in range(3):
                        difference = float(early_total[power] - late_total[power])
                        correction_size = float(affine_change[power])
                        rows.append(dict(branch=case['branch'], level=case['level'], material_order=order, power=power,
                            earlier_baseline=float(early_total[power]), later_baseline=float(late_total[power]),
                            paired_difference=difference, gravity_difference=float(gravity[power] - later_gravity[power]),
                            matter_difference=float(average[power, 3] - later_average[power, 3]),
                            support_candidate_change=correction_size,
                            candidate_change_is_order_matched_affine_prediction=True,
                            change_over_paired_sensitivity=abs(correction_size / difference) if difference else None,
                            sensitivity_is_rigorous_error_bound=False))
                    path = evidence.output / (name + '-material' + str(order) + '.npz')
                    np.savez_compressed(path, labels=labels, weights=weights, currents=currents, forces=forces,
                        average=average, gravity=gravity, gravity24=gravity24, union_edges=union_edges,
                        earlier_total=early_total, later_total=late_total, candidate_total=candidate_total,
                        later_average=later_average, later_gravity=later_gravity,
                        later_baseline_recomputed=np.array(cached_later is None), affine_change=affine_change)
                    evidence.own(path, 'outputs')
                    paths.append(str(path.relative_to(evidence.root)))
                quadrature = float(np.max(abs(averages[0] - averages[1])))
                evidence.check(name + ':material48_64', quadrature <= 2e-16, quadrature)
                later_difference = float(np.max(abs(later_averages[0] - later_averages[1])))
                evidence.check(name + ':later_baseline_material48_64', later_difference <= 2e-16, later_difference)
                evidence.report['cases'].append(dict(branch=case['branch'], level=case['level'], paths=paths,
                    material_difference=quadrature, later_baseline_material_difference=later_difference,
                    earlier_steps=flow['inner_steps'][:2].tolist(), later_steps=flow['inner_steps'][1:].tolist()))
                evidence.save()
        path = evidence.output / 'paired-probe-baseline-sensitivity.csv'
        with path.open('w', newline='', encoding='utf-8') as stream:
            writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
        evidence.own(path, 'outputs')
        evidence.report.update(seconds=perf_counter() - started, new_trajectories=0,
            scope='Compare BOTH complete archived Richardson acceleration/metric-time jets at the identical configuration and velocities; paired sensitivity is not a rigorous error enclosure')
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    with contextlib.redirect_stderr(__import__('sys').stdout):
        main()
