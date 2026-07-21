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

CHECKPOINT = "4793"
CLAIM_ID = "L-635"
MARKER = "PPC4161_SOURCE_PARENT_C_PD_DREL_TRIO_OR_EDGE_BOUND_FIRST_FILL_4793"
PACKET_MARKER = "PPC4161_PACKET_SOURCE_PARENT_C_PD_DREL_TRIO_OR_EDGE_BOUND_FIRST_FILL_4793"
DECISION = "SCALAR_CPERP_DEMOTED_LIFTED_C_PARENT_TRIO_SELECTED_CCORNER_ZERO_OR_BOUND_GATE_INSTALLED"
NEXT_TARGET = "4794-Y5-R2FR-lifted-C-action-PD-drel-contract-or-domain-corner-certificate.md"

DOC_PATH = POST / "4793-Y5-R2FR-source-parent-C-PD-drel-trio-or-edge-bound-first-fill.md"
FORMAL_PATH = FORMAL / "809-PPC4161-source-parent-C-PD-drel-trio-or-edge-bound-first-fill.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"

RUNNER = SCRIPT_DIR / "parent_trio_and_corner_edge_gate_runner.py"

SOURCE_REGISTER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4793_SOURCE_REGISTER.csv"
TRIO_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4793_PARENT_TRIO_INPUT.csv"
TRIO_OUTPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4793_PARENT_TRIO_OUTPUT.csv"
CORNER_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4793_CCORNER_INPUT.csv"
CORNER_OUTPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4793_CCORNER_OUTPUT.csv"
EDGE_UPDATE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4793_EDGE_UPDATE.csv"
GATE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4793_PROMOTION_GATES.csv"
FIREWALL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4793_FIREWALL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4793_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4793_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4793_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4793_VALIDATION.csv"

TRIO_CLAUSES = (
    "lifted_C_field_signed",
    "lifted_C_form_degree_units_signed",
    "parent_action_term_signed",
    "PD_projector_owner_signed",
    "PD_idempotence_signed",
    "PD_variation_rule_signed",
    "drel_complex_signed",
    "drel_nilpotent_signed",
    "boundary_pullback_signed",
    "closedness_identity_signed",
    "BC_primitive_or_harmonic_bound_signed",
    "local_FLRW_selector_signed",
    "matter_selector_same_domain_signed",
    "no_scalar_Cperp_promotion_signed",
    "no_projected_metric_theorem_by_closure_signed",
)

CORNER_ZERO_CLAUSES = (
    "domain_U_oriented_smooth_chain_signed",
    "boundary_S_closed_or_relative_boundary_signed",
    "partial_boundary_zero_signed",
    "no_regulator_joint_signed",
    "orientation_convention_signed",
    "corner_term_definition_signed",
    "stokes_boundary_of_boundary_signed",
    "no_corner_zero_by_assertion_signed",
)

