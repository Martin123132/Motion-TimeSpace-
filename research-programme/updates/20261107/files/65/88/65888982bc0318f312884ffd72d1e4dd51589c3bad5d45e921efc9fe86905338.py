from __future__ import annotations

import hashlib
import json
from pathlib import Path
import urllib.request
import zipfile

import psutil

ROOT = Path(__file__).resolve().parent
CAMB_COMMIT = '3ef0272d6f7ba1231128872e56e6d4c12af8267b'
FORUTILS_COMMIT = '841f06d5356877e90437f94b2d976dd98f7f923c'
COMPILER_URL = 'https://github.com/brechtsanders/winlibs_mingw/releases/download/14.2.0posix-19.1.7-12.0.0-msvcrt-r3/winlibs-x86_64-posix-seh-gcc-14.2.0-mingw-w64msvcrt-12.0.0-r3.zip'


def digest(path):
    result = hashlib.sha256()
    with Path(path).open('rb') as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b''):
            result.update(block)
    return result.hexdigest()


def fetch(url, path):
    request = urllib.request.Request(url, headers={'User-Agent': 'MTS-local-research-source-acquisition'})
    with urllib.request.urlopen(request, timeout=90) as response, path.open('xb') as target:
        while block := response.read(1024 * 1024):
            target.write(block)


def unpack(path, target, strip_root):
    with zipfile.ZipFile(path) as archive:
        for member in archive.infolist():
            parts = Path(member.filename).parts
            if strip_root:
                parts = parts[1:]
            if not parts:
                continue
            destination = target.joinpath(*parts)
            assert destination.resolve().is_relative_to(target.resolve()), member.filename
            if member.is_dir():
                destination.mkdir(parents=True, exist_ok=True)
            else:
                destination.parent.mkdir(parents=True, exist_ok=True)
                with destination.open('xb') as output:
                    output.write(archive.read(member))


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    sources = ROOT / 'sources'
    sources.mkdir(exist_ok=True)
    urls = [('camb.zip', f'https://codeload.github.com/cmbant/CAMB/zip/{CAMB_COMMIT}'),
        ('forutils.zip', f'https://codeload.github.com/cmbant/forutils/zip/{FORUTILS_COMMIT}'),
        ('compiler.zip', COMPILER_URL), ('compiler.sha256', COMPILER_URL + '.sha256')]
    rows = []
    for name, url in urls:
        target = sources / name
        if not target.exists():
            print('Downloading', name, flush=True)
            fetch(url, target)
        rows.append(dict(path=str(target), url=url, bytes=target.stat().st_size, sha256=digest(target)))
    expected = (sources / 'compiler.sha256').read_text().split()[0]
    assert digest(sources / 'compiler.zip') == expected
    for name, target, strip_root in [('camb.zip', ROOT / 'native', True),
        ('forutils.zip', ROOT / 'native/forutils', True), ('compiler.zip', ROOT / 'toolchain', False)]:
        marker = sources / (name + '.extracted')
        if not marker.exists():
            print('Extracting', name, flush=True)
            unpack(sources / name, target, strip_root)
            marker.write_text(digest(sources / name) + '\n')
    native = ROOT / 'native'
    report = dict(state='complete', camb_commit=CAMB_COMMIT, forutils_commit=FORUTILS_COMMIT,
        sources=rows, compiler_publisher_sha256_verified=True,
        pristine_native_hashes={str(path.relative_to(native)): digest(path)
            for path in native.rglob('*') if path.is_file()},
        global_installation_changed=False)
    (sources / 'acquisition.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print('Source and isolated portable compiler ready', flush=True)


if __name__ == '__main__':
    main()
