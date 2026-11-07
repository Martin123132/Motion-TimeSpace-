from stage162_common import *
import ast


def main():
    modest()
    folder=ROOT/'results/validation'
    folder.mkdir(parents=True,exist_ok=False)
    chain=ancestors()
    prior_hashes=authenticate([PARENT/name for name in chain[PARENT/'results/stage-integrity.json']['file_hashes']],chain)
    locations=[ROOT/'results/preflight',ROOT/'results/sources',ROOT/'results/comparison']
    locations.extend(ROOT/'runs'/endpoint/f'order{order}' for endpoint in ENDPOINTS for order in [5,6])
    locations.extend(ROOT/'results/response'/f'{model}-{route}-{count}'
        for model in ['heavy','cold'] for route in ['local','cubic'] for count in COUNTS)
    checks,packets,rehashed=[],{},{}
    for location in locations:
        packet=verify_packet(location)
        packets[str(location)]=packet
        assert all(row['name'].startswith('CONVERGENCE:') for row in packet['checks'] if not row['passed'])
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
    for route in ['local','cubic']:
        for model in ['heavy','cold']:
            for count in COUNTS:
                location=ROOT/'results/response'/f'{model}-{route}-{count}'
                response=read_npz(location/'response.npz')
                for quantity in ['photon','energy','gas','work','number','integrated_number_source']:
                    values=response[quantity]
                    assert np.array_equal(values[...,6:10],np.zeros_like(values[...,6:10]))
                    close(checks,'Independent response telescope:'+model+':'+route+':'+str(count)+':'+quantity,
                        values[...,16:18]+values[...,22:24],values[...,2:4],1e-8)
                for match in [20,40]:
                    key=f'{model}-{route}-{count}-m{match}'
                    saved=read_npz(PARENT/'results/comparison'/(key+'.npz'))
                    comparisons={step:read_npz(ROOT/'results/comparison'/(key+'-step'+step+'.npz')) for step in ['54','65','64']}
                    for step,comparison in comparisons.items():
                        assert np.array_equal(comparison['potential'][:,:1],saved['potential'][:,:1])
                        assert np.array_equal(comparison['amplitudes'][:,:1],saved['amplitudes'][:,:1])
                        if step!='65':
                            assert np.array_equal(comparison['potential'][:,1:3],saved['potential'][:,3:5])
                    for quantity in ['potential','residual','amplitudes']:
                        close(checks,'Independent paired-readout telescope:'+key+':'+quantity,
                            comparisons['54'][quantity][...,9:11]+comparisons['65'][quantity][...,9:11],
                            comparisons['64'][quantity][...,9:11],1e-8)
                    checks.append(dict(name='Actual saved baseline/MTS preserved:'+key,passed=True))
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
