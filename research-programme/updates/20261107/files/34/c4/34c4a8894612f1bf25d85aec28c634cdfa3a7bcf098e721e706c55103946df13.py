import csv
import itertools
import json
import math
import os
from datetime import datetime, timezone
from decimal import Decimal, localcontext
from pathlib import Path
from zoneinfo import ZoneInfo

for variable in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS'):
    os.environ[variable]='1'

import numpy as np
import psutil
from verify_remaining_real_pair import digest, read, require


ROOT = Path(__file__).resolve().parent
BANK = ROOT / 'final-epoch-kinematic-bank'
CAMPAIGN = ROOT / 'final-stable-real-batch-rays023-024'
PREDICTION = ROOT / 'REAL-PAIR-023-024-REFLECTION-PREDICTION.md'
LIMIT = 1e-10


def guard():
    require(not 3 <= datetime.now(ZoneInfo('Europe/London')).hour < 14
            and not any((folder/'STOP-REQUESTED').exists() for folder in (ROOT, ROOT.parent, BANK, CAMPAIGN))
            and not (ROOT.parent/'execution-v3/STOP-REQUEST.json').exists(), 'Compute hold')


def vector_difference(first, second, mode, suffix):
    modes = ('control','difference') if mode=='combined' else (mode,)
    terms = []
    for packet in (first,second):
        terms.append([packet[prefix+kernel+':'+suffix] for kernel in modes for prefix in ('total:','total_low:')])
    require(all(value.shape==(98,) and np.isfinite(value).all() for group in terms for value in group), 'Invalid projected vector')
    first_norm,second_norm = (math.hypot(*(math.fsum(column) for column in zip(*group,strict=True))) for group in terms)
    absolute = math.hypot(*(math.fsum([*left,*(-value for value in right)])
                              for left,right in zip(zip(*terms[0],strict=True),zip(*terms[1],strict=True),strict=True)))
    return absolute/max(first_norm,second_norm,1e-300)


def compare_pair(first_ray,second_ray,inputs):
    protocol = read(BANK/'protocol.json')
    angular = protocol['angular_nodes']
    first_node,second_node = angular[first_ray],angular[second_ray]
    require(first_node['ray']==first_ray and second_node['ray']==second_ray, 'Direction indices')
    first_direction,second_direction = first_node['direction'],second_node['direction']
    defect = math.dist([first_direction[0],-first_direction[1],first_direction[2]],second_direction)
    kernels = []
    for ray in (first_ray,second_ray):
        path = BANK/f'ray-{ray:03d}-kernel.json'
        cache = read(BANK/f'ray-{ray:03d}.json')
        require(cache['passed'] and digest(path)==cache['kernel_sha256'] and cache['protocol_sha256']==digest(BANK/'protocol.json'), 'Cache changed')
        inputs[str(path)] = cache['kernel_sha256']
        kernel = read(path)
        geometry = kernel['identity']
        require(Decimal(geometry['bath'][2][0])==0 and Decimal(geometry['recoil0'][1][0])==0, 'Not an in-plane event')
        require(all(Decimal(value)==0 for row_index,row in enumerate(geometry['transform']) for index,value in enumerate(row)
                    if (row_index==2)!=(index==2)), 'Frame transform does not commute with reflection')
        kernels.append(kernel)
    coefficient_errors = {}
    with localcontext() as context:
        context.prec = 110
        for key,first_values in kernels[0]['coefficients'].items():
            first = list(map(Decimal,first_values))
            second = list(map(Decimal,kernels[1]['coefficients'][key]))
            numerator = sum((left-right)**2 for left,right in zip(first,second,strict=True)).sqrt()
            scale = max(sum(value**2 for value in first).sqrt(),sum(value**2 for value in second).sqrt(),Decimal('1e-300'))
            coefficient_errors[key] = float(numerator/scale)
    rows = []
    for order in (18,26):
        guard()
        files = []
        for ray in (first_ray,second_ray):
            folder = ROOT/f'final-epoch-real-v2-ray{ray:03d}'/f'order-{order}'
            path,independent = folder/'complete.npz',read(folder/'independent.json')
            require(independent['passed'] and digest(path)==independent['complete_packet_sha256'], 'Unverified integral')
            files.append(path)
            inputs[str(path)] = independent['complete_packet_sha256']
        with np.load(files[0],allow_pickle=False) as first,np.load(files[1],allow_pickle=False) as second:
            cached_first,cached_second = {},{}
            for mode,join,degree,model,subdivision,component in itertools.product(('control','difference','combined'),(0,1),(0,1,2),
                        ('heavy','cold'),(1,2,4),('bank','candidate','bilinear_delta','equilibrium_delta')):
                suffix = f'join{join}:l{degree}:{model}-s{subdivision}:{component}'
                for kernel in (('control','difference') if mode=='combined' else (mode,)):
                    for prefix in ('total:','total_low:'):
                        key = prefix+kernel+':'+suffix
                        if key not in cached_first:
                            cached_first[key],cached_second[key] = first[key],second[key]
                relative = vector_difference(cached_first,cached_second,mode,suffix)
                rows.append(dict(pair=f'{first_ray}/{second_ray}',order=order,mode=mode,join=join,degree=degree,model=model,
                                 subdivision=subdivision,component=component,relative=relative,within_identity_gate=relative<=LIMIT))
    require(len(rows)==864, 'Incomplete projected-vector comparison')
    return dict(geometry_defect=defect,weight_difference=abs(first_node['weight']-second_node['weight']),
                polynomial_errors=coefficient_errors,
                orders={order:dict(maximum=max(row['relative'] for row in rows if row['order']==order),
                                   failures=sum(not row['within_identity_gate'] for row in rows if row['order']==order))
                        for order in (18,26)}),rows


