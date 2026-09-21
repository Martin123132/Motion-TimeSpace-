from __future__ import annotations

import argparse
import ast
import csv
import hashlib
import json
import re
import subprocess
from collections import Counter
from pathlib import Path, PurePosixPath
from urllib.parse import quote


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path('research-programme/updates/20260921')
MANIFEST = PACKAGE / 'MANIFEST.csv'
SEAL = 'source-intake/navier-stokes/20260914/annular-candidate-horizontal-shift-final-integrity.json'
RAW_PACKAGES = ('annular-candidate-horizontal-shift-attempt01/',
                'annular-horizontal-shift-step-scan-attempt01/',
                'annular-moving-Legendre-current-attempt01/',
                'annular-candidate-Ward-source-attempt01/')
FIELDS = ['source_path', 'published_path', 'size_bytes', 'sha256', 'disposition', 'reason']


def digest(path):
    hasher = hashlib.sha256()
    with path.open('rb') as stream:
        while chunk := stream.read(1024 * 1024):
            hasher.update(chunk)
    return hasher.hexdigest()


def git(*arguments):
    return subprocess.check_output(['git', '-C', str(ROOT), *arguments])


def safe_relative(value):
    path = PurePosixPath(value.replace('\\', '/'))
    if path.is_absolute() or '..' in path.parts or ':' in str(path):
        raise ValueError('Unsafe source path')
    if any(part.lower() in {'.git', '.env', '.venv', '__pycache__'} for part in path.parts):
        raise ValueError('Disallowed source path')
    return path.as_posix()


