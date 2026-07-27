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

CHECKPOINT = "4790"
CLAIM_ID = "L-632"
MARKER = "PPC4161_PARENT_OWN_SAME_SOURCE_OBJECT_OR_FILL_REQ_BZERO_FINITE_SHELL_PROFILE_4790"
PACKET_MARKER = "PPC4161_PACKET_PARENT_OWN_SAME_SOURCE_OBJECT_OR_FILL_REQ_BZERO_FINITE_SHELL_PROFILE_4790"
DECISION = "SAME_SOURCE_OBJECT_OWNER_GATE_INSTALLED_PHYSICAL_BRANCH_UNSIGNED_FINITE_SHELL_PROFILE_EXECUTABLE_NONCLAIM"
NEXT_TARGET = "4791-Y5-R2FR-parent-qmap-matter-functor-to-source-object-or-first-frame-leak-row.md"

DOC_PATH = POST / "4790-Y5-R2FR-parent-own-same-source-object-or-fill-Req-Bzero-finite-shell-profile.md"
FORMAL_PATH = FORMAL / "806-PPC4161-parent-own-same-source-object-or-fill-Req-Bzero-finite-shell-profile.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"

OWNER_RUNNER = SCRIPT_DIR / "same_source_object_profile_runner.py"
CLOSURE_RUNNER = SCRIPT_DIR / "controlled_residual_closure_testbench_runner.py"

SOURCE_REGISTER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4790_SOURCE_REGISTER.csv"
OWNER_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4790_SAME_SOURCE_OBJECT_OWNER_INPUT.csv"
OWNER_OUTPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4790_SAME_SOURCE_OBJECT_OWNER_OUTPUT.csv"
PROFILE_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4790_FINITE_SHELL_PROFILE_INPUT.csv"
PROFILE_OUTPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4790_FINITE_SHELL_PROFILE_OUTPUT.csv"
CLOSURE_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4790_CONTROLLED_RESIDUAL_CLOSURE_INPUT.csv"
CLOSURE_COMPONENT_OUTPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4790_CONTROLLED_RESIDUAL_CLOSURE_COMPONENT_OUTPUT.csv"
CLOSURE_AGGREGATE_OUTPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4790_CONTROLLED_RESIDUAL_CLOSURE_AGGREGATE_OUTPUT.csv"
OWNER_GATE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4790_OWNER_GATE_DECISION.csv"
PROMOTION_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4790_PROMOTION_GATES.csv"
FIREWALL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4790_FIREWALL_ROWS.csv"
ROUTE_MATRIX_CSV = SOURCE_DIR / "P8_Y5_R2FR_4790_ROUTE_SELECTION_MATRIX.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4790_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4790_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4790_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4790_VALIDATION.csv"

SOURCE_SPECS = [
    ("SRC4790_00_4789_doc", POST / "4789-Y5-R2FR-derive-Req-Bzero-same-current-identity-or-source-testbench-bound.md", "same-source-object owner theorem", "4789 owner theorem handoff"),
    ("SRC4790_01_1153_same_object", POST / "1153-Y5-R10-topological-PiM-Hilbert-equality-parent-signature-or-R_eq-source-fill.md", "same-object theorem", "conditional same-object de Rham theorem"),
    ("SRC4790_02_1154_source_owner", POST / "1154-Y5-R10-parent-worldtube-Hilbert-current-owner-or-R_eq-profile-builder.md", "source object ownership law", "source owner audit"),
    ("SRC4790_03_1155_coframe", POST / "1155-Y5-R10-single-observed-coframe-source-frame-owner-or-frame-residual-row.md", "single observed coframe", "observed frame gate"),
    ("SRC4790_04_1156_functor", POST / "1156-Y5-R10-parent-quotient-matter-functor-signature-or-frame-leak-bound-fill.md", "Quotient Matter Functor Signature Audit", "q/matter functor gate"),
    ("SRC4790_05_parent_contract", SOURCE_DIR / "P8_Y5_HILBERT_WORLDTUBE_PARENT_ACTION_CONTRACT.csv", "PAC537_1_single_observed_source_frame", "parent source-object contract"),
    ("SRC4790_06_glue_attempt", SOURCE_DIR / "P8_Y5_HILBERT_WORLDTUBE_GLUE_THEOREM_ATTEMPT.csv", "HWT536_0_parent_worldtube_fixed", "Hilbert worldtube glue attempt"),
    ("SRC4790_07_hamiltonian_contract", SOURCE_DIR / "P8_Y5_HAMILTONIAN_SOURCE_MEASURE_CONTRACT.csv", "HSM541_1_integrable_charge", "Hamiltonian source measure contract"),
    ("SRC4790_08_descent_gate", SOURCE_DIR / "P8_Y5_R10_944_DESCENT_PROOF_GATE.csv", "QDG944_7_total", "quotient descent gate"),
    ("SRC4790_09_owner_runner", OWNER_RUNNER, "def owner_row", "same source-object/profile runner"),
]

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

