from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CHECKPOINT_ID = "3602"
BRANCH_ID = "MTS_R2FR_Y5_PIM_HTAU_SUBDENOMINATOR_3602"
DOC = ROOT / "3602-Y5-R2FR-PiM-Htau-subdenominator-lock-or-component-bound.md"


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
        "next_3601": (RESIDUALS / "P8_Y5_R2FR_3601_NEXT_TARGET.csv", "NEXT3601_0"),
        "status_3601": (RESIDUALS / "P8_Y5_R2FR_3601_STATUS.csv", "ELLJ_SOURCE_CURRENT_NORMALIZATION"),
        "bounds_3601": (RESIDUALS / "P8_Y5_R2FR_3601_ELLJ_BOUND_ROWS.csv", "ELJB3601_9_R_PiM_plus_R_Htau"),
        "pim_htau_law": (RESIDUALS / "P8_EM_PiM_Htau_commutator_residual_law.csv", "PHCR3514_0_total"),
        "source_connection": (RESIDUALS / "P8_EM_source_branch_mass_connection_flatness_law.csv", "SBC3515_2_quotient_vertical_zero"),
        "source_descent_certificate": (RESIDUALS / "P8_EM_quotient_source_coordinate_descent_certificate.csv", "QSC3516_0_master_theorem"),
        "denominator_status": (RESIDUALS / "P8_Y5_Hilbert_source_denominator_PiM_Htau_Newton_bridge_status.csv", "STATUS3549_0"),
        "mass_flat_status": (RESIDUALS / "P8_Y5_mass_flat_source_connection_PiM_chainmap_status.csv", "STATUS3550_0"),
        "pim_chainmap_status": (RESIDUALS / "P8_Y5_Hilbert_identity_PiM_chainmap_source_support_status.csv", "PIMH_OPERATOR_CHAINMAP"),
        "local_gr_pim_htau_status": (RESIDUALS / "P8_local_GR_PiM_Htau_zero_mechanism_status.csv", "STAT3532_0_RPiM"),
        "pim_lock": (RESIDUALS / "P8_Y5_R10_HAMILTONIAN_PIM_QBARXH_LOCK_2665_LOCK_CONTRACT.csv", "HLOCK2665_4_PiM"),
        "htau_integrability": (RESIDUALS / "P8_Y5_R10_HTAU_INTEGRABILITY_CURL_2667_INTEGRABILITY_GATE.csv", "ICG2667_3_boundary_exact"),
        "matter_support": (RESIDUALS / "P8_Y5_MATTER_DESCENT_GATE_2611_WORLDTUBE_SOURCE_OWNER_AUDIT.csv", "WTA2611_0_support_selector"),
        "reference_contract": (RESIDUALS / "P8_Y5_R2FR_2938_MHREF_ELLJ_REFERENCE_LOCK_CONTRACT.csv", "REF2938_1_Href_selector"),
        "mhref_rows": (RESIDUALS / "P8_Y5_MHREF_2596_DENOMINATOR_ROWS.csv", "MHD2596_7_integrability"),
        "reference_decision": (RESIDUALS / "P8_Y5_BOUNDARY_REFERENCE_545_DECISION.csv", "D545_1_not_parent_owned"),
        "frame_split": (RESIDUALS / "P8_frame_source_split_residual_or_zero.csv", "FS3048_0_frame_split_definition"),
        "common_action": (RESIDUALS / "P8_EM_common_action_density_line_universal_source_scale.csv", "UCSR3510_0_zeta_w_common"),
    }


