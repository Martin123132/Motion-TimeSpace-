from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_PARENT_THETA_QTAU_FIXED_REFERENCE_OR_MHREF_FIRST_ROW_2339"

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
FORMALIZATION = PROJECT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICRO_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"

DOC = ROOT / "2339-Y5-R2FR-parent-theta-Qtau-fixed-reference-or-MHref-first-row.md"

PATHS = {
    "2338_doc": ROOT / "2338-Y5-R2FR-boundary-no-flux-theorem-or-Bzero-first-bound-row.md",
    "2338_validation": OUT / "P8_Y5_BRR545_2338_VALIDATION.csv",
    "2338_next": OUT / "P8_Y5_PARENT_QLOC_2338_NEXT_TARGET.csv",
    "2338_dependency": OUT / "P8_Y5_PARENT_QLOC_2338_BOUNDARY_DENOMINATOR_DEPENDENCY.csv",
    "2338_bzero_row": OUT / "P8_Y5_PARENT_QLOC_2338_BZERO_FIRST_BOUND_ROW.csv",
    "boundary_status": OUT / "P8_Y5_BOUNDARY_REFERENCE_FIRST_ROW_STATUS.csv",
    "1006_doc": ROOT / "1006-Y5-R10-MHref-positive-same-frame-denominator-or-Htau-source-row.md",
    "1007_doc": ROOT / "1007-Y5-R10-Htau-integrability-fixed-reference-theorem-or-symplectic-residual-row.md",
    "1008_doc": ROOT / "1008-Y5-R10-parent-theta-Qtau-extraction-or-charge-decomposition-runner.md",
    "1009_doc": ROOT / "1009-Y5-R10-parent-current-chain-action-contract-or-sector-variation-runner.md",
    "1016_doc": ROOT / "1016-Y5-R10-parent-worldtube-source-measure-selector-or-R_eq-first-input.md",
    "Qtau_decomposition": OUT / "P8_Y5_R10_993_QTAU_DECOMPOSITION_LEDGER.csv",
    "hamiltonian_contract": OUT / "P8_mass_current_Hamiltonian_boundary_charge_CONTRACT.csv",
    "mass_flux_contract": OUT / "P8_mass_flux_projector_Euler_calibration_CONTRACT.csv",
    "source_flux_theorem": OUT / "P8_SOURCE_MEASURE_MEFF_FLUX_THEOREM.csv",
    "parent_noether_chain": OUT / "P8_PARENT_NOETHER_CLOSURE_DERIVATION_CHAIN.csv",
}

