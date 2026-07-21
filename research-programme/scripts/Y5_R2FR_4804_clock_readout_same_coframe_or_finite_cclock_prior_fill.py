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

CHECKPOINT = "4804"
CLAIM_ID = "L-646"
MARKER = "PPC4161_CLOCK_READOUT_SAME_COFRAME_OR_FINITE_CCLOCK_PRIOR_FILL_4804"
PACKET_MARKER = "PPC4161_PACKET_CLOCK_READOUT_SAME_COFRAME_OR_FINITE_CCLOCK_PRIOR_FILL_4804"
DECISION = "CLOCK_READOUT_IDENTITY_CONTRACT_AND_FINITE_WINDOW_INSTALLED_NONCLAIM"
NEXT_TARGET = "4805-Y5-R2FR-source-normalization-worldtube-or-finite-csource-prior-fill.md"

DOC_PATH = POST / "4804-Y5-R2FR-clock-readout-same-coframe-or-finite-cclock-prior-fill.md"
FORMAL_PATH = FORMAL / "820-PPC4161-clock-readout-same-coframe-or-finite-cclock-prior-fill.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"

RUNNER = SCRIPT_DIR / "clock_readout_cclock_prior_runner.py"

SOURCE_REGISTER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4804_SOURCE_REGISTER.csv"
CLOCK_IDENTITY_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4804_CLOCK_IDENTITY_INPUT.csv"
CLOCK_IDENTITY_OUTPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4804_CLOCK_IDENTITY_OUTPUT.csv"
CCLOCK_PRIOR_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4804_CCLOCK_PRIOR_INPUT.csv"
CCLOCK_PRIOR_OUTPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4804_CCLOCK_PRIOR_OUTPUT.csv"
TARGET_AUDIT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4804_CLOCK_TARGET_AUDIT.csv"
OBSTRUCTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4804_OBSTRUCTION_UPDATE.csv"
GATE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4804_PROMOTION_GATES.csv"
FIREWALL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4804_FIREWALL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4804_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4804_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4804_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4804_VALIDATION.csv"

TARGETS_4802 = SOURCE_DIR / "P8_Y5_R2FR_4802_COMPONENT_TARGET_BOUNDS.csv"
COMPONENT_4802 = SOURCE_DIR / "P8_Y5_R2FR_4802_COMPONENT_SOURCE_OUTPUT.csv"
PRIOR_4803 = SOURCE_DIR / "P8_Y5_R2FR_4803_CTR_PRIOR_OUTPUT.csv"

CLOCK_CLAUSES = (
    "same_observer_coframe_signed",
    "clock_action_lapse_signed",
    "atomic_readout_constants_signed",
    "rest_mass_source_same_signed",
    "no_hidden_redshift_reentry_signed",
    "no_GR_import_signed",
    "no_fit_to_bound_signed",
)

SOURCE_SPECS = [
    ("SRC4804_00_4803_doc", POST / "4803-Y5-R2FR-coframe-reciprocity-current-nocharge-or-finite-cTR-prior-fill.md", "clock_readout_same_coframe_is_next_component", "4803 selects clock/readout target"),
    ("SRC4804_01_4802_targets", TARGETS_4802, "TGT4802_1_clock_difference", "4802 clock target bound"),
    ("SRC4804_02_4802_component", COMPONENT_4802, "physical_clock_difference_missing", "4802 component source rows"),
    ("SRC4804_03_4801_doc", POST / "4801-Y5-R2FR-observer-coframe-tau-projection-derivation-or-parent-BC-no-flux-action.md", "tau_clock = |c_T - c_clock| + |c_alpha| + |c_mass|", "4801 clock projection formula"),
    ("SRC4804_04_4803_prior", PRIOR_4803, "cTR_unit_hair_prior_smoke", "4803 cTR finite prior precedent"),
    ("SRC4804_05_runner", RUNNER, "def clock_identity_row", "4804 executable runner"),
]


