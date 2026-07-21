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

CHECKPOINT = "4795"
CLAIM_ID = "L-637"
MARKER = "PPC4161_JC_FROM_Q_PARENT_VARIATION_PD_OWNER_OR_DSFEPS_CERTIFICATE_4795"
PACKET_MARKER = "PPC4161_PACKET_JC_FROM_Q_PARENT_VARIATION_PD_OWNER_OR_DSFEPS_CERTIFICATE_4795"
DECISION = "JC_VARIATION_VOLUME_OBSTRUCTION_COMPUTED_PD_OWNER_BLOCKED_DSFEPS_ZERO_OR_BOUND_GATE_READY"
NEXT_TARGET = "4796-Y5-R2FR-parent-volume-lock-selector-or-finite-edge-bound-fill.md"

DOC_PATH = POST / "4795-Y5-R2FR-JC-from-Q-parent-variation-PD-owner-or-dSFeps-certificate.md"
FORMAL_PATH = FORMAL / "811-PPC4161-JC-from-Q-parent-variation-PD-owner-or-dSFeps-certificate.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"

RUNNER = SCRIPT_DIR / "JC_variation_PD_dSFeps_gate_runner.py"

SOURCE_REGISTER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4795_SOURCE_REGISTER.csv"
VARIATION_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4795_JC_VARIATION_INPUT.csv"
VARIATION_OUTPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4795_JC_VARIATION_OUTPUT.csv"
PD_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4795_PD_OWNER_INPUT.csv"
PD_OUTPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4795_PD_OWNER_OUTPUT.csv"
DSFEPS_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4795_DSFEPS_INPUT.csv"
DSFEPS_OUTPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4795_DSFEPS_OUTPUT.csv"
OBSTRUCTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4795_OBSTRUCTION_UPDATE.csv"
GATE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4795_PROMOTION_GATES.csv"
FIREWALL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4795_FIREWALL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4795_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4795_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4795_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4795_VALIDATION.csv"

JC_VARIATION_CLAUSES = (
    "JC_definition_from_Q_signed",
    "detQ_variation_identity_signed",
    "coframe_volume_variation_rule_signed",
    "normalization_ND_variation_rule_signed",
    "domain_variation_or_fixed_domain_signed",
    "top_form_closedness_signed",
    "parent_action_density_signed",
    "constraint_multiplier_owned",
    "PD_owner_connected_to_domain_signed",
    "drel_source_terms_signed",
    "volume_lock_selector_signed",
    "FLRW_active_class_preserved_signed",
    "matter_selector_same_domain_signed",
    "no_action_by_declaration_signed",
)

PD_OWNER_CLAUSES = (
    "PD_domain_representative_signed",
    "PD_idempotence_signed",
    "deltaPD_variation_signed",
    "PD_metric_dependency_accounted",
    "PD_stress_tensor_accounted",
    "PD_drel_commutator_signed",
    "PD_boundary_class_preserved",
    "PD_no_postfit_domain_signed",
    "PD_no_label_only_signed",
)

DSFEPS_ZERO_CLAUSES = (
    "surface_S_signed",
    "F_lambda_defined_on_S",
    "epsilon_X_allowed_generator_signed",
    "dS_operator_signed",
    "dS_Fepsilon_zero_signed",
    "no_physical_charge_erased_signed",
    "boundary_class_fixed_signed",
    "no_dSFeps_zero_by_assertion_signed",
)

