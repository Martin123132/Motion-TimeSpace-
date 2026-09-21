from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_locally_refined_source_action_20260916 import LocallyRefinedSourceAction
from annular_two_sided_GR_characteristics_20260915 import TwoSidedGRCharacteristics
from verify_annular_quadratic_crossing_precision_20260915_v2 import shape_force
from run_annular_source_fitted_crossing_20260915 import initial,field_comparison
import json
import numpy as np


def main():
    evidence = EvidenceRun('annular-local-crossing-precision-attempt01',__file__)
    try:
        intake = evidence.root/'source-intake/navier-stokes/20260914'
        folder = intake/'annular-local-refinement-crossing-attempt02'
        source_status = json.loads((folder/'status.json').read_text())
        evidence.check('paired_crossing_complete',source_status['state']=='complete' and all(row['passed'] for row in source_status['checks']))
        evidence.own(folder/'status.json')
        oracle_folder = intake/'annular-source-fitted-fine-crossing-attempt01'
        extra = intake/'annular-crossing-oracle768-attempt01'
        status = json.loads((extra/'status.json').read_text())
        evidence.check('additional_reference_qualified',status['state']=='complete' and all(row['passed'] for row in status['checks']))
        evidence.own(extra/'status.json')
        control_folder = intake/'annular-local-tight-controls-attempt01'
        control_status = json.loads((control_folder/'status.json').read_text())
        evidence.check('tight_integrations_complete',control_status['state']=='complete' and all(row['passed'] for row in control_status['checks']))
        evidence.own(control_folder/'status.json')
        oracles,oracle_states,oracle_forces = {},{},{}
        for degree in [384,512,768]:
            path = (extra if degree==768 else oracle_folder)/('oracle-'+str(degree)+'.npz')
            evidence.own(path)
            saved = np.load(path)
            times = saved['times']
            model = TwoSidedGRCharacteristics(degree,mass=0.)
            values = [model.unpack(state) for state in saved['states']]
            oracles[degree],oracle_states[degree] = model,saved['states']
            oracle_forces[degree] = np.array([model.source_force(value[0],value[1],value[3]) for value in values])
        for original in source_status['cases']:
            count,splits,branch = original['base_count'],original['source_splits'],original['branch']
            system = LocallyRefinedSourceAction(count,branch=='MTS',background_mass=0.,source_splits=splits)
            path = folder/(branch+'-'+str(count)+'.npz')
            evidence.own(path)
            states = np.load(path)['states']
            decompositions = [shape_force(system,instant,*np.split(state[:-1],2)) for instant,state in zip(times,states)]
            force = np.array([row['canonical_force'] for row in decompositions])
            row = dict(branch=branch,count=count,source_splits=splits,scalar_dofs=system.count,
                original_final_force_gate=original['strict_force_gate'],original_sampled_force_gate=original['stricter_nine_time_absolute_force_gate'],
                full_force_decompositions=decompositions)
            prefix = branch+str(count)
            difference = float(max(abs(value['derived_force']-value['canonical_force']) for value in decompositions))
            evidence.check(prefix+'_independent_shape_force_identity',difference < 2e-11,difference)
            difference = float(max(abs(force-np.array(original['forces']))))
            evidence.check(prefix+'_recorded_and_canonical_force_agree',difference < 2e-11,difference)
            errors24 = [field_comparison(system,state,oracles[512],exact,order=24) for state,exact in zip(states,oracle_states[512])]
            difference = float(max(abs(np.array(errors24)-original['field_errors'])))
            evidence.check(prefix+'_field_quadrature16_24',difference < 2e-8,difference)
            force_errors = {str(degree):abs(force-values).tolist() for degree,values in oracle_forces.items()}
            final_flags = {str(degree):bool(abs(force[-1]-values[-1]) < 2e-7 and abs(force[-1]-values[-1])/abs(values[-1]) < .02) for degree,values in oracle_forces.items()}
            sampled_flags = {str(degree):bool(max(abs(force-values)) < 2e-7) for degree,values in oracle_forces.items()}
            evidence.check(prefix+'_old_accuracy_flags_preserved',final_flags['512']==original['strict_force_gate']
                and sampled_flags['512']==original['stricter_nine_time_absolute_force_gate']
                and (max(errors24)<.005)==original['strict_waveform_gate'])
            row.update(field_errors24=errors24,maximum_field_error24=max(errors24),force_errors=force_errors,
                reference_final_forces={str(degree):float(values[-1]) for degree,values in oracle_forces.items()},
                quadrature16_24_maximum_difference=difference,
                final_force_flags_by_reference=final_flags,sampled_force_flags_by_reference=sampled_flags,
                final_force_passes_all_three_references=all(final_flags.values()),sampled_force_passes_all_three_references=all(sampled_flags.values()))
            if count==513:
                control_path = control_folder/(branch+'-513-tight-first-twentieth.npz')
                evidence.own(control_path)
                saved_control = np.load(control_path)
                control_times,control = saved_control['times'],saved_control['states']
                control_metadata = next(item for item in control_status['cases'] if item['branch']==branch)
                evidence.check(prefix+'_tighter_control_snapshot_consistent',np.array_equal(control_times,times[:2])
                    and control_metadata['count']==513 and control_metadata['source_splits']==splits
                    and control_metadata['rtol']==2e-12 and control_metadata['atol']==2e-14)
                difference = float(np.max(abs(control-states[:2])))
                evidence.check(prefix+'_tighter_temporal_state_agreement',difference < 2e-8,difference)
                forces = np.array([shape_force(system,instant,*np.split(state[:-1],2))['canonical_force'] for instant,state in zip(control_times,control)])
                force_difference = float(max(abs(forces-force[:2])))
                evidence.check(prefix+'_tighter_temporal_force_agreement',force_difference < 2e-8,force_difference)
                row.update(temporal_control_duration=.05,temporal_control_rtol=2e-12,temporal_control_atol=2e-14,
                    temporal_control_maximum_step=control_metadata['maximum_step'],temporal_control_state_difference=difference,
                    temporal_control_force_difference=force_difference,temporal_control_seconds=control_metadata['seconds'],
                    temporal_control_rhs_evaluations=control_metadata['rhs_evaluations'],temporal_control_not_full_duration=True)
            evidence.report['cases'].append(row)
            evidence.save()
            print(json.dumps(dict(branch=branch,count=count,final_pass=all(final_flags.values()),sampled_pass=all(sampled_flags.values()))),flush=True)
        evidence.report.update(scope='Independent local-refinement force/field/reference checks with tighter first-eighth temporal controls; nine samples are not a uniform-time proof.',
            all_original_Gram_terms_and_source_momentum_retained=True,live_quadratic_geometry_qualified=False,
            uniform_all_time_force_bound_proven=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
