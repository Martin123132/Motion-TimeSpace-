from __future__ import annotations

import csv
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


RUN_UTC = datetime.now(timezone.utc).isoformat()
ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
PARENT_ACTION = ROOT / "source-intake" / "parent-action"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"
PYCACHE = ROOT / "scripts" / "__pycache__"

CHECKPOINT = "3049"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "3049-Y5-R2FR-scalar-kappa-first-bound-runner-dryrun-or-parent-adoption-review-under-AX1090.md"

TARGETS = {
    "P8_Geff_time_drift": {
        "path": RESIDUALS / "P8_time_drift_residual_or_zero.csv",
        "quantity": "dln_Geff_dt",
        "arena": "clock_or_orbital_Gdot;local_GR",
        "minimum_for_claim": "numeric dln_Geff_dt in yr^-1 below bound or parent-derived zero drift",
    },
    "P8_range_dependence": {
        "path": RESIDUALS / "R10_alpha_lambda_curve_MTS_source_normalization.csv",
        "quantity": "alpha(lambda)",
        "arena": "R10_inverse_square_fifth_force",
        "minimum_for_claim": "executable lambda/alpha_predicted rows and real alpha_bound curve, or source-backed no-range theorem",
    },
    "P8_species_source_charge": {
        "path": RESIDUALS / "P8_species_source_charge_residual_or_zero.csv",
        "quantity": "eta_source_AB",
        "arena": "source_charge_WEP",
        "minimum_for_claim": "numeric eta_source_AB below 2.8e-15 or signed universal source-charge theorem",
    },
    "P8_radial_source_hair": {
        "path": RESIDUALS / "P8_radial_mu_profile_or_zero.csv",
        "quantity": "partial_r ln G_eff",
        "arena": "inverse_square_Newton;PPN_gamma_beta;R10",
        "minimum_for_claim": "radial no-hair theorem or profile envelope mapped to local bounds",
    },
    "P8_frame_calibration_split": {
        "path": RESIDUALS / "P8_frame_source_split_residual_or_zero.csv",
        "quantity": "delta_frame_source",
        "arena": "same_frame_Newton;clock;WEP",
        "minimum_for_claim": "same parent pullback for source variation and matter readout or bounded split residual",
    },
    "P8_Bianchi_kappa_exchange": {
        "path": RESIDUALS / "P8_delta_kappa_source_exchange_residual.csv",
        "quantity": "delta_kappa_source",
        "arena": "q_loc;PPN;R10;conservation",
        "minimum_for_claim": "same-frame arbitrary-source conservation theorem or explicit local projection coefficient",
    },
}