SOURCES = [
    ("SRC2339_00_2338_doc", "2338_doc", PATHS["2338_doc"], ["BDD2338_0_theta_Qtau", "BDD2338_2_MHref"], "2338 selected theta/Q_tau, fixed reference and M_H_ref as the next charge blocker"),
    ("SRC2339_01_2338_validation", "2338_validation", PATHS["2338_validation"], ["VAL2338_OVERALL", "PASS"], "2338 validation"),
    ("SRC2339_02_2338_next", "2338_next", PATHS["2338_next"], ["NEXT2338_0", "parent-theta-Qtau-fixed-reference"], "machine-readable 2339 target"),
    ("SRC2339_03_2338_dependency", "2338_dependency", PATHS["2338_dependency"], ["BDD2338_0_theta_Qtau", "BDD2338_1_fixed_reference", "BDD2338_2_MHref"], "boundary denominator dependency chain"),
    ("SRC2339_04_2338_bzero_row", "2338_bzero_row", PATHS["2338_bzero_row"], ["epsilon_Bzero_abs", "MISSING_M_H_REF"], "Bzero row waiting on M_H_ref"),
    ("SRC2339_05_boundary_status", "boundary_status", PATHS["boundary_status"], ["M_H_ref", "missing_claim_valid_source_or_zero_theorem"], "current M_H_ref first-row status"),
    ("SRC2339_06_1006_doc", "1006_doc", PATHS["1006_doc"], ["MHA1006_1_integrability", "MHS1006_0_Htau_minus_Href"], "positive same-frame M_H_ref prior attempt"),
    ("SRC2339_07_1007_doc", "1007_doc", PATHS["1007_doc"], ["HTA1007_1_parent_theta_Qtau", "HTA1007_3_fixed_reference", "SRS1007_0_integrability_formula"], "H_tau integrability/fixed reference blocker"),
    ("SRC2339_08_1008_doc", "1008_doc", PATHS["1008_doc"], ["PVA1008_1_theta_MTS", "QTA1008_8_Q_total", "CDS1008_4_total_promoter"], "parent theta/Q_tau extraction audit"),
    ("SRC2339_09_1009_doc", "1009_doc", PATHS["1009_doc"], ["PCS1009_9_total_parent_contract", "CG1009_1_theta_MTS", "CG1009_2_Qtau_MTS"], "sector parent-action contract"),
    ("SRC2339_10_1016_doc", "1016_doc", PATHS["1016_doc"], ["PSC1016_5_dressed_source_charge", "FIS1016_0_M_H_ref"], "worldtube/source-measure M_H_ref contract"),
    ("SRC2339_11_Qtau_decomposition", "Qtau_decomposition", PATHS["Qtau_decomposition"], ["QDEC993_5_total", "not_promoted"], "current Q_tau decomposition ledger"),
    ("SRC2339_12_hamiltonian_contract", "hamiltonian_contract", PATHS["hamiltonian_contract"], ["HC2_differentiable_integrable_Hxi", "HC4_charge_equals_PiM_Hilbert_mass"], "Hamiltonian boundary charge contract"),
    ("SRC2339_13_mass_flux_contract", "mass_flux_contract", PATHS["mass_flux_contract"], ["MF7_constant_universal_coupling_needed", "not_parent_derived"], "mass/source flux calibration contract"),
    ("SRC2339_14_source_flux_theorem", "source_flux_theorem", PATHS["source_flux_theorem"], ["M_eff", "closure_not_derived_for_current_MTS"], "source-measure flux theorem status"),
    ("SRC2339_15_parent_noether_chain", "parent_noether_chain", PATHS["parent_noether_chain"], ["Q_M[", "D505_2_charge_form"], "parent Noether/charge closure chain"),
]

OUTPUTS = {
    "sources": OUT / "P8_Y5_PARENT_QLOC_2339_SOURCE_REGISTER.csv",
    "audit": OUT / "P8_Y5_PARENT_QLOC_2339_THETA_QTAU_FIXED_REFERENCE_AUDIT.csv",
    "mhref_first": OUT / "P8_Y5_PARENT_QLOC_2339_MHREF_FIRST_ROW.csv",
    "normalization": OUT / "P8_Y5_PARENT_QLOC_2339_CHARGE_NORMALIZATION_DEPENDENCY.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2339_DECISION_LEDGER.csv",
    "claims": OUT / "P8_Y5_PARENT_QLOC_2339_CLAIM_GATES.csv",
    "refusal": OUT / "P8_Y5_PARENT_QLOC_2339_REFUSAL_RUNNER.csv",
    "next": OUT / "P8_Y5_PARENT_QLOC_2339_NEXT_TARGET.csv",
    "copies": OUT / "P8_Y5_PARENT_QLOC_2339_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2339_VALIDATION.csv",
}

BRANCH_COPY_SPECS = [
    ("COPY2339_0_audit", OUTPUTS["audit"], BETA_DOCS / "THETA_QTAU_FIXED_REFERENCE_AUDIT_2339_NONCLAIM.csv"),
    ("COPY2339_1_mhref", OUTPUTS["mhref_first"], MICRO_RESIDUALS / "MHref_first_row_2339_nonclaim.csv"),
    ("COPY2339_2_decision", OUTPUTS["decision"], RAB_QUEUE / "JR2339_THETA_QTAU_DECISION_LEDGER_NONCLAIM.csv"),
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


def relative_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        values = []
        for column in columns:
            value = str(row.get(column, ""))
            value = value.replace("|", "\\|").replace("\n", " ")
            values.append(value)
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, separator, *body])