def outputs() -> dict[str, Path]:
    return {
        "source_register": RESIDUALS / "P8_Y5_R2FR_3602_SOURCE_REGISTER.csv",
        "subdenominator_theorem": RESIDUALS / "P8_Y5_R2FR_3602_PIM_HTAU_SUBDENOMINATOR_THEOREM.csv",
        "component_residuals": RESIDUALS / "P8_Y5_R2FR_3602_PIM_HTAU_COMPONENT_RESIDUALS.csv",
        "component_bounds": RESIDUALS / "P8_Y5_R2FR_3602_PIM_HTAU_COMPONENT_BOUND_ROWS.csv",
        "promotion_gates": RESIDUALS / "P8_Y5_R2FR_3602_PROMOTION_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3602_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3602_NEXT_TARGET.csv",
        "canonical_status": RESIDUALS / "P8_Y5_PiM_Htau_subdenominator_status.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3602_VALIDATION.csv",
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
            "PHT3602_0_target",
            "3602 target",
            "Try to prove R_PiM+R_Htau=0, or keep each Pi_M/H_tau subdenominator component as an explicit bound term.",
            "3601 selected this as the algebraic heart of z_ellJ, so this checkpoint attacks the denominator directly rather than circling it.",
            "TARGET_IMPORTED",
            "next_3601",
        ),
        (
            "PHT3602_1_exact_decomposition",
            "PiM/Htau residual law",
            "R_PiM + R_Htau = C_M + C_shape + C_curl + C_domain + C_ref + C_frame + C_units.",
            "This is the exact bookkeeping identity inherited from the Pi_M/H_tau commutator law; the zero problem is now seven named components.",
            "EXACT_COMPONENT_DECOMPOSITION",
            "pim_htau_law",
        ),
        (
            "PHT3602_2_source_coordinate_connection",
            "source-coordinate connection",
            "Let Y(Phi)=(M_H_ref(Phi), sigma^a(Phi)) and A_X^I := D_X Y^I.  Then C_M and C_shape are the mass/shape connection pieces induced by A_X.",
            "This replaces a vague source calibration problem with a field-space connection on the source-coordinate bundle.",
            "EXACT_DEFINITION",
            "source_connection",
        ),
        (
            "PHT3602_3_quotient_zero_theorem",
            "q-basic source-coordinate theorem",
            "If Y=Ybar(q(Phi)) and v_X in ker(Dq), then A_X^I=dYbar^I(Dq(v_X))=0, hence C_M=C_shape=0.",
            "This is a real derivation route: source mass and source shape must be quotient observables before readout, not fitted orbital labels.",
            "CONDITIONAL_ZERO_THEOREM_DERIVED",
            "source_descent_certificate",
        ),
        (
            "PHT3602_4_Htau_integrability_zero",
            "H_tau curl zero theorem",
            "C_curl=0 if the parent L_X/theta/omega/tau/surface branch is fixed and the H_tau symplectic boundary term is exact, zero, or separately bounded.",
            "The curl obstruction is not a matter of notation; it is the Hamiltonian integrability condition needed before Pi_M can be treated as a charge derivative.",
            "CONDITIONAL_ZERO_ROUTE_NOT_SIGNED",
            "htau_integrability",
        ),
        (
            "PHT3602_5_domain_reference_frame_units_zero",
            "domain/reference/frame/unit silence",
            "C_domain=C_ref=C_frame=C_units=0 only if W_source, H_ref, tau/coframe/surface readout, and denominator units are parent-selected before measured GM or clock/orbit readout.",
            "These terms prevent laundering a local-GR/Newton result through a denominator chosen after the observable is known.",
            "CONDITIONAL_ZERO_ROUTE_NOT_SIGNED",
            "matter_support",
        ),
        (
            "PHT3602_6_subdenominator_theorem",
            "PiM/Htau subdenominator zero theorem",
            "If A_X=0, C_curl=0, and the domain/reference/frame/unit clauses are all parent-silent, then R_PiM+R_Htau=0.",
            "This is the clean theorem: the subdenominator can close, but only through source-coordinate q-basicity plus Hamiltonian integrability and anti-laundering locks.",
            "CONDITIONAL_ZERO_THEOREM_DERIVED",
            "denominator_status",
        ),
        (
            "PHT3602_7_current_MTS_verdict",
            "current corpus verdict",
            "Current MTS has the conditional mechanism, but not the live signatures for q-basic Y, actual vertical v_X, H_tau integrability, fixed support/reference/frame, or source-unit silence.",
            "So R_PiM+R_Htau remains a live bound vector.  No Newton, PPN, R10, orbital, clock, or local-GR claim is promoted here.",
            "BOUND_BRANCH_ACTIVE_NO_CLAIM",
            "local_gr_pim_htau_status",
        ),
        (
            "PHT3602_8_best_next_move",
            "next mathematical pressure point",
            "The least hand-wavy route is to prove source-coordinate q-basicity first: Y=(M_H_ref,sigma^a)=Ybar(q(Phi)) and Dq(v_X)=0.",
            "If this closes, C_M and C_shape die by chain rule before any numerical bound; if it fails, their connection components become the next numeric local-bound inputs.",
            "NEXT_TARGET_SELECTED",
            "mass_flat_status",
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
        ("PHTR3602_0_total", "R_PiM_plus_R_Htau", "C_M+C_shape+C_curl+C_domain+C_ref+C_frame+C_units", "combined Pi_M/H_tau subdenominator residual", "ACTIVE_NONCLAIM_EXACT_DECOMPOSITION", "pim_htau_law"),
        ("PHTR3602_1_C_M", "C_M", "-(partial_M A_X^M) partial_M(H_tau-H_ref)/(Pi_M H_tau)", "mass-coordinate connection curvature component", "OPEN_SOURCE_MASS_CONNECTION_ZERO_REQUIRED", "source_connection"),
        ("PHTR3602_2_C_shape", "C_shape", "-(partial_M A_X^a) partial_a(H_tau-H_ref)/(Pi_M H_tau)", "shape/source-sector leakage component", "OPEN_SOURCE_SHAPE_CONNECTION_ZERO_REQUIRED", "source_connection"),
        ("PHTR3602_3_C_curl", "C_curl", "Pi_M^H(curl(delta H_tau))/(Pi_M H_tau)", "Hamiltonian field-space curl/integrability component", "OPEN_HTAU_INTEGRABILITY_REQUIRED", "htau_integrability"),
        ("PHTR3602_4_C_domain", "C_domain", "normalized D_X(W_source, Sigma, Hodge, linked surfaces)", "domain/Hodge/worldtube variation inside Pi_M", "OPEN_SUPPORT_DOMAIN_LOCK_REQUIRED", "matter_support"),
        ("PHTR3602_5_C_ref", "C_ref", "-([D_X,Pi_M]H_ref + Pi_M D_X H_ref)/(Pi_M H_tau)", "reference subtraction commutator component", "OPEN_SOURCE_BLIND_REFERENCE_REQUIRED", "reference_contract"),
        ("PHTR3602_6_C_frame", "C_frame", "D_X ln(tau, e_obs, Sigma, readout frame mismatch)", "same-frame/tau/surface readout mismatch component", "OPEN_FRAME_READOUT_LOCK_REQUIRED", "frame_split"),
        ("PHTR3602_7_C_units", "C_units", "D_X ln(Pi_M H_tau denominator units)", "source denominator unit leakage component", "OPEN_DENOMINATOR_UNIT_LOCK_REQUIRED", "common_action"),
        ("PHTR3602_8_A_X", "A_X_source_connection", "A_X^I=D_X Y^I=dYbar^I(Dq(v_X)) when Y is q-basic", "source-coordinate connection whose zero kills C_M and C_shape", "CONDITIONAL_ZERO_NOT_LIVE", "source_descent_certificate"),
        ("PHTR3602_9_qbasic_Y", "qbasic_Y", "Y(Phi)=(M_H_ref,sigma^a)=Ybar(q(Phi))", "source mass and source shape descend through the quotient", "OPEN_QBASIC_CERTIFICATE_REQUIRED", "source_descent_certificate"),
        ("PHTR3602_10_vertical_vX", "vertical_vX", "Dq(v_X)=0", "actual residual direction is vertical for the parent quotient map", "OPEN_VERTICAL_BASIS_REQUIRED", "source_descent_certificate"),
        ("PHTR3602_11_PiM_chainmap", "PiM_chainmap", "[d,Pi_M^H]J_H^M=0 on fixed C_H^M plus fixed support", "Pi_M can act as a parent charge derivative only after support/reference locks", "PARTIAL_CHAINMAP_OPEN_SUPPORT", "pim_chainmap_status"),
        ("PHTR3602_12_MHref_tau_surface", "Delta_MHref_tau_surface_total", "tau/coframe/surface/integrability/M_H_ref denominator lock residual", "MH_ref denominator ownership still needed for qbasic_Y", "OPEN_MHREF_LOCK_REQUIRED", "mhref_rows"),
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
        ("PHTB3602_0_total", "R_PiM_plus_R_Htau", "C_M+C_shape+C_curl+C_domain+C_ref+C_frame+C_units", "dimensionless_or_declared_norm", "MISSING_SUBDENOMINATOR_ZERO_OR_NUMERIC_BOUND", "all C_i terms parent-zero or numeric/source-backed without cancellation", "pim_htau_law", "BOUND_REQUIRED_CRITICAL"),
        ("PHTB3602_1_C_M", "C_M", "-(partial_M A_X^M) partial_M(H_tau-H_ref)/(Pi_M H_tau)", "dimensionless_or_declared_norm", "MISSING_MASS_CONNECTION_FLATNESS", "M_H_ref q-basic plus v_X vertical, or source-backed bound on partial_M A_X^M", "source_connection", "BOUND_REQUIRED_CRITICAL"),
        ("PHTB3602_2_C_shape", "C_shape", "-(partial_M A_X^a) partial_a(H_tau-H_ref)/(Pi_M H_tau)", "dimensionless_or_declared_norm", "MISSING_SHAPE_CONNECTION_FLATNESS", "sigma^a q-basic plus v_X vertical, or source-backed bound on partial_M A_X^a", "source_connection", "BOUND_REQUIRED_CRITICAL"),
        ("PHTB3602_3_C_curl", "C_curl", "Pi_M^H(curl(delta H_tau))/(Pi_M H_tau)", "dimensionless_or_charge_curl_norm", "MISSING_HTAU_CURL_ZERO_OR_BOUND", "parent symplectic/Hamiltonian integrability certificate or numeric curl bound", "htau_integrability", "BOUND_REQUIRED_CRITICAL"),
        ("PHTB3602_4_C_domain", "C_domain", "normalized D_X(W_source, Sigma, Hodge, linked surfaces)", "dimensionless_or_declared_norm", "MISSING_SUPPORT_DOMAIN_LOCK", "W_source=closure(supp J_H[tau]) and linked surfaces fixed before readout", "matter_support", "BOUND_REQUIRED"),
        ("PHTB3602_5_C_ref", "C_ref", "-([D_X,Pi_M]H_ref + Pi_M D_X H_ref)/(Pi_M H_tau)", "dimensionless_or_declared_norm", "MISSING_SOURCE_BLIND_REFERENCE", "H_ref selected by topology/stationarity/asymptotic coframe with no source/material/GM labels", "reference_contract", "BOUND_REQUIRED"),
        ("PHTB3602_6_C_frame", "C_frame", "D_X ln(tau, e_obs, Sigma, readout frame mismatch)", "per_channel_derivative_units", "MISSING_SAME_FRAME_BRANCH_LOCK", "same tau/coframe/surface/source/orbit/clock branch for parent and readout", "frame_split", "BOUND_REQUIRED"),
        ("PHTB3602_7_C_units", "C_units", "D_X ln(Pi_M H_tau denominator units)", "per_channel_derivative_units", "MISSING_DENOMINATOR_UNIT_LOCK", "Pi_M/H_tau/M_H_ref/ell_J units fixed before measured GM and not duplicated with common action scale", "common_action", "BOUND_REQUIRED"),
        ("PHTB3602_8_A_X", "A_X_source_connection", "A_X^I=D_XY^I", "source_coordinate_connection_units", "MISSING_QBASIC_Y_AND_VERTICAL_VX", "Y=Ybar(q(Phi)) and Dq(v_X)=0, or component source-connection bounds", "source_descent_certificate", "BOUND_REQUIRED_CRITICAL"),
        ("PHTB3602_9_qbasic_MHref", "qbasic_MHref", "M_H_ref(Phi)=Mbar_H_ref(q(Phi))", "boolean_or_residual_norm", "MISSING_MHREF_QBASIC_DESCENT", "H_tau and H_ref both q-basic on the same tau/coframe/surface branch", "source_descent_certificate", "BOUND_REQUIRED"),
        ("PHTB3602_10_qbasic_sigma", "qbasic_sigma", "sigma^a(Phi)=sigmabar^a(q(Phi))", "boolean_or_residual_norm", "MISSING_SIGMA_QBASIC_DESCENT", "worldtube/shape coordinates selected from parent support current, not fitted domain masks", "source_descent_certificate", "BOUND_REQUIRED"),
        ("PHTB3602_11_vertical_vX", "vertical_vX", "Dq(v_X)=0", "boolean_or_residual_norm", "MISSING_ACTUAL_VERTICAL_BASIS", "actual residual basis is certified vertical for the parent quotient", "source_descent_certificate", "BOUND_REQUIRED"),
        ("PHTB3602_12_total_no_cancellation", "epsilon_PiM_Htau_total", "norm(C_M,C_shape,C_curl,C_domain,C_ref,C_frame,C_units)", "declared_norm", "NOT_SCORE_READY_TOTAL", "componentwise zero/bounds; no cancellation between unrelated missing terms", "bounds_3601", "TOTAL_BOUND_BRANCH_ACTIVE"),
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
        ("PROM3602_0_exact_decomposition", "PiM/Htau component decomposition", "PASS_EXACT_IDENTITY", "R_PiM+R_Htau is split into C_M,C_shape,C_curl,C_domain,C_ref,C_frame,C_units", "pim_htau_law"),
        ("PROM3602_1_qbasic_zero_route", "q-basic source-connection zero theorem", "PASS_CONDITIONAL_THEOREM", "Y=Ybar(q(Phi)) and Dq(v_X)=0 imply A_X=0 and C_M=C_shape=0", "source_descent_certificate"),
        ("PROM3602_2_subdenominator_zero_theorem", "full PiM/Htau zero theorem", "PASS_CONDITIONAL_THEOREM", "all seven C_i components zero imply R_PiM+R_Htau=0", "denominator_status"),
        ("PROM3602_3_current_PiM_Htau_claim", "current PiM/Htau silence claim", "FAIL_CURRENT_CLAIM", "q-basic source coordinates, vertical basis, H_tau curl, support, reference, frame and units are not jointly parent-signed", "status_3601"),
        ("PROM3602_4_current_Newton_GR_claim", "Newton/PPN/local-GR promotion", "FAIL_CURRENT_CLAIM", "the subdenominator is not live-zero, so no local-GR/Newton claim follows from 3602", "local_gr_pim_htau_status"),
        ("PROM3602_5_no_measured_GM_laundering", "no measured-GM source denominator laundering", "PASS_GUARD", "M_H_ref, H_ref, W_source, Pi_M and units must be fixed before orbital GM/readout", "reference_contract"),
        ("PROM3602_6_bound_pack", "PiM/Htau component bound pack complete", "PASS_NONCLAIM", "component rows are source-ready but not numeric/score-ready", "bounds_3601"),
        ("PROM3602_7_next_target", "next target selected", "PASS_ROUTE_SELECTED", "attack source-coordinate q-basicity and vertical-basis certificate before further numeric bounds", "mass_flat_status"),
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
            "status": "PIM_HTAU_SUBDENOMINATOR_CONDITIONAL_ZERO_THEOREM_BOUND_BRANCH_ACTIVE",
            "strongest_result": "3602 derives the exact local theorem for the Pi_M/H_tau subdenominator: R_PiM+R_Htau=0 if source-coordinate q-basicity, actual verticality, H_tau integrability, support/domain, source-blind reference, same-frame readout, and denominator-unit silence all hold.",
            "decision": "keep the theorem as a conditional win, keep all seven C_i components as nonclaim bound rows, and move next to source-coordinate q-basicity because it kills C_M and C_shape by chain rule rather than by numeric fitting",
            "still_missing": "Y=(M_H_ref,sigma^a) q-basic descent, Dq(v_X)=0 vertical basis certificate, H_tau curl zero/exactness, W_source support descent, source-blind H_ref selector, same-frame tau/coframe/surface readout lock, and denominator unit lock",
            "public_claim_allowed": False,
            "valid_for_claim": False,
            "source_path": str(source_map["pim_htau_law"][0]),
        }
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "next_id": "NEXT3602_0",
            "target_doc": "3603-Y5-R2FR-source-coordinate-qbasicity-or-AX-connection-bound.md",
            "target_script": "scripts/Y5_R2FR_3603_source_coordinate_qbasicity_or_AX_connection_bound.py",
            "objective": "try to prove Y=(M_H_ref,sigma^a) is q-basic and v_X is vertical so A_X=0; if not, retain A_X^M, A_X^a, partial_M A_X^M and partial_M A_X^a as source-connection bound inputs",
            "success_gate": "C_M and C_shape can be removed only by parent-owned source-coordinate descent and actual verticality, not by calibrating source mass/shape from measured orbital GM",
            "reason": "3602 shows the source-coordinate connection is the best route to killing two critical Pi_M/H_tau components before numeric scoring",
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
    validations.append(("VAL3602_0_sources_exist", all(path.exists() for path, _ in source_map.values()), "all required 3602 source paths exist"))
    validations.append(("VAL3602_1_needles_found", all(path.exists() and contains(path, needle) for path, needle in source_map.values()), "all selected 3602 source anchors found"))
    pre_validation = {key: path for key, path in out_paths.items() if key != "validation"}
    validations.append(("VAL3602_2_outputs_exist", all(path.exists() for path in pre_validation.values()), "all pre-validation 3602 csv output files written"))
    parse_ok = True
    parse_details: list[str] = []
    for output_id, path in pre_validation.items():
        try:
            parse_details.append(f"{output_id}:{len(read_csv(path))}")
        except Exception as exc:
            parse_ok = False
            parse_details.append(f"{output_id}:ERROR:{exc}")
    validations.append(("VAL3602_3_csv_parse", parse_ok, "; ".join(parse_details)))
    validations.append(("VAL3602_4_exact_decomposition_present", any(row["theorem_id"] == "PHT3602_1_exact_decomposition" and row["status"] == "EXACT_COMPONENT_DECOMPOSITION" for row in theorem), "PiM/Htau exact component decomposition row present"))
    validations.append(("VAL3602_5_component_bounds_present", {"C_M", "C_shape", "C_curl", "C_domain", "C_ref", "C_frame", "C_units"}.issubset({str(row["symbol"]) for row in bounds}), "all seven C_i component bound rows present"))
    validations.append(("VAL3602_6_qbasic_route_present", any(row["theorem_id"] == "PHT3602_3_quotient_zero_theorem" and row["status"] == "CONDITIONAL_ZERO_THEOREM_DERIVED" for row in theorem), "source-coordinate q-basic zero theorem present"))
    validations.append(("VAL3602_7_claims_blocked", all(any(row["gate_id"] == gate_id and row["status"] == "FAIL_CURRENT_CLAIM" for row in gates) for gate_id in ["PROM3602_3_current_PiM_Htau_claim", "PROM3602_4_current_Newton_GR_claim"]), "PiM/Htau and Newton/GR claims are blocked"))
    validations.append(("VAL3602_8_no_laundering_guard", any(row["gate_id"] == "PROM3602_5_no_measured_GM_laundering" and row["status"] == "PASS_GUARD" for row in gates), "measured-GM/source denominator laundering guard present"))
    validations.append(("VAL3602_9_no_claim_flags", not any(str(row.get("valid_for_claim", "False")).lower() == "true" or str(row.get("claim_allowed", "False")).lower() == "true" for table in [theorem, residuals, bounds, gates, status] for row in table), "all generated physics rows remain nonclaim"))
    validations.append(("VAL3602_10_next_target_selected", any(row["next_id"] == "NEXT3602_0" for row in next_target), "3603 source-coordinate q-basicity target selected"))
    source_paths = [Path(str(row["source_path"])) for table in [theorem, residuals, bounds, gates, status] for row in table if row.get("source_path")]
    validations.append(("VAL3602_11_generated_source_paths_exist", all(path.exists() for path in source_paths), "every generated row source_path exists"))
    formal_hits = []
    if FORMALIZATION.exists():
        for path in FORMALIZATION.rglob("*3602*"):
            if ".venv" in path.parts:
                continue
            if path.name.startswith("3602-") or path.name.startswith("Y5_R2FR_3602") or "P8_Y5_R2FR_3602" in path.name:
                formal_hits.append(path)
    validations.append(("VAL3602_12_formalization_workbench_untouched", len(formal_hits) == 0, "no 3602 checkpoint output appears in formalization-workbench outside package/venv noise"))
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
        "# 3602 - PiM/Htau subdenominator lock or component bound",
        "",
        "## Verdict",
        "3602 gets a real theorem out of the fog: `R_PiM + R_Htau = C_M + C_shape + C_curl + C_domain + C_ref + C_frame + C_units`.",
        "",
        "The best zero route is not a plateau axiom.  It is a chain-rule mechanism: make the source coordinates `Y=(M_H_ref,sigma^a)` descend through the parent quotient and prove the residual direction is vertical.  Then `A_X=dYbar(Dq(v_X))=0`, so the mass/shape connection terms `C_M` and `C_shape` vanish before fitting.",
        "",
        "The full PiM/Htau zero remains conditional because `C_curl`, support/domain, reference, frame, and unit silence are not yet parent-signed.  No Newton, PPN, R10, orbital, clock, or local-GR claim is promoted.",
        "",
        "## PiM/Htau Theorem Gate",
    ]
    for row in theorem:
        lines.append(f"- `{row['theorem_id']}`: {row['status']} - {row['statement']}")
    lines.extend(["", "## Component Residuals"])
    for row in residuals:
        lines.append(f"- `{row['residual_id']}` / `{row['symbol']}`: {row['status']} - {row['formula']}")
    lines.extend(["", "## Component Bound Rows"])
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
    write_csv(out_paths["subdenominator_theorem"], theorem)
    write_csv(out_paths["component_residuals"], residuals)
    write_csv(out_paths["component_bounds"], bounds)
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
