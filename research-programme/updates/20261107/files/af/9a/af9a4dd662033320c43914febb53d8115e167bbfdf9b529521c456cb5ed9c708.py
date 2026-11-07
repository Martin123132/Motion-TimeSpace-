from __future__ import annotations

import difflib
import zipfile

from native_common import *


def main():
    modest()
    acquisition = json.loads((ROOT / 'sources/acquisition.json').read_text())
    changed = []
    for relative, expected in acquisition['pristine_native_hashes'].items():
        current = ROOT / 'native' / relative
        assert current.is_file(), current
        if digest(current) != expected:
            changed.append(Path(relative).as_posix())
    allowed = ['fortran/Makefile_main', 'fortran/equations.f90', 'fortran/camb_python.f90', 'camb/model.py']
    assert set(changed) == set(allowed), changed
    additions = ['fortran/MTSTwoField.f90', 'camb/mts.py']
    patch = []
    with zipfile.ZipFile(ROOT / 'sources/camb.zip') as pristine:
        prefix = pristine.namelist()[0].split('/')[0]
        for relative in sorted(changed + additions):
            before = pristine.read(prefix + '/' + relative).decode('utf-8').splitlines(keepends=True) if relative in changed else []
            after = (ROOT / 'native' / relative).read_text(encoding='utf-8').splitlines(keepends=True)
            patch.extend(difflib.unified_diff(before, after, fromfile='a/' + relative if before else '/dev/null', tofile='b/' + relative))
    patch_path = ROOT / 'sources/native-source-delta.patch'
    patch_path.write_text(''.join(patch), encoding='utf-8')
    archive_path = ROOT / 'sources/native-source-delta.zip'
    with zipfile.ZipFile(archive_path, 'x', compression=zipfile.ZIP_DEFLATED) as archive:
        for relative in sorted(changed + additions):
            archive.write(ROOT / 'native' / relative, relative)
    with zipfile.ZipFile(archive_path) as archive:
        assert len(archive.namelist()) == 6
        for relative in archive.namelist():
            assert archive.read(relative) == (ROOT / 'native' / relative).read_bytes()
    folder = ROOT / 'results/source-delta'
    folder.mkdir(parents=True, exist_ok=False)
    finish(folder, dict(changed_upstream_files=changed, added_source_files=additions,
        zipped_source_count=6, archive_roundtrip_verified=True, unused_upstream_files_unchanged=True), __file__,
        [ROOT / 'sources/acquisition.json', patch_path, archive_path])
    print('Six-file source delta packaged and verified; all other upstream sources unchanged', flush=True)


if __name__ == '__main__':
    main()
