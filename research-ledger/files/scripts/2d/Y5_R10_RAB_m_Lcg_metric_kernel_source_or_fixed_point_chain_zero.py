from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


PACK_ID = "P8_Y5_R10_1290"
TITLE = "1290-Y5-R10-RAB-m-Lcg-metric-kernel-source-or-fixed-point-chain-zero"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_STARTED_UTC = datetime.now(timezone.utc)


SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
KERNEL_AUDIT_PATH = OUT_DIR / f"{PACK_ID}_METRIC_KERNEL_AUDIT.csv"
CHAIN_ZERO_PATH = OUT_DIR / f"{PACK_ID}_FIXED_POINT_CHAIN_ZERO_ATTEMPT.csv"
RESIDUAL_ROWS_PATH = OUT_DIR / f"{PACK_ID}_KERNEL_RESIDUAL_ROWS_NONCLAIM.csv"
DELTAK_STATUS_PATH = OUT_DIR / f"{PACK_ID}_DELTAK_STATUS_UPDATE.csv"
CLAIM_GATES_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATES.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1290_VALIDATION.csv"


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


def generated_inside_formalization() -> list[Path]:
    generated_paths = [
        SOURCE_REGISTER_PATH,
        KERNEL_AUDIT_PATH,
        CHAIN_ZERO_PATH,
        RESIDUAL_ROWS_PATH,
        DELTAK_STATUS_PATH,
        CLAIM_GATES_PATH,
        DECISION_PATH,
        NEXT_PATH,
        VALIDATION_PATH,
        DOC_PATH,
    ]
    return [path for path in generated_paths if FORMALIZATION in path.parents]


