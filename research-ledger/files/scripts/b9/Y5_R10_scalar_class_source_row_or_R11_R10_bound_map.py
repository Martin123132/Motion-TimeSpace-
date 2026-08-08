from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


STATUS = "Y5_R10_scalar_class_source_row_contract_and_R10_R11_bound_map_written_nonclaim"
CLAIM_CEILING = "scalar_class_coefficient_map_only_no_numeric_source_row_no_alpha_lambda_score_no_PPN_WEP_Gdot_pass_no_local_GR_claim"
NEXT_TARGET = "709-Y5-R10-scalar-class-parent-coefficient-hunt-or-zero-premise.md"

ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / "708-Y5-R10-scalar-class-source-row-or-R11-R10-bound-map.md"
FORMALIZATION_WORKBENCH = ROOT.parent / "formalization-workbench"
FORMALIZATION_CUTOFF = datetime.fromisoformat("2026-05-31T14:42:00")

OUTPUT_PATHS = [
    DOC_PATH,
    RESIDUALS / "P8_Y5_R10_708_SOURCE_REGISTER.csv",
    RESIDUALS / "P8_Y5_R10_708_SCALAR_CLASS_SOURCE_ROW_CONTRACT.csv",
    RESIDUALS / "P8_Y5_R10_708_LOCAL_EXPANSION_MAP.csv",
    RESIDUALS / "P8_Y5_R10_708_R10_ALPHA_LAMBDA_SCALAR_TEMPLATE.csv",
    RESIDUALS / "P8_Y5_R10_708_R11_SCALAR_OPERATOR_ROW.csv",
    RESIDUALS / "P8_Y5_R10_708_PPN_GDOT_WEP_MAP.csv",
    RESIDUALS / "P8_Y5_R10_708_AEH_UPDATE.csv",
    RESIDUALS / "P8_Y5_R10_708_CLAIM_GATE_EVALUATION.csv",
    RESIDUALS / "P8_Y5_R10_708_DECISION.csv",
    RESIDUALS / "P8_Y5_R10_708_NONCLAIM_SUMMARY.csv",
    RESIDUALS / "P8_Y5_BRR545_708_VALIDATION.csv",
]

SOURCE_PATHS = {
    "440_doc": ROOT / "440-metric-only-second-order-sector-reduction-attempt.md",
    "655_doc": ROOT / "655-Y5-R10-EH-operator-selection-under-WEP-closure-or-retained-R11-vector.md",
    "657_doc": ROOT / "657-Y5-R10-source-normalization-family-first-real-R11-fill.md",
    "704_prefactor": RESIDUALS / "P8_Y5_R10_704_EH_PREFACTOR_FORMALIZATION.csv",
    "704_gradient": RESIDUALS / "P8_Y5_R10_704_KAPPA_GRADIENT_BOUND_PACK.csv",
    "706_inventory": RESIDUALS / "P8_Y5_R10_706_AEH_TERM_INVENTORY.csv",
    "707_doc": ROOT / "707-Y5-R10-scalar-class-FR-prefactor-zero-or-AEH-bound.md",
    "707_validation": RESIDUALS / "P8_Y5_BRR545_707_VALIDATION.csv",
    "707_bound": RESIDUALS / "P8_Y5_R10_707_SCALAR_CLASS_AEH_BOUND_PACK.csv",
    "707_fallback": RESIDUALS / "P8_Y5_R10_707_R10_R11_FALLBACK_MAP.csv",
    "r10_template": RESIDUALS / "R10_alpha_lambda_curve_TEMPLATE.csv",
    "r11_template": RESIDUALS / "R11_nonEH_operator_vector_TEMPLATE.csv",
    "r11_skeleton": RESIDUALS / "R11_MTS_MINIMUM_EXECUTABLE_VECTOR_SKELETON.csv",
    "r11_link": RESIDUALS / "R11_R10_LINK_REQUIREMENTS.csv",
    "r11_status": RESIDUALS / "R11_EXECUTABLE_VECTOR_STATUS.csv",
    "local_template": RESIDUALS / "MTS_local_residual_predictions_TEMPLATE.csv",
}


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def source_list(*source_ids: str) -> str:
    return ";".join(str(SOURCE_PATHS[source_id]) for source_id in source_ids)


def validation_failures(source_id: str) -> list[dict[str, str]]:
    path = SOURCE_PATHS[source_id]
    if not path.exists():
        return [{"check_id": "missing", "result": "fail", "detail": str(path)}]
    return [row for row in read_csv(path) if row.get("result") != "pass"]


