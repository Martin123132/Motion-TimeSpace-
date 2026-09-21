from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_full_force_linearization_20260916 import FullForceLinearization
from annular_locally_refined_source_action_20260916 import LocallyRefinedSourceAction
from run_annular_source_fitted_crossing_20260915 import initial
import numpy as np


def main():
    evidence = EvidenceRun('annular-full-force-linearization-attempt01',__file__)
    try:
        random = np.random.default_rng(16340)
        for count,splits,background in [(33,2,0.),(33,2,.7),(129,8,0.)]:
            for gram in [False,True]:
                system = LocallyRefinedSourceAction(count,gram,background_mass=background,source_splits=splits)
                model = FullForceLinearization(system)
                branch = 'MTS' if gram else 'reference'
                for moved in [False,True]:
                    state = initial(system)
                    if moved:
                        state[system.count] += .0003
                        state[:system.count] *= 1.03
                        state[system.count+1:-2] += 1e-6*random.standard_normal(system.count)
                        state[-2] = .055
                    data = model.evaluate(state,True)
                    coordinates,rates = np.split(state[:-1],2)
                    original = system.acceleration(0.,coordinates,rates)
                    error = float(np.linalg.norm(data['acceleration']-original)/max(1.,np.linalg.norm(original)))
                    label = '-'.join(map(str,[branch,count,background,moved]))
                    evidence.check(label+'_unchanged_original_acceleration',error<2e-9,error)
                    directions = []
                    for index in [system.count,2*system.count+1,len(state)-1]:
                        direction = np.zeros(len(state))
                        direction[index] = 1.
                        directions.append(direction)
                    for group in ['field','rate','mixed']:
                        direction = random.standard_normal(len(state))
                        if group=='field':
                            direction[system.count:] = 0.
                        elif group=='rate':
                            direction[:system.count+1] = 0.
                            direction[-2:] = 0.
                        directions.append(direction/np.linalg.norm(direction))
                    errors,force_errors = [],[]
                    for direction in directions:
                        complex_data = model.evaluate(state.astype(complex)+1e-24j*direction)
                        expected = complex_data['flow'].imag/1e-24
                        actual = data['jacobian'] @ direction
                        errors.append(float(np.linalg.norm(actual-expected)/max(1.,np.linalg.norm(expected))))
                        expected_force = float(complex_data['force'].imag/1e-24)
                        force_errors.append(abs(float(data['force_gradient'] @ direction)-expected_force)/max(1.,abs(expected_force)))
                    evidence.check(label+'_independent_complex_step_full_Jacobian',max(errors)<2e-8,errors)
                    evidence.check(label+'_independent_complex_step_force_gradient',max(force_errors)<2e-8,force_errors)
                    evidence.check(label+'_clock_not_dropped_or_spuriously_force_coupled',np.linalg.norm(data['jacobian'][:,-1])==0.
                        and data['force_gradient'][-1]==0. and data['jacobian'][-1,-2]!=0.)
                    covector = random.standard_normal(len(state))
                    direction = directions[-1]
                    evidence.check(label+'_transpose_duality',abs(float(covector @ (data['jacobian'] @ direction)
                        -(data['jacobian'].T @ covector) @ direction))<1e-7)
                    evidence.report['cases'].append(dict(branch=branch,base_count=count,source_splits=splits,background=background,
                        moved=moved,acceleration_relative_error=error,maximum_Jacobian_direction_error=max(errors),
                        maximum_force_direction_error=max(force_errors),full_state_dimension=len(state)))
                    evidence.save()
        evidence.report.update(full_field_source_clock_linearization=True,original_action_unchanged=True,
            finite_prescribed_metric_only=True,linearization_not_stability_certificate=True)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()
