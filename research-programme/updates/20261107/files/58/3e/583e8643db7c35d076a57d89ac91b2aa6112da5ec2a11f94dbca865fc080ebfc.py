from stage167_common import *


def main():
    modest()
    folder=ROOT/'results/validation'
    folder.mkdir(parents=True,exist_ok=False)
    packet=verify_packet(ROOT/'results/budget')
    assert packet['all_checks_passed']
    chain=ancestors()
    prior_paths={PARENT/name for name in chain[PARENT/'results/stage-integrity.json']['file_hashes']}
    for name,sha in packet['input_hashes'].items():
        assert digest(name)==sha,name
        if not Path(name).is_relative_to(ROOT):
            prior_paths.add(Path(name))
    prior_hashes=authenticate(prior_paths,chain)
    checks,inputs=[],[ROOT/'results/budget/status.json',ROOT/'NUMERICAL-SUMMARY.json']
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    reader=ShapeReadout(ladder.basis,canonical=True)
    summary=json.loads((ROOT/'NUMERICAL-SUMMARY.json').read_text())
    assert len(summary['cases'])==8
    for label in summary['cases']:
        path=ROOT/'results/budget'/(label+'.npz')
        data=read_npz(path)
        inputs.append(path)
        assert all(np.isfinite(value).all() for value in data.values() if value.dtype.kind in 'fci')
        heat=float(data['heat'])
        channels=list(data['channels'])
        selected=list(data['selected'])
        assert selected==['endpoint65','incoming13_last','incoming38_last','incoming820_last','time_response']
        assert 'endpoint64' not in selected and 'arithmetic' not in selected and 'twofold_low' not in selected
        assert np.array_equal(data['frequency'],reader.frequency) and np.array_equal(data['measure'],reader.measure)
        assert data['source_potential'].shape==(11,700,2)
        assert data['source_energy'].shape==(11,2)
        assert data['central_potential'].shape==(700,9)
        for position,name in enumerate(channels):
            potential=data['source_potential'][position]
            energy=data['source_energy'][position]
            distortion=potential-reader.frequency[:,None]*energy[None,:]/reader.capacity
            amplitudes=np.linalg.lstsq(np.sqrt(reader.measure)[:,None]*reader.templates,
                np.sqrt(reader.measure)[:,None]*distortion,rcond=None)[0]
            residual=distortion-reader.templates@amplitudes
            independent=np.vstack([heat*(energy/reader.capacity-reader.shifts@amplitudes),heat*amplitudes,
                abs(heat)*norm(residual,reader.measure),abs(heat)*norm(distortion,reader.measure),abs(heat)*norm(potential,reader.measure)])
            close(checks,'IndependentSVD metrics:'+label+':'+name,independent,data['channel_metrics'][position],1e-10)
            close(checks,'IndependentSVD residual:'+label+':'+name,heat*residual,data['channel_residual'][position],1e-10)
            orthogonal=(reader.templates.T*reader.measure)@residual
            scale=reader.template_norms[:,None]*np.maximum(norm(distortion,reader.measure),1e-300)
            test(checks,'Weighted orthogonality:'+label+':'+name,float(np.max(abs(orthogonal)/scale)),1e-10)
        index=[channels.index(name) for name in selected]
        direct_allowance=sum(abs(data['channel_metrics'][position]) for position in index)
        direct_envelope=sum(abs(data['channel_residual'][position]) for position in index)
        close(checks,'Independent allowance sum:'+label,direct_allowance,data['allowance'],1e-10)
        close(checks,'Independent frequency envelope:'+label,direct_envelope,data['pointwise'],1e-10)
        close(checks,'Pointwise envelope norm below triangle sum:'+label,np.minimum(norm(direct_envelope,reader.measure),direct_allowance[3]),norm(direct_envelope,reader.measure),1e-10)
        region_masks=np.array([(reader.frequency>=lower)&(reader.frequency<upper) for lower,upper in zip(data['region_edges'][:-1],data['region_edges'][1:])])
        assert np.all(region_masks.sum(axis=0)==1)
        close(checks,'Independent envelope region partition:'+label,data['envelope_power'].sum(axis=0),norm(direct_envelope,reader.measure)**2,1e-10)
        model,route,match=label.split('-')
        parent_path=PARENT/'results/comparison'/f'{model}-{route}-4096-{match}.npz'
        parent=read_npz(parent_path)
        assert np.array_equal(data['central_potential'][:,:1],parent['potential'][:,:1])
        assert np.array_equal(data['central_potential'][:,5:7],parent['potential'][:,3:5])
        assert np.array_equal(data['central_potential'][:,7:9],parent['potential'][:,7:9])
        assert np.any(data['central_potential'][:,:1])
        checks.append(dict(name='Actual baseline and current MTS/total bitwise preserved:'+label,passed=True))
        joined=reader.split_values(data['central_potential'],data['central_energy'])
        close(checks,'Independent central metrics:'+label,metrics(joined,heat,reader.measure),data['central_metrics'],1e-10)
        for signal in ['endpoint65','time_response']:
            position=channels.index(signal)
            corrupted=[]
            close(corrupted,'Injected1e-6 spectral corruption',data['channel_residual'][position]*1.000001,data['channel_residual'][position],1e-10)
            assert not corrupted[0]['passed']
            checks.append(dict(name='Corruption rejected:'+label+':'+signal,passed=True))
    assert summary['band_orders']==[6,6,6,8,7,7,6]
    assert summary['response_counts']==[2048,4096] and summary['readout_nodes']==700
    assert summary['new_event_evaluations']==summary['new_response_evolutions']==0
    assert not summary['temperature_curve_changed'] and not summary['tolerances_changed']
    assert not summary['baseline_inner_rerun'] and not summary['geometric_tail_assumed']
    assert not summary['statistical_independence_assumed'] and summary['global_numerical_error_bound'] is None
    assert len(summary['unresolved_axes'])==8
    checks.append(dict(name='Partial budget scope,not total accuracy;fixed controls',passed=True))
    scripts=list(ROOT.glob('*.py'))
    for script in scripts:
        compile(script.read_text(encoding='utf-8'),str(script),'exec')
    assert not list(ROOT.rglob('__pycache__'))
    modified=[str(path) for path in (POST.parent/'formalization-workbench').rglob('*') if path.is_file() and path.stat().st_mtime>STARTED.timestamp()]
    assert not modified,modified[:10]
    largest=max(sum(path.is_file() for path in directory.iterdir()) for directory in [ROOT,*[path for path in ROOT.rglob('*') if path.is_dir()]])
    assert largest<=500
    checks.append(dict(name='Compile,no bytecode,folder cap and protected-workbench mtime guard',passed=True))
    failures=[row for row in checks if not row['passed']]
    finish(folder,dict(checks=checks,rehashed_prior_files=len(prior_hashes),consumed_and_immediate_rehashed=prior_hashes,
        compiled_scripts=len(scripts),largest_direct_file_count=largest,accepted_scope_verified=not failures,
        protected_workbench_recent_modified_file_count=0,
        protected_check_scope='Modification-time guard since16:30:22UTC19Oct2026,not a pre-turn content snapshot.'),inputs)
    print(json.dumps(dict(checks=len(checks),failures=failures,prior_files=len(prior_hashes))),flush=True)
    assert not failures,failures


if __name__=='__main__':
    main()
