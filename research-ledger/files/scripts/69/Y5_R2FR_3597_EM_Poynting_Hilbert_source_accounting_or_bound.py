from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CHECKPOINT_ID = "3597"
BRANCH_ID = "MTS_R2FR_Y5_EM_POYNTING_HILBERT_SOURCE_ACCOUNTING_3597"
DOC = ROOT / "3597-Y5-R2FR-EM-Poynting-Hilbert-source-accounting-or-bound.md"


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
        "next_3596": (
            RESIDUALS / "P8_Y5_R2FR_3596_NEXT_TARGET.csv",
            "NEXT3596_0",
        ),
        "status_3596": (
            RESIDUALS / "P8_Y5_R2FR_3596_STATUS.csv",
            "QM_LABEL_CONDITIONALLY_ZERO",
        ),
        "lock_3596": (
            RESIDUALS / "P8_Y5_R2FR_3596_WORLDTUBE_HILBERT_SOURCE_MEASURE_LOCK.csv",
            "WSL3596_4_EM_once",
        ),
        "inputs_3596": (
            RESIDUALS / "P8_Y5_R2FR_3596_QM_WORLD_TUBE_EM_INPUT_ROWS.csv",
            "epsilon_EM_once",
        ),
        "em_hodge_owner": (
            RESIDUALS / "P8_EM_Hodge_Maxwell_current_owner_bound_vector.csv",
            "EMB3503_4_Phi_EM_rad",
        ),
        "em_poynting_components": (
            RESIDUALS / "P8_EM_Poynting_source_flux_or_cross_term_vector.csv",
            "EMF3502_1_radiative_poynting_flux",
        ),
        "em_hodge_flow": (
            RESIDUALS / "P8_EM_Hodge_flow_rule_bound_or_zero.csv",
            "DHB3504_0_Delta_Hodge_EM",
        ),
        "maxwell_poynting_ledger": (
            RESIDUALS / "P8_Y5_R2FR_3463_MAXWELL_POYNTING_STRESS_LEDGER.csv",
            "Poynting",
        ),
        "em_owner_audit": (
            RESIDUALS / "P8_Y5_R2FR_3465_EM_OWNER_PACKAGE_AUDIT.csv",
            "F^2",
        ),
        "em_alpha_owner": (
            RESIDUALS / "P8_Y5_R2FR_3464_EM_ALPHA_CHARGE_OWNER_AUDIT.csv",
            "alpha",
        ),
        "em_current_source": (
            RESIDUALS / "P8_EM_current_source_Ward_alpha_source_residual.csv",
            "CSR3508_4_postvariation_rescaling",
        ),
        "em_ellj_law": (
            RESIDUALS / "P8_EM_ellJ_source_current_owner_residual_law.csv",
            "EJR3513_6_R_W",
        ),
        "q_map": (
            RESIDUALS / "P8_EM_actual_q_map_vertical_basis_candidate.csv",
            "QMAP3517_8_projector_readout",
        ),
        "kappa_gref_lock": (
            RESIDUALS / "P8_EM_fixed_kappa_Gref_action_line_lock.csv",
            "KGLR3511_2_delta_ellJ",
        ),
        "source_current_closure": (
            RESIDUALS / "P8_Y5_SOURCE_CURRENT_CLOSURE_THEOREM_ATTEMPT.csv",
            "SC532_7_measured_GM_next_gate",
        ),
        "worldtube_glue": (
            RESIDUALS / "P8_Y5_HILBERT_WORLDTUBE_GLUE_THEOREM_ATTEMPT.csv",
            "Pi_M",
        ),
        "source_measure_flux": (
            RESIDUALS / "P8_SOURCE_MEASURE_MEFF_FLUX_THEOREM.csv",
            "M_eff",
        ),
        "charge_direct": (
            RESIDUALS / "P8_charge_current_equality_DIRECT_ATTEMPT.csv",
            "CC7_closed_flux_and_Gauss_calibration",
        ),
        "charge_residuals": (
            RESIDUALS / "P8_charge_current_equality_RESIDUAL_DECOMPOSITION.csv",
            "Delta_cal",
        ),
    }