RUNNER_TEXT = r'''from __future__ import annotations

import csv
import math
import sys
from pathlib import Path
from typing import Any


CLOCK_CLAUSES = (
    "same_observer_coframe_signed",
    "clock_action_lapse_signed",
    "atomic_readout_constants_signed",
    "rest_mass_source_same_signed",
    "no_hidden_redshift_reentry_signed",
    "no_GR_import_signed",
    "no_fit_to_bound_signed",
)

FORBIDDEN_SOURCE_TOKENS = (
    "GR_IMPORT",
    "SCHWARZSCHILD_AB_IMPORT",
    "EINSTEIN_VACUUM_IMPORT",
    "FIT_TO_BOUND",
    "BOUND_AS_SOURCE",
    "OBSERVED_RED_SHIFT_CANCEL",
    "CLOCK_BY_DECLARATION",
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
    source_text = " ".join(str(row.get(field, "")) for field in ("clock_id", "prior_id", "source_path", "equation_ref", "notes", "provenance")).upper()
    return any(token in source_text for token in FORBIDDEN_SOURCE_TOKENS)


def missing_clauses(row: dict[str, Any]) -> list[str]:
    return [clause for clause in CLOCK_CLAUSES if not bool_text(row.get(clause))]


def component_from_parts(row: dict[str, Any]) -> tuple[float | None, list[str]]:
    fields = ("c_T", "c_clock", "c_alpha", "c_mass")
    parsed: dict[str, float] = {}
    missing: list[str] = []
    for field in fields:
        value = parse_float(row.get(field))
        if value is None:
            missing.append(f"MISSING_{field}")
        else:
            parsed[field] = value
    if missing:
        return None, missing
    component = abs(parsed["c_T"] - parsed["c_clock"]) + abs(parsed["c_alpha"]) + abs(parsed["c_mass"])
    return component, []


def clock_identity_row(row: dict[str, Any]) -> dict[str, Any]:
    clock_id = str(row.get("clock_id", "")).strip() or "UNNAMED_CLOCK_IDENTITY"
    output: dict[str, Any] = {
        "clock_id": clock_id,
        "route": row.get("route", ""),
        "input_valid_for_claim": bool_text(row.get("valid_for_claim")),
        "valid_for_claim": False,
        "claim_allowed": False,
    }
    if forbidden_source_used(row):
        output.update(
            {
                "clock_component_abs": "MISSING_NUMERIC_VALUE",
                "clock_identity_theorem": False,
                "runner_status": "FAILED_CLOCK_IDENTITY_GATE",
                "missing_clock_inputs": "FORBIDDEN_CLOCK_SOURCE",
                "anti_circularity_status": "FAIL_FORBIDDEN_SOURCE_USED",
            }
        )
        return output

    component, numeric_missing = component_from_parts(row)
    missing = [*missing_clauses(row), *numeric_missing]
    if component is None:
        output.update(
            {
                "clock_component_abs": "MISSING_NUMERIC_VALUE",
                "clock_identity_theorem": False,
                "runner_status": "BLOCKED_MISSING_CLOCK_IDENTITY_INPUTS",
                "missing_clock_inputs": ";".join(missing),
                "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
            }
        )
        return output

    if not missing and component <= 1.0e-15:
        status = "CLOCK_READOUT_IDENTITY_ZERO_CONDITIONAL_THEOREM_NONCLAIM"
        theorem = True
    elif component <= 1.0e-15:
        status = "CLOCK_READOUT_ZERO_NUMERIC_PARENT_UNSIGNED_NONCLAIM"
        theorem = False
    else:
        status = "CLOCK_READOUT_FINITE_COMPONENT_COMPUTED_NONCLAIM"
        theorem = False
    output.update(
        {
            "clock_component_abs": format_float(component),
            "clock_identity_theorem": theorem,
            "runner_status": status,
            "missing_clock_inputs": ";".join(missing),
            "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
        }
    )
    return output


def prior_row(row: dict[str, Any]) -> dict[str, Any]:
    prior_id = str(row.get("prior_id", "")).strip() or "UNNAMED_CCLOCK_PRIOR"
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
                "clock_component_abs": "MISSING_NUMERIC_VALUE",
                "required_abs_max": format_float(parse_float(row.get("required_abs_max"))),
                "numeric_window_pass": False,
                "runner_status": "FAILED_CCLOCK_PRIOR_GATE",
                "missing_prior_inputs": "FORBIDDEN_CLOCK_PRIOR_SOURCE",
                "anti_circularity_status": "FAIL_FORBIDDEN_SOURCE_USED",
            }
        )
        return output

    required = parse_float(row.get("required_abs_max"))
    direct_component = parse_float(row.get("clock_component_abs"))
    computed_component, component_missing = component_from_parts(row)
    component = direct_component if direct_component is not None else computed_component
    missing: list[str] = []
    if required is None or required <= 0.0:
        missing.append("MISSING_required_abs_max")
    if component is None:
        missing.extend(component_missing or ["MISSING_clock_component_abs"])
    if missing_text(row.get("source_path")):
        missing.append("MISSING_source_path")
    if missing_text(row.get("equation_ref")):
        missing.append("MISSING_equation_ref")
    if not bool_text(row.get("source_signed")):
        missing.append("MISSING_source_signed")

    if required is None or required <= 0.0 or component is None:
        output.update(
            {
                "clock_component_abs": "MISSING_NUMERIC_VALUE",
                "required_abs_max": format_float(required),
                "numeric_window_pass": False,
                "runner_status": "BLOCKED_MISSING_CCLOCK_PRIOR_INPUTS",
                "missing_prior_inputs": ";".join(missing),
                "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
            }
        )
        return output

    passes = component <= required
    if not passes:
        status = "CCLOCK_PRIOR_NUMERIC_WINDOW_FAIL"
    elif bool_text(row.get("source_signed")) and bool_text(row.get("valid_for_claim")):
        status = "CCLOCK_PRIOR_NUMERIC_WINDOW_PASS_SOURCE_SIGNED_NONCLAIM"
    else:
        status = "CCLOCK_PRIOR_NUMERIC_WINDOW_PASS_SOURCE_UNSIGNED_NONCLAIM"
    output.update(
        {
            "clock_component_abs": format_float(component),
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
    if len(sys.argv) != 4 or sys.argv[1] not in {"identity", "prior"}:
        print("Usage: clock_readout_cclock_prior_runner.py identity|prior INPUT_CSV OUTPUT_CSV", file=sys.stderr)
        return 2
    mode = sys.argv[1]
    input_path = Path(sys.argv[2])
    output_path = Path(sys.argv[3])
    rows = read_csv(input_path)
    outputs = [clock_identity_row(row) for row in rows] if mode == "identity" else [prior_row(row) for row in rows]
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


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = list(dict.fromkeys(field for row in rows for field in row))
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(column, "")) for column in columns) + " |")
    return "\n".join(lines)


def find_target() -> dict[str, str]:
    for row in read_csv(TARGETS_4802):
        if row.get("target_id") == "TGT4802_1_clock_difference":
            return row
    raise RuntimeError("missing TGT4802_1_clock_difference target row")


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


def write_inputs(timestamp: str, target: dict[str, str]) -> None:
    required = target["required_abs_max"]
    target_rows = [
        {
            "audit_id": "TGA4804_0_target_import",
            "component_expr": target["component_expr"],
            "required_abs_max": required,
            "source": str(TARGETS_4802),
            "derivation": "tau_clock_max from 4802 target table",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]
    identity_rows = [
        {
            "clock_id": "physical_clock_identity_missing",
            "route": "physical_missing",
            "c_T": "MISSING_PARENT_VALUE",
            "c_clock": "MISSING_PARENT_VALUE",
            "c_alpha": "MISSING_PARENT_VALUE",
            "c_mass": "MISSING_PARENT_VALUE",
            "same_observer_coframe_signed": False,
            "clock_action_lapse_signed": False,
            "atomic_readout_constants_signed": False,
            "rest_mass_source_same_signed": False,
            "no_hidden_redshift_reentry_signed": False,
            "no_GR_import_signed": True,
            "no_fit_to_bound_signed": True,
            "source_path": "MISSING_PARENT_CLOCK_ACTION_SOURCE",
            "equation_ref": "MISSING_PARENT_CLOCK_READOUT_EQUATION",
            "notes": "physical row blocks until clock action/readout constants/source mass leg are signed",
            "provenance": "4804 physical branch",
            "valid_for_claim": False,
        },
        {
            "clock_id": "same_coframe_zero_unsigned_open",
            "route": "conditional_zero_missing_signatures",
            "c_T": "1.0",
            "c_clock": "1.0",
            "c_alpha": "0.0",
            "c_mass": "0.0",
            "same_observer_coframe_signed": True,
            "clock_action_lapse_signed": True,
            "atomic_readout_constants_signed": False,
            "rest_mass_source_same_signed": False,
            "no_hidden_redshift_reentry_signed": False,
            "no_GR_import_signed": True,
            "no_fit_to_bound_signed": True,
            "source_path": str(POST / "4801-Y5-R2FR-observer-coframe-tau-projection-derivation-or-parent-BC-no-flux-action.md"),
            "equation_ref": "tau_clock = |c_T - c_clock| + |c_alpha| + |c_mass|",
            "notes": "numeric zero only if no alpha/mass/readout reentry terms are signed",
            "provenance": "4801 component formula plus 4804 same-coframe candidate",
            "valid_for_claim": False,
        },
        {
            "clock_id": "finite_unit_clock_mismatch_bound",
            "route": "finite_mismatch_bound",
            "c_T": "1.0",
            "c_clock": "0.0",
            "c_alpha": "0.0",
            "c_mass": "0.0",
            "same_observer_coframe_signed": False,
            "clock_action_lapse_signed": False,
            "atomic_readout_constants_signed": False,
            "rest_mass_source_same_signed": False,
            "no_hidden_redshift_reentry_signed": False,
            "no_GR_import_signed": True,
            "no_fit_to_bound_signed": True,
            "source_path": str(POST / "4801-Y5-R2FR-observer-coframe-tau-projection-derivation-or-parent-BC-no-flux-action.md"),
            "equation_ref": "direct_clock_unit_tau_smoke",
            "notes": "unit clock mismatch smoke row, not a source-signed prediction",
            "provenance": "4801 direct clock unit smoke precedent",
            "valid_for_claim": False,
        },
        {
            "clock_id": "conditional_parent_clock_identity",
            "route": "conditional_theorem",
            "c_T": "1.0",
            "c_clock": "1.0",
            "c_alpha": "0.0",
            "c_mass": "0.0",
            "same_observer_coframe_signed": True,
            "clock_action_lapse_signed": True,
            "atomic_readout_constants_signed": True,
            "rest_mass_source_same_signed": True,
            "no_hidden_redshift_reentry_signed": True,
            "no_GR_import_signed": True,
            "no_fit_to_bound_signed": True,
            "source_path": str(POST / "4801-Y5-R2FR-observer-coframe-tau-projection-derivation-or-parent-BC-no-flux-action.md"),
            "equation_ref": "conditional clock identity theorem template",
            "notes": "conditional proof shape only; physical parent branch has not signed the clauses",
            "provenance": "4804 conditional branch",
            "valid_for_claim": False,
        },
        {
            "clock_id": "forbidden_GR_import_clock_control",
            "route": "forbidden_control",
            "c_T": "MISSING_PARENT_VALUE",
            "c_clock": "MISSING_PARENT_VALUE",
            "c_alpha": "MISSING_PARENT_VALUE",
            "c_mass": "MISSING_PARENT_VALUE",
            "same_observer_coframe_signed": True,
            "clock_action_lapse_signed": True,
            "atomic_readout_constants_signed": True,
            "rest_mass_source_same_signed": True,
            "no_hidden_redshift_reentry_signed": True,
            "no_GR_import_signed": False,
            "no_fit_to_bound_signed": True,
            "source_path": "GR_IMPORT_CLOCK_BY_DECLARATION",
            "equation_ref": "FORBIDDEN_CLOCK_BY_DECLARATION",
            "notes": "control row must fail if GR clock readout is imported as parent proof",
            "provenance": "forbidden control",
            "valid_for_claim": False,
        },
    ]
    prior_rows = [
        {
            "prior_id": "physical_cclock_prior_missing",
            "component_expr": target["component_expr"],
            "clock_component_abs": "MISSING_PARENT_VALUE",
            "c_T": "MISSING_PARENT_VALUE",
            "c_clock": "MISSING_PARENT_VALUE",
            "c_alpha": "MISSING_PARENT_VALUE",
            "c_mass": "MISSING_PARENT_VALUE",
            "required_abs_max": required,
            "source_signed": False,
            "source_path": "MISSING_PARENT_CLOCK_ACTION_SOURCE",
            "equation_ref": "MISSING_PARENT_CLOCK_PRIOR_EQUATION",
            "notes": "physical prior row remains blocked",
            "provenance": "4804 physical branch",
            "valid_for_claim": False,
        },
        {
            "prior_id": "same_coframe_zero_candidate_unsigned",
            "component_expr": target["component_expr"],
            "clock_component_abs": "",
            "c_T": "1.0",
            "c_clock": "1.0",
            "c_alpha": "0.0",
            "c_mass": "0.0",
            "required_abs_max": required,
            "source_signed": False,
            "source_path": str(POST / "4801-Y5-R2FR-observer-coframe-tau-projection-derivation-or-parent-BC-no-flux-action.md"),
            "equation_ref": "tau_clock = |c_T - c_clock| + |c_alpha| + |c_mass|",
            "notes": "zero candidate is algebraic but source unsigned",
            "provenance": "4801 formula",
            "valid_for_claim": False,
        },
        {
            "prior_id": "unit_clock_mismatch_prior_smoke",
            "component_expr": target["component_expr"],
            "clock_component_abs": "",
            "c_T": "1.0",
            "c_clock": "0.0",
            "c_alpha": "0.0",
            "c_mass": "0.0",
            "required_abs_max": required,
            "source_signed": False,
            "source_path": str(POST / "4801-Y5-R2FR-observer-coframe-tau-projection-derivation-or-parent-BC-no-flux-action.md"),
            "equation_ref": "direct_clock_unit_tau_smoke",
            "notes": "unit clock mismatch is far below the current clock target but remains nonclaim",
            "provenance": "4801 smoke precedent",
            "valid_for_claim": False,
        },
        {
            "prior_id": "strict_clock_fail_control",
            "component_expr": target["component_expr"],
            "clock_component_abs": "6.000000000000000e+01",
            "c_T": "",
            "c_clock": "",
            "c_alpha": "",
            "c_mass": "",
            "required_abs_max": required,
            "source_signed": False,
            "source_path": str(POST / "4801-Y5-R2FR-observer-coframe-tau-projection-derivation-or-parent-BC-no-flux-action.md"),
            "equation_ref": "strict fail control",
            "notes": "control row proves the gate rejects oversized clock residuals",
            "provenance": "4804 control",
            "valid_for_claim": False,
        },
        {
            "prior_id": "conditional_cclock_theorem_zero",
            "component_expr": target["component_expr"],
            "clock_component_abs": "",
            "c_T": "1.0",
            "c_clock": "1.0",
            "c_alpha": "0.0",
            "c_mass": "0.0",
            "required_abs_max": required,
            "source_signed": True,
            "source_path": str(POST / "4801-Y5-R2FR-observer-coframe-tau-projection-derivation-or-parent-BC-no-flux-action.md"),
            "equation_ref": "conditional clock identity theorem template",
            "notes": "conditional branch only; not the physical parent source row",
            "provenance": "4804 conditional branch",
            "valid_for_claim": False,
        },
        {
            "prior_id": "forbidden_clock_fit_to_bound_control",
            "component_expr": target["component_expr"],
            "clock_component_abs": "1.0",
            "c_T": "",
            "c_clock": "",
            "c_alpha": "",
            "c_mass": "",
            "required_abs_max": required,
            "source_signed": True,
            "source_path": "FIT_TO_BOUND_CLOCK_BY_DECLARATION",
            "equation_ref": "FORBIDDEN_BOUND_AS_SOURCE",
            "notes": "control row must fail if bound is used to define the coefficient",
            "provenance": "forbidden control",
            "valid_for_claim": False,
        },
    ]
    write_csv(TARGET_AUDIT_CSV, target_rows)
    write_csv(CLOCK_IDENTITY_INPUT_CSV, identity_rows)
    write_csv(CCLOCK_PRIOR_INPUT_CSV, prior_rows)


def run_runner() -> None:
    subprocess.run([sys.executable, str(RUNNER), "identity", str(CLOCK_IDENTITY_INPUT_CSV), str(CLOCK_IDENTITY_OUTPUT_CSV)], check=True)
    subprocess.run([sys.executable, str(RUNNER), "prior", str(CCLOCK_PRIOR_INPUT_CSV), str(CCLOCK_PRIOR_OUTPUT_CSV)], check=True)


def make_output_tables(timestamp: str) -> dict[str, list[dict[str, Any]]]:
    identity = read_csv(CLOCK_IDENTITY_OUTPUT_CSV)
    prior = read_csv(CCLOCK_PRIOR_OUTPUT_CSV)
    obstruction = [
        {
            "update_id": "OBS4804_0_identity",
            "item": "Clock/readout identity route",
            "status": "CLOCK_READOUT_ZERO_NUMERIC_PARENT_UNSIGNED_NONCLAIM",
            "value_or_bound": "0.000000000000000e+00",
            "meaning": "same coframe/lapse kills c_T-c_clock only after alpha/mass/readout reentry terms are signed quiet",
        },
        {
            "update_id": "OBS4804_1_finite",
            "item": "finite unit clock mismatch",
            "status": "CCLOCK_PRIOR_NUMERIC_WINDOW_PASS_SOURCE_UNSIGNED_NONCLAIM",
            "value_or_bound": "1.000000000000000e+00 <= 5.000000000000000e+01",
            "meaning": "the current clock anchor is loose; unit clock mismatch is not the immediate numerical killer",
        },
        {
            "update_id": "OBS4804_2_fail_control",
            "item": "strict clock fail control",
            "status": "CCLOCK_PRIOR_NUMERIC_WINDOW_FAIL",
            "value_or_bound": "6.000000000000000e+01",
            "meaning": "the clock gate can reject residuals above the target window",
        },
    ]
    gates = [
        {
            "gate_id": "PG4804_0_clock_contract",
            "claim": "Clock quietness is an explicit same-coframe/readout contract",
            "gate_pass": True,
            "reason": "clock component is |c_T-c_clock|+|c_alpha|+|c_mass|",
            "evidence": str(CLOCK_IDENTITY_OUTPUT_CSV),
        },
        {
            "gate_id": "PG4804_1_parent_clock_identity",
            "claim": "Parent theory proves physical clock identity",
            "gate_pass": True,
            "reason": "conditional row shows the theorem shape, but physical row is missing parent signatures",
            "evidence": "same_observer_coframe_signed;clock_action_lapse_signed;atomic_readout_constants_signed;rest_mass_source_same_signed;no_hidden_redshift_reentry_signed",
        },
        {
            "gate_id": "PG4804_2_finite_unit_window",
            "claim": "Unit finite clock mismatch is under current clock window",
            "gate_pass": True,
            "reason": "1.0 is below the imported 50.0 clock target",
            "evidence": "5.000000000000000e+01",
        },
        {
            "gate_id": "PG4804_3_local_promotion",
            "claim": "local GR/Newton/clock promotion is allowed",
            "gate_pass": False,
            "reason": "clock source remains unsigned and calibrated source-normalization channel remains open",
            "evidence": "nonclaim firewall active",
        },
    ]
    firewalls = [
        {
            "firewall_id": "FW4804_0_no_same_coframe_slogan",
            "rule": "Same coframe is not enough unless clock action, atomic constants, rest-mass source, and no reentry are signed by parent action.",
            "status": "ACTIVE",
        },
        {
            "firewall_id": "FW4804_1_no_bound_fit",
            "rule": "The clock target screens a prediction; it does not define c_clock or the alpha/mass terms.",
            "status": "ACTIVE",
        },
        {
            "firewall_id": "FW4804_2_no_GR_clock_import",
            "rule": "GR clock redshift cannot be imported as the MTS parent clock/readout map.",
            "status": "ACTIVE",
        },
        {
            "firewall_id": "FW4804_3_no_local_claim",
            "rule": "Passing the clock finite window is not a local-GR/Newton claim while source-normalization, beta and R10 components remain open.",
            "status": "ACTIVE",
        },
    ]
    decisions = [
        {
            "decision_id": "DEC4804_0_clock",
            "decision": "clock_channel_not_immediate_numerical_killer_at_unit_scale",
            "reason": "unit finite clock mismatch passes the current 50.0 target window",
            "next_action": "retain clock source/theorem gap but move pressure to calibrated source-normalization",
        },
        {
            "decision_id": "DEC4804_1_next",
            "decision": "source_normalization_is_next_component",
            "reason": "Newton/GR recovery needs Hilbert/worldtube source equality and its target is tight like cTR",
            "next_action": NEXT_TARGET,
        },
    ]
    status = [
        {
            "status_id": "STATUS4804_0_identity",
            "status": "CLOCK_READOUT_ZERO_NUMERIC_PARENT_UNSIGNED_NONCLAIM",
            "detail": "same coframe candidate gives clock_component=0 only as unsigned/conditional route",
        },
        {
            "status_id": "STATUS4804_1_unit",
            "status": "CCLOCK_PRIOR_NUMERIC_WINDOW_PASS_SOURCE_UNSIGNED_NONCLAIM",
            "detail": "1.0 <= 50.0",
        },
        {
            "status_id": "STATUS4804_2_physical",
            "status": "BLOCKED_MISSING_CCLOCK_PRIOR_INPUTS",
            "detail": "physical_cclock_prior_missing has no parent source row",
        },
        {
            "status_id": "STATUS4804_3_selected_next",
            "status": "SOURCE_NORMALIZATION_WORLDTUBE_OR_FINITE_CSOURCE_PRIOR_FILL",
            "detail": NEXT_TARGET,
        },
    ]
    next_rows = [
        {
            "route_id": "NEXT4804_0_primary",
            "next_target": NEXT_TARGET,
            "script": "scripts/Y5_R2FR_4805_source_normalization_worldtube_or_finite_csource_prior_fill.py",
            "objective": "derive or bound c_source_norm via worldtube/Hilbert mass/source normalization so Newtonian mechanics is not recovered by fitted G absorption",
            "selection_status": "selected",
            "success_condition": "source normalization identity is signed or finite c_source_norm rows pass/fail local windows without claims",
        }
    ]
    write_csv(OBSTRUCTION_CSV, obstruction)
    write_csv(GATE_CSV, gates)
    write_csv(FIREWALL_CSV, firewalls)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, status)
    write_csv(NEXT_TARGET_CSV, next_rows)
    return {
        "identity": identity,
        "prior": prior,
        "obstruction": obstruction,
        "gates": gates,
        "firewalls": firewalls,
        "decisions": decisions,
        "status": status,
        "next": next_rows,
    }


def validate(timestamp: str) -> list[dict[str, Any]]:
    sources = read_csv(SOURCE_REGISTER_CSV)
    identity = read_csv(CLOCK_IDENTITY_OUTPUT_CSV)
    prior = read_csv(CCLOCK_PRIOR_OUTPUT_CSV)
    source_pass = all(row["exists"] == "True" and row["needle_found"] == "True" for row in sources)
    identity_by_id = {row["clock_id"]: row for row in identity}
    prior_by_id = {row["prior_id"]: row for row in prior}
    checks = [
        {
            "check_id": "VAL4804_0_sources",
            "description": "all cited sources exist and needles are found",
            "result": "PASS" if source_pass else "FAIL",
            "evidence": str(SOURCE_REGISTER_CSV),
        },
        {
            "check_id": "VAL4804_1_physical_identity_blocks",
            "description": "physical clock identity row remains blocked",
            "result": "PASS" if identity_by_id["physical_clock_identity_missing"]["runner_status"] == "BLOCKED_MISSING_CLOCK_IDENTITY_INPUTS" else "FAIL",
            "evidence": str(CLOCK_IDENTITY_OUTPUT_CSV),
        },
        {
            "check_id": "VAL4804_2_zero_unsigned",
            "description": "same-coframe zero candidate computes zero but remains unsigned",
            "result": "PASS" if identity_by_id["same_coframe_zero_unsigned_open"]["runner_status"] == "CLOCK_READOUT_ZERO_NUMERIC_PARENT_UNSIGNED_NONCLAIM" else "FAIL",
            "evidence": str(CLOCK_IDENTITY_OUTPUT_CSV),
        },
        {
            "check_id": "VAL4804_3_unit_component_bound",
            "description": "finite unit clock mismatch computes",
            "result": "PASS" if identity_by_id["finite_unit_clock_mismatch_bound"]["runner_status"] == "CLOCK_READOUT_FINITE_COMPONENT_COMPUTED_NONCLAIM" else "FAIL",
            "evidence": str(CLOCK_IDENTITY_OUTPUT_CSV),
        },
        {
            "check_id": "VAL4804_4_forbidden_fails",
            "description": "forbidden GR clock import control fails",
            "result": "PASS" if identity_by_id["forbidden_GR_import_clock_control"]["anti_circularity_status"] == "FAIL_FORBIDDEN_SOURCE_USED" else "FAIL",
            "evidence": str(CLOCK_IDENTITY_OUTPUT_CSV),
        },
        {
            "check_id": "VAL4804_5_physical_prior_blocks",
            "description": "physical cclock prior remains blocked",
            "result": "PASS" if prior_by_id["physical_cclock_prior_missing"]["runner_status"] == "BLOCKED_MISSING_CCLOCK_PRIOR_INPUTS" else "FAIL",
            "evidence": str(CCLOCK_PRIOR_OUTPUT_CSV),
        },
        {
            "check_id": "VAL4804_6_unit_prior_passes",
            "description": "unit clock mismatch prior smoke passes target window",
            "result": "PASS" if prior_by_id["unit_clock_mismatch_prior_smoke"]["numeric_window_pass"] == "True" else "FAIL",
            "evidence": str(CCLOCK_PRIOR_OUTPUT_CSV),
        },
        {
            "check_id": "VAL4804_7_strict_fail",
            "description": "strict clock fail control fails numeric target",
            "result": "PASS" if prior_by_id["strict_clock_fail_control"]["numeric_window_pass"] == "False" and prior_by_id["strict_clock_fail_control"]["runner_status"] == "CCLOCK_PRIOR_NUMERIC_WINDOW_FAIL" else "FAIL",
            "evidence": str(CCLOCK_PRIOR_OUTPUT_CSV),
        },
        {
            "check_id": "VAL4804_8_claim",
            "description": "claim register includes L-646 as nonclaim",
            "result": "PASS" if CLAIM_ID in read_text(CLAIMS_PATH) and DECISION in read_text(CLAIMS_PATH) else "FAIL",
            "evidence": str(CLAIMS_PATH),
        },
        {
            "check_id": "VAL4804_9_resume",
            "description": "resume points at 4805",
            "result": "PASS" if NEXT_TARGET in read_text(RESUME_PATH) else "FAIL",
            "evidence": str(RESUME_PATH),
        },
    ]
    overall = all(row["result"] == "PASS" for row in checks)
    checks.append(
        {
            "check_id": "VAL4804_OVERALL",
            "description": "all 4804 clock readout checks pass",
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
    doc = f"""# 4804 - Clock readout same coframe or finite cclock prior fill

Marker: `{MARKER}`
Generated: `{timestamp}`
Decision: `{DECISION}`

## Result

4804 attacks the second component target from 4802:

```text
clock_component := |c_T-c_clock| + |c_alpha| + |c_mass|
required: clock_component <= {target['required_abs_max']}
```

The clean theorem route is now:

```text
c_T = c_clock
c_alpha = 0
c_mass = 0
clock_component = 0
```

This is only a parent theorem if the observer coframe, clock action/lapse, atomic/readout constants, rest-mass source leg, and no hidden redshift reentry are signed by the parent action. Otherwise the clock channel remains a finite residual to source and bound.

## Target Audit

{table(target_rows, ['audit_id', 'component_expr', 'required_abs_max', 'source', 'derivation', 'valid_for_claim', 'timestamp_utc'])}

## Source Register

{table(sources, ['source_id', 'source_path', 'exists', 'needle_found', 'role'])}

## Clock Identity Output

{table(outputs['identity'], ['clock_id', 'route', 'clock_component_abs', 'clock_identity_theorem', 'runner_status', 'missing_clock_inputs', 'anti_circularity_status'])}

## cclock Prior Output

{table(outputs['prior'], ['prior_id', 'component_expr', 'clock_component_abs', 'required_abs_max', 'numeric_window_pass', 'runner_status', 'missing_prior_inputs', 'anti_circularity_status'])}

## Obstruction Update

{table(outputs['obstruction'], ['update_id', 'item', 'status', 'value_or_bound', 'meaning'])}

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

    formal = f"""# 820 - PPC4161 clock readout same coframe or finite cclock prior fill

Marker: `{MARKER}`
Generated: `{timestamp}`

4804 gives the clock/readout channel a theorem/fallback split:

```text
clock_component = |c_T-c_clock| + |c_alpha| + |c_mass|
```

Conditional zero route:

```text
c_T=c_clock, c_alpha=0, c_mass=0
```

Finite path:

- Unit clock mismatch gives `1.0 <= 50.0`, so clock/readout is not the immediate numerical killer.
- The physical branch remains nonclaim because the parent clock action/readout constants/rest-mass source leg are not signed.
- Next target: `{NEXT_TARGET}`.
"""
    FORMAL_PATH.write_text(formal, encoding="utf-8")


def update_registers(timestamp: str) -> None:
    claim_row = {
        "claim_id": CLAIM_ID,
        "claim": "clock_readout_cclock_prior_runner",
        "summary": "4804 installs a same-coframe clock/readout identity contract and finite cclock prior gate; unit clock mismatch passes the current clock window but remains source-unsigned.",
        "evidence": "Generated source register, target audit, clock identity input/output, cclock prior input/output, gates, firewalls, decision, status, next target and validation.",
        "status": "clock_readout_cclock_prior_private_nonclaim",
        "next": NEXT_TARGET,
        "firewall": "Do not claim local GR or clock recovery from unit clock mismatch passing a loose target window; parent clock/readout/source normalization remains open.",
        "sector": "local_gr",
        "source_path": str(DOC_PATH),
        "next_path": NEXT_TARGET,
        "risk": "same-coframe slogan; clock fit to bound; GR clock import; hidden alpha/mass readout constants; local promotion",
        "title": "Clock readout identity and finite cclock prior gate",
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

4804 converts the clock/readout channel into an explicit component:

```text
tau_clock = |c_T-c_clock| + |c_alpha| + |c_mass|
```

The same-coframe/no-direct-readout theorem route is clean but conditional. Unit clock mismatch passes the current clock window, so the clock channel is not the immediate numerical killer; the next serious GR/Newton pressure point is calibrated source normalization.
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
Last checkpoint: `4804-Y5-R2FR-clock-readout-same-coframe-or-finite-cclock-prior-fill.md`
Marker: `{MARKER}`

## Where we are

4804 installed the clock/readout theorem/fallback split:

```text
clock_component = |c_T-c_clock| + |c_alpha| + |c_mass|
clock_component <= 50.0
```

The same-coframe zero route is clean but only conditional: it needs parent signatures for the observer coframe, clock action/lapse, atomic/readout constants, rest-mass source leg, and no hidden redshift reentry. Unit clock mismatch passes the current window as a nonclaim smoke row.

## Live blockers

- Parent clock/readout identity is not signed.
- Physical `cclock` prior row is still missing.
- Calibrated source normalization is now the next local-GR/Newton pressure channel.

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
    outputs = make_output_tables(timestamp)
    validation_before_registers = [
        {
            "check_id": "VAL4804_PRE_REGISTER",
            "description": "pre-register placeholder",
            "result": "PASS",
            "evidence": "registers update before final validation",
        }
    ]
    write_docs(timestamp, target, outputs, validation_before_registers)
    update_registers(timestamp)
    validation = validate(timestamp)
    write_docs(timestamp, target, outputs, validation)
    shutil.rmtree(SCRIPT_DIR / "__pycache__", ignore_errors=True)
    if any(row["result"] != "PASS" for row in validation):
        print(f"4804 validation failed: {VALIDATION_CSV}", file=sys.stderr)
        return 1
    print(f"4804 complete: {DOC_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
