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

CHECKPOINT = "4796"
CLAIM_ID = "L-638"
MARKER = "PPC4161_PARENT_VOLUME_LOCK_SELECTOR_OR_FINITE_EDGE_BOUND_FILL_4796"
PACKET_MARKER = "PPC4161_PACKET_PARENT_VOLUME_LOCK_SELECTOR_OR_FINITE_EDGE_BOUND_FILL_4796"
DECISION = "PARENT_CONTINUITY_VOLUME_LOCK_LAW_SHAPE_STAGED_EDGE_BOUND_RUNNER_INSTALLED_NO_LOCAL_CLAIM"
NEXT_TARGET = "4797-Y5-R2FR-parent-continuity-source-SigmaPhi-or-PD-domain-functional.md"

DOC_PATH = POST / "4796-Y5-R2FR-parent-volume-lock-selector-or-finite-edge-bound-fill.md"
FORMAL_PATH = FORMAL / "812-PPC4161-parent-volume-lock-selector-or-finite-edge-bound-fill.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"

RUNNER = SCRIPT_DIR / "volume_lock_edge_bound_gate_runner.py"

SOURCE_REGISTER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4796_SOURCE_REGISTER.csv"
VOLUME_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4796_PARENT_VOLUME_LOCK_INPUT.csv"
VOLUME_OUTPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4796_PARENT_VOLUME_LOCK_OUTPUT.csv"
EDGE_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4796_FINITE_EDGE_BOUND_INPUT.csv"
EDGE_OUTPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4796_FINITE_EDGE_BOUND_OUTPUT.csv"
OBSTRUCTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4796_OBSTRUCTION_UPDATE.csv"
GATE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4796_PROMOTION_GATES.csv"
FIREWALL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4796_FIREWALL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4796_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4796_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4796_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4796_VALIDATION.csv"

VOLUME_LOCK_CLAUSES = (
    "parent_continuity_law_signed",
    "mathcalJ_C_from_parent_action_signed",
    "Sigma_C_source_defined_signed",
    "Phi_C_boundary_flux_defined_signed",
    "stationary_domain_transport_signed",
    "local_no_source_condition_signed",
    "local_no_flux_condition_signed",
    "moving_boundary_zero_or_bound_signed",
    "PD_variation_owner_signed",
    "ND_normalization_variation_signed",
    "FLRW_active_class_preserved_signed",
    "Bianchi_Ward_stress_accounting_signed",
    "matter_selector_same_domain_signed",
    "no_volume_lock_by_assertion_signed",
)

EDGE_BOUND_CLAUSES = (
    "edge_surface_certificate_signed",
    "corner_zero_or_bound_signed",
    "dSFeps_zero_or_bound_signed",
    "bC_norm_source_signed",
    "harmonic_zero_or_bound_signed",
    "residual_zero_or_bound_signed",
    "cocycle_zero_or_bound_signed",
    "projector_tail_zero_or_bound_signed",
    "units_declared_signed",
    "no_edge_cancellation_signed",
)

