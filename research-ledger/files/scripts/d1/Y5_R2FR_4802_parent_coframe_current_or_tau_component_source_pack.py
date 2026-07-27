from __future__ import annotations

import csv
import math
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

CHECKPOINT = "4802"
CLAIM_ID = "L-644"
MARKER = "PPC4161_PARENT_COFRAME_CURRENT_OR_TAU_COMPONENT_SOURCE_PACK_4802"
PACKET_MARKER = "PPC4161_PACKET_PARENT_COFRAME_CURRENT_OR_TAU_COMPONENT_SOURCE_PACK_4802"
DECISION = "COFRAME_CURRENT_NOCHARGE_GATE_AND_COMPONENT_SOURCE_PACK_INSTALLED_NONCLAIM"
NEXT_TARGET = "4803-Y5-R2FR-coframe-reciprocity-current-nocharge-or-finite-cTR-prior-fill.md"

DOC_PATH = POST / "4802-Y5-R2FR-parent-coframe-current-or-tau-component-source-pack.md"
FORMAL_PATH = FORMAL / "818-PPC4161-parent-coframe-current-or-tau-component-source-pack.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"

RUNNER = SCRIPT_DIR / "parent_coframe_component_source_pack_runner.py"

SOURCE_REGISTER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4802_SOURCE_REGISTER.csv"
CURRENT_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4802_COFRAME_CURRENT_INPUT.csv"
CURRENT_OUTPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4802_COFRAME_CURRENT_OUTPUT.csv"
COMPONENT_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4802_COMPONENT_SOURCE_INPUT.csv"
COMPONENT_OUTPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4802_COMPONENT_SOURCE_OUTPUT.csv"
TARGET_BOUNDS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4802_COMPONENT_TARGET_BOUNDS.csv"
OBSTRUCTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4802_OBSTRUCTION_UPDATE.csv"
GATE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4802_PROMOTION_GATES.csv"
FIREWALL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4802_FIREWALL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4802_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4802_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4802_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4802_VALIDATION.csv"

TAU_REQ_4800 = SOURCE_DIR / "P8_Y5_R2FR_4800_TAU_REQUIREMENTS.csv"
COFRAME_OUTPUT_4801 = SOURCE_DIR / "P8_Y5_R2FR_4801_COFRAME_PROJECTION_OUTPUT.csv"

CURRENT_CLAUSES = (
    "coframe_current_defined_signed",
    "Jq_variation_identity_signed",
    "nocharge_theorem_signed",
    "boundary_charge_zero_signed",
    "source_cell_zero_signed",
    "same_matter_coframe_signed",
    "no_GR_import_signed",
    "no_tau_fit_signed",
)

SOURCE_SPECS = [
    ("SRC4802_00_4801_doc", POST / "4801-Y5-R2FR-observer-coframe-tau-projection-derivation-or-parent-BC-no-flux-action.md", "tau_gamma = |c_T + c_R|", "4801 component tau formulas"),
    ("SRC4802_01_4801_output", COFRAME_OUTPUT_4801, "reciprocal_cell_preserving_no_direct_clock_candidate", "4801 machine-readable quiet-subspace candidate"),
    ("SRC4802_02_4800_tau", TAU_REQ_4800, "TAU4800_5", "4800 arena tau windows"),
    ("SRC4802_03_10_observer", POST / "10-observer-map-symplectic-contract.md", "J_q = T sqrt(S)", "observer cell definition"),
    ("SRC4802_04_11_current", POST / "11-cell-current-origin-attempt.md", "W partial_r R_AB = Q_R", "ordinary current hair obstruction"),
    ("SRC4802_05_2283_finalizer", POST / "2283-Y5-R2FR-radial-observer-cell-current-owner-or-q-closure-finalizer.md", "FINITE_Q_RESIDUAL_ROUTE_IS_NEXT_EXECUTABLE_PATH", "finite q/R_AB route finalizer"),
    ("SRC4802_06_1148_source_norm", POST / "1148-Y5-R10-cR11-source-normalization-owner-or-zero-theorem.md", "source-normalization residual vector", "source-normalization component precedent"),
    ("SRC4802_07_runner", RUNNER, "def coframe_current_row", "4802 executable runner"),
]