if __name__=='__main__':
    process=psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([4])
    guard()
    require(read(CAMPAIGN/'integrity.json')['passed'],'Pair must first pass its ordinary independent checks')
    frozen = read(ROOT/'real-pair023-024-reflection-freeze.json')
    for path,checksum in frozen['inputs'].items():
        require(digest(path)==checksum,'Supplementary prediction or inputs changed')
    inputs=dict(frozen['inputs'])
    inputs[str(CAMPAIGN/'integrity.json')]=digest(CAMPAIGN/'integrity.json')
    mirror,rows = compare_pair(23,24,inputs)
    control,control_rows = compare_pair(22,23,inputs)
    passed = (mirror['geometry_defect']<=LIMIT and mirror['weight_difference']==0 and max(mirror['polynomial_errors'].values())<=LIMIT
              and all(item['failures']==0 for item in mirror['orders'].values())
              and control['geometry_defect']>LIMIT and control['weight_difference']==0
              and all(item['failures']>0 for item in control['orders'].values()))
    with (CAMPAIGN/'reflection-rows.csv').open('x',newline='',encoding='utf-8') as stream:
        writer=csv.DictWriter(stream,fieldnames=rows[0])
        writer.writeheader()
        writer.writerows(rows+control_rows)
    result=dict(passed=passed,finished=datetime.now(timezone.utc).isoformat(),gate=LIMIT,mirror=mirror,control=control,inputs=inputs,
                rows_sha256=digest(CAMPAIGN/'reflection-rows.csv'),process=dict(pid=process.pid,created_time=process.create_time()),
                scope='Supplementary single-event reflection check. Never a reclassification of production rows or substitution of uncalculated rays.')
    with (CAMPAIGN/'reflection.json').open('x',encoding='utf-8') as stream:
        json.dump(result,stream,indent=2,allow_nan=False)
    print(json.dumps({key:result[key] for key in ('passed','mirror','control')}))
    raise SystemExit(0 if passed else 1)
