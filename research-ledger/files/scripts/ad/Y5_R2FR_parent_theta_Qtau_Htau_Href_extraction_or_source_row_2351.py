from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_PARENT_THETA_QTAU_HTAU_HREF_RECONCILIATION_2351"

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
FORMALIZATION = PROJECT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICRO_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"

DOC = ROOT / "2351-Y5-R2FR-parent-theta-Qtau-Htau-Href-extraction-or-source-row.md"

PATHS = {
    "2350_doc": ROOT / "2350-Y5-R2FR-boundary-improvement-current-zero-or-P4-boundary-row.md",
    "2350_next": OUT / "P8_Y5_PARENT_QLOC_2350_NEXT_TARGET.csv",
    "2350_stack": OUT / "P8_Y5_PARENT_QLOC_2350_PRIVATE_BRANCH_RESIDUAL_STACK.csv",
    "2350_p4": OUT / "P8_Y5_PARENT_QLOC_2350_P4_BOUNDARY_COMPONENT_ROW.csv",
    "2350_claims": OUT / "P8_Y5_PARENT_QLOC_2350_CLAIM_GATES.csv",
    "2340_doc": ROOT / "2340-Y5-R2FR-parent-theta-Qtau-Htau-Href-extraction-or-source-row.md",
    "2340_spine": OUT / "P8_Y5_PARENT_QLOC_2340_PARENT_CHARGE_EXTRACTION_SPINE.csv",
    "2340_sector": OUT / "P8_Y5_PARENT_QLOC_2340_SECTOR_EXTRACTION_MATRIX.csv",
    "2340_htau_href": OUT / "P8_Y5_PARENT_QLOC_2340_HTAU_HREF_SOURCE_ROW.csv",
    "2340_eh_split": OUT / "P8_Y5_PARENT_QLOC_2340_EH_ANCHOR_RESIDUAL_SPLIT.csv",
    "2340_next": OUT / "P8_Y5_PARENT_QLOC_2340_NEXT_TARGET.csv",
    "2341_doc": ROOT / "2341-Y5-R2FR-EH-anchor-residual-charge-zero-or-coefficient-row.md",
    "2341_zero": OUT / "P8_Y5_PARENT_QLOC_2341_RESIDUAL_CHARGE_ZERO_AUDIT.csv",
    "2341_components": OUT / "P8_Y5_PARENT_QLOC_2341_DELTA_QRES_COMPONENT_MAP.csv",
    "2341_coefficients": OUT / "P8_Y5_PARENT_QLOC_2341_DELTA_QRES_COEFFICIENT_ROWS.csv",
    "2341_observables": OUT / "P8_Y5_PARENT_QLOC_2341_DELTA_QRES_OBSERVABLE_MAP.csv",
    "2341_next": OUT / "P8_Y5_PARENT_QLOC_2341_NEXT_TARGET.csv",
    "1006_denominator": OUT / "P8_Y5_R10_1006_MHREF_DENOMINATOR_THEOREM_AUDIT.csv",
    "1007_integrability": OUT / "P8_Y5_R10_1007_HTAU_INTEGRABILITY_THEOREM_AUDIT.csv",
    "1008_variation": OUT / "P8_Y5_R10_1008_PARENT_VARIATION_AUDIT.csv",
    "1017_reference": OUT / "P8_Y5_R10_1017_REFERENCE_LOCK_LAW.csv",
    "1017_theorem": OUT / "P8_Y5_R10_1017_THEOREM_ATTEMPT.csv",
}

