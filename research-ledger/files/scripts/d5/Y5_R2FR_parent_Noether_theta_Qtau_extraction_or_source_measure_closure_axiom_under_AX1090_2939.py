from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_START_UTC = datetime.now(timezone.utc)

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
PARENT_ACTION = ROOT / "source-intake" / "parent-action"
FORMALIZATION = PROJECT / "formalization-workbench"

CHECKPOINT = "2939"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
RUN_UTC = SCRIPT_START_UTC.isoformat()

DOC = ROOT / "2939-Y5-R2FR-parent-Noether-theta-Qtau-extraction-or-source-measure-closure-axiom-under-AX1090.md"

SRC_2938_DOC = ROOT / "2938-Y5-R2FR-Htau-worldtube-source-measure-ellJ-reference-lock-or-Qbar-tau-first-value-under-AX1090.md"
SRC_2938_THEOREM = RESIDUALS / "P8_Y5_R2FR_2938_HTAU_WORLDTUBE_SOURCE_MEASURE_THEOREM_ATTEMPT.csv"
SRC_2938_IDENTITY = RESIDUALS / "P8_Y5_R2FR_2938_SOURCE_MEASURE_RESIDUAL_IDENTITY.csv"
SRC_2938_OBSTRUCTIONS = RESIDUALS / "P8_Y5_R2FR_2938_SOURCE_MEASURE_GLUE_OBSTRUCTION_LEDGER.csv"
SRC_2938_NEXT = RESIDUALS / "P8_Y5_R2FR_2938_NEXT_TARGET.csv"
SRC_2938_VALIDATION = RESIDUALS / "P8_Y5_BRR545_2938_VALIDATION.csv"

SRC_1008_DOC = ROOT / "1008-Y5-R10-parent-theta-Qtau-extraction-or-charge-decomposition-runner.md"
SRC_1009_DOC = ROOT / "1009-Y5-R10-parent-current-chain-action-contract-or-sector-variation-runner.md"
SRC_2923_CHECKLIST = RESIDUALS / "P8_Y5_R2FR_2923_HCORE_QTAU_COEFFICIENT_CHECKLIST.csv"
SRC_2668_PROOF = RESIDUALS / "P8_Y5_R10_LX_THETA_OMEGA_OWNER_2668_OWNER_PROOF_AUDIT.csv"
SRC_2668_GATE = RESIDUALS / "P8_Y5_R10_LX_THETA_OMEGA_OWNER_2668_OWNER_GATE.csv"
SRC_2856 = RESIDUALS / "P8_Y5_R2FR_2856_NOETHER_DERIVATION_ATTEMPT.csv"
SRC_2806 = RESIDUALS / "P8_Y5_R2FR_2806_PARENT_NOETHER_SEARCH_LEDGER.csv"
SRC_2770 = RESIDUALS / "P8_Y5_R2FR_2770_NOETHER_SOURCE_OWNER_AUDIT.csv"
SRC_2699 = RESIDUALS / "P8_Y5_R2FR_2699_NOETHER_RESIDUAL_DECOMPOSITION.csv"
SRC_2615 = RESIDUALS / "P8_Y5_TOTAL_HILBERT_SOURCE_GATE_2615_NOETHER_EXCHANGE_COLLAPSE_THEOREM.csv"
SRC_2339 = RESIDUALS / "P8_Y5_PARENT_QLOC_2339_THETA_QTAU_FIXED_REFERENCE_AUDIT.csv"
SRC_2429_GATE = RESIDUALS / "P8_Y5_PARENT_QLOC_2429_THETAQ_OWNER_GATE.csv"
SRC_2429_TEMPLATE = RESIDUALS / "P8_Y5_PARENT_QLOC_2429_THETAQ_PQ_TEMPLATE_CONTRACT.csv"
SRC_2462 = RESIDUALS / "P8_Y5_PARENT_QLOC_2462_THETA_QTAU_PROMOTION_VERDICT.csv"
SRC_2021_THEOREM = RESIDUALS / "P8_Y5_PARENT_QLOC_2021_QTAU_SECTOR_OWNER_THEOREM.csv"
SRC_2021_LEDGER = RESIDUALS / "P8_Y5_PARENT_QLOC_2021_QTAU_SECTOR_LEDGER.csv"
SRC_1733_AUDIT = RESIDUALS / "P8_Y5_PARENT_QLOC_1733_THETA_QTAU_CURRENT_OWNER_AUDIT.csv"
SRC_1733_COMPONENTS = RESIDUALS / "P8_Y5_PARENT_QLOC_1733_THETA_QTAU_COMPONENT_ROWS.csv"
SRC_993_LEDGER = RESIDUALS / "P8_Y5_R10_993_QTAU_DECOMPOSITION_LEDGER.csv"
SRC_771_AUDIT = RESIDUALS / "P8_Y5_R10_771_THETA_QTAU_CURRENT_OWNER_AUDIT.csv"
SRC_771_TEST = RESIDUALS / "P8_Y5_R10_771_NOETHER_EXTRACTION_TEST.csv"
SRC_824_AUDIT = RESIDUALS / "P8_Y5_R10_824_NOETHER_VARIATION_AUDIT.csv"
SRC_PARENT_NOETHER_CHAIN = RESIDUALS / "P8_PARENT_NOETHER_CLOSURE_DERIVATION_CHAIN.csv"
SRC_PARENT_NOETHER_THEOREM = RESIDUALS / "P8_PARENT_NOETHER_CLOSURE_THEOREM.csv"
SRC_PARENT_NOETHER_CTERM = RESIDUALS / "P8_PARENT_NOETHER_CLOSURE_C_TERM_LEDGER.csv"
SRC_PARENT_NOETHER_DEMOTION = RESIDUALS / "P8_PARENT_NOETHER_CLOSURE_DEMOTION_TEST.csv"
SRC_MIN_ACTION_BLOCKS = RESIDUALS / "P8_MIN_PARENT_LOCAL_GR_ACTION_BLOCKS.csv"
SRC_FIRST_VARIATION_GATES = RESIDUALS / "P8_MTS_SYMBOL_FIRST_VARIATION_GATES.csv"
SRC_GK_CONTRACT = RESIDUALS / "P8_GAMMA_KHAT_QLOC_FIRST_VARIATION_CONTRACT.csv"
SRC_PIM_CONTRACT = RESIDUALS / "P8_PiM_parent_symplectic_projector_algebra_CONTRACT.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2939_SOURCE_REGISTER.csv",
    "extraction": RESIDUALS / "P8_Y5_R2FR_2939_PARENT_NOETHER_EXTRACTION_ATTEMPT.csv",
    "sectors": RESIDUALS / "P8_Y5_R2FR_2939_THETA_QTAU_SECTOR_CERTIFICATE_LEDGER.csv",
    "ctau": RESIDUALS / "P8_Y5_R2FR_2939_CTAU_RESIDUAL_DECOMPOSITION.csv",
    "closure": RESIDUALS / "P8_Y5_R2FR_2939_SOURCE_MEASURE_CLOSURE_AXIOM.csv",
    "impact": RESIDUALS / "P8_Y5_R2FR_2939_LOCAL_GR_NEWTON_GATE_IMPACT.csv",
    "claims": RESIDUALS / "P8_Y5_R2FR_2939_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2939_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2939_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2939_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2939_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "extraction_copy": PARENT_ACTION / "Parent_Noether_theta_Qtau_extraction_attempt_2939_NONCLAIM.csv",
    "ctau_copy": PARENT_ACTION / "Ctau_residual_decomposition_2939_NONCLAIM.csv",
    "closure_copy": PARENT_ACTION / "Source_measure_closure_axiom_2939_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR2939_PARENT_ACTION_SYNTHESIS_NEXT_NONCLAIM.csv",
}

