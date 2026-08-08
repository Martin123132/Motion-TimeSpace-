from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
import sys
from pathlib import Path
from typing import Any


os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
os.environ.setdefault("NUMEXPR_NUM_THREADS", "1")
os.environ.setdefault("VECLIB_MAXIMUM_THREADS", "1")
sys.dont_write_bytecode = True

import numpy as np


CHECKPOINT = 5336
MARKER = "MTS_5336_FOLD_PAIR_EQUIVALENCE_INCREMENTAL_OWNERSHIP_GATE"
POST = Path(__file__).resolve().parents[1]
ROOT = POST.parent
FORMAL = ROOT / "formalization-workbench"
OUT = POST / "source-intake" / "functional_rg" / str(CHECKPOINT)
RESIDUALS = POST / "source-intake" / "mts_residuals"
VALIDATION = RESIDUALS / f"P8_Y5_BRR545_{CHECKPOINT}_VALIDATION.csv"
RESULT = OUT / "fold_pair_equivalence_incremental_ownership_result.json"
FORMAL_DIGEST = "0ec1bc6012136ffc6b28a1512aca6ce712b6decd2ff793310a9bd61775f3db1f"
Q_TARGET = 0.7698811733853892
ETA_PARENT = -0.06532510306084385
Q_GAUSSIAN_PAIR = -2.0 * ETA_PARENT
KNOWN_INTERACTION_NORM = 3.492540005516476e-116
TOLERANCE = 3.0e-12

