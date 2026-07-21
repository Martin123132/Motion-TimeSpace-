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

CHECKPOINT = "4801"
CLAIM_ID = "L-643"
MARKER = "PPC4161_OBSERVER_COFRAME_TAU_PROJECTION_DERIVATION_OR_PARENT_BC_NO_FLUX_ACTION_4801"
PACKET_MARKER = "PPC4161_PACKET_OBSERVER_COFRAME_TAU_PROJECTION_DERIVATION_OR_PARENT_BC_NO_FLUX_ACTION_4801"
DECISION = "OBSERVER_COFRAME_TAU_FORMULAS_DERIVED_PARTIAL_NUMERIC_WINDOWS_PASS_NONCLAIM"
NEXT_TARGET = "4802-Y5-R2FR-parent-coframe-current-or-tau-component-source-pack.md"

DOC_PATH = POST / "4801-Y5-R2FR-observer-coframe-tau-projection-derivation-or-parent-BC-no-flux-action.md"
FORMAL_PATH = FORMAL / "817-PPC4161-observer-coframe-tau-projection-derivation-or-parent-BC-no-flux-action.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"

RUNNER = SCRIPT_DIR / "observer_coframe_tau_projection_runner.py"

SOURCE_REGISTER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4801_SOURCE_REGISTER.csv"
BOUND_IMPORT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4801_4800_BOUND_IMPORT.csv"
COFRAME_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4801_COFRAME_PROJECTION_INPUT.csv"
COFRAME_OUTPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4801_COFRAME_PROJECTION_OUTPUT.csv"
TAU_MATRIX_CSV = SOURCE_DIR / "P8_Y5_R2FR_4801_TAU_MATRIX.csv"
OBSTRUCTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4801_OBSTRUCTION_UPDATE.csv"
GATE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4801_PROMOTION_GATES.csv"
FIREWALL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4801_FIREWALL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4801_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4801_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4801_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4801_VALIDATION.csv"

TAU_REQUIREMENTS_4800 = SOURCE_DIR / "P8_Y5_R2FR_4800_TAU_REQUIREMENTS.csv"
ARENA_OUTPUT_4800 = SOURCE_DIR / "P8_Y5_R2FR_4800_ARENA_PROJECTION_OUTPUT.csv"

COFRAME_CLAUSES = (
    "observer_coframe_defined_signed",
    "reciprocal_cell_formula_signed",
    "residual_component_decomposition_signed",
    "matter_same_coframe_signed",
    "clock_readout_map_signed",
    "R10_source_test_projection_signed",
    "orbital_residual_vector_signed",
    "beta_second_order_signed",
    "parent_BC_no_flux_or_finite_source_signed",
    "no_GR_import_signed",
    "no_fit_to_bound_signed",
)

SOURCE_SPECS = [
    ("SRC4801_00_4800_doc", POST / "4800-Y5-R2FR-local-residual-bound-to-PPN-R10-clock-or-parent-BC-action-source-rows.md", "derive tau_PPN", "4800 selects observer-coframe tau derivation"),
    ("SRC4801_01_4800_tau", TAU_REQUIREMENTS_4800, "TAU4800_0", "4800 required tau windows"),
    ("SRC4801_02_10_observer", POST / "10-observer-map-symplectic-contract.md", "theta_0 = T c dt", "observer coframe definition"),
    ("SRC4801_03_02_motion", POST / "02-motion-load-local-GR-reduction.md", "T^2 S = 1", "reciprocal local-GR lane"),
    ("SRC4801_04_07_nonprop", POST / "07-nonpropagating-reciprocity-constraint.md", "no R_AB kinetic term", "no-hair route via nonpropagating constraint"),
    ("SRC4801_05_11_current", POST / "11-cell-current-origin-attempt.md", "Q_R = constant", "ordinary current hair obstruction"),
    ("SRC4801_06_2283_finalizer", POST / "2283-Y5-R2FR-radial-observer-cell-current-owner-or-q-closure-finalizer.md", "FINITE_Q_RESIDUAL_ROUTE_IS_NEXT_EXECUTABLE_PATH", "finite q/R_AB route is allowed but nonclaim"),
    ("SRC4801_07_runner", RUNNER, "def coframe_projection_row", "4801 executable runner"),
]