def build_sources() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row_id, source_key, path, needles, role in SOURCES:
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
            "row_id": "TQF2339_0_target",
            "clause": "parent charge target",
            "mathematical_statement": "Find parent theta_MTS, Q_tau^MTS, fixed H_ref and positive M_H_ref so epsilon_Bzero_abs can be normalized without importing GR or fitting the reference.",
            "current_evidence": "2338 selects theta/Q_tau, fixed reference and M_H_ref as the next blocker",
            "status": "TARGET_SHARPENED",
            "obstruction": "all four objects must be owned together, not separately patched",
            "fallback": "stage a strict M_H_ref first row and keep boundary rows nonclaim",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "TQF2339_1_parent_L",
            "clause": "single parent current-chain action",
            "mathematical_statement": "delta L_parent = E_A delta Phi^A + d theta_MTS for EH, matter/source, boundary/reference, projector and retained MTS residual sectors.",
            "current_evidence": "1009 has a sector contract but CG1009_0_total_parent_action remains false",
            "status": "MISSING_SINGLE_PARENT_VARIATION",
            "obstruction": "sector blocks exist as contracts, not a signed total variation",
            "fallback": "require L_parent_source and sector certificates before any theta/Q_tau promotion",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "TQF2339_2_theta_Qtau",
            "clause": "theta_MTS and Q_tau^MTS extraction",
            "mathematical_statement": "J_tau = theta_MTS(L_tau Phi) - i_tau L_parent = d Q_tau^MTS + C_tau, with all retained C_tau pieces zero, bounded or sourced.",
            "current_evidence": "1008 keeps Q_tau^EH as a reference only and marks Q_tau^MTS total not promoted",
            "status": "MISSING_PARENT_THETA_QTAU",
            "obstruction": "boundary, extra, projector and matter/source pieces are not parent-extracted",
            "fallback": "charge decomposition rows remain nonclaim",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "TQF2339_3_fixed_reference",
            "clause": "fixed reference/counterterm",
            "mathematical_statement": "H_ref and any exact/topological boundary representative are fixed before source, radius, clock, orbit or readout choices and cannot cancel B_zero_flux post hoc.",
            "current_evidence": "1007 and 2338 both mark the fixed reference selector unsigned",
            "status": "MISSING_FIXED_REFERENCE_CERTIFICATE",
            "obstruction": "no reference selector/counterterm source with pre-readout certificate exists",
            "fallback": "post-readout or fitted H_ref attempts are refused",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "TQF2339_4_Htau_integrability",
            "clause": "Hamiltonian integrability",
            "mathematical_statement": "delta H_tau = integral_S(delta Q_tau^MTS - i_tau theta_MTS) is finite, differentiable and path independent on the same branch.",
            "current_evidence": "1007 says integrability is blocked until theta_MTS, Q_tau^MTS, tau lock, fixed reference and boundary flux are signed",
            "status": "MISSING_HTAU_INTEGRABILITY",
            "obstruction": "without integrability, H_tau is a placeholder not a source charge",
            "fallback": "epsilon_HPiM_integrability_abs remains active",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "TQF2339_5_tau_coframe_lock",
            "clause": "same tau/coframe/frame",
            "mathematical_statement": "The same observed tau and coframe define matter source, clocks, rods, H_tau, boundary surfaces and orbital readout.",
            "current_evidence": "1006, 1007 and 1016 retain same-frame/tau/source-readout locks as unsigned",
            "status": "MISSING_SAME_FRAME_LOCK",
            "obstruction": "frame leakage can masquerade as a mass-normalization residual",
            "fallback": "Delta_frame_source and source/readout leakage rows stay live",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "TQF2339_6_MHref_positive",
            "clause": "positive same-frame M_H_ref",
            "mathematical_statement": "M_H_ref := H_tau[S_outer] - H_ref is finite, positive, same-frame, source-backed and not filled from orbital GM.",
            "current_evidence": "1006 and boundary status report zero claim-valid M_H_ref rows",
            "status": "MISSING_POSITIVE_MHREF",
            "obstruction": "H_tau, H_ref, units, frame ids, source path and positivity certificate are missing",
            "fallback": "stage M_H_ref first row with valid_for_claim=false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "TQF2339_7_source_charge_identity",
            "clause": "Hamiltonian charge equals measured source normalization",
            "mathematical_statement": "M_H_ref equals the dressed Hilbert/source charge and reduces through Poisson/Gauss to measured GM only after the bridge is derived.",
            "current_evidence": "1016 gives the dressed source charge contract but marks integrability/reference lock missing",
            "status": "MISSING_SOURCE_MEASURE_BRIDGE",
            "obstruction": "using measured GM now would borrow Newton to prove Newton/local-GR recovery",
            "fallback": "anti-circularity guard remains active",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "TQF2339_8_verdict",
            "clause": "derive theta/Q_tau/fixed-reference/M_H_ref now",
            "mathematical_statement": "TQF2339_1 through TQF2339_7 would promote M_H_ref and reopen Bzero/R_eq/I_commutator scoring.",
            "current_evidence": "current corpus has contracts and schemas, not parent-signed charge extraction",
            "status": "THEOREM_NOT_DERIVED_RETAIN_FIRST_ROW",
            "obstruction": "the missing objects are upstream parent-action/current-chain data, not merely table values",
            "fallback": "M_H_ref first row plus next parent theta/Q_tau/H_tau extraction target",
            "valid_for_claim": "false",
        },
    ]


