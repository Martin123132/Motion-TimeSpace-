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
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
PARENT_ACTION = ROOT / "source-intake" / "parent-action"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"

CHECKPOINT = "2947"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
RUN_UTC = SCRIPT_START_UTC.isoformat()

DOC = ROOT / "2947-Y5-R2FR-parent-theta-Qtau-MHref-certificate-or-denominator-first-row-runner-under-AX1090.md"

SRC_2946_DOC = ROOT / "2946-Y5-R2FR-MHref-PiM-denominator-package-theorem-or-first-source-row-under-AX1090.md"
SRC_2946_THEOREM = RESIDUALS / "P8_Y5_R2FR_2946_DENOMINATOR_PACKAGE_THEOREM_ATTEMPT.csv"
SRC_2946_SCHEMA = RESIDUALS / "P8_Y5_R2FR_2946_FIRST_ROW_ACQUISITION_SCHEMAS.csv"
SRC_2946_NEXT = RESIDUALS / "P8_Y5_R2FR_2946_NEXT_TARGET.csv"
SRC_2939_SECTORS = RESIDUALS / "P8_Y5_R2FR_2939_THETA_QTAU_SECTOR_CERTIFICATE_LEDGER.csv"
SRC_2923_HCORE = RESIDUALS / "P8_Y5_R2FR_2923_HCORE_QTAU_COEFFICIENT_CHECKLIST.csv"
SRC_2339_AUDIT = RESIDUALS / "P8_Y5_PARENT_QLOC_2339_THETA_QTAU_FIXED_REFERENCE_AUDIT.csv"
SRC_2380_RECHECK = RESIDUALS / "P8_Y5_PARENT_QLOC_2380_THETA_QTAU_GATE_RECHECK.csv"
SRC_2462_PROMOTION = RESIDUALS / "P8_Y5_PARENT_QLOC_2462_THETA_QTAU_PROMOTION_VERDICT.csv"
SRC_1733_COMPONENTS = RESIDUALS / "P8_Y5_PARENT_QLOC_1733_THETA_QTAU_COMPONENT_ROWS.csv"
SRC_1734_LEAKS = RESIDUALS / "P8_Y5_PARENT_QLOC_1734_THETA_QTAU_LEAK_ROWS.csv"
SRC_2021_LEDGER = RESIDUALS / "P8_Y5_PARENT_QLOC_2021_QTAU_SECTOR_LEDGER.csv"
SRC_2021_THEOREM = RESIDUALS / "P8_Y5_PARENT_QLOC_2021_QTAU_SECTOR_OWNER_THEOREM.csv"
SRC_NOETHER_THEOREM = RESIDUALS / "P8_PARENT_NOETHER_CLOSURE_THEOREM.csv"
SRC_NOETHER_CTERMS = RESIDUALS / "P8_PARENT_NOETHER_CLOSURE_C_TERM_LEDGER.csv"
SRC_HCI = RESIDUALS / "P8_Y5_HAMILTONIAN_CHARGE_INTEGRABILITY_REFERENCE_ATTEMPT.csv"
SRC_CURL_AUDIT = RESIDUALS / "P8_Y5_R10_HTAU_INTEGRABILITY_CURL_2667_CURL_PROOF_AUDIT.csv"
SRC_CURL_TEMPLATE = RESIDUALS / "P8_Y5_R10_HTAU_INTEGRABILITY_CURL_2667_COMPONENT_ROW_TEMPLATE_NONCLAIM.csv"
SRC_HCHARGE = RESIDUALS / "P8_mass_current_Hamiltonian_boundary_charge_CONTRACT.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2947_SOURCE_REGISTER.csv",
    "certificate": RESIDUALS / "P8_Y5_R2FR_2947_THETA_QTAU_CERTIFICATE_ATTEMPT.csv",
    "sectors": RESIDUALS / "P8_Y5_R2FR_2947_SECTOR_CHARGE_CERTIFICATE_MATRIX.csv",
    "runner": RESIDUALS / "P8_Y5_R2FR_2947_MHREF_PIM_FIRST_ROW_RUNNER_ROWS.csv",
    "curl": RESIDUALS / "P8_Y5_R2FR_2947_HTAU_INTEGRABILITY_RESIDUAL_ROWS.csv",
    "guards": RESIDUALS / "P8_Y5_R2FR_2947_CHARGE_IMPORT_GUARDS.csv",
    "claims": RESIDUALS / "P8_Y5_R2FR_2947_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2947_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2947_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2947_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2947_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "certificate_copy": PARENT_ACTION / "Theta_Qtau_certificate_attempt_2947_NONCLAIM.csv",
    "sector_copy": PARENT_ACTION / "Theta_Qtau_sector_charge_matrix_2947_NONCLAIM.csv",
    "runner_copy": LOCAL_BOUNDS / "MHref_PiM_first_row_runner_rows_2947_NONCLAIM.csv",
    "curl_copy": LOCAL_BOUNDS / "Htau_integrability_residual_rows_2947_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR2947_PARENT_CURRENT_CHAIN_OR_IX_NEXT_NONCLAIM.csv",
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
        ("SRC2947_00_2946_doc", SRC_2946_DOC, "NEXT2946_0_2947;Validation overall: `True`", "2946 handoff to theta/Qtau root"),
        ("SRC2947_01_2946_theorem", SRC_2946_THEOREM, "THM2946_1_theta_Qtau;THM2946_7_verdict", "denominator theorem blocker"),
        ("SRC2947_02_2946_schema", SRC_2946_SCHEMA, "SCHEMA2946_1_theta_Qtau;SCHEMA2946_4_PiM_Hilbert", "first-row schema handoff"),
        ("SRC2947_03_2946_next", SRC_2946_NEXT, "NEXT2946_0_2947", "machine-readable 2947 target"),
        ("SRC2947_04_2939_sectors", SRC_2939_SECTORS, "SEC2939_0_EH_core;SEC2939_9_worldtube_glue", "sector certificate ledger"),
        ("SRC2947_05_2923_hcore", SRC_2923_HCORE, "HC2923_3_theta_Qtau;HC2923_5_MHref_denominator", "Hcore/Q_tau checklist"),
        ("SRC2947_06_2339_audit", SRC_2339_AUDIT, "TQF2339_0;TQF2339_7", "theta/Qtau fixed-reference audit"),
        ("SRC2947_07_2380_recheck", SRC_2380_RECHECK, "TQR2380_0;TQR2380_5", "theta/Qtau gate recheck"),
        ("SRC2947_08_2462_promotion", SRC_2462_PROMOTION, "TQV2462_0;TQV2462_3", "theta/Qtau promotion verdict"),
        ("SRC2947_09_1733_components", SRC_1733_COMPONENTS, "TQC1733_0;TQC1733_6", "theta/Qtau component rows"),
        ("SRC2947_10_1734_leaks", SRC_1734_LEAKS, "TLR1734_0;TLR1734_4", "theta/Qtau leak rows"),
        ("SRC2947_11_2021_ledger", SRC_2021_LEDGER, "QSL2021_0;QSL2021_6", "Q_tau sector ledger"),
        ("SRC2947_12_2021_theorem", SRC_2021_THEOREM, "QSO2021_0_variation_additivity;QSO2021_7_verdict", "Q_tau sector owner theorem"),
        ("SRC2947_13_noether_theorem", SRC_NOETHER_THEOREM, "T505_conditional_Noether_mass_charge_closure;T505_Newton_limit_corollary", "conditional Noether mass charge theorem"),
        ("SRC2947_14_noether_cterms", SRC_NOETHER_CTERMS, "C505_EH;C505_boundary", "Noether C-term ledger"),
        ("SRC2947_15_hci", SRC_HCI, "HCI554_2_parent_Lagrangian_theta_Q;HCI554_6_integrability_verdict", "Hamiltonian charge integrability attempt"),
        ("SRC2947_16_curl_audit", SRC_CURL_AUDIT, "HTC2667_0_target;HTC2667_7_verdict", "H_tau curl proof audit"),
        ("SRC2947_17_curl_template", SRC_CURL_TEMPLATE, "HCUR2667_0_delta_H_tau_nonintegrable;HCUR2667_6_MHref_feed", "H_tau curl component template"),
        ("SRC2947_18_hcharge", SRC_HCHARGE, "HC0_same_frame_EH_exterior;HC9_retained_residual_fallback", "Hamiltonian boundary charge contract"),
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


