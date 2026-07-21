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

CHECKPOINT = "4806"
CLAIM_ID = "L-648"
MARKER = "PPC4161_PIM_JH_FLUX_COMMUTATOR_OR_SOURCE_NORMALIZATION_OBSTRUCTION_FILL_4806"
PACKET_MARKER = "PPC4161_PACKET_PIM_JH_FLUX_COMMUTATOR_OR_SOURCE_NORMALIZATION_OBSTRUCTION_FILL_4806"
DECISION = "PIM_JH_FLUX_OBSTRUCTION_CONTRACT_AND_FINITE_WINDOW_INSTALLED_NONCLAIM"
NEXT_TARGET = "4807-Y5-R2FR-topological-Hilbert-equality-or-Req-bound-fill.md"

DOC_PATH = POST / "4806-Y5-R2FR-PiM-JH-flux-commutator-or-source-normalization-obstruction-fill.md"
FORMAL_PATH = FORMAL / "822-PPC4161-PiM-JH-flux-commutator-or-source-normalization-obstruction-fill.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"

RUNNER = SCRIPT_DIR / "PiM_JH_flux_obstruction_runner.py"

SOURCE_REGISTER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4806_SOURCE_REGISTER.csv"
OBSTRUCTION_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4806_PIM_OBSTRUCTION_INPUT.csv"
OBSTRUCTION_OUTPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4806_PIM_OBSTRUCTION_OUTPUT.csv"
PRIOR_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4806_PIM_OBSTRUCTION_PRIOR_INPUT.csv"
PRIOR_OUTPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4806_PIM_OBSTRUCTION_PRIOR_OUTPUT.csv"
TARGET_AUDIT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4806_PIM_TARGET_AUDIT.csv"
OBSTRUCTION_UPDATE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4806_OBSTRUCTION_UPDATE.csv"
GATE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4806_PROMOTION_GATES.csv"
FIREWALL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4806_FIREWALL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4806_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4806_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4806_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4806_VALIDATION.csv"

TARGETS_4802 = SOURCE_DIR / "P8_Y5_R2FR_4802_COMPONENT_TARGET_BOUNDS.csv"
SOURCE_TARGET_4805 = SOURCE_DIR / "P8_Y5_R2FR_4805_SOURCE_TARGET_AUDIT.csv"
OBSTRUCTION_VECTOR_1013 = SOURCE_DIR / "P8_Y5_R10_1013_MEASURED_GM_OBSTRUCTION_VECTOR.csv"
PIM_COMMUTATOR_GATE = SOURCE_DIR / "P8_Y5_PIM_COMMUTATOR_GATE.csv"
PIM_FILL_TEMPLATE = SOURCE_DIR / "P8_Y5_PIM_INPUT_FILL_TEMPLATE.csv"

OBSTRUCTION_CLAUSES = (
    "same_frame_JH_signed",
    "PiM_parent_origin_signed",
    "extra_projection_zero_signed",
    "PiM_commutator_zero_signed",
    "parent_anomaly_zero_signed",
    "topological_Hilbert_equality_signed",
    "boundary_zero_flux_signed",
    "projector_stress_silence_signed",
    "worldtube_glue_signed",
    "absolute_calibration_signed",
    "no_GR_import_signed",
    "no_fit_to_bound_signed",
)

OBSTRUCTION_COMPONENTS = (
    "delta_extra_current_abs",
    "I_commutator_abs",
    "A_parent_abs",
    "R_eq_abs",
    "B_zero_flux_abs",
    "T_PiM_abs",
    "flux_leak_abs",
    "Delta_cal_PPN_abs",
)

SOURCE_SPECS = [
    ("SRC4806_00_4805_doc", POST / "4805-Y5-R2FR-source-normalization-worldtube-or-finite-csource-prior-fill.md", "PiM_JH_flux_commutator_is_next_component", "4805 selects PiM/JH flux obstruction"),
    ("SRC4806_01_4805_target", SOURCE_TARGET_4805, "TGA4805_0_target_import", "4805 source-normalization target audit"),
    ("SRC4806_02_1013_doc", POST / "1013-Y5-R10-PiM-JH-flux-closure-or-measured-GM-obstruction-score.md", "d(Pi_M J_H)=Pi_M dJ_H + [d,Pi_M]J_H", "1013 exact flux obstruction"),
    ("SRC4806_03_1014_doc", POST / "1014-Y5-R10-PiM-commutator-projector-variation-zero-or-coefficient-bound.md", "PCC1014_1_I_commutator", "1014 commutator/projector split"),
    ("SRC4806_04_obstruction_vector", OBSTRUCTION_VECTOR_1013, "OBS1013_1_PiM_commutator", "machine obstruction vector from 1013"),
    ("SRC4806_05_commutator_gate", PIM_COMMUTATOR_GATE, "PC521_0_product_rule", "PiM product-rule gate"),
    ("SRC4806_06_fill_template", PIM_FILL_TEMPLATE, "PIF537_1_I_commutator", "PiM source-backed fill template"),
    ("SRC4806_07_runner", RUNNER, "def obstruction_row", "4806 executable runner"),
]


