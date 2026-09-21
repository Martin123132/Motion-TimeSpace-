from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_windowed_projector_chart_20260916 import WindowedProjectorChart
from annular_anchored_projector_chart_20260916 import omission_diagnostic, material_terms
from annular_locally_refined_source_action_20260916 import LocallyRefinedSourceAction
from run_annular_source_fitted_crossing_20260915 import initial
from scipy.integrate import solve_ivp
import argparse
import json
import time
import numpy as np


def phase_energy(data, field, rate, speed):
    value = field @ data['stiffness'] @ field+rate @ data['mass'] @ rate
    value += 2*speed*rate @ data['transport'] @ field+speed**2*field @ data['transport_square'] @ field
    return float(np.sqrt(max(0.,value)))


def snapshot(system, chart, instant, full_state, reduced_state):
    full_coordinates, full_rates = np.split(full_state[:-1],2)
    coordinates, rates = np.split(reduced_state[:-3],2)
    physical, physical_rates = chart.lift(coordinates,rates)
    data = chart.at(coordinates[-1])
    diagnostic = omission_diagnostic(chart,coordinates,rates)
    full_acceleration = system.acceleration(instant,full_coordinates,full_rates)
    full_material = material_terms(system,full_coordinates[-1],full_rates[-1])
    reduced_material = material_terms(system,coordinates[-1],rates[-1])
    full_force = full_material['inertia']*full_acceleration[-1]+full_material['momentum_b']*full_rates[-1]
    reduced_force = reduced_material['inertia']*diagnostic['reduced_acceleration'][-1]+reduced_material['momentum_b']*rates[-1]
    total = float(full_force-reduced_force)
    full_data = system.evaluate(instant,full_coordinates,full_rates)
    projected_data = system.evaluate(instant,physical,physical_rates)
    momentum_error = data['basis'].T @ (full_data['momenta'][:-1]-projected_data['momenta'][:-1])
    row = dict(time=float(instant),full_force=float(full_force),reduced_force=float(reduced_force),force_difference=total,
        same_state_force_difference=diagnostic['same_state_force'],same_state_force_bound=diagnostic['same_state_force_bound'],
        trajectory_contribution=total-diagnostic['same_state_force'],
        sampled_force_budget_met=bool(abs(total)<=2e-7),
        force_identity_error=abs(diagnostic['same_state_force']-diagnostic['same_state_force_predicted']),
        defect_identity_error=abs(diagnostic['kinetic_defect_square']-diagnostic['predicted_defect_square']),
        omitted_drive_norm=diagnostic['omitted_drive_norm'],kinetic_defect_norm=diagnostic['kinetic_defect_norm'],
        integrated_omitted_drive=float(reduced_state[-2]),integrated_kinetic_defect=float(reduced_state[-1]),
        reference_coordinate_phase_error=phase_energy(data['matrices'],full_coordinates[:-1]-physical[:-1],full_rates[:-1]-physical_rates[:-1],rates[-1]),
        source_position_error=abs(float(full_coordinates[-1]-coordinates[-1])),
        source_velocity_error=abs(float(full_rates[-1]-rates[-1])),clock_error=abs(float(full_state[-1]-reduced_state[-3])),
        full_energy=float(system.energy(instant,full_coordinates,full_rates)),
        reduced_energy=float(system.energy(instant,physical,physical_rates)),
        retained_momentum_difference_norm=float(np.linalg.norm(momentum_error)),
        source_connection_momentum=diagnostic['source_connection_momentum'],
        retained_EL_residual=diagnostic['retained_EL_residual'],
        relative_external_gap=data['relative_external_gap'],overlap_min=data['overlap_min'],
        full_position=float(full_coordinates[-1]),reduced_position=float(coordinates[-1]),
        full_speed=float(full_rates[-1]),reduced_speed=float(rates[-1]))
    return row


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--tight',action='store_true')
    options = parser.parse_args()
    label = 'annular-anchored-moving-'+('tight' if options.tight else 'smoke')+'-attempt01'
    evidence = EvidenceRun(label,__file__)
    try:
        intake = evidence.root/'source-intake/navier-stokes/20260914'
        selection_path = intake/'annular-force-aware-modes-attempt01/status.json'
        qualification_path = intake/'annular-anchored-chart-qualification-attempt03/status.json'
        for path in [selection_path,qualification_path]:
            evidence.own(path)
        selection = json.loads(selection_path.read_text())
        qualification = json.loads(qualification_path.read_text())
        evidence.check('chart_variationally_qualified',qualification['state']=='complete'
            and all(row['passed'] for row in qualification['checks']))
        times = np.linspace(0.,.005,41)
        evidence.report.update(configuration=dict(base_count=129,source_splits=8,background_mass=0.,
            final_time=.005,sample_count=41,accepted_intervals=8,source_window_half_width=.001,survey_count=201,
            rtol=2e-12 if options.tight else 2e-10,atol=2e-14 if options.tight else 2e-12,
            maximum_step_rule='0.5/omega_max' if options.tight else '1/omega_max',tight=options.tight,
            same_sample_reduction_force_budget=2e-7),
            scope='Short moving reduced/full original finite-action comparison; not a GR oracle test.',
            original_initial_full_state_unchanged=True,canonical_field_momentum_projection=True,
            no_force_correction=True,no_fitted_parameter=True,physical_GR_gates_unchanged=True,
            all_time_error_certificate=False,continuous_gap_certificate=False,
            omitted_drive_integral_not_trajectory_error_bound=True,github_action=False,subagents_used=False)
        evidence.save()
        for gram in [False,True]:
            started = time.monotonic()
            branch = 'MTS' if gram else 'reference'
            system = LocallyRefinedSourceAction(129,gram,background_mass=0.,source_splits=8)
            chosen = next(row for row in selection['cases'] if row['branch']==branch)['retained_indices']
            chart = WindowedProjectorChart(system,chosen)
            qualified = next(row for row in qualification['cases'] if row['branch']==branch and row['base_count']==129)
            evidence.check(branch+'_same_qualified_mask',chart.retained==qualified['selection_survey']['retained_indices'])
            full_states = [initial(system)]
            reduced_states = [np.append(chart.prepare(full_states[0]),[0.,0.])]
            initial_chart = chart.at(system.anchor)
            step = (.5 if options.tight else 1.)/np.sqrt(initial_chart['values'][-1])
            rtol,atol = evidence.report['configuration']['rtol'],evidence.report['configuration']['atol']
            calls = dict(full=0,reduced=0)
            rows = [snapshot(system,chart,0.,full_states[0],reduced_states[0])]
            evidence.check(branch+'_initial_canonical_projection',rows[0]['retained_momentum_difference_norm']<2e-10)

            def full_rhs(instant,state):
                coordinates,rates = np.split(state[:-1],2)
                return np.concatenate([rates,system.acceleration(instant,coordinates,rates),
                    [material_terms(system,coordinates[-1],rates[-1])['clock']]])

            def reduced_rhs(instant,state):
                core = state[:-2]
                coordinates,rates = np.split(core[:-1],2)
                derivative = chart.rhs(instant,core)
                diagnostic = omission_diagnostic(chart,coordinates,rates)
                return np.append(derivative,[diagnostic['omitted_drive_norm'],diagnostic['kinetic_defect_norm']])

            for interval in range(8):
                interval_times = times[5*interval:5*interval+6]
                results = []
                for name,rhs,state in [('full',full_rhs,full_states[-1]),('reduced',reduced_rhs,reduced_states[-1])]:
                    result = solve_ivp(rhs,(interval_times[0],interval_times[-1]),state,method='DOP853',
                        t_eval=interval_times,rtol=rtol,atol=atol,max_step=step,first_step=min(step/2,interval_times[-1]-interval_times[0]))
                    if not result.success:
                        raise RuntimeError(name+': '+result.message)
                    calls[name] += result.nfev
                    results.append(result.y.T[1:])
                full_states.extend(results[0])
                reduced_states.extend(results[1])
                for instant,full_state,reduced_state in zip(interval_times[1:],results[0],results[1]):
                    rows.append(snapshot(system,chart,instant,full_state,reduced_state))
                path = evidence.output/(branch+'-accepted-'+str(interval+1)+'.npz')
                np.savez_compressed(path,times=times[:len(full_states)],full_states=np.array(full_states),
                    reduced_states=np.array(reduced_states),retained_indices=chart.retained)
                evidence.own(path,'outputs')
                diagnostic_path = evidence.output/(branch+'-diagnostics-'+str(interval+1)+'.json')
                diagnostic_path.write_text(json.dumps(rows,indent=2,allow_nan=False)+'\n',encoding='utf-8')
                evidence.own(diagnostic_path,'outputs')
                evidence.report['progress'] = dict(branch=branch,accepted_time=float(interval_times[-1]),
                    completed_intervals=interval+1,seconds=time.monotonic()-started,calls=calls)
                evidence.save()
                print(evidence.report['progress'],flush=True)
                if time.monotonic()-started>3600:
                    raise RuntimeError('One-hour per-branch safe checkpoint; accepted states preserved.')
            force_error = max(abs(row['force_difference']) for row in rows)
            full_drift = max(abs(row['full_energy']-rows[0]['full_energy']) for row in rows)
            reduced_drift = max(abs(row['reduced_energy']-rows[0]['reduced_energy']) for row in rows)
            evidence.check(branch+'_all_rows_finite',all(np.isfinite(value) for row in rows for value in row.values()))
            evidence.check(branch+'_same_state_force_law',all(row['force_identity_error']<2e-10
                and abs(row['same_state_force_difference'])<=row['same_state_force_bound']+2e-12 for row in rows))
            evidence.check(branch+'_defect_law_and_retained_EL',all(row['defect_identity_error']<2e-9
                and row['retained_EL_residual']<2e-7 for row in rows))
            evidence.check(branch+'_autonomous_action_energy_drift',max(full_drift,reduced_drift)<2e-9,
                dict(full=full_drift,reduced=reduced_drift))
            evidence.check(branch+'_no_source_window_exit',all(chart.window[0]<row['reduced_position']<chart.window[1] for row in rows))
            evidence.check(branch+'_integrated_drives_nonnegative',all(row['integrated_omitted_drive']>=0
                and row['integrated_kinetic_defect']>=0 for row in rows))
            evidence.report['cases'].append(dict(branch=branch,retained_count=chart.count,full_count=system.count,
                selection_survey=chart.survey,maximum_sampled_force_error=force_error,
                sampled_reduction_force_budget_met=bool(force_error<=2e-7),
                failing_sample_count=sum(not row['sampled_force_budget_met'] for row in rows),
                initial_preparation_energy_norm=rows[0]['reference_coordinate_phase_error'],
                final_reference_coordinate_phase_error=rows[-1]['reference_coordinate_phase_error'],
                maximum_source_position_error=max(row['source_position_error'] for row in rows),
                maximum_source_velocity_error=max(row['source_velocity_error'] for row in rows),
                maximum_clock_error=max(row['clock_error'] for row in rows),
                final_integrated_omitted_drive=rows[-1]['integrated_omitted_drive'],
                final_integrated_kinetic_defect=rows[-1]['integrated_kinetic_defect'],
                full_energy_drift=full_drift,reduced_energy_drift=reduced_drift,
                chart_minimum_gap_all_evaluations=chart.minimum_gap,
                chart_minimum_overlap_all_evaluations=chart.minimum_overlap,
                chart_evaluations=chart.evaluations,rhs_calls=calls,maximum_step=step,
                seconds=time.monotonic()-started,freely_evolved_reduced_trajectory=True,
                finite_time_window_only=True,all_time_certificate=False))
            evidence.save()
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()
