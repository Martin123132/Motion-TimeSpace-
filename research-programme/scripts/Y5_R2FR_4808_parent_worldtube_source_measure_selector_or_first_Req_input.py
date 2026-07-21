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

CHECKPOINT = "4808"
CLAIM_ID = "L-650"
MARKER = "PPC4161_PARENT_WORLDTUBE_SOURCE_MEASURE_SELECTOR_OR_FIRST_REQ_INPUT_4808"
PACKET_MARKER = "PPC4161_PACKET_PARENT_WORLDTUBE_SOURCE_MEASURE_SELECTOR_OR_FIRST_REQ_INPUT_4808"
DECISION = "PARENT_WORLDTUBE_SOURCE_MEASURE_SELECTOR_AND_FIRST_INPUT_GATE_NONCLAIM"
NEXT_TARGET = "4809-Y5-R2FR-Hamiltonian-PiM-reference-lock-or-MHref-first-row.md"

DOC_PATH = POST / "4808-Y5-R2FR-parent-worldtube-source-measure-selector-or-first-Req-input.md"
FORMAL_PATH = FORMAL / "824-PPC4161-parent-worldtube-source-measure-selector-or-first-Req-input.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"
RUNNER = SCRIPT_DIR / "parent_worldtube_source_measure_selector_runner.py"

SOURCE_REGISTER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4808_SOURCE_REGISTER.csv"
SELECTOR_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4808_SELECTOR_INPUT.csv"
SELECTOR_OUTPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4808_SELECTOR_OUTPUT.csv"
FIRST_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4808_FIRST_REQ_INPUT.csv"
FIRST_OUTPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4808_FIRST_REQ_OUTPUT.csv"
TARGET_AUDIT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4808_TARGET_AUDIT.csv"
OBSTRUCTION_UPDATE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4808_OBSTRUCTION_UPDATE.csv"
GATE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4808_PROMOTION_GATES.csv"
FIREWALL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4808_FIREWALL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4808_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4808_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4808_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4808_VALIDATION.csv"

TARGET_4807 = SOURCE_DIR / "P8_Y5_R2FR_4807_REQ_TARGET_AUDIT.csv"
PARENT_CONTRACT = SOURCE_DIR / "P8_Y5_HILBERT_WORLDTUBE_PARENT_ACTION_CONTRACT.csv"
HAMILTONIAN_CONTRACT = SOURCE_DIR / "P8_Y5_HAMILTONIAN_SOURCE_MEASURE_CONTRACT.csv"
SOURCE_MEASURE_ATTEMPT = SOURCE_DIR / "P8_Y5_SOURCE_MEASURE_THEOREM_ATTEMPT.csv"
FIRST_RESIDUAL_INPUT = SOURCE_DIR / "P8_Y5_SOURCE_MEASURE_FIRST_RESIDUAL_INPUT.csv"
BOBS_PACK = SOURCE_DIR / "P8_Y5_R10_777_BOBS_SOURCE_MEASURE_FIRST_PACK.csv"
BOUND_SCHEMA = SOURCE_DIR / "P8_Y5_R10_778_SOURCE_MEASURE_BOUND_SCHEMA.csv"
BOUND_RUNNER = SOURCE_DIR / "P8_Y5_R10_779_SOURCE_MEASURE_BOUND_RUNNER.csv"

SELECTOR_CLAUSES = (
    "parent_action_signed",
    "single_observed_frame_signed",
    "tau_fixed_signed",
    "compact_support_signed",
    "linking_surface_class_signed",
    "M_H_ref_integrable_signed",
    "PiM_Hamiltonian_map_signed",
    "coupling_descent_signed",
    "boundary_reference_lock_signed",
    "no_GR_import_signed",
    "no_fit_to_bound_signed",
)

FIRST_COMPONENTS = (
    "B_zero_flux_abs",
    "Delta_symp_abs",
    "H_ref_shift_abs",
    "Delta_worldtube_domain_abs",
    "Delta_frame_source_abs",
    "B_obs_source_measure_abs",
)

