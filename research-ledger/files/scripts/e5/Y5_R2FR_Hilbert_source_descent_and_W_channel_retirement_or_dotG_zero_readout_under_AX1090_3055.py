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

CHECKPOINT = "3055"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "3055-Y5-R2FR-Hilbert-source-descent-and-W-channel-retirement-or-dotG-zero-readout-under-AX1090.md"
DOTG_TARGET = RESIDUALS / "P8_time_drift_residual_or_zero.csv"

SOURCE_PATHS = {
    "SRC3055_00_3054_doc": ROOT / "3054-Y5-R2FR-W-definition-parent-owner-or-dotG-parent-coefficient-derivation-under-AX1090.md",
    "SRC3055_01_3054_w_owner": RESIDUALS / "P8_Y5_R2FR_3054_W_PARENT_OWNER_CLAUSE.csv",
    "SRC3055_02_3054_w_audit": RESIDUALS / "P8_Y5_R2FR_3054_W_SYMBOL_OCCURRENCE_AUDIT.csv",
    "SRC3055_03_3054_w_gates": RESIDUALS / "P8_Y5_R2FR_3054_W_OWNER_GATE_EVALUATION.csv",
    "SRC3055_04_3054_dotg": RESIDUALS / "P8_Y5_R2FR_3054_DOTG_PARENT_COEFFICIENT_ATTEMPT.csv",
    "SRC3055_05_3054_next": RESIDUALS / "P8_Y5_R2FR_3054_NEXT_TARGET.csv",
    "SRC3055_06_3053_hilbert": RESIDUALS / "P8_Y5_R2FR_3053_HILBERT_SOURCE_READOUT_AUDIT.csv",
    "SRC3055_07_3037_min_lock": PARENT_ACTION / "minimum_source_readout_lock_parent_clause_3037_NOT_SIGNED.csv",
    "SRC3055_08_3038_common_source": PARENT_ACTION / "common_source_functional_normal_form_3038_NOT_SIGNED.csv",
    "SRC3055_09_3038_derivative_audit": PARENT_ACTION / "functional_derivative_match_audit_3038_NONCLAIM.csv",
    "SRC3055_10_3039_relative_weight": PARENT_ACTION / "relative_source_vertex_weight_theorem_3039_NOT_SIGNED.csv",
    "SRC3055_11_3039_single_potential": RESIDUALS / "P8_Y5_R2FR_3039_SINGLE_POTENTIAL_READOUT_REDUCTION.csv",
    "SRC3055_12_3039_two_channel": RESIDUALS / "P8_Y5_R2FR_3039_TWO_CHANNEL_QUADRATIC_EULER_LAW.csv",
    "SRC3055_13_3039_delta_prefactor": RESIDUALS / "P8_Y5_R2FR_3039_DELTA_A_PREFACTOR_RESIDUAL_CONTRACT.csv",
    "SRC3055_14_2645_no_prefactor": RESIDUALS / "P8_Y5_NO_SOURCE_PREFACTOR_2645_PARENT_ACTION_CLAUSE_ATTEMPT.csv",
    "SRC3055_15_parent_action_derivation": RESIDUALS / "P8_Y5_PARENT_ACTION_DERIVATION_ATTEMPT.csv",
    "SRC3055_16_dotg_target": DOTG_TARGET,
    "SRC3055_17_3050_spine": RESIDUALS / "P8_Y5_R2FR_3050_PARENT_TOPOLOGICAL_KAPPA_SPINE_CANDIDATE.csv",
}

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3055_SOURCE_REGISTER.csv",
    "hilbert_descent": RESIDUALS / "P8_Y5_R2FR_3055_HILBERT_SOURCE_DESCENT_THEOREM_ATTEMPT.csv",
    "w_retirement": RESIDUALS / "P8_Y5_R2FR_3055_W_CHANNEL_RETIREMENT_MAP.csv",
    "residual_contract": RESIDUALS / "P8_Y5_R2FR_3055_EPSILON_WCHANNEL_RESIDUAL_CONTRACT.csv",
    "dotg_zero": RESIDUALS / "P8_Y5_R2FR_3055_DOTG_ZERO_READOUT_ATTEMPT.csv",
    "claim_status": RESIDUALS / "P8_Y5_R2FR_3055_CLAIM_STATUS.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_3055_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_3055_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_3055_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3055_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "hilbert_descent_copy": PARENT_ACTION / "Hilbert_source_descent_theorem_attempt_3055_NOT_SIGNED.csv",
    "w_retirement_copy": PARENT_ACTION / "W_channel_retirement_map_3055_NOT_ADOPTED.csv",
    "residual_contract_copy": LOCAL_BOUNDS / "epsilon_Wchannel_residual_contract_3055_NONCLAIM.csv",
    "dotg_zero_copy": LOCAL_BOUNDS / "dotG_zero_readout_attempt_3055_BLOCKED_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR3055_TYPED_NO_SOURCE_PREFACTOR_OR_EPSILON_WCHANNEL_BOUND_NEXT_NONCLAIM.csv",
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
        "retired_for_current_MTS",
        "gate_passes_for_current_MTS",
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

