from stage153_separation_common import *


def main():
    modest()
    folder=ROOT/'results/validation'
    folder.mkdir(parents=True,exist_ok=True)
    assert not (folder/'status.json').exists()
    analysis=json.loads((ROOT/'results/analysis/status.json').read_text())
    precision=verify_packet(ROOT/'results/precision')
    assert precision['all_checks_passed'] and precision['all_repaired']
    chain=ancestors()
    hashes={}
    def checked_hash(path):
        path=Path(path).resolve()
        if str(path) not in hashes:
            hashes[str(path)]=digest(path)
        return hashes[str(path)]
    for filename,sha in chain[PARENT/'results/stage-integrity.json']['file_hashes'].items():
        assert checked_hash(PARENT/filename)==sha,filename
    for packet in [analysis,precision]:
        for filename,sha in packet['input_hashes'].items():
            assert checked_hash(filename)==sha,filename
            if not Path(filename).is_relative_to(ROOT):
                inherited.inherited.verify_source(Path(filename),chain)
    bad=[row['name'] for row in analysis['checks'] if not row['passed']]
    assert all(name.startswith(('FROZEN_FORECAST:','Same baseline cancellation:','CONVERGENCE:')) for name in bad)
    assert sum(name.startswith('Same baseline cancellation:') for name in bad)==precision['raw_cancellation_failures']==35
    checks=[dict(name='Immediate parent and every analysis input hash verified',passed=True)]
    summary=json.loads((ROOT/'NUMERICAL-SUMMARY.json').read_text())
    source=read_npz(ROOT/'results/analysis/source-separation.npz')
    data=read_npz(PARENT/'results/integration-source/source.npz')
    def independent_norm(value):
        spectral=value[1:-1]
        return np.sqrt(np.maximum(np.sum(spectral*np.linalg.solve(source['mass'],spectral),axis=0),0.))
    scale=independent_norm(data['actual'])
    close(checks,'Independent source denominator',scale,source['scale'],1e-11)
    for route in ['local','cubic']:
        record=summary['source']['routes'][route]
        prediction=source['prediction_'+route]
        residual=data['source6']-prediction
        norm=independent_norm(residual)/scale
        full=independent_norm(data['source6'])/scale
        close(checks,'Independent frozen discrepancy:'+route,norm,record['error_norm_over_S4']['6'],1e-11)
        for name,radius in [('observed_last_ball',source['radius65']),
                            ('two_observed_steps_ball',source['radius65']+source['radius54'])]:
            expected=np.maximum(norm-radius,0)/(full+radius)
            close(checks,'Independent conditional triangle:'+route+':'+name,
                expected,record[name]['relative_lower_with_source_shift'],1e-11)
            assert record[name]['explicitly_conditional'] and not record[name]['certified_radius']
        threshold=.01
        target=prediction/(1-threshold**2)
        radius=threshold*independent_norm(prediction)/(1-threshold**2)
        exact=np.maximum(independent_norm(data['source6']-target)-radius,0)/scale
        close(checks,'Independent minimum-distance threshold:'+route,
            exact,record['exact_displacement_to1percent_over_S4'],1e-10)
        for order,key in [(3,'source3'),(4,'actual'),(5,'source5'),(6,'source6')]:
            close(checks,'Independent saved forecast:order'+str(order)+':'+route,
                independent_norm(data[key]-prediction)/independent_norm(data[key]),
                record['self_relative_error'][str(order)],1e-10)
    cubic=summary['source']['routes']['cubic']
    assert cubic['certified_cold_radius'] is None and cubic['certified_anchor_radii']==[None]*4
    assert not summary['incoming_continuum_error_certified']
    assert not summary['predictor_anchor_errors_certified']
    anchors=source['anchors'].copy()
    weights=source['weights']
    defect=source['error6_cubic']
    hypothetical=anchors.copy()
    hypothetical[2]+=defect/weights[2]
    close(checks,'Unbounded centre-anchor error can algebraically explain entire discrepancy',
        sum(weight*value for weight,value in zip(weights,hypothetical)),source['source6'],1e-12)
    assert np.array_equal(anchors,source['anchors'])
    checks.append(dict(name='Identifiability witness does not alter saved anchors or assign a physical error',passed=True))
    ledger=dict(identification='unresolved without independent bounds on cold and predictor-anchor integration',
        hypothetical_witness='Exact centre=saved centre+E6/(3/2) makes the cubic interpolate H6 algebraically; not an inferred error or proposed correction.',
        certified_cold_radius=None,certified_anchor_radii=[None]*4,
        source_curve_changed=False,other_integration_axes_refined=False)
    write_json(folder/'identifiability.json',ledger)
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    reader=ShapeReadout(ladder.basis,canonical=True)
    maximum_svd=0.
    inputs=[ROOT/'results/analysis/status.json',ROOT/'NUMERICAL-SUMMARY.json',
        ROOT/'results/analysis/source-separation.npz',folder/'identifiability.json',*ladder.inputs]
    for model in ['heavy','cold']:
        for route in ['local','cubic']:
            for count in COUNTS:
                latest=read_npz(response_location(PARENT,model,route,count)/'response.npz')
                norm_path=ROOT/'results/analysis'/f'{model}-{route}-{count}-history-norms.npz'
                saved_norms=read_npz(norm_path)
                assert saved_norms['coordinate'].shape==(count+1,)
                for match in [20,40]:
                    label=f'{model}-{route}-{count}-m{match}'
                    path=ROOT/'results/analysis'/(label+'-readout.npz')
                    result=read_npz(path)
                    original=read_npz(comparison_path(STAGE150,model,route,count,match))
                    previous=read_npz(comparison_path(PARENT,model,route,count,match))
                    assert result['potential'].shape==(700,17)
                    assert np.array_equal(result['potential'][:,:1],original['potential'][:,:1])
                    assert np.array_equal(result['amplitudes'][:,:1],original['amplitudes'][:,:1])
                    assert np.array_equal(result['potential'][:,1:3],original['potential'][:,7:9])
                    assert np.array_equal(result['potential'][:,3:5],previous['potential'][:,9:11])
                    assert np.array_equal(result['frequency'],reader.frequency)
                    assert np.array_equal(result['measure'],reader.measure)
                    for new,old in [(slice(11,13),slice(12,14)),(slice(13,15),slice(14,16)),(slice(15,17),slice(16,18))]:
                        assert np.array_equal(result['potential'][:,new],reader.values@latest['photon'][-1,:,old])
                    distortion=result['potential']-reader.frequency[:,None]*(result['energy']/reader.capacity)
                    alternative=np.linalg.lstsq(np.sqrt(reader.measure)[:,None]*reader.templates,
                        np.sqrt(reader.measure)[:,None]*distortion,rcond=None)[0]
                    numerator=np.linalg.norm(np.sqrt(reader.measure)[:,None]*(reader.templates@(alternative-result['amplitudes'])),axis=0)
                    denominator=np.linalg.norm(np.sqrt(reader.measure)[:,None]*distortion,axis=0)
                    maximum_svd=max(maximum_svd,float(max(numerator/np.maximum(denominator,1e-300))))
                    reported=summary['responses'][f'{model}-{route}-{count}']['readouts'][str(match)]
                    for position,name in enumerate(['mu','y']):
                        heat=float(result['heat'])
                        physical=heat*result['amplitudes'][position]
                        reference=abs(heat*original['amplitudes'][position,9:11])
                        budget=sum(abs(physical[selection]) for selection in [slice(11,13),slice(13,15),slice(15,17)])
                        close(checks,'Independent '+name+' observed budget:'+label,
                            budget/reference,reported[name]['last_budget_over_S4'],1e-12)
                        close(checks,'Independent '+name+' frozen discrepancy:'+label,
                            abs(physical[9:11])/reference,reported[name]['defect_over_S4'],1e-12)
                    checks.append(dict(name='Same baseline/MTS projection and fixed S4 denominator:'+label,passed=True))
                    inputs.append(path)
                inputs.append(norm_path)
    test(checks,'Independent weighted SVD',maximum_svd,1e-10)
    assert summary['new_physical_events']==0 and summary['new_response_evolutions']==0
    assert not summary['temperature_curve_changed'] and summary['baseline_preserved']
    assert not summary['baseline_inner_history_refined']
    assert not (ROOT/'runs').exists()
    scripts=sorted(ROOT.glob('*.py'))
    for path in scripts:
        compile(path.read_text(),str(path),'exec')
    assert len(scripts)==5 and not list(ROOT.rglob('__pycache__'))
    largest=max(len(files) for directory,directories,files in os.walk(ROOT))
    assert largest<1000
    workbench=POST.parent/'formalization-workbench'
    recent=[path for path in workbench.rglob('*') if path.is_file() and path.stat().st_mtime>STARTED.timestamp()]
    assert not recent,recent
    checks.append(dict(name='Five scripts compile;no event/evolution jobs;no bytecode;protected workbench0',passed=True))
    checks.append(dict(name='All35 raw subtraction misses retained and96 higher-precision checks pass without relaxing tolerances',passed=True))
    final=dict(summary)
    final.update(raw_analysis_numerical_integrity_passed=summary['numerical_integrity_passed'],
        numerical_integrity_passed=precision['all_checks_passed'],
        scientific_checks=len(analysis['checks'])+len(precision['checks']),
        passing_scientific_checks=sum(row['passed'] for row in analysis['checks'])+sum(row['passed'] for row in precision['checks']),
        retained_raw_cancellation_failures=35,retained_failed_checks=len(bad),
        precision_summary_path=str(ROOT/'PRECISION-SUMMARY.json'),maximum_independent_svd_relative=maximum_svd,
        accepted_scope='Frozen cubic discrepancy separated from measured incoming-rule changes; exact anchor-error identity and conditional radii; saved baseline/MTS responses with verified60digit readout.')
    write_json(ROOT/'FINAL-SUMMARY.json',final)
    inputs.extend([ROOT/'results/precision/status.json',ROOT/'FINAL-SUMMARY.json'])
    consumed={filename:sha for filename,sha in hashes.items() if not Path(filename).is_relative_to(ROOT)}
    finish(folder,dict(checks=checks,accepted_scope_verified=all(row['passed'] for row in checks),
        consumed_and_immediate_rehashed=consumed,rehashed_prior_files=len(consumed),
        scientific_checks=final['scientific_checks'],passing_scientific_checks=final['passing_scientific_checks'],
        retained_failure_names=bad,compiled_scripts=len(scripts),maximum_independent_svd_relative=maximum_svd,
        largest_direct_file_count=largest,protected_workbench_recent_modified_file_count=0),__file__,inputs)
    print(json.dumps(dict(validation_checks=len(checks),passed=all(row['passed'] for row in checks),
        prior_files=len(consumed),science=final['scientific_checks'],retained_failures=len(bad),
        maximum_svd=maximum_svd)),flush=True)
    assert all(row['passed'] for row in checks)


if __name__=='__main__':
    main()
