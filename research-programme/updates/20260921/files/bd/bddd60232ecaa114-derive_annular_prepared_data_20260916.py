from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_relaxed_trace_action_20260916 import RelaxedTraceSourceAction
from annular_locally_refined_source_action_20260916 import LocallyRefinedSourceAction
from annular_boundary_response_20260916 import field_matrices
from scipy.linalg import solve_banded
import json
import numpy as np


def main():
    evidence = EvidenceRun('annular-prepared-data-criterion-attempt01', __file__)
    try:
        intake = evidence.root/'source-intake/navier-stokes/20260914'
        response_path = intake/'annular-relaxed-force-change-attempt01/status.json'
        evidence.own(response_path)
        response = json.loads(response_path.read_text())
        evidence.check('existing_response_derivation_complete', response['state']=='complete' and all(row['passed'] for row in response['checks']))
        for case in response['cases']:
            count = case['count']
            system = RelaxedTraceSourceAction(count, True, background_mass=0.)
            path = intake/'annular-quadratic-crossing-attempt01'/('MTS-'+str(count)+'.npz')
            evidence.own(path)
            saved = np.load(path)
            rows = []
            for instant, state, observed in zip(saved['times'], saved['states'], case['trajectory']):
                coordinates, rates = np.split(state[:-1], 2)
                trace = system.trace_data(instant, coordinates)
                kinetic = system.evaluate(instant, coordinates, rates)
                denominator = trace['denominator']
                mismatch = trace['physical_reference_jump']-trace['auxiliary_trace']
                gap = float(denominator*mismatch**2/2)
                target_gradient = np.asarray(system.original.T @ (trace['weights']*system.lifted_hinge))/denominator
                trace_gradient = system.jump-target_gradient
                perturbed = coordinates.astype(complex)
                perturbed[-1] += 1e-24j
                weights_b = system.trace_data(instant, perturbed)['weights'].imag/1e-24
                denominator_b = system.lifted_hinge @ (weights_b*system.lifted_hinge)
                target_b = (system.lifted_hinge @ (weights_b*(system.original @ coordinates[:-1]))-trace['auxiliary_trace']*denominator_b)/denominator
                inverse = solve_banded((2, 2), kinetic['mass_bands'], np.column_stack([trace_gradient, kinetic['cross']]))
                schur = kinetic['source_inertia']-kinetic['cross'] @ inverse[:, 1]
                material = system.source_mass/(1-rates[-1]**2)**1.5
                ratio = material/schur
                coefficient_linear = float(ratio*abs(denominator_b)/denominator)
                coefficient_root = float(ratio*np.sqrt(2*denominator)*abs(target_b+kinetic['cross'] @ inverse[:, 0]))
                bound = coefficient_linear*gap+coefficient_root*np.sqrt(gap)
                budget = 2e-7
                allowed = (2*budget/(coefficient_root+np.sqrt(coefficient_root**2+4*coefficient_linear*budget)))**2 if coefficient_linear+coefficient_root>0 else None
                signed_law = float(ratio*(denominator_b*mismatch**2/2-denominator*mismatch*(target_b+kinetic['cross'] @ inverse[:, 0])))
                evidence.check(str(count)+'-'+str(float(instant))+'_same_state_energy_bound',
                    schur>0 and abs(signed_law)<=bound+2e-14 and abs(signed_law-observed['derived_same_state_force_change'])<2e-11)
                rows.append(dict(time=float(instant), potential_gap=gap, coefficient_A=coefficient_linear, coefficient_B=coefficient_root,
                    instantaneous_bound=bound, derived_same_state_force=signed_law, force_budget=budget,
                    sufficient_potential_gap=allowed, instantaneous_sufficient_condition_met=bool(bound<=budget),
                    observed_trajectory_feedback=observed['trajectory_feedback_force_change'],
                    full_trajectory_certified=False, acceleration_defect_source=float(signed_law/material)))
            evidence.report['cases'].append(dict(count=count, saved_states=rows))
            evidence.save()
        fine = LocallyRefinedSourceAction(65, True, background_mass=0., source_splits=1)
        matrices = field_matrices(fine, fine.anchor)
        denominator = float(fine.lifted_hinge @ (matrices['gram_weights']*fine.lifted_hinge))
        evidence.check('scalar_layer_inherits_positive_Gram_coefficient', denominator>0, denominator)
        layer_rows = []
        radius, duration, drive_frequency = fine.anchor, .4, 1.
        times = np.linspace(0., duration, 1001)
        for thickness in [fine.gram_spacing/2**power for power in range(1, 7)]:
            mass = thickness**3*(radius**2/30+radius*thickness/30+thickness**2/105)
            bulk = thickness*(radius**2/3+radius*thickness/3+2*thickness**2/15)
            stiffness = bulk+denominator
            frequency = np.sqrt(stiffness/mass)
            mismatch = drive_frequency**2/(frequency**2-drive_frequency**2)*(np.sin(drive_frequency*times)-drive_frequency/frequency*np.sin(frequency*times))
            mismatch_rate = drive_frequency**3/(frequency**2-drive_frequency**2)*(np.cos(drive_frequency*times)-np.cos(frequency*times))
            norm = np.sqrt(mass*mismatch_rate**2+stiffness*mismatch**2)
            bound = np.sqrt(mass)*drive_frequency**2*times
            evidence.check('prepared_layer_'+str(thickness), np.all(norm<=bound+2e-14) and mismatch[0]==0 and mismatch_rate[0]==0)
            layer_rows.append(dict(thickness=float(thickness), mass=float(mass), stiffness=float(stiffness),
                frequency=float(frequency), original_fixed_Gram_coefficient=denominator,
                unprepared_unit_displacement_maximum=1., unprepared_energy_norm=float(np.sqrt(stiffness)),
                prepared_maximum_energy_norm=float(np.max(norm)), prepared_uniform_energy_bound=float(bound[-1]),
                conjugate_trace_load_bound=float(denominator/np.sqrt(stiffness)*bound[-1]),
                is_physical_source_force=False, scalar_trial_layer_not_full_coupled_solution=True))
        evidence.check('prepared_layer_bound_decreases_under_fixed_stencil_refinement',
            all(later['prepared_uniform_energy_bound']<earlier['prepared_uniform_energy_bound'] for earlier, later in zip(layer_rows, layer_rows[1:])))
        evidence.report.update(layer_controls=layer_rows, no_damping_added=True, original_initial_data_not_replaced=True,
            moving_source_stability_tube_certified=False, scalar_layer_is_not_parent_derivation=True,
            scope='Instantaneous bound evaluated on real saved moving states; scalar prepared-data scaling derived/tested separately. No stability constant or moving-force pass fabricated.')
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()
