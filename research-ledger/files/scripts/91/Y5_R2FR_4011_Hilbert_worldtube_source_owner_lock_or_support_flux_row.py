from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "4011"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "4011-Y5-R2FR-Hilbert-worldtube-source-owner-lock-or-support-flux-row.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_4011_SOURCE_REGISTER.csv",
    "theorem": SRC / "P8_Y5_R2FR_4011_HILBERT_WORLDTUBE_LOCK_THEOREM.csv",
    "audit": SRC / "P8_Y5_R2FR_4011_SOURCE_MEASURE_DESCENT_AUDIT.csv",
    "finite": SRC / "P8_Y5_R2FR_4011_SUPPORT_FLUX_FINITE_ROWS.csv",
    "cases": SRC / "P8_Y5_R2FR_4011_EVALUATOR_CASES.csv",
    "results": SRC / "P8_Y5_R2FR_4011_EVALUATOR_RESULTS.csv",
    "decision": SRC / "P8_Y5_R2FR_4011_DECISION_GATE.csv",
    "claim_gate": SRC / "P8_Y5_R2FR_4011_CLAIM_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_4011_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_4011_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_4011_VALIDATION.csv",
}

NEXT_DOC = "4012-Y5-R2FR-PiM-Htau-source-current-commutator-lock-or-CM-Ccurl-row.md"
NEXT_SCRIPT = "scripts/Y5_R2FR_4012_PiM_Htau_source_current_commutator_lock_or_CM_Ccurl_row.py"


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


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
        ("SRC4011_00_handoff", SRC / "P8_Y5_R2FR_4010_NEXT_TARGET.csv", "NEXT4010_0", "4010 handoff"),
        ("SRC4011_01_worldtube_theorem", SRC / "P8_Y5_R2FR_4010_BOUNDARY_WORLDTUBE_NOHAIR_THEOREM.csv", "BWT4010_3_worldtube_support", "4010 worldtube zero condition"),
        ("SRC4011_02_boundary_full_gate", SRC / "P8_Y5_R2FR_4010_BOUNDARY_WORLDTUBE_NOHAIR_THEOREM.csv", "BWT4010_5_full_zero_condition", "4010 full boundary gate"),
        ("SRC4011_03_worldtube_audit", SRC / "P8_Y5_R2FR_4010_BOUNDARY_WORLDTUBE_AUDIT.csv", "BWA4010_2_worldtube_support", "4010 worldtube unsigned audit"),
        ("SRC4011_04_projection_audit", SRC / "P8_Y5_R2FR_4010_BOUNDARY_WORLDTUBE_AUDIT.csv", "BWA4010_3_projector_local_projection", "4010 projector/local projection audit"),
        ("SRC4011_05_boundary_row", SRC / "P8_Y5_R2FR_4010_JR_BOUNDARY_FINITE_ROWS.csv", "JRBND4010_3_worldtube", "4010 finite worldtube row"),
        ("SRC4011_06_decision_next", SRC / "P8_Y5_R2FR_4010_DECISION_GATE.csv", "DEC4010_3_next", "4010 next decision"),
        ("SRC4011_07_support_selector", SRC / "P8_Y5_MATTER_DESCENT_GATE_2611_WORLDTUBE_SOURCE_OWNER_AUDIT.csv", "WTA2611_0_support_selector", "support selector audit"),
        ("SRC4011_08_same_charge", SRC / "P8_Y5_MATTER_DESCENT_GATE_2611_WORLDTUBE_SOURCE_OWNER_AUDIT.csv", "WTA2611_1_same_charge", "same charge audit"),
        ("SRC4011_09_no_domain_mask", SRC / "P8_Y5_MATTER_DESCENT_GATE_2611_WORLDTUBE_SOURCE_OWNER_AUDIT.csv", "WTA2611_2_no_readout_domain_mask", "no readout domain mask audit"),
        ("SRC4011_10_worldtube_verdict", SRC / "P8_Y5_MATTER_DESCENT_GATE_2611_WORLDTUBE_SOURCE_OWNER_AUDIT.csv", "WTA2611_3_matter_worldtube_verdict", "2611 worldtube verdict"),
        ("SRC4011_11_qsource_master", SRC / "P8_EM_quotient_source_coordinate_descent_certificate.csv", "QSC3516_0_master_theorem", "quotient source descent master theorem"),
        ("SRC4011_12_sigma_descent", SRC / "P8_EM_quotient_source_coordinate_descent_certificate.csv", "QSC3516_2_sigma_descent", "sigma/worldtube q-basic certificate"),
        ("SRC4011_13_R_W", SRC / "P8_EM_ellJ_source_current_owner_residual_law.csv", "EJR3513_6_R_W", "worldtube support drift row"),
        ("SRC4011_14_R_PiM", SRC / "P8_EM_ellJ_source_current_owner_residual_law.csv", "EJR3513_3_R_PiM", "Pi_M commutator row"),
        ("SRC4011_15_R_Htau", SRC / "P8_EM_ellJ_source_current_owner_residual_law.csv", "EJR3513_4_R_Htau", "H_tau curl row"),
        ("SRC4011_16_R_ref", SRC / "P8_EM_ellJ_source_current_owner_residual_law.csv", "EJR3513_5_R_ref", "reference source row"),
        ("SRC4011_17_R_frame", SRC / "P8_EM_ellJ_source_current_owner_residual_law.csv", "EJR3513_7_R_frame", "frame/source row"),
        ("SRC4011_18_PHCR_total", SRC / "P8_EM_PiM_Htau_commutator_residual_law.csv", "PHCR3514_0_total", "Pi_M/H_tau total residual"),
        ("SRC4011_19_C_shape", SRC / "P8_EM_PiM_Htau_commutator_residual_law.csv", "PHCR3514_2_C_shape", "shape leakage component"),
        ("SRC4011_20_C_domain", SRC / "P8_EM_PiM_Htau_commutator_residual_law.csv", "PHCR3514_4_C_domain", "domain/worldtube component"),
        ("SRC4011_21_C_ref", SRC / "P8_EM_PiM_Htau_commutator_residual_law.csv", "PHCR3514_5_C_ref", "reference component"),
        ("SRC4011_22_C_frame", SRC / "P8_EM_PiM_Htau_commutator_residual_law.csv", "PHCR3514_6_C_frame", "frame component"),
        ("SRC4011_23_contract_parent", SRC / "P8_Y5_HILBERT_WORLDTUBE_PARENT_ACTION_CONTRACT.csv", "PAC537_2_parent_fixed_worldtube", "parent fixed worldtube contract"),
        ("SRC4011_24_contract_PiM", SRC / "P8_Y5_HILBERT_WORLDTUBE_PARENT_ACTION_CONTRACT.csv", "PAC537_4_action_owned_PiM_projector", "action-owned Pi_M contract"),
        ("SRC4011_25_contract_charge", SRC / "P8_Y5_HILBERT_WORLDTUBE_PARENT_ACTION_CONTRACT.csv", "PAC537_5_Hilbert_topological_charge_equality", "Hilbert/topological charge equality contract"),
        ("SRC4011_26_glue_parent_worldtube", SRC / "P8_Y5_HILBERT_WORLDTUBE_GLUE_THEOREM_ATTEMPT.csv", "HWT536_0_parent_worldtube_fixed", "parent worldtube fixed clause"),
        ("SRC4011_27_glue_measure", SRC / "P8_Y5_HILBERT_WORLDTUBE_GLUE_THEOREM_ATTEMPT.csv", "HWT536_1_observed_Hilbert_measure_owned", "observed Hilbert measure clause"),
        ("SRC4011_28_glue_charge_map", SRC / "P8_Y5_HILBERT_WORLDTUBE_GLUE_THEOREM_ATTEMPT.csv", "HWT536_3_Hilbert_to_PiM_charge_map", "Hilbert to Pi_M map clause"),
        ("SRC4011_29_parent_glue_source", SRC / "P8_PARENT_WORLDTUBE_GLUE_THEOREM_CLAUSES.csv", "W504_4_worldtube_source_measure_glue", "parent worldtube source measure glue"),
        ("SRC4011_30_parent_obstruction", SRC / "P8_PARENT_WORLDTUBE_GLUE_OBSTRUCTIONS.csv", "O504_0_wrong_conserved_object", "wrong conserved object obstruction"),
        ("SRC4011_31_measure_theorem", SRC / "P8_WORLDTUBE_SOURCE_MEASURE_THEOREM.csv", "T510_1_worldtube_source_measure", "source measure theorem"),
        ("SRC4011_32_measure_clause", SRC / "P8_WORLDTUBE_SOURCE_MEASURE_CLAUSES.csv", "WG510_7_dressed_source_definition", "dressed source definition clause"),
        ("SRC4011_33_3596_definition", SRC / "P8_Y5_R2FR_3596_WORLDTUBE_HILBERT_SOURCE_MEASURE_LOCK.csv", "WSL3596_1_dressed_definition", "3596 dressed definition"),
        ("SRC4011_34_3596_EM_once", SRC / "P8_Y5_R2FR_3596_WORLDTUBE_HILBERT_SOURCE_MEASURE_LOCK.csv", "WSL3596_4_EM_once", "EM/Poynting once-only guard"),
        ("SRC4011_35_3596_conditional", SRC / "P8_Y5_R2FR_3596_WORLDTUBE_HILBERT_SOURCE_MEASURE_LOCK.csv", "WSL3596_6_conditional_lock_theorem", "3596 conditional lock theorem"),
        ("SRC4011_36_3891_descent", SRC / "P8_Y5_R2FR_3891_WORLDTUBE_SUPPORT_DESCENT_ATTEMPT.csv", "WSD3891_1_descent", "3891 support descent candidate"),
        ("SRC4011_37_3984_transfer", SRC / "P8_Y5_R2FR_3984_WORLDTUBE_OWNERSHIP_THEOREM_ATTEMPT.csv", "CWO3984_1_MTS_transfer_contract", "3984 source ownership transfer contract"),
        ("SRC4011_38_3984_failure", SRC / "P8_Y5_R2FR_3984_WORLDTUBE_OWNERSHIP_THEOREM_ATTEMPT.csv", "CWO3984_2_zero_proof_audit", "3984 unsigned subfactors audit"),
    ]


