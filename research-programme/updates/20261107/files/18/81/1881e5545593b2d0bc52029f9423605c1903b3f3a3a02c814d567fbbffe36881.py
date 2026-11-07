from common import *
import csv
import numpy as np


def main():
    modest()
    check_parent()
    require(LABEL == "summary", "summary owner")
    checks, reports, evidence = [], [], {}
    validation_count = 0
    def check(name, condition, value=None):
        checks.append(dict(name=name, passed=bool(condition), value=value))
    def evidence_read(path):
        evidence[str(path)] = digest(path)
        return read(path)
    gains = evidence_read(LATEST / "summary/summary.json")
    for family in ("half", "balanced", "double"):
        directory = STAGE / family
        bound = evidence_read(directory / "bound/result.json")
        validation = evidence_read(directory / "bound/validation.json")
        physical = evidence_read(directory / "physical-probe-result.json")
        probe = evidence_read(directory / "probe-result.json")
        check(family + ":bound", bound["passed"])
        check(family + ":independent", validation["passed"] and all(row["passed"] for row in validation["checks"]))
        check(family + ":physical", physical["passed"])
        check(family + ":original-probe", probe["passed"])
        validation_count += validation["count"]
        prior_path = ORIGINAL_PRIMITIVE if family == "balanced" else ORIGINAL_WAVES / family / "primitive"
        previous = evidence_read(prior_path / "primitive-result.json")
        for report in bound["reports"]:
            model = report["model"]
            old_probe = next(row for row in probe["reports"] if row["model"] == model)
            physical_probe = next(row for row in physical["reports"] if row["model"] == model)
            gain = next(row for row in gains["reports"] if row["family"] == family and row["model"] == model)
            primitive = next(row for row in previous["reports"] if row["model"] == model)
            branch = next(row for row in primitive["branches"] if row["branch"] == "poisson-spatial")
            case = next(row for row in branch["cases"] if row["tag"] == "half-cap")
            packet = load(report["packet"])
            check(family + ":" + model + ":packet", digest(report["packet"]) == report["sha256"])
            check(family + ":" + model + ":unchanged-readback", np.array_equal(np.asarray(report["measured"]), np.asarray(gain["measured"])))
            check(family + ":" + model + ":positive-comparison", np.min(packet["transition"]) >= 0)
            check(family + ":" + model + ":initial-comparison", np.min(packet["initial"]) >= 0)
            check(family + ":" + model + ":source-comparison", np.min(packet["forcing"]) >= 0)
            check(family + ":" + model + ":both-observables", all(report["covers"]))
            check(family + ":" + model + ":raw-normalization",
                  np.allclose(np.array(old_probe["raw_kernel_L1"]),
                              np.array(old_probe["normalized_kernel_L1"]) * np.array(old_probe["output_scales"])[:, None],
                              rtol=ALGEBRA, atol=0))
            check(family + ":" + model + ":scope", report["transformed_interpolant_scope"] and not report["native_continuum_certificate"])
            if model == "heavy":
                check(family + ":two-way-feedback", np.all(np.array(report["maximum_comparison"])[[0, 1], [1, 0]] > 0))
            else:
                check(family + ":absent-heavy-block", packet["initial"][0] == 0 and np.count_nonzero(packet["forcing"][:, 0]) == 0)
            reports.append(dict(family=family, model=model, wave_Mpc_inverse=gain["wave"],
                                N_interval=gain["N_interval"], output_order=["D", "delta_c"],
                                bound=report["prediction"]["bound"], measured=report["measured"],
                                prior_primitive_bound=case["bound"],
                                transition=report["prediction"]["comparison_transition"],
                                maximum_comparison=report["maximum_comparison"],
                                original_sample_log_growth=old_probe["sampled_constant_log_growth"],
                                physical_sample_log_growth=physical_probe["sampled_constant_log_gain"],
                                raw_kernel_L1=old_probe["raw_kernel_L1"],
                                normalized_kernel_L1=old_probe["normalized_kernel_L1"],
                                output_scales=old_probe["output_scales"], map_errors=physical_probe["errors"],
                                interpolation_errors=report["errors"], integration_error=report["integration_error"],
                                intervals=len(packet["efold"]) - 1, chunk_count=len(report["chunks"])))
        for manifest in directory.rglob("*inputs.json"):
            saved = evidence_read(manifest)
            for path, expected in saved.get("sources", {}).items():
                check("source:" + str(manifest.relative_to(STAGE)) + ":" + path, digest(path) == expected)
    failed = evidence_read(STAGE / "balanced/probe-01.end.json")
    check("historical-setup-failure-preserved", failed["exit_code"] == 1 and
          "FileNotFoundError" in (STAGE / "balanced/probe-01.stderr.log").read_text())
    check("no-new-physical-ODE", all(read(STAGE / family / "bound/result.json")["new_physical_ode_solves"] == 0 for family in ("half", "balanced", "double")))
    check_parent()
    passed = all(row["passed"] for row in checks)
    output = dict(passed=passed, reports=reports, independent_check_count=validation_count,
                  aggregate_check_count=len(checks), evidence_hashes=evidence, new_physical_ode_solves=0,
                  scope="Finite-interval numerically qualified transformed quintic operator, analytic skew tail; not directed interval arithmetic or native continuum certificate",
                  actual_errors_unchanged=True, previous_tighter_primitive_budgets_retained=True,
                  both_feedback_directions_retained=True, no_unknown_difference_used_as_source=True)
    write(ROOT / "summary.json", output)
    write(ROOT / "validation.json", dict(passed=passed, count=len(checks), checks=checks))
    with (ROOT / "comparison.csv").open("x", newline="", encoding="utf-8") as stream:
        columns = ("family", "model", "k_Mpc_inverse", "observable", "actual_error_percent",
                   "closed_state_bound_percent", "prior_primitive_bound_percent")
        writer = csv.DictWriter(stream, fieldnames=columns)
        writer.writeheader()
        for report in reports:
            for index, observable in enumerate(report["output_order"]):
                writer.writerow(dict(family=report["family"], model=report["model"], k_Mpc_inverse=report["wave_Mpc_inverse"],
                                     observable=observable, actual_error_percent=100 * report["measured"][index],
                                     closed_state_bound_percent=100 * report["bound"][index],
                                     prior_primitive_bound_percent=100 * report["prior_primitive_bound"][index]))
    with (ROOT / "comparison.csv").open(newline="", encoding="utf-8") as stream:
        parsed = list(csv.DictReader(stream))
    require(len(parsed) == 12 and all(None not in row and all(value is not None for value in row.values()) for row in parsed), "CSV shape")
    for row in checks:
        if not row["passed"]:
            print(row, flush=True)
    print("six comparisons;", validation_count, "independent checks;", len(checks), "aggregate checks; passed", passed, flush=True)
    require(passed, "preserve aggregate discrepancy")


if __name__ == "__main__":
    main()
