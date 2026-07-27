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
PARENT_ACTION = ROOT / "source-intake" / "parent-action"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"
PYCACHE = ROOT / "scripts" / "__pycache__"

CHECKPOINT = "3068"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "3068-Y5-R2FR-phi-owner-source-equation-or-tracefree-route-demotion-under-AX1090.md"
DOTG_TARGET = RESIDUALS / "P8_time_drift_residual_or_zero.csv"

SOURCE_PATHS = {
    "SRC3068_00_3067_doc": ROOT / "3067-Y5-R2FR-tracefree-improvement-Khat-birth-certificate-or-DeltaK-TF-bound-under-AX1090.md",
    "SRC3068_01_3067_next": RESIDUALS / "P8_Y5_R2FR_3067_NEXT_TARGET.csv",
    "SRC3068_02_3067_birth_gate": RESIDUALS / "P8_Y5_R2FR_3067_TRACEFREE_BIRTH_CERTIFICATE_GATE.csv",
    "SRC3068_03_3067_divergence": RESIDUALS / "P8_Y5_R2FR_3067_KL_DIVERGENCE_AND_DOMAIN_AUDIT.csv",
    "SRC3068_04_3067_deltak_tf": RESIDUALS / "P8_Y5_R2FR_3067_DELTAK_TF_BOUND_ROWS_NONCLAIM.csv",
    "SRC3068_05_1527_phi_owner_hunt": RESIDUALS / "P8_Y5_PARENT_QLOC_1527_PHI_OWNER_SOURCE_HUNT.csv",
    "SRC3068_06_1527_aux_action": RESIDUALS / "P8_Y5_PARENT_QLOC_1527_LOCAL_AUXILIARY_ACTION_CONTRACT.csv",
    "SRC3068_07_1527_multiplier_silence": RESIDUALS / "P8_Y5_PARENT_QLOC_1527_MULTIPLIER_STRESS_SILENCE_GATE.csv",
    "SRC3068_08_1527_nonlocality": RESIDUALS / "P8_Y5_PARENT_QLOC_1527_NONLOCALITY_GUARD.csv",
    "SRC3068_09_1527_adoption": RESIDUALS / "P8_Y5_PARENT_QLOC_1527_KHAT_ADOPTION_ROW.csv",
    "SRC3068_10_1527_claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1527_CLAIM_GATE.csv",
    "SRC3068_11_1527_local_gr": RESIDUALS / "P8_Y5_PARENT_QLOC_1527_LOCAL_GR_NEWTON_STATUS.csv",
    "SRC3068_12_1526_variation": RESIDUALS / "P8_Y5_PARENT_QLOC_1526_VARIATION_DERIVATION.csv",
    "SRC3068_13_1526_sign": RESIDUALS / "P8_Y5_PARENT_QLOC_1526_COEFFICIENT_SIGN_CONTRACT.csv",
    "SRC3068_14_1526_symbol_match": RESIDUALS / "P8_Y5_PARENT_QLOC_1526_SYMBOL_MATCH_AUDIT.csv",
    "SRC3068_15_metric_response_contract": RESIDUALS / "P8_GK_METRIC_RESPONSE_CONTRACT.csv",
    "SRC3068_16_metric_response_evidence": RESIDUALS / "P8_GK_METRIC_RESPONSE_SOURCE_EVIDENCE.csv",
    "SRC3068_17_1192_parent_phi": RESIDUALS / "P8_Y5_R10_1192_PARENT_PHI_SOURCE_AUDIT.csv",
    "SRC3068_18_1193_ricci_branch": RESIDUALS / "P8_Y5_R10_1193_RICCI_EXACT_SCALAR_BRANCH.csv",
    "SRC3068_19_2713_rollforward": RESIDUALS / "P8_Y5_R2FR_2713_KL00_PHIR_IMPROVEMENT_ROLLFORWARD.csv",
    "SRC3068_20_2714_lambda_zero": RESIDUALS / "P8_Y5_R2FR_2714_LAMBDA_PHI_ZERO_ATTEMPT.csv",
    "SRC3068_21_1190_tracefree_solver": RESIDUALS / "P8_Y5_R10_1190_TRACEFREE_KHAT_SOLVER_GATE.csv",
    "SRC3068_22_833_amplitude": RESIDUALS / "P8_Y5_R10_833_HESSIAN_KHAT_AMPLITUDE_LAW.csv",
    "SRC3068_23_dotg_target": DOTG_TARGET,
}

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3068_SOURCE_REGISTER.csv",
    "phi_attempt": RESIDUALS / "P8_Y5_R2FR_3068_PHI_OWNER_SOURCE_EQUATION_ATTEMPT.csv",
    "aux_variation": RESIDUALS / "P8_Y5_R2FR_3068_LOCAL_AUXILIARY_ACTION_VARIATION_AUDIT.csv",
    "lambda_stress": RESIDUALS / "P8_Y5_R2FR_3068_LAMBDA_PHI_STRESS_AND_BOUND_ROWS_NONCLAIM.csv",
    "route_decision": RESIDUALS / "P8_Y5_R2FR_3068_TRACEFREE_ROUTE_DECISION_LEDGER.csv",
    "claim_status": RESIDUALS / "P8_Y5_R2FR_3068_CLAIM_STATUS.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_3068_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_3068_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3068_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "phi_attempt_copy": PARENT_ACTION / "phi_owner_source_equation_attempt_3068_NOT_SIGNED.csv",
    "aux_variation_copy": PARENT_ACTION / "local_auxiliary_phi_action_variation_audit_3068_STAGED_NONCLAIM.csv",
    "lambda_stress_copy": LOCAL_BOUNDS / "lambda_phi_stress_bound_rows_3068_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR3068_lambda_phi_silence_or_aux_stress_bound_NEXT_NONCLAIM.csv",
}

