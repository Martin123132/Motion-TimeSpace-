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

CHECKPOINT = "3056"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "3056-Y5-R2FR-typed-no-source-prefactor-grammar-or-epsilon-Wchannel-bound-schema-under-AX1090.md"
DOTG_TARGET = RESIDUALS / "P8_time_drift_residual_or_zero.csv"

SOURCE_PATHS = {
    "SRC3056_00_3055_doc": ROOT / "3055-Y5-R2FR-Hilbert-source-descent-and-W-channel-retirement-or-dotG-zero-readout-under-AX1090.md",
    "SRC3056_01_3055_hilbert": RESIDUALS / "P8_Y5_R2FR_3055_HILBERT_SOURCE_DESCENT_THEOREM_ATTEMPT.csv",
    "SRC3056_02_3055_w_retirement": RESIDUALS / "P8_Y5_R2FR_3055_W_CHANNEL_RETIREMENT_MAP.csv",
    "SRC3056_03_3055_epsilon": RESIDUALS / "P8_Y5_R2FR_3055_EPSILON_WCHANNEL_RESIDUAL_CONTRACT.csv",
    "SRC3056_04_3055_next": RESIDUALS / "P8_Y5_R2FR_3055_NEXT_TARGET.csv",
    "SRC3056_05_2645_clause": RESIDUALS / "P8_Y5_NO_SOURCE_PREFACTOR_2645_PARENT_ACTION_CLAUSE_ATTEMPT.csv",
    "SRC3056_06_2645_claim_gates": RESIDUALS / "P8_Y5_NO_SOURCE_PREFACTOR_2645_CLAIM_GATES.csv",
    "SRC3056_07_2645_validator_cases": RESIDUALS / "P8_Y5_NO_SOURCE_PREFACTOR_2645_VALIDATOR_CASES.csv",
    "SRC3056_08_2645_validator_results": RESIDUALS / "P8_Y5_NO_SOURCE_PREFACTOR_2645_VALIDATOR_RESULTS.csv",
    "SRC3056_09_2587_action_contract": RESIDUALS / "P8_Y5_MIN_PARENT_MATTER_2587_ACTION_CONTRACT.csv",
    "SRC3056_10_2587_countermodels": RESIDUALS / "P8_Y5_MIN_PARENT_MATTER_2587_COUNTERMODEL_TESTS.csv",
    "SRC3056_11_2587_adoption_gate": RESIDUALS / "P8_Y5_MIN_PARENT_MATTER_2587_ADOPTION_GATE.csv",
    "SRC3056_12_3039_relative_weight": PARENT_ACTION / "relative_source_vertex_weight_theorem_3039_NOT_SIGNED.csv",
    "SRC3056_13_3054_w_owner": RESIDUALS / "P8_Y5_R2FR_3054_W_PARENT_OWNER_CLAUSE.csv",
    "SRC3056_14_parent_action_attempt": RESIDUALS / "P8_Y5_PARENT_ACTION_DERIVATION_ATTEMPT.csv",
    "SRC3056_15_local_action_blocks": RESIDUALS / "P8_MIN_PARENT_LOCAL_GR_ACTION_BLOCKS.csv",
    "SRC3056_16_dotg_target": DOTG_TARGET,
}

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3056_SOURCE_REGISTER.csv",
    "typed_grammar": RESIDUALS / "P8_Y5_R2FR_3056_TYPED_NO_SOURCE_PREFACTOR_GRAMMAR_ATTEMPT.csv",
    "grammar_gates": RESIDUALS / "P8_Y5_R2FR_3056_GRAMMAR_GATE_EVALUATION.csv",
    "epsilon_bound_schema": RESIDUALS / "P8_Y5_R2FR_3056_EPSILON_WCHANNEL_BOUND_SCHEMA.csv",
    "arena_requirements": RESIDUALS / "P8_Y5_R2FR_3056_LOCAL_ARENA_PROJECTION_REQUIREMENTS.csv",
    "claim_status": RESIDUALS / "P8_Y5_R2FR_3056_CLAIM_STATUS.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_3056_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_3056_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_3056_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3056_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "typed_grammar_copy": PARENT_ACTION / "typed_no_source_prefactor_grammar_attempt_3056_NOT_SIGNED.csv",
    "grammar_gates_copy": PARENT_ACTION / "typed_grammar_gate_evaluation_3056_NOT_SIGNED.csv",
    "epsilon_schema_copy": LOCAL_BOUNDS / "epsilon_Wchannel_bound_schema_3056_NONCLAIM.csv",
    "arena_requirements_copy": LOCAL_BOUNDS / "epsilon_Wchannel_arena_projection_requirements_3056_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR3056_PARENT_TYPE_SYSTEM_OR_EPSILON_WCHANNEL_COEFFICIENTS_NEXT_NONCLAIM.csv",
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
        "gate_passes_for_current_MTS",
        "bound_ready",
        "grammar_proves_zero",
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

