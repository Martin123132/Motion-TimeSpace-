from common import *
from adjoint_operator import relative, sup
from comparison_math import propagate
from scipy.interpolate import make_interp_spline
import numpy as np
import csv


def main():
    modest()
    check_parent()
    require(LABEL == "summary", "summary owner")
    checks, reports, evidence = [], [], {}
    def check(name, condition, value=None):
        checks.append(dict(name=name, passed=bool(condition), value=value))
    for family in ("half", "balanced", "double"):
        directory = STAGE / family
        qualification_path = directory / "qualification.json"
        result_path = directory / "budget/result.json"
        qualification, result = read(qualification_path), read(result_path)
        evidence[str(qualification_path)] = digest(qualification_path)
        evidence[str(result_path)] = digest(result_path)
        check(family + ":qualification", qualification["passed"])
        check(family + ":budget", result["passed"])
        for manifest in (directory / "qualification-inputs.json", directory / "budget/inputs.json"):
            for path, expected in read(manifest)["sources"].items():
                check(family + ":frozen:" + path, digest(path) == expected)
        for report in result["reports"]:
            model = report["model"]
            prefix = family + ":" + model
            qualified = next(item for item in qualification["reports"] if item["model"] == model)
            for name, value in qualified["errors"].items():
                check(prefix + ":identity:" + name, value < GATE, value)
            for name, value in qualified["algebra"].items():
                check(prefix + ":algebra:" + name, value < ALGEBRA, value)
            for path, expected in report["input_hashes"].items():
                check(prefix + ":input:" + path, digest(path) == expected)
            check(prefix + ":components-hash", digest(report["source_packet"]) == report["source_sha256"])
            check(prefix + ":parent-packet-hash", digest(report["parent_interval_packet"]) == report["parent_interval_sha256"])
            saved = load(report["source_packet"])
            with np.load(report["parent_interval_packet"]) as archive:
                parent = {name: archive[name].copy() for name in ("efold", "source", "comparison", "initial", "readout_norm", "terminal_boundary")}
            check(prefix + ":same-grid", np.array_equal(saved["efold"], parent["efold"]))
            nodes = np.stack([saved["current_force"], saved["shear_force"], saved["representation_force"]], axis=1)
            check(prefix + ":source-reconstruction", relative(nodes.sum(axis=1) - parent["source"], parent["source"]) < ALGEBRA)
            curve = make_interp_spline(saved["efold"], nodes, k=5, axis=0)
            family_report = next(item for item in read(ENVELOPE / family / "physical-probe-result.json")["reports"] if item["model"] == model)
            check(prefix + ":physical-map-parent", family_report["passed"])
            context_info = read(LATEST / family / (model + "-channels.json"))
            coefficient_path = context_info["coefficient_input"]["path"]
            with np.load(coefficient_path) as archive:
                slots = archive["slots"].copy() if "slots" in archive.files else None
            if slots is None:
                with np.load(coefficient_path) as archive:
                    dimension = int(archive["core_size"])
                heavy = np.array([dimension - 2, dimension - 1]) if model == "heavy" else np.array([], dtype=int)
            else:
                heavy = slots if model == "heavy" else np.array([], dtype=int)
            size = nodes.shape[-1]
            rest = np.array([slot for slot in range(size) if slot not in heavy])
            check(prefix + ":heavy-block-size", len(heavy) == (2 if model == "heavy" else 0))
            for index in np.unique(np.linspace(1, len(saved["efold"]) - 3, 97, dtype=int)):
                guard()
                for fraction in (.173, .613):
                    location = float(saved["efold"][index] + fraction * (saved["efold"][index + 1] - saved["efold"][index]))
                    actual = curve(location)
                    heavy_norm = np.linalg.norm(actual[:, heavy], axis=-1) if len(heavy) else np.zeros(3)
                    rest_norm = np.linalg.norm(actual[:, rest], axis=-1)
                    norm = np.stack([heavy_norm, rest_norm], axis=-1)
                    upper = saved["forcing_bounds"][index]
                    excess = float(np.max(norm - upper))
                    check(prefix + ":force-envelope:" + str(index) + ":" + str(fraction),
                          excess <= ALGEBRA * max(sup(upper), 1e-80), excess)
            replay = np.empty_like(saved["propagated_components"])
            zeros = np.zeros((len(saved["efold"]) - 1, 2))
            replay[:, 0] = propagate(saved["efold"], parent["comparison"], zeros, parent["initial"])[0]
            for component in range(3):
                replay[:, component + 1] = propagate(saved["efold"], parent["comparison"], saved["forcing_bounds"][:, component], np.zeros(2))[0]
            check(prefix + ":independent-3x3-replay", relative(replay - saved["propagated_components"], saved["propagated_components"]) < ALGEBRA)
            contributions = np.column_stack([parent["readout_norm"] @ replay, parent["terminal_boundary"]])
            check(prefix + ":physical-projection", relative(contributions - saved["contributions"], saved["contributions"]) < ALGEBRA)
            bound = contributions.sum(axis=1)
            check(prefix + ":covers-saved-error", np.all(abs(report["measured"]) <= bound))
            check(prefix + ":does-not-artificially-tighten", np.all(bound + ALGEBRA * max(sup(bound), 1e-80) >= report["previous_combined_bound"]))
            check(prefix + ":representation-retained", np.min(contributions[:, 3]) >= 0)
            for name, value in report["errors"].items():
                check(prefix + ":budget:" + name, value < (ALGEBRA if name in ("reconstruction", "envelope_shortfall") else GATE), value)
            reports.append(dict(family=family, model=model, prediction=report["prediction"],
                                previous_combined_bound=report["previous_combined_bound"], measured=report["measured"],
                                source_conditions=report["source_conditions"], errors=report["errors"],
                                qualification_errors=qualified["errors"], algebra_errors=qualified["algebra"]))
            del saved, parent, nodes, curve
    check_parent()
    passed = all(item["passed"] for item in checks)
    write(ROOT / "summary.json", dict(passed=passed, checks_count=len(checks), reports=reports, evidence_hashes=evidence,
                                     scope="Source-separated same-parent interpolant budgets plus analytic conditional linear-branch estimate",
                                     new_physical_ode_solves=0, previous_tighter_adjoint_budgets_preserved=True))
    write(ROOT / "validation.json", dict(passed=passed, count=len(checks), checks=checks))
    with (ROOT / "observable-budgets.csv").open("x", newline="", encoding="utf-8") as stream:
        columns = ("family", "model", "observable", "actual_percent", "initial_percent", "current_percent", "shear_percent", "representation_percent", "terminal_percent", "total_percent", "old_combined_percent")
        writer = csv.DictWriter(stream, fieldnames=columns)
        writer.writeheader()
        for report in reports:
            for index, observable in enumerate(report["prediction"]["output_order"]):
                row = dict(family=report["family"], model=report["model"], observable=observable, actual_percent=100 * report["measured"][index],
                           total_percent=100 * report["prediction"]["total_bound"][index],
                           old_combined_percent=100 * report["previous_combined_bound"][index])
                for name, value in zip(report["prediction"]["contribution_order"], report["prediction"]["contributions"][index]):
                    row[name + "_percent"] = 100 * value
                writer.writerow(row)
    for check_row in checks:
        if not check_row["passed"]:
            print(check_row, flush=True)
    print("six source/readout comparisons", len(checks), "checks passed", passed, flush=True)
    require(passed, "preserve verification discrepancy")


if __name__ == "__main__":
    main()