SOURCES = [
    ("SRC2351_00_2350_doc", "2350_doc", ["BIC2350_3_parent_charge_dependency", "NEXT2350_0"], "2350 makes boundary/improvement scoring depend on theta/Q_tau/H_tau/H_ref"),
    ("SRC2351_01_2350_stack", "2350_stack", ["PRS2350_2_charge_denominator", "M_H_ref"], "private branch residual stack exposes the charge denominator"),
    ("SRC2351_02_2350_p4", "2350_p4", ["P4B2350_0_boundary_total", "MISSING_M_H_REF"], "absolute boundary row awaiting parent charge normalization"),
    ("SRC2351_03_2350_claims", "2350_claims", ["CG2350_2_parent_charge", "false"], "2350 claim gate blocks local GR/Newton"),
    ("SRC2351_04_2340_doc", "2340_doc", ["PCS2340_0_parent_split", "COUPLING_KEY_CONFIRMED_AS_STRUCTURAL"], "2340 already built the parent charge spine and identified coupling/source-measure as structural"),
    ("SRC2351_05_2340_spine", "2340_spine", ["PCS2340_3_charge_decomposition", "EH_ANCHOR_PLUS_RESIDUAL_VECTOR"], "machine-readable parent charge extraction spine"),
    ("SRC2351_06_2340_sector", "2340_sector", ["SEM2340_3_GK_extra", "SEM2340_6_total"], "sector map for non-EH charge leakage"),
    ("SRC2351_07_2340_htau_href", "2340_htau_href", ["HHS2340_0_source_row", "MISSING_THETA_SOURCE"], "H_tau/H_ref/M_H_ref first source row remains unfilled"),
    ("SRC2351_08_2340_eh_split", "2340_eh_split", ["ERS2340_0_EH_anchor_law", "ERS2340_3_Newton_bridge"], "EH anchor plus residual and Newton bridge split"),
    ("SRC2351_09_2340_next", "2340_next", ["NEXT2340_1", "source-charge-equals-measured-GM"], "2340 already selected source-measure bridge as parallel target"),
    ("SRC2351_10_2341_doc", "2341_doc", ["RCZ2341_6_verdict", "NEXT2341_0"], "2341 attempted residual charge zero and selected source-measure next"),
    ("SRC2351_11_2341_zero", "2341_zero", ["RCZ2341_6_verdict", "ZERO_THEOREM_NOT_DERIVED"], "residual charge zero was not derived"),
    ("SRC2351_12_2341_components", "2341_components", ["DQC2341_2_projector", "Delta_Q_projector"], "component map for Delta_Q_res fallback"),
    ("SRC2351_13_2341_coefficients", "2341_coefficients", ["CQR2341_7_abs_sum", "MISSING_COMPONENT_INPUTS"], "coefficient rows remain missing and nonclaim"),
    ("SRC2351_14_2341_observables", "2341_observables", ["QOM2341_2_source_GM", "measured GM"], "observable map ties residual charge to measured source normalization"),
    ("SRC2351_15_2341_next", "2341_next", ["NEXT2341_0", "source-charge-equals-measured-GM"], "current handoff points at source-charge equals measured GM"),
    ("SRC2351_16_1006_denominator", "1006_denominator", ["MHA1006_6_theorem_verdict", "fail_current_claim"], "older M_H_ref denominator theorem audit remains failed"),
    ("SRC2351_17_1007_integrability", "1007_integrability", ["HTA1007_6_integrability_verdict", "fail_current_claim"], "older H_tau integrability audit remains failed"),
    ("SRC2351_18_1008_variation", "1008_variation", ["PVA1008_6_verdict", "fail_current_claim"], "older parent variation audit remains failed"),
    ("SRC2351_19_1017_reference", "1017_reference", ["HRL1017_5_MHref_denominator", "fail_current_claim"], "reference lock/denominator law remains failed"),
    ("SRC2351_20_1017_theorem", "1017_theorem", ["HPT1017_5_verdict", "fail_current_claim"], "reference theorem attempt remains failed"),
]

OUTPUTS = {
    "sources": OUT / "P8_Y5_PARENT_QLOC_2351_SOURCE_REGISTER.csv",
    "audit": OUT / "P8_Y5_PARENT_QLOC_2351_PARENT_CHARGE_RECONCILIATION_AUDIT.csv",
    "htau_href": OUT / "P8_Y5_PARENT_QLOC_2351_HTAU_HREF_SOURCE_ROW_STATUS.csv",
    "residual_handoff": OUT / "P8_Y5_PARENT_QLOC_2351_RESIDUAL_CHARGE_HANDOFF.csv",
    "source_measure": OUT / "P8_Y5_PARENT_QLOC_2351_SOURCE_MEASURE_BRIDGE_TARGET.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2351_DECISION_LEDGER.csv",
    "claims": OUT / "P8_Y5_PARENT_QLOC_2351_CLAIM_GATES.csv",
    "refusal": OUT / "P8_Y5_PARENT_QLOC_2351_REFUSAL_RUNNER.csv",
    "next": OUT / "P8_Y5_PARENT_QLOC_2351_NEXT_TARGET.csv",
    "copies": OUT / "P8_Y5_PARENT_QLOC_2351_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2351_VALIDATION.csv",
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def has_needles(path: Path, needles: list[str]) -> bool:
    text = read_text(path)
    return path.exists() and all(needle in text for needle in needles)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key not in headers:
                headers.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8", errors="replace") as handle:
        return list(csv.DictReader(handle))


def b(value: bool) -> str:
    return "true" if value else "false"


def source_register_rows() -> list[dict[str, Any]]:
    rows = []
    for row_id, key, needles, role in SOURCES:
        path = PATHS[key]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "row_id": row_id,
                "file_key": key,
                "source_path": str(path),
                "exists": b(path.exists()),
                "required_needles": ";".join(needles),
                "needles_found": b(has_needles(path, needles)),
                "role": role,
                "claim_status": "source_evidence_only",
                "valid_for_claim": "false",
            }
        )
    return rows


