from derive_annular_source_gravity_20260914 import EvidenceRun
from derive_annular_support_map_constraints_20260927 import restore_case, load_owned
from annular_directional_coupled_Euler_20260928 import restore_flow, layer, evaluate_wave, CHANNELS
from annular_support_shift_jet_20260928 import make_packet, wave_current, gram_block, perturb
from annular_support_radial_response_20260928 import gravitational_moments
from annular_joint_first_tangent_20260922 import MetricResponse
from annular_candidate_energy_current_20260921 import reconstructed_solver
from annular_physical_native_kernel_20260928 import NativeKernel, decimals
from derive_annular_native_shape_stress_20260928 import physical_data
from annular_radial_Ward_moments_20260921 import prepare
from annular_moving_Legendre_current_20260921 import samples
from decimal import localcontext
from time import perf_counter
from annular_precise_union_gravity_20260928 import gravity_on_union
import contextlib
import csv
import hashlib
import json
import numpy as np


def evaluate(engine, loads, action, tangent, acceleration, polynomial, directions, correction, response, amplitude, label, order):
    base_values, raw, unused = layer(engine, loads, action, tangent, acceleration, polynomial,
        directions['edge_vertices'], directions['field_vertices'], label, order)
    sampled = samples(action, label, order)
    data = physical_data(engine, loads, action, label)
    cardinal = data['cardinal']
    source_direction = -float(cardinal @ correction[:, -1])
    field_direction = cardinal @ (directions['field_vertices'] - correction[:, :-1])
    edge_direction = cardinal @ directions['edge_vertices'] + np.asarray(data['displacement'], float) * source_direction
    packet, direction = make_packet(engine, data, raw, sampled, acceleration, field_direction, edge_direction, source_direction)
    variation = response.values(packet['radius'])
    ratio = variation[0] / (packet['radius'] * sampled['geometry']['metric']) - variation[1]
    changed = perturb(packet, direction, amplitude, True)
    changed['alpha_t'] = packet['alpha_t'] + amplitude * packet['alpha'] * ratio
    wave_before, wave_after = evaluate_wave(packet), evaluate_wave(changed)
    gram_force = base_values[CHANNELS.index('gram_total')]
    result = engine.evaluate(data['edges'], data['field'], data['beta'])
    edge_velocity = data['displacement'] * data['source_velocity']
    image_rate = engine.tangent(data['edges'], data['field'], edge_velocity, data['rate'])
    source = float(data['source'])
    source_values = action.solver.values(action.solution, np.array([source]))[0][:, 0]
    lapse, metric = np.exp(source_values[1]), 1 - 2 * source_values[0] / source
    velocity = float(data['source_velocity'])
    dust_current = action.owner.source_mass * lapse**2 * velocity / np.sqrt(lapse**2 - velocity**2 / metric)
    current = []
    for power in range(3):
        gram = gram_block(engine, data, result, data['rate'], edge_velocity, power, image_rate)
        dust = dust_current * (source - 6)**power
        before, after = wave_current(packet, power), wave_current(changed, power)
        current.append([before, float(gram['total']), dust, before + float(gram['total']) + dust,
            after, after + float(gram['total']) + dust])
    return np.array([wave_before['wave_direct'] + gram_force, wave_after['wave_direct'] + gram_force,
        wave_before['wave_identity'] + gram_force, wave_after['wave_identity'] + gram_force]), np.array(current)


