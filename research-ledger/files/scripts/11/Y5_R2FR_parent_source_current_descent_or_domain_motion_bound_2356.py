from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_PARENT_SOURCE_CURRENT_DESCENT_DOMAIN_BOUND_2356"

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
FORMALIZATION = PROJECT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICRO_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"

DOC = ROOT / "2356-Y5-R2FR-parent-source-current-descent-or-domain-motion-bound.md"

PATHS = {
    "2355_doc": ROOT / "2355-Y5-R2FR-worldtube-support-owner-fixed-domain-or-Icommutator-first-row.md",
    "2355_validation": OUT / "P8_Y5_BRR545_2355_VALIDATION.csv",
    "2355_clauses": OUT / "P8_Y5_PARENT_QLOC_2355_SUPPORT_OWNER_CLAUSES.csv",
    "2355_icommutator": OUT / "P8_Y5_PARENT_QLOC_2355_ICOMMUTATOR_FIRST_ROW.csv",
    "2355_next": OUT / "P8_Y5_PARENT_QLOC_2355_NEXT_TARGET.csv",
    "1680_clauses": OUT / "P8_Y5_PARENT_QLOC_1680_SOURCE_CURRENT_OWNER_ZERO_THEOREM_CLAUSES.csv",
    "1680_proof": OUT / "P8_Y5_PARENT_QLOC_1680_PROOF_ATTEMPT_LEDGER.csv",
    "1680_contract": OUT / "P8_Y5_PARENT_QLOC_1680_FINITE_RSOURCE_COEFFICIENT_CONTRACT_NONCLAIM.csv",
    "1620_chain": OUT / "P8_Y5_PARENT_QLOC_1620_CHAIN_RULE_SOURCE_CURRENT_ZERO_ATTEMPT.csv",
    "1620_bridge": OUT / "P8_Y5_PARENT_QLOC_1620_PARENT_SIGNATURE_BRIDGE_CONTRACT.csv",
    "1620_bounds": OUT / "P8_Y5_PARENT_QLOC_1620_SOURCE_CURRENT_BOUND_FILL_ROWS.csv",
    "1156_functor": OUT / "P8_Y5_R10_1156_QUOTIENT_MATTER_FUNCTOR_SIGNATURE_AUDIT.csv",
    "1156_frame_leak": OUT / "P8_Y5_R10_1156_FRAME_LEAK_BOUND_FILL_ROWS.csv",
    "1155_coframe": OUT / "P8_Y5_R10_1155_SINGLE_OBSERVED_COFRAME_PROOF_AUDIT.csv",
    "1155_frame_rows": OUT / "P8_Y5_R10_1155_DELTA_FRAME_CAL_RESIDUAL_ROWS.csv",
    "1088_signature": OUT / "P8_Y5_R10_1088_MINIMAL_SIGNATURE_CLAUSE.csv",
    "1088_theorem": OUT / "P8_Y5_R10_1088_CONDITIONAL_ZERO_THEOREM.csv",
    "1088_counter": OUT / "P8_Y5_R10_1088_COUNTERMODEL_RETENTION.csv",
    "1016_contract": OUT / "P8_Y5_R10_1016_PARENT_SELECTOR_CONTRACT.csv",
    "1016_attempt": OUT / "P8_Y5_R10_1016_SELECTOR_THEOREM_ATTEMPT.csv",
    "1009_contract": OUT / "P8_Y5_R10_1009_PARENT_SECTOR_CONTRACT.csv",
    "1009_runner": OUT / "P8_Y5_R10_1009_SECTOR_VARIATION_RUNNER.csv",
    "1006_mhref": OUT / "P8_Y5_R10_1006_MHREF_DENOMINATOR_THEOREM_AUDIT.csv",
    "2351_mhref": OUT / "P8_Y5_PARENT_QLOC_2351_HTAU_HREF_SOURCE_ROW_STATUS.csv",
}

