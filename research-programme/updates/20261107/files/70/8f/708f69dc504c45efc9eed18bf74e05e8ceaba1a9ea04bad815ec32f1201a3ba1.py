from stage159_common import *
from decimal import Decimal,localcontext


def main():
    modest()
    folder=ROOT/'results/validation'
    folder.mkdir(parents=True,exist_ok=False)
    chain=ancestors()
    prior_hashes=authenticate([PARENT/filename for filename in chain[PARENT/'results/stage-integrity.json']['file_hashes']],chain)
    locations=[ROOT/'results/preflight',ROOT/'results/sources',ROOT/'results/comparison']
    locations.extend(ROOT/'runs/band3'/f'part{part}' for part in [0,1])
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
    parent=read_npz(PARENT/'results/sources/source.npz')
    assert set(frozen)==set(parent)
    for key in frozen:
        assert np.array_equal(frozen[key],parent[key])
        assert np.array_equal(source[key],parent[key])
    checks.append(dict(name='Every inherited source/control/prediction array,including3–8,bitwise preserved',passed=True))
    manifest=json.loads((ROOT/'results/preflight/events.json').read_text())
    norm=lambda value:np.sqrt(np.maximum(np.sum(value[1:-1]*np.linalg.solve(source['mass'],value[1:-1]),axis=0),0))
    scale=norm(source['actual'])
    summed=0
    for order,which in [(7,'old'),(8,'new')]:
        frequency=read_npz(ROOT/'results/sources'/f'order{order}-frequency.npz')
        for site_index,site in enumerate(SITES):
            rows=[row for row in manifest[which] if row['site']==site]
            assert len(rows)==36*order
            rule=list(incoming_rule(order,1e-5,24.))
            wanted=np.asarray([(frequency,weight) for frequency,weight in rule if 1.<frequency<3.])
            assert np.array_equal(frequency['frequencies'],wanted[:,0])
            assert np.array_equal(frequency['seed_weights'],wanted[:,1])
            terms={component:[] for component in COMPONENTS}
            for row in rows:
                saved,weight,path,loop_path=load_event(row)
                parameters,independent_weight=parameters_and_weight(row['theta'],row['node'])
                assert weight==independent_weight
                for component in COMPONENTS:
                    terms[component].append(-weight*saved[component])
                summed+=1
            for component_index,component in enumerate(COMPONENTS):
                values=np.asarray(terms[component]).reshape(len(rows),-1)
                expected=np.asarray([math.fsum(values[:,column]) for column in range(392)]).reshape(98,4)
                target=source['order7_reference_panel' if order==7 else 'order8_panel'][site_index,component_index]
                test(checks,'Independent complete source sum:'+str(order)+':'+site+':'+component,float(max(norm(expected-target)/scale)),1e-10)
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
    assert summed==1620
    checks.append(dict(name='756 reference and864 new weighted events independently reconstructed',passed=True))
    close(checks,'Old order7 reference matches parent panel',source['order7_reference_panel'],parent['new_panels'][0],1e-10)
    close(checks,'Independent order8-minus7 replacement',source['order8_panel']-source['order7_reference_panel'],source['order8_delta'],1e-10)
    for site_index,site in enumerate(SITES):
        increment=sum(source['order8_delta'][site_index])
        assert np.array_equal(source['order8_'+site+'_total'],increment)
        close(checks,'Preserved3–8 and other panels:'+site,parent['after34_full'][site_index]+increment,
            source['after_order8_full'][site_index],1e-12)
    packet=packets[str(ROOT/'results/sources')]
    current_joint=np.einsum('s,scij->cij',COEFFICIENTS,source['order8_delta'])
    previous_joint=np.einsum('s,scij->cij',COEFFICIENTS,parent['delta_panels'][0])
    for index,component in enumerate(COMPONENTS):
        close(checks,'Independent own-panel contraction:'+component,norm(current_joint[index])/norm(previous_joint[index]),
            packet['panel_metrics']['component_step_ratio_vs_order7_minus6'][index],1e-10)
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
                    close(checks,'Independent three-site response sum:'+model+':'+route+':'+str(count)+':'+key,
                        sum(value[...,start:start+2] for start in [12,14,16]),value[...,2:4],1e-8)
                for match in [20,40]:
                    label=f'{model}-{route}-{count}-m{match}'
                    prior=read_npz(PARENT/'results/comparison'/(label+'-band4.npz'))
                    result=read_npz(ROOT/'results/comparison'/(label+'.npz'))
                    assert np.array_equal(result['potential'][:,:1],prior['potential'][:,:1])
                    assert np.array_equal(result['amplitudes'][:,:1],prior['amplitudes'][:,:1])
                    assert np.array_equal(result['potential'][:,1:3],prior['potential'][:,3:5])
                    expected=reader.values@response['photon'][-1,:,2:4]
                    close(checks,'Independent readout increment:'+label,result['potential'][:,9:11],expected,1e-10)
                    close(checks,'No duplicate3–8 update:'+label,
                        prior['potential'][:,3:5]+expected,result['potential'][:,3:5],1e-12)
                    for position,start in enumerate([12,14,16]):
                        assert np.array_equal(result['potential'][:,11+2*position:13+2*position],reader.values@response['photon'][-1,:,start:start+2])
    scripts=sorted(ROOT.glob('*.py'))
    assert len(scripts)==8
    for path in scripts:
        compile(path.read_text(),str(path),'exec')
    assert not list(ROOT.rglob('__pycache__'))
    assert len(list((ROOT/'runs').rglob('nodes/*/*.npz')))==864
    largest=max(len(files) for directory,directories,files in os.walk(ROOT))
    assert largest<1000
    workbench=POST.parent/'formalization-workbench'
    assert not [path for path in workbench.rglob('*') if path.is_file() and path.stat().st_mtime>STARTED.timestamp()]
    checks.append(dict(name='Eight scripts compile;no bytecode;864new events;folder limits;protectedworkbench0',passed=True))
    scientific=[row for packet in packets.values() for row in packet['checks']]
    failures=[row for row in scientific if not row['passed']]
    finish(folder,dict(checks=checks,accepted_scope_verified=all(row['passed'] for row in checks),
        consumed_and_immediate_rehashed=prior_hashes,rehashed_prior_files=len(prior_hashes),
        scientific_checks=len(scientific),passing_scientific_checks=len(scientific)-len(failures),
        retained_failure_names=[row['name'] for row in failures],compiled_scripts=8,
        independently_summed_events=summed,retained_band38_order=7,
        largest_direct_file_count=largest,protected_workbench_recent_modified_file_count=0,
        temperature_curve_changed=False,baseline_preserved=True),__file__,
        [*[location/'status.json' for location in locations],*scripts,*ROOT.glob('*.ps1')])
    print(json.dumps(dict(validation=len(checks),passed=all(row['passed'] for row in checks),
        scientific=len(scientific),retained_failures=len(failures),prior_files=len(prior_hashes))),flush=True)
    assert all(row['passed'] for row in checks)


if __name__=='__main__':
    main()

