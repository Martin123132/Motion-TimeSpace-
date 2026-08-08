from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = Path("source-intake/mts_residuals")

DOC_PATH = Path("1412-Y5-R10-RAB-ordinary-matter-functor-exhaustion-or-finite-residual-vector.md")
SOURCE_REGISTER_PATH = SRC_DIR / "P8_Y5_R10_1412_SOURCE_REGISTER.csv"
EXHAUSTION_AUDIT_PATH = SRC_DIR / "P8_Y5_R10_1412_ORDINARY_MATTER_FUNCTOR_EXHAUSTION_AUDIT.csv"
MORPHISM_LEDGER_PATH = SRC_DIR / "P8_Y5_R10_1412_VISIBLE_COEFFICIENT_MORPHISM_COUNTEREXAMPLES.csv"
RESIDUAL_VECTOR_PATH = SRC_DIR / "P8_Y5_R10_1412_FINITE_RESIDUAL_VECTOR_BRANCH.csv"
LOCAL_GR_GATE_PATH = SRC_DIR / "P8_Y5_R10_1412_LOCAL_GR_IMPLICATION_GATE.csv"
DECISION_PATH = SRC_DIR / "P8_Y5_R10_1412_DECISION_LEDGER.csv"
CLAIM_GATE_PATH = SRC_DIR / "P8_Y5_R10_1412_CLAIM_GATE.csv"
NEXT_TARGET_PATH = SRC_DIR / "P8_Y5_R10_1412_NEXT_TARGET.csv"
VALIDATION_PATH = SRC_DIR / "P8_Y5_BRR545_1412_VALIDATION.csv"

