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

CHECKPOINT = "4789"
CLAIM_ID = "L-631"
MARKER = "PPC4161_DERIVE_REQ_BZERO_SAME_CURRENT_IDENTITY_OR_SOURCE_TESTBENCH_BOUND_4789"
PACKET_MARKER = "PPC4161_PACKET_DERIVE_REQ_BZERO_SAME_CURRENT_IDENTITY_OR_SOURCE_TESTBENCH_BOUND_4789"
DECISION = "SAME_CURRENT_IDENTITY_CONDITIONAL_THEOREM_INSTALLED_PHYSICAL_BRANCH_UNSIGNED_R_EQ_BZERO_BOUND_INTERFACE_READY"
NEXT_TARGET = "4790-Y5-R2FR-parent-own-same-source-object-or-fill-Req-Bzero-finite-shell-profile.md"

DOC_PATH = POST / "4789-Y5-R2FR-derive-Req-Bzero-same-current-identity-or-source-testbench-bound.md"
FORMAL_PATH = FORMAL / "805-PPC4161-derive-Req-Bzero-same-current-identity-or-source-testbench-bound.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"

SAME_CURRENT_RUNNER = SCRIPT_DIR / "same_current_identity_gate_runner.py"
CLOSURE_RUNNER = SCRIPT_DIR / "controlled_residual_closure_testbench_runner.py"

SOURCE_REGISTER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4789_SOURCE_REGISTER.csv"
THEOREM_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4789_SAME_CURRENT_THEOREM_INPUT.csv"
THEOREM_OUTPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4789_SAME_CURRENT_THEOREM_OUTPUT.csv"
BOUND_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4789_REQ_BZERO_BOUND_INPUT.csv"
BOUND_OUTPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4789_REQ_BZERO_BOUND_OUTPUT.csv"
CLOSURE_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4789_CONTROLLED_RESIDUAL_CLOSURE_INPUT.csv"
CLOSURE_COMPONENT_OUTPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4789_CONTROLLED_RESIDUAL_CLOSURE_COMPONENT_OUTPUT.csv"
CLOSURE_AGGREGATE_OUTPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4789_CONTROLLED_RESIDUAL_CLOSURE_AGGREGATE_OUTPUT.csv"
THEOREM_GATE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4789_THEOREM_GATE_DECISION.csv"
PROMOTION_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4789_PROMOTION_GATES.csv"
FIREWALL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4789_FIREWALL_ROWS.csv"
ROUTE_MATRIX_CSV = SOURCE_DIR / "P8_Y5_R2FR_4789_ROUTE_SELECTION_MATRIX.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4789_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4789_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4789_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4789_VALIDATION.csv"

SOURCE_SPECS = [
    ("SRC4789_00_4788_doc", POST / "4788-Y5-R2FR-close-Req-Bzero-boundary-projector-domain-or-controlled-source-testbench.md", "Pi_M J_H = J_M_top+dB_zero", "4788 exact R_eq/B_zero blocker"),
    ("SRC4789_01_1153_theorem", POST / "1153-Y5-R10-topological-PiM-Hilbert-equality-parent-signature-or-R_eq-source-fill.md", "same-object theorem", "conditional de Rham same-current theorem"),
    ("SRC4789_02_1154_owner", POST / "1154-Y5-R10-parent-worldtube-Hilbert-current-owner-or-R_eq-profile-builder.md", "source object ownership law", "source object owner gate"),
    ("SRC4789_03_1155_frame", POST / "1155-Y5-R10-single-observed-coframe-source-frame-owner-or-frame-residual-row.md", "single observed coframe", "same-frame source/readout gate"),
    ("SRC4789_04_4678_tail", SOURCE_DIR / "P8_Y5_R2FR_4678_REQ_BZERO_HTAU_TAIL_CONTRACTS.csv", "TAIL4678_0_R_eq", "R_eq/B_zero tail contract"),
    ("SRC4789_05_4688_boundary", SOURCE_DIR / "P8_Y5_R2FR_4688_BOUNDARY_NONHILBERT_ZERO_THEOREM.csv", "BNH4688_0_boundary_variation", "boundary primitive fallback"),
    ("SRC4789_06_4789_runner", SAME_CURRENT_RUNNER, "def theorem_row", "same-current identity and bound runner"),
    ("SRC4789_07_4788_runner", CLOSURE_RUNNER, "def aggregate_closure", "controlled residual closure runner"),
]

