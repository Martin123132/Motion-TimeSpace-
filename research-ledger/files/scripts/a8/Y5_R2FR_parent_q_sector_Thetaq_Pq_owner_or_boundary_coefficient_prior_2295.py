from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICROSCOPE = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"

BRANCH_ID = "MTS_R2FR_PARENT_QLOC_THETAQ_PQ_OWNER_2295"
START_TS = datetime.now(timezone.utc).timestamp()
DOC = ROOT / "2295-Y5-R2FR-parent-q-sector-Thetaq-Pq-owner-or-boundary-coefficient-prior.md"

PATHS = {
    "2294_doc": ROOT / "2294-Y5-R2FR-parent-boundary-charge-formula-Bq-or-alpha3-projection-bound.md",
    "2294_validation": OUT / "P8_Y5_BRR545_2294_VALIDATION.csv",
    "2294_next": OUT / "P8_Y5_PARENT_QLOC_2294_NEXT_TARGET.csv",
    "2294_formula": OUT / "P8_Y5_PARENT_QLOC_2294_PARENT_BOUNDARY_CHARGE_FORMULA.csv",
    "2294_owner": OUT / "P8_Y5_PARENT_QLOC_2294_BQ_OWNER_GATE.csv",
    "2294_alpha3": OUT / "P8_Y5_PARENT_QLOC_2294_ALPHA3_PROJECTION_COEFFICIENT_TEMPLATE.csv",
    "2294_r10": OUT / "P8_Y5_PARENT_QLOC_2294_R10_EDGE_CONTRACT.csv",
    "2247_doc": ROOT / "2247-Y5-R2FR-RAB-parent-R-sector-ThetaR-PR-owner-or-boundary-coefficient-prior.md",
    "2247_validation": OUT / "P8_Y5_BRR545_2247_VALIDATION.csv",
    "2247_classifier": OUT / "P8_Y5_PARENT_QLOC_2247_PARENT_R_CANDIDATE_CLASSIFIER.csv",
    "2247_template": OUT / "P8_Y5_PARENT_QLOC_2247_THETAR_PR_TEMPLATE_CONTRACT.csv",
    "2247_owner": OUT / "P8_Y5_PARENT_QLOC_2247_THETAR_OWNER_GATE.csv",
    "2247_noflux": OUT / "P8_Y5_PARENT_QLOC_2247_NOFLUX_THEOREM_ZERO_ROUTE.csv",
    "2247_priors": OUT / "P8_Y5_PARENT_QLOC_2247_BOUNDARY_COEFFICIENT_PRIOR_TEMPLATE.csv",
    "1041_doc": ROOT / "1041-Y5-R10-parent-X-sector-ThetaX-PX-owner-or-boundary-coefficient-prior.md",
    "1041_validation": OUT / "P8_Y5_BRR545_1041_VALIDATION.csv",
    "1041_priors": OUT / "P8_Y5_R10_1041_BOUNDARY_COEFFICIENT_PRIOR_TEMPLATE.csv",
    "action_terms": OUT / "P8_source_owner_parent_action_terms_CONTRACT.csv",
    "min_action": OUT / "P8_MIN_PARENT_LOCAL_GR_ACTION_BLOCKS.csv",
    "fallback_667": OUT / "P8_Y5_R10_667_RESIDUAL_FALLBACK_ROWS.csv",
    "owner_668": OUT / "P8_Y5_R10_668_SECTOR_OWNER_AUDIT.csv",
    "local_bounds": LOCAL_BOUNDS / "local_bound_claims.csv",
    "r10_candidate": LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv",
}

