from datetime import datetime,timezone
from pathlib import Path
from decimal import Decimal,localcontext
from fractions import Fraction
from seal_annular_constrained_state_search_20261001 import independent_sum,bareiss_positive
from analyze_annular_source_flat_state_20261002 import rational_separator,read_archive
import csv
import ctypes
import hashlib
import json
import numpy as np


def main():
    kernel = ctypes.windll.kernel32
    kernel.GetCurrentProcess.restype = ctypes.c_void_p
    kernel.SetProcessAffinityMask.argtypes = [ctypes.c_void_p,ctypes.c_size_t]
    if not kernel.SetProcessAffinityMask(kernel.GetCurrentProcess(),1<<2):
        raise OSError('Affinity failed')
    root = Path(__file__).resolve().parents[1]
    directory = root/'source-intake/navier-stokes/20260914'
    target = directory/'annular-source-flat-native-integrity-20261002.json'
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
    previous_path = directory/'annular-null-coupled-acceleration-integrity-20261001.json'
    previous = json.loads(previous_path.read_text())
    if previous['state']!='complete' or previous['mismatches']:
        raise RuntimeError('Incomplete parent')
    verify(str(previous_path.relative_to(root)))
    for relative,expected in previous['hashes'].items():
        verify(relative,expected)
    failed = 'annular-source-flat-native-state-fine-attempt01'
    names = [failed,'annular-source-flat-native-analysis-attempt01']
    for level in ['fine','third']:
        names += ['annular-source-flat-native-state-'+level+'-attempt02',
            'annular-source-flat-native-search-'+level+'-attempt01',
            'annular-source-flat-live-feedback-'+level+'-attempt01']
    for name in names:
        path = directory/name/'status.json'
        report = json.loads(path.read_text())
        if name==failed:
            if report['state']!='failed' or 'hinge_support_disjoint_rowwise' not in report.get('error',''):
                raise RuntimeError('Unexpected retained original outcome')
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
    form_layers,feedback_layers,certificates = 0,0,[]
    with localcontext() as context:
        context.prec = 75
        for level in ['fine','third']:
            search = reports['annular-source-flat-native-search-'+level+'-attempt01']
            forms = {}
            for item in search['rule_outputs']:
                saved = read_archive(root/item['path'])
                forms[item['material']] = saved
                for total,layer in [('forces','force_layers'),('norm','norm_layers'),('potential','potential_layers')]:
                    independent_sum(saved['weights'],saved[layer],saved[total])
                form_layers += len(saved['weights'])
            for row in search['searches']:
                if row['certificate'] and row['certificate']['found']:
                    saved = forms[row['material']]
                    matrix = rational_separator(saved['forces'],saved['norm'],row['size'],row['certificate'])
                    certificates.append(dict(level=level,size=row['size'],positive_leading_minors=bareiss_positive(matrix)))
            feedback = reports['annular-source-flat-live-feedback-'+level+'-attempt01']
            if feedback['fresh_metric_residual']>=8e-14 or feedback['native_radial_action_relative_error']>=2e-8:
                raise RuntimeError('Invalid live radial closure')
            if feedback['native_constraints_solved'] or feedback['full_trajectory_computed']:
                raise RuntimeError('Scalar feedback probe promoted beyond scope')
            for row in feedback['results']:
                saved = read_archive(root/row['path'])
                independent_sum(saved['weights'],saved['layers'],saved['total'])
                independent_sum(saved['weights'],saved['energy_layers'],saved['energy'])
                feedback_layers += len(saved['weights'])
                if np.max(abs(saved['total']-row['force']))!=0:
                    raise RuntimeError('Feedback summary mismatch')
    compiled = []
    for name in ['annular_source_flat_native_20261002.py','annular_native_source_hinge_20261002.py',
        'construct_annular_source_flat_state_20261002.py','construct_annular_source_flat_state_v2_20261002.py',
        'search_annular_source_flat_state_20261002.py','probe_annular_source_flat_live_feedback_20261002.py',
        'analyze_annular_source_flat_state_20261002.py','seal_annular_source_flat_state_20261002.py']:
        path = root/'scripts'/name
        compile(path.read_text(),str(path),'exec')
        verify(str(path.relative_to(root)))
        compiled.append(name)
    for name in ['DERIVATION-20261002-source-flat-native-compatible-initial-data.md',
        'DERIVATION-20261002-exact-source-hinge-support.md','DERIVATION-20261002-source-flat-live-feedback.md',
        'DERIVATION-20261002-source-flat-nullspace-separation.md',
        'DERIVATION-20261002-quadratic-source-core-construction.md',
        'DERIVATION-20261002-general-second-order-shape-preservation.md',
        'RESULTS-20261002-source-flat-native-state.md']:
        verify(name)
    csv_rows = 0
    for path in (directory/'annular-source-flat-native-analysis-attempt01').glob('*.csv'):
        with path.open(encoding='utf-8',newline='') as stream:
            rows = list(csv.DictReader(stream))
        if any(None in row or any(value is None for value in row.values()) or row['valid_for_claim']!='False' for row in rows):
            raise RuntimeError('Malformed comparison CSV '+str(path))
        csv_rows += len(rows)
    if csv_rows!=20:
        raise RuntimeError('Unexpected comparison row count')
    field = np.array([Fraction(2,3),Fraction(-3,5)],dtype=object)
    acceleration = np.array([Fraction(7,11),Fraction(5,13)],dtype=object)
    matrix = np.array([[Fraction(1,7),Fraction(3,8)],[Fraction(3,8),Fraction(-2,9)]],dtype=object)
    response = np.array([[Fraction(-5,12),Fraction(1,3)],[Fraction(1,3),Fraction(4,7)]],dtype=object)
    field_series = np.array([field,np.zeros(2,dtype=int),acceleration/2],dtype=object)
    matrix_series = np.array([matrix,np.zeros((2,2),dtype=int),response/2],dtype=object)
    quadratic_coefficient = sum((field_series[first]@matrix_series[middle]@field_series[last]
        for first in range(3) for middle in range(3) for last in range(3) if first+middle+last==2),Fraction(0))
    expected_second = 2*acceleration@matrix@field+field@response@field
    if 2*quadratic_coefficient!=expected_second:
        raise RuntimeError('General second-order constraint identity failed')
    started = datetime(2026,10,1,23,47,57,tzinfo=timezone.utc).timestamp()
    protected = root.parent/'formalization-workbench'
    changed = [str(path.relative_to(protected)) for path in protected.rglob('*')
        if path.is_file() and path.stat().st_mtime>=started]
    bytecode = list((root/'scripts').rglob('__pycache__'))
    if changed or bytecode or mismatches:
        raise RuntimeError(dict(protected_changes=changed,bytecode=list(map(str,bytecode)),mismatches=mismatches))
    analysis = reports['annular-source-flat-native-analysis-attempt01']
    result = dict(state='complete',sealed_at=datetime.now(timezone.utc).isoformat(),hashes=hashes,mismatches=mismatches,
        unique_files_rehashed=len(hashes),authorities=authorities,scripts_compiled=compiled,csv_rows_parsed=csv_rows,
        form_layers_independently_summed=form_layers,live_feedback_layers_independently_summed=feedback_layers,
        exact_finite_certificates_replayed=certificates,physical_initial_acceleration_computed=True,
        exact_general_second_derivative_control=str(expected_second),
        source_corner_compatible_initial_construction=True,native_force_and_radial_load_retained=True,
        comparison=analysis['coupled_summary'],refinement=analysis['refinement'],search_summary=analysis['search_summary'],
        live_feedback={level:{key:reports['annular-source-flat-live-feedback-'+level+'-attempt01'][key]
            for key in ['frozen_root','fresh_metric_residual','maximum_mass_change','maximum_log_lapse_change',
                'frozen_force_max','live_force_max','live_force_change_max','quadrature_force_change_max',
                'frozen_common_scaled_max','live_common_scaled_max']} for level in ['fine','third']},
        native_constraints_solved=False,physical_trajectory_computed=False,finite_certificate_not_global_no_go=True,
        retained_failure_reconciliation='Exact one-sided affine-hinge annihilation replaces finite-precision zero cancellation; full source-force tolerance unchanged.',
        protected_workbench_changed_since_turn_start=len(changed),bytecode_cache_present=False,pending={},
        current_resume_excluded=True,github_action=False,subagents_used=False,valid_for_physics_claim=False)
    with target.open('x',encoding='utf-8') as stream:
        stream.write(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(state='complete',files=len(hashes),mismatches=len(mismatches),scripts=len(compiled),
        csv_rows=csv_rows,form_layers=form_layers,live_layers=feedback_layers,certificates=len(certificates),
        passed_checks=sum(row['passed_checks'] for row in authorities.values()),protected_changes=len(changed))),flush=True)


if __name__=='__main__':
    main()
