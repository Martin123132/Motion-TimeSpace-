from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CHECKPOINT_ID = "3603"
BRANCH_ID = "MTS_R2FR_Y5_SOURCE_COORDINATE_QBASIC_AX_3603"
DOC = ROOT / "3603-Y5-R2FR-source-coordinate-qbasicity-or-AX-connection-bound.md"


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
        "next_3602": (RESIDUALS / "P8_Y5_R2FR_3602_NEXT_TARGET.csv", "NEXT3602_0"),
        "status_3602": (RESIDUALS / "P8_Y5_R2FR_3602_STATUS.csv", "PIM_HTAU_SUBDENOMINATOR"),
        "bounds_3602": (RESIDUALS / "P8_Y5_R2FR_3602_PIM_HTAU_COMPONENT_BOUND_ROWS.csv", "PHTB3602_8_A_X"),
        "source_connection": (RESIDUALS / "P8_EM_source_branch_mass_connection_flatness_law.csv", "SBC3515_1_induced_connection"),
        "source_connection_failures": (RESIDUALS / "P8_EM_source_branch_mass_connection_flatness_law.csv", "SBC3515_4_failure_decomposition"),
        "source_descent_certificate": (RESIDUALS / "P8_Y5_R2FR_3516_QUOTIENT_SOURCE_COORDINATE_DESCENT_CERTIFICATE.csv", "QSC3516_0_master_theorem"),
        "candidate_q_map": (RESIDUALS / "P8_Y5_R2FR_3517_CANDIDATE_Q_MAP.csv", "QMAP3517_5_source_coordinates_Y"),
        "candidate_vertical_basis": (RESIDUALS / "P8_Y5_R2FR_3517_CANDIDATE_VERTICAL_BASIS.csv", "VB3517_0_v_q_private"),
        "dq_matrix": (RESIDUALS / "P8_Y5_R2FR_3517_DQ_MATRIX_SKELETON.csv", "DQM3517_v_q_Y_target"),
        "field_quotient": (RESIDUALS / "P8_Y5_FIELD_QUOTIENT_2570_DQ_VERTICAL_GENERATOR_LEDGER.csv", "DQ2570_0_chain_rule_template"),
        "common_descent": (RESIDUALS / "P8_Y5_COMMON_DESCENT_DQZ_2643_PARENT_SIGNATURE_THEOREM_GATE.csv", "QVIS2643_0_chain_rule_theorem"),
        "mhref_descent": (RESIDUALS / "P8_Y5_R2FR_3551_MHREF_DESCENT_THEOREM.csv", "MHD3551_1_sum_difference_descent"),
        "htau_qbasic": (RESIDUALS / "P8_Y5_R2FR_3552_HTAU_QBASIC_THEOREM.csv", "HTD3552_1_qbasic_charge_theorem"),
        "source_support_qbasic": (RESIDUALS / "P8_Y5_R2FR_3560_SOURCE_SUPPORT_QBASIC_THEOREM.csv", "SWT3560_3_Y_qbasic_bundle_theorem"),
        "density_qbasic": (RESIDUALS / "P8_Y5_R2FR_3561_HILBERT_DENSITY_QBASIC_THEOREM.csv", "HDQ3561_1_pullback_density_theorem"),
        "no_source_hom": (RESIDUALS / "P8_Y5_R2FR_3562_NO_SOURCE_ONLY_HOM_THEOREM.csv", "NH3562_1_noHom_relative_weight_theorem"),
        "htau_reference": (RESIDUALS / "P8_Y5_R2FR_3577_HTAU_QBASIC_REFERENCE_THEOREM.csv", "HTQ3577_3_MHref_qbasic"),
        "pim_adoption": (RESIDUALS / "P8_Y5_R2FR_3559_HILBERT_IDENTITY_PIM_ADOPTION_THEOREM.csv", "PIA3559_3_qbasic_source_support_zero_route"),
        "mhref_status": (RESIDUALS / "P8_Y5_MHref_qbasic_descent_Htau_Href_status.csv", "STATUS3551_0"),
        "density_status": (RESIDUALS / "P8_Y5_Hilbert_source_density_qbasic_status.csv", "HILBERT_DENSITY_QBASIC_THEOREM_DERIVED_UNSIGNED"),
        "support_status": (RESIDUALS / "P8_Y5_source_support_qbasic_worldtube_status.csv", "SOURCE_SUPPORT_QBASIC_LEMMA_DERIVED_UNSIGNED"),
    }


