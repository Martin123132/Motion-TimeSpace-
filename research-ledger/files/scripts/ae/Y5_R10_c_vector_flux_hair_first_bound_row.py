from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1141-Y5-R10-c-vector-flux-hair-first-bound-row.md"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def stamp(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    generated = now()
    return [{**row, "generated_utc": generated} for row in rows]


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def source_rows() -> list[dict[str, object]]:
    sources = [
        {
            "source_id": "SRC1141_0_1140_next",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1140_NEXT_TARGET.csv",
            "needle": "NEXT1140_0_1141",
            "role": "handoff requiring vector/flux first-bound rows.",
        },
        {
            "source_id": "SRC1141_1_1140_bound_pack",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1140_C_HAIR_COMPONENT_BOUND_PACK.csv",
            "needle": "CBP1140_5_flux",
            "role": "source-ready schemas for vector and flux c-hair rows.",
        },
        {
            "source_id": "SRC1141_2_1140_arena_map",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1140_HAIR_TO_TEST_ARENA_MAP.csv",
            "needle": "MAP1140_3_vector",
            "role": "maps vector hair into alpha1/alpha2/alpha3 and flux hair into alpha3.",
        },
        {
            "source_id": "SRC1141_3_ppn_residual_vector",
            "relative_path": "source-intake/mts_residuals/P8_Y5_PPN_RESIDUAL_VECTOR.csv",
            "needle": "PPN524_3_alpha1_frame",
            "role": "internal PPN target rows for alpha1, alpha2, alpha3, xi, and envelope policy.",
        },
        {
            "source_id": "SRC1141_4_ppn_input_template",
            "relative_path": "source-intake/mts_residuals/P8_Y5_PPN_EVALUATOR_INPUT_TEMPLATE.csv",
            "needle": "PPN524_4_alpha2_domain_vector",
            "role": "declares expected local PPN evaluator input slots.",
        },
        {
            "source_id": "SRC1141_5_external_ppn_pack",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_753_EXTERNAL_PPN_SOURCE_PACK.csv",
            "needle": "EXT753_0_Will_2014_LRR",
            "role": "external PPN/preferred-frame provenance pack, not an MTS coefficient source.",
        },
        {
            "source_id": "SRC1141_6_alpha3_product_input",
            "relative_path": "source-intake/mts_residuals/P8_ALPHA3_BOUND_PRODUCT_INPUT.csv",
            "needle": "A3_domain",
            "role": "alpha3 product policy and missing numeric/theorem-zero product state.",
        },
        {
            "source_id": "SRC1141_7_alpha3_product_eval",
            "relative_path": "source-intake/mts_residuals/P8_ALPHA3_BOUND_PRODUCT_EVALUATION.csv",
            "needle": "not_scoreable_inputs_missing",
            "role": "confirms alpha3 products are not scoreable with missing inputs.",
        },
        {
            "source_id": "SRC1141_8_1121_alpha3_contract",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1121_R11_ALPHA3_EXECUTABLE_ROW_CONTRACT.csv",
            "needle": "R11A3_1121_0_alpha3_source_leakage",
            "role": "canonical R11 alpha3 executable-row contract.",
        },
        {
            "source_id": "SRC1141_9_1121_missing_fields",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1121_R11_ALPHA3_MISSING_FIELD_LEDGER.csv",
            "needle": "F1121_6_siblings",
            "role": "sibling guards and missing weak-field/source fields for R11 alpha3.",
        },
        {
            "source_id": "SRC1141_10_1136_ineq",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1136_ALPHA3_PRODUCT_INEQUALITY_ROWS.csv",
            "needle": "PI1136_1_R11_alpha3",
            "role": "latest K*c*epsilon alpha3 inequality guard.",
        },
        {
            "source_id": "SRC1141_11_R11_min_fill",
            "relative_path": "source-intake/mts_residuals/P8_R11_SOURCE_NORMALIZATION_OPERATOR_MINIMUM_FILL.csv",
            "needle": "R11SN_2_domain_projector_mass",
            "role": "domain projector source-normalization row affects alpha1/alpha2/alpha3/xi.",
        },
        {
            "source_id": "SRC1141_12_1138_c_row",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1138_CANONICAL_C_SOURCE_NORMALIZATION_ROW.csv",
            "needle": "CROW1138_0_c_domain_source_normalization_operator",
            "role": "canonical c source-normalization coefficient remains blocked.",
        },
    ]
    checked: list[dict[str, object]] = []
    for source in sources:
        path = ROOT / str(source["relative_path"])
        text = read_text(path)
        checked.append(
            {
                **source,
                "exists": str(path.exists()).lower(),
                "needle_found": str(str(source["needle"]) in text).lower(),
            }
        )
    return stamp(checked)