def certificate_rows() -> list[dict[str, Any]]:
    rows = [
        ("CERT2947_0_parent_variation", "single parent variation", "delta L_parent = sum_s(E_s delta Phi_s + dTheta_s) + d delta B_ref", "EXACT_CONDITIONAL_FORMULA", "one signed L_parent with all retained sectors is missing", False),
        ("CERT2947_1_total_theta", "theta_MTS", "Theta_total = sum_s Theta_s + delta B_ref", "CONDITIONAL_ADDITIVITY", "Theta_s not extracted for GK/domain/PiM/boundary/memory sectors", False),
        ("CERT2947_2_total_Qtau", "Q_tau_MTS", "J_tau = Theta_total(L_tau Phi)-i_tau L_parent = dQ_tau^MTS + C_tau", "CONDITIONAL_NOETHER_FORM", "Q_tau_X, Q_tau_projector, C_tau_s and boundary/reference pieces not owned", False),
        ("CERT2947_3_EH_reference", "EH Q_tau", "EH charge is a valid reference if MTS reduces to EH plus silent/exact sectors", "CONDITIONAL_GR_REFERENCE_ONLY", "MTS sector silence and source normalization are not signed", False),
        ("CERT2947_4_Htau_integrability", "H_tau integrability", "alpha_tau=int_S(delta Q_tau^MTS-i_tau Theta_total)-delta H_ref is field-space closed", "EXACT_REQUIREMENT", "omega_X, boundary flux, reference curl, projector stress and tau/surface locks remain open", False),
        ("CERT2947_5_MHref_feed", "M_H_ref denominator", "M_H_ref may use H_tau only after theta/Q_tau and integrability certificates exist", "SCHEMA_READY", "positive same-frame H_tau-H_ref still missing", False),
        ("CERT2947_6_verdict", "theta/Qtau certificate", "parent theta_MTS and Q_tau_MTS are claim-grade for current MTS", "CERTIFICATE_NOT_DERIVED", "one parent current chain and sector charge closure are not signed", False),
    ]
    return [
        add_common(
            {
                "certificate_id": cert_id,
                "object": obj,
                "required_statement": statement,
                "current_status": status,
                "blocking_gap": gap,
                "certificate_passed": passed,
            }
        )
        for cert_id, obj, statement, status, gap, passed in rows
    ]


