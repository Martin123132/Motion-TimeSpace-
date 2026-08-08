from __future__ import annotations

import csv
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_BOUNDARY_IMPROVEMENT_CURRENT_ZERO_OR_P4_BOUNDARY_ROW_2350"

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
FORMALIZATION = PROJECT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICRO_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"

DOC = ROOT / "2350-Y5-R2FR-boundary-improvement-current-zero-or-P4-boundary-row.md"

PATHS = {
    "2349_doc": ROOT / "2349-Y5-R2FR-projective-trace-silence-or-P4-projective-component-row.md",
    "2349_next": OUT / "P8_Y5_PARENT_QLOC_2349_NEXT_TARGET.csv",
    "2349_projective": OUT / "P8_Y5_PARENT_QLOC_2349_PROJECTIVE_TRACE_SILENCE_AUDIT.csv",
    "2348_spin": OUT / "P8_Y5_PARENT_QLOC_2348_SPIN_CONNECTION_COFRAME_OWNED_AUDIT.csv",
    "2347_srng": OUT / "P8_Y5_PARENT_QLOC_2347_SRNG_ADOPTION_AND_SCOPE_AUDIT.csv",
    "2337_boundary_queue": OUT / "P8_Y5_PARENT_QLOC_2337_BOUNDARY_IMPROVEMENT_QUEUE.csv",
    "2338_bzero_audit": OUT / "P8_Y5_PARENT_QLOC_2338_BZERO_NOFLUX_THEOREM_AUDIT.csv",
    "2338_bzero_row": OUT / "P8_Y5_PARENT_QLOC_2338_BZERO_FIRST_BOUND_ROW.csv",
    "2338_denominator": OUT / "P8_Y5_PARENT_QLOC_2338_BOUNDARY_DENOMINATOR_DEPENDENCY.csv",
    "2339_theta": OUT / "P8_Y5_PARENT_QLOC_2339_THETA_QTAU_FIXED_REFERENCE_AUDIT.csv",
    "2339_mhref": OUT / "P8_Y5_PARENT_QLOC_2339_MHREF_FIRST_ROW.csv",
    "2339_dependency": OUT / "P8_Y5_PARENT_QLOC_2339_CHARGE_NORMALIZATION_DEPENDENCY.csv",
    "2182_bzero": OUT / "P8_Y5_PARENT_QLOC_2182_REQ_BZERO_ZERO_CONDITIONS.csv",
    "2183_flux": OUT / "P8_Y5_PARENT_QLOC_2183_ZERO_BOUNDARY_FLUX_AUDIT.csv",
    "2061_boundary_current": OUT / "P8_Y5_PARENT_QLOC_2061_BOUNDARY_CURRENT_DERIVATION.csv",
    "2062_boundary_silence": OUT / "P8_Y5_PARENT_QLOC_2062_BOUNDARY_SILENCE_PROOF_ATTEMPT.csv",
    "2063_object_exhaustion": OUT / "P8_Y5_PARENT_QLOC_2063_BOUNDARY_OBJECT_EXHAUSTION_ATTEMPT.csv",
    "2074_boundary_audit": OUT / "P8_Y5_PARENT_QLOC_2074_BOUNDARY_SILENCE_AUDIT.csv",
    "2152_domain": OUT / "P8_Y5_PARENT_QLOC_2152_BOUNDARY_DOMAIN_CERTIFICATE.csv",
    "2152_exactness": OUT / "P8_Y5_PARENT_QLOC_2152_BOUNDARY_EXACTNESS_CLAUSES.csv",
    "2220_improvement": OUT / "P8_Y5_PARENT_QLOC_2220_TRACEFREE_IMPROVEMENT_BIRTH_CERTIFICATE.csv",
}