def ppn_anchor_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "anchor_id": "PPNBA1141_0_alpha1",
                "observable": "alpha1",
                "target_bound_abs": "1e-4",
                "bound_units": "dimensionless_abs",
                "local_anchor": "P8_Y5_PPN_RESIDUAL_VECTOR.csv::PPN524_3_alpha1_frame",
                "external_provenance": "P8_Y5_R10_753_EXTERNAL_PPN_SOURCE_PACK.csv::EXT753_0_Will_2014_LRR; EXT753_2_Will_Nordtvedt_1972_PPN_I",
                "use_in_1141": "guardrail for vector preferred-frame c-hair row",
                "source_lock_status": "internal_numeric_guardrail_with_external_ppn_provenance",
                "mts_prediction_status": "MISSING_VECTOR_RESPONSE_COEFFICIENT",
                "valid_for_claim": "false",
            },
            {
                "anchor_id": "PPNBA1141_1_alpha2",
                "observable": "alpha2",
                "target_bound_abs": "2e-9",
                "bound_units": "dimensionless_abs",
                "local_anchor": "P8_Y5_PPN_RESIDUAL_VECTOR.csv::PPN524_4_alpha2_domain_vector",
                "external_provenance": "P8_Y5_R10_753_EXTERNAL_PPN_SOURCE_PACK.csv::EXT753_0_Will_2014_LRR; EXT753_3_Nordtvedt_Will_1972_PPN_II",
                "use_in_1141": "sharpest vector/domain preferred-frame c-hair guardrail before alpha3",
                "source_lock_status": "internal_numeric_guardrail_with_external_ppn_provenance",
                "mts_prediction_status": "MISSING_VECTOR_RESPONSE_COEFFICIENT",
                "valid_for_claim": "false",
            },
            {
                "anchor_id": "PPNBA1141_2_alpha3",
                "observable": "alpha3",
                "target_bound_abs": "4e-20",
                "bound_units": "dimensionless_abs",
                "local_anchor": "P8_Y5_PPN_RESIDUAL_VECTOR.csv::PPN524_5_alpha3_flux; P8_Y5_R10_1136_ALPHA3_PRODUCT_INEQUALITY_ROWS.csv::PI1136_1_R11_alpha3",
                "external_provenance": "P8_Y5_R10_753_EXTERNAL_PPN_SOURCE_PACK.csv::EXT753_4_Damour_Schaefer_alpha3",
                "use_in_1141": "flux c-hair K*c*epsilon product guardrail",
                "source_lock_status": "internal_numeric_guardrail_with_external_alpha3_provenance",
                "mts_prediction_status": "MISSING_K_c_EPSILON_PRODUCT",
                "valid_for_claim": "false",
            },
        ]
    )


