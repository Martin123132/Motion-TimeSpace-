from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CHECKPOINT_ID = "3598"
BRANCH_ID = "MTS_R2FR_Y5_GAUSS_ORBITAL_CALIBRATION_3598"
DOC = ROOT / "3598-Y5-R2FR-Gauss-orbital-calibration-or-Delta-cal-bound.md"


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
        "next_3597": (
            RESIDUALS / "P8_Y5_R2FR_3597_NEXT_TARGET.csv",
            "NEXT3597_0",
        ),
        "status_3597": (
            RESIDUALS / "P8_Y5_R2FR_3597_STATUS.csv",
            "EM_POYNTING_ONCE_THEOREM",
        ),
        "pg_contract": (
            RESIDUALS / "P8_Hamiltonian_charge_Poisson_Gauss_calibration_CONTRACT.csv",
            "PG7_constant_universal_Geff",
        ),
        "hilbert_monopole_contract": (
            RESIDUALS / "P8_Hilbert_monopole_calibration_CONTRACT.csv",
            "HM3_absolute_monopole_calibration",
        ),
        "constant_geff_contract": (
            RESIDUALS / "P8_constant_universal_Geff_kappa_CONTRACT.csv",
            "CU7_measured_GM_product_silence",
        ),
        "mass_flux_contract": (
            RESIDUALS / "P8_mass_flux_projector_Euler_calibration_CONTRACT.csv",
            "MF5_absolute_calibration",
        ),
        "gauss_chain_523": (
            RESIDUALS / "P8_Y5_GAUSS_ORBITAL_CALIBRATION_CHAIN.csv",
            "CAL523_7_no_derivative_hair",
        ),
        "gauss_formula_523": (
            RESIDUALS / "P8_Y5_GAUSS_ORBITAL_FORMULA_LEDGER.csv",
            "GO523_4_source_normalization_error",
        ),
        "gauss_gates_523": (
            RESIDUALS / "P8_Y5_GAUSS_ORBITAL_ACCEPTANCE_GATES.csv",
            "AG523_5_no_overclaim",
        ),
        "gauss_decision_523": (
            RESIDUALS / "P8_Y5_GAUSS_ORBITAL_DECISION.csv",
            "D523_2_measured_GM_not_derived",
        ),
        "charge_direct": (
            RESIDUALS / "P8_charge_current_equality_DIRECT_ATTEMPT.csv",
            "CC7_closed_flux_and_Gauss_calibration",
        ),
        "charge_residuals": (
            RESIDUALS / "P8_charge_current_equality_RESIDUAL_DECOMPOSITION.csv",
            "Delta_cal",
        ),
        "calibration_lock": (
            RESIDUALS / "P8_CALIBRATION_LOCK_ATTEMPT.csv",
            "C498_cal_0_same_frame",
        ),
        "pg_residual_map": (
            RESIDUALS / "P8_PG_calibration_residual_MAP.csv",
            "PG8_no_derivative_hair",
        ),
        "pg_input_template": (
            RESIDUALS / "P8_PG_calibration_residual_INPUT_TEMPLATE.csv",
            "partial_r_ln_mu_obs",
        ),
        "constant_gm_gate": (
            RESIDUALS / "P8_CONSTANT_GM_DERIVATIVE_HAIR_GATE.csv",
            "CGM0_master_identity",
        ),
        "constant_gm_fill": (
            RESIDUALS / "P8_CONSTANT_GM_DERIVATIVE_HAIR_FILL_QUEUE.csv",
            "CGM2_radial_hair",
        ),
        "mu_extra_vector": (
            RESIDUALS / "P8_mu_extra_over_Geff_Meff_vector.csv",
            "EMV3501_10_em_poynting_hilbert_dressing",
        ),
        "newton_stack": (
            RESIDUALS / "P8_source_normalized_Newton_branch_STACK.csv",
            "SN9_orbital_inverse_square_readout",
        ),
        "local_residual_template": (
            RESIDUALS / "MTS_local_residual_predictions_TEMPLATE.csv",
            "R9_Gdot",
        ),
    }


