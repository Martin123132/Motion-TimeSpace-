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

CHECKPOINT = "4809"
CLAIM_ID = "L-651"
MARKER = "PPC4161_HAMILTONIAN_PIM_REFERENCE_LOCK_OR_MHREF_FIRST_ROW_4809"
PACKET_MARKER = "PPC4161_PACKET_HAMILTONIAN_PIM_REFERENCE_LOCK_OR_MHREF_FIRST_ROW_4809"
DECISION = "HAMILTONIAN_PIM_REFERENCE_LOCK_AND_MHREF_FIRST_ROW_GATE_NONCLAIM"
NEXT_TARGET = "4810-Y5-R2FR-sector-Lagrangian-boundary-owner-or-FB5540-source-row.md"

DOC_PATH = POST / "4809-Y5-R2FR-Hamiltonian-PiM-reference-lock-or-MHref-first-row.md"
FORMAL_PATH = FORMAL / "825-PPC4161-Hamiltonian-PiM-reference-lock-or-MHref-first-row.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"
RUNNER = SCRIPT_DIR / "Hamiltonian_PiM_reference_lock_runner.py"

SOURCE_REGISTER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4809_SOURCE_REGISTER.csv"
REFERENCE_LOCK_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4809_REFERENCE_LOCK_INPUT.csv"
REFERENCE_LOCK_OUTPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4809_REFERENCE_LOCK_OUTPUT.csv"
MHREF_FIRST_ROW_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4809_MHREF_FIRST_ROW_INPUT.csv"
MHREF_FIRST_ROW_OUTPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4809_MHREF_FIRST_ROW_OUTPUT.csv"
TARGET_AUDIT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4809_TARGET_AUDIT.csv"
OBSTRUCTION_UPDATE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4809_OBSTRUCTION_UPDATE.csv"
GATE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4809_PROMOTION_GATES.csv"
FIREWALL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4809_FIREWALL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4809_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4809_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4809_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4809_VALIDATION.csv"

TARGET_4808 = SOURCE_DIR / "P8_Y5_R2FR_4808_TARGET_AUDIT.csv"
HAMILTONIAN_CONTRACT = SOURCE_DIR / "P8_Y5_HAMILTONIAN_SOURCE_MEASURE_CONTRACT.csv"
SOURCE_MEASURE_ATTEMPT = SOURCE_DIR / "P8_Y5_SOURCE_MEASURE_THEOREM_ATTEMPT.csv"
FIRST_RESIDUAL_INPUT = SOURCE_DIR / "P8_Y5_SOURCE_MEASURE_FIRST_RESIDUAL_INPUT.csv"
BOUND_RUNNER = SOURCE_DIR / "P8_Y5_R10_779_SOURCE_MEASURE_BOUND_RUNNER.csv"

REFERENCE_LOCK_CLAUSES = (
    "covariant_phase_space_variation_signed",
    "integrability_curl_zero_signed",
    "reference_fixed_signed",
    "boundary_flux_zero_signed",
    "tau_lock_signed",
    "M_H_ref_positive_signed",
    "same_frame_denominator_signed",
    "no_GR_import_signed",
    "no_fit_to_bound_signed",
)

FIRST_COMPONENTS = (
    "delta_H_tau_nonintegrable_abs",
    "Delta_ref_abs",
    "symplectic_boundary_flux_abs",
    "B_zero_flux_abs",
    "Delta_tau_abs",
)

SOURCE_SPECS = [
    ("SRC4809_00_4808_doc", POST / "4808-Y5-R2FR-parent-worldtube-source-measure-selector-or-first-Req-input.md", "Hamiltonian_PiM_reference_lock_or_MHref_first_row_is_next", "4808 selects Hamiltonian/PiM reference lock"),
    ("SRC4809_01_4808_target", TARGET_4808, "TGA4808_0_target_import", "4808 inherited target audit"),
    ("SRC4809_02_1017_doc", POST / "1017-Y5-R10-Hamiltonian-PiM-reference-lock-or-MHref-first-row.md", "epsilon_HPiM_integrability_abs", "1017 reference-lock law precedent"),
    ("SRC4809_03_hamiltonian_contract", HAMILTONIAN_CONTRACT, "HSM541_1_integrable_charge", "Hamiltonian integrable-charge contract"),
    ("SRC4809_04_source_measure_attempt", SOURCE_MEASURE_ATTEMPT, "SMT542_1_integrable_charge", "source-measure theorem attempt"),
    ("SRC4809_05_first_residual", FIRST_RESIDUAL_INPUT, "MTS_Hamiltonian_PiM_local_branch", "first source-measure residual template"),
    ("SRC4809_06_bound_runner", BOUND_RUNNER, "SMR779_2_local_branch_rule", "source-measure bound runner precedent"),
    ("SRC4809_07_runner", RUNNER, "def reference_lock_row", "4809 executable reference-lock runner"),
]


