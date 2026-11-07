from stage162_common import *
import ast


def main():
    modest()
    folder=ROOT/'results/validation'
    folder.mkdir(parents=True,exist_ok=False)
    chain=ancestors()
    prior_hashes=authenticate([PARENT/name for name in chain[PARENT/'results/stage-integrity.json']['file_hashes']],chain)
    locations=[ROOT/'results/preflight',ROOT/'results/sources',ROOT/'results/moment-repair',ROOT/'results/conditioning',ROOT/'results/baseline-check',ROOT/'results/stable-jump-probe']
    locations.extend(ROOT/'runs'/endpoint/f'order{order}' for endpoint in ENDPOINTS for order in [5,6])
    checks,packets,rehashed=[],{},{}
    for location in locations:
        packet=verify_packet(location)
        packets[str(location)]=packet
        failures=[row for row in packet['checks'] if not row['passed']]
        if location==ROOT/'results/sources':
            assert failures and all(row['name'].startswith(('Endpoint unprojected moment:','Endpoint photon/gas exchange:')) for row in failures)
        elif location==ROOT/'results/moment-repair':
            assert failures and all(row['name'].startswith(('60digit atomic moment:','60digit atomic photon/gas:')) for row in failures)
        else:
            assert not failures
        for filename,sha in packet['input_hashes'].items():
            path=Path(filename)
            if filename not in rehashed:
                assert digest(path)==sha,path
                rehashed[filename]=sha
                if not path.is_relative_to(ROOT):
                    prior_hashes.update(authenticate([path],chain))
        checks.append(dict(name='Completed packet and all consumed hashes:'+str(location.relative_to(ROOT)),passed=True))
    proof=packets[str(ROOT/'results/preflight')]
    source=read_npz(ROOT/'results/sources/source.npz')
    frozen=read_npz(ROOT/'results/preflight/frozen-reference.npz')
    prior=read_npz(PARENT/'results/sources/source.npz')
    assert set(frozen)==set(prior)
    for key in frozen:
        assert np.array_equal(frozen[key],prior[key]),key
        assert np.array_equal(source[key],prior[key]),key
    checks.append(dict(name='Every inherited source/control/lower-band/prediction array bitwise unchanged',passed=True))
    inverse=np.linalg.inv(source['mass'])
    def norm(value):
        spectral=value[...,1:-1,:]
        return np.sqrt(np.maximum(np.einsum('...ij,ik,...kj->...j',spectral,inverse,spectral),0))
    scale=norm(source['actual'])
    replayed=0
    independent_moments={}
    for endpoint_index,endpoint in enumerate(ENDPOINTS):
        theta=proof['contexts'][endpoint][0]['theta']
        for order in [4,5,6]:
            path=ROOT/'results/sources'/f'{endpoint}-order{order}-panels.npz'
            stored=read_npz(path)
            frequencies=np.asarray(list(incoming_rule(order,1e-5,24.)))[:,0]
            assert np.array_equal(stored['frequencies'],frequencies)
            terms=[[[] for component in COMPONENTS] for panel in range(7)]
            with localcontext() as context:
                context.prec=60
                exact=np.empty((7,3,4,4),dtype=object)
                exact.fill(Decimal(0))
                for node in integration_nodes(theta,order):
                    saved,weight,event_path,loop_path=load_node162(endpoint,order,node,theta)
                    panel=int(np.searchsorted(BOUNDARIES,node['frequency'])-1)
                    assert 0<=panel<7
                    for component_index,component in enumerate(COMPONENTS):
                        values=saved[component]
                        terms[panel][component_index].append(-weight*values)
                        for position,moment in enumerate([0,1,2,97]):
                            for column in range(4):
                                exact[panel,component_index,position,column]+=Decimal.from_float(-weight)*Decimal.from_float(float(values[moment,column]))
                    replayed+=1
                for panel in range(7):
                    for component_index,component in enumerate(COMPONENTS):
                        assert len(terms[panel][component_index])==order*36
                        values=np.asarray(terms[panel][component_index]).reshape(order*36,-1)
                        independent=np.asarray([math.fsum(values[:,column]) for column in range(392)]).reshape(98,4)
                        independent[[0,1,2,97]]=np.asarray(exact[panel,component_index],dtype=float)
                        expected=source[f'endpoint_panels{order}'][panel,endpoint_index,component_index]
                        test(checks,f'Independent weighted endpoint panel:{endpoint}:{order}:{panel}:{component}',
                            float(max(norm(independent-expected)/scale)),1e-10)
                        test(checks,f'Independent frequency partition:{endpoint}:{order}:{panel}:{component}',
                            float(max(norm(stored['frequency_values'][panel*order:(panel+1)*order,component_index].sum(axis=0)-expected)/scale)),1e-10)
            independent_moments[(endpoint,order)]=exact.copy()
            assert np.array_equal(stored['panels'],source[f'endpoint_panels{order}'][:,endpoint_index])
    assert replayed==7560
    checks.append(dict(name='All7560 new/reference weighted events independently resummed',passed=True))
    vandermonde=np.vander(np.array([0.,.25,.5,1.]),4,increasing=True)
    weights=np.array([1.,.75,.75**2,.75**3])@np.linalg.inv(vandermonde)
    close(checks,'Independent cubic Lagrange weights',weights,np.array([.25,-1.,1.5,.25]),1e-12)
    current=source['after_band820_full']
    prediction=weights[0]*source['start']+weights[1]*current[1]+weights[2]*current[2]+weights[3]*source['end']
    test(checks,'Independent fixed cubic defect',float(max(norm(current[0]-prediction-source['endpoint_cubic_error4'])/scale)),1e-10)
    for step in ['54','65','64']:
        values=source['endpoint_delta'+step]
        expected=-.25*values.sum(axis=(0,1,2))
        test(checks,'Independent two-endpoint sign:'+step,
            float(max(norm(expected-source['endpoint_cubic_step'+step])/scale)),1e-10)
    moments=read_npz(ROOT/'results/moment-repair/moments.npz')
    with localcontext() as context:
        context.prec=60
        for endpoint in ENDPOINTS:
            for step,high,low in [('54',5,4),('65',6,5),('64',6,4)]:
                exact_delta=independent_moments[(endpoint,high)]-independent_moments[(endpoint,low)]
                assert np.array_equal(np.asarray(exact_delta,dtype=float),moments[endpoint+'_panel'+step])
                assert np.array_equal(np.asarray(exact_delta.sum(axis=(0,1)),dtype=float),moments[endpoint+'_total'+step])
                checks.append(dict(name='Independent60digit endpoint moment replay:'+endpoint+':'+step,passed=True))
    for route in ['local','cubic']:
        for model in ['heavy','cold']:
            for count in COUNTS:
                for match in [20,40]:
                    key=f'{model}-{route}-{count}-m{match}'
                    saved=read_npz(PARENT/'results/comparison'/(key+'.npz'))
                    baseline=read_npz(ROOT/'results/baseline-check'/(key+'.npz'))
                    assert np.array_equal(baseline['baseline_potential'],saved['potential'][:,:1])
                    assert np.array_equal(baseline['saved_mts_potential'],saved['potential'][:,3:5])
                    assert np.array_equal(baseline['baseline_amplitudes'],saved['amplitudes'][:,:1])
                    assert np.array_equal(baseline['saved_mts_amplitudes'],saved['amplitudes'][:,3:5])
                    assert np.any(baseline['baseline_potential'])
                    checks.append(dict(name='Actual nonzero saved baseline and MTS unchanged:'+key,passed=True))
    assert not (ROOT/'results/response').exists()
    probe=packets[str(ROOT/'results/stable-jump-probe')]
    assert probe['probe_events']==4 and probe['all_checks_passed']
    assert not probe['gas_equals_minus_photon_enforced'] and not probe['full_source_recomputed']
    for name,record in probe['records'].items():
        values=read_npz(ROOT/'results/stable-jump-probe'/(name+'.npz'))
        assert np.array_equal(values['old'],read_npz(Path(record['source_path']))['difference'])
        assert np.array_equal(values['new'][3:],values['old'][3:])
        pair=abs(values['new'][0]+values['new'][-1])/np.maximum(abs(values['new'][0]),1e-300)
        moment=abs(source['temperature']@values['new'][1:-1]-values['new'][0])/np.maximum(abs(values['new'][0]),1e-300)
        test(checks,'Independent stable-jump photon/electron probe:'+name,float(max(pair)),1e-10)
        test(checks,'Independent stable-jump spectral moment probe:'+name,float(max(moment)),1e-10)
    with localcontext() as context:
        context.prec=80
        for energy_string in ['0.00000001','0.0001','0.001','0.01']:
            energy=Decimal(energy_string)
            for ratio in ['-0.8','-0.01','0','0.01','0.3']:
                signed_soft=Decimal(ratio)*energy
                for angular,mixed,incident_soft in [(Decimal('.2'),Decimal('.7'),Decimal('1.3')),(Decimal('1.7'),Decimal('1.2'),Decimal('.8'))]:
                    denominator=1+energy*angular-signed_soft*mixed
                    hard=(energy-signed_soft-energy*signed_soft*incident_soft)/denominator
                    direct=hard+signed_soft-energy
                    stable=(-energy*signed_soft*incident_soft-(energy-signed_soft)*(energy*angular-signed_soft*mixed))/denominator
                    assert abs(stable-direct)<Decimal('1e-70')
    checks.append(dict(name='Independent80digit signed real/Born rational energy identity',passed=True))
    summary=json.loads((ROOT/'NUMERICAL-SUMMARY.json').read_text())
    assert not summary['response_propagation_allowed'] and not summary['moment_readiness_passed']
    checks.append(dict(name='Failed moment gate blocks propagation without projection or tolerance relaxation',passed=True))
    source_tree=ast.parse((ROOT/'stage162_common.py').read_text())
    old_tree=ast.parse((PARENT/'stage161_common.py').read_text())
    for name in ['owned_loop','expensive_components']:
        current=next(node for node in source_tree.body if isinstance(node,ast.FunctionDef) and node.name==name)
        old=next(node for node in old_tree.body if isinstance(node,ast.FunctionDef) and node.name==name)
        assert ast.dump(current)==ast.dump(old)
    checks.append(dict(name='AST-identical physics and no automatic temperature refit',passed=True))
    scripts=list(ROOT.glob('*.py'))
    for path in scripts:
        compile(path.read_text(encoding='utf-8'),str(path),'exec')
    assert not list(ROOT.rglob('__pycache__'))
    largest=max(sum(path.is_file() for path in folder.iterdir()) for folder in [ROOT,*[path for path in ROOT.rglob('*') if path.is_dir()]])
    assert largest<=500
    workbench=POST.parent/'formalization-workbench'
    modified=[str(path) for path in workbench.rglob('*') if path.is_file() and path.stat().st_mtime>STARTED.timestamp()]
    assert not modified,modified[:10]
    checks.append(dict(name='Compile/no-bytecode/folder-size and protected-workbench mtime checks',passed=True))
    scientific=[row for packet in packets.values() for row in packet['checks']]
    failed=[row['name'] for row in scientific if not row['passed']]
    finish(folder,dict(checks=checks,scientific_checks=len(scientific),
        passing_scientific_checks=sum(row['passed'] for row in scientific),retained_failure_names=failed,
        compiled_scripts=len(scripts),largest_direct_file_count=largest,
        rehashed_prior_files=len(prior_hashes),consumed_and_immediate_rehashed=prior_hashes,
        weighted_events_replayed=replayed,accepted_scope_verified=all(row['passed'] for row in checks),
        protected_workbench_recent_modified_file_count=0,
        protected_check_scope='Modification-time scan since22:14:52UTC18Oct2026,not a content baseline.'),__file__,
        [*rehashed,*prior_hashes,ROOT/'NUMERICAL-SUMMARY.json'])
    print(json.dumps(dict(validation_checks=len(checks),passed=all(row['passed'] for row in checks),
        scientific_checks=len(scientific),retained_failures=failed,prior_files=len(prior_hashes),compiled_scripts=len(scripts),
        weighted_events_replayed=replayed,largest_folder=largest)),flush=True)
    assert all(row['passed'] for row in checks)


if __name__=='__main__':
    main()
