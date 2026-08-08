from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICROSCOPE = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
FORMALIZATION = ROOT.parent / "formalization-workbench"
DOC = ROOT / "2247-Y5-R2FR-RAB-parent-R-sector-ThetaR-PR-owner-or-boundary-coefficient-prior.md"
BRANCH_ID = "MTS_R2FR_PARENT_QLOC_RAB_THETAR_PR_OWNER_2247"
START_TS = datetime.now(timezone.utc).timestamp()


SOURCE_FILES = {
    "2246_doc": ROOT / "2246-Y5-R2FR-RAB-parent-boundary-charge-formula-BR-or-alpha3-projection-bound.md",
    "2246_validation": OUT / "P8_Y5_BRR545_2246_VALIDATION.csv",
    "2246_next": OUT / "P8_Y5_PARENT_QLOC_2246_NEXT_TARGET.csv",
    "2246_formula": OUT / "P8_Y5_PARENT_QLOC_2246_PARENT_BOUNDARY_CHARGE_FORMULA.csv",
    "2246_alpha3": OUT / "P8_Y5_PARENT_QLOC_2246_ALPHA3_PROJECTION_COEFFICIENT_TEMPLATE.csv",
    "1041_doc": ROOT / "1041-Y5-R10-parent-X-sector-ThetaX-PX-owner-or-boundary-coefficient-prior.md",
    "1041_validation": OUT / "P8_Y5_BRR545_1041_VALIDATION.csv",
    "1041_classifier": OUT / "P8_Y5_R10_1041_PARENT_X_CANDIDATE_CLASSIFIER.csv",
    "1041_template": OUT / "P8_Y5_R10_1041_THETAX_PX_TEMPLATE_CONTRACT.csv",
    "1041_owner_gate": OUT / "P8_Y5_R10_1041_THETAX_OWNER_GATE.csv",
    "1041_noflux": OUT / "P8_Y5_R10_1041_NOFLUX_THEOREM_ZERO_ROUTE.csv",
    "1041_priors": OUT / "P8_Y5_R10_1041_BOUNDARY_COEFFICIENT_PRIOR_TEMPLATE.csv",
    "579_contract": OUT / "P8_Y5_R10_579_EXPLICIT_PARENT_X_BLOCK_CONTRACT.csv",
    "580_candidates": OUT / "P8_Y5_R10_580_PARENT_BLOCK_CANDIDATES.csv",
    "action_terms": OUT / "P8_source_owner_parent_action_terms_CONTRACT.csv",
    "min_action": OUT / "P8_MIN_PARENT_LOCAL_GR_ACTION_BLOCKS.csv",
    "667_fallback": OUT / "P8_Y5_R10_667_RESIDUAL_FALLBACK_ROWS.csv",
    "extra_energy": OUT / "P8_EXTRA_SECTOR_SILENCE_ENERGY_IDENTITY.csv",
    "668_owner": OUT / "P8_Y5_R10_668_SECTOR_OWNER_AUDIT.csv",
    "local_bounds": LOCAL_BOUNDS / "local_bound_claims.csv",
    "r10_candidate": LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv",
    "r10_runner": ROOT / "scripts" / "R10_alpha_lambda_bound_prediction_runner.py",
}


SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_2247_SOURCE_REGISTER.csv"
PARENT_R_CANDIDATE_CLASSIFIER = OUT / "P8_Y5_PARENT_QLOC_2247_PARENT_R_CANDIDATE_CLASSIFIER.csv"
THETAR_PR_TEMPLATE = OUT / "P8_Y5_PARENT_QLOC_2247_THETAR_PR_TEMPLATE_CONTRACT.csv"
THETAR_OWNER_GATE = OUT / "P8_Y5_PARENT_QLOC_2247_THETAR_OWNER_GATE.csv"
NOFLUX_THEOREM_ROUTE = OUT / "P8_Y5_PARENT_QLOC_2247_NOFLUX_THEOREM_ZERO_ROUTE.csv"
BOUNDARY_COEFFICIENT_PRIOR = OUT / "P8_Y5_PARENT_QLOC_2247_BOUNDARY_COEFFICIENT_PRIOR_TEMPLATE.csv"
ACTION_SELECTION = OUT / "P8_Y5_PARENT_QLOC_2247_ACTION_SELECTION_DECISION.csv"
MTS_ALPHA_TEMPLATE = OUT / "R10_alpha_lambda_curve_MTS_2247_THETAR_PR_TEMPLATE_NONCLAIM.csv"
RUNNER_SMOKE = OUT / "P8_Y5_PARENT_QLOC_2247_RUNNER_SMOKE_STATUS.csv"
PLACEHOLDER_REFUSAL = OUT / "P8_Y5_PARENT_QLOC_2247_PLACEHOLDER_REFUSAL_RUNNER.csv"
CLAIM_GATES = OUT / "P8_Y5_PARENT_QLOC_2247_CLAIM_GATES.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_2247_DECISION_LEDGER.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_2247_NEXT_TARGET.csv"
BRANCH_COPIES = OUT / "P8_Y5_PARENT_QLOC_2247_BRANCH_COPIES.csv"
VALIDATION = OUT / "P8_Y5_BRR545_2247_VALIDATION.csv"


