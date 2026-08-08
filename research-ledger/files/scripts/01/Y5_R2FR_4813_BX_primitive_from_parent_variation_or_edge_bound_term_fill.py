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

CHECKPOINT = "4813"
CLAIM_ID = "L-655"
MARKER = "PPC4161_BX_PRIMITIVE_FROM_PARENT_VARIATION_OR_EDGE_BOUND_TERM_FILL_4813"
PACKET_MARKER = "PPC4161_PACKET_BX_PRIMITIVE_FROM_PARENT_VARIATION_OR_EDGE_BOUND_TERM_FILL_4813"
DECISION = "BX_PRIMITIVE_PARENT_VARIATION_AND_BRANCH_SEPARATION_GATE_NONCLAIM"
NEXT_TARGET = "4814-Y5-R2FR-vertical-quotient-LX-construction-or-scalar-nohair-branch-choice.md"

DOC_PATH = POST / "4813-Y5-R2FR-BX-primitive-from-parent-variation-or-edge-bound-term-fill.md"
FORMAL_PATH = FORMAL / "829-PPC4161-BX-primitive-from-parent-variation-or-edge-bound-term-fill.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"
RUNNER = SCRIPT_DIR / "BX_primitive_parent_variation_runner.py"

SOURCE_REGISTER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4813_SOURCE_REGISTER.csv"
TEMPLATE_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4813_PARENT_VARIATION_TEMPLATE_INPUT.csv"
TEMPLATE_OUTPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4813_PARENT_VARIATION_TEMPLATE_OUTPUT.csv"
PRIMITIVE_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4813_BX_PRIMITIVE_GATES_INPUT.csv"
PRIMITIVE_OUTPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4813_BX_PRIMITIVE_GATES_OUTPUT.csv"
SCALAR_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4813_SCALAR_BRANCH_INPUT.csv"
SCALAR_OUTPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4813_SCALAR_BRANCH_OUTPUT.csv"
EDGE_FILL_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4813_EDGE_BOUND_FILL_INPUT.csv"
EDGE_FILL_OUTPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4813_EDGE_BOUND_FILL_OUTPUT.csv"
TARGET_AUDIT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4813_TARGET_AUDIT.csv"
OBSTRUCTION_UPDATE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4813_OBSTRUCTION_UPDATE.csv"
GATE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4813_PROMOTION_GATES.csv"
FIREWALL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4813_FIREWALL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4813_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4813_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4813_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4813_VALIDATION.csv"

TARGET_4812 = SOURCE_DIR / "P8_Y5_R2FR_4812_TARGET_AUDIT.csv"
TEMPLATE_1021 = SOURCE_DIR / "P8_Y5_R10_1021_PARENT_VARIATION_TEMPLATE.csv"
GATES_1021 = SOURCE_DIR / "P8_Y5_R10_1021_BX_PRIMITIVE_GATES.csv"
SCALAR_1021 = SOURCE_DIR / "P8_Y5_R10_1021_SCALAR_BRANCH_SEPARATION.csv"
FILL_1021 = SOURCE_DIR / "P8_Y5_R10_1021_EDGE_BOUND_FILL_SCHEMA.csv"
VARIATION_667 = SOURCE_DIR / "P8_Y5_R10_667_VARIATION_LEDGER.csv"
ACTION_667 = SOURCE_DIR / "P8_Y5_R10_667_PARENT_BOUNDARY_ACTION_ANSATZ.csv"
CANDIDATES_669 = SOURCE_DIR / "P8_Y5_R10_669_MINIMAL_LX_OPERATOR_CANDIDATES.csv"
VARIATION_669 = SOURCE_DIR / "P8_Y5_R10_669_THETA_QX_VARIATION_LEDGER.csv"
MOMENTUM_583 = SOURCE_DIR / "P8_Y5_R10_583_NOETHER_MOMENTUM_MAP_CONTRACT.csv"
DCDAGGER_591 = SOURCE_DIR / "P8_Y5_R10_591_DCDAGGER_FORMULA.csv"

TEMPLATE_CLAUSES = (
    "parent_LX_signed",
    "Theta_X_signed",
    "Q_X_signed",
    "P_X_signed",
    "B_ct_signed",
    "same_parent_signed",
    "no_GR_import_signed",
    "no_fit_to_bound_signed",
)

PRIMITIVE_CLAUSES = (
    "same_parent_origin_signed",
    "counterterm_owner_signed",
    "exact_surface_pullback_signed",
    "harmonic_zero_or_bound_signed",
    "kernel_norm_zero_or_bound_signed",
    "overlap_compatibility_signed",
    "no_GR_import_signed",
    "no_fit_to_bound_signed",
)

SCALAR_CLAUSES = (
    "Z_X_positive_signed",
    "M_X2_positive_signed",
    "J_X_zero_signed",
    "boundary_flux_zero_signed",
    "matter_coupling_zero_signed",
    "nohair_domain_signed",
    "no_GR_import_signed",
    "no_fit_to_bound_signed",
)

FILL_TERMS = (
    "norm_bX_abs",
    "harmonic_edge_abs",
    "residual_edge_abs",
    "norm_dS_Feps_abs",
    "C_corner_abs",
)

