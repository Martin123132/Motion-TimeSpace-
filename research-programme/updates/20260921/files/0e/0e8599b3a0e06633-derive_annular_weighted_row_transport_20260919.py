from derive_annular_source_gravity_20260914 import EvidenceRun
from run_annular_P2_continuum_bridge_20260918 import checked_load
import contextlib
import json
import numpy as np


def main():
    evidence = EvidenceRun('annular-weighted-row-transport-attempt01', __file__)
    try:
        evidence.report.update(github_action=False,subagents_used=False,no_new_evolution=True,
            full_live_P2_force_convergence_proven=False,uniform_evolving_refinement_rate_proven=False,
            actual_continuous_time_bound=False,signed_factors_before_norm=True,all_Gram_rows_retained=True)
        evidence.report['intervals'],evidence.report['work_bounds'] = [],[]
        source_folder = 'annular-moving-Gram-profile-attempt01'
        fields = ['coarse_trial','coarse_test','fine_trial','fine_test']
        for branch in ['reference','MTS']:
            samples = [checked_load(evidence,source_folder,branch+'-'+str(step).zfill(3)+'-profile.npz') for step in range(0,33,4)]
            budgets = {}
            for name in fields:
                weights_name = 'coarse_weights' if name.startswith('coarse') else 'fine_weights'
                evidence.check(branch+'_'+name+'_nonnegative_weights',all(np.all(sample[weights_name] >= 0.) for sample in samples))
                factors = [sample[name+'_factor'] for sample in samples]
                roots = [np.sqrt(sample[weights_name]) for sample in samples]
                weighted = [root*factor for root,factor in zip(roots,factors)]
                norms = [float(np.linalg.norm(value)) for value in weighted]
                initial = norms[0]
                field_budget,weight_budget,coupled_budget = 0.,0.,0.
                for interval in range(8):
                    before_root,after_root = roots[interval:interval+2]
                    before_factor,after_factor = factors[interval:interval+2]
                    field_increment = (after_root+before_root)*(after_factor-before_factor)/2
                    weight_increment = (after_root-before_root)*(after_factor+before_factor)/2
                    direct = weighted[interval+1]-weighted[interval]
                    error = float(np.max(abs(direct-field_increment-weight_increment),initial=0.))
                    scale = max(norms[interval],norms[interval+1],1e-20)
                    evidence.check(branch+'_'+name+'_'+str(interval)+'_exact_weighted_increment',error <= 1e-12*scale+1e-23,error)
                    field_size,weight_size = float(np.linalg.norm(field_increment)),float(np.linalg.norm(weight_increment))
                    field_budget += field_size
                    weight_budget += weight_size
                    coupled_budget += float(np.linalg.norm(direct))
                    evidence.report['intervals'].append(dict(branch=branch,field=name,start=interval*5e-6,stop=(interval+1)*5e-6,
                        field_increment_norm=field_size,weight_increment_norm=weight_size,
                        combined_increment_norm=float(np.linalg.norm(direct)),signed_increment_cross=float(2*field_increment @ weight_increment),
                        reconstruction_error=error,valid_for_claim=False))
                bound = initial+field_budget+weight_budget
                coupled_bound = initial+coupled_budget
                evidence.check(branch+'_'+name+'_sampled_weighted_path_bounds',max(norms) <= coupled_bound+1e-18
                    and coupled_bound <= bound+1e-18)
                row = dict(branch=branch,field=name,initial_norm=initial,final_norm=norms[-1],sampled_max=max(norms),
                    field_transport_budget=field_budget,weight_transport_budget=weight_budget,
                    separated_path_bound=bound,coupled_path_bound=coupled_bound,
                    actual_continuous_time_bound=False,valid_for_claim=False)
                evidence.report['cases'].append(row)
                budgets[name] = row
            separated = budgets['coarse_trial']['separated_path_bound']*budgets['coarse_test']['separated_path_bound']
            separated += budgets['fine_trial']['separated_path_bound']*budgets['fine_test']['separated_path_bound']
            coupled = budgets['coarse_trial']['coupled_path_bound']*budgets['coarse_test']['coupled_path_bound']
            coupled += budgets['fine_trial']['coupled_path_bound']*budgets['fine_test']['coupled_path_bound']
            works = [float(np.sum(sample['coarse_weights']*sample['coarse_trial_factor']*sample['coarse_test_factor'])
                -np.sum(sample['fine_weights']*sample['fine_trial_factor']*sample['fine_test_factor'])) for sample in samples]
            evidence.check(branch+'_all_sampled_works_bounded',max(abs(value) for value in works) <= coupled+1e-23 and coupled <= separated+1e-23)
            row = dict(branch=branch,sampled_absolute_work_max=max(abs(value) for value in works),
                separated_weighted_path_bound=separated,coupled_weighted_path_bound=coupled,
                actual_continuous_time_bound=False,valid_for_claim=False)
            evidence.report['work_bounds'].append(row)
            print(json.dumps(row),flush=True)
        with (evidence.output/'completion.txt').open('w',encoding='utf-8') as stream,contextlib.redirect_stdout(stream):
            evidence.complete()
        evidence.own(evidence.output/'completion.txt','outputs')
        evidence.save()
        print(json.dumps(dict(state='complete',checks=len(evidence.report['checks']))),flush=True)
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
