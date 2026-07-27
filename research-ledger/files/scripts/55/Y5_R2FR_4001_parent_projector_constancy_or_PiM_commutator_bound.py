from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "4001"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "4001-Y5-R2FR-parent-projector-constancy-or-PiM-commutator-bound.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_4001_SOURCE_REGISTER.csv",
    "theorem": SRC / "P8_Y5_R2FR_4001_PIM_CONSTANCY_THEOREM.csv",
    "audit": SRC / "P8_Y5_R2FR_4001_PIM_ZERO_PROOF_AUDIT.csv",
    "bounds": SRC / "P8_Y5_R2FR_4001_PIM_COMMUTATOR_BOUND_VECTOR.csv",
    "cases": SRC / "P8_Y5_R2FR_4001_EVALUATOR_CASES.csv",
    "results": SRC / "P8_Y5_R2FR_4001_EVALUATOR_RESULTS.csv",
    "decision": SRC / "P8_Y5_R2FR_4001_DECISION_GATE.csv",
    "claim_gate": SRC / "P8_Y5_R2FR_4001_CLAIM_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_4001_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_4001_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_4001_VALIDATION.csv",
}

NEXT_DOC = "4002-Y5-R2FR-Htau-Href-integrability-reference-lock-or-curl-bound.md"
NEXT_SCRIPT = "scripts/Y5_R2FR_4002_Htau_Href_integrability_reference_lock_or_curl_bound.py"


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def source_specs() -> list[tuple[str, Path, str, str]]:
    return [
        ("SRC4001_00_next", SRC / "P8_Y5_R2FR_4000_NEXT_TARGET.csv", "NEXT4000_0", "4000 handoff"),
        ("SRC4001_01_3999_commutation", SRC / "P8_Y5_R2FR_3999_FLUX_CLOSURE_THEOREM.csv", "FCT3999_2_projector_commutation", "3999 projector commutation target"),
        ("SRC4001_02_3999_bound", SRC / "P8_Y5_R2FR_3999_MH_FLUX_BOUND_VECTOR.csv", "MHF3999_3_projector", "3999 Delta_PiM bound slot"),
        ("SRC4001_03_3965_readout", SRC / "P8_Y5_R2FR_3965_PROJECTOR_STRESS_SPLIT.csv", "PSS3965_3_readout_guard", "no post-readout projector mask"),
        ("SRC4001_04_3514_total", SRC / "P8_EM_PiM_Htau_commutator_residual_law.csv", "PHCR3514_0_total", "PiM/Htau residual total"),
        ("SRC4001_05_3514_mass", SRC / "P8_EM_PiM_Htau_commutator_residual_law.csv", "PHCR3514_1_C_M", "mass-coordinate connection component"),
        ("SRC4001_06_3514_domain", SRC / "P8_EM_PiM_Htau_commutator_residual_law.csv", "PHCR3514_4_C_domain", "domain/Hodge/worldtube component"),
        ("SRC4001_07_3514_ref", SRC / "P8_EM_PiM_Htau_commutator_residual_law.csv", "PHCR3514_5_C_ref", "reference component"),
        ("SRC4001_08_3515_zero", SRC / "P8_EM_source_branch_mass_connection_flatness_law.csv", "SBC3515_2_quotient_vertical_zero", "quotient vertical zero theorem"),
        ("SRC4001_09_3515_decomp", SRC / "P8_EM_source_branch_mass_connection_flatness_law.csv", "SBC3515_4_failure_decomposition", "source-connection failure decomposition"),
        ("SRC4001_10_3516_master", SRC / "P8_EM_quotient_source_coordinate_descent_certificate.csv", "QSC3516_0_master_theorem", "q-basic source-coordinate certificate"),
        ("SRC4001_11_3516_filter", SRC / "P8_EM_quotient_source_coordinate_descent_certificate.csv", "QSC3516_3_actual_basis_filter", "vertical basis filter"),
        ("SRC4001_12_2407_chainmap", SRC / "P8_Y5_PARENT_QLOC_2407_PIM_ZERO_THEOREM_ATTEMPT.csv", "PZ2407_1_fixed_chainmap_lemma", "fixed chain-map lemma"),
        ("SRC4001_13_2407_wrong", SRC / "P8_Y5_PARENT_QLOC_2407_PIM_ZERO_THEOREM_ATTEMPT.csv", "PZ2407_5_topological_Hilbert_equality", "closed-wrong-current guard"),
        ("SRC4001_14_2585_audit", SRC / "P8_Y5_PIM_CHAINMAP_2585_THEOREM_AUDIT.csv", "CMA2585_7_verdict", "previous chainmap verdict"),
        ("SRC4001_15_2585_bounds", SRC / "P8_Y5_PIM_CHAINMAP_2585_ICOMMUTATOR_BOUND_ROWS.csv", "IC2585_TOTAL", "commutator bound row"),
        ("SRC4001_16_symp_contract", SRC / "P8_PiM_parent_symplectic_projector_algebra_CONTRACT.csv", "PM5_projector_variation_owned", "projector variation ownership"),
        ("SRC4001_17_variation_contract", SRC / "P8_PiM_projector_variation_stress_CONTRACT.csv", "PV7_readout_masks_after_variation_only", "readout masks after variation"),
        ("SRC4001_18_topological", SRC / "P8_TOPOLOGICAL_PIM_CLOSURE_CONDITIONS.csv", "TC500_3_Hilbert_equality", "topological Hilbert equality blocker"),
    ]


