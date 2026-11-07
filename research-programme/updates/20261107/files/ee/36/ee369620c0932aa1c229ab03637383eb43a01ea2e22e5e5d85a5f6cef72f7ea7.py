from derive_annular_source_gravity_20260914 import EvidenceRun
from pathlib import Path
from datetime import datetime, timezone
from decimal import Decimal, localcontext
from fractions import Fraction
import hashlib
import json
import numpy as np


def main():
    root = Path(__file__).resolve().parents[1]
    directory = root/'source-intake/navier-stokes/20260914'
    target = directory/'annular-C1-integrated-stage-integrity-20261001.json'
    if target.exists():
        raise FileExistsError(target)
    hashes, mismatches, records, reports = {}, [], {}, {}

    def verify(relative, expected=None):
        path = (root/relative).resolve()
        if path==root/'CURRENT_LOCAL_RESUME.md':
            return
        if not path.is_relative_to(root) or not path.is_file():
            raise RuntimeError('Invalid integrity source '+relative)
        key = str(path.relative_to(root))
        if key not in hashes:
            hashes[key] = hashlib.sha256(path.read_bytes()).hexdigest()
        if expected is not None and hashes[key]!=expected:
            mismatches.append(key)

    previous_path = directory/'annular-matter-gravity-stage-integrity-20261001.json'
    previous = json.loads(previous_path.read_text())
    if previous['state']!='complete' or previous['mismatches']:
        raise RuntimeError('Incomplete parent')
    verify(str(previous_path.relative_to(root)))
    for relative, expected in previous['hashes'].items():
        verify(relative,expected)
    names = ['annular-C1-coefficient-probe-attempt02',
        'annular-C1-material-reference-third-attempt01','annular-C1-material-MTS-third-attempt01',
        'annular-C1-matter-gravity-reference-third-attempt01','annular-C1-matter-gravity-MTS-third-attempt01',
        'annular-C1-integrated-assembly-attempt01']
    for name in names:
        path = directory/name/'status.json'
        report = json.loads(path.read_text())
        if report['state']!='complete' or not all(row['passed'] for row in report['checks']):
            raise RuntimeError('Incomplete stage '+name)
        verify(str(path.relative_to(root)))
        for category in ['inputs','outputs']:
            for relative, expected in report[category].items():
                verify(relative,expected)
        for member in path.parent.iterdir():
            if member.is_file():
                verify(str(member.relative_to(root)))
        log = directory/(name+'.log')
        if log.exists():
            verify(str(log.relative_to(root)))
        reports[name] = report
        records[name] = dict(state=report['state'],checks=len(report['checks']))
    recovery_path = root/'RECOVERY-20261001-C1-symbolic-probe.json'
    recovery = json.loads(recovery_path.read_text())
    if recovery['exit_code']!=1 or recovery['state']!='interrupted_symbolic_stage':
        raise RuntimeError('Invalid interrupted probe record')
    verify(str(recovery_path.relative_to(root)))
    first_path = directory/'annular-C1-coefficient-probe-attempt01/status.json'
    first = json.loads(first_path.read_text())
    if first['state']!='running' or len(first['checks'])!=1 or not first['checks'][0]['passed']:
        raise RuntimeError('Unexpected first probe content')
    for path in first_path.parent.iterdir():
        if path.is_file():
            verify(str(path.relative_to(root)))
    verify('scripts/probe_annular_C1_coefficient_response_20261001.py')
    matched, panels_resummed, wave_layers = {}, 0, 0
    with localcontext() as context:
        context.prec = 90
        for short in ['reference','MTS']:
            material = reports['annular-C1-material-'+short+'-third-attempt01']
            for item in material['rule_outputs']:
                with np.load(root/item['path'],allow_pickle=False) as archive:
                    weights,layers,total = [archive[key] for key in ['weights','layers','accumulated']]
                    key = 'wave-'+str(item['summary']['order'])
                    digest = hashlib.sha256(archive['labels'].tobytes()+weights.tobytes()).hexdigest()
                    if key in matched and matched[key]!=digest:
                        raise RuntimeError('Different branch material rules')
                    matched[key] = digest
                    for channel in range(4):
                        for moment in range(3):
                            terms = [Decimal.from_float(float(weight))*Decimal.from_float(float(value))
                                for weight,value in zip(weights,layers[:,channel,moment])]
                            exact = sum(terms,Decimal(0))
                            allowance = Decimal.from_float(64*np.finfo(float).eps)*sum(map(abs,terms),Decimal(0))+Decimal('1e-80')
                            if abs(exact-Decimal.from_float(float(total[channel,moment])))>allowance:
                                raise RuntimeError('Independent wave accumulation failed')
                    wave_layers += len(weights)
            matter = reports['annular-C1-matter-gravity-'+short+'-third-attempt01']
            for item in matter['results']:
                data = json.loads((root/item['path']).read_text())
                summary = data['summary']
                cuts = list(map(Decimal,data['cuts']))
                if len(data['panels'])+1!=len(cuts) or any(last<=first for first,last in zip(cuts[:-1],cuts[1:])):
                    raise RuntimeError('Invalid source partition')
                key = summary['mode']+'-'+str(summary['order'])
                digest = hashlib.sha256(json.dumps(data['cuts']).encode()).hexdigest()
                if key in matched and matched[key]!=digest:
                    raise RuntimeError('Different branch source partitions')
                matched[key] = digest
                for column,name in enumerate(['gravity','dust_radial','combined','dust_label']):
                    for moment in range(3):
                        value = sum((Decimal(panel[column][moment]) for panel in data['panels']),Decimal(0))
                        if abs(value-Decimal(summary[name][moment]))>Decimal('1e-62'):
                            raise RuntimeError('Independent source accumulation failed')
                panels_resummed += len(data['panels'])
    assembly = reports['annular-C1-integrated-assembly-attempt01']
    witnesses = 0
    for item in assembly['summaries']:
        data = json.loads((root/item['path']).read_text())
        prior = json.loads((root/data['prior_path']).read_text())
        if data['baseline']!=prior['baseline'] or data['baseline_error']!=prior['baseline_error']:
            raise RuntimeError('Baseline not held')
        columns,error = np.array(data['columns']),np.array(data['column_error'])
        old,old_error = np.array(prior['columns']),np.array(prior['column_error'])
        if not np.array_equal(columns[:,[0,2]],old[:,[0,2]]) or not np.array_equal(columns[0],old[0]):
            raise RuntimeError('Non-C1-current entry changed')
        if not np.array_equal(error[:,[0,2]],old_error[:,[0,2]]) or np.any(error<old_error):
            raise RuntimeError('Previous column allowance changed or removed')
        if data['scenario']!='accounted' and not np.array_equal(error,old_error):
            raise RuntimeError('Locked column budget changed')
        for orthant in data['envelope_search']['orthants']:
            witness = orthant['exact_witness']
            if witness is None:
                continue
            amplitudes = [orthant['signs'][column]*Fraction(int(witness['numerator'][column]),int(witness['denominator'])) for column in range(3)]
            for row in range(4):
                residual = Fraction.from_float(float(data['baseline'][row]))+sum(
                    Fraction.from_float(float(columns[row,column]))*amplitudes[column] for column in range(3))
                budget = Fraction.from_float(float(data['baseline_error'][row]))+sum(
                    Fraction.from_float(float(error[row,column]))*abs(amplitudes[column]) for column in range(3))
                if abs(residual)>budget:
                    raise RuntimeError('Original-equation witness failed')
            witnesses += 1
    compiled = []
    for name in ['annular_C1_coefficient_response_20261001.py','annular_C1_response_context_20261001.py',
        'probe_annular_C1_coefficient_response_20261001.py','probe_annular_C1_coefficient_response_v2_20261001.py',
        'integrate_annular_C1_material_20261001.py','integrate_annular_C1_matter_gravity_20261001.py',
        'assemble_annular_C1_integrated_20261001.py','seal_annular_C1_integrated_20261001.py']:
        path = root/'scripts'/name
        compile(path.read_text(),str(path),'exec')
        verify(str(path.relative_to(root)))
        compiled.append(name)
    for name in ['DERIVATION-20261001-C1-coefficient-current-response.md','DERIVATION-20261001-C1-integral-contract.md',
        'RESULTS-20261001-C1-integrated-current-response.md']:
        verify(name)
    started = datetime(2026,10,1,18,55,16,tzinfo=timezone.utc).timestamp()
    protected = root.parent/'formalization-workbench'
    changed = [str(path.relative_to(protected)) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime>=started]
    bytecode = list((root/'scripts').rglob('__pycache__'))
    if changed or bytecode or mismatches:
        raise RuntimeError(dict(changed=changed,bytecode=list(map(str,bytecode)),mismatches=mismatches))
    result = dict(state='complete',sealed_at=datetime.now(timezone.utc).isoformat(),hashes=hashes,mismatches=mismatches,
        unique_files_rehashed=len(hashes),authorities=records,interrupted_probe=recovery,
        scripts_compiled=compiled,wave_layers_independently_resummed=wave_layers,
        matter_panels_independently_resummed=panels_resummed,matched_branch_rules=matched,
        coupled_cases=len(assembly['summaries']),exact_witnesses_replayed_in_original_equations=witnesses,
        baseline_force_C0_C2_held=True,locked_budgets_verified=True,old_allowances_retained=True,
        protected_workbench_changed_since_turn_start=len(changed),bytecode_cache_present=False,
        pending={},current_resume_excluded=True,github_action=False,subagents_used=False,valid_for_physics_claim=False)
    with target.open('x') as stream:
        stream.write(json.dumps(result,indent=2)+'\n')
    print(json.dumps({key:value for key,value in result.items() if key!='hashes'},indent=2),flush=True)


if __name__=='__main__':
    main()