SOURCES = [
    ("SRC2350_00_2349_doc", "2349_doc", ["NEXT2349_0", "boundary/improvement current"], "2349 selected boundary/improvement as next leak"),
    ("SRC2350_01_2349_next", "2349_next", ["NEXT2349_0", "boundary-improvement"], "machine-readable 2350 target"),
    ("SRC2350_02_2349_projective", "2349_projective", ["PROJ2349_1_owned_coframe_private_zero", "ZERO_INSIDE_PRIVATE_BRANCH_ONLY"], "private projective zero switch"),
    ("SRC2350_03_2348_spin", "2348_spin", ["SPIN2348_1_exact_conditional_zero", "EXACT_CONDITIONAL_THEOREM"], "coframe spin conditional zero"),
    ("SRC2350_04_2347_srng", "2347_srng", ["SRNG2347_0_private_scope", "PRIVATE_REDUCTION_ALLOWED_NONCLAIM"], "private source/readout Gamma reduction"),
    ("SRC2350_05_2337_boundary_queue", "2337_boundary_queue", ["BND2337_4_priority", "SELECTED_NEXT"], "boundary queue after private SRNG"),
    ("SRC2350_06_2338_bzero_audit", "2338_bzero_audit", ["BZT2338_6_verdict", "ZERO_THEOREM_NOT_DERIVED_RETAIN_BOUND_ROW"], "Bzero no-flux theorem attempt"),
    ("SRC2350_07_2338_bzero_row", "2338_bzero_row", ["BZR2338_0_first_row", "MISSING_B_ZERO_FLUX"], "first Bzero bound row"),
    ("SRC2350_08_2338_denominator", "2338_denominator", ["BDD2338_2_MHref", "MISSING_M_H_REF"], "boundary denominator dependency"),
    ("SRC2350_09_2339_theta", "2339_theta", ["TQF2339_8_verdict", "THEOREM_NOT_DERIVED_RETAIN_FIRST_ROW"], "theta/Q_tau fixed-reference audit"),
    ("SRC2350_10_2339_mhref", "2339_mhref", ["MHR2339_0_first_row", "MISSING_H_TAU"], "M_H_ref first row"),
    ("SRC2350_11_2339_dependency", "2339_dependency", ["CND2339_4_local_GR_Newton", "BLOCKED_BUT_NOW_ORDERED"], "charge normalization dependency"),
    ("SRC2350_12_2182_bzero", "2182_bzero", ["BZ2182_5_current_verdict", "B_ZERO_FLUX_ZERO_NOT_DERIVED"], "Bzero zero conditions"),
    ("SRC2350_13_2183_flux", "2183_flux", ["BFA2183_4_zero_flux_verdict", "ZERO_BOUNDARY_FLUX_NOT_DERIVED"], "zero boundary flux audit"),
    ("SRC2350_14_2061_boundary_current", "2061_boundary_current", ["DER2061_2_zero_theorem", "THEOREM_EXACT_IF_ALL_CLAUSES_PARENT_SIGNED"], "boundary current identity"),
    ("SRC2350_15_2062_boundary_silence", "2062_boundary_silence", ["BSP2062_3_verdict", "CONDITIONAL_PROOF_ONLY"], "boundary silence proof attempt"),
    ("SRC2350_16_2063_object_exhaustion", "2063_object_exhaustion", ["BOE2063_5_verdict", "CONDITIONAL_PROOF_ONLY"], "boundary object-exhaustion countermodel"),
    ("SRC2350_17_2074_boundary_audit", "2074_boundary_audit", ["BSA2074_5_verdict", "BOUNDARY_SILENCE_BLOCKED"], "boundary silence audit"),
    ("SRC2350_18_2152_domain", "2152_domain", ["BDC2152_5_verdict", "FAIL_CURRENT_CLAIM"], "boundary domain certificate"),
    ("SRC2350_19_2152_exactness", "2152_exactness", ["BE2152_5_verdict", "FAIL_CURRENT_CLAIM"], "boundary exactness clauses"),
    ("SRC2350_20_2220_improvement", "2220_improvement", ["TIB2220_9_verdict", "BIRTH_CERTIFICATE_FAILS_CURRENT_CORPUS"], "trace-free improvement birth certificate"),
]

OUTPUTS = {
    "sources": OUT / "P8_Y5_PARENT_QLOC_2350_SOURCE_REGISTER.csv",
    "audit": OUT / "P8_Y5_PARENT_QLOC_2350_BOUNDARY_IMPROVEMENT_ZERO_AUDIT.csv",
    "stack": OUT / "P8_Y5_PARENT_QLOC_2350_PRIVATE_BRANCH_RESIDUAL_STACK.csv",
    "p4": OUT / "P8_Y5_PARENT_QLOC_2350_P4_BOUNDARY_COMPONENT_ROW.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2350_DECISION_LEDGER.csv",
    "claims": OUT / "P8_Y5_PARENT_QLOC_2350_CLAIM_GATES.csv",
    "refusal": OUT / "P8_Y5_PARENT_QLOC_2350_REFUSAL_RUNNER.csv",
    "next": OUT / "P8_Y5_PARENT_QLOC_2350_NEXT_TARGET.csv",
    "copies": OUT / "P8_Y5_PARENT_QLOC_2350_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2350_VALIDATION.csv",
}

BRANCH_COPY_SPECS = [
    ("COPY2350_0_boundary_audit", OUTPUTS["audit"], BETA_DOCS / "BOUNDARY_IMPROVEMENT_ZERO_AUDIT_2350_NONCLAIM.csv"),
    ("COPY2350_1_boundary_p4", OUTPUTS["p4"], MICRO_RESIDUALS / "P4_BOUNDARY_COMPONENT_ROW_2350_NONCLAIM.csv"),
    ("COPY2350_2_decision", OUTPUTS["decision"], RAB_QUEUE / "JR2350_BOUNDARY_IMPROVEMENT_DECISION_LEDGER_NONCLAIM.csv"),
]


def timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        values = []
        for column in columns:
            value = str(row.get(column, "")).replace("|", "\\|").replace("\n", " ")
            values.append(value)
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, separator, *body])


def build_sources() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row_id, source_key, needles, role in SOURCES:
        path = PATHS[source_key]
        exists = path.exists()
        text = read_text(path) if exists else ""
        missing = [needle for needle in needles if needle not in text]
        rows.append(
            {
                "timestamp_utc": timestamp(),
                "branch_id": BRANCH_ID,
                "row_id": row_id,
                "source_key": source_key,
                "source_path": str(path),
                "exists": bool_text(exists),
                "required": "true",
                "needles": ";".join(needles),
                "needles_found": bool_text(exists and not missing),
                "missing_needles": ";".join(missing),
                "source_role": role,
                "valid_for_claim": "false",
            }
        )
    return rows


def build_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "BIC2350_0_target",
            "clause": "boundary/improvement current zero target",
            "formal_statement": "B_boundary_impr=0 or epsilon_boundary_abs is finite, source-backed and absolute-summed before any local-GR/Newton claim.",
            "status": "TARGET_SHARPENED_AFTER_PRIVATE_SWITCHES",
            "obstruction": "boundary current can survive even after source/readout, spin and projective private switches",
            "effect_if_closed": "private local connection residual collapses to parent-signature/source-measure gates",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "BIC2350_1_private_reduced_context",
            "clause": "private branch residual after 2347/2348/2349",
            "formal_statement": "Inside private owned-coframe+SRNG: Delta_source/readout=0, Delta_projective=0, and Delta_spin is exact conditional if the coframe-owned clause is adopted; boundary/improvement remains live.",
            "status": "PRIVATE_REDUCTION_NOT_PUBLIC_CLAIM",
            "obstruction": "private clauses are not yet a public parent action; boundary is not touched by SRNG/projective/spin switches",
            "effect_if_closed": "focuses next proof on boundary charge rather than all connection channels at once",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "BIC2350_2_exact_no_flux_stack",
            "clause": "exact no-flux theorem stack",
            "formal_statement": "B_zero_flux=0 if parent theta/Q_tau, fixed reference, compact linked surfaces, no corner/inner/outer leaks, Hilbert-topological equality and positive M_H_ref are all signed.",
            "status": "EXACT_CONDITIONAL_THEOREM",
            "obstruction": "2338/2339 show every high-value premise is still unsigned or value-missing",
            "effect_if_closed": "epsilon_Bzero_abs=0 with no cancellation or fitted reference",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "BIC2350_3_parent_charge_dependency",
            "clause": "theta/Q_tau/H_tau/H_ref dependency",
            "formal_statement": "Boundary rows cannot be normalized until M_H_ref := H_tau[S_outer]-H_ref is finite, positive, same-frame and extracted from the parent current chain.",
            "status": "MISSING_PARENT_CHARGE_STACK",
            "obstruction": "theta_MTS, Q_tau^MTS, H_tau integrability, fixed H_ref and positivity are missing",
            "effect_if_closed": "makes Bzero/R_eq/I_commutator rows scoreable without importing orbital GM",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "BIC2350_4_object_language_gap",
            "clause": "boundary/corner object exhaustion",
            "formal_statement": "Allowed boundary/corner generators must exclude hidden local R_AB, Khat, lambda_phi, projector-stress or source-worldtube endpoint terms.",
            "status": "COUNTERMODEL_OPEN",
            "obstruction": "legal boundary and corner countermodels remain open when the parent boundary grammar is unsigned",
            "effect_if_closed": "prevents surface hair from masquerading as source mass",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "BIC2350_5_projector_equality_gap",
            "clause": "Hilbert/topological equality and projector commutator",
            "formal_statement": "Pi_M J_H = J_M_top + dB_zero and [d,Pi_M]J_H=0 must hold or produce retained R_eq/I_commutator numerator rows.",
            "status": "MISSING_EQUALITY_AND_COMMUTATOR_THEOREMS",
            "obstruction": "closed topological charge can be the wrong charge; projector algebra alone is not flux closure",
            "effect_if_closed": "protects the Newton source-normalization bridge",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "BIC2350_6_tracefree_improvement_gap",
            "clause": "trace-free improvement/Khat boundary birth certificate",
            "formal_statement": "Any Khat/improvement/lambda_phi sector must be parent-adopted with zero-mode, boundary and response certificates, or remain a finite P4 component.",
            "status": "BIRTH_CERTIFICATE_FAILS_CURRENT_CORPUS",
            "obstruction": "2220 fails current adoption due phi/lambda/boundary/sign/response clauses",
            "effect_if_closed": "prevents derivative-improvement stress from entering the PPN/local branch",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "BIC2350_7_verdict",
            "clause": "derive boundary/improvement zero now",
            "formal_statement": "Current corpus proves boundary/improvement current is zero on the private local-GR branch.",
            "status": "ZERO_THEOREM_NOT_DERIVED_RETAIN_P4_BOUNDARY_ROW",
            "obstruction": "no-flux theorem is exact but unsigned; boundary denominator/source-measure data are missing",
            "effect_if_closed": "not closed; retain finite nonclaim boundary component row",
            "valid_for_claim": "false",
        },
    ]


