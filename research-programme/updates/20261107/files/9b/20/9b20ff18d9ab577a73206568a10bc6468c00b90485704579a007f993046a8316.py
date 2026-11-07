import ast
import difflib
import os
import re
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import psutil

from common import ROOT, POST, PRIOR, NATIVE, BRIDGE, modest, require, read, write, digest
from probe_analysis import packet, physical, algebraic


def process_gone(identity):
    created = identity["created"]
    stamp = datetime.fromisoformat(created.replace("Z", "+00:00")).timestamp() if isinstance(created, str) else created
    try:
        current = psutil.Process(identity["pid"])
        same = abs(current.create_time() - stamp) < .01
        return not same, dict(pid=identity["pid"], created=created, same_identity_alive=same, current_command=current.cmdline())
    except psutil.NoSuchProcess:
        return True, dict(pid=identity["pid"], created=created, same_identity_alive=False)


def main():
    modest()
    checks, processes = [], []

    def check(name, passed):
        checks.append(dict(name=name, passed=bool(passed)))
        require(passed, name)

    native = read(ROOT / "native-probe-result.json")
    build = read(ROOT / "build-result.json")
    result = read(ROOT / "probe-check-result.json")
    replay = read(ROOT / "replay-result.json")
    for path, checksum in native["original_source_hashes"].items():
        check("original input " + Path(path).name, digest(path) == checksum)
    for path, checksum in build["original_input_hashes"].items():
        check("original build source " + Path(path).name, digest(path) == checksum)
    check("reused original objects and modules unchanged", all(digest(path) == checksum for path, checksum in build["reused_object_module_hashes"].items()))
    check("copied package unchanged", all(digest(path) == checksum for path, checksum in build["copied_package_hashes"].items()))
    check("isolated driver owner", build["source_sha256"] == digest(ROOT / "camb_python.f90"))
    check("isolated DLL owner", build["dll_sha256"] == digest(ROOT / "native/camb/cambdll.dll"))
    changes = list(difflib.ndiff((NATIVE / "fortran/camb_python.f90").read_text().splitlines(), (ROOT / "camb_python.f90").read_text().splitlines()))
    check("original driver lines preserved", not any(line.startswith("- ") for line in changes))
    check("observer still original", digest(PRIOR / "observer.dll") == native["observer_sha256"])
    check("retained parameter factory", digest(NATIVE.parent / "matching_common.py") == native["params_factory_sha256"])
    asset = ROOT / "native/fortran/HighLExtrapTemplate_lenspotentialCls.dat"
    check("import data repair exact", digest(asset) == digest(NATIVE / "fortran" / asset.name) == "506ddef3d81ae0b5e62b675742c87f0de09fa2b39a31fdebf3091d3e0197c44f")
    for script, key, report in (("run_native_probe.py", "source_sha256", native), ("check_probe.py", "source_sha256", result),
                               ("probe_analysis.py", "analysis_source_sha256", result), ("replay_response.py", "source_sha256", replay)):
        check(script + " receipt owner", digest(ROOT / script) == report[key])
    check("result linkage", result["native_result_sha256"] == digest(ROOT / "native-probe-result.json") and replay["input_sha256"] == digest(ROOT / "probe-check-result.json"))
    check("unchanged numerical gates", result["response_gate"] == replay["gate"] == 2e-5 and result["constraint_gate"] == 1e-10)
    check("48 completed runs", native["state"] == "complete" and len(native["reports"]) == 48)
    expected = {(model, index, tag) for model in ("heavy", "cold") for index in range(4) for tag in ("off", "zero", "plus", "minus", "halfplus", "halfminus")}
    check("run coverage", {(row["model"], row["index"], row["tag"]) for row in native["reports"]} == expected)
    for row in native["reports"]:
        check(row["file"] + " hash", digest(ROOT / "packets" / row["file"]) == row["sha256"])
        data = packet(row["model"], row["index"], row["tag"])
        check(row["file"] + " shape and finiteness", data["observer"].shape == (387, 30) and np.isfinite(data["observer"]).all() and np.isfinite(data["standard"]).all())
        check(row["file"] + " constraints", algebraic(data) < 1e-10)
        if row["tag"] == "off":
            check(row["file"] + " original overlap", max(row["observer_original_error"], row["standard_original_error"]) < 2e-5)
        else:
            check(row["file"] + " exact hook ownership", row["hook"]["count"] == 1 and row["hook"]["untouched"] == 0)
        if row["tag"] == "zero":
            check(row["file"] + " zero restart", max(row["restart_observer_error"], row["restart_standard_error"]) < 2e-5)
    for model in ("heavy", "cold"):
        for index in range(4):
            rows = [row for row in native["reports"] if row["model"] == model and row["index"] == index]
            check(f"{model}/{index} unchanged pre-slice", len({row["prefix_hash"] for row in rows}) == 1)
    failures = []
    for row in result["reports"]:
        path = ROOT / row["response_file"]
        check(path.name + " owner", digest(path) == row["response_sha256"])
        high = physical(packet(row["model"], row["index"], "plus"), row["model"])
        low = physical(packet(row["model"], row["index"], "minus"), row["model"])
        with np.load(path) as data:
            recomputed = np.column_stack([(high[key] - low[key]) / .2 for key in data["names"].tolist()])
            check(path.name + " central difference", np.array_equal(recomputed, data["values"]))
        passed = all(max(item["symmetry_error"], item["step_error"]) < 2e-5 for item in row["checks"]) and row["constraint_error"] < 1e-10
        check(path.name + " honest acceptance", passed == row["passed"])
        if not passed:
            failures.append(dict(model=row["model"], k=row["k"], unresolved=[item["variable"] for item in row["checks"] if not item["passed"]]))
    check("preserved all-species failure", not result["passed"] and not replay["all_species_source_passed"] and failures == [dict(model="heavy", k=5., unresolved=["Pi", "delta_b", "delta_gamma", "delta_neutrino"])])
    check("24 local replays distinct from source gate", replay["passed"] and len(replay["reports"]) == 24)
    for row in replay["reports"]:
        check(row["file"] + " replay owner", digest(ROOT / "replay" / row["file"]) == row["sha256"])
        check(row["file"] + " unchanged replay gate", row["passed"] and max(row["maximum_error"], max(row["measured_refinements"])) < 2e-5)
        check(row["file"] + " source failure retained", row["source_all_species_passed"] == (not (row["model"] == "heavy" and row["k"] == 5.)))
        with np.load(ROOT / "replay" / row["file"]) as data:
            errors = np.max(abs(data["prediction"] - data["expected"]), axis=0) / data["normalization"]
            feedback = np.max(abs(data["prediction"] - data["frozen"]), axis=0) / data["normalization"]
            check(row["file"] + " measured response", np.array_equal(errors, data["errors"]) and np.array_equal(feedback, data["feedback"]))
    for path in ROOT.glob("*.py"):
        compile(ast.parse(path.read_text(encoding="utf-8")), str(path), "exec")
    check("no bytecode cache", not list(ROOT.rglob("__pycache__")))
    for label, code in (("build-01", 0), ("native-01", 1), ("native-02", 0), ("checks-01", 1), ("replay-01", 0)):
        start, end = read(ROOT / (label + ".start.json")), read(ROOT / (label + ".end.json"))
        check(label + " documented outcome", end["exit_code"] == code and all(start[key] == end[key] for key in start))
        gone, identity = process_gone(end)
        processes.append(identity)
        check(label + " worker exited", gone)
    temporary_files = set()
    for compiler in build["processes"]:
        for item in [compiler] + compiler["children"]:
            gone, identity = process_gone(item)
            processes.append(identity)
            check("compiler process " + str(item["pid"]) + " exited", gone)
            for argument in item["command"]:
                matched = re.search(r"[A-Za-z]:[\\/]Temp[\\/][^\"']+", argument)
                if matched:
                    temporary_files.add(matched.group())
    check("observed compiler temp files removed", all(not Path(path).exists() for path in temporary_files))
    check("temporary drive mappings removed", build["temporary_mappings_removed"] and all(not Path(drive + ":/").exists() for drive in ("T", "R", "S")))
    for process in psutil.process_iter(["pid", "name", "cmdline"]):
        if process.info["pid"] == os.getpid() or "python" not in (process.info["name"] or "").lower():
            continue
        command = " ".join(process.info["cmdline"] or [])
        check("no other stage worker " + str(process.info["pid"]), not any(marker in command for marker in (ROOT.name, PRIOR.name, "source-readout-bridge-20261102")))
    check("previous accepted metric result preserved", digest(PRIOR / "full-cadence/feedback-result.json") == "90cc1138b63a6a53c01d40f482a02f16730fba93e6056996bb51ffa1db08ad7f")
    check("accepted rays unchanged", digest(BRIDGE / "final-stable-real-batch-rays037-038/common-coverage.json") == "95d628bbe34ddc317e1d954d8e556271d666645e259f0eda66245be0607a0db3")
    document = POST / "MTS-CHANGED-STATE-GRAVITY-FEEDBACK.md"
    check("physical handoff exists", document.is_file())
    sources = list(ROOT.glob("*.py")) + [ROOT / name for name in ("PROTOCOL.md", "IMPORT-REPAIR.md", "run.ps1", "camb_python.f90")] + [document, asset]
    write(ROOT / "validation-result.json", dict(passed=True, pid=os.getpid(), completed=datetime.now(timezone.utc).isoformat(),
        checks=checks, all_species_source_passed=False, all_local_replays_passed=True,
        passing_source_cases=7, unresolved=failures, observed_processes=processes,
        compiler_temporary_paths=sorted(temporary_files), source_hashes={str(path): digest(path) for path in sources},
        response_result_sha256=digest(ROOT / "probe-check-result.json"), replay_result_sha256=digest(ROOT / "replay-result.json"),
        scope="Provenance, accurate mixed scientific outcome, replay checks and cleanup; validation success is not an all-species source pass."))
    print(dict(validation_passed=True, checks=len(checks), passing_source_cases=7, local_replays=24, unresolved=failures), flush=True)


if __name__ == "__main__":
    main()
