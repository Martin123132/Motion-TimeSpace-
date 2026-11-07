from node214 import *
REPAIR=ROOT/'precision-repair'


def repair_protocol():
    config,extension=node_protocol()
    repair=read(REPAIR/'configuration.json')
    for name,value in repair['protocol_hashes'].items():
        assert digest(ROOT/name)==value,name
    assert digest(EXT/'results/assessment.json')==repair['retained_failed_assessment_sha256']
    return config,extension,repair


def prepare_repair():
    config,extension=node_protocol()
    assert not (REPAIR/'configuration.json').exists()
    failed=read(EXT/'results/assessment.json')['failed_checks']
    assert len(failed)==8 and all(row['name'].startswith('event-32:') for row in failed)
    write(REPAIR/'configuration.json',dict(frozen_at=now(),state_probe_event=32,
        retained_failed_assessment_sha256=digest(EXT/'results/assessment.json'),
        original_evaluator_precision=60,adapter_precision_observed=15,identity_tolerance=1e-10,
        protocol_hashes={name:digest(ROOT/name) for name in ('precision214.py','PRECISION-REPAIR.md')},
        change='restore original global mpmath context for non-protected state rows; no physical input or tolerance change'))
    print('Precision-context repair protocol saved.',flush=True)


def state_overlay(row,old,bundle,evaluators):
    mp.mp.dps=60
    parameters,weight=source.physics.parameters_and_weight(row['theta'],row['node'])
    raw=evaluators[0]['difference'].state_correction(parameters)['total']
    assert raw.shape==(98,196)
    raw=(-weight*raw).reshape(98,98,2)[:,:97,:]
    high,low=old[0].copy(),old[1].copy()
    retained_rows=list(source.LOW)
    for index in range(98):
        if index not in retained_rows:
            high[3,index]=raw[index]
            low[3,index]=0.
    for component,members in ((4,[1,2,3]),(5,[0,1,2,3])):
        high[component],low[component]=metrics.combine([(high[index],low[index]) for index in members])
    return high,low


def probe():
    config,extension,repair=repair_protocol()
    assert not (REPAIR/'results/probe.json').exists()
    row=extension['events'][32]
    original,theta=source.context(config['target_fraction'])
    bundle=OperatorBundle(cached.CachedFeatures(original),original.inputs)
    evaluators=cached.models(bundle)
    source.physics.precise_state=precise.precise_state
    parameters,weight=source.physics.parameters_and_weight(theta,row['node'])
    loop=read(row['loop_path'])
    assert digest(row['loop_path'])==row['loop_sha256']
    before=mp.mp.dps
    started=now();began=time.monotonic()
    high,low,diagnostics=owner.microscopic.weighted(parameters,bundle,evaluators,loop['scalar'],weight)
    assert mp.mp.dps==60
    full=tuple(np.moveaxis(values,0,2).reshape(6,98,98,2)[:,:,:97,:] for values in (high,low))
    old_packet=packet(EXT/'events/event-32.npz')
    old=(old_packet['high'],old_packet['low'])
    overlay=state_overlay(row,old,bundle,evaluators)
    rows=[]
    for name,value in diagnostics.items():
        check(rows,'production60:'+name,value,1e-10,'identity')
    for index,name in enumerate(('high','low')):
        check(rows,name+':unaffected three primitives bitwise',int(not np.array_equal(full[index][:3],old[index][:3])),0,'integrity')
        check(rows,name+':protected state rows bitwise',int(not np.array_equal(full[index][3,source.LOW],old[index][3,source.LOW])),0,'integrity')
    delta=metrics.subtract(overlay,full)
    for component in range(6):
        relative=np.linalg.norm(delta[0][component]+delta[1][component])/max(np.linalg.norm(full[0][component]+full[1][component]),1e-300)
        check(rows,f'overlay versus original production evaluator:{component}',relative,1e-10,'identity')
    save(REPAIR/'results/event-32-full-production.npz',high=full[0],low=full[1])
    save(REPAIR/'results/event-32-overlay.npz',high=overlay[0],low=overlay[1])
    report=dict(started_at=started,finished_at=now(),seconds=time.monotonic()-began,
        precision_before=before,precision_after=mp.mp.dps,checks=rows,failed_checks=[entry for entry in rows if not entry['passed']],
        production_matrix_sha256=digest(REPAIR/'results/event-32-full-production.npz'),
        overlay_sha256=digest(REPAIR/'results/event-32-overlay.npz'))
    write(REPAIR/'results/probe.json',report)
    print(json.dumps(dict(seconds=report['seconds'],precision_before=before,precision_after=mp.mp.dps,failed=report['failed_checks'])),flush=True)
    assert not report['failed_checks'],report['failed_checks']


def build():
    config,extension,repair=repair_protocol()
    probe=read(REPAIR/'results/probe.json')
    assert not probe['failed_checks']
    assert digest(REPAIR/'results/event-32-full-production.npz')==probe['production_matrix_sha256']
    original,theta=source.context(config['target_fraction'])
    bundle=OperatorBundle(cached.CachedFeatures(original),original.inputs)
    evaluators=cached.models(bundle)
    source.physics.precise_state=precise.precise_state
    matrices,unused=pairs()
    began=time.monotonic()
    for row,old in zip(extension['events'],matrices):
        event=row['event']
        path=REPAIR/f'events/event-{event:02d}.npz'
        assert not path.exists()
        values=state_overlay(row,old,bundle,evaluators)
        save(path,high=values[0],low=values[1])
        write(path.with_suffix('.json'),dict(sha256=digest(path),event=event,precision=60,
              original_event_sha256=digest(ROOT/'results/operator.npz' if event==0 else EXT/f'events/event-{event:02d}.npz'),
              loop_path=row['loop_path'],loop_sha256=row['loop_sha256'],finished_at=now()))
    write(REPAIR/'results/build.json',dict(events=36,seconds=time.monotonic()-began,new_virtual_integrals=0,
                original_real_and_virtual_values_reused=True,protected_state_rows_reused=True,finished_at=now()))
    print(json.dumps(dict(state='repaired36_state_matrices',seconds=time.monotonic()-began)),flush=True)


