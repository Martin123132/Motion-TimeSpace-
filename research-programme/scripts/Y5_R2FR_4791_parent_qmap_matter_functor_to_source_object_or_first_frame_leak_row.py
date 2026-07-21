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

CHECKPOINT = "4791"
CLAIM_ID = "L-633"
MARKER = "PPC4161_PARENT_QMAP_MATTER_FUNCTOR_TO_SOURCE_OBJECT_OR_FIRST_FRAME_LEAK_ROW_4791"
PACKET_MARKER = "PPC4161_PACKET_PARENT_QMAP_MATTER_FUNCTOR_TO_SOURCE_OBJECT_OR_FIRST_FRAME_LEAK_ROW_4791"
DECISION = "QMAP_MATTER_FUNCTOR_SOURCE_GATE_INSTALLED_PHYSICAL_BRANCH_UNSIGNED_CG_FRAME_LEAK_ROW_READY_NONCLAIM"
NEXT_TARGET = "4792-Y5-R2FR-Cperp-exactness-boundary-silence-or-real-cg-source-pack.md"

DOC_PATH = POST / "4791-Y5-R2FR-parent-qmap-matter-functor-to-source-object-or-first-frame-leak-row.md"
FORMAL_PATH = FORMAL / "807-PPC4161-parent-qmap-matter-functor-to-source-object-or-first-frame-leak-row.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"

FUNCTOR_RUNNER = SCRIPT_DIR / "qmap_matter_functor_source_gate_runner.py"
OWNER_RUNNER = SCRIPT_DIR / "same_source_object_profile_runner.py"

SOURCE_REGISTER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4791_SOURCE_REGISTER.csv"
FUNCTOR_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4791_QMAP_MATTER_FUNCTOR_INPUT.csv"
FUNCTOR_OUTPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4791_QMAP_MATTER_FUNCTOR_OUTPUT.csv"
CG_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4791_CG_FRAME_LEAK_INPUT.csv"
CG_OUTPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4791_CG_FRAME_LEAK_OUTPUT.csv"
OWNER_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4791_SOURCE_OBJECT_OWNER_INPUT.csv"
OWNER_OUTPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4791_SOURCE_OBJECT_OWNER_OUTPUT.csv"
PROFILE_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4791_SOURCE_OBJECT_PROFILE_INPUT.csv"
PROFILE_OUTPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4791_SOURCE_OBJECT_PROFILE_OUTPUT.csv"
FUNCTOR_GATE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4791_FUNCTOR_GATE_DECISION.csv"
PROMOTION_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4791_PROMOTION_GATES.csv"
FIREWALL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4791_FIREWALL_ROWS.csv"
ROUTE_MATRIX_CSV = SOURCE_DIR / "P8_Y5_R2FR_4791_ROUTE_SELECTION_MATRIX.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4791_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4791_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4791_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4791_VALIDATION.csv"

SOURCE_SPECS = [
    ("SRC4791_00_4790_doc", POST / "4790-Y5-R2FR-parent-own-same-source-object-or-fill-Req-Bzero-finite-shell-profile.md", "same source object =", "4790 source-object handoff"),
    ("SRC4791_01_1156_functor", POST / "1156-Y5-R10-parent-quotient-matter-functor-signature-or-frame-leak-bound-fill.md", "Quotient Matter Functor Signature Audit", "q/matter functor audit"),
    ("SRC4791_02_1157_qmap", POST / "1157-Y5-R10-parent-q-map-null-generator-proof-or-cg-bound-first-fill.md", "QMAP1157_8_verdict", "q-map/null-generator audit"),
    ("SRC4791_03_637_qmap", SOURCE_DIR / "P8_Y5_R10_637_QUOTIENT_MAP_DERIVATION.csv", "QM637_2_vertical_kernel", "candidate q-map vertical kernel"),
    ("SRC4791_04_710_descent", SOURCE_DIR / "P8_Y5_R10_710_DESCENT_PARENT_ACTION_CLAUSE.csv", "DPC710_9_verdict", "descent parent action clause"),
    ("SRC4791_05_944_descent", SOURCE_DIR / "P8_Y5_R10_944_DESCENT_PROOF_GATE.csv", "QDG944_7_total", "observed coframe descent proof gate"),
    ("SRC4791_06_1029_cg", POST / "1029-Y5-R10-cg-no-shadow-frame-theorem-or-first-numeric-coupling-row.md", "c_g intake template", "c_g first coupling row"),
    ("SRC4791_07_1032_cg", POST / "1032-Y5-R10-spm-closure-ledger-and-finite-cg-tau-acquisition-runner.md", "Finite c_g/tau acquisition template", "c_g/tau acquisition template"),
    ("SRC4791_08_functor_runner", FUNCTOR_RUNNER, "def functor_row", "4791 q/matter functor runner"),
    ("SRC4791_09_owner_runner", OWNER_RUNNER, "def owner_row", "4790 owner runner reused for partial handoff"),
]

