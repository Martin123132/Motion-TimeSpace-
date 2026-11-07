from continue199 import *
import zipfile

def snapshot():
    config=checked_protocol();destination=ROOT/'results/resume-before.zip'
    assert not destination.exists()
    destination.parent.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(destination,'w',compression=zipfile.ZIP_DEFLATED) as archive:
        for name,value in config['bookmarks'].items():
            path=Path(name);assert digest(path)==value
            archive.writestr(path.name,path.read_bytes())
    print('Original resume bytes saved.',flush=True)

def validate():
    config=checked_protocol();source_report=read(ROOT/'results/source-assessment.json')
    selected=source_report;response_root=ROOT;midpoint=None
    if (ROOT/'cold-side-midpoint/results/source-assessment.json').exists():
        midpoint=read(ROOT/'cold-side-midpoint/results/source-assessment.json')
        selected=midpoint;response_root=ROOT/'qualified-continuation'
    if (ROOT/'qualified-continuation/endpoint-matched/results/source-assessment.json').exists():
        response_root=ROOT/'qualified-continuation/endpoint-matched'
    rows=[];responses=[]
    capacity=read(ROOT/'results/capacity-lemma.json')
    rows.extend(capacity['checks'])
    rows.extend(read(ROOT/'results/post-test-diagnosis.json')['checks'])
    rows.extend(read(ROOT/'results/response-wiring-test.json')['checks'])
    if (response_root/'results/scalar-control.json').exists():
        rows.extend(read(response_root/'results/scalar-control.json')['checks'])
    for nodes in ([-.01,-.005,0.],[OFFSET,-.01,-.005]):
        from propagate199 import lagrange
        weights=lagrange(OFFSET,nodes)
        for power in range(3):
            actual=math.fsum(weight*node**power for weight,node in zip(weights,nodes))
            check(rows,f'{nodes}:quadratic exactness power{power}',actual-OFFSET**power,1e-14,'identity')
    norm=microscopic.norm_setup();target=packet(ROOT/'results/target-panel.npz')
    primitive_norm=norm(target['high']+target['low'])
    assert np.all(primitive_norm>0)
    check(rows,'zero-correction negative forecast rejected',int(not np.all(np.ones_like(primitive_norm[4])>.01)),0,'negative_control')
    for base in (1,2):
        delta=base+2
        reconstruction=saved.parts_sum(np.stack([target['high'][0],target['high'][delta],-target['high'][base]]),
            np.stack([target['low'][0],target['low'][delta],-target['low'][base]]))
        check(rows,f'original plus difference gives candidate{base}',np.max(norm(reconstruction[0]+reconstruction[1])/primitive_norm[base]),1e-10,'identity')
    check(rows,'original rejected forecast not propagated',int((ROOT/'responses').exists()),0,'integrity')
    if selected['permission_to_propagate']:
        for model in ('heavy','cold'):
            data={}
            for count in (2048,4096):
                folder=response_root/'responses'/f'{model}-{count}';report=read(folder/'status.json')
                for name,value in report['output_hashes'].items():assert digest(folder/name)==value
                rows.extend(dict(row,name=f'{model}:{count}:'+row['name']) for row in report['checks'])
                data[count]=packet(folder/'terminal.npz')
                responses.append(dict(model=model,count=count,metrics=report['metrics'],interval=report['interval']))
            for column in range(24):
                first=data[2048];second=data[4096]
                measure=second['measure']
                error=saved.response.norm((first['residual'][:,column]-second['residual'][:,column])[:,None],measure)[0]
                scale=saved.response.norm(second['residual'][:,column,None],measure)[0]
                check(rows,f'{model}:{column}:residual mesh',error/max(scale,1e-300),.01,'mesh')
                check(rows,f'{model}:{column}:gas mesh',abs(first['gas'][column]-second['gas'][column])/max(abs(second['gas'][column]),1e-300),.01,'mesh')
    else:
        check(rows,'unqualified continuation not propagated',int((response_root/'responses').exists()),0,'integrity')
    inputs=read(ROOT/'inputs.json')
    for root in (ROOT/'cold-side-midpoint',ROOT/'qualified-continuation',response_root):
        if (root/'inputs.json').exists():inputs.update(read(root/'inputs.json'))
    inputs={name:value for name,value in inputs.items() if not Path(name).is_relative_to(ROOT)}
    for name,value in inputs.items():assert digest(name)==value,name
    write(ROOT/'inputs.json',inputs)
    for path in ROOT.glob('*.py'):compile(path.read_text(encoding='utf-8'),str(path),'exec')
    check(rows,'no bytecode or partial files',len(list(ROOT.rglob('__pycache__')))+len(list(ROOT.rglob('*.partial'))),0,'integrity')
    workbench=BRANCH.parent.parent/'formalization-workbench';assert workbench.is_dir()
    started=datetime.fromisoformat(config['started_utc']).timestamp()
    changed=[str(path) for path in workbench.rglob('*') if path.is_file() and path.stat().st_mtime>=started]
    check(rows,'protected workbench recent changes',len(changed),0,'integrity')
    failed=[row for row in rows if not row['passed']]
    result=dict(state='validated',checks=rows,failed_checks=failed,source_qualified=selected['permission_to_propagate'],
        source_check_count=len(source_report['checks']),retained_source_failures=source_report['failed_checks'],
        original_forecast_qualified=source_report['permission_to_propagate'],
        midpoint_checks=None if midpoint is None else len(midpoint['checks']),
        midpoint_failures=[] if midpoint is None else midpoint['failed_checks'],
        selected_method='cold-side cubic' if midpoint is not None else 'original frozen quadratic',
        response_root=str(response_root),
        retained_unmatched_response_failures=read(ROOT/'results/unmatched-response-validation.json')['failed_checks'] if (ROOT/'results/unmatched-response-validation.json').exists() else [],
        response_records=responses,inputs_rehashed=len(inputs),protected_workbench_recent_modified_file_count=len(changed),
        all_validation_checks_passed=not failed)
    write(ROOT/'results/validation.json',result)
    print(json.dumps(dict(validation_checks=len(rows),validation_failures=failed,source_failures=len(source_report['failed_checks']),
        responses=responses,inputs_rehashed=len(inputs))),flush=True)