for path in list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC]:
    path.parent.mkdir(parents=True, exist_ok=True)


def rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


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


def source_parse_ok(path: Path) -> bool:
    if not path.exists():
        return False
    return csv_ok(path) if path.suffix.lower() == ".csv" else True


def row_count(path: Path) -> int:
    if not path.exists():
        return 0
    if path.suffix.lower() == ".csv":
        return len(rows(path))
    return len(path.read_text(encoding="utf-8").splitlines())


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
            writer.writerow({key: output_row.get(key, "") for key in fieldnames})


def under(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def has_claim_true(input_rows: list[dict[str, Any]]) -> bool:
    claim_fields = {
        "valid_for_claim",
        "claim_allowed",
        "valid_prediction_row",
        "score_ready",
        "claim_active",
        "parent_signed",
        "promote_to_live_khat",
        "local_gr_claim",
        "numeric_ready",
        "bound_ready",
    }
    for row in input_rows:
        for field in claim_fields:
            if field in row and boolish(row[field]):
                return True
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


def md_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def md_table(table_rows: list[dict[str, Any]], columns: list[str]) -> str:
    if not table_rows:
        return "_No rows._"
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    lines = [header, sep]
    for row in table_rows:
        lines.append("| " + " | ".join(md_escape(row.get(column, "")) for column in columns) + " |")
    return "\n".join(lines)


def copy_csv(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dst)


dotg_rows_before = rows(DOTG_TARGET)

source_register = [
    base(
        {
            "source_id": source_id,
            "source_path": str(path),
            "exists": str(path.exists()),
            "parse_ok": str(source_parse_ok(path)),
            "row_count": row_count(path),
            "role": "phi_owner_source_equation_evidence" if source_id != "SRC3068_23_dotg_target" else "append_guard_target",
            "status": "PRESENT" if path.exists() else "MISSING_SOURCE",
        }
    )
    for source_id, path in SOURCE_PATHS.items()
]

phi_attempt_rows = [
    base(
        {
            "attempt_id": "PHI3068_0_nonlocal_inverse_box",
            "route": "phi = Box^{-1} S_Gamma",
            "source_equation": "Box phi = S_Gamma with S_Gamma=(2/3)(Gamma_eff+C)",
            "derivation_status": "FORMAL_SOLVER_EXISTS",
            "parent_signed": "false",
            "promote_to_live_khat": "false",
            "obstruction": "inverse-Box route is nonlocal/closure-only unless the Green function and boundary data are parent-owned",
            "useful_gain": "records the exact source shape required by the flat tracefree cancellation",
            "missing_for_claim": "MISSING_LOCAL_OWNER;MISSING_PARENT_BOUNDARY;MISSING_GREEN_FUNCTION",
            "source_ids": "SRC3068_03_3067_divergence;SRC3068_05_1527_phi_owner_hunt;SRC3068_08_1527_nonlocality",
        }
    ),
    base(
        {
            "attempt_id": "PHI3068_1_local_lambda_auxiliary",
            "route": "local auxiliary lambda_phi constraint",
            "source_equation": "S_phiK=int sqrt(-g)[c_I phi R - nabla_mu lambda_phi nabla^mu phi - lambda_phi S_Gamma]+B_phiK gives Box phi=S_Gamma",
            "derivation_status": "LOCAL_ACTION_CONTRACT_RECONSTRUCTED",
            "parent_signed": "false",
            "promote_to_live_khat": "false",
            "obstruction": "lambda_phi has its own equation and stress; boundary/no-flux silence is unsigned",
            "useful_gain": "this is the least bad local field-theory route because it avoids naked inverse Box",
            "missing_for_claim": "MISSING_PARENT_ADOPTION;MISSING_LAMBDA_STRESS_SILENCE;MISSING_BOUNDARY_NO_FLUX",
            "source_ids": "SRC3068_06_1527_aux_action;SRC3068_07_1527_multiplier_silence;SRC3068_19_2713_rollforward",
        }
    ),
    base(
        {
            "attempt_id": "PHI3068_2_propagating_kinetic_scalar",
            "route": "direct kinetic/source scalar",
            "source_equation": "S_phi=int sqrt(-g)[-(3/4)Z_phi nabla phi nabla phi - phi Gamma_eff] gives (3/2)Z_phi Box phi = Gamma_eff",
            "derivation_status": "POSSIBLE_BUT_CONTAMINATED_PARENT_COMPLETION",
            "parent_signed": "false",
            "promote_to_live_khat": "false",
            "obstruction": "adds a propagating scalar stress and does not by itself identify K_hat as the phi R metric response",
            "useful_gain": "shows the flat source equation is easy to get, but not silently",
            "missing_for_claim": "MISSING_EXTRA_FIELD_SILENCE;MISSING_KHAT_ADOPTION;MISSING_SCALAR_DOF_BOUND",
            "source_ids": "SRC3068_02_3067_birth_gate;SRC3068_09_1527_adoption;SRC3068_22_833_amplitude",
        }
    ),
    base(
        {
            "attempt_id": "PHI3068_3_curved_exact_source",
            "route": "curvature-corrected scalar source",
            "source_equation": "(3/2)Box phi + 2 U_R[phi] = Gamma_eff + C if nabla U_R = R^nu_sigma nabla^sigma phi",
            "derivation_status": "SPECIAL_BRANCH_CONDITION_ONLY",
            "parent_signed": "false",
            "promote_to_live_khat": "false",
            "obstruction": "U_R exists only when the Ricci one-form is exact or a vector/tensor compensator is parent-owned",
            "useful_gain": "identifies the precise curvature correction a real parent equation must carry",
            "missing_for_claim": "MISSING_RICCI_EXACTNESS;MISSING_COMPENSATOR;MISSING_DOMAIN_CLASSIFIER",
            "source_ids": "SRC3068_17_1192_parent_phi;SRC3068_18_1193_ricci_branch",
        }
    ),
]

aux_variation_rows = [
    base(
        {
            "variation_id": "AUXV3068_0_parent_contract",
            "object": "S_phiK",
            "formula": "int sqrt(-g)[c_I phi R - nabla_mu lambda_phi nabla^mu phi - lambda_phi S_Gamma]+B_phiK",
            "variation_result": "local parent-shaped action can encode the flat tracefree source condition",
            "status": "STAGED_CONTRACT_NOT_LIVE_PARENT",
            "missing_for_claim": "MISSING_PARENT_ADOPTION;MISSING_SIGN;MISSING_BOUNDARY_TERM",
            "source_ids": "SRC3068_06_1527_aux_action;SRC3068_12_1526_variation;SRC3068_13_1526_sign",
        }
    ),
    base(
        {
            "variation_id": "AUXV3068_1_delta_lambda",
            "object": "lambda_phi variation",
            "formula": "delta_{lambda_phi} S_phiK=0 => Box phi=S_Gamma",
            "variation_result": "flat source equation is locally generated if boundary flux vanishes",
            "status": "DERIVED_CONDITIONAL",
            "missing_for_claim": "MISSING_BOUNDARY_NO_FLUX;MISSING_ZERO_MODE_REFERENCE",
            "source_ids": "SRC3068_06_1527_aux_action;SRC3068_20_2714_lambda_zero",
        }
    ),
    base(
        {
            "variation_id": "AUXV3068_2_delta_phi",
            "object": "phi variation",
            "formula": "delta_phi S_phiK=0 => Box lambda_phi=-c_I R plus boundary/convention terms",
            "variation_result": "the localizer creates a multiplier equation that must be silent",
            "status": "DERIVED_OBSTRUCTION",
            "missing_for_claim": "MISSING_LAMBDA_PHI_ZERO_THEOREM;MISSING_RICCI_FLAT_PARENT_DOMAIN",
            "source_ids": "SRC3068_06_1527_aux_action;SRC3068_07_1527_multiplier_silence",
        }
    ),
    base(
        {
            "variation_id": "AUXV3068_3_metric_response",
            "object": "metric variation",
            "formula": "delta_g(c_I int sqrt(-g)phi R) gives c_I[phi G_{mu nu}+(g_{mu nu}Box-nabla_mu nabla_nu)phi] plus boundary",
            "variation_result": "tracefree Hessian shape matches K_L only after coefficient/sign, channel routing and phi G_TF control",
            "status": "SHAPE_MATCH_NOT_FULL_IDENTITY",
            "missing_for_claim": "MISSING_SIGMA_RESP_CI_VALUE;MISSING_PHI_G_TF_ROUTE;MISSING_BOUNDARY_RESPONSE",
            "source_ids": "SRC3068_12_1526_variation;SRC3068_13_1526_sign;SRC3068_15_metric_response_contract",
        }
    ),
    base(
        {
            "variation_id": "AUXV3068_4_same_branch_adoption",
            "object": "live Khat adoption",
            "formula": "K_hat^{mu nu}:=TF[sigma_resp c_I metric response of int sqrt(-g)phi R] with sigma_resp*c_I=1",
            "variation_result": "adoption row exists but is not live in the main parent branch",
            "status": "ADOPTION_ROW_STAGED_NONCLAIM",
            "missing_for_claim": "MISSING_LIVE_KHAT_DEFINITION;MISSING_CURRENT_SYMBOL_REWRITE",
            "source_ids": "SRC3068_09_1527_adoption;SRC3068_14_1526_symbol_match",
        }
    ),
]

lambda_stress_rows = [
    base(
        {
            "row_id": "LPS3068_0_total_aux_stress",
            "quantity": "T_lambda_phi_TF",
            "definition": "tracefree metric response of -nabla lambda_phi dot nabla phi - lambda_phi S_Gamma plus boundary terms",
            "bound_expression": "||T_lambda_phi_TF|| <= C_grad||nabla lambda_phi||||nabla phi|| + |lambda_phi| ||delta_g S_Gamma|| + boundary_flux",
            "symbolic_value": "MISSING_LAMBDA_ZERO_OR_NUMERIC_BOUND",
            "status": "RETAINED_NONCLAIM_BOUND_ROW",
            "numeric_ready": "false",
            "bound_ready": "false",
            "missing_for_claim": "MISSING_LAMBDA_PHI_ZERO;MISSING_DELTA_G_SGAMMA_BOUND;MISSING_BOUNDARY_FLUX_BOUND",
            "source_ids": "SRC3068_07_1527_multiplier_silence;SRC3068_20_2714_lambda_zero",
        }
    ),
    base(
        {
            "row_id": "LPS3068_1_Ricci_flat_lambda_equation",
            "quantity": "lambda_phi",
            "definition": "Box lambda_phi=-c_I R",
            "bound_expression": "if R=0 and parent boundary/zero-mode gives lambda_phi=0 then T_lambda_phi=0",
            "symbolic_value": "MISSING_PARENT_RICCI_FLAT_DOMAIN_AND_BOUNDARY",
            "status": "CONDITIONAL_ZERO_ROUTE_UNSIGNED",
            "numeric_ready": "false",
            "bound_ready": "false",
            "missing_for_claim": "MISSING_RICCI_FLAT_PARENT_DOMAIN;MISSING_DIRICHLET_OR_NO_FLUX;MISSING_ZERO_MODE_FIX",
            "source_ids": "SRC3068_07_1527_multiplier_silence;SRC3068_20_2714_lambda_zero",
        }
    ),
    base(
        {
            "row_id": "LPS3068_2_generic_Ricci_source",
            "quantity": "R_source_to_lambda_phi",
            "definition": "nonzero Ricci scalar sources lambda_phi in matter/cosmology domains",
            "bound_expression": "||lambda_phi|| <= ||G_R * c_I R|| plus boundary data",
            "symbolic_value": "MISSING_GREEN_BOUND_FOR_R_SOURCE",
            "status": "GENERIC_DOMAIN_BOUND_REQUIRED",
            "numeric_ready": "false",
            "bound_ready": "false",
            "missing_for_claim": "MISSING_GREEN_OPERATOR_NORM;MISSING_R_SOURCE_BOUND;MISSING_ARENA_PROJECTION",
            "source_ids": "SRC3068_17_1192_parent_phi;SRC3068_18_1193_ricci_branch",
        }
    ),
    base(
        {
            "row_id": "LPS3068_3_boundary_flux",
            "quantity": "B_phiK_flux",
            "definition": "boundary contribution from integrations by parts in the local auxiliary action",
            "bound_expression": "|B_phiK_flux| <= boundary_norm(lambda_phi,phi,n,gamma)",
            "symbolic_value": "MISSING_PARENT_BOUNDARY_DATA",
            "status": "BOUNDARY_INPUT_REQUIRED",
            "numeric_ready": "false",
            "bound_ready": "false",
            "missing_for_claim": "MISSING_BOUNDARY_TERM;MISSING_LOCAL_COLLAR;MISSING_PROJECTOR_SILENCE",
            "source_ids": "SRC3068_08_1527_nonlocality;SRC3068_13_1526_sign",
        }
    ),
]

route_decision_rows = [
    base(
        {
            "decision_id": "TRD3068_0_phi_owner_status",
            "question": "Did 3068 derive a parent-owned phi source equation?",
            "answer": "PARTIAL_CONDITIONAL",
            "reason": "a local auxiliary contract generates Box phi=S_Gamma, but it is staged not parent-adopted and creates lambda_phi obligations",
            "route_status": "RETAIN_AS_CONDITIONAL_AUXILIARY_BRANCH",
            "next_action": "prove lambda_phi stress silence or keep auxiliary stress as an explicit DeltaK_TF/q_loc bound",
        }
    ),
    base(
        {
            "decision_id": "TRD3068_1_tracefree_route",
            "question": "Should tracefree K_L be demoted completely?",
            "answer": "NO_NOT_COMPLETELY",
            "reason": "the local auxiliary route is better than closure-only inverse Box, so the route deserves one more targeted silence proof",
            "route_status": "NOT_PROMOTED_NOT_DEAD",
            "next_action": "attack lambda_phi zero theorem from Box lambda_phi=-c_I R plus boundary/zero-mode",
        }
    ),
    base(
        {
            "decision_id": "TRD3068_2_local_GR_claim",
            "question": "Can local GR be claimed after 3068?",
            "answer": "NO",
            "reason": "Khat adoption, lambda stress, Ricci exactness, boundary silence and amplitude readout remain open",
            "route_status": "CLAIM_BLOCKED",
            "next_action": "3069 should either close lambda_phi silence or generate a sourced auxiliary-stress bound ledger",
        }
    ),
]

claim_rows = [
    base(
        {
            "claim_id": "CLAIM3068_0_phi_parent_owned",
            "claim": "phi is parent-owned in current MTS",
            "status": "NO_STAGED_CONTRACT_ONLY",
            "claim_active": "false",
            "reason": "local auxiliary action is reconstructed from prior contracts but not live-adopted",
        }
    ),
    base(
        {
            "claim_id": "CLAIM3068_1_lambda_stress_silent",
            "claim": "lambda_phi stress is theorem-zero",
            "status": "NO_UNSIGNED_BOUNDARY_AND_RICCI_DOMAIN",
            "claim_active": "false",
            "reason": "Box lambda_phi=-c_I R only gives a zero route in Ricci-flat domains with signed zero boundary data",
        }
    ),
    base(
        {
            "claim_id": "CLAIM3068_2_Khat_live_adopted",
            "claim": "tracefree K_L is live MTS K_hat",
            "status": "NO_ADOPTION_STAGED_ONLY",
            "claim_active": "false",
            "reason": "same-branch Khat adoption and coefficient/sign remain nonclaim",
        }
    ),
    base(
        {
            "claim_id": "CLAIM3068_3_local_GR_PPN",
            "claim": "local GR/PPN branch is derived",
            "status": "NO",
            "claim_active": "false",
            "reason": "auxiliary stress and DeltaK_TF remain live residuals",
        }
    ),
]

next_rows = [
    base(
        {
            "next_id": "NEXT3068_0_3069",
            "next_checkpoint": "3069-Y5-R2FR-lambda-phi-silence-theorem-or-auxiliary-stress-bound-under-AX1090.md",
            "script": "scripts/Y5_R2FR_lambda_phi_silence_theorem_or_auxiliary_stress_bound_under_AX1090_3069.py",
            "mission": "prove lambda_phi stress silence from Box lambda_phi=-c_I R plus parent boundary/zero-mode data, or retain it as an explicit auxiliary-stress bound feeding DeltaK_TF and q_loc",
            "starting_equation": "Box lambda_phi=-c_I R; in Ricci-flat local vacuum lambda_phi is harmonic, but lambda_phi=0 needs parent-signed boundary/no-flux and zero-mode conditions",
            "claim_policy": "no local-GR or Khat claim unless lambda_phi stress is theorem-zero or bounded below local PPN/R10/clock/orbital limits",
        }
    )
]

write_csv(OUTPUTS["sources"], source_register)
write_csv(OUTPUTS["phi_attempt"], phi_attempt_rows)
write_csv(OUTPUTS["aux_variation"], aux_variation_rows)
write_csv(OUTPUTS["lambda_stress"], lambda_stress_rows)
write_csv(OUTPUTS["route_decision"], route_decision_rows)
write_csv(OUTPUTS["claim_status"], claim_rows)
write_csv(OUTPUTS["next"], next_rows)

copy_csv(OUTPUTS["phi_attempt"], BRANCH_OUTPUTS["phi_attempt_copy"])
copy_csv(OUTPUTS["aux_variation"], BRANCH_OUTPUTS["aux_variation_copy"])
copy_csv(OUTPUTS["lambda_stress"], BRANCH_OUTPUTS["lambda_stress_copy"])
copy_csv(OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"])

branch_rows = [
    base(
        {
            "copy_id": copy_id,
            "destination": str(path),
            "exists": str(path.exists()),
            "row_count": row_count(path),
            "description": "3068 branch copy for parent-action/local-bound/acquisition-queue continuity",
        }
    )
    for copy_id, path in BRANCH_OUTPUTS.items()
]
write_csv(OUTPUTS["branches"], branch_rows)

generated_paths = list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC]
non_validation_csv_paths = [path for path in list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) if path != OUTPUTS["validation"]]
all_output_rows: list[dict[str, Any]] = []
for output_path in non_validation_csv_paths:
    all_output_rows.extend(rows(output_path))