for directory in {path.parent for path in OUTPUTS.values()} | {path.parent for path in BRANCH_OUTPUTS.values()} | {DOC.parent}:
    directory.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_parses(path: Path) -> bool:
    try:
        read_csv_rows(path)
        return True
    except Exception:
        return False


def anchors_present(path: Path, anchors: str) -> tuple[bool, str]:
    if not path.exists():
        return False, anchors
    text = read_text(path)
    missing = [anchor for anchor in anchors.split(";") if anchor and anchor not in text]
    return not missing, ";".join(missing)


def add_common(row: dict[str, Any]) -> dict[str, Any]:
    row.update(
        {
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "control_only": True,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": RUN_UTC,
        }
    )
    return row


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def is_under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def md_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def md_table(rows: list[dict[str, Any]], columns: list[str] | None = None) -> str:
    if not rows:
        return "_No rows._"
    selected = columns or list(rows[0].keys())
    header = "| " + " | ".join(selected) + " |"
    separator = "| " + " | ".join("---" for _ in selected) + " |"
    body = ["| " + " | ".join(md_escape(row.get(column, "")) for column in selected) + " |" for row in rows]
    return "\n".join([header, separator, *body])


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC2939_00_2938_doc", SRC_2938_DOC, "NEXT2938_0_2939;theta_MTS;Q_tau^MTS;Validation overall: `True`", "2938 handoff to parent Noether extraction"),
        ("SRC2939_01_2938_theorem", SRC_2938_THEOREM, "HWS2938_1_theta_Qtau;HWS2938_6_verdict", "Htau/source-measure theorem attempt"),
        ("SRC2939_02_2938_identity", SRC_2938_IDENTITY, "SMRI2938_0_master;SMRI2938_1_R_thetaQ", "source-measure residual identity"),
        ("SRC2939_03_2938_obstructions", SRC_2938_OBSTRUCTIONS, "OBS2938_0_theta_Qtau;OBS2938_1_integrability", "2938 obstruction ledger"),
        ("SRC2939_04_2938_next", SRC_2938_NEXT, "NEXT2938_0_2939", "machine-readable 2939 target"),
        ("SRC2939_05_2938_validation", SRC_2938_VALIDATION, "VAL2938_OVERALL;True", "2938 validation"),
        ("SRC2939_06_1008_doc", SRC_1008_DOC, "PVA1008_0_parent_action;PVA1008_6_verdict", "parent theta/Qtau extraction runner"),
        ("SRC2939_07_1009_doc", SRC_1009_DOC, "PCS1009_9_total_parent_contract;SVR1009_6_total_parent_switch_unsigned", "current-chain action sector contract"),
        ("SRC2939_08_2923_checklist", SRC_2923_CHECKLIST, "HC2923_0_parent_action_block;HC2923_3_theta_Qtau", "Hamiltonian/Q_tau coefficient checklist"),
        ("SRC2939_09_2668_proof", SRC_2668_PROOF, "LTO2668_1_absent_quotient;LTO2668_4_theta_charge", "L_X/Theta/omega owner proof audit"),
        ("SRC2939_10_2668_gate", SRC_2668_GATE, "LOG2668_0_branch;LOG2668_7_verdict", "L_X owner gate"),
        ("SRC2939_11_2856_noether", SRC_2856, "NDR2856_0_parent_variation;NDR2856_3_required_generator", "R2FR Noether derivation attempt"),
        ("SRC2939_12_2806_search", SRC_2806, "SEARCH2806_0_1008;SEARCH2806_4_parent_chain", "Noether search ledger"),
        ("SRC2939_13_2770_owner", SRC_2770, "NO2770_2_Noether_current_owner;NO2770_3_Hamiltonian_source_charge", "source owner audit"),
        ("SRC2939_14_2699_residuals", SRC_2699, "NRD2699_0_metric_response;NRD2699_6_total", "Noether residual decomposition"),
        ("SRC2939_15_2615_hilbert", SRC_2615, "NEC2615_2_weight_collapse;NEC2615_5_current_verdict", "Hilbert source/exchange theorem"),
        ("SRC2939_16_2339_ref", SRC_2339, "TQF2339_1_parent_L;TQF2339_2_theta_Qtau", "theta/Q_tau/fixed reference audit"),
        ("SRC2939_17_2429_gate", SRC_2429_GATE, "TOG2429_0_parent_route;TOG2429_5_verdict", "Theta_q owner gate"),
        ("SRC2939_18_2429_template", SRC_2429_TEMPLATE, "TPQ2429_0_general_variation;TPQ2429_5_verdict", "Theta_q/P_q template contract"),
        ("SRC2939_19_2462_verdict", SRC_2462, "TQV2462_0_conditional_sum;TQV2462_1_current_promotion", "theta/Q_tau promotion verdict"),
        ("SRC2939_20_2021_theorem", SRC_2021_THEOREM, "QSO2021_0_variation_additivity;QSO2021_7_verdict", "Q_tau sector owner theorem"),
        ("SRC2939_21_2021_ledger", SRC_2021_LEDGER, "QSL2021_0_EH_baseline;QSL2021_7_total", "Q_tau sector ledger"),
        ("SRC2939_22_1733_audit", SRC_1733_AUDIT, "COA1733_0_L_parent;COA1733_7_owner_verdict", "theta/Q_tau current owner audit"),
        ("SRC2939_23_1733_components", SRC_1733_COMPONENTS, "TQC1733_0_EH;TQC1733_6_total_Qtau", "theta/Q_tau component rows"),
        ("SRC2939_24_993_ledger", SRC_993_LEDGER, "QDEC993_0_EH;QDEC993_5_total", "Q_tau decomposition ledger"),
        ("SRC2939_25_771_audit", SRC_771_AUDIT, "TQ771_0_parent_variation;TQ771_6_owner_verdict", "early theta/Q_tau audit"),
        ("SRC2939_26_771_test", SRC_771_TEST, "NET771_0_parent_variation;NET771_4_verdict", "Noether extraction test"),
        ("SRC2939_27_824_audit", SRC_824_AUDIT, "N824_0_diffeomorphism_identity;N824_4_Bianchi_conservation_gate", "Noether variation warning"),
        ("SRC2939_28_parent_noether_chain", SRC_PARENT_NOETHER_CHAIN, "D505_0_local_parent_action_form;D505_6_worldtube_readout", "parent Noether closure derivation chain"),
        ("SRC2939_29_parent_noether_theorem", SRC_PARENT_NOETHER_THEOREM, "T505_conditional_Noether_mass_charge_closure;T505_Newton_limit_corollary", "parent Noether closure theorem"),
        ("SRC2939_30_parent_noether_cterm", SRC_PARENT_NOETHER_CTERM, "C505_EH;C505_boundary", "C-term ledger"),
        ("SRC2939_31_parent_noether_demotion", SRC_PARENT_NOETHER_DEMOTION, "DM505_0_if_EH_reduction_proved;DM505_2_if_C_terms_open_no_bounds", "Noether route demotion test"),
        ("SRC2939_32_min_action_blocks", SRC_MIN_ACTION_BLOCKS, "A511_0_EH_core;A511_6_metric_readout", "minimum local-GR action blocks"),
        ("SRC2939_33_first_variation_gates", SRC_FIRST_VARIATION_GATES, "FV512_0_metric;FV512_5_mass_projector", "symbol first-variation gates"),
        ("SRC2939_34_GK_contract", SRC_GK_CONTRACT, "GK513_0_action_existence;GK513_5_boundary_no_flux", "Gamma/Khat/q_loc first variation contract"),
        ("SRC2939_35_PiM_contract", SRC_PIM_CONTRACT, "PM0_fixed_exterior_topology;PM7_absolute_calibration_deferred", "Pi_M symplectic projector algebra contract"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, source_path, anchors, role in specs:
        found, missing = anchors_present(source_path, anchors)
        rows.append(
            add_common(
                {
                    "source_id": source_id,
                    "source_type": "local_file",
                    "source_path": str(source_path),
                    "anchors": anchors,
                    "role": role,
                    "path_exists": source_path.exists(),
                    "anchors_found": found,
                    "missing_anchors": missing,
                }
            )
        )
    return rows


def extraction_attempt_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "attempt_id": "PNE2939_0_master_formula",
            "object": "theta_MTS and Q_tau^MTS",
            "exact_statement": "For a finite-order diffeomorphism-invariant parent Lagrangian L_parent, delta L_parent=E_A delta Phi^A+dTheta_MTS and J_tau=Theta_MTS(L_tau Phi)-i_tau L_parent=dQ_tau^MTS+C_tau.",
            "derivation_status": "EXACT_CONDITIONAL_NOETHER_FORMULA",
            "current_mts_status": "NOT_PARENT_SIGNED",
            "condition_passed": True,
            "application_to_current_mts": False,
            "blocking_gap": "no signed L_parent with every retained sector varied before readout",
            "source_paths": f"{SRC_1008_DOC};{SRC_2021_THEOREM};{SRC_PARENT_NOETHER_THEOREM}",
        },
        {
            "attempt_id": "PNE2939_1_additivity",
            "object": "sector additivity",
            "exact_statement": "If L_parent=sum_s L_s+dB_ref, then Theta_MTS=sum_s Theta_s+delta B_ref and Q_tau^MTS=sum_s Q_tau^s+i_tau B_ref plus fixed corner/improvement terms.",
            "derivation_status": "EXACT_CONDITIONAL_SECTOR_SUM",
            "current_mts_status": "SECTOR_CERTIFICATES_MISSING",
            "condition_passed": True,
            "application_to_current_mts": False,
            "blocking_gap": "EH is only a reference anchor; extra/projector/boundary/matter-source sectors are not all extracted",
            "source_paths": f"{SRC_2021_THEOREM};{SRC_1009_DOC};{SRC_1733_COMPONENTS}",
        },
        {
            "attempt_id": "PNE2939_2_EH_anchor_limit",
            "object": "Q_tau^EH",
            "exact_statement": "Q_tau^EH may seed the known GR comparator only after MTS reduces to EH plus signed silent/topological residuals.",
            "derivation_status": "REFERENCE_GUARD_EXACT",
            "current_mts_status": "EH_ONLY_IMPORT_REJECTED",
            "condition_passed": True,
            "application_to_current_mts": False,
            "blocking_gap": "using EH charge as the total MTS charge would borrow the GR answer",
            "source_paths": f"{SRC_1008_DOC};{SRC_993_LEDGER};{SRC_2021_LEDGER}",
        },
        {
            "attempt_id": "PNE2939_3_extra_sector",
            "object": "Q_tau^X + C_tau^X",
            "exact_statement": "The extra motion/time/range/memory sector contributes only after L_X, Theta_X, omega_X, Q_tau^X, source silence and boundary pullback are owned.",
            "derivation_status": "FORMULA_READY_NOT_OWNED",
            "current_mts_status": "MISSING_LX_THETA_OMEGA_QTAU_OWNER",
            "condition_passed": False,
            "application_to_current_mts": False,
            "blocking_gap": "no selected parent L_X branch; Gamma/Khat/q_loc action-existence and first variation remain open",
            "source_paths": f"{SRC_2668_PROOF};{SRC_2668_GATE};{SRC_GK_CONTRACT}",
        },
        {
            "attempt_id": "PNE2939_4_projector_source",
            "object": "Q_tau^projector + [d,Pi_M]J_H",
            "exact_statement": "Pi_M/source-measure terms are legal only if Pi_M is parent-owned and delta(Pi_M J_H)=Pi_M delta J_H+(delta Pi_M)J_H is either zero or retained.",
            "derivation_status": "CONDITIONAL_PROJECTOR_LEDGER",
            "current_mts_status": "PIM_CURRENT_NOT_PARENT_DERIVED",
            "condition_passed": False,
            "application_to_current_mts": False,
            "blocking_gap": "projector algebra alone does not produce flux closure or a source charge",
            "source_paths": f"{SRC_PIM_CONTRACT};{SRC_1733_COMPONENTS};{SRC_2021_LEDGER}",
        },
        {
            "attempt_id": "PNE2939_5_matter_source",
            "object": "C_tau^matter/source",
            "exact_statement": "Ordinary matter/source contribution becomes part of Q_tau only when the same S_matter supplies Hilbert current, source measure, coframe and coupling normalization.",
            "derivation_status": "CONDITIONAL_SOURCE_GLUE_REQUIREMENT",
            "current_mts_status": "SOURCE_GLUE_NOT_SIGNED",
            "condition_passed": False,
            "application_to_current_mts": False,
            "blocking_gap": "same-action Hilbert current and worldtube source-measure glue remain unsigned",
            "source_paths": f"{SRC_2770};{SRC_2615};{SRC_2938_THEOREM}",
        },
        {
            "attempt_id": "PNE2939_6_verdict",
            "object": "current MTS theta_MTS/Q_tau^MTS extraction",
            "exact_statement": "Current MTS promotes theta_MTS and Q_tau^MTS only if every retained sector has an action source, variation equation, theta, Q_tau/C_tau piece, tau action, boundary/reference rule, stress contribution and parent certificate.",
            "derivation_status": "THEOREM_ROUTE_SHARPENED_BUT_NOT_CLOSED",
            "current_mts_status": "PARENT_NOETHER_EXTRACTION_NOT_DERIVED",
            "condition_passed": False,
            "application_to_current_mts": False,
            "blocking_gap": "retain closure-only branch and sector certificate matrix",
            "source_paths": f"{SRC_1008_DOC};{SRC_1009_DOC};{SRC_2462}",
        },
    ]
    return [add_common(row) for row in rows]