hilbert_descent_rows = [
    base(
        {
            "theorem_id": "HSD3055_0_parent_matter_action",
            "theorem_piece": "single universal matter action",
            "statement": "S_matter is a functional only of g_obs, psi and allowed matter parameters; no source-only a_H, a_W, w_A, kappa_A or species prefactor is typeable.",
            "derivation": "Hilbert variation then defines one observed stress tensor T_obs_munu.",
            "result_if_signed": "there is one source density rho_obs=T_obs00/c^2",
            "current_status": "NOT_SIGNED_COUNTERMODEL_SURVIVES",
            "signed_for_current_MTS": "false",
            "missing_for_claim": "MISSING_TYPED_NO_SOURCE_PREFACTOR_GRAMMAR; MISSING_MATTER_MEASURE_DESCENT",
            "source_path": str(SOURCE_PATHS["SRC3055_14_2645_no_prefactor"]),
        }
    ),
    base(
        {
            "theorem_id": "HSD3055_1_metric_readout_pairing",
            "theorem_piece": "one source pairing",
            "statement": "At first weak-field order S_src^loc must reduce to integral mu_obs rho_obs a_phi phi_g, not integral rho_H(a_H psi_N+a_W chi_W).",
            "derivation": "if psi_N=r_H phi_g and chi_W=r_W phi_g are readout coordinates, source weights are pullback coefficients fixed by r_H and r_W.",
            "result_if_signed": "a_H/r_H = a_W/r_W = a_phi, so no relative source-vertex freedom remains",
            "current_status": "CONDITIONAL_MATH_NOT_PARENT_SIGNED",
            "signed_for_current_MTS": "false",
            "missing_for_claim": "MISSING_SINGLE_PAIRING_PARENT_ACTION; MISSING_READOUT_JACOBIAN_VALUES",
            "source_path": str(SOURCE_PATHS["SRC3055_10_3039_relative_weight"]),
        }
    ),
    base(
        {
            "theorem_id": "HSD3055_2_W_owner_injection",
            "theorem_piece": "W-channel collapse",
            "statement": "3054 proposes W:=Phi_metric[g_obs], so chi_W=phi_g and r_W=1 in the local first-order branch.",
            "derivation": "W is a metric readout, not a varied parent coordinate.",
            "result_if_signed": "a_W is not an independent parent source vertex",
            "current_status": "DEPENDS_ON_3054_ADOPTION",
            "signed_for_current_MTS": "false",
            "missing_for_claim": "MISSING_W_OWNER_ADOPTION; MISSING_TWO_CHANNEL_RETIREMENT",
            "source_path": str(SOURCE_PATHS["SRC3055_01_3054_w_owner"]),
        }
    ),
    base(
        {
            "theorem_id": "HSD3055_3_lapse_readout",
            "theorem_piece": "H/lapse-channel collapse",
            "statement": "In the same weak-field chart, psi_N=-log(N)=phi_g+O(phi_g^2), so r_H=1 at first order.",
            "derivation": "Taylor expansion of N=sqrt(1-2 phi_g) in the observed metric branch.",
            "result_if_signed": "a_H and a_W reduce to the same first-order source pairing coefficient",
            "current_status": "CONDITIONAL_FIRST_ORDER_ONLY",
            "signed_for_current_MTS": "false",
            "missing_for_claim": "MISSING_PARENT_SIGNATURE_FOR_LAPSE_BRANCH; SECOND_ORDER_PPN_STILL_OPEN",
            "source_path": str(SOURCE_PATHS["SRC3055_11_3039_single_potential"]),
        }
    ),
    base(
        {
            "theorem_id": "HSD3055_4_countermodel",
            "theorem_piece": "two-channel obstruction",
            "statement": "S_src=rho_obs(a_H psi_N+a_W chi_W) with arbitrary a_H/a_W is still a legal diagnostic countermodel unless the parent grammar forbids it.",
            "derivation": "common density alone does not fix relative vertex weight.",
            "result_if_signed": "if not forbidden, epsilon_Wchan must be bounded empirically",
            "current_status": "COUNTERMODEL_SURVIVES",
            "signed_for_current_MTS": "false",
            "missing_for_claim": "MISSING_RULE_MAKING_TWO_CHANNEL_RELATIVE_WEIGHT_UNTYPEABLE",
            "source_path": str(SOURCE_PATHS["SRC3055_12_3039_two_channel"]),
        }
    ),
    base(
        {
            "theorem_id": "HSD3055_5_verdict",
            "theorem_piece": "Hilbert source descent verdict",
            "statement": "The derivation route is coherent: universal matter action + W retirement + lapse readout collapses two channels to one source.",
            "derivation": "but every nontrivial premise is still a parent-action/signature adoption, not a proven current theorem",
            "result_if_signed": "first-order local Newton source normalization would become derivable",
            "current_status": "PROMISING_CONDITIONAL_NOT_SIGNED",
            "signed_for_current_MTS": "false",
            "missing_for_claim": "MISSING_TYPED_PARENT_GRAMMAR; MISSING_SOURCE_DESCENT_PROOF",
            "source_path": str(SOURCE_PATHS["SRC3055_07_3037_min_lock"]),
        }
    ),
]