def repaired_pairs():
    values=[];hashes={}
    for event in range(36):
        path=REPAIR/f'events/event-{event:02d}.npz'
        report=read(path.with_suffix('.json'))
        assert digest(path)==report['sha256']
        current=packet(path)
        values.append((current['high'],current['low']))
        hashes[str(path)]=digest(path)
    return values,hashes


def freeze_repair():
    config,extension,repair=repair_protocol()
    assert not (REPAIR/'frozen/manifest.json').exists()
    matrices,hashes=repaired_pairs()
    coefficients=packet(ROOT/'frozen/history-coefficients.npz')
    predictions=[]
    for event,matrix in enumerate(matrices):
        prediction=contract(*matrix,coefficients)
        path=REPAIR/f'frozen/prediction-{event:02d}.npz'
        save(path,high=prediction[0],low=prediction[1])
        hashes[str(path)]=digest(path)
        predictions.append(prediction)
    total=matrix_sum(matrices)
    path=REPAIR/'results/operator-node.npz'
    save(path,high=total[0],low=total[1],active=np.array(ACTIVE),theta=config['theta'],frequency=config['event']['frequency'])
    hashes[str(path)]=digest(path)
    prediction=contract(*total,coefficients)
    path=REPAIR/'frozen/node-prediction.npz'
    save(path,high=prediction[0],low=prediction[1])
    hashes[str(path)]=digest(path)
    summed=metrics.primitives(predictions)
    path=REPAIR/'frozen/event-first-prediction.npz'
    save(path,high=summed[0],low=summed[1])
    hashes[str(path)]=digest(path)
    write(REPAIR/'frozen/manifest.json',dict(frozen_at=now(),files=hashes,configuration_sha256=digest(REPAIR/'configuration.json'),
              replay_not_holdout=True,events=36,contraction_digits=80))
    print('Repaired matrix/source predictions frozen.',flush=True)


def assess_repair():
    config,extension,repair=repair_protocol()
    assert not (REPAIR/'results/assessment.json').exists()
    manifest=read(REPAIR/'frozen/manifest.json')
    assert digest(REPAIR/'configuration.json')==manifest['configuration_sha256']
    for name,value in manifest['files'].items():
        assert digest(name)==value,name
    basis=packet(ROOT/'frozen/basis-metric.npz')
    factor=linear.cholesky(basis['mass'],lower=True)
    checks=list(read(REPAIR/'results/probe.json')['checks']);records=[];directs=[]
    matrices,unused=repaired_pairs()
    original_matrices,unused=pairs()
    for row,matrix,old in zip(extension['events'],matrices,original_matrices):
        event=row['event']
        for index,label in enumerate(('high','low')):
            check(checks,f'event{event}:{label}:baseline-real-virtual unchanged',int(not np.array_equal(matrix[index][:3],old[index][:3])),0,'integrity')
            check(checks,f'event{event}:{label}:protected state unchanged',int(not np.array_equal(matrix[index][3,source.LOW],old[index][3,source.LOW])),0,'integrity')
        assert digest(row['direct_path'])==row['direct_sha256']
        direct=packet(row['direct_path']);actual=(direct['high'],direct['low']);directs.append(actual)
        predicted=packet(REPAIR/f'frozen/prediction-{event:02d}.npz')
        compare(f'event-{event}',(predicted['high'],predicted['low']),actual,factor,checks,records)
    direct_sum=metrics.primitives(directs)
    predicted=packet(REPAIR/'frozen/node-prediction.npz')
    prediction=(predicted['high'],predicted['low'])
    compare('full-node',prediction,direct_sum,factor,checks,records)
    saved_node=packet(PARENT/'results/source-node-6.npz')
    compare('saved-source-reconstruction',direct_sum,(saved_node['actual_high'],saved_node['actual_low']),factor,checks,records)
    event_first=packet(REPAIR/'frozen/event-first-prediction.npz')
    compare('contract-before-after-sum',prediction,(event_first['high'],event_first['low']),factor,checks,records)
    identities=matrix_identities(packet(REPAIR/'results/operator-node.npz'),basis,checks)
    failed=[row for row in checks if not row['passed']]
    report=dict(stage=214,state='repaired_full_node_operator_qualified' if not failed else 'repaired_full_node_rejected',
        qualified=not failed,checks=checks,failed_checks=failed,records=records,column_identities=identities,
        retained_original_representation_failures=len(read(EXT/'results/assessment.json')['failed_checks']),
        original_bank_changed=False,grids_changed=False,tolerances_changed=False,new_virtual_integrals=0,
        all_frequency_operator=False,uniform_temperature_operator=False,permission_to_propagate=False)
    write(REPAIR/'results/assessment.json',report)
    print(json.dumps(dict(state=report['state'],checks=len(checks),failed=len(failed),
        maxima={component:max(row['relative'] for row in records if row['component']==component) for component in COMPONENTS},
        full_node={component:max(row['relative'] for row in records if row['scope']=='full-node' and row['component']==component) for component in COMPONENTS},
        column_identities=identities)),flush=True)


if __name__=='__main__':
    source.modest()
    parser=argparse.ArgumentParser()
    parser.add_argument('phase',choices=['prepare','probe','build','freeze','assess'])
    args=parser.parse_args()
    {'prepare':prepare_repair,'probe':probe,'build':build,'freeze':freeze_repair,'assess':assess_repair}[args.phase]()