def outputs() -> dict[str, Path]:
    return {
        "source_register": RESIDUALS / "P8_Y5_R2FR_3598_SOURCE_REGISTER.csv",
        "calibration_theorem": RESIDUALS / "P8_Y5_R2FR_3598_GAUSS_ORBITAL_CALIBRATION_THEOREM.csv",
        "delta_cal_residuals": RESIDUALS / "P8_Y5_R2FR_3598_DELTA_CAL_RESIDUAL_DECOMPOSITION.csv",
        "bound_rows": RESIDUALS / "P8_Y5_R2FR_3598_GAUSS_ORBITAL_BOUND_ROWS.csv",
        "promotion_gates": RESIDUALS / "P8_Y5_R2FR_3598_PROMOTION_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3598_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3598_NEXT_TARGET.csv",
        "canonical_status": RESIDUALS / "P8_Y5_Gauss_orbital_calibration_status.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3598_VALIDATION.csv",
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
            "GOC3598_0_target",
            "3598 target",
            "Connect M_source^dress[W;tau]=ell_M(Pi_M J_H_total) to Poisson/Gauss/orbital measured GM, or retain Delta_cal, partial_r ln mu_obs and d ln G_eff/dt bounds.",
            "3597 made source accounting precise; this gate asks whether that source is the thing slow bodies orbit.",
            "TARGET_IMPORTED",
            "next_3597",
        ),
        (
            "GOC3598_1_source_monopole_input",
            "source monopole input",
            "mu_parent := G_eff M_H[Pi_M J_H_total] with M_H already dressed by matter, EM/Poynting, binding and permitted boundary terms.",
            "This imports the non-cheat source definition but does not yet make it an observed orbital mass.",
            "SOURCE_INPUT_IMPORTED",
            "status_3597",
        ),
        (
            "GOC3598_2_weak_field_Poisson_bridge",
            "weak-field Poisson bridge",
            "If the same observed frame is used and the local exterior operator is EH at leading order, g_00=-1-2 Phi/c^2 gives nabla^2 Phi=4 pi G_eff rho_H + R_Poisson.",
            "The first real Newton bridge is not a galaxy fit; it is the coefficient and source match in the weak-field 00 equation.",
            "CONDITIONAL_POISSON_DERIVATION",
            "pg_contract",
        ),
        (
            "GOC3598_3_Gauss_surface_bridge",
            "Gauss surface bridge",
            "For any enclosing surface S, mu_Gauss(S) := (1/4 pi) integral_S grad Phi dot dS = G_eff M_H(enclosed) + Delta_Gauss.",
            "Gauss turns the field equation into a monopole charge only when residual volume, boundary, non-EH, range and domain pieces vanish or are retained.",
            "CONDITIONAL_GAUSS_DERIVATION",
            "gauss_formula_523",
        ),
        (
            "GOC3598_4_orbital_readout_bridge",
            "slow-orbit readout bridge",
            "For a slow nearly circular observed-frame test body, mu_obs(r) := r^2 |a_r| = v^2 r = mu_Gauss + Delta_orbit when finite-range, direct-force, frame, multipole and radial-hair corrections are absent.",
            "This is the point where the theory becomes Newtonian mechanics rather than only an internal source identity.",
            "CONDITIONAL_ORBITAL_DERIVATION",
            "newton_stack",
        ),
        (
            "GOC3598_5_exact_Delta_cal_identity",
            "Delta_cal identity",
            "Delta_cal := mu_obs - G_eff M_H[Pi_M J_H_total] = Delta_Poisson + Delta_Gauss + Delta_orbit + mu_extra + Delta_frame + Delta_G + Delta_flux + Delta_range + Delta_PPN_source.",
            "This is the hard accounting law: no residual may be hidden inside the phrase measured GM.",
            "EXACT_RESIDUAL_DECOMPOSITION",
            "charge_residuals",
        ),
        (
            "GOC3598_6_derivative_hair_identity",
            "derivative hair identity",
            "For X in {t,r,A,lambda,frame,domain}, D_X ln mu_obs = D_X ln G_eff + D_X ln M_H + D_X ln(1+epsilon_cal), where epsilon_cal=Delta_cal/(G_eff M_H).",
            "A cancellation only counts if a parent identity forces it; fitted cancellations are not Newtonian reduction.",
            "EXACT_DERIVATIVE_IDENTITY",
            "constant_gm_gate",
        ),
        (
            "GOC3598_7_conditional_calibration_theorem",
            "Gauss/orbital calibration theorem",
            "If the source charge is parent-owned, the weak-field operator is EH with standard coefficient, Gauss residuals vanish, slow bodies read the same Phi as inverse-square acceleration, mu_extra=0, G_eff is constant/universal, derivative hair is silent, and first-order normalization is PPN-stable, then Delta_cal=0 and mu_obs=G_eff M_H[Pi_M J_H_total].",
            "This is the clean conditional route from MTS source coupling to Newtonian GM.",
            "CONDITIONAL_ZERO_THEOREM_DERIVED",
            "gauss_chain_523",
        ),
        (
            "GOC3598_8_current_MTS_verdict",
            "current corpus verdict",
            "Current MTS has the calibration chain but not the proof: Delta_cal, partial_r ln mu_obs, d ln G_eff/dt, d ln M_eff/dt, mu_extra, frame split, range dependence, and PPN source stability remain active nonclaim rows.",
            "So 3598 narrows the route to Newton/GR, but does not promote local-GR/Newton/PPN.",
            "BOUND_BRANCH_ACTIVE_NO_CLAIM",
            "gauss_decision_523",
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
        ("DCR3598_0_total", "Delta_cal_total", "mu_obs - G_eff M_H[Pi_M J_H_total]", "total mismatch between dressed Hilbert source and observed orbital GM", "ACTIVE_NONCLAIM", "charge_residuals"),
        ("DCR3598_1_source_charge", "Delta_charge", "B_xi/G_eff - M_H[Pi_M J_H_total]", "boundary/Hamiltonian charge may not equal the projected Hilbert source", "INHERITED_OPEN", "charge_direct"),
        ("DCR3598_2_Poisson", "Delta_Poisson", "nabla^2 Phi - 4 pi G_eff rho_H", "weak-field source coefficient or local operator differs from EH/Poisson", "OPEN_OPERATOR_COEFFICIENT_REQUIRED", "pg_contract"),
        ("DCR3598_3_Gauss", "Delta_Gauss", "mu_Gauss(S) - G_eff M_H(enclosed)", "surface flux has residual volume, boundary, domain, range, memory or non-EH terms", "OPEN_GAUSS_SURFACE_REQUIRED", "gauss_formula_523"),
        ("DCR3598_4_orbit", "Delta_orbit", "mu_obs(r)-mu_Gauss(S_r)", "slow observed bodies may not read a pure inverse-square monopole", "OPEN_ORBITAL_READOUT_REQUIRED", "newton_stack"),
        ("DCR3598_5_mu_extra", "mu_extra", "mu_extra_boundary_bulk_domain + mu_extra_range + mu_extra_projector + mu_extra_EM + mu_extra_nonEH", "unowned sectors shift the monopole source", "OPEN_EXTRA_MASS_REQUIRED", "mu_extra_vector"),
        ("DCR3598_6_constant_Geff", "Delta_G", "D_X ln G_eff or G_eff-G0", "coupling normalization may drift with time, range, species, frame or domain", "OPEN_COUPLING_SUPERSELECTION_REQUIRED", "constant_geff_contract"),
        ("DCR3598_7_flux", "Delta_flux", "integral_annulus d(Pi_M J_H_total)", "projected source mass may drift with radius or time", "OPEN_FLUX_CLOSURE_REQUIRED", "mass_flux_contract"),
        ("DCR3598_8_radial_hair", "partial_r_ln_mu_obs", "partial_r ln mu_obs", "observed GM may be radius-dependent rather than a Newtonian monopole", "OPEN_RADIAL_NO_HAIR_REQUIRED", "constant_gm_fill"),
        ("DCR3598_9_time_hair", "dln_Geff_dt_plus_dln_Meff_dt", "d ln mu_obs/dt = d ln G_eff/dt + d ln M_eff/dt + d ln(1+epsilon_cal)/dt", "local Gdot silence requires separate coupling/source/calibration silence", "OPEN_TIME_DRIFT_REQUIRED", "constant_gm_gate"),
        ("DCR3598_10_frame_species_range", "Delta_frame_species_range", "delta_frame_source + eta_source_AB + alpha(lambda)", "source normalization may depend on frame, species or range", "OPEN_UNIVERSALITY_REQUIRED", "pg_input_template"),
        ("DCR3598_11_PPN", "Delta_PPN_source", "(gamma-1,beta-1,alpha1,alpha2,alpha3,xi)_source", "first-order Newton calibration does not automatically prove local GR", "DOWNSTREAM_PPN_OPEN", "local_residual_template"),
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
        ("GOB3598_0_epsilon_Delta_cal", "epsilon_Delta_cal", "abs(mu_obs-G_eff M_H[Pi_M J_H_total])/abs(G_eff M_H)", "dimensionless", "CONDITIONAL_ZERO_IF_ALL_CALIBRATION_PREMISES_SIGNED", "source-charge equality; EH Poisson coefficient; Gauss residual zero; inverse-square orbit readout; mu_extra=0; G_eff constant; derivative hair zero; PPN stability", "charge_residuals", "BOUND_REQUIRED_CRITICAL"),
        ("GOB3598_1_epsilon_Poisson", "epsilon_Poisson", "norm(nabla^2 Phi-4 pi G_eff rho_H)/norm(4 pi G_eff rho_H)", "dimensionless_or_declared_norm", "MISSING_EH_WEAK_FIELD_OPERATOR_COEFFICIENT", "same-frame EH leading operator or source-backed non-EH coefficient vector", "pg_contract", "BOUND_REQUIRED"),
        ("GOB3598_2_epsilon_Gauss", "epsilon_Gauss", "abs(mu_Gauss-G_eff M_H)/abs(G_eff M_H)", "dimensionless", "MISSING_GAUSS_SURFACE_RESIDUAL_ZERO", "surface integral residual, boundary/domain/range/non-EH terms zero or bounded", "gauss_formula_523", "BOUND_REQUIRED"),
        ("GOB3598_3_epsilon_orbit", "epsilon_orbit", "abs(mu_obs-mu_Gauss)/abs(mu_Gauss)", "dimensionless", "MISSING_SLOW_ORBIT_INVERSE_SQUARE_READOUT", "same observed Phi, no direct fifth force, finite-range correction, frame split, or active multipole/radial hair", "newton_stack", "BOUND_REQUIRED"),
        ("GOB3598_4_epsilon_mu_extra", "epsilon_mu_extra", "abs(mu_extra)/(abs(G_eff M_H))", "dimensionless", "MISSING_ZERO_EXTRA_MONOPOLE", "boundary, bulk, domain, memory, range, connection, projector, non-EH and EM extra channels zero or bounded", "mu_extra_vector", "BOUND_REQUIRED_CRITICAL"),
        ("GOB3598_5_dln_Geff_dt", "dln_Geff_dt", "d ln G_eff/dt", "yr^-1_or_declared_time^-1", "MISSING_COUPLING_SUPERSELECTION_OR_DRIFT_BOUND", "parent global coupling/superselection theorem or sourced local Gdot row", "constant_geff_contract", "BOUND_REQUIRED"),
        ("GOB3598_6_dln_Meff_dt", "dln_Meff_dt", "d ln M_H[Pi_M J_H_total]/dt", "yr^-1_or_declared_time^-1", "MISSING_PROJECTED_SOURCE_FLUX_CONSERVATION", "stationary/closed Pi_M flux theorem or sourced drift row", "mass_flux_contract", "BOUND_REQUIRED"),
        ("GOB3598_7_partial_r_ln_mu_obs", "partial_r_ln_mu_obs", "partial_r ln mu_obs", "length^-1_or_declared_radial_unit", "MISSING_RADIAL_NO_HAIR_OR_PROFILE_BOUND", "Gauss exterior/no-hair theorem or profile envelope relative to measured GM", "constant_gm_fill", "BOUND_REQUIRED_CRITICAL"),
        ("GOB3598_8_eta_source_AB", "eta_source_AB", "source/test species derivative of mu_obs", "dimensionless", "MISSING_SOURCE_SIDE_UNIVERSALITY", "source-charge WEP theorem or residual below local source lock", "pg_input_template", "BOUND_REQUIRED"),
        ("GOB3598_9_alpha_lambda", "alpha(lambda)", "finite-range/source-normalization Yukawa amplitude curve", "dimensionless_function", "MISSING_RANGE_INDEPENDENCE_OR_ALPHA_BOUND", "no-pole/range-zero theorem or source-backed alpha(lambda) curve", "pg_input_template", "BOUND_REQUIRED"),
        ("GOB3598_10_delta_frame_source", "delta_frame_source", "frame/source pullback mismatch in mu_obs", "dimensionless", "MISSING_SAME_FRAME_SOURCE_ORBIT_PULLBACK", "same observed coframe for source variation, matter, clocks and orbits", "calibration_lock", "BOUND_REQUIRED"),
        ("GOB3598_11_delta_beta_source", "delta_beta_source", "second-order source-normalized PPN beta/gamma residue", "dimensionless", "MISSING_SECOND_ORDER_SOURCE_STABILITY", "after first-order GM calibration, beta/gamma/preferred-frame vector zero or below bounds", "local_residual_template", "BOUND_REQUIRED_DOWNSTREAM"),
        ("GOB3598_12_epsilon_calibration_total", "epsilon_calibration_total", "sum of epsilon_Delta_cal, epsilon_Poisson, epsilon_Gauss, epsilon_orbit, epsilon_mu_extra, derivative hair, frame/species/range and PPN source residuals", "dimensionless_or_declared_norm", "NOT_SCORE_READY_TOTAL", "all component zeros or numeric/source-backed bounds with no fitted cancellation", "gauss_gates_523", "TOTAL_BOUND_BRANCH_ACTIVE"),
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
        ("PROM3598_0_calibration_theorem", "Gauss/orbital calibration theorem", "PASS_CONDITIONAL_THEOREM", "Delta_cal is zero only if the full source-to-Poisson-to-Gauss-to-orbit chain closes", "gauss_chain_523"),
        ("PROM3598_1_measured_GM_claim", "mu_obs = G_eff M_H claim", "FAIL_CURRENT_CLAIM", "Delta_cal, mu_extra, derivative hair, constant G_eff, inverse-square readout and PPN stability remain unsigned", "gauss_decision_523"),
        ("PROM3598_2_derivative_hair_visible", "dln_Geff_dt and partial_r_ln_mu_obs", "PASS_GUARD", "time/radial hair rows are explicit and cannot be hidden inside measured GM", "constant_gm_gate"),
        ("PROM3598_3_no_fitted_cancellation", "no cancellation by tuning", "PASS_GUARD", "cancellation counts only if parent identity forces it", "constant_gm_gate"),
        ("PROM3598_4_bound_pack", "calibration bound pack complete", "PASS_NONCLAIM", "rows are source-ready but not numeric/score-ready", "pg_input_template"),
        ("PROM3598_5_no_Newton_or_GR_claim", "no Newton/PPN/local-GR promotion", "PASS_GUARD", "this is a conditional route, not a local-GR pass", "gauss_gates_523"),
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
            "status": "GAUSS_ORBITAL_CALIBRATION_THEOREM_CONDITIONAL_DELTA_CAL_BOUND_ACTIVE",
            "strongest_result": "3598 derives the exact bridge required for Newtonian mechanics: a dressed Hilbert source becomes observed orbital GM only through same-frame Poisson, Gauss surface flux, inverse-square slow-orbit readout, zero extra monopoles, constant universal G_eff, derivative-hair silence, and PPN source stability.",
            "decision": "retain the conditional theorem, keep Delta_cal and derivative-hair rows as nonclaim bounds, and attack the constant-G_eff / radial-time-hair gate next",
            "still_missing": "EH weak-field coefficient, Gauss residual zero, inverse-square orbit readout, zero mu_extra, G_eff superselection, Pi_M flux conservation, partial_r ln mu_obs silence, dln_Geff_dt/dln_Meff_dt silence, source universality, range independence, frame pullback, and second-order PPN source stability",
            "public_claim_allowed": False,
            "valid_for_claim": False,
            "source_path": str(source_map["gauss_chain_523"][0]),
        }
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "next_id": "NEXT3598_0",
            "target_doc": "3599-Y5-R2FR-constant-Geff-radial-time-hair-zero-or-bound.md",
            "target_script": "scripts/Y5_R2FR_3599_constant_Geff_radial_time_hair_zero_or_bound.py",
            "objective": "try to prove the constant universal G_eff/kappa superselection and radial/time derivative silence for mu_obs, or fill dln_Geff_dt, dln_Meff_dt, partial_t_epsilon_mu and partial_r_ln_mu_obs bound rows",
            "success_gate": "Newtonian calibration may advance only if coupling/source derivative hair is parent-zero, or each drift/profile channel has sourced numeric bounds without cancellation by fit",
            "reason": "3598 shows Delta_cal collapses only after constant coupling and derivative-hair silence; that is now the shortest route toward a source-normalized Newton branch",
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
    validations.append(("VAL3598_0_sources_exist", all(path.exists() for path, _ in source_map.values()), "all required 3598 source paths exist"))
    validations.append(("VAL3598_1_needles_found", all(path.exists() and contains(path, needle) for path, needle in source_map.values()), "all selected 3598 source anchors found"))
    pre_validation = {key: path for key, path in out_paths.items() if key != "validation"}
    validations.append(("VAL3598_2_outputs_exist", all(path.exists() for path in pre_validation.values()), "all pre-validation 3598 csv output files written"))
    parse_ok = True
    parse_details: list[str] = []
    for output_id, path in pre_validation.items():
        try:
            parse_details.append(f"{output_id}:{len(read_csv(path))}")
        except Exception as exc:
            parse_ok = False
            parse_details.append(f"{output_id}:ERROR:{exc}")
    validations.append(("VAL3598_3_csv_parse", parse_ok, "; ".join(parse_details)))
    validations.append(("VAL3598_4_calibration_theorem_present", any(row["theorem_id"] == "GOC3598_7_conditional_calibration_theorem" and row["status"] == "CONDITIONAL_ZERO_THEOREM_DERIVED" for row in theorem), "Gauss/orbital conditional calibration theorem row present"))
    validations.append(("VAL3598_5_Delta_cal_explicit", any(row["symbol"] == "Delta_cal_total" for row in residuals) and any(row["symbol"] == "epsilon_Delta_cal" for row in bounds), "Delta_cal residual and bound rows are explicit"))
    validations.append(("VAL3598_6_derivative_hair_explicit", {"dln_Geff_dt", "dln_Meff_dt", "partial_r_ln_mu_obs"}.issubset({str(row["symbol"]) for row in bounds}), "time/radial derivative hair rows present"))
    validations.append(("VAL3598_7_claim_blocked", any(row["gate_id"] == "PROM3598_1_measured_GM_claim" and row["status"] == "FAIL_CURRENT_CLAIM" for row in gates), "current measured-GM calibration claim is blocked"))
    validations.append(("VAL3598_8_no_claim_flags", not any(str(row.get("valid_for_claim", "False")).lower() == "true" or str(row.get("claim_allowed", "False")).lower() == "true" for table in [theorem, residuals, bounds, gates, status] for row in table), "all generated physics rows remain nonclaim"))
    validations.append(("VAL3598_9_no_Newton_GR_claim", any(row["gate_id"] == "PROM3598_5_no_Newton_or_GR_claim" and row["status"] == "PASS_GUARD" for row in gates), "Newton/PPN/local-GR claim guard is active"))
    validations.append(("VAL3598_10_no_fitted_cancellation_guard", any(row["gate_id"] == "PROM3598_3_no_fitted_cancellation" and row["status"] == "PASS_GUARD" for row in gates), "no fitted-cancellation guard present"))
    validations.append(("VAL3598_11_next_target_selected", any(row["next_id"] == "NEXT3598_0" for row in next_target), "3599 constant G_eff/radial-time hair target selected"))
    source_paths = [Path(str(row["source_path"])) for table in [theorem, residuals, bounds, gates, status] for row in table if row.get("source_path")]
    validations.append(("VAL3598_12_generated_source_paths_exist", all(path.exists() for path in source_paths), "every generated row source_path exists"))
    formal_hits = []
    if FORMALIZATION.exists():
        for path in FORMALIZATION.rglob("*3598*"):
            if ".venv" in path.parts:
                continue
            if path.name.startswith("3598-") or path.name.startswith("Y5_R2FR_3598") or "P8_Y5_R2FR_3598" in path.name:
                formal_hits.append(path)
    validations.append(("VAL3598_13_formalization_workbench_untouched", len(formal_hits) == 0, "no 3598 checkpoint output appears in formalization-workbench outside package/venv noise"))
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
        "# 3598 - Gauss/orbital calibration or Delta_cal bound",
        "",
        "## Verdict",
        "3598 derives the exact conditional bridge from dressed Hilbert source to measured Newtonian `GM`: source charge must pass through the same-frame weak-field Poisson equation, Gauss surface flux, and slow inverse-square orbital readout.",
        "",
        "This is the key discipline point: `M_source^dress` is not automatically what planets feel.  It becomes `mu_obs=G_eff M_H` only when `Delta_cal=0` and the derivative-hair channels are silent by theorem or bounded with real rows.",
        "",
        "## Calibration Theorem Gate",
    ]
    for row in theorem:
        lines.append(f"- `{row['theorem_id']}`: {row['status']} - {row['statement']}")
    lines.extend(["", "## Delta_cal Residuals"])
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
    write_csv(out_paths["calibration_theorem"], theorem)
    write_csv(out_paths["delta_cal_residuals"], residuals)
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
