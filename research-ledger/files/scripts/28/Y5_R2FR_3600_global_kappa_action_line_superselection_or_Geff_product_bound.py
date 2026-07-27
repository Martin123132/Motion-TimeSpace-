from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CHECKPOINT_ID = "3600"
BRANCH_ID = "MTS_R2FR_Y5_GEFF_PRODUCT_LOCK_3600"
DOC = ROOT / "3600-Y5-R2FR-global-kappa-action-line-superselection-or-Geff-product-bound.md"


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
        "next_3599": (RESIDUALS / "P8_Y5_R2FR_3599_NEXT_TARGET.csv", "NEXT3599_0"),
        "status_3599": (
            RESIDUALS / "P8_Y5_R2FR_3599_STATUS.csv",
            "CONSTANT_GEFF_RADIAL_TIME_HAIR",
        ),
        "bounds_3599": (
            RESIDUALS / "P8_Y5_R2FR_3599_DERIVATIVE_HAIR_BOUND_ROWS.csv",
            "DHB3599_8_Geff_product",
        ),
        "kappa_contract": (
            RESIDUALS / "P8_constant_universal_Geff_kappa_CONTRACT.csv",
            "CU7_measured_GM_product_silence",
        ),
        "kappa_theorem": (
            RESIDUALS / "P8_CONSTANT_KAPPA_SUPERSELECTION_THEOREM.csv",
            "T508_1_topological_zeroform",
        ),
        "kappa_clause": (
            RESIDUALS / "P8_CONSTANT_KAPPA_TOPOLOGICAL_ZEROFORM_CLAUSE.csv",
            "K508_3_metric_stress_silence",
        ),
        "kappa_decision": (
            RESIDUALS / "P8_CONSTANT_KAPPA_DECISION.csv",
            "current_MTS_has_not_yet_earned_constant_kappa",
        ),
        "kappa_residual_map": (
            RESIDUALS / "P8_CONSTANT_KAPPA_RESIDUAL_MAP.csv",
            "KR508_5_Bianchi_exchange",
        ),
        "kappa_validation": (
            RESIDUALS / "P8_CONSTANT_KAPPA_VALIDATION.csv",
            "V508_3_no_overclaim",
        ),
        "product_lock": (
            RESIDUALS / "P8_EM_fixed_kappa_Gref_action_line_lock.csv",
            "KGLR3511_4_Geff_product",
        ),
        "factor_vector": (
            RESIDUALS / "P8_EM_product_lock_factor_vector_ellJ_Rframe.csv",
            "PLFV3512_5_Z_product",
        ),
        "product_runner": (
            RESIDUALS / "P8_EM_product_lock_bound_runner_results.csv",
            "PLRUN3512_0_Gdot_product",
        ),
        "common_action": (
            RESIDUALS / "P8_EM_common_action_density_line_universal_source_scale.csv",
            "UCSR3510_0_zeta_w_common",
        ),
        "common_runner": (
            RESIDUALS / "P8_EM_common_scale_bound_runner_results.csv",
            "UCRUN3510_0_Gdot",
        ),
        "constant_sector": (
            RESIDUALS / "P8_constant_sector_universality_CONTRACT.csv",
            "C4_no_constant_running_from_local_MTS",
        ),
        "ellj_law": (
            RESIDUALS / "P8_EM_ellJ_source_current_owner_residual_law.csv",
            "EJR3513_0_total",
        ),
        "pim_htau_law": (
            RESIDUALS / "P8_EM_PiM_Htau_commutator_residual_law.csv",
            "PHCR3514_0_total",
        ),
        "source_current": (
            RESIDUALS / "P8_EM_current_source_Ward_alpha_source_residual.csv",
            "CSR3508_4_postvariation_rescaling",
        ),
        "frame_split": (
            RESIDUALS / "P8_frame_source_split_residual_or_zero.csv",
            "FS3048_0_frame_split_definition",
        ),
        "delta_kappa_exchange": (
            RESIDUALS / "P8_delta_kappa_source_exchange_residual.csv",
            "BK3048_0_bianchi_exchange_definition",
        ),
        "charge_residuals": (
            RESIDUALS / "P8_charge_current_equality_RESIDUAL_DECOMPOSITION.csv",
            "Delta_G",
        ),
        "derivative_gate": (
            RESIDUALS / "P8_CONSTANT_GM_DERIVATIVE_HAIR_GATE.csv",
            "CGM0_master_identity",
        ),
    }


