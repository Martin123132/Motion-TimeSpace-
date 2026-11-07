from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_native_precision_context_20260929 import restore_native
from annular_wave_flux_form_20260929 import WaveFlux
from decimal import localcontext
from pathlib import Path
from time import perf_counter
import argparse
import csv
import hashlib
import json
import numpy as np


def verified_sources(evidence):
    path = evidence.output.parent/'annular-native-precision-repair-integrity-20260929.json'
    prior = json.loads(path.read_text())
    evidence.own(path)
    evidence.check('prior_seal_complete', prior['state'] == 'complete' and prior['native_pairs_passed'])
    digests = {}
    for relative, expected in prior['hashes'].items():
        if relative == 'CURRENT_LOCAL_RESUME.md':
            continue
        source = (evidence.root/relative).resolve()
        if not source.is_relative_to(evidence.root) or not source.is_file():
            raise RuntimeError('Missing or out-of-scope input: '+relative)
        if hashlib.sha256(source.read_bytes()).hexdigest() != expected:
            raise RuntimeError('Changed input: '+relative)
        digests[relative] = expected
        evidence.own(source)
    evidence.check('inherited_hashes_match', len(digests) == len(prior['hashes'])-1, len(digests))
    return digests


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--label', required=True)
    parser.add_argument('--orders', default='12:48,16:64,20:96')
    parser.add_argument('--seconds', type=float, default=3600.)
    parser.add_argument('--branch', default='reference-reference', choices=['reference-reference', 'MTS-primary'])
    parser.add_argument('--level', default='fine', choices=['fine', 'third'])
    args = parser.parse_args()
    rules = [tuple(map(int, item.split(':'))) for item in args.orders.split(',')]
    if any(len(rule) != 2 or min(rule) < 2 for rule in rules) or len(set(rules)) != len(rules):
        raise ValueError('Distinct positive radial:label rules required')
    evidence = EvidenceRun(args.label, __file__)
    started, deadline = perf_counter(), perf_counter()+args.seconds
    try:
        evidence.report.update(diagnostic_only=True, accepted_for_C0=False, numerical_acceptance_passed=False,
            actual_flux_by_parts_implemented=True, full_live_reaction_recomputed=False,
            branch=args.branch, level=args.level, github_action=False, subagents_used=False, original_workbench_write=False)
        for name in ['scripts/annular_wave_flux_form_20260929.py', 'DERIVATION-20260929-actual-wave-flux-integration.md']:
            evidence.own(evidence.root/name)
        digests = verified_sources(evidence)

        def progress(stage):
            evidence.report['progress'] = dict(stage=stage, seconds=perf_counter()-started)
            evidence.save()
            print(json.dumps(evidence.report['progress']), flush=True)

        with localcontext() as context:
            context.prec = 70
            restored = restore_native(evidence, digests, args.branch, args.level, deadline)
            action, loads, read = restored['action'], restored['loads'], restored['read']
            status = lambda name: read(str((evidence.output.parent/name/'status.json').relative_to(evidence.root)))
            match = lambda report: next(row for row in report['cases'] if row['branch'] == args.branch and row['level'] == args.level)
            live = match(status('annular-live-support-acceleration-attempt01'))
            jets = match(status('annular-position-metric-jet-validation-attempt01'))
            directions = read(live['direction_path'])
            correction = read(live['paths']['projection'])['correction']
            mode_rate = read(jets['paths']['completed_metric_time'])['mode_rate']
            wave = WaveFlux(action, directions, correction, mode_rate, restored['precision'].position)
            inverse = restored['inverse']
            invmax = lambda value: float(np.max(np.abs(inverse.solve(value.ravel()))))
            maximum = lambda value: float(np.max(np.abs(value)))
            baseline = restored['original'][64]['base_force_wave'].copy()
            baseline[:, -1] = 0.
            high_baseline = None
            if args.branch == 'reference-reference' and args.level == 'fine':
                parent = status('annular-original-label-rule-diagnostic-attempt03')
                row = next(item for item in parent['cases'] if item['summary']['material_order'] == 2048)
                high_baseline = read(row['path'])['force'].copy()
                high_baseline[:, -1] = 0.
            evidence.report['dimensions'] = dict(rates=list(loads.rates.shape), material_cells=len(wave.widths),
                radial_cuts=len(wave.radial_cuts), metric_cells=len(wave.metric.lengths))
            progress('restored')
            rows, previous = [], None
            for radial_order, label_order in rules:
                result, diagnostics = wave.integrate(radial_order, label_order, loads.rates.shape, deadline, progress)
                evidence.check('finite_'+str(radial_order)+'_'+str(label_order),
                    all(np.isfinite(value).all() for value in result.values()))
                summary = dict(radial_order=radial_order, label_order=label_order,
                    weak_flux_inverse=invmax(result['regular_flux']-result['weak']),
                    base_weak_flux_raw=maximum(result['base_flux']-result['base_weak']),
                    derivative_oracle_inverse=invmax(result['oracle_difference']),
                    moving_cut_inverse=invmax(result['moving_cuts']),
                    omitted_jump_inverse=invmax(result['jumps']), omitted_endpoint_inverse=invmax(result['endpoints']),
                    maximum_radial_flux_jump=max(item['maximum_radial_flux_jump'] for item in diagnostics),
                    maximum_radial_change_jump=max(item['maximum_radial_change_jump'] for item in diagnostics),
                    maximum_metric_derivative_gap=max(item['metric_derivative_gap'] for item in diagnostics),
                    coincident_cuts=sum(item['coincident_cuts'] for item in diagnostics),
                    baseline64_gap=maximum(result['base_flux']-baseline),
                    baseline2048_gap=None if high_baseline is None else maximum(result['base_flux']-high_baseline),
                    successive_flux_inverse=None if previous is None else invmax(result['complete_flux']-previous['complete_flux']),
                    successive_weak_inverse=None if previous is None else invmax(result['complete_weak']-previous['complete_weak']),
                    successive_base_raw=None if previous is None else maximum(result['base_flux']-previous['base_flux']),
                    seconds=perf_counter()-started, valid_for_claim=False)
                summary['weak_flux_passed'] = summary['weak_flux_inverse'] <= 2e-11
                summary['baseline_replay_passed'] = None if high_baseline is None else summary['baseline2048_gap'] <= 2e-15
                summary['pair_passed'] = None if previous is None else summary['successive_flux_inverse'] <= 2e-11
                path = evidence.output/('wave-flux-'+str(radial_order)+'-'+str(label_order)+'.npz')
                np.savez_compressed(path, **result)
                evidence.own(path, 'outputs')
                evidence.report['cases'].append(dict(summary=summary, path=str(path.relative_to(evidence.root))))
                evidence.save()
                print(json.dumps(summary), flush=True)
                evidence.check('complex_step_'+str(radial_order)+'_'+str(label_order), summary['derivative_oracle_inverse'] <= 2e-11,
                    summary['derivative_oracle_inverse'])
                evidence.check('no_ambiguous_cut_'+str(radial_order)+'_'+str(label_order), summary['coincident_cuts'] == 0)
                rows.append(summary)
                previous = result
        path = evidence.output/'wave-flux-resolution.csv'
        with path.open('x', newline='', encoding='utf-8') as stream:
            writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
        evidence.own(path, 'outputs')
        evidence.report['seconds'] = perf_counter()-started
        evidence.report['all_available_pairs_passed'] = len(rows) >= 2 and all(row['pair_passed'] for row in rows[1:])
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
