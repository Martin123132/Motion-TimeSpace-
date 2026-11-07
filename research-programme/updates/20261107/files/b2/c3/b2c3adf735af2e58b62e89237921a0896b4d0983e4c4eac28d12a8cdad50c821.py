import csv
import os
from datetime import datetime
from pathlib import Path
from common import ROOT, POST, CLOSURE, HIERARCHY, BRIDGE, NATIVE, EARLY, GATE, ALGEBRA, WAVE, modest, guard, require, check_prior, read, write, digest, load
from check_pressure_corrected import analyze, symbolic, norm, scale
import numpy as np
import psutil


def gone(record):
    stamp = record["created"]
    if isinstance(stamp, str):
        stamp = datetime.fromisoformat(stamp.replace("Z", "+00:00")).timestamp()
    try:
        return abs(psutil.Process(record["pid"]).create_time() - stamp) >= .01
    except psutil.NoSuchProcess:
        return True


def main():
    modest()
    prior = check_prior()
    checks = []
    def check(name, value):
        checks.append(dict(name=name, passed=bool(value)))
        require(value, name)
    check("previous verified progress", prior["state"] == "verified_closed" and prior["previous_goal_turn_classification"] == "progress")
    build = read(ROOT / "build/build-result.json")
    imports = read(ROOT / "build/import-data.json")
    owner = read(ROOT / "readout-result.json")
    config = read(ROOT / "readout-config.json")
    result = read(ROOT / "balance-corrected/balance-result.json")
    repair = read(ROOT / "background-repair-derivation.json")
    check("build complete", build["state"] == "complete")
    for group in ("original_input_hashes", "reused_object_module_hashes", "copied_package_hashes"):
        for path, checksum in build[group].items():
            check(group + " " + path, digest(path) == checksum)
    check("adapter owned", build["source_sha256"] == digest(ROOT / "build/camb_python.f90"))
    check("library owned", build["dll_sha256"] == digest(ROOT / "build/native/camb/cambdll.dll"))
    check("compiler unchanged", build["compiler_sha256"] == digest(EARLY / "toolchain/mingw64/bin/gfortran.exe"))
    check("parent adapter unchanged", imports["original_adapter_sha256"] == digest(CLOSURE / "build/camb_python.f90"))
    check("reused builder unchanged", imports["builder_sha256"] == digest(imports["reused_builder"]))
    check("build wrapper owned", imports["wrapper_sha256"] == digest(ROOT / "build_pressure.py"))
    check("package import data identical", imports["sha256"] == digest(imports["source"]) == digest(ROOT / "build/native/fortran/HighLExtrapTemplate_lenspotentialCls.dat"))
    old_adapter = (CLOSURE / "build/camb_python.f90").read_text(encoding="utf-8")
    adapter = (ROOT / "build/camb_python.f90").read_text(encoding="utf-8")
    first = adapter.index("    subroutine mts_operator_stress")
    last = adapter.index("    subroutine GetAllocatableSize", first)
    check("readout extension only", (adapter[:first].rstrip() + "\n\n" + adapter[last:]).strip() == (old_adapter[:old_adapter.index("    subroutine GetAllocatableSize")].rstrip() + "\n\n" + old_adapter[old_adapter.index("    subroutine GetAllocatableSize"):]).strip())
    check("temporary mappings removed", build["temporary_mappings_removed"] and all(not Path(drive + ":/").exists() for drive in ("T", "R", "S")))
    for record in build["processes"]:
        check("successful compiler " + str(record["pid"]), record["exit_code"] == 0)
        for process in [record, *record["children"]]:
            check("compiler identity exited " + str(process["pid"]), gone(process))
    for name in ("cc5bLCYF.fii", "cc2Efr7b.s", "ccNPMeD5.res"):
        check("observed compiler temporary absent " + name, not (Path("D:/Temp") / name).exists())
    check("completed readout", owner["state"] == "complete" and owner["error"] is None and owner["no_new_trajectory"])
    check("source pinned", owner["source_sha256"] == config["source_sha256"] == digest(ROOT / "read_pressure.py"))
    check("config owned", owner["config_sha256"] == digest(ROOT / "readout-config.json") and config["protocol_sha256"] == digest(ROOT / "PROTOCOL.md"))
    check("build and coupled owners", owner["build_sha256"] == digest(ROOT / "build/build-result.json") and owner["coupled_owner_sha256"] == digest(CLOSURE / "prediction-result.json") and config["coupled_closeout_sha256"] == digest(CLOSURE / "closeout.json"))
    check("numerical diagnostic source", result["source_sha256"] == digest(ROOT / "check_pressure_corrected.py") and result["readout_sha256"] == digest(ROOT / "readout-result.json"))
    check("unchanged gates", result["numerical_gate"] == GATE == 2e-5 and result["algebra_gate"] == ALGEBRA == 1e-10)
    check("seven exact stress identities", result["symbolic"] == symbolic() and len(result["symbolic"]) == 7)
    check("ten exact repair identities", repair["passed"] and len(repair["identities"]) == 10 and all(value == "0" for value in repair["identities"].values()))
    check("repair proof pinned", repair["source_sha256"] == digest(ROOT / "derive_background_repair.py") and repair["diagnostic_sha256"] == digest(ROOT / "balance-corrected/balance-result.json"))
    check("no repair simulation claimed", repair["numerical_repair_executed"] is False and repair["calibration_parameters_added"] is False)
    check("paired models", len(owner["reports"]) == 2 and {row["model"] for row in owner["reports"]} == {"heavy", "cold"})
    ablations, csv_rows = [], []
    for model_owner in owner["reports"]:
        guard()
        model = model_owner["model"]
        folder = ROOT / "runs" / model
        saved_model = next(row for row in result["reports"] if row["model"] == model)
        check(model + " local owner", model_owner == read(folder / "result.json"))
        check(model + " seven tags", [row["tag"] for row in model_owner["cases"]] == config["tags"] and len(model_owner["cases"]) == 7)
        context = load(folder / "initial-context.npz")
        reference = load(HIERARCHY / "runs-balanced" / model / "native-reference.npz")
        capture = read(folder / "capture-check.json")
        check(model + " context ownership", model_owner["initial_context_sha256"] == digest(folder / "initial-context.npz") and model_owner["capture_sha256"] == digest(folder / "capture-check.json"))
        check(model + " one verified initial slice", capture["single_capture"] and not capture["future_reference_evolution_recomputed"] and all(capture[name] for name in ("exact_state", "exact_rate", "exact_observer", "exact_signature")))
        check(model + " inherited initial state", np.array_equal(context["initial"], reference["initial"]) and np.array_equal(context["initial_rate"], reference["derivative"][0]))
        check(model + " inherited window", capture["captured_time"] == reference["times"][0] and capture["authorized_last_time"] == reference["times"][-1])
        check(model + " inherited owner", model_owner["initial_reference_sha256"] == digest(HIERARCHY / "runs-balanced" / model / "native-reference.npz"))
        packets = {}
        for case in model_owner["cases"]:
            tag = case["tag"]
            label = model + " " + tag
            packet = load(folder / case["file"])
            packets[tag] = packet
            source = load(case["source_file"])
            saved = next(row for row in saved_model["cases"] if row["tag"] == tag)
            check(label + " input ownership", case["source_sha256"] == digest(case["source_file"]) == case["original_solver"]["sha256"])
            check(label + " readout ownership", case["sha256"] == digest(folder / case["file"]) == saved["input_sha256"])
            check(label + " original observer exact", case["old_observer_error"] == 0 and np.array_equal(packet["observer"], source["observer"]))
            check(label + " original grid exact", np.array_equal(packet["times"], source["times"]))
            check(label + " finite numerical arrays", all(np.isfinite(value).all() for name, value in packet.items() if name not in ("species", "term_names", "observer_names")))
            check(label + " seven species and definitions", packet["terms"].shape == (case["points"], 7, 7) and len(packet["species"]) == 7)
            check(label + " frozen directional steps", np.array_equal(packet["difference_steps"], config["difference_steps"]) and len(packet["derivative_indices"]) >= 7)
            recomputed, arrays = analyze(packet)
            check(label + " exact recorded analysis", all(recomputed[name] == saved[name] for name in recomputed))
            check(label + " independently rebuilt diagnostic passed", recomputed["numerical_passed"])
            data_path = ROOT / "balance-corrected" / saved["file"]
            stored = load(data_path)
            check(label + " derived arrays owned", saved["sha256"] == digest(data_path))
            check(label + " derived arrays exact", set(stored) == set(arrays) and all(np.array_equal(stored[key], value) for key, value in arrays.items()))
            check(label + " raw gate honest", saved["raw_balance_within_gate"] == bool(max(saved["raw_continuity"], saved["raw_momentum"]) < GATE))
            if tag != "L64-zero":
                check(label + " identified physical result", saved["raw_balance_within_gate"] == (model == "cold"))
            else:
                check(label + " true zero residual", saved["raw_continuity"] == saved["raw_momentum"] == 0)
            csv_rows.append(dict(model=model, tag=tag, numerical_passed=saved["numerical_passed"], raw_continuity=saved["raw_continuity"], raw_momentum=saved["raw_momentum"], raw_balance_within_gate=saved["raw_balance_within_gate"], decomposition_continuity=saved["decomposition_continuity"], decomposition_momentum=saved["decomposition_momentum"], fine_integral_D=saved["integrals"][0]["defect_accounted_error"][0], fine_integral_Q=saved["integrals"][0]["defect_accounted_error"][1]))
            if tag == "G192-fine":
                hubble = packet["metadata"][:, 1]
                missing_pressure_c = arrays["continuity_residual"] - arrays["predicted_continuity"] - 3 * hubble * arrays["pressure"]
                missing_pressure_e = arrays["momentum_residual"] - arrays["predicted_momentum"] + WAVE * arrays["pressure"]
                ablation = dict(model=model, zero_pressure_continuity=norm(missing_pressure_c) / saved["continuity_scale"], zero_pressure_momentum=norm(missing_pressure_e) / saved["momentum_scale"])
                ablations.append(ablation)
                check(model + " independent pressure necessary", max(ablation["zero_pressure_continuity"], ablation["zero_pressure_momentum"]) > GATE)
        dynamic = [0, 1, 2, 3, 4, 6]
        check(model + " zero pressure/source control", np.count_nonzero(packets["L64-zero"]["terms"][:, :, dynamic]) == 0 and saved_model["zero"])
        check(model + " exact sign reversal", np.array_equal(-packets["L64-negative"]["terms"][:, :, dynamic], packets["L64-base"]["terms"][:, :, dynamic]) and saved_model["sign_error"] == 0)
    check("diagnostic passed, not heavy conservation", result["numerical_passed"] and result["physical_residuals_reported_without_redefining_tolerance"])
    csv_path = ROOT / "balance-corrected/pressure-balance.csv"
    with csv_path.open(newline="", encoding="utf-8") as stream:
        actual_csv = list(csv.DictReader(stream))
    check("fourteen clean CSV rows", len(actual_csv) == 14 and all(None not in row and None not in row.values() for row in actual_csv))
    check("CSV owned and exact", result["csv_sha256"] == digest(csv_path) and actual_csv == [{key: str(value) for key, value in row.items()} for row in csv_rows])
    original = read(ROOT / "balance-result.json")
    check("original zero-norm failure retained", not original["numerical_passed"] and (ROOT / "METRIC-REPAIR.md").is_file())
    for old_model, new_model in zip(original["reports"], result["reports"]):
        for old_case, new_case in zip(old_model["cases"], new_model["cases"]):
            if old_case["tag"] != "L64-zero":
                check(old_model["model"] + old_case["tag"] + " physical findings unchanged by metric repair", old_case["raw_continuity"] == new_case["raw_continuity"] and old_case["raw_momentum"] == new_case["raw_momentum"])
    receipts = []
    for label, script in (("build-01", "build_pressure.py"), ("readout-01", "read_pressure.py"), ("balance-01", "check_pressure.py"), ("balance-02", "check_pressure_corrected.py"), ("derivation-01", "derive_background_repair.py")):
        start, end = read(ROOT / (label + ".start.json")), read(ROOT / (label + ".end.json"))
        check(label + " exact successful receipt", all(start[key] == end[key] for key in start) and end["exit_code"] == 0)
        check(label + " original script preserved", end["source_sha256"] == digest(ROOT / script))
        check(label + " worker exited", gone(end))
        receipts.append(end)
    for path in ROOT.glob("*.py"):
        compile(path.read_text(encoding="utf-8"), str(path), "exec")
        check("compile " + path.name, True)
    check("no bytecode", not list(ROOT.rglob("__pycache__")))
    coverage = BRIDGE / "final-stable-real-batch-rays037-038/common-coverage.json"
    check("scattering source unchanged", digest(coverage) == "95d628bbe34ddc317e1d954d8e556271d666645e259f0eda66245be0607a0db3")
    sources = [NATIVE / "fortran/MTSTwoField.f90", NATIVE / "fortran/equations.f90", NATIVE / "fortran/massive_neutrinos.f90", NATIVE / "forutils/Interpolation.f90", POST / "MTS-PHASE-STRESS-CURRENT-AND-AVERAGING-REMAINDER.md", CLOSURE / "closeout.json"]
    document = POST / "MTS-INDEPENDENT-PRESSURE-AND-STRESS-BALANCE.md"
    for path in [document, *sources]:
        check("cited local source exists " + str(path), path.is_file())
    artifacts = [dict(path=str(path), sha256=digest(path)) for path in ROOT.rglob("*") if path.is_file() and not path.name.startswith("validation-")]
    artifacts.append(dict(path=str(document), sha256=digest(document)))
    write(ROOT / "validation-result.json", dict(passed=True, checks=checks, source_sha256=digest(__file__), pid=os.getpid(), accepted_balance_sha256=digest(ROOT / "balance-corrected/balance-result.json"), readout_sha256=digest(ROOT / "readout-result.json"), repair_derivation_sha256=digest(ROOT / "background-repair-derivation.json"), prior_closeout_sha256=digest(CLOSURE / "closeout.json"), artifacts=artifacts, local_sources=[dict(path=str(path), sha256=digest(path)) for path in sources], web_sources=["https://arxiv.org/html/astro-ph/9506072v1"], process_receipts=receipts, pressure_ablations=ablations, heavy_raw_continuity_pass=False, cold_raw_continuity_pass=True, background_repair_executed=False, no_github_action=True, no_other_chat_process_action=True))
    print(dict(passed=True, checks=len(checks), pressure_ablations=ablations, heavy_raw_continuity_pass=False, cold_raw_continuity_pass=True), flush=True)


if __name__ == "__main__":
    main()
