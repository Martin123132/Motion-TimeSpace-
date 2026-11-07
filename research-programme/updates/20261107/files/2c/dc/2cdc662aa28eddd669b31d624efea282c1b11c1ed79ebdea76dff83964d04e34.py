from __future__ import annotations

import shutil
from stage_common import *


def main():
    modest()
    folder = ROOT / 'sources/bootstrap'
    folder.mkdir(parents=True, exist_ok=False)
    ignored = shutil.ignore_patterns('WinMTS', '__pycache__', '*.dll', '*.pyc')
    shutil.copytree(PARENT / 'native', ROOT / 'native', ignore=ignored)
    source_hashes = {str(path.relative_to(ROOT / 'native')): digest(path)
        for path in (ROOT / 'native').rglob('*') if path.is_file()}
    for relative, expected in source_hashes.items():
        assert digest(PARENT / 'native' / relative) == expected
    finish(folder, dict(copied_source_hashes=source_hashes, global_installation_changed=False,
        compiler_reused_read_only=str(PARENT / 'toolchain/mingw64/bin/gfortran.exe')),
        __file__, [PARENT / 'toolchain/mingw64/bin/gfortran.exe', PARENT / 'native/camb/cambdll.dll'])


if __name__ == '__main__':
    main()
