import csv
import os
from datetime import datetime, timezone
from pathlib import Path

from common import ROOT, POST, SOURCE, PAIRED, BRANCH, BRIDGE, modest, require, read, write, digest
import numpy as np
import psutil

DOCUMENT = POST / "MTS-PHASE-STRESS-CURRENT-AND-AVERAGING-REMAINDER.md"


def gone(record):
    stamp = datetime.fromisoformat(record["created"].replace("Z", "+00:00")).timestamp()
    try:
        return abs(psutil.Process(record["pid"]).create_time() - stamp) >= .01
    except psutil.NoSuchProcess:
        return True


def main():
    modest()
    checks = []

    def check(name, passed):
        checks.append(dict(name=name, passed=bool(passed)))
        require(passed, name)

    closed = read(SOURCE / "closeout.json")
    check("previous stage closed", closed["state"] == "verified_closed")
    check("previous validation pinned", digest(SOURCE / "validation-result.json") == "da88fd822cf8180dc33319d3b4895e95881fbc00ab410a304c5e94e9e4fb5069")
    for row in closed["artifacts"]:
        check("previous sealed artifact: " + Path(row["path"]).name, digest(row["path"]) == row["sha256"])
    native = read(SOURCE / "phase-resolved/tangent-native-result.json")
    for path, checksum in native["original_source_hashes"].items():
        check("original source: " + str(Path(path).relative_to(POST)), digest(path) == checksum)
    check("paired failure preserved", digest(PAIRED / "probe-check-result.json") == "b415792c4a89383239d2481a543117855d7b3a8419a57a4594f9885468f81fdd" and not read(PAIRED / "probe-check-result.json")["passed"])
    check("sparse replay failure preserved", not read(SOURCE / "continuous-replay-result.json")["passed"])
    check("scattering coverage unchanged", digest(BRIDGE / "final-stable-real-batch-rays037-038/common-coverage.json") == "95d628bbe34ddc317e1d954d8e556271d666645e259f0eda66245be0607a0db3")
    symbolic = read(ROOT / "derivation-result.json")
    check("symbolic source unchanged", symbolic["source_sha256"] == digest(ROOT / "derive_phase_stress.py"))
    check("ten identities zero", len(symbolic["checks"]) == 10 and symbolic["passed"] and all(row["passed"] and row["residual"] == "0" for row in symbolic["checks"]))
    analysis = read(ROOT / "analysis-result.json")
    check("analysis source unchanged", analysis["source_sha256"] == digest(ROOT / "analyze_phase_stress.py"))
    check("symbolic linkage", analysis["symbolic_sha256"] == digest(ROOT / "derivation-result.json"))
    check("previous validation linkage", analysis["prior_validation_sha256"] == digest(SOURCE / "validation-result.json"))
    check("gates frozen", analysis["algebra_gate"] == 1e-10 and analysis["numerical_gate"] == 2e-5)
    check("two controls present", [row["model"] for row in analysis["reports"]] == ["heavy", "cold"])
    check("numerical pass", analysis["passed"])
    check("retained gauge converter unchanged", digest(ROOT / "probe_analysis.py") == digest(SOURCE / "probe_analysis.py"))
    evidence = []
    total_rows = 0
    for report in analysis["reports"]:
        model = report["model"]
        check(model + " packet source", digest(report["packet"]["path"]) == report["packet"]["sha256"])
        check(model + " background source", digest(report["background_file"]) == report["background_sha256"])
        check(model + " cell owner", digest(report["cell_file"]) == report["cell_sha256"])
        check(model + " subgates", all(report[key] for key in ("passed", "algebra_passed", "conservation_passed", "refinement_passed", "sampled_budget_passed")))
        check(model + " integrated conservation", max(report["conservation"].values()) < 2e-5)
        check(model + " quadrature strides", [row["stride"] for row in report["refinements"]] == [2, 4] and all(row["maximum"] < 2e-5 and max(row["errors"].values()) == row["maximum"] for row in report["refinements"]))
        check(model + " windows frozen", [row["cycles"] for row in report["window_dependence"]] == [1, 2, 4])
        with Path(report["cell_file"]).open(newline="", encoding="utf-8") as stream:
            reader = csv.DictReader(stream)
            rows = list(reader)
            header = reader.fieldnames
        check(model + " CSV shape", len(rows) == report["complete_cycles"] + int(report["final_partial_cell"]) and all(None not in row and None not in row.values() and len(row) == len(header) for row in rows))
        numeric_names = [name for name in header if name != "complete_cycle"]
        check(model + " finite CSV", all(np.isfinite(float(row[name])) for row in rows for name in numeric_names))
        check(model + " contiguous interval", all(float(row["left_tau_mpc"]) < float(row["right_tau_mpc"]) for row in rows) and all(rows[index]["right_tau_mpc"] == rows[index + 1]["left_tau_mpc"] for index in range(len(rows) - 1)))
        check(model + " cycle/partial flags", [row["complete_cycle"] for row in rows] == ["True"] * report["complete_cycles"] + (["False"] if report["final_partial_cell"] else []))
        complete = [row for row in rows if row["complete_cycle"] == "True"]
        array = lambda name: np.array([float(row[name]) for row in complete])
        maximum = lambda values: max(float(np.max(abs(values))), 1e-30)
        density_scale = maximum(array("D"))
        pressure_scale = maximum(array("P"))
        if model == "heavy":
            check("heavy algebraic identities", max(report["identities"].values()) < 1e-10)
            check("four fast budgets explicit", len(report["fast_budgets"]) == 4 and all(row["bounded_with_sampled_envelope"] and row["continuum_certified"] is False and max(row["refinement_source_scaled"].values()) < 2e-5 for row in report["fast_budgets"]))
            discrepancy = array("P") - array("P_leading_closure")
            remainder = array("P_expansion_current_lapse_remainder") + array("P_fast_closure_remainder")
            check("CSV closure remainder", maximum(discrepancy - remainder) / pressure_scale < 1e-10)
            old = report["window_dependence"][0]
            check("reported density normalization", abs(maximum(discrepancy) / density_scale - old["leading_closure_error_density_scaled"]) < 1e-12)
            check("reported pressure normalization", abs(maximum(discrepancy) / pressure_scale - old["leading_closure_error_pressure_scaled"]) < 1e-12)
            evidence.append(dict(model=model, complete_cycles=len(complete), density_norm=density_scale, pressure_norm=pressure_scale, closure_discrepancy_density_scaled=maximum(discrepancy) / density_scale, slow_remainder_density_scaled=maximum(array("P_expansion_current_lapse_remainder")) / density_scale, fast_remainder_density_scaled=maximum(array("P_fast_closure_remainder")) / density_scale, sum_reconstructs_discrepancy=True))
        else:
            check("cold pressure genuinely zero", all(float(row["P"]) == 0 for row in rows))
            check("cold no scalar identity borrowed", report["identities"] == {} and report["fast_budgets"] == [])
            evidence.append(dict(model=model, complete_cycles=len(complete), pressure_zero=True))
        total_rows += len(rows)
    for name in ("common.py", "probe_analysis.py", "derive_phase_stress.py", "analyze_phase_stress.py", "validate_phase_stress.py"):
        path = ROOT / name
        compile(path.read_text(encoding="utf-8"), str(path), "exec")
        check("in-memory compile " + name, True)
    receipts = []
    for label in ("derivation-01", "analysis-01"):
        start, end = read(ROOT / (label + ".start.json")), read(ROOT / (label + ".end.json"))
        check(label + " identity/exit", end["pid"] == start["pid"] and end["created"] == start["created"] and end["command"] == start["command"] and end["exit_code"] == 0)
        script = "derive_phase_stress.py" if label == "derivation-01" else "analyze_phase_stress.py"
        check(label + " source identity", end["source_sha256"] == digest(ROOT / script))
        check(label + " exited", gone(end))
        receipts.append(end)
    paths = [DOCUMENT, ROOT / "PROTOCOL.md", BRANCH / "native-heavy-matching-20261007/55-native-heavy-matching-and-late-matter.md", POST / "MTS-DIRECT-TANGENT-AND-NEWTON-FORCE-BOUND.md"]
    for path in paths:
        check("document/source path: " + path.name, path.is_file())
    check("no bytecode directory created", not list(ROOT.rglob("__pycache__")))
    running = []
    for process in psutil.process_iter(["pid", "create_time", "name", "cmdline"]):
        try:
            info = process.info
            command = " ".join(info["cmdline"] or [])
            if info["pid"] != os.getpid() and (info["name"] or "").lower() in ("python.exe", "gfortran.exe", "f951.exe") and any(token in command for token in ("mts-phase-stress-20261107", "mts-direct-tangent-20261107", "source-readout-bridge-20261102")):
                running.append(info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    check("no other stage worker", not running)
    artifacts = [dict(path=str(path), sha256=digest(path)) for path in ROOT.iterdir() if path.is_file() and not path.name.startswith("validation-")]
    artifacts.append(dict(path=str(DOCUMENT), sha256=digest(DOCUMENT)))
    result = dict(passed=all(row["passed"] for row in checks), pid=os.getpid(), finished=datetime.now(timezone.utc).isoformat(), checks=checks, finite_csv_rows=total_rows, evidence=evidence, process_receipts=receipts, other_stage_workers=running, source_sha256=digest(__file__), artifacts=artifacts, no_parent_mutation=True, no_github_action=True, no_other_chat_process_stopped=True)
    write(ROOT / "validation-result.json", result)
    print(dict(passed=result["passed"], checks=len(checks), finite_csv_rows=total_rows, evidence=evidence), flush=True)


if __name__ == "__main__":
    main()