SOURCE_SPECS = [
    ("SRC4796_00_4795_doc", POST / "4795-Y5-R2FR-JC-from-Q-parent-variation-PD-owner-or-dSFeps-certificate.md", "DEC4795_0_volume_obstruction", "4795 handoff: volume-lock obstruction"),
    ("SRC4796_01_4795_jc_output", SOURCE_DIR / "P8_Y5_R2FR_4795_JC_VARIATION_OUTPUT.csv", "JC_variation_volume_obstruction_smoke", "explicit int_D delta J_C smoke residual"),
    ("SRC4796_02_4795_dsfeps_output", SOURCE_DIR / "P8_Y5_R2FR_4795_DSFEPS_OUTPUT.csv", "finite_dSFeps_bound_smoke", "dSFeps finite bound component"),
    ("SRC4796_03_4794_corner_output", SOURCE_DIR / "P8_Y5_R2FR_4794_DOMAIN_CORNER_OUTPUT.csv", "finite_domain_corner_bound_smoke", "finite C_corner/domain-edge component"),
    ("SRC4796_04_1167_doc", POST / "1167-Y5-R10-parent-volume-lock-selector-or-finite-edge-bound-fill.md", "continuity_no_flux_law_is_best_volume_lock_route", "older continuity/no-flux route"),
    ("SRC4796_05_1020_doc", POST / "1020-Y5-R10-boundary-cohomology-domain-certificate-or-source-pack-first-row.md", "ETB1020_3_residual_bound", "weighted-Stokes finite edge bound"),
    ("SRC4796_06_runner", RUNNER, "def volume_lock_row", "4796 executable runner"),
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


def volume_lock_input_rows(timestamp: str) -> list[dict[str, Any]]:
    physical = clause_map(VOLUME_LOCK_CLAUSES, False)
    physical["FLRW_active_class_preserved_signed"] = True
    physical["no_volume_lock_by_assertion_signed"] = True

    residual = physical.copy()
    residual.update(
        {
            "parent_continuity_law_signed": False,
            "mathcalJ_C_from_parent_action_signed": False,
            "Sigma_C_source_defined_signed": False,
            "Phi_C_boundary_flux_defined_signed": False,
            "stationary_domain_transport_signed": False,
            "local_no_source_condition_signed": False,
            "local_no_flux_condition_signed": False,
            "moving_boundary_zero_or_bound_signed": False,
            "PD_variation_owner_signed": False,
            "ND_normalization_variation_signed": False,
            "Bianchi_Ward_stress_accounting_signed": False,
            "matter_selector_same_domain_signed": False,
        }
    )

    envelope = residual.copy()
    envelope.update(
        {
            "parent_continuity_law_signed": True,
            "Sigma_C_source_defined_signed": True,
            "Phi_C_boundary_flux_defined_signed": True,
            "stationary_domain_transport_signed": True,
            "moving_boundary_zero_or_bound_signed": True,
            "ND_normalization_variation_signed": True,
            "Bianchi_Ward_stress_accounting_signed": True,
        }
    )

    signed = clause_map(VOLUME_LOCK_CLAUSES, True)
    source_4795 = str(SOURCE_DIR / "P8_Y5_R2FR_4795_JC_VARIATION_OUTPUT.csv")

    def row(selector_id: str, status: str, source: str, clauses: dict[str, bool], values: dict[str, str] | None = None) -> dict[str, Any]:
        payload = {
            "selector_id": selector_id,
            "continuity_source": source,
            "JC_source": source,
            "Sigma_source": source,
            "Phi_source": source,
            "domain_transport_source": source,
            "PD_source": source,
            "FLRW_source": source,
            "provenance": source,
            "notes": "",
            "delta_JC_integral": "",
            "target_volume_lock": "",
            "source_term_integral_abs": "",
            "boundary_flux_abs": "",
            "moving_boundary_abs": "",
            "normalization_drift_abs": "",
            "row_status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        payload.update(clauses)
        if values:
            payload.update(values)
        return payload

    return [
        row("physical_parent_volume_lock_missing", "physical_branch_missing_parent_continuity_selector_nonclaim", str(POST / "1167-Y5-R10-parent-volume-lock-selector-or-finite-edge-bound-fill.md"), physical),
        row(
            "volume_obstruction_carried_from_4795",
            "4795_residual_carried_forward_nonclaim",
            source_4795,
            residual,
            {
                "delta_JC_integral": "1.095",
                "target_volume_lock": "0.0",
                "source_term_integral_abs": "0.0",
                "boundary_flux_abs": "0.0",
                "moving_boundary_abs": "0.0",
                "normalization_drift_abs": "0.0",
            },
        ),
        row(
            "finite_source_flux_envelope_smoke",
            "finite_balance_smoke_nonclaim_not_local_silence",
            source_4795,
            envelope,
            {
                "delta_JC_integral": "1.095",
                "target_volume_lock": "0.0",
                "source_term_integral_abs": "1.09",
                "boundary_flux_abs": "0.005",
                "moving_boundary_abs": "0.0",
                "normalization_drift_abs": "0.0",
            },
        ),
        row("conditional_parent_no_flux_volume_lock", "conditional_no_source_no_flux_theorem_nonclaim", "CONDITIONAL_PARENT_CONTINUITY_NO_FLUX_PACKET", signed),
        row("forbidden_volume_lock_hand_switch_control", "forbidden_control_nonclaim", "VOLUME_LOCK_BY_ASSERTION_LOCAL_FLRW_HAND_SWITCH_CONTINUITY_BY_ASSERTION", signed),
    ]


def edge_input_rows(timestamp: str) -> list[dict[str, Any]]:
    physical = clause_map(EDGE_BOUND_CLAUSES, False)
    physical["no_edge_cancellation_signed"] = True

    finite = clause_map(EDGE_BOUND_CLAUSES, True)
    finite["edge_surface_certificate_signed"] = False

    signed = clause_map(EDGE_BOUND_CLAUSES, True)
    edge_source = str(SOURCE_DIR / "P8_Y5_R2FR_4794_DOMAIN_CORNER_OUTPUT.csv")

    def row(edge_id: str, status: str, source: str, clauses: dict[str, bool], values: dict[str, str] | None = None) -> dict[str, Any]:
        payload = {
            "edge_id": edge_id,
            "edge_source": source,
            "corner_source": source,
            "dSFeps_source": str(SOURCE_DIR / "P8_Y5_R2FR_4795_DSFEPS_OUTPUT.csv") if source != "MISSING_EDGE_BOUND_SOURCE" else source,
            "bC_source": str(SOURCE_DIR / "P8_Y5_R2FR_4795_DSFEPS_OUTPUT.csv") if source != "MISSING_EDGE_BOUND_SOURCE" else source,
            "harmonic_source": source,
            "residual_source": source,
            "units_source": source,
            "provenance": source,
            "notes": "",
            "C_corner_abs": "",
            "norm_dS_Feps": "",
            "norm_bC": "",
            "harmonic_edge_abs": "",
            "residual_edge_abs": "",
            "cocycle_abs": "",
            "projector_tail_abs": "",
            "row_status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        payload.update(clauses)
        if values:
            payload.update(values)
        return payload

    return [
        row("physical_edge_bound_missing", "physical_branch_missing_edge_source_pack_nonclaim", "MISSING_EDGE_BOUND_SOURCE", physical),
        row(
            "finite_edge_bound_from_4794_4795_smoke",
            "finite_termwise_edge_bound_smoke_nonclaim",
            edge_source,
            finite,
            {
                "C_corner_abs": "1.3e-7",
                "norm_dS_Feps": "3.0e-4",
                "norm_bC": "2.0e-5",
                "harmonic_edge_abs": "2.0e-8",
                "residual_edge_abs": "1.0e-8",
                "cocycle_abs": "0.0",
                "projector_tail_abs": "0.0",
            },
        ),
        row("conditional_edge_zero_packet", "conditional_edge_zero_theorem_nonclaim", "CONDITIONAL_EDGE_ZERO_ALL_CLAUSES_SIGNED", signed),
        row("forbidden_edge_cancellation_control", "forbidden_control_nonclaim", "EDGE_CANCELLATION_OBSERVED_RESIDUAL_CANCEL_BOUNDARY_ZERO_BY_ASSERTION", signed),
    ]


def obstruction_rows(timestamp: str, volume_rows: list[dict[str, str]], edge_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    physical_volume = next(row for row in volume_rows if row["selector_id"] == "physical_parent_volume_lock_missing")
    residual_volume = next(row for row in volume_rows if row["selector_id"] == "volume_obstruction_carried_from_4795")
    envelope = next(row for row in volume_rows if row["selector_id"] == "finite_source_flux_envelope_smoke")
    finite_edge = next(row for row in edge_rows if row["edge_id"] == "finite_edge_bound_from_4794_4795_smoke")
    return [
        {
            "update_id": "OBS4796_0_parent_continuity_selector",
            "item": "d_4 mathcalJ_C = Sigma_C with Phi_C/domain transport",
            "status": physical_volume["runner_status"],
            "value_or_bound": physical_volume["missing_volume_lock_inputs"],
            "meaning": "the exact local volume lock still requires parent-owned continuity source, boundary flux and domain transport",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "update_id": "OBS4796_1_4795_residual",
            "item": "raw int_D delta J_C residual",
            "status": residual_volume["runner_status"],
            "value_or_bound": residual_volume["unclosed_volume_lock_abs"],
            "meaning": "without a selector or finite source/flux balance, the 4795 local obstruction remains open",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "update_id": "OBS4796_2_finite_source_flux_envelope",
            "item": "source/flux envelope",
            "status": envelope["runner_status"],
            "value_or_bound": envelope["source_flux_bound_abs"],
            "meaning": "a finite balance can explain a nonzero integral but is not local-vacuum silence unless the source/flux terms are zero by theorem",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "update_id": "OBS4796_3_termwise_edge_bound",
            "item": "Q_edge finite fallback",
            "status": finite_edge["runner_status"],
            "value_or_bound": finite_edge["Q_edge_bound_abs"],
            "meaning": "edge residual is now scoreable term-by-term in smoke mode, not cancellable by hand",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def gate_rows(timestamp: str, volume_rows: list[dict[str, str]], edge_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    physical_volume = next(row for row in volume_rows if row["selector_id"] == "physical_parent_volume_lock_missing")
    residual_volume = next(row for row in volume_rows if row["selector_id"] == "volume_obstruction_carried_from_4795")
    finite_edge = next(row for row in edge_rows if row["edge_id"] == "finite_edge_bound_from_4794_4795_smoke")
    return [
        {
            "gate_id": "PG4796_0_parent_continuity",
            "claim": "parent continuity law derives local volume lock",
            "gate_pass": False,
            "reason": "physical branch lacks Sigma_C, Phi_C, stationary domain transport, P_D variation, and matter/source selector",
            "evidence": physical_volume["missing_volume_lock_inputs"],
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "PG4796_1_residual_not_closed",
            "claim": "4795 volume obstruction is removed in the physical local branch",
            "gate_pass": False,
            "reason": "carried residual remains nonzero unless the parent selector or finite source/flux balance is supplied",
            "evidence": residual_volume["unclosed_volume_lock_abs"],
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "PG4796_2_edge_bound_runner",
            "claim": "finite edge fallback is executable",
            "gate_pass": True,
            "reason": "termwise smoke bound computes from C_corner, dSFeps, harmonic and residual terms",
            "evidence": finite_edge["Q_edge_bound_abs"],
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "PG4796_3_local_GR_Newton",
            "claim": "local GR/Newton/PPN/R10 promotion allowed",
            "gate_pass": False,
            "reason": "parent volume-lock selector is unsigned and finite edge row is smoke/nonclaim only",
            "evidence": "nonclaim firewall active",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def firewalls(timestamp: str) -> list[dict[str, Any]]:
    rules = [
        ("FW4796_0_no_volume_lock_assertion", "int_D delta J_C=0 must follow from parent Sigma_C/Phi_C/domain-transport law, not assertion."),
        ("FW4796_1_no_local_FLRW_hand_switch", "The local-vacuum branch and FLRW active branch must be selected by the same parent law."),
        ("FW4796_2_no_edge_cancellation", "Unknown edge/corner/harmonic/residual terms are bounded term-by-term, never cancelled against each other."),
        ("FW4796_3_no_source_flux_as_silence", "A nonzero source/flux envelope explains balance but is not a local-vacuum zero theorem."),
        ("FW4796_4_no_local_claim", "No local-GR/Newton/R10/PPN/WEP/clock/orbital claim follows from 4796."),
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
            "decision_id": "DEC4796_0_best_route",
            "decision": "parent_continuity_no_flux_law_remains_best_volume_lock_route",
            "reason": "it derives local int_D delta J_C=0 from zero source, zero flux and stationary domain transport rather than from a plateau axiom",
            "next_action": "derive Sigma_C, Phi_C, and domain transport from lifted-C parent action/current variation",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC4796_1_finite_fallback",
            "decision": "termwise_edge_bound_is_parallel_fallback",
            "reason": "if exact volume lock stalls, Q_edge can be bounded as C_corner + ||dS(F epsilon)||||B_C|| + harmonic + residual + cocycle + projector tail",
            "next_action": "source real arena edge rows or prove their zero certificates",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC4796_2_next",
            "decision": "attack_parent_source_or_PD_domain_functional",
            "reason": "Sigma_C/Phi_C and P_D/domain transport are now the first hard objects, not generic missingness",
            "next_action": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def status_rows(timestamp: str, volume_rows: list[dict[str, str]], edge_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    residual_volume = next(row for row in volume_rows if row["selector_id"] == "volume_obstruction_carried_from_4795")
    envelope = next(row for row in volume_rows if row["selector_id"] == "finite_source_flux_envelope_smoke")
    finite_edge = next(row for row in edge_rows if row["edge_id"] == "finite_edge_bound_from_4794_4795_smoke")
    return [
        {
            "status_id": "STATUS4796_0_volume_lock_route",
            "status": "PARENT_CONTINUITY_ROUTE_STAGED_NOT_PARENT_DERIVED",
            "detail": "local zero requires Sigma_C=0, Phi_C=0, stationary domain transport, P_D owner and Bianchi/Ward stress accounting",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "status_id": "STATUS4796_1_4795_residual",
            "status": residual_volume["runner_status"],
            "detail": f"unclosed_volume_lock_abs={residual_volume['unclosed_volume_lock_abs']}",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "status_id": "STATUS4796_2_source_flux_envelope",
            "status": envelope["runner_status"],
            "detail": f"source_flux_bound_abs={envelope['source_flux_bound_abs']}; this is balance, not local silence",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "status_id": "STATUS4796_3_edge_bound",
            "status": finite_edge["runner_status"],
            "detail": f"Q_edge_bound_abs={finite_edge['Q_edge_bound_abs']}",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "status_id": "STATUS4796_4_selected_next",
            "status": "PARENT_CONTINUITY_SOURCE_SIGMAPHI_OR_PD_DOMAIN_FUNCTIONAL",
            "detail": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "next_id": "NEXT4796_0_4797",
            "next_target": NEXT_TARGET,
            "objective": "derive Sigma_C/Phi_C/domain transport from lifted-C parent action or derive P_D as a domain functional with stress-safe variation",
            "include": "mathcalJ_C parent action term; Sigma_C source; Phi_C boundary flux; stationary domain transport; P_D variation; Bianchi/Ward stress; local no-source/no-flux theorem; FLRW active class",
            "exclude": "continuity by assertion; local/FLRW hand switch; source flux treated as local silence; edge cancellation; local-GR claim; GitHub",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
    ]


def validation_rows(timestamp: str) -> list[dict[str, Any]]:
    sources = parse_csv(SOURCE_REGISTER_CSV)
    volume_rows = parse_csv(VOLUME_OUTPUT_CSV)
    edge_rows = parse_csv(EDGE_OUTPUT_CSV)
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

    physical_volume = next(row for row in volume_rows if row["selector_id"] == "physical_parent_volume_lock_missing")
    residual_volume = next(row for row in volume_rows if row["selector_id"] == "volume_obstruction_carried_from_4795")
    envelope = next(row for row in volume_rows if row["selector_id"] == "finite_source_flux_envelope_smoke")
    conditional_volume = next(row for row in volume_rows if row["selector_id"] == "conditional_parent_no_flux_volume_lock")
    forbidden_volume = next(row for row in volume_rows if row["selector_id"] == "forbidden_volume_lock_hand_switch_control")
    physical_edge = next(row for row in edge_rows if row["edge_id"] == "physical_edge_bound_missing")
    finite_edge = next(row for row in edge_rows if row["edge_id"] == "finite_edge_bound_from_4794_4795_smoke")
    conditional_edge = next(row for row in edge_rows if row["edge_id"] == "conditional_edge_zero_packet")
    forbidden_edge = next(row for row in edge_rows if row["edge_id"] == "forbidden_edge_cancellation_control")

    add("VAL4796_0_sources", "all cited sources exist and needles are found", all(bool_text(row["exists"]) and bool_text(row["needle_found"]) for row in sources), str(SOURCE_REGISTER_CSV))
    add("VAL4796_1_physical_volume_blocks", "physical parent volume-lock selector remains blocked", physical_volume["runner_status"] == "BLOCKED_MISSING_PARENT_VOLUME_LOCK_OR_BALANCE_INPUTS", str(VOLUME_OUTPUT_CSV))
    add("VAL4796_2_4795_residual_carries", "4795 volume obstruction is carried and remains nonzero", residual_volume["runner_status"] == "VOLUME_LOCK_RESIDUAL_COMPUTED_PARENT_SELECTOR_OPEN_NONCLAIM" and residual_volume["unclosed_volume_lock_abs"] != "MISSING_NUMERIC_VALUE", str(VOLUME_OUTPUT_CSV))
    add("VAL4796_3_source_flux_envelope", "finite source/flux envelope can balance but not prove local silence", envelope["runner_status"] == "VOLUME_BALANCE_FINITE_SOURCE_FLUX_ENVELOPE_NONCLAIM" and envelope["Z_local_lock"] == "False", str(VOLUME_OUTPUT_CSV))
    add("VAL4796_4_conditional_volume_zero", "conditional parent no-flux theorem zeros volume lock", conditional_volume["runner_status"] == "PARENT_VOLUME_LOCK_SELECTOR_CONDITIONAL_THEOREM_NONCLAIM", str(VOLUME_OUTPUT_CSV))
    add("VAL4796_5_forbidden_volume_fails", "volume-lock hand switch fails", forbidden_volume["runner_status"] == "FAILED_PARENT_VOLUME_LOCK_GATE", str(VOLUME_OUTPUT_CSV))
    add("VAL4796_6_physical_edge_blocks", "physical edge bound source pack remains blocked", physical_edge["runner_status"] == "BLOCKED_MISSING_FINITE_EDGE_BOUND_INPUTS", str(EDGE_OUTPUT_CSV))
    add("VAL4796_7_finite_edge_computes", "finite termwise edge bound computes", finite_edge["runner_status"] == "EDGE_BOUND_FINITE_TERMWISE_NONCLAIM" and finite_edge["Q_edge_bound_abs"] != "MISSING_NUMERIC_VALUE", str(EDGE_OUTPUT_CSV))
    add("VAL4796_8_conditional_edge_zero", "conditional edge zero theorem passes as nonclaim", conditional_edge["runner_status"] == "EDGE_ZERO_CERTIFIED_CONDITIONAL_THEOREM_NONCLAIM", str(EDGE_OUTPUT_CSV))
    add("VAL4796_9_forbidden_edge_fails", "edge cancellation shortcut fails", forbidden_edge["runner_status"] == "FAILED_FINITE_EDGE_BOUND_GATE", str(EDGE_OUTPUT_CSV))
    add("VAL4796_10_claim", "claim register includes L-638 as nonclaim", CLAIM_ID in read_text(CLAIMS_PATH), str(CLAIMS_PATH))
    add("VAL4796_11_resume", "resume points at 4797", NEXT_TARGET in read_text(RESUME_PATH), str(RESUME_PATH))
    add("VAL4796_OVERALL", "all 4796 volume-lock/edge-bound checks pass", all(row["result"] == "PASS" for row in validation), DECISION)
    return validation


def write_claim(timestamp: str) -> None:
    if CLAIMS_PATH.exists() and any(row.get("claim_id") == CLAIM_ID for row in parse_csv(CLAIMS_PATH)):
        return
    with CLAIMS_PATH.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = reader.fieldnames or []
    row = {
        "claim_id": CLAIM_ID,
        "domain": "volume_lock_edge_bound_gate_runner",
        "claim": "4796 stages the parent continuity/no-flux volume-lock theorem route and installs a finite termwise edge-bound fallback runner.",
        "current_evidence": "Generated source register, parent volume-lock input/output, finite edge-bound input/output, obstruction update, gates, firewalls, decision, status, next target and validation.",
        "status": "parent_continuity_route_staged_edge_bound_runner_ready_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "Do not treat a finite source/flux balance as local-vacuum silence or cancel edge terms by hand.",
        "sector": "local_gr",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "continuity by assertion; local/FLRW hand switch; source flux as silence; edge cancellation; local-GR promotion",
        "title": "Parent volume-lock selector and finite edge bound",
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

4796 converts the local-volume problem into an explicit parent continuity/no-flux theorem target. The desired law is `d_4 mathcalJ_C = Sigma_C`, with spatial balance `delta int_D J_C = int_D Sigma_C + int_partialD Phi_C + moving_boundary_term + normalization/domain terms`. Local silence follows only if the same parent action signs `Sigma_C=0`, `Phi_C=0`, stationary domain transport, `P_D` variation, `N_D` normalization and Bianchi/Ward stress accounting on the local branch while preserving the FLRW active/top-class branch.

The finite fallback is now executable: `Q_edge_bound = C_corner + ||d_S(F epsilon)|| ||B_C|| + harmonic_edge + residual_edge + cocycle + projector_tail`. The smoke row computes a finite termwise bound, but physical source rows are still nonclaim.

## Firewalls

- No continuity or volume lock by assertion.
- No local/FLRW hand switch.
- No treating nonzero source/flux balance as local-vacuum silence.
- No edge-term cancellation between unknowns.
- No local-GR/Newton/PPN/R10 claim from this checkpoint.
"""
    write_text(RESUME_PATH, content)


def write_docs(timestamp: str) -> None:
    sources = parse_csv(SOURCE_REGISTER_CSV)
    volume_rows = parse_csv(VOLUME_OUTPUT_CSV)
    edge_rows = parse_csv(EDGE_OUTPUT_CSV)
    obstruction = parse_csv(OBSTRUCTION_CSV)
    gates = parse_csv(GATE_CSV)
    firewall_rows = parse_csv(FIREWALL_CSV)
    decisions = parse_csv(DECISION_CSV)
    statuses = parse_csv(STATUS_CSV)
    validation = parse_csv(VALIDATION_CSV)

    content = f"""# 4796 - Parent volume-lock selector or finite edge-bound fill

Marker: `{MARKER}`
Generated: `{timestamp}`
Decision: `{DECISION}`

## Result

4796 makes the local-volume bridge explicit:

```text
d_4 mathcalJ_C = Sigma_C
delta int_D J_C = int_D Sigma_C + int_partialD Phi_C
                + moving_boundary_term + normalization/domain terms
```

If the parent theory signs `Sigma_C=0`, `Phi_C=0`, stationary domain transport, `delta P_D` ownership, `delta N_D` accounting, and Bianchi/Ward stress bookkeeping on the local branch, then `int_D delta J_C=0` is a theorem. The same law can keep FLRW active through a homogeneous source or top class, so this is not a local/FLRW hand switch.

The checkpoint also installs the finite fallback:

```text
Q_edge_bound = C_corner + ||d_S(F epsilon)|| ||B_C||
             + harmonic_edge + residual_edge + cocycle + projector_tail
```

That fallback is executable in smoke mode but remains nonclaim until each term has a real arena certificate or source-backed bound.

## Source Register

{markdown_table(sources, ["source_id", "source_path", "exists", "needle_found", "role"])}

## Parent Volume-Lock Output

{markdown_table(volume_rows, ["selector_id", "Z_parent_continuity", "Z_local_lock", "Z_FLRW_compatible", "raw_volume_lock_abs", "source_flux_bound_abs", "unclosed_volume_lock_abs", "runner_status", "missing_volume_lock_inputs", "anti_circularity_status"])}

## Finite Edge-Bound Output

{markdown_table(edge_rows, ["edge_id", "Q_edge_bound_abs", "dSFeps_term_abs", "runner_status", "missing_edge_inputs", "anti_circularity_status"])}

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
    write_text(FORMAL_PATH, content.replace("# 4796 -", "# 812 - PPC4161 "))

    append_once(
        SPINE_PATH,
        MARKER,
        f"""
## {MARKER}

- 4796 stages the parent continuity/no-flux route for local volume lock: `d_4 mathcalJ_C = Sigma_C` must supply `Sigma_C`, `Phi_C`, domain transport, `P_D`, `N_D`, and Bianchi/Ward accounting.
- The 4795 residual remains open in the local branch unless that selector is derived; a finite source/flux envelope is balance, not local vacuum silence.
- The edge fallback is now executable as a termwise bound: `C_corner + ||d_S(F epsilon)|| ||B_C|| + harmonic + residual + cocycle + projector_tail`.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## {PACKET_MARKER}

4796 adds the parent continuity/no-flux volume-lock target and finite termwise edge-bound runner to the local packet. It does not claim local GR, but it turns the next bridge into concrete objects: `Sigma_C`, `Phi_C`, stationary domain transport, `P_D` variation, and stress-safe source accounting. Next target: `{NEXT_TARGET}`.
""",
    )


def main() -> int:
    timestamp = now()
    write_csv(SOURCE_REGISTER_CSV, source_register(timestamp))
    write_csv(VOLUME_INPUT_CSV, volume_lock_input_rows(timestamp))
    write_csv(EDGE_INPUT_CSV, edge_input_rows(timestamp))
    run_command([sys.executable, str(RUNNER), str(VOLUME_INPUT_CSV), str(VOLUME_OUTPUT_CSV), str(EDGE_INPUT_CSV), str(EDGE_OUTPUT_CSV)])

    volume_rows = parse_csv(VOLUME_OUTPUT_CSV)
    edge_rows = parse_csv(EDGE_OUTPUT_CSV)
    write_csv(OBSTRUCTION_CSV, obstruction_rows(timestamp, volume_rows, edge_rows))
    write_csv(GATE_CSV, gate_rows(timestamp, volume_rows, edge_rows))
    write_csv(FIREWALL_CSV, firewalls(timestamp))
    write_csv(DECISION_CSV, decision_rows(timestamp))
    write_csv(STATUS_CSV, status_rows(timestamp, volume_rows, edge_rows))
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
