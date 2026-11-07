from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import os
import re
import subprocess
from collections import Counter
from functools import lru_cache
from pathlib import Path, PurePosixPath
from urllib.parse import quote, unquote


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path('research-programme/updates/20261107')
BASE = 'fb59a16fb9f33dc6cdfaca87c23ff217a85dd0de'
DEFAULT_SOURCE = Path('D:/Users/ollet/Desktop/Turn an intuitive research programme into a formal field-theoretic framework/Motion-TimeSpace--main/post-checkpoint-work')
DEFAULT_DATA = Path('C:/MTS-Data')
FIELDS = ['source_path', 'published_path', 'size_bytes', 'sha256', 'disposition', 'reason', 'authority']
HASH = re.compile(r'^[a-fA-F0-9]{64}$')
SECRET = re.compile(rb'(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|sk-proj-[A-Za-z0-9_-]{40,})')
FORBIDDEN = {'.git', '.env', '.venv', '__pycache__'}
MUTABLE = {'RESUME-CURRENT.md', 'CURRENT_LOCAL_RESUME.md', 'NEXT.md', 'RESUME.md'}


def digest(path):
    hasher = hashlib.sha256()
    with path.open('rb') as stream:
        while chunk := stream.read(1024 * 1024):
            hasher.update(chunk)
    return hasher.hexdigest()


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def new_file(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('xb') as stream:
        stream.write(data)


def safe_path(value):
    path = PurePosixPath(value.replace('\\', '/'))
    if path.is_absolute() or '..' in path.parts or ':' in str(path) or any(part in FORBIDDEN for part in path.parts):
        raise ValueError(f'Unsafe relative path: {value}')
    return path.as_posix()


def inventory(source, data_root, output):
    branch = source / 'condensate-origin-20261003'
    bridge = data_root / 'condensate-origin-20261003/stiff-gas-dense-output-20261027/data/memory-tail-history-20261027/source-readout-bridge-20261102'
    entries = {}
    seals = []
    skipped = []

    @lru_cache(maxsize=None)
    def label(path):
        path = Path(os.path.normpath(path))
        for prefix, base in [('post', source), ('data', data_root)]:
            if path.is_relative_to(base):
                return prefix + '/' + path.relative_to(base).as_posix()
        return 'external/' + path.as_posix().replace(':', '')

    @lru_cache(maxsize=None)
    def resolve(raw, base):
        path = Path(raw.replace('\\', '/'))
        if path.is_absolute():
            return path
        safe_path(str(path))
        candidates = list(dict.fromkeys([base / path, source / path, branch / path]))
        existing = [candidate for candidate in candidates if candidate.is_file()]
        return existing[0] if existing else candidates[0]

    def add(path, sha, authority):
        if not isinstance(sha, str) or not HASH.fullmatch(sha):
            raise ValueError(f'Invalid hash: {path}')
        name = label(path)
        if name not in entries:
            entries[name] = dict(source_path=name, local_path=str(path), expected={}, size_bytes=path.stat().st_size if path.is_file() else None)
        row = entries[name]
        row['expected'].setdefault(sha.lower(), []).append(authority)

    def add_seal(path, base, maps):
        document = read_json(path)
        state = document.get('state')
        accepted = state in {'complete', 'batch_complete', 'panel_complete', 'verified_closed'} or (document.get('execution_complete') is True and document.get('integrity_passed') is True)
        if not accepted:
            skipped.append(dict(path=label(path), state=state, reason='No completed integrity state'))
            return
        authority = label(path)
        seals.append(dict(path=authority, sha256=digest(path), state=state, stage=document.get('stage'), qualified=document.get('qualified')))
        add(path, digest(path), authority)
        for key in maps:
            values = document.get(key, {})
            if isinstance(values, dict):
                for raw, sha in values.items():
                    if isinstance(sha, str) and HASH.fullmatch(sha):
                        add(resolve(raw, base), sha, authority)
            elif key == 'artifacts':
                for value in values:
                    add(resolve(value['path'], base), value['sha256'], authority)

    annular = source / 'source-intake/navier-stokes/20260914/annular-P7-bisection-integrity-20261003.json'
    add_seal(annular, source, ['hashes'])
    add_seal(branch / 'results/stage-integrity.json', source, ['file_hashes'])
    for directory in sorted(branch.iterdir()):
        seal = directory / 'results/stage-integrity.json'
        if directory.is_dir() and seal.is_file():
            add_seal(seal, directory, ['file_hashes', 'local_dependencies', 'directly_consumed_inputs', 'consumed_and_immediate_rehashed'])
            if len(seals) % 40 == 0:
                print(f'Inventoried {len(seals)} seals and {len(entries)} unique paths', flush=True)
    for directory in sorted(source.glob('mts-*-2026110*')):
        seal = directory / 'closeout.json'
        if seal.is_file():
            add_seal(seal, directory, ['artifacts'])
        else:
            skipped.append(dict(path=label(directory), reason='No closeout; excluded rather than promoted'))
    coverage_path = bridge / 'final-stable-real-batch-rays037-038/common-coverage.json'
    coverage = read_json(coverage_path)
    assert coverage['passed'] and coverage['through'] == 38 and coverage['individually_verified'] == 39
    authority = label(coverage_path)
    add(coverage_path, digest(coverage_path), authority)
    add(Path(coverage['legacy_source_receipt']), coverage['legacy_source_receipt_sha256'], authority)
    for ray in coverage['directions'].values():
        add(Path(ray['acceptance']), ray['acceptance_sha256'], authority)
        for relative, sha in ray['files'].items():
            add(Path(ray['directory']) / safe_path(relative), sha, authority)
    queue = [entry for entry in entries.values() if entry['source_path'].startswith('data/') and Path(entry['local_path']).name in {'protocol.json', 'integrity.json', 'input-map.json'}]
    walked = set()
    while queue:
        entry = queue.pop()
        path = Path(entry['local_path'])
        if str(path) in walked or not path.is_file() or path.stat().st_size > 16 * 1024 * 1024:
            continue
        walked.add(str(path))
        if digest(path) not in entry['expected']:
            continue
        document = read_json(path)
        before = set(entries)

        def walk(value):
            if isinstance(value, dict):
                if isinstance(value.get('path'), str) and isinstance(value.get('sha256'), str) and HASH.fullmatch(value['sha256']):
                    add(resolve(value['path'], path.parent), value['sha256'], label(path))
                for key, child in value.items():
                    if isinstance(child, str) and HASH.fullmatch(child) and ('/' in key or '\\' in key):
                        add(resolve(key, path.parent), child, label(path))
                    elif isinstance(child, (dict, list)):
                        walk(child)
            elif isinstance(value, list):
                for child in value:
                    walk(child)

        walk(document)
        queue.extend(entries[name] for name in set(entries) - before if Path(entries[name]['local_path']).name in {'protocol.json', 'integrity.json', 'input-map.json'})
    result = dict(base_commit=BASE, seals=seals, skipped=skipped, entries=sorted(entries.values(), key=lambda row: row['source_path']))
    new_file(output, (json.dumps(result, indent=2) + '\n').encode())
    sizes = Counter()
    for row in entries.values():
        sizes[Path(row['local_path']).suffix] += row['size_bytes'] or 0
    print(json.dumps(dict(seals=len(seals), candidates=len(entries), missing=sum(row['size_bytes'] is None for row in entries.values()), total_bytes=sum(sizes.values()), largest_extensions=sizes.most_common(10), skipped=skipped), indent=2))


def exclusion(row):
    path = Path(row['local_path'])
    parts = set(path.parts)
    if FORBIDDEN & parts or 'mts-relative-phase-perturbations-20261107' in parts:
        return 'excluded_unverified', 'Environment or explicitly untested branch; not published.'
    if path.name in MUTABLE:
        return 'excluded_mutable', 'Mutable restart instructions are not frozen scientific evidence.'
    if row['source_path'].startswith('external/'):
        return 'local_dependency', 'Dependency outside the authorized research/data roots; not redistributed.'
    if '_checkpoints' in parts:
        return 'local_backup', 'Rollback snapshot/restore tooling remains local; original public history is preserved.'
    if any('cache' in part.lower() for part in parts) or HASH.fullmatch(path.stem):
        return 'local_cache', 'Generated event/cache product; declared seal hash retained, not rehashed or uploaded.'
    compact_frontier = row['source_path'].startswith('post/mts-cold-background-extension-20261107/') or ('final-epoch-real-v2-ray' in row['source_path'] and path.name == 'complete.npz')
    if path.suffix.lower() in {'.npz', '.npy', '.bin', '.h5', '.hdf5'} and not compact_frontier:
        return 'local_array', 'Numerical array retained locally; declared seal hash recorded, not rehashed or uploaded.'
    if path.suffix.lower() in {'.pdf', '.zip', '.7z', '.gz', '.html', '.exe', '.dll', '.so', '.a', '.o', '.mod', '.whl', '.pyd', '.pyc', '.partial'}:
        return 'local_dependency', 'Third-party source/download, executable, archive or build product; retained locally.'
    if row['size_bytes'] is None:
        return 'unavailable', 'Seal declares this path, but the source is not available at publication time.'
    ceiling = 48 * 1024 * 1024 if ('integrity' in path.name or path.name == 'closeout.json') else 1024 * 1024
    if row['size_bytes'] > ceiling:
        return 'local_large', 'Large numerical product; sealed expected hash recorded, not rehashed or uploaded in this compact release.'
    return None


def supplement(plan_path, source, data_root):
    plan = read_json(plan_path)
    entries = {row['source_path']: row for row in plan['entries']}

    def label(path):
        path = Path(os.path.normpath(path))
        for prefix, base in [('post', source), ('data', data_root)]:
            if path.is_relative_to(base):
                return prefix + '/' + path.relative_to(base).as_posix()
        raise ValueError(f'Out-of-scope supplementary path: {path}')

    def add(path, sha, authority):
        name = label(path)
        assert path.is_file() and HASH.fullmatch(sha)
        if name not in entries:
            entries[name] = dict(source_path=name, local_path=str(path), expected={}, size_bytes=path.stat().st_size)
        entries[name]['expected'].setdefault(sha, []).append(authority)

    for name, state in [('mts-state-feedback-20261107', 'closed_mixed_scientific_result'), ('mts-wave-state-20261107', 'complete-bounded-stage'), ('mts-covariance-dynamics-20261107', 'completed-current-calculation-not-overall-goal')]:
        directory = source / name
        path = directory / 'closeout.json'
        document = read_json(path)
        assert document['state'] == state
        authority = label(path)
        add(path, digest(path), authority)
        plan['seals'].append(dict(path=authority, sha256=digest(path), state=state, stage=None, qualified=None))
        for artifact in document.get('artifacts', []):
            add(Path(artifact['path']), artifact['sha256'], authority)
        for relative, sha in document.get('files', {}).items():
            add(directory / relative, sha, authority)
        for key in ['validation', 'physical_replay']:
            if key in document:
                item = document[key]
                add(directory / item['path'], item['sha256'], authority)
        plan['skipped'] = [row for row in plan['skipped'] if row['path'] != authority]
    history = data_root / 'condensate-origin-20261003/stiff-gas-dense-output-20261027/data/memory-tail-history-20261027'
    path = history / 'FINAL-ENDPOINT-READY-20261102.json'
    document = read_json(path)
    assert document['history_complete'] and document['final_cell'] == 450
    authority = label(path)
    add(path, digest(path), authority)
    report = Path(document['independent_report'])
    assert digest(report) == document['independent_report_sha256'] and read_json(report)['passed']
    add(report, document['independent_report_sha256'], authority)
    for item in document['cases'].values():
        for kind in ['metadata', 'packet']:
            add(Path(item[kind + '_path']), item[kind + '_sha256'], authority)
    item = document['kinematic_bank']
    add(Path(item['protocol_path']), item['protocol_sha256'], authority)
    plan['entries'] = sorted(entries.values(), key=lambda row: row['source_path'])
    output = plan_path.with_name(plan_path.stem + '.supplemented.json')
    new_file(output, (json.dumps(plan, indent=2) + '\n').encode())
    counters, sizes = Counter(), Counter()
    for row in plan['entries']:
        category = (exclusion(row) or ('eligible', ''))[0]
        counters[category] += 1
        sizes[category] += row['size_bytes'] or 0
    print(json.dumps(dict(plan=str(output), selected_seals=len(plan['seals']), rows=len(plan['entries']), dispositions=counters, bytes=sizes), indent=2))


def export(plan_path):
    plan = read_json(plan_path)
    rows, payloads, problems = [], {}, []
    for ordinal, entry in enumerate(plan['entries'], 1):
        name = entry['source_path']
        decision = exclusion(entry)
        published = ''
        sha = next(iter(entry['expected']))
        if decision is None:
            path = Path(entry['local_path'])
            data = path.read_bytes()
            sha = hashlib.sha256(data).hexdigest()
            if sha not in entry['expected']:
                decision = ('excluded_changed', 'Current bytes do not match any selected seal; current file not published.')
                problems.append(dict(source_path=name, actual_sha256=sha, expected=list(entry['expected'])))
                sha = next(iter(entry['expected']))
            elif SECRET.search(data):
                raise ValueError(f'Credential-shaped content requires review: {name}')
            else:
                published = payloads.get(sha)
                if published is None:
                    suffix = path.suffix.lower() if re.fullmatch(r'\.[a-z0-9]{1,12}', path.suffix.lower()) else '.bin'
                    published = (PACKAGE / 'files' / sha[:2] / sha[2:4] / (sha + suffix)).as_posix()
                    new_file(ROOT / published, data)
                    payloads[sha] = published
                decision = ('published', 'Current bytes verified against a completed-stage seal; includes explicitly recorded failed tests.')
        authorities = entry['expected'][sha]
        rows.append(dict(source_path=name, published_path=published, size_bytes=entry['size_bytes'] if entry['size_bytes'] is not None else '', sha256=sha, disposition=decision[0], reason=decision[1], authority=authorities[0]))
        if ordinal % 2500 == 0:
            print(f'Inspected {ordinal}/{len(plan["entries"])} source rows', flush=True)
    package = ROOT / PACKAGE
    package.mkdir(parents=True, exist_ok=True)
    parts = []
    for start in range(0, len(rows), 4000):
        subset = rows[start:start + 4000]
        part = package / 'manifest' / f'part-{start // 4000 + 1:03d}.csv'
        part.parent.mkdir(parents=True, exist_ok=True)
        with part.open('x', encoding='utf-8', newline='') as stream:
            writer = csv.DictWriter(stream, fieldnames=FIELDS)
            writer.writeheader()
            writer.writerows(subset)
        parts.append(dict(part_path=part.relative_to(package).as_posix(), row_count=len(subset), size_bytes=part.stat().st_size, sha256=digest(part)))
    with (package / 'MANIFEST.csv').open('x', encoding='utf-8', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=['part_path', 'row_count', 'size_bytes', 'sha256'])
        writer.writeheader()
        writer.writerows(parts)
    new_file(package / 'manifest/README.md', ('# Complete source manifest\n\nEach part contains at most 4,000 source rows. The parent MANIFEST.csv hashes and counts every part.\n\n' + '\n'.join(f'- [{part["part_path"]}]({Path(part["part_path"]).name}) — {part["row_count"]} rows' for part in parts) + '\n').encode())
    new_file(package / 'SEALS.json', (json.dumps(plan['seals'], indent=2) + '\n').encode())
    new_file(package / 'EXCLUSIONS.json', (json.dumps(dict(excluded_unsealed_directories=plan['skipped'], changed_sources=problems), indent=2) + '\n').encode())
    groups = {}
    for start in range(0, len(rows), 160):
        subset = rows[start:start + 160]
        filename = f'items-{start + 1:06d}-{start + len(subset):06d}.md'
        group = f'volume-{start // (160 * 128) + 1:03d}'
        lines = ['# Verified source inventory', '', 'Local-only rows are explicit omissions, not truncated uploads.', '']
        for row in subset:
            if row['published_path']:
                target = '../../' + quote(Path(row['published_path']).relative_to(PACKAGE).as_posix(), safe='/')
                lines.append(f'- [{row["source_path"]}]({target}) — {row["size_bytes"]} bytes')
            else:
                lines.append(f'- `{row["source_path"]}` — **{row["disposition"]}**; {row["reason"]}')
        new_file(package / 'catalogue' / group / filename, ('\n'.join(lines) + '\n').encode())
        groups.setdefault(group, []).append(f'- [Rows {start + 1}–{start + len(subset)}]({filename})')
    for group, pages in groups.items():
        new_file(package / 'catalogue' / group / 'README.md', ('# Catalogue volume\n\n' + '\n'.join(pages) + '\n').encode())
    new_file(package / 'catalogue/README.md', ('# Complete bounded catalogue\n\n' + '\n'.join(f'- [{group}]({group}/README.md)' for group in groups) + '\n').encode())
    lookup = {row['source_path']: row for row in rows}
    selected = [
        ('Latest accepted cold background', 'post/mts-cold-background-extension-20261107/RESULTS.md'),
        ('Cold-background derivation', 'post/mts-cold-background-extension-20261107/DERIVATION.md'),
        ('GR/Poisson wavelength comparisons', 'post/mts-newton-wavelength-bounds-20261107/RESULTS.md'),
        ('Cold-adapted metric estimate', 'post/mts-cold-adapted-metric-gain-20261107/RESULTS.md'),
        ('Retained cosmology and the negative condensate test', 'post/condensate-origin-20261003/cosmology-reconnection-20261006/RESULTS.md'),
        ('Original condensate investigation', 'post/condensate-origin-20261003/RESULTS.md'),
        ('Interior-action storage calculation', 'post/condensate-origin-20261003/interior-storage-20261006/RESULTS.md'),
        ('Native two-field radiation hierarchy', 'post/condensate-origin-20261003/native-two-field-transfer-20261007/RESULTS.md'),
        ('Spectrum uncertainty budget', 'post/condensate-origin-20261003/final-spectrum-uncertainty-20261019/RESULTS.md'),
        ('Angular source to gravity bridge', 'post/condensate-origin-20261003/angular-source-gravity-bridge-20261027/RESULTS.md'),
        ('Completed annular audit with failed convergence gate', 'post/source-intake/navier-stokes/20260914/annular-P7-bisection-integrity-20261003.json'),
        ('Verified scattering directions 0-38', 'data/condensate-origin-20261003/stiff-gas-dense-output-20261027/data/memory-tail-history-20261027/source-readout-bridge-20261102/final-stable-real-batch-rays037-038/common-coverage.json'),
    ]
    guide = ['# Reading guide', '', 'Byte-preserved sources; historical private-run wording predates this authorized release.', '']
    for title, name in selected:
        row = lookup[name]
        if not row['published_path']:
            raise ValueError(f'Required reader source is not publishable: {name}: {row["disposition"]}')
        target = Path(row['published_path']).relative_to(PACKAGE).as_posix()
        guide.append(f'- [{title}]({target}) — `{name}`')
    guide.extend(['', '## Complete stage index', '', 'These are completed audits, not a list of successes: read each result and its qualifications.', ''])
    stage_rows = []
    for seal in plan['seals']:
        row = lookup.get(seal['path'])
        if not row or not row['published_path']:
            continue
        seal_path = PurePosixPath(seal['path'])
        base = seal_path.parent.parent if seal_path.parent.name == 'results' else seal_path.parent
        links = [f'[seal]({Path(row["published_path"]).relative_to(PACKAGE).as_posix()})']
        for filename in ['RESULTS.md', 'DERIVATION.md']:
            item = lookup.get((base / filename).as_posix())
            if item and item['published_path']:
                links.append(f'[{filename}]({Path(item["published_path"]).relative_to(PACKAGE).as_posix()})')
        stage_rows.append(f'- `{base}` — ' + ', '.join(links))
    for start in range(0, len(stage_rows), 150):
        filename = f'STAGES-{start // 150 + 1:02d}.md'
        new_file(package / filename, ('# Completed-stage navigation\n\n' + '\n'.join(stage_rows[start:start + 150]) + '\n').encode())
        guide.append(f'- [Completed stage entries {start + 1}–{min(start + 150, len(stage_rows))}]({filename})')
    guide.extend(['', '[Complete file catalogue](catalogue/README.md). [Hash and disposition manifest](MANIFEST.csv).', '', 'Original relative source links inside archived payloads describe the original directory tree. Use the catalogue or restore utility rather than treating a hash-sharded payload folder as a runnable checkout.', ''])
    new_file(package / 'READING-GUIDE.md', '\n'.join(guide).encode())
    report = dict(base_commit=BASE, selected_completed_seals=len(plan['seals']), inventory_rows=len(rows), dispositions=dict(Counter(row['disposition'] for row in rows)), unique_payloads=len(payloads), published_bytes=sum((ROOT / path).stat().st_size for path in payloads.values()), excluded_bytes=sum(int(row['size_bytes'] or 0) for row in rows if not row['published_path']), changed_sources=len(problems), all_included_current_bytes_match_seals=True, full_raw_data_backup=False, new_physics_tests_run=False)
    new_file(package / 'EXPORT-REPORT.json', (json.dumps(report, indent=2) + '\n').encode())
    print(json.dumps(report, indent=2))


def tree(revision):
    raw = subprocess.check_output(['git', '-C', str(ROOT), 'ls-tree', '-r', '-z', revision])
    result = {}
    for record in raw.split(b'\0'):
        if record:
            header, name = record.split(b'\t', 1)
            mode, kind, oid = header.split()
            result[name.decode()] = (mode.decode(), kind.decode(), oid.decode())
    return result


def manifest_rows():
    package = ROOT / PACKAGE
    parts = list(csv.DictReader((package / 'MANIFEST.csv').open(encoding='utf-8')))
    rows = []
    for part in parts:
        path = package / safe_path(part['part_path'])
        assert path.stat().st_size == int(part['size_bytes']) and digest(path) == part['sha256']
        subset = list(csv.DictReader(path.open(encoding='utf-8')))
        assert len(subset) == int(part['row_count'])
        rows.extend(subset)
    return rows


def normalize_relative_paths():
    package = ROOT / PACKAGE
    audit_path = package / 'SOURCE-PATH-NORMALIZATION.json'
    if audit_path.exists():
        raise FileExistsError('Normalization is a one-time publication repair')
    original_rows = manifest_rows()
    assert len(original_rows) == len({row['source_path'] for row in original_rows})
    mappings = {}
    for row in original_rows:
        name = row['source_path']
        normalized = os.path.normpath(name).replace('\\', '/')
        if normalized != name:
            safe_path(normalized)
            assert normalized not in {item['source_path'] for item in original_rows}
            mappings[name] = normalized
    assert len(mappings) == 2

    def save_csv(path, fields, rows):
        buffer = io.StringIO(newline='')
        writer = csv.DictWriter(buffer, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
        path.write_bytes(buffer.getvalue().encode())

    parts = list(csv.DictReader((package / 'MANIFEST.csv').open(encoding='utf-8')))
    changed_parts = []
    for part in parts:
        path = package / part['part_path']
        rows = list(csv.DictReader(path.open(encoding='utf-8')))
        changed = False
        for row in rows:
            if row['source_path'] in mappings:
                row['source_path'] = mappings[row['source_path']]
                changed = True
        if changed:
            changed_parts.append(dict(part=part['part_path'], previous_sha256=part['sha256']))
            save_csv(path, FIELDS, rows)
            part['size_bytes'], part['sha256'] = path.stat().st_size, digest(path)
    save_csv(package / 'MANIFEST.csv', ['part_path', 'row_count', 'size_bytes', 'sha256'], parts)
    catalogue_changes = []
    for path in (package / 'catalogue').rglob('*.md'):
        original = path.read_text(encoding='utf-8')
        corrected = original
        for name, normalized in mappings.items():
            corrected = corrected.replace(name, normalized)
        if corrected != original:
            path.write_bytes(corrected.encode())
            catalogue_changes.append(path.relative_to(package).as_posix())
    new_file(audit_path, (json.dumps(dict(reason='Resolve two historical parent-directory aliases for safe restoration; payload bytes unchanged.', paths=mappings, manifest_parts=changed_parts, catalogue_pages=catalogue_changes, scientific_payload_changes=0), indent=2) + '\n').encode())
    print(json.dumps(dict(normalized_paths=mappings, scientific_payload_changes=0), indent=2))


def verify(revision):
    rows = manifest_rows()
    assert len(rows) == len({row['source_path'] for row in rows})
    current, original = tree(revision), tree(BASE)
    allowed_changes = {'README.md', '.gitattributes'}
    deleted = set(original) - set(current)
    modified = {path for path in original.keys() & current.keys() if original[path] != current[path]}
    assert not deleted, deleted
    assert modified <= allowed_changes, modified
    added = set(current) - set(original)
    extra_allowed = {'docs/status/STATUS-2026-11-07.md', 'docs/status/PUBLICATION-NOTES-2026-11-07.md', 'tools/publish_verified_20261107.py'}
    assert all(path.startswith(PACKAGE.as_posix() + '/') or path in extra_allowed for path in added)
    checks = {}
    children = {}
    for name in current:
        if name.startswith(PACKAGE.as_posix() + '/'):
            parts = PurePosixPath(name).parts
            for index in range(len(PACKAGE.parts), len(parts)):
                children.setdefault('/'.join(parts[:index]), set()).add(parts[index])
    assert max(map(len, children.values())) <= 256
    for row in rows:
        name = row['published_path']
        if not name:
            assert row['disposition'] != 'published'
            continue
        assert row['disposition'] == 'published' and name in current
        assert 'mts-relative-phase-perturbations-20261107' not in row['source_path']
        safe_path(row['source_path'])
        checks[current[name][2]] = (int(row['size_bytes']), row['sha256'])
    payload_paths = {row['published_path'] for row in rows if row['published_path']}
    assert {name for name in added if name.startswith(PACKAGE.as_posix() + '/files/')} == payload_paths
    payload_count = len(checks)
    for name in added - payload_paths:
        path = ROOT / name
        assert path.is_file()
        checks[current[name][2]] = (path.stat().st_size, digest(path))
    process = subprocess.Popen(['git', '-C', str(ROOT), 'cat-file', '--batch'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    try:
        for oid, (size, sha) in checks.items():
            process.stdin.write((oid + '\n').encode())
            process.stdin.flush()
            header = process.stdout.readline().split()
            assert header == [oid.encode(), b'blob', str(size).encode()]
            data = process.stdout.read(size)
            assert len(data) == size and hashlib.sha256(data).hexdigest() == sha
            assert process.stdout.read(1) == b'\n'
    finally:
        process.stdin.close()
        process.stdout.close()
        process.wait(timeout=30)
    assert process.returncode == 0
    for path in (ROOT / PACKAGE).rglob('*.md'):
        if 'files' in path.relative_to(ROOT / PACKAGE).parts:
            continue
        for target in re.findall(r'\]\(([^)]+)\)', path.read_text(encoding='utf-8')):
            if not target.startswith(('https:', 'http:', '#')):
                assert (path.parent / unquote(target)).resolve().is_file(), (path, target)
    print(json.dumps(dict(revision=revision, inventory_rows=len(rows), verified_unique_payload_blobs=payload_count, verified_new_git_blobs=len(checks), new_tracked_paths=len(added), maximum_new_directory_entries=max(map(len, children.values())), original_files_deleted=len(deleted), original_paths_modified=sorted(modified), all_included_bytes_match=True), indent=2))


def restore(destination):
    if destination.exists():
        raise FileExistsError('Restore requires a new directory, never an existing research tree')
    rows = manifest_rows()
    for row in rows:
        if row['published_path']:
            name = safe_path(row['source_path'])
            data = (ROOT / row['published_path']).read_bytes()
            assert len(data) == int(row['size_bytes']) and hashlib.sha256(data).hexdigest() == row['sha256']
            new_file(destination / name, data)
    print('Restored included files only. See MANIFEST.csv for explicit local-only dependencies.')


def main():
    parser = argparse.ArgumentParser()
    command = parser.add_mutually_exclusive_group(required=True)
    command.add_argument('--inventory', type=Path)
    command.add_argument('--export', type=Path)
    command.add_argument('--verify')
    command.add_argument('--restore', type=Path)
    command.add_argument('--supplement', type=Path)
    command.add_argument('--normalize-relative-paths', action='store_true')
    parser.add_argument('--source', type=Path, default=DEFAULT_SOURCE)
    parser.add_argument('--data-root', type=Path, default=DEFAULT_DATA)
    arguments = parser.parse_args()
    if arguments.inventory:
        inventory(arguments.source, arguments.data_root, arguments.inventory)
    elif arguments.export:
        export(arguments.export)
    elif arguments.verify:
        verify(arguments.verify)
    elif arguments.supplement:
        supplement(arguments.supplement, arguments.source, arguments.data_root)
    elif arguments.normalize_relative_paths:
        normalize_relative_paths()
    else:
        restore(arguments.restore)


if __name__ == '__main__':
    main()