def main():
    evidence = EvidenceRun('annular-instantaneous-support-trial-attempt03', __file__)
    started, deadline = perf_counter(), perf_counter() + 7200
    try:
        evidence.own(evidence.root / 'DERIVATION-20260928-instantaneous-support-constraint-trial.md')
        evidence.own(evidence.root / 'DERIVATION-20260928-union-grid-gravity-correction.md')
        evidence.own(evidence.root / 'DERIVATION-20260928-probe-gravity-precision-correction.md')
        parent_path = evidence.output.parent / 'annular-live-support-acceleration-attempt01/status.json'
        parent = json.loads(parent_path.read_text())
        evidence.own(parent_path)
        evidence.check('live_acceleration_complete', parent['state'] == 'complete' and all(row['passed'] for row in parent['checks']))
        digests, bad = {}, []
        for category in ['inputs', 'outputs']:
            for relative, expected in parent[category].items():
                path = evidence.root / relative
                if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
                    bad.append(relative)
                else:
                    digests[str(path.relative_to(evidence.root))] = expected
                    evidence.own(path)
        evidence.check('parent_hashes_unchanged', not bad, bad)
        read = lambda relative: load_owned(evidence, digests, evidence.root / relative)
        current_path = evidence.output.parent / 'annular-live-support-acceleration-attempt01/live-acceleration-current-moments.csv'
        with current_path.open(newline='', encoding='utf-8') as stream:
            slopes = list(csv.DictReader(stream))

        def progress(stage):
            evidence.report['progress'] = dict(stage=stage, seconds=perf_counter() - started)
            evidence.save()
            print(json.dumps(evidence.report['progress']), flush=True)
            if perf_counter() > deadline:
                raise RuntimeError('Safe completed-layer trial boundary')

        def save(name, **arrays):
            path = evidence.output / (name + '.npz')
            np.savez_compressed(path, **arrays)
            evidence.own(path, 'outputs')
            return str(path.relative_to(evidence.root))

        summaries, moments, spatial = [], [], []
        with localcontext() as context:
            context.prec = 70
            for case in parent['cases']:
                name = case['branch'] + '-' + case['level']
                progress(name + ':restore')
                loads, action, sources = restore_case(evidence, digests, case['branch'], case['level'], deadline)
                mesh = read(sources['packet'])
                engine = NativeKernel(mesh['mesh'], mesh['gram_support'], case['branch'] == 'MTS-primary')
                flow, tangent, unused = restore_flow(evidence, digests, action, sources, case['level'])
                acceleration = flow['accelerations'][-1]
                polynomial, unused = prepare(action, loads, acceleration)
                directions = read(case['direction_path'])
                projection = read(case['paths']['projection'])
                correction = projection['correction']
                archive = read(case['paths']['live_response'])
                solver, solution = reconstructed_solver(archive)
                response = MetricResponse(solver, solution, archive['forcing'], 0., [])
                amplitude = case['summary']['conditional_linear_amplitude']
                evidence.check(name + ':finite_nonzero_coefficient', amplitude is not None and np.isfinite(amplitude))
                old_work = float(correction.ravel() @ projection['saved_Euler_residual'].ravel())
                old_slope = float(correction.ravel() @ projection['old_Euler_residual'].ravel())
                gravity, union_edges = gravity_on_union(action, tangent, 32)
                gravity24, unused_edges = gravity_on_union(action, tangent, 24)
                save(name + '-baseline-gravity', edges=union_edges, gravity32=gravity, gravity24=gravity24)
                evidence.check(name + ':gravity_precision60_80', tangent.precise_probe_mass_rate.precision_sample_difference <= 1e-26,
                    dict(precision_difference=tangent.precise_probe_mass_rate.precision_sample_difference,
                         sample_float_difference=tangent.precise_probe_mass_rate.max_sample_float_difference))
                gravity_change = gravitational_moments(action, response, 32)
                evidence.check(name + ':baseline_gravity_quadrature', np.max(abs(gravity - gravity24)) <= 2e-17,
                    float(np.max(abs(gravity - gravity24))))
                tangent.coordinate_rate.cache.clear()
                averages, current_averages, paths = [], [], []
                for order in [48, 64]:
                    labels, weights = np.polynomial.legendre.leggauss(order)
                    labels, weights = labels / 2, weights / 2
                    weights *= 6 * (labels + .5) * (.5 - labels)
                    forces, currents = [], []
                    for index, label in enumerate(labels):
                        if index % 16 == 0:
                            progress(name + ':material' + str(order) + ':' + str(index))
                        force, current = evaluate(engine, loads, action, tangent, acceleration, polynomial,
                            directions, correction, response, amplitude, label, 12)
                        forces.append(force)
                        currents.append(current)
                        if order == 64 and index == 31:
                            force8, current8 = evaluate(engine, loads, action, tangent, acceleration, polynomial,
                                directions, correction, response, amplitude, label, 8)
                            error_force = float(np.max(abs(force8 - force)))
                            error_current = float(np.max(abs(current8 - current)))
                            evidence.check(name + ':spatial8_12_force', error_force <= 2e-16, error_force)
                            evidence.check(name + ':spatial8_12_current', error_current <= 2e-16, error_current)
                            spatial.append(dict(branch=case['branch'], level=case['level'], force_difference=error_force, current_difference=error_current))
                    forces, currents = np.array(forces), np.array(currents)
                    average = np.tensordot(weights, forces, axes=(0, 0))
                    averaged_current = np.tensordot(weights, currents, axes=(0, 0))
                    averages.append(average)
                    current_averages.append(averaged_current)
                    paths.append(save(name + '-material' + str(order), labels=labels, weights=weights,
                        forces=forces, currents=currents, average=average, averaged_current=averaged_current,
                        gravity=gravity, gravity_change=gravity_change, amplitude=np.array(amplitude)))
                    evidence.check(name + ':Euler_cell_identity:' + str(order), np.max(abs(forces[:, :2] - forces[:, 2:])) <= 2e-15,
                        float(np.max(abs(forces[:, :2] - forces[:, 2:]))))
                    compensated_before = float(average[0] - old_work)
                    compensated_after = float(average[1] - old_work - amplitude * old_slope)
                    predicted_after = compensated_before + amplitude * case['summary']['live_projected_coefficient']
                    error = compensated_after - predicted_after
                    evidence.check(name + ':independent_force_amplitude:' + str(order), abs(error) <= 2e-17 + 2e-6 * abs(compensated_before), error)
                    summaries.append(dict(branch=case['branch'], level=case['level'], material_order=order, amplitude=amplitude,
                        projected_force_before=compensated_before, projected_force_after=compensated_after,
                        affine_prediction=predicted_after, force_identity_difference=error,
                        old_Euler_work_after=float(old_work + amplitude * old_slope)))
                    for power in range(3):
                        source = next(row for row in slopes if row['branch'] == case['branch'] and row['level'] == case['level'] and int(row['power']) == power)
                        before = float(gravity[power] + averaged_current[power, 3])
                        after = float(gravity[power] + amplitude * gravity_change[power] + averaged_current[power, 5])
                        predicted = before + amplitude * float(source['total'])
                        error = after - predicted
                        evidence.check(name + ':independent_shift_amplitude:' + str(order) + ':' + str(power), abs(error) <= 3e-17, error)
                        moments.append(dict(branch=case['branch'], level=case['level'], material_order=order, power=power,
                            gravity_before=float(gravity[power]), wave_before=float(averaged_current[power, 0]),
                            Gram=float(averaged_current[power, 1]), dust=float(averaged_current[power, 2]),
                            total_before=before, gravity_after=float(gravity[power] + amplitude * gravity_change[power]),
                            wave_after=float(averaged_current[power, 4]), total_after=after,
                            affine_prediction=predicted, identity_difference=error))
                difference_force = float(np.max(abs(averages[0] - averages[1])))
                difference_current = float(np.max(abs(current_averages[0] - current_averages[1])))
                evidence.check(name + ':material48_64_force', difference_force <= 2e-16, difference_force)
                evidence.check(name + ':material48_64_current', difference_current <= 2e-16, difference_current)
                evidence.report['cases'].append(dict(branch=case['branch'], level=case['level'], paths=paths,
                    force_quadrature_difference=difference_force, current_quadrature_difference=difference_current))
                evidence.save()
        for filename, rows in [('instantaneous-force-trial.csv', summaries), ('instantaneous-shift-trial.csv', moments), ('instantaneous-spatial-checks.csv', spatial)]:
            path = evidence.output / filename
            with path.open('w', newline='', encoding='utf-8') as stream:
                writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
                writer.writeheader()
                writer.writerows(rows)
            evidence.own(path, 'outputs')
        evidence.report.update(seconds=perf_counter() - started, new_trajectories=0,
            amplitude_fit_to_shift=False, full_functional_shift_constraint_tested=False,
            scope='Direct instantaneous force and full matter/gravity current test of action-derived scalar amplitude; no physical success outcome imposed')
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    with contextlib.redirect_stderr(__import__('sys').stdout):
        main()