def outputs() -> dict[str, Path]:
    return {
        "source_register": RESIDUALS / "P8_Y5_R2FR_3600_SOURCE_REGISTER.csv",
        "product_theorem": RESIDUALS / "P8_Y5_R2FR_3600_GEFF_PRODUCT_LOCK_THEOREM.csv",
        "residuals": RESIDUALS / "P8_Y5_R2FR_3600_GEFF_PRODUCT_RESIDUALS.csv",
        "bound_rows": RESIDUALS / "P8_Y5_R2FR_3600_GEFF_PRODUCT_BOUND_ROWS.csv",
        "promotion_gates": RESIDUALS / "P8_Y5_R2FR_3600_PROMOTION_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3600_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3600_NEXT_TARGET.csv",
        "canonical_status": RESIDUALS / "P8_Y5_Geff_product_lock_status.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3600_VALIDATION.csv",
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
            "GPL3600_0_target",
            "3600 target",
            "Parent-sign the global kappa/G_eff product lock by proving kappa, w_common, ell_J and R_frame are superselection/source-silent before readout, or retain Geff_product derivative bounds.",
            "3599 showed local Gdot/radial hair collapses only after the effective coupling product is silent.",
            "TARGET_IMPORTED",
            "next_3599",
        ),
        (
            "GPL3600_1_product_identity",
            "effective coupling product identity",
            "Z_product[X] := D_X ln(G_ref*w_common*ell_J*R_frame*C_extra) = z_G + z_w + z_ellJ + z_Rframe + z_extra.",
            "This is the exact anti-smuggling identity: constant kappa alone is not constant measured coupling.",
            "EXACT_PRODUCT_DECOMPOSITION",
            "factor_vector",
        ),
        (
            "GPL3600_2_kappa_zero_route",
            "kappa/G_ref superselection route",
            "z_G=0 if kappa_eff/G_ref is a parent global or topological zero-form sector, metric-stress silent, source/species/range/frame/domain blind, and not regenerated by Bianchi exchange.",
            "The older 508 route is legitimate as a conditional derivation path, but current MTS has not adopted the parent topological clause.",
            "CONDITIONAL_ZERO_ROUTE_NOT_SIGNED",
            "kappa_theorem",
        ),
        (
            "GPL3600_3_w_common_route",
            "common action-line route",
            "z_w=D_X ln w_common is zero only if the ordinary matter action-density line is fixed before readout and cannot depend on q, source labels, species, clocks or local MTS invariants.",
            "A common scale is less dangerous than species drift, but it still changes measured G/action/clock products if unowned.",
            "CONDITIONAL_ZERO_ROUTE_NOT_SIGNED",
            "common_action",
        ),
        (
            "GPL3600_4_ellJ_route",
            "source-current normalization route",
            "z_ellJ=D_X ln ell_J = R_md + R_Ward + R_PiM + R_Htau + R_ref + R_W + R_frame + R_units.",
            "This is the central denominator: source-current normalization is silent only when matter descent, Ward projection, Pi_M/H_tau, reference, support, frame and units all commute before readout.",
            "EXACT_ELLJ_DECOMPOSITION_RETAINED",
            "ellj_law",
        ),
        (
            "GPL3600_5_Rframe_route",
            "same-frame route",
            "z_Rframe=D_X ln R_frame is zero only when the source variation, Hamiltonian time, reference surface, matter readout, clocks and orbital frame are the same parent-selected observed branch.",
            "This prevents absorbing source drift into a frame convention.",
            "CONDITIONAL_ZERO_ROUTE_NOT_SIGNED",
            "frame_split",
        ),
        (
            "GPL3600_6_extra_source_route",
            "extra-sector product route",
            "z_extra is zero only if boundary, projector, non-Hilbert, domain, memory, range, connection and EM cross terms carry no source-normalization product factor.",
            "Otherwise the extra sector remains a real contribution to local Gdot/radial/source residuals.",
            "EXTRA_FACTOR_RETAINED",
            "product_lock",
        ),
        (
            "GPL3600_7_no_cancellation_rule",
            "no product cancellation",
            "Z_product=0 can be credited only if each factor is parent-zero or a parent Ward/superselection identity forces cancellation; fitted cancellation between z_G, z_w, z_ellJ and z_Rframe is nonclaim.",
            "This keeps the product lock from becoming a tuning knob.",
            "ANTI_TUNING_GUARD",
            "product_runner",
        ),
        (
            "GPL3600_8_conditional_product_lock_theorem",
            "G_eff product-lock theorem",
            "If z_G=z_w=z_ellJ=z_Rframe=z_extra=0 by parent action grammar, Ward identity, source-current ownership and same-frame readout, then D_X ln G_eff_product=0 and the G_eff part of d ln mu_obs/dX is silent.",
            "This is the clean route to constant effective coupling, but it is conditional.",
            "CONDITIONAL_ZERO_THEOREM_DERIVED",
            "product_lock",
        ),
        (
            "GPL3600_9_current_MTS_verdict",
            "current corpus verdict",
            "Current MTS has the exact product identity and a conditional kappa route, but w_common, ell_J, R_frame, extra-sector silence and product cancellation are not parent-signed.",
            "So 3600 keeps constant G_eff alive as a derivable target while retaining Geff_product, z_ellJ and z_Rframe rows as nonclaim bounds.",
            "BOUND_BRANCH_ACTIVE_NO_CLAIM",
            "kappa_decision",
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
        ("GPR3600_0_total", "Z_product", "D_X ln(G_ref*w_common*ell_J*R_frame*C_extra)", "total effective coupling product drift", "ACTIVE_NONCLAIM", "factor_vector"),
        ("GPR3600_1_zG", "z_G", "D_X ln G_ref or D_X ln kappa_eff", "global coupling/superselection drift", "CONDITIONAL_ZERO_NOT_SIGNED", "kappa_contract"),
        ("GPR3600_2_delta_kappa_exchange", "delta_kappa_source", "kappa_eff^-1 P_loc[T_obs^{mu nu} nabla_mu kappa_eff]", "Bianchi/source exchange if kappa varies locally", "OPEN_EXCHANGE_REQUIRED", "delta_kappa_exchange"),
        ("GPR3600_3_zW", "z_w", "D_X ln w_common", "ordinary action-density line/common matter scale drift", "OPEN_ACTION_LINE_REQUIRED", "common_action"),
        ("GPR3600_4_delta_w_species", "delta_w_species", "D_X ln w_A - D_X ln w_B", "species-dependent action line breaks source universality", "OPEN_SPECIES_SILENCE_REQUIRED", "common_action"),
        ("GPR3600_5_zEllJ", "z_ellJ", "D_X ln ell_J", "source-current/Hilbert charge normalization drift", "OPEN_SOURCE_CURRENT_OWNER_REQUIRED", "ellj_law"),
        ("GPR3600_6_RPiM_Htau", "R_PiM_plus_R_Htau", "R_PiM + R_Htau = C_M + C_shape + C_curl + C_domain + C_ref + C_frame + C_units", "core Pi_M/H_tau denominator obstruction inside ell_J", "OPEN_PIM_HTAU_REQUIRED", "pim_htau_law"),
        ("GPR3600_7_zRframe", "z_Rframe", "D_X ln R_frame", "same-frame/reference/readout drift", "OPEN_FRAME_LOCK_REQUIRED", "frame_split"),
        ("GPR3600_8_zExtra", "z_extra", "D_X ln C_extra", "boundary/projector/non-Hilbert/local MTS source factor drift", "OPEN_EXTRA_FACTOR_REQUIRED", "factor_vector"),
        ("GPR3600_9_Geff_common_scale", "Geff_common_scale", "D_X ln(G_ref*w_common)", "common scale part of effective G", "OPEN_COMMON_SCALE_REQUIRED", "common_runner"),
        ("GPR3600_10_epsilon_Gref_match", "epsilon_Gref_match", "mismatch between EH, Hamiltonian, Poisson and PPN coupling normalizations", "absolute coupling normalization mismatch", "OPEN_MATCH_REQUIRED", "product_lock"),
        ("GPR3600_11_Delta_G", "Delta_G", "B_xi(1/G_eff-1/G0) or d ln G_eff", "charge-current equality residual from coupling drift", "OPEN_COUPLING_RESIDUAL", "charge_residuals"),
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
        ("GPB3600_0_Geff_product", "Geff_product", "D_X ln(G_ref*w_common*ell_J*R_frame*C_extra)", "per_channel_derivative_units", "CONDITIONAL_ZERO_IF_ALL_PRODUCT_FACTORS_PARENT_SILENT", "z_G=0, z_w=0, z_ellJ=0, z_Rframe=0, z_extra=0 or parent identity cancellation", "factor_vector", "BOUND_REQUIRED_CRITICAL"),
        ("GPB3600_1_z_G", "z_G", "D_X ln G_ref or D_X ln kappa_eff", "per_channel_derivative_units", "MISSING_PARENT_KAPPA_SUPERSELECTION_ADOPTION", "global/topological zero-form kappa clause plus species/range/frame/domain blindness", "kappa_theorem", "BOUND_REQUIRED"),
        ("GPB3600_2_delta_kappa_source", "delta_kappa_source", "kappa_eff^-1 P_loc[T_obs^{mu nu} nabla_mu kappa_eff]", "declared_source_exchange_units", "MISSING_BIANCHI_EXCHANGE_ZERO", "d kappa_eff=0 or source-backed Bianchi exchange bound", "delta_kappa_exchange", "BOUND_REQUIRED"),
        ("GPB3600_3_z_w", "z_w", "D_X ln w_common", "per_channel_derivative_units", "MISSING_ACTION_LINE_SUPERSELECTION", "ordinary action-density line fixed before readout; no q/source/clock dependence", "common_action", "BOUND_REQUIRED"),
        ("GPB3600_4_delta_w_species", "delta_w_species", "D_X ln w_A - D_X ln w_B", "dimensionless_or_derivative_units", "MISSING_SPECIES_ACTION_LINE_BLINDNESS", "constant-sector universality or WEP/source-composition bound", "constant_sector", "BOUND_REQUIRED"),
        ("GPB3600_5_z_ellJ", "z_ellJ", "D_X ln ell_J", "per_channel_derivative_units", "MISSING_SOURCE_CURRENT_NORMALIZATION_OWNER", "matter descent, Ward, Pi_M, H_tau, reference, support, frame and units all parent-silent", "ellj_law", "BOUND_REQUIRED_CRITICAL"),
        ("GPB3600_6_R_PiM_plus_R_Htau", "R_PiM_plus_R_Htau", "C_M + C_shape + C_curl + C_domain + C_ref + C_frame + C_units", "dimensionless_or_declared_norm", "MISSING_PIM_HTAU_DENOMINATOR_LOCK", "source-current square commutator and H_tau curl must close or be bounded", "pim_htau_law", "BOUND_REQUIRED_CRITICAL"),
        ("GPB3600_7_z_Rframe", "z_Rframe", "D_X ln R_frame", "per_channel_derivative_units", "MISSING_SAME_FRAME_SOURCE_READOUT_LOCK", "one observed coframe/tau/source/reference/orbit/clock branch before readout", "frame_split", "BOUND_REQUIRED_CRITICAL"),
        ("GPB3600_8_z_extra", "z_extra", "D_X ln C_extra", "per_channel_derivative_units", "MISSING_EXTRA_FACTOR_SILENCE", "boundary/projector/non-Hilbert/domain/memory/range/connection/EM product factors zero or bounded", "factor_vector", "BOUND_REQUIRED"),
        ("GPB3600_9_epsilon_Gref_match", "epsilon_Gref_match", "EH/Hamiltonian/Poisson/PPN coupling normalization mismatch", "dimensionless", "MISSING_ABSOLUTE_COUPLING_MATCH", "same G_ref in action, Hamiltonian charge, Poisson coefficient and PPN map", "product_lock", "BOUND_REQUIRED"),
        ("GPB3600_10_no_product_cancellation_identity", "C_product_cancel_identity", "z_G+z_w+z_ellJ+z_Rframe+z_extra == 0 as parent identity", "boolean_or_symbolic_identity", "MISSING_PARENT_PRODUCT_CANCELLATION_IDENTITY", "no fitted cancellation among product factors", "product_runner", "GUARD_REQUIRED"),
        ("GPB3600_11_product_lock_total", "epsilon_product_lock_total", "norm of active Geff_product, z_G, z_w, z_ellJ, z_Rframe, z_extra and coupling-match residuals", "declared_norm", "NOT_SCORE_READY_TOTAL", "all product factors parent-zero or numeric/source-backed bounds", "product_runner", "TOTAL_BOUND_BRANCH_ACTIVE"),
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
        ("PROM3600_0_product_identity", "G_eff product decomposition", "PASS_EXACT_IDENTITY", "effective coupling drift splits into z_G, z_w, z_ellJ, z_Rframe and z_extra", "factor_vector"),
        ("PROM3600_1_kappa_route", "kappa/G_ref superselection route", "PASS_CONDITIONAL_ROUTE", "topological/global kappa can zero z_G if adopted, but is not current claim credit", "kappa_validation"),
        ("PROM3600_2_product_claim", "constant effective G product", "FAIL_CURRENT_CLAIM", "w_common, ell_J, R_frame, z_extra and product cancellation remain unsigned", "product_runner"),
        ("PROM3600_3_ellJ_claim", "source-current normalization silence", "FAIL_CURRENT_CLAIM", "ell_J denominator still contains matter descent, Ward, Pi_M/H_tau, reference, support, frame and unit residuals", "ellj_law"),
        ("PROM3600_4_Rframe_claim", "same-frame product silence", "FAIL_CURRENT_CLAIM", "same source/readout/clock/orbit frame remains unsigned", "frame_split"),
        ("PROM3600_5_no_product_cancellation", "no fitted product cancellation", "PASS_GUARD", "Z_product=0 needs factor zeros or a parent identity, not tuning", "product_runner"),
        ("PROM3600_6_bound_pack", "product bound pack complete", "PASS_NONCLAIM", "rows are source-ready but not numeric/score-ready", "product_runner"),
        ("PROM3600_7_no_Newton_or_GR_claim", "no Newton/PPN/local-GR promotion", "PASS_GUARD", "constant effective coupling is not promoted", "status_3599"),
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
            "status": "GEFF_PRODUCT_LOCK_IDENTITY_DERIVED_PRODUCT_BOUNDS_ACTIVE",
            "strongest_result": "3600 derives the effective-coupling product identity: D_X ln(G_ref*w_common*ell_J*R_frame*C_extra)=z_G+z_w+z_ellJ+z_Rframe+z_extra. The kappa/topological route can conditionally zero z_G, but constant measured coupling requires every product factor to be parent-silent.",
            "decision": "keep the product theorem, retain Geff_product/z_ellJ/z_Rframe/z_w/z_extra as active nonclaim rows, and attack ell_J source-current normalization next because it is the largest remaining algebraic denominator",
            "still_missing": "parent adoption of topological/global kappa clause, w_common action-line silence, ell_J source-current normalization owner, Pi_M/H_tau denominator lock, same-frame R_frame lock, extra-sector product silence, absolute Gref/EH/Hamiltonian/Poisson/PPN match, and no product cancellation identity",
            "public_claim_allowed": False,
            "valid_for_claim": False,
            "source_path": str(source_map["factor_vector"][0]),
        }
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "next_id": "NEXT3600_0",
            "target_doc": "3601-Y5-R2FR-ellJ-source-current-normalization-zero-or-bound.md",
            "target_script": "scripts/Y5_R2FR_3601_ellJ_source_current_normalization_zero_or_bound.py",
            "objective": "try to prove z_ellJ=D_X ln ell_J=0 by closing matter descent, Ward projection, Pi_M/H_tau, reference, support, frame and unit factors, or retain z_ellJ component bound rows",
            "success_gate": "the effective coupling product can advance only if the source-current normalization denominator is parent-owned before readout, not calibrated from observed GM",
            "reason": "3600 shows z_ellJ is the largest remaining algebraic denominator in the constant effective G product",
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
    validations.append(("VAL3600_0_sources_exist", all(path.exists() for path, _ in source_map.values()), "all required 3600 source paths exist"))
    validations.append(("VAL3600_1_needles_found", all(path.exists() and contains(path, needle) for path, needle in source_map.values()), "all selected 3600 source anchors found"))
    pre_validation = {key: path for key, path in out_paths.items() if key != "validation"}
    validations.append(("VAL3600_2_outputs_exist", all(path.exists() for path in pre_validation.values()), "all pre-validation 3600 csv output files written"))
    parse_ok = True
    parse_details: list[str] = []
    for output_id, path in pre_validation.items():
        try:
            parse_details.append(f"{output_id}:{len(read_csv(path))}")
        except Exception as exc:
            parse_ok = False
            parse_details.append(f"{output_id}:ERROR:{exc}")
    validations.append(("VAL3600_3_csv_parse", parse_ok, "; ".join(parse_details)))
    validations.append(("VAL3600_4_product_identity_present", any(row["theorem_id"] == "GPL3600_1_product_identity" and row["status"] == "EXACT_PRODUCT_DECOMPOSITION" for row in theorem), "effective coupling product decomposition row present"))
    validations.append(("VAL3600_5_core_factor_bounds_present", {"Geff_product", "z_G", "z_w", "z_ellJ", "z_Rframe"}.issubset({str(row["symbol"]) for row in bounds}), "core product factor bounds present"))
    validations.append(("VAL3600_6_current_claims_blocked", all(any(row["gate_id"] == gate_id and row["status"] == "FAIL_CURRENT_CLAIM" for row in gates) for gate_id in ["PROM3600_2_product_claim", "PROM3600_3_ellJ_claim", "PROM3600_4_Rframe_claim"]), "product, ellJ and Rframe claims are blocked"))
    validations.append(("VAL3600_7_no_product_cancellation_guard", any(row["gate_id"] == "PROM3600_5_no_product_cancellation" and row["status"] == "PASS_GUARD" for row in gates), "no fitted product-cancellation guard present"))
    validations.append(("VAL3600_8_no_claim_flags", not any(str(row.get("valid_for_claim", "False")).lower() == "true" or str(row.get("claim_allowed", "False")).lower() == "true" for table in [theorem, residuals, bounds, gates, status] for row in table), "all generated physics rows remain nonclaim"))
    validations.append(("VAL3600_9_no_Newton_GR_claim", any(row["gate_id"] == "PROM3600_7_no_Newton_or_GR_claim" and row["status"] == "PASS_GUARD" for row in gates), "Newton/PPN/local-GR claim guard is active"))
    validations.append(("VAL3600_10_next_target_selected", any(row["next_id"] == "NEXT3600_0" for row in next_target), "3601 ellJ normalization target selected"))
    source_paths = [Path(str(row["source_path"])) for table in [theorem, residuals, bounds, gates, status] for row in table if row.get("source_path")]
    validations.append(("VAL3600_11_generated_source_paths_exist", all(path.exists() for path in source_paths), "every generated row source_path exists"))
    formal_hits = []
    if FORMALIZATION.exists():
        for path in FORMALIZATION.rglob("*3600*"):
            if ".venv" in path.parts:
                continue
            if path.name.startswith("3600-") or path.name.startswith("Y5_R2FR_3600") or "P8_Y5_R2FR_3600" in path.name:
                formal_hits.append(path)
    validations.append(("VAL3600_12_formalization_workbench_untouched", len(formal_hits) == 0, "no 3600 checkpoint output appears in formalization-workbench outside package/venv noise"))
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
        "# 3600 - Global kappa/action-line superselection or G_eff product bound",
        "",
        "## Verdict",
        "3600 derives the effective-coupling product law: constant `kappa` is not enough.  The local Newton coupling is silent only when `G_ref`, `w_common`, `ell_J`, `R_frame`, and extra source factors are all parent-silent before readout.",
        "",
        "This is progress because it prevents the easy mistake: declaring one constant while the actual measured product still drifts through source-current normalization, action-line scale, frame/readout, or extra-sector factors.",
        "",
        "## Product-Lock Theorem Gate",
    ]
    for row in theorem:
        lines.append(f"- `{row['theorem_id']}`: {row['status']} - {row['statement']}")
    lines.extend(["", "## Product Residuals"])
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
    write_csv(out_paths["product_theorem"], theorem)
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