SOURCES = [
    ("SRC2295_00_2294_doc", "q_formula_handoff", PATHS["2294_doc"], ["Theta_q", "P_q", "2295-Y5-R2FR"], "2294 selected q-sector Theta_q/P_q ownership next."),
    ("SRC2295_01_2294_validation", "prior_validation", PATHS["2294_validation"], ["VAL2294_OVERALL", "PASS"], "2294 validation passed."),
    ("SRC2295_02_2294_next", "explicit_next_target", PATHS["2294_next"], ["2295-Y5-R2FR-parent-q-sector-Thetaq-Pq-owner-or-boundary-coefficient-prior.md", "Theta_q"], "Direct handoff into q-sector symplectic potential owner."),
    ("SRC2295_03_2294_formula", "Bq_formula_contract", PATHS["2294_formula"], ["BQF2294_4_verdict", "MISSING_PARENT_LQ_THETAQ_PQ_REFERENCE_PROJECTOR"], "B_q/Q_q formula requires Theta_q/P_q."),
    ("SRC2295_04_2294_owner", "Bq_owner_gate", PATHS["2294_owner"], ["BQG2294_5_verdict", "FAIL_CURRENT_CLAIM_BQ_NOT_PARENT_OWNED"], "B_q owner gates blocked safely."),
    ("SRC2295_05_2294_alpha3", "q_alpha3_prior_input", PATHS["2294_alpha3"], ["A3P2294_0_formula", "4e-20"], "q alpha3 coefficient rule input."),
    ("SRC2295_06_2294_r10", "q_R10_edge_input", PATHS["2294_r10"], ["R10E2294_1_alpha_edge_bound", "Qbar_edge_qH"], "q R10 edge coefficient input."),
    ("SRC2295_07_2247_doc", "RAB_owner_precedent", PATHS["2247_doc"], ["Theta_R", "P_R", "source-free no-hair"], "R_AB upstream owner scaffold."),
    ("SRC2295_08_2247_validation", "RAB_owner_validation", PATHS["2247_validation"], ["VAL2247_OVERALL", "PASS"], "2247 validation passed."),
    ("SRC2295_09_2247_classifier", "RAB_candidate_classifier", PATHS["2247_classifier"], ["RC2247_0_absent_quotient", "RC2247_2_positive_sourcefree_physical_R"], "Candidate route pattern."),
    ("SRC2295_10_2247_template", "RAB_theta_template", PATHS["2247_template"], ["TPR2247_1_first_derivative", "TPR2247_5_verdict"], "Theta/P template pattern."),
    ("SRC2295_11_2247_owner", "RAB_owner_gate", PATHS["2247_owner"], ["TOG2247_5_verdict", "FAIL_CURRENT_CLAIM_THETAR_PR_OWNER_MISSING"], "Owner gate pattern."),
    ("SRC2295_12_2247_noflux", "RAB_noflux_route", PATHS["2247_noflux"], ["NFR2247_0_positive_energy", "NFR2247_2_first_class_constraint"], "No-flux/no-hair route pattern."),
    ("SRC2295_13_1041_doc", "generic_owner_precedent", PATHS["1041_doc"], ["Theta_X", "P_X", "coefficient priors"], "Generic X owner scaffold."),
    ("SRC2295_14_1041_validation", "generic_owner_validation", PATHS["1041_validation"], ["V1041_SUMMARY", "pass"], "1041 validation passed."),
    ("SRC2295_15_action_terms", "parent_action_contract", PATHS["action_terms"], ["A0_total_covariant_parent", "A7_bulk_X_nohair_or_curve"], "Parent action menu."),
    ("SRC2295_16_min_action", "minimal_local_GR_blocks", PATHS["min_action"], ["A511_3_extra_field_silence", "A511_6_metric_readout"], "Minimal local-GR action block constraints."),
    ("SRC2295_17_667_fallback", "residual_fallback", PATHS["fallback_667"], ["RF667_0_LX_theta_Qtau_owner", "L_X;Theta_X;Q_X"], "Residual fallback owner warning."),
    ("SRC2295_18_668_owner", "sector_owner_audit", PATHS["owner_668"], ["SO668_2_MTS_extra_LX", "missing"], "Existing sector owner audit."),
    ("SRC2295_19_local_bounds", "local_alpha3_bounds", PATHS["local_bounds"], ["R7_alpha3", "4e-20"], "Source-backed alpha3 anchor."),
    ("SRC2295_20_R10_candidate", "R10_bound_candidate", PATHS["r10_candidate"], ["R10_VECTOR_2020_REVIEW", "alpha"], "Review-candidate R10 bound curve, nonclaim."),
]

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2295_SOURCE_REGISTER.csv",
    "classifier": OUT / "P8_Y5_PARENT_QLOC_2295_PARENT_Q_CANDIDATE_CLASSIFIER.csv",
    "template": OUT / "P8_Y5_PARENT_QLOC_2295_THETAQ_PQ_TEMPLATE_CONTRACT.csv",
    "owner_gate": OUT / "P8_Y5_PARENT_QLOC_2295_THETAQ_OWNER_GATE.csv",
    "noflux": OUT / "P8_Y5_PARENT_QLOC_2295_NOFLUX_THEOREM_ZERO_ROUTE.csv",
    "priors": OUT / "P8_Y5_PARENT_QLOC_2295_BOUNDARY_COEFFICIENT_PRIOR_TEMPLATE.csv",
    "selection": OUT / "P8_Y5_PARENT_QLOC_2295_ACTION_SELECTION_LEDGER.csv",
    "mts_template": OUT / "R10_alpha_lambda_curve_MTS_2295_THETAQ_PQ_OWNER_TEMPLATE_NONCLAIM.csv",
    "runner": OUT / "P8_Y5_PARENT_QLOC_2295_RUNNER_SMOKE_STATUS.csv",
    "refusal": OUT / "P8_Y5_PARENT_QLOC_2295_PLACEHOLDER_REFUSAL_RUNNER.csv",
    "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2295_CLAIM_GATES.csv",
    "decisions": OUT / "P8_Y5_PARENT_QLOC_2295_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2295_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2295_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2295_VALIDATION.csv",
}

BRANCH_COPY_TARGETS = {
    "queue_prior": QUEUE / "JR2295_BOUNDARY_COEFFICIENT_PRIOR_NONCLAIM.csv",
    "queue_template": QUEUE / "JR2295_THETAQ_PQ_TEMPLATE_NONCLAIM.csv",
    "branch_wep": MICROSCOPE / "Thetaq_Pq_owner_or_boundary_prior_nonclaim_2295.csv",
    "beta_docs": BETA_DOCS / "THETAQ_PQ_OWNER_OR_BOUNDARY_PRIOR_2295_NONCLAIM.csv",
}