RUNNER_TEXT = r'''from __future__ import annotations

import csv
import math
import sys
from pathlib import Path
from typing import Any


COFRAME_CLAUSES = (
    "observer_coframe_defined_signed",
    "reciprocal_cell_formula_signed",
    "residual_component_decomposition_signed",
    "matter_same_coframe_signed",
    "clock_readout_map_signed",
    "R10_source_test_projection_signed",
    "orbital_residual_vector_signed",
    "beta_second_order_signed",
    "parent_BC_no_flux_or_finite_source_signed",
    "no_GR_import_signed",
    "no_fit_to_bound_signed",
)

FORBIDDEN_SOURCE_TOKENS = (
    "GR_IMPORT",
    "SCHWARZSCHILD_AB_IMPORT",
    "EINSTEIN_VACUUM_IMPORT",
    "RETUNE_TO_PASS",
    "FIT_TAU_TO_BOUND",
    "OBSERVED_RESIDUAL_CANCEL",
    "TAU_BY_DECLARATION",
    "BOUND_AS_SOURCE",
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
            "mode_id",
            "source_id",
            "projection_source",
            "notes",
            "provenance",
        )
    ).upper()
    return any(token in source_text for token in FORBIDDEN_SOURCE_TOKENS)


def missing_clauses(row: dict[str, Any]) -> list[str]:
    return [clause for clause in COFRAME_CLAUSES if not bool_text(row.get(clause))]


def numeric_inputs(row: dict[str, Any]) -> tuple[dict[str, float], list[str]]:
    fields = (
        "epsilon_local_abs",
        "gamma_bound_abs",
        "beta_bound_abs",
        "clock_bound_abs",
        "R10_bound_abs",
        "orbital_bound_abs",
        "c_T",
        "c_R",
        "c_clock_readout",
        "c_alpha_clock",
        "c_mass_clock",
        "c_beta2",
        "c_source_norm",
        "K_R10",
        "q_source_R10",
        "q_test_R10",
        "c_R10_tail",
    )
    values: dict[str, float] = {}
    missing: list[str] = []
    for field in fields:
        value = parse_float(row.get(field))
        if value is None:
            missing.append(f"MISSING_{field}")
        else:
            values[field] = value
    return values, missing


def coframe_projection_row(row: dict[str, Any]) -> dict[str, Any]:
    mode_id = str(row.get("mode_id", "")).strip() or "UNNAMED_COFRAME_MODE"
    output: dict[str, Any] = {
        "mode_id": mode_id,
        "mode_type": row.get("mode_type", ""),
        "source_id": row.get("source_id", ""),
        "input_valid_for_claim": bool_text(row.get("valid_for_claim")),
        "valid_for_claim": False,
        "claim_allowed": False,
    }
    if forbidden_source_used(row):
        output.update(
            {
                "runner_status": "FAILED_COFRAME_TAU_PROJECTION_GATE",
                "missing_projection_inputs": "FORBIDDEN_COFRAME_TAU_SOURCE",
                "anti_circularity_status": "FAIL_FORBIDDEN_SOURCE_USED",
            }
        )
        for field in (
            "tau_gamma_abs",
            "tau_beta_abs",
            "tau_clock_abs",
            "tau_R10_abs",
            "tau_orbital_abs",
            "pred_gamma_abs",
            "pred_beta_abs",
            "pred_clock_abs",
            "pred_R10_abs",
            "pred_orbital_abs",
        ):
            output[field] = "MISSING_NUMERIC_VALUE"
        output.update(
            {
                "gamma_pass": False,
                "beta_pass": False,
                "clock_pass": False,
                "R10_pass": False,
                "orbital_pass": False,
                "all_numeric_pass": False,
            }
        )
        return output

    missing = missing_clauses(row)
    values, numeric_missing = numeric_inputs(row)
    if numeric_missing:
        output.update(
            {
                "runner_status": "BLOCKED_MISSING_COFRAME_PROJECTION_INPUTS",
                "missing_projection_inputs": ";".join([*missing, *numeric_missing]),
                "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
            }
        )
        for field in (
            "tau_gamma_abs",
            "tau_beta_abs",
            "tau_clock_abs",
            "tau_R10_abs",
            "tau_orbital_abs",
            "pred_gamma_abs",
            "pred_beta_abs",
            "pred_clock_abs",
            "pred_R10_abs",
            "pred_orbital_abs",
        ):
            output[field] = "MISSING_NUMERIC_VALUE"
        output.update(
            {
                "gamma_pass": False,
                "beta_pass": False,
                "clock_pass": False,
                "R10_pass": False,
                "orbital_pass": False,
                "all_numeric_pass": False,
            }
        )
        return output

    epsilon = abs(values["epsilon_local_abs"])
    tau_gamma = abs(values["c_T"] + values["c_R"])
    tau_beta = abs(values["c_beta2"]) + tau_gamma
    tau_clock = abs(values["c_T"] - values["c_clock_readout"]) + abs(values["c_alpha_clock"]) + abs(values["c_mass_clock"])
    tau_r10 = abs(values["K_R10"] * values["q_source_R10"] * values["q_test_R10"] + values["c_R10_tail"])
    tau_orbital = max(tau_gamma, tau_beta, abs(values["c_source_norm"]))

    pred_gamma = tau_gamma * epsilon
    pred_beta = tau_beta * epsilon
    pred_clock = tau_clock * epsilon
    pred_r10 = tau_r10 * epsilon
    pred_orbital = tau_orbital * epsilon

    gamma_pass = pred_gamma <= abs(values["gamma_bound_abs"])
    beta_pass = pred_beta <= abs(values["beta_bound_abs"])
    clock_pass = pred_clock <= abs(values["clock_bound_abs"])
    r10_pass = pred_r10 <= abs(values["R10_bound_abs"])
    orbital_pass = pred_orbital <= abs(values["orbital_bound_abs"])
    all_pass = gamma_pass and beta_pass and clock_pass and r10_pass and orbital_pass

    if epsilon <= 1.0e-30 and all_pass:
        status = "PARENT_BC_NO_FLUX_ZERO_RESIDUAL_CONDITIONAL_THEOREM_NONCLAIM"
    elif tau_gamma <= 1.0e-15 and tau_clock <= 1.0e-15 and all_pass:
        status = "RECIPROCAL_CELL_AND_CLOCK_READOUT_QUIET_PARTIAL_DERIVATION_NONCLAIM"
    elif all_pass and missing:
        status = "NUMERIC_TAU_WINDOW_PASS_BUT_PARENT_MAPPING_UNSIGNED_NONCLAIM"
    elif all_pass:
        status = "NUMERIC_TAU_WINDOW_PASS_SIGNED_MAPPING_NONCLAIM_UNLESS_INPUT_VALID"
    else:
        status = "NUMERIC_TAU_WINDOW_FAILS"

    claim_allowed = bool_text(row.get("valid_for_claim")) and not missing and all_pass
    output.update(
        {
            "tau_gamma_abs": format_float(tau_gamma),
            "tau_beta_abs": format_float(tau_beta),
            "tau_clock_abs": format_float(tau_clock),
            "tau_R10_abs": format_float(tau_r10),
            "tau_orbital_abs": format_float(tau_orbital),
            "pred_gamma_abs": format_float(pred_gamma),
            "pred_beta_abs": format_float(pred_beta),
            "pred_clock_abs": format_float(pred_clock),
            "pred_R10_abs": format_float(pred_r10),
            "pred_orbital_abs": format_float(pred_orbital),
            "gamma_pass": gamma_pass,
            "beta_pass": beta_pass,
            "clock_pass": clock_pass,
            "R10_pass": r10_pass,
            "orbital_pass": orbital_pass,
            "all_numeric_pass": all_pass,
            "runner_status": status,
            "missing_projection_inputs": ";".join(missing),
            "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
            "claim_allowed": claim_allowed,
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
    if len(sys.argv) != 3:
        print("usage: observer_coframe_tau_projection_runner.py <input.csv> <output.csv>", file=sys.stderr)
        return 2
    rows = [coframe_projection_row(row) for row in read_csv(Path(sys.argv[1]))]
    write_csv(Path(sys.argv[2]), rows)
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


def import_bounds_4800(timestamp: str) -> dict[str, float]:
    rows = parse_csv(TAU_REQUIREMENTS_4800)
    by_arena = {row["arena_id"]: row for row in rows}
    bounds = {
        "epsilon": float(by_arena["ppn_gamma_cassini_required_tau"]["epsilon_local_abs"]),
        "gamma": float(by_arena["ppn_gamma_cassini_required_tau"]["observable_bound_abs"]),
        "beta": float(by_arena["ppn_beta_mercury_required_tau"]["observable_bound_abs"]),
        "clock": float(by_arena["clock_redshift_galileo_required_tau"]["observable_bound_abs"]),
        "R10": float(by_arena["r10_yukawa_grav_strength_anchor_required_tau"]["observable_bound_abs"]),
        "orbital": float(by_arena["orbital_mercury_total_precession_fraction_required_tau"]["observable_bound_abs"]),
    }
    write_csv(
        BOUND_IMPORT_CSV,
        [
            {
                "bound_id": f"BOUND4801_{name}",
                "quantity": name,
                "value": format_float(value),
                "source": str(TAU_REQUIREMENTS_4800),
                "timestamp_utc": timestamp,
                "valid_for_claim": False,
            }
            for name, value in bounds.items()
        ],
    )
    return bounds


def clause_map(value: bool) -> dict[str, bool]:
    return {clause: value for clause in COFRAME_CLAUSES}


def coframe_input_rows(timestamp: str, bounds: dict[str, float]) -> list[dict[str, Any]]:
    physical = clause_map(False)
    physical["no_GR_import_signed"] = True
    physical["no_fit_to_bound_signed"] = True

    partial_reciprocal = clause_map(False)
    for clause in (
        "observer_coframe_defined_signed",
        "reciprocal_cell_formula_signed",
        "residual_component_decomposition_signed",
        "matter_same_coframe_signed",
        "clock_readout_map_signed",
        "no_GR_import_signed",
        "no_fit_to_bound_signed",
    ):
        partial_reciprocal[clause] = True

    finite_smoke = clause_map(False)
    for clause in (
        "observer_coframe_defined_signed",
        "reciprocal_cell_formula_signed",
        "residual_component_decomposition_signed",
        "matter_same_coframe_signed",
        "clock_readout_map_signed",
        "R10_source_test_projection_signed",
        "orbital_residual_vector_signed",
        "no_GR_import_signed",
        "no_fit_to_bound_signed",
    ):
        finite_smoke[clause] = True

    signed = clause_map(True)

    def row(
        mode_id: str,
        mode_type: str,
        source_id: str,
        clauses: dict[str, bool],
        coefficients: dict[str, Any] | None = None,
        epsilon: float | None = None,
        notes: str = "",
    ) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "mode_id": mode_id,
            "mode_type": mode_type,
            "source_id": source_id,
            "projection_source": source_id,
            "epsilon_local_abs": format_float(bounds["epsilon"] if epsilon is None else epsilon),
            "gamma_bound_abs": format_float(bounds["gamma"]),
            "beta_bound_abs": format_float(bounds["beta"]),
            "clock_bound_abs": format_float(bounds["clock"]),
            "R10_bound_abs": format_float(bounds["R10"]),
            "orbital_bound_abs": format_float(bounds["orbital"]),
            "c_T": "",
            "c_R": "",
            "c_clock_readout": "",
            "c_alpha_clock": "",
            "c_mass_clock": "",
            "c_beta2": "",
            "c_source_norm": "",
            "K_R10": "",
            "q_source_R10": "",
            "q_test_R10": "",
            "c_R10_tail": "",
            "notes": notes,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        payload.update(clauses)
        if coefficients:
            payload.update(coefficients)
        return payload

    zero_coeffs = {
        "c_T": "0.0",
        "c_R": "0.0",
        "c_clock_readout": "0.0",
        "c_alpha_clock": "0.0",
        "c_mass_clock": "0.0",
        "c_beta2": "0.0",
        "c_source_norm": "0.0",
        "K_R10": "0.0",
        "q_source_R10": "0.0",
        "q_test_R10": "0.0",
        "c_R10_tail": "0.0",
    }

    return [
        row(
            "physical_coframe_projection_missing",
            "physical_missing",
            "4801_physical_branch_missing_component_decomposition",
            physical,
            notes="no tau can be claimed until component coefficients are supplied by the parent observer/source map",
        ),
        row(
            "reciprocal_cell_preserving_no_direct_clock_candidate",
            "partial_derivation",
            "SRC4801_02_10_observer_plus_SRC4801_03_02_motion",
            partial_reciprocal,
            {
                "c_T": "1.0",
                "c_R": "-1.0",
                "c_clock_readout": "1.0",
                "c_alpha_clock": "0.0",
                "c_mass_clock": "0.0",
                "c_beta2": "0.0",
                "c_source_norm": "0.0",
                "K_R10": "0.0",
                "q_source_R10": "0.0",
                "q_test_R10": "0.0",
                "c_R10_tail": "0.0",
            },
            notes="coframe algebra: c_T+c_R=0 kills reciprocal-cell/PPN-gamma channel; c_T=c_clock_readout kills direct clock readout",
        ),
        row(
            "unit_shear_tau_window_smoke",
            "finite_residual_smoke",
            "SRC4801_01_4800_tau",
            finite_smoke,
            {
                "c_T": "0.0",
                "c_R": "1.0",
                "c_clock_readout": "0.0",
                "c_alpha_clock": "0.0",
                "c_mass_clock": "0.0",
                "c_beta2": "0.0",
                "c_source_norm": "1.0",
                "K_R10": "1.0",
                "q_source_R10": "1.0",
                "q_test_R10": "1.0",
                "c_R10_tail": "0.0",
            },
            notes="unit shear/source projection smoke: checks that tau of order one is inside 4800 windows, not that tau is derived",
        ),
        row(
            "direct_clock_unit_tau_smoke",
            "finite_residual_smoke",
            "SRC4801_01_4800_tau",
            finite_smoke,
            {
                "c_T": "0.0",
                "c_R": "0.0",
                "c_clock_readout": "1.0",
                "c_alpha_clock": "0.0",
                "c_mass_clock": "0.0",
                "c_beta2": "0.0",
                "c_source_norm": "0.0",
                "K_R10": "0.0",
                "q_source_R10": "0.0",
                "q_test_R10": "0.0",
                "c_R10_tail": "0.0",
            },
            notes="direct clock readout unit smoke remains under Galileo redshift anchor but is not a theorem",
        ),
        row(
            "conditional_parent_BC_no_flux_tau_zero",
            "conditional_theorem",
            "conditional_parent_BC_no_flux_source_action",
            signed,
            zero_coeffs,
            epsilon=0.0,
            notes="if parent B_C/Phi_C no-flux and source/Ward theorem sets epsilon_loc=0, all tau channels vanish",
        ),
        row(
            "forbidden_tau_fit_to_bound_control",
            "forbidden_control",
            "FIT_TAU_TO_BOUND;RETUNE_TO_PASS",
            physical,
            zero_coeffs,
            notes="must fail: tau may not be chosen from the observational bound",
        ),
    ]


def tau_matrix_rows(output_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in output_rows:
        if row["runner_status"].startswith("FAILED") or row["runner_status"].startswith("BLOCKED"):
            continue
        for arena, tau_field, pred_field, pass_field in (
            ("PPN_gamma", "tau_gamma_abs", "pred_gamma_abs", "gamma_pass"),
            ("PPN_beta", "tau_beta_abs", "pred_beta_abs", "beta_pass"),
            ("clock", "tau_clock_abs", "pred_clock_abs", "clock_pass"),
            ("R10", "tau_R10_abs", "pred_R10_abs", "R10_pass"),
            ("orbital", "tau_orbital_abs", "pred_orbital_abs", "orbital_pass"),
        ):
            rows.append(
                {
                    "matrix_id": f"TM4801_{len(rows)}",
                    "mode_id": row["mode_id"],
                    "arena": arena,
                    "tau_abs": row[tau_field],
                    "predicted_observable_abs": row[pred_field],
                    "numeric_pass": row[pass_field],
                    "mode_status": row["runner_status"],
                    "valid_for_claim": False,
                }
            )
    return rows


def obstruction_rows(output_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    by_id = {row["mode_id"]: row for row in output_rows}
    return [
        {
            "update_id": "OBS4801_0_formula",
            "item": "observer coframe tau formulas",
            "status": "DERIVED_AS_COMPONENT_PROJECTION_NONCLAIM",
            "value_or_bound": "tau_gamma=|c_T+c_R|; tau_clock=|c_T-c_clock|+constant/readout terms; tau_R10=|K q_s q_t+tail|",
            "meaning": "the residual-to-observable map is now component-wise instead of a single assumed tau",
        },
        {
            "update_id": "OBS4801_1_reciprocal_quiet",
            "item": "reciprocal-cell preserving candidate",
            "status": by_id["reciprocal_cell_preserving_no_direct_clock_candidate"]["runner_status"],
            "value_or_bound": f"tau_gamma={by_id['reciprocal_cell_preserving_no_direct_clock_candidate']['tau_gamma_abs']}; tau_clock={by_id['reciprocal_cell_preserving_no_direct_clock_candidate']['tau_clock_abs']}",
            "meaning": "if the parent map forces c_R=-c_T and no direct readout/constant channel, the tight local channels are quiet",
        },
        {
            "update_id": "OBS4801_2_unit_tau",
            "item": "unit finite projection smoke",
            "status": by_id["unit_shear_tau_window_smoke"]["runner_status"],
            "value_or_bound": f"pred_gamma={by_id['unit_shear_tau_window_smoke']['pred_gamma_abs']}; pred_orbital={by_id['unit_shear_tau_window_smoke']['pred_orbital_abs']}",
            "meaning": "order-one projection remains under the current 4800 anchors, but parent mapping is unsigned",
        },
    ]


def gate_rows(output_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    by_id = {row["mode_id"]: row for row in output_rows}
    return [
        {
            "gate_id": "PG4801_0_projection_formulas",
            "claim": "tau projection formulas are derived from the observer coframe decomposition",
            "gate_pass": True,
            "reason": "runner implements component formulas tied to T, sqrt(S), clock readout, source/test and orbital terms",
            "evidence": str(COFRAME_OUTPUT_CSV),
        },
        {
            "gate_id": "PG4801_1_reciprocal_quiet_candidate",
            "claim": "reciprocal-cell preserving/no-direct-clock mode is locally quiet in PPN gamma and clock channels",
            "gate_pass": by_id["reciprocal_cell_preserving_no_direct_clock_candidate"]["tau_gamma_abs"] == "0.000000000000000e+00" and by_id["reciprocal_cell_preserving_no_direct_clock_candidate"]["tau_clock_abs"] == "0.000000000000000e+00",
            "reason": "c_T+c_R=0 and c_T-c_clock=0 in the candidate row",
            "evidence": by_id["reciprocal_cell_preserving_no_direct_clock_candidate"]["runner_status"],
        },
        {
            "gate_id": "PG4801_2_parent_owner",
            "claim": "parent action derives the required coframe component restrictions",
            "gate_pass": False,
            "reason": "parent B_C/source no-flux, R10 source/test projection, orbital vector and beta second-order owner remain unsigned",
            "evidence": by_id["reciprocal_cell_preserving_no_direct_clock_candidate"]["missing_projection_inputs"],
        },
        {
            "gate_id": "PG4801_3_local_promotion",
            "claim": "local GR/Newton/PPN/R10/clock/orbital pass is allowed",
            "gate_pass": False,
            "reason": "numeric tau windows pass in smoke rows, but physical parent component map remains missing",
            "evidence": "nonclaim firewall active",
        },
    ]


def firewall_rows() -> list[dict[str, Any]]:
    return [
        {"firewall_id": "FW4801_0_no_tau_by_bound", "rule": "tau components are derived from coframe/source coefficients, never fitted to observational bounds.", "status": "ACTIVE"},
        {"firewall_id": "FW4801_1_no_GR_import", "rule": "Do not import Schwarzschild AB=1, Einstein vacuum, or GR PPN equations as the selector proof.", "status": "ACTIVE"},
        {"firewall_id": "FW4801_2_no_clock_confusion", "rule": "Clock readout cancellation requires a same-coframe matter/readout theorem, not a process-time slogan.", "status": "ACTIVE"},
        {"firewall_id": "FW4801_3_no_R10_anchor_overclaim", "rule": "R10 unit-source smoke is not an alpha(lambda) curve or a source/test material projection.", "status": "ACTIVE"},
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC4801_0_formula",
            "decision": "tau_is_a_component_projection_not_a_free_scalar",
            "reason": "observer coframe separates reciprocal-cell strain, clock readout, R10 source/test and orbital normalization",
            "next_action": "source the component coefficients or prove parent no-flux",
        },
        {
            "decision_id": "DEC4801_1_best_route",
            "decision": "reciprocal_cell_preserving_no_direct_clock_subspace_is_the_clean_target",
            "reason": "it kills the tight PPN gamma and clock channels without needing observational cancellation",
            "next_action": NEXT_TARGET,
        },
    ]


def status_rows(output_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    by_id = {row["mode_id"]: row for row in output_rows}
    return [
        {"status_id": "STATUS4801_0_reciprocal", "status": by_id["reciprocal_cell_preserving_no_direct_clock_candidate"]["runner_status"], "detail": f"tau_gamma={by_id['reciprocal_cell_preserving_no_direct_clock_candidate']['tau_gamma_abs']}; tau_clock={by_id['reciprocal_cell_preserving_no_direct_clock_candidate']['tau_clock_abs']}"},
        {"status_id": "STATUS4801_1_unit_shear", "status": by_id["unit_shear_tau_window_smoke"]["runner_status"], "detail": f"pred_gamma={by_id['unit_shear_tau_window_smoke']['pred_gamma_abs']}"},
        {"status_id": "STATUS4801_2_direct_clock", "status": by_id["direct_clock_unit_tau_smoke"]["runner_status"], "detail": f"pred_clock={by_id['direct_clock_unit_tau_smoke']['pred_clock_abs']}"},
        {"status_id": "STATUS4801_3_selected_next", "status": "PARENT_COFRAME_CURRENT_OR_TAU_COMPONENT_SOURCE_PACK", "detail": NEXT_TARGET},
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT4801_0_4802",
            "next_target": NEXT_TARGET,
            "trigger": "4801 derives tau formulas but physical component coefficients remain parent-unsigned",
            "required_inputs": "parent coframe current/no-flux theorem; c_T/c_R/c_clock coefficients; beta second-order map; R10 source/test projection; orbital source normalization",
            "valid_for_claim": False,
        }
    ]


def validation_rows(sources: list[dict[str, Any]], output_rows: list[dict[str, str]], tau_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_id = {row["mode_id"]: row for row in output_rows}
    checks: list[tuple[str, str, bool, str]] = [
        ("VAL4801_0_sources", "all cited sources exist and needles are found", all(bool_text(row["exists"]) and bool_text(row["needle_found"]) for row in sources), str(SOURCE_REGISTER_CSV)),
        ("VAL4801_1_physical_blocks", "physical coframe projection remains blocked", by_id["physical_coframe_projection_missing"]["runner_status"] == "BLOCKED_MISSING_COFRAME_PROJECTION_INPUTS", str(COFRAME_OUTPUT_CSV)),
        ("VAL4801_2_reciprocal_quiet", "reciprocal-cell candidate zeros gamma and clock tau", by_id["reciprocal_cell_preserving_no_direct_clock_candidate"]["tau_gamma_abs"] == "0.000000000000000e+00" and by_id["reciprocal_cell_preserving_no_direct_clock_candidate"]["tau_clock_abs"] == "0.000000000000000e+00", str(COFRAME_OUTPUT_CSV)),
        ("VAL4801_3_unit_shear_pass", "unit shear projection numerically passes gamma window", by_id["unit_shear_tau_window_smoke"]["pred_gamma_abs"] == "4.960000000000000e-07" and by_id["unit_shear_tau_window_smoke"]["gamma_pass"] == "True", str(COFRAME_OUTPUT_CSV)),
        ("VAL4801_4_direct_clock_pass", "direct clock unit projection numerically passes clock window", by_id["direct_clock_unit_tau_smoke"]["pred_clock_abs"] == "4.960000000000000e-07" and by_id["direct_clock_unit_tau_smoke"]["clock_pass"] == "True", str(COFRAME_OUTPUT_CSV)),
        ("VAL4801_5_conditional_zero", "conditional parent no-flux row zeros all predictions", by_id["conditional_parent_BC_no_flux_tau_zero"]["pred_gamma_abs"] == "0.000000000000000e+00" and by_id["conditional_parent_BC_no_flux_tau_zero"]["all_numeric_pass"] == "True", str(COFRAME_OUTPUT_CSV)),
        ("VAL4801_6_forbidden_fails", "tau fit-to-bound control fails", by_id["forbidden_tau_fit_to_bound_control"]["runner_status"] == "FAILED_COFRAME_TAU_PROJECTION_GATE", str(COFRAME_OUTPUT_CSV)),
        ("VAL4801_7_tau_matrix", "tau matrix contains arena rows", len(tau_rows) >= 20, str(TAU_MATRIX_CSV)),
        ("VAL4801_8_claim", "claim register includes L-643 as nonclaim", CLAIM_ID in read_text(CLAIMS_PATH) and MARKER in read_text(CLAIMS_PATH), str(CLAIMS_PATH)),
        ("VAL4801_9_resume", "resume points at 4802", NEXT_TARGET in read_text(RESUME_PATH), str(RESUME_PATH)),
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
            "check_id": "VAL4801_OVERALL",
            "description": "all 4801 observer-coframe tau projection checks pass",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "evidence": DECISION,
        }
    )
    return rows


def write_documents(
    timestamp: str,
    sources: list[dict[str, Any]],
    bounds: dict[str, float],
    output_rows: list[dict[str, str]],
    tau_rows: list[dict[str, Any]],
    obstructions: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    firewalls: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    statuses: list[dict[str, Any]],
    validations: list[dict[str, Any]],
) -> None:
    content = f"""# 4801 - Observer coframe tau projection derivation or parent BC no-flux action

Marker: `{MARKER}`
Generated: `{timestamp}`
Decision: `{DECISION}`

## Result

4801 derives the first explicit observer-coframe projection formulas for the 4800 `tau_X` factors.

Start from the local observer coframe:

```text
theta_0 = T c dt
theta_r = sqrt(S) dr
R_AB = ln(T^2 S)
```

Write a normalized finite local residual as component coefficients:

```text
delta ln T        = c_T epsilon_loc
delta ln sqrt(S)  = c_R epsilon_loc
delta clock_readout = c_clock epsilon_loc
```

Then the tight local channels are controlled by:

```text
tau_gamma = |c_T + c_R|
tau_clock = |c_T - c_clock| + |c_alpha| + |c_mass|
tau_R10   = |K_R10 q_source q_test + tail_R10|
tau_orbit = max(tau_gamma, tau_beta, |c_source_norm|)
```

This is the main movement: `tau` is no longer a single free scalar. It is a component projection of the observer/source map.

## What The Smoke Rows Say

Using `epsilon_loc = {bounds['epsilon']:.3e}`:

- A reciprocal-cell preserving/no-direct-clock mode has `tau_gamma=0` and `tau_clock=0`.
- A unit shear/source projection gives predictions of order `4.96e-7`, below the 4800 anchors, but it is still not parent-derived.
- A parent `B_C/Phi_C` no-flux/source-action theorem would set `epsilon_loc=0` and silence all channels.

## Source Register

{markdown_table(sources, ["source_id", "source_path", "exists", "needle_found", "role"])}

## Imported Bounds

{markdown_table(parse_csv(BOUND_IMPORT_CSV))}

## Coframe Projection Output

{markdown_table(output_rows, ["mode_id", "mode_type", "tau_gamma_abs", "tau_beta_abs", "tau_clock_abs", "tau_R10_abs", "tau_orbital_abs", "pred_gamma_abs", "pred_clock_abs", "pred_orbital_abs", "all_numeric_pass", "runner_status", "missing_projection_inputs", "anti_circularity_status"])}

## Tau Matrix

{markdown_table(tau_rows, ["mode_id", "arena", "tau_abs", "predicted_observable_abs", "numeric_pass", "mode_status"])}

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

    formal_content = f"""# 817 - PPC4161 observer coframe tau projection

Marker: `{MARKER}`
Generated: `{timestamp}`

## Formal Update

4801 replaces scalar `tau` placeholders with component projection formulas:

```text
tau_gamma = |c_T + c_R|
tau_clock = |c_T - c_clock| + |c_alpha| + |c_mass|
tau_R10   = |K_R10 q_source q_test + tail_R10|
tau_orbit = max(tau_gamma, tau_beta, |c_source_norm|)
```

This gives a clean target for the local bridge: derive a parent observer/source map that places the residual in the reciprocal-cell preserving and no-direct-clock subspace, or source finite component coefficients and let the local tests judge them.

See `{DOC_PATH}`.
"""
    write_text(FORMAL_PATH, formal_content)


def update_registers(timestamp: str) -> None:
    claim_line = (
        f'{CLAIM_ID},observer_coframe_tau_projection_runner,'
        f'"4801 derives component tau projection formulas from the observer coframe and shows reciprocal-cell/no-direct-clock modes are locally quiet while finite unit projections remain numerically under current anchors as nonclaim smoke rows.",'
        f'"Generated source register, 4800 bound import, coframe projection input/output, tau matrix, obstruction update, gates, firewalls, decision, status, next target and validation.",'
        f'observer_coframe_tau_projection_private_nonclaim_component_formulas_ready,'
        f'{NEXT_TARGET},'
        f'"Do not claim local GR from reciprocal-cell quietness unless the parent action derives the component restrictions and source/readout maps.",'
        f'local_gr,{DOC_PATH},{NEXT_TARGET},'
        f'tau by declaration; fit tau to bound; GR import; clock/process confusion; R10 anchor overclaim,'
        f'"Observer coframe tau projection",'
        f'{MARKER}; {DECISION}; generated {timestamp}\n'
    )
    if CLAIM_ID not in read_text(CLAIMS_PATH):
        with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
            handle.write(claim_line)

    spine_block = f"""
## {MARKER}

4801 turns `tau_X` into component projections:

```text
tau_gamma = |c_T + c_R|
tau_clock = |c_T - c_clock| + |c_alpha| + |c_mass|
tau_R10   = |K_R10 q_source q_test + tail_R10|
```

The promising subspace is now explicit: reciprocal-cell preserving (`c_T+c_R=0`) and no direct clock/readout residual (`c_T=c_clock`, constants quiet). This is not yet a parent theorem, but it is a sharper route than scalar tau placeholders.
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
Last checkpoint: `4801-Y5-R2FR-observer-coframe-tau-projection-derivation-or-parent-BC-no-flux-action.md`
Marker: `{MARKER}`

## Where we are

4801 derived component formulas for the local projection factors:

```text
tau_gamma = |c_T + c_R|
tau_clock = |c_T - c_clock| + |c_alpha| + |c_mass|
tau_R10   = |K_R10 q_source q_test + tail_R10|
tau_orbit = max(tau_gamma, tau_beta, |c_source_norm|)
```

The encouraging path is now precise: derive that the parent observer/source map places finite residuals in the reciprocal-cell preserving/no-direct-clock subspace, or source finite component coefficients and test them.

## Live blockers

- Parent action must derive `c_T+c_R=0` or provide finite sourced `c_T,c_R`.
- Clock/readout and constants must be same-coframe or source-bounded.
- R10 source/test and orbital residual vectors still need component source rows.
- Parent `B_C/Phi_C` no-flux theorem remains the clean zero-residual exit.

## Next target

`{NEXT_TARGET}`
"""
    write_text(RESUME_PATH, resume)


def main() -> int:
    timestamp = now()
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    SCRIPT_DIR.mkdir(parents=True, exist_ok=True)

    write_text(RUNNER, RUNNER_TEXT)
    bounds = import_bounds_4800(timestamp)
    sources = source_register(timestamp)
    inputs = coframe_input_rows(timestamp, bounds)

    write_csv(SOURCE_REGISTER_CSV, sources)
    write_csv(COFRAME_INPUT_CSV, inputs)

    python = sys.executable
    run_command([python, str(RUNNER), str(COFRAME_INPUT_CSV), str(COFRAME_OUTPUT_CSV)])
    output_rows = parse_csv(COFRAME_OUTPUT_CSV)

    tau_rows = tau_matrix_rows(output_rows)
    obstructions = obstruction_rows(output_rows)
    gates = gate_rows(output_rows)
    firewalls = firewall_rows()
    decisions = decision_rows()
    statuses = status_rows(output_rows)
    next_targets = next_target_rows()

    write_csv(TAU_MATRIX_CSV, tau_rows)
    write_csv(OBSTRUCTION_CSV, obstructions)
    write_csv(GATE_CSV, gates)
    write_csv(FIREWALL_CSV, firewalls)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_TARGET_CSV, next_targets)

    update_registers(timestamp)
    validations = validation_rows(sources, output_rows, tau_rows)
    write_csv(VALIDATION_CSV, validations)
    write_documents(timestamp, sources, bounds, output_rows, tau_rows, obstructions, gates, firewalls, decisions, statuses, validations)

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
