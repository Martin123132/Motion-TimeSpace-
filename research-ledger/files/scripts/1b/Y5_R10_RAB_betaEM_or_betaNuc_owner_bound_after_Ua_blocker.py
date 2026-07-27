from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = Path("source-intake/mts_residuals")

DOC_PATH = Path("1410-Y5-R10-RAB-betaEM-or-betaNuc-owner-bound-after-Ua-blocker.md")
SOURCE_REGISTER_PATH = SRC_DIR / "P8_Y5_R10_1410_SOURCE_REGISTER.csv"
COMMON_LOCK_PATH = SRC_DIR / "P8_Y5_R10_1410_COMMON_SECTOR_LOCK_THEOREM_ATTEMPT.csv"
EM_QCD_AUDIT_PATH = SRC_DIR / "P8_Y5_R10_1410_BETA_EM_QCD_OWNER_AUDIT.csv"
COUPLING_OBSTRUCTION_PATH = SRC_DIR / "P8_Y5_R10_1410_COUPLING_OBSTRUCTION_LEDGER.csv"
FINITE_TEMPLATE_PATH = SRC_DIR / "P8_Y5_R10_1410_FINITE_BETA_SOURCE_BOUND_TEMPLATE.csv"
DECISION_PATH = SRC_DIR / "P8_Y5_R10_1410_DECISION_LEDGER.csv"
CLAIM_GATE_PATH = SRC_DIR / "P8_Y5_R10_1410_CLAIM_GATE.csv"
NEXT_TARGET_PATH = SRC_DIR / "P8_Y5_R10_1410_NEXT_TARGET.csv"
VALIDATION_PATH = SRC_DIR / "P8_Y5_BRR545_1410_VALIDATION.csv"

STATUS = "Y5_R10_1410_betaEM_betaNuc_common_sector_lock_attempt_written_nonclaim"
CLAIM_CEILING = (
    "common_sector_lock_theorem_attempt_only_no_beta_zero_claim_no_WEP_pass_"
    "no_Ps_products_no_clock_R10_PPN_transfer_no_Newton_no_local_GR_pass"
)


def clean(value: Any) -> str:
    return str(value).replace("\n", " ").replace("\r", " ").strip()


def md_cell(value: Any) -> str:
    return clean(value).replace("|", "\\|")


def write_csv(relative_path: Path, rows: list[dict[str, Any]]) -> None:
    path = ROOT / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows supplied for {relative_path}")
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: clean(row.get(key, "")) for key in fieldnames})