def formalization_changed_count() -> int:
    if not FORMALIZATION_WORKBENCH.exists():
        return -1
    return sum(
        1
        for candidate in FORMALIZATION_WORKBENCH.rglob("*")
        if candidate.is_file() and datetime.fromtimestamp(candidate.stat().st_mtime) > FORMALIZATION_CUTOFF
    )


def source_register_rows() -> list[dict[str, str]]:
    generated = now()
    roles = {
        "440_doc": "metric-only reduction source for scalar/class retained sector",
        "655_doc": "R11 operator family and observable affected-row source",
        "657_doc": "source-normalization/R10/R11 residual source",
        "704_prefactor": "A_EH and epsilon_G formalization",
        "704_gradient": "kappa-gradient bound pack",
        "706_inventory": "A_EH term inventory containing scalar_class",
        "707_doc": "immediate scalar/class zero/bound predecessor",
        "707_validation": "707 validation gate",
        "707_bound": "707 scalar AEH bound pack",
        "707_fallback": "707 R10/R11 fallback map",
        "r10_template": "canonical R10 alpha(lambda) row shape",
        "r11_template": "canonical R11 non-EH operator vector shape",
        "r11_skeleton": "minimum executable R11 scalar/class row source",
        "r11_link": "R11-to-R10 link requirements",
        "r11_status": "R11 executable-vector status ledger",
        "local_template": "local residual prediction row template",
    }
    return [
        {
            "source_id": source_id,
            "path": str(path),
            "exists": "true" if path.exists() else "false",
            "role": roles[source_id],
            "generated_utc": generated,
        }
        for source_id, path in SOURCE_PATHS.items()
    ]


def source_row_contract_rows() -> list[dict[str, str]]:
    generated = now()
    rows = [
        (
            "SCR708_0_parent_action_form",
            "parent scalar/class action",
            "S_scalar = int sqrt(-g)[A_EH(u) R - 1/2 Z_IJ(u) grad u^I grad u^J - V(u)] + S_matter[B_A^2(u)g,psi_A]",
            "MISSING_PARENT_ACTION_COEFFICIENT_SOURCE",
            "action density",
            "defines whether scalar/class branch exists as physics or closure",
        ),
        (
            "SCR708_1_background",
            "local background point",
            "u0^I=(phi0,C0,...) and A_EH(u0)",
            "MISSING_BACKGROUND_VALUE",
            "field units",
            "sets delta_AEH_scalar=A_EH(u0)-1",
        ),
        (
            "SCR708_2_prefactor_gradient",
            "EH prefactor derivatives",
            "a_I = partial_I ln A_EH evaluated at u0",
            "MISSING_PREFACTOR_GRADIENT_VECTOR",
            "inverse field units",
            "sets epsilon_G, grad ln A_EH, frame transfer, and scalar force strength",
        ),
        (
            "SCR708_3_kinetic_metric",
            "kinetic metric",
            "Z_IJ(u0) positive/degenerate/gauge-classified",
            "MISSING_KINETIC_METRIC",
            "dimensionless_or_field_units",
            "needed to canonicalize scalar modes",
        ),
        (
            "SCR708_4_mass_matrix",
            "mass/range matrix",
            "M_IJ^2 = partial_I partial_J V_eff(u0)",
            "MISSING_MASS_MATRIX",
            "mass^2",
            "sets lambda_a = hbar/(m_a c) for R10",
        ),
        (
            "SCR708_5_matter_charges",
            "source/test charges",
            "b_A,I = partial_I ln m_A(u) or theorem b_A,I=0",
            "MISSING_SOURCE_TEST_CHARGE_VECTOR",
            "inverse field units",
            "sets WEP and R10 source dependence",
        ),
        (
            "SCR708_6_diagonalization",
            "canonical eigenmodes",
            "E_a^I diagonalizes Z_IJ and M_IJ^2 with normalized modes s_a",
            "MISSING_CANONICAL_DIAGONALIZATION",
            "mixed",
            "turns symbolic field-space entries into observable modes",
        ),
        (
            "SCR708_7_frame_normalization",
            "observed-frame convention",
            "specify Jordan/Einstein/readout frame and measured-G normalization",
            "MISSING_FRAME_AND_GREF_CONVENTION",
            "dimensionless",
            "prevents double-counting source normalization as a fifth force",
        ),
        (
            "SCR708_8_bound_sources",
            "bound source files",
            "R10 alpha(lambda), PPN gamma/beta, WEP eta, Gdot/G bound source paths",
            "MISSING_BOUND_SOURCE_PATHS",
            "mixed",
            "required before any comparison or pass/fail claim",
        ),
        (
            "SCR708_9_verdict",
            "claim-ready scalar/class source row",
            "all source-row fields above are numeric/theorem-zero and sourced",
            "fail_current_corpus",
            "mixed",
            "source row is a contract only",
        ),
    ]
    return [
        {
            "contract_id": contract_id,
            "required_object": required_object,
            "mathematical_definition": definition,
            "current_value_or_status": status,
            "units": units,
            "why_needed": why_needed,
            "valid_for_claim": "false",
            "source_paths": source_list("707_doc", "707_bound", "440_doc", "655_doc", "704_prefactor"),
            "generated_utc": generated,
        }
        for contract_id, required_object, definition, status, units, why_needed in rows
    ]