SOURCES = [
    ("SRC2356_00_2355_doc", "2355_doc", ["Result:", "fixed-domain worldtube route"], "2355 handoff"),
    ("SRC2356_01_2355_validation", "2355_validation", ["VAL2355_OVERALL", "PASS"], "2355 validation"),
    ("SRC2356_02_2355_clauses", "2355_clauses", ["SOC2355_2_quotient_descent", "MISSING_SOURCE_CURRENT_DESCENT_PROOF"], "2355 source-current descent gap"),
    ("SRC2356_03_2355_icommutator", "2355_icommutator", ["ICFR2355_1_domain_mask_motion", "MISSING_DCHI_OR_FIXED_DOMAIN_THEOREM"], "2355 domain-motion row"),
    ("SRC2356_04_2355_next", "2355_next", ["NEXT2355_0", "2356-Y5-R2FR-parent-source-current-descent-or-domain-motion-bound.md"], "machine handoff"),
    ("SRC2356_05_1680_clauses", "1680_clauses", ["CL1680_4", "single_source_current_owner"], "source-current owner clauses"),
    ("SRC2356_06_1680_proof", "1680_proof", ["PROOF1680_6_verdict", "THEOREM_NOT_PROVEN_FINITE_CONTRACT_REQUIRED"], "source-current owner proof verdict"),
    ("SRC2356_07_1680_contract", "1680_contract", ["RFC1680_1", "current_rescaling_residual"], "finite source-current contract"),
    ("SRC2356_08_1620_chain", "1620_chain", ["CR1620_1_zero_lemma", "EXACT_CONDITIONAL_SOURCE_CURRENT_ZERO_LEMMA"], "chain-rule source-current zero lemma"),
    ("SRC2356_09_1620_bridge", "1620_bridge", ["BRC1620_2_matter_descent", "DESCENT_NOT_SIGNED"], "parent signature bridge"),
    ("SRC2356_10_1620_bounds", "1620_bounds", ["SCB1620_0_JZ_bulk", "MISSING_PARENT_DESCENT_OR_NUMERIC_BOUND"], "source-current bound rows"),
    ("SRC2356_11_1156_functor", "1156_functor", ["QMF1156_4_matter_factorization", "NOT_PARENT_SIGNED"], "quotient matter functor status"),
    ("SRC2356_12_1156_frame_leak", "1156_frame_leak", ["FLB1156_7_epsilon_frame_leak", "BLOCKED_MISSING_COMPONENTS"], "frame leak fallback rows"),
    ("SRC2356_13_1155_coframe", "1155_coframe", ["COF1155_2_matter_functor", "NOT_PARENT_SIGNED"], "single observed coframe audit"),
    ("SRC2356_14_1155_frame_rows", "1155_frame_rows", ["DFR1155_3_Delta_W_support", "MISSING_SUPPORT_FRAME_EQUIVALENCE"], "support/frame residual rows"),
    ("SRC2356_15_1088_signature", "1088_signature", ["MOMS1088_0_action_form", "CONDITIONAL_CLAUSE_WRITTEN_NOT_PARENT_DERIVED"], "minimal matter signature"),
    ("SRC2356_16_1088_theorem", "1088_theorem", ["THM1088_5_conclusion", "ZERO_THEOREM_PROVED_UNDER_MOMS1088_SIGNATURE"], "conditional zero theorem"),
    ("SRC2356_17_1088_counter", "1088_counter", ["CM1088_0_species_weight", "NOT_KILLED_BY_CURRENT_CORPUS"], "countermodel retention"),
    ("SRC2356_18_1016_contract", "1016_contract", ["PSC1016_7_coupling_descent_silence", "not_signed_coupling_bound_schema_only"], "coupling descent selector clause"),
    ("SRC2356_19_1016_attempt", "1016_attempt", ["PST1016_3_coupling_descent_gate", "schema_only_not_signed"], "coupling descent theorem attempt"),
    ("SRC2356_20_1009_contract", "1009_contract", ["PCS1009_2_universal_matter", "conditional_source_input"], "universal matter sector contract"),
    ("SRC2356_21_1009_runner", "1009_runner", ["SVR1009_4_worldtube_glue_conditional", "REFUSED_INCOMPLETE_PARENT_CURRENT_CHAIN_CONTRACT"], "sector variation refusal"),
    ("SRC2356_22_1006_mhref", "1006_mhref", ["MHA1006_6_theorem_verdict", "fail_current_claim"], "M_H_ref denominator block"),
    ("SRC2356_23_2351_mhref", "2351_mhref", ["HHS2351_3_MHref", "MISSING_H_TAU_H_REF_MHREF"], "latest M_H_ref status"),
]

OUTPUTS = {
    "sources": OUT / "P8_Y5_PARENT_QLOC_2356_SOURCE_REGISTER.csv",
    "theorem": OUT / "P8_Y5_PARENT_QLOC_2356_SOURCE_CURRENT_DESCENT_THEOREM_AUDIT.csv",
    "clauses": OUT / "P8_Y5_PARENT_QLOC_2356_PARENT_DESCENT_CLAUSES.csv",
    "domain_bound": OUT / "P8_Y5_PARENT_QLOC_2356_DOMAIN_MOTION_BOUND_ROWS.csv",
    "envelope": OUT / "P8_Y5_PARENT_QLOC_2356_SOURCE_DOMAIN_ENVELOPE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2356_DECISION_LEDGER.csv",
    "claims": OUT / "P8_Y5_PARENT_QLOC_2356_CLAIM_GATES.csv",
    "refusal": OUT / "P8_Y5_PARENT_QLOC_2356_REFUSAL_RUNNER.csv",
    "next": OUT / "P8_Y5_PARENT_QLOC_2356_NEXT_TARGET.csv",
    "copies": OUT / "P8_Y5_PARENT_QLOC_2356_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2356_VALIDATION.csv",
}


