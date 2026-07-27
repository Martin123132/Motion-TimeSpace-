from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
PYCACHE = ROOT / "scripts" / "__pycache__"

DOC = ROOT / "3253-Y5-R2FR-parent-ordinary-sector-action-signature-or-C_Tw-component-current-norm-intake-under-AX1090.md"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3253_SOURCE_REGISTER.csv",
    "signature": OUT / "P8_Y5_R2FR_3253_PARENT_ORDINARY_SECTOR_ACTION_SIGNATURE.csv",
    "gap": OUT / "P8_Y5_R2FR_3253_SIGNATURE_CLOSURE_GAP_AUDIT.csv",
    "finite_law": OUT / "P8_Y5_R2FR_3253_CTW_FINITE_GRAM_OPERATOR_LAW.csv",
    "intake": OUT / "P8_Y5_R2FR_3253_CTW_COMPONENT_CURRENT_NORM_INTAKE_SCHEMA.csv",
    "update": OUT / "P8_Y5_R2FR_3253_WEIGHTED_SOURCE_UPDATE.csv",
    "gates": OUT / "P8_Y5_R2FR_3253_CLAIM_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3253_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3253_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_R2FR_3253_VALIDATION.csv",
}

RUN_UTC = datetime.now(timezone.utc).isoformat()


def bool_str(value: bool) -> str:
    return "true" if value else "false"


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_ok(path: Path) -> bool:
    try:
        if not path.exists():
            return False
        read_csv(path)
        return True
    except Exception:
        return False


def parse_ok(path: Path) -> bool:
    if not path.exists():
        return False
    return csv_ok(path) if path.suffix.lower() == ".csv" else True


def evidence(path: Path, needles: list[str], limit: int = 4) -> str:
    if not path.exists():
        return "MISSING_SOURCE"
    lowered = [needle.lower() for needle in needles]
    hits: list[str] = []
    with path.open("r", encoding="utf-8", errors="ignore") as handle:
        for line_number, line in enumerate(handle, start=1):
            low = line.lower()
            if any(needle in low for needle in lowered):
                clean = " ".join(line.strip().split())
                if clean:
                    hits.append(f"L{line_number}:{clean[:240]}")
            if len(hits) >= limit:
                break
    return " | ".join(hits) if hits else "NO_MATCH"


def md_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = [
        "| " + " | ".join(md_escape(row.get(column, "")) for column in columns) + " |"
        for row in rows
    ]
    return "\n".join([header, sep, *body])