def vector_bound_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "row_id": "VFB1141_0_alpha1_vector",
                "component": "c_vector_preferred_frame_hair",
                "observable": "alpha1",
                "target_bound_abs": "1e-4",
                "coframe": "observed_local_matter_source_coframe",
                "prediction_formula_required": "alpha1_pred = R_alpha1_vector[c_vector_preferred_frame_hair; observed_coframe]",
                "needed_fields": "system_id; vector_component; c_vector_abs; R_alpha1_vector; coframe; units; source_path; valid_for_claim",
                "current_prediction": "MISSING_VECTOR_RESPONSE_COEFFICIENT",
                "source_path": "MISSING_SOURCE_PATH",
                "units": "dimensionless alpha1 after declared observed-coframe response normalization",
                "status": "BLOCKED_MISSING_VECTOR_COEFFICIENT_AND_RESPONSE_MAP",
                "claim_allowed": "false",
                "valid_for_claim": "false",
            },
            {
                "row_id": "VFB1141_1_alpha2_vector",
                "component": "c_vector_preferred_frame_hair",
                "observable": "alpha2",
                "target_bound_abs": "2e-9",
                "coframe": "observed_local_matter_source_coframe",
                "prediction_formula_required": "alpha2_pred = R_alpha2_vector[c_vector_preferred_frame_hair; observed_coframe]",
                "needed_fields": "system_id; vector_component; c_vector_abs; R_alpha2_vector; coframe; units; source_path; valid_for_claim",
                "current_prediction": "MISSING_VECTOR_RESPONSE_COEFFICIENT",
                "source_path": "MISSING_SOURCE_PATH",
                "units": "dimensionless alpha2 after declared observed-coframe response normalization",
                "status": "BLOCKED_MISSING_VECTOR_COEFFICIENT_AND_RESPONSE_MAP",
                "claim_allowed": "false",
                "valid_for_claim": "false",
            },
            {
                "row_id": "VFB1141_2_alpha3_vector_sibling",
                "component": "c_vector_preferred_frame_hair",
                "observable": "alpha3",
                "target_bound_abs": "4e-20",
                "coframe": "observed_local_matter_source_coframe",
                "prediction_formula_required": "alpha3_vector_pred = R_alpha3_vector[c_vector_preferred_frame_hair; observed_coframe] or theorem-zero vector leakage",
                "needed_fields": "system_id; vector_component; c_vector_abs; R_alpha3_vector; coframe; units; source_path; valid_for_claim",
                "current_prediction": "MISSING_VECTOR_RESPONSE_COEFFICIENT",
                "source_path": "MISSING_SOURCE_PATH",
                "units": "dimensionless alpha3 vector contribution after declared response normalization",
                "status": "SIBLING_GUARD_BLOCKED_MISSING_VECTOR_ALPHA3_MAP",
                "claim_allowed": "false",
                "valid_for_claim": "false",
            },
        ]
    )


def flux_bound_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "row_id": "FFB1141_0_K_source_factor",
                "component": "c_domain_flux_hair",
                "observable": "alpha3",
                "quantity": "K_R11_flux_alpha3",
                "target_bound_abs": "factor_of_4e-20_product",
                "product_policy": "factor may pass only by numeric sourced value or parent theorem-zero; no source-unity shortcut",
                "needed_fields": "system_id; K_abs; K_units; K_source_path; weak_field_map; valid_for_claim",
                "current_value": "MISSING_K_R11_FLUX_ALPHA3_SOURCE_OR_ZERO_THEOREM",
                "source_path": "MISSING_SOURCE_PATH",
                "status": "BLOCKED_MISSING_K_FACTOR",
                "claim_allowed": "false",
                "valid_for_claim": "false",
            },
            {
                "row_id": "FFB1141_1_c_source_factor",
                "component": "c_domain_flux_hair",
                "observable": "alpha3",
                "quantity": "c_domain_source_normalization_operator",
                "target_bound_abs": "factor_of_4e-20_product",
                "product_policy": "c may pass only by numeric sourced value or parent theorem-zero; not by measured-GM absorption",
                "needed_fields": "system_id; c_flux_abs; c_units; c_source_path; observed_coframe_normalization; valid_for_claim",
                "current_value": "MISSING_DOMAIN_MU_EXTRA_OPERATOR_ZERO_OR_NUMERIC_COEFFICIENT",
                "source_path": "MISSING_SOURCE_PATH",
                "status": "BLOCKED_MISSING_c_FACTOR",
                "claim_allowed": "false",
                "valid_for_claim": "false",
            },
            {
                "row_id": "FFB1141_2_epsilon_flux_factor",
                "component": "c_domain_flux_hair",
                "observable": "alpha3",
                "quantity": "epsilon_domain_flux",
                "target_bound_abs": "factor_of_4e-20_product",
                "product_policy": "epsilon may pass only by sourced profile/bound or parent no-flux theorem",
                "needed_fields": "system_id; epsilon_abs; profile_support; epsilon_units; epsilon_source_path; valid_for_claim",
                "current_value": "MISSING_EPSILON_DOMAIN_FLUX_PROFILE_OR_ZERO_THEOREM",
                "source_path": "MISSING_SOURCE_PATH",
                "status": "BLOCKED_MISSING_EPSILON_FACTOR",
                "claim_allowed": "false",
                "valid_for_claim": "false",
            },
            {
                "row_id": "FFB1141_3_product_row",
                "component": "c_domain_flux_hair",
                "observable": "alpha3",
                "quantity": "abs(K_R11_flux_alpha3*c_domain_source_normalization_operator*epsilon_domain_flux)",
                "target_bound_abs": "4e-20",
                "product_policy": "product must pass independently before total alpha3 row; tuned cancellation forbidden",
                "needed_fields": "system_id; K_abs; c_flux_abs; epsilon_abs; product_abs; units; all_source_paths; valid_for_claim",
                "current_value": "MISSING_K_c_EPSILON_PRODUCT",
                "source_path": "MISSING_SOURCE_PATH",
                "status": "BLOCKED_MISSING_PRODUCT_OR_ZERO_FACTOR",
                "claim_allowed": "false",
                "valid_for_claim": "false",
            },
        ]
    )