typed_grammar_rows = [
    base(
        {
            "grammar_id": "TGRAM3056_0_allowed_objects",
            "grammar_piece": "allowed matter grammar",
            "typed_statement": "Allowed ordinary matter terms have type S_A[psi_A; q(Phi), theta_A] and integrate with the unique observed measure mu_obs(q(Phi)).",
            "forbidden_object": "source-only/readout-only prefactors a_H, a_W, w_A(Z), kappa_A(Z), c_A(source)",
            "proof_attempt": "if q(Phi), mu_obs and theta_A are the only permitted non-matter inputs, no separate source/readout label exists to type a_W/a_H",
            "result": "GOOD_GRAMMAR_SHAPE",
            "current_status": "NOT_PARENT_SIGNED",
            "grammar_proves_zero": "false",
            "missing_for_claim": "MISSING_TYPED_PARENT_OBJECT_LANGUAGE; MISSING_Q_STACK_OWNER",
            "source_path": str(SOURCE_PATHS["SRC3056_09_2587_action_contract"]),
        }
    ),
    base(
        {
            "grammar_id": "TGRAM3056_1_source_label_forgetting",
            "grammar_piece": "source-label forgetting",
            "typed_statement": "After variation, the source is T_obs_munu, not the labelled collection {(A,T_A)} and not a readout-channel-labelled current.",
            "forbidden_object": "post-variation selector that reweights source by H-channel or W-channel",
            "proof_attempt": "Hilbert variation of one S_matter erases source labels before weak-field projection",
            "result": "EXACT_IF_S_MATTER_UNIVERSAL",
            "current_status": "CONDITIONAL_ONLY",
            "grammar_proves_zero": "false",
            "missing_for_claim": "MISSING_VARIATION_BEFORE_READOUT_THEOREM; MISSING_NO_SPURION_RETURN",
            "source_path": str(SOURCE_PATHS["SRC3056_05_2645_clause"]),
        }
    ),
    base(
        {
            "grammar_id": "TGRAM3056_2_no_readout_channel_slot",
            "grammar_piece": "no H/W source-channel slot",
            "typed_statement": "psi_N and chi_W are readout coordinates of phi_g, not independent parent source slots.",
            "forbidden_object": "S_src=rho_obs(a_H psi_N+a_W chi_W) as parent structure",
            "proof_attempt": "3054/3055 route makes W:=Phi_metric and psi_N=phi_g+O(phi_g^2), so a_H/a_W can only be diagnostic pullback bookkeeping",
            "result": "PROMISING_ROUTE",
            "current_status": "BLOCKED_BY_W_OWNER_AND_LAPSE_SIGNATURE",
            "grammar_proves_zero": "false",
            "missing_for_claim": "MISSING_W_OWNER_ADOPTION; MISSING_LAPSE_READOUT_SIGNATURE",
            "source_path": str(SOURCE_PATHS["SRC3056_13_3054_w_owner"]),
        }
    ),
    base(
        {
            "grammar_id": "TGRAM3056_3_no_common_mode_escape",
            "grammar_piece": "common-mode calibration guard",
            "typed_statement": "A universal constant prefactor may be absorbed into the common action/G_ref normalization; non-universal source/readout prefactors may not.",
            "forbidden_object": "hiding epsilon_Wchan inside measured GM, G_ref or a field rescaling",
            "proof_attempt": "separate universal action scale from source/readout-dependent relative scale",
            "result": "GUARD_NEEDED",
            "current_status": "ACTION_SCALE_OWNER_MISSING",
            "grammar_proves_zero": "false",
            "missing_for_claim": "MISSING_ACTION_SCALE_OWNER; MISSING_G_REF_COMMON_MODE_LOCK",
            "source_path": str(SOURCE_PATHS["SRC3056_14_parent_action_attempt"]),
        }
    ),
    base(
        {
            "grammar_id": "TGRAM3056_4_countermodel",
            "grammar_piece": "surviving countermodel",
            "typed_statement": "If a parent grammar permits a source/readout spurion sigma_W, then a_W/a_H is typeable and epsilon_Wchan can be nonzero.",
            "forbidden_object": "sigma_W or source-class label returning after Hilbert variation",
            "proof_attempt": "2645 validator already refuses Ward-only, classical-EOM and field-rescale shortcuts",
            "result": "COUNTERMODEL_SURVIVES",
            "current_status": "NOT_PROVED",
            "grammar_proves_zero": "false",
            "missing_for_claim": "MISSING_NO_SPURION_RETURN_THEOREM",
            "source_path": str(SOURCE_PATHS["SRC3056_07_2645_validator_cases"]),
        }
    ),
    base(
        {
            "grammar_id": "TGRAM3056_5_verdict",
            "grammar_piece": "typed grammar verdict",
            "typed_statement": "The exact grammar that would make epsilon_Wchan=0 is now written, but current MTS lacks the parent type-system proof.",
            "forbidden_object": "claiming local source closure without grammar signature",
            "proof_attempt": "combine 2587 minimal matter, 2645 no-prefactor, 3054 W owner and 3055 Hilbert descent",
            "result": "CONDITIONAL_ZERO_THEOREM_NOT_SIGNED",
            "current_status": "BOUND_SCHEMA_REQUIRED_IF_NEXT_PROOF_FAILS",
            "grammar_proves_zero": "false",
            "missing_for_claim": "MISSING_PARENT_TYPE_SYSTEM; MISSING_NO_SOURCE_PREF_ACTOR_ADOPTION",
            "source_path": str(SOURCE_PATHS["SRC3056_03_3055_epsilon"]),
        }
    ),
]

