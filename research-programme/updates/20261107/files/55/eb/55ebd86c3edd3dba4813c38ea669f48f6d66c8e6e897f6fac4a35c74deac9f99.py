from __future__ import annotations
import os
for variable in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[variable]='1'
import sys
sys.dont_write_bytecode=True
from pathlib import Path
from datetime import datetime,timezone
import argparse,hashlib,json,time,zipfile
ROOT=Path(__file__).resolve().parent
BRANCH=ROOT.parent
PARENT=BRANCH/'cold-microscopic-history-response-20261023'
HISTORIES=BRANCH/'farther-cold-operator-bridge-20261023'
REFERENCE=PARENT/'precision-representation'
PARENT_SHA='992d92b49c9a2d14f6e2951ccec3c1d6886fc75b173fdf5755524fb1a12344e4'
FREQUENCY=16.435070908264382
sys.path.insert(0,str(PARENT))
import source201 as prior
import repair201 as repaired
import cached201 as cached
import assess201 as metrics
np,mp,linear=prior.np,prior.mp,prior.linear
source,microscopic,saved=prior.source,prior.microscopic,prior.saved
read,write,packet,save,digest,check=prior.read,prior.write,prior.packet,prior.save,prior.digest,prior.check
combine=prior.combine
COMPONENTS=metrics.COMPONENTS
GRIDS=prior.GRIDS


def protocol():
    config=read(ROOT/'configuration.json')
    for name,value in config['protocol_hashes'].items():
        assert digest(ROOT/name)==value,name
    for name,value in config['implementation_hashes'].items():
        assert digest(name)==value,name
    return config


def setup():
    cached.install()
    return repaired.setup()


