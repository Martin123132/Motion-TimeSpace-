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

CHECKPOINT = "4810"
CLAIM_ID = "L-652"
MARKER = "PPC4161_SECTOR_LAGRANGIAN_BOUNDARY_OWNER_OR_FB5540_SOURCE_ROW_4810"
PACKET_MARKER = "PPC4161_PACKET_SECTOR_LAGRANGIAN_BOUNDARY_OWNER_OR_FB5540_SOURCE_ROW_4810"
DECISION = "SECTOR_LAGRANGIAN_BOUNDARY_OWNER_AND_FB5540_SOURCE_ROW_GATE_NONCLAIM"
NEXT_TARGET = "4811-Y5-R2FR-boundary-exactness-projector-orthogonality-or-source-pack.md"

DOC_PATH = POST / "4810-Y5-R2FR-sector-Lagrangian-boundary-owner-or-FB5540-source-row.md"
FORMAL_PATH = FORMAL / "826-PPC4161-sector-Lagrangian-boundary-owner-or-FB5540-source-row.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"
RUNNER = SCRIPT_DIR / "sector_Lagrangian_boundary_owner_runner.py"

SOURCE_REGISTER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4810_SOURCE_REGISTER.csv"
OWNER_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4810_OWNER_CLAUSES_INPUT.csv"
OWNER_OUTPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4810_OWNER_CLAUSES_OUTPUT.csv"
ROUTE_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4810_ROUTE_TESTS_INPUT.csv"
ROUTE_OUTPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4810_ROUTE_TESTS_OUTPUT.csv"
SOURCE_ROW_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4810_FB5540_SOURCE_ROW_INPUT.csv"
SOURCE_ROW_OUTPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4810_FB5540_SOURCE_ROW_OUTPUT.csv"
TARGET_AUDIT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4810_TARGET_AUDIT.csv"
OBSTRUCTION_UPDATE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4810_OBSTRUCTION_UPDATE.csv"
GATE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4810_PROMOTION_GATES.csv"
FIREWALL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4810_FIREWALL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4810_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4810_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4810_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4810_VALIDATION.csv"

TARGET_4809 = SOURCE_DIR / "P8_Y5_R2FR_4809_TARGET_AUDIT.csv"
SECTOR_668 = SOURCE_DIR / "P8_Y5_R10_668_SECTOR_OWNER_AUDIT.csv"
BOUNDARY_668 = SOURCE_DIR / "P8_Y5_R10_668_BOUNDARY_CONDITION_LOCK.csv"
IMPACT_668 = SOURCE_DIR / "P8_Y5_R10_668_FB5540_IMPACT_MAP.csv"
CANDIDATES_669 = SOURCE_DIR / "P8_Y5_R10_669_MINIMAL_LX_OPERATOR_CANDIDATES.csv"
GATES_669 = SOURCE_DIR / "P8_Y5_R10_669_LX_OWNER_GATE_TESTS.csv"
VARIATION_669 = SOURCE_DIR / "P8_Y5_R10_669_THETA_QX_VARIATION_LEDGER.csv"
NO_POLE_670 = SOURCE_DIR / "P8_Y5_R10_670_NO_POLE_QUOTIENT_PROOF_CHAIN.csv"
SOURCEFREE_670 = SOURCE_DIR / "P8_Y5_R10_670_POSITIVE_SOURCEFREE_PROOF_CHAIN.csv"
BOUNDARY_671 = SOURCE_DIR / "P8_Y5_R10_671_BOUNDARY_CHARGE_OWNER_GATE.csv"

OWNER_CLAUSES = (
    "LX_parent_owned_signed",
    "Theta_QX_variation_signed",
    "omega_integrability_signed",
    "quotient_or_constraint_route_signed",
    "B_ref_fixed_signed",
    "B_class_boundary_silence_signed",
    "tau_functor_signed",
    "M_H_ref_owner_signed",
    "no_GR_import_signed",
    "no_fit_to_bound_signed",
)

SOURCE_COMPONENTS = (
    "delta_H_tau_nonintegrable_abs",
    "Delta_ref_abs",
    "symplectic_boundary_flux_abs",
    "B_zero_flux_abs",
    "Delta_tau_abs",
    "bulk_X_abs",
    "edge_X_abs",
    "R11_abs",
)

SOURCE_SPECS = [
    ("SRC4810_00_4809_doc", POST / "4809-Y5-R2FR-Hamiltonian-PiM-reference-lock-or-MHref-first-row.md", "sector_Lagrangian_boundary_owner_or_FB5540_source_row_is_next", "4809 selects sector Lagrangian/boundary owner"),
    ("SRC4810_01_4809_target", TARGET_4809, "TGA4809_0_target_import", "4809 inherited target audit"),
    ("SRC4810_02_1018_doc", POST / "1018-Y5-R10-sector-Lagrangian-boundary-owner-or-FB5540-source-row.md", "LOC1018_0_LX_owner", "1018 owner map precedent"),
    ("SRC4810_03_668_sector", SECTOR_668, "SO668_2_MTS_extra_LX", "668 sector owner audit"),
    ("SRC4810_04_668_boundary", BOUNDARY_668, "boundary", "668 boundary condition lock"),
    ("SRC4810_05_668_impact", IMPACT_668, "IM668_0_delta_H_tau", "668 FB5540 impact map"),
    ("SRC4810_06_669_candidates", CANDIDATES_669, "L_X", "669 minimal L_X candidates"),
    ("SRC4810_07_669_gates", GATES_669, "L_X", "669 L_X owner gate tests"),
    ("SRC4810_08_669_variation", VARIATION_669, "delta L_X = E_X delta X + d Theta_X", "669 Theta/QX variation ledger"),
    ("SRC4810_09_670_no_pole", NO_POLE_670, "Dq[v_X]=0", "670 no-pole quotient proof chain"),
    ("SRC4810_10_670_sourcefree", SOURCEFREE_670, "Z_X>0", "670 positive source-free proof chain"),
    ("SRC4810_11_671_boundary", BOUNDARY_671, "BCG671_4_projector_orthogonality", "671 boundary charge owner gate"),
    ("SRC4810_12_runner", RUNNER, "def owner_clause_row", "4810 executable owner/source-row runner"),
]