grammar_gate_rows = [
    base(
        {
            "gate_id": "GGATE3056_0_q_stack_owner",
            "requirement": "q(Phi) owns the observed matter stack before variation",
            "current_status": "CONTRACT_ONLY",
            "gate_passes_for_current_MTS": "false",
            "blocker": "q/e_obs/tau/ell_J ownership not parent-derived",
            "source_path": str(SOURCE_PATHS["SRC3056_09_2587_action_contract"]),
        }
    ),
    base(
        {
            "gate_id": "GGATE3056_1_single_measure_action_scale",
            "requirement": "one observed measure and one action scale for all ordinary matter sectors",
            "current_status": "NOT_DERIVED",
            "gate_passes_for_current_MTS": "false",
            "blocker": "hbar/action-scale/measure owner missing",
            "source_path": str(SOURCE_PATHS["SRC3056_05_2645_clause"]),
        }
    ),
    base(
        {
            "gate_id": "GGATE3056_2_no_source_prefactor",
            "requirement": "source-only prefactors w_A, a_W, a_H are untypeable",
            "current_status": "COUNTERMODEL_SURVIVES",
            "gate_passes_for_current_MTS": "false",
            "blocker": "typed parent grammar not proven",
            "source_path": str(SOURCE_PATHS["SRC3056_06_2645_claim_gates"]),
        }
    ),
    base(
        {
            "gate_id": "GGATE3056_3_variation_before_readout",
            "requirement": "Hilbert variation creates T_obs before H/W/local weak-field readout labels are introduced",
            "current_status": "CONDITIONAL",
            "gate_passes_for_current_MTS": "false",
            "blocker": "variation-before-readout theorem not signed",
            "source_path": str(SOURCE_PATHS["SRC3056_01_3055_hilbert"]),
        }
    ),
    base(
        {
            "gate_id": "GGATE3056_4_no_spurion_return",
            "requirement": "no source/readout spurion can re-enter after Hilbert variation",
            "current_status": "MISSING",
            "gate_passes_for_current_MTS": "false",
            "blocker": "no-spurion-return theorem not present",
            "source_path": str(SOURCE_PATHS["SRC3056_07_2645_validator_cases"]),
        }
    ),
    base(
        {
            "gate_id": "GGATE3056_5_common_mode_guard",
            "requirement": "universal scale can be calibrated, relative source/readout scale cannot",
            "current_status": "PARTIAL_GUARD",
            "gate_passes_for_current_MTS": "false",
            "blocker": "G_ref/common action normalization not fully signed with matter grammar",
            "source_path": str(SOURCE_PATHS["SRC3056_15_local_action_blocks"]),
        }
    ),
]

