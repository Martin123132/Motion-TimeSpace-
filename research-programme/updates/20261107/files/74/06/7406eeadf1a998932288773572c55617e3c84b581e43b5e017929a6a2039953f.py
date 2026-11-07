from derive_annular_source_gravity_20260914 import EvidenceRun
from seal_annular_constrained_state_search_20261001 import independent_sum
from datetime import datetime,timezone
from decimal import localcontext
from fractions import Fraction
from pathlib import Path
import csv
import hashlib
import json
import numpy as np


def main():
    root = Path(__file__).resolve().parents[1]
    directory = root/'source-intake/navier-stokes/20260914'
    target = directory/'annular-null-coupled-acceleration-integrity-20261001.json'
    if target.exists():
        raise FileExistsError(target)
    hashes,mismatches,reports,records = {},[],{},{}
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
    previous_path = directory/'annular-constrained-state-search-integrity-20261001.json'
    previous = json.loads(previous_path.read_text())
    if previous['state']!='complete' or previous['mismatches']:
        raise RuntimeError('Incomplete parent')
    verify(str(previous_path.relative_to(root)))
    for relative,expected in previous['hashes'].items():
        verify(relative,expected)
    failures = {
        'annular-native-null-acceleration-fine-attempt01':'bad operand type for abs',
        'annular-native-null-acceleration-third-attempt01':'bad operand type for abs',
        'annular-native-null-acceleration-summary-recovery-attempt01':'too many subscripts',
        'annular-Neumann-null-acceleration-fine-attempt01':'Unowned source',
        'annular-native-null-acceleration-comparison-attempt01':'fine:summary_quadrature_gate_maximum_difference'}
    complete = ['annular-native-null-acceleration-summary-recovery-attempt02',
        'annular-Neumann-kernel-family-attempt01',
        'annular-Neumann-null-acceleration-fine-attempt02','annular-Neumann-null-acceleration-third-attempt02',
        'annular-Neumann-source-corner-profile-fine-attempt01','annular-Neumann-source-corner-profile-third-attempt01',
        'annular-native-null-acceleration-comparison-attempt02','annular-pinned-source-P2-layer-law-attempt01']
    for name in list(failures)+complete:
        path = directory/name/'status.json'
        report = json.loads(path.read_text())
        if name in failures:
            if report['state']!='failed' or failures[name] not in report.get('error',''):
                raise RuntimeError('Unrecognized retained failure '+name)
        elif report['state']!='complete' or not all(row['passed'] for row in report['checks']):
            raise RuntimeError('Incomplete authority '+name)
        verify(str(path.relative_to(root)))
        for category in ['inputs','outputs']:
            for relative,expected in report[category].items():
                verify(relative,expected)
        for member in path.parent.iterdir():
            if member.is_file():
                verify(str(member.relative_to(root)))
        reports[name] = report
        records[name] = dict(state=report['state'],checks=len(report['checks']),
            passed_checks=sum(row['passed'] for row in report['checks']))
    layers = 0
    with localcontext() as context:
        context.prec = 75
        for prefix,suffix in [('annular-native-null-acceleration-','-attempt01'),('annular-Neumann-null-acceleration-','-attempt02')]:
            for level in ['fine','third']:
                for result in reports[prefix+level+suffix]['results']:
                    with np.load(root/result['gate_path'],allow_pickle=False) as archive:
                        independent_sum(archive['weights'],archive['force_layers'],archive['forms'])
                        if not np.array_equal(archive['fourth_derivative'],6*archive['forms'][:,0,0]):
                            raise RuntimeError('Fourth derivative factor changed')
                        layers += len(archive['weights'])
    lower,source,upper,amplitude = Fraction(26,5),Fraction(6),Fraction(34,5),Fraction(7,13)
    speed_square,drift = Fraction(3,5),Fraction(1,5)
    points = [Fraction(53,10),Fraction(29,5),Fraction(61,10),Fraction(67,10)]
    jump = 2*amplitude*(lower-upper)
    def profile(point):
        endpoint = lower if point<=source else upper
        return amplitude*((point-endpoint)**2-(source-endpoint)**2)
    compensated = [profile(point)-jump*max(point-source,Fraction(0)) for point in points]
    difference = sum((compensated[index]/np.prod([point-other for other in points if other!=point])
        for index,point in enumerate(points)),Fraction(0))
    if difference!=0 or profile(source)!=0:
        raise RuntimeError('Independent exact Neumann kernel witness failed')
    left_required = -drift-speed_square/(source-lower)
    right_required = -drift+speed_square/(upper-source)
    gap = speed_square*(1/(source-lower)+1/(upper-source))
    if right_required-left_required!=gap or gap<=0:
        raise RuntimeError('Independent exact source-corner gap failed')
    compiled = []
    for name in ['annular_zero_rate_euler_20261001.py','derive_annular_native_null_acceleration_20261001.py',
        'probe_annular_Neumann_kernel_family_20261001.py','derive_annular_Neumann_null_acceleration_20261001.py',
        'derive_annular_Neumann_null_acceleration_v2_20261001.py',
        'annular_acceleration_archive_checks_20261001.py','annular_acceleration_archive_checks_v2_20261001.py',
        'recover_annular_null_acceleration_summary_20261001.py','recover_annular_null_acceleration_summary_v2_20261001.py',
        'analyze_annular_native_null_acceleration_20261001.py','analyze_annular_native_null_acceleration_v2_20261001.py',
        'probe_annular_Neumann_source_corner_profile_20261001.py','derive_annular_pinned_source_P2_layer_20261001.py',
        'seal_annular_null_coupled_acceleration_20261001.py']:
        path = root/'scripts'/name
        compile(path.read_text(),str(path),'exec')
        verify(str(path.relative_to(root)))
        compiled.append(name)
    for name in ['DERIVATION-20261001-native-null-coupled-acceleration.md',
        'DERIVATION-20261001-Neumann-kernel-initial-slice.md',
        'DERIVATION-20261001-null-family-source-corner-compatibility.md',
        'DERIVATION-20261001-pinned-source-P2-acceleration-layer.md',
        'RESULTS-20261001-native-null-coupled-acceleration.md']:
        verify(name)
    csv_path = directory/'annular-native-null-acceleration-comparison-attempt02/coupled-null-acceleration-comparison.csv'
    with csv_path.open(encoding='utf-8',newline='') as stream:
        rows = list(csv.DictReader(stream))
    if len(rows)!=8 or any(None in row or any(value is None for value in row.values()) or row['valid_for_claim']!='False' for row in rows):
        raise RuntimeError('Malformed comparison CSV')
    started = datetime(2026,10,1,21,49,29,tzinfo=timezone.utc).timestamp()
    protected = root.parent/'formalization-workbench'
    changed = [str(path.relative_to(protected)) for path in protected.rglob('*')
        if path.is_file() and path.stat().st_mtime>=started]
    bytecode = list((root/'scripts').rglob('__pycache__'))
    if changed or bytecode or mismatches:
        raise RuntimeError(dict(changed=changed,bytecode=list(map(str,bytecode)),mismatches=mismatches))
    comparison = reports['annular-native-null-acceleration-comparison-attempt02']
    result = dict(state='complete',sealed_at=datetime.now(timezone.utc).isoformat(),hashes=hashes,mismatches=mismatches,
        unique_files_rehashed=len(hashes),authorities=records,scripts_compiled=compiled,csv_rows_parsed=len(rows),
        material_gate_layers_independently_resummed=layers,
        exact_rational_controls=dict(compensated_third_divided_difference=str(difference),positive_source_corner_gap=str(gap)),
        physical_coupled_acceleration_computed=True,natural_endpoint_initial_data_repaired=True,
        comparison=comparison['comparison'],spatial_refinement=comparison['spatial_refinement'],
        local_P2_layer_law=reports['annular-pinned-source-P2-layer-law-attempt01']['cases'],
        source_corner_condition_satisfied=False,native_quartic_gates_satisfied=False,
        finite_jet_failure_not_a_global_no_go=True,parent_action_changed=False,physical_trajectory_computed=False,
        protected_workbench_changed_since_turn_start=len(changed),bytecode_cache_present=False,
        pending={},current_resume_excluded=True,github_action=False,subagents_used=False,valid_for_physics_claim=False)
    with target.open('x',encoding='utf-8') as stream:
        stream.write(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(state=result['state'],unique_files_rehashed=len(hashes),mismatches=len(mismatches),
        scripts_compiled=len(compiled),gate_layers=layers,protected_changes=len(changed),
        complete_runs=len(complete),retained_reconciled_failures=len(failures))),flush=True)


if __name__=='__main__':
    main()

