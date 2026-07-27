from __future__ import annotations

import csv
import math
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
MICROSCOPE = ROOT / "source-intake" / "microscope"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1559-Y5-qR-delta-beta-two-parameter-PPN-control-runner-and-zero-condition-hunt.md"
START_TS = datetime.now(timezone.utc).timestamp()

SOURCE_FILES = {
    "1558_doc": ROOT / "1558-Y5-qR-beta-matter-clock-coefficient-source-map-or-rejection.md",
    "1558_validation": OUT / "P8_Y5_BRR545_1558_VALIDATION.csv",
    "1558_next": OUT / "P8_Y5_PARENT_QLOC_1558_NEXT_TARGET.csv",
    "1558_coefficients": OUT / "P8_Y5_PARENT_QLOC_1558_PPN_COEFFICIENT_DERIVATION.csv",
    "1558_readiness": OUT / "P8_Y5_PARENT_QLOC_1558_COEFFICIENT_READINESS_MATRIX.csv",
    "1557_budget": OUT / "P8_Y5_PARENT_QLOC_1557_BOUND_BUDGET_NONCLAIM.csv",
    "14_doc": ROOT / "14-closure-deviation-PPN-sensitivity.md",
    "13_doc": ROOT / "13-local-closure-PPN-benchmark.md",
    "10_doc": ROOT / "10-observer-map-symplectic-contract.md",
    "local_bound_claims": LOCAL_BOUNDS / "local_bound_claims.csv",
}

