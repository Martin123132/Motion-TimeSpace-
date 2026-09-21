from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_moving_spectral_frame_20260916 import differentiated_frame, aligned_frame, cluster_projector, cluster_projector_derivative, close_selection_under_clusters, maximum, finite_frame_jet
from annular_moving_spectral_curvature_20260916 import curved_system_frame, analytic_matrix_derivatives, second_frame
from annular_locally_refined_source_action_20260916 import LocallyRefinedSourceAction
from scipy.linalg import expm,eigh
import json
import numpy as np


def synthetic(position):
    generator = np.array([[0.,3.,.3,0.],[-3.,0.,.4,.1],[-.3,-.4,0.,.2],[0.,-.1,-.2,0.]])
    strain = np.array([[.1,.02,.03,0.],[.02,-.04,0.,.01],[.03,0.,.02,.01],[0.,.01,.01,.03]])
    change = np.eye(4)+position*strain
    rotation = expm(position*generator)
    eigenvalues = np.diag([1.+.2*position,1.-.2*position,4.,9.])
    mass = change.T @ change
    stiffness = change.T @ rotation @ eigenvalues @ rotation.T @ change
    return mass,stiffness


def main():
    evidence = EvidenceRun('annular-spectral-clusters-curvature-attempt03',__file__)
    try:
        intake = evidence.root/'source-intake/navier-stokes/20260914'
        path = intake/'annular-moving-spectral-connection-attempt02/status.json'
        evidence.own(path)
        status = json.loads(path.read_text())
        evidence.check('moving_connection_qualification_complete',status['state']=='complete' and all(row['passed'] for row in status['checks']))
        mass,stiffness = synthetic(0.)
        mass_complex,stiffness_complex = synthetic(1e-24j)
        mass_b,stiffness_b = mass_complex.imag/1e-24,stiffness_complex.imag/1e-24
        frame = differentiated_frame(mass,stiffness,mass_b,stiffness_b)
        evidence.check('exact_degenerate_pair_clustered',frame['clusters'][0]==[0,1])
        evidence.check('partial_cluster_selection_completed',close_selection_under_clusters([0,3],frame['clusters'])==[0,1,3])
        cluster = [0,1]
        projector = cluster_projector(frame['vectors'],mass,cluster)
        projector_b = cluster_projector_derivative(frame,mass,mass_b,cluster)
        step = 1e-5
        samples=[]
        for sign in [-1,1]:
            moved_mass,moved_stiffness=synthetic(sign*step)
            unused,moved_vectors=eigh(moved_stiffness,moved_mass)
            samples.append(cluster_projector(moved_vectors,moved_mass,cluster))
        error=maximum((samples[1]-samples[0])/(2*step)-projector_b)
        evidence.check('degenerate_projector_has_finite_correct_derivative',error<2e-8,error)
        evidence.check('differentiated_projector_identity',maximum(projector_b @ projector+projector @ projector_b-projector_b)<2e-10)
        rotation=np.eye(4)
        angle=.713
        rotation[:2,:2]=[[np.cos(angle),-np.sin(angle)],[np.sin(angle),np.cos(angle)]]
        evidence.check('within_cluster_rotation_does_not_change_projector',
            maximum(cluster_projector(frame['vectors'] @ rotation,mass,cluster)-projector)<2e-12)
        evidence.report['synthetic_cluster']=dict(internal_gap=0.,projector_derivative_error=error,
            whole_cluster_retention_required=True,synthetic_not_physical_evidence=True)
        for count,splits in [(33,2),(65,4)]:
            for background in [0.,.7]:
                for gram in [False,True]:
                    label=str(count)+'-'+str(background)+'-'+str(gram)
                    system=LocallyRefinedSourceAction(count,gram,background_mass=background,source_splits=splits)
                    position=6.03
                    frame=curved_system_frame(system,position,relative_gap=1e-3)
                    errors={}
                    moved_first,unused=analytic_matrix_derivatives(system,position+1e-24j)
                    for name in ['mass','transport','transport_square','stiffness']:
                        first_error=maximum(frame['analytic_first'][name]-frame['derivatives'][name])/max(1.,maximum(frame['derivatives'][name]))
                        second_error=maximum(moved_first[name].imag/1e-24-frame['analytic_second'][name])/max(1.,maximum(frame['analytic_second'][name]))
                        evidence.check(label+'-'+name+'_first_and_second_matrix_derivatives',first_error<2e-10 and second_error<2e-10,
                            dict(first=first_error,second=second_error))
                        errors[name]=dict(first=first_error,second=second_error)
                    second=frame['second_connection']
                    relative=maximum(second+second.T-frame['normalization_second'])/max(1.,maximum(second))
                    evidence.check(label+'_second_mass_normalization',relative<2e-8,relative)
                    block_second=frame['block_stiffness_bb']
                    symmetry=maximum(block_second-block_second.T)/max(1.,maximum(block_second))
                    offblock=maximum(block_second[~frame['within']])/max(1.,maximum(block_second))
                    evidence.check(label+'_second_block_eigen_derivative',symmetry<2e-8 and offblock<2e-8,
                        dict(symmetry=symmetry,offblock=offblock))
                    fd=[]
                    accepted_controls=0
                    for step in [2e-4,1e-4,5e-5,2e-5,1e-5,5e-6,2e-6,1e-6,5e-7]:
                        try:
                            unused,approx=finite_frame_jet(system,position,frame,step)
                            error=maximum(approx-frame['vectors_bb'])/max(1.,maximum(frame['vectors_bb']))
                            fd.append(dict(step=step,relative_second_frame_error=error))
                            accepted_controls=accepted_controls+1 if error<3e-3 else 0
                        except ValueError as alignment_error:
                            fd.append(dict(step=step,alignment_rejected=str(alignment_error)))
                            accepted_controls=0
                        if accepted_controls>=2:
                            break
                    evidence.check(label+'_independent_second_frame_control',accepted_controls>=2,fd)
                    evidence.report['cases'].append(dict(count=count,source_splits=splits,background_mass=background,
                        branch='MTS' if gram else 'reference',matrix_errors=errors,second_frame_controls=fd,
                        second_frame_maximum=maximum(frame['vectors_bb']),frame_clusters=frame['clusters'],
                        curvature_analytically_derived=True,finite_difference_not_used_as_curvature=True,numerical_cluster_relative_gap=1e-3))
                    evidence.save()
        evidence.report.update(scope='Exact cluster/projector qualification plus closed prescribed-metric matrix derivatives and analytic local-polar spectral curvature.',
            physical_cluster_coverage_is_only_tested_states=True,live_metric_extension=False,
            freely_moving_reduced_trajectory_verified=False,internal_degenerate_gap_division_used=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()