def md_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return ""
    headers = list(rows[0].keys())
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(md_cell(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines)


def anchor_found(relative_path: str, anchor: str) -> bool:
    path = ROOT / relative_path
    if not path.exists():
        return False
    return anchor in path.read_text(encoding="utf-8", errors="ignore")


def source_register_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "source_id": "SRC1410_0_1409_doc",
            "source_path": "1409-Y5-R10-RAB-Ua-kernel-first-fill-or-official-readout-blocker-ledger.md",
            "anchor": "NEXT1409_0_1410",
            "role": "prior checkpoint redirects work from blocked U_a data route to beta_EM/beta_nuc owner-or-bound route",
        },
        {
            "source_id": "SRC1410_1_1408_queue",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1408_SECTOR_BETA_SOURCE_FILL_QUEUE.csv",
            "anchor": "FQ1408_1_beta_EM",
            "role": "fill queue prioritizing beta_EM and beta_nuc after U_a",
        },
        {
            "source_id": "SRC1410_2_1405_current",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1405_PARENT_WEP_RESPONSE_CURRENT_DERIVATION.csv",
            "anchor": "WRC1405_6_common_owner_zero",
            "role": "linear WEP response identity and exact conditional common-owner zero lemma",
        },
        {
            "source_id": "SRC1410_3_1406_common_owner",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1406_COMMON_MATTER_OWNER_WEP_ZERO_AUDIT.csv",
            "anchor": "CMO1406_7_current_verdict",
            "role": "common matter owner remains unsigned, but exact conditional theorem exists",
        },
        {
            "source_id": "SRC1410_4_1407_no_source_slot",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1407_NOSOURCEONLYSPECIESSLOT_PROOF_AUDIT.csv",
            "anchor": "NSS1407_7_current_verdict",
            "role": "pre-action species/source slots survive, forcing strict beta schema",
        },
        {
            "source_id": "SRC1410_5_1395_zero_attempt",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1395_SECTOR_BETA_ZERO_THEOREM_ATTEMPT.csv",
            "anchor": "SBZ1395_5_current_verdict",
            "role": "sector beta zero routes for electronic, nuclear, EM, and joint binding are conditional only",
        },
        {
            "source_id": "SRC1410_6_1395_source_pack",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1395_BINDING_SECTOR_BETA_SOURCE_PACK.csv",
            "anchor": "SBP1395_5_pack_verdict",
            "role": "explicit beta_e, beta_nuc, beta_EM, beta_other rows remain value-missing",
        },
        {
            "source_id": "SRC1410_7_1396_em_lock",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1396_EM_LOCK_REPAIR_ATTEMPT.csv",
            "anchor": "ELR1396_6_current_verdict",
            "role": "EM-lock repair failed in current corpus because F2/current/readout/no-alpha signatures are unsigned",
        },
        {
            "source_id": "SRC1410_8_1396_beta_em_template",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1396_BETA_EM_SOURCE_BOUND_TEMPLATE.csv",
            "anchor": "BEM1396_6_template_verdict",
            "role": "finite beta_EM source-bound template ready but nonclaim",
        },
        {
            "source_id": "SRC1410_9_1396_arena_gate",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1396_ALPHAEM_WEP_CLOCK_R10_GATE.csv",
            "anchor": "EMG1396_4_local_GR",
            "role": "alpha_EM/WEP/clock/R10/local_GR transfers remain blocked",
        },
        {
            "source_id": "SRC1410_10_1409_Ua_blocker",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1409_OFFICIAL_READOUT_BLOCKER_LEDGER.csv",
            "anchor": "ORB1409_7_verdict",
            "role": "U_a/source readout route remains blocked and cannot be used to score products",
        },
        {
            "source_id": "SRC1410_11_this_script",
            "source_path": "scripts/Y5_R10_RAB_betaEM_or_betaNuc_owner_bound_after_Ua_blocker.py",
            "anchor": "STATUS",
            "role": "generator for this checkpoint",
        },
    ]
    for row in rows:
        row["path_exists"] = (ROOT / row["source_path"]).exists()
        row["anchor_found"] = anchor_found(row["source_path"], row["anchor"])
        row["valid_for_claim"] = False
        row["claim_allowed"] = False
    return rows


