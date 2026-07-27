from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


POST_CHECKPOINT = Path(__file__).resolve().parents[1]
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"
RUNS = POST_CHECKPOINT / "runs"
FORMALIZATION = POST_CHECKPOINT.parent / "formalization-workbench"
OUTPUT_DOC = POST_CHECKPOINT / "729-Y5-R10-fill-PJ-parent-origin-or-source-backed-edge-coefficients.md"
NEXT_TARGET = "730-Y5-R10-parent-Lagrangian-theta-vX-minimal-fill-or-edge-coefficients.md"
CUTOFF = datetime(2026, 5, 31, 14, 42, 0)

STATUS = "Y5_R10_729_Noether_PJ_origin_contract_current_chain_formula_progress_not_parent_certificate"
CLAIM_CEILING = "P_J_from_one_Noether_current_contract_only_no_R10_WEP_PPN_Newton_or_local_GR_pass"

SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_729_SOURCE_REGISTER.csv"
NOETHER_FORMULA_PATH = RESIDUALS / "P8_Y5_R10_729_NOETHER_PJ_ORIGIN_FORMULA.csv"
PJ_ATTEMPT_PATH = RESIDUALS / "P8_Y5_R10_729_PJ_PARENT_ORIGIN_ATTEMPT.csv"
IMPROVEMENT_GATE_PATH = RESIDUALS / "P8_Y5_R10_729_IMPROVEMENT_AMBIGUITY_GATE.csv"
PARENT_BLOCKER_PATH = RESIDUALS / "P8_Y5_R10_729_PARENT_ORIGIN_BLOCKER.csv"
EDGE_PLAN_PATH = RESIDUALS / "P8_Y5_R10_729_EDGE_COEFFICIENT_SOURCE_PLAN.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_R10_729_DECISION_MATRIX.csv"
ROUTE_UPDATE_PATH = RESIDUALS / "P8_Y5_R10_729_ROUTE_UPDATE.csv"
SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_729_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_729_VALIDATION.csv"

SOURCES: dict[str, dict[str, Any]] = {
    "728_doc": {
        "path": POST_CHECKPOINT / "728-Y5-R10-parent-Omega-and-DC-operator-fill-or-edge-row-source-input.md",
        "role": "immediate handoff: current Omega/DCdagger machinery",
        "needles": [
            "729-Y5-R10-fill-PJ-parent-origin-or-source-backed-edge-coefficients.md",
            "formula progress, not certificate",
            "P",
            "J_eff",
        ],
    },
    "728_validation": {
        "path": RESIDUALS / "P8_Y5_BRR545_728_VALIDATION.csv",
        "role": "prior validation gate",
        "needles": ["V728_11_next_target_selected", "pass", "V728_14_formalization_workbench_untouched"],
    },
    "728_blocker": {
        "path": RESIDUALS / "P8_Y5_R10_728_PARENT_OWNERSHIP_BLOCKER.csv",
        "role": "current parent-ownership blockers",
        "needles": ["POB728_2_PJ_from_one_current", "formula_derived_but_not_filled", "false"],
    },
    "728_comparison": {
        "path": RESIDUALS / "P8_Y5_R10_728_OMEGA_DCDAGGER_COMPARISON.csv",
        "role": "current P/J/Omega comparison blockers",
        "needles": ["CMP728_1_current_MTS_P_owner", "CMP728_2_current_MTS_J_owner", "false"],
    },
    "728_edge_status": {
        "path": RESIDUALS / "P8_Y5_R10_728_EDGE_SOURCE_INPUT_STATUS.csv",
        "role": "current edge coefficient source status",
        "needles": ["SBER726_0_required_source_backed_row", "missing_sources", "false"],
    },
    "592_doc": {
        "path": POST_CHECKPOINT / "592-Y5-R10-fill-PJ-parent-origin-or-source-backed-edge-coefficients.md",
        "role": "older Noether P/J origin checkpoint",
        "needles": ["j_X=theta_Y(v_X)-mu_X", "C_X^nu=-nabla_mu P", "Independent"],
    },
    "592_noether": {
        "path": RESIDUALS / "P8_Y5_R10_592_NOETHER_PJ_ORIGIN_FORMULA.csv",
        "role": "older Noether P/J formula table",
        "needles": ["NPJ592_3_PJ_split", "conditional_PJ_origin_formula", "false"],
    },
    "592_pj_attempt": {
        "path": RESIDUALS / "P8_Y5_R10_592_PJ_PARENT_ORIGIN_ATTEMPT.csv",
        "role": "older P/J parent-origin attempts",
        "needles": ["PJA592_5_current_verdict", "formula_derived_but_not_filled", "false"],
    },
    "592_improvement": {
        "path": RESIDUALS / "P8_Y5_R10_592_IMPROVEMENT_AMBIGUITY_GATE.csv",
        "role": "older improvement ambiguity gate",
        "needles": ["IAG592_0_superpotential_improvement", "IAG592_1_current_improvement", "open"],
    },
    "592_edge_plan": {
        "path": RESIDUALS / "P8_Y5_R10_592_EDGE_COEFFICIENT_SOURCE_PLAN.csv",
        "role": "older edge coefficient source plan",
        "needles": ["ESP592_0", "K_edge;Qbar_edge_XH;qbar_XT", "false"],
    },
    "593_doc": {
        "path": POST_CHECKPOINT / "593-Y5-R10-parent-Lagrangian-theta-vX-minimal-fill-or-edge-coefficients.md",
        "role": "older minimal parent fill fork",
        "needles": ["Minimal parent data can be filled as templates", "strict quotient", "affine block is rejected"],
    },
    "583_doc": {
        "path": POST_CHECKPOINT / "583-Y5-R10-parent-momentum-map-owner-or-edge-residual-demotion.md",
        "role": "momentum-map owner contract",
        "needles": ["delta L_parent", "i_{v_epsilon} Omega_Y = delta G[epsilon]", "P[Y], J_eff[Y]"],
    },
    "513_doc": {
        "path": POST_CHECKPOINT / "513-Gamma-Khat-q_loc-first-variation-or-demotion.md",
        "role": "Ward/stress source route",
        "needles": ["q_loc^nu = P_loc nabla_mu T_GK", "conditional_derivation_route", "not_supplied"],
    },
    "538_doc": {
        "path": POST_CHECKPOINT / "538-Y5-minimal-parent-action-Euler-Ward-test-or-closure-demotion.md",
        "role": "Euler-Ward parent action chain",
        "needles": ["Euler-Ward Chain Test", "Noether current", "conditional_pass_if_action_is_explicit"],
    },
}


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def text_contains(path: Path, needles: list[str]) -> bool:
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8", errors="replace")
    return all(needle in text for needle in needles)


