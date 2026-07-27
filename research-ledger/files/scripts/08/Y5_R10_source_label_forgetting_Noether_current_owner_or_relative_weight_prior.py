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
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
DOC = ROOT / "1063-Y5-R10-source-label-forgetting-Noether-current-owner-or-relative-weight-prior.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_DIR = ROOT / "runs" / "1063-source-label-forgetting-relative-weight-prior" / "results"
PRODUCT_RUN_DIR = RUN_DIR / "product_runner"
PREDICTION_TEMPLATE = OUT / "P8_Y5_R10_1063_RELATIVE_WEIGHT_PRODUCT_TEMPLATE_NONCLAIM.csv"
BOUND_IMPORT = OUT / "P8_Y5_R10_1063_RELATIVE_WEIGHT_BOUND_IMPORT.csv"


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
        ("SRC1063_0_1062_next", "source-intake/mts_residuals/P8_Y5_R10_1062_NEXT_TARGET.csv", "1063-Y5-R10-source-label-forgetting-Noether-current-owner", "1062 handoff."),
        ("SRC1063_1_1062_premise", "source-intake/mts_residuals/P8_Y5_R10_1062_PREMISE_SIGNATURE_AUDIT.csv", "PREM1062_3_source_label_forgetting", "source-label premise."),
        ("SRC1063_2_1062_counterexample", "source-intake/mts_residuals/P8_Y5_R10_1062_COUNTEREXAMPLE_SURVIVAL_LEDGER.csv", "CE1062_1_relative_source_weight", "relative source-weight counterexample."),
        ("SRC1063_3_953_source_functor", "source-intake/mts_residuals/P8_Y5_R10_953_SOURCE_FUNCTOR_THEOREM_ATTEMPT.csv", "NSF953_5_verdict", "source-functor theorem attempt."),
        ("SRC1063_4_955_matter_lemma", "source-intake/mts_residuals/P8_Y5_R10_955_MINIMAL_MATTER_ACTION_LEMMA.csv", "MMA955_6_verdict", "minimal matter action lemma."),
        ("SRC1063_5_989_parent_input", "source-intake/mts_residuals/P8_Y5_R10_989_PARENT_INPUT_CANDIDATE_LEDGER.csv", "PIC989_2_Noether_current_owner", "Noether/current/source owner input."),
        ("SRC1063_6_989_EM_lock", "source-intake/mts_residuals/P8_Y5_R10_989_EM_LOCK_SIGNATURE_AUDIT.csv", "ELA989_2_current_owner", "EM current owner audit."),
        ("SRC1063_7_1055_counterexample", "source-intake/mts_residuals/P8_Y5_R10_1055_COUNTEREXAMPLE_LEDGER.csv", "CE1055_3_relative_source_weight", "relative source-weight ledger."),
        ("SRC1063_8_1044_pullback", "source-intake/mts_residuals/P8_Y5_R10_1044_MATTER_PULLBACK_DERIVATION.csv", "MPD1044_6_source_current_universality", "matter source-current universality gap."),
        ("SRC1063_9_990_contract", "source-intake/mts_residuals/P8_Y5_R10_990_PARENT_ACTION_CONTRACT.csv", "PAC990_4_source_charge", "minimal parent action source charge contract."),
        ("SRC1063_10_393_doc", "393-source-normalized-Newtonian-limit-under-identity-closure.md", "Only a constant, universal, range-independent", "measured-G common-mode absorption rule."),
        ("SRC1063_11_639_matrix", "source-intake/mts_residuals/P8_Y5_R10_639_LOCAL_BOUND_MATRIX.csv", "LBM639_10", "local WEP/PPN/R10 bound matrix."),
        ("SRC1063_12_708_map", "source-intake/mts_residuals/P8_Y5_R10_708_PPN_GDOT_WEP_MAP.csv", "PGW708_4_R10_alpha", "PPN/Gdot/WEP/R10 projection map."),
        ("SRC1063_13_768_GR_Newton", "source-intake/mts_residuals/P8_Y5_R10_768_GR_NEWTON_REQUIREMENT_MAP.csv", "GN768_2_source_charge", "GR/Newton source charge requirement."),
        ("SRC1063_14_768_live_edge", "source-intake/mts_residuals/P8_Y5_R10_768_R11_SOURCE_NORMALIZATION_LIVE_EDGE.csv", "RSN768_0_cmu_sum_rule", "source-normalization live edge."),
        ("SRC1063_15_local_bounds", "source-intake/local_bounds/local_bound_claims.csv", "R1_WEP_source_charge", "local WEP/PPN/R10 bound anchors."),
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


