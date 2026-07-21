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

CHECKPOINT = "4799"
CLAIM_ID = "L-641"
MARKER = "PPC4161_BC_PRIMITIVE_OWNER_OR_SOURCE_SELECTOR_PARENT_ACTION_4799"
PACKET_MARKER = "PPC4161_PACKET_BC_PRIMITIVE_OWNER_OR_SOURCE_SELECTOR_PARENT_ACTION_4799"
DECISION = "BC_PRIMITIVE_AND_SOURCE_SELECTOR_PARENT_ACTION_GATE_INSTALLED_LOCAL_RESIDUAL_ROLLUP_NONCLAIM"
NEXT_TARGET = "4800-Y5-R2FR-local-residual-bound-to-PPN-R10-clock-or-parent-BC-action-source-rows.md"

DOC_PATH = POST / "4799-Y5-R2FR-BC-primitive-owner-or-source-selector-parent-action.md"
FORMAL_PATH = FORMAL / "815-PPC4161-BC-primitive-owner-or-source-selector-parent-action.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"

RUNNER = SCRIPT_DIR / "BC_primitive_source_selector_parent_action_runner.py"

SOURCE_REGISTER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4799_SOURCE_REGISTER.csv"
BC_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4799_BC_PRIMITIVE_INPUT.csv"
BC_OUTPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4799_BC_PRIMITIVE_OUTPUT.csv"
SOURCE_ACTION_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4799_SOURCE_ACTION_INPUT.csv"
SOURCE_ACTION_OUTPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4799_SOURCE_ACTION_OUTPUT.csv"
ROLLUP_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4799_LOCAL_RESIDUAL_ROLLUP_INPUT.csv"
ROLLUP_OUTPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4799_LOCAL_RESIDUAL_ROLLUP_OUTPUT.csv"
OBSTRUCTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4799_OBSTRUCTION_UPDATE.csv"
GATE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4799_PROMOTION_GATES.csv"
FIREWALL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4799_FIREWALL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4799_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4799_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4799_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4799_VALIDATION.csv"

BC_PRIMITIVE_CLAUSES = (
    "parent_boundary_variation_signed",
    "ThetaC_boundary_potential_signed",
    "BC_from_boundary_momentum_signed",
    "PhiC_exact_sector_transport_relation_signed",
    "boundary_counterterm_owned_signed",
    "boundary_class_fixed_signed",
    "harmonic_projection_zero_or_bound_signed",
    "residual_projection_zero_or_bound_signed",
    "closed_weight_or_kernel_bound_signed",
    "charge_preservation_signed",
    "Ward_boundary_stress_signed",
    "no_BC_by_declaration_signed",
    "no_edge_cancellation_signed",
)

SOURCE_ACTION_CLAUSES = (
    "parent_action_source_term_signed",
    "Noether_generator_liftedC_signed",
    "source_equals_Pitop_JC_signed",
    "same_operator_local_FLRW_signed",
    "local_absolute_H3_zero_signed",
    "relative_boundary_silence_or_bound_signed",
    "FLRW_top_class_amplitude_signed",
    "Ward_source_stress_signed",
    "no_source_by_declaration_signed",
    "no_local_FLRW_hand_switch_signed",
)

ROLLUP_CLAUSES = (
    "selector_bound_sourced_signed",
    "PhiBC_bound_sourced_signed",
    "stress_gap_bound_sourced_signed",
    "common_units_signed",
    "no_double_count_signed",
    "arena_projection_signed",
    "test_mapping_signed",
    "no_cancellation_signed",
)

SOURCE_SPECS = [
    ("SRC4799_00_4798_doc", DOC_PATH.parent / "4798-Y5-R2FR-local-zero-source-selector-and-PhiBC-stress-ledger.md", "DEC4798_1_PhiBC", "4798 selects PhiBC as the next hard boundary object"),
    ("SRC4799_01_4798_topo", SOURCE_DIR / "P8_Y5_R2FR_4798_TOPO_SELECTOR_OUTPUT.csv", "topology_kills_absolute_local_H3_but_boundary_leaks", "current local topological leak row"),
    ("SRC4799_02_4798_PhiBC", SOURCE_DIR / "P8_Y5_R2FR_4798_PHIBC_OUTPUT.csv", "PhiBC_finite_bound_from_edge_smoke", "current PhiBC finite boundary bound"),
    ("SRC4799_03_4798_stress", SOURCE_DIR / "P8_Y5_R2FR_4798_STRESS_LEDGER_OUTPUT.csv", "stress_ledger_finite_gap_smoke", "current finite stress gap"),
    ("SRC4799_04_1170_doc", POST / "1170-Y5-R10-topological-selector-boundary-flux-certificate-or-BC-primitive-owner.md", "PBC1170_0_exact_sector_match", "older exact-sector Phi/B_C relation"),
    ("SRC4799_05_1020_doc", POST / "1020-Y5-R10-boundary-cohomology-domain-certificate-or-source-pack-first-row.md", "ETB1020_3_residual_bound", "weighted-Stokes finite-bound guard"),
    ("SRC4799_06_274_decomp", POST / "274-lifted-C-sector-form-holonomy-route.md", "J_C = dB_C + J_C^{top}", "J_C exact/top decomposition"),
    ("SRC4799_07_207_bianchi", POST / "207-domain-projector-action-and-Bianchi-identity.md", "T_total =", "Ward/Bianchi stress guard"),
    ("SRC4799_08_runner", RUNNER, "def bc_primitive_row", "4799 executable runner"),
]


