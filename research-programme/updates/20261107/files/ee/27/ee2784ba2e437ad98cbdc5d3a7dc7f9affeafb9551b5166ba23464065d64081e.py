import csv
import os
from datetime import datetime
from pathlib import Path
from common import ROOT, POST, PRIOR, BRANCH, BRIDGE, GATE, ALGEBRA, modest, check_prior, require, read, write, digest, load
import numpy as np
import psutil


def gone(record):
    stamp = datetime.fromisoformat(record["created"].replace("Z", "+00:00")).timestamp()
    try:
        return abs(psutil.Process(record["pid"]).create_time() - stamp) >= .01
    except psutil.NoSuchProcess:
        return True


def main():
    modest()
    seal = check_prior()
    checks = []
    def check(name, value):
        checks.append(dict(name=name, passed=bool(value)))
        require(value, name)
    check("previous goal turn progress preserved", seal["state"] == "verified_closed" and seal["previous_goal_turn_classification"] == "progress")
    inputs, result = read(ROOT / "input-result.json"), read(ROOT / "tail-energy-result.json")
    check("input source pinned", inputs["passed"] and inputs["source_sha256"] == digest(ROOT / "prepare_tail_inputs.py"))
    check("numerical source pinned", result["passed"] and result["source_sha256"] == digest(ROOT / "derive_tail_energy.py"))
    check("protocol pinned", inputs["protocol_sha256"] == result["protocol_sha256"] == digest(ROOT / "PROTOCOL.md"))
    check("gates unchanged", result["numerical_gate"] == GATE == 2e-5 and result["algebra_gate"] == ALGEBRA == 1e-10)
    check("input/result links", result["input_result_sha256"] == digest(ROOT / "input-result.json") and result["prior_result_sha256"] == digest(PRIOR / "comparison-result.json"))
    check("symbolic streaming identities", result["symbolic"]["streaming_identities"] == ["0"] * 4)
    check("quadrupole collision rates", result["symbolic"]["quadrupole_collision_rates"] == ["3/10", "1"])
    check("no perturbation recapture", not inputs["perturbation_evolution_rerun"])
    check("background factory unchanged", inputs["factory_sha256"] == digest(BRANCH / "native-heavy-matching-20261007/matching_common.py"))
    check("native library unchanged", inputs["dll_sha256"] == digest(PRIOR / "build-corrected/native/camb/cambdll.dll"))
    numerical_fields = ("energy_balance_error", "rate_error", "independent_background_error", "containment_error", "norm_quadrature_refinement", "norm_source_refinement", "independent_norm_error", "norm_precision_error")
    for report in result["reports"]:
        model = report["model"]
        folder = ROOT / "results" / model
        source = next(row for row in inputs["reports"] if row["model"] == model)
        original = PRIOR / "runs-balanced" / model
        reference = load(original / "native-reference.npz")
        thermal = load(source["file"])
        check(model + " thermal ownership", source["sha256"] == digest(source["file"]))
        check(model + " saved states ownership", source["reference_sha256"] == digest(original / "native-reference.npz"))
        check(model + " saved operator ownership", source["operator_sha256"] == digest(original / "operator-audit.npz"))
        check(model + " background table ownership", source["table_sha256"] == digest(BRANCH / f"native-two-field-transfer-20261007/runs/backgrounds/{model}.npz"))
        check(model + " complete retained tail/core partition", report["tail_dimension"] == 154 and report["retained_core_dimension"] == (30 if model == "heavy" else 28))
        check(model + " UFA kept explicit", report["massless_UFA_retained"] and reference["signature"][12] == 1)
        check(model + " not gravity energy or full contraction", not report["physical_energy_density_claim"] and not report["full_gravity_contraction_claim"])
        check(model + " source readout physical", source["flat"] and source["scale_factor_error"] < GATE and np.min(thermal["opacity"]) >= 0)
        all_indices = []
        for group in report["groups"]:
            name = model + " " + group["name"]
            data = load(folder / group["file"])
            check(name + " ownership", digest(folder / group["file"]) == group["sha256"])
            check(name + " finite arrays", all(np.isfinite(value).all() for value in data.values()))
            check(name + " exact original grid", np.array_equal(data["times"], reference["times"]))
            check(name + " original dimension", len(data["indices"]) == group["tail_dimension"])
            check(name + " positive norm weights", np.min(data["weights"]) > 0)
            all_indices.extend(data["indices"].tolist())
            state = reference["state"][:, data["indices"]]
            recomputed = .5 * np.sum(data["weights"] * state ** 2, axis=1)
            check(name + " energy from original states", np.array_equal(recomputed, data["energy"]))
            check(name + " norm from energy", np.array_equal(np.sqrt(2 * data["energy"]), data["norm"]))
            denominator = max(float(np.max(abs(data["energy_rate"]))), float(np.max(abs(data["work"]))), float(np.max(abs(data["loss"]))), 1e-80)
            balance = float(np.max(abs(data["energy_rate"] - data["work"] + data["loss"])) / denominator)
            check(name + " independent work-loss score", balance == group["energy_balance_error"] and balance < GATE)
            check(name + " nonnegative physical damping", np.min(data["damping"]) >= 0 and np.min(data["loss"]) >= 0)
            check(name + " initial preparation explicitly zero", group["initial_preparation_norm"] == 0 and data["norm"][0] == 0 and data["bound"][0] == 0)
            overshoot = float(np.max(np.maximum(data["norm"] - data["bound"], 0)) / max(float(np.max(data["norm"])), 1e-80))
            check(name + " independently recomputed containment", overshoot == group["containment_error"] and overshoot < GATE)
            return_excess = float(np.max(np.maximum(data["return_magnitude"] - data["return_bound"], 0)) / max(float(np.max(data["return_magnitude"])), 1e-80))
            check(name + " return bound contains original response", return_excess < GATE)
            check(name + " numerical gates", all(group[field] < GATE for field in numerical_fields))
            check(name + " operator algebra gates", max(group["operator_identity_error"], group["return_port_error"]) < ALGEBRA)
            check(name + " damping logarithmic norm", abs(group["maximum_weighted_logarithmic_rate"] + group["minimum_damping"]) < GATE)
        check(model + " distinct tails", len(all_indices) == len(set(all_indices)) == 154)
        check(model + " selected scalar/CDM states kept in core", not set(reference["selected"]).intersection(all_indices))
        check(model + " all seven groups", len(report["groups"]) == 7)
        check(model + " all21 port impulses", len(report["kernels"]) == 21)
        for fraction in (0., .25, .5):
            data = load(folder / ("impulse-" + str(int(100 * fraction)) + ".npz"))
            release = reference["times"][0] + fraction * np.ptp(reference["times"])
            check(model + str(fraction) + " causal support", data["times"][0] == release and np.all(data["times"] >= release))
            check(model + str(fraction) + " original final time", data["times"][-1] == reference["times"][-1])
            check(model + str(fraction) + " finite impulse data", all(np.isfinite(value).all() for key, value in data.items() if key != "groups"))
            offset = 0
            for index, group in enumerate(report["groups"]):
                stored = load(folder / group["file"])
                count = group["tail_dimension"]
                resolved = data["undamped_fine"][:, offset:offset + count]
                norm_ratio = np.sqrt(np.sum(stored["weights"] * resolved ** 2, axis=1) / stored["weights"][0])
                recorded = next(row for row in report["kernels"] if row["release_fraction"] == fraction and row["group"] == group["name"])
                check(model + str(fraction) + group["name"] + " unit impulse", resolved[0, 0] == 1 and np.count_nonzero(resolved[0, 1:]) == 0)
                check(model + str(fraction) + group["name"] + " impulse norm", float(np.max(np.maximum(norm_ratio - 1, 0))) == recorded["norm_excess"] and recorded["norm_excess"] < GATE)
                check(model + str(fraction) + group["name"] + " returned envelope", np.max(abs(data["kernels"][:, index]) - data["envelopes"][:, index]) <= GATE * np.max(data["envelopes"][:, index]))
                check(model + str(fraction) + group["name"] + " zero-lag sign", data["kernels"][0, index] < 0 and data["kernels"][0, index] == recorded["initial_kernel"])
                check(model + str(fraction) + group["name"] + " refinement", recorded["refinement"] < GATE and recorded["passed"])
                offset += count
            check(model + str(fraction) + " full impulse dimension", offset == data["undamped_fine"].shape[1] == 154)
    with (ROOT / "tail-summary.csv").open(newline="", encoding="utf-8") as stream:
        reader = csv.DictReader(stream)
        rows = list(reader)
    check("fourteen CSV rows", len(rows) == 14)
    for row in rows:
        check(row["model"] + row["name"] + " parsed row", None not in row and None not in row.values() and row["passed"] == "True")
        check(row["model"] + row["name"] + " CSV evidence", all(float(row[field]) < GATE for field in numerical_fields))
    receipts = []
    for label, script in (("inputs-01", "prepare_tail_inputs.py"), ("energy-01", "derive_tail_energy.py")):
        start, end = read(ROOT / (label + ".start.json")), read(ROOT / (label + ".end.json"))
        check(label + " complete receipt", start["pid"] == end["pid"] and start["created"] == end["created"] and start["command"] == end["command"] and end["exit_code"] == 0)
        check(label + " actual code", end["source_sha256"] == digest(ROOT / script))
        check(label + " exited", gone(end))
        receipts.append(end)
    for path in ROOT.glob("*.py"):
        compile(path.read_text(encoding="utf-8"), str(path), "exec")
        check("compile " + path.name, True)
    check("no bytecode", not list(ROOT.rglob("__pycache__")))
    check("scattering unchanged", digest(BRIDGE / "final-stable-real-batch-rays037-038/common-coverage.json") == "95d628bbe34ddc317e1d954d8e556271d666645e259f0eda66245be0607a0db3")
    document = POST / "MTS-TAIL-ENERGY-AND-CAUSAL-FEEDBACK-BOUND.md"
    check("physics document", document.is_file())
    local_sources = [BRANCH / "native-heavy-matching-20261007/native/fortran/equations.f90", BRANCH / "native-heavy-matching-20261007/matching_common.py", POST / "MTS-RETAINED-HIERARCHY-AND-RETARDED-COUPLING.md"]
    for path in local_sources:
        check("source exists " + str(path), path.is_file())
    source_paths = [dict(path=str(path), sha256=digest(path)) for path in local_sources]
    artifacts = [dict(path=str(path), sha256=digest(path)) for path in ROOT.rglob("*") if path.is_file() and not path.name.startswith("validation-")]
    artifacts.append(dict(path=str(document), sha256=digest(document)))
    write(ROOT / "validation-result.json", dict(passed=all(row["passed"] for row in checks), checks=checks, pid=os.getpid(), source_sha256=digest(__file__), accepted_result_sha256=digest(ROOT / "tail-energy-result.json"), previous_closeout_sha256=digest(PRIOR / "closeout.json"), artifacts=artifacts, local_sources=source_paths, web_sources=["https://arxiv.org/html/astro-ph/9506072v1", "https://arxiv.org/html/1104.2933v3"], process_receipts=receipts, original_artifacts_preserved=True, no_github_action=True, no_unrelated_process_action=True))
    print(dict(passed=True, checks=len(checks), paired_driven_chains=14, port_impulses=42, csv_rows=len(rows)), flush=True)


if __name__ == "__main__":
    main()
