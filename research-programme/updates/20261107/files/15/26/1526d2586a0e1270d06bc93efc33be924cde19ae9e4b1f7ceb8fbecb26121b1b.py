from __future__ import annotations

import re
from velocity_common import *


def main():
    modest()
    output=ROOT/'results/stage-integrity.json'
    assert not output.exists()
    candidates=list(BRANCH.glob('*/results/stage-integrity.json'))+[BRANCH/'results/stage-integrity.json']
    by_hash={digest(path):path for path in candidates}
    cursor=PARENT/'results/stage-integrity.json'
    prior_count=0;edges=0;seen=set();parent=None
    while True:
        assert cursor not in seen
        seen.add(cursor)
        report=json.loads(cursor.read_text())
        assert report['state']=='complete'
        if parent is None:
            parent=report
        base=POST if cursor==BRANCH/'results/stage-integrity.json' else cursor.parent.parent
        for relative,expected in report['file_hashes'].items():
            assert digest(base/relative)==expected,base/relative
        prior_count+=len(report['file_hashes'])
        if cursor==BRANCH/'results/stage-integrity.json':
            break
        links=[report[key] for key in ['parent_seal_sha256','previous_seal_sha256'] if key in report]
        assert len(links)==1 and links[0] in by_hash
        cursor=by_hash[links[0]];edges+=1
    assert prior_count==6563,prior_count
    checkpoint=POST/'_checkpoints/20261003-pre-condensate-origin/manifest.json'
    assert digest(checkpoint)==parent['checkpoint_manifest_sha256']=='38f86719b0eb4c5e7fd86171a98af51918369f9daf81584a3c19c3d63222389e'
    original=POST/'.venv-score/Lib/site-packages/camb/cambdll.dll'
    native=BRANCH/'native-heavy-matching-20261007/native/camb/cambdll.dll'
    assert digest(original)==parent['original_library_sha256']
    assert digest(native)==parent['native_library_sha256']
    for source in parent['local_source_documents']+parent['primary_pdfs']:
        assert digest(source['path'])==source['sha256']
    scripts=list(ROOT.glob('*.py'))
    for path in scripts:
        compile(path.read_bytes(),str(path),'exec')
    hashes_of_scripts={digest(path) for path in scripts}
    validation=json.loads((ROOT/'results/validation/status.json').read_text())
    assert validation['all_checks_passed'] and all(row['passed'] for row in validation['checks'])
    packets=list(ROOT.glob('results/*/status.json'))+[ROOT/'sources/status.json']
    for path in packets:
        report=json.loads(path.read_text())
        assert report['state']=='complete' and report['script_sha256'] in hashes_of_scripts
        assert (path.parent/'COMPLETE').is_file()
        for source,expected in report['input_hashes'].items():
            assert digest(source)==expected,(path,source)
    source_manifest=json.loads((ROOT/'sources/status.json').read_text())
    for record in source_manifest['records']:
        assert record['url'].startswith('https://') and record['final_url'].startswith('https://')
        assert digest(record['path'])==record['sha256']
    citations=set()
    for path in ROOT.glob('*.md'):
        for reference in re.findall(r'`([^`\n]+)`',path.read_text(encoding='utf-8')):
            if reference.endswith(('.md','.py','.npz','.json','.png')):
                target=(ROOT/reference).resolve()
                assert target==output or target.is_file(),(path,reference)
                if target!=output:
                    citations.add(str(target))
    protected=POST.parent/'formalization-workbench'
    started=datetime(2026,10,7,2,42,47,tzinfo=timezone.utc)
    changed=[str(path) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime>started.timestamp()]
    assert protected.is_dir() and not changed,changed
    fits=json.loads((ROOT/'results/velocity-fits/status.json').read_text())
    assert len(fits['rows'])==48 and all(row['fit']['converged'] for row in fits['rows'])
    assert not fits['formal_model_preference'] and not fits['coefficient_parent_derived'] and not fits['overlap_scores_added']
    file_hashes={}
    for directory,directories,files in os.walk(ROOT):
        assert '__pycache__' not in directories,directory
        for name in sorted(files):
            path=Path(directory)/name
            if path!=output:
                file_hashes[path.relative_to(ROOT).as_posix()]=digest(path)
    write_json(output,dict(state='complete',sealed_at_utc=datetime.now(timezone.utc).isoformat(),file_hashes=file_hashes,
        parent_seal_sha256=digest(PARENT/'results/stage-integrity.json'),prior_sealed_entries_unchanged=prior_count,
        parent_chain_edges_verified=edges,checkpoint_manifest_sha256=digest(checkpoint),full_checkpoint_payload_rehashed=False,
        local_source_documents=parent['local_source_documents'],primary_pdfs=parent['primary_pdfs'],
        source_urls=parent['source_urls'],previous_primary_source_urls=parent['new_primary_source_urls'],
        new_primary_source_urls=[record['url'] for record in source_manifest['records']],
        observational_source_urls=parent['observational_source_urls'],
        local_dependencies={path:digest(path) for path in citations},compiled_scripts=[path.name for path in scripts],
        checked_result_packets=len(packets),validation_checks=validation['count'],all_checks_passed=True,
        real_multipole_data_reused=True,real_survey_window_reused=True,matched_control_treatment=True,
        primary_observations=32,primary_tracer_nuisance_parameters=6,field_parameters_fitted=0,
        conditional_leading_response_derived=True,coherent_linear_pair_moments_derived=True,
        residual_variance_parent_derived=False,real_mock_catalogs_used=False,
        nonlinear_tracer_model_validated=False,omitted_higher_multipole_window_error_bounded=False,
        formal_model_preference=False,overlapping_scores_added=False,
        native_library_reused_read_only=True,native_library_sha256=digest(native),original_library_sha256=digest(original),
        protected_workbench_recent_modified_file_count=0,
        protected_check_scope='Modification-time scan since02:42:47UTC7October2026, not a full content-hash baseline.',
        maximum_active_compute_workers=1,library_threads=1,active_stage_workers=0,
        github_action=False,subagents=0,global_installation_changed=False,galaxy_work_modified=False,
        conclusion='Common residual-velocity freedom removes previous heavy score advantage, leaving a primary near tie. Coherent parent pair moments derived; next derive density-weighted pair streaming and justify higher-ell survey coupling.'))
    print(json.dumps(dict(state='complete',sealed_files=len(file_hashes),prior_entries_unchanged=prior_count,
        next_prior_count=prior_count+len(file_hashes),validation_checks=validation['count'],packets=len(packets))))


if __name__=='__main__':
    main()
