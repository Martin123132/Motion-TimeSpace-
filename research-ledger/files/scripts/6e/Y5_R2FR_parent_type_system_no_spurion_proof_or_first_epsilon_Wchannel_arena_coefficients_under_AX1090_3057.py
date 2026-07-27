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

CHECKPOINT = "3057"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "3057-Y5-R2FR-parent-type-system-no-spurion-proof-or-first-epsilon-Wchannel-arena-coefficients-under-AX1090.md"
DOTG_TARGET = RESIDUALS / "P8_time_drift_residual_or_zero.csv"

SOURCE_PATHS = {
    "SRC3057_00_3056_doc": ROOT / "3056-Y5-R2FR-typed-no-source-prefactor-grammar-or-epsilon-Wchannel-bound-schema-under-AX1090.md",
    "SRC3057_01_3056_typed_grammar": RESIDUALS / "P8_Y5_R2FR_3056_TYPED_NO_SOURCE_PREFACTOR_GRAMMAR_ATTEMPT.csv",
    "SRC3057_02_3056_gates": RESIDUALS / "P8_Y5_R2FR_3056_GRAMMAR_GATE_EVALUATION.csv",
    "SRC3057_03_3056_bound_schema": RESIDUALS / "P8_Y5_R2FR_3056_EPSILON_WCHANNEL_BOUND_SCHEMA.csv",
    "SRC3057_04_3056_arena_req": RESIDUALS / "P8_Y5_R2FR_3056_LOCAL_ARENA_PROJECTION_REQUIREMENTS.csv",
    "SRC3057_05_3056_next": RESIDUALS / "P8_Y5_R2FR_3056_NEXT_TARGET.csv",
    "SRC3057_06_3055_epsilon": RESIDUALS / "P8_Y5_R2FR_3055_EPSILON_WCHANNEL_RESIDUAL_CONTRACT.csv",
    "SRC3057_07_3039_delta_A": RESIDUALS / "P8_Y5_R2FR_3039_DELTA_A_PREFACTOR_RESIDUAL_CONTRACT.csv",
    "SRC3057_08_3039_relative_weight": PARENT_ACTION / "relative_source_vertex_weight_theorem_3039_NOT_SIGNED.csv",
    "SRC3057_09_3038_derivative_audit": PARENT_ACTION / "functional_derivative_match_audit_3038_NONCLAIM.csv",
    "SRC3057_10_2645_clause": RESIDUALS / "P8_Y5_NO_SOURCE_PREFACTOR_2645_PARENT_ACTION_CLAUSE_ATTEMPT.csv",
    "SRC3057_11_2645_claim_gates": RESIDUALS / "P8_Y5_NO_SOURCE_PREFACTOR_2645_CLAIM_GATES.csv",
    "SRC3057_12_2587_action_contract": RESIDUALS / "P8_Y5_MIN_PARENT_MATTER_2587_ACTION_CONTRACT.csv",
    "SRC3057_13_2587_countermodels": RESIDUALS / "P8_Y5_MIN_PARENT_MATTER_2587_COUNTERMODEL_TESTS.csv",
    "SRC3057_14_3054_w_owner": RESIDUALS / "P8_Y5_R2FR_3054_W_PARENT_OWNER_CLAUSE.csv",
    "SRC3057_15_3050_gref": RESIDUALS / "P8_Y5_R2FR_3050_GREF_LOCK_AND_AW_NORMALIZATION_AUDIT.csv",
    "SRC3057_16_dotg_target": DOTG_TARGET,
}

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3057_SOURCE_REGISTER.csv",
    "type_contract": RESIDUALS / "P8_Y5_R2FR_3057_PARENT_TYPE_SYSTEM_CONTRACT.csv",
    "no_spurion": RESIDUALS / "P8_Y5_R2FR_3057_NO_SPURION_PROOF_ATTEMPT.csv",
    "first_coefficients": RESIDUALS / "P8_Y5_R2FR_3057_FIRST_K_EPSILON_COEFFICIENTS.csv",
    "arena_status": RESIDUALS / "P8_Y5_R2FR_3057_ARENA_COEFFICIENT_STATUS.csv",
    "claim_status": RESIDUALS / "P8_Y5_R2FR_3057_CLAIM_STATUS.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_3057_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_3057_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_3057_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3057_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "type_contract_copy": PARENT_ACTION / "parent_type_system_contract_3057_NOT_SIGNED.csv",
    "no_spurion_copy": PARENT_ACTION / "no_spurion_proof_attempt_3057_NOT_SIGNED.csv",
    "first_coefficients_copy": LOCAL_BOUNDS / "first_K_epsilon_coefficients_3057_INTERNAL_NONCLAIM.csv",
    "arena_status_copy": LOCAL_BOUNDS / "epsilon_Wchannel_arena_coefficient_status_3057_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR3057_EPSILON_SOURCE_NORM_TO_PPN_OR_TYPE_SYSTEM_NEXT_NONCLAIM.csv",
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