FUNCTOR_CLAUSES = (
    "parent_q_map_signed",
    "vertical_kernel_signed",
    "observed_coframe_functor_signed",
    "matter_action_factorized",
    "constants_quotient_owned",
    "geometry_stack_descends",
    "boundary_no_tail_signed",
    "no_hidden_visible_morphism_signed",
    "radiative_readout_closure_signed",
    "source_support_functor_signed",
    "hilbert_current_from_variation_signed",
    "no_q_by_declaration_signed",
    "no_vertical_by_label_signed",
)

OWNER_CLAUSES = (
    "parent_action_variation_signed",
    "single_observed_frame_signed",
    "quotient_matter_functor_signed",
    "source_worldtube_support_signed",
    "hilbert_current_variation_owned",
    "hamiltonian_charge_integrable",
    "M_H_ref_normalized",
    "PiM_hamiltonian_map_signed",
    "topological_PD_representative_signed",
    "same_linking_class_signed",
    "exact_Bzero_primitive_signed",
    "Bzero_flux_zero_signed",
    "no_extra_exchange_signed",
    "projector_commutator_zero_signed",
    "radial_closure_signed",
    "no_tautological_definition_signed",
    "no_postfit_readout_signed",
)


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_text(path_object: Path) -> str:
    return path_object.read_text(encoding="utf-8-sig", errors="replace")


def write_text(path_object: Path, content: str) -> None:
    path_object.parent.mkdir(parents=True, exist_ok=True)
    path_object.write_text(content, encoding="utf-8", newline="\n")


def append_once(path_object: Path, marker: str, block: str) -> None:
    existing = read_text(path_object) if path_object.exists() else ""
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
    with path_object.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
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
        text = read_text(path_object) if exists else ""
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


def functor_clause_map(value: bool) -> dict[str, bool]:
    return {clause: value for clause in FUNCTOR_CLAUSES}


def functor_row(functor_id: str, status: str, source: str, timestamp: str, clauses: dict[str, bool]) -> dict[str, Any]:
    return {
        "functor_id": functor_id,
        "functor_source": source,
        "provenance": source,
        "notes": "",
        "row_status": status,
        "valid_for_claim": False,
        "timestamp_utc": timestamp,
        **clauses,
    }


def functor_input_rows(timestamp: str) -> list[dict[str, Any]]:
    physical = functor_clause_map(False)
    for clause in ("no_q_by_declaration_signed", "no_vertical_by_label_signed"):
        physical[clause] = True
    q_only = functor_clause_map(False)
    for clause in ("parent_q_map_signed", "vertical_kernel_signed", "no_q_by_declaration_signed", "no_vertical_by_label_signed"):
        q_only[clause] = True
    signed = functor_clause_map(True)
    return [
        functor_row("physical_qmatter_functor_attempt", "physical_branch_nonclaim", "4790_PHYSICAL_BRANCH_PLUS_1156_1157_AUDIT", timestamp, physical),
        functor_row("q_vertical_only_not_enough", "conditional_q_vertical_only_nonclaim", "QM637_CONDITIONAL_Q_VERTICAL_ONLY", timestamp, q_only),
        functor_row("conditional_qmatter_source_frame_packet", "conditional_reference_theorem_nonclaim", "CONDITIONAL_QMATTER_FUNCTOR_ALL_CLAUSES_SIGNED", timestamp, signed),
        functor_row("private_qmatter_source_frame_testbench", "private_testbench_nonclaim", "PRIVATE_QMATTER_SOURCE_FRAME_PACKET", timestamp, signed),
        functor_row("forbidden_q_by_declaration_control", "forbidden_control_nonclaim", "Q_BY_DECLARATION_VERTICAL_BY_LABEL_OBSERVED_RESIDUAL_CANCEL", timestamp, signed),
    ]


