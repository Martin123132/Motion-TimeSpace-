from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CHECKPOINT_ID = "3601"
BRANCH_ID = "MTS_R2FR_Y5_ELLJ_SOURCE_CURRENT_NORMALIZATION_3601"
DOC = ROOT / "3601-Y5-R2FR-ellJ-source-current-normalization-zero-or-bound.md"


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
        "next_3600": (RESIDUALS / "P8_Y5_R2FR_3600_NEXT_TARGET.csv", "NEXT3600_0"),
        "status_3600": (RESIDUALS / "P8_Y5_R2FR_3600_STATUS.csv", "GEFF_PRODUCT_LOCK"),
        "bounds_3600": (RESIDUALS / "P8_Y5_R2FR_3600_GEFF_PRODUCT_BOUND_ROWS.csv", "GPB3600_5_z_ellJ"),
        "ellj_law": (RESIDUALS / "P8_EM_ellJ_source_current_owner_residual_law.csv", "EJR3513_0_total"),
        "ellj_theorem_2937": (RESIDUALS / "P8_Y5_R2FR_2937_ELLJ_OWNER_THEOREM_ATTEMPT.csv", "EJO2937_0_master_conditional_theorem"),
        "source_current": (RESIDUALS / "P8_EM_current_source_Ward_alpha_source_residual.csv", "CSR3508_4_postvariation_rescaling"),
        "matter_descent": (RESIDUALS / "P8_Y5_MATTER_DESCENT_GATE_2611_WORLDTUBE_SOURCE_OWNER_AUDIT.csv", "WTA2611_0_support_selector"),
        "ward_contract": (RESIDUALS / "P8_source_current_Ward_universality_CONTRACT.csv", "SC2_Ward_conservation_on_matter_shell"),
        "ward_owner": (RESIDUALS / "P8_Ward_source_owner_identity_CONTRACT.csv", "C0_on_shell_total_Ward"),
        "pim_htau_law": (RESIDUALS / "P8_EM_PiM_Htau_commutator_residual_law.csv", "PHCR3514_0_total"),
        "pim_lock": (RESIDUALS / "P8_Y5_R10_HAMILTONIAN_PIM_QBARXH_LOCK_2665_LOCK_CONTRACT.csv", "HLOCK2665_4_PiM"),
        "htau_integrability": (RESIDUALS / "P8_Y5_R10_HTAU_INTEGRABILITY_CURL_2667_INTEGRABILITY_GATE.csv", "ICG2667_3_boundary_exact"),
        "source_connection": (RESIDUALS / "P8_EM_source_branch_mass_connection_flatness_law.csv", "SBC3515_2_quotient_vertical_zero"),
        "source_descent_certificate": (RESIDUALS / "P8_EM_quotient_source_coordinate_descent_certificate.csv", "QSC3516_0_master_theorem"),
        "denominator_status": (RESIDUALS / "P8_Y5_Hilbert_source_denominator_PiM_Htau_Newton_bridge_status.csv", "STATUS3549_0"),
        "reference_contract": (RESIDUALS / "P8_Y5_R2FR_2938_MHREF_ELLJ_REFERENCE_LOCK_CONTRACT.csv", "REF2938_2_ellJ_lock"),
        "mhref_rows": (RESIDUALS / "P8_Y5_MHREF_2596_DENOMINATOR_ROWS.csv", "MHD2596_5_MHref"),
        "reference_decision": (RESIDUALS / "P8_Y5_BOUNDARY_REFERENCE_545_DECISION.csv", "D545_1_not_parent_owned"),
        "frame_split": (RESIDUALS / "P8_frame_source_split_residual_or_zero.csv", "FS3048_0_frame_split_definition"),
        "common_action": (RESIDUALS / "P8_EM_common_action_density_line_universal_source_scale.csv", "UCSR3510_0_zeta_w_common"),
    }