def build_stack_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "PRS2350_0_private_connection_residual",
            "residual": "epsilon_private_connection_abs",
            "formula": "epsilon_boundary_abs + epsilon_parent_signature_abs",
            "status": "PRIVATE_REDUCED_SCHEMA_NONCLAIM",
            "meaning": "source/readout, projective and conditionally spin channels are separated; boundary is the live private leakage route",
            "next_input": "boundary no-flux theorem or P4 boundary values",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PRS2350_1_boundary_abs",
            "residual": "epsilon_boundary_abs",
            "formula": "abs(B_zero_flux)/M_H_ref + abs(Delta_symp)/M_H_ref + abs(R_eq_integral)/M_H_ref + abs(I_commutator)/M_H_ref + abs(Delta_worldtube_domain) + abs(Pi_corner)/M_H_ref",
            "status": "ABSOLUTE_SUM_NO_CANCELLATION",
            "meaning": "boundary pieces must individually vanish or be bounded; no tuning against other channels",
            "next_input": "M_H_ref and component numerators",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PRS2350_2_charge_denominator",
            "residual": "M_H_ref dependency",
            "formula": "M_H_ref := H_tau[S_outer] - H_ref",
            "status": "MISSING_H_TAU_H_REF_MHREF",
            "meaning": "without the denominator, no normalized boundary source claim is score-ready",
            "next_input": "theta/Q_tau/H_tau/H_ref extraction",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PRS2350_3_anti_circularity",
            "residual": "not_orbital_GM_imported",
            "formula": "M_H_ref cannot be filled from observed orbital GM until M_H_ref -> Poisson/Gauss -> orbital GM is derived independently",
            "status": "GUARD_READY",
            "meaning": "prevents borrowing Newton to prove Newton",
            "next_input": "parent charge/source-measure bridge",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PRS2350_4_next_order",
            "residual": "ordered local-GR bridge",
            "formula": "private connection switches -> boundary/M_H_ref -> source-measure equality -> PPN/Newton residual vector",
            "status": "ORDERED_BUT_NOT_CLOSED",
            "meaning": "we are not circling; the remaining trench is now narrower and named",
            "next_input": "2351 parent charge extraction",
            "valid_for_claim": "false",
        },
    ]


