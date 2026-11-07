from holdout_common import *


def main():
    modest()
    folder=ROOT/'results/validation'
    folder.mkdir(parents=True,exist_ok=False)
    chain=ancestors()
    assert sum(len(packet['file_hashes']) for packet in chain.values())==INHERITED_PAYLOADS
    hashes={}
    def hashed(path):
        path=Path(path).resolve()
        key=str(path)
        if key not in hashes:
            hashes[key]=digest(path)
        return hashes[key]
    for filename,sha in chain[PARENT/'results/stage-integrity.json']['file_hashes'].items():
        assert hashed(PARENT/filename)==sha,filename
    checks=[dict(name='Stage143 immediate payloads unchanged',passed=True)]
    packets=['results/preflight','runs/expensive-holdout','runs/control-holdout',
             'results/holdout-source','results/holdout-response','results/spectral-readout']
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
            assert name=='results/holdout-source'
            assert all(label.startswith(('RAW_MOMENT:','PREDICTION_DIAGNOSTIC:')) for label in bad)
            failures[name]=bad
        for filename,sha in report['input_hashes'].items():
            path=Path(filename)
            assert hashed(path)==sha,path
            if not path.is_relative_to(ROOT):
                inherited.inherited.verify_source(path,chain)
        count+=report['count']
        passed+=sum(bool(row['passed']) for row in report['checks'])
        inputs.append(location/'status.json')
        checks.append(dict(name='Complete finite sourced packet:'+name,passed=True))
    assert len(list((ROOT/'virtual-cache').rglob('*.json')))==1008
    prediction_path=ROOT/'results/preflight/frozen-prediction.npz'
    prediction=read_npz(prediction_path)
    lock_path=ROOT/'results/preflight/prediction-lock.json'
    lock=json.loads(lock_path.read_text())
    assert digest(prediction_path)==lock['prediction_sha256']
    assert digest(ROOT/'DERIVATION.md')==lock['method_sha256']
    assert digest(ROOT/'holdout_common.py')==lock['common_sha256']
    for part,expected in [('expensive',1008),('control',4608)]:
        nodes=list((ROOT/'runs'/f'{part}-holdout/nodes').rglob('*.npz'))
        assert len(nodes)==expected
        assert min(path.stat().st_mtime for path in nodes)>lock_path.stat().st_mtime
    checks.append(dict(name='Prediction and methods frozen before all5616 actual event nodes',passed=True))
    prior=read_npz(PARENT/'results/adjacent-sources/source.npz')
    independently_predicted=.375*prior['start']+.75*prior['centre']-.125*prior['end']
    test(checks,'Independent withheld Lagrange prediction',
         np.max(abs(independently_predicted-prediction['predicted']))/
         np.max(abs(independently_predicted)),1e-12)
    source=read_npz(ROOT/'results/holdout-source/source.npz')
    assert np.array_equal(source['defect'],source['actual']-prediction['predicted'])
    for kind in ['local','cubic']:
        assert bubble(.25,kind)==1 and all(bubble(node,kind)==0 for node in [0,.5,1])
        reconstructed=quadratic(prior,.25)+bubble(.25,kind)*source['defect']
        test(checks,'Defect sensitivity matches actual node:'+kind,
             np.max(abs(reconstructed-source['actual']))/np.max(abs(source['actual'])),1e-12)
    prior_report=json.loads((PARENT/'results/spectral-readout/status.json').read_text())
    readout=json.loads((ROOT/'results/spectral-readout/status.json').read_text())
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    reader=ShapeReadout(ladder.basis,canonical=True)
    maximum_svd=0.
    maximum_budget=0.
    for model in ['heavy','cold']:
        heat=prior_report['metadata'][model]['heat']
        for kind in ['local','cubic']:
            active_path=ROOT/'results/holdout-response'/f'{model}-{kind}-active.npz'
            transfer_path=ROOT/'results/holdout-response'/f'{model}-{kind}-transfer.npz'
            active,transfer=read_npz(active_path),read_npz(transfer_path)
            inputs.extend([active_path,transfer_path])
            for key in ['photon','energy','gas','work','integrated_number_source']:
                assert np.array_equal(transfer[key][0],active[key][-1])
            checks.append(dict(name='All five physical state offsets survive seam:'+model+':'+kind,passed=True))
            for phase,data in [('active',active),('transfer',transfer)]:
                assert data['photon'].shape==(1025,96,12)
                assert all(np.isfinite(value).all() for value in data.values())
                for key in ['photon','energy','gas','work','integrated_number_source']:
                    assert np.array_equal(data[key][...,6:8],np.zeros_like(data[key][...,6:8]))
                budget=data['energy']+heat*data['gas']+data['work']
                scale=np.maximum(np.max(abs(data['energy'])+abs(heat*data['gas'])+abs(data['work']),axis=0),1e-300)
                error=float(np.max(abs(budget-budget[0])/scale))
                maximum_budget=max(maximum_budget,error)
                test(checks,'Independent stored energy-work budget:'+model+':'+kind+':'+phase,error,1e-7)
            for match in [20,40]:
                case=f'{model}-m{match}'
                label=case+'-'+kind
                archive_path=ROOT/'results/spectral-readout'/(label+'.npz')
                data=read_npz(archive_path)
                prior_path=PARENT/'results/spectral-readout'/(case+'.npz')
                previous=read_npz(prior_path)
                assert np.array_equal(data['potential'][:,:5],previous['potential'][:,:5])
                expected=reader.values@transfer['photon'][-1,:,4:6]
                assert np.array_equal(data['potential'][:,15:17],expected)
                assert np.array_equal(data['potential'][:,5:7],data['potential'][:,3:5]+expected)
                assert np.array_equal(data['potential'][:,9:11],data['potential'][:,1:3]+data['potential'][:,5:7])
                distortion=data['potential']-reader.frequency[:,None]*(data['energy']/reader.capacity)
                design=np.sqrt(reader.measure)[:,None]*reader.templates
                alternate=np.linalg.lstsq(design,np.sqrt(reader.measure)[:,None]*distortion,rcond=None)[0]
                maximum_svd=max(maximum_svd,float(np.max(abs(alternate-data['amplitudes']))/
                                   max(float(np.max(abs(data['amplitudes']))),1e-300)))
                values=readout['rows'][label]['metrics']
                assert np.array_equal(np.array(values['mu']),heat*data['amplitudes'][0])
                assert np.array_equal(np.array(values['y']),heat*data['amplitudes'][1])
                checks.append(dict(name='Unchanged baseline,independent defect and identical physical readout:'+label,passed=True))
                inputs.extend([archive_path,prior_path])
    test(checks,'Independent SVD of baseline and both corrected comparisons',maximum_svd)
    import ast
    old_tree=ast.parse((PARENT/'adjacent_source_common.py').read_text(encoding='utf-8'))
    new_tree=ast.parse((ROOT/'holdout_common.py').read_text(encoding='utf-8'))
    for function_name in ['owned_loop','expensive_components']:
        old_function=next(node for node in old_tree.body if isinstance(node,ast.FunctionDef) and node.name==function_name)
        new_function=next(node for node in new_tree.body if isinstance(node,ast.FunctionDef) and node.name==function_name)
        assert ast.dump(old_function)==ast.dump(new_function)
    checks.append(dict(name='Copied event physics and virtual ownership are AST-identical to Stage143',passed=True))
    scripts=sorted(ROOT.glob('*.py'))
    for script in scripts:
        compile(script.read_text(encoding='utf-8'),str(script),'exec')
    assert not list(ROOT.rglob('__pycache__'))
    largest=max(len(files) for directory,directories,files in os.walk(ROOT))
    assert largest<1000
    workbench=POST.parent/'formalization-workbench'
    recent=[path for path in workbench.rglob('*') if path.is_file() and path.stat().st_mtime>STARTED.timestamp()]
    assert not recent
    checks.append(dict(name='Compiled scripts,no bytecode,folder limits,protected workbench unchanged by modification time',passed=True))
    source_report=json.loads((ROOT/'results/holdout-source/status.json').read_text())
    response_report=json.loads((ROOT/'results/holdout-response/status.json').read_text())
    summary=dict(stage=144,scientific_checks=count,passing_scientific_checks=passed,
        retained_failed_checks=count-passed,failed_by_packet=failures,packets=packets,
        independent_temperature_fraction=.5625,theta=source_report['theta'],
        source_errors=source_report['source_relative'],
        energy_errors=source_report['energy_relative'],number_errors=source_report['number_relative'],
        component_metrics=source_report['component_metrics'],
        source_rewrite=source_report['maximum_source_rewrite'],responses=response_report['rows'],
        readouts=readout['rows'],column_order=readout['column_order'],
        maximum_energy_work_residual=maximum_budget,baseline_preserved=True,
        new_event_nodes=5616,new_virtual_coefficients=1008,
        inherited_stage143_flags=6,inherited_stage142_flags=16,inherited_stage141_flags=10,
        new_window_inner_feedback_recomputed=False,event_quadrature_error_bounded=False,
        interpolation_choices_are_error_bounds=False,final_epoch=1e-5,
        next_target='Use the withheld prediction and propagated sensitivities to choose the next actual-temperature or event-grid test; do not fit a new physics coefficient or repeat completed inner histories.')
    write_json(ROOT/'NUMERICAL-SUMMARY.json',summary)
    consumed={path:sha for path,sha in hashes.items() if not Path(path).is_relative_to(ROOT)}
    finish(folder,dict(checks=checks,accepted_scope_verified=all(row['passed'] for row in checks),
        consumed_and_immediate_rehashed=consumed,rehashed_prior_files=len(consumed),
        compiled_scripts=len(scripts),largest_direct_file_count=largest,
        scientific_checks=count,passing_scientific_checks=passed,retained_failed_checks=count-passed,
        protected_workbench_recent_modified_file_count=0),
        __file__,[*inputs,ROOT/'NUMERICAL-SUMMARY.json'])
    print(json.dumps(dict(validation_checks=len(checks),passed=all(row['passed'] for row in checks),
                         science=count,science_passed=passed,flags=count-passed,
                         rehashed_prior_files=len(consumed))),flush=True)
    assert all(row['passed'] for row in checks)


if __name__=='__main__':
    main()
