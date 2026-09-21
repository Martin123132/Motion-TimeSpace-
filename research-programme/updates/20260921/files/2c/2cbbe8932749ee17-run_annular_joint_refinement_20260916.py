from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_flat_preassembled_flow_20260916 import FlatPreassembledFlow
from annular_locally_refined_source_action_20260916 import LocallyRefinedSourceAction
from annular_local_spectral_step_20260916 import spectral_step
from run_annular_source_fitted_crossing_20260915 import initial, diagnostics
from scipy.integrate import solve_ivp
from datetime import datetime, timezone
import argparse
import json
import numpy as np
import time


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--label',required=True)
    parser.add_argument('--cases',nargs='+',default=['257:4','257:8','513:4','513:8'])
    parser.add_argument('--tight',action='store_true')
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
        deadline = datetime(2026,9,16,20,35,tzinfo=timezone.utc).timestamp()
        for specification in options.cases:
            count,splits = map(int,specification.split(':'))
            for gram in [False,True]:
                branch = 'MTS' if gram else 'reference'
                system = LocallyRefinedSourceAction(count,gram,background_mass=0.,source_splits=splits)
                model = FlatPreassembledFlow(system)
                states,evaluations,history = [initial(system)],0,[]
                started = time.monotonic()
                for interval in range(8):
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
                if time.time()>deadline:
                    evidence.report.update(state='paused_safe_checkpoint',reason='Four-hour check-in guard; completed cases preserved.')
                    evidence.save()
                    return
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()
