from derive_annular_source_gravity_20260914 import EvidenceRun
import json
import numpy as np


def main():
    evidence = EvidenceRun('annular-anchored-moving-precision-attempt01',__file__)
    try:
        intake = evidence.root/'source-intake/navier-stokes/20260914'
        folders = [intake/'annular-anchored-moving-smoke-attempt01',intake/'annular-anchored-moving-tight-attempt01']
        statuses = []
        for folder in folders:
            path = folder/'status.json'
            evidence.own(path)
            status = json.loads(path.read_text())
            evidence.check(folder.name+'_complete',status['state']=='complete' and all(row['passed'] for row in status['checks']))
            statuses.append(status)
        for branch in ['reference','MTS']:
            datasets,diagnostics = [],[]
            for folder in folders:
                path = folder/(branch+'-accepted-8.npz')
                evidence.own(path)
                with np.load(path) as saved:
                    datasets.append({key:saved[key].copy() for key in saved.files})
                path = folder/(branch+'-diagnostics-8.json')
                evidence.own(path)
                diagnostics.append(json.loads(path.read_text()))
            standard,tight = datasets
            evidence.check(branch+'_identical_times_and_subspace',np.array_equal(standard['times'],tight['times'])
                and np.array_equal(standard['retained_indices'],tight['retained_indices']))
            metrics = {}
            for field in ['full_force','reduced_force','force_difference','source_position_error',
                'source_velocity_error','clock_error','integrated_omitted_drive','integrated_kinetic_defect',
                'reference_coordinate_phase_error']:
                metrics[field] = max(abs(first[field]-second[field]) for first,second in zip(*diagnostics))
            evidence.check(branch+'_force_temporal_control',max(metrics[name] for name in ['full_force','reduced_force','force_difference'])<2e-9,metrics)
            evidence.check(branch+'_source_and_clock_temporal_control',metrics['source_position_error']<2e-10
                and metrics['source_velocity_error']<2e-9 and metrics['clock_error']<2e-11)
            evidence.check(branch+'_field_error_temporal_control',metrics['reference_coordinate_phase_error']<2e-8)
            for field in ['integrated_omitted_drive','integrated_kinetic_defect']:
                budget = 1e-10+1e-3*abs(diagnostics[1][-1][field])
                evidence.check(branch+'_'+field+'_temporal_control',metrics[field]<budget,dict(error=metrics[field],budget=budget))
            same_flags = [row['sampled_force_budget_met'] for row in diagnostics[0]]==[row['sampled_force_budget_met'] for row in diagnostics[1]]
            evidence.check(branch+'_sampled_force_flags_stable',same_flags)
            evidence.report['cases'].append(dict(branch=branch,maximum_differences=metrics,all_sampled_force_flags_stable=same_flags,
                comparison='Same moving chart and original finite action; 100x tighter tolerances and half the maximum step.',
                continuous_time_force_bound=False,continuum_limit=False))
        evidence.report.update(temporal_control_only=True,original_GR_gates_unchanged=True,
            no_replacement_of_GR_oracle=True,all_time_error_certificate=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()
