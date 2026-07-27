from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BRANCH_ID = "MTS_R2FR_MINIMAL_PARENT_MATTER_COUPLING_2526"
CHECKPOINT_ID = "2526"
DOC = ROOT / "2526-Y5-R2FR-minimal-parent-matter-coupling-action-or-domain-motion-input.md"
MTS_RESIDUALS = ROOT / "source-intake" / "mts_residuals"

OUTPUTS = {
    "source_register": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2526_SOURCE_REGISTER.csv",
    "coupling_candidate": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2526_MINIMAL_COUPLING_ACTION_CANDIDATE.csv",
    "action_signing_tests": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2526_ACTION_SIGNING_TESTS.csv",
    "countermodel_tests": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2526_COUNTERMODEL_TESTS.csv",
    "domain_input_requirements": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2526_DOMAIN_INPUT_REQUIREMENTS.csv",
    "claim_gates": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2526_CLAIM_GATES.csv",
    "dryrun_results": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2526_DRYRUN_RESULTS.csv",
    "decision_ledger": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2526_DECISION_LEDGER.csv",
    "next_target": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2526_NEXT_TARGET.csv",
    "branch_copies": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2526_BRANCH_COPIES.csv",
    "validation": MTS_RESIDUALS / "P8_Y5_BRR545_2526_VALIDATION.csv",
}

BRANCH_COPIES = {
    "coupling_candidate": ROOT
    / "source-intake"
    / "local_bounds"
    / "Minimal_parent_matter_coupling_candidate_2526_NONCLAIM.csv",
    "action_signing_tests": ROOT
    / "source-intake"
    / "beta-source"
    / "docs"
    / "Matter_coupling_action_signing_tests_2526_NONCLAIM.csv",
    "domain_input_requirements": ROOT
    / "source-intake"
    / "rab-sector"
    / "acquisition-queue"
    / "JR2526_DOMAIN_INPUT_REQUIREMENTS_NONCLAIM.csv",
    "next_target": ROOT
    / "source-intake"
    / "rab-sector"
    / "acquisition-queue"
    / "JR2526_NEXT_TARGET_NONCLAIM.csv",
}

SOURCE_SPECS = [
    {
        "source_id": "SRC2526_0_2525_next",
        "path": "source-intake/mts_residuals/P8_Y5_NO_SHADOW_2525_NEXT_TARGET.csv",
        "needles": ["NEXT2525_0_selected", "minimal parent matter-coupling action"],
        "role": "authoritative 2525 handoff to matter-coupling action gate",
    },
    {
        "source_id": "SRC2526_1_2525_validation",
        "path": "source-intake/mts_residuals/P8_Y5_BRR545_2525_VALIDATION.csv",
        "needles": ["VAL2525_OVERALL", "PASS"],
        "role": "previous checkpoint validation gate",
    },
    {
        "source_id": "SRC2526_2_2525_jdomain_rows",
        "path": "source-intake/mts_residuals/P8_Y5_NO_SHADOW_2525_JDOMAIN_BOUND_ROWS.csv",
        "needles": ["JDOM2525_1_current_descent", "MISSING_SOURCE_CURRENT_DESCENT_PROOF_OR_BOUND"],
        "role": "current source-current descent gap feeding domain rows",
    },
    {
        "source_id": "SRC2526_3_2357_doc",
        "path": "2357-Y5-R2FR-minimal-parent-matter-coupling-action-or-domain-motion-input.md",
        "needles": ["MCA2357_7_current_corpus_verdict", "NOT_DERIVED_FROM_CURRENT_MTS_CORE"],
        "role": "prior minimal parent matter-coupling candidate and verdict",
    },
    {
        "source_id": "SRC2526_4_2357_validation",
        "path": "source-intake/mts_residuals/P8_Y5_BRR545_2357_VALIDATION.csv",
        "needles": ["VAL2357_OVERALL", "PASS"],
        "role": "prior candidate validation gate",
    },
    {
        "source_id": "SRC2526_5_2357_candidate",
        "path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2357_MINIMAL_COUPLING_ACTION_CANDIDATE.csv",
        "needles": ["MCA2357_2_minimal_matter_terms", "CONDITIONALLY_SIGNS_MATTER_DESCENT"],
        "role": "machine-readable candidate action",
    },
    {
        "source_id": "SRC2526_6_2357_signing_tests",
        "path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2357_ACTION_SIGNING_TESTS.csv",
        "needles": ["AST2357_0_PDC2356_0_q_object", "NOT_SIGNED_BY_ACTION_CANDIDATE"],
        "role": "candidate signing-test matrix",
    },
    {
        "source_id": "SRC2526_7_2357_countermodels",
        "path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2357_COUNTERMODEL_TESTS.csv",
        "needles": ["CMT2357_0_species_weight", "EXCLUDED_IF_CANDIDATE_PARENT_ADOPTED_NOT_BY_CURRENT_CORPUS"],
        "role": "countermodels excluded only if candidate is parent-adopted",
    },
    {
        "source_id": "SRC2526_8_2357_inputs",
        "path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2357_DOMAIN_MOTION_INPUT_REQUIREMENTS.csv",
        "needles": ["DIR2357_0_action_adoption_certificate", "MISSING_PARENT_ADOPTION_CERTIFICATE"],
        "role": "remaining adoption and finite-input requirements",
    },
    {
        "source_id": "SRC2526_9_1088_signature",
        "path": "source-intake/mts_residuals/P8_Y5_R10_1088_MINIMAL_SIGNATURE_CLAUSE.csv",
        "needles": ["MOMS1088_0_action_form", "CONDITIONAL_CLAUSE_WRITTEN_NOT_PARENT_DERIVED"],
        "role": "older minimal ordinary matter signature clause",
    },
    {
        "source_id": "SRC2526_10_1088_theorem",
        "path": "source-intake/mts_residuals/P8_Y5_R10_1088_CONDITIONAL_ZERO_THEOREM.csv",
        "needles": ["THM1088_5_conclusion", "ZERO_THEOREM_PROVED_UNDER_MOMS1088_SIGNATURE"],
        "role": "conditional matter-current zero theorem",
    },
    {
        "source_id": "SRC2526_11_2508_no_slot",
        "path": "source-intake/mts_residuals/P8_Y5_NO_SHADOW_2508_NO_SOURCE_SLOT_THEOREM_GATES.csv",
        "needles": ["GATE2508_6_theorem", "CLAIM_BLOCKED"],
        "role": "no-source-only-slot theorem remains not parent-derived",
    },
    {
        "source_id": "SRC2526_12_2486_matter_descent",
        "path": "source-intake/mts_residuals/P8_Y5_FIELD_QUOTIENT_2486_MATTER_DESCENT_GATE.csv",
        "needles": ["MD2486_0_chain_rule", "EXACT_CONDITIONAL"],
        "role": "quotient matter descent is exact only after q/readout clauses close",
    },
]


def timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base_row(**kwargs: Any) -> dict[str, Any]:
    row: dict[str, Any] = {
        "timestamp_utc": timestamp(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
        "claim_allowed": False,
    }
    row.update(kwargs)
    return row


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except FileNotFoundError:
        return ""


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def csv_rows_parse(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        return bool(rows), len(rows), "OK"
    except Exception as exc:
        return False, 0, f"{type(exc).__name__}: {exc}"


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        cells: list[str] = []
        for column in columns:
            value = str(row.get(column, "")).replace("\n", "<br>").replace("|", "\\|")
            cells.append(value)
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for spec in SOURCE_SPECS:
        path = ROOT / spec["path"]
        text = read_text(path)
        found_needles = [needle for needle in spec["needles"] if needle in text]
        rows.append(
            base_row(
                source_id=spec["source_id"],
                source_path=spec["path"],
                path_exists=path.exists(),
                required_needles=";".join(spec["needles"]),
                found_needles=";".join(found_needles),
                role=spec["role"],
                source_pass=path.exists() and len(found_needles) == len(spec["needles"]),
            )
        )
    return rows


def coupling_candidate_rows() -> list[dict[str, Any]]:
    entries = [
        {
            "row_id": "MCA2526_0_parent_split",
            "action_piece": "parent matter/geometric split",
            "mathematical_form": "S_parent[Phi,psi]=S_geom[Phi]+sum_A S_A[psi_A;q(Phi),theta_A]+S_boundary[q(Phi)]",
            "role": "candidate coupling grammar, not a promoted total MTS parent action",
            "signing_status": "CANDIDATE_FORM_WRITTEN_NOT_PARENT_DERIVED",
            "blocks": "parent action adoption certificate missing",
        },
        {
            "row_id": "MCA2526_1_observed_stack",
            "action_piece": "single observed quotient stack",
            "mathematical_form": "e_obs=E(q(Phi)); g_obs=e_obs^T eta e_obs; A_obs=A(q(Phi)); Omega_obs=Omega(q(Phi)); mu_obs=mu(q(Phi))",
            "role": "routes ordinary matter through quotient-owned public data",
            "signing_status": "CONDITIONAL_IF_Q_OBJECT_AND_STACK_EXIST",
            "blocks": "q object and q-basic readout functor remain unsigned",
        },
        {
            "row_id": "MCA2526_2_minimal_matter_terms",
            "action_piece": "ordinary matter Lagrangian",
            "mathematical_form": "S_A=int mu_obs(qPhi) L_A(psi_A,D_obs(qPhi)psi_A,e_obs(qPhi),A_obs(qPhi),theta_A)",
            "role": "gives S_matter=Sbar_matter[q(Phi),psi,theta] and conditionally signs matter descent",
            "signing_status": "CONDITIONALLY_SIGNS_MATTER_DESCENT",
            "blocks": "candidate not derived from current MTS core",
        },
        {
            "row_id": "MCA2526_3_no_source_only_slot",
            "action_piece": "forbidden source-only couplings",
            "mathematical_form": "no w_A(X)S_A, no c_A(X)J_A rescaling, no A_A(X)^2 g_obs shadow frame, no source/domain/readout marker in L_A before variation",
            "role": "kills source-only species/current/marker countermodels if parent-adopted",
            "signing_status": "CONDITIONALLY_SIGNS_NO_SOURCE_SLOT",
            "blocks": "object-language uniqueness and no-Hom proof not derived",
        },
        {
            "row_id": "MCA2526_4_variation_order",
            "action_piece": "variation before readout",
            "mathematical_form": "T_H and J_H are functional derivatives of S_parent before material projection, support fitting, orbital calibration, or arena readout",
            "role": "blocks post-variation selector/source-mask manufacture",
            "signing_status": "CONDITIONALLY_SIGNS_VARIATION_ORDER",
            "blocks": "parent workflow/readout-order proof still needed",
        },
        {
            "row_id": "MCA2526_5_boundary_clause",
            "action_piece": "boundary/support tail",
            "mathematical_form": "delta_v S_boundary is zero, proper, q-owned, or retained as an explicit E_boundary/domain row",
            "role": "prevents bulk descent from hiding finite support flux",
            "signing_status": "PARTIAL_BOUNDARY_CONTRACT_ONLY",
            "blocks": "boundary/support tail zero or numeric row missing",
        },
        {
            "row_id": "MCA2526_6_descent_output",
            "action_piece": "conditional theorem output",
            "mathematical_form": "if MCA2526_0..5 plus q/v verticality hold, then delta_v S_matter=0 modulo Euler/gauge/proper boundary and J_H=q^*Jbar_H",
            "role": "signs the coupling side of 2525 source-current descent",
            "signing_status": "EXACT_CONDITIONAL_OUTPUT",
            "blocks": "antecedents not current-MTS proof",
        },
        {
            "row_id": "MCA2526_7_current_verdict",
            "action_piece": "current MTS adoption status",
            "mathematical_form": "no cited source derives MCA2526 as the unique parent matter coupling from MTS core variables",
            "role": "prevents turning a disciplined ansatz into a false theorem",
            "signing_status": "NOT_DERIVED_FROM_CURRENT_MTS_CORE",
            "blocks": "local-GR/Newton source-current descent remains conditional",
        },
    ]
    return [base_row(**entry) for entry in entries]


def action_signing_test_rows() -> list[dict[str, Any]]:
    entries = [
        ("AST2526_0_q_object", "parent q object", "uses q but does not derive q", "NOT_SIGNED_BY_ACTION_CANDIDATE", "q-object remains upstream"),
        ("AST2526_1_vertical_generator", "v_X in ker(Dq)", "if q and v are supplied, descent follows", "NOT_SIGNED_BY_ACTION_CANDIDATE", "vertical open-branch proof still missing"),
        ("AST2526_2_matter_factorization", "ordinary matter action factors through q", "MCA2526_2 enforces factorization", "CONDITIONALLY_SIGNED_BY_CANDIDATE_ONLY", "candidate is not derived from MTS core"),
        ("AST2526_3_matter_lift", "matter lift is gauge/Euler/boundary", "requires matter bundle functor and owned lift convention", "PARTIAL_CONDITIONAL_SIGNING", "matter bundle/lift not parent-signed"),
        ("AST2526_4_constants", "ordinary constants fixed as representation/superselection data", "theta_A is fixed data in the candidate", "CONDITIONALLY_SIGNED_BY_CANDIDATE_ONLY", "constant superselection not derived from MTS"),
        ("AST2526_5_no_source_slot", "no source-only weights/current rescalings/shadow frames", "MCA2526_3 explicitly excludes them", "CONDITIONALLY_SIGNED_BY_CANDIDATE_ONLY", "exclusion is a contract unless parent uniqueness is proved"),
        ("AST2526_6_variation_order", "variation before readout", "MCA2526_4 extracts current before readout", "CONDITIONALLY_SIGNED_BY_CANDIDATE_ONLY", "parent workflow proof still needed"),
        ("AST2526_7_boundary_support", "boundary/support silence", "MCA2526_5 makes boundary q-owned/proper or explicit", "PARTIAL_CONDITIONAL_SIGNING", "boundary/support numeric row or theorem missing"),
        ("AST2526_8_MHref", "M_H_ref normalization", "matter coupling action does not derive Hamiltonian reference charge", "NOT_SIGNED_BY_ACTION_CANDIDATE", "M_H_ref remains separate parent-charge problem"),
        ("AST2526_9_adoption", "MCA2526 derived from MTS core", "candidate is clean but not sourced as unique MTS parent action", "NOT_SIGNED_BY_CURRENT_CORPUS", "adoption certificate missing"),
    ]
    return [
        base_row(
            row_id=row_id,
            tested_clause=tested_clause,
            candidate_effect=candidate_effect,
            test_status=test_status,
            blocks_claim=blocks_claim,
            test_pass=False,
        )
        for row_id, tested_clause, candidate_effect, test_status, blocks_claim in entries
    ]


def countermodel_test_rows() -> list[dict[str, Any]]:
    entries = [
        {
            "row_id": "CMT2526_0_species_weight",
            "countermodel": "S_matter -> sum_A w_A(X) S_A",
            "candidate_response": "forbidden by no-source-only slot",
            "current_status": "EXCLUDED_IF_CANDIDATE_PARENT_ADOPTED_NOT_BY_CURRENT_CORPUS",
            "finite_row_if_not_excluded": "J_source_only_slot",
        },
        {
            "row_id": "CMT2526_1_variable_constants",
            "countermodel": "theta_A(X) carries alpha, mass-ratio, binding or clock sensitivity",
            "candidate_response": "theta_A fixed as representation/superselection data",
            "current_status": "EXCLUDED_IF_CANDIDATE_PARENT_ADOPTED_NOT_BY_CURRENT_CORPUS",
            "finite_row_if_not_excluded": "J_theta",
        },
        {
            "row_id": "CMT2526_2_shadow_frame",
            "countermodel": "ordinary matter sees A_A(X)^2 g_obs or disformal/source-only metric",
            "candidate_response": "forbidden by single observed-stack coupling",
            "current_status": "EXCLUDED_IF_CANDIDATE_PARENT_ADOPTED_NOT_BY_CURRENT_CORPUS",
            "finite_row_if_not_excluded": "J_source_only_slot;J_frame",
        },
        {
            "row_id": "CMT2526_3_post_variation_selector",
            "countermodel": "material/readout projection after variation changes source current",
            "candidate_response": "blocked by variation-before-readout clause",
            "current_status": "EXCLUDED_IF_CANDIDATE_PARENT_ADOPTED_NOT_BY_CURRENT_CORPUS",
            "finite_row_if_not_excluded": "J_readout_selector;I_domain_mask",
        },
        {
            "row_id": "CMT2526_4_boundary_domain_marker",
            "countermodel": "support/domain/boundary marker shifts under v_X",
            "candidate_response": "only partially handled; boundary must be q-owned/proper or numeric",
            "current_status": "RETAINED_UNTIL_BOUNDARY_SUPPORT_ROW_EXISTS",
            "finite_row_if_not_excluded": "J_boundary_support;I_domain_mask",
        },
        {
            "row_id": "CMT2526_5_q_missing",
            "countermodel": "candidate uses a q map that is not parent-derived",
            "candidate_response": "not addressed by matter coupling alone",
            "current_status": "RETAINED_AS_NEXT_GEOMETRY_GATE",
            "finite_row_if_not_excluded": "Dq_vertical_leak;J_vertical_physical",
        },
    ]
    return [base_row(**entry, countermodel_passed=False) for entry in entries]


def domain_input_requirement_rows() -> list[dict[str, Any]]:
    entries = [
        ("DIR2526_0_action_adoption_certificate", "parent action adoption certificate for MCA2526", "source_path; derivation_from_MTS_core; q_definition; sector_list; excluded_slots; variation_order", "MISSING_PARENT_ADOPTION_CERTIFICATE", "AST2526_2;AST2526_5;CG2526_0"),
        ("DIR2526_1_q_vertical_open_branch", "q object and v_X verticality on an open local branch", "q_formula; Dq_matrix; vertical_basis; domain; proof_or_numeric_leak_bound", "MISSING_Q_VERTICALITY_PROOF", "AST2526_0;AST2526_1;CG2526_1"),
        ("DIR2526_2_boundary_support_tail", "boundary/support tail zero or numeric row", "B_definition; support_annulus; boundary_flux; units; source_path; extraction_method", "MISSING_BOUNDARY_SUPPORT_INPUT", "AST2526_7;JDOM2525_4;JDOM2525_5"),
        ("DIR2526_3_MHref", "positive same-frame M_H_ref", "H_tau;H_ref;tau_frame;coframe;positivity;no_orbital_GM_import;source_path", "MISSING_H_TAU_H_REF_MHREF", "AST2526_8;JDOM2525_0;CG2526_2"),
        ("DIR2526_4_domain_motion_values", "finite domain-motion numerator values if theorem route fails", "E_current_descent;E_support_motion;E_domain_mask;E_boundary_crossing;units;source_paths", "MISSING_DOMAIN_MOTION_VALUES", "JDOM2525 rows;fallback runner"),
    ]
    return [
        base_row(
            row_id=row_id,
            input_needed=input_needed,
            required_fields=required_fields,
            current_status=current_status,
            feeds=feeds,
            score_ready=False,
        )
        for row_id, input_needed, required_fields, current_status, feeds in entries
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    entries = [
        ("CG2526_0_matter_coupling_derived", "MCA2526 is the derived MTS parent matter-coupling action", "DIR2526_0_action_adoption_certificate;AST2526_9_adoption"),
        ("CG2526_1_source_current_descent", "J_H=q^*Jbar_H and J_v^matter=0 for current MTS", "AST2526_0_q_object;AST2526_1_vertical_generator;CG2526_0_matter_coupling_derived"),
        ("CG2526_2_domain_motion_bound_score", "domain-motion/source-current bound is score-ready", "DIR2526_2_boundary_support_tail;DIR2526_3_MHref;DIR2526_4_domain_motion_values"),
        ("CG2526_3_local_GR_Newton", "local GR/Newton source-current reduction follows", "q/v verticality;M_H_ref;parent action adoption;boundary support"),
        ("CG2526_4_public_update", "ready for GitHub/public push", "private nonclaim checkpoint; parent action not derived"),
    ]
    return [
        base_row(
            row_id=row_id,
            claim=claim,
            passes_public_claim=False,
            blocked_by=blocked_by,
        )
        for row_id, claim, blocked_by in entries
    ]


def dryrun_rows() -> list[dict[str, Any]]:
    entries = [
        ("DRY2526_0_ansatz_as_derivation", "treat MCA2526 as proved because it is mathematically clean", "parent action adoption certificate from MTS core", "REJECT", "ANSATZ_NOT_DERIVATION"),
        ("DRY2526_1_minimal_coupling_hides_q", "use minimal coupling to avoid proving q and v_X verticality", "q object and open-branch vertical generator proof", "REJECT", "Q_VERTICALITY_UPSTREAM"),
        ("DRY2526_2_no_source_slot_by_decree", "claim no-source-slot because candidate forbids it", "parent object-language/no-Hom/constructor exhaustion proof", "REJECT", "CONTRACT_NOT_PARENT_UNIQUENESS"),
        ("DRY2526_3_boundary_sweep", "ignore boundary/support terms because bulk action descends", "boundary/support zero or numeric row", "REJECT", "BOUNDARY_SUPPORT_RETAINED"),
        ("DRY2526_4_observed_GM_normalization", "use observed orbital GM to normalize domain rows", "parent M_H_ref and tau/coframe lock", "REJECT", "ORBITAL_GM_LAUNDERING"),
        ("DRY2526_5_future_complete_action", "future parent action certificate plus q/v proof and boundary/MHref inputs", "none in schema; evidence remains future", "WOULD_ACCEPT_SCHEMA_IF_REAL_FILES_AND_VALUES_EXIST", "FUTURE_EVIDENCE_ONLY"),
    ]
    return [
        base_row(
            case_id=case_id,
            case_description=case_description,
            missing_requirements=missing_requirements,
            result_status=result_status,
            blocking_markers=blocking_markers,
            pass_fail="BLOCKED_NONCLAIM" if result_status == "REJECT" else "TEMPLATE_NONCLAIM",
            claim_pass=False,
        )
        for case_id, case_description, missing_requirements, result_status, blocking_markers in entries
    ]


def decision_rows() -> list[dict[str, Any]]:
    entries = [
        {
            "decision_id": "DEC2526_0_contract_status",
            "decision": "retain MCA2526 as least-scrutiny coupling contract",
            "rationale": "it is standard single observed-stack minimal coupling and explicitly forbids the dangerous source-only slots",
            "next_action": "use it as a contract, not as a theorem",
            "status": "ACTIVE",
        },
        {
            "decision_id": "DEC2526_1_no_promotion",
            "decision": "do not claim MCA2526 is derived MTS",
            "rationale": "no source derives it uniquely from current MTS core variables, q construction, or object-language exhaustion",
            "next_action": "keep action adoption certificate as missing input",
            "status": "ACTIVE",
        },
        {
            "decision_id": "DEC2526_2_next",
            "decision": "select q-object/vertical-generator open-branch proof next",
            "rationale": "the matter action can use q but cannot derive q or prove v_X in ker(Dq); this is now the clean upstream geometry gate",
            "next_action": "attempt open-branch q/Dq/v_X certificate or retain Dq_vertical_leak rows",
            "status": "ACTIVE",
        },
        {
            "decision_id": "DEC2526_3_queue",
            "decision": "keep finite domain inputs and fibre route queued",
            "rationale": "if q/v or action adoption fails, domain-motion inputs become the empirical fallback; fibre B_h remains independent",
            "next_action": "queue domain input pack and fibre re-entry after q/v proof",
            "status": "ACTIVE",
        },
    ]
    return [base_row(**entry) for entry in entries]


def next_target_rows() -> list[dict[str, Any]]:
    entries = [
        {
            "route_id": "NEXT2526_0_selected",
            "selection_status": "selected",
            "target_file": "2527-Y5-R2FR-q-object-vertical-generator-open-branch-proof-or-domain-bound.md",
            "target_script": "scripts/Y5_R2FR_q_object_vertical_generator_open_branch_proof_or_domain_bound_2527.py",
            "objective": "prove q and v_X in ker(Dq) on an open local branch for the source-current descent theorem, or stage finite Dq_vertical_leak/domain rows",
            "success_condition": "q object, Dq matrix, vertical basis and open-branch domain are parent-signed, or Dq_vertical_leak remains explicit nonclaim input",
            "do_not_do": "do not let the matter-coupling contract hide q; do not prove verticality only at one point; do not claim Newton/local GR",
        },
        {
            "route_id": "NEXT2526_1_parallel_adoption",
            "selection_status": "held_parallel",
            "target_file": "2527b-Y5-R2FR-parent-action-adoption-certificate-for-MCA2526.md",
            "target_script": "scripts/Y5_R2FR_parent_action_adoption_certificate_for_MCA2526_2527b.py",
            "objective": "try to source/adopt MCA2526 from MTS core rather than treating it as external closure",
            "success_condition": "source path and derivation from MTS core sign q stack, sector list, excluded slots and variation order, otherwise nonclaim",
            "do_not_do": "do not adopt by taste or because it is standard GR minimal coupling",
        },
        {
            "route_id": "NEXT2526_2_fibre_queue",
            "selection_status": "queued_after_q_verticality",
            "target_file": "2528-Y5-R2FR-fibre-Bh-finite-row-or-hidden-visible-grammar-reentry.md",
            "target_script": "scripts/Y5_R2FR_fibre_Bh_finite_row_or_hidden_visible_grammar_reentry_2528.py",
            "objective": "classify fibre B_h with hidden-visible grammar reentry or finite fibre coefficient rows after q/source-current lane is narrowed",
            "success_condition": "B_h has theorem-zero evidence or finite nonclaim Z_h/M2_h/B_h/C_h/source-charge rows",
            "do_not_do": "do not let matter-coupling closure erase independent fibre residuals",
        },
    ]
    return [base_row(**entry) for entry in entries]


def branch_copy_rows() -> list[dict[str, Any]]:
    source_map = {
        "coupling_candidate": OUTPUTS["coupling_candidate"],
        "action_signing_tests": OUTPUTS["action_signing_tests"],
        "domain_input_requirements": OUTPUTS["domain_input_requirements"],
        "next_target": OUTPUTS["next_target"],
    }
    rows: list[dict[str, Any]] = []
    for key, destination in BRANCH_COPIES.items():
        source = source_map[key]
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
        parse_ok, row_count, parse_message = csv_rows_parse(destination)
        rows.append(
            base_row(
                copy_id=f"COPY2526_{key}",
                source_path=str(source.relative_to(ROOT)),
                destination_path=str(destination.relative_to(ROOT)),
                copied=destination.exists(),
                parse_ok=parse_ok,
                row_count=row_count,
                parse_message=parse_message,
                status="NONCLAIM_BRANCH_COPY",
            )
        )
    return rows


def falsey(value: Any) -> bool:
    return str(value).strip().lower() in {"false", "0", "no", "not_computed", ""}


def no_claim_flags(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    for name, rows in rows_by_name.items():
        if name in {"source_register", "validation"}:
            continue
        for row in rows:
            for key in (
                "valid_for_claim",
                "claim_allowed",
                "score_ready",
                "valid_prediction_row",
                "accepted_for_scoring",
                "claim_pass",
                "test_pass",
                "countermodel_passed",
                "passes_public_claim",
            ):
                if key in row and not falsey(row[key]):
                    return False
    return True


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []

    def add(check_id: str, status: bool, detail: str = "") -> None:
        checks.append(
            base_row(
                check_id=check_id,
                status="PASS" if status else "FAIL",
                detail=detail,
                valid_for_claim=False,
                claim_allowed=False,
            )
        )

    source_rows = rows_by_name["source_register"]
    candidate_rows = rows_by_name["coupling_candidate"]
    signing_rows = rows_by_name["action_signing_tests"]

    add("VAL2526_00_sources_exist", all(str(row["path_exists"]) == "True" for row in source_rows))
    add("VAL2526_01_source_needles", all(str(row["source_pass"]) == "True" for row in source_rows))
    add(
        "VAL2526_02_candidate_written",
        any(row["row_id"] == "MCA2526_2_minimal_matter_terms" for row in candidate_rows)
        and any(row["row_id"] == "MCA2526_7_current_verdict" for row in candidate_rows),
        "minimal matter-coupling candidate and current-corpus verdict are written",
    )
    add(
        "VAL2526_03_candidate_not_promoted",
        any(
            row["row_id"] == "MCA2526_7_current_verdict"
            and row["signing_status"] == "NOT_DERIVED_FROM_CURRENT_MTS_CORE"
            for row in candidate_rows
        ),
        "candidate remains a contract, not a derived MTS theorem",
    )
    add(
        "VAL2526_04_signing_tests_cover_upstream",
        all(
            any(row["row_id"] == required for row in signing_rows)
            for required in [
                "AST2526_0_q_object",
                "AST2526_1_vertical_generator",
                "AST2526_2_matter_factorization",
                "AST2526_5_no_source_slot",
                "AST2526_8_MHref",
                "AST2526_9_adoption",
            ]
        ),
        "signing tests cover q, verticality, matter factorization, no-source slot, MHref and adoption",
    )
    add(
        "VAL2526_05_countermodels_retained",
        len(rows_by_name["countermodel_tests"]) == 6
        and all(str(row["countermodel_passed"]) == "False" for row in rows_by_name["countermodel_tests"]),
        "countermodels remain nonclaim unless parent adoption closes",
    )
    add(
        "VAL2526_06_inputs_listed",
        all(
            any(row["row_id"] == required for row in rows_by_name["domain_input_requirements"])
            for required in [
                "DIR2526_0_action_adoption_certificate",
                "DIR2526_1_q_vertical_open_branch",
                "DIR2526_2_boundary_support_tail",
                "DIR2526_3_MHref",
            ]
        ),
        "adoption, q/verticality, boundary/support and MHref inputs are explicit",
    )
    add(
        "VAL2526_07_claim_gates_blocked",
        all(str(row["passes_public_claim"]) == "False" for row in rows_by_name["claim_gates"]),
        "all public/local-GR claim gates are blocked",
    )
    add(
        "VAL2526_08_dryruns_block_bad_rows",
        all(str(row["claim_pass"]) == "False" for row in rows_by_name["dryrun_results"])
        and all(
            str(row["result_status"]) in {"REJECT", "WOULD_ACCEPT_SCHEMA_IF_REAL_FILES_AND_VALUES_EXIST"}
            for row in rows_by_name["dryrun_results"]
        ),
        "ansatz-as-proof, hidden-q, no-slot-by-decree, boundary sweep and observed-GM rows do not score",
    )
    add(
        "VAL2526_09_next_target_q_verticality",
        any(
            row["route_id"] == "NEXT2526_0_selected"
            and "q-object-vertical-generator" in row["target_file"]
            for row in rows_by_name["next_target"]
        ),
        "q-object/vertical-generator proof selected next",
    )
    add("VAL2526_10_no_claim_flags", no_claim_flags(rows_by_name))
    add(
        "VAL2526_11_branch_copies",
        all(
            str(row["copied"]) == "True" and str(row["parse_ok"]) == "True"
            for row in rows_by_name["branch_copies"]
        ),
    )
    formalization = ROOT.parent / "formalization-workbench"
    formalization_hits = [
        path
        for path in formalization.rglob("*2526*")
        if ".venv" not in path.parts and "site-packages" not in path.parts
    ] if formalization.exists() else []
    add(
        "VAL2526_12_no_formalization_artifacts",
        len(formalization_hits) == 0,
        ";".join(str(path) for path in formalization_hits),
    )
    add("VAL2526_13_pycache_absent", not (Path(__file__).resolve().parent / "__pycache__").exists())

    for name, path in OUTPUTS.items():
        if name == "validation":
            continue
        parse_ok, row_count, parse_message = csv_rows_parse(path)
        add(f"VAL2526_CSV_{path.stem}", parse_ok, f"{parse_message}; rows={row_count}")
    for key, path in BRANCH_COPIES.items():
        parse_ok, row_count, parse_message = csv_rows_parse(path)
        add(f"VAL2526_COPY_CSV_{key}", parse_ok, f"{parse_message}; rows={row_count}")

    overall = all(row["status"] == "PASS" for row in checks)
    checks.append(
        base_row(
            check_id="VAL2526_OVERALL",
            status="PASS" if overall else "FAIL",
            detail="2526 writes the minimal parent matter-coupling contract, shows it conditionally signs the coupling side but is not derived from current MTS core, and selects q-object/vertical-generator proof next.",
            valid_for_claim=False,
            claim_allowed=False,
        )
    )
    return checks


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    DOC.write_text(
        "\n".join(
            [
                "# 2526 - Minimal Parent Matter-Coupling Action or Domain-Motion Input",
                "",
                "**Current verdict:** the least-handwavy matter coupling contract is now explicit: ordinary matter sees one quotient-owned observed stack, with no source-only weights, shadow frames, or post-readout source selectors. This would conditionally sign the coupling side of source-current descent, but current MTS does not derive this action uniquely from core variables.",
                "",
                "**Main gain:** the coupling gap is no longer vague. The candidate signs matter factorization, no-source-slot, and variation-order only as a conditional parent-action contract. It does not sign `q`, `v_X in ker(Dq)`, `M_H_ref`, or boundary/support silence.",
                "",
                "**Claim discipline:** no Newton, local-GR, PPN, WEP, R10, clock, orbit, source-current, worldtube, `J_PiM`, `Q_mem`, or GitHub/public claim is made.",
                "",
                "## Source Register",
                md_table(rows_by_name["source_register"], ["source_id", "source_path", "path_exists", "found_needles", "source_pass", "role"]),
                "",
                "## Coupling Candidate",
                md_table(rows_by_name["coupling_candidate"], ["row_id", "action_piece", "mathematical_form", "role", "signing_status", "blocks"]),
                "",
                "## Action Signing Tests",
                md_table(rows_by_name["action_signing_tests"], ["row_id", "tested_clause", "candidate_effect", "test_status", "blocks_claim", "test_pass"]),
                "",
                "## Countermodel Tests",
                md_table(rows_by_name["countermodel_tests"], ["row_id", "countermodel", "candidate_response", "current_status", "finite_row_if_not_excluded", "countermodel_passed"]),
                "",
                "## Domain Input Requirements",
                md_table(rows_by_name["domain_input_requirements"], ["row_id", "input_needed", "required_fields", "current_status", "feeds", "score_ready"]),
                "",
                "## Claim Gates",
                md_table(rows_by_name["claim_gates"], ["row_id", "claim", "passes_public_claim", "blocked_by"]),
                "",
                "## Dry Run",
                md_table(rows_by_name["dryrun_results"], ["case_id", "case_description", "missing_requirements", "result_status", "blocking_markers", "pass_fail"]),
                "",
                "## Decision Ledger",
                md_table(rows_by_name["decision_ledger"], ["decision_id", "decision", "rationale", "next_action", "status"]),
                "",
                "## Next Target",
                md_table(rows_by_name["next_target"], ["route_id", "selection_status", "target_file", "target_script", "objective", "success_condition", "do_not_do"]),
                "",
                "## Validation",
                md_table(rows_by_name["validation"], ["check_id", "status", "detail"]),
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> None:
    remove_pycache()
    rows_by_name: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register_rows(),
        "coupling_candidate": coupling_candidate_rows(),
        "action_signing_tests": action_signing_test_rows(),
        "countermodel_tests": countermodel_test_rows(),
        "domain_input_requirements": domain_input_requirement_rows(),
        "claim_gates": claim_gate_rows(),
        "dryrun_results": dryrun_rows(),
        "decision_ledger": decision_rows(),
        "next_target": next_target_rows(),
    }

    for name, rows in rows_by_name.items():
        write_csv(OUTPUTS[name], rows)

    rows_by_name["branch_copies"] = branch_copy_rows()
    write_csv(OUTPUTS["branch_copies"], rows_by_name["branch_copies"])

    rows_by_name["validation"] = validation_rows(rows_by_name)
    write_csv(OUTPUTS["validation"], rows_by_name["validation"])
    write_doc(rows_by_name)
    remove_pycache()

    print(f"wrote {DOC}")
    for name, path in OUTPUTS.items():
        print(f"wrote {name}: {path}")
    for key, path in BRANCH_COPIES.items():
        print(f"copied {key}: {path}")


if __name__ == "__main__":
    main()