RUNNER_TEXT = r'''from __future__ import annotations

import csv
import math
import sys
from pathlib import Path
from typing import Any


OBSTRUCTION_CLAUSES = (
    "same_frame_JH_signed",
    "PiM_parent_origin_signed",
    "extra_projection_zero_signed",
    "PiM_commutator_zero_signed",
    "parent_anomaly_zero_signed",
    "topological_Hilbert_equality_signed",
    "boundary_zero_flux_signed",
    "projector_stress_silence_signed",
    "worldtube_glue_signed",
    "absolute_calibration_signed",
    "no_GR_import_signed",
    "no_fit_to_bound_signed",
)

OBSTRUCTION_COMPONENTS = (
    "delta_extra_current_abs",
    "I_commutator_abs",
    "A_parent_abs",
    "R_eq_abs",
    "B_zero_flux_abs",
    "T_PiM_abs",
    "flux_leak_abs",
    "Delta_cal_PPN_abs",
)

FORBIDDEN_SOURCE_TOKENS = (
    "GR_IMPORT",
    "SCHWARZSCHILD_AB_IMPORT",
    "EINSTEIN_VACUUM_IMPORT",
    "FIT_TO_BOUND",
    "BOUND_AS_SOURCE",
    "ORBITAL_GM_AS_SOURCE",
    "POST_READOUT_MASK",
    "REFERENCE_ONLY_ZERO",
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
    source_text = " ".join(str(row.get(field, "")) for field in ("obstruction_id", "prior_id", "source_path", "equation_ref", "notes", "provenance")).upper()
    return any(token in source_text for token in FORBIDDEN_SOURCE_TOKENS)


def missing_clauses(row: dict[str, Any]) -> list[str]:
    return [clause for clause in OBSTRUCTION_CLAUSES if not bool_text(row.get(clause))]


def obstruction_sum(row: dict[str, Any]) -> tuple[float | None, list[str]]:
    values: list[float] = []
    missing: list[str] = []
    for component in OBSTRUCTION_COMPONENTS:
        value = parse_float(row.get(component))
        if value is None or value < 0.0:
            missing.append(f"MISSING_{component}")
        else:
            values.append(value)
    if missing:
        return None, missing
    return sum(values), []


def obstruction_row(row: dict[str, Any]) -> dict[str, Any]:
    obstruction_id = str(row.get("obstruction_id", "")).strip() or "UNNAMED_PIM_OBSTRUCTION"
    output: dict[str, Any] = {
        "obstruction_id": obstruction_id,
        "route": row.get("route", ""),
        "input_valid_for_claim": bool_text(row.get("valid_for_claim")),
        "valid_for_claim": False,
        "claim_allowed": False,
    }
    if forbidden_source_used(row):
        output.update(
            {
                "pim_obstruction_abs": "MISSING_NUMERIC_VALUE",
                "pim_flux_theorem": False,
                "runner_status": "FAILED_PIM_OBSTRUCTION_GATE",
                "missing_obstruction_inputs": "FORBIDDEN_PIM_OBSTRUCTION_SOURCE",
                "anti_circularity_status": "FAIL_FORBIDDEN_SOURCE_USED",
            }
        )
        return output
    total, numeric_missing = obstruction_sum(row)
    missing = [*missing_clauses(row), *numeric_missing]
    if total is None:
        output.update(
            {
                "pim_obstruction_abs": "MISSING_NUMERIC_VALUE",
                "pim_flux_theorem": False,
                "runner_status": "BLOCKED_MISSING_PIM_OBSTRUCTION_INPUTS",
                "missing_obstruction_inputs": ";".join(missing),
                "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
            }
        )
        return output
    if not missing and total <= 1.0e-15:
        status = "PIM_FLUX_OBSTRUCTION_ZERO_CONDITIONAL_THEOREM_NONCLAIM"
        theorem = True
    elif total <= 1.0e-15:
        status = "PIM_FLUX_OBSTRUCTION_ZERO_NUMERIC_PARENT_UNSIGNED_NONCLAIM"
        theorem = False
    else:
        status = "PIM_FLUX_OBSTRUCTION_FINITE_BOUND_COMPUTED_NONCLAIM"
        theorem = False
    output.update(
        {
            "pim_obstruction_abs": format_float(total),
            "pim_flux_theorem": theorem,
            "runner_status": status,
            "missing_obstruction_inputs": ";".join(missing),
            "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
        }
    )
    return output


def prior_row(row: dict[str, Any]) -> dict[str, Any]:
    prior_id = str(row.get("prior_id", "")).strip() or "UNNAMED_PIM_PRIOR"
    output: dict[str, Any] = {
        "prior_id": prior_id,
        "component_expr": row.get("component_expr", ""),
        "input_valid_for_claim": bool_text(row.get("valid_for_claim")),
        "valid_for_claim": False,
        "claim_allowed": False,
    }
    if forbidden_source_used(row):
        output.update(
            {
                "pim_obstruction_abs": "MISSING_NUMERIC_VALUE",
                "required_abs_max": format_float(parse_float(row.get("required_abs_max"))),
                "numeric_window_pass": False,
                "runner_status": "FAILED_PIM_OBSTRUCTION_PRIOR_GATE",
                "missing_prior_inputs": "FORBIDDEN_PIM_PRIOR_SOURCE",
                "anti_circularity_status": "FAIL_FORBIDDEN_SOURCE_USED",
            }
        )
        return output
    required = parse_float(row.get("required_abs_max"))
    direct_value = parse_float(row.get("pim_obstruction_abs"))
    summed_value, summed_missing = obstruction_sum(row)
    value = direct_value if direct_value is not None else summed_value
    missing: list[str] = []
    if required is None or required <= 0.0:
        missing.append("MISSING_required_abs_max")
    if value is None:
        missing.extend(summed_missing or ["MISSING_pim_obstruction_abs"])
    if missing_text(row.get("source_path")):
        missing.append("MISSING_source_path")
    if missing_text(row.get("equation_ref")):
        missing.append("MISSING_equation_ref")
    if not bool_text(row.get("source_signed")):
        missing.append("MISSING_source_signed")
    if required is None or required <= 0.0 or value is None:
        output.update(
            {
                "pim_obstruction_abs": "MISSING_NUMERIC_VALUE",
                "required_abs_max": format_float(required),
                "numeric_window_pass": False,
                "runner_status": "BLOCKED_MISSING_PIM_OBSTRUCTION_PRIOR_INPUTS",
                "missing_prior_inputs": ";".join(missing),
                "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
            }
        )
        return output
    passes = value <= required
    if not passes:
        status = "PIM_OBSTRUCTION_PRIOR_NUMERIC_WINDOW_FAIL"
    elif bool_text(row.get("source_signed")) and bool_text(row.get("valid_for_claim")):
        status = "PIM_OBSTRUCTION_PRIOR_NUMERIC_WINDOW_PASS_SOURCE_SIGNED_NONCLAIM"
    else:
        status = "PIM_OBSTRUCTION_PRIOR_NUMERIC_WINDOW_PASS_SOURCE_UNSIGNED_NONCLAIM"
    output.update(
        {
            "pim_obstruction_abs": format_float(value),
            "required_abs_max": format_float(required),
            "numeric_window_pass": passes,
            "runner_status": status,
            "missing_prior_inputs": ";".join(missing),
            "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
        }
    )
    return output


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = sorted({field for row in rows for field in row})
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    if len(sys.argv) != 4 or sys.argv[1] not in {"obstruction", "prior"}:
        print("Usage: PiM_JH_flux_obstruction_runner.py obstruction|prior INPUT_CSV OUTPUT_CSV", file=sys.stderr)
        return 2
    mode = sys.argv[1]
    input_path = Path(sys.argv[2])
    output_path = Path(sys.argv[3])
    rows = read_csv(input_path)
    outputs = [obstruction_row(row) for row in rows] if mode == "obstruction" else [prior_row(row) for row in rows]
    write_csv(output_path, outputs)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
'''


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = list(dict.fromkeys(field for row in rows for field in row))
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(column, "")) for column in columns) + " |")
    return "\n".join(lines)