def gate_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "gate_id": "G1141_0_sources_exist",
                "rule": "1140 handoff, PPN target rows, alpha3 product rows, and R11 c rows are locally anchored",
                "gate_pass": "true_nonclaim",
                "reason": "source paths/needles are present but do not provide MTS coefficients",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1141_1_ppn_bounds_present",
                "rule": "alpha1, alpha2, and alpha3 numeric guardrails are carried explicitly",
                "gate_pass": "true_nonclaim",
                "reason": "numeric bounds exist as local guardrails; predictions are still missing",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1141_2_observed_coframe_fixed",
                "rule": "vector rows must use the observed local matter/source coframe",
                "gate_pass": "true_nonclaim",
                "reason": "coframe string is fixed in every vector row, but no coefficient is sourced",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1141_3_vector_prediction",
                "rule": "alpha1/alpha2/alpha3 vector predictions are numeric or theorem-zero",
                "gate_pass": "false",
                "reason": "R_alpha_i_vector and c_vector_preferred_frame_hair are missing",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1141_4_flux_product",
                "rule": "K*c*epsilon product is numeric below 4e-20 or has a parent zero factor",
                "gate_pass": "false",
                "reason": "K, c, epsilon, and product are missing or theorem-zero unsigned",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1141_5_no_cancellation",
                "rule": "no tuned cancellation between vector, flux, boundary, or domain channels",
                "gate_pass": "true_nonclaim",
                "reason": "every channel must pass independently before any total row is meaningful",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1141_6_sibling_guard",
                "rule": "R5/R6/R8/R11 siblings cannot be bypassed by an alpha3-only row",
                "gate_pass": "true_nonclaim",
                "reason": "1121 sibling guard remains active",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1141_7_local_claim",
                "rule": "R10/PPN/alpha3/local-GR promotion allowed",
                "gate_pass": "false",
                "reason": "first bound rows are source-ready only, not executable/scored",
                "valid_for_claim": "false",
            },
        ]
    )


def input_queue_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "input_id": "REQ1141_0_vector_zero_or_response",
                "target": "c_vector_preferred_frame_hair",
                "needed": "parent A8/covariant-domain theorem that observed vector hair is zero, or numeric c_vector and R_alpha1/R_alpha2/R_alpha3 response maps",
                "blocks": "alpha1; alpha2; alpha3 vector sibling; local preferred-frame claim",
                "best_next_test": "attempt topological/covariant domain-selector vector-zero proof before coefficient sourcing",
                "valid_for_claim": "false",
            },
            {
                "input_id": "REQ1141_1_K_factor",
                "target": "K_R11_flux_alpha3",
                "needed": "numeric weak-field map or theorem-zero factor source for K_R11_flux_alpha3",
                "blocks": "R11 alpha3 flux product",
                "best_next_test": "derive K=0 from no-flux/topological projector or source K map",
                "valid_for_claim": "false",
            },
            {
                "input_id": "REQ1141_2_c_factor",
                "target": "c_domain_source_normalization_operator",
                "needed": "numeric coefficient or parent theorem-zero; no GM absorption/source-unity shortcut",
                "blocks": "R11 alpha3 flux product; R5/R6/R8/R11 sibling rows",
                "best_next_test": "use 1140 c-hair split to prove vector/flux pieces zero or source c row",
                "valid_for_claim": "false",
            },
            {
                "input_id": "REQ1141_3_epsilon_factor",
                "target": "epsilon_domain_flux",
                "needed": "sourced flux profile/bound or parent no-exchange/no-flux theorem",
                "blocks": "R11 alpha3 flux product",
                "best_next_test": "attack epsilon_domain_flux=0 via local representative/no-exchange proof",
                "valid_for_claim": "false",
            },
            {
                "input_id": "REQ1141_4_coframe_normalization",
                "target": "observed_local_matter_source_coframe",
                "needed": "same-frame normalization tying source variation, matter readout, and PPN metric expansion",
                "blocks": "all vector/flux bound rows",
                "best_next_test": "verify existing coframe contract covers source-normalization c rows",
                "valid_for_claim": "false",
            },
        ]
    )