def cg_input_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "cg_id": "physical_cg_first_row_missing",
            "c_g": "MISSING_PARENT_INPUT",
            "tau_R10": "MISSING_ARENA_PROJECTION",
            "tau_PPN_gamma": "MISSING_ARENA_PROJECTION",
            "tau_PPN_beta": "MISSING_ARENA_PROJECTION",
            "tau_clock": "MISSING_ARENA_PROJECTION",
            "tau_WEP": "MISSING_ARENA_PROJECTION",
            "tau_orbital": "MISSING_ARENA_PROJECTION",
            "Z_cg_zero_theorem_signed": False,
            "cg_source": "MISSING_PARENT_SOURCE",
            "projection_source": "MISSING_ARENA_SOURCE",
            "zero_theorem_path": "MISSING_ZERO_THEOREM",
            "row_status": "physical_cg_missing_nonclaim",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "cg_id": "finite_cg_projection_smoke",
            "c_g": "1.0e-3",
            "tau_R10": "0.5",
            "tau_PPN_gamma": "0.2",
            "tau_PPN_beta": "0.1",
            "tau_clock": "0.05",
            "tau_WEP": "0.0",
            "tau_orbital": "0.3",
            "Z_cg_zero_theorem_signed": False,
            "cg_source": str(CG_INPUT_CSV),
            "projection_source": str(CG_INPUT_CSV),
            "zero_theorem_path": str(FUNCTOR_OUTPUT_CSV),
            "row_status": "finite_projection_smoke_nonclaim",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "cg_id": "conditional_qmatter_cg_zero",
            "c_g": "",
            "tau_R10": "",
            "tau_PPN_gamma": "",
            "tau_PPN_beta": "",
            "tau_clock": "",
            "tau_WEP": "",
            "tau_orbital": "",
            "Z_cg_zero_theorem_signed": True,
            "cg_source": str(FUNCTOR_OUTPUT_CSV),
            "projection_source": str(FUNCTOR_OUTPUT_CSV),
            "zero_theorem_path": str(FUNCTOR_OUTPUT_CSV),
            "row_status": "conditional_zero_theorem_nonclaim",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "cg_id": "forbidden_cg_orbital_backfill",
            "c_g": "0",
            "tau_R10": "0",
            "tau_PPN_gamma": "0",
            "tau_PPN_beta": "0",
            "tau_clock": "0",
            "tau_WEP": "0",
            "tau_orbital": "0",
            "Z_cg_zero_theorem_signed": False,
            "cg_source": "ORBITAL_GM_DEFINITION_OBSERVED_RESIDUAL_CANCEL",
            "projection_source": "PPN_FIT_AS_SOURCE",
            "zero_theorem_path": "Q_BY_DECLARATION",
            "row_status": "forbidden_control_nonclaim",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def owner_clause_map(value: bool) -> dict[str, bool]:
    return {clause: value for clause in OWNER_CLAUSES}


def owner_row(owner_id: str, status: str, source: str, timestamp: str, clauses: dict[str, bool]) -> dict[str, Any]:
    return {
        "owner_id": owner_id,
        "owner_source": source,
        "provenance": source,
        "notes": "",
        "row_status": status,
        "valid_for_claim": False,
        "timestamp_utc": timestamp,
        **clauses,
    }


def owner_input_rows(timestamp: str) -> list[dict[str, Any]]:
    physical = owner_clause_map(False)
    for clause in ("parent_action_variation_signed", "no_tautological_definition_signed", "no_postfit_readout_signed"):
        physical[clause] = True
    partial = owner_clause_map(False)
    for clause in (
        "parent_action_variation_signed",
        "single_observed_frame_signed",
        "quotient_matter_functor_signed",
        "source_worldtube_support_signed",
        "hilbert_current_variation_owned",
        "no_tautological_definition_signed",
        "no_postfit_readout_signed",
    ):
        partial[clause] = True
    signed = owner_clause_map(True)
    return [
        owner_row("physical_after_4791_qmatter_attempt", "physical_branch_nonclaim", "4791_PHYSICAL_QMATTER_UNSIGNED", timestamp, physical),
        owner_row("conditional_qmatter_partial_source_object", "conditional_qmatter_partial_owner_nonclaim", "4791_QMATTER_SUPPLIES_FRAME_WORLDTUBE_HILBERT_ONLY", timestamp, partial),
        owner_row("conditional_full_source_object_control", "conditional_full_source_object_nonclaim", "PRIVATE_FULL_SOURCE_OBJECT_CONTROL", timestamp, signed),
    ]