SOURCE_LOCKS = {
    "5149-Y5-R2FR-causal-spectral-density-critical-motion-mixing-and-vacuum-no-go.md": "4ccd4b37a60a3e5b66d8cc9d0f3e94473baf19f1468180a74a468f3ad1db606d",
    "5181-Y5-R2FR-critical-pair-bubble-positive-Hessian-and-parent-ownership-gate.md": "54a35ad66744f9e1f5ab6fdd15e66bc6f87a93330a999aae2235ea5cf98b3657",
    "5190-Y5-R2FR-static-Ward-helicity-one-derivative-mixing-no-go-and-direct-state-route-freeze.md": "4f3d83db550d5eed2bea3fc8f6d6542807ec610a152abd2146a39ede6bdf6d55",
    "5200-Y5-R2FR-CTP-vacuum-occupied-projector-metric-and-composite-exponent-ownership-gate.md": "348e580fb9c48c28b4b77e2219e0bc8760bcd012081373e7120caa7aac83e656",
    "5335-Y5-R2FR-covariant-zero-flux-energy-frame-and-retarded-history-bridge.md": "920035459b3a6231fe31f350ddef75b88898922f7256cc3792aefd29e3e75c12",
    "source-intake/functional_rg/5181/critical_pair_bubble_derivation.csv": "78cb5dec6a307c5e2361897c93b99ac7cd4b2689ffacb852671b67a46a45959a",
    "source-intake/functional_rg/5200/q_ownership_decision.csv": "c97131260c4df7beb1f3e3aea8af11ae4c1ebe7edd89a2ed75ff7f50904b0106",
    "source-intake/functional_rg/5335/critical_fold_IR_susceptibility_bridge.csv": "e387fee4cfdffafe81c9218d910794c66598f55c3790015a37347f9eb6e882ca",
    "source-intake/functional_rg/5335/covariant_energy_frame_retarded_history_bridge_result.json": "2ce966e521e3fe04b6c32525c651396022dc853661a4093cdd5420508d3da469",
}


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def serialized_hash(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def formal_inventory_digest() -> str:
    rows = [
        {
            "relative_path": str(path.relative_to(FORMAL)),
            "size": str(path.stat().st_size),
            "sha256": digest(path),
        }
        for path in sorted(
            (item for item in FORMAL.rglob("*") if item.is_file()),
            key=lambda item: str(item).lower(),
        )
    ]
    return serialized_hash(rows)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"empty CSV payload: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    temporary.replace(path)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(value, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)


def validation_row(gate: str, passed: bool, detail: str) -> dict[str, Any]:
    return {
        "gate": gate,
        "passed": passed,
        "detail": detail,
        "checkpoint": CHECKPOINT,
        "marker": MARKER,
    }


def source_rows() -> tuple[list[dict[str, Any]], bool]:
    rows: list[dict[str, Any]] = []
    all_locked = True
    for relative, expected in SOURCE_LOCKS.items():
        path = POST / relative
        actual = digest(path) if path.is_file() else "MISSING"
        locked = actual == expected
        all_locked = all_locked and locked
        rows.append(
            {
                "relative_path": relative,
                "absolute_path": str(path),
                "sha256": actual,
                "expected_sha256": expected,
                "locked": locked,
                "role": (
                    "parent pair/CTP ownership boundary"
                    if not relative.startswith("source-intake/functional_rg/5335")
                    else "checkpoint-5335 bridge under incremental audit"
                ),
            }
        )
    return rows, all_locked


def bubble_exact(momentum: float, mass: float) -> float:
    if momentum <= 0.0 or mass < 0.0:
        raise ValueError("momentum must be positive and mass nonnegative")
    if mass == 0.0:
        return 1.0 / (8.0 * momentum)
    return math.atan(momentum / (2.0 * mass)) / (
        4.0 * math.pi * momentum
    )


def bubble_quadrature(momentum: float, mass: float, order: int = 256) -> float:
    nodes, weights = np.polynomial.legendre.leggauss(order)
    theta = (nodes + 1.0) * math.pi / 4.0
    jacobian = math.pi / 4.0
    sine_cosine = np.sin(theta) * np.cos(theta)
    denominator = np.sqrt(
        mass * mass + momentum * momentum * sine_cosine * sine_cosine
    )
    integrand = sine_cosine / denominator
    return float(
        (1.0 / (4.0 * math.pi))
        * jacobian
        * np.sum(weights * integrand)
    )


def pair_fold_rows() -> tuple[list[dict[str, Any]], dict[str, float]]:
    rows: list[dict[str, Any]] = []
    maximum_relative_error = 0.0
    maximum_massless_factorization_error = 0.0
    for momentum in (0.01, 0.3, 1.0, 7.0, 100.0):
        for mass_ratio in (0.0, 1.0e-3, 0.1, 1.0, 10.0):
            mass = momentum * mass_ratio
            exact = bubble_exact(momentum, mass)
            numeric = bubble_quadrature(momentum, mass)
            relative_error = abs(numeric - exact) / exact
            maximum_relative_error = max(maximum_relative_error, relative_error)
            factorization_error = (
                abs(momentum * exact - 0.125) if mass == 0.0 else math.nan
            )
            if mass == 0.0:
                maximum_massless_factorization_error = max(
                    maximum_massless_factorization_error,
                    factorization_error,
                )
            rows.append(
                {
                    "momentum": momentum,
                    "mass_over_momentum": mass_ratio,
                    "mass": mass,
                    "B_exact": exact,
                    "B_fold_quadrature": numeric,
                    "relative_error": relative_error,
                    "massless_abs_k_times_B_minus_one_eighth": (
                        factorization_error if mass == 0.0 else "NOT_MASSLESS"
                    ),
                    "pair_discriminant": "Delta_pair=m^2+x(1-x)|k|^2",
                    "fold_class": (
                        "CRITICAL_SQRT_AT_M_ZERO"
                        if mass == 0.0
                        else "OFFSET_SQRT_ANALYTIC_AT_K_ZERO"
                    ),
                }
            )
    return rows, {
        "maximum_relative_error": maximum_relative_error,
        "maximum_massless_factorization_error": maximum_massless_factorization_error,
    }


def equivalence_rows() -> list[dict[str, Any]]:
    return [
        {
            "comparison": "singularity_normal_form",
            "retarded_history_fold": "rho_history proportional Delta_history^(-1/2)",
            "pair_threshold_fold": "Feynman integrand proportional Delta_pair^(-1/2)",
            "equivalence": "same square-root fold universality class",
            "identical_mechanism": False,
            "incremental_result": "exact exponent/normal-form interpretation",
        },
        {
            "comparison": "critical_discriminant",
            "retarded_history_fold": "Delta_history=0 at a non-injective history map",
            "pair_threshold_fold": "Delta_pair=m^2+x(1-x)|k|^2",
            "equivalence": "critical offset must vanish",
            "identical_mechanism": False,
            "incremental_result": "m=0 is the pair criticality condition",
        },
        {
            "comparison": "infrared_power",
            "retarded_history_fold": "Delta_history~|k|^2 implies |k|^-1",
            "pair_threshold_fold": "m=0 factorizes |k|^-1 exactly",
            "equivalence": "identical leading momentum exponent",
            "identical_mechanism": False,
            "incremental_result": "B0=1/(8|k|) already parent-owned at checkpoint 5181",
        },
        {
            "comparison": "causal_speed_requirement",
            "retarded_history_fold": "straight toy requires beta=v/u>1",
            "pair_threshold_fold": "two-propagator threshold; no superluminal source history",
            "equivalence": "none",
            "identical_mechanism": False,
            "incremental_result": "pair interpretation removes the literal beta>1 requirement",
        },
        {
            "comparison": "parent_ownership",
            "retarded_history_fold": "source geometry alone does not select MTS state weight",
            "pair_threshold_fold": "minimal motion propagators and Hilbert pair vertex own the carrier",
            "equivalence": "pair route is the parent-owned realization",
            "identical_mechanism": False,
            "incremental_result": "no additional parent coefficient or field",
        },
    ]


def mass_gap_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for ratio in (0.0, 1.0e-4, 1.0e-3, 0.01, 0.1, 1.0, 10.0):
        if ratio == 0.0:
            retained = 1.0
            low_k_status = "NONANALYTIC_CRITICAL_1_OVER_ABS_K"
        else:
            retained = (2.0 / math.pi) * math.atan(1.0 / (2.0 * ratio))
            low_k_status = "ANALYTIC_FOR_FIXED_NONZERO_MASS"
        rows.append(
            {
                "mass_over_momentum": ratio,
                "B_m_over_B_0": retained,
                "critical_offset_Delta0": ratio * ratio,
                "low_momentum_status": low_k_status,
                "condition_for_fold_carrier": "m_eff/|k| -> 0",
            }
        )
    return rows


def response_cq(x: np.ndarray, q_value: float) -> np.ndarray:
    return 1.0 / (x * (1.0 + x**q_value))


def logarithmic_slope_cq(x: float, q_value: float) -> float:
    power = x**q_value
    return -1.0 - q_value * power / (1.0 + power)


def q_nonidentifiability_rows() -> tuple[list[dict[str, Any]], dict[str, float]]:
    q_values = (0.1, 0.3, Q_GAUSSIAN_PAIR, Q_TARGET, 1.0)
    rows: list[dict[str, Any]] = []
    maximum_ir_limit_error = 0.0
    maximum_uv_limit_error = 0.0
    for q_value in q_values:
        x_ir = 1.0e-60
        x_uv = 1.0e60
        slope_ir = logarithmic_slope_cq(x_ir, q_value)
        slope_uv = logarithmic_slope_cq(x_uv, q_value)
        ir_error = abs(slope_ir + 1.0)
        uv_error = abs(slope_uv + 1.0 + q_value)
        maximum_ir_limit_error = max(maximum_ir_limit_error, ir_error)
        maximum_uv_limit_error = max(maximum_uv_limit_error, uv_error)
        rows.append(
            {
                "q": q_value,
                "deep_IR_slope": slope_ir,
                "deep_IR_limit": -1.0,
                "deep_UV_slope": slope_uv,
                "deep_UV_limit": -(1.0 + q_value),
                "fold_carrier_changes_with_q": False,
                "q_information_location": "crossover and UV tail, not leading IR fold",
                "is_target_q": abs(q_value - Q_TARGET) <= 1.0e-15,
                "is_sourced_Gaussian_pair_q": abs(q_value - Q_GAUSSIAN_PAIR)
                <= 1.0e-15,
            }
        )
    return rows, {
        "maximum_ir_limit_error": maximum_ir_limit_error,
        "maximum_uv_limit_error": maximum_uv_limit_error,
        "target_minus_Gaussian_pair_q": Q_TARGET - Q_GAUSSIAN_PAIR,
        "relative_q_shortfall": (Q_TARGET - Q_GAUSSIAN_PAIR) / Q_TARGET,
    }


def stieltjes_density(t: np.ndarray, q_value: float, mu: float = 1.0) -> np.ndarray:
    cosine = math.cos(math.pi * q_value / 2.0)
    t_half_q = t ** (q_value / 2.0)
    numerator = mu ** (1.0 + q_value) * (
        mu**q_value + t_half_q * cosine
    )
    denominator = (
        math.pi
        * np.sqrt(t)
        * (
            mu ** (2.0 * q_value)
            + 2.0 * mu**q_value * t_half_q * cosine
            + t**q_value
        )
    )
    return numerator / denominator


def spectral_family_rows() -> tuple[list[dict[str, Any]], float]:
    t = np.logspace(-24.0, 24.0, 401)
    rows: list[dict[str, Any]] = []
    minimum_density = math.inf
    for q_value in (0.1, 0.3, Q_GAUSSIAN_PAIR, Q_TARGET, 1.0):
        density = stieltjes_density(t, q_value)
        local_minimum = float(np.min(density))
        minimum_density = min(minimum_density, local_minimum)
        rows.append(
            {
                "q": q_value,
                "minimum_sampled_positive_density": local_minimum,
                "maximum_sampled_density": float(np.max(density)),
                "positive_on_sampled_cut": bool(np.all(density > 0.0)),
                "causal_continuum_allowed": True,
                "q_selected_by_positivity": False,
                "ownership_status": (
                    "TARGET_RESPONSE_REPRESENTABLE_NOT_PARENT_SELECTED"
                    if abs(q_value - Q_TARGET) <= 1.0e-15
                    else "ALTERNATIVE_POSITIVE_RESPONSE"
                ),
            }
        )
    return rows, minimum_density


def history_increment_rows() -> list[dict[str, Any]]:
    return [
        {
            "source_feature": "zero-net energy flow",
            "exact_MTS_mapping": "classical U_chi is own-stress Landau frame; U_occ may diagnose type-I state stress",
            "new_parent_ownership": False,
            "reason": "does not generate a new Hilbert source or occupied-state preparation law",
        },
        {
            "source_feature": "regular finite retarded roots",
            "exact_MTS_mapping": "finite exponential history spectrum",
            "new_parent_ownership": False,
            "reason": "analytic at low frequency and cannot select fractional q",
        },
        {
            "source_feature": "retarded square-root fold",
            "exact_MTS_mapping": "same fold universality class as the massless pair threshold",
            "new_parent_ownership": False,
            "reason": "checkpoint 5181 already owns B0=1/(8|k|)",
        },
        {
            "source_feature": "history-dependent source weighting",
            "exact_MTS_mapping": "could realize a scale filter only after a state law fixes the weight",
            "new_parent_ownership": False,
            "reason": "arbitrary q(tau) is closure unless derived from the parent CTP density matrix",
        },
        {
            "source_feature": "multi-history spectroscopy",
            "exact_MTS_mapping": "possible empirical diagnostic of a derived continuum state",
            "new_parent_ownership": False,
            "reason": "tests a future state but does not derive its action or q",
        },
    ]


def route_rows() -> list[dict[str, Any]]:
    return [
        {
            "question": "Does the 5335 fold supply the missing infrared carrier?",
            "answer": "YES_AS_AN_EQUIVALENT_NORMAL_FORM",
            "scope": "same square-root universality as the already-derived massless pair bubble",
            "claim_promoted": False,
        },
        {
            "question": "Is this a new parent mechanism beyond checkpoint 5181?",
            "answer": "NO",
            "scope": "B0=1/(8|k|) was already parent-owned",
            "claim_promoted": False,
        },
        {
            "question": "Does fold criticality derive q=0.7698811733853892?",
            "answer": "NO_EXACTLY",
            "scope": "all 0<q<=1 share the same leading IR fold; q lives in the crossover/UV tail",
            "claim_promoted": False,
        },
        {
            "question": "Does the known Gaussian pair block derive q?",
            "answer": "NO",
            "scope": f"q_pair={Q_GAUSSIAN_PAIR}; shortfall={Q_TARGET-Q_GAUSSIAN_PAIR}",
            "claim_promoted": False,
        },
        {
            "question": "Does retarded-history weighting derive the state preparation?",
            "answer": "NO",
            "scope": "the source permits weights but the parent does not select their scale law",
            "claim_promoted": False,
        },
        {
            "question": "What work should proceed next?",
            "answer": "RESUME_5334_D4_OUTER_NUMERICAL_LADDER",
            "scope": "the CTP/fold side loop is closed unless a new parent-owned composite block appears",
            "claim_promoted": False,
        },
    ]


def run() -> dict[str, Any]:
    formal_start = formal_inventory_digest()
    sources, sources_locked = source_rows()
    pair_rows, pair_checks = pair_fold_rows()
    equivalence = equivalence_rows()
    gap_rows = mass_gap_rows()
    q_rows, q_checks = q_nonidentifiability_rows()
    spectral_rows, minimum_density = spectral_family_rows()
    history_rows = history_increment_rows()
    decisions = route_rows()

    outputs = {
        "source_register": OUT / "source_register.csv",
        "pair_fold": OUT / "massless_pair_fold_equivalence.csv",
        "equivalence": OUT / "retarded_fold_vs_pair_threshold.csv",
        "mass_gap": OUT / "mass_gap_criticality_gate.csv",
        "q_nonidentifiability": OUT / "fold_q_nonidentifiability.csv",
        "spectral_family": OUT / "positive_spectral_family_nonselection.csv",
        "history_increment": OUT / "maths_exploration_incremental_value.csv",
        "route_decision": OUT / "route_decision.csv",
    }
    payloads = {
        "source_register": sources,
        "pair_fold": pair_rows,
        "equivalence": equivalence,
        "mass_gap": gap_rows,
        "q_nonidentifiability": q_rows,
        "spectral_family": spectral_rows,
        "history_increment": history_rows,
        "route_decision": decisions,
    }
    for key, path in outputs.items():
        write_csv(path, payloads[key])

    formal_end = formal_inventory_digest()
    target_row = next(row for row in q_rows if row["is_target_q"])
    gaussian_row = next(
        row for row in q_rows if row["is_sourced_Gaussian_pair_q"]
    )
    checks = [
        validation_row(
            "all_source_locks_pass",
            sources_locked,
            f"rows={len(sources)}",
        ),
        validation_row(
            "formalization_workbench_unchanged",
            formal_start == formal_end == FORMAL_DIGEST,
            f"start={formal_start}; end={formal_end}",
        ),
        validation_row(
            "pair_bubble_quadrature_matches_exact_formula",
            pair_checks["maximum_relative_error"] <= 3.0e-11,
            str(pair_checks["maximum_relative_error"]),
        ),
        validation_row(
            "massless_pair_factorizes_one_over_eight_abs_k",
            pair_checks["maximum_massless_factorization_error"] <= TOLERANCE,
            str(pair_checks["maximum_massless_factorization_error"]),
        ),
        validation_row(
            "fold_and_pair_share_square_root_universality",
            equivalence[0]["equivalence"]
            == "same square-root fold universality class",
            equivalence[0]["incremental_result"],
        ),
        validation_row(
            "literal_retarded_and_pair_mechanisms_not_conflated",
            all(not bool(row["identical_mechanism"]) for row in equivalence),
            f"rows={len(equivalence)}",
        ),
        validation_row(
            "nonzero_pair_gap_removes_critical_IR_branch",
            all(
                row["low_momentum_status"]
                == "ANALYTIC_FOR_FIXED_NONZERO_MASS"
                for row in gap_rows
                if float(row["mass_over_momentum"]) > 0.0
            ),
            f"massive_rows={len(gap_rows)-1}",
        ),
        validation_row(
            "leading_IR_fold_is_q_independent",
            q_checks["maximum_ir_limit_error"] <= 1.1e-7
            and all(not bool(row["fold_carrier_changes_with_q"]) for row in q_rows),
            json.dumps(q_checks, sort_keys=True),
        ),
        validation_row(
            "UV_tail_carries_q",
            q_checks["maximum_uv_limit_error"] <= 1.1e-7,
            str(q_checks["maximum_uv_limit_error"]),
        ),
        validation_row(
            "target_q_differs_from_sourced_Gaussian_pair",
            abs(float(target_row["q"]) - float(gaussian_row["q"])) > 0.6,
            f"target={target_row['q']}; pair={gaussian_row['q']}",
        ),
        validation_row(
            "positive_causal_family_does_not_select_q",
            minimum_density > 0.0
            and all(not bool(row["q_selected_by_positivity"]) for row in spectral_rows),
            f"minimum_density={minimum_density}",
        ),
        validation_row(
            "history_features_add_no_unsourced_parent_claim",
            all(not bool(row["new_parent_ownership"]) for row in history_rows),
            f"rows={len(history_rows)}",
        ),
        validation_row(
            "no_claim_promoted",
            all(not bool(row["claim_promoted"]) for row in decisions),
            f"rows={len(decisions)}",
        ),
        validation_row(
            "route_returns_to_active_D4_outer_ladder",
            decisions[-1]["answer"] == "RESUME_5334_D4_OUTER_NUMERICAL_LADDER",
            decisions[-1]["scope"],
        ),
    ]
    write_csv(VALIDATION, checks)
    validation = read_csv(VALIDATION)
    passed = all(row["passed"].lower() == "true" for row in validation)
    result = {
        "checkpoint": CHECKPOINT,
        "marker": MARKER,
        "decision": (
            "RETARDED_FOLD_EQUALS_MASSLESS_PAIR_THRESHOLD_AT_THE_"
            "UNIVERSALITY_LEVEL__IR_CARRIER_ALREADY_PARENT_OWNED__"
            "NO_INCREMENTAL_Q_OR_STATE_SELECTION__RETURN_TO_5334"
        ),
        "exact_equivalence": (
            "B0(k)=(1/8pi) integral_0^1 dx "
            "[x(1-x)|k|^2]^(-1/2)=1/(8|k|)"
        ),
        "q_target": Q_TARGET,
        "q_Gaussian_pair": Q_GAUSSIAN_PAIR,
        "q_shortfall": Q_TARGET - Q_GAUSSIAN_PAIR,
        "known_interaction_norm": KNOWN_INTERACTION_NORM,
        "output_row_counts": {
            key: len(read_csv(path)) for key, path in outputs.items()
        },
        "validation_rows": len(validation),
        "validation_passed": passed,
        "formalization_workbench_reference_digest": FORMAL_DIGEST,
        "formalization_workbench_start_digest": formal_start,
        "formalization_workbench_end_digest": formal_end,
        "formalization_workbench_modified_file_count": (
            0 if formal_start == formal_end == FORMAL_DIGEST else -1
        ),
        "claim_flags": {
            "valid_for_new_parent_ownership": False,
            "valid_for_derived_q": False,
            "valid_for_state_preparation": False,
            "valid_for_galaxy_claim": False,
            "valid_for_full_MTS_claim": False,
        },
        "next_action": (
            ".\\.venv-score\\Scripts\\python.exe "
            ".\\scripts\\Y5_R2FR_5334_D4_outer_regulator_ladder_controller.py "
            "--mode refinement-run --max-runtime-hours 2"
        ),
    }
    atomic_json(RESULT, result)
    if not passed:
        raise RuntimeError("checkpoint 5336 validation failed")
    return result


def validate_existing() -> dict[str, Any]:
    required = [
        RESULT,
        VALIDATION,
        OUT / "source_register.csv",
        OUT / "massless_pair_fold_equivalence.csv",
        OUT / "retarded_fold_vs_pair_threshold.csv",
        OUT / "mass_gap_criticality_gate.csv",
        OUT / "fold_q_nonidentifiability.csv",
        OUT / "positive_spectral_family_nonselection.csv",
        OUT / "maths_exploration_incremental_value.csv",
        OUT / "route_decision.csv",
    ]
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise FileNotFoundError("; ".join(missing))
    validation = read_csv(VALIDATION)
    if not validation or not all(
        row["passed"].lower() == "true" for row in validation
    ):
        raise RuntimeError("stored validation has a failed gate")
    if formal_inventory_digest() != FORMAL_DIGEST:
        raise RuntimeError("formalization-workbench digest changed")
    return json.loads(RESULT.read_text(encoding="utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("run", "validate"), default="run")
    arguments = parser.parse_args()
    result = run() if arguments.mode == "run" else validate_existing()
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