def build_p4_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "P4B2350_0_boundary_total",
            "quantity": "epsilon_boundary_abs",
            "component": "total boundary/improvement residual",
            "formula": "abs(B_zero_flux)/M_H_ref + abs(Delta_symp)/M_H_ref + abs(R_eq_integral)/M_H_ref + abs(I_commutator)/M_H_ref + abs(Delta_worldtube_domain) + abs(Pi_corner)/M_H_ref + abs(K_improvement_response)",
            "units": "dimensionless after M_H_ref/source normalization",
            "current_value": "MISSING_COMPONENT_VALUES;MISSING_M_H_REF",
            "source_path": "MISSING_PARENT_INPUT",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "P4B2350_1_Bzero_flux",
            "quantity": "epsilon_Bzero_abs",
            "component": "exact/reference boundary improvement flux",
            "formula": "abs(B_zero_flux)/M_H_ref",
            "units": "dimensionless",
            "current_value": "MISSING_B_ZERO_FLUX;MISSING_M_H_REF",
            "source_path": "P8_Y5_PARENT_QLOC_2338_BZERO_FIRST_BOUND_ROW.csv",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "P4B2350_2_Delta_symp",
            "quantity": "epsilon_HPiM_integrability_abs",
            "component": "Hamiltonian/symplectic nonintegrability",
            "formula": "abs(delta_H_tau_nonintegrable)/M_H_ref + abs(Delta_ref)/M_H_ref + abs(Delta_symp)/M_H_ref",
            "units": "dimensionless",
            "current_value": "MISSING_PARENT_THETA_QTAU;MISSING_HTAU_INTEGRABILITY",
            "source_path": "MISSING_PARENT_INPUT",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "P4B2350_3_Req",
            "quantity": "R_eq_integral_abs",
            "component": "Hilbert/topological source equality residual",
            "formula": "abs(integral(Pi_M J_H - J_M_top - dB_zero))/M_H_ref",
            "units": "dimensionless",
            "current_value": "MISSING_HILBERT_TOPOLOGICAL_EQUALITY;MISSING_M_H_REF",
            "source_path": "MISSING_SOURCE_MEASURE_BRIDGE",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "P4B2350_4_Icommutator",
            "quantity": "I_commutator_abs",
            "component": "projector/domain commutator residual",
            "formula": "abs(integral([d,Pi_M]J_H))/M_H_ref",
            "units": "dimensionless",
            "current_value": "MISSING_PIM_PARENT_ORIGIN;MISSING_M_H_REF",
            "source_path": "MISSING_PROJECTOR_CHAIN_MAP",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "P4B2350_5_worldtube_domain",
            "quantity": "Delta_worldtube_domain_abs",
            "component": "worldtube/support/domain motion leakage",
            "formula": "abs(Delta_worldtube_domain)",
            "units": "dimensionless or source-current normalized",
            "current_value": "MISSING_WORLDTUBE_SELECTOR;MISSING_COMPACT_SUPPORT_CERTIFICATE",
            "source_path": "MISSING_SOURCE_SUPPORT_MAP",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "P4B2350_6_corner_boundary",
            "quantity": "Pi_corner_abs",
            "component": "corner/inner/outer boundary hair",
            "formula": "abs(Pi_corner + Pi_inner + Pi_outer)/M_H_ref",
            "units": "dimensionless",
            "current_value": "MISSING_CORNER_CERTIFICATE;MISSING_OUTER_INNER_FLUX_ZERO",
            "source_path": "MISSING_BOUNDARY_TOPOLOGY_CERTIFICATE",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "P4B2350_7_K_improvement",
            "quantity": "K_improvement_response_abs",
            "component": "trace-free improvement/Khat/lambda_phi boundary response",
            "formula": "abs(Khat_boundary_response + lambda_phi_stress + projector_stress)",
            "units": "PPN/local residual units after response map",
            "current_value": "MISSING_KHAT_PARENT_ADOPTION;MISSING_RESPONSE_COEFFICIENTS",
            "source_path": "P8_Y5_PARENT_QLOC_2220_TRACEFREE_IMPROVEMENT_BIRTH_CERTIFICATE.csv",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "P4B2350_8_no_claim",
            "quantity": "local_GR_boundary_gate",
            "component": "claim policy",
            "formula": "claim_allowed = Z_boundary_global OR sourced_numeric_bound_passes_all_local_arenas",
            "units": "boolean gate",
            "current_value": "FALSE",
            "source_path": "P8_Y5_PARENT_QLOC_2350_CLAIM_GATES.csv",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
    ]


def build_decision_rows() -> list[dict[str, Any]]:
    return [
        {"branch_id": BRANCH_ID, "row_id": "DEC2350_0_result", "decision": "do not promote boundary/improvement zero", "reason": "the no-flux theorem stack is exact but still lacks parent theta/Q_tau, fixed reference, M_H_ref, boundary object exhaustion and source-measure equality", "consequence": "retain P4 boundary component row", "status": "CONDITIONAL_THEOREM_P4_RETAINED", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "DEC2350_1_private_narrowing", "decision": "treat boundary as the primary private-branch leak", "reason": "2347/2348/2349 narrowed source/readout, spin and projective channels but explicitly did not close boundary", "consequence": "focus next proof on parent charge and boundary normalization, not every connection channel at once", "status": "PRIVATE_BRANCH_NARROWED", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "DEC2350_2_bound_row", "decision": "stage absolute P4 boundary row", "reason": "finite residual path needs no-cancellation absolute components with M_H_ref denominator", "consequence": "future score cannot hide boundary current in fitted reference or orbital GM", "status": "BOUNDARY_P4_ROW_STAGED_NONCLAIM", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "DEC2350_3_next", "decision": "attack parent theta/Q_tau/H_tau/H_ref extraction next", "reason": "boundary rows cannot close or score until the parent charge and positive same-frame denominator are real", "consequence": "next target is parent charge extraction/source row", "status": "SELECT_PARENT_CHARGE_EXTRACTION_NEXT", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "DEC2350_4_public_policy", "decision": "no GitHub update from 2350", "reason": "this is private consolidation and residual staging, not a local-GR/Newton proof", "consequence": "continue private derivation work", "status": "NO_GITHUB_EVIDENCE_UPDATE", "valid_for_claim": "false"},
    ]