def seal():
    config=checked_protocol();validation=read(ROOT/'results/validation.json');assert validation['all_validation_checks_passed']
    inputs=read(ROOT/'inputs.json')
    for name,value in inputs.items():assert digest(name)==value,name
    for name in ('RESULTS.md','NEXT.md'):assert (ROOT/name).is_file()
    bookmarks=[]
    with zipfile.ZipFile(ROOT/'results/resume-before.zip') as archive:
        for name,value in config['bookmarks'].items():
            path=Path(name);before=archive.read(path.name);assert hashlib.sha256(before).hexdigest()==value
            current=path.read_bytes();assert current[current.index(b'# Stage198 COMPLETE'):]==before
            bookmarks.append(dict(path=str(path),previous_sha256=value,current_sha256=digest(path),previous_body_preserved=True))
    write(ROOT/'results/bookmarks.json',bookmarks)
    state='complete' if validation['source_qualified'] else 'complete_with_rejected_forecast'
    write(ROOT/'progress.json',dict(state=state,active_numerical_workers=0,source_qualified=validation['source_qualified'],completed_utc=datetime.now(timezone.utc).isoformat()))
    destination=ROOT/'results/stage-integrity.json';assert not destination.exists()
    parent=read(PARENT/'results/stage-integrity.json')
    assert digest(PARENT/'results/stage-integrity.json')==config['parent_seal_sha256']
    hashes={str(path.relative_to(ROOT)).replace('\\','/'):digest(path) for path in sorted(ROOT.rglob('*')) if path.is_file() and path!=destination}
    inherited=parent['inherited_sealed_payload_count']+len(parent['file_hashes'])
    record=dict(state='complete',stage=199,result_state=state,sealed_at_utc=datetime.now(timezone.utc).isoformat(),
        parent_seal_path=str(PARENT/'results/stage-integrity.json'),parent_seal_sha256=config['parent_seal_sha256'],
        inherited_sealed_payload_count=inherited,file_hashes=hashes,consumed_and_immediate_rehashed=inputs,
        inherited_context='Older archive inherited through authenticated parent seals; consumed and immediate files rehashed',
        source_qualified=validation['source_qualified'],retained_source_failure_count=len(validation['retained_source_failures']),
        retained_response_mesh_failure_count=len(validation['retained_unmatched_response_failures']),
        selected_response_path=validation['response_root'],selected_validation_failures=len(validation['failed_checks']),
        protected_workbench_recent_modified_file_count=validation['protected_workbench_recent_modified_file_count'],
        original_bank_changed=False,global_curve_changed=False,tolerances_changed=False,grids_changed=False,
        maximum_long_running_numerical_workers=1,maximum_concurrent_python_workers=2,short_validation_overlap=True,
        library_threads_per_worker=1,active_workers_at_seal=0,github_action=False,subagents=False,
        next_target=str(ROOT/'NEXT.md'))
    write(destination,record)
    for name,value in hashes.items():assert digest(ROOT/name)==value,name
    print(json.dumps(dict(state=state,payloads=len(hashes),inputs=len(inputs),seal_sha256=digest(destination))),flush=True)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('action',choices=['snapshot','validate','seal']);args=parser.parse_args()
    globals()[args.action]()
