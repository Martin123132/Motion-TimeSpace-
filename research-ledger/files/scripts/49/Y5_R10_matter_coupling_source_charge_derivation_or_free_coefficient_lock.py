from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


STATUS = "Y5_R10_matter_coupling_source_charge_law_derived_shape_free_coefficient_locked_nonclaim"
CLAIM_CEILING = "source_charge_law_shape_and_free_coefficient_lock_only_no_b_zero_no_R10_WEP_PPN_Gdot_R11_or_local_GR_claim"
NEXT_TARGET = "717-Y5-R10-observed-frame-lock-and-frame-transfer-coefficient-pack.md"

ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / "716-Y5-R10-matter-coupling-source-charge-derivation-or-free-coefficient-lock.md"
FORMALIZATION_WORKBENCH = ROOT.parent / "formalization-workbench"
FORMALIZATION_CUTOFF = datetime.fromisoformat("2026-05-31T14:42:00")

OUTPUT_PATHS = [
    DOC_PATH,
    RESIDUALS / "P8_Y5_R10_716_SOURCE_REGISTER.csv",
    RESIDUALS / "P8_Y5_R10_716_MATTER_COUPLING_DERIVATION.csv",
    RESIDUALS / "P8_Y5_R10_716_SOURCE_CHARGE_BRANCH_LOCK.csv",
    RESIDUALS / "P8_Y5_R10_716_FREE_COEFFICIENT_TEMPLATE.csv",
    RESIDUALS / "P8_Y5_R10_716_FRAME_TRANSFER_MAP.csv",
    RESIDUALS / "P8_Y5_R10_716_OBSERVABLE_ACTIVATION_MATRIX.csv",
    RESIDUALS / "P8_Y5_R10_716_ZERO_THEOREM_REQUIREMENTS.csv",
    RESIDUALS / "P8_Y5_R10_716_AEH_SCALAR_UPDATE.csv",
    RESIDUALS / "P8_Y5_R10_716_CLAIM_GATE_EVALUATION.csv",
    RESIDUALS / "P8_Y5_R10_716_DECISION.csv",
    RESIDUALS / "P8_Y5_R10_716_NONCLAIM_SUMMARY.csv",
    RESIDUALS / "P8_Y5_BRR545_716_VALIDATION.csv",
]

SOURCE_PATHS = {
    "715_doc": ROOT / "715-Y5-R10-retained-scalar-source-row-minimum-executable-coefficient-pack.md",
    "715_validation": RESIDUALS / "P8_Y5_BRR545_715_VALIDATION.csv",
    "715_pack": RESIDUALS / "P8_Y5_R10_715_MINIMUM_EXECUTABLE_COEFFICIENT_PACK.csv",
    "715_coupling": RESIDUALS / "P8_Y5_R10_715_COUPLING_BOTTLENECK_AUDIT.csv",
    "715_observable": RESIDUALS / "P8_Y5_R10_715_RETAINED_SCALAR_OBSERVABLE_MAP.csv",
    "708_contract": RESIDUALS / "P8_Y5_R10_708_SCALAR_CLASS_SOURCE_ROW_CONTRACT.csv",
    "708_local_map": RESIDUALS / "P8_Y5_R10_708_LOCAL_EXPANSION_MAP.csv",
    "708_ppn_map": RESIDUALS / "P8_Y5_R10_708_PPN_GDOT_WEP_MAP.csv",
    "710_descent": RESIDUALS / "P8_Y5_R10_710_DESCENT_PARENT_ACTION_CLAUSE.csv",
    "711_qda": RESIDUALS / "P8_Y5_R10_711_QUOTIENT_DESCENT_DERIVATION_AUDIT.csv",
    "711_owner": RESIDUALS / "P8_Y5_R10_711_DPC710_OWNERSHIP_MAP.csv",
    "410_doc": ROOT / "410-quotient-matter-functor-theorem-attempt.md",
    "626_doc": ROOT / "626-Y5-R10-quotient-invariant-matter-action-signature-or-cg-bound-input.md",
    "712_rules": RESIDUALS / "P8_Y5_R10_712_FORBIDDEN_PROMOTION_RULES.csv",
    "713_baselines": RESIDUALS / "P8_Y5_R10_713_LOCAL_BOUND_BASELINES.csv",
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
        "715_doc": "previous retained scalar coefficient pack",
        "715_validation": "previous validation gate",
        "715_pack": "minimum coefficient pack containing b_A,I and frame transfer",
        "715_coupling": "coupling bottleneck audit",
        "715_observable": "observable activation map",
        "708_contract": "scalar source-row contract",
        "708_local_map": "symbolic local scalar map",
        "708_ppn_map": "WEP/PPN/Gdot/R10 map",
        "710_descent": "candidate matter-blind clause",
        "711_qda": "quotient descent audit showing matter functor failure",
        "711_owner": "DPC710 ownership map showing matter blindness not parent-owned",
        "410_doc": "quotient matter functor theorem attempt",
        "626_doc": "quotient-invariant matter action signature attempt",
        "712_rules": "forbidden closure promotion rules",
        "713_baselines": "local baseline rows",
    }
    return [
        {
            "source_id": source_id,
            "path": str(path),
            "exists": str(path.exists()).lower(),
            "role": roles[source_id],
            "generated_utc": generated,
        }
        for source_id, path in SOURCE_PATHS.items()
    ]


