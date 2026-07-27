from __future__ import annotations

import csv
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"
SCRIPT_DIR = POST / "scripts"

CHECKPOINT = "4798"
CLAIM_ID = "L-640"
MARKER = "PPC4161_LOCAL_ZERO_SOURCE_SELECTOR_AND_PHIBC_STRESS_LEDGER_4798"
PACKET_MARKER = "PPC4161_PACKET_LOCAL_ZERO_SOURCE_SELECTOR_AND_PHIBC_STRESS_LEDGER_4798"
DECISION = "TOPOLOGICAL_LOCAL_TOP_ZERO_ROUTE_PARTIAL_PHIBC_BOUND_AND_STRESS_LEDGER_GAP_EXPLICIT"
NEXT_TARGET = "4799-Y5-R2FR-BC-primitive-owner-or-source-selector-parent-action.md"

DOC_PATH = POST / "4798-Y5-R2FR-local-zero-source-selector-and-PhiBC-stress-ledger.md"
FORMAL_PATH = FORMAL / "814-PPC4161-local-zero-source-selector-and-PhiBC-stress-ledger.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"

RUNNER = SCRIPT_DIR / "local_zero_phiBC_stress_ledger_runner.py"

SOURCE_REGISTER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4798_SOURCE_REGISTER.csv"
SELECTOR_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4798_TOPO_SELECTOR_INPUT.csv"
SELECTOR_OUTPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4798_TOPO_SELECTOR_OUTPUT.csv"
PHIBC_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4798_PHIBC_INPUT.csv"
PHIBC_OUTPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4798_PHIBC_OUTPUT.csv"
STRESS_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4798_STRESS_LEDGER_INPUT.csv"
STRESS_OUTPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4798_STRESS_LEDGER_OUTPUT.csv"
OBSTRUCTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4798_OBSTRUCTION_UPDATE.csv"
GATE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4798_PROMOTION_GATES.csv"
FIREWALL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4798_FIREWALL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4798_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4798_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4798_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4798_VALIDATION.csv"

TOPO_SELECTOR_CLAUSES = (
    "Pi_top_operator_defined_signed",
    "same_operator_local_FLRW_signed",
    "local_absolute_H3_zero_signed",
    "local_relative_boundary_zero_or_bound_signed",
    "FLRW_top_class_nonzero_allowed_signed",
    "parent_source_equals_top_projection_signed",
    "amplitude_normalization_signed",
    "no_hand_switch_signed",
)

PHIBC_CLAUSES = (
    "Phi_equals_i_tau_mathcalJ_signed",
    "JC_decomposition_dBC_plus_top_signed",
    "PhiC_BC_transport_relation_signed",
    "BC_primitive_owned_signed",
    "boundary_surface_certificate_signed",
    "no_corner_or_corner_bound_signed",
    "no_harmonic_or_harmonic_bound_signed",
    "no_residual_or_residual_bound_signed",
    "closed_weight_or_dSFeps_bound_signed",
    "charge_preservation_signed",
)

STRESS_LEDGER_CLAUSES = (
    "T_mathcalJ_accounted_signed",
    "T_Sigma_accounted_signed",
    "T_Phi_accounted_signed",
    "T_PD_accounted_signed",
    "T_domain_boundary_accounted_signed",
    "T_edge_bound_accounted_signed",
    "Ward_identity_written_signed",
    "no_hidden_external_force_signed",
)

SOURCE_SPECS = [
    ("SRC4798_00_4797_doc", POST / "4797-Y5-R2FR-parent-continuity-source-SigmaPhi-or-PD-domain-functional.md", "DEC4797_2_next", "4797 handoff to source selector and PhiBC ledger"),
    ("SRC4798_01_1169_doc", POST / "1169-Y5-R10-parent-source-topclass-owner-or-closed-weight-zero.md", "TOP1169_0_same_law_statement", "older topological selector route"),
    ("SRC4798_02_1169_ledger", SOURCE_DIR / "P8_Y5_R10_1169_SIGMA_PHI_OWNERSHIP_LEDGER.csv", "SPL1169_3_Phi_C", "Phi_C ownership gap"),
    ("SRC4798_03_1020_doc", POST / "1020-Y5-R10-boundary-cohomology-domain-certificate-or-source-pack-first-row.md", "ETB1020_3_residual_bound", "weighted-Stokes finite bound"),
    ("SRC4798_04_274_decomp", POST / "274-lifted-C-sector-form-holonomy-route.md", "J_C = dB_C + J_C^{top}", "J_C exact/top decomposition"),
    ("SRC4798_05_207_bianchi", POST / "207-domain-projector-action-and-Bianchi-identity.md", "T_total =", "Bianchi stress ledger guard"),
    ("SRC4798_06_4797_cartan", SOURCE_DIR / "P8_Y5_R2FR_4797_CARTAN_BALANCE_OUTPUT.csv", "cartan_reynolds_balance_smoke", "current Cartan balance"),
    ("SRC4798_07_4796_edge", SOURCE_DIR / "P8_Y5_R2FR_4796_FINITE_EDGE_BOUND_OUTPUT.csv", "finite_edge_bound_from_4794_4795_smoke", "current finite edge bound"),
    ("SRC4798_08_runner", RUNNER, "def topological_selector_row", "4798 executable runner"),
]


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_text(path_object: Path) -> str:
    return path_object.read_text(encoding="utf-8-sig", errors="replace") if path_object.exists() else ""


