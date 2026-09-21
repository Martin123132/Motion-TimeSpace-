from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_moving_spectral_frame_20260916 import system_frame, finite_frame_jet, jet_pullback, maximum
from annular_locally_refined_source_action_20260916 import LocallyRefinedSourceAction
from run_annular_source_fitted_crossing_20260915 import initial
from scipy.linalg import solve
import json
import numpy as np


def main():
    evidence = EvidenceRun('annular-moving-spectral-connection-attempt01', __file__)
    try:
        intake = evidence.root/'source-intake/navier-stokes/20260914'
        previous_path = intake/'annular-dynamic-reduction-final-integrity.json'
        previous = json.loads(previous_path.read_text())
        evidence.own(previous_path)
        evidence.check('previous_checkpoint_complete', previous['state']=='complete' and all(row['passed'] for row in previous['checks']))
        for count, splits in [(33,2),(65,4)]:
            for background in [0., .7]:
                for gram in [False,True]:
                    system = LocallyRefinedSourceAction(count, gram, background_mass=background, source_splits=splits)
                    for position in [6.03,6.035]:
                        label = str(count)+'-'+str(background)+'-'+str(gram)+'-'+str(position)
                        frame = system_frame(system, position)
                        matrices, derivatives = frame['matrices'], frame['derivatives']
                        mass, stiffness = matrices['mass'], matrices['stiffness']
                        vectors, vectors_b = frame['vectors'], frame['vectors_b']
                        values = frame['values']
                        normalization = vectors_b.T @ mass @ vectors+vectors.T @ mass @ vectors_b+vectors.T @ derivatives['mass'] @ vectors
                        eigen_derivative = derivatives['stiffness'] @ vectors+stiffness @ vectors_b
                        eigen_derivative -= (derivatives['mass'] @ vectors+mass @ vectors_b)*values[None,:]
                        eigen_derivative -= mass @ vectors @ frame['block_stiffness_b']
                        derivative_scale = max(1., maximum(derivatives['stiffness'] @ vectors), maximum(stiffness @ vectors_b))
                        evidence.check(label+'_mass_normalization_derivative', maximum(normalization)<2e-9, maximum(normalization))
                        evidence.check(label+'_cluster_eigen_derivative', maximum(eigen_derivative)/derivative_scale<2e-9,
                            maximum(eigen_derivative)/derivative_scale)
                        evidence.check(label+'_no_cross_cluster_stiffness_derivative',
                            maximum(frame['block_stiffness_b'][~frame['within']])/max(1.,maximum(frame['block_stiffness_b']))<2e-9)
                        fd_rows = []
                        for step in [2e-6,1e-6]:
                            first, second = finite_frame_jet(system, position, frame, step)
                            error = maximum(first-vectors_b)/max(1.,maximum(vectors_b))
                            fd_rows.append(dict(step=step, relative_frame_derivative_error=error))
                        evidence.check(label+'_independent_aligned_frame_derivative', max(row['relative_frame_derivative_error'] for row in fd_rows)<2e-4, fd_rows)
                        raw_coordinates, raw_rates = np.split(initial(system)[:-1], 2)
                        physical_field, physical_velocity = raw_coordinates[:-1], raw_rates[:-1]
                        speed = .06
                        modal = vectors.T @ mass @ physical_field
                        modal_rate = vectors.T @ mass @ (physical_velocity-speed*vectors_b @ modal)
                        coordinates, rates = np.append(modal,position), np.append(modal_rate,speed)
                        pulled = jet_pullback(system,position,frame,second,coordinates,rates)
                        old = pulled['original']
                        transport, square = frame['modal_transport'],frame['modal_square']
                        wave = (modal_rate @ modal_rate/2+speed*modal_rate @ transport @ modal
                            +speed**2*modal @ square @ modal/2-np.dot(values,modal**2)/2)
                        action = wave-system.source_mass*old['clock']
                        formula_momentum = np.append(modal_rate+speed*transport @ modal,
                            old['material_momentum']+modal_rate @ transport @ modal+speed*modal @ square @ modal)
                        evidence.check(label+'_derived_action_matches_unchanged_action', abs(float(action-old['action']))<2e-10,
                            abs(float(action-old['action'])))
                        evidence.check(label+'_derived_source_and_field_momenta', maximum(formula_momentum-pulled['momenta'])<2e-10,
                            maximum(formula_momentum-pulled['momenta']))
                        energy = formula_momentum @ rates-action
                        old_energy = old['momenta'] @ pulled['physical_rates']-old['action']
                        evidence.check(label+'_energy_preserved', abs(float(energy-old_energy))<2e-10, abs(float(energy-old_energy)))
                        jacobian = np.zeros((system.count+1,system.count+1))
                        jacobian[:-1,:-1],jacobian[:-1,-1],jacobian[-1,-1] = vectors,vectors_b @ modal,1.
                        old_hessian = np.zeros_like(jacobian)
                        old_hessian[:-1,:-1],old_hessian[:-1,-1] = mass,old['cross']
                        old_hessian[-1,:-1],old_hessian[-1,-1] = old['cross'],old['source_inertia']
                        lapse,root = system.metric(0.,position)
                        material_inertia = system.source_mass*lapse**2/(root**2*old['clock']**3)
                        new_hessian = np.zeros_like(jacobian)
                        new_hessian[:-1,:-1] = np.eye(system.count)
                        new_hessian[:-1,-1],new_hessian[-1,:-1] = transport @ modal,transport @ modal
                        new_hessian[-1,-1] = material_inertia+modal @ square @ modal
                        evidence.check(label+'_velocity_hessian_congruence', maximum(new_hessian-jacobian.T @ old_hessian @ jacobian)<2e-9)
                        schur = new_hessian[-1,-1]-new_hessian[-1,:-1] @ new_hessian[:-1,-1]
                        evidence.check(label+'_positive_transformed_inertia', schur>0, float(schur))
                        old_covector = np.append(old['scalar_covector'], system.source_covector(0.,pulled['physical_coordinates'],pulled['physical_rates']))
                        new_covector = np.append(vectors.T @ old_covector[:-1]+speed*vectors_b.T @ old['momenta'][:-1],
                            old_covector[-1]+old_covector[:-1] @ (vectors_b @ modal)
                            +old['momenta'][:-1] @ (vectors_b @ modal_rate+speed*second @ modal))
                        moved_coordinates = coordinates.astype(complex)
                        moved_coordinates[-1] += 1e-24j
                        direct_covector = jet_pullback(system,position,frame,second,moved_coordinates,rates)['action'].imag/1e-24
                        evidence.check(label+'_independent_source_covector', abs(float(direct_covector-new_covector[-1]))<2e-9,
                            abs(float(direct_covector-new_covector[-1])))
                        checks = []
                        for on_shell in [False,True]:
                            if on_shell:
                                physical_accel = system.acceleration(0.,pulled['physical_coordinates'],pulled['physical_rates'])
                                bias = 2*speed*vectors_b @ modal_rate+speed**2*second @ modal+physical_accel[-1]*vectors_b @ modal
                                modal_accel = solve(vectors,physical_accel[:-1]-bias)
                                acceleration = np.append(modal_accel,physical_accel[-1])
                            else:
                                acceleration = np.append(.003*np.cos(np.arange(system.count)*.71),.013)
                                physical_accel = np.append(vectors @ acceleration[:-1]+2*speed*vectors_b @ modal_rate
                                    +speed**2*second @ modal+acceleration[-1]*vectors_b @ modal,acceleration[-1])
                            shifted = jet_pullback(system,position,frame,second,coordinates+1e-24j*rates,rates+1e-24j*acceleration)
                            new_momentum_rate = shifted['momenta'].imag/1e-24
                            original_shifted = system.evaluate(0.,pulled['physical_coordinates']+1e-24j*pulled['physical_rates'],
                                pulled['physical_rates']+1e-24j*physical_accel)
                            old_momentum_rate = original_shifted['momenta'].imag/1e-24
                            old_residual = old_covector-old_momentum_rate
                            new_residual = new_covector-new_momentum_rate
                            error = maximum(new_residual-jacobian.T @ old_residual)
                            checks.append(dict(on_shell=on_shell,cotangent_residual_error=error,
                                old_residual=maximum(old_residual),new_residual=maximum(new_residual)))
                            evidence.check(label+'_EL_transformation_'+str(on_shell), error<2e-9 and (not on_shell or maximum(new_residual)<2e-8), checks[-1])
                        connection_shift = float(old['momenta'][:-1] @ (vectors_b @ modal))
                        evidence.report['cases'].append(dict(count=count,source_splits=splits,background_mass=background,
                            branch='MTS' if gram else 'reference',position=position,source_speed=speed,
                            clusters=[cluster for cluster in frame['clusters'] if len(cluster)>1],minimum_external_gap=frame['minimum_external_gap'],
                            finite_difference_controls=fd_rows,source_momentum_connection_shift=connection_shift,
                            naive_source_momentum_error=abs(connection_shift),transformed_inertia_schur=float(schur),EL_controls=checks,
                            full_frame_only=True,second_frame_jet_used_for_chain_rule_not_a_certified_modal_curvature=True))
                        evidence.save()
        evidence.report.update(scope='Full moving-frame action, canonical momentum, kinetic Hessian and off-shell EL covariance qualification; source moves and prescribed background is retained. No reduced trajectory or full GR proof.',
            source_momentum_connection_retained=True, omitted_mode_dynamic_bound_established=False,
            moving_spectral_reduced_solver_implemented=False, live_metric_action_varied=False,
            original_Gram_rows_retained=True, original_action_changed=False, damping_added=False,
            second_frame_derivative_accuracy_not_certified=True)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()
