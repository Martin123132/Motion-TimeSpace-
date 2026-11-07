from common197 import *

def prepare():
    assert not (ROOT/'configuration.json').exists()
    inputs={}
    register(inputs,PARENT/'results/stage-integrity.json',SEAL)
    parent=read(PARENT/'results/stage-integrity.json')
    for name,value in parent['consumed_and_immediate_rehashed'].items():
        register(inputs,name,value)
    for name,value in parent['file_hashes'].items():
        register(inputs,PARENT/name,value)
    config=read(PARENT/'configuration.json')
    step=.25/2048
    exact=[.875-.01/config['expansion_span'],.875+.01/config['expansion_span']]
    limits=[.75+math.ceil((exact[0]-.75)/step)*step,.75+math.floor((exact[1]-.75)/step)*step]
    new=dict(stage=197,started_utc=datetime.now(timezone.utc).isoformat(),theta0=config['theta0'],
             expansion_span=config['expansion_span'],exact_tested_fraction=exact,interval=limits,
             covered_fraction_of_local_span=(limits[1]-limits[0])/(exact[1]-exact[0]),
             counts=[2048,4096],profiles=['quadratic','linear'],parent_seal_sha256=SEAL,
             labels=LABELS,source_prediction_tolerance=.01,identity_tolerance=1e-10,
             protocol_hashes={path.name:digest(path) for path in [*ROOT.glob('*.py'),ROOT/'ACCEPTANCE.md',ROOT/'DERIVATION.md']},
             bookmark_hashes={str(path):digest(path) for path in [BRANCH/'RESUME-CURRENT.md',BRANCH.parent/'CURRENT_LOCAL_RESUME.md']})
    write(ROOT/'configuration.json',new)
    write(ROOT/'inputs.json',inputs)
    write(ROOT/'progress.json',dict(state='prepared'))
    print(json.dumps(dict(state='prepared',interval=limits,coverage=new['covered_fraction_of_local_span'],inputs=len(inputs))),flush=True)

def assemble():
    config=frozen();inputs=read(ROOT/'inputs.json');checks=[]
    roots=[PARENT,*panel.REFERENCE_ROOTS]
    for tag in TAGS:
        destination=ROOT/f'sources/{tag}.npz'
        if destination.exists():
            status=read(destination.with_suffix('.json'))
            assert digest(destination)==status['sha256']
            checks.extend(status['checks']);continue
        original_high=[];original_low=[];repaired_high=[];repaired_low=[]
        for root in roots:
            local=read(register(inputs,root/'configuration.json'))
            for node in local['selected']:
                path=panel.event_path(root,tag,node)
                metadata=read(register(inputs,path.with_suffix('.json')))
                data=packet(register(inputs,path,metadata['sha256']))
                assert not metadata['failed_checks'] and data['high'].shape==(4,6,98,4)
                old=packet(register(inputs,metadata['original_event'],metadata['original_event_sha256']))
                assert old['high'].shape==(2,6,98,4)
                expected_theta=config['theta0']*math.exp(configured_offset(tag))
                assert abs(float(data['theta'])/expected_theta-1)<1e-12
                if 'theta' in old:
                    assert float(data['theta'])==float(old['theta'])
                repaired_high.append(data['high'][:,:4]);repaired_low.append(data['low'][:,:4])
                original_high.append(old['high'][0,:4]);original_low.append(old['low'][0,:4])
        assert len(original_high)==252
        old=parts_sum(np.array(original_high),np.array(original_low))
        repaired=parts_sum(np.array(repaired_high),np.array(repaired_low))
        versions_high=[old[0]];versions_low=[old[1]]
        for group in range(4):
            pair=parts_sum(np.stack([repaired[0][group],-old[0]]),np.stack([repaired[1][group],-old[1]]))
            versions_high.append(pair[0]);versions_low.append(pair[1])
        versions_high.append(repaired[0][3]);versions_low.append(repaired[1][3])
        high=np.empty((6,3,98,4));low=np.empty_like(high)
        for version in range(6):
            for kind,members in enumerate(([0],[1,2,3],[0,1,2,3])):
                pair=parts_sum(versions_high[version][members],versions_low[version][members])
                high[version,kind],low[version,kind]=pair
        local_checks=[]
        with localcontext() as context:
            context.prec=100
            for component,row,column in [(0,0,0),(0,2,2),(2,48,1),(3,97,3)]:
                exact=sum((Decimal.from_float(float(upper[component,row,column]))+
                           Decimal.from_float(float(lower[component,row,column]))
                           for upper,lower in zip(original_high,original_low)),Decimal(0))
                actual=Decimal.from_float(float(old[0][component,row,column]))+Decimal.from_float(float(old[1][component,row,column]))
                check(local_checks,f'{tag}:independent100digit:{component}:{row}:{column}',float(abs(actual-exact)/max(abs(exact),Decimal('1e-300'))),1e-10,'identity')
        reconstructed=high[0]+high[4]-high[5]+low[0]+low[4]-low[5]
        check(local_checks,tag+':original+delta=candidate',np.max(abs(reconstructed))/max(np.max(abs(high[5])),1e-300),1e-10,'identity')
        check(local_checks,tag+':all finite',int(not np.isfinite(high+low).all()),0,'integrity')
        save(destination,high=high,low=low,offset=configured_offset(tag),versions=np.array(VERSIONS),kinds=np.array(KINDS))
        write(destination.with_suffix('.json'),dict(sha256=digest(destination),checks=local_checks,event_count=252))
        checks.extend(local_checks);write(ROOT/'inputs.json',inputs)
        print(json.dumps(dict(assembled=tag,events=252)),flush=True)
    check(checks,'all five sites present',sum(not (ROOT/f'sources/{tag}.npz').exists() for tag in TAGS),0,'integrity')
    write(ROOT/'sources/status.json',dict(checks=checks,failed_checks=[row for row in checks if not row['passed']]))
    assert all(row['passed'] for row in checks)
    write(ROOT/'progress.json',dict(state='sources_assembled'))

def configured_offset(tag):
    return float(OFFSETS[TAGS.index(tag)])

if __name__=='__main__':
    if not (ROOT/'configuration.json').exists():
        prepare()
    assemble()
