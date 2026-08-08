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

CHECKPOINT = "4792"
CLAIM_ID = "L-634"
MARKER = "PPC4161_CPERP_EXACTNESS_BOUNDARY_SILENCE_OR_REAL_CG_SOURCE_PACK_4792"
PACKET_MARKER = "PPC4161_PACKET_CPERP_EXACTNESS_BOUNDARY_SILENCE_OR_REAL_CG_SOURCE_PACK_4792"
DECISION = "CPERP_EXACTNESS_GATE_INSTALLED_PHYSICAL_BRANCH_BLOCKED_REAL_CG_SOURCE_PACK_COMPUTABLE_NONCLAIM"
NEXT_TARGET = "4793-Y5-R2FR-source-parent-C-PD-drel-trio-or-edge-bound-first-fill.md"

DOC_PATH = POST / "4792-Y5-R2FR-Cperp-exactness-boundary-silence-or-real-cg-source-pack.md"
FORMAL_PATH = FORMAL / "808-PPC4161-Cperp-exactness-boundary-silence-or-real-cg-source-pack.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"

RUNNER = SCRIPT_DIR / "cperp_exactness_cg_source_pack_runner.py"

SOURCE_REGISTER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4792_SOURCE_REGISTER.csv"
CPERP_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4792_CPERP_EXACTNESS_INPUT.csv"
CPERP_OUTPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4792_CPERP_EXACTNESS_OUTPUT.csv"
CG_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4792_CG_SOURCE_PACK_INPUT.csv"
CG_OUTPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4792_CG_SOURCE_PACK_OUTPUT.csv"
GATE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4792_PROMOTION_GATES.csv"
FIREWALL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4792_FIREWALL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4792_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4792_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4792_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4792_VALIDATION.csv"

EXACTNESS_CLAUSES = (
    "parent_C_object_signed",
    "parent_PD_projector_signed",
    "Cperp_definition_signed",
    "form_degree_units_signed",
    "drel_complex_signed",
    "drel_closedness_signed",
    "Hrel_trivial_or_bounded_signed",
    "primitive_BC_constructed_signed",
    "boundary_pullback_decomposition_signed",
    "boundary_primitive_zero_signed",
    "edge_charge_silent_signed",
    "presymplectic_kernel_signed",
    "vX_null_generator_signed",
    "matter_descent_same_domain_signed",
    "kinetic_rank_guard_signed",
    "local_FLRW_branch_selector_signed",
    "no_Cperp_by_declaration_signed",
    "no_boundary_zero_by_assertion_signed",
)

SOURCE_SPECS = [
    ("SRC4792_00_4791_doc", POST / "4791-Y5-R2FR-parent-qmap-matter-functor-to-source-object-or-first-frame-leak-row.md", "RT4791_0_Cperp_exactness", "4791 handoff selecting Cperp/c_g route"),
    ("SRC4792_01_1158_doc", POST / "1158-Y5-R10-cg-units-arena-projection-source-pack-or-Cperp-exactness-repair.md", "Cperp Exactness Repair Audit", "older c_g/Cperp exactness burden"),
    ("SRC4792_02_1160_chain", SOURCE_DIR / "P8_Y5_R10_1160_CPERP_RELATIVE_EXACTNESS_CHAIN.csv", "CRE1160_0_Cperp_object", "relative exactness chain"),
    ("SRC4792_03_1161_audit", SOURCE_DIR / "P8_Y5_R10_1161_CPERP_DREL_SOURCE_AUDIT.csv", "CDR1161_6_verdict", "Cperp/d_rel source audit"),
    ("SRC4792_04_1162_choice", SOURCE_DIR / "P8_Y5_R10_1162_STRICT_CPERP_CANDIDATE_CHOICE.csv", "CAND1162_0_topological_projector_residual", "strict Cperp candidate choice"),
    ("SRC4792_05_1163_contract", SOURCE_DIR / "P8_Y5_R10_1163_TOPOLOGICAL_CPERP_SOURCE_CONTRACT.csv", "CTC1163_0_candidate_lock", "topological Cperp source contract"),
    ("SRC4792_06_1158_cg_pack", SOURCE_DIR / "P8_Y5_R10_1158_CG_SOURCE_PACK_ROWS.csv", "CGSRC1158_2_cg_value", "c_g source pack rows"),
    ("SRC4792_07_runner", RUNNER, "def cperp_row", "4792 executable Cperp/c_g runner"),
]


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


