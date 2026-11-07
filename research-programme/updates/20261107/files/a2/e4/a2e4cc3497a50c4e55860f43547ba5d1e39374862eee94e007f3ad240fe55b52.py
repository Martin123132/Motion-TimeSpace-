from derive_annular_source_gravity_20260914 import EvidenceRun
from pathlib import Path
from datetime import datetime, timezone
from fractions import Fraction
from decimal import Decimal, localcontext
import csv
import hashlib
import json
import numpy as np


def bareiss_positive(matrix):
    work = [row.copy() for row in matrix]
    previous = Fraction(1)
    minors = []
    for index in range(len(work)-1):
        pivot = work[index][index]
        if pivot<=0:
            raise RuntimeError('Nonpositive leading minor')
        minors.append(str(pivot))
        for row in range(index+1,len(work)):
            for column in range(index+1,len(work)):
                work[row][column] = (pivot*work[row][column]-work[row][index]*work[index][column])/previous
        for row in range(index+1,len(work)):
            work[row][index] = Fraction(0)
        previous = pivot
    if work[-1][-1]<=0:
        raise RuntimeError('Nonpositive final determinant')
    return minors+[str(work[-1][-1])]


def independent_sum(weights,layers,total):
    values = layers.reshape(len(weights),-1)
    expected = total.ravel()
    for column in range(values.shape[1]):
        terms = [Decimal.from_float(float(weight))*Decimal.from_float(float(value))
            for weight,value in zip(weights,values[:,column])]
        exact = sum(terms,Decimal(0))
        budget = Decimal.from_float(128*np.finfo(float).eps)*sum(map(abs,terms),Decimal(0))+Decimal('1e-90')
        if abs(exact-Decimal.from_float(float(expected[column])))>budget:
            raise RuntimeError('Independent weighted sum failed')


