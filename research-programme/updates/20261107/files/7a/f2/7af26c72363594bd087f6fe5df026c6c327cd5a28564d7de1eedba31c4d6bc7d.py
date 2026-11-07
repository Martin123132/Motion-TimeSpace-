from operator213 import *
import hashlib


def validate():
    config=protocol()
    manifest=verify_prediction(config)
    assessment=read(ROOT/'results/assessment.json')
    rows=list(assessment['checks'])
    inputs=read(ROOT/'inputs.json')
    for name,value in inputs.items():
        assert digest(name)==value,name
    check(rows,'consumed and immediate inputs unchanged',0,0,'integrity')
    for reference in read(ROOT/'REFERENCE-PROVENANCE.json')['references']:
        assert digest(reference['path'])==reference['sha256'],reference['path']
    check(rows,'supplemental derivation references unchanged',0,0,'integrity')
    assert read(PARENT/'results/assessment.json')['qualified']
    check(rows,'Stage208 rejected forecast retained',len(read(BRANCH/'cold-source-temperature-connection-20261025/results/assessment-036.json')['failed_checks'])-96,0,'integrity')
    acquired={}
    for kind,key in [('anchors','anchors'),('target','target')]:
        acquired[kind]=0
        for row in config[key]:
            values,report=verify_event(event_path(kind,row))
            assert report['coefficients_sha256']==digest(ROOT/'frozen/history-coefficients.npz')
            parameters,weight=source.physics.parameters_and_weight(row['theta'],row['node'])
            loop=read(Path(report['loop_path']))
            assert loop['identity']==loop_identity(parameters)[0]
            assert loop['finite'] and np.isfinite(loop['scalar'])
            assert float(values['weight'])==weight and float(values['theta'])==row['theta']
            assert json.loads(str(values['node']))==row['node']
            if kind=='target':
                assert datetime.fromisoformat(report['started_at'])>datetime.fromisoformat(manifest['frozen_at'])
            else:
                assert datetime.fromisoformat(report['finished_at'])<datetime.fromisoformat(manifest['frozen_at'])
            acquired[kind]+=int(report['new_virtual_integral'])
    check(rows,'all108 anchor events authenticated',len(list((ROOT/'anchors').rglob('event-*.npz')))-108,0,'integrity')
    check(rows,'all36 target events authenticated',len(list((ROOT/'target').rglob('event-*.npz')))-36,0,'integrity')
    check(rows,'only absent anchor inputs calculated',acquired['anchors']-(108-config['anchor_cache_hits']),0,'integrity')
    check(rows,'only absent target inputs calculated',acquired['target']-(36-config['target_cache_hits']),0,'integrity')
    check(rows,'local virtual cache count',len(list((ROOT/'virtual-cache').rglob('*.json')))-sum(acquired.values()),0,'integrity')
    for name in ('frozen/history-coefficients.npz','histories/heavy-half.json','histories/heavy-quarter.json',
                 'histories/cold-half.json','histories/cold-quarter.json'):
        check(rows,name+':unchanged reused bytes',int(digest(ROOT/name)!=digest(PARENT/name)),0,'integrity')
    reference=packet(config['reference_source_path'])
    combined=packet(ROOT/'results/source-sum-7.npz')
    sample_errors=[]
    with mp.workdps(100):
        for grid,component,row,column in ((0,0,0,0),(1,4,97,3),(0,3,42,2),(1,5,81,1)):
            full_exact=mp.mpf(float(reference['predicted_high'][grid,component,row,column]))+mp.mpf(float(reference['predicted_low'][grid,component,row,column]))
            for frequency in config['frequencies']:
                frequency_index=next(item['frequency_index'] for item in config['target'] if item['frequency']==frequency)
                values=packet(ROOT/f'results/source-node-{frequency_index}.npz')
                terms=[]
                for anchor_index,label in enumerate(('warm','middle','cold')):
                    weight=mp.mpf(config['operator_weights'][anchor_index])
                    for event in range(36):
                        anchor=packet(ROOT/f'anchors/frequency-{frequency_index}/{label}/event-{event:02d}.npz')
                        components=([1,2,3] if component==4 else [0,1,2,3] if component==5 else [component])
                        for part in components:
                            terms.append(weight*(mp.mpf(float(anchor['high'][grid,part,row,column]))+
                                                 mp.mpf(float(anchor['low'][grid,part,row,column]))))
                exact=mp.fsum(terms)
                computed=mp.mpf(float(values['predicted_high'][grid,component,row,column]))+mp.mpf(float(values['predicted_low'][grid,component,row,column]))
                error=float(abs(exact-computed)/max(abs(exact),mp.mpf('1e-300')))
                check(rows,f'100-digit node {frequency_index}:{grid}:{component}:{row}:{column}',error,1e-10,'identity')
                sample_errors.append(error)
                full_exact+=exact
            computed=mp.mpf(float(combined['predicted_high'][grid,component,row,column]))+mp.mpf(float(combined['predicted_low'][grid,component,row,column]))
            error=float(abs(full_exact-computed)/max(abs(full_exact),mp.mpf('1e-300')))
            check(rows,f'100-digit seven-node sum {grid}:{component}:{row}:{column}',error,1e-10,'identity')
            sample_errors.append(error)
    for path in ROOT.rglob('*.py'):
        compile(path.read_text(encoding='utf-8'),str(path),'exec')
    check(rows,'no bytecode or unfinished writes',len(list(ROOT.rglob('__pycache__')))+len(list(ROOT.rglob('*.partial')))+len(list(ROOT.rglob('*.tmp'))),0,'integrity')
    for name,value in config['bookmarks'].items():
        assert digest(name)==value,name
    protected=BRANCH.parent.parent/'formalization-workbench'
    started=datetime.fromisoformat(config['turn_start']).timestamp()
    changed=[str(path) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime>=started]
    check(rows,'protected workbench recent-mtime count',len(changed),0,'integrity')
    failed=[row for row in rows if not row['passed']]
    new_failures=[row for row in rows[len(assessment['checks']):] if not row['passed']]
    assert not new_failures,new_failures
    integrity_failures=[row for row in failed if row['category'] not in ('prediction','mesh')]
    assert not integrity_failures,integrity_failures
    report=dict(stage=213,checks=rows,failed_checks=failed,qualified=assessment['qualified'],
                integrity_passed=not integrity_failures,inputs_rehashed=len(inputs),new_virtual_inputs=acquired,
                source_assessment_sha256=digest(ROOT/'results/assessment.json'),
                protected_workbench_recent_modified_file_count=len(changed),workbench_guard_scope='recent mtime, not full-tree hash',
                decimal_sample_max=max(sample_errors),permission_to_propagate=False,full_band=assessment['full_band'],
                full_original_8_20_panel_qualified=assessment['full_original_8_20_panel_qualified'],all_frequency_bands_qualified=False,uniform_temperature_qualified=False)
    write(ROOT/'results/validation.json',report)
    print(json.dumps(dict(checks=len(rows),failed=len(failed),inputs_rehashed=len(inputs),new_virtual_inputs=acquired,qualified=report['qualified'])),flush=True)