def local_expansion_map_rows() -> list[dict[str, str]]:
    generated = now()
    rows = [
        (
            "LEM708_0_field_multiplet",
            "u^I=(phi,C,...)",
            "collect scalar/class variables that can multiply R or couple to matter",
            "definition_map_only",
            "all later maps require a concrete list of I",
        ),
        (
            "LEM708_1_delta_AEH",
            "delta_AEH_scalar = A_EH(u0)-1",
            "if A_EH=F(phi,C), this is F(phi0,C0)-1",
            "symbolic_formula_no_value",
            "fills SAB707_0 only after A_EH(u0) is sourced",
        ),
        (
            "LEM708_2_epsilon_G",
            "epsilon_G_scalar = abs(1/A_EH(u0)-1) approx abs(delta_AEH_scalar)",
            "small-residual branch uses linearized prefactor mismatch",
            "symbolic_formula_no_value",
            "feeds source-normalization/local Newton gate",
        ),
        (
            "LEM708_3_gradient",
            "grad_mu ln A_EH = a_I grad_mu u^I",
            "a_I=partial_I ln A_EH|u0",
            "symbolic_formula_no_value",
            "feeds kappa-gradient, clock, and time-drift tests",
        ),
        (
            "LEM708_4_canonical_modes",
            "s_a = E_a^I delta u_I",
            "E diagonalizes kinetic and mass matrices",
            "symbolic_formula_no_value",
            "required before alpha(lambda) is meaningful",
        ),
        (
            "LEM708_5_range",
            "lambda_a = hbar/(m_a c)",
            "or lambda_a=1/m_a in natural units with units stated",
            "symbolic_formula_no_value",
            "sets R10 x-axis",
        ),
        (
            "LEM708_6_source_charge",
            "q_Aa = b_A,I E_a^I plus any frame-transfer term",
            "b_A,I=partial_I ln m_A or equivalent local source charge",
            "symbolic_formula_no_value",
            "sets WEP and fifth-force amplitude",
        ),
        (
            "LEM708_7_R10_alpha",
            "alpha_AB(lambda_a) = N_frame q_Aa q_Ba",
            "N_frame must be fixed by measured-G/source-normalization convention",
            "normalization_ambiguous_unscored",
            "prevents false alpha(lambda) pass",
        ),
        (
            "LEM708_8_PPN",
            "gamma-1, beta-1 = functions of canonical scalar coupling and derivative",
            "universal scalar-tensor formulas may be used only after convention/source charge is fixed",
            "formula_family_identified_not_claimed",
            "maps retained scalar branch to R3/R4",
        ),
        (
            "LEM708_9_WEP_Gdot",
            "eta_AB depends on q_Aa-q_Ba; Gdot/G includes -partial_t ln A_EH plus source-mass drift",
            "species and time dependence must be separated from calibration",
            "symbolic_formula_no_value",
            "maps retained scalar branch to R1/R9",
        ),
        (
            "LEM708_10_verdict",
            "symbolic map exists but is not executable",
            "coefficient source row absent",
            "fail_current_corpus",
            "no R10/R11/PPN/WEP/Gdot claim",
        ),
    ]
    return [
        {
            "map_id": map_id,
            "quantity": quantity,
            "formula_or_definition": formula,
            "current_status": status,
            "claim_effect": effect,
            "valid_for_claim": "false",
            "source_paths": source_list("704_prefactor", "704_gradient", "707_bound", "707_fallback", "r10_template", "local_template"),
            "generated_utc": generated,
        }
        for map_id, quantity, formula, status, effect in rows
    ]


