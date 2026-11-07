import os
import shutil
import subprocess
import time
from pathlib import Path

import psutil

from common import ROOT as STAGE, PRIOR, NATIVE, EARLY, modest, guard, require, read, write, digest, check_prior

ROOT = STAGE / "build"


def main():
    modest()
    check_prior()
    accepted = read(PRIOR / "full-cadence/native-result.json")
    for path, checksum in accepted["protected_source_hashes"].items():
        require(digest(path) == checksum, "changed protected input")
    receipt_path = NATIVE.parent / "runs/build-1/status.json"
    original = read(receipt_path)
    require(original["state"] == "complete", "original build incomplete")
    require(original["dll_sha256"] == digest(NATIVE / "camb/cambdll.dll"), "unowned original DLL")
    for path, checksum in original["input_hashes"].items():
        require(digest(path) == checksum, "original compiler input changed: " + path)
    package = ROOT / "native"
    package.mkdir(exist_ok=False)
    shutil.copytree(NATIVE / "camb", package / "camb", ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "*.dll", "*.so"))
    shutil.copy2(NATIVE / "LICENCE.txt", package / "LICENCE.txt")
    objects = sorted((NATIVE / "fortran/WinMTS").glob("*.o"))
    require(len(objects) > 30 and sum(path.name.lower() == "camb_python.o" for path in objects) == 1, "object coverage")
    modules = sorted((NATIVE / "fortran/WinMTS").glob("*.mod"))
    hashes = {str(path): digest(path) for path in objects + modules}
    report = dict(state="running", original_build_sha256=digest(receipt_path), original_library_sha256=original["dll_sha256"],
                  original_input_hashes=original["input_hashes"], reused_object_module_hashes=hashes,
                  source_hashes={name: digest(ROOT / name) for name in ("MTSTwoField.f90", "equations.f90", "camb_python.f90")}, commands=[], processes=[])
    mapped = []
    try:
        for drive, target in (("T:", EARLY / "toolchain/mingw64"), ("R:", NATIVE), ("S:", ROOT)):
            require(not Path(drive + "/").exists(), "occupied mapping " + drive)
            subprocess.run(["subst", drive, str(target)], check=True, creationflags=subprocess.CREATE_NO_WINDOW)
            mapped.append(drive)
        flags = ["-BT:/" + suffix + "/" for suffix in ("libexec/gcc/x86_64-w64-mingw32/14.2.0", "lib", "bin", "lib/gcc/x86_64-w64-mingw32/14.2.0", "x86_64-w64-mingw32/lib")]
        flags += ["-LT:/" + suffix + "/" for suffix in ("lib", "lib/gcc/x86_64-w64-mingw32/14.2.0", "x86_64-w64-mingw32/lib")]
        flags += ["-shared", "-static", "-cpp", "-fopenmp", "-O2", "-fcheck=bounds", "-fmax-errors=4", "-ffree-line-length-none"]
        rebuilt = ("MTSTwoField", "equations", "camb_python")
        commands = [["T:/bin/gfortran.exe", *flags, name + ".f90", "-c", "-o", name + ".o", "-JS:/", "-IS:/", "-IR:/fortran/WinMTS"] for name in rebuilt]
        lookup = {name.lower() + ".o": name + ".o" for name in rebuilt}
        inputs = ["S:/" + lookup[path.name.lower()] if path.name.lower() in lookup else "R:/fortran/WinMTS/" + path.name for path in objects]
        commands.append(["T:/bin/gfortran.exe", *flags, *inputs, "-o", "S:/native/camb/cambdll.dll"])
        environment = dict(os.environ, PATH="T:/bin;" + os.environ["PATH"])
        with (ROOT / "compiler.log").open("x", encoding="utf-8") as log:
            for command in commands:
                guard()
                process = subprocess.Popen(command, cwd="S:/", env=environment, stdout=log, stderr=log, creationflags=subprocess.CREATE_NO_WINDOW)
                child = psutil.Process(process.pid)
                identity = dict(pid=process.pid, created=child.create_time(), command=command, children=[])
                report["processes"].append(identity)
                report["commands"].append(command)
                known = set()
                while process.poll() is None:
                    for descendant in child.children(recursive=True):
                        try:
                            key = (descendant.pid, descendant.create_time())
                            if key not in known:
                                known.add(key)
                                identity["children"].append(dict(pid=descendant.pid, created=key[1], command=descendant.cmdline()))
                        except psutil.NoSuchProcess:
                            pass
                    time.sleep(.1)
                identity["exit_code"] = process.wait()
                require(identity["exit_code"] == 0, "compiler failed; preserve receipt")
        for path, checksum in hashes.items():
            require(digest(path) == checksum, "original object/module changed")
        for path, checksum in accepted["protected_source_hashes"].items():
            require(digest(path) == checksum, "parent changed during build")
        data_folder = package / "fortran"
        data_folder.mkdir()
        source = NATIVE / "fortran/HighLExtrapTemplate_lenspotentialCls.dat"
        shutil.copy2(source, data_folder / source.name)
        require(digest(source) == digest(data_folder / source.name), "import data copy")
        report.update(state="complete", dll_sha256=digest(package / "camb/cambdll.dll"),
                      compiler_sha256=digest(EARLY / "toolchain/mingw64/bin/gfortran.exe"),
                      copied_package_hashes={str(path): digest(path) for path in package.rglob("*") if path.is_file()})
    except BaseException as error:
        report.update(state="failed", error=repr(error))
        raise
    finally:
        for drive in reversed(mapped):
            subprocess.run(["subst", drive, "/D"], check=True, creationflags=subprocess.CREATE_NO_WINDOW)
        report["temporary_mappings_removed"] = all(not Path(drive + "/").exists() for drive in mapped)
        write(ROOT / "build-result.json", report)
        print(dict(state=report["state"], mappings_removed=report["temporary_mappings_removed"]), flush=True)


if __name__ == "__main__":
    main()