def ensure_dirs() -> None:
    for path in (OUT, QUEUE, MICROSCOPE, BETA_DOCS):
        path.mkdir(parents=True, exist_ok=True)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        if not rows:
            return
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def contains_all(path: Path, needles: list[str]) -> bool:
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8", errors="replace")
    return all(needle in text for needle in needles)


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def alpha3_bound() -> str:
    for row in read_csv(PATHS["local_bounds"]):
        if row.get("row_id") == "R7_alpha3" or row.get("observable") == "alpha3":
            return row.get("upper_bound", "4e-20")
    return "4e-20"


def source_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "source_id": source_id,
            "role": role,
            "path": str(path),
            "exists": path.exists(),
            "needles_present": contains_all(path, needles),
            "needles": ";".join(needles),
            "notes": notes,
            "valid_for_claim": False,
        }
        for source_id, role, path, needles, notes in SOURCES
    ]


def classifier_rows() -> list[dict[str, Any]]:
    rows = [
        ("QC2295_0_absent_quotient", "q is not a primitive parent field", "Theta_q=0 and P_q=0 because there is no independent q variation", "B_q=0 if quotient/nonprimitive q is parent-proved before variation", "must prove q is coordinate/readout artefact before variation, not deleted after local tests", 1, "BEST_THEOREM_ROUTE_NOT_PARENT_SIGNED"),
        ("QC2295_1_first_class_vertical_constraint", "q is a first-class vertical gauge/constraint direction", "Theta_q exists on parent fields and Omega-flat(v_q)=delta C_q; P_q is owned by the momentum-map constraint", "B_q/Q_q vanish only for proper compact transformations unless Q_q exact/proper and K_boundary=0 are proved", "requires parent Omega, D C_q, all-field v_q, bracket closure, degree count, and matter descent", 2, "BEST_ACTIVE_ROUTE_BUT_INCOMPLETE"),
        ("QC2295_2_positive_sourcefree_physical_q", "q is a physical positive operator but source-free in the local branch", "for first-derivative quadratic sector, Theta_q^mu=Z_q nabla^mu q delta q plus mixing/projector terms", "B_q and Phi_boundary vanish only if J_q=0 and boundary flux=0/no-hair are parent-proved", "a physical Green function exists; any source/readout leakage becomes a fifth-force residual", 3, "VIABLE_NOHAIR_ROUTE_INPUTS_MISSING"),
        ("QC2295_3_sourced_residual", "q is a physical sourced residual field", "Theta_q/P_q are standard once L_q is chosen, but the branch must be empirically scored", "alpha(lambda), alpha3, PPN, WEP, clock, and orbital coefficient rows become live", "not a local-GR derivation by itself; it is a testable residual framework", 4, "EMPIRICAL_FALLBACK_ONLY"),
        ("QC2295_4_universal_frame_marker", "matter sees a q-dependent Weyl/disformal/readout frame", "standard finite-sector Theta_q if q has a kinetic block", "source/test coupling is at least a product of source and test legs unless one leg is explicitly inside Qbar", "cheap universal coupling does not prove GR; it creates a fifth-force/clock/WEP countermodel unless the marker is theorem-zero", 5, "COUNTERMODEL_NOT_SOLUTION"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "candidate_id": row[0],
            "parent_route": row[1],
            "Thetaq_Pq_result": row[2],
            "boundary_result": row[3],
            "risk": row[4],
            "rank": row[5],
            "current_status": row[6],
            "valid_for_claim": False,
        }
        for row in rows
    ]


def template_rows() -> list[dict[str, Any]]:
    rows = [
        ("TPQ2295_0_general_variation", "finite-order parent q sector", "delta L_q=E_A delta Y_q^A+nabla_mu Theta_q^mu(delta Y_q)", "L_q is selected with field normalization, derivative order, density convention, and boundary class", "GENERAL_TEMPLATE_DERIVED_NOT_PARENT_SELECTED", "defines the upstream object needed for Q_q, B_q, K_boundary, and no-hair identities"),
        ("TPQ2295_1_first_derivative", "first-derivative template", "Theta_q^mu(delta Y)=Pi_A^mu delta Y^A, Pi_A^mu:=partial L_q/partial(nabla_mu Y^A)", "L_q has no higher derivatives or higher-derivative boundary terms have been reduced by auxiliary fields", "FORMULA_READY_LQ_MISSING", "turns a chosen L_q into a computable symplectic potential"),
        ("TPQ2295_2_finite_jet", "higher finite-jet template", "Theta_q^mu=sum_{r=0}^{N-1} Pi_A^{mu alpha_1...alpha_r} nabla_{alpha_1}...nabla_{alpha_r} delta Y^A", "finite derivative order N and all corner/counterterm conventions are declared", "FORMULA_READY_FINITE_JET_ORDER_MISSING", "fixes which epsilon_q jets must vanish for proper boundary silence"),
        ("TPQ2295_3_Noether_Pq", "P_q from vertical generator", "insert delta_epsilon Y^A=R^A_q epsilon_q+R^{A mu}_q nabla_mu epsilon_q+... into Theta_q; P_q^mu is the coefficient package whose divergence enters C_q", "v_q action on every parent field and tensor/density convention for C_q are fixed", "CONTRACT_READY_FIELD_ACTION_AND_CONVENTION_MISSING", "connects Theta_q to B_q=sigma n_mu P_q^mu+..."),
        ("TPQ2295_4_positive_q_example", "minimal positive scalar-like q residual example", "L_q=-1/2 Z_q nabla_mu q nabla^mu q -1/2 M_q^2 q^2 + J_q q gives Theta_q^mu=-Z_q nabla^mu q delta q", "q really is the retained local amplitude, Z_q>0, M_q^2>0, J_q and boundary data are source-owned", "EXAMPLE_ONLY_NOT_SELECTED", "if J_q=0 and boundary flux=0, no-hair can set q=0; otherwise alpha(lambda) is live"),
        ("TPQ2295_5_verdict", "Theta_q/P_q owner status", "Theta_q/P_q template is mathematically ready, but no parent q block is selected or proved", "one candidate in QC2295 closes its owner gates", "FAIL_CURRENT_CLAIM_THETAQ_PQ_NOT_PARENT_OWNED", "use nonclaim priors/templates for boundary coefficients until a parent block is signed"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "template_id": row[0],
            "object": row[1],
            "formula": row[2],
            "owned_if": row[3],
            "current_status": row[4],
            "claim_effect": row[5],
            "score_ready": False,
            "valid_for_claim": False,
        }
        for row in rows
    ]