def sector_rows() -> list[dict[str, Any]]:
    rows = [
        ("SEC2947_0_EH_core", "EH core", "Theta_EH and Q_tau^EH", "CONDITIONAL_REFERENCE_ONLY", "requires MTS EH reduction and all non-EH pieces silent/exact"),
        ("SEC2947_1_matter_source", "ordinary matter/source", "Hilbert source current and matter constraint terms", "CONDITIONAL_UNSIGNED", "matter descent, source owner and no source-only prefactor still open"),
        ("SEC2947_2_kappa_topological", "kappa topological", "constant-coupling charge/silence clause", "CANDIDATE_NOT_ADOPTED", "parent topological sector not adopted with source blindness"),
        ("SEC2947_3_GK_q_loc", "Gamma/Khat/q_loc", "Theta_GK, Q_tau^GK, C_tau^GK", "MISSING_ACTION_EXISTENCE_STRONG", "weak action template exists but parent-owned A/Gamma/GK sector not signed"),
        ("SEC2947_4_domain_projector", "domain/P_loc/Pi_M", "projector stress and charge contribution", "NOT_PARENT_DERIVED", "projector variation and chain-map/flux closure remain active"),
        ("SEC2947_5_boundary_reference", "boundary/reference", "Q_tau^boundary + delta B_ref + H_ref", "FIXED_REFERENCE_MISSING", "source-blind fixed reference and no-flux theorem missing"),
        ("SEC2947_6_memory_response", "memory/response", "memory/doublet charge contribution or zero theorem", "PARTIAL_CANDIDATE_NOT_MATCHED", "component map and positive/silent operator not signed"),
        ("SEC2947_7_tau_surface", "tau/surface/readout", "same tau and linked surfaces before readout", "MISSING_TAU_SURFACE_LOCK", "source/charge/clock/orbit tau identity not parent-signed"),
        ("SEC2947_8_worldtube_glue", "worldtube source glue", "Hamiltonian charge equals dressed source measure", "CONDITIONAL_NOT_SIGNED", "source measure, compact support, PiM/Hilbert equality open"),
        ("SEC2947_9_total", "total sector certificate", "all sector charges sum with no unowned C_tau leakage", "TOTAL_CERTIFICATE_FAILS", "at least six core sector certificates remain unsigned"),
    ]
    return [
        add_common(
            {
                "sector_id": sector_id,
                "sector": sector,
                "required_charge_piece": piece,
                "status": status,
                "blocking_gap": gap,
                "sector_certificate_passed": False,
            }
        )
        for sector_id, sector, piece, status, gap in rows
    ]