def parent_charge_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "PCR2351_0_target",
            "object": "parent theta/Q_tau/H_tau/H_ref bridge",
            "statement": "After 2350, the local GR/Newton route needs the parent Noether charge stack, not another local residual relabel.",
            "status": "TARGET_RECONCILED_WITH_2340_2341",
            "reason": "2350 says boundary scoring needs M_H_ref; 2340 provides the exact spine; 2341 shows Delta_Q_res zero is not yet derived.",
            "source_rows": "SRC2351_00_2350_doc;SRC2351_04_2340_doc;SRC2351_10_2341_doc",
            "next_action": "select source-charge equals measured GM or selector bound as 2352",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PCR2351_1_boundary_dependency_imported",
            "object": "boundary/improvement denominator dependency",
            "statement": "epsilon_boundary_abs cannot be normalized until M_H_ref := H_tau[S_outer]-H_ref is source-backed, positive and same-frame.",
            "status": "BLOCKED_BY_PARENT_CHARGE_STACK",
            "reason": "2350 P4 boundary row carries MISSING_M_H_REF and forbids orbital-GM backfill.",
            "source_rows": "SRC2351_00_2350_doc;SRC2351_01_2350_stack;SRC2351_02_2350_p4",
            "next_action": "do not score boundary row; extract or bound parent charge stack first",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PCR2351_2_2340_spine_imported",
            "object": "parent action/current/charge spine",
            "statement": "L_parent -> theta_MTS -> J_tau -> Q_tau^MTS -> H_tau is an exact template with sector ownership still unsigned.",
            "status": "EXACT_SPINE_IMPORTED_NOT_SIGNED",
            "reason": "2340 separates EH anchor from matter, boundary/reference, extra, projector and glue sectors without promoting their silence.",
            "source_rows": "SRC2351_04_2340_doc;SRC2351_05_2340_spine;SRC2351_06_2340_sector",
            "next_action": "use 2340 as the canonical parent-charge schema; do not duplicate it as a new proof",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PCR2351_3_Htau_Href_source_row_status",
            "object": "H_tau/H_ref/M_H_ref row",
            "statement": "M_H_ref := H_tau[S_outer]-H_ref is staged but all live numeric/source/certificate inputs remain missing.",
            "status": "FIRST_ROW_READY_VALUES_MISSING",
            "reason": "HHS2340_0 still has MISSING_THETA_SOURCE, MISSING_Q_TAU_SOURCE, MISSING_H_TAU, MISSING_H_REF and MISSING_M_H_REF.",
            "source_rows": "SRC2351_07_2340_htau_href;SRC2351_16_1006_denominator;SRC2351_17_1007_integrability",
            "next_action": "keep H_tau/H_ref as nonclaim source rows until parent current and fixed reference are signed",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PCR2351_4_EH_anchor_residual_split",
            "object": "EH anchor plus residual",
            "statement": "Q_tau^MTS = Q_tau^EH + Delta_Q_res is the clean comparison law; local GR follows only if residual charge and source-measure bridges close.",
            "status": "ANCHOR_LAW_EXACT_NONCLAIM",
            "reason": "EH is a reference anchor, not a proof that every MTS sector has zero charge response.",
            "source_rows": "SRC2351_08_2340_eh_split;SRC2351_11_2341_zero",
            "next_action": "retain Delta_Q_res coefficient rows and source-measure equality as live gates",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PCR2351_5_2341_residual_handoff",
            "object": "Delta_Q_res zero attempt",
            "statement": "Delta_Q_res=Delta_H_res=0 was attempted and not derived; coefficient rows are now the honest fallback.",
            "status": "ZERO_THEOREM_NOT_DERIVED_RETAIN_COEFFICIENT_ROWS",
            "reason": "Boundary/reference, GK/q_loc, projector/source-measure and coupling/source-measure obstructions are independent.",
            "source_rows": "SRC2351_11_2341_zero;SRC2351_12_2341_components;SRC2351_13_2341_coefficients",
            "next_action": "carry absolute residual charge envelope forward; no sign cancellation",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PCR2351_6_coupling_source_measure_priority",
            "object": "Hamiltonian charge equals measured source charge",
            "statement": "The coupling problem is the live bottleneck: a conserved Hamiltonian charge is not yet the measured GM/source charge.",
            "status": "STRUCTURAL_KEY_NOT_OPTIONAL",
            "reason": "2340 and 2341 both select source-charge equals measured GM; 2350 makes M_H_ref normalization depend on the same bridge.",
            "source_rows": "SRC2351_09_2340_next;SRC2351_14_2341_observables;SRC2351_15_2341_next",
            "next_action": "derive or bound source-charge equality without importing orbital GM",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PCR2351_7_verdict",
            "object": "2351 checkpoint verdict",
            "statement": "The parent-charge route is now consolidated rather than solved: 2351 imports 2340/2341, refuses local-GR promotion, and selects 2352 source-measure bridge.",
            "status": "RECONCILIATION_COMPLETE_DERIVATION_STILL_OPEN",
            "reason": "Every public local-GR/Newton gate still needs parent charge extraction, fixed reference, residual charge silence or sourced bounds, and source-measure equality.",
            "source_rows": "PCR2351_0_target;PCR2351_6_coupling_source_measure_priority",
            "next_action": "2352-Y5-R2FR-source-charge-equals-measured-GM-or-selector-bound.md",
            "valid_for_claim": "false",
        },
    ]


