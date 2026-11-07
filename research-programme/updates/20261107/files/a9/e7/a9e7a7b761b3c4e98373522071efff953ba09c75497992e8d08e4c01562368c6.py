import csv
import inspect
import json
import math
from datetime import datetime, timezone
from pathlib import Path

import reconcile_legacy_real_sources as job
import check_real_pair_023_024_reflection as reflection
import verify_stable_real_pair_003_004 as retained
import numpy as np
import psutil


ROOT,CAMPAIGN=job.ROOT,job.CAMPAIGN
require,read,digest=job.require,job.read,job.digest


def validate_common():
    parent=ROOT/'verify_stable_real_pair_003_004.py'
    require(digest(parent)==job.fixed()[str(parent)],'Changed retained verifier')
    source=inspect.getsource(retained.validate)
    changes=[
        ("== protocol['rays'] == [3, 4]", "== protocol['rays'] == [0, 1, 2]"),
        ("required_raw | {Path(path) for path in previous} == {Path(path) for path in protocol['protected']}",
         "(required_raw | {Path(path) for path in previous}) <= {Path(path) for path in protocol['protected']}"),
        ("read(CAMPAIGN / 'verified-panel036.json')", "read(ROOT/'final-stable-real-batch-rays003-004/verified-panel036.json')"),
        ("for ray in (3, 4):", "for ray in (0, 1, 2):"),
        ("source = ROOT / f'compensated-epoch-source-final450-ray{ray:03d}'",
         "source = ROOT / ('compensated-epoch-source-final450-001' if ray==0 else f'compensated-epoch-source-final450-ray{ray:03d}')"),
        ("        if ray == 3:", "        old = ROOT / f'final-epoch-real-source-ray{ray:03d}'\n        if ray in (0,1,2):"),
        ("prefix['order'] == 18 and not prefix['failed_panel_copied']", "prefix['orders'] == [18,26] and not prefix['affected_panels_copied']"),
        ("if ray == 3 and order == 18 and index < 35:", "if index < 35:"),
        ("(f'final-epoch-real-source-ray{ray:03d}' if ray < 3 else f'final-epoch-real-v2-ray{ray:03d}')) for ray in range(5)",
         "f'final-epoch-real-v2-ray{ray:03d}') for ray in range(27)"),
        ("prefix_reused=35, recalculated_panels=129", "prefix_reused=210, recalculated_panels=36"),
        ("rays 0–2 retained under original arithmetic pending common-representation comparison.",
         "rays 0–2 replayed with common stable arithmetic; prior originals remain immutable."),
    ]
    for before,after in changes:
        require(source.count(before)==1,'Verifier adaptation boundary changed: '+before)
        source=source.replace(before,after)
    context=dict(retained.__dict__,ROOT=ROOT,CAMPAIGN=CAMPAIGN)
    exec(compile(source,str(parent),'exec'),context)
    return context['validate']()


def audit_replay(ray,order):
    old,new,_,_=job.homes(ray)
    original,updated=old/f'order-{order}',new/f'order-{order}'
    receipt=read(updated/'original-replay.json')
    rows=receipt['rows']
    require(receipt['passed'] and len(rows)==72 and {(row['panel'],row['key']) for row in rows}==
            {(index,f'{mode}:join{join}:l{degree}:actions') for index in range(35,41) for mode in ('control','difference')
             for join in (0,1) for degree in (0,1,2)}, 'Missing signed action replays')
    require(all(row['bitwise_original'] and (row['panel'] in (35,36) or row['changed_values']==0) for row in rows),'Changed unaffected action')
    counts=[]
    for index in range(35,41):
        reflection.guard()
        with np.load(original/f'panel-{index:03d}.npz',allow_pickle=False) as before,np.load(updated/f'panel-{index:03d}.npz',allow_pickle=False) as after:
            points=sorted(key for key in before.files if key.startswith('point:'))
            require(points==sorted(key for key in after.files if key.startswith('point:')),'Point coverage mismatch')
            count=0
            for key in points:
                first,second=before[key],after[key]
                require(first.dtype==second.dtype==np.float64 and first.shape==second.shape and np.isfinite(second).all(),'Panel shape/units')
                count+=np.count_nonzero(first.view(np.uint64)!=second.view(np.uint64))
            require(index in (35,36) or not count,'Unchanged tail point values differ')
            counts.append(dict(index=index,changed_point_entries=int(count)))
    radial=read(new/'order18-vs26.json')['rows']
    results=[]
    with np.load(original/'complete.npz',allow_pickle=False) as before,np.load(updated/'complete.npz',allow_pickle=False) as after:
        cached_first,cached_second={},{}
        for row in radial:
            suffix=f"join{row['join']}:l{row['degree']}:{row['model']}-s{row['subdivision']}:{row['component']}"
            mode=row['mode']
            for kernel in (('control','difference') if mode=='combined' else (mode,)):
                for prefix in ('total:','total_low:'):
                    key=prefix+kernel+':'+suffix
                    if key not in cached_first:
                        cached_first[key],cached_second[key]=before[key],after[key]
            relative=reflection.vector_difference(cached_first,cached_second,mode,suffix)
            require(math.isfinite(relative),'Nonfinite original-vs-repaired result')
            results.append(dict(ray=ray,order=order,mode=mode,join=row['join'],degree=row['degree'],model=row['model'],
                                subdivision=row['subdivision'],component=row['component'],relative=relative))
    return dict(ray=ray,order=order,checked_action_arrays=len(rows),point_changes=counts,receipt_sha256=digest(updated/'original-replay.json'),
                above_identity=sum(row['relative']>1e-10 for row in results),above_refinement=sum(row['relative']>.002 for row in results),
                maximum=max(row['relative'] for row in results)),results


