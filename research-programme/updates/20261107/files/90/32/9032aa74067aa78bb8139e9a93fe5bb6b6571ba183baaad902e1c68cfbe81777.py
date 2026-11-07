from stage163_common import *


def main():
    modest()
    folder=ROOT/'results/validation'
    folder.mkdir(parents=True,exist_ok=False)
    chain=ancestors()
    locations=[ROOT/'results/preflight',ROOT/'results/sources',ROOT/'results/baseline-check',ROOT/'results/precision-diagnosis',
        ROOT/'results/compensated-probe',ROOT/'results/correlated-soft-probe']
    locations.extend(ROOT/'runs'/endpoint/f'order{order}' for endpoint in ENDPOINTS for order in [4,5,6])
    locations.extend(path.parent for path in (ROOT/'results/response').glob('*/status.json'))
    if (ROOT/'results/comparison/status.json').exists():
        locations.append(ROOT/'results/comparison')
    checks,packets,rehashed=[],{},{}
    prior_paths={PARENT/name for name in chain[PARENT/'results/stage-integrity.json']['file_hashes']}
    for location in locations:
        packet=verify_packet(location)
        packets[str(location)]=packet
        failures=[row for row in packet['checks'] if not row['passed']]
        if location==ROOT/'results/sources':
            assert all(row['name'].startswith(('60digit independent photon/gas:',
                '60digit unprojected spectral moment:','Float independent photon/gas:',
                'Float unprojected spectral moment:')) for row in failures)
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
    proof=packets[str(ROOT/'results/preflight')]
    source=read_npz(ROOT/'results/sources/source.npz')
    prior=read_npz(PARENT/'results/sources/source.npz')
    for key in prior:
        assert np.array_equal(source[key],prior[key]),key
    checks.append(dict(name='All inherited source/control/improved-band arrays bitwise retained',passed=True))
    replayed=0
    independent={}
    with localcontext() as context:
        context.prec=60
        for endpoint_index,endpoint in enumerate(ENDPOINTS):
            bundle=EpochBundle(ENDPOINTS[endpoint])
            theta=proof['contexts'][endpoint][0]['theta']
            norm0=Decimal.from_float(float(bundle.basis.norms[0]))
            norm1=Decimal.from_float(float(bundle.basis.norms[1]))
            mean=Decimal.from_float(float(bundle.basis.mean))
            for order in [4,5,6]:
                exact=np.empty((7,3,3,4),dtype=object)
                exact.fill(Decimal(0))
                for node in integration_nodes(theta,order):
                    path=moment_path(endpoint,order,node['index'])
                    event=read_npz(path)
                    params,weight=parameters_and_weight(theta,node)
                    assert json.loads(str(event['identity']))==node and float(event['weight'])==weight
                    panel=int(np.searchsorted(BOUNDARIES,node['frequency'])-1)
                    for component_index,component in enumerate(COMPONENTS):
                        assert event[component].shape==(3,4) and np.isfinite(event[component]).all()
                        for moment_index in range(3):
                            for column in range(4):
                                exact[panel,component_index,moment_index,column]+=Decimal.from_float(-weight)*Decimal.from_float(float(event[component][moment_index,column]))
                    replayed+=1
                lower=np.empty((7,3,4,4),dtype=object)
                lower[:,:,0,:]=exact[:,:,0,:]
                lower[:,:,1,:]=exact[:,:,1,:]/norm0
                lower[:,:,2,:]=(exact[:,:,0,:]-mean*exact[:,:,1,:])/norm1
                lower[:,:,3,:]=exact[:,:,2,:]
                independent[(endpoint,order)]=lower
                saved_json=json.loads((ROOT/'results/sources'/f'{endpoint}-order{order}-moments.json').read_text())
                saved=np.array([Decimal(value) for value in saved_json['values']],dtype=object).reshape(saved_json['shape'])
                assert np.array_equal(saved,lower)
                expected=source[f'repaired_endpoint_panels{order}'][:,endpoint_index]
                assert np.array_equal(expected[:,:,[0,1,2,97]],np.asarray(lower,dtype=float))
                old_panel=read_npz(PARENT/'results/sources'/f'{endpoint}-order{order}-panels.npz')['panels']
                assert np.array_equal(expected[:,:,3:97],old_panel[:,:,3:97])
                checks.append(dict(name=f'Independent primitive sum and unchanged higher rows:{endpoint}:{order}',passed=True))
            for step,high,low in [('54',5,4),('65',6,5),('64',6,4)]:
                delta=independent[(endpoint,high)]-independent[(endpoint,low)]
                expected=source[f'repaired_{endpoint}_total{step}']
                assert np.array_equal(expected[[0,1,2,97]],np.asarray(delta.sum(axis=(0,1)),dtype=float))
                checks.append(dict(name=f'Independent60digit order-difference replay:{endpoint}:{step}',passed=True))
    assert replayed==7560
    checks.append(dict(name='All7560 endpoint moment events independently replayed',passed=True))
    for route in ['local','cubic']:
        for endpoint in ENDPOINTS:
            for phase in [0.,.25,.5,.75,1.]:
                expected=float(phase==(0 if endpoint=='start' else 1))
                assert abs(endpoint_response_basis(phase,route,endpoint)-expected)<1e-14
        checks.append(dict(name='Unchanged endpoint response cardinal weights:'+route,passed=True))
    for model in ['heavy','cold']:
        for route in ['local','cubic']:
            for count in COUNTS:
                for match in [20,40]:
                    key=f'{model}-{route}-{count}-m{match}'
                    saved=read_npz(READOUT_OWNER/'results/comparison'/(key+'.npz'))
                    pair=read_npz(ROOT/'results/baseline-check'/(key+'.npz'))
                    assert np.array_equal(pair['baseline_potential'],saved['potential'][:,:1])
                    assert np.array_equal(pair['saved_mts_potential'],saved['potential'][:,3:5])
                    assert np.array_equal(pair['baseline_amplitudes'],saved['amplitudes'][:,:1])
                    assert np.array_equal(pair['saved_mts_amplitudes'],saved['amplitudes'][:,3:5])
                    assert np.any(pair['baseline_potential'])
                    checks.append(dict(name='Actual nonzero paired baseline and MTS retained:'+key,passed=True))
    summary=json.loads((ROOT/'NUMERICAL-SUMMARY.json').read_text())
    source_packet=packets[str(ROOT/'results/sources')]
    assert summary['response_propagation_allowed']==source_packet['all_checks_passed']
    if not source_packet['all_checks_passed']:
        assert not (ROOT/'results/response').exists()
        assert summary['new_response_evolutions']==0
    checks.append(dict(name='Unchanged raw1e-10 source gate controls propagation',passed=True))
    for tag,record in packets[str(ROOT/'results/correlated-soft-probe')]['records'].items():
        values=read_npz(ROOT/'results/correlated-soft-probe'/(tag+'.npz'))
        expected=read_npz(ROOT/'results/compensated-probe'/(tag+'.npz'))
        assert np.array_equal(values['old'],expected['old'])
        pair=abs(values['new'][0]+values['new'][-1])/np.maximum(abs(values['old'][0]),1e-300)
        assert np.array_equal(pair,np.asarray(record['new_pair']))
        energy_change=np.max(abs(values['new'][[0,2]]-values['old'][[0,2]]),axis=0)/np.maximum(abs(values['old'][0]),1e-300)
        test(checks,'Independent correlated-probe energy change:'+tag,float(max(energy_change)),1e-10)
        test(checks,'Independent correlated-probe pair:'+tag,float(max(pair)),1e-10)
    assert not packets[str(ROOT/'results/correlated-soft-probe')]['full_correlated_source_computed']
    checks.append(dict(name='Eight correlated-soft probes are not promoted to a full-source result',passed=True))
    with localcontext() as context:
        context.prec=80
        for energy_string in ['0.00000001','0.0001','0.001','0.01']:
            energy=Decimal(energy_string)
            for ratio in ['-0.8','-0.01','0','0.01','0.3']:
                soft=Decimal(ratio)*energy
                for angular,mixed,incident_soft in [(Decimal('.2'),Decimal('.7'),Decimal('1.3')),(Decimal('1.7'),Decimal('1.2'),Decimal('.8'))]:
                    denominator=1+energy*angular-soft*mixed
                    hard=(energy-soft-energy*soft*incident_soft)/denominator
                    direct=hard+soft-energy
                    stable=(-energy*soft*incident_soft-(energy-soft)*(energy*angular-soft*mixed))/denominator
                    assert abs(stable-direct)<Decimal('1e-70')
                    initial=1+energy*angular
                    hard0=energy/initial
                    hard_shift=-soft*((1+energy*incident_soft)*initial-energy*mixed)/(initial*denominator)
                    energy_shift=soft*(energy*(initial*(angular-incident_soft)+mixed)-soft*mixed*initial)/(initial*denominator)
                    assert abs(hard_shift-(hard-hard0))<Decimal('1e-70')
                    assert abs(energy_shift-(hard-hard0+soft))<Decimal('1e-70')
            for displacement in ['0.000000000001','0.00001','-0.00001']:
                old_recoil=[energy,2*energy,-3*energy]
                change=[Decimal(displacement),-2*Decimal(displacement),3*Decimal(displacement)]
                old_squared=sum(value*value for value in old_recoil)
                new_squared=sum((old+delta)**2 for old,delta in zip(old_recoil,change))
                direct=(1+new_squared).sqrt()-(1+old_squared).sqrt()
                stable=(2*sum(old*delta for old,delta in zip(old_recoil,change))+sum(delta*delta for delta in change))/(
                    (1+new_squared).sqrt()+(1+old_squared).sqrt())
                assert abs(stable-direct)<Decimal('1e-70')
    checks.append(dict(name='Independent80digit stable signed real/Born algebra',passed=True))
    checks.append(dict(name='Independent80digit correlated soft and recoil-shift identities',passed=True))
    scripts=list(ROOT.glob('*.py'))
    for path in scripts:
        compile(path.read_text(encoding='utf-8'),str(path),'exec')
    assert not list(ROOT.rglob('__pycache__'))
    largest=max(sum(path.is_file() for path in folder.iterdir()) for folder in [ROOT,*[path for path in ROOT.rglob('*') if path.is_dir()]])
    assert largest<=500
    workbench=POST.parent/'formalization-workbench'
    modified=[str(path) for path in workbench.rglob('*') if path.is_file() and path.stat().st_mtime>STARTED.timestamp()]
    assert not modified,modified[:10]
    checks.append(dict(name='Compile/no-bytecode/folder-size/protected-workbench mtime checks',passed=True))
    scientific=[row for packet in packets.values() for row in packet['checks']]
    failed=[row['name'] for row in scientific if not row['passed']]
    finish(folder,dict(checks=checks,scientific_checks=len(scientific),
        passing_scientific_checks=sum(row['passed'] for row in scientific),retained_failure_names=failed,
        compiled_scripts=len(scripts),largest_direct_file_count=largest,
        rehashed_prior_files=len(prior_hashes),consumed_and_immediate_rehashed=prior_hashes,
        weighted_events_replayed=replayed,accepted_scope_verified=all(row['passed'] for row in checks),
        protected_workbench_recent_modified_file_count=0,
        protected_check_scope='Modification-time scan since01:47:02UTC19Oct2026,not a content baseline.'),__file__,
        [*rehashed,*prior_hashes,ROOT/'NUMERICAL-SUMMARY.json'])
    print(json.dumps(dict(validation_checks=len(checks),passed=all(row['passed'] for row in checks),
        scientific_checks=len(scientific),retained_failures=len(failed),prior_files=len(prior_hashes),
        compiled_scripts=len(scripts),weighted_events_replayed=replayed,largest_folder=largest)),flush=True)
    assert all(row['passed'] for row in checks)


if __name__=='__main__':
    main()
