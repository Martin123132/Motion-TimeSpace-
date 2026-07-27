from __future__ import annotations

import csv
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

CHECKPOINT = "3048"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "3048-Y5-R2FR-scalar-kappa-residual-inputs-or-topological-adoption-decision-under-AX1090.md"

SOURCE_PATHS = {
    "SRC3048_00_3047_doc": ROOT / "3047-Y5-R2FR-topological-kappa-signature-or-scalar-kappa-residual-branch-under-AX1090.md",
    "SRC3048_01_3047_signature": RESIDUALS / "P8_Y5_R2FR_3047_TOPOLOGICAL_KAPPA_SIGNATURE_ATTEMPT.csv",
    "SRC3048_02_3047_variation": RESIDUALS / "P8_Y5_R2FR_3047_KAPPA_VARIATION_AUDIT.csv",
    "SRC3048_03_3047_adoption": RESIDUALS / "P8_Y5_R2FR_3047_PARENT_ADOPTION_GATE.csv",
    "SRC3048_04_3047_scalar_branch": RESIDUALS / "P8_Y5_R2FR_3047_SCALAR_KAPPA_RESIDUAL_BRANCH.csv",
    "SRC3048_05_3047_runner_bridge": RESIDUALS / "P8_Y5_R2FR_3047_SCALAR_KAPPA_RUNNER_BRIDGE.csv",
    "SRC3048_06_3047_next": RESIDUALS / "P8_Y5_R2FR_3047_NEXT_TARGET.csv",
    "SRC3048_07_kappa_top_clause": RESIDUALS / "P8_CONSTANT_KAPPA_TOPOLOGICAL_ZEROFORM_CLAUSE.csv",
    "SRC3048_08_kappa_residual_map": RESIDUALS / "P8_CONSTANT_KAPPA_RESIDUAL_MAP.csv",
    "SRC3048_09_global_coupling_contract": RESIDUALS / "P8_global_coupling_superselection_CONTRACT.csv",
    "SRC3048_10_constant_kappa_contract": RESIDUALS / "P8_constant_universal_Geff_kappa_CONTRACT.csv",
    "SRC3048_11_constant_gm_bound_matrix": RESIDUALS / "P8_CONSTANT_GM_RESIDUAL_BOUND_MATRIX.csv",
    "SRC3048_12_constant_gm_runner": RESIDUALS / "P8_CONSTANT_GM_LOCAL_RESIDUAL_RUNNER_INPUT.csv",
    "SRC3048_13_constant_gm_fill_queue": RESIDUALS / "P8_CONSTANT_GM_DERIVATIVE_HAIR_FILL_QUEUE.csv",
    "SRC3048_14_r10_existing_alpha": RESIDUALS / "R10_alpha_lambda_curve_MTS_source_normalization.csv",
    "SRC3048_15_wep_existing_species": RESIDUALS / "P8_species_source_charge_residual_or_zero.csv",
}

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3048_SOURCE_REGISTER.csv",
    "adoption_decision": RESIDUALS / "P8_Y5_R2FR_3048_TOPOLOGICAL_ADOPTION_DECISION.csv",
    "target_seed_audit": RESIDUALS / "P8_Y5_R2FR_3048_SCALAR_KAPPA_TARGET_SEED_AUDIT.csv",
    "first_inputs": RESIDUALS / "P8_Y5_R2FR_3048_SCALAR_KAPPA_FIRST_INPUT_ROWS_NONCLAIM.csv",
    "bound_linkage": RESIDUALS / "P8_Y5_R2FR_3048_BOUND_MATRIX_LINKAGE.csv",
    "runner_readiness": RESIDUALS / "P8_Y5_R2FR_3048_RUNNER_READINESS.csv",
    "promotion_gates": RESIDUALS / "P8_Y5_R2FR_3048_PROMOTION_GATES.csv",
    "countermodels": RESIDUALS / "P8_Y5_R2FR_3048_COUNTERMODEL_LEDGER.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_3048_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_3048_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_3048_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3048_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "adoption_copy": PARENT_ACTION / "topological_kappa_adoption_decision_3048_NOT_ADOPTED.csv",
    "seed_audit_copy": LOCAL_BOUNDS / "scalar_kappa_target_seed_audit_3048_NONCLAIM.csv",
    "first_inputs_copy": LOCAL_BOUNDS / "scalar_kappa_first_input_rows_3048_NONCLAIM.csv",
    "bound_linkage_copy": LOCAL_BOUNDS / "scalar_kappa_bound_matrix_linkage_3048_BLOCKED_NONCLAIM.csv",
    "readiness_copy": LOCAL_BOUNDS / "scalar_kappa_runner_readiness_3048_BLOCKED_NONCLAIM.csv",
    "queue_copy": RAB_QUEUE / "JR3048_SCALAR_KAPPA_FIRST_BOUND_RUNNER_DRYRUN_OR_PARENT_ADOPTION_REVIEW_NEXT_NONCLAIM.csv",
}

