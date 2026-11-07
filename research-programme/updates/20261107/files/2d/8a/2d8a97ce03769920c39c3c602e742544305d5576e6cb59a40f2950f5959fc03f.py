from stage154_anchor_common import *


def interpolation_weights(phase,route):
    nodes=[0.,.25,.5,.75,1.]
    indices=list(range(5)) if route=='cubic' else [0,1,2] if phase<=.5 else [2,3,4]
    weights=np.zeros(5)
    for index in indices:
        weight=1.
        for other in indices:
            if other!=index:
                weight*=(phase-nodes[other])/(nodes[index]-nodes[other])
        weights[index]=weight
    return weights


def main():
    modest()
    folder=ROOT/'results/validation'
    folder.mkdir(parents=True,exist_ok=True)
    assert not (folder/'status.json').exists()
    chain=ancestors()
    hashes={}
    def hashed(path):
        path=Path(path).resolve()
        if str(path) not in hashes:
            hashes[str(path)]=digest(path)
        return hashes[str(path)]
    for filename,sha in chain[PARENT/'results/stage-integrity.json']['file_hashes'].items():
        assert hashed(PARENT/filename)==sha
    allowed=verify_packet(ROOT/'results/readiness')['allowed_routes']
    packets=['results/preflight','runs/warm','runs/centre','results/anchor-sources','results/readiness',
        *[f'results/response/{model}-{route}-{count}' for model in ['heavy','cold'] for route in allowed if allowed[route] for count in COUNTS],
        'results/comparison']
    checks,inputs,failures=[],[],{}
    science=passed=0
    for name in packets:
        location=ROOT/name
        packet=json.loads((location/'status.json').read_text())
        assert packet['state']=='complete' and (location/'COMPLETE').exists()
        bad=[row['name'] for row in packet['checks'] if not row['passed']]
        prefixes=['ACCURACY:','RAW_MOMENT:','REFRESHED_FORECAST_DIAGNOSTIC:','CONDITIONAL_ANCHOR_BUDGET:'] if name=='results/anchor-sources' else ['READINESS:'] if name=='results/readiness' else ['CONVERGENCE:','RESPONSE_SENSITIVITY:'] if name=='results/comparison' else []
        assert all(any(label.startswith(prefix) for prefix in prefixes) for label in bad),(name,bad)
        if bad:
            failures[name]=bad
        for filename,sha in packet['input_hashes'].items():
            assert hashed(filename)==sha,filename
            if not Path(filename).is_relative_to(ROOT):
                inherited.inherited.verify_source(Path(filename),chain)
        science+=packet['count']
        passed+=sum(bool(row['passed']) for row in packet['checks'])
        checks.append(dict(name='Complete sourced packet;failures retained:'+name,passed=True))
        inputs.append(location/'status.json')
    data=read_npz(ROOT/'results/anchor-sources/source.npz')
    frozen=read_npz(ROOT/'results/preflight/frozen-reference.npz')
    assert all(np.array_equal(data[key],value) for key,value in frozen.items())
    source_report=verify_packet(ROOT/'results/anchor-sources')
    assert source_report['numerical_integrity_passed']
    def norm(value):
        spectral=value[1:-1]
        return np.sqrt(np.maximum(np.sum(spectral*np.linalg.solve(data['mass'],spectral),axis=0),0.))
    cold_scale=norm(data['actual'])
    for anchor in ANCHORS:
        scale=norm(data[anchor+'_source4'])
        parts=[data[anchor+'_delta_'+key] for key in COMPONENTS]
        budget=sum(norm(value) for value in parts)/scale
        close(checks,'Independent anchor source budget:'+anchor,budget,source_report['source_metrics'][anchor]['component_sum'],1e-10)
        close(checks,'Independent full source difference:'+anchor,
            data[anchor+'_source5']-data[anchor+'_source4'],sum(parts),1e-9)
        assert len(list((ROOT/'runs'/anchor/'nodes').rglob('*.npz')))==1260
    unique_loops={str(read_npz(path)['loop_path']) for anchor in ANCHORS for path in (ROOT/'runs'/anchor/'nodes').rglob('*.npz')}
    assert len(unique_loops)==len(list((ROOT/'virtual-cache').rglob('*.json')))
    checks.append(dict(name='2520 new events;all coefficients owned and counted',passed=True))
    for route in ['local','cubic']:
        weights=np.asarray([-1.,1.5]) if route=='cubic' else np.asarray([0.,.75])
        predicted_change=sum(weight*data[anchor+'_delta_total'] for weight,anchor in zip(weights,ANCHORS))
        close(checks,'Independent cold predictor shift:'+route,predicted_change,data[route+'_predictor_shift'],1e-10)
        budget=sum(abs(weight)*sum(norm(data[anchor+'_delta_'+key]) for key in COMPONENTS) for weight,anchor in zip(weights,ANCHORS))/cold_scale
        close(checks,'Independent weighted predictor uncertainty:'+route,budget,
            source_report['prediction_diagnostics'][route]['noncancelling_anchor_budget_over_coldS4'],1e-10)
        nodes=[data['start'],data['warm_source4'],data['centre_source4'],data['source6'],data['end']]
        perturbed=[data['start'],data['warm_source5'],data['centre_source5'],data['source6'],data['end']]
        maximum_original=maximum_change=0.
        for phase in np.linspace(0,1,101):
            coefficients=interpolation_weights(phase,route)
            original=sum(weight*value for weight,value in zip(coefficients,nodes))
            candidate=sum(weight*value for weight,value in zip(coefficients,perturbed))
            reference=central_source(data,phase,route)
            change=sum(delta_components(data,phase,route))
            maximum_original=max(maximum_original,float(max(norm(original-reference)/norm(reference))))
            scale=np.maximum(norm(change),1e-300)
            if np.any(change):
                maximum_change=max(maximum_change,float(max(norm(candidate-original-change)/scale)))
            close(checks,'Independent sensitivity basis:'+route+':'+str(phase),
                [response_basis(phase,route,anchor) for anchor in ANCHORS],coefficients[[1,2]],1e-10)
        test(checks,'Original curve matches independent interpolation:'+route,maximum_original,1e-12)
        test(checks,'Candidate sensitivity matches independent interpolation:'+route,maximum_change,1e-9)
    comparison=verify_packet(ROOT/'results/comparison')
    assert comparison['allowed_routes']==allowed and comparison['columns']==29
    assert comparison['baseline_preserved'] and not comparison['curve_adopted'] and comparison['cold_anchor_fixed']
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    reader=ShapeReadout(ladder.basis,canonical=True)
    maximum_energy=maximum_svd=maximum_rewrite=0.
    for model in ['heavy','cold']:
        for route in ['local','cubic']:
            if not allowed[route]:
                continue
            for count in COUNTS:
                location=ROOT/'results/response'/f'{model}-{route}-{count}'
                response=read_npz(location/'response.npz')
                packet=json.loads((location/'status.json').read_text())
                heat=packet['heat']
                old=read_npz(SOURCE152/'results/response'/f'{model}-{route}-order6-{count}/response.npz')
                assert response['photon'].shape==(count+1,96,24)
                for key in ['photon','energy','gas','work','integrated_number_source']:
                    assert np.array_equal(response[key][0,...,:12],old[key][0,...,:12])
                    assert not np.any(response[key][0,...,12:])
                    assert not np.any(response[key][...,6:8])
                balance=response['energy']+heat*response['gas']+response['work']
                scale=np.maximum(np.max(abs(response['energy'])+abs(heat*response['gas'])+abs(response['work']),axis=0),1e-300)
                error=float(np.max(abs(balance-balance[0])/scale))
                maximum_energy=max(maximum_energy,error)
                test(checks,'Independent24column energy/work:'+model+':'+route+':'+str(count),error,1e-7)
                maximum_rewrite=max(maximum_rewrite,packet['metrics']['source_rewrite'])
                for match in [20,40]:
                    label=f'{model}-m{match}-{route}-{count}'
                    path=ROOT/'results/comparison'/(label+'.npz')
                    result=read_npz(path)
                    prior=read_npz(SOURCE152/'results/comparison'/f'{model}-m{match}-{route}-order6-4096.npz')
                    reference=read_npz(STAGE150/'results/comparison'/f'{model}-m{match}-{route}-4096.npz')
                    assert result['potential'].shape==(700,29)
                    assert np.array_equal(result['potential'][:,:3],prior['potential'][:,:3])
                    assert np.array_equal(result['amplitudes'][:,:1],prior['amplitudes'][:,:1])
                    for position in range(6):
                        assert np.array_equal(result['potential'][:,17+2*position:19+2*position],
                            reader.values@response['photon'][-1,:,12+2*position:14+2*position])
                    for position,name in enumerate(['mu','y']):
                        values=heat*result['amplitudes'][position]
                        denominator=abs(heat*reference['amplitudes'][position,9:11])
                        budget=sum(abs(values[start:start+2]) for start in range(17,29,2))/denominator
                        assert np.array_equal(budget,np.asarray(comparison['readouts'][label]['component_budget'][name]))
                    distortion=result['potential']-reader.frequency[:,None]*(result['energy']/reader.capacity)
                    alternate=np.linalg.lstsq(np.sqrt(reader.measure)[:,None]*reader.templates,
                        np.sqrt(reader.measure)[:,None]*distortion,rcond=None)[0]
                    difference=reader.templates@(alternate-result['amplitudes'])
                    numerator=np.linalg.norm(np.sqrt(reader.measure)[:,None]*difference,axis=0)
                    denominator=np.linalg.norm(np.sqrt(reader.measure)[:,None]*distortion,axis=0)
                    maximum_svd=max(maximum_svd,float(max(numerator/np.maximum(denominator,1e-300))))
                    checks.append(dict(name='Exact baseline/component readout and fixed denominator:'+label,passed=True))
                    inputs.append(path)
                inputs.append(location/'response.npz')
    test(checks,'Independent weighted SVD',maximum_svd,1e-10)
    test(checks,'Source rewrite own norm',maximum_rewrite,1e-10)
    scripts=sorted(ROOT.glob('*.py'))
    for path in scripts:
        compile(path.read_text(),str(path),'exec')
    assert len(scripts)==9 and not list(ROOT.rglob('__pycache__'))
    largest=max(len(files) for directory,directories,files in os.walk(ROOT))
    assert largest<1000
    workbench=POST.parent/'formalization-workbench'
    assert not [path for path in workbench.rglob('*') if path.is_file() and path.stat().st_mtime>STARTED.timestamp()]
    checks.append(dict(name='Nine scripts compile;no bytecode;folder limits;protected workbench0',passed=True))
    next_target='Refine incoming order5-to6 at BOTH predictor anchors as a matched pair,using at most two limited workers and saved4/5controls/histories. Keep original and refreshed predictions frozen;test contraction of both weighted component budgets and their much smaller coherent predictor shift before adopting a curve update.'
    if not all(allowed.values()):
        next_target='Repair small-component source-coordinate numerical readiness before propagating blocked anchor changes;retain all raw physical sources.'
    elif not comparison['convergence_passed']:
        next_target='Refine only the failed own-response time-step diagnostic before interpreting anchor sensitivity.'
    summary=dict(stage=154,scientific_checks=science,passing_scientific_checks=passed,retained_failed_checks=science-passed,
        failed_by_packet=failures,source_metrics=source_report['source_metrics'],
        prediction_diagnostics=source_report['prediction_diagnostics'],allowed_routes=allowed,
        comparisons=comparison['comparisons'],readouts=comparison['readouts'],
        convergence_passed=comparison['convergence_passed'],maximum_energy_work_residual=maximum_energy,
        maximum_source_rewrite=maximum_rewrite,maximum_independent_svd_relative=maximum_svd,
        maximum_precision_cancellation=comparison['maximum_precision_cancellation'],
        maximum_direct_projection=comparison['maximum_direct_projection'],
        new_unique_physical_events=2520,new_virtual_coefficients=len(unique_loops),
        reused_order4_events=2016,reused_control_events=9216,frequency_modes=96,response_steps=COUNTS,
        anchor_fractions=ANCHORS,final_epoch=1e-5,baseline_preserved=True,baseline_inner_history_refined=False,
        curve_adopted=False,cold_anchor_fixed=True,other_quadrature_axes_refined=False,
        continuum_error_certified=False,source_interval=[.75,1.],
        accepted_scope='Order4-to5 warm-quarter and centre physical-event sensitivity with matched baseline/MTS readout and fixed cold anchor',
        next_target=next_target)
    write_json(ROOT/'NUMERICAL-SUMMARY.json',summary)
    consumed={path:sha for path,sha in hashes.items() if not Path(path).is_relative_to(ROOT)}
    finish(folder,dict(checks=checks,accepted_scope_verified=all(row['passed'] for row in checks),
        consumed_and_immediate_rehashed=consumed,rehashed_prior_files=len(consumed),
        scientific_checks=science,passing_scientific_checks=passed,
        compiled_scripts=len(scripts),largest_direct_file_count=largest,
        protected_workbench_recent_modified_file_count=0),__file__,[*inputs,ROOT/'NUMERICAL-SUMMARY.json'])
    print(json.dumps(dict(validation_checks=len(checks),passed=all(row['passed'] for row in checks),
        science=science,science_passed=passed,prior_files=len(consumed),next_target=next_target)),flush=True)
    assert all(row['passed'] for row in checks)


if __name__=='__main__':
    main()