THEOREM_CLAUSES = (
    "same_parent_action_signed",
    "same_observed_frame_signed",
    "source_worldtube_fixed_signed",
    "hilbert_current_variation_owned",
    "hamiltonian_charge_normalized",
    "topological_PD_representative_signed",
    "same_linking_class_signed",
    "exact_boundary_primitive_signed",
    "boundary_flux_zero_signed",
    "no_extra_exchange_signed",
    "projector_commutator_zero_signed",
    "no_tautological_definition_signed",
    "no_readout_worldtube_signed",
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

CONTROLLED_CLOSURE_CLAUSES = (
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


def theorem_clause_map(value: bool) -> dict[str, bool]:
    return {clause: value for clause in THEOREM_CLAUSES}


def theorem_row(branch_id: str, status: str, source: str, timestamp: str, clauses: dict[str, bool]) -> dict[str, Any]:
    return {
        "branch_id": branch_id,
        "theorem_source": source,
        "provenance": source,
        "notes": "",
        "row_status": status,
        "valid_for_claim": False,
        "timestamp_utc": timestamp,
        **clauses,
    }


def theorem_input_rows(timestamp: str) -> list[dict[str, Any]]:
    physical = theorem_clause_map(False)
    for clause in (
        "same_parent_action_signed",
        "no_tautological_definition_signed",
        "no_readout_worldtube_signed",
    ):
        physical[clause] = True

    conditional = theorem_clause_map(True)

    bzero_only = theorem_clause_map(False)
    for clause in (
        "same_parent_action_signed",
        "same_observed_frame_signed",
        "exact_boundary_primitive_signed",
        "boundary_flux_zero_signed",
        "no_tautological_definition_signed",
        "no_readout_worldtube_signed",
    ):
        bzero_only[clause] = True

    return [
        theorem_row(
            "physical_same_current_attempt",
            "physical_branch_nonclaim",
            "4788_PHYSICAL_BRANCH_PLUS_1153_1154_1155_AUDIT",
            timestamp,
            physical,
        ),
        theorem_row(
            "conditional_same_object_derham_theorem",
            "conditional_reference_theorem_nonclaim",
            "1153_SAME_OBJECT_DERHAM_THEOREM_ALL_HYPOTHESES_SIGNED_FOR_THEOREM_TEST",
            timestamp,
            conditional,
        ),
        theorem_row(
            "private_controlled_source_testbench_same_object",
            "private_controlled_testbench_nonclaim",
            "PRIVATE_CONTROLLED_SOURCE_OBJECT_ALL_CLAUSES_SIGNED",
            timestamp,
            conditional,
        ),
        theorem_row(
            "bzero_only_boundary_smoke",
            "conditional_boundary_only_smoke_nonclaim",
            "BOUNDARY_PRIMITIVE_ONLY_DOES_NOT_CLOSE_R_EQ",
            timestamp,
            bzero_only,
        ),
        theorem_row(
            "forbidden_tautological_JMtop_control",
            "forbidden_control_nonclaim",
            "DEFINE_JM_TOP_FROM_PIM_JH_OBSERVED_RESIDUAL_CANCEL",
            timestamp,
            conditional,
        ),
    ]


def bound_input_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "bound_id": "physical_same_current_bound_attempt",
            "R_eq_integral_abs_kg": "MISSING_R_EQ_INTEGRAL",
            "link_charge_mismatch_abs_kg": "MISSING_LINK_CHARGE_MISMATCH",
            "exterior_nonclosure_abs_kg": "MISSING_EXTERIOR_NONCLOSURE",
            "frame_mismatch_abs_kg": "MISSING_FRAME_MISMATCH",
            "extra_exchange_abs_kg": "MISSING_EXTRA_EXCHANGE",
            "projector_commutator_abs_kg": "MISSING_PROJECTOR_COMMUTATOR",
            "B_zero_flux_abs_kg": "MISSING_B_ZERO_FLUX",
            "boundary_reference_shift_abs_kg": "MISSING_REFERENCE_SHIFT",
            "collar_flux_abs_kg": "MISSING_COLLAR_FLUX",
            "M_H_ref_kg": "MISSING_M_H_REF",
            "bound_source": "4788_PHYSICAL_BRANCH_MISSING_SOURCE_ROWS",
            "source_path": "MISSING_SOURCE_FILE",
            "row_status": "physical_bound_missing_nonclaim",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "finite_same_current_bound_testbench",
            "R_eq_integral_abs_kg": "",
            "link_charge_mismatch_abs_kg": "2.0e-4",
            "exterior_nonclosure_abs_kg": "3.0e-4",
            "frame_mismatch_abs_kg": "1.0e-4",
            "extra_exchange_abs_kg": "4.0e-4",
            "projector_commutator_abs_kg": "5.0e-4",
            "B_zero_flux_abs_kg": "",
            "boundary_reference_shift_abs_kg": "2.0e-5",
            "collar_flux_abs_kg": "3.0e-5",
            "M_H_ref_kg": "1.0",
            "bound_source": "FINITE_SOURCE_TESTBENCH_COMPONENTS_NOT_PHYSICAL",
            "source_path": str(BOUND_INPUT_CSV),
            "row_status": "finite_bound_testbench_nonclaim",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "private_zero_same_current_bound",
            "R_eq_integral_abs_kg": "0",
            "link_charge_mismatch_abs_kg": "0",
            "exterior_nonclosure_abs_kg": "0",
            "frame_mismatch_abs_kg": "0",
            "extra_exchange_abs_kg": "0",
            "projector_commutator_abs_kg": "0",
            "B_zero_flux_abs_kg": "0",
            "boundary_reference_shift_abs_kg": "0",
            "collar_flux_abs_kg": "0",
            "M_H_ref_kg": "1.0",
            "bound_source": "PRIVATE_ZERO_TESTBENCH_NOT_PHYSICAL",
            "source_path": str(BOUND_INPUT_CSV),
            "row_status": "private_zero_testbench_nonclaim",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "forbidden_orbital_backfill_bound",
            "R_eq_integral_abs_kg": "0",
            "link_charge_mismatch_abs_kg": "0",
            "exterior_nonclosure_abs_kg": "0",
            "frame_mismatch_abs_kg": "0",
            "extra_exchange_abs_kg": "0",
            "projector_commutator_abs_kg": "0",
            "B_zero_flux_abs_kg": "0",
            "boundary_reference_shift_abs_kg": "0",
            "collar_flux_abs_kg": "0",
            "M_H_ref_kg": "1.0",
            "bound_source": "ORBITAL_GM_DEFINITION_OBSERVED_RESIDUAL_CANCEL",
            "source_path": "FORBIDDEN_POSTFIT_REFERENCE",
            "row_status": "forbidden_control_nonclaim",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def closure_clause_map(value: bool) -> dict[str, bool]:
    return {clause: value for clause in CONTROLLED_CLOSURE_CLAUSES}


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


def physical_partial_clauses() -> dict[str, bool]:
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


def closure_input_rows(timestamp: str, bound_outputs: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    signed = closure_clause_map(True)
    partial = physical_partial_clauses()
    finite_bound = next(row for row in bound_outputs if row["bound_id"] == "finite_same_current_bound_testbench")
    finite_req = finite_bound["R_eq_abs_kg"]
    finite_bzero = finite_bound["B_zero_abs_kg"]

    for symbol in CLOSURE_COMPONENTS:
        rows.append(closure_row("physical_after_4789_same_current_attempt", symbol, "physical_same_current_attempt_nonclaim", "4789_PHYSICAL_THEOREM_GATE_UNSIGNED", timestamp, partial))

    finite_clauses = physical_partial_clauses()
    for symbol in CLOSURE_COMPONENTS:
        if symbol == "R_eq":
            rows.append(closure_row("finite_Req_Bzero_bound_reduces_two_components", symbol, "finite_same_current_bound_testbench_nonclaim", "4789_FINITE_REQ_BOUND_TESTBENCH", timestamp, finite_clauses, bound=finite_req))
        elif symbol == "B_zero":
            rows.append(closure_row("finite_Req_Bzero_bound_reduces_two_components", symbol, "finite_same_current_bound_testbench_nonclaim", "4789_FINITE_BZERO_BOUND_TESTBENCH", timestamp, finite_clauses, bound=finite_bzero))
        else:
            rows.append(closure_row("finite_Req_Bzero_bound_reduces_two_components", symbol, "physical_other_components_still_gate_nonclaim", "4789_OTHER_RESIDUALS_STILL_USE_4788_PARTIAL_CLAUSES", timestamp, finite_clauses))

    for symbol in CLOSURE_COMPONENTS:
        rows.append(closure_row("conditional_same_object_derham_closure_smoke", symbol, "conditional_same_object_private_nonclaim", "4789_CONDITIONAL_ALL_CLAUSES_SIGNED_SMOKE", timestamp, signed))

    return rows


def theorem_gate_rows(timestamp: str, theorem_outputs: list[dict[str, str]]) -> list[dict[str, Any]]:
    physical = next(row for row in theorem_outputs if row["branch_id"] == "physical_same_current_attempt")
    conditional = next(row for row in theorem_outputs if row["branch_id"] == "conditional_same_object_derham_theorem")
    return [
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "SCG4789_0_exact_conditional_theorem",
            "claim": "Pi_M J_H = J_M_top + dB_zero follows by de Rham exactness when both currents are the same parent source object",
            "gate_pass": conditional["runner_status"].startswith("SAME_CURRENT_IDENTITY_ZERO"),
            "status": conditional["runner_status"],
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "SCG4789_1_current_physical_branch",
            "claim": "current physical MTS branch parent-signs the same-current identity",
            "gate_pass": False,
            "status": physical["runner_status"],
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "SCG4789_2_Bzero_only_not_enough",
            "claim": "boundary primitive alone closes R_eq",
            "gate_pass": False,
            "status": "REJECTED_BOUNDARY_ONLY_DOES_NOT_CLOSE_SAME_OBJECT_CURRENT",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def promotion_gate_rows(timestamp: str, theorem_outputs: list[dict[str, str]], closure_outputs: list[dict[str, str]]) -> list[dict[str, Any]]:
    physical = next(row for row in theorem_outputs if row["branch_id"] == "physical_same_current_attempt")
    finite = next(row for row in closure_outputs if row["closure_id"] == "finite_Req_Bzero_bound_reduces_two_components")
    return [
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "PG4789_0_local_GR",
            "claim": "same-current identity permits local GR/Newton promotion",
            "gate_pass": False,
            "reason": "R_eq/B_zero physical branch remains unsigned and other residual components remain live",
            "evidence": physical["identity_missing_clauses"],
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "PG4789_1_bound_interface",
            "claim": "R_eq/B_zero can now be turned into finite source-testbench rows",
            "gate_pass": finite["bound_component_count"] == "2",
            "reason": "finite testbench bounds reduce the two same-current components, but do not close boundary/projector/domain",
            "evidence": finite["runner_status"],
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "PG4789_2_no_claim",
            "claim": "no claim rows are marked valid",
            "gate_pass": True,
            "reason": "all generated rows keep valid_for_claim=false",
            "evidence": "nonclaim firewall active",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def firewall_rows(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("FW4789_0_no_tautological_JMtop", "do not define J_M_top from Pi_M J_H and call the identity derived"),
        ("FW4789_1_no_boundary_calibration", "do not tune B_zero/reference terms per system to absorb measured GM"),
        ("FW4789_2_no_orbital_GM_source", "do not use orbital GM, PPN, clock, R10, or observed residuals as source inputs"),
        ("FW4789_3_no_Bzero_only_promotion", "B_zero exactness alone does not prove same-current equality"),
        ("FW4789_4_no_local_GR_promotion", "same-current theorem remains one source-side gate, not a full local-GR proof"),
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


def route_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("RT4789_0_parent_same_object", "parent-own W_source, J_H, M_H_ref and omega_M_top in one observed frame", "SELECTED_NEXT"),
        ("RT4789_1_finite_shell_profile", "if ownership fails, fill finite-shell R_eq and B_zero profile rows with real source paths", "SELECTED_NEXT_FALLBACK"),
        ("RT4789_2_other_residuals", "after R_eq/B_zero are zero or bounded, return to boundary/nonHilbert/projector/domain closure", "QUEUED"),
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
        for route_id, route, status in specs
    ]


def status_rows(timestamp: str, theorem_outputs: list[dict[str, str]], bound_outputs: list[dict[str, str]], closure_outputs: list[dict[str, str]]) -> list[dict[str, Any]]:
    physical_theorem = next(row for row in theorem_outputs if row["branch_id"] == "physical_same_current_attempt")
    finite_bound = next(row for row in bound_outputs if row["bound_id"] == "finite_same_current_bound_testbench")
    physical_closure = next(row for row in closure_outputs if row["closure_id"] == "physical_after_4789_same_current_attempt")
    finite_closure = next(row for row in closure_outputs if row["closure_id"] == "finite_Req_Bzero_bound_reduces_two_components")
    return [
        {
            "checkpoint": CHECKPOINT,
            "status_id": "STATUS4789_0_physical_theorem",
            "status": physical_theorem["runner_status"],
            "detail": physical_theorem["identity_missing_clauses"],
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "status_id": "STATUS4789_1_finite_bound",
            "status": finite_bound["runner_status"],
            "detail": f"epsilon={finite_bound['epsilon_same_current_abs']}",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "status_id": "STATUS4789_2_physical_closure",
            "status": physical_closure["runner_status"],
            "detail": f"missing={physical_closure['missing_component_count']}",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "status_id": "STATUS4789_3_bound_closure",
            "status": finite_closure["runner_status"],
            "detail": f"bound={finite_closure['bound_component_count']};missing={finite_closure['missing_component_count']}",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "decision_id": "DEC4789_0_theorem",
            "decision": "same_current_identity_is_derived_as_exact_conditional_same_object_theorem",
            "reason": "if Pi_M J_H and J_M_top are parent-selected representatives of the same compact source cohomology class, de Rham exactness gives their difference as dB_zero",
            "next_action": "parent-sign the same source object packet instead of relabelling currents",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "decision_id": "DEC4789_1_current_branch",
            "decision": "physical_current_branch_not_signed",
            "reason": "same observed frame, source worldtube, Hilbert current variation, Hamiltonian normalization, topological PD representative, no-exchange and projector clauses are not all owned",
            "next_action": "try parent ownership first, then fill finite-shell R_eq/B_zero rows",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "decision_id": "DEC4789_2_bound_route",
            "decision": "finite_bound_interface_reduces_same_current_pair_when_sourced",
            "reason": "R_eq and B_zero now have a component envelope feeding the 4788 closure runner",
            "next_action": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def next_target_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "next_id": "NEXT4789_0_4790",
            "next_target": NEXT_TARGET,
            "objective": "parent-own the same source object W_source, J_H, M_H_ref and omega_M_top in one observed frame, or fill finite-shell R_eq/B_zero profile rows",
            "include": "observed frame; Hilbert matter variation; worldtube support; topological PD representative; exact boundary primitive; no-exchange vector",
            "exclude": "tautological current definitions; orbital GM backfill; boundary calibration; local-GR/Newton claim",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
    ]


def validation_rows(timestamp: str) -> list[dict[str, Any]]:
    sources = parse_csv(SOURCE_REGISTER_CSV)
    theorem = parse_csv(THEOREM_OUTPUT_CSV)
    bounds = parse_csv(BOUND_OUTPUT_CSV)
    closure = parse_csv(CLOSURE_AGGREGATE_OUTPUT_CSV)
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

    physical = next(row for row in theorem if row["branch_id"] == "physical_same_current_attempt")
    conditional = next(row for row in theorem if row["branch_id"] == "conditional_same_object_derham_theorem")
    bzero_only = next(row for row in theorem if row["branch_id"] == "bzero_only_boundary_smoke")
    forbidden_theorem = next(row for row in theorem if row["branch_id"] == "forbidden_tautological_JMtop_control")
    physical_bound = next(row for row in bounds if row["bound_id"] == "physical_same_current_bound_attempt")
    finite_bound = next(row for row in bounds if row["bound_id"] == "finite_same_current_bound_testbench")
    forbidden_bound = next(row for row in bounds if row["bound_id"] == "forbidden_orbital_backfill_bound")
    finite_closure = next(row for row in closure if row["closure_id"] == "finite_Req_Bzero_bound_reduces_two_components")
    physical_closure = next(row for row in closure if row["closure_id"] == "physical_after_4789_same_current_attempt")
    conditional_closure = next(row for row in closure if row["closure_id"] == "conditional_same_object_derham_closure_smoke")

    add("VAL4789_0_sources", "all cited sources exist and needles are found", all(bool_text(row["exists"]) and bool_text(row["needle_found"]) for row in sources), str(SOURCE_REGISTER_CSV))
    add("VAL4789_1_conditional_theorem_zero", "conditional same-object theorem zeros R_eq/B_zero", conditional["runner_status"].startswith("SAME_CURRENT_IDENTITY_ZERO"), str(THEOREM_OUTPUT_CSV))
    add("VAL4789_2_physical_blocks", "physical same-current branch remains blocked", physical["runner_status"] == "SAME_CURRENT_IDENTITY_PARTIAL_BLOCKED_NONCLAIM" and "same_observed_frame_signed" in physical["identity_missing_clauses"], str(THEOREM_OUTPUT_CSV))
    add("VAL4789_3_Bzero_only_not_enough", "B_zero-only row does not close full identity", bzero_only["runner_status"] == "SAME_CURRENT_IDENTITY_PARTIAL_BLOCKED_NONCLAIM" and bzero_only["B_zero_abs_kg"].startswith("0."), str(THEOREM_OUTPUT_CSV))
    add("VAL4789_4_forbidden_theorem_fails", "tautological current definition fails", forbidden_theorem["runner_status"] == "FAILED_SAME_CURRENT_IDENTITY_GATE", str(THEOREM_OUTPUT_CSV))
    add("VAL4789_5_physical_bound_blocks", "physical bound rows remain missing", physical_bound["runner_status"] == "BLOCKED_MISSING_SAME_CURRENT_BOUND_INPUTS", str(BOUND_OUTPUT_CSV))
    add("VAL4789_6_finite_bound_computes", "finite source-testbench bound computes", finite_bound["runner_status"] == "SAME_CURRENT_BOUND_COMPUTED_NONCLAIM" and finite_bound["epsilon_same_current_abs"] != "MISSING_NUMERIC_VALUE", str(BOUND_OUTPUT_CSV))
    add("VAL4789_7_forbidden_bound_fails", "orbital/postfit backfill fails", forbidden_bound["runner_status"] == "FAILED_CIRCULAR_SAME_CURRENT_BOUND", str(BOUND_OUTPUT_CSV))
    add("VAL4789_8_closure_reduces_pair", "finite bound feeds closure runner as two bounded components", finite_closure["bound_component_count"] == "2" and finite_closure["missing_component_count"] == "4", str(CLOSURE_AGGREGATE_OUTPUT_CSV))
    add("VAL4789_9_physical_closure_still_blocked", "physical closure still blocked without source object", physical_closure["runner_status"] == "CONTROLLED_RESIDUAL_CLOSURE_PARTIAL_BLOCKED", str(CLOSURE_AGGREGATE_OUTPUT_CSV))
    add("VAL4789_10_conditional_closure_zero", "conditional closure smoke zeros all components", conditional_closure["runner_status"].startswith("CONTROLLED_SOURCE_TESTBENCH_ZERO") or conditional_closure["runner_status"].startswith("CONTROLLED_RESIDUAL_CLOSURE_ZERO"), str(CLOSURE_AGGREGATE_OUTPUT_CSV))
    add("VAL4789_11_claim", "claim register includes L-631 as nonclaim", CLAIM_ID in read_text(CLAIMS_PATH), str(CLAIMS_PATH))
    add("VAL4789_12_resume", "resume points at 4790", NEXT_TARGET in read_text(RESUME_PATH), str(RESUME_PATH))
    add("VAL4789_OVERALL", "all 4789 same-current checks pass", all(row["result"] == "PASS" for row in validation), DECISION)
    return validation


def write_claim(timestamp: str) -> None:
    if CLAIMS_PATH.exists() and any(row.get("claim_id") == CLAIM_ID for row in parse_csv(CLAIMS_PATH)):
        return
    with CLAIMS_PATH.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = reader.fieldnames or []
    row = {
        "claim_id": CLAIM_ID,
        "domain": "same_current_identity_gate_runner",
        "claim": "4789 derives the exact conditional same-current theorem Pi_M J_H = J_M_top+dB_zero under a same parent source-object packet, rejects current physical promotion, and installs finite R_eq/B_zero bound plumbing.",
        "current_evidence": "Generated source register, theorem input/output, finite bound input/output, closure-runner handoff, gates, firewalls, route, decision, status, next target and validation.",
        "status": "conditional_theorem_private_nonclaim_physical_branch_unsigned",
        "next_test": NEXT_TARGET,
        "key_risk": "Do not treat de Rham exactness or B_zero primitive as physical source equality until W_source, J_H, M_H_ref and omega_M_top are parent-owned in one observed frame.",
        "sector": "local_gr",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "tautological JM_top definition; boundary calibration; orbital GM backfill",
        "title": "same-current identity theorem gate",
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

The exact same-current identity is now separated from the cheat. If one parent source object owns `W_source`, `J_H`, `M_H_ref`, `Pi_M`, `omega_M_top`, the fixed exact primitive and the no-exchange/projector clauses, then `Pi_M J_H = J_M_top + dB_zero` and `R_eq=B_zero=0` follow as a conditional de Rham theorem. Current physical MTS has not parent-signed that packet, so the live job is to own that same source object or fill finite-shell `R_eq/B_zero` profile rows with real sources.

## Firewalls

- No tautological `J_M_top := Pi_M J_H-dB_zero`.
- No orbital-GM, PPN, clock, R10, or observed residual backfill.
- No boundary/reference tuning per system.
- No local-GR/Newton/PPN promotion from the conditional theorem alone.
"""
    write_text(RESUME_PATH, content)


def write_docs(timestamp: str) -> None:
    sources = parse_csv(SOURCE_REGISTER_CSV)
    theorem_outputs = parse_csv(THEOREM_OUTPUT_CSV)
    bound_outputs = parse_csv(BOUND_OUTPUT_CSV)
    closure_outputs = parse_csv(CLOSURE_AGGREGATE_OUTPUT_CSV)
    theorem_gates = parse_csv(THEOREM_GATE_CSV)
    promotions = parse_csv(PROMOTION_GATES_CSV)
    firewalls = parse_csv(FIREWALL_CSV)
    routes = parse_csv(ROUTE_MATRIX_CSV)
    decisions = parse_csv(DECISION_CSV)
    status = parse_csv(STATUS_CSV)
    validation = parse_csv(VALIDATION_CSV)

    content = f"""# 4789 - Derive R_eq/B_zero same-current identity or source-testbench bound

Marker: `{MARKER}`
Generated: `{timestamp}`
Decision: `{DECISION}`

## Result

4789 does the derivation-first move for the `R_eq/B_zero` wall. The identity is not asserted as a plateau axiom:

```text
If one parent source object fixes W_source, J_H, M_H_ref, Pi_M, omega_M_top,
the exact boundary primitive, no hidden exchange, and no projector mismatch,
then Pi_M J_H and J_M_top are representatives of the same compact source class.
By the same-object de Rham lemma:

    Pi_M J_H - J_M_top = dB_zero

and with fixed zero-flux primitive:

    R_eq = 0,  B_zero = 0.
```

The current physical branch does **not** yet satisfy that packet. That is useful: it tells us the next proof is not vague "coupling"; it is the same-source-object owner theorem. If that cannot be signed, the fallback is now executable finite-shell plumbing for `R_eq` and `B_zero`.

## Source Register

{markdown_table(sources, ["source_id", "source_path", "exists", "needle_found", "role"])}

## Same-Current Theorem Output

{markdown_table(theorem_outputs, ["branch_id", "R_eq_abs_kg", "B_zero_abs_kg", "R_eq_status", "B_zero_status", "runner_status"])}

## R_eq/B_zero Bound Output

{markdown_table(bound_outputs, ["bound_id", "R_eq_abs_kg", "B_zero_abs_kg", "same_current_bound_abs_kg", "M_H_ref_kg", "epsilon_same_current_abs", "runner_status"])}

## Controlled Closure Handoff

{markdown_table(closure_outputs, ["closure_id", "Delta_H_abs_kg", "zero_component_count", "bound_component_count", "missing_component_count", "failed_component_count", "runner_status"])}

## Theorem Gates

{markdown_table(theorem_gates, ["gate_id", "claim", "gate_pass", "status"])}

## Promotion Gates

{markdown_table(promotions, ["gate_id", "claim", "gate_pass", "reason", "evidence"])}

## Firewalls

{markdown_table(firewalls, ["firewall_id", "rule", "status"])}

## Route Selection

{markdown_table(routes, ["route_id", "route", "selection_status"])}

## Decision Ledger

{markdown_table(decisions, ["decision_id", "decision", "reason", "next_action"])}

## Status

{markdown_table(status, ["status_id", "status", "detail"])}

## Validation

{markdown_table(validation, ["check_id", "description", "result", "evidence"])}

## Next Target

`{NEXT_TARGET}`
"""
    write_text(DOC_PATH, content)
    write_text(FORMAL_PATH, content.replace("# 4789 -", "# 805 - PPC4161 "))

    append_once(
        SPINE_PATH,
        MARKER,
        f"""
## {MARKER}

- 4789 derives the exact conditional same-current theorem for `Pi_M J_H = J_M_top+dB_zero` without promoting it to a physical claim.
- Current physical MTS remains blocked by the same-source-object packet: observed frame, worldtube support, Hilbert current variation, Hamiltonian normalization, topological PD representative, no-exchange and projector clauses.
- Finite-shell `R_eq/B_zero` bound plumbing now feeds the controlled residual closure runner, reducing the pair to sourceable rows when real inputs exist.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## {PACKET_MARKER}

4789 adds the same-current identity gate to the private local packet. The conditional theorem is exact, but physical promotion is blocked until the same parent source object owns `W_source`, `J_H`, `M_H_ref`, `Pi_M`, `omega_M_top`, `B_zero`, no-exchange and projector silence in one observed frame. Next target: `{NEXT_TARGET}`.
""",
    )


def main() -> int:
    timestamp = now()
    write_csv(SOURCE_REGISTER_CSV, source_register(timestamp))
    write_csv(THEOREM_INPUT_CSV, theorem_input_rows(timestamp))
    write_csv(BOUND_INPUT_CSV, bound_input_rows(timestamp))

    run_command([sys.executable, str(SAME_CURRENT_RUNNER), str(THEOREM_INPUT_CSV), str(THEOREM_OUTPUT_CSV), str(BOUND_INPUT_CSV), str(BOUND_OUTPUT_CSV)])
    bound_outputs = parse_csv(BOUND_OUTPUT_CSV)
    write_csv(CLOSURE_INPUT_CSV, closure_input_rows(timestamp, bound_outputs))
    run_command([sys.executable, str(CLOSURE_RUNNER), str(CLOSURE_INPUT_CSV), str(CLOSURE_COMPONENT_OUTPUT_CSV), str(CLOSURE_AGGREGATE_OUTPUT_CSV)])

    theorem_outputs = parse_csv(THEOREM_OUTPUT_CSV)
    closure_outputs = parse_csv(CLOSURE_AGGREGATE_OUTPUT_CSV)
    write_csv(THEOREM_GATE_CSV, theorem_gate_rows(timestamp, theorem_outputs))
    write_csv(PROMOTION_GATES_CSV, promotion_gate_rows(timestamp, theorem_outputs, closure_outputs))
    write_csv(FIREWALL_CSV, firewall_rows(timestamp))
    write_csv(ROUTE_MATRIX_CSV, route_rows(timestamp))
    write_csv(DECISION_CSV, decision_rows(timestamp))
    write_csv(STATUS_CSV, status_rows(timestamp, theorem_outputs, bound_outputs, closure_outputs))
    write_csv(NEXT_TARGET_CSV, next_target_rows(timestamp))
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
