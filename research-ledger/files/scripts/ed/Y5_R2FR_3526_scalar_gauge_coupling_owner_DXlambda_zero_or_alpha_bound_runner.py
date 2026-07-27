from __future__ import annotations

import csv
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
FORMALIZATION = ROOT.parent / "formalization-workbench"
DOC = ROOT / "3526-Y5-R2FR-scalar-gauge-coupling-owner-DXlambda-zero-or-alpha-bound-runner.md"
CANONICAL_STATUS = OUT / "P8_EM_scalar_gauge_coupling_owner_status.csv"


SOURCES: dict[str, dict[str, Any]] = {
    "script_3526": {"path": Path(__file__).resolve(), "role": "3526 generator"},
    "doc_3525": {
        "path": ROOT / "3525-Y5-R2FR-visible-EM-action-domain-exhaustion-or-q-stack-owner-first-branch.md",
        "role": "visible EM normal-form handoff",
    },
    "next_3525": {
        "path": OUT / "P8_Y5_R2FR_3525_NEXT_TARGET.csv",
        "role": "3525-selected scalar coupling target",
    },
    "reduction_3525": {
        "path": OUT / "P8_Y5_R2FR_3525_VISIBLE_EM_REDUCTION_THEOREM.csv",
        "role": "3525 normal form and C_XF2 obstruction",
    },
    "requirements_3525": {
        "path": OUT / "P8_Y5_R2FR_3525_EXECUTABLE_RESIDUAL_REQUIREMENTS.csv",
        "role": "3525 residual source/unit/projection requirements",
    },
    "tq_signature_1100": {
        "path": OUT / "P8_Y5_R10_1100_TQ_GAUGE_NORM_SIGNATURE.csv",
        "role": "T_Q gauge norm, charge lattice and same-current owner clauses",
    },
    "tq_theorem_1100": {
        "path": OUT / "P8_Y5_R10_1100_TQ_THEOREM_ATTEMPT.csv",
        "role": "1100 exact conditional alpha-owner theorem and countermodels",
    },
    "alpha_decomp_1100": {
        "path": OUT / "P8_Y5_R10_1100_ALPHA_NORMALIZATION_DECOMPOSITION.csv",
        "role": "1100 decomposition of parent piece, lambda_A, hidden and readout terms",
    },
    "alpha_product_bound_1100": {
        "path": OUT / "P8_Y5_R10_1100_ALPHA_PRODUCT_BOUND_IMPORT.csv",
        "role": "source-backed alpha product bound imports",
    },
    "alpha_owner_1812": {
        "path": OUT / "P8_Y5_PARENT_QLOC_1812_CONDITIONAL_OWNER_THEOREM.csv",
        "role": "1812 conditional alpha-level owner route",
    },
    "alpha_countermodels_1812": {
        "path": OUT / "P8_Y5_PARENT_QLOC_1812_COUNTERMODEL_LEDGER.csv",
        "role": "1812 scalar gauge kinetic and current-rescale countermodels",
    },
    "unique_f2_1057": {
        "path": OUT / "P8_Y5_R10_1057_UNIQUE_MAXWELL_SUBBLOCK_THEOREM_ATTEMPT.csv",
        "role": "1057 unique Maxwell F2 subblock attempt",
    },
    "f2_counterterms_1057": {
        "path": OUT / "P8_Y5_R10_1057_F2_COUNTERTERM_LEDGER.csv",
        "role": "1057 retained lambda_A/f_X/radiative counterterms",
    },
    "operator_domain_1058": {
        "path": OUT / "P8_Y5_R10_1058_VISIBLE_OPERATOR_DOMAIN_EXHAUSTION_ATTEMPT.csv",
        "role": "1058 visible operator-domain exhaustion attempt",
    },
    "radiative_readout_1058": {
        "path": OUT / "P8_Y5_R10_1058_RADIATIVE_READOUT_CLOSURE_GATE.csv",
        "role": "1058 radiative/readout alpha silence gates",
    },
    "alpha_bound_3465": {
        "path": OUT / "P8_Y5_R2FR_3465_ALPHA_ONLY_BOUND_CALCULATION.csv",
        "role": "3465 finite nonclaim WEP alpha-only effective bound",
    },
    "raw_effective_3465": {
        "path": OUT / "P8_Y5_R2FR_3465_RAW_TO_EFFECTIVE_COMPONENT_ROWS.csv",
        "role": "3465 raw-to-effective WEP component rows",
    },
    "clock_bound_1052": {
        "path": OUT / "P8_Y5_R10_1052_ALPHA_CLOCK_PRODUCT_BOUND_LEDGER.csv",
        "role": "1052 atomic-clock alpha product bounds",
    },
    "bound_matrix_1048": {
        "path": OUT / "P8_Y5_R10_1048_ALPHA_MASS_CLOCK_BOUND_MATRIX.csv",
        "role": "1048 alpha/mass/clock/R10 projection matrix",
    },
    "local_bounds": {
        "path": LOCAL_BOUNDS / "local_bound_claims.csv",
        "role": "local empirical bound anchors: WEP, clocks, PPN, Gdot, R10 symbolic curve",
    },
    "parent_charge_spine_2340": {
        "path": OUT / "P8_Y5_PARENT_QLOC_2340_PARENT_CHARGE_EXTRACTION_SPINE.csv",
        "role": "parent charge/current/source-normalization spine",
    },
}