def source_register_rows(timestamp: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path, needle, role in source_specs():
        text = read_text(path)
        rows.append(
            {
                "source_id": source_id,
                "role": role,
                "path": str(path),
                "needle": needle,
                "exists": path.exists(),
                "needle_found": needle in text,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def theorem_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "HWT4011_0_source_support_definition",
            "claim_piece": "Hilbert-owned worldtube support definition",
            "mathematical_form": "W_H[tau] := closure(supp J_H[tau]); M_H[W] := int_W rho_H[e_obs,tau] dV_H; sigma^a := I^a[W_H,e_obs,tau]/M_H",
            "derived_result": "worldtube support is a parent-current object, not an orbital/readout mask, if it is defined before Pi_M/orbital fitting",
            "status": "DEFINITION_PACKET_CONDITIONAL",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "HWT4011_1_support_descent_lemma",
            "claim_piece": "support variation zero",
            "mathematical_form": "If J_H[tau]=q^*Jbar_H[taubar], tau=q^*taubar, e_obs=q^*ebar_obs and supp J_H is compact regular, then D_v W_H=0 for v in ker(Dq), up to support-jump/corner terms",
            "derived_result": "the local support drift term R_W is exactly zero for q-basic Hilbert current support on the same reduced branch",
            "status": "EXACT_CONDITIONAL_LEMMA_WITH_REGULARITY_GUARD",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "HWT4011_2_source_measure_descent",
            "claim_piece": "dressed source measure q-basic",
            "mathematical_form": "M_H_ref := H_tau[S_outer]-H_ref and M_H[W_H]=int_{W_H}rho_H dV_H descend only when H_tau,H_ref,tau,e_obs and W_H are all same-branch q-basic",
            "derived_result": "support lock alone does not prove measured gravitational mass; it only removes the domain/support selector from the source problem",
            "status": "CONDITIONAL_DESCENT_NOT_FULL_CHARGE_GLUE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "HWT4011_3_shape_coordinate_lock",
            "claim_piece": "shape/source coordinates do not leak into mass projector",
            "mathematical_form": "sigma^a(Phi)=sigmabar^a(q(Phi)) implies partial_M A_X^a=0 on the reduced source branch, so C_shape=0",
            "derived_result": "shape leakage dies if shape coordinates are functionals of the same Hilbert support rather than independent fitted source knobs",
            "status": "EXACT_IF_SOURCE_COORDINATES_Q_BASIC",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "HWT4011_4_linked_surface_domain_lock",
            "claim_piece": "domain/Hodge/linked surfaces fixed before readout",
            "mathematical_form": "S_outer,S_ref,Hodge,Pi_M are chosen by the parent current/support branch; then D_X(W_source,Sigma,Hodge,linked surfaces)=0 and C_domain=0",
            "derived_result": "domain residual is not allowed to be chosen after seeing orbital/R10 data; it is either a parent-owned linked-surface rule or a finite support-flux row",
            "status": "CONDITIONAL_DOMAIN_LOCK_UNSIGNED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "HWT4011_5_support_flux_envelope",
            "claim_piece": "finite fallback if support lock fails",
            "mathematical_form": "epsilon_support_4011 <= |R_W|+|C_shape|+|C_domain|+|C_ref|+|C_frame|+|epsilon_support_jump|+|epsilon_EM_once|+|epsilon_boundary_flux|",
            "derived_result": "open support/current terms are converted into a finite residual vector with no cancellation credit and no claim promotion",
            "status": "FINITE_SUPPORT_FLUX_VECTOR_DERIVED_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "HWT4011_6_full_lock_condition",
            "claim_piece": "worldtube support contribution to J_R_boundary vanishes",
            "mathematical_form": "R_W=C_shape=C_domain=0 if J_H/tau/e_obs descend through q, support is compact regular, sigma^a is q-basic, linked surfaces are parent-owned, no readout mask enters, and EM/Poynting/binding is counted once",
            "derived_result": "delta_R W_source can be zeroed as a theorem on a strict parent branch, but same-charge Pi_M/H_tau glue remains the next bottleneck",
            "status": "EXACT_CONDITIONAL_ZERO_NOT_LOCAL_GR_CLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def audit_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "audit_id": "SDA4011_0_parent_Hilbert_current",
            "clause": "J_H[tau] is derived from the parent variation with the observed coframe before readout",
            "current_status": "CONDITIONAL_PACKET_EXISTS_NOT_FINAL_PARENT_ADOPTED",
            "risk_if_open": "support lock becomes a naming convention rather than a parent current theorem",
            "next_action": "adopt the 4008/4009/4010 same-branch source constructor or retain R_W",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "SDA4011_1_tau_coframe_same_branch",
            "clause": "tau and e_obs are the same objects in source support, Hamiltonian charge and local readout",
            "current_status": "FRAME_LOCK_CONDITIONAL",
            "risk_if_open": "R_frame absorbs apparent source stability",
            "next_action": "bind tau/e_obs to the reduced branch before source and orbital comparison",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "SDA4011_2_compact_regular_support",
            "clause": "supp J_H is compact, regular and has no source birth/death or corner jump under the allowed vertical direction",
            "current_status": "REGULARITY_GUARD_NOT_PARENT_PROVEN",
            "risk_if_open": "support-jump terms survive even when J_H is q-basic",
            "next_action": "state compact-support branch conditions and keep epsilon_support_jump for discontinuous cases",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "SDA4011_3_no_readout_domain_mask",
            "clause": "W_source and linked surfaces are selected by the current/support, not by post-fit domain cuts",
            "current_status": "GUARDRAIL_INSTALLED_NOT_THEOREM",
            "risk_if_open": "C_domain can fake local source agreement",
            "next_action": "make linked-surface rule parent-owned or carry C_domain",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "SDA4011_4_same_charge_PiM_Htau",
            "clause": "Pi_M J_H equals the exterior Hamiltonian/topological mass charge with zero-flux exact terms",
            "current_status": "NOT_DERIVED_KEY_BLOCKER",
            "risk_if_open": "worldtube support can be locked while measured GM still belongs to a different conserved object",
            "next_action": "derive Pi_M/H_tau commutator and curl lock in 4012",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "SDA4011_5_shape_coordinates",
            "clause": "sigma^a are q-basic functionals of W_H,e_obs,tau rather than independent source-sector knobs",
            "current_status": "CONDITIONAL_ON_SUPPORT_LOCK",
            "risk_if_open": "C_shape/source-profile leakage enters R10, WEP and PPN source profile tests",
            "next_action": "prove source coordinate descent after support lock or keep C_shape",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "SDA4011_6_EM_Poynting_once",
            "clause": "EM, Poynting flux and binding energy enter J_H_total exactly once",
            "current_status": "OPEN_CRITICAL_GUARD",
            "risk_if_open": "field energy is double counted, omitted, or moved into an empirical coupling",
            "next_action": "treat J_H_total=J_matter+J_EM+J_Poynting+J_binding+exact improvements as a required parent input",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "SDA4011_7_boundary_flux_silence",
            "clause": "boundary/reference/improvement terms carry zero exterior source flux",
            "current_status": "4010_BOUNDARY_GATE_REMAINS_UNSIGNED",
            "risk_if_open": "support lock is spoiled by boundary/reference source leakage",
            "next_action": "keep epsilon_boundary_flux until 4010 boundary nohair is parent-adopted",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def finite_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "SFLUX4011_0_master",
            "coefficient": "epsilon_support_4011",
            "formula": "|R_W|+|C_shape|+|C_domain|+|C_ref|+|C_frame|+|epsilon_support_jump|+|epsilon_EM_once|+|epsilon_boundary_flux|",
            "value": "MISSING_NUMERIC_SOURCE_BOUND",
            "units": "dimensionless_fractional_source_drift",
            "source_status": "FINITE_VECTOR_NONCLAIM",
            "observable_links": "R10; Newton source; PPN near-source profile; clocks; orbital systems",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "SFLUX4011_1_R_W",
            "coefficient": "R_W",
            "formula": "D_X ln int_{W_source} rho_H dV_H - D_X ln int_{closure(supp J_H[tau])} rho_H dV_H",
            "value": "ZERO_IF_W_SOURCE_EQUALS_PARENT_HILBERT_SUPPORT_ELSE_MISSING_BOUND",
            "units": "dimensionless_fractional_support_drift",
            "source_status": "WORLDTUBE_DESCENT_NOT_PARENT_SIGNED",
            "observable_links": "Newton source; R10 source support; WEP/source composition",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "SFLUX4011_2_C_shape",
            "coefficient": "C_shape",
            "formula": "-(partial_M A_X^a) partial_a(H_tau-H_ref)/(Pi_M H_tau)",
            "value": "ZERO_IF_SIGMA_A_Q_BASIC_ELSE_MISSING_SHAPE_CONNECTION_BOUND",
            "units": "dimensionless_shape_leakage",
            "source_status": "SOURCE_SHAPE_CONNECTION_UNSIGNED",
            "observable_links": "R10 source profile; WEP; PPN source profile",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "SFLUX4011_3_C_domain",
            "coefficient": "C_domain",
            "formula": "normalized D_X(W_source,Sigma,Hodge,linked surfaces)",
            "value": "ZERO_IF_LINKED_SURFACES_PARENT_OWNED_ELSE_MISSING_DOMAIN_BOUND",
            "units": "dimensionless_domain_drift",
            "source_status": "DOMAIN_SUPPORT_NOT_PARENT_SIGNED",
            "observable_links": "R10; Newton source; PPN near-source profile",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "SFLUX4011_4_same_charge",
            "coefficient": "epsilon_same_charge",
            "formula": "|Pi_M J_H - J_M_top - dB_zero|/(|Pi_M J_H|+floor)",
            "value": "MISSING_PIM_HTAU_CHARGE_GLUE",
            "units": "dimensionless_charge_mismatch",
            "source_status": "NOT_DERIVED_KEY_BLOCKER",
            "observable_links": "Newton GM; PPN gamma/beta; orbital mass; R10 normalization",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "SFLUX4011_5_reference_surface",
            "coefficient": "C_ref_plus_linked_surface_flux",
            "formula": "|C_ref| + |D_X(S_outer,S_ref,H_ref)|",
            "value": "MISSING_SOURCE_BLIND_REFERENCE_AND_LINKED_SURFACE_RULE",
            "units": "dimensionless_reference_flux",
            "source_status": "REFERENCE_SELECTOR_UNSIGNED",
            "observable_links": "Newton source; clocks; orbital systems",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "SFLUX4011_6_frame",
            "coefficient": "C_frame",
            "formula": "D_X ln(tau,e_obs,Sigma,readout frame mismatch)",
            "value": "MISSING_SAME_FRAME_LOCK",
            "units": "dimensionless_frame_drift",
            "source_status": "PARALLEL_RFRAME_FACTOR",
            "observable_links": "clocks; PPN preferred-frame; orbital timing",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "SFLUX4011_7_EM_once",
            "coefficient": "epsilon_EM_once",
            "formula": "|J_H_total-(J_matter+J_EM+J_Poynting+J_binding+dB_zero)|/(|J_H_total|+floor)",
            "value": "MISSING_PARENT_EM_POYNTING_BINDING_ONCE_ONLY_ACCOUNTING",
            "units": "dimensionless_energy_accounting_drift",
            "source_status": "OPEN_CRITICAL_GUARD",
            "observable_links": "EM; charge/mass source; local energy conservation; clocks",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "SFLUX4011_8_support_jump",
            "coefficient": "epsilon_support_jump",
            "formula": "corner/birth/death contribution from non-regular variation of supp J_H[tau]",
            "value": "ZERO_ONLY_ON_COMPACT_REGULAR_SUPPORT_BRANCH",
            "units": "dimensionless_distributional_support_term",
            "source_status": "REGULARITY_BRANCH_CONDITION",
            "observable_links": "near-source tests; material transitions; R10 source geometry",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "SFLUX4011_9_arena_projection",
            "coefficient": "support_flux_arena_projection",
            "formula": "map surviving epsilon_support_4011 components into R10, PPN, clock and orbital kernels",
            "value": "MISSING_ARENA_PROJECTION_IF_ANY_COMPONENT_LIVE",
            "units": "arena_dependent",
            "source_status": "PROJECTION_REQUIRED_FOR_NUMERIC_CLAIM",
            "observable_links": "R10; PPN; clocks; orbital systems",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def case_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "case_id": "CASE4011_0_full_lock_signed",
            "parent_Hilbert_current": True,
            "tau_coframe_same_branch": True,
            "compact_regular_support": True,
            "no_readout_domain_mask": True,
            "same_charge_PiM_Htau": True,
            "shape_q_basic": True,
            "EM_once": True,
            "boundary_flux_silent": True,
            "numeric_pack": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE4011_1_support_selector_open",
            "parent_Hilbert_current": False,
            "tau_coframe_same_branch": True,
            "compact_regular_support": True,
            "no_readout_domain_mask": True,
            "same_charge_PiM_Htau": True,
            "shape_q_basic": True,
            "EM_once": True,
            "boundary_flux_silent": True,
            "numeric_pack": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE4011_2_domain_mask_open",
            "parent_Hilbert_current": True,
            "tau_coframe_same_branch": True,
            "compact_regular_support": True,
            "no_readout_domain_mask": False,
            "same_charge_PiM_Htau": True,
            "shape_q_basic": True,
            "EM_once": True,
            "boundary_flux_silent": True,
            "numeric_pack": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE4011_3_shape_open",
            "parent_Hilbert_current": True,
            "tau_coframe_same_branch": True,
            "compact_regular_support": True,
            "no_readout_domain_mask": True,
            "same_charge_PiM_Htau": True,
            "shape_q_basic": False,
            "EM_once": True,
            "boundary_flux_silent": True,
            "numeric_pack": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE4011_4_same_charge_open",
            "parent_Hilbert_current": True,
            "tau_coframe_same_branch": True,
            "compact_regular_support": True,
            "no_readout_domain_mask": True,
            "same_charge_PiM_Htau": False,
            "shape_q_basic": True,
            "EM_once": True,
            "boundary_flux_silent": True,
            "numeric_pack": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE4011_5_EM_once_open",
            "parent_Hilbert_current": True,
            "tau_coframe_same_branch": True,
            "compact_regular_support": True,
            "no_readout_domain_mask": True,
            "same_charge_PiM_Htau": True,
            "shape_q_basic": True,
            "EM_once": False,
            "boundary_flux_silent": True,
            "numeric_pack": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE4011_6_support_jump_open",
            "parent_Hilbert_current": True,
            "tau_coframe_same_branch": True,
            "compact_regular_support": False,
            "no_readout_domain_mask": True,
            "same_charge_PiM_Htau": True,
            "shape_q_basic": True,
            "EM_once": True,
            "boundary_flux_silent": True,
            "numeric_pack": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE4011_7_boundary_flux_open",
            "parent_Hilbert_current": True,
            "tau_coframe_same_branch": True,
            "compact_regular_support": True,
            "no_readout_domain_mask": True,
            "same_charge_PiM_Htau": True,
            "shape_q_basic": True,
            "EM_once": True,
            "boundary_flux_silent": False,
            "numeric_pack": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE4011_8_numeric_pack",
            "parent_Hilbert_current": False,
            "tau_coframe_same_branch": False,
            "compact_regular_support": False,
            "no_readout_domain_mask": False,
            "same_charge_PiM_Htau": False,
            "shape_q_basic": False,
            "EM_once": False,
            "boundary_flux_silent": False,
            "numeric_pack": True,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def result_for_case(row: dict[str, Any], timestamp: str) -> dict[str, Any]:
    if bool(row["numeric_pack"]):
        return {
            "case_id": row["case_id"],
            "support_status": "FINITE_SUPPORT_FLUX_PACK_NONCLAIM",
            "worldtube_result": "EPSILON_SUPPORT_4011_VECTOR_REQUIRED",
            "charge_result": "NO_LOCAL_GR_PROMOTION",
            "next_action": "fill numeric/source-backed support, shape, domain, frame, EM-once and boundary-flux rows",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }

    blockers: list[str] = []
    if not bool(row["parent_Hilbert_current"]):
        blockers.append("R_W")
    if not bool(row["tau_coframe_same_branch"]):
        blockers.append("C_frame")
    if not bool(row["compact_regular_support"]):
        blockers.append("epsilon_support_jump")
    if not bool(row["no_readout_domain_mask"]):
        blockers.append("C_domain")
    if not bool(row["shape_q_basic"]):
        blockers.append("C_shape")
    if not bool(row["EM_once"]):
        blockers.append("epsilon_EM_once")
    if not bool(row["boundary_flux_silent"]):
        blockers.append("epsilon_boundary_flux")
    if not bool(row["same_charge_PiM_Htau"]):
        blockers.append("epsilon_same_charge")

    support_blockers = {"R_W", "C_frame", "epsilon_support_jump", "C_domain", "C_shape", "epsilon_EM_once", "epsilon_boundary_flux"}
    support_open = [item for item in blockers if item in support_blockers]
    charge_open = [item for item in blockers if item == "epsilon_same_charge"]

    if not blockers:
        return {
            "case_id": row["case_id"],
            "support_status": "CONDITIONAL_HILBERT_WORLDTUBE_SUPPORT_LOCK",
            "worldtube_result": "R_W_C_shape_C_domain_ZERO_IF_SINGLE_BRANCH_SIGNED",
            "charge_result": "SAME_CHARGE_ASSUMED_IN_CASE_NOT_PROVEN_GLOBALLY",
            "next_action": "move to Pi_M/H_tau source-current commutator and charge equality proof",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }

    return {
        "case_id": row["case_id"],
        "support_status": "SUPPORT_LOCK_BLOCKED" if support_open else "SUPPORT_LOCK_CONDITIONAL_BUT_CHARGE_OPEN",
        "worldtube_result": "+".join(support_open) if support_open else "SUPPORT_COMPONENTS_CONDITIONALLY_ZERO",
        "charge_result": "+".join(charge_open) if charge_open else "CHARGE_GLUE_NOT_TESTED_BY_THIS_CASE",
        "next_action": "retain " + "+".join(blockers) + " as finite nonclaim rows",
        "valid_for_claim": False,
        "timestamp_utc": timestamp,
    }


def result_rows(cases: list[dict[str, Any]], timestamp: str) -> list[dict[str, Any]]:
    return [result_for_case(row, timestamp) for row in cases]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC4011_0_conditional_derivation",
            "decision": "Hilbert worldtube support lock is derivable as a conditional theorem",
            "reason": "if W_source is closure(supp J_H[tau]) from the same q-basic Hilbert current and support is regular, R_W and shape/domain support drift vanish",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC4011_1_no_promotion",
            "decision": "do not promote local-GR, R10, PPN, clock or orbital claim",
            "reason": "same-charge Pi_M/H_tau glue, EM/Poynting once-only accounting, boundary flux silence and final parent adoption remain unsigned",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC4011_2_finite_policy",
            "decision": "if support lock fails, retain explicit support-flux vector",
            "reason": "R_W, C_shape, C_domain, C_ref, C_frame, support jumps, EM-once and boundary-flux terms have different observable projections and cannot be cancelled by assertion",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC4011_3_next",
            "decision": "next target is Pi_M/H_tau source-current commutator and charge-equality lock",
            "reason": "4011 can kill the support selector, but measured Newton/PPN source mass still needs Pi_M J_H = exterior H_tau/topological charge with zero-flux exact terms",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "CLAIM4011_0_local_GR",
            "arena": "local_GR_Newton_PPN",
            "allowed": False,
            "reason": "support lock is conditional and same-charge Pi_M/H_tau glue is still unsigned",
            "blocking_rows": "SFLUX4011_4_same_charge;SFLUX4011_9_arena_projection",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "CLAIM4011_1_R10",
            "arena": "R10_short_range",
            "allowed": False,
            "reason": "source support/profile rows are nonclaim and not numerically projected into the R10 kernel",
            "blocking_rows": "SFLUX4011_1_R_W;SFLUX4011_2_C_shape;SFLUX4011_3_C_domain;SFLUX4011_9_arena_projection",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "CLAIM4011_2_clocks_orbital",
            "arena": "clocks_orbital",
            "allowed": False,
            "reason": "same-frame, source-blind reference and measured GM charge equality remain open",
            "blocking_rows": "SFLUX4011_4_same_charge;SFLUX4011_5_reference_surface;SFLUX4011_6_frame",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "CLAIM4011_3_EM",
            "arena": "EM_source_energy",
            "allowed": False,
            "reason": "EM/Poynting/binding must be counted once inside J_H_total before any charge/coupling conclusion",
            "blocking_rows": "SFLUX4011_7_EM_once",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "NEXT4011_0",
            "next_doc": NEXT_DOC,
            "next_script": NEXT_SCRIPT,
            "target": "derive Pi_M/H_tau source-current commutator and charge equality on the same Hilbert worldtube branch, or keep C_M/C_curl/C_ref/equal-charge rows",
            "success_condition": "Pi_M is parent-owned and fixed, H_tau is integrable, H_ref is source-blind, Pi_M J_H equals exterior Hamiltonian/topological charge up to exact zero-flux terms; otherwise all charge-glue residuals remain valid_for_claim=false",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status": "COMPLETE_NONCLAIM",
            "summary": "Hilbert worldtube support lock derived as an exact conditional theorem; support drift can vanish on the same q-basic current branch, but source-charge equality remains the next coupling bottleneck",
            "current_best_next": NEXT_DOC,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def write_doc(timestamp: str, sources: list[dict[str, Any]], results: list[dict[str, Any]]) -> None:
    found = sum(1 for row in sources if row["exists"] and row["needle_found"])
    lines = [
        "# 4011 - Hilbert Worldtube Source-Owner Lock Or Support-Flux Row",
        "",
        f"- Timestamp: `{timestamp}`",
        "- Status: `private_nonclaim_checkpoint`",
        "- Scope: `post-checkpoint-work` only; no `formalization-workbench` edits.",
        "",
        "## Result",
        "",
        "The clean theorem route is now explicit:",
        "",
        "`W_H[tau] := closure(supp J_H[tau])`.",
        "",
        "If `J_H[tau]`, `tau`, and `e_obs` descend through the same reduced branch, and the support is compact/regular, then vertical variation of the support vanishes. In that branch, `R_W=0`; if the shape coordinates are also q-basic and linked surfaces are parent-owned, then `C_shape=0` and `C_domain=0`.",
        "",
        "That is a genuine derivation route, not a plateau axiom. But it is only a support/source-domain result; it does not yet prove that the same support carries the measured Newton/PPN mass charge.",
        "",
        "## Coupling Lesson",
        "",
        "This checkpoint separates two things that were getting glued together too early:",
        "",
        "- support ownership: `W_source` must be the Hilbert-current support before readout;",
        "- charge ownership: `Pi_M J_H` must equal the exterior `H_tau`/topological mass charge up to exact zero-flux terms.",
        "",
        "In short: support ownership is not yet charge ownership.",
        "",
        "4011 can conditionally solve the first. The second is now the next bottleneck.",
        "",
        "## Finite Support-Flux Row",
        "",
        "If the theorem branch is not adopted, the retained nonclaim vector is",
        "",
        "`epsilon_support_4011 <= |R_W|+|C_shape|+|C_domain|+|C_ref|+|C_frame|+|epsilon_support_jump|+|epsilon_EM_once|+|epsilon_boundary_flux|`.",
        "",
        "No cancellation between support, shape, reference, frame, EM/Poynting or boundary terms is credited.",
        "",
        "## Evaluator Results",
        "",
    ]
    for row in results:
        lines.append(
            f"- `{row['case_id']}`: support=`{row['support_status']}`, worldtube=`{row['worldtube_result']}`, charge=`{row['charge_result']}`, next=`{row['next_action']}`"
        )
    lines.extend(
        [
            "",
            "## Verdict",
            "",
            "This moves the project forward by turning the worldtube problem into a precise theorem-plus-vector fork. The worldtube selector can be made non-arbitrary, but the theory still has to prove the coupling/charge equality.",
            "",
            "## Next Target",
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
    marker = "## 4011 - Hilbert Worldtube Source-Owner Lock"
    block = f"""

{marker}

- Timestamp: `{timestamp}`
- Result: `W_H[tau] := closure(supp J_H[tau])` gives an exact conditional support theorem: if `J_H/tau/e_obs` are same-branch q-basic and support is compact regular, then `R_W=0`.
- Shape/domain payoff: q-basic `sigma^a` and parent-owned linked surfaces give `C_shape=0` and `C_domain=0` conditionally.
- Coupling split: support ownership is not yet charge ownership; `Pi_M J_H = J_M_top + dB_zero = exterior H_tau` remains the next bottleneck.
- Finite fallback: `epsilon_support_4011 <= |R_W|+|C_shape|+|C_domain|+|C_ref|+|C_frame|+|epsilon_support_jump|+|epsilon_EM_once|+|epsilon_boundary_flux|`.
- No claim: R10/Newton/PPN/clock/orbital promotion remains blocked until same-charge, EM-once, boundary and arena projection rows close.
- Next: `{NEXT_DOC}`.
"""
    current = read_text(SPINE_PATH)
    if marker not in current:
        SPINE_PATH.write_text(current.rstrip() + block + "\n", encoding="utf-8")


def marker_in_spine() -> bool:
    return "## 4011 - Hilbert Worldtube Source-Owner Lock" in read_text(SPINE_PATH)


def build_validation_rows(
    timestamp: str,
    sources: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    audit: list[dict[str, Any]],
    finite: list[dict[str, Any]],
    results: list[dict[str, Any]],
    compile_ok: bool,
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        checks.append({"check_id": check_id, "passed": bool(passed), "detail": detail, "timestamp_utc": timestamp})

    add("VAL4011_00_sources_exist", all(bool(row["exists"]) for row in sources), "every cited source path exists")
    add("VAL4011_01_needles_found", all(bool(row["needle_found"]) for row in sources), "every cited source needle found")
    add("VAL4011_02_definition", any(row["theorem_id"] == "HWT4011_0_source_support_definition" for row in theorem), "support definition present")
    add("VAL4011_03_support_descent", any(row["theorem_id"] == "HWT4011_1_support_descent_lemma" for row in theorem), "support descent lemma present")
    add("VAL4011_04_measure_descent", any(row["theorem_id"] == "HWT4011_2_source_measure_descent" for row in theorem), "source measure descent distinction present")
    add("VAL4011_05_shape_lock", any(row["theorem_id"] == "HWT4011_3_shape_coordinate_lock" for row in theorem), "shape coordinate lock present")
    add("VAL4011_06_domain_lock", any(row["theorem_id"] == "HWT4011_4_linked_surface_domain_lock" for row in theorem), "linked-surface/domain lock present")
    add("VAL4011_07_finite_vector_theorem", any(row["theorem_id"] == "HWT4011_5_support_flux_envelope" for row in theorem), "finite support vector theorem present")
    add("VAL4011_08_full_lock_condition", any(row["theorem_id"] == "HWT4011_6_full_lock_condition" for row in theorem), "full support lock condition present")
    add("VAL4011_09_audit_parent_current", any(row["audit_id"] == "SDA4011_0_parent_Hilbert_current" for row in audit), "parent Hilbert current audit present")
    add("VAL4011_10_audit_same_charge", any(row["audit_id"] == "SDA4011_4_same_charge_PiM_Htau" for row in audit), "same-charge audit present")
    add("VAL4011_11_audit_EM_once", any(row["audit_id"] == "SDA4011_6_EM_Poynting_once" for row in audit), "EM/Poynting once-only audit present")
    add("VAL4011_12_audit_boundary", any(row["audit_id"] == "SDA4011_7_boundary_flux_silence" for row in audit), "boundary flux audit present")
    master = next(row for row in finite if row["row_id"] == "SFLUX4011_0_master")
    add("VAL4011_13_master_vector", "epsilon_EM_once" in master["formula"] and "epsilon_boundary_flux" in master["formula"], "master support vector includes EM and boundary guards")
    add("VAL4011_14_R_W_row", any(row["row_id"] == "SFLUX4011_1_R_W" for row in finite), "R_W row present")
    add("VAL4011_15_C_shape_row", any(row["row_id"] == "SFLUX4011_2_C_shape" for row in finite), "C_shape row present")
    add("VAL4011_16_C_domain_row", any(row["row_id"] == "SFLUX4011_3_C_domain" for row in finite), "C_domain row present")
    add("VAL4011_17_same_charge_row", any(row["row_id"] == "SFLUX4011_4_same_charge" for row in finite), "same-charge row present")
    add("VAL4011_18_reference_row", any(row["row_id"] == "SFLUX4011_5_reference_surface" for row in finite), "reference/surface row present")
    add("VAL4011_19_frame_row", any(row["row_id"] == "SFLUX4011_6_frame" for row in finite), "frame row present")
    add("VAL4011_20_EM_row", any(row["row_id"] == "SFLUX4011_7_EM_once" for row in finite), "EM once-only row present")
    add("VAL4011_21_support_jump_row", any(row["row_id"] == "SFLUX4011_8_support_jump" for row in finite), "support jump row present")
    add("VAL4011_22_projection_row", any(row["row_id"] == "SFLUX4011_9_arena_projection" for row in finite), "arena projection row present")
    full = next(row for row in results if row["case_id"] == "CASE4011_0_full_lock_signed")
    support_open = next(row for row in results if row["case_id"] == "CASE4011_1_support_selector_open")
    domain_open = next(row for row in results if row["case_id"] == "CASE4011_2_domain_mask_open")
    shape_open = next(row for row in results if row["case_id"] == "CASE4011_3_shape_open")
    charge_open = next(row for row in results if row["case_id"] == "CASE4011_4_same_charge_open")
    em_open = next(row for row in results if row["case_id"] == "CASE4011_5_EM_once_open")
    jump_open = next(row for row in results if row["case_id"] == "CASE4011_6_support_jump_open")
    boundary_open = next(row for row in results if row["case_id"] == "CASE4011_7_boundary_flux_open")
    numeric_case = next(row for row in results if row["case_id"] == "CASE4011_8_numeric_pack")
    add("VAL4011_23_full_case", full["worldtube_result"] == "R_W_C_shape_C_domain_ZERO_IF_SINGLE_BRANCH_SIGNED", "full signed case conditionally zeros support terms")
    add("VAL4011_24_support_open_case", support_open["worldtube_result"] == "R_W", "support selector open routes to R_W")
    add("VAL4011_25_domain_open_case", domain_open["worldtube_result"] == "C_domain", "domain mask open routes to C_domain")
    add("VAL4011_26_shape_open_case", shape_open["worldtube_result"] == "C_shape", "shape open routes to C_shape")
    add("VAL4011_27_charge_open_case", charge_open["charge_result"] == "epsilon_same_charge", "same-charge open routes to charge row")
    add("VAL4011_28_EM_open_case", em_open["worldtube_result"] == "epsilon_EM_once", "EM once-only open routes to EM row")
    add("VAL4011_29_jump_open_case", jump_open["worldtube_result"] == "epsilon_support_jump", "support jump open routes to support-jump row")
    add("VAL4011_30_boundary_open_case", boundary_open["worldtube_result"] == "epsilon_boundary_flux", "boundary flux open routes to boundary row")
    add("VAL4011_31_numeric_case", numeric_case["support_status"] == "FINITE_SUPPORT_FLUX_PACK_NONCLAIM", "numeric pack remains nonclaim")
    add("VAL4011_32_claim_gate_false", all(str(row.get("allowed", "")).lower() == "false" for row in read_csv(OUTPUTS["claim_gate"])), "all claim gates false")
    add("VAL4011_33_next_target", OUTPUTS["next"].exists() and NEXT_DOC in read_text(OUTPUTS["next"]), "next target written")
    add("VAL4011_34_doc_exists", DOC_PATH.exists() and "Coupling Lesson" in read_text(DOC_PATH), "document written")
    add("VAL4011_35_spine_updated", SPINE_PATH.exists() and marker_in_spine(), "spine updated")
    add("VAL4011_36_no_fwb_outputs", not any(str(path).startswith(str(FWB)) for path in OUTPUTS.values()), "no outputs target formalization-workbench")
    add("VAL4011_37_compile", compile_ok, "script compiles")
    add("VAL4011_38_no_pycache", not (SCRIPT_PATH.parent / "__pycache__").exists(), "script __pycache__ removed")
    output_tables = [
        sources,
        theorem,
        audit,
        finite,
        results,
        read_csv(OUTPUTS["decision"]),
        read_csv(OUTPUTS["claim_gate"]),
        read_csv(OUTPUTS["next"]),
        read_csv(OUTPUTS["status"]),
    ]
    add("VAL4011_39_all_nonclaim", all(str(row.get("valid_for_claim", "")).lower() == "false" for table in output_tables for row in table), "all emitted rows remain nonclaim")
    add("VAL4011_40_no_nan", not any("nan" in str(row).lower() or "inf" in str(row).lower() for row in results), "no nan/inf evaluator outputs")
    add("VAL4011_41_private_scope", DOC_PATH.exists() and "private_nonclaim_checkpoint" in read_text(DOC_PATH), "private scope recorded")
    add("VAL4011_42_forward_target", "Pi_M" in read_text(OUTPUTS["next"]) and "H_tau" in read_text(OUTPUTS["next"]), "forward target is Pi_M/H_tau commutator lock")
    add("VAL4011_43_support_not_charge", "support ownership is not yet charge ownership" in read_text(DOC_PATH), "document separates support ownership from charge ownership")
    return checks


def main() -> None:
    timestamp = now_utc()
    sources = source_register_rows(timestamp)
    theorem = theorem_rows(timestamp)
    audit = audit_rows(timestamp)
    finite = finite_rows(timestamp)
    cases = case_rows(timestamp)
    results = result_rows(cases, timestamp)
    decisions = decision_rows(timestamp)
    claims = claim_gate_rows(timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["theorem"], theorem)
    write_csv(OUTPUTS["audit"], audit)
    write_csv(OUTPUTS["finite"], finite)
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

    validation = build_validation_rows(timestamp, sources, theorem, audit, finite, results, compile_ok)
    write_csv(OUTPUTS["validation"], validation)
    passed = sum(1 for row in validation if row["passed"])
    total = len(validation)
    print(f"4011 validation: {passed}/{total} passed")
    if passed != total:
        for row in validation:
            if not row["passed"]:
                print(f"FAIL {row['check_id']}: {row['detail']}")
        raise SystemExit(1)
    print(f"Wrote {DOC_PATH}")


if __name__ == "__main__":
    main()