def sector_certificate_rows() -> list[dict[str, Any]]:
    specs = [
        ("SEC2939_0_EH_core", "EH core", "Theta_EH and Q_tau^EH", "CONDITIONAL_GR_REFERENCE_ONLY", "MTS reduction to EH plus fixed tau/surface/reference and silent sectors", SRC_MIN_ACTION_BLOCKS),
        ("SEC2939_1_kappa_topological", "kappa topological sector", "d kappa_eff=0 and no local coupling drift", "CANDIDATE_NOT_ADOPTED", "parent adoption and no source/species/domain labels", SRC_1009_DOC),
        ("SEC2939_2_universal_matter", "ordinary matter/source", "same S_matter supplies Hilbert current and source coupling", "CONDITIONAL_SOURCE_INPUT_UNSIGNED", "matter descent, same observed coframe, no source-only prefactor", SRC_2770),
        ("SEC2939_3_extra_GK", "Gamma/Khat/q_loc extra sector", "Theta_X, Q_tau^X, C_tau^X", "MISSING_ACTION_EXISTENCE", "Helmholtz-compatible action, Euler closure, double-zero and boundary no-flux", SRC_GK_CONTRACT),
        ("SEC2939_4_domain_selector", "domain/projector selector", "selector stress and Q_tau selector contribution", "PARTIAL_CLAUSE_NOT_PARENT_CLOSED", "Euler/topological domain selection, metric stress and local/FLRW branch rule", SRC_FIRST_VARIATION_GATES),
        ("SEC2939_5_PiM", "mass projector Pi_M", "projector/source-current Hamiltonian contribution", "NOT_PARENT_DERIVED", "Pi_M parent origin, delta Pi_M stress, Ward/Euler flux closure", SRC_PIM_CONTRACT),
        ("SEC2939_6_boundary_reference", "boundary/reference", "Q_tau^boundary + delta B_ref", "FIXED_REFERENCE_MISSING", "fixed-before-readout reference, improvement ambiguity and boundary flux certificate", SRC_2339),
        ("SEC2939_7_memory_response", "memory/response doublet", "memory/doublet Q_tau contribution or zero theorem", "PARTIAL_CANDIDATE_NOT_MATCHED", "complete component map, positive operator, zero odd source, PPN lock", SRC_1009_DOC),
        ("SEC2939_8_tau_surface", "tau/surface/readout", "same observed time generator and linked surfaces", "MISSING_TAU_SURFACE_LOCK", "tau_source=tau_charge=tau_clock=tau_readout and fixed linked surfaces", SRC_1733_AUDIT),
        ("SEC2939_9_worldtube_glue", "worldtube source glue", "M_source[W]=int_S Q_M[tau] before orbital fitting", "CONDITIONAL_NOT_SIGNED", "parent Noether identity, charge form, exterior closure and compact source support", SRC_2938_THEOREM),
        ("SEC2939_10_total", "S_parent total", "theta_MTS and Q_tau^MTS total", "NOT_PROMOTED", "all sector certificates above must pass with source paths and units", SRC_1009_DOC),
    ]
    return [
        add_common(
            {
                "sector_id": sector_id,
                "sector": sector,
                "required_theta_Qtau_piece": piece,
                "current_status": status,
                "promotion_requirement": requirement,
                "source_path": str(source_path),
                "source_path_exists": source_path.exists(),
                "sector_certificate_passed": False,
            }
        )
        for sector_id, sector, piece, status, requirement, source_path in specs
    ]