def prepare():
    assert not (ROOT/'configuration.json').exists()
    seal_path=PARENT/'results/stage-integrity.json'
    assert digest(seal_path)==PARENT_SHA
    seal=read(seal_path)
    assert seal['x14_qualified']
    inputs=dict(seal['consumed_and_immediate_rehashed'])
    inputs.update({str(PARENT/name):value for name,value in seal['file_hashes'].items()})
    inputs[str(seal_path)]=PARENT_SHA
    for name,value in inputs.items():
        assert digest(name)==value,name
    original,theta,prediction,actual=setup()
    previous=read(REFERENCE/'configuration.json')
    assert theta==previous['theta'] and previous['source_prediction_tolerance']==.01 and previous['identity_tolerance']==1e-10
    assert not read(REFERENCE/'results/source-assessment.json')['failed_checks']
    nodes=microscopic.event_common.nodes(theta,FREQUENCY)
    reference_nodes=read(PARENT/'configuration.json')['nodes']
    assert len(nodes)==len(reference_nodes)==36
    inventory=read(HISTORIES/'results/next-source-cache.json')
    loops=[]
    for index,node in enumerate(nodes):
        parameters,weight=source.physics.parameters_and_weight(theta,node)
        identity=source.physics.event_owner.inherited.virtual_identity(parameters)
        key=hashlib.sha256(json.dumps(identity,sort_keys=True).encode()).hexdigest()
        entry=next(row for row in inventory['records'] if row['frequency']==FREQUENCY and row['event']==index)
        assert entry['exact_virtual_cached'] and entry['identity_key']==key
        saved.register(inputs,entry['path'],entry['sha256'])
        data=read(entry['path'])
        assert data['identity']==identity and data['finite']
        loops.append(dict(path=entry['path'],sha256=entry['sha256'],identity_key=key,weight=weight))
    all_nodes=source.physics.integration_nodes(theta,7)
    panel=sorted({(node['frequency'],node['seed_weight']) for node in all_nodes})
    rows=[]
    check(rows,'original seven-node incoming weight sum is12',sum(weight for frequency,weight in panel)-12.,1e-13,'identity')
    check(rows,'seven distinct original incoming nodes',len(panel)-7,0,'integrity')
    check(rows,'new node has36 exact cached virtual inputs',len(loops)-36,0,'integrity')
    check(rows,'unchanged half-quarter history representation',int(prediction.high.shape!=(99,20) or actual.high.shape!=(99,12)),0,'integrity')
    assert all(node['seed_weight']==nodes[0]['seed_weight'] for node in nodes)
    assert all(node['seed_weight']==reference_nodes[0]['seed_weight'] for node in reference_nodes)
    for path in original.inputs:
        saved.register(inputs,path)
    implementation={}
    for module in list(sys.modules.values()):
        filename=getattr(module,'__file__',None)
        if filename and Path(filename).suffix=='.py' and Path(filename).resolve().is_relative_to(BRANCH) and not Path(filename).resolve().is_relative_to(ROOT):
            saved.register(inputs,filename)
            implementation[str(Path(filename).resolve())]=digest(filename)
    frozen_names=('source202.py','assess202.py','ACCEPTANCE.md','DERIVATION.md')
    bookmarks={str(path):digest(path) for path in (BRANCH/'RESUME-CURRENT.md',BRANCH.parent/'CURRENT_LOCAL_RESUME.md')}
    write(ROOT/'configuration.json',dict(stage=202,started_utc=datetime.now(timezone.utc).isoformat(),
        parent_sha256=PARENT_SHA,target_fraction=.90625,theta=theta,frequency=FREQUENCY,nodes=nodes,loops=loops,
        source_prediction_tolerance=.01,identity_tolerance=1e-10,
        prediction_groups=['photon-half','gas-half','photon-quarter','gas-quarter','zero'],
        actual_groups=['original','repaired-half','repaired-quarter'],
        original_panel=[dict(frequency=frequency,seed_weight=weight) for frequency,weight in panel],
        partial_panel=[dict(frequency=14.,seed_weight=reference_nodes[0]['seed_weight']),dict(frequency=FREQUENCY,seed_weight=nodes[0]['seed_weight'])],
        packets_already_frequency_weighted=True,frequency_weights_reapplied=False,partial_panel_normalized=False,
        protocol_hashes={name:digest(ROOT/name) for name in frozen_names},implementation_hashes=implementation,bookmarks=bookmarks))
    save(ROOT/'frozen/history-coefficients.npz',prediction_high=prediction.high,prediction_low=prediction.low,
        actual_high=actual.high,actual_low=actual.low)
    write(ROOT/'inputs.json',inputs)
    write(ROOT/'results/preparation.json',dict(checks=rows,failed_checks=[row for row in rows if not row['passed']]))
    with zipfile.ZipFile(ROOT/'results/resume-before.zip','w',compression=zipfile.ZIP_DEFLATED) as archive:
        for name,value in bookmarks.items():
            assert digest(name)==value
            archive.writestr(Path(name).name,Path(name).read_bytes())
    assert all(row['passed'] for row in rows)
    write(ROOT/'progress.json',dict(state='prepared',cached_virtual_inputs=36))
    print(json.dumps(dict(state='prepared',cached_virtual_inputs=36,inputs=len(inputs),partial_panel=read(ROOT/'configuration.json')['partial_panel'])),flush=True)


def verify_frozen():
    manifest=read(ROOT/'frozen/prediction-manifest.json')
    for name,value in manifest['files'].items():
        assert digest(ROOT/name)==value,name
    return manifest