def main():
    reflection.CAMPAIGN=CAMPAIGN
    reflection.guard()
    verify=validate_common()
    require(verify['passed'] and set(verify['coverage'])==set(range(27)),'Incorrect repaired coverage')
    audit,rows=[],[]
    for ray in job.RAYS:
        for order in job.ORDERS:
            item,detail=audit_replay(ray,order)
            audit.append(item); rows.extend(detail)
    require(len(rows)==2592,'Original-vs-repaired row coverage')
    with (CAMPAIGN/'legacy-to-stable.csv').open('x',newline='',encoding='utf-8') as stream:
        writer=csv.DictWriter(stream,fieldnames=rows[0])
        writer.writeheader();writer.writerows(rows)
    mirrors,controls,angular_rows=[],[],[]
    inputs={str(CAMPAIGN/'protocol.json'):digest(CAMPAIGN/'protocol.json')}
    for role,pairs in [('mirror',[(0,15),(1,14),(2,13)]),('control',[(0,14),(1,13),(2,15)])]:
        for ray,reference in pairs:
            reflection.guard()
            comparison,detail=reflection.compare_pair(ray,reference,inputs)
            compatible=(comparison['weight_difference']==0 and comparison['geometry_defect']<=1e-10 and
                        max(comparison['polynomial_errors'].values())<=1e-10 and all(value['failures']==0 for value in comparison['orders'].values()))
            distinct=(comparison['weight_difference']==0 and comparison['geometry_defect']>1e-10 and all(value['failures']>0 for value in comparison['orders'].values()))
            (mirrors if role=='mirror' else controls).append(dict(rays=[ray,reference],passed=compatible if role=='mirror' else distinct,**comparison))
            angular_rows.extend(dict(role=role,**row) for row in detail)
    require(len(angular_rows)==5184,'Angular diagnostic coverage')
    with (CAMPAIGN/'reconciled-mirrors.csv').open('x',newline='',encoding='utf-8') as stream:
        writer=csv.DictWriter(stream,fieldnames=angular_rows[0])
        writer.writeheader();writer.writerows(angular_rows)
    passed=all(not row['above_refinement'] for row in audit) and all(item['passed'] for item in mirrors+controls)
    verify.update(passed=passed,coverage_authoritative=passed,qualifying_prior_coverage=digest(job.CURRENT/'integrity.json'),
                  reconciliation=audit,mirrors=mirrors,negative_controls=controls,verified_comparison_inputs=inputs,
                  old_new_csv_sha256=digest(CAMPAIGN/'legacy-to-stable.csv'),mirrors_csv_sha256=digest(CAMPAIGN/'reconciled-mirrors.csv'),
                  completed_at=datetime.now(timezone.utc).isoformat(),new_angular_directions=0,
                  decision='common stable representation accepted' if passed else 'preserve results, do not promote; discrepancy requires review')
    job.write(CAMPAIGN/('integrity.json' if passed else 'review-required.json'),verify)
    print(json.dumps(dict(passed=passed,verified_files=verify['verified_files'],exits=verify['actual_child_exits'],maxima=audit,
                          mirror_max=max(value['maximum'] for item in mirrors for value in item['orders'].values()))))
    return 0 if passed else 1


if __name__=='__main__':
    process=psutil.Process();process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS);process.cpu_affinity([4])
    raise SystemExit(main())
