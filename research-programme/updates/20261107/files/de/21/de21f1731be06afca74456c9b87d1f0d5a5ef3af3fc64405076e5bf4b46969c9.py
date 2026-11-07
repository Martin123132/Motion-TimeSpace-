from stage147_step_common import *


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
    checks=[dict(name='All immediate Stage146 payloads unchanged',passed=True)]
    frozen_path=ROOT/'results/preflight/frozen-method.json'
    frozen=json.loads(frozen_path.read_text())
    assert digest(ROOT/'ACCEPTANCE.md')==frozen['acceptance_sha256']
    assert digest(ROOT/'DERIVATION.md')==frozen['derivation_sha256']
    assert digest(PARENT/'results/repaired-readiness/source.npz')==frozen['source_sha256']
    checks.append(dict(name='Frozen physical source and predeclared method unchanged',passed=True))
    packets=['results/preflight',*['results/response/'+model+'-'+str(count)+'/'+phase
        for model in ['heavy','cold'] for count in [2048,4096] for phase in ['active','transfer']],
        'results/comparison']
    inputs=[frozen_path]
    count_science=passed=0
    failures={}
    for name in packets:
        report=json.loads((ROOT/name/'status.json').read_text())
        assert report['state']=='complete' and (ROOT/name/'COMPLETE').exists()
        assert report['count']==len(report['checks'])
        bad=[row['name'] for row in report['checks'] if not row['passed']]
        if bad:
            assert name=='results/comparison' and all(item.startswith('CONVERGENCE:') for item in bad)
            failures[name]=bad
        for filename,sha in report['input_hashes'].items():
            path=Path(filename)
            assert hashed(path)==sha,path
            if not path.is_relative_to(ROOT):
                inherited.inherited.verify_source(path,chain)
        count_science+=report['count']
        passed+=sum(bool(row['passed']) for row in report['checks'])
        inputs.append(ROOT/name/'status.json')
        checks.append(dict(name='Complete sourced packet:'+name,passed=True))
    comparison=json.loads((ROOT/'results/comparison/status.json').read_text())
    assert comparison['counts']==COUNTS and comparison['modes']==96
    assert not comparison['baseline_inner_history_refined']
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    reader=ShapeReadout(ladder.basis,canonical=True)
    maximum_budget=maximum_gate=maximum_svd=0.
    for model in ['heavy','cold']:
        heat=comparison['metadata'][model]['heat']
        saved_initial=read_npz(response_folder(model,1024,'active')/'response.npz')
        for count in COUNTS:
            data={phase:read_npz(response_folder(model,count,phase)/'response.npz') for phase in ['active','transfer']}
            for key in ['photon','energy','gas','work','integrated_number_source']:
                assert np.array_equal(data['active'][key][0],saved_initial[key][0])
                assert np.array_equal(data['active'][key][-1],data['transfer'][key][0])
            checks.append(dict(name='Unchanged initial state and continuous restart:'+model+':'+str(count),passed=True))
            for phase,value in data.items():
                assert value['photon'].shape==(count+1,96,12)
                assert all(np.isfinite(array).all() for array in value.values())
                for key in ['photon','energy','gas','work','integrated_number_source']:
                    assert np.array_equal(value[key][...,6:8],np.zeros_like(value[key][...,6:8]))
                budget=value['energy']+heat*value['gas']+value['work']
                scale=np.maximum(np.max(abs(value['energy'])+abs(heat*value['gas'])+abs(value['work']),axis=0),1e-300)
                error=float(np.max(abs(budget-budget[0])/scale))
                maximum_budget=max(maximum_budget,error)
                test(checks,'Independent stored energy-work budget:'+model+':'+str(count)+':'+phase,error,1e-7)
                phase_report=json.loads((response_folder(model,count,phase)/'status.json').read_text())
                maximum_gate=max(maximum_gate,phase_report['metrics']['source_rewrite'])
                inputs.append(response_folder(model,count,phase)/'response.npz')
            for match in [20,40]:
                key=f'{model}-m{match}'
                label=key+'-'+str(count)
                result_path=ROOT/'results/comparison'/(label+'.npz')
                result=read_npz(result_path)
                prior_path=PARENT/'results/spectral-readout'/(key+'-cubic.npz')
                prior=read_npz(prior_path)
                assert np.array_equal(result['frequency'],prior['frequency'])
                assert np.array_equal(result['measure'],prior['measure'])
                assert np.array_equal(result['potential'][:,:3],prior['potential'][:,:3])
                assert np.array_equal(result['amplitudes'][:,:1],prior['amplitudes'][:,:1])
                assert np.array_equal(result['potential'][:,15:17],reader.values@data['transfer']['photon'][-1,:,4:6])
                distortion=result['potential']-reader.frequency[:,None]*(result['energy']/reader.capacity)
                alternate=np.linalg.lstsq(np.sqrt(reader.measure)[:,None]*reader.templates,
                    np.sqrt(reader.measure)[:,None]*distortion,rcond=None)[0]
                error=reader.templates@(alternate-result['amplitudes'])
                error_norm=np.sqrt((reader.measure[:,None]*error**2).sum(axis=0))
                distortion_norm=np.sqrt((reader.measure[:,None]*distortion**2).sum(axis=0))
                maximum_svd=max(maximum_svd,float(np.max(error_norm/np.maximum(distortion_norm,1e-300))))
                assert np.array_equal(np.array(comparison['readouts'][label]['metrics']['mu']),heat*result['amplitudes'][0])
                assert np.array_equal(np.array(comparison['readouts'][label]['metrics']['y']),heat*result['amplitudes'][1])
                checks.append(dict(name='Baseline/MTS identical per-column decomposition:'+label,passed=True))
                inputs.extend([result_path,prior_path])
        for phase in ['active','transfer']:
            data=[read_npz(response_folder(model,count,phase)/'response.npz') for count in COUNTS]
            records=comparison['state_comparisons'][model][phase]['increment']['pairs']
            for pair_index,(coarse,fine) in enumerate(zip(data[:-1],data[1:])):
                delta=fine['photon'][-1,:,4:6]-coarse['photon'][-1,:,4:6]
                endpoint=np.sqrt(np.maximum(np.sum(delta*(ladder.basis.mass@delta),axis=0),0.))
                reported=np.array(records[pair_index]['absolute']['photon_endpoint'])
                test(checks,'Independent isolated photon convergence norm:'+model+':'+phase+':'+str(pair_index),
                     np.max(abs(endpoint-reported)/np.maximum(endpoint,1e-300)),1e-10)
                gas_error=abs(fine['gas'][-1,4:6]-coarse['gas'][-1,4:6])
                assert np.array_equal(gas_error,np.array(records[pair_index]['absolute']['gas_endpoint']))
    test(checks,'Source rewrite retains1e-10limit at every refined step',maximum_gate,1e-10)
    test(checks,'Independent spectral SVD uses each column own scale',maximum_svd,1e-10)
    for model in ['heavy','cold']:
        for match in [20,40]:
            key=f'{model}-m{match}'
            arrays=[read_npz(ROOT/'results/comparison'/(key+'-'+str(count)+'.npz')) for count in COUNTS]
            heat=comparison['metadata'][model]['heat']
            for row,name in enumerate(['mu','y']):
                values=[heat*array['amplitudes'][row,15:17] for array in arrays]
                relative=abs(values[2]-values[1])/abs(values[2])
                recorded=comparison['spectral_comparisons'][key][name]['increment']['relative_changes'][1]
                assert np.array_equal(relative,np.array(recorded))
                checks.append(dict(name='Isolated '+name+' convergence never scaled by baseline:'+key,passed=True))
    scripts=sorted(ROOT.glob('*.py'))
    for script in scripts:
        compile(script.read_text(encoding='utf-8'),str(script),'exec')
    assert not list(ROOT.rglob('__pycache__'))
    largest=max(len(files) for directory,directories,files in os.walk(ROOT))
    assert largest<1000
    workbench=POST.parent/'formalization-workbench'
    assert not [path for path in workbench.rglob('*') if path.is_file() and path.stat().st_mtime>STARTED.timestamp()]
    checks.append(dict(name='Compiled scripts,no bytecode,folder limit,protected workbench modification-time count0',passed=True))
    summary=dict(stage=147,scientific_checks=count_science,passing_scientific_checks=passed,
        retained_failed_checks=count_science-passed,failed_by_packet=failures,packets=packets,
        counts=COUNTS,frequency_modes=96,convergence_passed=not failures,
        state_comparisons=comparison['state_comparisons'],spectral_comparisons=comparison['spectral_comparisons'],
        readouts=comparison['readouts'],maximum_energy_work_residual=maximum_budget,
        maximum_source_rewrite=maximum_gate,maximum_independent_svd_relative=maximum_svd,
        baseline_preserved=True,baseline_inner_history_refined=False,source_unchanged=True,
        new_event_evaluations=0,new_virtual_loops=0,final_epoch=1e-5,
        accepted_scope='Fixed-source/frequency cubic response time-step test; baseline reanalysis and unchanged-history comparison',
        rigorous_error_bound=False,event_grid_uncertainty_bounded=False,
        next_target=('Extend physical-source coverage into the next colder temperature interval using the saved endpoint; retain this interval and its numerical convergence evidence.'
                     if not failures else 'Investigate the retained failing increment convergence diagnostics before adopting a finest-grid result.'))
    write_json(ROOT/'NUMERICAL-SUMMARY.json',summary)
    consumed={path:sha for path,sha in hashes.items() if not Path(path).is_relative_to(ROOT)}
    finish(folder,dict(checks=checks,accepted_scope_verified=all(item['passed'] for item in checks),
        consumed_and_immediate_rehashed=consumed,rehashed_prior_files=len(consumed),
        compiled_scripts=len(scripts),largest_direct_file_count=largest,
        scientific_checks=count_science,passing_scientific_checks=passed,
        convergence_passed=not failures,protected_workbench_recent_modified_file_count=0),
        __file__,[*inputs,ROOT/'NUMERICAL-SUMMARY.json'])
    print(json.dumps(dict(validation_checks=len(checks),passed=all(item['passed'] for item in checks),
        science=count_science,science_passed=passed,convergence_passed=not failures,
        rehashed_prior_files=len(consumed),maximum_budget=maximum_budget)),flush=True)
    assert all(item['passed'] for item in checks)


if __name__=='__main__':
    main()