def b(value: bool) -> str:
    return "true" if value else "false"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def has_needles(path: Path, needles: list[str]) -> bool:
    text = read_text(path)
    return path.exists() and all(needle in text for needle in needles)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key not in headers:
                headers.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8", errors="replace") as handle:
        return list(csv.DictReader(handle))


def source_rows() -> list[dict[str, Any]]:
    rows = []
    for row_id, source_key, needles, role in SOURCES:
        path = PATHS[source_key]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "row_id": row_id,
                "source_key": source_key,
                "path": str(path),
                "exists": b(path.exists()),
                "required_needles": ";".join(needles),
                "needles_found": b(has_needles(path, needles)),
                "source_role": role,
                "valid_for_claim": "false",
            }
        )
    return rows


def theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "SCD2356_0_chain_rule_identity",
            "statement": "For vertical v, delta_v S_matter decomposes into quotient, matter-lift, constants/markers, direct source slot, and boundary terms.",
            "mathematical_form": "delta_v S_m = DSbar[Dq(v)] + E_psi delta_v psi + J_theta L_v theta + J_direct[v] + delta_v B",
            "status": "EXACT_IDENTITY_OR_NORMAL_FORM",
            "proof_result": "source-current zero becomes explicit premises, not vibes",
            "missing_for_current_MTS": "parent matter action and owned lift data",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SCD2356_1_descent_theorem",
            "statement": "If S_matter factors through q and all vertical lifts are gauge/Euler/boundary-only, then the bulk vertical source current vanishes.",
            "mathematical_form": "S_m[Phi,psi]=Sbar_m[q(Phi),psi_bar,theta]+dB and Dq(v)=0 => J_v^matter=0 modulo owned boundary/gauge terms",
            "status": "EXACT_CONDITIONAL_THEOREM",
            "proof_result": "this is the clean coupling theorem needed by the local branch",
            "missing_for_current_MTS": "q object; Dq verticality; matter functor; constants; boundary; readout stability",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SCD2356_2_support_corollary",
            "statement": "If J_H=q^*Jbar_H with regular compact support, quotient support is vertically fixed.",
            "mathematical_form": "W_source=closure(supp J_H), J_H=q^*Jbar_H => D_v q(W_source)=0 on regular support strata",
            "status": "EXACT_CONDITIONAL_COROLLARY",
            "proof_result": "vertical support motion disappears only for the quotient-owned support object",
            "missing_for_current_MTS": "regular support; pullback source current; source-free annulus; no boundary tail",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SCD2356_3_domain_motion_normal_form",
            "statement": "If any descent clause fails, domain motion is a real first-row term.",
            "mathematical_form": "I_domain_motion = int_A dchi_W wedge P_M J_H + int_boundary(A) i_v(Pi_W J_H) + int_A chi_W P_M dJ_escape",
            "status": "NORMAL_FORM_RETAINED",
            "proof_result": "failed coupling descent becomes a finite row, not an assumed zero",
            "missing_for_current_MTS": "dchi/source-boundary values; M_H_ref; projection units",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SCD2356_4_noether_not_enough",
            "statement": "Diffeomorphism covariance/Noether conservation alone does not prove quotient descent.",
            "mathematical_form": "dJ=0 does not imply J=q^*Jbar, and conserved wrong-object currents do not fix source support",
            "status": "SHORTCUT_REFUSED",
            "proof_result": "blocks the seductive but false route from conservation to measured source ownership",
            "missing_for_current_MTS": "same-object Hilbert/topological equality and coupling descent",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SCD2356_5_countermodel_retained",
            "statement": "Species weights, variable constants, shadow frames, post-variation selectors, and boundary markers remain legal without the parent signature.",
            "mathematical_form": "S_m -> sum_A w_A(X) S_A or g_A=A_A(X)^2 g_obs creates J_v != 0 while visible q-geometry can look fixed",
            "status": "COUNTERMODEL_ACTIVE",
            "proof_result": "current corpus cannot promote J_H=q^*Jbar_H as current-MTS theorem",
            "missing_for_current_MTS": "object-language/current-owner/no-shadow clauses",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SCD2356_6_current_corpus_verdict",
            "statement": "Parent source-current descent is derived only as a conditional theorem in the current corpus.",
            "mathematical_form": "SCD2356_1 plus SCD2356_2 are exact if PDC2356_0..8 are parent-signed; otherwise use DMB2356 rows",
            "status": "THEOREM_CONDITIONAL_APPLICATION_BLOCKED",
            "proof_result": "local GR/Newton source ownership is closer but not closed",
            "missing_for_current_MTS": "one parent matter-coupling action or numeric domain-motion inputs",
            "valid_for_claim": "false",
        },
    ]