def runner_rows() -> list[dict[str, Any]]:
    rows = [
        ("RUN2947_0_theta_Qtau", "theta_Qtau_certificate", "L_parent;sector_list;theta_MTS;Q_tau_MTS;C_tau_decomposition;boundary_terms;reference_terms;source_path;equation_ref;parent_signed;valid_for_claim", "MISSING_PARENT_THETA_QTAU", "claim only if every sector certificate passes"),
        ("RUN2947_1_MHref", "M_H_ref_first_row", "system_id;tau_id;coframe_id;surface_outer;H_tau;H_ref;M_H_ref;units;theta_Qtau_certificate;integrability_certificate;not_orbital_GM_imported;valid_for_claim", "MISSING_H_TAU_H_REF_MHREF", "positive same-frame parent source charge"),
        ("RUN2947_2_PiM_Hilbert", "PiM_Hilbert_equality", "PiM_definition;J_H_definition;surface_pair;homology_class;integral_value;M_H_ref_link;G_ref_link;source_path;valid_for_claim", "MISSING_HILBERT_TO_HTAU_MAP", "same-frame Hilbert/Hamiltonian equality"),
        ("RUN2947_3_integrability", "Htau_integrability", "omega_total;i_tau_omega;curl_delta_H_tau;reference_curl;projector_stress;boundary_flux;absolute_envelope;valid_for_claim", "MISSING_INTEGRABILITY_CERTIFICATE", "field-space closed Hamiltonian one-form or finite bound"),
        ("RUN2947_4_no_cancellation", "absolute_denominator_guard", "abs_terms;component_status;no_cancellation;no_EH_import;no_orbital_GM;valid_for_claim", "GUARD_READY_VALUES_MISSING", "all components theorem-zero or source-backed finite"),
    ]
    return [
        add_common(
            {
                "runner_row_id": row_id,
                "quantity": quantity,
                "required_columns": columns,
                "current_status": status,
                "acceptance_condition": acceptance,
            }
        )
        for row_id, quantity, columns, status, acceptance in rows
    ]


def curl_rows() -> list[dict[str, Any]]:
    rows = [
        ("CURL2947_0_delta_H_tau", "delta_H_tau_nonintegrable_over_MH", "field-space curl obstruction normalized by M_H_ref", "MISSING_INTEGRABILITY_NUMERIC_OR_THEOREM_ZERO"),
        ("CURL2947_1_omega_X", "omega_X_integral", "int_S i_tau omega_X(delta_1,delta_2)", "MISSING_THETA_OMEGA_SURFACE_INPUTS"),
        ("CURL2947_2_tau_surface", "tau_surface_variation_lock", "fixed tau and linked surfaces for curl test", "MISSING_TAU_SURFACE_VARIATION_LOCK"),
        ("CURL2947_3_reference", "reference_curl_over_MH", "curl induced by H_ref/reference subtraction", "MISSING_REFERENCE_CURL_ZERO_OR_BOUND"),
        ("CURL2947_4_projector", "projector_domain_stress_over_MH", "delta Pi_M/domain/Hodge stress contribution", "MISSING_PROJECTOR_STRESS_MAP"),
        ("CURL2947_5_envelope", "epsilon_Htau_curl_abs", "absolute sum of H_tau curl, reference, projector and boundary flux components", "COMPONENTS_MISSING_NONCLAIM"),
    ]
    return [
        add_common(
            {
                "curl_row_id": row_id,
                "component": component,
                "definition": definition,
                "status": status,
            }
        )
        for row_id, component, definition, status in rows
    ]