SOURCE_SPECS = [
    ("SRC4793_00_4792_doc", DOC_PATH.parent / "4792-Y5-R2FR-Cperp-exactness-boundary-silence-or-real-cg-source-pack.md", "DEC4792_0_Cperp_route", "4792 handoff to parent C/P_D/d_rel"),
    ("SRC4793_01_1164_doc", POST / "1164-Y5-R10-parent-C-PD-drel-source-hunt-or-first-edge-zero-certificate.md", "PARENT_TRIO_NOT_CLOSED_LIFTED_ROUTE_SELECTED_FOR_NEXT_ACQUISITION", "older source hunt that demotes scalar Cperp"),
    ("SRC4793_02_274_lifted", POST / "274-lifted-C-sector-form-holonomy-route.md", "lifted_C_sector_3form_boundary_route_identified_not_parent_derived_projected_metric_remains_closure", "lifted C route shape"),
    ("SRC4793_03_275_JC", POST / "275-JC-three-form-memory-current-from-Q.md", "JC_three_form_has_conditional_kinematic_Q_origin_not_parent_action_projector_and_domain_still_closure", "three-form memory current shape"),
    ("SRC4793_04_1020_stokes", POST / "1020-Y5-R10-boundary-cohomology-domain-certificate-or-source-pack-first-row.md", "ETB1020_1_weighted_Stokes_identity", "weighted Stokes edge identity"),
    ("SRC4793_05_1020_zero", POST / "1020-Y5-R10-boundary-cohomology-domain-certificate-or-source-pack-first-row.md", "ETB1020_2_zero_conditions", "edge zero conditions"),
    ("SRC4793_06_1163_schema", SOURCE_DIR / "P8_Y5_R10_1163_EDGE_BOUND_INPUT_SCHEMA.csv", "EIS1163_0_C_corner", "strict edge-bound schema"),
    ("SRC4793_07_runner", RUNNER, "def corner_row", "4793 parent trio and corner runner"),
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


def trio_input_rows(timestamp: str) -> list[dict[str, Any]]:
    physical = clause_map(TRIO_CLAUSES, False)
    physical["no_scalar_Cperp_promotion_signed"] = True
    physical["no_projected_metric_theorem_by_closure_signed"] = True
    shape = physical.copy()
    for clause in ("lifted_C_field_signed", "lifted_C_form_degree_units_signed", "boundary_pullback_signed"):
        shape[clause] = True
    signed = clause_map(TRIO_CLAUSES, True)

    def row(row_id: str, route: str, status: str, source: str, clauses: dict[str, bool]) -> dict[str, Any]:
        return {
            "trio_id": row_id,
            "route": route,
            "source_path": source,
            "C_source": source,
            "PD_source": source,
            "drel_source": source,
            "action_source": source,
            "provenance": source,
            "notes": "",
            "row_status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
            **clauses,
        }

    return [
        row("physical_lifted_C_trio_attempt", "lifted_C_parent_trio", "physical_branch_nonclaim", str(POST / "1164-Y5-R10-parent-C-PD-drel-source-hunt-or-first-edge-zero-certificate.md"), physical),
        row("lifted_C_shape_not_enough", "lifted_C_shape_support", "shape_support_nonclaim", str(POST / "274-lifted-C-sector-form-holonomy-route.md"), shape),
        row("conditional_lifted_C_trio_packet", "conditional_lifted_C_parent_stack", "conditional_reference_theorem_nonclaim", "CONDITIONAL_LIFTED_C_ACTION_PD_DREL_ALL_CLAUSES_SIGNED", signed),
        row("forbidden_scalar_closure_control", "scalar_Cperp_closure_shortcut", "forbidden_control_nonclaim", "SCALAR_CPERP_PROMOTED_PROJECTED_METRIC_BY_CLOSURE", signed),
    ]


def corner_input_rows(timestamp: str) -> list[dict[str, Any]]:
    physical = clause_map(CORNER_ZERO_CLAUSES, False)
    physical["no_corner_zero_by_assertion_signed"] = True
    smooth = clause_map(CORNER_ZERO_CLAUSES, True)
    finite = physical.copy()
    finite["corner_term_definition_signed"] = True
    finite["orientation_convention_signed"] = True
    source = str(CORNER_INPUT_CSV)

    def row(row_id: str, status: str, source_text: str, clauses: dict[str, bool], measure: str = "", density: str = "") -> dict[str, Any]:
        return {
            "corner_id": row_id,
            "domain_source": source_text,
            "corner_source": source_text,
            "bound_source": source_text,
            "zero_theorem_path": source_text,
            "provenance": source_text,
            "notes": "",
            "corner_measure": measure,
            "corner_density_bound": density,
            "row_status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
            **clauses,
        }

    return [
        row("physical_Ccorner_missing", "physical_branch_missing_domain_certificate_nonclaim", "MISSING_DOMAIN_CORNER_SOURCE", physical),
        row("smooth_closed_domain_Ccorner_zero", "conditional_smooth_closed_domain_nonclaim", "BOUNDARY_OF_BOUNDARY_THEOREM_WITH_DOMAIN_CERTIFICATE", smooth),
        row("finite_corner_bound_smoke", "finite_corner_bound_smoke_nonclaim", source, finite, "2.0e-3", "4.0e-5"),
        row("forbidden_corner_assertion_control", "forbidden_control_nonclaim", "CORNER_ZERO_BY_ASSERTION_REGULATOR_IGNORED", smooth),
    ]


def edge_update_rows(timestamp: str, corner_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    physical = next(row for row in corner_rows if row["corner_id"] == "physical_Ccorner_missing")
    zero = next(row for row in corner_rows if row["corner_id"] == "smooth_closed_domain_Ccorner_zero")
    finite = next(row for row in corner_rows if row["corner_id"] == "finite_corner_bound_smoke")
    return [
        {
            "edge_id": "EDGE4793_0_Ccorner_physical",
            "quantity": "C_corner",
            "status": physical["runner_status"],
            "value_or_bound": physical["C_corner_abs"],
            "meaning": "physical domain/corner certificate is still missing",
            "feeds": "Cperp edge-bound sum",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "edge_id": "EDGE4793_1_Ccorner_zero_theorem",
            "quantity": "C_corner",
            "status": zero["runner_status"],
            "value_or_bound": zero["C_corner_abs"],
            "meaning": "if local domain is a smooth oriented chain with closed/relative boundary and no regulator joints, the corner term vanishes by boundary-of-boundary",
            "feeds": "conditional first edge zero certificate",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "edge_id": "EDGE4793_2_Ccorner_finite_bound",
            "quantity": "C_corner",
            "status": finite["runner_status"],
            "value_or_bound": finite["C_corner_abs"],
            "meaning": "if corners exist, the runner can score a finite bound from corner measure times density bound",
            "feeds": "finite edge-bound fallback",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def gate_rows(timestamp: str, trio_rows: list[dict[str, str]], corner_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    physical_trio = next(row for row in trio_rows if row["trio_id"] == "physical_lifted_C_trio_attempt")
    physical_corner = next(row for row in corner_rows if row["corner_id"] == "physical_Ccorner_missing")
    return [
        {
            "gate_id": "PG4793_0_parent_trio",
            "claim": "parent lifted C/P_D/d_rel stack is physically sourced",
            "gate_pass": False,
            "reason": "physical branch still lacks action term, P_D owner/idempotence/variation, d_rel, closedness, primitive, selector and matter coupling",
            "evidence": physical_trio["missing_trio_clauses"],
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "PG4793_1_Ccorner_physical",
            "claim": "physical C_corner term is zero or bounded",
            "gate_pass": False,
            "reason": "domain/corner certificate or finite corner measure/density source is missing in physical branch",
            "evidence": physical_corner["missing_corner_inputs"],
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "PG4793_2_local_GR_Newton",
            "claim": "local GR/Newton/PPN promotion allowed",
            "gate_pass": False,
            "reason": "parent trio and physical edge certificate remain nonclaim",
            "evidence": "nonclaim firewall active",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def firewalls(timestamp: str) -> list[dict[str, Any]]:
    rules = [
        ("FW4793_0_no_scalar_promotion", "Do not promote scalar Cperp or projected metric closure into a parent theorem."),
        ("FW4793_1_no_corner_assertion", "C_corner can vanish only from a domain certificate plus boundary-of-boundary theorem, not assertion."),
        ("FW4793_2_no_regulator_silence", "Regulator joints/collars must be certified absent or bounded."),
        ("FW4793_3_no_edge_numbers", "Finite corner bounds require sourced corner measure and density bound."),
        ("FW4793_4_no_local_claim", "No local-GR/Newton/R10/PPN/WEP/clock/orbital claim follows from 4793."),
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
            "decision_id": "DEC4793_0_scalar_route",
            "decision": "scalar_Cperp_remains_closure_only",
            "reason": "older source hunt rejects scalar exactness/projection as parent theorem; 4793 keeps that firewall active",
            "next_action": "do not spend more cycles trying to promote scalar Cperp without new parent source",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC4793_1_lifted_route",
            "decision": "lifted_C_parent_trio_is_best_theorem_route",
            "reason": "a lifted form/holonomy/three-form object can own degree, relative cohomology, boundary class and FLRW/local split in a less circular way",
            "next_action": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC4793_2_first_edge",
            "decision": "Ccorner_zero_or_bound_gate_installed",
            "reason": "corner term now has exact zero conditions and finite bound fallback instead of a vague boundary debt",
            "next_action": "source local domain/corner certificate or finite corner measure/density bound",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def status_rows(timestamp: str, trio_rows: list[dict[str, str]], corner_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    physical_trio = next(row for row in trio_rows if row["trio_id"] == "physical_lifted_C_trio_attempt")
    physical_corner = next(row for row in corner_rows if row["corner_id"] == "physical_Ccorner_missing")
    zero_corner = next(row for row in corner_rows if row["corner_id"] == "smooth_closed_domain_Ccorner_zero")
    return [
        {
            "status_id": "STATUS4793_0_parent_trio",
            "status": physical_trio["runner_status"],
            "detail": physical_trio["missing_trio_clauses"],
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "status_id": "STATUS4793_1_Ccorner_physical",
            "status": physical_corner["runner_status"],
            "detail": physical_corner["missing_corner_inputs"],
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "status_id": "STATUS4793_2_Ccorner_conditional_zero",
            "status": zero_corner["runner_status"],
            "detail": "conditional theorem now explicit: smooth closed relative boundary plus no regulator joints gives C_corner=0",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "status_id": "STATUS4793_3_selected_next",
            "status": "LIFTED_C_ACTION_PD_DREL_OR_DOMAIN_CORNER_CERTIFICATE",
            "detail": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "next_id": "NEXT4793_0_4794",
            "next_target": NEXT_TARGET,
            "objective": "write the lifted C parent-action/P_D/d_rel contract or source the local domain certificate that makes C_corner=0 by boundary-of-boundary",
            "include": "lifted C action term; P_D idempotence/variation; d_rel complex; closedness; B_C primitive; domain U/S certificate; no regulator joint; finite corner bound fallback",
            "exclude": "scalar Cperp promotion; projected metric by closure; corner zero by assertion; invented edge numbers; local-GR claim",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
    ]


def validation_rows(timestamp: str) -> list[dict[str, Any]]:
    sources = parse_csv(SOURCE_REGISTER_CSV)
    trio_rows = parse_csv(TRIO_OUTPUT_CSV)
    corner_rows = parse_csv(CORNER_OUTPUT_CSV)
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

    physical_trio = next(row for row in trio_rows if row["trio_id"] == "physical_lifted_C_trio_attempt")
    shape_trio = next(row for row in trio_rows if row["trio_id"] == "lifted_C_shape_not_enough")
    conditional_trio = next(row for row in trio_rows if row["trio_id"] == "conditional_lifted_C_trio_packet")
    forbidden_trio = next(row for row in trio_rows if row["trio_id"] == "forbidden_scalar_closure_control")
    physical_corner = next(row for row in corner_rows if row["corner_id"] == "physical_Ccorner_missing")
    zero_corner = next(row for row in corner_rows if row["corner_id"] == "smooth_closed_domain_Ccorner_zero")
    finite_corner = next(row for row in corner_rows if row["corner_id"] == "finite_corner_bound_smoke")
    forbidden_corner = next(row for row in corner_rows if row["corner_id"] == "forbidden_corner_assertion_control")

    add("VAL4793_0_sources", "all cited sources exist and needles are found", all(bool_text(row["exists"]) and bool_text(row["needle_found"]) for row in sources), str(SOURCE_REGISTER_CSV))
    add("VAL4793_1_physical_trio_blocks", "physical lifted C/P_D/d_rel route remains blocked", physical_trio["runner_status"] == "PARENT_C_PD_DREL_TRIO_PARTIAL_BLOCKED_NONCLAIM" and "parent_action_term_signed" in physical_trio["missing_trio_clauses"], str(TRIO_OUTPUT_CSV))
    add("VAL4793_2_shape_not_enough", "lifted C shape support is not enough", shape_trio["runner_status"] == "PARENT_C_PD_DREL_TRIO_PARTIAL_BLOCKED_NONCLAIM" and "PD_projector_owner_signed" in shape_trio["missing_trio_clauses"], str(TRIO_OUTPUT_CSV))
    add("VAL4793_3_conditional_trio_passes", "conditional full lifted trio stack passes as nonclaim theorem shape", conditional_trio["runner_status"] == "PARENT_C_PD_DREL_TRIO_CONDITIONAL_SOURCE_STACK_NONCLAIM", str(TRIO_OUTPUT_CSV))
    add("VAL4793_4_forbidden_scalar_fails", "scalar/projected-metric closure shortcut fails", forbidden_trio["runner_status"] == "FAILED_PARENT_TRIO_GATE", str(TRIO_OUTPUT_CSV))
    add("VAL4793_5_physical_corner_blocks", "physical C_corner row remains missing domain certificate or bound", physical_corner["runner_status"] == "BLOCKED_MISSING_CCORNER_ZERO_OR_BOUND_INPUTS", str(CORNER_OUTPUT_CSV))
    add("VAL4793_6_Ccorner_zero_theorem", "smooth closed relative domain zeroes C_corner conditionally", zero_corner["runner_status"] == "CCORNER_ZERO_BY_BOUNDARY_OF_BOUNDARY_THEOREM_CONDITIONAL_NONCLAIM", str(CORNER_OUTPUT_CSV))
    add("VAL4793_7_finite_corner_bound", "finite C_corner bound computes from measure times density", finite_corner["runner_status"] == "CCORNER_FINITE_BOUND_COMPUTED_NONCLAIM" and finite_corner["C_corner_abs"] != "MISSING_NUMERIC_VALUE", str(CORNER_OUTPUT_CSV))
    add("VAL4793_8_forbidden_corner_fails", "corner zero by assertion fails", forbidden_corner["runner_status"] == "FAILED_CIRCULAR_CORNER_EDGE_GATE", str(CORNER_OUTPUT_CSV))
    add("VAL4793_9_claim", "claim register includes L-635 as nonclaim", CLAIM_ID in read_text(CLAIMS_PATH), str(CLAIMS_PATH))
    add("VAL4793_10_resume", "resume points at 4794", NEXT_TARGET in read_text(RESUME_PATH), str(RESUME_PATH))
    add("VAL4793_OVERALL", "all 4793 parent trio and Ccorner checks pass", all(row["result"] == "PASS" for row in validation), DECISION)
    return validation


def write_claim(timestamp: str) -> None:
    if CLAIMS_PATH.exists() and any(row.get("claim_id") == CLAIM_ID for row in parse_csv(CLAIMS_PATH)):
        return
    with CLAIMS_PATH.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = reader.fieldnames or []
    row = {
        "claim_id": CLAIM_ID,
        "domain": "parent_trio_and_corner_edge_gate_runner",
        "claim": "4793 keeps scalar Cperp demoted, selects lifted C/P_D/d_rel as the least-circular theorem route, and installs a C_corner zero-or-bound gate.",
        "current_evidence": "Generated source register, parent trio input/output, Ccorner input/output, edge update, gates, firewalls, decision, status, next target and validation.",
        "status": "lifted_C_parent_trio_private_nonclaim_physical_branch_blocked_Ccorner_gate_ready",
        "next_test": NEXT_TARGET,
        "key_risk": "Do not promote scalar Cperp/projection closure or assert C_corner=0 without a domain certificate.",
        "sector": "local_gr",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "scalar Cperp promotion; projected metric by closure; Ccorner assertion; regulator joint silence; local-GR promotion",
        "title": "lifted C parent trio and Ccorner gate",
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

4793 confirms the scalar `C_perp`/projected-metric route remains closure-only and selects the lifted `C` sector as the least-circular theorem route. The physical lifted branch still lacks a parent action term, owned/idempotent/varied `P_D`, instantiated `d_rel`, closedness identity, `B_C` primitive or harmonic bound, branch selector and same-domain matter selector. The first edge term is now sharper: `C_corner=0` follows conditionally from a smooth oriented local domain with closed/relative boundary, `partial^2=0`, consistent orientation and no regulator joints; otherwise it needs a finite corner measure times density bound.

## Firewalls

- No scalar `C_perp` promotion.
- No projected metric theorem by closure.
- No `C_corner=0` by assertion.
- No ignoring regulator joints/collars.
- No local-GR/Newton/PPN/R10 claim from this checkpoint.
"""
    write_text(RESUME_PATH, content)


def write_docs(timestamp: str) -> None:
    sources = parse_csv(SOURCE_REGISTER_CSV)
    trio_rows = parse_csv(TRIO_OUTPUT_CSV)
    corner_rows = parse_csv(CORNER_OUTPUT_CSV)
    edge_rows = parse_csv(EDGE_UPDATE_CSV)
    gates = parse_csv(GATE_CSV)
    firewall_rows = parse_csv(FIREWALL_CSV)
    decisions = parse_csv(DECISION_CSV)
    statuses = parse_csv(STATUS_CSV)
    validation = parse_csv(VALIDATION_CSV)

    content = f"""# 4793 - Source parent C/P_D/d_rel trio or edge-bound first fill

Marker: `{MARKER}`
Generated: `{timestamp}`
Decision: `{DECISION}`

## Result

4793 does two useful things.

First, it refuses to resurrect the scalar `C_perp` route as a theorem. The scalar/projected-metric path stays closure-only unless a genuinely new parent source appears. The least-circular theorem route is the lifted `C` sector: a form/holonomy/three-form style object that can in principle own form degree, relative cohomology, boundary class and the local/FLRW split.

Second, it makes the first edge term concrete. `C_corner` is no longer a vague boundary debt:

```text
smooth oriented local domain U
  + closed/relative boundary S
  + partial(partial U)=0
  + consistent orientation
  + no regulator joints/collars
    => C_corner = 0
```

If those domain clauses are not certified, the fallback is finite: `|C_corner| <= corner_measure * corner_density_bound`.

## Source Register

{markdown_table(sources, ["source_id", "source_path", "exists", "needle_found", "role"])}

## Parent Trio Output

{markdown_table(trio_rows, ["trio_id", "route", "Z_parent_trio", "Z_lifted_route", "runner_status", "missing_trio_clauses", "anti_circularity_status"])}

## Ccorner Output

{markdown_table(corner_rows, ["corner_id", "C_corner_abs", "corner_measure", "corner_density_bound", "runner_status", "missing_corner_inputs", "anti_circularity_status"])}

## Edge Update

{markdown_table(edge_rows, ["edge_id", "quantity", "status", "value_or_bound", "meaning", "feeds"])}

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
    write_text(FORMAL_PATH, content.replace("# 4793 -", "# 809 - PPC4161 "))

    append_once(
        SPINE_PATH,
        MARKER,
        f"""
## {MARKER}

- 4793 keeps the scalar `C_perp`/projected-metric branch demoted to closure-only and selects the lifted `C` sector as the least-circular source route for parent `C/P_D/d_rel`.
- The first edge term now has an exact conditional zero law: `C_corner=0` for a smooth oriented local domain with closed/relative boundary, `partial^2=0`, consistent orientation and no regulator joints.
- If that domain certificate is not sourced, the finite fallback is explicit: `|C_corner| <= corner_measure * corner_density_bound`.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## {PACKET_MARKER}

4793 adds the parent lifted `C/P_D/d_rel` trio gate and first `C_corner` zero-or-bound gate. The physical branch still lacks the lifted parent action/projector/d_rel stack and local domain certificate, but the first edge term now has exact zero conditions and a finite bound fallback. Next target: `{NEXT_TARGET}`.
""",
    )


def main() -> int:
    timestamp = now()
    write_csv(SOURCE_REGISTER_CSV, source_register(timestamp))
    write_csv(TRIO_INPUT_CSV, trio_input_rows(timestamp))
    write_csv(CORNER_INPUT_CSV, corner_input_rows(timestamp))
    run_command([sys.executable, str(RUNNER), str(TRIO_INPUT_CSV), str(TRIO_OUTPUT_CSV), str(CORNER_INPUT_CSV), str(CORNER_OUTPUT_CSV)])

    trio_rows = parse_csv(TRIO_OUTPUT_CSV)
    corner_rows = parse_csv(CORNER_OUTPUT_CSV)
    write_csv(EDGE_UPDATE_CSV, edge_update_rows(timestamp, corner_rows))
    write_csv(GATE_CSV, gate_rows(timestamp, trio_rows, corner_rows))
    write_csv(FIREWALL_CSV, firewalls(timestamp))
    write_csv(DECISION_CSV, decision_rows(timestamp))
    write_csv(STATUS_CSV, status_rows(timestamp, trio_rows, corner_rows))
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