RUNNER_TEXT = r'''from __future__ import annotations

import csv
import math
import sys
from pathlib import Path
from typing import Any


BC_PRIMITIVE_CLAUSES = (
    "parent_boundary_variation_signed",
    "ThetaC_boundary_potential_signed",
    "BC_from_boundary_momentum_signed",
    "PhiC_exact_sector_transport_relation_signed",
    "boundary_counterterm_owned_signed",
    "boundary_class_fixed_signed",
    "harmonic_projection_zero_or_bound_signed",
    "residual_projection_zero_or_bound_signed",
    "closed_weight_or_kernel_bound_signed",
    "charge_preservation_signed",
    "Ward_boundary_stress_signed",
    "no_BC_by_declaration_signed",
    "no_edge_cancellation_signed",
)

SOURCE_ACTION_CLAUSES = (
    "parent_action_source_term_signed",
    "Noether_generator_liftedC_signed",
    "source_equals_Pitop_JC_signed",
    "same_operator_local_FLRW_signed",
    "local_absolute_H3_zero_signed",
    "relative_boundary_silence_or_bound_signed",
    "FLRW_top_class_amplitude_signed",
    "Ward_source_stress_signed",
    "no_source_by_declaration_signed",
    "no_local_FLRW_hand_switch_signed",
)

ROLLUP_CLAUSES = (
    "selector_bound_sourced_signed",
    "PhiBC_bound_sourced_signed",
    "stress_gap_bound_sourced_signed",
    "common_units_signed",
    "no_double_count_signed",
    "arena_projection_signed",
    "test_mapping_signed",
    "no_cancellation_signed",
)

FORBIDDEN_SOURCE_TOKENS = (
    "HAND_SWITCH",
    "LOCAL_FLRW_HAND_SWITCH",
    "SIGMA_ZERO_BY_ASSERTION",
    "PHI_ZERO_BY_ASSERTION",
    "BOUNDARY_ZERO_BY_ASSERTION",
    "BC_PRIMITIVE_BY_DECLARATION",
    "SOURCE_BY_DECLARATION",
    "EDGE_CANCELLATION",
    "DROP_PROJECTOR_STRESS",
    "DROP_BOUNDARY_STRESS",
    "EXTERNAL_PROJECTOR",
    "POSTFIT_REFERENCE",
    "OBSERVED_RESIDUAL_CANCEL",
    "R10_BOUND_AS_SOURCE",
)


def bool_text(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "y", "pass", "signed"}


def missing_text(value: Any) -> bool:
    text = str(value or "").strip()
    return not text or text.upper().startswith("MISSING") or text.upper() in {"NA", "N/A", "NONE", "NOT_COMPUTED"}


def parse_float(value: Any) -> float | None:
    if missing_text(value):
        return None
    try:
        number = float(str(value).strip())
    except ValueError:
        return None
    return number if math.isfinite(number) else None


def format_float(value: float | None) -> str:
    if value is None or not math.isfinite(value):
        return "MISSING_NUMERIC_VALUE"
    return f"{value:.15e}"


def forbidden_source_used(row: dict[str, Any]) -> bool:
    source_text = " ".join(
        str(row.get(field, ""))
        for field in (
            "source_path",
            "BC_source",
            "Phi_source",
            "boundary_source",
            "source_action_path",
            "selector_source",
            "stress_source",
            "rollup_source",
            "provenance",
            "notes",
        )
    ).upper()
    return any(token in source_text for token in FORBIDDEN_SOURCE_TOKENS)


def missing_clauses(row: dict[str, Any], clauses: tuple[str, ...]) -> list[str]:
    return [clause for clause in clauses if not bool_text(row.get(clause))]


def numeric_missing(row: dict[str, Any], fields: tuple[str, ...]) -> tuple[dict[str, float], list[str]]:
    values: dict[str, float] = {}
    missing: list[str] = []
    for field in fields:
        value = parse_float(row.get(field))
        if value is None or value < 0.0:
            missing.append(field)
        else:
            values[field] = value
    return values, missing


def bc_primitive_row(row: dict[str, Any]) -> dict[str, Any]:
    bc_id = str(row.get("bc_id", "")).strip() or "UNNAMED_BC_PRIMITIVE"
    output: dict[str, Any] = {
        "bc_id": bc_id,
        "row_status_input": row.get("row_status", ""),
        "input_valid_for_claim": bool_text(row.get("valid_for_claim")),
        "valid_for_claim": False,
        "claim_allowed": False,
    }
    if forbidden_source_used(row):
        output.update(
            {
                "Z_BC_primitive_owner": False,
                "Z_PhiBC_parent_silence": False,
                "BC_boundary_bound_abs": "MISSING_NUMERIC_VALUE",
                "missing_BC_inputs": "FORBIDDEN_BC_PRIMITIVE_OR_BOUNDARY_SOURCE",
                "runner_status": "FAILED_BC_PRIMITIVE_GATE",
                "anti_circularity_status": "FAIL_FORBIDDEN_SOURCE_USED",
            }
        )
        return output

    missing = missing_clauses(row, BC_PRIMITIVE_CLAUSES)
    if not missing:
        output.update(
            {
                "Z_BC_primitive_owner": True,
                "Z_PhiBC_parent_silence": True,
                "BC_boundary_bound_abs": "0.000000000000000e+00",
                "missing_BC_inputs": "",
                "runner_status": "BC_PRIMITIVE_PARENT_NO_FLUX_CONDITIONAL_THEOREM_NONCLAIM",
                "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
            }
        )
        return output

    fields = (
        "C_corner_abs",
        "norm_dS_Feps",
        "norm_bC",
        "harmonic_edge_abs",
        "residual_edge_abs",
        "transport_tail_abs",
        "boundary_counterterm_tail_abs",
    )
    values, missing_numbers = numeric_missing(row, fields)
    if not missing_numbers:
        bound = (
            values["C_corner_abs"]
            + values["norm_dS_Feps"] * values["norm_bC"]
            + values["harmonic_edge_abs"]
            + values["residual_edge_abs"]
            + values["transport_tail_abs"]
            + values["boundary_counterterm_tail_abs"]
        )
        relation_ok = (
            bool_text(row.get("PhiC_exact_sector_transport_relation_signed"))
            and bool_text(row.get("no_BC_by_declaration_signed"))
            and bool_text(row.get("no_edge_cancellation_signed"))
        )
        status = "BC_PRIMITIVE_FINITE_BOUND_COMPUTED_PARENT_UNSIGNED_NONCLAIM"
        if bound <= 1.0e-15:
            status = "BC_PRIMITIVE_NUMERIC_ZERO_PARENT_UNSIGNED_NONCLAIM"
        output.update(
            {
                "Z_BC_primitive_owner": False,
                "Z_PhiBC_parent_silence": bound <= 1.0e-15 and not missing,
                "Z_PhiBC_relation": relation_ok,
                "BC_boundary_bound_abs": format_float(bound),
                "missing_BC_inputs": ";".join(f"MISSING_{clause}" for clause in missing),
                "runner_status": status,
                "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
            }
        )
        return output

    output.update(
        {
            "Z_BC_primitive_owner": False,
            "Z_PhiBC_parent_silence": False,
            "Z_PhiBC_relation": bool_text(row.get("PhiC_exact_sector_transport_relation_signed")),
            "BC_boundary_bound_abs": "MISSING_NUMERIC_VALUE",
            "missing_BC_inputs": ";".join([*(f"MISSING_{clause}" for clause in missing), *(f"MISSING_{field}" for field in missing_numbers)]),
            "runner_status": "BLOCKED_MISSING_BC_PRIMITIVE_INPUTS",
            "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
        }
    )
    return output


def source_action_row(row: dict[str, Any]) -> dict[str, Any]:
    source_id = str(row.get("source_action_id", "")).strip() or "UNNAMED_SOURCE_ACTION"
    output: dict[str, Any] = {
        "source_action_id": source_id,
        "row_status_input": row.get("row_status", ""),
        "input_valid_for_claim": bool_text(row.get("valid_for_claim")),
        "valid_for_claim": False,
        "claim_allowed": False,
    }
    if forbidden_source_used(row):
        output.update(
            {
                "Z_source_action_owner": False,
                "Z_same_selector_local_FLRW": False,
                "local_source_abs": "MISSING_NUMERIC_VALUE",
                "local_source_boundary_abs": "MISSING_NUMERIC_VALUE",
                "FLRW_source_allowed": False,
                "missing_source_action_inputs": "FORBIDDEN_SOURCE_SELECTOR_OR_HAND_SWITCH_SOURCE",
                "runner_status": "FAILED_SOURCE_ACTION_GATE",
                "anti_circularity_status": "FAIL_FORBIDDEN_SOURCE_USED",
            }
        )
        return output

    missing = missing_clauses(row, SOURCE_ACTION_CLAUSES)
    if not missing:
        output.update(
            {
                "Z_source_action_owner": True,
                "Z_same_selector_local_FLRW": True,
                "local_source_abs": "0.000000000000000e+00",
                "local_source_boundary_abs": "0.000000000000000e+00",
                "FLRW_source_allowed": True,
                "missing_source_action_inputs": "",
                "runner_status": "SOURCE_SELECTOR_PARENT_ACTION_CONDITIONAL_THEOREM_NONCLAIM",
                "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
            }
        )
        return output

    fields = (
        "kappa_top_abs",
        "local_H3_abs",
        "relative_boundary_abs",
        "FLRW_top_abs",
        "normalization_abs",
    )
    values, missing_numbers = numeric_missing(row, fields)
    if not missing_numbers:
        local_top = values["kappa_top_abs"] * values["local_H3_abs"] * values["normalization_abs"]
        local_total = local_top + values["relative_boundary_abs"]
        flrw_allowed = bool_text(row.get("same_operator_local_FLRW_signed")) and values["FLRW_top_abs"] > 0.0
        status = "SOURCE_SELECTOR_LOCAL_TOP_ZERO_BOUNDARY_OPEN_PARENT_UNSIGNED_NONCLAIM"
        if local_total <= 1.0e-15:
            status = "SOURCE_SELECTOR_NUMERIC_LOCAL_ZERO_PARENT_UNSIGNED_NONCLAIM"
        output.update(
            {
                "Z_source_action_owner": False,
                "Z_same_selector_local_FLRW": bool_text(row.get("same_operator_local_FLRW_signed")),
                "local_source_abs": format_float(local_top),
                "local_source_boundary_abs": format_float(local_total),
                "FLRW_source_allowed": flrw_allowed,
                "missing_source_action_inputs": ";".join(f"MISSING_{clause}" for clause in missing),
                "runner_status": status,
                "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
            }
        )
        return output

    output.update(
        {
            "Z_source_action_owner": False,
            "Z_same_selector_local_FLRW": bool_text(row.get("same_operator_local_FLRW_signed")),
            "local_source_abs": "MISSING_NUMERIC_VALUE",
            "local_source_boundary_abs": "MISSING_NUMERIC_VALUE",
            "FLRW_source_allowed": bool_text(row.get("same_operator_local_FLRW_signed")),
            "missing_source_action_inputs": ";".join([*(f"MISSING_{clause}" for clause in missing), *(f"MISSING_{field}" for field in missing_numbers)]),
            "runner_status": "BLOCKED_MISSING_SOURCE_ACTION_INPUTS",
            "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
        }
    )
    return output


def residual_rollup_row(row: dict[str, Any]) -> dict[str, Any]:
    rollup_id = str(row.get("rollup_id", "")).strip() or "UNNAMED_LOCAL_ROLLUP"
    output: dict[str, Any] = {
        "rollup_id": rollup_id,
        "row_status_input": row.get("row_status", ""),
        "input_valid_for_claim": bool_text(row.get("valid_for_claim")),
        "valid_for_claim": False,
        "claim_allowed": False,
    }
    if forbidden_source_used(row):
        output.update(
            {
                "Z_local_residual_sourced": False,
                "Z_local_zero_bound": False,
                "local_residual_bound_abs": "MISSING_NUMERIC_VALUE",
                "missing_rollup_inputs": "FORBIDDEN_ROLLUP_OR_CANCELLATION_SOURCE",
                "runner_status": "FAILED_LOCAL_RESIDUAL_ROLLUP_GATE",
                "anti_circularity_status": "FAIL_FORBIDDEN_SOURCE_USED",
            }
        )
        return output

    missing = missing_clauses(row, ROLLUP_CLAUSES)
    fields = (
        "selector_leak_abs",
        "Phi_boundary_bound_abs",
        "stress_gap_abs",
        "other_projector_tail_abs",
    )
    values, missing_numbers = numeric_missing(row, fields)
    if not missing_numbers:
        total = (
            values["selector_leak_abs"]
            + values["Phi_boundary_bound_abs"]
            + values["stress_gap_abs"]
            + values["other_projector_tail_abs"]
        )
        status = "LOCAL_RESIDUAL_ROLLUP_FINITE_BOUND_COMPUTED_NONCLAIM"
        if total <= 1.0e-15:
            status = "LOCAL_RESIDUAL_ROLLUP_ZERO_CONDITIONAL_THEOREM_NONCLAIM"
        output.update(
            {
                "Z_local_residual_sourced": not missing,
                "Z_local_zero_bound": total <= 1.0e-15 and not missing,
                "selector_leak_abs": format_float(values["selector_leak_abs"]),
                "Phi_boundary_bound_abs": format_float(values["Phi_boundary_bound_abs"]),
                "stress_gap_abs": format_float(values["stress_gap_abs"]),
                "other_projector_tail_abs": format_float(values["other_projector_tail_abs"]),
                "local_residual_bound_abs": format_float(total),
                "missing_rollup_inputs": ";".join(f"MISSING_{clause}" for clause in missing),
                "runner_status": status,
                "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
            }
        )
        return output

    output.update(
        {
            "Z_local_residual_sourced": False,
            "Z_local_zero_bound": False,
            "local_residual_bound_abs": "MISSING_NUMERIC_VALUE",
            "missing_rollup_inputs": ";".join([*(f"MISSING_{clause}" for clause in missing), *(f"MISSING_{field}" for field in missing_numbers)]),
            "runner_status": "BLOCKED_MISSING_LOCAL_RESIDUAL_ROLLUP_INPUTS",
            "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
        }
    )
    return output


def read_csv(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"cannot write empty CSV: {path}")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def run(kind: str, input_path: Path, output_path: Path) -> None:
    functions = {
        "bc": bc_primitive_row,
        "source": source_action_row,
        "rollup": residual_rollup_row,
    }
    if kind not in functions:
        raise ValueError(f"unknown runner kind: {kind}")
    rows = [functions[kind](row) for row in read_csv(input_path)]
    write_csv(output_path, rows)


def main() -> int:
    if len(sys.argv) != 4:
        print("usage: BC_primitive_source_selector_parent_action_runner.py <bc|source|rollup> <input.csv> <output.csv>", file=sys.stderr)
        return 2
    run(sys.argv[1], Path(sys.argv[2]), Path(sys.argv[3]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
'''


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