def r10_alpha_template_rows() -> list[dict[str, str]]:
    generated = now()
    rows = [
        (
            "MTS_scalar_class_retained_branch",
            "post_checkpoint_708_scalar_class",
            "R10_alpha_lambda_scalar_class_template",
            "MISSING_lambda_a_from_mass_matrix",
            "m",
            "MISSING_alpha_AB_from_source_charges",
            "MISSING_REAL_R10_BOUND_CURVE_OR_SOURCE",
            "R10_alpha_lambda_curve_TEMPLATE.csv;R10_alpha_lambda_bound_curve_DIGITIZED.csv_if_available",
            "Yukawa_potential_or_mapped_non_Yukawa_envelope",
            "retained_unfilled",
            "LEM708_5;LEM708_6;LEM708_7",
            "MISSING_SOURCE_ROW_PATH",
            "same observed frame; canonical scalar mode; measured-G convention fixed; source/test charges sourced",
            "false",
            "scalar/class alpha(lambda) row is source-ready only; no numeric curve or bound comparison is claimed",
        )
    ]
    fieldnames = [
        "model_id",
        "branch_id",
        "curve_id",
        "lambda_value",
        "lambda_units",
        "alpha_predicted",
        "alpha_bound",
        "alpha_bound_source",
        "force_law_form",
        "derivation_status",
        "formula_reference",
        "source_file",
        "assumptions",
        "valid_for_claim",
        "notes",
    ]
    return [dict(zip(fieldnames, row)) | {"generated_utc": generated} for row in rows]


def r11_scalar_operator_rows() -> list[dict[str, str]]:
    generated = now()
    rows = [
        {
            "model_id": "MTS_scalar_class_retained_branch",
            "branch_id": "post_checkpoint_708_scalar_class",
            "vector_id": "R11_scalar_class_operator_vector_row",
            "operator_family": "scalar_tensor_class_metric",
            "coefficient_symbol": "F_phi_C_or_delta_AEH_scalar",
            "coefficient_value": "MISSING_NUMERIC_OR_DERIVED_ZERO_COEFFICIENT",
            "coefficient_units": "dimensionless_for_F; field_units_for_derivatives",
            "normalization": "MISSING_SCALAR_SOURCE_AND_EH_NORMALIZATION",
            "operator_form": "sqrt(-g)[A_EH(u) R - 1/2 Z_IJ(u) grad u^I grad u^J - V(u)] plus matter frame B_A(u)",
            "weak_field_map": "MISSING_CLOCK_PPN_GDOT_RANGE_WEP_MAP; see P8_Y5_R10_708_LOCAL_EXPANSION_MAP.csv",
            "affected_rows": "R1;R2;R3;R4;R9;R10;R11",
            "induced_observable": "eta_WEP;clock_residual;gamma_minus_1;beta_minus_1;Gdot_over_G;alpha(lambda);operator_ledger",
            "predicted_residual_or_bound_source": "MISSING_RESIDUAL_BOUND_OR_THEOREM_SOURCE",
            "derivation_status": "retained_unfilled",
            "formula_reference": "P8_Y5_R10_708_LOCAL_EXPANSION_MAP.csv",
            "source_file": "MISSING_PARENT_COEFFICIENT_SOURCE",
            "assumptions": "MISSING_FRAME_LOCALITY_SOURCE_NORMALIZATION_RANGE_AND_SPECIES_ASSUMPTIONS",
            "valid_for_claim": "false",
            "notes": "parseable scalar/class R11 row only; executable once coefficient row, diagonalization, source charges, and bounds are real",
            "source_paths": source_list("r11_template", "r11_skeleton", "r11_status", "707_fallback", "440_doc", "655_doc"),
            "generated_utc": generated,
        }
    ]
    return rows


