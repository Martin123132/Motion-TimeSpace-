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

CHECKPOINT = "4803"
CLAIM_ID = "L-645"
MARKER = "PPC4161_COFRAME_RECIPROCITY_CURRENT_NOCHARGE_OR_FINITE_CTR_PRIOR_FILL_4803"
PACKET_MARKER = "PPC4161_PACKET_COFRAME_RECIPROCITY_CURRENT_NOCHARGE_OR_FINITE_CTR_PRIOR_FILL_4803"
DECISION = "CTR_GAUSS_NOCHARGE_CONTRACT_AND_FINITE_PRIOR_WINDOW_INSTALLED_NONCLAIM"
NEXT_TARGET = "4804-Y5-R2FR-clock-readout-same-coframe-or-finite-cclock-prior-fill.md"

DOC_PATH = POST / "4803-Y5-R2FR-coframe-reciprocity-current-nocharge-or-finite-cTR-prior-fill.md"
FORMAL_PATH = FORMAL / "819-PPC4161-coframe-reciprocity-current-nocharge-or-finite-cTR-prior-fill.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"

RUNNER = SCRIPT_DIR / "coframe_cTR_nocharge_prior_runner.py"

SOURCE_REGISTER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4803_SOURCE_REGISTER.csv"
NOCHARGE_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4803_NOCHARGE_INPUT.csv"
NOCHARGE_OUTPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4803_NOCHARGE_OUTPUT.csv"
CTR_PRIOR_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4803_CTR_PRIOR_INPUT.csv"
CTR_PRIOR_OUTPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4803_CTR_PRIOR_OUTPUT.csv"
TARGET_AUDIT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4803_CTR_TARGET_AUDIT.csv"
OBSTRUCTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4803_OBSTRUCTION_UPDATE.csv"
GATE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4803_PROMOTION_GATES.csv"
FIREWALL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4803_FIREWALL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4803_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4803_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4803_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4803_VALIDATION.csv"

TARGETS_4802 = SOURCE_DIR / "P8_Y5_R2FR_4802_COMPONENT_TARGET_BOUNDS.csv"
CURRENT_4802 = SOURCE_DIR / "P8_Y5_R2FR_4802_COFRAME_CURRENT_OUTPUT.csv"
COMPONENT_4802 = SOURCE_DIR / "P8_Y5_R2FR_4802_COMPONENT_SOURCE_OUTPUT.csv"

NOCHARGE_CLAUSES = (
    "gauss_law_signed",
    "bulk_source_neutrality_signed",
    "boundary_charge_zero_signed",
    "counterterm_zero_signed",
    "same_matter_coframe_signed",
    "no_hidden_clock_or_source_reentry_signed",
    "no_GR_import_signed",
    "no_fit_to_bound_signed",
)

SOURCE_SPECS = [
    ("SRC4803_00_4802_doc", POST / "4802-Y5-R2FR-parent-coframe-current-or-tau-component-source-pack.md", "c_T + c_R = 0", "4802 selects cTR target"),
    ("SRC4803_01_4802_targets", TARGETS_4802, "TGT4802_0_cTR_sum", "4802 cTR target bound"),
    ("SRC4803_02_4802_current", CURRENT_4802, "ordinary_current_hair_unit_control", "4802 current/hair rows"),
    ("SRC4803_03_4802_component", COMPONENT_4802, "physical_cTR_sum_missing", "4802 component source rows"),
    ("SRC4803_04_11_current", POST / "11-cell-current-origin-attempt.md", "W partial_r R_AB = Q_R", "ordinary radial current hair obstruction"),
    ("SRC4803_05_10_observer", POST / "10-observer-map-symplectic-contract.md", "J_q = T sqrt(S)", "observer-cell definition"),
    ("SRC4803_06_2283_finalizer", POST / "2283-Y5-R2FR-radial-observer-cell-current-owner-or-q-closure-finalizer.md", "The executable next route is finite residual physics", "finite residual route precedent"),
    ("SRC4803_07_runner", RUNNER, "def nocharge_row", "4803 executable runner"),
]


