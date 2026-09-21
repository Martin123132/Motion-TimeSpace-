from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_matrix_free_adjoint_20260917 import MatrixFreeAdjoint
from annular_flat_preassembled_flow_20260916 import FlatPreassembledFlow
from annular_locally_refined_source_action_20260916 import LocallyRefinedSourceAction
from annular_GR_causal_predictor_20260917 import HermiteReference,CausalPredictor,restrict_array_reads
from annular_local_spectral_step_20260916 import spectral_step
from scipy.integrate import solve_ivp
from datetime import datetime,timezone
import argparse
import hashlib
import json
import numpy as np
import time


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--label',required=True)
    parser.add_argument('--count',type=int,choices=[33,513],required=True)
    parser.add_argument('--terminal-time',type=float,choices=[.05,.21,.4],required=True)
    parser.add_argument('--tight',action='store_true')
    parser.add_argument('--compute-small-forward',action='store_true')
    parser.add_argument('--stop-at-utc',required=True)
    options=parser.parse_args()
    evidence=EvidenceRun(options.label,__file__)
    try:
        if options.compute_small_forward and options.count!=33:
            raise ValueError('Existing large forward calculations must not be rerun.')
        intake=evidence.root/'source-intake/navier-stokes/20260914'
        label='annular-small-adjoint-inputs-attempt01' if options.count==33 else 'annular-GR-causal-inputs-attempt01'
        folder=intake/label
        path=folder/'status.json'
        evidence.own(path)
        prepared=json.loads(path.read_text())
        evidence.check('GR_only_inputs_complete',prepared['state']=='complete' and not prepared['finite_future_trajectories_read'])
        path=folder/('GR-only-768-'+str(options.count)+'.npz')
        restrict_array_reads([path],evidence.output)
        evidence.own(path)
        evidence.check('input_hash',hashlib.sha256(path.read_bytes()).hexdigest()==prepared['outputs'][str(path.relative_to(evidence.root))])
        blocked=False
        try:
            with (intake/'annular-GR-causal-standard-attempt01/MTS-prediction.npz').open('rb'):
                pass
        except PermissionError:
            blocked=True
        evidence.check('preexisting_forward_predictions_blocked',blocked)
        with np.load(path,allow_pickle=False) as saved:
            times,states,derivatives,seed,oracle_forces=[saved[name].copy() for name in ['times','states','derivatives','original_initial','oracle_forces']]
        selected=times<=options.terminal_time+1e-14
        times,states,derivatives,oracle_forces=times[selected],states[selected],derivatives[selected],oracle_forces[selected]
        evidence.check('exact_terminal_knot',abs(times[-1]-options.terminal_time)<1e-14)
        reference=HermiteReference(times,states,derivatives)
        deadline=datetime.fromisoformat(options.stop_at_utc.replace('Z','+00:00')).timestamp()
        rtol,atol=(2e-12,2e-15) if options.tight else (2e-10,2e-13)
        evidence.report.update(arguments=vars(options),count=options.count,source_splits=8,degree=768,
            terminal_time=options.terminal_time,configuration=dict(rtol=rtol,atol=atol,step_multiplier=.5 if options.tight else 1.),
            original_action_unchanged=True,finite_future_trajectories_read=False,
            preexisting_forward_predictions_read=False,npz_read_allowlist=[str(path.relative_to(evidence.root))],
            fresh_small_forward_performed=options.compute_small_forward,
            all_modes_and_Gram_rows_retained=True,matrix_free_transpose=True,
            velocity_coordinate_adjoint_exactly_includes_off_solution_canonical_correction=True,
            force_fit=False,force_correction=False,physical_force_gate=2e-7,
            duality_gate=2e-9,control_gate=2e-10,full_GR_gate_upgraded=False,
            interval_arithmetic=False,known_benchmark_not_blind_new_experiment=True)
        evidence.save()
        base_system=LocallyRefinedSourceAction(options.count,False,background_mass=0.,source_splits=8)
        base_model=FlatPreassembledFlow(base_system)
        for gram in [False,True]:
            if time.time()>=deadline:
                evidence.report.update(state='paused_safe_checkpoint',reason='Before next branch; completed outputs preserved.')
                evidence.save()
                return
            branch='MTS' if gram else 'reference'
            system=LocallyRefinedSourceAction(options.count,gram,background_mass=0.,source_splits=8)
            model=FlatPreassembledFlow(system)
            adjoint=MatrixFreeAdjoint(model)
            terminal,terminal_derivative=reference.evaluate(times[-1])
            gradient=adjoint.force_gradient(terminal)
            dimension=len(terminal)
            estimate=spectral_step(system,terminal)
            evidence.check(branch+'_resolved_spectral_step',estimate['eigen_residual']<2e-8,estimate)
            step=estimate['maximum_step']*(.5 if options.tight else 1.)
            terminal_value=np.append(gradient,np.zeros(4))
            accepted=[terminal_value]
            sample_times=[times[-1]]
            evaluations=0
            started=time.monotonic()

            def rhs(instant,extended):
                state,derivative=reference.evaluate(instant)
                context=adjoint.context(state)
                covector=extended[:dimension]
                density_total=covector @ (context['value']['flow']-derivative)
                density_gram=float(adjoint.gram_density(state,covector,context)) if gram else 0.
                density_base=density_total-density_gram
                return np.concatenate([-adjoint.transpose(state,covector,context),
                    [-density_base,-density_gram,-abs(density_base),-abs(density_gram)]])

            for interval,(upper,lower) in enumerate(zip(times[:0:-1],times[-2::-1])):
                solution=solve_ivp(rhs,(upper,lower),accepted[-1],method='DOP853',rtol=rtol,atol=atol,
                    max_step=step,first_step=min(step/2,(upper-lower)/2),t_eval=[lower])
                if not solution.success:
                    raise RuntimeError(solution.message)
                accepted.append(solution.y[:,-1])
                sample_times.append(lower)
                evaluations+=solution.nfev
                if (interval+1)%10==0 or lower==0.:
                    destination=evidence.output/(branch+'-backward-accepted-'+str(interval+1)+'.npz')
                    np.savez_compressed(destination,times=np.array(sample_times),extended=np.array(accepted))
                    evidence.own(destination,'outputs')
                    evidence.report['progress']=dict(branch=branch,accepted_backward_time=float(lower),
                        rhs_evaluations=evaluations,seconds=time.monotonic()-started)
                    evidence.save()
                    print(evidence.report['progress'],flush=True)
                if time.time()>=deadline and lower>0.:
                    destination=evidence.output/(branch+'-safe-stop-'+str(interval+1)+'.npz')
                    np.savez_compressed(destination,times=np.array(sample_times),extended=np.array(accepted))
                    evidence.own(destination,'outputs')
                    evidence.report.update(state='paused_safe_checkpoint',reason='Accepted backward knot preserved before four-hour check-in.')
                    evidence.save()
                    return
            accepted=np.array(accepted[::-1])
            initial_error=seed-states[0]
            initial_pairing=float(accepted[0,:dimension] @ initial_error)
            base_integral,gram_integral,absolute_base,absolute_gram=map(float,accepted[0,dimension:])
            terminal_defect=float(model.evaluate(terminal)['force']-oracle_forces[-1])
            predicted_linear=terminal_defect+initial_pairing+base_integral+gram_integral
            decomposition=np.array([terminal_defect,initial_pairing,base_integral,gram_integral])
            evidence.check(branch+'_finite_full_backward_path',np.isfinite(accepted).all() and len(accepted)==len(times))
            evidence.check(branch+'_signed_integrals_bounded',abs(base_integral)<=absolute_base+2e-11
                and abs(gram_integral)<=absolute_gram+2e-11)
            forward_correction=None
            forward_error=None
            if options.compute_small_forward:
                predictor=CausalPredictor(model,reference)
                forward_correction=initial_error.copy()
                for lower,upper in zip(times[:-1],times[1:]):
                    solution=solve_ivp(predictor.rhs,(lower,upper),forward_correction,method='DOP853',
                        rtol=rtol,atol=atol/100,max_step=step,first_step=min(step/2,(upper-lower)/2),t_eval=[upper])
                    if not solution.success:
                        raise RuntimeError(solution.message)
                    forward_correction=solution.y[:,-1]
                forward_linear=float(terminal_defect+gradient @ forward_correction)
                forward_error=abs(forward_linear-predicted_linear)
                evidence.check(branch+'_new_small_forward_backward_duality',forward_error<2e-9,forward_error)
            destination=evidence.output/(branch+'-adjoint.npz')
            output=dict(times=times,covectors=accepted[:,:dimension],integrals=accepted[:,dimension:],
                terminal_force_gradient=gradient,initial_error=initial_error,decomposition=decomposition,
                predicted_linear_GR_difference=predicted_linear,oracle_force=oracle_forces[-1])
            if forward_correction is not None:
                output.update(new_small_forward_correction=forward_correction)
            np.savez_compressed(destination,**output)
            evidence.own(destination,'outputs')
            row=dict(branch=branch,count=options.count,terminal_time=options.terminal_time,
                terminal_instantaneous_defect=terminal_defect,initial_pairing=initial_pairing,
                base_residual_integral=base_integral,Gram_residual_integral=gram_integral,
                absolute_base_integral=absolute_base,absolute_Gram_integral=absolute_gram,
                predicted_linear_GR_difference=predicted_linear,new_small_duality_error=forward_error,
                rhs_evaluations=evaluations,seconds=time.monotonic()-started,spectral_step=estimate,
                frozen_before_preexisting_forward_read=True,all_physical_claims_false=True)
            evidence.report['cases'].append(row)
            evidence.save()
            print(row,flush=True)
        evidence.report['prediction_frozen_at']=datetime.now(timezone.utc).isoformat()
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()