SOURCE_SPECS = [
    ("SRC4813_00_4812_doc", POST / "4812-Y5-R2FR-boundary-cohomology-domain-certificate-or-source-pack-first-row.md", "BX-primitive-from-parent-variation-or-edge-bound-term-fill", "4812 selects B_X primitive target"),
    ("SRC4813_01_4812_target", TARGET_4812, "TGA4812_0_target_import", "4812 inherited target audit"),
    ("SRC4813_02_1021_doc", POST / "1021-Y5-R10-BX-primitive-from-parent-variation-or-edge-bound-term-fill.md", "PVT1021_3_BX_definition", "1021 B_X primitive precedent"),
    ("SRC4813_03_1021_template", TEMPLATE_1021, "PVT1021_3_BX_definition", "1021 parent variation template"),
    ("SRC4813_04_1021_gates", GATES_1021, "BXG1021_2_exact_surface_pullback", "1021 B_X primitive gates"),
    ("SRC4813_05_1021_scalar", SCALAR_1021, "SB1021_3_scalar_verdict", "1021 scalar branch separation"),
    ("SRC4813_06_1021_fill", FILL_1021, "EBF1021_0_norm_bX", "1021 edge-bound fill schema"),
    ("SRC4813_07_667_variation", VARIATION_667, "variation", "667 variation ledger"),
    ("SRC4813_08_667_action", ACTION_667, "boundary", "667 parent boundary action ansatz"),
    ("SRC4813_09_669_candidates", CANDIDATES_669, "scalar", "669 L_X candidates"),
    ("SRC4813_10_669_variation", VARIATION_669, "delta L_X = E_X delta X + d Theta_X", "669 Theta/QX variation ledger"),
    ("SRC4813_11_583_momentum", MOMENTUM_583, "momentum", "583 Noether momentum-map contract"),
    ("SRC4813_12_591_DCd", DCDAGGER_591, "DC", "591 DCdagger boundary adjoint"),
    ("SRC4813_13_runner", RUNNER, "def parent_template_row", "4813 executable primitive runner"),
]


