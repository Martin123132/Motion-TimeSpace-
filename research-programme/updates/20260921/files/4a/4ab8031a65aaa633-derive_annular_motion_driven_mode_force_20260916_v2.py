from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_moving_spectral_curvature_20260916 import curved_system_frame
from annular_moving_spectral_frame_20260916 import close_selection_under_clusters,jet_pullback,maximum
from annular_locally_refined_source_action_20260916 import LocallyRefinedSourceAction
from run_annular_source_fitted_crossing_20260915 import initial
from annular_dynamic_reduction_bound_20260916 import evolution
import json
import numpy as np


def main():
    evidence=EvidenceRun('annular-motion-driven-mode-force-attempt02',__file__)
    try:
        intake=evidence.root/'source-intake/navier-stokes/20260914'
        for folder in ['annular-spectral-clusters-curvature-attempt03','annular-force-aware-modes-attempt01']:
            path=intake/folder/'status.json'
            evidence.own(path)
            status=json.loads(path.read_text())
            evidence.check(folder+'_complete',status['state']=='complete' and all(row['passed'] for row in status['checks']))
        selection=status
        for gram in [False,True]:
            branch='MTS' if gram else 'reference'
            system=LocallyRefinedSourceAction(129,gram,background_mass=0.,source_splits=8)
            frame=curved_system_frame(system,system.anchor,relative_gap=1e-3)
            vectors,vectors_b,second=frame['vectors'],frame['vectors_b'],frame['vectors_bb']
            mass=frame['matrices']['mass']
            chosen=next(row for row in selection['cases'] if row['branch']==branch)['retained_indices']
            retained=close_selection_under_clusters(chosen,frame['clusters'])
            omitted=np.setdiff1d(np.arange(system.count),retained)
            evidence.check(branch+'_retained_selection_is_union_of_clusters',all(not(set(cluster).intersection(retained)) or set(cluster).issubset(retained) for cluster in frame['clusters']))
            path=intake/'annular-invariant-modal-force-bound-attempt01'/(branch+'-modal-budget.npz')
            evidence.own(path)
            with np.load(path) as saved:
                contribution=saved['force_contribution_envelope']
            frozen_envelope=float(np.sum(contribution[np.ix_(retained,omitted)])+np.sum(contribution[np.ix_(omitted,omitted)])/2)
            evidence.check(branch+'_cluster_completion_preserves_frozen_budget',frozen_envelope<=2e-7)
            original_coordinates,original_rates=np.split(initial(system)[:-1],2)
            snapshot_times=np.array([0.,.2,.4])
            frozen_fields,frozen_rates,unused=evolution(mass,np.sqrt(frame['values']),vectors,
                original_coordinates[:-1],original_rates[:-1],snapshot_times)
            for instant,field,field_rate in zip(snapshot_times,frozen_fields,frozen_rates):
                for speed in [0.,.06]:
                    label=branch+'-'+str(instant)+'-'+str(speed)
                    all_modal=vectors.T @ mass @ field
                    all_rate=vectors.T @ mass @ (field_rate-speed*vectors_b @ all_modal)
                    modal,modal_rate=all_modal.copy(),all_rate.copy()
                    modal[omitted],modal_rate[omitted]=0.,0.
                    modal_rate[retained]+=speed*frame['modal_transport'][np.ix_(retained,omitted)] @ all_modal[omitted]
                    coordinates,rates=np.append(modal,system.anchor),np.append(modal_rate,speed)
                    pulled=jet_pullback(system,system.anchor,frame,second,coordinates,rates)
                    old=pulled['original']
                    transport,square,transport_b=frame['modal_transport'],frame['modal_square'],frame['modal_transport_b']
                    material_inertia=system.source_mass/(1-speed**2)**1.5
                    cross=transport @ modal
                    inertia=material_inertia+modal @ square @ modal
                    full_schur=inertia-cross @ cross
                    reduced_schur=inertia-cross[retained] @ cross[retained]
                    evidence.check(label+'_positive_full_and_reduced_inertia',full_schur>0 and reduced_schur>0,
                        dict(full=float(full_schur),reduced=float(reduced_schur)))
                    old_covector=np.append(old['scalar_covector'],system.source_covector(0.,pulled['physical_coordinates'],pulled['physical_rates']))
                    new_covector=np.append(vectors.T @ old_covector[:-1]+speed*vectors_b.T @ old['momenta'][:-1],
                        old_covector[-1]+old_covector[:-1] @ (vectors_b @ modal)
                        +old['momenta'][:-1] @ (vectors_b @ modal_rate+speed*second @ modal))
                    shifted=jet_pullback(system,system.anchor,frame,second,coordinates+1e-24j*rates,rates)
                    right_side=new_covector-shifted['momenta'].imag/1e-24
                    analytic_field_rhs=-speed*(transport-transport.T) @ modal_rate-frame['values']*modal
                    analytic_field_rhs-=speed**2*(transport_b-square) @ modal
                    field_rhs_error=maximum(right_side[:-1]-analytic_field_rhs)/max(1.,maximum(analytic_field_rhs))
                    evidence.check(label+'_derived_motion_driven_field_equation',field_rhs_error<2e-8,field_rhs_error)
                    action_formula=(modal_rate @ modal_rate/2+speed*modal_rate @ transport @ modal
                        +speed**2*modal @ square @ modal/2-np.dot(frame['values'],modal**2)/2-system.source_mass*old['clock'])
                    momentum_formula=np.append(modal_rate+speed*transport @ modal,
                        old['material_momentum']+modal_rate @ transport @ modal+speed*modal @ square @ modal)
                    evidence.check(label+'_clustered_moving_action_and_momenta',abs(float(action_formula-old['action']))<2e-9
                        and maximum(momentum_formula-pulled['momenta'])<2e-9)
                    reduced_accel=(right_side[-1]-cross[retained] @ right_side[retained])/reduced_schur
                    full_accel=(right_side[-1]-cross @ right_side[:-1])/full_schur
                    drive=right_side[omitted]-cross[omitted]*reduced_accel
                    predicted=-material_inertia*(cross[omitted] @ drive)/full_schur
                    difference=material_inertia*(full_accel-reduced_accel)
                    bound=material_inertia*np.linalg.norm(cross[omitted])*np.linalg.norm(drive)/full_schur
                    original_snapshot_coordinates=np.append(field,system.anchor)
                    original_snapshot_rates=np.append(field_rate,speed)
                    original_snapshot=system.evaluate(0.,original_snapshot_coordinates,original_snapshot_rates)
                    snapshot_accel=system.acceleration(0.,original_snapshot_coordinates,original_snapshot_rates)[-1]
                    field_error=field-pulled['physical_coordinates'][:-1]
                    rate_error=field_rate-pulled['physical_rates'][:-1]
                    kinetic_projection_residual=vectors[:,retained].T @ (original_snapshot['momenta'][:-1]-old['momenta'][:-1])
                    preparation_energy_square=rate_error @ mass @ rate_error+field_error @ frame['matrices']['stiffness'] @ field_error
                    preparation_energy_square+=2*speed*rate_error @ frame['matrices']['transport'] @ field_error
                    preparation_energy_square+=speed**2*field_error @ frame['matrices']['transport_square'] @ field_error
                    evidence.check(label+'_retained_canonical_momentum_projection',maximum(kinetic_projection_residual)<2e-10 and preparation_energy_square>=-2e-14,
                        dict(momentum_residual=maximum(kinetic_projection_residual),preparation_energy_square=float(preparation_energy_square)))
                    projection_force_difference=material_inertia*(snapshot_accel-full_accel)
                    total_fixture_force_difference=material_inertia*(snapshot_accel-reduced_accel)
                    evidence.check(label+'_projection_and_omission_force_decomposition',abs(float(projection_force_difference+difference-total_fixture_force_difference))<2e-12)
                    actual_original_accel=system.acceleration(0.,pulled['physical_coordinates'],pulled['physical_rates'])[-1]
                    evidence.check(label+'_full_acceleration_matches_original_action',abs(float(full_accel-actual_original_accel))<2e-8,
                        abs(float(full_accel-actual_original_accel)))
                    evidence.check(label+'_exact_omitted_drive_force_law',abs(float(predicted-difference))<2e-11 and abs(float(difference))<=bound+2e-14,
                        dict(identity_error=abs(float(predicted-difference)),observed=float(difference),bound=float(bound)))
                    evidence.check(label+'_held_source_stationary_limit',speed!=0. or maximum(right_side[omitted])<2e-8,
                        maximum(right_side[omitted]))
                    velocity_drive=(-speed*(transport-transport.T) @ modal_rate)[omitted]
                    speed_square_drive=(-speed**2*(transport_b-square) @ modal)[omitted]
                    acceleration_drive=-cross[omitted]*reduced_accel
                    evidence.report['cases'].append(dict(branch=branch,snapshot_time=float(instant),assigned_source_speed=speed,
                        fixture='exact frozen full-field snapshot, projected into retained moving coordinates; NOT a moving trajectory',
                        retained_count=len(retained),omitted_count=len(omitted),cluster_added_indices=sorted(set(retained)-set(chosen)),
                        frozen_envelope_after_cluster_completion=frozen_envelope,
                        omitted_drive_norm=float(np.linalg.norm(drive)),velocity_drive_norm=float(np.linalg.norm(velocity_drive)),
                        speed_square_drive_norm=float(np.linalg.norm(speed_square_drive)),source_acceleration_drive_norm=float(np.linalg.norm(acceleration_drive)),
                        same_state_material_force_difference=float(difference),same_state_material_force_bound=float(bound),
                        same_state_sufficient_budget_met=bool(bound<=2e-7),source_momentum_connection_shift=float(old['momenta'][:-1] @ (vectors_b @ modal)),
                        full_source_acceleration=float(full_accel),reduced_source_acceleration=float(reduced_accel),
                        full_acceleration_original_error=abs(float(full_accel-actual_original_accel)),
                        freely_evolved_reduced_trajectory=False,original_initial_tail_not_forgotten=True,
                        preparation='retain field coordinates and canonical field momenta; b,V fixed',
                        preparation_energy_norm=float(np.sqrt(max(0.,preparation_energy_square))),
                        projection_source_force_difference=float(projection_force_difference),
                        total_fixture_source_force_difference=float(total_fixture_force_difference),
                        total_fixture_observed_budget_met=bool(abs(total_fixture_force_difference)<=2e-7),
                        initial_error_quantified_not_uniformly_propagated=True))
                    evidence.save()
        evidence.report.update(scope='Derived and checked exact instantaneous source-force response to motion-driven omitted modes, with analytic basis curvature and cluster-complete masks. Frozen fixtures are not moving evolution.',
            no_force_correction_applied=True,field_modes_and_source_momentum_from_original_action=True,
            source_acceleration_driving_retained=True,all_time_reduced_error_bound=False,
            moving_solver_implemented=False,physical_GR_gates_unchanged=True,
            canonical_momentum_projection_derived=True,full_projection_error_recorded=True,
            frozen_bound_not_reused_as_moving_preparation_bound=True)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()