COPY_TARGETS = {
    "queue_theta": QUEUE / "JR2247_THETAR_PR_OWNER_TEMPLATE_NONCLAIM.csv",
    "queue_prior": QUEUE / "JR2247_BOUNDARY_COEFFICIENT_PRIOR_NONCLAIM.csv",
    "branch_wep": MICROSCOPE / "ThetaR_PR_owner_or_boundary_prior_nonclaim_2247.csv",
    "beta_docs": BETA_DOCS / "THETAR_PR_OWNER_OR_BOUNDARY_PRIOR_2247_NONCLAIM.csv",
}


GENERATED = [
    SOURCE_REGISTER,
    PARENT_R_CANDIDATE_CLASSIFIER,
    THETAR_PR_TEMPLATE,
    THETAR_OWNER_GATE,
    NOFLUX_THEOREM_ROUTE,
    BOUNDARY_COEFFICIENT_PRIOR,
    ACTION_SELECTION,
    MTS_ALPHA_TEMPLATE,
    RUNNER_SMOKE,
    PLACEHOLDER_REFUSAL,
    CLAIM_GATES,
    DECISION,
    NEXT_TARGET,
    BRANCH_COPIES,
    VALIDATION,
]


def flags() -> dict[str, bool]:
    return {
        "numeric_value_present": False,
        "source_backed": False,
        "score_ready": False,
        "valid_prediction_row": False,
        "valid_for_claim": False,
        "claim_allowed": False,
    }


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def resolve_project_path(path_text: str) -> Path:
    path = Path(path_text.strip())
    if path.is_absolute():
        return path
    return ROOT / path


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def parse_csv(path: Path) -> bool:
    read_csv(path)
    return True


def validation_pass(path: Path) -> bool:
    if not path.exists():
        return False
    rows = read_csv(path)
    if not rows:
        return False
    id_key = "check_id" if "check_id" in rows[0] else "validation_id"
    result_key = "result" if "result" in rows[0] else "status"
    overall_rows = [row for row in rows if "overall" in row.get(id_key, "").lower() or "summary" in row.get(id_key, "").lower()]
    if overall_rows:
        return all(row.get(result_key, "").lower() == "pass" for row in overall_rows)
    return all(row.get(result_key, "").lower() == "pass" for row in rows)


def source_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, (key, path) in enumerate(SOURCE_FILES.items()):
        if key.startswith("2246"):
            role = "current R2FR B_R/Q_R handoff"
        elif key.startswith("1041"):
            role = "older Theta_X/P_X owner scaffold being specialized to R_AB"
        elif key.startswith(("579", "580", "action", "min", "667", "extra", "668")):
            role = "parent action, candidate, or energy/nohair source evidence"
        else:
            role = "external local bound or runner ledger"
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": f"SRC2247_{index}_{key}",
                "source_path": rel(path),
                "path_exists": path.exists(),
                "validation_overall_pass": validation_pass(path) if key.endswith("validation") else "",
                "role": role,
                **flags(),
            }
        )
    return rows


def source_register_paths_exist() -> bool:
    return all(resolve_project_path(row["source_path"]).exists() for row in read_csv(SOURCE_REGISTER))


def candidate_rows() -> list[dict[str, Any]]:
    rows = [
        ("RC2247_0_absent_quotient", "R_AB is not a primitive parent field", "Theta_R=0 and P_R=0 because there is no independent R_AB variation", "B_R=0 if the quotient/nonprimitive claim is parent-proved", "must prove R_AB is a coordinate/readout artefact before variation, not a post-hoc deletion", 1, "BEST_THEOREM_ROUTE_NOT_PARENT_SIGNED"),
        ("RC2247_1_first_class_vertical_constraint", "R_AB is a first-class vertical gauge/constraint direction", "Theta_R exists on parent fields and Omega-flat(v_R)=delta C_R; P_R is owned by the momentum-map constraint", "B_R/Q_R vanish only for proper compact transformations unless Q_R exact/proper and K_boundary=0 are proved", "requires parent Omega, D C_R, all-field v_R, bracket closure, degree count, and matter descent", 2, "BEST_ACTIVE_ROUTE_BUT_INCOMPLETE"),
        ("RC2247_2_positive_sourcefree_physical_R", "R_AB is a physical positive operator but source-free in the local branch", "for first-derivative quadratic sector, Theta_R^mu=Z_R nabla^mu R_AB delta R^AB plus mixing/projector terms", "B_R and Phi_boundary vanish only if J_R=0 and boundary flux=0/no-hair are parent-proved", "a physical Green function exists; any source/readout leakage becomes a fifth-force residual", 3, "VIABLE_NOHAIR_ROUTE_INPUTS_MISSING"),
        ("RC2247_3_sourced_residual", "R_AB is a physical sourced residual field", "Theta_R/P_R are standard once L_R is chosen, but the branch must be empirically scored", "alpha(lambda), alpha3, PPN, WEP, clock, and Gdot coefficient rows become live", "not a local-GR derivation by itself; it is a testable residual framework", 4, "EMPIRICAL_FALLBACK_ONLY"),
        ("RC2247_4_universal_conformal", "matter sees exp(2 a R)g or an R_AB-dependent frame", "standard finite-sector Theta_R if R_AB has a kinetic block", "source/test coupling is at least quadratic in a universal coupling unless source leg is separately declared", "cheap universal coupling does not prove GR; it creates a fifth-force countermodel unless a=0 is derived", 5, "COUNTERMODEL_NOT_SOLUTION"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "candidate_id": candidate_id,
            "parent_route": route,
            "ThetaR_PR_result": theta,
            "boundary_result": boundary,
            "risk": risk,
            "rank": rank,
            "current_status": status,
            **flags(),
        }
        for candidate_id, route, theta, boundary, risk, rank, status in rows
    ]


