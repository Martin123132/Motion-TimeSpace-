from pathlib import Path
from datetime import datetime, timezone
import csv
import ctypes
import hashlib
import json
import os
import re


def main():
    for variable in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:
        os.environ[variable]='1'
    import numpy as np
    kernel=ctypes.windll.kernel32
    kernel.GetCurrentProcess.restype=ctypes.c_void_p
    kernel.SetProcessAffinityMask.argtypes=[ctypes.c_void_p,ctypes.c_size_t]
    kernel.SetPriorityClass.argtypes=[ctypes.c_void_p,ctypes.c_uint]
    if not kernel.SetProcessAffinityMask(kernel.GetCurrentProcess(),1<<4) or not kernel.SetPriorityClass(kernel.GetCurrentProcess(),0x4000):
        raise OSError('Resource cap failed')
    root=Path(__file__).resolve().parents[1]
    directory=root/'source-intake/navier-stokes/20260914'
    target=directory/'annular-P7-bisection-integrity-20261003.json'
    if target.exists():
        raise FileExistsError(target)
    hashes,mismatches,reports,authorities={},{}, {}, {}
    def verify(relative,expected=None):
        path=(root/relative).resolve()
        if path==root/'CURRENT_LOCAL_RESUME.md' or path==target:
            return
        if not path.is_relative_to(root) or not path.is_file():
            raise RuntimeError('Missing integrity input '+str(relative))
        key=str(path.relative_to(root))
        if key not in hashes:
            hashes[key]=hashlib.sha256(path.read_bytes()).hexdigest()
        if expected is not None and hashes[key]!=expected:
            mismatches[key]=dict(expected=expected,actual=hashes[key])
    parent_path=directory/'annular-all-native-jump-integrity-20261003.json'
    parent=json.loads(parent_path.read_text())
    if parent['state']!='complete' or parent['mismatches']:
        raise RuntimeError('Invalid parent authority')
    verify(parent_path.relative_to(root))
    for relative,digest in parent['hashes'].items():
        verify(relative,digest)
    names=['annular-P7-bisection-preparation-attempt01','annular-P7-bisected-live-primary-attempt01',
        'annular-P7-bisected-live-reference-attempt01','annular-P7-bisected-product-time-response-attempt01',
        'annular-P7-bisected-balanced-time-response-attempt01','annular-P7-bisection-analysis-attempt01',
        'annular-jump-dual-bound-attempt01']
    for name in names:
        path=directory/name/'status.json'
        report=json.loads(path.read_text())
        if report['state']!='complete' or not report['checks'] or not all(row['passed'] for row in report['checks']):
            raise RuntimeError('Incomplete run '+name)
        reports[name]=report
        verify(path.relative_to(root))
        for category in ['inputs','outputs']:
            for relative,digest in report[category].items():
                verify(relative,digest)
        for member in path.parent.iterdir():
            if member.is_file():
                verify(member.relative_to(root))
        authorities[name]=dict(state=report['state'],checks=len(report['checks']))
    scripts=['prepare_annular_P7_bisection_20261003.py','solve_annular_P7_bisection_20261003.py',
        'probe_annular_P7_bisection_20261003.py','analyze_annular_P7_bisection_20261003.py','seal_annular_P7_bisection_20261003.py',
        'derive_annular_jump_dual_bound_20261003.py']
    for name in scripts:
        path=root/'scripts'/name
        compile(path.read_text(),str(path),'exec')
        verify(path.relative_to(root))
    citations=[]
    for name in ['DERIVATION-20261003-fixed-profile-P7-bisection.md','RESULTS-20261003-fixed-profile-P7-bisection.md']:
        verify(name)
        for relative in re.findall(r'\x60([^\x60]+\.(?:md|py|json|npz|csv))\x60',(root/name).read_text()):
            verify(relative)
            citations.append(relative)
    analysis=reports['annular-P7-bisection-analysis-attempt01']
    csv_path=directory/'annular-P7-bisection-analysis-attempt01/P7-refinement-comparison.csv'
    with csv_path.open(encoding='utf-8',newline='') as stream:
        rows=list(csv.DictReader(stream))
    if len(rows)!=8 or any(None in row or any(value is None for value in row.values()) or row['valid_for_claim']!='False' for row in rows):
        raise RuntimeError('CSV validation failed')
    for mode in ['product','balanced']:
        probe=reports['annular-P7-bisected-'+mode+'-time-response-attempt01']
        arrays=[]
        for row in probe['probes']:
            with np.load(root/row['path'],allow_pickle=False) as archive:
                arrays.append({key:archive[key] for key in probe['witnesses']})
        for key,witness in probe['witnesses'].items():
            estimates=[(row[key]-arrays[0][key])/amount for row,amount in zip(arrays[1:],probe['amounts'])]
            coarse,fine=(4*estimates[1]-estimates[0])/3,(4*estimates[2]-estimates[1])/3
            if float(np.max(abs(fine)))!=witness['maximum'] or float(np.max(abs(fine-coarse)))!=witness['Richardson_difference']:
                raise RuntimeError('Jet replay failed '+mode+':'+key)
        for row in arrays:
            error=float(np.max(abs(row['shape']-row['ordinary_shape']-row['hinge_shape'])))
            if error>2e-12*max(float(np.max(abs(row['shape']))),1e-50):
                raise RuntimeError('Source chain replay failed')
        split=next(row for row in analysis['time_comparisons'] if row['mode']==mode)
        with np.load(root/split['split_path'],allow_pickle=False) as archive:
            error=np.max(abs(archive['measured']-archive['inferred_strong']-archive['weak_strong_transfer']))
            if error>5e-15*np.max(abs(archive['measured'])):
                raise RuntimeError('Weak/strong split replay failed')
    dual=reports['annular-jump-dual-bound-attempt01']
    for row in dual['results']:
        with np.load(root/row['path'],allow_pickle=False) as archive:
            norm=float(np.sqrt(archive['goal'].ravel()@archive['adjoint'].ravel()))
        if norm!=row['dual_norm'] or abs(norm*row['kinetic_defect_norm']-row['conditional_bound'])>2e-15*row['conditional_bound']:
            raise RuntimeError('Dual norm replay failed')
        if abs(row['field_response_change'])>row['conditional_bound']*(1+2e-10):
            raise RuntimeError('Conditional observable bound failed')
    start=datetime(2026,10,3,11,57,41,tzinfo=timezone.utc).timestamp()
    protected=root.parent/'formalization-workbench'
    changed=[str(path.relative_to(protected)) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime>=start]
    bytecode=list((root/'scripts').rglob('__pycache__'))
    if mismatches or changed or bytecode:
        raise RuntimeError(dict(mismatches=mismatches,protected_changes=changed,bytecode=list(map(str,bytecode))))
    result=dict(state='complete',sealed_at=datetime.now(timezone.utc).isoformat(),hashes=hashes,mismatches=mismatches,
        unique_files_rehashed=len(hashes),authorities=authorities,scripts_compiled=scripts,csv_rows_parsed=len(rows),
        cited_paths=sorted(set(citations)),refinement_rows=analysis['refinement_rows'],time_comparisons=analysis['time_comparisons'],
        fixed_physical_profile=True,native_support_unchanged=True,asymptotic_convergence_proven=False,
        spatial_jump_convergence_gate_passed=False,interface_dual_results=dual['results'],
        valid_for_physics_claim=False,protected_workbench_changed_since_turn_start=0,bytecode_cache_present=False,
        self_output_and_mutable_resume_excluded=True,pending={},github_action=False,subagents_used=False)
    with target.open('x',encoding='utf-8') as stream:
        stream.write(json.dumps(result,indent=2)+'\n')
    if json.loads(target.read_text())['state']!='complete':
        raise RuntimeError('Output authority verification failed')
    print(json.dumps(dict(state='complete',files=len(hashes),mismatches=len(mismatches),scripts=len(scripts),
        csv_rows=len(rows),checks=sum(row['checks'] for row in authorities.values()),protected_changes=0)),flush=True)


if __name__=='__main__':
    main()
