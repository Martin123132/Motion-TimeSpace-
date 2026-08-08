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

CHECKPOINT = "4797"
CLAIM_ID = "L-639"
MARKER = "PPC4161_PARENT_CONTINUITY_SOURCE_SIGMAPHI_OR_PD_DOMAIN_FUNCTIONAL_4797"
PACKET_MARKER = "PPC4161_PACKET_PARENT_CONTINUITY_SOURCE_SIGMAPHI_OR_PD_DOMAIN_FUNCTIONAL_4797"
DECISION = "CARTAN_REYNOLDS_BALANCE_DERIVED_PD_AVERAGE_VARIATION_DERIVED_PARENT_SOURCE_SELECTOR_STILL_OPEN"
NEXT_TARGET = "4798-Y5-R2FR-local-zero-source-selector-and-PhiBC-stress-ledger.md"

DOC_PATH = POST / "4797-Y5-R2FR-parent-continuity-source-SigmaPhi-or-PD-domain-functional.md"
FORMAL_PATH = FORMAL / "813-PPC4161-parent-continuity-source-SigmaPhi-or-PD-domain-functional.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"

RUNNER = SCRIPT_DIR / "cartan_balance_pd_domain_functional_runner.py"

SOURCE_REGISTER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4797_SOURCE_REGISTER.csv"
CARTAN_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4797_CARTAN_BALANCE_INPUT.csv"
CARTAN_OUTPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4797_CARTAN_BALANCE_OUTPUT.csv"
PD_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4797_PD_DOMAIN_FUNCTIONAL_INPUT.csv"
PD_OUTPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4797_PD_DOMAIN_FUNCTIONAL_OUTPUT.csv"
OBSTRUCTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4797_OBSTRUCTION_UPDATE.csv"
GATE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4797_PROMOTION_GATES.csv"
FIREWALL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4797_FIREWALL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4797_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4797_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4797_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4797_VALIDATION.csv"

CARTAN_IDENTITY_CLAUSES = (
    "spacetime_form_mathcalJ_signed",
    "tau_flow_vector_signed",
    "cartan_formula_signed",
    "source_equation_dJ_equals_Sigma_signed",
    "phi_equals_i_tau_mathcalJ_signed",
    "reynolds_transport_domain_signed",
    "normalization_ND_variation_signed",
)

CARTAN_PARENT_CLAUSES = (
    "parent_source_selector_signed",
    "local_Sigma_zero_signed",
    "local_Phi_zero_signed",
    "domain_motion_zero_signed",
    "FLRW_top_class_preserved_signed",
    "Bianchi_Ward_stress_signed",
    "no_multiplier_closure_signed",
    "no_local_FLRW_hand_switch_signed",
)

PD_IDENTITY_CLAUSES = (
    "domain_weight_WD_parent_field_signed",
    "coframe_measure_mu_signed",
    "ND_integral_definition_signed",
    "domain_average_definition_signed",
    "PD_definition_f_minus_average_signed",
    "average_variation_identity_signed",
)

PD_PARENT_CLAUSES = (
    "delta_WD_mu_stress_accounted_signed",
    "domain_boundary_motion_accounted_signed",
    "idempotence_signed",
    "drel_commutator_accounted_signed",
    "local_FLRW_domain_class_selector_signed",
    "no_external_projector_signed",
)