def has_claim_true(input_rows: list[dict[str, str] | dict[str, Any]]) -> bool:
    claim_fields = {
        "valid_for_claim",
        "claim_allowed",
        "valid_prediction_row",
        "score_ready",
        "claim_active",
        "signed_for_current_MTS",
        "proof_closes_current_MTS",
        "arena_ready",
    }
    return any(boolish(row.get(field, "false")) for row in input_rows for field in claim_fields)


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


def copy_csv(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dst)


dotg_rows_before = rows(DOTG_TARGET)

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

type_contract_rows = [
    base(
        {
            "type_id": "TYPE3057_0_parent_fields",
            "type_object": "Phi",
            "allowed_role": "parent geometric/dynamical fields",
            "forbidden_role": "matter source class label",
            "rule": "Phi may enter matter only through q(Phi) and observed stack maps",
            "current_status": "CONTRACT_ONLY",
            "signed_for_current_MTS": "false",
            "missing_for_claim": "MISSING_Q_STACK_OWNER",
        }
    ),
    base(
        {
            "type_id": "TYPE3057_1_observed_stack",
            "type_object": "q(Phi)->g_obs,e_obs,mu_obs,D_obs,tau_obs",
            "allowed_role": "universal readout input to S_matter",
            "forbidden_role": "source-dependent or channel-dependent shadow frame",
            "rule": "ordinary matter sees one observed stack before variation",
            "current_status": "CONTRACT_ONLY",
            "signed_for_current_MTS": "false",
            "missing_for_claim": "MISSING_SINGLE_OBSERVED_STACK_THEOREM",
        }
    ),
    base(
        {
            "type_id": "TYPE3057_2_matter_fields",
            "type_object": "psi_A,theta_A",
            "allowed_role": "ordinary matter and fixed material parameters",
            "forbidden_role": "dynamic source/readout weighting spurion",
            "rule": "theta_A can distinguish material equations of state, not local gravitational source-channel weights",
            "current_status": "NEEDS_NO_SPURION_RULE",
            "signed_for_current_MTS": "false",
            "missing_for_claim": "MISSING_THETA_A_SCOPE_RULE",
        }
    ),
    base(
        {
            "type_id": "TYPE3057_3_readout_labels",
            "type_object": "H_label,W_label",
            "allowed_role": "diagnostic labels introduced after variation for bookkeeping",
            "forbidden_role": "arguments of S_matter or parent source vertices",
            "rule": "readout labels cannot type a_H or a_W before Hilbert variation",
            "current_status": "RULE_WRITTEN_NOT_PARENT_SIGNED",
            "signed_for_current_MTS": "false",
            "missing_for_claim": "MISSING_NO_READOUT_LABEL_IN_ACTION_THEOREM",
        }
    ),
    base(
        {
            "type_id": "TYPE3057_4_spurion",
            "type_object": "sigma_H,sigma_W,sigma_source",
            "allowed_role": "none in ordinary matter source action",
            "forbidden_role": "restore a_H/a_W as hidden typed couplings",
            "rule": "no source/readout spurion exists in the parent grammar",
            "current_status": "MISSING_THEOREM",
            "signed_for_current_MTS": "false",
            "missing_for_claim": "MISSING_NO_SPURION_EXISTENCE_PROOF",
        }
    ),
]