def matter_functor_failed() -> bool:
    qda_rows = read_csv(SOURCE_PATHS["711_qda"])
    owner_rows = read_csv(SOURCE_PATHS["711_owner"])
    qda_fail = any(
        row.get("audit_id") == "QDA711_4_matter_functor_factorization"
        and row.get("current_status") == "fail_current_corpus"
        for row in qda_rows
    )
    owner_fail = any(
        row.get("dpc710_clause") == "DPC710_3_matter_functor_blind"
        and row.get("current_status") == "fail_current_corpus"
        for row in owner_rows
    )
    return qda_fail and owner_fail


def derivation_rows() -> list[dict[str, str]]:
    generated = now()
    rows = [
        (
            "MCD716_0_matter_metric",
            "retained matter frame",
            "g_A,mu nu = B_A^2(u) g_obs,mu nu, with optional direct constants theta_A(u)",
            "definition_from_retained_action",
            "sets the object whose u-variation defines source charge",
        ),
        (
            "MCD716_1_variation",
            "matter variation with respect to u^I",
            "delta_u S_A = integral sqrt(-g_obs) J_A,I delta u^I; J_A,I contains T_A partial_I ln B_A plus direct partial_I theta_A terms",
            "derived_shape",
            "stress trace/direct mass terms are the source of scalar charge",
        ),
        (
            "MCD716_2_charge_definition",
            "species/source charge",
            "b_A,I := partial_I ln m_A^obs(u)|u0 = partial_I ln B_A|u0 + direct_mass_or_constant_charge_A,I",
            "derived_definition",
            "this is the retained coefficient that must be zero, universal, or sourced",
        ),
        (
            "MCD716_3_frame_transfer",
            "observed-to-EH frame transfer",
            "q_A,I = b_A,I + f_frame a_I, where a_I=partial_I ln A_EH|u0 and f_frame is fixed only after the observed/EH/matter frame convention is chosen",
            "derived_shape_frame_dependent",
            "apparent b_A,I=0 is not enough if f_frame a_I survives",
        ),
        (
            "MCD716_4_canonical_charge",
            "canonical scalar mode charge",
            "Q_Aa = N_frame E_a^I q_A,I = N_frame E_a^I (b_A,I + f_frame a_I)",
            "derived_shape",
            "feeds WEP, R10, PPN, clocks, and Gdot after modes are sourced",
        ),
        (
            "MCD716_5_zero_condition",
            "exact algebraic zero condition",
            "Q_Aa=0 for all sources/tests A and modes a iff E_a^I(b_A,I+f_frame a_I)=0 for all A,a, or the mode is absent by a signed no-mode theorem",
            "conditional_zero_condition",
            "zero is a theorem only if matter blindness/same-frame/no-mode owners are signed",
        ),
        (
            "MCD716_6_current_corpus_verdict",
            "derivation verdict",
            "matter functor factorization and same-frame matter blindness are not parent-owned in the current corpus",
            "zero_not_derived",
            "lock retained b_A,I/f_frame as free symbolic coefficients until sourced or theorem-zero",
        ),
    ]
    return [
        {
            "derivation_id": derivation_id,
            "object": obj,
            "statement": statement,
            "derivation_status": status,
            "claim_effect": effect,
            "valid_for_claim": "false",
            "source_paths": source_list("708_contract", "708_local_map", "710_descent", "711_qda", "711_owner", "410_doc", "626_doc"),
            "generated_utc": generated,
        }
        for derivation_id, obj, statement, status, effect in rows
    ]


