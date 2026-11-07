from datetime import datetime,timezone
from pathlib import Path
from decimal import Decimal,localcontext
from seal_annular_constrained_state_search_20261001 import independent_sum,bareiss_positive
from analyze_annular_source_flat_state_20261002 import rational_separator,read_archive
import csv
import ctypes
import hashlib
import json
import re
import numpy as np


def main():
    kernel = ctypes.windll.kernel32
    kernel.GetCurrentProcess.restype = ctypes.c_void_p
    kernel.SetProcessAffinityMask.argtypes = [ctypes.c_void_p,ctypes.c_size_t]
    if not kernel.SetProcessAffinityMask(kernel.GetCurrentProcess(),1<<2):
        raise OSError('Affinity failed')
    root = Path(__file__).resolve().parents[1]
    directory = root/'source-intake/navier-stokes/20260914'
    target = directory/'annular-quadratic-transmission-integrity-20261002.json'
    if target.exists():
        raise FileExistsError(target)
    hashes,mismatches,reports,authorities = {},[],{},{}
    def verify(relative,expected=None):
        path = (root/relative).resolve()
        if path==root/'CURRENT_LOCAL_RESUME.md':
            return
        if not path.is_relative_to(root) or not path.is_file():
            raise RuntimeError('Invalid integrity path '+relative)
        key = str(path.relative_to(root))
        if key not in hashes:
            hashes[key] = hashlib.sha256(path.read_bytes()).hexdigest()
        if expected is not None and hashes[key]!=expected:
            mismatches.append(key)
    previous_path = directory/'annular-source-flat-native-integrity-20261002.json'
    previous = json.loads(previous_path.read_text())
    if previous['state']!='complete' or previous['mismatches']:
        raise RuntimeError('Incomplete parent')
    verify(str(previous_path.relative_to(root)))
    for relative,expected in previous['hashes'].items():
        verify(relative,expected)
    failures = {'annular-native-carrier-denominator-repair-attempt01':"bad operand type for abs(): 'list'",
        'annular-live-native-transmission-third-attempt01':'iteration0:outer_flux'}
    names = ['annular-quadratic-core-analysis-attempt01','annular-native-interface-transmission-attempt01',
        'annular-native-transmission-material-attempt01','annular-native-carrier-denominator-repair-attempt01',
        'annular-native-carrier-denominator-repair-attempt02','annular-live-native-transmission-third-attempt01',
        'annular-live-native-transmission-third-attempt02','annular-native-transmission-analysis-attempt01']
    for level in ['fine','third']:
        names += ['annular-quadratic-core-state-'+level+'-attempt01','annular-quadratic-core-search-'+level+'-attempt01']
    for name in names:
        path = directory/name/'status.json'
        report = json.loads(path.read_text())
        if name in failures:
            if report['state']!='failed' or failures[name] not in report.get('error',''):
                raise RuntimeError('Unrecognized retained failure '+name)
            failed_checks = [row['name'] for row in report['checks'] if not row['passed']]
            expected = [] if name.startswith('annular-native-carrier') else ['iteration0:outer_flux']
            if failed_checks!=expected:
                raise RuntimeError('Unexpected failed-check set '+name)
        elif report['state']!='complete' or not report['checks'] or not all(row['passed'] for row in report['checks']):
            raise RuntimeError('Incomplete authority '+name)
        verify(str(path.relative_to(root)))
        for category in ['inputs','outputs']:
            for relative,expected in report[category].items():
                verify(relative,expected)
        for member in path.parent.iterdir():
            if member.is_file():
                verify(str(member.relative_to(root)))
        reports[name] = report
        authorities[name] = dict(state=report['state'],checks=len(report['checks']),passed_checks=sum(row['passed'] for row in report['checks']))
    layers,certificates = 0,[]
    with localcontext() as context:
        context.prec = 75
        for level in ['fine','third']:
            search = reports['annular-quadratic-core-search-'+level+'-attempt01']
            forms = {}
            for item in search['rule_outputs']:
                saved = read_archive(root/item['path'])
                forms[item['material']] = saved
                for total,layer in [('forces','force_layers'),('norm','norm_layers'),('potential','potential_layers')]:
                    independent_sum(saved['weights'],saved[layer],saved[total])
                layers += len(saved['weights'])
            for item in search['searches']:
                if item['certificate'] and item['certificate']['found']:
                    saved = forms[item['material']]
                    matrix = rational_separator(saved['forces'],saved['norm'],item['size'],item['certificate'])
                    certificates.append(dict(level=level,size=item['size'],positive_leading_minors=bareiss_positive(matrix)))
        carrier = reports['annular-native-carrier-denominator-repair-attempt02']
        for case in carrier['cases']:
            exact = read_archive(root/case['exact_path'])
            decoded = {name:np.array([Decimal(value) for value in exact[name]],dtype=object) for name in ['A','C','beta','left','right','mean']}
            residual = decoded['beta']*(decoded['right']-decoded['left'])-decoded['A']
            pressure = decoded['beta']*(decoded['right']**2-decoded['left']**2)/2+decoded['C']
            if max(map(abs,residual))>=Decimal('1e-35') or max(map(abs,pressure))>=Decimal('1e-35'):
                raise RuntimeError('Carrier transmission replay failed')
            if case['continuous_material_bound_proven'] or case['own_metric_recomputed'] or case['source_acceleration_recomputed']:
                raise RuntimeError('Frozen carrier scope promoted')
    live = reports['annular-live-native-transmission-third-attempt02']
    high = next(row for row in live['results'] if row['name']=='primary-16-64')
    correct_flag = bool(live['vertex_iteration_converged'] and high['maximum_trace_residual']<1e-9 and high['relative_point_residual']<1e-8 and high['relative_jump_residual']<1e-7)
    if correct_flag!=live['heldout_initial_conditions_within_declared_tolerance']:
        raise RuntimeError('Live pilot classification mismatch')
    if live['continuous_material_bound_proven'] or live['spatial_refinement_done_for_this_state'] or live['second_order_preservation_done'] or live['physical_evolution']:
        raise RuntimeError('Live pilot scope promoted')
    compiled = []
    for name in ['annular_quadratic_core_20261002.py','construct_annular_quadratic_core_20261002.py',
        'search_annular_quadratic_core_20261002.py','analyze_annular_quadratic_core_20261002.py',
        'probe_annular_native_transmission_20261002.py','probe_annular_transmission_material_20261002.py',
        'probe_annular_native_carrier_20261002.py','probe_annular_native_carrier_v2_20261002.py',
        'construct_annular_live_transmission_20261002.py','construct_annular_live_transmission_v2_20261002.py',
        'analyze_annular_native_transmission_20261002.py','seal_annular_quadratic_transmission_20261002.py']:
        path = root/'scripts'/name
        compile(path.read_text(),str(path),'exec')
        verify(str(path.relative_to(root)))
        compiled.append(name)
    citations = []
    for name in ['DERIVATION-20261002-quadratic-core-joint-attempt.md','DERIVATION-20261002-native-interface-transmission.md',
        'DERIVATION-20261002-native-carrier-denominator-repair.md','DERIVATION-20261002-live-native-transmission-pilot.md',
        'DERIVATION-20261002-source-geodesic-reduction-under-transmission.md','DERIVATION-20261002-live-transmission-exact-outer-buffer.md',
        'RESULTS-20261002-quadratic-core-and-native-transmission.md']:
        verify(name)
        for relative in re.findall(r'`([^`]+\.(?:md|py|json|csv|npz))`',(root/name).read_text()):
            verify(relative)
            citations.append(relative)
    csv_rows = 0
    for name in ['annular-quadratic-core-analysis-attempt01','annular-native-transmission-analysis-attempt01']:
        for path in (directory/name).glob('*.csv'):
            with path.open(encoding='utf-8',newline='') as stream:
                rows = list(csv.DictReader(stream))
            if any(None in row or any(value is None for value in row.values()) or row['valid_for_claim']!='False' for row in rows):
                raise RuntimeError('Malformed comparison CSV '+str(path))
            csv_rows += len(rows)
    if csv_rows!=24+len(live['results']):
        raise RuntimeError('Unexpected comparison row count')
    start = datetime(2026,10,2,1,15,51,tzinfo=timezone.utc).timestamp()
    protected = root.parent/'formalization-workbench'
    changed = [str(path.relative_to(protected)) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime>=start]
    bytecode = list((root/'scripts').rglob('__pycache__'))
    if changed or bytecode or mismatches:
        raise RuntimeError(dict(protected_changes=changed,bytecode=list(map(str,bytecode)),mismatches=mismatches))
    analysis = reports['annular-native-transmission-analysis-attempt01']
    core_analysis = reports['annular-quadratic-core-analysis-attempt01']
    result = dict(state='complete',sealed_at=datetime.now(timezone.utc).isoformat(),hashes=hashes,mismatches=mismatches,
        unique_files_rehashed=len(hashes),authorities=authorities,scripts_compiled=compiled,csv_rows_parsed=csv_rows,
        cited_local_paths_validated=sorted(set(citations)),form_layers_independently_summed=layers,exact_finite_certificates_replayed=certificates,
        core_source_condition_solved=True,core_search_summary=core_analysis['search_summary'],core_refinement=core_analysis['refinement'],
        carrier_summary=analysis['carrier_summary'],live_summary=analysis['live_summary'],geodesic_comparison=analysis['geodesic_comparison'],
        live_pilot_within_declared_initial_tolerances=correct_flag,continuous_material_bound_proven=False,
        live_candidate_spatial_refinement_done=False,second_order_preservation_done=False,physical_trajectory_computed=False,
        retained_failures_reconciliation=['List-summary failure only; fine carrier arrays exactly reproduced by daughter.',
            'Exact quiet-interval representation removes affine-cancellation exterior fields of order1e-81; original strict boundary test retained.'],
        protected_workbench_changed_since_turn_start=len(changed),bytecode_cache_present=False,pending={},current_resume_excluded=True,
        github_action=False,subagents_used=False,valid_for_physics_claim=False)
    with target.open('x',encoding='utf-8') as stream:
        stream.write(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(state='complete',files=len(hashes),mismatches=len(mismatches),scripts=len(compiled),csv_rows=csv_rows,
        form_layers=layers,certificates=len(certificates),passed_checks=sum(row['passed_checks'] for row in authorities.values()),
        live_pilot_within_tolerances=correct_flag,protected_changes=len(changed))),flush=True)


if __name__=='__main__':
    main()
