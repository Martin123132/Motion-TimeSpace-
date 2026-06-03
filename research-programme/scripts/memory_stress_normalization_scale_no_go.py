from __future__ import annotations

import argparse
import csv
import json
import math
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "memory-stress-normalization-scale-no-go"
STATUS = "memory_stress_normalization_scale_no_go_Bmem_requires_boundary_charge_owner"
CLAIM_CEILING = "amplitude_not_derived_exact_parent_contract_written"

P = 3.0
U3 = 0.25
B_LOCKED = 2.0 / 27.0
DELTA_R_TARGET = 2.0 / 9.0
R_EARLY = 1.0 / 3.0
R_TODAY = 1.0 / 9.0


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def relpath(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def activation(N: float, p: float = P, u: float = U3) -> float:
    if N <= 0.0:
        return 0.0
    return 1.0 - math.exp(-((N / u) ** p))


def activation_derivative(N: float, p: float = P, u: float = U3) -> float:
    if N <= 0.0:
        return 0.0 if p > 1.0 else p / u
    x = N / u
    return (p / u) * (x ** (p - 1.0)) * math.exp(-(x**p))


def trapz(values: list[float], step: float) -> float:
    if len(values) < 2:
        return 0.0
    return step * (0.5 * values[0] + sum(values[1:-1]) + 0.5 * values[-1])


def source_register_rows() -> list[dict[str, Any]]:
    sources = [
        (ROOT / "139-density-law-hazard-theorem-attempt.md", "hazard derivation that fixes activation shape but not amplitude"),
        (ROOT / "140-boundary-charge-amplitude-decision-gate.md", "amplitude demotion and boundary-charge theorem target"),
        (ROOT / "141-consolidated-locked-memory-branch-contract.md", "locked branch contract and promotion requirements"),
        (ROOT / "285-generic-SN-BAO-short-smoke-with-ablations.md", "latest generic empirical checkpoint keeping fixed branch live but mixed"),
        (ROOT / "scripts" / "memory_stress_normalization_scale_no_go.py", "this derivation/no-go script"),
    ]
    return [{"source": relpath(path), "role": role, "exists": "yes" if path.exists() else "no"} for path, role in sources]


def normalization_integral_rows() -> list[dict[str, Any]]:
    n_max = 5.0
    steps = 40000
    step = n_max / steps
    grid = [i * step for i in range(steps + 1)]
    a_n_values = [activation_derivative(N) for N in grid]
    integral_a_n = trapz(a_n_values, step)
    rows = []
    for label, B in [
        ("zero_memory", 0.0),
        ("one_over_27_probe", 1.0 / 27.0),
        ("locked_two_over_27", B_LOCKED),
        ("near_primary_fitted_0p0745331916", 0.07453319160061826),
    ]:
        rows.append(
            {
                "branch": label,
                "B_mem": B,
                "integral_A_N_numeric": integral_a_n,
                "integral_A_N_exact": 1.0,
                "total_density_release_integral": B * integral_a_n,
                "pressure_kernel_impulse_integral": B * integral_a_n / 3.0,
                "kernel_identity": "p_plus_rho=B_mem*A_N/3",
                "amplitude_selected": "no",
            }
        )
    return rows


def scale_symmetry_rows() -> list[dict[str, Any]]:
    sample_points = [0.0, 0.02, 0.05, 0.1, 0.25, 0.5, 1.0, 2.0]
    rows = []
    for label, B in [
        ("zero_memory", 0.0),
        ("one_over_27_probe", 1.0 / 27.0),
        ("locked_two_over_27", B_LOCKED),
        ("near_primary_fitted_0p0745331916", 0.07453319160061826),
    ]:
        max_kernel_residual = 0.0
        max_density_rescale_error = 0.0
        reference_B = B_LOCKED
        for N in sample_points:
            a_n = activation_derivative(N)
            rho_n = B * a_n
            p_plus_rho = B * a_n / 3.0
            max_kernel_residual = max(max_kernel_residual, abs(3.0 * p_plus_rho - rho_n))
            if reference_B != 0.0:
                expected_ratio = B / reference_B
                reference_rho_n = reference_B * a_n
                if abs(reference_rho_n) > 1e-15:
                    max_density_rescale_error = max(max_density_rescale_error, abs((rho_n / reference_rho_n) - expected_ratio))
        rows.append(
            {
                "branch": label,
                "B_mem": B,
                "max_pressure_kernel_residual": max_kernel_residual,
                "max_density_rescale_error_vs_locked": max_density_rescale_error,
                "conservation_shape_preserved": "yes",
                "amplitude_fixed_by_kernel": "no",
            }
        )
    return rows


def endpoint_quadratic_rows() -> list[dict[str, Any]]:
    roots = [R_TODAY, R_EARLY]
    rows = []
    for label, R in [("today_low_endpoint", R_TODAY), ("early_high_endpoint", R_EARLY)]:
        F = 27.0 * R * R - 12.0 * R + 1.0
        U = 9.0 * R**3 - 6.0 * R**2 + R
        U2 = 54.0 * R - 12.0
        rows.append(
            {
                "endpoint": label,
                "R": R,
                "F_27R2_minus_12R_plus_1": F,
                "formal_potential_U": U,
                "second_derivative_Upp": U2,
                "ordinary_gradient_role": "unstable" if U2 < 0 else "stable",
            }
        )
    rows.append(
        {
            "endpoint": "contrast",
            "R": DELTA_R_TARGET,
            "F_27R2_minus_12R_plus_1": "",
            "formal_potential_U": "",
            "second_derivative_Upp": "",
            "ordinary_gradient_role": "DeltaR=R_early-R_today; B_mem=DeltaR/3",
        }
    )
    return rows


def amplitude_route_rows() -> list[dict[str, Any]]:
    return [
        {
            "route": "Bianchi_or_continuity",
            "result": "no_go",
            "reason": "fixes pressure relation p+rho=rho_N/3 but is homogeneous in B_mem",
            "promotion_effect": "cannot derive 2/27",
        },
        {
            "route": "additive_hazard_survival",
            "result": "no_go_for_amplitude",
            "reason": "fixes A=1-exp(-I_M) and integral A_N=1 but leaves total released charge arbitrary",
            "promotion_effect": "shape support only",
        },
        {
            "route": "stress_impulse_normalization",
            "result": "conditional_restatement",
            "reason": "integral(p+rho)dN=B_mem/3; choosing its value chooses B_mem",
            "promotion_effect": "circular unless parent action fixes impulse independently",
        },
        {
            "route": "endpoint_quadratic",
            "result": "formal_theorem_target",
            "reason": "roots 1/9 and 1/3 give DeltaR=2/9 but coefficients and endpoint arrow are not parent-owned",
            "promotion_effect": "exact target, not current derivation",
        },
        {
            "route": "normalized_boundary_charge",
            "result": "only_viable_contract",
            "reason": "a non-homogeneous charge quantization or Ward identity could set DeltaR=2/9 before data",
            "promotion_effect": "would derive B_mem=DeltaR/3=2/27 if all contract clauses are proven",
        },
    ]


def parent_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "clause": "boundary_current_owner",
            "must_prove": "parent variables define a conserved relative boundary current J_B before FLRW reduction",
            "why_needed": "without a current there is no charge whose normalization can fix B_mem",
            "status": "open",
        },
        {
            "clause": "charge_unit",
            "must_prove": "a dimensionless Q_* is fixed by the action or a Ward identity, not fitted",
            "why_needed": "DeltaR=Q_B/Q_* is meaningless without a non-data unit",
            "status": "open",
        },
        {
            "clause": "endpoint_equations",
            "must_prove": "endpoint stationarity gives 27R^2-12R+1=0 with coefficients fixed before data",
            "why_needed": "this is the exact source of R=1/3 and R=1/9",
            "status": "formal_target",
        },
        {
            "clause": "endpoint_arrow",
            "must_prove": "the parent dynamics select the cosmological transition 1/3 -> 1/9",
            "why_needed": "ordinary formal potential stability points the wrong way for the desired arrow",
            "status": "open",
        },
        {
            "clause": "trace_partition",
            "must_prove": "the background density amplitude receives one third of DeltaR by spatial trace partition",
            "why_needed": "B_mem=DeltaR/3 is required for 2/27",
            "status": "open",
        },
        {
            "clause": "local_silence",
            "must_prove": "the same current vanishes or is projected out in local vacuum/PPN domains",
            "why_needed": "cosmology amplitude cannot break the local GR branch",
            "status": "open",
        },
        {
            "clause": "Bianchi_closure",
            "must_prove": "metric variation of the current stress is covariantly conserved with the matter sector",
            "why_needed": "field-theory promotion requires conservation, not just background fitting",
            "status": "open",
        },
    ]


