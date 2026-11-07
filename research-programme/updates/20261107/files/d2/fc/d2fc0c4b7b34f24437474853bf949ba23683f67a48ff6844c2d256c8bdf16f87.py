import importlib.util
import shutil
from common import ROOT, PAIRED, NATIVE, modest, require, read, write, digest

if __name__ == "__main__":
    modest()
    owner = PAIRED / "build_probe.py"
    accepted = read(PAIRED / "validation-result.json")
    require(digest(owner) == accepted["source_hashes"][str(owner)], "builder changed")
    require(read(ROOT / "build-result.json")["state"] == "failed", "preserve failed adapter build")
    target = ROOT / "build-corrected"
    spec = importlib.util.spec_from_file_location("retained_isolated_builder", owner)
    builder = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(builder)
    builder.ROOT = target
    builder.main()
    auxiliary = target / "native/fortran"
    auxiliary.mkdir(exist_ok=False)
    source = NATIVE / "fortran/HighLExtrapTemplate_lenspotentialCls.dat"
    shutil.copy2(source, auxiliary / source.name)
    require(digest(source) == digest(auxiliary / source.name), "changed copied import data")
    write(target / "import-data.json", dict(source=str(source), sha256=digest(source), reused_builder=str(owner), builder_sha256=digest(owner), wrapper_sha256=digest(__file__)))