no_spurion_rows = [
    base(
        {
            "proof_id": "NSP3057_0_assume_type_system",
            "claim_piece": "no-spurion theorem assumptions",
            "statement": "Assume the only inputs to ordinary matter are psi_A, theta_A and q(Phi)-owned observed stack objects.",
            "proof_step": "then H/W/source labels are not in the domain of S_matter",
            "result": "ASSUMPTION_EXPLICIT",
            "current_status": "NOT_PARENT_SIGNED",
            "proof_closes_current_MTS": "false",
            "missing_for_claim": "MISSING_PARENT_TYPE_SYSTEM_ADOPTION",
            "source_path": str(SOURCE_PATHS["SRC3057_12_2587_action_contract"]),
        }
    ),
    base(
        {
            "proof_id": "NSP3057_1_untypability",
            "claim_piece": "a_W/a_H untypeability",
            "statement": "a_H and a_W require H/W labels or spurions as arguments; those labels are not available before variation.",
            "proof_step": "therefore the parent expression rho(a_H psi_N+a_W chi_W) is ill-typed as a parent source action",
            "result": "VALID_IF_TYPE_SYSTEM_ASSUMED",
            "current_status": "CONDITIONAL_ONLY",
            "proof_closes_current_MTS": "false",
            "missing_for_claim": "MISSING_NO_READOUT_LABEL_IN_ACTION_THEOREM",
            "source_path": str(SOURCE_PATHS["SRC3057_01_3056_typed_grammar"]),
        }
    ),
    base(
        {
            "proof_id": "NSP3057_2_after_variation",
            "claim_piece": "diagnostic readout allowed after Hilbert source exists",
            "statement": "After T_obs is formed, psi_N and chi_W may be used as diagnostic weak-field coordinates but cannot introduce new source vertices.",
            "proof_step": "readout maps can pull back the same source pairing, but cannot create relative source weights",
            "result": "DERIVED_CONDITIONALLY",
            "current_status": "VARIATION_BEFORE_READOUT_UNSIGNED",
            "proof_closes_current_MTS": "false",
            "missing_for_claim": "MISSING_VARIATION_ORDER_THEOREM",
            "source_path": str(SOURCE_PATHS["SRC3057_06_3055_epsilon"]),
        }
    ),
    base(
        {
            "proof_id": "NSP3057_3_countermodel",
            "claim_piece": "surviving spurion countermodel",
            "statement": "If sigma_W is allowed as a source/readout spurion, then a_W/a_H is typeable and epsilon_Wchan can be nonzero.",
            "proof_step": "the current corpus has not forbidden sigma_W as a typed object",
            "result": "COUNTERMODEL_SURVIVES",
            "current_status": "NOT_PROVED",
            "proof_closes_current_MTS": "false",
            "missing_for_claim": "MISSING_NO_SPURION_EXISTENCE_PROOF",
            "source_path": str(SOURCE_PATHS["SRC3057_11_2645_claim_gates"]),
        }
    ),
    base(
        {
            "proof_id": "NSP3057_4_verdict",
            "claim_piece": "3057 no-spurion verdict",
            "statement": "The no-spurion proof is mathematically clean once the type system is assumed, but the type system is not yet derived from MTS parent fields.",
            "proof_step": "do not promote epsilon_Wchan=0",
            "result": "CONDITIONAL_NOT_SIGNED",
            "current_status": "BOUND_OR_PARENT_TYPE_PROOF_STILL_REQUIRED",
            "proof_closes_current_MTS": "false",
            "missing_for_claim": "MISSING_PARENT_TYPE_SYSTEM_DERIVATION",
            "source_path": str(SOURCE_PATHS["SRC3057_02_3056_gates"]),
        }
    ),
]

