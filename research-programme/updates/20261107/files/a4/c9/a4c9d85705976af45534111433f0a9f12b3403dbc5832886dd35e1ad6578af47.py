from derive_annular_source_gravity_20260914 import EvidenceRun
from pathlib import Path
from datetime import datetime,timezone
from decimal import Decimal,localcontext
from fractions import Fraction
import hashlib
import json
import numpy as np


def main():
    root = Path(__file__).resolve().parents[1]
    directory = root/'source-intake/navier-stokes/20260914'
    target = directory/'annular-matter-gravity-stage-integrity-20261001.json'
    if target.exists():
        raise FileExistsError(target)
    hashes,records,mismatches = {},{},[]

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

    prior_path = directory/'annular-integrated-baseline-stage-integrity-20261001.json'
    prior = json.loads(prior_path.read_text())
    if prior['state']!='complete' or prior['mismatches']:
        raise RuntimeError('Incomplete previous stage')
    verify(str(prior_path.relative_to(root)))
    for relative,expected in prior['hashes'].items():
        verify(relative,expected)
    reports = {}
    names = ['annular-matter-gravity-reference-third-attempt01','annular-matter-gravity-MTS-third-attempt01',
        'annular-matter-gravity-assembly-attempt01','annular-matter-gravity-high-order-attempt01']
    for name in names:
        path = directory/name/'status.json'
        report = json.loads(path.read_text())
        if report['state']!='complete' or not all(row['passed'] for row in report['checks']):
            raise RuntimeError('Incomplete stage '+name)
        verify(str(path.relative_to(root)))
        for category in ['inputs','outputs']:
            for relative,expected in report[category].items():
                verify(relative,expected)
        for path in path.parent.iterdir():
            if path.is_file():
                verify(str(path.relative_to(root)))
        log = directory/(name+'.log')
        if log.exists():
            verify(str(log.relative_to(root)))
        records[name] = dict(state=report['state'],checks=len(report['checks']))
        reports[name] = report
    matched_cuts = {}
    panel_count = 0
    with localcontext() as context:
        context.prec = 90
        for short in ['reference','MTS']:
            report = reports['annular-matter-gravity-'+short+'-third-attempt01']
            for row in report['results']:
                data = json.loads((root/row['path']).read_text())
                summary = data['summary']
                cuts = [Decimal(value) for value in data['cuts']]
                if len(data['panels'])+1!=len(cuts) or any(last<=first for first,last in zip(cuts[:-1],cuts[1:])):
                    raise RuntimeError('Invalid completed panel partition')
                key = summary['mode']+'-'+str(summary['order'])
                digest = hashlib.sha256(json.dumps(data['cuts']).encode()).hexdigest()
                if key in matched_cuts and matched_cuts[key]!=digest:
                    raise RuntimeError('MTS/reference panel cuts differ '+key)
                matched_cuts[key] = digest
                for column,name in enumerate(['gravity','dust_radial','combined','dust_label']):
                    for index in range(3):
                        total = sum((Decimal(panel[column][index]) for panel in data['panels']),Decimal(0))
                        if abs(total-Decimal(summary[name][index]))>Decimal('1e-62'):
                            raise RuntimeError('Independent panel accumulation failed')
                panel_count += len(data['panels'])
    assembly = reports['annular-matter-gravity-assembly-attempt01']
    witnesses = 0
    original = json.loads((directory/'annular-repaired-compatibility-attempt02/status.json').read_text())
    previous = json.loads((directory/'annular-integrated-baseline-assembly-attempt01/status.json').read_text())
    for row in assembly['summaries']:
        data = json.loads((root/row['path']).read_text())
        old_row = next(item for item in original['summaries'] if item['branch']==row['branch']
            and item['source_variant']==row['source_variant'] and item['baseline_variant']=='separate_C0_baseline')
        recent_row = next(item for item in previous['summaries'] if item['branch']==row['branch']
            and item['source_variant']==row['source_variant'] and item['baseline_scenario']=='coefficient_retained_envelope')
        old,recent = [json.loads((root/item['path']).read_text()) for item in [old_row,recent_row]]
        if data['columns']!=old['columns'] or data['column_error']!=old['column_error']:
            raise RuntimeError('Columns changed')
        if row['scenario']=='locked_original' and data['baseline_error']!=old['baseline_error']:
            raise RuntimeError('Original error budget not locked')
        if row['scenario']=='locked_previous' and data['baseline_error']!=recent['baseline_error']:
            raise RuntimeError('Previous error budget not locked')
        if row['scenario']=='accounted' and np.any(np.array(data['baseline_error'])<np.array(recent['baseline_error'])):
            raise RuntimeError('Old allowance removed')
        for orthant in data['envelope_search']['orthants']:
            witness = orthant['exact_witness']
            if witness is None:
                continue
            amplitudes = [orthant['signs'][column]*Fraction(int(witness['numerator'][column]),int(witness['denominator'])) for column in range(3)]
            for index in range(4):
                residual = Fraction.from_float(float(data['baseline'][index]))+sum(Fraction.from_float(float(data['columns'][index][column]))*amplitudes[column] for column in range(3))
                budget = Fraction.from_float(float(data['baseline_error'][index]))+sum(Fraction.from_float(float(data['column_error'][index][column]))*abs(amplitudes[column]) for column in range(3))
                if abs(residual)>budget:
                    raise RuntimeError('Original-equation exact witness failed')
            witnesses += 1
    compiled = []
    for name in ['annular_matter_gravity_transport_20261001.py','probe_annular_matter_gravity_transport_20261001.py',
        'assemble_annular_matter_gravity_transport_20261001.py','verify_annular_matter_gravity_transport_20261001.py',
        'seal_annular_matter_gravity_transport_20261001.py']:
        path = root/'scripts'/name
        compile(path.read_text(),str(path),'exec')
        verify(str(path.relative_to(root)))
        compiled.append(name)
    for name in ['DERIVATION-20261001-matter-gravity-transport-remainder.md','RESULTS-20261001-matter-gravity-transport.md']:
        verify(name)
    started = datetime(2026,10,1,18,3,49,tzinfo=timezone.utc).timestamp()
    protected = root.parent/'formalization-workbench'
    changed = [str(path.relative_to(protected)) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime>=started]
    bytecode = list((root/'scripts').rglob('__pycache__'))
    if mismatches or changed or bytecode:
        raise RuntimeError(dict(mismatches=mismatches,protected=changed,bytecode=list(map(str,bytecode))))
    result = dict(state='complete',sealed_at=datetime.now(timezone.utc).isoformat(),hashes=hashes,mismatches=mismatches,
        unique_files_rehashed=len(hashes),authorities=records,scripts_compiled=compiled,
        panels_independently_resummed=panel_count,matched_branch_cut_hashes=matched_cuts,
        coupled_cases=len(assembly['summaries']),exact_witnesses_replayed_in_original_equations=witnesses,
        fixed_budgets_verified=True,old_error_allowances_retained=True,
        off_shell_transport_identity_verified=True,nonzero_remainder_retained=True,
        quadrature_arithmetic_improved_for_fixed_fields=True,parent_field_accuracy_proven=False,
        protected_workbench_changed_since_turn_start=len(changed),bytecode_cache_present=False,
        current_resume_excluded=True,pending={},github_action=False,subagents_used=False,valid_for_physics_claim=False)
    with target.open('x') as stream:
        stream.write(json.dumps(result,indent=2)+'\n')
    print(json.dumps({key:value for key,value in result.items() if key!='hashes'},indent=2),flush=True)


if __name__=='__main__':
    main()
