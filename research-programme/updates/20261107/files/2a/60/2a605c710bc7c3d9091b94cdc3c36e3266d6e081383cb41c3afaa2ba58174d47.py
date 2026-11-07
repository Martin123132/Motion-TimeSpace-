from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_support_shift_jet_20260928 import CHANNELS, symbolic_checks, make_packet, wave_blocks, wave_current, finite_wave_current, perturb, gram_block
from annular_directional_coupled_Euler_20260928 import restore_flow, layer
from derive_annular_support_map_constraints_20260927 import restore_case, load_owned
from derive_annular_native_shape_stress_20260928 import physical_data
from annular_physical_native_kernel_20260928 import NativeKernel, decimals
from annular_moving_Legendre_current_20260921 import samples
from annular_radial_Ward_moments_20260921 import prepare
from annular_native_time_current_20260928 import finite_gram_action, endpoint_functional
from validate_annular_native_shape_stress_v2_20260928 import DirectNodalKernel
from decimal import Decimal, localcontext
from time import perf_counter
import contextlib
import csv
import hashlib
import json
import numpy as np


def main():
    evidence = EvidenceRun('annular-support-shift-jet-attempt01', __file__)
    started, deadline = perf_counter(), perf_counter() + 9000
    try:
        evidence.report.update(channels=CHANNELS, protected_since='2026-09-28T10:14:00+00:00',
            new_nonlinear_solves=0, new_trajectories=0, github_action=False, subagents_used=False,
            scope='Exact inherited matter-current velocity/acceleration blocks at fixed configuration and metric time jet; gravitational shift normalization and conditional first-order compatibility derived, not a solved full constraint system')
        evidence.own(evidence.root / 'DERIVATION-20260928-support-shift-current-jet.md')
        seal_path = evidence.output.parent / 'annular-directional-coupled-Euler-final-integrity-20260928.json'
        seal = json.loads(seal_path.read_text())
        evidence.own(seal_path)
        evidence.check('previous_stage_sealed', seal['state'] == 'complete')
        digests, bad = {}, []
        for relative, digest in seal['hashes'].items():
            if relative == 'CURRENT_LOCAL_RESUME.md':
                continue
            path = evidence.root / relative
            if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != digest:
                bad.append(relative)
            else:
                digests[str(path.relative_to(evidence.root))] = digest
                evidence.own(path)
        evidence.check('all_prior_scientific_hashes', not bad, bad)
        read = lambda relative: load_owned(evidence, digests, evidence.root / relative)
        authority = read(str((evidence.output.parent / 'annular-directional-coupled-Euler-attempt02/status.json').relative_to(evidence.root)))
        schur = read(str((evidence.output.parent / 'annular-support-Schur-conditioning-attempt01/status.json').relative_to(evidence.root)))
        symbolic_checks(evidence)

        def progress(stage):
            evidence.report['progress'] = dict(stage=stage, seconds=perf_counter() - started)
            evidence.save()
            print(json.dumps(evidence.report['progress']), flush=True)
            if perf_counter() > deadline:
                raise RuntimeError('Safe saved-probe runtime boundary')

        def close(name, error, tolerance):
            evidence.check(name, np.isfinite(float(error)) and abs(error) <= tolerance,
                dict(error=float(error), tolerance=float(tolerance)))

        def save(name, **arrays):
            path = evidence.output / (name + '.npz')
            np.savez_compressed(path, **arrays)
            evidence.own(path, 'outputs')
            return str(path.relative_to(evidence.root))

        summaries, finite_rows, gram_rows = [], [], []
        with localcontext() as context:
            context.prec = 70
            for case in authority['cases']:
                branch, level = case['branch'], case['level']
                name = branch + '-' + level
                progress(name + ':restore')
                loads, action, sources = restore_case(evidence, digests, branch, level, deadline)
                mesh_packet = read(sources['packet'])
                engine = NativeKernel(mesh_packet['mesh'], mesh_packet['gram_support'], branch == 'MTS-primary')
                direct = DirectNodalKernel(mesh_packet['mesh'], mesh_packet['gram_support'], branch == 'MTS-primary')
                flow, tangent, centre = restore_flow(evidence, digests, action, sources, level)
                acceleration = flow['accelerations'][-1]
                polynomial, unused = prepare(action, loads, acceleration)
                directions = read(case['direction_path'])
                corrected = next(row for row in schur['cases'] if row['branch'] == branch and row['level'] == level)
                correction = read(corrected['output'])['correction']
                paths, probe_paths, averages = [], [], []
                for order in [48, 64]:
                    labels, weights = np.polynomial.legendre.leggauss(order)
                    labels, weights = labels / 2, weights / 2
                    weights *= 6 * (labels + .5) * (.5 - labels)
                    values = []
                    for index, label in enumerate(labels):
                        if index % 16 == 0:
                            progress(name + ':material' + str(order) + ':label' + str(index))
                        unused_values, raw, unused_pins = layer(engine, loads, action, tangent, acceleration, polynomial,
                            directions['edge_vertices'], directions['field_vertices'], label, 12)
                        row = samples(action, label, 12)
                        data = physical_data(engine, loads, action, label)
                        result = engine.evaluate(data['edges'], data['field'], data['beta'])
                        cardinal = data['cardinal']
                        base_field = cardinal @ directions['field_vertices']
                        base_edges = cardinal @ directions['edge_vertices']
                        source_correction = float(cardinal @ correction[:, -1])
                        local = []
                        for mode in ['original', 'compensated']:
                            field = base_field.copy()
                            edges = base_edges.copy()
                            source_direction = 0.
                            if mode == 'compensated':
                                field -= cardinal @ correction[:, :-1]
                                edges -= np.asarray(data['displacement'], float) * source_correction
                                source_direction = -source_correction
                            packet, direction = make_packet(engine, data, raw, row, acceleration, field, edges, source_direction)
                            field_decimal, edges_decimal = decimals(field), decimals(edges)
                            image_change = engine.tangent(data['edges'], data['field'], edges_decimal, field_decimal)
                            source_values = action.solver.values(action.solution, np.array([float(data['source'])]))[0]
                            lapse = float(np.exp(source_values[1, 0]))
                            metric = float(1 - 2 * source_values[0, 0] / float(data['source']))
                            clock = np.sqrt(lapse**2 - float(data['source_velocity'])**2 / metric)
                            inertia = action.owner.source_mass * lapse**2 / (metric * clock**3)
                            moments = []
                            selected = order == 64 and index in [0, 31, 63]
                            if selected:
                                probe_paths.append(save(name + '-' + mode + '-probe' + str(index), **packet,
                                    **{'direction_' + key: value for key, value in direction.items()},
                                    native_edges=np.array(data['edges'], str), native_field=np.array(data['field'], str),
                                    native_beta=np.array(data['beta'], str), native_beta_r=np.array(data['beta_radial'], str),
                                    native_direction_field=np.array(field_decimal, str), native_direction_edges=np.array(edges_decimal, str)))
                            for power in range(3):
                                wave = wave_blocks(packet, direction, power)
                                gram = gram_block(engine, data, result, field_decimal, edges_decimal, power, image_change)
                                dust = lapse**2 * metric * inertia * source_direction * (float(data['source']) - 6)**power
                                moments.append([wave[0], float(gram['total']), dust, wave[0] + float(gram['total']) + dust,
                                    wave[1], float(gram['field']), float(gram['bulk']), float(gram['local']), wave[2]])
                                if selected:
                                    actual = wave_current(packet, power)
                                    finite = finite_wave_current(packet, power)
                                    close(name + ':wave_raw_endpoint:' + mode + ':' + str(index) + ':' + str(power), finite[2] - actual, 2e-15 + 1e-8 * abs(actual))
                                    complex_velocity = wave_current(perturb(packet, direction, 1e-20j), power).imag / 1e-20
                                    complex_acceleration = wave_current(perturb(packet, direction, 1e-20j, True), power).imag / 1e-20
                                    close(name + ':analytic_velocity:' + mode + ':' + str(index) + ':' + str(power), complex_velocity - wave[0], 2e-16)
                                    close(name + ':analytic_acceleration:' + mode + ':' + str(index) + ':' + str(power), complex_acceleration - wave[1], 2e-17)
                                    estimates = []
                                    for step in [.1, .05, .025]:
                                        pair = [finite_wave_current(perturb(packet, direction, sign * step), power)[2] for sign in [1, -1]]
                                        estimates.append((pair[0] - pair[1]) / (2 * step))
                                    estimate = (4 * estimates[2] - estimates[1]) / 3
                                    close(name + ':mixed_finite_action:' + mode + ':' + str(index) + ':' + str(power), estimate - wave[0], 2e-14 + 1e-6 * abs(wave[0]))
                                    finite_rows.append(dict(branch=branch, level=level, mode=mode, label=float(label), power=power,
                                        current=float(actual), action_endpoint_current=float(finite[2]), endpoint_error=float(finite[2] - actual),
                                        velocity=float(wave[0]), finite_velocity=float(estimate), mixed_error=float(estimate - wave[0]),
                                        acceleration=float(wave[1]), complex_acceleration=float(complex_acceleration)))
                                    if index == 31:
                                        native_radius = np.asarray(data['edges'][engine.native_edges], float)
                                        evaluated = action.solver.values(action.solution, native_radius)[0]
                                        scale = decimals(np.exp(2 * evaluated[1]) * (1 - 2 * evaluated[0] / native_radius))
                                        estimates = []
                                        for step in [Decimal('.0001'), Decimal('.00005'), Decimal('.000025')]:
                                            raw_pair, endpoint_pair = [], []
                                            for sign in [1, -1]:
                                                raw_pair.append(finite_gram_action(direct, data['edges'], data['field'], field_decimal, data['beta'], scale,
                                                    Decimal.from_float(source_direction), power, Decimal(0), sign * step))
                                                endpoint_pair.append(endpoint_functional(direct, data['edges'], data['field'], field_decimal, data['beta'], data['beta_radial'], edges_decimal,
                                                    Decimal.from_float(source_direction), power, Decimal(0), sign * step))
                                            estimates.append((raw_pair[0] - raw_pair[1] - endpoint_pair[0] + endpoint_pair[1]) / (2 * step))
                                        predicted = (4 * estimates[2] - estimates[1]) / 3
                                        error = predicted - gram['total']
                                        close(name + ':Gram_mixed_action:' + mode + ':' + str(power), abs(error), Decimal('1e-22') + Decimal('2e-7') * gram['absolute_scale'])
                                        gram_rows.append(dict(branch=branch, level=level, mode=mode, power=power, analytic=str(gram['total']), finite=str(predicted), difference=str(error)))
                            local.append(moments)
                        values.append(local)
                    values = np.array(values)
                    average = np.tensordot(weights, values, axes=(0, 0))
                    averages.append(average)
                    paths.append(save(name + '-material' + str(order), labels=labels, weights=weights, values=values, average=average, channels=np.array(CHANNELS)))
                    for mode_index, mode in enumerate(['original', 'compensated']):
                        for power in range(3):
                            summaries.append(dict(branch=branch, level=level, mode=mode, material_order=order, power=power,
                                **dict(zip(CHANNELS, map(float, average[mode_index, power])))))
                close(name + ':material_quadrature', np.max(abs(averages[0] - averages[1])), 2e-15)
                evidence.report['cases'].append(dict(branch=branch, level=level, sources=sources, material_paths=paths, probe_paths=probe_paths,
                    correction_path=corrected['output'], direction_path=case['direction_path']))
                progress(name + ':saved')
        for filename, rows in [('support-shift-blocks.csv', summaries), ('wave-mixed-action-checks.csv', finite_rows), ('Gram-mixed-action-checks.csv', gram_rows)]:
            path = evidence.output / filename
            with path.open('w', newline='', encoding='utf-8') as stream:
                writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
                writer.writeheader()
                writer.writerows(rows)
            evidence.own(path, 'outputs')
        evidence.report.update(seconds=perf_counter() - started, summaries=summaries)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    with contextlib.redirect_stderr(__import__('sys').stdout):
        main()
