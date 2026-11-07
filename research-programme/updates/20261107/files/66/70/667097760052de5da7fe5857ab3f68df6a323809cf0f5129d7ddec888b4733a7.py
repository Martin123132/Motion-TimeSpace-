from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_position_enabled_compatibility_20260930 import diagnose
from pathlib import Path
import csv
import ctypes
import hashlib
import json
import numpy as np


def main():
    kernel = ctypes.windll.kernel32
    kernel.GetCurrentProcess.restype = ctypes.c_void_p
    kernel.SetProcessAffinityMask.argtypes = [ctypes.c_void_p,ctypes.c_size_t]
    if not kernel.SetProcessAffinityMask(kernel.GetCurrentProcess(),4):
        raise OSError('Cannot pin one CPU')
    evidence = EvidenceRun('annular-position-enabled-fine-attempt02',__file__)
    try:
        evidence.own(evidence.root/'DERIVATION-20260930-C0-force-eliminated-compatibility.md')
        verified = {}

        def verify(relative,expected=None):
            path = (evidence.root/relative).resolve()
            if path == evidence.root/'CURRENT_LOCAL_RESUME.md':
                return
            if not path.is_relative_to(evidence.root) or not path.is_file():
                raise RuntimeError('Missing or out-of-scope assembly input '+relative)
            key = str(path.relative_to(evidence.root))
            if key not in verified:
                verified[key] = hashlib.sha256(path.read_bytes()).hexdigest()
                evidence.own(path)
            if expected is not None and verified[key]!=expected:
                raise RuntimeError('Changed assembly input '+relative)
            return path

        def status(name):
            path = evidence.output.parent/name/'status.json'
            verify(str(path.relative_to(evidence.root)))
            report = json.loads(path.read_text())
            saved_reference = name=='annular-C0-integral-reference-attempt01' and report.get('external_safe_boundary_stop',False)
            saved_reference = saved_reference and report.get('numerical_failure') is False and any(
                row['summary']['level']=='fine' and row['summary'].get('complete_integral_constructed',False)
                for row in report.get('cases',[]))
            evidence.check(name+':complete_or_saved_fine', (report['state']=='complete' or saved_reference)
                and all(row['passed'] for row in report['checks']))
            if saved_reference:
                evidence.report['saved_reference_baseline_reused_old_Eulerian_failure_retained'] = True
            for category in ['inputs','outputs']:
                for relative,expected in report[category].items():
                    verify(relative,expected)
            return report

        def archive(relative):
            path = (evidence.root/relative).resolve()
            if not path.is_relative_to(evidence.root) or str(path.relative_to(evidence.root)) not in verified:
                raise RuntimeError('Unverified archive')
            if hashlib.sha256(path.read_bytes()).hexdigest()!=verified[str(path.relative_to(evidence.root))]:
                raise RuntimeError('Changed archive '+relative)
            with np.load(path,allow_pickle=False) as saved:
                return {name:saved[name].copy() for name in saved.files}

        status('annular-position-enabled-algebra-attempt01')
        sensitivity = status('annular-reacted-column-sensitivity-attempt01')
        summaries = []
        for short,branch in [('reference','reference-reference'),('MTS','MTS-primary')]:
            stable = status('annular-C0-stable-'+short+'-fine-attempt01')
            force = status('annular-C0-force-product-'+short+'-fine-attempt01')
            reaction = status('annular-C0-sensitivity-'+short+'-fine-attempt'+('01' if short=='reference' else '02'))
            historical = status('annular-C0-integral-reference-attempt01' if short=='reference'
                else 'annular-C0-integral-MTS-native-recovery-attempt02')
            evidence.check(short+':matched_C0',stable['branch']==branch and stable['level']=='fine' and stable['material_pair_passed'])
            case = next(row for row in sensitivity['cases'] if row['branch']==branch and row['level']=='fine')
            owned = archive(case['paths']['response'])
            evidence.check(short+':owned_shapes',owned['columns'].shape==(3,4) and owned['augmented_uncertainty'].shape==(3,4))
            rules = {row['summary']['order']:archive(row['path']) for row in stable['rule_outputs']}
            c0 = rules[32]['material_C0']
            c0_error = abs(c0-rules[24]['material_C0'])
            c0_error[1:] += np.maximum(abs(rules[24]['cross_difference'][1:]),abs(rules[32]['cross_difference'][1:]))
            c0_error[0] += max(abs(row['summary']['independent_difference']) for row in force['rule_outputs'])
            reaction_values = [np.array(row['summary']['reaction_C0']) for row in reaction['rule_outputs']]
            c0_error += abs(reaction_values[-1])+abs(reaction_values[-1]-reaction_values[0])
            columns = np.column_stack([c0,owned['columns'][1],owned['columns'][2]])
            column_error = np.column_stack([c0_error,owned['augmented_uncertainty'][1],owned['augmented_uncertainty'][2]])
            baseline,baseline_error = owned['columns'][0],owned['augmented_uncertainty'][0]
            prior_case = next(row for row in historical['cases'] if row['summary']['level']=='fine')
            independently_integrated = archive(prior_case['paths']['combined'])
            fresh_baseline = independently_integrated['baseline_fine']
            fresh_pair = abs(fresh_baseline-independently_integrated['baseline_coarse'])
            baseline_difference = fresh_baseline-baseline
            replay_budget = fresh_pair+baseline_error+64*np.finfo(float).eps*(abs(fresh_baseline)+abs(baseline))
            baseline_replay_passed = bool(np.all(abs(baseline_difference)<=replay_budget))
            variants = []
            for variant,values,error in [('historical',baseline,baseline_error),('separate_C0_baseline',fresh_baseline,fresh_pair)]:
                diagnostic = diagnose(values,columns,error,column_error)
                diagnostics_path = evidence.output/(short+'-'+variant+'-diagnostic.json')
                diagnostics_path.write_text(json.dumps(diagnostic,indent=2)+'\n',encoding='utf-8')
                evidence.own(diagnostics_path,'outputs')
                row = dict(branch=branch,level='fine',baseline_variant=variant,rank_resolved=diagnostic['rank_resolved'],
                    singular_values=diagnostic['singular_values'],
                    any_candidate_within_sampled_uncertainty=diagnostic['any_candidate_within_sampled_uncertainty'],
                    column_scaled_amplitudes=diagnostic['candidates'][0]['amplitudes'],
                    column_scaled_residual=diagnostic['candidates'][0]['residual'],
                    column_scaled_budget=diagnostic['candidates'][0]['sampled_uncertainty'],
                    null_obstruction=diagnostic['null_obstruction'],baseline_replay_passed=baseline_replay_passed,
                    baseline_difference=baseline_difference.tolist(),higher_grid_tested=False,
                    finite_history_established=False,valid_for_claim=False)
                variants.append(dict(summary=row,path=str(diagnostics_path.relative_to(evidence.root))))
                summaries.append(row)
                print(json.dumps(row),flush=True)
            arrays = evidence.output/(short+'-assembled.npz')
            np.savez_compressed(arrays,baseline=baseline,columns=columns,baseline_error=baseline_error,
                column_error=column_error,coarse_C0=rules[24]['material_C0'],
                independently_integrated_baseline=fresh_baseline,baseline_replay_budget=replay_budget,
                independent_baseline_pair=fresh_pair,baseline_difference=baseline_difference)
            evidence.own(arrays,'outputs')
            evidence.report['cases'].append(dict(branch=branch,level='fine',variants=variants,
                path=str(arrays.relative_to(evidence.root))))
            evidence.save()
        table = evidence.output/'summary.csv'
        with table.open('x',newline='',encoding='utf-8') as stream:
            writer = csv.DictWriter(stream,fieldnames=list(summaries[0]))
            writer.writeheader()
            for row in summaries:
                writer.writerow({key:json.dumps(value) if isinstance(value,(list,dict)) else value for key,value in row.items()})
        evidence.own(table,'outputs')
        evidence.report.update(actual_fine_amplitudes_evaluated=True,higher_grid_amplitudes_evaluated=False,
            diagnostic_only=True,baseline_alternatives_not_averaged=True,inherited_flags_retained=True,
            uncertainty_is_rigorous_bound=False,github_action=False,subagents_used=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()