def build_mhref_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "MHR2339_0_first_row",
            "quantity": "M_H_ref",
            "formula": "M_H_ref := H_tau[S_outer] - H_ref",
            "required_columns": "system_id;tau_id;coframe_id;surface_outer;H_tau;H_tau_units;H_ref;H_ref_units;M_H_ref;M_H_ref_units;reference_rule;counterterm_convention;theta_Qtau_certificate;integrability_certificate;source_path;equation_ref;valid_for_claim",
            "current_value": "MISSING_H_TAU;MISSING_H_REF;MISSING_M_H_REF",
            "required_for_claim": "finite H_tau and H_ref; positive difference; same tau/coframe; fixed reference; parent theta/Q_tau; source path; equation ref; no orbital-GM import",
            "status": "SCHEMA_READY_VALUES_MISSING",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "MHR2339_1_parent_certificate_vector",
            "quantity": "M_H_ref_certificate_vector",
            "formula": "C_MHref=(L_parent,theta_MTS,Q_tau^MTS,tau_lock,coframe_lock,H_ref_fixed,Htau_integrable,positivity,Poisson_Gauss_bridge,extra_sector_silence)",
            "required_columns": "certificate_id;certificate_source_path;certificate_status;parent_signed;valid_for_claim",
            "current_value": "MISSING_PARENT_SIGNATURES",
            "required_for_claim": "all certificate source paths exist and every parent_signed=true",
            "status": "CERTIFICATE_VECTOR_MISSING",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "MHR2339_2_anti_circularity_guard",
            "quantity": "not_orbital_GM_imported",
            "formula": "M_H_ref cannot be filled by GM_orbit/G_ref until M_H_ref -> Poisson/Gauss -> orbital GM is derived independently",
            "required_columns": "denominator_source_method;poisson_gauss_certificate;not_orbital_GM_imported;source_path;equation_ref",
            "current_value": "ORBITAL_GM_IMPORT_FORBIDDEN",
            "required_for_claim": "source method is parent H_tau-H_ref or derived bridge, not empirical backfill",
            "status": "GUARD_READY",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "MHR2339_3_zero_switch",
            "quantity": "M_H_ref_claim_switch",
            "formula": "claim_ready=true iff TQF2339_1..7 are parent-signed and MHR2339_0 is finite positive same-frame",
            "required_columns": "parent_charge_claim;fixed_reference_claim;Htau_integrability_claim;positive_denominator_claim",
            "current_value": "THEOREM_SWITCH_REJECTED_WITHOUT_PARENT_SIGNATURE",
            "required_for_claim": "no missing parent action/current-chain inputs and no placeholder values",
            "status": "ZERO_OR_CLAIM_SWITCH_BLOCKED",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
    ]


