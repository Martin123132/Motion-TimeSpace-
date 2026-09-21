from derive_annular_source_gravity_20260914 import EvidenceRun
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json
import re
import traceback


def main():
    root = Path(__file__).resolve().parents[1]
    intake = root/'source-intake/navier-stokes/20260914'
    destination = intake/'annular-curvature-energy-final-integrity.json'
    snapshot = intake/'annular-curvature-energy-resume-snapshot.md'
    executed = intake/'annular-curvature-energy-executed-sealer.py'
    if any(path.exists() for path in [destination,snapshot,executed]):
        raise FileExistsError('Immutable evidence already exists.')
    report = dict(state='running',checks=[],inputs={},outputs={},full_GR_limit_proven=False,
        valid_for_physics_claim=False,continuum_limit_proven=False,uniform_time_bound=False,
        github_action=False,subagents_used=False,implementation_checks_not_physics_passes=True,
        full_time_adjoint_performed=False,original_action_unchanged=True,
        protected_scan_scope='mtime since turn start2026-09-17T13:46:56Z; not a pre-turn full hash baseline')
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

    def own(path,table='inputs'):
        report[table][str(path.resolve().relative_to(root))] = digest(path)

    def save():
        destination.write_text(json.dumps(report,indent=2,allow_nan=False)+'\n',encoding='utf-8')

    def check(name,passed,detail=None):
        report['checks'].append(dict(name=name,passed=bool(passed),detail=detail))
        save()
        if not passed:
            raise RuntimeError(name+': '+repr(detail))

    def inherit(status):
        for table in ['inputs','outputs']:
            for name,expected in status[table].items():
                path = (root/name).resolve()
                key = str(path.relative_to(root))
                if not path.is_file() or digest(path)!=expected:
                    raise RuntimeError('Missing or changed immutable file: '+name)
                if key in report['inputs'] and report['inputs'][key]!=expected:
                    raise RuntimeError('Conflicting immutable file: '+name)
                report['inputs'][key] = expected

    save()
    try:
        previous_path = intake/'annular-source-refinement-final-integrity.json'
        previous = json.loads(previous_path.read_text())
        check('previous_seal_complete',previous['state']=='complete' and all(row['passed'] for row in previous['checks']))
        inherit(previous)
        own(previous_path)
        specifications = [('kernel','annular-curvature-kernel-attempt01',54,6),
            ('energy','annular-canonical-energy-attempt01',193,24),
            ('duality','annular-energy-duality-attempt01',41,8),
            ('remainder','annular-energy-remainder-scaling-attempt01',16,8)]
        statuses,counts = {},{}
        for name,label,count,cases in specifications:
            path = intake/label/'status.json'
            status = json.loads(path.read_text())
            json.dumps(status,allow_nan=False)
            check(name+'_complete',status['state']=='complete' and len(status['checks'])==count
                and len(status['cases'])==cases and all(row['passed'] for row in status['checks']))
            check(name+'_scope',not status['full_GR_limit_proven'] and not status['valid_for_physics_claim']
                and not status['complete_parent_source_action_derived'] and status['original_action_unchanged']
                and not status['finite_future_trajectories_read'] and not status['interval_arithmetic'])
            inherit(status)
            own(path)
            statuses[name],counts[name] = status,count
        kernel,energy,duality,remainder = [statuses[name] for name in ['kernel','energy','duality','remainder']]
        check('kernel_not_endpoint_Taylor_or_force_repair',not kernel['endpoint_Taylor_truncation_used']
            and kernel['floating_slope_moments_retained'] and not kernel['force_correction'] and not kernel['force_fit']
            and all(not row['full_GR_gate_upgraded'] for row in kernel['cases']))
        fine = next(row for row in kernel['cases'] if row['degree']==768 and row['count']==1025)
        check('old_wrong_sign_preserved_new_identity_qualified',fine['actual_source_force_at_021']>0
            and fine['kernel_source_force_at_021']>0 and fine['failed_endpoint_source_force_at_021']<0
            and fine['maximum_source_force_error']<2e-11)
        check('energy_not_uniform_certificate',not energy['uniform_dynamical_stability_proven']
            and not energy['nonlinear_remainder_bound_uniform_in_mesh'] and energy['finite_sample_diagnostics_only']
            and energy['reference_residual_coordinate_correction_retained'] and energy['metric_source_shift_beta']==1.
            and {row['branch'] for row in energy['cases']}=={'reference','MTS'}
            and all(row['beta_positive_threshold']<1. for row in energy['cases']))
        check('duality_not_completed_adjoint',not duality['full_time_adjoint_performed']
            and not duality['uniform_output_continuity_proven'] and not duality['continuum_regularities_established']
            and len(duality['C2_not_C3_cases'])==7)
        check('remainder_shortcut_rejected_symmetrically',not remainder['uniform_basic_energy_quadratic_remainder_claimed']
            and not remainder['physical_instability_claimed']
            and {row['branch'] for row in remainder['cases']}=={'reference','MTS'})
        check('earlier_failures_preserved',previous['inherited_failed_attempts_preserved']==25
            and previous['original_failed_cases_preserved'])
        note = root/'DERIVATION-20260917-finite-width-curvature-and-coupled-energy.md'
        content = note.read_text(encoding='utf-8')
        cited = re.findall(r'`([^`\r\n]+\.(?:py|md|json))`',content)
        check('cited_note_paths_exist',all((root/name).is_file() for name in cited),cited)
        check('finished_note_scoped','PENDING' not in content and 'not the full GR limit' in content
            and 'NOT been proved' in content and '304 successful implementation checks' in content)
        own(note)
        names = ['annular_finite_width_curvature_20260917.py','qualify_annular_curvature_kernel_20260917.py',
            'annular_canonical_energy_20260917.py','qualify_annular_canonical_energy_20260917.py',
            'qualify_annular_energy_duality_20260917.py','qualify_annular_energy_remainder_scaling_20260917.py',
            'seal_annular_curvature_energy_20260917.py']
        for name in names:
            path = root/'scripts'/name
            compile(path.read_bytes(),str(path),'exec')
            own(path)
        check('new_sources_compile',True,names)
        check('script_bytecode_cache_absent',not (root/'scripts/__pycache__').exists())
        protected = root.parent/'formalization-workbench'
        started = datetime(2026,9,17,13,46,56,tzinfo=timezone.utc).timestamp()
        changed = [str(path.relative_to(protected)) for path in protected.rglob('*')
            if path.is_file() and path.stat().st_mtime>=started]
        check('protected_workbench_mtime_changed_count_zero',not changed,changed)
        snapshot.write_bytes((root/'CURRENT_LOCAL_RESUME.md').read_bytes())
        executed.write_bytes(Path(__file__).read_bytes())
        own(snapshot,'outputs')
        own(executed,'outputs')
        check('resume_and_executed_source_preserved',True)
        report.update(state='complete',completed_at=datetime.now(timezone.utc).isoformat(),
            current_suite_checks=counts,total_successful_current_checks=sum(counts.values()),
            distinct_files_rehashed=len(cache),inherited_failed_attempts_preserved=25,
            new_failed_attempts_preserved=[],original_failed_cases_preserved=True,
            kernel_results=kernel['cases'],energy_results=energy['cases'],duality_results=duality['cases'],
            nonlinear_shortcut_diagnostics=remainder['cases'],
            full_width_curvature_identity_qualified=True,conditional_C2_consistency_derived=True,
            conditional_linear_energy_lemma_not_parent_certificate=True,
            nonlinear_basic_energy_shortcut_rejected=True)
        save()
        print(json.dumps(dict(state='complete',checks=len(report['checks']),current_checks=sum(counts.values()),
            rehashed_files=len(cache),protected_changed=len(changed),failed_attempts_preserved=25)),flush=True)
    except Exception as error:
        report.update(state='failed',error=repr(error),traceback=traceback.format_exc())
        save()
        raise


if __name__=='__main__':
    main()