def ctau_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "ctau_id": "CTA2939_0_master",
            "component": "C_tau_total",
            "definition": "C_tau^MTS = C_EH + C_extra + C_projector + C_boundary_ref + C_matter_source + C_tau_surface + C_Dq + C_units",
            "zero_or_bound_requirement": "all components are theorem-zero or source-backed bounded with common M_H_ref",
            "current_status": "COMPONENTS_UNFILLED",
            "feeds": "H_tau integrability;M_H_ref;Newton;R10;PPN;local_GR",
        },
        {
            "ctau_id": "CTA2939_1_C_EH",
            "component": "C_EH",
            "definition": "EH field-equation/subtraction term in the local exterior",
            "zero_or_bound_requirement": "MTS-to-EH reduction plus fixed Lambda/background subtraction",
            "current_status": "CONDITIONAL_GR_REFERENCE_ONLY",
            "feeds": "Newton;local_GR",
        },
        {
            "ctau_id": "CTA2939_2_C_extra",
            "component": "C_extra",
            "definition": "non-EH motion/time/domain/memory/range source and symplectic contribution",
            "zero_or_bound_requirement": "extra-sector no-hair/double-zero or finite source-backed residual",
            "current_status": "MISSING_EXTRA_SECTOR_THETA_QTAU",
            "feeds": "PPN;R10;local_GR",
        },
        {
            "ctau_id": "CTA2939_3_C_projector",
            "component": "C_projector",
            "definition": "Pi_M/source-current commutator and projector stress",
            "zero_or_bound_requirement": "d(Pi_M J_H)=0 or explicit commutator/projector-stress bound",
            "current_status": "RETAINED_PROJECTOR_OBSTRUCTION",
            "feeds": "Newton;R10;local_GR",
        },
        {
            "ctau_id": "CTA2939_4_C_boundary_ref",
            "component": "C_boundary_ref",
            "definition": "boundary, exact improvement, corner and H_ref shift",
            "zero_or_bound_requirement": "fixed source-blind reference plus exact/proper boundary no-flux or finite row",
            "current_status": "REFERENCE_BOUNDARY_NOT_FIXED",
            "feeds": "M_H_ref;Newton;PPN",
        },
        {
            "ctau_id": "CTA2939_5_C_matter_source",
            "component": "C_matter_source",
            "definition": "ordinary matter/source worldtube and coupling normalization contribution",
            "zero_or_bound_requirement": "same-action Hilbert current, source measure glue and no source-shadow prefactor",
            "current_status": "SOURCE_GLUE_NOT_SIGNED",
            "feeds": "Newton;WEP;R10",
        },
        {
            "ctau_id": "CTA2939_6_C_tau_surface",
            "component": "C_tau_surface",
            "definition": "nonprojectable tau, moving surface, frame/readout mismatch",
            "zero_or_bound_requirement": "same tau/coframe/frame across source, charge, clocks, R10 and orbit",
            "current_status": "MISSING_SAME_FRAME_LOCK",
            "feeds": "dotG;clocks;Newton",
        },
        {
            "ctau_id": "CTA2939_7_C_Dq",
            "component": "C_Dq",
            "definition": "quotient-map/current leakage into charge or source readout",
            "zero_or_bound_requirement": "explicit q(Phi), Dq, vertical kernel and observed-map descent",
            "current_status": "DQ_DESCENT_NOT_SIGNED",
            "feeds": "local_GR;PPN;R10",
        },
        {
            "ctau_id": "CTA2939_8_C_units",
            "component": "C_units",
            "definition": "ell_J, C_source, units and denominator convention leakage",
            "zero_or_bound_requirement": "pre-readout ell_J/C_source owner theorem or independent drift/source bound",
            "current_status": "ELLJ_CSOURCE_OWNER_NOT_DERIVED",
            "feeds": "dotG;R10;Newton",
        },
    ]
    return [add_common(row) for row in rows]


