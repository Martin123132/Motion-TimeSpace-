from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"

INPUTS = OUT / "P8_Y5_R2FR_3144_INPUTS.csv"
GRAMMAR = OUT / "P8_Y5_R2FR_3144_NO_CA_GRAMMAR_THEOREM.csv"
GATES = OUT / "P8_Y5_R2FR_3144_GRAMMAR_GATES.csv"
BRANCH = OUT / "P8_Y5_R2FR_3144_DELTAJ_BRANCH_SELECTION.csv"
RESIDUAL = OUT / "P8_Y5_R2FR_3144_SELECTED_DELTAJ_RESIDUAL_ROWS.csv"
DECISION = OUT / "P8_Y5_R2FR_3144_DECISION.csv"
VALIDATION = OUT / "P8_Y5_R2FR_3144_VALIDATION.csv"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def source_path(relative: str) -> str:
    return str((ROOT / relative).resolve())


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def input_rows() -> list[dict[str, str]]:
    now = stamp()
    rows = [
        {
            "source_id": "SRC3144_0_3143_doc",
            "path": source_path("3143-Y5-R2FR-same-current-owner-action-variation-under-AX1090.md"),
            "role": "handoff to no-cA/no-source-prefactor parent grammar or finite delta_J branch",
        },
        {
            "source_id": "SRC3144_1_3143_theorem",
            "path": source_path(
                "source-intake/mts_residuals/P8_Y5_R2FR_3143_SAME_CURRENT_OWNER_THEOREM.csv"
            ),
            "role": "same-current owner conditional theorem",
        },
        {
            "source_id": "SRC3144_2_3143_projection",
            "path": source_path(
                "source-intake/mts_residuals/P8_Y5_R2FR_3143_DELTAJ_PROJECTION_CLASSIFICATION.csv"
            ),
            "role": "delta_J insertion-stage classifier",
        },
        {
            "source_id": "SRC3144_3_3056_doc",
            "path": source_path(
                "3056-Y5-R2FR-typed-no-source-prefactor-grammar-or-epsilon-Wchannel-bound-schema-under-AX1090.md"
            ),
            "role": "typed no-source-prefactor grammar attempt",
        },
        {
            "source_id": "SRC3144_4_2784_doc",
            "path": source_path(
                "2784-Y5-R2FR-parent-action-object-language-measure-current-owner-proof-stack-under-AX1090.md"
            ),
            "role": "object-language/action-measure/current-owner proof stack",
        },
        {
            "source_id": "SRC3144_5_1890_doc",
            "path": source_path(
                "1890-Y5-R2FR-no-source-prefactor-parent-action-clause-or-component-basis-first-source-row.md"
            ),
            "role": "no source-prefactor parent action clause attempt",
        },
        {
            "source_id": "SRC3144_6_3123_doc",
            "path": source_path(
                "3123-Y5-R2FR-current-owner-action-variation-or-deltaJ-projection-exclusion-under-AX1090.md"
            ),
            "role": "current-owner action variation and projection classifier",
        },
        {
            "source_id": "SRC3144_7_PAC990",
            "path": source_path("source-intake/mts_residuals/P8_Y5_R10_990_PARENT_ACTION_CONTRACT.csv"),
            "role": "minimal parent EM/matter coupling contract",
        },
        {
            "source_id": "SRC3144_8_3056_typed_csv",
            "path": source_path(
                "source-intake/mts_residuals/P8_Y5_R2FR_3056_TYPED_NO_SOURCE_PREFACTOR_GRAMMAR_ATTEMPT.csv"
            ),
            "role": "3056 typed grammar rows",
        },
        {
            "source_id": "SRC3144_9_3056_gates",
            "path": source_path("source-intake/mts_residuals/P8_Y5_R2FR_3056_GRAMMAR_GATE_EVALUATION.csv"),
            "role": "3056 grammar gate rows",
        },
        {
            "source_id": "SRC3144_10_2784_counterexamples",
            "path": source_path("source-intake/mts_residuals/P8_Y5_R2FR_2784_COUNTEREXAMPLE_KILL_MATRIX.csv"),
            "role": "surviving object/action/current counterexamples",
        },
    ]
    for row in rows:
        row["exists"] = str(Path(row["path"]).exists()).lower()
        row["valid_for_claim"] = "false"
        row["generated_utc"] = now
    return rows