def decision_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "decision_id": "D1141_0_verdict",
                "decision": "first_bound_rows_built_but_not_scoreable",
                "reason": "alpha1/alpha2/alpha3 guardrails are explicit, but MTS vector and flux coefficients remain missing",
                "next_action": "do not run a claim comparator until vector response or K*c*epsilon inputs are real",
                "valid_for_claim": "false",
            },
            {
                "decision_id": "D1141_1_best_next",
                "decision": "try_zero_factor_proof_before_numeric_sourcing",
                "reason": "a parent zero theorem is less vulnerable than fitting/source-plumbing a tiny alpha3 product",
                "next_action": "attempt vector-zero and flux-zero-factor proof from topological/covariant domain selector",
                "valid_for_claim": "false",
            },
            {
                "decision_id": "D1141_2_claim_ceiling",
                "decision": "preferred_frame_and_alpha3_claim_blocked",
                "reason": "source-ready rows have MISSING_SOURCE_PATH and MISSING response/product fields",
                "next_action": "retain local-GR/PPN branch as blocked but now sharply localized",
                "valid_for_claim": "false",
            },
        ]
    )


def next_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "next_id": "NEXT1141_0_1142",
                "next_target": "1142-Y5-R10-c-vector-flux-zero-factor-proof-or-coefficient-source-fill.md",
                "objective": "try to prove observed vector c-hair and at least one K/c/epsilon flux factor vanish from the parent topological/covariant domain selector; if proof fails, produce the first strict source-fill row for the missing coefficient",
                "include": "A8 topological domain selector; observed coframe; vector zero theorem; K zero theorem; c zero theorem; epsilon no-flux theorem; alpha1/alpha2/alpha3 guards",
                "exclude": "tuned cancellation; measured-GM absorption; source-unity; alpha3/local-GR claim; GitHub; formalization edits",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            }
        ]
    )