def run(kind,seconds):
    config=protocol()
    assert not read(ROOT/'results/preparation.json')['failed_checks']
    if kind=='actual':
        verify_frozen()
    original,theta,prediction,actual=setup()
    representation=packet(ROOT/'frozen/history-coefficients.npz')
    for label,bundle in [('prediction',prediction),('actual',actual)]:
        assert np.array_equal(bundle.high,representation[label+'_high']) and np.array_equal(bundle.low,representation[label+'_low'])
    bundle=prediction if kind=='prediction' else actual
    source.physics.precise_state=repaired.precise_state
    began=time.monotonic()
    for index,node in enumerate(config['nodes']):
        path=ROOT/f'{kind}/event-{index:02d}.npz'
        if path.exists():
            record=read(path.with_suffix('.json'))
            assert digest(path)==record['sha256'] and not record['failed_checks']
            continue
        if time.monotonic()-began>=seconds:
            write(ROOT/'progress.json',dict(state='safe_restart',phase=kind,next_event=index));return
        started=datetime.now(timezone.utc).isoformat()
        start=time.monotonic()
        parameters,weight=source.physics.parameters_and_weight(theta,node)
        entry=config['loops'][index]
        assert weight==entry['weight'] and digest(entry['path'])==entry['sha256']
        loop=read(entry['path'])
        assert loop['identity']==source.physics.event_owner.inherited.virtual_identity(parameters)
        high,low,diagnostics=microscopic.weighted(parameters,bundle,cached.models(bundle),loop['scalar'],weight)
        checks=[]
        for name,value in diagnostics.items():
            check(checks,name,value,1e-10,'identity')
        check(checks,'finite',int(not np.isfinite(high+low).all()),0,'integrity')
        check(checks,'shape',int(high.shape!=low.shape or high.shape!=((5 if kind=='prediction' else 3),6,98,4)),0,'integrity')
        if kind=='prediction':
            check(checks,'zero history gives exactly zero source',np.max(abs(high[-1]))+np.max(abs(low[-1])),0,'identity')
        save(path,high=high,low=low,theta=theta,weight=weight,node=json.dumps(node,sort_keys=True))
        failed=[row for row in checks if not row['passed']]
        record=dict(checks=checks,failed_checks=failed,sha256=digest(path),loop_path=entry['path'],loop_sha256=entry['sha256'],
            started_utc=started,finished_utc=datetime.now(timezone.utc).isoformat(),seconds=time.monotonic()-start,new_virtual_integrals=0)
        write(path.with_suffix('.json'),record)
        write(ROOT/'progress.json',dict(state='evaluating',phase=kind,done=index+1,total=36))
        print(json.dumps(dict(phase=kind,event=index,seconds=record['seconds'],failed_checks=len(failed))),flush=True)
        assert not failed,failed
    write(ROOT/'progress.json',dict(state=kind+'_complete'))


def freeze():
    config=protocol()
    assert not (ROOT/'actual').exists() and not (ROOT/'frozen/prediction-manifest.json').exists()
    files={}
    predictions=[]
    for index in range(36):
        path=ROOT/f'prediction/event-{index:02d}.npz'
        record=read(path.with_suffix('.json'))
        assert digest(path)==record['sha256'] and not record['failed_checks']
        values=packet(path)
        pairs=[combine([(values['high'][2*grid],values['low'][2*grid]),(values['high'][2*grid+1],values['low'][2*grid+1])]) for grid in range(2)]
        predicted=(np.stack([value[0] for value in pairs]),np.stack([value[1] for value in pairs]))
        destination=ROOT/f'frozen/event-{index:02d}-prediction.npz'
        save(destination,high=predicted[0],low=predicted[1])
        predictions.append(predicted)
        for item in (path,path.with_suffix('.json'),destination):
            files[str(item.relative_to(ROOT))]=digest(item)
    neighbour=metrics.primitives(predictions)
    reference=packet(REFERENCE/'results/x14-source.npz')
    reference_prediction=(reference['prediction_high'],reference['prediction_low'])
    pair=metrics.primitives([reference_prediction,neighbour])
    for label,values in [('neighbour',neighbour),('two-frequency',pair)]:
        path=ROOT/f'frozen/{label}-prediction.npz'
        save(path,high=values[0],low=values[1])
        files[str(path.relative_to(ROOT))]=digest(path)
    for name in ('configuration.json','frozen/history-coefficients.npz'):
        files[name]=digest(ROOT/name)
    write(ROOT/'frozen/prediction-manifest.json',dict(files=files,frozen_utc=datetime.now(timezone.utc).isoformat(),
        new_predictions=36,reference_prediction_path=str(REFERENCE/'results/x14-source.npz'),
        reference_prediction_sha256=digest(REFERENCE/'results/x14-source.npz'),assessment_sha256=digest(ROOT/'assess202.py'),
        scopes=['neighbour','two-frequency'],frequency_weights_reapplied=False))
    write(ROOT/'progress.json',dict(state='predictions_frozen'))
    print('Neighbour and weighted-pair predictions frozen before absolute events.',flush=True)


if __name__=='__main__':
    source.modest()
    parser=argparse.ArgumentParser()
    parser.add_argument('phase',choices=['prepare','prediction','freeze','actual'])
    parser.add_argument('--seconds',type=float,default=5400)
    args=parser.parse_args()
    if args.phase=='prepare':prepare()
    elif args.phase=='freeze':freeze()
    else:run(args.phase,args.seconds)