def owner_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("TOG2295_0_parent_route", "select one parent q route", "absent quotient, first-class vertical constraint, positive sourcefree field, or sourced residual is chosen before scoring", "ROUTE_NOT_PARENT_SELECTED", "Theta_q/P_q remain a menu rather than an action"),
        ("TOG2295_1_field_content", "field list and transformation law", "Y_q^A and delta_epsilon Y_q^A are declared for metric/coframe, q, extra modes, domain/memory, matter, and boundary fields", "FIELD_ACTION_INCOMPLETE", "P_q cannot be computed from Theta_q"),
        ("TOG2295_2_operator_signs", "positive/no-pole or residual operator", "Z_q, M_q^2, kinetic sign, projector mixing, and Hessian positivity are parent-owned", "OPERATOR_SIGNS_MISSING", "local-GR reduction cannot tell no-hair from hidden dynamics"),
        ("TOG2295_3_source_zero", "source/test blindness", "J_q=0, qbar_qT=0, Qbar_edge_qH=0, or bounded coefficient rows are sourced channelwise", "SOURCE_ZERO_OR_BOUND_MISSING", "R10/WEP/clock/PPN/orbital residual rows remain live"),
        ("TOG2295_4_boundary_flux", "boundary no-flux or coefficient row", "Phi_boundary_local_q=0 theorem or alpha3/R10 boundary coefficients are source-backed", "BOUNDARY_FLUX_ZERO_OR_BOUND_MISSING", "K_boundary_alpha3_q and edge R10 templates remain nonclaim"),
        ("TOG2295_5_verdict", "claim-grade Theta_q/P_q owner", "TOG2295_0 through TOG2295_4 pass together", "FAIL_CURRENT_CLAIM_THETAQ_PQ_OWNER_MISSING", "demote to nonclaim coefficient priors/templates"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": row[0],
            "needed": row[1],
            "test": row[2],
            "current_status": row[3],
            "if_missing": row[4],
            "valid_for_claim": False,
        }
        for row in rows
    ]


def noflux_rows() -> list[dict[str, Any]]:
    rows = [
        ("NFR2295_0_positive_energy", "positive source-free operator", "int_A q L_q q = positive_norm[q] + Phi_boundary_local_q", "positive_norm plus Phi_boundary_local_q=0 plus J_q=0 forces q=0 modulo pure gauge/topological class", "L_q, sign proof, source-zero, boundary flux theorem, allowed topology", "PROMISING_NOT_PARENT_SIGNED"),
        ("NFR2295_1_topological_exact", "topological/exact boundary sector", "L_boundary=dB or class-only topological density with no local metric/source variation", "edge flux is fixed background subtraction or exact on the certified boundary class", "boundary class owner, harmonic/corner control, reference subtraction", "ROUTE_OPEN_NOT_CLOSED"),
        ("NFR2295_2_first_class_constraint", "constraint/gauge no-pole", "Omega_flat(v_q)=delta C_q and bracket closes first-class with Q_q/K_boundary proper-zero", "q is removed from reduced phase space after degree count and matter descent", "parent Omega, D C_q, all-field v_q, bracket, degree count, matter/no-marker descent", "BEST_THEOREM_ROUTE_INCOMPLETE"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": row[0],
            "route": row[1],
            "identity": row[2],
            "closure_condition": row[3],
            "missing": row[4],
            "current_status": row[5],
            "valid_for_claim": False,
        }
        for row in rows
    ]


