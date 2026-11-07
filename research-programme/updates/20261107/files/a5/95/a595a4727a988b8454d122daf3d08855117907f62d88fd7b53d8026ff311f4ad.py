from adjacent_source_common import *


def main():
    modest()
    folder=ROOT/'results/validation'
    folder.mkdir(parents=True,exist_ok=False)
    chain=ancestors()
    parent=chain[PARENT/'results/stage-integrity.json']
    assert sum(len(packet['file_hashes']) for packet in chain.values())==219863
    hashes={}
    def hashed(path):
        path=Path(path).resolve()
        key=str(path)
        if key not in hashes:
            hashes[key]=digest(path)
        return hashes[key]
    for name,sha in parent['file_hashes'].items():
        assert hashed(PARENT/name)==sha,name
    packets=['results/preflight','runs/expensive-centre','runs/control-centre','runs/expensive-end',
             'runs/control-end','results/adjacent-sources','results/energy-coordinate-readiness','results/adjacent-response','results/spectral-readout']
    checks=[dict(name='Stage142 immediate payloads unchanged',passed=True)]
    count,passed,failures=0,0,{}
    inputs=[]
    for name in packets:
        location=ROOT/name
        report=json.loads((location/'status.json').read_text())
        assert report['state']=='complete' and (location/'COMPLETE').exists()
        assert report['count']==len(report['checks'])
        bad=[row['name'] for row in report['checks'] if not row['passed']]
        if bad:
            assert name=='results/adjacent-sources'
            assert all(item.startswith('INTERPOLATION_DIAGNOSTIC:') or item in ['Temperature moment:centre','Temperature moment:end'] for item in bad)
            failures[name]=bad
        for filename,sha in report['input_hashes'].items():
            path=Path(filename)
            assert hashed(path)==sha,path
            if not path.is_relative_to(ROOT):
                inherited.inherited.verify_source(path,chain)
        count+=report['count']
        passed+=sum(bool(row['passed']) for row in report['checks'])
        inputs.append(location/'status.json')
        checks.append(dict(name='Finite sourced complete packet:'+name,passed=True))
    assert len(list((ROOT/'virtual-cache').rglob('*.json')))==2016
    node_counts={name:len(list((ROOT/name/'nodes').rglob('*.npz'))) for name in packets if name.startswith('runs/')}
    assert sum(node_counts.values())==11232
    checks.append(dict(name='Both complete actual-temperature event populations and virtual coefficients',passed=True))
    source=read_npz(ROOT/'results/adjacent-sources/source.npz')
    preflight=read_npz(ROOT/'results/preflight/frozen-inputs.npz')
    assert np.array_equal(source['start'],preflight['start_source'])
    assert np.array_equal(source['curvature'],source['centre']-(source['start']+source['end'])/2)
    checks.append(dict(name='Reused start unchanged and measured curvature is actual-minus-secant',passed=True))
    response_report=json.loads((ROOT/'results/adjacent-response/status.json').read_text())
    readout_report=json.loads((ROOT/'results/spectral-readout/status.json').read_text())
    parent_readout=json.loads((PARENT/'results/decomposition-v2/status.json').read_text())
    basis=infrared_ladder.ConsistentBasis(**parent_readout['basis_specification'])
    reader=ShapeReadout(basis,canonical=True)
    maximum_svd=0.
    for model in ['heavy','cold']:
        heat=parent_readout['metadata'][model]['heat']
        for count_steps in [256,512,1024]:
            active=read_npz(ROOT/'results/adjacent-response'/f'{model}-active{count_steps}.npz')
            transferred=read_npz(ROOT/'results/adjacent-response'/f'{model}-transfer{count_steps}.npz')
            for key in ['photon','energy','gas','work','integrated_number_source']:
                difference=np.max(abs(transferred[key][0]-active[key][-1]))
                scale=max(float(np.max(abs(active[key][-1]))),1e-300)
                test(checks,'Stored seam retains:'+model+':'+str(count_steps)+':'+key,difference/scale,1e-12)
            for phase,data in [('active',active),('transfer',transferred)]:
                assert data['photon'].shape==(count_steps+1,96,12)
                assert all(np.isfinite(value).all() for value in data.values())
                balance=data['energy']+heat*data['gas']+data['work']
                scale=np.maximum(np.max(abs(data['energy'])+abs(heat*data['gas'])+abs(data['work']),axis=0),1e-300)
                test(checks,'Independent budget:'+model+':'+str(count_steps)+':'+phase,
                     np.max(abs(balance-balance[0])/scale),1e-7)
                assert np.array_equal(data['photon'][:,:,6:8],np.zeros_like(data['photon'][:,:,6:8]))
                assert np.array_equal(data['gas'][:,6:8],np.zeros_like(data['gas'][:,6:8]))
            inputs.extend([ROOT/'results/adjacent-response'/f'{model}-active{count_steps}.npz',
                           ROOT/'results/adjacent-response'/f'{model}-transfer{count_steps}.npz'])
        final=transferred
        new=reader.values@final['photon'][-1,:,2:4]
        for match in [20,40]:
            case=f'{model}-m{match}'
            archive_path=ROOT/'results/spectral-readout'/(case+'.npz')
            data=read_npz(archive_path)
            prior_path=PARENT/'results/decomposition-v2'/f'{case}-physical-canonical700.npz'
            prior=read_npz(prior_path)
            assert np.array_equal(data['potential'][:,0],prior['corrected_potential'][:,0])
            assert np.array_equal(data['potential'][:,1:3],prior['corrected_potential'][:,1:3])
            assert np.array_equal(data['potential'][:,3:5],new)
            assert np.array_equal(data['potential'][:,5:7],data['potential'][:,1:3]+new)
            design=np.sqrt(reader.measure)[:,None]*reader.templates
            distortion=data['potential']-reader.frequency[:,None]*(data['energy']/reader.capacity)
            alternate=np.linalg.lstsq(design,np.sqrt(reader.measure)[:,None]*distortion,rcond=None)[0]
            denominator=max(float(np.max(abs(data['amplitudes']))),1e-300)
            maximum_svd=max(maximum_svd,float(np.max(abs(alternate-data['amplitudes']))/denominator))
            values=readout_report['rows'][case]['metrics']
            assert np.array_equal(np.array(values['mu']),heat*data['amplitudes'][0])
            assert np.array_equal(np.array(values['y']),heat*data['amplitudes'][1])
            assert np.max(abs(np.array(values['joint_captured_squared_fraction'])+
                              np.array(values['residual_norm_fraction'])**2-1))<1e-10
            checks.append(dict(name='Same nonzero baseline plus old and new source;physical units and ratios:'+case,passed=True))
            inputs.extend([archive_path,prior_path])
    test(checks,'Independent SVD of every physical spectral comparison',maximum_svd)
    scripts=sorted(ROOT.glob('*.py'))
    for script in scripts:
        compile(script.read_text(encoding='utf-8'),str(script),'exec')
    assert not list(ROOT.rglob('__pycache__'))
    largest=max(len(files) for directory,directories,files in os.walk(ROOT))
    assert largest<1000
    workbench=POST.parent/'formalization-workbench'
    assert not [path for path in workbench.rglob('*') if path.is_file() and path.stat().st_mtime>STARTED.timestamp()]
    checks.append(dict(name='Compiled scripts,no caches,folder limit and protected workbench unchanged by modification time',passed=True))
    source_report=json.loads((ROOT/'results/adjacent-sources/status.json').read_text())
    summary=dict(stage=143,scientific_checks=count,passing_scientific_checks=passed,
                 retained_failed_checks=count-passed,failed_by_packet=failures,packet_names=packets,
                 physical_source_interval=[.5,.75],previous_source_interval=[.25,.5],
                 represented_source_union=[.25,.75],final_scale=1e-5,
                 full_extra_source_history_complete=False,
                 new_temperature_nodes=source_report['metrics'],
                 response_comparisons=response_report['comparisons'],readouts=readout_report['rows'],
                 physical_column_order=readout_report['column_order'],
                 baseline_preserved=True,old_mts_window_preserved=True,
                 new_event_nodes=11232,new_virtual_coefficients=2016,
                 inherited_stage142_energy_flags=16,inherited_stage141_response_flags=10,
                 new_window_inner_feedback_recomputed=False,event_quadrature_error_bounded=False,
                 next_target='Test the three-anchor source interpolation inside this genuinely new .5U-.75U interval at a withheld temperature, selected before evaluation; use its propagated mu/y/residual effect, not only the source-vector norm, to decide whether another source point is needed. Reuse all new endpoints and existing transfer machinery. No automatic whole-history inner refinement or claim of present-day observation.')
    write_json(ROOT/'NUMERICAL-SUMMARY.json',summary)
    consumed={path:sha for path,sha in hashes.items() if not Path(path).is_relative_to(ROOT)}
    finish(folder,dict(checks=checks,accepted_scope_verified=all(row['passed'] for row in checks),
                       consumed_and_immediate_rehashed=consumed,rehashed_prior_files=len(consumed),
                       all_verified_input_files=len(hashes),compiled_scripts=len(scripts),
                       largest_direct_file_count=largest,scientific_checks=count,
                       passing_scientific_checks=passed,retained_failed_checks=count-passed,
                       protected_workbench_recent_modified_file_count=0),
           __file__,[*inputs,ROOT/'NUMERICAL-SUMMARY.json'])
    print(json.dumps(dict(validation_checks=len(checks),passed=all(row['passed'] for row in checks),
                          scientific_checks=count,scientific_passed=passed,
                          retained_flags=count-passed,rehashed_prior_files=len(consumed),
                          largest_direct_file_count=largest)),flush=True)
    assert all(row['passed'] for row in checks)


if __name__=='__main__':
    main()