def source_register() -> list[dict[str, Any]]:
    specs = [
        (
            "SRC3253_3252_handoff",
            DOC.parent / "3252-Y5-R2FR-parent-action-density-line-owner-or-C_Tw-operator-norm-first-source-row-under-AX1090.md",
            "immediate parent action-density/C_Tw handoff",
            ["NEXT3252_0_3253", "C_Tw", "action-density"],
        ),
        (
            "SRC3253_3252_owner_csv",
            OUT / "P8_Y5_R2FR_3252_PARENT_ACTION_DENSITY_LINE_OWNER_ATTEMPT.csv",
            "single action-density/hbar/measure owner clauses",
            ["ADL3252_0_parent_line", "ADL3252_4_zero_theorem"],
        ),
        (
            "SRC3253_3252_ctw_csv",
            OUT / "P8_Y5_R2FR_3252_CTW_OPERATOR_NORM_SOURCE_ROW.csv",
            "C_Tw operator norm exact definition and RSS bound",
            ["CTW3252_0_operator_definition", "CTW3252_1_component_rss_bound"],
        ),
        (
            "SRC3253_3251_source_prefactor",
            DOC.parent / "3251-Y5-R2FR-source-prefactor-edge-zero-or-same-frame-DJH-residual-first-bound-under-AX1090.md",
            "C_wH zero route and weighted-source bound",
            ["NHE3251_5_CwH_zero", "C_Tw"],
        ),
        (
            "SRC3253_3250_same_frame",
            DOC.parent / "3250-Y5-R2FR-Hilbert-current-eobs-tau-owner-or-source-worldtube-flux-norm-row-under-AX1090.md",
            "same-frame Hilbert-current source package",
            ["SFP3250_3_DJH_zero_if_signed", "J_H"],
        ),
        (
            "SRC3253_1220_doc",
            DOC.parent / "1220-Y5-R10-parent-typed-object-language-signature-or-finite-coupling-closure.md",
            "parent typed object-language signature pressure",
            ["PTOL1220_4_action_scale_measure_owner", "PTOL1220_7_verdict"],
        ),
        (
            "SRC3253_1220_signature",
            OUT / "P8_Y5_R10_1220_PARENT_TYPED_SIGNATURE_ATTEMPT.csv",
            "typed signature clauses for no hidden visible coefficients/source weights",
            ["PTOL1220_1_visible_coefficient_domain", "PTOL1220_3_source_weight_exclusion"],
        ),
        (
            "SRC3253_1230_doc",
            DOC.parent / "1230-Y5-R10-universal-action-scale-measure-owner-theorem-or-finite-delta-w-prior.md",
            "universal action scale and measure owner fork",
            ["UAS1230_0_target", "MDS1230_0_parent_measure_line"],
        ),
        (
            "SRC3253_1230_action_scale",
            OUT / "P8_Y5_R10_1230_ACTION_SCALE_OWNER_THEOREM_ATTEMPT.csv",
            "connected naturality and common-mode absorption",
            ["UAS1230_1_connected_naturality_lemma", "UAS1230_3_measure_owner_extension"],
        ),
        (
            "SRC3253_1230_measure",
            OUT / "P8_Y5_R10_1230_MEASURE_DESCENT_PROOF_STACK.csv",
            "hbar/measure/current descent clauses",
            ["MDS1230_0_parent_measure_line", "MDS1230_3_current_extraction"],
        ),
        (
            "SRC3253_1231_doc",
            DOC.parent / "1231-Y5-R10-parent-matter-category-connectedness-or-source-label-residual-map.md",
            "source-label connectedness and disconnected residual basis",
            ["CMC1231_1_interaction_graph_lemma", "DCW1231_1_leptonic_electron"],
        ),
        (
            "SRC3253_1231_basis",
            OUT / "P8_Y5_R10_1231_DISCONNECTED_COMPONENT_RESIDUAL_BASIS.csv",
            "finite source-weight component basis",
            ["DCW1231_1_leptonic_electron", "DCW1231_4_EM_Coulomb_binding"],
        ),
        (
            "SRC3253_1231_map",
            OUT / "P8_Y5_R10_1231_DELTA_W_COMPONENT_MAP.csv",
            "Delta_w and source residual component map",
            ["DWM1231_2_source_stress_residual", "DWM1231_3_local_source_residual"],
        ),
        (
            "SRC3253_1055_contract",
            OUT / "P8_Y5_R10_1055_PARENT_ACTION_CONTRACT_CANDIDATE.csv",
            "parent action contract candidate",
            ["PAC1055_6_single_parent_action", "PAC1055_4_source_label_forgetting"],
        ),
        (
            "SRC3253_1045_functor",
            OUT / "P8_Y5_R10_1045_PARENT_MATTER_FUNCTOR_SIGNATURE_AUDIT.csv",
            "matter functor/coframe descent signature",
            ["MFS1045_2_matter_bundle_functor", "MFS1045_4_no_shadow_frame"],
        ),
        (
            "SRC3253_1046_shadow",
            OUT / "P8_Y5_R10_1046_NO_SHADOW_FRAME_THEOREM_ATTEMPT.csv",
            "no-shadow-frame conditional theorem",
            ["NSF1046_2_no_extra_frame_slot", "NSF1046_5_verdict"],
        ),
        (
            "SRC3253_1106_min_pack",
            OUT / "P8_Y5_R10_1106_MINIMAL_CLOSURE_PACK.csv",
            "minimal closure pack clauses",
            ["MIN1106_A", "MIN1106_B", "MIN1106_C"],
        ),
        (
            "SRC3253_1722_doc",
            DOC.parent / "1722-Y5-R2FR-parent-action-density-edge-or-CwH-current-norm-bound.md",
            "earlier CwH operator-bound statement",
            ["CWHL1722_1_operator_bound", "CWHL1722_2_component_projection"],
        ),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, role, needles in specs:
        rows.append(
            {
                "source_id": source_id,
                "source_path": str(path),
                "exists": bool_str(path.exists()),
                "parse_ok": bool_str(parse_ok(path)),
                "role": role,
                "evidence_hits": evidence(path, needles),
                "valid_for_claim": "false",
            }
        )
    return rows


def parent_signature_rows() -> list[dict[str, Any]]:
    sigma = (
        "Sigma_ord := (q_loc, e_obs(q_loc), L_action, hbar_parent, dmu_parent, "
        "C_ord, theta_rep, S_ord, J_H extraction, Coeff(O_vis), R_readout)"
    )
    return [
        {
            "signature_id": "POS3253_0_composite_object",
            "claim_piece": "parent ordinary-sector action signature",
            "formal_statement": sigma,
            "derivation_gain": "compresses action line, coefficient domain, matter functor, hbar, measure, current extraction, and readout into one object that can be signed or rejected",
            "current_status": "EXACT_COMPOSITE_CONTRACT_NOT_PARENT_SIGNED",
            "valid_for_claim": "false",
        },
        {
            "signature_id": "POS3253_1_single_density_line",
            "claim_piece": "one ordinary action density",
            "formal_statement": "S_ord = integral_A L_action(q_loc(Phi), e_obs(q), Psi, theta_rep) dmu_parent(q), with species as fields/representations inside L_action rather than separate source-normalization lines",
            "derivation_gain": "a source-only multiplier w_A is no longer a silent external knob; it must be an admissible coefficient or automorphism of Sigma_ord",
            "current_status": "CONDITIONAL_FROM_1055_1220_1230_3252",
            "valid_for_claim": "false",
        },
        {
            "signature_id": "POS3253_2_visible_coefficient_domain",
            "claim_piece": "no hidden visible coefficient morphism",
            "formal_statement": "Coeff(O_vis) subset Inv(q_loc, theta_rep) and Hom(C_hid, Coeff(O_vis)) has no physical target for alpha, masses, clocks, source weights, or material markers",
            "derivation_gain": "kills f(I_hid)F^2, m_A(I_hid), clock(I_hid), and w_A(I_hid) as typed parent terms if signed",
            "current_status": "POWERFUL_RULE_STILL_UNSIGNED",
            "valid_for_claim": "false",
        },
        {
            "signature_id": "POS3253_3_matter_functor_and_no_shadow_frame",
            "claim_piece": "ordinary matter descends through observed coframe",
            "formal_statement": "Psi_A in Gamma(E_A[e_obs]); S_A = S_A[Psi_A, e_obs, omega[e_obs], theta_rep]; no hidden conformal/disformal/source frame is a separate argument",
            "derivation_gain": "prevents source coupling from returning as a frame, marker, or material-preparation variable",
            "current_status": "EXACT_CONDITIONAL_FROM_1045_1046",
            "valid_for_claim": "false",
        },
        {
            "signature_id": "POS3253_4_hbar_measure_current_owner",
            "claim_piece": "single hbar, measure, and Hilbert-current extraction owner",
            "formal_statement": "exp(i S_ord/hbar_parent), dmu_parent, quotient/coframe Jacobian, and T_obs=(2/sqrt(-g_obs)) delta S_ord/delta g_obs are species-blind before readout",
            "derivation_gain": "removes hbar_A, measure Jacobian J_A, and post-variation kappa_A T_A routes that mimic source weights",
            "current_status": "CONDITIONAL_FROM_1230_3252",
            "valid_for_claim": "false",
        },
        {
            "signature_id": "POS3253_5_source_label_forgetting",
            "claim_piece": "source-label quotient or connected ordinary matter category",
            "formal_statement": "q_src forgets species labels before gravitational source selection, or pi_0(C_ord)=* with nonzero parent-owned edges so connected naturality collapses relative weights",
            "derivation_gain": "turns w_A=w_* into a common Newton coupling calibration and Delta_w_rel=0",
            "current_status": "CONDITIONAL_FROM_1231_3251",
            "valid_for_claim": "false",
        },
        {
            "signature_id": "POS3253_6_readout_and_boundary_stability",
            "claim_piece": "radiative/readout/boundary stability",
            "formal_statement": "S_eff, R_readout, compact support, collars, and boundary/projector maps commute with the same quotient and do not create source-label coefficients after variation",
            "derivation_gain": "prevents the theorem from being true in the parent action but false in clocks, WEP, PPN, R10, or local-current readout",
            "current_status": "UNSIGNED_STABILITY_CLAUSE",
            "valid_for_claim": "false",
        },
        {
            "signature_id": "POS3253_7_zero_theorem_if_signed",
            "claim_piece": "weighted-source branch zero",
            "formal_statement": "If POS3253_0 through POS3253_6 are parent-signed, then for every vertical v in ker(Dq_loc): Lie_v e_obs=Lie_v tau=Lie_v theta_rep=0, Delta_w_rel=0, C_wH=0, and the weighted-source part of D_A J_H vanishes",
            "derivation_gain": "this is the clean route from MTS source coupling toward local GR/Newton without inserting a plateau or closure axiom",
            "current_status": "EXACT_CONDITIONAL_THEOREM_NOT_CURRENT_CLAIM",
            "valid_for_claim": "false",
        },
        {
            "signature_id": "POS3253_8_current_verdict",
            "claim_piece": "current corpus status",
            "formal_statement": "The corpus contains strong conditional pieces but not a parent derivation signing Sigma_ord as one object; therefore use the finite C_Tw Gram route unless/until POS3253 closes",
            "derivation_gain": "prevents handwaving while still giving a calculable fallback branch",
            "current_status": "NOT_PARENT_SIGNED",
            "valid_for_claim": "false",
        },
    ]


def gap_rows() -> list[dict[str, Any]]:
    return [
        {
            "gap_id": "SCG3253_0_hidden_scalar",
            "unsigned_clause": "visible coefficient domain",
            "surviving_counterexample": "I_hid or Xhat feeds f(I)F^2, m_A(I), clock(I), or w_A(I)",
            "why_it_matters": "without a typed no-target theorem, absence of a term in one draft action is not derivation",
            "kills": "POS3253_2",
            "required_resolution": "prove parent object-language exhaustion or keep explicit finite coefficient rows",
            "valid_for_claim": "false",
        },
        {
            "gap_id": "SCG3253_1_action_scale",
            "unsigned_clause": "single hbar/action scale owner",
            "surviving_counterexample": "S_A -> w_A S_A leaves isolated classical Euler-Lagrange equations unchanged while changing source strength",
            "why_it_matters": "this is exactly how a wrong Newton coupling could hide until Hilbert/source extraction",
            "kills": "POS3253_1;POS3253_4",
            "required_resolution": "derive one action-density line and one hbar_parent, or source Delta_w priors",
            "valid_for_claim": "false",
        },
        {
            "gap_id": "SCG3253_2_measure_jacobian",
            "unsigned_clause": "species-blind measure/coframe/quotient Jacobian",
            "surviving_counterexample": "dmu_A or J_A creates a source-label factor after quotient descent",
            "why_it_matters": "a clean action density is insufficient if the measure repopulates source weights",
            "kills": "POS3253_4",
            "required_resolution": "derive D_A log dmu_parent has no source-label component",
            "valid_for_claim": "false",
        },
        {
            "gap_id": "SCG3253_3_post_variation_readout",
            "unsigned_clause": "pre-readout current extraction",
            "surviving_counterexample": "F((T_A,A))=kappa_A T_A after Hilbert variation",
            "why_it_matters": "covariance of T_A alone does not forbid a later source map",
            "kills": "POS3253_4;POS3253_6",
            "required_resolution": "show J_H is selected before source/material readout or include kappa residuals",
            "valid_for_claim": "false",
        },
        {
            "gap_id": "SCG3253_4_disconnected_components",
            "unsigned_clause": "source-label forgetting or connected C_ord",
            "surviving_counterexample": "ordinary matter component graph splits into electron, quark, QCD, EM binding, nuclear surface, and measure/readout residuals",
            "why_it_matters": "independent relative weights survive as Delta_w_c unless connected naturality or q_src collapses them",
            "kills": "POS3253_5",
            "required_resolution": "prove pi_0(C_ord)=* for source normalization or calculate component-current Gram rows",
            "valid_for_claim": "false",
        },
        {
            "gap_id": "SCG3253_5_radiative_return",
            "unsigned_clause": "S_eff/readout stability",
            "surviving_counterexample": "loop/effective/readout maps regenerate forbidden coefficients even if bare action is clean",
            "why_it_matters": "observables live after renormalization/readout, not just in the handwritten bare grammar",
            "kills": "POS3253_6",
            "required_resolution": "derive quotient-commuting readout/renormalization or keep finite rows",
            "valid_for_claim": "false",
        },
    ]


def finite_law_rows() -> list[dict[str, Any]]:
    return [
        {
            "law_id": "CTWG3253_0_component_current_definition",
            "object": "J_c",
            "formal_statement": "J_c := star_eobs(T_c_obs(tau,.)) on A_ext, using the same e_obs, tau, orientation, volume form, and current norm as J_H",
            "derivation_status": "DEFINITION_EXACT_FROM_3250_3252",
            "required_inputs": "component stress split T_c_obs; A_ext; tau_id; e_obs_id; J inner product",
            "valid_for_claim": "false",
        },
        {
            "law_id": "CTWG3253_1_exact_gram_operator_norm",
            "object": "C_Tw",
            "formal_statement": "For finite delta_w basis with positive Sigma metric G_Sigma and current Gram matrix G_J, (G_J)_{cd}=<J_c,J_d>_J, C_Tw^2 = lambda_max(G_J, G_Sigma)",
            "derivation_status": "NEW_EXACT_FINITE_DIMENSIONAL_OPERATOR_IDENTITY",
            "required_inputs": "G_J matrix; G_Sigma metric; consistent units and same-frame current norm",
            "valid_for_claim": "false",
        },
        {
            "law_id": "CTWG3253_2_euclidean_rss_bound",
            "object": "C_Tw_upper",
            "formal_statement": "If G_Sigma=I and only diagonal current norms are available, C_Tw <= sqrt(sum_c ||J_c||_J^2); this is safe but not generally sharp",
            "derivation_status": "BOUND_FROM_3252_RETAINED_AS_DIAGONAL_FALLBACK",
            "required_inputs": "component current norms ||J_c||_J; no claim that cross terms vanish",
            "valid_for_claim": "false",
        },
        {
            "law_id": "CTWG3253_3_weighted_source_bound",
            "object": "weighted_source_piece",
            "formal_statement": "||D_A J_H||_weighted <= sqrt(lambda_max(G_J,G_Sigma)) ||delta_w||_Sigma; if POS3253 signs Delta_w_rel=0, this branch is zero",
            "derivation_status": "EXACT_FORMULA_PENDING_NUMERIC_OR_ZERO_INPUTS",
            "required_inputs": "Delta_w theorem-zero or numeric prior; CTWG3253_1 Gram matrix",
            "valid_for_claim": "false",
        },
        {
            "law_id": "CTWG3253_4_units_guard",
            "object": "scoreability",
            "formal_statement": "Do not compare C_Tw across arenas until J norm, integration domain A_ext, tau normalization, stress units, and delta_w metric are declared in the same convention",
            "derivation_status": "METHODOLOGY_GATE",
            "required_inputs": "unit_system; A_ext; norm definition; tau normalization; source path for each component row",
            "valid_for_claim": "false",
        },
    ]


def component_intake_rows() -> list[dict[str, Any]]:
    basis_path = OUT / "P8_Y5_R10_1231_DISCONNECTED_COMPONENT_RESIDUAL_BASIS.csv"
    basis_rows = read_csv(basis_path) if basis_path.exists() else []
    rows: list[dict[str, Any]] = []
    for basis in basis_rows:
        component_id = basis.get("component_id", "MISSING_COMPONENT_ID")
        component = basis.get("component", "")
        symbol = basis.get("symbol", "")
        if component_id == "DCW1231_0_common_mode":
            status = "COMMON_MODE_CALIBRATION_ROW_NONCLAIM"
            role = "common Newton-coupling calibration check, not a relative residual if universal"
        else:
            status = "MISSING_COMPONENT_CURRENT_NORM_AND_GRAM_INNER_PRODUCTS"
            role = "relative source residual component for C_Tw finite branch"
        rows.append(
            {
                "intake_id": f"CCI3253_{len(rows)}",
                "basis_component_id": component_id,
                "component": component,
                "residual_symbol": symbol,
                "component_role": role,
                "J_c_definition": f"J_{symbol.replace('delta w_', '').replace('delta_w_', '').replace('delta ', '')} := star_eobs(T_{component_id}_obs(tau,.))",
                "norm_required": "||J_c||_J and all cross inner products <J_c,J_d>_J for exact Gram route",
                "A_ext": "MISSING_A_EXT_SOURCE_REGION",
                "tau_id": "MISSING_TAU_ID",
                "e_obs_id": "MISSING_E_OBS_ID",
                "G_sigma_entry": "MISSING_DELTA_W_METRIC_ENTRY",
                "G_J_entry_or_norm": "MISSING_COMPONENT_CURRENT_GRAM_ROW",
                "units": "MISSING_STRESS_CURRENT_NORM_UNITS",
                "source_path": "MISSING_COMPONENT_STRESS_SOURCE_PATH",
                "status": status,
                "valid_for_claim": "false",
            }
        )
    return rows


def update_rows() -> list[dict[str, Any]]:
    return [
        {
            "update_id": "WSU3253_0_signature_route",
            "target": "D_A J_H weighted-source residual",
            "previous_form": "C_wH <= C_Tw ||delta_w||_Sigma",
            "new_form": "If Sigma_ord is parent-signed, Delta_w_rel=0 and the weighted-source term is zero",
            "gain": "turns the coupling problem into one exact ordinary-sector signature theorem",
            "claim_effect": "conditional only",
            "valid_for_claim": "false",
        },
        {
            "update_id": "WSU3253_1_exact_finite_fallback",
            "target": "C_Tw fallback",
            "previous_form": "C_Tw <= sqrt(sum_c ||J_c||_J^2)",
            "new_form": "C_Tw^2 = lambda_max(G_J,G_Sigma) for finite component basis; RSS is only the diagonal-safe upper bound",
            "gain": "future data work becomes a matrix/eigenvalue calculation rather than a vague source norm",
            "claim_effect": "nonclaim until G_J, G_Sigma, tau, e_obs, A_ext, units, and delta_w are sourced",
            "valid_for_claim": "false",
        },
        {
            "update_id": "WSU3253_2_local_GR_route",
            "target": "local GR/Newton source coupling",
            "previous_form": "blocked by live source prefactor and current residuals",
            "new_form": "source side closes either by POS3253 theorem-zero or by finite ||D_A J_H||_weighted bound inserted into the 3250 master residual vector",
            "gain": "local-GR reduction now has a theorem branch and a numerically scoreable fallback branch",
            "claim_effect": "still blocked until one branch is completed",
            "valid_for_claim": "false",
        },
    ]


def gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "claim_gate_id": "CG3253_0_signature_shape",
            "claim": "Sigma_ord is the right composite target for ordinary-sector source coupling",
            "gate_pass": "true",
            "reason": "it explicitly includes every surviving source-coupling escape route from 1045/1046/1055/1106/1220/1230/1231/3252",
            "claim_allowed": "false",
        },
        {
            "claim_gate_id": "CG3253_1_signature_parent_signed",
            "claim": "Sigma_ord is derived from parent MTS primitives",
            "gate_pass": "false",
            "reason": "the composite object is assembled as a contract, not signed by a parent action derivation",
            "claim_allowed": "false",
        },
        {
            "claim_gate_id": "CG3253_2_CwH_zero",
            "claim": "C_wH=0 is current MTS theorem",
            "gate_pass": "false",
            "reason": "requires POS3253_0 through POS3253_6 plus source-label forgetting or connectedness",
            "claim_allowed": "false",
        },
        {
            "claim_gate_id": "CG3253_3_exact_CTw_law",
            "claim": "finite-dimensional C_Tw Gram/eigenvalue law is mathematically derived",
            "gate_pass": "true",
            "reason": "pure operator-norm/Rayleigh quotient identity once component basis and metrics are finite",
            "claim_allowed": "false",
        },
        {
            "claim_gate_id": "CG3253_4_CTw_numeric",
            "claim": "C_Tw is numeric/source-backed",
            "gate_pass": "false",
            "reason": "G_J, G_Sigma, tau, e_obs, A_ext, stress-current units, and component source paths remain missing",
            "claim_allowed": "false",
        },
        {
            "claim_gate_id": "CG3253_5_local_GR_Newton",
            "claim": "local GR/Newton source coupling is derived or bounded enough to claim",
            "gate_pass": "false",
            "reason": "weighted-source branch is sharpened but neither theorem-zero nor numeric bound is completed",
            "claim_allowed": "false",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3253_0_progress",
            "decision": "Keep derivation-first route, but promote finite fallback to an exact Gram/eigenvalue problem",
            "because": "this is the best way to stop circling: either sign Sigma_ord or fill a matrix row",
            "next_action": "attack one parent signature clause or source the first component-current Gram row",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3253_1_best_first_component",
            "decision": "Use EM/Coulomb binding as the first finite component-current target if theorem route stalls",
            "because": "it connects to Maxwell/Poynting stress, alpha/EM work, WEP material response, and source coupling in one arena",
            "next_action": "derive/source J_EM := star_eobs(T_EM_obs(tau,.)) on A_ext and its J-norm/Gram entries",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3253_2_no_public_claim",
            "decision": "Do not claim local GR, WEP, PPN, R10, clock, orbital, or Newton pass",
            "because": "the theorem branch is conditional and the finite branch has missing source rows",
            "next_action": "carry nonclaim gates forward",
            "valid_for_claim": "false",
        },
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT3253_0_3254",
            "selection": "selected_primary",
            "next_checkpoint": "3254-Y5-R2FR-first-component-current-Gram-row-or-parent-signature-clause-lock-under-AX1090.md",
            "next_script": "scripts/Y5_R2FR_3254_first_component_current_Gram_row_or_parent_signature_clause_lock.py",
            "objective": "Either sign the highest-leverage Sigma_ord clause, or create the first source-ready Gram row for J_EM/current-stress so C_Tw starts becoming calculable.",
            "guardrail": "No local-GR/Newton/Maxwell/WEP claim unless theorem-zero or numeric Gram/source rows actually close.",
            "valid_for_claim": "false",
        }
    ]


