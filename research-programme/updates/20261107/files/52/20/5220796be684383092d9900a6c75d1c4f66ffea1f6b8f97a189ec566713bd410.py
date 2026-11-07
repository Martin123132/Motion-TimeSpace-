from stage160_common import *


def main():
    modest()
    folder=ROOT/'results/validation'
    folder.mkdir(parents=True,exist_ok=False)
    packet=verify_packet(ROOT/'results/analysis')
    assert packet['numerical_integrity_passed']
    assert all(row['name'].startswith('CONVERGENCE:') for row in packet['checks'] if not row['passed'])
    for filename,sha in packet['consumed_prior_hashes'].items():
        assert digest(filename)==sha,filename
    summary=json.loads((ROOT/'NUMERICAL-SUMMARY.json').read_text())
    data=read_npz(PARENT/'results/sources/source.npz')
    saved=read_npz(ROOT/'results/analysis/source-allowance.npz')
    checks=[dict(name='Analysis packets and all consumed prior hashes verified',passed=True)]
    inverse=np.linalg.inv(saved['mass'])
    def norm(value):
        return np.sqrt(np.maximum(np.einsum('...ij,ik,...kj->...j',value[...,1:-1,:],inverse,value[...,1:-1,:]),0))
    scale=norm(data['actual'])
    close(checks,'Independent inverse-mass source normalization',scale,saved['scale'],1e-10)
    for order in [5,6]:
        for site_index,site in enumerate(SITES):
            bank=read_npz(ROOT/'results/analysis'/f'{site}-order{order}-panels.npz')
            values=bank['frequency_values']
            expected=values.reshape(7,order,3,98,4).sum(axis=1)
            test(checks,f'Independent frequency partition:{site}:{order}',
                float(np.max(norm(expected-bank['panels'])/scale)),1e-10)
            assert np.array_equal(bank['panels'],saved['panels'+str(order)][:,site_index])
            for component_index,component in enumerate(COMPONENTS):
                test(checks,f'Independent archived full integral:{site}:{order}:{component}',
                    float(np.max(norm(bank['panels'][:,component_index].sum(axis=0)-full_component(data,site,order,component))/scale)),1e-10)
    delta65=saved['panels6']-saved['panels5']
    assert np.array_equal(delta65,saved['delta65'])
    latest=delta65.copy()
    latest[3]=data['order8_panel']-data['order7_reference_panel']
    latest[4]=data['new_panels'][1]-data['old_panels'][1]
    close(checks,'Independent mixed latest-step assembly',latest,saved['latest_steps'],1e-10)
    current=data['after_order8_full']
    assert np.array_equal(current,saved['latest_sources'])
    independent_norm=norm(latest)/scale
    close(checks,'Independent site/component norms',independent_norm,saved['latest_component_magnitudes'],1e-10)
    older=delta65.copy()
    older[3]=data['delta_panels'][0]
    observed=independent_norm[[3,4]]/(norm(older[[3,4]])/scale)
    observed[0]=np.maximum(observed[0],norm(older[3])/norm(delta65[3]))
    close(checks,'Independent contraction cap without clipping',observed,saved['observed_ratio_caps'],1e-10)
    assert summary['source']['geometric_scenario_available']==bool(np.all(observed<1))
    for route in ['local','cubic']:
        weights=weights_for(route)
        if route=='cubic':
            prediction=(data['start']+data['end'])/4-current[1]+1.5*current[2]
        else:
            prediction=latest_prediction(data,route)
        error=current[0]-prediction
        close(checks,'Independent predictor:'+route,prediction,saved[route+'_prediction'],1e-12)
        close(checks,'Independent residual:'+route,error,saved[route+'_error'],1e-12)
        numerator=norm(error)/scale
        denominator=norm(current[0])/scale
        record=summary['source']['routes'][route]
        close(checks,'Own-current-source discrepancy:'+route,numerator/denominator,record['relative_error'],1e-10)
        joint=sum(weights[site_index]*latest[:,site_index].sum(axis=1) for site_index in range(3))
        panel=norm(joint)/scale
        independent=(abs(weights)[None,:,None,None]*independent_norm).sum(axis=(0,1,2))
        cold=independent_norm[:,0].sum(axis=(0,1))
        scenarios=record['scenarios']
        for name,radius in [('matched_panel_last_step',panel.sum(axis=0)),('independent_last_step',independent)]:
            close(checks,'Independent conditional numerator:'+route+':'+name,radius,scenarios[name]['numerator_radius'],1e-10)
            close(checks,'Independent conditional denominator:'+route+':'+name,cold,scenarios[name]['cold_radius'],1e-10)
        if summary['source']['geometric_scenario_available']:
            radii=independent_norm.copy()
            radii[[3,4]]=independent_norm[[3,4]]*observed/(1-observed)
            close(checks,'Post-rule tail excludes computed increment:'+route,
                (abs(weights)[None,:,None,None]*radii).sum(axis=(0,1,2)),
                scenarios['selected_geometric_other_last_step']['numerator_radius'],1e-10)
        for name,scenario in scenarios.items():
            assert scenario['certified'] is False and scenario['endpoint_and_other_axis_radius'] is None
            if 'numerator_radius' in scenario:
                radius=np.asarray(scenario['numerator_radius'])
                cold_radius=np.asarray(scenario['cold_radius'])
                lower=np.where(numerator>radius,(numerator-radius)/(denominator+cold_radius),0.)
                close(checks,'Reverse-triangle conditional lower bound:'+route+':'+name,lower,scenario['lower_relative'],1e-10)
                close(checks,'Unmeasured numerator allowance:'+route+':'+name,
                    numerator-radius-.01*(denominator+cold_radius),scenario['extra_numerator_allowance_for1percent'],1e-10)
        assert all(item['radius'] is None for item in record['unresolved_axes'])
        assert record['global_error_bound'] is None
        assert record['pure_interpolation_error_identified'] is False
        assert set(record['remaining_error_shape_outside_observed_steps'])==set(map(str,SHAPE_CUTOFFS))
    synthetic=conditional_radius(np.asarray([2.,2.]),np.asarray([4.,4.]),np.asarray([.5,3.]),np.asarray([1.,1.]))
    assert np.array_equal(synthetic['lower_relative'],[.3,0.])
    checks.append(dict(name='Conditional-bound zero/positive controls and unspecified-axis blockers',passed=True))
    for model in ['heavy','cold']:
        for route in ['local','cubic']:
            for count in COUNTS:
                label=f'{model}-{route}-{count}'
                history=read_npz(ROOT/'results/analysis'/(label+'-history.npz'))
                older=read_npz(SOURCE156/'results/analysis'/(label+'-history.npz'))
                for quantity in ['photon','gas']:
                    expected=older[quantity+'_last_budget']+history[quantity+'_target_budget']
                    assert np.array_equal(expected,history[quantity+'_overlap_budget'])
                    assert summary['response']['records'][label]['state'][quantity]['future_error_radius_certified'] is False
                for match in [20,40]:
                    name=label+f'-m{match}'
                    current_readout=read_npz(PARENT/'results/comparison'/(name+'.npz'))
                    old_readout=read_npz(SOURCE156/'results/analysis'/(name+'-readout.npz'))
                    result=read_npz(ROOT/'results/analysis'/(name+'-readout.npz'))
                    assert np.array_equal(result['potential'][:,:1],current_readout['potential'][:,:1])
                    assert np.array_equal(result['amplitudes'][:,:1],current_readout['amplitudes'][:,:1])
                    assert np.array_equal(result['potential'][:,3:5],current_readout['potential'][:,3:5])
                    assert np.array_equal(result['potential'][:,1:3],old_readout['potential'][:,1:3])
                    close(checks,'Independent baseline-paired readout telescope:'+name,
                        result['potential'][:,3:5]-result['potential'][:,1:3],result['potential'][:,9:11],1e-8)
                    for position,quantity in enumerate(['mu','y','residual_norm']):
                        current_values=abs(result['amplitudes'][position]) if position<2 else result['residual_norm']
                        old_values=abs(old_readout['amplitudes'][position]) if position<2 else old_readout['residual_norm']
                        budget=current_values[11:23].reshape(6,2).sum(axis=0)+old_values[11:29].reshape(9,2).sum(axis=0)
                        ratio=current_values[9:11]/budget
                        claimed=summary['response']['records'][label]['readouts'][str(match)][quantity]['gap_over_overlapping_budget']
                        close(checks,'Independent overlapping sensitivity proxy:'+name+':'+quantity,ratio,claimed,1e-10)
    assert summary['new_physical_events']==summary['new_response_evolutions']==0
    assert summary['temperature_curve_changed'] is False
    assert summary['numerical_remainder_certified'] is False
    assert summary['response']['pure_latest_defect_response_available'] is False
    assert not list(ROOT.rglob('__pycache__'))
    scripts=sorted(ROOT.glob('*.py'))
    assert len(scripts)==4
    for path in scripts:
        compile(path.read_text(),str(path),'exec')
    largest=max(len(files) for directory,directories,files in os.walk(ROOT))
    assert largest<1000
    workbench=POST.parent/'formalization-workbench'
    assert not [path for path in workbench.rglob('*') if path.is_file() and path.stat().st_mtime>STARTED.timestamp()]
    checks.append(dict(name='Four scripts compile;no new events/evolutions;frozen curve;folder/workbench guards',passed=True))
    failures=[row for row in packet['checks'] if not row['passed']]
    finish(folder,dict(checks=checks,accepted_scope_verified=all(row['passed'] for row in checks),
        rehashed_prior_files=packet['rehashed_prior_files'],scientific_checks=len(packet['checks']),
        passing_scientific_checks=len(packet['checks'])-len(failures),retained_failure_names=[row['name'] for row in failures],
        compiled_scripts=4,largest_direct_file_count=largest,protected_workbench_recent_modified_file_count=0),
        __file__,[ROOT/'results/analysis/status.json',ROOT/'NUMERICAL-SUMMARY.json',*scripts])
    print(json.dumps(dict(validation=len(checks),passed=all(row['passed'] for row in checks),
        scientific=len(packet['checks']),retained_failures=len(failures))),flush=True)
    assert all(row['passed'] for row in checks)


if __name__=='__main__':
    main()