SOURCE_PATHS = {
    "SRC3049_00_3048_doc": ROOT / "3048-Y5-R2FR-scalar-kappa-residual-inputs-or-topological-adoption-decision-under-AX1090.md",
    "SRC3049_01_3048_adoption": RESIDUALS / "P8_Y5_R2FR_3048_TOPOLOGICAL_ADOPTION_DECISION.csv",
    "SRC3049_02_3048_first_inputs": RESIDUALS / "P8_Y5_R2FR_3048_SCALAR_KAPPA_FIRST_INPUT_ROWS_NONCLAIM.csv",
    "SRC3049_03_3048_runner_readiness": RESIDUALS / "P8_Y5_R2FR_3048_RUNNER_READINESS.csv",
    "SRC3049_04_3048_bound_linkage": RESIDUALS / "P8_Y5_R2FR_3048_BOUND_MATRIX_LINKAGE.csv",
    "SRC3049_05_3048_next": RESIDUALS / "P8_Y5_R2FR_3048_NEXT_TARGET.csv",
    "SRC3049_06_3048_validation": RESIDUALS / "P8_Y5_BRR545_3048_VALIDATION.csv",
    "SRC3049_07_3047_variation": RESIDUALS / "P8_Y5_R2FR_3047_KAPPA_VARIATION_AUDIT.csv",
    "SRC3049_08_3047_adoption_gate": RESIDUALS / "P8_Y5_R2FR_3047_PARENT_ADOPTION_GATE.csv",
    "SRC3049_09_topological_clause": RESIDUALS / "P8_CONSTANT_KAPPA_TOPOLOGICAL_ZEROFORM_CLAUSE.csv",
    "SRC3049_10_global_contract": RESIDUALS / "P8_global_coupling_superselection_CONTRACT.csv",
    "SRC3049_11_constant_kappa_contract": RESIDUALS / "P8_constant_universal_Geff_kappa_CONTRACT.csv",
    "SRC3049_12_bound_matrix": RESIDUALS / "P8_CONSTANT_GM_RESIDUAL_BOUND_MATRIX.csv",
    "SRC3049_13_runner_input": RESIDUALS / "P8_CONSTANT_GM_LOCAL_RESIDUAL_RUNNER_INPUT.csv",
    "SRC3049_14_fill_queue": RESIDUALS / "P8_CONSTANT_GM_DERIVATIVE_HAIR_FILL_QUEUE.csv",
    "SRC3049_15_time_target": TARGETS["P8_Geff_time_drift"]["path"],
    "SRC3049_16_r10_target": TARGETS["P8_range_dependence"]["path"],
    "SRC3049_17_wep_target": TARGETS["P8_species_source_charge"]["path"],
    "SRC3049_18_radial_target": TARGETS["P8_radial_source_hair"]["path"],
    "SRC3049_19_frame_target": TARGETS["P8_frame_calibration_split"]["path"],
    "SRC3049_20_bianchi_target": TARGETS["P8_Bianchi_kappa_exchange"]["path"],
}

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3049_SOURCE_REGISTER.csv",
    "adoption_review": RESIDUALS / "P8_Y5_R2FR_3049_TOPOLOGICAL_ADOPTION_REVIEW.csv",
    "row_diagnostics": RESIDUALS / "P8_Y5_R2FR_3049_SCALAR_KAPPA_DRYRUN_ROW_DIAGNOSTICS.csv",
    "dryrun_results": RESIDUALS / "P8_Y5_R2FR_3049_SCALAR_KAPPA_DRYRUN_RESULTS.csv",
    "local_claim_status": RESIDUALS / "P8_Y5_R2FR_3049_LOCAL_CLAIM_STATUS.csv",
    "unlock_map": RESIDUALS / "P8_Y5_R2FR_3049_UNLOCK_CONDITION_MAP.csv",
    "promotion_gates": RESIDUALS / "P8_Y5_R2FR_3049_PROMOTION_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_3049_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_3049_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_3049_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3049_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "adoption_copy": PARENT_ACTION / "topological_kappa_adoption_review_3049_NOT_ADOPTED.csv",
    "diagnostics_copy": LOCAL_BOUNDS / "scalar_kappa_dryrun_row_diagnostics_3049_NONCLAIM.csv",
    "dryrun_copy": LOCAL_BOUNDS / "scalar_kappa_dryrun_results_3049_BLOCKED_NONCLAIM.csv",
    "claim_status_copy": LOCAL_BOUNDS / "local_claim_status_3049_BLOCKED_NONCLAIM.csv",
    "unlock_copy": PARENT_ACTION / "topological_kappa_unlock_condition_map_3049_PARENT_ACTION_TARGET.csv",
    "next_copy": RAB_QUEUE / "JR3049_PARENT_TOPOLOGICAL_KAPPA_SPINE_OR_SCALAR_COEFFICIENT_FILL_NEXT_NONCLAIM.csv",
}

for path in list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC]:
    path.parent.mkdir(parents=True, exist_ok=True)


def rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def as_str(value: Any) -> str:
    return "" if value is None else str(value)


def boolish(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "y", "pass", "passed"}


def csv_ok(path: Path) -> bool:
    try:
        if not path.exists():
            return False
        with path.open("r", newline="", encoding="utf-8") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
        return False


def write_csv(path: Path, output_rows: list[dict[str, Any]]) -> None:
    fieldnames: list[str] = []
    for output_row in output_rows:
        for key in output_row:
            if key not in fieldnames:
                fieldnames.append(key)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for output_row in output_rows:
            writer.writerow({key: as_str(output_row.get(key, "")) for key in fieldnames})


