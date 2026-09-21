from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_flat_preassembled_flow_20260916 import FlatPreassembledFlow
from annular_locally_refined_source_action_20260916 import LocallyRefinedSourceAction
from annular_local_spectral_step_20260916 import spectral_step
from run_annular_source_fitted_crossing_20260915 import initial, diagnostics
from scipy.integrate import solve_ivp
from datetime import datetime, timezone
import argparse
import json
import hashlib
import numpy as np
import time


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--label',required=True)
    parser.add_argument('--cases',nargs='+',default=['257:4','257:8','513:4','513:8'])
    parser.add_argument('--tight',action='store_true')
    parser.add_argument('--stop-at-utc',required=True)
    parser.add_argument('--resume-label',required=True)
    options = parser.parse_args()
    evidence = EvidenceRun(options.label,__file__)
    try:
        intake = evidence.root/'source-intake/navier-stokes/20260914'
        path = intake/'annular-flat-preassembly-attempt01/status.json'
        evidence.own(path)
        status = json.loads(path.read_text())
        evidence.check('unchanged_action_preassembly_qualified',status['state']=='complete' and all(row['passed'] for row in status['checks']))
        evidence.report.update(arguments=vars(options),original_action_unchanged=True,original_initial_function_unchanged=True,
            all_modes_and_Gram_rows_retained=True,force_correction=False,reduced_solver=False,
            full_source_momentum_retained=True,background_mass=0.,final_time=.4,
            configuration=dict(rtol=2e-12 if options.tight else 2e-10,atol=2e-14 if options.tight else 2e-12,
                spectral_step_multiplier=.5 if options.tight else 1.,samples=81),
            prespecified_accuracy_gates=dict(field=.005,source=5e-7,velocity=2e-5,clock=2e-7,
                force_absolute=2e-7,force_relative=.02),
            fixed_base_local_refinement_is_action_nested=True,cross_base_Gram_actions_not_exactly_nested=True)
        evidence.save()
        times = np.linspace(0.,.4,81)
        previous_folder = intake/options.resume_label
        previous_path = previous_folder/'status.json'
        previous = json.loads(previous_path.read_text())
        evidence.own(previous_path)
        evidence.check('predecessor_paused_same_configuration',previous['state']=='paused_safe_checkpoint'
            and all(row['passed'] for row in previous['checks'])
            and previous['arguments']['cases']==options.cases and previous['arguments']['tight']==options.tight
            and previous['configuration']==evidence.report['configuration'])
        for table in ['inputs','outputs']:
            for name,expected in previous[table].items():
                source_path = evidence.root/name
                if hashlib.sha256(source_path.read_bytes()).hexdigest()!=expected:
                    raise RuntimeError('Changed predecessor input/output: '+name)
                evidence.own(source_path)
        evidence.check('predecessor_hashes_intact',True)
        evidence.report['resumed_from'] = options.resume_label
        completed_cases = {(row['branch'],row['count'],row['splits']):row for row in previous['cases']}
        deadline = datetime.fromisoformat(options.stop_at_utc.replace('Z','+00:00')).timestamp()
        if time.time() >= deadline:
            raise ValueError('Safe-stop deadline has already passed.')
        for specification in options.cases:
            count,splits = map(int,specification.split(':'))
            for gram in [False,True]:
                if time.time() >= deadline:
                    evidence.report.update(state='paused_safe_checkpoint',reason='Before next case; previous cases preserved.')
                    evidence.save()
                    return
                branch = 'MTS' if gram else 'reference'
                key = (branch,count,splits)
                if key in completed_cases:
                    prefix = branch+str(count)+'-'+str(splits)
                    old_checks = [row for row in previous['checks'] if row['name'].startswith(prefix+'_')]
                    evidence.check(prefix+'_completed_case_preserved',len(old_checks)==4 and all(row['passed'] for row in old_checks))
                    source_path = previous_folder/(prefix+'-trajectory.npz')
                    destination = evidence.output/source_path.name
                    destination.write_bytes(source_path.read_bytes())
                    evidence.own(destination,'outputs')
                    evidence.report['cases'].append(completed_cases[key])
                    evidence.save()
                    continue
                system = LocallyRefinedSourceAction(count,gram,background_mass=0.,source_splits=splits)
                model = FlatPreassembledFlow(system)
                states,evaluations,history = [initial(system)],0,[]
                elapsed_previous = 0.
                progress = previous.get('progress',{})
                if (progress.get('branch'),progress.get('count'),progress.get('splits'))==key:
                    history = previous['active_spectral_history']
                    interval_count = len(history)
                    path = previous_folder/(branch+'-'+str(count)+'-'+str(splits)+'-accepted-'+str(interval_count)+'.npz')
                    with np.load(path,allow_pickle=False) as saved:
                        accepted_times,accepted_states = saved['times'].copy(),saved['states'].copy()
                    evidence.check(branch+'_accepted_prefix_valid',0<interval_count<8
                        and np.array_equal(accepted_times,times[:10*interval_count+1])
                        and accepted_states.shape==(len(accepted_times),2*system.count+3)
                        and np.isfinite(accepted_states).all())
                    evidence.check(branch+'_original_initial_state_preserved',np.array_equal(accepted_states[0],initial(system)))
                    states = list(accepted_states)
                    evaluations = progress['rhs_evaluations']
                    elapsed_previous = progress['seconds']
                started = time.monotonic()-elapsed_previous
                for interval in range(len(history),8):
                    estimate = spectral_step(system,states[-1])
                    if estimate['eigen_residual']>=2e-8:
                        raise RuntimeError('Unresolved original-action stiffness.')
                    step = estimate['maximum_step']*(.5 if options.tight else 1.)
                    interval_times = times[10*interval:10*interval+11]
                    solution = solve_ivp(model.rhs,(interval_times[0],interval_times[-1]),states[-1],t_eval=interval_times,
                        method='DOP853',rtol=evidence.report['configuration']['rtol'],atol=evidence.report['configuration']['atol'],
                        max_step=step,first_step=step/2)
                    if not solution.success:
                        raise RuntimeError(solution.message)
                    states.extend(solution.y.T[1:])
                    evaluations += solution.nfev
                    history.append(dict(**estimate,used_step=step))
                    evidence.report['active_spectral_history'] = history
                    destination = evidence.output/(branch+'-'+str(count)+'-'+str(splits)+'-accepted-'+str(interval+1)+'.npz')
                    np.savez_compressed(destination,times=times[:len(states)],states=np.array(states))
                    evidence.own(destination,'outputs')
                    evidence.report['progress'] = dict(branch=branch,count=count,splits=splits,accepted_time=float(interval_times[-1]),
                        seconds=time.monotonic()-started,rhs_evaluations=evaluations)
                    evidence.save()
                    print(evidence.report['progress'],flush=True)
                    if time.time()>deadline and interval<7:
                        evidence.report.update(state='paused_safe_checkpoint',reason='Four-hour check-in guard; accepted states preserved.')
                        evidence.save()
                        return
                states = np.array(states)
                values = [model.evaluate(state,True) for state in states]
                forces = np.array([value['force'] for value in values])
                energies = np.array([value['energy'] for value in values])
                original = diagnostics(system,times[::10],states[::10])
                canonical_errors = []
                for instant,state,value in zip(times[::10],states[::10],forces[::10]):
                    coordinates,rates = np.split(state[:-1],2)
                    acceleration = system.acceleration(instant,coordinates,rates)
                    canonical_errors.append(abs(float(value-system.source_mass*acceleration[-1]/(1-rates[-1]**2)**1.5)))
                prefix = branch+str(count)+'-'+str(splits)
                evidence.check(prefix+'_finite_positive_inertia',np.isfinite(states).all() and all(value['schur']>0. for value in values))
                evidence.check(prefix+'_original_EL_and_map',original['maximum_euler_residual']<2e-10 and original['minimum_jacobian']>.9,original)
                energy_drift = float(np.max(abs(energies-energies[0]))/abs(energies[0]))
                evidence.check(prefix+'_energy',energy_drift<2e-8,energy_drift)
                evidence.check(prefix+'_original_canonical_force',max(canonical_errors)<2e-11,max(canonical_errors))
                destination = evidence.output/(prefix+'-trajectory.npz')
                np.savez_compressed(destination,times=times,states=states,forces=forces,energies=energies)
                evidence.own(destination,'outputs')
                source_index = np.searchsorted(system.edges,system.anchor)
                local_widths = [system.anchor-system.edges[source_index-1],system.edges[source_index+1]-system.anchor]
                row = dict(branch=branch,count=count,splits=splits,scalar_dofs=system.count,local_widths=local_widths,
                    bulk_spacing=system.gram_spacing,seconds=time.monotonic()-started,rhs_evaluations=evaluations,
                    spectral_history=history,energy_relative_drift=energy_drift,
                    maximum_original_force_difference=max(canonical_errors),final_force=float(forces[-1]),
                    original_diagnostics=original)
                evidence.report['cases'].append(row)
                evidence.save()
                print(dict(branch=branch,count=count,splits=splits,seconds=row['seconds'],final_force=row['final_force']),flush=True)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()