def ppn_gdot_wep_rows() -> list[dict[str, str]]:
    generated = now()
    rows = [
        (
            "PGW708_0_R1_WEP",
            "R1",
            "eta_AB",
            "eta_AB requires species-dependent q_Aa and q_Ba; universal zero charge gives theorem-zero only if parent-signed",
            "MISSING_SOURCE_TEST_CHARGE_VECTOR",
            "false",
        ),
        (
            "PGW708_1_R3_gamma",
            "R3",
            "gamma_minus_1",
            "gamma-1 is a scalar-coupling function after canonical normalization and measured-frame convention",
            "MISSING_GAMMA_MAP",
            "false",
        ),
        (
            "PGW708_2_R4_beta",
            "R4",
            "beta_minus_1",
            "beta-1 requires derivative of scalar coupling and nonlinear source normalization",
            "MISSING_BETA_MAP",
            "false",
        ),
        (
            "PGW708_3_R9_Gdot",
            "R9",
            "Gdot_over_G",
            "Gdot/G includes -partial_t ln A_EH plus matter/source drift; calibration offsets must be separated",
            "MISSING_TIME_DERIVATIVE_AND_CALIBRATION_MAP",
            "false",
        ),
        (
            "PGW708_4_R10_alpha",
            "R10",
            "alpha(lambda)",
            "alpha(lambda_a)=N_frame q_Aa q_Ba after canonical scalar range and source charges are sourced",
            "MISSING_ALPHA_LAMBDA_MAP",
            "false",
        ),
        (
            "PGW708_5_R11_operator",
            "R11",
            "scalar_tensor_class_metric",
            "R11 scalar row is retained unless coefficient is zero/theorem-bounded or mapped to residuals",
            "MISSING_EXECUTABLE_R11_SCALAR_ROW",
            "false",
        ),
        (
            "PGW708_6_verdict",
            "R1_R3_R4_R9_R10_R11",
            "scalar local residual vector",
            "map shape exists but no row is score-ready",
            "fail_current_corpus",
            "false",
        ),
    ]
    return [
        {
            "row_id": row_id,
            "arena": arena,
            "observable": observable,
            "map_requirement": requirement,
            "current_status": status,
            "valid_for_claim": valid,
            "source_paths": source_list("local_template", "r11_link", "r11_status", "707_fallback", "657_doc"),
            "generated_utc": generated,
        }
        for row_id, arena, observable, requirement, status, valid in rows
    ]


def aeh_update_rows() -> list[dict[str, str]]:
    generated = now()
    rows = [
        (
            "AEHU708_0_scalar_delta",
            "delta_AEH_scalar",
            "delta_AEH_scalar=A_EH(u0)-1",
            "MISSING_BACKGROUND_VALUE_OR_ZERO_THEOREM",
            "retained_unfilled_after_708",
        ),
        (
            "AEHU708_1_scalar_gradient",
            "grad_ln_AEH_scalar",
            "grad_mu ln A_EH=a_I grad_mu u^I",
            "MISSING_PREFACTOR_GRADIENT_AND_FIELD_PROFILE",
            "retained_unfilled_after_708",
        ),
        (
            "AEHU708_2_epsilon_G",
            "epsilon_G_scalar",
            "epsilon_G_scalar=abs(1/A_EH(u0)-1)",
            "MISSING_AEH_VALUE",
            "retained_unfilled_after_708",
        ),
        (
            "AEHU708_3_AEH_sum",
            "A_EH",
            "A_EH=1+delta_AEH_scalar+remaining delta_AEH_i",
            "MISSING_CHANNEL_VALUES_OR_ZERO_THEOREMS",
            "still_unfilled_after_708",
        ),
    ]
    return [
        {
            "update_id": update_id,
            "target": target,
            "formula": formula,
            "value_or_bound": value,
            "current_status": status,
            "valid_for_claim": "false",
            "source_paths": source_list("704_prefactor", "706_inventory", "707_bound"),
            "generated_utc": generated,
        }
        for update_id, target, formula, value, status in rows
    ]


def claim_gate_rows() -> list[dict[str, str]]:
    generated = now()
    rows = [
        ("CG708_0_sources", "all source files load", "source register exists check", "pass_structure", "allows checkpoint only"),
        ("CG708_1_prior_707", "707 validation clean", "707 validation has no failures", "pass_structure", "inherits clean predecessor"),
        ("CG708_2_source_contract", "scalar/class source row", "contract written but MISSING fields remain", "fail_blocked", "no scalar coefficient claim"),
        ("CG708_3_diagonalization", "canonical scalar modes", "MISSING_CANONICAL_DIAGONALIZATION", "fail_blocked", "no scalar range or alpha amplitude"),
        ("CG708_4_R10_curve", "R10 alpha(lambda)", "MISSING lambda, alpha, and real bound curve", "fail_blocked", "no R10 score"),
        ("CG708_5_PPN_WEP_Gdot", "PPN/WEP/Gdot maps", "MISSING charge/frame/time maps", "fail_blocked", "no local residual score"),
        ("CG708_6_R11_row", "R11 scalar row", "retained_unfilled", "fail_blocked", "no executable R11 scalar branch"),
        ("CG708_7_AEH", "A_EH fill", "MISSING_CHANNEL_VALUES_OR_ZERO_THEOREMS", "fail_blocked", "no A_EH or local-GR promotion"),
    ]
    return [
        {
            "gate_id": gate_id,
            "gate": gate,
            "observed_state": observed,
            "result": result,
            "claim_effect": effect,
            "valid_for_claim": "false",
            "source_paths": source_list("707_validation", "707_bound", "707_fallback", "r10_template", "r11_skeleton"),
            "generated_utc": generated,
        }
        for gate_id, gate, observed, result, effect in rows
    ]