def prior_rows() -> list[dict[str, Any]]:
    bound = alpha3_bound()
    rows = [
        ("BCP2295_0_K_boundary_alpha3_q", "K_boundary_alpha3_q", "alpha3", f"if Phi_boundary_local_q is sourced and nonzero, |K_boundary_alpha3_q| <= {bound}/|Phi_boundary_local_q|", bound, "Phi_boundary_local_q numeric/source-backed or theorem-zero; normalization; uncertainty policy", "NONCLAIM_PRIOR_SCHEMA_READY_INPUTS_MISSING"),
        ("BCP2295_1_Phi_boundary_local_q", "Phi_boundary_local_q", "alpha3;R10;orbital", "Phi_boundary_local_q=0 by no-flux theorem, or numeric amplitude with units and source path", "theorem_zero_or_numeric", "boundary norm, surface, units, time/source normalization, topology/corner policy", "NONCLAIM_PRIOR_SCHEMA_READY_INPUTS_MISSING"),
        ("BCP2295_2_edge_R10_coefficients_q", "K_edge_q;Qbar_edge_qH;qbar_qT", "alpha_R10(lambda)", "|alpha_edge_q|=|K_edge_q Qbar_edge_qH qbar_qT| must be <= alpha_bound(lambda) after curve promotion", "review-candidate alpha_bound(lambda) only", "K_edge_q(lambda), Qbar_edge_qH(lambda), qbar_qT, lambda support, promoted bound curve", "NONCLAIM_PRIOR_SCHEMA_READY_INPUTS_MISSING"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "prior_id": row[0],
            "coefficient": row[1],
            "observable": row[2],
            "prior_or_bound_rule": row[3],
            "anchor_bound": row[4],
            "required_inputs": row[5],
            "current_status": row[6],
            "score_ready": False,
            "valid_for_claim": False,
        }
        for row in rows
    ]


def selection_rows() -> list[dict[str, Any]]:
    rows = [
        ("SEL2295_0_do_not_select_yet", "Do not select a public parent q action at 2295.", "the corpus has candidate routes but no source file proving the required L_q/Theta_q/P_q package", "use the templates as contracts for the next derivation step"),
        ("SEL2295_1_best_derivation_next", "Best derivation route remains absent/quotient or first-class constraint first, then positive/nohair.", "those are the routes that can genuinely reduce to local GR rather than merely survive empirical bounds", "try to close source-free energy identity or first-class momentum-map owner before coefficient priors"),
        ("SEL2295_2_fallback_prior", "If the owner route stalls, use alpha3/R10 coefficient priors as private diagnostic scaffolding.", "the exact inequalities are known, but numeric K/Phi/Qbar values would be invented today", "nonclaim rows only"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "selection_id": row[0],
            "decision": row[1],
            "reason": row[2],
            "safe_use": row[3],
            "valid_for_claim": False,
        }
        for row in rows
    ]


def mts_template_rows() -> list[dict[str, Any]]:
    rows = [
        ("Thetaq_Pq_owner_contract", "MISSING_PARENT_ROUTE", "MISSING_PARENT_THETAQ_PQ_OWNER", "Theta_q/P_q determine B_q, Q_q, K_boundary, and any edge alpha(lambda)", "template_invalid_parent_route_not_selected"),
        ("sourcefree_q_nohair_template", "MISSING_POSITIVE_OPERATOR", "MISSING_ZQ_MQ2_JQ_ZERO_PHI_ZERO", "positive_norm[q]+Phi_boundary_local_q=0 with source-free J_q=0 can force q=0", "template_invalid_positive_nohair_inputs_missing"),
        ("alpha3_q_coefficient_prior_template", "MISSING_NOT_R10_RANGE", "MISSING_K_BOUNDARY_ALPHA3_Q_PHI_BOUNDARY_LOCAL_Q", f"|K_boundary_alpha3_q Phi_boundary_local_q| <= {alpha3_bound()}", "template_invalid_prior_inputs_missing"),
        ("R10_q_edge_prior_template", "MISSING_PARENT_LAMBDA_Q", "MISSING_KEDGE_QBAR_EDGE_QH_QBAR_QT", "|alpha_edge_q|=|K_edge_q Qbar_edge_qH qbar_qT| <= alpha_bound(lambda)", "template_invalid_R10_prior_inputs_missing"),
    ]
    return [
        {
            "model": "MTS_source_normalized_Newton_branch",
            "branch_id": row[0],
            "lambda_value": row[1],
            "alpha_predicted": row[2],
            "force_law_form": row[3],
            "derivation_status": row[4],
            "score_ready": False,
            "valid_for_claim": False,
        }
        for row in rows
    ]


def runner_rows() -> list[dict[str, Any]]:
    return [{"branch_id": BRANCH_ID, "runner_id": "SMOKE2295_0_runner_status", "input_rows": 4, "claim_valid_rows": 0, "numeric_score_rows": 0, "runner_would_claim": False, "runner_would_score": False, "status": "blocked_nonclaim", "valid_for_claim": False}]


