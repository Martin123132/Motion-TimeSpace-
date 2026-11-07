from stage164_common import *


def main():
    modest()
    folder=ROOT/'results/validation'
    folder.mkdir(parents=True,exist_ok=False)
    chain=ancestors()
    locations=[ROOT/'results'/name for name in ['preflight','sources','legacy-update','reference','baseline-check','phase-diagnosis','state-roundoff-probe']]
    locations.extend(ROOT/'runs'/endpoint/f'order{order}' for endpoint in ENDPOINTS for order in [4,5,6])
    if (ROOT/'results/comparison/status.json').exists():
        locations.append(ROOT/'results/comparison')
        locations.extend(path.parent for path in (ROOT/'results/response').glob('*/status.json'))
    checks,packets,rehashed=[],{},{}
    prior_paths={PARENT/name for name in chain[PARENT/'results/stage-integrity.json']['file_hashes']}
    for location in locations:
        packet=verify_packet(location)
        packets[str(location)]=packet
        failures=[row for row in packet['checks'] if not row['passed']]
        if location==ROOT/'results/legacy-update' or location==ROOT/'results/sources':
            assert all(row['name'].startswith(('60digit independent photon/gas:','60digit unprojected spectral moment:',
                'Float independent photon/gas:','Float unprojected spectral moment:')) for row in failures)
        elif location==ROOT/'results/reference':
            assert all(row['name'].startswith('Unchanged phase gate:') for row in failures)
        elif location==ROOT/'results/comparison':
            assert all(row['name'].startswith('CONVERGENCE:') for row in failures)
        else:
            assert not failures,(location,failures)
        for filename,sha in packet['input_hashes'].items():
            path=Path(filename)
            if filename not in rehashed:
                assert digest(path)==sha,path
                rehashed[filename]=sha
                if not path.is_relative_to(ROOT):
                    prior_paths.add(path)
        checks.append(dict(name='Completed packet and consumed hashes:'+str(location.relative_to(ROOT)),passed=True))
    prior_hashes=authenticate(prior_paths,chain)
    source=read_npz(ROOT/'results/sources/source.npz')
    prior=read_npz(PARENT/'results/sources/source.npz')
    assert all(np.array_equal(source[key],prior[key]) for key in prior)
    checks.append(dict(name='All prior source/improved-band/temperature arrays bitwise preserved',passed=True))
    proof=packets[str(ROOT/'results/preflight')]
    exacts={}
    replayed=0
    with localcontext() as context:
        context.prec=60
        for endpoint_index,endpoint in enumerate(ENDPOINTS):
            bundle=EpochBundle(ENDPOINTS[endpoint])
            theta=proof['contexts'][endpoint][0]['theta']
            norm0,norm1=[Decimal.from_float(float(value)) for value in bundle.basis.norms[:2]]
            mean=Decimal.from_float(float(bundle.basis.mean))
            for order in [4,5,6]:
                primitive=np.empty((7,3,3,4),dtype=object)
                primitive.fill(Decimal(0))
                for node in integration_nodes(theta,order):
                    values=read_npz(moment_path(endpoint,order,node['index']))
                    old=read_npz(parent163.moment_path(endpoint,order,node['index']))
                    parameters,weight=parameters_and_weight(theta,node)
                    assert json.loads(str(values['identity']))==node and float(values['weight'])==weight
                    assert np.array_equal(values['virtual'],old['virtual']) and np.array_equal(values['state'],old['state'])
                    panel=int(np.searchsorted(BOUNDARIES,node['frequency'])-1)
                    for component_index,component in enumerate(COMPONENTS):
                        for moment_index in range(3):
                            for column in range(4):
                                primitive[panel,component_index,moment_index,column]+=Decimal.from_float(-weight)*Decimal.from_float(float(values[component][moment_index,column]))
                    replayed+=1
                lower=np.stack([primitive[:,:,0],primitive[:,:,1]/norm0,
                    (primitive[:,:,0]-mean*primitive[:,:,1])/norm1,primitive[:,:,2]],axis=2)
                exacts[(endpoint,order)]=lower
                saved_json=json.loads((ROOT/'results/sources'/f'{endpoint}-order{order}-moments.json').read_text())
                saved=np.array([Decimal(value) for value in saved_json['values']],dtype=object).reshape(saved_json['shape'])
                assert np.array_equal(lower,saved)
                expected=source[f'soft_endpoint_panels{order}'][:,endpoint_index]
                assert np.array_equal(expected[:,:,[0,1,2,97]],np.asarray(lower,dtype=float))
                prior_panel=read_npz(SOURCE162/'results/sources'/f'{endpoint}-order{order}-panels.npz')['panels']
                assert np.array_equal(expected[:,:,3:97],prior_panel[:,:,3:97])
                checks.append(dict(name=f'Independent primitive replay and retained higher rows:{endpoint}:{order}',passed=True))
            for step,high,low in [('54',5,4),('65',6,5),('64',6,4)]:
                delta=(exacts[(endpoint,high)]-exacts[(endpoint,low)]).sum(axis=(0,1))
                assert np.array_equal(np.asarray(delta,dtype=float),source[f'soft_{endpoint}_total{step}'][[0,1,2,97]])
                checks.append(dict(name='Independent physical-step60digit replay:'+endpoint+':'+step,passed=True))
    assert replayed==7560
    checks.append(dict(name='All7560 original weights and updated real primitives replayed',passed=True))
    diagnosis=packets[str(ROOT/'results/phase-diagnosis')]
    with localcontext() as context:
        context.prec=80
        for label,record in diagnosis['records'].items():
            window,route,step=label.split('-')
            high,low={'54':(5,4),'65':(6,5),'64':(6,4)}[step]
            for diagnostic,case in record.items():
                value=np.array([Decimal(0)]*4,dtype=object)
                for endpoint,index in ([('start',4)] if window=='earlier' else [('start',0),('end',4)]):
                    term=(exacts[(endpoint,high)]-exacts[(endpoint,low)]).sum(axis=(0,1))[:,case['column']]
                    value+=Decimal.from_float(case['weights'][index])*term
                residuals=dict(energy=value[0],pair=value[0]+value[-1],
                    moment=Decimal.from_float(float(source['temperature'][0]))*value[1]+Decimal.from_float(float(source['temperature'][1]))*value[2]-value[0])
                for kind,residual in residuals.items():
                    expected=Decimal(case['exact_'+kind])
                    assert abs(residual-expected)<Decimal('1e-55'),(label,diagnostic,kind)
            checks.append(dict(name='Independent exact phase cancellation:'+label,passed=True))
    state_probe=packets[str(ROOT/'results/state-roundoff-probe')]
    assert state_probe['probes']==12 and not state_probe['source_adopted'] and not state_probe['state_full_bank_repaired']
    for label,record in state_probe['records'].items():
        endpoint,order_tag,node_tag=label.split('-')
        saved=read_npz(moment_path(endpoint,int(order_tag[5:]),int(node_tag[4:])))
        values=read_npz(ROOT/'results/state-roundoff-probe'/(label+'.npz'))
        assert np.array_equal(saved['state'],values['old'])
        assert np.array_equal(saved['difference'],values['old_real'])
        assert np.max(abs(values['new']-values['old']))/np.max(abs(values['old']))<=1e-10
        assert np.max(abs(values['new'][0]+values['new'][-1])/np.maximum(abs(values['new'][0]),1e-300))<=1e-10
        assert not record['source_adopted'] and not record['full_bank_state_repaired']
        checks.append(dict(name='Independent diagnostic state probe versus retained full-bank source:'+label,passed=True))
    reference=packets[str(ROOT/'results/reference')]
    ref_arrays=read_npz(ROOT/'results/reference/reference.npz')
    with localcontext() as context:
        context.prec=60
        for endpoint in ENDPOINTS:
            packet=json.loads((ROOT/'results/sources'/f'{endpoint}-source4-exact.json').read_text())
            saved=np.array([Decimal(value) for value in packet['saved']],dtype=object).reshape(4,4)
            repaired=np.array([Decimal(value) for value in packet['full']],dtype=object).reshape(4,4)
            arithmetic=np.array([Decimal(value) for value in packet['update']],dtype=object).reshape(4,4)
            assert np.max(abs(repaired-saved-arithmetic))<Decimal('1e-55')
            expected=ref_arrays[endpoint+'_coordinate_reference']
            raw=ref_arrays[endpoint+'_raw_reference']
            assert np.array_equal(raw,source[f'soft_{endpoint}_update4'])
            assert np.array_equal(expected[0],raw[0]) and np.array_equal(expected[-1],-raw[0])
            assert np.array_equal(expected[1],raw[1]) and np.array_equal(expected[3:-1],raw[3:-1])
            checks.append(dict(name='Independent numerical-reference channel and unchanged non-pivot rows:'+endpoint,passed=True))
            for kind in ['pair','moment']:
                terms=reference['records'][endpoint]['defects']
                values={name:np.array([Decimal(value) for value in terms[name][kind]],dtype=object) for name in terms}
                assert max(abs(value) for value in values['legacy64']-values['arithmetic']-values['physical64'])<Decimal('1e-55')
                assert max(abs(value) for value in values['repaired4']-values['old']-values['arithmetic'])<Decimal('1e-55')
                checks.append(dict(name='Independent unprojected defect accounting:'+endpoint+':'+kind,passed=True))
    for route in ['local','cubic']:
        for model in ['heavy','cold']:
            for count in COUNTS:
                for match in [20,40]:
                    label=f'{model}-{route}-{count}-m{match}'
                    actual=read_npz(READOUT_OWNER/'results/comparison'/(label+'.npz'))
                    pair=read_npz(ROOT/'results/baseline-check'/(label+'.npz'))
                    assert np.array_equal(pair['baseline_potential'],actual['potential'][:,:1])
                    assert np.array_equal(pair['saved_mts_potential'],actual['potential'][:,3:5])
                    assert np.array_equal(pair['baseline_amplitudes'],actual['amplitudes'][:,:1])
                    assert np.array_equal(pair['saved_mts_amplitudes'],actual['amplitudes'][:,3:5])
                    assert np.any(pair['baseline_potential'])
                    checks.append(dict(name='Actual nonzero baseline/MTS retained:'+label,passed=True))
    summary=json.loads((ROOT/'NUMERICAL-SUMMARY.json').read_text())
    assert summary['physical_source_checks_passed']==packets[str(ROOT/'results/sources')]['all_checks_passed']
    assert summary['reference_replay_qualified']==reference['reference_replay_qualified']
    assert not reference['legacy_raw_update_reclassified']
    assert summary['state_roundoff_probe_events']==12 and not summary['state_roundoff_full_bank_adopted']
    assert summary['phase_diagnosis_checks_passed'] and summary['state_roundoff_probe_passed']
    if not reference['reference_replay_qualified']:
        assert not (ROOT/'results/response').exists()
        assert summary['new_response_evolutions']==0
    checks.append(dict(name='Legacy failures retained and reference qualification controls any replay',passed=True))
    scripts=list(ROOT.glob('*.py'))
    for path in scripts:
        compile(path.read_text(encoding='utf-8'),str(path),'exec')
    assert not list(ROOT.rglob('__pycache__'))
    largest=max(sum(path.is_file() for path in directory.iterdir()) for directory in [ROOT,*[path for path in ROOT.rglob('*') if path.is_dir()]])
    assert largest<=500
    modified=[str(path) for path in (POST.parent/'formalization-workbench').rglob('*') if path.is_file() and path.stat().st_mtime>STARTED.timestamp()]
    assert not modified,modified[:10]
    checks.append(dict(name='Scripts compile,no bytecode,folder cap,protected-workbench mtime guard',passed=True))
    scientific=[row for packet in packets.values() for row in packet['checks']]
    failed=[row['name'] for row in scientific if not row['passed']]
    finish(folder,dict(checks=checks,scientific_checks=len(scientific),passing_scientific_checks=sum(row['passed'] for row in scientific),
        retained_failure_names=failed,compiled_scripts=len(scripts),largest_direct_file_count=largest,
        rehashed_prior_files=len(prior_hashes),consumed_and_immediate_rehashed=prior_hashes,
        weighted_events_replayed=replayed,accepted_scope_verified=all(row['passed'] for row in checks),
        protected_workbench_recent_modified_file_count=0,protected_check_scope='Modification-time scan since03:11UTC19Oct2026,not a content baseline.'),
        __file__,[*rehashed,*prior_hashes,ROOT/'NUMERICAL-SUMMARY.json'])
    print(json.dumps(dict(checks=len(checks),passed=all(row['passed'] for row in checks),scientific_checks=len(scientific),
        retained_failures=len(failed),prior_files=len(prior_hashes),events=replayed,compiled_scripts=len(scripts))),flush=True)
    assert all(row['passed'] for row in checks)


if __name__=='__main__':
    main()