dotg_rows_after = rows(DOTG_TARGET)
formalization_generated_hits = [path for path in generated_paths if under(path, FORMALIZATION)]

all_sources_exist = all(boolish(row["exists"]) for row in source_register)
all_sources_parse = all(boolish(row["parse_ok"]) for row in source_register)
nonlocal_rejected = any(row["attempt_id"] == "PHI3068_0_nonlocal_inverse_box" and row["parent_signed"] == "false" for row in phi_attempt_rows)
local_aux_reconstructed = any(row["attempt_id"] == "PHI3068_1_local_lambda_auxiliary" and row["derivation_status"] == "LOCAL_ACTION_CONTRACT_RECONSTRUCTED" for row in phi_attempt_rows)
all_phi_attempts_nonclaim = all(row["parent_signed"] == "false" and row["promote_to_live_khat"] == "false" for row in phi_attempt_rows)
lambda_variation_present = any(row["variation_id"] == "AUXV3068_1_delta_lambda" and "Box phi=S_Gamma" in row["formula"] for row in aux_variation_rows)
phi_variation_obstruction = any(row["variation_id"] == "AUXV3068_2_delta_phi" and "lambda_phi" in row["formula"] for row in aux_variation_rows)
metric_shape_guarded = any(row["variation_id"] == "AUXV3068_3_metric_response" and row["status"] == "SHAPE_MATCH_NOT_FULL_IDENTITY" for row in aux_variation_rows)
all_lambda_bounds_nonclaim = all(
    row["numeric_ready"] == "false"
    and row["bound_ready"] == "false"
    and row["valid_for_claim"] == "false"
    and "MISSING" in row["symbolic_value"]
    for row in lambda_stress_rows
)
route_retained_not_promoted = any(row["decision_id"] == "TRD3068_1_tracefree_route" and row["answer"] == "NO_NOT_COMPLETELY" for row in route_decision_rows)
all_claims_inactive = all(row["claim_active"] == "false" for row in claim_rows)
next_is_3069 = next_rows[0]["next_checkpoint"].startswith("3069-")

