from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_position_enabled_compatibility_20260930 import diagnose
from annular_exact_envelope_20261001 import envelope_search
from math import fsum
import argparse
import csv
import ctypes
import hashlib
import json
import numpy as np


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--reference-run', default='annular-coefficient-baseline-reference-third-attempt01')
    parser.add_argument('--MTS-run', default='annular-coefficient-baseline-MTS-third-attempt01')
    args = parser.parse_args()
    kernel = ctypes.windll.kernel32
    kernel.GetCurrentProcess.restype = ctypes.c_void_p
    kernel.SetProcessAffinityMask.argtypes = [ctypes.c_void_p, ctypes.c_size_t]
    if not kernel.SetProcessAffinityMask(kernel.GetCurrentProcess(), 4):
        raise OSError('Cannot pin one CPU')
    evidence = EvidenceRun('annular-integrated-baseline-assembly-attempt01', __file__)
    verified, summaries, component_rows = {}, [], []

    def verify(relative, expected=None):
        path = (evidence.root/relative).resolve()
        if not path.is_relative_to(evidence.root) or not path.is_file():
            raise RuntimeError('Invalid integrated assembly input '+relative)
        key = str(path.relative_to(evidence.root))
        if key not in verified:
            verified[key] = hashlib.sha256(path.read_bytes()).hexdigest()
            evidence.own(path)
        if expected is not None and verified[key]!=expected:
            raise RuntimeError('Changed integrated assembly input '+relative)
        return path

    def status(name):
        path = evidence.output.parent/name/'status.json'
        report = json.loads(verify(str(path.relative_to(evidence.root))).read_text())
        evidence.check(name+':complete', report['state']=='complete' and all(row['passed'] for row in report['checks']))
        for category in ['inputs', 'outputs']:
            for relative, expected in report[category].items():
                if relative!='CURRENT_LOCAL_RESUME.md':
                    verify(relative, expected)
        return report

    def owned_path(relative):
        path = (evidence.root/relative).resolve()
        if str(path.relative_to(evidence.root)) not in verified:
            raise RuntimeError('Unowned scientific result '+relative)
        return path

    def archive(relative):
        with np.load(owned_path(relative), allow_pickle=False) as saved:
            return {name:saved[name].copy() for name in saved.files}

    def save(name, value):
        path = evidence.output/(name+'.json')
        with path.open('x', encoding='utf-8') as stream:
            stream.write(json.dumps(value, indent=2, allow_nan=False)+'\n')
        evidence.own(path, 'outputs')
        return str(path.relative_to(evidence.root))

    try:
        evidence.own(evidence.root/'DERIVATION-20261001-integrated-baseline-current-contract.md')
        prior = status('annular-repaired-compatibility-attempt02')
        for short, branch in [('reference', 'reference-reference'), ('MTS', 'MTS-primary')]:
            integrated = status(args.reference_run if short=='reference' else args.MTS_run)
            evidence.check(short+':matched_integral', integrated['branch']==branch and integrated['level']=='third'
                and integrated['both_integral_rules_completed'] and integrated['force_row_held'])
            low, high = [archive(row['path']) for row in integrated['rule_outputs']]
            evidence.check(short+':matched_orders', int(low['quadrature'][0])==24 and int(high['quadrature'][0])==32)
            wave_pair = np.abs(high['accumulated'][1]-low['accumulated'][1])
            native_pair = abs(high['held_native']-low['held_native'])
            dust_pair, gravity_pair = np.zeros(4), np.zeros(4)
            dust_pair[1:] = abs(high['held_dust']-low['held_dust'])
            gravity_pair[1:] = abs(high['held_gravity']-low['held_gravity'])
            component_pairs = dict(wave=wave_pair, native=native_pair, dust=dust_pair, gravity=gravity_pair)
            addition_scale = abs(high['accumulated'][1])+abs(high['held_native'])
            addition_scale[1:] += abs(high['held_dust'])+abs(high['held_gravity'])
            floating = 256*np.finfo(float).eps*(high['sampled_absolute'][1]+addition_scale)
            old_replay = np.maximum(abs(low['old_wave_replay_difference']), abs(high['old_wave_replay_difference']))
            assembly_spread = np.maximum(abs(low['assembly_difference']), abs(high['assembly_difference']))
            correction_pair = abs(high['accumulated'][2]-low['accumulated'][2])
            diagnostic_parts = dict(**component_pairs, old_control_replay=old_replay,
                direct_assembly_spread=assembly_spread, floating_diagnostic=floating)
            component_error = sum(diagnostic_parts.values())
            extra_error = correction_pair+old_replay+assembly_spread+256*np.finfo(float).eps*high['sampled_absolute'][2]
            extra_error[0] = 0
            budget_detail = dict(branch=branch, new_baseline=high['baseline'].tolist(),
                old_baseline=high['original_baseline'].tolist(), correction=high['accumulated'][2].tolist(),
                corrected_total_pair=(high['baseline']-low['baseline']).tolist(),
                original_total_pair=(high['original_baseline']-low['original_baseline']).tolist(),
                correction_pair=correction_pair.tolist(), component_parts={key:value.tolist() for key, value in diagnostic_parts.items()},
                component_error=component_error.tolist(), extra_retained_envelope_error=extra_error.tolist(),
                component_envelope_is_rigorous=False, unknown_parent_precision_not_set_to_zero=True,
                valid_for_claim=False)
            for index, label in enumerate(['force', 'h0', 'h1', 'h2']):
                for name, values in diagnostic_parts.items():
                    component_rows.append(dict(branch=branch, row=label, component=name, value=values[index], valid_for_claim=False))
            case_paths = []
            for variant in ['rounded_coefficients', 'parent_nodal']:
                entries = [row for row in prior['summaries'] if row['branch']==branch and row['source_variant']==variant]
                inherited = {row['baseline_variant']:json.loads(owned_path(row['path']).read_text()) for row in entries}
                previous = inherited['separate_C0_baseline']
                columns, column_error = np.array(previous['columns']), np.array(previous['column_error'])
                evidence.check(short+':'+variant+':parent_baseline_replay', np.array_equal(high['original_baseline'], previous['baseline']))
                historical = inherited['historical']
                scenarios = [('historical_control', np.array(historical['baseline']), np.array(historical['baseline_error']), False),
                    ('coefficient_retained_envelope', high['baseline'], np.array(previous['baseline_error'])+extra_error, False),
                    ('coefficient_component_diagnostic', high['baseline'], component_error, True)]
                for name, baseline, baseline_error, diagnostic_only in scenarios:
                    result = diagnose(baseline, columns, baseline_error, column_error)
                    exact = envelope_search(baseline, columns, baseline_error, column_error)
                    if name=='historical_control':
                        evidence.check(short+':'+variant+':historical_decision_replay', result['rank_resolved']==historical['diagnostic']['rank_resolved']
                            and exact['any_replayed_witness']==historical['envelope_search']['any_replayed_witness'])
                    evidence.check(short+':'+variant+':'+name+':rank_not_changed_by_B', result['rank_resolved']==previous['diagnostic']['rank_resolved']
                        and result['singular_values']==previous['diagnostic']['singular_values'])
                    for candidate in result['candidates']:
                        amplitudes = np.array(candidate['amplitudes'])
                        candidate['budget_by_origin'] = dict(baseline=baseline_error.tolist(),
                            C0=(column_error[:, 0]*abs(amplitudes[0])).tolist(),
                            C1=(column_error[:, 1]*abs(amplitudes[1])).tolist(),
                            C2=(column_error[:, 2]*abs(amplitudes[2])).tolist())
                    detail = dict(branch=branch, source_variant=variant, baseline_scenario=name, baseline=baseline.tolist(),
                        baseline_error=baseline_error.tolist(), columns=columns.tolist(), column_error=column_error.tolist(),
                        diagnostic=result, envelope_search=exact, component_budget_diagnostic_only=diagnostic_only,
                        inherited_source_flags_retained=True, error_arrays_are_rigorous=False,
                        finite_history_established=False, valid_for_claim=False)
                    path = save(short+'-'+variant+'-'+name, detail)
                    case_paths.append(path)
                    representative = result['candidates'][0]
                    row = dict(branch=branch, source_variant=variant, baseline_scenario=name,
                        rank_resolved=result['rank_resolved'], representative_within=representative['within_sampled_uncertainty'],
                        representative_h2=representative['residual'][3], representative_h2_budget=representative['sampled_uncertainty'][3],
                        any_exact_sampled_envelope_witness=exact['any_replayed_witness'],
                        left_null_obstruction=result['null_obstruction']['value'], component_budget_diagnostic_only=diagnostic_only,
                        path=path, valid_for_claim=False)
                    summaries.append(row)
                    print(json.dumps(row), flush=True)
            evidence.report['cases'].append(dict(branch=branch, paths=case_paths, component_path=save(short+'-baseline-components', budget_detail)))
            evidence.save()
        for name, rows in [('summary', summaries), ('baseline-error-components', component_rows)]:
            path = evidence.output/(name+'.csv')
            with path.open('x', newline='', encoding='utf-8') as stream:
                writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
                writer.writeheader()
                writer.writerows(rows)
            with path.open(newline='', encoding='utf-8') as stream:
                parsed = list(csv.DictReader(stream, strict=True))
            evidence.check(name+':csv_valid', len(parsed)==len(rows) and all(None not in row and all(value is not None for value in row.values())
                and row['valid_for_claim']=='False' for row in parsed))
            evidence.own(path, 'outputs')
        evidence.report.update(summaries=summaries, new_baseline_integrated=True, columns_unchanged=True,
            integration_authorities=[args.reference_run, args.MTS_run],
            no_physical_parameter_refit=True, github_action=False, subagents_used=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()
