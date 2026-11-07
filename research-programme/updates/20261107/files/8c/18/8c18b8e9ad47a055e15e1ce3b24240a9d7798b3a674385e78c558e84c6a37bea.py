from stage156_common import *


def independent_weights(phase,route):
    nodes=[0.,.25,.5,.75,1.]
    selected=range(5) if route=='cubic' else [0,1,2] if phase<=.5 else [2,3,4]
    result=np.zeros(5)
    for index in selected:
        value=1.
        for other in selected:
            if index!=other:
                value*=(phase-nodes[other])/(nodes[index]-nodes[other])
        result[index]=value
    return result


def main():
    modest()
    folder=ROOT/'results/validation'
    folder.mkdir(parents=True,exist_ok=False)
    chain=ancestors()
    hashes={}
    def hashed(path):
        path=Path(path).resolve()
        if str(path) not in hashes:
            hashes[str(path)]=digest(path)
        return hashes[str(path)]
    for filename,sha in chain[PARENT/'results/stage-integrity.json']['file_hashes'].items():
        assert hashed(PARENT/filename)==sha
    analysis=json.loads((ROOT/'results/analysis/status.json').read_text())
    assert analysis['state']=='complete' and (ROOT/'results/analysis/COMPLETE').exists()
    assert analysis['numerical_integrity_passed']
    failures=[row for row in analysis['checks'] if not row['passed']]
    assert all(row['name'].startswith(('MATCHED_FORECAST:','CONVERGENCE:')) for row in failures)
    for filename,sha in analysis['input_hashes'].items():
        assert hashed(filename)==sha,filename
        if not Path(filename).is_relative_to(ROOT):
            inherited.inherited.verify_source(Path(filename),chain)
    checks=[dict(name='Analysis and immutable provenance verified;failed forecasts retained',passed=True)]
    inputs=[ROOT/'results/analysis/status.json',ROOT/'NUMERICAL-SUMMARY.json',
        ROOT/'results/analysis/source-separation.npz']
    summary=json.loads((ROOT/'NUMERICAL-SUMMARY.json').read_text())
    saved=read_npz(ROOT/'results/analysis/source-separation.npz')
    data=read_npz(PARENT/'results/anchor-sources/source.npz')
    def norm(value):
        spectral=value[1:-1]
        return np.sqrt(np.maximum(np.sum(spectral*np.linalg.solve(data['mass'],spectral),axis=0),0))
    scale=norm(data['actual'])
    current=norm(data['source6'])/scale
    close(checks,'Independent Cholesky-free cold normalization',saved['scale'],scale,1e-11)
    source=summary['source']
    ratios={}
    tails={}
    for site in ['cold','warm','centre']:
        previous=np.asarray([norm(saved[f'{site}_{key}_5']) for key in COMPONENTS])/scale
        latest=np.asarray([norm(saved[f'{site}_{key}_6']) for key in COMPONENTS])/scale
        ratio=latest/previous
        ratios[site]=ratio
        record=source['incoming_component_ladders'][site]
        close(checks,'Independent previous norms:'+site,previous,record['previous'],1e-10)
        close(checks,'Independent latest norms:'+site,latest,record['latest'],1e-10)
        close(checks,'Independent observed component ratios:'+site,ratio,record['ratios'],1e-10)
        assert not record['uniform_future_contraction_proven']
        if np.all(ratio<1):
            tail=latest*ratio/(1-ratio)
            tails[site]=tail
            close(checks,'Independent component geometric scenario:'+site,tail,record['geometric_tail'],1e-10)
            truncated=np.zeros_like(latest)
            term=latest.copy()
            for step in range(10000):
                term=term*ratio
                truncated+=term
            remainder=term*ratio/(1-ratio)
            close(checks,'Post6 geometric sum excludes last computed step:'+site,truncated+remainder,tail,1e-10)
    for route in ['local','cubic']:
        record=source['routes'][route]
        error=saved[route+'_error6']
        error_norm=norm(error)/scale
        expected={5:np.zeros_like(error),6:np.zeros_like(error)}
        weights={'cold':1.,'warm':1. if route=='cubic' else 0.,'centre':-1.5 if route=='cubic' else -.75}
        assert record['weights']==weights
        for order in [5,6]:
            for site,weight in weights.items():
                expected[order]+=weight*sum(saved[f'{site}_{key}_{order}'] for key in COMPONENTS)
            close(checks,'Independent matched increment:'+route+':'+str(order),
                expected[order],saved[f'{route}_change{order}'],1e-10)
        close(checks,'Independent residual telescope:'+route,saved[route+'_error4']+expected[5]+expected[6],error,1e-11)
        close(checks,'Current source-relative discrepancy:'+route,norm(error)/norm(data['source6']),
            record['matched_errors']['6']['own_source'],1e-10)
        last_cold=sum(norm(saved[f'cold_{key}_6']) for key in COMPONENTS)/scale
        previous_cold=sum(norm(saved[f'cold_{key}_5']) for key in COMPONENTS)/scale
        last_budget=sum(abs(weight)*sum(norm(saved[f'{site}_{key}_6']) for key in COMPONENTS) for site,weight in weights.items())/scale
        previous_budget=sum(abs(weight)*sum(norm(saved[f'{site}_{key}_5']) for key in COMPONENTS) for site,weight in weights.items())/scale
        scenarios={'observed_last_step_as_radius':(last_cold,last_budget),
            'observed_two_steps_as_radius':(last_cold+previous_cold,last_budget+previous_budget)}
        if len(tails)==3:
            cold_radius=tails['cold'].sum(axis=0)
            scenarios['independent_component_geometric']=(cold_radius,sum(abs(weight)*tails[site].sum(axis=0) for site,weight in weights.items()))
            ratio=norm(expected[6])/norm(expected[5])
            if np.all(ratio<1):
                scenarios['coherent_matched_geometric']=(cold_radius,norm(expected[6])/scale*ratio/(1-ratio))
        for name,(cold_radius,error_radius) in scenarios.items():
            result=record['scenarios'][name]
            assert result['conditional'] and not result['certified'] and result['unmeasured_endpoint_and_other_axis_radii'] is None
            close(checks,'Independent scenario radius:'+route+':'+name,error_radius,result['tested_error_radius'],1e-10)
            close(checks,'Independent scenario lower bound:'+route+':'+name,
                np.maximum(error_norm-error_radius,0)/(current+cold_radius),result['relative_lower'],1e-10)
            close(checks,'Independent unresolved-budget threshold:'+route+':'+name,
                error_norm-error_radius-THRESHOLD*(current+cold_radius),
                result['unresolved_error_radius_allowance_to_keep_above1percent'],1e-10)
        for group in record['shape_projections'].values():
            assert set(group)==set(map(str,SHAPE_CUTOFFS))
            for rows in group.values():
                for row in rows:
                    test(checks,'Whitened projection unit fractions:'+route,
                        abs(row['projection_fraction_of_defect']**2+row['residual_fraction_of_defect']**2-1),1e-10)
        maximum=0.
        for phase in np.linspace(0,1,101):
            coefficients=independent_weights(phase,route)
            before=[data['start'],data['warm_source4'],data['centre_source4'],data['actual'],data['end']]
            after=[data['start'],data['warm_source6'],data['centre_source6'],data['source6'],data['end']]
            original=sum(weight*value for weight,value in zip(coefficients,before))
            candidate=sum(weight*value for weight,value in zip(coefficients,after))
            known=cold_bubble(phase,route)*(data['delta5_total']+data['delta6_total'])
            for anchor in ANCHORS:
                known+=response_basis(phase,route,anchor)*(data[anchor+'_delta_total']+data[anchor+'_delta6_total'])
            maximum=max(maximum,float(max(norm(candidate-original-known)/scale)))
            close(checks,'Independent updated physical curve:'+route+':'+str(phase),
                candidate,stage155_parent.central_source(data,phase,route)+sum(stage155_parent.delta_components(data,phase,route)),1e-11)
        test(checks,'Saved full response forcing identity:'+route,maximum,1e-12)
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    reader=ShapeReadout(ladder.basis,canonical=True)
    for model in ['heavy','cold']:
        for route in ['local','cubic']:
            for count in COUNTS:
                label=f'{model}-{route}-{count}'
                record=summary['response']['records'][label]
                assert not record['updated_pure_cubic_defect_response_available']
                original=read_npz(location(STAGE150,model,route,count)/'response.npz')
                last=read_npz(location(PARENT,model,route,count)/'response.npz')
                photon=last['photon'][-1,:,2:4]-original['photon'][-1,:,0:2]
                history=read_npz(ROOT/'results/analysis'/(label+'-history.npz'))
                expected_norm=np.sqrt(np.maximum(np.sum(photon*(data['mass']@photon),axis=0),0))
                close(checks,'Independent endpoint photon gap:'+label,history['photon_gap'][-1],expected_norm,1e-8)
                for match in [20,40]:
                    path=ROOT/'results/analysis'/(label+'-m'+str(match)+'-readout.npz')
                    split=read_npz(path)
                    old=read_npz(STAGE150/'results/comparison'/f'{model}-m{match}-{route}-{count}.npz')
                    newest=read_npz(PARENT/'results/comparison'/f'{model}-m{match}-{route}-{count}.npz')
                    assert split['potential'].shape==(700,29)
                    assert np.array_equal(split['potential'][:,:1],old['potential'][:,:1])
                    assert np.array_equal(split['amplitudes'][:,:1],old['amplitudes'][:,:1])
                    assert np.array_equal(split['potential'][:,1:3],old['potential'][:,7:9])
                    assert np.array_equal(split['potential'][:,3:5],newest['potential'][:,9:11])
                    close(checks,'Independent direct small readout:'+label+':'+str(match),
                        split['potential'][:,9:11],reader.values@photon,1e-8)
                    for position,name in enumerate(['mu','y']):
                        denominator=abs(old['amplitudes'][position,9:11])
                        gap=abs(split['amplitudes'][position,9:11])/denominator
                        budget=sum(abs(split['amplitudes'][position,start:start+2]) for start in range(11,29,2))/denominator
                        values=record['readouts'][str(match)][name]
                        close(checks,'Independent paired '+name+' gap:'+label+':'+str(match),gap,values['gap_over_S4'],1e-10)
                        close(checks,'Independent nine-component '+name+' budget:'+label+':'+str(match),budget,values['latest_budget_over_S4'],1e-10)
                    checks.append(dict(name='Same baseline,source history and29-column readout:'+label+':'+str(match),passed=True))
                    inputs.append(path)
    assert summary['new_physical_events']==summary['new_response_evolutions']==0
    assert not summary['temperature_curve_changed'] and not summary['numerical_remainder_certified']
    assert summary['response']['updated_defect_response_not_fabricated']
    scripts=sorted(ROOT.glob('*.py'))
    for path in scripts:
        compile(path.read_text(),str(path),'exec')
    assert len(scripts)==4 and not list(ROOT.rglob('__pycache__'))
    largest=max(len(files) for directory,directories,files in os.walk(ROOT))
    assert largest<1000
    workbench=POST.parent/'formalization-workbench'
    assert not [path for path in workbench.rglob('*') if path.is_file() and path.stat().st_mtime>STARTED.timestamp()]
    checks.append(dict(name='Four scripts compile;no bytecode;folder limits;protectedworkbench0;zero new events/evolutions',passed=True))
    consumed={path:sha for path,sha in hashes.items() if not Path(path).is_relative_to(ROOT)}
    finish(folder,dict(checks=checks,accepted_scope_verified=all(row['passed'] for row in checks),
        consumed_and_immediate_rehashed=consumed,rehashed_prior_files=len(consumed),
        scientific_checks=analysis['count'],passing_scientific_checks=analysis['count']-len(failures),
        retained_failure_names=[row['name'] for row in failures],compiled_scripts=len(scripts),
        largest_direct_file_count=largest,protected_workbench_recent_modified_file_count=0),
        __file__,inputs)
    print(json.dumps(dict(validation=len(checks),passed=all(row['passed'] for row in checks),
        scientific=analysis['count'],retained_failures=len(failures),prior_files=len(consumed))),flush=True)
    assert all(row['passed'] for row in checks)


if __name__=='__main__':
    main()