RUNNER_TEXT = r'''from __future__ import annotations

import csv
import math
import sys
from pathlib import Path
from typing import Any


NOCHARGE_CLAUSES = (
    "gauss_law_signed",
    "bulk_source_neutrality_signed",
    "boundary_charge_zero_signed",
    "counterterm_zero_signed",
    "same_matter_coframe_signed",
    "no_hidden_clock_or_source_reentry_signed",
    "no_GR_import_signed",
    "no_fit_to_bound_signed",
)

FORBIDDEN_SOURCE_TOKENS = (
    "GR_IMPORT",
    "SCHWARZSCHILD_AB_IMPORT",
    "EINSTEIN_VACUUM_IMPORT",
    "FIT_TO_BOUND",
    "BOUND_AS_SOURCE",
    "OBSERVED_RESIDUAL_CANCEL",
    "CTR_BY_DECLARATION",
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
    source_text = " ".join(str(row.get(field, "")) for field in ("nocharge_id", "prior_id", "source_path", "equation_ref", "notes", "provenance")).upper()
    return any(token in source_text for token in FORBIDDEN_SOURCE_TOKENS)


def missing_clauses(row: dict[str, Any]) -> list[str]:
    return [clause for clause in NOCHARGE_CLAUSES if not bool_text(row.get(clause))]


def nocharge_row(row: dict[str, Any]) -> dict[str, Any]:
    nocharge_id = str(row.get("nocharge_id", "")).strip() or "UNNAMED_NOCHARGE"
    output: dict[str, Any] = {
        "nocharge_id": nocharge_id,
        "route": row.get("route", ""),
        "input_valid_for_claim": bool_text(row.get("valid_for_claim")),
        "valid_for_claim": False,
        "claim_allowed": False,
    }
    if forbidden_source_used(row):
        output.update(
            {
                "Q_ext_bound_abs": "MISSING_NUMERIC_VALUE",
                "cTR_bound_abs": "MISSING_NUMERIC_VALUE",
                "nocharge_theorem": False,
                "runner_status": "FAILED_CTR_NOCHARGE_GATE",
                "missing_nocharge_inputs": "FORBIDDEN_NOCHARGE_SOURCE",
                "anti_circularity_status": "FAIL_FORBIDDEN_SOURCE_USED",
            }
        )
        return output

    missing = missing_clauses(row)
    fields = ("Q_bulk_abs", "Q_boundary_abs", "Q_counterterm_abs", "Q_reentry_abs")
    values: dict[str, float] = {}
    numeric_missing: list[str] = []
    for field in fields:
        value = parse_float(row.get(field))
        if value is None or value < 0.0:
            numeric_missing.append(f"MISSING_{field}")
        else:
            values[field] = value

    if numeric_missing:
        output.update(
            {
                "Q_ext_bound_abs": "MISSING_NUMERIC_VALUE",
                "cTR_bound_abs": "MISSING_NUMERIC_VALUE",
                "nocharge_theorem": False,
                "runner_status": "BLOCKED_MISSING_CTR_NOCHARGE_INPUTS",
                "missing_nocharge_inputs": ";".join([*missing, *numeric_missing]),
                "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
            }
        )
        return output

    q_bound = values["Q_bulk_abs"] + values["Q_boundary_abs"] + values["Q_counterterm_abs"] + values["Q_reentry_abs"]
    if not missing and q_bound <= 1.0e-15:
        status = "CTR_GAUSS_NOCHARGE_CONDITIONAL_THEOREM_NONCLAIM"
        theorem = True
    elif q_bound <= 1.0e-15:
        status = "CTR_GAUSS_ZERO_NUMERIC_PARENT_UNSIGNED_NONCLAIM"
        theorem = False
    else:
        status = "CTR_GAUSS_FINITE_HAIR_BOUND_COMPUTED_NONCLAIM"
        theorem = False
    output.update(
        {
            "Q_ext_bound_abs": format_float(q_bound),
            "cTR_bound_abs": format_float(q_bound),
            "nocharge_theorem": theorem,
            "runner_status": status,
            "missing_nocharge_inputs": ";".join(missing),
            "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
        }
    )
    return output


def prior_row(row: dict[str, Any]) -> dict[str, Any]:
    prior_id = str(row.get("prior_id", "")).strip() or "UNNAMED_CTR_PRIOR"
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
                "cTR_abs_value": "MISSING_NUMERIC_VALUE",
                "required_abs_max": row.get("required_abs_max", ""),
                "numeric_window_pass": False,
                "runner_status": "FAILED_CTR_PRIOR_GATE",
                "missing_prior_inputs": "FORBIDDEN_CTR_PRIOR_SOURCE",
                "anti_circularity_status": "FAIL_FORBIDDEN_SOURCE_USED",
            }
        )
        return output

    required = parse_float(row.get("required_abs_max"))
    value = parse_float(row.get("cTR_abs_value"))
    source_signed = bool_text(row.get("source_signed"))
    theorem_zero = bool_text(row.get("theorem_zero_signed"))
    source_path = str(row.get("source_path", "")).strip()
    equation_ref = str(row.get("equation_ref", "")).strip()
    missing: list[str] = []
    if required is None or required < 0.0:
        missing.append("MISSING_required_abs_max")

    if theorem_zero and required is not None:
        output.update(
            {
                "cTR_abs_value": "0.000000000000000e+00",
                "required_abs_max": format_float(required),
                "numeric_window_pass": True,
                "runner_status": "CTR_THEOREM_ZERO_CONDITIONAL_NONCLAIM",
                "missing_prior_inputs": "",
                "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
            }
        )
        return output

    if value is None:
        missing.append("MISSING_cTR_abs_value")
    if not source_signed:
        missing.append("MISSING_source_signed")
    if not source_path:
        missing.append("MISSING_source_path")
    if not equation_ref:
        missing.append("MISSING_equation_ref")

    if value is None or required is None:
        output.update(
            {
                "cTR_abs_value": format_float(value),
                "required_abs_max": format_float(required),
                "numeric_window_pass": False,
                "runner_status": "BLOCKED_MISSING_CTR_PRIOR_INPUTS",
                "missing_prior_inputs": ";".join(missing),
                "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
            }
        )
        return output

    numeric_pass = abs(value) <= abs(required)
    if numeric_pass and missing:
        status = "CTR_PRIOR_NUMERIC_WINDOW_PASS_SOURCE_UNSIGNED_NONCLAIM"
    elif numeric_pass:
        status = "CTR_PRIOR_NUMERIC_WINDOW_PASS_SOURCE_SIGNED_NONCLAIM_UNLESS_INPUT_VALID"
    else:
        status = "CTR_PRIOR_NUMERIC_WINDOW_FAIL"
    output.update(
        {
            "cTR_abs_value": format_float(abs(value)),
            "required_abs_max": format_float(abs(required)),
            "numeric_window_pass": numeric_pass,
            "runner_status": status,
            "missing_prior_inputs": ";".join(missing),
            "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
            "claim_allowed": bool_text(row.get("valid_for_claim")) and not missing and numeric_pass,
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


def main() -> int:
    if len(sys.argv) != 4:
        print("usage: coframe_cTR_nocharge_prior_runner.py <nocharge|prior> <input.csv> <output.csv>", file=sys.stderr)
        return 2
    mode = sys.argv[1]
    if mode == "nocharge":
        rows = [nocharge_row(row) for row in read_csv(Path(sys.argv[2]))]
    elif mode == "prior":
        rows = [prior_row(row) for row in read_csv(Path(sys.argv[2]))]
    else:
        raise ValueError(f"unknown mode: {mode}")
    write_csv(Path(sys.argv[3]), rows)
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


def cTR_target() -> float:
    for row in parse_csv(TARGETS_4802):
        if row["target_id"] == "TGT4802_0_cTR_sum":
            return float(row["required_abs_max"])
    raise ValueError("missing TGT4802_0_cTR_sum")


def target_audit_rows(timestamp: str, target: float) -> list[dict[str, Any]]:
    return [
        {
            "audit_id": "TGA4803_0_target_import",
            "component_expr": "abs(c_T+c_R)",
            "required_abs_max": f"{target:.15e}",
            "source": str(TARGETS_4802),
            "derivation": "min(tau_gamma_max,tau_orbital_max) from 4802 target table",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def clause_map(value: bool) -> dict[str, bool]:
    return {clause: value for clause in NOCHARGE_CLAUSES}


def nocharge_input_rows(timestamp: str) -> list[dict[str, Any]]:
    physical = clause_map(False)
    physical["no_GR_import_signed"] = True
    physical["no_fit_to_bound_signed"] = True

    gauss_zero = clause_map(False)
    for clause in ("gauss_law_signed", "bulk_source_neutrality_signed", "boundary_charge_zero_signed", "counterterm_zero_signed", "no_GR_import_signed", "no_fit_to_bound_signed"):
        gauss_zero[clause] = True

    finite_hair = clause_map(False)
    for clause in ("gauss_law_signed", "no_GR_import_signed", "no_fit_to_bound_signed"):
        finite_hair[clause] = True

    signed = clause_map(True)

    def row(nocharge_id: str, route: str, source: str, clauses: dict[str, bool], values: dict[str, Any] | None = None, notes: str = "") -> dict[str, Any]:
        payload: dict[str, Any] = {
            "nocharge_id": nocharge_id,
            "route": route,
            "source_path": source,
            "equation_ref": "",
            "Q_bulk_abs": "",
            "Q_boundary_abs": "",
            "Q_counterterm_abs": "",
            "Q_reentry_abs": "",
            "notes": notes,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        payload.update(clauses)
        if values:
            payload.update(values)
        return payload

    return [
        row("physical_cTR_nocharge_missing", "physical_missing", "4803_physical_branch_missing_parent_nocharge", physical),
        row(
            "gauss_zero_unsigned_same_matter_open",
            "conditional_gauss_zero_missing_same_matter",
            "SRC4803_04_11_current_plus_SRC4803_05_10_observer",
            gauss_zero,
            {"Q_bulk_abs": "0.0", "Q_boundary_abs": "0.0", "Q_counterterm_abs": "0.0", "Q_reentry_abs": "0.0", "equation_ref": "Q_ext=Q_bulk+Q_boundary+Q_counterterm+Q_reentry"},
            "Gauss/nocharge route zeros cTR only if same-matter-coframe and no hidden reentry are signed",
        ),
        row(
            "finite_unit_hair_bound",
            "finite_hair_bound",
            "SRC4803_02_4802_current",
            finite_hair,
            {"Q_bulk_abs": "1.0", "Q_boundary_abs": "0.0", "Q_counterterm_abs": "0.0", "Q_reentry_abs": "0.0", "equation_ref": "ordinary_current_hair_unit_control"},
            "unit Q_R/cTR hair carried as finite nonclaim fallback",
        ),
        row(
            "conditional_parent_gauss_nocharge",
            "conditional_theorem",
            "conditional_parent_bulk_boundary_counterterm_reentry_zero",
            signed,
            {"Q_bulk_abs": "0.0", "Q_boundary_abs": "0.0", "Q_counterterm_abs": "0.0", "Q_reentry_abs": "0.0", "equation_ref": "all coframe charges vanish by parent theorem"},
        ),
        row(
            "forbidden_GR_import_nocharge_control",
            "forbidden_control",
            "SCHWARZSCHILD_AB_IMPORT;CTR_BY_DECLARATION",
            physical,
            {"Q_bulk_abs": "0.0", "Q_boundary_abs": "0.0", "Q_counterterm_abs": "0.0", "Q_reentry_abs": "0.0"},
        ),
    ]


def prior_input_rows(timestamp: str, target: float) -> list[dict[str, Any]]:
    def row(prior_id: str, value: str = "", source_signed: bool = False, source_path: str = "", equation_ref: str = "", theorem_zero: bool = False, notes: str = "") -> dict[str, Any]:
        return {
            "prior_id": prior_id,
            "component_expr": "abs(c_T+c_R)",
            "required_abs_max": f"{target:.15e}",
            "cTR_abs_value": value,
            "source_signed": source_signed,
            "source_path": source_path,
            "equation_ref": equation_ref,
            "theorem_zero_signed": theorem_zero,
            "notes": notes,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }

    return [
        row("physical_cTR_prior_missing"),
        row("cTR_zero_candidate_unsigned", "0.0", False, "SRC4803_03_4802_component", "cTR_sum_zero_candidate_unsigned", False, "zero candidate from 4802, source unsigned"),
        row("cTR_unit_hair_prior_smoke", "1.0", False, "SRC4803_03_4802_component", "cTR_sum_unit_hair_smoke", False, "unit hair under target, source unsigned"),
        row("cTR_strict_fail_control", "10.0", False, "SRC4803_03_4802_component", "strict fail control", False, "fails current cTR target window"),
        row("conditional_cTR_theorem_zero", theorem_zero=True, source_signed=True, source_path="conditional_parent_gauss_nocharge", equation_ref="c_T+c_R=0"),
        row("forbidden_cTR_fit_to_bound_control", "0.0", False, "FIT_TO_BOUND;BOUND_AS_SOURCE", "fit control"),
    ]


def obstruction_rows(nocharge_rows: list[dict[str, str]], prior_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    no_by_id = {row["nocharge_id"]: row for row in nocharge_rows}
    pr_by_id = {row["prior_id"]: row for row in prior_rows}
    return [
        {
            "update_id": "OBS4803_0_gauss",
            "item": "Gauss/nocharge route",
            "status": no_by_id["gauss_zero_unsigned_same_matter_open"]["runner_status"],
            "value_or_bound": no_by_id["gauss_zero_unsigned_same_matter_open"]["cTR_bound_abs"],
            "meaning": "bulk/boundary/counterterm zero is enough only after same-matter-coframe and no-reentry are signed",
        },
        {
            "update_id": "OBS4803_1_finite",
            "item": "finite unit cTR prior",
            "status": pr_by_id["cTR_unit_hair_prior_smoke"]["runner_status"],
            "value_or_bound": f"{pr_by_id['cTR_unit_hair_prior_smoke']['cTR_abs_value']} <= {pr_by_id['cTR_unit_hair_prior_smoke']['required_abs_max']}",
            "meaning": "unit cTR is inside the current local target window, so cTR is not the immediate numerical killer",
        },
        {
            "update_id": "OBS4803_2_fail_control",
            "item": "strict cTR fail control",
            "status": pr_by_id["cTR_strict_fail_control"]["runner_status"],
            "value_or_bound": pr_by_id["cTR_strict_fail_control"]["cTR_abs_value"],
            "meaning": "the gate can reject oversized cTR rather than accepting any coefficient",
        },
    ]


def gate_rows(nocharge_rows: list[dict[str, str]], prior_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    no_by_id = {row["nocharge_id"]: row for row in nocharge_rows}
    pr_by_id = {row["prior_id"]: row for row in prior_rows}
    return [
        {
            "gate_id": "PG4803_0_gauss_contract",
            "claim": "Gauss/nocharge route gives a precise cTR zero theorem contract",
            "gate_pass": True,
            "reason": "Q_ext decomposes into bulk, boundary, counterterm, and reentry pieces",
            "evidence": str(NOCHARGE_OUTPUT_CSV),
        },
        {
            "gate_id": "PG4803_1_parent_nocharge",
            "claim": "parent theory proves c_T+c_R=0",
            "gate_pass": no_by_id["conditional_parent_gauss_nocharge"]["nocharge_theorem"] == "True",
            "reason": "conditional row shows the proof shape, but physical row is still missing parent signatures",
            "evidence": no_by_id["physical_cTR_nocharge_missing"]["missing_nocharge_inputs"],
        },
        {
            "gate_id": "PG4803_2_finite_unit_window",
            "claim": "unit finite cTR is under current target window",
            "gate_pass": pr_by_id["cTR_unit_hair_prior_smoke"]["numeric_window_pass"] == "True",
            "reason": "1.0 is below the imported 5.256633 cTR target",
            "evidence": pr_by_id["cTR_unit_hair_prior_smoke"]["required_abs_max"],
        },
        {
            "gate_id": "PG4803_3_local_promotion",
            "claim": "local GR/Newton/PPN promotion is allowed",
            "gate_pass": False,
            "reason": "cTR source remains unsigned and other component channels remain open",
            "evidence": "nonclaim firewall active",
        },
    ]


def firewall_rows() -> list[dict[str, Any]]:
    return [
        {"firewall_id": "FW4803_0_no_gauss_shortcut", "rule": "Gauss law plus conservation is not a no-charge theorem unless bulk, boundary, counterterm and reentry pieces vanish by parent action.", "status": "ACTIVE"},
        {"firewall_id": "FW4803_1_no_bound_fit", "rule": "The 5.2566 target screens a cTR prediction; it does not define cTR.", "status": "ACTIVE"},
        {"firewall_id": "FW4803_2_no_same_coframe_skip", "rule": "Matter/readout must use the same coframe before a quiet cTR channel can be promoted.", "status": "ACTIVE"},
        {"firewall_id": "FW4803_3_no_local_claim", "rule": "Passing the cTR finite window is not a local-GR claim while clock, beta, source-normalization and R10 components remain open.", "status": "ACTIVE"},
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC4803_0_cTR",
            "decision": "cTR_is_not_immediate_numerical_killer_at_unit_scale",
            "reason": "unit finite cTR passes the current 5.2566 target window",
            "next_action": "retain cTR source/theorem gap but move pressure to clock/readout component",
        },
        {
            "decision_id": "DEC4803_1_next",
            "decision": "clock_readout_same_coframe_is_next_component",
            "reason": "after cTR, the next tight local component is tau_clock = |c_T-c_clock|+constant terms",
            "next_action": NEXT_TARGET,
        },
    ]


def status_rows(nocharge_rows: list[dict[str, str]], prior_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    no_by_id = {row["nocharge_id"]: row for row in nocharge_rows}
    pr_by_id = {row["prior_id"]: row for row in prior_rows}
    return [
        {"status_id": "STATUS4803_0_gauss", "status": no_by_id["gauss_zero_unsigned_same_matter_open"]["runner_status"], "detail": f"cTR={no_by_id['gauss_zero_unsigned_same_matter_open']['cTR_bound_abs']}"},
        {"status_id": "STATUS4803_1_unit", "status": pr_by_id["cTR_unit_hair_prior_smoke"]["runner_status"], "detail": f"1.0 <= {pr_by_id['cTR_unit_hair_prior_smoke']['required_abs_max']}"},
        {"status_id": "STATUS4803_2_physical", "status": pr_by_id["physical_cTR_prior_missing"]["runner_status"], "detail": pr_by_id["physical_cTR_prior_missing"]["missing_prior_inputs"]},
        {"status_id": "STATUS4803_3_selected_next", "status": "CLOCK_READOUT_SAME_COFRAME_OR_FINITE_CCLOCK_PRIOR_FILL", "detail": NEXT_TARGET},
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT4803_0_4804",
            "next_target": NEXT_TARGET,
            "trigger": "unit cTR is numerically under current target but clock/readout component remains unfilled",
            "required_inputs": "same-coframe clock/readout theorem or finite c_clock/c_alpha/c_mass prior rows",
            "valid_for_claim": False,
        }
    ]


def validation_rows(sources: list[dict[str, Any]], nocharge_rows: list[dict[str, str]], prior_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    no_by_id = {row["nocharge_id"]: row for row in nocharge_rows}
    pr_by_id = {row["prior_id"]: row for row in prior_rows}
    checks: list[tuple[str, str, bool, str]] = [
        ("VAL4803_0_sources", "all cited sources exist and needles are found", all(bool_text(row["exists"]) and bool_text(row["needle_found"]) for row in sources), str(SOURCE_REGISTER_CSV)),
        ("VAL4803_1_physical_nocharge_blocks", "physical cTR nocharge row remains blocked", no_by_id["physical_cTR_nocharge_missing"]["runner_status"] == "BLOCKED_MISSING_CTR_NOCHARGE_INPUTS", str(NOCHARGE_OUTPUT_CSV)),
        ("VAL4803_2_gauss_zero_unsigned", "Gauss zero candidate computes zero but remains unsigned", no_by_id["gauss_zero_unsigned_same_matter_open"]["cTR_bound_abs"] == "0.000000000000000e+00" and no_by_id["gauss_zero_unsigned_same_matter_open"]["nocharge_theorem"] == "False", str(NOCHARGE_OUTPUT_CSV)),
        ("VAL4803_3_unit_hair_bound", "finite unit hair bound computes", no_by_id["finite_unit_hair_bound"]["cTR_bound_abs"] == "1.000000000000000e+00", str(NOCHARGE_OUTPUT_CSV)),
        ("VAL4803_4_nocharge_forbidden_fails", "forbidden GR-import nocharge control fails", no_by_id["forbidden_GR_import_nocharge_control"]["runner_status"] == "FAILED_CTR_NOCHARGE_GATE", str(NOCHARGE_OUTPUT_CSV)),
        ("VAL4803_5_physical_prior_blocks", "physical cTR prior remains blocked", pr_by_id["physical_cTR_prior_missing"]["runner_status"] == "BLOCKED_MISSING_CTR_PRIOR_INPUTS", str(CTR_PRIOR_OUTPUT_CSV)),
        ("VAL4803_6_unit_prior_passes", "unit cTR prior smoke passes target window", pr_by_id["cTR_unit_hair_prior_smoke"]["numeric_window_pass"] == "True" and pr_by_id["cTR_unit_hair_prior_smoke"]["claim_allowed"] == "False", str(CTR_PRIOR_OUTPUT_CSV)),
        ("VAL4803_7_strict_fail", "strict cTR fail control fails numeric target", pr_by_id["cTR_strict_fail_control"]["runner_status"] == "CTR_PRIOR_NUMERIC_WINDOW_FAIL", str(CTR_PRIOR_OUTPUT_CSV)),
        ("VAL4803_8_claim", "claim register includes L-645 as nonclaim", CLAIM_ID in read_text(CLAIMS_PATH) and MARKER in read_text(CLAIMS_PATH), str(CLAIMS_PATH)),
        ("VAL4803_9_resume", "resume points at 4804", NEXT_TARGET in read_text(RESUME_PATH), str(RESUME_PATH)),
    ]
    rows = [
        {"check_id": check_id, "description": desc, "result": "PASS" if passed else "FAIL", "evidence": evidence}
        for check_id, desc, passed, evidence in checks
    ]
    rows.append(
        {
            "check_id": "VAL4803_OVERALL",
            "description": "all 4803 cTR nocharge/prior checks pass",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "evidence": DECISION,
        }
    )
    return rows


def write_documents(
    timestamp: str,
    target: float,
    sources: list[dict[str, Any]],
    target_rows: list[dict[str, Any]],
    nocharge_rows: list[dict[str, str]],
    prior_rows: list[dict[str, str]],
    obstructions: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    firewalls: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    statuses: list[dict[str, Any]],
    validations: list[dict[str, Any]],
) -> None:
    content = f"""# 4803 - Coframe reciprocity current nocharge or finite cTR prior fill

Marker: `{MARKER}`
Generated: `{timestamp}`
Decision: `{DECISION}`

## Result

4803 attacks the first component target from 4802:

```text
cTR := c_T + c_R
required: |cTR| <= {target:.15e}
```

The derived current route is now a precise Gauss/no-charge contract:

```text
Q_ext = Q_bulk + Q_boundary + Q_counterterm + Q_reentry
cTR_bound <= |Q_ext|
```

If all four pieces vanish by parent action and the same matter/readout coframe is signed, then `c_T+c_R=0`. If not, `cTR` remains a finite residual coefficient to source.

## Target Audit

{markdown_table(target_rows)}

## Source Register

{markdown_table(sources, ["source_id", "source_path", "exists", "needle_found", "role"])}

## Nocharge Output

{markdown_table(nocharge_rows, ["nocharge_id", "route", "Q_ext_bound_abs", "cTR_bound_abs", "nocharge_theorem", "runner_status", "missing_nocharge_inputs", "anti_circularity_status"])}

## cTR Prior Output

{markdown_table(prior_rows, ["prior_id", "component_expr", "cTR_abs_value", "required_abs_max", "numeric_window_pass", "runner_status", "missing_prior_inputs", "anti_circularity_status"])}

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

    formal_content = f"""# 819 - PPC4161 coframe reciprocity current nocharge or finite cTR prior fill

Marker: `{MARKER}`
Generated: `{timestamp}`

## Formal Update

4803 gives `c_T+c_R` a clean theorem/fallback split:

```text
Q_ext = Q_bulk + Q_boundary + Q_counterterm + Q_reentry
cTR_bound <= |Q_ext|
```

Parent theorem path:

```text
Q_bulk = Q_boundary = Q_counterterm = Q_reentry = 0
same matter/readout coframe signed
=> c_T+c_R = 0
```

Finite path:

```text
|c_T+c_R| <= {target:.15e}
```

Unit `cTR` passes the current target window, so the next local-pressure component is clock/readout rather than more looping on ordinary current conservation.

See `{DOC_PATH}`.
"""
    write_text(FORMAL_PATH, formal_content)


def update_registers(timestamp: str) -> None:
    claim_line = (
        f'{CLAIM_ID},coframe_cTR_nocharge_prior_runner,'
        f'"4803 installs a Gauss/no-charge contract for c_T+c_R and a finite cTR prior gate; unit cTR passes the current target window but remains source-unsigned.",'
        f'"Generated source register, target audit, nocharge input/output, cTR prior input/output, gates, firewalls, decision, status, next target and validation.",'
        f'coframe_cTR_nocharge_prior_private_nonclaim,'
        f'{NEXT_TARGET},'
        f'"Do not claim local GR from unit cTR passing a target window; parent source/nocharge and other component channels remain open.",'
        f'local_gr,{DOC_PATH},{NEXT_TARGET},'
        f'Gauss conservation as nocharge; cTR fit to bound; GR import; same-coframe skip; local promotion,'
        f'"Coframe cTR nocharge and finite prior gate",'
        f'{MARKER}; {DECISION}; generated {timestamp}\n'
    )
    if CLAIM_ID not in read_text(CLAIMS_PATH):
        with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
            handle.write(claim_line)

    spine_block = f"""
## {MARKER}

4803 converts `c_T+c_R` into a Gauss/no-charge theorem contract plus finite prior gate:

```text
Q_ext = Q_bulk + Q_boundary + Q_counterterm + Q_reentry
cTR_bound <= |Q_ext|
```

Unit `cTR` is under the current target window, so `c_T+c_R` is not the immediate numerical killer. The remaining issue is parent sourcing/theorem ownership, and the next component pressure is clock/readout.
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
Last checkpoint: `4803-Y5-R2FR-coframe-reciprocity-current-nocharge-or-finite-cTR-prior-fill.md`
Marker: `{MARKER}`

## Where we are

4803 installed the first component theorem/fallback split:

```text
cTR := c_T+c_R
Q_ext = Q_bulk + Q_boundary + Q_counterterm + Q_reentry
cTR_bound <= |Q_ext|
|cTR| <= 5.256633029822351
```

Unit `cTR` passes the current target window as a nonclaim smoke row, but physical sourcing is still missing. The parent theorem route requires bulk neutrality, boundary charge zero, counterterm zero, no hidden reentry, and same matter/readout coframe.

## Live blockers

- Parent no-charge theorem is not signed.
- Physical `cTR` prior row is still missing.
- Clock/readout component is now the next tight local-pressure channel.

## Next target

`{NEXT_TARGET}`
"""
    write_text(RESUME_PATH, resume)


def main() -> int:
    timestamp = now()
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    SCRIPT_DIR.mkdir(parents=True, exist_ok=True)

    write_text(RUNNER, RUNNER_TEXT)
    target = cTR_target()
    sources = source_register(timestamp)
    target_rows = target_audit_rows(timestamp, target)
    nocharge_inputs = nocharge_input_rows(timestamp)
    prior_inputs = prior_input_rows(timestamp, target)

    write_csv(SOURCE_REGISTER_CSV, sources)
    write_csv(TARGET_AUDIT_CSV, target_rows)
    write_csv(NOCHARGE_INPUT_CSV, nocharge_inputs)
    write_csv(CTR_PRIOR_INPUT_CSV, prior_inputs)

    python = sys.executable
    run_command([python, str(RUNNER), "nocharge", str(NOCHARGE_INPUT_CSV), str(NOCHARGE_OUTPUT_CSV)])
    run_command([python, str(RUNNER), "prior", str(CTR_PRIOR_INPUT_CSV), str(CTR_PRIOR_OUTPUT_CSV)])

    nocharge_rows = parse_csv(NOCHARGE_OUTPUT_CSV)
    prior_rows = parse_csv(CTR_PRIOR_OUTPUT_CSV)
    obstructions = obstruction_rows(nocharge_rows, prior_rows)
    gates = gate_rows(nocharge_rows, prior_rows)
    firewalls = firewall_rows()
    decisions = decision_rows()
    statuses = status_rows(nocharge_rows, prior_rows)
    next_targets = next_target_rows()

    write_csv(OBSTRUCTION_CSV, obstructions)
    write_csv(GATE_CSV, gates)
    write_csv(FIREWALL_CSV, firewalls)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_TARGET_CSV, next_targets)

    update_registers(timestamp)
    validations = validation_rows(sources, nocharge_rows, prior_rows)
    write_csv(VALIDATION_CSV, validations)
    write_documents(timestamp, target, sources, target_rows, nocharge_rows, prior_rows, obstructions, gates, firewalls, decisions, statuses, validations)

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