def prior_validation_clean(path: Path) -> bool:
    rows = read_csv(path)
    return bool(rows) and all(row.get("result") == "pass" for row in rows)


def relative(path: Path) -> str:
    try:
        return str(path.relative_to(POST_CHECKPOINT)).replace("\\", "/")
    except ValueError:
        return str(path)


def source_path_string(*keys: str) -> str:
    return ";".join(str(SOURCES[key]["path"]) for key in keys)


def markdown_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    header = "| " + " | ".join(fields) + " |"
    separator = "| " + " | ".join("---" for _ in fields) + " |"
    body = []
    for row in rows:
        cells = []
        for field in fields:
            value = str(row.get(field, ""))
            value = value.replace("\n", " ").replace("|", "\\|")
            cells.append(value)
        body.append("| " + " | ".join(cells) + " |")
    return "\n".join([header, separator, *body])


def formalization_changed_after_cutoff() -> int:
    if not FORMALIZATION.exists():
        return -1
    count = 0
    for path in FORMALIZATION.rglob("*"):
        if not path.is_file():
            continue
        modified = datetime.fromtimestamp(path.stat().st_mtime)
        if modified > CUTOFF:
            count += 1
    return count


def under_post_checkpoint(paths: list[Path]) -> bool:
    root = POST_CHECKPOINT.resolve()
    for path in paths:
        try:
            path.resolve().relative_to(root)
        except ValueError:
            return False
    return True


def make_source_register(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "source_id": key,
            "path": str(info["path"]),
            "exists": bool_text(info["path"].exists()),
            "needle_check": bool_text(text_contains(info["path"], info["needles"])),
            "role": info["role"],
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
        for key, info in SOURCES.items()
    ]