def refusal_rows(groups: list[list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows = []
    for group in groups:
        for row in group:
            row_id = row.get("candidate_id") or row.get("template_id") or row.get("gate_id") or row.get("route_id") or row.get("prior_id") or row.get("selection_id") or row.get("branch_id")
            obj = row.get("parent_route") or row.get("object") or row.get("needed") or row.get("route") or row.get("coefficient") or row.get("decision") or row.get("force_law_form")
            status = row.get("current_status") or row.get("derivation_status") or "NONCLAIM"
            reason = row.get("risk") or row.get("owned_if") or row.get("if_missing") or row.get("missing") or row.get("required_inputs") or row.get("reason") or row.get("force_law_form")
            rows.append({"branch_id": BRANCH_ID, "refusal_id": f"REF2295_{row_id}", "object": obj, "status": status, "refusal_status": "not_claim_promoted", "reason": f"{reason};VALID_FOR_CLAIM_FALSE", "score_ready": False, "valid_for_claim": False})
    return rows


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("CGATE2295_0_parent_q_owner", "parent q-sector action owns Theta_q/P_q", False, "candidate routes are ranked and templates are written, but no L_q/field-content/operator/source/boundary package is parent-selected"),
        ("CGATE2295_1_local_GR_no_pole", "q is absent/gauge/sourcefree enough to reduce locally to GR/Newton", False, "absent quotient, first-class constraint, or positive no-hair route is not closed"),
        ("CGATE2295_2_alpha3_prior", "alpha3 q coefficient prior is executable", False, "K_boundary_alpha3_q and Phi_boundary_local_q remain missing"),
        ("CGATE2295_3_R10_prior", "R10 q edge coefficient prior is executable", False, "K_edge_q, Qbar_edge_qH, qbar_qT, lambda support, and promoted bound curve remain incomplete"),
    ]
    return [{"branch_id": BRANCH_ID, "gate_id": row[0], "claim": row[1], "gate_pass": row[2], "reason": row[3], "valid_for_claim": False} for row in rows]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        ("DEC2295_0_parent_route_status", "Do not pretend a parent q action is selected yet.", "2295 derives the generic Theta_q/P_q machinery but does not find a source file proving any candidate route", "attack the absent/quotient, first-class, or positive/nohair source-zero route directly"),
        ("DEC2295_1_best_route", "Best derivation route is quotient/first-class first, positive no-hair second, empirical residual last.", "quotient/constraint gives true no-pole if it closes; positive no-hair can still derive local silence; sourced residual is testable but not a GR reduction", "try to close source-free positive q no-hair or first-class momentum-map owner before coefficient priors"),
        ("DEC2295_2_next_target", "Next target should test the source-free positive q no-hair identity and first-class alternative.", "it is the most concrete route that can convert Theta_q/P_q templates into local-GR reduction without inventing coefficients", "2296-Y5-R2FR-q-sourcefree-positive-nohair-or-firstclass-owner-gate.md"),
    ]
    return [{"branch_id": BRANCH_ID, "decision_id": row[0], "decision": row[1], "because": row[2], "next_action": row[3], "valid_for_claim": False} for row in rows]


def next_target_rows() -> list[dict[str, Any]]:
    return [{
        "branch_id": BRANCH_ID,
        "next_target": "2296-Y5-R2FR-q-sourcefree-positive-nohair-or-firstclass-owner-gate.md",
        "script": "scripts/Y5_R2FR_q_sourcefree_positive_nohair_or_firstclass_owner_gate_2296.py",
        "objective": "try to derive the source-free positive q-sector no-hair identity with Z_q>0, M_q^2>0, J_q=0, and Phi_boundary_local_q=0, while testing the first-class constraint alternative; if both fail, fill the first nonclaim alpha3/R10 prior row",
        "include": "positive operator identity, source-zero clauses, boundary flux zero, topology/gauge caveats, Hessian sign gates, Omega_flat(v_q)=delta C_q alternative, degree-count hooks, alpha3/R10 prior schema",
        "exclude": "invented Z/M/J/K/Phi/Qbar values, deleting GR charges, naked linear c_g scoring, cancellation between residuals, R10/local-GR pass claim, formalization-workbench edits, GitHub action",
        "valid_for_claim": False,
    }]


def copy_branch_files() -> list[dict[str, Any]]:
    plan = {"queue_prior": OUTPUTS["priors"], "queue_template": OUTPUTS["template"], "branch_wep": OUTPUTS["priors"], "beta_docs": OUTPUTS["priors"]}
    rows = []
    for copy_id, src in plan.items():
        dest = BRANCH_COPY_TARGETS[copy_id]
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dest)
        rows.append({"branch_id": BRANCH_ID, "copy_id": copy_id, "source": str(src), "destination": str(dest), "source_exists": src.exists(), "destination_exists": dest.exists(), "notes": "branch/quarantine copy for 2295 Theta_q/P_q owner checkpoint"})
    return rows


def parse_csvs(paths: list[Path]) -> bool:
    try:
        for path in paths:
            read_csv(path)
        return True
    except Exception:
        return False


def claim_flags_false(paths: list[Path]) -> bool:
    fields = {"valid_for_claim", "score_ready", "runner_would_claim", "runner_would_score"}
    for path in paths:
        for row in read_csv(path):
            for field in fields.intersection(row.keys()):
                if str(row[field]).lower() not in {"false", "0", "no"}:
                    return False
    return True


def formalization_count() -> int:
    if not FORMALIZATION.exists():
        return 0
    ignored = {"__pycache__", ".git", ".venv", "venv", "node_modules"}
    return sum(1 for path in FORMALIZATION.rglob("*2295*") if not any(part in ignored for part in path.parts))