NEEDLES = {
    "1558_doc": ["`q_R` now has a derived PPN translation", "not yet a local-GR derivation"],
    "1558_validation": ["VAL1558_OVERALL", "PASS"],
    "1558_next": ["1559-Y5-qR-delta-beta-two-parameter-PPN-control-runner"],
    "1558_coefficients": ["PPNC1558_0_qR_gamma", "PPNC1558_6_perihelion_degeneracy"],
    "1558_readiness": ["READY1558_0_qR_gamma", "TRANSLATION_ONLY"],
    "1557_budget": ["BUD1557_0_qR", "BUD1557_1_delta_beta"],
    "14_doc": ["Mercury shift factor = (2 q_R - delta_beta)/3."],
    "13_doc": ["R_AB approx q_R L", "gamma approx 1 + q_R."],
    "10_doc": ["derive R_AB=0 from the parent theory", "beta - 1 = 0"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1559_SOURCE_REGISTER.csv"
TWO_PARAMETER_MODEL = OUT / "P8_Y5_PARENT_QLOC_1559_TWO_PARAMETER_MODEL.csv"
PARAMETER_BOUNDS = OUT / "P8_Y5_PARENT_QLOC_1559_PARAMETER_BOUND_BOX_NONCLAIM.csv"
CONTROL_RUNNER = OUT / "P8_Y5_PARENT_QLOC_1559_TWO_PARAMETER_CONTROL_RUNNER_NONCLAIM.csv"
ZERO_CONDITIONS = OUT / "P8_Y5_PARENT_QLOC_1559_PARENT_ZERO_CONDITION_HUNT.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1559_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1559_DECISION.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1559_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1559_VALIDATION.csv"

QUARANTINE = MICROSCOPE / "quarantine" / "1559"
QUAR_MODEL = QUARANTINE / "TWO_PARAMETER_MODEL_NONCLAIM.csv"
QUAR_BOUNDS = QUARANTINE / "PARAMETER_BOUND_BOX_NONCLAIM.csv"
QUAR_RUNNER = QUARANTINE / "TWO_PARAMETER_CONTROL_RUNNER_NONCLAIM.csv"
QUAR_ZERO = QUARANTINE / "PARENT_ZERO_CONDITION_HUNT_NONCLAIM.csv"
QUAR_DECISION = QUARANTINE / "DECISION_NONCLAIM.csv"
BRANCH_MODEL = BRANCH_RESIDUALS / "two_parameter_model_nonclaim_1559.csv"
BRANCH_BOUNDS = BRANCH_RESIDUALS / "parameter_bound_box_nonclaim_1559.csv"
BRANCH_RUNNER = BRANCH_RESIDUALS / "two_parameter_control_runner_nonclaim_1559.csv"
BRANCH_ZERO = BRANCH_RESIDUALS / "parent_zero_condition_hunt_nonclaim_1559.csv"
BRANCH_DECISION = BRANCH_RESIDUALS / "two_parameter_decision_nonclaim_1559.csv"

THETA_GR_ARCSEC = 1.7512432813682448
SHAPIRO_GR_MICROSECONDS = 119.4750358485562
MERCURY_GR_ARCSEC_PER_CENTURY = 42.98201260912118


def flags() -> dict[str, bool]:
    return {
        "numeric_value_present": False,
        "source_backed": False,
        "score_ready": False,
        "valid_prediction_row": False,
        "valid_for_claim": False,
        "claim_allowed": False,
    }


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def source_list(*keys: str) -> str:
    return "; ".join(rel(SOURCE_FILES[key]) for key in keys)


def file_contains(path: Path, needles: list[str]) -> bool:
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8", errors="ignore")
    return all(needle in text for needle in needles)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def parse_csv(path: Path) -> bool:
    read_csv(path)
    return True


def generated_flags_false(paths: list[Path]) -> bool:
    false_values = {"", "false", "0", "no", "none", "null"}
    claim_keys = [
        "numeric_value_present",
        "source_backed",
        "score_ready",
        "valid_prediction_row",
        "valid_for_claim",
        "claim_allowed",
        "accepted_for_scoring",
        "passes_for_claim",
    ]
    for path in paths:
        for row in read_csv(path):
            for key in claim_keys:
                if key in row and str(row[key]).strip().lower() not in false_values:
                    return False
    return True


def local_bounds_by_row_id() -> dict[str, dict[str, str]]:
    return {row["row_id"]: row for row in read_csv(SOURCE_FILES["local_bound_claims"])}


def source_register_rows() -> list[dict[str, Any]]:
    rows = []
    for index, (key, path) in enumerate(SOURCE_FILES.items()):
        needles = NEEDLES.get(key, [])
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "source_id": f"SRC1559_{index}_{key}",
                "source_path": rel(path),
                "exists": path.exists(),
                "needle_found": file_contains(path, needles) if needles else True,
                "needles": "; ".join(needles),
                "purpose": "evidence for q_R/delta_beta two-parameter PPN control runner and parent zero-condition hunt",
                **flags(),
            }
        )
    return rows


def two_parameter_model_rows() -> list[dict[str, Any]]:
    q_light = THETA_GR_ARCSEC / 2.0
    q_shapiro = SHAPIRO_GR_MICROSECONDS / 2.0
    q_mercury = 2.0 * MERCURY_GR_ARCSEC_PER_CENTURY / 3.0
    beta_mercury = -MERCURY_GR_ARCSEC_PER_CENTURY / 3.0
    rows = [
        ("MODEL1559_0_gamma", "gamma_minus_1", "q_R", "1", "dimensionless", "linear PPN dictionary"),
        ("MODEL1559_1_beta", "beta_minus_1", "delta_beta", "1", "dimensionless", "definition of nonlinear beta drift"),
        ("MODEL1559_2_light", "solar_light_bending_residual_arcsec", "q_R", f"{q_light:.16g}", "arcsec", "theta_GR q_R/2"),
        ("MODEL1559_3_shapiro", "solar_Shapiro_residual_microseconds", "q_R", f"{q_shapiro:.16g}", "microseconds", "delay_GR q_R/2"),
        ("MODEL1559_4_mercury_qR", "Mercury_perihelion_residual_arcsec_per_century", "q_R", f"{q_mercury:.16g}", "arcsec/century", "GR_perihelion 2 q_R/3"),
        ("MODEL1559_5_mercury_beta", "Mercury_perihelion_residual_arcsec_per_century", "delta_beta", f"{beta_mercury:.16g}", "arcsec/century", "-GR_perihelion delta_beta/3"),
        ("MODEL1559_6_mercury_combo", "Mercury_perihelion_fractional_factor", "q_R; delta_beta", "(2 q_R - delta_beta)/3", "dimensionless", "perihelion degeneracy line"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "model_id": model_id,
            "observable_response": observable_response,
            "leak_parameter": leak_parameter,
            "coefficient": coefficient,
            "units": units,
            "derivation_note": derivation_note,
            "model_status": "PPN_TRANSLATION_CONTROL_NOT_MTS_PREDICTION",
            "source_paths": source_list("1558_coefficients", "14_doc", "13_doc", "10_doc"),
            **flags(),
        }
        for model_id, observable_response, leak_parameter, coefficient, units, derivation_note in rows
    ]