epsilon_bound_schema_rows = [
    base(
        {
            "bound_id": "EWB3056_0_schema_header",
            "residual": "epsilon_Wchan",
            "definition": "epsilon_Wchan := (a_W/r_W)/(a_H/r_H)-1",
            "arena": "all local arenas",
            "observable": "source normalization residual",
            "projection_formula": "Delta O_X = K_epsilon_X * epsilon_Wchan + higher_order_or_R_lock_terms",
            "required_inputs": "K_epsilon_X; arena observable bound; denominator convention; source path; units; sign convention",
            "current_status": "SCHEMA_ONLY_NONCLAIM",
            "bound_ready": "false",
            "valid_for_claim": "false",
            "reason": "no arena projection coefficients are sourced yet",
        }
    ),
    base(
        {
            "bound_id": "EWB3056_1_ppn",
            "residual": "epsilon_Wchan",
            "definition": "first-order mismatch in local source/readout normalization",
            "arena": "PPN",
            "observable": "gamma_minus_1/beta_minus_1/effective Newtonian source coefficient",
            "projection_formula": "Delta_PPN = K_epsilon_PPN * epsilon_Wchan",
            "required_inputs": "MISSING_K_EPSILON_PPN; MISSING_PPN_EXPANSION_ORDER; MISSING_METRIC_GAUGE_MAP",
            "current_status": "MISSING_ARENA_PROJECTION",
            "bound_ready": "false",
            "valid_for_claim": "false",
            "reason": "PPN coefficient map from epsilon_Wchan not derived",
        }
    ),
    base(
        {
            "bound_id": "EWB3056_2_R10",
            "residual": "epsilon_Wchan",
            "definition": "source channel mismatch leaking into short-range effective coupling",
            "arena": "R10",
            "observable": "alpha(lambda) Yukawa-like local residual",
            "projection_formula": "alpha_pred(lambda)=K_epsilon_R10(lambda)*epsilon_Wchan",
            "required_inputs": "MISSING_K_EPSILON_R10_LAMBDA; MISSING_LAMBDA_PROFILE; MISSING_REAL_BOUND_CURVE",
            "current_status": "MISSING_ARENA_PROJECTION",
            "bound_ready": "false",
            "valid_for_claim": "false",
            "reason": "no sourced epsilon-to-alpha projection",
        }
    ),
    base(
        {
            "bound_id": "EWB3056_3_WEP",
            "residual": "epsilon_Wchan",
            "definition": "possible source/test composition sensitivity if prefactor is material-labelled",
            "arena": "WEP",
            "observable": "eta_AB",
            "projection_formula": "eta_AB = K_epsilon_WEP_AB * epsilon_Wchan",
            "required_inputs": "MISSING_MATERIAL_BASIS; MISSING_K_EPSILON_WEP_AB; MISSING_SOURCE_TEST_PROJECTION",
            "current_status": "MISSING_ARENA_PROJECTION",
            "bound_ready": "false",
            "valid_for_claim": "false",
            "reason": "composition basis and coefficient provenance missing",
        }
    ),
    base(
        {
            "bound_id": "EWB3056_4_clocks",
            "residual": "epsilon_Wchan",
            "definition": "readout drift if H/W source channel changes clock coupling",
            "arena": "clock",
            "observable": "dln nu_clock/dt or alpha-clock sensitivity residual",
            "projection_formula": "Delta_clock = K_epsilon_clock * epsilon_Wchan",
            "required_inputs": "MISSING_K_EPSILON_CLOCK; MISSING_CLOCK_READOUT_MODEL; MISSING_TIME_DRIFT_MAP",
            "current_status": "MISSING_ARENA_PROJECTION",
            "bound_ready": "false",
            "valid_for_claim": "false",
            "reason": "clock sensitivity map not derived",
        }
    ),
    base(
        {
            "bound_id": "EWB3056_5_orbital",
            "residual": "epsilon_Wchan",
            "definition": "difference between source mass and orbital GM if source-channel prefactor survives",
            "arena": "orbital",
            "observable": "GM_source/orbital residual; anomalous precession or range residual",
            "projection_formula": "Delta_orbit = K_epsilon_orbit * epsilon_Wchan",
            "required_inputs": "MISSING_K_EPSILON_ORBIT; MISSING_GM_DENOMINATOR_LOCK; MISSING_ORBITAL_DATA_BINDING",
            "current_status": "MISSING_ARENA_PROJECTION",
            "bound_ready": "false",
            "valid_for_claim": "false",
            "reason": "orbital projection coefficient not derived",
        }
    ),
]