def clause_map(value: bool) -> dict[str, bool]:
    return {clause: value for clause in EXACTNESS_CLAUSES}


def cperp_input_rows(timestamp: str) -> list[dict[str, Any]]:
    physical = clause_map(False)
    physical["no_Cperp_by_declaration_signed"] = True
    physical["no_boundary_zero_by_assertion_signed"] = True

    candidate_lock = clause_map(False)
    for clause in ("Cperp_definition_signed", "no_Cperp_by_declaration_signed", "no_boundary_zero_by_assertion_signed"):
        candidate_lock[clause] = True

    boundary_only = clause_map(False)
    for clause in ("boundary_primitive_zero_signed", "edge_charge_silent_signed", "no_Cperp_by_declaration_signed", "no_boundary_zero_by_assertion_signed"):
        boundary_only[clause] = True

    signed = clause_map(True)

    def row(row_id: str, status: str, source: str, clauses: dict[str, bool]) -> dict[str, Any]:
        return {
            "cperp_id": row_id,
            "candidate": "C_perp=(I-P_D)C topological/projector residual",
            "source_path": source,
            "Cperp_source": source,
            "drel_source": source,
            "boundary_source": source,
            "theorem_source": source,
            "provenance": source,
            "notes": "",
            "row_status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
            **clauses,
        }

    return [
        row("physical_Cperp_exactness_attempt", "physical_branch_nonclaim", str(SOURCE_DIR / "P8_Y5_R10_1163_TOPOLOGICAL_CPERP_SOURCE_CONTRACT.csv"), physical),
        row("candidate_lock_not_enough", "candidate_selected_but_parent_objects_missing_nonclaim", str(SOURCE_DIR / "P8_Y5_R10_1162_STRICT_CPERP_CANDIDATE_CHOICE.csv"), candidate_lock),
        row("boundary_zero_only_not_enough", "boundary_zero_control_without_exactness_nonclaim", str(SOURCE_DIR / "P8_Y5_R10_1159_BOUNDARY_PRIMITIVE_ZERO_AUDIT.csv"), boundary_only),
        row("conditional_full_Cperp_zero_packet", "conditional_reference_theorem_nonclaim", "CONDITIONAL_CPERP_DREL_BOUNDARY_MATTER_ALL_CLAUSES_SIGNED", signed),
        row("forbidden_boundary_assertion_control", "forbidden_control_nonclaim", "BOUNDARY_ZERO_BY_ASSERTION_CPERP_BY_DECLARATION", signed),
    ]


