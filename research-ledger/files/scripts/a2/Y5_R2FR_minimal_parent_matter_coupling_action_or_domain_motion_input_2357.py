from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_MINIMAL_PARENT_MATTER_COUPLING_ACTION_2357"

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
FORMALIZATION = PROJECT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICRO_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"

DOC = ROOT / "2357-Y5-R2FR-minimal-parent-matter-coupling-action-or-domain-motion-input.md"

PATHS = {
    "2356_doc": ROOT / "2356-Y5-R2FR-parent-source-current-descent-or-domain-motion-bound.md",
    "2356_validation": OUT / "P8_Y5_BRR545_2356_VALIDATION.csv",
    "2356_theorem": OUT / "P8_Y5_PARENT_QLOC_2356_SOURCE_CURRENT_DESCENT_THEOREM_AUDIT.csv",
    "2356_clauses": OUT / "P8_Y5_PARENT_QLOC_2356_PARENT_DESCENT_CLAUSES.csv",
    "2356_domain": OUT / "P8_Y5_PARENT_QLOC_2356_DOMAIN_MOTION_BOUND_ROWS.csv",
    "2356_next": OUT / "P8_Y5_PARENT_QLOC_2356_NEXT_TARGET.csv",
    "1088_signature": OUT / "P8_Y5_R10_1088_MINIMAL_SIGNATURE_CLAUSE.csv",
    "1088_theorem": OUT / "P8_Y5_R10_1088_CONDITIONAL_ZERO_THEOREM.csv",
    "1088_counter": OUT / "P8_Y5_R10_1088_COUNTERMODEL_RETENTION.csv",
    "1156_functor": OUT / "P8_Y5_R10_1156_QUOTIENT_MATTER_FUNCTOR_SIGNATURE_AUDIT.csv",
    "1155_coframe": OUT / "P8_Y5_R10_1155_SINGLE_OBSERVED_COFRAME_PROOF_AUDIT.csv",
    "1016_contract": OUT / "P8_Y5_R10_1016_PARENT_SELECTOR_CONTRACT.csv",
    "1016_claim": OUT / "P8_Y5_R10_1016_CLAIM_GATE.csv",
    "1009_contract": OUT / "P8_Y5_R10_1009_PARENT_SECTOR_CONTRACT.csv",
    "1009_claim": OUT / "P8_Y5_R10_1009_CLAIM_GATE.csv",
    "1680_clauses": OUT / "P8_Y5_PARENT_QLOC_1680_SOURCE_CURRENT_OWNER_ZERO_THEOREM_CLAUSES.csv",
    "1680_proof": OUT / "P8_Y5_PARENT_QLOC_1680_PROOF_ATTEMPT_LEDGER.csv",
    "1620_chain": OUT / "P8_Y5_PARENT_QLOC_1620_CHAIN_RULE_SOURCE_CURRENT_ZERO_ATTEMPT.csv",
    "2351_mhref": OUT / "P8_Y5_PARENT_QLOC_2351_HTAU_HREF_SOURCE_ROW_STATUS.csv",
}