def parameter_bound_rows() -> list[dict[str, Any]]:
    bounds = local_bounds_by_row_id()
    gamma = bounds["R3_gamma"]
    beta = bounds["R4_beta"]
    rows = [
        (
            "BOX1559_0_qR",
            "q_R",
            "R3_gamma",
            gamma["measured_value"],
            gamma["one_sigma"],
            gamma["upper_bound"],
            gamma["units"],
            "q_R = gamma-1 in the PPN translation map",
            gamma["reference_path_or_url"],
        ),
        (
            "BOX1559_1_delta_beta",
            "delta_beta",
            "R4_beta",
            beta["measured_value"],
            beta["one_sigma"],
            beta["upper_bound"],
            beta["units"],
            "delta_beta = beta-1 by PPN parameter definition; beta row carries its original gamma-prior caveat",
            beta["reference_path_or_url"],
        ),
        (
            "BOX1559_2_perihelion_combo",
            "2 q_R - delta_beta",
            "R3_gamma; R4_beta",
            "not_independently_fit_here",
            "not_independently_fit_here",
            "derived_combination_only",
            "dimensionless",
            "perihelion constrains the combination through (2 q_R-delta_beta)/3, but no independent Mercury covariance is reconstructed here",
            f"{gamma['reference_path_or_url']}; {beta['reference_path_or_url']}",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "bound_id": bound_id,
            "parameter_or_combo": parameter_or_combo,
            "local_bound_rows": local_bound_rows,
            "measured_or_central": measured_or_central,
            "one_sigma": one_sigma,
            "control_bound": control_bound,
            "units": units,
            "interpretation": interpretation,
            "reference_path_or_url": reference_path_or_url,
            "bound_status": "CONTROL_CONSTRAINT_NOT_PARENT_PREDICTION",
            "source_paths": source_list("local_bound_claims", "1558_coefficients"),
            **flags(),
        }
        for (
            bound_id,
            parameter_or_combo,
            local_bound_rows,
            measured_or_central,
            one_sigma,
            control_bound,
            units,
            interpretation,
            reference_path_or_url,
        ) in rows
    ]


def evaluate_control_case(case_id: str, label: str, q_r: float, delta_beta: float, purpose: str) -> dict[str, Any]:
    bounds = local_bounds_by_row_id()
    q_bound = float(bounds["R3_gamma"]["upper_bound"])
    beta_bound = float(bounds["R4_beta"]["upper_bound"])
    gamma_minus_1 = q_r
    beta_minus_1 = delta_beta
    light = THETA_GR_ARCSEC * q_r / 2.0
    shapiro = SHAPIRO_GR_MICROSECONDS * q_r / 2.0
    mercury = MERCURY_GR_ARCSEC_PER_CENTURY * (2.0 * q_r - delta_beta) / 3.0
    q_pass = abs(q_r) <= q_bound
    beta_pass = abs(delta_beta) <= beta_bound
    return {
        "same_parent_branch_id": BRANCH_ID,
        "case_id": case_id,
        "label": label,
        "q_R_input": f"{q_r:.12g}",
        "delta_beta_input": f"{delta_beta:.12g}",
        "gamma_minus_1": f"{gamma_minus_1:.12g}",
        "beta_minus_1": f"{beta_minus_1:.12g}",
        "light_bending_residual_arcsec": f"{light:.12g}",
        "shapiro_residual_microseconds": f"{shapiro:.12g}",
        "mercury_residual_arcsec_per_century": f"{mercury:.12g}",
        "q_R_bound_pass": q_pass,
        "delta_beta_bound_pass": beta_pass,
        "control_status": "PASS_CONTROL_BOX" if q_pass and beta_pass else "FAIL_CONTROL_BOX",
        "purpose": purpose,
        "source_paths": source_list("1558_coefficients", "local_bound_claims"),
        **flags(),
    }


