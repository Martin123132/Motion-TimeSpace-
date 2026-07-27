from __future__ import annotations

import csv
import json
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
DOC = ROOT / "1064-Y5-R10-parent-category-label-forgetting-proof-or-relative-weight-runner-fill.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_DIR = ROOT / "runs" / "1064-parent-category-label-forgetting-relative-weight-runner" / "results"
PRODUCT_RUN_DIR = RUN_DIR / "product_runner"
PREDICTION_TEMPLATE = OUT / "P8_Y5_R10_1064_RELATIVE_WEIGHT_PRODUCT_TEMPLATE_NONCLAIM.csv"
BOUND_IMPORT = OUT / "P8_Y5_R10_1064_RELATIVE_WEIGHT_BOUND_IMPORT.csv"


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


def source_register_rows() -> list[dict[str, str]]:
    specs = [
        ("SRC1064_0_1063_next", "source-intake/mts_residuals/P8_Y5_R10_1063_NEXT_TARGET.csv", "1064-Y5-R10-parent-category-label-forgetting-proof", "1063 handoff."),
        ("SRC1064_1_1063_theorem", "source-intake/mts_residuals/P8_Y5_R10_1063_SOURCE_FORGETTING_THEOREM_ATTEMPT.csv", "THM1063_5_verdict", "1063 theorem verdict."),
        ("SRC1064_2_1063_owner", "source-intake/mts_residuals/P8_Y5_R10_1063_NOETHER_SOURCE_OWNER_AUDIT.csv", "NO1063_2_Noether_current_owner", "Noether owner audit."),
        ("SRC1064_3_1063_prior", "source-intake/mts_residuals/P8_Y5_R10_1063_RELATIVE_WEIGHT_PRIOR_MATRIX.csv", "RWP1063_4_delta_w_R10", "relative-weight prior matrix."),
        ("SRC1064_4_1063_template", "source-intake/mts_residuals/P8_Y5_R10_1063_RELATIVE_WEIGHT_PRODUCT_TEMPLATE_NONCLAIM.csv", "PRED1063_0_WEP_relative_source_weight", "prior product templates."),
        ("SRC1064_5_954_label_forgetting", "source-intake/mts_residuals/P8_Y5_R10_954_PARENT_LABEL_FORGETTING_ATTEMPT.csv", "PLF954_5_verdict", "parent label-forgetting attempt."),
        ("SRC1064_6_954_parent_clause", "source-intake/mts_residuals/P8_Y5_R10_954_PARENT_ACTION_CLAUSE.csv", "PAC954_1_no_source_prefactors", "no source-prefactor clause."),
        ("SRC1064_7_954_bound_targets", "source-intake/mts_residuals/P8_Y5_R10_954_SOURCE_FUNCTOR_BOUND_TARGETS.csv", "SCB954_2_WEP_surface_beta_source", "older species-weight bound targets."),
        ("SRC1064_8_954_countermodel_map", "source-intake/mts_residuals/P8_Y5_R10_954_COUNTERMODEL_TO_BOUND_MAP.csv", "CBM954_0_labelled_weight", "countermodel-to-bound map."),
        ("SRC1064_9_955_prefactor_class", "source-intake/mts_residuals/P8_Y5_R10_955_SOURCE_PREFACTOR_CLASSIFICATION.csv", "SPC955_2_relative_species_weight", "source prefactor classes."),
        ("SRC1064_10_955_runner", "source-intake/mts_residuals/P8_Y5_R10_955_SPECIES_WEIGHT_RESIDUAL_RUNNER.csv", "SWR955_3_WEP_coulomb_beta_source", "older runner refusal rows."),
        ("SRC1064_11_956_spine", "source-intake/mts_residuals/P8_Y5_R10_956_SOURCE_SIDE_GR_NEWTON_SPINE.csv", "SSG956_3_minimal_matter_action", "source-side GR/Newton spine."),
        ("SRC1064_12_639_bounds", "source-intake/mts_residuals/P8_Y5_R10_639_LOCAL_BOUND_MATRIX.csv", "LBM639_10", "local bound matrix."),
        ("SRC1064_13_local_bounds", "source-intake/local_bounds/local_bound_claims.csv", "R9_Gdot", "local empirical bound anchors."),
        ("SRC1064_14_P8_template", "source-intake/mts_residuals/P8_SOURCE_NORMALIZATION_NUMERIC_INPUT_TEMPLATE.csv", "NI5_species", "source-normalization numeric input template."),
        ("SRC1064_15_P8_bound_runner", "source-intake/mts_residuals/P8_Y5_SOURCE_NORMALIZATION_BOUND_RUNNER_INPUT.csv", "Y5B_3_species_source_charge", "source-normalization bound runner input."),
        ("SRC1064_16_PPN_gates", "source-intake/mts_residuals/P8_Y5_PPN_SOURCE_STABILITY_GATES.csv", "PSG524_5_beta_source_zero", "PPN source stability gates."),
        ("SRC1064_17_393_doc", "393-source-normalized-Newtonian-limit-under-identity-closure.md", "Only a constant, universal, range-independent", "measured-G common-mode guard."),
    ]
    rows: list[dict[str, str]] = []
    for source_id, relative_path, needle, note in specs:
        path = source_path(relative_path)
        exists = path.exists()
        needle_found = exists and needle in read_text(path)
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