def parse_csv(path_object: Path) -> list[dict[str, str]]:
    with path_object.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


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
    return str(value).strip().lower() in {"true", "1", "yes", "y", "pass", "signed"}


def run_command(args: list[str]) -> None:
    subprocess.run(args, check=True, cwd=str(ROOT))


def clause_map(clauses: tuple[str, ...], value: bool) -> dict[str, bool]:
    return {clause: value for clause in clauses}


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


def bc_input_rows(timestamp: str) -> list[dict[str, Any]]:
    physical = clause_map(BC_PRIMITIVE_CLAUSES, False)
    physical["no_BC_by_declaration_signed"] = True
    physical["no_edge_cancellation_signed"] = True

    finite = clause_map(BC_PRIMITIVE_CLAUSES, False)
    for clause in (
        "PhiC_exact_sector_transport_relation_signed",
        "harmonic_projection_zero_or_bound_signed",
        "residual_projection_zero_or_bound_signed",
        "closed_weight_or_kernel_bound_signed",
        "no_BC_by_declaration_signed",
        "no_edge_cancellation_signed",
    ):
        finite[clause] = True

    signed = clause_map(BC_PRIMITIVE_CLAUSES, True)

    def row(bc_id: str, status: str, source: str, clauses: dict[str, bool], values: dict[str, Any] | None = None) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "bc_id": bc_id,
            "BC_source": source,
            "Phi_source": source,
            "boundary_source": source,
            "provenance": source,
            "notes": "",
            "C_corner_abs": "",
            "norm_dS_Feps": "",
            "norm_bC": "",
            "harmonic_edge_abs": "",
            "residual_edge_abs": "",
            "transport_tail_abs": "",
            "boundary_counterterm_tail_abs": "",
            "row_status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        payload.update(clauses)
        if values:
            payload.update(values)
        return payload

    return [
        row(
            "physical_BC_primitive_missing",
            "BLOCKED_PARENT_BC_ACTION_INPUTS_MISSING",
            "4799_physical_branch_missing_parent_LC_ThetaC_BC_counterterm",
            physical,
        ),
        row(
            "BC_primitive_finite_bound_from_4798_smoke",
            "FINITE_BOUND_SMOKE_PARENT_UNSIGNED",
            "SRC4799_02_4798_PhiBC_plus_SRC4799_05_1020_weighted_Stokes",
            finite,
            {
                "C_corner_abs": "1.0e-8",
                "norm_dS_Feps": "4.0e-3",
                "norm_bC": "2.0e-5",
                "harmonic_edge_abs": "2.0e-8",
                "residual_edge_abs": "4.0e-8",
                "transport_tail_abs": "2.0e-8",
                "boundary_counterterm_tail_abs": "0.0",
                "notes": "termwise reproduction of the 4798 PhiBC finite-bound scale; not a parent no-flux theorem",
            },
        ),
        row(
            "conditional_BC_parent_no_flux",
            "CONDITIONAL_THEOREM_NONCLAIM",
            "conditional_parent_boundary_action_owns_BC_and_no_flux",
            signed,
            {
                "C_corner_abs": "0.0",
                "norm_dS_Feps": "0.0",
                "norm_bC": "0.0",
                "harmonic_edge_abs": "0.0",
                "residual_edge_abs": "0.0",
                "transport_tail_abs": "0.0",
                "boundary_counterterm_tail_abs": "0.0",
                "notes": "only valid if a future parent action derives the natural BC primitive and Ward stress",
            },
        ),
        row(
            "forbidden_BC_zero_assertion_control",
            "FORBIDDEN_CONTROL",
            "BOUNDARY_ZERO_BY_ASSERTION;BC_PRIMITIVE_BY_DECLARATION",
            physical,
        ),
    ]