SOURCES = [
    ("SRC2357_00_2356_doc", "2356_doc", ["Result:", "parent source-current descent theorem"], "2356 handoff"),
    ("SRC2357_01_2356_validation", "2356_validation", ["VAL2356_OVERALL", "PASS"], "2356 validation"),
    ("SRC2357_02_2356_theorem", "2356_theorem", ["SCD2356_1_descent_theorem", "EXACT_CONDITIONAL_THEOREM"], "source-current descent theorem"),
    ("SRC2357_03_2356_clauses", "2356_clauses", ["PDC2356_2_matter_action_factorization", "MATTER_DESCENT_NOT_PARENT_SIGNED"], "matter factorization clause"),
    ("SRC2357_04_2356_domain", "2356_domain", ["DMB2356_0_total", "MISSING_COMPONENT_VALUES"], "domain-motion fallback"),
    ("SRC2357_05_2356_next", "2356_next", ["NEXT2356_0", "2357-Y5-R2FR-minimal-parent-matter-coupling-action-or-domain-motion-input.md"], "machine handoff"),
    ("SRC2357_06_1088_signature", "1088_signature", ["MOMS1088_0_action_form", "CONDITIONAL_CLAUSE_WRITTEN_NOT_PARENT_DERIVED"], "minimal ordinary matter signature"),
    ("SRC2357_07_1088_theorem", "1088_theorem", ["THM1088_5_conclusion", "ZERO_THEOREM_PROVED_UNDER_MOMS1088_SIGNATURE"], "conditional matter zero theorem"),
    ("SRC2357_08_1088_counter", "1088_counter", ["CM1088_2_shadow_frame", "NOT_KILLED_BY_CURRENT_CORPUS"], "countermodel retention"),
    ("SRC2357_09_1156_functor", "1156_functor", ["QMF1156_4_matter_factorization", "NOT_PARENT_SIGNED"], "quotient matter functor"),
    ("SRC2357_10_1155_coframe", "1155_coframe", ["COF1155_7_verdict", "SINGLE_OBSERVED_COFRAME_NOT_DERIVED"], "single coframe verdict"),
    ("SRC2357_11_1016_contract", "1016_contract", ["PSC1016_7_coupling_descent_silence", "not_signed_coupling_bound_schema_only"], "coupling descent contract"),
    ("SRC2357_12_1016_claim", "1016_claim", ["CG1016_5_coupling_descent_zero", "false"], "coupling descent claim blocked"),
    ("SRC2357_13_1009_contract", "1009_contract", ["PCS1009_2_universal_matter", "conditional_source_input"], "universal matter sector"),
    ("SRC2357_14_1009_claim", "1009_claim", ["CG1009_0_total_parent_action", "false"], "total parent action blocked"),
    ("SRC2357_15_1680_clauses", "1680_clauses", ["CL1680_4", "single_source_current_owner"], "source-current owner clause"),
    ("SRC2357_16_1680_proof", "1680_proof", ["PROOF1680_2_current", "CONDITIONAL_MATH_VALID"], "source-current owner conditional proof"),
    ("SRC2357_17_1620_chain", "1620_chain", ["CR1620_1_zero_lemma", "EXACT_CONDITIONAL_SOURCE_CURRENT_ZERO_LEMMA"], "chain-rule source-current zero"),
    ("SRC2357_18_2351_mhref", "2351_mhref", ["HHS2351_3_MHref", "MISSING_H_TAU_H_REF_MHREF"], "M_H_ref still missing"),
]