def proof_attempt_rows() -> list[dict[str, str]]:
    return [
        {
            "proof_id": "PLF1064_0_target",
            "step": "parent category label-forgetting",
            "mathematical_form": "q_src({(T_A,A)}) = T_total before coupling selection; F_src(T_total)=kappa_univ T_total",
            "proof_result": "TARGET_RESTATED",
            "support": "NSF953_2; PLF954_5; SSG956_1",
            "gap": "target is not a derivation; parent category still must forbid labelled source arguments",
            "parent_signed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "proof_id": "PLF1064_1_total_Hilbert_variation",
            "step": "variation of a single matter action forgets bookkeeping labels after summation",
            "mathematical_form": "T_total = 2/sqrt(-g) delta(sum_A S_A)/delta g = sum_A T_A",
            "proof_result": "CONDITIONAL_MATH_CLEAN",
            "support": "PLF954_1_total_variation_route; MMA955_1_same_action_principle",
            "gap": "only works if the action being varied has no source-only prefactors w_A",
            "parent_signed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "proof_id": "PLF1064_2_no_source_only_slot",
            "step": "ban source-only species prefactors",
            "mathematical_form": "Allowed[S_matter] excludes w_A S_A when w_A has no nongravitational measurement role",
            "proof_result": "EXACT_CLAUSE_NOT_DERIVED",
            "support": "PAC954_1_no_source_prefactors; MMA955_5_minimal_schema",
            "gap": "absence of a slot is a parent action schema condition unless derived from deeper quotient/operator classification",
            "parent_signed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "proof_id": "PLF1064_3_counterexample",
            "step": "relative-weight obstruction",
            "mathematical_form": "S_matter=sum_A w_A S_A gives T_source=sum_A w_A T_A while preserving covariance/additivity",
            "proof_result": "COUNTEREXAMPLE_SURVIVES",
            "support": "PLF954_2_prefactor_obstruction; MMA955_3_relative_prefactor; SPC955_2_relative_species_weight",
            "gap": "field rescalings do not generally remove w_A once interactions, charges, and quantum normalization are measured",
            "parent_signed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "proof_id": "PLF1064_4_no_hidden_spurion_return",
            "step": "prevent disguised source labels",
            "mathematical_form": "partial_m kappa = partial_D kappa = partial_boundary kappa = partial_readout kappa = 0",
            "proof_result": "PARALLEL_GATE_UNSIGNED",
            "support": "PAC954_3_no_hidden_spurion_return; SPC955_3_hidden_marker_weight",
            "gap": "no-marker/no-extension theorem remains rejected or conditional in current corpus",
            "parent_signed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "proof_id": "PLF1064_5_verdict",
            "step": "parent category label-forgetting proof",
            "mathematical_form": "single S_matter + no w_A + no hidden spurion return + total Hilbert variation => source labels forgotten",
            "proof_result": "CONDITIONAL_CONTRACT_NOT_PARENT_DERIVED",
            "support": "953/954/955/956/1063 chain",
            "gap": "no-source-only-slot theorem is not signed; relative-weight runner fill is required",
            "parent_signed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def no_source_slot_rows() -> list[dict[str, str]]:
    return [
        {
            "slot_id": "NSS1064_0_absent_slot",
            "slot": "w_A source-only prefactor",
            "allowed_status": "desired_absent_slot",
            "required_signature": "parent action grammar has no argument corresponding to source-only species weight",
            "if_present": "relative source WEP/PPN/R10 residual",
            "current_status": "not_parent_signed",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "slot_id": "NSS1064_1_common_mode",
            "slot": "w_common",
            "allowed_status": "calibration_only",
            "required_signature": "constant universal range/time/species/frame independent multiplier",
            "if_present": "absorbed into measured G only after all derivative/common-mode guards pass",
            "current_status": "guarded_not_claim",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "slot_id": "NSS1064_2_relative_weight",
            "slot": "epsilon_A with w_A=w_common(1+epsilon_A)",
            "allowed_status": "live_countermodel_if_not_forbidden",
            "required_signature": "numeric epsilon_A vector with source path or parent theorem-zero",
            "if_present": "WEP/source charge and possibly PPN/R10 residuals",
            "current_status": "retained_nonclaim",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "slot_id": "NSS1064_3_nonHilbert_weight",
            "slot": "zeta_A J_NH,A",
            "allowed_status": "parallel_open_gate",
            "required_signature": "non-Hilbert current is absent, exact/projected silent, or explicitly bounded",
            "if_present": "bypasses Hilbert-current source theorem",
            "current_status": "retained_separate_gate",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def runner_schema_rows() -> list[dict[str, str]]:
    columns = [
        ("prediction_id", "stable row id"),
        ("arena", "MICROSCOPE_WEP, PPN_Newton, Gdot_orbital, or R10_short_range"),
        ("product_symbol", "exact relative-weight product tested"),
        ("product_value", "numeric prediction only; placeholders are invalid"),
        ("product_units", "dimensionless, yr^-1, or declared alpha(lambda) convention"),
        ("product_source", "local source path proving the product"),
        ("inputs_present", "semicolon-separated real inputs"),
        ("required_inputs", "all required coefficients/maps/source files"),
        ("derivation_status", "derived_zero, sourced_numeric, or blocked status"),
        ("valid_for_claim", "true only when numeric/sourced/unit matched"),
        ("notes", "assumptions and no-cancellation caveats"),
    ]
    return [
        {
            "column": column,
            "definition": definition,
            "required": "true",
            "nonclaim_rule": "reject if missing marker, nonnumeric product, unity shortcut, source missing, or valid_for_claim=false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for column, definition in columns
    ]


def numeric_requirement_rows() -> list[dict[str, str]]:
    return [
        {
            "requirement_id": "REQ1064_0_WEP_species",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "P_WEP_relative_source_weight",
            "required_inputs": "species_pair;Delta_w_AB;tau_WEP;material/source map;eta_prediction;source_file",
            "units": "dimensionless",
            "bound_or_target": "2.8e-15",
            "source_requirement": "parent label-forgetting theorem or sourced Delta_w_AB and tau_WEP map",
            "current_status": "MISSING_DELTA_W_AB_TAU_WEP_PRODUCT",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "requirement_id": "REQ1064_1_PPN_gamma",
            "arena": "PPN_Newton",
            "product_symbol": "P_PPN_source_weight_gamma",
            "required_inputs": "C_gamma_source_weight;Delta_w_source;weak_field_response_map;source_file",
            "units": "dimensionless",
            "bound_or_target": "2.3e-05",
            "source_requirement": "weak-field PPN response from relative weights into gamma-1 or theorem-zero",
            "current_status": "MISSING_C_GAMMA_SOURCE_WEIGHT_PRODUCT",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "requirement_id": "REQ1064_2_PPN_beta",
            "arena": "PPN_Newton",
            "product_symbol": "P_PPN_source_weight_beta",
            "required_inputs": "C_beta_source_weight;Delta_w_source;second_order_response_map;source_file",
            "units": "dimensionless",
            "bound_or_target": "7.8e-05",
            "source_requirement": "second-order PPN source response or theorem-zero",
            "current_status": "MISSING_C_BETA_SOURCE_WEIGHT_PRODUCT",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "requirement_id": "REQ1064_3_Gdot",
            "arena": "Gdot_orbital",
            "product_symbol": "P_Gdot_relative_source_weight",
            "required_inputs": "dln_w_source_dt;time_map;source-frame convention;source_file",
            "units": "yr^-1",
            "bound_or_target": "9.6e-15",
            "source_requirement": "time constancy theorem or sourced drift below LLR lock",
            "current_status": "MISSING_DLN_W_SOURCE_DT",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "requirement_id": "REQ1064_4_R10",
            "arena": "R10_short_range",
            "product_symbol": "P_R10_relative_weight(lambda)",
            "required_inputs": "lambda_w;K_w(lambda);Delta_w_source;Delta_w_test;tau_R10;alpha_bound(lambda);source_file",
            "units": "dimensionless with length column",
            "bound_or_target": "promoted alpha(lambda) curve",
            "source_requirement": "finite-range product and bound curve, or no finite-range source-weight theorem",
            "current_status": "MISSING_KW_DELTAW_SOURCE_DELTAW_TEST_TAU_R10_PRODUCT",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def common_mode_guard_rows() -> list[dict[str, str]]:
    return [
        {
            "guard_id": "CMG1064_0_common_absorption",
            "candidate_absorption": "w_common into measured G",
            "required_zero_derivatives": "D_A=0;D_t=0;D_r=0;D_lambda=0;Delta_frame=0",
            "must_be": "constant;universal;range_independent;time_independent;species_blind;same_frame",
            "current_status": "not_proved",
            "if_failed": "relative/source-normalization residual remains physical",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "guard_id": "CMG1064_1_relative_not_absorbable",
            "candidate_absorption": "epsilon_A relative source weights into G",
            "required_zero_derivatives": "Delta_AB epsilon=0 for every source/test material pair",
            "must_be": "species_blind before calibration",
            "current_status": "not_proved",
            "if_failed": "WEP/source charge residual cannot be hidden in G",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "guard_id": "CMG1064_2_range_not_absorbable",
            "candidate_absorption": "finite-range source weight into local calibration",
            "required_zero_derivatives": "D_lambda=0 and D_r=0 across tested range",
            "must_be": "range_independent before R10/orbital comparison",
            "current_status": "not_proved",
            "if_failed": "R10/orbital/fifth-force row must be filled",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def prediction_rows() -> list[dict[str, str]]:
    return [
        {
            "prediction_id": "PRED1064_0_WEP_relative_source_weight",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "P_WEP_relative_source_weight",
            "product_value": "MISSING_DELTA_W_AB_TAU_WEP_PRODUCT",
            "product_units": "dimensionless",
            "product_source": "source-intake/mts_residuals/P8_Y5_R10_1064_NUMERIC_SOURCE_REQUIREMENTS.csv",
            "inputs_present": "none",
            "required_inputs": "species_pair;Delta_w_AB;tau_WEP;material/source map;eta_prediction;source_file",
            "derivation_status": "MISSING_NUMERIC_OR_THEOREM_ZERO_RELATIVE_WEIGHT",
            "valid_for_claim": "false",
            "notes": "WEP source-charge prediction missing.",
        },
        {
            "prediction_id": "PRED1064_1_PPN_gamma_source_weight",
            "arena": "PPN_Newton",
            "product_symbol": "P_PPN_source_weight_gamma",
            "product_value": "MISSING_C_GAMMA_SOURCE_WEIGHT_PRODUCT",
            "product_units": "dimensionless",
            "product_source": "source-intake/mts_residuals/P8_Y5_R10_1064_NUMERIC_SOURCE_REQUIREMENTS.csv",
            "inputs_present": "none",
            "required_inputs": "C_gamma_source_weight;Delta_w_source;weak_field_response_map;source_file",
            "derivation_status": "MISSING_RESPONSE_OPERATOR",
            "valid_for_claim": "false",
            "notes": "PPN gamma source-weight response missing.",
        },
        {
            "prediction_id": "PRED1064_2_PPN_beta_source_weight",
            "arena": "PPN_Newton",
            "product_symbol": "P_PPN_source_weight_beta",
            "product_value": "MISSING_C_BETA_SOURCE_WEIGHT_PRODUCT",
            "product_units": "dimensionless",
            "product_source": "source-intake/mts_residuals/P8_Y5_R10_1064_NUMERIC_SOURCE_REQUIREMENTS.csv",
            "inputs_present": "none",
            "required_inputs": "C_beta_source_weight;Delta_w_source;second_order_response_map;source_file",
            "derivation_status": "MISSING_RESPONSE_OPERATOR",
            "valid_for_claim": "false",
            "notes": "PPN beta source-weight response missing.",
        },
        {
            "prediction_id": "PRED1064_3_Gdot_relative_source_weight",
            "arena": "Gdot_orbital",
            "product_symbol": "P_Gdot_relative_source_weight",
            "product_value": "MISSING_DLN_W_SOURCE_DT",
            "product_units": "yr^-1",
            "product_source": "source-intake/mts_residuals/P8_Y5_R10_1064_NUMERIC_SOURCE_REQUIREMENTS.csv",
            "inputs_present": "none",
            "required_inputs": "dln_w_source_dt;time_map;source-frame convention;source_file",
            "derivation_status": "MISSING_TIME_MAP",
            "valid_for_claim": "false",
            "notes": "Gdot source-weight drift missing.",
        },
        {
            "prediction_id": "PRED1064_4_R10_relative_weight_lambda",
            "arena": "R10_short_range",
            "product_symbol": "P_R10_relative_weight(lambda)",
            "product_value": "MISSING_KW_DELTAW_SOURCE_DELTAW_TEST_TAU_R10_PRODUCT",
            "product_units": "dimensionless",
            "product_source": "source-intake/mts_residuals/P8_Y5_R10_1064_NUMERIC_SOURCE_REQUIREMENTS.csv",
            "inputs_present": "none",
            "required_inputs": "lambda_w;K_w(lambda);Delta_w_source;Delta_w_test;tau_R10;alpha_bound(lambda);source_file",
            "derivation_status": "MISSING_R10_RELATIVE_WEIGHT_PRODUCT",
            "valid_for_claim": "false",
            "notes": "R10 finite-range source-weight product missing.",
        },
    ]


def bound_rows() -> list[dict[str, str]]:
    return [
        {
            "bound_id": "BOUND1064_0_WEP_source_charge",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "P_WEP_relative_source_weight",
            "bound_value": "2.8e-15",
            "bound_units": "dimensionless",
            "bound_source": "source-intake/local_bounds/local_bound_claims.csv",
            "source_row": "R1_WEP_source_charge",
            "bound_type": "numeric_bound_nonclaim",
            "valid_for_claim": "false",
            "notes": "Prediction missing; bound anchor only.",
        },
        {
            "bound_id": "BOUND1064_1_PPN_gamma",
            "arena": "PPN_Newton",
            "product_symbol": "P_PPN_source_weight_gamma",
            "bound_value": "2.3e-05",
            "bound_units": "dimensionless",
            "bound_source": "source-intake/local_bounds/local_bound_claims.csv",
            "source_row": "R3_gamma",
            "bound_type": "numeric_bound_nonclaim",
            "valid_for_claim": "false",
            "notes": "Cassini gamma anchor; source-weight response missing.",
        },
        {
            "bound_id": "BOUND1064_2_PPN_beta",
            "arena": "PPN_Newton",
            "product_symbol": "P_PPN_source_weight_beta",
            "bound_value": "7.8e-05",
            "bound_units": "dimensionless",
            "bound_source": "source-intake/local_bounds/local_bound_claims.csv",
            "source_row": "R4_beta",
            "bound_type": "numeric_bound_nonclaim",
            "valid_for_claim": "false",
            "notes": "PPN beta anchor; source-weight response missing.",
        },
        {
            "bound_id": "BOUND1064_3_Gdot",
            "arena": "Gdot_orbital",
            "product_symbol": "P_Gdot_relative_source_weight",
            "bound_value": "9.6e-15",
            "bound_units": "yr^-1",
            "bound_source": "source-intake/local_bounds/local_bound_claims.csv",
            "source_row": "R9_Gdot",
            "bound_type": "numeric_bound_nonclaim",
            "valid_for_claim": "false",
            "notes": "LLR Gdot anchor; time map missing.",
        },
        {
            "bound_id": "BOUND1064_4_R10_alpha_lambda",
            "arena": "R10_short_range",
            "product_symbol": "P_R10_relative_weight(lambda)",
            "bound_value": "MISSING_PROMOTED_ALPHA_LAMBDA_CURVE",
            "bound_units": "range-dependent",
            "bound_source": "source-intake/local_bounds/local_bound_claims.csv",
            "source_row": "R10_fifth_force",
            "bound_type": "symbolic_curve_required",
            "valid_for_claim": "false",
            "notes": "R10 curve not promoted for this runner.",
        },
    ]


def product_status_rows(product_result: dict[str, Any]) -> list[dict[str, str]]:
    status = product_result["status"]
    return [
        {
            "runner_id": "APR1064_0_relative_weight_strict_product_runner",
            "prediction_rows": str(status.get("prediction_rows")),
            "bound_rows": str(status.get("bound_rows")),
            "valid_prediction_rows": str(status.get("valid_prediction_rows")),
            "valid_bound_rows": str(status.get("valid_bound_rows")),
            "comparison_rows": str(status.get("comparison_rows")),
            "claim_allowed": str(status.get("claim_allowed")).lower(),
            "expected_result": "reject_all_missing_relative_weight_products",
            "status_path": str(PRODUCT_RUN_DIR / "alpha_product_runner_status.json"),
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def claim_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "CG1064_0_label_forgetting_proof",
            "claim": "parent category label-forgetting is proved",
            "gate_pass": "false",
            "reason": "no-source-only-slot theorem remains an exact clause, not a parent derivation",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1064_1_no_wA_slot",
            "claim": "w_A source-only prefactor is forbidden",
            "gate_pass": "false",
            "reason": "relative prefactor counterexample survives unless parent action grammar forbids it",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1064_2_relative_weight_runner_scores",
            "claim": "relative-weight WEP/PPN/Gdot/R10 products score",
            "gate_pass": "false",
            "reason": "strict runner has valid_prediction_rows=0 and R10 bound curve remains unpromoted",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1064_3_measured_G_absorption",
            "claim": "relative weights can be absorbed into measured G",
            "gate_pass": "false",
            "reason": "only common universal range/time/species/frame independent normalization is absorbable",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1064_4_local_GR_Newton",
            "claim": "local GR/Newton source side is derived",
            "gate_pass": "false",
            "reason": "source-side coupling remains conditional and EH/R11/PPN readout gates remain open",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC1064_0_proof_status",
            "decision": "parent category label-forgetting proof remains conditional",
            "because": "the no-source-only-slot clause is exact but not derived from deeper MTS primitives",
            "next_action": "keep as parent-action contract and do not promote universal coupling",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1064_1_runner_status",
            "decision": "strict relative-weight runner contract is filled",
            "because": "WEP, PPN gamma/beta, Gdot, and R10 now have exact numeric/source requirements and refusal rows",
            "next_action": "fill one product row numerically or derive the no-w_A theorem",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1064_2_best_next",
            "decision": "next target is the no-source-only-slot parent grammar",
            "because": "this is the smallest theorem that would remove w_A rather than bounding it",
            "next_action": "1065-Y5-R10-no-source-only-slot-parent-grammar-or-first-relative-weight-numeric-row.md",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_target": "1065-Y5-R10-no-source-only-slot-parent-grammar-or-first-relative-weight-numeric-row.md",
            "objective": "try to derive the parent action grammar that forbids source-only species prefactors w_A; if the theorem still fails, fill the first numeric relative-weight row, starting with the WEP species-source charge product, with source path, units, and refusal gates.",
            "include": "allowed-action grammar, field normalization loopholes, interaction/charge normalization, w_A theorem-zero clauses, first WEP numeric row schema if theorem fails",
            "exclude": "assuming minimality, absorbing relative weights into measured G, unity shortcuts, cancellation, public local-GR/WEP/R10 claim, GitHub action, formalization-workbench edits",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def count_formalization_modified_since_start() -> int:
    if not FORMALIZATION.exists():
        return 0
    count = 0
    start_timestamp = STARTED.timestamp()
    for path in FORMALIZATION.rglob("*"):
        try:
            if path.is_file() and path.stat().st_mtime > start_timestamp:
                count += 1
        except OSError:
            continue
    return count


def validate_outputs(
    outputs: dict[str, Path],
    sources: list[dict[str, str]],
    proof: list[dict[str, str]],
    slots: list[dict[str, str]],
    schema: list[dict[str, str]],
    requirements: list[dict[str, str]],
    common_guards: list[dict[str, str]],
    predictions: list[dict[str, str]],
    bounds: list[dict[str, str]],
    product_result: dict[str, Any],
    claims: list[dict[str, str]],
    next_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    checks: list[dict[str, str]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        checks.append({"check_id": check_id, "result": "pass" if passed else "fail", "detail": detail, "generated_utc": stamp()})

    sources_ok = bool(sources) and all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources)
    add("V1064_1_sources_exist_and_needles", sources_ok, "every cited local source path exists and every source needle was found")
    proof_rejected = any(row["proof_id"] == "PLF1064_5_verdict" and row["proof_result"] == "CONDITIONAL_CONTRACT_NOT_PARENT_DERIVED" for row in proof)
    add("V1064_2_label_forgetting_not_promoted", proof_rejected, "label-forgetting proof remains conditional")
    slot_live = any(row["slot_id"] == "NSS1064_2_relative_weight" and row["current_status"] == "retained_nonclaim" for row in slots)
    add("V1064_3_wA_slot_retained", slot_live, "relative source-weight slot is retained as nonclaim countermodel")
    schema_ok = len(schema) == len(PRODUCT_REQUIRED_COLUMNS)
    add("V1064_4_runner_schema_written", schema_ok, "strict product-runner schema written")
    req_ok = len(requirements) == 5 and all(row["valid_for_claim"] == "false" for row in requirements)
    add("V1064_5_numeric_requirements_written", req_ok, "WEP, PPN gamma/beta, Gdot, and R10 numeric/source requirements written")
    guard_ok = len(common_guards) >= 3 and all(row["valid_for_claim"] == "false" for row in common_guards)
    add("V1064_6_common_mode_guard_written", guard_ok, "measured-G common-mode guard written")
    predictions_nonclaim = len(predictions) == 5 and all(row["valid_for_claim"] == "false" and "MISSING" in json.dumps(row) for row in predictions)
    add("V1064_7_prediction_templates_nonclaim", predictions_nonclaim, "all relative-weight prediction templates remain missing-input placeholders")
    bounds_ok = any(row["bound_id"] == "BOUND1064_3_Gdot" and row["bound_value"] == "9.6e-15" for row in bounds) and any(row["bound_id"] == "BOUND1064_0_WEP_source_charge" for row in bounds)
    add("V1064_8_bound_import_written", bounds_ok, "WEP/PPN/Gdot bound anchors imported and R10 remains curve-required")
    product_refused = product_result["status"].get("valid_prediction_rows") == 0 and product_result["status"].get("claim_allowed") is False
    add("V1064_9_product_runner_refuses_placeholders", product_refused, "product runner refuses all strict relative-weight placeholders")
    claims_blocked = bool(claims) and all(row["gate_pass"] == "false" and row["claim_allowed"] == "false" for row in claims)
    add("V1064_10_claim_gates_blocked", claims_blocked, "all label-forgetting and relative-weight claim gates remain blocked")
    next_ok = bool(next_rows) and next_rows[0]["next_target"].startswith("1065-Y5-R10-no-source-only-slot")
    add("V1064_11_next_target_written", next_ok, "next target selects no-source-only-slot grammar or first numeric row")
    generated_inside = all(ROOT in path.resolve().parents or path.resolve() == ROOT for path in outputs.values())
    add("V1064_12_generated_files_in_post_checkpoint", generated_inside, "all generated files are under post-checkpoint-work")
    formalization_count = count_formalization_modified_since_start()
    add("V1064_13_formalization_untouched", formalization_count == 0, f"formalization-workbench modified-file count since script start is {formalization_count}")

    summary_pass = all(row["result"] == "pass" for row in checks)
    checks.insert(0, {"check_id": "V1064_SUMMARY", "result": "pass" if summary_pass else "fail", "detail": "1064 parent category label-forgetting / relative-weight runner validation summary", "generated_utc": stamp()})
    return checks


def write_doc(
    sources: list[dict[str, str]],
    proof: list[dict[str, str]],
    slots: list[dict[str, str]],
    schema: list[dict[str, str]],
    requirements: list[dict[str, str]],
    common_guards: list[dict[str, str]],
    predictions: list[dict[str, str]],
    bounds: list[dict[str, str]],
    product_status: list[dict[str, str]],
    product_comparisons: list[dict[str, Any]],
    claims: list[dict[str, str]],
    decisions: list[dict[str, str]],
    validation: list[dict[str, str]],
    next_rows: list[dict[str, str]],
) -> None:
    text = "\n".join(
        [
            "# 1064 - Parent Category Label-Forgetting Proof Or Relative-Weight Runner Fill",
            "",
            "**Current verdict:** label-forgetting is still a conditional parent-action contract, not a theorem. The exact missing clause is the no-source-only-slot rule for `w_A`.",
            "",
            "**Runner result:** the strict relative-weight runner contract now covers WEP, PPN gamma, PPN beta, Gdot, and R10, and it refuses all current placeholders.",
            "",
            "**Coupling discipline:** a common source normalization can be absorbed into measured `G` only if it is universal, species-blind, range-independent, time-independent, and same-frame. Relative weights cannot hide there.",
            "",
            "## Source Register",
            md_table(sources, ["source_id", "relative_path", "exists", "needle", "needle_found", "note"]),
            "",
            "## Parent Label-Forgetting Proof Attempt",
            md_table(proof, ["proof_id", "step", "mathematical_form", "proof_result", "support", "gap", "parent_signed"]),
            "",
            "## No-Source-Only-Slot Audit",
            md_table(slots, ["slot_id", "slot", "allowed_status", "required_signature", "if_present", "current_status"]),
            "",
            "## Strict Runner Schema",
            md_table(schema, ["column", "definition", "required", "nonclaim_rule"]),
            "",
            "## Numeric Source Requirements",
            md_table(requirements, ["requirement_id", "arena", "product_symbol", "required_inputs", "units", "bound_or_target", "source_requirement", "current_status"]),
            "",
            "## Measured-G Common-Mode Guard",
            md_table(common_guards, ["guard_id", "candidate_absorption", "required_zero_derivatives", "must_be", "current_status", "if_failed"]),
            "",
            "## Product Prediction Templates",
            md_table(predictions, ["prediction_id", "arena", "product_symbol", "product_value", "product_units", "required_inputs", "derivation_status", "valid_for_claim"]),
            "",
            "## Bound Import",
            md_table(bounds, ["bound_id", "arena", "product_symbol", "bound_value", "bound_units", "bound_type", "valid_for_claim"]),
            "",
            "## Product Runner Status",
            md_table(product_status, ["runner_id", "prediction_rows", "bound_rows", "valid_prediction_rows", "valid_bound_rows", "comparison_rows", "claim_allowed", "expected_result"]),
            "",
            "## Product Comparison Rows",
            md_table(product_comparisons, ["comparison_id", "arena", "product_symbol", "product_value", "bound_value", "comparison_status", "pass_for_claim", "issues"]),
            "",
            "## Claim Gates",
            md_table(claims, ["gate_id", "claim", "gate_pass", "reason", "claim_allowed", "valid_for_claim"]),
            "",
            "## Decision Ledger",
            md_table(decisions, ["decision_id", "decision", "because", "next_action", "valid_for_claim"]),
            "",
            "## Validation",
            md_table(validation, ["check_id", "result", "detail", "generated_utc"]),
            "",
            "## Next Target",
            md_table(next_rows, ["next_target", "objective", "include", "exclude", "valid_for_claim"]),
            "",
        ]
    )
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    sources = source_register_rows()
    proof = proof_attempt_rows()
    slots = no_source_slot_rows()
    schema = runner_schema_rows()
    requirements = numeric_requirement_rows()
    common_guards = common_mode_guard_rows()
    predictions = prediction_rows()
    bounds = bound_rows()
    claims = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    outputs = {
        "sources": OUT / "P8_Y5_R10_1064_SOURCE_REGISTER.csv",
        "proof": OUT / "P8_Y5_R10_1064_LABEL_FORGETTING_PROOF_ATTEMPT.csv",
        "slots": OUT / "P8_Y5_R10_1064_NO_SOURCE_ONLY_SLOT_AUDIT.csv",
        "schema": OUT / "P8_Y5_R10_1064_RELATIVE_WEIGHT_RUNNER_SCHEMA.csv",
        "requirements": OUT / "P8_Y5_R10_1064_NUMERIC_SOURCE_REQUIREMENTS.csv",
        "common_guards": OUT / "P8_Y5_R10_1064_COMMON_MODE_GUARD.csv",
        "predictions": PREDICTION_TEMPLATE,
        "bounds": BOUND_IMPORT,
        "runner_status": OUT / "P8_Y5_R10_1064_PRODUCT_RUNNER_STATUS.csv",
        "comparisons": OUT / "P8_Y5_R10_1064_PRODUCT_COMPARISON_ROWS.csv",
        "claims": OUT / "P8_Y5_R10_1064_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_R10_1064_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_R10_1064_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_1064_VALIDATION.csv",
        "doc": DOC,
    }

    write_csv(outputs["sources"], sources)
    write_csv(outputs["proof"], proof)
    write_csv(outputs["slots"], slots)
    write_csv(outputs["schema"], schema)
    write_csv(outputs["requirements"], requirements)
    write_csv(outputs["common_guards"], common_guards)
    write_csv(outputs["predictions"], predictions, PRODUCT_REQUIRED_COLUMNS)
    write_csv(outputs["bounds"], bounds, BOUND_REQUIRED_COLUMNS)
    write_csv(outputs["claims"], claims)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["next"], next_rows)

    product_result = run_product_runner(PREDICTION_TEMPLATE, BOUND_IMPORT, PRODUCT_RUN_DIR)
    status_rows = product_status_rows(product_result)
    write_csv(outputs["runner_status"], status_rows)
    write_csv(outputs["comparisons"], product_result["comparisons"])

    validation = validate_outputs(
        outputs,
        sources,
        proof,
        slots,
        schema,
        requirements,
        common_guards,
        predictions,
        bounds,
        product_result,
        claims,
        next_rows,
    )
    write_csv(outputs["validation"], validation)
    write_doc(
        sources,
        proof,
        slots,
        schema,
        requirements,
        common_guards,
        predictions,
        bounds,
        status_rows,
        product_result["comparisons"],
        claims,
        decisions,
        validation,
        next_rows,
    )

    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    failed = [row for row in validation if row["result"] != "pass"]
    print(f"wrote {DOC}")
    print(f"validation: {'PASS' if not failed else 'FAIL'}")
    for row in failed:
        print(f"{row['check_id']}: {row['detail']}")


if __name__ == "__main__":
    main()