def control_runner_rows() -> list[dict[str, Any]]:
    return [
        evaluate_control_case("CASE1559_0_GR_origin", "GR/null closure origin", 0.0, 0.0, "baseline origin of q_R/delta_beta plane"),
        evaluate_control_case("CASE1559_1_Cassini_q_edge", "positive q_R bound edge", 2.3e-5, 0.0, "Cassini gamma-edge control point"),
        evaluate_control_case("CASE1559_2_beta_edge", "positive delta_beta bound edge", 0.0, 7.8e-5, "beta edge control point"),
        evaluate_control_case("CASE1559_3_perihelion_degeneracy", "perihelion degeneracy line", 2.0e-5, 4.0e-5, "2 q_R - delta_beta = 0 while gamma/beta bounds still matter"),
        evaluate_control_case("CASE1559_4_q_fail", "q_R too large", 5.0e-5, 0.0, "shows Cassini/gamma clamp"),
        evaluate_control_case("CASE1559_5_beta_fail", "delta_beta too large", 0.0, 1.2e-4, "shows beta clamp"),
    ]


def zero_condition_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "ZERO1559_0_qR_linear",
            "q_R=0",
            "parent equations must force R_AB=O(L^2), not R_AB=q_R L",
            "linear reciprocal strain coefficient vanishes",
            "MISSING_PARENT_FIELD_EQUATION",
            "derive first-order observer-sector equation whose regular/local-vacuum solution has T^2 S=1+O(L^2)",
        ),
        (
            "ZERO1559_1_qR_charge",
            "q_R=0",
            "no reciprocal boundary/current charge may source R_AB at O(L)",
            "Q_R local charge is zero or pure gauge with proper boundary term",
            "MISSING_ZERO_CHARGE_THEOREM",
            "supply first-class constraint/no-boundary-charge proof rather than closure axiom",
        ),
        (
            "ZERO1559_2_qR_matter",
            "q_R observed by matter",
            "matter and photons must read the same T,S coframe, otherwise gamma translation is not universal",
            "universal coframe descent",
            "MISSING_MATTER_DESCENT",
            "derive matter action descent through the same observer map",
        ),
        (
            "ZERO1559_3_beta_second_order",
            "delta_beta=0",
            "second-order weak-field completion must match beta=1 in a valid PPN gauge",
            "nonlinear source self-coupling equals GR control lane",
            "MISSING_SECOND_ORDER_PARENT_COMPLETION",
            "derive O(U^2) metric/coframe field equation and coordinate/gauge map",
        ),
        (
            "ZERO1559_4_beta_conservation",
            "delta_beta=0",
            "Bianchi/conservation identity must fix the nonlinear potential terms consistently",
            "local conservation closes source normalization and beta completion",
            "MISSING_BIANCHI_SOURCE_IDENTITY",
            "derive the parent identity linking field equations to matter conservation",
        ),
        (
            "ZERO1559_5_no_extra_modes",
            "q_R=0 and delta_beta=0",
            "extra finite-range/scalar/tracefree modes must decouple or be suppressed locally",
            "no surviving local hair in the PPN residual vector",
            "MISSING_MODE_DECOUPLING_THEOREM",
            "derive decoupling/suppression or keep local branch as bounded closure",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "zero_id": zero_id,
            "target_zero": target_zero,
            "required_statement": required_statement,
            "mathematical_content": mathematical_content,
            "status": status,
            "next_derivation_step": next_derivation_step,
            "source_paths": source_list("10_doc", "13_doc", "1558_coefficients"),
            **flags(),
        }
        for zero_id, target_zero, required_statement, mathematical_content, status, next_derivation_step in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("GATE1559_0_control_runner", "two-parameter PPN control runner", "PASS_NONCLAIM_CONTROL", "control-plane arithmetic works and can reject trial leak vectors"),
        ("GATE1559_1_parent_prediction", "MTS predicts q_R and delta_beta", "BLOCKED_NO_CLAIM", "no parent equations produce q_R/delta_beta values"),
        ("GATE1559_2_GR_origin", "MTS derives local GR origin q_R=0, delta_beta=0", "BLOCKED_NO_CLAIM", "zero-condition ledger remains unsigned"),
        ("GATE1559_3_matter_universal", "local bounds apply to all matter/photons", "BLOCKED_NO_CLAIM", "matter/coframe descent still missing"),
        ("GATE1559_4_empirical_score", "empirical MTS local-bound score", "BLOCKED_NO_CLAIM", "runner can score hypothetical vectors, not the theory"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "claim_gate": claim_gate,
            "status": status,
            "reason": reason,
            "source_paths": source_list("1558_coefficients", "local_bound_claims", "10_doc", "13_doc"),
            **flags(),
        }
        for gate_id, claim_gate, status, reason in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1559_0_verdict",
            "decision": "two-parameter local control status",
            "result": "CONTROL_RUNNER_READY_ZERO_THEOREM_MISSING",
            "reason": "q_R/delta_beta local residuals are now test-shaped, but the parent theory has not derived the GR origin",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1559_1_next",
            "decision": "next target",
            "result": "NEXT_1560_PARENT_WEAK_FIELD_ZERO_CONDITION_DERIVATION",
            "reason": "the best next route is to attack the parent equations needed for q_R=0 and delta_beta=0",
            **flags(),
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "next_id": "NEXT1559_0_1560",
            "next_target": "1560-Y5-parent-weak-field-zero-condition-derivation-or-demotion.md",
            "script": "scripts/Y5_parent_weak_field_zero_condition_derivation_or_demotion.py",
            "objective": "attempt to derive the first-order q_R=0 condition and second-order delta_beta=0 condition from a parent weak-field field-equation/action structure; if this fails, demote the local GR branch to an explicit bounded-closure control lane",
            "do_not": "do not use the PPN control runner as a parent derivation; do not claim local GR/Newton reduction; do not edit formalization-workbench",
            **flags(),
        }
    ]