def branch_lock_rows() -> list[dict[str, str]]:
    generated = now()
    rows = [
        (
            "SCL716_0_parent_zero",
            "parent-signed zero charge",
            "b_A,I=0 and f_frame a_I=0, or no canonical scalar mode",
            "not_available",
            "would suppress scalar WEP/R10 only if signed by matter functor, same-frame, and no-mode owners",
            "derive theorem; do not assume",
        ),
        (
            "SCL716_1_universal_nonzero",
            "universal nonzero charge",
            "Q_Aa=Q_a independent of species A",
            "free_subbranch_allowed_nonclaim",
            "WEP protected at leading composition level, but R10/PPN/Gdot remain active",
            "source Q_a and score later",
        ),
        (
            "SCL716_2_species_nonzero",
            "species-dependent charge",
            "Q_Aa differs across A",
            "free_subbranch_allowed_nonclaim",
            "WEP and R10 activate immediately",
            "source material charges or bound free coefficients",
        ),
        (
            "SCL716_3_frame_induced",
            "frame-induced charge",
            "b_A,I=0 but f_frame a_I != 0",
            "free_subbranch_allowed_nonclaim",
            "same-frame failure can resurrect coupling",
            "fix frame transfer in 717",
        ),
        (
            "SCL716_4_current_lock",
            "retained free coefficient lock",
            "b_A,I and f_frame remain explicit free symbolic coefficients",
            "selected_current_route",
            "prevents closure-zero laundering",
            NEXT_TARGET,
        ),
    ]
    return [
        {
            "branch_id": branch_id,
            "branch": branch,
            "charge_condition": condition,
            "current_status": status,
            "observable_effect": effect,
            "next_action": next_action,
            "valid_for_claim": "false",
            "source_paths": source_list("715_coupling", "711_qda", "711_owner", "712_rules"),
            "generated_utc": generated,
        }
        for branch_id, branch, condition, status, effect, next_action in rows
    ]


def free_template_rows() -> list[dict[str, str]]:
    generated = now()
    rows = [
        (
            "FCT716_0_source_A_mode_a",
            "A",
            "mode_a",
            "b_A,I",
            "FREE_SYMBOLIC_B_A_I_UNTIL_DERIVED_OR_SOURCED",
            "f_frame",
            "FREE_SYMBOLIC_FRAME_TRANSFER_UNTIL_717",
            "q_A,I=b_A,I+f_frame*a_I",
            "Q_Aa=N_frame*E_a^I*q_A,I",
            "retained_free_coefficient_nonclaim",
        ),
        (
            "FCT716_1_source_B_mode_a",
            "B",
            "mode_a",
            "b_B,I",
            "FREE_SYMBOLIC_B_B_I_UNTIL_DERIVED_OR_SOURCED",
            "f_frame",
            "FREE_SYMBOLIC_FRAME_TRANSFER_UNTIL_717",
            "q_B,I=b_B,I+f_frame*a_I",
            "Q_Ba=N_frame*E_a^I*q_B,I",
            "retained_free_coefficient_nonclaim",
        ),
        (
            "FCT716_2_alpha_pair",
            "A_B_pair",
            "mode_a",
            "b_A,I;b_B,I",
            "FREE_SYMBOLIC_PAIR_CHARGES",
            "f_frame",
            "FREE_SYMBOLIC_FRAME_TRANSFER_UNTIL_717",
            "q_A,I and q_B,I",
            "alpha_AB,a=Q_Aa*Q_Ba",
            "retained_free_coefficient_nonclaim",
        ),
    ]
    return [
        {
            "template_id": template_id,
            "source_or_test_label": label,
            "mode_label": mode,
            "raw_charge_symbol": raw_symbol,
            "raw_charge_status": raw_status,
            "frame_transfer_symbol": frame_symbol,
            "frame_transfer_status": frame_status,
            "effective_field_charge": field_charge,
            "canonical_charge_or_alpha": canonical,
            "derivation_status": status,
            "valid_for_claim": "false",
            "source_paths": source_list("715_pack", "715_observable", "708_ppn_map"),
            "generated_utc": generated,
        }
        for template_id, label, mode, raw_symbol, raw_status, frame_symbol, frame_status, field_charge, canonical, status in rows
    ]


def frame_transfer_rows() -> list[dict[str, str]]:
    generated = now()
    rows = [
        (
            "FTM716_0_same_observed_frame",
            "g_matter=g_obs and EH term already in observed frame",
            "f_frame=0",
            "requires DPC710_6 same-frame identity or explicit action convention",
            "not_derived_current_corpus",
        ),
        (
            "FTM716_1_Einstein_transform",
            "g_E=A_EH(u) g_obs, matter metric rewritten in Einstein frame",
            "f_frame=-1/2 in the common conformal convention",
            "requires explicit choice of Einstein-frame normalization and signs",
            "not_selected_current_corpus",
        ),
        (
            "FTM716_2_general_disformal",
            "matter/readout metric includes Weyl/disformal representative factor",
            "f_frame plus disformal coefficients retained",
            "requires representative-coupling exclusion or bound rows",
            "blocked_for_claim",
        ),
        (
            "FTM716_3_current_policy",
            "frame not locked",
            "retain f_frame symbolically",
            "no scoring until 717 fixes or bounds frame transfer",
            "selected_current_route",
        ),
    ]
    return [
        {
            "frame_id": frame_id,
            "frame_branch": branch,
            "frame_transfer_value": value,
            "requirement": requirement,
            "current_status": status,
            "valid_for_claim": "false",
            "source_paths": source_list("715_pack", "710_descent", "711_owner", "626_doc"),
            "generated_utc": generated,
        }
        for frame_id, branch, value, requirement, status in rows
    ]


