from common243 import *
import ast
import json
from datetime import datetime, timezone


def main():
    modest()
    assert not (ROOT / 'results/stage-integrity.json').exists()
    config = protocol()
    phases = [('replay-configuration.json', 'replay243.py'),
        ('tail-configuration.json', 'tail243.py'), ('assessment-configuration.json', 'assess243.py'),
        ('attribution-configuration.json', 'attribute243.py'), ('corner-configuration.json', 'corner243.py'),
        ('relaxation-configuration.json', 'relaxation243.py')]
    for configuration, script in phases:
        assert read(ROOT / configuration)['script_sha256'] == digest(ROOT / script)
    assert read(ROOT / 'tail-configuration.json')['method_sha256'] == digest(ROOT / 'TAIL-METHOD.md')
    paths = [DATA / 'drives/validation.json', DATA / 'assessment/result.json']
    paths += [DATA / folder / f'{model}.json' for folder in ('attribution', 'corner', 'relaxation') for model in ('heavy', 'cold')]
    paths.append(DATA / 'fast-memory-bounds.json')
    inputs, checks = dict(read(ROOT / 'inputs.json')), []
    for path in paths:
        report = read(path)
        checks.extend(dict(row, report=path.relative_to(DATA).as_posix()) for row in report['checks'])
        for name, checksum in report.get('consumed_inputs', {}).items():
            if name in inputs:
                assert inputs[name] == checksum, name
            inputs[name] = checksum
        if path != DATA / 'assessment/result.json':
            assert report['qualified'], path
    for path, checksum in inputs.items():
        assert digest(path) == checksum, path
    failed = [row for row in checks if not row['passed']]
    assert len(checks) == 788 and len(failed) == 16
    assert all(row['report'] == 'assessment/result.json' for row in failed)
    assert read(DATA / 'assessment/result.json')['qualified'] is False
    own_files = [path for path in ROOT.iterdir() if path.is_file()] + [path for path in DATA.rglob('*') if path.is_file()]
    validated_json, validated_arrays, validated_scripts = 0, 0, 0
    for path in own_files:
        if path.suffix == '.py':
            ast.parse(path.read_text(encoding='utf-8'), filename=str(path))
            validated_scripts += 1
        elif path.suffix == '.json':
            json.loads(path.read_text(encoding='utf-8'))
            validated_json += 1
        elif path.suffix == '.npz':
            with np.load(path, allow_pickle=False) as arrays:
                for key in arrays.files:
                    assert np.isfinite(arrays[key]).all(), (path, key)
                    validated_arrays += 1
    assert not list(ROOT.glob('__pycache__'))
    assert not list(DATA.rglob('__pycache__'))
    protected = BRANCH.parent.parent / 'formalization-workbench'
    started = datetime(2026, 10, 27, 13, 18, 48, tzinfo=timezone.utc).timestamp()
    recent = [str(path) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime >= started]
    assert not recent, recent[:20]
    bookmarks = [BRANCH / 'RESUME-CURRENT.md', BRANCH.parent / 'CURRENT_LOCAL_RESUME.md']
    for path in bookmarks:
        with path.open(encoding='utf-8') as handle:
            head = handle.read(2500)
        assert head.startswith('# Stage243 SAVED') and ROOT.as_posix() in head
    for model in ('heavy', 'cold'):
        for phase in ('replay', 'tail'):
            assert read(DATA / f'workers/{phase}-{model}.json')['state'] == 'complete'
    status = dict(stage=243, execution_complete=True, integrity_passed=True, qualified=False,
        whole_history_refinement_passed=False, no_unqualified_source_promotion=True,
        counts=dict(checks=len(checks), passed=len(checks) - len(failed), failed=len(failed),
            json_files=validated_json, numeric_arrays=validated_arrays, scripts=validated_scripts),
        failed_checks=failed, directly_consumed_inputs=inputs,
        file_hashes={path.relative_to(ROOT).as_posix(): digest(path) for path in sorted(own_files)},
        total_payload_bytes=sum(path.stat().st_size for path in own_files),
        data_physical_location=str(DATA.resolve()), parent_seal=SEAL,
        protected_scan=dict(root=str(protected), modified_since_stage_start=len(recent),
            scope='Timestamp write scan plus exact hashes of consumed sources; no Git repository exists at research root'),
        bookmarks={str(path): digest(path) for path in bookmarks}, finished_at=now(),
        scope='Driven retained soft-tail model and source-equation diagnostics; no new sky test, source contraction, or gravity propagation',
        next='Stiffly accurate coupled history reconstruction, then validated tail and source-to-gravity response')
    write(ROOT / 'results/stage-integrity.json', status)
    result = read(ROOT / 'results/stage-integrity.json')
    for path, checksum in result['file_hashes'].items():
        assert digest(ROOT / path) == checksum, path
    write(ROOT / 'results/COMPLETE.json', dict(execution_complete=True, integrity_passed=True,
        whole_history_refinement_passed=False, seal_sha256=digest(ROOT / 'results/stage-integrity.json')))
    print(dict(seal=digest(ROOT / 'results/stage-integrity.json'), counts=status['counts'],
        payload_bytes=status['total_payload_bytes'], protected_modified=len(recent),
        integrity_passed=True, whole_history_refinement_passed=False), flush=True)


if __name__ == '__main__':
    main()

