import importlib.util
import shutil
from common import ROOT, PAIRED, NATIVE, HIERARCHY, CLOSURE, modest, check_prior, require, read, write, digest


def main():
    modest()
    check_prior()
    owner = PAIRED / "build_probe.py"
    validated = read(PAIRED / "validation-result.json")
    require(digest(owner) == validated["source_hashes"][str(owner)], "retained builder changed")
    spec = importlib.util.spec_from_file_location("retained_isolated_builder", owner)
    builder = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(builder)
    builder.ROOT = ROOT / "build"
    builder.main()
    target = ROOT / "build/native/fortran"
    target.mkdir(exist_ok=False)
    source = NATIVE / "fortran/HighLExtrapTemplate_lenspotentialCls.dat"
    shutil.copy2(source, target / source.name)
    require(digest(source) == digest(target / source.name), "import data copy")
    write(ROOT / "build/import-data.json", dict(source=str(source), sha256=digest(source), original_adapter=str(CLOSURE / "build/camb_python.f90"), original_adapter_sha256=digest(CLOSURE / "build/camb_python.f90"), reused_builder=str(owner), builder_sha256=digest(owner), wrapper_sha256=digest(__file__)))


if __name__ == "__main__":
    main()