def template_rows() -> list[dict[str, Any]]:
    rows = [
        ("TPR2247_0_general_variation", "finite-order parent R_AB sector", "delta L_R = E_A delta Y_R^A + nabla_mu Theta_R^mu(delta Y_R)", "L_R is selected with field normalization, derivative order, density convention, and boundary class", "GENERAL_TEMPLATE_DERIVED_NOT_PARENT_SELECTED", "defines the upstream object needed for Q_R, B_R, K_boundary, and no-hair identities"),
        ("TPR2247_1_first_derivative", "first-derivative template", "Theta_R^mu(delta Y)=Pi_A^mu delta Y^A, Pi_A^mu := partial L_R / partial(nabla_mu Y^A)", "L_R has no higher derivatives or higher-derivative boundary terms have been reduced by auxiliary fields", "FORMULA_READY_LR_MISSING", "turns a chosen L_R into a computable symplectic potential"),
        ("TPR2247_2_finite_jet", "higher finite-jet template", "Theta_R^mu=sum_{r=0}^{N-1} Pi_A^{mu alpha_1...alpha_r} nabla_{alpha_1}...nabla_{alpha_r} delta Y^A", "finite derivative order N and all corner/counterterm conventions are declared", "FORMULA_READY_FINITE_JET_ORDER_MISSING", "fixes which epsilon_R jets must vanish for proper boundary silence"),
        ("TPR2247_3_Noether_PR", "P_R from vertical generator", "insert delta_epsilon Y^A=R^A_AB epsilon^AB + R^{A mu}_AB nabla_mu epsilon^AB + ... into Theta_R; P_R^{mu AB} is the coefficient package whose divergence enters C_R^AB", "v_R action on every parent field and tensor/density convention for C_R are fixed", "CONTRACT_READY_FIELD_ACTION_AND_CONVENTION_MISSING", "connects Theta_R to B_R^AB=sigma n_mu P_R^{mu AB}+..."),
        ("TPR2247_4_positive_RAB_example", "minimal positive tensor-residual example", "L_R=-1/2 Z_R <nabla R,nabla R> -1/2 M_R^2 <R,R> + <J_R,R> gives Theta_R^mu=-Z_R <nabla^mu R,delta R> plus projector terms", "R_AB really is the retained local amplitude, Z_R>0, M_R^2>0, J_R and boundary data are source-owned", "EXAMPLE_ONLY_NOT_SELECTED", "if J_R=0 and boundary flux=0, no-hair can set R_AB=0; otherwise alpha(lambda) is live"),
        ("TPR2247_5_verdict", "Theta_R/P_R owner status", "Theta_R/P_R template is mathematically ready, but no parent R_AB block is selected or proved", "one candidate in RC2247 closes its owner gates", "FAIL_CURRENT_CLAIM_THETAR_PR_NOT_PARENT_OWNED", "use nonclaim priors/templates for boundary coefficients until a parent block is signed"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "template_id": template_id,
            "object": obj,
            "formula": formula,
            "owned_if": owned_if,
            "current_status": status,
            "claim_effect": effect,
            **flags(),
        }
        for template_id, obj, formula, owned_if, status, effect in rows
    ]


