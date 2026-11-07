from common import *
from polynomial_budget import unit_checks
import numpy as np


def main():
    modest()
    check_parent()
    require(LABEL == "summary", "summary family")
    checks, reports, evidence = [], [], {}
    for family in ("half", "balanced", "double"):
        root = STAGE / family
        result, validation = read(root / "result.json"), read(root / "validation.json")
        require(result["passed"] and validation["passed"] and all(row["passed"] for row in validation["checks"]), "family gates")
        for path, expected in read(root / "inputs.json")["sources"].items():
            require(digest(path) == expected, "frozen family source")
        for path, expected in result["input_hashes"].items():
            require(digest(path) == expected, "retained packet")
        for model in result["reports"]:
            for case in model["cases"]:
                require(digest(case["packet"]) == case["sha256"], "new kernel packet")
            fine = model["cases"][1]["budgets"][0]
            reports.append(dict(family=family, model=model["model"], wave=model["wave"], N_interval=model["N_interval"],
                                H_over_k_sample_max=model["H_over_k_sample_max"], measured=model["measured"],
                                source_suprema=fine["source_suprema"], kernel_L1=fine["kernel_L1"],
                                holder_terms=fine["holder_terms"], holder_budget=fine["holder_budget"],
                                combined_budget=fine["combined_budget"], cancellation_factor=fine["cancellation_factor"],
                                independent_readback_error=model["cases"][1]["readback_error"],
                                native_phase_error=result["phase"], uniform_bound_proved=False))
        evidence[str(root / "result.json")] = digest(root / "result.json")
        evidence[str(root / "validation.json")] = digest(root / "validation.json")
        checks.extend(dict(family=family, **row) for row in validation["checks"])
    for model in ("heavy", "cold"):
        intervals = [row["N_interval"] for row in reports if row["model"] == model]
        require(all(interval == intervals[0] for interval in intervals), "common retained time interval")
    require(len(unit_checks()) == 16, "independent polynomial recheck")
    check_parent()
    write(ROOT / "summary.json", dict(passed=True, reports=reports, source_order=["current_M", "shear_S"],
          readout_order=["D", "delta_c"], holder_term_order=["endpoint_current", "integrated_current", "integrated_shear"],
          new_ode_solves=0, retained_adjoint_traces=12, phase_reduction_native_samples=291,
          artificial_carrier_and_explicit_gradient_gamma_cancel=True,
          physical_frequency_and_velocity_derivative_retained=True, uniform_limit_proved=False,
          evidence_hashes=evidence))
    write(ROOT / "validation.json", dict(passed=True, count=len(checks), checks=checks))
    print("source-gain and phase cancellation aggregate passed", len(checks), flush=True)


if __name__ == "__main__":
    main()