OUTPUTS = {
    "sources": OUT / "P8_Y5_PARENT_QLOC_2357_SOURCE_REGISTER.csv",
    "candidate": OUT / "P8_Y5_PARENT_QLOC_2357_MINIMAL_COUPLING_ACTION_CANDIDATE.csv",
    "signing": OUT / "P8_Y5_PARENT_QLOC_2357_ACTION_SIGNING_TESTS.csv",
    "countermodels": OUT / "P8_Y5_PARENT_QLOC_2357_COUNTERMODEL_TESTS.csv",
    "domain_inputs": OUT / "P8_Y5_PARENT_QLOC_2357_DOMAIN_MOTION_INPUT_REQUIREMENTS.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2357_DECISION_LEDGER.csv",
    "claims": OUT / "P8_Y5_PARENT_QLOC_2357_CLAIM_GATES.csv",
    "refusal": OUT / "P8_Y5_PARENT_QLOC_2357_REFUSAL_RUNNER.csv",
    "next": OUT / "P8_Y5_PARENT_QLOC_2357_NEXT_TARGET.csv",
    "copies": OUT / "P8_Y5_PARENT_QLOC_2357_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2357_VALIDATION.csv",
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


def candidate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "MCA2357_0_parent_split",
            "action_piece": "parent matter/geometric split",
            "mathematical_form": "S_parent[Phi,psi]=S_geom[Phi]+sum_A S_A[psi_A;q(Phi),theta_A]+S_boundary[q(Phi)]",
            "role": "candidate coupling grammar, not a promoted total MTS parent action",
            "signing_status": "CANDIDATE_FORM_WRITTEN_NOT_PARENT_DERIVED",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "MCA2357_1_quotient_observed_stack",
            "action_piece": "observed geometry/gauge stack",
            "mathematical_form": "e_obs=E(q(Phi)); g_obs=e_obs^T eta e_obs; A_obs=A(q(Phi)); Omega_obs=Omega(q(Phi)); mu_obs=mu(q(Phi))",
            "role": "routes matter through quotient-owned observed data",
            "signing_status": "CONDITIONAL_IF_Q_OBJECT_AND_STACK_EXIST",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "MCA2357_2_minimal_matter_terms",
            "action_piece": "ordinary matter Lagrangian",
            "mathematical_form": "S_A=int mu_obs(qPhi) L_A(psi_A,D_obs(qPhi)psi_A,e_obs(qPhi),A_obs(qPhi),theta_A)",
            "role": "gives S_matter=Sbar_matter[q(Phi),psi,theta]",
            "signing_status": "CONDITIONALLY_SIGNS_MATTER_DESCENT",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "MCA2357_3_no_source_only_slot",
            "action_piece": "forbidden coupling slots",
            "mathematical_form": "no w_A(X)S_A, no c_A(X)J_A rescaling, no A_A(X)^2g_obs shadow frame, no source/domain/readout marker in L_A before variation",
            "role": "kills source-only species/current/marker countermodels if parent-adopted",
            "signing_status": "CONDITIONALLY_SIGNS_NO_SOURCE_SLOT",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "MCA2357_4_variation_order",
            "action_piece": "variation before readout",
            "mathematical_form": "J_H and T_H are functional derivatives of S_parent before material projection, support fitting, orbital calibration, or arena readout",
            "role": "blocks post-variation selector/source-mask manufacture",
            "signing_status": "CONDITIONALLY_SIGNS_VARIATION_ORDER",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "MCA2357_5_boundary_clause",
            "action_piece": "boundary/support tail",
            "mathematical_form": "delta_v S_boundary is zero, proper, q-owned, or retained as an explicit DMB2356 boundary/support row",
            "role": "prevents bulk descent from hiding finite support flux",
            "signing_status": "PARTIAL_BOUNDARY_CONTRACT_ONLY",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "MCA2357_6_descent_result_if_parent_adopted",
            "action_piece": "conditional theorem output",
            "mathematical_form": "if MCA2357_0..5 and q/v verticality hold, then delta_v S_matter=0 mod Euler/gauge/proper boundary and J_H=q^*Jbar_H",
            "role": "would sign the coupling side of 2356",
            "signing_status": "EXACT_CONDITIONAL_OUTPUT",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "MCA2357_7_current_corpus_verdict",
            "action_piece": "current MTS adoption status",
            "mathematical_form": "no cited source derives MCA2357 as the unique parent matter coupling from MTS core variables",
            "role": "prevents turning a disciplined ansatz into a false theorem",
            "signing_status": "NOT_DERIVED_FROM_CURRENT_MTS_CORE",
            "valid_for_claim": "false",
        },
    ]