w_retirement_rows = [
    base(
        {
            "retire_id": "WRET3055_0_W",
            "old_object": "W",
            "new_status": "metric readout only",
            "replacement": "Phi_metric[g_obs]",
            "retirement_rule": "not varied, not fitted, not an independent source potential",
            "retired_for_current_MTS": "false",
            "blocker": "3054 owner clause not adopted",
        }
    ),
    base(
        {
            "retire_id": "WRET3055_1_chi_W",
            "old_object": "chi_W",
            "new_status": "diagnostic coordinate",
            "replacement": "phi_g=Phi_metric/c^2",
            "retirement_rule": "allowed only after pullback from g_obs; no parent source slot",
            "retired_for_current_MTS": "false",
            "blocker": "two-channel source language still present",
        }
    ),
    base(
        {
            "retire_id": "WRET3055_2_a_W",
            "old_object": "a_W",
            "new_status": "forbidden independent parent vertex",
            "replacement": "a_phi/r_W pullback coefficient",
            "retirement_rule": "relative freedom a_W/a_H must be untypeable or bounded",
            "retired_for_current_MTS": "false",
            "blocker": "typed no-source-prefactor grammar not proven",
        }
    ),
    base(
        {
            "retire_id": "WRET3055_3_C_W",
            "old_object": "C_W or C_WH",
            "new_status": "operator/source coefficient pullback",
            "replacement": "4*pi*G_ref/c^2 in chi coordinate after W:=Phi_metric",
            "retirement_rule": "not an independent denominator after G_ref/W owner locks",
            "retired_for_current_MTS": "false",
            "blocker": "operator pullback proof not signed",
        }
    ),
    base(
        {
            "retire_id": "WRET3055_4_A_W",
            "old_object": "A_W",
            "new_status": "diagnostic ratio only",
            "replacement": "A_W=1 only if W/Gref/Hilbert gates pass",
            "retirement_rule": "never use fitted GM to set this ratio",
            "retired_for_current_MTS": "false",
            "blocker": "claim remains blocked",
        }
    ),
]

