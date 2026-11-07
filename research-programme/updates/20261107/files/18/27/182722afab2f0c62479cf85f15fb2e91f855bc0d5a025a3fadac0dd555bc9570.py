import ast
import csv
import math
import os
import re
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import psutil

from common import ROOT, POST, PRIOR, PAIRED, BRANCH, BRIDGE, modest, require, read, write, digest
from probe_analysis import physical


def gone(identity):
    created = identity["created"]
    stamp = datetime.fromisoformat(created.replace("Z", "+00:00")).timestamp() if isinstance(created, str) else created
    try:
        process = psutil.Process(identity["pid"])
        return abs(process.create_time() - stamp) >= .01
    except psutil.NoSuchProcess:
        return True


def load_packet(path):
    with np.load(path) as data:
        return {key: data[key].copy() for key in data.files}


def main():
    modest()
    checks, process_receipts = [], []

    def check(name, value):
        checks.append(dict(name=name, passed=bool(value)))
        require(value, name)

    build = read(ROOT / "build-result.json")
    for path, checksum in build["original_input_hashes"].items():
        check("original build source " + Path(path).name, digest(path) == checksum)
    check("original compiled objects unchanged", all(digest(path) == checksum for path, checksum in build["reused_object_module_hashes"].items()))
    check("isolated package unchanged", all(digest(path) == checksum for path, checksum in build["copied_package_hashes"].items()))
    check("driver source owner", digest(ROOT / "camb_python.f90") == build["source_sha256"])
    check("DLL owner", digest(ROOT / "native/camb/cambdll.dll") == build["dll_sha256"])
    check("import data owner", digest(ROOT / "native/fortran/HighLExtrapTemplate_lenspotentialCls.dat") == read(ROOT / "import-data.json")["sha256"])
    old_native = read(PAIRED / "native-probe-result.json")
    check("inherited calibration unchanged", digest(BRANCH / "cosmology-reconnection-20261006/results/comparison/status.json") == old_native["inherited_parameters_sha256"])
    check("old paired failure preserved", digest(PAIRED / "probe-check-result.json") == "b415792c4a89383239d2481a543117855d7b3a8419a57a4594f9885468f81fdd" and not read(PAIRED / "probe-check-result.json")["passed"])
    cross_cadence = []
    for folder in (ROOT, ROOT / "phase-resolved"):
        native = read(folder / "tangent-native-result.json")
        result = read(folder / "tangent-check-result.json")
        script = "run_tangent.py" if folder == ROOT else "run_phase_tangent.py"
        check(folder.name + " producer owner", digest(ROOT / script) == native["source_sha256"])
        check(folder.name + " native completed", native["state"] == "complete" and len(native["reports"]) == 14)
        check(folder.name + " checker unchanged", result["source_sha256"] == digest(ROOT / "check_tangent.py") and result["analysis_source_sha256"] == digest(ROOT / "probe_analysis.py"))
        check(folder.name + " source linkage", result["native_result_sha256"] == digest(folder / "tangent-native-result.json"))
        check(folder.name + " numerical gates", result["passed"] and result["response_gate"] == 2e-5 and result["constraint_gate"] == 1e-10)
        for path, checksum in native["original_source_hashes"].items():
            check(folder.name + " input " + Path(path).name, digest(path) == checksum)
        for row in native["reports"]:
            path = folder / "packets" / row["file"]
            check(str(path.relative_to(ROOT)) + " hash", digest(path) == row["sha256"])
            data = load_packet(path)
            growth = data["names"].tolist().index("growth")
            columns = np.arange(len(data["names"])) != growth
            check(row["file"] + " physical arrays finite", np.isfinite(data["full_observer"]).all() and np.isfinite(data["full_standard"][:, columns]).all())
            check(row["file"] + " undefined diagnostic explicit", np.array_equal(np.isfinite(data["full_standard"][:, growth]), data["growth_defined"]))
            check(row["file"] + " original probes preserved", len(data["times"]) == 387 and np.array_equal(data["full_times"][data["original_indices"]], data["times"]))
            if row["direct"]:
                check(row["file"] + " full-state hook", row["hook"]["count"] == 1 and row["hook"]["untouched"] == row["hook"]["cache_max"] == 0 and row["hook"]["flags"] == [0, 0, 1, 0])
            if row["tag"] == "zero":
                check(row["file"] + " zero physical direction", all(np.count_nonzero(value) == 0 for value in physical(data, row["model"]).values()))
            if row["tag"] == "off":
                check(row["file"] + " baseline overlap", max(row["original_observer_error"], row["original_standard_error"]) < 2e-5)
            if row["tag"] == "restart":
                check(row["file"] + " ordinary restart", row["restart_error"] < 2e-5)
        for row in result["reports"]:
            check(folder.name + row["model"] + " response owner", digest(folder / row["file"]) == row["sha256"])
            check(folder.name + row["model"] + " response gates", row["max_constraint"] < 1e-10 and all(item["zero_max"] == 0 and max(item["parity"], item["half_error"], item["negative_half_error"]) < 2e-5 for item in row["checks"]))
    for model in ("heavy", "cold"):
        old = load_packet(ROOT / f"packets/{model}-3-one.npz")
        new = load_packet(ROOT / f"phase-resolved/packets/{model}-3-one.npz")
        indices = np.searchsorted(new["full_times"], old["full_times"])
        check(model + " every original timestamp retained", np.array_equal(new["full_times"][indices], old["full_times"]))
        check(model + " unchanged initial cadence", np.array_equal(new["full_times"][:new["original_indices"][0]], old["full_times"][:old["original_indices"][0]]))
        old_physical, new_physical = physical(old, model), physical(new, model)
        errors = {name: float(np.max(abs(new_physical[name] - value)) / max(float(np.max(abs(new_physical[name]))), 1e-30)) for name, value in old_physical.items()}
        check(model + " direct response stable under sampling repair", max(errors.values()) < 2e-5)
        cross_cadence.append(dict(model=model, errors=errors))
    failed = read(ROOT / "continuous-replay-result.json")
    replay = read(ROOT / "phase-resolved/continuous-replay-result.json")
    check("sparse continuous failure preserved", not failed["passed"] and all(not row["passed"] for row in failed["reports"]))
    check("same continuous checker", failed["source_sha256"] == replay["source_sha256"] == digest(ROOT / "replay_full_tangent.py"))
    check("continuous repaired result accepted", replay["passed"] and replay["gate"] == 2e-5 and replay["metric_supplied"] and not replay["independently_anchored_windows"])
    for row in replay["reports"]:
        check(row["model"] + " continuous source owner", digest(ROOT / "phase-resolved/continuous-replay" / row["file"]) == row["sha256"])
        check(row["model"] + " continuous fixed gate", max(row["maximum_error"], max(row["refinements"])) < 2e-5 and row["max_source_phase_spacing"] <= .025)
        with np.load(ROOT / "phase-resolved/continuous-replay" / row["file"]) as data:
            errors = np.max(abs(data["predicted"] - data["expected"][None, :, :]), axis=1) / data["normalization"]
            check(row["model"] + " saved evolution evidence", np.allclose(errors, data["errors"], rtol=1e-12, atol=0) and abs(float(np.max(errors)) - row["maximum_error"]) < 1e-15)
    newton = read(ROOT / "newton-response-result.json")
    check("Newton split owner", newton["passed"] and newton["source_sha256"] == digest(ROOT / "bound_newton_response.py") and newton["output_sha256"] == digest(ROOT / "newton-response.csv"))
    check("Newton budgets and propagation", all(row["split_error"] < 1e-10 and max(row["velocity_replay_error"], row["source_refinement"]) < 2e-5 and row["force_error"] <= row["force_triangle_budget"] and row["bound_residual"] < 1e-10 for row in newton["reports"]))
    with (ROOT / "newton-response.csv").open(newline="") as stream:
        rows = list(csv.DictReader(stream))
    check("24 finite Newton comparison rows", len(rows) == 24 and all(math.isfinite(float(value)) for row in rows for key, value in row.items() if key != "model"))
    for path in ROOT.glob("*.py"):
        compile(ast.parse(path.read_text()), str(path), "exec")
    check("no bytecode cache", not list(ROOT.rglob("__pycache__")))
    for label in ("build-01", "native-01", "checks-01", "continuous-01", "phase-native-01", "phase-checks-01", "phase-continuous-01", "newton-01"):
        start, end = read(ROOT / (label + ".start.json")), read(ROOT / (label + ".end.json"))
        check(label + " outcome preserved", all(start[key] == end[key] for key in start) and end["exit_code"] == (1 if label == "continuous-01" else 0))
        check(label + " exact worker exited", gone(end))
        process_receipts.append(end)
    temp_files = set()
    for compiler in build["processes"]:
        for identity in [compiler] + compiler["children"]:
            check("compiler " + str(identity["pid"]) + " exited", gone(identity))
            process_receipts.append(identity)
            for argument in identity["command"]:
                matched = re.search(r"[A-Za-z]:[\\/]Temp[\\/][^\"']+", argument)
                if matched:
                    temp_files.add(matched.group())
    check("compiler temporary files removed", all(not Path(path).exists() for path in temp_files))
    check("temporary mappings removed", build["temporary_mappings_removed"] and all(not Path(drive + ":/").exists() for drive in ("T", "R", "S")))
    for process in psutil.process_iter(["pid", "name", "cmdline"]):
        if process.info["pid"] != os.getpid() and "python" in (process.info["name"] or "").lower():
            check("no concurrent task worker " + str(process.info["pid"]), not any(marker in " ".join(process.info["cmdline"] or []) for marker in (ROOT.name, PRIOR.name, PAIRED.name, "source-readout-bridge-20261102")))
    check("ray map unchanged", digest(BRIDGE / "final-stable-real-batch-rays037-038/common-coverage.json") == "95d628bbe34ddc317e1d954d8e556271d666645e259f0eda66245be0607a0db3")
    document = POST / "MTS-DIRECT-TANGENT-AND-NEWTON-FORCE-BOUND.md"
    check("handoff exists", document.is_file())
    sources = list(ROOT.glob("*.py")) + [ROOT / name for name in ("PROTOCOL.md", "CONTINUOUS-REPLAY-PROTOCOL.md", "PHASE-OUTPUT-DECISION.md", "run.ps1", "camb_python.f90")] + [document]
    write(ROOT / "validation-result.json", dict(passed=True, pid=os.getpid(), completed=datetime.now(timezone.utc).isoformat(),
        checks=checks, cross_cadence=cross_cadence, process_receipts=process_receipts, compiler_temp_files=sorted(temp_files),
        source_hashes={str(path): digest(path) for path in sources},
        response_sha256=digest(ROOT / "phase-resolved/tangent-check-result.json"),
        replay_sha256=digest(ROOT / "phase-resolved/continuous-replay-result.json"),
        newton_sha256=digest(ROOT / "newton-response-result.json"),
        original_failures_preserved=True, scope="Direct linear response, phase-resolved continuous field replay, and explicit cosmological Newton-force/interpolant budgets. No continuum or static-local theorem claimed."))
    print(dict(passed=True, checks=len(checks), cross_cadence_max=[dict(model=row["model"], maximum=max(row["errors"].values())) for row in cross_cadence]), flush=True)


if __name__ == "__main__":
    main()