def signing_test_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "AST2357_0_PDC2356_0_q_object",
            "tested_clause": "parent q object",
            "candidate_effect": "uses q but does not derive q",
            "test_status": "NOT_SIGNED_BY_ACTION_CANDIDATE",
            "blocks_claim": "q-object remains upstream",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "AST2357_1_PDC2356_1_vertical_generator",
            "tested_clause": "v_X in ker(Dq)",
            "candidate_effect": "if q and v are supplied, descent follows",
            "test_status": "NOT_SIGNED_BY_ACTION_CANDIDATE",
            "blocks_claim": "vertical open-branch proof still missing",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "AST2357_2_PDC2356_2_matter_factorization",
            "tested_clause": "ordinary matter action factors through q",
            "candidate_effect": "MCA2357_2 directly enforces the factorization",
            "test_status": "CONDITIONALLY_SIGNED_BY_CANDIDATE_ONLY",
            "blocks_claim": "candidate is not derived from current MTS core",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "AST2357_3_PDC2356_3_matter_lift",
            "tested_clause": "matter lift is gauge/Euler/boundary",
            "candidate_effect": "requires matter bundle functor and owned lift convention",
            "test_status": "PARTIAL_CONDITIONAL_SIGNING",
            "blocks_claim": "matter bundle/lift not parent-signed",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "AST2357_4_PDC2356_4_constants",
            "tested_clause": "ordinary constants are fixed representation data",
            "candidate_effect": "theta_A appears only as fixed superselection data",
            "test_status": "CONDITIONALLY_SIGNED_BY_CANDIDATE_ONLY",
            "blocks_claim": "superselection theorem not derived from MTS",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "AST2357_5_PDC2356_5_no_source_slot",
            "tested_clause": "no source-only weights/current rescalings/shadow frames",
            "candidate_effect": "MCA2357_3 explicitly excludes them",
            "test_status": "CONDITIONALLY_SIGNED_BY_CANDIDATE_ONLY",
            "blocks_claim": "exclusion is a contract unless parent action uniqueness is proved",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "AST2357_6_PDC2356_6_variation_order",
            "tested_clause": "variation before readout",
            "candidate_effect": "MCA2357_4 defines current extraction before readout",
            "test_status": "CONDITIONALLY_SIGNED_BY_CANDIDATE_ONLY",
            "blocks_claim": "readout/action ordering still needs parent workflow proof",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "AST2357_7_PDC2356_7_boundary",
            "tested_clause": "boundary/support silence",
            "candidate_effect": "MCA2357_5 makes boundary either q-owned/proper or explicit",
            "test_status": "PARTIAL_CONDITIONAL_SIGNING",
            "blocks_claim": "numeric/proper boundary row still missing",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "AST2357_8_PDC2356_8_MHref",
            "tested_clause": "M_H_ref normalization",
            "candidate_effect": "matter coupling action does not derive Hamiltonian reference charge",
            "test_status": "NOT_SIGNED_BY_ACTION_CANDIDATE",
            "blocks_claim": "M_H_ref remains separate parent-charge problem",
            "valid_for_claim": "false",
        },
    ]


def countermodel_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "CMT2357_0_species_weight",
            "countermodel": "S_matter -> sum_A w_A(X) S_A",
            "candidate_response": "forbidden by MCA2357_3",
            "current_status": "EXCLUDED_IF_CANDIDATE_PARENT_ADOPTED_NOT_BY_CURRENT_CORPUS",
            "finite_row_if_not_excluded": "DMB2356_4_J_slot",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CMT2357_1_variable_constants",
            "countermodel": "theta_A(X) carries alpha, mass-ratio, binding, or clock sensitivity",
            "candidate_response": "theta_A fixed as representation/superselection data",
            "current_status": "EXCLUDED_IF_CANDIDATE_PARENT_ADOPTED_NOT_BY_CURRENT_CORPUS",
            "finite_row_if_not_excluded": "DMB2356_3_J_theta",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CMT2357_2_shadow_frame",
            "countermodel": "ordinary matter sees A_A(X)^2 g_obs or disformal/source-only metric",
            "candidate_response": "forbidden by minimal observed-stack coupling",
            "current_status": "EXCLUDED_IF_CANDIDATE_PARENT_ADOPTED_NOT_BY_CURRENT_CORPUS",
            "finite_row_if_not_excluded": "DMB2356_4_J_slot",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CMT2357_3_post_variation_selector",
            "countermodel": "material/readout projection after variation changes source current",
            "candidate_response": "blocked by variation-before-readout clause",
            "current_status": "EXCLUDED_IF_CANDIDATE_PARENT_ADOPTED_NOT_BY_CURRENT_CORPUS",
            "finite_row_if_not_excluded": "DMB2356_4_J_slot;DMB2356_6_I_domain_mask",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CMT2357_4_boundary_domain_marker",
            "countermodel": "support/domain/boundary marker shifts under v_X",
            "candidate_response": "only partially handled by boundary clause; must be q-owned/proper or numeric",
            "current_status": "RETAINED_UNTIL_BOUNDARY_SUPPORT_ROW_EXISTS",
            "finite_row_if_not_excluded": "DMB2356_5_J_boundary;DMB2356_6_I_domain_mask",
            "valid_for_claim": "false",
        },
    ]