def theorem_attempt_rows() -> list[dict[str, str]]:
    return [
        {
            "step_id": "THM1063_0_target",
            "claim_shape": "derive species-blind source-label forgetting and one Noether/Hilbert current owner",
            "formal_statement": "Admissible source functor should take T_total as input, not labelled pairs (T_A,A).",
            "attempt_result": "TARGET_RESTATED",
            "why_it_matters": "if labels are absent, relative source weights kappa_A/kappa_B cannot be formed",
            "current_gap": "parent matter category still exposes labels unless a deeper quotient forgets them",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "step_id": "THM1063_1_additivity",
            "claim_shape": "covariance plus additivity gives a unique source current",
            "formal_statement": "F_src(T_A+T_B)=F_src(T_A)+F_src(T_B) removes nonlinear source mixing.",
            "attempt_result": "INSUFFICIENT_ALONE",
            "why_it_matters": "it is a useful theorem ingredient, but not enough",
            "current_gap": "F((T_A,A))=kappa_A T_A is still additive and covariant",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "step_id": "THM1063_2_same_action_Hilbert_source",
            "claim_shape": "same S_matter gives equations of motion and Hilbert stress source",
            "formal_statement": "E_A=delta S_matter/delta Psi_A and T_A=2/sqrt(-g) delta S_A/delta g_obs.",
            "attempt_result": "STRONG_CONDITIONAL_LEMMA",
            "why_it_matters": "rules out a separate arbitrary source functional",
            "current_gap": "constant relative prefactors w_A inside S_A survive unless parent minimality is signed",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "step_id": "THM1063_3_Noether_current_owner",
            "claim_shape": "same parent Noether owner fixes charge labels, matter coupling, and source normalization",
            "formal_statement": "one parent current J_owner produces observed source/test coupling with no species-only coefficient slot",
            "attempt_result": "OWNER_NOT_DERIVED",
            "why_it_matters": "would close beta_source_alpha-like source normalization debts",
            "current_gap": "PIC989_2 and ELA989_2 still mark Noether/current owner as candidate-missing/unsigned",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "step_id": "THM1063_4_measured_G_absorption",
            "claim_shape": "measured G can absorb source normalization",
            "formal_statement": "only common, universal, range-independent source normalization may be absorbed into measured G",
            "attempt_result": "COMMON_MODE_ONLY",
            "why_it_matters": "prevents fake Newton wins",
            "current_gap": "relative, range-dependent, radial, time-dependent, or species-labelled weights remain physical residuals",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "step_id": "THM1063_5_verdict",
            "claim_shape": "source-label forgetting / Noether current theorem",
            "formal_statement": "label-forgotten source functor + same-action Hilbert source + current owner => one universal source normalization",
            "attempt_result": "CONDITIONAL_THEOREM_NOT_PARENT_DERIVED",
            "why_it_matters": "this is the clean path to GR-style universal coupling",
            "current_gap": "relative w_A counterexample survives current corpus",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def noether_owner_rows() -> list[dict[str, str]]:
    return [
        {
            "owner_id": "NO1063_0_source_functor_domain",
            "object": "source functor domain",
            "required_owner": "parent category maps ordinary matter to T_total before source coupling selection",
            "current_status": "label_forgetting_not_parent_signed",
            "if_missing": "kappa_A T_A survives as a legal additive source",
            "source": "NSF953_1_domain_fork; NSF953_5_verdict",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "owner_id": "NO1063_1_same_action_Hilbert_current",
            "object": "Hilbert matter source",
            "required_owner": "same S_matter supplies matter equations and gravitational source",
            "current_status": "conditional_lemma_not_parent_derivation",
            "if_missing": "separate source current or relative prefactor can be inserted",
            "source": "MMA955_1_same_action_principle; MMA955_6_verdict",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "owner_id": "NO1063_2_Noether_current_owner",
            "object": "Noether/current/source normalization",
            "required_owner": "single parent Noether owner fixes charge unit, matter coupling, and source/test normalization",
            "current_status": "candidate_missing",
            "if_missing": "beta_source_alpha and relative source weights remain free finite-branch debts",
            "source": "PIC989_2_Noether_current_owner; ELA989_2_current_owner",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "owner_id": "NO1063_3_Hamiltonian_source_charge",
            "object": "measured Newtonian source mass",
            "required_owner": "integrable fixed-reference Hamiltonian source charge with same-frame source measure",
            "current_status": "selected_live_edge_not_closed",
            "if_missing": "EH-looking equations still lack measured Newtonian GM/source normalization",
            "source": "PAC990_4_source_charge; GN768_2_source_charge",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def relative_weight_prior_rows() -> list[dict[str, str]]:
    return [
        {
            "prior_id": "RWP1063_0_common_weight",
            "quantity": "w_common",
            "definition": "one common multiplier on the whole matter/source action",
            "observable_channel": "measured_G_common_mode",
            "current_status": "absorbable_only_if_constant_universal_range_independent",
            "required_for_claim": "prove no species, time, radial, range, or frame dependence before absorption",
            "bound_or_target": "calibration_only_not_a_test_pass",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "prior_id": "RWP1063_1_delta_w_WEP",
            "quantity": "Delta_w_AB",
            "definition": "relative source weight contrast between MICROSCOPE test materials",
            "observable_channel": "WEP_source_charge_eta_AB",
            "current_status": "MISSING_NUMERIC_OR_THEOREM_ZERO_RELATIVE_WEIGHT",
            "required_for_claim": "parent label-forgetting theorem or sourced Delta_w_AB with tau_WEP/material map",
            "bound_or_target": "eta_AB <= 2.8e-15",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "prior_id": "RWP1063_2_delta_w_PPN",
            "quantity": "C_PPN_source_weight * Delta_w_source",
            "definition": "source normalization response of PPN gamma/beta to relative source weights",
            "observable_channel": "PPN_gamma_beta_Newton_source_normalization",
            "current_status": "MISSING_RESPONSE_OPERATOR",
            "required_for_claim": "weak-field response map from relative source weights into gamma/beta or theorem-zero",
            "bound_or_target": "gamma-1 <= 2.3e-05; beta-1 <= 7.8e-05",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "prior_id": "RWP1063_3_delta_w_Gdot",
            "quantity": "d_t ln w_source",
            "definition": "time drift of source normalization if relative source weights move",
            "observable_channel": "Gdot_over_G",
            "current_status": "MISSING_TIME_MAP",
            "required_for_claim": "time map and proof that any surviving source weight is constant or below bound",
            "bound_or_target": "Gdot/G <= 9.6e-15 yr^-1",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "prior_id": "RWP1063_4_delta_w_R10",
            "quantity": "K_w(lambda) Delta_w_source Delta_w_test",
            "definition": "finite-range relative-weight source/test product for inverse-square/R10 tests",
            "observable_channel": "R10_alpha_lambda",
            "current_status": "MISSING_KW_LAMBDA_SOURCE_TEST_WEIGHTS",
            "required_for_claim": "range, coupling normalization, source/test weights, tau_R10, and promoted alpha(lambda) bound curve",
            "bound_or_target": "alpha(lambda) curve required",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def prediction_rows() -> list[dict[str, str]]:
    return [
        {
            "prediction_id": "PRED1063_0_WEP_relative_source_weight",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "P_WEP_relative_source_weight",
            "product_value": "MISSING_DELTA_W_AB_TAU_WEP_PRODUCT",
            "product_units": "dimensionless",
            "product_source": "source-intake/mts_residuals/P8_Y5_R10_1063_RELATIVE_WEIGHT_PRIOR_MATRIX.csv",
            "inputs_present": "none",
            "required_inputs": "Delta_w_TA6V_minus_PtRh10;tau_WEP;source-label-forgetting theorem OR numeric product",
            "derivation_status": "MISSING_NUMERIC_OR_THEOREM_ZERO_RELATIVE_WEIGHT",
            "valid_for_claim": "false",
            "notes": "Direct WEP source-charge row; no relative source weight is derived.",
        },
        {
            "prediction_id": "PRED1063_1_PPN_gamma_source_weight",
            "arena": "PPN_Newton",
            "product_symbol": "P_PPN_source_weight_gamma",
            "product_value": "MISSING_C_GAMMA_SOURCE_WEIGHT_PRODUCT",
            "product_units": "dimensionless",
            "product_source": "source-intake/mts_residuals/P8_Y5_R10_1063_RELATIVE_WEIGHT_PRIOR_MATRIX.csv",
            "inputs_present": "none",
            "required_inputs": "C_gamma_source_weight;Delta_w_source;weak_field_response_map OR theorem-zero",
            "derivation_status": "MISSING_RESPONSE_OPERATOR",
            "valid_for_claim": "false",
            "notes": "PPN gamma cannot be scored until source-weight response is mapped.",
        },
        {
            "prediction_id": "PRED1063_2_PPN_beta_source_weight",
            "arena": "PPN_Newton",
            "product_symbol": "P_PPN_source_weight_beta",
            "product_value": "MISSING_C_BETA_SOURCE_WEIGHT_PRODUCT",
            "product_units": "dimensionless",
            "product_source": "source-intake/mts_residuals/P8_Y5_R10_1063_RELATIVE_WEIGHT_PRIOR_MATRIX.csv",
            "inputs_present": "none",
            "required_inputs": "C_beta_source_weight;Delta_w_source;weak_field_response_map OR theorem-zero",
            "derivation_status": "MISSING_RESPONSE_OPERATOR",
            "valid_for_claim": "false",
            "notes": "PPN beta cannot be scored until source-weight response is mapped.",
        },
        {
            "prediction_id": "PRED1063_3_R10_relative_weight_lambda",
            "arena": "R10_short_range",
            "product_symbol": "P_R10_relative_weight(lambda)",
            "product_value": "MISSING_KW_DELTAW_SOURCE_DELTAW_TEST_TAU_R10_PRODUCT",
            "product_units": "dimensionless",
            "product_source": "source-intake/mts_residuals/P8_Y5_R10_1063_RELATIVE_WEIGHT_PRIOR_MATRIX.csv",
            "inputs_present": "none",
            "required_inputs": "lambda_w;K_w(lambda);Delta_w_source;Delta_w_test;tau_R10;alpha_bound(lambda) OR theorem-zero",
            "derivation_status": "MISSING_R10_RELATIVE_WEIGHT_PRODUCT",
            "valid_for_claim": "false",
            "notes": "R10 row remains symbolic until finite range and source/test weights are real.",
        },
    ]


def bound_rows() -> list[dict[str, str]]:
    return [
        {
            "bound_id": "BOUND1063_0_WEP_source_charge",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "P_WEP_relative_source_weight",
            "bound_value": "2.8e-15",
            "bound_units": "dimensionless",
            "bound_source": "source-intake/local_bounds/local_bound_claims.csv",
            "source_row": "R1_WEP_source_charge",
            "bound_type": "numeric_bound_nonclaim",
            "valid_for_claim": "false",
            "notes": "MICROSCOPE WEP source-charge anchor; prediction missing.",
        },
        {
            "bound_id": "BOUND1063_1_PPN_gamma",
            "arena": "PPN_Newton",
            "product_symbol": "P_PPN_source_weight_gamma",
            "bound_value": "2.3e-05",
            "bound_units": "dimensionless",
            "bound_source": "source-intake/local_bounds/local_bound_claims.csv",
            "source_row": "R3_gamma",
            "bound_type": "numeric_bound_nonclaim",
            "valid_for_claim": "false",
            "notes": "Cassini gamma anchor; source-weight response not mapped.",
        },
        {
            "bound_id": "BOUND1063_2_PPN_beta",
            "arena": "PPN_Newton",
            "product_symbol": "P_PPN_source_weight_beta",
            "bound_value": "7.8e-05",
            "bound_units": "dimensionless",
            "bound_source": "source-intake/local_bounds/local_bound_claims.csv",
            "source_row": "R4_beta",
            "bound_type": "numeric_bound_nonclaim",
            "valid_for_claim": "false",
            "notes": "PPN beta anchor; source-weight response not mapped.",
        },
        {
            "bound_id": "BOUND1063_3_R10_alpha_lambda",
            "arena": "R10_short_range",
            "product_symbol": "P_R10_relative_weight(lambda)",
            "bound_value": "MISSING_PROMOTED_ALPHA_LAMBDA_CURVE",
            "bound_units": "range-dependent",
            "bound_source": "source-intake/local_bounds/local_bound_claims.csv",
            "source_row": "R10_fifth_force",
            "bound_type": "symbolic_curve_required",
            "valid_for_claim": "false",
            "notes": "R10 needs a promoted curve and finite-range product before scoring.",
        },
    ]


def product_status_rows(product_result: dict[str, Any]) -> list[dict[str, str]]:
    status = product_result["status"]
    return [
        {
            "runner_id": "APR1063_0_relative_weight_product_runner",
            "prediction_rows": str(status.get("prediction_rows")),
            "bound_rows": str(status.get("bound_rows")),
            "valid_prediction_rows": str(status.get("valid_prediction_rows")),
            "valid_bound_rows": str(status.get("valid_bound_rows")),
            "comparison_rows": str(status.get("comparison_rows")),
            "claim_allowed": str(status.get("claim_allowed")).lower(),
            "expected_result": "reject_all_relative_weight_placeholders",
            "status_path": str(PRODUCT_RUN_DIR / "alpha_product_runner_status.json"),
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def claim_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "CG1063_0_source_label_forgetting",
            "claim": "source-label forgetting is derived",
            "gate_pass": "false",
            "reason": "conditional theorem exists but the parent category has not removed labels before source selection",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1063_1_Noether_current_owner",
            "claim": "Noether/current owner fixes source normalization",
            "gate_pass": "false",
            "reason": "PIC989_2 remains candidate_missing and ELA989_2 remains unsigned",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1063_2_relative_weights_zero",
            "claim": "relative source weights vanish",
            "gate_pass": "false",
            "reason": "w_A counterexample survives same-action/additivity unless parent minimality is derived",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1063_3_WEP_PPN_R10_scores",
            "claim": "relative-weight products score WEP/PPN/R10",
            "gate_pass": "false",
            "reason": "all prediction products are placeholders and product runner has valid_prediction_rows=0",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1063_4_local_GR_Newton",
            "claim": "local GR/Newton follows from source coupling",
            "gate_pass": "false",
            "reason": "source coupling is one required gate; EH/R11/operator/PPN readout remain open",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC1063_0_theorem_status",
            "decision": "source-label forgetting is a clean conditional theorem but not current derivation",
            "because": "labels must be removed before source coupling selection; current corpus has not signed that category step",
            "next_action": "keep theorem as parent-action contract",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1063_1_counterexample_status",
            "decision": "relative source weights are retained as explicit coupling debts",
            "because": "w_A survives covariance, Ward/additivity, and same-action rhetoric when parent minimality is unsigned",
            "next_action": "use product templates for WEP/PPN/R10 rather than hiding the coupling",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1063_2_best_next",
            "decision": "next target is parent category label-forgetting proof or relative-weight numeric fill",
            "because": "this is the least hand-wavy route to universal coupling and measured-G source normalization",
            "next_action": "1064-Y5-R10-parent-category-label-forgetting-proof-or-relative-weight-runner-fill.md",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_target": "1064-Y5-R10-parent-category-label-forgetting-proof-or-relative-weight-runner-fill.md",
            "objective": "try to prove the parent category forgets species/source labels before coupling selection; if not, fill a strict relative-weight runner schema with numeric/source requirements for WEP, PPN/Newton, Gdot, and R10 without claiming a pass.",
            "include": "category-domain proof attempt, no-source-only-slot theorem, w_A prior-width requirements, WEP/PPN/Gdot/R10 product runner schema, measured-G common-mode guard",
            "exclude": "assuming WEP, absorbing relative weights into G, unity shortcuts, cancellation, public local-GR/WEP/R10 claim, GitHub action, formalization-workbench edits",
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
    theorem: list[dict[str, str]],
    owners: list[dict[str, str]],
    priors: list[dict[str, str]],
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
    add("V1063_1_sources_exist_and_needles", sources_ok, "every cited local source path exists and every source needle was found")
    theorem_ok = any(row["step_id"] == "THM1063_5_verdict" and row["attempt_result"] == "CONDITIONAL_THEOREM_NOT_PARENT_DERIVED" for row in theorem)
    add("V1063_2_theorem_not_promoted", theorem_ok, "source-label theorem is conditional and not promoted")
    owners_ok = any(row["owner_id"] == "NO1063_2_Noether_current_owner" and row["current_status"] == "candidate_missing" for row in owners)
    add("V1063_3_Noether_owner_missing", owners_ok, "Noether/current owner remains missing")
    priors_ok = len(priors) >= 5 and all(row["valid_for_claim"] == "false" for row in priors)
    add("V1063_4_relative_weight_priors_written", priors_ok, "relative-weight prior/debt rows cover common, WEP, PPN, Gdot, and R10 channels")
    predictions_nonclaim = len(predictions) == 4 and all(row["valid_for_claim"] == "false" and "MISSING" in json.dumps(row) for row in predictions)
    add("V1063_5_prediction_templates_nonclaim", predictions_nonclaim, "all relative-weight prediction rows are missing-input placeholders")
    bound_numeric = any(row["bound_id"] == "BOUND1063_0_WEP_source_charge" and row["bound_value"] == "2.8e-15" for row in bounds) and any(row["bound_id"] == "BOUND1063_1_PPN_gamma" for row in bounds)
    add("V1063_6_bound_import_written", bound_numeric, "WEP and PPN numeric bound anchors are imported")
    product_refused = product_result["status"].get("valid_prediction_rows") == 0 and product_result["status"].get("claim_allowed") is False
    add("V1063_7_product_runner_refuses_placeholders", product_refused, "product runner refuses all relative-weight placeholders")
    claims_blocked = bool(claims) and all(row["gate_pass"] == "false" and row["claim_allowed"] == "false" for row in claims)
    add("V1063_8_claim_gates_blocked", claims_blocked, "all relative-weight and local-GR claim gates remain blocked")
    next_ok = bool(next_rows) and next_rows[0]["next_target"].startswith("1064-Y5-R10-parent-category-label-forgetting")
    add("V1063_9_next_target_written", next_ok, "next target selects parent-category label forgetting or relative-weight runner fill")
    generated_inside = all(ROOT in path.resolve().parents or path.resolve() == ROOT for path in outputs.values())
    add("V1063_10_generated_files_in_post_checkpoint", generated_inside, "all generated files are under post-checkpoint-work")
    formalization_count = count_formalization_modified_since_start()
    add("V1063_11_formalization_untouched", formalization_count == 0, f"formalization-workbench modified-file count since script start is {formalization_count}")

    summary_pass = all(row["result"] == "pass" for row in checks)
    checks.insert(0, {"check_id": "V1063_SUMMARY", "result": "pass" if summary_pass else "fail", "detail": "1063 source-label / Noether current / relative-weight validation summary", "generated_utc": stamp()})
    return checks


def write_doc(
    sources: list[dict[str, str]],
    theorem: list[dict[str, str]],
    owners: list[dict[str, str]],
    priors: list[dict[str, str]],
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
            "# 1063 - Source-Label Forgetting, Noether Current Owner, Or Relative-Weight Prior",
            "",
            "**Current verdict:** the universal-coupling theorem is clean but still conditional. The current corpus does not yet prove that the parent source functor forgets species labels before source coupling selection.",
            "",
            "**Coupling wound:** a constant relative source weight `w_A` survives covariance, Ward/additivity, and same-action language unless the parent category forbids source-only species slots.",
            "",
            "**Practical result:** relative source weights are now explicit nonclaim product debts across WEP, PPN/Newton, Gdot, and R10. They cannot be hidden inside measured `G` unless they are common, universal, range-independent, time-independent, and species-blind.",
            "",
            "## Source Register",
            md_table(sources, ["source_id", "relative_path", "exists", "needle", "needle_found", "note"]),
            "",
            "## Source-Forgetting Theorem Attempt",
            md_table(theorem, ["step_id", "claim_shape", "formal_statement", "attempt_result", "why_it_matters", "current_gap"]),
            "",
            "## Noether / Source Owner Audit",
            md_table(owners, ["owner_id", "object", "required_owner", "current_status", "if_missing", "source"]),
            "",
            "## Relative-Weight Prior Matrix",
            md_table(priors, ["prior_id", "quantity", "definition", "observable_channel", "current_status", "required_for_claim", "bound_or_target"]),
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
    theorem = theorem_attempt_rows()
    owners = noether_owner_rows()
    priors = relative_weight_prior_rows()
    predictions = prediction_rows()
    bounds = bound_rows()
    claims = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    outputs = {
        "sources": OUT / "P8_Y5_R10_1063_SOURCE_REGISTER.csv",
        "theorem": OUT / "P8_Y5_R10_1063_SOURCE_FORGETTING_THEOREM_ATTEMPT.csv",
        "owners": OUT / "P8_Y5_R10_1063_NOETHER_SOURCE_OWNER_AUDIT.csv",
        "priors": OUT / "P8_Y5_R10_1063_RELATIVE_WEIGHT_PRIOR_MATRIX.csv",
        "predictions": PREDICTION_TEMPLATE,
        "bounds": BOUND_IMPORT,
        "runner_status": OUT / "P8_Y5_R10_1063_PRODUCT_RUNNER_STATUS.csv",
        "comparisons": OUT / "P8_Y5_R10_1063_PRODUCT_COMPARISON_ROWS.csv",
        "claims": OUT / "P8_Y5_R10_1063_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_R10_1063_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_R10_1063_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_1063_VALIDATION.csv",
        "doc": DOC,
    }

    write_csv(outputs["sources"], sources)
    write_csv(outputs["theorem"], theorem)
    write_csv(outputs["owners"], owners)
    write_csv(outputs["priors"], priors)
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
        theorem,
        owners,
        priors,
        predictions,
        bounds,
        product_result,
        claims,
        next_rows,
    )
    write_csv(outputs["validation"], validation)
    write_doc(
        sources,
        theorem,
        owners,
        priors,
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