def write_new(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('xb') as stream:
        stream.write(content)


def export(source):
    if (ROOT / MANIFEST).exists():
        raise FileExistsError('Export already exists; do not mutate its snapshot')
    seal = json.loads((source / SEAL).read_text(encoding='utf-8'))
    assert seal['state'] == 'complete' and len(seal['checks']) == 423
    assert all(row['passed'] for row in seal['checks'])
    assert seal['comparisons_passed'] is False
    assert len(seal['original_coarse_failures']) == 6
    assert seal['current_comparisons_passed'] and seal['refined_derivatives_passed']
    expected = {}
    for kind in ('inputs', 'outputs'):
        for raw, sha in seal[kind].items():
            name = safe_relative(raw)
            if name in expected:
                assert expected[name] == sha
            expected[name] = sha
    declared_count = len(expected)
    expected[SEAL] = digest(source / SEAL)
    for path in source.glob('*.md'):
        match = re.match(r'(?:DERIVATION|RESULTS?)-(\d{8})-', path.name)
        if match and '20260910' <= match[1] <= '20260921':
            expected.setdefault(path.name, digest(path))
    queue = [name for name in expected if name.startswith('scripts/') and name.endswith('.py')]
    seen = set()
    historical_syntax_failures = []
    while queue:
        name = queue.pop()
        if name in seen:
            continue
        seen.add(name)
        try:
            tree = ast.parse((source / name).read_bytes(), filename=name)
        except SyntaxError as error:
            historical_syntax_failures.append(dict(path=name, line=error.lineno, message=error.msg))
            continue
        modules = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                modules.update(item.name.split('.')[0] for item in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                modules.add(node.module.split('.')[0])
        for module in modules:
            relative = f'scripts/{module}.py'
            if (source / relative).is_file() and relative not in expected:
                expected[relative] = digest(source / relative)
                queue.append(relative)
    prior = {}
    with (ROOT / 'docs/status/PUBLICATION-MANIFEST-2026-09-09.csv').open(encoding='utf-8-sig') as stream:
        for row in csv.DictReader(stream):
            if (ROOT / row['published_path']).is_file():
                prior.setdefault(row['sha256'], row['published_path'])
    rows, payloads = [], {}
    secret = re.compile(rb'(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|sk-proj-[A-Za-z0-9_-]{40,})')
    for ordinal, (name, sha) in enumerate(sorted(expected.items()), 1):
        path = source / name
        if not path.is_file() or digest(path) != sha:
            raise ValueError(f'Sealed source missing or changed: {name}')
        size = path.stat().st_size
        published, disposition, reason = '', 'omitted_raw', 'Historical numerical array kept locally; not needed for reading the published derivations.'
        if sha in prior:
            published, disposition, reason = prior[sha], 'reused', 'Byte-identical artifact already published on main.'
        elif path.suffix != '.npz' or any(part in name for part in RAW_PACKAGES):
            if size >= 95 * 1024 * 1024:
                raise ValueError(f'Payload exceeds conservative Git blob limit: {name}')
            data = path.read_bytes()
            if secret.search(data):
                raise ValueError(f'Credential-shaped content requires review: {name}')
            published = payloads.get(sha)
            if published is None:
                published = (PACKAGE / 'files' / sha[:2] / (sha[:16] + '-' + path.name)).as_posix()
                write_new(ROOT / published, data)
                payloads[sha] = published
            disposition, reason = 'published', 'Byte-exact source snapshot; failure and partial-state records retained.'
        rows.append(dict(source_path=name, published_path=published, size_bytes=size,
                         sha256=sha, disposition=disposition, reason=reason))
        if ordinal % 1000 == 0:
            print(f'Checked {ordinal}/{len(expected)} source files', flush=True)
    with (ROOT / MANIFEST).open('x', encoding='utf-8', newline='') as stream:
        writer = csv.DictWriter(stream, FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    catalogue = ROOT / PACKAGE / 'catalogue'
    catalogue.mkdir()
    links = []
    for start in range(0, len(rows), 200):
        part = rows[start:start + 200]
        filename = f'items-{start + 1:05d}-{start + len(part):05d}.md'
        lines = ['# Source inventory', '', 'Omitted entries are explicitly local-only, not broken or truncated exports.', '']
        for row in part:
            label = row['source_path']
            if row['published_path']:
                target = '../../../../' + quote(row['published_path'], safe='/')
                lines.append(f"- [{label}]({target}) — {row['disposition']}, {row['size_bytes']} bytes")
            else:
                lines.append(f"- `{label}` — **local raw array, not published**, {row['size_bytes']} bytes; SHA-256 `{row['sha256']}`")
        write_new(catalogue / filename, ('\n'.join(lines) + '\n').encode())
        links.append(f'- [Items {start + 1}–{start + len(part)}]({filename})')
    write_new(catalogue / 'README.md', ('# Complete bounded inventory\n\n' + '\n'.join(links) + '\n').encode())
    counts = dict(Counter(row['disposition'] for row in rows))
    report = dict(sealed_paths=declared_count, inventoried_paths=len(rows), dispositions=counts,
                  new_unique_payloads=len(payloads), new_payload_bytes=sum((ROOT / path).stat().st_size for path in payloads.values()),
                  source_bytes=sum(row['size_bytes'] for row in rows),
                  omitted_bytes=sum(row['size_bytes'] for row in rows if not row['published_path']),
                  authoritative_seal=SEAL, original_coarse_failures=6,
                  scientific_claim_promotion=False, source_hashes_verified=True,
                  preserved_historical_syntax_failures=historical_syntax_failures)
    write_new(ROOT / PACKAGE / 'EXPORT-REPORT.json', (json.dumps(report, indent=2) + '\n').encode())
    selected = [SEAL, 'RESULTS-20260921-candidate-horizontal-shift-and-localized-current.md',
                'DERIVATION-20260921-candidate-horizontal-shift-and-localized-current.md',
                'DERIVATION-20260921-horizontal-shift-step-size-refinement.md',
                'DERIVATION-20260921-moving-source-localized-Legendre-current.md']
    quick = ['# September 21: currents from the retained action', '',
             'Source snapshots are byte-exact. Dates and “private/no GitHub” statements inside them describe their original runs, not this later authorized publication.', '', '## Read first', '']
    lookup = {row['source_path']: row for row in rows}
    for name in selected:
        row = lookup[name]
        quick.append(f"- [{name}](../../../{quote(row['published_path'], safe='/')})")
    quick.extend(['', '## Complete inventory', '', '[Bounded source catalogue](catalogue/README.md). [Machine-readable mapping](MANIFEST.csv). [Export counts](EXPORT-REPORT.json).', '',
                  'All declared seal paths are inventoried, including excluded historical raw arrays. Source scripts, derivations, JSON/CSV audit records and four recent numerical packages are published. This is not an all-data standalone rerun capsule: omitted arrays must be restored locally. Six original coarse failures and their separate successful refinement remain distinct.', '',
                  'Restore included source paths into a NEW directory with `python tools/publish_annular_20260921.py --restore DESTINATION`. Do not use the public hash-sharded directory as a runnable source tree. Local import dependencies are included; Python packages, omitted raw arrays, mutable resume and protected sibling seal dependencies are not supplied.', '',
                  'Verify committed bytes with `python tools/publish_annular_20260921.py --verify HEAD`. This checks Git blobs, all manifest entries, bounded directory counts, and local catalogue targets; it does not rerun the physics.', ''])
    write_new(ROOT / PACKAGE / 'README.md', '\n'.join(quick).encode())
    print(json.dumps(report, indent=2), flush=True)


def verify(revision):
    rows = list(csv.DictReader((ROOT / MANIFEST).open(encoding='utf-8')))
    assert len(rows) == len({row['source_path'] for row in rows})
    records = git('ls-tree', '-r', '-z', revision).split(b'\0')
    tree = {}
    for record in records:
        if record:
            header, name = record.split(b'\t', 1)
            mode, kind, oid = header.split()
            if kind == b'blob':
                tree[name.decode()] = oid.decode()
    checked = {}
    identifiers = list(dict.fromkeys(tree[row['published_path']] for row in rows if row['published_path']))
    for start in range(0, len(identifiers), 32):
        batch = identifiers[start:start + 32]
        output = subprocess.run(['git', '-C', str(ROOT), 'cat-file', '--batch'],
                                input=('\n'.join(batch) + '\n').encode(), capture_output=True,
                                check=True, timeout=120).stdout
        cursor = 0
        for oid in batch:
            end = output.index(b'\n', cursor)
            header = output[cursor:end].split()
            assert header[0].decode() == oid and header[1] == b'blob'
            size = int(header[2])
            cursor = end + 1
            content = memoryview(output)[cursor:cursor + size]
            assert len(content) == size
            checked[oid] = (size, hashlib.sha256(content).hexdigest())
            cursor += size
            assert output[cursor:cursor + 1] == b'\n'
            cursor += 1
        assert cursor == len(output)
    for row in rows:
        name = row['published_path']
        if not name:
            assert row['disposition'] == 'omitted_raw' and row['source_path'].endswith('.npz')
        else:
            assert checked[tree[name]] == (int(row['size_bytes']), row['sha256']), name
    children = {}
    for name in tree:
        if name.startswith(PACKAGE.as_posix() + '/'):
            parts = PurePosixPath(name).parts
            for index in range(len(PACKAGE.parts), len(parts)):
                children.setdefault('/'.join(parts[:index]), set()).add(parts[index])
    assert max(map(len, children.values())) < 1000
    from urllib.parse import unquote
    for path in (ROOT / PACKAGE).rglob('*.md'):
        if 'files' in path.relative_to(ROOT / PACKAGE).parts:
            continue
        for target in re.findall(r'\]\(([^)]+)\)', path.read_text(encoding='utf-8')):
            assert (path.parent / unquote(target)).resolve().is_file(), (path, target)
    print(json.dumps(dict(revision=revision, inventory_rows=len(rows), verified_unique_git_blobs=len(checked),
                          maximum_new_directory_entries=max(map(len, children.values())), all_included_bytes_match=True), indent=2))


def restore(destination):
    if destination.exists():
        raise FileExistsError('Restore destination must not already exist')
    rows = list(csv.DictReader((ROOT / MANIFEST).open(encoding='utf-8')))
    for row in rows:
        if row['published_path']:
            source = ROOT / row['published_path']
            assert digest(source) == row['sha256']
            write_new(destination / safe_relative(row['source_path']), source.read_bytes())
    print('Restored included files only. Consult MANIFEST.csv for omitted raw arrays and README.md for runtime omissions.')


def main():
    parser = argparse.ArgumentParser()
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument('--export', type=Path)
    modes.add_argument('--verify')
    modes.add_argument('--restore', type=Path)
    args = parser.parse_args()
    if args.export:
        export(args.export.resolve())
    elif args.verify:
        verify(args.verify)
    else:
        restore(args.restore.resolve())


if __name__ == '__main__':
    main()
