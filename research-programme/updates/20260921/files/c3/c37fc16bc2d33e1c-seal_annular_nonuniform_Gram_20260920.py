from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_nonuniform_Gram_candidate_20260920 import template_rows
from datetime import datetime, timezone
from decimal import Decimal, getcontext
from fractions import Fraction
from pathlib import Path
import csv
import hashlib
import json
import re
import traceback
import numpy as np


def main():
    getcontext().prec = 80
    root = Path(__file__).resolve().parents[1]
    intake = root/'source-intake/navier-stokes/20260914'
    destination = intake/'annular-nonuniform-Gram-final-integrity.json'
    executed = intake/'annular-nonuniform-Gram-executed-sealer.py'
    snapshot = intake/'annular-nonuniform-Gram-resume-snapshot.md'
    table_labels = ['uniform-recovery', 'variations', 'fixed-field-bounds', 'parent-meshes',
        'qualified-pairs', 'precision-refinement', 'stable-atoms', 'geometry-sources']
    tables = [intake/('annular-nonuniform-Gram-'+label+'.csv') for label in table_labels]
    if any(path.exists() for path in [destination, executed, snapshot]+tables):
        raise FileExistsError('Immutable seal destination already exists.')
    report = dict(state='running', checks=[], inputs={}, outputs={}, github_action=False, subagents_used=False,
        no_new_evolution=True, original_live_action_unchanged=True, candidate_only=True,
        valid_for_physics_claim=False, full_GR_limit_proven=False,
        full_live_P2_force_convergence_proven=False, certified_continuous_time_bound=False,
        physical_force_mismatch_fixed=False, actual_time_integrated_force_test=False,
        nonuniform_parent_uniqueness_proven=False, evolving_front_resolution_proven=False,
        protected_scan_scope='mtime since2026-09-20T14:48:24Z; not a pre-turn whole-tree hash baseline')
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
        for category in ['inputs', 'outputs']:
            for name, expected in data[category].items():
                source = (root/name).resolve()
                key = str(source.relative_to(root))
                if not source.is_file() or digest(source) != expected:
                    raise RuntimeError('Changed sealed source: '+name)
                if key in report['inputs'] and report['inputs'][key] != expected:
                    raise RuntimeError('Conflicting source: '+name)
                report['inputs'][key] = expected
        own(path)
        return data

    save()
    try:
        previous = inherit(intake/'annular-trace-aware-Gram-final-integrity.json')
        check('previous_seal_preserved', previous['state'] == 'complete'
            and all(row['passed'] for row in previous['checks']) and previous['trace_aware_Gram_force_qualified']
            and not previous['physical_force_mismatch_fixed'])
        names = ['annular-nonuniform-Gram-controls-attempt01', 'annular-nonuniform-Gram-parent-probes-attempt02',
            'annular-nonuniform-Gram-precision-attempt01', 'annular-nonuniform-Gram-atoms-attempt02']
        statuses = [inherit(intake/name/'status.json') for name in names]
        for name, status in zip(names, statuses):
            check(name+'_complete_nonclaim', status['state'] == 'complete' and all(row['passed'] for row in status['checks'])
                and not status['valid_for_physics_claim'] and not status['full_GR_limit_proven']
                and not status['full_live_P2_force_convergence_proven'] and not status['certified_continuous_time_bound']
                and not status['physical_force_mismatch_fixed'] and status['no_new_evolution'] and status['original_live_action_unchanged']
                and status['candidate_only'] and not status['nonuniform_parent_uniqueness_proven']
                and not status['github_action'] and not status['subagents_used'])
        controls, probes, precision, atoms = statuses
        failed_names = ['annular-nonuniform-Gram-parent-probes-attempt01', 'annular-nonuniform-Gram-atoms-attempt01']
        for name in failed_names:
            failed = inherit(intake/name/'status.json')
            check(name+'_failure_preserved_not_promoted', failed['state'] == 'failed'
                and any(not row['passed'] for row in failed['checks']) and not failed['valid_for_physics_claim'])
        check('primary_uniform_recovery_and_variation', controls['uniform_recovery_qualified'] and controls['variation_qualified'])
        check('nonuniqueness_witness_not_fitted', controls['nonuniqueness']['same_ideal_uniform_rule']
            and controls['nonuniqueness']['both_positive'] and controls['nonuniqueness']['witness_not_a_fitted_physics_parameter']
            and controls['nonuniqueness']['primary_energy'] != controls['nonuniqueness']['alternative_energy'])
        check('original_frozen_geometry_retained_both_branches', len(probes['sources']) == 2
            and all(row['coefficient_reproduction_error'] == 0 for row in probes['sources']))
        reference_rows = [row for row in probes['cases'] if row['branch'] == 'reference']
        check('reference_Gram_baseline_exact_zero', len(reference_rows) == 16 and all(Decimal(row['bilinear']) == 0
            and Decimal(row['trial_energy']) == 0 and Decimal(row['test_energy']) == 0 for row in reference_rows))
        check('precision_refinement_not_physical_accuracy', precision['fixed_profile_arithmetic_qualified']
            and precision['float_pilot_superseded_for_signed_pairs'] and len(precision['refinement']) == 16
            and all(Decimal(row['absolute_bilinear_change']) < Decimal(row['arithmetic_gate'])
                and row['not_a_physical_force_gate'] for row in precision['refinement']))
        check('local_atom_evaluator_qualified', atoms['stable_fixed_profile_kernel_qualified']
            and atoms['atom_preparation_digits'] == 72 and len(atoms['cases']) == 16
            and all(Decimal(row['absolute_error']) <= Decimal(row['arithmetic_gate']) for row in atoms['cases']))
        check('saved_profiles_not_evolving_front_certificate', probes['fixed_saved_profile_probe_complete']
            and not probes['actual_time_integrated_force_test'] and not probes['evolving_front_resolution_proven'])
        constant = float(Fraction(59097, 573104)+2*Fraction(3, 392)+Fraction(1, 392))
        for count in sorted(set(row['count'] for row in probes['meshes'])):
            template, unused = template_rows(count)
            norm_bound = float(np.max(np.asarray(abs(template.T @ template).sum(axis=1))))
            check('sourced_template_norm_'+str(count), norm_bound <= constant+3e-15, norm_bound)
        qualified_rows = [row for row in precision['cases'] if row['digits'] == 72]
        pairs = [dict(**row, source_path=str((intake/names[2]/'status.json').relative_to(root))) for row in qualified_rows]
        pairs += [dict(**row, source_path=str((intake/names[1]/'status.json').relative_to(root))) for row in reference_rows]
        rows_by_table = [controls['uniform'], controls['variations'], controls['refinements'], probes['meshes'],
            pairs, precision['refinement'], atoms['cases'], probes['sources']]
        source_indices = [0, 0, 0, 1, None, 2, 3, 1]
        for path, rows, source_index in zip(tables, rows_by_table, source_indices):
            sourced = rows if source_index is None else [dict(**row,
                source_path=str((intake/names[source_index]/'status.json').relative_to(root))) for row in rows]
            fields = list(dict.fromkeys(key for row in sourced for key in row))
            with path.open('w', encoding='utf-8', newline='') as stream:
                writer = csv.DictWriter(stream, fieldnames=fields)
                writer.writeheader()
                writer.writerows(sourced)
            with path.open(encoding='utf-8', newline='') as stream:
                parsed = list(csv.DictReader(stream))
            check(path.name+'_sourced_nonclaim_rows_parse', len(parsed) == len(rows) and all(None not in row
                and row['valid_for_claim'] == 'False' and (root/row['source_path']).is_file() for row in parsed))
            own(path, 'outputs')
        note = root/'DERIVATION-20260920-nonuniform-Gram-action-and-stable-atoms.md'
        content = note.read_text(encoding='utf-8')
        cited = re.findall(r'`([^`\r\n]+\.(?:py|md|json|csv))`', content)
        check('completed_report_and_cited_paths', 'RESULTS_PENDING' not in content and bool(cited)
            and all((root/name).is_file() for name in cited), cited)
        for name in cited:
            own(root/name)
        own(note)
        for name in ['annular_nonuniform_Gram_candidate_20260920.py', 'validate_annular_nonuniform_Gram_20260920.py',
                'probe_annular_nonuniform_Gram_parent_20260920.py', 'probe_annular_nonuniform_Gram_parent_v2_20260920.py',
                'qualify_annular_nonuniform_Gram_precision_20260920.py', 'derive_annular_nonuniform_Gram_atoms_20260920.py',
                'derive_annular_nonuniform_Gram_atoms_v2_20260920.py', 'seal_annular_nonuniform_Gram_20260920.py']:
            path = root/'scripts'/name
            compile(path.read_bytes(), str(path), 'exec')
            own(path)
        check('sources_compile_without_bytecode', not (root/'scripts/__pycache__').exists())
        protected = root.parent/'formalization-workbench'
        start = datetime(2026, 9, 20, 14, 48, 24, tzinfo=timezone.utc).timestamp()
        changed = [str(path.relative_to(protected)) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime >= start]
        check('protected_workbench_mtime_unchanged', not changed, changed)
        snapshot.write_bytes((root/'CURRENT_LOCAL_RESUME.md').read_bytes())
        executed.write_bytes(Path(__file__).read_bytes())
        own(snapshot, 'outputs')
        own(executed, 'outputs')
        report.update(state='complete', completed_at=datetime.now(timezone.utc).isoformat(),
            implementation_checks=sum(len(status['checks']) for status in statuses),
            implementation_check_breakdown={name:len(status['checks']) for name, status in zip(names, statuses)},
            total_failed_attempts_preserved=previous['total_failed_attempts_preserved']+len(failed_names),
            new_failures=failed_names, distinct_files_rehashed=len(cache), table_rows=[len(rows) for rows in rows_by_table],
            primary_variational_candidate_qualified=True, stable_fixed_profile_kernel_qualified=True,
            next_target='Assemble the complete candidate frozen action on the common P2 space, including unchanged mass/gradient and correct source/coefficient variation. Qualify against the stable atom form, estimate unfiltered frequencies, then short frozen-response pilots in both branches with extension sensitivity; no long live run yet.')
        save()
        print(json.dumps(dict(state='complete', checks=report['implementation_checks'], integrity_checks=len(report['checks']),
            files_rehashed=len(cache), table_rows=report['table_rows'], failures_preserved=report['total_failed_attempts_preserved'])), flush=True)
    except Exception as error:
        report.update(state='failed', error=repr(error), traceback=traceback.format_exc())
        save()
        raise


if __name__ == '__main__':
    main()