def decision_rows() -> list[dict[str, str]]:
    generated = now()
    rows = [
        (
            "D708_0_map",
            "scalar/class retained branch",
            "symbolic_map_written",
            "delta_AEH, grad ln A_EH, scalar range, source charge, R10 alpha, PPN, WEP, and Gdot dependencies are now explicit",
            NEXT_TARGET,
        ),
        (
            "D708_1_claim",
            "claim status",
            "blocked_nonclaim",
            "no parent coefficient row, diagonalization, source charges, or bound source rows exist",
            NEXT_TARGET,
        ),
        (
            "D708_2_best_next",
            "next derivation route",
            "selected",
            "hunt parent coefficient source for A_EH(u), Z_IJ, V, B_A or prove scalar/class zero premise",
            NEXT_TARGET,
        ),
    ]
    return [
        {
            "decision_id": decision_id,
            "target": target,
            "result": result,
            "reason": reason,
            "next_action": next_action,
            "valid_for_claim": "false",
            "generated_utc": generated,
        }
        for decision_id, target, result, reason, next_action in rows
    ]


def summary_rows() -> list[dict[str, str]]:
    generated = now()
    return [
        {
            "summary_id": "S708_0",
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "main_result": "scalar/class branch now has an exact source-row contract and symbolic local residual map, but no executable coefficient row",
            "hardest_blocker": "missing parent coefficients for A_EH(u), kinetic metric, mass/range, matter charges, and frame/source normalization",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated,
        }
    ]


def has_missing_marker(row: dict[str, str]) -> bool:
    return "MISSING" in " ".join(str(value) for value in row.values())


def all_generated_rows(*groups: list[dict[str, str]]) -> list[dict[str, str]]:
    return [row for group in groups for row in group]