SOURCE_SPECS = [
    ("SRC4797_00_4796_doc", POST / "4796-Y5-R2FR-parent-volume-lock-selector-or-finite-edge-bound-fill.md", "DEC4796_2_next", "4796 handoff to Sigma/Phi or P_D functional"),
    ("SRC4797_01_1168_doc", POST / "1168-Y5-R10-lifted-C-continuity-action-source-or-dSFeps-bound.md", "CAS1168_0_spacetime_current_split", "older Sigma/Phi split"),
    ("SRC4797_02_207_PD", POST / "207-domain-projector-action-and-Bianchi-identity.md", "Bianchi closure can be made formal;", "domain projector and Bianchi guard"),
    ("SRC4797_03_274_CD", POST / "274-lifted-C-sector-form-holonomy-route.md", "C_D[D] = N_D^{-1} integral_D J_C", "domain class observable"),
    ("SRC4797_04_275_JC", POST / "275-JC-three-form-memory-current-from-Q.md", "J_C = det(Q_coh) Omega_D / V_D", "J_C determinant/volume route"),
    ("SRC4797_05_4796_volume_output", SOURCE_DIR / "P8_Y5_R2FR_4796_PARENT_VOLUME_LOCK_OUTPUT.csv", "volume_obstruction_carried_from_4795", "current volume obstruction"),
    ("SRC4797_06_runner", RUNNER, "def cartan_balance_row", "4797 executable runner"),
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


def cartan_input_rows(timestamp: str) -> list[dict[str, Any]]:
    identity = clause_map(CARTAN_IDENTITY_CLAUSES, True)
    parent_missing = clause_map(CARTAN_PARENT_CLAUSES, False)
    parent_missing["FLRW_top_class_preserved_signed"] = True
    parent_missing["no_multiplier_closure_signed"] = True
    parent_missing["no_local_FLRW_hand_switch_signed"] = True
    physical = {**clause_map(CARTAN_IDENTITY_CLAUSES, False), **parent_missing}
    signed = {**clause_map(CARTAN_IDENTITY_CLAUSES, True), **clause_map(CARTAN_PARENT_CLAUSES, True)}
    source = str(POST / "1168-Y5-R10-lifted-C-continuity-action-source-or-dSFeps-bound.md")

    def row(balance_id: str, status: str, source_text: str, clauses: dict[str, bool], values: dict[str, str] | None = None) -> dict[str, Any]:
        payload = {
            "balance_id": balance_id,
            "cartan_source": source_text,
            "mathcalJ_source": source_text,
            "Sigma_source": source_text,
            "Phi_source": source_text,
            "domain_source": source_text,
            "normalization_source": source_text,
            "stress_source": source_text,
            "provenance": source_text,
            "notes": "",
            "delta_JC_integral": "",
            "sigma_integral": "",
            "phi_boundary_integral": "",
            "domain_motion_integral": "",
            "normalization_term": "",
            "row_status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        payload.update(clauses)
        if values:
            payload.update(values)
        return payload

    return [
        row("physical_parent_source_missing", "physical_branch_missing_parent_source_selector_nonclaim", source, physical),
        row(
            "cartan_reynolds_balance_smoke",
            "cartan_identity_balance_smoke_nonclaim",
            str(SOURCE_DIR / "P8_Y5_R2FR_4796_PARENT_VOLUME_LOCK_OUTPUT.csv"),
            {**identity, **parent_missing},
            {
                "delta_JC_integral": "1.095",
                "sigma_integral": "0.900",
                "phi_boundary_integral": "0.150",
                "domain_motion_integral": "0.040",
                "normalization_term": "0.005",
            },
        ),
        row("conditional_local_no_flux_lock", "conditional_cartan_no_flux_theorem_nonclaim", "CONDITIONAL_CARTAN_PARENT_NO_FLUX_PACKET", signed),
        row("forbidden_multiplier_closure_control", "forbidden_control_nonclaim", "MULTIPLIER_CLOSURE_AS_PROOF_CONTINUITY_BY_ASSERTION_LOCAL_FLRW_HAND_SWITCH", signed),
    ]


def pd_input_rows(timestamp: str) -> list[dict[str, Any]]:
    identity = clause_map(PD_IDENTITY_CLAUSES, True)
    parent_missing = clause_map(PD_PARENT_CLAUSES, False)
    parent_missing["no_external_projector_signed"] = True
    physical = {**clause_map(PD_IDENTITY_CLAUSES, False), **parent_missing}
    signed = {**clause_map(PD_IDENTITY_CLAUSES, True), **clause_map(PD_PARENT_CLAUSES, True)}
    source = str(POST / "207-domain-projector-action-and-Bianchi-identity.md")

    def row(pd_id: str, status: str, source_text: str, clauses: dict[str, bool], values: dict[str, str] | None = None) -> dict[str, Any]:
        payload = {
            "pd_id": pd_id,
            "PD_source": source_text,
            "WD_source": source_text,
            "measure_source": source_text,
            "variation_source": source_text,
            "drel_source": source_text,
            "stress_source": source_text,
            "provenance": source_text,
            "notes": "",
            "avg_f": "",
            "avg_delta_f": "",
            "avg_f_delta_lnWmu": "",
            "avg_delta_lnWmu": "",
            "delta_f_sample": "",
            "row_status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        payload.update(clauses)
        if values:
            payload.update(values)
        return payload

    return [
        row("physical_PD_domain_functional_missing", "physical_branch_missing_PD_domain_functional_nonclaim", source, physical),
        row(
            "PD_average_variation_identity_smoke",
            "PD_average_variation_identity_smoke_nonclaim",
            source,
            {**identity, **parent_missing},
            {
                "avg_f": "2.0",
                "avg_delta_f": "0.10",
                "avg_f_delta_lnWmu": "0.03",
                "avg_delta_lnWmu": "0.01",
                "delta_f_sample": "0.20",
            },
        ),
        row("conditional_PD_domain_functional", "conditional_PD_functional_theorem_nonclaim", "CONDITIONAL_PD_DOMAIN_FUNCTIONAL_PACKET", signed),
        row("forbidden_external_projector_control", "forbidden_control_nonclaim", "EXTERNAL_PROJECTOR_PD_BY_LABEL_FREEZE_DOMAIN_BOUNDARY_DROP_PROJECTOR_STRESS", signed),
    ]


def obstruction_rows(timestamp: str, cartan_rows: list[dict[str, str]], pd_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    physical_cartan = next(row for row in cartan_rows if row["balance_id"] == "physical_parent_source_missing")
    smoke_cartan = next(row for row in cartan_rows if row["balance_id"] == "cartan_reynolds_balance_smoke")
    physical_pd = next(row for row in pd_rows if row["pd_id"] == "physical_PD_domain_functional_missing")
    smoke_pd = next(row for row in pd_rows if row["pd_id"] == "PD_average_variation_identity_smoke")
    return [
        {
            "update_id": "OBS4797_0_cartan_identity",
            "item": "Cartan/Reynolds domain balance",
            "status": smoke_cartan["runner_status"],
            "value_or_bound": f"balance_error={smoke_cartan['cartan_balance_error_abs']}; local_lock_abs={smoke_cartan['local_lock_abs']}",
            "meaning": "the transport identity balances the residual but does not make it local-vacuum zero",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "update_id": "OBS4797_1_parent_source_selector",
            "item": "Sigma_C/Phi_C/source selector",
            "status": physical_cartan["runner_status"],
            "value_or_bound": physical_cartan["missing_cartan_inputs"],
            "meaning": "the remaining physical burden is source/flux selector and stress ownership, not the transport identity",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "update_id": "OBS4797_2_PD_variation_identity",
            "item": "delta P_D from domain average",
            "status": smoke_pd["runner_status"],
            "value_or_bound": f"delta_average={smoke_pd['delta_average']}; delta_PD_sample={smoke_pd['delta_PD_sample']}",
            "meaning": "P_D variation is no longer a label: it carries measure/domain stress terms",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "update_id": "OBS4797_3_PD_parent_functional",
            "item": "P_D parent functional",
            "status": physical_pd["runner_status"],
            "value_or_bound": physical_pd["missing_PD_inputs"],
            "meaning": "physical domain weight, boundary motion, idempotence, drel commutator and class selector still need parent ownership",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def gate_rows(timestamp: str, cartan_rows: list[dict[str, str]], pd_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    smoke_cartan = next(row for row in cartan_rows if row["balance_id"] == "cartan_reynolds_balance_smoke")
    smoke_pd = next(row for row in pd_rows if row["pd_id"] == "PD_average_variation_identity_smoke")
    return [
        {
            "gate_id": "PG4797_0_cartan_identity",
            "claim": "Cartan/Reynolds balance identity is derived",
            "gate_pass": True,
            "reason": "mathcalJ_C transport splits into Sigma/Phi/domain/normalization balance in the executable row",
            "evidence": smoke_cartan["cartan_balance_error_abs"],
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "PG4797_1_local_lock",
            "claim": "local int_D delta J_C is physically zero",
            "gate_pass": False,
            "reason": "balance identity is not enough; local Sigma/Phi/domain-motion zero theorem is still unsigned",
            "evidence": smoke_cartan["local_lock_abs"],
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "PG4797_2_PD_variation",
            "claim": "delta P_D is explicit",
            "gate_pass": True,
            "reason": "domain-average variation formula computes delta P_D with measure/domain terms",
            "evidence": smoke_pd["delta_PD_sample"],
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "PG4797_3_PD_parent_owner",
            "claim": "P_D is physically parent-owned",
            "gate_pass": False,
            "reason": "domain weight, boundary motion, drel commutator, and local/FLRW selector remain unsigned",
            "evidence": smoke_pd["missing_PD_inputs"],
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "PG4797_4_local_GR_Newton",
            "claim": "local GR/Newton/PPN/R10 promotion allowed",
            "gate_pass": False,
            "reason": "source selector and P_D parent ownership are still nonclaim",
            "evidence": "nonclaim firewall active",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def firewalls(timestamp: str) -> list[dict[str, Any]]:
    rules = [
        ("FW4797_0_no_multiplier_closure", "A multiplier may impose continuity but does not by itself derive Sigma_C/Phi_C/source selection."),
        ("FW4797_1_no_balance_as_silence", "A Cartan balance with nonzero Sigma/Phi/domain terms is not local-vacuum silence."),
        ("FW4797_2_no_external_projector", "P_D must be a varied domain functional; external/frozen projectors are rejected."),
        ("FW4797_3_no_hidden_stress", "Domain weight, boundary motion, projector, Sigma_C and Phi_C stress must remain in the Ward ledger."),
        ("FW4797_4_no_local_claim", "No local-GR/Newton/R10/PPN/WEP/clock/orbital claim follows from 4797."),
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
            "decision_id": "DEC4797_0_cartan_result",
            "decision": "Cartan_Reynolds_transport_identity_is_adopted",
            "reason": "Sigma_C and Phi_C are no longer free words: they are source and boundary-flux pieces of transported mathcalJ_C",
            "next_action": "derive the parent selector that makes Sigma_C=Phi_C=domain_motion=0 locally while preserving FLRW top class",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC4797_1_PD_result",
            "decision": "P_D_variation_must_use_domain_average_functional",
            "reason": "delta P_D contains delta f plus weighted-measure/domain terms, so projector stress cannot be dropped",
            "next_action": "source W_D/mu/domain-boundary motion and add stress ledger rows",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC4797_2_next",
            "decision": "target_source_selector_and_PhiBC_stress_ledger",
            "reason": "the mathematical identities are now separated from the dynamical parent source/flux ownership",
            "next_action": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def status_rows(timestamp: str, cartan_rows: list[dict[str, str]], pd_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    smoke_cartan = next(row for row in cartan_rows if row["balance_id"] == "cartan_reynolds_balance_smoke")
    smoke_pd = next(row for row in pd_rows if row["pd_id"] == "PD_average_variation_identity_smoke")
    return [
        {
            "status_id": "STATUS4797_0_cartan_balance",
            "status": smoke_cartan["runner_status"],
            "detail": f"balance_error={smoke_cartan['cartan_balance_error_abs']}; local_lock_abs={smoke_cartan['local_lock_abs']}",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "status_id": "STATUS4797_1_PD_variation",
            "status": smoke_pd["runner_status"],
            "detail": f"delta_average={smoke_pd['delta_average']}; delta_PD_sample={smoke_pd['delta_PD_sample']}",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "status_id": "STATUS4797_2_selected_next",
            "status": "LOCAL_ZERO_SOURCE_SELECTOR_AND_PHIBC_STRESS_LEDGER",
            "detail": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "next_id": "NEXT4797_0_4798",
            "next_target": NEXT_TARGET,
            "objective": "derive the same-law selector for local Sigma_C/Phi_C/domain-motion zero and FLRW top-class activity, while tying Phi_C to B_C and stress ledger terms",
            "include": "local no-source theorem; local no-flux theorem; FLRW top-class source; Phi_C-B_C relation; domain-boundary stress; projector stress; Ward/Bianchi ledger",
            "exclude": "multiplier closure as proof; balance as silence; external P_D; hidden boundary stress; local-GR claim; GitHub",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
    ]


def validation_rows(timestamp: str) -> list[dict[str, Any]]:
    sources = parse_csv(SOURCE_REGISTER_CSV)
    cartan_rows = parse_csv(CARTAN_OUTPUT_CSV)
    pd_rows = parse_csv(PD_OUTPUT_CSV)
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

    physical_cartan = next(row for row in cartan_rows if row["balance_id"] == "physical_parent_source_missing")
    smoke_cartan = next(row for row in cartan_rows if row["balance_id"] == "cartan_reynolds_balance_smoke")
    conditional_cartan = next(row for row in cartan_rows if row["balance_id"] == "conditional_local_no_flux_lock")
    forbidden_cartan = next(row for row in cartan_rows if row["balance_id"] == "forbidden_multiplier_closure_control")
    physical_pd = next(row for row in pd_rows if row["pd_id"] == "physical_PD_domain_functional_missing")
    smoke_pd = next(row for row in pd_rows if row["pd_id"] == "PD_average_variation_identity_smoke")
    conditional_pd = next(row for row in pd_rows if row["pd_id"] == "conditional_PD_domain_functional")
    forbidden_pd = next(row for row in pd_rows if row["pd_id"] == "forbidden_external_projector_control")

    add("VAL4797_0_sources", "all cited sources exist and needles are found", all(bool_text(row["exists"]) and bool_text(row["needle_found"]) for row in sources), str(SOURCE_REGISTER_CSV))
    add("VAL4797_1_physical_cartan_blocks", "physical parent source selector remains blocked", physical_cartan["runner_status"] == "BLOCKED_MISSING_CARTAN_BALANCE_OR_PARENT_SOURCE_INPUTS", str(CARTAN_OUTPUT_CSV))
    add("VAL4797_2_cartan_identity_computes", "Cartan/Reynolds balance computes and matches finite terms", smoke_cartan["runner_status"] == "CARTAN_BALANCE_MATCHES_BUT_NOT_LOCAL_SILENCE_NONCLAIM" and smoke_cartan["cartan_balance_error_abs"] == "0.000000000000000e+00", str(CARTAN_OUTPUT_CSV))
    add("VAL4797_3_cartan_conditional_zero", "conditional no-source/no-flux theorem zeros local lock", conditional_cartan["runner_status"] == "CARTAN_PARENT_NO_FLUX_VOLUME_LOCK_CONDITIONAL_THEOREM_NONCLAIM", str(CARTAN_OUTPUT_CSV))
    add("VAL4797_4_forbidden_cartan_fails", "multiplier/hand-switch shortcut fails", forbidden_cartan["runner_status"] == "FAILED_CARTAN_BALANCE_GATE", str(CARTAN_OUTPUT_CSV))
    add("VAL4797_5_physical_PD_blocks", "physical P_D domain functional remains blocked", physical_pd["runner_status"] == "BLOCKED_MISSING_PD_DOMAIN_FUNCTIONAL_INPUTS", str(PD_OUTPUT_CSV))
    add("VAL4797_6_PD_variation_computes", "P_D average variation identity computes", smoke_pd["runner_status"] == "PD_AVERAGE_VARIATION_IDENTITY_COMPUTED_PARENT_STRESS_OPEN_NONCLAIM" and smoke_pd["delta_PD_sample"] != "MISSING_NUMERIC_VALUE", str(PD_OUTPUT_CSV))
    add("VAL4797_7_PD_conditional", "conditional P_D domain functional passes as nonclaim", conditional_pd["runner_status"] == "PD_DOMAIN_FUNCTIONAL_CONDITIONAL_THEOREM_NONCLAIM", str(PD_OUTPUT_CSV))
    add("VAL4797_8_forbidden_PD_fails", "external/frozen P_D shortcut fails", forbidden_pd["runner_status"] == "FAILED_PD_DOMAIN_FUNCTIONAL_GATE", str(PD_OUTPUT_CSV))
    add("VAL4797_9_claim", "claim register includes L-639 as nonclaim", CLAIM_ID in read_text(CLAIMS_PATH), str(CLAIMS_PATH))
    add("VAL4797_10_resume", "resume points at 4798", NEXT_TARGET in read_text(RESUME_PATH), str(RESUME_PATH))
    add("VAL4797_OVERALL", "all 4797 Cartan/P_D checks pass", all(row["result"] == "PASS" for row in validation), DECISION)
    return validation


def write_claim(timestamp: str) -> None:
    if CLAIMS_PATH.exists() and any(row.get("claim_id") == CLAIM_ID for row in parse_csv(CLAIMS_PATH)):
        return
    with CLAIMS_PATH.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = reader.fieldnames or []
    row = {
        "claim_id": CLAIM_ID,
        "domain": "cartan_balance_pd_domain_functional_runner",
        "claim": "4797 derives the Cartan/Reynolds balance identity for mathcalJ_C transport and derives the P_D domain-average variation law as nonclaim infrastructure.",
        "current_evidence": "Generated source register, Cartan input/output, P_D input/output, obstruction update, gates, firewalls, decision, status, next target and validation.",
        "status": "cartan_balance_and_PD_variation_derived_parent_source_selector_open_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "Do not treat balance identity as local silence or P_D identity as parent ownership without source/stress selector.",
        "sector": "local_gr",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "multiplier closure; balance as silence; external projector; hidden boundary/projector stress; local-GR promotion",
        "title": "Cartan balance and P_D domain functional",
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

4797 derives the kinematic part of the local-volume bridge. For a transported local domain, Cartan/Reynolds gives `d/ds int_D J_C = int_D i_tau d mathcalJ_C + int_partialD i_tau mathcalJ_C + domain/normalization terms`. With `d mathcalJ_C = Sigma_C`, this identifies `Sigma_C` as the source/top-class part and `Phi_C = i_tau mathcalJ_C` as the boundary flux. This is a real derivation, but local silence still requires a parent same-law selector proving local `Sigma_C=0`, `Phi_C=0`, zero domain-motion contribution and stress-safe preservation of the FLRW top class.

4797 also turns `P_D` from a label into a variational domain-average functional:

`delta <f>_D = <delta f>_D + <f delta ln(W_D mu)>_D - <f>_D <delta ln(W_D mu)>_D`.

That exposes the hidden projector/domain stress terms. The physical branch still needs parent ownership of `W_D`, boundary motion, `d_rel` commutator and local/FLRW domain-class selector.

## Firewalls

- No multiplier continuity as proof.
- No Cartan balance with nonzero source/flux as local silence.
- No external or frozen `P_D`.
- No dropping projector/domain/boundary stress from the Ward ledger.
- No local-GR/Newton/PPN/R10 claim from this checkpoint.
"""
    write_text(RESUME_PATH, content)


def write_docs(timestamp: str) -> None:
    sources = parse_csv(SOURCE_REGISTER_CSV)
    cartan_rows = parse_csv(CARTAN_OUTPUT_CSV)
    pd_rows = parse_csv(PD_OUTPUT_CSV)
    obstruction = parse_csv(OBSTRUCTION_CSV)
    gates = parse_csv(GATE_CSV)
    firewall_rows = parse_csv(FIREWALL_CSV)
    decisions = parse_csv(DECISION_CSV)
    statuses = parse_csv(STATUS_CSV)
    validation = parse_csv(VALIDATION_CSV)

    content = f"""# 4797 - Parent continuity source SigmaPhi or P_D domain functional

Marker: `{MARKER}`
Generated: `{timestamp}`
Decision: `{DECISION}`

## Result

4797 separates theorem from dynamics.

The kinematic identity is now explicit:

```text
d/ds integral_{{D_s}} J_C
  = integral_D i_tau d mathcalJ_C
  + integral_partialD i_tau mathcalJ_C
  + domain_motion + normalization

d mathcalJ_C = Sigma_C
Phi_C = i_tau mathcalJ_C | partialD
```

So `Sigma_C` and `Phi_C` are not arbitrary knobs. They are the source/top-class part and transported boundary-flux part of `mathcalJ_C`. This gives the correct mathematical bridge, but not the physical local-zero theorem.

The `P_D` route is also sharpened:

```text
<f>_D = N_D^-1 integral W_D f mu
delta <f>_D = <delta f>_D + <f delta ln(W_D mu)>_D
               - <f>_D <delta ln(W_D mu)>_D
delta P_D f = delta f - delta <f>_D
```

That is the exact term that must enter the stress/Ward ledger if `P_D` is real rather than a postfit average.

## Source Register

{markdown_table(sources, ["source_id", "source_path", "exists", "needle_found", "role"])}

## Cartan Balance Output

{markdown_table(cartan_rows, ["balance_id", "Z_cartan_identity", "Z_parent_source", "Z_local_lock", "Z_FLRW_compatible", "predicted_delta_JC", "cartan_balance_error_abs", "local_lock_abs", "runner_status", "missing_cartan_inputs", "anti_circularity_status"])}

## P_D Domain Functional Output

{markdown_table(pd_rows, ["pd_id", "Z_PD_average_identity", "Z_PD_parent_functional", "delta_average", "delta_PD_sample", "runner_status", "missing_PD_inputs", "anti_circularity_status"])}

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
    write_text(FORMAL_PATH, content.replace("# 4797 -", "# 813 - PPC4161 "))

    append_once(
        SPINE_PATH,
        MARKER,
        f"""
## {MARKER}

- 4797 derives the Cartan/Reynolds balance identity for transported `J_C`: `Sigma_C` is the source/top-class component of `d mathcalJ_C`, and `Phi_C` is the boundary flux `i_tau mathcalJ_C`.
- It also derives the `P_D` domain-average variation law, exposing the measure/domain/projector stress terms that must enter the Ward ledger.
- The local-GR bridge still needs the parent selector proving local source/flux/domain-motion zero while preserving FLRW top-class activity.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## {PACKET_MARKER}

4797 adds the Cartan/Reynolds transport identity and the `P_D` domain-average variation identity to the private local packet. This is derivation progress: the next problem is no longer the identity, but the parent source selector and stress ledger. Next target: `{NEXT_TARGET}`.
""",
    )


def main() -> int:
    timestamp = now()
    write_csv(SOURCE_REGISTER_CSV, source_register(timestamp))
    write_csv(CARTAN_INPUT_CSV, cartan_input_rows(timestamp))
    write_csv(PD_INPUT_CSV, pd_input_rows(timestamp))
    run_command([sys.executable, str(RUNNER), str(CARTAN_INPUT_CSV), str(CARTAN_OUTPUT_CSV), str(PD_INPUT_CSV), str(PD_OUTPUT_CSV)])

    cartan_rows = parse_csv(CARTAN_OUTPUT_CSV)
    pd_rows = parse_csv(PD_OUTPUT_CSV)
    write_csv(OBSTRUCTION_CSV, obstruction_rows(timestamp, cartan_rows, pd_rows))
    write_csv(GATE_CSV, gate_rows(timestamp, cartan_rows, pd_rows))
    write_csv(FIREWALL_CSV, firewalls(timestamp))
    write_csv(DECISION_CSV, decision_rows(timestamp))
    write_csv(STATUS_CSV, status_rows(timestamp, cartan_rows, pd_rows))
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
