from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_full_force_linearization_20260916 import FullForceLinearization
from annular_force_adjoint_response_20260916 import ResponsePath
from annular_locally_refined_source_action_20260916 import LocallyRefinedSourceAction
from scipy.integrate import solve_ivp
from scipy.linalg import eigvalsh
from datetime import datetime, timezone
import argparse
import hashlib
import json
import numpy as np
import time


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--tight', action='store_true')
    options = parser.parse_args()
    label = 'tight' if options.tight else 'standard'
    evidence = EvidenceRun('annular-causal-'+label+'-attempt01', __file__)
    try:
        inputs = evidence.root/'source-intake/navier-stokes/20260914/annular-causal-inputs-attempt01'
        evidence.own(inputs/'status.json')
        status = json.loads((inputs/'status.json').read_text())
        evidence.check('isolated_input_pack_complete', status['state']=='complete' and all(row['passed'] for row in status['checks']))
        config = status['configuration']
        rtol = config['tight_rtol' if options.tight else 'standard_rtol']
        atol = config['tight_atol' if options.tight else 'standard_atol']
        evidence.report.update(configuration=dict(rtol=rtol, atol=atol, tight=options.tight, final_time=.005),
            future_full_arrays_loaded=False, force_fit=False, original_action_unchanged=True,
            original_GR_failures_unchanged=True, all_time_error_certificate=False)
        for branch in ['reference', 'MTS']:
            path = inputs/(branch+'-predictor-inputs.npz')
            evidence.own(path)
            key = str(path.relative_to(evidence.root))
            evidence.check(branch+'_input_hash', hashlib.sha256(path.read_bytes()).hexdigest()==status['outputs'][key])
            with np.load(path, allow_pickle=False) as saved:
                evidence.check(branch+'_strict_input_schema', set(saved.files)==set(status['predictor_keys']))
                data = {key:saved[key].copy() for key in saved.files}
            system = LocallyRefinedSourceAction(129, branch=='MTS', background_mass=0., source_splits=8)
            model = FullForceLinearization(system)
            matrices = model.matrices(data['initial_state'][system.count])[0]
            omega = np.sqrt(eigvalsh(matrices['stiffness'], matrices['mass'])[-1])
            cap = (.25 if options.tight else .5)/omega
            for stride in ([1] if options.tight else [1,2]):
                started = time.monotonic()
                times = data['times'][::stride]
                reduced = ResponsePath(times, data['reduced_states'][::stride], data['reduced_derivatives'][::stride])
                correction = data['initial_state']-reduced.value(0.)
                corrections = [correction.copy()]
                evaluations = 0

                def rhs(instant, perturbation):
                    values = model.evaluate(reduced.value(instant), True)
                    return values['jacobian'] @ perturbation+values['flow']-reduced.derivative(instant)

                for interval, (left, right) in enumerate(zip(times[:-1], times[1:])):
                    result = solve_ivp(rhs, (left,right), correction, method='DOP853', rtol=rtol, atol=atol,
                        max_step=cap, first_step=min(cap/2, (right-left)/2))
                    if not result.success:
                        raise RuntimeError(result.message)
                    correction = result.y[:,-1]
                    corrections.append(correction.copy())
                    evaluations += result.nfev
                    if (interval+1)%40==0 or interval==len(times)-2:
                        target = evidence.output/(branch+'-stride'+str(stride)+'-accepted-'+str(interval+1)+'.npz')
                        np.savez_compressed(target, times=times[:len(corrections)], corrections=np.array(corrections))
                        evidence.own(target, 'outputs')
                        evidence.report['progress'] = dict(branch=branch, stride=stride, accepted_time=float(right),
                            seconds=time.monotonic()-started, evaluations=evaluations)
                        evidence.save()
                        print(evidence.report['progress'], flush=True)
                        if time.monotonic()-started>3600:
                            raise RuntimeError('One-hour case safe checkpoint; accepted chunks preserved.')
                corrections = np.array(corrections)
                correction_rates = np.array([rhs(instant, correction) for instant,correction in zip(times,corrections)])
                correction_path = ResponsePath(times, corrections, correction_rates)
                samples = np.sort(np.concatenate([times,(times[:-1]+times[1:])/2]))
                arrays = {key:[] for key in ['reduced_states', 'corrections', 'corrected_states', 'corrected_forces',
                    'linear_forces', 'nominal_forces', 'nonlinear_residuals', 'half_nonlinear_residuals',
                    'correction_reconstruction_residuals', 'total_residuals', 'schur', 'energy']}
                identity_error = 0.
                for instant in samples:
                    nominal = reduced.value(instant)
                    correction = correction_path.value(instant)
                    corrected = nominal+correction
                    values = model.evaluate(nominal, True)
                    actual = model.evaluate(corrected)
                    half = model.evaluate(nominal+correction/2)
                    linear_flow = values['jacobian'] @ correction
                    nonlinear = actual['flow']-values['flow']-linear_flow
                    reconstruction = correction_path.derivative(instant)-(linear_flow+values['flow']-reduced.derivative(instant))
                    total = actual['flow']-reduced.derivative(instant)-correction_path.derivative(instant)
                    identity_error = max(identity_error,float(np.max(abs(total-nonlinear+reconstruction))))
                    coordinates, rates = np.split(corrected[:-1],2)
                    row = dict(reduced_states=nominal, corrections=correction, corrected_states=corrected,
                        corrected_forces=actual['force'], nominal_forces=values['force'],
                        linear_forces=values['force']+values['force_gradient'] @ correction,
                        nonlinear_residuals=nonlinear, half_nonlinear_residuals=half['flow']-values['flow']-linear_flow/2,
                        correction_reconstruction_residuals=reconstruction, total_residuals=total,
                        schur=actual['schur'], energy=system.energy(instant,coordinates,rates))
                    for key,value in row.items():
                        arrays[key].append(value)
                arrays = {key:np.array(value) for key,value in arrays.items()}
                prefix = branch+'-stride'+str(stride)
                evidence.check(prefix+'_finite_predictor_outputs', all(np.isfinite(value).all() for value in arrays.values()))
                initial_error = float(np.max(abs(arrays['corrected_states'][0]-data['initial_state'])))
                evidence.check(prefix+'_original_initial_state_recovered', initial_error<2e-15, initial_error)
                evidence.check(prefix+'_residual_identity', identity_error<1e-10, identity_error)
                evidence.check(prefix+'_positive_schur', np.min(arrays['schur'])>0.)
                destination = evidence.output/(prefix+'-prediction.npz')
                np.savez_compressed(destination, times=samples, knot_times=times, **arrays)
                evidence.own(destination, 'outputs')
                row = dict(branch=branch, stride=stride, seconds=time.monotonic()-started, evaluations=evaluations,
                    maximum_step=cap, sample_count=len(samples), identity_error=identity_error,
                    maximum_measured_nonlinear_residual=float(np.max(abs(arrays['nonlinear_residuals']))),
                    maximum_measured_reconstruction_residual=float(np.max(abs(arrays['correction_reconstruction_residuals']))),
                    maximum_energy_drift=float(np.max(abs(arrays['energy']-arrays['energy'][0]))),
                    nonlinear_remainder_is_measured_not_uniform_bound=True)
                evidence.report['cases'].append(row)
                evidence.save()
        manifest = evidence.output/'predictions-sealed.json'
        manifest.write_text(json.dumps(dict(sealed_at=datetime.now(timezone.utc).isoformat(),
            outputs=evidence.report['outputs'], inputs=evidence.report['inputs'], future_full_arrays_loaded=False,
            input_isolation_not_blind_discovery=True), indent=2)+'\n', encoding='utf-8')
        evidence.own(manifest, 'outputs')
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()