def gate_rows() -> list[dict[str, Any]]:
    source_missing = [row for row in source_register_rows() if row["exists"] != "yes"]
    scale = scale_symmetry_rows()
    integrals = normalization_integral_rows()
    endpoint = endpoint_quadratic_rows()
    return [
        {
            "gate": "source_paths_exist",
            "status": "pass" if not source_missing else "fail",
            "evidence": "all sources present" if not source_missing else ";".join(row["source"] for row in source_missing),
            "claim_effect": "derivation audit is traceable",
        },
        {
            "gate": "pressure_kernel_selects_amplitude",
            "status": "fail",
            "evidence": "max residuals vanish for multiple B_mem values",
            "claim_effect": "kernel is homogeneous in B_mem",
        },
        {
            "gate": "hazard_integral_selects_amplitude",
            "status": "fail",
            "evidence": f"integral_A_N={integrals[0]['integral_A_N_numeric']}",
            "claim_effect": "hazard fixes unit activation fraction, not total charge",
        },
        {
            "gate": "scale_symmetry_no_go",
            "status": "pass",
            "evidence": "; ".join(f"{row['branch']} residual={row['max_pressure_kernel_residual']}" for row in scale),
            "claim_effect": "B_mem cannot be derived from homogeneous stress equations alone",
        },
        {
            "gate": "endpoint_quadratic_exact_target",
            "status": "pass_formal",
            "evidence": f"R_early={R_EARLY}; R_today={R_TODAY}; DeltaR={DELTA_R_TARGET}; B={B_LOCKED}",
            "claim_effect": "exact target retained",
        },
        {
            "gate": "endpoint_arrow_derived",
            "status": "fail",
            "evidence": "; ".join(f"{row['endpoint']}:{row['ordinary_gradient_role']}" for row in endpoint if row["endpoint"] != "contrast"),
            "claim_effect": "formal potential cannot promote amplitude",
        },
        {
            "gate": "parent_contract_written",
            "status": "pass",
            "evidence": "boundary current, charge unit, endpoint equation, arrow, trace partition, local silence, Bianchi closure",
            "claim_effect": "future derivation target is exact",
        },
        {
            "gate": "B_mem_derived_now",
            "status": "fail",
            "evidence": "requires non-homogeneous parent-owned boundary charge",
            "claim_effect": "2/27 remains empirical closure/theorem target",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "meaning": (
                "The memory stress equations, continuity/Bianchi condition, and additive hazard law are homogeneous in the amplitude. "
                "They preserve their identities for any B_mem, so they cannot select 2/27. "
                "The only non-circular route is a parent-owned normalized boundary charge that fixes DeltaR=2/9 and then maps B_mem=DeltaR/3."
            ),
            "next_target": "derive_boundary_current_owner_or_keep_Bmem_as_locked_empirical_closure",
        }
    ]


