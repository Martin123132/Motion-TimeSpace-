from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


POST_CHECKPOINT = Path(__file__).resolve().parents[1]
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"
FORMALIZATION = POST_CHECKPOINT.parent / "formalization-workbench"
OUTPUT_DOC = POST_CHECKPOINT / "728-Y5-R10-parent-Omega-and-DC-operator-fill-or-edge-row-source-input.md"
NEXT_TARGET = "729-Y5-R10-fill-PJ-parent-origin-or-source-backed-edge-coefficients.md"
GENERATED_UTC = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
CUTOFF = datetime(2026, 5, 31, 14, 42, 0)


SOURCES = {
    "727_doc": {
        "path": POST_CHECKPOINT / "727-Y5-R10-DCdagger-vertical-generator-map-or-source-backed-edge-row.md",
        "note": "immediate handoff: parent Omega/DC fill",
        "needles": ["728-Y5-R10-parent-Omega-and-DC-operator-fill-or-edge-row-source-input.md", "Current verdict: **conditional map only**", "Omega_Y^{-1}"],
    },
    "727_validation": {
        "path": RESIDUALS / "P8_Y5_BRR545_727_VALIDATION.csv",
        "note": "prior validation gate",
        "needles": ["V727_11_next_target_selected", "pass", "V727_14_formalization_workbench_untouched"],
    },
    "727_map": {
        "path": RESIDUALS / "P8_Y5_R10_727_DCDAGGER_VERTICAL_MAP.csv",
        "note": "current DCdagger Omega-flat map",
        "needles": ["DVM727_3_precise_map", "Omega_Y^flat", "false"],
    },
    "727_closure": {
        "path": RESIDUALS / "P8_Y5_R10_727_MAPPING_CLOSURE_GATE.csv",
        "note": "current closure gates",
        "needles": ["MCG727_0_parent_Omega", "MCG727_7_edge_sources", "true"],
    },
    "727_edge_status": {
        "path": RESIDUALS / "P8_Y5_R10_727_EDGE_ROW_SOURCE_STATUS.csv",
        "note": "current edge row source status",
        "needles": ["SBER726_0_required_source_backed_row", "missing_sources", "false"],
    },
    "591_doc": {
        "path": POST_CHECKPOINT / "591-Y5-R10-parent-Omega-and-DC-operator-fill-or-edge-row-source-input.md",
        "note": "older formal Omega/DC checkpoint",
        "needles": ["formal DC_X and DCdagger formulas", "P/J/Omega ownership", "Edge-source rows are still missing"],
    },
    "591_omega": {
        "path": RESIDUALS / "P8_Y5_R10_591_PARENT_OMEGA_CANDIDATE.csv",
        "note": "older parent Omega candidate rows",
        "needles": ["OM591_0_covariant_variation_definition", "formal_definition_only", "false"],
    },
    "591_dc": {
        "path": RESIDUALS / "P8_Y5_R10_591_DC_OPERATOR_FORMULA.csv",
        "note": "older formal DC operator formula rows",
        "needles": ["DC591_1_linearization_tensor_convention", "formal_operator_formula", "DC591_2_densitized_variant"],
    },
    "591_dcadjoint": {
        "path": RESIDUALS / "P8_Y5_R10_591_DCDAGGER_FORMULA.csv",
        "note": "older formal DCdagger formula rows",
        "needles": ["DCA591_1_PJ_adjoint", "operator_shape_derived", "DCA591_4_compare_to_Omega_flat"],
    },
    "591_comparison": {
        "path": RESIDUALS / "P8_Y5_R10_591_OMEGA_DCDAGGER_COMPARISON.csv",
        "note": "older Omega/DCdagger comparison blockers",
        "needles": ["CMP591_5_verdict", "formula_progress_but_no_certificate", "false"],
    },
    "591_edge": {
        "path": RESIDUALS / "P8_Y5_R10_591_EDGE_SOURCE_INPUT_STATUS.csv",
        "note": "older edge source input status",
        "needles": ["SBE589_0_required_source_backed_row", "missing", "false"],
    },
    "592_doc": {
        "path": POST_CHECKPOINT / "592-Y5-R10-fill-PJ-parent-origin-or-source-backed-edge-coefficients.md",
        "note": "older next checkpoint: P/J parent origin",
        "needles": ["Noether current", "P and J_eff", "current MTS"],
    },
    "592_noether": {
        "path": RESIDUALS / "P8_Y5_R10_592_NOETHER_PJ_ORIGIN_FORMULA.csv",
        "note": "Noether P/J origin formula",
        "needles": ["NPJ592_3_PJ_split", "conditional_PJ_origin_formula", "false"],
    },
    "592_pj_attempt": {
        "path": RESIDUALS / "P8_Y5_R10_592_PJ_PARENT_ORIGIN_ATTEMPT.csv",
        "note": "P/J parent origin attempts",
        "needles": ["PJA592_5_current_verdict", "formula_derived_but_not_filled", "false"],
    },
    "592_improvement": {
        "path": RESIDUALS / "P8_Y5_R10_592_IMPROVEMENT_AMBIGUITY_GATE.csv",
        "note": "P/J improvement ambiguity gate",
        "needles": ["IAG592_0_superpotential_improvement", "IAG592_1_current_improvement", "open"],
    },
    "592_edge_plan": {
        "path": RESIDUALS / "P8_Y5_R10_592_EDGE_COEFFICIENT_SOURCE_PLAN.csv",
        "note": "edge coefficient source plan",
        "needles": ["ESP592_0", "K_edge;Qbar_edge_XH;qbar_XT", "false"],
    },
    "583_doc": {
        "path": POST_CHECKPOINT / "583-Y5-R10-parent-momentum-map-owner-or-edge-residual-demotion.md",
        "note": "momentum-map owner contract",
        "needles": ["delta L_parent", "i_{v_epsilon} Omega_Y = delta G[epsilon]", "P[Y], J_eff[Y]"],
    },
    "513_doc": {
        "path": POST_CHECKPOINT / "513-Gamma-Khat-q_loc-first-variation-or-demotion.md",
        "note": "Ward/stress divergence route for J-like source",
        "needles": ["q_loc^nu = P_loc nabla_mu T_GK", "conditional_derivation_route", "not_supplied"],
    },
    "538_doc": {
        "path": POST_CHECKPOINT / "538-Y5-minimal-parent-action-Euler-Ward-test-or-closure-demotion.md",
        "note": "Euler-Ward parent action chain",
        "needles": ["Euler-Ward Chain Test", "Noether current", "conditional_pass_if_action_is_explicit"],
    },
}


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def source_path_string(*keys: str) -> str:
    return ";".join(str(SOURCES[key]["path"]) for key in keys)