def outputs() -> dict[str, Path]:
    return {
        "source_register": RESIDUALS / "P8_Y5_R2FR_3597_SOURCE_REGISTER.csv",
        "em_once_theorem": RESIDUALS / "P8_Y5_R2FR_3597_EM_POYNTING_ONCE_THEOREM.csv",
        "residuals": RESIDUALS / "P8_Y5_R2FR_3597_EM_SOURCE_ACCOUNTING_RESIDUALS.csv",
        "bound_rows": RESIDUALS / "P8_Y5_R2FR_3597_EM_ONCE_BOUND_ROWS.csv",
        "promotion_gates": RESIDUALS / "P8_Y5_R2FR_3597_PROMOTION_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3597_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3597_NEXT_TARGET.csv",
        "canonical_status": RESIDUALS / "P8_Y5_EM_Poynting_Hilbert_source_accounting_status.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3597_VALIDATION.csv",
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
            "EMT3597_0_target",
            "3597 target",
            "Prove that EM stress, Poynting flux, and binding energy enter J_H_total exactly once in the source-measure branch, or retain epsilon_EM_once and Phi_EM_rad bounds.",
            "3596 made EM/Poynting/binding once-only accounting the next critical guard.",
            "TARGET_IMPORTED",
            "next_3596",
        ),
        (
            "EMT3597_1_visible_Maxwell_Hilbert_stress",
            "visible Maxwell Hilbert stress",
            "For S_EM=-1/4 integral sqrt(-g_obs) w_EM F_ab F^ab, variation before readout gives T_EM^{mu nu}=w_EM(F^{mu alpha}F^nu_alpha-1/4 g_obs^{mu nu}F^2) in the chosen sign convention.",
            "This puts bound-field EM energy inside the same Hilbert source object as matter, provided the Hodge/coframe and w_EM are parent-owned.",
            "CONDITIONAL_STRESS_DERIVED",
            "maxwell_poynting_ledger",
        ),
        (
            "EMT3597_2_Poynting_balance",
            "Poynting balance",
            "D_tau E_EM[V] + integral_boundary S_Poynting dot n dA = - integral_V J dot E + improvement/boundary terms.",
            "Matter-only energy is not conserved because Lorentz exchange moves energy between matter and EM; the total matter+EM Hilbert source is the conserved object.",
            "CONDITIONAL_BALANCE_DERIVED",
            "em_poynting_components",
        ),
        (
            "EMT3597_3_no_omission",
            "no zero-times EM source",
            "If Phi_EM_rad is nonzero, the local source charge has time/boundary hair unless Phi_EM_rad is included in M_source^dress or bounded over the stated window.",
            "A stationary isolated local branch may set net exterior Poynting flux to zero; a radiative/background branch may not hide it.",
            "POYNTING_FLUX_EXPLICIT_GUARD",
            "em_hodge_owner",
        ),
        (
            "EMT3597_4_no_double_count",
            "no twice-counted binding source",
            "EM binding energy cannot be counted once inside dressed matter mass and again as an independent topological/source charge.",
            "The dressed source must be a single functional M_source^dress[W;tau]=ell_M(Pi_M J_H_total), not a matter mass plus an extra fitted EM patch.",
            "DOUBLE_COUNT_GUARD",
            "lock_3596",
        ),
        (
            "EMT3597_5_same_owner_requirements",
            "same owner requirements",
            "The same q/e_obs/tau branch must own the EM Hodge star, charge/current normalization, Maxwell action scale, Hilbert variation, Pi_M projection, and readout ordering.",
            "Otherwise EM can re-enter through Hodge drift, w_EM, C_XF2, C_JQ, readout regeneration, or Delta_J_total.",
            "OWNER_PREMISES_LISTED",
            "em_hodge_flow",
        ),
        (
            "EMT3597_6_conditional_theorem",
            "EM/Poynting once-only theorem",
            "If Delta_Hodge_EM=0, w_EM=1, C_XF2=0, C_JQ=0, C_EM_readout=0, Delta_J_total=0, Pi_M is parent-fixed, exact improvements are boundary-silent, and Phi_EM_rad is zero or explicitly included, then epsilon_EM_once=0.",
            "This is the clean route: Poynting is not ignored, it is the boundary flux term of the same Hilbert source accounting.",
            "CONDITIONAL_ZERO_THEOREM_DERIVED",
            "em_hodge_owner",
        ),
        (
            "EMT3597_7_current_MTS_verdict",
            "current corpus verdict",
            "Current MTS has a viable accounting law but not a parent-signed EM once-only proof: Delta_Hodge_EM, w_EM, C_XF2, C_JQ, Phi_EM_rad, C_EM_readout, Delta_J_total, and exact-improvement silence remain active nonclaim rows.",
            "So the branch moves from vague source coupling to a concrete checklist; it does not yet promote Newton/PPN/local-GR.",
            "BOUND_BRANCH_ACTIVE_NO_CLAIM",
            "inputs_3596",
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
        ("EMR3597_0_total", "R_EM_once_total", "Pi_M[J_H_total - J_matter - J_EM - J_Poynting - J_binding - dB_impr]", "total once-only EM/Poynting/source-accounting mismatch", "ACTIVE_NONCLAIM", "lock_3596"),
        ("EMR3597_1_Hodge", "R_Delta_Hodge_EM", "Delta_Hodge_EM = *_EM - *_obs[e_obs(q)] or chi_EM - chi_obs", "EM flux/stress may source a different effective geometry than the observed gravitational coframe", "OPEN_PARENT_SIGNATURE_REQUIRED", "em_hodge_flow"),
        ("EMR3597_2_wEM", "R_w_EM", "w_EM - 1", "independent Maxwell stress multiplier rescales EM source contribution", "OPEN_NORMALIZATION_REQUIRED", "em_hodge_owner"),
        ("EMR3597_3_XF2", "R_C_XF2", "C_XF2 hidden-visible F^2/F*F operator", "nonminimal hidden/motion/time EM coupling regenerates source, clock, WEP and alpha residuals", "OPEN_OPERATOR_DOMAIN_REQUIRED", "em_owner_audit"),
        ("EMR3597_4_CJQ", "R_C_JQ", "C_JQ charge/current normalization drift", "A/J normalization ambiguity shifts Lorentz exchange and EM stress scale", "OPEN_CHARGE_CURRENT_OWNER_REQUIRED", "em_alpha_owner"),
        ("EMR3597_5_PhiEM", "R_Phi_EM_rad", "Phi_EM_rad = integral_boundary S_Poynting dot n dA", "radiative/background EM flux changes the local source charge unless zero or included", "OPEN_FLUX_ZERO_OR_BOUND_REQUIRED", "em_poynting_components"),
        ("EMR3597_6_readout", "R_C_EM_readout", "C_EM_readout effective post-reduction EM coefficient", "readout or loop closure can reintroduce EM response after a parent-level zero", "OPEN_READOUT_CLOSURE_REQUIRED", "em_current_source"),
        ("EMR3597_7_DeltaJ", "R_Delta_J_total", "dJ_H_total - 0 = Delta_nonEH + Delta_frame + Delta_extra + Delta_boundary + Delta_radiative", "total Hilbert current closure is not parent-signed", "OPEN_CURRENT_CLOSURE_REQUIRED", "source_current_closure"),
        ("EMR3597_8_double_count", "R_EM_double_count", "M_matter^dress + M_EM^separate - M_source^dress[J_H_total]", "binding/field energy may be counted twice if source mass is assembled after readout", "OPEN_ANTI_TAUTOLOGY_GUARD", "em_current_source"),
        ("EMR3597_9_improvement", "R_dB_improvement", "integral_boundary dB_impr or stress improvement flux", "exact/improvement stress terms must vanish on the chosen boundary or remain as source rows", "OPEN_BOUNDARY_SILENCE_REQUIRED", "em_ellj_law"),
        ("EMR3597_10_calibration_downstream", "R_Gauss_orbital_calibration", "M_source^dress[J_H_total] - M_Gauss_orbital", "once-only source accounting is necessary but still not a Newton/GR reduction without Gauss/orbital calibration", "DOWNSTREAM_OPEN", "charge_residuals"),
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
        ("EMB3597_0_epsilon_EM_once", "epsilon_EM_once", "abs(Pi_M[J_H_total-J_matter-J_EM-J_Poynting-J_binding-dB_impr])/abs(M_H_ref)", "dimensionless", "CONDITIONAL_ZERO_IF_ALL_OWNER_PREMISES_SIGNED", "Delta_Hodge_EM=0; w_EM=1; C_XF2=0; C_JQ=0; C_EM_readout=0; Delta_J_total=0; Phi_EM_rad zero/included; no double count; boundary improvements silent", "em_hodge_owner", "BOUND_REQUIRED_CRITICAL"),
        ("EMB3597_1_epsilon_Hodge_EM", "epsilon_Hodge_EM", "norm(*_EM-*_obs[e_obs(q)]) or norm(chi_EM-chi_obs)", "dimensionless_or_tensor", "MISSING_PARENT_OBSERVED_HODGE_SIGNATURE", "parent q/e_obs derivation of EM Hodge star or component bounds for principal/skewon/axion/disformal/readout pieces", "em_hodge_flow", "BOUND_REQUIRED"),
        ("EMB3597_2_epsilon_w_EM", "epsilon_w_EM", "abs(w_EM-1)", "dimensionless", "MISSING_UNIQUE_MAXWELL_ACTION_NORMALIZATION", "unique visible Maxwell F^2 norm and alpha/charge-current owner before readout", "em_hodge_owner", "BOUND_REQUIRED"),
        ("EMB3597_3_epsilon_XF2", "epsilon_XF2", "norm(C_XF2) with declared operator normalization", "model_dependent", "MISSING_OPERATOR_DOMAIN_EXCLUSION_OR_BOUND", "exclude hidden/motion/time F^2 and F*F operators or provide sourced coefficient bounds", "em_owner_audit", "BOUND_REQUIRED"),
        ("EMB3597_4_epsilon_CJQ", "epsilon_CJQ", "abs(C_JQ)", "dimensionless", "MISSING_CHARGE_CURRENT_NORMALIZATION_OWNER", "fix representation weights, current normalization, alpha readout and Lorentz-force normalization together", "em_alpha_owner", "BOUND_REQUIRED"),
        ("EMB3597_5_epsilon_Phi_EM_rad", "epsilon_Phi_EM_rad", "abs(integral_boundary S_Poynting dot n dA)/(abs(G_ref M_H) over stated window)", "time^-1_or_dimensionless_window", "MISSING_STATIONARY_ISOLATED_ZERO_OR_FLUX_BOUND", "stationary local source theorem or sourced Poynting flux bound", "em_poynting_components", "BOUND_REQUIRED_CRITICAL"),
        ("EMB3597_6_epsilon_EM_readout", "epsilon_EM_readout", "norm(C_EM_readout)", "model_dependent", "MISSING_READOUT_RADIATIVE_CLOSURE", "show readout-after-variation cannot regenerate EM coefficient dependence, or bound it", "em_current_source", "BOUND_REQUIRED"),
        ("EMB3597_7_epsilon_Delta_J_total", "epsilon_Delta_J_total", "norm(dJ_H_total)", "current_divergence_units", "MISSING_TOTAL_HILBERT_CURRENT_CLOSURE", "parent matter+EM+extra-sector Ward identity and boundary closure", "source_current_closure", "BOUND_REQUIRED"),
        ("EMB3597_8_epsilon_EM_double_count", "epsilon_EM_double_count", "abs(M_matter^dress+M_EM^separate-M_source^dress[J_H_total])/abs(M_H_ref)", "dimensionless", "MISSING_SINGLE_DRESSED_SOURCE_FUNCTIONAL_CERTIFICATE", "source mass assembled once as ell_M(Pi_M J_H_total), not matter mass plus post-readout EM patch", "lock_3596", "BOUND_REQUIRED"),
        ("EMB3597_9_epsilon_dB_impr", "epsilon_dB_impr", "abs(integral_boundary dB_impr)/abs(M_H_ref)", "dimensionless", "MISSING_BOUNDARY_IMPROVEMENT_SILENCE", "boundary/domain certificate or retained improvement flux row", "em_ellj_law", "BOUND_REQUIRED"),
        ("EMB3597_10_epsilon_EM_source_total", "epsilon_EM_source_total", "sum of epsilon_EM_once, epsilon_Hodge_EM, epsilon_w_EM, epsilon_XF2, epsilon_CJQ, epsilon_Phi_EM_rad, epsilon_EM_readout, epsilon_Delta_J_total, epsilon_EM_double_count, epsilon_dB_impr", "dimensionless_or_declared_norm", "NOT_SCORE_READY_TOTAL", "all component zeros or numeric/source-backed bounds", "inputs_3596", "TOTAL_BOUND_BRANCH_ACTIVE"),
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
        ("PROM3597_0_conditional_theorem", "EM/Poynting once-only identity", "PASS_CONDITIONAL_THEOREM", "epsilon_EM_once is zero only under the full listed same-owner premises", "em_hodge_owner"),
        ("PROM3597_1_Poynting_visible", "Poynting vector included", "PASS_GUARD", "Phi_EM_rad is an explicit source/boundary term, not a hidden afterthought", "em_poynting_components"),
        ("PROM3597_2_EM_once_claim", "current EM once-only claim", "FAIL_CURRENT_CLAIM", "Hodge, action normalization, current normalization, hidden XF2, readout, current closure and flux rows remain unsigned", "em_hodge_owner"),
        ("PROM3597_3_no_double_count", "binding/field energy double-count guard", "PASS_NONCLAIM_GUARD", "the single dressed-source functional is required before any orbital mass readout", "lock_3596"),
        ("PROM3597_4_bound_pack", "source-accounting bound pack complete", "PASS_NONCLAIM", "rows are source-ready but not numeric/score-ready", "inputs_3596"),
        ("PROM3597_5_no_Newton_claim", "no Newton/PPN/local-GR promotion", "PASS_GUARD", "Gauss/orbital calibration remains downstream even if EM once-only closes", "charge_residuals"),
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
            "status": "EM_POYNTING_ONCE_THEOREM_CONDITIONAL_BOUND_BRANCH_ACTIVE",
            "strongest_result": "3597 converts the coupling worry into a precise source-accounting theorem: EM stress, Poynting flux and binding energy can be included exactly once if they are varied in the same observed Hilbert source branch before Pi_M and before readout, with flux/boundary terms either zero or explicitly retained.",
            "decision": "keep the conditional theorem, retain all EM once-only rows as nonclaim bounds, and move next to calibrating the dressed Hilbert source against Gauss/orbital measured GM",
            "still_missing": "parent-signed observed EM Hodge/coframe, w_EM=1 normalization, C_XF2=0 operator exclusion, C_JQ charge-current normalization, Phi_EM_rad zero or sourced flux bound, C_EM_readout=0 closure, total Hilbert current closure, exact-improvement boundary silence, and Gauss/orbital calibration",
            "public_claim_allowed": False,
            "valid_for_claim": False,
            "source_path": str(source_map["em_hodge_owner"][0]),
        }
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "next_id": "NEXT3597_0",
            "target_doc": "3598-Y5-R2FR-Gauss-orbital-calibration-or-Delta-cal-bound.md",
            "target_script": "scripts/Y5_R2FR_3598_Gauss_orbital_calibration_or_Delta_cal_bound.py",
            "objective": "connect the dressed Hilbert source charge M_source^dress[W;tau]=ell_M(Pi_M J_H_total) to Poisson/Gauss/orbital measured GM, or retain Delta_cal/partial_r_ln_mu_obs/dln_Geff_dt bounds",
            "success_gate": "a Newtonian/GR local limit may only advance if the source charge that obeys the Hilbert/Poynting accounting is the same quantity measured by orbital acceleration and Gauss-law flux",
            "reason": "3597 makes EM/Poynting accounting precise; the next leap is source calibration to actual Newtonian mechanics rather than another internal source identity",
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
    validations.append(("VAL3597_0_sources_exist", all(path.exists() for path, _ in source_map.values()), "all required 3597 source paths exist"))
    validations.append(("VAL3597_1_needles_found", all(path.exists() and contains(path, needle) for path, needle in source_map.values()), "all selected 3597 source anchors found"))
    pre_validation = {key: path for key, path in out_paths.items() if key != "validation"}
    validations.append(("VAL3597_2_outputs_exist", all(path.exists() for path in pre_validation.values()), "all pre-validation 3597 csv output files written"))
    parse_ok = True
    parse_details: list[str] = []
    for output_id, path in pre_validation.items():
        try:
            parse_details.append(f"{output_id}:{len(read_csv(path))}")
        except Exception as exc:
            parse_ok = False
            parse_details.append(f"{output_id}:ERROR:{exc}")
    validations.append(("VAL3597_3_csv_parse", parse_ok, "; ".join(parse_details)))
    validations.append(("VAL3597_4_conditional_theorem_present", any(row["theorem_id"] == "EMT3597_6_conditional_theorem" and row["status"] == "CONDITIONAL_ZERO_THEOREM_DERIVED" for row in theorem), "EM once-only conditional theorem row present"))
    validations.append(("VAL3597_5_Poynting_flux_explicit", any(row["symbol"] == "epsilon_Phi_EM_rad" and "Poynting" in str(row["formula"]) for row in bounds), "Poynting flux bound row is explicit"))
    validations.append(("VAL3597_6_EM_once_input_active", any(row["symbol"] == "epsilon_EM_once" and row["score_status"] == "BOUND_REQUIRED_CRITICAL" for row in bounds), "epsilon_EM_once remains active until all owner premises close"))
    validations.append(("VAL3597_7_claim_blocked", any(row["gate_id"] == "PROM3597_2_EM_once_claim" and row["status"] == "FAIL_CURRENT_CLAIM" for row in gates), "current EM/Poynting once-only claim is blocked"))
    validations.append(("VAL3597_8_no_claim_flags", not any(str(row.get("valid_for_claim", "False")).lower() == "true" or str(row.get("claim_allowed", "False")).lower() == "true" for table in [theorem, residuals, bounds, gates, status] for row in table), "all generated physics rows remain nonclaim"))
    validations.append(("VAL3597_9_no_local_gr_claim", any(row["gate_id"] == "PROM3597_5_no_Newton_claim" and row["status"] == "PASS_GUARD" for row in gates), "Newton/PPN/local-GR claim guard is active"))
    validations.append(("VAL3597_10_double_count_guard", any(row["symbol"] == "epsilon_EM_double_count" for row in bounds), "double-count guard row present"))
    validations.append(("VAL3597_11_next_target_selected", any(row["next_id"] == "NEXT3597_0" for row in next_target), "3598 Gauss/orbital calibration target selected"))
    source_paths = [Path(str(row["source_path"])) for table in [theorem, residuals, bounds, gates, status] for row in table if row.get("source_path")]
    validations.append(("VAL3597_12_generated_source_paths_exist", all(path.exists() for path in source_paths), "every generated row source_path exists"))
    formal_hits = list(FORMALIZATION.rglob("*3597*")) if FORMALIZATION.exists() else []
    validations.append(("VAL3597_13_formalization_workbench_untouched", len(formal_hits) == 0, "no 3597 checkpoint output appears in formalization-workbench"))
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
        "# 3597 - EM/Poynting Hilbert source accounting or bound",
        "",
        "## Verdict",
        "3597 derives the clean conditional accounting law: EM stress, Poynting flux, and binding energy may enter the source branch exactly once if they are all owned by the same observed Hilbert variation before `Pi_M` and before readout.",
        "",
        "This is progress, not a claim.  The Poynting vector now has a precise role: it is the exterior flux term in the dressed source balance.  If that flux is not zero or explicitly included, the local source charge has time/boundary hair and cannot be promoted to a Newton/PPN/local-GR result.",
        "",
        "## Once-Only Theorem Gate",
    ]
    for row in theorem:
        lines.append(f"- `{row['theorem_id']}`: {row['status']} - {row['statement']}")
    lines.extend(["", "## Residual Decomposition"])
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
    write_csv(out_paths["em_once_theorem"], theorem)
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