TARGET_FILES = {
    "P8_Geff_time_drift": RESIDUALS / "P8_time_drift_residual_or_zero.csv",
    "P8_range_dependence": RESIDUALS / "R10_alpha_lambda_curve_MTS_source_normalization.csv",
    "P8_species_source_charge": RESIDUALS / "P8_species_source_charge_residual_or_zero.csv",
    "P8_radial_source_hair": RESIDUALS / "P8_radial_mu_profile_or_zero.csv",
    "P8_frame_calibration_split": RESIDUALS / "P8_frame_source_split_residual_or_zero.csv",
    "P8_Bianchi_kappa_exchange": RESIDUALS / "P8_delta_kappa_source_exchange_residual.csv",
}

SEED_TARGETS = {
    "P8_Geff_time_drift": [
        {
            "row_id": "TD3048_0_time_drift_definition",
            "component_id": "P8_Geff_time_drift",
            "observable": "Gdot_over_G",
            "symbol": "dln_Geff_dt",
            "formula": "dln_Geff_dt := D_t ln(kappa_eff c^4/(8*pi)) in the observed local frame",
            "candidate_value": "MISSING_NUMERIC_OR_DERIVED_ZERO_DRIFT",
            "bound_or_target": "9.6e-15 yr^-1 or derived zero",
            "units": "yr^-1",
            "source_path": str(RESIDUALS / "P8_CONSTANT_GM_RESIDUAL_BOUND_MATRIX.csv"),
            "empirical_provenance": "bound matrix row P8_Geff_time_drift; source-backed numeric coefficient still missing",
            "derivation_status": "SEEDED_NONCLAIM_3048_MISSING_PARENT_ZERO_OR_NUMERIC_DRIFT",
            "score_ready": "false",
            "valid_prediction_row": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "next_action": "derive topological/global kappa superselection with G_ref ownership or fill dln_Geff_dt prediction from parent scalar-kappa dynamics",
            "timestamp_utc": RUN_UTC,
        }
    ],
    "P8_radial_source_hair": [
        {
            "row_id": "RH3048_0_radial_hair_definition",
            "component_id": "P8_radial_source_hair",
            "observable": "partial_r_ln_mu_obs",
            "symbol": "partial_r_ln_Geff;partial_r_ln_mu_obs",
            "formula": "partial_r ln mu_obs = partial_r ln G_eff + partial_r ln M_eff + partial_r ln(1+epsilon_mu)",
            "candidate_value": "MISSING_RADIAL_PROFILE_OR_DERIVED_ZERO",
            "bound_or_target": "zero radial hair or mapped PPN/fifth-force residuals",
            "units": "inverse_length_or_dimensionless_envelope",
            "source_path": str(RESIDUALS / "P8_CONSTANT_GM_RESIDUAL_BOUND_MATRIX.csv"),
            "empirical_provenance": "bound matrix row P8_radial_source_hair; no radial profile yet",
            "derivation_status": "SEEDED_NONCLAIM_3048_MISSING_GAUSS_NOHAIR_THEOREM_OR_PROFILE",
            "score_ready": "false",
            "valid_prediction_row": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "next_action": "derive exterior Gauss/no-hair law for kappa_eff or provide radial envelope mapped to PPN/R10",
            "timestamp_utc": RUN_UTC,
        }
    ],
    "P8_frame_calibration_split": [
        {
            "row_id": "FS3048_0_frame_split_definition",
            "component_id": "P8_frame_calibration_split",
            "observable": "delta_frame_source",
            "symbol": "delta_frame_source;D_domain_ln_Geff",
            "formula": "delta_frame_source := Delta_frame ln(kappa_eff source readout) after one observed-frame calibration",
            "candidate_value": "MISSING_NUMERIC_OR_DERIVED_ZERO_FRAME_SPLIT",
            "bound_or_target": "one observed source frame or explicit residual below WEP/clock locks",
            "units": "dimensionless",
            "source_path": str(RESIDUALS / "P8_CONSTANT_GM_RESIDUAL_BOUND_MATRIX.csv"),
            "empirical_provenance": "bound matrix row P8_frame_calibration_split; same-frame source theorem missing",
            "derivation_status": "SEEDED_NONCLAIM_3048_MISSING_SOURCE_VARIATION_FRAME_THEOREM",
            "score_ready": "false",
            "valid_prediction_row": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "next_action": "attach the same parent pullback to source variation and matter readout, or fill residual coefficient",
            "timestamp_utc": RUN_UTC,
        }
    ],
    "P8_Bianchi_kappa_exchange": [
        {
            "row_id": "BK3048_0_bianchi_exchange_definition",
            "component_id": "P8_Bianchi_kappa_exchange",
            "observable": "q_loc_kappa_exchange",
            "symbol": "delta_kappa_source",
            "formula": "delta_kappa_source := kappa_eff^-1 P_loc[T_obs^{mu nu} nabla_mu kappa_eff]",
            "candidate_value": "MISSING_ARENA_PROJECTION_OR_DERIVED_ZERO_EXCHANGE",
            "bound_or_target": "same-frame arbitrary-source conservation theorem or explicit exchange coefficient",
            "units": "projected_force_density_or_dimensionless_normalized_residual",
            "source_path": str(RESIDUALS / "P8_CONSTANT_KAPPA_RESIDUAL_MAP.csv"),
            "empirical_provenance": "residual map KR508_5; local arena projection not yet sourced",
            "derivation_status": "SEEDED_NONCLAIM_3048_MISSING_BIANCHI_SAME_FRAME_CONSERVATION_THEOREM",
            "score_ready": "false",
            "valid_prediction_row": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "next_action": "prove arbitrary-source same-frame conservation with nabla kappa_eff=0 or map exchange coefficient into q_loc/PPN/R10 arena rows",
            "timestamp_utc": RUN_UTC,
        }
    ],
}

