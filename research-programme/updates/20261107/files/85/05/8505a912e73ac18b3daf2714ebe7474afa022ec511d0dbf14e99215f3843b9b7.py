from __future__ import annotations

import importlib.util
import subprocess
from stage_common import *


def main():
    modest()
    folder = ROOT / 'runs' / sys.argv[1]
    folder.mkdir(parents=True, exist_ok=False)
    mapped = False
    report = dict(state='running', commands=[])
    try:
        if Path('R:/').exists():
            raise RuntimeError('R: already occupied; refusing to change it')
        subprocess.run(['subst', 'R:', str(ROOT.parent)], check=True)
        mapped = True
        native = Path('R:/') / ROOT.name / 'native'
        chain = Path('R:/') / PARENT.name / 'toolchain/mingw64'
        compiler = str(chain / 'bin/gfortran.exe')
        environment = dict(os.environ, PATH=str(chain / 'bin') + ';' + os.environ['PATH'])
        spec = importlib.util.spec_from_file_location('isolated_compiler', native / 'camb/_compilers.py')
        helper = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(helper)
        sources = ['../forutils/' + name.removesuffix('.f90') for name in
            helper.makefile_dict(native / 'forutils/Makefile')['SRCS'].replace('MatrixUtils.f90', '').split()]
        sources += helper.makefile_dict(native / 'fortran/Makefile_main')['SOURCEFILES'].split()
        (native / 'fortran/WinMTS').mkdir(exist_ok=True)
        flags = ['-B' + (chain / suffix).as_posix() + '/' for suffix in
            ['libexec/gcc/x86_64-w64-mingw32/14.2.0', 'lib', 'bin',
             'lib/gcc/x86_64-w64-mingw32/14.2.0', 'x86_64-w64-mingw32/lib']]
        flags += ['-L' + (chain / suffix).as_posix() + '/' for suffix in
            ['lib', 'lib/gcc/x86_64-w64-mingw32/14.2.0', 'x86_64-w64-mingw32/lib']]
        flags += ['-shared', '-static', '-cpp', '-fopenmp', '-O2', '-fcheck=bounds', '-fmax-errors=4']
        objects = []
        with (folder / 'log.txt').open('x', encoding='utf-8') as log:
            subprocess.run([compiler, '--version'], check=True, stdout=log, stderr=log, env=environment)
            for source in sources:
                target = 'WinMTS/' + Path(source).name + '.o'
                objects.append(target)
                command = [compiler, *flags, source + '.f90', '-c', '-o', target, '-JWinMTS']
                report['commands'].append(command)
                print('Building', source, flush=True)
                subprocess.run(command, cwd=native / 'fortran', env=environment, check=True, stdout=log, stderr=log)
            command = [compiler, *flags, *objects, '-o', '../camb/cambdll.dll', '-JWinMTS']
            report['commands'].append(command)
            subprocess.run(command, cwd=native / 'fortran', env=environment, check=True, stdout=log, stderr=log)
        report.update(state='complete', dll_sha256=digest(ROOT / 'native/camb/cambdll.dll'),
            compiler_sha256=digest(PARENT / 'toolchain/mingw64/bin/gfortran.exe'),
            input_hashes={str((ROOT / 'native/fortran' / (name + '.f90')).resolve()):
                digest(native / 'fortran' / (name + '.f90')) for name in sources},
            bounds_checking=True, threads=1)
        (folder / 'COMPLETE').write_text('complete\n', encoding='utf-8')
    except BaseException as error:
        report.update(state='failed', error=repr(error))
        raise
    finally:
        if mapped:
            subprocess.run(['subst', 'R:', '/D'], check=True)
        report['temporary_drive_mapping_removed'] = not Path('R:/').exists()
        report['finished_utc'] = datetime.now(timezone.utc).isoformat()
        write_json(folder / 'status.json', report)


if __name__ == '__main__':
    main()