RUNNER_TEXT = r'''from __future__ import annotations

import csv
import math
import sys
from pathlib import Path
from typing import Any


CURRENT_CLAUSES = (
    "coframe_current_defined_signed",
    "Jq_variation_identity_signed",
    "nocharge_theorem_signed",
    "boundary_charge_zero_signed",
    "source_cell_zero_signed",
    "same_matter_coframe_signed",
    "no_GR_import_signed",
    "no_tau_fit_signed",
)

FORBIDDEN_SOURCE_TOKENS = (
    "GR_IMPORT",
    "SCHWARZSCHILD_AB_IMPORT",
    "EINSTEIN_VACUUM_IMPORT",
    "FIT_TO_BOUND",
    "TAU_BY_DECLARATION",
    "BOUND_AS_SOURCE",
    "OBSERVED_RESIDUAL_CANCEL",
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
    source_text = " ".join(str(row.get(field, "")) for field in ("current_id", "component_id", "source_path", "equation_ref", "notes", "provenance")).upper()
    return any(token in source_text for token in FORBIDDEN_SOURCE_TOKENS)


def missing_current_clauses(row: dict[str, Any]) -> list[str]:
    return [clause for clause in CURRENT_CLAUSES if not bool_text(row.get(clause))]


def coframe_current_row(row: dict[str, Any]) -> dict[str, Any]:
    current_id = str(row.get("current_id", "")).strip() or "UNNAMED_COFAME_CURRENT"
    output: dict[str, Any] = {
        "current_id": current_id,
        "current_route": row.get("current_route", ""),
        "input_valid_for_claim": bool_text(row.get("valid_for_claim")),
        "valid_for_claim": False,
        "claim_allowed": False,
    }
    if forbidden_source_used(row):
        output.update(
            {
                "cTR_bound_abs": "MISSING_NUMERIC_VALUE",
                "tau_gamma_abs": "MISSING_NUMERIC_VALUE",
                "current_nocharge_theorem": False,
                "runner_status": "FAILED_COFRAME_CURRENT_GATE",
                "missing_current_inputs": "FORBIDDEN_CURRENT_SOURCE",
                "anti_circularity_status": "FAIL_FORBIDDEN_SOURCE_USED",
            }
        )
        return output

    missing = missing_current_clauses(row)
    if not missing:
        output.update(
            {
                "cTR_bound_abs": "0.000000000000000e+00",
                "tau_gamma_abs": "0.000000000000000e+00",
                "current_nocharge_theorem": True,
                "runner_status": "COFRAME_CURRENT_NOCHARGE_CONDITIONAL_THEOREM_NONCLAIM",
                "missing_current_inputs": "",
                "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
            }
        )
        return output

    fields = ("Q_cell_abs", "boundary_charge_abs", "source_cell_abs", "counterterm_abs")
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
                "cTR_bound_abs": "MISSING_NUMERIC_VALUE",
                "tau_gamma_abs": "MISSING_NUMERIC_VALUE",
                "current_nocharge_theorem": False,
                "runner_status": "BLOCKED_MISSING_COFRAME_CURRENT_INPUTS",
                "missing_current_inputs": ";".join([*missing, *numeric_missing]),
                "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
            }
        )
        return output

    bound = values["Q_cell_abs"] + values["boundary_charge_abs"] + values["source_cell_abs"] + values["counterterm_abs"]
    if bound <= 1.0e-15:
        status = "COFRAME_CURRENT_NUMERIC_ZERO_PARENT_UNSIGNED_NONCLAIM"
    else:
        status = "COFRAME_CURRENT_HAIR_BOUND_COMPUTED_NONCLAIM"
    output.update(
        {
            "cTR_bound_abs": format_float(bound),
            "tau_gamma_abs": format_float(bound),
            "current_nocharge_theorem": False,
            "runner_status": status,
            "missing_current_inputs": ";".join(missing),
            "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
        }
    )
    return output


def component_source_row(row: dict[str, Any]) -> dict[str, Any]:
    component_id = str(row.get("component_id", "")).strip() or "UNNAMED_COMPONENT"
    output: dict[str, Any] = {
        "component_id": component_id,
        "component_expr": row.get("component_expr", ""),
        "arena_pressure": row.get("arena_pressure", ""),
        "input_valid_for_claim": bool_text(row.get("valid_for_claim")),
        "valid_for_claim": False,
        "claim_allowed": False,
    }
    if forbidden_source_used(row):
        output.update(
            {
                "component_abs_value": "MISSING_NUMERIC_VALUE",
                "required_abs_max": row.get("required_abs_max", ""),
                "numeric_window_pass": False,
                "runner_status": "FAILED_COMPONENT_SOURCE_GATE",
                "missing_component_inputs": "FORBIDDEN_COMPONENT_SOURCE",
                "anti_circularity_status": "FAIL_FORBIDDEN_SOURCE_USED",
            }
        )
        return output

    required = parse_float(row.get("required_abs_max"))
    value = parse_float(row.get("numeric_abs_value"))
    theorem_zero = bool_text(row.get("theorem_zero_signed"))
    source_signed = bool_text(row.get("source_signed"))
    source_path = str(row.get("source_path", "")).strip()
    equation_ref = str(row.get("equation_ref", "")).strip()
    missing: list[str] = []
    if required is None or required < 0.0:
        missing.append("MISSING_required_abs_max")

    if theorem_zero and required is not None:
        output.update(
            {
                "component_abs_value": "0.000000000000000e+00",
                "required_abs_max": format_float(required),
                "numeric_window_pass": True,
                "runner_status": "COMPONENT_THEOREM_ZERO_CONDITIONAL_NONCLAIM",
                "missing_component_inputs": "",
                "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
            }
        )
        return output

    if value is None:
        missing.append("MISSING_numeric_abs_value")
    if not source_signed:
        missing.append("MISSING_source_signed")
    if not source_path:
        missing.append("MISSING_source_path")
    if not equation_ref:
        missing.append("MISSING_equation_ref")

    if value is None or required is None:
        output.update(
            {
                "component_abs_value": format_float(value),
                "required_abs_max": format_float(required),
                "numeric_window_pass": False,
                "runner_status": "BLOCKED_MISSING_COMPONENT_SOURCE_INPUTS",
                "missing_component_inputs": ";".join(missing),
                "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
            }
        )
        return output

    numeric_pass = abs(value) <= abs(required)
    if numeric_pass and missing:
        status = "COMPONENT_NUMERIC_WINDOW_PASS_SOURCE_UNSIGNED_NONCLAIM"
    elif numeric_pass:
        status = "COMPONENT_NUMERIC_WINDOW_PASS_SOURCE_SIGNED_NONCLAIM_UNLESS_INPUT_VALID"
    else:
        status = "COMPONENT_NUMERIC_WINDOW_FAIL"

    output.update(
        {
            "component_abs_value": format_float(abs(value)),
            "required_abs_max": format_float(abs(required)),
            "numeric_window_pass": numeric_pass,
            "runner_status": status,
            "missing_component_inputs": ";".join(missing),
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
        print("usage: parent_coframe_component_source_pack_runner.py <current|component> <input.csv> <output.csv>", file=sys.stderr)
        return 2
    mode = sys.argv[1]
    if mode == "current":
        rows = [coframe_current_row(row) for row in read_csv(Path(sys.argv[2]))]
    elif mode == "component":
        rows = [component_source_row(row) for row in read_csv(Path(sys.argv[2]))]
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


def format_float(value: float) -> str:
    return f"{value:.15e}"


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


def load_tau_windows() -> dict[str, float]:
    rows = parse_csv(TAU_REQ_4800)
    by_arena = {row["arena_id"]: row for row in rows}
    return {
        "epsilon": float(by_arena["ppn_gamma_cassini_required_tau"]["epsilon_local_abs"]),
        "gamma_tau": float(by_arena["ppn_gamma_cassini_required_tau"]["tau_required_max_abs"]),
        "beta_tau": float(by_arena["ppn_beta_mercury_required_tau"]["tau_required_max_abs"]),
        "clock_tau": float(by_arena["clock_redshift_galileo_required_tau"]["tau_required_max_abs"]),
        "R10_tau": float(by_arena["r10_yukawa_grav_strength_anchor_required_tau"]["tau_required_max_abs"]),
        "orbital_tau": float(by_arena["orbital_mercury_total_precession_fraction_required_tau"]["tau_required_max_abs"]),
    }


def target_bound_rows(timestamp: str, windows: dict[str, float]) -> list[dict[str, Any]]:
    rows = [
        {
            "target_id": "TGT4802_0_cTR_sum",
            "component_expr": "abs(c_T+c_R)",
            "arena_pressure": "PPN_gamma_and_orbital",
            "required_abs_max": format_float(min(windows["gamma_tau"], windows["orbital_tau"])),
            "source": str(TAU_REQ_4800),
            "meaning": "reciprocal-cell/shear projection must stay under the stricter orbital/gamma tau window",
        },
        {
            "target_id": "TGT4802_1_clock_difference",
            "component_expr": "abs(c_T-c_clock)+abs(c_alpha)+abs(c_mass)",
            "arena_pressure": "clock_redshift",
            "required_abs_max": format_float(windows["clock_tau"]),
            "source": str(TAU_REQ_4800),
            "meaning": "direct clock/readout and constants channel budget",
        },
        {
            "target_id": "TGT4802_2_beta_second_order",
            "component_expr": "abs(c_beta2)+abs(c_T+c_R)",
            "arena_pressure": "PPN_beta",
            "required_abs_max": format_float(windows["beta_tau"]),
            "source": str(TAU_REQ_4800),
            "meaning": "second-order beta plus reciprocal-cell budget",
        },
        {
            "target_id": "TGT4802_3_source_norm",
            "component_expr": "abs(c_source_norm)",
            "arena_pressure": "orbital_source_normalization",
            "required_abs_max": format_float(windows["orbital_tau"]),
            "source": str(TAU_REQ_4800),
            "meaning": "measured-GM/Newton source normalization budget",
        },
        {
            "target_id": "TGT4802_4_R10_product",
            "component_expr": "abs(K_R10*q_source*q_test+c_R10_tail)",
            "arena_pressure": "R10_anchor_only",
            "required_abs_max": format_float(windows["R10_tau"]),
            "source": str(TAU_REQ_4800),
            "meaning": "R10 source/test/material kernel budget; anchor only until alpha(lambda) curve exists",
        },
    ]
    for row in rows:
        row["timestamp_utc"] = timestamp
        row["valid_for_claim"] = False
    return rows


def clause_map(value: bool) -> dict[str, bool]:
    return {clause: value for clause in CURRENT_CLAUSES}


def current_input_rows(timestamp: str) -> list[dict[str, Any]]:
    physical = clause_map(False)
    physical["no_GR_import_signed"] = True
    physical["no_tau_fit_signed"] = True

    algebraic_zero = clause_map(False)
    for clause in ("coframe_current_defined_signed", "Jq_variation_identity_signed", "boundary_charge_zero_signed", "source_cell_zero_signed", "no_GR_import_signed", "no_tau_fit_signed"):
        algebraic_zero[clause] = True

    hair = clause_map(False)
    for clause in ("coframe_current_defined_signed", "Jq_variation_identity_signed", "no_GR_import_signed", "no_tau_fit_signed"):
        hair[clause] = True

    signed = clause_map(True)

    def row(current_id: str, route: str, source: str, clauses: dict[str, bool], values: dict[str, Any] | None = None, notes: str = "") -> dict[str, Any]:
        payload: dict[str, Any] = {
            "current_id": current_id,
            "current_route": route,
            "source_path": source,
            "equation_ref": "",
            "Q_cell_abs": "",
            "boundary_charge_abs": "",
            "source_cell_abs": "",
            "counterterm_abs": "",
            "notes": notes,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        payload.update(clauses)
        if values:
            payload.update(values)
        return payload

    return [
        row("physical_coframe_current_missing", "physical_missing", "4802_physical_branch_missing_parent_current", physical),
        row(
            "coframe_current_algebraic_zero_candidate",
            "partial_zero_candidate",
            "SRC4802_03_10_observer_and_SRC4802_04_11_current",
            algebraic_zero,
            {"Q_cell_abs": "0.0", "boundary_charge_abs": "0.0", "source_cell_abs": "0.0", "counterterm_abs": "0.0", "equation_ref": "delta ln J_q = c_T+c_R"},
            "numeric zero is available only if no-charge and same-matter-coframe theorems are parent-owned",
        ),
        row(
            "ordinary_current_hair_unit_control",
            "hair_control",
            "SRC4802_04_11_current",
            hair,
            {"Q_cell_abs": "1.0", "boundary_charge_abs": "0.0", "source_cell_abs": "0.0", "counterterm_abs": "0.0", "equation_ref": "W partial_r R_AB = Q_R"},
            "ordinary current conservation permits a unit reciprocal-cell hair charge",
        ),
        row(
            "conditional_parent_coframe_nocharge",
            "conditional_theorem",
            "conditional_parent_current_nocharge_theorem",
            signed,
            {"Q_cell_abs": "0.0", "boundary_charge_abs": "0.0", "source_cell_abs": "0.0", "counterterm_abs": "0.0", "equation_ref": "Q_cell=boundary=source=0"},
        ),
        row(
            "forbidden_GR_import_current_control",
            "forbidden_control",
            "SCHWARZSCHILD_AB_IMPORT;FIT_TO_BOUND",
            physical,
            {"Q_cell_abs": "0.0", "boundary_charge_abs": "0.0", "source_cell_abs": "0.0", "counterterm_abs": "0.0"},
        ),
    ]


def component_input_rows(timestamp: str, targets: list[dict[str, Any]]) -> list[dict[str, Any]]:
    target = {row["target_id"]: float(row["required_abs_max"]) for row in targets}

    def row(component_id: str, expr: str, arena: str, required: float, value: str = "", source_signed: bool = False, source_path: str = "", equation_ref: str = "", theorem_zero: bool = False, notes: str = "") -> dict[str, Any]:
        return {
            "component_id": component_id,
            "component_expr": expr,
            "arena_pressure": arena,
            "required_abs_max": format_float(required),
            "numeric_abs_value": value,
            "source_signed": source_signed,
            "source_path": source_path,
            "equation_ref": equation_ref,
            "theorem_zero_signed": theorem_zero,
            "notes": notes,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }

    return [
        row("physical_cTR_sum_missing", "abs(c_T+c_R)", "PPN_gamma_and_orbital", target["TGT4802_0_cTR_sum"]),
        row("cTR_sum_zero_candidate_unsigned", "abs(c_T+c_R)", "PPN_gamma_and_orbital", target["TGT4802_0_cTR_sum"], "0.0", False, "SRC4802_01_4801_output", "reciprocal_cell_preserving_no_direct_clock_candidate", False, "candidate zero from 4801, not parent-signed"),
        row("cTR_sum_unit_hair_smoke", "abs(c_T+c_R)", "PPN_gamma_and_orbital", target["TGT4802_0_cTR_sum"], "1.0", False, "SRC4802_01_4801_output", "unit_shear_tau_window_smoke", False, "unit hair remains under current target window but is not a source"),
        row("physical_clock_difference_missing", "abs(c_T-c_clock)+abs(c_alpha)+abs(c_mass)", "clock_redshift", target["TGT4802_1_clock_difference"]),
        row("physical_beta_second_order_missing", "abs(c_beta2)+abs(c_T+c_R)", "PPN_beta", target["TGT4802_2_beta_second_order"]),
        row("physical_source_norm_missing", "abs(c_source_norm)", "orbital_source_normalization", target["TGT4802_3_source_norm"]),
        row("physical_R10_product_missing", "abs(K_R10*q_source*q_test+c_R10_tail)", "R10_anchor_only", target["TGT4802_4_R10_product"]),
        row("conditional_cTR_theorem_zero", "abs(c_T+c_R)", "PPN_gamma_and_orbital", target["TGT4802_0_cTR_sum"], theorem_zero=True, source_signed=True, source_path="conditional_parent_coframe_nocharge", equation_ref="c_T+c_R=0"),
        row("forbidden_component_fit_control", "abs(c_T+c_R)", "PPN_gamma_and_orbital", target["TGT4802_0_cTR_sum"], "0.0", False, "FIT_TO_BOUND;BOUND_AS_SOURCE", "fit control"),
    ]


def obstruction_rows(current_rows: list[dict[str, str]], component_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    by_current = {row["current_id"]: row for row in current_rows}
    by_component = {row["component_id"]: row for row in component_rows}
    return [
        {
            "update_id": "OBS4802_0_current",
            "item": "coframe current/no-charge route",
            "status": by_current["coframe_current_algebraic_zero_candidate"]["runner_status"],
            "value_or_bound": by_current["coframe_current_algebraic_zero_candidate"]["cTR_bound_abs"],
            "meaning": "the algebraic zero route is available but lacks parent no-charge and same-matter-coframe ownership",
        },
        {
            "update_id": "OBS4802_1_hair",
            "item": "ordinary current hair control",
            "status": by_current["ordinary_current_hair_unit_control"]["runner_status"],
            "value_or_bound": by_current["ordinary_current_hair_unit_control"]["cTR_bound_abs"],
            "meaning": "ordinary current conservation still permits Q_R hair; this is why no-charge theorem is required",
        },
        {
            "update_id": "OBS4802_2_component_targets",
            "item": "component source pack",
            "status": "TARGET_WINDOWS_READY_PHYSICAL_COMPONENTS_MISSING",
            "value_or_bound": by_component["physical_cTR_sum_missing"]["required_abs_max"],
            "meaning": "the component scoreboard is installed; physical coefficient/source rows remain missing",
        },
    ]


def gate_rows(current_rows: list[dict[str, str]], component_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    by_current = {row["current_id"]: row for row in current_rows}
    by_component = {row["component_id"]: row for row in component_rows}
    return [
        {
            "gate_id": "PG4802_0_target_windows",
            "claim": "component target bounds are derived from 4800 tau windows",
            "gate_pass": True,
            "reason": "cTR, clock, beta, source normalization and R10 product budgets are computed from existing tau requirements",
            "evidence": str(TARGET_BOUNDS_CSV),
        },
        {
            "gate_id": "PG4802_1_coframe_nocharge",
            "claim": "parent coframe current proves c_T+c_R=0",
            "gate_pass": False,
            "reason": "candidate zero row is numeric/algebraic only; no parent no-charge theorem is signed",
            "evidence": by_current["coframe_current_algebraic_zero_candidate"]["missing_current_inputs"],
        },
        {
            "gate_id": "PG4802_2_unit_hair_budget",
            "claim": "unit cTR hair is under the current target window",
            "gate_pass": by_component["cTR_sum_unit_hair_smoke"]["numeric_window_pass"] == "True",
            "reason": "the current finite residual scale allows O(1) cTR without immediate anchor failure",
            "evidence": by_component["cTR_sum_unit_hair_smoke"]["required_abs_max"],
        },
        {
            "gate_id": "PG4802_3_local_promotion",
            "claim": "local GR/Newton/PPN/R10/clock/orbital pass is allowed",
            "gate_pass": False,
            "reason": "physical component coefficients and parent current/source ownership are still missing",
            "evidence": "nonclaim firewall active",
        },
    ]


def firewall_rows() -> list[dict[str, Any]]:
    return [
        {"firewall_id": "FW4802_0_no_current_shortcut", "rule": "Ordinary current conservation is not a no-charge theorem; Q_R hair must be zeroed or bounded.", "status": "ACTIVE"},
        {"firewall_id": "FW4802_1_no_component_fit", "rule": "Component values cannot be fitted from local bounds; bounds only define target windows.", "status": "ACTIVE"},
        {"firewall_id": "FW4802_2_no_product_shortcut", "rule": "R10 product scoring is forbidden until K_R10, q_source, q_test and tail are individually sourced or theorem-zero.", "status": "ACTIVE"},
        {"firewall_id": "FW4802_3_no_source_norm_absorption", "rule": "Source normalization cannot be absorbed into measured GM while also claiming Newton/GR derivation.", "status": "ACTIVE"},
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC4802_0_scoreboard",
            "decision": "component_target_scoreboard_installed",
            "reason": "the local bridge now asks for specific coefficient combinations, not vague coupling closure",
            "next_action": "fill or theorem-zero cTR first, then clock/source/R10 components",
        },
        {
            "decision_id": "DEC4802_1_best_next",
            "decision": "attack_coframe_reciprocity_current_nocharge_first",
            "reason": "c_T+c_R is the cleanest parent theorem route and controls PPN gamma/orbital pressure directly",
            "next_action": NEXT_TARGET,
        },
    ]


def status_rows(current_rows: list[dict[str, str]], component_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    by_current = {row["current_id"]: row for row in current_rows}
    by_component = {row["component_id"]: row for row in component_rows}
    return [
        {"status_id": "STATUS4802_0_current", "status": by_current["coframe_current_algebraic_zero_candidate"]["runner_status"], "detail": f"cTR={by_current['coframe_current_algebraic_zero_candidate']['cTR_bound_abs']}"},
        {"status_id": "STATUS4802_1_hair", "status": by_current["ordinary_current_hair_unit_control"]["runner_status"], "detail": f"cTR={by_current['ordinary_current_hair_unit_control']['cTR_bound_abs']}"},
        {"status_id": "STATUS4802_2_cTR_target", "status": by_component["physical_cTR_sum_missing"]["runner_status"], "detail": f"required={by_component['physical_cTR_sum_missing']['required_abs_max']}"},
        {"status_id": "STATUS4802_3_selected_next", "status": "COFRAME_RECIPROCITY_CURRENT_NOCHARGE_OR_FINITE_CTR_PRIOR_FILL", "detail": NEXT_TARGET},
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT4802_0_4803",
            "next_target": NEXT_TARGET,
            "trigger": "4802 installs component target windows and selects c_T+c_R as the highest-value theorem/source target",
            "required_inputs": "parent coframe current; no-charge theorem; boundary/source/counterterm ledger; finite cTR prior fallback",
            "valid_for_claim": False,
        }
    ]


def validation_rows(sources: list[dict[str, Any]], current_rows: list[dict[str, str]], component_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    by_current = {row["current_id"]: row for row in current_rows}
    by_component = {row["component_id"]: row for row in component_rows}
    checks: list[tuple[str, str, bool, str]] = [
        ("VAL4802_0_sources", "all cited sources exist and needles are found", all(bool_text(row["exists"]) and bool_text(row["needle_found"]) for row in sources), str(SOURCE_REGISTER_CSV)),
        ("VAL4802_1_physical_current_blocks", "physical coframe current remains blocked", by_current["physical_coframe_current_missing"]["runner_status"] == "BLOCKED_MISSING_COFRAME_CURRENT_INPUTS", str(CURRENT_OUTPUT_CSV)),
        ("VAL4802_2_candidate_zero", "coframe current algebraic zero candidate computes", by_current["coframe_current_algebraic_zero_candidate"]["cTR_bound_abs"] == "0.000000000000000e+00", str(CURRENT_OUTPUT_CSV)),
        ("VAL4802_3_hair_control", "ordinary current hair control computes unit cTR", by_current["ordinary_current_hair_unit_control"]["cTR_bound_abs"] == "1.000000000000000e+00", str(CURRENT_OUTPUT_CSV)),
        ("VAL4802_4_forbidden_current_fails", "GR import current control fails", by_current["forbidden_GR_import_current_control"]["runner_status"] == "FAILED_COFRAME_CURRENT_GATE", str(CURRENT_OUTPUT_CSV)),
        ("VAL4802_5_cTR_target", "physical cTR source row is blocked with target window", by_component["physical_cTR_sum_missing"]["runner_status"] == "BLOCKED_MISSING_COMPONENT_SOURCE_INPUTS" and by_component["physical_cTR_sum_missing"]["required_abs_max"] == "5.256633029822351e+00", str(COMPONENT_OUTPUT_CSV)),
        ("VAL4802_6_unit_cTR_passes", "unit cTR smoke passes target window but remains unsigned", by_component["cTR_sum_unit_hair_smoke"]["numeric_window_pass"] == "True" and by_component["cTR_sum_unit_hair_smoke"]["claim_allowed"] == "False", str(COMPONENT_OUTPUT_CSV)),
        ("VAL4802_7_component_forbidden_fails", "component fit control fails", by_component["forbidden_component_fit_control"]["runner_status"] == "FAILED_COMPONENT_SOURCE_GATE", str(COMPONENT_OUTPUT_CSV)),
        ("VAL4802_8_claim", "claim register includes L-644 as nonclaim", CLAIM_ID in read_text(CLAIMS_PATH) and MARKER in read_text(CLAIMS_PATH), str(CLAIMS_PATH)),
        ("VAL4802_9_resume", "resume points at 4803", NEXT_TARGET in read_text(RESUME_PATH), str(RESUME_PATH)),
    ]
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
            "check_id": "VAL4802_OVERALL",
            "description": "all 4802 parent coframe current/component source-pack checks pass",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "evidence": DECISION,
        }
    )
    return rows


def write_documents(
    timestamp: str,
    sources: list[dict[str, Any]],
    targets: list[dict[str, Any]],
    current_rows: list[dict[str, str]],
    component_rows: list[dict[str, str]],
    obstructions: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    firewalls: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    statuses: list[dict[str, Any]],
    validations: list[dict[str, Any]],
) -> None:
    content = f"""# 4802 - Parent coframe current or tau component source pack

Marker: `{MARKER}`
Generated: `{timestamp}`
Decision: `{DECISION}`

## Result

4802 turns the 4801 tau formulas into a parent-current gate and a finite component source-pack scoreboard.

The coframe identity is:

```text
J_q = T sqrt(S)
delta ln J_q = delta ln T + delta ln sqrt(S)
tau_gamma = |c_T + c_R|
```

So the first parent theorem target is:

```text
c_T + c_R = 0
```

This can come from a genuine coframe-current no-charge theorem, a parent `B_C/Phi_C` no-flux/source theorem, or a finite sourced `c_T+c_R` row. Ordinary current conservation alone is still not enough because it permits `Q_R` hair.

## Component Target Bounds

{markdown_table(targets, ["target_id", "component_expr", "arena_pressure", "required_abs_max", "meaning"])}

## Source Register

{markdown_table(sources, ["source_id", "source_path", "exists", "needle_found", "role"])}

## Coframe Current Output

{markdown_table(current_rows, ["current_id", "current_route", "cTR_bound_abs", "tau_gamma_abs", "current_nocharge_theorem", "runner_status", "missing_current_inputs", "anti_circularity_status"])}

## Component Source Output

{markdown_table(component_rows, ["component_id", "component_expr", "arena_pressure", "component_abs_value", "required_abs_max", "numeric_window_pass", "runner_status", "missing_component_inputs", "anti_circularity_status"])}

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

    formal_content = f"""# 818 - PPC4161 parent coframe current or tau component source pack

Marker: `{MARKER}`
Generated: `{timestamp}`

## Formal Update

4802 makes the local projection programme component-scored:

```text
abs(c_T+c_R) <= min(tau_gamma_max, tau_orbital_max)
abs(c_T-c_clock)+abs(c_alpha)+abs(c_mass) <= tau_clock_max
abs(c_beta2)+abs(c_T+c_R) <= tau_beta_max
abs(c_source_norm) <= tau_orbital_max
abs(K_R10 q_source q_test + tail_R10) <= tau_R10_max
```

The highest-value next proof/source target is `c_T+c_R`: either a parent no-charge coframe current proves it zero, or a finite prior row must be sourced without fitting to bounds.

See `{DOC_PATH}`.
"""
    write_text(FORMAL_PATH, formal_content)


def update_registers(timestamp: str) -> None:
    claim_line = (
        f'{CLAIM_ID},parent_coframe_component_source_pack_runner,'
        f'"4802 installs a parent coframe-current no-charge gate and a component source-pack scoreboard for c_T+c_R, clock/readout, beta, source-normalization, and R10 product channels.",'
        f'"Generated source register, current input/output, component target bounds, component source input/output, gates, firewalls, decision, status, next target and validation.",'
        f'parent_coframe_current_component_source_pack_private_nonclaim,'
        f'{NEXT_TARGET},'
        f'"Do not treat ordinary current conservation, unit component smoke, or target bounds as parent-derived local-GR evidence.",'
        f'local_gr,{DOC_PATH},{NEXT_TARGET},'
        f'ordinary current as no-charge; component fit to bound; R10 product shortcut; source-normalization absorption; GR import,'
        f'"Parent coframe current and component source pack",'
        f'{MARKER}; {DECISION}; generated {timestamp}\n'
    )
    if CLAIM_ID not in read_text(CLAIMS_PATH):
        with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
            handle.write(claim_line)

    spine_block = f"""
## {MARKER}

4802 creates the local component scoreboard:

```text
abs(c_T+c_R) <= min(tau_gamma_max, tau_orbital_max)
abs(c_T-c_clock)+abs(c_alpha)+abs(c_mass) <= tau_clock_max
abs(c_source_norm) <= tau_orbital_max
```

This is progress because the parent-action problem is now pointed at named coefficients. The first target is `c_T+c_R`, since it is the reciprocal-cell/shear channel controlling PPN gamma pressure.
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
Last checkpoint: `4802-Y5-R2FR-parent-coframe-current-or-tau-component-source-pack.md`
Marker: `{MARKER}`

## Where we are

4802 installed the component source-pack scoreboard:

```text
abs(c_T+c_R) <= min(tau_gamma_max, tau_orbital_max)
abs(c_T-c_clock)+abs(c_alpha)+abs(c_mass) <= tau_clock_max
abs(c_beta2)+abs(c_T+c_R) <= tau_beta_max
abs(c_source_norm) <= tau_orbital_max
abs(K_R10 q_source q_test + tail_R10) <= tau_R10_max
```

The first target is `c_T+c_R`: prove it zero from a parent coframe no-charge/current theorem, or source a finite prior row. Ordinary current conservation is not enough because it permits `Q_R` hair.

## Live blockers

- Parent no-charge theorem for the coframe current is not signed.
- Physical component rows for clock/readout, beta, source normalization and R10 are still missing.
- Unit component smoke rows are scale checks only; no local-GR claim follows.

## Next target

`{NEXT_TARGET}`
"""
    write_text(RESUME_PATH, resume)


def main() -> int:
    timestamp = now()
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    SCRIPT_DIR.mkdir(parents=True, exist_ok=True)

    write_text(RUNNER, RUNNER_TEXT)
    windows = load_tau_windows()
    sources = source_register(timestamp)
    targets = target_bound_rows(timestamp, windows)
    current_inputs = current_input_rows(timestamp)
    component_inputs = component_input_rows(timestamp, targets)

    write_csv(SOURCE_REGISTER_CSV, sources)
    write_csv(TARGET_BOUNDS_CSV, targets)
    write_csv(CURRENT_INPUT_CSV, current_inputs)
    write_csv(COMPONENT_INPUT_CSV, component_inputs)

    python = sys.executable
    run_command([python, str(RUNNER), "current", str(CURRENT_INPUT_CSV), str(CURRENT_OUTPUT_CSV)])
    run_command([python, str(RUNNER), "component", str(COMPONENT_INPUT_CSV), str(COMPONENT_OUTPUT_CSV)])

    current_rows = parse_csv(CURRENT_OUTPUT_CSV)
    component_rows = parse_csv(COMPONENT_OUTPUT_CSV)
    obstructions = obstruction_rows(current_rows, component_rows)
    gates = gate_rows(current_rows, component_rows)
    firewalls = firewall_rows()
    decisions = decision_rows()
    statuses = status_rows(current_rows, component_rows)
    next_targets = next_target_rows()

    write_csv(OBSTRUCTION_CSV, obstructions)
    write_csv(GATE_CSV, gates)
    write_csv(FIREWALL_CSV, firewalls)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_TARGET_CSV, next_targets)

    update_registers(timestamp)
    validations = validation_rows(sources, current_rows, component_rows)
    write_csv(VALIDATION_CSV, validations)
    write_documents(timestamp, sources, targets, current_rows, component_rows, obstructions, gates, firewalls, decisions, statuses, validations)

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