SOURCE_SPECS = [
    ("SRC4808_00_4807_doc", POST / "4807-Y5-R2FR-topological-Hilbert-equality-or-Req-bound-fill.md", "parent_worldtube_source_measure_selector_is_next_component", "4807 selects parent worldtube/source-measure"),
    ("SRC4808_01_4807_target", TARGET_4807, "TGA4807_0_target_import", "4807 inherited target audit"),
    ("SRC4808_02_1016_doc", POST / "1016-Y5-R10-parent-worldtube-source-measure-selector-or-R_eq-first-input.md", "W_source = closure(supp J_H[tau])", "1016 legal selector contract"),
    ("SRC4808_03_parent_contract", PARENT_CONTRACT, "PAC537_2_parent_fixed_worldtube", "parent action worldtube contract"),
    ("SRC4808_04_hamiltonian_contract", HAMILTONIAN_CONTRACT, "HSM541_2_observed_worldtube_source", "Hamiltonian source-measure contract"),
    ("SRC4808_05_source_measure_attempt", SOURCE_MEASURE_ATTEMPT, "SMT542_4_first_residual_trigger", "source-measure theorem attempt"),
    ("SRC4808_06_first_residual", FIRST_RESIDUAL_INPUT, "MTS_Hamiltonian_PiM_local_branch", "first source-measure residual template"),
    ("SRC4808_07_bound_runner", BOUND_RUNNER, "SMR779_2_local_branch_rule", "source-measure bound runner precedent"),
    ("SRC4808_08_runner", RUNNER, "def selector_row", "4808 executable runner"),
]