def formalization_touched() -> bool:
    if not FORMALIZATION.exists():
        return False
    ignored = {"__pycache__", ".git", ".venv", "venv", "node_modules"}
    for path in FORMALIZATION.rglob("*"):
        if any(part in ignored for part in path.parts):
            continue
        try:
            if path.stat().st_mtime >= START_TS:
                return True
        except OSError:
            continue
    return False


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def validation_rows(copies: list[dict[str, Any]]) -> list[dict[str, Any]]:
    generated = [path for key, path in OUTPUTS.items() if key != "validation"] + [Path(row["destination"]) for row in copies]
    checks = [
        ("VAL2295_00_sources_exist", all(row["exists"] for row in source_rows()), "all direct and registered 2295 source paths exist"),
        ("VAL2295_01_needles_present", all(row["needles_present"] for row in source_rows()), "all cited source needles are present"),
        ("VAL2295_02_prior_validations", contains_all(PATHS["2294_validation"], ["VAL2294_OVERALL", "PASS"]) and contains_all(PATHS["2247_validation"], ["VAL2247_OVERALL", "PASS"]) and contains_all(PATHS["1041_validation"], ["V1041_SUMMARY", "pass"]), "2294, 2247, and 1041 validations pass overall"),
        ("VAL2295_03_candidates_ranked", len(read_csv(OUTPUTS["classifier"])) >= 5 and any(row["candidate_id"] == "QC2295_0_absent_quotient" for row in read_csv(OUTPUTS["classifier"])), "parent q candidate routes are ranked without selection"),
        ("VAL2295_04_Thetaq_Pq_templates", any(row["template_id"] == "TPQ2295_1_first_derivative" and "Theta_q" in row["formula"] for row in read_csv(OUTPUTS["template"])) and any(row["current_status"] == "FAIL_CURRENT_CLAIM_THETAQ_PQ_NOT_PARENT_OWNED" for row in read_csv(OUTPUTS["template"])), "Theta_q/P_q templates are written and not parent-promoted"),
        ("VAL2295_05_owner_gates_fail_safely", any(row["current_status"] == "FAIL_CURRENT_CLAIM_THETAQ_PQ_OWNER_MISSING" for row in read_csv(OUTPUTS["owner_gate"])) and all(row["valid_for_claim"].lower() == "false" for row in read_csv(OUTPUTS["owner_gate"])), "owner gates identify missing route, field action, signs, source-zero, and boundary flux"),
        ("VAL2295_06_nohair_routes_staged", any(row["route_id"] == "NFR2295_0_positive_energy" for row in read_csv(OUTPUTS["noflux"])) and any(row["route_id"] == "NFR2295_2_first_class_constraint" for row in read_csv(OUTPUTS["noflux"])), "no-hair and first-class routes are staged as nonclaim derivation targets"),
        ("VAL2295_07_coefficient_priors_nonclaim", len(read_csv(OUTPUTS["priors"])) >= 3 and any(row["coefficient"] == "K_boundary_alpha3_q" for row in read_csv(OUTPUTS["priors"])) and all(row["score_ready"].lower() == "false" for row in read_csv(OUTPUTS["priors"])), "alpha3/R10 q coefficient prior templates remain nonclaim"),
        ("VAL2295_08_action_selection_refused", any(row["selection_id"] == "SEL2295_0_do_not_select_yet" for row in read_csv(OUTPUTS["selection"])), "no parent q action is falsely selected at 2295"),
        ("VAL2295_09_mts_template_nonclaim", all(row["valid_for_claim"].lower() == "false" for row in read_csv(OUTPUTS["mts_template"])), "MTS smoke template has no claim-valid rows"),
        ("VAL2295_10_runner_smoke_refuses_claim", read_csv(OUTPUTS["runner"])[0]["runner_would_claim"].lower() == "false", "runner smoke status refuses claim"),
        ("VAL2295_11_claim_gates_blocked", all(row["valid_for_claim"].lower() == "false" for row in read_csv(OUTPUTS["claim_gates"])), "all local-GR/empirical claim gates remain blocked"),
        ("VAL2295_12_next_target_written", read_csv(OUTPUTS["next_target"])[0]["next_target"].startswith("2296-Y5-R2FR-q-sourcefree-positive-nohair"), "next target row is present"),
        ("VAL2295_13_csv_parse", parse_csvs(generated), "all generated 2295 CSVs parse cleanly"),
        ("VAL2295_14_claim_flags_false", claim_flags_false(generated), "all generated prediction/claim flags remain false"),
        ("VAL2295_15_branch_copies", len(copies) == len(BRANCH_COPY_TARGETS) and parse_csvs([Path(row["destination"]) for row in copies]), "branch/quarantine nonclaim copies exist and parse"),
        ("VAL2295_16_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent after run"),
        ("VAL2295_17_formalization_no_2295", formalization_count() == 0, "formalization-workbench has no non-venv 2295 artifacts"),
        ("VAL2295_18_formalization_untouched", not formalization_touched(), "formalization-workbench untouched during 2295 run"),
    ]
    rows = [{"branch_id": BRANCH_ID, "check_id": check_id, "result": "PASS" if passed else "FAIL", "detail": detail} for check_id, passed, detail in checks]
    rows.append({"branch_id": BRANCH_ID, "check_id": "VAL2295_OVERALL", "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL", "detail": "2295 ranks q parent routes, writes Theta_q/P_q templates, refuses action selection, keeps coefficient priors nonclaim, and selects q no-hair/first-class owner gate next"})
    return rows


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(str(row.get(column, "")).replace("\n", " ").replace("|", "\\|") for column in columns) + " |" for row in rows]
    return "\n".join([header, sep, *body])