def build_normalization_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "CND2339_0_Bzero",
            "dependent_quantity": "epsilon_Bzero_abs",
            "formula": "abs(B_zero_flux)/M_H_ref",
            "requires": "M_H_ref first row plus finite B_zero_flux numerator",
            "current_status": "BLOCKED_MISSING_MHREF_AND_NUMERATOR",
            "claim_effect": "2338 Bzero row remains non-score-ready",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CND2339_1_Delta_symp",
            "dependent_quantity": "epsilon_HPiM_integrability_abs",
            "formula": "abs(delta_H_tau_nonintegrable)/M_H_ref + abs(Delta_ref)/M_H_ref + abs(B_zero_flux)/M_H_ref + abs(Delta_symp)/M_H_ref",
            "requires": "parent theta/Q_tau, fixed H_ref, M_H_ref and same-frame component numerators",
            "current_status": "BLOCKED_MISSING_HTAU_REFERENCE_STACK",
            "claim_effect": "H_tau/M_H_ref/local-GR gates remain closed",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CND2339_2_Req",
            "dependent_quantity": "R_eq_integral",
            "formula": "integral(Pi_M J_H - J_M_top - dB_zero)/M_H_ref",
            "requires": "M_H_ref and Hilbert/topological equality or retained R_eq numerator",
            "current_status": "BLOCKED_MISSING_SOURCE_MEASURE_BRIDGE",
            "claim_effect": "conserved-wrong-object loophole remains guarded",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CND2339_3_Icommutator",
            "dependent_quantity": "I_commutator",
            "formula": "integral([d,Pi_M]J_H)/M_H_ref",
            "requires": "M_H_ref and parent Pi_M chain-map origin",
            "current_status": "BLOCKED_MISSING_PIM_PARENT_ORIGIN",
            "claim_effect": "projector/source-measure branch remains residualized",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CND2339_4_local_GR_Newton",
            "dependent_quantity": "local GR/Newton recovery",
            "formula": "parent local residuals + source charge + boundary/reference residuals vanish or are bounded before readout",
            "requires": "theta/Q_tau, fixed reference, M_H_ref, Poisson/Gauss bridge, PPN residual vector and boundary no-cancellation envelope",
            "current_status": "BLOCKED_BUT_NOW_ORDERED",
            "claim_effect": "the next proof path is narrower: parent charge first, then source-measure equality, then PPN",
            "valid_for_claim": "false",
        },
    ]


def build_decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2339_0_theorem_result",
            "decision": "do not claim parent theta/Q_tau/fixed-reference/M_H_ref",
            "reason": "the corpus still lacks a single parent current-chain variation, extracted total Q_tau, fixed reference selector and positive H_tau-H_ref row",
            "consequence": "Bzero/R_eq/I_commutator/local-GR remain blocked",
            "status": "THEOREM_FAILED_CLEANLY",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2339_1_first_row",
            "decision": "stage M_H_ref first row as nonclaim",
            "reason": "every normalized boundary/source residual needs the same denominator and anti-circularity guard",
            "consequence": "future work can fill H_tau/H_ref or prove the parent charge without changing the claim gate",
            "status": "MHREF_FIRST_ROW_STAGED_NONCLAIM",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2339_2_next",
            "decision": "attack parent theta/Q_tau extraction tied directly to H_tau/H_ref source row",
            "reason": "M_H_ref cannot be filled until the symplectic/Noether charge and fixed reference are real",
            "consequence": "next target is a parent theta/Q_tau/H_tau/H_ref extraction or source row, not GitHub",
            "status": "SELECT_2340_PARENT_CHARGE_SOURCE_ROW",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2339_3_public_policy",
            "decision": "no GitHub evidence update from 2339",
            "reason": "the result is useful private plumbing but not a stable public claim",
            "consequence": "keep trench work private until a clean checkpoint summarizes derived/conditional/blocked pieces",
            "status": "NO_GITHUB_EVIDENCE_UPDATE",
            "valid_for_claim": "false",
        },
    ]