def copy_outputs() -> None:
    copies = [
        (TWO_PARAMETER_MODEL, QUAR_MODEL),
        (PARAMETER_BOUNDS, QUAR_BOUNDS),
        (CONTROL_RUNNER, QUAR_RUNNER),
        (ZERO_CONDITIONS, QUAR_ZERO),
        (DECISION, QUAR_DECISION),
        (TWO_PARAMETER_MODEL, BRANCH_MODEL),
        (PARAMETER_BOUNDS, BRANCH_BOUNDS),
        (CONTROL_RUNNER, BRANCH_RUNNER),
        (ZERO_CONDITIONS, BRANCH_ZERO),
        (DECISION, BRANCH_DECISION),
    ]
    for source, destination in copies:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def formalization_modified_count_since_start() -> int:
    if not FORMALIZATION.exists():
        return 0
    return sum(1 for path in FORMALIZATION.rglob("*") if path.is_file() and path.stat().st_mtime >= START_TS)


def validation_rows(generated_csvs: list[Path]) -> list[dict[str, Any]]:
    sources = read_csv(SOURCE_REGISTER)
    model = read_csv(TWO_PARAMETER_MODEL)
    bounds = read_csv(PARAMETER_BOUNDS)
    runner = read_csv(CONTROL_RUNNER)
    zero = read_csv(ZERO_CONDITIONS)
    gate_rows = read_csv(CLAIM_GATE)
    decision_items = read_csv(DECISION)
    next_rows = read_csv(NEXT_TARGET)

    gr_case = next(row for row in runner if row["case_id"] == "CASE1559_0_GR_origin")
    q_fail = next(row for row in runner if row["case_id"] == "CASE1559_4_q_fail")
    degeneracy = next(row for row in runner if row["case_id"] == "CASE1559_3_perihelion_degeneracy")
    q_model = next(row for row in model if row["model_id"] == "MODEL1559_0_gamma")
    beta_model = next(row for row in model if row["model_id"] == "MODEL1559_1_beta")

    checks = [
        ("VAL1559_0_sources_exist", all(row["exists"] == "True" for row in sources), "all cited 1559 source paths exist"),
        ("VAL1559_1_needles_found", all(row["needle_found"] == "True" for row in sources), "all registered evidence needles found"),
        ("VAL1559_2_model_q_beta", q_model["coefficient"] == "1" and beta_model["coefficient"] == "1", "q_R and delta_beta unit translation rows present"),
        ("VAL1559_3_model_perihelion_combo", any(row["model_id"] == "MODEL1559_6_mercury_combo" and "2 q_R - delta_beta" in row["coefficient"] for row in model), "perihelion degeneracy model present"),
        ("VAL1559_4_bound_box", len(bounds) >= 3 and any(row["bound_id"] == "BOX1559_0_qR" and row["control_bound"] == "2.3e-05" for row in bounds), "q_R and delta_beta bound box written"),
        ("VAL1559_5_GR_origin_passes", gr_case["control_status"] == "PASS_CONTROL_BOX" and gr_case["gamma_minus_1"] == "0", "GR origin passes control box"),
        ("VAL1559_6_q_fail_fails", q_fail["control_status"] == "FAIL_CONTROL_BOX" and q_fail["q_R_bound_pass"] == "False", "oversized q_R fails Cassini/gamma bound"),
        ("VAL1559_7_degeneracy_line", math.isclose(float(degeneracy["mercury_residual_arcsec_per_century"]), 0.0, rel_tol=0, abs_tol=1e-12), "perihelion degeneracy example has zero Mercury residual"),
        ("VAL1559_8_zero_conditions", len(zero) >= 6 and any(row["zero_id"] == "ZERO1559_3_beta_second_order" for row in zero), "parent zero-condition hunt ledger written"),
        ("VAL1559_9_claim_gates", any(row["gate_id"] == "GATE1559_2_GR_origin" and row["status"] == "BLOCKED_NO_CLAIM" for row in gate_rows), "local GR derivation remains blocked"),
        ("VAL1559_10_decision_next", any(row["result"] == "NEXT_1560_PARENT_WEAK_FIELD_ZERO_CONDITION_DERIVATION" for row in decision_items), "decision selects parent weak-field zero-condition derivation next"),
        ("VAL1559_11_next_target", any("1560-Y5-parent-weak-field-zero-condition" in row["next_target"] for row in next_rows), "next target is parent weak-field zero-condition derivation or demotion"),
        ("VAL1559_12_csv_parse", all(parse_csv(path) for path in generated_csvs), "all generated 1559 CSVs parse cleanly"),
        ("VAL1559_13_claim_flags_false", generated_flags_false(generated_csvs), "all generated prediction/claim flags remain false"),
        ("VAL1559_14_branch_copies", all(path.exists() for path in [QUAR_MODEL, QUAR_BOUNDS, QUAR_RUNNER, QUAR_ZERO, QUAR_DECISION, BRANCH_MODEL, BRANCH_BOUNDS, BRANCH_RUNNER, BRANCH_ZERO, BRANCH_DECISION]), "branch/quarantine nonclaim copies written"),
        ("VAL1559_15_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent after run"),
        ("VAL1559_16_formalization_untouched", formalization_modified_count_since_start() == 0, "formalization modified-file count since start=0"),
    ]
    overall = all(result for _, result, _ in checks)
    rows = [
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail,
        }
        for check_id, result, detail in checks
    ]
    rows.append(
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": "VAL1559_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1559 q_R/delta_beta two-parameter PPN control runner and zero-condition hunt validation",
        }
    )
    return rows


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |")
    return "\n".join([header, sep, *body])