residual_contract_rows = [
    base(
        {
            "residual_id": "EPSW3055_0_definition",
            "symbol": "epsilon_Wchan",
            "definition": "epsilon_Wchan := (a_W/r_W)/(a_H/r_H) - 1",
            "meaning": "dimensionless survivor of independent W-channel source weighting after readout pullback",
            "units": "dimensionless",
            "current_value": "MISSING_PARENT_ZERO_OR_NUMERIC_BOUND_INPUT",
            "valid_for_claim": "false",
            "next_action": "prove epsilon_Wchan=0 by typed parent grammar or create source-backed local bound row",
        }
    ),
    base(
        {
            "residual_id": "EPSW3055_1_relation_to_delta_A",
            "symbol": "delta_A_source",
            "definition": "delta_A_source = Xi_H/C_WH - 1 + R_lock, with epsilon_Wchan one component of the relative source-vertex mismatch",
            "meaning": "connects source-retirement failure to existing local Newton normalization residual",
            "units": "dimensionless",
            "current_value": "MISSING_R_LOCK_AND_OPERATOR_PULLBACK",
            "valid_for_claim": "false",
            "next_action": "map epsilon_Wchan into PPN/R10/WEP/local-clock arenas only after coefficient provenance exists",
        }
    ),
    base(
        {
            "residual_id": "EPSW3055_2_zero_condition",
            "symbol": "epsilon_Wchan=0",
            "definition": "holds if S_matter[g_obs,psi] is universal, W:=Phi_metric, psi_N=phi_g+O(phi_g^2), chi_W=phi_g, and no source-only prefactor is typeable",
            "meaning": "the exact parent contract needed to close the first-order source channel",
            "units": "dimensionless",
            "current_value": "CONDITIONAL_ONLY",
            "valid_for_claim": "false",
            "next_action": "attack typed no-source-prefactor grammar",
        }
    ),
    base(
        {
            "residual_id": "EPSW3055_3_bound_route",
            "symbol": "epsilon_Wchan_bound",
            "definition": "if the zero theorem fails, epsilon_Wchan must be bounded as a local source-normalization residual",
            "meaning": "prevents pretending the two-channel countermodel disappeared",
            "units": "dimensionless",
            "current_value": "NO_SOURCE_BACKED_BOUND_ROW",
            "valid_for_claim": "false",
            "next_action": "build nonclaim bound-acquisition schema only after proof route fails",
        }
    ),
]

dotg_zero_rows = [
    base(
        {
            "dotg_id": "DZ3055_0_required_identity",
            "formula": "dln_Geff_dt = D_t ln(kappa_eff*c^4/(8*pi)) + D_t ln Z_readout",
            "zero_condition": "d kappa_eff=0 and Z_readout=1 in the same observed Hilbert-source frame",
            "current_status": "PARTIAL_ONLY",
            "valid_prediction_row": "false",
            "reason": "topological kappa candidate does not yet prove readout zero",
            "source_path": str(SOURCE_PATHS["SRC3055_17_3050_spine"]),
        }
    ),
    base(
        {
            "dotg_id": "DZ3055_1_source_retirement_effect",
            "formula": "Z_readout depends on W/Hilbert/source-channel drift",
            "zero_condition": "W-channel retirement plus Hilbert source descent removes the surviving readout drift",
            "current_status": "CONDITIONAL_NOT_SIGNED",
            "valid_prediction_row": "false",
            "reason": "this becomes useful only after epsilon_Wchan=0 is parent-proven",
            "source_path": str(SOURCE_PATHS["SRC3055_01_3054_w_owner"]),
        }
    ),
    base(
        {
            "dotg_id": "DZ3055_2_verdict",
            "formula": "dotG/G zero local prediction",
            "zero_condition": "topological kappa + zero readout drift",
            "current_status": "BLOCKED_NONCLAIM",
            "valid_prediction_row": "false",
            "reason": "not available until source descent and W-channel retirement close",
            "source_path": str(SOURCE_PATHS["SRC3055_16_dotg_target"]),
        }
    ),
]

