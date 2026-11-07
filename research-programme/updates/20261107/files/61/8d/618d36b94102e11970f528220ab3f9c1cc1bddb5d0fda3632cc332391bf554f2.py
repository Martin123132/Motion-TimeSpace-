import argparse
import hashlib
import inspect
import math
import sys
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

import psutil
import run_stable_absorption_pair as stable
import run_final_real_directions as original
import verify_stable_real_pair_003_004 as retained


ROOT = Path(__file__).resolve().parent
read, digest, verify = original.read, original.digest, original.verify
require, write = stable.require, stable.write
STABLE_HASH = 'c8a7b53df118e23fcae5c74ab6346869a16bfec2e1125b9ac0a813a71dfd6d3a'
CHECK_HASH = '249942eec79ad3828d9ab9141f621a40dc277d785f2a9a4cd4397d6398b994ef'
REPAIR = ROOT/'legacy-stable-reconciliation-rays000-002'
REPAIR_HASH = 'a3f9693f2bc857a00d7e91f0ef76f565e58f6d914b4665cb4e26d39e5b38758f'
REFLECT_HASH = '34c4a8894612f1bf25d85aec28c634cdfa3a7bcf098e721e706c55103946df13'


def locations(first):
    require(first in range(27,126,2), 'Expected an untouched regular pair, not the final singleton')
    tag=f'{first:03d}-{first+1:03d}'
    return ROOT/f'final-stable-real-batch-rays{tag}', ROOT/f'real-pair{tag}-preflight.json', ROOT/f'real-pair{tag}-reflection-freeze.json'


def guard(first,stop):
    folder,_,_=locations(first)
    now=datetime.now(timezone.utc)
    require(now<stop and not 3<=now.astimezone(ZoneInfo('Europe/London')).hour<14,'Time or Music Lab hold')
    require(not any((directory/'STOP-REQUESTED').exists() for directory in
            (folder,ROOT,ROOT.parent,ROOT/'saved-epoch-cell450',ROOT/'final-epoch-kinematic-bank'))
            and not (ROOT.parent/'execution-v3/STOP-REQUEST.json').exists(),'Active compute hold')


def verify_result(first):
    campaign,preflight_path,_=locations(first)
    preflight=read(preflight_path)
    verify(preflight['inputs']);verify(preflight['preserved_inputs'])
    require(digest(retained.__file__)==CHECK_HASH and digest(REPAIR/'integrity.json')==REPAIR_HASH,'Changed acceptance base')
    source=inspect.getsource(retained.validate)
    changes=[
        ("== protocol['rays'] == [3, 4]",f"== protocol['rays'] == [{first}, {first+1}]"),
        ("required_raw | {Path(path) for path in previous} == {Path(path) for path in protocol['protected']}",
         "(required_raw | {Path(path) for path in previous}) <= {Path(path) for path in pair_prior} and pair_prior == protocol['protected']"),
        ("read(CAMPAIGN / 'verified-panel036.json')","read(ROOT/'final-stable-real-batch-rays003-004/verified-panel036.json')"),
        ("for ray in (3, 4):",f"for ray in ({first}, {first+1}):"),
        ("(f'final-epoch-real-source-ray{ray:03d}' if ray < 3 else f'final-epoch-real-v2-ray{ray:03d}')) for ray in range(5)",
         f"f'final-epoch-real-v2-ray{{ray:03d}}') for ray in range({first+2})"),
        ("prefix_reused=35, recalculated_panels=129","prefix_reused=0, recalculated_panels=164"),
        ("rays 0–2 retained under original arithmetic pending common-representation comparison.",
         "rays 0–2 use their independently verified stable reconciliation.")
    ]
    for before,after in changes:
        require(source.count(before)==1,'Changed verifier boundary: '+before)
        source=source.replace(before,after)
    context=dict(retained.__dict__,ROOT=ROOT,CAMPAIGN=campaign,pair_prior=preflight['preserved_inputs'])
    exec(compile(source,retained.__file__,'exec'),context)
    result=context['validate']()
    result.update(preflight_sha256=digest(preflight_path),verifier_sha256=digest(__file__),
                  prior_common_sha256=preflight['prior_common_sha256'],reconciliation_sha256=REPAIR_HASH)
    return result