def closure_axiom_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "axiom_id": "AX2939_0_parent_Noether",
            "axiom_if_adopted": "There exists a finite-order diffeomorphism-invariant parent Lagrangian L_parent whose total variation gives theta_MTS and whose observed-time Noether current satisfies J_tau=dQ_tau^MTS+C_tau.",
            "cost": "This becomes an explicit parent-action closure, not a derivation from the present corpus.",
            "allowed_use": "private algebraic continuation only; no Newton/local-GR/R10 claim.",
            "current_recommendation": "do_not_adopt_yet_try_minimal_parent_action_synthesis",
        },
        {
            "axiom_id": "AX2939_1_Ctau_silence",
            "axiom_if_adopted": "C_tau^MTS vanishes or is bounded below all local gates on the compact local exterior.",
            "cost": "Would hide the main local-GR residual vector unless each component is later derived.",
            "allowed_use": "temporary branch label for proving downstream implications only.",
            "current_recommendation": "reject_as_claim_input",
        },
        {
            "axiom_id": "AX2939_2_source_measure",
            "axiom_if_adopted": "M_source[W]=H_tau[S_outer]-H_ref=int_W rho_H dV_H with fixed ell_J/reference and no orbital GM import.",
            "cost": "Turns the Newton source bridge into a closure axiom.",
            "allowed_use": "nonclaim bridge bookkeeping only.",
            "current_recommendation": "keep_as_fallback_after_2940_attempt",
        },
    ]
    return [add_common(row) for row in rows]


