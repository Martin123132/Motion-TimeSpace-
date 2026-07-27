from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
DOC = ROOT / "3552-Y5-R2FR-Htau-qbasic-charge-extraction-or-DXHtau-bound-pack.md"
CANONICAL_STATUS = OUT / "P8_Y5_Htau_qbasic_charge_extraction_status.csv"


SOURCES: dict[str, dict[str, Any]] = {
    "script_3552": {"path": Path(__file__).resolve(), "role": "3552 generator"},
    "doc_3551": {
        "path": ROOT / "3551-Y5-R2FR-MHref-qbasic-descent-or-Htau-Href-bound-pack.md",
        "role": "M_H_ref descent handoff",
    },
    "next_3551": {
        "path": OUT / "P8_Y5_R2FR_3551_NEXT_TARGET.csv",
        "role": "3551 selected H_tau target",
    },
    "mhref_leakage_3551": {
        "path": OUT / "P8_Y5_R2FR_3551_MHREF_LEAKAGE_BOUND_PACK.csv",
        "role": "D_X H_tau leakage handoff",
    },
    "mhref_theorem_3551": {
        "path": OUT / "P8_Y5_R2FR_3551_MHREF_DESCENT_THEOREM.csv",
        "role": "M_H_ref q-basic theorem",
    },
    "mhref_clauses_3551": {
        "path": OUT / "P8_Y5_R2FR_3551_HTAU_HREF_DESCENT_CLAUSE_AUDIT.csv",
        "role": "H_tau/H_ref descent clauses",
    },
    "charge_schema_1008": {
        "path": OUT / "P8_Y5_R10_1008_CHARGE_DECOMPOSITION_SCHEMA.csv",
        "role": "parent theta/Q_tau extraction schema",
    },
    "charge_doc_1008": {
        "path": ROOT / "1008-Y5-R10-parent-theta-Qtau-extraction-or-charge-decomposition-runner.md",
        "role": "parent theta/Q_tau extraction checkpoint",
    },
    "qtau_ledger_993": {
        "path": OUT / "P8_Y5_R10_993_QTAU_DECOMPOSITION_LEDGER.csv",
        "role": "Q_tau piece ledger",
    },
    "owner_audit_771": {
        "path": OUT / "P8_Y5_R10_771_THETA_QTAU_CURRENT_OWNER_AUDIT.csv",
        "role": "theta/Q_tau current owner audit",
    },
    "noether_extraction_771": {
        "path": OUT / "P8_Y5_R10_771_NOETHER_EXTRACTION_TEST.csv",
        "role": "Noether extraction test",
    },
    "noether_variation_824": {
        "path": OUT / "P8_Y5_R10_824_NOETHER_VARIATION_AUDIT.csv",
        "role": "Noether/Ward identity warning",
    },
    "gauge_noether_917": {
        "path": OUT / "P8_Y5_R10_917_GAUGE_NOETHER_IDENTITY_ATTEMPT.csv",
        "role": "gauge/source identity attempt",
    },
    "yloc_noether": {
        "path": OUT / "P8_YLOC_SOURCE_CURRENT_NOETHER_AUDIT.csv",
        "role": "Noether alone is not a local-zero theorem",
    },
    "parent_noether_chain": {
        "path": OUT / "P8_PARENT_NOETHER_CLOSURE_DERIVATION_CHAIN.csv",
        "role": "parent Noether charge-form chain",
    },
    "momentum_map_583": {
        "path": OUT / "P8_Y5_R10_583_NOETHER_MOMENTUM_MAP_CONTRACT.csv",
        "role": "momentum-map contract",
    },
    "tau_contract_685": {
        "path": OUT / "P8_Y5_R10_685_TAU_GENERATOR_CONTRACT.csv",
        "role": "tau generator contract",
    },
    "tau_audit_684": {
        "path": OUT / "P8_Y5_R10_684_TAU_GENERATOR_AUDIT.csv",
        "role": "same-tau audit",
    },
    "htau_curl_2667": {
        "path": OUT / "P8_Y5_R10_HTAU_INTEGRABILITY_CURL_2667_INTEGRABILITY_GATE.csv",
        "role": "H_tau integrability curl gate",
    },
    "hamiltonian_contract": {
        "path": OUT / "P8_mass_current_Hamiltonian_boundary_charge_CONTRACT.csv",
        "role": "Hamiltonian boundary charge contract",
    },
    "qmap_3517": {
        "path": OUT / "P8_EM_actual_q_map_vertical_basis_candidate.csv",
        "role": "candidate q/e_obs/tau branch",
    },
}