def profile_input_rows(timestamp: str) -> list[dict[str, Any]]:
    base = {
        "profile_id": "owner_runner_placeholder_profile",
        "system_id": "4791_owner_runner",
        "branch_id": "not_used_for_claim",
        "r_inner_m": "1.0",
        "r_outer_m": "2.0",
        "PiM_JH_integral_kg": "1.0",
        "JM_top_integral_kg": "1.0",
        "Bzero_primitive_integral_kg": "0",
        "Bzero_boundary_flux_abs_kg": "0",
        "boundary_reference_shift_abs_kg": "0",
        "collar_flux_abs_kg": "0",
        "frame_mismatch_abs_kg": "0",
        "extra_exchange_abs_kg": "0",
        "projector_commutator_abs_kg": "0",
        "radial_nonclosure_abs_kg": "0",
        "M_H_ref_kg": "1.0",
        "profile_source": str(PROFILE_INPUT_CSV),
        "source_path": str(PROFILE_INPUT_CSV),
        "zero_theorem_path": str(OWNER_INPUT_CSV),
        "provenance": str(PROFILE_INPUT_CSV),
        "notes": "placeholder only so owner runner emits source-object profile output",
        "row_status": "private_zero_profile_nonclaim",
        "valid_for_claim": False,
        "timestamp_utc": timestamp,
    }
    return [base]