def source_action_input_rows(timestamp: str) -> list[dict[str, Any]]:
    physical = clause_map(SOURCE_ACTION_CLAUSES, False)
    physical["no_source_by_declaration_signed"] = True
    physical["no_local_FLRW_hand_switch_signed"] = True

    candidate = clause_map(SOURCE_ACTION_CLAUSES, False)
    for clause in (
        "same_operator_local_FLRW_signed",
        "local_absolute_H3_zero_signed",
        "relative_boundary_silence_or_bound_signed",
        "no_source_by_declaration_signed",
        "no_local_FLRW_hand_switch_signed",
    ):
        candidate[clause] = True

    signed = clause_map(SOURCE_ACTION_CLAUSES, True)

    def row(source_action_id: str, status: str, source: str, clauses: dict[str, bool], values: dict[str, Any] | None = None) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "source_action_id": source_action_id,
            "source_action_path": source,
            "selector_source": source,
            "stress_source": source,
            "provenance": source,
            "notes": "",
            "kappa_top_abs": "",
            "local_H3_abs": "",
            "relative_boundary_abs": "",
            "FLRW_top_abs": "",
            "normalization_abs": "",
            "row_status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        payload.update(clauses)
        if values:
            payload.update(values)
        return payload

    return [
        row(
            "physical_source_action_missing",
            "BLOCKED_PARENT_SOURCE_ACTION_INPUTS_MISSING",
            "4799_physical_branch_missing_parent_action_source_term_Noether_generator_Ward_stress",
            physical,
        ),
        row(
            "top_selector_parent_action_candidate",
            "LOCAL_TOP_ZERO_BOUNDARY_OPEN_PARENT_UNSIGNED",
            "SRC4799_01_4798_topo_plus_SRC4799_04_1170_exact_sector",
            candidate,
            {
                "kappa_top_abs": "1.0",
                "local_H3_abs": "0.0",
                "relative_boundary_abs": "1.66e-7",
                "FLRW_top_abs": "1.0",
                "normalization_abs": "1.0",
                "notes": "same operator can keep FLRW top active while local absolute H3 vanishes; parent action/source owner still missing",
            },
        ),
        row(
            "conditional_source_selector_parent_action",
            "CONDITIONAL_THEOREM_NONCLAIM",
            "conditional_parent_action_source_equals_Pitop_JC_same_operator",
            signed,
            {
                "kappa_top_abs": "1.0",
                "local_H3_abs": "0.0",
                "relative_boundary_abs": "0.0",
                "FLRW_top_abs": "1.0",
                "normalization_abs": "1.0",
            },
        ),
        row(
            "forbidden_local_FLRW_hand_switch_control",
            "FORBIDDEN_CONTROL",
            "LOCAL_FLRW_HAND_SWITCH;SOURCE_BY_DECLARATION",
            physical,
        ),
    ]