def parent_descent_clause_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "PDC2356_0_parent_q_object",
            "required_clause": "parent quotient map exists before matter/readout",
            "required_form": "q: Phi_parent -> Q_obs is part of parent kinematics/action",
            "current_status": "Q_OBJECT_NOT_PARENT_SIGNED",
            "failure_if_missing": "Dq(v)=0 is notation, not theorem",
            "residual_if_missing": "Dq_vertical_leak",
            "parent_signed": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PDC2356_1_vertical_generator",
            "required_clause": "local residual direction is actually quotient-vertical",
            "required_form": "v_X in ker(Dq) on an open local branch, not just at a point or by label",
            "current_status": "VERTICALITY_NOT_SIGNED",
            "failure_if_missing": "source current can couple to a physical local mode",
            "residual_if_missing": "J_vertical_physical",
            "parent_signed": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PDC2356_2_matter_action_factorization",
            "required_clause": "ordinary matter action factors through q",
            "required_form": "S_matter[Phi,psi]=Sbar_matter[q(Phi),psi,theta]+dB",
            "current_status": "MATTER_DESCENT_NOT_PARENT_SIGNED",
            "failure_if_missing": "representative Weyl/disformal/source-only couplings remain legal",
            "residual_if_missing": "J_matter_descent_leak",
            "parent_signed": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PDC2356_3_owned_matter_lift",
            "required_clause": "matter-field vertical lift is gauge/Euler/boundary only",
            "required_form": "delta_v psi_A is zero, gauge, local-Lorentz, diffeo, Euler-proportional, or exact-boundary",
            "current_status": "MATTER_LIFT_OWNER_OPEN",
            "failure_if_missing": "bulk matter lift creates source current despite Dq(v)=0",
            "residual_if_missing": "J_matter_lift",
            "parent_signed": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PDC2356_4_constants_superselection",
            "required_clause": "masses, charges, clock standards and representation labels are quotient-owned constants",
            "required_form": "L_v theta_A=0 for ordinary matter constants unless retained as finite coefficient rows",
            "current_status": "CONSTANT_SUPERSELECTION_UNSIGNED",
            "failure_if_missing": "composition/clock/EM source currents survive",
            "residual_if_missing": "J_theta",
            "parent_signed": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PDC2356_5_no_source_only_slot",
            "required_clause": "no pre-action species weights, current rescalings, source-only markers or shadow frames",
            "required_form": "Hom(hidden/source labels, active source coefficients)=Const or absent before variation",
            "current_status": "NO_SOURCE_ONLY_SLOT_NOT_DERIVED",
            "failure_if_missing": "source-current zero can be counterfeited by hidden weights",
            "residual_if_missing": "J_source_only_slot",
            "parent_signed": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PDC2356_6_variation_before_readout",
            "required_clause": "Hilbert/source current is extracted before material/readout projection",
            "required_form": "delta S_parent precedes arena/material/source support selection",
            "current_status": "VARIATION_ORDER_CONDITIONAL_ONLY",
            "failure_if_missing": "post-variation selector manufactures a conserved-looking current",
            "residual_if_missing": "J_readout_selector",
            "parent_signed": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PDC2356_7_boundary_support_silence",
            "required_clause": "boundary, worldtube, support, and exterior tails are zero/proper or bounded",
            "required_form": "delta_v B=0/proper and no hidden source/anomaly tail crosses the support annulus",
            "current_status": "BOUNDARY_SUPPORT_SILENCE_OPEN",
            "failure_if_missing": "bulk descent does not control the finite source/domain row",
            "residual_if_missing": "J_boundary_support",
            "parent_signed": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PDC2356_8_MHref_normalization",
            "required_clause": "M_H_ref is positive, parent-derived, same-frame, and not orbital-GM backfilled",
            "required_form": "M_H_ref=H_tau[S_outer]-H_ref>0 with fixed tau/coframe/reference",
            "current_status": "MISSING_H_TAU_H_REF_MHREF",
            "failure_if_missing": "domain-motion/source-current row cannot be dimensionless or noncircular",
            "residual_if_missing": "J_denominator",
            "parent_signed": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PDC2356_9_verdict",
            "required_clause": "all parent source-current descent clauses close together",
            "required_form": "PDC2356_0 through PDC2356_8 parent-signed in one branch",
            "current_status": "DESCENT_CHAIN_NOT_CLOSED",
            "failure_if_missing": "keep domain-motion bound rows live",
            "residual_if_missing": "epsilon_source_domain_motion",
            "parent_signed": "false",
            "valid_for_claim": "false",
        },
    ]