def htau_href_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "HHS2351_0_parent_current_chain",
            "quantity": "theta_MTS and Q_tau^MTS",
            "required_for": "H_tau extraction and local GR/Newton normalization",
            "current_status": "TEMPLATE_EXISTS_OWNER_CHAIN_UNSIGNED",
            "missing_inputs": "explicit L_parent sector terms;theta_i;J_tau;Q_tau sector ownership;constraint term C_tau",
            "source_path": str(PATHS["2340_spine"]),
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "HHS2351_1_Htau_integrability",
            "quantity": "delta H_tau[S]=integral_S(delta Q_tau^MTS-i_tau theta_MTS)",
            "required_for": "finite Hamiltonian charge independent of path in field space",
            "current_status": "INTEGRABILITY_BLOCKED",
            "missing_inputs": "closed field-space one-form;boundary/corner silence;sector variation certificates",
            "source_path": str(PATHS["1007_integrability"]),
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "HHS2351_2_fixed_reference",
            "quantity": "H_ref",
            "required_for": "no cancellation knob and no readout-fit reference",
            "current_status": "MISSING_FIXED_REFERENCE_SOURCE",
            "missing_inputs": "reference class;counterterm convention;fixed-before-readout certificate;Delta_ref bound",
            "source_path": str(PATHS["1017_reference"]),
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "HHS2351_3_MHref",
            "quantity": "M_H_ref := H_tau[S_outer]-H_ref",
            "required_for": "denominator for boundary, residual charge, PPN and source-measure rows",
            "current_status": "MISSING_H_TAU_H_REF_MHREF",
            "missing_inputs": "H_tau numeric/source;H_ref numeric/source;positivity;same-frame certificate;non-orbital derivation",
            "source_path": str(PATHS["2340_htau_href"]),
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "HHS2351_4_anti_circularity_guard",
            "quantity": "not_orbital_GM_imported",
            "required_for": "Newton recovery without borrowing Newton",
            "current_status": "GUARD_READY_NONCLAIM",
            "missing_inputs": "derive M_H_ref -> Poisson/Gauss source -> orbital GM before any orbital calibration",
            "source_path": str(PATHS["2350_stack"]),
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "HHS2351_5_status",
            "quantity": "H_tau/H_ref source row",
            "required_for": "claim-grade local-GR/Newton branch",
            "current_status": "NONCLAIM_SOURCE_ROW_ONLY",
            "missing_inputs": "all source, coefficient and certificate fields listed above",
            "source_path": str(PATHS["2340_htau_href"]),
            "score_ready": "false",
            "valid_for_claim": "false",
        },
    ]


def residual_handoff_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "RCH2351_0_total",
            "residual": "epsilon_Qres_abs",
            "formula": "sum_i abs(Delta_Q_i)/M_H_ref",
            "status": "ABSOLUTE_ENVELOPE_STAGED_NOT_NUMERIC",
            "blocking_inputs": "M_H_ref;Delta_Q_i coefficients;source paths;projection thresholds",
            "source_rows": "CQR2341_7_abs_sum;HHS2351_3_MHref",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "RCH2351_1_boundary_ref",
            "residual": "Delta_Q_boundary_ref",
            "formula": "Q_boundary + delta B_ref + C_ref",
            "status": "ZERO_NOT_DERIVED_COEFFICIENT_MISSING",
            "blocking_inputs": "fixed H_ref;B_zero_flux;Delta_symp;corner/no-flux theorem;M_H_ref",
            "source_rows": "DQC2341_0_boundary_ref;P4B2350_1_Bzero_flux;P4B2350_2_Delta_symp",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "RCH2351_2_GK_extra",
            "residual": "Delta_Q_GK_extra",
            "formula": "Q_extra + C_extra from Gamma/Khat/q_loc and retained non-EH sectors",
            "status": "ZERO_NOT_DERIVED_COEFFICIENT_MISSING",
            "blocking_inputs": "q_loc zero or profile bound;Khat adoption;non-EH sector variation;M_H_ref",
            "source_rows": "DQC2341_1_GK_extra;CQR2341_1_GK_extra",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "RCH2351_3_projector",
            "residual": "Delta_Q_projector",
            "formula": "C_projector + [d,Pi_M]J_H + delta Pi_M terms",
            "status": "ZERO_NOT_DERIVED_COEFFICIENT_MISSING",
            "blocking_inputs": "Pi_M parent origin;R_eq;I_commutator;worldtube selector;M_H_ref",
            "source_rows": "DQC2341_2_projector;P4B2350_3_Req;P4B2350_4_Icommutator",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "RCH2351_4_source_glue_coupling",
            "residual": "Delta_Q_source_glue + Delta_Q_coupling_G",
            "formula": "Hamiltonian charge/source-current mismatch plus coupling normalization drift",
            "status": "MAIN_LIVE_BOTTLENECK",
            "blocking_inputs": "source Ward identity;Hilbert/topological equality;Poisson/Gauss bridge;selector bound",
            "source_rows": "QOM2341_2_source_GM;NEXT2341_0",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "RCH2351_5_readout_clock",
            "residual": "Delta_Q_readout_PPN + Delta_Q_EM_clock",
            "formula": "PPN/clock residual projection from charge mismatch and coupling tails",
            "status": "OBSERVABLE_MAP_STAGED_NOT_PROJECTED",
            "blocking_inputs": "PPN coefficients;clock/WEP map;R10/R11 bounds;valid source charge denominator",
            "source_rows": "QOM2341_1_PPN;QOM2341_3_R10_R11",
            "valid_for_claim": "false",
        },
    ]


