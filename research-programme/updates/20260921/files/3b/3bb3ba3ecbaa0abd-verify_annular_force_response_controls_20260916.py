from derive_annular_source_gravity_20260914 import EvidenceRun
import json


def main():
    evidence = EvidenceRun('annular-force-response-controls-attempt01',__file__)
    try:
        intake = evidence.root/'source-intake/navier-stokes/20260914'
        statuses = {}
        for name,folder in [('standard','annular-force-adjoint-response-attempt01'),('tight','annular-force-adjoint-tight-attempt01'),
            ('paths','annular-force-response-paths-attempt01')]:
            path = intake/folder/'status.json'
            evidence.own(path)
            status = json.loads(path.read_text())
            evidence.check(name+'_complete',status['state']=='complete' and all(row['passed'] for row in status['checks']))
            statuses[name] = status
        fields = ['initial_preparation_linear_response','accumulated_motion_linear_response',
            'net_reconstruction_contribution','reduced_interpolation_contribution','full_replay_residual_contribution',
            'total_measured_nonlinear_remainder','physical_linear_prediction']
        for branch in ['reference','MTS']:
            coarse = next(row for row in statuses['standard']['cases'] if row['branch']==branch and row['stride']==2)
            fine = next(row for row in statuses['standard']['cases'] if row['branch']==branch and row['stride']==1)
            tight = next(row for row in statuses['tight']['cases'] if row['branch']==branch)
            path = next(row for row in statuses['paths']['cases'] if row['branch']==branch)
            grid_changes = {field:abs(coarse[field]-fine[field]) for field in fields}
            time_changes = {field:abs(fine[field]-tight[field]) for field in fields}
            evidence.check(branch+'_path_resolution_control',max(grid_changes.values())<2e-10,grid_changes)
            evidence.check(branch+'_adjoint_time_control',max(time_changes.values())<2e-10,time_changes)
            evidence.check(branch+'_saved_force_target_unchanged',abs(tight['observed_total_force_difference']-path['endpoint_total_difference'])<2e-14)
            evidence.check(branch+'_linear_attribution_flags_recomputed',all(row['physical_linear_attribution_qualified']==
                (row['physical_linear_prediction_error']<2e-10 and abs(row['net_reconstruction_contribution'])<2e-10
                and abs(row['total_measured_nonlinear_remainder'])<2e-10) for row in [coarse,fine,tight]))
            nonlinear_agreement = max(abs(tight['initial_counterfactual_linear_difference']),abs(tight['motion_counterfactual_linear_difference']))
            evidence.check(branch+'_independent_nonlinear_counterfactual_control',nonlinear_agreement<2e-10,nonlinear_agreement)
            qualified = bool(fine['physical_linear_attribution_qualified'] and tight['physical_linear_attribution_qualified'])
            evidence.report['cases'].append(dict(branch=branch,path_refinement_changes=grid_changes,time_refinement_changes=time_changes,
                physical_attribution_qualified=qualified,nonlinear_counterfactual_maximum_difference=nonlinear_agreement,
                standard_absolute_reconstruction_sum=fine['absolute_reconstruction_contributions'],
                tight_absolute_reconstruction_sum=tight['absolute_reconstruction_contributions'],
                reconstruction_cancellation_not_hidden=True,
                uniform_nonlinear_bound=False,continuous_time_force_budget_proven=False))
        evidence.report.update(original_GR_gates_unchanged=True,short_finite_response_only=True,
            measured_remainders_not_uniform_bounds=True,no_claim_upgraded=True)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()
