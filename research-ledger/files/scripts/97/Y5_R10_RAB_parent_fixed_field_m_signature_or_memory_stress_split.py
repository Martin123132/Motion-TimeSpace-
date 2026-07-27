from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


PACK_ID = "P8_Y5_R10_1302"
TITLE = "1302-Y5-R10-RAB-parent-fixed-field-m-signature-or-memory-stress-split"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_STARTED_UTC = datetime.now(timezone.utc)


SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
FIXED_FIELD_SIGNATURE_AUDIT_PATH = OUT_DIR / f"{PACK_ID}_FIXED_FIELD_M_SIGNATURE_AUDIT.csv"
MEMORY_STRESS_RESIDUAL_PATH = OUT_DIR / f"{PACK_ID}_MEMORY_STRESS_RESIDUAL_CONTRACT_NONCLAIM.csv"
CHAIN_PRUNING_STATUS_PATH = OUT_DIR / f"{PACK_ID}_CHAIN_PRUNING_STATUS_NONCLAIM.csv"
LOCAL_NOHAIR_REQUIREMENTS_PATH = OUT_DIR / f"{PACK_ID}_MEMORY_STRESS_NOHAIR_REQUIREMENTS.csv"
KBAR_UPDATE_PATH = OUT_DIR / f"{PACK_ID}_KBAR_UPDATE_PREVIEW_NONCLAIM.csv"
CLAIM_GATES_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATES.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1302_VALIDATION.csv"


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
        FIXED_FIELD_SIGNATURE_AUDIT_PATH,
        MEMORY_STRESS_RESIDUAL_PATH,
        CHAIN_PRUNING_STATUS_PATH,
        LOCAL_NOHAIR_REQUIREMENTS_PATH,
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
            "source_id": "SRC1302_0_1301_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1301_NEXT_TARGET.csv",
            "needle": "NEXT1301_0_1302",
            "role": "handoff into parent fixed-field m signature or memory-stress split",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1302_1_1301_contract",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1301_PARENT_FIXED_FIELD_CLOSURE_CONTRACT.csv",
            "needle": "FFC1301_0_parent_field_status",
            "role": "unsigned fixed-field parent clauses from 1301",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1302_2_1301_stress_split",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1301_MEMORY_STRESS_SPLIT_LEDGER.csv",
            "needle": "MSS1301_1_memory_kinetic_stress",
            "role": "active memory stress separated from algebraic chain zero",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1302_3_826_ansatz",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_826_PARENT_ACTION_ANSATZ.csv",
            "needle": "AA826_1_memory_sector",
            "role": "candidate independent m scalar action scaffold",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1302_4_968_parent_domain",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_968_PARENT_DOMAIN_SIGNATURE_AUDIT.csv",
            "needle": "NOT_PARENT_SIGNED_CURRENT_CORPUS",
            "role": "parent-domain signature still not signed",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1302_5_969_owner_hunt",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_969_MEMORY_OPERATOR_OWNER_HUNT.csv",
            "needle": "NO_PARENT_MEMORY_OPERATOR_OWNER_FOUND_CURRENT_CORPUS",
            "role": "memory operator owner absent",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1302_6_970_quadratic_action",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_970_QUADRATIC_MEMORY_ACTION_CONSTRUCTION.csv",
            "needle": "CONSTRUCTION_RELATIVE_NOT_PARENT_CLOSED",
            "role": "relative memory action construction and stress/nohair blockers",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1302_7_967_positive_operator",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_967_MEMORY_POSITIVE_OPERATOR_LEMMA.csv",
            "needle": "RELATIVE_LEMMA_READY_PARENT_INPUTS_UNSIGNED",
            "role": "available no-hair theorem shape if parent inputs are supplied",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1302_8_1009_sector_contract",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1009_PARENT_SECTOR_CONTRACT.csv",
            "needle": "PCS1009_7_memory_response_doublet",
            "role": "parent sector ledger marks memory response as partial candidate not matched",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]
    for row in source_register:
        exists, needle_found = exists_and_contains(str(row["local_path"]), str(row["needle"]))
        row["exists"] = exists
        row["needle_found"] = needle_found

    fixed_field_signature_audit = [
        {
            "audit_id": "FFA1302_0_parent_field_status",
            "clause": "m is an independent parent scalar field admitted in S_parent before readout.",
            "supporting_evidence": "AA826_1 supplies a candidate L_m scaffold.",
            "blocking_evidence": "PDS968_6 and MOO969_7 say parent domain/operator owner is not signed.",
            "audit_result": "SUPPORTED_AS_CANDIDATE_NOT_SIGNED",
            "promotion_status": "DO_NOT_PROMOTE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "FFA1302_1_no_metric_composite",
            "clause": "m is not a metric norm, curvature scalar, Hodge/projector contraction, domain selector, or observed-source calibration.",
            "supporting_evidence": "Fixed-field branch in 1290/1301 identifies the sufficient condition.",
            "blocking_evidence": "Metric-composite counterbranch remains live and no parent field list excludes it.",
            "audit_result": "NOT_SIGNED_COUNTERBRANCH_LIVE",
            "promotion_status": "DO_NOT_PROMOTE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "FFA1302_2_variation_order",
            "clause": "Hilbert variation is done at fixed parent fields before readout/projection/domain reduction.",
            "supporting_evidence": "968 contains a relative readout-exclusion theorem shape.",
            "blocking_evidence": "968 also says parent domain signature and no-hidden-marker signatures are missing.",
            "audit_result": "RELATIVE_SCHEMA_ONLY",
            "promotion_status": "DO_NOT_PROMOTE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "FFA1302_3_units_frame_index",
            "clause": "local frame, signature, index placement, and units are locked.",
            "supporting_evidence": "1298/1300 identify the exact trace-reversal need.",
            "blocking_evidence": "no source in the current chain supplies the unit/index lock.",
            "audit_result": "MISSING_LOCK",
            "promotion_status": "DO_NOT_PROMOTE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "FFA1302_4_stress_split",
            "clause": "fixed-field chain zero is separated from the active m-sector Hilbert stress.",
            "supporting_evidence": "1301 split ledger and 970 relative action construction make the separation explicit.",
            "blocking_evidence": "stress channel itself is not zero or bounded.",
            "audit_result": "SPLIT_ACHIEVED_ZERO_NOT_ACHIEVED",
            "promotion_status": "PROMOTE_AS_NONCLAIM_GUARD_ONLY",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "FFA1302_5_verdict",
            "clause": "current corpus parent-signs fixed-field m enough to remove M_m^Sigma_abs from score ledgers.",
            "supporting_evidence": "conditional algebraic derivation from 1301 remains valid.",
            "blocking_evidence": "parent field status, no-composite exclusion, variation order, and frame/units are unsigned.",
            "audit_result": "FAIL_CURRENT_CORPUS_KEEP_CONDITIONAL_ONLY",
            "promotion_status": "NO_SCORE_NO_LOCAL_GR_CLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    memory_stress_residual = [
        {
            "residual_id": "MSR1302_0_canonical_scalar_stress_form",
            "object": "active memory scalar Hilbert stress",
            "formula": "T_m^{mu nu}=Z_m nabla^mu m nabla^nu m - g^{mu nu}[1/2 Z_m nabla_alpha m nabla^alpha m + V_R(m;X_B)] + T_ZX^{mu nu}+T_source/bath^{mu nu}+T_boundary^{mu nu}",
            "scope": "candidate scalar-memory parent action branch from 826/970",
            "needed_inputs": "MISSING_Z_m_SIGN_AND_VALUE;MISSING_V_R_SUBTRACTION;MISSING_X_B_METRIC_RESPONSE;MISSING_SOURCE_BATH_TERMS;MISSING_BOUNDARY_TERMS",
            "current_status": "HARD_RESIDUAL_CONTRACT_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "residual_id": "MSR1302_1_spatial_trace_bound_template",
            "object": "K_mem_stress^Sigma := sum_i K_mem_stress^{ii}",
            "formula": "|K_mem_stress^Sigma| <= |Z_m| sum_i |nabla^i m nabla^i m| + 3|1/2 Z_m (nabla m)^2 + V_R - V_ref| + |T_ZX^Sigma| + |T_source/bath^Sigma| + |T_boundary^Sigma|",
            "scope": "absolute-value local Kbar safety bound template",
            "needed_inputs": "MISSING_GRAD_m_BOUND;MISSING_Z_m_BOUND;MISSING_V_R_MINUS_V_REF_BOUND;MISSING_T_ZX_BOUND;MISSING_SOURCE_BATH_BOUND;MISSING_BOUNDARY_BOUND;MISSING_FRAME_UNITS",
            "current_status": "BOUND_TEMPLATE_NOT_SCOREABLE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "residual_id": "MSR1302_2_constant_nohair_safe_case",
            "object": "local constant/no-hair memory branch",
            "formula": "If nabla m=0, J_m=0, boundary flux=0, and V_R(m_*;X_B)-V_ref is constant/EH-subtracted, then K_mem_stress^Sigma=0 or cosmological-constant-only.",
            "scope": "sufficient theorem-zero route",
            "needed_inputs": "MISSING_PARENT_NOHAIR;MISSING_J_m_ZERO;MISSING_BOUNDARY_FLUX_ZERO;MISSING_EH_COMPATIBLE_SUBTRACTION;MISSING_X_B_DRIFT_ZERO",
            "current_status": "SUFFICIENT_ROUTE_PARENT_UNSIGNED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "residual_id": "MSR1302_3_metric_composite_fallback",
            "object": "metric-composite m response plus active stress",
            "formula": "If m=m[g,Phi,D,P], retain both M_m^Sigma_abs and K_mem_stress^Sigma until a parent definition supplies component bounds.",
            "scope": "fallback branch",
            "needed_inputs": "MISSING_PARENT_DEFINITION_OF_m;MISSING_RESPONSE_COMPONENTS;MISSING_STRESS_COMPONENTS",
            "current_status": "FALLBACK_RETAINED_NO_SCORE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    chain_pruning_status = [
        {
            "prune_id": "CP1302_0_m_chain_conditional_prune",
            "target": "STK1299_0_m_spatial_trace / M_m^Sigma_abs",
            "branch": "fixed independent parent scalar",
            "result": "can prune internally as M_m^Sigma_abs=0 only inside this branch",
            "promotion_limit": "not live-scoreable until FFA1302_0..3 become signed",
            "current_status": "CONDITIONAL_PRUNE_INTERNAL_ONLY",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "prune_id": "CP1302_1_m_chain_public_guard",
            "target": "local GR/Newton/PPN/R10 runners",
            "branch": "all branches",
            "result": "must still include missing m-chain or branch-selection guard",
            "promotion_limit": "no 00-only or fixed-field-only public pass",
            "current_status": "GUARD_ACTIVE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "prune_id": "CP1302_2_memory_stress_replacement",
            "target": "local Kbar bound assembly",
            "branch": "active independent m action",
            "result": "replace vague memory-stress concern with MSR1302 bound/nohair contract",
            "promotion_limit": "still not scoreable until bound/nohair inputs are supplied",
            "current_status": "HARD_CONTRACT_WRITTEN_NOT_SCORED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    local_nohair_requirements = [
        {
            "req_id": "NHM1302_0_operator_owner",
            "requirement": "parent action gives the m or X Euler equation L_m m = J_m in the local branch",
            "source_shape": "967/970",
            "current_status": "MISSING_PARENT_OWNER",
            "blocks": "cannot turn stress residual into no-hair theorem",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "req_id": "NHM1302_1_positive_gap",
            "requirement": "positive kinetic operator and mass/zero-mode gap",
            "source_shape": "MPO967_1;QMA970_2",
            "current_status": "MISSING_SIGN_AND_GAP",
            "blocks": "constant or ghostlike memory hair can survive",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "req_id": "NHM1302_2_source_silence",
            "requirement": "J_m=0 in ordinary compact local exterior, including no matter/source/bath/readout drive",
            "source_shape": "MPO967_3;QMA970_3",
            "current_status": "MISSING_ZERO_SOURCE_THEOREM",
            "blocks": "memory stress may be source driven",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "req_id": "NHM1302_3_boundary_zero",
            "requirement": "boundary flux/zero-mode/topological class is fixed to zero or source-independent constant",
            "source_shape": "MPO967_2;QMA970_4",
            "current_status": "MISSING_BOUNDARY_DATA",
            "blocks": "boundary hair can source local residuals",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "req_id": "NHM1302_4_potential_subtraction",
            "requirement": "constant V_R(m_*) piece is EH-compatible Lambda/background subtraction, not source normalization hair",
            "source_shape": "MR514_4;1301 stress split",
            "current_status": "MISSING_SUBTRACTION_OWNER",
            "blocks": "potential volume stress can remain in Kbar/source budget",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "req_id": "NHM1302_5_observable_projection",
            "requirement": "map any retained K_mem_stress into Newton/PPN/clock/R10/orbital tolerances with units",
            "source_shape": "local residual score gates",
            "current_status": "MISSING_ARENA_PROJECTIONS",
            "blocks": "finite residual cannot be scored",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    kbar_update = [
        {
            "update_id": "KBU1302_0_fixed_m_not_promoted",
            "target_row": "STK1299_0_m_spatial_trace",
            "update": "fixed-field m zero remains conditional branch pruning only",
            "still_missing": "MISSING_PARENT_FIXED_FIELD_SIGNATURE;MISSING_NO_METRIC_COMPOSITE_EXCLUSION;MISSING_VARIATION_ORDER_LOCK",
            "current_status": "NO_SCORE_CONDITIONAL_ONLY",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "update_id": "KBU1302_1_memory_stress_added",
            "target_row": "KBA1299_0_total_Kbar_abs_bound",
            "update": "add K_mem_stress^Sigma as a separate retained residual contract when independent m action is active",
            "still_missing": "MISSING_K_MEM_STRESS_BOUND_OR_NOHAIR;MISSING_LCG_SPATIAL_TRACE;MISSING_CDB_TRACE;MISSING_PROJECTOR_BOUNDARY",
            "current_status": "BOUND_ASSEMBLY_SHARPENED_NOT_SCOREABLE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "update_id": "KBU1302_2_metric_composite_guard",
            "target_row": "all local response runners",
            "update": "retain metric-composite branch as a hard blocker unless m is typed as parent scalar",
            "still_missing": "MISSING_PARENT_DEFINITION_OF_m",
            "current_status": "GUARD_ACTIVE_NO_LOCAL_GR_CLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    claim_gates = [
        {
            "gate_id": "CG1302_0_fixed_field_signature",
            "claim": "m is parent-signed as fixed independent scalar",
            "current_status": "FAIL_CURRENT_CORPUS",
            "reason": "826 is a scaffold, while 968/969/1009 say parent domain/operator/sector are not signed",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1302_1_chain_pruning",
            "claim": "M_m^Sigma_abs=0 may be used in scoring",
            "current_status": "BLOCKED_CONDITIONAL_ONLY",
            "reason": "branch selection is not parent-owned",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1302_2_memory_stress_contract",
            "claim": "memory stress residual has exact nonclaim contract",
            "current_status": "SATISFIED_FOR_NONCLAIM_CONTRACT",
            "reason": "MSR1302 rows define stress form, bound template, nohair route, and fallback",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1302_3_memory_nohair",
            "claim": "memory stress is zero or below local bounds",
            "current_status": "BLOCKED_INPUTS_MISSING",
            "reason": "operator owner, positive gap, source silence, boundary zero, subtraction owner, and arena projections missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1302_4_local_GR",
            "claim": "local GR/Newton/PPN recovery pass",
            "current_status": "BLOCKED_NO_LOCAL_GR_CLAIM",
            "reason": "fixed-field chain zero not promoted and retained memory/Lcg/CDB/projector/source-normalization inputs remain",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decision = [
        {
            "decision_id": "DEC1302_0_do_not_sign_m_yet",
            "decision": "do not parent-sign fixed-field m from current corpus",
            "because": "the existing evidence is a scaffold and relative theorem shape, not a closed parent field/domain/operator signature",
            "next_action": "carry fixed-field m as an internal conditional branch only",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1302_1_promote_stress_contract",
            "decision": "promote memory stress split as a hard nonclaim residual contract",
            "because": "this prevents the chain-zero lemma from erasing kinetic/potential/source/boundary stress",
            "next_action": "attack memory nohair/bound inputs directly",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_target = [
        {
            "next_id": "NEXT1302_0_1303",
            "target_file": "1303-Y5-R10-RAB-memory-stress-nohair-or-bound-inputs.md",
            "target_script": "scripts/Y5_R10_RAB_memory_stress_nohair_or_bound_inputs.py",
            "task": "try to close the retained K_mem_stress branch by deriving local no-hair/source-zero/boundary-zero/subtraction clauses; if that fails, stage concrete bound inputs for K_mem_stress^Sigma",
            "success_condition": "K_mem_stress^Sigma becomes theorem-zero under signed clauses or receives a source-backed nonclaim bound-input ledger",
            "do_not": "do not use the fixed-field chain zero to erase active memory Hilbert stress",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    write_csv(SOURCE_REGISTER_PATH, source_register)
    write_csv(FIXED_FIELD_SIGNATURE_AUDIT_PATH, fixed_field_signature_audit)
    write_csv(MEMORY_STRESS_RESIDUAL_PATH, memory_stress_residual)
    write_csv(CHAIN_PRUNING_STATUS_PATH, chain_pruning_status)
    write_csv(LOCAL_NOHAIR_REQUIREMENTS_PATH, local_nohair_requirements)
    write_csv(KBAR_UPDATE_PATH, kbar_update)
    write_csv(CLAIM_GATES_PATH, claim_gates)
    write_csv(DECISION_PATH, decision)
    write_csv(NEXT_PATH, next_target)

    validations = []
    source_count = len(source_register)
    source_hits = sum(1 for row in source_register if row["exists"] and row["needle_found"])
    validations.append(
        validation_row(
            "VAL1302_0_sources_exist",
            "registered source paths exist and anchors are found",
            source_hits == source_count,
            f"{source_hits}/{source_count} source anchors found",
        )
    )
    validations.append(
        validation_row(
            "VAL1302_1_fixed_field_not_signed",
            "fixed-field m signature is not promoted",
            any(row["audit_result"] == "FAIL_CURRENT_CORPUS_KEEP_CONDITIONAL_ONLY" for row in fixed_field_signature_audit)
            and not any(row["promotion_status"] == "PROMOTE_FOR_SCORE" for row in fixed_field_signature_audit),
            ";".join(str(row["audit_id"]) + "=" + str(row["audit_result"]) for row in fixed_field_signature_audit),
        )
    )
    validations.append(
        validation_row(
            "VAL1302_2_memory_stress_contract",
            "memory stress residual contract and bound template exist",
            any(row["residual_id"] == "MSR1302_0_canonical_scalar_stress_form" for row in memory_stress_residual)
            and any(row["residual_id"] == "MSR1302_1_spatial_trace_bound_template" for row in memory_stress_residual),
            ";".join(str(row["residual_id"]) for row in memory_stress_residual),
        )
    )
    validations.append(
        validation_row(
            "VAL1302_3_nohair_requirements_blocked",
            "memory nohair requirements remain explicit and blocked",
            len(local_nohair_requirements) == 6 and all(str(row["current_status"]).startswith("MISSING") for row in local_nohair_requirements),
            ";".join(str(row["req_id"]) + "=" + str(row["current_status"]) for row in local_nohair_requirements),
        )
    )
    validations.append(
        validation_row(
            "VAL1302_4_Kbar_not_scoreable",
            "Kbar update preview keeps scoring blocked",
            all("NO_SCORE" in str(row["current_status"]) or "NOT_SCOREABLE" in str(row["current_status"]) or "GUARD_ACTIVE" in str(row["current_status"]) for row in kbar_update),
            ";".join(str(row["update_id"]) + "=" + str(row["current_status"]) for row in kbar_update),
        )
    )
    generated_tables = [
        SOURCE_REGISTER_PATH,
        FIXED_FIELD_SIGNATURE_AUDIT_PATH,
        MEMORY_STRESS_RESIDUAL_PATH,
        CHAIN_PRUNING_STATUS_PATH,
        LOCAL_NOHAIR_REQUIREMENTS_PATH,
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
    validations.append(validation_row("VAL1302_5_csv_parse", "all generated CSVs parse cleanly", parse_ok, "; ".join(parse_details)))
    formalization_hits = generated_inside_formalization()
    validations.append(
        validation_row(
            "VAL1302_6_formalization_untouched",
            "formalization-workbench untouched by generated outputs",
            not formalization_hits,
            f"formalization_generated_output_count={len(formalization_hits)}",
        )
    )
    validations.append(
        validation_row(
            "VAL1302_7_nonclaim_policy",
            "all generated rows remain nonclaim",
            all_nonclaim(
                [
                    source_register,
                    fixed_field_signature_audit,
                    memory_stress_residual,
                    chain_pruning_status,
                    local_nohair_requirements,
                    kbar_update,
                    claim_gates,
                    decision,
                    next_target,
                ]
            ),
            "valid_for_claim=false and claim_allowed=false throughout generated tables",
        )
    )
    validations.append(
        validation_row(
            "VAL1302_8_next_target_1303",
            "next target routes to memory stress nohair or bound inputs",
            next_target[0]["next_id"] == "NEXT1302_0_1303" and "memory-stress-nohair" in str(next_target[0]["target_file"]),
            str(next_target[0]["target_file"]),
        )
    )
    overall_pass = all(row["status"] == "PASS" for row in validations)
    validations.append(
        validation_row(
            "VAL1302_9_overall",
            "overall 1302 validation",
            overall_pass,
            "1302 refuses to parent-sign fixed-field m from weak evidence, writes the hard memory-stress residual contract, keeps scoring blocked, and routes to nohair/bound inputs",
        )
    )
    write_csv(VALIDATION_PATH, validations)

    doc = f"""# 1302 Y5 R10 RAB parent fixed-field m signature or memory-stress split

Generated: `{RUN_STARTED_UTC.isoformat()}`

**Current verdict:** 1302 does not parent-sign `m` as a fixed independent scalar. The fixed-field result from 1301 remains mathematically useful, but only as an internal conditional branch. The live progress is that the active memory-sector Hilbert stress is now converted into a hard retained residual contract.

**Main progress:** the theory no longer has a vague gap called “memory stress.” The retained branch now has an explicit stress form and a spatial-trace bound template for `K_mem_stress^Sigma`, plus a clean no-hair route if the parent action later supplies operator owner, positivity, source silence, boundary zero, and EH-compatible subtraction.

**Still blocked:** no Newton/PPN/R10/local-GR score is allowed. `m` is not parent-signed as fixed-field, and `K_mem_stress^Sigma` is not zero or bounded.

## Source Register

{markdown_table(source_register, ["source_id", "local_path", "needle", "exists", "needle_found", "role", "valid_for_claim", "claim_allowed"])}

## Fixed-Field `m` Signature Audit

{markdown_table(fixed_field_signature_audit, ["audit_id", "clause", "supporting_evidence", "blocking_evidence", "audit_result", "promotion_status", "valid_for_claim", "claim_allowed"])}

## Memory Stress Residual Contract

{markdown_table(memory_stress_residual, ["residual_id", "object", "formula", "scope", "needed_inputs", "current_status", "valid_for_claim", "claim_allowed"])}

## Chain Pruning Status

{markdown_table(chain_pruning_status, ["prune_id", "target", "branch", "result", "promotion_limit", "current_status", "valid_for_claim", "claim_allowed"])}

## Memory-Stress No-Hair Requirements

{markdown_table(local_nohair_requirements, ["req_id", "requirement", "source_shape", "current_status", "blocks", "valid_for_claim", "claim_allowed"])}

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
