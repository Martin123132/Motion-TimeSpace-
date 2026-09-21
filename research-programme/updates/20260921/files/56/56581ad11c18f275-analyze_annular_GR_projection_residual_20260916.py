from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_flat_preassembled_flow_20260916 import FlatPreassembledFlow, band_product
from annular_locally_refined_source_action_20260916 import LocallyRefinedSourceAction
from scipy.linalg import solve_banded
import argparse
import hashlib
import json
import numpy as np


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--label',required=True)
    options = parser.parse_args()
    evidence = EvidenceRun(options.label,__file__)
    try:
        intake = evidence.root/'source-intake/navier-stokes/20260914'
        projection_folder = intake/'annular-GR-projection-residual-attempt02'
        path = projection_folder/'status.json'
        evidence.own(path)
        projected_status = json.loads(path.read_text())
        evidence.check('GR_only_projection_saved_before_comparison',projected_status['state']=='complete'
            and not projected_status['finite_future_trajectories_read'] and all(row['passed'] for row in projected_status['checks']))
        evidence.report.update(retrospective_attribution_not_prediction=True,force_correction=False,
            trajectory_errors_not_independently_predicted=True,original_action_unchanged=True,
            full_time_force_budget=2e-7,oracle_resolution_not_rigorous_bound=True)
        cases = {}
        for label in ['annular-joint-rectangle-attempt01','annular-joint-finer1025-attempt01']:
            folder = intake/label
            path = folder/'status.json'
            evidence.own(path)
            status = json.loads(path.read_text())
            evidence.check(label+'_complete',status['state']=='complete' and all(row['passed'] for row in status['checks']))
            for row in status['cases']:
                if row['splits']!=8:
                    continue
                prefix = row['branch']+str(row['count'])+'-8'
                path = folder/(prefix+'-trajectory.npz')
                evidence.own(path)
                evidence.check(prefix+'_sealed_trajectory',hashlib.sha256(path.read_bytes()).hexdigest()==status['outputs'][str(path.relative_to(evidence.root))])
                with np.load(path,allow_pickle=False) as saved:
                    cases[(row['branch'],row['count'])] = {name:saved[name].copy() for name in ['times','states','forces']}
        for count in [257,513,1025]:
            projections = {}
            for degree in [384,512,768]:
                path = projection_folder/('projection-'+str(degree)+'-'+str(count)+'.npz')
                evidence.own(path)
                evidence.check(str(degree)+'-'+str(count)+'_sealed_projection',hashlib.sha256(path.read_bytes()).hexdigest()==projected_status['outputs'][str(path.relative_to(evidence.root))])
                with np.load(path,allow_pickle=False) as saved:
                    projections[degree] = {name:saved[name].copy() for name in saved.files}
            for branch in ['reference','MTS']:
                system = LocallyRefinedSourceAction(count,branch=='MTS',background_mass=0.,source_splits=8)
                model = FlatPreassembledFlow(system)
                actual = cases[(branch,count)]
                prefix = branch+str(count)
                for degree,projected in projections.items():
                    times = projected['times']
                    evidence.check(prefix+str(degree)+'_matching_times',np.array_equal(times,actual['times']))
                    consistency = projected[branch+'_force']-projected['oracle_forces']
                    trajectory = actual['forces']-projected[branch+'_force']
                    total = actual['forces']-projected['oracle_forces']
                    closure = float(np.max(abs(total-consistency-trajectory)))
                    evidence.check(prefix+str(degree)+'_force_error_identity',closure<2e-13,closure)
                    force_resolution = float(np.max(abs(projected[branch+'_force']-projections[768][branch+'_force'])))
                    derivative_resolution = float(np.max(abs(projected['derivatives']-projections[768]['derivatives'])))
                    row = dict(branch=branch,count=count,degree=degree,splits=8,
                        max_total_force_error=float(np.max(abs(total))),max_consistency_force=float(np.max(abs(consistency))),
                        max_trajectory_force=float(np.max(abs(trajectory))),
                        total_at_021=float(total[42]),consistency_at_021=float(consistency[42]),trajectory_at_021=float(trajectory[42]),
                        projected_force_resolution_to768=force_resolution,derivative_resolution_to768=derivative_resolution,
                        total_force_gate_pass=bool(np.max(abs(total))<2e-7),decomposition_not_a_corrected_prediction=True)
                    if degree==768:
                        errors = actual['states']-projected['states']
                        linear,half_remainder,replayed,components = [],[],[],[]
                        for state,error,actual_state in zip(projected['states'],errors,actual['states']):
                            derivative = model.evaluate(state.astype(complex)+1e-25j*error)['force'].imag/1e-25
                            baseline_force = model.evaluate(state)['force']
                            half_force = model.evaluate(state+error/2)['force']
                            linear.append(derivative)
                            half_remainder.append(half_force-baseline_force-derivative/2)
                            replayed.append(model.evaluate(actual_state)['force'])
                            pieces = []
                            for selected in [slice(0,system.count),slice(system.count,system.count+1),
                                slice(system.count+1,-2),slice(-2,-1),slice(-1,None)]:
                                direction = np.zeros_like(error)
                                direction[selected] = error[selected]
                                pieces.append(model.evaluate(state.astype(complex)+1e-25j*direction)['force'].imag/1e-25)
                            components.append(pieces)
                        linear,half_remainder,components = np.array(linear),np.array(half_remainder),np.array(components)
                        remainder = trajectory-linear
                        replay_error = float(np.max(abs(np.array(replayed)-actual['forces'])))
                        component_error = float(np.max(abs(np.sum(components,axis=1)-linear)))
                        evidence.check(prefix+'_original_force_replay',replay_error<2e-11,replay_error)
                        evidence.check(prefix+'_directional_component_identity',component_error<2e-11,component_error)
                        index = 42
                        state = projected['states'][index]
                        matrices = model.matrices(state[system.count])
                        cross = band_product(matrices['transport'],state[:system.count])
                        inverse_cross = solve_banded((2,2),matrices['mass'],cross,check_finite=False)
                        inertia = system.source_mass/(1-state[-2]**2)**1.5
                        schur = model.evaluate(state)['schur']
                        nodal = -inertia/schur*inverse_cross*projected[branch+'_momentum_field'][index]
                        source_index = np.searchsorted(system.base_radii,system.anchor)
                        local = (system.radii>=system.base_radii[source_index-1]) & (system.radii<=system.base_radii[source_index])
                        contraction_error = float(abs(np.sum(nodal)-projected[branch+'_field_part'][index]))
                        evidence.check(prefix+'_spatial_force_contraction',contraction_error<2e-11,contraction_error)
                        row.update(max_linearization_remainder=float(np.max(abs(remainder))),
                            linearization_remainder_at_021=float(remainder[42]),
                            maximum_half_remainder=float(np.max(abs(half_remainder))),
                            half_to_full_remainder_ratio=float(np.max(abs(half_remainder))/max(np.max(abs(remainder)),1e-30)),
                            component_order=['field','source_position','field_rate','source_velocity','clock'],
                            component_force_at_021=components[42].tolist(),linearized_force_at_021=float(linear[42]),
                            source_covector_force_at_021=float(projected[branch+'_source_part'][42]),
                            field_feedback_force_at_021=float(projected[branch+'_field_part'][42]),
                            source_cell_feedback_at_021=float(np.sum(nodal[local])),
                            outside_source_cell_feedback_at_021=float(np.sum(nodal[~local])),
                            absolute_nodal_feedback_sum_at_021=float(np.sum(abs(nodal))),
                            max_nodal_state_error=float(np.max(abs(errors))))
                        destination = evidence.output/(prefix+'-retrospective-attribution.npz')
                        np.savez_compressed(destination,times=times,consistency=consistency,trajectory=trajectory,total=total,
                            actual_state_error=errors,linearized_trajectory_force=linear,remainder=remainder,
                            half_remainder=half_remainder,force_components=components,
                            reference_nodes=system.radii,field_force_contributions_at_021=nodal)
                        evidence.own(destination,'outputs')
                    evidence.report['cases'].append(row)
                    evidence.save()
                    print(row,flush=True)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()