def domain_motion_bound_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "DMB2356_0_total",
            "quantity": "epsilon_source_domain_motion_abs",
            "component": "absolute envelope for failed source-current descent/domain-motion terms",
            "formula": "abs(J_qdesc+J_lift+J_theta+J_slot+J_boundary+I_domain_mask+I_boundary_crossing)/M_H_ref",
            "units": "dimensionless after parent source-current and M_H_ref normalization",
            "status": "MISSING_COMPONENT_VALUES",
            "source_required": "all numerator terms, M_H_ref, units, extraction method, and source paths",
            "valid_for_claim": "false",
            "score_ready": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DMB2356_1_J_qdesc",
            "quantity": "J_qdesc",
            "component": "failure of matter action to factor through q",
            "formula": "||delta_v S_matter - DSbar[Dq(v)]||_bulk",
            "units": "action-variation or source-current units over M_H_ref",
            "status": "MISSING_MATTER_DESCENT_PROOF_OR_NUMERIC_BOUND",
            "source_required": "parent matter action or finite residual coefficient with basis and units",
            "valid_for_claim": "false",
            "score_ready": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DMB2356_2_J_lift",
            "quantity": "J_matter_lift",
            "component": "unowned matter-field vertical lift",
            "formula": "||E_psi delta_v psi||_bulk plus non-Euler/gauge pieces",
            "units": "source-current units over M_H_ref",
            "status": "MISSING_MATTER_LIFT_OWNER",
            "source_required": "matter bundle functor/lift theorem or numeric lift coefficient",
            "valid_for_claim": "false",
            "score_ready": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DMB2356_3_J_theta",
            "quantity": "J_theta",
            "component": "constant/material/clock/EM derivative",
            "formula": "sum_a J_theta^a L_v theta_a",
            "units": "source-current units over M_H_ref",
            "status": "MISSING_CONSTANT_SUPERSELECTION_OR_COEFFICIENTS",
            "source_required": "constant superselection theorem or alpha/mass/clock sensitivity coefficients",
            "valid_for_claim": "false",
            "score_ready": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DMB2356_4_J_slot",
            "quantity": "J_source_only_slot",
            "component": "pre-action species weights/current rescalings/shadow frames/source markers",
            "formula": "sum_A (partial_v ln w_A or partial_v ln c_A or shadow-frame derivative) source_A",
            "units": "dimensionless coefficient times source-current units over M_H_ref",
            "status": "MISSING_NO_SOURCE_ONLY_SLOT_OR_COEFFICIENTS",
            "source_required": "object-language/current-owner proof or finite coefficient rows",
            "valid_for_claim": "false",
            "score_ready": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DMB2356_5_J_boundary",
            "quantity": "J_boundary_support",
            "component": "boundary/support/worldtube tail after bulk descent",
            "formula": "abs(delta_v B + exterior/source-tail flux)/M_H_ref",
            "units": "boundary source-current units over M_H_ref",
            "status": "MISSING_BOUNDARY_SUPPORT_SILENCE_OR_BOUND",
            "source_required": "zero/proper boundary theorem or numeric tail/flux row",
            "valid_for_claim": "false",
            "score_ready": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DMB2356_6_I_domain_mask",
            "quantity": "I_domain_mask",
            "component": "moving support/domain mask",
            "formula": "abs(int_A dchi_W wedge P_M J_H)/M_H_ref",
            "units": "source flux over M_H_ref",
            "status": "MISSING_DCHI_OR_FIXED_DOMAIN_THEOREM",
            "source_required": "fixed W_source theorem from descent or source-backed dchi row",
            "valid_for_claim": "false",
            "score_ready": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DMB2356_7_I_boundary_crossing",
            "quantity": "I_boundary_crossing",
            "component": "support/linking surface crossing term",
            "formula": "abs(int_boundary(A_ext) i_v(Pi_W J_H))/M_H_ref",
            "units": "source flux over M_H_ref",
            "status": "MISSING_BOUNDARY_CROSSING_BOUND",
            "source_required": "zero boundary-crossing theorem or numeric surface flux row",
            "valid_for_claim": "false",
            "score_ready": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DMB2356_8_acceptance_rule",
            "quantity": "domain_motion_bound_acceptance",
            "component": "acceptance gate for replacing descent proof by finite sourced row",
            "formula": "valid only if every missing component is theorem-zero or numeric with units/source path and M_H_ref is noncircular",
            "units": "gate",
            "status": "NONCLAIM_ACCEPTANCE_RULE_INSTALLED",
            "source_required": "no MISSING_* statuses before scoring",
            "valid_for_claim": "false",
            "score_ready": "false",
        },
    ]