def markdown_doc(
    sources: list[dict[str, Any]],
    signature: list[dict[str, Any]],
    gaps: list[dict[str, Any]],
    finite_law: list[dict[str, Any]],
    intake: list[dict[str, Any]],
    updates: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> str:
    intake_preview = intake[:8]
    return "\n\n".join(
        [
            "# 3253 - Parent ordinary-sector action signature or C_Tw component-current norm intake under AX1090",
            f"Generated: `{RUN_UTC}`",
            "Private derivation checkpoint. This does not claim local GR, Newton, Maxwell, WEP, R10, PPN, clock, orbital, or public source-coupling success.",
            "## Summary\n"
            "- `3253` tries the derivation-first route honestly: assemble the exact parent ordinary-sector signature `Sigma_ord` that would remove source weights instead of assuming a plateau.\n"
            "- The theorem route is now explicit: if `Sigma_ord` is parent-signed, `Delta_w_rel=0`, `C_wH=0`, and the weighted-source piece of `D_A J_H` vanishes.\n"
            "- The current corpus still does **not** sign `Sigma_ord`; the source-coupling branch remains nonclaim.\n"
            "- The fallback is strengthened substantially: finite `C_Tw` is now an exact Gram/eigenvalue problem, `C_Tw^2=lambda_max(G_J,G_Sigma)`, with the old RSS formula retained only as a safe diagonal upper bound.\n"
            "- First concrete finite target is therefore not a vibes ledger: fill one component-current Gram row, preferably the EM/Coulomb stress current because it touches Maxwell/Poynting, alpha, material response, and source coupling.",
            "## Parent Ordinary-Sector Action Signature",
            md_table(
                signature,
                [
                    "signature_id",
                    "claim_piece",
                    "formal_statement",
                    "derivation_gain",
                    "current_status",
                    "valid_for_claim",
                ],
            ),
            "## Signature Closure Gap Audit",
            md_table(
                gaps,
                [
                    "gap_id",
                    "unsigned_clause",
                    "surviving_counterexample",
                    "why_it_matters",
                    "kills",
                    "required_resolution",
                    "valid_for_claim",
                ],
            ),
            "## C_Tw Finite Gram Operator Law",
            md_table(
                finite_law,
                [
                    "law_id",
                    "object",
                    "formal_statement",
                    "derivation_status",
                    "required_inputs",
                    "valid_for_claim",
                ],
            ),
            "## C_Tw Component Current Norm Intake Schema",
            md_table(
                intake_preview,
                [
                    "intake_id",
                    "basis_component_id",
                    "component",
                    "residual_symbol",
                    "component_role",
                    "norm_required",
                    "status",
                    "valid_for_claim",
                ],
            ),
            "## Weighted-Source Update",
            md_table(
                updates,
                [
                    "update_id",
                    "target",
                    "previous_form",
                    "new_form",
                    "gain",
                    "claim_effect",
                    "valid_for_claim",
                ],
            ),
            "## Claim Gates",
            md_table(gates, ["claim_gate_id", "claim", "gate_pass", "reason", "claim_allowed"]),
            "## Decisions",
            md_table(decisions, ["decision_id", "decision", "because", "next_action", "valid_for_claim"]),
            "## Next Target",
            md_table(
                next_target,
                [
                    "next_id",
                    "selection",
                    "next_checkpoint",
                    "next_script",
                    "objective",
                    "guardrail",
                    "valid_for_claim",
                ],
            ),
            "## Source Register",
            md_table(
                sources,
                ["source_id", "source_path", "exists", "parse_ok", "role", "evidence_hits", "valid_for_claim"],
            ),
            "## Validation",
            md_table(validation, ["validation_id", "passed", "requirement", "evidence"]),
            "## Working Verdict\n"
            "`3253` moves the coupling work forward in two ways. First, the theorem path is now a single object, `Sigma_ord`, whose signature would make relative source weights impossible rather than merely small. Second, if that object remains unsigned, the fallback is no longer an opaque `C_Tw`: it is a finite Gram/eigenvalue calculation. The project is still not allowed to claim local GR/Newton source closure, but the next attack is concrete: either sign one `Sigma_ord` clause or fill the first `G_J` row for the EM/Coulomb component current.",
        ]
    ) + "\n"


def validation_rows(
    sources: list[dict[str, Any]],
    signature: list[dict[str, Any]],
    gaps: list[dict[str, Any]],
    finite_law: list[dict[str, Any]],
    intake: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(validation_id: str, passed: bool, requirement: str, evidence_text: str) -> None:
        rows.append(
            {
                "validation_id": validation_id,
                "passed": bool_str(passed),
                "requirement": requirement,
                "evidence": evidence_text,
            }
        )

    source_paths_exist = all(row["exists"] == "true" and row["parse_ok"] == "true" for row in sources)
    add("VAL3253_0_sources_exist_parse", source_paths_exist, "every cited source path exists and parses if CSV", str(source_paths_exist))

    all_outputs_parse = all(csv_ok(path) for path in OUTPUTS.values() if path != OUTPUTS["validation"])
    add("VAL3253_1_output_csvs_parse", all_outputs_parse, "all 3253 output CSVs parse before validation write", str(all_outputs_parse))

    signature_tuple = any(row["signature_id"] == "POS3253_0_composite_object" and "Sigma_ord" in row["formal_statement"] for row in signature)
    add("VAL3253_2_sigma_ord_tuple", signature_tuple, "composite Sigma_ord signature row exists", str(signature_tuple))

    zero_theorem = any(row["signature_id"] == "POS3253_7_zero_theorem_if_signed" and "C_wH=0" in row["formal_statement"] for row in signature)
    add("VAL3253_3_conditional_zero_theorem", zero_theorem, "conditional weighted-source zero theorem is written", str(zero_theorem))

    gap_nonclaim = all(row["valid_for_claim"] == "false" for row in gaps)
    add("VAL3253_4_gaps_nonclaim", gap_nonclaim, "signature gap rows remain nonclaim", str(gap_nonclaim))

    exact_law = any(row["law_id"] == "CTWG3253_1_exact_gram_operator_norm" and "lambda_max" in row["formal_statement"] for row in finite_law)
    add("VAL3253_5_exact_gram_law", exact_law, "exact C_Tw Gram/eigenvalue law exists", str(exact_law))

    intake_count_ok = len(intake) >= 7
    intake_nonclaim = all(row["valid_for_claim"] == "false" for row in intake)
    intake_missing = all("MISSING_" in row["A_ext"] or "COMMON_MODE" in row["status"] for row in intake)
    add("VAL3253_6_intake_rows", intake_count_ok and intake_nonclaim and intake_missing, "component-current intake rows present, nonclaim, and preserve missing markers", f"count={len(intake)} nonclaim={intake_nonclaim} missing={intake_missing}")

    public_claims_blocked = all(row["claim_allowed"] == "false" for row in gates)
    local_claim_blocked = any(row["claim_gate_id"] == "CG3253_5_local_GR_Newton" and row["gate_pass"] == "false" for row in gates)
    add("VAL3253_7_claims_blocked", public_claims_blocked and local_claim_blocked, "all public/source-coupling claims remain blocked", f"claim_allowed_all_false={public_claims_blocked} local_gate_false={local_claim_blocked}")

    output_scope_ok = all(str(path).startswith(str(ROOT)) for path in [DOC, *OUTPUTS.values()])
    add("VAL3253_8_output_scope", output_scope_ok, "all generated files stay in post-checkpoint-work", str(output_scope_ok))

    formalization_3253_files = []
    if FW.exists():
        formalization_3253_files = [path for path in FW.rglob("*3253*") if path.is_file()]
    add("VAL3253_9_formalization_untouched", not formalization_3253_files, "no 3253 files are written under formalization-workbench", f"file_count={len(formalization_3253_files)}")

    next_present = bool(next_rows())
    add("VAL3253_10_next_target", next_present, "3254 next target is selected", str(next_present))

    overall = all(row["passed"] == "true" for row in rows)
    add("VAL3253_OVERALL", overall, "3253 validation overall", "all required validation rows passed" if overall else "one or more validation rows failed")
    return rows


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)

    sources = source_register()
    signature = parent_signature_rows()
    gaps = gap_rows()
    finite_law = finite_law_rows()
    intake = component_intake_rows()
    updates = update_rows()
    gates = gate_rows()
    decisions = decision_rows()
    next_target = next_rows()

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["signature"], signature)
    write_csv(OUTPUTS["gap"], gaps)
    write_csv(OUTPUTS["finite_law"], finite_law)
    write_csv(OUTPUTS["intake"], intake)
    write_csv(OUTPUTS["update"], updates)
    write_csv(OUTPUTS["gates"], gates)
    write_csv(OUTPUTS["decision"], decisions)
    write_csv(OUTPUTS["next"], next_target)

    validation = validation_rows(sources, signature, gaps, finite_law, intake, gates)
    write_csv(OUTPUTS["validation"], validation)
    DOC.write_text(
        markdown_doc(sources, signature, gaps, finite_law, intake, updates, gates, decisions, next_target, validation),
        encoding="utf-8",
    )

    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)

    overall = next(row for row in validation if row["validation_id"] == "VAL3253_OVERALL")
    print(f"{overall['validation_id']}={overall['passed']}")
    print(DOC)
    for name, path in OUTPUTS.items():
        print(f"{name}: {path}")


if __name__ == "__main__":
    main()