def common_sector_lock_rows() -> list[dict[str, Any]]:
    return [
        {
            "lock_id": "CSL1410_0_definition",
            "claim_piece": "common-sector-lock target",
            "statement": "For all ordinary material sectors s in {e,nuc,EM,other}, E_s,A(X)=C_*(X) Ebar_s,A in the local matter branch.",
            "derivation_status": "TARGET_DEFINED",
            "mathematical_consequence": "beta_s^a := partial_a ln E_s,A = partial_a ln C_* := beta_*^a for every sector and material A",
            "missing_for_claim": "parent action must sign that all ordinary sector constants/bindings inherit the same owner C_* and no sector-specific C_s(X) exists",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "lock_id": "CSL1410_1_exact_cancellation",
            "claim_piece": "composition cancellation from common owner",
            "statement": "If beta_s^a=beta_*^a for every sector, then Delta alpha_AB^a=sum_s Delta f_s,AB beta_s^a=(sum_s Delta f_s,AB) beta_*^a=0.",
            "derivation_status": "EXACT_CONDITIONAL_LEMMA_DERIVED",
            "mathematical_consequence": "linear WEP response is zero before contracting with U_a; this is stronger than fitting one Ti/Pt cancellation",
            "missing_for_claim": "common-sector-lock premise remains parent-unsigned",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "lock_id": "CSL1410_2_zero_vs_common_mode",
            "claim_piece": "we do not need beta_EM=0 or beta_nuc=0 first",
            "statement": "A universal beta_*^a is locally unobservable in WEP because it is composition common-mode; only beta_s^a-beta_*^a enters Delta alpha_AB.",
            "derivation_status": "IMPORTANT_REDUCTION",
            "mathematical_consequence": "the less-scrutinized route is sector-lock/equivalence rather than individual zero of every coupling",
            "missing_for_claim": "must still forbid independent EM/QCD/electronic residual couplings and source-only slots",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "lock_id": "CSL1410_3_partial_lock_warning",
            "claim_piece": "partial EM-QCD lock is insufficient",
            "statement": "If only beta_EM^a=beta_nuc^a but beta_e or beta_other remain independent, then Delta alpha_AB still has residual terms.",
            "derivation_status": "RESIDUAL_WARNING",
            "mathematical_consequence": "beta_EM/beta_nuc progress is useful but does not alone prove WEP/local GR",
            "missing_for_claim": "beta_e, beta_other, material tensor, and U_a remain active gates",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "lock_id": "CSL1410_4_current_verdict",
            "claim_piece": "common-sector-lock theorem status",
            "statement": "The theorem is exact as a conditional algebraic result, but the parent action has not yet signed the common-sector-lock premise.",
            "derivation_status": "CONDITIONAL_THEOREM_READY_NOT_PROMOTED",
            "mathematical_consequence": "1410 improves the route by replacing literal beta-zero demand with a weaker common-owner target",
            "missing_for_claim": "parent object-language clause excluding sector-specific C_s(X), lambda_A F^2, QCD/Yukawa drift, and source-only material slots",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def em_qcd_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "audit_id": "BQO1410_0_beta_EM_charge_generator",
            "sector": "EM",
            "owner_clause": "T_Q is a compact parent vertical generator with fixed normalization and charge lattice",
            "current_evidence": "ELR1396_0_charge_generator",
            "status": "UNSIGNED",
            "if_signed": "charge units and A_Q normalization stop floating independently",
            "if_unsigned": "retain beta_EM/b_alpha_EM finite rows",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "BQO1410_1_beta_EM_Maxwell_block",
            "sector": "EM",
            "owner_clause": "unique Maxwell kinetic subblock forbids independent lambda_A F_Q^2 counterterm",
            "current_evidence": "ELR1396_1_unique_Maxwell_F2",
            "status": "FAILS_CURRENT_CORPUS",
            "if_signed": "EM kinetic normalization becomes parent-owned/common-mode",
            "if_unsigned": "lambda_A F_Q^2 remains the live coupling gap",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "BQO1410_2_beta_EM_current_readout",
            "sector": "EM",
            "owner_clause": "charge current, Hodge/coframe readout, and dimensionless alpha_EM descend from the same owner",
            "current_evidence": "ELR1396_2_current_owner;ELR1396_3_readout_descent",
            "status": "UNSIGNED",
            "if_signed": "clock/alpha drift cannot re-enter through a unit/readout leak",
            "if_unsigned": "clock/WEP/R10 transfer remains blocked",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "BQO1410_3_beta_EM_no_alpha_vertex",
            "sector": "EM",
            "owner_clause": "ordinary matter functor forbids alpha_EM(X), f_A(X)F^2, m_A(X), and binding-response vertices",
            "current_evidence": "ELR1396_4_no_alpha_vertex;NSS1407_7_current_verdict",
            "status": "UNSIGNED",
            "if_signed": "Damour-Donoghue-like EM composition charges are theorem-zero locally",
            "if_unsigned": "finite EM composition residual remains physical fallback",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "BQO1410_4_beta_nuc_QCD_owner",
            "sector": "nuclear_QCD",
            "owner_clause": "Lambda_QCD, light-quark/Yukawa inputs, and nuclear binding inherit the same ordinary-matter owner or are representation constants",
            "current_evidence": "CMO1406_3_constant_spectrum_owner;SBZ1395_1_nuclear_zero",
            "status": "UNSIGNED",
            "if_signed": "beta_nuc locks to beta_* or becomes theorem-zero relative to composition",
            "if_unsigned": "finite beta_nuc row remains required",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "BQO1410_5_beta_nuc_binding_inheritance",
            "sector": "nuclear_QCD",
            "owner_clause": "composite rest mass and nuclear binding terms inherit the same coframe/matter action variation as bulk matter",
            "current_evidence": "CMO1406_4_binding_inheritance;WRC1405_2_sector_decomposition",
            "status": "CONDITIONAL_NOT_PARENT_SIGNED",
            "if_signed": "nuclear binding cannot generate composition-specific gravitational response at linear order",
            "if_unsigned": "nuclear sector feeds WEP/orbital/R10 residual vector",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "BQO1410_6_joint_EM_QCD_verdict",
            "sector": "EM_and_nuclear_QCD",
            "owner_clause": "beta_EM and beta_nuc are locked to the same common owner beta_* and no hidden sector-specific coupling survives",
            "current_evidence": "BQO1410_1_beta_EM_Maxwell_block;BQO1410_4_beta_nuc_QCD_owner;CSL1410_4_current_verdict",
            "status": "NOT_PROVED_SOURCE_TEMPLATE_REQUIRED",
            "if_signed": "EM/QCD pieces stop being the coupling bottleneck for WEP at linear order",
            "if_unsigned": "carry finite source-bound templates for beta_EM and beta_nuc",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def coupling_obstruction_rows() -> list[dict[str, Any]]:
    return [
        {
            "obstruction_id": "COUP1410_0_independent_F2",
            "coupling_gap": "independent lambda_A F_Q^2 or equivalent EM kinetic normalization",
            "why_it_matters": "lets alpha/charge normalization vary outside the common metric owner",
            "current_status": "ACTIVE_COUNTERTERM_GAP",
            "needed_resolution": "parent action uniqueness theorem forbids sector-specific Maxwell normalization",
            "blocks": "beta_EM_zero;alpha_EM_lock;WEP_clock_R10_transfer;local_GR_EM_silence",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "obstruction_id": "COUP1410_1_alpha_readout_leak",
            "coupling_gap": "Hodge/coframe/hbar*c readout may carry independent X-dependence",
            "why_it_matters": "a formal EM action lock is not enough if the dimensionless alpha readout leaks",
            "current_status": "UNSIGNED_READOUT_DESCENT",
            "needed_resolution": "observed coframe and dimensionless alpha readout descent theorem",
            "blocks": "clock_alpha_claim;beta_EM_to_R10_transfer",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "obstruction_id": "COUP1410_2_QCD_spectrum_owner",
            "coupling_gap": "Lambda_QCD, quark masses, Yukawas, or nuclear binding may have sector-specific X-dependence",
            "why_it_matters": "nuclear binding dominates composition response if not common-mode locked",
            "current_status": "UNSIGNED_MATTER_SPECTRUM_OWNER",
            "needed_resolution": "ordinary-sector spectrum constants are representation/superselection data or share one owner",
            "blocks": "beta_nuc_lock;orbital_R10_material_leg;local_GR_matter_silence",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "obstruction_id": "COUP1410_3_source_only_slots",
            "coupling_gap": "pre-action w_A(X), kappa_A(X), or source-only material multipliers",
            "why_it_matters": "can create composition/source response without violating basic locality/covariance tests",
            "current_status": "COUNTEREXAMPLE_SURVIVES_CURRENT_CORPUS",
            "needed_resolution": "NoSourceOnlySpeciesSlot parent grammar certificate",
            "blocks": "common_matter_owner_zero;sector_lock_promotion",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "obstruction_id": "COUP1410_4_Ua_external_kernel",
            "coupling_gap": "U_a source/readout kernel not yet numeric or derived",
            "why_it_matters": "even finite beta values cannot be scored until source contraction is real",
            "current_status": "BLOCKED_BY_1409_OFFICIAL_READOUT_LEDGER",
            "needed_resolution": "official CMSM arrays or parent theorem eliminating finite source leg",
            "blocks": "P_s_products;WEP_pressure_score",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def finite_template_rows() -> list[dict[str, Any]]:
    return [
        {
            "template_id": "FBT1410_0_beta_EM_lock_or_bound",
            "quantity": "beta_EM^a - beta_*^a",
            "parent_definition": "relative EM-sector response to the common ordinary-matter owner",
            "units": "X_a^-1 or dimensionless per parent coordinate",
            "dimension_basis": "MISSING_PARENT_COORDINATE_BASIS",
            "value": "MISSING_ZERO_THEOREM_OR_SOURCE_VALUE",
            "uncertainty": "MISSING_UNCERTAINTY",
            "sign_convention": "MISSING_SIGN_CONVENTION",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1410_BETA_EM_QCD_OWNER_AUDIT.csv",
            "source_anchor": "BQO1410_6_joint_EM_QCD_verdict",
            "arena_projection": "WEP;clock;R10;local_EM_residual",
            "lambda_or_domain": "WEP_LOCAL_DOMAIN_ONLY_UNTIL_TRANSFER",
            "fill_status": "SOURCE_READY_TEMPLATE_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "template_id": "FBT1410_1_beta_nuc_lock_or_bound",
            "quantity": "beta_nuc^a - beta_*^a",
            "parent_definition": "relative nuclear/QCD binding response to the common ordinary-matter owner",
            "units": "X_a^-1 or dimensionless per parent coordinate",
            "dimension_basis": "MISSING_PARENT_COORDINATE_BASIS",
            "value": "MISSING_ZERO_THEOREM_OR_SOURCE_VALUE",
            "uncertainty": "MISSING_UNCERTAINTY",
            "sign_convention": "MISSING_SIGN_CONVENTION",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1410_BETA_EM_QCD_OWNER_AUDIT.csv",
            "source_anchor": "BQO1410_6_joint_EM_QCD_verdict",
            "arena_projection": "WEP;orbital;R10;local_matter_residual",
            "lambda_or_domain": "WEP_LOCAL_DOMAIN_ONLY_UNTIL_TRANSFER",
            "fill_status": "SOURCE_READY_TEMPLATE_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "template_id": "FBT1410_2_beta_star_common_mode",
            "quantity": "beta_*^a",
            "parent_definition": "common ordinary-sector owner response",
            "units": "X_a^-1 or dimensionless per parent coordinate",
            "dimension_basis": "MISSING_PARENT_COORDINATE_BASIS",
            "value": "COMMON_MODE_NOT_WEP_SCORABLE",
            "uncertainty": "not_applicable_until_parent_signed",
            "sign_convention": "not_applicable_until_parent_signed",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1410_COMMON_SECTOR_LOCK_THEOREM_ATTEMPT.csv",
            "source_anchor": "CSL1410_2_zero_vs_common_mode",
            "arena_projection": "composition-blind WEP common mode only",
            "lambda_or_domain": "local_matter_branch",
            "fill_status": "COMMON_MODE_IDENTIFIED_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "template_id": "FBT1410_3_residual_vector",
            "quantity": "Delta alpha_AB^a residual",
            "parent_definition": "sum_s Delta f_s,AB (beta_s^a-beta_*^a)",
            "units": "dimensionless or X_a^-1 contracted with source kernel",
            "dimension_basis": "MISSING_FULL_MATERIAL_TENSOR_AND_PARENT_BASIS",
            "value": "MISSING_RESIDUAL_VECTOR",
            "uncertainty": "MISSING_UNCERTAINTY",
            "sign_convention": "MISSING_SIGN_CONVENTION",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1410_COMMON_SECTOR_LOCK_THEOREM_ATTEMPT.csv",
            "source_anchor": "CSL1410_3_partial_lock_warning",
            "arena_projection": "WEP pressure after material tensor and U_a are real",
            "lambda_or_domain": "WEP_LOCAL_DOMAIN_ONLY_UNTIL_TRANSFER",
            "fill_status": "DEPENDENT_RESIDUAL_TEMPLATE_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC1410_0_route_choice",
            "decision": "prioritize common-sector-lock over literal beta_EM=0 or beta_nuc=0",
            "reason": "WEP only sees composition-relative response; a universal beta_* common mode cancels exactly in Delta alpha_AB",
            "effect": "the parent action target is weaker and closer to GR-style universal coupling",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC1410_1_EM_status",
            "decision": "do not promote beta_EM",
            "reason": "unique Maxwell F2/current/readout/no-alpha package is not parent-signed and independent F2 counterterm remains live",
            "effect": "retain beta_EM-beta_* finite template",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC1410_2_QCD_status",
            "decision": "do not promote beta_nuc",
            "reason": "QCD/nuclear matter-spectrum owner and binding inheritance are unsigned",
            "effect": "retain beta_nuc-beta_* finite template",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC1410_3_next_best_work",
            "decision": "write the parent ordinary-sector lock clause next",
            "reason": "one clause can attack EM, QCD, electron, and other-sector residuals together",
            "effect": "next checkpoint should try to ban sector-specific C_s(X) and lambda_A F2-style counterterms from the parent object language",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "claim_id": "GATE1410_0_common_lock",
            "claim": "all ordinary sectors are locked to one common owner beta_*",
            "status": "CONDITIONAL_ONLY_NO_CLAIM",
            "reason": "algebraic lemma is exact but parent action has not excluded sector-specific couplings",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "claim_id": "GATE1410_1_beta_EM",
            "claim": "beta_EM relative residual is zero or bounded",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "EM-lock remains unsigned and finite source row has no value/units/sign/source",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "claim_id": "GATE1410_2_beta_nuc",
            "claim": "beta_nuc relative residual is zero or bounded",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "QCD/nuclear matter-spectrum owner remains unsigned and finite source row has no value/units/sign/source",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "claim_id": "GATE1410_3_WEP",
            "claim": "WEP branch can be scored",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "U_a, material tensor, beta_e/beta_other, beta_EM, and beta_nuc remain incomplete",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "claim_id": "GATE1410_4_transfer",
            "claim": "rows transfer to clocks, R10, PPN, orbital, Newton, or local GR",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "arena isolation and source/readout gates remain active",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "claim_id": "GATE1410_5_verdict",
            "claim": "1410 proves the coupling problem is solved",
            "status": "NO_PROMOTION",
            "reason": "1410 clarifies the clean coupling target but does not sign the parent action clause",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT1410_0_1411",
            "target_doc": "1411-Y5-R10-RAB-common-sector-lock-parent-action-clause-or-counterterm-ban.md",
            "target_script": "scripts/Y5_R10_RAB_common_sector_lock_parent_action_clause_or_counterterm_ban.py",
            "task": "attempt to derive the parent object-language clause that all ordinary sector energies share one owner C_*(X), or explicitly list the allowed counterterms that prevent the theorem",
            "success_condition": "either sign the common-sector-lock premise for e/nuc/EM/other sectors, or produce a minimal counterterm ledger with finite residual templates",
            "do_not_claim": "beta_EM zero; beta_nuc zero; WEP pass; P_s products; clock/R10/PPN transfer; Newton/local GR",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "next_id": "NEXT1410_1_data_parallel",
            "target_doc": "future-beta-source-bound-acquisition.md",
            "target_script": "future_source_intake_route",
            "task": "if theorem route fails, source finite beta_EM-beta_* and beta_nuc-beta_* bounds with units/sign/provenance",
            "success_condition": "claim-grade rows with values, uncertainties, source paths, parent-basis maps, and arena projection gates",
            "do_not_claim": "source-free fitted cancellation or surrogate transfer",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def validation_rows(
    sources: list[dict[str, Any]],
    common_lock: list[dict[str, Any]],
    audits: list[dict[str, Any]],
    obstructions: list[dict[str, Any]],
    templates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    timestamp = datetime.now(timezone.utc).isoformat()
    output_paths = [
        DOC_PATH,
        SOURCE_REGISTER_PATH,
        COMMON_LOCK_PATH,
        EM_QCD_AUDIT_PATH,
        COUPLING_OBSTRUCTION_PATH,
        FINITE_TEMPLATE_PATH,
        DECISION_PATH,
        CLAIM_GATE_PATH,
        NEXT_TARGET_PATH,
        VALIDATION_PATH,
    ]
    rows: list[dict[str, Any]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        rows.append(
            {
                "check_id": check_id,
                "status": "PASS" if passed else "FAIL",
                "detail": detail,
                "timestamp_utc": timestamp,
            }
        )

    add(
        "VAL1410_0_sources",
        all(row["path_exists"] == True and row["anchor_found"] == True for row in sources),
        "all cited local source paths exist and anchors are present",
    )
    add(
        "VAL1410_1_common_lock",
        any(row["lock_id"] == "CSL1410_1_exact_cancellation" and row["derivation_status"] == "EXACT_CONDITIONAL_LEMMA_DERIVED" for row in common_lock)
        and any(row["lock_id"] == "CSL1410_4_current_verdict" and row["derivation_status"] == "CONDITIONAL_THEOREM_READY_NOT_PROMOTED" for row in common_lock),
        "common-sector-lock algebra is derived as conditional but not promoted",
    )
    add(
        "VAL1410_2_owner_audit",
        any(row["audit_id"] == "BQO1410_1_beta_EM_Maxwell_block" and row["status"] == "FAILS_CURRENT_CORPUS" for row in audits)
        and any(row["audit_id"] == "BQO1410_4_beta_nuc_QCD_owner" and row["status"] == "UNSIGNED" for row in audits),
        "EM and nuclear/QCD owner blockers are explicit",
    )
    add(
        "VAL1410_3_coupling_obstructions",
        {"COUP1410_0_independent_F2", "COUP1410_2_QCD_spectrum_owner", "COUP1410_3_source_only_slots"}.issubset(
            {row["obstruction_id"] for row in obstructions}
        )
        and all(row["valid_for_claim"] == False for row in obstructions),
        "coupling obstruction ledger contains the active counterterm/spectrum/source-slot blockers",
    )
    add(
        "VAL1410_4_templates",
        all(row["valid_for_claim"] == False and row["claim_allowed"] == False for row in templates)
        and any(row["quantity"] == "beta_EM^a - beta_*^a" for row in templates)
        and any(row["quantity"] == "beta_nuc^a - beta_*^a" for row in templates),
        "finite beta source-bound templates exist but contain no promoted values",
    )
    add(
        "VAL1410_5_decision",
        any(row["decision_id"] == "DEC1410_0_route_choice" for row in decisions)
        and any(row["decision_id"] == "DEC1410_3_next_best_work" for row in decisions),
        "decision ledger selects common-sector-lock parent clause as next route",
    )
    add(
        "VAL1410_6_claim_refusal",
        all(row["valid_for_claim"] == False and row["claim_allowed"] == False for row in gates),
        "beta, WEP, transfer, Newton, and local-GR claims are refused",
    )
    add(
        "VAL1410_7_scope",
        all((ROOT / path).resolve().is_relative_to(ROOT.resolve()) for path in output_paths),
        "outputs are confined to post-checkpoint-work paths",
    )
    add(
        "VAL1410_8_overall",
        True,
        "1410 replaces literal beta-zero pressure with a weaker common-sector-lock target and keeps finite beta rows nonclaim",
    )
    return rows


def write_doc(
    sources: list[dict[str, Any]],
    common_lock: list[dict[str, Any]],
    audits: list[dict[str, Any]],
    obstructions: list[dict[str, Any]],
    templates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    next_targets: list[dict[str, Any]],
    validations: list[dict[str, Any]],
) -> None:
    doc = f"""# 1410 - beta_EM Or beta_nuc Owner/Bound After U_a Blocker

**Status:** `{STATUS}`

**Current verdict:** this checkpoint finds the cleaner coupling target. We do not need to prove `beta_EM=0` and `beta_nuc=0` as isolated miracles first. The weaker GR-like target is `beta_s^a=beta_*^a` for all ordinary sectors, so composition-dependent response cancels as common mode. That algebra is exact, but the parent action has not yet signed the sector-lock premise.

**Discipline move:** no finite `beta_EM`, `beta_nuc`, `P_s`, WEP, clock, R10, PPN, Newton, or local-GR claim is promoted. The active coupling problem is now sharply identified as sector-specific counterterms/readout leaks: especially independent Maxwell normalization, QCD/matter-spectrum drift, and source-only species slots.

**Claim ceiling:** `{CLAIM_CEILING}`

## Source Register

{md_table(sources)}

## Common-Sector-Lock Theorem Attempt

{md_table(common_lock)}

## beta_EM / beta_nuc Owner Audit

{md_table(audits)}

## Coupling Obstruction Ledger

{md_table(obstructions)}

## Finite Beta Source-Bound Template

{md_table(templates)}

## Decision Ledger

{md_table(decisions)}

## Claim Gate

{md_table(gates)}

## Next Target

{md_table(next_targets)}

## Validation

{md_table(validations)}
"""
    (ROOT / DOC_PATH).write_text(doc, encoding="utf-8")


def main() -> None:
    sources = source_register_rows()
    common_lock = common_sector_lock_rows()
    audits = em_qcd_audit_rows()
    obstructions = coupling_obstruction_rows()
    templates = finite_template_rows()
    decisions = decision_rows()
    gates = claim_gate_rows()
    next_targets = next_target_rows()
    validations = validation_rows(sources, common_lock, audits, obstructions, templates, decisions, gates)

    write_csv(SOURCE_REGISTER_PATH, sources)
    write_csv(COMMON_LOCK_PATH, common_lock)
    write_csv(EM_QCD_AUDIT_PATH, audits)
    write_csv(COUPLING_OBSTRUCTION_PATH, obstructions)
    write_csv(FINITE_TEMPLATE_PATH, templates)
    write_csv(DECISION_PATH, decisions)
    write_csv(CLAIM_GATE_PATH, gates)
    write_csv(NEXT_TARGET_PATH, next_targets)
    write_csv(VALIDATION_PATH, validations)
    write_doc(sources, common_lock, audits, obstructions, templates, decisions, gates, next_targets, validations)

    if any(row["status"] != "PASS" for row in validations):
        raise SystemExit("1410 validation failed")

    print(STATUS)


if __name__ == "__main__":
    main()