if PYCACHE.exists():
    shutil.rmtree(PYCACHE)

validation_rows = [
    base({"validation_id": "VAL3068_00_sources_exist", "passed": all_sources_exist, "requirement": "all cited source paths exist", "evidence": OUTPUTS["sources"].name}),
    base({"validation_id": "VAL3068_01_sources_parse", "passed": all_sources_parse, "requirement": "all cited CSV sources parse and markdown sources exist", "evidence": OUTPUTS["sources"].name}),
    base({"validation_id": "VAL3068_02_csv_parse", "passed": all(csv_ok(path) for path in non_validation_csv_paths), "requirement": "all generated and branch-copy CSVs parse cleanly", "evidence": "csv.DictReader parse check"}),
    base({"validation_id": "VAL3068_03_nonlocal_rejected", "passed": nonlocal_rejected, "requirement": "inverse-Box phi route is rejected for local field-theory claim", "evidence": OUTPUTS["phi_attempt"].name}),
    base({"validation_id": "VAL3068_04_local_aux_reconstructed_nonclaim", "passed": local_aux_reconstructed and all_phi_attempts_nonclaim, "requirement": "local auxiliary phi source equation is reconstructed but not parent-signed", "evidence": OUTPUTS["phi_attempt"].name}),
    base({"validation_id": "VAL3068_05_variation_equations_present", "passed": lambda_variation_present and phi_variation_obstruction and metric_shape_guarded, "requirement": "delta lambda, delta phi and metric-response audits are recorded with guards", "evidence": OUTPUTS["aux_variation"].name}),
    base({"validation_id": "VAL3068_06_lambda_stress_nonclaim", "passed": all_lambda_bounds_nonclaim, "requirement": "lambda_phi stress rows are missing-input nonclaim bounds", "evidence": OUTPUTS["lambda_stress"].name}),
    base({"validation_id": "VAL3068_07_route_retained_not_promoted", "passed": route_retained_not_promoted, "requirement": "tracefree route is retained as conditional auxiliary branch but not promoted", "evidence": OUTPUTS["route_decision"].name}),
    base({"validation_id": "VAL3068_08_claims_inactive", "passed": all_claims_inactive and not has_claim_true(all_output_rows), "requirement": "no generated row activates Khat, q_loc, local-GR, R10, PPN, clock or orbital claims", "evidence": OUTPUTS["claim_status"].name}),
    base({"validation_id": "VAL3068_09_dotg_no_placeholder_append", "passed": dotg_rows_before == dotg_rows_after and not any("3068" in row.get("row_id", "") for row in dotg_rows_after), "requirement": "3068 does not append placeholder dotG rows", "evidence": str(DOTG_TARGET)}),
    base({"validation_id": "VAL3068_10_branch_copies", "passed": all(path.exists() and csv_ok(path) for path in BRANCH_OUTPUTS.values()), "requirement": "branch copies exist and parse", "evidence": OUTPUTS["branches"].name}),
    base({"validation_id": "VAL3068_11_output_scope", "passed": all(under(path, ROOT) for path in generated_paths), "requirement": "all generated outputs are inside post-checkpoint-work", "evidence": str(ROOT)}),
    base({"validation_id": "VAL3068_12_formalization_untouched", "passed": len(formalization_generated_hits) == 0, "requirement": "formalization-workbench generated-output count remains 0", "evidence": f"generated outputs under formalization={len(formalization_generated_hits)}"}),
    base({"validation_id": "VAL3068_13_next_target", "passed": next_is_3069, "requirement": "next target selects lambda_phi silence theorem or auxiliary stress bound", "evidence": OUTPUTS["next"].name}),
    base({"validation_id": "VAL3068_14_pycache_removed", "passed": not PYCACHE.exists(), "requirement": "scripts __pycache__ removed", "evidence": str(PYCACHE)}),
]
write_csv(OUTPUTS["validation"], validation_rows)