def build_claim_rows() -> list[dict[str, Any]]:
    return [
        {"branch_id": BRANCH_ID, "row_id": "CG2350_0_private_narrowing", "gate": "private connection residual narrowed to boundary plus parent signature/source-measure gates", "passed": "true", "claim_effect": "private working simplification only; not valid_for_claim", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2350_1_boundary_zero_public", "gate": "boundary/improvement current theorem-zero", "passed": "false", "claim_effect": "P4 boundary row retained", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2350_2_parent_charge", "gate": "theta_MTS/Q_tau/H_tau/H_ref/M_H_ref extracted and fixed", "passed": "false", "claim_effect": "boundary rows non-score-ready", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2350_3_object_exhaustion", "gate": "boundary/corner/improvement object language exhausted", "passed": "false", "claim_effect": "countermodels remain open", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2350_4_source_measure", "gate": "Hilbert/topological/source-measure equality and projector commutator closed", "passed": "false", "claim_effect": "Newton source normalization remains blocked", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2350_5_p4_score_ready", "gate": "boundary P4 row has values, units, source paths and local projections", "passed": "false", "claim_effect": "nonclaim placeholder only", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2350_6_local_GR_Newton", "gate": "local GR/Newton boundary bridge derived", "passed": "false", "claim_effect": "parent charge/source-measure/PPN gates remain", "valid_for_claim": "false"},
    ]


def build_refusal_rows() -> list[dict[str, Any]]:
    return [
        {"branch_id": BRANCH_ID, "row_id": "REF2350_0_private_narrowing_as_claim", "claim": "private narrowing proves local GR/Newton", "allowed": "false", "reason": "private source/readout/spin/projective switches do not close boundary or parent charge", "blocking_rows": "BIC2350_7_verdict;CG2350_6_local_GR_Newton", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "REF2350_1_stokes_shortcut", "claim": "Stokes/exactness alone kills boundary flux", "allowed": "false", "reason": "domain, corners, harmonic edge modes, fixed reference and weighted kernels must be certified", "blocking_rows": "BIC2350_4_object_language_gap;P4B2350_6_corner_boundary", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "REF2350_2_EH_import", "claim": "use EH theta/Q_tau/H_ref as full MTS boundary charge", "allowed": "false", "reason": "MTS parent current-chain extraction and extra-sector silence are missing", "blocking_rows": "BIC2350_3_parent_charge_dependency;CG2350_2_parent_charge", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "REF2350_3_orbital_GM_denominator", "claim": "fill M_H_ref from observed orbital GM", "allowed": "false", "reason": "that borrows Newton/source normalization before deriving the bridge", "blocking_rows": "PRS2350_3_anti_circularity;P4B2350_0_boundary_total", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "REF2350_4_p4_as_pass", "claim": "P4 boundary row is an empirical pass", "allowed": "false", "reason": "component values, M_H_ref, response maps, source paths and bounds are missing", "blocking_rows": "P4B2350_0_boundary_total;CG2350_5_p4_score_ready", "valid_for_claim": "false"},
    ]


