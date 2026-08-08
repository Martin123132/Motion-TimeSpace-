from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from Y5_R10_alpha_product_prediction_stub_runner_and_required_inputs import (
    BOUND_REQUIRED_COLUMNS,
    PRODUCT_REQUIRED_COLUMNS,
    run_product_runner,
)


STARTED = datetime.now(timezone.utc)
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1088-Y5-R10-minimal-parent-ordinary-matter-signature-clause-or-finite-coefficient-intake.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_DIR = ROOT / "runs" / "1088-minimal-parent-ordinary-matter-signature" / "results"
PRODUCT_RUN_DIR = RUN_DIR / "product_runner"
PREDICTION_TEMPLATE = OUT / "P8_Y5_R10_1088_WEP_PRODUCT_CANDIDATE_NONCLAIM.csv"
BOUND_IMPORT = OUT / "P8_Y5_R10_1088_WEP_BOUND_IMPORT.csv"
ETA_BOUND = 2.8e-15


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def source_path(path_text: str) -> Path:
    path = Path(path_text)
    if path.is_absolute():
        return path
    return ROOT / path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def parse_float(value: object) -> float | None:
    try:
        return float(str(value).strip())
    except ValueError:
        return None


def md_cell(value: object) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def md_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    return "\n".join(
        [
            "| " + " | ".join(columns) + " |",
            "| " + " | ".join("---" for _ in columns) + " |",
            *["| " + " | ".join(md_cell(row.get(column, "")) for column in columns) + " |" for row in rows],
        ]
    ) + "\n"


