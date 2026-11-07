from derive_annular_source_gravity_20260914 import EvidenceRun
from derive_annular_support_map_constraints_20260927 import restore_case, load_owned
from annular_compensated_position_20260928 import PositionLoads
from annular_physical_native_kernel_20260928 import NativeKernel
from annular_position_time_loads_20260929 import symbolic_checks, wave_moments, native_expansion, native_label, pushforward_moments
from decimal import localcontext
from time import perf_counter
import argparse
import csv
import gc
import hashlib
import json
import numpy as np


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--label', default='annular-position-time-loads-attempt01')
    parser.add_argument('--max-seconds', type=float, default=7200)
    parser.add_argument('--case-limit', type=int, default=4)
    args = parser.parse_args()
    evidence = EvidenceRun(args.label, __file__)
    started, deadline = perf_counter(), perf_counter() + args.max_seconds
    try:
        evidence.report.update(scope='Mixed weak position-time loading and owned interface atoms for B0',
            github_action=False, subagents_used=False, original_workbench_write=False, new_trajectories=0,
            B0_radial_solved=False, C0_old_reaction_solved=False, C0_current_column_computed=False,
            inherited_position_density_precision_warnings=4, inherited_mixed_time_precision_warnings=4,
            inherited_raw_C2_warnings=2, uncertainty_is_rigorous_bound=False,
            source_units='code-normalized', maximum_numerical_workers=1)
        evidence.own(evidence.root / 'DERIVATION-20260929-position-time-loads-and-interface-jumps.md')
        seal_path = evidence.output.parent / 'annular-old-reaction-final-integrity-20260929.json'
        seal = json.loads(seal_path.read_text())
        evidence.own(seal_path)
        digests, bad = {}, []
        for relative, expected in seal['hashes'].items():
            if relative == 'CURRENT_LOCAL_RESUME.md':
                continue
            path = evidence.root / relative
            if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
                bad.append(relative)
            else:
                digests[str(path.relative_to(evidence.root))] = expected
                evidence.own(path)
        evidence.check('scientific_parent_unchanged', seal['state'] == 'complete' and not bad, bad)
        read = lambda relative: load_owned(evidence, digests, evidence.root / relative)
        status = lambda name: read(str((evidence.output.parent / name / 'status.json').relative_to(evidence.root)))
        live = status('annular-live-support-acceleration-attempt01')
        jets = status('annular-position-metric-jet-validation-attempt01')
        direct = status('annular-direct-background-coupled-current-attempt01')
        symbolic_checks(evidence)

        def progress(stage):
            evidence.report['progress'] = dict(stage=stage, seconds=perf_counter() - started)
            evidence.save()
            print(json.dumps(evidence.report['progress']), flush=True)
            if perf_counter() > deadline:
                raise RuntimeError('Safe mixed-loading boundary')

        def save(name, **arrays):
            path = evidence.output / (name + '.npz')
            np.savez_compressed(path, **arrays)
            evidence.own(path, 'outputs')
            return str(path.relative_to(evidence.root))

        summaries, moment_rows, endpoint_rows = [], [], []
        with localcontext() as context:
            context.prec = 70
            for case in direct['cases'][:args.case_limit]:
                branch, level = case['branch'], case['level']
                name = branch + '-' + level
                progress(name + ':restore')
                loads, action, sources = restore_case(evidence, digests, branch, level, deadline)
                match = lambda report: next(row for row in report['cases'] if row['branch'] == branch and row['level'] == level)
                previous, jet = match(live), match(jets)
                directions = read(previous['direction_path'])
                correction = read(previous['paths']['projection'])['correction']
                mode_rate = read(jet['paths']['completed_metric_time'])['mode_rate']
                acceleration = read(case['paths']['flow'])['acceleration']
                packet = read(sources['packet'])
                native = NativeKernel(action.mesh, packet['gram_support'], branch.startswith('MTS'))
                engine = PositionLoads(loads, action, native, directions, correction)
                paths, waves = {}, {}
                for material, spatial in [(48, 8), (48, 12), (64, 12)]:
                    progress(name + ':wave-' + str(material) + '-' + str(spatial))
                    result = wave_moments(loads, action, directions, correction, mode_rate, acceleration,
                        material, spatial, deadline)
                    waves[material, spatial] = result
                    paths['wave_' + str(material) + '_' + str(spatial)] = save(name + '-wave-' + str(material) + '-' + str(spatial), **result)
                    tolerance = 5e-12 * result['local_scale'] + 1e-22
                    evidence.check(name + ':wave_product_rule:' + str(material) + ':' + str(spatial),
                        result['local_error'] <= tolerance, dict(error=result['local_error'], tolerance=tolerance))
                    evidence.check(name + ':positive_cell_J:' + str(material) + ':' + str(spatial), result['minimum_jacobian'] > 0)
                fine = waves[64, 12]['moments'][:, :, 3]
                spatial_error = abs(waves[48, 12]['moments'][:, :, 3] - waves[48, 8]['moments'][:, :, 3])
                material_error = abs(fine - waves[48, 12]['moments'][:, :, 3])
                wave_tolerance = 2e-8 * abs(fine) + 5e-21
                evidence.check(name + ':wave_material48_64', np.all(material_error <= wave_tolerance),
                    dict(error=material_error.tolist(), tolerance=wave_tolerance.tolist()))
                evidence.check(name + ':wave_spatial8_12', np.all(spatial_error <= wave_tolerance),
                    dict(error=spatial_error.tolist(), tolerance=wave_tolerance.tolist()))
                for channel, label in enumerate(['temporal_square', 'gradient_square']):
                    for power in range(3):
                        moment_rows.append(dict(branch=branch, level=level, channel=label, power=power,
                            weak_mixed=float(fine[channel, power]), regular_mixed=None, endpoint_mixed=None,
                            regular_plus_endpoint=None, error=float(material_error[channel, power]),
                            error_kind='material48_64', valid_for_claim=False))
                expansion = None
                native_probe_error, native_step_error = 0., 0.
                if native.enabled:
                    progress(name + ':native-expansion')
                    expansion = native_expansion(engine, mode_rate, 24, lambda stage: progress(name + ':' + stage))
                    paths['native'] = save(name + '-native-mixed-expansion', **expansion)
                    native_step_error = float(np.max(expansion['step_errors']))
                    evidence.check(name + ':native_step_halving', native_step_error <= 2e-10 * float(np.max(abs(expansion['values'][:, 3]))) + 1e-28, native_step_error)
                    probes = []
                    for label in [-.413, -.217, .071, .289, .447]:
                        values, step_error = native_label(engine, mode_rate, label)
                        fitted = np.array([np.polynomial.chebyshev.chebval(2 * label, coefficients) for coefficients in expansion['coefficients']])
                        error = np.max(abs(fitted - values), axis=1)
                        scale = np.max(abs(values), axis=1)
                        tolerance = 2e-8 * scale + 1e-23
                        evidence.check(name + ':native_offgrid:' + str(label), np.all(error <= tolerance),
                            dict(error=error.tolist(), tolerance=tolerance.tolist()))
                        native_probe_error = max(native_probe_error, float(error[3]))
                        probes.append([label, *error, step_error])
                    paths['native_probes'] = save(name + '-native-mixed-probes', rows=np.array(probes))
                pushforward_errors, pushforward_scales, jumps = [], [], []
                for kind, enabled in [('source_density', False), ('gram', True)]:
                    if enabled and not native.enabled:
                        continue
                    results = {}
                    for order in [48, 64]:
                        progress(name + ':' + kind + '-pushforward' + str(order))
                        results[order] = pushforward_moments(engine, mode_rate, expansion, enabled, order)
                        result = results[order]
                        paths[kind + str(order)] = save(name + '-' + kind + '-pushforward' + str(order),
                            **{key: value for key, value in result.items() if key != 'endpoints'})
                        scale = float(np.max(abs(result['weak'])))
                        tolerance = 2e-10 * scale + (1e-24 if enabled else 1e-22)
                        evidence.check(name + ':' + kind + ':regular_plus_atoms:' + str(order),
                            result['error'] <= tolerance, dict(error=result['error'], tolerance=tolerance,
                            omitted_atom_max=float(np.max(abs(result['atoms'])))))
                    result = results[64]
                    quadrature_error = float(np.max(abs(result['weak'] - results[48]['weak'])))
                    evidence.check(name + ':' + kind + ':material48_64', quadrature_error <= 2e-10 * float(np.max(abs(result['weak']))) + (1e-24 if enabled else 1e-22), quadrature_error)
                    pushforward_errors.append(result['error'])
                    pushforward_scales.append(float(np.max(abs(result['weak']))))
                    for power in range(3):
                        moment_rows.append(dict(branch=branch, level=level, channel=kind, power=power,
                            weak_mixed=float(result['weak'][power]), regular_mixed=float(result['regular'][power]),
                            endpoint_mixed=float(result['atoms'][power]), regular_plus_endpoint=float(result['total'][power]),
                            error=result['error'], error_kind='Decimal70_regular_plus_atom_identity', valid_for_claim=False))
                    for endpoint in result['endpoints']:
                        radius, velocity = endpoint['radius'], endpoint['speed']
                        values = action.solver.values(action.solution, np.array([radius]))[0][:, 0]
                        metric, lapse = 1 - 2 * values[0] / radius, np.exp(values[1])
                        if enabled:
                            coefficients = np.array([action.owner.coupling * radius**2 * metric, action.owner.coupling * radius])
                        else:
                            clock = np.sqrt(lapse**2 - velocity**2 / metric)
                            coefficients = action.owner.coupling * action.owner.source_mass * np.array([
                                np.sqrt(metric) * lapse / clock, velocity**2 / (radius * lapse * metric**1.5 * clock)])
                        metric_jump = coefficients * endpoint['atom']
                        endpoint_rows.append(dict(branch=branch, level=level, channel=kind, **endpoint,
                            metric_mass_jump=float(metric_jump[0]), metric_lapse_jump=float(metric_jump[1]),
                            valid_for_claim=False))
                        jumps.append(float(np.max(abs(metric_jump))))
                summary = dict(branch=branch, level=level,
                    wave_mixed_max=float(np.max(abs(fine))), wave_material_error=float(np.max(material_error)),
                    wave_spatial_error=float(np.max(spatial_error)), native_mixed_probe_error=native_probe_error,
                    native_step_error=native_step_error, pushforward_identity_error=max(pushforward_errors),
                    pushforward_weak_scale=max(pushforward_scales), metric_endpoint_jump_max=max(jumps),
                    endpoint_rows=sum(row['branch'] == branch and row['level'] == level for row in endpoint_rows),
                    valid_for_claim=False)
                summaries.append(summary)
                evidence.report['cases'].append(dict(branch=branch, level=level, paths=paths, summary=summary))
                progress(name + ':complete')
                del engine, native, loads, action, waves
                gc.collect()
        for name, rows in [('mixed-loading-summary', summaries), ('mixed-weak-moments', moment_rows), ('mixed-endpoint-atoms', endpoint_rows)]:
            path = evidence.output / (name + '.csv')
            with path.open('x', encoding='utf-8', newline='') as stream:
                writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
                writer.writeheader()
                writer.writerows(rows)
            evidence.own(path, 'outputs')
        evidence.report['seconds'] = perf_counter() - started
        evidence.complete()
    except BaseException as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
