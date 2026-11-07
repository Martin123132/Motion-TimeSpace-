from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_C0_boundary_integral_v2_20260930 import PositionIntegral, native_event_atoms, dust_event_atoms, native_coefficient_rows
from annular_position_support_column_20260930 import native_rows, native_position_probe, dust_rows, dust_position_column, gravity_position_rows
from annular_native_precision_context_20260929 import restore_native
from annular_native_tangent_precision_repair_20260929 import repair_engine
from annular_position_reaction_20260929 import ResponseSum
from annular_joint_first_tangent_20260922 import MetricResponse
from annular_candidate_energy_current_20260921 import reconstructed_solver
from annular_physical_native_kernel_20260928 import decimals
from decimal import Decimal, localcontext
from time import perf_counter
import argparse
import ctypes
import csv
import hashlib
import json
import numpy as np


def verified_sources(evidence):
    path = evidence.output.parent/'annular-position-support-stage-integrity-20260930.json'
    seal = json.loads(path.read_text())
    evidence.own(path)
    evidence.check('prior_seal_complete', seal['state'] == 'complete' and not seal['mismatches']
        and seal['all_four_fresh_Euler_checks_complete_and_passed'] and seal['C0_actual_pointwise_probes'] == 12)
    digests = {}

    def accept(relative, expected):
        if relative == 'CURRENT_LOCAL_RESUME.md':
            return
        source = (evidence.root/relative).resolve()
        if not source.is_relative_to(evidence.root) or not source.is_file():
            raise RuntimeError('Missing or out-of-scope C0 input: '+relative)
        if hashlib.sha256(source.read_bytes()).hexdigest() != expected:
            raise RuntimeError('Changed C0 input: '+relative)
        key = str(source.relative_to(evidence.root))
        if key in digests and digests[key] != expected:
            raise RuntimeError('Conflicting C0 source')
        digests[key] = expected
        evidence.own(source)

    for relative, expected in seal['hashes'].items():
        accept(relative, expected)
    path = evidence.output.parent/'annular-C0-boundaries-manufactured-attempt01/status.json'
    status = json.loads(path.read_text())
    evidence.check('boundary_manufactured_complete', status['state'] == 'complete' and all(row['passed'] for row in status['checks']))
    accept(str(path.relative_to(evidence.root)), hashlib.sha256(path.read_bytes()).hexdigest())
    for category in ['inputs', 'outputs']:
        for relative, expected in status[category].items():
            accept(relative, expected)
    return digests


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--label', required=True)
    parser.add_argument('--reuse-wave-parent')
    parser.add_argument('--branch', choices=['reference-reference', 'MTS-primary'], required=True)
    parser.add_argument('--cpu', type=int, choices=[2, 4], required=True)
    parser.add_argument('--seconds', type=float, default=10000.)
    parser.add_argument('--levels', nargs='+', choices=['fine', 'third'], default=['fine', 'third'])
    args = parser.parse_args()
    kernel = ctypes.windll.kernel32
    kernel.GetCurrentProcess.restype = ctypes.c_void_p
    kernel.SetProcessAffinityMask.argtypes = [ctypes.c_void_p, ctypes.c_size_t]
    if not kernel.SetProcessAffinityMask(kernel.GetCurrentProcess(), 1 << args.cpu):
        raise OSError('Cannot set single-core affinity')
    evidence = EvidenceRun(args.label, __file__)
    started, deadline = perf_counter(), perf_counter()+args.seconds
    try:
        evidence.report.update(branch=args.branch, logical_cpu=args.cpu, github_action=False, subagents_used=False,
            original_workbench_write=False, units='code-normalized', complete_C0_accepted=False,
            reaction_sensitivity_propagated=False, finite_history_established=False,
            inherited_position_density_precision_warnings=4, inherited_mixed_time_precision_warnings=4,
            inherited_raw_C2_warnings=2, old_weak_flux_flags_retained=True, rule_outputs=[])
        digests = verified_sources(evidence)
        evidence.own(evidence.root/'DERIVATION-20260930-C0-boundary-integral.md')

        def progress(stage):
            evidence.report['progress'] = dict(stage=stage, seconds=perf_counter()-started)
            evidence.save()
            print(json.dumps(evidence.report['progress']), flush=True)
            if perf_counter() > deadline:
                raise RuntimeError('Safe C0 boundary')

        def save(name, **arrays):
            path = evidence.output/(name+'.npz')
            np.savez_compressed(path, **arrays)
            evidence.own(path, 'outputs')
            return str(path.relative_to(evidence.root))

        def response(archive):
            solver, solution = reconstructed_solver(archive)
            return MetricResponse(solver, solution, archive.get('forcing'), 0., [])

        reusable = {}
        if args.reuse_wave_parent:
            path = evidence.output.parent/args.reuse_wave_parent/'status.json'
            prior = json.loads(path.read_text())
            evidence.own(path)
            evidence.check('wave_reuse_known_native_zero_type_failure', prior['state'] == 'failed'
                and prior['branch'] == args.branch and 'float' in prior['error']
                and 'decimal.Decimal' in prior['error'] and 'unsupported operand' in prior['error'])
            for category in ['inputs', 'outputs']:
                for relative, expected in prior[category].items():
                    if relative == 'CURRENT_LOCAL_RESUME.md':
                        continue
                    source = (evidence.root/relative).resolve()
                    if not source.is_relative_to(evidence.root) or hashlib.sha256(source.read_bytes()).hexdigest() != expected:
                        raise RuntimeError('Changed reusable wave input: '+relative)
                    digests[str(source.relative_to(evidence.root))] = expected
                    evidence.own(source)
            for row in prior['rule_outputs']:
                if row['component'] == 'wave':
                    reusable[row['level'], row['order']] = row['path']
            evidence.check('two_fine_wave_rules_reusable', all(('fine', order) in reusable for order in [24, 32]))
            evidence.report['reused_completed_wave_parent'] = args.reuse_wave_parent

        summaries = []
        with localcontext() as context:
            context.prec = 70
            for level in args.levels:
                progress(level+':restore')
                setup = restore_native(evidence, digests, args.branch, level, deadline)
                loads, action, read = [setup[key] for key in ['loads', 'action', 'read']]
                report = lambda name:read(str((evidence.output.parent/name/'status.json').relative_to(evidence.root)))
                match = lambda status:next(row for row in status['cases'] if row['branch'] == args.branch and row['level'] == level)
                live = match(report('annular-live-support-acceleration-attempt01'))
                jets = match(report('annular-position-metric-jet-validation-attempt01'))
                flow = match(report('annular-direct-background-coupled-current-attempt01'))
                directions = read(live['direction_path'])
                correction = read(live['paths']['projection'])['correction']
                mode_rate = read(jets['paths']['completed_metric_time'])['mode_rate']
                acceleration = read(flow['paths']['flow'])['acceleration']
                metric_time = ResponseSum(response(read(flow['paths']['background_response'])), response(read(flow['paths']['velocity_response'])))
                owned = report('annular-wave-flux-live-response-'+level+'-attempt01')
                selected = next(row for row in owned['cases'] if row['summary']['branch'] == args.branch and row['summary']['level'] == level)
                candidate = read(selected['paths']['candidate'])
                mixed, position = response(candidate), setup['precision'].position
                precision = repair_engine(setup['precision'])
                evaluator = PositionIntegral(action, directions, correction, mode_rate, acceleration,
                    candidate['acceleration_change'], position, metric_time, mixed)
                eigen_labels = [-.5, .5]
                roots = np.polynomial.chebyshev.chebroots(np.polynomial.chebyshev.chebder(evaluator.geometry.source_derivative))
                eigen_labels += [float(value.real/2) for value in roots if abs(value.imag) < 1e-12 and abs(value.real) < 1]
                minimum_source_slope = min(float(evaluator.geometry.geometry(0., label)[1]) for label in eigen_labels)
                evidence.check(level+':label_monotonicity', minimum_source_slope > 0 and action.owner.width > 0, minimum_source_slope)
                paths, wave = {}, {}
                for radial_order, label_order in [(24, 28), (32, 36)]:
                    progress(level+':wave-'+str(radial_order))
                    if (level, radial_order) in reusable:
                        path = reusable[level, radial_order]
                        result = read(path)
                    else:
                        result = evaluator.integrate_rows(radial_order, label_order, deadline, lambda stage:progress(level+':'+stage))
                        path = save(level+'-wave-'+str(radial_order), **result)
                    evidence.check(level+':wave_finite-'+str(radial_order), all(np.isfinite(value).all() for value in result.values()))
                    wave[radial_order], paths['wave'+str(radial_order)] = result, path
                    evidence.report['rule_outputs'].append(dict(level=level, component='wave', order=radial_order,
                        complete=result['complete'].tolist(), path=path, seconds=perf_counter()-started))
                    evidence.save()
                progress(level+':native-and-dust')
                matter = {}
                for order in [48, 64]:
                    labels, weights = np.polynomial.legendre.leggauss(order)
                    labels, weights = labels/2, weights/2
                    weights *= 6*(labels+.5)*(.5-labels)
                    native_columns, dust_columns, native_base, dust_base = [], [], [], []
                    for index, label in enumerate(labels):
                        data, unused, unused2, unused3, unused4 = precision.packet(float(label), 'decimal_tangents')
                        if setup['native'].enabled:
                            probed = native_position_probe(precision, mode_rate, directions, float(label), steps=())
                            native_columns.append(probed['derivative'])
                            native_base.append(probed['base'])
                            if index == 0:
                                cardinal = data['cardinal']
                                field_test = cardinal@decimals(directions['field_vertices'])
                                edge_test = cardinal@decimals(directions['edge_vertices'])
                                beta_rows, radial_rows = native_coefficient_rows(setup['native'], data, field_test, edge_test)
                                linear_rows = beta_rows@data['beta']+radial_rows@data['beta_radial']
                                direct_rows = np.array(native_rows(setup['native'], data, field_test, edge_test), dtype=object)
                                error = float(np.max(abs(linear_rows-direct_rows)))
                                evidence.check(level+':native_coefficient_linear_replay:'+str(order), error <= 1e-35, error)
                        else:
                            native_columns.append(np.zeros(4))
                            native_base.append(np.zeros(4))
                        source, velocity = float(data['source']), float(data['source_velocity'])
                        cardinal_float = np.asarray(data['cardinal'], float)
                        source_change = -float(cardinal_float@correction[:, -1])
                        velocity_change = float(cardinal_float@mode_rate[:, -1])
                        values, radial = action.solver.values(action.solution, np.array([source]))
                        material_values = position.values(np.array([source]))[:, 0]+radial[:, 0]*source_change
                        dust_columns.append(dust_position_column(source, velocity, values[:, 0], action.owner.source_mass,
                            source_change, velocity_change, material_values))
                        dust_base.append(dust_rows(source, velocity, values[:, 0], action.owner.source_mass))
                        if index % 16 == 15:
                            progress(level+':matter'+str(order)+':'+str(index+1))
                    matter[order] = dict(native=weights@np.array(native_columns), dust=weights@np.array(dust_columns),
                        native_base=weights@np.array(native_base), dust_base=weights@np.array(dust_base))
                    paths['matter'+str(order)] = save(level+'-matter-'+str(order), labels=labels, weights=weights,
                        native_layers=np.array(native_columns), dust_layers=np.array(dust_columns), **matter[order])
                    evidence.report['rule_outputs'].append(dict(level=level, component='native-and-dust', order=order,
                        path=paths['matter'+str(order)], seconds=perf_counter()-started))
                    evidence.save()
                progress(level+':coefficient-cut-events')
                native_events = native_event_atoms(precision, directions, evaluator.geometry, deadline, lambda stage:progress(level+':'+stage))
                dust_events = dust_event_atoms(precision, evaluator.geometry)
                paths['events'] = save(level+'-events', **{'native_'+key:value for key, value in native_events.items()},
                    **{'dust_'+key:value for key, value in dust_events.items()})
                gravity = {order:gravity_position_rows(action, position, metric_time, mixed, order) for order in [24, 32]}
                total, baselines = [], []
                for wave_order, matter_order in [(24, 48), (32, 64)]:
                    full = wave[wave_order]['complete']+matter[matter_order]['native']+native_events['atoms']
                    full[1:] += matter[matter_order]['dust']+dust_events['atoms']+gravity[wave_order]['column']
                    baseline = wave[wave_order]['base']+matter[matter_order]['native_base']
                    baseline[1:] += matter[matter_order]['dust_base']+gravity[wave_order]['base']
                    total.append(full)
                    baselines.append(baseline)
                difference = np.abs(total[1]-total[0])
                paths['combined'] = save(level+'-combined', coarse=total[0], fine=total[1], paired_difference=difference,
                    baseline_coarse=baselines[0], baseline_fine=baselines[1],
                    gravity24=gravity[24]['column'], gravity32=gravity[32]['column'])
                summary = dict(branch=args.branch, level=level, C0=total[1].tolist(), paired_difference=difference.tolist(),
                    paired_max=float(np.max(difference)), paired_passed=bool(np.max(difference) <= 2e-17),
                    native_event_count=int(native_events['events']), dust_event_count=int(dust_events['events']),
                    native_event_max=float(np.max(abs(native_events['atoms']))),
                    dust_event_max=float(np.max(abs(dust_events['atoms']))),
                    wave_face_max=float(np.max(abs(wave[32]['material_faces']))),
                    complete_integral_constructed=True, reaction_sensitivity_propagated=False, valid_for_claim=False)
                evidence.report['cases'].append(dict(summary=summary, paths=paths))
                summaries.append(summary)
                evidence.save()
                print(json.dumps(summary), flush=True)
        table = evidence.output/'C0-integral-checks.csv'
        with table.open('x', newline='', encoding='utf-8') as stream:
            writer = csv.DictWriter(stream, fieldnames=list(summaries[0]))
            writer.writeheader()
            writer.writerows(summaries)
        evidence.own(table, 'outputs')
        evidence.report['all_integral_pairs_passed'] = all(row['paired_passed'] for row in summaries)
        evidence.report['seconds'] = perf_counter()-started
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()