def write_doc(
    sources: list[dict[str, Any]],
    model: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    zero: list[dict[str, Any]],
    gate_rows: list[dict[str, Any]],
    decision_items: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n".join(
            [
                "# 1559 - q_R/delta_beta Two-Parameter PPN Control Runner and Zero-Condition Hunt",
                "",
                "## Verdict",
                "- The `q_R/delta_beta` local branch now has a two-parameter PPN control runner.",
                "- `q_R` is clamped by the Cassini/gamma row through `gamma-1=q_R`; `delta_beta` is clamped by the beta row through `beta-1=delta_beta`.",
                "- Mercury perihelion exposes the degeneracy line `(2 q_R-delta_beta)/3`, so it cannot by itself separate spatial reciprocal hair from nonlinear beta drift.",
                "- The runner can reject hypothetical leak vectors, but it still cannot score MTS as a prediction because the parent action has not produced the vector.",
                "- The next honest target is the parent weak-field zero-condition derivation: prove `q_R=0` and `delta_beta=0`, or demote local GR to bounded closure.",
                "",
                "## Source Register",
                md_table(sources, ["source_id", "source_path", "exists", "needle_found", "needles"]),
                "",
                "## Two-Parameter Model",
                md_table(model, ["model_id", "observable_response", "leak_parameter", "coefficient", "units", "model_status"]),
                "",
                "## Parameter Bound Box",
                md_table(bounds, ["bound_id", "parameter_or_combo", "local_bound_rows", "measured_or_central", "one_sigma", "control_bound", "interpretation"]),
                "",
                "## Control Runner",
                md_table(runner, ["case_id", "label", "q_R_input", "delta_beta_input", "gamma_minus_1", "beta_minus_1", "mercury_residual_arcsec_per_century", "control_status", "purpose"]),
                "",
                "## Parent Zero-Condition Hunt",
                md_table(zero, ["zero_id", "target_zero", "required_statement", "mathematical_content", "status", "next_derivation_step"]),
                "",
                "## Claim Gates",
                md_table(gate_rows, ["gate_id", "claim_gate", "status", "reason"]),
                "",
                "## Decision",
                md_table(decision_items, ["decision_id", "decision", "result", "reason"]),
                "",
                "## Validation",
                md_table(validation, ["check_id", "result", "detail"]),
                "",
                "## Next Target",
                md_table(next_rows, ["next_target", "script", "objective", "do_not"]),
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> None:
    sources = source_register_rows()
    model = two_parameter_model_rows()
    bounds = parameter_bound_rows()
    runner = control_runner_rows()
    zero = zero_condition_rows()
    gate_rows = claim_gate_rows()
    decision_items = decision_rows()
    next_rows = next_target_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(TWO_PARAMETER_MODEL, model)
    write_csv(PARAMETER_BOUNDS, bounds)
    write_csv(CONTROL_RUNNER, runner)
    write_csv(ZERO_CONDITIONS, zero)
    write_csv(CLAIM_GATE, gate_rows)
    write_csv(DECISION, decision_items)
    write_csv(NEXT_TARGET, next_rows)
    copy_outputs()
    remove_pycache()

    generated_csvs = [
        SOURCE_REGISTER,
        TWO_PARAMETER_MODEL,
        PARAMETER_BOUNDS,
        CONTROL_RUNNER,
        ZERO_CONDITIONS,
        CLAIM_GATE,
        DECISION,
        NEXT_TARGET,
    ]
    validation = validation_rows(generated_csvs)
    write_csv(VALIDATION, validation)
    write_doc(sources, model, bounds, runner, zero, gate_rows, decision_items, validation, next_rows)


if __name__ == "__main__":
    main()