def forecast(first,path,inputs):
    bank=ROOT/'final-epoch-kinematic-bank'
    nodes=read(bank/'protocol.json')['angular_nodes']
    mirrors=[]; controls=[]; pending=[]
    for ray in (first,first+1):
        node=nodes[ray]
        reflected=[node['direction'][0],-node['direction'][1],node['direction'][2]]
        candidates=[item['ray'] for item in nodes if item['weight']==node['weight']
                    and item['ray']!=ray and math.dist(item['direction'],reflected)<=1e-10]
        require(len(candidates)==1,'Expected one actual reflected node')
        partner=candidates[0]
        if partner>first+1:
            pending.append([ray,partner]);continue
        if [partner,ray] not in mirrors:
            mirrors.append([ray,partner])
    for ray,partner in mirrors:
        candidates=[other for other in range(first+2) if other not in (ray,partner) and nodes[other]['weight']==nodes[ray]['weight']]
        require(candidates,'Missing same-weight negative control')
        other=next((other_pair[1] for other_pair in mirrors if other_pair[0]!=ray and other_pair[1] in candidates),candidates[0])
        controls.append([ray,other])
    frozen={str(bank/'protocol.json'):digest(bank/'protocol.json'),
            str(ROOT/'check_real_pair_023_024_reflection.py'):REFLECT_HASH,str(Path(__file__)):digest(__file__)}
    for ray in sorted({first,first+1}|{partner for _,partner in mirrors+controls}):
        kernel=bank/f'ray-{ray:03d}-kernel.json'
        frozen[str(kernel)]=digest(kernel)
        if ray<first:
            for order in (18,26):
                packet=ROOT/f'final-epoch-real-v2-ray{ray:03d}'/f'order-{order}'/'complete.npz'
                require(str(packet) in inputs,'Partner not bound to prior common map')
                frozen[str(packet)]=inputs[str(packet)]
    verify(frozen)
    write(path,dict(frozen_at=datetime.now(timezone.utc).isoformat(),mirrors=mirrors,controls=controls,pending=pending,
                    gate=1e-10,orders=[18,26],inputs=frozen,candidate_outputs_present=False,
                    prediction='Equal reflected signed source vectors in every projected group at both orders; wrong partners differ. Independently calculate all new directions.'))