arena_requirements_rows = [
    base(
        {
            "requirement_id": "AREQ3056_0_zero_route",
            "route": "theorem_zero",
            "must_have": "typed parent grammar proving source/readout prefactors untypeable",
            "missing": "parent type system; no-spurion-return; action-scale owner; measure/coframe descent",
            "acceptance_rule": "epsilon_Wchan=0 can be claimed only after all grammar gates pass",
            "status": "NOT_READY",
        }
    ),
    base(
        {
            "requirement_id": "AREQ3056_1_bound_route",
            "route": "finite_bound",
            "must_have": "numeric K_epsilon_X for each arena plus source-backed empirical bound",
            "missing": "all K_epsilon_X coefficients; several empirical binding rows; denominator conventions",
            "acceptance_rule": "abs(K_epsilon_X*epsilon_Wchan)<=bound_X for every active local arena",
            "status": "SCHEMA_ONLY",
        }
    ),
    base(
        {
            "requirement_id": "AREQ3056_2_no_mixing",
            "route": "method_guard",
            "must_have": "do not use empirical bound to define epsilon_Wchan",
            "missing": "parent prediction or theorem-zero",
            "acceptance_rule": "prediction/proof first, bound second",
            "status": "GUARD_ACTIVE",
        }
    ),
    base(
        {
            "requirement_id": "AREQ3056_3_claim_policy",
            "route": "local_GR",
            "must_have": "epsilon_Wchan=0 or bounded below thresholds plus W/Phi/Gref/Hilbert gates",
            "missing": "epsilon zero/bound; parent type grammar; local arena projections",
            "acceptance_rule": "no local-GR/Newton claim from 3056",
            "status": "BLOCKED_NONCLAIM",
        }
    ),
]

