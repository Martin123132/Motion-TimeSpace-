from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_acceleration_archive_checks_v2_20261001 import verify_report,validate_result,compare_orders
import ctypes
import csv
import json
import numpy as np


def main():
    kernel = ctypes.windll.kernel32
    kernel.GetCurrentProcess.restype = ctypes.c_void_p
    kernel.SetProcessAffinityMask.argtypes = [ctypes.c_void_p,ctypes.c_size_t]
    if not kernel.SetProcessAffinityMask(kernel.GetCurrentProcess(),1<<2):
        raise OSError('Affinity failed')
    evidence = EvidenceRun('annular-native-null-acceleration-comparison-attempt02',__file__)
    try:
        root = 'source-intake/navier-stokes/20260914/'
        failed_path = evidence.root/root/'annular-native-null-acceleration-comparison-attempt01/status.json'
        failed_analysis = json.loads(failed_path.read_text())
        evidence.own(failed_path)
        for category in ['inputs','outputs']:
            for name in failed_analysis[category]:
                evidence.own(evidence.root/name)
        evidence.check('recognized_subtractive_metadata_roundoff_failure',failed_analysis['state']=='failed'
            and 'fine:summary_quadrature_gate_maximum_difference' in failed_analysis['error'])
        original = verify_report(evidence,root+'annular-native-null-acceleration-summary-recovery-attempt02/status.json')
        builder = verify_report(evidence,root+'annular-Neumann-kernel-family-attempt01/status.json')
        evidence.check('recovery_and_builder_complete',original['state']==builder['state']=='complete')
        original_cases = {row['level']:row for row in original['cases']}
        builder_cases = {row['level']:row for row in builder['cases']}
        failed = verify_report(evidence,root+'annular-Neumann-null-acceleration-fine-attempt01/status.json')
        evidence.check('failed_attempt_was_only_missing_self_report_hash',failed['state']=='failed'
            and 'Unowned source' in failed['error'] and not failed.get('results'))
        rows,profiles,controls,corner_profiles = [],{},{},{}
        for level in ['fine','third']:
            corner_profile = verify_report(evidence,root+'annular-Neumann-source-corner-profile-'+level+'-attempt01/status.json')
            evidence.check(level+':corner_profile_complete',corner_profile['state']=='complete')
            corner_profiles[level] = corner_profile
            report = verify_report(evidence,root+'annular-Neumann-null-acceleration-'+level+'-attempt02/status.json')
            evidence.check(level+':new_acceleration_complete',report['state']=='complete'
                and report['natural_flux_compatible_initial_profile'] and report['full_coupled_zero_rate_reduction']
                and not report['physical_trajectory_computed'])
            replayed = [validate_result(evidence,result,level+':Neumann:'+str(result['material'])) for result in report['results']]
            for result,validated in zip(report['results'],replayed):
                validated['independently_resummed_gate'] = validated['gate'].copy()
                validated['gate'] = np.asarray(result['full_gate'],dtype=float)
            order_comparison = compare_orders(*replayed)
            for key,value in order_comparison.items():
                evidence.check(level+':summary_'+key,abs(report[key]-value)<2e-13*max(abs(value),1e-30))
            profiles[level] = replayed[-1]
            old = original_cases[level]
            for family,results,comparison in [('original',old['results'],old),('Neumann',report['results'],order_comparison)]:
                for result in results:
                    rows.append(dict(family=family,grid=level,spatial=result['spatial'],material=result['material'],
                        maximum_acceleration=result['maximum_acceleration'],maximum_source_acceleration=result['maximum_source_acceleration'],
                        maximum_endpoint_acceleration=result['maximum_edge_acceleration'],
                        maximum_bulk_acceleration=result['maximum_bulk_acceleration'],
                        maximum_native_gate=float(np.max(np.abs(result['full_gate']))),
                        first_native_gate=result['full_gate'][0],gate_order_difference=comparison['quadrature_gate_maximum_difference'],
                        gate_order_relative_difference=comparison['quadrature_gate_relative_difference'],
                        source_units='inherited_code_normalized',valid_for_claim=False))
            high = report['results'][-1]
            old_high = old['results'][-1]
            corners = builder_cases[level]['source_corner']
            source_lower,source_upper = min(profiles[level]['source_acceleration']),max(profiles[level]['source_acceleration'])
            corner_disjoint = all(source_lower>row['required_left'] and source_upper<row['required_right'] for row in corners)
            evidence.check(level+':computed_source_between_incompatible_trace_requirements',corner_disjoint,
                dict(source_range=[source_lower,source_upper],required_left=[row['required_left'] for row in corners],
                    required_right=[row['required_right'] for row in corners]))
            evidence.check(level+':numerical_drift_does_not_supply_required_jump',
                all(abs(row['observed_drift_spreads'][-1]['drift_jump'])<1e-5*row['acceleration_gap'] for row in corners))
            evidence.check(level+':natural_endpoint_repair_resolved',high['maximum_edge_acceleration']<1e-10)
            gate_norm = float(np.max(np.abs(high['full_gate'])))
            evidence.check(level+':nonzero_gate_above_quadrature_spread',gate_norm>1000*order_comparison['quadrature_gate_maximum_difference'])
            controls[level] = dict(old_maximum_acceleration=old_high['maximum_acceleration'],
                new_maximum_acceleration=high['maximum_acceleration'],
                acceleration_reduction=old_high['maximum_acceleration']/high['maximum_acceleration'],
                old_gate_maximum=float(np.max(np.abs(old_high['full_gate']))),new_gate_maximum=gate_norm,
                new_endpoint_driven_maximum=high['maximum_edge_acceleration'],
                source_range=[source_lower,source_upper],corner_rows=corners,
                central_profile=dict(source_acceleration=corner_profile['source_acceleration'],
                    source_trace_limits=corner_profile['source_trace_limits'],interior_bands=corner_profile['interior_bands'],
                    nearest_source_nodes=corner_profile['nearest_source_nodes']),**order_comparison)
        fine_gate,third_gate = profiles['fine']['gate'],profiles['third']['gate']
        spatial = dict(gate_maximum_ratio=float(np.max(np.abs(third_gate))/np.max(np.abs(fine_gate))),
            gate_difference_maximum=float(np.max(np.abs(third_gate-fine_gate))),
            source_acceleration_difference=float(np.max(np.abs(profiles['third']['source_acceleration']-profiles['fine']['source_acceleration']))),
            two_grids_are_not_convergence_proof=True)
        spatial['source_layer_comparison'] = {}
        for side in ['left','right']:
            coarse = corner_profiles['fine']['nearest_source_nodes'][side][0]
            refined = corner_profiles['third']['nearest_source_nodes'][side][0]
            spatial['source_layer_comparison'][side] = dict(nearest_distance_ratio=refined['distance']/coarse['distance'],
                nearest_error_ratio=refined['error']/coarse['error'])
        path = evidence.output/'coupled-null-acceleration-comparison.csv'
        with path.open('x',encoding='utf-8',newline='') as stream:
            writer = csv.DictWriter(stream,fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
        evidence.own(path,'outputs')
        evidence.report.update(comparison=controls,spatial_refinement=spatial,summary_rows=rows,
            physical_source_acceleration_computed=True,natural_endpoint_initial_data_repaired=True,
            source_corner_condition_satisfied=False,native_quartic_gates_satisfied=False,
            metadata_replayed_from_stored_sums_after_independent_tensor_sum_validation=True,
            matched_reference_shares_source_corner_incompatibility=True,
            reference_zero_Gram_gate_is_structural_not_empirical=True,
            no_global_theory_exclusion=True,action_changed=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()