first_coefficient_rows = [
    base(
        {
            "coefficient_id": "KEPS3057_0_internal_source_norm",
            "coefficient": "K_epsilon_source_norm",
            "value": "1",
            "units": "dimensionless",
            "derivation": "By definition epsilon_Wchan is the multiplicative relative W/H source-channel mismatch; at first order delta_A_source receives +epsilon_Wchan before R_lock/operator terms.",
            "projection_formula": "delta_A_source = epsilon_Wchan + R_lock + Delta_operator_pullback + higher_order",
            "arena": "internal_local_Newton_source_normalization",
            "current_status": "INTERNAL_COEFFICIENT_DERIVED_NONCLAIM",
            "valid_prediction_row": "false",
            "valid_for_claim": "false",
            "blocker": "R_lock/operator pullback and physical arena map still open",
            "source_path": str(SOURCE_PATHS["SRC3057_07_3039_delta_A"]),
        }
    ),
    base(
        {
            "coefficient_id": "KEPS3057_1_effective_G_source",
            "coefficient": "K_epsilon_Gsource",
            "value": "1_if_WPhi_Gref_Hilbert_gates_pass",
            "units": "dimensionless",
            "derivation": "A pure source-normalization mismatch rescales the local Newton source coefficient at first order if all readout denominators are already locked.",
            "projection_formula": "Delta G_source/G_ref = epsilon_Wchan + residuals",
            "arena": "conditional_local_Newton_G_source",
            "current_status": "CONDITIONAL_NOT_ARENA_READY",
            "valid_prediction_row": "false",
            "valid_for_claim": "false",
            "blocker": "W/Phi/Gref/Hilbert gates are not all signed",
            "source_path": str(SOURCE_PATHS["SRC3057_15_3050_gref"]),
        }
    ),
    base(
        {
            "coefficient_id": "KEPS3057_2_ppn_placeholder",
            "coefficient": "K_epsilon_PPN",
            "value": "MISSING_PPN_METRIC_EXPANSION",
            "units": "dimensionless",
            "derivation": "requires mapping source-normalization residual into gamma,beta and gauge-fixed metric coefficients",
            "projection_formula": "Delta_PPN = K_epsilon_PPN*epsilon_Wchan",
            "arena": "PPN",
            "current_status": "MISSING_ARENA_COEFFICIENT",
            "valid_prediction_row": "false",
            "valid_for_claim": "false",
            "blocker": "PPN expansion not derived",
            "source_path": str(SOURCE_PATHS["SRC3057_03_3056_bound_schema"]),
        }
    ),
    base(
        {
            "coefficient_id": "KEPS3057_3_R10_placeholder",
            "coefficient": "K_epsilon_R10(lambda)",
            "value": "MISSING_SHORT_RANGE_PROFILE",
            "units": "dimensionless",
            "derivation": "requires a finite-range source-channel profile; epsilon_Wchan alone is a normalization residual, not a lambda-profile",
            "projection_formula": "alpha_pred(lambda)=K_epsilon_R10(lambda)*epsilon_Wchan",
            "arena": "R10",
            "current_status": "MISSING_ARENA_COEFFICIENT",
            "valid_prediction_row": "false",
            "valid_for_claim": "false",
            "blocker": "no lambda profile/source projection",
            "source_path": str(SOURCE_PATHS["SRC3057_03_3056_bound_schema"]),
        }
    ),
]

arena_status_rows = [
    base(
        {
            "arena_id": "ASTAT3057_0_internal_source",
            "arena": "internal local Newton source normalization",
            "coefficient_status": "FIRST_INTERNAL_K_DERIVED",
            "usable_for_claim": "false",
            "reason": "K=1 is internal bookkeeping; physical arena residuals still need R_lock/operator/readout maps",
        }
    ),
    base(
        {
            "arena_id": "ASTAT3057_1_ppn",
            "arena": "PPN",
            "coefficient_status": "MISSING",
            "usable_for_claim": "false",
            "reason": "requires gauge-fixed PPN expansion",
        }
    ),
    base(
        {
            "arena_id": "ASTAT3057_2_R10",
            "arena": "R10",
            "coefficient_status": "MISSING",
            "usable_for_claim": "false",
            "reason": "requires finite-range lambda profile and real bound curve",
        }
    ),
    base(
        {
            "arena_id": "ASTAT3057_3_WEP_clock_orbit",
            "arena": "WEP/clock/orbit",
            "coefficient_status": "MISSING",
            "usable_for_claim": "false",
            "reason": "requires material basis, clock readout and GM denominator maps",
        }
    ),
]

