from __future__ import annotations
import os
for variable in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[variable]='1'
import sys
sys.dont_write_bytecode=True
from pathlib import Path
import argparse,json,time,hashlib,zipfile
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parent
BRANCH=ROOT.parent
PARENT=BRANCH/'history-aware-complete-band-temperature-test-20261025'
PARENT_SHA='b2cded71b9a6d1ab3fde3360c682f500c3fd830635f5c9fc935f2edf9fdd9738'
sys.path.insert(0,str(BRANCH/'history-aware-operator-temperature-test-20261025'))
import operator209 as owner
np,mp,linear=owner.np,owner.mp,owner.linear
source,cached,precise,metrics=owner.source,owner.cached,owner.precise,owner.metrics
read,write,packet,save,digest,check=owner.read,owner.write,owner.packet,owner.save,owner.digest,owner.check
COMPONENTS=owner.COMPONENTS
ACTIVE=list(range(96))+[98]


def now():
    return datetime.now(timezone.utc).isoformat()


def protocol():
    config=read(ROOT/'configuration.json')
    for name,value in config['protocol_hashes'].items():
        assert digest(ROOT/name)==value,name
    return config


class OperatorBundle(precise.Bundle):
    def __init__(self,features,inputs):
        columns=[]
        for index in ACTIVE+[None]:
            vector=[0.]*99
            if index is not None:
                vector[index]=1.
            columns.extend([vector,vector])
        super().__init__(features,columns,inputs)

    def apply(self,rows,join):
        values=np.asarray(rows,dtype=float)
        selected=values[...,ACTIVE]
        return np.concatenate([selected,np.zeros(values.shape[:-1]+(1,))],axis=-1)


def prepare():
    assert not (ROOT/'configuration.json').exists()
    seal_path=PARENT/'results/stage-integrity.json'
    assert digest(seal_path)==PARENT_SHA
    parent=read(seal_path)
    assert parent['full_original_8_20_panel_qualified']
    inputs=dict(parent['consumed_and_immediate_rehashed'])
    inputs.update({str(PARENT/name):value for name,value in parent['file_hashes'].items()})
    inputs[str(seal_path)]=PARENT_SHA
    for name,value in inputs.items():
        assert digest(name)==value,name
    previous=read(PARENT/'configuration.json')
    event=next(row for row in previous['target'] if row['event']==0 and row['frequency_index']==6)
    report_path=PARENT/'target/frequency-6/event-00.json'
    report=read(report_path)
    direct_path=report_path.with_suffix('.npz')
    assert digest(direct_path)==report['sha256'] and not report['failed_checks']
    loop_path=Path(report['loop_path'])
    assert digest(loop_path)==report['loop_sha256']
    original,theta=source.context(previous['target_fraction'])
    assert theta==previous['theta']==event['theta']
    parameters,weight=source.physics.parameters_and_weight(theta,event['node'])
    loop=read(loop_path)
    assert loop['finite'] and loop['identity']==source.physics.event_owner.inherited.virtual_identity(parameters)
    assert weight==event['weight']
    coefficients=packet(PARENT/'frozen/history-coefficients.npz')
    assert coefficients['high'].shape==coefficients['low'].shape==(99,12)
    assert np.max(abs(coefficients['high'][96:98]))+np.max(abs(coefficients['low'][96:98]))==0
    assert np.max(abs(coefficients['high'][:,-4:]))+np.max(abs(coefficients['low'][:,-4:]))==0
    for path in original.inputs:
        inputs[str(path)]=digest(path)
    implementation={}
    for module in list(sys.modules.values()):
        name=getattr(module,'__file__',None)
        if name and Path(name).suffix=='.py' and Path(name).resolve().is_relative_to(BRANCH) and not Path(name).resolve().is_relative_to(ROOT):
            path=Path(name).resolve()
            inputs[str(path)]=digest(path)
            implementation[str(path)]=digest(path)
    references=read(PARENT/'REFERENCE-PROVENANCE.json')['references']
    for entry in references:
        assert digest(entry['path'])==entry['sha256']
        inputs[entry['path']]=entry['sha256']
    bookmarks={str(path):digest(path) for path in (BRANCH/'RESUME-CURRENT.md',BRANCH.parent/'CURRENT_LOCAL_RESUME.md')}
    (ROOT/'results').mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(ROOT/'results/resume-before.zip','w',compression=zipfile.ZIP_DEFLATED) as archive:
        for path in bookmarks:
            archive.writestr(Path(path).name,Path(path).read_bytes())
    save(ROOT/'frozen/history-coefficients.npz',**coefficients)
    save(ROOT/'frozen/basis-metric.npz',mass=original.basis.mass,norms=original.basis.norms,mean=original.basis.mean)
    config=dict(stage=214,turn_start='2026-10-25T16:16:01+00:00',prepared_at=now(),
                target_fraction=previous['target_fraction'],theta=theta,event=event,
                parent_seal_path=str(seal_path),parent_seal_sha256=PARENT_SHA,
                direct_path=str(direct_path),direct_sha256=report['sha256'],loop_path=str(loop_path),
                loop_sha256=report['loop_sha256'],coefficients_sha256=digest(ROOT/'frozen/history-coefficients.npz'),
                basis_metric_sha256=digest(ROOT/'frozen/basis-metric.npz'),implementation=implementation,
                active_input_indices=ACTIVE,padded_input_count=98,matrix_shape=[6,98,97,2],
                identity_tolerance=1e-10,zero_tolerance=0,bookmarks=bookmarks,
                replay_not_holdout=True,original_bank_changed=False,grids_changed=False,tolerances_changed=False,
                protocol_hashes={name:digest(ROOT/name) for name in ('lift214.py','ACCEPTANCE.md','DERIVATION.md')})
    write(ROOT/'inputs.json',inputs)
    write(ROOT/'configuration.json',config)
    write(ROOT/'progress.json',dict(state='prepared',prepared_at=now()))
    print(json.dumps(dict(state='prepared',inputs=len(inputs),event=0,frequency=event['frequency'],columns=97)),flush=True)


