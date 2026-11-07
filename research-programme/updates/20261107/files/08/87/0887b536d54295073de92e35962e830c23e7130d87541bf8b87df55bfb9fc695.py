from __future__ import annotations
import os
for variable in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[variable]='1'
import sys
sys.dont_write_bytecode=True
from pathlib import Path
from datetime import datetime,timezone
import argparse,hashlib,json,zipfile
ROOT=Path(__file__).resolve().parent
BRANCH=ROOT.parent
PARENT=BRANCH/'cold-fourth-frequency-source-20261024'
PARENT_SHA='e492e2a719fe4d2aa8ba05c750b68becf435e70d52fa5344dc096c9af34c97e1'
FREQUENCY=18.449187113596366
REFERENCE=PARENT/'results/four-frequency-source.npz'
sys.path.insert(0,str(PARENT))
import source204 as previous
runner=previous.runner
inherited_assessment=previous.inherited_assessment
np,mp,linear=runner.np,runner.mp,runner.linear
source,microscopic,saved=runner.source,runner.microscopic,runner.saved
read,write,packet,save,digest,check=runner.read,runner.write,runner.packet,runner.save,runner.digest,runner.check
combine,metrics,COMPONENTS,GRIDS=runner.combine,runner.metrics,runner.COMPONENTS,runner.GRIDS
HISTORIES=runner.HISTORIES
LEAVES=(*previous.LEAVES,PARENT/'results/neighbour-source.npz')
runner.ROOT=ROOT
runner.FREQUENCY=FREQUENCY


def protocol():
    return runner.protocol()


def leaf_frequency(path):
    values=packet(path)
    frequencies=np.atleast_1d(values['frequencies'] if 'frequencies' in values else values['frequency'])
    assert frequencies.shape==(1,),str(path)
    return float(frequencies[0])


def prepare():
    assert not (ROOT/'configuration.json').exists()
    seal_path=PARENT/'results/stage-integrity.json'
    assert digest(seal_path)==PARENT_SHA
    seal=read(seal_path)
    assert seal['neighbour_and_four_frequency_qualified'] and not seal['frequency_weights_reapplied']
    inputs=dict(seal['consumed_and_immediate_rehashed'])
    inputs.update({str(PARENT/name):value for name,value in seal['file_hashes'].items()})
    inputs[str(seal_path)]=PARENT_SHA
    for name,value in inputs.items():assert digest(name)==value,name
    parent_config=read(PARENT/'configuration.json')
    parent_report=read(PARENT/'results/source-assessment.json')
    assert parent_report['qualified'] and not parent_report['failed_checks']
    assert digest(REFERENCE)==parent_report['scopes']['four-frequency']['result_sha256']
    original,theta,prediction,actual=runner.setup()
    assert theta==parent_config['theta']
    assert parent_config['source_prediction_tolerance']==.01 and parent_config['identity_tolerance']==1e-10
    nodes=microscopic.event_common.nodes(theta,FREQUENCY)
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
    panel=sorted({(node['frequency'],node['seed_weight']) for node in all_nodes if 8.<node['frequency']<20.})
    partial=sorted([*parent_config['partial_panel'],dict(frequency=FREQUENCY,seed_weight=nodes[0]['seed_weight'])],key=lambda item:item['frequency'])
    rows=[]
    check(rows,'original seven-node weight sum12',sum(weight for frequency,weight in panel)-12.,1e-13,'identity')
    check(rows,'seven original incoming nodes',len(panel)-7,0,'integrity')
    check(rows,'five distinct partial-panel nodes',len({item['frequency'] for item in partial})-5,0,'integrity')
    check(rows,'36 exact cached virtual inputs',len(loops)-36,0,'integrity')
    check(rows,'selected frequencies retain original seed weights',int(not all((item['frequency'],item['seed_weight']) in panel for item in partial)),0,'integrity')
    check(rows,'saved leaves match reference frequencies',int(not np.array_equal(np.sort([leaf_frequency(path) for path in LEAVES]),packet(REFERENCE)['frequencies'])),0,'integrity')
    parent_history=packet(PARENT/'frozen/history-coefficients.npz')
    for label,bundle in [('prediction',prediction),('actual',actual)]:
        for part in ('high','low'):
            check(rows,label+':same history '+part,int(not np.array_equal(getattr(bundle,part),parent_history[label+'_'+part])),0,'integrity')
    assert all(node['seed_weight']==nodes[0]['seed_weight'] for node in nodes)
    assert np.array_equal(packet(REFERENCE)['frequencies'],np.array(seal['partial_panel_frequencies']))
    for path in original.inputs:saved.register(inputs,path)
    implementation={}
    for module in list(sys.modules.values()):
        name=getattr(module,'__file__',None)
        if name and Path(name).suffix=='.py' and Path(name).resolve().is_relative_to(BRANCH) and not Path(name).resolve().is_relative_to(ROOT):
            saved.register(inputs,name)
            implementation[str(Path(name).resolve())]=digest(name)
    bookmarks={str(path):digest(path) for path in (BRANCH/'RESUME-CURRENT.md',BRANCH.parent/'CURRENT_LOCAL_RESUME.md')}
    write(ROOT/'configuration.json',dict(stage=205,started_utc=datetime.now(timezone.utc).isoformat(),
        parent_sha256=PARENT_SHA,target_fraction=.90625,theta=theta,frequency=FREQUENCY,nodes=nodes,loops=loops,
        source_prediction_tolerance=.01,identity_tolerance=1e-10,
        prediction_groups=parent_config['prediction_groups'],actual_groups=parent_config['actual_groups'],
        original_panel=[dict(frequency=frequency,seed_weight=weight) for frequency,weight in panel],partial_panel=partial,
        packets_already_frequency_weighted=True,frequency_weights_reapplied=False,partial_panel_normalized=False,
        reference_path=str(REFERENCE),reference_sha256=digest(REFERENCE),
        protocol_hashes={name:digest(ROOT/name) for name in ('source205.py','assess205.py','ACCEPTANCE.md','DERIVATION.md')},
        implementation_hashes=implementation,bookmarks=bookmarks))
    save(ROOT/'frozen/history-coefficients.npz',prediction_high=prediction.high,prediction_low=prediction.low,actual_high=actual.high,actual_low=actual.low)
    write(ROOT/'inputs.json',inputs)
    write(ROOT/'results/preparation.json',dict(checks=rows,failed_checks=[row for row in rows if not row['passed']]))
    with zipfile.ZipFile(ROOT/'results/resume-before.zip','w',compression=zipfile.ZIP_DEFLATED) as archive:
        for name,value in bookmarks.items():
            assert digest(name)==value
            archive.writestr(Path(name).name,Path(name).read_bytes())
    assert all(row['passed'] for row in rows)
    write(ROOT/'progress.json',dict(state='prepared'))
    print(json.dumps(dict(state='prepared',inputs=len(inputs),partial_panel=partial)),flush=True)


