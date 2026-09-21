from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_GR_causal_predictor_20260917 import HermiteReference, CausalPredictor, restrict_array_reads
from annular_flat_preassembled_flow_20260916 import FlatPreassembledFlow
from annular_locally_refined_source_action_20260916 import LocallyRefinedSourceAction
from annular_local_spectral_step_20260916 import spectral_step
from scipy.integrate import solve_ivp
from datetime import datetime
import argparse
import hashlib
import json
import numpy as np
import time


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--label',required=True)
    parser.add_argument('--degree',type=int,choices=[384,512,768],default=768)
    parser.add_argument('--stride',type=int,choices=[1,2],default=1)
    parser.add_argument('--tight',action='store_true')
    parser.add_argument('--stop-at-utc',required=True)
    options = parser.parse_args()
    evidence = EvidenceRun(options.label,__file__)
    try:
        intake = evidence.root/'source-intake/navier-stokes/20260914'
        folder = intake/'annular-GR-causal-inputs-attempt01'
        path = folder/'status.json'
        evidence.own(path)
        prepared = json.loads(path.read_text())
        evidence.check('qualified_isolated_inputs_complete',prepared['state']=='complete' and not prepared['finite_future_trajectories_read']
            and all(row['passed'] for row in prepared['checks']))
        path = folder/('GR-only-'+str(options.degree)+'-513.npz')
        restrict_array_reads([path],evidence.output)
        blocked = False
        try:
            with (intake/'annular-joint-rectangle-attempt01/reference513-8-trajectory.npz').open('rb'):
                pass
        except PermissionError:
            blocked = True
        evidence.check('future_finite_trajectory_read_rejected',blocked)
        evidence.own(path)
        evidence.check('isolated_input_hash',hashlib.sha256(path.read_bytes()).hexdigest()==prepared['outputs'][str(path.relative_to(evidence.root))])
        with np.load(path,allow_pickle=False) as saved:
            times,states,derivatives,seed,oracle_forces = [saved[name].copy() for name in ['times','states','derivatives','original_initial','oracle_forces']]
        reference = HermiteReference(times[::options.stride],states[::options.stride],derivatives[::options.stride])
        deadline = datetime.fromisoformat(options.stop_at_utc.replace('Z','+00:00')).timestamp()
        if time.time()>=deadline:
            raise ValueError('Safe-stop deadline has already passed.')
        evidence.report.update(arguments=vars(options),finite_future_trajectories_read=False,
            npz_read_allowlist=[str(path.relative_to(evidence.root))],known_benchmark_not_blind_new_experiment=True,
            original_action_unchanged=True,all_modes_and_Gram_rows_retained=True,force_fit=False,
            retrospective_force_subtraction=False,count=513,source_splits=8,final_time=.4,
            configuration=dict(rtol=2e-12 if options.tight else 2e-10,atol=2e-16 if options.tight else 2e-14,
                spectral_step_multiplier=.5 if options.tight else 1.,degree=options.degree,stride=options.stride),
            reconstruction_derivative_is_own_exact_derivative=True,
            original_initial_projection_error_retained=True,physical_force_gate=2e-7,numerical_control_gate=2e-8)
        evidence.save()
        for gram in [False,True]:
            if time.time()>=deadline:
                evidence.report.update(state='paused_safe_checkpoint',reason='Before next branch; previous predictions preserved.')
                evidence.save()
                return
            branch = 'MTS' if gram else 'reference'
            system = LocallyRefinedSourceAction(513,gram,background_mass=0.,source_splits=8)
            model = FlatPreassembledFlow(system)
            predictor = CausalPredictor(model,reference)
            corrections = [seed-reference.evaluate(0.)[0]]
            history,evaluations = [],0
            started = time.monotonic()
            for interval in range(8):
                beginning,ending = times[10*interval],times[10*interval+10]
                estimate = spectral_step(system,reference.evaluate(beginning)[0])
                if estimate['eigen_residual']>=2e-8:
                    raise RuntimeError('Unresolved original stiffness.')
                step = estimate['maximum_step']*(.5 if options.tight else 1.)
                pieces = reference.times[(reference.times>=beginning-1e-14)&(reference.times<=ending+1e-14)]
                for lower,upper in zip(pieces[:-1],pieces[1:]):
                    selected = times[(times>=lower-1e-14)&(times<=upper+1e-14)]
                    solution = solve_ivp(predictor.rhs,(lower,upper),corrections[-1],t_eval=selected,method='DOP853',
                        rtol=evidence.report['configuration']['rtol'],atol=evidence.report['configuration']['atol'],
                        max_step=step,first_step=min(step/2,(upper-lower)/2))
                    if not solution.success:
                        raise RuntimeError(solution.message)
                    corrections.extend(solution.y.T[1:])
                    evaluations += solution.nfev
                if len(corrections)!=10*interval+11:
                    raise RuntimeError('Missing or duplicated accepted prediction samples.')
                history.append(dict(**estimate,used_step=step))
                destination = evidence.output/(branch+'-accepted-'+str(interval+1)+'.npz')
                np.savez_compressed(destination,times=times[:len(corrections)],corrections=np.array(corrections))
                evidence.own(destination,'outputs')
                evidence.report['progress'] = dict(branch=branch,accepted_time=float(ending),seconds=time.monotonic()-started,
                    rhs_evaluations=evaluations)
                evidence.report['active_spectral_history'] = history
                evidence.save()
                print(evidence.report['progress'],flush=True)
                if time.time()>=deadline and interval<7:
                    evidence.report.update(state='paused_safe_checkpoint',reason='Accepted prediction saved before four-hour check-in.')
                    evidence.save()
                    return
            corrections = np.array(corrections)
            predictions = [predictor.outputs(instant,correction) for instant,correction in zip(times,corrections)]
            predicted_states = np.array([value['state'] for value in predictions])
            force_linear = np.array([value['linear_force'] for value in predictions])
            force_reconstructed = np.array([value['reconstructed_force'] for value in predictions])
            nonlinear_flow = np.array([value['nonlinear_flow_remainder'] for value in predictions])
            energies = np.array([value['energy'] for value in predictions])
            evidence.check(branch+'_finite_positive_inertia',np.isfinite(predicted_states).all()
                and np.isfinite(nonlinear_flow).all() and all(value['schur']>0. for value in predictions))
            preparation_error = float(np.max(abs(predicted_states[0]-seed)))
            evidence.check(branch+'_original_initial_state',preparation_error<2e-14,preparation_error)
            evidence.check(branch+'_full_original_horizon',len(corrections)==81 and times[-1]==.4)
            destination = evidence.output/(branch+'-prediction.npz')
            np.savez_compressed(destination,times=times,states=predicted_states,corrections=corrections,
                force_linear=force_linear,force_reconstructed=force_reconstructed,nonlinear_flow_remainder=nonlinear_flow,
                oracle_forces=oracle_forces,energies=energies)
            evidence.own(destination,'outputs')
            row = dict(branch=branch,count=513,splits=8,degree=options.degree,stride=options.stride,
                seconds=time.monotonic()-started,rhs_evaluations=evaluations,spectral_history=history,
                maximum_correction=float(np.max(abs(corrections))),
                maximum_nonlinear_flow_remainder=float(np.max(abs(nonlinear_flow))),
                maximum_linear_vs_reconstructed_force=float(np.max(abs(force_linear-force_reconstructed))),
                energy_relative_drift=float(np.max(abs(energies-energies[0]))/abs(energies[0])),
                maximum_predicted_GR_force_difference=float(np.max(abs(force_reconstructed-oracle_forces))),
                future_finite_states_opened=False)
            evidence.report['cases'].append(row)
            evidence.save()
            print({key:value for key,value in row.items() if key!='spectral_history'},flush=True)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()