def source_register_rows(timestamp: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path, needle, role in source_specs():
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            {
                "source_id": source_id,
                "role": role,
                "path": str(path),
                "needle": needle,
                "exists": exists,
                "needle_found": needle in text,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def theorem_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "PCM4001_0_product_rule",
            "claim_piece": "projected-current product rule",
            "mathematical_form": "d(Pi_M J_H)=Pi_M dJ_H + [d,Pi_M]J_H, with [d,Pi_M]J_H := d(Pi_M J_H)-Pi_M dJ_H",
            "derived_result": "the projector commutator is a real term; it cannot be deleted by notation",
            "status": "EXACT_OBSTRUCTION_IDENTITY",
            "source_path": str(SRC / "P8_Y5_PARENT_QLOC_2407_PIM_ZERO_THEOREM_ATTEMPT.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "PCM4001_1_fixed_chainmap_zero",
            "claim_piece": "fixed parent chain-map zero theorem",
            "mathematical_form": "If Pi_M:C_H(A_ext)->C_M(A_ext) is parent-selected before readout, d Pi_M=Pi_M d on C_H(A_ext), D_A Pi_M=0, and J_H in C_H(A_ext), then [d,Pi_M]J_H=0.",
            "derived_result": "the algebraic route to projector silence is clean for one fixed physical source-current complex",
            "status": "EXACT_CONDITIONAL_ZERO_THEOREM",
            "source_path": str(SRC / "P8_Y5_PIM_CHAINMAP_2585_THEOREM_AUDIT.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "PCM4001_2_parent_constancy_branch",
            "claim_piece": "parent constancy on the same exterior annulus",
            "mathematical_form": "D_A Pi_M=0 if A_ext, W_source, S_link, orientation, tau, e_obs/Hodge, reference subtraction, and denominator are all selected by the parent branch before readout.",
            "derived_result": "topological/absolute-charge Pi_M can be stress-silent; Hodge, Green, domain, or readout Pi_M must carry variation stress or bounds",
            "status": "CONDITIONAL_PARENT_CONSTANCY_THEOREM",
            "source_path": str(SRC / "P8_PiM_projector_variation_stress_CONTRACT.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "PCM4001_3_quotient_source_connection_zero",
            "claim_piece": "q-basic source-coordinate route",
            "mathematical_form": "Y=(M_H_ref,sigma^a)=Ybar(q(Phi)) and v_X in ker(Dq) imply D_XY=0, hence A_X^M=A_X^a=0 and the C_M/C_shape source-connection pieces vanish.",
            "derived_result": "part of the Pi_M/Htau obstruction can be killed by quotient descent, but only for certified vertical directions and q-basic source coordinates",
            "status": "EXACT_CONDITIONAL_PARTIAL_ZERO_THEOREM",
            "source_path": str(SRC / "P8_EM_quotient_source_coordinate_descent_certificate.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "PCM4001_4_closed_wrong_current_guard",
            "claim_piece": "closed topological current must be the Hilbert/Newton source",
            "mathematical_form": "Pi_M J_H = J_M_top + dB_zero with int_boundary dB_zero=0 and the same M_H_ref denominator",
            "derived_result": "a closed current that is not the observed Hilbert source cannot prove Newton/source normalization",
            "status": "GUARD_REQUIRED_NOT_PARENT_SIGNED",
            "source_path": str(SRC / "P8_TOPOLOGICAL_PIM_CLOSURE_CONDITIONS.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "PCM4001_5_absolute_bound_if_not_zero",
            "claim_piece": "failed projector zero theorem becomes an absolute residual",
            "mathematical_form": "Delta_PiM_4001 <= |C_M|+|C_shape|+|C_curl|+|C_domain|+|C_ref|+|C_frame|+|C_units|+|I_commutator|+|T_PiM|+|R_eq|",
            "derived_result": "projector failure is now a no-cancellation vector feeding Newton, PPN, R10, Gdot, and local-GR gates",
            "status": "EXECUTABLE_BOUND_VECTOR",
            "source_path": str(SRC / "P8_EM_PiM_Htau_commutator_residual_law.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "PCM4001_6_current_verdict",
            "claim_piece": "4001 current verdict",
            "mathematical_form": "Pi_M silence is derived only as a conditional branch; current MTS still needs parent signatures or source-backed component rows.",
            "derived_result": "the next sharp blocker is H_tau/H_ref integrability and reference lock, because it controls C_curl, C_ref, and M_H_ref q-basic descent",
            "status": "ROUTE_REDUCED_NO_LOCAL_GR_CLAIM",
            "source_path": str(SRC / "P8_EM_source_branch_mass_connection_flatness_law.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def audit_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "audit_id": "PZA4001_0_parent_selector",
            "clause": "Pi_M is parent-selected before readout",
            "required_signature": "mass/source selector or absolute charge map in the parent action/current complex",
            "current_evidence": "fixed chain-map theorem exists, but parent selector remains unsigned",
            "verdict": "OPEN_PARENT_SELECTOR",
            "feeds_bound": "I_commutator_abs;readout_mask",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "PZA4001_1_fixed_domain",
            "clause": "source worldtube, exterior annulus, linked surfaces, and orientation are fixed before readout",
            "required_signature": "W_source=closure(supp J_H[tau]) with fixed A_ext and S_link on the same branch",
            "current_evidence": "domain/worldtube support remains conditional",
            "verdict": "OPEN_DOMAIN_WORLD_TUBE_LOCK",
            "feeds_bound": "C_domain",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "PZA4001_2_chainmap",
            "clause": "Pi_M commutes with d on the physical Hilbert current complex",
            "required_signature": "d Pi_M=Pi_M d and J_H in C_H(A_ext)",
            "current_evidence": "mathematical lemma clean; physical current-domain certificate missing",
            "verdict": "CONDITIONAL_CHAINMAP_NOT_LIVE",
            "feeds_bound": "I_commutator_abs",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "PZA4001_3_source_coordinate_descent",
            "clause": "source coordinates are q-basic for certified vertical directions",
            "required_signature": "Y=Ybar(q(Phi)) and Dq(v_X)=0 for the actual residual basis",
            "current_evidence": "exact theorem exists but q-map/v-basis and q-basic source certificate remain unsigned",
            "verdict": "PARTIAL_ZERO_ROUTE_NOT_LIVE",
            "feeds_bound": "C_M;C_shape",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "PZA4001_4_Htau_Href",
            "clause": "H_tau and H_ref are integrable, same-frame, and source-blind where required",
            "required_signature": "curl(delta H_tau)=0 and H_ref fixed by source-blind boundary/topology/asymptotic data",
            "current_evidence": "C_curl and C_ref remain open components",
            "verdict": "NEXT_DERIVATION_TARGET",
            "feeds_bound": "C_curl;C_ref;C_units",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "PZA4001_5_wrong_current_guard",
            "clause": "closed topological charge equals the observed Hilbert/Newton mass channel",
            "required_signature": "Pi_M J_H=J_M_top+dB_zero with zero compact boundary flux and same M_H_ref denominator",
            "current_evidence": "topological closure conditions keep Hilbert equality failed open",
            "verdict": "CLOSED_WRONG_CURRENT_REFUSED",
            "feeds_bound": "R_eq_guard;B_zero_flux",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "PZA4001_6_readout_firewall",
            "clause": "post-readout or fitted projector masks never enter the parent variation",
            "required_signature": "Pi_M fixed before orbital, PPN, R10, clock, or source-normalization scoring",
            "current_evidence": "policy guard active and evaluator refuses readout masks",
            "verdict": "GUARD_ACTIVE",
            "feeds_bound": "readout_mask",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "PZA4001_7_zero_proof_verdict",
            "clause": "D_A Pi_M=0 and [d,Pi_M]J_H=0",
            "required_signature": "all upstream clauses signed on the same annulus and same tau/e_obs/reference/denominator branch",
            "current_evidence": "conditional theorem constructed; current corpus still needs signatures or bounds",
            "verdict": "CONDITIONAL_ZERO_BRANCH_PLUS_BOUND_VECTOR",
            "feeds_bound": "Delta_PiM_4001",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def bound_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "bound_id": "PMB4001_0_master",
            "target": "Delta_PiM_4001",
            "formula": "|C_M|+|C_shape|+|C_curl|+|C_domain|+|C_ref|+|C_frame|+|C_units|+|I_commutator_abs|+|projector_stress|+|R_eq_guard|",
            "numeric_value": "MISSING_PARENT_SIGNED_COMPONENTS",
            "units": "dimensionless",
            "status": "EXECUTABLE_VECTOR_READY",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "PMB4001_1_C_M",
            "target": "C_M",
            "formula": "-(partial_M A_X^M) partial_M(H_tau-H_ref)/(Pi_M H_tau)",
            "numeric_value": "ZERO_IF_Q_BASIC_SOURCE_COORDINATE_DESCENT_ELSE_BOUND_REQUIRED",
            "units": "dimensionless",
            "status": "CONDITIONAL_QUOTIENT_ZERO_OR_BOUND",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "PMB4001_2_C_shape",
            "target": "C_shape",
            "formula": "-(partial_M A_X^a) partial_a(H_tau-H_ref)/(Pi_M H_tau)",
            "numeric_value": "ZERO_IF_Q_BASIC_SHAPE_DESCENT_OR_MASS_SHAPE_ORTHOGONALITY_ELSE_BOUND_REQUIRED",
            "units": "dimensionless",
            "status": "CONDITIONAL_QUOTIENT_ZERO_OR_BOUND",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "PMB4001_3_C_curl",
            "target": "C_curl",
            "formula": "Pi_M^H(curl(delta H_tau))/(Pi_M H_tau)",
            "numeric_value": "MISSING_HTAU_INTEGRABILITY_CURL_ZERO_OR_BOUND",
            "units": "dimensionless",
            "status": "NEXT_TARGET",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "PMB4001_4_C_domain",
            "target": "C_domain",
            "formula": "normalized D_X(W_source,Sigma,Hodge,linked surfaces)",
            "numeric_value": "MISSING_DOMAIN_WORLDTUBE_LOCK_OR_OPERATOR_BOUND",
            "units": "dimensionless_or_operator_norm",
            "status": "OPEN_DOMAIN_BOUND",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "PMB4001_5_C_ref",
            "target": "C_ref",
            "formula": "-([D_X,Pi_M]H_ref + Pi_M D_X H_ref)/(Pi_M H_tau)",
            "numeric_value": "MISSING_REFERENCE_SELECTOR_ZERO_OR_BOUND",
            "units": "dimensionless",
            "status": "NEXT_TARGET",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "PMB4001_6_C_frame_units",
            "target": "C_frame + C_units",
            "formula": "D_X ln(tau,e_obs,Sigma,readout frame) + D_X ln(Pi_M H_tau denominator units)",
            "numeric_value": "MISSING_SAME_FRAME_AND_DENOMINATOR_LOCK",
            "units": "dimensionless",
            "status": "OPEN_FRAME_DENOMINATOR_BOUND",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "PMB4001_7_I_commutator",
            "target": "I_commutator_abs",
            "formula": "M_H_ref^-1 |int_A [d,Pi_M]J_H|",
            "numeric_value": "MISSING_CHAINMAP_ZERO_OR_SOURCE_ROW",
            "units": "dimensionless_after_MHref_normalization",
            "status": "OPEN_CHAINMAP_OR_SOURCE_ROW",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "PMB4001_8_projector_stress",
            "target": "projector_stress",
            "formula": "T_PiM^{mu nu}:=-(2/sqrt(-g)) delta_g[Pi_M J_H]/delta g_mu_nu",
            "numeric_value": "ZERO_IF_TOPOLOGICAL_METRIC_INDEPENDENT_ELSE_PPN_SOURCE_BOUND_REQUIRED",
            "units": "PPN_or_operator_units",
            "status": "OPEN_PROJECTOR_STRESS_MAP",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "PMB4001_9_R_eq_guard",
            "target": "R_eq_guard",
            "formula": "Pi_M J_H - J_M_top - dB_zero on the same M_H_ref denominator",
            "numeric_value": "MISSING_TOPOLOGICAL_HILBERT_EQUALITY_OR_VALUE",
            "units": "dimensionless",
            "status": "CLOSED_WRONG_CURRENT_GUARD",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def case_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "case_id": "CASE4001_0_fixed_chainmap_zero",
            "route": "fixed_parent_chainmap_on_physical_current_complex",
            "C_M": 0.0,
            "C_shape": 0.0,
            "C_curl": 0.0,
            "C_domain": 0.0,
            "C_ref": 0.0,
            "C_frame": 0.0,
            "C_units": 0.0,
            "I_commutator_abs": 0.0,
            "projector_stress": 0.0,
            "R_eq_guard": 0.0,
            "uses_readout_projector_mask": False,
            "uses_closed_wrong_current": False,
            "input_status": "CONDITIONAL_ZERO_CLAUSES_UNSIGNED",
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE4001_1_quotient_descent_partial",
            "route": "q_basic_source_coordinates_kill_C_M_C_shape",
            "C_M": 0.0,
            "C_shape": 0.0,
            "C_curl": 2.0e-6,
            "C_domain": 0.0,
            "C_ref": 1.0e-6,
            "C_frame": 0.0,
            "C_units": 0.0,
            "I_commutator_abs": 0.0,
            "projector_stress": 0.0,
            "R_eq_guard": 0.0,
            "uses_readout_projector_mask": False,
            "uses_closed_wrong_current": False,
            "input_status": "PARTIAL_ZERO_HTAU_HREF_STILL_OPEN",
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE4001_2_domain_projector_drift",
            "route": "domain_Hodge_worldtube_variation_bound",
            "C_M": 0.0,
            "C_shape": 0.0,
            "C_curl": 0.0,
            "C_domain": 4.0e-5,
            "C_ref": 0.0,
            "C_frame": 0.0,
            "C_units": 0.0,
            "I_commutator_abs": 2.0e-5,
            "projector_stress": 3.0e-5,
            "R_eq_guard": 0.0,
            "uses_readout_projector_mask": False,
            "uses_closed_wrong_current": False,
            "input_status": "PROJECTOR_DOMAIN_DRIFT_NONZERO",
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE4001_3_reference_frame_leak",
            "route": "reference_frame_denominator_bound",
            "C_M": 0.0,
            "C_shape": 0.0,
            "C_curl": 1.0e-6,
            "C_domain": 0.0,
            "C_ref": 3.0e-6,
            "C_frame": 5.0e-6,
            "C_units": 7.0e-6,
            "I_commutator_abs": 0.0,
            "projector_stress": 0.0,
            "R_eq_guard": 0.0,
            "uses_readout_projector_mask": False,
            "uses_closed_wrong_current": False,
            "input_status": "REFERENCE_FRAME_UNITS_NONZERO",
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE4001_4_closed_wrong_current_refused",
            "route": "closed_topological_but_not_Hilbert_source",
            "C_M": 0.0,
            "C_shape": 0.0,
            "C_curl": 0.0,
            "C_domain": 0.0,
            "C_ref": 0.0,
            "C_frame": 0.0,
            "C_units": 0.0,
            "I_commutator_abs": 0.0,
            "projector_stress": 0.0,
            "R_eq_guard": 0.0,
            "uses_readout_projector_mask": False,
            "uses_closed_wrong_current": True,
            "input_status": "CLOSED_WRONG_CURRENT_NOT_NEWTON_SOURCE",
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE4001_5_readout_mask_refused",
            "route": "forbidden_post_readout_projector",
            "C_M": 0.0,
            "C_shape": 0.0,
            "C_curl": 0.0,
            "C_domain": 0.0,
            "C_ref": 0.0,
            "C_frame": 0.0,
            "C_units": 0.0,
            "I_commutator_abs": 0.0,
            "projector_stress": 0.0,
            "R_eq_guard": 0.0,
            "uses_readout_projector_mask": True,
            "uses_closed_wrong_current": False,
            "input_status": "POST_READOUT_PIM_MASK_FORBIDDEN",
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE4001_6_missing_parent_rows",
            "route": "missing_projector_component_vector",
            "C_M": "",
            "C_shape": "",
            "C_curl": "",
            "C_domain": "",
            "C_ref": "",
            "C_frame": "",
            "C_units": "",
            "I_commutator_abs": "",
            "projector_stress": "",
            "R_eq_guard": "",
            "uses_readout_projector_mask": False,
            "uses_closed_wrong_current": False,
            "input_status": "MISSING_PIM_COMPONENT_VECTOR",
            "timestamp_utc": timestamp,
        },
    ]


NUMERIC_FIELDS = [
    "C_M",
    "C_shape",
    "C_curl",
    "C_domain",
    "C_ref",
    "C_frame",
    "C_units",
    "I_commutator_abs",
    "projector_stress",
    "R_eq_guard",
]


def optional_float(value: Any) -> float | None:
    text = str(value).strip()
    if not text or text.upper().startswith("MISSING"):
        return None
    return float(text)


def as_bool(value: Any) -> bool:
    return str(value).strip().lower() == "true"


def evaluate_case(row: dict[str, Any]) -> dict[str, Any]:
    values = {field: optional_float(row.get(field)) for field in NUMERIC_FIELDS}
    readout_mask = as_bool(row.get("uses_readout_projector_mask"))
    wrong_current = as_bool(row.get("uses_closed_wrong_current"))
    result: dict[str, Any] = {
        "case_id": row["case_id"],
        "route": row["route"],
        "input_status": row["input_status"],
        "Delta_PiM_4001": "MISSING",
        "epsilon_source_connection_abs": "MISSING",
        "epsilon_integrability_reference_abs": "MISSING",
        "epsilon_domain_projector_abs": "MISSING",
        "epsilon_guard_abs": "MISSING",
        "uses_readout_projector_mask": readout_mask,
        "uses_closed_wrong_current": wrong_current,
        "passes_schema": False,
        "passes_no_readout_mask": not readout_mask,
        "passes_hilbert_current_guard": not wrong_current,
        "conditional_zero_theorem_applies": False,
        "bound_ready": False,
        "claim_allowed": False,
        "valid_for_claim": False,
    }
    if any(value is None for value in values.values()):
        return result
    source_connection = abs(values["C_M"] or 0.0) + abs(values["C_shape"] or 0.0)
    integrability_reference = abs(values["C_curl"] or 0.0) + abs(values["C_ref"] or 0.0) + abs(values["C_frame"] or 0.0) + abs(values["C_units"] or 0.0)
    domain_projector = abs(values["C_domain"] or 0.0) + abs(values["I_commutator_abs"] or 0.0) + abs(values["projector_stress"] or 0.0)
    guard = abs(values["R_eq_guard"] or 0.0)
    total = source_connection + integrability_reference + domain_projector + guard
    result.update(
        {
            "Delta_PiM_4001": f"{total:.12e}",
            "epsilon_source_connection_abs": f"{source_connection:.12e}",
            "epsilon_integrability_reference_abs": f"{integrability_reference:.12e}",
            "epsilon_domain_projector_abs": f"{domain_projector:.12e}",
            "epsilon_guard_abs": f"{guard:.12e}",
            "passes_schema": True,
            "passes_no_readout_mask": not readout_mask,
            "passes_hilbert_current_guard": not wrong_current,
            "conditional_zero_theorem_applies": total == 0.0 and not readout_mask and not wrong_current,
            "bound_ready": not readout_mask and not wrong_current,
        }
    )
    return result


def result_rows(cases: list[dict[str, Any]], timestamp: str) -> list[dict[str, Any]]:
    rows = [evaluate_case(row) for row in cases]
    for row in rows:
        row["timestamp_utc"] = timestamp
    return rows


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC4001_0",
            "finding": "Pi_M commutator silence is derivable as a conditional fixed-chainmap theorem, not an axiom.",
            "evidence": "If Pi_M is a parent-selected chain-map on the physical Hilbert current complex and fixed on the same annulus before readout, then [d,Pi_M]J_H=0.",
            "limitation": "current corpus still lacks parent selector, fixed source-domain, physical current complex, and Hilbert/topological equality signatures.",
            "next_action": NEXT_DOC,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC4001_1",
            "finding": "The quotient-source-coordinate route kills only the source-connection part unless H_tau/H_ref are also locked.",
            "evidence": "Y=Ybar(q(Phi)) and Dq(v_X)=0 eliminate C_M/C_shape, but C_curl, C_ref, frame, and units remain explicit.",
            "limitation": "H_tau integrability and H_ref source-blind reference are now the sharp next blockers.",
            "next_action": "derive H_tau/H_ref integrability-reference lock or retain C_curl/C_ref bounds",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "CLAIM4001_0_projector_silence",
            "claim": "D_A Pi_M=0 and [d,Pi_M]J_H=0 are proven for current MTS",
            "allowed": False,
            "reason": "fixed-chainmap theorem is conditional; parent selector/domain/current/Hilbert-equality signatures remain unsigned",
            "required_exit": "sign all parent-chainmap clauses on the same annulus or supply source-backed Delta_PiM component bounds",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "CLAIM4001_1_local_GR_Newton",
            "claim": "local GR/Newton source denominator is complete",
            "allowed": False,
            "reason": "projector route now has a theorem branch but C_curl/C_ref/frame/units and calibration gates remain open",
            "required_exit": NEXT_DOC,
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "CLAIM4001_2_readout_projector",
            "claim": "post-readout Pi_M masks can be used to close source mass",
            "allowed": False,
            "reason": "readout masks are explicitly refused by the evaluator and contract",
            "required_exit": "parent-selected Pi_M before variation",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "CLAIM4001_3_closed_wrong_current",
            "claim": "any closed topological current proves Newton mass",
            "allowed": False,
            "reason": "closed current must equal the observed Hilbert source with zero boundary exact term and same denominator",
            "required_exit": "Pi_M J_H=J_M_top+dB_zero plus zero linked boundary flux",
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "NEXT4001_0",
            "next_doc": NEXT_DOC,
            "next_script": NEXT_SCRIPT,
            "target": "derive H_tau/H_ref integrability and source-blind reference lock, or retain explicit C_curl/C_ref/C_units bounds",
            "success_condition": "curl(delta H_tau)=0 and H_ref is source-blind/fixed on the same tau/e_obs/source branch, or C_curl, C_ref, C_frame, and C_units are numeric/source-backed nonclaim rows",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status": "PARENT_PROJECTOR_CONSTANCY_OR_PIM_COMMUTATOR_BOUND",
            "headline": "Pi_M silence is reduced to a fixed parent chain-map theorem; if unsigned, Delta_PiM_4001 is an explicit component vector and readout masks/closed-wrong-currents are refused.",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def write_doc(timestamp: str, sources: list[dict[str, Any]], results: list[dict[str, Any]]) -> None:
    found = sum(bool(row["needle_found"]) for row in sources)
    lines = [
        "# 4001 - Parent Projector Constancy Or PiM Commutator Bound",
        "",
        f"Timestamp: `{timestamp}`",
        "",
        "## Result",
        "",
        "`Pi_M` is no longer a fuzzy projector word. It has one clean zero route and one explicit failure vector.",
        "",
        "Zero route:",
        "",
        "`Pi_M:C_H(A_ext)->C_M(A_ext)` is a parent-selected fixed chain-map on the physical Hilbert current complex, on the same annulus, same `tau`, same `e_obs`, same reference, and before readout.",
        "",
        "Then",
        "",
        "`d(Pi_M J_H)=Pi_M dJ_H + [d,Pi_M]J_H`, and `[d,Pi_M]J_H=0`.",
        "",
        "## Constancy Conditions",
        "",
        "`D_A Pi_M=0` requires the parent branch to fix `A_ext`, `W_source`, linked surfaces, orientation, `tau`, `e_obs`/Hodge data, reference subtraction, and the `M_H_ref` denominator before any scoring.",
        "",
        "A topological/absolute-charge `Pi_M` can be stress-silent. A Hodge, Green, domain, or fitted/readout implementation cannot be used silently; its variation stress or operator bound must be retained.",
        "",
        "## Quotient Route",
        "",
        "If `Y=(M_H_ref,sigma^a)=Ybar(q(Phi))` and `v_X in ker(Dq)`, then `D_XY=0`, so `C_M` and `C_shape` vanish. This is only a partial projector/source-connection zero unless `H_tau`, `H_ref`, frame, units, and domain/reference clauses are also locked.",
        "",
        "## Bound If Closure Fails",
        "",
        "`Delta_PiM_4001 = |C_M|+|C_shape|+|C_curl|+|C_domain|+|C_ref|+|C_frame|+|C_units|+|I_commutator_abs|+|projector_stress|+|R_eq_guard|`.",
        "",
        "The evaluator refuses both a post-readout mask and a closed wrong current. A closed topological current is not enough unless it is the observed Hilbert/Newton source with the same denominator.",
        "",
        "## Evaluator Results",
        "",
    ]
    for row in results:
        lines.append(
            f"- `{row['case_id']}`: status `{row['input_status']}`, Delta `{row['Delta_PiM_4001']}`, zero={row['conditional_zero_theorem_applies']}, no_readout={row['passes_no_readout_mask']}, Hilbert_guard={row['passes_hilbert_current_guard']}, claim={row['claim_allowed']}"
        )
    lines.extend(
        [
            "",
            "## Verdict",
            "",
            "This is progress but not a local-GR/Newton claim: the algebraic projector zero branch is sharp, yet current MTS still needs parent signatures or source-backed values for the component vector.",
            "",
            "## Next Target",
            "",
            "The next best move is `H_tau/H_ref`: prove integrability and source-blind reference lock, or carry `C_curl`, `C_ref`, `C_frame`, and `C_units` as explicit bounds.",
            "",
            f"- `{NEXT_DOC}`",
            f"- `{NEXT_SCRIPT}`",
            "",
            "## Source Count",
            "",
            f"- source needles found: `{found}/{len(sources)}`",
            "",
        ]
    )
    DOC_PATH.write_text("\n".join(lines), encoding="utf-8")


def append_spine(timestamp: str) -> None:
    marker = "## 4001 - PiM Projector Constancy"
    block = f"""

{marker}

- Timestamp: `{timestamp}`
- Result: `Pi_M` silence is reduced to a fixed parent chain-map theorem on the physical Hilbert current complex: if `d Pi_M=Pi_M d`, `D_A Pi_M=0`, and `J_H` is in the same complex before readout, then `[d,Pi_M]J_H=0`.
- Bound route: `Delta_PiM_4001 = |C_M|+|C_shape|+|C_curl|+|C_domain|+|C_ref|+|C_frame|+|C_units|+|I_commutator_abs|+|projector_stress|+|R_eq_guard|`.
- Guards: post-readout `Pi_M` masks and closed-but-wrong topological currents are refused.
- Claim status: conditional theorem plus executable residual vector; no local-GR/Newton claim yet.
- Next: `{NEXT_DOC}`.
"""
    current = read_text(SPINE_PATH) if SPINE_PATH.exists() else ""
    if marker not in current:
        SPINE_PATH.write_text(current.rstrip() + block + "\n", encoding="utf-8")


def build_validation_rows(
    timestamp: str,
    sources: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    audit: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    results: list[dict[str, Any]],
    compile_ok: bool,
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        checks.append({"check_id": check_id, "passed": bool(passed), "detail": detail, "timestamp_utc": timestamp})

    source_paths = [Path(row["path"]) for row in sources]
    add("VAL4001_00_sources_exist", all(path.exists() for path in source_paths), "every cited source path exists")
    add("VAL4001_01_needles_found", all(bool(row["needle_found"]) for row in sources), "every cited source needle found")
    add("VAL4001_02_product_rule", any(row["theorem_id"] == "PCM4001_0_product_rule" for row in theorem), "product rule present")
    add("VAL4001_03_chainmap_zero", any(row["theorem_id"] == "PCM4001_1_fixed_chainmap_zero" for row in theorem), "fixed-chainmap theorem present")
    add("VAL4001_04_parent_constancy", any(row["theorem_id"] == "PCM4001_2_parent_constancy_branch" for row in theorem), "parent constancy theorem present")
    add("VAL4001_05_quotient_route", any(row["theorem_id"] == "PCM4001_3_quotient_source_connection_zero" for row in theorem), "quotient source route present")
    add("VAL4001_06_wrong_current_guard", any(row["theorem_id"] == "PCM4001_4_closed_wrong_current_guard" for row in theorem), "closed wrong current guard present")
    add("VAL4001_07_bound_theorem", any(row["theorem_id"] == "PCM4001_5_absolute_bound_if_not_zero" for row in theorem), "bound theorem present")
    add("VAL4001_08_current_verdict", any(row["theorem_id"] == "PCM4001_6_current_verdict" for row in theorem), "current verdict present")
    add("VAL4001_09_audit_verdict", any(row["audit_id"] == "PZA4001_7_zero_proof_verdict" for row in audit), "zero-proof audit verdict present")
    add("VAL4001_10_readout_audit", any(row["audit_id"] == "PZA4001_6_readout_firewall" for row in audit), "readout firewall audit present")
    add("VAL4001_11_master_bound", any(row["bound_id"] == "PMB4001_0_master" for row in bounds), "master bound present")
    add("VAL4001_12_curl_ref_bounds", any(row["bound_id"] == "PMB4001_3_C_curl" for row in bounds) and any(row["bound_id"] == "PMB4001_5_C_ref" for row in bounds), "curl/ref bounds present")
    zero = next(row for row in results if row["case_id"] == "CASE4001_0_fixed_chainmap_zero")
    partial = next(row for row in results if row["case_id"] == "CASE4001_1_quotient_descent_partial")
    domain = next(row for row in results if row["case_id"] == "CASE4001_2_domain_projector_drift")
    ref = next(row for row in results if row["case_id"] == "CASE4001_3_reference_frame_leak")
    wrong = next(row for row in results if row["case_id"] == "CASE4001_4_closed_wrong_current_refused")
    readout = next(row for row in results if row["case_id"] == "CASE4001_5_readout_mask_refused")
    missing = next(row for row in results if row["case_id"] == "CASE4001_6_missing_parent_rows")
    add("VAL4001_13_zero_case", float(zero["Delta_PiM_4001"]) == 0.0 and str(zero["conditional_zero_theorem_applies"]).lower() == "true", "zero theorem case clean")
    add("VAL4001_14_partial_case", float(partial["epsilon_source_connection_abs"]) == 0.0 and float(partial["epsilon_integrability_reference_abs"]) > 0.0, "quotient descent partial case retains Htau/Href debt")
    add("VAL4001_15_domain_case", float(domain["epsilon_domain_projector_abs"]) > 0.0, "domain projector drift produces residual")
    add("VAL4001_16_ref_case", float(ref["epsilon_integrability_reference_abs"]) > 0.0, "reference/frame leak produces residual")
    add("VAL4001_17_wrong_current_refused", str(wrong["passes_schema"]).lower() == "true" and str(wrong["passes_hilbert_current_guard"]).lower() == "false", "closed wrong current refused")
    add("VAL4001_18_readout_refused", str(readout["passes_schema"]).lower() == "true" and str(readout["passes_no_readout_mask"]).lower() == "false", "readout PiM mask refused")
    add("VAL4001_19_missing_blocks", missing["Delta_PiM_4001"] == "MISSING" and str(missing["passes_schema"]).lower() == "false", "missing parent rows block")
    add("VAL4001_20_claim_gate_false", all(str(row.get("allowed", "")).lower() == "false" for row in read_csv(OUTPUTS["claim_gate"])), "all claim gates false")
    add("VAL4001_21_next_target", OUTPUTS["next"].exists() and NEXT_DOC in read_text(OUTPUTS["next"]), "next target written")
    add("VAL4001_22_doc_exists", DOC_PATH.exists() and "closed wrong current" in read_text(DOC_PATH) and "post-readout mask" in read_text(DOC_PATH), "document written")
    add("VAL4001_23_spine_updated", SPINE_PATH.exists() and "## 4001 - PiM Projector Constancy" in read_text(SPINE_PATH), "spine updated")
    add("VAL4001_24_no_fwb_outputs", not any(str(path).startswith(str(FWB)) for path in OUTPUTS.values()), "no outputs target formalization-workbench")
    add("VAL4001_25_compile", compile_ok, "script compiles")
    add("VAL4001_26_no_pycache", not (SCRIPT_PATH.parent / "__pycache__").exists(), "script __pycache__ removed")
    add("VAL4001_27_status_exists", OUTPUTS["status"].exists(), "status file exists")
    add("VAL4001_28_results_nonclaim", all(str(row.get("valid_for_claim", "")).lower() == "false" for row in results), "all evaluator results remain nonclaim")
    add("VAL4001_29_no_nan", not any("nan" in str(row).lower() or "inf" in str(row).lower() for row in results), "no nan/inf evaluator outputs")
    add("VAL4001_30_same_annulus_guard", DOC_PATH.exists() and "same annulus" in read_text(DOC_PATH), "same-annulus guard recorded")
    add("VAL4001_31_no_readout_policy", DOC_PATH.exists() and "before readout" in read_text(DOC_PATH), "before-readout policy recorded")
    return checks


def main() -> None:
    timestamp = now_utc()
    sources = source_register_rows(timestamp)
    theorem = theorem_rows(timestamp)
    audit = audit_rows(timestamp)
    bounds = bound_rows(timestamp)
    cases = case_rows(timestamp)
    results = result_rows(cases, timestamp)
    decisions = decision_rows(timestamp)
    claims = claim_gate_rows(timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["theorem"], theorem)
    write_csv(OUTPUTS["audit"], audit)
    write_csv(OUTPUTS["bounds"], bounds)
    write_csv(OUTPUTS["cases"], cases)
    write_csv(OUTPUTS["results"], results)
    write_csv(OUTPUTS["decision"], decisions)
    write_csv(OUTPUTS["claim_gate"], claims)
    write_csv(OUTPUTS["next"], next_target)
    write_csv(OUTPUTS["status"], status)
    write_doc(timestamp, sources, results)
    append_spine(timestamp)

    compile_ok = True
    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
    except py_compile.PyCompileError:
        compile_ok = False
    cache = SCRIPT_PATH.parent / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)

    validation = build_validation_rows(timestamp, sources, theorem, audit, bounds, results, compile_ok)
    write_csv(OUTPUTS["validation"], validation)
    passed = sum(1 for row in validation if row["passed"])
    total = len(validation)
    print(f"4001 validation: {passed}/{total} passed")
    if passed != total:
        for row in validation:
            if not row["passed"]:
                print(f"FAIL {row['check_id']}: {row['detail']}")
        raise SystemExit(1)
    print(f"Wrote {DOC_PATH}")


if __name__ == "__main__":
    main()
