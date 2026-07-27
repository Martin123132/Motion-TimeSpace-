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

CHECKPOINT = "4794"
CLAIM_ID = "L-636"
MARKER = "PPC4161_LIFTED_C_ACTION_PD_DREL_CONTRACT_OR_DOMAIN_CORNER_CERTIFICATE_4794"
PACKET_MARKER = "PPC4161_PACKET_LIFTED_C_ACTION_PD_DREL_CONTRACT_OR_DOMAIN_CORNER_CERTIFICATE_4794"
DECISION = "DETQ_VARIATION_IDENTITY_DERIVED_LIFTED_ACTION_STILL_BLOCKED_DOMAIN_CCORNER_GATE_READY"
NEXT_TARGET = "4795-Y5-R2FR-JC-from-Q-parent-variation-PD-owner-or-dSFeps-certificate.md"

DOC_PATH = POST / "4794-Y5-R2FR-lifted-C-action-PD-drel-contract-or-domain-corner-certificate.md"
FORMAL_PATH = FORMAL / "810-PPC4161-lifted-C-action-PD-drel-contract-or-domain-corner-certificate.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"

RUNNER = SCRIPT_DIR / "lifted_C_action_domain_certificate_runner.py"

SOURCE_REGISTER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4794_SOURCE_REGISTER.csv"
ACTION_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4794_LIFTED_ACTION_INPUT.csv"
ACTION_OUTPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4794_LIFTED_ACTION_OUTPUT.csv"
DETQ_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4794_DETQ_VARIATION_INPUT.csv"
DETQ_OUTPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4794_DETQ_VARIATION_OUTPUT.csv"
DOMAIN_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4794_DOMAIN_CORNER_INPUT.csv"
DOMAIN_OUTPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4794_DOMAIN_CORNER_OUTPUT.csv"
CONTRACT_UPDATE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4794_CONTRACT_UPDATE.csv"
GATE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4794_PROMOTION_GATES.csv"
FIREWALL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4794_FIREWALL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4794_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4794_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4794_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4794_VALIDATION.csv"

ACTION_CLAUSES = (
    "JC_from_Q_or_coframe_defined",
    "detQ_variation_identity_signed",
    "JC_normalization_units_signed",
    "parent_action_density_signed",
    "constraint_multiplier_owned",
    "PD_projector_variational_owner_signed",
    "PD_idempotence_variation_signed",
    "drel_complex_instantiated_signed",
    "drel_nilpotency_signed",
    "boundary_BC_primitive_channel_signed",
    "closedness_or_source_terms_signed",
    "bianchi_ward_stress_accounting_signed",
    "matter_selector_same_domain_signed",
    "local_FLRW_selector_signed",
    "amplitude_locks_signed",
    "no_scalar_Cperp_promotion_signed",
    "no_projected_metric_by_closure_signed",
)

DOMAIN_ZERO_CLAUSES = (
    "domain_U_oriented_smooth_chain_signed",
    "boundary_S_closed_or_relative_boundary_signed",
    "partial_boundary_zero_signed",
    "no_regulator_joint_signed",
    "fixed_boundary_class_signed",
    "orientation_convention_signed",
    "allowed_variations_preserve_boundary_signed",
    "no_corner_zero_by_assertion_signed",
)

