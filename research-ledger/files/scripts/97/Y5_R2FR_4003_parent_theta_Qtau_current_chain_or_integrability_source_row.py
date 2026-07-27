from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "4003"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "4003-Y5-R2FR-parent-theta-Qtau-current-chain-or-integrability-source-row.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_4003_SOURCE_REGISTER.csv",
    "theorem": SRC / "P8_Y5_R2FR_4003_PARENT_CURRENT_CHAIN_THEOREM.csv",
    "audit": SRC / "P8_Y5_R2FR_4003_CURRENT_CHAIN_AUDIT.csv",
    "bounds": SRC / "P8_Y5_R2FR_4003_INTEGRABILITY_COMPONENT_BOUND_VECTOR.csv",
    "cases": SRC / "P8_Y5_R2FR_4003_EVALUATOR_CASES.csv",
    "results": SRC / "P8_Y5_R2FR_4003_EVALUATOR_RESULTS.csv",
    "decision": SRC / "P8_Y5_R2FR_4003_DECISION_GATE.csv",
    "claim_gate": SRC / "P8_Y5_R2FR_4003_CLAIM_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_4003_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_4003_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_4003_VALIDATION.csv",
}

NEXT_DOC = "4004-Y5-R2FR-IX-extra-sector-current-extraction-or-source-backed-curl-row.md"
NEXT_SCRIPT = "scripts/Y5_R2FR_4004_IX_extra_sector_current_extraction_or_source_backed_curl_row.py"


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
        ("SRC4003_00_handoff", SRC / "P8_Y5_R2FR_4002_NEXT_TARGET.csv", "NEXT4002_0", "4002 handoff"),
        ("SRC4003_01_oneform", SRC / "P8_Y5_R2FR_4002_HTAU_HREF_THEOREM.csv", "HIR4002_0_phase_space_one_form", "Htau one-form"),
        ("SRC4003_02_curl_decomposition", SRC / "P8_Y5_R2FR_4002_HTAU_HREF_THEOREM.csv", "HIR4002_2_curl_decomposition", "curl split"),
        ("SRC4003_03_ix_bound", SRC / "P8_Y5_R2FR_4002_CURL_REFERENCE_BOUND_VECTOR.csv", "HRB4002_1_I_X", "I_X handoff"),
        ("SRC4003_04_theta_components", SRC / "P8_Y5_PARENT_QLOC_1733_THETA_QTAU_COMPONENT_ROWS.csv", "TQC1733_6_total_Qtau", "Theta/Qtau component rows"),
        ("SRC4003_05_current_owner", SRC / "P8_Y5_PARENT_QLOC_1733_THETA_QTAU_CURRENT_OWNER_AUDIT.csv", "COA1733_2_Noether_current", "Noether current owner audit"),
        ("SRC4003_06_descent_lemma", SRC / "P8_Y5_PARENT_QLOC_1733_DESCENT_CURRENT_LEMMA.csv", "DCL1733_0_contract", "descent-current lemma"),
        ("SRC4003_07_leak_rows", SRC / "P8_Y5_PARENT_QLOC_1734_THETA_QTAU_LEAK_ROWS.csv", "TLR1734_4_total_theta_qtau_leak", "projectability leak rows"),
        ("SRC4003_08_parent_L_gate", SRC / "P8_Y5_PARENT_QLOC_1785_PARENT_LAGRANGIAN_THETA_VX_GATE.csv", "PLT1785_0_L_parent", "parent Lagrangian gate"),
        ("SRC4003_09_presymplectic", SRC / "P8_Y5_PARENT_QLOC_2237_PRESYMPLECTIC_NULL_CHAIN.csv", "NULL2237_0_parent_L_theta", "presymplectic null chain"),
        ("SRC4003_10_theta_omega", SRC / "P8_Y5_PARENT_QLOC_2238_THETA_OMEGA_FILL.csv", "TO2238_0_theta_R", "theta/omega auxiliary fill"),
        ("SRC4003_11_fixed_reference", SRC / "P8_Y5_PARENT_QLOC_2339_THETA_QTAU_FIXED_REFERENCE_AUDIT.csv", "TQF2339_2_theta_Qtau", "fixed-reference theta/Qtau audit"),
        ("SRC4003_12_worldtube", SRC / "P8_WORLDTUBE_SOURCE_MEASURE_THEOREM.csv", "T510_2_MTS_transfer_condition", "worldtube transfer condition"),
        ("SRC4003_13_hamiltonian_contract", SRC / "P8_mass_current_Hamiltonian_boundary_charge_CONTRACT.csv", "HC2_differentiable_integrable_Hxi", "Hamiltonian boundary charge contract"),
        ("SRC4003_14_em_poynting", SRC / "P8_EM_PiM_Htau_commutator_residual_law.csv", "PHCR3514_3_C_curl", "EM/Poynting Htau residual law"),
        ("SRC4003_15_gauss_contract", SRC / "P8_Hamiltonian_charge_Poisson_Gauss_calibration_CONTRACT.csv", "PG1_charge_equals_projected_Hilbert_source", "Poisson/Gauss calibration guard"),
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
            "theorem_id": "PCC4003_0_parent_variation",
            "claim_piece": "single parent variational owner",
            "mathematical_form": "delta L_parent = E_A delta Phi^A + d Theta_total(Phi;delta Phi)",
            "derived_result": "Theta_total is not an independent insert; it must be the boundary term produced by varying one parent action containing EH, matter/source, EM, projector, boundary/reference and retained MTS sectors.",
            "status": "EXACT_CURRENT_CHAIN_CONTRACT_NOT_PARENT_SIGNED",
            "source_path": str(SRC / "P8_Y5_PARENT_QLOC_1733_THETA_QTAU_CURRENT_OWNER_AUDIT.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "PCC4003_1_noether_current",
            "claim_piece": "observed-time Noether current",
            "mathematical_form": "J_tau := Theta_total(Phi;L_tau Phi) - i_tau L_parent - mu_tau; dJ_tau = -E_A L_tau Phi^A; J_tau = dQ_tau^MTS + C_tau on the constrained branch.",
            "derived_result": "The Hamiltonian charge exists only after the same tau acts on all parent fields and every nonzero bulk constraint, quasi-symmetry, or boundary term is zeroed or retained.",
            "status": "DERIVED_COVARIANT_PHASE_SPACE_CHAIN",
            "source_path": str(SRC / "P8_Y5_PARENT_QLOC_1733_DESCENT_CURRENT_LEMMA.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "PCC4003_2_charge_decomposition",
            "claim_piece": "full MTS charge split",
            "mathematical_form": "Q_tau^MTS = Q_tau^EH + Q_tau^X + Q_tau^PiM + Q_tau^boundary + Q_tau^matter/EM + Q_tau^Dq + exact/proper terms.",
            "derived_result": "EH charge can be a reference piece, but it cannot be promoted to the MTS charge unless X, projector, boundary, matter/EM and quotient pieces are proved zero/exact/proper or retained as explicit residuals.",
            "status": "EXACT_DECOMPOSITION_GUARD",
            "source_path": str(SRC / "P8_Y5_PARENT_QLOC_1733_THETA_QTAU_COMPONENT_ROWS.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "PCC4003_3_descent_zero_lemma",
            "claim_piece": "legal reduction to EH/reduced charge",
            "mathematical_form": "If L_parent=q^*L_red+L_vert_alg+dB, tau is q-projectable, Dq[v]=0, Theta_vert is zero/exact/proper, B is fixed before readout, and matter/source descends through q, then Q_tau^parent=q^*Q_tau^red+i_tau B+proper corner terms.",
            "derived_result": "This is the non-smuggled route to local GR: vertical/excess sectors do not disappear by assumption; they disappear only by quotient descent plus boundary and matter silence.",
            "status": "CONDITIONAL_ZERO_LEMMA_NOT_CLAIM",
            "source_path": str(SRC / "P8_Y5_PARENT_QLOC_1733_DESCENT_CURRENT_LEMMA.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "PCC4003_4_integrability_feedthrough",
            "claim_piece": "current chain feeds H_tau integrability",
            "mathematical_form": "alpha_tau[delta Phi]=int_S(delta Q_tau^MTS-i_tau Theta_total)-delta H_ref; d_field alpha_tau=0 iff all retained current-chain curl components vanish or are included as source-backed rows.",
            "derived_result": "The 4002 H_tau/H_ref lock is now connected to a concrete current-chain checklist: missing theta/Qtau pieces become I_X, I_projector, I_boundary, I_matter_EM, I_Dq and C_tau_bulk.",
            "status": "DERIVED_FEEDTHROUGH_TO_4002_BOUND",
            "source_path": str(SRC / "P8_Y5_R2FR_4002_HTAU_HREF_THEOREM.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "PCC4003_5_bound_if_unsigned",
            "claim_piece": "current-chain residual vector",
            "mathematical_form": "Delta_current_chain_4003=|C_tau_bulk|+|I_X|+|I_projector|+|I_boundary|+|I_matter_EM|+|I_Dq|+|Theta_leak|+|Qtau_leak|+|Omega_null_gap|+|sector_gap|+|EH_borrowing_guard|.",
            "derived_result": "If the parent-current theorem is not closed, the work does not loop; it produces a finite menu of components to derive or source one at a time.",
            "status": "EXECUTABLE_BOUND_VECTOR",
            "source_path": str(SRC / "P8_Y5_PARENT_QLOC_1798_DELTAH_CURL_COMPONENT_PACK.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "PCC4003_6_no_EH_borrowing_guard",
            "claim_piece": "anti-circularity guard",
            "mathematical_form": "Q_tau^EH valid and Q_tau^X,Q_tau^PiM,Q_tau^boundary,Q_tau^matter/EM,Q_tau^Dq unowned imply Q_tau^MTS not promoted.",
            "derived_result": "Borrowing the GR/EH Hamiltonian charge is allowed as a baseline comparator, not as a proof of MTS local-GR recovery.",
            "status": "GUARD_ACTIVE",
            "source_path": str(SRC / "P8_mass_current_Hamiltonian_boundary_charge_CONTRACT.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "PCC4003_7_first_row_rule",
            "claim_piece": "nonclaim component-row fallback",
            "mathematical_form": "If PCC4003_0..6 do not close, write source-backed rows for I_X/I_projector/I_boundary/I_matter_EM/I_Dq with units and valid_for_claim=false before any local arena score.",
            "derived_result": "The next move is derivation-first but not all-or-nothing: each obstruction can become a tested coefficient row without claiming local GR.",
            "status": "SOURCE_ROW_FALLBACK_READY",
            "source_path": str(SRC / "P8_Y5_R2FR_4002_CURL_REFERENCE_BOUND_VECTOR.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def audit_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "audit_id": "PCA4003_0_L_parent",
            "clause": "one parent action",
            "required_signature": "L_parent contains EH, matter/source, EM, projector, boundary/reference and retained MTS sectors before readout.",
            "current_evidence": "COA1733_0 and PLT1785_0 mark the total parent variation as missing.",
            "current_status": "MISSING_SINGLE_PARENT_VARIATION",
            "feeds_component": "C_tau_bulk;sector_gap",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "PCA4003_1_Theta_total",
            "clause": "Theta_total extraction",
            "required_signature": "Theta_total=Theta_EH+Theta_matter/EM+Theta_X+Theta_projector+deltaB_ref+Theta_boundary from the same delta L_parent.",
            "current_evidence": "COA1733_1 says the split is formal and not extracted.",
            "current_status": "THETA_TOTAL_NOT_PARENT_EXTRACTED",
            "feeds_component": "Theta_leak",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "PCA4003_2_Qtau_total",
            "clause": "Q_tau^MTS extraction",
            "required_signature": "J_tau=Theta_total(L_tau Phi)-i_tau L_parent-mu_tau=dQ_tau^MTS+C_tau with all retained C_tau pieces accounted for.",
            "current_evidence": "COA1733_2 and TQC1733_6 keep Q_tau^MTS total blocked.",
            "current_status": "QTAU_TOTAL_NOT_PROMOTED",
            "feeds_component": "Qtau_leak;C_tau_bulk",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "PCA4003_3_X_extra_current",
            "clause": "extra motion/time/memory/range current",
            "required_signature": "delta L_X=E_X delta X+dTheta_X and J_tau^X=dQ_tau^X+C_tau^X, or a parent-signed algebraic auxiliary theorem gives Theta_X=Q_tau^X=0/proper.",
            "current_evidence": "TQC1733_1_X_extra and DCC1798_1_I_X mark the sector current missing.",
            "current_status": "I_X_OPEN",
            "feeds_component": "I_X",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "PCA4003_4_projector_current",
            "clause": "projector/source-current contribution",
            "required_signature": "delta(Pi_M J_H)=Pi_M delta J_H+(delta Pi_M)J_H is varied before readout and its Hamiltonian current contribution is zero/bounded.",
            "current_evidence": "TQC1733_2_projector_PiM and HRB4002_2 keep projector ownership linked to 4001.",
            "current_status": "I_PROJECTOR_OPEN",
            "feeds_component": "I_projector",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "PCA4003_5_boundary_reference",
            "clause": "boundary/reference current",
            "required_signature": "B_ref, corner terms, exact improvements and no-hair class are fixed by the parent variational problem before source/readout.",
            "current_evidence": "TQC1733_3_boundary_reference and TQF2339_3_fixed_reference mark the reference owner missing.",
            "current_status": "I_BOUNDARY_OPEN",
            "feeds_component": "I_boundary",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "PCA4003_6_matter_EM_coupling",
            "clause": "matter, EM and Poynting placement",
            "required_signature": "bound/static EM stress is included once in J_H/Theta_total; net radiative/background Poynting or hidden material-marker energy is retained as a source component.",
            "current_evidence": "PHCR3514 and COA1733_5 keep matter/coupling descent nonclaim.",
            "current_status": "I_MATTER_EM_OPEN",
            "feeds_component": "I_matter_EM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "PCA4003_7_qDq_tau_projectability",
            "clause": "quotient/current projectability",
            "required_signature": "Dq(L_tau Phi)=L_tau_red q(Phi), Dq[v]=0, and source/clock/orbit/boundary readout is blind to vertical representatives.",
            "current_evidence": "DCL1733_1/DCL1733_3 and TLR1734 rows keep q/Dq/tau leakage live.",
            "current_status": "I_DQ_OPEN",
            "feeds_component": "I_Dq",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "PCA4003_8_presymplectic_null_gap",
            "clause": "vertical null directions",
            "required_signature": "ker(Dq)=ker(Omega_parent) after gauge/boundary quotient, with no hidden boundary charge.",
            "current_evidence": "NULL2237_0/1 keep parent theta/Omega missing; TO2238 gives only conditional auxiliary zeros.",
            "current_status": "OMEGA_NULL_GAP_OPEN",
            "feeds_component": "Omega_null_gap",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "PCA4003_9_verdict",
            "clause": "parent current-chain verdict",
            "required_signature": "PCA4003_0 through PCA4003_8 pass together.",
            "current_evidence": "The exact chain is written, but current corpus still lacks the parent-owned sector extraction.",
            "current_status": "CURRENT_CHAIN_NOT_PARENT_SIGNED_BUT_EXECUTABLE",
            "feeds_component": "Delta_current_chain_4003",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def bound_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "bound_id": "PCB4003_0_master",
            "component": "Delta_current_chain_4003",
            "formula": "|C_tau_bulk|+|I_X|+|I_projector|+|I_boundary|+|I_matter_EM|+|I_Dq|+|Theta_leak|+|Qtau_leak|+|Omega_null_gap|+|sector_gap|+|EH_borrowing_guard|",
            "numeric_value": "MISSING_PARENT_SIGNED_COMPONENTS",
            "units": "dimensionless_after_M_H_ref_or_declared_component_norms",
            "status": "EXECUTABLE_VECTOR_READY_NONCLAIM",
            "source_anchor": "PCC4003_5_bound_if_unsigned",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "PCB4003_1_C_tau_bulk",
            "component": "C_tau_bulk",
            "formula": "|E_A L_tau Phi^A + retained bulk constraints + quasi_symmetry_defect|/M_H_ref",
            "numeric_value": "MISSING_PARENT_EULER_WARD_LEDGER",
            "units": "dimensionless",
            "status": "SOURCE_BACKED_FORMULA_NOT_NUMERIC",
            "source_anchor": "HC3_constraints_and_boundary_conditions;PCC4003_1_noether_current",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "PCB4003_2_I_X",
            "component": "I_X",
            "formula": "|d_field alpha_tau^X|/M_H_ref with alpha_tau^X=int_S(delta Q_tau^X-i_tau Theta_X)",
            "numeric_value": "MISSING_L_X_THETA_X_QTAU_X_OR_ZERO_THEOREM",
            "units": "dimensionless",
            "status": "NEXT_DERIVATION_TARGET",
            "source_anchor": "TQC1733_1_X_extra;DCC1798_1_I_X;PLT1785_1_theta_Y",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "PCB4003_3_I_projector",
            "component": "I_projector",
            "formula": "|d_field alpha_tau^projector|/M_H_ref",
            "numeric_value": "ZERO_IF_4001_CHAINMAP_AND_PROJECTOR_STRESS_CLOSE_ELSE_BOUND_REQUIRED",
            "units": "dimensionless",
            "status": "LINKS_TO_4001_PROJECTOR_GATE",
            "source_anchor": "TQC1733_2_projector_PiM;HRB4002_2_I_projector",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "PCB4003_4_I_boundary",
            "component": "I_boundary",
            "formula": "|d_field alpha_tau^boundary + curl(delta B_ref) + corner/improvement drift|/M_H_ref",
            "numeric_value": "MISSING_BOUNDARY_REFERENCE_OWNER",
            "units": "dimensionless",
            "status": "OPEN_BOUNDARY_REFERENCE",
            "source_anchor": "TQC1733_3_boundary_reference;TQF2339_3_fixed_reference",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "PCB4003_5_I_matter_EM",
            "component": "I_matter_EM",
            "formula": "|matter_source_descent_leak + EM_static_double_count_guard + net_radiative_or_background_Poynting_flux|/M_H_ref",
            "numeric_value": "MISSING_MATTER_EM_COUPLING_DESCENT_OR_FLUX_BOUND",
            "units": "dimensionless",
            "status": "OPEN_COUPLING_AND_POYNTING_GATE",
            "source_anchor": "COA1733_5_matter_coupling_descent;PHCR3514_3_C_curl",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "PCB4003_6_I_Dq",
            "component": "I_Dq",
            "formula": "|Dq_current_leak + source_readout_Dq_leak + coupling_marker_leak|/M_H_ref",
            "numeric_value": "MISSING_Q_DQ_TAU_PROJECTABILITY_OR_BOUND",
            "units": "dimensionless",
            "status": "OPEN_QUOTIENT_CURRENT_LEAK",
            "source_anchor": "TQC1733_5_Dq_leak;TLR1734_4_total_theta_qtau_leak",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "PCB4003_7_Theta_Qtau_leak",
            "component": "Theta_leak+Qtau_leak",
            "formula": "|unowned Theta_total pieces|/M_H_ref + |unowned Q_tau pieces|/M_H_ref",
            "numeric_value": "MISSING_THETA_TOTAL_QTAU_TOTAL_COMPONENT_CERTIFICATES",
            "units": "dimensionless",
            "status": "OPEN_TOTAL_CURRENT_OWNER",
            "source_anchor": "COA1733_1_Theta_total;COA1733_2_Noether_current;TQC1733_6_total_Qtau",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "PCB4003_8_Omega_null_gap",
            "component": "Omega_null_gap",
            "formula": "|failure of ker(Dq)=ker(Omega_parent)| plus boundary Hamiltonian charge of vertical directions",
            "numeric_value": "MISSING_PARENT_OMEGA_AND_BOUNDARY_ZERO_THEOREM",
            "units": "dimensionless_or_declared_presymplectic_norm",
            "status": "OPEN_PRESYMPLECTIC_NULL_GAP",
            "source_anchor": "NULL2237_0_parent_L_theta;NULL2237_4_no_boundary_charge;TO2238_0_theta_R",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "PCB4003_9_EH_borrowing_guard",
            "component": "EH_borrowing_guard",
            "formula": "1 if Q_tau^EH is used as Q_tau^MTS while any retained non-EH component is unowned; else 0",
            "numeric_value": "GUARD_ACTIVE",
            "units": "boolean_guard",
            "status": "REFUSES_GR_BASELINE_AS_MTS_PROOF",
            "source_anchor": "TQC1733_0_EH;HC0_same_frame_EH_exterior;T510_2_MTS_transfer_condition",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def case_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "case_id": "CASE4003_0_full_parent_current_zero",
            "description": "all parent-current clauses close and retained components are zero/exact/proper",
            "has_parent_L": True,
            "has_theta_total": True,
            "has_Qtau_total": True,
            "has_X_current": True,
            "has_projector_current": True,
            "has_boundary_reference": True,
            "has_matter_EM_descent": True,
            "has_qDq_descent": True,
            "has_omega_null": True,
            "uses_EH_reference_as_MTS": False,
            "numeric_component_rows": True,
            "schema_complete": True,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE4003_1_EH_only_reference",
            "description": "EH charge exists but non-EH MTS sectors are not extracted",
            "has_parent_L": False,
            "has_theta_total": False,
            "has_Qtau_total": False,
            "has_X_current": False,
            "has_projector_current": False,
            "has_boundary_reference": False,
            "has_matter_EM_descent": False,
            "has_qDq_descent": False,
            "has_omega_null": False,
            "uses_EH_reference_as_MTS": True,
            "numeric_component_rows": False,
            "schema_complete": True,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE4003_2_X_extra_missing",
            "description": "parent L/theta/Qtau exist formally but X-sector current is absent",
            "has_parent_L": True,
            "has_theta_total": True,
            "has_Qtau_total": True,
            "has_X_current": False,
            "has_projector_current": True,
            "has_boundary_reference": True,
            "has_matter_EM_descent": True,
            "has_qDq_descent": True,
            "has_omega_null": True,
            "uses_EH_reference_as_MTS": False,
            "numeric_component_rows": False,
            "schema_complete": True,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE4003_3_projector_boundary_missing",
            "description": "extra sector is controlled but projector and boundary/reference current pieces remain open",
            "has_parent_L": True,
            "has_theta_total": True,
            "has_Qtau_total": True,
            "has_X_current": True,
            "has_projector_current": False,
            "has_boundary_reference": False,
            "has_matter_EM_descent": True,
            "has_qDq_descent": True,
            "has_omega_null": True,
            "uses_EH_reference_as_MTS": False,
            "numeric_component_rows": False,
            "schema_complete": True,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE4003_4_Dq_matter_marker_missing",
            "description": "charge chain exists but q/Dq projectability and matter/EM/coupling descent are missing",
            "has_parent_L": True,
            "has_theta_total": True,
            "has_Qtau_total": True,
            "has_X_current": True,
            "has_projector_current": True,
            "has_boundary_reference": True,
            "has_matter_EM_descent": False,
            "has_qDq_descent": False,
            "has_omega_null": True,
            "uses_EH_reference_as_MTS": False,
            "numeric_component_rows": False,
            "schema_complete": True,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE4003_5_numeric_nonclaim_component_row",
            "description": "one or more residual components have numeric/source-backed rows but total current chain is not closed",
            "has_parent_L": False,
            "has_theta_total": False,
            "has_Qtau_total": False,
            "has_X_current": False,
            "has_projector_current": False,
            "has_boundary_reference": False,
            "has_matter_EM_descent": False,
            "has_qDq_descent": False,
            "has_omega_null": False,
            "uses_EH_reference_as_MTS": False,
            "numeric_component_rows": True,
            "schema_complete": True,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE4003_6_missing_parent_rows",
            "description": "schema/source paths missing for parent-current rows",
            "has_parent_L": False,
            "has_theta_total": False,
            "has_Qtau_total": False,
            "has_X_current": False,
            "has_projector_current": False,
            "has_boundary_reference": False,
            "has_matter_EM_descent": False,
            "has_qDq_descent": False,
            "has_omega_null": False,
            "uses_EH_reference_as_MTS": False,
            "numeric_component_rows": False,
            "schema_complete": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def result_rows(cases: list[dict[str, Any]], timestamp: str) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    required = [
        "has_parent_L",
        "has_theta_total",
        "has_Qtau_total",
        "has_X_current",
        "has_projector_current",
        "has_boundary_reference",
        "has_matter_EM_descent",
        "has_qDq_descent",
        "has_omega_null",
    ]
    for case in cases:
        schema_complete = bool(case["schema_complete"])
        all_clauses = schema_complete and all(bool(case[name]) for name in required)
        eh_borrowing = bool(case["uses_EH_reference_as_MTS"])
        if not schema_complete:
            status = "BLOCKED_MISSING_PARENT_ROWS"
            delta = "MISSING"
            zero = False
            next_action = "repair source/schema rows before scoring"
        elif eh_borrowing:
            status = "EH_BORROWING_REFUSED"
            delta = "GUARD_ACTIVE_PLUS_SYMBOLIC_COMPONENTS"
            zero = False
            next_action = "do not promote EH baseline; derive or retain non-EH components"
        elif all_clauses:
            status = "CONDITIONAL_ZERO_THEOREM_AVAILABLE"
            delta = 0.0
            zero = True
            next_action = "then feed 4002 H_tau/H_ref and local-GR gates"
        elif bool(case["numeric_component_rows"]):
            status = "NONCLAIM_SOURCE_ROW_ACCEPTED"
            delta = "PARTIAL_NUMERIC_COMPONENTS_TOTAL_CHAIN_OPEN"
            zero = False
            next_action = "keep row nonclaim and continue component extraction"
        elif not bool(case["has_X_current"]):
            status = "I_X_OPEN"
            delta = "SYMBOLIC_I_X_BOUND_REQUIRED"
            zero = False
            next_action = "derive Theta_X/Q_tau_X or prove algebraic auxiliary zero"
        elif not bool(case["has_projector_current"]) or not bool(case["has_boundary_reference"]):
            status = "PROJECTOR_BOUNDARY_OPEN"
            delta = "SYMBOLIC_PROJECTOR_BOUNDARY_BOUND_REQUIRED"
            zero = False
            next_action = "connect 4001 projector and fixed boundary/reference selector"
        elif not bool(case["has_matter_EM_descent"]) or not bool(case["has_qDq_descent"]):
            status = "MATTER_DQ_COUPLING_OPEN"
            delta = "SYMBOLIC_MATTER_DQ_BOUND_REQUIRED"
            zero = False
            next_action = "prove q/Dq source descent or write coupling/Poynting residual row"
        else:
            status = "CURRENT_CHAIN_OPEN"
            delta = "SYMBOLIC_BOUND_REQUIRED"
            zero = False
            next_action = "identify first open component and attack it"
        results.append(
            {
                "case_id": case["case_id"],
                "input_status": status,
                "conditional_current_zero_applies": zero,
                "Delta_current_chain_4003": delta,
                "passes_schema": schema_complete,
                "passes_EH_borrowing_guard": not eh_borrowing,
                "claim_allowed": False,
                "next_action": next_action,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return results


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DG4003_0_parent_current",
            "question": "Does the corpus now parent-sign L_parent -> Theta_total -> J_tau -> Q_tau^MTS for all retained sectors?",
            "answer": "False",
            "reason": "The exact current-chain contract is derived, but X/projector/boundary/matter-Dq components are not extracted from one parent variation.",
            "action": "no local-GR or Newton claim from H_tau yet",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DG4003_1_not_a_loop",
            "question": "Is this just another missing-list checkpoint?",
            "answer": "False",
            "reason": "The fork now gives a mathematical current-chain zero theorem and a component vector that can be attacked row-by-row.",
            "action": "advance to the first component derivation rather than re-auditing all components",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DG4003_2_next_component",
            "question": "Which component should be attacked first?",
            "answer": "I_X",
            "reason": "If the extra MTS sector is algebraic/auxiliary, Theta_X and Q_tau_X may vanish exactly; if derivative-bearing, it gives the first real source/current coefficient.",
            "action": f"write {NEXT_DOC}",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DG4003_3_poynting_note",
            "question": "Where do EM waves/Poynting ideas enter?",
            "answer": "I_matter_EM",
            "reason": "Bound/static EM stress belongs inside the source current once; net radiative or background Poynting flux is a residual component, not a hidden cancellation.",
            "action": "keep Poynting as an explicit flux/coupling row if the parent current does not silence it",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    gates = [
        ("CG4003_0_Htau_integrability", "H_tau closed phase-space one-form from parent Theta/Qtau", False, "parent current chain still unsigned"),
        ("CG4003_1_local_GR", "local GR recovery from MTS parent charge", False, "Q_tau^MTS is not promoted"),
        ("CG4003_2_Newton", "Newtonian source mass from Hamiltonian charge", False, "anti-circular source/GM bridge remains open"),
        ("CG4003_3_PPN_R10_clocks_orbits", "local arena passes", False, "local arena rows need current-chain components"),
        ("CG4003_4_GitHub_public_claim", "public-facing claim safety", False, "private checkpoint only"),
    ]
    return [
        {
            "gate_id": gate_id,
            "claim": claim,
            "allowed": allowed,
            "reason": reason,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for gate_id, claim, allowed, reason in gates
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "NEXT4003_0",
            "next_doc": NEXT_DOC,
            "next_script": NEXT_SCRIPT,
            "target": "derive I_X by varying the extra MTS sector current, or create a source-backed nonclaim I_X row with units and parent-action blocker",
            "success_condition": "Theta_X=Q_tau_X=0/proper from algebraic auxiliary grammar, or explicit Theta_X/Q_tau_X/C_tau_X from derivative sector, or numeric/source-backed nonclaim I_X bound row",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status": "COMPLETE_NONCLAIM",
            "summary": "parent Theta_total/Q_tau current-chain theorem and executable residual vector written; full local-GR/Htau claim remains blocked until sector components are derived or bounded",
            "current_best_next": NEXT_DOC,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def write_doc(timestamp: str, sources: list[dict[str, Any]], results: list[dict[str, Any]]) -> None:
    found = sum(1 for row in sources if row["exists"] and row["needle_found"])
    lines = [
        "# 4003 - Parent Theta/Qtau Current Chain Or Integrability Source Row",
        "",
        f"- Timestamp: `{timestamp}`",
        "- Status: `private_nonclaim_checkpoint`",
        "- Scope: `post-checkpoint-work` only; no `formalization-workbench` edits.",
        "",
        "## Result",
        "",
        "This checkpoint makes the exact parent-current fork explicit.",
        "",
        "The route is real:",
        "",
        "`delta L_parent = E_A delta Phi^A + d Theta_total(Phi;delta Phi)`",
        "",
        "`J_tau = Theta_total(Phi;L_tau Phi) - i_tau L_parent - mu_tau`",
        "",
        "`J_tau = d Q_tau^MTS + C_tau` on the constrained branch.",
        "",
        "Then the 4002 Hamiltonian one-form is",
        "",
        "`alpha_tau[delta Phi]=int_S(delta Q_tau^MTS-i_tau Theta_total)-delta H_ref`.",
        "",
        "So the proof path is not vague: derive the parent current, prove the retained pieces zero/exact/proper, and only then let `H_tau` become a source charge.",
        "",
        "## Non-Smuggled Local GR Route",
        "",
        "The clean descent lemma is:",
        "",
        "`L_parent = q^*L_red + L_vert_alg + dB`",
        "",
        "with projectable `tau`, explicit `Dq`, vertical directions killed by quotient/symplectic silence, fixed boundary/reference `B`, and matter/source descent through `q`.",
        "",
        "If those clauses hold, then",
        "",
        "`Q_tau^parent = q^*Q_tau^red + i_tau B + proper corner terms`,",
        "",
        "and the EH/GR exterior charge can be inherited rather than borrowed.",
        "",
        "That is the bridge we want: GR comes out as the reduced current branch, not as a pasted-on baseline.",
        "",
        "## What Blocks The Claim",
        "",
        "`Q_tau^EH` exists as a reference comparator, but `Q_tau^MTS` is not promoted while these pieces remain unowned:",
        "",
        "- `Q_tau^X`, `Theta_X`, `C_tau^X` for the extra motion/time/memory/range sector.",
        "- projector/source-current variation, especially `(delta Pi_M)J_H`.",
        "- boundary/reference/corner improvements and fixed `H_ref`.",
        "- matter, EM, coupling, and Poynting placement in the same current.",
        "- quotient/current projectability through `q` and `Dq`.",
        "- parent presymplectic null equivalence `ker(Dq)=ker(Omega_parent)`.",
        "",
        "## Bound If Closure Fails",
        "",
        "`Delta_current_chain_4003=|C_tau_bulk|+|I_X|+|I_projector|+|I_boundary|+|I_matter_EM|+|I_Dq|+|Theta_leak|+|Qtau_leak|+|Omega_null_gap|+|sector_gap|+|EH_borrowing_guard|`.",
        "",
        "This is the useful part: if a proof clause does not close, it becomes a named component to derive, bound, or source. No more fog bank.",
        "",
        "## Evaluator Results",
        "",
    ]
    for row in results:
        lines.append(
            f"- `{row['case_id']}`: `{row['input_status']}`, zero={row['conditional_current_zero_applies']}, delta=`{row['Delta_current_chain_4003']}`, claim={row['claim_allowed']}, next=`{row['next_action']}`"
        )
    lines.extend(
        [
            "",
            "## Verdict",
            "",
            "We moved from “Theta/Qtau missing” to an exact contract and a ranked attack vector. The best next leap is `I_X`: derive whether the extra MTS sector is algebraic/auxiliary so `Theta_X=Q_tau_X=0/proper`, or expose the first real extra-sector Hamiltonian current.",
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
    marker = "## 4003 - Parent Theta/Qtau Current Chain"
    block = f"""

{marker}

- Timestamp: `{timestamp}`
- Result: the exact chain is now fixed as `delta L_parent=E_A delta Phi^A+dTheta_total`, `J_tau=Theta_total(L_tau Phi)-i_tau L_parent-mu_tau`, and `J_tau=dQ_tau^MTS+C_tau`.
- Descent route: if `L_parent=q^*L_red+L_vert_alg+dB`, `tau` is q-projectable, vertical sectors are zero/exact/proper, boundary/reference is fixed, and matter/source descends through `q`, then the EH/reduced Hamiltonian charge can be inherited rather than borrowed.
- Bound route: `Delta_current_chain_4003=|C_tau_bulk|+|I_X|+|I_projector|+|I_boundary|+|I_matter_EM|+|I_Dq|+|Theta_leak|+|Qtau_leak|+|Omega_null_gap|+|sector_gap|+|EH_borrowing_guard|`.
- Current verdict: parent current chain is derived as a contract but not parent-signed; local-GR/Newton/PPN/R10 claims remain blocked.
- Next: `{NEXT_DOC}`.
"""
    current = read_text(SPINE_PATH)
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

    add("VAL4003_00_sources_exist", all(bool(row["exists"]) for row in sources), "every cited source path exists")
    add("VAL4003_01_needles_found", all(bool(row["needle_found"]) for row in sources), "every cited source needle found")
    add("VAL4003_02_parent_variation", any(row["theorem_id"] == "PCC4003_0_parent_variation" for row in theorem), "parent variation row present")
    add("VAL4003_03_current_chain", any(row["theorem_id"] == "PCC4003_1_noether_current" for row in theorem), "Noether current chain row present")
    add("VAL4003_04_charge_decomposition", any(row["theorem_id"] == "PCC4003_2_charge_decomposition" for row in theorem), "charge decomposition row present")
    add("VAL4003_05_descent_zero", any(row["theorem_id"] == "PCC4003_3_descent_zero_lemma" for row in theorem), "descent zero lemma row present")
    add("VAL4003_06_feedthrough", any(row["theorem_id"] == "PCC4003_4_integrability_feedthrough" for row in theorem), "4002 feedthrough row present")
    add("VAL4003_07_bound_vector", any(row["theorem_id"] == "PCC4003_5_bound_if_unsigned" for row in theorem), "bound vector theorem row present")
    add("VAL4003_08_no_eh_borrowing", any(row["theorem_id"] == "PCC4003_6_no_EH_borrowing_guard" for row in theorem), "EH borrowing guard present")
    add("VAL4003_09_first_row_rule", any(row["theorem_id"] == "PCC4003_7_first_row_rule" for row in theorem), "component-row fallback present")
    add("VAL4003_10_audit_verdict", any(row["audit_id"] == "PCA4003_9_verdict" for row in audit), "audit verdict present")
    add("VAL4003_11_ix_audit", any(row["audit_id"] == "PCA4003_3_X_extra_current" for row in audit), "I_X audit present")
    add("VAL4003_12_master_bound", any(row["bound_id"] == "PCB4003_0_master" for row in bounds), "master bound present")
    add("VAL4003_13_ix_next_bound", any(row["bound_id"] == "PCB4003_2_I_X" and row["status"] == "NEXT_DERIVATION_TARGET" for row in bounds), "I_X marked next derivation target")
    add("VAL4003_14_poynting_bound", any(row["bound_id"] == "PCB4003_5_I_matter_EM" for row in bounds), "matter/EM/Poynting component present")
    add("VAL4003_15_eh_guard_bound", any(row["bound_id"] == "PCB4003_9_EH_borrowing_guard" for row in bounds), "EH borrowing guard bound present")
    zero = next(row for row in results if row["case_id"] == "CASE4003_0_full_parent_current_zero")
    eh = next(row for row in results if row["case_id"] == "CASE4003_1_EH_only_reference")
    ix = next(row for row in results if row["case_id"] == "CASE4003_2_X_extra_missing")
    partial = next(row for row in results if row["case_id"] == "CASE4003_5_numeric_nonclaim_component_row")
    missing = next(row for row in results if row["case_id"] == "CASE4003_6_missing_parent_rows")
    add("VAL4003_16_zero_case", float(zero["Delta_current_chain_4003"]) == 0.0 and str(zero["conditional_current_zero_applies"]).lower() == "true", "conditional zero case clean")
    add("VAL4003_17_eh_refused", eh["input_status"] == "EH_BORROWING_REFUSED" and str(eh["passes_EH_borrowing_guard"]).lower() == "false", "EH-only promotion refused")
    add("VAL4003_18_ix_open", ix["input_status"] == "I_X_OPEN", "I_X missing case routed correctly")
    add("VAL4003_19_partial_nonclaim", partial["input_status"] == "NONCLAIM_SOURCE_ROW_ACCEPTED" and str(partial["claim_allowed"]).lower() == "false", "partial numeric rows remain nonclaim")
    add("VAL4003_20_missing_blocks", missing["Delta_current_chain_4003"] == "MISSING" and str(missing["passes_schema"]).lower() == "false", "missing parent rows block")
    add("VAL4003_21_claim_gate_false", all(str(row.get("allowed", "")).lower() == "false" for row in read_csv(OUTPUTS["claim_gate"])), "all claim gates false")
    add("VAL4003_22_next_target", OUTPUTS["next"].exists() and NEXT_DOC in read_text(OUTPUTS["next"]), "next target written")
    add("VAL4003_23_doc_exists", DOC_PATH.exists() and "No more fog bank" in read_text(DOC_PATH), "document written")
    add("VAL4003_24_spine_updated", SPINE_PATH.exists() and "## 4003 - Parent Theta/Qtau Current Chain" in read_text(SPINE_PATH), "spine updated")
    add("VAL4003_25_no_fwb_outputs", not any(str(path).startswith(str(FWB)) for path in OUTPUTS.values()), "no outputs target formalization-workbench")
    add("VAL4003_26_compile", compile_ok, "script compiles")
    add("VAL4003_27_no_pycache", not (SCRIPT_PATH.parent / "__pycache__").exists(), "script __pycache__ removed")
    add("VAL4003_28_status_exists", OUTPUTS["status"].exists(), "status file exists")
    output_tables = [sources, theorem, audit, bounds, results, read_csv(OUTPUTS["decision"]), read_csv(OUTPUTS["claim_gate"]), read_csv(OUTPUTS["next"]), read_csv(OUTPUTS["status"])]
    add("VAL4003_29_all_nonclaim", all(str(row.get("valid_for_claim", "")).lower() == "false" for table in output_tables for row in table), "all emitted rows remain nonclaim")
    add("VAL4003_30_no_nan", not any("nan" in str(row).lower() or "inf" in str(row).lower() for row in results), "no nan/inf evaluator outputs")
    add("VAL4003_31_scope_private", DOC_PATH.exists() and "private_nonclaim_checkpoint" in read_text(DOC_PATH), "private scope recorded")
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
    print(f"4003 validation: {passed}/{total} passed")
    if passed != total:
        for row in validation:
            if not row["passed"]:
                print(f"FAIL {row['check_id']}: {row['detail']}")
        raise SystemExit(1)
    print(f"Wrote {DOC_PATH}")


if __name__ == "__main__":
    main()
