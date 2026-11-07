from __future__ import annotations

import re
from precision_common import *


def main():
    modest()
    output=ROOT/'results/stage-integrity.json'
    assert not output.exists()
    seals=list(BRANCH.glob('*/results/stage-integrity.json'))+[BRANCH/'results/stage-integrity.json']
    by_hash={digest(path):path for path in seals}
    cursor=PARENT/'results/stage-integrity.json'
    parent=json.loads(cursor.read_text())
    seen=set()
    prior_count=0
    while True:
        assert cursor not in seen
        seen.add(cursor)
        report=json.loads(cursor.read_text())
        assert report['state']=='complete'
        base=POST if cursor==BRANCH/'results/stage-integrity.json' else cursor.parent.parent
        for relative,expected in report['file_hashes'].items():
            assert digest(base/relative)==expected,base/relative
        prior_count+=len(report['file_hashes'])
        if cursor==BRANCH/'results/stage-integrity.json':
            break
        links=[report[key] for key in ['parent_seal_sha256','previous_seal_sha256'] if key in report]
        assert len(links)==1 and links[0] in by_hash
        cursor=by_hash[links[0]]
    assert prior_count==6842,prior_count
    checkpoint=POST/'_checkpoints/20261003-pre-condensate-origin/manifest.json'
    original=POST/'.venv-score/Lib/site-packages/camb/cambdll.dll'
    native_library=NATIVE/'camb/cambdll.dll'
    assert digest(checkpoint)==parent['checkpoint_manifest_sha256']
    assert digest(original)==parent['original_library_sha256']
    assert digest(native_library)==parent['native_library_sha256']
    for source in parent['local_source_documents']+parent['primary_pdfs']:
        assert digest(source['path'])==source['sha256']
    scripts=list(ROOT.glob('*.py'))
    for path in scripts:
        compile(path.read_bytes(),str(path),'exec')
    script_hashes={digest(path) for path in scripts}
    packets=list(ROOT.glob('results/*/status.json'))+list(ROOT.glob('runs/*/status.json'))
    assert len(packets)==15,len(packets)
    for path in packets:
        packet=json.loads(path.read_text())
        assert packet['state']=='complete' and packet['script_sha256'] in script_hashes
        assert (path.parent/'COMPLETE').is_file()
        for source,expected in packet['input_hashes'].items():
            assert digest(source)==expected,(path,source)
    validation=json.loads((ROOT/'results/validation/status.json').read_text())
    assert validation['all_checks_passed'] and all(row['passed'] for row in validation['checks'])
    spectrum=json.loads((ROOT/'results/spectrum/status.json').read_text())
    empirical=json.loads((ROOT/'results/primary-refit/status.json').read_text())
    low_k=json.loads((ROOT/'results/low-k-domain/status.json').read_text())
    assert low_k['all_checks_passed'] and all(row['passed'] for row in low_k['checks'])
    production=json.loads((ROOT/'results/production-spectrum/status.json').read_text())
    production_fit=json.loads((ROOT/'results/production-primary-refit/status.json').read_text())
    for report in [production,production_fit]:
        assert report['all_checks_passed'] and all(row['passed'] for row in report['checks'])
    total_checks=validation['count']+len(low_k['checks'])+len(production['checks'])+len(production_fit['checks'])
    assert len(empirical['rows'])==12
    assert all(row['all_converged'] and not row['any_edge'] for row in empirical['summaries'])
    assert not empirical['field_parameters_refitted']
    citations=set()
    for path in ROOT.glob('*.md'):
        for reference in re.findall(r'`([^`\n]+)`',path.read_text(encoding='utf-8')):
            if reference.endswith(('.md','.py','.npz','.json','.html')):
                target=(ROOT/reference).resolve()
                assert target==output or target.is_file(),(path,reference)
                if target!=output:
                    citations.add(str(target))
    started=datetime(2026,10,7,4,40,55,tzinfo=timezone.utc)
    workbench=POST.parent/'formalization-workbench'
    changed=[str(path) for path in workbench.rglob('*') if path.is_file() and path.stat().st_mtime>started.timestamp()]
    assert workbench.is_dir() and not changed,changed
    hashes={}
    for directory,directories,files in os.walk(ROOT):
        assert '__pycache__' not in directories,directory
        for name in sorted(files):
            path=Path(directory)/name
            if path!=output:
                hashes[path.relative_to(ROOT).as_posix()]=digest(path)
    write_json(output,dict(state='complete',sealed_at_utc=datetime.now(timezone.utc).isoformat(),
        file_hashes=hashes,parent_seal_sha256=digest(PARENT/'results/stage-integrity.json'),
        prior_sealed_entries_unchanged=prior_count,parent_chain_edges_verified=len(seen)-1,
        checkpoint_manifest_sha256=digest(checkpoint),full_checkpoint_payload_rehashed=False,
        local_source_documents=parent['local_source_documents'],primary_pdfs=parent['primary_pdfs'],
        source_urls=parent['source_urls'],previous_primary_source_urls=parent['new_primary_source_urls'],
        new_primary_source_urls=[],observational_source_urls=parent['observational_source_urls'],
        local_dependencies={path:digest(path) for path in citations},compiled_scripts=[path.name for path in scripts],
        checked_result_packets=len(packets),validation_checks=total_checks,main_validation_checks=validation['count'],low_k_integral_checks=len(low_k['checks']),production_checks=len(production['checks'])+len(production_fit['checks']),all_checks_passed=True,
        prior_goal_turn='progress',conditioned_source_equations_derived=True,
        full_history_slow_sources_regenerated=True,calibration_equation_preserved=True,
        early_only_splice_used=False,exact_early_modes=412,late_spectra_recomputed=5,
        matching_rows_recomputed=True,original_physics_parameters_held=True,
        empirical_primary_recomputed=True,empirical_cap_fits=24,empirical_optimizer_starts=96,
        new_field_parameters_fitted=0,common_tracer_nuisances_per_model=6,formal_model_preference=False,
        tiny_k_precision_floor_measured=True,low_k_integral_tail_checked=True,
        tiny_k_production_rows_replaced=True,tiny_k_corrected_native_mode_count=production['corrected_low_mode_count'],
        production_spectrum_authority='results/production-spectrum/status.json',
        production_empirical_authority='results/production-primary-refit/status.json',
        full_finite_k_second_order_evolution=False,native_library_reused_read_only=True,
        native_library_sha256=digest(native_library),original_library_sha256=digest(original),
        protected_workbench_recent_modified_file_count=0,
        protected_check_scope='Modification-time scan since04:40:55UTC7October2026, not a full content-hash baseline.',
        maximum_active_compute_workers=1,library_threads=1,active_stage_workers=0,
        github_action=False,subagents=0,global_installation_changed=False,galaxy_work_modified=False,
        conclusion='Full-history slow-source repair propagated through exact native matching, resolved transfers and the primary observational diagnostic. A separate tiny-mode precision floor was also corrected with direct high-precision native rows and a repeated primary fit. Next use the derived primordial curvature data for finite-k nonlinear source evolution.'))
    print(json.dumps(dict(state='complete',sealed_files=len(hashes),prior_entries_unchanged=prior_count,
        next_prior_count=prior_count+len(hashes),validation_checks=total_checks,result_packets=len(packets))),flush=True)


if __name__=='__main__':
    main()