def prepare(first,stop,prior_sha):
    guard(first,stop)
    campaign,preflight,prediction=locations(first)
    require(not any(path.exists() for path in (campaign,preflight,prediction)),'Existing pair state: inspect before proceeding')
    prior=ROOT/f'final-stable-real-batch-rays{first-2:03d}-{first-1:03d}'
    common_file=prior/'common-coverage.json'
    require(digest(common_file)==prior_sha and digest(REPAIR/'integrity.json')==REPAIR_HASH,'Prior common map changed')
    common=read(common_file)
    require(common['passed'] and common['through']==first-1 and common['legacy_source_receipt_sha256']==REPAIR_HASH
            and sorted(map(int,common['directions']))==list(range(first)),'Prior coverage or representation differs')
    require(digest(prior/'integrity.json')==common['latest_production_sha256'] and read(prior/'integrity.json')['passed'], 'Prior production receipt')
    prior_reflection=read(prior/'reflection.json')
    require(prior_reflection['passed'] and prior_reflection['rows_sha256']==digest(prior/'reflection-rows.csv'),'Prior reflection evidence differs')
    require(digest(stable.__file__)==STABLE_HASH,'Changed stable evaluator')
    verify({ROOT/name:value for name,value in {**stable.FROZEN,**original.PARENTS}.items()})
    protected=dict(read(prior/'protocol.json')['protected'])
    protected.update(read(REPAIR/'protocol.json')['protected'])
    for folder,names in ((REPAIR,('protocol.json','end.json','integrity.json','legacy-to-stable.csv','reconciled-mirrors.csv')),
                         (prior,('protocol.json','end.json','integrity.json','common-coverage.json','reflection.json','reflection-rows.csv'))):
        for name in names:
            protected[str(folder/name)]=digest(folder/name)
    for index,row in common['directions'].items():
        ray=int(index);folder=ROOT/f'final-epoch-real-v2-ray{ray:03d}'
        require(Path(row['directory']).resolve()==folder.resolve(),'Common map reverted to a legacy path')
        protected.update({str(folder/name):value for name,value in row['files'].items()})
        protected[str(Path(row['acceptance']))]=row['acceptance_sha256']
    for index,(path,value) in enumerate(protected.items()):
        if index%32==0:
            guard(first,stop)
        require(digest(path)==value.lower(),'Changed protected input: '+path)
    inputs={str(Path(__file__)):digest(__file__),str(Path(stable.__file__)):STABLE_HASH,str(Path(retained.__file__)):CHECK_HASH,
            str(ROOT/'check_real_pair_023_024_reflection.py'):REFLECT_HASH,str(common_file):prior_sha,str(REPAIR/'integrity.json'):REPAIR_HASH}
    bank=ROOT/'final-epoch-kinematic-bank'
    inputs[str(bank/'protocol.json')]=digest(bank/'protocol.json')
    compiled=[]
    for ray in (first,first+1):
        for prefix in ('compensated-epoch-source-final450-ray','final-absorption-native-v2-ray','final-epoch-real-v2-ray'):
            require(not (ROOT/f'{prefix}{ray:03d}').exists(),'Existing candidate artifacts; do not automatically retry')
        cache_path=bank/f'ray-{ray:03d}.json';cache=read(cache_path)
        require(cache['passed'] and cache['ray']==ray and cache['protocol_sha256']==inputs[str(bank/'protocol.json')]
                and all(item['passed'] for item in cache['checks']),'Matching cache required')
        inputs[str(cache_path)]=digest(cache_path);inputs[str(bank/f'ray-{ray:03d}-kernel.json')]=cache['kernel_sha256']
        for stage in ('precise','native','freeze','run','check','compare'):
            source,meta=(original.render if stage=='precise' else stable.render)(stage,ray)
            compile(source,f'<{stage} ray{ray}>','exec')
            compiled.append(dict(ray=ray,stage=stage,sha256=hashlib.sha256(source.encode()).hexdigest()))
    verify(inputs)
    forecast(first,prediction,protected)
    inputs[str(prediction)]=digest(prediction)
    write(preflight,dict(passed=True,rays=[first,first+1],prepared=datetime.now(timezone.utc).isoformat(),
          inputs=inputs,preserved_inputs=protected,compiled=compiled,prior_common_sha256=prior_sha,prior_coverage=first,
          numerical_work_started=False,process=dict(pid=psutil.Process().pid,created_time=psutil.Process().create_time())))
    print(f'Preflight: {len(protected)} earlier files, {len(compiled)} compiled stages; frozen mirrors {read(prediction)["mirrors"]}.')


def launch(first):
    _,preflight,_=locations(first)
    record=read(preflight)
    require(record['passed'] and record['rays']==[first,first+1] and len(record['compiled'])==12,'Preflight required')
    verify(record['inputs'])
    require(digest(stable.__file__)==STABLE_HASH,'Stable supervisor changed')
    source=Path(stable.__file__).read_text()
    changes=[
        ("read,digest,verify=original.read,original.digest,original.verify","read,digest,verify=original.read,original.digest,original.verify\nFROZEN.update(pair_extra_frozen)"),
        ("    protected=dict(original_protocol['preserved_inputs'])","    protected=dict(original_protocol['preserved_inputs'])\n    protected.update(read(pair_preflight)['preserved_inputs'])"),
        ("    arguments,remainder=parser.parse_known_args();rays=[arguments.first,arguments.first+1]",
         "    arguments,remainder=parser.parse_known_args();rays=[arguments.first,arguments.first+1]\n    require(rays==read(pair_preflight)['rays'],'Pair scope mismatch')")
    ]
    for before,after in changes:
        require(source.count(before)==1,'Changed launch boundary')
        source=source.replace(before,after)
    context=dict(__file__=str(Path(__file__)),__name__='__main__',pair_preflight=preflight,
                 pair_extra_frozen={Path(stable.__file__).name:STABLE_HASH,preflight.name:digest(preflight)})
    exec(compile(source,stable.__file__,'exec'),context)