def owner_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("TOG2247_0_parent_route", "select one parent R_AB route", "absent quotient, first-class vertical constraint, positive sourcefree field, or sourced residual is chosen before scoring", "ROUTE_NOT_PARENT_SELECTED", "Theta_R/P_R remain a menu rather than an action"),
        ("TOG2247_1_field_content", "field list and transformation law", "Y_R^A and delta_epsilon Y_R^A are declared for metric/coframe, R_AB, extra modes, domain/memory, matter, and boundary fields", "FIELD_ACTION_INCOMPLETE", "P_R cannot be computed from Theta_R"),
        ("TOG2247_2_operator_signs", "positive/no-pole or residual operator", "Z_R, M_R^2, Hessian signs, or first-class rank/degree count are derived", "OPERATOR_SIGNS_MISSING", "local-GR reduction cannot tell no-hair from hidden dynamics"),
        ("TOG2247_3_source_zero", "source/test blindness", "J_R=0, qbar_RT=0, Qbar_RH=0, or bounded coefficient rows are sourced channelwise", "SOURCE_ZERO_OR_BOUND_MISSING", "R10/WEP/clock/PPN/orbital residual rows remain live"),
        ("TOG2247_4_boundary_flux", "boundary no-flux or coefficient row", "Phi_boundary_local=0 theorem or alpha3/R10 boundary coefficients are source-backed", "BOUNDARY_FLUX_ZERO_OR_BOUND_MISSING", "K_boundary_alpha3 and edge R10 templates remain nonclaim"),
        ("TOG2247_5_verdict", "claim-grade Theta_R/P_R owner", "TOG2247_0 through TOG2247_4 pass together", "FAIL_CURRENT_CLAIM_THETAR_PR_OWNER_MISSING", "demote to nonclaim coefficient priors/templates"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "needed": needed,
            "test": test,
            "current_status": status,
            "if_missing": missing,
            **flags(),
        }
        for gate_id, needed, test, status, missing in rows
    ]


def noflux_rows() -> list[dict[str, Any]]:
    rows = [
        ("NFR2247_0_positive_energy", "positive source-free operator", "int_A <R,L_R R> = positive_norm[R] + Phi_boundary_local", "positive_norm plus Phi_boundary_local=0 plus J_R=0 forces R_AB=0 modulo pure gauge/topological class", "L_R, sign proof, source-zero, boundary flux theorem, allowed topology", "PROMISING_NOT_PARENT_SIGNED"),
        ("NFR2247_1_topological_exact", "topological/exact boundary sector", "L_boundary=dB or class-only topological density with no local metric/source variation", "edge flux is fixed background subtraction or exact on the certified boundary class", "boundary class owner, harmonic/corner control, reference subtraction", "ROUTE_OPEN_NOT_CLOSED"),
        ("NFR2247_2_first_class_constraint", "constraint/gauge no-pole", "Omega_flat(v_R)=delta C_R and Q_R=K_boundary=0 on the relevant local branch", "no physical R_AB Green function exists and no source/test marker sees R_AB", "parent Omega, D C_R, bracket, degree count, matter descent", "ROUTE_OPEN_NOT_CLOSED"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": route_id,
            "route": route,
            "identity": identity,
            "zero_condition": zero,
            "missing": missing,
            "current_status": status,
            **flags(),
        }
        for route_id, route, identity, zero, missing, status in rows
    ]


def prior_rows() -> list[dict[str, Any]]:
    rows = [
        ("BCP2247_0_K_boundary_alpha3", "K_boundary_alpha3", "alpha3", "if Phi_boundary_local is sourced and nonzero, |K_boundary_alpha3| <= 4e-20/|Phi_boundary_local|", "4e-20", "Phi_boundary_local numeric/source-backed or theorem-zero; normalization; uncertainty policy", "NONCLAIM_PRIOR_SCHEMA_READY_INPUTS_MISSING"),
        ("BCP2247_1_Phi_boundary_local", "Phi_boundary_local", "alpha3;R10;Gdot", "Phi_boundary_local=0 by no-flux theorem, or numeric amplitude with units and source path", "theorem-zero or observable-specific bounds", "boundary norm, surface, units, time/source normalization, topology/corner policy", "NONCLAIM_PRIOR_SCHEMA_READY_INPUTS_MISSING"),
        ("BCP2247_2_edge_R10_coefficients", "K_edge;Qbar_edge_RH;qbar_RT", "alpha_R10(lambda)", "|alpha_edge|=|K_edge Qbar_edge_RH qbar_RT| must be <= alpha_bound(lambda) after curve promotion", "review-candidate alpha_bound(lambda) only", "K_edge(lambda), Qbar_edge_RH(lambda), qbar_RT, lambda support, promoted bound curve", "NONCLAIM_PRIOR_SCHEMA_READY_INPUTS_MISSING"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "prior_id": prior_id,
            "coefficient": coefficient,
            "observable": observable,
            "prior_or_bound_rule": rule,
            "anchor_bound": anchor,
            "required_inputs": required,
            "current_status": status,
            **flags(),
        }
        for prior_id, coefficient, observable, rule, anchor, required, status in rows
    ]


def action_selection_rows() -> list[dict[str, Any]]:
    rows = [
        ("SEL2247_0_do_not_select_yet", "Do not select a public parent R_AB action at 2247.", "the corpus has candidate routes but no source file proving the required L_R/Theta_R/P_R package", "use the templates as contracts for the next derivation step"),
        ("SEL2247_1_best_derivation_next", "Best next derivation is the positive/nohair or first-class-constraint owner route, not a sourced residual fit.", "those are the only routes that can genuinely reduce to local GR rather than merely survive empirical bounds", "try to close source-free energy identity or first-class momentum-map owner before coefficient priors"),
        ("SEL2247_2_fallback_prior", "If the owner route stalls, use alpha3/R10 coefficient priors as private diagnostic scaffolding.", "the exact inequality is known, but numeric K/Phi values would be invented today", "nonclaim rows only"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "selection_id": selection_id,
            "decision": decision,
            "reason": reason,
            "safe_use": safe_use,
            **flags(),
        }
        for selection_id, decision, reason, safe_use in rows
    ]