def rollup_input_rows(timestamp: str) -> list[dict[str, Any]]:
    physical = clause_map(ROLLUP_CLAUSES, False)
    physical["no_cancellation_signed"] = True

    finite = clause_map(ROLLUP_CLAUSES, False)
    for clause in (
        "selector_bound_sourced_signed",
        "PhiBC_bound_sourced_signed",
        "stress_gap_bound_sourced_signed",
        "common_units_signed",
        "no_double_count_signed",
        "no_cancellation_signed",
    ):
        finite[clause] = True

    signed = clause_map(ROLLUP_CLAUSES, True)

    def row(rollup_id: str, status: str, source: str, clauses: dict[str, bool], values: dict[str, Any] | None = None) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "rollup_id": rollup_id,
            "rollup_source": source,
            "provenance": source,
            "notes": "",
            "selector_leak_abs": "",
            "Phi_boundary_bound_abs": "",
            "stress_gap_abs": "",
            "other_projector_tail_abs": "",
            "row_status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        payload.update(clauses)
        if values:
            payload.update(values)
        return payload

    return [
        row(
            "physical_local_residual_rollup_missing",
            "BLOCKED_LOCAL_ARENA_MAPPING_MISSING",
            "4799_physical_branch_missing_arena_projection_and_test_mapping",
            physical,
        ),
        row(
            "local_residual_rollup_from_4798_smoke",
            "FINITE_BOUND_SMOKE_NO_CANCELLATION",
            "SRC4799_01_4798_topo_SRC4799_02_4798_PhiBC_SRC4799_03_4798_stress",
            finite,
            {
                "selector_leak_abs": "1.66e-7",
                "Phi_boundary_bound_abs": "1.70e-7",
                "stress_gap_abs": "1.60e-7",
                "other_projector_tail_abs": "0.0",
                "notes": "conservative same-scale rollup; no cancellation; not yet mapped to PPN/R10/clock/orbital tolerances",
            },
        ),
        row(
            "conditional_local_residual_zero",
            "CONDITIONAL_THEOREM_NONCLAIM",
            "conditional_parent_BC_source_action_and_Ward_stress_closed",
            signed,
            {
                "selector_leak_abs": "0.0",
                "Phi_boundary_bound_abs": "0.0",
                "stress_gap_abs": "0.0",
                "other_projector_tail_abs": "0.0",
            },
        ),
        row(
            "forbidden_rollup_cancellation_control",
            "FORBIDDEN_CONTROL",
            "EDGE_CANCELLATION;OBSERVED_RESIDUAL_CANCEL",
            physical,
        ),
    ]