SOURCE_SPECS = [
    ("SRC4795_00_4794_doc", POST / "4794-Y5-R2FR-lifted-C-action-PD-drel-contract-or-domain-corner-certificate.md", "DEC4794_0_detQ", "4794 detQ/J_C handoff"),
    ("SRC4795_01_1166_doc", POST / "1166-Y5-R10-JC-from-Q-parent-variation-or-local-corner-certificate.md", "local volume-lock/domain-selector theorem", "older J_C variation obstruction"),
    ("SRC4795_02_1166_variation", SOURCE_DIR / "P8_Y5_R10_1166_JC_FROM_Q_VARIATION_DERIVATION.csv", "JCV1166_4_relative_obstruction", "relative obstruction is domain integral"),
    ("SRC4795_03_1166_criterion", SOURCE_DIR / "P8_Y5_R10_1166_RELATIVE_EXACTNESS_CRITERION.csv", "REC1166_2_exactness_condition", "relative exactness criterion"),
    ("SRC4795_04_207_PD", POST / "207-domain-projector-action-and-Bianchi-identity.md", "physical domain selection is still missing.", "domain projector/Bianchi source"),
    ("SRC4795_05_1020_kernel", POST / "1020-Y5-R10-boundary-cohomology-domain-certificate-or-source-pack-first-row.md", "BDC1020_4_kernel_weight", "dS(F epsilon) zero/bound requirement"),
    ("SRC4795_06_1020_stokes", POST / "1020-Y5-R10-boundary-cohomology-domain-certificate-or-source-pack-first-row.md", "ETB1020_1_weighted_Stokes_identity", "weighted Stokes derivative term"),
    ("SRC4795_07_runner", RUNNER, "def dsfeps_row", "4795 runner"),
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


def variation_input_rows(timestamp: str) -> list[dict[str, Any]]:
    physical = clause_map(JC_VARIATION_CLAUSES, False)
    for clause in (
        "JC_definition_from_Q_signed",
        "detQ_variation_identity_signed",
        "coframe_volume_variation_rule_signed",
        "normalization_ND_variation_rule_signed",
        "domain_variation_or_fixed_domain_signed",
        "top_form_closedness_signed",
        "no_action_by_declaration_signed",
    ):
        physical[clause] = True
    numeric = physical.copy()
    signed = clause_map(JC_VARIATION_CLAUSES, True)

    def row(row_id: str, status: str, source: str, clauses: dict[str, bool], values: dict[str, str] | None = None) -> dict[str, Any]:
        payload = {
            "variation_id": row_id,
            "JC_source": source,
            "variation_source": source,
            "PD_source": source,
            "drel_source": source,
            "volume_lock_source": source,
            "provenance": source,
            "notes": "",
            "JC_density": "",
            "trace_Qinv_dQ": "",
            "delta_log_omega0": "",
            "delta_log_ND": "",
            "domain_boundary_flux_density": "",
            "domain_volume": "",
            "target_volume_lock": "",
            "row_status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
            **clauses,
        }
        if values:
            payload.update(values)
        return payload

    return [
        row("physical_JC_variation_missing_parent", "physical_branch_nonclaim", str(POST / "1166-Y5-R10-JC-from-Q-parent-variation-or-local-corner-certificate.md"), physical),
        row(
            "JC_variation_volume_obstruction_smoke",
            "variation_obstruction_smoke_nonclaim",
            str(VARIATION_INPUT_CSV),
            numeric,
            {
                "JC_density": "1.2",
                "trace_Qinv_dQ": "0.1916666666666667",
                "delta_log_omega0": "0.01",
                "delta_log_ND": "0.02",
                "domain_boundary_flux_density": "0.001",
                "domain_volume": "5.0",
                "target_volume_lock": "0.0",
            },
        ),
        row("conditional_volume_lock_packet", "conditional_reference_theorem_nonclaim", "CONDITIONAL_JC_VARIATION_VOLUME_LOCK_ALL_CLAUSES_SIGNED", signed),
        row("forbidden_volume_lock_assertion_control", "forbidden_control_nonclaim", "VOLUME_LOCK_BY_ASSERTION_ACTION_BY_DECLARATION_LOCAL_FLRW_HAND_SWITCH", signed),
    ]


def pd_input_rows(timestamp: str) -> list[dict[str, Any]]:
    physical = clause_map(PD_OWNER_CLAUSES, False)
    for clause in ("PD_no_postfit_domain_signed", "PD_no_label_only_signed"):
        physical[clause] = True
    idempotent_only = physical.copy()
    idempotent_only["PD_domain_representative_signed"] = True
    idempotent_only["PD_idempotence_signed"] = True
    signed = clause_map(PD_OWNER_CLAUSES, True)

    def row(row_id: str, status: str, source: str, clauses: dict[str, bool]) -> dict[str, Any]:
        return {
            "pd_id": row_id,
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
        row("physical_PD_owner_missing", "physical_branch_nonclaim", str(POST / "207-domain-projector-action-and-Bianchi-identity.md"), physical),
        row("PD_idempotent_shape_not_enough", "idempotent_shape_nonclaim", str(PD_INPUT_CSV), idempotent_only),
        row("conditional_PD_owner_packet", "conditional_reference_theorem_nonclaim", "CONDITIONAL_PD_OWNER_VARIATION_ALL_CLAUSES_SIGNED", signed),
        row("forbidden_PD_by_label_control", "forbidden_control_nonclaim", "PD_BY_LABEL_PD_BY_DECLARATION_POSTFIT_REFERENCE", signed),
    ]


def dsfeps_input_rows(timestamp: str) -> list[dict[str, Any]]:
    physical = clause_map(DSFEPS_ZERO_CLAUSES, False)
    physical["no_dSFeps_zero_by_assertion_signed"] = True
    zero = clause_map(DSFEPS_ZERO_CLAUSES, True)
    finite = physical.copy()
    for clause in ("surface_S_signed", "F_lambda_defined_on_S", "epsilon_X_allowed_generator_signed", "dS_operator_signed", "boundary_class_fixed_signed"):
        finite[clause] = True
    source = str(DSFEPS_INPUT_CSV)

    def row(row_id: str, status: str, source_text: str, clauses: dict[str, bool], norm: str = "", primitive: str = "") -> dict[str, Any]:
        return {
            "dsfeps_id": row_id,
            "surface_source": source_text,
            "epsilon_source": source_text,
            "bound_source": source_text,
            "zero_theorem_path": source_text,
            "provenance": source_text,
            "notes": "",
            "norm_dS_Feps": norm,
            "norm_bC": primitive,
            "row_status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
            **clauses,
        }

    return [
        row("physical_dSFeps_missing", "physical_branch_missing_kernel_certificate_nonclaim", "MISSING_DSFEPS_SOURCE", physical),
        row("closed_weight_dSFeps_zero", "conditional_closed_weight_nonclaim", "CLOSED_WEIGHT_AND_ALLOWED_EPSILON_CERTIFICATE", zero, "", "2.0e-5"),
        row("finite_dSFeps_bound_smoke", "finite_bound_smoke_nonclaim", source, finite, "3.0e-4", "2.0e-5"),
        row("forbidden_proper_gauge_erase_control", "forbidden_control_nonclaim", "DSFEPS_ZERO_BY_ASSERTION_PROPER_GAUGE_ERASES_PHYSICAL_CHARGE", zero),
    ]


def obstruction_rows(timestamp: str, variation_rows: list[dict[str, str]], pd_rows: list[dict[str, str]], dsfeps_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    variation = next(row for row in variation_rows if row["variation_id"] == "JC_variation_volume_obstruction_smoke")
    pd = next(row for row in pd_rows if row["pd_id"] == "physical_PD_owner_missing")
    dsfeps = next(row for row in dsfeps_rows if row["dsfeps_id"] == "finite_dSFeps_bound_smoke")
    return [
        {
            "update_id": "OBS4795_0_volume_obstruction",
            "item": "int_D delta J_C",
            "status": variation["runner_status"],
            "value_or_bound": variation["volume_lock_abs"],
            "meaning": "relative exactness is blocked unless a parent volume-lock selector sets this local integral to zero",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "update_id": "OBS4795_1_PD_owner",
            "item": "P_D owner and variation",
            "status": pd["runner_status"],
            "value_or_bound": pd["missing_PD_clauses"],
            "meaning": "idempotent notation is insufficient until delta P_D and stress/source terms are owned",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "update_id": "OBS4795_2_dSFeps_bound",
            "item": "weighted-Stokes derivative term",
            "status": dsfeps["runner_status"],
            "value_or_bound": dsfeps["dSFeps_bound_abs"],
            "meaning": "if closed-weight zero fails, d_S(F epsilon) contributes a finite norm product",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def gate_rows(timestamp: str, variation_rows: list[dict[str, str]], pd_rows: list[dict[str, str]], dsfeps_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    physical_variation = next(row for row in variation_rows if row["variation_id"] == "physical_JC_variation_missing_parent")
    physical_pd = next(row for row in pd_rows if row["pd_id"] == "physical_PD_owner_missing")
    physical_dsfeps = next(row for row in dsfeps_rows if row["dsfeps_id"] == "physical_dSFeps_missing")
    return [
        {
            "gate_id": "PG4795_0_volume_lock",
            "claim": "local int_D delta J_C volume-lock selector is physically derived",
            "gate_pass": False,
            "reason": "physical variation branch still lacks parent action, P_D, d_rel, volume-lock selector, FLRW preservation and matter selector",
            "evidence": physical_variation["missing_variation_inputs"],
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "PG4795_1_PD_owner",
            "claim": "P_D owner/variation is physically sourced",
            "gate_pass": False,
            "reason": "physical P_D row lacks representative, idempotence, deltaP_D, stress, commutator and boundary-class ownership",
            "evidence": physical_pd["missing_PD_clauses"],
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "PG4795_2_dSFeps",
            "claim": "physical d_S(F epsilon) term is zero or bounded",
            "gate_pass": False,
            "reason": "physical kernel/generator source remains missing",
            "evidence": physical_dsfeps["missing_dSFeps_inputs"],
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "PG4795_3_local_GR_Newton",
            "claim": "local GR/Newton/PPN promotion allowed",
            "gate_pass": False,
            "reason": "volume lock, P_D owner and physical dSFeps certificate remain nonclaim",
            "evidence": "nonclaim firewall active",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def firewalls(timestamp: str) -> list[dict[str, Any]]:
    rules = [
        ("FW4795_0_no_volume_lock_assertion", "int_D delta J_C=0 must come from a parent selector, not a hand switch."),
        ("FW4795_1_no_PD_label", "P_D must include deltaP_D and stress/source accounting, not just idempotent notation."),
        ("FW4795_2_no_dSFeps_assertion", "d_S(F epsilon)=0 must preserve physical charges or be replaced by a finite norm bound."),
        ("FW4795_3_no_edge_cancellation", "Do not cancel unknown edge terms against each other; bound them term-by-term."),
        ("FW4795_4_no_local_claim", "No local-GR/Newton/R10/PPN/WEP/clock/orbital claim follows from 4795."),
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
            "decision_id": "DEC4795_0_volume_obstruction",
            "decision": "relative_exactness_reduced_to_volume_lock",
            "reason": "J_C variation computes a coherent local integral obstruction; exactness requires int_D delta J_C=0 in the local branch",
            "next_action": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC4795_1_PD_owner",
            "decision": "PD_owner_is_next_parent_source_burden",
            "reason": "without deltaP_D and projector stress, the action variation cannot be conservation-safe",
            "next_action": "derive P_D from a parent domain functional or demote it to finite source-bound input",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC4795_2_dSFeps",
            "decision": "dSFeps_zero_or_bound_gate_ready",
            "reason": "weighted Stokes derivative term now has both closed-weight zero conditions and finite norm-product fallback",
            "next_action": "source closed-weight/allowed-epsilon certificate or fill norm_dS_Feps and norm_bC",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def status_rows(timestamp: str, variation_rows: list[dict[str, str]], pd_rows: list[dict[str, str]], dsfeps_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    variation = next(row for row in variation_rows if row["variation_id"] == "JC_variation_volume_obstruction_smoke")
    physical_pd = next(row for row in pd_rows if row["pd_id"] == "physical_PD_owner_missing")
    finite_dsfeps = next(row for row in dsfeps_rows if row["dsfeps_id"] == "finite_dSFeps_bound_smoke")
    return [
        {
            "status_id": "STATUS4795_0_volume_obstruction",
            "status": variation["runner_status"],
            "detail": f"delta_JC_integral={variation['delta_JC_integral']}; volume_lock_abs={variation['volume_lock_abs']}",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "status_id": "STATUS4795_1_PD_owner",
            "status": physical_pd["runner_status"],
            "detail": physical_pd["missing_PD_clauses"],
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "status_id": "STATUS4795_2_dSFeps_bound",
            "status": finite_dsfeps["runner_status"],
            "detail": finite_dsfeps["dSFeps_bound_abs"],
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "status_id": "STATUS4795_3_selected_next",
            "status": "PARENT_VOLUME_LOCK_SELECTOR_OR_FINITE_EDGE_BOUND_FILL",
            "detail": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "next_id": "NEXT4795_0_4796",
            "next_target": NEXT_TARGET,
            "objective": "derive or reject the parent law enforcing int_D delta J_C=0 on local stationary domains while preserving FLRW coherent class; if rejected, fill finite edge-bound rows",
            "include": "volume-lock selector; local stationarity; FLRW class; P_D variation; N_D normalization; dSFeps norm; bC norm; harmonic/residual edge terms",
            "exclude": "local/FLRW hand switch; P_D by label; dSFeps zero by assertion; edge cancellation; local-GR claim",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
    ]


def validation_rows(timestamp: str) -> list[dict[str, Any]]:
    sources = parse_csv(SOURCE_REGISTER_CSV)
    variations = parse_csv(VARIATION_OUTPUT_CSV)
    pd_rows = parse_csv(PD_OUTPUT_CSV)
    dsfeps_rows = parse_csv(DSFEPS_OUTPUT_CSV)
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

    physical_variation = next(row for row in variations if row["variation_id"] == "physical_JC_variation_missing_parent")
    computed_variation = next(row for row in variations if row["variation_id"] == "JC_variation_volume_obstruction_smoke")
    conditional_variation = next(row for row in variations if row["variation_id"] == "conditional_volume_lock_packet")
    forbidden_variation = next(row for row in variations if row["variation_id"] == "forbidden_volume_lock_assertion_control")
    physical_pd = next(row for row in pd_rows if row["pd_id"] == "physical_PD_owner_missing")
    shape_pd = next(row for row in pd_rows if row["pd_id"] == "PD_idempotent_shape_not_enough")
    conditional_pd = next(row for row in pd_rows if row["pd_id"] == "conditional_PD_owner_packet")
    forbidden_pd = next(row for row in pd_rows if row["pd_id"] == "forbidden_PD_by_label_control")
    physical_dsfeps = next(row for row in dsfeps_rows if row["dsfeps_id"] == "physical_dSFeps_missing")
    zero_dsfeps = next(row for row in dsfeps_rows if row["dsfeps_id"] == "closed_weight_dSFeps_zero")
    finite_dsfeps = next(row for row in dsfeps_rows if row["dsfeps_id"] == "finite_dSFeps_bound_smoke")
    forbidden_dsfeps = next(row for row in dsfeps_rows if row["dsfeps_id"] == "forbidden_proper_gauge_erase_control")

    add("VAL4795_0_sources", "all cited sources exist and needles are found", all(bool_text(row["exists"]) and bool_text(row["needle_found"]) for row in sources), str(SOURCE_REGISTER_CSV))
    add("VAL4795_1_physical_variation_blocks", "physical J_C variation remains blocked by parent source clauses", physical_variation["runner_status"] == "BLOCKED_MISSING_JC_VARIATION_OR_VOLUME_LOCK_INPUTS" and "MISSING_parent_action_density_signed" in physical_variation["missing_variation_inputs"], str(VARIATION_OUTPUT_CSV))
    add("VAL4795_2_volume_obstruction_computes", "J_C variation smoke computes nonzero volume-lock obstruction", computed_variation["runner_status"] == "JC_VARIATION_COMPUTED_VOLUME_LOCK_OPEN_NONCLAIM" and computed_variation["volume_lock_abs"] != "MISSING_NUMERIC_VALUE", str(VARIATION_OUTPUT_CSV))
    add("VAL4795_3_conditional_volume_lock", "conditional volume-lock theorem zeros obstruction", conditional_variation["runner_status"] == "JC_VARIATION_VOLUME_LOCK_CONDITIONAL_PARENT_THEOREM_NONCLAIM", str(VARIATION_OUTPUT_CSV))
    add("VAL4795_4_forbidden_variation_fails", "volume lock/action by assertion fails", forbidden_variation["runner_status"] == "FAILED_JC_VARIATION_GATE", str(VARIATION_OUTPUT_CSV))
    add("VAL4795_5_physical_PD_blocks", "physical P_D owner remains blocked", physical_pd["runner_status"] == "PD_OWNER_PARTIAL_BLOCKED_NONCLAIM", str(PD_OUTPUT_CSV))
    add("VAL4795_6_PD_shape_not_enough", "idempotent P_D shape is not enough", shape_pd["runner_status"] == "PD_OWNER_PARTIAL_BLOCKED_NONCLAIM" and "deltaPD_variation_signed" in shape_pd["missing_PD_clauses"], str(PD_OUTPUT_CSV))
    add("VAL4795_7_conditional_PD", "conditional P_D owner passes as nonclaim", conditional_pd["runner_status"] == "PD_OWNER_VARIATION_CONDITIONAL_NONCLAIM", str(PD_OUTPUT_CSV))
    add("VAL4795_8_forbidden_PD_fails", "P_D by label/postfit source fails", forbidden_pd["runner_status"] == "FAILED_PD_OWNER_GATE", str(PD_OUTPUT_CSV))
    add("VAL4795_9_physical_dSFeps_blocks", "physical dSFeps source remains missing", physical_dsfeps["runner_status"] == "BLOCKED_MISSING_DSFEPS_ZERO_OR_BOUND_INPUTS", str(DSFEPS_OUTPUT_CSV))
    add("VAL4795_10_dSFeps_zero", "closed-weight allowed-epsilon branch zeros dSFeps conditionally", zero_dsfeps["runner_status"] == "DSFEPS_ZERO_CERTIFIED_CONDITIONAL_NONCLAIM", str(DSFEPS_OUTPUT_CSV))
    add("VAL4795_11_dSFeps_bound", "finite dSFeps bound computes", finite_dsfeps["runner_status"] == "DSFEPS_FINITE_BOUND_COMPUTED_NONCLAIM" and finite_dsfeps["dSFeps_bound_abs"] != "MISSING_NUMERIC_VALUE", str(DSFEPS_OUTPUT_CSV))
    add("VAL4795_12_forbidden_dSFeps_fails", "dSFeps zero/proper gauge erase shortcut fails", forbidden_dsfeps["runner_status"] == "FAILED_DSFEPS_GATE", str(DSFEPS_OUTPUT_CSV))
    add("VAL4795_13_claim", "claim register includes L-637 as nonclaim", CLAIM_ID in read_text(CLAIMS_PATH), str(CLAIMS_PATH))
    add("VAL4795_14_resume", "resume points at 4796", NEXT_TARGET in read_text(RESUME_PATH), str(RESUME_PATH))
    add("VAL4795_OVERALL", "all 4795 J_C/P_D/dSFeps checks pass", all(row["result"] == "PASS" for row in validation), DECISION)
    return validation


def write_claim(timestamp: str) -> None:
    if CLAIMS_PATH.exists() and any(row.get("claim_id") == CLAIM_ID for row in parse_csv(CLAIMS_PATH)):
        return
    with CLAIMS_PATH.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = reader.fieldnames or []
    row = {
        "claim_id": CLAIM_ID,
        "domain": "JC_variation_PD_dSFeps_gate_runner",
        "claim": "4795 computes the lifted J_C variation/volume-lock obstruction, keeps P_D owner blocked, and installs dS(F epsilon) zero-or-bound gate.",
        "current_evidence": "Generated source register, J_C variation input/output, P_D owner input/output, dSFeps input/output, obstruction update, gates, firewalls, decision, status, next target and validation.",
        "status": "JC_volume_obstruction_nonclaim_PD_owner_blocked_dSFeps_gate_ready",
        "next_test": NEXT_TARGET,
        "key_risk": "Do not assume int_D delta J_C=0, P_D ownership, or dS(F epsilon)=0 without source certificates.",
        "sector": "local_gr",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "volume-lock assertion; P_D by label; dSFeps zero by assertion; proper gauge erases physical charge; local-GR promotion",
        "title": "J_C variation, P_D owner, and dSFeps gate",
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

4795 computes the lifted `J_C` variation obstruction explicitly. With `J_C=N_D^-1 det(Q) omega_0`, the local variation density is `J_C[Tr(Q^-1 delta Q)+delta log omega_0-delta log N_D]` plus domain boundary flux. Relative exactness now hinges on a parent volume-lock selector enforcing `int_D delta J_C=0` on local stationary domains while preserving the FLRW coherent class. The physical branch still lacks that selector and the variational owner for `P_D`. The next weighted-Stokes edge term is also explicit: `d_S(F epsilon)=0` needs a closed-weight/allowed-generator certificate, otherwise it contributes `||d_S(F epsilon)|| ||B_C||`.

## Firewalls

- No local volume lock by assertion.
- No `P_D` by label or postfit domain selection.
- No `d_S(F epsilon)=0` if it erases physical charge.
- No cancellation between unknown edge terms.
- No local-GR/Newton/PPN/R10 claim from this checkpoint.
"""
    write_text(RESUME_PATH, content)


def write_docs(timestamp: str) -> None:
    sources = parse_csv(SOURCE_REGISTER_CSV)
    variations = parse_csv(VARIATION_OUTPUT_CSV)
    pd_rows = parse_csv(PD_OUTPUT_CSV)
    dsfeps_rows = parse_csv(DSFEPS_OUTPUT_CSV)
    obstruction = parse_csv(OBSTRUCTION_CSV)
    gates = parse_csv(GATE_CSV)
    firewall_rows = parse_csv(FIREWALL_CSV)
    decisions = parse_csv(DECISION_CSV)
    statuses = parse_csv(STATUS_CSV)
    validation = parse_csv(VALIDATION_CSV)

    content = f"""# 4795 - J_C from Q parent variation, P_D owner, or dSFeps certificate

Marker: `{MARKER}`
Generated: `{timestamp}`
Decision: `{DECISION}`

## Result

4795 pushes the lifted `J_C` route from identity to obstruction:

```text
J_C = N_D^-1 det(Q) omega_0
delta J_C = J_C[Tr(Q^-1 delta Q) + delta log omega_0 - delta log N_D] + domain_flux
relative silence needs int_D delta J_C = 0
```

That last line is the new hard law: a parent local volume-lock/domain selector. The checkpoint also tests `P_D` ownership and refuses idempotent notation without `delta P_D` and stress accounting.

The edge fallback is sharpened too:

```text
int_S F epsilon d_S B_C
  = corner term - int_S d_S(F epsilon) wedge B_C
|derivative term| <= ||d_S(F epsilon)|| ||B_C||
```

## Source Register

{markdown_table(sources, ["source_id", "source_path", "exists", "needle_found", "role"])}

## J_C Variation Output

{markdown_table(variations, ["variation_id", "delta_JC_density", "delta_JC_integral", "volume_lock_abs", "runner_status", "missing_variation_inputs", "anti_circularity_status"])}

## P_D Owner Output

{markdown_table(pd_rows, ["pd_id", "Z_PD_owner", "Z_deltaPD", "runner_status", "missing_PD_clauses", "anti_circularity_status"])}

## dSFeps Output

{markdown_table(dsfeps_rows, ["dsfeps_id", "norm_dS_Feps", "norm_bC", "dSFeps_bound_abs", "runner_status", "missing_dSFeps_inputs", "anti_circularity_status"])}

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
    write_text(FORMAL_PATH, content.replace("# 4795 -", "# 811 - PPC4161 "))

    append_once(
        SPINE_PATH,
        MARKER,
        f"""
## {MARKER}

- 4795 computes the lifted `J_C` variation obstruction: relative exactness needs a parent local volume-lock selector forcing `int_D delta J_C=0`.
- `P_D` ownership is now a strict source burden: idempotence alone is not enough without `delta P_D`, stress accounting, d_rel commutator and boundary-class preservation.
- The `d_S(F epsilon)` edge term has a zero-or-bound gate: closed-weight/allowed-generator zero or finite `||d_S(F epsilon)|| ||B_C||`.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## {PACKET_MARKER}

4795 adds the lifted `J_C` volume-lock obstruction, `P_D` owner gate and `d_S(F epsilon)` zero-or-bound gate to the private local packet. The next derivation target is the parent selector for `int_D delta J_C=0` or finite edge-bound fill. Next target: `{NEXT_TARGET}`.
""",
    )


def main() -> int:
    timestamp = now()
    write_csv(SOURCE_REGISTER_CSV, source_register(timestamp))
    write_csv(VARIATION_INPUT_CSV, variation_input_rows(timestamp))
    write_csv(PD_INPUT_CSV, pd_input_rows(timestamp))
    write_csv(DSFEPS_INPUT_CSV, dsfeps_input_rows(timestamp))
    run_command([sys.executable, str(RUNNER), str(VARIATION_INPUT_CSV), str(VARIATION_OUTPUT_CSV), str(PD_INPUT_CSV), str(PD_OUTPUT_CSV), str(DSFEPS_INPUT_CSV), str(DSFEPS_OUTPUT_CSV)])

    variations = parse_csv(VARIATION_OUTPUT_CSV)
    pd_rows = parse_csv(PD_OUTPUT_CSV)
    dsfeps_rows = parse_csv(DSFEPS_OUTPUT_CSV)
    write_csv(OBSTRUCTION_CSV, obstruction_rows(timestamp, variations, pd_rows, dsfeps_rows))
    write_csv(GATE_CSV, gate_rows(timestamp, variations, pd_rows, dsfeps_rows))
    write_csv(FIREWALL_CSV, firewalls(timestamp))
    write_csv(DECISION_CSV, decision_rows(timestamp))
    write_csv(STATUS_CSV, status_rows(timestamp, variations, pd_rows, dsfeps_rows))
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