SOURCE_SPECS = [
    ("SRC4794_00_4793_doc", POST / "4793-Y5-R2FR-source-parent-C-PD-drel-trio-or-edge-bound-first-fill.md", "DEC4793_1_lifted_route", "4793 handoff to lifted C and Ccorner certificate"),
    ("SRC4794_01_1165_doc", POST / "1165-Y5-R10-lifted-C-sector-parent-action-contract-or-Ccorner-zero-bound.md", "The best branch is the `J_C` domain three-form route", "old lifted C contract"),
    ("SRC4794_02_1165_contract", SOURCE_DIR / "P8_Y5_R10_1165_LIFTED_C_PARENT_ACTION_CONTRACT.csv", "LPC1165_0_select_lifted_object", "old lifted C contract rows"),
    ("SRC4794_03_274_lifted", POST / "274-lifted-C-sector-form-holonomy-route.md", "J_C = dB_C + J_C^{top}", "lifted C decomposition"),
    ("SRC4794_04_275_detQ", POST / "275-JC-three-form-memory-current-from-Q.md", "comes from the determinant / volume form of a 3D spatial domain.", "determinant/volume origin"),
    ("SRC4794_05_1020_domain", POST / "1020-Y5-R10-boundary-cohomology-domain-certificate-or-source-pack-first-row.md", "BDC1020_0_surface_manifold", "domain/corner certificate"),
    ("SRC4794_06_1020_stokes", POST / "1020-Y5-R10-boundary-cohomology-domain-certificate-or-source-pack-first-row.md", "ETB1020_1_weighted_Stokes_identity", "weighted Stokes identity"),
    ("SRC4794_07_runner", RUNNER, "def detq_row", "4794 lifted action/domain runner"),
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


def action_input_rows(timestamp: str) -> list[dict[str, Any]]:
    physical = clause_map(ACTION_CLAUSES, False)
    for clause in ("JC_from_Q_or_coframe_defined", "detQ_variation_identity_signed", "JC_normalization_units_signed", "no_scalar_Cperp_promotion_signed", "no_projected_metric_by_closure_signed"):
        physical[clause] = True
    identity_only = physical.copy()
    signed = clause_map(ACTION_CLAUSES, True)

    def row(row_id: str, route: str, status: str, source: str, clauses: dict[str, bool]) -> dict[str, Any]:
        return {
            "action_id": row_id,
            "route": route,
            "source_path": source,
            "action_source": source,
            "JC_source": source,
            "variation_source": source,
            "PD_source": source,
            "drel_source": source,
            "provenance": source,
            "notes": "",
            "row_status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
            **clauses,
        }

    return [
        row("physical_JC_detQ_action_attempt", "J_C_from_detQ_lifted_action", "physical_branch_nonclaim", str(POST / "275-JC-three-form-memory-current-from-Q.md"), physical),
        row("detQ_variation_identity_only", "detQ_volume_variation_identity", "identity_derived_not_parent_action_nonclaim", str(ACTION_INPUT_CSV), identity_only),
        row("conditional_full_lifted_action_contract", "conditional_lifted_C_action_PD_drel", "conditional_reference_theorem_nonclaim", "CONDITIONAL_LIFTED_C_ACTION_PD_DREL_ALL_CLAUSES_SIGNED", signed),
        row("forbidden_action_by_declaration_control", "forbidden_action_shortcut", "forbidden_control_nonclaim", "ACTION_BY_DECLARATION_PD_BY_DECLARATION_DREL_BY_DECLARATION_PROJECTED_METRIC_BY_CLOSURE", signed),
    ]


def detq_input_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "detq_id": "detQ_variation_identity_smoke",
            "Q_matrix": "2,0,0,0,3,0,0,0,4",
            "dQ_matrix": "0.1,0,0,0,0.2,0,0,0,0.3",
            "epsilon": "1.0e-7",
            "source_path": str(DETQ_INPUT_CSV),
            "provenance": str(DETQ_INPUT_CSV),
            "row_status": "detQ_identity_smoke_nonclaim",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "detq_id": "singular_Q_control",
            "Q_matrix": "1,0,0,0,0,0,0,0,0",
            "dQ_matrix": "0.1,0,0,0,0.2,0,0,0,0.3",
            "epsilon": "1.0e-7",
            "source_path": str(DETQ_INPUT_CSV),
            "provenance": str(DETQ_INPUT_CSV),
            "row_status": "singular_control_nonclaim",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "detq_id": "forbidden_detQ_postfit_control",
            "Q_matrix": "2,0,0,0,3,0,0,0,4",
            "dQ_matrix": "0.1,0,0,0,0.2,0,0,0,0.3",
            "epsilon": "1.0e-7",
            "source_path": "POSTFIT_REFERENCE",
            "provenance": "POSTFIT_REFERENCE",
            "row_status": "forbidden_control_nonclaim",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def domain_input_rows(timestamp: str) -> list[dict[str, Any]]:
    physical = clause_map(DOMAIN_ZERO_CLAUSES, False)
    physical["no_corner_zero_by_assertion_signed"] = True
    zero = clause_map(DOMAIN_ZERO_CLAUSES, True)
    finite = physical.copy()
    for clause in ("orientation_convention_signed", "fixed_boundary_class_signed", "allowed_variations_preserve_boundary_signed"):
        finite[clause] = True
    source = str(DOMAIN_INPUT_CSV)

    def row(row_id: str, status: str, source_text: str, clauses: dict[str, bool], corner_measure: str = "", corner_density: str = "", joint_measure: str = "", joint_density: str = "", regulator: str = "") -> dict[str, Any]:
        return {
            "domain_id": row_id,
            "domain_source": source_text,
            "corner_source": source_text,
            "bound_source": source_text,
            "zero_theorem_path": source_text,
            "provenance": source_text,
            "notes": "",
            "corner_measure": corner_measure,
            "corner_density_bound": corner_density,
            "joint_measure": joint_measure,
            "joint_density_bound": joint_density,
            "regulator_collar_flux_abs": regulator,
            "row_status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
            **clauses,
        }

    return [
        row("physical_domain_corner_missing", "physical_branch_missing_domain_certificate_nonclaim", "MISSING_DOMAIN_CORNER_SOURCE", physical),
        row("smooth_closed_domain_certificate", "conditional_domain_certificate_nonclaim", "SMOOTH_CLOSED_RELATIVE_DOMAIN_CERTIFICATE", zero),
        row("finite_domain_corner_bound_smoke", "finite_domain_bound_smoke_nonclaim", source, finite, "2.0e-3", "4.0e-5", "1.0e-3", "2.0e-5", "3.0e-8"),
        row("forbidden_corner_assertion_control", "forbidden_control_nonclaim", "CORNER_ZERO_BY_ASSERTION_REGULATOR_IGNORED", zero),
    ]


def contract_update_rows(timestamp: str, action_rows: list[dict[str, str]], detq_rows: list[dict[str, str]], domain_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    physical_action = next(row for row in action_rows if row["action_id"] == "physical_JC_detQ_action_attempt")
    detq = next(row for row in detq_rows if row["detq_id"] == "detQ_variation_identity_smoke")
    domain_zero = next(row for row in domain_rows if row["domain_id"] == "smooth_closed_domain_certificate")
    domain_bound = next(row for row in domain_rows if row["domain_id"] == "finite_domain_corner_bound_smoke")
    return [
        {
            "update_id": "CU4794_0_detQ_identity",
            "item": "delta det(Q) identity",
            "status": detq["runner_status"],
            "result": f"linear_delta_det={detq['linear_delta_det']}; identity_error_abs={detq['identity_error_abs']}",
            "meaning": "J_C-from-volume route has a concrete first variation identity, not merely a slogan",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "update_id": "CU4794_1_action_gap",
            "item": "lifted parent action",
            "status": physical_action["runner_status"],
            "result": physical_action["missing_action_clauses"],
            "meaning": "detQ variation is not enough until action density, P_D, d_rel, boundary and matter selectors are parent-owned",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "update_id": "CU4794_2_domain_zero",
            "item": "C_corner zero certificate",
            "status": domain_zero["runner_status"],
            "result": domain_zero["domain_edge_abs"],
            "meaning": "a smooth closed/relative local domain with no regulator joints kills the corner term",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "update_id": "CU4794_3_domain_bound",
            "item": "finite domain corner bound",
            "status": domain_bound["runner_status"],
            "result": domain_bound["domain_edge_abs"],
            "meaning": "if corners/joints/collars exist, the finite residual is measure-density plus regulator flux",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def gate_rows(timestamp: str, action_rows: list[dict[str, str]], domain_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    physical_action = next(row for row in action_rows if row["action_id"] == "physical_JC_detQ_action_attempt")
    physical_domain = next(row for row in domain_rows if row["domain_id"] == "physical_domain_corner_missing")
    return [
        {
            "gate_id": "PG4794_0_lifted_action",
            "claim": "lifted J_C parent action/P_D/d_rel stack is physically sourced",
            "gate_pass": False,
            "reason": "detQ variation identity is derived, but action density, projector owner, d_rel, boundary and matter selectors remain missing",
            "evidence": physical_action["missing_action_clauses"],
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "PG4794_1_domain_corner",
            "claim": "physical domain certificate zeroes or bounds C_corner",
            "gate_pass": False,
            "reason": "physical domain/corner source remains missing",
            "evidence": physical_domain["missing_domain_inputs"],
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "PG4794_2_local_GR_Newton",
            "claim": "local GR/Newton/PPN promotion allowed",
            "gate_pass": False,
            "reason": "action contract and physical domain certificate remain nonclaim",
            "evidence": "nonclaim firewall active",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def firewalls(timestamp: str) -> list[dict[str, Any]]:
    rules = [
        ("FW4794_0_detQ_not_action", "The determinant variation identity is a real mathematical input, not a parent action by itself."),
        ("FW4794_1_projector_must_vary", "P_D must have idempotence, domain rule and delta P_D stress accounting."),
        ("FW4794_2_drel_must_be_instantiated", "d_rel needs a declared relative pair, signs, nilpotency and boundary pullback."),
        ("FW4794_3_domain_certificate", "C_corner zero requires a sourced local domain certificate, not an assertion."),
        ("FW4794_4_no_local_claim", "No local-GR/Newton/R10/PPN/WEP/clock/orbital claim follows from 4794."),
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
            "decision_id": "DEC4794_0_detQ",
            "decision": "detQ_variation_identity_is_adopted_as_first_lifted_variation_input",
            "reason": "delta det(Q)=det(Q) Tr(Q^-1 deltaQ) gives the J_C-from-volume route a concrete first variation",
            "next_action": "derive the full J_C[Q,e,D] variation including coframe/domain terms and source stress",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC4794_1_action",
            "decision": "lifted_parent_action_still_not_closed",
            "reason": "detQ identity does not provide P_D, d_rel, B_C, Bianchi/Ward accounting or matter selector",
            "next_action": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC4794_2_domain",
            "decision": "domain_corner_certificate_gate_ready",
            "reason": "C_corner has both exact zero conditions and finite bound formula; physical source row remains missing",
            "next_action": "source local domain U/S certificate or finite corner/joint/regulator bounds",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def status_rows(timestamp: str, action_rows: list[dict[str, str]], detq_rows: list[dict[str, str]], domain_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    physical_action = next(row for row in action_rows if row["action_id"] == "physical_JC_detQ_action_attempt")
    detq = next(row for row in detq_rows if row["detq_id"] == "detQ_variation_identity_smoke")
    physical_domain = next(row for row in domain_rows if row["domain_id"] == "physical_domain_corner_missing")
    return [
        {
            "status_id": "STATUS4794_0_detQ_identity",
            "status": detq["runner_status"],
            "detail": f"linear_delta_det={detq['linear_delta_det']}; finite_delta_det={detq['finite_delta_det']}; error={detq['identity_error_abs']}",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "status_id": "STATUS4794_1_action_contract",
            "status": physical_action["runner_status"],
            "detail": physical_action["missing_action_clauses"],
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "status_id": "STATUS4794_2_domain_corner",
            "status": physical_domain["runner_status"],
            "detail": physical_domain["missing_domain_inputs"],
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "status_id": "STATUS4794_3_selected_next",
            "status": "JC_FROM_Q_PARENT_VARIATION_PD_OWNER_OR_DSF_EPS_CERTIFICATE",
            "detail": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "next_id": "NEXT4794_0_4795",
            "next_target": NEXT_TARGET,
            "objective": "extend the detQ first variation into a parent J_C[Q,e,D] variation with P_D owner/d_rel source terms, or certify d_S(F epsilon)=0/bounded in the edge theorem",
            "include": "delta detQ; coframe volume variation; domain representative D; P_D variation; d_rel signs; B_C primitive source; dS_Feps zero or norm bound",
            "exclude": "action by declaration; P_D by label; d_rel by notation only; C_corner assertion; local-GR claim",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
    ]


def validation_rows(timestamp: str) -> list[dict[str, Any]]:
    sources = parse_csv(SOURCE_REGISTER_CSV)
    action_rows = parse_csv(ACTION_OUTPUT_CSV)
    detq_rows = parse_csv(DETQ_OUTPUT_CSV)
    domain_rows = parse_csv(DOMAIN_OUTPUT_CSV)
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

    physical_action = next(row for row in action_rows if row["action_id"] == "physical_JC_detQ_action_attempt")
    identity_action = next(row for row in action_rows if row["action_id"] == "detQ_variation_identity_only")
    conditional_action = next(row for row in action_rows if row["action_id"] == "conditional_full_lifted_action_contract")
    forbidden_action = next(row for row in action_rows if row["action_id"] == "forbidden_action_by_declaration_control")
    detq = next(row for row in detq_rows if row["detq_id"] == "detQ_variation_identity_smoke")
    singular = next(row for row in detq_rows if row["detq_id"] == "singular_Q_control")
    forbidden_detq = next(row for row in detq_rows if row["detq_id"] == "forbidden_detQ_postfit_control")
    physical_domain = next(row for row in domain_rows if row["domain_id"] == "physical_domain_corner_missing")
    zero_domain = next(row for row in domain_rows if row["domain_id"] == "smooth_closed_domain_certificate")
    finite_domain = next(row for row in domain_rows if row["domain_id"] == "finite_domain_corner_bound_smoke")
    forbidden_domain = next(row for row in domain_rows if row["domain_id"] == "forbidden_corner_assertion_control")

    add("VAL4794_0_sources", "all cited sources exist and needles are found", all(bool_text(row["exists"]) and bool_text(row["needle_found"]) for row in sources), str(SOURCE_REGISTER_CSV))
    add("VAL4794_1_physical_action_blocks", "physical lifted action remains blocked after detQ identity", physical_action["runner_status"] == "DETQ_VARIATION_IDENTITY_DERIVED_BUT_PARENT_ACTION_BLOCKED_NONCLAIM" and "parent_action_density_signed" in physical_action["missing_action_clauses"], str(ACTION_OUTPUT_CSV))
    add("VAL4794_2_identity_not_action", "detQ identity alone is not a parent action", identity_action["runner_status"] == "DETQ_VARIATION_IDENTITY_DERIVED_BUT_PARENT_ACTION_BLOCKED_NONCLAIM", str(ACTION_OUTPUT_CSV))
    add("VAL4794_3_conditional_action", "conditional full lifted action contract passes as nonclaim", conditional_action["runner_status"] == "LIFTED_C_ACTION_PD_DREL_CONDITIONAL_CONTRACT_NONCLAIM", str(ACTION_OUTPUT_CSV))
    add("VAL4794_4_forbidden_action_fails", "action/projector/drel by declaration fails", forbidden_action["runner_status"] == "FAILED_LIFTED_C_ACTION_CONTRACT_GATE", str(ACTION_OUTPUT_CSV))
    add("VAL4794_5_detQ_smoke", "detQ variation numeric smoke passes", detq["runner_status"] == "DETQ_VARIATION_IDENTITY_NUMERIC_SMOKE_PASS_NONCLAIM", str(DETQ_OUTPUT_CSV))
    add("VAL4794_6_singular_Q_blocks", "singular Q matrix blocks detQ variation", singular["runner_status"] == "BLOCKED_SINGULAR_Q_FOR_DETQ_VARIATION", str(DETQ_OUTPUT_CSV))
    add("VAL4794_7_forbidden_detQ_fails", "postfit detQ source fails", forbidden_detq["runner_status"] == "FAILED_DETQ_VARIATION_GATE", str(DETQ_OUTPUT_CSV))
    add("VAL4794_8_physical_domain_blocks", "physical domain corner certificate remains missing", physical_domain["runner_status"] == "BLOCKED_MISSING_DOMAIN_CORNER_ZERO_OR_BOUND_INPUTS", str(DOMAIN_OUTPUT_CSV))
    add("VAL4794_9_domain_zero", "smooth closed domain zeroes C_corner conditionally", zero_domain["runner_status"] == "DOMAIN_CCORNER_ZERO_CERTIFIED_CONDITIONAL_NONCLAIM", str(DOMAIN_OUTPUT_CSV))
    add("VAL4794_10_domain_bound", "finite domain corner/joint/regulator bound computes", finite_domain["runner_status"] == "DOMAIN_CCORNER_FINITE_BOUND_COMPUTED_NONCLAIM" and finite_domain["domain_edge_abs"] != "MISSING_NUMERIC_VALUE", str(DOMAIN_OUTPUT_CSV))
    add("VAL4794_11_forbidden_domain_fails", "corner zero/regulator shortcut fails", forbidden_domain["runner_status"] == "FAILED_DOMAIN_CORNER_CERTIFICATE_GATE", str(DOMAIN_OUTPUT_CSV))
    add("VAL4794_12_claim", "claim register includes L-636 as nonclaim", CLAIM_ID in read_text(CLAIMS_PATH), str(CLAIMS_PATH))
    add("VAL4794_13_resume", "resume points at 4795", NEXT_TARGET in read_text(RESUME_PATH), str(RESUME_PATH))
    add("VAL4794_OVERALL", "all 4794 lifted action/domain checks pass", all(row["result"] == "PASS" for row in validation), DECISION)
    return validation


def write_claim(timestamp: str) -> None:
    if CLAIMS_PATH.exists() and any(row.get("claim_id") == CLAIM_ID for row in parse_csv(CLAIMS_PATH)):
        return
    with CLAIMS_PATH.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = reader.fieldnames or []
    row = {
        "claim_id": CLAIM_ID,
        "domain": "lifted_C_action_domain_certificate_runner",
        "claim": "4794 derives/checks the detQ first-variation identity for the lifted J_C route, while keeping parent action/P_D/d_rel and physical domain-corner certificate nonclaim.",
        "current_evidence": "Generated source register, lifted action input/output, detQ variation input/output, domain corner input/output, contract update, gates, firewalls, decision, status, next target and validation.",
        "status": "detQ_variation_identity_nonclaim_lifted_action_and_domain_certificate_still_open",
        "next_test": NEXT_TARGET,
        "key_risk": "Do not treat determinant variation as a full parent action, or Ccorner zero as physical without a domain certificate.",
        "sector": "local_gr",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "action by declaration; P_D/d_rel by notation; projected metric closure; corner assertion; regulator silence",
        "title": "lifted C action and domain corner certificate",
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

4794 adds a concrete mathematical foothold for the lifted `J_C` route: the determinant/volume candidate obeys `delta det(Q)=det(Q) Tr(Q^-1 delta Q)`, and the smoke runner verifies the identity numerically. This is real progress, but it is not a parent action. The physical branch still lacks the action density, constraint owner, variational `P_D`, instantiated `d_rel`, boundary `B_C`, closedness/source terms, Bianchi/Ward stress accounting, matter selector, local/FLRW selector and amplitude locks. The domain corner gate is also sharper: `C_corner=0` is certified only with a smooth closed/relative local domain and no regulator joints; otherwise a finite corner/joint/regulator bound is required.

## Firewalls

- `delta det(Q)` is not a full action.
- No `P_D` or `d_rel` by label.
- No projected metric theorem by closure.
- No `C_corner=0` without a physical domain certificate.
- No local-GR/Newton/PPN/R10 claim from this checkpoint.
"""
    write_text(RESUME_PATH, content)


def write_docs(timestamp: str) -> None:
    sources = parse_csv(SOURCE_REGISTER_CSV)
    action_rows = parse_csv(ACTION_OUTPUT_CSV)
    detq_rows = parse_csv(DETQ_OUTPUT_CSV)
    domain_rows = parse_csv(DOMAIN_OUTPUT_CSV)
    updates = parse_csv(CONTRACT_UPDATE_CSV)
    gates = parse_csv(GATE_CSV)
    firewall_rows = parse_csv(FIREWALL_CSV)
    decisions = parse_csv(DECISION_CSV)
    statuses = parse_csv(STATUS_CSV)
    validation = parse_csv(VALIDATION_CSV)

    content = f"""# 4794 - Lifted C action/P_D/d_rel contract or domain corner certificate

Marker: `{MARKER}`
Generated: `{timestamp}`
Decision: `{DECISION}`

## Result

4794 adds the first concrete variation brick for the lifted `J_C` route:

```text
J_C ~ det(Q) vol_D
delta det(Q) = det(Q) Tr(Q^-1 delta Q)
```

The determinant identity is verified by a numeric smoke row. It helps the lifted `J_C[Q,e,D]` route become a real variation problem, but it **does not** close the parent action. The missing owners are still the action density, constraint/multiplier, variational `P_D`, instantiated `d_rel`, boundary `B_C`, closedness/source terms, Bianchi/Ward stress accounting, matter selector, local/FLRW selector and amplitude locks.

4794 also tightens the local-domain edge branch:

```text
smooth closed/relative domain + fixed boundary class + no regulator joints
  => C_corner = 0
otherwise
  |C_corner/domain edge| <= corner_measure*density + joint_measure*density + regulator_collar_flux
```

## Source Register

{markdown_table(sources, ["source_id", "source_path", "exists", "needle_found", "role"])}

## Lifted Action Output

{markdown_table(action_rows, ["action_id", "route", "Z_action_contract", "Z_detQ_variation", "runner_status", "missing_action_clauses", "anti_circularity_status"])}

## detQ Variation Output

{markdown_table(detq_rows, ["detq_id", "det_Q", "trace_Qinv_dQ", "linear_delta_det", "finite_delta_det", "identity_error_abs", "runner_status", "missing_inputs"])}

## Domain Corner Output

{markdown_table(domain_rows, ["domain_id", "C_corner_abs", "joint_abs", "regulator_abs", "domain_edge_abs", "runner_status", "missing_domain_inputs", "anti_circularity_status"])}

## Contract Update

{markdown_table(updates, ["update_id", "item", "status", "result", "meaning"])}

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
    write_text(FORMAL_PATH, content.replace("# 4794 -", "# 810 - PPC4161 "))

    append_once(
        SPINE_PATH,
        MARKER,
        f"""
## {MARKER}

- 4794 installs a concrete first-variation identity for the lifted `J_C` route: `delta det(Q)=det(Q) Tr(Q^-1 delta Q)`.
- The identity is useful but nonclaim: a full parent action still needs action density, variational `P_D`, instantiated `d_rel`, `B_C`, source terms, Bianchi/Ward stress and matter/branch selectors.
- The domain corner branch now has an exact certificate route and finite fallback: smooth closed/relative domain gives `C_corner=0`; otherwise corner/joint/regulator terms are bounded explicitly.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## {PACKET_MARKER}

4794 adds the lifted `J_C` determinant-variation check and the domain-corner certificate gate to the private local packet. The physical branch remains nonclaim, but the next derivation can now attack `J_C[Q,e,D]` variation and `P_D/d_rel` ownership directly. Next target: `{NEXT_TARGET}`.
""",
    )


def main() -> int:
    timestamp = now()
    write_csv(SOURCE_REGISTER_CSV, source_register(timestamp))
    write_csv(ACTION_INPUT_CSV, action_input_rows(timestamp))
    write_csv(DETQ_INPUT_CSV, detq_input_rows(timestamp))
    write_csv(DOMAIN_INPUT_CSV, domain_input_rows(timestamp))
    run_command([sys.executable, str(RUNNER), str(ACTION_INPUT_CSV), str(ACTION_OUTPUT_CSV), str(DETQ_INPUT_CSV), str(DETQ_OUTPUT_CSV), str(DOMAIN_INPUT_CSV), str(DOMAIN_OUTPUT_CSV)])

    action_rows = parse_csv(ACTION_OUTPUT_CSV)
    detq_rows = parse_csv(DETQ_OUTPUT_CSV)
    domain_rows = parse_csv(DOMAIN_OUTPUT_CSV)
    write_csv(CONTRACT_UPDATE_CSV, contract_update_rows(timestamp, action_rows, detq_rows, domain_rows))
    write_csv(GATE_CSV, gate_rows(timestamp, action_rows, domain_rows))
    write_csv(FIREWALL_CSV, firewalls(timestamp))
    write_csv(DECISION_CSV, decision_rows(timestamp))
    write_csv(STATUS_CSV, status_rows(timestamp, action_rows, detq_rows, domain_rows))
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