def validation_rows(
    source_rows,
    contract,
    expansion,
    r10,
    r11,
    ppn,
    aeh,
    gates,
    decisions,
    summary,
) -> list[dict[str, str]]:
    generated = now()
    missing_sources = [row["source_id"] for row in source_rows if row["exists"] != "true"]
    prior_failures = len(validation_failures("707_validation"))
    contract_keys = {
        "SCR708_0_parent_action_form",
        "SCR708_1_background",
        "SCR708_2_prefactor_gradient",
        "SCR708_3_kinetic_metric",
        "SCR708_4_mass_matrix",
        "SCR708_5_matter_charges",
        "SCR708_6_diagonalization",
        "SCR708_7_frame_normalization",
        "SCR708_8_bound_sources",
        "SCR708_9_verdict",
    }
    expansion_keys = {
        "LEM708_1_delta_AEH",
        "LEM708_3_gradient",
        "LEM708_5_range",
        "LEM708_6_source_charge",
        "LEM708_7_R10_alpha",
        "LEM708_8_PPN",
        "LEM708_9_WEP_Gdot",
        "LEM708_10_verdict",
    }
    contract_complete = contract_keys.issubset({row["contract_id"] for row in contract})
    expansion_complete = expansion_keys.issubset({row["map_id"] for row in expansion})
    r10_template_only = len(r10) == 1 and r10[0]["valid_for_claim"] == "false" and has_missing_marker(r10[0])
    r11_retained = len(r11) == 1 and r11[0]["operator_family"] == "scalar_tensor_class_metric" and r11[0]["derivation_status"] == "retained_unfilled"
    ppn_complete = {"R1", "R3", "R4", "R9", "R10", "R11"}.issubset({row["arena"] for row in ppn})
    aeh_unfilled = all(row["valid_for_claim"] == "false" for row in aeh) and any(has_missing_marker(row) for row in aeh)
    gates_block = all(row["valid_for_claim"] == "false" for row in gates) and any(row["result"] == "fail_blocked" for row in gates)
    no_claim = all(row.get("valid_for_claim") != "true" for row in all_generated_rows(contract, expansion, r10, r11, ppn, aeh, gates, decisions, summary))
    scoped = all(str(path).startswith(str(ROOT)) for path in OUTPUT_PATHS)
    formalization_count = formalization_changed_count()
    next_selected = decisions[-1]["next_action"] == NEXT_TARGET and summary[0]["next_target"] == NEXT_TARGET
    checks = [
        ("V708_0_source_paths_exist", not missing_sources, "all cited source paths exist" if not missing_sources else "missing=" + ";".join(missing_sources)),
        ("V708_1_prior_707_clean", prior_failures == 0, f"707_validation_failures={prior_failures}"),
        ("V708_2_source_contract_complete", contract_complete, f"contract_rows={len(contract)}"),
        ("V708_3_expansion_map_complete", expansion_complete, f"expansion_rows={len(expansion)}"),
        ("V708_4_R10_template_nonclaim", r10_template_only, "R10 scalar template has MISSING markers and valid_for_claim=false"),
        ("V708_5_R11_scalar_row_retained", r11_retained, "scalar_tensor_class_metric retained_unfilled"),
        ("V708_6_PPN_WEP_Gdot_map_complete", ppn_complete, "arenas=R1;R3;R4;R9;R10;R11"),
        ("V708_7_AEH_update_unfilled", aeh_unfilled, "AEH scalar fields remain MISSING/nonclaim"),
        ("V708_8_gates_block_claim", gates_block, f"gate_rows={len(gates)}"),
        ("V708_9_no_claim_rows_promoted", no_claim, "all generated rows valid_for_claim=false"),
        ("V708_10_next_target_selected", next_selected, NEXT_TARGET),
        ("V708_11_outputs_scoped", scoped, "all outputs under post-checkpoint-work"),
        ("V708_12_formalization_workbench_untouched", formalization_count == 0, f"formalization_changed_after_cutoff={formalization_count}"),
        ("V708_13_status_nonclaim", "no_numeric_source_row" in CLAIM_CEILING and "no_local_GR_claim" in CLAIM_CEILING, CLAIM_CEILING),
    ]
    return [{"check_id": cid, "result": "pass" if ok else "fail", "detail": detail, "generated_utc": generated} for cid, ok, detail in checks]


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join("---" for _ in columns) + " |"
    body = [
        "| " + " | ".join(str(row.get(column, "")).replace("\n", " ").replace("|", "\\|") for column in columns) + " |"
        for row in rows
    ]
    return "\n".join([header, divider, *body]) + "\n"