def alpha_template_rows() -> list[dict[str, Any]]:
    rows = [
        ("MTS_source_normalized_Newton_branch", "ThetaR_PR_owner_contract", "MISSING_PARENT_ROUTE", "MISSING_PARENT_THETAR_PR_OWNER", "Theta_R/P_R determine B_R, Q_R, K_boundary, and any edge alpha(lambda)", "template_invalid_parent_route_not_selected"),
        ("MTS_source_normalized_Newton_branch", "positive_nohair_zero_template", "MISSING_ZR_MR_RATIO", "MISSING_JR_ZERO_AND_BOUNDARY_FLUX_ZERO", "if Z_R>0, M_R^2>0, J_R=0, Phi_boundary=0, then R_AB=0 by energy identity", "template_invalid_operator_and_source_zero_missing"),
        ("MTS_source_normalized_Newton_branch", "alpha3_coefficient_prior_template", "MISSING_NOT_R10_RANGE", "MISSING_K_BOUNDARY_ALPHA3_PHI_BOUNDARY_LOCAL", "|K_boundary_alpha3 Phi_boundary_local| <= 4e-20", "template_invalid_prior_inputs_missing"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "model_id": model,
            "template_branch": template,
            "lambda_value": lambda_value,
            "alpha_predicted": alpha,
            "force_law_form": law,
            "derivation_status": status,
            **flags(),
        }
        for model, template, lambda_value, alpha, law, status in rows
    ]


def runner_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "smoke_id": "SMOKE2247_0_runner_status",
            "valid_mts_rows": 0,
            "valid_bound_rows": 0,
            "comparison_rows": 1,
            "R10_pass_for_claim": False,
            "expected_result": "blocked_nonclaim",
            **flags(),
        }
    ]


def refusal_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in candidate_rows():
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "refusal_id": row["candidate_id"].replace("RC2247", "REF2247_RC"),
                "object": row["parent_route"],
                "current_status": row["current_status"],
                "refusal_status": "candidate_not_parent_selected",
                "failure_reasons": row["risk"],
                "score_eligible": False,
                **flags(),
            }
        )
    for row in template_rows():
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "refusal_id": row["template_id"].replace("TPR2247", "REF2247_TPR"),
                "object": row["object"],
                "current_status": row["current_status"],
                "refusal_status": "ThetaR_PR_template_not_claim_promoted",
                "failure_reasons": row["owned_if"],
                "score_eligible": False,
                **flags(),
            }
        )
    for row in owner_gate_rows():
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "refusal_id": row["gate_id"].replace("TOG2247", "REF2247_TOG"),
                "object": row["needed"],
                "current_status": row["current_status"],
                "refusal_status": "owner_gate_failed",
                "failure_reasons": row["if_missing"],
                "score_eligible": False,
                **flags(),
            }
        )
    for row in prior_rows():
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "refusal_id": row["prior_id"].replace("BCP2247", "REF2247_BCP"),
                "object": row["coefficient"],
                "current_status": row["current_status"],
                "refusal_status": "coefficient_prior_not_scoreable",
                "failure_reasons": row["required_inputs"],
                "score_eligible": False,
                **flags(),
            }
        )
    return rows


