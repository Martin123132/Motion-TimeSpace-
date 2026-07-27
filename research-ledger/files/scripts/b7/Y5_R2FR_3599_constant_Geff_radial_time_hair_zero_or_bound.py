from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CHECKPOINT_ID = "3599"
BRANCH_ID = "MTS_R2FR_Y5_CONSTANT_GEFF_RADIAL_TIME_HAIR_3599"
DOC = ROOT / "3599-Y5-R2FR-constant-Geff-radial-time-hair-zero-or-bound.md"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"refusing to write empty csv: {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def contains(path: Path, needle: str) -> bool:
    return needle in path.read_text(encoding="utf-8-sig", errors="replace")


def sources() -> dict[str, tuple[Path, str]]:
    return {
        "next_3598": (
            RESIDUALS / "P8_Y5_R2FR_3598_NEXT_TARGET.csv",
            "NEXT3598_0",
        ),
        "status_3598": (
            RESIDUALS / "P8_Y5_R2FR_3598_STATUS.csv",
            "GAUSS_ORBITAL_CALIBRATION",
        ),
        "bounds_3598": (
            RESIDUALS / "P8_Y5_R2FR_3598_GAUSS_ORBITAL_BOUND_ROWS.csv",
            "GOB3598_7_partial_r_ln_mu_obs",
        ),
        "derivative_gate": (
            RESIDUALS / "P8_CONSTANT_GM_DERIVATIVE_HAIR_GATE.csv",
            "CGM0_master_identity",
        ),
        "derivative_fill_queue": (
            RESIDUALS / "P8_CONSTANT_GM_DERIVATIVE_HAIR_FILL_QUEUE.csv",
            "CGM1_time_drift",
        ),
        "constant_gm_zero_attempt": (
            RESIDUALS / "P8_CONSTANT_GM_ZERO_THEOREM_ATTEMPT.csv",
            "Z1_global_coupling_superselection",
        ),
        "constant_gm_decision": (
            RESIDUALS / "P8_CONSTANT_GM_ZERO_OR_RESIDUAL_DECISION.csv",
            "zero_theorem_currently_closes",
        ),
        "constant_gm_bound_matrix": (
            RESIDUALS / "P8_CONSTANT_GM_RESIDUAL_BOUND_MATRIX.csv",
            "P8_Geff_time_drift",
        ),
        "constant_gm_runner_input": (
            RESIDUALS / "P8_CONSTANT_GM_LOCAL_RESIDUAL_RUNNER_INPUT.csv",
            "P8_radial_source_hair",
        ),
        "constant_geff_contract": (
            RESIDUALS / "P8_constant_universal_Geff_kappa_CONTRACT.csv",
            "CU7_measured_GM_product_silence",
        ),
        "kappa_product_lock": (
            RESIDUALS / "P8_EM_fixed_kappa_Gref_action_line_lock.csv",
            "KGLR3511_4_Geff_product",
        ),
        "charge_residuals": (
            RESIDUALS / "P8_charge_current_equality_RESIDUAL_DECOMPOSITION.csv",
            "Delta_G",
        ),
        "mu_extra_vector": (
            RESIDUALS / "P8_mu_extra_over_Geff_Meff_vector.csv",
            "EMV3501_2_time_MH_flux",
        ),
        "radial_profile": (
            RESIDUALS / "P8_radial_mu_profile_or_zero.csv",
            "RH3048_0_radial_hair_definition",
        ),
        "time_drift": (
            RESIDUALS / "P8_time_drift_residual_or_zero.csv",
            "TD3048_0_time_drift_definition",
        ),
        "source_flux_closure": (
            RESIDUALS / "P8_Y5_R2FR_3502_DRESSED_SOURCE_FLUX_CLOSURE_THEOREM.csv",
            "DFC3502_2_time_flux_closure",
        ),
        "derivative_nohair_3557": (
            RESIDUALS / "P8_Y5_R2FR_3557_DERIVATIVE_HAIR_NOHAIR_THEOREM.csv",
            "NH3557_0_master_derivative_identity",
        ),
        "derivative_bound_3557": (
            RESIDUALS / "P8_Y5_R2FR_3557_DERIVATIVE_HAIR_BOUND_RUNNER_INPUT.csv",
            "B3557_0_Gdot",
        ),
        "derivative_status_3557": (
            RESIDUALS / "P8_Y5_source_normalization_derivative_hair_status.csv",
            "Y5_DERIVATIVE_HAIR",
        ),
        "r11_derivative_vector": (
            RESIDUALS / "R11_SOURCE_NORMALIZATION_DERIVATIVE_HAIR_VECTOR.csv",
            "R11_source_normalization_derivative_hair_vector",
        ),
    }