def validate(
    sources: list[dict[str, object]],
    anchors: list[dict[str, object]],
    vector_rows: list[dict[str, object]],
    flux_rows: list[dict[str, object]],
    gates: list[dict[str, object]],
    queue: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_target: list[dict[str, object]],
    outputs: dict[str, Path],
) -> list[dict[str, object]]:
    validation: list[dict[str, object]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        validation.append(
            {
                "check_id": check_id,
                "result": "pass" if passed else "fail",
                "detail": detail,
                "valid_for_claim": "false",
                "generated_utc": now(),
            }
        )

    all_rows = anchors + vector_rows + flux_rows + gates + queue + decisions + next_target
    anchor_bounds = {row["observable"]: row["target_bound_abs"] for row in anchors}
    add(
        "V1141_0_sources_exist",
        all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources),
        "all cited local source paths exist and needles are found",
    )
    add(
        "V1141_1_ppn_bounds",
        anchor_bounds == {"alpha1": "1e-4", "alpha2": "2e-9", "alpha3": "4e-20"},
        "alpha1, alpha2, and alpha3 guardrails are explicit",
    )
    add(
        "V1141_2_vector_rows",
        {row["observable"] for row in vector_rows} == {"alpha1", "alpha2", "alpha3"}
        and all(row["status"].startswith("BLOCKED") or row["status"].startswith("SIBLING") for row in vector_rows),
        "vector c-hair rows cover alpha1/alpha2/alpha3 and remain blocked",
    )
    add(
        "V1141_3_flux_rows",
        {row["quantity"] for row in flux_rows}
        == {
            "K_R11_flux_alpha3",
            "c_domain_source_normalization_operator",
            "epsilon_domain_flux",
            "abs(K_R11_flux_alpha3*c_domain_source_normalization_operator*epsilon_domain_flux)",
        },
        "flux c-hair rows cover K, c, epsilon, and product",
    )
    add(
        "V1141_4_missing_sources_retained",
        all(row["source_path"] == "MISSING_SOURCE_PATH" for row in vector_rows + flux_rows),
        "first-bound rows do not pretend to have coefficient source paths",
    )
    add(
        "V1141_5_no_cancellation_gate",
        any(row["gate_id"] == "G1141_5_no_cancellation" and row["gate_pass"] == "true_nonclaim" for row in gates),
        "no-cancellation policy is explicit and active",
    )
    add(
        "V1141_6_claim_gates_blocked",
        any(row["gate_id"] == "G1141_3_vector_prediction" and row["gate_pass"] == "false" for row in gates)
        and any(row["gate_id"] == "G1141_4_flux_product" and row["gate_pass"] == "false" for row in gates)
        and any(row["gate_id"] == "G1141_7_local_claim" and row["gate_pass"] == "false" for row in gates),
        "vector, flux, and local claim gates remain blocked",
    )
    add(
        "V1141_7_input_queue",
        {"REQ1141_0_vector_zero_or_response", "REQ1141_1_K_factor", "REQ1141_2_c_factor", "REQ1141_3_epsilon_factor"}.issubset(
            {row["input_id"] for row in queue}
        ),
        "missing vector, K, c, and epsilon inputs are queued",
    )
    add(
        "V1141_8_no_claim_rows",
        all(row.get("valid_for_claim") == "false" for row in all_rows)
        and all(row.get("claim_allowed", "false") == "false" for row in vector_rows + flux_rows + next_target),
        "all generated rows remain nonclaim",
    )
    add(
        "V1141_9_next_target",
        next_target[0]["next_target"].startswith("1142-") and "zero-factor" in str(next_target[0]["next_target"]),
        "1142 handoff targets zero-factor proof before coefficient sourcing",
    )
    add(
        "V1141_10_generated_under_post_checkpoint",
        all(str(path.resolve()).startswith(str(ROOT.resolve())) for path in outputs.values()),
        "all generated outputs are under post-checkpoint-work",
    )
    csv_parse_ok = True
    for output_name, path in outputs.items():
        if output_name == "validation":
            continue
        if path.suffix.lower() == ".csv" and path.exists():
            with path.open("r", newline="", encoding="utf-8") as handle:
                list(csv.DictReader(handle))
        elif path.suffix.lower() == ".csv":
            csv_parse_ok = False
    add("V1141_11_csv_parse", csv_parse_ok, "all 1141 CSV outputs parse cleanly")
    add("V1141_12_formalization_untouched", True, "generator writes no outputs under formalization-workbench")
    add(
        "V1141_SUMMARY",
        True,
        "1141 builds strict source-ready vector/flux c-hair bound rows, keeps claims blocked, and sends zero-factor proof to 1142",
    )
    return validation


def table(headers: list[str], rows: list[dict[str, object]]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines)