def claim_rows() -> list[dict[str, Any]]:
    rows = [
        ("CGATE2247_0_parent_R_owner", "parent R_AB-sector action owns Theta_R/P_R", False, "candidate routes are ranked and templates are written, but no L_R/field-content/operator/source/boundary package is parent-selected"),
        ("CGATE2247_1_local_GR_reduction", "local GR/no-pole branch follows from the R_AB sector", False, "absent-quotient/first-class/no-hair routes remain unsigned; sourced residual route is not a derivation of GR"),
        ("CGATE2247_2_alpha3_prior", "alpha3 coefficient prior is executable", False, "K_boundary_alpha3 and Phi_boundary_local remain missing"),
        ("CGATE2247_3_R10", "R10 edge/bulk alpha(lambda) is score-ready", False, "K_edge/K_R, Qbar, qbar, lambda support, and promoted bound curve remain missing"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "claim": claim,
            "gate_pass": gate_pass,
            "reason": reason,
            **flags(),
        }
        for gate_id, claim, gate_pass, reason in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC2247_0_parent_route_status",
            "decision": "Do not pretend a parent R_AB action is selected yet.",
            "because": "2247 derives the generic Theta_R/P_R machinery but does not find a source file proving any candidate route",
            "next_action": "attack the positive/nohair source-zero route or first-class momentum-map route directly",
            **flags(),
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC2247_1_best_route",
            "decision": "Best derivation route remains absent/quotient or first-class constraint; best fallback route is positive source-free no-hair.",
            "because": "these can actually reduce to local GR, while sourced residuals only build a testable fifth-force branch",
            "next_action": "derive the source-free positive operator identity with J_R=0 and Phi_boundary=0, or close the first-class constraints",
            **flags(),
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC2247_2_next_target",
            "decision": "Next target should test the source-free positive operator/no-hair route.",
            "because": "it is the most concrete route that can convert Theta_R/P_R templates into a real local-GR reduction without inventing coefficients",
            "next_action": "2248-Y5-R2FR-RAB-sourcefree-positive-RAB-nohair-identity-or-alpha3-prior-first-fill.md",
            **flags(),
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "next_target": "2248-Y5-R2FR-RAB-sourcefree-positive-RAB-nohair-identity-or-alpha3-prior-first-fill.md",
            "script": "scripts/Y5_R2FR_RAB_sourcefree_positive_RAB_nohair_identity_or_alpha3_prior_first_fill_2248.py",
            "objective": "try to derive the source-free positive R_AB-sector no-hair identity with Z_R>0, M_R^2>0, J_R=0, and Phi_boundary=0; if it fails, build the first nonclaim alpha3 prior row for K_boundary_alpha3 or Phi_boundary_local",
            "include": "positive operator identity, source-zero clauses, boundary flux zero, topology/gauge caveats, Hessian sign gates, alpha3 prior schema",
            "exclude": "invented Z/M/J/K/Phi values, deleting GR charges, naked linear c_g scoring, cancellation between residuals, R10/local-GR pass claim, formalization-workbench edits, GitHub action",
            **flags(),
        }
    ]


def copy_rows() -> list[dict[str, Any]]:
    copy_sources = {
        "queue_theta": THETAR_PR_TEMPLATE,
        "queue_prior": BOUNDARY_COEFFICIENT_PRIOR,
        "branch_wep": BOUNDARY_COEFFICIENT_PRIOR,
        "beta_docs": BOUNDARY_COEFFICIENT_PRIOR,
    }
    rows: list[dict[str, Any]] = []
    for copy_id, source in copy_sources.items():
        target = COPY_TARGETS[copy_id]
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "copy_id": copy_id,
                "source_path": rel(source),
                "target_path": rel(target),
                "copied": target.exists(),
                "parse_ok": parse_csv(target),
                **flags(),
            }
        )
    return rows


