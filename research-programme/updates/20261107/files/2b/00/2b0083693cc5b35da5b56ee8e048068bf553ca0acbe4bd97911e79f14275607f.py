from __future__ import annotations

import re
from spectrum_common import *


def main():
    modest()
    output=ROOT/'results/stage-integrity.json'
    assert not output.exists()
    candidates=list(BRANCH.glob('*/results/stage-integrity.json'))+[BRANCH/'results/stage-integrity.json']
    by_hash={digest(path):path for path in candidates}
    cursor=PARENT/'results/stage-integrity.json'
    prior_count=0;edges=0;seen=set();parent_report=None
    while True:
        assert cursor not in seen
        seen.add(cursor)
        report=json.loads(cursor.read_text())
        assert report['state']=='complete',cursor
        if parent_report is None:
            parent_report=report
        base=POST if cursor==BRANCH/'results/stage-integrity.json' else cursor.parent.parent
        for relative,expected in report['file_hashes'].items():
            assert digest(base/relative)==expected,base/relative
        prior_count+=len(report['file_hashes'])
        if cursor==BRANCH/'results/stage-integrity.json':
            break
        links=[report[key] for key in ['parent_seal_sha256','previous_seal_sha256'] if key in report]
        assert len(links)==1 and links[0] in by_hash,(cursor,links)
        cursor=by_hash[links[0]]
        edges+=1
    assert prior_count==6204,prior_count
    manifest=POST/'_checkpoints/20261003-pre-condensate-origin/manifest.json'
    assert digest(manifest)==parent_report['checkpoint_manifest_sha256']=='38f86719b0eb4c5e7fd86171a98af51918369f9daf81584a3c19c3d63222389e'
    original_library=POST/'.venv-score/Lib/site-packages/camb/cambdll.dll'
    assert digest(original_library)=='dacec802377123147f336c37218cdf871b293f1de2b87019c8726b7290082bef'
    for source in parent_report['local_source_documents']+parent_report['primary_pdfs']:
        assert digest(source['path'])==source['sha256']
    validation=json.loads((ROOT/'results/validation/status.json').read_text())
    assert validation['all_checks_passed'] and all(row['passed'] for row in validation['checks'])
    scripts=list(ROOT.glob('*.py'))
    for path in scripts:
        compile(path.read_bytes(),str(path),'exec')
    producers={digest(path) for path in scripts}
    packets=list(ROOT.glob('runs/*/status.json'))+list(ROOT.glob('results/*/status.json'))+list(ROOT.glob('sources/*/status.json'))
    for path in packets:
        report=json.loads(path.read_text())
        assert report['state']=='complete' and report['script_sha256'] in producers,path
        assert (path.parent/'COMPLETE').is_file(),path
        for source,expected in report['input_hashes'].items():
            assert digest(source)==expected,(path,source)
    cited=set()
    for path in ROOT.glob('*.md'):
        for reference in re.findall(r'`([^`\n]+)`',path.read_text(encoding='utf-8')):
            if reference.endswith(('.md','.py','.npz','.json','.png')):
                target=(ROOT/reference).resolve()
                assert target==output or target.is_file(),(path,reference)
                if target!=output:
                    cited.add(str(target))
    protected=POST.parent/'formalization-workbench'
    started=datetime(2026,10,7,1,53,38,tzinfo=timezone.utc)
    changed=[str(path) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime>started.timestamp()]
    assert protected.is_dir() and not changed,changed
    excluded={'runs/matplotlib-cache'}
    hashes={}
    for directory,directories,files in os.walk(ROOT):
        directories[:]=[name for name in directories if (Path(directory)/name).relative_to(ROOT).as_posix() not in excluded]
        assert '__pycache__' not in directories,directory
        for name in sorted(files):
            path=Path(directory)/name
            if path!=output:
                hashes[path.relative_to(ROOT).as_posix()]=digest(path)
    source_report=json.loads((ROOT/'sources/sdss-growth/status.json').read_text())
    write_json(output,dict(state='complete',sealed_at_utc=datetime.now(timezone.utc).isoformat(),file_hashes=hashes,
        parent_seal_sha256=digest(PARENT/'results/stage-integrity.json'),prior_sealed_entries_unchanged=prior_count,
        parent_chain_edges_verified=edges,checkpoint_manifest_sha256=digest(manifest),full_checkpoint_payload_rehashed=False,
        local_source_documents=parent_report['local_source_documents'],primary_pdfs=parent_report['primary_pdfs'],
        source_urls=parent_report['source_urls'],previous_primary_source_urls=parent_report['new_primary_source_urls'],
        new_primary_source_urls=[source_report['official_landing_page'],*[row['remote_url'] for row in source_report['source_records']]],
        observational_source_urls=parent_report['observational_source_urls'],
        local_dependencies={path:digest(path) for path in cited},compiled_scripts=[path.name for path in scripts],
        checked_result_packets=len(packets),validation_checks=validation['count'],all_checks_passed=True,
        k_count=len(modes(2)),nested_coarse_count=len(modes(1)),qualified_max_k_Mpc_inverse=5.,exploratory_max_k_Mpc_inverse=10.,
        inherited_pressure_gate_unchanged=2e-6,high_k_failures_retained=True,
        resolved_physical_matter_spectrum=True,physical_sigma8_integrated=True,
        real_growth_data_screen=True,observational_parameter_fit=False,formal_model_preference=False,
        excluded_reproducible_dependency_caches=sorted(excluded),native_library_reused_read_only=True,
        native_library_sha256=digest(PARENT/'native/camb/cambdll.dll'),original_library_sha256=digest(original_library),
        protected_workbench_recent_modified_file_count=0,
        protected_check_scope='Modification-time scan since01:53:38UTC7October2026, not a full content-hash baseline.',
        maximum_active_compute_workers=1,maximum_python_processes_during_tests=1,
        heavy_workers_below_normal_pinned_core2=True,library_threads=1,active_stage_workers=0,
        github_action=False,subagents=0,global_installation_changed=False,galaxy_work_modified=False,
        conclusion='Dense sourced native matter transfer and density/velocity integrals, with matched control recovery and real SDSS growth screening. Next: validate survey-template mapping before formal parameter comparison.'))
    print(json.dumps(dict(state='complete',sealed_files=len(hashes),prior_entries_unchanged=prior_count,
        next_prior_count=prior_count+len(hashes),validation_checks=validation['count'],packets=len(packets))),flush=True)


if __name__=='__main__':
    main()