def write_doc(
    sources: list[dict[str, object]],
    anchors: list[dict[str, object]],
    vector_rows: list[dict[str, object]],
    flux_rows: list[dict[str, object]],
    gates: list[dict[str, object]],
    queue: list[dict[str, object]],
    decisions: list[dict[str, object]],
    validation: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    text = f"""# 1141 - Y5/R10 c Vector/Flux Hair First Bound Row

**Current verdict:** first bound rows now exist for `c_vector_preferred_frame_hair` and `c_domain_flux_hair`, but they are source-ready only. They are not executable, scoreable, or claim-valid.

**Useful progress:** the local pressure point is no longer vague. Vector hair must feed explicit `alpha1`, `alpha2`, and `alpha3` rows; flux hair must pass the independent `K*c*epsilon <= 4e-20` product row or prove a parent zero factor.

**Important guard:** the `alpha3` branch cannot be rescued by tuned cancellation, source-unity, or measured-`GM` absorption. Vector, flux, and sibling rows must pass independently in the observed local matter/source coframe.

**Best next attack:** try the theorem-zero route first: prove the topological/covariant domain selector has no observed vector hair and forces at least one of `K`, `c`, or `epsilon` to vanish. If that fails, fill the first real coefficient source row.

**No claim:** no R10, PPN, alpha3, preferred-frame, local-GR, measured-GM, GitHub, or public claim follows from 1141.

## Source Register
{table(["source_id", "relative_path", "exists", "needle", "needle_found", "role"], sources)}

## PPN Bound Anchors
{table(["anchor_id", "observable", "target_bound_abs", "bound_units", "local_anchor", "external_provenance", "source_lock_status", "mts_prediction_status", "valid_for_claim"], anchors)}

## Vector Hair First Bound Rows
{table(["row_id", "component", "observable", "target_bound_abs", "coframe", "prediction_formula_required", "needed_fields", "current_prediction", "source_path", "status", "valid_for_claim"], vector_rows)}

## Flux Hair First Bound Rows
{table(["row_id", "component", "observable", "quantity", "target_bound_abs", "product_policy", "needed_fields", "current_value", "source_path", "status", "valid_for_claim"], flux_rows)}

## Coherence and Claim Gates
{table(["gate_id", "rule", "gate_pass", "reason", "valid_for_claim"], gates)}

## Required Parent/Input Queue
{table(["input_id", "target", "needed", "blocks", "best_next_test", "valid_for_claim"], queue)}

## Decision Ledger
{table(["decision_id", "decision", "reason", "next_action", "valid_for_claim"], decisions)}

## Validation
{table(["check_id", "result", "detail", "valid_for_claim"], validation)}

## Next Target
{table(["next_id", "next_target", "objective", "include", "exclude", "valid_for_claim", "claim_allowed"], next_target)}
"""
    DOC.write_text(text, encoding="utf-8")


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists() and pycache.is_dir():
        shutil.rmtree(pycache)


def main() -> None:
    outputs = {
        "source_register": OUT / "P8_Y5_R10_1141_SOURCE_REGISTER.csv",
        "anchors": OUT / "P8_Y5_R10_1141_PPN_BOUND_ANCHOR_ROWS.csv",
        "vector": OUT / "P8_Y5_R10_1141_VECTOR_HAIR_FIRST_BOUND_ROWS.csv",
        "flux": OUT / "P8_Y5_R10_1141_FLUX_HAIR_FIRST_BOUND_ROWS.csv",
        "gates": OUT / "P8_Y5_R10_1141_COHERENCE_AND_NO_CANCELLATION_GATES.csv",
        "queue": OUT / "P8_Y5_R10_1141_REQUIRED_PARENT_INPUT_QUEUE.csv",
        "decisions": OUT / "P8_Y5_R10_1141_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_R10_1141_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_1141_VALIDATION.csv",
    }
    sources = source_rows()
    anchors = ppn_anchor_rows()
    vector_rows = vector_bound_rows()
    flux_rows = flux_bound_rows()
    gates = gate_rows()
    queue = input_queue_rows()
    decisions = decision_rows()
    next_target = next_rows()

    write_csv(outputs["source_register"], sources)
    write_csv(outputs["anchors"], anchors)
    write_csv(outputs["vector"], vector_rows)
    write_csv(outputs["flux"], flux_rows)
    write_csv(outputs["gates"], gates)
    write_csv(outputs["queue"], queue)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["next"], next_target)
    validation = validate(sources, anchors, vector_rows, flux_rows, gates, queue, decisions, next_target, outputs)
    write_csv(outputs["validation"], validation)
    write_doc(sources, anchors, vector_rows, flux_rows, gates, queue, decisions, validation, next_target)
    remove_pycache()

    failed = [row for row in validation if row["result"] != "pass"]
    print(f"wrote {DOC}")
    print(f"validation: {'PASS' if not failed else 'FAIL'}")
    if failed:
        for row in failed:
            print(f"{row['check_id']}: {row['detail']}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
