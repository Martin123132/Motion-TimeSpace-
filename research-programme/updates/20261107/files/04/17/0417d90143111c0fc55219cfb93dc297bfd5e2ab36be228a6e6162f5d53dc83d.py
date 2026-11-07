import csv
import os
import re
from datetime import datetime
from pathlib import Path
from common import ROOT, POST, WINDOW, SOURCE, BRIDGE, modest, require, read, write, digest
import numpy as np
import psutil


def gone(record):
    created = record["created"]
    stamp = datetime.fromisoformat(created.replace("Z", "+00:00")).timestamp() if isinstance(created, str) else float(created)
    try:
        return abs(psutil.Process(record["pid"]).create_time() - stamp) >= .01
    except psutil.NoSuchProcess:
        return True


def load(path):
    with np.load(path) as archive:
        return {name: archive[name].copy() for name in archive.files}


def main():
    modest()
    checks = []
    def check(name, value):
        checks.append(dict(name=name, passed=bool(value)))
        require(value, name)
    seal = read(WINDOW / "closeout.json")
    check("previous progress closed", seal["state"] == "verified_closed")
    check("previous validation pinned", digest(WINDOW / "validation-result.json") == "9d416b56d8ac7ab2d317cd76b826632007de73faf1a17bce274a5039c7f7eab8")
    for record in seal["artifacts"]:
        check("previous artifact " + str(Path(record["path"]).relative_to(WINDOW)), digest(record["path"]) == record["sha256"])
    for record in seal["handoff_artifacts"]:
        if Path(record["path"]).name == "MTS-WINDOW-EVOLUTION-AND-SELF-GRAVITY.md":
            check("previous physics document", digest(record["path"]) == record["sha256"])
    build = read(ROOT / "build-corrected/build-result.json")
    failed_build = read(ROOT / "build-result.json")
    check("failed build preserved", failed_build["state"] == "failed" and failed_build["source_sha256"] == digest(ROOT / "camb_python.f90"))
    check("accepted isolated build", build["state"] == "complete" and build["source_sha256"] == digest(ROOT / "build-corrected/camb_python.f90") and build["dll_sha256"] == digest(ROOT / "build-corrected/native/camb/cambdll.dll"))
    for collection in ("original_input_hashes", "reused_object_module_hashes", "copied_package_hashes"):
        for path, checksum in build[collection].items():
            check(collection + ": " + path, digest(path) == checksum)
    check("copied import data", read(ROOT / "build-corrected/import-data.json")["sha256"] == digest(ROOT / "build-corrected/native/fortran/HighLExtrapTemplate_lenspotentialCls.dat"))
    processes = []
    cleanup = []
    for label, report in (("build-01", failed_build), ("build-02", build)):
        start = read(ROOT / (label + ".start.json"))
        end = read(ROOT / (label + ".end.json"))
        lower = datetime.fromisoformat(start["created"].replace("Z", "+00:00")).timestamp()
        upper = datetime.fromisoformat(end["finished"].replace("Z", "+00:00")).timestamp()
        for parent in report["processes"]:
            for identity in [parent] + parent["children"]:
                check("compiler process exited " + str(identity["pid"]), gone(identity))
                processes.append(identity)
                for argument in identity["command"]:
                    if re.fullmatch(r"D:\\Temp\\cc[A-Za-z0-9_]+\.(s|o|res|lst|ld)", argument):
                        path = Path(argument)
                        exists = path.exists()
                        removed = False
                        if exists:
                            resolved = path.resolve()
                            check("owned temp directory " + path.name, resolved.parent == Path("D:/Temp").resolve())
                            stat = resolved.stat()
                            check("owned temp creation time " + path.name, lower - 2 <= stat.st_ctime <= upper + 2)
                            resolved.unlink()
                            removed = not resolved.exists()
                            check("owned temp removed " + path.name, removed)
                        cleanup.append(dict(path=str(path), existed=exists, removed=removed, owner_pid=identity["pid"]))
        check(label + " mappings released", report["temporary_mappings_removed"])
    check("no task drive mapping remains", all(not Path(drive + ":/").exists() for drive in ("T", "R", "S")))
    owner = read(ROOT / "hierarchy-balanced-result.json")
    check("balanced native runner complete", owner["state"] == "complete" and len(owner["reports"]) == 2)
    correction = read(ROOT / "RUN-PROVENANCE-CORRECTION.json")
    check("provenance annotation only", correction["state"] == "annotation_only_predictions_unchanged" and not correction["numerical_outputs_changed"] and not correction["acceptance_gates_changed"] and correction["no_numerical_rerun"])
    check("both affected reports annotated", {entry["result"] for entry in correction["entries"]} == {"hierarchy-startstep-result.json", "hierarchy-balanced-result.json"})
    for entry in correction["entries"]:
        report = read(ROOT / entry["result"])
        actual = read(ROOT / entry["config"])
        launch = read(ROOT / (entry["launch_label"] + ".start.json"))
        check(entry["result"] + " unchanged report", entry["result_sha256"] == digest(ROOT / entry["result"]))
        check(entry["config"] + " actual config owner", entry["config_sha256"] == digest(ROOT / entry["config"]))
        check(entry["result"] + " original erroneous link explicit", entry["recorded_config_sha256"] == report["config_sha256"] == digest(ROOT / correction["original_config"]))
        check(entry["result"] + " actual source chain", entry["runner_sha256"] == report["source_sha256"] == actual["source_sha256"] == launch["source_sha256"] == digest(ROOT / entry["runner"]))
        check(entry["config"] + " frozen protocol", actual["protocol_sha256"] == digest(ROOT / "PROTOCOL.md") and actual["numerical_gate"] == 2e-5 and actual["algebra_gate"] == 1e-10)
        check(entry["config"] + " declared controlled cases", actual["state_cases"] == [["full", 2e-11, 1.0], ["precision", 2e-12, 1.0], ["zero", 2e-11, 0.0], ["negative", 2e-11, -1.0]] and actual["kernel_release_fractions"] == [0.0, .25, .5] and actual["kernel_tolerances"] == [2e-11, 2e-12])
    config = read(ROOT / "run-config-balanced.json")
    check("protocol frozen", config["protocol_sha256"] == digest(ROOT / "PROTOCOL.md"))
    comparison = read(ROOT / "comparison-result.json")
    channels = read(ROOT / "memory-channel-algebra-result.json")
    check("accepted numerical comparison", comparison["passed"] and comparison["gate"] == 2e-5 and comparison["algebra_gate"] == 1e-10 and comparison["source_sha256"] == digest(ROOT / "check_hierarchy.py"))
    check("comparison link", comparison["runner_result_sha256"] == digest(ROOT / "hierarchy-balanced-result.json"))
    check("accepted action compression derivation", channels["passed"] and channels["symbolic"] == ["0", "0", "0"] and channels["source_sha256"] == digest(ROOT / "derive_memory_channels_algebra.py"))
    check("channel linkage", channels["comparison_sha256"] == digest(ROOT / "comparison-result.json") and channels["operator_sha256"] == digest(ROOT / "runs-balanced/heavy/operator-audit.npz"))
    check("original off-grid channel failure preserved", not read(ROOT / "memory-channel-result.json")["passed"] and read(ROOT / "memory-channel-result.json")["source_sha256"] == digest(ROOT / "derive_memory_channels.py"))
    check("prior solver failures preserved", read(ROOT / "hierarchy-result.json")["state"] == "failed" and read(ROOT / "hierarchy-startstep-result.json")["state"] == "failed")
    check("completed old-unit prediction preserved", (ROOT / "runs-startstep/heavy/full.npz").is_file() and read(ROOT / "runs-startstep/heavy/full-solver-status.json")["success"])
    for model_record in owner["reports"]:
        model = model_record["model"]
        folder = ROOT / "runs-balanced" / model
        native = load(folder / "native-reference.npz")
        check(model + " native owner", digest(folder / "native-reference.npz") == model_record["captured_reference_sha256"])
        check(model + " dimension and selector", len(native["mapping"]) == model_record["dimension"] and model_record["selector"] not in native["mapping"])
        check(model + " prepared remaining block exactly zero", np.count_nonzero(native["initial"][native["remaining"]]) == 0)
        check(model + " full supported regime", native["signature"][11] == 0 and native["signature"][12] == 1 and np.count_nonzero(native["signature"][70:76]) == 0)
        check(model + " operator/reference ownership exact", model_record["adapter_overlap"] == model_record["operator_observer_error"] == model_record["operator_derivative_error"] == 0)
        check(model + " linearity", model_record["maximum_linearity_error"] < 1e-10)
        balance = load(folder / "balanced-scale.npz")
        check(model + " recorded initial-operator scaling", np.array_equal(balance["initial"], native["initial"]) and np.array_equal(balance["normalization"], np.maximum(balance["previous"], np.max(abs(balance["frozen_states"]), axis=0))) and len(balance["offsets"]) == 17)
        for case in model_record["cases"]:
            path = folder / case["file"]
            check(model + case["tag"] + " output owner", digest(path) == case["sha256"])
            predicted = load(path)
            check(model + case["tag"] + " finite", all(np.isfinite(value).all() for value in predicted.values()))
            check(model + case["tag"] + " same grid", np.array_equal(predicted["times"], native["times"]))
            if case["tag"] == "full":
                denominator = np.maximum(np.max(abs(native["state"]), axis=0), 1e-30)
                maximum = float(np.max(abs(predicted["state"] - native["state"]) / denominator))
                result = next(row for row in comparison["reports"] if row["model"] == model)
                check(model + " independently recomputed full-state score", abs(maximum - result["full_state_error"]) < 1e-15 and maximum < 2e-5)
        check(model + " all original controlled gates", all(row["passed"] for row in next(row for row in comparison["reports"] if row["model"] == model)["kernels"]))
        for kernel in model_record["kernels"]:
            path = folder / kernel["file"]
            check(model + kernel["tag"] + " source owner", digest(path) == kernel["sha256"])
            values = load(path)
            check(model + kernel["tag"] + " causal support", np.all(values["times"] >= values["release"]) and np.isfinite(values["kernel"]).all())
    check("pure compression identities", max(max(row["row_rank_one_identity"], row["selected_block_identity"], row["density_channel_column_identity"]) for row in channels["operator_reports"]) < 1e-10)
    check("independent background match", max(row["independent_background_error"] for row in channels["operator_reports"]) < 2e-5)
    check("two-function reconstruction", all(row["source_owned_two_function_reconstruction_error"] < 2e-5 and row["zero_field_position_row"] for row in channels["kernel_reports"]))
    csv_counts = {}
    for filename, key in (("state-comparison.csv", "state_csv_sha256"), ("retarded-kernel.csv", "kernel_csv_sha256")):
        check(filename + " owner", comparison[key] == digest(ROOT / filename))
        with (ROOT / filename).open(newline="", encoding="utf-8") as stream:
            reader = csv.DictReader(stream)
            rows = list(reader)
            columns = reader.fieldnames
        check(filename + " finite parsed rows", all(None not in row and None not in row.values() and all(np.isfinite(float(row[key])) for key in columns if key not in ("model", "selected")) for row in rows))
        csv_counts[filename] = len(rows)
    check("both complete state dimensions", csv_counts["state-comparison.csv"] == 366)
    expected = [("build-01", 1, "build_hierarchy.py"), ("build-02", 0, "build_hierarchy_corrected.py"), ("hierarchy-01", 1, "run_hierarchy.py"), ("start-diagnostic-01", 1, "diagnose_start_attempt01.py"), ("start-diagnostic-02", 0, "diagnose_start.py"), ("hierarchy-02", 1, "run_hierarchy_startstep.py"), ("hierarchy-03", 0, "run_hierarchy_balanced.py"), ("comparison-01", 0, "check_hierarchy.py"), ("channels-01", 1, "derive_memory_channels.py"), ("channels-02", 0, "derive_memory_channels_algebra.py")]
    expected.append(("validation-01", 1, "validate_hierarchy_attempt01.py"))
    for label, status, script in expected:
        start, end = read(ROOT / (label + ".start.json")), read(ROOT / (label + ".end.json"))
        check(label + " process receipt", start["pid"] == end["pid"] and start["created"] == end["created"] and start["command"] == end["command"] and end["exit_code"] == status)
        check(label + " exact source preserved", end["source_sha256"] == digest(ROOT / script))
        check(label + " exited", gone(end))
        processes.append(end)
    for path in ROOT.glob("*.py"):
        if path.name == "diagnose_start_attempt01.py":
            try:
                compile(path.read_text(encoding="utf-8"), str(path), "exec")
            except SyntaxError:
                check("preserved parse-only failure remains explicit", True)
            else:
                check("preserved parse-only failure remains explicit", False)
        else:
            compile(path.read_text(encoding="utf-8"), str(path), "exec")
            check("compile " + path.name, True)
    check("no generated bytecode", not list(ROOT.rglob("__pycache__")))
    check("scattering source bank unchanged", digest(BRIDGE / "final-stable-real-batch-rays037-038/common-coverage.json") == "95d628bbe34ddc317e1d954d8e556271d666645e259f0eda66245be0607a0db3")
    document = POST / "MTS-RETAINED-HIERARCHY-AND-RETARDED-COUPLING.md"
    check("physics handoff exists", document.is_file())
    artifacts = [dict(path=str(path), sha256=digest(path)) for path in ROOT.rglob("*") if path.is_file() and not path.name.startswith("validation-")]
    artifacts.append(dict(path=str(document), sha256=digest(document)))
    write(ROOT / "validation-result.json", dict(passed=all(row["passed"] for row in checks), pid=os.getpid(), checks=checks, csv_rows=csv_counts, accepted_comparison_sha256=digest(ROOT / "comparison-result.json"), accepted_channel_sha256=digest(ROOT / "memory-channel-algebra-result.json"), source_sha256=digest(__file__), artifacts=artifacts, process_receipts=processes, compiler_temp_cleanup=cleanup, original_inputs_preserved=True, future_species_histories_supplied=False, inherited_approximations_retained=True, no_github_action=True, no_other_chat_process_action=True))
    print(dict(passed=True, checks=len(checks), csv_rows=csv_counts, compiler_temp_cleanup=cleanup), flush=True)


if __name__ == "__main__":
    main()

