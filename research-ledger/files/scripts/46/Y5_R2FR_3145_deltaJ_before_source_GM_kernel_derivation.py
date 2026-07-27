from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"

INPUTS = OUT / "P8_Y5_R2FR_3145_INPUTS.csv"
KERNEL = OUT / "P8_Y5_R2FR_3145_DELTAJ_BEFORE_GM_KERNEL.csv"
LIMITS = OUT / "P8_Y5_R2FR_3145_LIMIT_REDUCTIONS.csv"
GATES = OUT / "P8_Y5_R2FR_3145_OBSERVABILITY_GATES.csv"
RESIDUALS = OUT / "P8_Y5_R2FR_3145_RESIDUAL_VECTOR.csv"
DECISION = OUT / "P8_Y5_R2FR_3145_DECISION.csv"
VALIDATION = OUT / "P8_Y5_R2FR_3145_VALIDATION.csv"


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
            "source_id": "SRC3145_0_3144_doc",
            "path": source_path("3144-Y5-R2FR-no-cA-slot-grammar-or-deltaJ-branch-selection-under-AX1090.md"),
            "role": "selected before-variation finite delta_J branch",
        },
        {
            "source_id": "SRC3145_1_3144_residuals",
            "path": source_path(
                "source-intake/mts_residuals/P8_Y5_R2FR_3144_SELECTED_DELTAJ_RESIDUAL_ROWS.csv"
            ),
            "role": "Delta_GM_J missing-kernel handoff",
        },
        {
            "source_id": "SRC3145_2_3144_decision",
            "path": source_path("source-intake/mts_residuals/P8_Y5_R2FR_3144_DECISION.csv"),
            "role": "3145 target selection",
        },
        {
            "source_id": "SRC3145_3_3121_doc",
            "path": source_path("3121-Y5-R2FR-deltaJ-source-calibration-DeltaGM-bridge-under-AX1090.md"),
            "role": "older delta_J to DeltaGM leading bridge",
        },
        {
            "source_id": "SRC3145_4_3121_gate",
            "path": source_path("source-intake/mts_residuals/P8_Y5_R2FR_3121_DELTAJ_GM_BRIDGE_GATE.csv"),
            "role": "derived conditional gate rows",
        },
        {
            "source_id": "SRC3145_5_3142_doc",
            "path": source_path("3142-Y5-R2FR-em-poynting-qbasic-sector-under-AX1090.md"),
            "role": "Maxwell/Hilbert stress and Poynting lock",
        },
        {
            "source_id": "SRC3145_6_3143_doc",
            "path": source_path("3143-Y5-R2FR-same-current-owner-action-variation-under-AX1090.md"),
            "role": "same-current zero route and finite residual retention",
        },
        {
            "source_id": "SRC3145_7_local_bounds",
            "path": source_path("source-intake/local_bounds/local_bound_claims.csv"),
            "role": "local WEP/PPN/Gdot bound anchors; not directly scoreable here",
        },
    ]
    for row in rows:
        row["exists"] = str(Path(row["path"]).exists()).lower()
        row["valid_for_claim"] = "false"
        row["generated_utc"] = now
    return rows


