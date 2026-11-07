from derive_annular_source_gravity_20260914 import EvidenceRun
from diagnose_annular_wave_flux_third_20260930 import verified_sources
from annular_native_precision_context_20260929 import restore_native
from annular_position_reaction_registered_20260930 import hybrid_position_reaction
from annular_position_reaction_20260929 import ResponseSum
from annular_joint_first_tangent_20260922 import MetricResponse
from annular_candidate_energy_current_20260921 import reconstructed_solver
from decimal import Decimal, localcontext
from time import perf_counter
import argparse
import ctypes
import csv
import hashlib
import json
import numpy as np


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--label', required=True)
    parser.add_argument('--branch', choices=['reference-reference', 'MTS-primary'], required=True)
    parser.add_argument('--cpu', type=int, choices=[2, 4], required=True)
    parser.add_argument('--levels', nargs='+', choices=['fine', 'third'], default=['fine', 'third'])
    parser.add_argument('--seconds', type=float, default=6500.)
    args = parser.parse_args()
    kernel = ctypes.windll.kernel32
    kernel.GetCurrentProcess.restype = ctypes.c_void_p
    kernel.SetProcessAffinityMask.argtypes = [ctypes.c_void_p, ctypes.c_size_t]
    if not kernel.SetProcessAffinityMask(kernel.GetCurrentProcess(), 1 << args.cpu):
        raise OSError('Cannot set single-core affinity')
    evidence = EvidenceRun(args.label, __file__)
    started, deadline = perf_counter(), perf_counter()+args.seconds
    try:
        evidence.report.update(diagnostic_only=True, accepted_for_C0=False, branch=args.branch,
            logical_cpu=args.cpu, github_action=False, subagents_used=False, original_workbench_write=False,
            fresh_momentum_and_source_force=True, unchanged_field_wave_and_native_force_reused=True,
            residual_update_uses_linearity=False, all_force_components_newly_integrated=False,
            metric_coordinate_rule='Original registered polynomial centers retained',
            inherited_position_density_precision_warnings=4, inherited_mixed_time_precision_warnings=4,
            inherited_raw_C2_warnings=2, units='code-normalized', rule_outputs=[])
        if len(set(args.levels)) != len(args.levels):
            raise ValueError('Duplicate levels are not permitted')
        evidence.report['requested_levels'] = args.levels
        for name in ['DERIVATION-20260930-refined-wave-and-fresh-Euler-check.md',
                'scripts/annular_position_reaction_registered_20260930.py']:
            evidence.own(evidence.root/name)
        digests = verified_sources(evidence)

        def ingest(name):
            path = evidence.output.parent/name/'status.json'
            status = json.loads(path.read_text())
            evidence.own(path)
            digests[str(path.relative_to(evidence.root))] = hashlib.sha256(path.read_bytes()).hexdigest()
            evidence.check(name+':complete', status['state'] == 'complete'
                and all(row['passed'] for row in status['checks']))
            for category in ['inputs', 'outputs']:
                for relative, expected in status[category].items():
                    if relative == 'CURRENT_LOCAL_RESUME.md':
                        continue
                    path = (evidence.root/relative).resolve()
                    if not path.is_relative_to(evidence.root) or not path.is_file():
                        raise RuntimeError('Out-of-scope or missing input: '+relative)
                    if relative in digests and digests[relative] != expected:
                        raise RuntimeError('Conflicting authority: '+relative)
                    if hashlib.sha256(path.read_bytes()).hexdigest() != expected:
                        raise RuntimeError('Changed authority: '+relative)
                    digests[relative] = expected
                    evidence.own(path)
            return status

        def progress(stage):
            evidence.report['progress'] = dict(stage=stage, seconds=perf_counter()-started)
            evidence.save()
            print(json.dumps(evidence.report['progress']), flush=True)
            if perf_counter() > deadline:
                raise RuntimeError('Safe fresh Euler boundary')

        def save(name, **arrays):
            path = evidence.output/(name+'.npz')
            np.savez_compressed(path, **arrays)
            evidence.own(path, 'outputs')
            return str(path.relative_to(evidence.root))

        def response(archive):
            solver, solution = reconstructed_solver(archive)
            return MetricResponse(solver, solution, archive.get('forcing'), 0., [])

        authorities = {
            'fine': ('annular-wave-flux-live-response-fine-attempt01',
                'annular-wave-flux-events-reference-attempt02' if args.branch == 'reference-reference'
                else 'annular-wave-flux-events-MTS-fine-attempt01'),
            'third': ('annular-wave-flux-live-response-third-attempt01',
                'annular-wave-flux-events-reference-third-attempt03' if args.branch == 'reference-reference'
                else 'annular-wave-flux-events-MTS-third-attempt02')}
        parents = {level: tuple(ingest(name) for name in authorities[level]) for level in args.levels}
        summaries = []
        with localcontext() as context:
            context.prec = 70
            for level in args.levels:
                progress(level+':restore')
                setup = restore_native(evidence, digests, args.branch, level, deadline)
                loads, action, read, inverse = setup['loads'], setup['action'], setup['read'], setup['inverse']
                norm = lambda values: float(np.max(np.abs(inverse.solve(np.asarray(values, float).ravel()))))
                report = lambda name: read(str((evidence.output.parent/name/'status.json').relative_to(evidence.root)))
                match = lambda status: next(row for row in status['cases']
                    if row['branch'] == args.branch and row['level'] == level)
                live = match(report('annular-live-support-acceleration-attempt01'))
                jets = match(report('annular-position-metric-jet-validation-attempt01'))
                flow = match(report('annular-direct-background-coupled-current-attempt01'))
                directions = read(live['direction_path'])
                correction = read(live['paths']['projection'])['correction']
                mode_rate = read(jets['paths']['completed_metric_time'])['mode_rate']
                acceleration = read(flow['paths']['flow'])['acceleration']
                metric_time = ResponseSum(response(read(flow['paths']['background_response'])),
                    response(read(flow['paths']['velocity_response'])))
                live_parent, wave_parent = parents[level]
                candidate_row = next(row for row in live_parent['cases']
                    if row['summary']['branch'] == args.branch and row['summary']['level'] == level)
                candidate = read(candidate_row['paths']['candidate'])
                mixed = response(candidate)
                evidence.check(level+':reaction_shape', candidate['acceleration_change'].shape == loads.rates.shape
                    and np.isfinite(candidate['acceleration_change']).all())
                wave_rows = {row['summary']['radial_order']: row for row in wave_parent['cases']}
                evidence.check(level+':wave_identity', wave_parent['branch'] == args.branch and wave_parent['level'] == level
                    and all(wave_rows[order]['summary']['pair_passed'] for order in [24, 32]))
                native = report('annular-native-tangent-precision-repair-attempt01')
                native_rows = {row['summary']['order']: row for row in native['cases'] if row['summary']['level'] == level}
                arrays, paths, rules = {}, {}, []
                for order, radial_order, native_order in [(48, 24, 64), (64, 32, 96)]:
                    progress(level+':fresh-rule-'+str(order))
                    checked = hybrid_position_reaction(loads, action, setup['native'], directions, correction, mode_rate,
                        acceleration, setup['precision'].position, metric_time, mixed, order, deadline,
                        lambda stage: progress(level+':'+stage), acceleration_change=candidate['acceleration_change'],
                        include_native=False)
                    evidence.check(level+':finite-'+str(order), all(np.isfinite(values).all() for values in checked.values()))
                    evidence.check(level+':mixed_jet-'+str(order), norm(checked['oracle_difference']) <= 2e-11,
                        norm(checked['oracle_difference']))
                    original = setup['original'][order]
                    source_difference = np.zeros_like(loads.rates)
                    source_difference[:, -1] = checked['force_wave'][:, -1]-original['force_wave'][:, -1]
                    evidence.check(level+':source_force_independent_of_reaction-'+str(order),
                        np.array_equal(checked['force_wave'][:, -1], original['force_wave'][:, -1]), norm(source_difference))
                    wave = read(wave_rows[radial_order]['path'])['complete_flux'].copy()
                    wave[:, -1] = checked['force_wave'][:, -1]
                    native_force = np.zeros_like(loads.rates)
                    if args.branch == 'MTS-primary':
                        values = read(native_rows[native_order]['path'])['force_decimal']
                        native_force = np.array([float(Decimal(value)) for value in values.ravel()]).reshape(loads.rates.shape)
                    residual = checked['momentum_rate']-wave-native_force
                    old_weak_residual = checked['momentum_rate']-checked['force_wave']-native_force
                    oracle_residual = checked['oracle_momentum_rate']-wave-native_force
                    row = dict(branch=args.branch, level=level, material_order=order,
                        radial_order=radial_order, label_order=28 if order == 48 else 36, native_order=native_order,
                        fresh_Euler_inverse=norm(residual), fresh_Euler_passed=norm(residual) <= 2e-11,
                        oracle_Euler_inverse=norm(oracle_residual), mixed_jet_inverse=norm(checked['oracle_difference']),
                        old_weak_Euler_inverse=norm(old_weak_residual),
                        fresh_weak_vs_flux_inverse=norm(checked['force_wave']-wave),
                        source_force_change_inverse=norm(source_difference),
                        high_linear_update_discrepancy=None if order == 48 else norm(residual-candidate['residual_by_linear_update']),
                        seconds=perf_counter()-started, valid_for_claim=False)
                    path = save(args.branch+'-'+level+'-fresh-material'+str(order), **checked,
                        full_flux_wave_force=wave, repaired_native_force=native_force,
                        fresh_complete_residual=residual, fresh_oracle_residual=oracle_residual,
                        old_weak_complete_residual=old_weak_residual)
                    evidence.report['rule_outputs'].append(dict(summary=row, path=path))
                    evidence.save()
                    print(json.dumps(row), flush=True)
                    arrays[order], paths[order] = residual, path
                    rules.append(row)
                paired = norm(arrays[64]-arrays[48])
                summary = dict(branch=args.branch, level=level, fresh_high_Euler_inverse=rules[-1]['fresh_Euler_inverse'],
                    fresh_low_Euler_inverse=rules[0]['fresh_Euler_inverse'], corrected_rule_pair_inverse=paired,
                    corrected_rule_pair_passed=paired <= 2e-11,
                    both_fresh_Euler_rules_passed=all(row['fresh_Euler_passed'] for row in rules),
                    high_linear_update_discrepancy=rules[-1]['high_linear_update_discrepancy'],
                    high_linear_update_agreement_passed=rules[-1]['high_linear_update_discrepancy'] <= 2e-11,
                    fresh_weak_vs_flux_inverse=rules[-1]['fresh_weak_vs_flux_inverse'],
                    old_weak_gate_retained=True, fresh_momentum_reintegration=True,
                    unchanged_force_components_reused=True, valid_for_claim=False)
                evidence.report['cases'].append(dict(summary=summary, paths=paths, rules=rules))
                summaries.append(summary)
                evidence.save()
                print(json.dumps(summary), flush=True)
        table = evidence.output/'fresh-Euler-checks.csv'
        with table.open('x', newline='', encoding='utf-8') as stream:
            writer = csv.DictWriter(stream, fieldnames=list(summaries[0]))
            writer.writeheader()
            writer.writerows(summaries)
        evidence.own(table, 'outputs')
        evidence.report['all_fresh_equation_checks_passed'] = all(row['both_fresh_Euler_rules_passed']
            and row['corrected_rule_pair_passed'] and row['high_linear_update_agreement_passed'] for row in summaries)
        evidence.report['seconds'] = perf_counter()-started
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