RUNNER_TEXT = r'''from __future__ import annotations

import csv
import math
import sys
from pathlib import Path
from typing import Any


OWNER_CLAUSES = (
    "LX_parent_owned_signed",
    "Theta_QX_variation_signed",
    "omega_integrability_signed",
    "quotient_or_constraint_route_signed",
    "B_ref_fixed_signed",
    "B_class_boundary_silence_signed",
    "tau_functor_signed",
    "M_H_ref_owner_signed",
    "no_GR_import_signed",
    "no_fit_to_bound_signed",
)

SOURCE_COMPONENTS = (
    "delta_H_tau_nonintegrable_abs",
    "Delta_ref_abs",
    "symplectic_boundary_flux_abs",
    "B_zero_flux_abs",
    "Delta_tau_abs",
    "bulk_X_abs",
    "edge_X_abs",
    "R11_abs",
)

FORBIDDEN_SOURCE_TOKENS = (
    "GR_IMPORT",
    "FIT_TO_BOUND",
    "BOUND_AS_SOURCE",
    "ORBITAL_GM_AS_SOURCE",
    "POST_READOUT_MASK",
    "REFERENCE_ONLY_ZERO",
    "BARE_MASS_SHORTCUT",
    "NEWTON_G_AS_INPUT",
    "CANCEL_UNKNOWN_COMPONENTS",
    "SYMBOLIC_LX_ONLY",
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
        for field in ("owner_id", "route_id", "row_id", "source_path", "equation_ref", "notes", "provenance")
    ).upper()
    return any(token in source_text for token in FORBIDDEN_SOURCE_TOKENS)


def missing_owner_clauses(row: dict[str, Any]) -> list[str]:
    return [clause for clause in OWNER_CLAUSES if not bool_text(row.get(clause))]


def component_guard(row: dict[str, Any]) -> tuple[float | None, list[str]]:
    values: list[float] = []
    missing: list[str] = []
    for component in SOURCE_COMPONENTS:
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


def owner_clause_row(row: dict[str, Any]) -> dict[str, Any]:
    owner_id = str(row.get("owner_id", "")).strip() or "UNNAMED_OWNER_ROW"
    output: dict[str, Any] = {
        "owner_id": owner_id,
        "owner_target": row.get("owner_target", ""),
        "input_valid_for_claim": bool_text(row.get("valid_for_claim")),
        "valid_for_claim": False,
        "claim_allowed": False,
    }
    if forbidden_source_used(row):
        output.update(
            {
                "owner_gate_status": "FAILED_OWNER_GATE",
                "owner_theorem": False,
                "missing_owner_inputs": "FORBIDDEN_OWNER_SOURCE",
                "anti_circularity_status": "FAIL_FORBIDDEN_SOURCE_USED",
            }
        )
        return output
    missing = missing_owner_clauses(row)
    if missing:
        status = "BLOCKED_MISSING_OWNER_SIGNATURES"
        theorem = False
    else:
        status = "OWNER_ROUTE_SIGNED_CONDITIONAL_NONCLAIM"
        theorem = True
    output.update(
        {
            "owner_gate_status": status,
            "owner_theorem": theorem,
            "missing_owner_inputs": ";".join(missing),
            "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
        }
    )
    return output


def route_test_row(row: dict[str, Any]) -> dict[str, Any]:
    route_id = str(row.get("route_id", "")).strip() or "UNNAMED_ROUTE"
    output: dict[str, Any] = {
        "route_id": route_id,
        "route": row.get("route", ""),
        "input_valid_for_claim": bool_text(row.get("valid_for_claim")),
        "valid_for_claim": False,
        "claim_allowed": False,
    }
    if forbidden_source_used(row):
        output.update(
            {
                "route_status": "FAILED_ROUTE_GATE",
                "route_theorem": False,
                "missing_route_inputs": "FORBIDDEN_ROUTE_SOURCE",
                "anti_circularity_status": "FAIL_FORBIDDEN_SOURCE_USED",
            }
        )
        return output
    required = [field.strip() for field in str(row.get("required_signatures", "")).split(";") if field.strip()]
    missing = [field for field in required if not bool_text(row.get(field))]
    if missing:
        status = "ROUTE_BLOCKED_MISSING_SIGNATURES"
        theorem = False
    else:
        status = "ROUTE_SIGNED_CONDITIONAL_NONCLAIM"
        theorem = True
    output.update(
        {
            "route_status": status,
            "route_theorem": theorem,
            "missing_route_inputs": ";".join(missing),
            "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
        }
    )
    return output


def source_row(row: dict[str, Any]) -> dict[str, Any]:
    row_id = str(row.get("row_id", "")).strip() or "UNNAMED_FB5540_ROW"
    output: dict[str, Any] = {
        "row_id": row_id,
        "component_expr": row.get("component_expr", ""),
        "input_valid_for_claim": bool_text(row.get("valid_for_claim")),
        "valid_for_claim": False,
        "claim_allowed": False,
    }
    if forbidden_source_used(row):
        output.update(
            {
                "FB5540_guard_abs": "MISSING_NUMERIC_VALUE",
                "required_abs_max": format_float(parse_float(row.get("required_abs_max"))),
                "numeric_window_pass": False,
                "source_row_status": "FAILED_FB5540_SOURCE_ROW_GATE",
                "missing_source_inputs": "FORBIDDEN_SOURCE_ROW",
                "anti_circularity_status": "FAIL_FORBIDDEN_SOURCE_USED",
            }
        )
        return output
    required = parse_float(row.get("required_abs_max"))
    direct_value = parse_float(row.get("FB5540_guard_abs"))
    computed_value, computed_missing = component_guard(row)
    value = direct_value if direct_value is not None else computed_value
    missing: list[str] = []
    if required is None or required <= 0.0:
        missing.append("MISSING_required_abs_max")
    if value is None:
        missing.extend(computed_missing or ["MISSING_FB5540_guard_abs"])
    if missing_text(row.get("source_path")):
        missing.append("MISSING_source_path")
    if missing_text(row.get("equation_ref")):
        missing.append("MISSING_equation_ref")
    if not bool_text(row.get("source_signed")):
        missing.append("MISSING_source_signed")
    if required is None or required <= 0.0 or value is None:
        output.update(
            {
                "FB5540_guard_abs": "MISSING_NUMERIC_VALUE",
                "required_abs_max": format_float(required),
                "numeric_window_pass": False,
                "source_row_status": "BLOCKED_MISSING_FB5540_SOURCE_INPUTS",
                "missing_source_inputs": ";".join(missing),
                "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
            }
        )
        return output
    passes = value <= required
    status = "FB5540_SOURCE_ROW_NUMERIC_WINDOW_FAIL"
    if passes:
        status = (
            "FB5540_SOURCE_ROW_NUMERIC_WINDOW_PASS_SOURCE_SIGNED_NONCLAIM"
            if bool_text(row.get("source_signed")) and bool_text(row.get("valid_for_claim"))
            else "FB5540_SOURCE_ROW_NUMERIC_WINDOW_PASS_SOURCE_UNSIGNED_NONCLAIM"
        )
    output.update(
        {
            "FB5540_guard_abs": format_float(value),
            "required_abs_max": format_float(required),
            "numeric_window_pass": passes,
            "source_row_status": status,
            "missing_source_inputs": ";".join(missing),
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
    if len(sys.argv) != 4 or sys.argv[1] not in {"owner", "route", "source"}:
        print("Usage: sector_Lagrangian_boundary_owner_runner.py owner|route|source INPUT_CSV OUTPUT_CSV", file=sys.stderr)
        return 2
    mode = sys.argv[1]
    rows = read_csv(Path(sys.argv[2]))
    if mode == "owner":
        outputs = [owner_clause_row(row) for row in rows]
    elif mode == "route":
        outputs = [route_test_row(row) for row in rows]
    else:
        outputs = [source_row(row) for row in rows]
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
    rows = read_csv(TARGET_4809)
    if not rows:
        raise RuntimeError("missing 4809 target rows")
    return {
        "component_expr": "abs(FB5540_guard)",
        "required_abs_max": rows[0]["required_abs_max"],
        "source": str(TARGET_4809),
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
    return {component: "0.0" for component in SOURCE_COMPONENTS}


def missing_components() -> dict[str, str]:
    return {component: "MISSING_PARENT_VALUE" for component in SOURCE_COMPONENTS}


def unit_components() -> dict[str, str]:
    values = zero_components()
    values["bulk_X_abs"] = "1.0"
    return values


def strict_components() -> dict[str, str]:
    values = zero_components()
    values["bulk_X_abs"] = "10.0"
    return values


def with_owner_clauses(values: dict[str, Any], signed: bool) -> dict[str, Any]:
    return {**values, **{clause: signed for clause in OWNER_CLAUSES}}


def write_runner() -> None:
    SCRIPT_DIR.mkdir(parents=True, exist_ok=True)
    RUNNER.write_text(RUNNER_TEXT, encoding="utf-8")


def write_inputs(timestamp: str, target: dict[str, str]) -> None:
    required = target["required_abs_max"]
    target_rows = [
        {
            "audit_id": "TGA4810_0_target_import",
            "component_expr": "abs(FB5540_guard)",
            "required_abs_max": required,
            "source": target["source"],
            "derivation": "same normalized local coupling window inherited from 4809 Hamiltonian/PiM reference-lock target",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]
    owner_rows = [
        {
            "owner_id": "physical_sector_owner_missing",
            "owner_target": "L_X;Theta_X;Q_tau^X;omega_X;B_ref;B_class;tau;M_H_ref",
            **with_owner_clauses({}, False),
            "no_GR_import_signed": True,
            "no_fit_to_bound_signed": True,
            "source_path": "MISSING_PARENT_SECTOR_LAGRANGIAN_BOUNDARY_OWNER",
            "equation_ref": "MISSING_PARENT_OWNER_EQUATION",
            "notes": "physical branch blocks until L_X variation, charge, boundary reference/class, tau and M_H_ref are all parent-owned together",
            "provenance": "4810 physical branch",
            "valid_for_claim": False,
        },
        {
            "owner_id": "symbolic_LX_owner_unsigned",
            "owner_target": "symbolic_LX_variation",
            **with_owner_clauses({}, False),
            "no_GR_import_signed": True,
            "no_fit_to_bound_signed": True,
            "source_path": str(VARIATION_669),
            "equation_ref": "V669_0_to_V669_4",
            "notes": "variation formula exists but parent owner signatures are not closed for current MTS",
            "provenance": "669 variation ledger",
            "valid_for_claim": False,
        },
        {
            "owner_id": "conditional_owner_stack",
            "owner_target": "full_owner_stack_conditional",
            **with_owner_clauses({}, True),
            "source_path": str(POST / "1018-Y5-R10-sector-Lagrangian-boundary-owner-or-FB5540-source-row.md"),
            "equation_ref": "LOC1018_0_to_LOC1018_8",
            "notes": "conditional owner theorem shape only; physical branch has not signed the clauses",
            "provenance": "1018 owner clauses",
            "valid_for_claim": False,
        },
        {
            "owner_id": "forbidden_symbolic_or_fit_control",
            "owner_target": "forbidden_control",
            **with_owner_clauses({}, True),
            "source_path": "SYMBOLIC_LX_ONLY_CANCEL_UNKNOWN_COMPONENTS_ORBITAL_GM_AS_SOURCE",
            "equation_ref": "FORBIDDEN_FIT_TO_BOUND",
            "notes": "control row must fail if symbolic L_X or unknown cancellation is treated as ownership",
            "provenance": "forbidden control",
            "valid_for_claim": False,
        },
    ]
    route_rows = [
        {
            "route_id": "route_no_pole_quotient_unsigned",
            "route": "no independent X after quotient",
            "mathematical_form": "S_parent=S_red[q(Phi)] and Dq[v_X]=0 before variation",
            "required_signatures": "q_map_signed;Dq_kernel_signed;action_descent_signed;matter_descent_signed;boundary_charge_zero_signed;degree_count_signed",
            "q_map_signed": False,
            "Dq_kernel_signed": False,
            "action_descent_signed": False,
            "matter_descent_signed": False,
            "boundary_charge_zero_signed": False,
            "degree_count_signed": False,
            "source_path": str(NO_POLE_670),
            "equation_ref": "NQ670_0_to_NQ670_8",
            "notes": "best GR-reduction route, but current parent quotient/boundary clauses are unsigned",
            "provenance": "670 no-pole proof chain",
            "valid_for_claim": False,
        },
        {
            "route_id": "route_vertical_constraint_unsigned",
            "route": "X is vertical first-class constraint direction",
            "mathematical_form": "delta G_X=Omega(delta Phi,v_X); Q_X differentiable; K_boundary=0",
            "required_signatures": "momentum_map_signed;QX_differentiable_signed;K_boundary_zero_signed;first_class_signed;PiM_edge_orthogonal_signed",
            "momentum_map_signed": False,
            "QX_differentiable_signed": False,
            "K_boundary_zero_signed": False,
            "first_class_signed": False,
            "PiM_edge_orthogonal_signed": False,
            "source_path": str(BOUNDARY_671),
            "equation_ref": "BCG671_0_to_BCG671_7",
            "notes": "active theorem route, blocked by boundary differentiability and PiM/edge orthogonality",
            "provenance": "671 boundary charge owner gate",
            "valid_for_claim": False,
        },
        {
            "route_id": "route_positive_sourcefree_unsigned",
            "route": "positive source-free local operator kills X",
            "mathematical_form": "int_A (Z_X|grad X|^2+M_X^2 X^2)=int_A XJ_X+boundary_flux_X",
            "required_signatures": "Z_positive_signed;M2_positive_signed;JX_zero_signed;boundary_flux_zero_signed;compact_domain_signed",
            "Z_positive_signed": False,
            "M2_positive_signed": False,
            "JX_zero_signed": False,
            "boundary_flux_zero_signed": False,
            "compact_domain_signed": False,
            "source_path": str(SOURCEFREE_670),
            "equation_ref": "PSF670_0_to_PSF670_7",
            "notes": "positive theorem route, blocked by missing parent Z_X, M_X^2, J_X=0 and boundary-flux zero",
            "provenance": "670 source-free proof chain",
            "valid_for_claim": False,
        },
        {
            "route_id": "route_conditional_all_signed",
            "route": "conditional owner theorem",
            "mathematical_form": "all no-pole/vertical/sourcefree clauses supplied by parent action",
            "required_signatures": "q_map_signed;Dq_kernel_signed;action_descent_signed;matter_descent_signed;boundary_charge_zero_signed;degree_count_signed",
            "q_map_signed": True,
            "Dq_kernel_signed": True,
            "action_descent_signed": True,
            "matter_descent_signed": True,
            "boundary_charge_zero_signed": True,
            "degree_count_signed": True,
            "source_path": str(POST / "1018-Y5-R10-sector-Lagrangian-boundary-owner-or-FB5540-source-row.md"),
            "equation_ref": "RT1018_0 conditional route",
            "notes": "conditional branch only; not the current physical MTS proof",
            "provenance": "1018 route tests",
            "valid_for_claim": False,
        },
        {
            "route_id": "route_forbidden_fit_control",
            "route": "forbidden sourced fit",
            "mathematical_form": "unknown components cancel against fitted bound",
            "required_signatures": "q_map_signed",
            "q_map_signed": True,
            "source_path": "CANCEL_UNKNOWN_COMPONENTS_BOUND_AS_SOURCE",
            "equation_ref": "FORBIDDEN_SOURCE_FIT",
            "notes": "control row must fail if coefficient cancellation or bound-fitting is treated as a route",
            "provenance": "forbidden control",
            "valid_for_claim": False,
        },
    ]
    source_rows = [
        {
            "row_id": "physical_FB5540_source_row_missing",
            "component_expr": "abs(FB5540_guard)",
            "FB5540_guard_abs": "MISSING_PARENT_VALUE",
            **missing_components(),
            "M_H_ref_abs": "MISSING_PARENT_VALUE",
            "required_abs_max": required,
            "source_signed": False,
            "source_path": "MISSING_PARENT_FB5540_SOURCE_ROW",
            "equation_ref": "MISSING_PARENT_FB5540_SOURCE_EQUATION",
            "notes": "physical row blocks until M_H_ref plus all FB5540/bulk/edge/R11 components have units and source paths",
            "provenance": "4810 physical branch",
            "valid_for_claim": False,
        },
        {
            "row_id": "owner_zero_candidate_unsigned",
            "component_expr": "abs(FB5540_guard)",
            "FB5540_guard_abs": "",
            **zero_components(),
            "M_H_ref_abs": "1.0",
            "required_abs_max": required,
            "source_signed": False,
            "source_path": str(POST / "1018-Y5-R10-sector-Lagrangian-boundary-owner-or-FB5540-source-row.md"),
            "equation_ref": "RT1018_5_verdict conditional zero route",
            "notes": "zero candidate is algebraic but owner source is unsigned",
            "provenance": "1018 owner map",
            "valid_for_claim": False,
        },
        {
            "row_id": "unit_bulk_X_prior_smoke",
            "component_expr": "abs(FB5540_guard)",
            "FB5540_guard_abs": "",
            **unit_components(),
            "M_H_ref_abs": "1.0",
            "required_abs_max": required,
            "source_signed": False,
            "source_path": str(IMPACT_668),
            "equation_ref": "unit bulk_X smoke",
            "notes": "unit bulk residual is below current target but remains nonclaim",
            "provenance": "668 impact map",
            "valid_for_claim": False,
        },
        {
            "row_id": "strict_FB5540_fail_control",
            "component_expr": "abs(FB5540_guard)",
            "FB5540_guard_abs": "",
            **strict_components(),
            "M_H_ref_abs": "1.0",
            "required_abs_max": required,
            "source_signed": False,
            "source_path": str(IMPACT_668),
            "equation_ref": "strict fail control",
            "notes": "control row proves the gate rejects oversized source rows",
            "provenance": "4810 control",
            "valid_for_claim": False,
        },
        {
            "row_id": "conditional_owner_theorem_zero",
            "component_expr": "abs(FB5540_guard)",
            "FB5540_guard_abs": "",
            **zero_components(),
            "M_H_ref_abs": "1.0",
            "required_abs_max": required,
            "source_signed": True,
            "source_path": str(POST / "1018-Y5-R10-sector-Lagrangian-boundary-owner-or-FB5540-source-row.md"),
            "equation_ref": "conditional sector owner theorem template",
            "notes": "conditional branch only; not a physical parent source row",
            "provenance": "4810 conditional branch",
            "valid_for_claim": False,
        },
        {
            "row_id": "forbidden_cancellation_source_control",
            "component_expr": "abs(FB5540_guard)",
            "FB5540_guard_abs": "0.0",
            **zero_components(),
            "M_H_ref_abs": "1.0",
            "required_abs_max": required,
            "source_signed": True,
            "source_path": "CANCEL_UNKNOWN_COMPONENTS_ORBITAL_GM_AS_SOURCE_SYMBOLIC_LX_ONLY",
            "equation_ref": "FORBIDDEN_REFERENCE_ONLY_ZERO",
            "notes": "control row must fail if unknown cancellations or orbital GM denominators are treated as proof",
            "provenance": "forbidden control",
            "valid_for_claim": False,
        },
    ]
    write_csv(TARGET_AUDIT_CSV, target_rows)
    write_csv(OWNER_INPUT_CSV, owner_rows)
    write_csv(ROUTE_INPUT_CSV, route_rows)
    write_csv(SOURCE_ROW_INPUT_CSV, source_rows)


def run_runner() -> None:
    subprocess.run([sys.executable, str(RUNNER), "owner", str(OWNER_INPUT_CSV), str(OWNER_OUTPUT_CSV)], check=True)
    subprocess.run([sys.executable, str(RUNNER), "route", str(ROUTE_INPUT_CSV), str(ROUTE_OUTPUT_CSV)], check=True)
    subprocess.run([sys.executable, str(RUNNER), "source", str(SOURCE_ROW_INPUT_CSV), str(SOURCE_ROW_OUTPUT_CSV)], check=True)


def make_output_tables() -> dict[str, list[dict[str, Any]]]:
    owners = read_csv(OWNER_OUTPUT_CSV)
    routes = read_csv(ROUTE_OUTPUT_CSV)
    source_rows = read_csv(SOURCE_ROW_OUTPUT_CSV)
    obstruction_update = [
        {
            "update_id": "OBS4810_0_owner_map",
            "item": "sector Lagrangian/boundary owner stack",
            "status": "BLOCKED_MISSING_OWNER_SIGNATURES",
            "value_or_bound": "L_X;Theta_X;Q_tau^X;omega_X;B_ref;B_class;tau;M_H_ref",
            "meaning": "the owner map is explicit, but current MTS has not signed the full stack",
        },
        {
            "update_id": "OBS4810_1_best_route",
            "item": "no-pole quotient route",
            "status": "ROUTE_BLOCKED_MISSING_SIGNATURES",
            "value_or_bound": "Dq[v_X]=0 plus action/matter descent plus boundary charge zero",
            "meaning": "this remains the cleanest GR-reduction route because it removes the physical X pole structurally",
        },
        {
            "update_id": "OBS4810_2_source_fallback",
            "item": "FB5540 no-cancellation source row",
            "status": "FB5540_SOURCE_ROW_NUMERIC_WINDOW_PASS_SOURCE_UNSIGNED_NONCLAIM",
            "value_or_bound": "1.000000000000000e+00 <= 5.256633029822351e+00",
            "meaning": "a unit bulk-X smoke row fits the current window, but all physical source-row coefficients remain missing",
        },
    ]
    gates = [
        {
            "gate_id": "PG4810_0_owner_map_written",
            "claim": "Sector owner map covers L_X, Theta/Q, quotient/constraint, boundary, tau and M_H_ref",
            "gate_pass": True,
            "reason": "owner clauses and route tests are executable rows",
            "evidence": str(OWNER_OUTPUT_CSV),
        },
        {
            "gate_id": "PG4810_1_no_pole_route",
            "claim": "No-pole quotient route closes current MTS",
            "gate_pass": False,
            "reason": "q map, Dq kernel, action descent, matter descent and boundary charge zero remain unsigned",
            "evidence": str(ROUTE_OUTPUT_CSV),
        },
        {
            "gate_id": "PG4810_2_positive_sourcefree_route",
            "claim": "Positive source-free X theorem closes current MTS",
            "gate_pass": False,
            "reason": "Z_X, M_X^2, J_X=0, boundary flux zero and compact domain are missing",
            "evidence": str(ROUTE_OUTPUT_CSV),
        },
        {
            "gate_id": "PG4810_3_FB5540_source_row",
            "claim": "FB5540 source row is claim-ready",
            "gate_pass": False,
            "reason": "physical row lacks M_H_ref plus numerator, bulk, edge and R11 source-backed components",
            "evidence": str(SOURCE_ROW_OUTPUT_CSV),
        },
        {
            "gate_id": "PG4810_4_Newton_local_GR",
            "claim": "Newton/local-GR source coupling promotion is allowed",
            "gate_pass": False,
            "reason": "owner theorem and source-row fallback are both nonclaim",
            "evidence": "nonclaim firewall active",
        },
    ]
    firewalls = [
        {"firewall_id": "FW4810_0_no_symbolic_LX", "rule": "A symbolic L_X is not owner evidence unless its variation, charge, symplectic form and boundary class are parent-signed.", "status": "ACTIVE"},
        {"firewall_id": "FW4810_1_no_unknown_cancellation", "rule": "FB5540, bulk X, edge X and R11 components cannot cancel as unknowns.", "status": "ACTIVE"},
        {"firewall_id": "FW4810_2_no_orbital_GM_denominator", "rule": "Orbital GM cannot supply M_H_ref for the row meant to derive source coupling.", "status": "ACTIVE"},
        {"firewall_id": "FW4810_3_no_boundary_closure_credit", "rule": "Boundary exactness/projector orthogonality must be proved or sourced, not assumed.", "status": "ACTIVE"},
    ]
    decisions = [
        {
            "decision_id": "DEC4810_0_owner_result",
            "decision": "sector_owner_map_explicit_but_not_closed",
            "reason": "L_X/Theta/Q, B_ref, B_class, tau and M_H_ref are all named but not parent-signed together",
            "next_action": "do not promote FB5540, R10, R11 or local GR from symbolic sector machinery",
        },
        {
            "decision_id": "DEC4810_1_best_route",
            "decision": "no_pole_quotient_route_remains_best_derivation_route",
            "reason": "it structurally removes the physical X pole instead of tuning a small coefficient",
            "next_action": "attack boundary exactness/projector orthogonality and quotient descent",
        },
        {
            "decision_id": "DEC4810_2_source_fallback",
            "decision": "complete_source_pack_required_if_zero_route_fails",
            "reason": "FB5540, bulk X, edge X and R11 need a no-cancellation source row with one M_H_ref denominator",
            "next_action": "source all coefficients together or keep row blocked",
        },
        {
            "decision_id": "DEC4810_3_next",
            "decision": "boundary_exactness_projector_orthogonality_or_source_pack_is_next",
            "reason": "boundary/edge charge is the live obstruction after owner map and no-pole routes remain unsigned",
            "next_action": NEXT_TARGET,
        },
    ]
    status = [
        {"status_id": "STATUS4810_0_owner", "status": "BLOCKED_MISSING_OWNER_SIGNATURES", "detail": "physical owner stack is explicit but unsigned"},
        {"status_id": "STATUS4810_1_route", "status": "NO_POLE_QUOTIENT_ROUTE_BEST_BUT_UNSIGNED", "detail": "Dq/action/matter/boundary clauses remain missing"},
        {"status_id": "STATUS4810_2_source", "status": "FB5540_SOURCE_ROW_WINDOW_SMOKE_PASS_NONCLAIM", "detail": "1.0 <= 5.256633029822351, physical source pack missing"},
        {"status_id": "STATUS4810_3_selected_next", "status": "BOUNDARY_EXACTNESS_PROJECTOR_ORTHOGONALITY_OR_SOURCE_PACK", "detail": NEXT_TARGET},
    ]
    next_rows = [
        {
            "route_id": "NEXT4810_0_primary",
            "next_target": NEXT_TARGET,
            "script": "scripts/Y5_R2FR_4811_boundary_exactness_projector_orthogonality_or_source_pack.py",
            "objective": "derive boundary exactness/projector orthogonality/no edge double-count or build a complete FB5540 bulk/edge/R11 source pack",
            "selection_status": "selected",
            "success_condition": "boundary charge is killed by theorem-zero clauses or all residual source coefficients are source-backed together",
        }
    ]
    write_csv(OBSTRUCTION_UPDATE_CSV, obstruction_update)
    write_csv(GATE_CSV, gates)
    write_csv(FIREWALL_CSV, firewalls)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, status)
    write_csv(NEXT_TARGET_CSV, next_rows)
    return {
        "owners": owners,
        "routes": routes,
        "source_rows": source_rows,
        "obstruction_update": obstruction_update,
        "gates": gates,
        "firewalls": firewalls,
        "decisions": decisions,
        "status": status,
        "next": next_rows,
    }


def validate() -> list[dict[str, Any]]:
    sources = read_csv(SOURCE_REGISTER_CSV)
    owners = {row["owner_id"]: row for row in read_csv(OWNER_OUTPUT_CSV)}
    routes = {row["route_id"]: row for row in read_csv(ROUTE_OUTPUT_CSV)}
    source_rows = {row["row_id"]: row for row in read_csv(SOURCE_ROW_OUTPUT_CSV)}
    source_pass = all(row["exists"] == "True" and row["needle_found"] == "True" for row in sources)
    checks = [
        {"check_id": "VAL4810_0_sources", "description": "all cited sources exist and needles are found", "result": "PASS" if source_pass else "FAIL", "evidence": str(SOURCE_REGISTER_CSV)},
        {"check_id": "VAL4810_1_physical_owner_blocks", "description": "physical owner row remains blocked", "result": "PASS" if owners["physical_sector_owner_missing"]["owner_gate_status"] == "BLOCKED_MISSING_OWNER_SIGNATURES" else "FAIL", "evidence": str(OWNER_OUTPUT_CSV)},
        {"check_id": "VAL4810_2_conditional_owner", "description": "conditional owner row signs only as nonclaim theorem shape", "result": "PASS" if owners["conditional_owner_stack"]["owner_gate_status"] == "OWNER_ROUTE_SIGNED_CONDITIONAL_NONCLAIM" else "FAIL", "evidence": str(OWNER_OUTPUT_CSV)},
        {"check_id": "VAL4810_3_forbidden_owner_fails", "description": "forbidden symbolic/fit owner control fails", "result": "PASS" if owners["forbidden_symbolic_or_fit_control"]["anti_circularity_status"] == "FAIL_FORBIDDEN_SOURCE_USED" else "FAIL", "evidence": str(OWNER_OUTPUT_CSV)},
        {"check_id": "VAL4810_4_no_pole_blocks", "description": "no-pole quotient route remains blocked", "result": "PASS" if routes["route_no_pole_quotient_unsigned"]["route_status"] == "ROUTE_BLOCKED_MISSING_SIGNATURES" else "FAIL", "evidence": str(ROUTE_OUTPUT_CSV)},
        {"check_id": "VAL4810_5_forbidden_route_fails", "description": "forbidden route fit control fails", "result": "PASS" if routes["route_forbidden_fit_control"]["anti_circularity_status"] == "FAIL_FORBIDDEN_SOURCE_USED" else "FAIL", "evidence": str(ROUTE_OUTPUT_CSV)},
        {"check_id": "VAL4810_6_physical_source_blocks", "description": "physical FB5540 source row remains blocked", "result": "PASS" if source_rows["physical_FB5540_source_row_missing"]["source_row_status"] == "BLOCKED_MISSING_FB5540_SOURCE_INPUTS" else "FAIL", "evidence": str(SOURCE_ROW_OUTPUT_CSV)},
        {"check_id": "VAL4810_7_unit_source_passes", "description": "unit FB5540 smoke row passes target window", "result": "PASS" if source_rows["unit_bulk_X_prior_smoke"]["numeric_window_pass"] == "True" else "FAIL", "evidence": str(SOURCE_ROW_OUTPUT_CSV)},
        {"check_id": "VAL4810_8_strict_fail", "description": "strict FB5540 source row control fails numeric target", "result": "PASS" if source_rows["strict_FB5540_fail_control"]["numeric_window_pass"] == "False" and source_rows["strict_FB5540_fail_control"]["source_row_status"] == "FB5540_SOURCE_ROW_NUMERIC_WINDOW_FAIL" else "FAIL", "evidence": str(SOURCE_ROW_OUTPUT_CSV)},
        {"check_id": "VAL4810_9_forbidden_source_fails", "description": "forbidden cancellation source row control fails", "result": "PASS" if source_rows["forbidden_cancellation_source_control"]["anti_circularity_status"] == "FAIL_FORBIDDEN_SOURCE_USED" else "FAIL", "evidence": str(SOURCE_ROW_OUTPUT_CSV)},
        {"check_id": "VAL4810_10_claim", "description": "claim register includes L-652 as nonclaim", "result": "PASS" if CLAIM_ID in read_text(CLAIMS_PATH) and DECISION in read_text(CLAIMS_PATH) else "FAIL", "evidence": str(CLAIMS_PATH)},
        {"check_id": "VAL4810_11_resume", "description": "resume points at 4811", "result": "PASS" if NEXT_TARGET in read_text(RESUME_PATH) else "FAIL", "evidence": str(RESUME_PATH)},
    ]
    checks.append({"check_id": "VAL4810_OVERALL", "description": "all 4810 sector-owner checks pass", "result": "PASS" if all(row["result"] == "PASS" for row in checks) else "FAIL", "evidence": DECISION})
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
        "claim": "sector_Lagrangian_boundary_owner_runner",
        "current_evidence": "4810 installs the sector Lagrangian/boundary owner gate and FB5540 no-cancellation source-row fallback; unit bulk-X residual passes the current window but remains source-unsigned.",
        "status": "sector_Lagrangian_boundary_owner_private_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "symbolic L_X; unknown cancellation; boundary closure assumption; orbital GM denominator",
        "sector": "local_gr",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "symbolic L_X ownership; reference-only boundary zero; bulk-edge double count; fit to bound; GR/Newton import",
        "title": "Sector Lagrangian boundary owner and FB5540 source-row gate",
        "notes": f"{MARKER}; {DECISION}; generated {timestamp}",
    }
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row))
        writer.writerow(row)


def update_registers(timestamp: str) -> None:
    append_claim(timestamp)
    spine_text = f"""

## {MARKER}

4810 assigns the local coupling problem to a sector-owner stack:

```text
delta L_X = E_X delta X + d Theta_X
J_tau^X = Theta_X(L_tau X) - i_tau L_X = dQ_tau^X + C_tau^X
FB5540_guard = (|delta_H_tau_nonintegrable| + |Delta_ref| + |symplectic_boundary_flux|
                + |B_zero_flux| + |Delta_tau| + |bulk_X| + |edge_X| + |R11|) / |M_H_ref|
```

The best derivation route is still no-pole quotient descent: `Dq[v_X]=0` plus action/matter descent and boundary charge zero. Current MTS does not yet sign those clauses, so the fallback is a complete no-cancellation source pack rather than a symbolic `L_X` claim.
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
Last checkpoint: `4810-Y5-R2FR-sector-Lagrangian-boundary-owner-or-FB5540-source-row.md`
Marker: `{MARKER}`

## Where we are

4810 installed the sector Lagrangian/boundary owner gate:

```text
delta L_X = E_X delta X + d Theta_X
J_tau^X = Theta_X(L_tau X) - i_tau L_X = dQ_tau^X + C_tau^X
FB5540_guard = (|delta_H_tau_nonintegrable| + |Delta_ref| + |symplectic_boundary_flux|
                + |B_zero_flux| + |Delta_tau| + |bulk_X| + |edge_X| + |R11|) / |M_H_ref|
FB5540_guard <= 5.256633029822351
```

The owner map is now explicit. The physical branch still needs parent-signed `L_X`, `Theta_X`, `Q_tau^X`, `omega_X`, `B_ref`, `B_class`, `tau`, and `M_H_ref` together. The best derivation route remains the no-pole quotient path, but it needs boundary exactness/projector orthogonality.

## Live blockers

- Symbolic `L_X` is not enough; its variation, charge, symplectic form and boundary class need parent ownership.
- No-pole quotient descent needs `Dq[v_X]=0`, action/matter descent and boundary charge zero.
- The fallback source row needs one no-cancellation pack for FB5540, bulk X, edge X and R11 with a common `M_H_ref`.

## Next target

`{NEXT_TARGET}`
"""
    RESUME_PATH.write_text(resume, encoding="utf-8")


def write_docs(timestamp: str, target: dict[str, str], outputs: dict[str, list[dict[str, Any]]], validation: list[dict[str, Any]]) -> None:
    sources = read_csv(SOURCE_REGISTER_CSV)
    target_rows = read_csv(TARGET_AUDIT_CSV)
    doc = f"""# 4810 - Sector Lagrangian boundary owner or FB5540 source row

Marker: `{MARKER}`
Generated: `{timestamp}`
Decision: `{DECISION}`

## Result

4810 makes the sector-owner requirement explicit before the local Newton/GR coupling branch can advance:

```text
delta L_X = E_X delta X + d Theta_X
J_tau^X = Theta_X(L_tau X) - i_tau L_X = dQ_tau^X + C_tau^X
FB5540_guard = (|delta_H_tau_nonintegrable| + |Delta_ref| + |symplectic_boundary_flux|
                + |B_zero_flux| + |Delta_tau| + |bulk_X| + |edge_X| + |R11|) / |M_H_ref|
required: FB5540_guard <= {target['required_abs_max']}
```

The owner map is sharp, but current MTS does not yet close the physical owner stack. The strongest derivation route is still the no-pole quotient route; if that fails, the fallback is a complete no-cancellation source pack, not a symbolic `L_X` or cancellation between unknowns.

## Target Audit

{table(target_rows, ['audit_id', 'component_expr', 'required_abs_max', 'source', 'derivation', 'valid_for_claim', 'timestamp_utc'])}

## Source Register

{table(sources, ['source_id', 'source_path', 'exists', 'needle_found', 'role'])}

## Owner Clause Output

{table(outputs['owners'], ['owner_id', 'owner_target', 'owner_gate_status', 'owner_theorem', 'missing_owner_inputs', 'anti_circularity_status'])}

## Route Test Output

{table(outputs['routes'], ['route_id', 'route', 'route_status', 'route_theorem', 'missing_route_inputs', 'anti_circularity_status'])}

## FB5540 Source Row Output

{table(outputs['source_rows'], ['row_id', 'component_expr', 'FB5540_guard_abs', 'required_abs_max', 'numeric_window_pass', 'source_row_status', 'missing_source_inputs', 'anti_circularity_status'])}

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

    formal = f"""# 826 - PPC4161 sector Lagrangian boundary owner or FB5540 source row

Marker: `{MARKER}`
Generated: `{timestamp}`

4810 gives the local coupling obstruction a sector-owner gate:

```text
delta L_X = E_X delta X + d Theta_X
J_tau^X = Theta_X(L_tau X) - i_tau L_X = dQ_tau^X + C_tau^X
FB5540_guard = (|delta_H_tau_nonintegrable| + |Delta_ref| + |symplectic_boundary_flux|
                + |B_zero_flux| + |Delta_tau| + |bulk_X| + |edge_X| + |R11|) / |M_H_ref|
```

Unit bulk-X residual gives `1.0 <= 5.256633029822351`, but the physical branch remains nonclaim until the parent action owns `L_X`, `Theta_X`, `Q_tau^X`, `omega_X`, `B_ref`, `B_class`, `tau`, and `M_H_ref` together. Next target: `{NEXT_TARGET}`.
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
