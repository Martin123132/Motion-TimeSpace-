from turnover_common import *


def measure_prediction(basis,solution,baseline,window):
    reader=ShapeReadout(basis,canonical=True)
    nodes,weights=special.roots_legendre(600)
    half=math.log(10)/2
    core=np.exp(math.log(.001*.01)/2+half*nodes)
    occupation=1/np.expm1(core)
    core_weight=weights*half*core**3*occupation*(1+occupation)/I3
    standard=np.column_stack([core/inherited.inherited.BETA-1,core*(core/np.tanh(core/2)-4)])
    templates=standard-core[:,None]*reader.shifts
    saved_profiles=np.stack([profile_at(float(coordinate),baseline,window) for coordinate in solution['coordinate']])
    true_core=np.einsum('fi,nik->nfk',basis.evaluate(core),saved_profiles)
    true_full=np.einsum('fi,nik->nfk',basis.values,saved_profiles)
    forecast_full=true_full.copy()
    interior=basis.nodes<=solution['frequency'][-1]
    forecast_core=[]
    source_only_core=[]
    source_only_full=true_full.copy()
    for epoch in range(65):
        forecast=interpolate.CubicSpline(np.log(solution['frequency']),solution['slope'][epoch],axis=0,extrapolate=False)
        target=interpolate.CubicSpline(np.log(solution['frequency']),solution['source_target'][epoch],axis=0,extrapolate=False)
        forecast_full[epoch,interior]=basis.nodes[interior,None]*forecast(np.log(basis.nodes[interior]))
        source_only_full[epoch,interior]=basis.nodes[interior,None]*target(np.log(basis.nodes[interior]))
        forecast_core.append(core[:,None]*forecast(np.log(core)))
        source_only_core.append(core[:,None]*target(np.log(core)))
    forecast_core=np.array(forecast_core)
    source_only_core=np.array(source_only_core)
    def residual(full,local):
        energy=np.einsum('i,nik->nk',reader.measure*reader.frequency,full)
        eta=energy/reader.capacity
        amplitude=np.einsum('ij,njk->nik',reader.amplitude_matrix,full)
        return local-core[None,:,None]*eta[:,None,:]-np.einsum('fi,nik->nfk',templates,amplitude)
    actual_residual=residual(true_full,true_core)
    predicted_residual=residual(forecast_full,forecast_core)
    target_residual=residual(source_only_full,source_only_core)
    squared=lambda value:np.einsum('i,nik,nik->nk',core_weight,value,value)
    actual_power=squared(actual_residual)
    predicted_power=squared(predicted_residual)
    target_power=squared(target_residual)
    peak=np.sqrt(actual_power.max(axis=0))
    local_error=np.sqrt(squared(forecast_core-true_core))
    residual_error=np.sqrt(squared(predicted_residual-actual_residual))
    target_error=np.sqrt(squared(target_residual-actual_residual))
    step=solution['coordinate'][1]-solution['coordinate'][0]
    slope=lambda value:(1.5*value[-1]-2*value[-2]+.5*value[-3])/step
    final_actual=slope(actual_power)
    final_predicted=slope(predicted_power)
    minimum_actual=solution['coordinate'][np.argmin(actual_power,axis=0)]/math.log(10)
    minimum_predicted=solution['coordinate'][np.argmin(predicted_power,axis=0)]/math.log(10)
    metrics=dict(field_error_over_residual_peak=(local_error.max(axis=0)/peak).tolist(),
        residual_error_over_peak=(residual_error.max(axis=0)/peak).tolist(),
        endpoint_residual_error_relative=(residual_error[-1]/np.sqrt(actual_power[-1])).tolist(),
        source_only_error_over_peak=(target_error.max(axis=0)/peak).tolist(),
        actual_minimum_epoch=minimum_actual.tolist(),predicted_minimum_epoch=minimum_predicted.tolist(),
        minimum_epoch_error=abs(minimum_actual-minimum_predicted).tolist(),
        late_power_slope_correct_sign=(np.sign(final_actual)==np.sign(final_predicted)).tolist(),
        final_power_slope_actual=final_actual.tolist(),final_power_slope_predicted=final_predicted.tolist(),
        predicted_to_actual_late_power_slope=(final_predicted/final_actual).tolist(),
        endpoint_predicted_to_actual_power=(predicted_power[-1]/actual_power[-1]).tolist(),
        correction_starts_at_saved_initial_state=True,later_test_band_used_as_driver=False)
    outputs=dict(core_frequency=core,core_measure=core_weight,true_core=true_core,predicted_core=forecast_core,
        true_residual=actual_residual,predicted_residual=predicted_residual,
        actual_power=actual_power,predicted_power=predicted_power,source_only_power=target_power,
        projected_actual_fullband_input=true_full,projected_predicted_fullband_input=forecast_full)
    return metrics,outputs