def construct():
    config=protocol()
    assert not (ROOT/'results/operator.npz').exists()
    for name,value in config['implementation'].items():
        assert digest(name)==value,name
    original,theta=source.context(config['target_fraction'])
    features=cached.CachedFeatures(original)
    bundle=OperatorBundle(features,original.inputs)
    parameters,weight=source.physics.parameters_and_weight(theta,config['event']['node'])
    loop=read(config['loop_path'])
    assert digest(config['loop_path'])==config['loop_sha256']
    assert loop['identity']==source.physics.event_owner.inherited.virtual_identity(parameters)
    source.physics.precise_state=precise.precise_state
    evaluators=cached.models(bundle)
    started=now()
    began=time.monotonic()
    write(ROOT/'progress.json',dict(state='constructing',started_at=started,pid=os.getpid()))
    high,low,diagnostics=source.evaluate(parameters,bundle,evaluators,loop['scalar'])
    assert high.shape==low.shape==(6,98,196)
    high,low=source.precise_combine([(high,low)],[-weight])
    high=high.reshape(6,98,98,2)
    low=low.reshape(6,98,98,2)
    rows=[]
    for name,value in diagnostics.items():
        check(rows,name,value,1e-10,'identity')
    check(rows,'padded input exactly zero',np.max(abs(high[:,:,97]))+np.max(abs(low[:,:,97])),0,'negative_control')
    high,low=high[:,:,:97,:],low[:,:,:97,:]
    check(rows,'matrix finite',int(not np.isfinite(high+low).all()),0,'integrity')
    save(ROOT/'results/operator.npz',high=high,low=low,active=np.array(ACTIVE),theta=theta,weight=weight,components=np.array(COMPONENTS))
    import psutil
    memory=psutil.Process().memory_info()
    report=dict(started_at=started,finished_at=now(),seconds=time.monotonic()-began,checks=rows,
                failed_checks=[row for row in rows if not row['passed']],matrix_sha256=digest(ROOT/'results/operator.npz'),
                peak_working_set_bytes=getattr(memory,'peak_wset',memory.rss),
                matrix_bytes=high.nbytes+low.nbytes,new_virtual_integrals=0,
                implementation=config['implementation'],loop_path=config['loop_path'],loop_sha256=config['loop_sha256'])
    write(ROOT/'results/construction.json',report)
    write(ROOT/'progress.json',dict(state='matrix_constructed',finished_at=now()))
    print(json.dumps({key:report[key] for key in ('seconds','failed_checks','peak_working_set_bytes','matrix_bytes')}),flush=True)
    assert not report['failed_checks'],report['failed_checks']