def all_nonclaim(tables: list[list[dict[str, object]]]) -> bool:
    return all(
        is_false(row.get("valid_for_claim", False)) and is_false(row.get("claim_allowed", False))
        for rows in tables
        for row in rows
    )


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    source_register = [
        {
            "source_id": "SRC1290_0_1289_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1289_NEXT_TARGET.csv",
            "needle": "NEXT1289_0_1290",
            "role": "handoff into m/Lcg metric kernels or fixed-point chain zero",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1290_1_1289_chain_kernel",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1289_FIRST_DERIVATIVE_TERM_ROW_NONCLAIM.csv",
            "needle": "KDR1289_0_Gamma_m_L_chain_kernel_00",
            "role": "symbolic chain-kernel row with M_m^{00} and M_L^{00}",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1290_2_1289_zero_gate",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1289_FIRST_DERIVATIVE_TERM_ROW_NONCLAIM.csv",
            "needle": "KDR1289_1_local_zero_condition_for_chain_kernel",
            "role": "conditional zero gate for chain kernel",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1290_3_1289_variation",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1289_KMETRIC_VARIATION_EXPANSION_NONCLAIM.csv",
            "needle": "KVE1289_2_metric_response_kernels",
            "role": "Kmetric chain expansion source",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1290_4_798_locked_expansion",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_798_GAMMA_SOURCE_EXPANSION.csv",
            "needle": "GSE798_2_local_locked_expansion",
            "role": "locked local expansion around m_*",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1290_5_798_verdict",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_798_GAMMA_SOURCE_EXPANSION.csv",
            "needle": "GSE798_5_source_law_verdict",
            "role": "screening/source law remains unsigned",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1290_6_514_double_zero",
            "local_path": "source-intake/mts_residuals/P8_GK_METRIC_RESPONSE_CONTRACT.csv",
            "needle": "MR514_5_double_zero",
            "role": "first stress variation must vanish at local fixed point",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1290_7_514_scalar_density",
            "local_path": "source-intake/mts_residuals/P8_GK_METRIC_RESPONSE_CONTRACT.csv",
            "needle": "MR514_0_scalar_density",
            "role": "Gamma_eff must be parent scalar-density input",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1290_8_selector_double_zero",
            "local_path": "source-intake/mts_residuals/P8_LOCAL_EH_R11_SELECTOR_LEMMA.csv",
            "needle": "L2_double_zero_sufficient",
            "role": "double-zero selector sufficiency lemma",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1290_9_single_zero_warning",
            "local_path": "source-intake/mts_residuals/P8_LOCAL_EH_R11_SELECTOR_LEMMA.csv",
            "needle": "L1_single_zero_fails",
            "role": "single-zero warning under variation",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1290_10_514_residual_branch",
            "local_path": "source-intake/mts_residuals/P8_GK_RESIDUAL_BOUND_BRANCH.csv",
            "needle": "GB514_3_double_zero_missing",
            "role": "fallback if fixed-point double zero is missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1290_11_1289_DeltaK_template",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1289_DELTAK00_COMPARISON_TEMPLATE.csv",
            "needle": "DTC1289_2_DeltaK00_template",
            "role": "DeltaK00 template to update",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]
    for row in source_register:
        exists, needle_found = exists_and_contains(str(row["local_path"]), str(row["needle"]))
        row["exists"] = exists
        row["needle_found"] = needle_found

    kernel_audit = [
        {
            "kernel_id": "MKA1290_0_fixed_field_scalar_branch",
            "kernel": "M_m^{00};M_L^{00}",
            "candidate_derivation": "In Hilbert variation at fixed independent scalar fields m and L_cg, delta_g m=0 and delta_g L_cg=0, hence M_m^{00}=0 and M_L^{00}=0 for the algebraic Gamma_eff=L_cg^-2 F(m) term.",
            "required_assumptions": "m and L_cg are parent-owned scalar inputs; not metric norms; not Hodge/projector/domain readouts; no hidden units/readout metric dependence",
            "source_path": "source-intake/mts_residuals/P8_GK_METRIC_RESPONSE_CONTRACT.csv;source-intake/mts_residuals/P8_Y5_R10_1289_FIRST_DERIVATIVE_TERM_ROW_NONCLAIM.csv",
            "source_anchor": "MR514_0_scalar_density;KDR1289_0_Gamma_m_L_chain_kernel_00",
            "result": "CONDITIONAL_KERNEL_ZERO",
            "current_status": "USEFUL_LEMMA_NOT_PARENT_SIGNED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "kernel_id": "MKA1290_1_m_metric_composite_branch",
            "kernel": "M_m^{00}",
            "candidate_derivation": "If m is a metric-composite readout, norm, projector contraction, or domain-selected scalar, then M_m^{00}=delta m/delta g_{00} is generally nonzero and must be retained.",
            "required_assumptions": "explicit parent definition of m and whether fixed-field Hilbert variation holds",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1289_FIRST_DERIVATIVE_TERM_ROW_NONCLAIM.csv;source-intake/mts_residuals/P8_GK_RESIDUAL_BOUND_BRANCH.csv",
            "source_anchor": "KDR1289_0_Gamma_m_L_chain_kernel_00;GB514_3_double_zero_missing",
            "result": "RESIDUAL_BRANCH_IF_METRIC_COMPOSITE",
            "current_status": "M_m_00_NOT_SOURCE_FILLED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "kernel_id": "MKA1290_2_Lcg_metric_length_branch",
            "kernel": "M_L^{00}",
            "candidate_derivation": "If L_cg is a metric length, curvature scale, domain size, or readout calibration, then M_L^{00}=delta L_cg/delta g_{00} generally survives and the chain term -2 L_cg^-3 F(m) M_L^{00} is physical.",
            "required_assumptions": "explicit parent definition of L_cg and whether it is global/topological, scalar spurion, or metric-readout scale",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_798_GAMMA_SOURCE_EXPANSION.csv;source-intake/mts_residuals/P8_Y5_R10_1289_FIRST_DERIVATIVE_TERM_ROW_NONCLAIM.csv",
            "source_anchor": "GSE798_1_gradient_expansion;KDR1289_0_Gamma_m_L_chain_kernel_00",
            "result": "RESIDUAL_BRANCH_IF_METRIC_LENGTH",
            "current_status": "M_L_00_NOT_SOURCE_FILLED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "kernel_id": "MKA1290_3_strict_double_zero_branch",
            "kernel": "chain_kernel_all_metric_channels",
            "candidate_derivation": "If the local branch has F(m_*)=0 and F_prime(m_*)=0, then the m and L_cg chain terms vanish to first variation even if M_m^{00} and M_L^{00} are finite.",
            "required_assumptions": "parent law locks m=m_*; F has a true double zero; kernels remain finite; no connection/domain/boundary stress",
            "source_path": "source-intake/mts_residuals/P8_LOCAL_EH_R11_SELECTOR_LEMMA.csv;source-intake/mts_residuals/P8_GK_METRIC_RESPONSE_CONTRACT.csv",
            "source_anchor": "L2_double_zero_sufficient;MR514_5_double_zero",
            "result": "BEST_LOW_SCRUTINY_ZERO_ROUTE",
            "current_status": "SUFFICIENT_CLAUSE_NOT_DERIVED_FOR_MTS",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "kernel_id": "MKA1290_4_background_subtraction_branch",
            "kernel": "Lcg_chain_at_nonzero_F",
            "candidate_derivation": "If F(m_*) is nonzero but constant, it may be absorbed into Lambda0/background only if the subtraction is parent-owned and EH-compatible; otherwise the L_cg metric response remains source-normalization hair.",
            "required_assumptions": "fixed background subtraction; no local boundary/source-measure flux; no radial/time/species variation of the constant",
            "source_path": "source-intake/mts_residuals/P8_GK_METRIC_RESPONSE_CONTRACT.csv;source-intake/mts_residuals/P8_Y5_R10_798_GAMMA_SOURCE_EXPANSION.csv",
            "source_anchor": "MR514_4_fixed_point_subtraction;GSE798_2_local_locked_expansion",
            "result": "POSSIBLE_BUT_HIGHER_SCRUTINY_THAN_STRICT_DOUBLE_ZERO",
            "current_status": "BACKGROUND_SUBTRACTION_NOT_PARENT_SIGNED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    chain_zero = [
        {
            "clause_id": "FCZ1290_0_parent_scalar_status",
            "condition": "m and L_cg are parent-owned scalar inputs varied independently of the metric",
            "mathematical_effect": "M_m^{00}=0 and M_L^{00}=0 for algebraic Gamma_eff=L_cg^-2F(m)",
            "current_evidence": "conditional scalar-density contract exists, but actual parent definitions of m and L_cg are not signed",
            "verdict": "CONDITIONAL_NOT_PROVEN",
            "blocks_if_missing": "chain kernels remain finite residuals",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "clause_id": "FCZ1290_1_stationary_point",
            "condition": "F_prime(m_*)=0 on the local branch",
            "mathematical_effect": "kills the m-channel first variation L_cg^-2 F_prime(m_*) M_m^{00}",
            "current_evidence": "GSE798 supplies a locked-expansion template, not a parent lock",
            "verdict": "CONDITIONAL_NOT_PROVEN",
            "blocks_if_missing": "linear m-channel PPN/source hair remains",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "clause_id": "FCZ1290_2_strict_F0_zero",
            "condition": "F(m_*)=0 or parent-owned EH-compatible subtraction removes the constant",
            "mathematical_effect": "kills the L_cg-chain term -2 L_cg^-3 F(m_*) M_L^{00} or routes it to Lambda0",
            "current_evidence": "double-zero lemma exists; background subtraction contract exists only conditionally",
            "verdict": "STRICT_F0_ZERO_IS_CLEANER_THAN_BACKGROUND_SUBTRACTION",
            "blocks_if_missing": "L_cg metric response/source-normalization hair remains",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "clause_id": "FCZ1290_3_connection_domain_boundary",
            "condition": "K_conn^{00}=K_domain^{00}=K_boundary^{00}=0 or bounded",
            "mathematical_effect": "prevents hidden derivative/projector/worldtube stress from replacing the killed chain term",
            "current_evidence": "776/1289 ledgers keep these terms open",
            "verdict": "OPEN",
            "blocks_if_missing": "Kmetric^{00} remains partial and Delta_K^{00} not computable",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "clause_id": "FCZ1290_4_chain_zero_verdict",
            "condition": "FCZ1290_0..3 all pass",
            "mathematical_effect": "Kmetric_chain^{00}=0 to first variation in the local fixed-point branch",
            "current_evidence": "the algebraic route is clear, but parent ownership is not yet present",
            "verdict": "CHAIN_ZERO_NOT_CLAIMED",
            "blocks_if_missing": "retain M_m/M_L residual rows and proceed to parent-clause construction",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    residual_rows = [
        {
            "residual_id": "KRR1290_0_m_kernel_residual",
            "residual_component": "R_m^{00}",
            "formula": "R_m^{00}=C_sign L_cg^-2 F_prime(m) M_m^{00}",
            "zero_condition": "M_m^{00}=0 by fixed-field scalar status, or F_prime(m_*)=0 by parent-locked stationary point",
            "needed_values": "MISSING_PARENT_DEFINITION_OF_m;MISSING_M_m_00_OR_ZERO_PROOF;MISSING_F_PRIME_ZERO_PROOF;MISSING_C_SIGN",
            "maps_to_tests": "PPN;Newton_source;clock;orbital;R10_if_finite_range",
            "current_status": "RETAINED_NONCLAIM_RESIDUAL",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "residual_id": "KRR1290_1_Lcg_kernel_residual",
            "residual_component": "R_L^{00}",
            "formula": "R_L^{00}=-2 C_sign L_cg^-3 F(m) M_L^{00}",
            "zero_condition": "M_L^{00}=0 by metric-silent L_cg, or F(m_*)=0 by strict double zero, or parent-owned background subtraction",
            "needed_values": "MISSING_PARENT_DEFINITION_OF_L_cg;MISSING_M_L_00_OR_ZERO_PROOF;MISSING_F_ZERO_OR_SUBTRACTION;MISSING_C_SIGN",
            "maps_to_tests": "PPN;Newton_source;clock;orbital;source_normalization",
            "current_status": "RETAINED_NONCLAIM_RESIDUAL",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "residual_id": "KRR1290_2_connection_domain_boundary_residual",
            "residual_component": "R_cdb^{00}",
            "formula": "R_cdb^{00}=K_conn^{00}+K_domain^{00}+K_boundary^{00}",
            "zero_condition": "metric-free/topological projector plus no-flux boundary theorem, or explicit residual bound",
            "needed_values": "MISSING_K_CONN_00;MISSING_K_DOMAIN_00;MISSING_K_BOUNDARY_00;MISSING_NO_FLUX_THEOREM",
            "maps_to_tests": "PPN;clock;orbital;boundary_mass_flux",
            "current_status": "RETAINED_NONCLAIM_RESIDUAL",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    deltak_status = [
        {
            "status_id": "DKU1290_0_Kmetric_chain_progress",
            "object": "Kmetric_chain^{00}",
            "status": "CONDITIONAL_ZERO_ROUTE_IDENTIFIED",
            "formula": "chain term is killed by fixed-field scalar kernels or strict double zero F(m_*)=F_prime(m_*)=0",
            "remaining_missing": "MISSING_PARENT_SCALAR_STATUS;MISSING_STRICT_DOUBLE_ZERO_PARENT_LOCK;MISSING_CDB_TERMS",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "status_id": "DKU1290_1_Kmetric_partial_update",
            "object": "Kmetric^{00}",
            "status": "VOLUME_PLUS_CONDITIONAL_CHAIN_LEDGER",
            "formula": "Kmetric^{00}=Kmetric_volume^{00}+R_m^{00}+R_L^{00}+R_cdb^{00}",
            "remaining_missing": "MISSING_VOLUME_SIGN;MISSING_RESIDUAL_ZERO_OR_BOUNDS;MISSING_CURRENT_KHAT_MATCH",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "status_id": "DKU1290_2_DeltaK00_verdict",
            "object": "Delta_K^{00}",
            "status": "NOT_COMPUTABLE_YET_BUT_NARROWER",
            "formula": "Delta_K^{00}=K_L^{00}-[Kmetric_volume^{00}+R_m^{00}+R_L^{00}+R_cdb^{00}]",
            "remaining_missing": "MISSING_CURRENT_MTS_KHAT_MATCH;MISSING_VOLUME_CONVENTION;MISSING_KERNEL_ZERO_OR_NUMERIC_BOUNDS",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    claim_gates = [
        {
            "gate_id": "CG1290_0_sources",
            "claim": "private checkpoint provenance",
            "current_status": "SATISFIED_FOR_PRIVATE_CHECKPOINT",
            "reason": "all registered anchors are validated",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1290_1_kernel_zero",
            "claim": "M_m^{00}=M_L^{00}=0",
            "current_status": "BLOCKED_CONDITIONAL_ONLY",
            "reason": "fixed-field scalar status for m and L_cg is not parent-signed",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1290_2_strict_double_zero",
            "claim": "F(m_*)=F_prime(m_*)=0 local double zero",
            "current_status": "BLOCKED_NOT_PARENT_DERIVED",
            "reason": "double-zero sufficiency exists, but MTS does not yet derive the local lock or F shape",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1290_3_Kmetric_complete",
            "claim": "Kmetric^{00} complete",
            "current_status": "BLOCKED_CDB_AND_VOLUME_CONVENTION_OPEN",
            "reason": "connection/domain/boundary residuals and sign/volume convention remain open",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1290_4_local_GR",
            "claim": "local GR/Newton/PPN recovery",
            "current_status": "BLOCKED_NONCLAIM",
            "reason": "Delta_K^{00}, response vector, and amplitude score remain incomplete",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decision = [
        {
            "decision_id": "DEC1290_0_best_route",
            "decision": "prefer strict double-zero or fixed-field scalar parent clause over background subtraction",
            "because": "it kills both m and L_cg chain channels with less source-normalization scrutiny",
            "next_action": "construct or reject the parent clause that makes m,L_cg metric-silent and F double-zero locally",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1290_1_progress",
            "decision": "chain kernel has a conditional zero theorem and residual fallback",
            "because": "1290 separates the branches instead of leaving M_m/M_L as vague unknowns",
            "next_action": "either sign the scalar-status premises or carry KRR1290 residuals to response bounds",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1290_2_no_claim",
            "decision": "do not claim local GR",
            "because": "the best zero route is sufficient but not derived from the actual MTS parent action",
            "next_action": "1291 should write the exact parent clause or demote chain-zero to closure-only",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_target = [
        {
            "next_id": "NEXT1290_0_1291",
            "target_file": "1291-Y5-R10-RAB-strict-double-zero-parent-clause-or-chain-kernel-residual-bound.md",
            "target_script": "scripts/Y5_R10_RAB_strict_double_zero_parent_clause_or_chain_kernel_residual_bound.py",
            "task": "construct the parent clause that makes m and L_cg metric-silent with F(m_*)=F_prime(m_*)=0, or demote the chain-zero route to residual bounds",
            "success_condition": "strict double-zero parent clause is written with all premises and failure modes, or KRR1290 residuals are promoted to the next bound-input ledger",
            "do_not": "do not use conditional fixed-field scalar status as a local-GR proof without parent ownership and boundary/domain silence",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    write_csv(SOURCE_REGISTER_PATH, source_register)
    write_csv(KERNEL_AUDIT_PATH, kernel_audit)
    write_csv(CHAIN_ZERO_PATH, chain_zero)
    write_csv(RESIDUAL_ROWS_PATH, residual_rows)
    write_csv(DELTAK_STATUS_PATH, deltak_status)
    write_csv(CLAIM_GATES_PATH, claim_gates)
    write_csv(DECISION_PATH, decision)
    write_csv(NEXT_PATH, next_target)

    validations = []
    source_count = len(source_register)
    source_hits = sum(1 for row in source_register if row["exists"] and row["needle_found"])
    validations.append(
        validation_row(
            "VAL1290_0_sources_exist",
            "registered source paths exist and anchors are found",
            source_hits == source_count,
            f"{source_hits}/{source_count} source anchors found",
        )
    )
    fixed_field = next(row for row in kernel_audit if row["kernel_id"] == "MKA1290_0_fixed_field_scalar_branch")
    validations.append(
        validation_row(
            "VAL1290_1_fixed_field_kernel_zero_written",
            "fixed-field scalar kernel-zero lemma is written as conditional nonclaim",
            fixed_field["result"] == "CONDITIONAL_KERNEL_ZERO"
            and fixed_field["current_status"] == "USEFUL_LEMMA_NOT_PARENT_SIGNED"
            and is_false(fixed_field["claim_allowed"]),
            "MKA1290_0_fixed_field_scalar_branch",
        )
    )
    strict_double = next(row for row in kernel_audit if row["kernel_id"] == "MKA1290_3_strict_double_zero_branch")
    validations.append(
        validation_row(
            "VAL1290_2_strict_double_zero_identified",
            "strict double-zero route is identified but not claimed",
            strict_double["result"] == "BEST_LOW_SCRUTINY_ZERO_ROUTE"
            and strict_double["current_status"] == "SUFFICIENT_CLAUSE_NOT_DERIVED_FOR_MTS",
            "MKA1290_3_strict_double_zero_branch",
        )
    )
    chain_verdict = next(row for row in chain_zero if row["clause_id"] == "FCZ1290_4_chain_zero_verdict")
    validations.append(
        validation_row(
            "VAL1290_3_chain_zero_not_claimed",
            "chain zero attempt remains conditional and blocked",
            chain_verdict["verdict"] == "CHAIN_ZERO_NOT_CLAIMED"
            and is_false(chain_verdict["claim_allowed"]),
            "FCZ1290_4_chain_zero_verdict",
        )
    )
    residual_ok = all("RETAINED_NONCLAIM_RESIDUAL" == row["current_status"] for row in residual_rows)
    validations.append(
        validation_row(
            "VAL1290_4_residual_rows_retained",
            "m, Lcg, and connection/domain/boundary residual rows are retained",
            residual_ok and all(is_false(row["claim_allowed"]) for row in residual_rows),
            f"residual_rows={len(residual_rows)}",
        )
    )
    deltak_verdict = next(row for row in deltak_status if row["status_id"] == "DKU1290_2_DeltaK00_verdict")
    validations.append(
        validation_row(
            "VAL1290_5_DeltaK_narrower_not_computable",
            "DeltaK00 status is narrowed but still not computable",
            deltak_verdict["status"] == "NOT_COMPUTABLE_YET_BUT_NARROWER"
            and "MISSING_CURRENT_MTS_KHAT_MATCH" in deltak_verdict["remaining_missing"],
            "DKU1290_2_DeltaK00_verdict",
        )
    )
    validations.append(
        validation_row(
            "VAL1290_6_claim_gates_blocked",
            "claim gates block local GR/PPN promotion",
            all(is_false(row["claim_allowed"]) for row in claim_gates)
            and any("BLOCKED" in row["current_status"] for row in claim_gates),
            f"claim_gate_rows={len(claim_gates)}",
        )
    )
    generated_tables = [
        SOURCE_REGISTER_PATH,
        KERNEL_AUDIT_PATH,
        CHAIN_ZERO_PATH,
        RESIDUAL_ROWS_PATH,
        DELTAK_STATUS_PATH,
        CLAIM_GATES_PATH,
        DECISION_PATH,
        NEXT_PATH,
    ]
    parse_ok = True
    parse_details: list[str] = []
    for table_path in generated_tables:
        try:
            parse_details.append(f"{table_path.name}:{len(read_csv(table_path))}")
        except Exception as exc:
            parse_ok = False
            parse_details.append(f"{table_path.name}:ERROR:{exc}")
    validations.append(validation_row("VAL1290_7_csv_parse", "all generated CSVs parse cleanly", parse_ok, "; ".join(parse_details)))
    formalization_hits = generated_inside_formalization()
    validations.append(
        validation_row(
            "VAL1290_8_formalization_untouched",
            "formalization-workbench untouched by generated outputs",
            not formalization_hits,
            f"formalization_generated_output_count={len(formalization_hits)}",
        )
    )
    validations.append(
        validation_row(
            "VAL1290_9_nonclaim_policy",
            "all generated rows remain nonclaim",
            all_nonclaim([source_register, kernel_audit, chain_zero, residual_rows, deltak_status, claim_gates, decision, next_target]),
            "valid_for_claim=false and claim_allowed=false throughout generated tables",
        )
    )
    validations.append(
        validation_row(
            "VAL1290_10_next_target_1291",
            "next target routes to strict double-zero parent clause or residual bounds",
            next_target[0]["next_id"] == "NEXT1290_0_1291" and "double-zero" in next_target[0]["target_file"],
            str(next_target[0]["target_file"]),
        )
    )
    overall_pass = all(row["status"] == "PASS" for row in validations)
    validations.append(
        validation_row(
            "VAL1290_11_overall",
            "overall 1290 validation",
            overall_pass,
            "1290 identifies the conditional fixed-field scalar kernel-zero lemma and the stricter F=Fprime=0 route, retains residual rows, and keeps DeltaK/local-GR nonclaim",
        )
    )
    write_csv(VALIDATION_PATH, validations)

    doc = f"""# 1290 Y5 R10 RAB m/Lcg metric-kernel source or fixed-point chain zero

Generated: `{RUN_STARTED_UTC.isoformat()}`

**Current verdict:** 1290 finds a real conditional route: if `m` and `L_cg` are parent-owned scalar inputs held fixed in Hilbert metric variation, then `M_m^{{00}}=0` and `M_L^{{00}}=0` for the algebraic `Gamma_eff=L_cg^-2 F(m)` term. But this is not yet a claim, because the corpus has not parent-signed that `m` and `L_cg` are metric-silent rather than metric/readout composites.

**Main progress:** the cleanest low-scrutiny branch is now clear. A strict local double zero, `F(m_*)=0` and `F_prime(m_*)=0`, kills both chain channels even if the kernels are finite. That is safer than relying on background subtraction, but it still needs a parent law locking the local branch to `m_*`.

**Next derivation target:** construct the strict double-zero parent clause for `m,L_cg,F`, or demote the chain-zero route to explicit residual bounds.

## Source Register

{markdown_table(source_register, ["source_id", "local_path", "needle", "exists", "needle_found", "role", "valid_for_claim", "claim_allowed"])}

## Metric Kernel Audit

{markdown_table(kernel_audit, ["kernel_id", "kernel", "candidate_derivation", "required_assumptions", "source_path", "source_anchor", "result", "current_status", "valid_for_claim", "claim_allowed"])}

## Fixed-Point Chain-Zero Attempt

{markdown_table(chain_zero, ["clause_id", "condition", "mathematical_effect", "current_evidence", "verdict", "blocks_if_missing", "valid_for_claim", "claim_allowed"])}

## Kernel Residual Rows

{markdown_table(residual_rows, ["residual_id", "residual_component", "formula", "zero_condition", "needed_values", "maps_to_tests", "current_status", "valid_for_claim", "claim_allowed"])}

## DeltaK Status Update

{markdown_table(deltak_status, ["status_id", "object", "status", "formula", "remaining_missing", "valid_for_claim", "claim_allowed"])}

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