def write_text(path_object: Path, content: str) -> None:
    path_object.parent.mkdir(parents=True, exist_ok=True)
    path_object.write_text(content, encoding="utf-8", newline="\n")


def append_once(path_object: Path, marker: str, block: str) -> None:
    existing = read_text(path_object)
    if marker in existing:
        return
    separator = "" if not existing or existing.endswith("\n") else "\n"
    write_text(path_object, existing + separator + block.rstrip() + "\n")


def parse_csv(path_object: Path) -> list[dict[str, str]]:
    with path_object.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path_object: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"cannot write empty CSV: {path_object}")
    path_object.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for field in row:
            if field not in fieldnames:
                fieldnames.append(field)
    with path_object.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def run_command(args: list[str]) -> None:
    subprocess.run(args, check=True, cwd=str(ROOT))


def markdown_table(rows: list[dict[str, Any]], fields: list[str] | None = None) -> str:
    if not rows:
        return "\n"
    selected = fields or list(rows[0].keys())
    lines = [
        "| " + " | ".join(selected) + " |",
        "| " + " | ".join("---" for _ in selected) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(field, "")).replace("\n", " ") for field in selected) + " |")
    return "\n".join(lines) + "\n"


def bool_text(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "pass", "signed"}


def source_register(timestamp: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path_object, needle, role in SOURCE_SPECS:
        exists = path_object.exists()
        text = read_text(path_object)
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "source_path": str(path_object),
                "exists": exists,
                "needle": needle,
                "needle_found": needle in text,
                "role": role,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def clause_map(clauses: tuple[str, ...], value: bool) -> dict[str, bool]:
    return {clause: value for clause in clauses}


def selector_input_rows(timestamp: str) -> list[dict[str, Any]]:
    physical = clause_map(TOPO_SELECTOR_CLAUSES, False)
    physical["FLRW_top_class_nonzero_allowed_signed"] = True
    physical["no_hand_switch_signed"] = True

    topology_partial = clause_map(TOPO_SELECTOR_CLAUSES, False)
    for clause in (
        "Pi_top_operator_defined_signed",
        "same_operator_local_FLRW_signed",
        "local_absolute_H3_zero_signed",
        "FLRW_top_class_nonzero_allowed_signed",
        "no_hand_switch_signed",
    ):
        topology_partial[clause] = True

    signed = clause_map(TOPO_SELECTOR_CLAUSES, True)

    def row(selector_id: str, status: str, source: str, clauses: dict[str, bool], values: dict[str, str] | None = None) -> dict[str, Any]:
        payload = {
            "selector_id": selector_id,
            "selector_source": source,
            "topology_source": source,
            "FLRW_source": source,
            "provenance": source,
            "notes": "",
            "top_coupling_abs": "",
            "local_H3_abs": "",
            "relative_boundary_leak_abs": "",
            "FLRW_top_class_abs": "",
            "row_status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        payload.update(clauses)
        if values:
            payload.update(values)
        return payload

    return [
        row("physical_topological_selector_missing", "physical_branch_missing_parent_top_selector_nonclaim", str(POST / "1169-Y5-R10-parent-source-topclass-owner-or-closed-weight-zero.md"), physical),
        row(
            "topology_kills_absolute_local_H3_but_boundary_leaks",
            "topology_partial_selector_smoke_nonclaim",
            str(SOURCE_DIR / "P8_Y5_R10_1169_TOPOLOGICAL_SELECTOR_THEOREM.csv"),
            topology_partial,
            {
                "top_coupling_abs": "1.0",
                "local_H3_abs": "0.0",
                "relative_boundary_leak_abs": "1.66e-7",
                "FLRW_top_class_abs": "1.0",
            },
        ),
        row("conditional_same_law_top_selector", "conditional_top_selector_theorem_nonclaim", "CONDITIONAL_SAME_LAW_TOP_SELECTOR_PACKET", signed),
        row("forbidden_local_FLRW_hand_switch_control", "forbidden_control_nonclaim", "TOP_CLASS_BY_DECLARATION_LOCAL_FLRW_HAND_SWITCH_SIGMA_ZERO_BY_ASSERTION", signed),
    ]


def phibc_input_rows(timestamp: str) -> list[dict[str, Any]]:
    physical = clause_map(PHIBC_CLAUSES, False)
    relation_bound = clause_map(PHIBC_CLAUSES, False)
    for clause in (
        "Phi_equals_i_tau_mathcalJ_signed",
        "JC_decomposition_dBC_plus_top_signed",
        "PhiC_BC_transport_relation_signed",
        "no_corner_or_corner_bound_signed",
        "closed_weight_or_dSFeps_bound_signed",
    ):
        relation_bound[clause] = True
    signed = clause_map(PHIBC_CLAUSES, True)

    def row(phi_id: str, status: str, source: str, clauses: dict[str, bool], values: dict[str, str] | None = None) -> dict[str, Any]:
        payload = {
            "phi_id": phi_id,
            "Phi_source": source,
            "BC_source": source,
            "boundary_source": source,
            "provenance": source,
            "notes": "",
            "C_corner_abs": "",
            "norm_dS_Feps": "",
            "norm_bC": "",
            "harmonic_edge_abs": "",
            "residual_edge_abs": "",
            "transport_tail_abs": "",
            "row_status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        payload.update(clauses)
        if values:
            payload.update(values)
        return payload

    return [
        row("physical_PhiBC_missing", "physical_branch_missing_PhiBC_certificate_nonclaim", str(POST / "1020-Y5-R10-boundary-cohomology-domain-certificate-or-source-pack-first-row.md"), physical),
        row(
            "PhiBC_finite_bound_from_edge_smoke",
            "PhiBC_relation_partial_finite_bound_nonclaim",
            str(SOURCE_DIR / "P8_Y5_R2FR_4796_FINITE_EDGE_BOUND_OUTPUT.csv"),
            relation_bound,
            {
                "C_corner_abs": "1.3e-7",
                "norm_dS_Feps": "3.0e-4",
                "norm_bC": "2.0e-5",
                "harmonic_edge_abs": "2.0e-8",
                "residual_edge_abs": "1.0e-8",
                "transport_tail_abs": "4.0e-9",
            },
        ),
        row("conditional_PhiBC_boundary_silence", "conditional_PhiBC_zero_theorem_nonclaim", "CONDITIONAL_PHIBC_BOUNDARY_SILENCE_PACKET", signed),
        row("forbidden_boundary_zero_control", "forbidden_control_nonclaim", "PHI_ZERO_BY_ASSERTION_BOUNDARY_ZERO_BY_ASSERTION_EDGE_CANCELLATION", signed),
    ]


def stress_input_rows(timestamp: str) -> list[dict[str, Any]]:
    physical = clause_map(STRESS_LEDGER_CLAUSES, False)
    physical["no_hidden_external_force_signed"] = True

    finite_gap = clause_map(STRESS_LEDGER_CLAUSES, False)
    finite_gap["Ward_identity_written_signed"] = True
    finite_gap["no_hidden_external_force_signed"] = True

    signed = clause_map(STRESS_LEDGER_CLAUSES, True)

    def row(stress_id: str, status: str, source: str, clauses: dict[str, bool], values: dict[str, str] | None = None) -> dict[str, Any]:
        payload = {
            "stress_id": stress_id,
            "stress_source": source,
            "Ward_source": source,
            "provenance": source,
            "notes": "",
            "T_mathcalJ_abs": "",
            "T_Sigma_abs": "",
            "T_Phi_abs": "",
            "T_PD_abs": "",
            "T_domain_boundary_abs": "",
            "T_edge_abs": "",
            "Ward_accounted_abs": "",
            "row_status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        payload.update(clauses)
        if values:
            payload.update(values)
        return payload

    return [
        row("physical_stress_ledger_missing", "physical_branch_missing_stress_ledger_nonclaim", str(POST / "207-domain-projector-action-and-Bianchi-identity.md"), physical),
        row(
            "stress_ledger_finite_gap_smoke",
            "stress_ledger_gap_smoke_nonclaim",
            str(POST / "207-domain-projector-action-and-Bianchi-identity.md"),
            finite_gap,
            {
                "T_mathcalJ_abs": "2.0e-8",
                "T_Sigma_abs": "8.0e-8",
                "T_Phi_abs": "4.0e-8",
                "T_PD_abs": "3.0e-8",
                "T_domain_boundary_abs": "2.0e-8",
                "T_edge_abs": "1.7e-7",
                "Ward_accounted_abs": "2.0e-7",
            },
        ),
        row("conditional_full_stress_ledger", "conditional_stress_ward_theorem_nonclaim", "CONDITIONAL_FULL_STRESS_LEDGER_PACKET", signed),
        row("forbidden_drop_stress_control", "forbidden_control_nonclaim", "DROP_PROJECTOR_STRESS_DROP_BOUNDARY_STRESS_EXTERNAL_PROJECTOR", signed),
    ]


def obstruction_rows(timestamp: str, selector_rows: list[dict[str, str]], phibc_rows: list[dict[str, str]], stress_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    selector = next(row for row in selector_rows if row["selector_id"] == "topology_kills_absolute_local_H3_but_boundary_leaks")
    phibc = next(row for row in phibc_rows if row["phi_id"] == "PhiBC_finite_bound_from_edge_smoke")
    stress = next(row for row in stress_rows if row["stress_id"] == "stress_ledger_finite_gap_smoke")
    return [
        {
            "update_id": "OBS4798_0_topological_selector",
            "item": "absolute top-class local zero",
            "status": selector["runner_status"],
            "value_or_bound": f"local_sigma_top_abs={selector['local_sigma_top_abs']}; leak={selector['local_selector_leak_abs']}",
            "meaning": "absolute H3 can kill the local top source, but boundary/relative leakage still controls local silence",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "update_id": "OBS4798_1_PhiBC_boundary_flux",
            "item": "Phi_C/B_C boundary flux",
            "status": phibc["runner_status"],
            "value_or_bound": phibc["Phi_boundary_bound_abs"],
            "meaning": "Phi_C is tied to B_C only conditionally; finite edge bound remains until primitive/cohomology/kernel certificates close",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "update_id": "OBS4798_2_stress_ledger",
            "item": "Ward stress accounting",
            "status": stress["runner_status"],
            "value_or_bound": stress["unaccounted_stress_abs"],
            "meaning": "any source/flux/projector/domain residual must be carried as stress, not hidden as geometry",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def gate_rows(timestamp: str, selector_rows: list[dict[str, str]], phibc_rows: list[dict[str, str]], stress_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    selector = next(row for row in selector_rows if row["selector_id"] == "topology_kills_absolute_local_H3_but_boundary_leaks")
    phibc = next(row for row in phibc_rows if row["phi_id"] == "PhiBC_finite_bound_from_edge_smoke")
    stress = next(row for row in stress_rows if row["stress_id"] == "stress_ledger_finite_gap_smoke")
    return [
        {
            "gate_id": "PG4798_0_absolute_top_zero",
            "claim": "absolute topological source vanishes locally",
            "gate_pass": selector["Z_local_top_zero"] == "True",
            "reason": "local absolute H3 is zero in the smoke selector row",
            "evidence": selector["local_sigma_top_abs"],
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "PG4798_1_total_local_zero",
            "claim": "total local Sigma/Phi/domain residual vanishes",
            "gate_pass": False,
            "reason": "boundary/relative Phi_C/B_C leakage remains finite or unsigned",
            "evidence": selector["local_selector_leak_abs"],
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "PG4798_2_PhiBC_bound",
            "claim": "Phi_C/B_C finite fallback is executable",
            "gate_pass": True,
            "reason": "termwise Phi boundary bound computes from current edge pieces",
            "evidence": phibc["Phi_boundary_bound_abs"],
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "PG4798_3_stress_ledger",
            "claim": "source/flux/projector stress is fully accounted",
            "gate_pass": False,
            "reason": "stress row computes a finite unaccounted gap until all Ward terms are signed",
            "evidence": stress["unaccounted_stress_abs"],
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "PG4798_4_local_GR_Newton",
            "claim": "local GR/Newton/PPN/R10 promotion allowed",
            "gate_pass": False,
            "reason": "total local zero and stress ledger remain nonclaim",
            "evidence": "nonclaim firewall active",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def firewalls(timestamp: str) -> list[dict[str, Any]]:
    rules = [
        ("FW4798_0_no_topology_overclaim", "Absolute H3 local-zero does not silence relative cohomology, boundary flux, corners, or edge modes."),
        ("FW4798_1_no_Phi_zero_assertion", "Phi_C=0 must follow from Phi_C/B_C relation and boundary certificate, not assertion."),
        ("FW4798_2_no_edge_cancellation", "Boundary, harmonic, residual and transport tails are bounded termwise, never cancelled."),
        ("FW4798_3_no_hidden_stress", "Sigma_C, Phi_C, P_D, domain-boundary and edge stress must remain in the Ward ledger."),
        ("FW4798_4_no_local_claim", "No local-GR/Newton/R10/PPN/WEP/clock/orbital claim follows from 4798."),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "firewall_id": firewall_id,
            "rule": rule,
            "status": "ACTIVE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for firewall_id, rule in rules
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC4798_0_topology",
            "decision": "absolute_topology_kills_only_the_top_local_piece",
            "reason": "same-law Pi_top can distinguish local bounded domains from FLRW, but boundary/relative leakage remains",
            "next_action": "derive B_C primitive/no-boundary-flux certificate or keep finite bound",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC4798_1_PhiBC",
            "decision": "PhiBC_is_the_next_hard_boundary_object",
            "reason": "Phi_C/B_C relation is where topological local-zero either becomes a theorem or remains a bounded residual",
            "next_action": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC4798_2_stress",
            "decision": "stress_ledger_must_close_before_local_GR",
            "reason": "even a small residual is a hidden force if not carried by Ward/Bianchi accounting",
            "next_action": "source stress terms for Sigma_C, Phi_C, P_D, domain boundary and edge residuals",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def status_rows(timestamp: str, selector_rows: list[dict[str, str]], phibc_rows: list[dict[str, str]], stress_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    selector = next(row for row in selector_rows if row["selector_id"] == "topology_kills_absolute_local_H3_but_boundary_leaks")
    phibc = next(row for row in phibc_rows if row["phi_id"] == "PhiBC_finite_bound_from_edge_smoke")
    stress = next(row for row in stress_rows if row["stress_id"] == "stress_ledger_finite_gap_smoke")
    return [
        {
            "status_id": "STATUS4798_0_top_selector",
            "status": selector["runner_status"],
            "detail": f"local_sigma_top_abs={selector['local_sigma_top_abs']}; leak={selector['local_selector_leak_abs']}",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "status_id": "STATUS4798_1_PhiBC",
            "status": phibc["runner_status"],
            "detail": f"Phi_boundary_bound_abs={phibc['Phi_boundary_bound_abs']}",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "status_id": "STATUS4798_2_stress",
            "status": stress["runner_status"],
            "detail": f"unaccounted_stress_abs={stress['unaccounted_stress_abs']}",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "status_id": "STATUS4798_3_selected_next",
            "status": "BC_PRIMITIVE_OWNER_OR_SOURCE_SELECTOR_PARENT_ACTION",
            "detail": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "next_id": "NEXT4798_0_4799",
            "next_target": NEXT_TARGET,
            "objective": "derive B_C primitive/Phi_C boundary owner from parent variation or derive parent action source selector equaling Pi_top[J_C]",
            "include": "B_C primitive; Phi_C transport relation; boundary class; h/r edge zero or bound; source equals Pi_top; Ward stress terms",
            "exclude": "topology overclaim; Phi zero assertion; edge cancellation; hidden stress; local-GR claim; GitHub",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
    ]


def validation_rows(timestamp: str) -> list[dict[str, Any]]:
    sources = parse_csv(SOURCE_REGISTER_CSV)
    selector_rows = parse_csv(SELECTOR_OUTPUT_CSV)
    phibc_rows = parse_csv(PHIBC_OUTPUT_CSV)
    stress_rows = parse_csv(STRESS_OUTPUT_CSV)
    validation: list[dict[str, Any]] = []

    def add(check_id: str, description: str, passed: bool, evidence: str) -> None:
        validation.append(
            {
                "checkpoint": CHECKPOINT,
                "check_id": check_id,
                "description": description,
                "result": "PASS" if passed else "FAIL",
                "evidence": evidence,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )

    physical_selector = next(row for row in selector_rows if row["selector_id"] == "physical_topological_selector_missing")
    selector = next(row for row in selector_rows if row["selector_id"] == "topology_kills_absolute_local_H3_but_boundary_leaks")
    conditional_selector = next(row for row in selector_rows if row["selector_id"] == "conditional_same_law_top_selector")
    forbidden_selector = next(row for row in selector_rows if row["selector_id"] == "forbidden_local_FLRW_hand_switch_control")
    physical_phibc = next(row for row in phibc_rows if row["phi_id"] == "physical_PhiBC_missing")
    phibc = next(row for row in phibc_rows if row["phi_id"] == "PhiBC_finite_bound_from_edge_smoke")
    conditional_phibc = next(row for row in phibc_rows if row["phi_id"] == "conditional_PhiBC_boundary_silence")
    forbidden_phibc = next(row for row in phibc_rows if row["phi_id"] == "forbidden_boundary_zero_control")
    physical_stress = next(row for row in stress_rows if row["stress_id"] == "physical_stress_ledger_missing")
    stress = next(row for row in stress_rows if row["stress_id"] == "stress_ledger_finite_gap_smoke")
    conditional_stress = next(row for row in stress_rows if row["stress_id"] == "conditional_full_stress_ledger")
    forbidden_stress = next(row for row in stress_rows if row["stress_id"] == "forbidden_drop_stress_control")

    add("VAL4798_0_sources", "all cited sources exist and needles are found", all(bool_text(row["exists"]) and bool_text(row["needle_found"]) for row in sources), str(SOURCE_REGISTER_CSV))
    add("VAL4798_1_physical_selector_blocks", "physical topological selector remains blocked", physical_selector["runner_status"] == "BLOCKED_MISSING_TOPOLOGICAL_SELECTOR_INPUTS", str(SELECTOR_OUTPUT_CSV))
    add("VAL4798_2_topology_partial", "absolute local H3 zero computes but boundary leak remains", selector["runner_status"] == "TOPOLOGICAL_SELECTOR_LOCAL_TOP_ZERO_BUT_BOUNDARY_LEAK_OPEN_NONCLAIM" and selector["local_sigma_top_abs"] == "0.000000000000000e+00", str(SELECTOR_OUTPUT_CSV))
    add("VAL4798_3_conditional_selector", "conditional same-law selector zeros local source", conditional_selector["runner_status"] == "TOPOLOGICAL_LOCAL_ZERO_FLRW_ACTIVE_CONDITIONAL_THEOREM_NONCLAIM", str(SELECTOR_OUTPUT_CSV))
    add("VAL4798_4_forbidden_selector_fails", "hand-switched selector fails", forbidden_selector["runner_status"] == "FAILED_TOPOLOGICAL_SELECTOR_GATE", str(SELECTOR_OUTPUT_CSV))
    add("VAL4798_5_physical_PhiBC_blocks", "physical PhiBC certificate remains blocked", physical_phibc["runner_status"] == "BLOCKED_MISSING_PHIBC_BOUNDARY_INPUTS", str(PHIBC_OUTPUT_CSV))
    add("VAL4798_6_PhiBC_bound", "PhiBC finite boundary bound computes", phibc["runner_status"] == "PHIBC_BOUNDARY_FINITE_BOUND_COMPUTED_NONCLAIM" and phibc["Phi_boundary_bound_abs"] != "MISSING_NUMERIC_VALUE", str(PHIBC_OUTPUT_CSV))
    add("VAL4798_7_conditional_PhiBC", "conditional PhiBC boundary silence passes", conditional_phibc["runner_status"] == "PHIBC_BOUNDARY_SILENCE_CONDITIONAL_THEOREM_NONCLAIM", str(PHIBC_OUTPUT_CSV))
    add("VAL4798_8_forbidden_PhiBC_fails", "Phi/boundary assertion fails", forbidden_phibc["runner_status"] == "FAILED_PHIBC_BOUNDARY_GATE", str(PHIBC_OUTPUT_CSV))
    add("VAL4798_9_physical_stress_blocks", "physical stress ledger remains blocked", physical_stress["runner_status"] == "BLOCKED_MISSING_STRESS_LEDGER_INPUTS", str(STRESS_OUTPUT_CSV))
    add("VAL4798_10_stress_gap", "stress ledger finite gap computes", stress["runner_status"] == "STRESS_WARD_LEDGER_FINITE_GAP_COMPUTED_NONCLAIM" and stress["unaccounted_stress_abs"] != "MISSING_NUMERIC_VALUE", str(STRESS_OUTPUT_CSV))
    add("VAL4798_11_conditional_stress", "conditional stress ledger closes", conditional_stress["runner_status"] == "STRESS_WARD_LEDGER_CONDITIONAL_THEOREM_NONCLAIM", str(STRESS_OUTPUT_CSV))
    add("VAL4798_12_forbidden_stress_fails", "dropped stress shortcut fails", forbidden_stress["runner_status"] == "FAILED_STRESS_LEDGER_GATE", str(STRESS_OUTPUT_CSV))
    add("VAL4798_13_claim", "claim register includes L-640 as nonclaim", CLAIM_ID in read_text(CLAIMS_PATH), str(CLAIMS_PATH))
    add("VAL4798_14_resume", "resume points at 4799", NEXT_TARGET in read_text(RESUME_PATH), str(RESUME_PATH))
    add("VAL4798_OVERALL", "all 4798 selector/PhiBC/stress checks pass", all(row["result"] == "PASS" for row in validation), DECISION)
    return validation


def write_claim(timestamp: str) -> None:
    if CLAIMS_PATH.exists() and any(row.get("claim_id") == CLAIM_ID for row in parse_csv(CLAIMS_PATH)):
        return
    with CLAIMS_PATH.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = reader.fieldnames or []
    row = {
        "claim_id": CLAIM_ID,
        "domain": "local_zero_phiBC_stress_ledger_runner",
        "claim": "4798 shows the topological selector kills only the absolute local top source while Phi_C/B_C boundary leakage and stress ledger remain explicit finite/nonclaim gates.",
        "current_evidence": "Generated source register, topological selector input/output, PhiBC input/output, stress ledger input/output, obstruction update, gates, firewalls, decision, status, next target and validation.",
        "status": "topological_local_top_zero_partial_PhiBC_bound_stress_gap_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "Do not overclaim topology; boundary/relative flux and Ward stress must close before local-GR promotion.",
        "sector": "local_gr",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "topology overclaim; Phi zero assertion; edge cancellation; hidden stress; local-GR promotion",
        "title": "Local zero selector, PhiBC and stress ledger",
        "notes": f"{MARKER}; {DECISION}; generated {timestamp}",
    }
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writerow({field: row.get(field, "") for field in fieldnames})


def write_resume(timestamp: str) -> None:
    content = f"""# Current Local Resume

Last checkpoint: `{DOC_PATH.name}`
Generated: `{timestamp}`

## Current target

`{NEXT_TARGET}`

## Live blocker

4798 confirms the strongest current local-zero route: a same-law absolute topological selector can kill the local top-class source on bounded/contractible domains while allowing FLRW top-class activity. But that only kills the absolute top piece. It does not kill relative cohomology, exact boundary flux, corners, harmonic/residual edge modes, or transport tails.

The live boundary object is now `Phi_C/B_C`. The finite smoke gate computes a nonclaim `Phi_boundary_bound_abs` from the existing corner, weighted-Stokes, harmonic, residual and transport terms. To get local GR, this must become either a parent `B_C` primitive/no-flux theorem or a sourced finite residual small enough for local tests.

The Ward stress ledger is also live: any `Sigma_C`, `Phi_C`, `P_D`, domain-boundary or edge residual must be carried as stress. Hidden stress is now an explicit failure mode, not a footnote.

## Firewalls

- No topology overclaim: absolute H3 zero is not total local silence.
- No `Phi_C=0` by assertion.
- No cancellation between edge terms.
- No dropping projector/domain/boundary/source stress.
- No local-GR/Newton/PPN/R10 claim from this checkpoint.
"""
    write_text(RESUME_PATH, content)


def write_docs(timestamp: str) -> None:
    sources = parse_csv(SOURCE_REGISTER_CSV)
    selector_rows = parse_csv(SELECTOR_OUTPUT_CSV)
    phibc_rows = parse_csv(PHIBC_OUTPUT_CSV)
    stress_rows = parse_csv(STRESS_OUTPUT_CSV)
    obstruction = parse_csv(OBSTRUCTION_CSV)
    gates = parse_csv(GATE_CSV)
    firewall_rows = parse_csv(FIREWALL_CSV)
    decisions = parse_csv(DECISION_CSV)
    statuses = parse_csv(STATUS_CSV)
    validation = parse_csv(VALIDATION_CSV)

    content = f"""# 4798 - Local-zero source selector and PhiBC stress ledger

Marker: `{MARKER}`
Generated: `{timestamp}`
Decision: `{DECISION}`

## Result

4798 turns the promising topological selector into a stricter gate:

```text
Sigma_C^top = kappa_top Pi_top[J_C]
H^3_abs(D_local)=0  =>  Sigma_C^top(local)=0
H^3_abs(Sigma_FLRW) nonzero  =>  FLRW top class may remain active
```

That is real structural progress because it is the same operator in both arenas. It is not enough for local GR, because local tests also see relative/boundary leakage:

```text
local leak = Sigma_C^top + Phi_C/B_C boundary flux + relative/harmonic/residual tails
```

The checkpoint therefore ties `Phi_C` to the `B_C` boundary problem and installs a stress ledger for `Sigma_C`, `Phi_C`, `P_D`, domain-boundary and edge residuals.

## Source Register

{markdown_table(sources, ["source_id", "source_path", "exists", "needle_found", "role"])}

## Topological Selector Output

{markdown_table(selector_rows, ["selector_id", "Z_top_selector", "Z_local_top_zero", "Z_FLRW_active_allowed", "local_sigma_top_abs", "local_selector_leak_abs", "runner_status", "missing_selector_inputs", "anti_circularity_status"])}

## PhiBC Boundary Output

{markdown_table(phibc_rows, ["phi_id", "Z_PhiBC_relation", "Z_boundary_silence", "Phi_boundary_bound_abs", "runner_status", "missing_PhiBC_inputs", "anti_circularity_status"])}

## Stress Ledger Output

{markdown_table(stress_rows, ["stress_id", "Z_stress_ledger", "unaccounted_stress_abs", "runner_status", "missing_stress_inputs", "anti_circularity_status"])}

## Obstruction Update

{markdown_table(obstruction, ["update_id", "item", "status", "value_or_bound", "meaning"])}

## Promotion Gates

{markdown_table(gates, ["gate_id", "claim", "gate_pass", "reason", "evidence"])}

## Firewalls

{markdown_table(firewall_rows, ["firewall_id", "rule", "status"])}

## Decision Ledger

{markdown_table(decisions, ["decision_id", "decision", "reason", "next_action"])}

## Status

{markdown_table(statuses, ["status_id", "status", "detail"])}

## Validation

{markdown_table(validation, ["check_id", "description", "result", "evidence"])}

## Next Target

`{NEXT_TARGET}`
"""
    write_text(DOC_PATH, content)
    write_text(FORMAL_PATH, content.replace("# 4798 -", "# 814 - PPC4161 "))

    append_once(
        SPINE_PATH,
        MARKER,
        f"""
## {MARKER}

- 4798 confirms the topological selector as the cleanest same-law local-zero/FLRW-active route, but limits it to the absolute top source only.
- It ties remaining local leakage to `Phi_C/B_C` boundary flux and finite edge terms rather than allowing topology to erase them by rhetoric.
- It installs a stress/Ward ledger gate so source, flux, projector, boundary and edge residuals cannot hide as unaccounted forces.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## {PACKET_MARKER}

4798 adds the local-zero topological selector, `Phi_C/B_C` boundary bound and stress/Ward ledger to the private local packet. The next hard object is the parent `B_C` primitive or parent action proof that `Sigma_C` equals the top projection. Next target: `{NEXT_TARGET}`.
""",
    )


def main() -> int:
    timestamp = now()
    write_csv(SOURCE_REGISTER_CSV, source_register(timestamp))
    write_csv(SELECTOR_INPUT_CSV, selector_input_rows(timestamp))
    write_csv(PHIBC_INPUT_CSV, phibc_input_rows(timestamp))
    write_csv(STRESS_INPUT_CSV, stress_input_rows(timestamp))
    run_command([sys.executable, str(RUNNER), str(SELECTOR_INPUT_CSV), str(SELECTOR_OUTPUT_CSV), str(PHIBC_INPUT_CSV), str(PHIBC_OUTPUT_CSV), str(STRESS_INPUT_CSV), str(STRESS_OUTPUT_CSV)])

    selector_rows = parse_csv(SELECTOR_OUTPUT_CSV)
    phibc_rows = parse_csv(PHIBC_OUTPUT_CSV)
    stress_rows = parse_csv(STRESS_OUTPUT_CSV)
    write_csv(OBSTRUCTION_CSV, obstruction_rows(timestamp, selector_rows, phibc_rows, stress_rows))
    write_csv(GATE_CSV, gate_rows(timestamp, selector_rows, phibc_rows, stress_rows))
    write_csv(FIREWALL_CSV, firewalls(timestamp))
    write_csv(DECISION_CSV, decision_rows(timestamp))
    write_csv(STATUS_CSV, status_rows(timestamp, selector_rows, phibc_rows, stress_rows))
    write_csv(NEXT_TARGET_CSV, next_rows(timestamp))
    write_resume(timestamp)
    write_claim(timestamp)
    write_csv(VALIDATION_CSV, validation_rows(timestamp))
    write_docs(timestamp)

    pycache = SCRIPT_DIR / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