def contract(high,low,coefficients,digits=80):
    predicted_high=np.zeros((6,98,coefficients['high'].shape[1]))
    predicted_low=np.zeros_like(predicted_high)
    with mp.workdps(digits):
        for join in range(2):
            columns=list(range(join,coefficients['high'].shape[1],2))
            vectors=[[mp.mpf(float(coefficients['high'][index,column]))+mp.mpf(float(coefficients['low'][index,column]))
                      for index in ACTIVE] for column in columns]
            for component,row in np.ndindex(6,98):
                terms=[mp.mpf(float(high[component,row,index,join]))+mp.mpf(float(low[component,row,index,join])) for index in range(97)]
                for column,vector in zip(columns,vectors):
                    value=mp.fsum(left*right for left,right in zip(terms,vector))
                    predicted_high[component,row,column]=float(value)
                    predicted_low[component,row,column]=float(value-mp.mpf(float(value)))
    output=[]
    for values in (predicted_high,predicted_low):
        output.append(np.moveaxis(values.reshape(6,98,3,4),2,0))
    return tuple(output)


def freeze():
    config=protocol()
    assert not (ROOT/'frozen/replay-manifest.json').exists()
    report=read(ROOT/'results/construction.json')
    assert not report['failed_checks']
    assert digest(ROOT/'results/operator.npz')==report['matrix_sha256']
    matrix=packet(ROOT/'results/operator.npz')
    coefficients=packet(ROOT/'frozen/history-coefficients.npz')
    assert digest(ROOT/'frozen/history-coefficients.npz')==config['coefficients_sha256']
    began=time.monotonic()
    prediction=contract(matrix['high'],matrix['low'],coefficients)
    save(ROOT/'frozen/replay-prediction.npz',high=prediction[0],low=prediction[1])
    paths=('results/operator.npz','frozen/history-coefficients.npz','frozen/basis-metric.npz','frozen/replay-prediction.npz')
    write(ROOT/'frozen/replay-manifest.json',dict(frozen_at=now(),files={name:digest(ROOT/name) for name in paths},
          configuration_sha256=digest(ROOT/'configuration.json'),replay_not_holdout=True,contraction_digits=80,seconds=time.monotonic()-began))
    write(ROOT/'progress.json',dict(state='replay_predictions_frozen',frozen_at=now()))
    print(json.dumps(dict(state='replay_predictions_frozen',seconds=time.monotonic()-began)),flush=True)