claim_rows = [
    base(
        {
            "claim_id": "CLAIM3056_0_typed_grammar",
            "claim": "source-only prefactors are untypeable in current MTS",
            "status": "NO_NOT_SIGNED",
            "claim_active": "false",
            "reason": "typed parent object language and no-spurion-return theorem are missing",
        }
    ),
    base(
        {
            "claim_id": "CLAIM3056_1_epsilon_zero",
            "claim": "epsilon_Wchan=0",
            "status": "NO_CONDITIONAL_ONLY",
            "claim_active": "false",
            "reason": "zero theorem requires grammar gates that do not pass",
        }
    ),
    base(
        {
            "claim_id": "CLAIM3056_2_epsilon_bound",
            "claim": "epsilon_Wchan is bounded safely in local arenas",
            "status": "NO_SCHEMA_ONLY",
            "claim_active": "false",
            "reason": "arena projection coefficients are missing",
        }
    ),
    base(
        {
            "claim_id": "CLAIM3056_3_dotG",
            "claim": "dotG/G zero follows from source grammar",
            "status": "NO_READOUT_ZERO_UNSIGNED",
            "claim_active": "false",
            "reason": "source grammar does not yet close readout drift",
        }
    ),
    base(
        {
            "claim_id": "CLAIM3056_4_local_GR",
            "claim": "local GR/Newton source side is derived",
            "status": "NO_NOT_YET",
            "claim_active": "false",
            "reason": "3056 provides the exact proof/bound fork but does not close either branch",
        }
    ),
]

decision_rows = [
    base(
        {
            "decision_id": "DEC3056_0_proof_attempt",
            "question": "Can 3056 prove source-only prefactors untypeable?",
            "answer": "NO_NOT_YET",
            "reason": "the needed grammar is clear, but the parent type system and no-spurion theorem are not present",
            "action": "do not claim epsilon_Wchan=0",
        }
    ),
    base(
        {
            "decision_id": "DEC3056_1_progress",
            "question": "Did 3056 improve the situation?",
            "answer": "YES",
            "reason": "it converts the vague coupling problem into either a typed grammar theorem or a dimensionless residual bound problem",
            "action": "carry epsilon_Wchan as the named local source-channel residual",
        }
    ),
    base(
        {
            "decision_id": "DEC3056_2_bound_schema",
            "question": "Is the bound route ready to score?",
            "answer": "NO_SCHEMA_ONLY",
            "reason": "K_epsilon_X projection coefficients are missing for every local arena",
            "action": "do not run empirical scoring until coefficients exist",
        }
    ),
    base(
        {
            "decision_id": "DEC3056_3_next",
            "question": "Best next target?",
            "answer": "PARENT_TYPE_SYSTEM_OR_FIRST_K_EPSILON",
            "reason": "either prove no-spurion grammar, or derive the first arena projection coefficient for epsilon_Wchan",
            "action": "build 3057 parent type system/no-spurion proof or epsilon arena coefficients",
        }
    ),
]

next_rows = [
    base(
        {
            "next_id": "NEXT3056_0_3057",
            "next_checkpoint": "3057-Y5-R2FR-parent-type-system-no-spurion-proof-or-first-epsilon-Wchannel-arena-coefficients-under-AX1090.md",
            "script": "scripts/Y5_R2FR_parent_type_system_no_spurion_proof_or_first_epsilon_Wchannel_arena_coefficients_under_AX1090_3057.py",
            "mission": "try to prove no source/readout spurion can type a_W/a_H; if that fails, derive the first K_epsilon_X projection coefficients for PPN/R10/WEP/clock/orbit schemas",
            "starting_equation": "epsilon_Wchan := (a_W/r_W)/(a_H/r_H)-1 and Delta O_X = K_epsilon_X*epsilon_Wchan + ...",
            "claim_policy": "no local-GR/Newton claim until epsilon_Wchan is zero by parent type theorem or bounded by sourced arena projections",
        }
    )
]

write_csv(OUTPUTS["sources"], source_register)
write_csv(OUTPUTS["typed_grammar"], typed_grammar_rows)
write_csv(OUTPUTS["grammar_gates"], grammar_gate_rows)
write_csv(OUTPUTS["epsilon_bound_schema"], epsilon_bound_schema_rows)
write_csv(OUTPUTS["arena_requirements"], arena_requirements_rows)
write_csv(OUTPUTS["claim_status"], claim_rows)
write_csv(OUTPUTS["decision"], decision_rows)
write_csv(OUTPUTS["next"], next_rows)