def envelope_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "ENV2356_0_zero_path",
            "path": "source-current descent proof",
            "condition": "all PDC2356 clauses parent-signed in one action branch",
            "output": "J_v^matter=0, D_v q(W_source)=0, and I_domain_mask theorem-zero modulo owned boundary terms",
            "current_status": "CONDITIONAL_ONLY",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "ENV2356_1_bound_path",
            "path": "domain-motion/source-current finite row",
            "condition": "any PDC2356 clause remains unsigned",
            "output": "epsilon_source_domain_motion_abs from DMB2356 rows",
            "current_status": "MISSING_COMPONENT_VALUES",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "ENV2356_2_gr_newton_gate",
            "path": "local GR/Newton source gate",
            "condition": "zero path closes or bound path is numerically small with noncircular M_H_ref and observable projection",
            "output": "reopen local PPN/Newton source-normalization tests",
            "current_status": "BLOCKED_NONCLAIM",
            "valid_for_claim": "false",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2356_0_result",
            "decision": "do not claim parent source-current descent for current MTS",
            "reason": "the descent theorem is exact conditionally, but q, verticality, matter factorization, constants, no-source-slot, boundary, and M_H_ref are unsigned",
            "effect": "local GR/Newton remains blocked but now has a precise coupling theorem target",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2356_1_progress",
            "decision": "preserve the theorem as the clean route",
            "reason": "if a parent matter action factors through q, the source current and support motion vanish by chain rule rather than by axiom",
            "effect": "this is the derivable version of the coupling intuition",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2356_2_bound_fallback",
            "decision": "install domain-motion/source-current bound rows",
            "reason": "without source-current descent, the moving-domain and source-only-slot terms must be explicit",
            "effect": "no hidden post-readout mask or measured-GM backfill",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2356_3_next",
            "decision": "select minimal parent matter-coupling action next",
            "reason": "the quickest honest route is to write the exact action/coupling contract that would sign PDC2356_2 through PDC2356_6, then test it against countermodels",
            "effect": "2357 targets a real coupling action form or first numeric domain-motion row",
            "valid_for_claim": "false",
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2356_0_source_current_descent",
            "claim": "J_H=q^*Jbar_H and J_v^matter=0",
            "passes_public_claim": "false",
            "blocked_by": "PDC2356_0_parent_q_object;PDC2356_2_matter_action_factorization;PDC2356_5_no_source_only_slot",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2356_1_fixed_worldtube",
            "claim": "D_v W_source=0 and domain-motion rows vanish",
            "passes_public_claim": "false",
            "blocked_by": "PDC2356_3_owned_matter_lift;PDC2356_7_boundary_support_silence;DMB2356_6_I_domain_mask",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2356_2_dimensionless_bound",
            "claim": "epsilon_source_domain_motion_abs is score-ready",
            "passes_public_claim": "false",
            "blocked_by": "PDC2356_8_MHref_normalization;DMB2356_0_total",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2356_3_local_GR_Newton",
            "claim": "local GR/Newton source-normalization gate can reopen",
            "passes_public_claim": "false",
            "blocked_by": "source-current descent not parent-signed; finite bound rows missing values; M_H_ref missing",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2356_4_public_update",
            "claim": "ready for GitHub/public claim",
            "passes_public_claim": "false",
            "blocked_by": "private nonclaim checkpoint and open local-GR derivation gate",
            "valid_for_claim": "false",
        },
    ]


def refusal_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2356_0_noether_shortcut",
            "temptation": "use diffeomorphism covariance or dJ=0 to claim source-current descent",
            "allowed": "false",
            "why_not": "conservation does not prove J_H is a pullback from q or that it is the measured source object",
            "blocking_rows": "SCD2356_4_noether_not_enough;PDC2356_2_matter_action_factorization",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2356_1_vertical_by_label",
            "temptation": "call the residual direction vertical without deriving q and Dq(v)=0",
            "allowed": "false",
            "why_not": "verticality must be a parent map statement on an open branch",
            "blocking_rows": "PDC2356_0_parent_q_object;PDC2356_1_vertical_generator",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2356_2_minimal_signature_as_axiom",
            "temptation": "adopt the 1088 matter signature as if already derived",
            "allowed": "false",
            "why_not": "it is an exact contract, not current-corpus evidence until a parent action signs it",
            "blocking_rows": "PDC2356_2_matter_action_factorization;PDC2356_5_no_source_only_slot",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2356_3_observed_GM_backfill",
            "temptation": "normalize the domain-motion row with observed orbital GM",
            "allowed": "false",
            "why_not": "that imports the Newton limit into the proof rather than deriving it",
            "blocking_rows": "PDC2356_8_MHref_normalization;CG2356_2_dimensionless_bound",
            "valid_for_claim": "false",
        },
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2356_0",
            "next_target": "2357-Y5-R2FR-minimal-parent-matter-coupling-action-or-domain-motion-input.md",
            "why": "write/test the exact parent matter-coupling action that would sign source-current descent, no-source-slot, and variation-before-readout",
            "route_type": "derivation_first",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2356_1",
            "next_target": "2357b-Y5-R2FR-domain-motion-numeric-input-pack.md",
            "why": "fallback if the matter-coupling action cannot be parent-signed: source the DMB2356 numerator rows and M_H_ref",
            "route_type": "fallback_nonclaim",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2356_2",
            "next_target": "2357c-Y5-R2FR-q-object-vertical-generator-open-branch-proof.md",
            "why": "parallel if matter factorization is plausible but q/v_X verticality still lacks a parent open-branch proof",
            "route_type": "parallel_nonclaim",
            "valid_for_claim": "false",
        },
    ]


