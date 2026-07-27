from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


PACK_ID = "P8_Y5_R10_1303"
TITLE = "1303-Y5-R10-RAB-memory-stress-nohair-or-bound-inputs"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_STARTED_UTC = datetime.now(timezone.utc)


SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
NOHAIR_ATTEMPT_PATH = OUT_DIR / f"{PACK_ID}_MEMORY_STRESS_NOHAIR_ATTEMPT.csv"
BOUND_INPUT_LEDGER_PATH = OUT_DIR / f"{PACK_ID}_K_MEM_STRESS_SIGMA_BOUND_INPUT_LEDGER_NONCLAIM.csv"
ZERO_OR_BOUND_DECISION_PATH = OUT_DIR / f"{PACK_ID}_ZERO_OR_BOUND_DECISION.csv"
RUNNER_SCHEMA_PATH = OUT_DIR / f"{PACK_ID}_K_MEM_STRESS_BOUND_RUNNER_SCHEMA_NONCLAIM.csv"
KBAR_UPDATE_PATH = OUT_DIR / f"{PACK_ID}_KBAR_UPDATE_PREVIEW_NONCLAIM.csv"
CLAIM_GATES_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATES.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1303_VALIDATION.csv"


def source_path(relative_path: str) -> Path:
    path = Path(relative_path)
    if path.is_absolute():
        return path
    return ROOT / path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def md_escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def markdown_table(rows: list[dict[str, object]], fields: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    return "\n".join(
        [
            "| " + " | ".join(fields) + " |",
            "| " + " | ".join(["---"] * len(fields)) + " |",
            *["| " + " | ".join(md_escape(row.get(field, "")) for field in fields) + " |" for row in rows],
        ]
    )


def exists_and_contains(relative_path: str, needle: str) -> tuple[bool, bool]:
    path = source_path(relative_path)
    if not path.exists():
        return False, False
    if not needle:
        return True, True
    return True, needle in read_text(path)


def validation_row(check_id: str, check: str, passed: bool, details: str) -> dict[str, object]:
    return {"check_id": check_id, "check": check, "status": "PASS" if passed else "FAIL", "details": details}


def is_false(value: object) -> bool:
    return str(value).strip().lower() in {"false", "0", "no"}


def all_nonclaim(tables: list[list[dict[str, object]]]) -> bool:
    return all(
        is_false(row.get("valid_for_claim", False)) and is_false(row.get("claim_allowed", False))
        for rows in tables
        for row in rows
    )


def generated_inside_formalization() -> list[Path]:
    generated_paths = [
        SOURCE_REGISTER_PATH,
        NOHAIR_ATTEMPT_PATH,
        BOUND_INPUT_LEDGER_PATH,
        ZERO_OR_BOUND_DECISION_PATH,
        RUNNER_SCHEMA_PATH,
        KBAR_UPDATE_PATH,
        CLAIM_GATES_PATH,
        DECISION_PATH,
        NEXT_PATH,
        VALIDATION_PATH,
        DOC_PATH,
    ]
    return [path for path in generated_paths if FORMALIZATION in path.parents]


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    source_register = [
        {
            "source_id": "SRC1303_0_1302_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1302_NEXT_TARGET.csv",
            "needle": "NEXT1302_0_1303",
            "role": "handoff into K_mem_stress nohair-or-bound gate",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1303_1_1302_residual_contract",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1302_MEMORY_STRESS_RESIDUAL_CONTRACT_NONCLAIM.csv",
            "needle": "K_mem_stress^Sigma",
            "role": "retained memory-stress spatial trace contract",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1303_2_1302_nohair_requirements",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1302_MEMORY_STRESS_NOHAIR_REQUIREMENTS.csv",
            "needle": "MISSING_PARENT_OWNER",
            "role": "1302 nohair blocker list",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1303_3_967_positive_operator",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_967_MEMORY_POSITIVE_OPERATOR_LEMMA.csv",
            "needle": "RELATIVE_LEMMA_READY_PARENT_INPUTS_UNSIGNED",
            "role": "relative nohair theorem shape",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1303_4_968_operator_inputs",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_968_MEMORY_OPERATOR_INPUT_AUDIT.csv",
            "needle": "INPUTS_MISSING_NO_THEOREM_ZERO",
            "role": "operator/nohair activation inputs missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1303_5_970_action_construction",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_970_QUADRATIC_MEMORY_ACTION_CONSTRUCTION.csv",
            "needle": "CONSTRUCTION_RELATIVE_NOT_PARENT_CLOSED",
            "role": "candidate memory action but not parent closed",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1303_6_1042_nohair_identity",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1042_POSITIVE_X_NOHAIR_IDENTITY.csv",
            "needle": "CONDITIONAL_THEOREM_DERIVED_FULL_CLAIM_BLOCKED",
            "role": "general positive-X nohair identity and residual fallback",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1303_7_1042_premise_gate",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1042_NOHAIR_PREMISE_GATE.csv",
            "needle": "FAIL_CURRENT_CLAIM_NOHAIR_NOT_PARENT_SIGNED",
            "role": "nohair premise gate remains failed for claim",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1303_8_826_action_ansatz",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_826_PARENT_ACTION_ANSATZ.csv",
            "needle": "AA826_1_memory_sector",
            "role": "candidate scalar-memory stress owner scaffold",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]
    for row in source_register:
        exists, needle_found = exists_and_contains(str(row["local_path"]), str(row["needle"]))
        row["exists"] = exists
        row["needle_found"] = needle_found

    nohair_attempt = [
        {
            "attempt_id": "NHA1303_0_operator_owner",
            "premise": "parent action supplies a self-adjoint local memory operator L_m and field/domain owner",
            "candidate_evidence": "970 writes a quadratic action candidate; 967/1042 write the theorem form",
            "blocking_evidence": "968 and 970 say parent owner/operator/domain are not supplied",
            "result": "NOT_DERIVED",
            "effect_on_K_mem_stress": "cannot use nohair to set gradients or X/m profile to zero",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "NHA1303_1_positive_gap",
            "premise": "Z_m is positive and the local Hessian/mass gap removes zero modes",
            "candidate_evidence": "967/1042 positive-operator lemmas give the mathematical identity",
            "blocking_evidence": "Z_m, m_X^2, lambda_gap, topology, and sign certificate are missing",
            "result": "NOT_DERIVED",
            "effect_on_K_mem_stress": "gradient/potential energy terms cannot be killed",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "NHA1303_2_source_silence",
            "premise": "J_m=0 in ordinary local exterior, with no matter, chi_D wall, boundary exchange, readout, or history drive",
            "candidate_evidence": "967/970 list source silence as the theorem-zero route",
            "blocking_evidence": "970 source decomposition keeps J_X terms not derived zero",
            "result": "NOT_DERIVED",
            "effect_on_K_mem_stress": "source-driven memory profile remains possible",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "NHA1303_3_boundary_zero",
            "premise": "boundary flux, zero mode, and topological class vanish or are source-independent constants",
            "candidate_evidence": "967/1042 identify boundary zero as sufficient",
            "blocking_evidence": "968/970 retain boundary data and topological class as missing",
            "result": "NOT_DERIVED",
            "effect_on_K_mem_stress": "boundary hair can feed K_mem_stress^Sigma",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "NHA1303_4_EH_subtraction",
            "premise": "constant potential piece V_R(m_*;X_B)-V_ref is Lambda/background only, not a source-normalization residual",
            "candidate_evidence": "1302 records the safe constant/nohair case",
            "blocking_evidence": "subtraction owner and X_B drift-zero clauses are missing",
            "result": "NOT_DERIVED",
            "effect_on_K_mem_stress": "potential volume term remains in bound input ledger",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "NHA1303_5_verdict",
            "premise": "K_mem_stress^Sigma is theorem-zero",
            "candidate_evidence": "conditional nohair identity is mathematically available",
            "blocking_evidence": "all owner/sign/source/boundary/subtraction premises remain unsigned",
            "result": "FAIL_CURRENT_CORPUS_STAGE_BOUND_INPUTS",
            "effect_on_K_mem_stress": "build concrete nonclaim bound inputs instead of claiming zero",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    bound_input_ledger = [
        {
            "input_id": "KMS1303_0_Zm_abs_bound",
            "symbol": "Z_m_bar",
            "definition": "upper bound on |Z_m| in the local memory-stress domain",
            "units": "units_required_from_parent_L_m_normalization",
            "enters_formula": "Z_m_bar * B_grad_sp and 0.5*Z_m_bar*B_grad_4",
            "source_status": "MISSING_SOURCE_BACKED_VALUE_OR_THEOREM",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_826_PARENT_ACTION_ANSATZ.csv;source-intake/mts_residuals/P8_Y5_R10_1302_MEMORY_STRESS_RESIDUAL_CONTRACT_NONCLAIM.csv",
            "source_anchor": "AA826_1_memory_sector;MSR1302_1_spatial_trace_bound_template",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "input_id": "KMS1303_1_spatial_gradient_bound",
            "symbol": "B_grad_sp",
            "definition": "B_grad_sp >= sum_i |nabla^i m nabla^i m| in the same local frame used by Kbar trace reversal",
            "units": "m_units^2 / length^2 after frame lock",
            "enters_formula": "Z_m_bar * B_grad_sp",
            "source_status": "MISSING_GRAD_m_PROFILE_OR_NOHAIR",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_967_MEMORY_POSITIVE_OPERATOR_LEMMA.csv;source-intake/mts_residuals/P8_Y5_R10_968_MEMORY_OPERATOR_INPUT_AUDIT.csv",
            "source_anchor": "MPO967_4_energy_identity;MOI968_8_verdict",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "input_id": "KMS1303_2_four_gradient_bound",
            "symbol": "B_grad_4",
            "definition": "B_grad_4 >= |nabla_alpha m nabla^alpha m| in the locked signature and local coframe",
            "units": "m_units^2 / length^2 after signature lock",
            "enters_formula": "3 * 0.5 * Z_m_bar * B_grad_4",
            "source_status": "MISSING_SIGNATURE_FRAME_AND_PROFILE",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1302_MEMORY_STRESS_RESIDUAL_CONTRACT_NONCLAIM.csv",
            "source_anchor": "MSR1302_1_spatial_trace_bound_template",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "input_id": "KMS1303_3_potential_subtraction_bound",
            "symbol": "B_V",
            "definition": "B_V >= |V_R(m;X_B)-V_ref| after any parent-owned EH/Lambda subtraction",
            "units": "energy_density_or_geometric_stress_units_after_normalization",
            "enters_formula": "3 * B_V",
            "source_status": "MISSING_V_R_PARENT_FORM_AND_SUBTRACTION_OWNER",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_826_PARENT_ACTION_ANSATZ.csv;source-intake/mts_residuals/P8_Y5_R10_1302_MEMORY_STRESS_NOHAIR_REQUIREMENTS.csv",
            "source_anchor": "AA826_1_memory_sector;NHM1302_4_potential_subtraction",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "input_id": "KMS1303_4_XB_metric_response_bound",
            "symbol": "B_ZX_Sigma",
            "definition": "bound on the spatial trace from X_B dependence of Z_m and V_R",
            "units": "same_as_K_mem_stress_spatial_trace",
            "enters_formula": "B_ZX_Sigma",
            "source_status": "MISSING_X_B_METRIC_RESPONSE",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1302_MEMORY_STRESS_RESIDUAL_CONTRACT_NONCLAIM.csv",
            "source_anchor": "MSR1302_0_canonical_scalar_stress_form",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "input_id": "KMS1303_5_source_bath_bound",
            "symbol": "B_source_bath_Sigma",
            "definition": "bound on source, bath, history, or readout-drive spatial stress trace",
            "units": "same_as_K_mem_stress_spatial_trace",
            "enters_formula": "B_source_bath_Sigma",
            "source_status": "MISSING_SOURCE_BATH_ZERO_OR_BOUND",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_970_QUADRATIC_MEMORY_ACTION_CONSTRUCTION.csv",
            "source_anchor": "QMA970_3_source_silence",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "input_id": "KMS1303_6_boundary_trace_bound",
            "symbol": "B_boundary_Sigma",
            "definition": "bound on boundary flux, corner, zero-mode, and topological spatial trace terms",
            "units": "same_as_K_mem_stress_spatial_trace",
            "enters_formula": "B_boundary_Sigma",
            "source_status": "MISSING_BOUNDARY_ZERO_OR_BOUND",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_967_MEMORY_POSITIVE_OPERATOR_LEMMA.csv;source-intake/mts_residuals/P8_Y5_R10_970_QUADRATIC_MEMORY_ACTION_CONSTRUCTION.csv",
            "source_anchor": "MPO967_2_boundary;QMA970_4_boundary_zero_mode",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "input_id": "KMS1303_7_frame_units_lock",
            "symbol": "U_frame_mem",
            "definition": "local coframe, signature, spatial-index convention, and stress normalization for K_mem_stress^Sigma",
            "units": "normalization_contract",
            "enters_formula": "required before comparing K_mem_stress^Sigma to Kbar_00/Newton/PPN/R10 budgets",
            "source_status": "MISSING_FRAME_UNITS_LOCK",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1302_MEMORY_STRESS_RESIDUAL_CONTRACT_NONCLAIM.csv",
            "source_anchor": "MSR1302_1_spatial_trace_bound_template",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    zero_or_bound_decision = [
        {
            "decision_id": "ZB1303_0_theorem_zero_route",
            "route": "positive-operator nohair",
            "status": "BLOCKED_NOT_PARENT_SIGNED",
            "required_to_open": "operator owner; positive gap; source silence; boundary zero; EH subtraction; observable projection",
            "effect": "would set K_mem_stress^Sigma=0 or Lambda-only in the local compact exterior",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "ZB1303_1_bound_route",
            "route": "explicit absolute bound inputs",
            "status": "OPEN_AS_NONCLAIM_SCHEMA",
            "required_to_open": "fill KMS1303_0..7 with sourced values/theorems and units",
            "effect": "would make K_mem_stress^Sigma scoreable without claiming theorem-zero",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "ZB1303_2_live_policy",
            "route": "current live branch",
            "status": "NO_SCORE_RETAINED_RESIDUAL",
            "required_to_open": "either zero route or bound route must be completed",
            "effect": "Kbar/Newton/PPN/local-GR remains blocked",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    runner_schema = [
        {
            "schema_id": "KMRUN1303_0_bound_formula",
            "target": "K_mem_stress^Sigma",
            "formula": "|K_mem_stress^Sigma| <= Z_m_bar*B_grad_sp + 3*(0.5*Z_m_bar*B_grad_4 + B_V) + B_ZX_Sigma + B_source_bath_Sigma + B_boundary_Sigma",
            "required_inputs": "KMS1303_0_Zm_abs_bound;KMS1303_1_spatial_gradient_bound;KMS1303_2_four_gradient_bound;KMS1303_3_potential_subtraction_bound;KMS1303_4_XB_metric_response_bound;KMS1303_5_source_bath_bound;KMS1303_6_boundary_trace_bound;KMS1303_7_frame_units_lock",
            "runner_status": "SCHEMA_ONLY_NOT_EXECUTABLE",
            "why_not_executable": "all values/theorems and units are missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "schema_id": "KMRUN1303_1_zero_gate",
            "target": "K_mem_stress^Sigma",
            "formula": "K_mem_stress^Sigma=0 if operator owner + positive gap + source silence + boundary zero + EH subtraction + X_B drift zero all pass",
            "required_inputs": "NHM1302_0..5 plus no topological/gauge zero mode",
            "runner_status": "ZERO_GATE_SCHEMA_ONLY",
            "why_not_executable": "zero premises are unsigned",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    kbar_update = [
        {
            "update_id": "KBU1303_0_memory_stress_bound_schema_added",
            "target_row": "KBA1299_0_total_Kbar_abs_bound",
            "update": "K_mem_stress^Sigma has a concrete zero-or-bound interface",
            "still_missing": "MISSING_KMS1303_0_TO_7_VALUES_OR_THEOREMS;MISSING_LCG_SPATIAL_TRACE;MISSING_CDB_TRACE;MISSING_PROJECTOR_BOUNDARY",
            "current_status": "BOUND_INTERFACE_WRITTEN_NOT_SCOREABLE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "update_id": "KBU1303_1_memory_nohair_rejected_for_now",
            "target_row": "K_mem_stress^Sigma",
            "update": "nohair theorem is mathematically available but not parent-signed",
            "still_missing": "MISSING_PARENT_OWNER;MISSING_SIGN_GAP;MISSING_SOURCE_ZERO;MISSING_BOUNDARY_ZERO;MISSING_SUBTRACTION",
            "current_status": "ZERO_NOT_CLAIMED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "update_id": "KBU1303_2_local_GR_guard",
            "target_row": "local GR/Newton/PPN/R10 runners",
            "update": "must require either zero route or complete bound route before scoring memory-stress branch",
            "still_missing": "MISSING_MEMORY_STRESS_ZERO_OR_BOUND",
            "current_status": "NO_SCORE_GUARD_ACTIVE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    claim_gates = [
        {
            "gate_id": "CG1303_0_nohair_derivation",
            "claim": "K_mem_stress^Sigma is theorem-zero",
            "current_status": "BLOCKED_NOT_PARENT_SIGNED",
            "reason": "conditional nohair identity exists but owner/sign/source/boundary/subtraction premises are missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1303_1_bound_inputs",
            "claim": "K_mem_stress^Sigma has a scoreable bound",
            "current_status": "BLOCKED_INPUT_VALUES_MISSING",
            "reason": "KMS1303_0..7 are schema rows with no sourced numeric/theorem values",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1303_2_schema_progress",
            "claim": "K_mem_stress^Sigma no longer has a vague blocker",
            "current_status": "SATISFIED_FOR_NONCLAIM_SCHEMA",
            "reason": "1303 writes exact zero route, bound formula, input ledger, and runner schema",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1303_3_Kbar_score",
            "claim": "Kbar_L,loc,00 bound is scoreable",
            "current_status": "BLOCKED_NOT_SCOREABLE",
            "reason": "memory stress, Lcg spatial trace, CDB trace, and projector-boundary terms remain unresolved",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1303_4_local_GR",
            "claim": "local GR/Newton/PPN recovery pass",
            "current_status": "BLOCKED_NO_LOCAL_GR_CLAIM",
            "reason": "no theorem-zero or finite-bound pass exists for the retained memory-stress branch",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decision = [
        {
            "decision_id": "DEC1303_0_nohair_not_claimed",
            "decision": "do not claim memory-stress nohair from current corpus",
            "because": "the nohair identity is conditional but the parent action does not supply the needed operator/source/boundary/subtraction premises",
            "next_action": "choose first KMS input to fill, starting with operator owner or Z_m/sign-gap",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1303_1_bound_schema_adopted",
            "decision": "stage K_mem_stress^Sigma bound inputs as the fallback route",
            "because": "a finite bound can make the branch testable even if theorem-zero fails",
            "next_action": "derive/source the first bound input instead of using a zero shortcut",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_target = [
        {
            "next_id": "NEXT1303_0_1304",
            "target_file": "1304-Y5-R10-RAB-memory-operator-owner-or-first-stress-bound-input.md",
            "target_script": "scripts/Y5_R10_RAB_memory_operator_owner_or_first_stress_bound_input.py",
            "task": "try to source/derive the memory operator owner and Z_m positivity/gap; if that fails, fill the first nonclaim bound input row for Z_m_bar and B_grad_sp",
            "success_condition": "operator-owner/positive-gap premise advances, or KMS1303_0/KMS1303_1 receive source-backed nonclaim rows without local-GR scoring",
            "do_not": "do not set K_mem_stress^Sigma to zero from the conditional nohair identity alone",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    write_csv(SOURCE_REGISTER_PATH, source_register)
    write_csv(NOHAIR_ATTEMPT_PATH, nohair_attempt)
    write_csv(BOUND_INPUT_LEDGER_PATH, bound_input_ledger)
    write_csv(ZERO_OR_BOUND_DECISION_PATH, zero_or_bound_decision)
    write_csv(RUNNER_SCHEMA_PATH, runner_schema)
    write_csv(KBAR_UPDATE_PATH, kbar_update)
    write_csv(CLAIM_GATES_PATH, claim_gates)
    write_csv(DECISION_PATH, decision)
    write_csv(NEXT_PATH, next_target)

    validations = []
    source_count = len(source_register)
    source_hits = sum(1 for row in source_register if row["exists"] and row["needle_found"])
    validations.append(
        validation_row(
            "VAL1303_0_sources_exist",
            "registered source paths exist and anchors are found",
            source_hits == source_count,
            f"{source_hits}/{source_count} source anchors found",
        )
    )
    validations.append(
        validation_row(
            "VAL1303_1_nohair_not_claimed",
            "memory nohair is attempted but not claimed",
            any(row["result"] == "FAIL_CURRENT_CORPUS_STAGE_BOUND_INPUTS" for row in nohair_attempt)
            and not any(row["result"] == "DERIVED_FOR_CLAIM" for row in nohair_attempt),
            ";".join(str(row["attempt_id"]) + "=" + str(row["result"]) for row in nohair_attempt),
        )
    )
    validations.append(
        validation_row(
            "VAL1303_2_bound_inputs_staged",
            "all K_mem_stress bound input rows are staged as nonclaim missing inputs",
            len(bound_input_ledger) == 8 and all("MISSING" in str(row["source_status"]) for row in bound_input_ledger),
            ";".join(str(row["input_id"]) for row in bound_input_ledger),
        )
    )
    validations.append(
        validation_row(
            "VAL1303_3_runner_schema_not_executable",
            "runner schema exists but remains non-executable/no-score",
            len(runner_schema) == 2 and all("SCHEMA" in str(row["runner_status"]) for row in runner_schema),
            ";".join(str(row["schema_id"]) + "=" + str(row["runner_status"]) for row in runner_schema),
        )
    )
    validations.append(
        validation_row(
            "VAL1303_4_Kbar_not_scoreable",
            "Kbar update preview keeps scoring blocked",
            all("NOT_SCOREABLE" in str(row["current_status"]) or "ZERO_NOT_CLAIMED" in str(row["current_status"]) or "NO_SCORE" in str(row["current_status"]) for row in kbar_update),
            ";".join(str(row["update_id"]) + "=" + str(row["current_status"]) for row in kbar_update),
        )
    )
    generated_tables = [
        SOURCE_REGISTER_PATH,
        NOHAIR_ATTEMPT_PATH,
        BOUND_INPUT_LEDGER_PATH,
        ZERO_OR_BOUND_DECISION_PATH,
        RUNNER_SCHEMA_PATH,
        KBAR_UPDATE_PATH,
        CLAIM_GATES_PATH,
        DECISION_PATH,
        NEXT_PATH,
    ]
    parse_ok = True
    parse_details: list[str] = []
    for table_path in generated_tables:
        try:
            parse_details.append(f"{table_path.name}:{len(read_csv(table_path))}")
        except Exception as error:
            parse_ok = False
            parse_details.append(f"{table_path.name}:ERROR:{error}")
    validations.append(validation_row("VAL1303_5_csv_parse", "all generated CSVs parse cleanly", parse_ok, "; ".join(parse_details)))
    formalization_hits = generated_inside_formalization()
    validations.append(
        validation_row(
            "VAL1303_6_formalization_untouched",
            "formalization-workbench untouched by generated outputs",
            not formalization_hits,
            f"formalization_generated_output_count={len(formalization_hits)}",
        )
    )
    validations.append(
        validation_row(
            "VAL1303_7_nonclaim_policy",
            "all generated rows remain nonclaim",
            all_nonclaim([source_register, nohair_attempt, bound_input_ledger, zero_or_bound_decision, runner_schema, kbar_update, claim_gates, decision, next_target]),
            "valid_for_claim=false and claim_allowed=false throughout generated tables",
        )
    )
    validations.append(
        validation_row(
            "VAL1303_8_next_target_1304",
            "next target routes to memory operator owner or first stress bound input",
            next_target[0]["next_id"] == "NEXT1303_0_1304" and "memory-operator-owner" in str(next_target[0]["target_file"]),
            str(next_target[0]["target_file"]),
        )
    )
    overall_pass = all(row["status"] == "PASS" for row in validations)
    validations.append(
        validation_row(
            "VAL1303_9_overall",
            "overall 1303 validation",
            overall_pass,
            "1303 rejects an unsigned memory-stress nohair claim, stages exact K_mem_stress bound inputs and runner schema, keeps scoring blocked, and routes to operator owner or first bound input",
        )
    )
    write_csv(VALIDATION_PATH, validations)

    doc = f"""# 1303 Y5 R10 RAB memory-stress nohair or bound inputs

Generated: `{RUN_STARTED_UTC.isoformat()}`

**Current verdict:** 1303 does not prove `K_mem_stress^Sigma=0`. The no-hair mathematics exists as a conditional positive-operator identity, but the parent owner, sign/gap, source-zero, boundary-zero, and subtraction premises are still unsigned.

**Main progress:** the retained memory-stress branch is now test-shaped. `K_mem_stress^Sigma` has an explicit bound formula, eight named missing inputs, and a runner schema. That is much better than a foggy “memory stress might matter” blocker.

**Still blocked:** no Newton/PPN/R10/local-GR score is allowed. The zero route and the finite-bound route both remain incomplete.

## Source Register

{markdown_table(source_register, ["source_id", "local_path", "needle", "exists", "needle_found", "role", "valid_for_claim", "claim_allowed"])}

## Memory-Stress No-Hair Attempt

{markdown_table(nohair_attempt, ["attempt_id", "premise", "candidate_evidence", "blocking_evidence", "result", "effect_on_K_mem_stress", "valid_for_claim", "claim_allowed"])}

## `K_mem_stress^Sigma` Bound Input Ledger

{markdown_table(bound_input_ledger, ["input_id", "symbol", "definition", "units", "enters_formula", "source_status", "source_path", "source_anchor", "valid_for_claim", "claim_allowed"])}

## Zero Or Bound Decision

{markdown_table(zero_or_bound_decision, ["decision_id", "route", "status", "required_to_open", "effect", "valid_for_claim", "claim_allowed"])}

## Runner Schema

{markdown_table(runner_schema, ["schema_id", "target", "formula", "required_inputs", "runner_status", "why_not_executable", "valid_for_claim", "claim_allowed"])}

## Kbar Update Preview

{markdown_table(kbar_update, ["update_id", "target_row", "update", "still_missing", "current_status", "valid_for_claim", "claim_allowed"])}

## Claim Gates

{markdown_table(claim_gates, ["gate_id", "claim", "current_status", "reason", "valid_for_claim", "claim_allowed"])}

## Decision Ledger

{markdown_table(decision, ["decision_id", "decision", "because", "next_action", "valid_for_claim", "claim_allowed"])}

## Next Target

{markdown_table(next_target, ["next_id", "target_file", "target_script", "task", "success_condition", "do_not", "valid_for_claim", "claim_allowed"])}

## Validation

{markdown_table(validations, ["check_id", "check", "status", "details"])}
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


if __name__ == "__main__":
    main()