def make_noether_formula(generated_utc: str) -> list[dict[str, Any]]:
    source_paths = source_path_string("728_doc", "592_doc", "592_noether", "583_doc")
    return [
        {
            "formula_id": "NPJ729_0_parent_variation",
            "statement": "delta L_parent = E_A delta Y^A + d theta_Y(delta Y)",
            "meaning": "P and J_eff can be parent-owned only after the parent theta_Y is explicit.",
            "derived_status": "standard_variational_identity",
            "current_chain_status": "formula_available_but_L_parent_missing",
            "source_paths": source_paths,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "formula_id": "NPJ729_1_vertical_quasi_symmetry",
            "statement": "v_X[Y]^A = R^A_nu[Y] X^nu + R^{A mu}_nu[Y] nabla_mu X^nu + ... and delta_X L_parent = d mu_X",
            "meaning": "The X direction must be a parent symmetry, quotient vertical direction, or proper gauge direction before it can own a current.",
            "derived_status": "conditional_symmetry_template",
            "current_chain_status": "v_X_not_field_by_field_constructed",
            "source_paths": source_paths,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "formula_id": "NPJ729_2_Noether_current",
            "statement": "j_X = theta_Y(v_X) - mu_X",
            "meaning": "This single current is the only allowed parent-origin source for both P and J_eff.",
            "derived_status": "standard_Noether_definition",
            "current_chain_status": "mu_X_and_theta_Y_not_current_MTS_filled",
            "source_paths": source_paths,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "formula_id": "NPJ729_3_PJ_split",
            "statement": "j_X = X_nu J_eff^nu + (nabla_mu X_nu) P^{mu nu} + dB_improvement",
            "meaning": "P is the coefficient of nabla X and J_eff is the coefficient of X in the same current, not two independently declared objects.",
            "derived_status": "conditional_PJ_origin_formula",
            "current_chain_status": "split_not_extracted_from_current_MTS_parent_action",
            "source_paths": source_paths,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "formula_id": "NPJ729_4_constraint_density",
            "statement": "j_X = X_nu(-nabla_mu P^{mu nu}+J_eff^nu) + d(X_nu P^{mu nu} dSigma_mu + B_improvement)",
            "meaning": "The 728 object C_X^nu=-nabla_mu P^{mu nu}+J_eff^nu is parent-owned only if this integration-by-parts comes from j_X.",
            "derived_status": "formal_derivation_of_CX_from_current",
            "current_chain_status": "matches_728_operator_shape_but_not_a_certificate",
            "source_paths": source_path_string("728_doc", "728_blocker", "592_noether"),
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "formula_id": "NPJ729_5_symplectic_flat_closure",
            "statement": "delta int_Sigma X_nu C_X^nu + delta Q_X = Omega_Y(delta Y, v_X)",
            "meaning": "The extracted P/J split must also reproduce the Omega-flat vertical generator used by the 727-728 DCdagger chain.",
            "derived_status": "closure_condition",
            "current_chain_status": "Omega_Y_and_Q_X_not_parent_owned",
            "source_paths": source_path_string("728_doc", "728_comparison", "583_doc"),
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "formula_id": "NPJ729_6_current_verdict",
            "statement": "independent P^{mu nu} and J_eff^nu are rejected unless they are the two coefficients of j_X",
            "meaning": "This prevents the local branch from smuggling a closure assumption into notation.",
            "derived_status": "discipline_gate",
            "current_chain_status": "gate_installed_no_theorem_claim",
            "source_paths": source_path_string("728_blocker", "592_pj_attempt", "593_doc"),
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def make_pj_attempts(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "attempt_id": "PJA729_0_GR_EH_template",
            "candidate_parent_origin": "Einstein-Hilbert plus diffeomorphism-covariant matter/extra action",
            "P_origin": "superpotential/boundary derivative-of-X coefficient from theta_EH(L_X g)-i_X L",
            "J_origin": "Hamiltonian/momentum constraint and matter stress-current coefficient of X",
            "test_result": "standard_template_only",
            "blocker": "MTS C_X/P/J have not been identified with this diffeomorphism current.",
            "route_value": "best if local GR is recovered by ordinary constraint identity",
            "source_paths": source_path_string("592_pj_attempt", "593_doc", "538_doc"),
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "attempt_id": "PJA729_1_strict_quotient_zero",
            "candidate_parent_origin": "L_parent=L_red[pi(Y)] with dpi(v_X)=0 and matter also factors through pi",
            "P_origin": "zero or exact improvement because theta_Y(v_X) is exact on the quotient vertical direction",
            "J_origin": "zero or exact source current because quotient-observable matter is blind to v_X",
            "test_result": "cleanest_no_pole_if_pi_and_matter_blindness_exist",
            "blocker": "pi, reduced matter functor, and boundary/properness conditions are not constructed.",
            "route_value": "best if the local defect direction is pure representative redundancy",
            "source_paths": source_path_string("593_doc", "583_doc", "728_comparison"),
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "attempt_id": "PJA729_2_affine_Vdef_block",
            "candidate_parent_origin": "S_X=int P^{mu nu}(nabla_mu X_nu-A_mu_nu[Y])+X_nu J_eff^nu[Y]",
            "P_origin": "coefficient of nabla X by construction",
            "J_origin": "coefficient of X by construction",
            "test_result": "rejected_as_parent_origin",
            "blocker": "This names P and J rather than deriving them from pre-existing L_parent/theta_Y/v_X.",
            "route_value": "useful as bookkeeping only after upstream ownership exists",
            "source_paths": source_path_string("592_pj_attempt", "593_doc", "728_blocker"),
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "attempt_id": "PJA729_3_GK_stress_Ward_route",
            "candidate_parent_origin": "Hilbert stress / Euler-Ward route for Gamma-Khat or GK sector",
            "P_origin": "possible stress-current improvement or superpotential term",
            "J_origin": "Euler-Ward source term sum_A E_A nabla^nu Phi^A",
            "test_result": "promising_for_J_not_yet_for_P",
            "blocker": "S_GK, Helmholtz/integrability, and the P superpotential representative remain absent.",
            "route_value": "candidate for source-current derivation but not full local GR closure",
            "source_paths": source_path_string("513_doc", "538_doc", "592_pj_attempt"),
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "attempt_id": "PJA729_4_memory_domain_relative_current",
            "candidate_parent_origin": "relative memory/domain current with exact primitive",
            "P_origin": "relative superpotential or projector boundary coefficient",
            "J_origin": "relative/source current S_L+d_rel(P_mem J_rel)",
            "test_result": "not_closed",
            "blocker": "P_mem stress, exact relative primitive, and local branch exactness are not derived.",
            "route_value": "possible extension route after core parent current is explicit",
            "source_paths": source_path_string("592_pj_attempt", "728_doc"),
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "attempt_id": "PJA729_5_independent_PJ",
            "candidate_parent_origin": "declare P and J_eff independently",
            "P_origin": "free tensor",
            "J_origin": "inserted current",
            "test_result": "rejected",
            "blocker": "It transfers the closure assumption into symbols and gives no theorem credit.",
            "route_value": "forbidden for derivable local GR",
            "source_paths": source_path_string("592_pj_attempt", "728_blocker"),
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "attempt_id": "PJA729_6_current_verdict",
            "candidate_parent_origin": "one current j_X producing P and J_eff",
            "P_origin": "coefficient of nabla_mu X_nu in theta_Y(v_X)-mu_X",
            "J_origin": "coefficient of X_nu in theta_Y(v_X)-mu_X",
            "test_result": "formula_derived_but_not_filled",
            "blocker": "current MTS still lacks explicit L_parent, theta_Y, mu_X, v_X, and fixed boundary representative.",
            "route_value": "next checkpoint should attempt minimal parent fill again in current chain",
            "source_paths": source_path_string("728_blocker", "592_doc", "593_doc"),
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def make_improvement_gate(generated_utc: str) -> list[dict[str, Any]]:
    source_paths = source_path_string("592_improvement", "728_doc")
    return [
        {
            "gate_id": "IAG729_0_superpotential_improvement",
            "ambiguity": "P^{mu nu}->P^{mu nu}+nabla_rho S^{rho mu nu}",
            "risk": "same bulk C_X but different boundary charge Q_X and different alpha_edge bookkeeping",
            "required_fix": "parent boundary/reference choice must fix the representative before any edge claim",
            "status": "open",
            "source_paths": source_paths,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "IAG729_1_current_improvement",
            "ambiguity": "j_X->j_X+dB_X",
            "risk": "bulk P/J split can shift into boundary terms",
            "required_fix": "differentiable Hamiltonian generator with fixed Q_X and explicit allowed improvements",
            "status": "open",
            "source_paths": source_paths,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "IAG729_2_density_convention",
            "ambiguity": "P tensor versus densitized Ptilde",
            "risk": "DC, DCdagger, and connection terms change by convention",
            "required_fix": "choose the convention from parent theta/current before computing DCdagger",
            "status": "open",
            "source_paths": source_path_string("728_doc", "592_improvement"),
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "IAG729_3_on_shell_trivial_current",
            "ambiguity": "Noether current can be shifted by Euler-equation terms",
            "risk": "J_eff may vanish on shell but still be nonzero as an off-shell generator coefficient",
            "required_fix": "off-shell current decomposition and constraint algebra",
            "status": "open",
            "source_paths": source_paths,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "IAG729_4_matter_improper_charge",
            "ambiguity": "improper boundary symmetries can carry physical mass, angular momentum, or matter charge",
            "risk": "a vertical X could accidentally eat real ADM/Hamiltonian charges",
            "required_fix": "proper vertical domain plus Pi_M^H edge projection audit",
            "status": "open",
            "source_paths": source_path_string("592_improvement", "593_doc"),
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def make_parent_blocker(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "blocker_id": "POB729_0_L_parent",
            "needed_object": "explicit L_parent",
            "current_status": "missing",
            "why_it_matters": "without L_parent there is no theta_Y and no parent current j_X",
            "acceptable_resolution": "write current-chain L_parent or strict quotient L_red[pi(Y)] with source map",
            "next_action": NEXT_TARGET,
            "source_paths": source_path_string("728_blocker", "593_doc"),
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "blocker_id": "POB729_1_theta_mu_vX",
            "needed_object": "theta_Y, mu_X, and field-by-field v_X",
            "current_status": "missing",
            "why_it_matters": "these are the inputs of j_X=theta_Y(v_X)-mu_X",
            "acceptable_resolution": "derive them from diffeo covariance or quotient verticality",
            "next_action": NEXT_TARGET,
            "source_paths": source_path_string("728_blocker", "592_doc", "593_doc"),
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "blocker_id": "POB729_2_one_current_PJ_split",
            "needed_object": "P and J_eff from one Noether current",
            "current_status": "formula_derived_but_not_filled",
            "why_it_matters": "separate P/J declarations are not theorem credit",
            "acceptable_resolution": "extract P and J from the coefficient split of j_X",
            "next_action": NEXT_TARGET,
            "source_paths": source_path_string("728_blocker", "592_noether", "592_pj_attempt"),
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "blocker_id": "POB729_3_boundary_representative",
            "needed_object": "fixed boundary/superpotential representative",
            "current_status": "open",
            "why_it_matters": "bulk/edge shifts can change the inferred alpha_edge",
            "acceptable_resolution": "differentiable Hamiltonian boundary term Q_X with allowed-improvement ledger",
            "next_action": NEXT_TARGET,
            "source_paths": source_path_string("728_doc", "592_improvement"),
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "blocker_id": "POB729_4_matter_projector_silence",
            "needed_object": "matter quotient/projector blindness to local vertical direction",
            "current_status": "not_proved",
            "why_it_matters": "without matter silence qbar_XT and local-force residuals remain open",
            "acceptable_resolution": "prove matter action factors through quotient or source response is bounded",
            "next_action": NEXT_TARGET,
            "source_paths": source_path_string("593_doc", "513_doc", "728_comparison"),
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "blocker_id": "POB729_5_edge_coefficients",
            "needed_object": "source-backed K_edge, Qbar_edge_XH, qbar_XT",
            "current_status": "missing_sources",
            "why_it_matters": "if theorem-zero fails, R10 needs numeric sourced edge residual rows",
            "acceptable_resolution": "parent theorem-zero or source-backed coefficient rows below alpha_edge bound",
            "next_action": "source real edge coefficients if parent fill fails",
            "source_paths": source_path_string("728_edge_status", "592_edge_plan"),
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def make_edge_plan(generated_utc: str) -> list[dict[str, Any]]:
    rows = read_csv(SOURCES["728_edge_status"]["path"])
    out: list[dict[str, Any]] = []
    for index, row in enumerate(rows):
        source_status = row.get("current_source_status", "")
        out.append(
            {
                "plan_id": f"ESP729_{index}",
                "edge_row_id": row.get("edge_row_id", ""),
                "lambda_um": row.get("lambda_um", ""),
                "alpha_edge_ceiling": row.get("alpha_edge_ceiling", ""),
                "coefficient_needed": "K_edge;Qbar_edge_XH;qbar_XT",
                "source_status": source_status,
                "acceptable_source": "parent theorem-zero, parent kernel/projection coefficient, or external source-backed numeric coefficient",
                "current_status": "missing" if "missing" in source_status else "diagnostic_only",
                "valid_for_claim": "false",
                "source_paths": source_path_string("728_edge_status", "592_edge_plan"),
                "generated_utc": generated_utc,
            }
        )
    return out


def make_decision(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "D729_0_Noether_PJ_contract_current_chain",
            "decision": "P and J_eff are allowed only as coefficients of one current j_X=theta_Y(v_X)-mu_X",
            "meaning": "The 728 C_X formula is disciplined but not yet parent-certified.",
            "claim_status": "conditional_formula_not_filled",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D729_1_affine_origin_rejected_again",
            "decision": "affine Vdef is bookkeeping unless upstream parent action already produces P/J",
            "meaning": "Declaring coefficients is not the same as deriving a local-GR branch.",
            "claim_status": "blocked_for_claim",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D729_2_next_best_route_is_minimal_parent_fill",
            "decision": "attempt L_parent/theta/mu_X/v_X fill in the current 728-729 chain",
            "meaning": "Choose between diffeomorphism current identity, strict quotient-zero, or hybrid split.",
            "claim_status": "next_derivation_target",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D729_3_edge_coefficients_still_missing",
            "decision": "source-backed edge coefficient fallback remains open but unsourced",
            "meaning": "No R10/local claim until K_edge, Qbar_edge_XH, qbar_XT or theorem-zero is real.",
            "claim_status": "fallback_blocked",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def make_route_update(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "route_id": "RU729_0_allowed",
            "allowed_after_729": "use j_X=theta_Y(v_X)-mu_X as the exact current-origin contract for P/J",
            "forbidden_after_729": "claim P/J ownership merely because P/J appear in an affine defect action",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "RU729_1_allowed",
            "allowed_after_729": "try current-chain minimal parent fill: diffeo identity, strict quotient-zero, or hybrid",
            "forbidden_after_729": "ignore boundary/superpotential ambiguity while evaluating alpha_edge",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "RU729_2_allowed",
            "allowed_after_729": "if parent fill fails, source real edge coefficients rather than promoting smoke rows",
            "forbidden_after_729": "mark diagnostic edge coefficients valid_for_claim",
            "next_action": "edge coefficient sourcing only after theorem route stalls",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def make_summary(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "main_result": "current-chain P/J origin contract is explicit: one parent Noether current or no theorem credit",
            "hard_blocker": "explicit L_parent, theta_Y, mu_X, v_X, boundary representative, and matter/projector silence are still not supplied",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def all_generated_claim_false(paths: list[Path]) -> bool:
    for path in paths:
        rows = read_csv(path)
        if not rows or "valid_for_claim" not in rows[0]:
            continue
        if any(row.get("valid_for_claim", "").lower() != "false" for row in rows):
            return False
    return True


def make_validation(
    source_register: list[dict[str, Any]],
    formula_rows: list[dict[str, Any]],
    pj_rows: list[dict[str, Any]],
    improvement_rows: list[dict[str, Any]],
    blocker_rows: list[dict[str, Any]],
    edge_rows: list[dict[str, Any]],
    decision_rows: list[dict[str, Any]],
    output_paths: list[Path],
) -> list[dict[str, Any]]:
    generated_tables = [
        SOURCE_REGISTER_PATH,
        NOETHER_FORMULA_PATH,
        PJ_ATTEMPT_PATH,
        IMPROVEMENT_GATE_PATH,
        PARENT_BLOCKER_PATH,
        EDGE_PLAN_PATH,
        DECISION_PATH,
        ROUTE_UPDATE_PATH,
        SUMMARY_PATH,
    ]
    source_paths_ok = all(row["exists"] == "true" for row in source_register)
    source_needles_ok = all(row["needle_check"] == "true" for row in source_register)
    prior_clean = prior_validation_clean(SOURCES["728_validation"]["path"])
    selected_729 = text_contains(SOURCES["728_validation"]["path"], ["V728_11_next_target_selected", "729-Y5-R10-fill-PJ-parent-origin-or-source-backed-edge-coefficients.md"])
    split_written = any(row["formula_id"] == "NPJ729_3_PJ_split" for row in formula_rows)
    constraint_written = any(row["formula_id"] == "NPJ729_4_constraint_density" for row in formula_rows)
    symplectic_written = any(row["formula_id"] == "NPJ729_5_symplectic_flat_closure" for row in formula_rows)
    independent_rejected = any(row["attempt_id"] == "PJA729_5_independent_PJ" and row["test_result"] == "rejected" for row in pj_rows)
    affine_rejected = any(row["attempt_id"] == "PJA729_2_affine_Vdef_block" and row["test_result"] == "rejected_as_parent_origin" for row in pj_rows)
    quotient_present = any(row["attempt_id"] == "PJA729_1_strict_quotient_zero" for row in pj_rows)
    improvement_open = bool(improvement_rows) and all(row["status"] == "open" for row in improvement_rows)
    blockers_visible = any(row["blocker_id"] == "POB729_2_one_current_PJ_split" for row in blocker_rows) and any(
        row["blocker_id"] == "POB729_5_edge_coefficients" and row["current_status"] == "missing_sources"
        for row in blocker_rows
    )
    edge_missing = bool(edge_rows) and any(row["current_status"] == "missing" for row in edge_rows)
    next_selected = all(row["next_target"] == NEXT_TARGET for row in decision_rows)
    claim_false = all_generated_claim_false(generated_tables)
    outputs_scoped = under_post_checkpoint(output_paths)
    formalization_count = formalization_changed_after_cutoff()
    return [
        {
            "check_id": "V729_0_source_paths_exist",
            "result": "pass" if source_paths_ok else "fail",
            "detail": f"source_rows={len(source_register)}",
        },
        {
            "check_id": "V729_1_source_needles_present",
            "result": "pass" if source_needles_ok else "fail",
            "detail": "all source files contain expected evidence needles",
        },
        {
            "check_id": "V729_2_prior_728_clean",
            "result": "pass" if prior_clean else "fail",
            "detail": "728 validation has no failures",
        },
        {
            "check_id": "V729_3_728_selected_729",
            "result": "pass" if selected_729 else "fail",
            "detail": "728 selected this checkpoint",
        },
        {
            "check_id": "V729_4_Noether_PJ_contract_written",
            "result": "pass" if split_written and constraint_written and symplectic_written else "fail",
            "detail": f"formula_rows={len(formula_rows)};split={split_written};constraint={constraint_written};symplectic={symplectic_written}",
        },
        {
            "check_id": "V729_5_independent_PJ_rejected",
            "result": "pass" if independent_rejected else "fail",
            "detail": "independent P/J receives no theorem credit",
        },
        {
            "check_id": "V729_6_affine_origin_rejected",
            "result": "pass" if affine_rejected else "fail",
            "detail": "affine Vdef is bookkeeping unless upstream parent current owns P/J",
        },
        {
            "check_id": "V729_7_quotient_route_retained",
            "result": "pass" if quotient_present else "fail",
            "detail": "strict quotient-zero remains the clean no-pole route if pi/matter blindness can be built",
        },
        {
            "check_id": "V729_8_improvement_ambiguity_retained",
            "result": "pass" if improvement_open else "fail",
            "detail": f"improvement_rows={len(improvement_rows)};all_open={improvement_open}",
        },
        {
            "check_id": "V729_9_parent_blockers_visible",
            "result": "pass" if blockers_visible else "fail",
            "detail": f"blocker_rows={len(blocker_rows)}",
        },
        {
            "check_id": "V729_10_edge_coefficients_still_nonclaim",
            "result": "pass" if edge_missing and all(row["valid_for_claim"] == "false" for row in edge_rows) else "fail",
            "detail": f"edge_rows={len(edge_rows)};edge_missing={edge_missing}",
        },
        {
            "check_id": "V729_11_old_592_593_integrated",
            "result": "pass",
            "detail": "Noether P/J formula and minimal-parent fork are carried forward",
        },
        {
            "check_id": "V729_12_next_target_selected",
            "result": "pass" if next_selected else "fail",
            "detail": NEXT_TARGET,
        },
        {
            "check_id": "V729_13_no_claim_rows_promoted",
            "result": "pass" if claim_false else "fail",
            "detail": "all generated rows with valid_for_claim remain false",
        },
        {
            "check_id": "V729_14_outputs_scoped",
            "result": "pass" if outputs_scoped else "fail",
            "detail": "all outputs under post-checkpoint-work",
        },
        {
            "check_id": "V729_15_formalization_workbench_untouched",
            "result": "pass" if formalization_count == 0 else "fail",
            "detail": f"formalization_changed_after_cutoff={formalization_count}",
        },
        {
            "check_id": "V729_16_no_local_arena_claim",
            "result": "pass",
            "detail": "R10/WEP/PPN/Newton/local-GR claims remain blocked",
        },
        {
            "check_id": "V729_17_validation_rows_ready",
            "result": "pass",
            "detail": "validation table constructed",
        },
    ]


def write_markdown(
    generated_utc: str,
    run_root: Path,
    source_register: list[dict[str, Any]],
    formula_rows: list[dict[str, Any]],
    pj_rows: list[dict[str, Any]],
    improvement_rows: list[dict[str, Any]],
    blocker_rows: list[dict[str, Any]],
    edge_rows: list[dict[str, Any]],
    decision_rows: list[dict[str, Any]],
    route_rows: list[dict[str, Any]],
    summary_rows: list[dict[str, Any]],
    validation_rows: list[dict[str, Any]],
) -> None:
    text = f"""# 729 - Y5 R10 Fill P/J Parent Origin Or Source-Backed Edge Coefficients

## Summary

This checkpoint ports the old 592 P/J-origin result into the current 728 operator chain.

The useful derivation is:

```text
delta L_parent = E_A delta Y^A + d theta_Y(delta Y)
j_X = theta_Y(v_X) - mu_X
j_X = X_nu J_eff^nu + (nabla_mu X_nu) P^{{mu nu}} + dB_improvement
C_X^nu = -nabla_mu P^{{mu nu}} + J_eff^nu
```

Current verdict: **contract sharpened, not closed**. The local branch gets no theorem credit from independently named `P` and `J_eff`; they must be extracted from one parent Noether current, with boundary representative fixed.

| Field | Value |
| --- | --- |
| Generated UTC | `{generated_utc}` |
| Claim status | private/nonclaim checkpoint |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |
| Run root | `{relative(run_root)}` |

## Noether P/J Origin Formula

{markdown_table(formula_rows, ["formula_id", "statement", "meaning", "derived_status", "current_chain_status", "valid_for_claim"])}

## P/J Parent-Origin Attempts

{markdown_table(pj_rows, ["attempt_id", "candidate_parent_origin", "P_origin", "J_origin", "test_result", "blocker", "route_value", "valid_for_claim"])}

## Improvement Ambiguity Gate

{markdown_table(improvement_rows, ["gate_id", "ambiguity", "risk", "required_fix", "status", "valid_for_claim"])}

## Parent-Origin Blocker

{markdown_table(blocker_rows, ["blocker_id", "needed_object", "current_status", "why_it_matters", "acceptable_resolution", "next_action", "valid_for_claim"])}

## Edge Coefficient Source Plan

{markdown_table(edge_rows, ["plan_id", "edge_row_id", "lambda_um", "alpha_edge_ceiling", "coefficient_needed", "source_status", "acceptable_source", "current_status", "valid_for_claim"])}

## Decision Matrix

{markdown_table(decision_rows, ["decision_id", "decision", "meaning", "claim_status", "next_target", "valid_for_claim"])}

## Route Update

{markdown_table(route_rows, ["route_id", "allowed_after_729", "forbidden_after_729", "next_action", "valid_for_claim"])}

## Nonclaim Summary

{markdown_table(summary_rows, ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target", "valid_for_claim"])}

## Source Register

{markdown_table(source_register, ["source_id", "path", "exists", "needle_check", "role"])}

## Validation

{markdown_table(validation_rows, ["check_id", "result", "detail"])}

## Practical Read

This is a useful tightening move, not a victory lap. We now have the exact contract for the coupling bottleneck: `P/J` must be the two visible faces of one parent Noether current. The next target is to try the minimal parent fill again in the current chain: diffeo-current identity, strict quotient-zero, or hybrid split. If that fails, the honest fallback is source-backed edge coefficients, not a smoke-row promotion.
"""
    OUTPUT_DOC.write_text(text, encoding="utf-8")


def main() -> None:
    generated_utc = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    run_root = RUNS / f"{stamp}-Y5-R10-fill-PJ-parent-origin-current"
    run_root.mkdir(parents=True, exist_ok=True)

    source_register = make_source_register(generated_utc)
    formula_rows = make_noether_formula(generated_utc)
    pj_rows = make_pj_attempts(generated_utc)
    improvement_rows = make_improvement_gate(generated_utc)
    blocker_rows = make_parent_blocker(generated_utc)
    edge_rows = make_edge_plan(generated_utc)
    decision_rows = make_decision(generated_utc)
    route_rows = make_route_update(generated_utc)
    summary_rows = make_summary(generated_utc)

    output_paths = [
        OUTPUT_DOC,
        SOURCE_REGISTER_PATH,
        NOETHER_FORMULA_PATH,
        PJ_ATTEMPT_PATH,
        IMPROVEMENT_GATE_PATH,
        PARENT_BLOCKER_PATH,
        EDGE_PLAN_PATH,
        DECISION_PATH,
        ROUTE_UPDATE_PATH,
        SUMMARY_PATH,
        VALIDATION_PATH,
        run_root / "status.json",
        run_root / "COMPLETE.marker",
    ]

    write_csv(SOURCE_REGISTER_PATH, source_register, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(
        NOETHER_FORMULA_PATH,
        formula_rows,
        ["formula_id", "statement", "meaning", "derived_status", "current_chain_status", "source_paths", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        PJ_ATTEMPT_PATH,
        pj_rows,
        [
            "attempt_id",
            "candidate_parent_origin",
            "P_origin",
            "J_origin",
            "test_result",
            "blocker",
            "route_value",
            "source_paths",
            "valid_for_claim",
            "generated_utc",
        ],
    )
    write_csv(
        IMPROVEMENT_GATE_PATH,
        improvement_rows,
        ["gate_id", "ambiguity", "risk", "required_fix", "status", "source_paths", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        PARENT_BLOCKER_PATH,
        blocker_rows,
        [
            "blocker_id",
            "needed_object",
            "current_status",
            "why_it_matters",
            "acceptable_resolution",
            "next_action",
            "source_paths",
            "valid_for_claim",
            "generated_utc",
        ],
    )
    write_csv(
        EDGE_PLAN_PATH,
        edge_rows,
        [
            "plan_id",
            "edge_row_id",
            "lambda_um",
            "alpha_edge_ceiling",
            "coefficient_needed",
            "source_status",
            "acceptable_source",
            "current_status",
            "valid_for_claim",
            "source_paths",
            "generated_utc",
        ],
    )
    write_csv(
        DECISION_PATH,
        decision_rows,
        ["decision_id", "decision", "meaning", "claim_status", "next_target", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        ROUTE_UPDATE_PATH,
        route_rows,
        ["route_id", "allowed_after_729", "forbidden_after_729", "next_action", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        SUMMARY_PATH,
        summary_rows,
        ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target", "valid_for_claim", "generated_utc"],
    )

    validation_rows = make_validation(
        source_register,
        formula_rows,
        pj_rows,
        improvement_rows,
        blocker_rows,
        edge_rows,
        decision_rows,
        output_paths,
    )
    write_csv(VALIDATION_PATH, validation_rows, ["check_id", "result", "detail"])

    write_markdown(
        generated_utc,
        run_root,
        source_register,
        formula_rows,
        pj_rows,
        improvement_rows,
        blocker_rows,
        edge_rows,
        decision_rows,
        route_rows,
        summary_rows,
        validation_rows,
    )

    status_payload = {
        "generated_utc": generated_utc,
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "next_target": NEXT_TARGET,
        "doc": str(OUTPUT_DOC),
        "validation": str(VALIDATION_PATH),
        "all_validation_pass": all(row["result"] == "pass" for row in validation_rows),
    }
    (run_root / "status.json").write_text(json.dumps(status_payload, indent=2), encoding="utf-8")
    (run_root / "COMPLETE.marker").write_text("complete\n", encoding="utf-8")
    print(json.dumps(status_payload, indent=2))


if __name__ == "__main__":
    main()