def build_claim_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2339_0_parent_L",
            "gate": "single parent current-chain action exists",
            "passed": "false",
            "claim_effect": "theta_MTS and Q_tau^MTS cannot be promoted",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2339_1_theta_Qtau",
            "gate": "theta_MTS and Q_tau^MTS extracted",
            "passed": "false",
            "claim_effect": "H_tau integrability remains blocked",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2339_2_fixed_reference",
            "gate": "H_ref fixed before readout",
            "passed": "false",
            "claim_effect": "reference cancellation remains refused",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2339_3_Htau_integrability",
            "gate": "H_tau finite, differentiable and path-independent",
            "passed": "false",
            "claim_effect": "M_H_ref cannot be treated as a parent source charge",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2339_4_MHref_positive_same_frame",
            "gate": "M_H_ref positive same-frame denominator exists",
            "passed": "false",
            "claim_effect": "Bzero/R_eq/I_commutator rows remain non-score-ready",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2339_5_local_GR_Newton",
            "gate": "local GR/Newton recovery derived",
            "passed": "false",
            "claim_effect": "still blocked by parent charge, source-measure bridge and boundary residuals",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2339_6_github",
            "gate": "safe public GitHub update",
            "passed": "false",
            "claim_effect": "private checkpoint only",
            "valid_for_claim": "false",
        },
    ]


def build_refusal_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2339_0_EH_import",
            "claim": "use EH theta/Q_tau as the full MTS theta/Q_tau",
            "allowed": "false",
            "reason": "EH is a reference template only until MTS parent reduction and silent/topological residual clauses are signed",
            "blocking_rows": "TQF2339_1_parent_L;TQF2339_2_theta_Qtau;CG2339_1_theta_Qtau",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2339_1_fitted_reference",
            "claim": "choose H_ref to cancel B_zero_flux or Delta_ref after readout",
            "allowed": "false",
            "reason": "the reference/counterterm convention must be fixed before source/readout choices",
            "blocking_rows": "TQF2339_3_fixed_reference;CG2339_2_fixed_reference",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2339_2_orbital_GM_denominator",
            "claim": "fill M_H_ref from observed orbital GM before deriving the Poisson/Gauss bridge",
            "allowed": "false",
            "reason": "this would borrow Newton to prove the Newton/local-GR source normalization",
            "blocking_rows": "TQF2339_7_source_charge_identity;MHR2339_2_anti_circularity_guard",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2339_3_unowned_Qtau_total",
            "claim": "declare Q_tau^MTS total from the decomposition ledger alone",
            "allowed": "false",
            "reason": "the ledger names pieces but does not extract boundary, extra, projector and matter/source contributions from a parent action",
            "blocking_rows": "TQF2339_2_theta_Qtau;CG2339_1_theta_Qtau",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2339_4_local_gr",
            "claim": "2339 proves local GR/Newton recovery",
            "allowed": "false",
            "reason": "2339 only stages the exact charge/denominator contract and keeps the parent-charge gates closed",
            "blocking_rows": "CG2339_0_parent_L;CG2339_4_MHref_positive_same_frame;CG2339_5_local_GR_Newton",
            "valid_for_claim": "false",
        },
    ]


def build_next_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2339_0",
            "next_target": "2340-Y5-R2FR-parent-theta-Qtau-Htau-Href-extraction-or-source-row.md",
            "why": "M_H_ref can become real only by extracting parent theta/Q_tau and the fixed H_tau-H_ref source row, or by explicitly retaining the missing components as residuals.",
            "claim_status": "private_derivation_next_step",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2339_1",
            "next_target": "2340b-Y5-R2FR-Hilbert-source-charge-equality-or-Req-bound.md",
            "why": "even with M_H_ref, the Hamiltonian charge must equal the observed Hilbert/source charge or produce R_eq.",
            "claim_status": "parallel_nonclaim",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2339_2",
            "next_target": "2340c-Y5-R2FR-MHref-source-backed-row-acquisition.md",
            "why": "fallback if derivation stalls: fill H_tau, H_ref, units, source path and certificates as nonclaim first-row data.",
            "claim_status": "fallback_nonclaim",
            "valid_for_claim": "false",
        },
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row_id, source, destination in BRANCH_COPY_SPECS:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
        copied_rows = read_csv_rows(destination)
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "row_id": row_id,
                "source_csv": relative_path(source),
                "branch_copy_path": str(destination),
                "copy_exists": bool_text(destination.exists()),
                "row_count": str(len(copied_rows)),
                "valid_for_claim": "false",
            }
        )
    return rows