def observable_activation_rows() -> list[dict[str, str]]:
    generated = now()
    rows = [
        (
            "OAM716_0_Newton",
            "Newtonian limit",
            "Q_Aa Q_Ba modifies G_eff_AB(r) unless absorbed as a constant measured-G calibration",
            "active_if_Q_nonzero_or_A0_unfixed",
            "needs frame lock, A0, charges, ranges",
        ),
        (
            "OAM716_1_WEP",
            "R1_WEP_source_charge",
            "species dependence in Q_Aa creates composition-dependent acceleration",
            "active_if_Q_Aa_not_universal",
            "needs material/source charge map",
        ),
        (
            "OAM716_2_clock",
            "R2_clock_redshift",
            "clock/readout charge can differ from bulk matter charge",
            "active_if_clock_charge_or_frame_transfer_nonzero",
            "needs clock readout map",
        ),
        (
            "OAM716_3_gamma",
            "R3_gamma",
            "universal scalar charge shifts light/curvature PPN response",
            "active_if_long_range_universal_Q_nonzero",
            "needs canonical charge and PPN convention",
        ),
        (
            "OAM716_4_beta",
            "R4_beta",
            "field derivative of charge/prefactor sources nonlinear PPN response",
            "active_if_Q_or_derivative_Q_nonzero",
            "needs a_IJ and derivative charge map",
        ),
        (
            "OAM716_5_Gdot",
            "R9_Gdot",
            "time drift of A0 or matter charge changes measured G/M",
            "active_if_partial_t_u0_or_source_drift_nonzero",
            "needs time-profile/calibration map",
        ),
        (
            "OAM716_6_R10",
            "R10_fifth_force",
            "finite range mode with Q_Aa Q_Ba creates alpha(lambda)",
            "active_if_Q_nonzero_and_lambda_in_test_range",
            "needs real alpha_bound(lambda)",
        ),
        (
            "OAM716_7_R11",
            "R11_EH_operator_ledger",
            "retained scalar action is an operator family until zero/bounds are proven",
            "active_until_coefficient_vector_or_EH_only_theorem",
            "needs executable R11 scalar row",
        ),
    ]
    return [
        {
            "activation_id": activation_id,
            "arena": arena,
            "activation_rule": rule,
            "current_status": status,
            "minimum_next_input": next_input,
            "valid_for_claim": "false",
            "source_paths": source_list("715_observable", "713_baselines", "708_ppn_map"),
            "generated_utc": generated,
        }
        for activation_id, arena, rule, status, next_input in rows
    ]


def zero_requirements_rows() -> list[dict[str, str]]:
    generated = now()
    rows = [
        (
            "ZTR716_0_matter_functor",
            "matter factors only through observed quotient geometry",
            "QDA711_4/DPC710_3 must be parent-signed",
            "fail_current_corpus",
        ),
        (
            "ZTR716_1_constant_sector",
            "species constants carry no scalar/class charge",
            "partial_I theta_A=0 and partial_I m_A^bare=0 for all A",
            "not_derived",
        ),
        (
            "ZTR716_2_same_frame",
            "no frame-transfer charge",
            "f_frame=0 or a_I=0 in the scored frame",
            "not_derived",
        ),
        (
            "ZTR716_3_no_mode",
            "canonical scalar mode absent or pure gauge/topological",
            "Z/M/action owner proves no local propagating source channel",
            "not_derived",
        ),
        (
            "ZTR716_4_boundary_silence",
            "no boundary/projection source remnant",
            "vertical/boundary terms have zero local projection and no flux charge",
            "not_derived",
        ),
        (
            "ZTR716_5_verdict",
            "b_A,I and Q_Aa zero theorem",
            "all prior requirements are signed with source paths and no MISSING markers",
            "not_satisfied",
        ),
    ]
    return [
        {
            "requirement_id": requirement_id,
            "zero_requirement": requirement,
            "proof_obligation": obligation,
            "current_status": status,
            "claim_effect": "blocks_zero_charge_claim" if status != "not_satisfied" else "zero_charge_not_available",
            "valid_for_claim": "false",
            "source_paths": source_list("410_doc", "626_doc", "710_descent", "711_qda", "711_owner"),
            "generated_utc": generated,
        }
        for requirement_id, requirement, obligation, status in rows
    ]