def domain_input_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "DIR2357_0_action_adoption_certificate",
            "input_needed": "parent action adoption certificate for MCA2357",
            "required_fields": "source_path; derivation_from_MTS_core; q_definition; sector_list; excluded_slots; variation_order",
            "current_status": "MISSING_PARENT_ADOPTION_CERTIFICATE",
            "feeds": "AST2357_2;AST2357_5;CG2357_0",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DIR2357_1_q_vertical_open_branch",
            "input_needed": "q object and v_X verticality on an open local branch",
            "required_fields": "q_formula; Dq_matrix; vertical_basis; domain; proof_or_numeric_leak_bound",
            "current_status": "MISSING_Q_VERTICALITY_PROOF",
            "feeds": "AST2357_0;AST2357_1;CG2357_1",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DIR2357_2_boundary_support_tail",
            "input_needed": "boundary/support tail zero or numeric row",
            "required_fields": "B_definition; support_annulus; boundary_flux; units; source_path; extraction_method",
            "current_status": "MISSING_BOUNDARY_SUPPORT_INPUT",
            "feeds": "AST2357_7;DMB2356_5;DMB2356_6",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DIR2357_3_MHref",
            "input_needed": "positive same-frame M_H_ref",
            "required_fields": "H_tau; H_ref; tau_frame; coframe; positivity; no_orbital_GM_import; source_path",
            "current_status": "MISSING_H_TAU_H_REF_MHREF",
            "feeds": "AST2357_8;DMB2356_0;CG2357_2",
            "valid_for_claim": "false",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2357_0_result",
            "decision": "do not claim the minimal matter-coupling action as derived current MTS",
            "reason": "it cleanly signs the matter-factorization/no-source-slot route only if adopted as parent action, but no source derives that adoption from MTS core",
            "effect": "source-current descent remains conditional, not a local-GR/Newton claim",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2357_1_progress",
            "decision": "keep MCA2357 as the least-scrutiny coupling contract",
            "reason": "it is standard field-theory minimal coupling through a single observed quotient stack and forbids the dangerous hidden source slots",
            "effect": "the coupling gap is now a concrete parent-action adoption test",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2357_2_remaining_hard_gates",
            "decision": "q/v verticality and M_H_ref remain separate upstream blockers",
            "reason": "the matter coupling action can use q but cannot derive q or the Hamiltonian reference charge by itself",
            "effect": "2358 should attack q/v open-branch proof before returning to numerical domain rows",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2357_3_next",
            "decision": "select q-object/vertical-generator open-branch proof next",
            "reason": "with a candidate matter coupling contract in hand, the cleanest route is now deriving q and v_X in ker(Dq) rather than adding empirical patches",
            "effect": "2358 targets the geometry side of the source-current descent theorem",
            "valid_for_claim": "false",
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2357_0_matter_coupling_derived",
            "claim": "MCA2357 is the derived MTS parent matter-coupling action",
            "passes_public_claim": "false",
            "blocked_by": "DIR2357_0_action_adoption_certificate;AST2357_2_PDC2356_2_matter_factorization",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2357_1_source_current_descent",
            "claim": "J_H=q^*Jbar_H and J_v^matter=0 for current MTS",
            "passes_public_claim": "false",
            "blocked_by": "AST2357_0_PDC2356_0_q_object;AST2357_1_PDC2356_1_vertical_generator;CG2357_0_matter_coupling_derived",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2357_2_domain_motion_bound_score",
            "claim": "domain-motion/source-current bound is score-ready",
            "passes_public_claim": "false",
            "blocked_by": "DIR2357_2_boundary_support_tail;DIR2357_3_MHref",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2357_3_local_GR_Newton",
            "claim": "local GR/Newton reduction follows",
            "passes_public_claim": "false",
            "blocked_by": "q/v verticality;M_H_ref;parent action adoption;boundary support",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2357_4_public_update",
            "claim": "ready for GitHub/public push",
            "passes_public_claim": "false",
            "blocked_by": "private nonclaim checkpoint; parent action not derived",
            "valid_for_claim": "false",
        },
    ]