def build_validation(
    sources: list[dict[str, Any]],
    audit: list[dict[str, Any]],
    mhref: list[dict[str, Any]],
    normalization: list[dict[str, Any]],
    decision: list[dict[str, Any]],
    claims: list[dict[str, Any]],
    refusal: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    copies: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    validations: list[tuple[str, bool, str]] = []
    validations.append(("VAL2339_00_required_sources_exist", all(row["exists"] == "true" for row in sources), "every required source path exists"))
    validations.append(("VAL2339_01_required_needles_found", all(row["needles_found"] == "true" for row in sources), "all required source needles were found"))
    validations.append(("VAL2339_02_parent_theorem_not_promoted", any(row["status"] == "THEOREM_NOT_DERIVED_RETAIN_FIRST_ROW" for row in audit), "theta/Q_tau/fixed-reference/M_H_ref theorem not promoted"))
    validations.append(("VAL2339_03_mhref_first_row_staged", any(row["row_id"] == "MHR2339_0_first_row" for row in mhref), "M_H_ref first row exists"))
    validations.append(("VAL2339_04_mhref_rows_nonready", all(row["score_ready"] == "false" and row["valid_for_claim"] == "false" for row in mhref), "M_H_ref rows remain non-score-ready"))
    validations.append(("VAL2339_05_normalization_dependencies_named", len(normalization) >= 5 and all(row["valid_for_claim"] == "false" for row in normalization), "Bzero, Delta_symp, R_eq, I_commutator and local-GR dependencies named"))
    validations.append(("VAL2339_06_claim_gates_blocked", all(row["passed"] == "false" for row in claims), "all claim gates remain blocked"))
    validations.append(("VAL2339_07_refusals_block_shortcuts", all(row["allowed"] == "false" for row in refusal), "shortcut claims refused"))
    validations.append(("VAL2339_08_next_selected", any("2340-Y5-R2FR-parent-theta-Qtau-Htau-Href" in row["next_target"] for row in next_rows), "2340 parent charge/Htau/Href next target recorded"))
    validations.append(("VAL2339_09_github_blocked", any(row["status"] == "NO_GITHUB_EVIDENCE_UPDATE" for row in decision), "public GitHub update not recommended from 2339"))
    validations.append(("VAL2339_10_branch_copies_parse", all(row["copy_exists"] == "true" and int(row["row_count"]) > 0 for row in copies), "branch copies exist and parse"))

    generated_paths = [*OUTPUTS.values(), *(destination for _, _, destination in BRANCH_COPY_SPECS)]
    generated_all_exist = all(path.exists() for path in generated_paths)
    validations.append(("VAL2339_11_outputs_exist", generated_all_exist, "CSV outputs and branch copies exist before doc render"))

    no_claim_flags = True
    for path in [*OUTPUTS.values(), *(destination for _, _, destination in BRANCH_COPY_SPECS)]:
        if path.exists() and path.suffix == ".csv":
            rows = read_csv_rows(path)
            if any(row.get("valid_for_claim", "").lower() == "true" for row in rows):
                no_claim_flags = False
                break
    validations.append(("VAL2339_12_no_claim_flags", no_claim_flags, "no generated row is valid_for_claim=true"))

    formalization_clean = not any(FORMALIZATION.rglob("*2339*")) if FORMALIZATION.exists() else True
    validations.append(("VAL2339_13_formalization_untouched_by_2339", formalization_clean, "no 2339 checkpoint output appears in formalization-workbench"))

    rows = [
        {
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
            "valid_for_claim": "false",
        }
        for row_id, passed, detail in validations
    ]
    overall = all(row["status"] == "PASS" for row in rows)
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "row_id": "VAL2339_OVERALL",
            "status": "PASS" if overall else "FAIL",
            "detail": "2339 attempts parent theta/Q_tau/fixed-reference/M_H_ref closure, rejects shortcut promotion, stages M_H_ref first row, and selects parent charge/Htau/Href extraction next.",
            "valid_for_claim": "false",
        }
    )
    return rows