def reflect(first):
    import csv
    import check_real_pair_023_024_reflection as method
    campaign,_,freeze=locations(first)
    method.CAMPAIGN=campaign;method.guard()
    require(digest(method.__file__)==REFLECT_HASH and read(campaign/'integrity.json')['passed'],'Qualified comparator/production required')
    prediction=read(freeze);verify(prediction['inputs'])
    inputs=dict(prediction['inputs']);inputs[str(campaign/'integrity.json')]=digest(campaign/'integrity.json')
    results={'mirrors':[],'controls':[]};rows=[]
    for role,pairs in results.items():
        for ray,partner in prediction[role]:
            method.guard()
            comparison,detail=method.compare_pair(ray,partner,inputs)
            matched=(comparison['weight_difference']==0 and comparison['geometry_defect']<=method.LIMIT and
                     max(comparison['polynomial_errors'].values())<=method.LIMIT and all(value['failures']==0 for value in comparison['orders'].values()))
            different=(comparison['weight_difference']==0 and comparison['geometry_defect']>method.LIMIT
                       and all(value['failures']>0 for value in comparison['orders'].values()))
            pairs.append(dict(rays=[ray,partner],passed=matched if role=='mirrors' else different,**comparison))
            rows.extend(dict(role=role,**row) for row in detail)
    require(len(rows)==864*(len(prediction['mirrors'])+len(prediction['controls'])),'Missing vector comparisons')
    with (campaign/'reflection-rows.csv').open('x',newline='',encoding='utf-8') as stream:
        writer=csv.DictWriter(stream,fieldnames=('role','pair','order','mode','join','degree','model','subdivision','component','relative','within_identity_gate'))
        writer.writeheader();writer.writerows(rows)
    passed=all(item['passed'] for group in results.values() for item in group)
    write(campaign/'reflection.json',dict(passed=passed,completed_comparisons=len(rows),pending=prediction['pending'],
          tested=bool(rows),finished=datetime.now(timezone.utc).isoformat(),gate=method.LIMIT,**results,inputs=inputs,
          prediction_sha256=digest(freeze),rows_sha256=digest(campaign/'reflection-rows.csv')))
    print(f'Reflection: {len(rows)} comparisons; pending partners {prediction["pending"]}; passed={passed}.')
    require(passed,'Frozen supplementary reflection prediction failed')


if __name__=='__main__':
    parser=argparse.ArgumentParser(add_help=False)
    parser.add_argument('stage');parser.add_argument('--first',type=int,required=True);parser.add_argument('--stop-utc',required=True)
    parser.add_argument('--common-sha')
    options,extra=parser.parse_known_args()
    first=options.first
    campaign,preflight,freeze=locations(first)
    stop=datetime.fromisoformat(options.stop_utc.replace('Z','+00:00'))
    require(stop.tzinfo is not None and stop.utcoffset().total_seconds()==0,'Explicit UTC cutoff')
    process=psutil.Process();process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS);process.cpu_affinity([4])
    guard(first,stop)
    if options.stage=='prepare':
        require(not extra and options.common_sha and len(options.common_sha)==64,'Explicit parent coverage fingerprint required')
        prepare(first,stop,options.common_sha.lower())
    elif options.stage=='verify':
        require(not extra,'Unexpected verifier arguments')
        result=verify_result(first)
        write(campaign/'integrity.json',result)
        print(json.dumps({key:result[key] for key in ('passed','actual_child_exits','verified_files','rays')}))
    elif options.stage=='reflect':
        require(not extra,'Unexpected diagnostic arguments')
        reflect(first)
    else:
        require(options.stage in ('batch','native','freeze','run','check','compare') and options.common_sha is None,'Unrecognized worker mode')
        launch(first)