claim_rows = [
    base(
        {
            "claim_id": "CLAIM3057_0_no_spurion",
            "claim": "no source/readout spurion can type a_W/a_H in current MTS",
            "status": "NO_CONDITIONAL_ONLY",
            "claim_active": "false",
            "reason": "type-system proof is clean only as an assumed contract",
        }
    ),
    base(
        {
            "claim_id": "CLAIM3057_1_epsilon_zero",
            "claim": "epsilon_Wchan=0",
            "status": "NO_NOT_SIGNED",
            "claim_active": "false",
            "reason": "surviving sigma_W countermodel not eliminated",
        }
    ),
    base(
        {
            "claim_id": "CLAIM3057_2_first_K",
            "claim": "first physical arena coefficient is claim-ready",
            "status": "NO_INTERNAL_ONLY",
            "claim_active": "false",
            "reason": "K=1 is internal delta_A_source coefficient, not PPN/R10/WEP/clock/orbit coefficient",
        }
    ),
    base(
        {
            "claim_id": "CLAIM3057_3_local_GR",
            "claim": "local GR/Newton source branch is derived",
            "status": "NO_NOT_YET",
            "claim_active": "false",
            "reason": "source-channel theorem and arena maps remain incomplete",
        }
    ),
]

decision_rows = [
    base(
        {
            "decision_id": "DEC3057_0_no_spurion",
            "question": "Can 3057 close the no-spurion theorem?",
            "answer": "NO",
            "reason": "the proof works if the parent type system is assumed, but that type system is not derived from MTS core variables",
            "action": "keep epsilon_Wchan nonzero-or-bound residual live",
        }
    ),
    base(
        {
            "decision_id": "DEC3057_1_coefficient",
            "question": "Did 3057 derive any K_epsilon coefficient?",
            "answer": "YES_INTERNAL_ONLY",
            "reason": "delta_A_source receives epsilon_Wchan with coefficient one by definition of the residual",
            "action": "use K_epsilon_source_norm=1 as internal bridge, not as empirical pass",
        }
    ),
    base(
        {
            "decision_id": "DEC3057_2_next",
            "question": "Best next target?",
            "answer": "MAP_INTERNAL_K_TO_PPN_OR_PROVE_TYPE_SYSTEM",
            "reason": "either derive the parent type system, or project the internal source residual into the first physical arena",
            "action": "build 3058 PPN source-normalization projection or parent type-system derivation",
        }
    ),
]

next_rows = [
    base(
        {
            "next_id": "NEXT3057_0_3058",
            "next_checkpoint": "3058-Y5-R2FR-epsilon-Wchannel-source-normalization-to-PPN-projection-or-parent-type-system-derivation-under-AX1090.md",
            "script": "scripts/Y5_R2FR_epsilon_Wchannel_source_normalization_to_PPN_projection_or_parent_type_system_derivation_under_AX1090_3058.py",
            "mission": "try to map K_epsilon_source_norm=1 into a gauge-fixed PPN/local Newton residual; if that fails, return to deriving the parent type system/no-spurion rule",
            "starting_equation": "delta_A_source = epsilon_Wchan + R_lock + Delta_operator_pullback + higher_order",
            "claim_policy": "no empirical/local-GR claim until physical arena coefficients and residual bounds are sourced",
        }
    )
]

write_csv(OUTPUTS["sources"], source_register)
write_csv(OUTPUTS["type_contract"], type_contract_rows)
write_csv(OUTPUTS["no_spurion"], no_spurion_rows)
write_csv(OUTPUTS["first_coefficients"], first_coefficient_rows)
write_csv(OUTPUTS["arena_status"], arena_status_rows)
write_csv(OUTPUTS["claim_status"], claim_rows)
write_csv(OUTPUTS["decision"], decision_rows)
write_csv(OUTPUTS["next"], next_rows)