def refusal_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2357_0_ansatz_as_derivation",
            "temptation": "treat MCA2357 as proved because it is mathematically clean",
            "allowed": "false",
            "why_not": "a clean coupling grammar is not a derivation from MTS core variables",
            "blocking_rows": "MCA2357_7_current_corpus_verdict;CG2357_0_matter_coupling_derived",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2357_1_minimal_coupling_hides_q",
            "temptation": "use minimal coupling to avoid proving q and v_X verticality",
            "allowed": "false",
            "why_not": "MCA2357 uses q; it does not construct q or prove Dq(v)=0",
            "blocking_rows": "AST2357_0_PDC2356_0_q_object;AST2357_1_PDC2356_1_vertical_generator",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2357_2_boundary_sweep",
            "temptation": "ignore boundary/support terms because the bulk action descends",
            "allowed": "false",
            "why_not": "bulk descent does not kill moving support or boundary tail rows",
            "blocking_rows": "MCA2357_5_boundary_clause;DIR2357_2_boundary_support_tail",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2357_3_orbital_normalization",
            "temptation": "use observed GM to normalize the bound",
            "allowed": "false",
            "why_not": "that would smuggle Newton into the proof",
            "blocking_rows": "DIR2357_3_MHref;CG2357_2_domain_motion_bound_score",
            "valid_for_claim": "false",
        },
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2357_0",
            "next_target": "2358-Y5-R2FR-q-object-vertical-generator-open-branch-proof-or-domain-bound.md",
            "why": "MCA2357 gives the clean matter-coupling contract, so the next derivation must prove q and v_X in ker(Dq) on an open local branch",
            "route_type": "derivation_first",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2357_1",
            "next_target": "2358b-Y5-R2FR-parent-action-adoption-certificate-for-MCA2357.md",
            "why": "parallel route: try to source/adopt MCA2357 from MTS core instead of treating it as an external closure",
            "route_type": "parallel_nonclaim",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2357_2",
            "next_target": "2358c-Y5-R2FR-domain-motion-bound-input-pack.md",
            "why": "fallback route: if q/v or action adoption fails, fill DMB2356 component rows and M_H_ref",
            "route_type": "fallback_nonclaim",
            "valid_for_claim": "false",
        },
    ]