copy_csv(OUTPUTS["typed_grammar"], BRANCH_OUTPUTS["typed_grammar_copy"])
copy_csv(OUTPUTS["grammar_gates"], BRANCH_OUTPUTS["grammar_gates_copy"])
copy_csv(OUTPUTS["epsilon_bound_schema"], BRANCH_OUTPUTS["epsilon_schema_copy"])
copy_csv(OUTPUTS["arena_requirements"], BRANCH_OUTPUTS["arena_requirements_copy"])
copy_csv(OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"])

branch_rows = [
    base(
        {
            "copy_id": copy_id,
            "destination": str(path),
            "exists": path.exists(),
            "row_count": len(rows(path)) if path.exists() else 0,
            "description": "3056 branch copy",
        }
    )
    for copy_id, path in BRANCH_OUTPUTS.items()
]
write_csv(OUTPUTS["branches"], branch_rows)

if PYCACHE.exists():
    shutil.rmtree(PYCACHE)

non_validation_csv_paths = [
    OUTPUTS["sources"],
    OUTPUTS["typed_grammar"],
    OUTPUTS["grammar_gates"],
    OUTPUTS["epsilon_bound_schema"],
    OUTPUTS["arena_requirements"],
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

has_countermodel = any(row["result"] == "COUNTERMODEL_SURVIVES" for row in typed_grammar_rows)
has_epsilon_schema = any(row["residual"] == "epsilon_Wchan" for row in epsilon_bound_schema_rows)
has_missing_projection = any("MISSING_ARENA_PROJECTION" in row["current_status"] for row in epsilon_bound_schema_rows)
all_gates_block = all(row["gate_passes_for_current_MTS"] == "false" for row in grammar_gate_rows)

validation_rows = [
    base({"validation_id": "VAL3056_00_sources_exist", "passed": all(boolish(row["exists"]) for row in source_register), "requirement": "all cited source paths exist", "evidence": OUTPUTS["sources"].name}),
    base({"validation_id": "VAL3056_01_csv_parse", "passed": all(csv_ok(path) for path in non_validation_csv_paths), "requirement": "all generated and branch-copy CSVs parse cleanly", "evidence": "csv.DictReader parse check"}),
    base({"validation_id": "VAL3056_02_typed_grammar_attempt", "passed": has_countermodel and typed_grammar_rows[-1]["result"] == "CONDITIONAL_ZERO_THEOREM_NOT_SIGNED", "requirement": "typed no-source-prefactor grammar attempt exists and remains unsigned", "evidence": OUTPUTS["typed_grammar"].name}),
    base({"validation_id": "VAL3056_03_grammar_gates_block", "passed": all_gates_block, "requirement": "all typed grammar gates block current claims", "evidence": OUTPUTS["grammar_gates"].name}),
    base({"validation_id": "VAL3056_04_epsilon_bound_schema", "passed": has_epsilon_schema and has_missing_projection, "requirement": "epsilon_Wchan bound schema exists but lacks arena projections", "evidence": OUTPUTS["epsilon_bound_schema"].name}),
    base({"validation_id": "VAL3056_05_arena_requirements_nonclaim", "passed": all(row["status"] in {"NOT_READY", "SCHEMA_ONLY", "GUARD_ACTIVE", "BLOCKED_NONCLAIM"} for row in arena_requirements_rows), "requirement": "arena projection requirements remain nonclaim", "evidence": OUTPUTS["arena_requirements"].name}),
    base({"validation_id": "VAL3056_06_dotg_no_placeholder_append", "passed": dotg_rows_before == dotg_rows_after and not any("3056" in row.get("row_id", "") for row in dotg_rows_after), "requirement": "3056 does not append a placeholder dotG row", "evidence": str(DOTG_TARGET)}),
    base({"validation_id": "VAL3056_07_no_claim_rows", "passed": not has_claim_true(all_output_rows), "requirement": "no generated row is valid for claim", "evidence": "valid_for_claim/claim_allowed/score_ready/claim_active/signature flags"}),
    base({"validation_id": "VAL3056_08_claim_status_nonactive", "passed": all(str(row["claim_active"]).lower() == "false" for row in claim_rows), "requirement": "all 3056 claims remain inactive", "evidence": OUTPUTS["claim_status"].name}),
    base({"validation_id": "VAL3056_09_branch_copies", "passed": all(path.exists() and csv_ok(path) for path in BRANCH_OUTPUTS.values()), "requirement": "branch copies exist and parse", "evidence": OUTPUTS["branches"].name}),
    base({"validation_id": "VAL3056_10_output_scope", "passed": all(under(path, ROOT) for path in generated_paths), "requirement": "all generated outputs are inside post-checkpoint-work", "evidence": str(ROOT)}),
    base({"validation_id": "VAL3056_11_formalization_untouched", "passed": len(formalization_generated_hits) == 0, "requirement": "formalization-workbench modified-file target count remains 0", "evidence": f"generated outputs under formalization={len(formalization_generated_hits)}"}),
    base({"validation_id": "VAL3056_12_next_target", "passed": next_rows[0]["next_checkpoint"].startswith("3057-"), "requirement": "next target selects parent type system/no-spurion proof or first K_epsilon coefficients", "evidence": OUTPUTS["next"].name}),
    base({"validation_id": "VAL3056_13_pycache_removed", "passed": not PYCACHE.exists(), "requirement": "scripts __pycache__ removed", "evidence": str(PYCACHE)}),
]
write_csv(OUTPUTS["validation"], validation_rows)

doc_text = f"""# 3056 - Typed No-Source-Prefactor Grammar or Epsilon W-Channel Bound Schema

Status: `Y5_R2FR_3056_typed_no_source_prefactor_grammar_written_not_signed_epsilon_bound_schema_nonclaim`

Generated: `{RUN_UTC}`

## Verdict

3056 writes the clean grammar that would kill the surviving coupling problem:

`S_A[psi_A; q(Phi), theta_A]`

with one observed stack, one measure, and one Hilbert variation.

In that grammar there is nowhere to type an independent readout/source prefactor:

`a_W/a_H`

or a parent-level two-channel source term:

`rho_obs(a_H psi_N + a_W chi_W)`.

If the grammar is parent-signed, then:

`epsilon_Wchan := (a_W/r_W)/(a_H/r_H) - 1 = 0`.

But 3056 cannot claim this yet. The current corpus still lacks the actual parent type system, source-label forgetting theorem, no-spurion-return theorem, and common action/measure owner. So the countermodel survives.

The fallback is now also clean: if the proof fails, `epsilon_Wchan` must be bounded through arena coefficients:

`Delta O_X = K_epsilon_X * epsilon_Wchan + higher_order_or_R_lock_terms`.

Those `K_epsilon_X` coefficients are not sourced yet, so this is a nonclaim schema only.

## Typed Grammar Attempt

{md_table(typed_grammar_rows, ["grammar_id", "grammar_piece", "typed_statement", "forbidden_object", "result", "current_status", "missing_for_claim"])}

## Grammar Gate Evaluation

{md_table(grammar_gate_rows, ["gate_id", "requirement", "current_status", "gate_passes_for_current_MTS", "blocker"])}

## Epsilon W-Channel Bound Schema

{md_table(epsilon_bound_schema_rows, ["bound_id", "residual", "arena", "observable", "projection_formula", "required_inputs", "current_status", "bound_ready"])}

## Local Arena Projection Requirements

{md_table(arena_requirements_rows, ["requirement_id", "route", "must_have", "missing", "acceptance_rule", "status"])}

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
    raise SystemExit(f"3056 validation failed: {[row['validation_id'] for row in failures]}")

print(f"wrote {DOC}")
print(f"validation rows: {len(validation_rows)} passed")
print("claim status: typed grammar conditional; epsilon_Wchan bound schema nonclaim")
