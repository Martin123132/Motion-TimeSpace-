from finer_common import *
import mpmath as mp
import re


def verify_precise(data,packet):
    with mp.workdps(90):
        mass=mp.matrix(data['mass'].tolist())
        stiffness=mp.matrix(data['stiffness'].tolist())
        temperature=mp.matrix(data['temperature'].tolist())
        solved=mp.matrix(packet['solution'])
        photon,gas=solved[:96,:],solved[96:97,:]
        step=mp.mpf(float(data['step']))
        first=int(data['index'])==1
        alpha=(mp.mpf(1) if first else mp.mpf('1.5'))/step
        history=mp.matrix(data['previous_photon'].tolist())/step if first else (2*mp.matrix(data['previous_photon'].tolist())-mp.mpf('.5')*mp.matrix(data['older_photon'].tolist()))/step
        gas_history=mp.matrix([data['previous_gas'].tolist()])/step if first else (2*mp.matrix([data['previous_gas'].tolist()])-mp.mpf('.5')*mp.matrix([data['older_gas'].tolist()]))/step
        rate,heat=mp.mpf(float(data['rate'])),mp.mpf(float(data['heat']))
        external=mp.matrix(data['external'].tolist())
        physical=stiffness*(photon-temperature*gas)+external
        photon_residual=mass*(alpha*photon-history)-rate*physical
        gas_residual=heat*((alpha+1)*gas-gas_history)+rate*temperature.T*physical
        maximum=mp.mpf(0)
        for branch in range(photon.cols):
            photon_scale=mp.norm(alpha*mass*photon.column(branch))+mp.norm(mass*history.column(branch))+mp.norm(rate*physical.column(branch))
            gas_scale=abs(heat*(alpha+1)*gas[branch])+abs(heat*gas_history[branch])+abs(rate)*mp.fsum(abs(temperature[index])*abs(physical[index,branch]) for index in range(96))
            maximum=max(maximum,mp.norm(photon_residual.column(branch))/max(photon_scale,mp.mpf('1e-300')),
                abs(gas_residual[branch])/max(gas_scale,mp.mpf('1e-300')))
        assert maximum<=mp.mpf('1e-35'),maximum
        return float(maximum)