def bool_text(value: bool) -> str:
    return "True" if value else "False"


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def csv_parse_ok(path: Path) -> bool:
    try:
        read_csv_rows(path)
    except (csv.Error, OSError, UnicodeDecodeError):
        return False
    return True


def markdown_escape(value: Any) -> str:
    return str(value).replace("\n", "<br>").replace("|", "\\|")


def markdown_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(fields) + " |"
    divider = "| " + " | ".join("---" for _ in fields) + " |"
    body = [
        "| " + " | ".join(markdown_escape(row.get(field, "")) for field in fields)
        + " |"
        for row in rows
    ]
    return "\n".join([header, divider, *body])


def source_rows() -> list[dict[str, Any]]:
    return [
        {
            "source_id": source_id,
            "path": str(item["path"]),
            "exists": bool_text(item["path"].exists()),
            "role": item["role"],
            "valid_for_claim": "False",
        }
        for source_id, item in SOURCES.items()
    ]


def theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "HTD3552_0_covariant_phase_space_charge",
            "claim_piece": "H_tau definition",
            "statement": "delta H_tau = integral_S(delta Q_tau^MTS - i_tau theta_MTS) plus explicit constraint/bulk terms that must vanish or be retained.",
            "proof_step": "This is the covariant Hamiltonian charge shape; it becomes MTS-owned only when theta_MTS, Q_tau^MTS and every C_tau piece come from the parent action.",
            "condition_needed": "explicit L_parent variation, tau action on all fields, sector charge split, constraints, fixed reference and surface branch.",
            "current_status": "FORMAL_SHAPE_NOT_PARENT_OWNED",
            "source_path": str(SOURCES["charge_schema_1008"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "HTD3552_1_qbasic_charge_theorem",
            "claim_piece": "H_tau q-basicness",
            "statement": "If L_parent, tau_obs, theta_MTS, Q_tau^MTS, boundary/reference data, and the integration surface all factor through the same q/e_obs/tau branch, then H_tau=Hbar_tau(q(Phi)).",
            "proof_step": "The Hamiltonian variation is built only from q-basic objects; integrability makes its phase-space integral a q-basic scalar up to a fixed additive reference.",
            "condition_needed": "same branch, integrability curl zero, improvement ambiguity fixed, no readout-defined charge, no retained unbounded sector.",
            "current_status": "EXACT_CONDITIONAL_THEOREM_UNSIGNED",
            "source_path": str(SOURCES["qmap_3517"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "HTD3552_2_vertical_zero",
            "claim_piece": "D_X H_tau zero",
            "statement": "If H_tau=Hbar_tau(q(Phi)) and Dq(v_X)=0, then D_X H_tau=0.",
            "proof_step": "D_X H_tau=dHbar_tau(Dq(v_X))=0.",
            "condition_needed": "actual q map and vertical residual basis, not a declared invisible direction.",
            "current_status": "EXACT_COROLLARY_NOT_LIVE",
            "source_path": str(SOURCES["mhref_theorem_3551"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "HTD3552_3_integrability_gate",
            "claim_piece": "path independence",
            "statement": "H_tau is a scalar charge only if curl(delta H_tau)=0 or every curl/boundary term is retained with units.",
            "proof_step": "Without integrability, H_tau depends on the path in field space and cannot be the q-basic mass-coordinate owner.",
            "condition_needed": "parent theta/omega owner, tau/surface lock, boundary exactness, projector stress map and units.",
            "current_status": "BLOCKED_BY_2667",
            "source_path": str(SOURCES["htau_curl_2667"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "HTD3552_4_EH_import_guard",
            "claim_piece": "GR charge comparison",
            "statement": "Q_tau^EH can be used as a template only; it proves MTS H_tau only after MTS residual, boundary, projector, matter/source and extra-sector pieces are extracted, zeroed or bounded.",
            "proof_step": "A reference GR expression is not a parent MTS charge theorem.",
            "condition_needed": "MTS parent reduction guard plus retained-sector silence/bounds.",
            "current_status": "GUARD_ACTIVE",
            "source_path": str(SOURCES["charge_doc_1008"]["path"]),
            "valid_for_claim": "False",
        },
    ]


def chain_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "chain_id": "CCA3552_0_parent_action",
            "object": "L_parent",
            "required_identity": "delta L_parent = E_A delta Phi^A + d theta_MTS(delta Phi)",
            "current_evidence": "771/1008 say no single explicit current-chain L_parent varies EH, matter/source, extra, projector, boundary/reference and coupling sectors.",
            "status": "MISSING_EXPLICIT_CURRENT_CHAIN",
            "if_signed": "theta_MTS becomes evaluable rather than a placeholder",
            "source_path": str(SOURCES["owner_audit_771"]["path"]),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "chain_id": "CCA3552_1_tau_action",
            "object": "tau_obs",
            "required_identity": "L_tau Phi^A is defined for metric, matter, representative, projector, boundary and reference fields before readout",
            "current_evidence": "684/685 keep source, charge, clock, orbit and boundary tau roles split.",
            "status": "MISSING_PARENT_SELECTED_TAU_LOCK",
            "if_signed": "tau-choice ambiguity leaves D_X H_tau",
            "source_path": str(SOURCES["tau_contract_685"]["path"]),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "chain_id": "CCA3552_2_theta_MTS",
            "object": "theta_MTS",
            "required_identity": "theta_MTS = theta_EH + theta_boundary + theta_extra + theta_projector + theta_matter/source",
            "current_evidence": "1008 says theta_EH alone is not enough and total theta is not extracted.",
            "status": "MISSING_THETA_EXTRACTION",
            "if_signed": "delta H_tau can be formed from parent variables",
            "source_path": str(SOURCES["charge_schema_1008"]["path"]),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "chain_id": "CCA3552_3_Qtau_split",
            "object": "Q_tau^MTS",
            "required_identity": "J_tau=dQ_tau^MTS+C_tau with Q_EH, Q_boundary, Q_extra, Q_projector and Q_matter/source pieces extracted",
            "current_evidence": "993 has Q_EH as conditional GR reference; all other retained pieces are not extracted or not glued.",
            "status": "PIECE_SPLIT_NOT_PROMOTED",
            "if_signed": "total Q_tau becomes candidate physical Hamiltonian mass charge",
            "source_path": str(SOURCES["qtau_ledger_993"]["path"]),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "chain_id": "CCA3552_4_constraints",
            "object": "C_tau",
            "required_identity": "all retained bulk/source/projector/boundary constraints vanish by EOM or are bounded with source rows",
            "current_evidence": "Noether/Ward identities assign ownership but do not set residual currents to zero.",
            "status": "OWNERSHIP_NOT_ZERO_THEOREM",
            "if_signed": "bulk-to-boundary reduction becomes honest",
            "source_path": str(SOURCES["noether_variation_824"]["path"]),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "chain_id": "CCA3552_5_boundary_reference",
            "object": "boundary/reference",
            "required_identity": "B_ref/H_ref and improvement ambiguity are fixed before source/orbit/clock readout",
            "current_evidence": "1008 and 685 reject fitted/unfixed counterterms.",
            "status": "REFERENCE_AND_IMPROVEMENT_UNSIGNED",
            "if_signed": "H_tau cannot absorb source normalization by counterterm choice",
            "source_path": str(SOURCES["charge_doc_1008"]["path"]),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "chain_id": "CCA3552_6_integrability",
            "object": "curl(delta H_tau)",
            "required_identity": "curl(delta H_tau)=0 or every curl/boundary/projector-stress term is explicitly retained",
            "current_evidence": "2667 marks every integrability gate false.",
            "status": "HTAU_INTEGRABILITY_CURL_NOT_CLAIM_READY",
            "if_signed": "H_tau becomes path-independent on the selected branch",
            "source_path": str(SOURCES["htau_curl_2667"]["path"]),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def dxhtau_bound_rows() -> list[dict[str, Any]]:
    return [
        {
            "bound_id": "DXH3552_0_total",
            "quantity": "D_X H_tau",
            "formula": "D_X H_tau = E_tau + E_theta + E_QEH + E_Qboundary + E_Qextra + E_Qprojector + E_Qmatter + E_constraint + E_curl + E_surface + E_units",
            "non_cancellation_bound": "|D_X H_tau| <= |E_tau| + |E_theta| + |E_QEH| + |E_Qboundary| + |E_Qextra| + |E_Qprojector| + |E_Qmatter| + |E_constraint| + |E_curl| + |E_surface| + |E_units|",
            "needed_inputs": "component values or theorem-zeros for every retained sector, with common units and source paths",
            "current_value": "MISSING_DX_HTAU_COMPONENT_VECTOR",
            "units": "mass/energy derivative along X or normalized residual",
            "arena": "M_H_ref; Newton source denominator; local GR; PPN; R10",
            "source_path": str(SOURCES["mhref_leakage_3551"]["path"]),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "DXH3552_1_tau_generator",
            "quantity": "E_tau",
            "formula": "variation from tau_obs not being the same q-basic source/charge/clock/orbit/boundary generator",
            "non_cancellation_bound": "|E_tau| retained independently",
            "needed_inputs": "tau action on all parent fields; boundary-clock normalization; same-tau theorem",
            "current_value": "MISSING_PARENT_SELECTED_TAU_LOCK",
            "units": "mass/energy derivative or dimensionless normalized drift",
            "arena": "clocks; orbital GM; H_tau integrability",
            "source_path": str(SOURCES["tau_audit_684"]["path"]),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "DXH3552_2_theta",
            "quantity": "E_theta",
            "formula": "variation from missing theta_MTS sector extraction",
            "non_cancellation_bound": "|E_theta| retained independently",
            "needed_inputs": "theta_EH, theta_boundary, theta_extra, theta_projector, theta_matter/source",
            "current_value": "MISSING_THETA_MTS_SOURCE",
            "units": "symplectic-potential contribution to charge derivative",
            "arena": "H_tau charge extraction",
            "source_path": str(SOURCES["charge_schema_1008"]["path"]),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "DXH3552_3_EH_import",
            "quantity": "E_QEH",
            "formula": "EH reference charge mismatch if Q_tau^EH is treated as total MTS charge",
            "non_cancellation_bound": "|E_QEH| retained unless MTS parent reduction/silence clauses are signed",
            "needed_inputs": "MTS parent reduction guard; extra/projector/matter/source silence or bounds",
            "current_value": "MISSING_MTS_PARENT_REDUCTION_GUARD",
            "units": "charge derivative contribution",
            "arena": "GR/Newton comparison baseline",
            "source_path": str(SOURCES["charge_doc_1008"]["path"]),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "DXH3552_4_boundary",
            "quantity": "E_Qboundary",
            "formula": "boundary/reference/improvement contribution to Q_tau",
            "non_cancellation_bound": "|E_Qboundary| retained independently",
            "needed_inputs": "fixed counterterm policy; boundary flux condition; improvement ambiguity certificate",
            "current_value": "MISSING_FIXED_BEFORE_READOUT_COUNTERTERM_POLICY",
            "units": "boundary charge derivative",
            "arena": "H_ref; M_H_ref; local boundary terms",
            "source_path": str(SOURCES["qtau_ledger_993"]["path"]),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "DXH3552_5_extra_sector",
            "quantity": "E_Qextra",
            "formula": "motion/time/domain/memory/range charge leakage",
            "non_cancellation_bound": "|E_Qextra| retained independently",
            "needed_inputs": "extra-sector theta and charge extraction or no-hair/topological/silence theorem",
            "current_value": "MISSING_Q_TAU_EXTRA_SOURCE",
            "units": "extra-sector charge derivative",
            "arena": "cosmology/local split; local GR residuals",
            "source_path": str(SOURCES["qtau_ledger_993"]["path"]),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "DXH3552_6_projector",
            "quantity": "E_Qprojector",
            "formula": "projector/Pi_M variation and [d,Pi_M]J_H contribution",
            "non_cancellation_bound": "|E_Qprojector| retained independently",
            "needed_inputs": "Pi_M same-object theorem; projector variation owner; commutator bound",
            "current_value": "MISSING_Q_TAU_PROJECTOR_SOURCE",
            "units": "projector charge derivative",
            "arena": "C_M; source denominator; PPN source profile",
            "source_path": str(SOURCES["qtau_ledger_993"]["path"]),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "DXH3552_7_matter_source",
            "quantity": "E_Qmatter",
            "formula": "matter/source constraint and worldtube glue contribution",
            "non_cancellation_bound": "|E_Qmatter| retained independently",
            "needed_inputs": "Hilbert-current equality; worldtube source glue; matter coupling descent",
            "current_value": "MISSING_Q_TAU_MATTER_SOURCE",
            "units": "matter/source charge derivative",
            "arena": "Newton source mass; WEP; local source coupling",
            "source_path": str(SOURCES["gauge_noether_917"]["path"]),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "DXH3552_8_constraints_curl_surface",
            "quantity": "E_constraint + E_curl + E_surface",
            "formula": "bulk constraint, field-space curl and surface/domain mismatch contributions",
            "non_cancellation_bound": "|E_constraint| + |E_curl| + |E_surface| retained independently",
            "needed_inputs": "Euler/Ward ledger; curl zero/bound; tau/surface lock; boundary exactness",
            "current_value": "MISSING_CONSTRAINT_CURL_SURFACE_VECTOR",
            "units": "charge derivative or normalized residual",
            "arena": "H_tau integrability; local GR; Newton source",
            "source_path": str(SOURCES["htau_curl_2667"]["path"]),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def partial_mass_rows() -> list[dict[str, Any]]:
    return [
        {
            "row_id": "PMDX3552_0_total",
            "quantity": "partial_M D_X H_tau",
            "formula": "partial_M D_X H_tau = sum_i partial_M E_i",
            "non_cancellation_bound": "|partial_M D_X H_tau| <= |partial_M E_tau| + |partial_M E_theta| + |partial_M E_QEH| + |partial_M E_Qboundary| + |partial_M E_Qextra| + |partial_M E_Qprojector| + |partial_M E_Qmatter| + |partial_M E_constraint| + |partial_M E_curl| + |partial_M E_surface| + |partial_M E_units|",
            "needed_inputs": "mass derivative of each H_tau leakage component",
            "current_value": "MISSING_PARTIAL_M_DX_HTAU_COMPONENT_VECTOR",
            "units": "mass-normalized charge derivative",
            "feeds": "C_M via partial_M A_X^M",
            "source_path": str(SOURCES["mhref_leakage_3551"]["path"]),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "row_id": "PMDX3552_1_projector_matter",
            "quantity": "partial_M(E_Qprojector + E_Qmatter)",
            "formula": "source-sensitive charge leakage through Pi_M and Hilbert-current glue",
            "non_cancellation_bound": "|partial_M E_Qprojector| + |partial_M E_Qmatter|",
            "needed_inputs": "Pi_M variation owner; worldtube/source current equality; source-coordinate branch",
            "current_value": "MISSING_SOURCE_SENSITIVE_CHARGE_DERIVATIVE",
            "units": "mass-normalized source charge leakage",
            "feeds": "C_M; Newton source normalization",
            "source_path": str(SOURCES["qtau_ledger_993"]["path"]),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "row_id": "PMDX3552_2_boundary_extra",
            "quantity": "partial_M(E_Qboundary + E_Qextra)",
            "formula": "mass dependence of boundary/reference and extra-sector charge leakage",
            "non_cancellation_bound": "|partial_M E_Qboundary| + |partial_M E_Qextra|",
            "needed_inputs": "source-blind reference derivative; extra-sector no-source theorem or coefficient vector",
            "current_value": "MISSING_BOUNDARY_EXTRA_MASS_DERIVATIVE",
            "units": "mass-normalized charge leakage",
            "feeds": "C_M; H_ref separation; local GR residual",
            "source_path": str(SOURCES["hamiltonian_contract"]["path"]),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "row_id": "PMDX3552_3_integrability",
            "quantity": "partial_M(E_curl + E_surface)",
            "formula": "mass dependence of H_tau curl and surface branch mismatch",
            "non_cancellation_bound": "|partial_M E_curl| + |partial_M E_surface|",
            "needed_inputs": "curl zero/bound by source mass branch; same surface/coframe lock",
            "current_value": "MISSING_CURL_SURFACE_MASS_DERIVATIVE",
            "units": "mass-normalized curl leakage",
            "feeds": "C_M; M_H_ref positivity and path independence",
            "source_path": str(SOURCES["htau_curl_2667"]["path"]),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "D3552_0_theorem_verdict",
            "question": "Did 3552 make H_tau live?",
            "decision": "No live claim. It proves the exact q-basic charge theorem, but the parent theta/Q_tau chain is not extracted.",
            "basis": "1008, 771, 993 and 2667 keep L_parent, theta_MTS, retained Q_tau pieces, tau action and integrability unsigned.",
            "consequence": "H_tau is now a component charge-extraction problem, not a vague denominator problem.",
            "valid_for_claim": "False",
        },
        {
            "decision_id": "D3552_1_EH_guard",
            "question": "Can the EH/GR Hamiltonian charge be used?",
            "decision": "Only as a comparison template.",
            "basis": "EH charge lacks MTS residual, projector, boundary/reference, extra and matter/source sector ownership.",
            "consequence": "No GR/Newton reduction claim from EH import alone.",
            "valid_for_claim": "False",
        },
        {
            "decision_id": "D3552_2_next_target",
            "question": "What is the least-cheatable next step?",
            "decision": "Build the parent sector current-chain contract for theta_MTS.",
            "basis": "Without delta L_parent and theta_MTS by sector, Q_tau and H_tau cannot be extracted or bounded numerically.",
            "consequence": "Move to 3553: sector action variation/theta source pack.",
            "valid_for_claim": "False",
        },
    ]


def status_rows() -> list[dict[str, Any]]:
    return [
        {
            "status_id": "STATUS3552_0",
            "checkpoint": "3552 H_tau q-basic charge extraction or D_X H_tau bound pack",
            "claim_allowed": "False",
            "H_tau_status": "EXACT_QBASIC_IF_PARENT_THETA_QTAU_CHAIN_DESCENDS_AND_IS_INTEGRABLE; CURRENTLY_UNSIGNED",
            "DX_Htau_status": "component leakage vector installed with no-cancellation bounds",
            "partialM_DX_Htau_status": "C_M input rows installed; source-sensitive mass derivative still missing",
            "strongest_result": "H_tau obstruction reduced to parent current-chain extraction plus retained-sector leakage vector",
            "next_target": "3553-Y5-R2FR-parent-sector-current-chain-theta-source-pack.md",
            "valid_for_claim": "False",
        }
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT3552_0",
            "target_doc": "3553-Y5-R2FR-parent-sector-current-chain-theta-source-pack.md",
            "target_script": "scripts/Y5_R2FR_3553_parent_sector_current_chain_theta_source_pack.py",
            "objective": "construct the parent sector current-chain contract L_parent -> theta_MTS by retained sector, or produce source-ready nonclaim theta leakage rows for EH, boundary, extra, projector and matter/source sectors",
            "success_gate": "either theta_MTS is assembled from parent sector variations with source paths, or every missing theta sector has explicit leakage rows with units, arena projections and valid_for_claim=false",
            "reason": "theta_MTS is the first missing object in the H_tau charge theorem and unlocks Q_tau/integrability scoring",
            "valid_for_claim": "False",
        }
    ]


def validation_rows(
    generated_csvs: list[Path],
    sources: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    chain: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    partials: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    all_sources_exist = all(row["exists"] == "True" for row in sources)
    csvs_parse = all(csv_parse_ok(path) for path in generated_csvs)
    qbasic_theorem_present = any(row["theorem_id"] == "HTD3552_1_qbasic_charge_theorem" for row in theorem)
    required_chain = {"CCA3552_0_parent_action", "CCA3552_2_theta_MTS", "CCA3552_3_Qtau_split", "CCA3552_6_integrability"}
    chain_covered = required_chain.issubset({row["chain_id"] for row in chain})
    all_nonclaim = (
        all(row["valid_for_claim"] == "False" for row in theorem)
        and all(row["claim_allowed"] == "False" and row["valid_for_claim"] == "False" for row in chain)
        and all(row["claim_allowed"] == "False" and row["valid_for_claim"] == "False" for row in bounds)
        and all(row["claim_allowed"] == "False" and row["valid_for_claim"] == "False" for row in partials)
        and all(row["valid_for_claim"] == "False" for row in decisions)
    )
    leakage_vector_ready = any(row["bound_id"] == "DXH3552_0_total" and "+" in row["non_cancellation_bound"] for row in bounds)
    missing_markers_present = all("MISSING_" in row["current_value"] for row in bounds + partials)
    no_formalization_outputs = all(not path.resolve().is_relative_to(FORMALIZATION.resolve()) for path in generated_csvs)

    return [
        {
            "validation_id": "VAL3552_0_sources_exist",
            "passes": bool_text(all_sources_exist),
            "status": "PASS" if all_sources_exist else "FAIL",
            "detail": f"{sum(row['exists'] == 'True' for row in sources)}/{len(sources)} cited source paths exist",
        },
        {
            "validation_id": "VAL3552_1_generated_csvs_parse",
            "passes": bool_text(csvs_parse),
            "status": "PASS" if csvs_parse else "FAIL",
            "detail": f"{len(generated_csvs)} generated CSV files parse with DictReader",
        },
        {
            "validation_id": "VAL3552_2_qbasic_charge_theorem_present",
            "passes": bool_text(qbasic_theorem_present),
            "status": "PASS" if qbasic_theorem_present else "FAIL",
            "detail": "H_tau q-basic charge theorem is present",
        },
        {
            "validation_id": "VAL3552_3_charge_chain_covered",
            "passes": bool_text(chain_covered),
            "status": "PASS" if chain_covered else "FAIL",
            "detail": "parent action, theta_MTS, Q_tau split and integrability gates are covered",
        },
        {
            "validation_id": "VAL3552_4_all_rows_nonclaim",
            "passes": bool_text(all_nonclaim),
            "status": "PASS" if all_nonclaim else "FAIL",
            "detail": "all theorem/audit/bound/decision rows keep claims disabled",
        },
        {
            "validation_id": "VAL3552_5_leakage_vector_non_cancellation",
            "passes": bool_text(leakage_vector_ready and missing_markers_present),
            "status": "PASS" if leakage_vector_ready and missing_markers_present else "FAIL",
            "detail": "D_X H_tau and partial_M D_X H_tau rows expose missing inputs and use no-cancellation bounds",
        },
        {
            "validation_id": "VAL3552_6_formalization_workbench_untouched",
            "passes": bool_text(no_formalization_outputs),
            "status": "PASS" if no_formalization_outputs else "FAIL",
            "detail": "3552 generated outputs only inside post-checkpoint-work",
        },
    ]


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    lines = [
        "# 3552 - H_tau q-basic charge extraction or D_X H_tau bound pack",
        "",
        "## Verdict",
        "",
        "- **The exact route is now written:** `H_tau` is q-basic if the parent current chain `L_parent -> theta_MTS -> J_tau -> Q_tau^MTS -> H_tau` is built only from the same visible `q/e_obs/tau` branch and is integrable.",
        "- **The local zero is exact but not live:** if `H_tau=Hbar_tau(q(Phi))` and `Dq(v_X)=0`, then `D_X H_tau=0`.",
        "- **No EH shortcut:** the GR/EH charge is a comparison template only until MTS extracts or bounds boundary, extra, projector, matter/source and constraint pieces.",
        "- **Bound fallback installed:** if the theorem is unsigned, use an explicit no-cancellation leakage vector for `D_X H_tau` and `partial_M D_X H_tau`.",
        "",
        "## H_tau Theorem",
        "",
        markdown_table(
            rows_by_name["theorem"],
            ["theorem_id", "claim_piece", "statement", "current_status"],
        ),
        "",
        "## Parent Charge Chain",
        "",
        markdown_table(
            rows_by_name["chain"],
            ["chain_id", "object", "required_identity", "status", "if_signed"],
        ),
        "",
        "## D_X H_tau Bound Pack",
        "",
        markdown_table(
            rows_by_name["bounds"],
            ["bound_id", "quantity", "formula", "current_value", "arena"],
        ),
        "",
        "## partial_M D_X H_tau Rows",
        "",
        markdown_table(
            rows_by_name["partials"],
            ["row_id", "quantity", "formula", "current_value", "feeds"],
        ),
        "",
        "## Decisions",
        "",
        markdown_table(
            rows_by_name["decisions"],
            ["decision_id", "question", "decision", "consequence"],
        ),
        "",
        "## Validation",
        "",
        markdown_table(
            rows_by_name["validation"],
            ["validation_id", "passes", "status", "detail"],
        ),
        "",
        "## Next target",
        "",
        "Move to `3553-Y5-R2FR-parent-sector-current-chain-theta-source-pack.md`: build the sector-by-sector `theta_MTS` source pack, because it is the first missing object in the `H_tau` theorem.",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
    ]
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)

    sources = source_rows()
    theorem = theorem_rows()
    chain = chain_audit_rows()
    bounds = dxhtau_bound_rows()
    partials = partial_mass_rows()
    decisions = decision_rows()
    status = status_rows()
    next_target = next_target_rows()

    outputs: dict[Path, tuple[list[dict[str, Any]], list[str]]] = {
        OUT / "P8_Y5_R2FR_3552_SOURCE_REGISTER.csv": (
            sources,
            ["source_id", "path", "exists", "role", "valid_for_claim"],
        ),
        OUT / "P8_Y5_R2FR_3552_HTAU_QBASIC_THEOREM.csv": (
            theorem,
            [
                "theorem_id",
                "claim_piece",
                "statement",
                "proof_step",
                "condition_needed",
                "current_status",
                "source_path",
                "valid_for_claim",
            ],
        ),
        OUT / "P8_Y5_R2FR_3552_PARENT_CHARGE_CHAIN_AUDIT.csv": (
            chain,
            [
                "chain_id",
                "object",
                "required_identity",
                "current_evidence",
                "status",
                "if_signed",
                "source_path",
                "claim_allowed",
                "valid_for_claim",
            ],
        ),
        OUT / "P8_Y5_R2FR_3552_DXHTAU_LEAKAGE_BOUND_PACK.csv": (
            bounds,
            [
                "bound_id",
                "quantity",
                "formula",
                "non_cancellation_bound",
                "needed_inputs",
                "current_value",
                "units",
                "arena",
                "source_path",
                "claim_allowed",
                "valid_for_claim",
            ],
        ),
        OUT / "P8_Y5_R2FR_3552_PARTIALM_DXHTAU_BOUND_ROWS.csv": (
            partials,
            [
                "row_id",
                "quantity",
                "formula",
                "non_cancellation_bound",
                "needed_inputs",
                "current_value",
                "units",
                "feeds",
                "source_path",
                "claim_allowed",
                "valid_for_claim",
            ],
        ),
        OUT / "P8_Y5_R2FR_3552_DECISION_LEDGER.csv": (
            decisions,
            ["decision_id", "question", "decision", "basis", "consequence", "valid_for_claim"],
        ),
        OUT / "P8_Y5_R2FR_3552_STATUS.csv": (
            status,
            [
                "status_id",
                "checkpoint",
                "claim_allowed",
                "H_tau_status",
                "DX_Htau_status",
                "partialM_DX_Htau_status",
                "strongest_result",
                "next_target",
                "valid_for_claim",
            ],
        ),
        OUT / "P8_Y5_R2FR_3552_NEXT_TARGET.csv": (
            next_target,
            ["next_id", "target_doc", "target_script", "objective", "success_gate", "reason", "valid_for_claim"],
        ),
        CANONICAL_STATUS: (
            status,
            [
                "status_id",
                "checkpoint",
                "claim_allowed",
                "H_tau_status",
                "DX_Htau_status",
                "partialM_DX_Htau_status",
                "strongest_result",
                "next_target",
                "valid_for_claim",
            ],
        ),
    }

    generated_paths: list[Path] = []
    for path, (rows, fields) in outputs.items():
        write_csv(path, rows, fields)
        generated_paths.append(path)

    validation = validation_rows(generated_paths, sources, theorem, chain, bounds, partials, decisions)
    validation_path = OUT / "P8_Y5_BRR545_3552_VALIDATION.csv"
    write_csv(validation_path, validation, ["validation_id", "passes", "status", "detail"])
    generated_paths.append(validation_path)

    write_doc(
        {
            "theorem": theorem,
            "chain": chain,
            "bounds": bounds,
            "partials": partials,
            "decisions": decisions,
            "status": status,
            "next_target": next_target,
            "validation": validation,
        }
    )

    print(f"wrote {DOC}")
    for path in generated_paths:
        print(f"wrote {path}")


if __name__ == "__main__":
    main()
