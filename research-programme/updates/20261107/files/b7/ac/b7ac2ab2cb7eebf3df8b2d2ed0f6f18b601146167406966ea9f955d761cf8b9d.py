from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
import psutil


ROOT = Path(__file__).resolve().parent
POST = ROOT.parent
CHECKPOINT = POST / '_checkpoints' / '20261003-pre-condensate-origin'
OUTPUT = ROOT / 'results' / 'checkpoint-validation'


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([4])
    if OUTPUT.exists():
        raise RuntimeError('Refusing to overwrite validation evidence.')
    OUTPUT.mkdir(parents=True)
    specification = importlib.util.spec_from_file_location('snapshot_restore', CHECKPOINT / 'restore_snapshot.py')
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    destination = POST.parent / 'RESTORE-PREVIEW-20261003-NOT-CREATED'
    dry_run = module.restore(destination, dry_run=True)
    assert not destination.exists()
    manifest = json.loads((CHECKPOINT / 'manifest.json').read_text())
    changed = []
    for record in manifest['files']:
        source = POST / record['path']
        if not source.is_file() or module.digest(source) != record['sha256']:
            changed.append(record['path'])
    assert not changed, changed
    print(json.dumps({'full_payload_reverified': manifest['file_count'], 'original_files_changed': len(changed)}), flush=True)

    fixture = OUTPUT / 'restore-fixture'
    fixture.mkdir()
    payload = fixture / 'payload'
    payload.mkdir()
    original_source = OUTPUT / 'fixture-original'
    original_source.mkdir()
    fixture_files = {'README.md': b'recovery test\n', 'nested/variables.txt': 'psi theta Gamma\n'.encode()}
    records = []
    for relative, content in fixture_files.items():
        path = payload / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
        records.append({'path': relative, 'bytes': len(content), 'sha256': hashlib.sha256(content).hexdigest()})
    fixture_manifest = {'state': 'complete', 'source_root': str(original_source), 'file_count': len(records), 'total_bytes': sum(row['bytes'] for row in records), 'files': records}
    manifest_path = fixture / 'manifest.json'
    manifest_path.write_text(json.dumps(fixture_manifest), encoding='utf-8')
    (fixture / 'manifest.sha256').write_text(module.digest(manifest_path), encoding='ascii')
    module.CHECKPOINT = fixture
    restored = OUTPUT / 'fixture-restored'
    module.restore(restored, dry_run=True)
    assert not restored.exists()
    executed = module.restore(restored, dry_run=False)
    for relative, content in fixture_files.items():
        assert (restored / relative).read_bytes() == content
    failures = []

    def refuses(name, target):
        try:
            module.restore(target, dry_run=True)
        except RuntimeError as error:
            failures.append({'name': name, 'refused': True, 'message': str(error)})
        else:
            raise AssertionError(f'Expected refusal: {name}')

    refuses('existing_destination', restored)
    refuses('source_tree_overlap', original_source / 'new-child')
    (payload / 'README.md').write_bytes(b'corruption test\n')
    refuses('corrupted_payload', OUTPUT / 'fixture-corrupt-rejected')
    (payload / 'README.md').write_bytes(fixture_files['README.md'])
    manifest_path.write_text(manifest_path.read_text() + ' ', encoding='utf-8')
    refuses('corrupted_manifest', OUTPUT / 'fixture-manifest-rejected')
    protected = POST.parent / 'formalization-workbench'
    import datetime
    started = datetime.datetime(2026, 10, 3, 13, 7, 37, tzinfo=datetime.timezone.utc).timestamp()
    protected_recent = [str(path.relative_to(protected)) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime >= started]
    report = {'state': 'complete', 'full_snapshot_dry_run': dry_run, 'original_snapshot_sources_changed': changed, 'fixture_execute': executed, 'fixture_refusals': failures, 'protected_workbench_files_modified_since_turn_start': protected_recent, 'github_action': False, 'independent_payload_rehash': True}
    (OUTPUT / 'status.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    assert not protected_recent, protected_recent
    print(json.dumps({'state': 'complete', 'verified_files': manifest['file_count'], 'fixture_restored_files': len(records), 'safety_refusals': len(failures), 'protected_changes': len(protected_recent)}), flush=True)


if __name__ == '__main__':
    main()