def grammar_rows() -> list[dict[str, str]]:
    now = stamp()
    return [
        {
            "theorem_id": "NCAG3144_0_allowed_parent_arguments",
            "statement": "Allowed ordinary matter/current terms are functors of q(Phi), Obs_e(Q_obs), A_Q(q), fixed representation labels theta_A,n_A, matter fields, and universal constants.",
            "effect_if_signed": "all source/current normalizations are q-owned or fixed representation data",
            "current_status": "grammar_shape_good_not_parent_signed",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "theorem_id": "NCAG3144_1_forbidden_cA_slot",
            "statement": "A source-only or hidden coefficient c_A(Xhat) A_Q J_A is untypeable unless c_A is fixed representation/current data.",
            "effect_if_signed": "same-current owner theorem fires and delta_J=0 for this slot",
            "current_status": "conditional_not_parent_signed",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "theorem_id": "NCAG3144_2_forbidden_wA_slot",
            "statement": "A source-only pre-action multiplier w_A S_A is untypeable unless it is an owned nongravitational matter parameter or common action scale.",
            "effect_if_signed": "source prefactor and relative species/current weights cannot enter Hilbert/source extraction",
            "current_status": "conditional_not_parent_signed",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "theorem_id": "NCAG3144_3_variation_before_readout",
            "statement": "Hilbert/Noether variation must occur before material, source/test, H/W, weak-field, or post-readout labels are introduced.",
            "effect_if_signed": "post-variation current/source selectors are forbidden",
            "current_status": "conditional_not_parent_signed",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "theorem_id": "NCAG3144_4_no_spurion_return",
            "statement": "No hidden marker, boundary/domain class, readout mask, or radiative threshold may re-enter as a source/current coefficient after quotienting.",
            "effect_if_signed": "readout/effective-action current re-entry is blocked",
            "current_status": "missing_parent_no_spurion_theorem",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "theorem_id": "NCAG3144_5_countermodel",
            "statement": "If the parent admits a hidden/current spurion sigma_J, then c_A(sigma_J)A_QJ_A and w_A(sigma_J)S_A are typeable.",
            "effect_if_signed": "none; this is the surviving finite branch",
            "current_status": "countermodel_survives",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "theorem_id": "NCAG3144_6_verdict",
            "statement": "The no-cA/no-wA grammar theorem has an exact shape but is not parent-signed in current corpus.",
            "effect_if_signed": "delta_J and source-prefactor zero route would reopen",
            "current_status": "not_claim_ready_select_finite_branch",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def gate_rows() -> list[dict[str, str]]:
    now = stamp()
    return [
        {
            "gate_id": "NCAGATE3144_0_parent_type_system",
            "gate": "typed_parent_object_language_signed",
            "status": "fail_for_claim",
            "claim_allowed": "false",
            "reason": "3056 and 2784 keep object-language grammar as contract, not parent theorem",
            "generated_utc": now,
        },
        {
            "gate_id": "NCAGATE3144_1_no_cA",
            "gate": "cA_Xhat_AQJA_slot_forbidden",
            "status": "fail_for_claim",
            "claim_allowed": "false",
            "reason": "hidden/current spurion countermodel remains legal enough to retain",
            "generated_utc": now,
        },
        {
            "gate_id": "NCAGATE3144_2_no_wA",
            "gate": "wA_SA_source_prefactor_forbidden",
            "status": "fail_for_claim",
            "claim_allowed": "false",
            "reason": "1890/2784 keep source-only species action prefactor as unsigned countermodel",
            "generated_utc": now,
        },
        {
            "gate_id": "NCAGATE3144_3_no_spurion",
            "gate": "no_spurion_readout_radiative_return",
            "status": "fail_for_claim",
            "claim_allowed": "false",
            "reason": "no-spurion-return theorem is missing",
            "generated_utc": now,
        },
        {
            "gate_id": "NCAGATE3144_4_zero_route",
            "gate": "deltaJ_zero_from_parent_grammar",
            "status": "not_claim_ready",
            "claim_allowed": "false",
            "reason": "all no-slot grammar gates must pass before delta_J=0 can be promoted",
            "generated_utc": now,
        },
    ]


def branch_rows() -> list[dict[str, str]]:
    now = stamp()
    return [
        {
            "branch_id": "DB3144_0_selected",
            "branch": "before_variation_current_source_insertion",
            "selection_status": "selected_conservative_finite_branch",
            "why_selected": "the exact grammar proof did not sign; a parent-level c_A A_QJ_A or w_A S_A enters before Maxwell/Hilbert variation and projects most broadly",
            "material_coulomb": "yes",
            "source_GM": "yes",
            "WEP": "yes_if_differential",
            "R10": "yes_if_source_test_legs_exist",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "branch_id": "DB3144_1_calibration",
            "branch": "universal_calibrated_current_unit",
            "selection_status": "retained_as_possible_subcase_not_default",
            "why_selected": "allowed only if parent proves common-mode universality before measured-G/GM absorption",
            "material_coulomb": "raw_yes_observable_no",
            "source_GM": "raw_yes_observable_no",
            "WEP": "no_unless_differential",
            "R10": "no_unless_source_test_convention_differs",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "branch_id": "DB3144_2_readout",
            "branch": "post_variation_readout_selector",
            "selection_status": "retained_alternative",
            "why_selected": "would not change Hilbert stress/source GM but can affect measured charge/material/R10 readout",
            "material_coulomb": "maybe",
            "source_GM": "no_for_Hilbert_stress",
            "WEP": "maybe",
            "R10": "maybe",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "branch_id": "DB3144_3_effective",
            "branch": "radiative_or_effective_action_reentry",
            "selection_status": "retained_alternative",
            "why_selected": "requires separate effective-action/readout audit to decide whether it is action-level or readout-only",
            "material_coulomb": "yes_if_action_level",
            "source_GM": "yes_if_stress_changes",
            "WEP": "maybe",
            "R10": "maybe",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def residual_rows() -> list[dict[str, str]]:
    now = stamp()
    return [
        {
            "row_id": "DBR3144_0_deltaJ_before_variation",
            "quantity": "delta_J_before",
            "definition": "hidden source/test current normalization inserted before Maxwell solve and Hilbert variation",
            "branch": "before_variation_current_source_insertion",
            "value_or_status": "MISSING_PARENT_COEFFICIENT_OR_ZERO_GRAMMAR",
            "projection_status": "projects_to_material_Coulomb_source_GM_WEP_R10",
            "required_next_inputs": "coefficient origin; units; source/test legs; tau_WEP/R10; DeltaGM bridge; no-cancellation policy",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "row_id": "DBR3144_1_CJ_smoke_import",
            "quantity": "C_J_TA6V_minus_PtRh10",
            "definition": "3122 one-channel Coulomb material coefficient for selected before-variation branch",
            "branch": "before_variation_current_source_insertion",
            "value_or_status": "-3.979617773650e-03_nonclaim_smoke",
            "projection_status": "material_Coulomb_WEP_smoke_only",
            "required_next_inputs": "replace smoke convention with source-backed material/readout tensor or keep nonclaim",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "row_id": "DBR3144_2_deltaJ_smoke_envelope",
            "quantity": "abs_deltaJ_one_channel_envelope",
            "definition": "3122 eta_bound/abs(Delta C_J) under no-cancellation one-channel smoke assumptions",
            "branch": "before_variation_current_source_insertion",
            "value_or_status": "7.035851579866e-13_nonclaim_smoke",
            "projection_status": "pressure_scale_not_prediction",
            "required_next_inputs": "direct MTS delta_J coefficient or parent zero theorem",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "row_id": "DBR3144_3_DeltaGMJ",
            "quantity": "Delta_GM_J",
            "definition": "source/orbital GM residual induced by before-variation current normalization changing EM stress",
            "branch": "before_variation_current_source_insertion",
            "value_or_status": "MISSING_DELTAJ_TO_SOURCE_GM_KERNEL",
            "projection_status": "source_calibration_orbital_PPN_missing_kernel",
            "required_next_inputs": "EM binding fraction/source body; source worldtube; GM denominator lock; PPN/orbital kernel",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "row_id": "DBR3144_4_beta_source_alpha",
            "quantity": "beta_source_alpha",
            "definition": "WEP/R10 source-test alpha current normalization leg after selected finite branch",
            "branch": "before_variation_current_source_insertion",
            "value_or_status": "MISSING_SOURCE_TEST_CURRENT_LEGS",
            "projection_status": "WEP_R10_missing_tau_and_source_test_maps",
            "required_next_inputs": "beta_source_J; beta_test_J; tau_WEP; tau_R10; material/source maps",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    now = stamp()
    return [
        {
            "decision_id": "NCD3144_0_grammar",
            "decision": "no_cA_no_wA_grammar_not_parent_signed",
            "reason": "3056/2784/1890 provide the correct grammar shape but not the parent type-system/no-spurion/action-measure theorem",
            "effect": "do not promote delta_J=0 from grammar",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "NCD3144_1_branch",
            "decision": "select_before_variation_finite_deltaJ_branch",
            "reason": "it is the conservative action-level branch if c_A A_QJ_A or w_A S_A is legal",
            "effect": "carry delta_J_before into material Coulomb, source GM, WEP, and R10 residual interfaces",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "NCD3144_2_next",
            "decision": "derive_first_deltaJ_before_projection_kernel_or_parent_coefficient",
            "reason": "selected branch now needs either a parent coefficient/source row or a projection kernel into source GM/WEP/R10",
            "effect": "3145 should target DeltaGM_J kernel or source-backed delta_J_before coefficient row",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def validation_rows(
    inputs: list[dict[str, str]],
    grammar: list[dict[str, str]],
    gates: list[dict[str, str]],
    branches: list[dict[str, str]],
    residuals: list[dict[str, str]],
    decisions: list[dict[str, str]],
) -> list[dict[str, str]]:
    now = stamp()
    sources_exist = all(row["exists"] == "true" for row in inputs)
    verdict_nonclaim = any(
        row["theorem_id"] == "NCAG3144_6_verdict"
        and row["current_status"] == "not_claim_ready_select_finite_branch"
        for row in grammar
    )
    gates_block = all(row["claim_allowed"] == "false" for row in gates)
    branch_selected = any(
        row["branch_id"] == "DB3144_0_selected"
        and row["selection_status"] == "selected_conservative_finite_branch"
        for row in branches
    )
    residuals_cover = {"delta_J_before", "Delta_GM_J", "beta_source_alpha"}.issubset(
        {row["quantity"] for row in residuals}
    )
    decisions_nonclaim = all(row["valid_for_claim"] == "false" for row in decisions)
    return [
        {
            "check_id": "V3144_0_sources_exist",
            "status": "pass" if sources_exist else "fail",
            "details": json.dumps({row["source_id"]: row["exists"] for row in inputs}, ensure_ascii=False),
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3144_1_grammar_not_promoted",
            "status": "pass" if verdict_nonclaim else "fail",
            "details": f"grammar_rows={len(grammar)}",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3144_2_gates_block_claims",
            "status": "pass" if gates_block else "fail",
            "details": json.dumps({row["gate_id"]: row["status"] for row in gates}, ensure_ascii=False),
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3144_3_finite_branch_selected",
            "status": "pass" if branch_selected else "fail",
            "details": "before-variation finite branch selected conservatively",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3144_4_residual_rows_cover_selected_branch",
            "status": "pass" if residuals_cover else "fail",
            "details": json.dumps([row["quantity"] for row in residuals], ensure_ascii=False),
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3144_5_no_claim_leak",
            "status": "pass" if gates_block and decisions_nonclaim else "fail",
            "details": "",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def main() -> None:
    inputs = input_rows()
    grammar = grammar_rows()
    gates = gate_rows()
    branches = branch_rows()
    residuals = residual_rows()
    decisions = decision_rows()
    validations = validation_rows(inputs, grammar, gates, branches, residuals, decisions)
    write_csv(INPUTS, inputs)
    write_csv(GRAMMAR, grammar)
    write_csv(GATES, gates)
    write_csv(BRANCH, branches)
    write_csv(RESIDUAL, residuals)
    write_csv(DECISION, decisions)
    write_csv(VALIDATION, validations)


if __name__ == "__main__":
    main()