def outputs() -> dict[str, Path]:
    return {
        "source_register": RESIDUALS / "P8_Y5_R2FR_3601_SOURCE_REGISTER.csv",
        "ellj_theorem": RESIDUALS / "P8_Y5_R2FR_3601_ELLJ_NORMALIZATION_THEOREM.csv",
        "residuals": RESIDUALS / "P8_Y5_R2FR_3601_ELLJ_RESIDUALS.csv",
        "bound_rows": RESIDUALS / "P8_Y5_R2FR_3601_ELLJ_BOUND_ROWS.csv",
        "promotion_gates": RESIDUALS / "P8_Y5_R2FR_3601_PROMOTION_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3601_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3601_NEXT_TARGET.csv",
        "canonical_status": RESIDUALS / "P8_Y5_ellJ_source_current_normalization_status.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3601_VALIDATION.csv",
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
        ("ELJ3601_0_target", "3601 target", "Prove z_ellJ=D_X ln ell_J=0 by closing matter descent, Ward projection, Pi_M/H_tau, reference, support, frame and unit factors, or retain component bounds.", "3600 identified ell_J as the largest remaining algebraic denominator in the effective coupling product.", "TARGET_IMPORTED", "next_3600"),
        ("ELJ3601_1_exact_decomposition", "ell_J residual law", "z_ellJ[X] = R_md + R_Ward + R_PiM + R_Htau + R_ref + R_W + R_frame + R_units.", "This is an exact component accounting identity: ell_J is not a single mystery coupling any more.", "EXACT_DECOMPOSITION", "ellj_law"),
        ("ELJ3601_2_matter_descent", "matter descent zero route", "R_md=0 if S_matter descends as Sbar[q(Phi),psi,theta] with no source-only weight, hidden representative marker, or direct X/Z matter vertex.", "This kills source-only multipliers only by action grammar, not by fitting WEP/source data after readout.", "CONDITIONAL_ZERO_ROUTE_NOT_SIGNED", "source_current"),
        ("ELJ3601_3_Ward_projection", "Ward projection zero route", "R_Ward=0 if the on-shell Hilbert/Ward current is conserved before Pi_M and readout, and all boundary/non-Hilbert tails are exact, zero, or retained separately.", "Ward conservation alone is not enough; it has to survive projection and exterior support.", "CONDITIONAL_ZERO_ROUTE_NOT_SIGNED", "ward_contract"),
        ("ELJ3601_4_PiM_Htau_square", "PiM/Htau denominator square", "R_PiM+R_Htau = C_M + C_shape + C_curl + C_domain + C_ref + C_frame + C_units.", "This is the algebraic heart of ell_J; it is where source-coordinate flatness and Hamiltonian integrability must meet.", "EXACT_SUBDECOMPOSITION", "pim_htau_law"),
        ("ELJ3601_5_source_connection_zero_route", "source-branch connection route", "C_M=C_shape=0 if the source coordinates Y=(M_H_ref,sigma^a) are q-basic and the residual direction v_X is vertical; then the source-branch connection A_X vanishes.", "This is the strongest route found so far: make the source coordinates quotient observables.", "CONDITIONAL_ZERO_ROUTE_NOT_SIGNED", "source_connection"),
        ("ELJ3601_6_reference_support_frame_units", "reference/support/frame/units route", "R_ref, R_W, R_frame and R_units vanish only if H_ref is source-blind, W_source=closure(supp J_H[tau]), one observed frame/tau/surface branch is fixed, and ell_J/C_source units are selected before measured GM.", "These are anti-laundering clauses: no source denominator may be defined by the orbit it is supposed to predict.", "CONDITIONAL_ZERO_ROUTE_NOT_SIGNED", "reference_contract"),
        ("ELJ3601_7_conditional_theorem", "ell_J normalization theorem", "If R_md=R_Ward=R_PiM=R_Htau=R_ref=R_W=R_frame=R_units=0 by one parent source-current chain, then z_ellJ=0 and the ell_J factor in the effective coupling product is source-silent.", "This is the correct route to removing ell_J from local Gdot/Newton/R10/PPN residuals.", "CONDITIONAL_ZERO_THEOREM_DERIVED", "ellj_theorem_2937"),
        ("ELJ3601_8_current_MTS_verdict", "current corpus verdict", "Current MTS has the exact ell_J decomposition and conditional theorem, but matter descent, Ward projection, Pi_M/H_tau, reference, support, frame and unit factors are not jointly parent-signed.", "So 3601 does not promote constant G, Newton, PPN or local GR; it selects Pi_M/H_tau as the next hard target.", "BOUND_BRANCH_ACTIVE_NO_CLAIM", "denominator_status"),
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
        ("ELJR3601_0_total", "z_ellJ", "D_X ln ell_J", "total source-current normalization drift", "ACTIVE_NONCLAIM", "ellj_law"),
        ("ELJR3601_1_R_md", "R_md", "D_X ln(delta S_matter/delta e_obs)-D_X ln(delta Sbar[q(Phi)]/delta e_obs)", "matter descent/source-only multiplier obstruction", "OPEN_MATTER_DESCENT_REQUIRED", "source_current"),
        ("ELJR3601_2_R_Ward", "R_Ward", "normalized failure of nabla_mu T_H^{mu nu}=0 to imply d(Pi_M J_H)=0", "Ward conservation fails to pass projection/readout", "OPEN_WARD_PROJECTION_REQUIRED", "ward_owner"),
        ("ELJR3601_3_R_PiM", "R_PiM", "([D_X,Pi_M^H]J_H + Pi_M^H[D_X,J_H] - D_X Pi_M^H[J_H]) / Pi_M^H[J_H]", "Pi_M/source-current commutator obstruction", "OPEN_PROJECTOR_LOCK_REQUIRED", "pim_lock"),
        ("ELJR3601_4_R_Htau", "R_Htau", "normalized curl(delta H_tau) = normalized integral_S i_tau omega_total plus exact/boundary terms", "Hamiltonian charge nonintegrability/source-charge curl", "OPEN_HTAU_INTEGRABILITY_REQUIRED", "htau_integrability"),
        ("ELJR3601_5_R_ref", "R_ref", "D_X H_ref/(H_tau-H_ref)", "source-blind reference failure", "OPEN_REFERENCE_LOCK_REQUIRED", "reference_contract"),
        ("ELJR3601_6_R_W", "R_W", "D_X ln int_Wsource rho_H dV_H - D_X ln int_closure(supp J_H[tau]) rho_H dV_H", "worldtube support/domain selector drift", "OPEN_SUPPORT_SELECTOR_REQUIRED", "matter_descent"),
        ("ELJR3601_7_R_frame", "R_frame", "D_X ln(source readout frame)-D_X ln(parent H_tau frame)", "same-frame/tau/readout mismatch", "OPEN_FRAME_LOCK_REQUIRED", "frame_split"),
        ("ELJR3601_8_R_units", "R_units", "D_X ln C_source + D_X ln hidden ell_J unit convention", "duplicate source-unit normalization after w_common and G_ref are separated", "OPEN_UNIT_LOCK_REQUIRED", "common_action"),
        ("ELJR3601_9_R_PiM_plus_R_Htau", "R_PiM_plus_R_Htau", "C_M+C_shape+C_curl+C_domain+C_ref+C_frame+C_units", "combined algebraic heart of ell_J denominator", "OPEN_SUBDENOMINATOR_REQUIRED", "pim_htau_law"),
        ("ELJR3601_10_A_source_connection", "A_X_source_connection", "A_X^M,A_X^a from D_X Y(Phi) with Y=(M_H_ref,sigma^a)", "source-branch mass/shape connection obstruction", "OPEN_SOURCE_CONNECTION_REQUIRED", "source_connection"),
        ("ELJR3601_11_MHref_units", "Delta_MHref_tau_surface_total", "tau/coframe/surface/integrability/M_H_ref denominator lock residual", "M_H_ref and source denominator units not fully parent-locked", "OPEN_MHREF_DENOMINATOR_REQUIRED", "mhref_rows"),
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
        ("ELJB3601_0_z_ellJ", "z_ellJ", "D_X ln ell_J = R_md+R_Ward+R_PiM+R_Htau+R_ref+R_W+R_frame+R_units", "per_channel_derivative_units", "CONDITIONAL_ZERO_IF_ALL_COMPONENTS_PARENT_SILENT", "all ell_J components zero by one parent source-current chain or source-backed bounds", "ellj_law", "BOUND_REQUIRED_CRITICAL"),
        ("ELJB3601_1_R_md", "R_md", "matter descent/source-only multiplier residual", "per_channel_derivative_units", "MISSING_MATTER_DESCENT_SIGNATURE", "S_matter descends through q with no source-only weights/markers/direct vertices", "source_current", "BOUND_REQUIRED"),
        ("ELJB3601_2_R_Ward", "R_Ward", "Ward conservation to projected source flux residual", "dimensionless_or_declared_norm", "MISSING_WARD_PROJECTION_CLOSURE", "total Ward identity survives Pi_M/readout and boundary/non-Hilbert tails are owned", "ward_contract", "BOUND_REQUIRED"),
        ("ELJB3601_3_R_PiM", "R_PiM", "Pi_M/source-current commutator residual", "dimensionless_or_declared_norm", "MISSING_PIM_PARENT_CHAINMAP_LOCK", "Pi_M fixed before readout; source support/Hodge/domain data parent-owned", "pim_lock", "BOUND_REQUIRED_CRITICAL"),
        ("ELJB3601_4_R_Htau", "R_Htau", "H_tau curl/integrability residual", "dimensionless_or_declared_norm", "MISSING_HTAU_INTEGRABILITY_LOCK", "parent L_X/theta/omega/tau/surface/boundary exactness", "htau_integrability", "BOUND_REQUIRED_CRITICAL"),
        ("ELJB3601_5_R_ref", "R_ref", "D_X H_ref/(H_tau-H_ref)", "per_channel_derivative_units", "MISSING_SOURCE_BLIND_REFERENCE", "H_ref selected by topology/stationarity/asymptotic coframe only", "reference_contract", "BOUND_REQUIRED"),
        ("ELJB3601_6_R_W", "R_W", "worldtube support/domain selector drift", "per_channel_derivative_units", "MISSING_WORLDTUBE_SUPPORT_SELECTOR", "W_source=closure(supp J_H[tau]) before readout", "matter_descent", "BOUND_REQUIRED"),
        ("ELJB3601_7_R_frame", "R_frame", "source frame/readout mismatch", "per_channel_derivative_units", "MISSING_SAME_FRAME_TAU_READOUT_LOCK", "same observed coframe/tau/source/orbit/clock/reference branch", "frame_split", "BOUND_REQUIRED"),
        ("ELJB3601_8_R_units", "R_units", "D_X ln C_source + D_X ln hidden ell_J unit convention", "per_channel_derivative_units", "MISSING_SOURCE_UNIT_LOCK", "C_source/ell_J units fixed before measured GM and not duplicated with w_common/G_ref", "common_action", "BOUND_REQUIRED"),
        ("ELJB3601_9_R_PiM_plus_R_Htau", "R_PiM_plus_R_Htau", "C_M+C_shape+C_curl+C_domain+C_ref+C_frame+C_units", "dimensionless_or_declared_norm", "MISSING_PIM_HTAU_SUBDENOMINATOR_LOCK", "mass-flat source connection plus H_tau integrability/reference/worldtube/frame/unit locks", "pim_htau_law", "BOUND_REQUIRED_CRITICAL"),
        ("ELJB3601_10_C_M_C_shape", "C_M_plus_C_shape", "mass/shape source-branch connection curvature terms", "dimensionless_or_declared_norm", "MISSING_SOURCE_COORDINATE_QBASIC_CERTIFICATE", "Y=(M_H_ref,sigma^a) q-basic and v_X vertical, or component bounds", "source_descent_certificate", "BOUND_REQUIRED"),
        ("ELJB3601_11_ellJ_total", "epsilon_ellJ_total", "norm of active R_md,R_Ward,R_PiM,R_Htau,R_ref,R_W,R_frame,R_units and subdenominator components", "declared_norm", "NOT_SCORE_READY_TOTAL", "all components parent-zero or numeric/source-backed with no cancellation", "bounds_3600", "TOTAL_BOUND_BRANCH_ACTIVE"),
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
        ("PROM3601_0_ellJ_decomposition", "ell_J component decomposition", "PASS_EXACT_IDENTITY", "z_ellJ splits into eight source-current owner components", "ellj_law"),
        ("PROM3601_1_conditional_theorem", "ell_J zero theorem", "PASS_CONDITIONAL_THEOREM", "z_ellJ=0 follows if all components close by one parent source-current chain", "ellj_theorem_2937"),
        ("PROM3601_2_ellJ_claim", "current ell_J silence claim", "FAIL_CURRENT_CLAIM", "matter descent, Ward, Pi_M/H_tau, reference, support, frame and units are not jointly signed", "denominator_status"),
        ("PROM3601_3_PiM_Htau_claim", "PiM/Htau subdenominator claim", "FAIL_CURRENT_CLAIM", "R_PiM+R_Htau remains the core open algebraic subproblem", "pim_htau_law"),
        ("PROM3601_4_no_measured_GM_laundering", "no measured-GM denominator laundering", "PASS_GUARD", "ell_J, H_ref, M_H_ref and C_source cannot be defined from orbital GM after the fact", "reference_contract"),
        ("PROM3601_5_bound_pack", "ellJ bound pack complete", "PASS_NONCLAIM", "rows are source-ready but not numeric/score-ready", "bounds_3600"),
        ("PROM3601_6_no_Newton_or_GR_claim", "no Newton/PPN/local-GR promotion", "PASS_GUARD", "ell_J source-current normalization is not promoted", "status_3600"),
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
            "status": "ELLJ_SOURCE_CURRENT_NORMALIZATION_DECOMPOSED_PIM_HTAU_NEXT",
            "strongest_result": "3601 turns ell_J into an exact source-current owner decomposition: z_ellJ=R_md+R_Ward+R_PiM+R_Htau+R_ref+R_W+R_frame+R_units. The conditional theorem is clear, but current MTS has not parent-signed the component zeros.",
            "decision": "retain the ell_J theorem as conditional, keep z_ellJ and all components as active nonclaim rows, and attack R_PiM+R_Htau next because it is the largest algebraic subdenominator",
            "still_missing": "matter descent grammar, Ward-to-projected-flux closure, Pi_M parent chainmap/commutator zero, H_tau integrability, source-blind H_ref, worldtube support selector, same frame/tau/readout lock, source-unit lock, and source-coordinate q-basic certificate",
            "public_claim_allowed": False,
            "valid_for_claim": False,
            "source_path": str(source_map["ellj_law"][0]),
        }
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "next_id": "NEXT3601_0",
            "target_doc": "3602-Y5-R2FR-PiM-Htau-subdenominator-lock-or-component-bound.md",
            "target_script": "scripts/Y5_R2FR_3602_PiM_Htau_subdenominator_lock_or_component_bound.py",
            "objective": "try to prove R_PiM+R_Htau=0 by closing source-coordinate q-basicity, Pi_M chainmap/commutator, H_tau integrability curl, reference, domain, frame and unit terms, or retain C_M/C_shape/C_curl/C_domain/C_ref/C_frame/C_units bounds",
            "success_gate": "ell_J can advance only if the Pi_M/H_tau subdenominator is parent-owned before readout, not patched by measured GM calibration",
            "reason": "3601 shows R_PiM+R_Htau is the algebraic heart of z_ellJ",
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
    validations.append(("VAL3601_0_sources_exist", all(path.exists() for path, _ in source_map.values()), "all required 3601 source paths exist"))
    validations.append(("VAL3601_1_needles_found", all(path.exists() and contains(path, needle) for path, needle in source_map.values()), "all selected 3601 source anchors found"))
    pre_validation = {key: path for key, path in out_paths.items() if key != "validation"}
    validations.append(("VAL3601_2_outputs_exist", all(path.exists() for path in pre_validation.values()), "all pre-validation 3601 csv output files written"))
    parse_ok = True
    parse_details: list[str] = []
    for output_id, path in pre_validation.items():
        try:
            parse_details.append(f"{output_id}:{len(read_csv(path))}")
        except Exception as exc:
            parse_ok = False
            parse_details.append(f"{output_id}:ERROR:{exc}")
    validations.append(("VAL3601_3_csv_parse", parse_ok, "; ".join(parse_details)))
    validations.append(("VAL3601_4_decomposition_present", any(row["theorem_id"] == "ELJ3601_1_exact_decomposition" and row["status"] == "EXACT_DECOMPOSITION" for row in theorem), "ellJ exact decomposition row present"))
    validations.append(("VAL3601_5_component_bounds_present", {"z_ellJ", "R_md", "R_Ward", "R_PiM", "R_Htau", "R_ref", "R_W", "R_frame", "R_units"}.issubset({str(row["symbol"]) for row in bounds}), "ellJ component bound rows present"))
    validations.append(("VAL3601_6_claims_blocked", all(any(row["gate_id"] == gate_id and row["status"] == "FAIL_CURRENT_CLAIM" for row in gates) for gate_id in ["PROM3601_2_ellJ_claim", "PROM3601_3_PiM_Htau_claim"]), "ellJ and PiM/Htau claims are blocked"))
    validations.append(("VAL3601_7_no_laundering_guard", any(row["gate_id"] == "PROM3601_4_no_measured_GM_laundering" and row["status"] == "PASS_GUARD" for row in gates), "measured-GM laundering guard present"))
    validations.append(("VAL3601_8_no_claim_flags", not any(str(row.get("valid_for_claim", "False")).lower() == "true" or str(row.get("claim_allowed", "False")).lower() == "true" for table in [theorem, residuals, bounds, gates, status] for row in table), "all generated physics rows remain nonclaim"))
    validations.append(("VAL3601_9_no_Newton_GR_claim", any(row["gate_id"] == "PROM3601_6_no_Newton_or_GR_claim" and row["status"] == "PASS_GUARD" for row in gates), "Newton/PPN/local-GR claim guard is active"))
    validations.append(("VAL3601_10_next_target_selected", any(row["next_id"] == "NEXT3601_0" for row in next_target), "3602 PiM/Htau target selected"))
    source_paths = [Path(str(row["source_path"])) for table in [theorem, residuals, bounds, gates, status] for row in table if row.get("source_path")]
    validations.append(("VAL3601_11_generated_source_paths_exist", all(path.exists() for path in source_paths), "every generated row source_path exists"))
    formal_hits = []
    if FORMALIZATION.exists():
        for path in FORMALIZATION.rglob("*3601*"):
            if ".venv" in path.parts:
                continue
            if path.name.startswith("3601-") or path.name.startswith("Y5_R2FR_3601") or "P8_Y5_R2FR_3601" in path.name:
                formal_hits.append(path)
    validations.append(("VAL3601_12_formalization_workbench_untouched", len(formal_hits) == 0, "no 3601 checkpoint output appears in formalization-workbench outside package/venv noise"))
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
        "# 3601 - ellJ source-current normalization zero or bound",
        "",
        "## Verdict",
        "3601 turns `ell_J` from a vague denominator into an exact component law: `z_ellJ = R_md + R_Ward + R_PiM + R_Htau + R_ref + R_W + R_frame + R_units`.",
        "",
        "This is a real narrowing.  `ell_J` can be zero only if the full source-current chain is parent-owned before readout; it cannot be defined from measured orbital `GM` after the fact.",
        "",
        "## ellJ Theorem Gate",
    ]
    for row in theorem:
        lines.append(f"- `{row['theorem_id']}`: {row['status']} - {row['statement']}")
    lines.extend(["", "## ellJ Residuals"])
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
    write_csv(out_paths["ellj_theorem"], theorem)
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
