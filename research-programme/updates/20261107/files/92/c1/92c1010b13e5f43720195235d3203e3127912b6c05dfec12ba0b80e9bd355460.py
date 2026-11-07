from __future__ import annotations

from feedback_common import *


def main():
    modest()
    folder=ROOT/'results/feedback'
    folder.mkdir(parents=True,exist_ok=False)
    rows=[]
    inputs=[]
    states={}
    for wave in [.03,.1,1.]:
        reference=NativeSeed('lcdm',wave)
        normalization=float(reference.density[0,reference.final])
        for label in ['heavy','cold','lcdm']:
            model=NativeSeed(label,wave)
            initial=model.seed(normalization)
            result=solve_harmonics(initial,model.coefficients)
            loose=solve_harmonics(initial,model.coefficients,tight=False)
            alternate=NativeSeed(label,wave,'pchip')
            varied=solve_harmonics(initial,alternate.coefficients)
            transport=solve_harmonics(initial,model.coefficients,feedback=False)
            no_quantum_source=solve_harmonics(initial,model.coefficients,quadratic_pressure=False)
            endpoint=result.y[:,-1].reshape(4,-1)
            expected=np.array([model.density[:,model.final],model.velocity[:,model.final]])/normalization
            relative=np.abs(endpoint[:2]-expected)/np.maximum(np.abs(expected),1e-8)
            interpolation_error=float(np.max(abs(varied.y[:,-1].reshape(4,-1)[2:]-endpoint[2:]))/max(np.max(abs(endpoint[2:])),1e-8))
            samples=np.linspace(INITIAL,FINAL,257)
            parameters=np.array([model.coefficients(value)[2][-1] for value in samples])
            cb_weights=model.source_constants[:2]/sum(model.source_constants[:2])
            second_cb=float(np.dot(cb_weights,endpoint[2,:2]))
            transport_cb=float(np.dot(cb_weights,transport.y[:,-1].reshape(4,-1)[2,:2]))
            max_kappa=0. if model.mass is None else wave/(.5*model.mass)
            max_h_over_mass=0. if model.mass is None else float(max(np.exp(model.log_hubble(samples)-samples))/model.mass)
            native_volume_shift=float(max(abs(3*inherited.fields(label)[1]['potential'][model.mode,model.initial:model.final+1]))/normalization)
            row=dict(branch=label,k_Mpc_inverse=wave,species=model.species,common_normalization=normalization,
                endpoint=endpoint.tolist(),native_endpoint=expected.tolist(),
                max_native_linear_relative_error=float(relative.max()),native_errors=relative.tolist(),
                linear_projection_qualified=bool(relative.max()<.005),
                integration_change=float(np.max(abs(loose.y[:,-1]-result.y[:,-1]))),
                interpolation_quadratic_fraction=interpolation_error,interpolation_qualified=interpolation_error<.001,
                cb_second_density_coefficient=second_cb,cb_prescribed_velocity_coefficient=transport_cb,
                cb_feedback_increment=second_cb-transport_cb,
                cb_feedback_fraction_of_prescribed=(second_cb-transport_cb)/transport_cb,
                max_pressure_lambda=float(max(parameters)),max_kappa=max_kappa,max_H_over_M=max_h_over_mass,
                coordinate_volume_shift_over_common_normalization=native_volume_shift,
                omitted_quantum_source_endpoint_change=float(np.max(abs(no_quantum_source.y[:,-1]-result.y[:,-1]))),
                heavy_mass_Mpc_inverse=model.mass,second_order_initial_data='zero generated-response seed, not primordial second-order matching',
                full_native_second_order=False)
            rows.append(row)
            inputs+=model.paths
            states[(label,wave)]=(model,initial,result)
            np.savez_compressed(folder/(label+'-'+str(wave)+'.npz'),efold=samples,state=result.sol(samples),
                initial=initial,normalization=normalization,species=np.array(model.species))
            print(json.dumps({key:row[key] for key in ['branch','k_Mpc_inverse','max_native_linear_relative_error',
                'interpolation_quadratic_fraction','cb_second_density_coefficient','cb_feedback_fraction_of_prescribed']}),flush=True)
    numerical_controls=[]
    for growing in [False,True]:
        initial=np.array([1.,1.,float(growing),float(growing)])
        coefficients=lambda coordinate:(.5,np.array([1.5]),np.array([0.]))
        result=solve_harmonics(initial,coefficients,start=0.,end=.4)
        amplitude=math.exp(.4)
        exact=np.array([amplitude,amplitude,amplitude**2-(0 if growing else amplitude),amplitude**2-(0 if growing else amplitude)])
        numerical_controls.append(dict(name='EdS growing' if growing else 'EdS generated',error=float(max(abs(result.y[:,-1]-exact)))))
    periodic=[]
    for label in ['heavy','cold','lcdm']:
        model,initial,result=states[(label,.03)]
        prediction=result.y[:,-1].reshape(4,-1)[2:]
        for amplitude,count in [(.02,64),(.01,64),(.01,128)]:
            row=solve_periodic(initial,model.coefficients,amplitude,count)
            actual=np.array([row['second_density'],row['second_velocity']])
            row.update(branch=label,case='native-seeded .03',prediction=prediction.tolist(),
                max_coefficient_error=float(np.max(abs(actual-prediction))))
            periodic.append(row)
            print(json.dumps({key:row[key] for key in ['branch','amplitude','count','max_coefficient_error','nfev']}),flush=True)
    quantum_coefficients=lambda coordinate:(.5,np.array([1.5]),np.array([.08]))
    quantum_initial=np.array([1.,.8,0.,0.])
    quantum_result=solve_harmonics(quantum_initial,quantum_coefficients,start=0.,end=.25)
    quantum_wrong=solve_harmonics(quantum_initial,quantum_coefficients,start=0.,end=.25,quadratic_pressure=False)
    prediction=quantum_result.y[:,-1].reshape(4,-1)[2:]
    wrong=quantum_wrong.y[:,-1].reshape(4,-1)[2:]
    for amplitude,count in [(.02,64),(.01,64),(.01,128)]:
        row=solve_periodic(quantum_initial,quantum_coefficients,amplitude,count,start=0.,end=.25)
        actual=np.array([row['second_density'],row['second_velocity']])
        row.update(branch='quantum-sensitive control',case='dimensionless controlled coefficients, not a new MTS calibration',
            prediction=prediction.tolist(),max_coefficient_error=float(np.max(abs(actual-prediction))),
            omitted_quantum_source_error=float(np.max(abs(actual-wrong))))
        periodic.append(row)
        print(json.dumps({key:row[key] for key in ['branch','amplitude','count','max_coefficient_error','nfev']}),flush=True)
    finish(folder,dict(rows=rows,periodic_checks=periodic,analytic_controls=numerical_controls,
        new_parameters_fitted=0,actual_survey_refit=False,maximum_active_workers=1,
        approximation='Weak-field Gaussian canonical subfamily: c,b separate pressureless fluids, heavy leading NR pressure; other species background only.',
        second_order_initial_matching='No primordial claim: second-order perturbations initialized to zero at z=1.',
        source_projection='Proper Newtonian density seeds; not Stage60 metric-volume-corrected coordinate density.'),
        __file__,sorted(set(inputs))+list(folder.glob('*.npz')))
    print(json.dumps(dict(state='complete',branches=len(rows),periodic_tests=len(periodic))))


if __name__=='__main__':
    main()
