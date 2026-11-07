from stage158_common import *
from decimal import Decimal,localcontext


def main():
    modest()
    folder=ROOT/'results/validation'
    folder.mkdir(parents=True,exist_ok=False)
    chain=ancestors()
    prior_hashes=authenticate([PARENT/filename for filename in chain[PARENT/'results/stage-integrity.json']['file_hashes']],chain)
    locations=[ROOT/'results/preflight',ROOT/'results/sources',ROOT/'results/comparison']
    locations.extend(ROOT/'runs'/f'band{band}'/f'part{part}' for band in BANDS for part in [0,1])
    locations.extend(ROOT/'results/response'/f'{model}-{route}-{count}'
        for model in ['heavy','cold'] for route in ['local','cubic'] for count in COUNTS)
    checks=[]
    packets={}
    rehashed={}
    for location in locations:
        packet=verify_packet(location)
        packets[str(location)]=packet
        failures=[row for row in packet['checks'] if not row['passed']]
        assert all(row['name'].startswith('CONVERGENCE:') for row in failures)
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
    original=read_npz(SOURCE155/'results/anchor-sources/source.npz')
    assert set(frozen)==set(original)
    for key in frozen:
        assert np.array_equal(frozen[key],original[key])
        assert np.array_equal(source[key],original[key])
    checks.append(dict(name='All inherited source/control/prediction arrays preserved exactly',passed=True))
    manifest=json.loads((ROOT/'results/preflight/events.json').read_text())
    data=packets[str(ROOT/'results/sources')]
    norm=lambda value:np.sqrt(np.maximum(np.sum(value[1:-1]*np.linalg.solve(source['mass'],value[1:-1]),axis=0),0))
    scale=norm(source['actual'])
    independently_summed=0
    shared=0
    for order,which in [(6,'old'),(7,'new')]:
        for band_index,band in enumerate(BANDS):
            frequency=read_npz(ROOT/'results/sources'/f'band{band}-order{order}-frequencies.npz')
            for site_index,site in enumerate(SITES):
                rows=[row for row in manifest[which] if row['site']==site and row['band']==band]
                terms={component:[] for component in COMPONENTS}
                for row in rows:
                    event,weight,path,loop_path=load_event(row)
                    parameters,independent_weight=parameters_and_weight(row['theta'],row['node'])
                    assert weight==independent_weight
                    if which=='new' and row['reused_path']:
                        shared+=1
                    for component in COMPONENTS:
                        terms[component].append(-weight*event[component])
                    independently_summed+=1
                for component_index,component in enumerate(COMPONENTS):
                    values=np.asarray(terms[component])
                    expected=np.asarray([math.fsum(values.reshape(len(rows),-1)[:,column]) for column in range(392)]).reshape(98,4)
                    target=source['old_panels' if order==6 else 'new_panels'][band_index,site_index,component_index]
                    test(checks,'Independent full panel sum:'+str(order)+':'+str(band)+':'+site+':'+component,float(max(norm(expected-target)/scale)),1e-10)
                    test(checks,'Independent frequency partition:'+str(order)+':'+str(band)+':'+site+':'+component,
                        float(max(norm(np.sum(frequency['sites'][site_index,component_index],axis=0)-target)/scale)),1e-10)
                chosen=[row for row in rows if row['node']['frequency']==frequency['frequencies'][len(frequency['frequencies'])//2]]
                with localcontext() as context:
                    context.prec=60
                    exact=np.empty((3,4,4),dtype=object)
                    exact.fill(Decimal(0))
                    for row in chosen:
                        event,weight,path,loop_path=load_event(row)
                        for component_index,component in enumerate(COMPONENTS):
                            for position,moment in enumerate([0,1,2,97]):
                                for column in range(4):
                                    exact[component_index,position,column]+=Decimal.from_float(-weight)*Decimal.from_float(float(event[component][moment,column]))
                    actual=frequency['sites'][site_index,:,len(frequency['frequencies'])//2][:,[0,1,2,97]]
                    close(checks,'Independent60digit centre-frequency moments:'+str(order)+':'+str(band)+':'+site,
                        np.asarray(exact,dtype=float),actual,1e-10)
            joint=np.einsum('s,scfij->cfij',COEFFICIENTS,frequency['sites'])
            close(checks,'Independent common-frequency combination:'+str(order)+':'+str(band),joint,frequency['joint'],1e-10)
    assert independently_summed==2808 and shared==216
    checks.append(dict(name='2808 old/new weighted events reconstructed;216 reused values use new weights',passed=True))
    close(checks,'Independent panel replacement',source['new_panels']-source['old_panels'],source['delta_panels'],1e-10)
    for phase,indices in [('after3',[0]),('after34',[0,1])]:
        increment=sum(source['delta_panels'][index].sum(axis=1) for index in indices)
        for site_index,site in enumerate(SITES):
            close(checks,'Unselected panels unchanged:'+phase+':'+site,
                original_full(original,site)+increment[site_index],source[phase+'_full'][site_index],1e-12)
    for band_index,band in enumerate(BANDS):
        for site_index,site in enumerate(SITES):
            for component_index,component in enumerate(COMPONENTS):
                assert np.array_equal(source[f'band{band}_{site}_{component}'],source['delta_panels'][band_index,site_index,component_index])
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    reader=ShapeReadout(ladder.basis,canonical=True)
    for model in ['heavy','cold']:
        for route in ['local','cubic']:
            for count in COUNTS:
                response=read_npz(ROOT/'results/response'/f'{model}-{route}-{count}/response.npz')
                for key in ['photon','gas','energy','work','number','integrated_number_source']:
                    value=response[key]
                    assert np.array_equal(value[0],np.zeros_like(value[0]))
                    close(checks,'Independent response band telescope:'+model+':'+route+':'+str(count)+':'+key,
                        value[...,:2]+value[...,4:6],value[...,2:4],1e-8)
                for match in [20,40]:
                    prior=read_npz(SOURCE155/'results/comparison'/f'{model}-m{match}-{route}-{count}.npz')
                    after3=None
                    for band,selection,starts in [(3,slice(0,2),[12,14,16]),(4,slice(4,6),[18,20,22])]:
                        label=f'{model}-{route}-{count}-m{match}-band{band}'
                        result=read_npz(ROOT/'results/comparison'/(label+'.npz'))
                        assert np.array_equal(result['potential'][:,:1],prior['potential'][:,:1])
                        assert np.array_equal(result['amplitudes'][:,:1],prior['amplitudes'][:,:1])
                        expected=reader.values@response['photon'][-1,:,selection]
                        close(checks,'Independent new readout increment:'+label,result['potential'][:,9:11],expected,1e-10)
                        if band==3:
                            assert np.array_equal(result['potential'][:,1:3],prior['potential'][:,9:11])
                            after3=result['potential'][:,3:5]
                        else:
                            assert np.array_equal(result['potential'][:,1:3],after3)
                        close(checks,'Independent saved-convention update:'+label,
                            result['potential'][:,1:3]+expected,result['potential'][:,3:5],1e-12)
                        for position,start in enumerate(starts):
                            assert np.array_equal(result['potential'][:,11+2*position:13+2*position],reader.values@response['photon'][-1,:,start:start+2])
    scripts=sorted(ROOT.glob('*.py'))
    assert len(scripts)==8
    for path in scripts:
        compile(path.read_text(),str(path),'exec')
    assert not list(ROOT.rglob('__pycache__'))
    assert len(list((ROOT/'runs').rglob('nodes/*/*.npz')))==1296
    largest=max(len(files) for directory,directories,files in os.walk(ROOT))
    assert largest<1000
    workbench=POST.parent/'formalization-workbench'
    assert not [path for path in workbench.rglob('*') if path.is_file() and path.stat().st_mtime>STARTED.timestamp()]
    checks.append(dict(name='Eight scripts compile;no bytecode;1296 new event files;directory limits;protectedworkbench0',passed=True))
    scientific=[row for packet in packets.values() for row in packet['checks']]
    failures=[row for row in scientific if not row['passed']]
    finish(folder,dict(checks=checks,accepted_scope_verified=all(row['passed'] for row in checks),
        consumed_and_immediate_rehashed=prior_hashes,rehashed_prior_files=len(prior_hashes),
        scientific_checks=len(scientific),passing_scientific_checks=len(scientific)-len(failures),
        retained_failure_names=[row['name'] for row in failures],compiled_scripts=8,
        independently_summed_events=independently_summed,shared_values_verified=shared,
        largest_direct_file_count=largest,protected_workbench_recent_modified_file_count=0,
        temperature_curve_changed=False,baseline_preserved=True),__file__,
        [*[location/'status.json' for location in locations],*scripts,*ROOT.glob('*.ps1')])
    print(json.dumps(dict(validation=len(checks),passed=all(row['passed'] for row in checks),
        scientific=len(scientific),retained_failures=len(failures),prior_files=len(prior_hashes))),flush=True)
    assert all(row['passed'] for row in checks)


if __name__=='__main__':
    main()

