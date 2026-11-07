from stage161_common import *
from decimal import Decimal,localcontext


def main():
    modest()
    folder=ROOT/'results/validation'
    folder.mkdir(parents=True,exist_ok=False)
    chain=ancestors()
    prior_hashes=authenticate([PARENT/filename for filename in chain[PARENT/'results/stage-integrity.json']['file_hashes']],chain)
    locations=[ROOT/'results/preflight',ROOT/'results/sources',ROOT/'results/comparison']
    locations.extend(ROOT/'runs/band5'/f'part{part}' for part in [0,1])
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
        checks.append(dict(name='Complete packet and consumed hashes:'+str(location.relative_to(ROOT)),passed=True))
    source=read_npz(ROOT/'results/sources/source.npz')
    frozen=read_npz(ROOT/'results/preflight/frozen-reference.npz')
    prior_source=read_npz(SOURCE159/'results/sources/source.npz')
    allowance=read_npz(ROOT/'results/preflight/frozen-allowance.npz')
    prior_allowance=read_npz(PARENT/'results/analysis/source-allowance.npz')
    assert set(frozen)==set(prior_source)
    assert set(allowance)==set(prior_allowance)
    for key in frozen:
        assert np.array_equal(frozen[key],prior_source[key])
        assert np.array_equal(source[key],prior_source[key])
    for key in allowance:
        assert np.array_equal(allowance[key],prior_allowance[key])
    checks.append(dict(name='Every inherited lower-band/source/control/prediction array bitwise preserved',passed=True))
    manifest=json.loads((ROOT/'results/preflight/events.json').read_text())
    inverse=np.linalg.inv(source['mass'])
    def norm(value):
        spectral=value[...,1:-1,:]
        return np.sqrt(np.maximum(np.einsum('...ij,ik,...kj->...j',spectral,inverse,spectral),0))
    scale=norm(source['actual'])
    summed=shared=0
    for order,which in [(6,'old'),(7,'new')]:
        frequency=read_npz(ROOT/'results/sources'/f'order{order}-frequency.npz')
        for site_index,site in enumerate(SITES):
            rows=[row for row in manifest[which] if row['site']==site]
            assert len(rows)==36*order
            wanted=np.asarray([(value,weight) for value,weight in incoming_rule(order,1e-5,24.) if 8.<value<20.])
            assert np.array_equal(frequency['frequencies'],wanted[:,0])
            assert np.array_equal(frequency['seed_weights'],wanted[:,1])
            terms={component:[] for component in COMPONENTS}
            for row in rows:
                saved,weight,path,loop_path=load_event(row)
                parameters,independent_weight=parameters_and_weight(row['theta'],row['node'])
                assert weight==independent_weight
                if which=='new' and row['reused_path']:
                    assert weight!=float(saved['weight'])
                    shared+=1
                for component in COMPONENTS:
                    terms[component].append(-weight*saved[component])
                summed+=1
            for component_index,component in enumerate(COMPONENTS):
                values=np.asarray(terms[component]).reshape(len(rows),-1)
                expected=np.asarray([math.fsum(values[:,column]) for column in range(392)]).reshape(98,4)
                target=source['band820_order6_reference_panel' if order==6 else 'band820_order7_panel'][site_index,component_index]
                test(checks,'Independent weighted panel sum:'+str(order)+':'+site+':'+component,
                    float(max(norm(expected-target)/scale)),1e-10)
                test(checks,'Independent frequency partition:'+str(order)+':'+site+':'+component,
                    float(max(norm(np.sum(frequency['sites'][site_index,component_index],axis=0)-target)/scale)),1e-10)
            midpoint=len(wanted)//2
            selected=[row for row in rows if row['node']['frequency']==wanted[midpoint,0]]
            assert len(selected)==36
            with localcontext() as context:
                context.prec=60
                exact=np.empty((3,4,4),dtype=object)
                exact.fill(Decimal(0))
                for row in selected:
                    saved,weight,path,loop_path=load_event(row)
                    for component_index,component in enumerate(COMPONENTS):
                        for position,moment in enumerate([0,1,2,97]):
                            for column in range(4):
                                exact[component_index,position,column]+=Decimal.from_float(-weight)*Decimal.from_float(float(saved[component][moment,column]))
                close(checks,'Independent60digit sampled moments:'+str(order)+':'+site,np.asarray(exact,dtype=float),
                    frequency['sites'][site_index,:,midpoint][:,[0,1,2,97]],1e-10)
        joint=np.einsum('s,scfij->cfij',COEFFICIENTS,frequency['sites'])
        close(checks,'Independent common-frequency combination:'+str(order),joint,frequency['joint'],1e-10)
    assert summed==1404 and shared==108
    checks.append(dict(name='1404 weighted events resummed;108 shared values require new weights',passed=True))
    close(checks,'Order6 reference against Stage160 reconstruction',source['band820_order6_reference_panel'],allowance['panels6'][5],1e-10)
    close(checks,'Independent order7-minus6 replacement',
        source['band820_order7_panel']-source['band820_order6_reference_panel'],source['band820_delta'],1e-10)
    for site_index,site in enumerate(SITES):
        increment=sum(source['band820_delta'][site_index])
        assert np.array_equal(source['band820_'+site+'_total'],increment)
        close(checks,'No duplicate lower-band update:'+site,prior_source['after_order8_full'][site_index]+increment,
            source['after_band820_full'][site_index],1e-12)
    packet=packets[str(ROOT/'results/sources')]
    current_joint=np.einsum('s,scij->cij',COEFFICIENTS,source['band820_delta'])
    previous_joint=np.einsum('s,scij->cij',COEFFICIENTS,allowance['delta65'][5])
    for index,component in enumerate(COMPONENTS):
        close(checks,'Independent same-panel contraction:'+component,norm(current_joint[index])/norm(previous_joint[index]),
            packet['panel_metrics']['component_step_ratio_vs_order6_minus5'][index],1e-10)
    expected_steps=allowance['latest_steps'].copy()
    expected_steps[5]=source['band820_delta']
    assert np.array_equal(expected_steps,source['band820_latest_steps'])
    earlier_summary=json.loads((PARENT/'NUMERICAL-SUMMARY.json').read_text())
    for route in ['local','cubic']:
        weights=parent160.weights_for(route)
        record=packet['uncertainty_update'][route]
        previous=earlier_summary['source']['routes'][route]['scenarios']
        close(checks,'Previous independent budget replay:'+route,record['previous_independent_budget'],
            previous['independent_last_step']['numerator_radius'],1e-10)
        close(checks,'Previous matched budget replay:'+route,record['previous_matched_panel_budget'],
            previous['matched_panel_last_step']['numerator_radius'],1e-10)
        magnitudes=norm(expected_steps)/scale
        independent=(abs(weights)[None,:,None,None]*magnitudes).sum(axis=(0,1,2))
        matched=norm(np.einsum('s,pscij->pij',weights,expected_steps)).sum(axis=0)/scale
        close(checks,'Independent updated last-step budget:'+route,independent,record['current_independent_budget'],1e-10)
        close(checks,'Independent matched last-step budget:'+route,matched,record['current_matched_panel_budget'],1e-10)
        full=source['after_band820_full']
        prediction=current_prediction(source,route)+sum(source155.predictor_basis(.75,route,site)*
            source['band820_'+site+'_total'] for site in ['warm','centre'])
        if route=='cubic':
            close(checks,'Updated cubic anchors independent formula',prediction,
                source['start']/4-full[1]+1.5*full[2]+source['end']/4,1e-12)
        error=norm(full[0]-prediction)/scale
        cold=norm(full[0])/scale
        cold_radius=magnitudes[:,0].sum(axis=(0,1))
        for name,radius in [('independent_conditional',independent),('matched_conditional',matched)]:
            scenario=record[name]
            assert not scenario['certified'] and scenario['endpoint_and_other_axis_radius'] is None
            close(checks,'Conditional reverse triangle:'+route+':'+name,
                np.maximum(error-radius,0)/(cold+cold_radius),scenario['lower_relative'],1e-10)
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    reader=ShapeReadout(ladder.basis,canonical=True)
    for model in ['heavy','cold']:
        for route in ['local','cubic']:
            for count in COUNTS:
                response=read_npz(ROOT/'results/response'/f'{model}-{route}-{count}/response.npz')
                for key in ['photon','gas','energy','work','number','integrated_number_source']:
                    value=response[key]
                    assert np.array_equal(value[0],np.zeros_like(value[0]))
                    assert np.array_equal(value[...,6:10],np.zeros_like(value[...,6:10]))
                    close(checks,'Independent three-site response:'+model+':'+route+':'+str(count)+':'+key,
                        sum(value[...,start:start+2] for start in [12,14,16]),value[...,2:4],1e-8)
                for match in [20,40]:
                    label=f'{model}-{route}-{count}-m{match}'
                    prior=read_npz(SOURCE159/'results/comparison'/(label+'.npz'))
                    result=read_npz(ROOT/'results/comparison'/(label+'.npz'))
                    assert np.array_equal(result['potential'][:,:1],prior['potential'][:,:1])
                    assert np.array_equal(result['amplitudes'][:,:1],prior['amplitudes'][:,:1])
                    assert np.array_equal(result['potential'][:,1:3],prior['potential'][:,3:5])
                    expected=reader.values@response['photon'][-1,:,2:4]
                    close(checks,'Independent readout increment:'+label,result['potential'][:,9:11],expected,1e-10)
                    close(checks,'No lower-band readout duplicate:'+label,
                        prior['potential'][:,3:5]+expected,result['potential'][:,3:5],1e-12)
                    for position,start in enumerate([12,14,16]):
                        assert np.array_equal(result['potential'][:,11+2*position:13+2*position],reader.values@response['photon'][-1,:,start:start+2])
    scripts=sorted(ROOT.glob('*.py'))
    assert len(scripts)==8
    for path in scripts:
        compile(path.read_text(),str(path),'exec')
    assert not list(ROOT.rglob('__pycache__'))
    assert len(list((ROOT/'runs').rglob('nodes/*/*.npz')))==648
    largest=max(len(files) for directory,directories,files in os.walk(ROOT))
    assert largest<1000
    workbench=POST.parent/'formalization-workbench'
    assert not [path for path in workbench.rglob('*') if path.is_file() and path.stat().st_mtime>STARTED.timestamp()]
    checks.append(dict(name='Eight scripts compile;no bytecode;648new events;folder/workbench guards',passed=True))
    scientific=[row for packet in packets.values() for row in packet['checks']]
    failures=[row for row in scientific if not row['passed']]
    finish(folder,dict(checks=checks,accepted_scope_verified=all(row['passed'] for row in checks),
        consumed_and_immediate_rehashed=prior_hashes,rehashed_prior_files=len(prior_hashes),
        scientific_checks=len(scientific),passing_scientific_checks=len(scientific)-len(failures),
        retained_failure_names=[row['name'] for row in failures],compiled_scripts=8,
        independently_summed_events=summed,shared_event_reweightings=shared,
        largest_direct_file_count=largest,protected_workbench_recent_modified_file_count=0,
        lower_bands_changed=False,temperature_curve_changed=False,baseline_preserved=True),__file__,
        [*[location/'status.json' for location in locations],*scripts,*ROOT.glob('*.ps1')])
    print(json.dumps(dict(validation=len(checks),passed=all(row['passed'] for row in checks),
        scientific=len(scientific),retained_failures=len(failures),prior_files=len(prior_hashes))),flush=True)
    assert all(row['passed'] for row in checks)


if __name__=='__main__':
    main()