def write_doc(
    sources: list[dict[str, Any]],
    audit: list[dict[str, Any]],
    mhref: list[dict[str, Any]],
    normalization: list[dict[str, Any]],
    decision: list[dict[str, Any]],
    claims: list[dict[str, Any]],
    refusal: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    copies: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    text = f"""# 2339 - parent theta/Q_tau fixed-reference or M_H_ref first row

## Summary

2339 attacks the exact charge-normalization blocker selected by 2338.

The target is deliberately strict: own `theta_MTS`, `Q_tau^MTS`, fixed `H_ref`, integrable `H_tau`, and positive same-frame
`M_H_ref := H_tau[S_outer] - H_ref` before any boundary/source residual is scored.

The derivation route is now clean, but current MTS does not yet sign the required parent current-chain variation. So 2339
does **not** claim `M_H_ref`, local GR, Newton recovery, or a boundary pass. It stages the first honest `M_H_ref` row and
keeps every shortcut refused: EH-only import, fitted reference, orbital-GM denominator laundering, and unowned `Q_tau`
promotion.

## Source Register

{markdown_table(sources, ["row_id", "source_key", "source_path", "exists", "required", "needles_found", "source_role", "valid_for_claim"])}

## Theta/Q_tau Fixed-Reference Audit

{markdown_table(audit, ["row_id", "clause", "mathematical_statement", "current_evidence", "status", "obstruction", "fallback", "valid_for_claim"])}

## M_H_ref First Row

{markdown_table(mhref, ["row_id", "quantity", "formula", "current_value", "required_for_claim", "status", "score_ready", "valid_for_claim"])}

## Charge Normalization Dependency

{markdown_table(normalization, ["row_id", "dependent_quantity", "formula", "requires", "current_status", "claim_effect", "valid_for_claim"])}

## Decision Ledger

{markdown_table(decision, ["row_id", "decision", "reason", "consequence", "status", "valid_for_claim"])}

## Claim Gates

{markdown_table(claims, ["row_id", "gate", "passed", "claim_effect", "valid_for_claim"])}

## Refusal Runner

{markdown_table(refusal, ["row_id", "claim", "allowed", "reason", "blocking_rows", "valid_for_claim"])}

## Next Target

{markdown_table(next_rows, ["row_id", "next_target", "why", "claim_status", "valid_for_claim"])}

## Branch Copies

{markdown_table(copies, ["row_id", "source_csv", "branch_copy_path", "copy_exists", "row_count", "valid_for_claim"])}

## Validation

{markdown_table(validation, ["row_id", "status", "detail", "valid_for_claim"])}
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> int:
    sources = build_sources()
    audit = build_audit_rows()
    mhref = build_mhref_rows()
    normalization = build_normalization_rows()
    decision = build_decision_rows()
    claims = build_claim_rows()
    refusal = build_refusal_rows()
    next_rows = build_next_rows()

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["audit"], audit)
    write_csv(OUTPUTS["mhref_first"], mhref)
    write_csv(OUTPUTS["normalization"], normalization)
    write_csv(OUTPUTS["decision"], decision)
    write_csv(OUTPUTS["claims"], claims)
    write_csv(OUTPUTS["refusal"], refusal)
    write_csv(OUTPUTS["next"], next_rows)

    copies = copy_branch_outputs()
    write_csv(OUTPUTS["copies"], copies)

    validation = build_validation(sources, audit, mhref, normalization, decision, claims, refusal, next_rows, copies)
    write_csv(OUTPUTS["validation"], validation)

    write_doc(sources, audit, mhref, normalization, decision, claims, refusal, next_rows, copies, validation)

    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        print(f"2339 validation failed: {len(failed)} failed rows")
        for row in failed:
            print(f"{row['row_id']}: {row['detail']}")
        return 1

    print(f"2339 checkpoint generated: {DOC}")
    print(f"Validation: {OUTPUTS['validation']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
