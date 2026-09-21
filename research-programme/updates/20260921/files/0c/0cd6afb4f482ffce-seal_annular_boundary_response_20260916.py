import hashlib
import json
import re
import traceback
from datetime import datetime, timezone
from pathlib import Path
from navier_stokes_source_audit_20260908 import limit_process


def main():
    limit_process()
    root = Path(__file__).resolve().parents[1]
    intake = root/'source-intake/navier-stokes/20260914'
    destination = intake/'annular-boundary-response-final-integrity.json'
    snapshot = intake/'annular-boundary-response-resume-snapshot.md'
    executed = intake/'annular-boundary-response-executed-sealer.py'
    if any(path.exists() for path in [destination, snapshot, executed]):
        raise FileExistsError('Seals and executed evidence are immutable.')
    report = dict(state='running', checks=[], inputs={}, outputs={}, full_GR_limit_proven=False,
                  valid_for_physics_claim=False, complete_parent_source_action_derived=False,
                  moving_source_force_problem_solved=False, relaxed_action_dynamically_validated=False,
                  github_action=False, subagents_used=False,
                  protected_scan_scope='mtime since 2026-09-16T08:58:15Z, not a pre-turn full hash baseline')
    cache = {}

    def digest(path):
        path = path.resolve()
        if path not in cache:
            value = hashlib.sha256()
            with path.open('rb') as stream:
                while chunk := stream.read(1024*1024):
                    value.update(chunk)
            cache[path] = value.hexdigest()
        return cache[path]

    def own(path, table='inputs'):
        report[table][str(path.resolve().relative_to(root))] = digest(path)

    def save():
        destination.write_text(json.dumps(report, indent=2, allow_nan=False)+'\n', encoding='utf-8')

    def check(name, passed, detail=None):
        report['checks'].append(dict(name=name, passed=bool(passed), detail=detail))
        save()
        if not passed:
            raise RuntimeError(name+': '+repr(detail))

    def inherit(status):
        for table in ['inputs', 'outputs']:
            for name, expected in status[table].items():
                path = (root/name).resolve()
                normalized = str(path.relative_to(root))
                if not path.is_file() or digest(path)!=expected:
                    raise RuntimeError('Missing or altered immutable evidence: '+name)
                if normalized in report['inputs'] and report['inputs'][normalized]!=expected:
                    raise RuntimeError('Conflicting evidence digest: '+name)
                report['inputs'][normalized] = expected

    save()
    try:
        previous_path = intake/'annular-boundary-capacity-final-integrity.json'
        previous = json.loads(previous_path.read_text())
        check('previous_checkpoint_complete', previous['state']=='complete' and all(row['passed'] for row in previous['checks']))
        inherit(previous)
        own(previous_path)
        statuses, counts = {}, {}
        for label, folder, count in [
            ('dynamic', 'annular-boundary-dynamic-response-attempt02', 93),
            ('domain', 'annular-trace-domain-and-inertia-attempt02', 82),
            ('susceptibility', 'annular-trace-susceptibility-attempt02', 38),
            ('relaxation', 'annular-relaxed-trace-action-attempt01', 44)]:
            path = intake/folder/'status.json'
            status = json.loads(path.read_text())
            json.dumps(status, allow_nan=False)
            check(label+'_complete', status['state']=='complete' and len(status['checks'])==count and all(row['passed'] for row in status['checks']))
            check(label+'_broad_claims_false', not status['full_GR_limit_proven'] and not status['valid_for_physics_claim'] and not status['complete_parent_source_action_derived'])
            inherit(status)
            own(path)
            statuses[label], counts[label] = status, count
        failures = ['annular-boundary-dynamic-response-attempt01', 'annular-trace-domain-and-inertia-attempt01', 'annular-trace-susceptibility-attempt01']
        for folder in failures:
            path = intake/folder/'status.json'
            status = json.loads(path.read_text())
            check(folder+'_preserved', status['state']=='failed')
            inherit(status)
            own(path)
        dynamic = statuses['dynamic']
        check('moving_decomposition_covers_both_branches_and_all_saved_times',
              {(row['count'], row['branch']) for row in dynamic['cases']}=={(count, branch) for count in [257, 513] for branch in ['reference', 'MTS']}
              and all(len(row['trajectory'])==9 for row in dynamic['cases']))
        check('causal_controls_cover_both_branches', len(dynamic['frozen_controls'])==8
              and all(row['prescribed_source'] and row['retarded_state_error']<2e-10 for row in dynamic['frozen_controls']))
        check('moving_reduced_solver_not_overclaimed', not dynamic['moving_source_reduced_memory_solver_implemented'] and not dynamic['static_trace_constraint_imposed'])
        domain = statuses['domain']
        check('domain_claim_has_fixed_stencil_and_topology_limits', domain['bare_bulk_nonclosability_requires_fixed_nonzero_Gram_stiffness']
              and domain['admissible_completion_in_augmented_domain_not_ruled_out'] and not domain['simultaneous_base_grid_limit_proven']
              and not domain['full_parent_theory_rejected'])
        check('spectral_matrix_preserves_reference_and_MTS', len(domain['cases'])==24
              and {(row['count'], row['source_splits'], row['branch']) for row in domain['cases']}
              =={(count, splits, branch) for count in [257, 513] for splits in [2, 4, 8, 16, 32, 64] for branch in ['reference', 'MTS']})
        check('diagnostic_rounding_correction_does_not_modify_old_evolution', not domain['existing_evolution_action_changed']
              and domain['original_analytic_formula_tolerances_preserved'] and len(domain['quadrature_coordinate_rounding'])==24)
        susceptibility = statuses['susceptibility']
        check('trace_response_has_no_fitted_coefficient_or_force_pass', not susceptibility['fitted_response_coefficients']
              and not susceptibility['moving_source_force_problem_solved'] and susceptibility['original_Gram_terms_retained'])
        check('static_attenuation_valid_and_distinct_from_evolved_trace', all(0<row['static_attenuation']<1
              and row['no_claim_actual_trajectory_is_static'] for row in susceptibility['cases']) and len(susceptibility['cases'])==6)
        relaxation = statuses['relaxation']
        check('relaxation_is_static_and_not_a_parent_uniqueness_claim', not relaxation['unique_parent_action_derived']
              and not relaxation['moving_time_evolution_of_relaxed_action_tested'] and not relaxation['dynamic_convergence_to_relaxation_proven']
              and not relaxation['finite_trajectory_changed'] and not relaxation['finite_unrelaxed_action_changed'])
        check('recovery_sequences_preserved', len(relaxation['cases'])==2 and all(len(row['recovery_sequence'])==6 for row in relaxation['cases']))
        check('prior_force_failures_preserved', all(not row['strict_force_gate'] for row in previous['refinement_results'] if row['branch']=='MTS'))
        note = root/'DERIVATION-20260916-boundary-memory-and-trace-domain-completion.md'
        content = note.read_text(encoding='utf-8')
        cited = re.findall(r'`([^`\r\n]+\.(?:py|md|json))`', content)
        check('cited_local_paths_exist', all((root/name).is_file() for name in cited), cited)
        check('note_distinguishes_auxiliary_trace_from_bulk_derivative', 'auxiliary eta is not automatically the derivative trace' in content
              and 'not a full GR limit' in content and 'not a sufficient well-posedness theorem' in content)
        check('external_acquisition_limit_recorded', all(url in content for url in domain['source_urls']) and 'direct PDF opens timed out' in content)
        own(note)
        modules = ['annular_boundary_response_20260916.py', 'verify_annular_boundary_response_20260916.py',
                   'verify_annular_boundary_response_20260916_v2.py', 'derive_annular_trace_domain_20260916.py',
                   'derive_annular_trace_domain_20260916_v2.py', 'derive_annular_trace_susceptibility_20260916.py',
                   'derive_annular_trace_susceptibility_20260916_v2.py', 'verify_annular_relaxed_trace_action_20260916.py',
                   'seal_annular_boundary_response_20260916.py']
        for name in modules:
            path = root/'scripts'/name
            compile(path.read_bytes(), str(path), 'exec')
            own(path)
        check('new_modules_compile_without_bytecode', True, modules)
        check('script_bytecode_cache_absent', not (root/'scripts/__pycache__').exists())
        protected = root.parent/'formalization-workbench'
        started = datetime(2026, 9, 16, 8, 58, 15, tzinfo=timezone.utc).timestamp()
        changed = [str(path.relative_to(protected)) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime>=started]
        check('protected_workbench_mtime_changed_count_zero', not changed, changed)
        snapshot.write_bytes((root/'CURRENT_LOCAL_RESUME.md').read_bytes())
        executed.write_bytes(Path(__file__).read_bytes())
        own(snapshot, 'outputs')
        own(executed, 'outputs')
        check('resume_and_executed_sealer_preserved', True)
        report.update(state='complete', completed_at=datetime.now(timezone.utc).isoformat(), current_suite_checks=counts,
                      total_successful_current_checks=sum(counts.values()), distinct_files_rehashed=len(cache),
                      inherited_failed_attempts_preserved=previous['inherited_failed_attempts_preserved']+len(failures),
                      implementation_checks_not_physics_passes=True)
        save()
        print(json.dumps(dict(state='complete', checks=len(report['checks']), current_checks=sum(counts.values()),
                              rehashed_files=len(cache), protected_changed=len(changed))), flush=True)
    except Exception as error:
        report.update(state='failed', error=repr(error), traceback=traceback.format_exc())
        save()
        raise


if __name__=='__main__':
    main()