copy_csv(OUTPUTS["type_contract"], BRANCH_OUTPUTS["type_contract_copy"])
copy_csv(OUTPUTS["no_spurion"], BRANCH_OUTPUTS["no_spurion_copy"])
copy_csv(OUTPUTS["first_coefficients"], BRANCH_OUTPUTS["first_coefficients_copy"])
copy_csv(OUTPUTS["arena_status"], BRANCH_OUTPUTS["arena_status_copy"])
copy_csv(OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"])

branch_rows = [
    base(
        {
            "copy_id": copy_id,
            "destination": str(path),
            "exists": path.exists(),
            "row_count": len(rows(path)) if path.exists() else 0,
            "description": "3057 branch copy",
        }
    )
    for copy_id, path in BRANCH_OUTPUTS.items()
]
write_csv(OUTPUTS["branches"], branch_rows)

if PYCACHE.exists():
    shutil.rmtree(PYCACHE)

non_validation_csv_paths = [
    OUTPUTS["sources"],
    OUTPUTS["type_contract"],
    OUTPUTS["no_spurion"],
    OUTPUTS["first_coefficients"],
    OUTPUTS["arena_status"],
    OUTPUTS["claim_status"],
    OUTPUTS["decision"],
    OUTPUTS["next"],
    OUTPUTS["branches"],
    *BRANCH_OUTPUTS.values(),
]

all_output_rows: list[dict[str, str]] = []
for path in non_validation_csv_paths:
    all_output_rows.extend(rows(path))

generated_paths = [DOC, *OUTPUTS.values(), *BRANCH_OUTPUTS.values()]
formalization_generated_hits = [path for path in generated_paths if FORMALIZATION.exists() and under(path, FORMALIZATION)]
dotg_rows_after = rows(DOTG_TARGET)

has_no_spurion_countermodel = any(row["result"] == "COUNTERMODEL_SURVIVES" for row in no_spurion_rows)
has_internal_k = any(row["coefficient"] == "K_epsilon_source_norm" and row["value"] == "1" for row in first_coefficient_rows)
has_missing_arena = any(row["coefficient_status"] == "MISSING" for row in arena_status_rows)

validation_rows = [
    base({"validation_id": "VAL3057_00_sources_exist", "passed": all(boolish(row["exists"]) for row in source_register), "requirement": "all cited source paths exist", "evidence": OUTPUTS["sources"].name}),
    base({"validation_id": "VAL3057_01_csv_parse", "passed": all(csv_ok(path) for path in non_validation_csv_paths), "requirement": "all generated and branch-copy CSVs parse cleanly", "evidence": "csv.DictReader parse check"}),
    base({"validation_id": "VAL3057_02_type_contract_written", "passed": len(type_contract_rows) >= 5 and any(row["type_object"] == "sigma_H,sigma_W,sigma_source" for row in type_contract_rows), "requirement": "parent type-system contract includes explicit spurion exclusion object", "evidence": OUTPUTS["type_contract"].name}),
    base({"validation_id": "VAL3057_03_no_spurion_conditional", "passed": has_no_spurion_countermodel and no_spurion_rows[-1]["result"] == "CONDITIONAL_NOT_SIGNED", "requirement": "no-spurion proof remains conditional and countermodel survives", "evidence": OUTPUTS["no_spurion"].name}),
    base({"validation_id": "VAL3057_04_internal_K_derived", "passed": has_internal_k, "requirement": "first internal K_epsilon coefficient is derived as 1", "evidence": OUTPUTS["first_coefficients"].name}),
    base({"validation_id": "VAL3057_05_physical_arenas_missing", "passed": has_missing_arena and all(row["usable_for_claim"] == "false" for row in arena_status_rows), "requirement": "physical arena coefficients remain missing and nonclaim", "evidence": OUTPUTS["arena_status"].name}),
    base({"validation_id": "VAL3057_06_dotg_no_placeholder_append", "passed": dotg_rows_before == dotg_rows_after and not any("3057" in row.get("row_id", "") for row in dotg_rows_after), "requirement": "3057 does not append a placeholder dotG row", "evidence": str(DOTG_TARGET)}),
    base({"validation_id": "VAL3057_07_no_claim_rows", "passed": not has_claim_true(all_output_rows), "requirement": "no generated row is valid for claim", "evidence": "valid_for_claim/claim_allowed/score_ready/claim_active/signature flags"}),
    base({"validation_id": "VAL3057_08_claim_status_nonactive", "passed": all(str(row["claim_active"]).lower() == "false" for row in claim_rows), "requirement": "all 3057 claims remain inactive", "evidence": OUTPUTS["claim_status"].name}),
    base({"validation_id": "VAL3057_09_branch_copies", "passed": all(path.exists() and csv_ok(path) for path in BRANCH_OUTPUTS.values()), "requirement": "branch copies exist and parse", "evidence": OUTPUTS["branches"].name}),
    base({"validation_id": "VAL3057_10_output_scope", "passed": all(under(path, ROOT) for path in generated_paths), "requirement": "all generated outputs are inside post-checkpoint-work", "evidence": str(ROOT)}),
    base({"validation_id": "VAL3057_11_formalization_untouched", "passed": len(formalization_generated_hits) == 0, "requirement": "formalization-workbench modified-file target count remains 0", "evidence": f"generated outputs under formalization={len(formalization_generated_hits)}"}),
    base({"validation_id": "VAL3057_12_next_target", "passed": next_rows[0]["next_checkpoint"].startswith("3058-"), "requirement": "next target selects PPN projection or parent type-system derivation", "evidence": OUTPUTS["next"].name}),
    base({"validation_id": "VAL3057_13_pycache_removed", "passed": not PYCACHE.exists(), "requirement": "scripts __pycache__ removed", "evidence": str(PYCACHE)}),
]
write_csv(OUTPUTS["validation"], validation_rows)

doc_text = f"""# 3057 - Parent Type-System No-Spurion Proof or First Epsilon W-Channel Arena Coefficients

Status: `Y5_R2FR_3057_no_spurion_conditional_first_internal_Kepsilon_source_norm_derived_nonclaim`

Generated: `{RUN_UTC}`

## Verdict

3057 takes the no-spurion route as far as the current corpus permits.

If the parent matter type system only allows:

`S_A[psi_A; q(Phi), theta_A]`

and forbids source/readout spurions:

`sigma_H, sigma_W, sigma_source`

then `a_H` and `a_W` cannot be typed as parent source vertices. In that assumed type system, `epsilon_Wchan=0`.

But the proof still does not close for current MTS, because the parent type system itself is not yet derived from the core fields. The countermodel survives: if `sigma_W` is allowed, then `a_W/a_H` is typeable.

3057 does derive one useful internal coefficient:

`delta_A_source = epsilon_Wchan + R_lock + Delta_operator_pullback + higher_order`

so:

`K_epsilon_source_norm = 1`.

This is **not** a PPN/R10/WEP/clock/orbit coefficient and is not a claim. It is the internal bridge needed for the next projection step.

## Parent Type-System Contract

{md_table(type_contract_rows, ["type_id", "type_object", "allowed_role", "forbidden_role", "rule", "current_status", "missing_for_claim"])}

## No-Spurion Proof Attempt

{md_table(no_spurion_rows, ["proof_id", "claim_piece", "statement", "proof_step", "result", "current_status", "missing_for_claim"])}

## First K-Epsilon Coefficients

{md_table(first_coefficient_rows, ["coefficient_id", "coefficient", "value", "arena", "projection_formula", "current_status", "blocker"])}

## Arena Coefficient Status

{md_table(arena_status_rows, ["arena_id", "arena", "coefficient_status", "usable_for_claim", "reason"])}

## Claim Status

{md_table(claim_rows, ["claim_id", "claim", "status", "claim_active", "reason"])}

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
    raise SystemExit(f"3057 validation failed: {[row['validation_id'] for row in failures]}")

print(f"wrote {DOC}")
print(f"validation rows: {len(validation_rows)} passed")
print("claim status: no-spurion conditional; K_epsilon_source_norm=1 internal nonclaim")