def build_outputs(timestamp: str) -> dict[str, Any]:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    outputs = {
        "source_register.csv": (source_register_rows(), ["source", "role", "exists"]),
        "normalization_integrals.csv": (
            normalization_integral_rows(),
            [
                "branch",
                "B_mem",
                "integral_A_N_numeric",
                "integral_A_N_exact",
                "total_density_release_integral",
                "pressure_kernel_impulse_integral",
                "kernel_identity",
                "amplitude_selected",
            ],
        ),
        "scale_symmetry_no_go.csv": (
            scale_symmetry_rows(),
            ["branch", "B_mem", "max_pressure_kernel_residual", "max_density_rescale_error_vs_locked", "conservation_shape_preserved", "amplitude_fixed_by_kernel"],
        ),
        "endpoint_quadratic_reaudit.csv": (
            endpoint_quadratic_rows(),
            ["endpoint", "R", "F_27R2_minus_12R_plus_1", "formal_potential_U", "second_derivative_Upp", "ordinary_gradient_role"],
        ),
        "amplitude_route_ledger.csv": (amplitude_route_rows(), ["route", "result", "reason", "promotion_effect"]),
        "parent_contract.csv": (parent_contract_rows(), ["clause", "must_prove", "why_needed", "status"]),
        "gate_results.csv": (gate_rows(), ["gate", "status", "evidence", "claim_effect"]),
        "decision.csv": (decision_rows(), ["decision", "claim_ceiling", "meaning", "next_target"]),
    }
    for filename, (rows, fieldnames) in outputs.items():
        write_csv(results_dir / filename, rows, fieldnames)

    payload = {
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "generated": list(outputs),
        "B_mem_locked": B_LOCKED,
        "DeltaR_target": DELTA_R_TARGET,
        "B_mem_derived_now": False,
        "no_go_reason": "memory_stress_and_hazard_equations_are_homogeneous_in_Bmem",
        "only_viable_derivation_route": "parent_owned_normalized_boundary_charge_DeltaR_2over9_then_trace_partition_Bmem_DeltaR_over_3",
        "next_target": "derive_boundary_current_owner_or_keep_Bmem_as_locked_empirical_closure",
    }
    write_json(run_dir / "status.json", payload)
    (run_dir / "DONE.txt").write_text(STATUS + "\n", encoding="utf-8")
    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Memory-stress normalization scale no-go.")
    parser.add_argument("--timestamp", default=datetime.now().strftime("%Y%m%d-%H%M%S"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = build_outputs(args.timestamp)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
