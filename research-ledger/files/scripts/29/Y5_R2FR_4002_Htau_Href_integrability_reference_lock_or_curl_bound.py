from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "4002"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "4002-Y5-R2FR-Htau-Href-integrability-reference-lock-or-curl-bound.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_4002_SOURCE_REGISTER.csv",
    "theorem": SRC / "P8_Y5_R2FR_4002_HTAU_HREF_THEOREM.csv",
    "audit": SRC / "P8_Y5_R2FR_4002_INTEGRABILITY_REFERENCE_AUDIT.csv",
    "bounds": SRC / "P8_Y5_R2FR_4002_CURL_REFERENCE_BOUND_VECTOR.csv",
    "cases": SRC / "P8_Y5_R2FR_4002_EVALUATOR_CASES.csv",
    "results": SRC / "P8_Y5_R2FR_4002_EVALUATOR_RESULTS.csv",
    "decision": SRC / "P8_Y5_R2FR_4002_DECISION_GATE.csv",
    "claim_gate": SRC / "P8_Y5_R2FR_4002_CLAIM_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_4002_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_4002_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_4002_VALIDATION.csv",
}

NEXT_DOC = "4003-Y5-R2FR-parent-theta-Qtau-current-chain-or-integrability-source-row.md"
NEXT_SCRIPT = "scripts/Y5_R2FR_4003_parent_theta_Qtau_current_chain_or_integrability_source_row.py"


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
        ("SRC4002_00_next", SRC / "P8_Y5_R2FR_4001_NEXT_TARGET.csv", "NEXT4001_0", "4001 handoff"),
        ("SRC4002_01_4001_bounds", SRC / "P8_Y5_R2FR_4001_PIM_COMMUTATOR_BOUND_VECTOR.csv", "PMB4001_3_C_curl", "4001 curl/ref handoff"),
        ("SRC4002_02_3514_curl", SRC / "P8_EM_PiM_Htau_commutator_residual_law.csv", "PHCR3514_3_C_curl", "H_tau curl component"),
        ("SRC4002_03_3514_ref", SRC / "P8_EM_PiM_Htau_commutator_residual_law.csv", "PHCR3514_5_C_ref", "H_ref component"),
        ("SRC4002_04_1645_oneform", SRC / "P8_Y5_PARENT_QLOC_1645_HTAU_INTEGRABILITY_THEOREM.csv", "HTM1645_0_phase_space_one_form", "Hamiltonian one-form"),
        ("SRC4002_05_1645_criterion", SRC / "P8_Y5_PARENT_QLOC_1645_HTAU_INTEGRABILITY_THEOREM.csv", "HTM1645_1_integrability_criterion", "integrability criterion"),
        ("SRC4002_06_1645_curl", SRC / "P8_Y5_PARENT_QLOC_1645_HTAU_INTEGRABILITY_THEOREM.csv", "HTM1645_2_curl_decomposition", "curl decomposition"),
        ("SRC4002_07_1645_ref", SRC / "P8_Y5_PARENT_QLOC_1645_HTAU_INTEGRABILITY_THEOREM.csv", "HTM1645_3_fixed_reference_law", "fixed reference law"),
        ("SRC4002_08_1796_attempt", SRC / "P8_Y5_PARENT_QLOC_1796_INTEGRABILITY_REFERENCE_ATTEMPT.csv", "HIR1796_6_verdict", "integrability/reference attempt verdict"),
        ("SRC4002_09_1797_zero", SRC / "P8_Y5_PARENT_QLOC_1797_DELTA_INTEGRABILITY_ZERO_PROOF_ATTEMPT.csv", "ZP1797_5_verdict", "zero proof verdict"),
        ("SRC4002_10_1798_components", SRC / "P8_Y5_PARENT_QLOC_1798_DELTAH_CURL_COMPONENT_PACK.csv", "DCC1798_8_total_abs_envelope", "deltaH curl component pack"),
        ("SRC4002_11_2547_ref", SRC / "P8_Y5_NO_SHADOW_2547_FIXED_REFERENCE_SELECTOR_THEOREM.csv", "FRS2547_4_no_shortcuts", "fixed reference no shortcuts"),
        ("SRC4002_12_2382_ref", SRC / "P8_Y5_PARENT_QLOC_2382_FIXED_REFERENCE_SELECTOR_THEOREM.csv", "FRT2382_2_source_blind_chain_rule", "source-blind reference chain rule"),
        ("SRC4002_13_2339_audit", SRC / "P8_Y5_PARENT_QLOC_2339_THETA_QTAU_FIXED_REFERENCE_AUDIT.csv", "TQF2339_4_Htau_integrability", "theta/Qtau/Href audit"),
        ("SRC4002_14_2340_row", SRC / "P8_Y5_PARENT_QLOC_2340_HTAU_HREF_SOURCE_ROW.csv", "HHS2340_0_source_row", "Htau/Href source row schema"),
        ("SRC4002_15_2351_status", SRC / "P8_Y5_PARENT_QLOC_2351_HTAU_HREF_SOURCE_ROW_STATUS.csv", "HHS2351_5_status", "Htau/Href row status"),
        ("SRC4002_16_boundary_chain", SRC / "P8_Y5_BOUNDARY_REFERENCE_CONDITIONAL_THEOREM_CHAIN.csv", "CT545_3_reference_symplectic_zero", "boundary/reference theorem chain"),
        ("SRC4002_17_obstructions", SRC / "P8_Y5_BOUNDARY_REFERENCE_OBSTRUCTION_LEDGER.csv", "BRO543_0_reference_shift", "boundary/reference obstruction ledger"),
        ("SRC4002_18_hamiltonian_contract", SRC / "P8_mass_current_Hamiltonian_boundary_charge_CONTRACT.csv", "HC2_differentiable_integrable_Hxi", "Hamiltonian integrability contract"),
        ("SRC4002_19_gauss_contract", SRC / "P8_Hamiltonian_charge_Poisson_Gauss_calibration_CONTRACT.csv", "PG1_charge_equals_projected_Hilbert_source", "Hamiltonian-to-source calibration guard"),
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
            "theorem_id": "HIR4002_0_phase_space_one_form",
            "claim_piece": "Hamiltonian charge one-form",
            "mathematical_form": "alpha_tau[delta Phi] := int_S(delta Q_tau^MTS - i_tau Theta_total) - delta H_ref",
            "derived_result": "H_tau is not a primitive scalar; it is the integral of a covariant phase-space one-form on an allowed local branch",
            "status": "EXACT_DEFINITION_CONDITIONAL_ON_PARENT_THETA_QTAU",
            "source_path": str(SRC / "P8_Y5_PARENT_QLOC_1645_HTAU_INTEGRABILITY_THEOREM.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "HIR4002_1_integrability_criterion",
            "claim_piece": "H_tau integrability criterion",
            "mathematical_form": "H_tau exists path-independently iff d_field alpha_tau(delta_1 Phi,delta_2 Phi)=0 on the allowed branch phase space",
            "derived_result": "curl(delta H_tau)=0 is the exact condition for a well-defined Hamiltonian source charge",
            "status": "EXACT_CONDITIONAL_THEOREM",
            "source_path": str(SRC / "P8_Y5_PARENT_QLOC_1645_HTAU_INTEGRABILITY_THEOREM.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "HIR4002_2_curl_decomposition",
            "claim_piece": "field-space curl obstruction split",
            "mathematical_form": "d alpha_tau = I_EH + I_X + I_projector + I_boundary + I_ref + I_tau + I_surface + I_Dq",
            "derived_result": "nonintegrability is not vague; it splits into extra-sector, projector, boundary/reference, tau, surface/frame, and quotient/current leakage terms",
            "status": "EXACT_OBSTRUCTION_DECOMPOSITION",
            "source_path": str(SRC / "P8_Y5_PARENT_QLOC_1798_DELTAH_CURL_COMPONENT_PACK.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "HIR4002_3_fixed_reference_selector",
            "claim_piece": "source-blind fixed H_ref",
            "mathematical_form": "H_ref=H_ref[Sigma_ref] and D_source Sigma_ref=D_r Sigma_ref=D_t Sigma_ref=D_frame Sigma_ref=D_readout Sigma_ref=0 imply D H_ref=0 in those directions",
            "derived_result": "the reference subtraction is legal only as fixed boundary/topology/asymptotic data, not as a fitted mass or GM counterterm",
            "status": "EXACT_CHAIN_RULE_ZERO_CONDITIONAL_ON_PARENT_SELECTOR",
            "source_path": str(SRC / "P8_Y5_PARENT_QLOC_2382_FIXED_REFERENCE_SELECTOR_THEOREM.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "HIR4002_4_MHref_denominator_lock",
            "claim_piece": "same-frame positive Hamiltonian denominator",
            "mathematical_form": "M_H_ref := H_tau[S_outer;tau,e_obs] - H_ref[Sigma_ref;tau,e_obs] > 0, with no orbital-GM import",
            "derived_result": "C_curl and C_ref can be normalized only after H_tau, H_ref, tau, coframe, surfaces, units, and positivity are owned together",
            "status": "DENOMINATOR_CONTRACT_NOT_SOURCE_FILLED",
            "source_path": str(SRC / "P8_Y5_PARENT_QLOC_2340_HTAU_HREF_SOURCE_ROW.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "HIR4002_5_zero_branch",
            "claim_piece": "conditional H_tau/H_ref zero theorem",
            "mathematical_form": "If one parent L gives Theta_total and Q_tau^MTS, alpha_tau is closed, H_ref is fixed/source-blind, tau/e_obs/surfaces are locked, and M_H_ref is positive/same-frame, then C_curl=C_ref=C_frame=C_units=0.",
            "derived_result": "the route to a legal Hamiltonian source denominator is real, but current corpus has not signed all clauses",
            "status": "DERIVED_CONDITIONAL_ZERO_THEOREM_NOT_CLAIM",
            "source_path": str(SRC / "P8_Y5_PARENT_QLOC_1796_INTEGRABILITY_REFERENCE_ATTEMPT.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "HIR4002_6_bound_if_not_zero",
            "claim_piece": "failed integrability/reference lock becomes a residual vector",
            "mathematical_form": "Delta_Htau_Href_4002 = |I_X|+|I_projector|+|I_boundary|+|I_ref|+|I_tau|+|I_surface|+|I_Dq|+|Delta_ref|+|C_frame|+|C_units|",
            "derived_result": "if the theorem branch is unsigned, H_tau/H_ref debt remains no-cancellation input to Newton, PPN, R10, Gdot, and local-GR gates",
            "status": "EXECUTABLE_BOUND_VECTOR",
            "source_path": str(SRC / "P8_Y5_PARENT_QLOC_1798_DELTAH_CURL_COMPONENT_PACK.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def audit_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "audit_id": "HRA4002_0_parent_theta_Qtau",
            "clause": "one parent action owns Theta_total and Q_tau^MTS",
            "required_signature": "delta L_parent=E_A delta Phi^A+dTheta_total and J_tau=Theta_total(L_tau Phi)-i_tau L=dQ_tau^MTS+C_tau",
            "current_evidence": "conditional route exists but total parent theta/Q_tau extraction remains missing",
            "verdict": "OPEN_PARENT_CURRENT_CHAIN",
            "feeds_bound": "I_X;I_projector;I_boundary;I_Dq",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "HRA4002_1_field_space_closure",
            "clause": "alpha_tau is closed on the allowed local branch",
            "required_signature": "d_field alpha_tau=0 after all retained sector, boundary, projector, tau, surface and quotient terms are included",
            "current_evidence": "curl decomposition exists; zero proof not closed",
            "verdict": "OPEN_CURL_COMPONENTS",
            "feeds_bound": "C_curl",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "HRA4002_2_fixed_reference",
            "clause": "H_ref is fixed before source, radius, time, frame and readout changes",
            "required_signature": "H_ref=H_ref[Sigma_ref] with Sigma_ref source-blind and no GM/fitted-mass labels",
            "current_evidence": "source-blind chain rule is derived as a contract; parent selector is unsigned",
            "verdict": "OPEN_REFERENCE_SELECTOR",
            "feeds_bound": "C_ref;Delta_ref",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "HRA4002_3_tau_frame_surface",
            "clause": "same tau/coframe/surfaces define source, charge, denominator and readout",
            "required_signature": "tau_source=tau_charge=tau_MHref=tau_readout, same e_obs/coframe, fixed S_outer/S_ref",
            "current_evidence": "same-frame lock remains unsigned",
            "verdict": "OPEN_FRAME_SURFACE_LOCK",
            "feeds_bound": "I_tau;I_surface;C_frame",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "HRA4002_4_positive_denominator",
            "clause": "M_H_ref is finite positive same-frame and not orbital-GM backfilled",
            "required_signature": "numeric/source-backed H_tau, H_ref, units, tau_id, coframe_id, positivity and no_orbital_GM_import certificate",
            "current_evidence": "source row schema exists; current value missing",
            "verdict": "OPEN_MHREF_SOURCE_ROW",
            "feeds_bound": "C_units;normalization",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "HRA4002_5_no_fitted_reference",
            "clause": "H_ref cannot be chosen to cancel the observed residual",
            "required_signature": "partial_{GM_obs,M_fit,residual,readout} Sigma_ref=0 and same for counterterms",
            "current_evidence": "guardrail exists and evaluator refuses fitted reference cases",
            "verdict": "GUARD_ACTIVE",
            "feeds_bound": "fitted_reference_guard",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "HRA4002_6_zero_proof_verdict",
            "clause": "C_curl=C_ref=C_frame=C_units=0",
            "required_signature": "HRA4002_0 through HRA4002_4 close in one parent branch",
            "current_evidence": "conditional theorem built; current MTS needs parent current chain or source-backed rows",
            "verdict": "CONDITIONAL_ZERO_BRANCH_PLUS_BOUND_VECTOR",
            "feeds_bound": "Delta_Htau_Href_4002",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def bound_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "bound_id": "HRB4002_0_master",
            "target": "Delta_Htau_Href_4002",
            "formula": "|I_X|+|I_projector|+|I_boundary|+|I_ref|+|I_tau|+|I_surface|+|I_Dq|+|Delta_ref|+|C_frame|+|C_units|",
            "numeric_value": "MISSING_PARENT_SIGNED_COMPONENTS",
            "units": "dimensionless",
            "status": "EXECUTABLE_VECTOR_READY",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "HRB4002_1_I_X",
            "target": "I_X",
            "formula": "|d_field alpha_tau^X|/M_H_ref",
            "numeric_value": "MISSING_EXTRA_SECTOR_THETA_QTAU_OR_ZERO",
            "units": "dimensionless",
            "status": "OPEN_PARENT_CURRENT_CHAIN",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "HRB4002_2_I_projector",
            "target": "I_projector",
            "formula": "|d_field alpha_tau^projector|/M_H_ref",
            "numeric_value": "ZERO_IF_4001_CHAINMAP_AND_PROJECTOR_STRESS_CLOSE_ELSE_BOUND_REQUIRED",
            "units": "dimensionless",
            "status": "LINKS_TO_4001_PROJECTOR_GATE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "HRB4002_3_I_boundary",
            "target": "I_boundary",
            "formula": "|d_field alpha_tau^boundary|/M_H_ref",
            "numeric_value": "MISSING_BOUNDARY_REFERENCE_OWNER",
            "units": "dimensionless",
            "status": "OPEN_BOUNDARY_REFERENCE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "HRB4002_4_I_ref_Delta_ref",
            "target": "I_ref + Delta_ref",
            "formula": "|curl(delta H_ref)|/M_H_ref + |H_ref_shift_or_unfixed_counterterm|/M_H_ref",
            "numeric_value": "MISSING_FIXED_REFERENCE_SELECTOR_OR_BOUND",
            "units": "dimensionless",
            "status": "OPEN_REFERENCE_SELECTOR",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "HRB4002_5_I_tau_surface",
            "target": "I_tau + I_surface + C_frame",
            "formula": "|curl_tau alpha_tau|/M_H_ref + |curl_surface alpha_tau|/M_H_ref + |D_X ln(tau,e_obs,Sigma,frame)|",
            "numeric_value": "MISSING_SAME_FRAME_TAU_SURFACE_LOCK",
            "units": "dimensionless",
            "status": "OPEN_FRAME_SURFACE_LOCK",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "HRB4002_6_I_Dq",
            "target": "I_Dq",
            "formula": "|Dq_current_leak + source_readout_Dq_leak + coupling_marker_leak|/M_H_ref",
            "numeric_value": "MISSING_Q_DQ_DESCENT_OR_BOUND",
            "units": "dimensionless",
            "status": "OPEN_QUOTIENT_CURRENT_LEAK",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "HRB4002_7_C_units",
            "target": "C_units",
            "formula": "D_X ln(Pi_M H_tau denominator units) plus M_H_ref positivity/source/unit sidecar",
            "numeric_value": "MISSING_POSITIVE_SAME_FRAME_MHREF",
            "units": "dimensionless",
            "status": "OPEN_DENOMINATOR_SIDECAR",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def case_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "case_id": "CASE4002_0_integrable_fixed_reference_zero",
            "route": "parent_theta_Qtau_closed_reference_locked",
            "I_X": 0.0,
            "I_projector": 0.0,
            "I_boundary": 0.0,
            "I_ref": 0.0,
            "I_tau": 0.0,
            "I_surface": 0.0,
            "I_Dq": 0.0,
            "Delta_ref": 0.0,
            "C_frame": 0.0,
            "C_units": 0.0,
            "uses_fitted_reference": False,
            "uses_orbital_GM_denominator": False,
            "input_status": "CONDITIONAL_ZERO_CLAUSES_UNSIGNED",
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE4002_1_parent_current_missing",
            "route": "theta_Qtau_missing_curl_components",
            "I_X": 2.0e-6,
            "I_projector": 3.0e-6,
            "I_boundary": 1.0e-6,
            "I_ref": 0.0,
            "I_tau": 0.0,
            "I_surface": 0.0,
            "I_Dq": 4.0e-6,
            "Delta_ref": 0.0,
            "C_frame": 0.0,
            "C_units": 0.0,
            "uses_fitted_reference": False,
            "uses_orbital_GM_denominator": False,
            "input_status": "PARENT_THETA_QTAU_COMPONENTS_NONZERO",
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE4002_2_reference_drift",
            "route": "unfixed_reference_selector",
            "I_X": 0.0,
            "I_projector": 0.0,
            "I_boundary": 0.0,
            "I_ref": 5.0e-6,
            "I_tau": 0.0,
            "I_surface": 0.0,
            "I_Dq": 0.0,
            "Delta_ref": 7.0e-6,
            "C_frame": 0.0,
            "C_units": 0.0,
            "uses_fitted_reference": False,
            "uses_orbital_GM_denominator": False,
            "input_status": "REFERENCE_SELECTOR_DRIFT_NONZERO",
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE4002_3_tau_frame_units_leak",
            "route": "same_frame_denominator_not_locked",
            "I_X": 0.0,
            "I_projector": 0.0,
            "I_boundary": 0.0,
            "I_ref": 0.0,
            "I_tau": 2.0e-6,
            "I_surface": 3.0e-6,
            "I_Dq": 0.0,
            "Delta_ref": 0.0,
            "C_frame": 5.0e-6,
            "C_units": 7.0e-6,
            "uses_fitted_reference": False,
            "uses_orbital_GM_denominator": False,
            "input_status": "TAU_FRAME_UNITS_NONZERO",
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE4002_4_fitted_reference_refused",
            "route": "forbidden_reference_laundering",
            "I_X": 0.0,
            "I_projector": 0.0,
            "I_boundary": 0.0,
            "I_ref": 0.0,
            "I_tau": 0.0,
            "I_surface": 0.0,
            "I_Dq": 0.0,
            "Delta_ref": 0.0,
            "C_frame": 0.0,
            "C_units": 0.0,
            "uses_fitted_reference": True,
            "uses_orbital_GM_denominator": False,
            "input_status": "FITTED_REFERENCE_FORBIDDEN",
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE4002_5_orbital_denominator_refused",
            "route": "forbidden_orbital_GM_MHref",
            "I_X": 0.0,
            "I_projector": 0.0,
            "I_boundary": 0.0,
            "I_ref": 0.0,
            "I_tau": 0.0,
            "I_surface": 0.0,
            "I_Dq": 0.0,
            "Delta_ref": 0.0,
            "C_frame": 0.0,
            "C_units": 0.0,
            "uses_fitted_reference": False,
            "uses_orbital_GM_denominator": True,
            "input_status": "ORBITAL_GM_DENOMINATOR_FORBIDDEN",
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE4002_6_missing_parent_rows",
            "route": "missing_Htau_Href_component_vector",
            "I_X": "",
            "I_projector": "",
            "I_boundary": "",
            "I_ref": "",
            "I_tau": "",
            "I_surface": "",
            "I_Dq": "",
            "Delta_ref": "",
            "C_frame": "",
            "C_units": "",
            "uses_fitted_reference": False,
            "uses_orbital_GM_denominator": False,
            "input_status": "MISSING_HTAU_HREF_COMPONENT_VECTOR",
            "timestamp_utc": timestamp,
        },
    ]


NUMERIC_FIELDS = [
    "I_X",
    "I_projector",
    "I_boundary",
    "I_ref",
    "I_tau",
    "I_surface",
    "I_Dq",
    "Delta_ref",
    "C_frame",
    "C_units",
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
    fitted_ref = as_bool(row.get("uses_fitted_reference"))
    orbital_denominator = as_bool(row.get("uses_orbital_GM_denominator"))
    result: dict[str, Any] = {
        "case_id": row["case_id"],
        "route": row["route"],
        "input_status": row["input_status"],
        "Delta_Htau_Href_4002": "MISSING",
        "epsilon_parent_current_abs": "MISSING",
        "epsilon_reference_abs": "MISSING",
        "epsilon_frame_units_abs": "MISSING",
        "uses_fitted_reference": fitted_ref,
        "uses_orbital_GM_denominator": orbital_denominator,
        "passes_schema": False,
        "passes_reference_guard": not fitted_ref,
        "passes_denominator_guard": not orbital_denominator,
        "conditional_zero_theorem_applies": False,
        "bound_ready": False,
        "claim_allowed": False,
        "valid_for_claim": False,
    }
    if any(value is None for value in values.values()):
        return result
    parent_current = (
        abs(values["I_X"] or 0.0)
        + abs(values["I_projector"] or 0.0)
        + abs(values["I_boundary"] or 0.0)
        + abs(values["I_Dq"] or 0.0)
    )
    reference = abs(values["I_ref"] or 0.0) + abs(values["Delta_ref"] or 0.0)
    frame_units = abs(values["I_tau"] or 0.0) + abs(values["I_surface"] or 0.0) + abs(values["C_frame"] or 0.0) + abs(values["C_units"] or 0.0)
    total = parent_current + reference + frame_units
    result.update(
        {
            "Delta_Htau_Href_4002": f"{total:.12e}",
            "epsilon_parent_current_abs": f"{parent_current:.12e}",
            "epsilon_reference_abs": f"{reference:.12e}",
            "epsilon_frame_units_abs": f"{frame_units:.12e}",
            "passes_schema": True,
            "passes_reference_guard": not fitted_ref,
            "passes_denominator_guard": not orbital_denominator,
            "conditional_zero_theorem_applies": total == 0.0 and not fitted_ref and not orbital_denominator,
            "bound_ready": not fitted_ref and not orbital_denominator,
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
            "decision_id": "DEC4002_0",
            "finding": "H_tau/H_ref can be made derivable only through a closed covariant phase-space one-form with a fixed source-blind reference.",
            "evidence": "alpha_tau and d_field alpha_tau give exact integrability and curl-obstruction criteria; H_ref source-blindness follows by selector chain rule.",
            "limitation": "current MTS has not parent-extracted Theta_total/Q_tau^MTS or supplied a positive source-backed M_H_ref row.",
            "next_action": NEXT_DOC,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC4002_1",
            "finding": "Fitted references and orbital-GM denominators are now executable failure cases, not informal warnings.",
            "evidence": "evaluator refuses both fitted H_ref and orbital-GM M_H_ref even when numerical residuals are zero.",
            "limitation": "the finite bound branch still needs component source rows if parent extraction fails.",
            "next_action": "derive parent theta/Q_tau current chain or fill first source-backed integrability row",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "CLAIM4002_0_Htau_integrability",
            "claim": "H_tau is a well-defined integrable source charge for current MTS",
            "allowed": False,
            "reason": "integrability theorem is conditional; parent Theta_total/Q_tau^MTS and curl-zero component signatures remain unsigned",
            "required_exit": NEXT_DOC,
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "CLAIM4002_1_fixed_reference",
            "claim": "H_ref is source-blind and fixed for current MTS",
            "allowed": False,
            "reason": "source-blind chain rule is derived but the parent Sigma_ref selector and positive same-frame M_H_ref are unsigned",
            "required_exit": "parent reference selector or source-backed Delta_ref row",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "CLAIM4002_2_Newton_denominator",
            "claim": "M_H_ref is the derived Newton source denominator",
            "allowed": False,
            "reason": "H_tau/H_ref source row is missing and orbital-GM import is refused",
            "required_exit": "numeric/source-backed H_tau, H_ref, M_H_ref with no orbital-GM import and positive same-frame units",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "CLAIM4002_3_local_GR",
            "claim": "local GR/Newton/PPN branch is complete",
            "allowed": False,
            "reason": "H_tau/H_ref lock is one denominator gate; source calibration, G, PPN and extra-sector gates remain active",
            "required_exit": "complete downstream source/Poisson/Gauss/PPN residual closure",
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "NEXT4002_0",
            "next_doc": NEXT_DOC,
            "next_script": NEXT_SCRIPT,
            "target": "derive the parent theta/Q_tau current chain for H_tau, or create the first source-backed integrability component row",
            "success_condition": "Theta_total and Q_tau^MTS are extracted from one parent action with retained sectors accounted for, or I_X/I_projector/I_boundary/I_Dq rows become numeric/source-backed nonclaim inputs",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status": "HTAU_HREF_INTEGRABILITY_REFERENCE_LOCK_OR_CURL_BOUND",
            "headline": "H_tau/H_ref lock is reduced to a closed phase-space one-form plus fixed source-blind reference theorem; otherwise Delta_Htau_Href_4002 is an explicit curl/reference/frame/unit vector.",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def write_doc(timestamp: str, sources: list[dict[str, Any]], results: list[dict[str, Any]]) -> None:
    found = sum(bool(row["needle_found"]) for row in sources)
    lines = [
        "# 4002 - Htau/Href Integrability Reference Lock Or Curl Bound",
        "",
        f"Timestamp: `{timestamp}`",
        "",
        "## Result",
        "",
        "`H_tau` is now treated as a Hamiltonian charge functional, not a name for whatever mass we need.",
        "",
        "Define the covariant phase-space one-form",
        "",
        "`alpha_tau[delta Phi] := int_S(delta Q_tau^MTS - i_tau Theta_total) - delta H_ref`.",
        "",
        "`H_tau` exists path-independently only if",
        "",
        "`d_field alpha_tau(delta_1 Phi, delta_2 Phi)=0`.",
        "",
        "## Reference Lock",
        "",
        "`H_ref=H_ref[Sigma_ref]` is legal only when `Sigma_ref` is fixed by boundary/topology/asymptotic data before source, radius, time, frame, readout, or orbital comparison.",
        "",
        "The chain rule gives source-blindness only if `D_source Sigma_ref=0`; fitted mass, observed `GM`, residual sign, and post-hoc counterterms are forbidden inputs.",
        "",
        "## Denominator Lock",
        "",
        "`M_H_ref := H_tau[S_outer;tau,e_obs] - H_ref[Sigma_ref;tau,e_obs] > 0`.",
        "",
        "It must be same-frame, source-backed, unit-declared, and not imported from orbital `GM`.",
        "",
        "## Bound If Closure Fails",
        "",
        "`Delta_Htau_Href_4002 = |I_X|+|I_projector|+|I_boundary|+|I_ref|+|I_tau|+|I_surface|+|I_Dq|+|Delta_ref|+|C_frame|+|C_units|`.",
        "",
        "This is the no-cancellation replacement for saying `H_tau/H_ref is missing`.",
        "",
        "## Evaluator Results",
        "",
    ]
    for row in results:
        lines.append(
            f"- `{row['case_id']}`: status `{row['input_status']}`, Delta `{row['Delta_Htau_Href_4002']}`, zero={row['conditional_zero_theorem_applies']}, ref_guard={row['passes_reference_guard']}, denom_guard={row['passes_denominator_guard']}, claim={row['claim_allowed']}"
        )
    lines.extend(
        [
            "",
            "## Verdict",
            "",
            "We have the proper derivation contract: closed phase-space one-form plus fixed source-blind reference plus positive same-frame denominator. Current MTS has the route, not the claim.",
            "",
            "## Next Target",
            "",
            "The sharpest next move is parent current extraction: derive `Theta_total` and `Q_tau^MTS` from one parent action with retained sectors included, or fill the first source-backed curl component row.",
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
    marker = "## 4002 - Htau/Href Integrability Reference Lock"
    block = f"""

{marker}

- Timestamp: `{timestamp}`
- Result: `H_tau` is defined through `alpha_tau[delta Phi]=int_S(delta Q_tau^MTS-i_tau Theta_total)-delta H_ref`; integrability requires `d_field alpha_tau=0`.
- Reference rule: `H_ref=H_ref[Sigma_ref]` is source-blind only if the parent fixes `Sigma_ref` before source/radius/time/frame/readout/orbital comparison.
- Denominator guard: `M_H_ref=H_tau-H_ref>0` must be same-frame/source-backed/unit-declared and cannot be imported from orbital `GM`.
- Bound route: `Delta_Htau_Href_4002=|I_X|+|I_projector|+|I_boundary|+|I_ref|+|I_tau|+|I_surface|+|I_Dq|+|Delta_ref|+|C_frame|+|C_units|`.
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
    add("VAL4002_00_sources_exist", all(path.exists() for path in source_paths), "every cited source path exists")
    add("VAL4002_01_needles_found", all(bool(row["needle_found"]) for row in sources), "every cited source needle found")
    add("VAL4002_02_oneform", any(row["theorem_id"] == "HIR4002_0_phase_space_one_form" for row in theorem), "phase-space one-form present")
    add("VAL4002_03_integrability", any(row["theorem_id"] == "HIR4002_1_integrability_criterion" for row in theorem), "integrability criterion present")
    add("VAL4002_04_curl_decomposition", any(row["theorem_id"] == "HIR4002_2_curl_decomposition" for row in theorem), "curl decomposition present")
    add("VAL4002_05_reference_selector", any(row["theorem_id"] == "HIR4002_3_fixed_reference_selector" for row in theorem), "fixed reference selector present")
    add("VAL4002_06_denominator_lock", any(row["theorem_id"] == "HIR4002_4_MHref_denominator_lock" for row in theorem), "MHref denominator lock present")
    add("VAL4002_07_zero_branch", any(row["theorem_id"] == "HIR4002_5_zero_branch" for row in theorem), "conditional zero theorem present")
    add("VAL4002_08_bound_theorem", any(row["theorem_id"] == "HIR4002_6_bound_if_not_zero" for row in theorem), "bound theorem present")
    add("VAL4002_09_audit_verdict", any(row["audit_id"] == "HRA4002_6_zero_proof_verdict" for row in audit), "zero-proof audit verdict present")
    add("VAL4002_10_reference_guard_audit", any(row["audit_id"] == "HRA4002_5_no_fitted_reference" for row in audit), "reference guard audit present")
    add("VAL4002_11_master_bound", any(row["bound_id"] == "HRB4002_0_master" for row in bounds), "master bound present")
    add("VAL4002_12_ref_units_bounds", any(row["bound_id"] == "HRB4002_4_I_ref_Delta_ref" for row in bounds) and any(row["bound_id"] == "HRB4002_7_C_units" for row in bounds), "reference/units bounds present")
    zero = next(row for row in results if row["case_id"] == "CASE4002_0_integrable_fixed_reference_zero")
    parent = next(row for row in results if row["case_id"] == "CASE4002_1_parent_current_missing")
    ref = next(row for row in results if row["case_id"] == "CASE4002_2_reference_drift")
    frame = next(row for row in results if row["case_id"] == "CASE4002_3_tau_frame_units_leak")
    fitted = next(row for row in results if row["case_id"] == "CASE4002_4_fitted_reference_refused")
    orbital = next(row for row in results if row["case_id"] == "CASE4002_5_orbital_denominator_refused")
    missing = next(row for row in results if row["case_id"] == "CASE4002_6_missing_parent_rows")
    add("VAL4002_13_zero_case", float(zero["Delta_Htau_Href_4002"]) == 0.0 and str(zero["conditional_zero_theorem_applies"]).lower() == "true", "zero theorem case clean")
    add("VAL4002_14_parent_case", float(parent["epsilon_parent_current_abs"]) > 0.0, "parent current missing case produces residual")
    add("VAL4002_15_reference_case", float(ref["epsilon_reference_abs"]) > 0.0, "reference drift produces residual")
    add("VAL4002_16_frame_case", float(frame["epsilon_frame_units_abs"]) > 0.0, "frame/units leak produces residual")
    add("VAL4002_17_fitted_ref_refused", str(fitted["passes_schema"]).lower() == "true" and str(fitted["passes_reference_guard"]).lower() == "false", "fitted reference refused")
    add("VAL4002_18_orbital_denominator_refused", str(orbital["passes_schema"]).lower() == "true" and str(orbital["passes_denominator_guard"]).lower() == "false", "orbital GM denominator refused")
    add("VAL4002_19_missing_blocks", missing["Delta_Htau_Href_4002"] == "MISSING" and str(missing["passes_schema"]).lower() == "false", "missing parent rows block")
    add("VAL4002_20_claim_gate_false", all(str(row.get("allowed", "")).lower() == "false" for row in read_csv(OUTPUTS["claim_gate"])), "all claim gates false")
    add("VAL4002_21_next_target", OUTPUTS["next"].exists() and NEXT_DOC in read_text(OUTPUTS["next"]), "next target written")
    add("VAL4002_22_doc_exists", DOC_PATH.exists() and "fitted mass" in read_text(DOC_PATH) and "orbital `GM`" in read_text(DOC_PATH), "document written")
    add("VAL4002_23_spine_updated", SPINE_PATH.exists() and "## 4002 - Htau/Href Integrability Reference Lock" in read_text(SPINE_PATH), "spine updated")
    add("VAL4002_24_no_fwb_outputs", not any(str(path).startswith(str(FWB)) for path in OUTPUTS.values()), "no outputs target formalization-workbench")
    add("VAL4002_25_compile", compile_ok, "script compiles")
    add("VAL4002_26_no_pycache", not (SCRIPT_PATH.parent / "__pycache__").exists(), "script __pycache__ removed")
    add("VAL4002_27_status_exists", OUTPUTS["status"].exists(), "status file exists")
    add("VAL4002_28_results_nonclaim", all(str(row.get("valid_for_claim", "")).lower() == "false" for row in results), "all evaluator results remain nonclaim")
    add("VAL4002_29_no_nan", not any("nan" in str(row).lower() or "inf" in str(row).lower() for row in results), "no nan/inf evaluator outputs")
    add("VAL4002_30_no_orbital_guard", DOC_PATH.exists() and "not imported from orbital `GM`" in read_text(DOC_PATH), "no orbital-GM guard recorded")
    add("VAL4002_31_phase_space_language", DOC_PATH.exists() and "covariant phase-space one-form" in read_text(DOC_PATH), "phase-space derivation language recorded")
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
    print(f"4002 validation: {passed}/{total} passed")
    if passed != total:
        for row in validation:
            if not row["passed"]:
                print(f"FAIL {row['check_id']}: {row['detail']}")
        raise SystemExit(1)
    print(f"Wrote {DOC_PATH}")


if __name__ == "__main__":
    main()