def main():
    modest()
    folder=ROOT/'results/validation'
    folder.mkdir(parents=True,exist_ok=False)
    review=json.loads((ROOT/'ACCURACY-REVIEW.json').read_text())
    scripts=sorted(ROOT.glob('*.py'))
    for script in scripts:
        compile(script.read_bytes(),str(script),'exec')
    script_hashes={digest(script) for script in scripts}
    inputs,consumed,checks=[],set(),[]
    hashes,failures={},{}
    scientific,passing=0,0
    def hashed(path):
        path=Path(path).resolve()
        if path not in hashes:
            hashes[path]=digest(path)
        return hashes[path]
    packets=sorted(path for path in (ROOT/'results').glob('*/status.json') if path.parent!=folder)
    for path in packets:
        packet=json.loads(path.read_text())
        assert packet['state']=='complete' and (path.parent/'COMPLETE').is_file()
        assert packet['script_sha256'] in script_hashes,path
        failed=[row['name'] for row in packet['checks'] if not row['passed']]
        assert failed==review['expected_failed_by_packet'].get(path.parent.name,[]),(path,failed)
        assert packet['count']==len(packet['checks']) and packet['all_checks_passed']==(not failed)
        if failed:
            failures[path.parent.name]=failed
        for source,sha in packet['input_hashes'].items():
            assert hashed(source)==sha,source
            consumed.add(Path(source))
        for archive in path.parent.glob('*.npz'):
            with np.load(archive) as saved:
                for key in saved.files:
                    if saved[key].dtype.kind not in ['U','S']:
                        assert np.isfinite(saved[key]).all(),(archive,key)
            inputs.append(archive)
        inputs.append(path)
        scientific+=packet['count']
        passing+=sum(bool(row['passed']) for row in packet['checks'])
        checks.append(dict(name='Complete finite sourced packet:'+path.parent.name,passed=True))
    assert failures==review['expected_failed_by_packet']
    assert (scientific,passing)==(review['scientific_checks'],review['passing_scientific_checks'])
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    basis=ladder.basis
    inputs.extend(ladder.inputs)
    consumed.update(ladder.inputs)
    for model in ['heavy','cold']:
        path=ROOT/'results'/f'inner-{model}-n5120/prediction.npz'
        saved=read_npz(path)
        assert len(saved['frequency'])==2633 and saved['frequency'][0]==basis.minimum
        assert len(saved['coordinate'])==65 and not np.count_nonzero(saved['defect'][0])
        baseline,window,history_inputs=load_histories(model)
        inputs.extend(history_inputs)
        consumed.update(history_inputs)
        driver,unused=make_drivers(basis,baseline,window,np.array([basis.minimum]),.1)
        margin=int(max(abs(saved['offsets'])))
        spacing=math.log(saved['frequency'][-1]/saved['frequency'][0])/(len(saved['frequency'])-1)
        ghosts=saved['frequency'][0]*np.exp(spacing*np.arange(-margin,0))
        for epoch,coordinate in enumerate(saved['coordinate']):
            coefficient=saved['coefficient_bank'][epoch]
            dc=coefficient[len(saved['offsets'])+1]/ghosts**2
            br=coefficient[len(saved['offsets'])+3:len(saved['offsets'])+3+margin]
            drive=driver(float(coordinate))[:,:3]
            target=(dc[:,None]*drive[1]+br[:,None]*drive[0])/(dc+br)[:,None]
            assert np.allclose(saved['lower_target'][epoch],target,rtol=1e-12,atol=0)
        checks.append(dict(name='Independent finer grid and original lower-boundary law:'+model,passed=True))
        for upper in [.04,.02]:
            response_folder=ROOT/'results'/f'feedback-m{int(upper*1000)}-n5120'
            source=read_npz(response_folder/(model+'-source.npz'))
            response=read_npz(response_folder/(model+'-response.npz'))
            assert len(response['coordinate'])==2049 and np.array_equal(response['saved_step_indices'],np.arange(2049))
            replacement=compact_defect(basis.nodes,saved['frequency'],saved['defect'][-1],upper)
            assert np.allclose(source['replacement_moments'][-1],(basis.values.T*basis.measure)@replacement,rtol=1e-12,atol=0)
            total=basis.values@response['photon'][-1,:,:3]+replacement-basis.values@source['projected_replacement'][-1]
            assert np.max(norm(total-response['physical_change'],basis.measure)/norm(response['physical_change'],basis.measure))<1e-10
            background=thermal_wave.thermal.ThermalBackground(model)
            scale=np.maximum((abs(response['energy'])+background.chi*abs(response['gas'])+abs(response['work'])).max(axis=0),1e-300)
            assert np.max(abs(response['energy']+background.chi*response['gas']+response['work'])/scale)<1e-7
            checks.append(dict(name='Independent total radiation and paired energy bookkeeping:'+model+':'+str(upper),passed=True))
    precision_checks=0
    precision_inputs={}
    for path in sorted((ROOT/'results').glob('gas-precision-*/*-inputs.npz')):
        data=read_npz(path)
        model=path.name.split('-step')[0]
        window=int(path.parent.name.split('-m')[-1])
        cache_key=(model,window)
        if cache_key not in precision_inputs:
            response_folder=ROOT/'results'/f'feedback-m{window}-n5120'
            source=read_npz(response_folder/(model+'-source.npz'))
            response=read_npz(response_folder/(model+'-response.npz'))
            background=thermal_wave.thermal.ThermalBackground(model)
            emission=NonlocalEmission(basis,background,'nonlocal-leading',BRANCH/'infrared-source-domain-20261008/banks/s960-i256')
            forcing=interpolate.interp1d(source['coordinate'],source['source'],axis=0,bounds_error=True)
            precision_inputs[cache_key]=(source,response,background,emission,forcing)
        source,response,background,emission,forcing=precision_inputs[cache_key]
        index=int(data['index'])
        columns=data['columns']
        assert 1<=index<=2048
        assert f'step{index:04d}' in path.name
        position=float(source['coordinate'][0]+(source['coordinate'][-1]-source['coordinate'][0])*index/2048)
        local=background.at(position)
        theta=local['thermal_parameter']
        pieces=forcing(position)
        expected=dict(mass=basis.mass,temperature=basis.temperature,
            stiffness=ladder.at(theta,0)[:96,:96]-emission.at(theta,'dcbr'),
            step=(source['coordinate'][-1]-source['coordinate'][0])/2048,
            rate=local['coefficient']/theta,heat=background.chi,
            external=np.column_stack([pieces.sum(axis=0),*pieces])[:,columns],
            previous_photon=response['photon'][index-1][:,columns],
            older_photon=response['photon'][max(0,index-2)][:,columns],
            previous_gas=response['gas'][index-1,columns],
            older_gas=response['gas'][max(0,index-2),columns],
            old_photon=response['photon'][index][:,columns],old_gas=response['gas'][index,columns])
        for key,value in expected.items():
            assert np.array_equal(data[key],value),(path,key)
        digits_path=path.with_name(path.name.replace('-inputs.npz','-digits70.json'))
        packet=json.loads(digits_path.read_text())
        error=verify_precise(data,packet)
        inputs.append(digits_path)
        lower_path=path.with_name(path.name.replace('-inputs.npz','-digits50.json'))
        inputs.append(lower_path)
        lower=json.loads(lower_path.read_text())
        lower_error=verify_precise(data,lower)
        with mp.workdps(90):
            first,second=mp.matrix(lower['solution']),mp.matrix(packet['solution'])
            agreement=mp.mpf(0)
            for branch in range(first.cols):
                agreement=max(agreement,
                    mp.norm(first[:96,branch]-second[:96,branch])/max(mp.norm(second[:96,branch]),mp.mpf('1e-300')),
                    abs(first[96,branch]-second[96,branch])/max(abs(second[96,branch]),mp.mpf('1e-300')))
            assert agreement<=mp.mpf('1e-25'),(path,agreement)
        assert set([0,1,2]).issubset(set(data['columns'].tolist()))
        checks.append(dict(name='Independent70-digit physical coupled equations:'+path.stem,value=error,limit=1e-35,passed=True))
        checks.append(dict(name='Independent50-digit physical coupled equations:'+path.stem,value=lower_error,limit=1e-35,passed=True))
        checks.append(dict(name='Independent precision agreement and saved-input reconstruction:'+path.stem,value=float(agreement),limit=1e-25,passed=True))
        precision_checks+=1
    assert precision_checks>=4
    documents=sorted(ROOT.glob('*.md'))
    citations=set()
    for document in documents:
        for reference in re.findall(chr(96)+'([^'+chr(96)+']+)'+chr(96),document.read_text(encoding='utf-8')):
            if reference.endswith(('.md','.py','.json','.npz','.pdf')):
                path=(ROOT/reference).resolve()
                assert path.is_file(),(document,reference)
                citations.add(path)
                if not path.is_relative_to(ROOT):
                    consumed.add(path)
    chain=ancestors()
    parent=chain[PARENT/'results/stage-integrity.json']
    rehashed=set()
    for name,sha in parent['file_hashes'].items():
        path=PARENT/name
        assert hashed(path)==sha,path
        rehashed.add(path)
    for path in consumed:
        if not path.is_relative_to(ROOT):
            verify_source(path,chain)
            rehashed.add(path)
    inherited_count=sum(len(packet['file_hashes']) for packet in chain.values())
    assert inherited_count==203770,inherited_count
    checks.append(dict(name='Immediate parent and consumed dependencies unchanged',passed=True,rehashed=len(rehashed)))
    maximum=max(len(files) for directory,directories,files in os.walk(ROOT))
    assert maximum<1000 and not list(ROOT.rglob('__pycache__')) and not list(ROOT.rglob('*.tmp'))
    checks.append(dict(name='Compilation,citations,bytecode and directory capacity',passed=True))
    finish(folder,dict(checks=checks,scientific_checks=scientific,passing_scientific_checks=passing,
        retained_failed_checks=scientific-passing,retained_failure_names=failures,compiled_scripts=len(scripts),
        checked_science_packets=len(packets),accepted_scope_verified=True,largest_direct_file_count=maximum,
        high_precision_witnesses_independently_checked=precision_checks,
        inherited_payload_count=inherited_count,prior_archive_full_rehash_performed=False,
        consumed_and_immediate_rehashed={str(path):hashed(path) for path in sorted(rehashed)}),
        __file__,[*inputs,*scripts,*documents,*citations,ROOT/'ACCURACY-REVIEW.json'])
    print(json.dumps(dict(science=scientific,passes=passing,failures=scientific-passing,validation_checks=len(checks),witnesses=precision_checks,rehashed=len(rehashed))),flush=True)


if __name__=='__main__':
    main()