def cg_input_rows(timestamp: str) -> list[dict[str, Any]]:
    finite_source = str(CG_INPUT_CSV)
    return [
        {
            "cg_id": "physical_cg_source_pack_missing",
            "c_g": "MISSING_PARENT_INPUT",
            "Xhat_units": "MISSING_XHAT_NORMALIZATION",
            "c_g_units": "MISSING_CG_UNITS",
            "tau_R10": "MISSING_ARENA_PROJECTION",
            "tau_PPN_gamma": "MISSING_ARENA_PROJECTION",
            "tau_PPN_beta": "MISSING_ARENA_PROJECTION",
            "tau_clock": "MISSING_ARENA_PROJECTION",
            "tau_WEP": "MISSING_ARENA_PROJECTION",
            "tau_orbital": "MISSING_ARENA_PROJECTION",
            "K_X_R10": "MISSING_R10_KERNEL",
            "Qbar_XH": "MISSING_SOURCE_CHARGE",
            "lambda_X_m": "MISSING_RANGE",
            "alpha_bound_R10": "MISSING_BOUND",
            "ppn_gamma_bound": "MISSING_BOUND",
            "ppn_beta_bound": "MISSING_BOUND",
            "clock_bound": "MISSING_BOUND",
            "wep_bound": "MISSING_BOUND",
            "orbital_bound": "MISSING_BOUND",
            "Z_cg_zero_theorem_signed": False,
            "Ag_source": "MISSING_PARENT_SOURCE",
            "Xhat_source": "MISSING_PARENT_SOURCE",
            "cg_source": "MISSING_PARENT_SOURCE",
            "projection_source": "MISSING_ARENA_SOURCE",
            "bound_source": "MISSING_BOUND_SOURCE",
            "zero_theorem_path": "MISSING_ZERO_THEOREM",
            "row_status": "physical_cg_source_missing_nonclaim",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "cg_id": "finite_cg_real_source_pack_smoke",
            "c_g": "1.0e-6",
            "Xhat_units": "dimensionless",
            "c_g_units": "dimensionless",
            "tau_R10": "1.0e-1",
            "tau_PPN_gamma": "2.0e-1",
            "tau_PPN_beta": "1.0e-1",
            "tau_clock": "5.0e-2",
            "tau_WEP": "2.0e-2",
            "tau_orbital": "3.0e-1",
            "K_X_R10": "1.0",
            "Qbar_XH": "5.0e-1",
            "lambda_X_m": "1.0e-4",
            "alpha_bound_R10": "1.0e-5",
            "ppn_gamma_bound": "1.0e-4",
            "ppn_beta_bound": "1.0e-4",
            "clock_bound": "1.0e-4",
            "wep_bound": "1.0e-4",
            "orbital_bound": "1.0e-4",
            "Z_cg_zero_theorem_signed": False,
            "Ag_source": finite_source,
            "Xhat_source": finite_source,
            "cg_source": finite_source,
            "projection_source": finite_source,
            "bound_source": finite_source,
            "zero_theorem_path": str(CPERP_OUTPUT_CSV),
            "row_status": "finite_source_pack_smoke_nonclaim",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "cg_id": "conditional_Cperp_cg_zero",
            "c_g": "",
            "Xhat_units": "",
            "c_g_units": "",
            "tau_R10": "",
            "tau_PPN_gamma": "",
            "tau_PPN_beta": "",
            "tau_clock": "",
            "tau_WEP": "",
            "tau_orbital": "",
            "K_X_R10": "",
            "Qbar_XH": "",
            "lambda_X_m": "",
            "alpha_bound_R10": "",
            "ppn_gamma_bound": "",
            "ppn_beta_bound": "",
            "clock_bound": "",
            "wep_bound": "",
            "orbital_bound": "",
            "Z_cg_zero_theorem_signed": True,
            "Ag_source": "",
            "Xhat_source": "",
            "cg_source": "",
            "projection_source": "",
            "bound_source": "",
            "zero_theorem_path": str(CPERP_OUTPUT_CSV),
            "row_status": "conditional_cperp_zero_nonclaim",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "cg_id": "forbidden_orbital_GM_cg_control",
            "c_g": "1.0e-6",
            "Xhat_units": "dimensionless",
            "c_g_units": "dimensionless",
            "tau_R10": "1.0e-1",
            "tau_PPN_gamma": "1.0e-1",
            "tau_PPN_beta": "1.0e-1",
            "tau_clock": "1.0e-1",
            "tau_WEP": "1.0e-1",
            "tau_orbital": "1.0e-1",
            "K_X_R10": "1.0",
            "Qbar_XH": "1.0",
            "lambda_X_m": "1.0e-4",
            "alpha_bound_R10": "1.0",
            "ppn_gamma_bound": "1.0",
            "ppn_beta_bound": "1.0",
            "clock_bound": "1.0",
            "wep_bound": "1.0",
            "orbital_bound": "1.0",
            "Z_cg_zero_theorem_signed": False,
            "Ag_source": finite_source,
            "Xhat_source": finite_source,
            "cg_source": "ORBITAL_GM_DEFINITION",
            "projection_source": "ORBITAL_GM_DEFINITION",
            "bound_source": finite_source,
            "zero_theorem_path": str(CPERP_OUTPUT_CSV),
            "row_status": "forbidden_orbital_backfill_control",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def gate_rows(timestamp: str, cperp_rows: list[dict[str, str]], cg_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    physical_cperp = next(row for row in cperp_rows if row["cperp_id"] == "physical_Cperp_exactness_attempt")
    finite_cg = next(row for row in cg_rows if row["cg_id"] == "finite_cg_real_source_pack_smoke")
    return [
        {
            "gate_id": "PG4792_0_Cperp_zero_theorem",
            "claim": "Cperp exactness and boundary silence are physical evidence",
            "gate_pass": False,
            "reason": "physical branch remains blocked by parent C/P_D/d_rel/closedness/primitive/boundary/matter clauses",
            "evidence": physical_cperp["missing_exactness_clauses"],
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "PG4792_1_cg_finite_score",
            "claim": "finite c_g source pack can score only when sources and projections exist",
            "gate_pass": finite_cg["runner_status"] == "CG_SOURCE_PACK_COMPUTED_NONCLAIM" and bool_text(finite_cg["all_bounds_pass"]),
            "reason": "runner computes a smoke row but physical source pack remains missing",
            "evidence": str(CG_OUTPUT_CSV),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "PG4792_2_local_GR_Newton",
            "claim": "local GR/Newton/PPN promotion allowed",
            "gate_pass": False,
            "reason": "no physical Cperp zero theorem and no real c_g source pack are available",
            "evidence": "nonclaim firewall active",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def firewalls(timestamp: str) -> list[dict[str, Any]]:
    rules = [
        ("FW4792_0_no_Cperp_declaration", "Cperp cannot be exact/trivial by declaration; source parent C, P_D, d_rel and closedness."),
        ("FW4792_1_no_boundary_assertion", "Boundary primitive silence must come from a primitive/decomposition/no-edge theorem, not assertion."),
        ("FW4792_2_no_cg_without_sources", "Finite c_g requires A_g, Xhat, value/units, arena projections and bound sources."),
        ("FW4792_3_no_orbital_GM_backfill", "Orbital GM, PPN fit, R10 bound or clock calibration cannot be used as a parent coupling source."),
        ("FW4792_4_no_public_claim", "No R10, PPN, WEP, clock, orbital, local-GR or Newton claim follows from 4792."),
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
            "decision_id": "DEC4792_0_Cperp_route",
            "decision": "Cperp_zero_route_not_physical_yet",
            "reason": "candidate C_perp=(I-P_D)C exists, but parent C object, P_D owner, d_rel complex, closedness, primitive, boundary and branch selector remain unsigned",
            "next_action": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC4792_1_cg_route",
            "decision": "finite_cg_source_pack_runner_ready_nonclaim",
            "reason": "smoke row computes with real numeric fields, but physical row still lacks parent A_g/Xhat/c_g/tau sources",
            "next_action": "source finite c_g prior/projection pack only after C/P_D/d_rel route stalls",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def status_rows(timestamp: str, cperp_rows: list[dict[str, str]], cg_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    physical_cperp = next(row for row in cperp_rows if row["cperp_id"] == "physical_Cperp_exactness_attempt")
    physical_cg = next(row for row in cg_rows if row["cg_id"] == "physical_cg_source_pack_missing")
    return [
        {
            "status_id": "STATUS4792_0_physical_Cperp",
            "status": physical_cperp["runner_status"],
            "detail": physical_cperp["missing_exactness_clauses"],
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "status_id": "STATUS4792_1_physical_cg",
            "status": physical_cg["runner_status"],
            "detail": physical_cg["missing_inputs"],
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "status_id": "STATUS4792_2_selected_next",
            "status": "SOURCE_PARENT_C_PD_DREL_TRIO_FIRST",
            "detail": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "next_id": "NEXT4792_0_4793",
            "next_target": NEXT_TARGET,
            "objective": "source or derive the parent C object, P_D projector and d_rel relative complex before attempting Cperp exactness again",
            "include": "C object; P_D ownership/idempotence/variation; d_rel complex; form degree/units; closedness identity; local branch selector",
            "exclude": "Cperp by declaration; boundary zero by assertion; c_g from orbital GM/post-fit residuals; local-GR claim",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
    ]


def validation_rows(timestamp: str) -> list[dict[str, Any]]:
    sources = parse_csv(SOURCE_REGISTER_CSV)
    cperp_rows = parse_csv(CPERP_OUTPUT_CSV)
    cg_rows = parse_csv(CG_OUTPUT_CSV)
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

    physical_cperp = next(row for row in cperp_rows if row["cperp_id"] == "physical_Cperp_exactness_attempt")
    candidate_lock = next(row for row in cperp_rows if row["cperp_id"] == "candidate_lock_not_enough")
    boundary_only = next(row for row in cperp_rows if row["cperp_id"] == "boundary_zero_only_not_enough")
    conditional_zero = next(row for row in cperp_rows if row["cperp_id"] == "conditional_full_Cperp_zero_packet")
    forbidden_cperp = next(row for row in cperp_rows if row["cperp_id"] == "forbidden_boundary_assertion_control")
    physical_cg = next(row for row in cg_rows if row["cg_id"] == "physical_cg_source_pack_missing")
    finite_cg = next(row for row in cg_rows if row["cg_id"] == "finite_cg_real_source_pack_smoke")
    zero_cg = next(row for row in cg_rows if row["cg_id"] == "conditional_Cperp_cg_zero")
    forbidden_cg = next(row for row in cg_rows if row["cg_id"] == "forbidden_orbital_GM_cg_control")

    add("VAL4792_0_sources", "all cited sources exist and needles are found", all(bool_text(row["exists"]) and bool_text(row["needle_found"]) for row in sources), str(SOURCE_REGISTER_CSV))
    add("VAL4792_1_physical_Cperp_blocks", "physical Cperp route remains blocked", physical_cperp["runner_status"] == "CPERP_EXACTNESS_PARTIAL_BLOCKED_NONCLAIM" and "parent_C_object_signed" in physical_cperp["missing_exactness_clauses"], str(CPERP_OUTPUT_CSV))
    add("VAL4792_2_candidate_not_enough", "candidate selection alone does not close exactness", candidate_lock["runner_status"] == "CPERP_EXACTNESS_PARTIAL_BLOCKED_NONCLAIM" and "parent_C_object_signed" in candidate_lock["missing_exactness_clauses"], str(CPERP_OUTPUT_CSV))
    add("VAL4792_3_boundary_not_enough", "boundary silence alone does not close Cperp exactness", boundary_only["runner_status"] == "CPERP_EXACTNESS_PARTIAL_BLOCKED_NONCLAIM" and "drel_complex_signed" in boundary_only["missing_exactness_clauses"], str(CPERP_OUTPUT_CSV))
    add("VAL4792_4_conditional_zero", "conditional all-clause Cperp theorem zeros c_g", conditional_zero["runner_status"] == "CPERP_EXACTNESS_BOUNDARY_SILENCE_ZERO_PRIVATE_OR_CONDITIONAL_NONCLAIM", str(CPERP_OUTPUT_CSV))
    add("VAL4792_5_forbidden_Cperp_fails", "Cperp/boundary by assertion fails", forbidden_cperp["runner_status"] == "FAILED_CPERP_EXACTNESS_GATE", str(CPERP_OUTPUT_CSV))
    add("VAL4792_6_physical_cg_blocks", "physical c_g source pack remains missing", physical_cg["runner_status"] == "BLOCKED_MISSING_CG_SOURCE_PACK_INPUTS", str(CG_OUTPUT_CSV))
    add("VAL4792_7_finite_cg_smoke_computes", "finite c_g source pack smoke computes and compares bounds", finite_cg["runner_status"] == "CG_SOURCE_PACK_COMPUTED_NONCLAIM" and bool_text(finite_cg["all_bounds_pass"]), str(CG_OUTPUT_CSV))
    add("VAL4792_8_zero_cg_branch", "conditional Cperp zero theorem zeros c_g", zero_cg["runner_status"] == "CG_ZERO_BY_CPERP_EXACTNESS_PRIVATE_OR_CONDITIONAL_NONCLAIM", str(CG_OUTPUT_CSV))
    add("VAL4792_9_forbidden_cg_fails", "orbital GM/postfit c_g source fails", forbidden_cg["runner_status"] == "FAILED_CIRCULAR_CG_SOURCE_PACK", str(CG_OUTPUT_CSV))
    add("VAL4792_10_claim", "claim register includes L-634 as nonclaim", CLAIM_ID in read_text(CLAIMS_PATH), str(CLAIMS_PATH))
    add("VAL4792_11_resume", "resume points at 4793", NEXT_TARGET in read_text(RESUME_PATH), str(RESUME_PATH))
    add("VAL4792_OVERALL", "all 4792 Cperp/c_g checks pass", all(row["result"] == "PASS" for row in validation), DECISION)
    return validation


def write_claim(timestamp: str) -> None:
    if CLAIMS_PATH.exists() and any(row.get("claim_id") == CLAIM_ID for row in parse_csv(CLAIMS_PATH)):
        return
    with CLAIMS_PATH.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = reader.fieldnames or []
    row = {
        "claim_id": CLAIM_ID,
        "domain": "Cperp_exactness_cg_source_pack_runner",
        "claim": "4792 installs a strict Cperp exactness/boundary-silence gate and a real finite c_g source-pack smoke runner; physical Cperp and c_g branches remain unsigned.",
        "current_evidence": "Generated source register, Cperp exactness input/output, c_g source-pack input/output, gates, firewalls, decision, status, next target and validation.",
        "status": "Cperp_gate_private_nonclaim_physical_branch_blocked_cg_source_pack_runner_ready",
        "next_test": NEXT_TARGET,
        "key_risk": "Do not promote Cperp candidate selection, boundary-zero assertion, or post-fit orbital/PPN/R10 rows into a parent coupling source.",
        "sector": "local_gr",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "Cperp by declaration; boundary zero by assertion; finite c_g without A_g/Xhat/tau sources; local-GR promotion",
        "title": "Cperp exactness and c_g source-pack gate",
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

4792 installed the strict `C_perp` exactness / boundary-silence / `c_g` source-pack gate. The clean zero route works only as a conditional/private theorem: if parent `C`, owned `P_D`, `C_perp=(I-P_D)C`, form degree/units, `d_rel`, closedness, relative cohomology, primitive, boundary silence, presymplectic nullness, matter descent, kinetic-rank guard and branch selector are all signed, then `C_perp` is silent and `c_g=0`. Current physical MTS does not yet source the parent `C/P_D/d_rel` trio, so local GR/Newton/PPN remains blocked.

## Firewalls

- No `C_perp` exactness by declaration.
- No boundary primitive zero by assertion.
- No finite `c_g` score without `A_g`, `Xhat`, value/units, source paths, projections and bound rows.
- No orbital-GM, PPN-fit, clock-calibration or R10-bound backfill as parent coupling source.
- No local-GR/Newton/PPN/R10 claim from this checkpoint.
"""
    write_text(RESUME_PATH, content)


def write_docs(timestamp: str) -> None:
    sources = parse_csv(SOURCE_REGISTER_CSV)
    cperp_rows = parse_csv(CPERP_OUTPUT_CSV)
    cg_rows = parse_csv(CG_OUTPUT_CSV)
    gates = parse_csv(GATE_CSV)
    firewall_rows = parse_csv(FIREWALL_CSV)
    decisions = parse_csv(DECISION_CSV)
    statuses = parse_csv(STATUS_CSV)
    validation = parse_csv(VALIDATION_CSV)

    content = f"""# 4792 - Cperp exactness, boundary silence, or real c_g source pack

Marker: `{MARKER}`
Generated: `{timestamp}`
Decision: `{DECISION}`

## Result

4792 turns the Cperp/coupling fork into an executable gate:

```text
C_perp=(I-P_D)C
  + sourced parent C/P_D/d_rel/closedness/relative class
  + constructed primitive B_C and silent boundary pullback
  + presymplectic-null v_X and same-domain matter descent
    => c_g = 0 only in the conditional/private zero theorem branch
```

The physical MTS branch does **not** yet pass this. Candidate selection and boundary silence alone are not enough. The finite `c_g` source-pack runner now computes when all numeric/source fields are present, but the physical row remains missing `A_g`, `Xhat`, `c_g`, `tau` projections, companion factors and bound sources.

## Source Register

{markdown_table(sources, ["source_id", "source_path", "exists", "needle_found", "role"])}

## Cperp Exactness Output

{markdown_table(cperp_rows, ["cperp_id", "Z_cperp_exact", "Z_boundary_silent", "Z_cg", "runner_status", "missing_exactness_clauses"])}

## c_g Source-Pack Output

{markdown_table(cg_rows, ["cg_id", "c_g", "lambda_X_m", "alpha_R10_abs", "ppn_gamma_abs", "ppn_beta_abs", "clock_abs", "wep_abs", "orbital_abs", "all_bounds_pass", "unit_status", "runner_status", "missing_inputs"])}

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
    write_text(FORMAL_PATH, content.replace("# 4792 -", "# 808 - PPC4161 "))

    append_once(
        SPINE_PATH,
        MARKER,
        f"""
## {MARKER}

- 4792 establishes the strict Cperp/coupling fork: either a parent-signed `C/P_D/d_rel` exactness stack plus boundary silence zeros `c_g`, or finite `c_g` needs a fully sourced `A_g/Xhat/value/units/projection/bound` pack.
- Current physical branch remains blocked at parent `C`, `P_D`, `d_rel`, closedness, primitive, boundary silence, matter descent, kinetic-rank and branch-selector clauses.
- The finite `c_g` runner computes on smoke data but cannot be promoted until physical source rows replace placeholders.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## {PACKET_MARKER}

4792 adds the Cperp exactness/boundary-silence gate and real finite `c_g` source-pack smoke runner to the private local packet. The zero theorem is clean but conditional; the physical branch now points to parent `C/P_D/d_rel` acquisition. Next target: `{NEXT_TARGET}`.
""",
    )


def main() -> int:
    timestamp = now()
    write_csv(SOURCE_REGISTER_CSV, source_register(timestamp))
    write_csv(CPERP_INPUT_CSV, cperp_input_rows(timestamp))
    write_csv(CG_INPUT_CSV, cg_input_rows(timestamp))
    run_command([sys.executable, str(RUNNER), str(CPERP_INPUT_CSV), str(CPERP_OUTPUT_CSV), str(CG_INPUT_CSV), str(CG_OUTPUT_CSV)])

    cperp_rows = parse_csv(CPERP_OUTPUT_CSV)
    cg_rows = parse_csv(CG_OUTPUT_CSV)
    write_csv(GATE_CSV, gate_rows(timestamp, cperp_rows, cg_rows))
    write_csv(FIREWALL_CSV, firewalls(timestamp))
    write_csv(DECISION_CSV, decision_rows(timestamp))
    write_csv(STATUS_CSV, status_rows(timestamp, cperp_rows, cg_rows))
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
