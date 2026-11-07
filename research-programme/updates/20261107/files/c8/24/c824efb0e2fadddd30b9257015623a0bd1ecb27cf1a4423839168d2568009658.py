from __future__ import annotations

from datetime import datetime, timezone
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys

import psutil

from acquire_native import ROOT, digest


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    label = sys.argv[1]
    folder = ROOT / 'runs' / label
    folder.mkdir(parents=True, exist_ok=False)
    mapped = False
    report = dict(state='running', started_utc=datetime.now(timezone.utc).isoformat(), commands=[])
    try:
        if Path('R:/').exists():
            raise RuntimeError('R: is already occupied; no existing mapping will be changed')
        subprocess.run(['subst', 'R:', str(ROOT)], check=True)
        mapped = True
        native = Path('R:/native')
        compiler = 'R:/toolchain/mingw64/bin/gfortran.exe'
        environment = dict(os.environ, OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1', MKL_NUM_THREADS='1',
            PYTHONDONTWRITEBYTECODE='1', PATH='R:/toolchain/mingw64/bin;' + os.environ['PATH'])
        spec = importlib.util.spec_from_file_location('isolated_compiler', native / 'camb/_compilers.py')
        helper = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(helper)
        sources = ['../forutils/' + name.removesuffix('.f90') for name in
            helper.makefile_dict(native / 'forutils/Makefile')['SRCS'].replace('MatrixUtils.f90', '').split()]
        sources += helper.makefile_dict(native / 'fortran/Makefile_main')['SOURCEFILES'].split()
        output_dir = native / 'fortran/WinMTS'
        output_dir.mkdir(exist_ok=True)
        flags = ['-BR:/toolchain/mingw64/libexec/gcc/x86_64-w64-mingw32/14.2.0/',
            '-BR:/toolchain/mingw64/lib/', '-LR:/toolchain/mingw64/lib/',
            '-BR:/toolchain/mingw64/bin/', '-BR:/toolchain/mingw64/lib/gcc/x86_64-w64-mingw32/14.2.0/',
            '-BR:/toolchain/mingw64/x86_64-w64-mingw32/lib/',
            '-LR:/toolchain/mingw64/lib/gcc/x86_64-w64-mingw32/14.2.0/',
            '-LR:/toolchain/mingw64/x86_64-w64-mingw32/lib/', '-shared', '-static', '-cpp', '-fopenmp',
            '-O2', '-fcheck=bounds', '-fmax-errors=4']
        objects = []
        with (folder / 'log.txt').open('x', encoding='utf-8') as log:
            subprocess.run([compiler, '--version'], check=True, stdout=log, stderr=log, env=environment)
            for source in sources:
                target = 'WinMTS/' + Path(source).name + '.o'
                objects.append(target)
                command = [compiler, *flags, source + '.f90', '-c', '-o', target, '-JWinMTS']
                report['commands'].append(command)
                print('Building', source, flush=True)
                log.write(' '.join(command) + '\n')
                log.flush()
                if '--link-only' not in sys.argv:
                    subprocess.run(command, cwd=native / 'fortran', env=environment, check=True, stdout=log, stderr=log)
            command = [compiler, *flags, *objects, '-o', '../camb/cambdll.dll', '-JWinMTS']
            report['commands'].append(command)
            subprocess.run(command, cwd=native / 'fortran', env=environment, check=True, stdout=log, stderr=log)
        report.update(state='complete', dll_sha256=digest(ROOT / 'native/camb/cambdll.dll'),
            compiler_sha256=digest(ROOT / 'toolchain/mingw64/bin/gfortran.exe'),
            input_hashes={str((native / 'fortran' / (name + '.f90')).resolve()):
                digest(native / 'fortran' / (name + '.f90')) for name in sources},
            bounds_checking=True, optimization='O2', threads=1, reused_objects='--link-only' in sys.argv,
            object_hashes={name: digest(native / 'fortran' / name) for name in objects})
        (folder / 'COMPLETE').write_text('complete\n', encoding='utf-8')
    except BaseException as error:
        report.update(state='failed', error=repr(error))
        raise
    finally:
        if mapped:
            subprocess.run(['subst', 'R:', '/D'], check=True)
        report['temporary_drive_mapping_removed'] = not Path('R:/').exists()
        report['finished_utc'] = datetime.now(timezone.utc).isoformat()
        (folder / 'status.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print('Isolated native library built', flush=True)


if __name__ == '__main__':
    main()