def impact_rows() -> list[dict[str, Any]]:
    specs = [
        ("IMP2939_0_Htau", "H_tau source charge", "blocked", "theta_MTS/Q_tau^MTS not extracted; C_tau components unfilled"),
        ("IMP2939_1_MHref", "M_H_ref denominator", "blocked", "H_tau, H_ref, tau/frame and positivity depend on Noether extraction"),
        ("IMP2939_2_Newton", "Newton/Gauss source bridge", "blocked", "source charge cannot be compared to orbital GM without circularity"),
        ("IMP2939_3_local_GR", "local GR/PPN branch", "blocked", "extra/projector/boundary/source residuals remain in C_tau_total"),
        ("IMP2939_4_R10", "R10 alpha branch", "blocked", "Qbar_XH denominator and tau_R10 source normalization depend on M_H_ref/source measure"),
        ("IMP2939_5_dotG", "dotG-to-kappa transfer", "blocked", "ell_J/C_source/R_frame owner remains downstream of source-current normalization"),
        ("IMP2939_6_cosmology", "cosmology branch", "not decided", "Noether local source issue does not by itself falsify/confirm cosmological memory fits"),
    ]
    return [
        add_common(
            {
                "impact_id": impact_id,
                "gate": gate,
                "status": status,
                "reason": reason,
                "claim_allowed": False,
            }
        )
        for impact_id, gate, status, reason in specs
    ]


def claim_gate_rows(extraction_rows: list[dict[str, Any]], sector_rows: list[dict[str, Any]], ctau_data: list[dict[str, Any]]) -> list[dict[str, Any]]:
    conditional_formula = any(row["attempt_id"] == "PNE2939_0_master_formula" and row["derivation_status"] == "EXACT_CONDITIONAL_NOETHER_FORMULA" for row in extraction_rows)
    current_extracted = any(row["attempt_id"] == "PNE2939_6_verdict" and row["current_mts_status"] != "PARENT_NOETHER_EXTRACTION_NOT_DERIVED" for row in extraction_rows)
    all_sector_passed = all(str(row["sector_certificate_passed"]).lower() == "true" for row in sector_rows)
    ctau_filled = all("MISSING" not in row["current_status"] and "UNFILLED" not in row["current_status"] and "NOT_SIGNED" not in row["current_status"] for row in ctau_data)
    rows = [
        ("CG2939_0_conditional_formula", "Noether theta/Q_tau formula written", conditional_formula, "PASS_CONDITIONAL_NONCLAIM" if conditional_formula else "FAIL"),
        ("CG2939_1_current_extraction", "current MTS extracts theta_MTS and Q_tau^MTS", current_extracted, "BLOCKED_NONCLAIM"),
        ("CG2939_2_sector_certificates", "all sector theta/Q_tau certificates pass", all_sector_passed, "BLOCKED_SECTOR_CERTIFICATES_MISSING"),
        ("CG2939_3_Ctau", "all C_tau residual components are zero/bounded", ctau_filled, "BLOCKED_COMPONENTS_UNFILLED"),
        ("CG2939_4_MHref", "M_H_ref can be promoted", False, "BLOCKED_BY_QTAU_HTAU_HREF"),
        ("CG2939_5_Newton_GR", "Newton/local-GR bridge can be claimed", False, "BLOCKED_BY_PARENT_NOETHER_EXTRACTION"),
        ("CG2939_6_R10", "R10/Qbar/tau can be claimed", False, "BLOCKED_BY_MHREF_SOURCE_MEASURE"),
        ("CG2939_7_public_claim", "any public local/empirical claim allowed from 2939", False, "NO_PUBLIC_CLAIM"),
    ]
    return [
        add_common(
            {
                "claim_gate_id": gate_id,
                "claim": claim,
                "condition_passed": passed,
                "status": status,
                "blocks_claim": not passed or gate_id != "CG2939_0_conditional_formula",
                "claim_allowed": False,
            }
        )
        for gate_id, claim, passed, status in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "decision_id": "DEC2939_0_result",
            "decision": "keep parent Noether extraction as conditional, not claimed",
            "reason": "the formal theorem is exact but the current corpus does not supply a signed total parent action or sector certificates",
            "next_action": "do not promote theta_MTS/Q_tau^MTS as current MTS objects",
        },
        {
            "decision_id": "DEC2939_1_root_gap",
            "decision": "the next root gap is parent action synthesis, not another empirical runner",
            "reason": "without L_parent, every H_tau/M_H_ref/Qbar/tau row remains a denominator shadow",
            "next_action": "build a minimal parent current-chain action candidate with sector certificates",
        },
        {
            "decision_id": "DEC2939_2_no_EH_smuggling",
            "decision": "EH covariant charge remains a comparator/reference only",
            "reason": "EH charge is useful, but using it as total MTS Q_tau would prove GR by assuming GR",
            "next_action": "allow EH anchor only after MTS-to-EH reduction certificates are signed",
        },
        {
            "decision_id": "DEC2939_3_closure_fallback",
            "decision": "write closure axioms but do not adopt them as evidence",
            "reason": "closure may be useful for algebraic exploration, but the project goal is derivability",
            "next_action": "try 2940 parent action synthesis before any closure branch continuation",
        },
    ]
    return [add_common(row) for row in rows]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "next_id": "NEXT2939_0_2940",
                "priority": "selected_primary",
                "next_doc": "2940-Y5-R2FR-minimal-parent-current-chain-action-synthesis-or-sector-certificate-matrix-under-AX1090.md",
                "next_script": "scripts/Y5_R2FR_minimal_parent_current_chain_action_synthesis_or_sector_certificate_matrix_under_AX1090_2940.py",
                "objective": "Attempt to synthesize the minimal parent current-chain action whose sector variations would actually supply theta_MTS, Q_tau^MTS and C_tau; if synthesis fails, produce a precise sector-certificate matrix and keep local claims blocked.",
                "include": "EH core; kappa topological candidate; universal matter; Gamma/Khat/q_loc sector; Pi_M/worldtube sector; boundary/reference; tau/surface; field list; variation equation; theta/Q_tau/C_tau row for each sector",
                "exclude": "R10/local-GR/Newton claim; EH-only parent import; measured-GM denominator; fitted reference; GitHub action; formalization-workbench edits",
            }
        )
    ]