def source_measure_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "SMB2351_0_target",
            "target": "source-charge equals measured GM",
            "needed_law": "M_H_ref -> M_source -> Poisson/Gauss source -> orbital GM",
            "status": "SELECTED_NEXT_DERIVATION_TARGET",
            "why": "This is where GR/Newton recovery becomes physical rather than merely formal.",
            "anti_shortcut": "do not import observed orbital GM to define M_H_ref",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SMB2351_1_Hilbert_topological_equality",
            "target": "Pi_M J_H = J_M_top + dB_zero",
            "needed_law": "R_eq_integral=0 or source-backed absolute bound",
            "status": "OPEN_PARALLEL_GATE",
            "why": "A closed charge can be the wrong physical source charge if the projection equality fails.",
            "anti_shortcut": "topological conservation alone is not source-measure equality",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SMB2351_2_projector_commutator",
            "target": "[d,Pi_M]J_H=0",
            "needed_law": "I_commutator=0 or source-backed absolute bound",
            "status": "OPEN_PARALLEL_GATE",
            "why": "Domain/projector variation can create apparent source charge drift.",
            "anti_shortcut": "do not assume Pi_M commutes with exterior derivative or readout selection",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SMB2351_3_selector_worldtube",
            "target": "source support and worldtube selector",
            "needed_law": "Delta_worldtube_domain=0 or bounded below local thresholds",
            "status": "OPEN_SELECTOR_GATE",
            "why": "Measured mass is a source/readout statement, not just an asymptotic charge label.",
            "anti_shortcut": "do not hide radius/readout dependence in the source definition",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SMB2351_4_empirical_handoff",
            "target": "PPN/orbital/R10/R11/clocks",
            "needed_law": "once source-charge bridge is derived or bounded, project residual vector into local tests",
            "status": "DEFERRED_UNTIL_PARENT_GATE",
            "why": "Testing too early measures placeholder plumbing rather than the theory branch.",
            "anti_shortcut": "no local-GR pass until source-measure and residual charge gates are both closed or bounded",
            "valid_for_claim": "false",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2351_0_no_public_claim",
            "decision": "do not claim local GR/Newton reduction",
            "reason": "parent charge, fixed reference, residual charge and source-measure gates are open",
            "effect": "all claim gates remain false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2351_1_reuse_2340_spine",
            "decision": "treat 2340 as the canonical parent-charge schema",
            "reason": "2340 already did the parent theta/Q_tau/H_tau/H_ref extraction template",
            "effect": "2351 reconciles rather than duplicates",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2351_2_reuse_2341_coefficients",
            "decision": "carry 2341 coefficient rows forward",
            "reason": "Delta_Q_res zero failed honestly and the fallback rows are the right nonclaim scaffold",
            "effect": "no sign-cancellation, no hidden residual deletion",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2351_3_select_2352",
            "decision": "next target is source-charge equals measured GM or selector bound",
            "reason": "this is the coupling bridge that makes GR/Newton recovery physical",
            "effect": "derive the source-measure bridge before more empirical scoring",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2351_4_parallel_fallback",
            "decision": "keep Hilbert/projector and coefficient acquisition as parallel nonclaim fallbacks",
            "reason": "if source-measure proof fails, the residual must become sourced rows rather than a claim",
            "effect": "2352b/2352c are named but secondary",
            "valid_for_claim": "false",
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2351_0_spine_exists",
            "gate": "parent charge spine exists",
            "passes_private_nonclaim": "true",
            "passes_public_claim": "false",
            "why": "the formal template exists but sector ownership and source certificates are unsigned",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2351_1_theta_Qtau_extracted",
            "gate": "theta_MTS and Q_tau^MTS extracted from parent action",
            "passes_private_nonclaim": "false",
            "passes_public_claim": "false",
            "why": "explicit parent sector variations and charge ownership are missing",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2351_2_Htau_integrable",
            "gate": "H_tau integrability",
            "passes_private_nonclaim": "false",
            "passes_public_claim": "false",
            "why": "field-space closedness and boundary/corner certificates are missing",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2351_3_Href_fixed",
            "gate": "fixed reference H_ref",
            "passes_private_nonclaim": "false",
            "passes_public_claim": "false",
            "why": "reference class and no-cancellation certificate are missing",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2351_4_MHref_valid",
            "gate": "positive same-frame M_H_ref",
            "passes_private_nonclaim": "false",
            "passes_public_claim": "false",
            "why": "H_tau and H_ref are not source-backed and orbital GM backfill is forbidden",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2351_5_DeltaQres_zero_or_bound",
            "gate": "Delta_Q_res zero or absolute bound",
            "passes_private_nonclaim": "false",
            "passes_public_claim": "false",
            "why": "2341 failed the zero theorem and coefficient rows are missing",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2351_6_source_measure_bridge",
            "gate": "Hamiltonian charge equals measured source charge",
            "passes_private_nonclaim": "false",
            "passes_public_claim": "false",
            "why": "Poisson/Gauss/source-selector bridge is not derived",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2351_7_local_GR_Newton",
            "gate": "local GR/Newton recovered",
            "passes_private_nonclaim": "false",
            "passes_public_claim": "false",
            "why": "requires CG2351_1 through CG2351_6",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2351_8_empirical_score_ready",
            "gate": "PPN/R10/orbital score-ready",
            "passes_private_nonclaim": "false",
            "passes_public_claim": "false",
            "why": "no valid parent denominator or residual projection coefficients",
            "valid_for_claim": "false",
        },
    ]