def obstruction_rows(bc_rows: list[dict[str, str]], source_rows: list[dict[str, str]], rollup_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    finite_bc = next(row for row in bc_rows if row["bc_id"] == "BC_primitive_finite_bound_from_4798_smoke")
    source_candidate = next(row for row in source_rows if row["source_action_id"] == "top_selector_parent_action_candidate")
    finite_rollup = next(row for row in rollup_rows if row["rollup_id"] == "local_residual_rollup_from_4798_smoke")
    return [
        {
            "update_id": "OBS4799_0_BC_primitive",
            "item": "B_C primitive and Phi_C boundary flux",
            "status": finite_bc["runner_status"],
            "value_or_bound": finite_bc["BC_boundary_bound_abs"],
            "meaning": "the exact-sector boundary primitive is finite-bounded, but parent boundary variation/Theta_C/counterterm/charge-preservation are not signed",
        },
        {
            "update_id": "OBS4799_1_source_selector",
            "item": "parent source selector for Sigma_C",
            "status": source_candidate["runner_status"],
            "value_or_bound": f"local_source_abs={source_candidate['local_source_abs']}; boundary_total={source_candidate['local_source_boundary_abs']}",
            "meaning": "absolute local top class is zero while FLRW remains allowed, but parent source action and Ward stress ownership remain unsigned",
        },
        {
            "update_id": "OBS4799_2_local_rollup",
            "item": "conservative local residual bound",
            "status": finite_rollup["runner_status"],
            "value_or_bound": finite_rollup["local_residual_bound_abs"],
            "meaning": "current nonclaim residual scale is explicit and can be sent to PPN/R10/clock/orbital source rows next",
        },
    ]


def gate_rows(bc_rows: list[dict[str, str]], source_rows: list[dict[str, str]], rollup_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    physical_bc = next(row for row in bc_rows if row["bc_id"] == "physical_BC_primitive_missing")
    finite_bc = next(row for row in bc_rows if row["bc_id"] == "BC_primitive_finite_bound_from_4798_smoke")
    source_candidate = next(row for row in source_rows if row["source_action_id"] == "top_selector_parent_action_candidate")
    finite_rollup = next(row for row in rollup_rows if row["rollup_id"] == "local_residual_rollup_from_4798_smoke")
    return [
        {
            "gate_id": "PG4799_0_parent_BC_owner",
            "claim": "parent action owns B_C primitive and natural no-flux boundary condition",
            "gate_pass": bool_text(finite_bc.get("Z_BC_primitive_owner")),
            "reason": "finite bound exists, but parent boundary variation/Theta_C/counterterm/charge-preservation are unsigned",
            "evidence": physical_bc["missing_BC_inputs"],
        },
        {
            "gate_id": "PG4799_1_source_selector",
            "claim": "Sigma_C source selector is parent-action owned",
            "gate_pass": bool_text(source_candidate.get("Z_source_action_owner")),
            "reason": "same local/FLRW topological asymmetry is alive, but source term and Noether/Ward owner are missing",
            "evidence": source_candidate["missing_source_action_inputs"],
        },
        {
            "gate_id": "PG4799_2_finite_rollup",
            "claim": "all current local residual pieces are carried termwise without cancellation",
            "gate_pass": finite_rollup["runner_status"] == "LOCAL_RESIDUAL_ROLLUP_FINITE_BOUND_COMPUTED_NONCLAIM",
            "reason": "selector, PhiBC and stress finite scales are rolled up conservatively",
            "evidence": finite_rollup["local_residual_bound_abs"],
        },
        {
            "gate_id": "PG4799_3_test_promotion",
            "claim": "local-GR/PPN/R10/clock/orbital promotion allowed",
            "gate_pass": False,
            "reason": "local arena projection/test mapping is still missing and parent BC/source owner is not signed",
            "evidence": "nonclaim firewall active",
        },
    ]


def firewall_rows() -> list[dict[str, Any]]:
    return [
        {"firewall_id": "FW4799_0_no_BC_assertion", "rule": "B_C or Phi_C may not be set to zero by boundary assertion; it must follow from parent boundary variation or sourced finite bounds.", "status": "ACTIVE"},
        {"firewall_id": "FW4799_1_no_source_declaration", "rule": "Sigma_C source ownership must come from the parent action/Noether generator, not by naming Pi_top as a source.", "status": "ACTIVE"},
        {"firewall_id": "FW4799_2_no_cancellation", "rule": "Selector, PhiBC, stress and projector tails are added termwise; no observed residual cancellation is accepted.", "status": "ACTIVE"},
        {"firewall_id": "FW4799_3_no_local_claim", "rule": "No GR/Newton/PPN/R10/WEP/clock/orbital claim follows until arena projections and local tolerances are sourced.", "status": "ACTIVE"},
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC4799_0_BC_route",
            "decision": "parent_BC_action_or_finite_BC_bound_is_now_the_hinge",
            "reason": "Stokes exposes int_partialD B_C as the exact-sector obstruction after local absolute topology is killed",
            "next_action": "derive parent boundary variation Theta_C/B_C or map the finite B_C residual into local test source rows",
        },
        {
            "decision_id": "DEC4799_1_source_route",
            "decision": "source_selector_needs_parent_action_Noether_owner",
            "reason": "same local/FLRW operator is plausible but not enough without source stress and amplitude ownership",
            "next_action": "source parent action rows for Sigma_C and Ward stress or keep selector as nonclaim infrastructure",
        },
        {
            "decision_id": "DEC4799_2_next",
            "decision": "send_current_residual_bound_to_local_tests_next",
            "reason": "we now have a conservative finite residual bound instead of only a missing-input statement",
            "next_action": NEXT_TARGET,
        },
    ]


def status_rows(bc_rows: list[dict[str, str]], source_rows: list[dict[str, str]], rollup_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    finite_bc = next(row for row in bc_rows if row["bc_id"] == "BC_primitive_finite_bound_from_4798_smoke")
    source_candidate = next(row for row in source_rows if row["source_action_id"] == "top_selector_parent_action_candidate")
    finite_rollup = next(row for row in rollup_rows if row["rollup_id"] == "local_residual_rollup_from_4798_smoke")
    return [
        {"status_id": "STATUS4799_0_BC", "status": finite_bc["runner_status"], "detail": f"BC_boundary_bound_abs={finite_bc['BC_boundary_bound_abs']}"},
        {"status_id": "STATUS4799_1_source", "status": source_candidate["runner_status"], "detail": f"local_source_boundary_abs={source_candidate['local_source_boundary_abs']}"},
        {"status_id": "STATUS4799_2_rollup", "status": finite_rollup["runner_status"], "detail": f"local_residual_bound_abs={finite_rollup['local_residual_bound_abs']}"},
        {"status_id": "STATUS4799_3_selected_next", "status": "LOCAL_RESIDUAL_BOUND_TO_TEST_ROWS_OR_PARENT_BC_ACTION", "detail": NEXT_TARGET},
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT4799_0_4800",
            "next_target": NEXT_TARGET,
            "trigger": "4799 finite residual rollup exists but parent BC/source and local test mapping remain unsigned",
            "required_inputs": "PPN/R10/clock/orbital tau rows; arena projection; or parent boundary action variation Theta_C/B_C",
            "valid_for_claim": False,
        }
    ]


def validation_rows(
    sources: list[dict[str, Any]],
    bc_rows: list[dict[str, str]],
    source_rows: list[dict[str, str]],
    rollup_rows: list[dict[str, str]],
) -> list[dict[str, Any]]:
    checks: list[tuple[str, str, bool, str]] = []
    checks.append(("VAL4799_0_sources", "all cited sources exist and needles are found", all(bool_text(row["exists"]) and bool_text(row["needle_found"]) for row in sources), str(SOURCE_REGISTER_CSV)))

    bc_by_id = {row["bc_id"]: row for row in bc_rows}
    source_by_id = {row["source_action_id"]: row for row in source_rows}
    rollup_by_id = {row["rollup_id"]: row for row in rollup_rows}

    checks.append(("VAL4799_1_physical_BC_blocks", "physical B_C primitive branch remains blocked", bc_by_id["physical_BC_primitive_missing"]["runner_status"] == "BLOCKED_MISSING_BC_PRIMITIVE_INPUTS", str(BC_OUTPUT_CSV)))
    checks.append(("VAL4799_2_BC_bound", "B_C finite boundary bound computes", bc_by_id["BC_primitive_finite_bound_from_4798_smoke"]["BC_boundary_bound_abs"] == "1.700000000000000e-07", str(BC_OUTPUT_CSV)))
    checks.append(("VAL4799_3_conditional_BC", "conditional parent B_C no-flux branch passes", bc_by_id["conditional_BC_parent_no_flux"]["runner_status"] == "BC_PRIMITIVE_PARENT_NO_FLUX_CONDITIONAL_THEOREM_NONCLAIM", str(BC_OUTPUT_CSV)))
    checks.append(("VAL4799_4_forbidden_BC_fails", "B_C zero by assertion fails", bc_by_id["forbidden_BC_zero_assertion_control"]["runner_status"] == "FAILED_BC_PRIMITIVE_GATE", str(BC_OUTPUT_CSV)))

    checks.append(("VAL4799_5_physical_source_blocks", "physical source-action branch remains blocked", source_by_id["physical_source_action_missing"]["runner_status"] == "BLOCKED_MISSING_SOURCE_ACTION_INPUTS", str(SOURCE_ACTION_OUTPUT_CSV)))
    checks.append(("VAL4799_6_source_candidate", "same-law source selector candidate computes local top zero plus boundary leak", source_by_id["top_selector_parent_action_candidate"]["local_source_boundary_abs"] == "1.660000000000000e-07", str(SOURCE_ACTION_OUTPUT_CSV)))
    checks.append(("VAL4799_7_conditional_source", "conditional source-action branch passes", source_by_id["conditional_source_selector_parent_action"]["runner_status"] == "SOURCE_SELECTOR_PARENT_ACTION_CONDITIONAL_THEOREM_NONCLAIM", str(SOURCE_ACTION_OUTPUT_CSV)))
    checks.append(("VAL4799_8_forbidden_source_fails", "local/FLRW hand switch fails", source_by_id["forbidden_local_FLRW_hand_switch_control"]["runner_status"] == "FAILED_SOURCE_ACTION_GATE", str(SOURCE_ACTION_OUTPUT_CSV)))

    checks.append(("VAL4799_9_physical_rollup_blocks", "physical residual rollup remains blocked", rollup_by_id["physical_local_residual_rollup_missing"]["runner_status"] == "BLOCKED_MISSING_LOCAL_RESIDUAL_ROLLUP_INPUTS", str(ROLLUP_OUTPUT_CSV)))
    checks.append(("VAL4799_10_rollup_bound", "local residual rollup computes without cancellation", rollup_by_id["local_residual_rollup_from_4798_smoke"]["local_residual_bound_abs"] == "4.960000000000000e-07", str(ROLLUP_OUTPUT_CSV)))
    checks.append(("VAL4799_11_conditional_rollup", "conditional zero rollup passes", rollup_by_id["conditional_local_residual_zero"]["runner_status"] == "LOCAL_RESIDUAL_ROLLUP_ZERO_CONDITIONAL_THEOREM_NONCLAIM", str(ROLLUP_OUTPUT_CSV)))
    checks.append(("VAL4799_12_forbidden_rollup_fails", "rollup cancellation fails", rollup_by_id["forbidden_rollup_cancellation_control"]["runner_status"] == "FAILED_LOCAL_RESIDUAL_ROLLUP_GATE", str(ROLLUP_OUTPUT_CSV)))
    checks.append(("VAL4799_13_claim", "claim register includes L-641 as nonclaim", CLAIM_ID in read_text(CLAIMS_PATH) and MARKER in read_text(CLAIMS_PATH), str(CLAIMS_PATH)))
    checks.append(("VAL4799_14_resume", "resume points at 4800", NEXT_TARGET in read_text(RESUME_PATH), str(RESUME_PATH)))

    rows = [
        {
            "check_id": check_id,
            "description": description,
            "result": "PASS" if passed else "FAIL",
            "evidence": evidence,
        }
        for check_id, description, passed, evidence in checks
    ]
    rows.append(
        {
            "check_id": "VAL4799_OVERALL",
            "description": "all 4799 B_C/source action/residual rollup checks pass",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "evidence": DECISION,
        }
    )
    return rows


def write_documents(
    timestamp: str,
    sources: list[dict[str, Any]],
    bc_rows: list[dict[str, str]],
    source_rows: list[dict[str, str]],
    rollup_rows: list[dict[str, str]],
    obstructions: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    firewalls: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    statuses: list[dict[str, Any]],
    validations: list[dict[str, Any]],
) -> None:
    content = f"""# 4799 - BC primitive owner or source selector parent action

Marker: `{MARKER}`
Generated: `{timestamp}`
Decision: `{DECISION}`

## Result

4799 turns the live local-GR hinge into an explicit parent-action gate instead of another vague missing-input note.

The route now splits cleanly:

```text
J_C = d_D B_C + J_C^top
int_D J_C = int_partialD B_C + int_D J_C^top
```

The absolute local top term can vanish on a bounded/contractible local domain, but the exact-sector boundary primitive still remains:

```text
local residual <= |relative/top boundary leak| + |Phi_C/B_C boundary bound| + |unaccounted Ward stress|
```

The current conservative nonclaim rollup is:

```text
1.66e-7 + 1.70e-7 + 1.60e-7 = 4.96e-7
```

This is progress because it creates a measurable local-residual object. It is not a local-GR claim because parent `B_C`/`Phi_C` ownership, source-action ownership, Ward stress closure, and arena projection to PPN/R10/clock/orbital tests are still unsigned.

## Parent BC Primitive Contract

A future parent action must supply all of the following before `B_C` can be silenced:

```text
delta L_C = E_C delta C + d Theta_C
B_C = boundary momentum / primitive induced by Theta_C plus owned counterterms
Phi_C = L_tau B_C + motion_B_C + d_D zeta_C plus controlled harmonic part
pullback_partialD(Phi_C) = 0 or termwise sourced bound
```

It must also prove charge preservation: the boundary condition is allowed to kill only unphysical residual/gauge leakage, not the physical mass/time/rotation/charge generator.

## Source Register

{markdown_table(sources, ["source_id", "source_path", "exists", "needle_found", "role"])}

## BC Primitive Output

{markdown_table(bc_rows, ["bc_id", "Z_BC_primitive_owner", "Z_PhiBC_parent_silence", "BC_boundary_bound_abs", "runner_status", "missing_BC_inputs", "anti_circularity_status"])}

## Source Action Output

{markdown_table(source_rows, ["source_action_id", "Z_source_action_owner", "Z_same_selector_local_FLRW", "local_source_abs", "local_source_boundary_abs", "FLRW_source_allowed", "runner_status", "missing_source_action_inputs", "anti_circularity_status"])}

## Local Residual Rollup

{markdown_table(rollup_rows, ["rollup_id", "Z_local_residual_sourced", "Z_local_zero_bound", "selector_leak_abs", "Phi_boundary_bound_abs", "stress_gap_abs", "local_residual_bound_abs", "runner_status", "missing_rollup_inputs", "anti_circularity_status"])}

## Obstruction Update

{markdown_table(obstructions)}

## Promotion Gates

{markdown_table(gates)}

## Firewalls

{markdown_table(firewalls)}

## Decision Ledger

{markdown_table(decisions)}

## Status

{markdown_table(statuses)}

## Validation

{markdown_table(validations)}

## Next Target

`{NEXT_TARGET}`
"""
    write_text(DOC_PATH, content)

    formal_content = f"""# 815 - PPC4161 BC primitive owner or source selector parent action

Marker: `{MARKER}`
Generated: `{timestamp}`

## Formal Update

4799 reduces the local-GR bridge to two parent-owned objects:

1. `B_C/Phi_C` boundary primitive ownership from the parent boundary variation.
2. `Sigma_C` source-selector ownership from the parent action/Noether/Ward ledger.

The current executable nonclaim residual is:

```text
local_residual_bound_abs <= 4.96e-7
```

This bound is not yet an observational pass/fail number; 4800 must map it into PPN/R10/clock/orbital arena units or replace it with a parent no-flux/source theorem.

See `{DOC_PATH}`.
"""
    write_text(FORMAL_PATH, formal_content)


def update_registers(timestamp: str) -> None:
    claim_line = (
        f'{CLAIM_ID},BC_primitive_source_selector_parent_action_runner,'
        f'"4799 reduces the local-GR bridge to parent B_C/Phi_C boundary ownership and parent Sigma_C source-action ownership, while installing a conservative finite local residual rollup.",'
        f'"Generated source register, B_C primitive input/output, source-action input/output, local residual rollup, gates, firewalls, decision, status, next target and validation.",'
        f'BC_source_action_gate_private_nonclaim_residual_rollup_ready,'
        f'{NEXT_TARGET},'
        f'"Do not promote topology, B_C silence, source selector, or finite residual rollup into local-GR/PPN/R10/clock/orbital evidence without arena source rows.",'
        f'local_gr,{DOC_PATH},{NEXT_TARGET},'
        f'B_C zero assertion; source by declaration; local/FLRW hand switch; edge cancellation; hidden Ward stress; local test promotion,'
        f'"B_C primitive and source-action parent gate",'
        f'{MARKER}; {DECISION}; generated {timestamp}\n'
    )
    if CLAIM_ID not in read_text(CLAIMS_PATH):
        with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
            handle.write(claim_line)

    spine_block = f"""
## {MARKER}

4799 makes the local bridge sharper: local topology can remove the absolute top source, but local GR still depends on parent ownership of the exact-sector boundary primitive `B_C/Phi_C` and the source selector `Sigma_C`.

Current private residual rollup:

```text
selector_leak_abs + Phi_boundary_bound_abs + stress_gap_abs = 4.96e-7
```

This is nonclaim infrastructure. 4800 must either map this bound to PPN/R10/clock/orbital rows or replace it with a parent no-flux/source-action theorem.
"""
    append_once(SPINE_PATH, MARKER, spine_block)

    packet_block = f"""
## {PACKET_MARKER}

- Checkpoint: `{DOC_PATH}`
- Formal note: `{FORMAL_PATH}`
- Runner: `{RUNNER}`
- Claim row: `{CLAIM_ID}`
- Decision: `{DECISION}`
- Next: `{NEXT_TARGET}`
"""
    append_once(PACKET_PATH, PACKET_MARKER, packet_block)

    resume = f"""# Current local resume

Updated: `{timestamp}`
Last checkpoint: `4799-Y5-R2FR-BC-primitive-owner-or-source-selector-parent-action.md`
Marker: `{MARKER}`

## Where we are

4799 installed the parent `B_C/Phi_C` boundary primitive gate, the parent `Sigma_C` source-action gate, and a conservative nonclaim local residual rollup:

```text
1.66e-7 + 1.70e-7 + 1.60e-7 = 4.96e-7
```

This is not a local-GR/PPN/R10/clock/orbital pass. It is the first clean residual object that can be pushed into local tests or replaced by a parent theorem.

## Live blockers

- Parent boundary variation must derive `B_C`, `Phi_C`, boundary counterterm ownership, charge preservation, and Ward boundary stress.
- Parent action/Noether source term must derive `Sigma_C = Pi_top[J_C]` without a local/FLRW hand switch.
- The finite residual must be projected into PPN/R10/clock/orbital units before any empirical claim.

## Next target

`{NEXT_TARGET}`
"""
    write_text(RESUME_PATH, resume)


def main() -> int:
    timestamp = now()
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    SCRIPT_DIR.mkdir(parents=True, exist_ok=True)

    write_text(RUNNER, RUNNER_TEXT)

    write_csv(SOURCE_REGISTER_CSV, source_register(timestamp))
    write_csv(BC_INPUT_CSV, bc_input_rows(timestamp))
    write_csv(SOURCE_ACTION_INPUT_CSV, source_action_input_rows(timestamp))
    write_csv(ROLLUP_INPUT_CSV, rollup_input_rows(timestamp))

    python = sys.executable
    run_command([python, str(RUNNER), "bc", str(BC_INPUT_CSV), str(BC_OUTPUT_CSV)])
    run_command([python, str(RUNNER), "source", str(SOURCE_ACTION_INPUT_CSV), str(SOURCE_ACTION_OUTPUT_CSV)])
    run_command([python, str(RUNNER), "rollup", str(ROLLUP_INPUT_CSV), str(ROLLUP_OUTPUT_CSV)])

    sources = parse_csv(SOURCE_REGISTER_CSV)
    bc_rows = parse_csv(BC_OUTPUT_CSV)
    source_rows = parse_csv(SOURCE_ACTION_OUTPUT_CSV)
    rollup_rows = parse_csv(ROLLUP_OUTPUT_CSV)

    obstructions = obstruction_rows(bc_rows, source_rows, rollup_rows)
    gates = gate_rows(bc_rows, source_rows, rollup_rows)
    firewalls = firewall_rows()
    decisions = decision_rows()
    statuses = status_rows(bc_rows, source_rows, rollup_rows)
    next_targets = next_target_rows()

    write_csv(OBSTRUCTION_CSV, obstructions)
    write_csv(GATE_CSV, gates)
    write_csv(FIREWALL_CSV, firewalls)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_TARGET_CSV, next_targets)

    update_registers(timestamp)
    validations = validation_rows(sources, bc_rows, source_rows, rollup_rows)
    write_csv(VALIDATION_CSV, validations)
    write_documents(timestamp, sources, bc_rows, source_rows, rollup_rows, obstructions, gates, firewalls, decisions, statuses, validations)

    run_command([python, "-m", "py_compile", str(RUNNER), str(Path(__file__))])
    cache = SCRIPT_DIR / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)

    if any(row["result"] != "PASS" for row in validations):
        print(f"{CHECKPOINT} validation failed: {VALIDATION_CSV}", file=sys.stderr)
        return 1
    print(f"{CHECKPOINT} complete: {DOC_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
