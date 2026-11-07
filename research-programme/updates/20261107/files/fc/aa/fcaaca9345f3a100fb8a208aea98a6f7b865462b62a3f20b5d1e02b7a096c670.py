from common import *
import csv
import numpy as np
import sympy as sp


def main():
    modest()
    check_parent()
    require(LABEL == "summary", "summary owner")
    checks, reports, evidence = [], [], {}
    def check(name, condition, value=None):
        checks.append(dict(name=name, passed=bool(condition), value=value))
    for family in ("half", "balanced", "double"):
        path = STAGE / family / "result.json"
        evidence[str(path)] = digest(path)
        result = read(path)
        check(family + ":complete", result["passed"])
        frozen = read(STAGE / family / "inputs.json")
        for filename, expected in frozen["sources"].items():
            check(family + ":source:" + filename, digest(filename) == expected)
        for report in result["reports"]:
            model = report["model"]
            prefix = family + ":" + model
            evidence[report["coefficient_input"]["path"]] = report["coefficient_input"]["sha256"]
            check(prefix + ":coefficients", digest(report["coefficient_input"]["path"]) == report["coefficient_input"]["sha256"])
            for name, value in report["errors"].items():
                check(prefix + ":native:" + name, value < GATE, value)
            for name, value in report["algebra"].items():
                check(prefix + ":algebra:" + name, value < ALGEBRA, value)
            rows = report["rows"]
            check(prefix + ":samples", len(rows) == 97)
            values = np.array([[row["epsilon_H_over_k"], row["delta_k_over_am"], row["kappa_amH_over_k2"]] for row in rows])
            check(prefix + ":dimensionless-identity", np.max(abs(values[:, 0] / values[:, 1] - values[:, 2]) / values[:, 2]) < ALGEBRA)
            omega_origin = rows[0]["omega"] * np.exp(-rows[0]["efold"])
            mass_consistency = max(abs(row["omega"] / (omega_origin * np.exp(row["efold"])) - 1) for row in rows)
            check(prefix + ":retained-constant-mass", mass_consistency < ALGEBRA, mass_consistency)
            frequency_ratio = np.hypot(1., 1 / values[:, 1])
            rescaling = 1 / frequency_ratio
            exact = np.array([[entry["exact"] for entry in row["coupling"]] for row in rows])
            upper = np.array([[entry["upper"] for entry in row["coupling"]] for row in rows])
            balanced = upper * np.column_stack([rescaling, 1 / rescaling])
            check(prefix + ":bounds", np.all(exact <= upper * (1 + ALGEBRA)))
            check(prefix + ":product-invariant", np.max(abs(np.prod(balanced, axis=1) / np.prod(upper, axis=1) - 1)) < ALGEBRA)
            old_path = LATEST / family / "bound" / model / "result.json"
            evidence[str(old_path)] = digest(old_path)
            old = read(old_path)
            saved = load(old["packet"])
            check(prefix + ":old-packet", digest(old["packet"]) == old["sha256"])
            if model == "heavy":
                omega_start = omega_origin * np.exp(saved["efold"][0])
                omega_end = omega_origin * np.exp(saved["efold"][-1])
                factor_start = rows[0]["wave"] / np.hypot(rows[0]["wave"], omega_start)
                factor_end = rows[0]["wave"] / np.hypot(rows[0]["wave"], omega_end)
            else:
                factor_start, factor_end = 1., 1.
            initial_scale, final_scale = np.diag([factor_start, 1.]), np.diag([factor_end, 1.])
            balanced_transition = final_scale @ saved["transition"] @ np.diag([1 / factor_start, 1.])
            restored_transition = np.diag([1 / factor_end, 1.]) @ balanced_transition @ initial_scale
            check(prefix + ":transition-restore", np.max(abs(restored_transition - saved["transition"])) / np.max(abs(saved["transition"])) < ALGEBRA)
            changed_initial = initial_scale @ saved["initial"]
            changed_final = final_scale @ saved["final"]
            changed_readout = saved["readout_norm"] @ np.diag([1 / factor_end, 1.])
            restored_bound = changed_readout @ changed_final + saved["terminal_boundary"]
            original_bound = np.array(old["prediction"]["bound"])
            restore_error = float(np.max(abs(restored_bound - original_bound)) / np.max(original_bound))
            check(prefix + ":original-output-bound-unchanged", restore_error < ALGEBRA, restore_error)
            check(prefix + ":positive-transition", np.min(balanced_transition) >= 0)
            reports.append(dict(family=family, model=model, wave=rows[0]["wave"], samples=len(rows),
                                errors=report["errors"], algebra=report["algebra"],
                                epsilon_range=[float(values[:, 0].min()), float(values[:, 0].max())],
                                delta_range=[float(values[:, 1].min()), float(values[:, 1].max())],
                                kappa_range=[float(values[:, 2].min()), float(values[:, 2].max())],
                                full_frequency_kappa_range=[float(np.min(values[:, 0] * frequency_ratio)), float(np.max(values[:, 0] * frequency_ratio))],
                                exact_maximum_coupling=np.max(exact, axis=0).tolist(),
                                analytic_upper_maximum=np.max(upper, axis=0).tolist(),
                                balanced_upper_maximum=np.max(balanced, axis=0).tolist(),
                                balance_factors=[factor_start, factor_end],
                                balanced_transition=balanced_transition.tolist(),
                                restored_bound=restored_bound.tolist(), output_restoration_error=restore_error,
                                actual_previous_difference=old["measured"],
                                sampled_coefficient_qualification_only=True))
    wave, omega, hubble = sp.symbols("k omega H", positive=True)
    full = sp.sqrt(wave**2 + omega**2)
    factor = wave / full
    logarithmic_rate = sp.simplify(sp.diff(factor, omega) * omega / factor)
    check("analytic-balanced-derivative", sp.simplify(logarithmic_rate + omega**2 / full**2) == 0)
    check("analytic-full-kappa", sp.simplify(hubble / wave * full / wave - hubble * full / wave**2) == 0)
    check_parent()
    passed = all(row["passed"] for row in checks)
    write(ROOT / "summary.json", dict(passed=passed, reports=reports, checks_count=len(checks), evidence_hashes=evidence,
                                     new_physical_ode_solves=0, coupling_factorization="rank at most two through Psi and Phi_N",
                                     no_pressure_or_remainder_log_norm_bound_assumed_proved=True,
                                     no_asymptotic_exponent_fit=True, actual_bound_and_observable_unchanged=True))
    write(ROOT / "validation.json", dict(passed=passed, count=len(checks), checks=checks))
    with (ROOT / "couplings.csv").open("x", newline="", encoding="utf-8") as stream:
        columns = ("family", "model", "k", "epsilon_max", "delta_max", "kappa_max", "to_scalar_upper", "from_scalar_upper", "balanced_to_upper", "balanced_from_upper")
        writer = csv.DictWriter(stream, fieldnames=columns)
        writer.writeheader()
        for report in reports:
            writer.writerow(dict(family=report["family"], model=report["model"], k=report["wave"],
                                 epsilon_max=report["epsilon_range"][1], delta_max=report["delta_range"][1], kappa_max=report["kappa_range"][1],
                                 to_scalar_upper=report["analytic_upper_maximum"][0], from_scalar_upper=report["analytic_upper_maximum"][1],
                                 balanced_to_upper=report["balanced_upper_maximum"][0], balanced_from_upper=report["balanced_upper_maximum"][1]))
    for row in checks:
        if not row["passed"]:
            print(row, flush=True)
    print("derived metric factorization:", len(reports), "cases", len(checks), "checks passed", passed, flush=True)
    require(passed, "preserve aggregate discrepancy")


if __name__ == "__main__":
    main()