def main():
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('--model',choices=['heavy','cold'],required=True)
    parser.add_argument('--case',choices=['main640','main1280','wide1280','lower1280','hard005','coarse1280'],required=True)
    args=parser.parse_args()
    modest()
    settings=dict(minimum=1e-5,maximum=.05,hard_floor=.1,steps=1280,coarse=False)
    if args.case=='main640':
        settings['steps']=640
    if args.case=='wide1280':
        settings['maximum']=.1
    if args.case=='lower1280':
        settings['minimum']=2e-5
    if args.case=='hard005':
        settings['hard_floor']=.05
    if args.case=='coarse1280':
        settings['coarse']=True
    folder=ROOT/'runs'/f'{args.model}-{args.case}'
    folder.mkdir(parents=True,exist_ok=False)
    specification_path=BRANCH/'temperature-distortion-projection-20261012/results/projection/status.json'
    specification=json.loads(specification_path.read_text())['basis_specification']
    basis=infrared_ladder.ConsistentBasis(**specification)
    baseline,window,inputs=load_histories(args.model)
    chain=ancestors()
    for path in inputs+[specification_path]:
        verify_source(path,chain)
    solution,diagnostics,extra=reconstruct(basis,args.model,baseline,window,settings)
    for path in extra:
        verify_source(path,chain)
    metrics,readout=measure_prediction(basis,solution,baseline,window)
    checks=[]
    for key,limit in [('linear_solve',1e-10),('equilibrium',1e-10),('offdiagonal_negative',1e-14)]:
        value=diagnostics['errors'][key]
        checks.append(dict(name='STRUCTURE:'+key,value=value,limit=limit,passed=bool(value<=limit)))
    checks.append(dict(name='STRUCTURE:implicit M-matrix margin',value=diagnostics['implicit_diagonal_margin'],
        passed=diagnostics['implicit_diagonal_margin']>0))
    for column,label in enumerate(['baseline','join1','join2']):
        for key in ['field_error_over_residual_peak','residual_error_over_peak']:
            value=metrics[key][column]
            checks.append(dict(name='PREDICTION:'+key+':'+label,value=value,limit=.05,passed=value<=.05))
        value=metrics['minimum_epoch_error'][column]
        checks.append(dict(name='PREDICTION:turnaround:'+label,value=value,limit=.03,passed=value<=.03))
        checks.append(dict(name='PREDICTION:late-slope-sign:'+label,passed=metrics['late_power_slope_correct_sign'][column]))
    assert all(np.isfinite(value).all() for value in solution.values())
    assert all(np.isfinite(value).all() for value in readout.values())
    np.savez_compressed(folder/'prediction.npz',**solution,**readout)
    finish(folder,dict(checks=checks,model=args.model,settings=settings,diagnostics=diagnostics,metrics=metrics,
        structural_all_passed=all(row['passed'] for row in checks if row['name'].startswith('STRUCTURE:')),
        full_history_rerun=False,conditional_reconstruction=True,physical_cutoff_fitted=False,
        hard_driver_floor_is_numerical_holdout=True,future_test_band_in_forcing=False,
        photon_gas_feedback_applied=False,new_velocity_event_integrations=0,
        source54_columns_retained=True),__file__,[*inputs,*extra,specification_path])
    print(json.dumps(dict(case=args.model+'-'+args.case,diagnostics=diagnostics,
        primary_metrics={key:value[:3] for key,value in metrics.items() if isinstance(value,list)},
        failed=[row['name'] for row in checks if not row['passed']])),flush=True)


if __name__=='__main__':
    main()