def refusal_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2351_0_EH_total_shortcut",
            "shortcut": "set Q_tau^MTS=Q_tau^EH",
            "allowed": "false",
            "reason": "EH is an anchor; non-EH charge residuals must be zero, topological, fixed, or bounded",
            "source_rows": "PCS2340_3_charge_decomposition;RCZ2341_6_verdict",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2351_1_orbital_GM_backfill",
            "shortcut": "fill M_H_ref from observed orbital GM",
            "allowed": "false",
            "reason": "this borrows Newton/source normalization before deriving it",
            "source_rows": "PRS2350_3_anti_circularity;HHS2351_4_anti_circularity_guard",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2351_2_residual_sign_cancellation",
            "shortcut": "let Delta_Q_i signs cancel",
            "allowed": "false",
            "reason": "independent missing sectors require absolute-sum residuals unless a parent identity proves exact cancellation",
            "source_rows": "CQR2341_7_abs_sum;HHS2340_3_charge_residual_row",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2351_3_boundary_as_closed",
            "shortcut": "treat boundary/improvement P4 row as a pass",
            "allowed": "false",
            "reason": "boundary row lacks B_zero_flux, Delta_symp, R_eq, I_commutator, worldtube, corner and M_H_ref inputs",
            "source_rows": "P4B2350_0_boundary_total",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2351_4_source_measure_by_name",
            "shortcut": "call Hamiltonian charge the source charge by definition",
            "allowed": "false",
            "reason": "measured GM requires a source/current/selector bridge, not just conserved-charge vocabulary",
            "source_rows": "QOM2341_2_source_GM;SMB2351_0_target",
            "valid_for_claim": "false",
        },
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2351_0",
            "next_target": "2352-Y5-R2FR-source-charge-equals-measured-GM-or-selector-bound.md",
            "why": "the main live bottleneck is proving the parent Hamiltonian charge is the measured source charge without orbital-GM backfill",
            "claim_status": "private_derivation_next_step",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2351_1",
            "next_target": "2352b-Y5-R2FR-Hilbert-source-charge-equality-or-Req-Icommutator-bound.md",
            "why": "parallel exact route: close Pi_M J_H = J_M_top + dB_zero and [d,Pi_M]J_H or retain R_eq/I_commutator rows",
            "claim_status": "parallel_nonclaim",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2351_2",
            "next_target": "2352c-Y5-R2FR-DeltaQres-coefficient-source-row-runner.md",
            "why": "fallback route: source coefficient rows for the residual charge vector if theorem-zero continues to fail",
            "claim_status": "fallback_nonclaim",
            "valid_for_claim": "false",
        },
    ]


def copy_rows() -> list[dict[str, Any]]:
    copies = [
        (
            "COPY2351_0_beta_reconciliation",
            OUTPUTS["audit"],
            BETA_DOCS / "PARENT_CHARGE_RECONCILIATION_AUDIT_2351_NONCLAIM.csv",
            "beta-source derivation notes",
        ),
        (
            "COPY2351_1_microscope_htau",
            OUTPUTS["htau_href"],
            MICRO_RESIDUALS / "HTAU_HREF_SOURCE_ROW_STATUS_2351_NONCLAIM.csv",
            "local residual/PPN gate inputs",
        ),
        (
            "COPY2351_2_rab_decision",
            OUTPUTS["decision"],
            RAB_QUEUE / "JR2351_PARENT_CHARGE_RECONCILIATION_DECISION_LEDGER_NONCLAIM.csv",
            "acquisition queue decision handoff",
        ),
    ]
    rows = []
    for row_id, src, dst, purpose in copies:
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dst)
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "row_id": row_id,
                "source_path": str(src),
                "copy_path": str(dst),
                "exists": b(dst.exists()),
                "purpose": purpose,
                "valid_for_claim": "false",
            }
        )
    return rows