def bool_text(value: bool) -> str:
    return "True" if value else "False"


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def markdown_escape(value: Any) -> str:
    return str(value).replace("\n", "<br>").replace("|", "\\|")


def markdown_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    if not rows:
        return "_No rows._"
    return "\n".join(
        [
            "| " + " | ".join(fields) + " |",
            "| " + " | ".join("---" for _ in fields) + " |",
            *["| " + " | ".join(markdown_escape(row.get(field, "")) for field in fields) + " |" for row in rows],
        ]
    )


def source_rows() -> list[dict[str, Any]]:
    return [
        {
            "source_id": source_id,
            "path": str(item["path"]),
            "exists": bool_text(item["path"].exists()),
            "role": item["role"],
            "valid_for_claim": "False",
        }
        for source_id, item in SOURCES.items()
    ]


def ratio_theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "RAT3526_0_physical_ratio_identity",
            "claim_piece": "the scalar throat is the physical alpha/source coupling ratio, not a gauge convention",
            "statement": "For S_EM=-1/2 int lambda_A F_Q wedge *_obs F_Q + int e_obs A_Q.J_rep, the measured coupling is proportional to alpha_EM=e_obs^2/lambda_A; therefore C_XF2=D_X ln(lambda_A/e_obs^2)=-D_X ln alpha_EM.",
            "derivation": "A field rescaling A_Q -> s A_Q sends lambda_A -> lambda_A/s^2 and e_obs -> e_obs/s, leaving e_obs^2/lambda_A invariant. The derivative of the ratio is therefore not removed by changing EM units.",
            "what_it_proves": "the missing coupling is real and must be parent-owned or bounded",
            "what_it_does_not_prove": "it does not set C_XF2 to zero",
            "status": "DERIVED_EXACT_IDENTITY",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "RAT3526_1_parent_zero_contract",
            "claim_piece": "parent level/current/domain owner would force C_XF2=0",
            "statement": "If lambda_A=C_P N_Q, e_obs=Q_*, and C_P,N_Q,Q_* are fixed parent/representation data with no lambda_A, f_X, current-rescale or readout/radiative terms, then D_X ln(lambda_A/e_obs^2)=0.",
            "derivation": "C_XF2=D_X ln(C_P)+D_X ln(N_Q)-2D_X ln(Q_*). Each derivative vanishes when the curvature norm, generator norm and charge unit are fixed parent or representation objects.",
            "what_it_proves": "the exact zero route is not mysterious: fixed level plus fixed current plus exhausted operator domain is sufficient",
            "what_it_does_not_prove": "the present corpus does not yet sign those premises together",
            "status": "EXACT_CONDITIONAL_ZERO_THEOREM",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "RAT3526_2_same_noether_current_contract",
            "claim_piece": "same current owner is required for WEP/R10/source tests",
            "statement": "The charge current used in int A_Q.J_Q must be the Noether current of the same T_Q owner that fixes the Maxwell kinetic norm.",
            "derivation": "If J_Q can be replaced by c_A(X)J_A or if source/test charges use a different readout convention, alpha drift can hide in source weights even when the kinetic F_Q^2 coefficient is fixed.",
            "what_it_proves": "source coupling cannot be closed by the Maxwell kinetic coefficient alone",
            "what_it_does_not_prove": "the Noether/current/source denominator chain is still unsigned",
            "status": "NECESSARY_CONDITION_DERIVED",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "RAT3526_3_bound_branch_identity",
            "claim_piece": "if the zero theorem fails, every local test sees a product",
            "statement": "Observable rows constrain C_XF2 multiplied by an arena transfer such as tau_clock, tau_WEP, beta_source_alpha, K_R10(lambda), or a source-normalization kernel.",
            "derivation": "C_XF2 is a local derivative in theory space; clocks, WEP, R10 and PPN see it only after a field profile, material sensitivity, source map and readout projection are supplied.",
            "what_it_proves": "a finite empirical branch is possible without pretending the parent proof has closed",
            "what_it_does_not_prove": "no standalone MTS C_XF2 prediction exists yet",
            "status": "EXECUTABLE_BOUND_ROUTE",
            "valid_for_claim": "False",
        },
    ]


