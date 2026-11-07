from response221 import *

OLD=BRANCH/'cold-complete-seven-frequency-source-20261024'
REFERENCES={
    'results/seven-frequency-source.npz':'78cfd05cd002c0ab94042d8a9ec0442827245586dd15fdbd99adc161594c1ccf',
    'frozen/history-coefficients.npz':'cc935623db57d2e0e59075fc567e648fb47ca6f4d41ef7b7b34e3bc1a66a0026',
    'configuration.json':'902d99d109030961e987508fab8d6b459d6fc2c30a7aa75683792d35985ca076',
}


def compare_source(label,predicted,expected,factor,limit,rows,records,category):
    error=metrics.subtract(predicted,expected)
    for field,measure in [('photon',lambda values:metrics.norms(values,factor)),('gas',lambda values:abs(values[...,-1,:]))]:
        ratio=measure(error[0]+error[1])/np.maximum(measure(expected[0]+expected[1]),1e-300)
        for grid,component,column in np.ndindex(ratio.shape):
            value=float(ratio[grid,component,column])
            records.append(dict(scope=label,field=field,grid=GRIDS[grid],component=COMPONENTS[component],
                model=MODELS[column//2],join=column%2,relative=value))
            check(rows,f'{label}:{field}:{grid}:{component}:{column}',value,limit,category)


def endpoint():
    protocol();rows=[];records=[]
    for name,value in REFERENCES.items():
        assert digest(OLD/name)==value,name
    old_config=read(OLD/'configuration.json')
    assert old_config['prediction_groups']==['photon-half','gas-half','photon-quarter','gas-quarter','zero']
    assert old_config['actual_groups']==['original','repaired-half','repaired-quarter']
    old=packet(OLD/'results/seven-frequency-source.npz')
    old_coefficients=packet(OLD/'frozen/history-coefficients.npz')
    increments=[metrics.subtract((old['absolute_high'][grid+1],old['absolute_low'][grid+1]),
        (old['absolute_high'][0],old['absolute_low'][0])) for grid in (0,1)]
    actual=tuple(np.stack([pair[part] for pair in increments]) for part in (0,1))
    assembled=[]
    with mp.workdps(100):
        for model_index,model in enumerate(MODELS):
            values,report=verify_point(model,LAST)
            check(rows,model+':same endpoint theta',float(values['theta'])/old_config['theta']-1,1e-10,'integrity')
            check(rows,model+':same endpoint fraction',float(values['fraction'])-old_config['target_fraction'],0,'integrity')
            coefficients=packet(point_folder(model,LAST)/'coefficients.npz')
            for grid in (0,1):
                first=8*grid+2*model_index
                active=list(range(96))+[98]
                expected=[sum(mp.mpf(float(old_coefficients[name][entry,column]))
                    for name in ('prediction_high','prediction_low') for column in (first,first+4)) for entry in active]
                current=[mp.mpf(float(coefficients['high'][entry,grid]))+mp.mpf(float(coefficients['low'][entry,grid])) for entry in range(97)]
                for field,selection in [('photon',slice(0,96)),('gas',slice(96,97))]:
                    error=mp.sqrt(mp.fsum((left-right)**2 for left,right in zip(current[selection],expected[selection])))
                    scale=mp.sqrt(mp.fsum(value**2 for value in expected[selection]))
                    check(rows,f'{model}:{GRIDS[grid]}:same coefficient repair:{field}',error/max(scale,mp.mpf('1e-300')),1e-10,'identity')
            assembled.append((values['high'][0,:2],values['low'][0,:2]))
    predicted=tuple(np.concatenate([pair[part] for pair in assembled],axis=-1) for part in (0,1))
    factor=linear.cholesky(packet(PARENT/'frozen/basis-metric.npz')['mass'],lower=True)
    compare_source('same-history split-source replay',predicted,(old['prediction_high'],old['prediction_low']),factor,1e-10,rows,records,'identity')
    compare_source('old direct repaired-minus-original',predicted,actual,factor,.01,rows,records,'prediction')
    failed=[row for row in rows if not row['passed']]
    save(ROOT/'results/cold-endpoint-replay.npz',predicted_high=predicted[0],predicted_low=predicted[1],
        actual_high=actual[0],actual_low=actual[1])
    write(ROOT/'results/endpoint-replay.json',dict(checks=rows,failed_checks=failed,records=records,qualified=not failed,
        completed_at=now(),reference_hashes={str(OLD/name):value for name,value in REFERENCES.items()},
        declaration_sha256=digest(ROOT/'ENDPOINT-CHECK.md'),script_sha256=digest(ROOT/'crosscheck221.py'),
        new_observational_test=False,known_cold_endpoint=True))
    print(json.dumps(dict(checks=len(rows),failed=len(failed),maxima={scope:max(row['relative'] for row in records if row['scope']==scope)
        for scope in sorted({row['scope'] for row in records})})),flush=True)


def close():
    config=protocol();main=read(ROOT/'results/assessment.json');endpoint_report=read(ROOT/'results/endpoint-replay.json')
    assert digest(ROOT/'crosscheck221.py')==endpoint_report['script_sha256']
    assert digest(ROOT/'ENDPOINT-CHECK.md')==endpoint_report['declaration_sha256']
    inputs=read(ROOT/'inputs-final.json')
    for name,value in endpoint_report['reference_hashes'].items():
        register(inputs,name,value)
    for name,value in inputs.items():
        assert digest(name)==value,name
    failures=[dict(row,owner=owner) for owner,report in [('transport',main),('endpoint_replay',endpoint_report)] for row in report['failed_checks']]
    qualified=not failures
    implementation_qualified=not any(row['category'] not in ('comparison','prediction') for row in failures)
    current=dict(stage=221,qualified=qualified,implementation_qualified=implementation_qualified,
        checks_count=len(main['checks'])+len(endpoint_report['checks']),failed_checks=failures,
        reports={str(path.relative_to(ROOT)):digest(path) for path in (ROOT/'results/assessment.json',ROOT/'results/endpoint-replay.json')},
        inputs_rehashed=len(inputs),scope='controlled full-panel short-interval transport with explicit incoming maps and a known cold-source replay')
    write(ROOT/'results/current-validation.json',current)
    for name in ('RESULTS.md','NEXT.md'):
        assert (ROOT/name).is_file()
    bookmarks=[]
    with zipfile.ZipFile(ROOT/'results/resume-before.zip') as archive:
        for name,value in config['bookmarks'].items():
            before=archive.read(Path(name).name)
            assert hashlib.sha256(before).hexdigest()==value and Path(name).read_bytes().endswith(before)
            bookmarks.append(dict(path=name,previous_sha256=value,current_sha256=digest(name),previous_body_preserved=True))
    write(ROOT/'results/bookmarks.json',bookmarks)
    write(ROOT/'progress.json',dict(state='complete',qualified=qualified,implementation_qualified=implementation_qualified,
        source_points=128,response_cases=4,active_workers=0,completed_at=now()))
    destination=ROOT/'results/stage-integrity.json';assert not destination.exists()
    parent=read(PARENT/'results/stage-integrity.json')
    hashes={path.relative_to(ROOT).as_posix():digest(path) for path in sorted(ROOT.rglob('*')) if path.is_file() and path!=destination}
    write(destination,dict(stage=221,state='complete',qualified=qualified,implementation_qualified=implementation_qualified,sealed_at=now(),
        parent_seal_path=str(PARENT/'results/stage-integrity.json'),parent_seal_sha256=PARENT_SHA,
        inherited_sealed_payload_count=parent['inherited_sealed_payload_count']+len(parent['file_hashes']),
        consumed_and_immediate_rehashed=inputs,file_hashes=hashes,current_validation_path='results/current-validation.json',
        retained_current_failures=len(failures),active_workers_at_seal=0,original_bank_changed=False,global_curve_changed=False,
        grids_changed=False,tolerances_changed=False,github_action=False,subagents=False,next_target=str(ROOT/'NEXT.md')))
    print(json.dumps(dict(qualified=qualified,checks=current['checks_count'],failed=len(failures),payloads=len(hashes),sha256=digest(destination))),flush=True)


if __name__=='__main__':
    source.modest()
    parser=argparse.ArgumentParser()
    parser.add_argument('phase',choices=['endpoint','close'])
    args=parser.parse_args()
    {'endpoint':endpoint,'close':close}[args.phase]()