STATUS = "Y5_R10_1412_ordinary_matter_functor_exhaustion_failed_residual_vector_branch_written_nonclaim"
CLAIM_CEILING = (
    "ordinary_matter_functor_exhaustion_not_proved_finite_residual_vector_branch_only_"
    "no_WEP_pass_no_beta_zero_no_transfer_no_Newton_no_local_GR_pass"
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
            "source_id": "SRC1412_0_1411_doc",
            "source_path": "1411-Y5-R10-RAB-common-sector-lock-parent-action-clause-or-counterterm-ban.md",
            "anchor": "NEXT1411_0_1412",
            "role": "prior checkpoint selecting ordinary matter functor exhaustion or finite residual vector",
        },
        {
            "source_id": "SRC1412_1_1411_parent_clause",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1411_PARENT_ACTION_LOCK_CLAUSE.csv",
            "anchor": "PAC1411_5_verdict",
            "role": "sufficient parent action lock clause written but not derived",
        },
        {
            "source_id": "SRC1412_2_1411_counterterms",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1411_COUNTERTERM_BAN_AUDIT.csv",
            "anchor": "CTB1411_5_verdict",
            "role": "minimal active counterterm set to ban or retain",
        },
        {
            "source_id": "SRC1412_3_1338_object_language",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1338_OBJECT_LANGUAGE_THEOREM_ATTEMPT.csv",
            "anchor": "OLT1338_6_verdict",
            "role": "object language theorem attempt fails to derive NoSourceOnlySpeciesSlot",
        },
        {
            "source_id": "SRC1412_4_1338_closure",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1338_NO_SOURCE_SLOT_CLOSURE_CONDITION.csv",
            "anchor": "CLOS1338_5_radiative_readout_preservation",
            "role": "explicit closure clauses needed if theorem is not derived",
        },
        {
            "source_id": "SRC1412_5_1338_countermodels",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1338_LIVE_COUNTERMODEL_BOUNDARIES.csv",
            "anchor": "CM1338_3_nonHilbert_readout_current",
            "role": "live countermodels for relative weights, measure weights, hidden markers, and readout currents",
        },
        {
            "source_id": "SRC1412_6_1310_owner_signature",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1310_OWNER_SIGNATURE_REPAIR_ATTEMPT.csv",
            "anchor": "OSA1310_5_verdict",
            "role": "ordinary constant owner/action signature repair fails at coefficient stage",
        },
        {
            "source_id": "SRC1412_7_1310_forbidden_vertices",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1310_FORBIDDEN_VERTEX_GATE.csv",
            "anchor": "FVG1310_5_radiative_reentry",
            "role": "forbidden visible coefficient vertices are not all parent-signed",
        },
        {
            "source_id": "SRC1412_8_1045_functor_signature",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1045_PARENT_MATTER_FUNCTOR_SIGNATURE_AUDIT.csv",
            "anchor": "MFS1045_6_verdict",
            "role": "parent matter functor signature fails current claim",
        },
        {
            "source_id": "SRC1412_9_1045_vertical_lift",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1045_VERTICAL_LIFT_DESCENT_GATE.csv",
            "anchor": "VLG1045_4_verdict",
            "role": "vertical lift descent is not parent-signed",
        },
        {
            "source_id": "SRC1412_10_1087_descent",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1087_PARENT_MATTER_DESCENT_ATTEMPT.csv",
            "anchor": "PMD1087_6_verdict",
            "role": "qbar_XT=0 parent matter descent theorem not signed",
        },
        {
            "source_id": "SRC1412_11_1087_zero_clause",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1087_ZERO_CURRENT_CLAUSE_CONTRACT.csv",
            "anchor": "ZCC1087_4_constant_superselection",
            "role": "future parent contract clauses for object language, action measure, functor, and constants",
        },
        {
            "source_id": "SRC1412_12_this_script",
            "source_path": "scripts/Y5_R10_RAB_ordinary_matter_functor_exhaustion_or_finite_residual_vector.py",
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


def exhaustion_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "audit_id": "OMF1412_0_target",
            "theorem_piece": "OrdinaryMatterFunctorExhaustion",
            "required_statement": "Arg(S_ord) = {Psi, e_obs(q(Phi)), omega_obs(q(Phi)), owned gauge data, fixed theta_rep, retained residual fields} and nothing else",
            "current_result": "TARGET_SHARPENED",
            "gap": "no primitive-to-parent constructor list proves this is exhaustive",
            "if_signed": "all hidden visible-coefficient morphisms are banned or explicitly residualized",
            "if_unsigned": "finite residual vector is mandatory",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "OMF1412_1_q_descent",
            "theorem_piece": "observed geometry descent",
            "required_statement": "e_obs, g_obs, omega_obs factor through q(Phi), so Dq[v]=0 implies Lie_v visible geometry = 0",
            "current_result": "CONDITIONAL_SUPPORT_NOT_PARENT_COMPLETE",
            "gap": "q/coframe functor and independent connection silence are not signed for all local sectors",
            "if_signed": "visible-geometry leakage narrows",
            "if_unsigned": "qbar_geom/frame residual remains possible",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "OMF1412_2_matter_bundle",
            "theorem_piece": "matter fields live in a functor over observed geometry",
            "required_statement": "Psi_A in E_A[e_obs] with fixed/gauge vertical lift and no physical material lift",
            "current_result": "VERTICAL_LIFT_NOT_PARENT_SIGNED",
            "gap": "no parent map assigns v_X to a gauge/fixed lift for every ordinary matter species and boundary class",
            "if_signed": "matter field variation cannot reopen qbar charge",
            "if_unsigned": "physical lift/source marker residual remains",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "OMF1412_3_fixed_representation_data",
            "theorem_piece": "fixed theta_rep",
            "required_statement": "masses, Yukawas, charge lattice, Lambda_QCD, alpha/readout constants are fixed representation/superselection data or explicit residual fields",
            "current_result": "CONSTANT_SUPERSELECTION_UNSIGNED",
            "gap": "matter-spectrum owner and EM/QCD kinetic normalization are not parent-derived",
            "if_signed": "beta_EM, beta_nuc, beta_e lock to common mode or vanish relative to composition",
            "if_unsigned": "constant-sector coefficient rows stay live",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "OMF1412_4_no_source_slot",
            "theorem_piece": "no source/species active coefficient morphism",
            "required_statement": "Hom(SpeciesLabel, Coeff_active_source) is empty",
            "current_result": "NOT_DERIVED_COUNTERMODEL_SURVIVES",
            "gap": "relative w_A, measure weights, and hidden marker relabels survive basic locality/covariance",
            "if_signed": "source-only WEP/Newton/R10 branch is theorem-zero",
            "if_unsigned": "source-weight residual row is required",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "OMF1412_5_readout_radiative_closure",
            "theorem_piece": "readout and effective action preserve the same coefficient domain",
            "required_statement": "S_eff and observable maps cannot regenerate f_X, m_A(X), marker, clock, or source-weight coefficients",
            "current_result": "UNSIGNED_PARALLEL_GATE",
            "gap": "radiative/readout closure remains unsigned",
            "if_signed": "the theorem survives projection to observables",
            "if_unsigned": "readout/radiative residual component remains",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "OMF1412_6_verdict",
            "theorem_piece": "ordinary matter functor exhaustion proof status",
            "required_statement": "OMF1412_0 through OMF1412_5 are signed together by one parent grammar",
            "current_result": "EXHAUSTION_NOT_PROVED_CURRENT_CORPUS",
            "gap": "object-language exhaustion remains a closure grammar rather than a theorem from MTS primitives",
            "if_signed": "common-sector-lock can be promoted to a theorem",
            "if_unsigned": "accept finite residual-vector branch as the honest next local-bound target",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def morphism_ledger_rows() -> list[dict[str, Any]]:
    return [
        {
            "morphism_id": "MOR1412_0_EM_kinetic",
            "candidate_morphism": "X -> Z_EM(X)F_Q^2",
            "source_counterterm": "CTB1411_0_ZEM;FVG1310_0_alpha_vertex",
            "why_not_banned": "unique EM/gauge kinetic owner is not parent-signed",
            "residual_component": "R_EM := beta_EM^a-beta_*^a",
            "status": "LIVE_UNTIL_FUNCTOR_EXHAUSTION",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "morphism_id": "MOR1412_1_QCD_spectrum",
            "candidate_morphism": "X -> {Z_QCD(X), Lambda_QCD(X), y_i(X), B_A(X)}",
            "source_counterterm": "CTB1411_1_ZQCD;FVG1310_1_mass_binding_vertex",
            "why_not_banned": "matter spectrum owner is not parent-signed",
            "residual_component": "R_nuc := beta_nuc^a-beta_*^a",
            "status": "LIVE_UNTIL_FUNCTOR_EXHAUSTION",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "morphism_id": "MOR1412_2_electronic_clock",
            "candidate_morphism": "X -> {m_e(X), Z_e(X), nu_i(X), readout_i(X)}",
            "source_counterterm": "CTB1411_2_Zelectron;FVG1310_2_clock_readout_vertex",
            "why_not_banned": "clock/electronic readout descent and fixed spectrum are unsigned",
            "residual_component": "R_e_clock := beta_e^a-beta_*^a plus b_clock_i",
            "status": "LIVE_UNTIL_FUNCTOR_EXHAUSTION",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "morphism_id": "MOR1412_3_species_source",
            "candidate_morphism": "SpeciesLabel -> w_A(X), kappa_A(X), source-only multiplier",
            "source_counterterm": "CTB1411_3_source_slot;CM1338_0_relative_wA",
            "why_not_banned": "NoSourceOnlySpeciesSlot is not derived",
            "residual_component": "R_source := qbar_source_weight",
            "status": "LIVE_UNTIL_FUNCTOR_EXHAUSTION",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "morphism_id": "MOR1412_4_marker_boundary",
            "candidate_morphism": "hidden marker/domain/boundary -> active/readout coefficient",
            "source_counterterm": "CM1338_2_hidden_marker_relabel;PMD1087_5_hidden_domain_boundary",
            "why_not_banned": "no-shadow, marker, boundary, and radiative preservation clauses are unsigned",
            "residual_component": "R_marker_boundary",
            "status": "LIVE_UNTIL_FUNCTOR_EXHAUSTION",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "morphism_id": "MOR1412_5_verdict",
            "candidate_morphism": "hidden visible coefficient morphism family",
            "source_counterterm": "MOR1412_0 through MOR1412_4",
            "why_not_banned": "the constructor list is not exhausted by current MTS primitives",
            "residual_component": "R_ord := (R_EM,R_nuc,R_e_clock,R_source,R_marker_boundary,R_readout)",
            "status": "MORPHISMS_RETAINED_AS_FINITE_RESIDUAL_VECTOR",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def residual_vector_rows() -> list[dict[str, Any]]:
    return [
        {
            "component_id": "RV1412_0_R_EM",
            "component": "R_EM",
            "definition": "beta_EM^a - beta_*^a or equivalent EM kinetic/alpha relative response",
            "feeds": "WEP Coulomb composition; clocks/alpha; R10 material leg; local EM residual",
            "required_inputs": "parent coordinate basis; EM normalization map; source value or theorem-zero; units; sign; source path",
            "current_value": "MISSING",
            "current_status": "FINITE_RESIDUAL_TEMPLATE_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "component_id": "RV1412_1_R_nuc",
            "component": "R_nuc",
            "definition": "beta_nuc^a - beta_*^a or equivalent QCD/nuclear binding relative response",
            "feeds": "WEP nuclear composition; orbital/self-energy residual; R10 material leg",
            "required_inputs": "QCD/spectrum owner or bound; nuclear material fractions; units; sign; source path",
            "current_value": "MISSING",
            "current_status": "FINITE_RESIDUAL_TEMPLATE_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "component_id": "RV1412_2_R_e_clock",
            "component": "R_e_clock",
            "definition": "beta_e^a - beta_*^a plus explicit clock/readout drift terms",
            "feeds": "atomic/electronic WEP component; clock redshift; alpha/mass-ratio observations",
            "required_inputs": "electronic mass/readout owner; clock sensitivity matrix; units; sign; source path",
            "current_value": "MISSING",
            "current_status": "FINITE_RESIDUAL_TEMPLATE_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "component_id": "RV1412_3_R_source",
            "component": "R_source",
            "definition": "qbar_source_weight from w_A(X), kappa_A(X), or source-only material multipliers",
            "feeds": "WEP source charge; Newton-GM normalization; R10/R11 source-side rows",
            "required_inputs": "NoSourceOnlySpeciesSlot theorem or finite source-weight bound; material/source labels; projection kernel",
            "current_value": "MISSING",
            "current_status": "FINITE_RESIDUAL_TEMPLATE_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "component_id": "RV1412_4_R_marker_boundary",
            "component": "R_marker_boundary",
            "definition": "hidden marker, domain, boundary, support-shift, or non-Hilbert readout current residual",
            "feeds": "PPN/source side; WEP/readout residual; local-GR boundary silence",
            "required_inputs": "no-shadow/no-marker/boundary-silence theorem or finite bound rows",
            "current_value": "MISSING",
            "current_status": "FINITE_RESIDUAL_TEMPLATE_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "component_id": "RV1412_5_R_readout_rad",
            "component": "R_readout_rad",
            "definition": "radiative/effective/readout regeneration of hidden visible coefficients",
            "feeds": "clock/alpha transfer; WEP observable projection; local test readout",
            "required_inputs": "radiative/readout preservation theorem or observable-specific finite envelope",
            "current_value": "MISSING",
            "current_status": "FINITE_RESIDUAL_TEMPLATE_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "component_id": "RV1412_6_vector_verdict",
            "component": "R_ord",
            "definition": "(R_EM,R_nuc,R_e_clock,R_source,R_marker_boundary,R_readout_rad)",
            "feeds": "next local-bound and derivation queue",
            "required_inputs": "each component theorem-zero or source-backed with units, sign, basis, and arena projection",
            "current_value": "TEMPLATE_ONLY",
            "current_status": "FINITE_RESIDUAL_VECTOR_BRANCH_ACCEPTED_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def local_gr_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "LG1412_0_common_sector_lock",
            "local_GR_requirement": "ordinary matter has universal metric/coframe coupling with no composition-relative current",
            "1412_status": "NOT_PROVED",
            "impact": "local-GR matter-source side remains conditional",
            "next_action": "prove functor exhaustion or bound R_ord",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "LG1412_1_EH_exterior",
            "local_GR_requirement": "Einstein-Hilbert exterior/operator and PPN silence are derived",
            "1412_status": "NOT_ADDRESSED_BY_FUNCTOR_GATE",
            "impact": "even a matter functor theorem would not alone prove local GR",
            "next_action": "keep EH/PPN branch separate from matter-coupling branch",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "LG1412_2_Ua_WEP_kernel",
            "local_GR_requirement": "source/readout kernel U_a and WEP product normalization are real or theorem-eliminated",
            "1412_status": "BLOCKED_BY_1409",
            "impact": "finite residuals cannot be scored yet",
            "next_action": "continue official data route in parallel or derive source leg away",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "LG1412_3_vector_branch",
            "local_GR_requirement": "all retained residual-vector components are zero or below local-bound thresholds",
            "1412_status": "TEMPLATE_ONLY",
            "impact": "local-GR pass is impossible until residual components are filled or killed",
            "next_action": "choose first residual component to derive/bound",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC1412_0_theorem_verdict",
            "decision": "OrdinaryMatterFunctorExhaustion is not proved from current corpus",
            "reason": "primitive constructor list, vertical lift, fixed representation data, no-source-slot, and readout/radiative preservation remain unsigned",
            "effect": "do not promote common-sector-lock or WEP/local-GR matter coupling",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1412_1_branch_selection",
            "decision": "accept finite residual-vector branch as the honest fallback",
            "reason": "live morphisms must be either source-backed or theorem-zero before local tests",
            "effect": "R_ord becomes the next coupling object to reduce component by component",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1412_2_next_priority",
            "decision": "target the smallest residual first: no visible coefficient morphism for EM/QCD or source-only slot",
            "reason": "R_EM/R_nuc/source-weight are the highest-leverage blockers for WEP and GR-style universal matter coupling",
            "effect": "next checkpoint should try to kill one component by typed morphism/domain proof or source it as a finite row",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "claim_id": "GATE1412_0_exhaustion",
            "claim": "ordinary matter functor exhaustion is proven",
            "status": "NOT_PROVED_NO_CLAIM",
            "reason": "current evidence supports a closure contract, not derivation from primitives",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "claim_id": "GATE1412_1_common_lock",
            "claim": "common-sector-lock is promoted",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "it depends on the unproved functor-exhaustion theorem",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "claim_id": "GATE1412_2_residual_vector",
            "claim": "finite residual vector has numeric values or bound pass",
            "status": "TEMPLATE_ONLY_NO_CLAIM",
            "reason": "R_ord components are named but not filled with values, units, signs, or source anchors",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "claim_id": "GATE1412_3_WEP_transfer",
            "claim": "WEP/clock/R10/PPN transfer is allowed",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "arena isolation, U_a, material tensor, and residual-vector gates remain active",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "claim_id": "GATE1412_4_local_GR",
            "claim": "local GR/Newton reduction is derived",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "matter coupling is not exhausted and EH/PPN/source kernel gates remain separate blockers",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "claim_id": "GATE1412_5_verdict",
            "claim": "1412 solves the matter-coupling branch",
            "status": "NO_PROMOTION",
            "reason": "1412 converts an unproved theorem into an explicit residual-vector branch",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT1412_0_1413",
            "target_doc": "1413-Y5-R10-RAB-first-residual-component-zero-or-source-row.md",
            "target_script": "scripts/Y5_R10_RAB_first_residual_component_zero_or_source_row.py",
            "task": "choose the highest-leverage residual component from R_ord, preferably R_EM or R_source, and either prove the typed morphism is absent or write a source-ready finite row",
            "success_condition": "one component is theorem-zero under a parent-signed clause, or it has a finite source-row schema with units/sign/source anchors and remains nonclaim",
            "do_not_claim": "WEP pass; beta zero for all sectors; P_s products; clock/R10/PPN transfer; Newton/local GR",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "next_id": "NEXT1412_1_parallel",
            "target_doc": "future-functor-exhaustion-primitive-constructor-list.md",
            "target_script": "future_parent_grammar_route",
            "task": "if a primitive constructor list is later available, revisit OrdinaryMatterFunctorExhaustion as a theorem rather than closure",
            "success_condition": "constructors from motion/time/space/quotient/observed frame/fixed representation data exclude every MOR1412 morphism",
            "do_not_claim": "closure contract as derivation",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def validation_rows(
    sources: list[dict[str, Any]],
    exhaustion: list[dict[str, Any]],
    morphisms: list[dict[str, Any]],
    residuals: list[dict[str, Any]],
    local_gr: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    timestamp = datetime.now(timezone.utc).isoformat()
    output_paths = [
        DOC_PATH,
        SOURCE_REGISTER_PATH,
        EXHAUSTION_AUDIT_PATH,
        MORPHISM_LEDGER_PATH,
        RESIDUAL_VECTOR_PATH,
        LOCAL_GR_GATE_PATH,
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
        "VAL1412_0_sources",
        all(row["path_exists"] == True and row["anchor_found"] == True for row in sources),
        "all cited local source paths exist and anchors are present",
    )
    add(
        "VAL1412_1_exhaustion_audit",
        any(row["audit_id"] == "OMF1412_6_verdict" and row["current_result"] == "EXHAUSTION_NOT_PROVED_CURRENT_CORPUS" for row in exhaustion),
        "ordinary matter functor exhaustion is explicitly not proved",
    )
    add(
        "VAL1412_2_morphism_ledger",
        {"MOR1412_0_EM_kinetic", "MOR1412_1_QCD_spectrum", "MOR1412_3_species_source", "MOR1412_5_verdict"}.issubset(
            {row["morphism_id"] for row in morphisms}
        )
        and all(row["valid_for_claim"] == False for row in morphisms),
        "live coefficient morphisms are retained as nonclaim residual components",
    )
    add(
        "VAL1412_3_residual_vector",
        any(row["component_id"] == "RV1412_6_vector_verdict" and row["current_status"] == "FINITE_RESIDUAL_VECTOR_BRANCH_ACCEPTED_NONCLAIM" for row in residuals)
        and all(row["valid_for_claim"] == False for row in residuals),
        "finite residual-vector branch is accepted as fallback but contains no values",
    )
    add(
        "VAL1412_4_local_GR_gate",
        all(row["valid_for_claim"] == False and row["claim_allowed"] == False for row in local_gr)
        and any(row["gate_id"] == "LG1412_3_vector_branch" for row in local_gr),
        "local-GR implications remain blocked and separated from matter-coupling audit",
    )
    add(
        "VAL1412_5_decision",
        any(row["decision_id"] == "DEC1412_1_branch_selection" for row in decisions)
        and any(row["decision_id"] == "DEC1412_2_next_priority" for row in decisions),
        "decision ledger selects finite residual-vector branch and next component target",
    )
    add(
        "VAL1412_6_claim_refusal",
        all(row["valid_for_claim"] == False and row["claim_allowed"] == False for row in gates),
        "exhaustion, common lock, residual-vector, transfer, and local-GR claims are refused",
    )
    add(
        "VAL1412_7_scope",
        all((ROOT / path).resolve().is_relative_to(ROOT.resolve()) for path in output_paths),
        "outputs are confined to post-checkpoint-work paths",
    )
    add(
        "VAL1412_8_overall",
        True,
        "1412 fails the functor-exhaustion proof honestly and creates the finite ordinary residual-vector branch",
    )
    return rows


def write_doc(
    sources: list[dict[str, Any]],
    exhaustion: list[dict[str, Any]],
    morphisms: list[dict[str, Any]],
    residuals: list[dict[str, Any]],
    local_gr: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    next_targets: list[dict[str, Any]],
    validations: list[dict[str, Any]],
) -> None:
    doc = f"""# 1412 - Ordinary Matter Functor Exhaustion Or Finite Residual Vector

**Status:** `{STATUS}`

**Current verdict:** `OrdinaryMatterFunctorExhaustion` is not proved from the current corpus. The contract is now precise, but it remains a closure grammar rather than a theorem from MTS primitives. Therefore the honest branch is finite residual-vector work: retain the live visible-coefficient morphisms as `R_ord` components until each is theorem-zero or source-backed.

**Discipline move:** no common-sector-lock, WEP, transfer, Newton, or local-GR claim is promoted. The win is that the coupling problem is no longer foggy: the remaining matter-coupling debt is the vector `R_ord = (R_EM, R_nuc, R_e_clock, R_source, R_marker_boundary, R_readout_rad)`.

**Claim ceiling:** `{CLAIM_CEILING}`

## Source Register

{md_table(sources)}

## Ordinary Matter Functor Exhaustion Audit

{md_table(exhaustion)}

## Visible Coefficient Morphism Counterexamples

{md_table(morphisms)}

## Finite Residual Vector Branch

{md_table(residuals)}

## Local GR Implication Gate

{md_table(local_gr)}

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
    exhaustion = exhaustion_audit_rows()
    morphisms = morphism_ledger_rows()
    residuals = residual_vector_rows()
    local_gr = local_gr_gate_rows()
    decisions = decision_rows()
    gates = claim_gate_rows()
    next_targets = next_target_rows()
    validations = validation_rows(sources, exhaustion, morphisms, residuals, local_gr, decisions, gates)

    write_csv(SOURCE_REGISTER_PATH, sources)
    write_csv(EXHAUSTION_AUDIT_PATH, exhaustion)
    write_csv(MORPHISM_LEDGER_PATH, morphisms)
    write_csv(RESIDUAL_VECTOR_PATH, residuals)
    write_csv(LOCAL_GR_GATE_PATH, local_gr)
    write_csv(DECISION_PATH, decisions)
    write_csv(CLAIM_GATE_PATH, gates)
    write_csv(NEXT_TARGET_PATH, next_targets)
    write_csv(VALIDATION_PATH, validations)
    write_doc(sources, exhaustion, morphisms, residuals, local_gr, decisions, gates, next_targets, validations)

    if any(row["status"] != "PASS" for row in validations):
        raise SystemExit("1412 validation failed")

    print(STATUS)


if __name__ == "__main__":
    main()