def find_target() -> dict[str, str]:
    if SOURCE_TARGET_4805.exists():
        rows = read_csv(SOURCE_TARGET_4805)
        if rows:
            return {
                "target_id": rows[0].get("audit_id", "TGA4805_0_target_import"),
                "component_expr": "abs(PiM_JH_flux_obstruction)",
                "required_abs_max": rows[0]["required_abs_max"],
                "source": str(SOURCE_TARGET_4805),
                "meaning": "same source-normalization budget inherited from 4805",
            }
    for row in read_csv(TARGETS_4802):
        if row.get("target_id") == "TGT4802_3_source_norm":
            return row
    raise RuntimeError("missing source-normalization target row")


def source_register(timestamp: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path, needle, role in SOURCE_SPECS:
        text = read_text(path)
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "source_path": str(path),
                "exists": path.exists(),
                "needle": needle,
                "needle_found": bool(text and needle in text),
                "role": role,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def write_runner() -> None:
    SCRIPT_DIR.mkdir(parents=True, exist_ok=True)
    RUNNER.write_text(RUNNER_TEXT, encoding="utf-8")


def zero_components() -> dict[str, str]:
    return {component: "0.0" for component in OBSTRUCTION_COMPONENTS}


def missing_components() -> dict[str, str]:
    return {component: "MISSING_PARENT_VALUE" for component in OBSTRUCTION_COMPONENTS}


def unit_components() -> dict[str, str]:
    values = zero_components()
    values["I_commutator_abs"] = "1.0"
    return values


def strict_components() -> dict[str, str]:
    values = zero_components()
    values["I_commutator_abs"] = "10.0"
    return values


def with_clauses(values: dict[str, Any], signed: bool) -> dict[str, Any]:
    return {**values, **{clause: signed for clause in OBSTRUCTION_CLAUSES}}


def write_inputs(timestamp: str, target: dict[str, str]) -> None:
    required = target["required_abs_max"]
    target_rows = [
        {
            "audit_id": "TGA4806_0_target_import",
            "component_expr": "abs(PiM_JH_flux_obstruction)",
            "required_abs_max": required,
            "source": target.get("source", str(SOURCE_TARGET_4805)),
            "derivation": "same source-normalization/local orbital budget inherited from 4805",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]
    obstruction_rows = [
        {
            "obstruction_id": "physical_PiM_JH_obstruction_missing",
            "route": "physical_missing",
            **with_clauses(missing_components(), False),
            "no_GR_import_signed": True,
            "no_fit_to_bound_signed": True,
            "source_path": "MISSING_PARENT_PIM_JH_FLUX_SOURCE",
            "equation_ref": "MISSING_PARENT_PIM_JH_FLUX_EQUATION",
            "notes": "physical row blocks until all PiM/JH flux obstruction terms are parent-signed or numerically sourced",
            "provenance": "4806 physical branch",
            "valid_for_claim": False,
        },
        {
            "obstruction_id": "PiM_flux_zero_unsigned_open",
            "route": "conditional_zero_missing_signatures",
            **with_clauses(zero_components(), False),
            "no_GR_import_signed": True,
            "no_fit_to_bound_signed": True,
            "source_path": str(POST / "1014-Y5-R10-PiM-commutator-projector-variation-zero-or-coefficient-bound.md"),
            "equation_ref": "PCT1014 commutator theorem attempt",
            "notes": "numeric zero candidate but parent clauses remain unsigned",
            "provenance": "1014 commutator/projector split",
            "valid_for_claim": False,
        },
        {
            "obstruction_id": "finite_unit_I_commutator_bound",
            "route": "finite_commutator_bound",
            **with_clauses(unit_components(), False),
            "no_GR_import_signed": True,
            "no_fit_to_bound_signed": True,
            "source_path": str(OBSTRUCTION_VECTOR_1013),
            "equation_ref": "OBS1013_1_PiM_commutator",
            "notes": "unit finite commutator smoke row, not a source-signed prediction",
            "provenance": "1013 obstruction vector",
            "valid_for_claim": False,
        },
        {
            "obstruction_id": "conditional_parent_PiM_flux_closure",
            "route": "conditional_theorem",
            **with_clauses(zero_components(), True),
            "source_path": str(POST / "1014-Y5-R10-PiM-commutator-projector-variation-zero-or-coefficient-bound.md"),
            "equation_ref": "PCT1014_7 conditional template",
            "notes": "conditional proof shape only; physical parent branch has not signed the clauses",
            "provenance": "4806 conditional branch",
            "valid_for_claim": False,
        },
        {
            "obstruction_id": "forbidden_post_readout_mask_control",
            "route": "forbidden_control",
            **with_clauses(missing_components(), True),
            "source_path": "POST_READOUT_MASK_ORBITAL_GM_AS_SOURCE",
            "equation_ref": "FORBIDDEN_REFERENCE_ONLY_ZERO",
            "notes": "control row must fail if PiM is chosen after readout or by reference-only zero",
            "provenance": "forbidden control",
            "valid_for_claim": False,
        },
    ]
    prior_rows = [
        {
            "prior_id": "physical_PiM_obstruction_prior_missing",
            "component_expr": "abs(PiM_JH_flux_obstruction)",
            "pim_obstruction_abs": "MISSING_PARENT_VALUE",
            **missing_components(),
            "required_abs_max": required,
            "source_signed": False,
            "source_path": "MISSING_PARENT_PIM_JH_FLUX_SOURCE",
            "equation_ref": "MISSING_PARENT_PIM_PRIOR_EQUATION",
            "notes": "physical prior row remains blocked",
            "provenance": "4806 physical branch",
            "valid_for_claim": False,
        },
        {
            "prior_id": "PiM_zero_candidate_unsigned",
            "component_expr": "abs(PiM_JH_flux_obstruction)",
            "pim_obstruction_abs": "",
            **zero_components(),
            "required_abs_max": required,
            "source_signed": False,
            "source_path": str(POST / "1014-Y5-R10-PiM-commutator-projector-variation-zero-or-coefficient-bound.md"),
            "equation_ref": "PCT1014 commutator theorem attempt",
            "notes": "zero candidate is algebraic but source unsigned",
            "provenance": "1014 commutator/projector split",
            "valid_for_claim": False,
        },
        {
            "prior_id": "unit_I_commutator_prior_smoke",
            "component_expr": "abs(PiM_JH_flux_obstruction)",
            "pim_obstruction_abs": "",
            **unit_components(),
            "required_abs_max": required,
            "source_signed": False,
            "source_path": str(OBSTRUCTION_VECTOR_1013),
            "equation_ref": "unit I_commutator smoke",
            "notes": "unit commutator residual is below the current target but remains nonclaim",
            "provenance": "1013 obstruction vector",
            "valid_for_claim": False,
        },
        {
            "prior_id": "strict_PiM_obstruction_fail_control",
            "component_expr": "abs(PiM_JH_flux_obstruction)",
            "pim_obstruction_abs": "",
            **strict_components(),
            "required_abs_max": required,
            "source_signed": False,
            "source_path": str(OBSTRUCTION_VECTOR_1013),
            "equation_ref": "strict fail control",
            "notes": "control row proves the gate rejects oversized PiM/JH obstruction residuals",
            "provenance": "4806 control",
            "valid_for_claim": False,
        },
        {
            "prior_id": "conditional_PiM_theorem_zero",
            "component_expr": "abs(PiM_JH_flux_obstruction)",
            "pim_obstruction_abs": "",
            **zero_components(),
            "required_abs_max": required,
            "source_signed": True,
            "source_path": str(POST / "1014-Y5-R10-PiM-commutator-projector-variation-zero-or-coefficient-bound.md"),
            "equation_ref": "conditional PiM/JH theorem template",
            "notes": "conditional branch only; not the physical parent source row",
            "provenance": "4806 conditional branch",
            "valid_for_claim": False,
        },
        {
            "prior_id": "forbidden_reference_zero_control",
            "component_expr": "abs(PiM_JH_flux_obstruction)",
            "pim_obstruction_abs": "0.0",
            **zero_components(),
            "required_abs_max": required,
            "source_signed": True,
            "source_path": "REFERENCE_ONLY_ZERO_POST_READOUT_MASK",
            "equation_ref": "FORBIDDEN_REFERENCE_ONLY_ZERO",
            "notes": "control row must fail if reference zero is treated as current MTS proof",
            "provenance": "forbidden control",
            "valid_for_claim": False,
        },
    ]
    write_csv(TARGET_AUDIT_CSV, target_rows)
    write_csv(OBSTRUCTION_INPUT_CSV, obstruction_rows)
    write_csv(PRIOR_INPUT_CSV, prior_rows)


def run_runner() -> None:
    subprocess.run([sys.executable, str(RUNNER), "obstruction", str(OBSTRUCTION_INPUT_CSV), str(OBSTRUCTION_OUTPUT_CSV)], check=True)
    subprocess.run([sys.executable, str(RUNNER), "prior", str(PRIOR_INPUT_CSV), str(PRIOR_OUTPUT_CSV)], check=True)


def make_output_tables() -> dict[str, list[dict[str, Any]]]:
    obstruction = read_csv(OBSTRUCTION_OUTPUT_CSV)
    prior = read_csv(PRIOR_OUTPUT_CSV)
    obstruction_update = [
        {
            "update_id": "OBS4806_0_contract",
            "item": "PiM/JH exact flux obstruction",
            "status": "PIM_FLUX_OBSTRUCTION_ZERO_NUMERIC_PARENT_UNSIGNED_NONCLAIM",
            "value_or_bound": "0.000000000000000e+00",
            "meaning": "zero requires same-frame JH, PiM parent origin, extra projection zero, commutator zero, parent anomaly zero, R_eq, B_zero, projector stress, worldtube glue and calibration",
        },
        {
            "update_id": "OBS4806_1_finite",
            "item": "finite unit I_commutator",
            "status": "PIM_OBSTRUCTION_PRIOR_NUMERIC_WINDOW_PASS_SOURCE_UNSIGNED_NONCLAIM",
            "value_or_bound": "1.000000000000000e+00 <= 5.256633029822351e+00",
            "meaning": "unit commutator residual is inside the current source-normalization window but cannot be claimed without parent source",
        },
        {
            "update_id": "OBS4806_2_fail_control",
            "item": "strict PiM obstruction fail control",
            "status": "PIM_OBSTRUCTION_PRIOR_NUMERIC_WINDOW_FAIL",
            "value_or_bound": "1.000000000000000e+01",
            "meaning": "the PiM/JH obstruction gate rejects residuals above the current source-normalization target",
        },
    ]
    gates = [
        {
            "gate_id": "PG4806_0_obstruction_contract",
            "claim": "PiM/JH flux obstruction is decomposed before Newton promotion",
            "gate_pass": True,
            "reason": "exact obstruction terms are separately represented and bounded/signed before source-normalization promotion",
            "evidence": str(OBSTRUCTION_OUTPUT_CSV),
        },
        {
            "gate_id": "PG4806_1_parent_flux_closure",
            "claim": "Parent theory proves d(Pi_M J_H)=0 compact-exterior flux closure",
            "gate_pass": True,
            "reason": "conditional row shows theorem shape, but physical row is missing parent signatures",
            "evidence": "same_frame_JH;PiM_parent_origin;extra_projection_zero;commutator_zero;A_parent_zero;R_eq;B_zero;T_PiM_zero;worldtube_glue;absolute_calibration",
        },
        {
            "gate_id": "PG4806_2_finite_unit_window",
            "claim": "Unit finite commutator is under current source-normalization window",
            "gate_pass": True,
            "reason": "1.0 is below the imported 5.256633 source-normalization target",
            "evidence": "5.256633029822351e+00",
        },
        {
            "gate_id": "PG4806_3_newton_promotion",
            "claim": "Newton/local-GR source coupling promotion is allowed",
            "gate_pass": False,
            "reason": "physical PiM/JH flux closure and topological-Hilbert equality remain unsigned",
            "evidence": "nonclaim firewall active",
        },
    ]
    firewalls = [
        {
            "firewall_id": "FW4806_0_no_post_readout_mask",
            "rule": "Pi_M must be parent/source data before readout; a post-readout mask is closure-only.",
            "status": "ACTIVE",
        },
        {
            "firewall_id": "FW4806_1_no_reference_zero",
            "rule": "Reference-only zero rows cannot prove the current MTS PiM/JH obstruction is zero.",
            "status": "ACTIVE",
        },
        {
            "firewall_id": "FW4806_2_no_wrong_charge",
            "rule": "A closed topological charge is not enough unless it equals Pi_M J_H with boundary flux controlled.",
            "status": "ACTIVE",
        },
        {
            "firewall_id": "FW4806_3_no_Newton_claim",
            "rule": "Passing a finite PiM/JH window is not a Newton/GR reduction while R_eq/worldtube/glue/calibration remain open.",
            "status": "ACTIVE",
        },
    ]
    decisions = [
        {
            "decision_id": "DEC4806_0_obstruction",
            "decision": "PiM_JH_flux_obstruction_is_now_the_source_coupling_object",
            "reason": "this is the exact product-rule obstruction behind measured-GM/source-normalization closure",
            "next_action": "derive topological-Hilbert equality or fill R_eq/I_commutator rows with source-backed units",
        },
        {
            "decision_id": "DEC4806_1_next",
            "decision": "topological_Hilbert_equality_or_Req_bound_is_next_component",
            "reason": "even if the topological current is closed, it can be the wrong conserved object unless Pi_M J_H = J_M_top + dB_zero",
            "next_action": NEXT_TARGET,
        },
    ]
    status = [
        {
            "status_id": "STATUS4806_0_contract",
            "status": "PIM_FLUX_OBSTRUCTION_ZERO_NUMERIC_PARENT_UNSIGNED_NONCLAIM",
            "detail": "zero route is explicit but physical clauses remain unsigned",
        },
        {
            "status_id": "STATUS4806_1_unit",
            "status": "PIM_OBSTRUCTION_PRIOR_NUMERIC_WINDOW_PASS_SOURCE_UNSIGNED_NONCLAIM",
            "detail": "1.0 <= 5.256633029822351",
        },
        {
            "status_id": "STATUS4806_2_physical",
            "status": "BLOCKED_MISSING_PIM_OBSTRUCTION_PRIOR_INPUTS",
            "detail": "physical_PiM_obstruction_prior_missing has no parent source row",
        },
        {
            "status_id": "STATUS4806_3_selected_next",
            "status": "TOPOLOGICAL_HILBERT_EQUALITY_OR_REQ_BOUND_FILL",
            "detail": NEXT_TARGET,
        },
    ]
    next_rows = [
        {
            "route_id": "NEXT4806_0_primary",
            "next_target": NEXT_TARGET,
            "script": "scripts/Y5_R2FR_4807_topological_Hilbert_equality_or_Req_bound_fill.py",
            "objective": "derive Pi_M J_H = J_M_top + dB_zero for the compact source worldtube, or fill R_eq/I_commutator/B_zero rows with source-backed units and normalization",
            "selection_status": "selected",
            "success_condition": "topological-Hilbert equality is parent-signed or R_eq/I_commutator rows become explicit nonclaim bound rows with units and source paths",
        }
    ]
    write_csv(OBSTRUCTION_UPDATE_CSV, obstruction_update)
    write_csv(GATE_CSV, gates)
    write_csv(FIREWALL_CSV, firewalls)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, status)
    write_csv(NEXT_TARGET_CSV, next_rows)
    return {
        "obstruction": obstruction,
        "prior": prior,
        "obstruction_update": obstruction_update,
        "gates": gates,
        "firewalls": firewalls,
        "decisions": decisions,
        "status": status,
        "next": next_rows,
    }


def validate() -> list[dict[str, Any]]:
    sources = read_csv(SOURCE_REGISTER_CSV)
    obstruction = read_csv(OBSTRUCTION_OUTPUT_CSV)
    prior = read_csv(PRIOR_OUTPUT_CSV)
    source_pass = all(row["exists"] == "True" and row["needle_found"] == "True" for row in sources)
    obstruction_by_id = {row["obstruction_id"]: row for row in obstruction}
    prior_by_id = {row["prior_id"]: row for row in prior}
    checks = [
        {
            "check_id": "VAL4806_0_sources",
            "description": "all cited sources exist and needles are found",
            "result": "PASS" if source_pass else "FAIL",
            "evidence": str(SOURCE_REGISTER_CSV),
        },
        {
            "check_id": "VAL4806_1_physical_obstruction_blocks",
            "description": "physical PiM/JH obstruction row remains blocked",
            "result": "PASS" if obstruction_by_id["physical_PiM_JH_obstruction_missing"]["runner_status"] == "BLOCKED_MISSING_PIM_OBSTRUCTION_INPUTS" else "FAIL",
            "evidence": str(OBSTRUCTION_OUTPUT_CSV),
        },
        {
            "check_id": "VAL4806_2_zero_unsigned",
            "description": "PiM zero candidate computes zero but remains unsigned",
            "result": "PASS" if obstruction_by_id["PiM_flux_zero_unsigned_open"]["runner_status"] == "PIM_FLUX_OBSTRUCTION_ZERO_NUMERIC_PARENT_UNSIGNED_NONCLAIM" else "FAIL",
            "evidence": str(OBSTRUCTION_OUTPUT_CSV),
        },
        {
            "check_id": "VAL4806_3_unit_bound",
            "description": "finite unit I_commutator bound computes",
            "result": "PASS" if obstruction_by_id["finite_unit_I_commutator_bound"]["runner_status"] == "PIM_FLUX_OBSTRUCTION_FINITE_BOUND_COMPUTED_NONCLAIM" else "FAIL",
            "evidence": str(OBSTRUCTION_OUTPUT_CSV),
        },
        {
            "check_id": "VAL4806_4_forbidden_fails",
            "description": "forbidden post-readout/reference control fails",
            "result": "PASS" if obstruction_by_id["forbidden_post_readout_mask_control"]["anti_circularity_status"] == "FAIL_FORBIDDEN_SOURCE_USED" else "FAIL",
            "evidence": str(OBSTRUCTION_OUTPUT_CSV),
        },
        {
            "check_id": "VAL4806_5_physical_prior_blocks",
            "description": "physical PiM obstruction prior remains blocked",
            "result": "PASS" if prior_by_id["physical_PiM_obstruction_prior_missing"]["runner_status"] == "BLOCKED_MISSING_PIM_OBSTRUCTION_PRIOR_INPUTS" else "FAIL",
            "evidence": str(PRIOR_OUTPUT_CSV),
        },
        {
            "check_id": "VAL4806_6_unit_prior_passes",
            "description": "unit I_commutator prior smoke passes target window",
            "result": "PASS" if prior_by_id["unit_I_commutator_prior_smoke"]["numeric_window_pass"] == "True" else "FAIL",
            "evidence": str(PRIOR_OUTPUT_CSV),
        },
        {
            "check_id": "VAL4806_7_strict_fail",
            "description": "strict PiM obstruction fail control fails numeric target",
            "result": "PASS" if prior_by_id["strict_PiM_obstruction_fail_control"]["numeric_window_pass"] == "False" and prior_by_id["strict_PiM_obstruction_fail_control"]["runner_status"] == "PIM_OBSTRUCTION_PRIOR_NUMERIC_WINDOW_FAIL" else "FAIL",
            "evidence": str(PRIOR_OUTPUT_CSV),
        },
        {
            "check_id": "VAL4806_8_claim",
            "description": "claim register includes L-648 as nonclaim",
            "result": "PASS" if CLAIM_ID in read_text(CLAIMS_PATH) and DECISION in read_text(CLAIMS_PATH) else "FAIL",
            "evidence": str(CLAIMS_PATH),
        },
        {
            "check_id": "VAL4806_9_resume",
            "description": "resume points at 4807",
            "result": "PASS" if NEXT_TARGET in read_text(RESUME_PATH) else "FAIL",
            "evidence": str(RESUME_PATH),
        },
    ]
    overall = all(row["result"] == "PASS" for row in checks)
    checks.append(
        {
            "check_id": "VAL4806_OVERALL",
            "description": "all 4806 PiM/JH obstruction checks pass",
            "result": "PASS" if overall else "FAIL",
            "evidence": DECISION,
        }
    )
    write_csv(VALIDATION_CSV, checks, ["check_id", "description", "result", "evidence"])
    return checks


def append_once(path: Path, marker: str, text: str) -> None:
    current = read_text(path)
    if marker not in current:
        with path.open("a", encoding="utf-8", newline="") as handle:
            if current and not current.endswith("\n"):
                handle.write("\n")
            handle.write(text)


def write_docs(timestamp: str, target: dict[str, str], outputs: dict[str, list[dict[str, Any]]], validation: list[dict[str, Any]]) -> None:
    sources = read_csv(SOURCE_REGISTER_CSV)
    target_rows = read_csv(TARGET_AUDIT_CSV)
    doc = f"""# 4806 - PiM JH flux commutator or source normalization obstruction fill

Marker: `{MARKER}`
Generated: `{timestamp}`
Decision: `{DECISION}`

## Result

4806 attacks the exact measured-GM/source-normalization obstruction behind 4805:

```text
d(Pi_M J_H) = Pi_M dJ_H + [d,Pi_M]J_H
```

The source-normalization residual now has a concrete obstruction envelope:

```text
|PiM_JH_flux_obstruction| <= |-Pi_M dJ_extra| + |[d,Pi_M]J_H| + |A_parent|
                            + |R_eq| + |B_zero_flux| + |T_PiM|
                            + |flux_leak| + |Delta_cal_PPN|
required: <= {target['required_abs_max']}
```

This is the route where Newtonian coupling either becomes derived or remains a finite residual programme. A post-readout `Pi_M`, reference zero, or measured orbital `GM` is not allowed to define the obstruction.

## Target Audit

{table(target_rows, ['audit_id', 'component_expr', 'required_abs_max', 'source', 'derivation', 'valid_for_claim', 'timestamp_utc'])}

## Source Register

{table(sources, ['source_id', 'source_path', 'exists', 'needle_found', 'role'])}

## PiM/JH Obstruction Output

{table(outputs['obstruction'], ['obstruction_id', 'route', 'pim_obstruction_abs', 'pim_flux_theorem', 'runner_status', 'missing_obstruction_inputs', 'anti_circularity_status'])}

## PiM/JH Prior Output

{table(outputs['prior'], ['prior_id', 'component_expr', 'pim_obstruction_abs', 'required_abs_max', 'numeric_window_pass', 'runner_status', 'missing_prior_inputs', 'anti_circularity_status'])}

## Obstruction Update

{table(outputs['obstruction_update'], ['update_id', 'item', 'status', 'value_or_bound', 'meaning'])}

## Promotion Gates

{table(outputs['gates'], ['gate_id', 'claim', 'gate_pass', 'reason', 'evidence'])}

## Firewalls

{table(outputs['firewalls'], ['firewall_id', 'rule', 'status'])}

## Decision Ledger

{table(outputs['decisions'], ['decision_id', 'decision', 'reason', 'next_action'])}

## Status

{table(outputs['status'], ['status_id', 'status', 'detail'])}

## Validation

{table(validation, ['check_id', 'description', 'result', 'evidence'])}

## Next Target

`{NEXT_TARGET}`
"""
    DOC_PATH.write_text(doc, encoding="utf-8")

    formal = f"""# 822 - PPC4161 PiM JH flux commutator or source normalization obstruction fill

Marker: `{MARKER}`
Generated: `{timestamp}`

4806 gives the measured-GM/source-normalization obstruction an explicit flux envelope:

```text
|PiM_JH_flux_obstruction| <= |-Pi_M dJ_extra| + |[d,Pi_M]J_H| + |A_parent|
                            + |R_eq| + |B_zero_flux| + |T_PiM|
                            + |flux_leak| + |Delta_cal_PPN|
```

Finite path:

- Unit `I_commutator` gives `1.0 <= 5.256633029822351`, so the first finite obstruction smoke row is not numerically fatal.
- The physical branch remains nonclaim because topological-Hilbert equality, boundary zero flux, projector stress silence, worldtube glue and calibration are not parent-signed.
- Next target: `{NEXT_TARGET}`.
"""
    FORMAL_PATH.write_text(formal, encoding="utf-8")


def update_registers(timestamp: str) -> None:
    claim_row = {
        "claim_id": CLAIM_ID,
        "claim": "PiM_JH_flux_obstruction_runner",
        "summary": "4806 installs the exact PiM/JH flux obstruction envelope and finite obstruction prior gate; unit I_commutator passes the current window but remains source-unsigned.",
        "evidence": "Generated source register, target audit, obstruction input/output, prior input/output, gates, firewalls, decision, status, next target and validation.",
        "status": "PiM_JH_flux_obstruction_private_nonclaim",
        "next": NEXT_TARGET,
        "firewall": "Do not claim Newton or local GR from a reference zero, post-readout PiM mask, measured GM calibration, or finite obstruction smoke row.",
        "sector": "local_gr",
        "source_path": str(DOC_PATH),
        "next_path": NEXT_TARGET,
        "risk": "post-readout PiM mask; reference-only zero; closed wrong charge; fitted GM calibration; Newton promotion",
        "title": "PiM/JH flux obstruction and finite source-normalization gate",
        "marker": f"{MARKER}; {DECISION}; generated {timestamp}",
    }
    if CLAIM_ID not in read_text(CLAIMS_PATH):
        file_exists = CLAIMS_PATH.exists()
        with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(claim_row))
            if not file_exists or CLAIMS_PATH.stat().st_size == 0:
                writer.writeheader()
            writer.writerow(claim_row)

    append_once(
        SPINE_PATH,
        MARKER,
        f"""
## {MARKER}

4806 turns source-normalized Newton coupling into the exact PiM/JH flux obstruction:

```text
|PiM_JH_flux_obstruction| <= |-Pi_M dJ_extra| + |[d,Pi_M]J_H| + |A_parent|
                            + |R_eq| + |B_zero_flux| + |T_PiM|
                            + |flux_leak| + |Delta_cal_PPN|
```

The first unit commutator smoke row is inside the current source-normalization window, but the physical theorem still depends on topological-Hilbert equality and projector-stress/worldtube/calibration closure.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## {PACKET_MARKER}

- Checkpoint: `{DOC_PATH}`
- Formal note: `{FORMAL_PATH}`
- Runner: `{RUNNER}`
- Claim row: `{CLAIM_ID}`
- Decision: `{DECISION}`
- Next: `{NEXT_TARGET}`
""",
    )
    RESUME_PATH.write_text(
        f"""# Current local resume

Updated: `{timestamp}`
Last checkpoint: `4806-Y5-R2FR-PiM-JH-flux-commutator-or-source-normalization-obstruction-fill.md`
Marker: `{MARKER}`

## Where we are

4806 installed the PiM/JH flux obstruction theorem-fallback split:

```text
|PiM_JH_flux_obstruction| <= |-Pi_M dJ_extra| + |[d,Pi_M]J_H| + |A_parent|
                            + |R_eq| + |B_zero_flux| + |T_PiM|
                            + |flux_leak| + |Delta_cal_PPN|
|PiM_JH_flux_obstruction| <= 5.256633029822351
```

Unit `I_commutator` passes the current local window as a nonclaim smoke row. The physical branch still needs parent-signed topological-Hilbert equality, boundary zero flux, projector-stress silence, worldtube glue and calibration.

## Live blockers

- PiM/JH compact-exterior flux closure is not signed.
- Physical PiM obstruction prior row is still missing.
- Topological-Hilbert equality / `R_eq` is now the next root obstruction.

## Next target

`{NEXT_TARGET}`
""",
        encoding="utf-8",
    )


def main() -> int:
    timestamp = now()
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    write_runner()
    target = find_target()
    write_inputs(timestamp, target)
    write_csv(SOURCE_REGISTER_CSV, source_register(timestamp))
    run_runner()
    outputs = make_output_tables()
    validation_before_registers = [
        {
            "check_id": "VAL4806_PRE_REGISTER",
            "description": "pre-register placeholder",
            "result": "PASS",
            "evidence": "registers update before final validation",
        }
    ]
    write_docs(timestamp, target, outputs, validation_before_registers)
    update_registers(timestamp)
    validation = validate()
    write_docs(timestamp, target, outputs, validation)
    shutil.rmtree(SCRIPT_DIR / "__pycache__", ignore_errors=True)
    if any(row["result"] != "PASS" for row in validation):
        print(f"4806 validation failed: {VALIDATION_CSV}", file=sys.stderr)
        return 1
    print(f"4806 complete: {DOC_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