def freeze():
    config=protocol()
    assert not (ROOT/'actual').exists() and not (ROOT/'frozen/prediction-manifest.json').exists()
    files={};predictions=[]
    for index in range(36):
        path=ROOT/f'prediction/event-{index:02d}.npz'
        record=read(path.with_suffix('.json'))
        assert digest(path)==record['sha256'] and not record['failed_checks']
        values=packet(path)
        pairs=[combine([(values['high'][2*grid],values['low'][2*grid]),(values['high'][2*grid+1],values['low'][2*grid+1])]) for grid in range(2)]
        predicted=(np.stack([pair[0] for pair in pairs]),np.stack([pair[1] for pair in pairs]))
        destination=ROOT/f'frozen/event-{index:02d}-prediction.npz'
        save(destination,high=predicted[0],low=predicted[1]);predictions.append(predicted)
        for item in (path,path.with_suffix('.json'),destination):files[str(item.relative_to(ROOT))]=digest(item)
    neighbour=metrics.primitives(predictions)
    assert digest(REFERENCE)==config['reference_sha256']
    reference=packet(REFERENCE)
    combined=metrics.primitives([(reference['prediction_high'],reference['prediction_low']),neighbour])
    for label,values in [('neighbour',neighbour),('five-frequency',combined)]:
        path=ROOT/f'frozen/{label}-prediction.npz'
        save(path,high=values[0],low=values[1]);files[str(path.relative_to(ROOT))]=digest(path)
    for name in ('configuration.json','frozen/history-coefficients.npz','results/adapter-validation.json'):
        files[name]=digest(ROOT/name)
    write(ROOT/'frozen/prediction-manifest.json',dict(files=files,frozen_utc=datetime.now(timezone.utc).isoformat(),
        new_predictions=36,reference_prediction_path=str(REFERENCE),reference_prediction_sha256=digest(REFERENCE),
        assessment_sha256=digest(ROOT/'assess205.py'),scopes=['neighbour','five-frequency'],frequency_weights_reapplied=False))
    write(ROOT/'progress.json',dict(state='predictions_frozen'))
    print('Neighbour and weighted five-node predictions frozen before absolute events.',flush=True)


if __name__=='__main__':
    source.modest()
    parser=argparse.ArgumentParser()
    parser.add_argument('phase',choices=['prepare','prediction','freeze','actual'])
    parser.add_argument('--seconds',type=float,default=6000)
    args=parser.parse_args()
    if args.phase=='prepare':prepare()
    elif args.phase=='freeze':freeze()
    else:
        assert not read(ROOT/'results/adapter-validation.json')['failed_checks']
        runner.run(args.phase,args.seconds)