def aeh_update_rows() -> list[dict[str, str]]:
    generated = now()
    rows = [
        (
            "AEHU716_0_bAI",
            "b_A,I",
            "FREE_SYMBOLIC_RETAINED_COEFFICIENT",
            "zero_not_parent_derived",
            "matter/source charge remains active",
        ),
        (
            "AEHU716_1_frame",
            "f_frame*a_I",
            "FREE_SYMBOLIC_FRAME_TRANSFER_TERM",
            "frame_not_locked",
            "same-frame or Einstein-frame convention must be fixed next",
        ),
        (
            "AEHU716_2_QAa",
            "Q_Aa",
            "N_frame E_a^I(b_A,I+f_frame a_I)",
            "derived_shape_only",
            "effective charge formula exists but is not sourced",
        ),
        (
            "AEHU716_3_alpha",
            "alpha_AB,a(lambda_a)",
            "Q_Aa Q_Ba",
            "derived_shape_only",
            "R10 remains unscored until charge/range/bound curve are real",
        ),
    ]
    return [
        {
            "update_id": update_id,
            "target": target,
            "value_or_status": value,
            "current_status": status,
            "claim_effect": effect,
            "valid_for_claim": "false",
            "source_paths": source_list("715_pack", "715_coupling", "708_ppn_map"),
            "generated_utc": generated,
        }
        for update_id, target, value, status, effect in rows
    ]