def guard_rows() -> list[dict[str, Any]]:
    rows = [
        ("GUARD2947_0_no_EH_import", "EH theta/Q_tau cannot be used as MTS theta/Q_tau without sector reduction", True),
        ("GUARD2947_1_no_orbital_GM", "orbital GM cannot define H_tau, H_ref, M_H_ref or Q_tau", True),
        ("GUARD2947_2_no_reference_fit", "H_ref/B_ref cannot be fitted after source/readout comparison", True),
        ("GUARD2947_3_no_silent_by_word", "extra sectors must be theorem-zero, exact, topological, or retained as residual rows", True),
        ("GUARD2947_4_no_cancellation", "opposite-sign denominator and flux residuals cannot be cancelled to pass a local test", True),
    ]
    return [
        add_common(
            {
                "guard_id": guard_id,
                "guard": guard,
                "guard_passed": passed,
            }
        )
        for guard_id, guard, passed in rows
    ]


def claim_rows() -> list[dict[str, Any]]:
    rows = [
        ("CG2947_0_theta_Qtau", "theta_MTS/Q_tau_MTS certificate passes", False, "CERTIFICATE_NOT_DERIVED", False),
        ("CG2947_1_Htau", "H_tau integrability and fixed reference pass", False, "INTEGRABILITY_REFERENCE_BLOCKED", False),
        ("CG2947_2_MHref", "M_H_ref denominator row valid", False, "FIRST_ROW_VALUES_MISSING", False),
        ("CG2947_3_PiM", "Pi_M/Hilbert/Hamiltonian equality passes", False, "PIM_EQUALITY_UNSIGNED", False),
        ("CG2947_4_Newton_GR", "Newton/local-GR reduction derived", False, "DENOMINATOR_ROOT_OPEN", False),
        ("CG2947_5_public_claim", "public claim allowed from 2947", False, "PRIVATE_NONCLAIM_CHECKPOINT", False),
    ]
    return [
        add_common(
            {
                "claim_gate_id": gate_id,
                "claim": claim,
                "condition_passed": passed,
                "status": status,
                "claim_allowed": allowed,
            }
        )
        for gate_id, claim, passed, status, allowed in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        ("DEC2947_0_result", "theta/Qtau certificate not closed", "one signed parent Lagrangian/current chain across all retained sectors is missing", "do not promote H_tau or M_H_ref"),
        ("DEC2947_1_gain", "missing charge pieces are now componentized", "sector matrix, first-row runner and H_tau curl residual rows identify exact gaps", "use these rows for the next root"),
        ("DEC2947_2_first_live_obstruction", "I_X/Q_tau_X is the first non-EH charge obstruction", "EH is only a reference; GK/domain/projector/boundary sectors remain unsigned", "attack parent current-chain sector action or I_X first row next"),
        ("DEC2947_3_guardrails", "charge import shortcuts remain blocked", "EH-only, orbital-GM, fitted reference and cancellation routes are refused", "keep nonclaim discipline"),
    ]
    return [
        add_common(
            {
                "decision_id": decision_id,
                "decision": decision,
                "reason": reason,
                "next_action": next_action,
            }
        )
        for decision_id, decision, reason, next_action in rows
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "next_id": "NEXT2947_0_2948",
                "priority": "selected_primary",
                "next_doc": "2948-Y5-R2FR-parent-current-chain-sector-action-certificate-or-IX-charge-residual-first-row-under-AX1090.md",
                "next_script": "scripts/Y5_R2FR_parent_current_chain_sector_action_certificate_or_IX_charge_residual_first_row_under_AX1090_2948.py",
                "objective": "Attack the first live non-EH charge obstruction: either certify the parent current-chain sector action pieces that supply Theta_X/Q_tau_X/C_tau_X for retained extra sectors, or emit a first-row residual for I_X/M_H_ref with units, source path, boundary/projector flux, and no-cancellation guard.",
                "include": "L_X;Theta_X;Q_tau_X;C_tau_X;GK/q_loc;projector/domain;boundary/reference;omega_X;I_X/M_H_ref;sector silence",
                "exclude": "EH-only import; saying extra sectors are silent by wording; measured orbital GM; local-GR/Newton/R10 claim; GitHub action; formalization-workbench edits",
            }
        )
    ]


