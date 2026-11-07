from transient_common import *
from validate_source_probe import independent_dual
import re


def main():
    modest()
    folder=ROOT/'results/validation'
    assert not (ROOT/'results/stage-integrity.json').exists()
    folder.mkdir(parents=True,exist_ok=False)
    review=json.loads((ROOT/'ACCURACY-REVIEW.json').read_text())
    scripts=sorted(ROOT.glob('*.py'))
    for script in scripts:
        compile(script.read_bytes(),str(script),'exec')
    script_hashes={digest(script) for script in scripts}
    inputs,consumed,checks=[],set(),[]
    hashes={}
    def hashed(path):
        path=Path(path).resolve()
        if path not in hashes:
            hashes[path]=digest(path)
        return hashes[path]
    packets=sorted(path for path in (ROOT/'results').glob('*/status.json') if path.parent!=folder)
    failures={}
    scientific=passing=0
    for path in packets:
        packet=json.loads(path.read_text())
        assert packet['state']=='complete' and (path.parent/'COMPLETE').is_file()
        assert packet['script_sha256'] in script_hashes
        failed=[row['name'] for row in packet['checks'] if not row['passed']]
        assert all(name.startswith(('Refinement1percent:','Source1percent:')) or
            (name.startswith('Response:') and name.endswith(':gas')) for name in failed),(path,failed)
        if failed:
            failures[path.parent.name]=failed
        assert packet['count']==len(packet['checks']) and packet['all_checks_passed']==(not failed)
        for source,sha in packet['input_hashes'].items():
            assert hashed(source)==sha,source
            consumed.add(Path(source))
        for archive in path.parent.glob('*.npz'):
            values=read_npz(archive)
            assert all(np.isfinite(value).all() for value in values.values() if value.dtype.kind not in ['U','S'])
            inputs.append(archive)
        inputs.append(path)
        scientific+=len(packet['checks'])
        passing+=sum(bool(row['passed']) for row in packet['checks'])
        checks.append(dict(name='Finite sourced packet:'+path.parent.name,passed=True))
    assert len(packets)==10
    assert failures==review['expected_failed_by_packet']
    assert scientific==review['scientific_checks'] and passing==review['passing_scientific_checks']
    sampling_path=refined_owner('heavy')/'results/inner-heavy-n40960/prediction.npz'
    sampling_parent=read_npz(sampling_path)
    start,end=sampling_parent['coordinate'][[0,-1]]
    response_points=np.array([float(start+(end-start)*index/2048) for index in range(33)])
    replay_points=start+(end-start)*np.arange(0,641,20)/40960
    coordinate_roundoff=float(np.max(abs(response_points-replay_points)))
    assert coordinate_roundoff<=4*np.spacing(float(end))
    inserted=(response_points[:-1]+response_points[1:])/2
    invisible_coordinate=np.sort(np.concatenate([response_points,inserted]))
    invisible_values=np.zeros(len(invisible_coordinate))
    invisible_values[np.searchsorted(invisible_coordinate,inserted)]=1.
    invisible=interpolate.interp1d(invisible_coordinate,invisible_values)
    assert np.array_equal(invisible(response_points),np.zeros(33))
    assert np.array_equal(invisible(inserted),np.ones(32))
    inputs.append(sampling_path)
    consumed.add(sampling_path)
    checks.append(dict(name='Finite32-point response sampling contract and unseen-between-step control',
        coordinate_roundoff=coordinate_roundoff,passed=True))
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    basis=ladder.basis
    inputs.extend(ladder.inputs)
    consumed.update(ladder.inputs)
    for model in ['heavy','cold']:
        owner=refined_owner(model)
        old_path=owner/'results'/f'inner-{model}-n40960/prediction.npz'
        parent=read_npz(old_path)
        old_quarter_path=PARENT/'results'/f'replay-{model}-s00000/prediction.npz'
        old_quarter=read_npz(old_quarter_path)
        replay_folder=ROOT/'results'/f'replay-{model}-s00000'
        replay=read_npz(replay_folder/'prediction.npz')
        frozen=read_npz(replay_folder/'frozen-reference.npz')
        law=read_npz(replay_folder/'initial-law.npz')
        first=read_npz(replay_folder/'first-step-law.npz')
        generator=sparse.load_npz(replay_folder/'initial-generator.npz')
        first_generator=sparse.load_npz(replay_folder/'first-generator.npz')
        status=json.loads((replay_folder/'status.json').read_text())
        record_path=Path(status['original_restart'])
        record=json.loads(record_path.read_text())
        snapshot_path=record_path.parent/record['archive']
        assert hashed(snapshot_path)==record['archive_sha256']
        snapshot=read_npz(snapshot_path)
        assert int(snapshot['completed_step'])==0 and not np.count_nonzero(snapshot['error'])
        assert np.array_equal(replay['defect'][0],snapshot['error'])
        assert np.array_equal(replay['outer_slope'][0],snapshot['old_outer'])
        assert np.array_equal(replay['saved_step_indices'],SAMPLE_STEPS)
        assert np.array_equal(frozen['saved_step_indices'],SAMPLE_STEPS)
        assert not np.count_nonzero(frozen['defect'][0]) and not np.count_nonzero(law['initial_error'])
        for key in ['frequency','coefficient_knots','coefficient_bank','offsets']:
            assert np.array_equal(replay[key],parent[key]),key
        for old_index,step in enumerate(old_quarter['saved_step_indices']):
            selected=int(np.flatnonzero(SAMPLE_STEPS==step)[0])
            for key in ['defect','outer_slope','slope','lower_target']:
                assert np.array_equal(replay[key][selected],old_quarter[key][old_index])
        assert int(replay['steps'])==40960 and int(replay['stop_step'])==640
        step=float(law['step'])
        assert np.array_equal(law['initial_drive'],law['initial_source']-law['outer_derivative'])
        for label,matrix,values,force in [
            ('frozen',sparse.eye(5265)-step*generator,first['frozen'],step*law['initial_drive']),
            ('actual',sparse.eye(5265)-step*first_generator,first['actual'],step*first['generator_source']-(first['outer']-first['old_outer']))]:
            denominator=np.maximum(np.max(abs(matrix)@abs(values)+abs(force),axis=0),1e-300)
            residual=np.max(abs(matrix@values-force),axis=0)/denominator
            assert max(residual)<1e-10
            checks.append(check('Independent first-step resolvent:'+model+':'+label,max(residual),1e-10))
        assert np.array_equal(first['actual'],replay['defect'][1])
        assert np.array_equal(first['frozen'],frozen['defect'][1])
        inputs.extend([old_path,old_quarter_path,record_path,snapshot_path])
        consumed.update([old_path,old_quarter_path,record_path,snapshot_path])
        checks.append(dict(name='Initial matching,fixed controls and bitwise quarters:'+model,passed=True))
    for upper in [.04,.02]:
        label=int(upper*1000)
        bank_folder=ROOT/'results'/f'operator-m{label}'
        bank=read_npz(bank_folder/'bank.npz')
        status=json.loads((bank_folder/'status.json').read_text())
        prior_path=PARENT/'results'/f'operator-m{label}/bank.npz'
        prior=read_npz(prior_path)
        assert status['new_soft_temperature_evaluations']==12 and status['reused_temperature_evaluations']==3
        assert np.array_equal(bank['steps'],SOURCE_STEPS[1:-1])
        for index,step in enumerate(bank['steps']):
            event=read_npz(bank_folder/f'event-{step:05d}.npz')
            assert np.array_equal(event['adjoint'],bank['adjoint'][index])
            assert np.all(event['ratios']>0) and np.all(event['rates']>0)
            moment=np.sum(event['rates']*(event['ratios']-1)**2*(event['ratios']+1)/event['ratios']**3)
            expected=bank['weights']*bank['frequency']*moment/(2*I3)
            assert np.linalg.norm(basis.temperature@event['adjoint']-expected)/np.linalg.norm(expected)<1e-10
            if int(step) in [160,320,480]:
                selected=int(np.flatnonzero(prior['steps']==step)[0])
                assert np.array_equal(bank['adjoint'][index],prior['adjoint'][selected])
        inputs.append(prior_path)
        consumed.add(prior_path)
        checks.append(dict(name='Shared source bank and bitwise three-operator reuse:'+str(upper),passed=True))
    for model in ['heavy','cold']:
        background=thermal_wave.thermal.ThermalBackground(model)
        for upper in [.04,.02]:
            label=int(upper*1000)
            probe=ROOT/'results'/f'transient-{model}-m{label}'
            status=json.loads((probe/'status.json').read_text())
            assert not status['inner_coefficients_resampled'] and not status['other_source_intervals_changed']
            assert status['source_subdivisions']==[4,8,16] and status['source_knot_counts']==[110,114,122]
            evaluated={variant:read_npz(probe/(variant+'-evaluated.npz')) for variant in ['assembled','direct','frozen']}
            assert np.array_equal(evaluated['assembled']['source'][:,1:],evaluated['direct']['source'][:,1:])
            frozen_delta=evaluated['frozen']['source']-evaluated['direct']['source']
            diagnostic=status['frozen_source_diagnostic']
            components=np.maximum(independent_dual(evaluated['frozen']['source'][1:],basis).sum(axis=1),
                independent_dual(evaluated['direct']['source'][1:],basis).sum(axis=1))
            expected=independent_dual(frozen_delta[1:].sum(axis=1),basis)/np.maximum(components,1e-300)
            assert np.allclose(diagnostic['relative_to_components'],expected,rtol=1e-8,atol=0)
            for variant in ['assembled','direct']:
                old_folder=PARENT/'results'/f'probe-{model}-m{label}'
                old_source_path=old_folder/(variant+'-source.npz')
                old_response_path=old_folder/(variant+'-response.npz')
                old_source,old_response=read_npz(old_source_path),read_npz(old_response_path)
                inputs.extend([old_source_path,old_response_path])
                consumed.update([old_source_path,old_response_path])
                previous=old_response
                changes=[]
                for refinement in ['control',8,16]:
                    source=read_npz(probe/f'{variant}-{refinement}-source.npz')
                    response=read_npz(probe/f'{variant}-{refinement}-response.npz')
                    reference=old_response if refinement=='control' else previous
                    assert len(source['coordinate'])==(114 if refinement==8 else 122)
                    assert np.all(np.diff(source['coordinate'])>0)
                    selected=np.searchsorted(source['coordinate'],old_source['coordinate'])
                    for key,value in old_source.items():
                        if value.ndim>0 and value.shape[0]==110:
                            assert np.array_equal(source[key][selected],value),key
                    extra=np.ones(len(source['coordinate']),dtype=bool)
                    extra[selected]=False
                    assert np.all(source['coordinate'][extra]<evaluated[variant]['coordinate'][-1])
                    if refinement=='control':
                        control=interpolate.interp1d(old_source['coordinate'],old_source['source'],axis=0)(source['coordinate'])
                        assert np.array_equal(source['source'][extra],control[extra])
                    else:
                        eval_selection=np.searchsorted(evaluated[variant]['coordinate'],source['coordinate'][extra])
                        assert np.array_equal(source['source'][extra],evaluated[variant]['source'][eval_selection])
                    assert np.array_equal(response['coordinate'],old_response['coordinate'])
                    assert len(response['coordinate'])==2049 and int(response['integration_steps'])==2048
                    assert np.array_equal(response['unresolved_change'],old_response['unresolved_change'])
                    scale=np.maximum((abs(response['energy'])+background.chi*abs(response['gas'])+abs(response['work'])).max(axis=0),1e-300)
                    assert np.max(abs(response['energy']+background.chi*response['gas']+response['work'])/scale)<1e-7
                    metric=status['comparisons'][variant][str(refinement)]['comparison']
                    delta=response['gas'][:,:3]-reference['gas'][:,:3]
                    assert np.array_equal(metric['gas_endpoint_signed_difference'],delta[-1])
                    for key,selection in [('gas_peak_relative',slice(None)),('gas_late_relative',slice(1536,None))]:
                        expected=abs(delta[selection]).max(axis=0)/np.maximum(abs(reference['gas'][selection,:3]).max(axis=0),1e-300)
                        assert np.allclose(metric[key],expected,atol=0,rtol=1e-12)
                    expected=abs(delta[-1])/np.maximum(abs(reference['gas'][-1,:3]),1e-300)
                    assert np.allclose(metric['gas_endpoint_relative'],expected,atol=0,rtol=1e-12)
                    radiation=norm(response['physical_change']-reference['physical_change'],basis.measure)/np.maximum(norm(reference['physical_change'],basis.measure),1e-300)
                    assert np.allclose(metric['radiation_relative'],radiation,atol=0,rtol=1e-12)
                    parts=np.stack([response['gas'][-1,offset:offset+3] for offset in [3,6,9]])
                    assert np.array_equal(metric['gas_endpoint_components'],parts)
                    if refinement=='control':
                        assert max(metric['gas_peak_relative'])<1e-7 and max(metric['radiation_relative'])<1e-7
                    else:
                        changes.append(delta)
                        previous=response
                    checks.append(dict(name='Fixed response,unchanged knots and independent metrics:'+model+':'+str(upper)+':'+variant+':'+str(refinement),passed=True))
                expected=abs(changes[1][-1])/np.maximum(abs(changes[0][-1]),1e-300)
                assert np.allclose(status['convergence'][variant]['endpoint_difference_ratio'],expected,rtol=1e-12,atol=0)
            for refinement in ['control',8,16]:
                assembled=read_npz(probe/f'assembled-{refinement}-response.npz')
                direct=read_npz(probe/f'direct-{refinement}-response.npz')
                assert np.array_equal(assembled['gas'][:,6:],direct['gas'][:,6:])
            checks.append(dict(name='Frozen source,contraction and unchanged DC/BR responses:'+model+':'+str(upper),passed=True))
    chain=ancestors()
    parent=chain[PARENT/'results/stage-integrity.json']
    rehashed=set()
    for name,sha in parent['file_hashes'].items():
        path=PARENT/name
        assert hashed(path)==sha,path
        rehashed.add(path)
    for path in consumed:
        if not path.is_relative_to(ROOT):
            verify_source(path,chain)
            rehashed.add(path)
    inherited_count=sum(len(packet['file_hashes']) for packet in chain.values())
    assert inherited_count==204997
    documents=sorted(ROOT.glob('*.md'))
    for document in documents:
        for reference in re.findall(chr(96)+'([^'+chr(96)+']+)'+chr(96),document.read_text(encoding='utf-8')):
            if reference.endswith(('.md','.py','.json','.npz','.pdf')):
                assert (ROOT/reference).resolve().is_file(),reference
    maximum=max(len(files) for directory,directories,files in os.walk(ROOT))
    assert maximum<1000 and not list(ROOT.rglob('__pycache__')) and not list(ROOT.rglob('*.tmp'))
    workbench=POST.parent/'formalization-workbench'
    changed=[str(path) for path in workbench.rglob('*') if path.is_file() and path.stat().st_mtime>STARTED.timestamp()]
    assert workbench.is_dir() and not changed,changed
    checks.append(dict(name='Parent,consumed sources,citations,capacity and protected-workbench scan',passed=True))
    finish(folder,dict(checks=checks,scientific_checks=scientific,passing_scientific_checks=passing,
        retained_failed_checks=scientific-passing,retained_failure_names=failures,compiled_scripts=len(scripts),
        checked_science_packets=len(packets),accepted_scope_verified=True,largest_direct_file_count=maximum,
        inherited_payload_count=inherited_count,replayed_steps=1280,completed_backgrounds=['heavy','cold'],
        consumed_and_immediate_rehashed={str(path):hashed(path) for path in sorted(rehashed)}),
        __file__,[*inputs,*scripts,*documents,ROOT/'ACCURACY-REVIEW.json',ROOT/'NUMERICAL-SUMMARY.json'])
    print(json.dumps(dict(science=scientific,passes=passing,failures=scientific-passing,
        validation_checks=len(checks),rehashed=len(rehashed))),flush=True)


if __name__=='__main__':
    main()