def copy_branch_artifacts() -> list[dict[str, Any]]:
    copies = [
        (OUTPUTS["candidate"], BETA_DOCS / "MINIMAL_COUPLING_ACTION_CANDIDATE_2357_NONCLAIM.csv", "beta docs coupling candidate"),
        (OUTPUTS["signing"], MICRO_RESIDUALS / "ACTION_SIGNING_TESTS_2357_NONCLAIM.csv", "microscope signing tests"),
        (OUTPUTS["decision"], RAB_QUEUE / "JR2357_MINIMAL_COUPLING_DECISION_NONCLAIM.csv", "RAB queue decision ledger"),
    ]
    rows = []
    for src, dst, role in copies:
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dst)
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "row_id": f"COPY2357_{len(rows)}",
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
    candidate: list[dict[str, Any]],
    signing: list[dict[str, Any]],
    countermodels: list[dict[str, Any]],
    domain_inputs: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    claims: list[dict[str, Any]],
    refusals: list[dict[str, Any]],
    next_targets: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    created = datetime.now(timezone.utc).isoformat()
    text = f"""# 2357 — Minimal Parent Matter-Coupling Action Or Domain-Motion Input

Created UTC: `{created}`

Branch: `{BRANCH_ID}`

## Result

Result: the **least-handwavy coupling route is now explicit**:

`S_parent[Phi,psi] = S_geom[Phi] + sum_A int mu_obs(qPhi) L_A(psi_A,D_obs(qPhi)psi_A,e_obs(qPhi),A_obs(qPhi),theta_A) + S_boundary[qPhi]`.

This candidate would conditionally sign the matter-factorization, no-source-slot, and variation-before-readout parts of the
2356 source-current descent theorem. But it is **not yet derived from current MTS core variables**, and it does not by itself
prove the parent `q` object, `v_X in ker(Dq)`, boundary/support silence, or `M_H_ref`.

So this is a real sharpening of the coupling gap, not a public/local-GR claim.

## Source Audit

{md_table(sources, ["row_id", "source_key", "exists", "needles_found", "source_role"])}

## Minimal Coupling Action Candidate

{md_table(candidate, ["row_id", "action_piece", "mathematical_form", "role", "signing_status", "valid_for_claim"])}

## Action Signing Tests

{md_table(signing, ["row_id", "tested_clause", "candidate_effect", "test_status", "blocks_claim", "valid_for_claim"])}

## Countermodel Tests

{md_table(countermodels, ["row_id", "countermodel", "candidate_response", "current_status", "finite_row_if_not_excluded", "valid_for_claim"])}

## Domain-Motion Inputs

{md_table(domain_inputs, ["row_id", "input_needed", "required_fields", "current_status", "feeds", "valid_for_claim"])}

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
    for path in FORMALIZATION.rglob("*2357*"):
        if not path.is_file():
            continue
        parts = {part.lower() for part in path.parts}
        if ".venv" in parts or "site-packages" in parts or "__pycache__" in parts:
            continue
        if path.name.startswith(("2357-", "P8_Y5_PARENT_QLOC_2357", "P8_Y5_BRR545_2357")):
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
    candidate_text = read_text(OUTPUTS["candidate"])
    signing = read_csv(OUTPUTS["signing"])
    claims = read_csv(OUTPUTS["claims"])
    next_text = read_text(OUTPUTS["next"])
    checks = [
        ("VAL2357_00_required_sources_exist", all(row["exists"] == "true" for row in sources), "every required source path exists"),
        ("VAL2357_01_required_needles_found", all(row["needles_found"] == "true" for row in sources), "all required source needles were found"),
        ("VAL2357_02_outputs_exist", all(path.exists() and path.stat().st_size > 0 for path in produced), "all 2357 outputs written"),
        ("VAL2357_03_candidate_written", "MCA2357_2_minimal_matter_terms" in candidate_text and "MCA2357_7_current_corpus_verdict" in candidate_text, "minimal parent matter-coupling candidate written with verdict"),
        ("VAL2357_04_not_promoted", "NOT_DERIVED_FROM_CURRENT_MTS_CORE" in candidate_text, "candidate not promoted as current-MTS derivation"),
        ("VAL2357_05_signing_tests_nonclaim", signing and all(row.get("valid_for_claim") == "false" for row in signing), "all signing tests remain nonclaim"),
        ("VAL2357_06_claim_gates_blocked", claims and all(row.get("passes_public_claim") == "false" and row.get("valid_for_claim") == "false" for row in claims), "all public claim gates blocked"),
        ("VAL2357_07_next_selected", "2358-Y5-R2FR-q-object-vertical-generator-open-branch-proof-or-domain-bound.md" in next_text, "2358 q-object/vertical-generator target selected"),
        ("VAL2357_08_branch_copies_parse", copies and all(row["copy_exists"] == "true" for row in copies), "branch copies exist"),
        ("VAL2357_09_formalization_untouched", not formalization_hits(), "no 2357 checkpoint output appears in formalization-workbench"),
        ("VAL2357_10_no_claim_flags", no_true_claim_flags(produced), "no generated row has claim/score-ready/parent-signed true flags"),
        ("VAL2357_11_no_github_policy", True, "public GitHub update not recommended from 2357"),
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
            "row_id": "VAL2357_OVERALL",
            "status": "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL",
            "detail": "2357 writes the minimal parent matter-coupling action candidate, shows it conditionally signs the coupling side but is not derived from current MTS core, and selects q-object/vertical-generator proof as 2358.",
            "valid_for_claim": "false",
        }
    )
    return rows


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)

    sources = source_rows()
    candidate = candidate_rows()
    signing = signing_test_rows()
    countermodels = countermodel_rows()
    domain_inputs = domain_input_rows()
    decisions = decision_rows()
    claims = claim_gate_rows()
    refusals = refusal_rows()
    next_targets = next_rows()

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["candidate"], candidate)
    write_csv(OUTPUTS["signing"], signing)
    write_csv(OUTPUTS["countermodels"], countermodels)
    write_csv(OUTPUTS["domain_inputs"], domain_inputs)
    write_csv(OUTPUTS["decision"], decisions)
    write_csv(OUTPUTS["claims"], claims)
    write_csv(OUTPUTS["refusal"], refusals)
    write_csv(OUTPUTS["next"], next_targets)

    copies = copy_branch_artifacts()
    write_csv(OUTPUTS["copies"], copies)

    validation = validation_rows(sources, copies)
    write_csv(OUTPUTS["validation"], validation)
    write_markdown(sources, candidate, signing, countermodels, domain_inputs, decisions, claims, refusals, next_targets, validation)

    if validation[-1]["status"] != "PASS":
        failed = ", ".join(row["row_id"] for row in validation if row["status"] != "PASS")
        raise SystemExit(f"2357 validation failed: {failed}")
    print(f"2357 checkpoint written: {DOC}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
