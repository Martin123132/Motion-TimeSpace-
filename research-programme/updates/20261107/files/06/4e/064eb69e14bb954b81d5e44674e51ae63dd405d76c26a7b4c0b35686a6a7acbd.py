from stage146_precision_common import *
from decimal import Decimal,localcontext


def main():
    modest()
    folder=ROOT/'results/validation'
    folder.mkdir(parents=True,exist_ok=False)
    chain=ancestors()
    assert sum(len(packet['file_hashes']) for packet in chain.values())==INHERITED_PAYLOADS
    hashes={}
    def hashed(path):
        path=Path(path).resolve()
        if str(path) not in hashes:
            hashes[str(path)]=digest(path)
        return hashes[str(path)]
    for filename,sha in chain[PARENT/'results/stage-integrity.json']['file_hashes'].items():
        assert hashed(PARENT/filename)==sha,filename
    checks=[dict(name='Immediate Stage145 including literal predictions and raw failures unchanged',passed=True)]
    readiness=verify_packet(ROOT/'results/repaired-readiness')
    allowed=readiness['allowed_routes']
    packets=['results/preflight',*['results/reaggregation/'+case for case in CASES],'results/repaired-readiness']
    for model in ['heavy','cold']:
        for kind in ['local','cubic']:
            response_folder=ROOT/'results/response'/f'{model}-{kind}'
            if allowed[kind]:
                packets.extend(['results/response/'+model+'-'+kind+'/'+phase for phase in ['active','transfer']])
                packets.append('results/response/'+model+'-'+kind)
            else:
                assert not response_folder.exists()
    if any(allowed.values()):
        packets.append('results/spectral-readout')
    count=passed=0
    failures={}
    inputs=[]
    for name in packets:
        location=ROOT/name
        report=json.loads((location/'status.json').read_text())
        assert report['state']=='complete' and (location/'COMPLETE').exists()
        assert report['count']==len(report['checks'])
        bad=[row['name'] for row in report['checks'] if not row['passed']]
        if bad:
            assert name=='results/repaired-readiness'
            assert all(label.startswith(('Unchanged small-defect rewrite gate:',
                'Independent gas pairing:','Reconstructed moment:','Unprojected colder-source')) for label in bad)
            failures[name]=bad
        for filename,sha in report['input_hashes'].items():
            path=Path(filename)
            assert hashed(path)==sha,path
            if not path.is_relative_to(ROOT):
                inherited.inherited.verify_source(path,chain)
        count+=report['count']
        passed+=sum(bool(row['passed']) for row in report['checks'])
        inputs.append(location/'status.json')
        checks.append(dict(name='Complete sourced packet:'+name,passed=True))
    assert not verify_packet(PARENT/'results/colder-source')['energy_coordinate_evolution_allowed']
    assert verify_packet(PARENT/'results/route-readiness')['allowed_routes']=={'local':True,'cubic':False}
    checks.append(dict(name='Original blocked cubic route remains blocked in its sealed record',passed=True))
    source=read_npz(ROOT/'results/repaired-readiness/source.npz')
    actual=[]
    total_reused=0
    for case in CASES:
        location=ROOT/'results/reaggregation'/case
        report=json.loads((location/'status.json').read_text())
        total_reused+=report['reused_event_nodes']
        assert report['new_event_evaluations']==report['new_loop_evaluations']==0
        data=read_npz(location/'source.npz')
        actual.append(data['remainder'])
        terms=read_npz(location/'leading-terms.npz')
        with localcontext() as context:
            context.prec=60
            for column in range(4):
                scalar=sum((Decimal.from_float(float(value)) for value in terms['scalar_terms'][:,column]),Decimal(0))
                for index in range(2):
                    expected=float(-Decimal.from_float(float(terms['constants'][index]))*scalar)
                    assert expected==data['sampled_leading'][index+1,column]
        raw=raw_components(case)
        assert np.array_equal(data['sampled_leading'][[0,-1]],raw['sampled_leading'][[0,-1]])
        assert np.isfinite(data['remainder']).all()
        checks.append(dict(name='Leading constant-test factorization independently reconstructed:'+case,passed=True))
        inputs.extend([location/'source.npz',location/'leading-terms.npz'])
    assert total_reused==29952
    phases=[0,.25,.5,.75,1]
    for kind in ['local','cubic']:
        for phase,expected in zip(phases,actual):
            value=forecast(source,source['warm_defect'],phase,kind)+cold_bubble(phase,kind)*source[kind+'_defect']
            test(checks,'All refined source nodes retained:'+kind+':'+str(phase),
                 np.max(abs(value-expected))/np.max(abs(expected)),1e-12)
    for phase in [.1,.3,.6,.9]:
        independent=np.zeros_like(actual[0])
        for index,node in enumerate(phases):
            weight=math.prod((phase-other)/(node-other) for ordinal,other in enumerate(phases) if ordinal!=index)
            independent+=weight*actual[index]
        candidate=forecast(source,source['warm_defect'],phase,'cubic')+cold_bubble(phase,'cubic')*source['cubic_defect']
        test(checks,'Independent five-node Lagrange quartic:'+str(phase),
             np.max(abs(independent-candidate))/np.max(abs(independent)),1e-12)
    maximum_budget=maximum_svd=0.
    readout={}
    responses={}
    if any(allowed.values()):
        readout=json.loads((ROOT/'results/spectral-readout/status.json').read_text())
        ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
        reader=ShapeReadout(ladder.basis,canonical=True)
        for model in ['heavy','cold']:
            heat=readout['metadata'][model]['heat']
            for kind in ['local','cubic']:
                if not allowed[kind]:
                    continue
                location=ROOT/'results/response'/f'{model}-{kind}'
                response_report=json.loads((location/'status.json').read_text())
                responses[model+'-'+kind]=response_report['precision_change_from_saved_stage144_curve']
                active,transfer=[read_npz(location/phase/'response.npz') for phase in ['active','transfer']]
                for key in ['photon','energy','gas','work','integrated_number_source']:
                    assert np.array_equal(active[key][-1],transfer[key][0])
                checks.append(dict(name='Physical restart seam:'+model+':'+kind,passed=True))
                for phase,data in [('active',active),('transfer',transfer)]:
                    assert data['photon'].shape==(1025,96,12)
                    assert all(np.isfinite(value).all() for value in data.values())
                    budget=data['energy']+heat*data['gas']+data['work']
                    scale=np.maximum(np.max(abs(data['energy'])+abs(heat*data['gas'])+abs(data['work']),axis=0),1e-300)
                    error=float(np.max(abs(budget-budget[0])/scale))
                    maximum_budget=max(maximum_budget,error)
                    test(checks,'Stored energy-work budget:'+model+':'+kind+':'+phase,error,1e-7)
                    inputs.append(location/phase/'response.npz')
                for match in [20,40]:
                    label=f'{model}-m{match}-{kind}'
                    result_path=ROOT/'results/spectral-readout'/(label+'.npz')
                    data=read_npz(result_path)
                    prior_path=WARM/'results/spectral-readout'/(label+'.npz')
                    prior=read_npz(prior_path)
                    assert np.array_equal(data['potential'][:,:3],prior['potential'][:,:3])
                    assert np.array_equal(data['potential'][:,15:17],reader.values@transfer['photon'][-1,:,4:6])
                    distortion=data['potential']-reader.frequency[:,None]*(data['energy']/reader.capacity)
                    design=np.sqrt(reader.measure)[:,None]*reader.templates
                    alternate=np.linalg.lstsq(design,np.sqrt(reader.measure)[:,None]*distortion,rcond=None)[0]
                    maximum_svd=max(maximum_svd,float(np.max(abs(alternate-data['amplitudes']))/
                        max(float(np.max(abs(data['amplitudes']))),1e-300)))
                    metrics=readout['rows'][label]['metrics']
                    assert np.array_equal(np.array(metrics['mu']),heat*data['amplitudes'][0])
                    assert np.array_equal(np.array(metrics['y']),heat*data['amplitudes'][1])
                    checks.append(dict(name='Same unchanged nonzero baseline and MTS readout:'+label,passed=True))
                    inputs.extend([result_path,prior_path])
        test(checks,'Independent SVD spectral decomposition',maximum_svd,1e-10)
    scripts=sorted(ROOT.glob('*.py'))
    for script in scripts:
        compile(script.read_text(encoding='utf-8'),str(script),'exec')
    assert not list(ROOT.rglob('__pycache__'))
    largest=max(len(files) for directory,directories,files in os.walk(ROOT))
    assert largest<1000
    workbench=POST.parent/'formalization-workbench'
    recent=[path for path in workbench.rglob('*') if path.is_file() and path.stat().st_mtime>STARTED.timestamp()]
    assert not recent
    checks.append(dict(name='Script compilation,no bytecode,folder limits,protected workbench modification-time count0',passed=True))
    summary=dict(stage=146,scientific_checks=count,passing_scientific_checks=passed,
        retained_failed_checks=count-passed,failed_by_packet=failures,packets=packets,
        allowed_routes=allowed,threshold=1e-10,maximum_rewrite=readiness['maximum_rewrite_by_route'],
        source_diagnostics=readiness['diagnostics'],precision_response_changes=responses,
        readouts=readout.get('rows',{}),route_comparison=readout.get('route_comparison_relative_to_cubic',{}),
        maximum_energy_work_residual=maximum_budget,maximum_svd=maximum_svd,
        reused_event_nodes=total_reused,new_event_nodes=0,new_virtual_coefficients=0,
        literal_stage145_prediction_and_failures_unchanged=True,baseline_preserved=True,
        final_epoch=1e-5,frequency_modes=96,response_steps_per_phase=1024,
        accepted_scope='Saved-event arithmetic repair and gate-qualified local/cubic window responses',
        new_window_inner_feedback_recomputed=False,event_quadrature_error_bounded=False,
        interpolation_choices_are_error_bounds=False,observational_fit=False,
        next_target='Check the newly propagated small cubic increment under response-step refinement, reusing repaired sources and the saved baseline. Then extend the physical source into the next colder interval rather than repeatedly refitting this interval.')
    write_json(ROOT/'NUMERICAL-SUMMARY.json',summary)
    consumed={path:sha for path,sha in hashes.items() if not Path(path).is_relative_to(ROOT)}
    finish(folder,dict(checks=checks,accepted_scope_verified=all(row['passed'] for row in checks),
        consumed_and_immediate_rehashed=consumed,rehashed_prior_files=len(consumed),
        compiled_scripts=len(scripts),largest_direct_file_count=largest,
        scientific_checks=count,passing_scientific_checks=passed,retained_failed_checks=count-passed,
        protected_workbench_recent_modified_file_count=0),__file__,[*inputs,ROOT/'NUMERICAL-SUMMARY.json'])
    print(json.dumps(dict(validation_checks=len(checks),passed=all(row['passed'] for row in checks),
        science=count,science_passed=passed,flags=count-passed,rehashed_prior_files=len(consumed))),flush=True)
    assert all(row['passed'] for row in checks)


if __name__=='__main__':
    main()