def write_doc(
    source_rows: list[dict[str, Any]],
    extraction_rows: list[dict[str, Any]],
    sector_rows: list[dict[str, Any]],
    ctau_data: list[dict[str, Any]],
    closure_rows: list[dict[str, Any]],
    impact_data: list[dict[str, Any]],
    claim_rows: list[dict[str, Any]],
    decision: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    branch_rows: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    text = f"""# 2939 - Y5 R2FR: parent Noether theta/Qtau extraction or source-measure closure axiom under AX1090

Status: `Y5_R2FR_2939_conditional_parent_Noether_theta_Qtau_formula_written_current_MTS_not_extracted_2940_parent_action_synthesis_next`

Claim ceiling: `conditional_Noether_formula_yes_current_theta_MTS_no_Qtau_MTS_no_Htau_no_MHref_no_Newton_no_local_GR_no_R10_no_GitHub_claim`

2939 attacks the root current-chain question. The exact Noether formula is not the problem:

`delta L_parent = E_A delta Phi^A + d theta_MTS`, and `J_tau = theta_MTS(L_tau Phi) - i_tau L_parent = d Q_tau^MTS + C_tau`.

The problem is ownership. Current MTS has not yet supplied a single parent action whose retained EH, matter/source, extra, projector, boundary/reference, tau/surface and worldtube sectors all vary before readout. So this checkpoint writes the formula, refuses promotion, and decomposes the surviving `C_tau` residual.

## Source Register

{md_table(source_rows, ["source_id", "source_type", "source_path", "path_exists", "anchors_found", "role"])}

## Parent Noether Extraction Attempt

{md_table(extraction_rows, ["attempt_id", "object", "derivation_status", "current_mts_status", "condition_passed", "application_to_current_mts", "blocking_gap"])}

## Theta/Q_tau Sector Certificate Ledger

{md_table(sector_rows, ["sector_id", "sector", "required_theta_Qtau_piece", "current_status", "promotion_requirement", "sector_certificate_passed"])}

## C_tau Residual Decomposition

{md_table(ctau_data, ["ctau_id", "component", "definition", "zero_or_bound_requirement", "current_status", "feeds"])}

## Source-Measure Closure Axiom

{md_table(closure_rows, ["axiom_id", "axiom_if_adopted", "cost", "allowed_use", "current_recommendation"])}

## Local GR/Newton Gate Impact

{md_table(impact_data, ["impact_id", "gate", "status", "reason", "claim_allowed"])}

## Claim Gates

{md_table(claim_rows, ["claim_gate_id", "claim", "condition_passed", "status", "blocks_claim", "claim_allowed"])}

## Decision Ledger

{md_table(decision, ["decision_id", "decision", "reason", "next_action"])}

## Next Target

{md_table(next_rows, ["next_id", "priority", "next_doc", "next_script", "objective", "exclude"])}

## Branch Copies

{md_table(branch_rows, ["copy_id", "source_path", "copy_path", "source_exists", "copy_exists", "valid_for_claim"])}

## Validation

{md_table(validation, ["validation_id", "passed", "check", "required"])}

Validation overall: `{next(row["passed"] for row in validation if row["validation_id"] == "VAL2939_OVERALL")}`.
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    source_rows = source_register_rows()
    extraction_rows = extraction_attempt_rows()
    sector_rows = sector_certificate_rows()
    ctau_data = ctau_rows()
    closure_rows = closure_axiom_rows()
    impact_data = impact_rows()
    claim_rows = claim_gate_rows(extraction_rows, sector_rows, ctau_data)
    decision = decision_rows()
    next_rows = next_target_rows()

    write_csv(OUTPUTS["sources"], source_rows)
    write_csv(OUTPUTS["extraction"], extraction_rows)
    write_csv(OUTPUTS["sectors"], sector_rows)
    write_csv(OUTPUTS["ctau"], ctau_data)
    write_csv(OUTPUTS["closure"], closure_rows)
    write_csv(OUTPUTS["impact"], impact_data)
    write_csv(OUTPUTS["claims"], claim_rows)
    write_csv(OUTPUTS["decision"], decision)
    write_csv(OUTPUTS["next"], next_rows)

    shutil.copy2(OUTPUTS["extraction"], BRANCH_OUTPUTS["extraction_copy"])
    shutil.copy2(OUTPUTS["ctau"], BRANCH_OUTPUTS["ctau_copy"])
    shutil.copy2(OUTPUTS["closure"], BRANCH_OUTPUTS["closure_copy"])
    shutil.copy2(OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"])
    branch_rows = [
        add_common(
            {
                "copy_id": copy_id,
                "source_path": str(source_path),
                "copy_path": str(copy_path),
                "source_exists": source_path.exists(),
                "copy_exists": copy_path.exists(),
                "valid_for_claim": False,
            }
        )
        for copy_id, source_path, copy_path in [
            ("extraction_copy", OUTPUTS["extraction"], BRANCH_OUTPUTS["extraction_copy"]),
            ("ctau_copy", OUTPUTS["ctau"], BRANCH_OUTPUTS["ctau_copy"]),
            ("closure_copy", OUTPUTS["closure"], BRANCH_OUTPUTS["closure_copy"]),
            ("next_copy", OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"]),
        ]
    ]
    write_csv(OUTPUTS["branches"], branch_rows)

    generated_csvs = list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values())
    sources_exist = all(str(row["path_exists"]).lower() == "true" for row in source_rows)
    anchors_ok = all(str(row["anchors_found"]).lower() == "true" for row in source_rows)
    conditional_formula = any(row["attempt_id"] == "PNE2939_0_master_formula" and row["derivation_status"] == "EXACT_CONDITIONAL_NOETHER_FORMULA" for row in extraction_rows)
    current_blocked = any(row["attempt_id"] == "PNE2939_6_verdict" and row["current_mts_status"] == "PARENT_NOETHER_EXTRACTION_NOT_DERIVED" for row in extraction_rows)
    sector_failures_explicit = any(row["sector_id"] == "SEC2939_10_total" and row["current_status"] == "NOT_PROMOTED" for row in sector_rows) and all(str(row["sector_certificate_passed"]).lower() == "false" for row in sector_rows)
    ctau_unfilled = any("MISSING" in row["current_status"] or "UNFILLED" in row["current_status"] or "NOT_SIGNED" in row["current_status"] for row in ctau_data)
    closure_nonclaim = all(str(row["valid_for_claim"]).lower() == "false" and str(row["claim_allowed"]).lower() == "false" for row in closure_rows)
    claims_blocked = all(str(row["claim_allowed"]).lower() == "false" for row in claim_rows)
    branches_exist = all(row["copy_exists"] for row in branch_rows)
    outputs_under_root = all(is_under(path, ROOT) for path in generated_csvs + [DOC])
    formalization_clean = not any(FORMALIZATION.rglob("*2939*")) if FORMALIZATION.exists() else True
    csvs_parse = all(csv_parses(path) for path in generated_csvs)

    validation = [
        {"validation_id": "VAL2939_0_sources_exist", "passed": sources_exist, "check": "all cited local source paths exist", "required": True},
        {"validation_id": "VAL2939_1_anchors_found", "passed": anchors_ok, "check": "all source anchors found", "required": True},
        {"validation_id": "VAL2939_2_conditional_formula", "passed": conditional_formula, "check": "conditional parent Noether formula written", "required": True},
        {"validation_id": "VAL2939_3_current_blocked", "passed": current_blocked, "check": "current MTS theta/Q_tau extraction remains blocked", "required": True},
        {"validation_id": "VAL2939_4_sector_failures_explicit", "passed": sector_failures_explicit, "check": "sector certificate failures are explicit", "required": True},
        {"validation_id": "VAL2939_5_ctau_unfilled", "passed": ctau_unfilled, "check": "C_tau residual decomposition exposes unfilled components", "required": True},
        {"validation_id": "VAL2939_6_closure_nonclaim", "passed": closure_nonclaim, "check": "closure axioms remain nonclaim", "required": True},
        {"validation_id": "VAL2939_7_claims_blocked", "passed": claims_blocked, "check": "no empirical/local-GR/Newton claim allowed", "required": True},
        {"validation_id": "VAL2939_8_branches_exist", "passed": branches_exist, "check": "branch copy files exist", "required": True},
        {"validation_id": "VAL2939_9_csvs_parse", "passed": csvs_parse, "check": "all generated CSV files parse", "required": True},
        {"validation_id": "VAL2939_10_outputs_under_post_checkpoint", "passed": outputs_under_root, "check": "all generated outputs are under post-checkpoint-work", "required": True},
        {"validation_id": "VAL2939_11_formalization_clean", "passed": formalization_clean, "check": "no 2939 outputs were written to formalization-workbench", "required": True},
    ]
    overall = all(row["passed"] is True for row in validation)
    validation.append({"validation_id": "VAL2939_OVERALL", "passed": overall, "check": "2939 validation overall", "required": True})
    validation = [add_common(row) for row in validation]
    write_csv(OUTPUTS["validation"], validation)
    write_doc(source_rows, extraction_rows, sector_rows, ctau_data, closure_rows, impact_data, claim_rows, decision, next_rows, branch_rows, validation)

    print(f"wrote {DOC}")
    print(f"validation overall: {overall}")


if __name__ == "__main__":
    main()