def seal():
    config=protocol()
    validation=read(ROOT/'results/validation.json')
    assert validation['integrity_passed']
    assert validation['source_assessment_sha256']==digest(ROOT/'results/assessment.json')
    for reference in read(ROOT/'REFERENCE-PROVENANCE.json')['references']:
        assert digest(reference['path'])==reference['sha256'],reference['path']
    for name in ('RESULTS.md','NEXT.md','RUN-NOTES.md'):
        assert (ROOT/name).is_file()
    inputs=read(ROOT/'inputs.json')
    for name,value in inputs.items():
        assert digest(name)==value,name
    bookmarks=[]
    with zipfile.ZipFile(ROOT/'results/resume-before.zip') as archive:
        for name,value in config['bookmarks'].items():
            path=Path(name)
            before=archive.read(path.name)
            assert hashlib.sha256(before).hexdigest()==value
            assert path.read_bytes().endswith(before)
            bookmarks.append(dict(path=str(path),previous_sha256=value,current_sha256=digest(path),previous_body_preserved=True))
    write(ROOT/'results/bookmarks.json',bookmarks)
    write(ROOT/'progress.json',dict(state='complete',nodes_and_seven_frequency_qualified=validation['qualified'],full_band=validation['full_band'],
                                   permission_to_propagate=False,active_numerical_workers=0,completed_at=now()))
    destination=ROOT/'results/stage-integrity.json'
    assert not destination.exists()
    parent=read(PARENT/'results/stage-integrity.json')
    hashes={str(path.relative_to(ROOT)).replace('\\','/'):digest(path) for path in sorted(ROOT.rglob('*')) if path.is_file() and path!=destination}
    write(destination,dict(stage=213,state='complete',sealed_at=now(),nodes_and_seven_frequency_qualified=validation['qualified'],
          full_band=validation['full_band'],full_original_8_20_panel_qualified=validation['full_original_8_20_panel_qualified'],
          all_frequency_bands_qualified=False,uniform_temperature_qualified=False,permission_to_propagate=False,parent_seal_path=str(PARENT/'results/stage-integrity.json'),parent_seal_sha256=PARENT_SHA,
          inherited_sealed_payload_count=parent['inherited_sealed_payload_count']+len(parent['file_hashes']),
          file_hashes=hashes,consumed_and_immediate_rehashed=inputs,anchor_events=108,direct_target_events=36,reused_target_events=216,
          target_fraction=config['target_fraction'],theta=config['theta'],frequencies=FREQUENCIES,coverage=config['coverage'],
          retained_prediction_failures=len(validation['failed_checks']),new_virtual_inputs=validation['new_virtual_inputs'],
          original_bank_changed=False,global_curve_changed=False,grids_changed=False,tolerances_changed=False,
          maximum_concurrent_event_workers=2,numerical_threads_per_worker=1,active_workers_at_seal=0,
          protected_workbench_recent_modified_file_count=validation['protected_workbench_recent_modified_file_count'],
          github_action=False,subagents=False,next_target=str(ROOT/'NEXT.md')))
    print(json.dumps(dict(seal=str(destination),sha256=digest(destination),payloads=len(hashes))),flush=True)


if __name__=='__main__':
    source.modest()
    parser=argparse.ArgumentParser()
    parser.add_argument('phase',choices=['validate','seal'])
    args=parser.parse_args()
    {'validate':validate,'seal':seal}[args.phase]()