def table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    header = "| " + " | ".join(columns) + " |\n"
    separator = "| " + " | ".join("---" for _ in columns) + " |\n"
    body = ""
    for row in rows:
        body += "| " + " | ".join(str(row.get(column, "")).replace("|", "\\|") for column in columns) + " |\n"
    return header + separator + body


def formalization_hits() -> list[Path]:
    if not FORMALIZATION.exists():
        return []
    return [path for path in FORMALIZATION.rglob("*2351*") if path.is_file()]


def make_validation(sources: list[dict[str, Any]], copies: list[dict[str, Any]]) -> list[dict[str, Any]]:
    produced = [path for path in OUTPUTS.values() if path.name != OUTPUTS["validation"].name]
    claim_rows = read_csv(OUTPUTS["claims"])
    htau_rows = read_csv(OUTPUTS["htau_href"])
    residual_rows = read_csv(OUTPUTS["residual_handoff"])
    next_text = read_text(OUTPUTS["next"])
    audit_text = read_text(OUTPUTS["audit"])
    validation = [
        {
            "row_id": "VAL2351_00_sources_exist",
            "status": "PASS" if all(row["exists"] == "true" for row in sources) else "FAIL",
            "detail": "all cited 2350/2340/2341/1006/1007/1008/1017 source paths exist",
            "valid_for_claim": "false",
        },
        {
            "row_id": "VAL2351_01_needles_found",
            "status": "PASS" if all(row["needles_found"] == "true" for row in sources) else "FAIL",
            "detail": "required source strings found in every cited source",
            "valid_for_claim": "false",
        },
        {
            "row_id": "VAL2351_02_outputs_written",
            "status": "PASS" if all(path.exists() and path.stat().st_size > 0 for path in produced) else "FAIL",
            "detail": "all 2351 CSV outputs written before validation",
            "valid_for_claim": "false",
        },
        {
            "row_id": "VAL2351_03_2340_spine_imported",
            "status": "PASS" if "PCR2351_2_2340_spine_imported" in audit_text else "FAIL",
            "detail": "2351 reuses the 2340 parent-charge spine instead of duplicating it",
            "valid_for_claim": "false",
        },
        {
            "row_id": "VAL2351_04_2341_handoff_imported",
            "status": "PASS" if "PCR2351_5_2341_residual_handoff" in audit_text else "FAIL",
            "detail": "2351 imports the 2341 residual-charge zero failure and coefficient-row fallback",
            "valid_for_claim": "false",
        },
        {
            "row_id": "VAL2351_05_htau_href_nonclaim",
            "status": "PASS" if htau_rows and all(row.get("valid_for_claim") == "false" and row.get("score_ready") == "false" for row in htau_rows) else "FAIL",
            "detail": "H_tau/H_ref/M_H_ref rows remain nonclaim and non-score-ready",
            "valid_for_claim": "false",
        },
        {
            "row_id": "VAL2351_06_residual_handoff_nonclaim",
            "status": "PASS" if residual_rows and all(row.get("valid_for_claim") == "false" for row in residual_rows) else "FAIL",
            "detail": "residual charge handoff keeps every component nonclaim",
            "valid_for_claim": "false",
        },
        {
            "row_id": "VAL2351_07_no_valid_claim_rows",
            "status": "PASS" if claim_rows and all(row.get("valid_for_claim") == "false" and row.get("passes_public_claim") == "false" for row in claim_rows) else "FAIL",
            "detail": "all public claim gates are blocked",
            "valid_for_claim": "false",
        },
        {
            "row_id": "VAL2351_08_next_target_selected",
            "status": "PASS" if "2352-Y5-R2FR-source-charge-equals-measured-GM-or-selector-bound.md" in next_text else "FAIL",
            "detail": "source-charge equals measured GM selected as next derivation target",
            "valid_for_claim": "false",
        },
        {
            "row_id": "VAL2351_09_branch_copies",
            "status": "PASS" if copies and all(row["exists"] == "true" for row in copies) else "FAIL",
            "detail": "branch copies written to beta-source, microscope residuals and RAB acquisition queue",
            "valid_for_claim": "false",
        },
        {
            "row_id": "VAL2351_10_formalization_untouched",
            "status": "PASS" if not formalization_hits() else "FAIL",
            "detail": "no 2351 files found under formalization-workbench",
            "valid_for_claim": "false",
        },
        {
            "row_id": "VAL2351_OVERALL",
            "status": "PENDING",
            "detail": "filled after validation rows are computed",
            "valid_for_claim": "false",
        },
    ]
    overall = "PASS" if all(row["status"] == "PASS" for row in validation[:-1]) else "FAIL"
    validation[-1]["status"] = overall
    validation[-1]["detail"] = (
        "2351 reconciles 2350 boundary dependency with 2340 parent-charge spine and 2341 residual-charge handoff; "
        "local GR/Newton remains blocked and 2352 source-measure bridge is selected next."
    )
    return validation