def claim_gate_rows(
    source_rows: list[dict[str, str]],
    derivation_rows_: list[dict[str, str]],
    branch_rows: list[dict[str, str]],
    free_rows: list[dict[str, str]],
    frame_rows: list[dict[str, str]],
    zero_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    generated = now()
    missing_sources = [row["source_id"] for row in source_rows if row["exists"] != "true"]
    prior_failures = validation_failures("715_validation")
    functor_failed = matter_functor_failed()
    selected_free = any(row["branch_id"] == "SCL716_4_current_lock" and row["current_status"] == "selected_current_route" for row in branch_rows)
    frame_not_locked = any(row["frame_id"] == "FTM716_3_current_policy" and row["current_status"] == "selected_current_route" for row in frame_rows)
    zero_not_satisfied = any(row["requirement_id"] == "ZTR716_5_verdict" and row["current_status"] == "not_satisfied" for row in zero_rows)
    rows = [
        (
            "CG716_0_sources",
            "all source files load",
            f"missing_sources={len(missing_sources)}",
            "pass_structure" if not missing_sources else "fail_blocked",
            "allows checkpoint only",
        ),
        (
            "CG716_1_prior_715",
            "715 validation clean",
            f"715_validation_failures={len(prior_failures)}",
            "pass_structure" if not prior_failures else "fail_blocked",
            "inherits coefficient pack",
        ),
        (
            "CG716_2_charge_law_shape",
            "source charge law",
            f"derivation_rows={len(derivation_rows_)}",
            "pass_structure",
            "shape derived but no value claim",
        ),
        (
            "CG716_3_matter_functor_zero",
            "matter-blind zero theorem",
            f"matter_functor_failed_current_corpus={functor_failed}",
            "fail_blocked",
            "b_A,I=0 not claimable",
        ),
        (
            "CG716_4_free_lock",
            "free coefficient lock",
            f"selected_free_route={selected_free} free_template_rows={len(free_rows)}",
            "pass_blocked_recorded",
            "keeps retained branch honest",
        ),
        (
            "CG716_5_frame_transfer",
            "frame-transfer status",
            f"frame_not_locked={frame_not_locked}",
            "fail_blocked",
            "no scalar scoring before frame lock",
        ),
        (
            "CG716_6_zero_requirements",
            "zero theorem requirements",
            f"zero_verdict_not_satisfied={zero_not_satisfied}",
            "fail_blocked",
            "no coupling-zero theorem",
        ),
        (
            "CG716_7_claim_status",
            "R10/WEP/PPN/Gdot/R11/local-GR claims",
            "source charges and frame transfer are symbolic only",
            "fail_blocked",
            "no local-GR or fifth-force claim",
        ),
        (
            "CG716_8_next_target",
            "next target",
            NEXT_TARGET,
            "pass_structure",
            "frame-transfer coefficient pack selected",
        ),
    ]
    return [
        {
            "gate_id": gate_id,
            "gate": gate,
            "observed_state": state,
            "result": result,
            "claim_effect": effect,
            "valid_for_claim": "false",
            "source_paths": source_list("715_validation", "715_pack", "711_qda", "711_owner", "410_doc", "626_doc"),
            "generated_utc": generated,
        }
        for gate_id, gate, state, result, effect in rows
    ]


def decision_rows() -> list[dict[str, str]]:
    generated = now()
    rows = [
        (
            "D716_0_derivation",
            "matter charge law",
            "shape_derived",
            "variation of retained matter frame yields b_A,I and Q_Aa formulas",
            NEXT_TARGET,
        ),
        (
            "D716_1_zero",
            "b_A,I=0 theorem",
            "rejected_current_corpus",
            "matter functor/same-frame/no-mode requirements are not parent-signed",
            NEXT_TARGET,
        ),
        (
            "D716_2_free",
            "retained free coefficient",
            "locked_nonclaim",
            "b_A,I and f_frame remain explicit symbolic coefficients instead of hidden assumptions",
            NEXT_TARGET,
        ),
        (
            "D716_3_next",
            "next target",
            "selected",
            "frame transfer must be fixed before any scalar charge scoring",
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


def nonclaim_summary_rows() -> list[dict[str, str]]:
    generated = now()
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "charge_law": "Q_Aa=N_frame E_a^I(b_A,I+f_frame a_I)",
            "zero_charge_claim": "false",
            "free_coefficient_locked": "true",
            "main_result": "matter/source charge law shape is derived, but b_A,I=0 is not parent-derived; retain b_A,I and frame transfer as explicit symbolic coefficients",
            "remaining_blocker": "observed-frame lock and frame-transfer coefficient f_frame; then source/bound b_A,I",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated,
        }
    ]


def all_generated_rows(*tables: list[dict[str, str]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for table in tables:
        rows.extend(table)
    return rows


def validation_rows(
    source_rows: list[dict[str, str]],
    derivation_rows_: list[dict[str, str]],
    branch_rows: list[dict[str, str]],
    free_rows: list[dict[str, str]],
    frame_rows: list[dict[str, str]],
    activation_rows: list[dict[str, str]],
    zero_rows: list[dict[str, str]],
    aeh_rows: list[dict[str, str]],
    gate_rows: list[dict[str, str]],
    decision_rows_: list[dict[str, str]],
    summary_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    generated = now()
    missing_sources = [row for row in source_rows if row["exists"] != "true"]
    prior_failures = validation_failures("715_validation")
    all_rows = all_generated_rows(
        source_rows,
        derivation_rows_,
        branch_rows,
        free_rows,
        frame_rows,
        activation_rows,
        zero_rows,
        aeh_rows,
        gate_rows,
        decision_rows_,
        summary_rows,
    )
    changed_count = formalization_changed_count()
    checks = [
        (
            "V716_0_source_paths_exist",
            not missing_sources,
            "all cited source paths exist" if not missing_sources else "missing=" + ",".join(row["source_id"] for row in missing_sources),
        ),
        (
            "V716_1_prior_715_clean",
            not prior_failures,
            f"715_validation_failures={len(prior_failures)}",
        ),
        (
            "V716_2_matter_functor_failure_confirmed",
            matter_functor_failed(),
            "QDA711_4 and OWN711_3 fail_current_corpus",
        ),
        (
            "V716_3_charge_law_shape_written",
            any("Q_Aa" in row["statement"] for row in derivation_rows_),
            "Q_Aa charge law present",
        ),
        (
            "V716_4_zero_condition_not_promoted",
            any(row["branch_id"] == "SCL716_0_parent_zero" and row["current_status"] == "not_available" for row in branch_rows),
            "zero branch not available",
        ),
        (
            "V716_5_free_coefficient_locked",
            any(row["branch_id"] == "SCL716_4_current_lock" and row["current_status"] == "selected_current_route" for row in branch_rows),
            "free coefficient route selected",
        ),
        (
            "V716_6_free_template_nonclaim",
            len(free_rows) == 3 and all(row["valid_for_claim"] == "false" for row in free_rows),
            f"free_template_rows={len(free_rows)}",
        ),
        (
            "V716_7_frame_transfer_retained",
            any(row["frame_transfer_value"] == "retain f_frame symbolically" for row in frame_rows),
            "frame transfer retained symbolically",
        ),
        (
            "V716_8_observable_activation_complete",
            {"Newtonian limit", "R1_WEP_source_charge", "R2_clock_redshift", "R3_gamma", "R4_beta", "R9_Gdot", "R10_fifth_force", "R11_EH_operator_ledger"}.issubset({row["arena"] for row in activation_rows}),
            f"activation_rows={len(activation_rows)}",
        ),
        (
            "V716_9_zero_requirements_blocked",
            any(row["requirement_id"] == "ZTR716_5_verdict" and row["current_status"] == "not_satisfied" for row in zero_rows),
            "zero theorem requirements not satisfied",
        ),
        (
            "V716_10_AEH_update_charge_formula",
            any(row["target"] == "Q_Aa" and "N_frame" in row["value_or_status"] for row in aeh_rows),
            "AEH update records Q_Aa formula",
        ),
        (
            "V716_11_claim_gates_block",
            any(row["gate_id"] == "CG716_7_claim_status" and row["result"] == "fail_blocked" for row in gate_rows),
            "claim gate remains blocked",
        ),
        (
            "V716_12_next_target_selected",
            any(row["next_action"] == NEXT_TARGET for row in decision_rows_),
            NEXT_TARGET,
        ),
        (
            "V716_13_no_claim_rows_promoted",
            all(row.get("valid_for_claim", "false") == "false" for row in all_rows),
            "all generated rows valid_for_claim=false",
        ),
        (
            "V716_14_outputs_scoped",
            all(str(path).startswith(str(ROOT)) for path in OUTPUT_PATHS),
            "all outputs under post-checkpoint-work",
        ),
        (
            "V716_15_formalization_workbench_untouched",
            changed_count == 0,
            f"formalization_changed_after_cutoff={changed_count}",
        ),
        (
            "V716_16_status_nonclaim",
            CLAIM_CEILING in summary_rows[0]["claim_ceiling"],
            CLAIM_CEILING,
        ),
    ]
    return [
        {
            "check_id": check_id,
            "result": "pass" if passed else "fail",
            "detail": detail,
            "generated_utc": generated,
        }
        for check_id, passed, detail in checks
    ]


def markdown_table(rows: list[dict[str, str]], columns: list[str]) -> str:
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |")
    return "\n".join(lines)


def write_markdown(
    source_rows: list[dict[str, str]],
    derivation_rows_: list[dict[str, str]],
    branch_rows: list[dict[str, str]],
    free_rows: list[dict[str, str]],
    frame_rows: list[dict[str, str]],
    activation_rows: list[dict[str, str]],
    zero_rows: list[dict[str, str]],
    aeh_rows: list[dict[str, str]],
    gate_rows: list[dict[str, str]],
    decision_rows_: list[dict[str, str]],
    summary_rows: list[dict[str, str]],
    validation_rows_: list[dict[str, str]],
) -> None:
    content = f"""# 716 - Y5 R10 Matter Coupling Source Charge Derivation Or Free Coefficient Lock

## Summary

716 derives the retained scalar/source charge **shape**, but rejects the zero claim for the current corpus.

The retained matter frame gives the charge law:

`b_A,I := partial_I ln m_A^obs(u)|u0`

and the observable canonical charge is

`Q_Aa = N_frame E_a^I (b_A,I + f_frame a_I)`.

Because the matter functor/same-frame/no-mode premises are not parent-signed, `b_A,I=0` is not a theorem. The safe route is to lock `b_A,I` and `f_frame` as explicit retained/free symbolic coefficients until the frame is fixed and the coupling is either derived, bounded, or theorem-zero.

| Status | `{STATUS}` |
| --- | --- |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## Matter Coupling Derivation

{markdown_table(derivation_rows_, ["derivation_id", "object", "statement", "derivation_status", "claim_effect", "valid_for_claim"])}

## Source Charge Branch Lock

{markdown_table(branch_rows, ["branch_id", "branch", "charge_condition", "current_status", "observable_effect", "next_action", "valid_for_claim"])}

## Free Coefficient Template

{markdown_table(free_rows, ["template_id", "source_or_test_label", "mode_label", "raw_charge_symbol", "raw_charge_status", "frame_transfer_symbol", "frame_transfer_status", "effective_field_charge", "canonical_charge_or_alpha", "valid_for_claim"])}

## Frame Transfer Map

{markdown_table(frame_rows, ["frame_id", "frame_branch", "frame_transfer_value", "requirement", "current_status", "valid_for_claim"])}

## Observable Activation Matrix

{markdown_table(activation_rows, ["activation_id", "arena", "activation_rule", "current_status", "minimum_next_input", "valid_for_claim"])}

## Zero Theorem Requirements

{markdown_table(zero_rows, ["requirement_id", "zero_requirement", "proof_obligation", "current_status", "claim_effect", "valid_for_claim"])}

## Aeh Scalar Update

{markdown_table(aeh_rows, ["update_id", "target", "value_or_status", "current_status", "claim_effect", "valid_for_claim"])}

## Claim Gate Evaluation

{markdown_table(gate_rows, ["gate_id", "gate", "observed_state", "result", "claim_effect", "valid_for_claim"])}

## Decision

{markdown_table(decision_rows_, ["decision_id", "target", "result", "reason", "next_action", "valid_for_claim"])}

## Nonclaim Summary

{markdown_table(summary_rows, ["status", "claim_ceiling", "charge_law", "zero_charge_claim", "free_coefficient_locked", "main_result", "remaining_blocker", "next_target", "valid_for_claim"])}

## Source Register

{markdown_table(source_rows, ["source_id", "path", "exists", "role"])}

## Validation

{markdown_table(validation_rows_, ["check_id", "result", "detail"])}

## Verdict

This is a good, slightly annoying checkpoint: the coupling is no longer vague, but it also refuses to disappear for free. The exact pressure point is now `f_frame` plus `b_A,I`. If the next frame lock gives `f_frame=0` and a later matter theorem gives `b_A,I=0`, the scalar route can collapse cleanly toward GR. If either survives, we must score it as a real retained scalar interaction.
"""
    DOC_PATH.write_text(content, encoding="utf-8")


def main() -> int:
    source_rows = source_register_rows()
    derivation_rows_ = derivation_rows()
    branch_rows = branch_lock_rows()
    free_rows = free_template_rows()
    frame_rows = frame_transfer_rows()
    activation_rows = observable_activation_rows()
    zero_rows = zero_requirements_rows()
    aeh_rows = aeh_update_rows()
    gate_rows = claim_gate_rows(source_rows, derivation_rows_, branch_rows, free_rows, frame_rows, zero_rows)
    decision_rows_ = decision_rows()
    summary_rows = nonclaim_summary_rows()
    validation_rows_ = validation_rows(
        source_rows,
        derivation_rows_,
        branch_rows,
        free_rows,
        frame_rows,
        activation_rows,
        zero_rows,
        aeh_rows,
        gate_rows,
        decision_rows_,
        summary_rows,
    )

    write_csv(
        RESIDUALS / "P8_Y5_R10_716_SOURCE_REGISTER.csv",
        source_rows,
        ["source_id", "path", "exists", "role", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_716_MATTER_COUPLING_DERIVATION.csv",
        derivation_rows_,
        ["derivation_id", "object", "statement", "derivation_status", "claim_effect", "valid_for_claim", "source_paths", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_716_SOURCE_CHARGE_BRANCH_LOCK.csv",
        branch_rows,
        ["branch_id", "branch", "charge_condition", "current_status", "observable_effect", "next_action", "valid_for_claim", "source_paths", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_716_FREE_COEFFICIENT_TEMPLATE.csv",
        free_rows,
        [
            "template_id",
            "source_or_test_label",
            "mode_label",
            "raw_charge_symbol",
            "raw_charge_status",
            "frame_transfer_symbol",
            "frame_transfer_status",
            "effective_field_charge",
            "canonical_charge_or_alpha",
            "derivation_status",
            "valid_for_claim",
            "source_paths",
            "generated_utc",
        ],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_716_FRAME_TRANSFER_MAP.csv",
        frame_rows,
        ["frame_id", "frame_branch", "frame_transfer_value", "requirement", "current_status", "valid_for_claim", "source_paths", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_716_OBSERVABLE_ACTIVATION_MATRIX.csv",
        activation_rows,
        ["activation_id", "arena", "activation_rule", "current_status", "minimum_next_input", "valid_for_claim", "source_paths", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_716_ZERO_THEOREM_REQUIREMENTS.csv",
        zero_rows,
        ["requirement_id", "zero_requirement", "proof_obligation", "current_status", "claim_effect", "valid_for_claim", "source_paths", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_716_AEH_SCALAR_UPDATE.csv",
        aeh_rows,
        ["update_id", "target", "value_or_status", "current_status", "claim_effect", "valid_for_claim", "source_paths", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_716_CLAIM_GATE_EVALUATION.csv",
        gate_rows,
        ["gate_id", "gate", "observed_state", "result", "claim_effect", "valid_for_claim", "source_paths", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_716_DECISION.csv",
        decision_rows_,
        ["decision_id", "target", "result", "reason", "next_action", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_716_NONCLAIM_SUMMARY.csv",
        summary_rows,
        [
            "status",
            "claim_ceiling",
            "charge_law",
            "zero_charge_claim",
            "free_coefficient_locked",
            "main_result",
            "remaining_blocker",
            "next_target",
            "valid_for_claim",
            "generated_utc",
        ],
    )
    write_csv(
        RESIDUALS / "P8_Y5_BRR545_716_VALIDATION.csv",
        validation_rows_,
        ["check_id", "result", "detail", "generated_utc"],
    )
    write_markdown(
        source_rows,
        derivation_rows_,
        branch_rows,
        free_rows,
        frame_rows,
        activation_rows,
        zero_rows,
        aeh_rows,
        gate_rows,
        decision_rows_,
        summary_rows,
        validation_rows_,
    )

    failures = [row for row in validation_rows_ if row["result"] != "pass"]
    print(f"{STATUS}: validation_passes={len(validation_rows_) - len(failures)}/{len(validation_rows_)}")
    if failures:
        for failure in failures:
            print(f"FAIL {failure['check_id']}: {failure['detail']}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