RUNNER_TEXT = r'''from __future__ import annotations

import csv
import math
import sys
from pathlib import Path
from typing import Any


TEMPLATE_CLAUSES = (
    "parent_LX_signed",
    "Theta_X_signed",
    "Q_X_signed",
    "P_X_signed",
    "B_ct_signed",
    "same_parent_signed",
    "no_GR_import_signed",
    "no_fit_to_bound_signed",
)

PRIMITIVE_CLAUSES = (
    "same_parent_origin_signed",
    "counterterm_owner_signed",
    "exact_surface_pullback_signed",
    "harmonic_zero_or_bound_signed",
    "kernel_norm_zero_or_bound_signed",
    "overlap_compatibility_signed",
    "no_GR_import_signed",
    "no_fit_to_bound_signed",
)

SCALAR_CLAUSES = (
    "Z_X_positive_signed",
    "M_X2_positive_signed",
    "J_X_zero_signed",
    "boundary_flux_zero_signed",
    "matter_coupling_zero_signed",
    "nohair_domain_signed",
    "no_GR_import_signed",
    "no_fit_to_bound_signed",
)

FILL_TERMS = (
    "norm_bX_abs",
    "harmonic_edge_abs",
    "residual_edge_abs",
    "norm_dS_Feps_abs",
    "C_corner_abs",
)

FORBIDDEN_SOURCE_TOKENS = (
    "GR_IMPORT",
    "FIT_TO_BOUND",
    "BOUND_AS_SOURCE",
    "ORBITAL_GM_AS_SOURCE",
    "SYMBOLIC_BX_EXACT",
    "SCALAR_NOHAIR_AS_EDGE_PRIMITIVE",
    "SOURCE_FREE_BY_ASSERTION",
    "COUNTERTERM_BY_READOUT",
    "DELETE_HARMONIC_BY_ASSUMPTION",
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
        for field in ("template_id", "gate_id", "branch_id", "fill_id", "source_path", "equation_ref", "notes", "provenance")
    ).upper()
    return any(token in source_text for token in FORBIDDEN_SOURCE_TOKENS)


def missing_clauses(row: dict[str, Any], clauses: tuple[str, ...]) -> list[str]:
    return [clause for clause in clauses if not bool_text(row.get(clause))]


def clause_row(row: dict[str, Any], id_field: str, status_field: str, theorem_field: str, missing_field: str, clauses: tuple[str, ...], fail_status: str, blocked_status: str, signed_status: str) -> dict[str, Any]:
    row_id = str(row.get(id_field, "")).strip() or f"UNNAMED_{id_field.upper()}"
    output: dict[str, Any] = {id_field: row_id, "route": row.get("route", ""), "valid_for_claim": False, "claim_allowed": False}
    if forbidden_source_used(row):
        output.update({status_field: fail_status, theorem_field: False, missing_field: "FORBIDDEN_SOURCE", "anti_circularity_status": "FAIL_FORBIDDEN_SOURCE_USED"})
        return output
    missing = missing_clauses(row, clauses)
    status = signed_status if not missing else blocked_status
    output.update({status_field: status, theorem_field: not missing, missing_field: ";".join(missing), "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED"})
    return output


def parent_template_row(row: dict[str, Any]) -> dict[str, Any]:
    return clause_row(row, "template_id", "template_status", "template_theorem", "missing_template_inputs", TEMPLATE_CLAUSES, "FAILED_PARENT_TEMPLATE_GATE", "BLOCKED_MISSING_PARENT_VARIATION_INPUTS", "PARENT_VARIATION_TEMPLATE_SIGNED_CONDITIONAL_NONCLAIM")


def primitive_gate_row(row: dict[str, Any]) -> dict[str, Any]:
    return clause_row(row, "gate_id", "primitive_status", "primitive_theorem", "missing_primitive_inputs", PRIMITIVE_CLAUSES, "FAILED_BX_PRIMITIVE_GATE", "BLOCKED_MISSING_BX_PRIMITIVE_INPUTS", "BX_PRIMITIVE_SIGNED_CONDITIONAL_NONCLAIM")


def scalar_branch_row(row: dict[str, Any]) -> dict[str, Any]:
    return clause_row(row, "branch_id", "scalar_status", "scalar_theorem", "missing_scalar_inputs", SCALAR_CLAUSES, "FAILED_SCALAR_BRANCH_GATE", "BLOCKED_MISSING_SCALAR_NOHAIR_INPUTS", "SCALAR_NOHAIR_SIGNED_CONDITIONAL_NONCLAIM")


def fill_values(row: dict[str, Any]) -> tuple[float | None, list[str]]:
    missing: list[str] = []
    values: list[float] = []
    for term in FILL_TERMS:
        value = parse_float(row.get(term))
        if value is None or value < 0.0:
            missing.append(f"MISSING_{term}")
        else:
            values.append(value)
    if missing:
        return None, missing
    return sum(values), []


def edge_fill_row(row: dict[str, Any]) -> dict[str, Any]:
    fill_id = str(row.get("fill_id", "")).strip() or "UNNAMED_EDGE_FILL"
    output: dict[str, Any] = {"fill_id": fill_id, "quantity": row.get("quantity", ""), "valid_for_claim": False, "claim_allowed": False}
    if forbidden_source_used(row):
        output.update({"edge_fill_abs": "MISSING_NUMERIC_VALUE", "required_abs_max": format_float(parse_float(row.get("required_abs_max"))), "numeric_window_pass": False, "fill_status": "FAILED_EDGE_FILL_GATE", "missing_fill_inputs": "FORBIDDEN_EDGE_FILL_SOURCE", "anti_circularity_status": "FAIL_FORBIDDEN_SOURCE_USED"})
        return output
    required = parse_float(row.get("required_abs_max"))
    value, missing = fill_values(row)
    if required is None or required <= 0.0:
        missing.append("MISSING_required_abs_max")
    if missing_text(row.get("source_path")):
        missing.append("MISSING_source_path")
    if missing_text(row.get("equation_ref")):
        missing.append("MISSING_equation_ref")
    if not bool_text(row.get("source_signed")):
        missing.append("MISSING_source_signed")
    if required is None or required <= 0.0 or value is None:
        output.update({"edge_fill_abs": "MISSING_NUMERIC_VALUE", "required_abs_max": format_float(required), "numeric_window_pass": False, "fill_status": "BLOCKED_MISSING_EDGE_FILL_INPUTS", "missing_fill_inputs": ";".join(missing), "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED"})
        return output
    passes = value <= required
    status = "EDGE_FILL_NUMERIC_WINDOW_FAIL"
    if passes:
        status = "EDGE_FILL_NUMERIC_WINDOW_PASS_SOURCE_UNSIGNED_NONCLAIM"
        if bool_text(row.get("source_signed")) and bool_text(row.get("valid_for_claim")):
            status = "EDGE_FILL_NUMERIC_WINDOW_PASS_SOURCE_SIGNED_NONCLAIM"
    output.update({"edge_fill_abs": format_float(value), "required_abs_max": format_float(required), "numeric_window_pass": passes, "fill_status": status, "missing_fill_inputs": ";".join(missing), "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED"})
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
    if len(sys.argv) != 4 or sys.argv[1] not in {"template", "primitive", "scalar", "fill"}:
        print("Usage: BX_primitive_parent_variation_runner.py template|primitive|scalar|fill INPUT_CSV OUTPUT_CSV", file=sys.stderr)
        return 2
    rows = read_csv(Path(sys.argv[2]))
    mode = sys.argv[1]
    if mode == "template":
        outputs = [parent_template_row(row) for row in rows]
    elif mode == "primitive":
        outputs = [primitive_gate_row(row) for row in rows]
    elif mode == "scalar":
        outputs = [scalar_branch_row(row) for row in rows]
    else:
        outputs = [edge_fill_row(row) for row in rows]
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
    rows = read_csv(TARGET_4812)
    if not rows:
        raise RuntimeError("missing 4812 target rows")
    return {"component_expr": "abs(edge_fill)", "required_abs_max": rows[0]["required_abs_max"], "source": str(TARGET_4812)}


def source_register(timestamp: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path, needle, role in SOURCE_SPECS:
        text = read_text(path)
        rows.append({"checkpoint": CHECKPOINT, "source_id": source_id, "source_path": str(path), "exists": path.exists(), "needle": needle, "needle_found": bool(text and needle in text), "role": role, "valid_for_claim": False, "timestamp_utc": timestamp})
    return rows


def bools(names: tuple[str, ...], signed: bool) -> dict[str, bool]:
    return {name: signed for name in names}


def missing_fill_terms() -> dict[str, str]:
    return {term: "MISSING_PARENT_VALUE" for term in FILL_TERMS}


def zero_fill_terms() -> dict[str, str]:
    return {term: "0.0" for term in FILL_TERMS}


def unit_fill_terms() -> dict[str, str]:
    return {"norm_bX_abs": "1.0", "harmonic_edge_abs": "0.0", "residual_edge_abs": "0.0", "norm_dS_Feps_abs": "0.0", "C_corner_abs": "0.0"}


def strict_fill_terms() -> dict[str, str]:
    values = unit_fill_terms()
    values["norm_bX_abs"] = "10.0"
    return values


def write_runner() -> None:
    SCRIPT_DIR.mkdir(parents=True, exist_ok=True)
    RUNNER.write_text(RUNNER_TEXT, encoding="utf-8")


def write_inputs(timestamp: str, target: dict[str, str]) -> None:
    required = target["required_abs_max"]
    write_csv(TARGET_AUDIT_CSV, [{"audit_id": "TGA4813_0_target_import", "component_expr": "abs(edge_fill)", "required_abs_max": required, "source": target["source"], "derivation": "same normalized local coupling window inherited from 4812 weighted-Stokes edge-bound target", "valid_for_claim": False, "timestamp_utc": timestamp}])
    template_rows = [
        {"template_id": "physical_parent_variation_missing", "route": "physical_missing", **bools(TEMPLATE_CLAUSES, False), "no_GR_import_signed": True, "no_fit_to_bound_signed": True, "source_path": "MISSING_PARENT_LX_THETA_QX_PX_BCT", "equation_ref": "MISSING_PARENT_VARIATION_EQUATION", "notes": "physical branch lacks signed L_X, Theta_X, Q_X, P_X, B_ct from one parent action", "provenance": "4813 physical branch", "valid_for_claim": False},
        {"template_id": "parent_variation_template_unsigned", "route": "template_written_not_owned", **bools(TEMPLATE_CLAUSES, False), "no_GR_import_signed": True, "no_fit_to_bound_signed": True, "source_path": str(TEMPLATE_1021), "equation_ref": "PVT1021_0_to_PVT1021_5", "notes": "template exists but parent ownership is unsigned", "provenance": "1021 parent variation template", "valid_for_claim": False},
        {"template_id": "conditional_parent_variation", "route": "conditional_theorem", **bools(TEMPLATE_CLAUSES, True), "source_path": str(POST / "1021-Y5-R10-BX-primitive-from-parent-variation-or-edge-bound-term-fill.md"), "equation_ref": "PVT1021 conditional map", "notes": "conditional branch only", "provenance": "1021 template", "valid_for_claim": False},
        {"template_id": "forbidden_counterterm_readout_control", "route": "forbidden_control", **bools(TEMPLATE_CLAUSES, True), "source_path": "COUNTERTERM_BY_READOUT_ORBITAL_GM_AS_SOURCE", "equation_ref": "FORBIDDEN_COUNTERTERM", "notes": "control row must fail if B_ct is chosen after readout", "provenance": "forbidden control", "valid_for_claim": False},
    ]
    primitive_rows = [
        {"gate_id": "physical_BX_primitive_missing", "route": "physical_missing", **bools(PRIMITIVE_CLAUSES, False), "no_GR_import_signed": True, "no_fit_to_bound_signed": True, "source_path": "MISSING_PARENT_BX_PRIMITIVE", "equation_ref": "MISSING_BX_PRIMITIVE_EQUATION", "notes": "physical branch lacks same-parent origin, counterterm owner, exact pullback, harmonic/kernel bounds and overlap compatibility", "provenance": "4813 physical branch", "valid_for_claim": False},
        {"gate_id": "BX_primitive_gates_unsigned", "route": "primitive_contract_not_closed", **bools(PRIMITIVE_CLAUSES, False), "no_GR_import_signed": True, "no_fit_to_bound_signed": True, "source_path": str(GATES_1021), "equation_ref": "BXG1021_0_to_BXG1021_5", "notes": "primitive gates exist but remain unsigned", "provenance": "1021 primitive gates", "valid_for_claim": False},
        {"gate_id": "conditional_BX_primitive", "route": "conditional_theorem", **bools(PRIMITIVE_CLAUSES, True), "source_path": str(POST / "1021-Y5-R10-BX-primitive-from-parent-variation-or-edge-bound-term-fill.md"), "equation_ref": "BXG1021 conditional closure", "notes": "conditional branch only", "provenance": "1021 primitive gates", "valid_for_claim": False},
        {"gate_id": "forbidden_symbolic_BX_exact", "route": "forbidden_control", **bools(PRIMITIVE_CLAUSES, True), "source_path": "SYMBOLIC_BX_EXACT_DELETE_HARMONIC_BY_ASSUMPTION", "equation_ref": "FORBIDDEN_SYMBOLIC_BX", "notes": "control row must fail if exactness is asserted without primitive/cohomology", "provenance": "forbidden control", "valid_for_claim": False},
    ]
    scalar_rows = [
        {"branch_id": "physical_scalar_nohair_missing", "route": "physical_missing", **bools(SCALAR_CLAUSES, False), "no_GR_import_signed": True, "no_fit_to_bound_signed": True, "source_path": "MISSING_PARENT_SCALAR_NOHAIR_INPUTS", "equation_ref": "MISSING_SCALAR_NOHAIR_EQUATION", "notes": "physical scalar route lacks Z, mass gap, zero source, boundary flux and matter-coupling silence", "provenance": "4813 physical branch", "valid_for_claim": False},
        {"branch_id": "scalar_branch_separated_unsigned", "route": "separate_scalar_nohair_route", **bools(SCALAR_CLAUSES, False), "no_GR_import_signed": True, "no_fit_to_bound_signed": True, "source_path": str(SCALAR_1021), "equation_ref": "SB1021_0_to_SB1021_3", "notes": "scalar route is separated from Noether edge primitive but not signed", "provenance": "1021 scalar separation", "valid_for_claim": False},
        {"branch_id": "conditional_scalar_nohair", "route": "conditional_theorem", **bools(SCALAR_CLAUSES, True), "source_path": str(SCALAR_1021), "equation_ref": "SB1021 conditional no-hair", "notes": "conditional branch only", "provenance": "1021 scalar separation", "valid_for_claim": False},
        {"branch_id": "forbidden_scalar_as_edge_primitive", "route": "forbidden_control", **bools(SCALAR_CLAUSES, True), "source_path": "SCALAR_NOHAIR_AS_EDGE_PRIMITIVE_SOURCE_FREE_BY_ASSERTION", "equation_ref": "FORBIDDEN_SCALAR_MIX", "notes": "control row must fail if scalar no-hair is mislabeled as Noether edge primitive", "provenance": "forbidden control", "valid_for_claim": False},
    ]
    fill_rows = [
        {"fill_id": "physical_edge_fill_missing", "quantity": "EDGEBOUND first term pack", **missing_fill_terms(), "required_abs_max": required, "source_signed": False, "source_path": "MISSING_PARENT_EDGE_FILL_TERMS", "equation_ref": "MISSING_EDGE_FILL_EQUATION", "notes": "physical fill lacks norm_bX, harmonic, residual, kernel and corner terms", "provenance": "4813 physical branch", "valid_for_claim": False},
        {"fill_id": "edge_fill_schema_missing", "quantity": "EDGEBOUND first term pack", **missing_fill_terms(), "required_abs_max": required, "source_signed": False, "source_path": str(FILL_1021), "equation_ref": "EBF1021_0_to_EBF1021_5", "notes": "schema exists but terms are missing", "provenance": "1021 fill schema", "valid_for_claim": False},
        {"fill_id": "unit_norm_bX_fill_smoke", "quantity": "EDGEBOUND first term pack", **unit_fill_terms(), "required_abs_max": required, "source_signed": False, "source_path": str(FILL_1021), "equation_ref": "unit norm_bX smoke", "notes": "unit norm_bX term is below current target but remains nonclaim", "provenance": "4813 smoke row", "valid_for_claim": False},
        {"fill_id": "strict_norm_bX_fill_fail", "quantity": "EDGEBOUND first term pack", **strict_fill_terms(), "required_abs_max": required, "source_signed": False, "source_path": str(FILL_1021), "equation_ref": "strict fail control", "notes": "control row proves oversized edge-fill term fails", "provenance": "4813 control", "valid_for_claim": False},
        {"fill_id": "conditional_zero_edge_fill", "quantity": "EDGEBOUND first term pack", **zero_fill_terms(), "required_abs_max": required, "source_signed": True, "source_path": str(POST / "1021-Y5-R10-BX-primitive-from-parent-variation-or-edge-bound-term-fill.md"), "equation_ref": "conditional zero fill", "notes": "conditional branch only", "provenance": "1021 conditional branch", "valid_for_claim": False},
        {"fill_id": "forbidden_bound_source_fill", "quantity": "EDGEBOUND first term pack", **zero_fill_terms(), "required_abs_max": required, "source_signed": True, "source_path": "BOUND_AS_SOURCE_FIT_TO_BOUND", "equation_ref": "FORBIDDEN_FILL", "notes": "control row must fail if bound supplies source coefficient", "provenance": "forbidden control", "valid_for_claim": False},
    ]
    write_csv(TEMPLATE_INPUT_CSV, template_rows)
    write_csv(PRIMITIVE_INPUT_CSV, primitive_rows)
    write_csv(SCALAR_INPUT_CSV, scalar_rows)
    write_csv(EDGE_FILL_INPUT_CSV, fill_rows)


def run_runner() -> None:
    subprocess.run([sys.executable, str(RUNNER), "template", str(TEMPLATE_INPUT_CSV), str(TEMPLATE_OUTPUT_CSV)], check=True)
    subprocess.run([sys.executable, str(RUNNER), "primitive", str(PRIMITIVE_INPUT_CSV), str(PRIMITIVE_OUTPUT_CSV)], check=True)
    subprocess.run([sys.executable, str(RUNNER), "scalar", str(SCALAR_INPUT_CSV), str(SCALAR_OUTPUT_CSV)], check=True)
    subprocess.run([sys.executable, str(RUNNER), "fill", str(EDGE_FILL_INPUT_CSV), str(EDGE_FILL_OUTPUT_CSV)], check=True)


def make_output_tables() -> dict[str, list[dict[str, Any]]]:
    templates = read_csv(TEMPLATE_OUTPUT_CSV)
    primitives = read_csv(PRIMITIVE_OUTPUT_CSV)
    scalars = read_csv(SCALAR_OUTPUT_CSV)
    fills = read_csv(EDGE_FILL_OUTPUT_CSV)
    obstruction = [
        {"update_id": "OBS4813_0_template", "item": "parent variation to B_X map", "status": "BLOCKED_MISSING_PARENT_VARIATION_INPUTS", "value_or_bound": "L_X/Theta_X/Q_X/P_X/B_ct from one parent action", "meaning": "B_X remains a contract, not a derived primitive"},
        {"update_id": "OBS4813_1_primitive", "item": "B_X primitive gate", "status": "BLOCKED_MISSING_BX_PRIMITIVE_INPUTS", "value_or_bound": "B_X=d_S b_X+h_X+r_X requires same-parent origin, counterterm, exact pullback, harmonic/kernel bounds", "meaning": "edge exactness cannot be claimed"},
        {"update_id": "OBS4813_2_scalar_split", "item": "scalar no-hair branch separation", "status": "BLOCKED_MISSING_SCALAR_NOHAIR_INPUTS", "value_or_bound": "Z_X>0, M_X^2>0, J_X=0, boundary_flux=0", "meaning": "scalar silence is a separate proof, not Noether edge exactness"},
        {"update_id": "OBS4813_3_fill", "item": "first edge-bound fill row", "status": "EDGE_FILL_NUMERIC_WINDOW_PASS_SOURCE_UNSIGNED_NONCLAIM", "value_or_bound": "1.000000000000000e+00 <= 5.256633029822351e+00", "meaning": "unit norm_bX smoke fits current window; physical terms remain missing"},
    ]
    gates = [
        {"gate_id": "PG4813_0_template_contract", "claim": "Parent variation to B_X template is executable", "gate_pass": True, "reason": "L_X, Theta_X, Q_X, P_X, B_ct and decomposition clauses are explicit", "evidence": str(TEMPLATE_OUTPUT_CSV)},
        {"gate_id": "PG4813_1_BX_primitive", "claim": "B_X primitive is derived in current MTS", "gate_pass": False, "reason": "same-parent origin, counterterm, exact pullback, harmonic/kernel/overlap clauses remain unsigned", "evidence": str(PRIMITIVE_OUTPUT_CSV)},
        {"gate_id": "PG4813_2_scalar_nohair", "claim": "Scalar-like X local silence is proved", "gate_pass": False, "reason": "Z_X, M_X^2, J_X=0, boundary_flux and matter-coupling silence remain unsigned", "evidence": str(SCALAR_OUTPUT_CSV)},
        {"gate_id": "PG4813_3_edge_fill", "claim": "Edge-bound fill row is claim-ready", "gate_pass": False, "reason": "physical fill terms and source paths are missing", "evidence": str(EDGE_FILL_OUTPUT_CSV)},
        {"gate_id": "PG4813_4_Newton_local_GR", "claim": "Newton/local-GR source coupling promotion is allowed", "gate_pass": False, "reason": "B_X primitive, scalar no-hair and edge fill fallback are all nonclaim", "evidence": "nonclaim firewall active"},
    ]
    firewalls = [
        {"firewall_id": "FW4813_0_no_symbolic_BX", "rule": "B_X exactness requires explicit b_X or bounded h_X/r_X terms.", "status": "ACTIVE"},
        {"firewall_id": "FW4813_1_no_counterterm_readout", "rule": "B_ct cannot be chosen after orbital/readout fitting.", "status": "ACTIVE"},
        {"firewall_id": "FW4813_2_no_scalar_edge_mix", "rule": "Scalar no-hair proof cannot be relabeled as Noether edge primitive proof.", "status": "ACTIVE"},
        {"firewall_id": "FW4813_3_no_source_free_assertion", "rule": "J_X=0 and boundary_flux=0 must be parent-signed, not asserted.", "status": "ACTIVE"},
    ]
    decisions = [
        {"decision_id": "DEC4813_0_primitive_result", "decision": "explicit_BX_primitive_not_derived_from_current_files", "reason": "parent L_X/Theta_X/Q_X/P_X/B_ct chain is still a contract", "next_action": "do not claim Q_edge zero"},
        {"decision_id": "DEC4813_1_route_split", "decision": "vertical_quotient_and_scalar_nohair_routes_must_be_separated", "reason": "scalar positive operator can kill X only by no-hair/source-free proof, not by Noether edge primitive", "next_action": NEXT_TARGET},
        {"decision_id": "DEC4813_2_best_next", "decision": "vertical_quotient_LX_construction_is_least_scrutiny_route", "reason": "it removes the local pole before fitting source coefficients", "next_action": NEXT_TARGET},
        {"decision_id": "DEC4813_3_fallback", "decision": "edge_bound_and_scalar_coefficients_required_if_parent_route_fails", "reason": "then the theory must survive as bounded residuals", "next_action": "fill EBF terms plus Z_X/M_X2/J_X/K_X/Qbar/qbar rows"},
    ]
    status = [
        {"status_id": "STATUS4813_0_template", "status": "PARENT_VARIATION_TEMPLATE_WRITTEN_NOT_OWNED", "detail": "B_X map explicit but unsigned"},
        {"status_id": "STATUS4813_1_primitive", "status": "BX_PRIMITIVE_NOT_DERIVED", "detail": "b_X/h_X/r_X remain missing or unbounded"},
        {"status_id": "STATUS4813_2_scalar", "status": "SCALAR_BRANCH_SEPARATED_NOT_PROVED", "detail": "do not mix scalar no-hair with edge primitive proof"},
        {"status_id": "STATUS4813_3_next", "status": "VERTICAL_QUOTIENT_LX_OR_SCALAR_NOHAIR_BRANCH_CHOICE", "detail": NEXT_TARGET},
    ]
    next_rows = [{"route_id": "NEXT4813_0_primary", "next_target": NEXT_TARGET, "script": "scripts/Y5_R2FR_4814_vertical_quotient_LX_construction_or_scalar_nohair_branch_choice.py", "objective": "choose and test vertical/quotient L_X construction or scalar no-hair/source-coefficient route without mixing proof languages", "selection_status": "selected", "success_condition": "X is removed as absent/vertical before variation or scalar branch gets a real no-hair/source-coefficient gate"}]
    write_csv(OBSTRUCTION_UPDATE_CSV, obstruction)
    write_csv(GATE_CSV, gates)
    write_csv(FIREWALL_CSV, firewalls)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, status)
    write_csv(NEXT_TARGET_CSV, next_rows)
    return {"templates": templates, "primitives": primitives, "scalars": scalars, "fills": fills, "obstruction": obstruction, "gates": gates, "firewalls": firewalls, "decisions": decisions, "status": status, "next": next_rows}


def validate() -> list[dict[str, Any]]:
    sources = read_csv(SOURCE_REGISTER_CSV)
    templates = {row["template_id"]: row for row in read_csv(TEMPLATE_OUTPUT_CSV)}
    primitives = {row["gate_id"]: row for row in read_csv(PRIMITIVE_OUTPUT_CSV)}
    scalars = {row["branch_id"]: row for row in read_csv(SCALAR_OUTPUT_CSV)}
    fills = {row["fill_id"]: row for row in read_csv(EDGE_FILL_OUTPUT_CSV)}
    source_pass = all(row["exists"] == "True" and row["needle_found"] == "True" for row in sources)
    checks = [
        {"check_id": "VAL4813_0_sources", "description": "all cited sources exist and needles are found", "result": "PASS" if source_pass else "FAIL", "evidence": str(SOURCE_REGISTER_CSV)},
        {"check_id": "VAL4813_1_template_blocks", "description": "physical parent variation template remains blocked", "result": "PASS" if templates["physical_parent_variation_missing"]["template_status"] == "BLOCKED_MISSING_PARENT_VARIATION_INPUTS" else "FAIL", "evidence": str(TEMPLATE_OUTPUT_CSV)},
        {"check_id": "VAL4813_2_forbidden_template_fails", "description": "forbidden counterterm/readout control fails", "result": "PASS" if templates["forbidden_counterterm_readout_control"]["anti_circularity_status"] == "FAIL_FORBIDDEN_SOURCE_USED" else "FAIL", "evidence": str(TEMPLATE_OUTPUT_CSV)},
        {"check_id": "VAL4813_3_primitive_blocks", "description": "physical B_X primitive remains blocked", "result": "PASS" if primitives["physical_BX_primitive_missing"]["primitive_status"] == "BLOCKED_MISSING_BX_PRIMITIVE_INPUTS" else "FAIL", "evidence": str(PRIMITIVE_OUTPUT_CSV)},
        {"check_id": "VAL4813_4_forbidden_BX_fails", "description": "forbidden symbolic B_X exactness control fails", "result": "PASS" if primitives["forbidden_symbolic_BX_exact"]["anti_circularity_status"] == "FAIL_FORBIDDEN_SOURCE_USED" else "FAIL", "evidence": str(PRIMITIVE_OUTPUT_CSV)},
        {"check_id": "VAL4813_5_scalar_blocks", "description": "physical scalar no-hair branch remains blocked", "result": "PASS" if scalars["physical_scalar_nohair_missing"]["scalar_status"] == "BLOCKED_MISSING_SCALAR_NOHAIR_INPUTS" else "FAIL", "evidence": str(SCALAR_OUTPUT_CSV)},
        {"check_id": "VAL4813_6_forbidden_scalar_fails", "description": "forbidden scalar-as-edge control fails", "result": "PASS" if scalars["forbidden_scalar_as_edge_primitive"]["anti_circularity_status"] == "FAIL_FORBIDDEN_SOURCE_USED" else "FAIL", "evidence": str(SCALAR_OUTPUT_CSV)},
        {"check_id": "VAL4813_7_edge_fill_blocks", "description": "physical edge fill row remains blocked", "result": "PASS" if fills["physical_edge_fill_missing"]["fill_status"] == "BLOCKED_MISSING_EDGE_FILL_INPUTS" else "FAIL", "evidence": str(EDGE_FILL_OUTPUT_CSV)},
        {"check_id": "VAL4813_8_unit_fill_passes", "description": "unit norm_bX fill smoke passes target window", "result": "PASS" if fills["unit_norm_bX_fill_smoke"]["numeric_window_pass"] == "True" else "FAIL", "evidence": str(EDGE_FILL_OUTPUT_CSV)},
        {"check_id": "VAL4813_9_strict_fail", "description": "strict norm_bX fill control fails numeric target", "result": "PASS" if fills["strict_norm_bX_fill_fail"]["numeric_window_pass"] == "False" and fills["strict_norm_bX_fill_fail"]["fill_status"] == "EDGE_FILL_NUMERIC_WINDOW_FAIL" else "FAIL", "evidence": str(EDGE_FILL_OUTPUT_CSV)},
        {"check_id": "VAL4813_10_forbidden_fill_fails", "description": "forbidden bound-as-source fill control fails", "result": "PASS" if fills["forbidden_bound_source_fill"]["anti_circularity_status"] == "FAIL_FORBIDDEN_SOURCE_USED" else "FAIL", "evidence": str(EDGE_FILL_OUTPUT_CSV)},
        {"check_id": "VAL4813_11_claim", "description": "claim register includes L-655 as nonclaim", "result": "PASS" if CLAIM_ID in read_text(CLAIMS_PATH) and DECISION in read_text(CLAIMS_PATH) else "FAIL", "evidence": str(CLAIMS_PATH)},
        {"check_id": "VAL4813_12_resume", "description": "resume points at 4814", "result": "PASS" if NEXT_TARGET in read_text(RESUME_PATH) else "FAIL", "evidence": str(RESUME_PATH)},
    ]
    checks.append({"check_id": "VAL4813_OVERALL", "description": "all 4813 B_X primitive checks pass", "result": "PASS" if all(row["result"] == "PASS" for row in checks) else "FAIL", "evidence": DECISION})
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
    if CLAIM_ID in read_text(CLAIMS_PATH):
        return
    row = {"claim_id": CLAIM_ID, "domain": "local_gr", "claim": "BX_primitive_parent_variation_runner", "current_evidence": "4813 installs the parent-variation to B_X primitive gate, separates scalar no-hair from Noether edge exactness, and stages edge-bound fill rows; unit norm_bX smoke passes current window but remains source-unsigned.", "status": "BX_primitive_parent_variation_private_nonclaim", "next_test": NEXT_TARGET, "key_risk": "symbolic B_X exactness; counterterm by readout; scalar no-hair as edge primitive; source-free by assertion", "sector": "local_gr", "evidence": str(DOC_PATH), "next_action": NEXT_TARGET, "risk": "missing parent L_X/Theta/Q/P/Bct; missing b_X primitive; harmonic deletion; scalar/Noether proof mix; bound-as-source", "title": "B_X primitive parent variation and branch separation gate", "notes": f"{MARKER}; {DECISION}; generated {timestamp}"}
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        csv.DictWriter(handle, fieldnames=list(row)).writerow(row)


def update_registers(timestamp: str) -> None:
    append_claim(timestamp)
    append_once(SPINE_PATH, MARKER, f"""

## {MARKER}

4813 makes the `B_X` primitive route explicit:

```text
delta L_X = E_A^X delta X^A + d Theta_X
B_X := i_S^*(n_mu P_X^{{mu nu}} epsilon_nu + B_ct[epsilon])
B_X = d_S b_X + h_X + r_X
```

Current MTS has the map but not the parent-signed objects. The scalar-like positive branch is now separated from the Noether edge-charge route: scalar no-hair can silence a physical X profile only through `Z_X>0`, `M_X^2>0`, `J_X=0`, and boundary flux zero; it cannot be used as a shortcut for `Q_edge=0`.
""")
    append_once(PACKET_PATH, PACKET_MARKER, f"""

## {PACKET_MARKER}

- Checkpoint: `{DOC_PATH}`
- Formal note: `{FORMAL_PATH}`
- Runner: `{RUNNER}`
- Claim row: `{CLAIM_ID}`
- Decision: `{DECISION}`
- Next: `{NEXT_TARGET}`
""")
    RESUME_PATH.write_text(f"""# Current local resume

Updated: `{timestamp}`
Last checkpoint: `4813-Y5-R2FR-BX-primitive-from-parent-variation-or-edge-bound-term-fill.md`
Marker: `{MARKER}`

## Where we are

4813 installed the `B_X` primitive/branch-separation gate:

```text
delta L_X = E_A^X delta X^A + d Theta_X
B_X := i_S^*(n_mu P_X^{{mu nu}} epsilon_nu + B_ct[epsilon])
B_X = d_S b_X + h_X + r_X
```

## Live blockers

- `L_X`, `Theta_X`, `Q_X`, `P_X`, and `B_ct` are still contracts, not one parent-signed variation.
- `b_X`, `h_X`, and `r_X` are not derived or bounded.
- Scalar no-hair and Noether edge exactness are separate proof routes and must not be mixed.

## Next target

`{NEXT_TARGET}`
""", encoding="utf-8")


def write_docs(timestamp: str, target: dict[str, str], outputs: dict[str, list[dict[str, Any]]], validation: list[dict[str, Any]]) -> None:
    sources = read_csv(SOURCE_REGISTER_CSV)
    target_rows = read_csv(TARGET_AUDIT_CSV)
    doc = f"""# 4813 - B_X primitive from parent variation or edge bound term fill

Marker: `{MARKER}`
Generated: `{timestamp}`
Decision: `{DECISION}`

## Result

4813 tests whether the weighted-Stokes primitive is actually derivable:

```text
delta L_X = E_A^X delta X^A + d Theta_X
B_X := i_S^*(n_mu P_X^{{mu nu}} epsilon_nu + B_ct[epsilon])
B_X = d_S b_X + h_X + r_X
required edge-fill envelope <= {target['required_abs_max']}
```

Current MTS has the parent-variation map, but not the parent-signed `L_X/Theta_X/Q_X/P_X/B_ct` chain needed to construct `b_X`. The scalar-like branch is separated from the Noether edge route so a scalar no-hair proof cannot be smuggled in as `Q_edge=0`.

## Target Audit

{table(target_rows, ['audit_id', 'component_expr', 'required_abs_max', 'source', 'derivation', 'valid_for_claim', 'timestamp_utc'])}

## Source Register

{table(sources, ['source_id', 'source_path', 'exists', 'needle_found', 'role'])}

## Parent Variation Template Output

{table(outputs['templates'], ['template_id', 'route', 'template_status', 'template_theorem', 'missing_template_inputs', 'anti_circularity_status'])}

## B_X Primitive Gate Output

{table(outputs['primitives'], ['gate_id', 'route', 'primitive_status', 'primitive_theorem', 'missing_primitive_inputs', 'anti_circularity_status'])}

## Scalar Branch Output

{table(outputs['scalars'], ['branch_id', 'route', 'scalar_status', 'scalar_theorem', 'missing_scalar_inputs', 'anti_circularity_status'])}

## Edge Bound Fill Output

{table(outputs['fills'], ['fill_id', 'quantity', 'edge_fill_abs', 'required_abs_max', 'numeric_window_pass', 'fill_status', 'missing_fill_inputs', 'anti_circularity_status'])}

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
    FORMAL_PATH.write_text(f"""# 829 - PPC4161 B_X primitive from parent variation or edge bound term fill

Marker: `{MARKER}`
Generated: `{timestamp}`

4813 gives the edge primitive its parent-variation gate:

```text
delta L_X = E_A^X delta X^A + d Theta_X
B_X := i_S^*(n_mu P_X^{{mu nu}} epsilon_nu + B_ct[epsilon])
B_X = d_S b_X + h_X + r_X
```

Unit `norm_bX` fill gives `1.0 <= 5.256633029822351`, but the physical branch remains nonclaim until the parent variation constructs `P_X/B_ct/b_X` or the scalar branch proves source-free no-hair on its own terms. Next target: `{NEXT_TARGET}`.
""", encoding="utf-8")


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