def write_doc(
    sources: list[dict[str, Any]],
    audit: list[dict[str, Any]],
    htau_href: list[dict[str, Any]],
    residual: list[dict[str, Any]],
    source_measure: list[dict[str, Any]],
    decision: list[dict[str, Any]],
    claims: list[dict[str, Any]],
    refusal: list[dict[str, Any]],
    next_targets: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    now = datetime.now(timezone.utc).isoformat()
    content = f"""# 2351 — Y5 R2FR Parent theta/Q_tau/H_tau/H_ref Extraction Or Source Row

Generated: `{now}`

## Summary

2351 is a reconciliation checkpoint, not a new local-GR claim. 2350 made the boundary/improvement row depend on
`theta_MTS`, `Q_tau^MTS`, `H_tau`, fixed `H_ref`, and positive same-frame `M_H_ref`. 2340 already built the exact
parent-charge spine, and 2341 already tried and failed to derive `Delta_Q_res = Delta_H_res = 0`. Therefore the correct
move is not to duplicate those branches; it is to lock the handoff and attack the coupling/source-measure bridge next.

Current verdict: **local GR/Newton is still blocked**, but the trench is narrower. The live bottleneck is proving that
the parent Hamiltonian charge is the measured source charge without importing orbital `GM`.

## Output Files

- `{OUTPUTS["sources"]}`
- `{OUTPUTS["audit"]}`
- `{OUTPUTS["htau_href"]}`
- `{OUTPUTS["residual_handoff"]}`
- `{OUTPUTS["source_measure"]}`
- `{OUTPUTS["decision"]}`
- `{OUTPUTS["claims"]}`
- `{OUTPUTS["refusal"]}`
- `{OUTPUTS["next"]}`
- `{OUTPUTS["copies"]}`
- `{OUTPUTS["validation"]}`

## Source Register

{table(sources, ["row_id", "file_key", "exists", "needles_found", "role"])}

## Parent-Charge Reconciliation Audit

{table(audit, ["row_id", "object", "status", "reason", "next_action", "valid_for_claim"])}

## H_tau/H_ref Source Row Status

{table(htau_href, ["row_id", "quantity", "current_status", "missing_inputs", "score_ready", "valid_for_claim"])}

## Residual Charge Handoff

{table(residual, ["row_id", "residual", "status", "blocking_inputs", "valid_for_claim"])}

## Source-Measure Bridge Target

{table(source_measure, ["row_id", "target", "status", "needed_law", "anti_shortcut", "valid_for_claim"])}

## Decision Ledger

{table(decision, ["row_id", "decision", "reason", "effect", "valid_for_claim"])}

## Claim Gates

{table(claims, ["row_id", "gate", "passes_private_nonclaim", "passes_public_claim", "why", "valid_for_claim"])}

## Refusal Runner

{table(refusal, ["row_id", "shortcut", "allowed", "reason", "source_rows", "valid_for_claim"])}

## Next Targets

{table(next_targets, ["row_id", "next_target", "why", "claim_status", "valid_for_claim"])}

## Validation

{table(validation, ["row_id", "status", "detail", "valid_for_claim"])}

## Working Read

This checkpoint is actually good news in a boring-but-serious way: we are no longer vaguely saying “connect to GR”.
The route is now:

1. keep the EH charge as the comparison anchor;
2. prove or bound the non-EH residual charge vector;
3. prove the Hamiltonian charge is the measured source charge;
4. only then push into PPN, orbital, R10/R11 and clock score tests.

The coupling/source-measure step is the throat of the problem. If it closes, the local branch becomes genuinely
dangerous in the good way. If it does not close, the theory must honestly retain sourced residual rows instead of
claiming a GR/Newton reduction.
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_register_rows()
    audit = parent_charge_audit_rows()
    htau_href = htau_href_rows()
    residual = residual_handoff_rows()
    source_measure = source_measure_rows()
    decision = decision_rows()
    claims = claim_gate_rows()
    refusal = refusal_rows()
    next_targets = next_rows()

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["audit"], audit)
    write_csv(OUTPUTS["htau_href"], htau_href)
    write_csv(OUTPUTS["residual_handoff"], residual)
    write_csv(OUTPUTS["source_measure"], source_measure)
    write_csv(OUTPUTS["decision"], decision)
    write_csv(OUTPUTS["claims"], claims)
    write_csv(OUTPUTS["refusal"], refusal)
    write_csv(OUTPUTS["next"], next_targets)
    copies = copy_rows()
    write_csv(OUTPUTS["copies"], copies)
    validation = make_validation(sources, copies)
    write_csv(OUTPUTS["validation"], validation)
    write_doc(sources, audit, htau_href, residual, source_measure, decision, claims, refusal, next_targets, validation)

    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        failed_ids = ", ".join(row["row_id"] for row in failed)
        raise SystemExit(f"2351 validation failed: {failed_ids}")
    print(f"2351 checkpoint written: {DOC}")


if __name__ == "__main__":
    main()