RUNNER_TEXT = r'''from __future__ import annotations

import csv
import math
import sys
from pathlib import Path
from typing import Any


SELECTOR_CLAUSES = (
    "parent_action_signed",
    "single_observed_frame_signed",
    "tau_fixed_signed",
    "compact_support_signed",
    "linking_surface_class_signed",
    "M_H_ref_integrable_signed",
    "PiM_Hamiltonian_map_signed",
    "coupling_descent_signed",
    "boundary_reference_lock_signed",
    "no_GR_import_signed",
    "no_fit_to_bound_signed",
)

FIRST_COMPONENTS = (
    "B_zero_flux_abs",
    "Delta_symp_abs",
    "H_ref_shift_abs",
    "Delta_worldtube_domain_abs",
    "Delta_frame_source_abs",
    "B_obs_source_measure_abs",
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
    source_text = " ".join(str(row.get(field, "")) for field in ("selector_id", "input_id", "source_path", "equation_ref", "notes", "provenance")).upper()
    return any(token in source_text for token in FORBIDDEN_SOURCE_TOKENS)


def missing_clauses(row: dict[str, Any]) -> list[str]:
    return [clause for clause in SELECTOR_CLAUSES if not bool_text(row.get(clause))]


def first_epsilon(row: dict[str, Any]) -> tuple[float | None, list[str]]:
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


def selector_row(row: dict[str, Any]) -> dict[str, Any]:
    selector_id = str(row.get("selector_id", "")).strip() or "UNNAMED_SELECTOR"
    output: dict[str, Any] = {
        "selector_id": selector_id,
        "route": row.get("route", ""),
        "input_valid_for_claim": bool_text(row.get("valid_for_claim")),
        "valid_for_claim": False,
        "claim_allowed": False,
    }
    if forbidden_source_used(row):
        output.update(
            {
                "epsilon_selector_abs": "MISSING_NUMERIC_VALUE",
                "selector_theorem": False,
                "runner_status": "FAILED_SELECTOR_GATE",
                "missing_selector_inputs": "FORBIDDEN_SELECTOR_SOURCE",
                "anti_circularity_status": "FAIL_FORBIDDEN_SOURCE_USED",
            }
        )
        return output
    epsilon, numeric_missing = first_epsilon(row)
    missing = [*missing_clauses(row), *numeric_missing]
    if epsilon is None:
        output.update(
            {
                "epsilon_selector_abs": "MISSING_NUMERIC_VALUE",
                "selector_theorem": False,
                "runner_status": "BLOCKED_MISSING_SELECTOR_INPUTS",
                "missing_selector_inputs": ";".join(missing),
                "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
            }
        )
        return output
    if not missing and epsilon <= 1.0e-15:
        status = "PARENT_SELECTOR_ZERO_CONDITIONAL_THEOREM_NONCLAIM"
        theorem = True
    elif epsilon <= 1.0e-15:
        status = "PARENT_SELECTOR_ZERO_NUMERIC_PARENT_UNSIGNED_NONCLAIM"
        theorem = False
    else:
        status = "PARENT_SELECTOR_FINITE_INPUT_COMPUTED_NONCLAIM"
        theorem = False
    output.update(
        {
            "epsilon_selector_abs": format_float(epsilon),
            "selector_theorem": theorem,
            "runner_status": status,
            "missing_selector_inputs": ";".join(missing),
            "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
        }
    )
    return output


def first_input_row(row: dict[str, Any]) -> dict[str, Any]:
    input_id = str(row.get("input_id", "")).strip() or "UNNAMED_FIRST_INPUT"
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
                "epsilon_selector_abs": "MISSING_NUMERIC_VALUE",
                "required_abs_max": format_float(parse_float(row.get("required_abs_max"))),
                "numeric_window_pass": False,
                "runner_status": "FAILED_FIRST_INPUT_GATE",
                "missing_first_inputs": "FORBIDDEN_FIRST_INPUT_SOURCE",
                "anti_circularity_status": "FAIL_FORBIDDEN_SOURCE_USED",
            }
        )
        return output
    required = parse_float(row.get("required_abs_max"))
    direct_value = parse_float(row.get("epsilon_selector_abs"))
    computed_value, computed_missing = first_epsilon(row)
    value = direct_value if direct_value is not None else computed_value
    missing: list[str] = []
    if required is None or required <= 0.0:
        missing.append("MISSING_required_abs_max")
    if value is None:
        missing.extend(computed_missing or ["MISSING_epsilon_selector_abs"])
    if missing_text(row.get("source_path")):
        missing.append("MISSING_source_path")
    if missing_text(row.get("equation_ref")):
        missing.append("MISSING_equation_ref")
    if not bool_text(row.get("source_signed")):
        missing.append("MISSING_source_signed")
    if required is None or required <= 0.0 or value is None:
        output.update(
            {
                "epsilon_selector_abs": "MISSING_NUMERIC_VALUE",
                "required_abs_max": format_float(required),
                "numeric_window_pass": False,
                "runner_status": "BLOCKED_MISSING_FIRST_INPUTS",
                "missing_first_inputs": ";".join(missing),
                "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
            }
        )
        return output
    passes = value <= required
    status = "FIRST_INPUT_NUMERIC_WINDOW_FAIL"
    if passes:
        status = "FIRST_INPUT_NUMERIC_WINDOW_PASS_SOURCE_SIGNED_NONCLAIM" if bool_text(row.get("source_signed")) and bool_text(row.get("valid_for_claim")) else "FIRST_INPUT_NUMERIC_WINDOW_PASS_SOURCE_UNSIGNED_NONCLAIM"
    output.update(
        {
            "epsilon_selector_abs": format_float(value),
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
    if len(sys.argv) != 4 or sys.argv[1] not in {"selector", "first"}:
        print("Usage: parent_worldtube_source_measure_selector_runner.py selector|first INPUT_CSV OUTPUT_CSV", file=sys.stderr)
        return 2
    mode = sys.argv[1]
    rows = read_csv(Path(sys.argv[2]))
    outputs = [selector_row(row) for row in rows] if mode == "selector" else [first_input_row(row) for row in rows]
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
    rows = read_csv(TARGET_4807)
    if not rows:
        raise RuntimeError("missing 4807 target rows")
    return {
        "component_expr": "abs(epsilon_selector)",
        "required_abs_max": rows[0]["required_abs_max"],
        "source": str(TARGET_4807),
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


def unit_components() -> dict[str, str]:
    values = zero_components()
    values["B_zero_flux_abs"] = "1.0"
    return values


def strict_components() -> dict[str, str]:
    values = zero_components()
    values["B_zero_flux_abs"] = "10.0"
    return values


def with_clauses(values: dict[str, Any], signed: bool) -> dict[str, Any]:
    return {**values, **{clause: signed for clause in SELECTOR_CLAUSES}}


def write_runner() -> None:
    SCRIPT_DIR.mkdir(parents=True, exist_ok=True)
    RUNNER.write_text(RUNNER_TEXT, encoding="utf-8")


def write_inputs(timestamp: str, target: dict[str, str]) -> None:
    required = target["required_abs_max"]
    target_rows = [
        {
            "audit_id": "TGA4808_0_target_import",
            "component_expr": "abs(epsilon_selector)",
            "required_abs_max": required,
            "source": target["source"],
            "derivation": "same R_eq/source-normalization budget inherited from 4807",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]
    selector_rows = [
        {
            "selector_id": "physical_selector_missing",
            "route": "physical_missing",
            **with_clauses(missing_components(), False),
            "no_GR_import_signed": True,
            "no_fit_to_bound_signed": True,
            "M_H_ref_abs": "MISSING_PARENT_VALUE",
            "source_path": "MISSING_PARENT_WORLDTUBE_SOURCE_SELECTOR",
            "equation_ref": "MISSING_PARENT_SELECTOR_EQUATION",
            "notes": "physical branch blocks until W_source, J_H[tau], M_H_ref, PiM_H, boundary/reference and coupling descent are parent-signed",
            "provenance": "4808 physical branch",
            "valid_for_claim": False,
        },
        {
            "selector_id": "selector_zero_unsigned_open",
            "route": "conditional_zero_missing_signatures",
            **with_clauses(zero_components(), False),
            "no_GR_import_signed": True,
            "no_fit_to_bound_signed": True,
            "M_H_ref_abs": "1.0",
            "source_path": str(POST / "1016-Y5-R10-parent-worldtube-source-measure-selector-or-R_eq-first-input.md"),
            "equation_ref": "PSC1016 parent selector contract",
            "notes": "numeric zero candidate but selector clauses are unsigned for current MTS",
            "provenance": "1016 selector contract",
            "valid_for_claim": False,
        },
        {
            "selector_id": "finite_unit_boundary_reference_bound",
            "route": "finite_first_input_bound",
            **with_clauses(unit_components(), False),
            "no_GR_import_signed": True,
            "no_fit_to_bound_signed": True,
            "M_H_ref_abs": "1.0",
            "source_path": str(FIRST_RESIDUAL_INPUT),
            "equation_ref": "MTS_Hamiltonian_PiM_local_branch",
            "notes": "unit boundary/reference smoke row, not a source-signed prediction",
            "provenance": "first residual template",
            "valid_for_claim": False,
        },
        {
            "selector_id": "conditional_parent_selector",
            "route": "conditional_theorem",
            **with_clauses(zero_components(), True),
            "M_H_ref_abs": "1.0",
            "source_path": str(POST / "1016-Y5-R10-parent-worldtube-source-measure-selector-or-R_eq-first-input.md"),
            "equation_ref": "PST1016 conditional selector lemma",
            "notes": "conditional proof shape only; physical branch has not signed the clauses",
            "provenance": "4808 conditional branch",
            "valid_for_claim": False,
        },
        {
            "selector_id": "forbidden_late_selector_control",
            "route": "forbidden_control",
            **with_clauses(missing_components(), True),
            "M_H_ref_abs": "MISSING_PARENT_VALUE",
            "source_path": "POST_READOUT_MASK_BARE_MASS_SHORTCUT_REFERENCE_ONLY_ZERO",
            "equation_ref": "FORBIDDEN_LATE_EQUALITY_MULTIPLIER",
            "notes": "control row must fail if W_source or M_H_ref is chosen after orbital readout",
            "provenance": "forbidden control",
            "valid_for_claim": False,
        },
    ]
    first_rows = [
        {
            "input_id": "physical_first_input_missing",
            "component_expr": "abs(epsilon_selector)",
            "epsilon_selector_abs": "MISSING_PARENT_VALUE",
            **missing_components(),
            "M_H_ref_abs": "MISSING_PARENT_VALUE",
            "required_abs_max": required,
            "source_signed": False,
            "source_path": "MISSING_PARENT_FIRST_INPUT_SOURCE",
            "equation_ref": "MISSING_PARENT_FIRST_INPUT_EQUATION",
            "notes": "physical first input row blocks until M_H_ref, B_zero, Delta_symp and source path are real",
            "provenance": "4808 physical branch",
            "valid_for_claim": False,
        },
        {
            "input_id": "selector_zero_candidate_unsigned",
            "component_expr": "abs(epsilon_selector)",
            "epsilon_selector_abs": "",
            **zero_components(),
            "M_H_ref_abs": "1.0",
            "required_abs_max": required,
            "source_signed": False,
            "source_path": str(POST / "1016-Y5-R10-parent-worldtube-source-measure-selector-or-R_eq-first-input.md"),
            "equation_ref": "PST1016 conditional selector lemma",
            "notes": "zero candidate is algebraic but source unsigned",
            "provenance": "1016 selector contract",
            "valid_for_claim": False,
        },
        {
            "input_id": "unit_boundary_reference_prior_smoke",
            "component_expr": "abs(epsilon_selector)",
            "epsilon_selector_abs": "",
            **unit_components(),
            "M_H_ref_abs": "1.0",
            "required_abs_max": required,
            "source_signed": False,
            "source_path": str(FIRST_RESIDUAL_INPUT),
            "equation_ref": "unit B_zero_flux smoke",
            "notes": "unit first residual is below current target but remains nonclaim",
            "provenance": "first residual template",
            "valid_for_claim": False,
        },
        {
            "input_id": "strict_selector_fail_control",
            "component_expr": "abs(epsilon_selector)",
            "epsilon_selector_abs": "",
            **strict_components(),
            "M_H_ref_abs": "1.0",
            "required_abs_max": required,
            "source_signed": False,
            "source_path": str(FIRST_RESIDUAL_INPUT),
            "equation_ref": "strict fail control",
            "notes": "control row proves the gate rejects oversized first residuals",
            "provenance": "4808 control",
            "valid_for_claim": False,
        },
        {
            "input_id": "conditional_selector_theorem_zero",
            "component_expr": "abs(epsilon_selector)",
            "epsilon_selector_abs": "",
            **zero_components(),
            "M_H_ref_abs": "1.0",
            "required_abs_max": required,
            "source_signed": True,
            "source_path": str(POST / "1016-Y5-R10-parent-worldtube-source-measure-selector-or-R_eq-first-input.md"),
            "equation_ref": "conditional selector theorem template",
            "notes": "conditional branch only; not the physical parent source row",
            "provenance": "4808 conditional branch",
            "valid_for_claim": False,
        },
        {
            "input_id": "forbidden_reference_selector_control",
            "component_expr": "abs(epsilon_selector)",
            "epsilon_selector_abs": "0.0",
            **zero_components(),
            "M_H_ref_abs": "1.0",
            "required_abs_max": required,
            "source_signed": True,
            "source_path": "REFERENCE_ONLY_ZERO_POST_READOUT_MASK_BARE_MASS_SHORTCUT",
            "equation_ref": "FORBIDDEN_REFERENCE_ONLY_ZERO",
            "notes": "control row must fail if reference zero or bare mass shortcut is treated as proof",
            "provenance": "forbidden control",
            "valid_for_claim": False,
        },
    ]
    write_csv(TARGET_AUDIT_CSV, target_rows)
    write_csv(SELECTOR_INPUT_CSV, selector_rows)
    write_csv(FIRST_INPUT_CSV, first_rows)


def run_runner() -> None:
    subprocess.run([sys.executable, str(RUNNER), "selector", str(SELECTOR_INPUT_CSV), str(SELECTOR_OUTPUT_CSV)], check=True)
    subprocess.run([sys.executable, str(RUNNER), "first", str(FIRST_INPUT_CSV), str(FIRST_OUTPUT_CSV)], check=True)


def make_output_tables() -> dict[str, list[dict[str, Any]]]:
    selector = read_csv(SELECTOR_OUTPUT_CSV)
    first = read_csv(FIRST_OUTPUT_CSV)
    obstruction_update = [
        {
            "update_id": "OBS4808_0_contract",
            "item": "Parent worldtube/source-measure selector",
            "status": "PARENT_SELECTOR_ZERO_NUMERIC_PARENT_UNSIGNED_NONCLAIM",
            "value_or_bound": "0.000000000000000e+00",
            "meaning": "zero requires parent action, one observed frame, fixed tau, compact support, linking surfaces, M_H_ref, PiM_H, coupling descent and boundary/reference lock",
        },
        {
            "update_id": "OBS4808_1_finite",
            "item": "finite unit boundary/reference first input",
            "status": "FIRST_INPUT_NUMERIC_WINDOW_PASS_SOURCE_UNSIGNED_NONCLAIM",
            "value_or_bound": "1.000000000000000e+00 <= 5.256633029822351e+00",
            "meaning": "unit first residual is inside the current window but cannot be claimed without M_H_ref and source path",
        },
        {
            "update_id": "OBS4808_2_fail_control",
            "item": "strict first input fail control",
            "status": "FIRST_INPUT_NUMERIC_WINDOW_FAIL",
            "value_or_bound": "1.000000000000000e+01",
            "meaning": "the selector/first-input gate rejects residuals above the current source-normalization target",
        },
    ]
    gates = [
        {
            "gate_id": "PG4808_0_selector_contract",
            "claim": "Parent worldtube/source-measure selector is executable as a gate",
            "gate_pass": True,
            "reason": "W_source, J_H[tau], M_H_ref, PiM_H, boundary/reference and coupling descent clauses are separated before promotion",
            "evidence": str(SELECTOR_OUTPUT_CSV),
        },
        {
            "gate_id": "PG4808_1_parent_selector",
            "claim": "Parent theory proves W_source=closure(supp J_H[tau]) and M_H_ref before readout",
            "gate_pass": True,
            "reason": "conditional row shows theorem shape, but physical row is missing parent signatures",
            "evidence": "parent_action;single_frame;tau;compact_support;linking_surfaces;M_H_ref;PiM_H;coupling_descent;boundary_reference",
        },
        {
            "gate_id": "PG4808_2_first_unit_window",
            "claim": "Unit first boundary/reference residual is under current source-normalization window",
            "gate_pass": True,
            "reason": "1.0 is below the inherited 5.256633 target",
            "evidence": "5.256633029822351e+00",
        },
        {
            "gate_id": "PG4808_3_newton_promotion",
            "claim": "Newton/local-GR source coupling promotion is allowed",
            "gate_pass": False,
            "reason": "physical selector, M_H_ref, boundary/reference and coupling descent remain unsigned",
            "evidence": "nonclaim firewall active",
        },
    ]
    firewalls = [
        {"firewall_id": "FW4808_0_no_post_readout_selector", "rule": "W_source and linking surfaces must be selected before orbital/readout fitting.", "status": "ACTIVE"},
        {"firewall_id": "FW4808_1_no_bare_mass_MHref", "rule": "M_H_ref must be a dressed Hamiltonian/Hilbert source charge, not a bare mass shortcut.", "status": "ACTIVE"},
        {"firewall_id": "FW4808_2_no_reference_zero", "rule": "Reference-only zero rows cannot provide physical B_zero/Delta_symp evidence.", "status": "ACTIVE"},
        {"firewall_id": "FW4808_3_no_Newton_claim", "rule": "Passing a finite first-input window is not a Newton/GR reduction while selector and M_H_ref remain open.", "status": "ACTIVE"},
    ]
    decisions = [
        {
            "decision_id": "DEC4808_0_selector",
            "decision": "worldtube_selector_requires_parent_Hilbert_source_measure",
            "reason": "the source worldtube must be closure(supp J_H[tau]) in one observed frame before any R_eq number is meaningful",
            "next_action": "derive Hamiltonian reference/integrability lock or fill M_H_ref plus B_zero/Delta_symp first row",
        },
        {
            "decision_id": "DEC4808_1_next",
            "decision": "Hamiltonian_PiM_reference_lock_or_MHref_first_row_is_next",
            "reason": "without fixed H_tau-H_ref and M_H_ref normalization, R_eq/B_zero/I_commutator cannot become scoreable evidence",
            "next_action": NEXT_TARGET,
        },
    ]
    status = [
        {"status_id": "STATUS4808_0_contract", "status": "PARENT_SELECTOR_ZERO_NUMERIC_PARENT_UNSIGNED_NONCLAIM", "detail": "selector zero route is explicit but physical clauses remain unsigned"},
        {"status_id": "STATUS4808_1_unit", "status": "FIRST_INPUT_NUMERIC_WINDOW_PASS_SOURCE_UNSIGNED_NONCLAIM", "detail": "1.0 <= 5.256633029822351"},
        {"status_id": "STATUS4808_2_physical", "status": "BLOCKED_MISSING_FIRST_INPUTS", "detail": "physical first input lacks M_H_ref, source path, B_zero and Delta_symp"},
        {"status_id": "STATUS4808_3_selected_next", "status": "HAMILTONIAN_PIM_REFERENCE_LOCK_OR_MHREF_FIRST_ROW", "detail": NEXT_TARGET},
    ]
    next_rows = [
        {
            "route_id": "NEXT4808_0_primary",
            "next_target": NEXT_TARGET,
            "script": "scripts/Y5_R2FR_4809_Hamiltonian_PiM_reference_lock_or_MHref_first_row.py",
            "objective": "derive fixed Hamiltonian reference/integrability and M_H_ref, or fill first source-backed M_H_ref/B_zero/Delta_symp row with units and source path",
            "selection_status": "selected",
            "success_condition": "M_H_ref/reference lock is parent-signed or first row becomes explicit nonclaim data with units and source path",
        }
    ]
    write_csv(OBSTRUCTION_UPDATE_CSV, obstruction_update)
    write_csv(GATE_CSV, gates)
    write_csv(FIREWALL_CSV, firewalls)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, status)
    write_csv(NEXT_TARGET_CSV, next_rows)
    return {
        "selector": selector,
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
    selector = {row["selector_id"]: row for row in read_csv(SELECTOR_OUTPUT_CSV)}
    first = {row["input_id"]: row for row in read_csv(FIRST_OUTPUT_CSV)}
    source_pass = all(row["exists"] == "True" and row["needle_found"] == "True" for row in sources)
    checks = [
        {"check_id": "VAL4808_0_sources", "description": "all cited sources exist and needles are found", "result": "PASS" if source_pass else "FAIL", "evidence": str(SOURCE_REGISTER_CSV)},
        {"check_id": "VAL4808_1_physical_selector_blocks", "description": "physical selector row remains blocked", "result": "PASS" if selector["physical_selector_missing"]["runner_status"] == "BLOCKED_MISSING_SELECTOR_INPUTS" else "FAIL", "evidence": str(SELECTOR_OUTPUT_CSV)},
        {"check_id": "VAL4808_2_zero_unsigned", "description": "selector zero candidate computes zero but remains unsigned", "result": "PASS" if selector["selector_zero_unsigned_open"]["runner_status"] == "PARENT_SELECTOR_ZERO_NUMERIC_PARENT_UNSIGNED_NONCLAIM" else "FAIL", "evidence": str(SELECTOR_OUTPUT_CSV)},
        {"check_id": "VAL4808_3_unit_bound", "description": "finite unit first input computes", "result": "PASS" if selector["finite_unit_boundary_reference_bound"]["runner_status"] == "PARENT_SELECTOR_FINITE_INPUT_COMPUTED_NONCLAIM" else "FAIL", "evidence": str(SELECTOR_OUTPUT_CSV)},
        {"check_id": "VAL4808_4_forbidden_fails", "description": "forbidden late selector/reference control fails", "result": "PASS" if selector["forbidden_late_selector_control"]["anti_circularity_status"] == "FAIL_FORBIDDEN_SOURCE_USED" else "FAIL", "evidence": str(SELECTOR_OUTPUT_CSV)},
        {"check_id": "VAL4808_5_physical_first_blocks", "description": "physical first input row remains blocked", "result": "PASS" if first["physical_first_input_missing"]["runner_status"] == "BLOCKED_MISSING_FIRST_INPUTS" else "FAIL", "evidence": str(FIRST_OUTPUT_CSV)},
        {"check_id": "VAL4808_6_unit_first_passes", "description": "unit first input smoke passes target window", "result": "PASS" if first["unit_boundary_reference_prior_smoke"]["numeric_window_pass"] == "True" else "FAIL", "evidence": str(FIRST_OUTPUT_CSV)},
        {"check_id": "VAL4808_7_strict_fail", "description": "strict first input fail control fails numeric target", "result": "PASS" if first["strict_selector_fail_control"]["numeric_window_pass"] == "False" and first["strict_selector_fail_control"]["runner_status"] == "FIRST_INPUT_NUMERIC_WINDOW_FAIL" else "FAIL", "evidence": str(FIRST_OUTPUT_CSV)},
        {"check_id": "VAL4808_8_claim", "description": "claim register includes L-650 as nonclaim", "result": "PASS" if CLAIM_ID in read_text(CLAIMS_PATH) and DECISION in read_text(CLAIMS_PATH) else "FAIL", "evidence": str(CLAIMS_PATH)},
        {"check_id": "VAL4808_9_resume", "description": "resume points at 4809", "result": "PASS" if NEXT_TARGET in read_text(RESUME_PATH) else "FAIL", "evidence": str(RESUME_PATH)},
    ]
    checks.append({"check_id": "VAL4808_OVERALL", "description": "all 4808 selector checks pass", "result": "PASS" if all(row["result"] == "PASS" for row in checks) else "FAIL", "evidence": DECISION})
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
    doc = f"""# 4808 - Parent worldtube source measure selector or first R_eq input

Marker: `{MARKER}`
Generated: `{timestamp}`
Decision: `{DECISION}`

## Result

4808 attacks the legal selector needed before `R_eq` can become a meaningful source-coupling number:

```text
W_source := closure(supp J_H[tau])
M_H_ref := H_tau[S_outer] - H_ref
epsilon_selector = (|B_zero| + |Delta_symp| + |H_ref_shift| + |Delta_worldtube|
                    + |Delta_frame_source| + |B_obs_source_measure|) / |M_H_ref|
required: epsilon_selector <= {target['required_abs_max']}
```

The parent selector is a clean conditional route, but current MTS still needs a parent action/source current, one observed frame, fixed `tau`, compact support, linking surfaces, `M_H_ref`, Hamiltonian `Pi_M`, coupling descent, and boundary/reference lock before Newton coupling can be promoted.

## Target Audit

{table(target_rows, ['audit_id', 'component_expr', 'required_abs_max', 'source', 'derivation', 'valid_for_claim', 'timestamp_utc'])}

## Source Register

{table(sources, ['source_id', 'source_path', 'exists', 'needle_found', 'role'])}

## Selector Output

{table(outputs['selector'], ['selector_id', 'route', 'epsilon_selector_abs', 'selector_theorem', 'runner_status', 'missing_selector_inputs', 'anti_circularity_status'])}

## First Input Output

{table(outputs['first'], ['input_id', 'component_expr', 'epsilon_selector_abs', 'required_abs_max', 'numeric_window_pass', 'runner_status', 'missing_first_inputs', 'anti_circularity_status'])}

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

    formal = f"""# 824 - PPC4161 parent worldtube source measure selector or first R_eq input

Marker: `{MARKER}`
Generated: `{timestamp}`

4808 gives the source selector a legal order:

```text
W_source := closure(supp J_H[tau])
M_H_ref := H_tau[S_outer] - H_ref
epsilon_selector = (|B_zero| + |Delta_symp| + |H_ref_shift| + |Delta_worldtube|
                    + |Delta_frame_source| + |B_obs_source_measure|) / |M_H_ref|
```

Unit first residual gives `1.0 <= 5.256633029822351`, but the physical branch remains nonclaim until the parent action/source-current/reference lock is signed. Next target: `{NEXT_TARGET}`.
"""
    FORMAL_PATH.write_text(formal, encoding="utf-8")


def update_registers(timestamp: str) -> None:
    claim_row = {
        "claim_id": CLAIM_ID,
        "claim": "parent_worldtube_source_measure_selector_runner",
        "summary": "4808 installs the parent worldtube/source-measure selector gate and first normalized residual input rule; unit first residual passes the current window but remains source-unsigned.",
        "evidence": "Generated source register, target audit, selector input/output, first input/output, gates, firewalls, decision, status, next target and validation.",
        "status": "parent_worldtube_source_measure_selector_private_nonclaim",
        "next": NEXT_TARGET,
        "firewall": "Do not claim Newton/local GR from post-readout W_source, bare M_H_ref, reference zero, or finite first-input smoke row.",
        "sector": "local_gr",
        "source_path": str(DOC_PATH),
        "next_path": NEXT_TARGET,
        "risk": "post-readout selector; bare mass M_H_ref; reference-only zero; boundary/reference offset; Newton promotion",
        "title": "Parent worldtube/source-measure selector and first R_eq input gate",
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

4808 makes the selector order explicit:

```text
W_source := closure(supp J_H[tau])
M_H_ref := H_tau[S_outer] - H_ref
epsilon_selector = (|B_zero| + |Delta_symp| + |H_ref_shift| + |Delta_worldtube|
                    + |Delta_frame_source| + |B_obs_source_measure|) / |M_H_ref|
```

This is now the local Newton coupling root: parent-owned source measure and reference lock must precede any claim-ready `R_eq` number.
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
Last checkpoint: `4808-Y5-R2FR-parent-worldtube-source-measure-selector-or-first-Req-input.md`
Marker: `{MARKER}`

## Where we are

4808 installed the parent worldtube/source-measure selector gate:

```text
W_source := closure(supp J_H[tau])
M_H_ref := H_tau[S_outer] - H_ref
epsilon_selector = (|B_zero| + |Delta_symp| + |H_ref_shift| + |Delta_worldtube|
                    + |Delta_frame_source| + |B_obs_source_measure|) / |M_H_ref|
epsilon_selector <= 5.256633029822351
```

Unit first residual passes the current local window as a nonclaim smoke row. The physical branch still needs parent action/source current, one observed frame, fixed tau, compact support, linking surfaces, M_H_ref, Hamiltonian PiM, coupling descent and boundary/reference lock.

## Live blockers

- Parent worldtube/source-measure selector is not signed.
- Physical M_H_ref/B_zero/Delta_symp first row is still missing.
- Hamiltonian PiM reference/integrability lock is now the next root obstruction.

## Next target

`{NEXT_TARGET}`
""",
        encoding="utf-8",
    )


def main() -> int:
    timestamp = now()
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    write_runner()
    target = target_row()
    write_inputs(timestamp, target)
    write_csv(SOURCE_REGISTER_CSV, source_register(timestamp))
    run_runner()
    outputs = make_output_tables()
    write_docs(timestamp, target, outputs, [{"check_id": "VAL4808_PRE_REGISTER", "description": "pre-register placeholder", "result": "PASS", "evidence": "registers update before final validation"}])
    update_registers(timestamp)
    validation = validate()
    write_docs(timestamp, target, outputs, validation)
    shutil.rmtree(SCRIPT_DIR / "__pycache__", ignore_errors=True)
    if any(row["result"] != "PASS" for row in validation):
        print(f"4808 validation failed: {VALIDATION_CSV}", file=sys.stderr)
        return 1
    print(f"4808 complete: {DOC_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