def assess():
    config=protocol()
    assert not (ROOT/'results/assessment.json').exists()
    manifest=read(ROOT/'frozen/replay-manifest.json')
    assert digest(ROOT/'configuration.json')==manifest['configuration_sha256']
    for name,value in manifest['files'].items():
        assert digest(ROOT/name)==value,name
    assert digest(config['direct_path'])==config['direct_sha256']
    direct=packet(config['direct_path'])
    predicted=packet(ROOT/'frozen/replay-prediction.npz')
    matrix=packet(ROOT/'results/operator.npz')
    coefficients=packet(ROOT/'frozen/history-coefficients.npz')
    basis=packet(ROOT/'frozen/basis-metric.npz')
    factor=linear.cholesky(basis['mass'],lower=True)
    rows=list(read(ROOT/'results/construction.json')['checks'])
    records=[]
    difference=metrics.subtract((predicted['high'],predicted['low']),(direct['high'],direct['low']))
    for name,measure in [('photon',lambda values:metrics.norms(values,factor)),('gas',lambda values:abs(values[...,-1,:]))]:
        relative=measure(difference[0][:2]+difference[1][:2])/np.maximum(measure(direct['high'][:2]+direct['low'][:2]),1e-300)
        for grid,component,column in np.ndindex(relative.shape):
            value=float(relative[grid,component,column])
            record=dict(grid=('half','quarter')[grid],component=COMPONENTS[component],background=('heavy','cold')[column//2],
                        join=column%2,measure=name,relative=value)
            records.append(record)
            check(rows,f'replay:{grid}:{component}:{column}:{name}',value,1e-10,'representation')
    check(rows,'zero history replay exactly zero',np.max(abs(predicted['high'][-1]))+np.max(abs(predicted['low'][-1])),0,'negative_control')
    identities=[]
    with mp.workdps(80):
        norm0,norm1=[mp.mpf(float(value)) for value in basis['norms'][:2]]
        mean=mp.mpf(float(basis['mean']))
        for component,index,join in np.ndindex(6,97,2):
            values={row:mp.mpf(float(matrix['high'][component,row,index,join]))+mp.mpf(float(matrix['low'][component,row,index,join])) for row in (0,1,2,97)}
            moment_terms=[values[0],-mean*norm0*values[1],-norm1*values[2]]
            moment=float(abs(mp.fsum(moment_terms))/max(sum(abs(value) for value in moment_terms),mp.mpf('1e-300')))
            exchange=float(abs(values[0]+values[97])/max(abs(values[0]),abs(values[97]),mp.mpf('1e-300')))
            identities.append(dict(component=COMPONENTS[component],input=index,join=join,moment=moment,exchange=exchange))
        for component in range(6):
            selected=[row for row in identities if row['component']==COMPONENTS[component]]
            for name in ('moment','exchange'):
                check(rows,f'columnwise {COMPONENTS[component]}:{name}',max(row[name] for row in selected),1e-10,'identity')
    values=matrix['high']+matrix['low']
    inverse_transpose=linear.solve_triangular(factor.T,np.eye(96),lower=False)
    bounds=[]
    for component,join in np.ndindex(6,2):
        photon=values[component,1:97,:96,join]
        gas_photon=values[component,97,:96,join]
        photon_gas=values[component,1:97,96,join]
        gas_gas=values[component,97,96,join]
        transformed=linear.solve_triangular(factor,photon@inverse_transpose,lower=True)
        gamma_gamma=float(linear.svdvals(transformed)[0])
        gamma_gas=float(np.linalg.norm(linear.solve_triangular(factor,photon_gas,lower=True)))
        gas_gamma=float(np.linalg.norm(gas_photon@inverse_transpose))
        gas_gas=float(abs(gas_gas))
        bounds.append(dict(component=COMPONENTS[component],join=join,photon_to_photon=gamma_gamma,
                           gas_to_photon=gamma_gas,photon_to_gas=gas_gamma,gas_to_gas=gas_gas,
                           numerical_matrix_norms_not_interval_enclosures=True))
        for background in range(2):
            half=2*background+join
            quarter=4+half
            delta=(coefficients['high'][:,half]-coefficients['high'][:,quarter])+(coefficients['low'][:,half]-coefficients['low'][:,quarter])
            photon_norm=np.linalg.norm(factor.T@delta[:96])
            gas_norm=abs(delta[98])
            output=values[component,:,:,join]@delta[ACTIVE]
            measured_photon=np.linalg.norm(linear.solve_triangular(factor,output[1:97],lower=True))
            measured_gas=abs(output[97])
            for name,actual,bound in [('photon',measured_photon,gamma_gamma*photon_norm+gamma_gas*gas_norm),
                                      ('gas',measured_gas,gas_gamma*photon_norm+gas_gas*gas_norm)]:
                check(rows,f'block bound {component}:{join}:{background}:{name}',max(0.,actual-bound)/max(bound,1e-300),1e-10,'bound')
    failed=[row for row in rows if not row['passed']]
    result=dict(stage=214,state='representation_rejected' if failed else 'single_event_operator_qualified',
                qualified=not failed,checks=rows,failed_checks=failed,records=records,column_identities=identities,norm_blocks=bounds,
                coverage='one existing event, 97 active repair inputs, two infrared joins',replay_not_holdout=True,
                full_frequency_operator=False,uniform_temperature_operator=False,permission_to_propagate=False)
    write(ROOT/'results/assessment.json',result)
    write(ROOT/'progress.json',dict(state=result['state'],finished_at=now()))
    print(json.dumps(dict(state=result['state'],checks=len(rows),failed=len(failed),
                maxima={component:max(row['relative'] for row in records if row['component']==component) for component in COMPONENTS},
                column_moment_max=max(row['moment'] for row in identities),column_exchange_max=max(row['exchange'] for row in identities))),flush=True)


if __name__=='__main__':
    source.modest()
    parser=argparse.ArgumentParser()
    parser.add_argument('phase',choices=['prepare','construct','freeze','assess'])
    args=parser.parse_args()
    {'prepare':prepare,'construct':construct,'freeze':freeze,'assess':assess}[args.phase]()