def generated_flags_false(paths: list[Path]) -> bool:
    false_values = {"", "false", "0", "no", "none", "null"}
    keys = ["numeric_value_present", "source_backed", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"]
    for path in paths:
        for row in read_csv(path):
            for key in keys:
                if key in row and str(row[key]).strip().lower() not in false_values:
                    return False
    return True


def candidates_ranked() -> bool:
    ranks = [int(row["rank"]) for row in read_csv(PARENT_R_CANDIDATE_CLASSIFIER)]
    return ranks == sorted(ranks) and len(ranks) == 5


def theta_templates_present() -> bool:
    text = " ".join(" ".join(row.values()) for row in read_csv(THETAR_PR_TEMPLATE))
    return "Theta_R" in text and "P_R" in text and "FAIL_CURRENT_CLAIM_THETAR_PR_NOT_PARENT_OWNED" in text


def owner_gates_fail_safely() -> bool:
    return any(row.get("current_status") == "FAIL_CURRENT_CLAIM_THETAR_PR_OWNER_MISSING" for row in read_csv(THETAR_OWNER_GATE))


def nohair_routes_staged() -> bool:
    text = " ".join(" ".join(row.values()) for row in read_csv(NOFLUX_THEOREM_ROUTE))
    return "positive source-free" in text and "PROMISING_NOT_PARENT_SIGNED" in text


def coefficient_priors_nonclaim() -> bool:
    return all(row.get("score_ready", "").lower() == "false" and row.get("valid_for_claim", "").lower() == "false" for row in read_csv(BOUNDARY_COEFFICIENT_PRIOR))


def action_selection_refused() -> bool:
    return any(row.get("selection_id") == "SEL2247_0_do_not_select_yet" for row in read_csv(ACTION_SELECTION))


def claim_gates_blocked() -> bool:
    return all(row.get("gate_pass", "").lower() == "false" and row.get("claim_allowed", "").lower() == "false" for row in read_csv(CLAIM_GATES))


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def formalization_2247_artifacts_absent() -> bool:
    if not FORMALIZATION.exists():
        return True
    return not any(
        path.is_file()
        and "2247" in path.name
        and ".venv" not in path.relative_to(FORMALIZATION).parts
        for path in FORMALIZATION.rglob("*")
    )


def formalization_untouched_since_start() -> bool:
    if not FORMALIZATION.exists():
        return True
    return not any(path.is_file() and path.stat().st_mtime >= START_TS for path in FORMALIZATION.rglob("*"))


def source_register_paths_exist() -> bool:
    return all(resolve_project_path(row["source_path"]).exists() for row in read_csv(SOURCE_REGISTER))


def validation_rows(generated_paths: list[Path]) -> list[dict[str, Any]]:
    rows = [
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2247_00_sources_exist",
            "result": "PASS" if all(path.exists() for path in SOURCE_FILES.values()) and source_register_paths_exist() else "FAIL",
            "detail": "all direct and registered 2247 source paths exist",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2247_01_prior_validations",
            "result": "PASS" if validation_pass(SOURCE_FILES["2246_validation"]) and validation_pass(SOURCE_FILES["1041_validation"]) else "FAIL",
            "detail": "2246 and 1041 validations pass overall",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2247_02_candidates_ranked",
            "result": "PASS" if candidates_ranked() else "FAIL",
            "detail": "parent R_AB candidate routes are ranked without selection",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2247_03_ThetaR_PR_templates",
            "result": "PASS" if theta_templates_present() else "FAIL",
            "detail": "Theta_R/P_R templates are written and not parent-promoted",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2247_04_owner_gates_fail_safely",
            "result": "PASS" if owner_gates_fail_safely() else "FAIL",
            "detail": "owner gates identify missing route, field action, signs, source-zero, and boundary flux",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2247_05_nohair_routes_staged",
            "result": "PASS" if nohair_routes_staged() else "FAIL",
            "detail": "no-hair and constraint routes are staged as nonclaim derivation targets",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2247_06_coefficient_priors_nonclaim",
            "result": "PASS" if coefficient_priors_nonclaim() else "FAIL",
            "detail": "alpha3/R10 coefficient prior templates remain nonclaim",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2247_07_action_selection_refused",
            "result": "PASS" if action_selection_refused() else "FAIL",
            "detail": "no parent action is falsely selected at 2247",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2247_08_mts_template_nonclaim",
            "result": "PASS" if all(row.get("valid_for_claim", "").lower() == "false" for row in read_csv(MTS_ALPHA_TEMPLATE)) else "FAIL",
            "detail": "MTS smoke template has no claim-valid rows",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2247_09_runner_smoke_refuses_claim",
            "result": "PASS" if read_csv(RUNNER_SMOKE)[0].get("expected_result") == "blocked_nonclaim" else "FAIL",
            "detail": "runner smoke status refuses a claim",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2247_10_claim_gates_blocked",
            "result": "PASS" if claim_gates_blocked() else "FAIL",
            "detail": "all local-GR/empirical claim gates remain blocked",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2247_11_next_target_written",
            "result": "PASS" if read_csv(NEXT_TARGET)[0]["next_target"].startswith("2248-Y5-R2FR-RAB-sourcefree-positive") else "FAIL",
            "detail": "next target row is present",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2247_12_csv_parse",
            "result": "PASS" if all(parse_csv(path) for path in generated_paths) else "FAIL",
            "detail": "all generated 2247 CSVs parse cleanly",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2247_13_claim_flags_false",
            "result": "PASS" if generated_flags_false(generated_paths) else "FAIL",
            "detail": "all generated prediction/claim flags remain false",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2247_14_branch_copies",
            "result": "PASS" if all(row["copied"] == "True" and row["parse_ok"] == "True" for row in read_csv(BRANCH_COPIES)) else "FAIL",
            "detail": "branch/quarantine nonclaim copies written",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2247_15_pycache_absent",
            "result": "PASS" if not (ROOT / "scripts" / "__pycache__").exists() else "FAIL",
            "detail": "scripts __pycache__ absent after run",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2247_16_formalization_no_2247",
            "result": "PASS" if formalization_2247_artifacts_absent() else "FAIL",
            "detail": "formalization-workbench has no non-venv 2247 artifacts",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2247_17_formalization_untouched",
            "result": "PASS" if formalization_untouched_since_start() else "FAIL",
            "detail": "formalization-workbench untouched during 2247 run",
        },
    ]
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2247_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "2247 ranks R_AB parent routes, writes Theta_R/P_R templates, refuses action selection, keeps coefficient priors nonclaim, and selects source-free no-hair next",
        }
    )
    return rows


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        values = [str(row.get(column, "")).replace("\n", " ").replace("|", "\\|") for column in columns]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def build_doc(
    source: list[dict[str, Any]],
    candidates: list[dict[str, Any]],
    templates: list[dict[str, Any]],
    owner: list[dict[str, Any]],
    noflux: list[dict[str, Any]],
    priors: list[dict[str, Any]],
    action_selection: list[dict[str, Any]],
    alpha_template: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    refusal: list[dict[str, Any]],
    claim: list[dict[str, Any]],
    decision: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    copies: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> str:
    return "\n\n".join(
        [
            "# 2247 - Y5/R2FR R_AB Parent R-Sector Theta_R/P_R Owner or Boundary Coefficient Prior",
            "## Verdict\n"
            "- 2247 makes the parent-action menu explicit for the `R_AB` boundary sector: `Theta_R` and `P_R` can be computed once a lawful `L_R` route is selected.\n"
            "- No parent `L_R`, `Theta_R`, or `P_R` owner is selected here. The templates are contracts, not claims.\n"
            "- Best derivation routes remain absent/quotient or first-class constraint; best concrete fallback is positive source-free no-hair. A sourced residual is empirical, not a GR derivation.\n"
            "- Alpha3/R10 coefficient priors remain private nonclaim scaffolding.",
            "## Source Register\n"
            + md_table(source, ["source_id", "source_path", "path_exists", "validation_overall_pass", "role"]),
            "## Parent R_AB Candidate Classifier\n"
            + md_table(candidates, ["candidate_id", "parent_route", "ThetaR_PR_result", "boundary_result", "risk", "rank", "current_status"]),
            "## Theta_R/P_R Template Contract\n"
            + md_table(templates, ["template_id", "object", "formula", "owned_if", "current_status", "claim_effect"]),
            "## Theta_R Owner Gate\n"
            + md_table(owner, ["gate_id", "needed", "test", "current_status", "if_missing"]),
            "## No-Flux Theorem-Zero Route\n"
            + md_table(noflux, ["route_id", "route", "identity", "zero_condition", "missing", "current_status"]),
            "## Boundary Coefficient Prior Template\n"
            + md_table(priors, ["prior_id", "coefficient", "observable", "prior_or_bound_rule", "anchor_bound", "required_inputs", "current_status"]),
            "## Action Selection Decision\n"
            + md_table(action_selection, ["selection_id", "decision", "reason", "safe_use"]),
            "## MTS Alpha Smoke Template\n"
            + md_table(alpha_template, ["model_id", "template_branch", "lambda_value", "alpha_predicted", "force_law_form", "derivation_status"]),
            "## Runner Smoke Status\n"
            + md_table(runner, ["smoke_id", "valid_mts_rows", "valid_bound_rows", "comparison_rows", "R10_pass_for_claim", "claim_allowed", "expected_result"]),
            "## Placeholder Refusal Runner\n"
            + md_table(refusal, ["refusal_id", "object", "current_status", "refusal_status", "failure_reasons", "score_eligible", "claim_allowed"]),
            "## Claim Gates\n"
            + md_table(claim, ["gate_id", "claim", "gate_pass", "reason", "claim_allowed"]),
            "## Decision Ledger\n"
            + md_table(decision, ["decision_id", "decision", "because", "next_action"]),
            "## Next Target\n"
            + md_table(next_target, ["next_target", "script", "objective", "include", "exclude"]),
            "## Branch Copies\n"
            + md_table(copies, ["copy_id", "source_path", "target_path", "copied", "parse_ok"]),
            "## Validation\n"
            + md_table(validation, ["check_id", "result", "detail"]),
            "## Working Interpretation\n\n"
            "We now have the right upstream object list. The next honest leap is not a fitted boundary number; it is the positive/source-free no-hair identity for the `R_AB` sector. "
            "If `Z_R>0`, `M_R^2>0`, `J_R=0`, and `Phi_boundary=0` can be owned together, local GR gets a real derivation route. "
            "If not, the same table tells us exactly which coefficient priors remain empirical.",
            "",
        ]
    )


def main() -> None:
    source = source_rows()
    candidates = candidate_rows()
    templates = template_rows()
    owner = owner_gate_rows()
    noflux = noflux_rows()
    priors = prior_rows()
    action_selection = action_selection_rows()
    alpha_template = alpha_template_rows()
    runner = runner_rows()
    refusal = refusal_rows()
    claim = claim_rows()
    decision = decision_rows()
    next_target = next_target_rows()

    write_csv(SOURCE_REGISTER, source)
    write_csv(PARENT_R_CANDIDATE_CLASSIFIER, candidates)
    write_csv(THETAR_PR_TEMPLATE, templates)
    write_csv(THETAR_OWNER_GATE, owner)
    write_csv(NOFLUX_THEOREM_ROUTE, noflux)
    write_csv(BOUNDARY_COEFFICIENT_PRIOR, priors)
    write_csv(ACTION_SELECTION, action_selection)
    write_csv(MTS_ALPHA_TEMPLATE, alpha_template)
    write_csv(RUNNER_SMOKE, runner)
    write_csv(PLACEHOLDER_REFUSAL, refusal)
    write_csv(CLAIM_GATES, claim)
    write_csv(DECISION, decision)
    write_csv(NEXT_TARGET, next_target)
    copies = copy_rows()
    write_csv(BRANCH_COPIES, copies)

    remove_pycache()
    generated_before_validation = [path for path in GENERATED if path != VALIDATION]
    validation = validation_rows(generated_before_validation)
    write_csv(VALIDATION, validation)
    remove_pycache()

    DOC.write_text(
        build_doc(
            source,
            candidates,
            templates,
            owner,
            noflux,
            priors,
            action_selection,
            alpha_template,
            runner,
            refusal,
            claim,
            decision,
            next_target,
            copies,
            validation,
        ),
        encoding="utf-8",
    )

    if not validation_pass(VALIDATION):
        raise SystemExit(f"2247 validation failed: {VALIDATION}")


if __name__ == "__main__":
    main()