def build_next_rows() -> list[dict[str, Any]]:
    return [
        {"branch_id": BRANCH_ID, "row_id": "NEXT2350_0", "next_target": "2351-Y5-R2FR-parent-theta-Qtau-Htau-Href-extraction-or-source-row.md", "why": "boundary zero or scoring is impossible until theta_MTS, Q_tau^MTS, H_tau, fixed H_ref and positive same-frame M_H_ref are extracted from the parent action or retained as sourced residuals", "route_type": "local_GR_derivation_next_step", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "NEXT2350_1", "next_target": "2351b-Y5-R2FR-Hilbert-source-charge-equality-or-Req-Icommutator-bound.md", "why": "even with M_H_ref, the Hamiltonian/Hilbert/topological/source charge equality must close or produce R_eq/I_commutator rows", "route_type": "parallel_nonclaim", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "NEXT2350_2", "next_target": "2351c-Y5-R2FR-boundary-component-source-acquisition.md", "why": "fallback if derivation stalls: source B_zero, Delta_symp, R_eq, I_commutator, worldtube and corner rows without claiming a pass", "route_type": "fallback_nonclaim", "valid_for_claim": "false"},
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row_id, source, destination in BRANCH_COPY_SPECS:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
        rows.append(
            {
                "timestamp_utc": timestamp(),
                "branch_id": BRANCH_ID,
                "row_id": row_id,
                "source_csv": str(source.relative_to(ROOT)),
                "branch_copy_path": str(destination),
                "copy_exists": bool_text(destination.exists()),
                "row_count": len(read_csv_rows(destination)),
                "valid_for_claim": "false",
            }
        )
    return rows


def build_validation(
    sources: list[dict[str, Any]],
    audit_rows: list[dict[str, Any]],
    stack_rows: list[dict[str, Any]],
    p4_rows: list[dict[str, Any]],
    decision_rows: list[dict[str, Any]],
    claim_rows: list[dict[str, Any]],
    refusal_rows: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    copy_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(row_id: str, passed: bool, detail: str) -> None:
        rows.append({"timestamp_utc": timestamp(), "branch_id": BRANCH_ID, "row_id": row_id, "status": "PASS" if passed else "FAIL", "detail": detail, "valid_for_claim": "false"})

    add("VAL2350_00_required_sources_exist", all(row["exists"] == "true" for row in sources), "every required source path exists")
    add("VAL2350_01_required_needles_found", all(row["needles_found"] == "true" for row in sources), "all required source needles were found")
    add("VAL2350_02_private_narrowing_recorded", any(row["row_id"] == "BIC2350_1_private_reduced_context" and row["status"] == "PRIVATE_REDUCTION_NOT_PUBLIC_CLAIM" for row in audit_rows), "private connection narrowing recorded without public claim")
    add("VAL2350_03_boundary_zero_not_promoted", any(row["row_id"] == "BIC2350_7_verdict" and row["status"] == "ZERO_THEOREM_NOT_DERIVED_RETAIN_P4_BOUNDARY_ROW" for row in audit_rows), "boundary/improvement zero not promoted")
    add("VAL2350_04_mhref_dependency_named", any(row["row_id"] == "BIC2350_3_parent_charge_dependency" and row["status"] == "MISSING_PARENT_CHARGE_STACK" for row in audit_rows), "M_H_ref/theta/Q_tau dependency named")
    add("VAL2350_05_residual_stack_absolute", any(row["row_id"] == "PRS2350_1_boundary_abs" and row["status"] == "ABSOLUTE_SUM_NO_CANCELLATION" for row in stack_rows), "boundary residual stack uses absolute no-cancellation sum")
    add("VAL2350_06_p4_rows_nonready", all(row["score_ready"] == "false" and row["valid_for_claim"] == "false" for row in p4_rows), "P4 boundary rows are non-score-ready and nonclaim")
    add("VAL2350_07_p4_missing_inputs_flagged", any("MISSING_B_ZERO_FLUX" in row["current_value"] for row in p4_rows) and any("MISSING_M_H_REF" in row["current_value"] for row in p4_rows), "P4 rows explicitly flag missing boundary flux and denominator")
    private_gate = [row for row in claim_rows if row["row_id"] == "CG2350_0_private_narrowing"]
    public_gates = [row for row in claim_rows if row["row_id"] != "CG2350_0_private_narrowing"]
    add("VAL2350_08_claim_gates_blocked_except_private", bool(private_gate and private_gate[0]["passed"] == "true") and all(row["passed"] == "false" for row in public_gates) and all(row["valid_for_claim"] == "false" for row in claim_rows), "only private narrowing gate passes and remains not valid_for_claim")
    add("VAL2350_09_refusals_block_shortcuts", all(row["allowed"] == "false" for row in refusal_rows), "shortcut claims refused")
    add("VAL2350_10_next_selected", any(row["row_id"] == "NEXT2350_0" and "parent-theta-Qtau-Htau-Href" in row["next_target"] for row in next_rows), "parent charge extraction next target recorded")
    add("VAL2350_11_branch_copies_parse", all(row["copy_exists"] == "true" and int(row["row_count"]) > 0 for row in copy_rows), "branch copies exist and parse")
    generated_groups = [sources, audit_rows, stack_rows, p4_rows, decision_rows, claim_rows, refusal_rows, next_rows, copy_rows]
    add("VAL2350_12_no_claim_flags", all(row.get("valid_for_claim") == "false" for group in generated_groups for row in group), "no generated row is valid_for_claim=true")
    checkpoint_needles = [
        "BOUNDARY_IMPROVEMENT_ZERO_AUDIT_2350",
        "P4_BOUNDARY_COMPONENT_ROW_2350",
        "JR2350_BOUNDARY_IMPROVEMENT",
        "Y5_R2FR_boundary_improvement",
    ]
    formalization_hits: list[str] = []
    if FORMALIZATION.exists():
        for needle in checkpoint_needles:
            try:
                result = subprocess.run(["rg", "-n", "--fixed-strings", needle, str(FORMALIZATION)], capture_output=True, text=True, timeout=30, check=False)
            except (OSError, subprocess.TimeoutExpired):
                result = subprocess.CompletedProcess(args=[], returncode=1, stdout="", stderr="")
            if result.returncode == 0 and result.stdout.strip():
                formalization_hits.extend(result.stdout.strip().splitlines())
    add("VAL2350_13_formalization_untouched_by_2350", not formalization_hits, "no 2350 checkpoint output appears in formalization-workbench")
    add("VAL2350_14_no_github_policy", any(row["row_id"] == "DEC2350_4_public_policy" and row["status"] == "NO_GITHUB_EVIDENCE_UPDATE" for row in decision_rows), "public GitHub update not recommended from 2350")
    add("VAL2350_OVERALL", all(row["status"] == "PASS" for row in rows), "2350 consolidates the private connection narrowing, rejects boundary/improvement zero promotion, stages an absolute P4 boundary row, and selects parent theta/Q_tau/H_tau/H_ref extraction next.")
    return rows


def write_doc(
    sources: list[dict[str, Any]],
    audit_rows: list[dict[str, Any]],
    stack_rows: list[dict[str, Any]],
    p4_rows: list[dict[str, Any]],
    decision_rows: list[dict[str, Any]],
    claim_rows: list[dict[str, Any]],
    refusal_rows: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    copy_rows: list[dict[str, Any]],
    validation_rows: list[dict[str, Any]],
) -> None:
    sections = [
        "# 2350 - Boundary Improvement Current Zero Or P4 Boundary Row",
        "",
        "## Summary",
        "",
        "2350 is the consolidation checkpoint after the private connection narrowing.",
        "",
        "The useful progress is that the private branch is now much less foggy: SRNG/OFC removes source/readout Gamma leakage",
        "inside the working branch, the coframe-owned spin connection gives an exact conditional spin-zero route, and projective trace",
        "is zero inside the private owned-coframe+SRNG branch. What survives that whole squeeze is boundary/improvement current.",
        "",
        "The boundary no-flux theorem is mathematically sharp but not parent-signed. It needs parent `theta_MTS/Q_tau^MTS`, fixed",
        "`H_ref`, integrable `H_tau`, positive same-frame `M_H_ref`, compact/corner-free boundary support, Hilbert/source equality,",
        "projector-commutator silence, and no hidden Khat/lambda_phi improvement stress. Those are not present as claim-grade inputs.",
        "",
        "So no local-GR/Newton claim is made. The correct move is a strict absolute P4 boundary row plus the next derivation target:",
        "extract the parent charge and fixed denominator rather than importing EH or observed orbital GM.",
        "",
        "## Source Register",
        "",
        markdown_table(sources, ["row_id", "source_key", "source_path", "exists", "required", "needles_found", "source_role", "valid_for_claim"]),
        "",
        "## Boundary Improvement Zero Audit",
        "",
        markdown_table(audit_rows, ["row_id", "clause", "formal_statement", "status", "obstruction", "effect_if_closed", "valid_for_claim"]),
        "",
        "## Private Branch Residual Stack",
        "",
        markdown_table(stack_rows, ["row_id", "residual", "formula", "status", "meaning", "next_input", "valid_for_claim"]),
        "",
        "## P4 Boundary Component Row",
        "",
        markdown_table(p4_rows, ["row_id", "quantity", "component", "formula", "units", "current_value", "source_path", "score_ready", "valid_for_claim"]),
        "",
        "## Decision Ledger",
        "",
        markdown_table(decision_rows, ["row_id", "decision", "reason", "consequence", "status", "valid_for_claim"]),
        "",
        "## Claim Gates",
        "",
        markdown_table(claim_rows, ["row_id", "gate", "passed", "claim_effect", "valid_for_claim"]),
        "",
        "## Refusal Runner",
        "",
        markdown_table(refusal_rows, ["row_id", "claim", "allowed", "reason", "blocking_rows", "valid_for_claim"]),
        "",
        "## Next Target",
        "",
        markdown_table(next_rows, ["row_id", "next_target", "why", "route_type", "valid_for_claim"]),
        "",
        "## Branch Copies",
        "",
        markdown_table(copy_rows, ["row_id", "source_csv", "branch_copy_path", "copy_exists", "row_count", "valid_for_claim"]),
        "",
        "## Validation",
        "",
        markdown_table(validation_rows, ["row_id", "status", "detail", "valid_for_claim"]),
        "",
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    sources = build_sources()
    audit_rows = build_audit_rows()
    stack_rows = build_stack_rows()
    p4_rows = build_p4_rows()
    decision_rows = build_decision_rows()
    claim_rows = build_claim_rows()
    refusal_rows = build_refusal_rows()
    next_rows = build_next_rows()

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["audit"], audit_rows)
    write_csv(OUTPUTS["stack"], stack_rows)
    write_csv(OUTPUTS["p4"], p4_rows)
    write_csv(OUTPUTS["decision"], decision_rows)
    write_csv(OUTPUTS["claims"], claim_rows)
    write_csv(OUTPUTS["refusal"], refusal_rows)
    write_csv(OUTPUTS["next"], next_rows)

    copy_rows = copy_branch_outputs()
    write_csv(OUTPUTS["copies"], copy_rows)

    validation_rows = build_validation(sources, audit_rows, stack_rows, p4_rows, decision_rows, claim_rows, refusal_rows, next_rows, copy_rows)
    write_csv(OUTPUTS["validation"], validation_rows)
    write_doc(sources, audit_rows, stack_rows, p4_rows, decision_rows, claim_rows, refusal_rows, next_rows, copy_rows, validation_rows)
    print(f"2350 checkpoint generated: {DOC}")
    print(f"Validation: {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