def gate_rows(timestamp: str, functors: list[dict[str, str]], owners: list[dict[str, str]], cg_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    physical_functor = next(row for row in functors if row["functor_id"] == "physical_qmatter_functor_attempt")
    conditional_functor = next(row for row in functors if row["functor_id"] == "conditional_qmatter_source_frame_packet")
    partial_owner = next(row for row in owners if row["owner_id"] == "conditional_qmatter_partial_source_object")
    physical_cg = next(row for row in cg_rows if row["cg_id"] == "physical_cg_first_row_missing")
    finite_cg = next(row for row in cg_rows if row["cg_id"] == "finite_cg_projection_smoke")
    return [
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "QMG4791_0_conditional_functor",
            "claim": "q/matter functor can supply observed frame, source support and Hilbert current clauses",
            "gate_pass": conditional_functor["runner_status"] == "QMAP_MATTER_FUNCTOR_TO_SOURCE_OBJECT_PARTIAL_OWNER_NONCLAIM",
            "status": conditional_functor["runner_status"],
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "QMG4791_1_physical_functor",
            "claim": "current physical MTS parent-signs q/matter functor",
            "gate_pass": False,
            "status": physical_functor["runner_status"],
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "QMG4791_2_partial_owner",
            "claim": "q/matter functor alone closes full source object",
            "gate_pass": False,
            "status": partial_owner["runner_status"],
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "QMG4791_3_physical_cg",
            "claim": "physical c_g row is score-ready",
            "gate_pass": False,
            "status": physical_cg["runner_status"],
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "QMG4791_4_finite_cg_smoke",
            "claim": "finite c_g projection runner computes when values and projections exist",
            "gate_pass": finite_cg["runner_status"] == "CG_FRAME_LEAK_ROW_COMPUTED_NONCLAIM",
            "status": finite_cg["runner_status"],
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def promotion_rows(timestamp: str, functors: list[dict[str, str]], owners: list[dict[str, str]]) -> list[dict[str, Any]]:
    physical_functor = next(row for row in functors if row["functor_id"] == "physical_qmatter_functor_attempt")
    partial_owner = next(row for row in owners if row["owner_id"] == "conditional_qmatter_partial_source_object")
    return [
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "PG4791_0_qmatter",
            "claim": "q/matter functor theorem is physical evidence",
            "gate_pass": False,
            "reason": "physical branch keeps q, vertical kernel, matter factorization and closure clauses unsigned",
            "evidence": physical_functor["missing_functor_clauses"],
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "PG4791_1_source_object",
            "claim": "q/matter functor partial owner is enough for R_eq/B_zero",
            "gate_pass": False,
            "reason": "Hamiltonian charge, Pi_M, topology, B_zero and no-exchange/projector/radial clauses remain missing",
            "evidence": partial_owner["missing_owner_clauses"],
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "PG4791_2_local_GR",
            "claim": "local GR/Newton/PPN claim allowed",
            "gate_pass": False,
            "reason": "q/matter functor and c_g row remain nonclaim; source object and PPN followthrough remain open",
            "evidence": "nonclaim firewall active",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def firewalls(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("FW4791_0_no_q_by_declaration", "q must be parent kinematics/reduced phase-space data, not declared after deciding which variables to hide"),
        ("FW4791_1_no_vertical_by_label", "v_X in ker(Dq) must follow from null/exactness, not naming"),
        ("FW4791_2_no_functor_as_full_source", "q/matter functor can own frame/source-current clauses but not Hamiltonian mass/topology by itself"),
        ("FW4791_3_no_cg_without_projection", "c_g cannot score without value, units, source path and arena projections"),
        ("FW4791_4_no_WEP_only_shortcut", "common c_g may be WEP-silent but still affect R10, clocks, PPN or orbital source normalization"),
        ("FW4791_5_no_local_claim", "no local-GR/Newton/PPN/R10 claim follows from this checkpoint"),
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
        for firewall_id, rule in rows
    ]


def routes(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("RT4791_0_Cperp_exactness", "derive Cperp exactness and boundary silence so v_X is actually null/vertical", "SELECTED_NEXT"),
        ("RT4791_1_cg_source_pack", "fill real c_g value/units/projection source pack if exactness route fails", "SELECTED_FALLBACK"),
        ("RT4791_2_Hamiltonian_charge", "after q/matter functor closes, derive integrable M_H_ref and Pi_M Hamiltonian map", "QUEUED"),
        ("RT4791_3_source_object", "return to full source-object owner packet after q/functor and Hamiltonian pieces are signed", "QUEUED"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "route_id": route_id,
            "route": route,
            "selection_status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for route_id, route, status in rows
    ]


def decisions(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "decision_id": "DEC4791_0_functor_partial_owner",
            "decision": "qmatter_functor_can_only_partially_feed_source_object",
            "reason": "if signed, it supplies observed frame, source support and Hilbert current clauses, but not Hamiltonian mass, Pi_M, topology, B_zero, exchange/projector/radial silence",
            "next_action": "derive Cperp exactness/boundary silence or fill c_g source pack",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "decision_id": "DEC4791_1_current_branch",
            "decision": "physical_qmatter_functor_not_parent_signed",
            "reason": "q object, vertical kernel, matter factorization, constants, geometry stack, boundary tail and hidden-visible morphism clauses remain unsigned",
            "next_action": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "decision_id": "DEC4791_2_cg",
            "decision": "first_cg_frame_leak_row_ready_but_unfilled",
            "reason": "runner computes finite c_g arena envelope only when value, units/source path and tau projections exist",
            "next_action": "source c_g/tau rows or prove Z_cg through q/matter functor exactness",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def status_rows(timestamp: str, functors: list[dict[str, str]], owners: list[dict[str, str]], cg_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    physical_functor = next(row for row in functors if row["functor_id"] == "physical_qmatter_functor_attempt")
    partial_owner = next(row for row in owners if row["owner_id"] == "conditional_qmatter_partial_source_object")
    finite_cg = next(row for row in cg_rows if row["cg_id"] == "finite_cg_projection_smoke")
    physical_cg = next(row for row in cg_rows if row["cg_id"] == "physical_cg_first_row_missing")
    return [
        {
            "checkpoint": CHECKPOINT,
            "status_id": "STATUS4791_0_physical_functor",
            "status": physical_functor["runner_status"],
            "detail": physical_functor["missing_functor_clauses"],
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "status_id": "STATUS4791_1_partial_owner",
            "status": partial_owner["runner_status"],
            "detail": partial_owner["missing_owner_clauses"],
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "status_id": "STATUS4791_2_physical_cg",
            "status": physical_cg["runner_status"],
            "detail": physical_cg["missing_inputs"],
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "status_id": "STATUS4791_3_finite_cg",
            "status": finite_cg["runner_status"],
            "detail": f"epsilon={finite_cg['epsilon_cg_total_abs']}",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "next_id": "NEXT4791_0_4792",
            "next_target": NEXT_TARGET,
            "objective": "derive Cperp exactness plus boundary silence for the q/null route, or fill a real c_g units/projection source pack",
            "include": "Cperp exactness; presymplectic kernel; boundary primitive silence; Xhat normalization; c_g source; tau_R10/tau_PPN/tau_clock/tau_orbital",
            "exclude": "q by declaration; vertical by label; WEP-only shortcut; orbital GM backfill; local-GR/Newton claim",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
    ]


def validation_rows(timestamp: str) -> list[dict[str, Any]]:
    sources = parse_csv(SOURCE_REGISTER_CSV)
    functors = parse_csv(FUNCTOR_OUTPUT_CSV)
    cg_rows = parse_csv(CG_OUTPUT_CSV)
    owners = parse_csv(OWNER_OUTPUT_CSV)
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

    physical_functor = next(row for row in functors if row["functor_id"] == "physical_qmatter_functor_attempt")
    q_only = next(row for row in functors if row["functor_id"] == "q_vertical_only_not_enough")
    conditional_functor = next(row for row in functors if row["functor_id"] == "conditional_qmatter_source_frame_packet")
    forbidden_functor = next(row for row in functors if row["functor_id"] == "forbidden_q_by_declaration_control")
    physical_cg = next(row for row in cg_rows if row["cg_id"] == "physical_cg_first_row_missing")
    finite_cg = next(row for row in cg_rows if row["cg_id"] == "finite_cg_projection_smoke")
    zero_cg = next(row for row in cg_rows if row["cg_id"] == "conditional_qmatter_cg_zero")
    forbidden_cg = next(row for row in cg_rows if row["cg_id"] == "forbidden_cg_orbital_backfill")
    partial_owner = next(row for row in owners if row["owner_id"] == "conditional_qmatter_partial_source_object")
    full_owner = next(row for row in owners if row["owner_id"] == "conditional_full_source_object_control")

    add("VAL4791_0_sources", "all cited sources exist and needles are found", all(bool_text(row["exists"]) and bool_text(row["needle_found"]) for row in sources), str(SOURCE_REGISTER_CSV))
    add("VAL4791_1_physical_functor_blocks", "physical q/matter functor remains blocked", physical_functor["runner_status"] == "QMAP_MATTER_FUNCTOR_PARTIAL_BLOCKED_NONCLAIM" and "parent_q_map_signed" in physical_functor["missing_functor_clauses"], str(FUNCTOR_OUTPUT_CSV))
    add("VAL4791_2_q_only_not_enough", "q/vertical alone does not close matter functor", q_only["runner_status"] == "QMAP_MATTER_FUNCTOR_PARTIAL_BLOCKED_NONCLAIM" and "matter_action_factorized" in q_only["missing_functor_clauses"], str(FUNCTOR_OUTPUT_CSV))
    add("VAL4791_3_conditional_functor_supplies_owner_subset", "conditional q/matter functor supplies partial source-object clauses", conditional_functor["runner_status"] == "QMAP_MATTER_FUNCTOR_TO_SOURCE_OBJECT_PARTIAL_OWNER_NONCLAIM" and "source_worldtube_support_signed" in conditional_functor["source_object_clauses_supplied"], str(FUNCTOR_OUTPUT_CSV))
    add("VAL4791_4_forbidden_functor_fails", "q by declaration / vertical by label fails", forbidden_functor["runner_status"] == "FAILED_QMAP_MATTER_FUNCTOR_GATE", str(FUNCTOR_OUTPUT_CSV))
    add("VAL4791_5_physical_cg_blocks", "physical c_g row remains missing", physical_cg["runner_status"] == "BLOCKED_MISSING_CG_FRAME_LEAK_INPUTS", str(CG_OUTPUT_CSV))
    add("VAL4791_6_finite_cg_computes", "finite c_g projection smoke computes", finite_cg["runner_status"] == "CG_FRAME_LEAK_ROW_COMPUTED_NONCLAIM" and finite_cg["epsilon_cg_total_abs"] != "MISSING_NUMERIC_VALUE", str(CG_OUTPUT_CSV))
    add("VAL4791_7_zero_cg_passes_conditional", "conditional q/matter zero theorem zeros c_g", zero_cg["runner_status"] == "CG_ZERO_BY_QMATTER_FUNCTOR_PRIVATE_OR_CONDITIONAL_NONCLAIM", str(CG_OUTPUT_CSV))
    add("VAL4791_8_forbidden_cg_fails", "forbidden c_g backfill fails", forbidden_cg["runner_status"] == "FAILED_CIRCULAR_CG_FRAME_LEAK_ROW", str(CG_OUTPUT_CSV))
    add("VAL4791_9_partial_owner_still_blocks", "q/matter partial owner still lacks Hamiltonian/topology source-object clauses", partial_owner["runner_status"] == "SAME_SOURCE_OBJECT_OWNER_PARTIAL_BLOCKED_NONCLAIM" and "hamiltonian_charge_integrable" in partial_owner["missing_owner_clauses"], str(OWNER_OUTPUT_CSV))
    add("VAL4791_10_full_owner_control_zero", "full source-object control still zeros when all clauses signed", full_owner["runner_status"].startswith("SAME_SOURCE_OBJECT_OWNER_ZERO"), str(OWNER_OUTPUT_CSV))
    add("VAL4791_11_claim", "claim register includes L-633 as nonclaim", CLAIM_ID in read_text(CLAIMS_PATH), str(CLAIMS_PATH))
    add("VAL4791_12_resume", "resume points at 4792", NEXT_TARGET in read_text(RESUME_PATH), str(RESUME_PATH))
    add("VAL4791_OVERALL", "all 4791 q/matter functor checks pass", all(row["result"] == "PASS" for row in validation), DECISION)
    return validation


def write_claim(timestamp: str) -> None:
    if CLAIMS_PATH.exists() and any(row.get("claim_id") == CLAIM_ID for row in parse_csv(CLAIMS_PATH)):
        return
    with CLAIMS_PATH.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = reader.fieldnames or []
    row = {
        "claim_id": CLAIM_ID,
        "domain": "qmap_matter_functor_source_gate_runner",
        "claim": "4791 installs a q-map/matter-functor-to-source-object gate and first c_g frame-leak row; physical q/functor remains unsigned while conditional functor supplies only partial source-object ownership.",
        "current_evidence": "Generated source register, q/matter functor input/output, c_g frame-leak input/output, source-object owner handoff, gates, firewalls, route, decision, status, next target and validation.",
        "status": "qmatter_functor_private_nonclaim_physical_branch_unsigned_cg_row_unfilled",
        "next_test": NEXT_TARGET,
        "key_risk": "Do not treat q by declaration, vertical by label, or WEP-only silence as c_g/source-object proof.",
        "sector": "local_gr",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "q by declaration; vertical by label; c_g without projections; partial functor promoted to source-object closure",
        "title": "q/matter functor source-object gate",
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

4791 installed the parent `q`/matter-functor-to-source-object gate. Conditional q/matter functor ownership can supply the single observed frame, source support and Hilbert-current clauses, and it zeros `c_g` only in that conditional/private branch. Current physical MTS still has not parent-signed `q`, `v_X in ker(Dq)`, matter action factorization, constants/geometry descent, boundary no-tail, hidden-visible morphism silence or readout closure. Even if q/matter closes, Hamiltonian `M_H_ref`, `Pi_M`, topology, `B_zero`, no-exchange/projector/radial silence remain separate source-object gates.

## Firewalls

- No `q` by declaration.
- No `v_X in ker(Dq)` by label.
- No WEP-only shortcut for common `c_g`.
- No c_g scoring without value, units, source path and arena projections.
- No local-GR/Newton/PPN/R10 claim from this checkpoint.
"""
    write_text(RESUME_PATH, content)


def write_docs(timestamp: str) -> None:
    sources = parse_csv(SOURCE_REGISTER_CSV)
    functors = parse_csv(FUNCTOR_OUTPUT_CSV)
    cg_rows = parse_csv(CG_OUTPUT_CSV)
    owners = parse_csv(OWNER_OUTPUT_CSV)
    gates = parse_csv(FUNCTOR_GATE_CSV)
    promotions = parse_csv(PROMOTION_GATES_CSV)
    firewall_rows = parse_csv(FIREWALL_CSV)
    route_rows = parse_csv(ROUTE_MATRIX_CSV)
    decision_rows = parse_csv(DECISION_CSV)
    statuses = parse_csv(STATUS_CSV)
    validation = parse_csv(VALIDATION_CSV)

    content = f"""# 4791 - Parent q-map/matter functor to source object or first frame-leak row

Marker: `{MARKER}`
Generated: `{timestamp}`
Decision: `{DECISION}`

## Result

4791 tests the upstream source-object route:

```text
parent q + v_X in ker(Dq) + observed coframe functor
  + matter action factorization
  + quotient-owned constants/geometry/boundary/readout closure
    => single observed frame, source support, Hilbert current variation
    => c_g = 0 inside that conditional/private branch
```

That is **not** a full source-object proof. It still does not derive the Hamiltonian mass `M_H_ref`, Hamiltonian `Pi_M`, topological representative, `B_zero`, no-exchange/projector/radial silence, or PPN followthrough. The physical branch also still lacks the parent q/null proof, so the first `c_g` row remains a strict source/projection acquisition row.

## Source Register

{markdown_table(sources, ["source_id", "source_path", "exists", "needle_found", "role"])}

## q/matter Functor Output

{markdown_table(functors, ["functor_id", "Z_qmatter", "Z_cg", "Z_frame", "runner_status", "missing_functor_clauses", "source_object_clauses_supplied"])}

## c_g Frame-Leak Output

{markdown_table(cg_rows, ["cg_id", "c_g", "epsilon_cg_R10", "epsilon_cg_PPN_gamma", "epsilon_cg_PPN_beta", "epsilon_cg_clock", "epsilon_cg_WEP", "epsilon_cg_orbital", "epsilon_cg_total_abs", "runner_status"])}

## Source-Object Owner Handoff

{markdown_table(owners, ["owner_id", "R_eq_abs_kg", "B_zero_abs_kg", "runner_status", "missing_owner_clauses"])}

## Functor Gates

{markdown_table(gates, ["gate_id", "claim", "gate_pass", "status"])}

## Promotion Gates

{markdown_table(promotions, ["gate_id", "claim", "gate_pass", "reason", "evidence"])}

## Firewalls

{markdown_table(firewall_rows, ["firewall_id", "rule", "status"])}

## Route Selection

{markdown_table(route_rows, ["route_id", "route", "selection_status"])}

## Decision Ledger

{markdown_table(decision_rows, ["decision_id", "decision", "reason", "next_action"])}

## Status

{markdown_table(statuses, ["status_id", "status", "detail"])}

## Validation

{markdown_table(validation, ["check_id", "description", "result", "evidence"])}

## Next Target

`{NEXT_TARGET}`
"""
    write_text(DOC_PATH, content)
    write_text(FORMAL_PATH, content.replace("# 4791 -", "# 807 - PPC4161 "))

    append_once(
        SPINE_PATH,
        MARKER,
        f"""
## {MARKER}

- 4791 shows the q/matter-functor route can only be a partial source-object owner: it can supply observed-frame/source-support/Hilbert-current clauses if fully signed, but it does not derive Hamiltonian mass, `Pi_M`, topology, `B_zero`, exchange/projector/radial silence or PPN followthrough.
- Physical MTS still does not parent-sign `q`, `v_X in ker(Dq)`, matter factorization, constants/geometry descent, boundary no-tail, hidden-visible morphism silence or readout closure.
- The first `c_g` frame-leak row is executable but remains unfilled until value, units, source paths and arena projections exist.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## {PACKET_MARKER}

4791 adds the q-map/matter-functor-to-source-object gate and first `c_g` frame-leak row to the private local packet. Conditional q/matter ownership zeros `c_g` only in a private/conditional branch and supplies only partial source-object clauses. Next target: `{NEXT_TARGET}`.
""",
    )


def main() -> int:
    timestamp = now()
    write_csv(SOURCE_REGISTER_CSV, source_register(timestamp))
    write_csv(FUNCTOR_INPUT_CSV, functor_input_rows(timestamp))
    write_csv(CG_INPUT_CSV, cg_input_rows(timestamp))
    run_command([sys.executable, str(FUNCTOR_RUNNER), str(FUNCTOR_INPUT_CSV), str(FUNCTOR_OUTPUT_CSV), str(CG_INPUT_CSV), str(CG_OUTPUT_CSV)])

    write_csv(OWNER_INPUT_CSV, owner_input_rows(timestamp))
    write_csv(PROFILE_INPUT_CSV, profile_input_rows(timestamp))
    run_command([sys.executable, str(OWNER_RUNNER), str(OWNER_INPUT_CSV), str(OWNER_OUTPUT_CSV), str(PROFILE_INPUT_CSV), str(PROFILE_OUTPUT_CSV)])

    functors = parse_csv(FUNCTOR_OUTPUT_CSV)
    cg_rows = parse_csv(CG_OUTPUT_CSV)
    owners = parse_csv(OWNER_OUTPUT_CSV)
    write_csv(FUNCTOR_GATE_CSV, gate_rows(timestamp, functors, owners, cg_rows))
    write_csv(PROMOTION_GATES_CSV, promotion_rows(timestamp, functors, owners))
    write_csv(FIREWALL_CSV, firewalls(timestamp))
    write_csv(ROUTE_MATRIX_CSV, routes(timestamp))
    write_csv(DECISION_CSV, decisions(timestamp))
    write_csv(STATUS_CSV, status_rows(timestamp, functors, owners, cg_rows))
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
