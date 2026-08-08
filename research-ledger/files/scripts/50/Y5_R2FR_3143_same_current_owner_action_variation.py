from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"

INPUTS = OUT / "P8_Y5_R2FR_3143_INPUTS.csv"
THEOREM = OUT / "P8_Y5_R2FR_3143_SAME_CURRENT_OWNER_THEOREM.csv"
PROJECTION = OUT / "P8_Y5_R2FR_3143_DELTAJ_PROJECTION_CLASSIFICATION.csv"
RESIDUAL = OUT / "P8_Y5_R2FR_3143_CURRENT_OWNER_ZERO_OR_RESIDUAL_ROWS.csv"
GATE = OUT / "P8_Y5_R2FR_3143_GATE.csv"
DECISION = OUT / "P8_Y5_R2FR_3143_DECISION.csv"
VALIDATION = OUT / "P8_Y5_R2FR_3143_VALIDATION.csv"


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
            "source_id": "SRC3143_0_3142_doc",
            "path": source_path("3142-Y5-R2FR-em-poynting-qbasic-sector-under-AX1090.md"),
            "role": "selects same-current owner or finite alpha product as next target",
        },
        {
            "source_id": "SRC3143_1_3142_residual",
            "path": source_path(
                "source-intake/mts_residuals/P8_Y5_R2FR_3142_EM_ZERO_OR_RESIDUAL_ROW.csv"
            ),
            "role": "beta_source_alpha and EM current residual rows",
        },
        {
            "source_id": "SRC3143_2_3119_doc",
            "path": source_path(
                "3119-Y5-R2FR-same-current-owner-or-deltaJ-source-test-residual-priority-under-AX1090.md"
            ),
            "role": "same-current owner theorem attempt",
        },
        {
            "source_id": "SRC3143_3_3120_doc",
            "path": source_path(
                "3120-Y5-R2FR-deltaJ-product-bound-runner-or-current-owner-source-intake-under-AX1090.md"
            ),
            "role": "delta_J product-bound runner and finite branch",
        },
        {
            "source_id": "SRC3143_4_3122_doc",
            "path": source_path(
                "3122-Y5-R2FR-current-owner-descent-or-CJ-source-coefficient-fill-under-AX1090.md"
            ),
            "role": "first C_J finite material coefficient and smoke envelope",
        },
        {
            "source_id": "SRC3143_5_3123_doc",
            "path": source_path(
                "3123-Y5-R2FR-current-owner-action-variation-or-deltaJ-projection-exclusion-under-AX1090.md"
            ),
            "role": "action-variation same-current proof route and projection classifier",
        },
        {
            "source_id": "SRC3143_6_1100_TQ",
            "path": source_path(
                "1100-Y5-R10-parent-TQ-owner-fixed-charge-lattice-and-gauge-norm-signature.md"
            ),
            "role": "T_Q and same-current owner gaps",
        },
        {
            "source_id": "SRC3143_7_PAC990",
            "path": source_path("source-intake/mts_residuals/P8_Y5_R10_990_PARENT_ACTION_CONTRACT.csv"),
            "role": "parent EM/matter/GR coupling contract",
        },
        {
            "source_id": "SRC3143_8_EMLOCK988",
            "path": source_path("source-intake/mts_residuals/P8_Y5_R10_988_EM_LOCK_THEOREM_GATE.csv"),
            "role": "EM lock gate",
        },
        {
            "source_id": "SRC3143_9_ELA989",
            "path": source_path("source-intake/mts_residuals/P8_Y5_R10_989_EM_LOCK_SIGNATURE_AUDIT.csv"),
            "role": "EM lock signature/current owner audit",
        },
        {
            "source_id": "SRC3143_10_1890_source_prefactor",
            "path": source_path(
                "1890-Y5-R2FR-no-source-prefactor-parent-action-clause-or-component-basis-first-source-row.md"
            ),
            "role": "no source-prefactor/no double-counting matter-normalization clause",
        },
    ]
    for row in rows:
        row["exists"] = str(Path(row["path"]).exists()).lower()
        row["valid_for_claim"] = "false"
        row["generated_utc"] = now
    return rows