def branch_rows() -> list[dict[str, Any]]:
    copies = [
        ("certificate_copy", OUTPUTS["certificate"], BRANCH_OUTPUTS["certificate_copy"]),
        ("sector_copy", OUTPUTS["sectors"], BRANCH_OUTPUTS["sector_copy"]),
        ("runner_copy", OUTPUTS["runner"], BRANCH_OUTPUTS["runner_copy"]),
        ("curl_copy", OUTPUTS["curl"], BRANCH_OUTPUTS["curl_copy"]),
        ("next_copy", OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"]),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source_path, copy_path in copies:
        if source_path.exists():
            shutil.copyfile(source_path, copy_path)
        rows.append(
            add_common(
                {
                    "copy_id": copy_id,
                    "source_path": str(source_path),
                    "copy_path": str(copy_path),
                    "source_exists": source_path.exists(),
                    "copy_exists": copy_path.exists(),
                }
            )
        )
    return rows


def validation_rows(source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    generated_csvs = [path for key, path in OUTPUTS.items() if key != "validation"]
    formalization_has_2947 = False
    if FORMALIZATION.exists():
        formalization_has_2947 = any(FORMALIZATION.rglob("*2947*"))
    certificate = read_csv_rows(OUTPUTS["certificate"])
    sectors = read_csv_rows(OUTPUTS["sectors"])
    runner = read_csv_rows(OUTPUTS["runner"])
    guards = read_csv_rows(OUTPUTS["guards"])
    claims = read_csv_rows(OUTPUTS["claims"])
    next_target = read_csv_rows(OUTPUTS["next"])
    checks = [
        ("VAL2947_0_sources_exist", all(row["path_exists"] for row in source_rows), "all cited local source paths exist", True),
        ("VAL2947_1_anchors_found", all(row["anchors_found"] for row in source_rows), "all source anchors found", True),
        ("VAL2947_2_certificate_attempted", any(row.get("certificate_id") == "CERT2947_6_verdict" for row in certificate), "theta/Qtau certificate verdict exists", True),
        ("VAL2947_3_certificate_not_claimed", any(row.get("certificate_id") == "CERT2947_6_verdict" and row.get("certificate_passed") == "False" for row in certificate), "theta/Qtau certificate remains nonclaim", True),
        ("VAL2947_4_sector_matrix", len(sectors) >= 10 and all(row.get("sector_certificate_passed") == "False" for row in sectors), "sector charge matrix emitted and nonclaim", True),
        ("VAL2947_5_runner_rows", len(runner) >= 5, "denominator first-row runner rows emitted", True),
        ("VAL2947_6_guards_passed", all(row.get("guard_passed") == "True" for row in guards), "charge import guards pass", True),
        ("VAL2947_7_claims_blocked", all(row.get("claim_allowed") == "False" for row in claims), "all claims blocked", True),
        ("VAL2947_8_next_target_selected", any(row.get("next_id") == "NEXT2947_0_2948" for row in next_target), "2948 current-chain/I_X target selected", True),
        ("VAL2947_9_branches_exist", all(path.exists() for path in BRANCH_OUTPUTS.values()), "branch copy files exist", True),
        ("VAL2947_10_csvs_parse", all(csv_parses(path) for path in generated_csvs), "all generated CSV files parse", True),
        ("VAL2947_11_outputs_under_post_checkpoint", all(is_under(path, ROOT) for path in [DOC, *OUTPUTS.values(), *BRANCH_OUTPUTS.values()]), "all generated outputs are under post-checkpoint-work", True),
        ("VAL2947_12_formalization_clean", not formalization_has_2947, "no 2947 outputs were written to formalization-workbench", True),
    ]
    overall = all(passed == required for _, passed, _, required in checks)
    rows = [{"validation_id": validation_id, "passed": passed, "check": check, "required": required} for validation_id, passed, check, required in checks]
    rows.append({"validation_id": "VAL2947_OVERALL", "passed": overall, "check": "2947 validation overall", "required": True})
    return rows


def write_doc(
    source_rows: list[dict[str, Any]],
    certificate: list[dict[str, Any]],
    sectors: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    curl: list[dict[str, Any]],
    guards: list[dict[str, Any]],
    claims: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    branches: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    overall = next(row for row in validation if row["validation_id"] == "VAL2947_OVERALL")["passed"]
    text = f"""# 2947 - Y5 R2FR: parent theta/Qtau MHref certificate or denominator first-row runner under AX1090

Status: `Y5_R2FR_2947_theta_Qtau_certificate_not_derived_denominator_runner_instantiated`

Claim ceiling: `no_Htau_no_MHref_no_PiM_source_charge_no_Newton_no_local_GR_no_R10_no_PPN_no_public_claim`

2947 attacks the earliest formal denominator root. The required parent charge chain is:

`delta L_parent = E_A delta Phi^A + d theta_MTS`

and

`J_tau = theta_MTS(L_tau Phi) - i_tau L_parent = dQ_tau^MTS + C_tau`.

The current corpus has the conditional Noether shape, but not the claim-grade MTS certificate. The obstruction is not philosophical: the EH charge is only a reference, and the retained MTS sectors do not yet have signed `Theta_s`, `Q_tau_s`, `C_tau_s`, boundary/reference, projector/domain, tau/surface and integrability certificates in one parent current chain.

## Source Register

{md_table(source_rows, ["source_id", "source_path", "path_exists", "anchors_found", "role"])}

## Theta/Q_tau Certificate Attempt

{md_table(certificate, ["certificate_id", "object", "required_statement", "current_status", "blocking_gap", "certificate_passed"])}

## Sector Charge Certificate Matrix

{md_table(sectors, ["sector_id", "sector", "required_charge_piece", "status", "blocking_gap", "sector_certificate_passed"])}

## MHref/PiM First-Row Runner Rows

{md_table(runner, ["runner_row_id", "quantity", "required_columns", "current_status", "acceptance_condition"])}

## H_tau Integrability Residual Rows

{md_table(curl, ["curl_row_id", "component", "definition", "status"])}

## Charge Import Guards

{md_table(guards, ["guard_id", "guard", "guard_passed"])}

## Claim Gates

{md_table(claims, ["claim_gate_id", "claim", "condition_passed", "status", "claim_allowed"])}

## Decision Ledger

{md_table(decisions, ["decision_id", "decision", "reason", "next_action"])}

## Next Target

{md_table(next_target, ["next_id", "priority", "next_doc", "next_script", "objective", "exclude"])}

## Branch Copies

{md_table(branches, ["copy_id", "source_path", "copy_path", "source_exists", "copy_exists", "valid_for_claim"])}

## Validation

{md_table(validation, ["validation_id", "passed", "check", "required"])}

Validation overall: `{overall}`.
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    source_rows = source_register_rows()
    write_csv(OUTPUTS["sources"], source_rows)

    certificate = certificate_rows()
    sectors = sector_rows()
    runner = runner_rows()
    curl = curl_rows()
    guards = guard_rows()
    claims = claim_rows()
    decisions = decision_rows()
    next_target = next_rows()

    write_csv(OUTPUTS["certificate"], certificate)
    write_csv(OUTPUTS["sectors"], sectors)
    write_csv(OUTPUTS["runner"], runner)
    write_csv(OUTPUTS["curl"], curl)
    write_csv(OUTPUTS["guards"], guards)
    write_csv(OUTPUTS["claims"], claims)
    write_csv(OUTPUTS["decision"], decisions)
    write_csv(OUTPUTS["next"], next_target)

    branches = branch_rows()
    write_csv(OUTPUTS["branches"], branches)

    validation = validation_rows(source_rows)
    write_csv(OUTPUTS["validation"], validation)

    write_doc(source_rows, certificate, sectors, runner, curl, guards, claims, decisions, next_target, branches, validation)

    overall = next(row for row in validation if row["validation_id"] == "VAL2947_OVERALL")["passed"]
    print(f"2947 validation overall: {overall}")
    print(DOC)


if __name__ == "__main__":
    main()