def main():
    root = Path(__file__).resolve().parents[1]
    directory = root/'source-intake/navier-stokes/20260914'
    target = directory/'annular-constrained-state-search-integrity-20261001.json'
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
    previous_path = directory/'annular-common-jet-jump-stage-integrity-20261001.json'
    previous = json.loads(previous_path.read_text())
    if previous['state']!='complete' or previous['mismatches']:
        raise RuntimeError('Incomplete parent')
    verify(str(previous_path.relative_to(root)))
    for relative,expected in previous['hashes'].items():
        verify(relative,expected)
    names = ['annular-nonzero-shape-constraint-'+level+'-attempt0'+str(attempt)
        for level in ['fine','third'] for attempt in [1,2,3]]
    names += ['annular-nonzero-shape-search-analysis-attempt01','annular-pinned-shape-search-analysis-attempt01',
        'annular-native-shape-state-analysis-attempt01','annular-nonzero-kernel-family-attempt01',
        'annular-nonzero-kernel-family-attempt02','annular-null-slice-preservation-gate-attempt01']
    for level in ['fine','third']:
        names += ['annular-live-constraint-feedback-'+level+'-attempt01',
            'annular-pinned-shape-constraint-'+level+'-attempt01','annular-native-shape-state-'+level+'-attempt01']
    for name in names:
        path = directory/name/'status.json'
        report = json.loads(path.read_text())
        failed = name.startswith('annular-nonzero-shape-constraint-') and not name.endswith('attempt03')
        if failed:
            expected = "RuntimeError('MTS-primary:base_factor_replay: None')" if name.endswith('attempt01') else "RuntimeError('Normalized analytic Jacobian failed')"
            if report['state']!='failed' or report.get('error')!=expected:
                raise RuntimeError('Unreconciled original '+name)
        elif report['state']!='complete' or not all(row['passed'] for row in report['checks']):
            raise RuntimeError('Incomplete daughter '+name)
        verify(str(path.relative_to(root)))
        for category in ['inputs','outputs']:
            for relative,expected in report[category].items():
                verify(relative,expected)
        for member in path.parent.iterdir():
            if member.is_file():
                verify(str(member.relative_to(root)))
        log = directory/(name+'.log')
        if log.exists():
            verify(str(log.relative_to(root)))
        reports[name] = report
        records[name] = dict(state=report['state'],checks=len(report['checks']))
    families = [
        ('fixed_D_unpinned','annular-nonzero-shape-search-analysis-attempt01','annular-nonzero-shape-constraint-','-attempt03'),
        ('fixed_D_pinned','annular-pinned-shape-search-analysis-attempt01','annular-pinned-shape-constraint-','-attempt01'),
        ('native_pinned','annular-native-shape-state-analysis-attempt01','annular-native-shape-state-','-attempt01')]
    certificates = []
    form_layers,live_layers = 0,0
    with localcontext() as context:
        context.prec = 75
        for scope,analysis_name,prefix,suffix in families:
            analysis = reports[analysis_name]
            for level in ['fine','third']:
                for item in reports[prefix+level+suffix]['rule_outputs']:
                    with np.load(root/item['path'],allow_pickle=False) as archive:
                        for total,layer in [('forces','force_layers'),('norm','norm_layers'),('potential','potential_layers')]:
                            independent_sum(archive['weights'],archive[layer],archive[total])
                        form_layers += len(archive['weights'])
            for row in analysis['summaries']:
                certificate = row['certificate']
                if not certificate['found']:
                    continue
                for order in [48,32]:
                    if order==32 and not certificate['same_separator_lower_rule_positive']:
                        continue
                    search = reports[prefix+row['level']+suffix]
                    item = next(item for item in search['rule_outputs'] if item['branch']=='MTS-primary' and item['material']==order)
                    with np.load(root/item['path'],allow_pickle=False) as archive:
                        forces,norm = archive['forces'],archive['norm']
                    forces = (forces+forces.transpose(0,2,1))/2
                    norm = (norm+norm.T)/2
                    coefficients = list(map(Fraction.from_float,certificate['coefficients']))
                    coercivity = Fraction.from_float(certificate['coercivity'])
                    size = row['size']
                    matrix = [[sum(coefficients[test]*Fraction.from_float(float(forces[test,first,last]))
                        for test in range(size-1))-coercivity*Fraction.from_float(float(norm[first,last]))
                        for last in range(size)] for first in range(size)]
                    certificates.append(dict(scope=scope,level=row['level'],size=size,order=order,
                        positive_leading_minors=bareiss_positive(matrix)))
        for level in ['fine','third']:
            report = reports['annular-live-constraint-feedback-'+level+'-attempt01']
            if report['fresh_metric_residual']>=8e-14 or report['full_constrained_equilibrium_solved']:
                raise RuntimeError('Invalid comparator live-probe status')
            for result in report['results']:
                with np.load(root/result['path'],allow_pickle=False) as archive:
                    independent_sum(archive['weights'],archive['layers'],archive['total'])
                    live_layers += len(archive['weights'])
    preservation = reports['annular-null-slice-preservation-gate-attempt01']
    if preservation['parent_physical_acceleration_computed']:
        raise RuntimeError('Algebraic oracle mislabeled as coupled evolution')
    for case in preservation['cases']:
        with np.load(root/case['path'],allow_pickle=False) as archive:
            if np.max(abs(archive['forms'][:,:,0]))>=1e-40:
                raise RuntimeError('Null section radical failed')
            for name,time_value in [('forces_large',.125),('forces_small',.0625)]:
                expected = time_value**4*archive['forms'][:,1,1]/4
                if np.any(abs(archive[name]-expected)>1e-35+1e-11*abs(expected)):
                    raise RuntimeError('Independent quartic force law failed')
            if np.max(abs(archive['forces_large']-16*archive['forces_small']))>1e-11*max(float(np.max(abs(archive['forces_large']))),1e-40):
                raise RuntimeError('Independent quartic scaling failed')
    construction = reports['annular-nonzero-kernel-family-attempt02']
    for case in construction['cases']:
        if case['native_metric_residual']>=8e-14 or case['dynamic_preservation_established'] or case['flat_control_family_invariant']:
            raise RuntimeError('Invalid kernel-family interpretation')
        with np.load(root/case['native_rhs_path'],allow_pickle=False) as archive:
            radius,gram,state,coupling = archive['radius'],archive['old_gram'],archive['state'],float(archive['kappa'])
            metric = 1-2*state[0].ravel()/radius
            correction = np.array([coupling*radius**2*metric*gram,coupling*radius*gram])
            if not np.array_equal(correction,archive['correction']) or not np.array_equal(archive['old_rhs']-correction,archive['native_rhs']):
                raise RuntimeError('Native radial-load correction replay failed')
        for probe in case['native_probes']:
            if Decimal(probe['analytic_image_max'])>=Decimal('1e-40') or probe['maximum_shape_force']>=1e-20:
                raise RuntimeError('Invalid kernel sample')
    lower,source,upper,amplitude = Fraction(26,5),Fraction(6),Fraction(34,5),Fraction(7,13)
    points = [Fraction(53,10),Fraction(29,5),Fraction(61,10),Fraction(67,10)]
    jump = amplitude*(lower-upper)
    compensated = [amplitude*(point-source)*(point-lower if point<=source else point-upper)-jump*max(point-source,Fraction(0)) for point in points]
    difference = sum((compensated[index]/np.prod([point-other for other in points if other!=point])
        for index,point in enumerate(points)),Fraction(0))
    if difference!=0:
        raise RuntimeError('Independent exact nonuniform null-kernel witness failed')
    compiled = []
    for name in ['search_annular_nonzero_shape_constraint_20261001.py',
        'search_annular_nonzero_shape_constraint_v2_20261001.py','search_annular_nonzero_shape_constraint_v3_20261001.py',
        'analyze_annular_nonzero_shape_search_20261001.py','probe_annular_live_constraint_feedback_20261001.py',
        'search_annular_pinned_shape_constraint_20261001.py','analyze_annular_pinned_shape_search_20261001.py',
        'annular_native_trial_matrix_20261001.py','search_annular_native_shape_state_20261001.py',
        'analyze_annular_native_shape_state_20261001.py','probe_annular_nonzero_kernel_family_20261001.py',
        'probe_annular_nonzero_kernel_family_v2_20261001.py','derive_annular_null_slice_preservation_gate_20261001.py',
        'seal_annular_constrained_state_search_20261001.py']:
        path = root/'scripts'/name
        compile(path.read_text(),str(path),'exec')
        verify(str(path.relative_to(root)))
        compiled.append(name)
    for name in ['DERIVATION-20261001-nonzero-shape-constraint-state-search.md',
        'DERIVATION-20261001-constraint-search-coordinate-repair.md','DERIVATION-20261001-live-constraint-feedback-probe.md',
        'DERIVATION-20261001-pinned-constraint-search-correction.md','DERIVATION-20261001-native-shape-state-Jacobian.md',
        'DERIVATION-20261001-nonzero-kernel-family-and-preservation.md','DERIVATION-20261001-kernel-native-radial-reconciliation.md',
        'DERIVATION-20261001-null-slice-fourth-order-preservation.md','RESULTS-20261001-nonzero-constrained-state-attempt.md']:
        verify(name)
    csv_rows = 0
    for relative in hashes:
        if relative.endswith('.csv') and '20261001' in relative:
            with (root/relative).open(encoding='utf-8-sig',newline='') as stream:
                reader = csv.DictReader(stream)
                for row in reader:
                    if None in row or any(value is None for value in row.values()):
                        raise RuntimeError('Malformed CSV '+relative)
                    csv_rows += 1
    started = datetime(2026,10,1,20,23,38,tzinfo=timezone.utc).timestamp()
    protected = root.parent/'formalization-workbench'
    changed = [str(path.relative_to(protected)) for path in protected.rglob('*')
        if path.is_file() and path.stat().st_mtime>=started]
    bytecode = list((root/'scripts').rglob('__pycache__'))
    if changed or bytecode or mismatches:
        raise RuntimeError(dict(changed=changed,bytecode=list(map(str,bytecode)),mismatches=mismatches))
    result = dict(state='complete',sealed_at=datetime.now(timezone.utc).isoformat(),hashes=hashes,mismatches=mismatches,
        unique_files_rehashed=len(hashes),authorities=records,scripts_compiled=compiled,csv_rows_parsed=csv_rows,
        exact_separators_independently_replayed=certificates,independently_summed_form_layers=form_layers,
        live_fixed_D_force_layers_independently_resummed=live_layers,
        finite_matrix_obstruction_is_not_global_no_go=True,
        scope_corrections=['Unpinned first search retained as comparator; pinned daughters authoritative for fixed endpoints.',
            'Fixed-D obstructions do not substitute for the native action; native searches performed separately.',
            'Native-null radial equations checked separately from inherited fixed-reference loads.'],
        nonzero_instantaneous_native_Gram_family_constructed=True,flat_control_family_invariant=False,
        quartic_preservation_oracle_cases=len(preservation['cases']),parent_coupled_acceleration_computed=False,
        native_frozen_candidates=reports['annular-native-shape-state-analysis-attempt01']['live_candidates'],
        parent_action_changed=False,full_equilibrium_solved=False,physical_evolution_performed=False,
        protected_workbench_changed_since_turn_start=len(changed),bytecode_cache_present=False,
        pending={},current_resume_excluded=True,github_action=False,subagents_used=False,valid_for_physics_claim=False)
    with target.open('x',encoding='utf-8') as stream:
        stream.write(json.dumps(result,indent=2)+'\n')
    print(json.dumps({key:value for key,value in result.items()
        if key not in ['hashes','exact_separators_independently_replayed']},indent=2),flush=True)


if __name__=='__main__':
    main()

