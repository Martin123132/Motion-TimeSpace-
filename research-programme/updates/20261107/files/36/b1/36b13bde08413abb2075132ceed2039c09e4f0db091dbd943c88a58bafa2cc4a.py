from stage165_common import *


def main():
    modest()
    folder=ROOT/'results/validation'
    folder.mkdir(parents=True,exist_ok=False)
    chain=ancestors()
    locations=[ROOT/'results'/name for name in ['preflight','sources','legacy-update','reference','baseline-check']]
    locations.extend(ROOT/'runs'/endpoint/f'order{order}' for endpoint in ENDPOINTS for order in [4,5,6])
    for name in ['phase-diagnosis','reference-stable','comparison']:
        if (ROOT/'results'/name/'status.json').exists():
            locations.append(ROOT/'results'/name)
    for name in ['real-residual-ranking','precise-shift-probe','sources-refined','legacy-update-refined','reference-refined','phase-diagnosis-refined','phase-rounding-diagnosis','reference-certified','basis-representation-diagnosis']:
        if (ROOT/'results'/name/'status.json').exists():
            locations.append(ROOT/'results'/name)
    if (ROOT/'runs/refined').exists():
        locations.extend(ROOT/'runs/refined'/endpoint for endpoint in ENDPOINTS)
    if (ROOT/'results/response').exists():
        locations.extend(path.parent for path in (ROOT/'results/response').glob('*/status.json'))
    checks,packets,rehashed=[],{},{}
    prior_paths={PARENT/name for name in chain[PARENT/'results/stage-integrity.json']['file_hashes']}
    for location in locations:
        packet=verify_packet(location)
        packets[str(location)]=packet
        failures=[row for row in packet['checks'] if not row['passed']]
        if location.name in ['legacy-update','sources','legacy-update-refined','sources-refined']:
            assert all(row['name'].startswith(('60digit independent photon/gas:','60digit unprojected spectral moment:','Float independent photon/gas:','Float unprojected spectral moment:')) for row in failures)
        elif location.name in ['reference','reference-stable','reference-refined','reference-certified']:
            assert all(row['name'].startswith(('Unchanged phase gate:','Stable phase gate:','Certified phase gate:')) for row in failures)
        elif location.name=='comparison':
            assert all(row['name'].startswith('CONVERGENCE:') for row in failures)
        else:
            assert not failures,(location,failures)
        for filename,sha in packet['input_hashes'].items():
            if filename not in rehashed:
                path=Path(filename)
                assert digest(path)==sha,path
                rehashed[filename]=sha
                if not path.is_relative_to(ROOT):
                    prior_paths.add(path)
        checks.append(dict(name='Completed packet and consumed hashes:'+str(location.relative_to(ROOT)),passed=True))
    prior_hashes=authenticate(prior_paths,chain)
    source=read_npz(ROOT/'results/sources/source.npz')
    refined_source=read_npz(ROOT/'results/sources-refined/source.npz') if (ROOT/'results/sources-refined/source.npz').exists() else None
    prior=read_npz(PARENT/'results/sources/source.npz')
    assert all(np.array_equal(source[key],prior[key]) for key in prior if not key.startswith('soft_'))
    checks.append(dict(name='Non-soft source,improved bands and temperature arrays unchanged',passed=True))
    proof=packets[str(ROOT/'results/preflight')]
    replayed=0
    refined_events=0
    with localcontext() as context:
        context.prec=80
        for endpoint_index,endpoint in enumerate(ENDPOINTS):
            bundle=EpochBundle(ENDPOINTS[endpoint])
            theta=proof['contexts'][endpoint][0]['theta']
            norm0,norm1=[Decimal.from_float(float(value)) for value in bundle.basis.norms[:2]]
            mean=Decimal.from_float(float(bundle.basis.mean))
            exacts={}
            refined_exacts={}
            for order in [4,5,6]:
                primitive=np.empty((7,3,3,4),dtype=object)
                primitive.fill(Decimal(0))
                refined_primitive=np.empty_like(primitive)
                refined_primitive.fill(Decimal(0))
                for node in integration_nodes(theta,order):
                    values=read_npz(moment_path(endpoint,order,node['index']))
                    old=read_npz(parent164.moment_path(endpoint,order,node['index']))
                    parameters,weight=parameters_and_weight(theta,node)
                    assert json.loads(str(values['identity']))==node and float(values['weight'])==weight
                    raw=read_npz(str(values['raw_path']))
                    loop=json.loads(Path(str(values['loop_path'])).read_text())
                    assert float(values['loop_scalar'])==float(raw['loop_scalar'])==loop['scalar']
                    assert loop['identity']==event_owner.inherited.virtual_identity(parameters)
                    assert float(values['virtual_coefficient'])==.5*(float(values['vacuum_coefficient'])+float(values['loop_scalar']))
                    assert float(values['state_pair_exact'])<1e-10 and float(values['virtual_pair_exact'])<1e-10
                    equivalence=json.loads(str(values['equivalence']))
                    refined_path=ROOT/'runs/refined'/endpoint/f'order{order}'/'nodes'/f'{node["index"]//500:03d}'/f'{node["index"]:05d}.npz'
                    candidate=read_npz(refined_path) if refined_path.exists() else values
                    if refined_source is not None:
                        required=bool(np.any(values['difference'][0]+values['difference'][-1]!=0))
                        assert required==refined_path.exists()
                        if required:
                            assert str(candidate['base_sha256'])==digest(moment_path(endpoint,order,node['index']))
                            assert np.array_equal(candidate['virtual'],values['virtual']) and np.array_equal(candidate['state'],values['state'])
                            assert np.max(abs(candidate['difference']-values['difference']))/np.max(abs(values['difference']))<1e-10
                            assert float(candidate['precise_shift_pair'])<1e-10 and float(candidate['direction_repair'])<1e-14
                            refined_events+=1
                    panel=int(np.searchsorted(BOUNDARIES,node['frequency'])-1)
                    for component_index,component in enumerate(COMPONENTS):
                        ratio=float(np.max(abs(values[component]-old[component]))/max(np.max(abs(old[component])),1e-300))
                        assert ratio==equivalence[component] and ratio<1e-10
                        for moment_index in range(3):
                            for column in range(4):
                                primitive[panel,component_index,moment_index,column]+=Decimal.from_float(-weight)*Decimal.from_float(float(values[component][moment_index,column]))
                                refined_primitive[panel,component_index,moment_index,column]+=Decimal.from_float(-weight)*Decimal.from_float(float(candidate[component][moment_index,column]))
                    replayed+=1
                lower=np.stack([primitive[:,:,0],primitive[:,:,1]/norm0,(primitive[:,:,0]-mean*primitive[:,:,1])/norm1,primitive[:,:,2]],axis=2)
                exacts[order]=lower
                packet=json.loads((ROOT/'results/sources'/f'{endpoint}-order{order}-moments.json').read_text())
                expected=np.array([Decimal(value) for value in packet['values']],dtype=object).reshape(packet['shape'])
                assert np.array_equal(lower,expected)
                saved=source[f'soft_endpoint_panels{order}'][:,endpoint_index]
                assert np.array_equal(saved[:,:,[0,1,2,97]],np.asarray(lower,dtype=float))
                old_panel=read_npz(SOURCE162/'results/sources'/f'{endpoint}-order{order}-panels.npz')['panels']
                assert np.array_equal(saved[:,:,3:97],old_panel[:,:,3:97])
                checks.append(dict(name=f'Independent primitive replay,loop provenance and unchanged higher rows:{endpoint}:{order}',passed=True))
                if refined_source is not None:
                    refined_lower=np.stack([refined_primitive[:,:,0],refined_primitive[:,:,1]/norm0,
                        (refined_primitive[:,:,0]-mean*refined_primitive[:,:,1])/norm1,refined_primitive[:,:,2]],axis=2)
                    refined_exacts[order]=refined_lower
                    refined_packet=json.loads((ROOT/'results/sources-refined'/f'{endpoint}-order{order}-moments.json').read_text())
                    refined_expected=np.array([Decimal(value) for value in refined_packet['values']],dtype=object).reshape(refined_packet['shape'])
                    assert np.array_equal(refined_lower,refined_expected)
                    refined_panel=refined_source[f'soft_endpoint_panels{order}'][:,endpoint_index]
                    assert np.array_equal(refined_panel[:,:,[0,1,2,97]],np.asarray(refined_lower,dtype=float))
                    assert np.array_equal(refined_panel[:,:,3:97],old_panel[:,:,3:97])
                    checks.append(dict(name=f'Independent adaptive primitive replay and unchanged higher rows:{endpoint}:{order}',passed=True))
            for step,high,low in [('54',5,4),('65',6,5),('64',6,4)]:
                delta=(exacts[high]-exacts[low]).sum(axis=(0,1))
                assert np.array_equal(np.asarray(delta,dtype=float),source[f'soft_{endpoint}_total{step}'][[0,1,2,97]])
                checks.append(dict(name='Independent80digit physical increment:'+endpoint+':'+step,passed=True))
                if refined_source is not None:
                    refined_delta=(refined_exacts[high]-refined_exacts[low]).sum(axis=(0,1))
                    assert np.array_equal(np.asarray(refined_delta,dtype=float),refined_source[f'soft_{endpoint}_total{step}'][[0,1,2,97]])
                    checks.append(dict(name='Independent refined80digit physical increment:'+endpoint+':'+step,passed=True))
    assert replayed==7560
    if refined_source is not None:
        assert refined_events==474
        assert all(np.array_equal(refined_source[key],source[key]) for key in source if not key.startswith('soft_'))
        checks.append(dict(name='All474 nonzero pair events refined;no bands or temperature arrays changed',passed=True))
    reference=packets[str(ROOT/'results/reference')]
    with localcontext() as context:
        context.prec=80
        for endpoint in ENDPOINTS:
            packet=json.loads((ROOT/'results/sources'/f'{endpoint}-source4-exact.json').read_text())
            values={key:np.array([Decimal(value) for value in packet[key]],dtype=object).reshape(4,4) for key in ['saved','full','update']}
            assert np.max(abs(values['full']-values['saved']-values['update']))<Decimal('1e-55')
            for kind in ['pair','moment']:
                terms={key:np.array([Decimal(value) for value in terms[kind]],dtype=object) for key,terms in reference['records'][endpoint]['defects'].items()}
                assert max(abs(value) for value in terms['legacy64']-terms['arithmetic']-terms['physical64'])<Decimal('1e-55')
                assert max(abs(value) for value in terms['repaired4']-terms['old']-terms['arithmetic'])<Decimal('1e-55')
                checks.append(dict(name='Unprojected reference defect accounting:'+endpoint+':'+kind,passed=True))
    if refined_source is not None:
        refined_reference=packets[str(ROOT/'results/reference-refined')]
        with localcontext() as context:
            context.prec=80
            for endpoint in ENDPOINTS:
                packet=json.loads((ROOT/'results/sources-refined'/f'{endpoint}-source4-exact.json').read_text())
                values={key:np.array([Decimal(value) for value in packet[key]],dtype=object).reshape(4,4) for key in ['saved','full','update']}
                assert np.max(abs(values['full']-values['saved']-values['update']))<Decimal('1e-55')
                for kind in ['pair','moment']:
                    terms={key:np.array([Decimal(value) for value in terms[kind]],dtype=object) for key,terms in refined_reference['records'][endpoint]['defects'].items()}
                    assert max(abs(value) for value in terms['legacy64']-terms['arithmetic']-terms['physical64'])<Decimal('1e-55')
                    assert max(abs(value) for value in terms['repaired4']-terms['old']-terms['arithmetic'])<Decimal('1e-55')
                    checks.append(dict(name='Independent refined reference defect ledger:'+endpoint+':'+kind,passed=True))
    for route in ['local','cubic']:
        for model in ['heavy','cold']:
            for count in COUNTS:
                for match in [20,40]:
                    label=f'{model}-{route}-{count}-m{match}'
                    actual=read_npz(READOUT_OWNER/'results/comparison'/(label+'.npz'))
                    pair=read_npz(ROOT/'results/baseline-check'/(label+'.npz'))
                    for quantity in ['potential','amplitudes']:
                        assert np.array_equal(pair['baseline_'+quantity],actual[quantity][:,:1])
                        assert np.array_equal(pair['saved_mts_'+quantity],actual[quantity][:,3:5])
                    assert np.any(pair['baseline_potential'])
                    checks.append(dict(name='Actual baseline and MTS independently retained:'+label,passed=True))
    summary=json.loads((ROOT/'NUMERICAL-SUMMARY.json').read_text())
    assert not summary['reference_history_adopted']
    qualified=packets[str(ROOT/'results/reference-refined')] if refined_source is not None else reference
    if str(ROOT/'results/reference-stable') in packets:
        qualified=packets[str(ROOT/'results/reference-stable')]
    if str(ROOT/'results/reference-certified') in packets:
        qualified=packets[str(ROOT/'results/reference-certified')]
    assert summary['reference_replay_qualified']==qualified['reference_replay_qualified']
    if not summary['reference_replay_qualified']:
        assert not (ROOT/'results/response').exists() and summary['new_response_evolutions']==0
    checks.append(dict(name='Unchanged source qualification precedes any response replay',passed=True))
    if str(ROOT/'results/basis-representation-diagnosis') in packets:
        basis=packets[str(ROOT/'results/basis-representation-diagnosis')]
        assert basis['all_checks_passed'] and basis['phases_per_route']==4097
        assert not any(basis[key] for key in ['source_arrays_changed','basis_arrays_changed','probe_adopted','temperature_curve_changed','tolerance_changed','response_propagation_allowed'])
        assert len(basis['records'])==12
        with localcontext() as context:
            context.prec=80
            constants={key:Decimal(value) for key,value in basis['constants'].items()}
            assert constants['exact_product_temperature0']==constants['mean']*constants['norm0']
            assert constants['temperature0_low_part']==constants['exact_product_temperature0']-constants['stored_temperature0']
            assert constants['coefficient_energy']==0
            assert constants['coefficient_number']==constants['stored_temperature0']/constants['norm0']-constants['mean']
            for label,record in basis['records'].items():
                assert record['maxima']['twofold_probe']<1e-10
                for worst in record['worst'].values():
                    expected=constants['coefficient_number']*Decimal(worst['number'])
                    assert abs(expected-Decimal(worst['basis_defect']))/max(abs(Decimal(worst['photon'])),Decimal('1e-300'))<Decimal('1e-50')
        checks.append(dict(name='Analytic basis-factorization diagnosis and twofold probe retained without waiving production gates',passed=True))
    scripts=list(ROOT.glob('*.py'))
    for path in scripts:
        compile(path.read_text(encoding='utf-8'),str(path),'exec')
    assert not list(ROOT.rglob('__pycache__'))
    largest=max(sum(path.is_file() for path in directory.iterdir()) for directory in [ROOT,*[path for path in ROOT.rglob('*') if path.is_dir()]])
    assert largest<=500
    modified=[str(path) for path in (POST.parent/'formalization-workbench').rglob('*') if path.is_file() and path.stat().st_mtime>STARTED.timestamp()]
    assert not modified,modified[:10]
    checks.append(dict(name='Compile,no bytecode,folder cap and protected-workbench mtime check',passed=True))
    scientific=[row for packet in packets.values() for row in packet['checks']]
    finish(folder,dict(checks=checks,scientific_checks=len(scientific),passing_scientific_checks=sum(row['passed'] for row in scientific),
        retained_failure_names=[row['name'] for row in scientific if not row['passed']],compiled_scripts=len(scripts),largest_direct_file_count=largest,
        rehashed_prior_files=len(prior_hashes),consumed_and_immediate_rehashed=prior_hashes,weighted_events_replayed=replayed,adaptive_events_replayed=refined_events,
        accepted_scope_verified=all(row['passed'] for row in checks),protected_workbench_recent_modified_file_count=0,
        protected_check_scope='Modification-time scan since13:18:55UTC19Oct2026,not a content snapshot.'),__file__,[*rehashed,*prior_hashes,ROOT/'NUMERICAL-SUMMARY.json'])
    print(json.dumps(dict(checks=len(checks),passed=all(row['passed'] for row in checks),scientific_checks=len(scientific),
        failed=sum(not row['passed'] for row in scientific),events=replayed,prior_files=len(prior_hashes))),flush=True)


if __name__=='__main__':
    main()
