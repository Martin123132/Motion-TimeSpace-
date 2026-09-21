from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_full_force_linearization_20260916 import FullForceLinearization
from annular_force_adjoint_response_20260916 import AdjointResponse
from annular_locally_refined_source_action_20260916 import LocallyRefinedSourceAction
from scipy.integrate import solve_ivp
import argparse
import numpy as np
import json
import time


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--tight',action='store_true')
    options = parser.parse_args()
    evidence = EvidenceRun('annular-force-adjoint-'+('tight' if options.tight else 'response')+'-attempt01',__file__)
    try:
        intake = evidence.root/'source-intake/navier-stokes/20260914'
        path_folder = intake/'annular-force-response-paths-attempt01'
        for path in [path_folder/'status.json',intake/'annular-full-force-linearization-attempt01/status.json']:
            evidence.own(path)
            status = json.loads(path.read_text())
            evidence.check(path.parent.name+'_complete',status['state']=='complete' and all(row['passed'] for row in status['checks']))
        settings_path = intake/'annular-anchored-moving-tight-attempt01/status.json'
        evidence.own(settings_path)
        settings = json.loads(settings_path.read_text())
        evidence.report.update(configuration=dict(tight=options.tight,identity_tolerance=2e-10,attribution_tolerance=2e-10,
            rtol=2e-12 if options.tight else 2e-10,adjoint_atol=2e-14 if options.tight else 2e-12,
            integral_atol=1e-17 if options.tight else 1e-15),
            original_GR_gates_unchanged=True,original_action_unchanged=True,
            all_time_error_certificate=False,nonlinear_remainder_bound=False,scope='Endpoint-force response on the saved short finite-action test.')
        evidence.save()
        for branch in ['reference','MTS']:
            path = path_folder/(branch+'-physical-paths.npz')
            evidence.own(path)
            with np.load(path) as saved:
                data = {key:saved[key].copy() for key in saved.files}
            model = FullForceLinearization(LocallyRefinedSourceAction(129,branch=='MTS',background_mass=0.,source_splits=8))
            step = next(row for row in settings['cases'] if row['branch']==branch)['maximum_step']
            step *= .5 if options.tight else 1.
            for stride in ([1] if options.tight else [2,1]):
                started = time.monotonic()
                response = AdjointResponse(model,data,stride)
                dimension = response.dimension
                initial = np.concatenate([response.terminal,np.zeros(4)])
                atol = np.append(np.full(dimension,2e-14 if options.tight else 2e-12),np.full(4,1e-17 if options.tight else 1e-15))
                result = solve_ivp(response.backward,(data['times'][-1],0.),initial,method='DOP853',
                    rtol=2e-12 if options.tight else 2e-10,atol=atol,max_step=step,first_step=step/2)
                evidence.check(branch+str(stride)+'_adjoint_integrated',result.success)
                row = response.summarize(result)
                row.update(branch=branch,stride=stride,seconds=time.monotonic()-started)
                row['physical_linear_attribution_qualified'] = bool(row['physical_linear_prediction_error']<2e-10
                    and abs(row['net_reconstruction_contribution'])<2e-10 and abs(row['total_measured_nonlinear_remainder'])<2e-10)
                evidence.check(branch+str(stride)+'_complete_identity_closes',row['exact_identity_closure_error']<2e-10,row['exact_identity_closure_error'])
                evidence.check(branch+str(stride)+'_clock_adjoint_decoupling_derived_not_dropped',row['initial_adjoint_clock_component']==0.)
                if stride==1 and not options.tight:
                    perturbations = np.zeros((3,dimension))
                    perturbations[0] = response.initial_error
                    perturbations[2] = response.initial_error
                    tangent = solve_ivp(response.tangent,(0.,data['times'][-1]),perturbations.ravel(),method='DOP853',
                        rtol=2e-10,atol=1e-17,max_step=step,first_step=step/2)
                    evidence.check(branch+'_tangent_integrated',tangent.success)
                    projections = tangent.y[:,-1].reshape(3,dimension) @ response.terminal
                    expected = np.array([row['initial_preparation_linear_response'],row['accumulated_motion_linear_response'],
                        row['initial_preparation_linear_response']+row['accumulated_motion_linear_response']+row['net_reconstruction_contribution']])
                    row['tangent_adjoint_maximum_difference'] = float(np.max(abs(projections-expected)))
                    row['forward_tangent_projections'] = projections.tolist()
                    evidence.check(branch+'_independent_tangent_adjoint_duality',row['tangent_adjoint_maximum_difference']<2e-10,row['tangent_adjoint_maximum_difference'])
                path = evidence.output/(branch+'-stride'+str(stride)+'-adjoint.npz')
                np.savez_compressed(path,times=result.t,adjoint=result.y,terminal_force_gradient=response.terminal,initial_error=response.initial_error)
                evidence.own(path,'outputs')
                evidence.report['cases'].append(row)
                evidence.save()
                print(dict(branch=branch,stride=stride,seconds=time.monotonic()-started,linear_error=row['physical_linear_prediction_error'],
                    identity_error=row['exact_identity_closure_error'],numerical=row['net_reconstruction_contribution']),flush=True)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()