def kernel_rows() -> list[dict[str, str]]:
    now = stamp()
    return [
        {
            "kernel_id": "KGM3145_0_branch_variable",
            "object": "epsilon_J_before and u_J(x)",
            "statement": "Selected finite branch is represented as J_Q -> J_Q + epsilon_J_before u_J(x) J_Q before Maxwell solve and Hilbert variation.",
            "formula": "delta J_Q = epsilon_J_before u_J J_Q",
            "derived_status": "definition_for_selected_branch",
            "observable_role": "branch source variable; not a prediction until epsilon_J_before is parent-sourced",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "kernel_id": "KGM3145_1_maxwell_frechet",
            "object": "delta F_Q",
            "statement": "On the fixed public Maxwell background used by 3142/3121, the first field response is the Maxwell Green/Frechet response to delta J_Q.",
            "formula": "L_A[delta A_Q]=delta J_Q, delta F_Q=d(delta A_Q)=G_F[epsilon_J_before u_J J_Q]",
            "derived_status": "conditional_linear_response_derived",
            "observable_role": "maps current-normalization branch into field-strength perturbation",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "kernel_id": "KGM3145_2_em_stress_frechet",
            "object": "delta T_EM",
            "statement": "Holding public metric/coframe, Hodge owner, and EM kinetic normalization fixed, the EM stress perturbation is the Frechet derivative of Hilbert Maxwell stress.",
            "formula": "delta T_EM^{mu nu}=Z_EM(delta F^mu_a F^{nu a}+F^mu_a delta F^{nu a}-1/2 g^{mu nu} F_ab delta F^{ab})",
            "derived_status": "conditional_hilbert_stress_response_derived",
            "observable_role": "first source-side stress contamination entering Newton/GR",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "kernel_id": "KGM3145_3_source_mass_functional",
            "object": "K_GM_J[S;u_J]",
            "statement": "The source-GM kernel is the Hilbert/source mass functional applied to delta T_EM plus any matter relaxation and boundary/support terms not killed by parent descent.",
            "formula": "K_GM_J[S;u]=(1/M_H,S) Int_S xi_nu delta T_EM^{mu nu}[u] dSigma_mu + K_relax,S[u]+K_boundary,S[u]",
            "derived_status": "kernel_definition_derived_nonclaim",
            "observable_role": "turns delta_J_before into raw source mass / GM response",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "kernel_id": "KGM3145_4_observed_calibration_subtraction",
            "object": "Delta ln GM_obs",
            "statement": "The observable source-GM residual is calibration-subtracted; common-mode current normalization shared by source and calibration is not itself a local-GR failure.",
            "formula": "Delta ln(GM)_obs,J = epsilon_J_before [K_GM_J[S;u_S]-K_GM_J[cal;u_cal]]",
            "derived_status": "observable_kernel_law_derived_nonclaim",
            "observable_role": "main 3145 bridge from selected branch to Newton/orbital source normalization",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "kernel_id": "KGM3145_5_local_GR_condition",
            "object": "local GR/Newton gate",
            "statement": "The finite branch is harmless for local GR only if epsilon_J_before=0, or the calibration-subtracted kernel vanishes, or its absolute residual vector is below local bounds without fitted-GM circularity.",
            "formula": "pass_local <= epsilon_J_before=0 OR K_GM_J[S]=K_GM_J[cal] OR |Pi_local epsilon_J_before Delta K_GM_J| <= bound",
            "derived_status": "gate_law_derived_nonclaim",
            "observable_role": "prevents both false failure and false pass",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def limit_rows() -> list[dict[str, str]]:
    now = stamp()
    return [
        {
            "limit_id": "LIM3145_0_constant_profile",
            "assumptions": "u_J=1 over source support; fixed public Hodge/Z_EM; stationary weak field; no relaxation; no boundary/support tail",
            "reduction": "delta F=epsilon_J_before F and delta T_EM=2 epsilon_J_before T_EM",
            "kernel_result": "K_GM_J[S]=2 f_EM,S^H",
            "status": "derived_simplifying_limit",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "limit_id": "LIM3145_1_weighted_profile",
            "assumptions": "u_J varies over source support but Maxwell response remains linear and stationary",
            "reduction": "source mass response is EM-energy weighted plus nonlocal Green-kernel corrections",
            "kernel_result": "K_GM_J[S]=2 f_EM,S^H <u_J>_EM,S + K_nonlocal,S + K_relax,S + K_boundary,S",
            "status": "derived_profile_generalization",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "limit_id": "LIM3145_2_calibrated_common_mode",
            "assumptions": "same u_J, same kernel, and same time dependence in source and calibration convention",
            "reduction": "K_GM_J[S]-K_GM_J[cal]=0",
            "kernel_result": "Delta ln(GM)_obs,J=0 despite a raw common-mode mass normalization",
            "status": "derived_observable_silence_condition",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "limit_id": "LIM3145_3_differential_source",
            "assumptions": "source and calibration have different EM fractions/profile weights/relaxation/boundary tails",
            "reduction": "Delta K_GM_J != 0",
            "kernel_result": "Delta ln(GM)_obs,J=epsilon_J_before Delta K_GM_J",
            "status": "derived_observable_residual_condition",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "limit_id": "LIM3145_4_same_current_zero",
            "assumptions": "3143 same-current owner and 3144 no-cA/no-wA grammar both parent-signed",
            "reduction": "epsilon_J_before=delta_J_before=0",
            "kernel_result": "Delta ln(GM)_obs,J=0 and Delta_T_EM^J=0",
            "status": "conditional_zero_route_not_currently_signed",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def gate_rows() -> list[dict[str, str]]:
    now = stamp()
    return [
        {
            "gate_id": "G3145_0_parent_coefficient",
            "gate": "epsilon_J_before_parent_sourced_or_zero",
            "status": "fail_for_claim",
            "reason": "3144 selected finite branch but no parent coefficient or zero theorem has been signed",
            "next_action": "derive epsilon_J_before from parent coupling or keep as bounded residual",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "G3145_1_source_kernel",
            "gate": "K_GM_J_source_numeric_or_zero",
            "status": "fail_for_claim",
            "reason": "source EM fraction/profile/relaxation/boundary kernel is formula-derived but not sourced",
            "next_action": "source f_EM,S^H, profile weight, K_relax, K_boundary for a chosen body",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "G3145_2_calibration_kernel",
            "gate": "K_GM_J_calibration_reference_locked",
            "status": "fail_for_claim",
            "reason": "observable residual requires a same-frame calibration convention, not fitted-GM circularity",
            "next_action": "choose source-calibration convention and derive its kernel before scoring",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "G3145_3_metric_response",
            "gate": "Delta_T_EM_to_metric_shape_kernel",
            "status": "not_required_for_raw_GM_but_required_for_PPN",
            "reason": "DeltaGM alone does not determine gamma/beta; metric Green/PPN projection is a separate kernel",
            "next_action": "derive Pi_PPN G_metric[delta T_EM] after source kernel is staged",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "G3145_4_no_fitted_GM_shortcut",
            "gate": "no_orbital_GM_denominator_circularity",
            "status": "pass_as_policy_guard",
            "reason": "3145 uses calibrated residual DeltaK, not fitted orbital GM as proof input",
            "next_action": "keep this guard in future score runners",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def residual_rows() -> list[dict[str, str]]:
    now = stamp()
    return [
        {
            "residual_id": "RV3145_0_epsilon_J_before",
            "quantity": "epsilon_J_before",
            "formula_or_status": "MISSING_PARENT_COEFFICIENT_OR_3144_ZERO_GRAMMAR",
            "arena": "EM/source coupling",
            "observable_effect": "multiplies every selected before-variation current/source residual",
            "needed_for_claim": "parent coefficient value, bound, or zero theorem",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "residual_id": "RV3145_1_K_GM_source",
            "quantity": "K_GM_J[S;u_S]",
            "formula_or_status": "(1/M_H,S) Int_S xi.delta T_EM[u_S] + K_relax,S + K_boundary,S",
            "arena": "Newton/orbital source GM",
            "observable_effect": "raw source mass/GM response to epsilon_J_before",
            "needed_for_claim": "source body profile, EM stress fraction, support/worldtube and relaxation convention",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "residual_id": "RV3145_2_K_GM_cal",
            "quantity": "K_GM_J[cal;u_cal]",
            "formula_or_status": "same functional evaluated on calibration reference",
            "arena": "measured-G/GM calibration",
            "observable_effect": "subtracts universal/common-mode current normalization",
            "needed_for_claim": "same-frame calibration reference and no fitted-GM circularity proof",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "residual_id": "RV3145_3_Delta_ln_GM_obs",
            "quantity": "Delta_ln_GM_obs_J",
            "formula_or_status": "epsilon_J_before*(K_GM_J[S;u_S]-K_GM_J[cal;u_cal])",
            "arena": "Newton/orbital/local GR",
            "observable_effect": "first derived source-GM residual law for 3144 selected branch",
            "needed_for_claim": "epsilon_J_before and both kernels numeric/sourced or theorem-zero",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "residual_id": "RV3145_4_PPN_shape",
            "quantity": "Delta_PPN_J",
            "formula_or_status": "Pi_PPN G_metric[delta T_EM[u_S]-delta T_EM[cal]] epsilon_J_before",
            "arena": "PPN gamma/beta",
            "observable_effect": "shape residual, not reducible to DeltaGM alone",
            "needed_for_claim": "metric Green operator and PPN projection kernel",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "residual_id": "RV3145_5_Gdot",
            "quantity": "d_ln_GM_dt_J",
            "formula_or_status": "DeltaK_GM_J d(epsilon_J_before)/dt + epsilon_J_before d(DeltaK_GM_J)/dt",
            "arena": "clock/orbital/Gdot",
            "observable_effect": "time-varying current branch route",
            "needed_for_claim": "time profile for epsilon_J_before and kernel evolution",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    now = stamp()
    return [
        {
            "decision_id": "D3145_0_kernel_derived",
            "decision": "DeltaGM_J kernel is now derived as a calibration-subtracted Hilbert/source-mass Frechet functional",
            "effect": "3144 missing DeltaGM bridge is replaced by formula-level kernel rows, not a numeric claim",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "D3145_1_common_mode_guard",
            "decision": "common-mode current normalization is not automatically observable",
            "effect": "do not mark local GR failed unless calibration-subtracted or time/differential residual survives",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "D3145_2_next",
            "decision": "next target should source or derive the first K_GM_J source/calibration kernel pair",
            "effect": "choose a body/convention, probably Earth/Sun or laboratory calibration, and fill f_EM/profile/relaxation rows",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def validation_rows(
    inputs: list[dict[str, str]],
    kernels: list[dict[str, str]],
    limits: list[dict[str, str]],
    gates: list[dict[str, str]],
    residuals: list[dict[str, str]],
    decisions: list[dict[str, str]],
) -> list[dict[str, str]]:
    now = stamp()
    sources_exist = all(row["exists"] == "true" for row in inputs)
    has_frechet = {"KGM3145_1_maxwell_frechet", "KGM3145_2_em_stress_frechet"}.issubset(
        {row["kernel_id"] for row in kernels}
    )
    has_observable_law = any(
        row["kernel_id"] == "KGM3145_4_observed_calibration_subtraction"
        and "K_GM_J[S;u_S]-K_GM_J[cal;u_cal]" in row["formula"]
        for row in kernels
    )
    has_limits = {"LIM3145_0_constant_profile", "LIM3145_2_calibrated_common_mode", "LIM3145_3_differential_source"}.issubset(
        {row["limit_id"] for row in limits}
    )
    claims_blocked = all(row["claim_allowed"] == "false" for row in kernels + limits + gates + residuals)
    residual_cover = {"epsilon_J_before", "K_GM_J[S;u_S]", "K_GM_J[cal;u_cal]", "Delta_ln_GM_obs_J"}.issubset(
        {row["quantity"] for row in residuals}
    )
    decisions_nonclaim = all(row["valid_for_claim"] == "false" for row in decisions)
    return [
        {
            "check_id": "V3145_0_sources_exist",
            "status": "pass" if sources_exist else "fail",
            "details": json.dumps({row["source_id"]: row["exists"] for row in inputs}, ensure_ascii=False),
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3145_1_frechet_kernel_present",
            "status": "pass" if has_frechet else "fail",
            "details": json.dumps([row["kernel_id"] for row in kernels], ensure_ascii=False),
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3145_2_observable_calibration_law_present",
            "status": "pass" if has_observable_law else "fail",
            "details": "Delta ln(GM)_obs,J = epsilon_J_before DeltaK_GM_J",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3145_3_limit_reductions_present",
            "status": "pass" if has_limits else "fail",
            "details": json.dumps([row["limit_id"] for row in limits], ensure_ascii=False),
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3145_4_no_claim_leak",
            "status": "pass" if claims_blocked and decisions_nonclaim else "fail",
            "details": "",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3145_5_residual_vector_covers_kernel",
            "status": "pass" if residual_cover else "fail",
            "details": json.dumps([row["quantity"] for row in residuals], ensure_ascii=False),
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def main() -> None:
    inputs = input_rows()
    kernels = kernel_rows()
    limits = limit_rows()
    gates = gate_rows()
    residuals = residual_rows()
    decisions = decision_rows()
    validations = validation_rows(inputs, kernels, limits, gates, residuals, decisions)
    write_csv(INPUTS, inputs)
    write_csv(KERNEL, kernels)
    write_csv(LIMITS, limits)
    write_csv(GATES, gates)
    write_csv(RESIDUALS, residuals)
    write_csv(DECISION, decisions)
    write_csv(VALIDATION, validations)


if __name__ == "__main__":
    main()