def theorem_rows() -> list[dict[str, str]]:
    now = stamp()
    return [
        {
            "theorem_id": "SCOT3143_0_current_definition",
            "statement": "Define the visible EM current by variation before readout: J_Q^mu=(1/mu_obs) delta S_matter/delta A_Q_mu.",
            "proof_or_status": "definition of Hilbert/Noether current owner for the visible connection",
            "current_status": "definition_exact_if_parent_action_owns_AQ",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "theorem_id": "SCOT3143_1_qbasic_matter_current",
            "statement": "If S_matter=Sbar_matter[q(Phi),Psi,A_Q(q),n_A,theta_A] and Dq[v]=0, then Lie_v S_matter=0 and Lie_v A_Q=0.",
            "proof_or_status": "chain rule over q plus fixed representation labels",
            "current_status": "conditional_theorem",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "theorem_id": "SCOT3143_2_action_variation",
            "statement": "If current extraction commutes with vertical variation, Lie_v J_Q^mu=(1/mu_obs) delta(Lie_v S_matter)/delta A_Q_mu plus zero readout terms.",
            "proof_or_status": "functional derivative of the same q-basic matter action; requires variation-before-readout and no effective re-entry",
            "current_status": "conditional_theorem",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "theorem_id": "SCOT3143_3_same_current_owner",
            "statement": "If no c_A(Xhat), q_A(Xhat), w_A, kappa_A, post-variation selector, or radiative current re-entry exists, then Lie_v J_Q^mu=0.",
            "proof_or_status": "all current factors are q-owned or fixed representation data, so no vertical derivative remains",
            "current_status": "exact_conditional_same_current_owner",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "theorem_id": "SCOT3143_4_deltaJ_zero",
            "statement": "Under SCOT3143_0 through SCOT3143_3, delta_J=0, beta_source_alpha=0 for this channel, Delta_T_EM^J=0, and Delta(GM)_J=0.",
            "proof_or_status": "same-current owner kills hidden source/test current normalization before Maxwell solve and Hilbert stress variation",
            "current_status": "conditional_zero_theorem",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "theorem_id": "SCOT3143_5_Ward_limit",
            "statement": "Ward conservation alone gives nabla_mu J_Q^mu=0 but does not prove Lie_v J_Q^mu=0 or unique normalization.",
            "proof_or_status": "conserved weighted currents can survive if c_A or w_A slots are allowed",
            "current_status": "guard_exact",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "theorem_id": "SCOT3143_6_verdict",
            "statement": "The same-current owner has a functional-derivative proof route, but the parent no-c_A/no-w_A/no-readout-reentry grammar is not fully signed.",
            "proof_or_status": "3123/1100/1890 keep current owner and source-prefactor clauses unsigned",
            "current_status": "not_claim_ready",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def projection_rows() -> list[dict[str, str]]:
    now = stamp()
    return [
        {
            "projection_id": "SCP3143_0_qbasic_forbidden",
            "insertion_stage": "q-basic/forbidden",
            "material_coulomb": "no",
            "source_GM": "no",
            "WEP": "no",
            "R10": "no",
            "classification": "ZERO_BY_ACTION_VARIATION",
            "reason": "same-current owner gives Lie_v J_Q=0 before readout",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "projection_id": "SCP3143_1_before_variation",
            "insertion_stage": "before Maxwell solve / before Hilbert variation",
            "material_coulomb": "yes",
            "source_GM": "yes",
            "WEP": "yes if differential",
            "R10": "yes if finite range/source-test legs exist",
            "classification": "FINITE_BEFORE_VARIATION_PROJECTS_BOTH",
            "reason": "F[J] and T_EM[J] change before source/stress extraction",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "projection_id": "SCP3143_2_calibration_only",
            "insertion_stage": "universal calibrated current unit",
            "material_coulomb": "raw yes observable no",
            "source_GM": "raw yes observable no",
            "WEP": "no unless differential/source-time dependent",
            "R10": "no unless source/test convention differs",
            "classification": "FINITE_CALIBRATION_ONLY",
            "reason": "common unit can be absorbed only after uniqueness/common-mode guard",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "projection_id": "SCP3143_3_post_readout",
            "insertion_stage": "post-variation readout selector",
            "material_coulomb": "maybe",
            "source_GM": "no for Hilbert stress",
            "WEP": "maybe",
            "R10": "maybe",
            "classification": "FINITE_READOUT_ONLY_NO_GM",
            "reason": "measured charge/readout changes but parent Hilbert stress does not",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "projection_id": "SCP3143_4_effective_action",
            "insertion_stage": "radiative/source threshold",
            "material_coulomb": "yes if effective action before variation",
            "source_GM": "yes if stress changes",
            "WEP": "maybe",
            "R10": "maybe",
            "classification": "FINITE_EFFECTIVE_ACTION_AMBIGUOUS",
            "reason": "depends on whether threshold re-enters action or only readout",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def residual_rows() -> list[dict[str, str]]:
    now = stamp()
    return [
        {
            "row_id": "SCR3143_0_theorem_zero_candidate",
            "quantity": "delta_J",
            "definition": "Lie_v ln c_A or hidden source/test current normalization derivative",
            "value_or_status": "0_if_SCOT3143_parent_clauses_signed_else_MISSING",
            "projection": "all EM/source current channels",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "source_path": source_path("source-intake/mts_residuals/P8_Y5_R2FR_3143_SAME_CURRENT_OWNER_THEOREM.csv"),
            "generated_utc": now,
        },
        {
            "row_id": "SCR3143_1_CJ_material_smoke",
            "quantity": "C_J_TA6V_minus_PtRh10",
            "definition": "one-channel Coulomb/material current-normalization coefficient from 3122 smoke convention",
            "value_or_status": "-3.979617773650e-03_nonclaim_smoke",
            "projection": "MICROSCOPE-like TA6V-PtRh10 Coulomb material response",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "source_path": source_path("3122-Y5-R2FR-current-owner-descent-or-CJ-source-coefficient-fill-under-AX1090.md"),
            "generated_utc": now,
        },
        {
            "row_id": "SCR3143_2_deltaJ_smoke_envelope",
            "quantity": "abs(delta_J)_one_channel_envelope",
            "definition": "eta_bound/abs(Delta C_J) under 3122 no-cancellation smoke assumptions",
            "value_or_status": "7.035851579866e-13_nonclaim_smoke",
            "projection": "WEP one-channel smoke bound only, not MTS prediction",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "source_path": source_path("3122-Y5-R2FR-current-owner-descent-or-CJ-source-coefficient-fill-under-AX1090.md"),
            "generated_utc": now,
        },
        {
            "row_id": "SCR3143_3_source_GM_residual",
            "quantity": "Delta_GM_J",
            "definition": "source-mass/orbital GM residual from current normalization changing EM stress before Hilbert variation",
            "value_or_status": "MISSING_DELTAJ_TO_SOURCE_GM_PROJECTION",
            "projection": "source calibration, orbital, PPN",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "source_path": source_path("3123-Y5-R2FR-current-owner-action-variation-or-deltaJ-projection-exclusion-under-AX1090.md"),
            "generated_utc": now,
        },
        {
            "row_id": "SCR3143_4_beta_source_alpha",
            "quantity": "beta_source_alpha",
            "definition": "source/test alpha-current normalization residual if same-current owner is unsigned",
            "value_or_status": "MISSING_SAME_CURRENT_OWNER_OR_ARENA_PROJECTION",
            "projection": "WEP/R10 alpha source-test legs",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "source_path": source_path("source-intake/mts_residuals/P8_Y5_R2FR_3142_EM_ZERO_OR_RESIDUAL_ROW.csv"),
            "generated_utc": now,
        },
    ]


def gate_rows() -> list[dict[str, str]]:
    now = stamp()
    return [
        {
            "gate_id": "SCG3143_0_action_variation",
            "gate": "same_current_owner_from_action_variation",
            "status": "pass_conditional_theorem",
            "claim_allowed": "false",
            "reason": "functional derivative of a q-basic matter action proves Lie_v J_Q=0 if no forbidden current slots exist",
            "generated_utc": now,
        },
        {
            "gate_id": "SCG3143_1_parent_grammar",
            "gate": "no_cA_qA_wA_kappaA_readout_reentry_parent_signed",
            "status": "fail_for_claim",
            "claim_allowed": "false",
            "reason": "current corpus does not fully forbid hidden current/source prefactor slots",
            "generated_utc": now,
        },
        {
            "gate_id": "SCG3143_2_deltaJ_zero",
            "gate": "deltaJ_beta_source_alpha_zero",
            "status": "not_claim_ready",
            "claim_allowed": "false",
            "reason": "zero theorem conditional and finite projection rows are nonclaim",
            "generated_utc": now,
        },
        {
            "gate_id": "SCG3143_3_finite_branch",
            "gate": "finite_deltaJ_product_prediction",
            "status": "not_claim_ready",
            "claim_allowed": "false",
            "reason": "3122 smoke envelope is not a direct MTS prediction; source-GM/R10/tau projections missing",
            "generated_utc": now,
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    now = stamp()
    return [
        {
            "decision_id": "SCD3143_0_theorem",
            "decision": "same_current_owner_has_exact_action_variation_route",
            "reason": "J_Q defined as delta S_matter/delta A_Q carries no independent normalization if S_matter is q-basic and labels are fixed",
            "effect": "Ward conservation is demoted to support; current normalization ownership comes from variation-before-readout",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "SCD3143_1_claim",
            "decision": "do_not_claim_deltaJ_zero",
            "reason": "no-c_A/no-w_A/no-post-readout/radiative closure clauses remain unsigned",
            "effect": "retain delta_J, C_J, Delta_GM_J, and beta_source_alpha residuals",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "SCD3143_2_next",
            "decision": "target_no_cA_slot_parent_grammar_or_select_finite_branch",
            "reason": "the exact remaining proof burden is whether c_A(Xhat)A_QJ_A and w_A S_A are untypeable in the parent action",
            "effect": "3144 should try no-c_A/no-source-prefactor grammar; if it fails choose before-variation/readout/calibration/effective finite branch",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def validation_rows(
    inputs: list[dict[str, str]],
    theorem: list[dict[str, str]],
    projection: list[dict[str, str]],
    residual: list[dict[str, str]],
    gates: list[dict[str, str]],
    decisions: list[dict[str, str]],
) -> list[dict[str, str]]:
    now = stamp()
    sources_exist = all(row["exists"] == "true" for row in inputs)
    conditional_owner = any(
        row["theorem_id"] == "SCOT3143_3_same_current_owner"
        and row["current_status"] == "exact_conditional_same_current_owner"
        for row in theorem
    )
    ward_guard = any(row["theorem_id"] == "SCOT3143_5_Ward_limit" for row in theorem)
    projection_complete = {
        "ZERO_BY_ACTION_VARIATION",
        "FINITE_BEFORE_VARIATION_PROJECTS_BOTH",
        "FINITE_CALIBRATION_ONLY",
        "FINITE_READOUT_ONLY_NO_GM",
        "FINITE_EFFECTIVE_ACTION_AMBIGUOUS",
    }.issubset({row["classification"] for row in projection})
    residuals_retained = {"delta_J", "C_J_TA6V_minus_PtRh10", "Delta_GM_J", "beta_source_alpha"}.issubset(
        {row["quantity"] for row in residual}
    )
    gates_block = all(row["claim_allowed"] == "false" for row in gates)
    decisions_nonclaim = all(row["valid_for_claim"] == "false" for row in decisions)
    return [
        {
            "check_id": "V3143_0_sources_exist",
            "status": "pass" if sources_exist else "fail",
            "details": json.dumps({row["source_id"]: row["exists"] for row in inputs}, ensure_ascii=False),
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3143_1_same_current_conditional_theorem",
            "status": "pass" if conditional_owner else "fail",
            "details": f"theorem_rows={len(theorem)}",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3143_2_ward_guard_retained",
            "status": "pass" if ward_guard else "fail",
            "details": "Ward conservation not used as normalization proof",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3143_3_projection_classifier_complete",
            "status": "pass" if projection_complete else "fail",
            "details": json.dumps([row["classification"] for row in projection], ensure_ascii=False),
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3143_4_residual_rows_retained",
            "status": "pass" if residuals_retained else "fail",
            "details": json.dumps([row["quantity"] for row in residual], ensure_ascii=False),
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3143_5_no_claim_leak",
            "status": "pass" if gates_block and decisions_nonclaim else "fail",
            "details": "",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def main() -> None:
    inputs = input_rows()
    theorem = theorem_rows()
    projection = projection_rows()
    residual = residual_rows()
    gates = gate_rows()
    decisions = decision_rows()
    validations = validation_rows(inputs, theorem, projection, residual, gates, decisions)
    write_csv(INPUTS, inputs)
    write_csv(THEOREM, theorem)
    write_csv(PROJECTION, projection)
    write_csv(RESIDUAL, residual)
    write_csv(GATE, gates)
    write_csv(DECISION, decisions)
    write_csv(VALIDATION, validations)


if __name__ == "__main__":
    main()
