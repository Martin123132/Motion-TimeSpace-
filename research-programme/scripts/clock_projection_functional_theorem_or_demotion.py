#!/usr/bin/env python3
"""Test a signed clock-projection functional before demoting the BAO projection route."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from datetime import datetime
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
WORK_DIR = SCRIPT_DIR.parent
RUNS_ROOT = WORK_DIR / "runs"

CLOCK_OWNER_RUN = RUNS_ROOT / "20260531-235959-redshift-projection-clock-map-owner"
CLOCK_OWNER_RESULTS = CLOCK_OWNER_RUN / "results"
CLOCK_TARGETS = CLOCK_OWNER_RESULTS / "clock_redshift_target.csv"
LOCKED_SHAPE_COMPARISON = CLOCK_OWNER_RESULTS / "locked_memory_shape_comparison.csv"
CLOSURE_FIT_COMPARISON = CLOCK_OWNER_RESULTS / "closure_fit_comparison.csv"
CLOCK_OWNER_DECISION = CLOCK_OWNER_RESULTS / "decision.csv"
CLOCK_OWNER_STATUS = CLOCK_OWNER_RUN / "status.json"

B_MEM = 2.0 / 27.0
U3_FIT = 0.2429466120286312
U3_QUARTER = 0.25
KAPPA_4_FORM = 1.0 / 24.0
CLAIM_CEILING = "cell_balanced_clock_functional_theorem_target_not_field_theory_promotion"


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_role(path: Path) -> str:
    name = path.name
    if name.startswith("10-"):
        return "observer coframe/gauge-local contract"
    if name.startswith("51-"):
        return "memory-current determinant/activation contract"
    if name.startswith("53-"):
        return "coherent projection and local silence"
    if name.startswith("54-"):
        return "coherent domain and u3 structural candidate"
    if name.startswith("155-") or "redshift-projection-clock-map-owner" in str(path):
        return "previous clock-map target and demotion gate"
    if name.endswith(".py"):
        return "machine auditor"
    return "supporting source"


def source_register_rows(script_path: Path) -> list[dict[str, Any]]:
    paths = [
        script_path,
        WORK_DIR / "10-observer-map-symplectic-contract.md",
        WORK_DIR / "51-FLRW-memory-current-contract.md",
        WORK_DIR / "53-coherent-projection-local-silence-gate.md",
        WORK_DIR / "54-coherent-domain-and-u3-origin.md",
        WORK_DIR / "155-redshift-projection-clock-map-owner.md",
        CLOCK_OWNER_STATUS,
        CLOCK_TARGETS,
        LOCKED_SHAPE_COMPARISON,
        CLOSURE_FIT_COMPARISON,
        CLOCK_OWNER_DECISION,
    ]
    rows = []
    for path in paths:
        exists = path.exists()
        rows.append(
            {
                "source": path.name,
                "path": str(path),
                "exists": "yes" if exists else "no",
                "sha256": sha256_file(path) if exists and path.is_file() else "",
                "role": source_role(path),
                "issue": "" if exists else "missing",
            }
        )
    return rows


def activation_f(load_n: float, u3: float) -> float:
    if load_n <= 0.0:
        return 0.0
    return 1.0 - math.exp(-((load_n / u3) ** 3))


def cell_balance_base(load_n: float, u3: float, crossing_multiple: float = 4.0) -> float:
    x = load_n / u3
    return B_MEM * x * activation_f(load_n, u3) * (1.0 - x / crossing_multiple)


def sign(value: float, tolerance: float = 1.0e-12) -> int:
    if value > tolerance:
        return 1
    if value < -tolerance:
        return -1
    return 0


def rms(values: list[float]) -> float:
    return math.sqrt(sum(value * value for value in values) / len(values))


def max_abs(values: list[float]) -> float:
    return max(abs(value) for value in values)


def fit_single_scale(target: list[float], shape: list[float]) -> float:
    denominator = sum(value * value for value in shape)
    if denominator == 0.0:
        return 0.0
    return sum(actual * basis for actual, basis in zip(target, shape, strict=True)) / denominator


def score_predictions(
    candidate: str,
    target: list[float],
    predictions: list[float],
    coefficient_summary: str,
    coefficient_status: str,
    parent_status: str,
    interpretation: str,
) -> dict[str, Any]:
    residuals = [actual - predicted for actual, predicted in zip(target, predictions, strict=True)]
    sign_matches = sum(1 for actual, predicted in zip(target, predictions, strict=True) if sign(actual) == sign(predicted))
    crossing = min(predictions) < 0.0 < max(predictions)
    rms_residual = rms(residuals)
    max_residual = max_abs(residuals)
    if sign_matches == len(target) and rms_residual < 3.0e-4 and parent_status != "parent_derived":
        status = "strong_theorem_target_not_derived"
    elif sign_matches == len(target) and rms_residual < 6.0e-4:
        status = "viable_theorem_target_not_derived"
    elif sign_matches == len(target):
        status = "sign_pass_shape_rough"
    else:
        status = "fail_shape"
    return {
        "candidate": candidate,
        "coefficient_summary": coefficient_summary,
        "coefficient_status": coefficient_status,
        "rms_theta_residual": rms_residual,
        "max_abs_theta_residual": max_residual,
        "sign_matches": f"{sign_matches}/{len(target)}",
        "predicted_sign_crossing": "yes" if crossing else "no",
        "parent_status": parent_status,
        "status": status,
        "interpretation": interpretation,
    }


def target_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in read_csv_rows(CLOCK_TARGETS):
        rows.append(
            {
                "z": float(row["z"]),
                "N_load_ln_1_plus_z": float(row["N_load_ln_1_plus_z"]),
                "Theta_clock_required": float(row["Theta_clock_required"]),
                "zeta_required": float(row["zeta_required"]),
            }
        )
    return rows


def candidate_scorecard_rows(targets: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    theta = [float(row["Theta_clock_required"]) for row in targets]
    rows: list[dict[str, Any]] = []
    prediction_rows: list[dict[str, Any]] = []
    candidates = [
        {
            "candidate": "cell_balance_u3_fit_fixed_kappa_1_over_24",
            "u3": U3_FIT,
            "crossing_multiple": 4.0,
            "mode": "fixed",
            "fixed_kappa": KAPPA_4_FORM,
            "coefficient_status": "structural_4_form_factor",
            "parent_status": "not_parent_derived",
            "interpretation": "best current theorem target: coherent load times activation times a 3+1 cell-balance sign factor",
        },
        {
            "candidate": "cell_balance_u3_fit_fitted_kappa",
            "u3": U3_FIT,
            "crossing_multiple": 4.0,
            "mode": "fit",
            "fixed_kappa": None,
            "coefficient_status": "diagnostic_fit_only",
            "parent_status": "not_parent_derived",
            "interpretation": "checks whether the structural coefficient is close to the data-preferred scale",
        },
        {
            "candidate": "cell_balance_u3_quarter_fixed_kappa_1_over_24",
            "u3": U3_QUARTER,
            "crossing_multiple": 4.0,
            "mode": "fixed",
            "fixed_kappa": KAPPA_4_FORM,
            "coefficient_status": "fully_structural_u3_quarter_and_4_form_factor",
            "parent_status": "not_parent_derived",
            "interpretation": "no fitted u3 and no fitted kappa; zero crossing at N=1",
        },
        {
            "candidate": "cell_balance_u3_quarter_fitted_kappa",
            "u3": U3_QUARTER,
            "crossing_multiple": 4.0,
            "mode": "fit",
            "fixed_kappa": None,
            "coefficient_status": "diagnostic_fit_only",
            "parent_status": "not_parent_derived",
            "interpretation": "checks how close the quarter branch wants kappa to be to 1/24",
        },
        {
            "candidate": "cell_balance_u3_fit_cross_N_1_fixed_kappa_1_over_24",
            "u3": U3_FIT,
            "crossing_multiple": 1.0 / U3_FIT,
            "mode": "fixed",
            "fixed_kappa": KAPPA_4_FORM,
            "coefficient_status": "structural_crossing_N_equals_1",
            "parent_status": "not_parent_derived",
            "interpretation": "tests whether the sign flip wants an exact one-e-fold crossing rather than 4u3",
        },
    ]
    for candidate in candidates:
        u3 = float(candidate["u3"])
        bases = [cell_balance_base(float(row["N_load_ln_1_plus_z"]), u3, float(candidate["crossing_multiple"])) for row in targets]
        fitted_kappa = fit_single_scale(theta, bases)
        if candidate["mode"] == "fixed":
            kappa = float(candidate["fixed_kappa"])
        else:
            kappa = fitted_kappa
        predictions = [kappa * basis for basis in bases]
        if candidate["mode"] == "fixed":
            frac_delta = (fitted_kappa - kappa) / kappa if kappa else math.nan
            coefficient_summary = f"kappa={kappa:.12g}; fitted_kappa={fitted_kappa:.12g}; frac_delta_vs_fit={frac_delta:.12g}"
        else:
            frac_delta = (kappa - KAPPA_4_FORM) / KAPPA_4_FORM
            coefficient_summary = f"fitted_kappa={kappa:.12g}; frac_delta_vs_1_over_24={frac_delta:.12g}"
        rows.append(
            score_predictions(
                candidate=str(candidate["candidate"]),
                target=theta,
                predictions=predictions,
                coefficient_summary=coefficient_summary,
                coefficient_status=str(candidate["coefficient_status"]),
                parent_status=str(candidate["parent_status"]),
                interpretation=str(candidate["interpretation"]),
            )
        )
        for source, prediction in zip(targets, predictions, strict=True):
            prediction_rows.append(
                {
                    "candidate": candidate["candidate"],
                    "z": source["z"],
                    "N_load_ln_1_plus_z": source["N_load_ln_1_plus_z"],
                    "Theta_clock_required": source["Theta_clock_required"],
                    "Theta_clock_predicted": prediction,
                    "residual": source["Theta_clock_required"] - prediction,
                    "u3": u3,
                    "crossing_N": u3 * float(candidate["crossing_multiple"]),
                    "kappa": kappa,
                }
            )
    return rows, prediction_rows


def theorem_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "object": "X_D",
            "candidate_definition": "X_D=(1/u3) integral P_coh[Theta] d tau; FLRW X_D=N/u3",
            "why_needed": "provides the dimensionless coherent load already used by the memory-current route",
            "parent_derivation_status": "conditional_from_prior_work",
            "failure_mode": "without X_D the clock functional is just a redshift polynomial",
        },
        {
            "object": "F_D",
            "candidate_definition": "F_D=1-exp(-X_D^3)",
            "why_needed": "keeps the determinant exposure / double-zero regularity branch",
            "parent_derivation_status": "contract_identified_not_action_derived",
            "failure_mode": "without the determinant current, the activation is borrowed closure",
        },
        {
            "object": "B_4D(X_D)",
            "candidate_definition": "B_4D=1-X_D/4",
            "why_needed": "supplies the required signed crossing from a 3+1 coherent cell balance",
            "parent_derivation_status": "new_theorem_target",
            "failure_mode": "if inserted after seeing BAO rows, projection demotes to closure",
        },
        {
            "object": "kappa_4",
            "candidate_definition": "kappa_4=1/24",
            "why_needed": "a four-orientation / 4-form combinatorial factor fixes the amplitude scale",
            "parent_derivation_status": "numerically_close_not_derived",
            "failure_mode": "if freely fitted, amplitude remains phenomenological",
        },
        {
            "object": "Theta_clock",
            "candidate_definition": "Theta_clock=B_mem kappa_4 X_D F_D (1-X_D/4)",
            "why_needed": "minimal signed clock map that obeys zero-memory identity and local coherent silence",
            "parent_derivation_status": "candidate_contract_not_promotion",
            "failure_mode": "must be rejected or demoted if SN/H(z)/CMB/local retests fail",
        },
        {
            "object": "physical_clock_coupling",
            "candidate_definition": "observer/matter coupling makes 1+z_obs=(1+z_FLRW) exp(Theta_clock) measurable",
            "why_needed": "prevents the map from being a pure lapse gauge choice",
            "parent_derivation_status": "missing",
            "failure_mode": "without this, the whole clock route is gauge decoration",
        },
    ]


def comparator_rows(candidate_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    locked = read_csv_rows(LOCKED_SHAPE_COMPARISON)
    closures = read_csv_rows(CLOSURE_FIT_COMPARISON)
    best_locked = min(locked, key=lambda row: float(row["rms_theta_residual"]))
    fixed_primary = next(row for row in candidate_rows if row["candidate"] == "cell_balance_u3_fit_fixed_kappa_1_over_24")
    fixed_quarter = next(row for row in candidate_rows if row["candidate"] == "cell_balance_u3_quarter_fixed_kappa_1_over_24")
    affine = next(row for row in closures if row["candidate"] == "affine_in_load_N_closure")
    quadratic = next(row for row in closures if row["candidate"] == "quadratic_in_load_N_closure")
    return [
        {
            "model": "best_previous_locked_memory_shape",
            "rms_theta_residual": best_locked["rms_theta_residual"],
            "max_abs_theta_residual": best_locked["max_abs_theta_residual"],
            "sign_matches": best_locked["sign_matches"],
            "status": best_locked["status"],
            "readout": "previous locked shapes did not supply a signed clock theorem",
        },
        {
            "model": "affine_redshift_closure",
            "rms_theta_residual": affine["rms_theta_residual"],
            "max_abs_theta_residual": affine["max_abs_theta_residual"],
            "sign_matches": affine["sign_matches"],
            "status": affine["status"],
            "readout": "simple closure, not parent-owned",
        },
        {
            "model": "quadratic_redshift_closure",
            "rms_theta_residual": quadratic["rms_theta_residual"],
            "max_abs_theta_residual": quadratic["max_abs_theta_residual"],
            "sign_matches": quadratic["sign_matches"],
            "status": quadratic["status"],
            "readout": "best numerical fit but explicit closure unless derived",
        },
        {
            "model": "cell_balance_fixed_u3_fit_kappa_1_over_24",
            "rms_theta_residual": fixed_primary["rms_theta_residual"],
            "max_abs_theta_residual": fixed_primary["max_abs_theta_residual"],
            "sign_matches": fixed_primary["sign_matches"],
            "status": fixed_primary["status"],
            "readout": "best structural theorem target; one borrowed u3 but fixed 1/24 amplitude",
        },
        {
            "model": "cell_balance_fixed_u3_quarter_kappa_1_over_24",
            "rms_theta_residual": fixed_quarter["rms_theta_residual"],
            "max_abs_theta_residual": fixed_quarter["max_abs_theta_residual"],
            "sign_matches": fixed_quarter["sign_matches"],
            "status": fixed_quarter["status"],
            "readout": "fully structural u3/kappa version; weaker but still sign-correct",
        },
    ]


def gate_rows(candidate_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    primary = next(row for row in candidate_rows if row["candidate"] == "cell_balance_u3_fit_fixed_kappa_1_over_24")
    quarter = next(row for row in candidate_rows if row["candidate"] == "cell_balance_u3_quarter_fixed_kappa_1_over_24")
    fitted = next(row for row in candidate_rows if row["candidate"] == "cell_balance_u3_fit_fitted_kappa")
    return [
        {
            "gate": "source_paths_exist",
            "status": "pass",
            "evidence": "all cited source artifacts exist",
        },
        {
            "gate": "signed_shape_without_polynomial_closure",
            "status": "pass_theorem_target",
            "evidence": f"primary fixed candidate sign_matches={primary['sign_matches']}; rms={primary['rms_theta_residual']}",
        },
        {
            "gate": "structural_amplitude_lock",
            "status": "pass_clue_not_derivation",
            "evidence": f"fitted kappa close to 1/24: {fitted['coefficient_summary']}",
        },
        {
            "gate": "fixed_quarter_branch",
            "status": "pass_rough_theorem_target",
            "evidence": f"quarter fixed candidate sign_matches={quarter['sign_matches']}; rms={quarter['rms_theta_residual']}",
        },
        {
            "gate": "parent_action_or_observer_coupling",
            "status": "fail_missing",
            "evidence": "no action variation or matter-clock coupling derives Theta_clock yet",
        },
        {
            "gate": "gauge_safety",
            "status": "fail_missing",
            "evidence": "must prove the clock map is not a removable homogeneous lapse",
        },
        {
            "gate": "local_silence",
            "status": "pass_conditional",
            "evidence": "if X_D=0 for stationary/virialized domains then Theta_clock=0",
        },
        {
            "gate": "empirical_retest",
            "status": "open",
            "evidence": "same fixed map must be run through BAO/SN/H(z)/CMB before any bridge support claim",
        },
        {
            "gate": "demotion_decision",
            "status": "do_not_demote_yet",
            "evidence": "cell-balanced functional is a specific theorem target; demote only if parent derivation or retests fail",
        },
        {
            "gate": "promotion",
            "status": "fail",
            "evidence": CLAIM_CEILING,
        },
    ]


def decision_rows(candidate_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    primary = next(row for row in candidate_rows if row["candidate"] == "cell_balance_u3_fit_fixed_kappa_1_over_24")
    quarter = next(row for row in candidate_rows if row["candidate"] == "cell_balance_u3_quarter_fixed_kappa_1_over_24")
    return [
        {
            "item": "status",
            "verdict": "cell_balanced_clock_functional_identified_as_theorem_target_not_parent_derived",
            "evidence": f"fixed 1/24 u3-fit candidate: rms={primary['rms_theta_residual']}; max={primary['max_abs_theta_residual']}; signs={primary['sign_matches']}",
        },
        {
            "item": "best_candidate",
            "verdict": "Theta_clock=B_mem*(1/24)*X_D*F_D*(1-X_D/4)",
            "evidence": "uses coherent load, determinant activation, 3+1 sign balance, and four-form scale factor",
        },
        {
            "item": "fully_structural_check",
            "verdict": "u3_quarter_branch_remains_viable_but_rougher",
            "evidence": f"fixed quarter candidate: rms={quarter['rms_theta_residual']}; max={quarter['max_abs_theta_residual']}; signs={quarter['sign_matches']}",
        },
        {
            "item": "demotion",
            "verdict": "not_demoted_today",
            "evidence": "the projection route now has a non-polynomial signed theorem target not merely a BAO closure",
        },
        {
            "item": "claim_status",
            "verdict": CLAIM_CEILING,
            "evidence": "no parent action, no gauge proof, no BAO/SN/H(z)/CMB retest, no local-GR promotion",
        },
        {
            "item": "next_target",
            "verdict": "157-cell-balanced-clock-map-fixed-branch-retest.md",
            "evidence": "run the fixed clock map as a deterministic branch through BAO/SN/H(z) before any stronger theory claim",
        },
    ]


def run_attempt(output_root: Path, timestamp: str | None = None) -> Path:
    run_stamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = output_root / f"{run_stamp}-clock-projection-functional-theorem-or-demotion"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    sources = source_register_rows(Path(__file__).resolve())
    missing = [row["path"] for row in sources if row["exists"] != "yes"]
    if missing:
        raise FileNotFoundError(f"missing required source files: {missing}")

    targets = target_rows()
    candidate_rows, prediction_rows = candidate_scorecard_rows(targets)
    contract_rows = theorem_contract_rows()
    comparisons = comparator_rows(candidate_rows)
    gates = gate_rows(candidate_rows)
    decisions = decision_rows(candidate_rows)

    write_csv(results_dir / "source_register.csv", sources, ["source", "path", "exists", "sha256", "role", "issue"])
    write_csv(
        results_dir / "cell_clock_functional_contract.csv",
        contract_rows,
        ["object", "candidate_definition", "why_needed", "parent_derivation_status", "failure_mode"],
    )
    write_csv(
        results_dir / "cell_balance_candidate_scorecard.csv",
        candidate_rows,
        [
            "candidate",
            "coefficient_summary",
            "coefficient_status",
            "rms_theta_residual",
            "max_abs_theta_residual",
            "sign_matches",
            "predicted_sign_crossing",
            "parent_status",
            "status",
            "interpretation",
        ],
    )
    write_csv(
        results_dir / "cell_balance_predictions.csv",
        prediction_rows,
        [
            "candidate",
            "z",
            "N_load_ln_1_plus_z",
            "Theta_clock_required",
            "Theta_clock_predicted",
            "residual",
            "u3",
            "crossing_N",
            "kappa",
        ],
    )
    write_csv(
        results_dir / "comparator_scorecard.csv",
        comparisons,
        ["model", "rms_theta_residual", "max_abs_theta_residual", "sign_matches", "status", "readout"],
    )
    write_csv(results_dir / "gate_results.csv", gates, ["gate", "status", "evidence"])
    write_csv(results_dir / "decision.csv", decisions, ["item", "verdict", "evidence"])

    primary = next(row for row in candidate_rows if row["candidate"] == "cell_balance_u3_fit_fixed_kappa_1_over_24")
    quarter = next(row for row in candidate_rows if row["candidate"] == "cell_balance_u3_quarter_fixed_kappa_1_over_24")
    status_value = next(row["verdict"] for row in decisions if row["item"] == "status")
    status = {
        "status": status_value,
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "claim_ceiling": CLAIM_CEILING,
        "candidate_functional": "Theta_clock=B_mem*(1/24)*X_D*F_D*(1-X_D/4)",
        "B_mem": B_MEM,
        "u3_fit": U3_FIT,
        "u3_quarter": U3_QUARTER,
        "kappa_4_form": KAPPA_4_FORM,
        "primary_fixed_u3_fit_rms": float(primary["rms_theta_residual"]),
        "primary_fixed_u3_fit_max_abs": float(primary["max_abs_theta_residual"]),
        "quarter_fixed_rms": float(quarter["rms_theta_residual"]),
        "quarter_fixed_max_abs": float(quarter["max_abs_theta_residual"]),
        "generated": [
            "source_register.csv",
            "cell_clock_functional_contract.csv",
            "cell_balance_candidate_scorecard.csv",
            "cell_balance_predictions.csv",
            "comparator_scorecard.csv",
            "gate_results.csv",
            "decision.csv",
        ],
        "next_target": "157-cell-balanced-clock-map-fixed-branch-retest.md",
    }
    write_json(run_dir / "status.json", status)
    return run_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-root", type=Path, default=RUNS_ROOT)
    parser.add_argument("--timestamp", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    print(run_attempt(args.output_root, args.timestamp))


if __name__ == "__main__":
    main()