def count_formalization_modified_since_start() -> int:
    if not FORMALIZATION.exists():
        return 0
    return sum(
        1
        for path in FORMALIZATION.rglob("*")
        if path.is_file() and datetime.fromtimestamp(path.stat().st_mtime, timezone.utc) >= STARTED
    )


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def source_register_rows() -> list[dict[str, str]]:
    specs = [
        ("SRC1088_0_1087_next", "source-intake/mts_residuals/P8_Y5_R10_1087_NEXT_TARGET.csv", "NEXT1087_0_1088", "1087 handoff."),
        ("SRC1088_1_1087_descent", "source-intake/mts_residuals/P8_Y5_R10_1087_PARENT_MATTER_DESCENT_ATTEMPT.csv", "PMD1087_6_verdict", "parent matter descent verdict."),
        ("SRC1088_2_1087_contract", "source-intake/mts_residuals/P8_Y5_R10_1087_ZERO_CURRENT_CLAUSE_CONTRACT.csv", "ZCC1087_0_object_language", "zero-current parent clause contract."),
        ("SRC1088_3_1087_pack", "source-intake/mts_residuals/P8_Y5_R10_1087_DD_COEFFICIENT_SOURCE_PACK.csv", "DDSP1087_0_c_alpha", "DD coefficient source-pack."),
        ("SRC1088_4_1078_object", "source-intake/mts_residuals/P8_Y5_R10_1078_OBJECT_LANGUAGE_PROOF_ATTEMPT.csv", "OL1078_4_verdict", "object-language gate."),
        ("SRC1088_5_1078_measure", "source-intake/mts_residuals/P8_Y5_R10_1078_ACTION_MEASURE_PROOF_ATTEMPT.csv", "AM1078_4_verdict", "action-measure gate."),
        ("SRC1088_6_1078_current", "source-intake/mts_residuals/P8_Y5_R10_1078_CURRENT_OWNER_PROOF_ATTEMPT.csv", "CO1078_4_verdict", "current-owner gate."),
        ("SRC1088_7_1045_functor", "source-intake/mts_residuals/P8_Y5_R10_1045_PARENT_MATTER_FUNCTOR_SIGNATURE_AUDIT.csv", "MFS1045_6_verdict", "parent matter functor audit."),
        ("SRC1088_8_1045_lift", "source-intake/mts_residuals/P8_Y5_R10_1045_VERTICAL_LIFT_DESCENT_GATE.csv", "VLG1045_4_verdict", "vertical lift descent gate."),
        ("SRC1088_9_1079_premise", "source-intake/mts_residuals/P8_Y5_R10_1079_CURRENT_OWNER_PREMISE_LEDGER.csv", "PR1079_4_no_pre_action_species_weight", "species/pre-action weight premise."),
        ("SRC1088_10_1082_units", "source-intake/mts_residuals/P8_Y5_R10_1082_COEFFICIENT_UNITS_CONTRACT.csv", "CUC1082_3_C_parent", "parent coefficient units contract."),
        ("SRC1088_11_1086_pressure", "source-intake/mts_residuals/P8_Y5_R10_1086_NONCLAIM_COEFFICIENT_PRESSURE_ROWS.csv", "CPR1086_2_equal_two_component_bulk_Earth", "coefficient pressure rows."),
        ("SRC1088_12_1084_kernel", "source-intake/mts_residuals/P8_Y5_R10_1084_SOURCE_PROFILE_KERNEL_DERIVATION_LEDGER.csv", "K1084_0_angular_integral", "finite-range source-profile kernel."),
        ("SRC1088_13_local_bounds", "source-intake/local_bounds/local_bound_claims.csv", "R1_WEP_source_charge", "MICROSCOPE WEP bound row."),
    ]
    rows: list[dict[str, str]] = []
    for source_id, relative_path, needle, note in specs:
        path = source_path(relative_path)
        exists = path.exists()
        text = read_text(path) if exists else ""
        needle_found = exists and needle.lower() in text.lower()
        rows.append(
            {
                "source_id": source_id,
                "relative_path": relative_path,
                "absolute_path": str(path),
                "exists": str(exists).lower(),
                "needle": needle,
                "needle_found": str(needle_found).lower(),
                "note": note,
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def minimal_signature_clause_rows() -> list[dict[str, str]]:
    return [
        {
            "clause_id": "MOMS1088_0_action_form",
            "minimal_signature_clause": "S_parent = S_geom[Phi] + sum_A S_A[Psi_A; E(q(Phi)), Omega(E(q(Phi))), A_obs(q(Phi)), theta_A]",
            "what_it_signs": "ordinary matter sees only observed quotient geometry, observed gauge data, and representation/superselection constants",
            "current_status": "CONDITIONAL_CLAUSE_WRITTEN_NOT_PARENT_DERIVED",
            "missing_for_adoption": "one corpus parent action that explicitly owns q, E, Omega, A_obs, Psi_A, theta_A, and the sum over species",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "clause_id": "MOMS1088_1_quotient_observables",
            "minimal_signature_clause": "q: Phi_parent -> Q_obs with v_X in ker(Dq), e_obs=E(q(Phi)), g_obs=e_obs^T eta e_obs",
            "what_it_signs": "Lie_vX e_obs = Lie_vX g_obs = 0 by chain rule",
            "current_status": "CONDITIONAL_GEOMETRY_SUBLEMMA",
            "missing_for_adoption": "parent-derived observed quotient/coframe functor and independent connection silence",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "clause_id": "MOMS1088_2_matter_bundle",
            "minimal_signature_clause": "Psi_A is a section of E_A[e_obs,A_obs] and vertical lifts on Psi_A are fixed, gauge, local-Lorentz, diffeomorphism, or boundary only",
            "what_it_signs": "no physical ordinary-matter lift along a quotient-vertical field",
            "current_status": "MISSING_PARENT_MATTER_BUNDLE_FUNCTOR",
            "missing_for_adoption": "species-complete parent matter bundle functor and boundary class",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "clause_id": "MOMS1088_3_constant_superselection",
            "minimal_signature_clause": "Lie_vX theta_A = 0 for ordinary masses, charges, clock standards, representation labels, and hbar/c normalization",
            "what_it_signs": "no hidden composition current through material constants",
            "current_status": "CONSTANT_SUPERSELECTION_UNSIGNED",
            "missing_for_adoption": "parent theorem that constants are fixed representation data, or explicit retained residual fields",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "clause_id": "MOMS1088_4_no_species_weights",
            "minimal_signature_clause": "the parent matter sum has no independent w_A(X) S_A or material-only source multiplier before variation",
            "what_it_signs": "kills pre-action species/source weights that mimic WEP violation while keeping the visible metric fixed",
            "current_status": "PRE_ACTION_WEIGHT_EXCLUSION_UNSIGNED",
            "missing_for_adoption": "object-language plus action-measure clause forbidding source-only inert weights",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "clause_id": "MOMS1088_5_variation_order",
            "minimal_signature_clause": "Hilbert/current extraction is performed on S_parent before material/readout projection or empirical fitting",
            "what_it_signs": "prevents post-variation source selectors from manufacturing a residual current",
            "current_status": "CONDITIONAL_SUBTHEOREM_ONLY",
            "missing_for_adoption": "parent-side variation-before-readout rule tied to the same action",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "clause_id": "MOMS1088_6_no_shadow_domain",
            "minimal_signature_clause": "no shadow matter frame A_A(X)^2 g_obs, disformal B_A(X), support/domain marker, boundary charge, or source-only metric is present",
            "what_it_signs": "closes hidden frame/domain leakage",
            "current_status": "NO_SHADOW_DOMAIN_UNSIGNED",
            "missing_for_adoption": "single parent exclusion of shadow frames and boundary/domain charges",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "clause_id": "MOMS1088_7_verdict",
            "minimal_signature_clause": "MOMS1088_0 through MOMS1088_6 are all parent-derived in one ordinary-matter action signature",
            "what_it_signs": "qbar_XT=0 and the local WEP source-current branch is theorem-zero",
            "current_status": "MINIMAL_PARENT_ORDINARY_MATTER_SIGNATURE_NOT_DERIVED",
            "missing_for_adoption": "the clause is now exact, but current files provide it only as a future contract, not as a derived parent action",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def conditional_zero_theorem_rows() -> list[dict[str, str]]:
    return [
        {
            "theorem_id": "THM1088_0_assumptions",
            "step": "assume the full MOMS1088 parent ordinary-matter signature",
            "derivation": "all ordinary matter terms depend on v_X only through q(Phi), quotient-owned observed geometry/gauge data, gauge/boundary lifts, and X-trivial constants",
            "result": "ASSUMPTION_SET_EXACT",
            "claim_status": "conditional_only",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "theorem_id": "THM1088_1_visible_fields",
            "step": "differentiate observed fields along v_X",
            "derivation": "Dq[v_X]=0 gives Lie_vX e_obs = D E[Dq(v_X)] = 0, and similarly for g_obs, Omega[e_obs], and A_obs(q(Phi))",
            "result": "VISIBLE_FIELD_VARIATION_ZERO_IF_SIGNATURE_SIGNED",
            "claim_status": "conditional_only",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "theorem_id": "THM1088_2_matter_lift",
            "step": "differentiate matter fields along the owned vertical lift",
            "derivation": "delta_v Psi_A is zero, gauge, local-Lorentz, diffeomorphism, or boundary-only, so its contribution to the bulk Euler/Hilbert source current vanishes",
            "result": "BULK_MATTER_LIFT_VARIATION_ZERO_IF_SIGNATURE_SIGNED",
            "claim_status": "conditional_only",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "theorem_id": "THM1088_3_constants",
            "step": "differentiate representation constants",
            "derivation": "Lie_vX theta_A=0 removes alpha_EM, mass-ratio, clock, and material-constant source-current channels unless they are explicitly retained as finite residual fields",
            "result": "CONSTANT_CHANNEL_ZERO_IF_SIGNATURE_SIGNED",
            "claim_status": "conditional_only",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "theorem_id": "THM1088_4_no_weight_leak",
            "step": "exclude pre-action weights and shadow/domain terms",
            "derivation": "without w_A(X), shadow frames, or domain markers, no source-only material label remains for delta_v S_matter to hit",
            "result": "NO_HIDDEN_RESIDUAL_SLOT_IF_SIGNATURE_SIGNED",
            "claim_status": "conditional_only",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "theorem_id": "THM1088_5_conclusion",
            "step": "take the vertical variation of ordinary matter",
            "derivation": "delta_v S_matter = 0 up to gauge/boundary terms, hence J_X^matter=0 and qbar_XT=0 for local WEP/DD composition response",
            "result": "ZERO_THEOREM_PROVED_UNDER_MOMS1088_SIGNATURE",
            "claim_status": "conditional_only",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "theorem_id": "THM1088_6_current_corpus_verdict",
            "step": "compare theorem assumptions with current source files",
            "derivation": "1087/1078/1045 show the required clauses are known, but not parent-derived in one action",
            "result": "CONDITIONAL_ZERO_THEOREM_NOT_PROMOTED",
            "claim_status": "blocked_by_unsigned_signature",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def countermodel_rows() -> list[dict[str, str]]:
    return [
        {
            "countermodel_id": "CM1088_0_species_weight",
            "legal_without_signature": "S_matter -> sum_A w_A(X) S_A with species/material-dependent w_A",
            "damage": "visible metric can remain quotient-owned while WEP source current is nonzero",
            "killed_by": "MOMS1088_4_no_species_weights",
            "current_status": "NOT_KILLED_BY_CURRENT_CORPUS",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "countermodel_id": "CM1088_1_variable_constants",
            "legal_without_signature": "theta_A(X) includes alpha_EM, nuclear binding, mass-ratio, or clock sensitivities",
            "damage": "composition-dependent DD charges survive even if geometry descends",
            "killed_by": "MOMS1088_3_constant_superselection",
            "current_status": "NOT_KILLED_BY_CURRENT_CORPUS",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "countermodel_id": "CM1088_2_shadow_frame",
            "legal_without_signature": "ordinary matter uses A_A(X)^2 g_obs or disformal/source-only metric data",
            "damage": "local fifth-force or WEP residual hides outside the observed coframe chain rule",
            "killed_by": "MOMS1088_6_no_shadow_domain",
            "current_status": "NOT_KILLED_BY_CURRENT_CORPUS",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "countermodel_id": "CM1088_3_post_variation_selector",
            "legal_without_signature": "material/readout projection is applied after variation and changes source normalization",
            "damage": "a residual source current appears as a readout artifact rather than a parent current",
            "killed_by": "MOMS1088_5_variation_order",
            "current_status": "NOT_KILLED_BY_CURRENT_CORPUS",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "countermodel_id": "CM1088_4_boundary_domain_marker",
            "legal_without_signature": "source support, boundary charge, or domain marker shifts under v_X",
            "damage": "bulk descent can hold while finite-boundary/source-profile WEP residual remains",
            "killed_by": "MOMS1088_6_no_shadow_domain",
            "current_status": "NOT_KILLED_BY_CURRENT_CORPUS",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def finite_product_formula_rows() -> list[dict[str, str]]:
    return [
        {
            "formula_id": "FPF1088_0_eta_formula",
            "formula": "eta_AB(lambda) = K_MICROSCOPE(lambda) * [c_alpha Qeff_E_alpha(lambda) DeltaQ_AB_alpha + c_surface Qeff_E_surface(lambda) DeltaQ_AB_surface + q_tail_AB(lambda)]",
            "meaning": "fallback finite branch if MOMS1088 zero theorem remains unsigned",
            "required_inputs": "same-branch lambda, K, Qeff source profile, test-material DD deltas, c_alpha, c_surface, tail envelope",
            "status": "FORMULA_READY_NONCLAIM",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "formula_id": "FPF1088_1_zero_limit",
            "formula": "if MOMS1088 signs, c_alpha=c_surface=q_tail=0 before readout and eta_AB=0",
            "meaning": "theorem route beats finite fitting by deleting the coefficient vector",
            "required_inputs": "parent-derived MOMS1088 signature",
            "status": "CONDITIONAL_ZERO_LIMIT",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "formula_id": "FPF1088_2_same_branch_lock",
            "formula": "lambda_X, K_MICROSCOPE, Qeff_E, c_I, and DeltaQ_I must be owned by the same branch and normalization",
            "meaning": "prevents range/amplitude/readout mix-and-match tuning",
            "required_inputs": "branch_id and source paths for every factor",
            "status": "CLAIM_POLICY_LOCK",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def finite_intake_schema_rows() -> list[dict[str, str]]:
    return [
        {
            "field_id": "FIS1088_0_branch_id",
            "field_name": "branch_id",
            "units": "label",
            "required_source": "one MTS branch supplying range, amplitude, coefficients, and readout",
            "validity_rule": "must be same branch for every row",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "field_id": "FIS1088_1_lambda",
            "field_name": "lambda_X_m",
            "units": "m",
            "required_source": "parent Z_X/M_X^2 or source-backed finite-range branch",
            "validity_rule": "positive numeric with source path; no fitted convenience range",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "field_id": "FIS1088_2_readout",
            "field_name": "K_MICROSCOPE_lambda",
            "units": "dimensionless readout factor",
            "required_source": "official or derived MICROSCOPE readout/projection model",
            "validity_rule": "not a unit proxy unless explicitly labelled nonclaim",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "field_id": "FIS1088_3_source_profile",
            "field_name": "Qeff_E_alpha;Qeff_E_surface",
            "units": "DD charge convention",
            "required_source": "bulk long-range theorem or finite profile integration with sourced Earth profile",
            "validity_rule": "must match lambda_X and composition profile",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "field_id": "FIS1088_4_coefficients",
            "field_name": "c_alpha;c_surface;q_tail",
            "units": "dimensionless after parent normalization",
            "required_source": "parent action derivative or labelled phenomenological source with provenance",
            "validity_rule": "no pair cancellation, no posthoc sign choice, no measured-G absorption",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "field_id": "FIS1088_5_prediction",
            "field_name": "eta_pred",
            "units": "dimensionless",
            "required_source": "computed from all source-backed factors using FPF1088_0",
            "validity_rule": "claim allowed only if abs(eta_pred) <= 2.8e-15 and all gates are source-backed",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def finite_intake_template_rows() -> list[dict[str, str]]:
    return [
        {
            "template_id": "FIT1088_0_c_alpha",
            "branch_id": "MTS_WEP_finite_branch",
            "quantity": "c_alpha",
            "value": "MISSING_PARENT_EM_DERIVATIVE_OR_PROVENANCE_VALUE",
            "units": "dimensionless_after_parent_normalization",
            "source_path": "MISSING_PARENT_OR_EXPLICIT_PHENOMENOLOGICAL_SOURCE",
            "source_row": "MISSING",
            "derivation_status": "missing",
            "valid_for_claim": "false",
            "notes": "do not fill from smoke-fit, cancellation line, or desired WEP bound",
        },
        {
            "template_id": "FIT1088_1_c_surface",
            "branch_id": "MTS_WEP_finite_branch",
            "quantity": "c_surface",
            "value": "MISSING_PARENT_BINDING_DERIVATIVE_OR_PROVENANCE_VALUE",
            "units": "dimensionless_after_parent_normalization",
            "source_path": "MISSING_PARENT_OR_EXPLICIT_PHENOMENOLOGICAL_SOURCE",
            "source_row": "MISSING",
            "derivation_status": "missing",
            "valid_for_claim": "false",
            "notes": "must be all-material, not tuned to TA6V/PtRh10",
        },
        {
            "template_id": "FIT1088_2_q_tail",
            "branch_id": "MTS_WEP_finite_branch",
            "quantity": "q_tail_AB_lambda",
            "value": "MISSING_TAIL_ENVELOPE",
            "units": "dimensionless_eta_contribution_or_charge_envelope",
            "source_path": "MISSING_PARENT_OR_EMPIRICAL_ENVELOPE_SOURCE",
            "source_row": "MISSING",
            "derivation_status": "missing",
            "valid_for_claim": "false",
            "notes": "needed because alpha/surface DD rows are not a complete material basis",
        },
        {
            "template_id": "FIT1088_3_lambda_K_profile",
            "branch_id": "MTS_WEP_finite_branch",
            "quantity": "lambda_X_m;K_MICROSCOPE;Qeff_E",
            "value": "MISSING_SAME_BRANCH_RANGE_READOUT_PROFILE",
            "units": "m;dimensionless;DD_charge",
            "source_path": "MISSING_RANGE_READOUT_PROFILE_SOURCE",
            "source_row": "MISSING",
            "derivation_status": "missing",
            "valid_for_claim": "false",
            "notes": "must share one branch normalization with c_alpha/c_surface",
        },
    ]


def prediction_rows() -> list[dict[str, str]]:
    return [
        {
            "prediction_id": "PRED1088_0_signature_or_finite_intake_missing",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "P_WEP_relative_source_weight",
            "product_value": "MISSING_PARENT_SIGNATURE_OR_FILLED_FINITE_DD_INTAKE",
            "product_units": "dimensionless",
            "product_source": "source-intake/mts_residuals/P8_Y5_R10_1088_MINIMAL_SIGNATURE_CLAUSE.csv",
            "inputs_present": "conditional signature theorem; finite intake schema; MICROSCOPE bound",
            "required_inputs": "parent-signed MOMS1088 signature OR filled same-branch finite intake with c_alpha/c_surface/q_tail/lambda/K/profile",
            "derivation_status": "SIGNATURE_NOT_DERIVED_FINITE_INTAKE_EMPTY",
            "valid_for_claim": "false",
            "notes": "generic product runner must refuse; 1088 proves only the conditional zero theorem and opens the finite intake schema",
        }
    ]


def bound_import_rows() -> list[dict[str, str]]:
    return [
        {
            "bound_id": "BOUND1088_0_MICROSCOPE_WEP",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "P_WEP_relative_source_weight",
            "bound_value": f"{ETA_BOUND:.16e}",
            "bound_units": "dimensionless",
            "bound_source": "source-intake/local_bounds/local_bound_claims.csv",
            "source_row": "R1_WEP_source_charge",
            "bound_type": "absolute_eta_upper_bound",
            "valid_for_claim": "true",
            "notes": "source-backed comparator bound; MTS prediction row remains invalid",
        }
    ]


def product_status_rows(product_status: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "runner_id": "APR1088_0_signature_or_finite_intake_stub",
            "prediction_rows": str(product_status.get("prediction_rows", "")),
            "bound_rows": str(product_status.get("bound_rows", "")),
            "valid_prediction_rows": str(product_status.get("valid_prediction_rows", "")),
            "valid_bound_rows": str(product_status.get("valid_bound_rows", "")),
            "comparison_rows": str(product_status.get("comparison_rows", "")),
            "claim_allowed": str(product_status.get("claim_allowed", "")).lower(),
            "expected_result": "reject missing parent signature and empty finite DD intake",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def claim_gate_rows(product_status: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "gate_id": "CG1088_0_parent_signature",
            "claim_component": "minimal parent ordinary-matter signature",
            "gate_pass": "false",
            "claim_allowed": "false",
            "reason": "MOMS1088_7_verdict=MINIMAL_PARENT_ORDINARY_MATTER_SIGNATURE_NOT_DERIVED",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1088_1_conditional_zero_theorem",
            "claim_component": "qbar_XT=0 theorem",
            "gate_pass": "true",
            "claim_allowed": "false",
            "reason": "proved only under unsigned MOMS1088 assumptions",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1088_2_finite_intake",
            "claim_component": "finite DD coefficient intake",
            "gate_pass": "false",
            "claim_allowed": "false",
            "reason": "all finite coefficient/range/readout/profile rows contain missing placeholders",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1088_3_product_runner",
            "claim_component": "WEP product runner",
            "gate_pass": str(product_status.get("valid_prediction_rows") == 0).lower(),
            "claim_allowed": "false",
            "reason": f"valid_prediction_rows={product_status.get('valid_prediction_rows')}",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC1088_0_theorem_status",
            "decision": "conditional zero theorem is now explicit",
            "because": "if the minimal ordinary-matter parent signature is true, the vertical source current vanishes by chain rule plus gauge/boundary matter lift plus constant superselection",
            "next_action": "hunt the corpus for a parent source that actually signs MOMS1088, rather than adopting it as an axiom",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1088_1_derivation_status",
            "decision": "do not promote the local branch",
            "because": "species weights, variable constants, shadow frames, post-variation selectors, and boundary/domain markers remain legal countermodels without MOMS1088",
            "next_action": "either derive the signature from the parent action or keep finite coefficients explicit",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1088_2_finite_route",
            "decision": "finite DD intake route is opened as phenomenological scaffolding only",
            "because": "the exact eta formula and same-branch locks are written, but no coefficient values are sourced",
            "next_action": "only review filled rows if they include value, units, source path, source row, derivation status, and bound link",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_id": "NEXT1088_0_1089",
            "next_target": "1089-Y5-R10-parent-ordinary-matter-signature-source-hunt-or-DD-intake-review.md",
            "objective": "search the corpus for a real parent-action source that signs the MOMS1088 ordinary-matter signature; if none exists, keep the finite DD intake route as explicit nonclaim scaffolding and review only fully sourced rows",
            "include": "parent action source hunt; ordinary matter object-language; no species weights; constant superselection; variation-before-readout; no-shadow frame; finite intake review rules",
            "exclude": "adopting MOMS1088 as axiom; invented coefficients; pair cancellation; measured-G absorption; WEP/local-GR claim; GitHub; formalization edits",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def csv_outputs_parse(paths: list[Path]) -> bool:
    try:
        for path in paths:
            with path.open(newline="", encoding="utf-8") as handle:
                list(csv.DictReader(handle))
        return True
    except csv.Error:
        return False


def validate_outputs(
    outputs: dict[str, Path],
    source_rows: list[dict[str, str]],
    signature_rows: list[dict[str, str]],
    theorem_rows: list[dict[str, str]],
    countermodel_rows_: list[dict[str, str]],
    formula_rows: list[dict[str, str]],
    schema_rows: list[dict[str, str]],
    template_rows: list[dict[str, str]],
    prediction_rows_: list[dict[str, str]],
    bound_rows_: list[dict[str, str]],
    product_status: dict[str, Any],
    claim_rows: list[dict[str, str]],
    next_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    checks: list[tuple[str, bool, str]] = []
    checks.append(("V1088_0_local_sources_exist", all(row["exists"] == "true" and row["needle_found"] == "true" for row in source_rows), "all cited local source paths and needles are present"))
    checks.append(("V1088_1_signature_contract_written", any(row["clause_id"] == "MOMS1088_7_verdict" and row["current_status"] == "MINIMAL_PARENT_ORDINARY_MATTER_SIGNATURE_NOT_DERIVED" for row in signature_rows), "minimal ordinary-matter signature contract ends in explicit unsigned verdict"))
    checks.append(("V1088_2_conditional_theorem_only", any(row["theorem_id"] == "THM1088_5_conclusion" and row["result"] == "ZERO_THEOREM_PROVED_UNDER_MOMS1088_SIGNATURE" for row in theorem_rows) and any(row["theorem_id"] == "THM1088_6_current_corpus_verdict" and row["result"] == "CONDITIONAL_ZERO_THEOREM_NOT_PROMOTED" for row in theorem_rows), "conditional qbar_XT zero theorem is written and not promoted"))
    checks.append(("V1088_3_countermodels_retained", len(countermodel_rows_) == 5 and all(row["current_status"] == "NOT_KILLED_BY_CURRENT_CORPUS" for row in countermodel_rows_), "all known countermodels remain retained until parent signature is signed"))
    checks.append(("V1088_4_finite_formula_ready_nonclaim", any(row["formula_id"] == "FPF1088_0_eta_formula" for row in formula_rows) and all(row["valid_for_claim"] == "false" for row in formula_rows), "finite eta formula and same-branch locks are written as nonclaim"))
    checks.append(("V1088_5_intake_template_empty", len(template_rows) == 4 and all("MISSING" in row["value"] and row["valid_for_claim"] == "false" for row in template_rows), "finite DD intake template remains empty and nonclaim"))
    checks.append(("V1088_6_schema_complete", len(schema_rows) == 6 and all(row["valid_for_claim"] == "false" for row in schema_rows), "finite intake schema has the required gates"))
    checks.append(("V1088_7_prediction_missing_nonclaim", any("MISSING_PARENT_SIGNATURE" in row["product_value"] and row["valid_for_claim"] == "false" for row in prediction_rows_), "prediction row remains missing signature or finite intake"))
    checks.append(("V1088_8_bound_numeric", bool(bound_rows_) and parse_float(bound_rows_[0]["bound_value"]) is not None and float(bound_rows_[0]["bound_value"]) > 0 and bound_rows_[0]["valid_for_claim"] == "true", "MICROSCOPE bound import is positive numeric"))
    checks.append(("V1088_9_product_runner_refuses", product_status.get("valid_prediction_rows") == 0 and product_status.get("claim_allowed") is False, "generic product runner reports no valid prediction rows and claim false"))
    checks.append(("V1088_10_claim_gates_safe", claim_rows and all(row["claim_allowed"] == "false" for row in claim_rows), "all claim gates deny WEP/local-GR claim"))
    checks.append(("V1088_11_next_target", any(row["next_target"].startswith("1089-Y5-R10-parent-ordinary-matter") for row in next_rows), "1089 handoff written"))
    generated_paths = list(outputs.values()) + [DOC]
    checks.append(("V1088_12_generated_under_post_checkpoint", all(str(path.resolve()).startswith(str(ROOT.resolve())) for path in generated_paths), "all generated outputs are under post-checkpoint-work"))
    checks.append(("V1088_13_csv_parse", csv_outputs_parse([path for key, path in outputs.items() if key != "validation"]), "all 1088 CSV outputs parse cleanly"))
    checks.append(("V1088_14_formalization_untouched", count_formalization_modified_since_start() == 0, "formalization-workbench modified-file count remains zero"))
    checks.append(("V1088_SUMMARY", True, "conditional local WEP zero theorem proved under a minimal parent ordinary-matter signature, but signature is not derived; finite DD intake remains empty and nonclaim"))
    return [
        {
            "check_id": check_id,
            "result": "pass" if passed else "fail",
            "detail": detail,
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for check_id, passed, detail in checks
    ]


def write_doc(
    source_rows: list[dict[str, str]],
    signature_rows: list[dict[str, str]],
    theorem_rows: list[dict[str, str]],
    countermodel_rows_: list[dict[str, str]],
    formula_rows: list[dict[str, str]],
    schema_rows: list[dict[str, str]],
    template_rows: list[dict[str, str]],
    product_status_rows_: list[dict[str, str]],
    product_comparisons: list[dict[str, Any]],
    claim_rows: list[dict[str, str]],
    decisions: list[dict[str, str]],
    validation_rows: list[dict[str, str]],
    next_rows: list[dict[str, str]],
) -> None:
    text = "\n".join(
        [
            "# 1088-Y5-R10 minimal parent ordinary-matter signature clause or finite coefficient intake",
            "",
            "## Current verdict",
            "1088 gets a clean mathematical win, but only conditionally. If ordinary matter is forced to live on the observed quotient bundle with X-trivial representation constants, no species weights, no shadow frame/domain terms, and variation before readout, then the vertical source current vanishes and qbar_XT=0. The corpus does not yet derive that full signature from one parent action, so this is not a local-GR/WEP claim. The fallback finite DD intake route is opened, but it is deliberately empty and nonclaim.",
            "",
            "## Local source register",
            md_table(source_rows, ["source_id", "relative_path", "exists", "needle_found", "note"]),
            "## Minimal parent ordinary-matter signature",
            md_table(signature_rows, ["clause_id", "minimal_signature_clause", "what_it_signs", "current_status", "missing_for_adoption"]),
            "## Conditional zero theorem",
            md_table(theorem_rows, ["theorem_id", "step", "derivation", "result", "claim_status"]),
            "## Countermodels still legal without the signature",
            md_table(countermodel_rows_, ["countermodel_id", "legal_without_signature", "damage", "killed_by", "current_status"]),
            "## Finite product formula",
            md_table(formula_rows, ["formula_id", "formula", "meaning", "required_inputs", "status"]),
            "## Finite DD intake schema",
            md_table(schema_rows, ["field_id", "field_name", "units", "required_source", "validity_rule"]),
            "## Finite DD intake template",
            md_table(template_rows, ["template_id", "quantity", "value", "units", "source_path", "source_row", "derivation_status", "notes"]),
            "## Product runner status",
            md_table(product_status_rows_, ["runner_id", "valid_prediction_rows", "valid_bound_rows", "comparison_rows", "claim_allowed", "expected_result"]),
            "## Product comparison rows",
            md_table(product_comparisons, ["comparison_id", "arena", "product_symbol", "product_value", "bound_value", "comparison_status", "pass_for_claim", "issues"]),
            "## Claim gates",
            md_table(claim_rows, ["gate_id", "claim_component", "gate_pass", "claim_allowed", "reason"]),
            "## Decision ledger",
            md_table(decisions, ["decision_id", "decision", "because", "next_action"]),
            "## Validation",
            md_table(validation_rows, ["check_id", "result", "detail"]),
            "## Next target",
            md_table(next_rows, ["next_id", "next_target", "objective", "include", "exclude"]),
            "",
        ]
    )
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    source_rows = source_register_rows()
    signature_rows = minimal_signature_clause_rows()
    theorem_rows = conditional_zero_theorem_rows()
    countermodel_rows_ = countermodel_rows()
    formula_rows = finite_product_formula_rows()
    schema_rows = finite_intake_schema_rows()
    template_rows = finite_intake_template_rows()
    prediction_rows_ = prediction_rows()
    bound_rows_ = bound_import_rows()
    next_rows = next_target_rows()

    outputs = {
        "source_register": OUT / "P8_Y5_R10_1088_SOURCE_REGISTER.csv",
        "signature_clause": OUT / "P8_Y5_R10_1088_MINIMAL_SIGNATURE_CLAUSE.csv",
        "conditional_theorem": OUT / "P8_Y5_R10_1088_CONDITIONAL_ZERO_THEOREM.csv",
        "countermodels": OUT / "P8_Y5_R10_1088_COUNTERMODEL_RETENTION.csv",
        "finite_formula": OUT / "P8_Y5_R10_1088_FINITE_PRODUCT_FORMULA.csv",
        "finite_schema": OUT / "P8_Y5_R10_1088_FINITE_DD_INTAKE_SCHEMA.csv",
        "finite_template": OUT / "P8_Y5_R10_1088_FINITE_DD_INTAKE_TEMPLATE_NONCLAIM.csv",
        "prediction": PREDICTION_TEMPLATE,
        "bound": BOUND_IMPORT,
        "product_status": OUT / "P8_Y5_R10_1088_PRODUCT_RUNNER_STATUS.csv",
        "product_comparison": OUT / "P8_Y5_R10_1088_PRODUCT_COMPARISON_ROWS.csv",
        "claim_gates": OUT / "P8_Y5_R10_1088_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_R10_1088_DECISION_LEDGER.csv",
        "next_target": OUT / "P8_Y5_R10_1088_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_1088_VALIDATION.csv",
    }

    write_csv(outputs["source_register"], source_rows)
    write_csv(outputs["signature_clause"], signature_rows)
    write_csv(outputs["conditional_theorem"], theorem_rows)
    write_csv(outputs["countermodels"], countermodel_rows_)
    write_csv(outputs["finite_formula"], formula_rows)
    write_csv(outputs["finite_schema"], schema_rows)
    write_csv(outputs["finite_template"], template_rows)
    write_csv(outputs["prediction"], prediction_rows_, PRODUCT_REQUIRED_COLUMNS)
    write_csv(outputs["bound"], bound_rows_, BOUND_REQUIRED_COLUMNS)

    product_result = run_product_runner(PREDICTION_TEMPLATE, BOUND_IMPORT, PRODUCT_RUN_DIR)
    product_status = product_result["status"]
    product_status_rows_ = product_status_rows(product_status)
    product_comparisons = product_result["comparisons"]
    claim_rows = claim_gate_rows(product_status)
    decisions = decision_rows()

    write_csv(outputs["product_status"], product_status_rows_)
    write_csv(outputs["product_comparison"], product_comparisons)
    write_csv(outputs["claim_gates"], claim_rows)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["next_target"], next_rows)

    validation_rows = validate_outputs(
        outputs,
        source_rows,
        signature_rows,
        theorem_rows,
        countermodel_rows_,
        formula_rows,
        schema_rows,
        template_rows,
        prediction_rows_,
        bound_rows_,
        product_status,
        claim_rows,
        next_rows,
    )
    write_csv(outputs["validation"], validation_rows)
    write_doc(
        source_rows,
        signature_rows,
        theorem_rows,
        countermodel_rows_,
        formula_rows,
        schema_rows,
        template_rows,
        product_status_rows_,
        product_comparisons,
        claim_rows,
        decisions,
        validation_rows,
        next_rows,
    )
    remove_pycache()

    failed = [row for row in validation_rows if row["result"] != "pass"]
    print(f"wrote {DOC}")
    print(f"validation: {'PASS' if not failed else 'FAIL'}")
    for row in failed:
        print(f"{row['check_id']}: {row['detail']}")


if __name__ == "__main__":
    main()
