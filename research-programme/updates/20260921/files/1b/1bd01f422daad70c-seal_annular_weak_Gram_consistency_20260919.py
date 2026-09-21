from derive_annular_source_gravity_20260914 import EvidenceRun
from datetime import datetime, timezone
from pathlib import Path
import csv
import hashlib
import json
import math
import re
import traceback


def main():
    root = Path(__file__).resolve().parents[1]
    intake = root/'source-intake/navier-stokes/20260914'
    destination = intake/'annular-weak-Gram-consistency-final-integrity.json'
    snapshot = intake/'annular-weak-Gram-consistency-resume-snapshot.md'
    executed = intake/'annular-weak-Gram-consistency-executed-sealer.py'
    tables = [intake/('annular-weak-Gram-'+name+'.csv') for name in ['algebra','work','norms','frozen','frozen-norms','hinge-controls','local-atoms']]
    if any(path.exists() for path in [destination,snapshot,executed]+tables):
        raise FileExistsError('Immutable seal destination already exists.')
    report = dict(state='running', checks=[], inputs={}, outputs={}, github_action=False, subagents_used=False,
        valid_for_physics_claim=False, full_GR_limit_proven=False, full_live_P2_force_convergence_proven=False,
        no_new_trajectory_evolution=True, full_nonlinear_stability_proven=False,
        uniform_evolving_refinement_rate_proven=False, original_source_Dirichlet_condition_unchanged=True,
        continuum_mismatch_resolved=False, protected_scan_scope='mtime since2026-09-19T14:39:53Z; not a pre-turn whole-tree hash baseline')
    cache = {}

    def digest(path):
        path = path.resolve()
        if path not in cache:
            hasher = hashlib.sha256()
            with path.open('rb') as stream:
                while chunk := stream.read(1024*1024):
                    hasher.update(chunk)
            cache[path] = hasher.hexdigest()
        return cache[path]

    def own(path, category='inputs'):
        report[category][str(path.resolve().relative_to(root))] = digest(path)

    def save():
        destination.write_text(json.dumps(report, indent=2, allow_nan=False)+'\n', encoding='utf-8')

    def check(name, passed, detail=None):
        report['checks'].append(dict(name=name, passed=bool(passed), detail=detail))
        save()
        if not passed:
            raise RuntimeError(name+': '+repr(detail))

    def inherit(path):
        data = json.loads(path.read_text())
        for category in ['inputs','outputs']:
            for name, expected in data[category].items():
                source = (root/name).resolve()
                key = str(source.relative_to(root))
                if not source.is_file() or digest(source) != expected:
                    raise RuntimeError('Changed sealed source: '+name)
                if key in report['inputs'] and report['inputs'][key] != expected:
                    raise RuntimeError('Conflicting sealed source: '+name)
                report['inputs'][key] = expected
        own(path)
        return data

    save()
    try:
        previous = inherit(intake/'annular-wave-energy-final-integrity.json')
        check('previous_seal_and43failures_preserved', previous['state'] == 'complete'
            and all(row['passed'] for row in previous['checks']) and previous['total_failed_attempts_preserved'] == 43)
        names = ['annular-weak-Gram-algebra-attempt01','annular-live-weak-Gram-transfer-attempt01',
            'annular-frozen-Gram-refinement-attempt01','annular-local-atom-Gram-bounds-attempt01']
        statuses = []
        for name in names:
            status = inherit(intake/name/'status.json')
            statuses.append(status)
            check(name+'_complete_nonclaim_private', status['state'] == 'complete'
                and all(row['passed'] for row in status['checks']) and not status['valid_for_physics_claim']
                and not status['full_GR_limit_proven'] and not status['full_live_P2_force_convergence_proven']
                and not status['github_action'] and not status['subagents_used'])
        failures = []
        for prefix in ['annular-weak-Gram-algebra-','annular-live-weak-Gram-transfer-',
                'annular-frozen-Gram-refinement-','annular-local-atom-Gram-bounds-']:
            for path in sorted(intake.glob(prefix+'*/status.json')):
                if path.parent.name not in names:
                    failed = inherit(path)
                    check(path.parent.name+'_failed_attempt_preserved', failed['state'] == 'failed')
                    failures.append(dict(folder=path.parent.name,error=failed['error']))
        check('no_new_failed_execution', not failures)
        count = sum(len(status['checks']) for status in statuses)
        check('146_successful_implementation_checks', count == 146, count)
        sources = [str((intake/name/'status.json').relative_to(root)) for name in names]
        algebra = [dict(**row,source_path=sources[0],units='synthetic_fixture') for row in statuses[0]['cases']]
        work = [dict(branch=case['branch'],time=case['time'],**row,source_path=sources[1],units='normalized_annular_work')
            for case in statuses[1]['cases'] for row in case['rows']]
        norms = [dict(branch=case['branch'],time=case['time'],**row,source_path=sources[1],units='normalized_annular_norm')
            for case in statuses[1]['cases'] for row in case['norms']]
        frozen = [{**{key:value for key,value in row.items() if key != 'norms'},'source_path':sources[2],'units':'normalized_annular_work'}
            for row in statuses[2]['cases']]
        frozen_norms = [dict(branch=case['branch'],base_count=case['base_count'],field=name,**row,
            source_path=sources[2],units='normalized_annular_norm',valid_for_claim=False)
            for case in statuses[2]['cases'] for name,row in case['norms'].items()]
        controls = [dict(**row,source_path=sources[2],units='synthetic_fixture') for row in statuses[2]['controls']]
        local = [dict(**row,source_path=sources[3],units='normalized_annular_work') for row in statuses[3]['cases']]
        rows_by_table = [algebra,work,norms,frozen,frozen_norms,controls,local]
        check('expected_table_rows', [len(rows) for rows in rows_by_table] == [4,12,16,8,16,3,8])
        for path, rows in zip(tables,rows_by_table):
            with path.open('w',encoding='utf-8',newline='') as stream:
                writer = csv.DictWriter(stream,fieldnames=list(rows[0]))
                writer.writeheader()
                writer.writerows(rows)
            with path.open(encoding='utf-8',newline='') as stream:
                parsed = list(csv.DictReader(stream))
            check(path.name+'_sourced_nonclaim_rows_parse', len(parsed) == len(rows) and all(None not in row
                and row['valid_for_claim'] == 'False' and (root/row['source_path']).is_file() for row in parsed))
            check(path.name+'_numeric_values_finite', all(math.isfinite(value) for row in rows
                for value in row.values() if isinstance(value,(float,int))))
            own(path,'outputs')
        check('actual_both_branches_initial_final', {(case['branch'],case['time']) for case in statuses[1]['cases']}
            == {('reference',0.),('reference',4e-5),('MTS',0.),('MTS',4e-5)}
            and statuses[1]['full_live_geometry_reconstructed'] and statuses[1]['both_nonnested_jump_defects_retained']
            and statuses[1]['mass_adjoint_not_an_assumed_orthogonal_projection'] and statuses[1]['all_Gram_rows_retained'])
        for case in statuses[1]['cases']:
            check(case['branch']+'_'+str(case['time'])+'_partition_and_weak_identity',
                abs(case['rows'][0]['weak_work']-case['rows'][1]['weak_work']-case['rows'][2]['weak_work']) < 1e-20
                and abs(case['direct_load_work']-case['rows'][0]['weak_work']) < 1e-20)
        for row in work:
            check(row['branch']+'_'+str(row['time'])+'_'+row['partition']+'_telescope_and_bounds',
                row['telescope_error'] <= row['numerical_tolerance']
                and abs(row['weak_work']) <= row['row_absolute_bound']+1e-23
                and abs(row['weak_work']) <= row['partition_Cauchy_bound']+1e-23)
        for row in norms:
            check(row['branch']+'_'+str(row['time'])+'_'+row['field']+'_explicit_norm_bounds',
                row['template_row_bound'] <= row['uniform_template_bound']
                and row['Gram_norm'] <= row['discrete_third_difference_bound']+1e-19
                and row['Gram_norm'] <= row['lifted_H1_bound']+1e-19)
        for row in frozen:
            check(row['branch']+'_'+str(row['base_count'])+'_frozen_bounds_and_local_reconstruction',
                abs(row['work']) <= row['fixed_P2_atom_work_bound']+1e-20
                and abs(row['work']) <= row['discrete_third_work_bound']+1e-20
                and abs(row['work']-row['source_work']-row['remaining_work']) < 1e-20)
        for row in local:
            check(row['branch']+'_'+str(row['base_count'])+'_local_atom_bilinear_bound',
                abs(row['work']) <= row['local_atom_work_bound']+1e-24 and row['bilinear_identity_error'] < 1e-20
                and row['arithmetic_bound_allowance'] >= 0.)
        check('fixed_fields_not_evolving_convergence', statuses[2]['frozen_actual_coarse_geometry']
            and statuses[2]['fixed_original_source_jump_not_refitted_on_new_grid']
            and statuses[2]['fixed_P2_consistency_not_uniform_evolving_family_convergence']
            and statuses[3]['floating_residual_measured_not_interval_certified'])
        note = root/'DERIVATION-20260919-weak-Gram-consistency-and-fixed-field-bound.md'
        content = note.read_text(encoding='utf-8')
        cited = re.findall(r'`([^`\r\n]+\.(?:py|md|json|csv))`',content)
        check('all_cited_local_paths_exist', bool(cited) and all((root/name).is_file() for name in cited),cited)
        check('claim_limits_and_nonmonotonicity_disclosed', all(phrase in content for phrase in [
            'does not establish the full GR limit','12.5718%','13.58%','NOT monotone',
            'not a pre-turn whole-tree hash baseline','not146 independent physical validations',
            'not uniform convergence of the actual evolving hierarchy','not interval-arithmetic error certificates']))
        own(note)
        for name in ['annular_weak_Gram_transfer_20260919.py','validate_annular_weak_Gram_transfer_20260919.py',
                'derive_annular_live_weak_Gram_transfer_20260919.py','derive_annular_frozen_Gram_refinement_20260919.py',
                'derive_annular_local_atom_Gram_bounds_20260919.py','seal_annular_weak_Gram_consistency_20260919.py']:
            path = root/'scripts'/name
            compile(path.read_bytes(),str(path),'exec')
            own(path)
        for name in ['coefficients.json','status.json','COMPLETE']:
            own(root/'source-intake/navier-stokes/20260909/sbp4-second-derivative-derived'/name)
        check('sources_compile_without_bytecode', not (root/'scripts/__pycache__').exists())
        protected = root.parent/'formalization-workbench'
        start = datetime(2026,9,19,14,39,53,tzinfo=timezone.utc).timestamp()
        changed = [str(path.relative_to(protected)) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime >= start]
        check('protected_mtime_changed_count_zero', not changed,changed)
        snapshot.write_bytes((root/'CURRENT_LOCAL_RESUME.md').read_bytes())
        executed.write_bytes(Path(__file__).read_bytes())
        own(snapshot,'outputs')
        own(executed,'outputs')
        report.update(state='complete',completed_at=datetime.now(timezone.utc).isoformat(),implementation_checks=count,
            total_failed_attempts_preserved=43+len(failures),new_failures=failures,distinct_files_rehashed=len(cache),
            table_rows=[len(rows) for rows in rows_by_table],full_interval_retested=False,
            next_target='time-dependent compensated derivative-jump budgets and mass-adjoint test regularity using saved states')
        save()
        print(json.dumps(dict(state='complete',implementation_checks=count,integrity_checks=len(report['checks']),
            files_rehashed=len(cache),failed_attempts_preserved=43+len(failures),table_rows=report['table_rows'])),flush=True)
    except Exception as error:
        report.update(state='failed',error=repr(error),traceback=traceback.format_exc())
        save()
        raise


if __name__ == '__main__':
    main()