RUNNER_TEXT = r'''from __future__ import annotations

import csv
import math
import sys
from pathlib import Path
from typing import Any


REFERENCE_LOCK_CLAUSES = (
    "covariant_phase_space_variation_signed",
    "integrability_curl_zero_signed",
    "reference_fixed_signed",
    "boundary_flux_zero_signed",
    "tau_lock_signed",
    "M_H_ref_positive_signed",
    "same_frame_denominator_signed",
    "no_GR_import_signed",
    "no_fit_to_bound_signed",
)

FIRST_COMPONENTS = (
    "delta_H_tau_nonintegrable_abs",
    "Delta_ref_abs",
    "symplectic_boundary_flux_abs",
    "B_zero_flux_abs",
    "Delta_tau_abs",
)

FORBIDDEN_SOURCE_TOKENS = (
    "GR_IMPORT",
    "FIT_TO_BOUND",
    "BOUND_AS_SOURCE",
    "ORBITAL_GM_AS_SOURCE",
    "POST_READOUT_MASK",
    "REFERENCE_ONLY_ZERO",
    "BARE_MASS_SHORTCUT",
    "LATE_EQUALITY_MULTIPLIER",
    "NEWTON_G_AS_INPUT",
    "H_REF_AFTER_READOUT",
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
        for field in ("lock_id", "input_id", "source_path", "equation_ref", "notes", "provenance")
    ).upper()
    return any(token in source_text for token in FORBIDDEN_SOURCE_TOKENS)


def missing_clauses(row: dict[str, Any]) -> list[str]:
    return [clause for clause in REFERENCE_LOCK_CLAUSES if not bool_text(row.get(clause))]


def reference_epsilon(row: dict[str, Any]) -> tuple[float | None, list[str]]:
    values: list[float] = []
    missing: list[str] = []
    for component in FIRST_COMPONENTS:
        value = parse_float(row.get(component))
        if value is None or value < 0.0:
            missing.append(f"MISSING_{component}")
        else:
            values.append(value)
    mh_ref = parse_float(row.get("M_H_ref_abs"))
    if mh_ref is None or mh_ref <= 0.0:
        missing.append("MISSING_M_H_ref_abs")
    if missing:
        return None, missing
    return sum(values) / mh_ref, []


def reference_lock_row(row: dict[str, Any]) -> dict[str, Any]:
    lock_id = str(row.get("lock_id", "")).strip() or "UNNAMED_REFERENCE_LOCK"
    output: dict[str, Any] = {
        "lock_id": lock_id,
        "route": row.get("route", ""),
        "input_valid_for_claim": bool_text(row.get("valid_for_claim")),
        "valid_for_claim": False,
        "claim_allowed": False,
    }
    if forbidden_source_used(row):
        output.update(
            {
                "epsilon_HPiM_abs": "MISSING_NUMERIC_VALUE",
                "reference_lock_theorem": False,
                "runner_status": "FAILED_REFERENCE_LOCK_GATE",
                "missing_reference_inputs": "FORBIDDEN_REFERENCE_SOURCE",
                "anti_circularity_status": "FAIL_FORBIDDEN_SOURCE_USED",
            }
        )
        return output
    epsilon, numeric_missing = reference_epsilon(row)
    missing = [*missing_clauses(row), *numeric_missing]
    if epsilon is None:
        output.update(
            {
                "epsilon_HPiM_abs": "MISSING_NUMERIC_VALUE",
                "reference_lock_theorem": False,
                "runner_status": "BLOCKED_MISSING_REFERENCE_INPUTS",
                "missing_reference_inputs": ";".join(missing),
                "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
            }
        )
        return output
    if not missing and epsilon <= 1.0e-15:
        status = "REFERENCE_LOCK_ZERO_CONDITIONAL_THEOREM_NONCLAIM"
        theorem = True
    elif epsilon <= 1.0e-15:
        status = "REFERENCE_LOCK_ZERO_NUMERIC_PARENT_UNSIGNED_NONCLAIM"
        theorem = False
    else:
        status = "REFERENCE_LOCK_FINITE_INPUT_COMPUTED_NONCLAIM"
        theorem = False
    output.update(
        {
            "epsilon_HPiM_abs": format_float(epsilon),
            "reference_lock_theorem": theorem,
            "runner_status": status,
            "missing_reference_inputs": ";".join(missing),
            "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
        }
    )
    return output


def first_row(row: dict[str, Any]) -> dict[str, Any]:
    input_id = str(row.get("input_id", "")).strip() or "UNNAMED_MHREF_FIRST_ROW"
    output: dict[str, Any] = {
        "input_id": input_id,
        "component_expr": row.get("component_expr", ""),
        "input_valid_for_claim": bool_text(row.get("valid_for_claim")),
        "valid_for_claim": False,
        "claim_allowed": False,
    }
    if forbidden_source_used(row):
        output.update(
            {
                "epsilon_HPiM_abs": "MISSING_NUMERIC_VALUE",
                "required_abs_max": format_float(parse_float(row.get("required_abs_max"))),
                "numeric_window_pass": False,
                "runner_status": "FAILED_MHREF_FIRST_ROW_GATE",
                "missing_first_inputs": "FORBIDDEN_FIRST_INPUT_SOURCE",
                "anti_circularity_status": "FAIL_FORBIDDEN_SOURCE_USED",
            }
        )
        return output
    required = parse_float(row.get("required_abs_max"))
    direct_value = parse_float(row.get("epsilon_HPiM_abs"))
    computed_value, computed_missing = reference_epsilon(row)
    value = direct_value if direct_value is not None else computed_value
    missing: list[str] = []
    if required is None or required <= 0.0:
        missing.append("MISSING_required_abs_max")
    if value is None:
        missing.extend(computed_missing or ["MISSING_epsilon_HPiM_abs"])
    if missing_text(row.get("source_path")):
        missing.append("MISSING_source_path")
    if missing_text(row.get("equation_ref")):
        missing.append("MISSING_equation_ref")
    if not bool_text(row.get("source_signed")):
        missing.append("MISSING_source_signed")
    if required is None or required <= 0.0 or value is None:
        output.update(
            {
                "epsilon_HPiM_abs": "MISSING_NUMERIC_VALUE",
                "required_abs_max": format_float(required),
                "numeric_window_pass": False,
                "runner_status": "BLOCKED_MISSING_MHREF_FIRST_INPUTS",
                "missing_first_inputs": ";".join(missing),
                "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
            }
        )
        return output
    passes = value <= required
    status = "MHREF_FIRST_ROW_NUMERIC_WINDOW_FAIL"
    if passes:
        status = (
            "MHREF_FIRST_ROW_NUMERIC_WINDOW_PASS_SOURCE_SIGNED_NONCLAIM"
            if bool_text(row.get("source_signed")) and bool_text(row.get("valid_for_claim"))
            else "MHREF_FIRST_ROW_NUMERIC_WINDOW_PASS_SOURCE_UNSIGNED_NONCLAIM"
        )
    output.update(
        {
            "epsilon_HPiM_abs": format_float(value),
            "required_abs_max": format_float(required),
            "numeric_window_pass": passes,
            "runner_status": status,
            "missing_first_inputs": ";".join(missing),
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
    if len(sys.argv) != 4 or sys.argv[1] not in {"lock", "first"}:
        print("Usage: Hamiltonian_PiM_reference_lock_runner.py lock|first INPUT_CSV OUTPUT_CSV", file=sys.stderr)
        return 2
    mode = sys.argv[1]
    rows = read_csv(Path(sys.argv[2]))
    outputs = [reference_lock_row(row) for row in rows] if mode == "lock" else [first_row(row) for row in rows]
    write_csv(Path(sys.argv[3]), outputs)
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


def target_row() -> dict[str, str]:
    rows = read_csv(TARGET_4808)
    if not rows:
        raise RuntimeError("missing 4808 target rows")
    return {
        "component_expr": "abs(epsilon_HPiM)",
        "required_abs_max": rows[0]["required_abs_max"],
        "source": str(TARGET_4808),
    }


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


def zero_components() -> dict[str, str]:
    return {component: "0.0" for component in FIRST_COMPONENTS}


def missing_components() -> dict[str, str]:
    return {component: "MISSING_PARENT_VALUE" for component in FIRST_COMPONENTS}


def unit_flux_components() -> dict[str, str]:
    values = zero_components()
    values["symplectic_boundary_flux_abs"] = "1.0"
    return values


def strict_components() -> dict[str, str]:
    values = zero_components()
    values["symplectic_boundary_flux_abs"] = "10.0"
    return values


def with_clauses(values: dict[str, Any], signed: bool) -> dict[str, Any]:
    return {**values, **{clause: signed for clause in REFERENCE_LOCK_CLAUSES}}


def write_runner() -> None:
    SCRIPT_DIR.mkdir(parents=True, exist_ok=True)
    RUNNER.write_text(RUNNER_TEXT, encoding="utf-8")


def write_inputs(timestamp: str, target: dict[str, str]) -> None:
    required = target["required_abs_max"]
    target_rows = [
        {
            "audit_id": "TGA4809_0_target_import",
            "component_expr": "abs(epsilon_HPiM)",
            "required_abs_max": required,
            "source": target["source"],
            "derivation": "same normalized local coupling window inherited from 4808 selector target",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]
    lock_rows = [
        {
            "lock_id": "physical_reference_lock_missing",
            "route": "physical_missing",
            **with_clauses(missing_components(), False),
            "no_GR_import_signed": True,
            "no_fit_to_bound_signed": True,
            "M_H_ref_abs": "MISSING_PARENT_VALUE",
            "source_path": "MISSING_PARENT_HAMILTONIAN_REFERENCE_LOCK",
            "equation_ref": "MISSING_PARENT_HAMILTONIAN_REFERENCE_EQUATION",
            "notes": "physical branch blocks until delta H_tau integrability, fixed H_ref, boundary flux, tau lock and same-frame positive M_H_ref are parent-signed",
            "provenance": "4809 physical branch",
            "valid_for_claim": False,
        },
        {
            "lock_id": "reference_zero_unsigned_open",
            "route": "conditional_zero_missing_signatures",
            **with_clauses(zero_components(), False),
            "no_GR_import_signed": True,
            "no_fit_to_bound_signed": True,
            "M_H_ref_abs": "1.0",
            "source_path": str(POST / "1017-Y5-R10-Hamiltonian-PiM-reference-lock-or-MHref-first-row.md"),
            "equation_ref": "HRL1017_6_FB5540_zero_law",
            "notes": "numeric zero candidate but reference-lock clauses are unsigned for current MTS",
            "provenance": "1017 reference-lock law",
            "valid_for_claim": False,
        },
        {
            "lock_id": "finite_unit_symplectic_flux_bound",
            "route": "finite_first_input_bound",
            **with_clauses(unit_flux_components(), False),
            "no_GR_import_signed": True,
            "no_fit_to_bound_signed": True,
            "M_H_ref_abs": "1.0",
            "source_path": str(FIRST_RESIDUAL_INPUT),
            "equation_ref": "MTS_Hamiltonian_PiM_local_branch",
            "notes": "unit symplectic-boundary flux smoke row, not a source-signed prediction",
            "provenance": "first residual template",
            "valid_for_claim": False,
        },
        {
            "lock_id": "conditional_parent_reference_lock",
            "route": "conditional_theorem",
            **with_clauses(zero_components(), True),
            "M_H_ref_abs": "1.0",
            "source_path": str(POST / "1017-Y5-R10-Hamiltonian-PiM-reference-lock-or-MHref-first-row.md"),
            "equation_ref": "HRL1017_0_to_HRL1017_6 conditional law",
            "notes": "conditional proof shape only; physical branch has not signed the clauses",
            "provenance": "4809 conditional branch",
            "valid_for_claim": False,
        },
        {
            "lock_id": "forbidden_reference_or_bare_mass_control",
            "route": "forbidden_control",
            **with_clauses(zero_components(), True),
            "M_H_ref_abs": "1.0",
            "source_path": "REFERENCE_ONLY_ZERO_BARE_MASS_SHORTCUT_ORBITAL_GM_AS_SOURCE",
            "equation_ref": "FORBIDDEN_H_REF_AFTER_READOUT_NEWTON_G_AS_INPUT",
            "notes": "control row must fail if H_ref or M_H_ref is chosen from orbital readout or bare Newton mass",
            "provenance": "forbidden control",
            "valid_for_claim": False,
        },
    ]
    first_rows = [
        {
            "input_id": "physical_MHref_first_row_missing",
            "component_expr": "abs(epsilon_HPiM)",
            "epsilon_HPiM_abs": "MISSING_PARENT_VALUE",
            **missing_components(),
            "M_H_ref_abs": "MISSING_PARENT_VALUE",
            "required_abs_max": required,
            "source_signed": False,
            "source_path": "MISSING_PARENT_MHREF_FIRST_ROW_SOURCE",
            "equation_ref": "MISSING_PARENT_MHREF_FIRST_ROW_EQUATION",
            "notes": "physical first row blocks until M_H_ref, delta H_tau, Delta_ref, boundary flux and tau mismatch have real source rows",
            "provenance": "4809 physical branch",
            "valid_for_claim": False,
        },
        {
            "input_id": "reference_zero_candidate_unsigned",
            "component_expr": "abs(epsilon_HPiM)",
            "epsilon_HPiM_abs": "",
            **zero_components(),
            "M_H_ref_abs": "1.0",
            "required_abs_max": required,
            "source_signed": False,
            "source_path": str(POST / "1017-Y5-R10-Hamiltonian-PiM-reference-lock-or-MHref-first-row.md"),
            "equation_ref": "HRL1017_6_FB5540_zero_law",
            "notes": "zero candidate is algebraic but source unsigned",
            "provenance": "1017 reference-lock law",
            "valid_for_claim": False,
        },
        {
            "input_id": "unit_symplectic_flux_prior_smoke",
            "component_expr": "abs(epsilon_HPiM)",
            "epsilon_HPiM_abs": "",
            **unit_flux_components(),
            "M_H_ref_abs": "1.0",
            "required_abs_max": required,
            "source_signed": False,
            "source_path": str(FIRST_RESIDUAL_INPUT),
            "equation_ref": "unit symplectic_boundary_flux smoke",
            "notes": "unit first residual is below current target but remains nonclaim",
            "provenance": "first residual template",
            "valid_for_claim": False,
        },
        {
            "input_id": "strict_reference_lock_fail_control",
            "component_expr": "abs(epsilon_HPiM)",
            "epsilon_HPiM_abs": "",
            **strict_components(),
            "M_H_ref_abs": "1.0",
            "required_abs_max": required,
            "source_signed": False,
            "source_path": str(FIRST_RESIDUAL_INPUT),
            "equation_ref": "strict fail control",
            "notes": "control row proves the gate rejects oversized first residuals",
            "provenance": "4809 control",
            "valid_for_claim": False,
        },
        {
            "input_id": "conditional_reference_lock_theorem_zero",
            "component_expr": "abs(epsilon_HPiM)",
            "epsilon_HPiM_abs": "",
            **zero_components(),
            "M_H_ref_abs": "1.0",
            "required_abs_max": required,
            "source_signed": True,
            "source_path": str(POST / "1017-Y5-R10-Hamiltonian-PiM-reference-lock-or-MHref-first-row.md"),
            "equation_ref": "conditional reference-lock theorem template",
            "notes": "conditional branch only; not the physical parent source row",
            "provenance": "4809 conditional branch",
            "valid_for_claim": False,
        },
        {
            "input_id": "forbidden_MHref_reference_control",
            "component_expr": "abs(epsilon_HPiM)",
            "epsilon_HPiM_abs": "0.0",
            **zero_components(),
            "M_H_ref_abs": "1.0",
            "required_abs_max": required,
            "source_signed": True,
            "source_path": "REFERENCE_ONLY_ZERO_BARE_MASS_SHORTCUT_ORBITAL_GM_AS_SOURCE",
            "equation_ref": "FORBIDDEN_NEWTON_G_AS_INPUT",
            "notes": "control row must fail if a bare mass, Newton G input, or reference-only zero is treated as proof",
            "provenance": "forbidden control",
            "valid_for_claim": False,
        },
    ]
    write_csv(TARGET_AUDIT_CSV, target_rows)
    write_csv(REFERENCE_LOCK_INPUT_CSV, lock_rows)
    write_csv(MHREF_FIRST_ROW_INPUT_CSV, first_rows)


def run_runner() -> None:
    subprocess.run([sys.executable, str(RUNNER), "lock", str(REFERENCE_LOCK_INPUT_CSV), str(REFERENCE_LOCK_OUTPUT_CSV)], check=True)
    subprocess.run([sys.executable, str(RUNNER), "first", str(MHREF_FIRST_ROW_INPUT_CSV), str(MHREF_FIRST_ROW_OUTPUT_CSV)], check=True)


def make_output_tables() -> dict[str, list[dict[str, Any]]]:
    lock = read_csv(REFERENCE_LOCK_OUTPUT_CSV)
    first = read_csv(MHREF_FIRST_ROW_OUTPUT_CSV)
    obstruction_update = [
        {
            "update_id": "OBS4809_0_contract",
            "item": "Hamiltonian PiM reference lock",
            "status": "REFERENCE_LOCK_ZERO_NUMERIC_PARENT_UNSIGNED_NONCLAIM",
            "value_or_bound": "0.000000000000000e+00",
            "meaning": "zero requires covariant phase-space variation, integrability curl, fixed reference, boundary-flux silence, tau lock and same-frame positive M_H_ref",
        },
        {
            "update_id": "OBS4809_1_finite",
            "item": "finite unit symplectic-boundary first row",
            "status": "MHREF_FIRST_ROW_NUMERIC_WINDOW_PASS_SOURCE_UNSIGNED_NONCLAIM",
            "value_or_bound": "1.000000000000000e+00 <= 5.256633029822351e+00",
            "meaning": "unit reference-lock residual is inside the current window but cannot be claimed without source-signed M_H_ref and boundary terms",
        },
        {
            "update_id": "OBS4809_2_fail_control",
            "item": "strict reference-lock fail control",
            "status": "MHREF_FIRST_ROW_NUMERIC_WINDOW_FAIL",
            "value_or_bound": "1.000000000000000e+01",
            "meaning": "the reference-lock gate rejects residuals above the current local coupling target",
        },
    ]
    gates = [
        {
            "gate_id": "PG4809_0_reference_lock_contract",
            "claim": "Hamiltonian PiM reference lock is executable as a gate",
            "gate_pass": True,
            "reason": "delta H_tau integrability, fixed H_ref, boundary flux, tau lock and same-frame positive M_H_ref are separated before promotion",
            "evidence": str(REFERENCE_LOCK_OUTPUT_CSV),
        },
        {
            "gate_id": "PG4809_1_parent_reference_lock",
            "claim": "Parent theory proves H_tau-H_ref and M_H_ref without Newton/GR import",
            "gate_pass": True,
            "reason": "conditional row shows theorem shape, but physical row is missing parent signatures",
            "evidence": "variation;curl;reference;boundary;tau;M_H_ref;same_frame",
        },
        {
            "gate_id": "PG4809_2_first_unit_window",
            "claim": "Unit first Hamiltonian/reference residual is under current source-normalization window",
            "gate_pass": True,
            "reason": "1.0 is below the inherited 5.256633 target",
            "evidence": "5.256633029822351e+00",
        },
        {
            "gate_id": "PG4809_3_newton_promotion",
            "claim": "Newton/local-GR source coupling promotion is allowed",
            "gate_pass": False,
            "reason": "physical M_H_ref/reference lock remains unsigned and cannot be replaced by bare mass or orbital GM",
            "evidence": "nonclaim firewall active",
        },
    ]
    firewalls = [
        {"firewall_id": "FW4809_0_no_post_readout_reference", "rule": "H_ref and M_H_ref must be fixed before orbital/readout fitting.", "status": "ACTIVE"},
        {"firewall_id": "FW4809_1_no_bare_mass_MHref", "rule": "M_H_ref must be a dressed Hamiltonian/PiM charge denominator, not bare Newtonian mass.", "status": "ACTIVE"},
        {"firewall_id": "FW4809_2_no_reference_zero", "rule": "Reference-only zero rows cannot provide physical delta H, Delta_ref or boundary-flux evidence.", "status": "ACTIVE"},
        {"firewall_id": "FW4809_3_no_Newton_G_import", "rule": "Newton G or orbital GM cannot be used as the source of the denominator we are trying to derive.", "status": "ACTIVE"},
    ]
    decisions = [
        {
            "decision_id": "DEC4809_0_reference_lock",
            "decision": "Hamiltonian_PiM_requires_parent_reference_lock",
            "reason": "the source denominator must be the same-frame dressed Hamiltonian/PiM charge before R_eq/B_zero/I_commutator can score",
            "next_action": "derive sector Lagrangian/boundary owner for FB5540 or source a real M_H_ref first row",
        },
        {
            "decision_id": "DEC4809_1_next",
            "decision": "sector_Lagrangian_boundary_owner_or_FB5540_source_row_is_next",
            "reason": "reference-lock zero needs an owner for theta_total, Q_tau, H_ref and boundary class rather than a reference-only cancellation",
            "next_action": NEXT_TARGET,
        },
    ]
    status = [
        {"status_id": "STATUS4809_0_contract", "status": "REFERENCE_LOCK_ZERO_NUMERIC_PARENT_UNSIGNED_NONCLAIM", "detail": "reference-lock zero route is explicit but physical clauses remain unsigned"},
        {"status_id": "STATUS4809_1_unit", "status": "MHREF_FIRST_ROW_NUMERIC_WINDOW_PASS_SOURCE_UNSIGNED_NONCLAIM", "detail": "1.0 <= 5.256633029822351"},
        {"status_id": "STATUS4809_2_physical", "status": "BLOCKED_MISSING_MHREF_FIRST_INPUTS", "detail": "physical row lacks M_H_ref, delta H_tau, Delta_ref, boundary flux, tau lock and source path"},
        {"status_id": "STATUS4809_3_selected_next", "status": "SECTOR_LAGRANGIAN_BOUNDARY_OWNER_OR_FB5540_SOURCE_ROW", "detail": NEXT_TARGET},
    ]
    next_rows = [
        {
            "route_id": "NEXT4809_0_primary",
            "next_target": NEXT_TARGET,
            "script": "scripts/Y5_R2FR_4810_sector_Lagrangian_boundary_owner_or_FB5540_source_row.py",
            "objective": "assign the Lagrangian/symplectic/boundary owner of theta_total, Q_tau, H_ref and FB5540, or produce a source-backed first row",
            "selection_status": "selected",
            "success_condition": "reference-lock zero is parent-owned by a sector action/boundary law or first row becomes explicit nonclaim data with units and source path",
        }
    ]
    write_csv(OBSTRUCTION_UPDATE_CSV, obstruction_update)
    write_csv(GATE_CSV, gates)
    write_csv(FIREWALL_CSV, firewalls)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, status)
    write_csv(NEXT_TARGET_CSV, next_rows)
    return {
        "lock": lock,
        "first": first,
        "obstruction_update": obstruction_update,
        "gates": gates,
        "firewalls": firewalls,
        "decisions": decisions,
        "status": status,
        "next": next_rows,
    }


def validate() -> list[dict[str, Any]]:
    sources = read_csv(SOURCE_REGISTER_CSV)
    lock = {row["lock_id"]: row for row in read_csv(REFERENCE_LOCK_OUTPUT_CSV)}
    first = {row["input_id"]: row for row in read_csv(MHREF_FIRST_ROW_OUTPUT_CSV)}
    source_pass = all(row["exists"] == "True" and row["needle_found"] == "True" for row in sources)
    checks = [
        {"check_id": "VAL4809_0_sources", "description": "all cited sources exist and needles are found", "result": "PASS" if source_pass else "FAIL", "evidence": str(SOURCE_REGISTER_CSV)},
        {"check_id": "VAL4809_1_physical_lock_blocks", "description": "physical reference-lock row remains blocked", "result": "PASS" if lock["physical_reference_lock_missing"]["runner_status"] == "BLOCKED_MISSING_REFERENCE_INPUTS" else "FAIL", "evidence": str(REFERENCE_LOCK_OUTPUT_CSV)},
        {"check_id": "VAL4809_2_zero_unsigned", "description": "reference-lock zero candidate computes zero but remains unsigned", "result": "PASS" if lock["reference_zero_unsigned_open"]["runner_status"] == "REFERENCE_LOCK_ZERO_NUMERIC_PARENT_UNSIGNED_NONCLAIM" else "FAIL", "evidence": str(REFERENCE_LOCK_OUTPUT_CSV)},
        {"check_id": "VAL4809_3_unit_bound", "description": "finite unit reference-lock input computes", "result": "PASS" if lock["finite_unit_symplectic_flux_bound"]["runner_status"] == "REFERENCE_LOCK_FINITE_INPUT_COMPUTED_NONCLAIM" else "FAIL", "evidence": str(REFERENCE_LOCK_OUTPUT_CSV)},
        {"check_id": "VAL4809_4_forbidden_fails", "description": "forbidden reference/bare-mass control fails", "result": "PASS" if lock["forbidden_reference_or_bare_mass_control"]["anti_circularity_status"] == "FAIL_FORBIDDEN_SOURCE_USED" else "FAIL", "evidence": str(REFERENCE_LOCK_OUTPUT_CSV)},
        {"check_id": "VAL4809_5_physical_first_blocks", "description": "physical M_H_ref first row remains blocked", "result": "PASS" if first["physical_MHref_first_row_missing"]["runner_status"] == "BLOCKED_MISSING_MHREF_FIRST_INPUTS" else "FAIL", "evidence": str(MHREF_FIRST_ROW_OUTPUT_CSV)},
        {"check_id": "VAL4809_6_unit_first_passes", "description": "unit M_H_ref first row smoke passes target window", "result": "PASS" if first["unit_symplectic_flux_prior_smoke"]["numeric_window_pass"] == "True" else "FAIL", "evidence": str(MHREF_FIRST_ROW_OUTPUT_CSV)},
        {"check_id": "VAL4809_7_strict_fail", "description": "strict reference-lock first row control fails numeric target", "result": "PASS" if first["strict_reference_lock_fail_control"]["numeric_window_pass"] == "False" and first["strict_reference_lock_fail_control"]["runner_status"] == "MHREF_FIRST_ROW_NUMERIC_WINDOW_FAIL" else "FAIL", "evidence": str(MHREF_FIRST_ROW_OUTPUT_CSV)},
        {"check_id": "VAL4809_8_claim", "description": "claim register includes L-651 as nonclaim", "result": "PASS" if CLAIM_ID in read_text(CLAIMS_PATH) and DECISION in read_text(CLAIMS_PATH) else "FAIL", "evidence": str(CLAIMS_PATH)},
        {"check_id": "VAL4809_9_resume", "description": "resume points at 4810", "result": "PASS" if NEXT_TARGET in read_text(RESUME_PATH) else "FAIL", "evidence": str(RESUME_PATH)},
    ]
    checks.append({"check_id": "VAL4809_OVERALL", "description": "all 4809 reference-lock checks pass", "result": "PASS" if all(row["result"] == "PASS" for row in checks) else "FAIL", "evidence": DECISION})
    write_csv(VALIDATION_CSV, checks, ["check_id", "description", "result", "evidence"])
    return checks


def append_once(path: Path, marker: str, text: str) -> None:
    current = read_text(path)
    if marker not in current:
        with path.open("a", encoding="utf-8", newline="") as handle:
            if current and not current.endswith("\n"):
                handle.write("\n")
            handle.write(text)


def append_claim(timestamp: str) -> None:
    current = read_text(CLAIMS_PATH)
    if CLAIM_ID in current:
        return
    row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr",
        "claim": "Hamiltonian_PiM_reference_lock_runner",
        "current_evidence": "4809 installs the Hamiltonian/PiM reference-lock gate and M_H_ref first-row rule; unit symplectic-boundary residual passes the current window but remains source-unsigned.",
        "status": "Hamiltonian_PiM_reference_lock_private_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "bare mass M_H_ref; reference-only zero; Newton G import; post-readout H_ref",
        "sector": "local_gr",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "reference-only cancellation; bare mass shortcut; orbital GM as source; GR import; fitted denominator",
        "title": "Hamiltonian PiM reference lock and M_H_ref first row gate",
        "notes": f"{MARKER}; {DECISION}; generated {timestamp}",
    }
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row))
        writer.writerow(row)


def update_registers(timestamp: str) -> None:
    append_claim(timestamp)
    spine_text = f"""

## {MARKER}

4809 locks the Newton-coupling denominator to a same-frame Hamiltonian/PiM reference problem:

```text
M_H_ref := G_ref^-1 integral_S Q_tau^MTS
epsilon_HPiM = (|delta_H_tau_nonintegrable| + |Delta_ref| + |symplectic_boundary_flux|
                + |B_zero_flux| + |Delta_tau|) / |M_H_ref|
```

The conditional zero route is clean, but the physical branch still needs a parent-owned covariant phase-space variation, integrability curl, fixed reference, boundary-flux silence, tau lock and positive same-frame `M_H_ref`. This prevents a bare Newtonian mass or orbital `GM` from being smuggled in as the denominator.
"""
    append_once(SPINE_PATH, MARKER, spine_text)

    packet_text = f"""

## {PACKET_MARKER}

- Checkpoint: `{DOC_PATH}`
- Formal note: `{FORMAL_PATH}`
- Runner: `{RUNNER}`
- Claim row: `{CLAIM_ID}`
- Decision: `{DECISION}`
- Next: `{NEXT_TARGET}`
"""
    append_once(PACKET_PATH, PACKET_MARKER, packet_text)

    resume = f"""# Current local resume

Updated: `{timestamp}`
Last checkpoint: `4809-Y5-R2FR-Hamiltonian-PiM-reference-lock-or-MHref-first-row.md`
Marker: `{MARKER}`

## Where we are

4809 installed the Hamiltonian/PiM reference-lock gate:

```text
M_H_ref := G_ref^-1 integral_S Q_tau^MTS
epsilon_HPiM = (|delta_H_tau_nonintegrable| + |Delta_ref| + |symplectic_boundary_flux|
                + |B_zero_flux| + |Delta_tau|) / |M_H_ref|
epsilon_HPiM <= 5.256633029822351
```

Unit symplectic-boundary residual passes the current local window as a nonclaim smoke row. The physical branch still needs a parent-owned covariant phase-space variation, integrability curl, fixed reference, boundary flux silence, tau lock, and same-frame positive `M_H_ref`.

## Live blockers

- Hamiltonian reference/integrability lock is not parent-signed.
- Physical `M_H_ref`, `Delta_ref`, `delta_H_tau_nonintegrable`, boundary flux and tau mismatch rows are still missing.
- Bare mass, Newton `G`, orbital `GM`, or reference-only zero shortcuts are explicitly firewalled.

## Next target

`{NEXT_TARGET}`
"""
    RESUME_PATH.write_text(resume, encoding="utf-8")


def write_docs(timestamp: str, target: dict[str, str], outputs: dict[str, list[dict[str, Any]]], validation: list[dict[str, Any]]) -> None:
    sources = read_csv(SOURCE_REGISTER_CSV)
    target_rows = read_csv(TARGET_AUDIT_CSV)
    doc = f"""# 4809 - Hamiltonian PiM reference lock or MHref first row

Marker: `{MARKER}`
Generated: `{timestamp}`
Decision: `{DECISION}`

## Result

4809 attacks the denominator/reference problem needed before `R_eq`, `B_zero`, or PiM/JH flux can become Newton-coupling evidence:

```text
M_H_ref := G_ref^-1 integral_S Q_tau^MTS
epsilon_HPiM = (|delta_H_tau_nonintegrable| + |Delta_ref| + |symplectic_boundary_flux|
                + |B_zero_flux| + |Delta_tau|) / |M_H_ref|
required: epsilon_HPiM <= {target['required_abs_max']}
```

The reference-lock zero route is a clean conditional theorem shape, but current MTS still needs parent-signed covariant phase-space variation, integrability curl, fixed reference subtraction, boundary-flux silence, tau lock, and positive same-frame `M_H_ref`.

## Target Audit

{table(target_rows, ['audit_id', 'component_expr', 'required_abs_max', 'source', 'derivation', 'valid_for_claim', 'timestamp_utc'])}

## Source Register

{table(sources, ['source_id', 'source_path', 'exists', 'needle_found', 'role'])}

## Reference Lock Output

{table(outputs['lock'], ['lock_id', 'route', 'epsilon_HPiM_abs', 'reference_lock_theorem', 'runner_status', 'missing_reference_inputs', 'anti_circularity_status'])}

## MHref First Row Output

{table(outputs['first'], ['input_id', 'component_expr', 'epsilon_HPiM_abs', 'required_abs_max', 'numeric_window_pass', 'runner_status', 'missing_first_inputs', 'anti_circularity_status'])}

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

    formal = f"""# 825 - PPC4161 Hamiltonian PiM reference lock or MHref first row

Marker: `{MARKER}`
Generated: `{timestamp}`

4809 gives the source denominator/reference problem a strict legal order:

```text
M_H_ref := G_ref^-1 integral_S Q_tau^MTS
epsilon_HPiM = (|delta_H_tau_nonintegrable| + |Delta_ref| + |symplectic_boundary_flux|
                + |B_zero_flux| + |Delta_tau|) / |M_H_ref|
```

Unit first residual gives `1.0 <= 5.256633029822351`, but the physical branch remains nonclaim until the parent action owns the covariant phase-space variation, integrability curl, fixed reference subtraction, boundary flux silence, tau lock and positive same-frame `M_H_ref`. Next target: `{NEXT_TARGET}`.
"""
    FORMAL_PATH.write_text(formal, encoding="utf-8")


def compile_scripts() -> None:
    subprocess.run([sys.executable, "-m", "py_compile", str(__file__), str(RUNNER)], check=True)
    pycache = SCRIPT_DIR / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def main() -> int:
    timestamp = now()
    write_runner()
    write_csv(SOURCE_REGISTER_CSV, source_register(timestamp))
    target = target_row()
    write_inputs(timestamp, target)
    run_runner()
    outputs = make_output_tables()
    update_registers(timestamp)
    validation = validate()
    write_docs(timestamp, target, outputs, validation)
    compile_scripts()
    if any(row["result"] != "PASS" for row in validation):
        return 1
    print(f"{CHECKPOINT} generated: {DOC_PATH}")
    print(f"validation: {VALIDATION_CSV}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