def copy_branch_artifacts() -> list[dict[str, Any]]:
    copies = [
        (OUTPUTS["clauses"], BETA_DOCS / "PARENT_DESCENT_CLAUSES_2356_NONCLAIM.csv", "beta docs parent descent clauses"),
        (OUTPUTS["domain_bound"], MICRO_RESIDUALS / "DOMAIN_MOTION_BOUND_ROWS_2356_NONCLAIM.csv", "microscope domain-motion rows"),
        (OUTPUTS["decision"], RAB_QUEUE / "JR2356_SOURCE_CURRENT_DESCENT_DECISION_NONCLAIM.csv", "RAB queue decision ledger"),
    ]
    rows = []
    for src, dst, role in copies:
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dst)
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "row_id": f"COPY2356_{len(rows)}",
                "source": str(src),
                "destination": str(dst),
                "copy_role": role,
                "copy_exists": b(dst.exists() and dst.stat().st_size > 0),
                "valid_for_claim": "false",
            }
        )
    return rows


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = [
        "| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |"
        for row in rows
    ]
    return "\n".join([header, separator, *body]) + "\n"


def write_markdown(
    sources: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    clauses: list[dict[str, Any]],
    domain_bound: list[dict[str, Any]],
    envelope: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    claims: list[dict[str, Any]],
    refusals: list[dict[str, Any]],
    next_targets: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    created = datetime.now(timezone.utc).isoformat()
    text = f"""# 2356 — Parent Source-Current Descent Or Domain-Motion Bound

Created UTC: `{created}`

Branch: `{BRANCH_ID}`

## Result

Result: the **parent source-current descent theorem is now written in its exact conditional form**:

`S_matter[Phi,psi] = Sbar_matter[q(Phi),psi,theta] + dB` and `Dq(v)=0`
imply `J_v^matter=0` only if the matter lift, constants, source-only slots, boundary/support terms, readout order,
and `M_H_ref` normalization are all parent-owned.

That is progress, but **not yet a local-GR/Newton claim**. Current MTS still lacks the one parent matter-coupling action
that signs those clauses together. The fallback is now explicit: every failed clause feeds the domain-motion/source-current
bound `epsilon_source_domain_motion_abs`.

## Source Audit

{md_table(sources, ["row_id", "source_key", "exists", "needles_found", "source_role"])}

## Source-Current Descent Theorem Audit

{md_table(theorem, ["row_id", "status", "statement", "proof_result", "missing_for_current_MTS", "valid_for_claim"])}

## Parent Descent Clauses

{md_table(clauses, ["row_id", "required_clause", "current_status", "failure_if_missing", "residual_if_missing", "parent_signed", "valid_for_claim"])}

## Domain-Motion Bound Rows

{md_table(domain_bound, ["row_id", "quantity", "component", "formula", "status", "units", "score_ready", "valid_for_claim"])}

## Source-Domain Envelope

{md_table(envelope, ["row_id", "path", "condition", "output", "current_status", "valid_for_claim"])}

## Decision Ledger

{md_table(decisions, ["row_id", "decision", "reason", "effect", "valid_for_claim"])}

## Claim Gates

{md_table(claims, ["row_id", "claim", "passes_public_claim", "blocked_by", "valid_for_claim"])}

## Refusal Runner

{md_table(refusals, ["row_id", "temptation", "allowed", "why_not", "blocking_rows", "valid_for_claim"])}

## Next Targets

{md_table(next_targets, ["row_id", "next_target", "why", "route_type", "valid_for_claim"])}

## Validation

{md_table(validation, ["row_id", "status", "detail", "valid_for_claim"])}
"""
    DOC.write_text(text, encoding="utf-8")


def formalization_hits() -> list[Path]:
    if not FORMALIZATION.exists():
        return []
    hits: list[Path] = []
    for path in FORMALIZATION.rglob("*2356*"):
        if not path.is_file():
            continue
        parts = {part.lower() for part in path.parts}
        if ".venv" in parts or "site-packages" in parts or "__pycache__" in parts:
            continue
        if path.name.startswith(("2356-", "P8_Y5_PARENT_QLOC_2356", "P8_Y5_BRR545_2356")):
            hits.append(path)
    return hits


def no_true_claim_flags(paths: list[Path]) -> bool:
    guarded_columns = {
        "valid_for_claim",
        "passes_public_claim",
        "score_ready",
        "claim_allowed",
        "valid_prediction_row",
        "parent_signed",
    }
    for path in paths:
        if path.suffix.lower() != ".csv":
            continue
        for row in read_csv(path):
            for column in guarded_columns:
                if row.get(column, "").strip().lower() == "true":
                    return False
    return True


def validation_rows(sources: list[dict[str, Any]], copies: list[dict[str, Any]]) -> list[dict[str, Any]]:
    produced = [path for key, path in OUTPUTS.items() if key != "validation"]
    theorem_text = read_text(OUTPUTS["theorem"])
    clauses = read_csv(OUTPUTS["clauses"])
    domain_bound = read_csv(OUTPUTS["domain_bound"])
    claims = read_csv(OUTPUTS["claims"])
    next_text = read_text(OUTPUTS["next"])
    checks = [
        ("VAL2356_00_required_sources_exist", all(row["exists"] == "true" for row in sources), "every required source path exists"),
        ("VAL2356_01_required_needles_found", all(row["needles_found"] == "true" for row in sources), "all required source needles were found"),
        ("VAL2356_02_outputs_exist", all(path.exists() and path.stat().st_size > 0 for path in produced), "all 2356 outputs written"),
        ("VAL2356_03_conditional_theorem_written", "SCD2356_1_descent_theorem" in theorem_text and "EXACT_CONDITIONAL_THEOREM" in theorem_text, "parent source-current descent theorem written conditionally"),
        ("VAL2356_04_application_blocked", "SCD2356_6_current_corpus_verdict" in theorem_text and "THEOREM_CONDITIONAL_APPLICATION_BLOCKED" in theorem_text, "current MTS application remains blocked"),
        ("VAL2356_05_parent_clauses_nonclaim", clauses and all(row.get("parent_signed") == "false" and row.get("valid_for_claim") == "false" for row in clauses), "parent descent clauses remain unsigned/nonclaim"),
        ("VAL2356_06_domain_rows_nonclaim", domain_bound and all(row.get("score_ready") == "false" and row.get("valid_for_claim") == "false" for row in domain_bound), "domain-motion rows remain non-score-ready"),
        ("VAL2356_07_claim_gates_blocked", claims and all(row.get("passes_public_claim") == "false" and row.get("valid_for_claim") == "false" for row in claims), "all public claim gates blocked"),
        ("VAL2356_08_next_selected", "2357-Y5-R2FR-minimal-parent-matter-coupling-action-or-domain-motion-input.md" in next_text, "2357 minimal matter-coupling action target selected"),
        ("VAL2356_09_branch_copies_parse", copies and all(row["copy_exists"] == "true" for row in copies), "branch copies exist"),
        ("VAL2356_10_formalization_untouched", not formalization_hits(), "no 2356 checkpoint output appears in formalization-workbench"),
        ("VAL2356_11_no_claim_flags", no_true_claim_flags(produced), "no generated row has claim/score-ready/parent-signed true flags"),
        ("VAL2356_12_no_github_policy", True, "public GitHub update not recommended from 2356"),
    ]
    rows = [
        {
            "row_id": row_id,
            "status": "PASS" if ok else "FAIL",
            "detail": detail,
            "valid_for_claim": "false",
        }
        for row_id, ok, detail in checks
    ]
    rows.append(
        {
            "row_id": "VAL2356_OVERALL",
            "status": "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL",
            "detail": "2356 derives the parent source-current descent theorem conditionally, refuses current-MTS promotion, installs domain-motion/source-current bound rows, and selects minimal parent matter-coupling action as 2357.",
            "valid_for_claim": "false",
        }
    )
    return rows


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)

    sources = source_rows()
    theorem = theorem_rows()
    clauses = parent_descent_clause_rows()
    domain_bound = domain_motion_bound_rows()
    envelope = envelope_rows()
    decisions = decision_rows()
    claims = claim_gate_rows()
    refusals = refusal_rows()
    next_targets = next_rows()

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["theorem"], theorem)
    write_csv(OUTPUTS["clauses"], clauses)
    write_csv(OUTPUTS["domain_bound"], domain_bound)
    write_csv(OUTPUTS["envelope"], envelope)
    write_csv(OUTPUTS["decision"], decisions)
    write_csv(OUTPUTS["claims"], claims)
    write_csv(OUTPUTS["refusal"], refusals)
    write_csv(OUTPUTS["next"], next_targets)

    copies = copy_branch_artifacts()
    write_csv(OUTPUTS["copies"], copies)

    validation = validation_rows(sources, copies)
    write_csv(OUTPUTS["validation"], validation)
    write_markdown(sources, theorem, clauses, domain_bound, envelope, decisions, claims, refusals, next_targets, validation)

    if validation[-1]["status"] != "PASS":
        failed = ", ".join(row["row_id"] for row in validation if row["status"] != "PASS")
        raise SystemExit(f"2356 validation failed: {failed}")
    print(f"2356 checkpoint written: {DOC}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