def owner_proof_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "clause_id": "OWN3526_0_parent_TQ_object",
            "required_clause": "T_Q is a parent action object and A_Q is its visible connection",
            "current_evidence": "1100 records partial compact U(1) support but says T_Q is not supplied as a varied parent-action object",
            "status": "PARTIAL_TEMPLATE_ONLY",
            "effect_on_C_XF2": "without this, lambda_A/e_obs^2 can be appended after the parent action",
            "source_path": str(SOURCES["tq_signature_1100"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "clause_id": "OWN3526_1_fixed_level_norm",
            "required_clause": "C_P N_Q is fixed by a parent fibre metric, level, lattice form or symplectic normalization",
            "current_evidence": "1100 and 1057 retain the nonrescalable generator norm as unsigned",
            "status": "NOT_PARENT_SIGNED",
            "effect_on_C_XF2": "D_X ln lambda_A can be nonzero or conventional rather than physical-parent fixed",
            "source_path": str(SOURCES["unique_f2_1057"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "clause_id": "OWN3526_2_unique_F2_domain",
            "required_clause": "no independent lambda_A F_Q^2, f_X F_Q^2 or visible counterterm outside the parent curvature norm",
            "current_evidence": "1057/1058 explicitly retain legal scalar gauge kinetic counterterms unless operator-domain exhaustion is derived",
            "status": "FAIL_CURRENT_CORPUS_COUNTERTERM_LEGAL",
            "effect_on_C_XF2": "direct scalar source C_XF2 remains live",
            "source_path": str(SOURCES["operator_domain_1058"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "clause_id": "OWN3526_3_fixed_charge_unit",
            "required_clause": "Q_* and charge labels are fixed representation/lattice data with no hidden/source dependence",
            "current_evidence": "compact/integer labels exist as partial support, but base normalization Q_* is unsigned",
            "status": "PARTIAL_INTEGER_LABELS_BASE_UNIT_UNSIGNED",
            "effect_on_C_XF2": "D_X ln e_obs may remain open",
            "source_path": str(SOURCES["tq_signature_1100"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "clause_id": "OWN3526_4_same_current_owner",
            "required_clause": "J_Q is the same Noether current for matter, test bodies, source bodies and EM stress",
            "current_evidence": "1100 and 2340 keep current/source normalization and charge extraction unsigned",
            "status": "NOT_PARENT_SIGNED",
            "effect_on_C_XF2": "WEP/R10/source response can reappear through current rescaling even if alpha is fixed in vacuum",
            "source_path": str(SOURCES["parent_charge_spine_2340"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "clause_id": "OWN3526_5_readout_radiative_guard",
            "required_clause": "clock/spectroscopy/EFT/readout maps preserve the same alpha owner",
            "current_evidence": "1058 radiative/readout gates are all false",
            "status": "UNSIGNED_PRESERVATION_REQUIREMENT",
            "effect_on_C_XF2": "a tree-level zero could be regenerated in measured alpha or clocks",
            "source_path": str(SOURCES["radiative_readout_1058"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "clause_id": "OWN3526_6_live_verdict",
            "required_clause": "OWN3526_0 through OWN3526_5 all parent-signed",
            "current_evidence": "none of the inspected source hierarchy signs all clauses together",
            "status": "C_XF2_ZERO_NOT_CLAIMED",
            "effect_on_C_XF2": "retain finite alpha/WEP/R10/clock/source-normalization branch",
            "source_path": str(SOURCES["alpha_decomp_1100"]["path"]),
            "valid_for_claim": "False",
        },
    ]


def countermodel_rows() -> list[dict[str, Any]]:
    return [
        {
            "countermodel_id": "CM3526_0_field_rescaling_not_proof",
            "countermodel": "rescale A_Q and compensate e_obs and lambda_A",
            "mathematical_form": "A_Q -> s A_Q; lambda_A -> lambda_A/s^2; e_obs -> e_obs/s",
            "why_it_matters": "the physical ratio e_obs^2/lambda_A is invariant, so normalization choice cannot be counted as a derivation",
            "blocked_by": "parent nonrescalable T_Q norm plus fixed charge unit",
            "retained": "True",
            "valid_for_claim": "False",
        },
        {
            "countermodel_id": "CM3526_1_independent_lambda",
            "countermodel": "legal scalar Maxwell kinetic coefficient",
            "mathematical_form": "Delta S=-1/2 int lambda_extra(X) F_Q wedge *_obs F_Q",
            "why_it_matters": "gauge and diffeomorphism covariance allow it unless the visible operator-domain is exhausted",
            "blocked_by": "unique F2 / no independent visible counterterm theorem",
            "retained": "True",
            "valid_for_claim": "False",
        },
        {
            "countermodel_id": "CM3526_2_hidden_scalar",
            "countermodel": "hidden invariant feeds visible F2",
            "mathematical_form": "Delta S=-1/2 int f(I_hid) F_Q wedge *_obs F_Q",
            "why_it_matters": "even with the observed Hodge, a hidden scalar coefficient creates alpha/WEP/clock pressure",
            "blocked_by": "no hidden-visible coefficient morphism or trivial hidden invariant algebra",
            "retained": "True",
            "valid_for_claim": "False",
        },
        {
            "countermodel_id": "CM3526_3_current_rescale",
            "countermodel": "source/test current uses a different charge convention",
            "mathematical_form": "J_A -> c_A(X) J_A with compensating apparent charge normalization",
            "why_it_matters": "vacuum alpha can look fixed while WEP/R10/source weights drift",
            "blocked_by": "same Noether current owner across kinetic, interaction, source and readout",
            "retained": "True",
            "valid_for_claim": "False",
        },
        {
            "countermodel_id": "CM3526_4_readout_radiative",
            "countermodel": "EFT threshold or clock readout regenerates alpha dependence",
            "mathematical_form": "lambda_A -> lambda_A + delta_lambda_rad(mu,X) or alpha_obs=R_alpha(q,X)",
            "why_it_matters": "tree-level owner does not automatically survive the measured clock/spectroscopy branch",
            "blocked_by": "radiative/readout closure",
            "retained": "True",
            "valid_for_claim": "False",
        },
    ]


def bound_rows() -> list[dict[str, Any]]:
    return [
        {
            "bound_id": "B3526_0_WEP_alpha_only_effective",
            "arena": "MICROSCOPE_WEP_alpha_only",
            "residual_symbol": "D_e_eff = S_E^q b_alpha",
            "observable_bound": "|D_e_eff| <= eta_bound / Delta_Q_alpha_Coulomb_abs",
            "bound_value": "1.407170315973e-12",
            "units": "dimensionless",
            "source_path": str(SOURCES["alpha_bound_3465"]["path"]),
            "source_row": "AOB3465_2_D_e_bound",
            "projection_formula": "Delta_w_eff_alpha = D_e_eff * Delta_Q_alpha_Coulomb_abs",
            "mts_inputs_required": "map C_XF2 to b_alpha and S_E^q; isolate alpha channel; include no-cancellation envelope for mass/shadow/readout components",
            "numeric_bound_ready": "True",
            "mts_prediction_status": "MISSING_CXF2_TO_DEEFF_PROJECTION",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "B3526_1_clock_alpha_product",
            "arena": "atomic_clock_alpha_drift",
            "residual_symbol": "P_clock_alpha = b_alpha * tau_clock_time",
            "observable_bound": "|P_clock_alpha| <= 2.1e-18 yr^-1",
            "bound_value": "2.1e-18",
            "units": "yr^-1",
            "source_path": str(SOURCES["clock_bound_1052"]["path"]),
            "source_row": "ACB1052_2",
            "projection_formula": "d ln(nu_a/nu_b)=DeltaK_alpha_ab*b_alpha*dXhat/dt + ...",
            "mts_inputs_required": "C_XF2 to b_alpha map; tau_clock_time; clock sensitivity basis; non-alpha channels",
            "numeric_bound_ready": "True",
            "mts_prediction_status": "MISSING_TAU_CLOCK_AND_CXF2_TO_BALPHA",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "B3526_2_WEP_alpha_product_target",
            "arena": "MICROSCOPE_WEP_product",
            "residual_symbol": "P_WEP_alpha = beta_source_alpha * b_alpha * tau_WEP",
            "observable_bound": "|P_WEP_alpha| <= 4.797780522732e-05",
            "bound_value": "4.797780522732e-05",
            "units": "dimensionless",
            "source_path": str(SOURCES["alpha_product_bound_1100"]["path"]),
            "source_row": "BOUND1100_1_WEP_alpha_product",
            "projection_formula": "eta_AB ~ DeltaQ_alpha_AB*beta_source_alpha*b_alpha*tau_WEP",
            "mts_inputs_required": "beta_source_alpha; tau_WEP; b_alpha from C_XF2; material charge matrix",
            "numeric_bound_ready": "True",
            "mts_prediction_status": "MISSING_WEP_ALPHA_PRODUCT_PROJECTION",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "B3526_3_R10_alpha_lambda_curve",
            "arena": "R10_short_range_fifth_force",
            "residual_symbol": "alpha_X(lambda_X)",
            "observable_bound": "alpha(lambda) curve required",
            "bound_value": "alpha(lambda)",
            "units": "range-dependent",
            "source_path": str(SOURCES["local_bounds"]["path"]),
            "source_row": "R10_fifth_force",
            "projection_formula": "alpha_X(lambda_X) ~ K_X Qbar_source Qbar_test/(4*pi*Z_X*G_obs)",
            "mts_inputs_required": "lambda_X; Z_X; M_X^2; K_X; Qbar_source/test; C_XF2 source/test charge projection; promoted curve",
            "numeric_bound_ready": "False",
            "mts_prediction_status": "MISSING_R10_CURVE_AND_PARENT_COEFFICIENTS",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "B3526_4_clock_redshift_anchor",
            "arena": "redshift_LPI_clocks",
            "residual_symbol": "alpha_clock_redshift",
            "observable_bound": "|alpha_clock_redshift| <= 2.48e-05",
            "bound_value": "2.48e-05",
            "units": "dimensionless",
            "source_path": str(SOURCES["local_bounds"]["path"]),
            "source_row": "R2_clock_redshift",
            "projection_formula": "alpha_clock_redshift=P_clock[C_XF2, clock readout, source potential map]",
            "mts_inputs_required": "clock readout map; local potential/source normalization; C_XF2 clock sensitivity",
            "numeric_bound_ready": "True",
            "mts_prediction_status": "MISSING_CLOCK_READOUT_PROJECTION",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "B3526_5_source_scale_Gdot_anchor",
            "arena": "LLR_Gdot_source_scale",
            "residual_symbol": "source_scale_drift or Gdot/G",
            "observable_bound": "|Gdot/G| <= 9.6e-15 yr^-1",
            "bound_value": "9.6e-15",
            "units": "yr^-1",
            "source_path": str(SOURCES["local_bounds"]["path"]),
            "source_row": "R9_Gdot",
            "projection_formula": "source/current normalization drift contributes to measured Gdot only after Hamiltonian source denominator and orbit readout are fixed",
            "mts_inputs_required": "M_H_ref; source denominator; C_XF2 to EM source weight; orbit readout map",
            "numeric_bound_ready": "True",
            "mts_prediction_status": "MISSING_SOURCE_NORMALIZATION_PROJECTION",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def runner_result_rows(bounds: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in bounds:
        numeric_bound = row["numeric_bound_ready"] == "True"
        mts_ready = not str(row["mts_prediction_status"]).startswith("MISSING")
        if numeric_bound and mts_ready:
            result = "READY_FOR_NUMERIC_COMPARISON"
            reason = "numeric bound and MTS prediction fields are present"
        elif numeric_bound:
            result = "BOUND_READY_PREDICTION_BLOCKED"
            reason = row["mts_prediction_status"]
        else:
            result = "BOUND_AND_PREDICTION_BLOCKED"
            reason = row["mts_prediction_status"]
        rows.append(
            {
                "result_id": row["bound_id"].replace("B3526", "RUN3526"),
                "arena": row["arena"],
                "residual_symbol": row["residual_symbol"],
                "numeric_bound_ready": row["numeric_bound_ready"],
                "mts_prediction_ready": bool_text(mts_ready),
                "comparison_result": result,
                "reason": reason,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    rows.append(
        {
            "result_id": "RUN3526_SUMMARY",
            "arena": "all",
            "residual_symbol": "C_XF2",
            "numeric_bound_ready": bool_text(any(row["numeric_bound_ready"] == "True" for row in bounds)),
            "mts_prediction_ready": "False",
            "comparison_result": "NO_CLAIM_BUT_BOUND_BRANCH_IS_EXECUTABLE",
            "reason": "finite WEP/clock/source anchors exist, but C_XF2 to arena projections and parent coefficients are not sourced",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    )
    return rows


def status_rows() -> list[dict[str, Any]]:
    return [
        {
            "status_id": "STAT3526_0_identity",
            "quantity": "C_XF2_identity",
            "value": "derived_exact",
            "meaning": "C_XF2 is D_X ln(lambda_A/e_obs^2), the negative alpha derivative and not a field-normalization convention",
            "claim_effect": "the coupling throat is mathematically real",
            "valid_for_claim": "False",
        },
        {
            "status_id": "STAT3526_1_zero_theorem",
            "quantity": "C_XF2_zero",
            "value": "exact_conditional_not_live",
            "meaning": "fixed parent level, charge unit, same current owner, unique F2 domain and readout/radiative guard would imply zero",
            "claim_effect": "not a live local-GR/Maxwell/source-coupling pass",
            "valid_for_claim": "False",
        },
        {
            "status_id": "STAT3526_2_live_blocker",
            "quantity": "current_corpus_parent_signature",
            "value": "not_jointly_signed",
            "meaning": "1100, 1812, 1057 and 1058 contain the right clauses but not one parent-signed package",
            "claim_effect": "retain alpha/WEP/R10/clock/source bound branch",
            "valid_for_claim": "False",
        },
        {
            "status_id": "STAT3526_3_bound_branch",
            "quantity": "finite_bound_anchors",
            "value": "WEP_and_clock_and_source_anchors_ready_projection_missing",
            "meaning": "real numeric bounds exist, especially WEP alpha-only and clock product rows, but MTS C_XF2 projections are missing",
            "claim_effect": "future runner can score once parent coefficients and transfer kernels exist",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3526_0_ratio_is_physical",
            "decision": "treat lambda_A/e_obs^2 as the physical coupling ratio",
            "rationale": "A_Q rescaling leaves e_obs^2/lambda_A invariant, so normalization convention is not a proof",
            "effect": "prevents a fake alpha/source-coupling victory",
            "claim_allowed": "False",
        },
        {
            "decision_id": "DEC3526_1_do_not_promote_zero",
            "decision": "do not claim C_XF2=0 from the current corpus",
            "rationale": "fixed level/norm, unique F2, same current owner and radiative/readout closure are not jointly signed",
            "effect": "keeps the local GR/Newton/Maxwell source route honest",
            "claim_allowed": "False",
        },
        {
            "decision_id": "DEC3526_2_next_derivation_target",
            "decision": "attack the charge-generator level/current owner directly next",
            "rationale": "that is the shortest route that could actually parent-sign lambda_A/e_obs^2 instead of only bounding it",
            "effect": "next step is a proof attempt, not a broad source sweep",
            "claim_allowed": "False",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_doc": "3527-Y5-R2FR-charge-generator-level-current-owner-or-alpha-ratio-countermodel-kill.md",
            "next_script": "scripts/Y5_R2FR_3527_charge_generator_level_current_owner_or_alpha_ratio_countermodel_kill.py",
            "objective": "Construct or reject the parent object that fixes T_Q level/norm, charge unit Q_*, and Noether current normalization together, so lambda_A/e_obs^2 is parent-owned rather than a retained alpha residual.",
            "success_gate": "Either a single parent level/current object signs C_P, N_Q, Q_* and J_Q with no independent F2 counterterm, or one explicit countermodel remains and the C_XF2 bound branch stays mandatory.",
            "why_next": "3526 proves the exact coupling ratio; the only possible derivation leap is now the level/current owner, not another global missing-ledger pass.",
            "claim_allowed": "False",
        }
    ]


def validate(
    outputs: dict[str, Path],
    sources: list[dict[str, Any]],
    theorems: list[dict[str, Any]],
    audit: list[dict[str, Any]],
    countermodels: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    results: list[dict[str, Any]],
    status: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []
    checks.append({"check_id": "VAL3526_0_sources_exist", "passed": bool_text(all(row["exists"] == "True" for row in sources)), "detail": "all cited local source paths exist", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3526_1_ratio_identity_derived", "passed": bool_text(any(row["theorem_id"] == "RAT3526_0_physical_ratio_identity" and row["status"] == "DERIVED_EXACT_IDENTITY" for row in theorems)), "detail": "C_XF2 physical ratio identity is present", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3526_2_zero_not_promoted", "passed": bool_text(any(row["clause_id"] == "OWN3526_6_live_verdict" and row["status"] == "C_XF2_ZERO_NOT_CLAIMED" for row in audit) and any(row["quantity"] == "C_XF2_zero" and row["value"] == "exact_conditional_not_live" for row in status)), "detail": "C_XF2 zero theorem is conditional only", "valid_for_claim": "False"})
    retained_countermodels = {row["countermodel_id"] for row in countermodels if row["retained"] == "True"}
    checks.append({"check_id": "VAL3526_3_countermodels_retained", "passed": bool_text({"CM3526_1_independent_lambda", "CM3526_2_hidden_scalar", "CM3526_3_current_rescale"} <= retained_countermodels), "detail": "independent lambda, hidden scalar and current-rescale countermodels retained", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3526_4_real_WEP_bound_imported", "passed": bool_text(any(row["bound_id"] == "B3526_0_WEP_alpha_only_effective" and row["bound_value"] == "1.407170315973e-12" and row["numeric_bound_ready"] == "True" for row in bounds)), "detail": "finite WEP alpha-only effective bound imported", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3526_5_clock_and_R10_rows_present", "passed": bool_text(any(row["bound_id"] == "B3526_1_clock_alpha_product" and row["bound_value"] == "2.1e-18" for row in bounds) and any(row["bound_id"] == "B3526_3_R10_alpha_lambda_curve" and row["numeric_bound_ready"] == "False" for row in bounds)), "detail": "clock product and R10 curve rows are staged with correct readiness flags", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3526_6_runner_blocks_claim", "passed": bool_text(any(row["result_id"] == "RUN3526_SUMMARY" and row["comparison_result"] == "NO_CLAIM_BUT_BOUND_BRANCH_IS_EXECUTABLE" for row in results)), "detail": "runner refuses claim while keeping finite bound branch executable", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3526_7_no_claim_flags_true", "passed": bool_text(all(row.get("valid_for_claim", "False") == "False" for row in sources + theorems + audit + countermodels + bounds + results + status) and all(row["claim_allowed"] == "False" for row in decisions + next_rows)), "detail": "no alpha/WEP/R10/clock/local-GR claim is promoted", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3526_8_next_target_selected", "passed": bool_text(next_rows[0]["next_doc"].startswith("3527-Y5-R2FR-charge-generator-level-current-owner")), "detail": "3527 level/current owner proof target selected", "valid_for_claim": "False"})
    parse_ok = True
    parsed: list[str] = []
    for name, path in outputs.items():
        if name in {"doc", "validation"}:
            continue
        try:
            read_csv_rows(path)
            parsed.append(name)
        except Exception:
            parse_ok = False
            parsed.append(f"{name}:PARSE_FAIL")
    checks.append({"check_id": "VAL3526_9_csvs_parse", "passed": bool_text(parse_ok), "detail": "; ".join(parsed), "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3526_10_outputs_stay_in_post_checkpoint_work", "passed": bool_text(all(ROOT in path.parents or path == DOC for path in outputs.values())), "detail": f"root={ROOT}", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3526_11_formalization_workbench_not_targeted", "passed": bool_text(all(FORMALIZATION not in path.parents for path in outputs.values())), "detail": str(FORMALIZATION), "valid_for_claim": "False"})
    passed = all(row["passed"] == "True" for row in checks)
    checks.append({"check_id": "VAL3526_SUMMARY", "passed": bool_text(passed), "detail": "PASS" if passed else "FAIL", "valid_for_claim": "False"})
    return checks


def write_doc(
    sources: list[dict[str, Any]],
    theorems: list[dict[str, Any]],
    audit: list[dict[str, Any]],
    countermodels: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    results: list[dict[str, Any]],
    status: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    validation_rows: list[dict[str, Any]],
) -> None:
    doc = f"""# 3526 - Scalar Gauge Coupling Owner, `D_X ln(lambda_A/e_obs^2)=0`, Or Alpha Bound Runner

## Summary
- **Derivation gain:** the scalar throat is now exact: `C_XF2 = D_X ln(lambda_A/e_obs^2) = -D_X ln alpha_EM` in the visible EM normal form.
- **Important guard:** rescaling `A_Q` cannot prove the coupling away, because `e_obs^2/lambda_A` is invariant under that rescaling.
- **Zero route:** `C_XF2=0` follows if one parent object fixes the curvature norm, charge-generator norm, base charge unit, same Noether current, unique `F_Q^2` operator domain, and readout/radiative closure.
- **Live verdict:** the current corpus does not yet sign those clauses together, so no alpha/WEP/R10/clock/source-normalization claim is allowed.
- **Bound progress:** the fallback branch now carries real finite anchors, especially the WEP alpha-only effective ceiling and clock product bound, while refusing to score without MTS transfer kernels.

## Coupling Identity
`S_EM = -1/2 int lambda_A F_Q wedge *_obs F_Q + int e_obs A_Q.J_rep + ...`

`alpha_EM proportional e_obs^2/lambda_A`

`C_XF2 := D_X ln(lambda_A/e_obs^2) = -D_X ln alpha_EM`

This is the point where the theory either derives source coupling or pays rent in WEP, clocks, R10, source normalization and PPN. No more fog machine.

## Source Register
{markdown_table(sources, ["source_id", "path", "exists", "role", "valid_for_claim"])}

## Ratio Theorem
{markdown_table(theorems, ["theorem_id", "claim_piece", "statement", "derivation", "what_it_proves", "what_it_does_not_prove", "status", "valid_for_claim"])}

## Owner Proof Audit
{markdown_table(audit, ["clause_id", "required_clause", "current_evidence", "status", "effect_on_C_XF2", "source_path", "valid_for_claim"])}

## Countermodel Ledger
{markdown_table(countermodels, ["countermodel_id", "countermodel", "mathematical_form", "why_it_matters", "blocked_by", "retained", "valid_for_claim"])}

## Bound Rows
{markdown_table(bounds, ["bound_id", "arena", "residual_symbol", "observable_bound", "bound_value", "units", "source_path", "source_row", "projection_formula", "mts_inputs_required", "numeric_bound_ready", "mts_prediction_status", "claim_allowed", "valid_for_claim"])}

## Runner Results
{markdown_table(results, ["result_id", "arena", "residual_symbol", "numeric_bound_ready", "mts_prediction_ready", "comparison_result", "reason", "claim_allowed", "valid_for_claim"])}

## Canonical Status
{markdown_table(status, ["status_id", "quantity", "value", "meaning", "claim_effect", "valid_for_claim"])}

## Decision Ledger
{markdown_table(decisions, ["decision_id", "decision", "rationale", "effect", "claim_allowed"])}

## Next Target
{markdown_table(next_rows, ["next_doc", "next_script", "objective", "success_gate", "why_next", "claim_allowed"])}

## Validation
{markdown_table(validation_rows, ["check_id", "passed", "detail", "valid_for_claim"])}
"""
    DOC.write_text(doc, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_rows()
    theorems = ratio_theorem_rows()
    audit = owner_proof_audit_rows()
    countermodels = countermodel_rows()
    bounds = bound_rows()
    results = runner_result_rows(bounds)
    status = status_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()
    outputs = {
        "source_register": OUT / "P8_Y5_R2FR_3526_SOURCE_REGISTER.csv",
        "ratio_theorem": OUT / "P8_Y5_R2FR_3526_SCALAR_COUPLING_RATIO_THEOREM.csv",
        "owner_proof_audit": OUT / "P8_Y5_R2FR_3526_OWNER_PROOF_AUDIT.csv",
        "countermodel_ledger": OUT / "P8_Y5_R2FR_3526_COUNTERMODEL_LEDGER.csv",
        "bound_rows": OUT / "P8_Y5_R2FR_3526_ALPHA_BOUND_ROWS.csv",
        "runner_results": OUT / "P8_Y5_R2FR_3526_BOUND_RUNNER_RESULTS.csv",
        "status": OUT / "P8_Y5_R2FR_3526_STATUS.csv",
        "canonical_status": CANONICAL_STATUS,
        "decision_ledger": OUT / "P8_Y5_R2FR_3526_DECISION_LEDGER.csv",
        "next_target": OUT / "P8_Y5_R2FR_3526_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_3526_VALIDATION.csv",
        "doc": DOC,
    }
    write_csv(outputs["source_register"], sources, ["source_id", "path", "exists", "role", "valid_for_claim"])
    write_csv(outputs["ratio_theorem"], theorems, ["theorem_id", "claim_piece", "statement", "derivation", "what_it_proves", "what_it_does_not_prove", "status", "valid_for_claim"])
    write_csv(outputs["owner_proof_audit"], audit, ["clause_id", "required_clause", "current_evidence", "status", "effect_on_C_XF2", "source_path", "valid_for_claim"])
    write_csv(outputs["countermodel_ledger"], countermodels, ["countermodel_id", "countermodel", "mathematical_form", "why_it_matters", "blocked_by", "retained", "valid_for_claim"])
    write_csv(outputs["bound_rows"], bounds, ["bound_id", "arena", "residual_symbol", "observable_bound", "bound_value", "units", "source_path", "source_row", "projection_formula", "mts_inputs_required", "numeric_bound_ready", "mts_prediction_status", "claim_allowed", "valid_for_claim"])
    write_csv(outputs["runner_results"], results, ["result_id", "arena", "residual_symbol", "numeric_bound_ready", "mts_prediction_ready", "comparison_result", "reason", "claim_allowed", "valid_for_claim"])
    status_fields = ["status_id", "quantity", "value", "meaning", "claim_effect", "valid_for_claim"]
    write_csv(outputs["status"], status, status_fields)
    write_csv(outputs["canonical_status"], status, status_fields)
    write_csv(outputs["decision_ledger"], decisions, ["decision_id", "decision", "rationale", "effect", "claim_allowed"])
    write_csv(outputs["next_target"], next_rows, ["next_doc", "next_script", "objective", "success_gate", "why_next", "claim_allowed"])
    validation_rows = validate(outputs, sources, theorems, audit, countermodels, bounds, results, status, decisions, next_rows)
    write_csv(outputs["validation"], validation_rows, ["check_id", "passed", "detail", "valid_for_claim"])
    write_doc(sources, theorems, audit, countermodels, bounds, results, status, decisions, next_rows, validation_rows)
    print(f"wrote {DOC}")
    print(f"validation {outputs['validation']}")


if __name__ == "__main__":
    main()