def outputs() -> dict[str, Path]:
    return {
        "source_register": RESIDUALS / "P8_Y5_R2FR_3599_SOURCE_REGISTER.csv",
        "nohair_theorem": RESIDUALS / "P8_Y5_R2FR_3599_CONSTANT_GEFF_RADIAL_TIME_NOHAIR_THEOREM.csv",
        "residuals": RESIDUALS / "P8_Y5_R2FR_3599_DERIVATIVE_HAIR_RESIDUALS.csv",
        "bound_rows": RESIDUALS / "P8_Y5_R2FR_3599_DERIVATIVE_HAIR_BOUND_ROWS.csv",
        "promotion_gates": RESIDUALS / "P8_Y5_R2FR_3599_PROMOTION_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3599_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3599_NEXT_TARGET.csv",
        "canonical_status": RESIDUALS / "P8_Y5_constant_Geff_radial_time_hair_status.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3599_VALIDATION.csv",
    }


def source_register_rows(source_map: dict[str, tuple[Path, str]]) -> list[dict[str, object]]:
    rows = []
    for source_id, (path, needle) in source_map.items():
        exists = path.exists()
        rows.append(
            {
                "timestamp_utc": now(),
                "branch_id": BRANCH_ID,
                "checkpoint_id": CHECKPOINT_ID,
                "source_id": source_id,
                "source_path": str(path),
                "exists": exists,
                "needle": needle,
                "needle_found": exists and contains(path, needle),
                "valid_for_claim": False,
            }
        )
    return rows