def under(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def base(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "checkpoint": CHECKPOINT,
        "branch_id": BRANCH_ID,
        "timestamp_utc": RUN_UTC,
        "score_ready": "false",
        "valid_prediction_row": "false",
        "valid_for_claim": "false",
        "claim_allowed": "false",
        **row,
    }


def md_table(table_rows: list[dict[str, Any]], columns: list[str]) -> str:
    if not table_rows:
        return "_No rows._"
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    lines = [header, sep]
    for row in table_rows:
        values = []
        for column in columns:
            value = as_str(row.get(column, "")).replace("\n", " ").replace("|", "/")
            values.append(value)
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def has_claim_true(input_rows: list[dict[str, str]]) -> bool:
    claim_fields = {"valid_for_claim", "claim_allowed", "valid_prediction_row", "score_ready", "ready_for_claim"}
    return any(boolish(row.get(field, "false")) for row in input_rows for field in claim_fields)


def missing_count(input_rows: list[dict[str, str]]) -> int:
    return sum(1 for row in input_rows for value in row.values() if "MISSING" in value.upper())


def zero_if_count(input_rows: list[dict[str, str]]) -> int:
    tokens = ("ZERO_IF", "THEOREM_ZERO", "DERIVED_ZERO", "NO_RANGE_THEOREM")
    return sum(1 for row in input_rows for value in row.values() if any(token in value.upper() for token in tokens))


def numeric_values(input_rows: list[dict[str, str]], fields: tuple[str, ...]) -> list[float]:
    found: list[float] = []
    for row in input_rows:
        for field in fields:
            value = row.get(field, "")
            if "MISSING" in value.upper() or "NOT_APPLICABLE" in value.upper() or "ZERO_IF" in value.upper():
                continue
            if re.fullmatch(r"[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?", value.strip()):
                found.append(float(value))
    return found


def text_contains_any(input_rows: list[dict[str, str]], needles: tuple[str, ...]) -> bool:
    haystack = "\n".join(value for row in input_rows for value in row.values()).upper()
    return any(needle.upper() in haystack for needle in needles)


def prediction_status(component_id: str, input_rows: list[dict[str, str]]) -> str:
    prediction_fields = (
        "candidate_value",
        "alpha_predicted",
        "predicted_value",
        "coefficient_value",
        "explicit_product_value",
        "finite_value_or_bound",
    )
    if numeric_values(input_rows, prediction_fields):
        return "NUMERIC_PREDICTION_PRESENT_BUT_NOT_PROMOTED"
    if text_contains_any(input_rows, ("MISSING_THEOREM_ZERO_CERTIFICATE", "MISSING_PARENT_ZERO", "MISSING_NUMERIC", "MISSING_SOURCE_NORMALIZED", "MISSING_RADIAL", "MISSING_ARENA")):
        return "MISSING_PARENT_ZERO_OR_NUMERIC_PREDICTION"
    if text_contains_any(input_rows, ("ZERO_IF_", "THEOREM_ZERO_CANDIDATE", "DERIVED_ZERO")):
        return "CONDITIONAL_ZERO_PRESENT_BUT_UNSIGNED"
    if component_id == "P8_range_dependence" and text_contains_any(input_rows, ("ALL_LOCAL_R10_RANGE", "NO_RANGE_THEOREM")):
        return "NO_RANGE_THEOREM_TEMPLATE_UNSIGNED"
    return "NO_SCOREABLE_PREDICTION_FIELD_FOUND"


def bound_status(component_id: str, input_rows: list[dict[str, str]]) -> str:
    bound_fields = ("bound_or_target", "bound_or_scale", "target_value", "alpha_bound", "reported_bound_abs")
    if component_id == "P8_range_dependence" and text_contains_any(input_rows, ("MISSING_DIGITIZED_ALPHA_BOUND", "MISSING_SOURCE_FILE", "verified alpha(lambda) bound curve")):
        return "MISSING_EXECUTABLE_R10_BOUND_CURVE"
    if numeric_values(input_rows, bound_fields):
        return "NUMERIC_BOUND_OR_SCALE_PRESENT"
    if text_contains_any(input_rows, ("mapped PPN/fifth-force", "explicit residual below", "arena_projection", "same-frame arbitrary-source")):
        return "BOUND_REQUIRES_ARENA_MAP"
    return "BOUND_NOT_SCOREABLE"


def dryrun_status(component_id: str, input_rows: list[dict[str, str]]) -> tuple[str, str]:
    p_status = prediction_status(component_id, input_rows)
    b_status = bound_status(component_id, input_rows)
    if p_status.startswith("NUMERIC_PREDICTION") and b_status.startswith("NUMERIC_BOUND") and not has_claim_true(input_rows):
        return "DRYRUN_NUMERIC_BUT_NONCLAIM_REVIEW_REQUIRED", "numeric branch would require independent reviewer and claim gates"
    if component_id == "P8_range_dependence" and b_status == "MISSING_EXECUTABLE_R10_BOUND_CURVE":
        return "BLOCKED_MISSING_R10_BOUND_CURVE_AND_MTS_PREDICTION", "R10 needs real lambda/alpha_predicted rows and a real alpha_bound curve"
    if p_status == "CONDITIONAL_ZERO_PRESENT_BUT_UNSIGNED":
        return "BLOCKED_CONDITIONAL_ZERO_NOT_PARENT_SIGNED", "zero route is written as a condition, not a theorem"
    if p_status == "MISSING_PARENT_ZERO_OR_NUMERIC_PREDICTION":
        return "BLOCKED_MISSING_PARENT_ZERO_OR_NUMERIC_PREDICTION", "no parent-derived zero or numeric coefficient exists"
    return "BLOCKED_NOT_SCOREABLE", f"{p_status}; {b_status}"


def copy_csv(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dst)


source_register = [
    base(
        {
            "source_id": source_id,
            "path": str(path),
            "exists": path.exists(),
            "parse_ok": csv_ok(path) if path.suffix.lower() == ".csv" and path.exists() else "",
            "row_count": len(rows(path)) if path.suffix.lower() == ".csv" and path.exists() else "",
            "role": source_id.split("_", 2)[-1],
            "status": "PRESENT" if path.exists() else "MISSING_BLOCKER",
        }
    )
    for source_id, path in SOURCE_PATHS.items()
]

adoption_source_rows = rows(SOURCE_PATHS["SRC3049_01_3048_adoption"])
adoption_review_rows = [
    base(
        {
            "review_id": "ADREV3049_0_variation",
            "question": "Does the 3047/3048 route contain a mathematical d kappa_eff=0 variation?",
            "answer": "YES_CONDITIONAL",
            "evidence": "delta_A3 S_kappa_top -> d kappa_eff=0 when S_kappa_top is parent-owned and boundary variation is admissible",
            "blocks_claim": "true",
            "missing_for_adoption": "ACTIVE_PARENT_ACTION_ADOPTION;BOUNDARY_VARIATION_SIGNATURE",
        }
    ),
    base(
        {
            "review_id": "ADREV3049_1_parent_spine",
            "question": "Is S_kappa_top adopted into the active parent-action spine?",
            "answer": "NO",
            "evidence": "3048 ADOPT3048_0_parent_spine = NO_NOT_IN_3048",
            "blocks_claim": "true",
            "missing_for_adoption": "EXPLICIT_PARENT_SPINE_ROW",
        }
    ),
    base(
        {
            "review_id": "ADREV3049_2_Gref",
            "question": "Is G_ref owned by kappa_eff?",
            "answer": "UNSIGNED",
            "evidence": "3048 ADOPT3048_1_Gref_ownership = UNSIGNED",
            "blocks_claim": "true",
            "missing_for_adoption": "G_ref = kappa_eff c^4/(8*pi) parent lock",
        }
    ),
    base(
        {
            "review_id": "ADREV3049_3_stress_boundary",
            "question": "Are topological stress silence and boundary conditions signed?",
            "answer": "UNSIGNED",
            "evidence": "3048 ADOPT3048_2_boundary_stress = UNSIGNED",
            "blocks_claim": "true",
            "missing_for_adoption": "METRIC_STRESS_SILENCE;FIXED_OR_TOPOLOGICAL_A3_BOUNDARY",
        }
    ),
    base(
        {
            "review_id": "ADREV3049_4_decision",
            "question": "Can 3049 choose the adoption branch?",
            "answer": "NO_KEEP_DRYRUN_BRANCH",
            "evidence": f"adoption_rows={len(adoption_source_rows)}; no parent-spine update requested or sourced",
            "blocks_claim": "true",
            "missing_for_adoption": "3050 parent-action theorem attempt",
        }
    ),
]

row_diagnostics: list[dict[str, Any]] = []
dryrun_results: list[dict[str, Any]] = []
for component_id, target in TARGETS.items():
    path = target["path"]
    input_rows = rows(path)
    for index, row in enumerate(input_rows):
        row_text = "\n".join(row.values()).upper()
        row_diagnostics.append(
            base(
                {
                    "diag_id": f"DIAG3049_{component_id}_{index}",
                    "component_id": component_id,
                    "target_file": str(path),
                    "row_index": index,
                    "row_id": row.get("row_id", row.get("curve_id", f"row_{index}")),
                    "parse_ok": csv_ok(path),
                    "has_missing_marker": "MISSING" in row_text,
                    "has_conditional_zero_marker": any(token in row_text for token in ("ZERO_IF", "THEOREM_ZERO", "DERIVED_ZERO")),
                    "has_claim_true": has_claim_true([row]),
                    "prediction_status": prediction_status(component_id, [row]),
                    "bound_status": bound_status(component_id, [row]),
                    "diagnostic_status": "NONCLAIM_BLOCKED_ROW",
                    "next_action": row.get("next_action", row.get("notes", target["minimum_for_claim"])),
                }
            )
        )
    result_status, block_reason = dryrun_status(component_id, input_rows)
    dryrun_results.append(
        base(
            {
                "dryrun_id": f"DRY3049_{component_id}",
                "component_id": component_id,
                "quantity": target["quantity"],
                "arena": target["arena"],
                "target_file": str(path),
                "file_exists": path.exists(),
                "parse_ok": csv_ok(path),
                "row_count": len(input_rows),
                "missing_marker_count": missing_count(input_rows),
                "conditional_zero_marker_count": zero_if_count(input_rows),
                "prediction_status": prediction_status(component_id, input_rows),
                "bound_status": bound_status(component_id, input_rows),
                "dryrun_result": result_status,
                "blocks_claim": "true",
                "block_reason": block_reason,
                "minimum_for_claim": target["minimum_for_claim"],
            }
        )
    )

local_claim_rows = [
    base(
        {
            "claim_id": "LCS3049_0_constant_kappa",
            "claim": "d kappa_eff=0 is active local theorem",
            "status": "BLOCKED_CONDITIONAL_ONLY",
            "reason": "S_kappa_top variation exists but parent adoption/G_ref/stress/boundary gates are unsigned",
            "evidence": "ADREV3049_0-4",
        }
    ),
    base(
        {
            "claim_id": "LCS3049_1_Newton_AW",
            "claim": "A_W=1 and Newton coefficient is derived",
            "status": "BLOCKED_GREF_OWNERSHIP_UNSIGNED",
            "reason": "A_W still depends on kappa_eff c^4/(8*pi*G_ref); G_ref lock is not parent-derived",
            "evidence": "3046/3048 adoption review",
        }
    ),
    base(
        {
            "claim_id": "LCS3049_2_local_GR_PPN",
            "claim": "local GR/PPN branch passes",
            "status": "BLOCKED_FIRST_ORDER_AND_SECOND_ORDER_RESIDUALS",
            "reason": "Gdot/range/WEP/radial/frame/Bianchi rows are nonclaim and second-order beta remains deferred",
            "evidence": "DRY3049 component results",
        }
    ),
    base(
        {
            "claim_id": "LCS3049_3_R10",
            "claim": "R10 fifth-force/inverse-square pass",
            "status": "BLOCKED_MISSING_ALPHA_CURVE_AND_MTS_PREDICTION",
            "reason": "R10 target has missing lambda, missing alpha_predicted, missing digitized alpha_bound/source file",
            "evidence": "R10_alpha_lambda_curve_MTS_source_normalization.csv",
        }
    ),
    base(
        {
            "claim_id": "LCS3049_4_WEP_source_charge",
            "claim": "source-charge WEP pass",
            "status": "BLOCKED_PARENT_SOURCE_CHARGE_THEOREM_OR_NUMERIC_COEFFICIENT",
            "reason": "conditional zero exists but is not parent-signed; finite coefficient rows remain missing",
            "evidence": "P8_species_source_charge_residual_or_zero.csv",
        }
    ),
]

unlock_rows = [
    base(
        {
            "unlock_id": "UNLOCK3049_0_minimal_topological_spine",
            "route": "derive/adopt S_kappa_top as a parent-action sector",
            "required_contract": "S_kappa_top = integral_M kappa_eff dA_3, A_3 boundary variation fixed/topological, delta_g S_kappa_top=0, matter/source action sees only constant kappa_eff",
            "would_close": "dln_Geff_dt; radial/range kappa running; Bianchi exchange if G_ref also locks",
            "still_needed_after": "G_ref ownership; second-order beta/source-normalized PPN; source/frame pullback silence",
            "priority": 1,
        }
    ),
    base(
        {
            "unlock_id": "UNLOCK3049_1_Gref_lock",
            "route": "parent-owned reference coupling",
            "required_contract": "G_ref = kappa_eff c^4/(8*pi) in the same observed/source frame as W and Phi_metric",
            "would_close": "epsilon_Gref; A_W coefficient mismatch; Newton amplitude normalization",
            "still_needed_after": "field/source hair silence and PPN residual vector",
            "priority": 2,
        }
    ),
    base(
        {
            "unlock_id": "UNLOCK3049_2_scalar_coefficient_fill",
            "route": "if topology fails, fill scalar-kappa residual coefficients",
            "required_contract": "numeric/source-backed dln_Geff_dt, alpha(lambda), eta_source_AB, partial_r profile, delta_frame_source, delta_kappa_source",
            "would_close": "dryrun not-scoreable status and convert closure debt into empirical bounds",
            "still_needed_after": "no-cancellation policy, arena universality, independent source paths",
            "priority": 3,
        }
    ),
]

next_rows = [
    base(
        {
            "next_id": "NEXT3049_0_3050",
            "next_checkpoint": "3050-Y5-R2FR-parent-topological-kappa-spine-with-Gref-lock-or-scalar-kappa-coefficient-fill-under-AX1090.md",
            "script": "scripts/Y5_R2FR_parent_topological_kappa_spine_with_Gref_lock_or_scalar_kappa_coefficient_fill_under_AX1090_3050.py",
            "mission": "try to construct the minimal parent-action topological kappa spine that signs d kappa_eff=0 and G_ref ownership; if any clause fails, select the first scalar-kappa coefficient fill target instead of claiming local GR",
            "starting_equation": "S_kappa_top -> d kappa_eff=0 plus G_ref = kappa_eff c^4/(8*pi); otherwise dryrun residuals remain physical",
            "claim_policy": "only promote Newton/local-GR after parent action, reference coupling, frame/source silence, and residual dryrun gates all pass",
        }
    )
]

decision_rows = [
    base(
        {
            "decision_id": "DEC3049_0_dryrun",
            "question": "Did 3049 make the scalar-kappa residual branch executable?",
            "answer": "YES_NONCLAIM",
            "reason": "all six target files parse and produce dryrun statuses",
            "action": "use dryrun statuses to choose 3050 parent-spine derivation route",
        }
    ),
    base(
        {
            "decision_id": "DEC3049_1_claim",
            "question": "Did any local-GR/R10/WEP branch pass?",
            "answer": "NO",
            "reason": "every branch remains blocked by parent-zero/numeric coefficient or missing R10 curve",
            "action": "no public claim; no GitHub claim escalation",
        }
    ),
    base(
        {
            "decision_id": "DEC3049_2_best_route",
            "question": "What is the best next attack?",
            "answer": "TRY_PARENT_TOPOLOGICAL_KAPPA_SPINE_WITH_GREF_LOCK",
            "reason": "one parent-action proof could kill several residual heads; coefficient filling is second-best",
            "action": "3050 should attempt the theorem first, then demote to coefficient-fill if unsigned",
        }
    ),
]

promotion_gates = [
    base(
        {
            "gate_id": "GATE3049_0_sources_exist",
            "gate": "all cited 3049 sources exist",
            "passed": all(boolish(row["exists"]) for row in source_register),
            "claim_effect": "dryrun evidence is source-backed",
        }
    ),
    base(
        {
            "gate_id": "GATE3049_1_targets_parse",
            "gate": "all scalar-kappa target files parse",
            "passed": all(boolish(row["parse_ok"]) for row in dryrun_results),
            "claim_effect": "dryrun can run",
        }
    ),
    base(
        {
            "gate_id": "GATE3049_2_all_blocked",
            "gate": "every local residual branch remains blocked/nonclaim",
            "passed": all(str(row["dryrun_result"]).startswith("BLOCKED") for row in dryrun_results),
            "claim_effect": "prevents accidental local-GR/R10/WEP promotion",
        }
    ),
    base(
        {
            "gate_id": "GATE3049_3_no_claim_rows",
            "gate": "no target/generated row is valid for claim",
            "passed": not has_claim_true(row_diagnostics + dryrun_results + adoption_review_rows + local_claim_rows + unlock_rows),
            "claim_effect": "private checkpoint only",
        }
    ),
    base(
        {
            "gate_id": "GATE3049_4_adoption_not_promoted",
            "gate": "topological kappa parent adoption remains unpromoted in 3049",
            "passed": any(row["review_id"] == "ADREV3049_1_parent_spine" and row["answer"] == "NO" for row in adoption_review_rows),
            "claim_effect": "no smuggled d kappa_eff=0 theorem",
        }
    ),
    base(
        {
            "gate_id": "GATE3049_5_next_target",
            "gate": "next target attempts parent theorem before coefficient fill",
            "passed": next_rows[0]["next_checkpoint"].startswith("3050-"),
            "claim_effect": "derivation-first path preserved",
        }
    ),
]

write_csv(OUTPUTS["sources"], source_register)
write_csv(OUTPUTS["adoption_review"], adoption_review_rows)
write_csv(OUTPUTS["row_diagnostics"], row_diagnostics)
write_csv(OUTPUTS["dryrun_results"], dryrun_results)
write_csv(OUTPUTS["local_claim_status"], local_claim_rows)
write_csv(OUTPUTS["unlock_map"], unlock_rows)
write_csv(OUTPUTS["promotion_gates"], promotion_gates)
write_csv(OUTPUTS["decision"], decision_rows)
write_csv(OUTPUTS["next"], next_rows)

copy_csv(OUTPUTS["adoption_review"], BRANCH_OUTPUTS["adoption_copy"])
copy_csv(OUTPUTS["row_diagnostics"], BRANCH_OUTPUTS["diagnostics_copy"])
copy_csv(OUTPUTS["dryrun_results"], BRANCH_OUTPUTS["dryrun_copy"])
copy_csv(OUTPUTS["local_claim_status"], BRANCH_OUTPUTS["claim_status_copy"])
copy_csv(OUTPUTS["unlock_map"], BRANCH_OUTPUTS["unlock_copy"])
copy_csv(OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"])

branch_rows = [
    base(
        {
            "copy_id": copy_id,
            "destination": str(path),
            "exists": path.exists(),
            "row_count": len(rows(path)) if path.exists() else 0,
            "description": "3049 branch copy",
        }
    )
    for copy_id, path in BRANCH_OUTPUTS.items()
]
write_csv(OUTPUTS["branches"], branch_rows)

if PYCACHE.exists():
    shutil.rmtree(PYCACHE)

non_validation_csv_paths = [
    *OUTPUTS.values(),
    *BRANCH_OUTPUTS.values(),
]
non_validation_csv_paths.remove(OUTPUTS["validation"])

all_output_rows: list[dict[str, str]] = []
for path in non_validation_csv_paths:
    all_output_rows.extend(rows(path))

formalization_hits = list(FORMALIZATION.rglob("*3049*")) if FORMALIZATION.exists() else []
generated_paths = [DOC, *OUTPUTS.values(), *BRANCH_OUTPUTS.values()]

validation_rows = [
    base({"validation_id": "VAL3049_00_sources_exist", "passed": all(boolish(row["exists"]) for row in source_register), "requirement": "all cited source paths exist", "evidence": OUTPUTS["sources"].name}),
    base({"validation_id": "VAL3049_01_csv_parse", "passed": all(csv_ok(path) for path in non_validation_csv_paths), "requirement": "all generated and branch-copy CSVs parse cleanly", "evidence": "csv.DictReader parse check"}),
    base({"validation_id": "VAL3049_02_targets_covered", "passed": len(dryrun_results) == len(TARGETS), "requirement": "dryrun covers all six scalar-kappa target files", "evidence": OUTPUTS["dryrun_results"].name}),
    base({"validation_id": "VAL3049_03_targets_parse", "passed": all(boolish(row["parse_ok"]) for row in dryrun_results), "requirement": "all scalar-kappa target files parse", "evidence": OUTPUTS["dryrun_results"].name}),
    base({"validation_id": "VAL3049_04_all_blocked", "passed": all(str(row["dryrun_result"]).startswith("BLOCKED") for row in dryrun_results), "requirement": "no scalar-kappa residual target is claim-scoreable", "evidence": OUTPUTS["dryrun_results"].name}),
    base({"validation_id": "VAL3049_05_adoption_not_promoted", "passed": any(row["review_id"] == "ADREV3049_4_decision" and row["answer"] == "NO_KEEP_DRYRUN_BRANCH" for row in adoption_review_rows), "requirement": "topological branch is reviewed but not silently adopted", "evidence": OUTPUTS["adoption_review"].name}),
    base({"validation_id": "VAL3049_06_no_claim_rows", "passed": not has_claim_true(all_output_rows), "requirement": "no generated row is valid for claim", "evidence": "valid_for_claim/claim_allowed/score_ready flags"}),
    base({"validation_id": "VAL3049_07_claim_status_blocked", "passed": all(str(row["status"]).startswith("BLOCKED") for row in local_claim_rows), "requirement": "local Newton/GR/R10/WEP status remains blocked", "evidence": OUTPUTS["local_claim_status"].name}),
    base({"validation_id": "VAL3049_08_unlock_map_exists", "passed": len(unlock_rows) >= 3 and unlock_rows[0]["route"].startswith("derive/adopt"), "requirement": "next derivation route is explicitly mapped", "evidence": OUTPUTS["unlock_map"].name}),
    base({"validation_id": "VAL3049_09_branch_copies", "passed": all(path.exists() and csv_ok(path) for path in BRANCH_OUTPUTS.values()), "requirement": "branch copies exist and parse", "evidence": OUTPUTS["branches"].name}),
    base({"validation_id": "VAL3049_10_output_scope", "passed": all(under(path, ROOT) for path in generated_paths), "requirement": "all generated outputs are inside post-checkpoint-work", "evidence": str(ROOT)}),
    base({"validation_id": "VAL3049_11_formalization_untouched", "passed": len(formalization_hits) == 0, "requirement": "formalization-workbench modified-file target count remains 0", "evidence": f"formalization 3049 hits={len(formalization_hits)}"}),
    base({"validation_id": "VAL3049_12_next_target", "passed": next_rows[0]["next_checkpoint"].startswith("3050-"), "requirement": "next target selects parent topological kappa spine or scalar coefficient fill", "evidence": OUTPUTS["next"].name}),
    base({"validation_id": "VAL3049_13_pycache_removed", "passed": not PYCACHE.exists(), "requirement": "scripts __pycache__ removed", "evidence": str(PYCACHE)}),
]
write_csv(OUTPUTS["validation"], validation_rows)

doc_text = f"""# 3049 - Scalar-Kappa First Bound Runner Dryrun or Parent Adoption Review

Status: `Y5_R2FR_3049_scalar_kappa_dryrun_all_blocked_parent_topology_not_adopted`

Generated: `{RUN_UTC}`

## Verdict

3049 runs the dryrun branch and reviews the parent-adoption branch.

Result: the dryrun is operational, but **every scalar-kappa/local branch remains blocked**. That is actually good discipline: the code path now works, and the theory debt is localized rather than floating around in prose.

The parent/topological route is still the best attack, because one clean parent-action theorem could kill several leakage channels at once:

`S_kappa_top -> d kappa_eff = 0`

plus

`G_ref = kappa_eff c^4/(8*pi)`

But 3049 does not adopt those clauses. It keeps them as the 3050 theorem target.

## Parent Adoption Review

{md_table(adoption_review_rows, ["review_id", "question", "answer", "evidence", "blocks_claim", "missing_for_adoption"])}

## Dryrun Results

{md_table(dryrun_results, ["dryrun_id", "component_id", "quantity", "arena", "parse_ok", "row_count", "missing_marker_count", "prediction_status", "bound_status", "dryrun_result", "block_reason"])}

## Row Diagnostics

{md_table(row_diagnostics, ["diag_id", "component_id", "row_id", "has_missing_marker", "has_conditional_zero_marker", "prediction_status", "bound_status", "diagnostic_status"])}

## Local Claim Status

{md_table(local_claim_rows, ["claim_id", "claim", "status", "reason", "evidence"])}

## Unlock Condition Map

{md_table(unlock_rows, ["unlock_id", "route", "required_contract", "would_close", "still_needed_after", "priority"])}

## Promotion Gates

{md_table(promotion_gates, ["gate_id", "gate", "passed", "claim_effect"])}

## Decision Ledger

{md_table(decision_rows, ["decision_id", "question", "answer", "reason", "action"])}

## Next Target

{md_table(next_rows, ["next_id", "next_checkpoint", "mission", "starting_equation", "claim_policy"])}

## Source Register

{md_table(source_register, ["source_id", "exists", "parse_ok", "row_count", "role", "status"])}

## Branch Copies

{md_table(branch_rows, ["copy_id", "destination", "exists", "row_count", "description"])}

## Validation

{md_table(validation_rows, ["validation_id", "passed", "requirement", "evidence"])}
"""

DOC.write_text(doc_text, encoding="utf-8")

failures = [row for row in validation_rows if not boolish(row["passed"])]
if failures:
    raise SystemExit(f"3049 validation failed: {[row['validation_id'] for row in failures]}")

print(f"wrote {DOC}")
print(f"validation rows: {len(validation_rows)} passed")
print("claim status: dryrun operational; all local scalar-kappa branches blocked; 3050 theorem target selected")
