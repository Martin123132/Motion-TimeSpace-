from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_position_enabled_compatibility_20260930 import diagnose
import argparse
import csv
import ctypes
import hashlib
import json
import numpy as np


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--reference-channels',default='annular-resolved-channels-reference-third-attempt01')
    parser.add_argument('--MTS-channels',default='annular-resolved-channels-MTS-third-attempt01')
    args = parser.parse_args()
    kernel = ctypes.windll.kernel32
    kernel.GetCurrentProcess.restype = ctypes.c_void_p
    kernel.SetProcessAffinityMask.argtypes = [ctypes.c_void_p,ctypes.c_size_t]
    if not kernel.SetProcessAffinityMask(kernel.GetCurrentProcess(),4):
        raise OSError('Cannot pin one CPU')
    evidence = EvidenceRun('annular-position-enabled-third-attempt01',__file__)
    verified = {}

    def verify(relative,expected=None):
        path = (evidence.root/relative).resolve()
        if not path.is_relative_to(evidence.root) or not path.is_file():
            raise RuntimeError('Missing or out-of-scope input '+relative)
        key = str(path.relative_to(evidence.root))
        if key not in verified:
            verified[key] = hashlib.sha256(path.read_bytes()).hexdigest()
            evidence.own(path)
        if expected is not None and verified[key]!=expected:
            raise RuntimeError('Changed assembly input '+relative)
        return path

    def status(name):
        path = (evidence.output.parent/name/'status.json').resolve()
        if path.parent.parent!=evidence.output.parent:
            raise ValueError('Invalid assembly parent')
        verify(str(path.relative_to(evidence.root)))
        report = json.loads(path.read_text())
        evidence.check(name+':complete',report['state']=='complete' and all(row['passed'] for row in report['checks']))
        for category in ['inputs','outputs']:
            for relative,expected in report[category].items():
                verify(relative,expected)
        return report

    def archive(relative):
        path = (evidence.root/relative).resolve()
        key = str(path.relative_to(evidence.root))
        if key not in verified or hashlib.sha256(path.read_bytes()).hexdigest()!=verified[key]:
            raise RuntimeError('Unowned or changed archive '+relative)
        with np.load(path,allow_pickle=False) as saved:
            return {name:saved[name].copy() for name in saved.files}

    try:
        evidence.own(evidence.root/'DERIVATION-20260930-C0-force-eliminated-compatibility.md')
        evidence.own(evidence.root/'DERIVATION-20261001-resolved-acceleration-current.md')
        status('annular-position-enabled-algebra-attempt01')
        sensitivity = status('annular-reacted-column-sensitivity-attempt01')
        summaries = []
        for short,branch in [('reference','reference-reference'),('MTS','MTS-primary')]:
            parent_name = 'annular-C0-higher-'+short+'-third-attempt02'
            parent = status(parent_name)
            channel_name = args.reference_channels if short=='reference' else args.MTS_channels
            channels = status(channel_name)
            evidence.check(short+':matched_complete_columns',parent['branch']==branch and parent['level']=='third'
                and parent['complete_integral_constructed'] and parent['all_requested_pairs_passed']
                and parent['independent_force_both_orders_passed'] and parent['independent_force_pair_passed']
                and channels['branch']==branch and channels['level']=='third' and channels['C0_parent']==parent_name
                and channels['reaction_sensitivity_integrated'] and channels['resolved_C2_complete'])
            case = next(row for row in sensitivity['cases'] if row['branch']==branch and row['level']=='third')
            owned = archive(case['paths']['response'])
            evidence.check(short+':owned_shapes',owned['columns'].shape==(3,4) and owned['augmented_uncertainty'].shape==(3,4))
            rules = {row['summary']['order']:archive(row['path']) for row in parent['rule_outputs']}
            response = {row['summary']['order']:archive(row['path']) for row in channels['rule_outputs']}
            c0 = rules[32]['C0']
            reaction_low,reaction_high = [response[order]['complete'][0] for order in [24,32]]
            c0_error = abs(c0-rules[24]['C0'])+abs(reaction_high)+abs(reaction_high-reaction_low)
            c0_error[0] += max(abs(row['summary']['independent_difference']) for row in parent['rule_outputs'])
            evidence.check(short+':finite_C0_budget',np.isfinite(c0_error).all() and np.all(c0_error>=0))
            resolved = response[32]['complete'][1]
            c2_difference = resolved-owned['columns'][2]
            c2_pair = abs(resolved-response[24]['complete'][1])
            c2_replay_budget = owned['augmented_uncertainty'][2]+c2_pair
            c2_replay_budget += 64*np.finfo(float).eps*(abs(resolved)+abs(owned['columns'][2]))
            c2_replay = bool(np.all(abs(c2_difference)<=c2_replay_budget))
            conservative_c2_error = owned['augmented_uncertainty'][2]+c2_pair+abs(c2_difference)
            baseline,baseline_error = owned['columns'][0],owned['augmented_uncertainty'][0]
            fresh = rules[32]['baseline']
            fresh_pair = abs(fresh-rules[24]['baseline'])
            baseline_difference = fresh-baseline
            replay_budget = fresh_pair+baseline_error+64*np.finfo(float).eps*(abs(fresh)+abs(baseline))
            baseline_replay = bool(np.all(abs(baseline_difference)<=replay_budget))
            variants = []
            for c2_variant,c2,c2_error in [('historical_C2',owned['columns'][2],owned['augmented_uncertainty'][2]),
                    ('resolved_C2_with_retained_disagreement',resolved,conservative_c2_error)]:
                columns = np.column_stack([c0,owned['columns'][1],c2])
                column_error = np.column_stack([c0_error,owned['augmented_uncertainty'][1],c2_error])
                for baseline_variant,values,error in [('historical',baseline,baseline_error),
                        ('separate_C0_baseline',fresh,baseline_error+fresh_pair)]:
                    diagnostic = diagnose(values,columns,error,column_error)
                    diagnostic.update(baseline_variant=baseline_variant,C2_variant=c2_variant,
                        baseline_replay_passed=baseline_replay,C2_replay_passed=c2_replay,
                        inherited_flags_retained=True,spatial_convergence_established=False)
                    output = evidence.output/(short+'-'+baseline_variant+'-'+c2_variant+'.json')
                    with output.open('x',encoding='utf-8') as stream:
                        stream.write(json.dumps(diagnostic,indent=2)+'\n')
                    evidence.own(output,'outputs')
                    row = dict(branch=branch,level='third',baseline_variant=baseline_variant,C2_variant=c2_variant,
                        rank_resolved=diagnostic['rank_resolved'],singular_values=diagnostic.get('singular_values'),
                        any_candidate_within_sampled_uncertainty=diagnostic.get('any_candidate_within_sampled_uncertainty',False),
                        representative=diagnostic['candidates'][0] if diagnostic['candidates'] else None,
                        null_obstruction=diagnostic.get('null_obstruction'),baseline_replay_passed=baseline_replay,
                        C2_replay_passed=c2_replay,valid_for_claim=False)
                    variants.append(dict(summary=row,path=str(output.relative_to(evidence.root))))
                    summaries.append(row)
                    print(json.dumps(row),flush=True)
            output = evidence.output/(short+'-assembled.npz')
            np.savez_compressed(output,C0=c0,C0_error=c0_error,coarse_C0=rules[24]['C0'],
                historical_columns=owned['columns'],historical_error=owned['augmented_uncertainty'],
                resolved_C2=resolved,resolved_C2_error=conservative_c2_error,C2_difference=c2_difference,
                C2_pair=c2_pair,C2_replay_budget=c2_replay_budget,independent_baseline=fresh,
                independent_baseline_pair=fresh_pair,baseline_difference=baseline_difference,baseline_replay_budget=replay_budget)
            evidence.own(output,'outputs')
            evidence.report['cases'].append(dict(branch=branch,level='third',channel_authority=channel_name,variants=variants,path=str(output.relative_to(evidence.root)),
                C0_error=c0_error.tolist(),C2_difference=c2_difference.tolist(),C2_pair=c2_pair.tolist(),
                C2_replay_budget=c2_replay_budget.tolist(),C2_replay_passed=c2_replay,
                baseline_difference=baseline_difference.tolist(),baseline_replay_budget=replay_budget.tolist(),
                baseline_replay_passed=baseline_replay))
            evidence.save()
        table = evidence.output/'summary.csv'
        with table.open('x',newline='',encoding='utf-8') as stream:
            writer = csv.DictWriter(stream,fieldnames=list(summaries[0]))
            writer.writeheader()
            writer.writerows({key:json.dumps(value) if isinstance(value,(list,dict)) else value for key,value in row.items()} for row in summaries)
        evidence.own(table,'outputs')
        evidence.report.update(actual_third_amplitudes_evaluated=True,diagnostic_only=True,baseline_alternatives_not_averaged=True,
            C2_alternatives_not_averaged=True,inherited_flags_retained=True,uncertainty_is_rigorous_bound=False,
            spatial_convergence_established=False,finite_history_established=False,github_action=False,subagents_used=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()