def write_doc(source_rows, contract, expansion, r10, r11, ppn, aeh, gates, decisions, summary, validation) -> None:
    doc = f"""# 708 - Y5 R10 Scalar Class Source Row Or R11 R10 Bound Map

## Verdict

708 converts the surviving scalar/class coupling into a precise executable contract:

```text
u^I = (phi, C, ...)
S_scalar = int sqrt(-g)[A_EH(u) R - 1/2 Z_IJ(u) grad u^I grad u^J - V(u)]
delta_AEH_scalar = A_EH(u0)-1
grad_mu ln A_EH = (partial_I ln A_EH)|u0 grad_mu u^I
lambda_a = hbar/(m_a c)
alpha_AB(lambda_a) = N_frame q_Aa q_Ba
```

That is the useful step: the scalar/class branch is no longer a vague "coupling problem". It is a concrete list of parent coefficients, diagonalization data, source charges, frame convention, and bound sources.

The current corpus still does **not** supply those inputs. So 708 writes the source-ready row and R10/R11/PPN/WEP/Gdot map, but keeps every generated row `valid_for_claim=false`.

| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## Scalar Class Source Row Contract

{markdown_table(contract, ["contract_id", "required_object", "current_value_or_status", "units", "why_needed", "valid_for_claim"])}

## Local Expansion Map

{markdown_table(expansion, ["map_id", "quantity", "formula_or_definition", "current_status", "claim_effect", "valid_for_claim"])}

## R10 Alpha Lambda Scalar Template

{markdown_table(r10, ["model_id", "branch_id", "curve_id", "lambda_value", "alpha_predicted", "alpha_bound", "derivation_status", "valid_for_claim"])}

## R11 Scalar Operator Row

{markdown_table(r11, ["operator_family", "coefficient_symbol", "coefficient_value", "weak_field_map", "affected_rows", "derivation_status", "valid_for_claim"])}

## PPN Gdot WEP Map

{markdown_table(ppn, ["row_id", "arena", "observable", "current_status", "valid_for_claim"])}

## AEH Update

{markdown_table(aeh, ["update_id", "target", "formula", "value_or_bound", "current_status", "valid_for_claim"])}

## Claim Gate Evaluation

{markdown_table(gates, ["gate_id", "gate", "observed_state", "result", "claim_effect", "valid_for_claim"])}

## Decision

{markdown_table(decisions, ["decision_id", "target", "result", "reason", "next_action", "valid_for_claim"])}

## Nonclaim Summary

{markdown_table(summary, ["summary_id", "status", "claim_ceiling", "main_result", "hardest_blocker", "next_target", "valid_for_claim"])}

## Source Register

{markdown_table(source_rows, ["source_id", "path", "exists", "role"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


def main() -> None:
    source_rows = source_register_rows()
    contract = source_row_contract_rows()
    expansion = local_expansion_map_rows()
    r10 = r10_alpha_template_rows()
    r11 = r11_scalar_operator_rows()
    ppn = ppn_gdot_wep_rows()
    aeh = aeh_update_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    summary = summary_rows()
    validation = validation_rows(source_rows, contract, expansion, r10, r11, ppn, aeh, gates, decisions, summary)

    write_csv(
        OUTPUT_PATHS[1],
        source_rows,
        ["source_id", "path", "exists", "role", "generated_utc"],
    )
    write_csv(
        OUTPUT_PATHS[2],
        contract,
        [
            "contract_id",
            "required_object",
            "mathematical_definition",
            "current_value_or_status",
            "units",
            "why_needed",
            "valid_for_claim",
            "source_paths",
            "generated_utc",
        ],
    )
    write_csv(
        OUTPUT_PATHS[3],
        expansion,
        ["map_id", "quantity", "formula_or_definition", "current_status", "claim_effect", "valid_for_claim", "source_paths", "generated_utc"],
    )
    write_csv(
        OUTPUT_PATHS[4],
        r10,
        [
            "model_id",
            "branch_id",
            "curve_id",
            "lambda_value",
            "lambda_units",
            "alpha_predicted",
            "alpha_bound",
            "alpha_bound_source",
            "force_law_form",
            "derivation_status",
            "formula_reference",
            "source_file",
            "assumptions",
            "valid_for_claim",
            "notes",
            "generated_utc",
        ],
    )
    write_csv(
        OUTPUT_PATHS[5],
        r11,
        [
            "model_id",
            "branch_id",
            "vector_id",
            "operator_family",
            "coefficient_symbol",
            "coefficient_value",
            "coefficient_units",
            "normalization",
            "operator_form",
            "weak_field_map",
            "affected_rows",
            "induced_observable",
            "predicted_residual_or_bound_source",
            "derivation_status",
            "formula_reference",
            "source_file",
            "assumptions",
            "valid_for_claim",
            "notes",
            "source_paths",
            "generated_utc",
        ],
    )
    write_csv(
        OUTPUT_PATHS[6],
        ppn,
        ["row_id", "arena", "observable", "map_requirement", "current_status", "valid_for_claim", "source_paths", "generated_utc"],
    )
    write_csv(
        OUTPUT_PATHS[7],
        aeh,
        ["update_id", "target", "formula", "value_or_bound", "current_status", "valid_for_claim", "source_paths", "generated_utc"],
    )
    write_csv(
        OUTPUT_PATHS[8],
        gates,
        ["gate_id", "gate", "observed_state", "result", "claim_effect", "valid_for_claim", "source_paths", "generated_utc"],
    )
    write_csv(
        OUTPUT_PATHS[9],
        decisions,
        ["decision_id", "target", "result", "reason", "next_action", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUTPUT_PATHS[10],
        summary,
        ["summary_id", "status", "claim_ceiling", "main_result", "hardest_blocker", "next_target", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUTPUT_PATHS[11],
        validation,
        ["check_id", "result", "detail", "generated_utc"],
    )
    write_doc(source_rows, contract, expansion, r10, r11, ppn, aeh, gates, decisions, summary, validation)

    failures = [row for row in validation if row["result"] != "pass"]
    print(f"status={STATUS}")
    print(f"doc={DOC_PATH}")
    print(f"contract_rows={len(contract)}")
    print(f"expansion_rows={len(expansion)}")
    print(f"r10_rows={len(r10)}")
    print(f"r11_rows={len(r11)}")
    print(f"validation_failures={len(failures)}")
    print(f"next_target={NEXT_TARGET}")
    if failures:
        for failure in failures:
            print(f"FAIL {failure['check_id']}: {failure['detail']}")


if __name__ == "__main__":
    main()
