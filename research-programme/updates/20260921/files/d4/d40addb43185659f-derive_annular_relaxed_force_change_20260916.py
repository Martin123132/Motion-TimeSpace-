from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_relaxed_trace_action_20260916 import RelaxedTraceSourceAction
from annular_locally_refined_source_action_20260916 import LocallyRefinedSourceAction
from scipy.linalg import solve_banded
import json
import numpy as np


def mechanical_force(system, instant, coordinates, rates):
    return float(system.source_mass*system.acceleration(instant, coordinates, rates)[-1]/(1-rates[-1]**2)**1.5)


def main():
    evidence = EvidenceRun('annular-relaxed-force-change-attempt01', __file__)
    try:
        intake = evidence.root/'source-intake/navier-stokes/20260914'
        old_folder = intake/'annular-quadratic-crossing-attempt01'
        for folder in ['annular-quadratic-crossing-attempt01', 'annular-relaxed-branch-smoke-attempt01', 'annular-relaxed-branch-refinement257-attempt01']:
            path = intake/folder/'status.json'
            evidence.own(path)
            status = json.loads(path.read_text())
            evidence.check(folder+'_complete', status['state']=='complete' and all(row['passed'] for row in status['checks']))
        for count in [65, 129, 257]:
            original = LocallyRefinedSourceAction(count, True, background_mass=0., source_splits=1)
            relaxed = RelaxedTraceSourceAction(count, True, background_mass=0.)
            old_path = old_folder/('MTS-'+str(count)+'.npz')
            new_path = intake/('annular-relaxed-branch-smoke-attempt01' if count<257 else 'annular-relaxed-branch-refinement257-attempt01')/('relaxed_MTS-'+str(count)+'.npz')
            for path in [old_path, new_path]:
                evidence.own(path)
            old_saved, new_saved = np.load(old_path), np.load(new_path)
            evidence.check(str(count)+'_same_comparison_times', np.array_equal(old_saved['times'], new_saved['times']))
            rows = []
            errors = dict(potential=0., field_covector=0., source_covector=0., full_momentum=0., force_response=0.)
            for instant, old_state, new_state in zip(old_saved['times'], old_saved['states'], new_saved['states']):
                coordinates, rates = np.split(old_state[:-1], 2)
                new_coordinates, new_rates = np.split(new_state[:-1], 2)
                before = original.evaluate(instant, coordinates, rates)
                after = relaxed.evaluate(instant, coordinates, rates)
                trace = relaxed.trace_data(instant, coordinates)
                denominator = trace['denominator']
                mismatch = trace['physical_reference_jump']-trace['auxiliary_trace']
                gap = float(denominator*mismatch**2/2)
                target_gradient = np.asarray(relaxed.original.T @ (trace['weights']*relaxed.lifted_hinge))/denominator
                field_gradient = denominator*mismatch*(relaxed.jump-target_gradient)
                perturbed = coordinates.astype(complex)
                perturbed[-1] += 1e-24j
                weight_b = relaxed.trace_data(instant, perturbed)['weights'].imag/1e-24
                denominator_b = relaxed.lifted_hinge @ (weight_b*relaxed.lifted_hinge)
                values = relaxed.original @ coordinates[:-1]
                target_b = (relaxed.lifted_hinge @ (weight_b*values)-trace['auxiliary_trace']*denominator_b)/denominator
                source_gradient = denominator_b*mismatch**2/2-denominator*mismatch*target_b
                inverse = solve_banded((2, 2), before['mass_bands'], np.column_stack([field_gradient, before['cross']]))
                schur = before['source_inertia']-before['cross'] @ inverse[:, 1]
                material_inertia = relaxed.source_mass/(1-rates[-1]**2)**1.5
                predicted_force_change = float(material_inertia*(source_gradient-before['cross'] @ inverse[:, 0])/schur)
                old_force = mechanical_force(original, instant, coordinates, rates)
                relaxed_same = mechanical_force(relaxed, instant, coordinates, rates)
                relaxed_evolved = mechanical_force(relaxed, instant, new_coordinates, new_rates)
                errors['potential'] = max(errors['potential'], abs(float(before['potential']-after['potential'])-gap))
                errors['field_covector'] = max(errors['field_covector'], float(np.max(abs(after['scalar_covector']-before['scalar_covector']-field_gradient))))
                observed_source_difference = relaxed.source_covector(instant, coordinates, rates)-original.source_covector(instant, coordinates, rates)
                errors['source_covector'] = max(errors['source_covector'], abs(float(observed_source_difference-source_gradient)))
                errors['full_momentum'] = max(errors['full_momentum'], float(np.max(abs(after['momenta']-before['momenta']))))
                errors['force_response'] = max(errors['force_response'], abs(relaxed_same-old_force-predicted_force_change))
                rows.append(dict(time=float(instant), positive_potential_gap=gap, trace_mismatch=float(mismatch),
                    original_force=old_force, relaxed_same_state_force=relaxed_same, relaxed_evolved_force=relaxed_evolved,
                    derived_same_state_force_change=predicted_force_change,
                    trajectory_feedback_force_change=relaxed_evolved-relaxed_same, total_force_change=relaxed_evolved-old_force))
            for name, threshold in dict(potential=2e-13, field_covector=2e-10, source_covector=2e-11, full_momentum=2e-14, force_response=2e-11).items():
                evidence.check(str(count)+'_'+name, errors[name]<threshold, errors[name])
            evidence.report['cases'].append(dict(count=count, errors=errors, trajectory=rows))
            evidence.save()
        evidence.report.update(scope='Exact finite same-state force response to the derived potential relaxation, separated from changed-trajectory feedback. No retuning, damping, or force subtraction applied.',
            force_decomposition_used_as_correction=False, derivative_trace_prescribed=False,
            relaxed_model_adopted_as_parent=False, dynamic_limit_proven=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()