claim_rows = [
    base(
        {
            "claim_id": "CLAIM3055_0_hilbert_descent",
            "claim": "Hilbert source descent is proven for current MTS",
            "status": "NO_NOT_SIGNED",
            "claim_active": "false",
            "reason": "universal matter action and typed no-source-prefactor grammar are not proven",
        }
    ),
    base(
        {
            "claim_id": "CLAIM3055_1_W_channel_retired",
            "claim": "the old W/a_W/C_W channel is retired",
            "status": "NO_COUNTERMODEL_SURVIVES",
            "claim_active": "false",
            "reason": "two-channel expression remains a diagnostic countermodel unless made untypeable",
        }
    ),
    base(
        {
            "claim_id": "CLAIM3055_2_epsilon_zero",
            "claim": "epsilon_Wchan=0",
            "status": "NO_CONDITIONAL_ONLY",
            "claim_active": "false",
            "reason": "zero condition is written but not parent-signed",
        }
    ),
    base(
        {
            "claim_id": "CLAIM3055_3_dotG_zero",
            "claim": "dotG/G is zero in local branch",
            "status": "NO_READOUT_ZERO_UNSIGNED",
            "claim_active": "false",
            "reason": "topological kappa alone is insufficient without readout zero",
        }
    ),
    base(
        {
            "claim_id": "CLAIM3055_4_local_GR",
            "claim": "local GR/Newton source normalization is derived",
            "status": "NO_NOT_YET",
            "claim_active": "false",
            "reason": "3055 names the exact residual if the proof fails, but does not close it",
        }
    ),
]

decision_rows = [
    base(
        {
            "decision_id": "DEC3055_0_derivation",
            "question": "Can the source-channel collapse be derived in principle?",
            "answer": "YES_CONDITIONALLY",
            "reason": "one universal S_matter plus W:=Phi_metric and psi_N=phi_g forces a single first-order source pairing",
            "action": "record theorem shape but do not promote claim",
        }
    ),
    base(
        {
            "decision_id": "DEC3055_1_current_MTS",
            "question": "Does current MTS prove the collapse?",
            "answer": "NO",
            "reason": "typed no-source-prefactor grammar and matter measure descent are missing; two-channel countermodel survives",
            "action": "keep epsilon_Wchan residual active",
        }
    ),
    base(
        {
            "decision_id": "DEC3055_2_bound",
            "question": "What if the proof route fails?",
            "answer": "BOUND_EPSILON_WCHAN",
            "reason": "epsilon_Wchan is now the named dimensionless residual representing independent W-source weighting",
            "action": "prepare source-backed bound acquisition only after another proof attempt",
        }
    ),
    base(
        {
            "decision_id": "DEC3055_3_next",
            "question": "Best next attack?",
            "answer": "TYPED_NO_SOURCE_PREFACTOR_GRAMMAR",
            "reason": "making a_W untypeable is cleaner and less empirical than fitting a bound immediately",
            "action": "build 3056 typed grammar proof attempt or epsilon_Wchan bound schema",
        }
    ),
]

next_rows = [
    base(
        {
            "next_id": "NEXT3055_0_3056",
            "next_checkpoint": "3056-Y5-R2FR-typed-no-source-prefactor-grammar-or-epsilon-Wchannel-bound-schema-under-AX1090.md",
            "script": "scripts/Y5_R2FR_typed_no_source_prefactor_grammar_or_epsilon_Wchannel_bound_schema_under_AX1090_3056.py",
            "mission": "try to prove source-only a_W/a_H prefactors are untypeable in the parent matter grammar; if this fails, build nonclaim epsilon_Wchan bound-acquisition rows",
            "starting_equation": "epsilon_Wchan := (a_W/r_W)/(a_H/r_H)-1; local source closure needs epsilon_Wchan=0",
            "claim_policy": "no local-GR/Newton claim until epsilon_Wchan is parent-zero or source-backed bounded below required thresholds",
        }
    )
]

