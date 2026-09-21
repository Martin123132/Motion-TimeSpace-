from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_locally_refined_source_action_20260916 import LocallyRefinedSourceAction
from annular_two_sided_GR_characteristics_20260915 import TwoSidedGRCharacteristics
from annular_flat_preassembled_flow_20260916 import FlatPreassembledFlow, band_product
from scipy.linalg import solve_banded
from run_annular_source_fitted_crossing_20260915 import field_comparison
import argparse
import hashlib
import json
import numpy as np


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--label',required=True)
    parser.add_argument('--runs',nargs='+',required=True)
    parser.add_argument('--control',nargs='+')
    options = parser.parse_args()
    evidence = EvidenceRun(options.label,__file__)
    try:
        intake = evidence.root/'source-intake/navier-stokes/20260914'
        failed_path = intake/'annular-joint-validation-attempt01/status.json'
        evidence.own(failed_path)
        failed = json.loads(failed_path.read_text())
        evidence.check('legacy_state_replay_failure_preserved', failed['state']=='failed' and 'old_full_action_replay' in failed['error'])
        evidence.report['legacy_state_replay_tolerance_unchanged'] = 2e-8
        oracle_folder = intake/'annular-dense-GR-references-attempt01'
        oracle_status = json.loads((oracle_folder/'status.json').read_text())
        evidence.own(oracle_folder/'status.json')
        evidence.check('dense_references_complete',oracle_status['state']=='complete' and all(row['passed'] for row in oracle_status['checks']))
        oracles,oracle_data,oracle_velocities = {},{},{}
        for degree in [384,512,768]:
            path = oracle_folder/('oracle-'+str(degree)+'.npz')
            evidence.own(path)
            with np.load(path,allow_pickle=False) as saved:
                oracle_data[degree] = {key:saved[key].copy() for key in ['times','states','forces']}
            oracles[degree] = TwoSidedGRCharacteristics(degree,mass=0.,source=.03)
            oracle_velocities[degree] = np.array([oracles[degree].unpack(state)[3] for state in oracle_data[degree]['states']])
        times = oracle_data[512]['times']
        differences = {str(degree):float(np.max(abs(oracle_data[degree]['forces']-oracle_data[768]['forces']))) for degree in [384,512]}
        evidence.report.update(arguments=vars(options),oracle_force_differences_to768=differences,
            original_action_unchanged=True,original_gates_unchanged=True,uniform_time_certificate=False,
            continuum_limit_proven=False,cross_base_Gram_actions_not_exactly_nested=True,
            force_budget=2e-7,relative_endpoint_force_budget=.02,force_time_control_budget=2e-8)
        trajectories = {}
        old_folder = intake/'annular-local-refinement-crossing-attempt02'
        evidence.own(old_folder/'status.json')
        old_status = json.loads((old_folder/'status.json').read_text())
        for label in options.runs:
            folder = intake/label
            path = folder/'status.json'
            evidence.own(path)
            status = json.loads(path.read_text())
            evidence.check(label+'_complete',status['state']=='complete' and all(row['passed'] for row in status['checks']))
            for case in status['cases']:
                branch,count,splits = case['branch'],case['count'],case['splits']
                key = (branch,count,splits)
                if key in trajectories:
                    raise ValueError('Duplicate physical case.')
                prefix = branch+str(count)+'-'+str(splits)
                path = folder/(prefix+'-trajectory.npz')
                evidence.own(path)
                evidence.check(prefix+'_sealed_trajectory',hashlib.sha256(path.read_bytes()).hexdigest()==status['outputs'][str(path.relative_to(evidence.root))])
                with np.load(path,allow_pickle=False) as saved:
                    data = {name:saved[name].copy() for name in ['times','states','forces','energies']}
                evidence.check(prefix+'_same_full_horizon_times',np.array_equal(data['times'],times) and len(times)==81 and times[-1]==.4)
                trajectories[key] = data
                system = LocallyRefinedSourceAction(count,branch=='MTS',background_mass=0.,source_splits=splits)
                matrices = FlatPreassembledFlow(system).matrices(system.anchor)
                trace_stiffness = float(system.lifted_hinge @ (matrices['gram']*system.lifted_hinge))
                forces = data['forces']
                all_errors = {str(degree):abs(forces-oracle_data[degree]['forces']) for degree in oracles}
                final_flags,sampled_flags,nine_flags,source_flags = {},{},{},{}
                source_errors = {}
                for degree in oracles:
                    error = all_errors[str(degree)]
                    final_flags[str(degree)] = bool(error[-1]<2e-7 and error[-1]/abs(oracle_data[degree]['forces'][-1])<.02)
                    sampled_flags[str(degree)] = bool(np.max(error)<2e-7)
                    nine_flags[str(degree)] = bool(np.max(error[::10])<2e-7)
                    source = float(np.max(abs(data['states'][:,system.count]-oracle_data[degree]['states'][:,-3])))
                    velocity = float(np.max(abs(data['states'][:,-2]-oracle_velocities[degree])))
                    clock = float(np.max(abs(data['states'][:,-1]-oracle_data[degree]['states'][:,-1])))
                    source_errors[str(degree)] = dict(source=source,velocity=velocity,clock=clock)
                    source_flags[str(degree)] = bool(source<5e-7 and velocity<2e-5 and clock<2e-7)
                field_errors = [field_comparison(system,state,oracles[768],exact,order=16)
                    for state,exact in zip(data['states'],oracle_data[768]['states'])]
                field_errors24 = [field_comparison(system,state,oracles[768],exact,order=24)
                    for state,exact in zip(data['states'][::10],oracle_data[768]['states'][::10])]
                quadrature_error = float(np.max(abs(np.array(field_errors24)-np.array(field_errors)[::10])))
                evidence.check(prefix+'_field_quadrature',quadrature_error<2e-8,quadrature_error)
                signed = forces-oracle_data[768]['forces']
                row = dict(branch=branch,count=count,splits=splits,scalar_dofs=system.count,
                    bulk_spacing=case['bulk_spacing'],local_widths=case['local_widths'],
                    trace_stiffness=trace_stiffness,trace_stiffness_over_bulk_spacing=trace_stiffness/case['bulk_spacing'],
                    source_widths_over_bulk_spacing=(np.array(case['local_widths'])/case['bulk_spacing']).tolist(),
                    final_force_errors={degree:float(error[-1]) for degree,error in all_errors.items()},
                    maximum_force_errors={degree:float(np.max(error)) for degree,error in all_errors.items()},
                    nine_time_force_errors={degree:float(np.max(error[::10])) for degree,error in all_errors.items()},
                    rms_force_error768=float(np.sqrt(np.mean(signed**2))),peak_error_time768=float(times[np.argmax(abs(signed))]),
                    final_flags=final_flags,sampled81_flags=sampled_flags,sampled9_flags=nine_flags,
                    final_pass_all_references=all(final_flags.values()),sampled_pass_all_references=all(sampled_flags.values()),
                    reference_dependent_classification=len(set(final_flags.values()))>1 or len(set(sampled_flags.values()))>1,
                    source_errors=source_errors,source_clock_flags=source_flags,
                    field_errors768=field_errors,maximum_field_error768=max(field_errors),field_gate768=bool(max(field_errors)<.005),
                    original_energy_relative_drift=case['energy_relative_drift'],seconds=case['seconds'])
                old = next((value for value in old_status['cases'] if value['branch']==branch
                    and value['base_count']==count and value['source_splits']==splits),None)
                if old is not None:
                    old_path = old_folder/(branch+'-'+str(count)+'.npz')
                    evidence.own(old_path)
                    with np.load(old_path,allow_pickle=False) as saved:
                        old_states = saved['states'].copy()
                    state_replay = float(np.max(abs(data['states'][::10]-old_states)))
                    force_replay = float(np.max(abs(forces[::10]-np.array(old['forces']))))
                    evidence.check(prefix+'_old_force_replay',force_replay<2e-8,force_replay)
                    difference = abs(data['states'][::10]-old_states)
                    row.update(legacy_state_replay_pass=bool(state_replay<2e-8),
                        legacy_state_replay_tolerance=2e-8,
                        legacy_state_component_errors=dict(field=float(np.max(difference[:,:system.count])),
                            source=float(np.max(difference[:,system.count])),field_rate=float(np.max(difference[:,system.count+1:-2])),
                            source_rate=float(np.max(difference[:,-2])),clock=float(np.max(difference[:,-1]))))
                    row.update(old_state_replay_error=state_replay,old_force_replay_error=force_replay)
                path = evidence.output/(prefix+'-force-comparison.npz')
                np.savez_compressed(path,times=times,predicted_forces=forces,
                    **{'oracle'+str(degree):oracle_data[degree]['forces'] for degree in oracles})
                evidence.own(path,'outputs')
                evidence.report['cases'].append(row)
                evidence.save()
                print(dict(branch=branch,count=count,splits=splits,final768=row['final_force_errors']['768'],
                    maximum768=row['maximum_force_errors']['768'],all81=row['sampled_pass_all_references']),flush=True)
        rectangles = []
        for branch in ['reference','MTS']:
            forces = {(count,splits):trajectories[(branch,count,splits)]['forces'] for count in [257,513] for splits in [4,8]}
            interaction = (forces[(513,8)]-forces[(513,4)])-(forces[(257,8)]-forces[(257,4)])
            rectangles.append(dict(branch=branch,maximum_source_split_effect257=float(np.max(abs(forces[(257,8)]-forces[(257,4)]))),
                maximum_source_split_effect513=float(np.max(abs(forces[(513,8)]-forces[(513,4)]))),
                maximum_bulk_effect4=float(np.max(abs(forces[(513,4)]-forces[(257,4)]))),
                maximum_bulk_effect8=float(np.max(abs(forces[(513,8)]-forces[(257,8)]))),
                maximum_interaction=float(np.max(abs(interaction))),endpoint_interaction=float(interaction[-1])))
        evidence.report['refinement_rectangle'] = rectangles
        evidence.report['Gram_response'] = []
        grids = sorted({(count,splits) for branch,count,splits in trajectories})
        for count,splits in grids:
            reference = trajectories[('reference',count,splits)]
            modified = trajectories[('MTS',count,splits)]
            reference_model = FlatPreassembledFlow(LocallyRefinedSourceAction(count,False,background_mass=0.,source_splits=splits))
            modified_model = FlatPreassembledFlow(LocallyRefinedSourceAction(count,True,background_mass=0.,source_splits=splits))
            direct,feedback,derived,gram_energy = [],[],[],[]
            for state,modified_force,reference_force in zip(modified['states'],modified['forces'],reference['forces']):
                shared = reference_model.evaluate(state)
                coordinates,rates = np.split(state[:-1],2)
                field,position,speed = coordinates[:-1],coordinates[-1],rates[-1]
                matrices = modified_model.matrices(position)
                factor = modified_model.lifted @ field
                gram_covector = modified_model.lifted_transpose @ (matrices['gram']*factor)
                cross = band_product(matrices['transport'],field)
                material = modified_model.system.source_mass/(1-speed**2)**1.5
                predicted = material/shared['schur']*(-factor @ (matrices['gram_b']*factor)/2
                    +cross @ solve_banded((2,2),matrices['mass'],gram_covector,check_finite=False))
                direct.append(float(modified_force-shared['force']))
                feedback.append(float(shared['force']-reference_force))
                derived.append(float(predicted))
                gram_energy.append(float(factor @ (matrices['gram']*factor)/2))
            direct,feedback,derived,gram_energy = map(np.array,[direct,feedback,derived,gram_energy])
            error = float(np.max(abs(direct-derived)))
            evidence.check(str(count)+'-'+str(splits)+'_derived_Gram_source_force',error<2e-11,error)
            total = modified['forces']-reference['forces']
            closure = float(np.max(abs(total-direct-feedback)))
            evidence.check(str(count)+'-'+str(splits)+'_exact_trajectory_split',closure<2e-14,closure)
            destination = evidence.output/('Gram-response-'+str(count)+'-'+str(splits)+'.npz')
            np.savez_compressed(destination,times=times,direct=direct,feedback=feedback,total=total,
                derived_direct=derived,gram_energy=gram_energy)
            evidence.own(destination,'outputs')
            evidence.report['Gram_response'].append(dict(count=count,splits=splits,
                maximum_direct=float(np.max(abs(direct))),maximum_feedback=float(np.max(abs(feedback))),
                maximum_total=float(np.max(abs(total))),endpoint_direct=float(direct[-1]),
                endpoint_feedback=float(feedback[-1]),endpoint_total=float(total[-1]),
                maximum_Gram_energy=float(np.max(gram_energy)),derived_force_identity_error=error,
                order_dependent_decomposition=True,not_a_force_correction=True))
        for control_label in options.control or []:
            folder = intake/control_label
            status = json.loads((folder/'status.json').read_text())
            evidence.own(folder/'status.json')
            evidence.check(control_label+'_full_duration_tighter_runs_complete',status['state']=='complete'
                and status['configuration']['rtol']==2e-12 and status['configuration']['spectral_step_multiplier']==.5)
            for case in status['cases']:
                branch,count,splits = case['branch'],case['count'],case['splits']
                path = folder/(branch+str(count)+'-'+str(splits)+'-trajectory.npz')
                evidence.own(path)
                with np.load(path,allow_pickle=False) as saved:
                    state_change = float(np.max(abs(saved['states']-trajectories[(branch,count,splits)]['states'])))
                    force_change = float(np.max(abs(saved['forces']-trajectories[(branch,count,splits)]['forces'])))
                evidence.check(branch+str(count)+'-'+str(splits)+'_full_duration_temporal_control',state_change<2e-8 and force_change<2e-8,
                    dict(state=state_change,force=force_change))
                evidence.report.setdefault('time_controls',[]).append(dict(branch=branch,count=count,splits=splits,
                    full_duration=.4,state_change=state_change,force_change=force_change))
        controlled = {(row['branch'],row['count'],row['splits']) for row in evidence.report.get('time_controls',[])}
        evidence.report['observed_orders'] = []
        for branch in ['reference','MTS']:
            selected = sorted([row for row in evidence.report['cases'] if row['branch']==branch and row['splits']==8],
                key=lambda row:row['count'])
            for coarse,fine in zip(selected[:-1],selected[1:]):
                error_ratio = coarse['maximum_force_errors']['768']/fine['maximum_force_errors']['768']
                spacing_ratio = coarse['bulk_spacing']/fine['bulk_spacing']
                evidence.report['observed_orders'].append(dict(branch=branch,coarse=coarse['count'],fine=fine['count'],
                    error_ratio=error_ratio,observed_order=float(np.log(error_ratio)/np.log(spacing_ratio)),
                    asymptotic_order_proven=False,source_cell_fraction_changes=True))
        for row in evidence.report['cases']:
            row['full_duration_tighter_time_control_available'] = (row['branch'],row['count'],row['splits']) in controlled
            row['time_controlled_all_sampled_gates_pass'] = bool(row['full_duration_tighter_time_control_available']
                and row['sampled_pass_all_references'] and row['field_gate768'] and all(row['source_clock_flags'].values()))
        evidence.report.update(all_tested_cases_pass=all(row['sampled_pass_all_references'] and row['field_gate768']
            and all(row['source_clock_flags'].values()) for row in evidence.report['cases']),
            actual_physics_pass_not_required_for_successful_implementation=True)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()