CLOSURE_COMPONENTS = (
    "R_eq",
    "B_zero",
    "boundary_flux",
    "open_EM",
    "nonEM_owner_gap",
    "projector_comm",
    "domain_shadow",
    "kappa_drift",
)

CLOSURE_CLAUSES = (
    "same_parent_branch_signed",
    "controlled_Ttotal_profile_signed",
    "variation_before_readout_signed",
    "same_frame_signed",
    "no_postfit_signed",
    "same_current_identity_signed",
    "Bzero_primitive_signed",
    "compact_test_support_signed",
    "boundary_collar_silent_signed",
    "no_wall_stress_signed",
    "fixed_boundary_data_signed",
    "poynting_once_signed",
    "fixed_EM_hodge_signed",
    "no_radiative_collar_flux_signed",
    "hilbert_only_source_signed",
    "no_spin_torsion_nonhilbert_signed",
    "no_decoupled_source_block_signed",
    "projector_commutes_signed",
    "readout_postprocess_signed",
    "no_source_worldtube_reentry_signed",
    "fixed_domain_signed",
    "qbasic_support_signed",
    "no_birth_death_shell_signed",
    "kappa_lock_signed",
    "source_measure_lock_signed",
    "no_running_kappa_signed",
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
    signed = owner_clause_map(True)
    frame_only = owner_clause_map(False)
    for clause in ("parent_action_variation_signed", "single_observed_frame_signed", "quotient_matter_functor_signed", "no_tautological_definition_signed", "no_postfit_readout_signed"):
        frame_only[clause] = True
    return [
        owner_row("physical_same_source_owner_attempt", "physical_branch_nonclaim", "4789_PHYSICAL_BRANCH_PLUS_1153_1156_SOURCE_OWNER_AUDIT", timestamp, physical),
        owner_row("conditional_same_source_owner_packet", "conditional_reference_theorem_nonclaim", "CONDITIONAL_SOURCE_OBJECT_PACKET_ALL_CLAUSES_SIGNED", timestamp, signed),
        owner_row("frame_functor_only_not_enough", "conditional_frame_functor_only_smoke_nonclaim", "FRAME_FUNCTOR_WITHOUT_HAMILTONIAN_TOPOLOGY_SOURCE_OBJECT", timestamp, frame_only),
        owner_row("forbidden_readout_source_owner_control", "forbidden_control_nonclaim", "ORBITAL_GM_DEFINITION_DEFINE_JM_TOP_FROM_PIM_JH", timestamp, signed),
    ]


def profile_row(profile_id: str, system_id: str, branch_id: str, values: dict[str, Any], source: str, status: str, timestamp: str) -> dict[str, Any]:
    row = {
        "profile_id": profile_id,
        "system_id": system_id,
        "branch_id": branch_id,
        "r_inner_m": values.get("r_inner_m", ""),
        "r_outer_m": values.get("r_outer_m", ""),
        "PiM_JH_integral_kg": values.get("PiM_JH_integral_kg", ""),
        "JM_top_integral_kg": values.get("JM_top_integral_kg", ""),
        "Bzero_primitive_integral_kg": values.get("Bzero_primitive_integral_kg", ""),
        "Bzero_boundary_flux_abs_kg": values.get("Bzero_boundary_flux_abs_kg", ""),
        "boundary_reference_shift_abs_kg": values.get("boundary_reference_shift_abs_kg", ""),
        "collar_flux_abs_kg": values.get("collar_flux_abs_kg", ""),
        "frame_mismatch_abs_kg": values.get("frame_mismatch_abs_kg", ""),
        "extra_exchange_abs_kg": values.get("extra_exchange_abs_kg", ""),
        "projector_commutator_abs_kg": values.get("projector_commutator_abs_kg", ""),
        "radial_nonclosure_abs_kg": values.get("radial_nonclosure_abs_kg", ""),
        "M_H_ref_kg": values.get("M_H_ref_kg", ""),
        "profile_source": source,
        "source_path": source,
        "zero_theorem_path": values.get("zero_theorem_path", ""),
        "provenance": source,
        "notes": values.get("notes", ""),
        "row_status": status,
        "valid_for_claim": False,
        "timestamp_utc": timestamp,
    }
    return row


def profile_input_rows(timestamp: str) -> list[dict[str, Any]]:
    missing_values = {field: f"MISSING_{field.upper()}" for field in (
        "PiM_JH_integral_kg",
        "JM_top_integral_kg",
        "Bzero_primitive_integral_kg",
        "Bzero_boundary_flux_abs_kg",
        "boundary_reference_shift_abs_kg",
        "collar_flux_abs_kg",
        "frame_mismatch_abs_kg",
        "extra_exchange_abs_kg",
        "projector_commutator_abs_kg",
        "radial_nonclosure_abs_kg",
        "M_H_ref_kg",
    )}
    finite = {
        "r_inner_m": "1.0",
        "r_outer_m": "2.0",
        "PiM_JH_integral_kg": "1.003",
        "JM_top_integral_kg": "1.0015",
        "Bzero_primitive_integral_kg": "0.0005",
        "Bzero_boundary_flux_abs_kg": "5.0e-5",
        "boundary_reference_shift_abs_kg": "2.0e-5",
        "collar_flux_abs_kg": "3.0e-5",
        "frame_mismatch_abs_kg": "1.0e-4",
        "extra_exchange_abs_kg": "2.0e-4",
        "projector_commutator_abs_kg": "3.0e-4",
        "radial_nonclosure_abs_kg": "4.0e-4",
        "M_H_ref_kg": "1.0",
    }
    zero = {key: "0" for key in finite}
    zero["r_inner_m"] = "1.0"
    zero["r_outer_m"] = "2.0"
    zero["PiM_JH_integral_kg"] = "1.0"
    zero["JM_top_integral_kg"] = "1.0"
    zero["M_H_ref_kg"] = "1.0"
    return [
        profile_row("physical_finite_shell_profile_missing", "physical_local_source", "physical_same_source_owner_attempt", missing_values, "MISSING_SOURCE_FILE", "physical_profile_missing_nonclaim", timestamp),
        profile_row("finite_shell_profile_smoke", "controlled_source_smoke", "finite_profile_testbench", finite, str(PROFILE_INPUT_CSV), "finite_profile_testbench_nonclaim", timestamp),
        profile_row("private_zero_source_object_profile", "private_zero_source", "private_zero_testbench", zero, str(PROFILE_INPUT_CSV), "private_zero_profile_nonclaim", timestamp),
        profile_row("forbidden_orbital_profile_backfill", "forbidden_source", "forbidden_control", zero, "ORBITAL_GM_DEFINITION_OBSERVED_RESIDUAL_CANCEL", "forbidden_control_nonclaim", timestamp),
    ]


def closure_clause_map(value: bool) -> dict[str, bool]:
    return {clause: value for clause in CLOSURE_CLAUSES}


def partial_closure_clauses() -> dict[str, bool]:
    clauses = closure_clause_map(False)
    for clause in (
        "same_parent_branch_signed",
        "controlled_Ttotal_profile_signed",
        "variation_before_readout_signed",
        "same_frame_signed",
        "no_postfit_signed",
        "poynting_once_signed",
        "fixed_EM_hodge_signed",
        "no_radiative_collar_flux_signed",
        "kappa_lock_signed",
        "source_measure_lock_signed",
        "no_running_kappa_signed",
    ):
        clauses[clause] = True
    return clauses


def closure_row(closure_id: str, symbol: str, status: str, source: str, timestamp: str, clauses: dict[str, bool], bound: str = "") -> dict[str, Any]:
    return {
        "closure_id": closure_id,
        "component_symbol": symbol,
        "residual_bound_abs_kg": bound,
        "closure_source": source,
        "bound_source": source,
        "component_source": source,
        "provenance": source,
        "notes": "",
        "row_status": status,
        "valid_for_claim": False,
        "timestamp_utc": timestamp,
        **clauses,
    }


def closure_input_rows(timestamp: str, profile_outputs: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    partial = partial_closure_clauses()
    signed = closure_clause_map(True)
    finite_profile = next(row for row in profile_outputs if row["profile_id"] == "finite_shell_profile_smoke")

    for symbol in CLOSURE_COMPONENTS:
        rows.append(closure_row("physical_after_4790_source_owner_attempt", symbol, "physical_source_owner_attempt_nonclaim", "4790_PHYSICAL_OWNER_GATE_UNSIGNED", timestamp, partial))

    for symbol in CLOSURE_COMPONENTS:
        if symbol == "R_eq":
            rows.append(closure_row("finite_profile_reduces_Req_Bzero_pair", symbol, "finite_profile_bound_nonclaim", "4790_FINITE_PROFILE_REQ_BOUND", timestamp, partial, bound=finite_profile["R_eq_integral_abs_kg"]))
        elif symbol == "B_zero":
            rows.append(closure_row("finite_profile_reduces_Req_Bzero_pair", symbol, "finite_profile_bound_nonclaim", "4790_FINITE_PROFILE_BZERO_BOUND", timestamp, partial, bound=finite_profile["B_zero_abs_kg"]))
        else:
            rows.append(closure_row("finite_profile_reduces_Req_Bzero_pair", symbol, "other_components_still_gate_nonclaim", "4790_OTHER_RESIDUALS_STILL_USE_PARTIAL_CLAUSES", timestamp, partial))

    for symbol in CLOSURE_COMPONENTS:
        rows.append(closure_row("conditional_source_object_closure_smoke", symbol, "conditional_source_object_private_nonclaim", "4790_CONDITIONAL_SOURCE_OBJECT_ALL_CLAUSES_SIGNED", timestamp, signed))

    return rows


def owner_gate_rows(timestamp: str, owner_outputs: list[dict[str, str]]) -> list[dict[str, Any]]:
    physical = next(row for row in owner_outputs if row["owner_id"] == "physical_same_source_owner_attempt")
    conditional = next(row for row in owner_outputs if row["owner_id"] == "conditional_same_source_owner_packet")
    frame_only = next(row for row in owner_outputs if row["owner_id"] == "frame_functor_only_not_enough")
    return [
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "SOG4790_0_conditional_owner",
            "claim": "same source-object packet zeros R_eq/B_zero",
            "gate_pass": conditional["runner_status"].startswith("SAME_SOURCE_OBJECT_OWNER_ZERO"),
            "status": conditional["runner_status"],
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "SOG4790_1_physical_owner",
            "claim": "current physical MTS parent-owns the same source object",
            "gate_pass": False,
            "status": physical["runner_status"],
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "SOG4790_2_frame_functor_not_enough",
            "claim": "q/matter frame functor alone owns the source charge",
            "gate_pass": False,
            "status": frame_only["runner_status"],
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def promotion_rows(timestamp: str, owner_outputs: list[dict[str, str]], profile_outputs: list[dict[str, str]]) -> list[dict[str, Any]]:
    physical_owner = next(row for row in owner_outputs if row["owner_id"] == "physical_same_source_owner_attempt")
    finite_profile = next(row for row in profile_outputs if row["profile_id"] == "finite_shell_profile_smoke")
    return [
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "PG4790_0_source_object",
            "claim": "source object owner theorem can promote same-current equality",
            "gate_pass": False,
            "reason": "physical branch has unsigned owner clauses",
            "evidence": physical_owner["missing_owner_clauses"],
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "PG4790_1_profile_interface",
            "claim": "finite-shell profile interface computes an honest nonclaim envelope",
            "gate_pass": finite_profile["runner_status"] == "SAME_SOURCE_PROFILE_COMPUTED_NONCLAIM",
            "reason": "profile computes R_eq, B_zero and retained source-object envelope from upstream fields",
            "evidence": finite_profile["epsilon_same_source_abs"],
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "PG4790_2_no_local_GR",
            "claim": "local GR/Newton claim allowed",
            "gate_pass": False,
            "reason": "same source object, other residuals, and PPN followthrough remain unsigned",
            "evidence": "nonclaim firewall active",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def firewalls(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("FW4790_0_no_source_by_readout", "source worldtube and surfaces must be fixed before orbital/radial readout"),
        ("FW4790_1_no_bare_mass", "M_H_ref must be dressed Hamiltonian/Noether charge, not bare rest mass"),
        ("FW4790_2_no_topological_label", "omega_M_top cannot be an independent conserved label detached from J_H"),
        ("FW4790_3_no_boundary_tuning", "B_zero/reference/collar terms cannot be tuned per system"),
        ("FW4790_4_no_frame_functor_shortcut", "q/matter functor alone is insufficient without Hamiltonian charge/topology/boundary ownership"),
        ("FW4790_5_no_local_claim", "no local-GR/Newton/PPN claim follows from this checkpoint"),
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
        ("RT4790_0_q_matter_functor", "derive q-map and matter functor as parent data for the observed frame", "SELECTED_NEXT"),
        ("RT4790_1_Hamiltonian_charge", "derive integrable M_H_ref and Pi_M Hamiltonian map in the same branch", "SELECTED_NEXT_PARALLEL"),
        ("RT4790_2_profile_fill", "if theorem route fails, fill finite-shell profile with real source/current integrals", "SELECTED_FALLBACK"),
        ("RT4790_3_remaining_residuals", "after source-object pair closes, return to boundary/nonHilbert/projector/domain residuals", "QUEUED"),
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
            "decision_id": "DEC4790_0_owner_packet",
            "decision": "same_source_object_packet_is_the_real_R_eq_Bzero_parent_requirement",
            "reason": "the same-current identity only becomes physical when observed frame, source worldtube, Hilbert variation, Hamiltonian charge, topological representative, boundary primitive and no-exchange/projector silence are one parent object",
            "next_action": "derive the upstream q/matter functor and Hamiltonian charge clauses",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "decision_id": "DEC4790_1_current_branch",
            "decision": "current_physical_branch_unsigned",
            "reason": "old contract rows keep q/matter functor, source worldtube, charge integrability, Pi_M map, topology and extra-sector silence unproved",
            "next_action": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "decision_id": "DEC4790_2_profile",
            "decision": "finite_shell_profile_interface_is_ready",
            "reason": "R_eq, B_zero and retained source-object terms can now be computed from explicit shell/profile columns without using GM backfill",
            "next_action": "fill real source rows only after parent/current definitions exist",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def status_rows(timestamp: str, owner_outputs: list[dict[str, str]], profile_outputs: list[dict[str, str]], closure_outputs: list[dict[str, str]]) -> list[dict[str, Any]]:
    physical_owner = next(row for row in owner_outputs if row["owner_id"] == "physical_same_source_owner_attempt")
    finite_profile = next(row for row in profile_outputs if row["profile_id"] == "finite_shell_profile_smoke")
    finite_closure = next(row for row in closure_outputs if row["closure_id"] == "finite_profile_reduces_Req_Bzero_pair")
    return [
        {
            "checkpoint": CHECKPOINT,
            "status_id": "STATUS4790_0_physical_owner",
            "status": physical_owner["runner_status"],
            "detail": physical_owner["missing_owner_clauses"],
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "status_id": "STATUS4790_1_profile",
            "status": finite_profile["runner_status"],
            "detail": f"epsilon={finite_profile['epsilon_same_source_abs']}",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "status_id": "STATUS4790_2_closure",
            "status": finite_closure["runner_status"],
            "detail": f"bound={finite_closure['bound_component_count']};missing={finite_closure['missing_component_count']}",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "next_id": "NEXT4790_0_4791",
            "next_target": NEXT_TARGET,
            "objective": "derive q-map/matter-functor ownership into the same source object, or fill the first real frame-leak/source-object row",
            "include": "q:Phi->Q_obs; e_obs(q); S_matter factorization; constants descent; Hamiltonian charge; c_g/Delta_frame fallback",
            "exclude": "q by declaration; source by readout; orbital GM backfill; local-GR/Newton claim",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
    ]


def validation_rows(timestamp: str) -> list[dict[str, Any]]:
    sources = parse_csv(SOURCE_REGISTER_CSV)
    owners = parse_csv(OWNER_OUTPUT_CSV)
    profiles = parse_csv(PROFILE_OUTPUT_CSV)
    closures = parse_csv(CLOSURE_AGGREGATE_OUTPUT_CSV)
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

    physical_owner = next(row for row in owners if row["owner_id"] == "physical_same_source_owner_attempt")
    conditional_owner = next(row for row in owners if row["owner_id"] == "conditional_same_source_owner_packet")
    frame_only = next(row for row in owners if row["owner_id"] == "frame_functor_only_not_enough")
    forbidden_owner = next(row for row in owners if row["owner_id"] == "forbidden_readout_source_owner_control")
    physical_profile = next(row for row in profiles if row["profile_id"] == "physical_finite_shell_profile_missing")
    finite_profile = next(row for row in profiles if row["profile_id"] == "finite_shell_profile_smoke")
    private_profile = next(row for row in profiles if row["profile_id"] == "private_zero_source_object_profile")
    forbidden_profile = next(row for row in profiles if row["profile_id"] == "forbidden_orbital_profile_backfill")
    finite_closure = next(row for row in closures if row["closure_id"] == "finite_profile_reduces_Req_Bzero_pair")
    conditional_closure = next(row for row in closures if row["closure_id"] == "conditional_source_object_closure_smoke")

    add("VAL4790_0_sources", "all cited sources exist and needles are found", all(bool_text(row["exists"]) and bool_text(row["needle_found"]) for row in sources), str(SOURCE_REGISTER_CSV))
    add("VAL4790_1_physical_owner_blocks", "physical source-object owner remains blocked", physical_owner["runner_status"] == "SAME_SOURCE_OBJECT_OWNER_PARTIAL_BLOCKED_NONCLAIM" and "quotient_matter_functor_signed" in physical_owner["missing_owner_clauses"], str(OWNER_OUTPUT_CSV))
    add("VAL4790_2_conditional_owner_zero", "conditional source-object packet zeros R_eq/B_zero", conditional_owner["runner_status"].startswith("SAME_SOURCE_OBJECT_OWNER_ZERO"), str(OWNER_OUTPUT_CSV))
    add("VAL4790_3_frame_only_blocks", "frame functor alone does not own source object", frame_only["runner_status"] == "SAME_SOURCE_OBJECT_OWNER_PARTIAL_BLOCKED_NONCLAIM" and "hamiltonian_charge_integrable" in frame_only["missing_owner_clauses"], str(OWNER_OUTPUT_CSV))
    add("VAL4790_4_forbidden_owner_fails", "readout/tautological source owner fails", forbidden_owner["runner_status"] == "FAILED_SAME_SOURCE_OBJECT_OWNER_GATE", str(OWNER_OUTPUT_CSV))
    add("VAL4790_5_physical_profile_blocks", "physical finite-shell profile remains missing", physical_profile["runner_status"] == "BLOCKED_MISSING_SAME_SOURCE_PROFILE_INPUTS", str(PROFILE_OUTPUT_CSV))
    add("VAL4790_6_finite_profile_computes", "finite-shell profile computes nonclaim envelope", finite_profile["runner_status"] == "SAME_SOURCE_PROFILE_COMPUTED_NONCLAIM" and finite_profile["epsilon_same_source_abs"] != "MISSING_NUMERIC_VALUE", str(PROFILE_OUTPUT_CSV))
    add("VAL4790_7_private_profile_zero", "private source-object profile zeros", private_profile["runner_status"] == "SAME_SOURCE_PROFILE_ZERO_PRIVATE_OR_THEOREM_NONCLAIM", str(PROFILE_OUTPUT_CSV))
    add("VAL4790_8_forbidden_profile_fails", "forbidden profile backfill fails", forbidden_profile["runner_status"] == "FAILED_CIRCULAR_SAME_SOURCE_PROFILE", str(PROFILE_OUTPUT_CSV))
    add("VAL4790_9_closure_pair_bound", "finite profile feeds closure runner as R_eq/B_zero bounds", finite_closure["bound_component_count"] == "2" and finite_closure["missing_component_count"] == "4", str(CLOSURE_AGGREGATE_OUTPUT_CSV))
    add("VAL4790_10_conditional_closure_zero", "conditional closure smoke zeros all components", conditional_closure["runner_status"].startswith("CONTROLLED_SOURCE_TESTBENCH_ZERO") or conditional_closure["runner_status"].startswith("CONTROLLED_RESIDUAL_CLOSURE_ZERO"), str(CLOSURE_AGGREGATE_OUTPUT_CSV))
    add("VAL4790_11_claim", "claim register includes L-632 as nonclaim", CLAIM_ID in read_text(CLAIMS_PATH), str(CLAIMS_PATH))
    add("VAL4790_12_resume", "resume points at 4791", NEXT_TARGET in read_text(RESUME_PATH), str(RESUME_PATH))
    add("VAL4790_OVERALL", "all 4790 source-object checks pass", all(row["result"] == "PASS" for row in validation), DECISION)
    return validation


def write_claim(timestamp: str) -> None:
    if CLAIMS_PATH.exists() and any(row.get("claim_id") == CLAIM_ID for row in parse_csv(CLAIMS_PATH)):
        return
    with CLAIMS_PATH.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = reader.fieldnames or []
    row = {
        "claim_id": CLAIM_ID,
        "domain": "same_source_object_profile_runner",
        "claim": "4790 installs the same parent source-object owner gate and finite-shell R_eq/B_zero profile runner; physical branch remains unsigned while conditional/private packets and smoke profiles validate.",
        "current_evidence": "Generated source register, owner input/output, finite-shell profile input/output, closure handoff, gates, firewalls, route, decision, status, next target and validation.",
        "status": "same_source_object_gate_private_nonclaim_physical_branch_unsigned",
        "next_test": NEXT_TARGET,
        "key_risk": "Do not treat frame functor, topological label, bare mass, or readout worldtube as a parent-owned source object.",
        "sector": "local_gr",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "source by readout; topological wrong object; nonintegrable Hamiltonian charge; hidden frame leak",
        "title": "same source-object owner gate",
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

4790 installed the same parent source-object owner gate. The conditional packet closes `R_eq/B_zero`, but the physical branch is still missing the upstream owner stack: parent `q`, quotient/matter functor, single observed frame, source worldtube, Hilbert current variation, integrable `M_H_ref`, Hamiltonian `Pi_M`, topological PD representative, boundary primitive, no-exchange and projector/radial silence. The finite-shell profile runner is ready for real source/current rows, but current physical rows remain missing.

## Firewalls

- No source worldtube chosen from orbital or radial readout.
- No bare mass as `M_H_ref`.
- No independent topological label as measured mass.
- No boundary/reference tuning per system.
- No local-GR/Newton/PPN claim from this checkpoint.
"""
    write_text(RESUME_PATH, content)


def write_docs(timestamp: str) -> None:
    sources = parse_csv(SOURCE_REGISTER_CSV)
    owners = parse_csv(OWNER_OUTPUT_CSV)
    profiles = parse_csv(PROFILE_OUTPUT_CSV)
    closures = parse_csv(CLOSURE_AGGREGATE_OUTPUT_CSV)
    owner_gates = parse_csv(OWNER_GATE_CSV)
    promotions = parse_csv(PROMOTION_GATES_CSV)
    firewall_rows = parse_csv(FIREWALL_CSV)
    route_rows = parse_csv(ROUTE_MATRIX_CSV)
    decision_rows = parse_csv(DECISION_CSV)
    statuses = parse_csv(STATUS_CSV)
    validation = parse_csv(VALIDATION_CSV)

    content = f"""# 4790 - Parent-own same source object or fill R_eq/B_zero finite-shell profile

Marker: `{MARKER}`
Generated: `{timestamp}`
Decision: `{DECISION}`

## Result

4790 attacks the object behind the coupling. The clean theorem is:

```text
same source object =
  parent q/matter functor
  + single observed source/readout frame
  + fixed Hilbert source worldtube
  + Hilbert current variation J_H
  + integrable dressed Hamiltonian mass M_H_ref
  + Hamiltonian Pi_M map
  + topological PD representative omega_M_top
  + fixed exact B_zero primitive
  + no extra/projector/radial mass-charge exchange

If that whole packet is parent-owned, then R_eq = 0 and B_zero = 0.
```

The current physical branch does not yet own that packet. The useful improvement is that a finite-shell profile now exists with explicit columns for `Pi_M J_H`, `J_M_top`, `B_zero`, `M_H_ref`, frame mismatch, extra exchange, projector commutator and radial nonclosure. That is the non-smuggled fallback.

## Source Register

{markdown_table(sources, ["source_id", "source_path", "exists", "needle_found", "role"])}

## Same Source-Object Owner Output

{markdown_table(owners, ["owner_id", "R_eq_abs_kg", "B_zero_abs_kg", "runner_status", "missing_owner_clauses"])}

## Finite-Shell Profile Output

{markdown_table(profiles, ["profile_id", "R_eq_integral_abs_kg", "B_zero_abs_kg", "retained_source_object_abs_kg", "same_source_profile_bound_abs_kg", "M_H_ref_kg", "epsilon_same_source_abs", "runner_status"])}

## Controlled Closure Handoff

{markdown_table(closures, ["closure_id", "Delta_H_abs_kg", "zero_component_count", "bound_component_count", "missing_component_count", "failed_component_count", "runner_status"])}

## Owner Gates

{markdown_table(owner_gates, ["gate_id", "claim", "gate_pass", "status"])}

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
    write_text(FORMAL_PATH, content.replace("# 4790 -", "# 806 - PPC4161 "))

    append_once(
        SPINE_PATH,
        MARKER,
        f"""
## {MARKER}

- 4790 identifies the physical owner of the same-current identity as a same parent source-object packet, not a symbolic equality.
- Physical MTS remains unsigned because q/matter functor, source worldtube, Hilbert variation, integrable `M_H_ref`, Hamiltonian `Pi_M`, topology, boundary primitive, extra exchange and projector/radial clauses are not all parent-owned.
- Finite-shell profile plumbing now computes `R_eq`, `B_zero` and retained source-object envelope from explicit source/current rows without orbital-GM backfill.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## {PACKET_MARKER}

4790 adds the same source-object owner gate and finite-shell `R_eq/B_zero` profile runner to the private local packet. The conditional packet closes the same-current pair; the physical branch remains blocked until the upstream q/matter functor and Hamiltonian source-charge owner stack is derived. Next target: `{NEXT_TARGET}`.
""",
    )


def main() -> int:
    timestamp = now()
    write_csv(SOURCE_REGISTER_CSV, source_register(timestamp))
    write_csv(OWNER_INPUT_CSV, owner_input_rows(timestamp))
    write_csv(PROFILE_INPUT_CSV, profile_input_rows(timestamp))
    run_command([sys.executable, str(OWNER_RUNNER), str(OWNER_INPUT_CSV), str(OWNER_OUTPUT_CSV), str(PROFILE_INPUT_CSV), str(PROFILE_OUTPUT_CSV)])

    profile_outputs = parse_csv(PROFILE_OUTPUT_CSV)
    write_csv(CLOSURE_INPUT_CSV, closure_input_rows(timestamp, profile_outputs))
    run_command([sys.executable, str(CLOSURE_RUNNER), str(CLOSURE_INPUT_CSV), str(CLOSURE_COMPONENT_OUTPUT_CSV), str(CLOSURE_AGGREGATE_OUTPUT_CSV)])

    owner_outputs = parse_csv(OWNER_OUTPUT_CSV)
    closure_outputs = parse_csv(CLOSURE_AGGREGATE_OUTPUT_CSV)
    write_csv(OWNER_GATE_CSV, owner_gate_rows(timestamp, owner_outputs))
    write_csv(PROMOTION_GATES_CSV, promotion_rows(timestamp, owner_outputs, profile_outputs))
    write_csv(FIREWALL_CSV, firewalls(timestamp))
    write_csv(ROUTE_MATRIX_CSV, routes(timestamp))
    write_csv(DECISION_CSV, decisions(timestamp))
    write_csv(STATUS_CSV, status_rows(timestamp, owner_outputs, profile_outputs, closure_outputs))
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
