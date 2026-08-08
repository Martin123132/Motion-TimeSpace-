from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


PACK_ID = "P8_Y5_R10_1301"
TITLE = "1301-Y5-R10-RAB-parent-metric-response-components-for-m-spatial-trace"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_STARTED_UTC = datetime.now(timezone.utc)


SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
DERIVATION_ATTEMPT_PATH = OUT_DIR / f"{PACK_ID}_M_m_ij_DERIVATION_ATTEMPT.csv"
SPATIAL_TRACE_COMPONENT_PATH = OUT_DIR / f"{PACK_ID}_SPATIAL_TRACE_COMPONENT_RESULT_NONCLAIM.csv"
PARENT_CLOSURE_CONTRACT_PATH = OUT_DIR / f"{PACK_ID}_PARENT_FIXED_FIELD_CLOSURE_CONTRACT.csv"
STRESS_SPLIT_PATH = OUT_DIR / f"{PACK_ID}_MEMORY_STRESS_SPLIT_LEDGER.csv"
KBAR_UPDATE_PATH = OUT_DIR / f"{PACK_ID}_KBAR_UPDATE_PREVIEW_NONCLAIM.csv"
CLAIM_GATES_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATES.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1301_VALIDATION.csv"


def source_path(relative_path: str) -> Path:
    candidate_path = Path(relative_path)
    if candidate_path.is_absolute():
        return candidate_path
    return ROOT / candidate_path


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
    header = "| " + " | ".join(fields) + " |"
    divider = "| " + " | ".join(["---"] * len(fields)) + " |"
    body = ["| " + " | ".join(md_escape(row.get(field, "")) for field in fields) + " |" for row in rows]
    return "\n".join([header, divider, *body])


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
        DERIVATION_ATTEMPT_PATH,
        SPATIAL_TRACE_COMPONENT_PATH,
        PARENT_CLOSURE_CONTRACT_PATH,
        STRESS_SPLIT_PATH,
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
            "source_id": "SRC1301_0_1300_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1300_NEXT_TARGET.csv",
            "needle": "NEXT1300_0_1301",
            "role": "handoff into parent m metric-response component derivation",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1301_1_1300_input_row",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1300_SUM_i_M_m_ii_INPUT_ROW_NONCLAIM.csv",
            "needle": "M_m^Sigma_abs",
            "role": "exact first missing spatial trace input",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1301_2_1290_metric_audit",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1290_METRIC_KERNEL_AUDIT.csv",
            "needle": "MKA1290_0_fixed_field_scalar_branch",
            "role": "conditional fixed-field scalar zero lemma for chain kernels",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1301_3_1289_variation",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1289_KMETRIC_VARIATION_EXPANSION_NONCLAIM.csv",
            "needle": "delta Gamma_eff=L_cg^-2 F_prime(m) delta m",
            "role": "chain-rule metric variation to be component-generalized",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1301_4_1288_blocker",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1288_KMETRIC_DERIVATIVE_TERM_BLOCKER.csv",
            "needle": "MISSING_METRIC_VARIATION_OF_m_AND_L_cg",
            "role": "active blocker showing metric variation laws are not parent-signed",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1301_5_826_action_ansatz",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_826_PARENT_ACTION_ANSATZ.csv",
            "needle": "L_m = -1/2 Z_m(X_B) nabla_mu m nabla^mu m - V_R(m;X_B)",
            "role": "candidate independent memory-scalar parent action scaffold",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1301_6_970_memory_action",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_970_QUADRATIC_MEMORY_ACTION_CONSTRUCTION.csv",
            "needle": "CONSTRUCTION_RELATIVE_NOT_PARENT_CLOSED",
            "role": "memory stress/operator branch remains relative, not parent closed",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1301_7_968_operator_inputs",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_968_MEMORY_OPERATOR_INPUT_AUDIT.csv",
            "needle": "INPUTS_MISSING_NO_THEOREM_ZERO",
            "role": "missing inputs for a real memory scalar no-hair theorem",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1301_8_1299_trace_gate",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1299_TRACE_THEOREM_AUDIT.csv",
            "needle": "FAIL_CURRENT_CORPUS_KEEP_SPATIAL_TRACE_ROWS",
            "role": "guard against replacing spatial trace with unearned isotropy/trace theorem",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]
    for row in source_register:
        exists, needle_found = exists_and_contains(str(row["local_path"]), str(row["needle"]))
        row["exists"] = exists
        row["needle_found"] = needle_found

    derivation_attempt = [
        {
            "derivation_id": "DRV1301_0_fixed_independent_scalar_chain",
            "target": "M_m^{ij} inside delta Gamma_eff",
            "premise": "m is an independent parent scalar field held fixed in the Hilbert metric variation of the algebraic Gamma_eff term.",
            "derivation": "delta_g Gamma_eff|chain = L_cg^-2 F_prime(m) delta_g m. At fixed parent fields delta_g m=0, so M_m^{mu nu}:=delta_g m/delta g_{mu nu}=0 for all components, including ij.",
            "result": "M_m^{ij}=0 and M_m^Sigma_abs=0 for the algebraic Gamma_eff chain only.",
            "status": "RELATIVE_DERIVED_UNDER_UNSIGNED_PARENT_CLAUSE",
            "why_not_claim": "current corpus has not parent-signed that m is fixed-field rather than metric-composite/readout/domain/projector data.",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1290_METRIC_KERNEL_AUDIT.csv;source-intake/mts_residuals/P8_Y5_R10_1289_KMETRIC_VARIATION_EXPANSION_NONCLAIM.csv",
            "source_anchor": "MKA1290_0_fixed_field_scalar_branch;KVE1289_1_chain_rule_scalar_variation",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "derivation_id": "DRV1301_1_metric_composite_counterbranch",
            "target": "M_m^{ij}",
            "premise": "m is a metric-composite readout, norm, curvature scalar, projector contraction, or domain-selected scalar.",
            "derivation": "Then delta_g m contains explicit metric/projector/connection variation, so M_m^{ij} is generally nonzero and must be bounded rather than set to zero.",
            "result": "M_m^Sigma_abs retained as a real residual input.",
            "status": "COUNTERBRANCH_RETAINED",
            "why_not_claim": "no source chooses between fixed independent scalar and metric-composite m.",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1290_METRIC_KERNEL_AUDIT.csv;source-intake/mts_residuals/P8_Y5_R10_1288_KMETRIC_DERIVATIVE_TERM_BLOCKER.csv",
            "source_anchor": "MKA1290_1_m_metric_composite_branch;KMR1288_1_Gamma_metric_dependence",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "derivation_id": "DRV1301_2_active_memory_stress_split",
            "target": "stress of the m-sector parent action",
            "premise": "m is independent but has its own kinetic/potential parent action L_m.",
            "derivation": "The fixed-field zero kills only the chain response delta_g m in Gamma_eff. The Hilbert variation of L_m still produces memory-sector stress through metric contraction of gradients, potential volume terms, boundary terms, and source/bath pieces.",
            "result": "route kinetic/potential stress to K_mem_stress/CDB residuals, not to M_m^Sigma_abs.",
            "status": "SEPARATE_STRESS_CHANNEL_REQUIRED",
            "why_not_claim": "local no-hair/source-zero/boundary-zero theorem for L_m is still unsigned.",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_826_PARENT_ACTION_ANSATZ.csv;source-intake/mts_residuals/P8_Y5_R10_970_QUADRATIC_MEMORY_ACTION_CONSTRUCTION.csv",
            "source_anchor": "AA826_1_memory_sector;QMA970_7_verdict",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "derivation_id": "DRV1301_3_strict_double_zero_backup",
            "target": "m-chain first variation",
            "premise": "local branch locks m=m_* and F_prime(m_*)=0, or stronger F(m_*)=F_prime(m_*)=0.",
            "derivation": "The factor F_prime(m_*) kills the m-chain term even if M_m^{ij} is finite; strict double zero also helps the L_cg chain.",
            "result": "backup zero route, independent of the fixed-field scalar branch, but still parent-unsigned.",
            "status": "SUFFICIENT_BUT_NOT_PARENT_DERIVED",
            "why_not_claim": "parent lock to m_* and F shape are not derived from the current action.",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1290_METRIC_KERNEL_AUDIT.csv;source-intake/mts_residuals/P8_Y5_R10_798_GAMMA_SOURCE_EXPANSION.csv",
            "source_anchor": "MKA1290_3_strict_double_zero_branch;GSE798_2_local_locked_expansion",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    spatial_trace_component = [
        {
            "component_id": "MMIJ1301_0_fixed_field_component_zero",
            "target_input": "M_m^Sigma_abs",
            "component_law": "If m is a fixed independent parent scalar in the algebraic Gamma_eff metric variation, then M_m^{11}=M_m^{22}=M_m^{33}=0.",
            "trace_result": "M_m^Sigma_abs := sum_i |M_m^{ii}| = 0",
            "scope": "algebraic Gamma_eff chain response only",
            "remaining_channels": "memory-sector Hilbert stress; derivative/projector/domain/boundary stress; L_cg chain; CDB spatial trace",
            "required_parent_clauses": "FFC1301_0;FFC1301_1;FFC1301_2;FFC1301_3;FFC1301_4",
            "current_status": "RELATIVE_ZERO_RESULT_NOT_PARENT_SIGNED",
            "usable_for_scoring": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "component_id": "MMIJ1301_1_metric_composite_retention",
            "target_input": "M_m^Sigma_abs",
            "component_law": "If m depends on g, curvature, projector geometry, domain data, or readout norms, no zero follows.",
            "trace_result": "M_m^Sigma_abs must be bounded or sourced explicitly",
            "scope": "retained counterbranch",
            "remaining_channels": "metric-composite response coefficients and units",
            "required_parent_clauses": "explicit m[g,Phi,D,P] definition and local frame/index convention",
            "current_status": "RETAINED_NONCLAIM_COUNTERBRANCH",
            "usable_for_scoring": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    parent_closure_contract = [
        {
            "clause_id": "FFC1301_0_parent_field_status",
            "clause": "m is an admitted independent parent scalar field, not a post-variation readout or fitted function.",
            "needed_to_promote": "delta_g m=0 at fixed fields",
            "current_evidence": "826 gives an ansatz scaffold; 968/969 say owner is missing.",
            "status": "UNSIGNED",
            "if_missing": "M_m^{ij} remains a live response kernel",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "clause_id": "FFC1301_1_no_metric_composite",
            "clause": "m is not a metric norm, curvature scalar, Hodge/projector contraction, domain selector, or observed-source calibration.",
            "needed_to_promote": "rules out hidden delta_g m terms",
            "current_evidence": "1290 explicitly retains the metric-composite counterbranch.",
            "status": "UNSIGNED",
            "if_missing": "spatial metric-response components must be bounded",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "clause_id": "FFC1301_2_variation_order",
            "clause": "Hilbert variation of Gamma_eff is performed at fixed parent fields before readout/projection/domain reduction.",
            "needed_to_promote": "prevents readout-after-variation leakage from re-entering M_m^{ij}",
            "current_evidence": "968 parent-domain signature is not parent-signed.",
            "status": "UNSIGNED",
            "if_missing": "post-variation selectors can fake a nonzero response",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "clause_id": "FFC1301_3_units_frame_index_lock",
            "clause": "local coframe, signature, index placement, and units of M_m^{mu nu} are fixed.",
            "needed_to_promote": "makes M_m^Sigma_abs comparable to Kbar_00 trace reversal",
            "current_evidence": "1298 and 1300 still mark index/unit locks missing.",
            "status": "UNSIGNED",
            "if_missing": "zero branch may be notation-only rather than tensor-slot valid",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "clause_id": "FFC1301_4_stress_channel_split",
            "clause": "any kinetic/potential/bath/source stress of L_m is routed into a separate memory-stress residual ledger and not silently deleted.",
            "needed_to_promote": "keeps fixed-field chain zero from pretending the whole memory sector is absent",
            "current_evidence": "970 says memory action construction is relative, not parent closed.",
            "status": "UNSIGNED",
            "if_missing": "local GR pass would smuggle away the actual m Hilbert stress",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    stress_split = [
        {
            "split_id": "MSS1301_0_chain_response",
            "object": "delta_g Gamma_eff chain term",
            "response_piece": "L_cg^-2 F_prime(m) delta_g m",
            "fixed_field_result": "zero if FFC1301_0..3 hold",
            "where_it_lands": "M_m^Sigma_abs / STK1299_0",
            "current_status": "RELATIVE_ZERO_NOT_SCOREABLE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "split_id": "MSS1301_1_memory_kinetic_stress",
            "object": "L_m kinetic term",
            "response_piece": "delta_g[-1/2 Z_m g^{mu nu} nabla_mu m nabla_nu m]",
            "fixed_field_result": "not zero unless local no-hair/constant m and boundary/source silence are proved",
            "where_it_lands": "K_mem_stress / CDB / retained local residual",
            "current_status": "RETAINED_NEEDS_NOHAIR_OR_BOUND",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "split_id": "MSS1301_2_memory_potential_volume",
            "object": "L_m potential term",
            "response_piece": "delta_g[-V_R(m;X_B)] through sqrt(-g) and X_B/baseline dependence",
            "fixed_field_result": "constant piece needs EH-compatible subtraction; nonconstant X_B/m drift remains",
            "where_it_lands": "background subtraction / source normalization / K_mem_stress",
            "current_status": "RETAINED_NEEDS_BACKGROUND_AND_DRIFT_GATES",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "split_id": "MSS1301_3_boundary_source_bath",
            "object": "boundary/source/bath terms",
            "response_piece": "J_X, boundary flux, readout, history, or bath variation",
            "fixed_field_result": "not controlled by the algebraic chain zero",
            "where_it_lands": "boundary/projector/domain residuals and memory no-hair inputs",
            "current_status": "RETAINED_NEEDS_PARENT_SOURCE_SILENCE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    kbar_update = [
        {
            "update_id": "KBU1301_0_conditional_m_spatial_trace_zero",
            "target_row": "STK1299_0_m_spatial_trace",
            "new_result": "M_m^Sigma_abs=0 under fixed independent scalar chain clause",
            "allowed_use": "internal branch pruning only",
            "why_not_score": "parent fixed-field clauses are unsigned and memory stress remains separate",
            "current_status": "CONDITIONAL_BRANCH_RESULT_NOT_PROMOTED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "update_id": "KBU1301_1_counterbranch_retained",
            "target_row": "STK1299_0_m_spatial_trace",
            "new_result": "if m is metric-composite, M_m^Sigma_abs remains missing",
            "allowed_use": "blocker ledger and future bound input",
            "why_not_score": "no parent definition selects fixed-field vs metric-composite",
            "current_status": "COUNTERBRANCH_RETAINS_MISSING_INPUT",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "update_id": "KBU1301_2_total_Kbar_guard",
            "target_row": "KBA1299_0_total_Kbar_abs_bound",
            "new_result": "m-chain spatial trace can be conditionally killed but Lcg/CDB/projector and memory-stress channels remain",
            "allowed_use": "route selection for 1302",
            "why_not_score": "full Kbar_00 still lacks other spatial trace and source-normalization inputs",
            "current_status": "NO_SCORE_TOTAL_KBAR_STILL_BLOCKED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    claim_gates = [
        {
            "gate_id": "CG1301_0_relative_derivation",
            "claim": "M_m^{ij}=0 under fixed independent scalar variation",
            "current_status": "RELATIVE_DERIVATION_PASS",
            "reason": "fixed-field Hilbert variation gives delta_g m=0 componentwise",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1301_1_parent_signature",
            "claim": "m is parent-signed as fixed independent scalar for the Gamma_eff chain",
            "current_status": "BLOCKED_UNSIGNED_PARENT_CLAUSES",
            "reason": "current corpus retains metric-composite/readout/domain/projector counterbranches",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1301_2_memory_stress",
            "claim": "m-sector kinetic/potential/source stress is zero or bounded",
            "current_status": "BLOCKED_SEPARATE_STRESS_CHANNEL",
            "reason": "chain zero does not erase Hilbert stress of L_m",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1301_3_first_trace_input",
            "claim": "M_m^Sigma_abs is resolved for scoring",
            "current_status": "BLOCKED_CONDITIONAL_ONLY",
            "reason": "one clean branch exists, but branch selection is not parent-owned",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1301_4_local_GR",
            "claim": "local GR/Newton/PPN recovery pass",
            "current_status": "BLOCKED_NO_LOCAL_GR_CLAIM",
            "reason": "Lcg spatial trace, CDB trace, projector boundary, source normalization, and memory stress remain unresolved",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decision = [
        {
            "decision_id": "DEC1301_0_branch_pruning_progress",
            "decision": "record fixed-field m as a mathematically clean relative zero branch",
            "because": "it gives M_m^{ij}=0 componentwise without isotropy/tracefree smuggling",
            "next_action": "try to parent-sign fixed-field m and split active memory stress into its own residual row",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1301_1_no_public_promotion",
            "decision": "do not promote M_m^Sigma_abs=0 to the live local-GR runner",
            "because": "the parent action has not chosen fixed independent m over metric-composite m",
            "next_action": "build a parent m-status signature gate before removing the missing input from score ledgers",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_target = [
        {
            "next_id": "NEXT1301_0_1302",
            "target_file": "1302-Y5-R10-RAB-parent-fixed-field-m-signature-or-memory-stress-split.md",
            "target_script": "scripts/Y5_R10_RAB_parent_fixed_field_m_signature_or_memory_stress_split.py",
            "task": "try to parent-sign m as a fixed independent scalar for the Gamma_eff chain; if not, split the active memory Hilbert stress into a retained residual input with exact clauses",
            "success_condition": "either FFC1301_0..4 become source-backed enough for nonclaim branch pruning, or the metric-composite/memory-stress branch receives a hard closure/bound contract",
            "do_not": "do not treat the fixed-field chain zero as a full memory-sector/local-GR pass",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    write_csv(SOURCE_REGISTER_PATH, source_register)
    write_csv(DERIVATION_ATTEMPT_PATH, derivation_attempt)
    write_csv(SPATIAL_TRACE_COMPONENT_PATH, spatial_trace_component)
    write_csv(PARENT_CLOSURE_CONTRACT_PATH, parent_closure_contract)
    write_csv(STRESS_SPLIT_PATH, stress_split)
    write_csv(KBAR_UPDATE_PATH, kbar_update)
    write_csv(CLAIM_GATES_PATH, claim_gates)
    write_csv(DECISION_PATH, decision)
    write_csv(NEXT_PATH, next_target)

    validations = []
    source_count = len(source_register)
    source_hits = sum(1 for row in source_register if row["exists"] and row["needle_found"])
    validations.append(
        validation_row(
            "VAL1301_0_sources_exist",
            "registered source paths exist and anchors are found",
            source_hits == source_count,
            f"{source_hits}/{source_count} source anchors found",
        )
    )
    validations.append(
        validation_row(
            "VAL1301_1_relative_fixed_field_derivation",
            "fixed-field scalar branch derives componentwise M_m^{ij}=0 only relatively",
            any(row["derivation_id"] == "DRV1301_0_fixed_independent_scalar_chain" and row["status"] == "RELATIVE_DERIVED_UNDER_UNSIGNED_PARENT_CLAUSE" for row in derivation_attempt),
            ";".join(str(row["derivation_id"]) + "=" + str(row["status"]) for row in derivation_attempt),
        )
    )
    validations.append(
        validation_row(
            "VAL1301_2_counterbranch_retained",
            "metric-composite counterbranch remains retained",
            any(row["derivation_id"] == "DRV1301_1_metric_composite_counterbranch" and row["status"] == "COUNTERBRANCH_RETAINED" for row in derivation_attempt),
            "counterbranch prevents premature M_m^Sigma_abs=0 promotion",
        )
    )
    validations.append(
        validation_row(
            "VAL1301_3_stress_split",
            "memory stress is split away from algebraic chain zero",
            len(stress_split) == 4 and any(row["split_id"] == "MSS1301_1_memory_kinetic_stress" for row in stress_split),
            ";".join(str(row["split_id"]) for row in stress_split),
        )
    )
    validations.append(
        validation_row(
            "VAL1301_4_parent_clauses_unsigned",
            "parent fixed-field closure clauses remain unsigned",
            len(parent_closure_contract) == 5 and all(row["status"] == "UNSIGNED" for row in parent_closure_contract),
            ";".join(str(row["clause_id"]) + "=" + str(row["status"]) for row in parent_closure_contract),
        )
    )
    validations.append(
        validation_row(
            "VAL1301_5_Kbar_not_scoreable",
            "Kbar update preview keeps scoring blocked",
            all("NO_SCORE" in str(row["current_status"]) or "NOT_PROMOTED" in str(row["current_status"]) or "RETAINS_MISSING" in str(row["current_status"]) for row in kbar_update),
            ";".join(str(row["update_id"]) + "=" + str(row["current_status"]) for row in kbar_update),
        )
    )
    generated_tables = [
        SOURCE_REGISTER_PATH,
        DERIVATION_ATTEMPT_PATH,
        SPATIAL_TRACE_COMPONENT_PATH,
        PARENT_CLOSURE_CONTRACT_PATH,
        STRESS_SPLIT_PATH,
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
    validations.append(validation_row("VAL1301_6_csv_parse", "all generated CSVs parse cleanly", parse_ok, "; ".join(parse_details)))
    formalization_hits = generated_inside_formalization()
    validations.append(
        validation_row(
            "VAL1301_7_formalization_untouched",
            "formalization-workbench untouched by generated outputs",
            not formalization_hits,
            f"formalization_generated_output_count={len(formalization_hits)}",
        )
    )
    validations.append(
        validation_row(
            "VAL1301_8_nonclaim_policy",
            "all generated rows remain nonclaim",
            all_nonclaim([source_register, derivation_attempt, spatial_trace_component, parent_closure_contract, stress_split, kbar_update, claim_gates, decision, next_target]),
            "valid_for_claim=false and claim_allowed=false throughout generated tables",
        )
    )
    validations.append(
        validation_row(
            "VAL1301_9_next_target_1302",
            "next target routes to parent fixed-field m signature or memory-stress split",
            next_target[0]["next_id"] == "NEXT1301_0_1302" and "fixed-field-m" in str(next_target[0]["target_file"]),
            str(next_target[0]["target_file"]),
        )
    )
    overall_pass = all(row["status"] == "PASS" for row in validations)
    validations.append(
        validation_row(
            "VAL1301_10_overall",
            "overall 1301 validation",
            overall_pass,
            "1301 derives a relative componentwise fixed-field chain zero, retains metric-composite/stress counterbranches, blocks scoring, and routes to parent signature or stress split",
        )
    )
    write_csv(VALIDATION_PATH, validations)

    doc = f"""# 1301 Y5 R10 RAB parent metric-response components for m spatial trace

Generated: `{RUN_STARTED_UTC.isoformat()}`

**Current verdict:** 1301 gets a real conditional derivation: if `m` is an independent parent scalar held fixed during the Hilbert metric variation of the algebraic `Gamma_eff` term, then `delta_g m=0`, so `M_m^{{ij}}=0` componentwise and `M_m^Sigma_abs=0`. This is only a relative branch, not a live claim.

**Main progress:** the first spatial trace blocker now has a clean branch split. The fixed-field chain route kills `M_m^Sigma_abs` without using an isotropy/tracefree shortcut. The metric-composite/readout route keeps `M_m^Sigma_abs` live. The active memory action route is split into a separate Hilbert-stress residual so we do not delete real physics by notation.

**Still blocked:** the parent action has not signed that `m` is fixed-field rather than metric-composite, and the kinetic/potential/source/boundary stress of any `m` action is not zero/bounded. No Newton/PPN/R10/local-GR score is allowed.

## Source Register

{markdown_table(source_register, ["source_id", "local_path", "needle", "exists", "needle_found", "role", "valid_for_claim", "claim_allowed"])}

## `M_m^{{ij}}` Derivation Attempt

{markdown_table(derivation_attempt, ["derivation_id", "target", "premise", "derivation", "result", "status", "why_not_claim", "source_path", "source_anchor", "valid_for_claim", "claim_allowed"])}

## Spatial Trace Component Result

{markdown_table(spatial_trace_component, ["component_id", "target_input", "component_law", "trace_result", "scope", "remaining_channels", "required_parent_clauses", "current_status", "usable_for_scoring", "valid_for_claim", "claim_allowed"])}

## Parent Fixed-Field Closure Contract

{markdown_table(parent_closure_contract, ["clause_id", "clause", "needed_to_promote", "current_evidence", "status", "if_missing", "valid_for_claim", "claim_allowed"])}

## Memory Stress Split Ledger

{markdown_table(stress_split, ["split_id", "object", "response_piece", "fixed_field_result", "where_it_lands", "current_status", "valid_for_claim", "claim_allowed"])}

## Kbar Update Preview

{markdown_table(kbar_update, ["update_id", "target_row", "new_result", "allowed_use", "why_not_score", "current_status", "valid_for_claim", "claim_allowed"])}

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