write_csv(OUTPUTS["sources"], source_register)
write_csv(OUTPUTS["hilbert_descent"], hilbert_descent_rows)
write_csv(OUTPUTS["w_retirement"], w_retirement_rows)
write_csv(OUTPUTS["residual_contract"], residual_contract_rows)
write_csv(OUTPUTS["dotg_zero"], dotg_zero_rows)
write_csv(OUTPUTS["claim_status"], claim_rows)
write_csv(OUTPUTS["decision"], decision_rows)
write_csv(OUTPUTS["next"], next_rows)

copy_csv(OUTPUTS["hilbert_descent"], BRANCH_OUTPUTS["hilbert_descent_copy"])
copy_csv(OUTPUTS["w_retirement"], BRANCH_OUTPUTS["w_retirement_copy"])
copy_csv(OUTPUTS["residual_contract"], BRANCH_OUTPUTS["residual_contract_copy"])
copy_csv(OUTPUTS["dotg_zero"], BRANCH_OUTPUTS["dotg_zero_copy"])
copy_csv(OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"])

branch_rows = [
    base(
        {
            "copy_id": copy_id,
            "destination": str(path),
            "exists": path.exists(),
            "row_count": len(rows(path)) if path.exists() else 0,
            "description": "3055 branch copy",
        }
    )
    for copy_id, path in BRANCH_OUTPUTS.items()
]
write_csv(OUTPUTS["branches"], branch_rows)

if PYCACHE.exists():
    shutil.rmtree(PYCACHE)

non_validation_csv_paths = [
    OUTPUTS["sources"],
    OUTPUTS["hilbert_descent"],
    OUTPUTS["w_retirement"],
    OUTPUTS["residual_contract"],
    OUTPUTS["dotg_zero"],
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

has_epsilon_definition = any(row["symbol"] == "epsilon_Wchan" for row in residual_contract_rows)
has_countermodel = any(row["current_status"] == "COUNTERMODEL_SURVIVES" for row in hilbert_descent_rows)
has_forbidden_aw = any(row["old_object"] == "a_W" and "forbidden" in row["new_status"] for row in w_retirement_rows)

validation_rows = [
    base({"validation_id": "VAL3055_00_sources_exist", "passed": all(boolish(row["exists"]) for row in source_register), "requirement": "all cited source paths exist", "evidence": OUTPUTS["sources"].name}),
    base({"validation_id": "VAL3055_01_csv_parse", "passed": all(csv_ok(path) for path in non_validation_csv_paths), "requirement": "all generated and branch-copy CSVs parse cleanly", "evidence": "csv.DictReader parse check"}),
    base({"validation_id": "VAL3055_02_hilbert_theorem_conditional", "passed": has_countermodel and hilbert_descent_rows[-1]["current_status"] == "PROMISING_CONDITIONAL_NOT_SIGNED", "requirement": "Hilbert source descent theorem is conditional and countermodel remains", "evidence": OUTPUTS["hilbert_descent"].name}),
    base({"validation_id": "VAL3055_03_w_retirement_map", "passed": has_forbidden_aw and len(w_retirement_rows) >= 5, "requirement": "W-channel retirement map names a_W as forbidden parent vertex", "evidence": OUTPUTS["w_retirement"].name}),
    base({"validation_id": "VAL3055_04_residual_defined", "passed": has_epsilon_definition, "requirement": "epsilon_Wchan residual is explicitly defined", "evidence": OUTPUTS["residual_contract"].name}),
    base({"validation_id": "VAL3055_05_dotg_no_placeholder_append", "passed": dotg_rows_before == dotg_rows_after and not any("3055" in row.get("row_id", "") for row in dotg_rows_after), "requirement": "3055 does not append a placeholder dotG row", "evidence": str(DOTG_TARGET)}),
    base({"validation_id": "VAL3055_06_dotg_zero_nonclaim", "passed": all(str(row["valid_prediction_row"]).lower() == "false" for row in dotg_zero_rows), "requirement": "dotG zero readout attempt remains nonclaim", "evidence": OUTPUTS["dotg_zero"].name}),
    base({"validation_id": "VAL3055_07_no_claim_rows", "passed": not has_claim_true(all_output_rows), "requirement": "no generated row is valid for claim", "evidence": "valid_for_claim/claim_allowed/score_ready/claim_active/signature flags"}),
    base({"validation_id": "VAL3055_08_claim_status_nonactive", "passed": all(str(row["claim_active"]).lower() == "false" for row in claim_rows), "requirement": "all 3055 claims remain inactive", "evidence": OUTPUTS["claim_status"].name}),
    base({"validation_id": "VAL3055_09_branch_copies", "passed": all(path.exists() and csv_ok(path) for path in BRANCH_OUTPUTS.values()), "requirement": "branch copies exist and parse", "evidence": OUTPUTS["branches"].name}),
    base({"validation_id": "VAL3055_10_output_scope", "passed": all(under(path, ROOT) for path in generated_paths), "requirement": "all generated outputs are inside post-checkpoint-work", "evidence": str(ROOT)}),
    base({"validation_id": "VAL3055_11_formalization_untouched", "passed": len(formalization_generated_hits) == 0, "requirement": "formalization-workbench modified-file target count remains 0", "evidence": f"generated outputs under formalization={len(formalization_generated_hits)}"}),
    base({"validation_id": "VAL3055_12_next_target", "passed": next_rows[0]["next_checkpoint"].startswith("3056-"), "requirement": "next target selects typed no-source-prefactor grammar or epsilon bound schema", "evidence": OUTPUTS["next"].name}),
    base({"validation_id": "VAL3055_13_pycache_removed", "passed": not PYCACHE.exists(), "requirement": "scripts __pycache__ removed", "evidence": str(PYCACHE)}),
]
write_csv(OUTPUTS["validation"], validation_rows)

doc_text = f"""# 3055 - Hilbert Source Descent and W-Channel Retirement or dotG Zero Readout

Status: `Y5_R2FR_3055_Hilbert_source_descent_conditional_epsilon_Wchannel_named_nonclaim`

Generated: `{RUN_UTC}`

## Verdict

3055 turns the source problem into a cleaner theorem-or-residual fork.

If the parent matter sector is really:

`S_matter[g_obs, psi]`

and if the local weak-field readouts are:

`psi_N = phi_g + O(phi_g^2)`

`chi_W = W/c^2 = phi_g`

then the source term must be one pairing:

`S_src^loc = integral mu_obs rho_obs a_phi phi_g`

not a parent-level two-channel object:

`rho_obs(a_H psi_N + a_W chi_W)`.

So the route is promising: a universal Hilbert matter action plus `W:=Phi_metric` would make the relative `a_H/a_W` freedom disappear.

But the countermodel still survives for current MTS because the typed grammar forbidding source-only prefactors has not been proven. Therefore 3055 names the exact residual:

`epsilon_Wchan := (a_W/r_W)/(a_H/r_H) - 1`

That residual is now the thing to prove zero or bound. No local-GR/Newton claim is active.

## Hilbert Source Descent Theorem Attempt

{md_table(hilbert_descent_rows, ["theorem_id", "theorem_piece", "statement", "derivation", "result_if_signed", "current_status", "missing_for_claim"])}

## W-Channel Retirement Map

{md_table(w_retirement_rows, ["retire_id", "old_object", "new_status", "replacement", "retirement_rule", "retired_for_current_MTS", "blocker"])}

## Epsilon W-Channel Residual Contract

{md_table(residual_contract_rows, ["residual_id", "symbol", "definition", "meaning", "units", "current_value", "next_action"])}

## dotG Zero Readout Attempt

{md_table(dotg_zero_rows, ["dotg_id", "formula", "zero_condition", "current_status", "valid_prediction_row", "reason"])}

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
    raise SystemExit(f"3055 validation failed: {[row['validation_id'] for row in failures]}")

print(f"wrote {DOC}")
print(f"validation rows: {len(validation_rows)} passed")
print("claim status: Hilbert source descent conditional; epsilon_Wchan residual named nonclaim")