def build_doc(sources, classifier, template, owner, noflux, priors, selection, mts, runner, refusals, gates, decisions, next_target, copies, validation) -> str:
    src_md = [{**row, "path": rel(Path(row["path"]))} for row in sources]
    copy_md = [{**row, "source": rel(Path(row["source"])), "destination": rel(Path(row["destination"]))} for row in copies]
    return "\n\n".join([
        "# 2295 - Y5/R2FR Parent q-Sector Theta_q/P_q Owner or Boundary Coefficient Prior",
        "## Verdict\n- 2295 makes the parent-action menu explicit for the q boundary sector: `Theta_q` and `P_q` can be computed once a lawful `L_q` or constraint route is selected.\n- No parent `L_q`, `Theta_q`, or `P_q` owner is selected here. The templates are contracts, not claims.\n- Alpha3/R10 coefficient priors remain private nonclaim scaffolding.",
        "## Source Register\n" + md_table(src_md, ["source_id", "role", "path", "exists", "needles_present", "notes", "valid_for_claim"]),
        "## Parent q Candidate Classifier\n" + md_table(classifier, ["candidate_id", "parent_route", "Thetaq_Pq_result", "boundary_result", "risk", "rank", "current_status", "valid_for_claim"]),
        "## Theta_q/P_q Template Contract\n" + md_table(template, ["template_id", "object", "formula", "owned_if", "current_status", "claim_effect", "score_ready", "valid_for_claim"]),
        "## Theta_q Owner Gate\n" + md_table(owner, ["gate_id", "needed", "test", "current_status", "if_missing", "valid_for_claim"]),
        "## No-Flux / No-Hair Route\n" + md_table(noflux, ["route_id", "route", "identity", "closure_condition", "missing", "current_status", "valid_for_claim"]),
        "## Boundary Coefficient Prior Template\n" + md_table(priors, ["prior_id", "coefficient", "observable", "prior_or_bound_rule", "anchor_bound", "required_inputs", "current_status", "score_ready", "valid_for_claim"]),
        "## Action Selection Ledger\n" + md_table(selection, ["selection_id", "decision", "reason", "safe_use", "valid_for_claim"]),
        "## MTS Smoke Template\n" + md_table(mts, ["model", "branch_id", "lambda_value", "alpha_predicted", "force_law_form", "derivation_status", "score_ready", "valid_for_claim"]),
        "## Runner Smoke Status\n" + md_table(runner, ["runner_id", "input_rows", "claim_valid_rows", "numeric_score_rows", "runner_would_claim", "runner_would_score", "status", "valid_for_claim"]),
        "## Placeholder Refusal Runner\n" + md_table(refusals, ["refusal_id", "object", "status", "refusal_status", "reason", "score_ready", "valid_for_claim"]),
        "## Claim Gates\n" + md_table(gates, ["gate_id", "claim", "gate_pass", "reason", "valid_for_claim"]),
        "## Decision Ledger\n" + md_table(decisions, ["decision_id", "decision", "because", "next_action", "valid_for_claim"]),
        "## Next Target\n" + md_table(next_target, ["next_target", "script", "objective", "include", "exclude", "valid_for_claim"]),
        "## Branch Copies\n" + md_table(copy_md, ["copy_id", "source", "destination", "source_exists", "destination_exists", "notes"]),
        "## Validation\n" + md_table(validation, ["check_id", "result", "detail"]),
        "## Working Interpretation\nThe useful thing here is the coupling problem is now upstreamed into an action-selection problem. If q is quotient or first-class, the local branch can genuinely reduce toward GR. If q is a positive source-free field, the no-hair identity becomes the bridge. If q is sourced, it is not a GR derivation by itself; it is a testable residual sector with alpha3/R10/WEP/clock rows.",
    ]) + "\n"


def main() -> None:
    ensure_dirs()
    sources = source_rows()
    classifier = classifier_rows()
    template = template_rows()
    owner = owner_gate_rows()
    noflux = noflux_rows()
    priors = prior_rows()
    selection = selection_rows()
    mts = mts_template_rows()
    runner = runner_rows()
    refusals = refusal_rows([classifier, template, owner, noflux, priors, selection, mts])
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_target_rows()

    for key, rows in [
        ("source_register", sources),
        ("classifier", classifier),
        ("template", template),
        ("owner_gate", owner),
        ("noflux", noflux),
        ("priors", priors),
        ("selection", selection),
        ("mts_template", mts),
        ("runner", runner),
        ("refusal", refusals),
        ("claim_gates", gates),
        ("decisions", decisions),
        ("next_target", next_target),
    ]:
        write_csv(OUTPUTS[key], rows)

    copies = copy_branch_files()
    write_csv(OUTPUTS["branch_copies"], copies)
    remove_pycache()
    validation = validation_rows(copies)
    write_csv(OUTPUTS["validation"], validation)
    DOC.write_text(build_doc(sources, classifier, template, owner, noflux, priors, selection, mts, runner, refusals, gates, decisions, next_target, copies, validation), encoding="utf-8")
    remove_pycache()

    failed = [row for row in validation if row["result"] != "PASS"]
    if failed:
        raise SystemExit("2295 validation failed: " + ", ".join(row["check_id"] for row in failed))
    print(f"Wrote {DOC}")
    print(f"Wrote {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