def text_contains(path: Path, needles: list[str]) -> bool:
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8", errors="replace")
    return all(needle in text for needle in needles)


def csv_contains(path: Path, *needles: str) -> bool:
    return text_contains(path, list(needles))


def prior_validation_clean(path: Path) -> bool:
    rows = read_csv(path)
    return bool(rows) and all(row.get("result") == "pass" for row in rows)


def all_valid_false(paths: list[Path]) -> bool:
    for path in paths:
        rows = read_csv(path)
        if not rows:
            continue
        if "valid_for_claim" not in rows[0]:
            continue
        if any(row.get("valid_for_claim", "").lower() != "false" for row in rows):
            return False
    return True


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


def markdown_table(rows: list[dict[str, object]], fields: list[str]) -> str:
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


def make_source_register() -> list[dict[str, object]]:
    return [
        {
            "source_id": key,
            "path": str(info["path"]),
            "exists": bool_text(info["path"].exists()),
            "needle_check": bool_text(text_contains(info["path"], info["needles"])),
            "role": info["note"],
            "valid_for_claim": "false",
            "generated_utc": GENERATED_UTC,
        }
        for key, info in SOURCES.items()
    ]


def main() -> None:
    RESIDUALS.mkdir(parents=True, exist_ok=True)
    source_register = make_source_register()

    parent_omega_candidate = [
        {
            "block_id": "OM728_0_covariant_variation_definition",
            "candidate_theta": "delta L_parent = E_A delta Y^A + d theta_Y(delta Y)",
            "candidate_Omega": "Omega_Y(delta1,delta2)=int_Sigma[delta1 theta_Y(delta2)-delta2 theta_Y(delta1)]",
            "what_it_would_buy": "defines Omega-flat and makes DCdagger comparable to a vertical generator",
            "current_status": "formal_definition_only",
            "claim_blocker": "no explicit MTS L_parent/theta_Y supplies this object yet",
            "valid_for_claim": "false",
            "source_paths": source_path_string("591_omega", "583_doc"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "block_id": "OM728_1_EH_metric_core",
            "candidate_theta": "theta_EH^mu=(2 kappa)^-1 sqrt(-g)(nabla_nu delta g^{mu nu}-nabla^mu delta g)",
            "candidate_Omega": "standard covariant phase-space EH symplectic current",
            "what_it_would_buy": "metric diffeomorphism generator has known Omega-flat form",
            "current_status": "standard_GR_template_not_yet_declared_as_MTS_parent_core",
            "claim_blocker": "template is not parent ownership of MTS extra symbols",
            "valid_for_claim": "false",
            "source_paths": source_path_string("591_omega"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "block_id": "OM728_2_extra_sector",
            "candidate_theta": "theta_extra=sum_A Pi_A^mu delta Phi^A plus possible higher-derivative improvements",
            "candidate_Omega": "int_Sigma delta Pi_A wedge delta Phi^A plus improvement terms",
            "what_it_would_buy": "field-by-field vertical action can be compared with DCdagger",
            "current_status": "missing_explicit_MTS_extra_parent_Lagrangian",
            "claim_blocker": "Gamma/Khat/memory/domain/projector sectors lack an explicit parent Lagrangian",
            "valid_for_claim": "false",
            "source_paths": source_path_string("591_omega", "513_doc"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "block_id": "OM728_3_affine_X_block",
            "candidate_theta": "from P^{mu nu} nabla_mu X_nu: theta_X^mu=sqrt(-g)P^{mu nu}delta X_nu",
            "candidate_Omega": "delta P^{mu nu} wedge delta X_nu on Sigma plus metric-density terms",
            "what_it_would_buy": "shows the affine block supplies an X/P pair unless quotiented/proper-gauge",
            "current_status": "useful_warning_not_parent_silence_proof",
            "claim_blocker": "it names a multiplier pair but does not prove it is quotient-silent",
            "valid_for_claim": "false",
            "source_paths": source_path_string("591_omega", "592_pj_attempt"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "block_id": "OM728_4_reduced_Omega",
            "candidate_theta": "theta_reduced=theta_parent after quotienting proper vertical pair and fixing boundary reference",
            "candidate_Omega": "Omega_reduced nondegenerate on physical quotient directions",
            "what_it_would_buy": "lets DCdagger=0 imply v_X=0 modulo known degeneracies",
            "current_status": "not_constructed",
            "claim_blocker": "nondegenerate reduced phase space and no-proper-stabilizer theorem are absent",
            "valid_for_claim": "false",
            "source_paths": source_path_string("591_omega", "727_closure"),
            "generated_utc": GENERATED_UTC,
        },
    ]

    dc_operator_formula = [
        {
            "formula_id": "DC728_0_constraint_definition",
            "object": "C_X^nu[Y]",
            "formula": "C_X^nu=-nabla_mu P^{mu nu}[Y]+J_eff^nu[Y]",
            "assumptions": "P is treated as an ordinary contravariant tensor; density convention must be fixed by parent theta/current",
            "status": "definition_contract",
            "valid_for_claim": "false",
            "source_paths": source_path_string("591_dc", "592_noether"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "formula_id": "DC728_1_linearization_tensor_convention",
            "object": "DC_X^nu[delta Y]",
            "formula": "DC_X^nu=-nabla_mu(delta P^{mu nu})-deltaGamma^mu_{mu rho}P^{rho nu}-deltaGamma^nu_{mu rho}P^{mu rho}+delta J_eff^nu",
            "assumptions": "valid when nabla and volume measure are metric/coframe dependent and P is not densitized",
            "status": "formal_operator_formula",
            "valid_for_claim": "false",
            "source_paths": source_path_string("591_dc"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "formula_id": "DC728_2_densitized_variant",
            "object": "DC_X^nu for density Ptilde",
            "formula": "if C_X^nu=-(1/sqrt(g))partial_mu Ptilde^{mu nu}+J^nu then DC differs by density/volume terms and fewer connection terms",
            "assumptions": "must choose tensor versus density before comparing with Omega-flat",
            "status": "convention_gate_open",
            "valid_for_claim": "false",
            "source_paths": source_path_string("591_dc", "592_improvement"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "formula_id": "DC728_3_parent_field_expansion",
            "object": "delta P and delta J",
            "formula": "delta P^{mu nu}=P^{mu nu}_{,A}delta Y^A+P^{mu nu alpha}_{,A}nabla_alpha delta Y^A+...; delta J^nu=J^nu_{,A}delta Y^A+J^{nu alpha}_{,A}nabla_alpha delta Y^A+...",
            "assumptions": "P and J must be composites of explicit parent fields",
            "status": "expansion_template_not_filled",
            "valid_for_claim": "false",
            "source_paths": source_path_string("591_dc", "592_pj_attempt"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "formula_id": "DC728_4_boundary_pairing",
            "object": "boundary term from DC",
            "formula": "int_M X_nu[-nabla_mu delta P^{mu nu}]=int_M(nabla_mu X_nu)delta P^{mu nu}-int_boundary n_mu X_nu delta P^{mu nu}",
            "assumptions": "boundary term must be cancelled by delta Q_X or killed by proper X/domain",
            "status": "edge_risk_explicit",
            "valid_for_claim": "false",
            "source_paths": source_path_string("591_dc", "727_closure"),
            "generated_utc": GENERATED_UTC,
        },
    ]

    dcdagger_formula = [
        {
            "adjoint_id": "DCA728_0_formal_pairing",
            "formula": "<X,DC[delta Y]>=<DCdagger X,delta Y>+B_DC[X,delta Y]",
            "meaning": "defines DCdagger only after a bulk pairing and boundary domain are chosen",
            "current_status": "formal_definition",
            "valid_for_claim": "false",
            "source_paths": source_path_string("591_dcadjoint", "727_map"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "adjoint_id": "DCA728_1_PJ_adjoint",
            "formula": "DCdagger_A X=(DP_A)^dagger[nabla_mu X_nu]+(DJ_A)^dagger[X_nu]+connection/volume adjoint terms",
            "meaning": "the adjoint is controlled by how P and J depend on parent fields",
            "current_status": "operator_shape_derived",
            "valid_for_claim": "false",
            "source_paths": source_path_string("591_dcadjoint", "592_pj_attempt"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "adjoint_id": "DCA728_2_metric_connection_terms",
            "formula": "metric/coframe component also receives adjoints of -X_nu deltaGamma^mu_{mu rho}P^{rho nu}-X_nu deltaGamma^nu_{mu rho}P^{mu rho}",
            "meaning": "even simple P,J still produce connection variation terms in Omega-flat matching",
            "current_status": "must_be_included",
            "valid_for_claim": "false",
            "source_paths": source_path_string("591_dcadjoint", "591_dc"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "adjoint_id": "DCA728_3_boundary_adjoint",
            "formula": "B_DC=-int_boundary n_mu X_nu delta P^{mu nu}+delta Q_X plus possible density/reference terms",
            "meaning": "differentiability of G_X is equivalent to cancelling this boundary covector",
            "current_status": "not_cancelled_currently",
            "valid_for_claim": "false",
            "source_paths": source_path_string("591_dcadjoint", "727_closure"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "adjoint_id": "DCA728_4_compare_to_Omega_flat",
            "formula": "DCdagger_A X=[Omega_flat(v_X)]_A for every parent field A",
            "meaning": "this is an equation for P,J,theta,Omega and v_X, not a slogan",
            "current_status": "not_closed_without_parent_PJ_and_Omega",
            "valid_for_claim": "false",
            "source_paths": source_path_string("591_dcadjoint", "727_map"),
            "generated_utc": GENERATED_UTC,
        },
    ]

    omega_dcdagger_comparison = [
        {
            "comparison_id": "CMP728_0_GR_like_success_condition",
            "left_side": "DCdagger X from C_X=-nabla P+J",
            "right_side": "Omega_flat(L_X Y)",
            "match_condition": "P is the canonical/symplectic momentum coefficient and J is the matter/extra momentum density from the same parent Noether current",
            "current_result": "conditional_standard_GR_like_route",
            "claim_status": "false",
            "source_paths": source_path_string("591_comparison", "592_noether"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "comparison_id": "CMP728_1_current_MTS_P_owner",
            "left_side": "P^{mu nu}[Y]",
            "right_side": "coefficient in theta_Y(v_X) or canonical momentum map",
            "match_condition": "P is derived from V_def/parent theta, not an independent tensor",
            "current_result": "not_derived",
            "claim_status": "false",
            "source_paths": source_path_string("591_comparison", "592_pj_attempt"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "comparison_id": "CMP728_2_current_MTS_J_owner",
            "left_side": "J_eff^nu[Y]",
            "right_side": "Euler-Ward/source-current contribution in the same Noether identity",
            "match_condition": "J_eff follows from S_GK/memory/domain parent variation",
            "current_result": "not_derived",
            "claim_status": "false",
            "source_paths": source_path_string("591_comparison", "513_doc", "538_doc"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "comparison_id": "CMP728_3_current_MTS_Omega",
            "left_side": "field-space pairing used in DCdagger",
            "right_side": "Omega_Y from theta_Y",
            "match_condition": "same parent action supplies both theta/Omega and C_X",
            "current_result": "missing",
            "claim_status": "false",
            "source_paths": source_path_string("591_comparison", "727_closure"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "comparison_id": "CMP728_4_boundary",
            "left_side": "B_DC and Q_X",
            "right_side": "differentiable Hamiltonian generator with zero/proper local charge",
            "match_condition": "delta Q_X cancels B_DC and Q_X=0/exact/proper on compact branch",
            "current_result": "not_derived",
            "claim_status": "false",
            "source_paths": source_path_string("591_comparison", "592_improvement"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "comparison_id": "CMP728_5_verdict",
            "left_side": "formal DC/DCdagger formula",
            "right_side": "parent-owned Omega-flat vertical generator",
            "match_condition": "all comparison rows close together",
            "current_result": "formula_progress_but_no_certificate",
            "claim_status": "false",
            "source_paths": source_path_string("591_comparison", "727_doc"),
            "generated_utc": GENERATED_UTC,
        },
    ]

    parent_ownership_blocker = [
        {
            "blocker_id": "POB728_0_L_parent",
            "needed_object": "explicit L_parent",
            "why_needed": "one action must supply theta/Omega, P, J_eff, mu_X, Q_X, and matter readout",
            "current_status": "missing",
            "if_missing": "operator formulas remain templates",
            "valid_for_claim": "false",
            "source_paths": source_path_string("592_doc", "538_doc"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "blocker_id": "POB728_1_theta_mu_vX",
            "needed_object": "theta_Y, mu_X, and v_X",
            "why_needed": "Noether current j_X=theta_Y(v_X)-mu_X is the exact P/J origin contract",
            "current_status": "missing",
            "if_missing": "P/J cannot be parent-owned",
            "valid_for_claim": "false",
            "source_paths": source_path_string("592_noether", "583_doc"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "blocker_id": "POB728_2_PJ_from_one_current",
            "needed_object": "P and J_eff from the same Noether current",
            "why_needed": "independent P/J declarations do not give theorem credit",
            "current_status": "formula_derived_but_not_filled",
            "if_missing": "C_X remains closure/source residual",
            "valid_for_claim": "false",
            "source_paths": source_path_string("592_noether", "592_pj_attempt"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "blocker_id": "POB728_3_improvement_representative",
            "needed_object": "fixed boundary/superpotential representative",
            "why_needed": "P and Q_X can shift by improvements while changing edge charge",
            "current_status": "open",
            "if_missing": "edge alpha can be moved between bulk and boundary bookkeeping",
            "valid_for_claim": "false",
            "source_paths": source_path_string("592_improvement"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "blocker_id": "POB728_4_edge_coefficients",
            "needed_object": "source-backed K_edge,Qbar_edge_XH,qbar_XT",
            "why_needed": "fallback branch cannot be scored from diagnostic budgets",
            "current_status": "missing_sources",
            "if_missing": "edge row remains nonclaim smoke",
            "valid_for_claim": "false",
            "source_paths": source_path_string("727_edge_status", "592_edge_plan"),
            "generated_utc": GENERATED_UTC,
        },
    ]

    edge_source_input_status = [
        {
            "edge_row_id": row["edge_row_id"],
            "lambda_um": row["lambda_um"],
            "alpha_edge_ceiling": row["alpha_edge_ceiling"],
            "current_source_status": row.get("source_status", row.get("current_source_status", "")),
            "K_edge_source": "missing" if row.get("source_status", "") == "missing_sources" else "diagnostic_only",
            "Qbar_edge_XH_source": "missing" if row.get("source_status", "") == "missing_sources" else "diagnostic_only",
            "qbar_XT_source": "missing" if row.get("source_status", "") == "missing_sources" else "diagnostic_only",
            "required_next": row["required_next"],
            "valid_for_claim": "false",
            "source_paths": source_path_string("727_edge_status", "592_edge_plan"),
            "generated_utc": GENERATED_UTC,
        }
        for row in read_csv(SOURCES["727_edge_status"]["path"])
    ]

    decision_matrix = [
        {
            "decision_id": "D728_0_DC_operator_derived_formally",
            "decision": "formal DC_X and DCdagger formulas are carried into the current chain",
            "meaning": "the next proof debt is P/J/Omega ownership, not raw linearization",
            "claim_status": "nonclaim_formula_progress",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "source_paths": source_path_string("591_doc", "591_dc", "591_dcadjoint"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "decision_id": "D728_1_parent_Omega_candidate_not_enough",
            "decision": "standard covariant Omega candidate is not a current MTS certificate",
            "meaning": "no DCdagger=Omega-flat(v_X) proof until theta/Omega and P/J come from one action",
            "claim_status": "blocked_for_claim",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "source_paths": source_path_string("591_omega", "592_doc"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "decision_id": "D728_2_PJ_origin_is_next",
            "decision": "next target should fill P/J parent origin",
            "meaning": "P and J_eff need exact Noether origin j_X=theta(v_X)-mu_X, or the edge source path takes over",
            "claim_status": "next_derivation_target",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "source_paths": source_path_string("592_noether", "592_pj_attempt"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "decision_id": "D728_3_edge_sources_still_missing",
            "decision": "source-backed edge row remains unfilled",
            "meaning": "fallback requires K_edge,Qbar_edge_XH,qbar_XT or theorem-zero rows",
            "claim_status": "fallback_blocked",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "source_paths": source_path_string("727_edge_status", "592_edge_plan"),
            "generated_utc": GENERATED_UTC,
        },
    ]

    route_update = [
        {
            "route_id": "RU728_0_allowed",
            "allowed_after_728": "use formal DC/DCdagger formulas as the next parent-origin test",
            "forbidden_after_728": "claim Omega closure from standard GR templates without MTS parent action ownership",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "source_paths": source_path_string("591_dc", "591_dcadjoint"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "route_id": "RU728_1_allowed",
            "allowed_after_728": "try to derive P and J from one parent Noether current/theta_Y",
            "forbidden_after_728": "treat independent P or inserted J as theorem-owned",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "source_paths": source_path_string("592_noether", "592_pj_attempt"),
            "generated_utc": GENERATED_UTC,
        },
        {
            "route_id": "RU728_2_allowed",
            "allowed_after_728": "if P/J/Omega ownership fails, fill source-backed edge coefficients",
            "forbidden_after_728": "mark edge diagnostic rows valid_for_claim",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "source_paths": source_path_string("727_edge_status", "592_edge_plan"),
            "generated_utc": GENERATED_UTC,
        },
    ]

    nonclaim_summary = [
        {
            "status": "Y5_R10_728_parent_Omega_candidate_and_DC_operator_written_parent_certificate_not_closed_edge_sources_missing",
            "claim_ceiling": "Omega_candidate_and_DC_formal_operator_only_no_R10_WEP_PPN_Newton_or_local_GR_pass",
            "main_result": "formal Omega, DC_X, and DCdagger machinery is now current-chain explicit",
            "hard_blocker": "one parent action must still supply theta/Omega, P, J_eff, v_X, mu_X, boundary representative, and matter/projector silence",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "source_paths": source_path_string("727_doc", "591_doc", "592_doc"),
            "generated_utc": GENERATED_UTC,
        }
    ]

    outputs = {
        "source_register": (
            RESIDUALS / "P8_Y5_R10_728_SOURCE_REGISTER.csv",
            source_register,
            ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"],
        ),
        "parent_omega_candidate": (
            RESIDUALS / "P8_Y5_R10_728_PARENT_OMEGA_CANDIDATE.csv",
            parent_omega_candidate,
            ["block_id", "candidate_theta", "candidate_Omega", "what_it_would_buy", "current_status", "claim_blocker", "valid_for_claim", "source_paths", "generated_utc"],
        ),
        "dc_operator_formula": (
            RESIDUALS / "P8_Y5_R10_728_DC_OPERATOR_FORMULA.csv",
            dc_operator_formula,
            ["formula_id", "object", "formula", "assumptions", "status", "valid_for_claim", "source_paths", "generated_utc"],
        ),
        "dcdagger_formula": (
            RESIDUALS / "P8_Y5_R10_728_DCDAGGER_FORMULA.csv",
            dcdagger_formula,
            ["adjoint_id", "formula", "meaning", "current_status", "valid_for_claim", "source_paths", "generated_utc"],
        ),
        "omega_dcdagger_comparison": (
            RESIDUALS / "P8_Y5_R10_728_OMEGA_DCDAGGER_COMPARISON.csv",
            omega_dcdagger_comparison,
            ["comparison_id", "left_side", "right_side", "match_condition", "current_result", "claim_status", "source_paths", "generated_utc"],
        ),
        "parent_ownership_blocker": (
            RESIDUALS / "P8_Y5_R10_728_PARENT_OWNERSHIP_BLOCKER.csv",
            parent_ownership_blocker,
            ["blocker_id", "needed_object", "why_needed", "current_status", "if_missing", "valid_for_claim", "source_paths", "generated_utc"],
        ),
        "edge_source_input_status": (
            RESIDUALS / "P8_Y5_R10_728_EDGE_SOURCE_INPUT_STATUS.csv",
            edge_source_input_status,
            ["edge_row_id", "lambda_um", "alpha_edge_ceiling", "current_source_status", "K_edge_source", "Qbar_edge_XH_source", "qbar_XT_source", "required_next", "valid_for_claim", "source_paths", "generated_utc"],
        ),
        "decision_matrix": (
            RESIDUALS / "P8_Y5_R10_728_DECISION_MATRIX.csv",
            decision_matrix,
            ["decision_id", "decision", "meaning", "claim_status", "next_target", "valid_for_claim", "source_paths", "generated_utc"],
        ),
        "route_update": (
            RESIDUALS / "P8_Y5_R10_728_ROUTE_UPDATE.csv",
            route_update,
            ["route_id", "allowed_after_728", "forbidden_after_728", "next_action", "valid_for_claim", "source_paths", "generated_utc"],
        ),
        "nonclaim_summary": (
            RESIDUALS / "P8_Y5_R10_728_NONCLAIM_SUMMARY.csv",
            nonclaim_summary,
            ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target", "valid_for_claim", "source_paths", "generated_utc"],
        ),
    }

    for path, rows, fields in outputs.values():
        write_csv(path, rows, fields)

    generated_paths = [path for path, _, _ in outputs.values()]
    formalization_count = formalization_changed_after_cutoff()
    validations = [
        {
            "check_id": "V728_0_source_paths_exist",
            "result": "pass" if all(info["path"].exists() for info in SOURCES.values()) else "fail",
            "detail": "all cited source paths exist",
        },
        {
            "check_id": "V728_1_source_needles_present",
            "result": "pass" if all(text_contains(info["path"], info["needles"]) for info in SOURCES.values()) else "fail",
            "detail": "all source files contain expected evidence needles",
        },
        {
            "check_id": "V728_2_prior_727_clean",
            "result": "pass" if prior_validation_clean(SOURCES["727_validation"]["path"]) else "fail",
            "detail": "727 validation has no failures",
        },
        {
            "check_id": "V728_3_727_selected_728",
            "result": "pass" if csv_contains(SOURCES["727_doc"]["path"], "728-Y5-R10-parent-Omega-and-DC-operator-fill-or-edge-row-source-input.md") else "fail",
            "detail": "727 selected this checkpoint",
        },
        {
            "check_id": "V728_4_Omega_candidate_nonclaim",
            "result": "pass" if len(parent_omega_candidate) == 5 and all(row["valid_for_claim"] == "false" for row in parent_omega_candidate) else "fail",
            "detail": f"omega_rows={len(parent_omega_candidate)}",
        },
        {
            "check_id": "V728_5_DC_operator_has_connection_and_density_gate",
            "result": "pass"
            if any("deltaGamma" in row["formula"] for row in dc_operator_formula)
            and any("densitized" in row["object"] or "density" in row["formula"] for row in dc_operator_formula)
            else "fail",
            "detail": f"dc_rows={len(dc_operator_formula)};connection_terms=True",
        },
        {
            "check_id": "V728_6_DCadjoint_boundary_explicit",
            "result": "pass" if any("boundary" in row["formula"] or "B_DC" in row["formula"] for row in dcdagger_formula) else "fail",
            "detail": f"adjoint_rows={len(dcdagger_formula)};boundary_explicit=True",
        },
        {
            "check_id": "V728_7_comparison_blocks_claim",
            "result": "pass" if len(omega_dcdagger_comparison) == 6 and all(row["claim_status"] == "false" for row in omega_dcdagger_comparison) else "fail",
            "detail": f"comparison_rows={len(omega_dcdagger_comparison)}",
        },
        {
            "check_id": "V728_8_parent_ownership_blockers_visible",
            "result": "pass"
            if {"explicit L_parent", "theta_Y, mu_X, and v_X", "P and J_eff from the same Noether current"}.issubset({row["needed_object"] for row in parent_ownership_blocker})
            else "fail",
            "detail": f"blocker_rows={len(parent_ownership_blocker)}",
        },
        {
            "check_id": "V728_9_edge_sources_still_nonclaim",
            "result": "pass"
            if len(edge_source_input_status) == 3
            and all(row["valid_for_claim"] == "false" for row in edge_source_input_status)
            and any(row["current_source_status"] == "missing_sources" for row in edge_source_input_status)
            else "fail",
            "detail": f"edge_rows={len(edge_source_input_status)};edge_missing=True",
        },
        {
            "check_id": "V728_10_old_591_592_integrated",
            "result": "pass"
            if csv_contains(SOURCES["591_comparison"]["path"], "CMP591_5_verdict")
            and csv_contains(SOURCES["592_noether"]["path"], "NPJ592_3_PJ_split")
            else "fail",
            "detail": "Omega/DC formalism and P/J next contract integrated",
        },
        {
            "check_id": "V728_11_next_target_selected",
            "result": "pass" if all(row["next_target"] == NEXT_TARGET for row in decision_matrix) else "fail",
            "detail": NEXT_TARGET,
        },
        {
            "check_id": "V728_12_no_claim_rows_promoted",
            "result": "pass" if all_valid_false(generated_paths) else "fail",
            "detail": "all generated rows with valid_for_claim remain false",
        },
        {
            "check_id": "V728_13_outputs_scoped",
            "result": "pass" if under_post_checkpoint([OUTPUT_DOC, *generated_paths]) else "fail",
            "detail": "all outputs under post-checkpoint-work",
        },
        {
            "check_id": "V728_14_formalization_workbench_untouched",
            "result": "pass" if formalization_count == 0 else "fail",
            "detail": f"formalization_changed_after_cutoff={formalization_count}",
        },
        {
            "check_id": "V728_15_no_local_arena_claim",
            "result": "pass" if "no_R10_WEP_PPN_Newton_or_local_GR_pass" in nonclaim_summary[0]["claim_ceiling"] else "fail",
            "detail": "R10/WEP/PPN/Newton/local-GR claims remain blocked",
        },
        {
            "check_id": "V728_16_source_register_written",
            "result": "pass" if len(source_register) >= 18 else "fail",
            "detail": f"source_rows={len(source_register)}",
        },
        {
            "check_id": "V728_17_validation_rows_ready",
            "result": "pass",
            "detail": "validation table constructed",
        },
    ]

    validation_path = RESIDUALS / "P8_Y5_BRR545_728_VALIDATION.csv"
    write_csv(validation_path, validations, ["check_id", "result", "detail"])

    doc = f"""# 728 - Y5 R10 Parent Omega And DC Operator Fill Or Edge Row Source Input

## Summary

This checkpoint carries the formal operator machinery into the current 720+ chain.

Useful formal progress:

```text
C_X^nu = -nabla_mu P^{{mu nu}} + J_eff^nu
DC_X^nu[delta Y] = -nabla_mu(delta P^{{mu nu}}) - deltaGamma terms + delta J_eff^nu
DCdagger_A X = (DP_A)^dagger[nabla X] + (DJ_A)^dagger[X] + connection/volume/boundary adjoints
```

Current verdict: **formula progress, not certificate**. The same parent action still has to own `theta/Omega`, `P`, `J_eff`, `Q_X`, `v_X`, `mu_X`, and the boundary representative.

| Field | Value |
| --- | --- |
| Generated UTC | `{GENERATED_UTC}` |
| Claim status | private/nonclaim checkpoint |
| Next target | `{NEXT_TARGET}` |

## Parent Omega Candidate

{markdown_table(parent_omega_candidate, ["block_id", "current_status", "what_it_would_buy", "claim_blocker", "valid_for_claim"])}

## DC Operator Formula

{markdown_table(dc_operator_formula, ["formula_id", "object", "formula", "status", "valid_for_claim"])}

## DCdagger Formula

{markdown_table(dcdagger_formula, ["adjoint_id", "formula", "current_status", "valid_for_claim"])}

## Omega/DCdagger Comparison

{markdown_table(omega_dcdagger_comparison, ["comparison_id", "left_side", "right_side", "current_result", "claim_status"])}

## Parent Ownership Blocker

{markdown_table(parent_ownership_blocker, ["blocker_id", "needed_object", "current_status", "if_missing", "valid_for_claim"])}

## Edge Source Input Status

{markdown_table(edge_source_input_status, ["edge_row_id", "lambda_um", "alpha_edge_ceiling", "current_source_status", "K_edge_source", "Qbar_edge_XH_source", "qbar_XT_source", "valid_for_claim"])}

## Decision Matrix

{markdown_table(decision_matrix, ["decision_id", "decision", "claim_status", "next_target", "valid_for_claim"])}

## Route Update

{markdown_table(route_update, ["route_id", "allowed_after_728", "forbidden_after_728", "next_action", "valid_for_claim"])}

## Nonclaim Summary

{markdown_table(nonclaim_summary, ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target", "valid_for_claim"])}

## Source Register

{markdown_table(source_register, ["source_id", "path", "exists", "needle_check", "role"])}

## Validation

{markdown_table(validations, ["check_id", "result", "detail"])}

## Practical Read

This is useful but not yet magic. We now have enough formal `DC_X` and `DCdagger` structure to red-team properly. The next wall is sharper: derive `P` and `J_eff` as coefficients of one Noether current `j_X=theta_Y(v_X)-mu_X`, or stop theorem-hunting and source the edge coefficients.
"""

    OUTPUT_DOC.write_text(doc, encoding="utf-8")
    print(f"wrote {OUTPUT_DOC}")
    print(f"wrote {validation_path}")
    print(f"validation_passes={sum(row['result'] == 'pass' for row in validations)}/{len(validations)}")
    print(f"next_target={NEXT_TARGET}")


if __name__ == "__main__":
    main()