def theorem_rows(source_map: dict[str, tuple[Path, str]]) -> list[dict[str, object]]:
    p = {key: str(value[0]) for key, value in source_map.items()}
    rows = [
        (
            "NH3599_0_target",
            "3599 target",
            "Try to prove constant universal G_eff/kappa superselection and radial/time derivative silence for mu_obs, or retain dln_Geff_dt, dln_Meff_dt, partial_t epsilon_mu and partial_r ln mu_obs bounds.",
            "3598 showed Delta_cal cannot close while derivative hair is unowned.",
            "TARGET_IMPORTED",
            "next_3598",
        ),
        (
            "NH3599_1_master_identity",
            "master derivative identity",
            "epsilon_mu := mu_extra/(G_eff M_eff), mu_obs = G_eff M_eff(1+epsilon_mu), and D_X ln mu_obs = D_X ln G_eff + D_X ln M_eff + D_X ln(1+epsilon_mu).",
            "This is exact algebra. It prevents hiding time/radial/source/range drift inside measured GM.",
            "EXACT_IDENTITY_DERIVED",
            "derivative_gate",
        ),
        (
            "NH3599_2_global_coupling_superselection",
            "constant G_eff route",
            "If kappa_eff/G_eff is a global parent coupling or superselection label, not a local field and not a function of q, memory, source species, range, frame or domain, then D_X ln G_eff=0 for X={t,r,A,lambda,frame,domain}.",
            "This is the correct zero route for Newton's constant: not derived numerically, but fixed by action grammar/global coupling status.",
            "CONDITIONAL_ZERO_ROUTE_NOT_SIGNED",
            "constant_geff_contract",
        ),
        (
            "NH3599_3_product_lock",
            "G_eff product lock",
            "D_X ln G_eff_product = D_X ln(G_ref w_common ell_J R_frame), so constant kappa alone is insufficient unless action-line, source-current normalization and frame factors are also derivative-silent.",
            "This blocks a cheap win where kappa is constant but the effective measured coupling still drifts.",
            "EXACT_PRODUCT_DECOMPOSITION",
            "kappa_product_lock",
        ),
        (
            "NH3599_4_source_flux_nohair",
            "M_eff flux no-hair",
            "If d(Pi_M J_H_total)=0 in the source-free exterior annulus and the local branch is stationary with no net timelike boundary flux, then partial_r ln M_eff=0 and d ln M_eff/dt=0.",
            "This is the source-side no-hair route: closed projected Hilbert flux, not post-fit mass constancy.",
            "CONDITIONAL_ZERO_ROUTE_NOT_SIGNED",
            "source_flux_closure",
        ),
        (
            "NH3599_5_extra_monopole_nohair",
            "epsilon_mu no-hair",
            "If mu_extra=0, or mu_extra/(G_eff M_eff) is a parent-fixed universal constant, then D_X ln(1+epsilon_mu)=0; otherwise mu_extra carries derivative hair.",
            "This separates harmless global calibration from real local physics.",
            "CONDITIONAL_ZERO_ROUTE_NOT_SIGNED",
            "mu_extra_vector",
        ),
        (
            "NH3599_6_time_nohair",
            "time hair law",
            "d ln mu_obs/dt = d ln G_eff/dt + d ln M_eff/dt + partial_t epsilon_mu/(1+epsilon_mu).",
            "Therefore local Gdot silence requires all three terms zero by parent identity, or sourced bounds with no fitted cancellation.",
            "EXACT_TIME_HAIR_LAW",
            "time_drift",
        ),
        (
            "NH3599_7_radial_nohair",
            "radial hair law",
            "partial_r ln mu_obs = partial_r ln G_eff + partial_r ln M_eff + partial_r epsilon_mu/(1+epsilon_mu).",
            "Therefore inverse-square Newton requires radial coupling silence, closed Gauss/source flux and no radial extra-monopole profile.",
            "EXACT_RADIAL_HAIR_LAW",
            "radial_profile",
        ),
        (
            "NH3599_8_no_cancellation_rule",
            "no fitted cancellation",
            "A cancellation among D_X ln G_eff, D_X ln M_eff and D_X ln(1+epsilon_mu) counts only if the parent action gives an identity; fitted epoch-by-epoch or radius-by-radius cancellation remains nonclaim.",
            "This is the guardrail that keeps the branch from smuggling closure.",
            "ANTI_TUNING_GUARD",
            "constant_gm_zero_attempt",
        ),
        (
            "NH3599_9_current_MTS_verdict",
            "current corpus verdict",
            "Current MTS has the exact derivative identities and conditional zero routes, but not parent signatures for global G_eff product silence, Pi_M flux conservation, mu_extra derivative silence, radial no-hair or local Gdot silence.",
            "So 3599 keeps the zero route alive but retains all drift/profile rows as nonclaim bounds.",
            "BOUND_BRANCH_ACTIVE_NO_CLAIM",
            "constant_gm_decision",
        ),
    ]
    stamp = now()
    return [
        {
            "timestamp_utc": stamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "theorem_id": theorem_id,
            "claim_piece": claim_piece,
            "statement": statement,
            "derivation": derivation,
            "status": status,
            "source_path": p[source_id],
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for theorem_id, claim_piece, statement, derivation, status, source_id in rows
    ]


def residual_rows(source_map: dict[str, tuple[Path, str]]) -> list[dict[str, object]]:
    p = {key: str(value[0]) for key, value in source_map.items()}
    rows = [
        ("DHR3599_0_total", "D_X_ln_mu_obs", "D_X ln mu_obs - D_X ln G_eff - D_X ln M_eff - D_X ln(1+epsilon_mu)", "master derivative identity residual; should be algebraically zero", "EXACT_IDENTITY", "derivative_gate"),
        ("DHR3599_1_Geff_product", "D_X_ln_Geff_product", "D_X ln(G_ref w_common ell_J R_frame)", "effective coupling product may drift even if kappa is global", "OPEN_PRODUCT_LOCK_REQUIRED", "kappa_product_lock"),
        ("DHR3599_2_dln_Geff_dt", "dln_Geff_dt", "d ln G_eff/dt", "local Gdot/coupling drift term", "OPEN_SUPERSELECTION_REQUIRED", "time_drift"),
        ("DHR3599_3_dln_Meff_dt", "dln_Meff_dt", "d ln M_eff/dt", "time flux of projected dressed source charge", "OPEN_FLUX_CLOSURE_REQUIRED", "source_flux_closure"),
        ("DHR3599_4_partial_t_epsilon_mu", "partial_t_epsilon_mu", "partial_t epsilon_mu/(1+epsilon_mu)", "time variation of extra-monopole/source-normalization residual", "OPEN_EXTRA_MONOPOLE_REQUIRED", "mu_extra_vector"),
        ("DHR3599_5_partial_r_Geff", "partial_r_ln_Geff", "partial_r ln G_eff", "radial coupling/range/source normalization hair", "OPEN_RANGE_RADIAL_SUPERSELECTION_REQUIRED", "constant_geff_contract"),
        ("DHR3599_6_partial_r_Meff", "partial_r_ln_Meff", "partial_r ln M_eff", "radial flux leakage of projected source charge", "OPEN_RADIAL_FLUX_CLOSURE_REQUIRED", "source_flux_closure"),
        ("DHR3599_7_partial_r_epsilon_mu", "partial_r_epsilon_mu", "partial_r epsilon_mu/(1+epsilon_mu)", "radial extra-monopole or profile hair", "OPEN_PROFILE_BOUND_REQUIRED", "radial_profile"),
        ("DHR3599_8_partial_r_mu_obs", "partial_r_ln_mu_obs", "partial_r ln mu_obs", "observed GM radial hair; direct inverse-square Newton obstruction", "OPEN_RADIAL_NOHAIR_REQUIRED", "radial_profile"),
        ("DHR3599_9_mu_extra_amplitude", "epsilon_mu", "mu_extra/(G_eff M_eff)", "extra boundary/bulk/domain/range/EM/nonEH monopole amplitude", "OPEN_EXTRA_MONOPOLE_AMPLITUDE_REQUIRED", "mu_extra_vector"),
        ("DHR3599_10_range_species_frame", "alpha_lambda_eta_frame", "alpha(lambda)+eta_source_AB+delta_frame_source", "range, species and frame variants of derivative hair", "OPEN_UNIVERSALITY_REQUIRED", "constant_gm_runner_input"),
        ("DHR3599_11_PPN_downstream", "delta_beta_source", "second-order source-normalized PPN residue", "constant GM is first-order only without PPN stability", "DOWNSTREAM_PPN_OPEN", "r11_derivative_vector"),
    ]
    stamp = now()
    return [
        {
            "timestamp_utc": stamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "residual_id": residual_id,
            "symbol": symbol,
            "formula": formula,
            "meaning": meaning,
            "status": status,
            "source_path": p[source_id],
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for residual_id, symbol, formula, meaning, status, source_id in rows
    ]


def bound_rows(source_map: dict[str, tuple[Path, str]]) -> list[dict[str, object]]:
    p = {key: str(value[0]) for key, value in source_map.items()}
    rows = [
        ("DHB3599_0_dln_Geff_dt", "dln_Geff_dt", "d ln G_eff/dt", "yr^-1_or_declared_time^-1", "MISSING_GLOBAL_COUPLING_SUPERSELECTION_OR_DRIFT_BOUND", "prove kappa/G_eff is a global parent coupling and product factors are silent, or fill a sourced local Gdot bound row", "constant_gm_bound_matrix", "BOUND_REQUIRED_CRITICAL"),
        ("DHB3599_1_dln_Meff_dt", "dln_Meff_dt", "d ln M_eff/dt", "yr^-1_or_declared_time^-1", "MISSING_STATIONARY_PROJECTED_SOURCE_FLUX_CLOSURE", "prove d(Pi_M J_H_total)=0 and no timelike boundary flux, or fill source drift row", "source_flux_closure", "BOUND_REQUIRED_CRITICAL"),
        ("DHB3599_2_partial_t_epsilon_mu", "partial_t_epsilon_mu", "partial_t epsilon_mu/(1+epsilon_mu)", "yr^-1_or_declared_time^-1", "MISSING_EXTRA_MONOPOLE_TIME_SILENCE", "mu_extra=0 or parent-fixed universal constant; otherwise separate time derivative of each extra channel", "mu_extra_vector", "BOUND_REQUIRED_CRITICAL"),
        ("DHB3599_3_partial_r_ln_mu_obs", "partial_r_ln_mu_obs", "partial_r ln mu_obs", "length^-1_or_declared_radial_unit", "MISSING_RADIAL_NO_HAIR_OR_PROFILE_BOUND", "prove radial coupling/source/extra-monopole silence, or fill profile envelope relative to measured GM", "radial_profile", "BOUND_REQUIRED_CRITICAL"),
        ("DHB3599_4_partial_r_ln_Geff", "partial_r_ln_Geff", "partial_r ln G_eff", "length^-1_or_declared_radial_unit", "MISSING_RANGE_RADIAL_COUPLING_SUPERSELECTION", "global coupling plus no finite-range/radial running, or source-backed profile", "constant_geff_contract", "BOUND_REQUIRED"),
        ("DHB3599_5_partial_r_ln_Meff", "partial_r_ln_Meff", "partial_r ln M_eff", "length^-1_or_declared_radial_unit", "MISSING_RADIAL_PROJECTED_FLUX_CLOSURE", "closed Pi_M flux over exterior annuli, or radial source hair profile", "source_flux_closure", "BOUND_REQUIRED"),
        ("DHB3599_6_partial_r_epsilon_mu", "partial_r_epsilon_mu", "partial_r epsilon_mu/(1+epsilon_mu)", "length^-1_or_declared_radial_unit", "MISSING_EXTRA_MONOPOLE_RADIAL_SILENCE", "zero/universal mu_extra or component profile rows", "mu_extra_vector", "BOUND_REQUIRED"),
        ("DHB3599_7_epsilon_mu", "epsilon_mu", "mu_extra/(G_eff M_eff)", "dimensionless", "MISSING_ZERO_EXTRA_MONOPOLE_OR_UNIVERSAL_CONSTANT", "row-by-row zero theorem or coefficient vector for boundary/bulk/domain/range/EM/nonEH monopoles", "mu_extra_vector", "BOUND_REQUIRED"),
        ("DHB3599_8_Geff_product", "Geff_product", "D_X ln(G_ref w_common ell_J R_frame)", "per_channel_derivative_units", "MISSING_PRODUCT_FACTOR_SILENCE", "kappa, action-line, source-current normalization and frame factor all parent-silent", "kappa_product_lock", "BOUND_REQUIRED"),
        ("DHB3599_9_alpha_lambda", "alpha(lambda)", "finite-range/radial source-normalization amplitude", "dimensionless_function", "MISSING_NO_RANGE_POLE_OR_ALPHA_CURVE", "no finite-range pole theorem or sourced alpha(lambda) curve", "constant_gm_runner_input", "BOUND_REQUIRED"),
        ("DHB3599_10_no_cancellation_identity", "C_cancel_identity", "D_X ln G_eff + D_X ln M_eff + D_X ln(1+epsilon_mu) == 0 as parent identity", "boolean_or_symbolic_identity", "MISSING_PARENT_CANCELLATION_IDENTITY", "only an action/Ward/superselection identity may cancel derivative terms", "constant_gm_zero_attempt", "GUARD_REQUIRED"),
        ("DHB3599_11_derivative_hair_total", "epsilon_derivative_hair_total", "norm of active dln_Geff_dt, dln_Meff_dt, partial_t epsilon_mu, partial_r ln mu_obs, product/range/frame/species channels", "declared_norm", "NOT_SCORE_READY_TOTAL", "all component zeros or numeric/source-backed bounds with no fitted cancellation", "derivative_bound_3557", "TOTAL_BOUND_BRANCH_ACTIVE"),
    ]
    stamp = now()
    return [
        {
            "timestamp_utc": stamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "bound_id": bound_id,
            "symbol": symbol,
            "formula": formula,
            "units": units,
            "current_value": current_value,
            "required_inputs": required_inputs,
            "source_path": p[source_id],
            "score_status": score_status,
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for bound_id, symbol, formula, units, current_value, required_inputs, source_id, score_status in rows
    ]


def promotion_rows(source_map: dict[str, tuple[Path, str]]) -> list[dict[str, object]]:
    p = {key: str(value[0]) for key, value in source_map.items()}
    rows = [
        ("PROM3599_0_master_identity", "derivative hair decomposition", "PASS_EXACT_IDENTITY", "mu_obs drift splits into G_eff, M_eff and epsilon_mu terms", "derivative_gate"),
        ("PROM3599_1_constant_Geff_claim", "constant G_eff/kappa claim", "FAIL_CURRENT_CLAIM", "global coupling/product-factor silence is conditional but not parent-signed", "constant_geff_contract"),
        ("PROM3599_2_time_hair_claim", "local Gdot/time hair silence", "FAIL_CURRENT_CLAIM", "dln_Geff_dt, dln_Meff_dt and partial_t epsilon_mu remain unsigned", "time_drift"),
        ("PROM3599_3_radial_hair_claim", "radial no-hair/inverse-square source", "FAIL_CURRENT_CLAIM", "partial_r ln mu_obs remains unsigned until coupling/source/extra profiles close", "radial_profile"),
        ("PROM3599_4_no_fitted_cancellation", "no fitted cancellation", "PASS_GUARD", "derivative cancellation only counts as a parent identity", "constant_gm_zero_attempt"),
        ("PROM3599_5_bound_pack", "derivative-hair bound pack complete", "PASS_NONCLAIM", "rows are source-ready but not numeric/score-ready", "derivative_bound_3557"),
        ("PROM3599_6_no_Newton_or_GR_claim", "no Newton/PPN/local-GR promotion", "PASS_GUARD", "constant GM is not promoted and second-order PPN remains downstream", "constant_gm_decision"),
    ]
    stamp = now()
    return [
        {
            "timestamp_utc": stamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "gate_id": gate_id,
            "gate": gate,
            "status": status,
            "consequence": consequence,
            "source_path": p[source_id],
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for gate_id, gate, status, consequence, source_id in rows
    ]


def status_rows(source_map: dict[str, tuple[Path, str]]) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "status": "CONSTANT_GEFF_RADIAL_TIME_HAIR_IDENTITY_DERIVED_BOUNDS_ACTIVE",
            "strongest_result": "3599 derives the exact no-hair accounting identity: every local measured-GM drift or radial profile must come from G_eff/product drift, projected source-flux drift, or extra-monopole epsilon_mu drift. Constant Newtonian GM follows only if all three channels are parent-silent, not by fitted cancellation.",
            "decision": "keep the exact identity and conditional zero routes, retain dln_Geff_dt, dln_Meff_dt, partial_t_epsilon_mu and partial_r_ln_mu_obs as active nonclaim rows, and attack the global kappa/action-line/source-current product lock next",
            "still_missing": "global kappa/G_eff superselection, action-line w_common silence, ell_J source-current normalization silence, same-frame R_frame silence, Pi_M flux conservation, mu_extra zero/universal-constant theorem, radial no-hair profile, time-drift bounds, and second-order PPN stability",
            "public_claim_allowed": False,
            "valid_for_claim": False,
            "source_path": str(source_map["derivative_gate"][0]),
        }
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "next_id": "NEXT3599_0",
            "target_doc": "3600-Y5-R2FR-global-kappa-action-line-superselection-or-Geff-product-bound.md",
            "target_script": "scripts/Y5_R2FR_3600_global_kappa_action_line_superselection_or_Geff_product_bound.py",
            "objective": "try to parent-sign the global kappa/G_eff product lock by proving kappa, w_common, ell_J and R_frame are superselection/source-silent before readout, or retain Geff_product derivative bound rows",
            "success_gate": "constant G_eff may advance only if the whole G_ref*w_common*ell_J*R_frame product is derivative-silent by action grammar/Ward identity, not merely because one symbol kappa is declared constant",
            "reason": "3599 shows local Gdot/radial hair collapses only after the effective coupling product is parent-silent; this is the sharpest next proof target",
            "valid_for_claim": False,
        }
    ]


def validation_rows(
    source_map: dict[str, tuple[Path, str]],
    out_paths: dict[str, Path],
    theorem: list[dict[str, object]],
    residuals: list[dict[str, object]],
    bounds: list[dict[str, object]],
    gates: list[dict[str, object]],
    status: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> list[dict[str, object]]:
    validations: list[tuple[str, bool, str]] = []
    validations.append(("VAL3599_0_sources_exist", all(path.exists() for path, _ in source_map.values()), "all required 3599 source paths exist"))
    validations.append(("VAL3599_1_needles_found", all(path.exists() and contains(path, needle) for path, needle in source_map.values()), "all selected 3599 source anchors found"))
    pre_validation = {key: path for key, path in out_paths.items() if key != "validation"}
    validations.append(("VAL3599_2_outputs_exist", all(path.exists() for path in pre_validation.values()), "all pre-validation 3599 csv output files written"))
    parse_ok = True
    parse_details: list[str] = []
    for output_id, path in pre_validation.items():
        try:
            parse_details.append(f"{output_id}:{len(read_csv(path))}")
        except Exception as exc:
            parse_ok = False
            parse_details.append(f"{output_id}:ERROR:{exc}")
    validations.append(("VAL3599_3_csv_parse", parse_ok, "; ".join(parse_details)))
    validations.append(("VAL3599_4_master_identity_present", any(row["theorem_id"] == "NH3599_1_master_identity" and row["status"] == "EXACT_IDENTITY_DERIVED" for row in theorem), "master derivative identity row present"))
    validations.append(("VAL3599_5_core_bounds_present", {"dln_Geff_dt", "dln_Meff_dt", "partial_t_epsilon_mu", "partial_r_ln_mu_obs"}.issubset({str(row["symbol"]) for row in bounds}), "core time/radial derivative-hair bounds present"))
    validations.append(("VAL3599_6_claims_blocked", all(any(row["gate_id"] == gate_id and row["status"] == "FAIL_CURRENT_CLAIM" for row in gates) for gate_id in ["PROM3599_1_constant_Geff_claim", "PROM3599_2_time_hair_claim", "PROM3599_3_radial_hair_claim"]), "constant G_eff, time hair and radial hair claims are blocked"))
    validations.append(("VAL3599_7_no_fitted_cancellation_guard", any(row["gate_id"] == "PROM3599_4_no_fitted_cancellation" and row["status"] == "PASS_GUARD" for row in gates), "no fitted-cancellation guard present"))
    validations.append(("VAL3599_8_no_claim_flags", not any(str(row.get("valid_for_claim", "False")).lower() == "true" or str(row.get("claim_allowed", "False")).lower() == "true" for table in [theorem, residuals, bounds, gates, status] for row in table), "all generated physics rows remain nonclaim"))
    validations.append(("VAL3599_9_no_Newton_GR_claim", any(row["gate_id"] == "PROM3599_6_no_Newton_or_GR_claim" and row["status"] == "PASS_GUARD" for row in gates), "Newton/PPN/local-GR claim guard is active"))
    validations.append(("VAL3599_10_next_target_selected", any(row["next_id"] == "NEXT3599_0" for row in next_target), "3600 G_eff product-lock target selected"))
    source_paths = [Path(str(row["source_path"])) for table in [theorem, residuals, bounds, gates, status] for row in table if row.get("source_path")]
    validations.append(("VAL3599_11_generated_source_paths_exist", all(path.exists() for path in source_paths), "every generated row source_path exists"))
    formal_hits = []
    if FORMALIZATION.exists():
        for path in FORMALIZATION.rglob("*3599*"):
            if ".venv" in path.parts:
                continue
            if path.name.startswith("3599-") or path.name.startswith("Y5_R2FR_3599") or "P8_Y5_R2FR_3599" in path.name:
                formal_hits.append(path)
    validations.append(("VAL3599_12_formalization_workbench_untouched", len(formal_hits) == 0, "no 3599 checkpoint output appears in formalization-workbench outside package/venv noise"))
    stamp = now()
    return [
        {
            "timestamp_utc": stamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "validation_id": validation_id,
            "passes": passes,
            "status": "PASS" if passes else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
        }
        for validation_id, passes, detail in validations
    ]


def write_doc(theorem, residuals, bounds, gates, status, next_target, validation) -> None:
    lines = [
        "# 3599 - Constant G_eff radial/time hair zero or bound",
        "",
        "## Verdict",
        "3599 derives the exact measured-GM derivative identity: every local time drift or radial profile must be carried by `G_eff`, by the projected dressed source `M_eff`, or by the extra-monopole factor `epsilon_mu`.",
        "",
        "This is useful because it turns the Newtonian-constant question into a finite proof target.  Constant `GM` is not claimed; it is allowed only if the effective coupling product, projected source flux, and extra-monopole channels are parent-silent, or independently bounded without fitted cancellation.",
        "",
        "## No-Hair Theorem Gate",
    ]
    for row in theorem:
        lines.append(f"- `{row['theorem_id']}`: {row['status']} - {row['statement']}")
    lines.extend(["", "## Derivative-Hair Residuals"])
    for row in residuals:
        lines.append(f"- `{row['residual_id']}` / `{row['symbol']}`: {row['status']} - {row['formula']}")
    lines.extend(["", "## Bound Rows"])
    for row in bounds:
        lines.append(f"- `{row['bound_id']}` / `{row['symbol']}`: {row['score_status']} - {row['formula']}")
    lines.extend(["", "## Promotion Gates"])
    for row in gates:
        lines.append(f"- `{row['gate_id']}`: {row['status']} - {row['consequence']}")
    lines.extend(["", "## Status"])
    for row in status:
        lines.append(f"- `{row['status']}`: {row['strongest_result']}")
        lines.append(f"- Decision: {row['decision']}")
        lines.append(f"- Still missing: {row['still_missing']}")
    lines.extend(["", "## Validation"])
    for row in validation:
        lines.append(f"- `{row['validation_id']}`: {row['status']} ({row['detail']})")
    lines.extend(["", "## Next target"])
    for row in next_target:
        lines.append(f"- `{row['next_id']}` -> `{row['target_doc']}`")
        lines.append(f"- Objective: {row['objective']}")
    DOC.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    source_map = sources()
    out_paths = outputs()
    register = source_register_rows(source_map)
    theorem = theorem_rows(source_map)
    residuals = residual_rows(source_map)
    bounds = bound_rows(source_map)
    gates = promotion_rows(source_map)
    status = status_rows(source_map)
    next_target = next_target_rows()

    write_csv(out_paths["source_register"], register)
    write_csv(out_paths["nohair_theorem"], theorem)
    write_csv(out_paths["residuals"], residuals)
    write_csv(out_paths["bound_rows"], bounds)
    write_csv(out_paths["promotion_gates"], gates)
    write_csv(out_paths["status"], status)
    write_csv(out_paths["next_target"], next_target)
    write_csv(out_paths["canonical_status"], status)

    validation = validation_rows(source_map, out_paths, theorem, residuals, bounds, gates, status, next_target)
    write_csv(out_paths["validation"], validation)
    write_doc(theorem, residuals, bounds, gates, status, next_target, validation)

    print(f"wrote {DOC}")
    for output_id, path in out_paths.items():
        print(f"{output_id}: {path}")


if __name__ == "__main__":
    main()