for path in list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC] + list(TARGET_FILES.values()):
    path.parent.mkdir(parents=True, exist_ok=True)


def rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def as_str(value: Any) -> str:
    return "" if value is None else str(value)


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


def boolish(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "y", "passed"}


def csv_ok(path: Path) -> bool:
    try:
        if not path.exists():
            return False
        with path.open("r", newline="", encoding="utf-8") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
        return False


def under(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def has_claim_true(input_rows: list[dict[str, str]]) -> bool:
    claim_fields = {"valid_for_claim", "claim_allowed", "valid_prediction_row", "score_ready"}
    return any(boolish(row.get(field, "false")) for row in input_rows for field in claim_fields)


def has_missing_marker(input_rows: list[dict[str, str]]) -> bool:
    return any("MISSING" in value.upper() for row in input_rows for value in row.values())


def base(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "checkpoint": CHECKPOINT,
        "branch_id": BRANCH_ID,
        "timestamp_utc": RUN_UTC,
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
        for col in columns:
            value = as_str(row.get(col, "")).replace("\n", " ").replace("|", "/")
            values.append(value)
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def copy_csv(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dst)


existing_before = {component_id: path.exists() for component_id, path in TARGET_FILES.items()}

seed_audit_rows: list[dict[str, Any]] = []
for component_id, seed_rows in SEED_TARGETS.items():
    path = TARGET_FILES[component_id]
    created = False
    if not path.exists():
        write_csv(path, seed_rows)
        created = True
    parsed_rows = rows(path)
    seed_audit_rows.append(
        base(
            {
                "audit_id": f"SEED3048_{component_id}",
                "component_id": component_id,
                "target_file": str(path),
                "existed_before": existing_before[component_id],
                "created_by_3048": created,
                "exists_after": path.exists(),
                "parse_ok": csv_ok(path),
                "row_count": len(parsed_rows),
                "contains_missing_marker": has_missing_marker(parsed_rows),
                "contains_claim_true": has_claim_true(parsed_rows),
                "status": "SEEDED_NONCLAIM" if created else "EXISTING_REUSED_NONCLAIM_AUDITED",
                "valid_for_claim": "false",
            }
        )
    )

source_register = [
    base(
        {
            "source_id": source_id,
            "path": str(path),
            "exists": path.exists(),
            "row_count": len(rows(path)) if path.suffix.lower() == ".csv" and path.exists() else "",
            "role": source_id.split("_", 2)[-1],
            "status": "PRESENT" if path.exists() else "MISSING_BLOCKER",
            "valid_for_claim": "false",
        }
    )
    for source_id, path in SOURCE_PATHS.items()
]

bound_matrix_rows = rows(SOURCE_PATHS["SRC3048_11_constant_gm_bound_matrix"])
bound_by_component = {row.get("component_id", ""): row for row in bound_matrix_rows}

first_input_components = [
    {
        "input_id": "SKRI3048_0_Gdot",
        "component_id": "P8_Geff_time_drift",
        "quantity": "dln_Geff_dt",
        "target_file": TARGET_FILES["P8_Geff_time_drift"],
        "formula": "D_t ln(kappa_eff c^4/(8*pi))",
        "current_value": "MISSING_NUMERIC_OR_DERIVED_ZERO_DRIFT",
        "observable_link": "Gdot_over_G; local GR",
    },
    {
        "input_id": "SKRI3048_1_R10",
        "component_id": "P8_range_dependence",
        "quantity": "alpha(lambda)",
        "target_file": TARGET_FILES["P8_range_dependence"],
        "formula": "finite-range kappa/source hair maps to alpha(lambda)",
        "current_value": "MISSING_EXECUTABLE_ALPHA_LAMBDA_CURVE_OR_ZERO_THEOREM",
        "observable_link": "R10 inverse-square/fifth-force",
    },
    {
        "input_id": "SKRI3048_2_WEP",
        "component_id": "P8_species_source_charge",
        "quantity": "eta_source_AB",
        "target_file": TARGET_FILES["P8_species_source_charge"],
        "formula": "eta_source_AB = epsilon_species_A - epsilon_species_B",
        "current_value": "ZERO_IF_PARENT_MEASURE_CURRENT_SOURCE_LABEL_THEOREM_SIGNED; otherwise missing numeric",
        "observable_link": "source-charge WEP",
    },
    {
        "input_id": "SKRI3048_3_radial",
        "component_id": "P8_radial_source_hair",
        "quantity": "partial_r ln G_eff",
        "target_file": TARGET_FILES["P8_radial_source_hair"],
        "formula": "partial_r ln mu_obs residual decomposition",
        "current_value": "MISSING_RADIAL_PROFILE_OR_DERIVED_ZERO",
        "observable_link": "Newton inverse-square; PPN gamma/beta; R10",
    },
    {
        "input_id": "SKRI3048_4_frame",
        "component_id": "P8_frame_calibration_split",
        "quantity": "delta_frame_source",
        "target_file": TARGET_FILES["P8_frame_calibration_split"],
        "formula": "Delta_frame ln(kappa_eff source readout)",
        "current_value": "MISSING_NUMERIC_OR_DERIVED_ZERO_FRAME_SPLIT",
        "observable_link": "clock; WEP; same-frame Newton",
    },
    {
        "input_id": "SKRI3048_5_Bianchi",
        "component_id": "P8_Bianchi_kappa_exchange",
        "quantity": "delta_kappa_source",
        "target_file": TARGET_FILES["P8_Bianchi_kappa_exchange"],
        "formula": "kappa_eff^-1 P_loc[T_obs^{mu nu} nabla_mu kappa_eff]",
        "current_value": "MISSING_ARENA_PROJECTION_OR_DERIVED_ZERO_EXCHANGE",
        "observable_link": "q_loc; PPN; R10; conservation",
    },
]

first_input_rows: list[dict[str, Any]] = []
bound_linkage_rows: list[dict[str, Any]] = []
runner_readiness_rows: list[dict[str, Any]] = []
for component in first_input_components:
    path = Path(component["target_file"])
    parsed_rows = rows(path)
    matrix_row = bound_by_component.get(component["component_id"], {})
    bound_status = "BOUND_MATRIX_LINKED" if matrix_row else "MISSING_DIRECT_BOUND_MATRIX_ROW"
    if component["component_id"] == "P8_Bianchi_kappa_exchange":
        bound_status = "NEEDS_ARENA_PROJECTION_BEFORE_DIRECT_BOUND"
    first_input_rows.append(
        base(
            {
                "input_id": component["input_id"],
                "component_id": component["component_id"],
                "quantity": component["quantity"],
                "formula": component["formula"],
                "target_file": str(path),
                "file_exists": path.exists(),
                "row_count": len(parsed_rows),
                "current_value": component["current_value"],
                "observable_link": component["observable_link"],
                "missing_for_claim": "DERIVED_ZERO_OR_NUMERIC_PARENT_COEFFICIENT; SOURCE_PATH; UNITS; ARENA_PROJECTION",
                "status": "FIRST_INPUT_ROW_PRESENT_NONCLAIM",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            }
        )
    )
    bound_linkage_rows.append(
        base(
            {
                "link_id": f"BL3048_{component['component_id']}",
                "component_id": component["component_id"],
                "quantity": component["quantity"],
                "bound_status": bound_status,
                "target_type": matrix_row.get("target_type", "arena_projection_required"),
                "target_value": matrix_row.get("target_value", "not_yet_directly_mapped"),
                "units": matrix_row.get("units", "not_yet_directly_mapped"),
                "evaluation_rule": matrix_row.get("evaluation_rule", "derive/map arena projection before scoring"),
                "reason_not_scoreable": matrix_row.get("reason_not_scoreable", "local arena projection/source coefficient missing"),
                "valid_for_claim": "false",
            }
        )
    )
    runner_readiness_rows.append(
        base(
            {
                "runner_id": f"RUN3048_{component['component_id']}",
                "component_id": component["component_id"],
                "target_file": str(path),
                "parse_ok": csv_ok(path),
                "has_missing_marker": has_missing_marker(parsed_rows),
                "has_claim_true": has_claim_true(parsed_rows),
                "ready_for_nonclaim_dryrun": path.exists() and csv_ok(path),
                "ready_for_claim": "false",
                "blocked_by": "MISSING_PARENT_ZERO_OR_NUMERIC_COEFFICIENT" if has_missing_marker(parsed_rows) else "NONCLAIM_STATUS_RETAINED",
                "status": "DRYRUN_READY_BUT_CLAIM_BLOCKED" if path.exists() and csv_ok(path) else "NOT_READY",
                "valid_for_claim": "false",
            }
        )
    )

adoption_rows = [
    base(
        {
            "decision_id": "ADOPT3048_0_parent_spine",
            "question": "Do we promote S_kappa_top into the active parent action now?",
            "answer": "NO_NOT_IN_3048",
            "reason": "3047 proved the variation route only conditionally; promotion still needs explicit parent-spine ownership, G_ref ownership, and boundary/stress silence.",
            "claim_effect": "d kappa_eff=0 remains conditional; no A_W/Newton/PPN/local-GR claim",
            "valid_for_claim": "false",
        }
    ),
    base(
        {
            "decision_id": "ADOPT3048_1_Gref_ownership",
            "question": "Is G_ref now owned by kappa_eff through the parent action?",
            "answer": "UNSIGNED",
            "reason": "3046 left G_ref = kappa_eff c^4/(8*pi) as required but not parent-derived.",
            "claim_effect": "epsilon_Gref and A_W remain retained residuals",
            "valid_for_claim": "false",
        }
    ),
    base(
        {
            "decision_id": "ADOPT3048_2_boundary_stress",
            "question": "Are boundary variation and topological stress silence signed?",
            "answer": "UNSIGNED",
            "reason": "A_3 boundary/fixed-sector and metric-stress silence are required clauses, not yet active parent theorems.",
            "claim_effect": "topological kappa route cannot be used as a public theorem",
            "valid_for_claim": "false",
        }
    ),
    base(
        {
            "decision_id": "ADOPT3048_3_residual_branch",
            "question": "What is the honest fallback?",
            "answer": "SCALAR_KAPPA_RESIDUAL_INPUTS_STAGED",
            "reason": "All missing local effects are represented as explicit nonclaim rows rather than hidden assumptions.",
            "claim_effect": "testable/dryrun path is open; claim path remains closed",
            "valid_for_claim": "false",
        }
    ),
]

countermodel_rows = [
    base(
        {
            "countermodel_id": "CM3048_0_promote_without_parent",
            "case": "Use d kappa_eff=0 from the topological ansatz without adding S_kappa_top to the active parent action",
            "why_it_blocks": "This imports the desired constant-coupling result as an axiom; it is not a derivation.",
            "status": "LIVE_BLOCKER",
            "valid_for_claim": "false",
        }
    ),
    base(
        {
            "countermodel_id": "CM3048_1_constant_kappa_free_Gref",
            "case": "kappa_eff is constant but G_ref remains an independent denominator in W",
            "why_it_blocks": "A_W can still be a constant mismatch: kappa_eff c^4/(8*pi*G_ref)-1.",
            "status": "LIVE_BLOCKER",
            "valid_for_claim": "false",
        }
    ),
    base(
        {
            "countermodel_id": "CM3048_2_bound_inversion",
            "case": "Fit or choose residual coefficients from experimental limits",
            "why_it_blocks": "A bound cannot define the parent coupling; coefficients must come from parent action or remain nonclaim.",
            "status": "LIVE_BLOCKER",
            "valid_for_claim": "false",
        }
    ),
    base(
        {
            "countermodel_id": "CM3048_3_seed_as_evidence",
            "case": "Treat the new seed CSVs as evidence that local GR passes",
            "why_it_blocks": "They intentionally contain MISSING markers and valid_for_claim=false.",
            "status": "LIVE_BLOCKER",
            "valid_for_claim": "false",
        }
    ),
]

decision_rows = [
    base(
        {
            "decision_id": "DEC3048_0_route",
            "question": "adopt topology or stage scalar-kappa residuals?",
            "answer": "stage scalar-kappa residuals",
            "reason": "No explicit theory decision has promoted the parent-action spine, and adoption would be too easy to smuggle.",
            "action": "seed missing residual files and audit existing nonclaim rows",
            "valid_for_claim": "false",
        }
    ),
    base(
        {
            "decision_id": "DEC3048_1_claim",
            "question": "does 3048 improve the claim status?",
            "answer": "NO_CLAIM_BUT_BETTER_TESTABILITY",
            "reason": "The bottleneck is now executable: each missing coupling leak has a file, row, and next action.",
            "action": "run nonclaim dryrun next; do not use as evidence",
            "valid_for_claim": "false",
        }
    ),
    base(
        {
            "decision_id": "DEC3048_2_next",
            "question": "what is the next least-smuggly move?",
            "answer": "3049 scalar-kappa runner dryrun or explicit parent adoption review",
            "reason": "Either prove/adopt the topological clause, or let the residual runner show exactly why local-GR remains blocked.",
            "action": "build 3049 dryrun/adoption review",
            "valid_for_claim": "false",
        }
    ),
]

generated_so_far = [
    OUTPUTS["sources"],
    OUTPUTS["adoption_decision"],
    OUTPUTS["target_seed_audit"],
    OUTPUTS["first_inputs"],
    OUTPUTS["bound_linkage"],
    OUTPUTS["runner_readiness"],
    OUTPUTS["countermodels"],
    OUTPUTS["decision"],
    OUTPUTS["next"],
    OUTPUTS["branches"],
] + list(BRANCH_OUTPUTS.values())

next_rows = [
    base(
        {
            "next_id": "NEXT3048_0_3049",
            "next_checkpoint": "3049-Y5-R2FR-scalar-kappa-first-bound-runner-dryrun-or-parent-adoption-review-under-AX1090.md",
            "script": "scripts/Y5_R2FR_scalar_kappa_first_bound_runner_dryrun_or_parent_adoption_review_under_AX1090_3049.py",
            "mission": "dry-run the scalar-kappa residual files and confirm every local-GR/R10/WEP/clock branch remains blocked unless a parent-derived zero or numeric coefficient exists; alternatively run an explicit parent-adoption review for S_kappa_top and G_ref ownership",
            "starting_equation": "d kappa_eff=0 only after parent adoption; otherwise retain dln_Geff_dt, alpha(lambda), eta_source_AB, partial_r ln G_eff, delta_frame_source and delta_kappa_source",
            "claim_policy": "no A_W/Newton/PPN/local-GR claim from seeded residual files",
            "valid_for_claim": "false",
        }
    )
]

promotion_gates = [
    base(
        {
            "gate_id": "GATE3048_0_sources_exist",
            "gate": "all cited 3048 source paths exist",
            "passed": all(boolish(row["exists"]) for row in source_register),
            "claim_effect": "source-backed private checkpoint",
            "valid_for_claim": "false",
        }
    ),
    base(
        {
            "gate_id": "GATE3048_1_target_files_exist",
            "gate": "Gdot/R10/WEP/radial/frame/Bianchi residual target files exist",
            "passed": all(path.exists() for path in TARGET_FILES.values()),
            "claim_effect": "nonclaim runner dryrun can proceed",
            "valid_for_claim": "false",
        }
    ),
    base(
        {
            "gate_id": "GATE3048_2_no_claim_rows",
            "gate": "no generated or target residual row is valid for claim",
            "passed": not any(has_claim_true(rows(path)) for path in TARGET_FILES.values()),
            "claim_effect": "blocks accidental overclaim",
            "valid_for_claim": "false",
        }
    ),
    base(
        {
            "gate_id": "GATE3048_3_parent_adoption",
            "gate": "topological kappa sector actively adopted into parent action",
            "passed": "false",
            "claim_effect": "constant-kappa theorem remains conditional",
            "valid_for_claim": "false",
        }
    ),
    base(
        {
            "gate_id": "GATE3048_4_runner_readiness",
            "gate": "all scalar-kappa target files parse for nonclaim dryrun",
            "passed": all(boolish(row["parse_ok"]) for row in runner_readiness_rows),
            "claim_effect": "3049 can run dryrun",
            "valid_for_claim": "false",
        }
    ),
    base(
        {
            "gate_id": "GATE3048_5_next_target",
            "gate": "next target is dryrun/adoption review, not public claim",
            "passed": next_rows[0]["next_checkpoint"].startswith("3049-"),
            "claim_effect": "keeps path derivable/testable",
            "valid_for_claim": "false",
        }
    ),
]

write_csv(OUTPUTS["sources"], source_register)
write_csv(OUTPUTS["adoption_decision"], adoption_rows)
write_csv(OUTPUTS["target_seed_audit"], seed_audit_rows)
write_csv(OUTPUTS["first_inputs"], first_input_rows)
write_csv(OUTPUTS["bound_linkage"], bound_linkage_rows)
write_csv(OUTPUTS["runner_readiness"], runner_readiness_rows)
write_csv(OUTPUTS["promotion_gates"], promotion_gates)
write_csv(OUTPUTS["countermodels"], countermodel_rows)
write_csv(OUTPUTS["decision"], decision_rows)
write_csv(OUTPUTS["next"], next_rows)

copy_csv(OUTPUTS["adoption_decision"], BRANCH_OUTPUTS["adoption_copy"])
copy_csv(OUTPUTS["target_seed_audit"], BRANCH_OUTPUTS["seed_audit_copy"])
copy_csv(OUTPUTS["first_inputs"], BRANCH_OUTPUTS["first_inputs_copy"])
copy_csv(OUTPUTS["bound_linkage"], BRANCH_OUTPUTS["bound_linkage_copy"])
copy_csv(OUTPUTS["runner_readiness"], BRANCH_OUTPUTS["readiness_copy"])
copy_csv(OUTPUTS["next"], BRANCH_OUTPUTS["queue_copy"])

branch_rows = [
    base(
        {
            "copy_id": copy_id,
            "destination": str(path),
            "exists": path.exists(),
            "row_count": len(rows(path)) if path.exists() else 0,
            "description": "3048 branch copy",
            "valid_for_claim": "false",
        }
    )
    for copy_id, path in BRANCH_OUTPUTS.items()
]
write_csv(OUTPUTS["branches"], branch_rows)

if PYCACHE.exists():
    shutil.rmtree(PYCACHE)

non_validation_csv_paths = [
    OUTPUTS["sources"],
    OUTPUTS["adoption_decision"],
    OUTPUTS["target_seed_audit"],
    OUTPUTS["first_inputs"],
    OUTPUTS["bound_linkage"],
    OUTPUTS["runner_readiness"],
    OUTPUTS["promotion_gates"],
    OUTPUTS["countermodels"],
    OUTPUTS["decision"],
    OUTPUTS["next"],
    OUTPUTS["branches"],
    *BRANCH_OUTPUTS.values(),
    *TARGET_FILES.values(),
]

all_generated_rows: list[dict[str, str]] = []
for path in non_validation_csv_paths:
    all_generated_rows.extend(rows(path))

formalization_hits = list(FORMALIZATION.rglob("*3048*")) if FORMALIZATION.exists() else []
generated_paths = [DOC, *OUTPUTS.values(), *BRANCH_OUTPUTS.values(), *TARGET_FILES.values()]

validation_rows = [
    base({"validation_id": "VAL3048_00_sources_exist", "passed": all(boolish(row["exists"]) for row in source_register), "requirement": "all cited source paths exist", "evidence": OUTPUTS["sources"].name}),
    base({"validation_id": "VAL3048_01_seed_targets_exist", "passed": all(path.exists() for path in TARGET_FILES.values()), "requirement": "all scalar-kappa target files exist after seeding", "evidence": OUTPUTS["target_seed_audit"].name}),
    base({"validation_id": "VAL3048_02_csv_parse", "passed": all(csv_ok(path) for path in non_validation_csv_paths), "requirement": "all generated, branch-copy, and scalar-kappa target CSVs parse cleanly", "evidence": "csv.DictReader parse check"}),
    base({"validation_id": "VAL3048_03_topological_not_adopted", "passed": any(row["decision_id"] == "ADOPT3048_0_parent_spine" and row["answer"] == "NO_NOT_IN_3048" for row in adoption_rows), "requirement": "topological kappa clause is not silently promoted", "evidence": OUTPUTS["adoption_decision"].name}),
    base({"validation_id": "VAL3048_04_first_inputs_cover_targets", "passed": len(first_input_rows) == 6 and all(boolish(row["file_exists"]) for row in first_input_rows), "requirement": "first input rows cover Gdot, R10, WEP, radial, frame, and Bianchi exchange", "evidence": OUTPUTS["first_inputs"].name}),
    base({"validation_id": "VAL3048_05_runner_dryrun_ready", "passed": all(boolish(row["ready_for_nonclaim_dryrun"]) for row in runner_readiness_rows), "requirement": "target files are ready for nonclaim dryrun", "evidence": OUTPUTS["runner_readiness"].name}),
    base({"validation_id": "VAL3048_06_claims_blocked", "passed": not any(has_claim_true(rows(path)) for path in TARGET_FILES.values()) and not any(has_claim_true([row]) for row in all_generated_rows), "requirement": "no target or generated row is valid for claim", "evidence": "valid_for_claim/claim_allowed/score_ready flags"}),
    base({"validation_id": "VAL3048_07_missing_markers_retained", "passed": any(boolish(row["has_missing_marker"]) for row in runner_readiness_rows), "requirement": "missing theory inputs remain visible instead of hidden", "evidence": OUTPUTS["runner_readiness"].name}),
    base({"validation_id": "VAL3048_08_countermodels_live", "passed": len(countermodel_rows) >= 4 and all(row["status"] == "LIVE_BLOCKER" for row in countermodel_rows), "requirement": "shortcut countermodels remain live", "evidence": OUTPUTS["countermodels"].name}),
    base({"validation_id": "VAL3048_09_branch_copies", "passed": all(path.exists() and csv_ok(path) for path in BRANCH_OUTPUTS.values()), "requirement": "branch copies exist and parse", "evidence": OUTPUTS["branches"].name}),
    base({"validation_id": "VAL3048_10_output_scope", "passed": all(under(path, ROOT) for path in generated_paths), "requirement": "all generated outputs are inside post-checkpoint-work", "evidence": str(ROOT)}),
    base({"validation_id": "VAL3048_11_formalization_untouched", "passed": len(formalization_hits) == 0, "requirement": "formalization-workbench modified-file target count remains 0", "evidence": f"formalization 3048 hits={len(formalization_hits)}"}),
    base({"validation_id": "VAL3048_12_next_target", "passed": next_rows[0]["next_checkpoint"].startswith("3049-"), "requirement": "next target selects scalar-kappa dryrun or parent adoption review", "evidence": OUTPUTS["next"].name}),
    base({"validation_id": "VAL3048_13_pycache_removed", "passed": not PYCACHE.exists(), "requirement": "scripts __pycache__ removed", "evidence": str(PYCACHE)}),
]
write_csv(OUTPUTS["validation"], validation_rows)

doc_text = f"""# 3048 - Scalar-Kappa Residual Inputs or Topological Adoption Decision

Status: `Y5_R2FR_3048_scalar_kappa_inputs_seeded_topology_not_adopted`

Generated: `{RUN_UTC}`

## Verdict

3048 does **not** promote the topological kappa route into the active parent-action spine.

The clean 3047 identity remains:

`delta_A3 S_kappa_top -> d kappa_eff = 0`

but only if `S_kappa_top` is actually parent-owned and if `G_ref`, boundary variation, metric-stress silence, and matter/source blindness are all signed. They are not signed here.

So this checkpoint takes the non-smuggly fallback: every scalar-kappa leakage channel now has an explicit target file/row path. The new rows are deliberately nonclaim and contain visible missing markers where the parent zero theorem or numeric coefficient is absent.

## Topological Adoption Decision

{md_table(adoption_rows, ["decision_id", "question", "answer", "reason", "claim_effect"])}

## Scalar-Kappa Target Seed Audit

{md_table(seed_audit_rows, ["audit_id", "component_id", "target_file", "existed_before", "created_by_3048", "exists_after", "parse_ok", "row_count", "contains_missing_marker", "contains_claim_true", "status"])}

## First Input Rows

{md_table(first_input_rows, ["input_id", "component_id", "quantity", "formula", "target_file", "current_value", "observable_link", "status"])}

## Bound Matrix Linkage

{md_table(bound_linkage_rows, ["link_id", "component_id", "quantity", "bound_status", "target_value", "units", "reason_not_scoreable"])}

## Runner Readiness

{md_table(runner_readiness_rows, ["runner_id", "component_id", "parse_ok", "has_missing_marker", "has_claim_true", "ready_for_nonclaim_dryrun", "ready_for_claim", "blocked_by", "status"])}

## Countermodels

{md_table(countermodel_rows, ["countermodel_id", "case", "why_it_blocks", "status"])}

## Decision Ledger

{md_table(decision_rows, ["decision_id", "question", "answer", "reason", "action"])}

## Promotion Gates

{md_table(promotion_gates, ["gate_id", "gate", "passed", "claim_effect"])}

## Next Target

{md_table(next_rows, ["next_id", "next_checkpoint", "mission", "starting_equation", "claim_policy"])}

## Source Register

{md_table(source_register, ["source_id", "exists", "row_count", "role", "status"])}

## Branch Copies

{md_table(branch_rows, ["copy_id", "destination", "exists", "row_count", "description"])}

## Validation

{md_table(validation_rows, ["validation_id", "passed", "requirement", "evidence"])}
"""

DOC.write_text(doc_text, encoding="utf-8")

failures = [row for row in validation_rows if not boolish(row["passed"])]
if failures:
    raise SystemExit(f"3048 validation failed: {[row['validation_id'] for row in failures]}")

print(f"wrote {DOC}")
print(f"validation rows: {len(validation_rows)} passed")
print("claim status: topology not adopted; scalar-kappa residual inputs seeded for nonclaim dryrun")
