import hashlib
import json
import re
import traceback
from datetime import datetime, timezone
from pathlib import Path
from navier_stokes_source_audit_20260908 import limit_process


def main():
    limit_process()
    root=Path(__file__).resolve().parents[1]
    intake=root/'source-intake/navier-stokes/20260914'
    destination=intake/'annular-source-gravity-final-integrity.json'
    snapshot=intake/'annular-source-gravity-resume-snapshot.md'
    executed=intake/'annular-source-gravity-executed-sealer.py'
    if any(path.exists() for path in [destination,snapshot,executed]):
        raise FileExistsError('Preserve every previous executed attempt.')
    report=dict(state='running',checks=[],inputs={},outputs={},
                live_source_only_gravity_evolved=True,
                source_force_from_action_with_live_radial_constraints=True,
                material_mass_conservation_imposed=False,
                identical_zero_scalar_reference_MTS_sector=True,
                dust_width_crossing_law_conditionally_derived=True,
                dust_caustic_not_an_MTS_specific_failure=True,
                nonzero_scalar_radial_embedding_covectors_derived=True,
                full_scalar_gravity_coupling_evolved=False,
                complete_parent_source_action_derived=False,
                physical_material_width_or_mass_derived=False,
                full_GR_limit_proven=False,valid_for_physics_claim=False,
                weak_thin_shell_limit_ruled_out=False,
                github_action=False,subagents_used=False,
                resource_policy='Sequential BelowNormal single-core numerical workers; no unrelated process changed.',
                protected_scan_scope='mtime since2026-09-14T22:37:14Z, not a pre-turn content hash baseline.')

    def save():
        destination.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')

    def own(path,table='inputs'):
        report[table][str(path.relative_to(root))]=hashlib.sha256(path.read_bytes()).hexdigest()

    def check(name,passed,detail=None):
        report['checks'].append(dict(name=name,passed=bool(passed),detail=detail))
        save()
        if not passed:
            raise RuntimeError(name+': '+repr(detail))

    def inherit(status):
        for table in ['inputs','outputs']:
            for filename,expected in status[table].items():
                path=root/filename
                if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest()!=expected:
                    raise RuntimeError('Missing or changed evidence: '+filename)
                if filename in report['inputs'] and report['inputs'][filename]!=expected:
                    raise RuntimeError('Conflicting evidence hash: '+filename)
                report['inputs'][filename]=expected

    save()
    try:
        previous=intake/'annular-moving-collar-final-integrity.json'
        old=json.loads(previous.read_text())
        check('previous_moving_collar_seal_complete',
              old['state']=='complete' and all(row['passed'] for row in old['checks']))
        inherit(old)
        own(previous)
        statuses={}
        counts={}
        for label,folder,count in [
            ('source_gravity_algebra','annular-source-gravity-algebra-attempt01',12),
            ('live_source_gravity','annular-source-gravity-evolution-attempt01',24),
            ('dust_width_focusing','annular-source-gravity-focusing-attempt01',39),
            ('lapse_limit_algebra','annular-source-gravity-limit-algebra-attempt01',9),
            ('curved_scalar_radial_embedding','annular-moving-curved-radial-assembly-attempt01',39)]:
            path=intake/folder/'status.json'
            status=json.loads(path.read_text())
            check(label+'_complete',status['state']=='complete' and len(status['checks'])==count and
                  all(row['passed'] for row in status['checks']))
            check(label+'_broad_claims_false',not status['full_GR_limit_proven'] and
                  not status['complete_parent_source_action_derived'] and not status['valid_for_physics_claim'])
            inherit(status)
            own(path)
            statuses[label]=status
            counts[label]=count
        gravity=statuses['live_source_gravity']
        check('live_gravity_not_prescribed_mass',gravity['source_force_from_live_metric'] and
              not gravity['material_mass_or_ADM_energy_imposed'] and not gravity['full_scalar_gravity_coupling_evolved'])
        focusing=statuses['dust_width_focusing']
        check('crossing_has_GR_and_resolution_controls',
              len(focusing['cases'])==9 and abs(focusing['measured_thin_width_exponent']-.5)<.01 and
              all(row['physical_evolution_stopped_at_crossing'] for row in focusing['cases']))
        assembly=statuses['curved_scalar_radial_embedding']
        check('four_full_factor_curved_cases_not_evolution',
              len(assembly['cases'])==4 and not assembly['live_curved_evolution_completed'] and
              not assembly['temporal_canonical_current_evolution_checked'])
        stems=['annular_source_gravity_collar','derive_annular_source_gravity',
               'run_annular_source_gravity','run_annular_source_gravity_focusing',
               'derive_annular_source_gravity_limit','derive_annular_moving_curved_radial_assembly',
               'seal_annular_source_gravity']
        for stem in stems:
            path=root/'scripts'/(stem+'_20260914.py')
            compile(path.read_bytes(),str(path),'exec')
            own(path)
        check('seven_sources_compile_without_bytecode',True)
        executed.write_bytes(Path(__file__).read_bytes())
        own(executed,'outputs')
        note=root/'DERIVATION-20260914-live-source-gravity-and-dust-width-limit.md'
        document=note.read_text(encoding='utf-8')
        cited=[root/value for value in re.findall(r'\x60([^\x60]+)\x60',document)
               if value.endswith(('.md','.py','.json','.npz','.csv'))]
        check('every_local_citation_exists',bool(cited) and all(path.is_file() for path in cited),len(cited))
        check('no_pending_result_marker','RESULTS_PENDING' not in document)
        for path in cited:
            own(path)
        own(note,'outputs')
        source_path=intake/'annular-source-gravity-external-source-notes.json'
        source=json.loads(source_path.read_text())
        urls=re.findall(r'https://[^)\s]+',document)
        check('external_primary_source_recorded',urls==[source['source_url']] and
              source['paper_year']==1985 and source['quote_words']==0 and not source['valid_for_physics_claim'])
        own(source_path)
        protected=root.parent/'formalization-workbench'
        check('protected_workbench_exists',protected.is_dir())
        start=datetime.fromisoformat('2026-09-14T22:37:14+00:00').timestamp()
        changed=[str(path) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime>start]
        check('protected_workbench_mtime_changed_count_zero',not changed,changed)
        check('no_script_bytecode_cache',not (root/'scripts/__pycache__').exists())
        snapshot.write_bytes((root/'CURRENT_LOCAL_RESUME.md').read_bytes())
        own(snapshot,'outputs')
        report.update(state='complete',validation_counts=counts,total_validation_checks=sum(counts.values()),
                      source_gravity_finest=gravity['cases'][3],
                      width_limit_constant=statuses['lapse_limit_algebra']['derived_limit_constant'],
                      width_exponent=focusing['measured_thin_width_exponent'],
                      protected_changed_count=len(changed),completed_at=datetime.now(timezone.utc).isoformat())
        save()
        print(json.dumps(dict(state=report['state'],checks=len(report['checks']),validation_counts=counts,
                              distinct_files=len(set(report['inputs'])|set(report['outputs'])),
                              protected_changed_count=len(changed))),flush=True)
    except Exception as error:
        report.update(state='failed',error=repr(error),traceback=traceback.format_exc())
        save()
        raise


if __name__=='__main__':
    main()