doc_text = f"""# 3068 - Phi Owner Source Equation or Tracefree Route Demotion

Status: `Y5_R2FR_3068_phi_source_local_auxiliary_contract_reconstructed_lambda_stress_blocks_claim`

Generated: `{RUN_UTC}`

## Verdict

3068 tried to turn the tracefree `K_L` route from a formal solver into a parent-owned field-theory mechanism.

The useful result is that the route is **not merely inverse-box magic**. A local auxiliary parent-shaped contract exists:

`S_phiK = int sqrt(-g)[c_I phi R - nabla_mu lambda_phi nabla^mu phi - lambda_phi S_Gamma] + B_phiK`

with

`S_Gamma = (2/3)(Gamma_eff + C)`.

The `lambda_phi` variation gives the desired flat-patch source equation:

`Box phi = S_Gamma`.

That is real progress for the derivation route. But the price is also real: the `phi` variation gives

`Box lambda_phi = -c_I R`

up to convention and boundary terms, so `lambda_phi` carries stress unless a same-parent Ricci-flat/domain/boundary theorem kills it or bounds it.

Therefore 3068 does **not** promote `K_L` to live `K_hat`, does **not** set `DeltaK_TF=0`, and does **not** claim local GR/PPN. The tracefree route is retained as a conditional auxiliary branch, not demoted to pure closure-only yet.

## Phi Owner Source Equation Attempts

{md_table(phi_attempt_rows, ["attempt_id", "route", "derivation_status", "parent_signed", "obstruction", "useful_gain"])}

## Local Auxiliary Action Variation Audit

{md_table(aux_variation_rows, ["variation_id", "object", "formula", "variation_result", "status", "missing_for_claim"])}

## Lambda Phi Stress and Bound Rows

{md_table(lambda_stress_rows, ["row_id", "quantity", "definition", "bound_expression", "symbolic_value", "status", "numeric_ready", "bound_ready"])}

## Tracefree Route Decision Ledger

{md_table(route_decision_rows, ["decision_id", "question", "answer", "reason", "route_status", "next_action"])}

## Claim Status

{md_table(claim_rows, ["claim_id", "claim", "status", "claim_active", "reason"])}

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

if PYCACHE.exists():
    shutil.rmtree(PYCACHE)

failures = [row for row in validation_rows if not boolish(row["passed"])]
if failures:
    raise SystemExit(f"3068 validation failed: {[row['validation_id'] for row in failures]}")

print(f"wrote {DOC}")
print(f"validation rows: {len(validation_rows)} passed")
print("claim status: phi source equation locally reconstructed but not parent-signed; lambda_phi stress blocks local-GR promotion")