def outputs() -> dict[str, Path]:
    return {
        "source_register": RESIDUALS / "P8_Y5_R2FR_3603_SOURCE_REGISTER.csv",
        "qbasic_ax_theorem": RESIDUALS / "P8_Y5_R2FR_3603_QBASIC_AX_THEOREM.csv",
        "ax_obstruction_law": RESIDUALS / "P8_Y5_R2FR_3603_AX_OBSTRUCTION_LAW.csv",
        "ax_bound_rows": RESIDUALS / "P8_Y5_R2FR_3603_AX_BOUND_ROWS.csv",
        "promotion_gates": RESIDUALS / "P8_Y5_R2FR_3603_PROMOTION_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3603_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3603_NEXT_TARGET.csv",
        "canonical_status": RESIDUALS / "P8_Y5_source_coordinate_qbasic_AX_status.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3603_VALIDATION.csv",
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
            "AX3603_0_target",
            "3603 target",
            "Prove Y=(M_H_ref,sigma^a) is q-basic and v_X is vertical so A_X=0, or retain A_X and its M-derivatives as source-connection bounds.",
            "3602 shows C_M and C_shape die only if the source-coordinate connection A_X dies before measured GM or source readout.",
            "TARGET_IMPORTED",
            "next_3602",
        ),
        (
            "AX3603_1_qbasic_criterion",
            "infinitesimal q-basicity criterion",
            "For connected q-fibres, Y descends as Y=Ybar(q(Phi)) iff dY annihilates ker(Dq) and is compatible across quotient branches.",
            "This turns source-coordinate descent into a derivative test: every candidate vertical generator must satisfy dM_H_ref(v)=0 and d sigma^a(v)=0.",
            "EXACT_DIFFERENTIAL_CRITERION",
            "field_quotient",
        ),
        (
            "AX3603_2_AX_connection_identity",
            "source-coordinate connection identity",
            "A_X^I:=D_XY^I=dY^I(v_X). If Y is q-basic, A_X^I=dYbar^I(Dq(v_X)).",
            "This is the root chain rule.  It shows why the problem is not an arbitrary coupling constant: it is a source-coordinate derivative.",
            "EXACT_CHAIN_RULE_IDENTITY",
            "source_connection",
        ),
        (
            "AX3603_3_bundle_zero_theorem",
            "source-coordinate bundle zero theorem",
            "If M_H_ref and sigma^a are q-basic and Dq(v_X)=0, then A_X=0, hence partial_M A_X^M=partial_M A_X^a=0 and C_M=C_shape=0.",
            "Combine the q-basic bundle theorem with the chain rule; mass-flatness follows because A_X vanishes identically on the source branch, not by fitted cancellation.",
            "CONDITIONAL_ZERO_THEOREM_DERIVED",
            "source_support_qbasic",
        ),
        (
            "AX3603_4_MHref_descent_route",
            "M_H_ref q-basic route",
            "M_H_ref=H_tau-H_ref is q-basic if H_tau and H_ref are q-basic on the same tau/coframe/surface/reference/unit branch.",
            "A difference of q-basic scalar charges is q-basic; for vertical v_X, A_X^M=D_XH_tau-D_XH_ref=0.",
            "CONDITIONAL_ZERO_ROUTE_NOT_LIVE",
            "mhref_descent",
        ),
        (
            "AX3603_5_shape_reynolds_route",
            "shape q-basic/Reynolds route",
            "For sigma^a=I^a/M_H_ref with I^a=int_W s^a rho_H dV_H, D_X sigma^a=(D_XI^a-sigma^a D_XM_H_ref)/M_H_ref.",
            "If rho_H dV_H, s^a, W_source and M_H_ref are q-basic, Reynolds transport leaves no bulk or boundary motion term, so D_X sigma^a=0.",
            "EXACT_REYNOLDS_TRANSPORT_LAW",
            "source_support_qbasic",
        ),
        (
            "AX3603_6_nonzero_bound_law",
            "source-connection leakage law",
            "If the theorem does not fire, ||A_X|| is bounded by a horizontal Dq leak plus E_MHref+E_sigma: ||A_X|| <= ||dYbar|| ||Dq(v_X)|| + ||E_MHref|| + ||E_sigma||.",
            "This is the useful nonclaim route: every future local arena can score the q-map leak and the two source-coordinate leakage packs without allowing cancellations.",
            "EXACT_BOUND_LAW_NONCLAIM",
            "source_connection_failures",
        ),
        (
            "AX3603_7_current_MTS_verdict",
            "current corpus verdict",
            "Current MTS has the conditional source-coordinate bundle theorem, but it does not yet own the actual Dq matrix, vertical basis, H_tau q-basicness, Hilbert-density q-basicness, regular support, or no-source-only Hom clauses.",
            "So A_X=0 is not live; C_M and C_shape remain component-bound rows.  This is progress because the next fight is now the Dq matrix and source-coordinate leak vector, not a vague coupling gap.",
            "BOUND_BRANCH_ACTIVE_NO_CLAIM",
            "status_3602",
        ),
        (
            "AX3603_8_best_next_move",
            "next mathematical pressure point",
            "Close or bound the actual q-map vertical basis: fill Dq(v_X) entries for each candidate residual direction before trying to claim any q-basic source-coordinate zero.",
            "All q-basic theorems become useless if the chosen residual direction is not genuinely vertical; the Dq matrix is the shared lock across M_H_ref, sigma^a, density, support and H_tau.",
            "NEXT_TARGET_SELECTED",
            "candidate_vertical_basis",
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


def obstruction_rows(source_map: dict[str, tuple[Path, str]]) -> list[dict[str, object]]:
    p = {key: str(value[0]) for key, value in source_map.items()}
    rows = [
        ("AXR3603_0_A_X_total", "A_X_source_connection", "A_X=dY(v_X)=dYbar(Dq(v_X))+E_Y", "total source-coordinate connection vector", "ACTIVE_NONCLAIM_EXACT_CHAIN_RULE", "source_connection"),
        ("AXR3603_1_Dq_vX", "Dq_vX", "Dq(v_X)", "horizontal quotient leak of the candidate residual direction", "OPEN_VERTICAL_BASIS_REQUIRED", "candidate_vertical_basis"),
        ("AXR3603_2_A_XM", "A_XM", "D_X M_H_ref = D_XH_tau-D_XH_ref+E_branch_units", "mass-coordinate source connection", "OPEN_MHREF_QBASIC_REQUIRED", "mhref_descent"),
        ("AXR3603_3_A_Xshape", "A_Xshape", "D_X sigma^a=(D_XI^a-sigma^a D_XM_H_ref)/M_H_ref", "shape/source-support connection", "OPEN_SHAPE_QBASIC_REQUIRED", "source_support_qbasic"),
        ("AXR3603_4_E_Htau", "E_Htau_qbasic", "D_XH_tau - dHbar_tau(Dq(v_X))", "Hamiltonian charge extraction/q-basicness leakage", "OPEN_HTAU_QBASIC_REQUIRED", "htau_qbasic"),
        ("AXR3603_5_E_Href", "E_Href_qbasic", "D_XH_ref - dHbar_ref(Dq(v_X))", "source-blind reference leakage", "OPEN_REFERENCE_BRANCH_REQUIRED", "htau_reference"),
        ("AXR3603_6_E_rho", "E_rho_qbasic", "D_X(rho_H dV_H)-d rhobar_H(Dq(v_X))", "Hilbert source density q-basic leakage", "OPEN_DENSITY_QBASIC_REQUIRED", "density_qbasic"),
        ("AXR3603_7_E_noHom", "E_source_weight", "relative active source prefactor/source-marker/readout-mask terms", "source-only weight countermodel inside density/support", "OPEN_NO_SOURCE_ONLY_HOM_REQUIRED", "no_source_hom"),
        ("AXR3603_8_E_boundary", "E_boundary_birth", "int_boundary s^a rho_H v_boundary dS plus zero-crossing/birth-death events", "support boundary regularity leakage", "OPEN_SUPPORT_REGULARITY_REQUIRED", "source_support_qbasic"),
        ("AXR3603_9_E_tau_frame", "E_tau_frame", "D_X(tau,e_obs,Sigma,readout frame mismatch)", "same-frame tau/coframe support mismatch", "OPEN_FRAME_LOCK_REQUIRED", "candidate_q_map"),
        ("AXR3603_10_E_readout_mask", "E_readout_mask", "D_X W_source post-readout mask or fitted source-domain selector", "readout/domain mask leakage into source coordinates", "OPEN_NO_READOUT_MASK_REQUIRED", "support_status"),
        ("AXR3603_11_E_EM_flux", "E_EM_flux", "nonstationary or non-q-basic EM/Poynting flux contribution to rho_H/support", "EM stress support leakage", "OPEN_EM_FLUX_SILENCE_OR_BOUND_REQUIRED", "density_qbasic"),
        ("AXR3603_12_partial_M_AXM", "partial_M_A_XM", "partial_M(D_XM_H_ref)", "C_M input derivative; zero only if A_XM vanishes identically or derivative bound is sourced", "OPEN_MASS_FLATNESS_DERIVATIVE_REQUIRED", "bounds_3602"),
        ("AXR3603_13_partial_M_AXshape", "partial_M_A_Xshape", "partial_M(D_X sigma^a)", "C_shape input derivative; zero only if A_Xshape vanishes identically or derivative bound is sourced", "OPEN_SHAPE_FLATNESS_DERIVATIVE_REQUIRED", "bounds_3602"),
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
        ("AXB3603_0_A_X_total", "A_X_source_connection", "||A_X|| <= ||dYbar|| ||Dq(v_X)|| + ||E_MHref|| + ||E_sigma||", "source_coordinate_connection_norm", "MISSING_QBASIC_Y_VERTICAL_VX_OR_BOUND", "Dq(v_X) entries plus E_MHref and E_sigma bounds with no cancellation", "source_connection_failures", "BOUND_REQUIRED_CRITICAL"),
        ("AXB3603_1_Dq_vX", "Dq_vX", "Dq(v_X)", "q_component_norm", "MISSING_ACTUAL_DQ_MATRIX_ENTRY", "actual q map, candidate residual basis, norm convention and source/readout columns", "dq_matrix", "BOUND_REQUIRED_CRITICAL"),
        ("AXB3603_2_A_XM", "A_XM", "D_XH_tau-D_XH_ref+E_branch_units", "mass_connection_units", "MISSING_MHREF_QBASIC_OR_DX_BOUND", "H_tau/H_ref q-basic same branch or independent D_XH_tau/D_XH_ref bounds", "mhref_descent", "BOUND_REQUIRED_CRITICAL"),
        ("AXB3603_3_A_Xshape", "A_Xshape", "(D_XI^a-sigma^a D_XM_H_ref)/M_H_ref", "shape_connection_units", "MISSING_SHAPE_QBASIC_OR_REYNOLDS_BOUND", "q-basic Hilbert density/support or source-backed Reynolds boundary/readout/flux rows", "source_support_qbasic", "BOUND_REQUIRED_CRITICAL"),
        ("AXB3603_4_E_MHref", "E_MHref", "E_Htau+E_Href+E_tau_branch+E_ref_branch+E_units", "mass_connection_units", "MISSING_MHREF_LEAKAGE_PACK", "H_tau charge extraction, H_ref source-blindness, same branch and units", "mhref_status", "BOUND_REQUIRED"),
        ("AXB3603_5_E_sigma", "E_sigma", "E_rho+E_boundary_birth+E_tau_frame+E_readout_mask+E_EM_flux+E_MHref_denom", "shape_connection_units", "MISSING_SIGMA_LEAKAGE_PACK", "density q-basic, regular support, frame lock, no readout mask, EM flux bound and positive M_H_ref", "source_support_qbasic", "BOUND_REQUIRED"),
        ("AXB3603_6_E_rho", "E_rho_qbasic", "D_X(rho_H dV_H)-d rhobar_H(Dq(v_X))", "density_derivative_norm", "MISSING_DENSITY_QBASIC_OWNER", "source action pullback, no source-only Hom, q-basic EM, non-Hilbert silence, boundary regularity", "density_qbasic", "BOUND_REQUIRED"),
        ("AXB3603_7_E_source_weight", "E_source_weight", "relative source prefactor/source-marker/readout-mask source density terms", "density_derivative_norm", "MISSING_NO_SOURCE_ONLY_HOM_THEOREM", "parent sort grammar excluding active-source-prefactor morphisms except common scalar line", "no_source_hom", "BOUND_REQUIRED"),
        ("AXB3603_8_E_boundary", "E_boundary_birth", "int_boundary s^a rho_H v_boundary dS + support birth/death events", "shape_boundary_norm", "MISSING_REGULAR_SUPPORT_CERTIFICATE", "stable regular support boundary with vanishing density or explicit boundary event bounds", "source_support_qbasic", "BOUND_REQUIRED"),
        ("AXB3603_9_E_EM_flux", "E_EM_flux", "nonstationary/non-q-basic EM flux through source support", "energy_flux_derivative_norm", "MISSING_EM_STRESS_FLUX_SILENCE_OR_BOUND", "q-basic Maxwell stress plus stationary/no-net-flux support or source-backed Poynting flux row", "density_qbasic", "BOUND_REQUIRED"),
        ("AXB3603_10_partial_M_AXM", "partial_M_A_XM", "partial_M(D_XM_H_ref)", "connection_curvature_norm", "MISSING_PARTIAL_M_AXM_BOUND", "A_XM identically zero, or finite-difference/Lipschitz bound across source-mass branch", "bounds_3602", "BOUND_REQUIRED_CRITICAL"),
        ("AXB3603_11_partial_M_AXshape", "partial_M_A_Xshape", "partial_M(D_X sigma^a)", "connection_curvature_norm", "MISSING_PARTIAL_M_AXSHAPE_BOUND", "A_Xshape identically zero, shape orthogonality theorem, or finite-difference/Lipschitz source-shape bound", "bounds_3602", "BOUND_REQUIRED_CRITICAL"),
        ("AXB3603_12_C_M_Cshape_transfer", "C_M_plus_C_shape", "C_M+C_shape from partial_M A_XM and partial_M A_Xshape", "dimensionless_or_declared_norm", "NOT_SCORE_READY_TOTAL", "componentwise derivative bounds; no cancellation against C_curl/domain/reference/frame/units", "bounds_3602", "TOTAL_BOUND_BRANCH_ACTIVE"),
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
        ("PROM3603_0_chain_rule_identity", "A_X source-coordinate identity", "PASS_EXACT_IDENTITY", "A_X=dY(v_X), and q-basic Y gives A_X=dYbar(Dq(v_X))", "source_connection"),
        ("PROM3603_1_bundle_zero_theorem", "source-coordinate q-basic zero theorem", "PASS_CONDITIONAL_THEOREM", "q-basic M_H_ref and sigma^a plus Dq(v_X)=0 kill A_X, C_M and C_shape", "source_support_qbasic"),
        ("PROM3603_2_reynolds_shape_law", "shape Reynolds transport law", "PASS_EXACT_IDENTITY", "D_X sigma^a=(D_XI^a-sigma^a D_XM_H_ref)/M_H_ref isolates support/density/boundary leakage", "source_support_qbasic"),
        ("PROM3603_3_current_AX_zero_claim", "current A_X=0 claim", "FAIL_CURRENT_CLAIM", "actual Dq matrix, vertical basis, M_H_ref q-basicness, density q-basicness and regular support are not jointly parent-signed", "status_3602"),
        ("PROM3603_4_current_CM_Cshape_claim", "current C_M/C_shape silence claim", "FAIL_CURRENT_CLAIM", "partial_M A_XM and partial_M A_Xshape have no live zero or numeric bound yet", "bounds_3602"),
        ("PROM3603_5_anti_tautology_guard", "no source coordinate in q by declaration", "PASS_GUARD", "Y is a target derived observable; including M_H_ref or sigma^a as primitive q components would be circular", "candidate_q_map"),
        ("PROM3603_6_no_measured_GM_laundering", "no measured-GM source-coordinate laundering", "PASS_GUARD", "M_H_ref and sigma^a must be fixed by parent charge/support, not by orbit/R10/PPN fits", "source_descent_certificate"),
        ("PROM3603_7_bound_pack", "A_X bound pack complete", "PASS_NONCLAIM", "A_X, Dq leak, MHref leakage, shape leakage and derivative rows are source-ready but not score-ready", "bounds_3602"),
        ("PROM3603_8_next_target", "next target selected", "PASS_ROUTE_SELECTED", "fill the actual q-map vertical matrix or retain Dq leak bounds", "candidate_vertical_basis"),
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
            "status": "SOURCE_COORDINATE_QBASIC_AX_THEOREM_DERIVED_DQ_MATRIX_NEXT",
            "strongest_result": "3603 fuses the scattered q-basic results into one source-coordinate connection law: A_X=dY(v_X)=dYbar(Dq(v_X))+E_Y, with exact zero if Y=(M_H_ref,sigma^a) is q-basic and v_X is truly vertical. The shape component now has a Reynolds transport formula, not a mystery coupling.",
            "decision": "retain A_X, A_XM, A_Xshape, Dq_vX, E_MHref, E_sigma and partial_M derivative rows as nonclaim bounds; move next to the actual Dq vertical-basis matrix because every q-basic theorem depends on it",
            "still_missing": "actual q-map matrix entries, certified residual basis, Dq(v_X)=0 or norm bounds, H_tau/H_ref q-basic same-branch lock, Hilbert-density q-basic owner, no-source-only Hom theorem, support regularity, same-frame/readout lock, EM flux silence and derivative bounds for partial_M A_X",
            "public_claim_allowed": False,
            "valid_for_claim": False,
            "source_path": str(source_map["source_support_qbasic"][0]),
        }
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "next_id": "NEXT3603_0",
            "target_doc": "3604-Y5-R2FR-actual-qmap-vertical-basis-or-Dq-leak-bound.md",
            "target_script": "scripts/Y5_R2FR_3604_actual_qmap_vertical_basis_or_Dq_leak_bound.py",
            "objective": "try to construct the actual q-map/Dq matrix and certify which residual directions satisfy Dq(v_X)=0; if not, retain Dq leak bounds for v_q, v_memory, v_coeff, v_boundary and rejected v_RAB directions",
            "success_gate": "no q-basic source-coordinate, H_tau, density or support theorem can be promoted unless the same actual q map and residual basis prove verticality or provide source-backed Dq leak bounds",
            "reason": "3603 shows A_X dies by chain rule only after Dq(v_X)=0; without the Dq matrix, every q-basic zero remains conditional",
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
    validations.append(("VAL3603_0_sources_exist", all(path.exists() for path, _ in source_map.values()), "all required 3603 source paths exist"))
    validations.append(("VAL3603_1_needles_found", all(path.exists() and contains(path, needle) for path, needle in source_map.values()), "all selected 3603 source anchors found"))
    pre_validation = {key: path for key, path in out_paths.items() if key != "validation"}
    validations.append(("VAL3603_2_outputs_exist", all(path.exists() for path in pre_validation.values()), "all pre-validation 3603 csv output files written"))
    parse_ok = True
    parse_details: list[str] = []
    for output_id, path in pre_validation.items():
        try:
            parse_details.append(f"{output_id}:{len(read_csv(path))}")
        except Exception as exc:
            parse_ok = False
            parse_details.append(f"{output_id}:ERROR:{exc}")
    validations.append(("VAL3603_3_csv_parse", parse_ok, "; ".join(parse_details)))
    validations.append(("VAL3603_4_chain_rule_present", any(row["theorem_id"] == "AX3603_2_AX_connection_identity" and row["status"] == "EXACT_CHAIN_RULE_IDENTITY" for row in theorem), "A_X chain-rule identity present"))
    validations.append(("VAL3603_5_bundle_zero_present", any(row["theorem_id"] == "AX3603_3_bundle_zero_theorem" and row["status"] == "CONDITIONAL_ZERO_THEOREM_DERIVED" for row in theorem), "source-coordinate bundle zero theorem present"))
    validations.append(("VAL3603_6_reynolds_law_present", any(row["theorem_id"] == "AX3603_5_shape_reynolds_route" and row["status"] == "EXACT_REYNOLDS_TRANSPORT_LAW" for row in theorem), "shape Reynolds transport law present"))
    validations.append(("VAL3603_7_bound_rows_present", {"A_X_source_connection", "Dq_vX", "A_XM", "A_Xshape", "E_MHref", "E_sigma", "partial_M_A_XM", "partial_M_A_Xshape"}.issubset({str(row["symbol"]) for row in bounds}), "critical A_X and derivative bound rows present"))
    validations.append(("VAL3603_8_claims_blocked", all(any(row["gate_id"] == gate_id and row["status"] == "FAIL_CURRENT_CLAIM" for row in gates) for gate_id in ["PROM3603_3_current_AX_zero_claim", "PROM3603_4_current_CM_Cshape_claim"]), "A_X and C_M/C_shape claims are blocked"))
    validations.append(("VAL3603_9_no_tautology_guard", any(row["gate_id"] == "PROM3603_5_anti_tautology_guard" and row["status"] == "PASS_GUARD" for row in gates), "anti-tautology guard present"))
    validations.append(("VAL3603_10_no_claim_flags", not any(str(row.get("valid_for_claim", "False")).lower() == "true" or str(row.get("claim_allowed", "False")).lower() == "true" for table in [theorem, residuals, bounds, gates, status] for row in table), "all generated physics rows remain nonclaim"))
    validations.append(("VAL3603_11_next_target_selected", any(row["next_id"] == "NEXT3603_0" for row in next_target), "3604 Dq vertical-basis target selected"))
    source_paths = [Path(str(row["source_path"])) for table in [theorem, residuals, bounds, gates, status] for row in table if row.get("source_path")]
    validations.append(("VAL3603_12_generated_source_paths_exist", all(path.exists() for path in source_paths), "every generated row source_path exists"))
    formal_hits = []
    if FORMALIZATION.exists():
        for path in FORMALIZATION.rglob("*3603*"):
            if ".venv" in path.parts:
                continue
            if path.name.startswith("3603-") or path.name.startswith("Y5_R2FR_3603") or "P8_Y5_R2FR_3603" in path.name:
                formal_hits.append(path)
    validations.append(("VAL3603_13_formalization_workbench_untouched", len(formal_hits) == 0, "no 3603 checkpoint output appears in formalization-workbench outside package/venv noise"))
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
        "# 3603 - source-coordinate q-basicity or A_X connection bound",
        "",
        "## Verdict",
        "3603 fuses the scattered source-coordinate work into one sharp law: `A_X=dY(v_X)=dYbar(Dq(v_X))+E_Y`, with `Y=(M_H_ref,sigma^a)`.",
        "",
        "This is the leap we wanted: if `Y` is q-basic and `v_X` is genuinely vertical, then `A_X=0`; therefore `partial_M A_X^M=partial_M A_X^a=0`, so `C_M` and `C_shape` die by chain rule rather than by a fitted plateau or calibration trick.",
        "",
        "The live corpus still cannot claim that zero, because the actual `Dq` matrix/residual basis is not certified.  The nonzero branch is now a usable bound law: `||A_X|| <= ||dYbar|| ||Dq(v_X)|| + ||E_MHref|| + ||E_sigma||`.",
        "",
        "## Source-Coordinate Theorem Gate",
    ]
    for row in theorem:
        lines.append(f"- `{row['theorem_id']}`: {row['status']} - {row['statement']}")
    lines.extend(["", "## A_X Obstruction Law"])
    for row in residuals:
        lines.append(f"- `{row['residual_id']}` / `{row['symbol']}`: {row['status']} - {row['formula']}")
    lines.extend(["", "## A_X Bound Rows"])
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
    residuals = obstruction_rows(source_map)
    bounds = bound_rows(source_map)
    gates = promotion_rows(source_map)
    status = status_rows(source_map)
    next_target = next_target_rows()

    write_csv(out_paths["source_register"], register)
    write_csv(out_paths["qbasic_ax_theorem"], theorem)
    write_csv(out_paths["ax_obstruction_law"], residuals)
    write_csv(out_paths["ax_bound_rows"], bounds)
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
