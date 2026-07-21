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

CHECKPOINT = "4814"
CLAIM_ID = "L-656"
MARKER = "PPC4161_VERTICAL_QUOTIENT_LX_CONSTRUCTION_OR_SCALAR_NOHAIR_BRANCH_CHOICE_4814"
PACKET_MARKER = "PPC4161_PACKET_VERTICAL_QUOTIENT_LX_CONSTRUCTION_OR_SCALAR_NOHAIR_BRANCH_CHOICE_4814"
DECISION = "VERTICAL_QUOTIENT_LX_CONSTRUCTION_SELECTED_SCALAR_NOHAIR_FALLBACK_NONCLAIM"
NEXT_TARGET = "4815-Y5-R2FR-q-vX-action-descent-certificate-or-scalar-nohair-demotion.md"

DOC_PATH = POST / "4814-Y5-R2FR-vertical-quotient-LX-construction-or-scalar-nohair-branch-choice.md"
FORMAL_PATH = FORMAL / "830-PPC4161-vertical-quotient-LX-construction-or-scalar-nohair-branch-choice.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"
RUNNER = SCRIPT_DIR / "vertical_quotient_scalar_branch_choice_runner.py"

SOURCE_REGISTER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4814_SOURCE_REGISTER.csv"
BRANCH_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4814_BRANCH_DECISION_INPUT.csv"
BRANCH_OUTPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4814_BRANCH_DECISION_OUTPUT.csv"
VERTICAL_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4814_VERTICAL_QUOTIENT_INPUT.csv"
VERTICAL_OUTPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4814_VERTICAL_QUOTIENT_OUTPUT.csv"
SCALAR_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4814_SCALAR_NOHAIR_INPUT.csv"
SCALAR_OUTPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4814_SCALAR_NOHAIR_OUTPUT.csv"
FALLBACK_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4814_FALLBACK_SOURCE_ROWS_INPUT.csv"
FALLBACK_OUTPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4814_FALLBACK_SOURCE_ROWS_OUTPUT.csv"
TARGET_AUDIT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4814_TARGET_AUDIT.csv"
OBSTRUCTION_UPDATE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4814_OBSTRUCTION_UPDATE.csv"
GATE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4814_PROMOTION_GATES.csv"
FIREWALL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4814_FIREWALL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4814_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4814_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4814_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4814_VALIDATION.csv"

TARGET_4813 = SOURCE_DIR / "P8_Y5_R2FR_4813_TARGET_AUDIT.csv"
BRANCH_1022 = SOURCE_DIR / "P8_Y5_R10_1022_BRANCH_DECISION_MATRIX.csv"
VERTICAL_1022 = SOURCE_DIR / "P8_Y5_R10_1022_VERTICAL_QUOTIENT_CONSTRUCTION.csv"
SCALAR_1022 = SOURCE_DIR / "P8_Y5_R10_1022_SCALAR_NOHAIR_CONSTRUCTION.csv"
FALLBACK_1022 = SOURCE_DIR / "P8_Y5_R10_1022_FALLBACK_SOURCE_ROWS.csv"
QVT_581 = SOURCE_DIR / "P8_Y5_R10_581_QUOTIENT_VERTICAL_THEOREM_CHAIN.csv"
QMAP_637 = SOURCE_DIR / "P8_Y5_R10_637_QUOTIENT_MAP_DERIVATION.csv"
OBS_637 = SOURCE_DIR / "P8_Y5_R10_637_OBS_FUNCTOR_DERIVATION.csv"
DVM_590 = SOURCE_DIR / "P8_Y5_R10_590_DCDAGGER_VERTICAL_MAP.csv"
SOURCEFREE_670 = SOURCE_DIR / "P8_Y5_R10_670_POSITIVE_SOURCEFREE_PROOF_CHAIN.csv"

BRANCH_CLAUSES = (
    "branch_separated_signed",
    "quotient_attempt_selected_signed",
    "scalar_demoted_to_fallback_signed",
    "source_residual_last_resort_signed",
    "no_route_mixing_signed",
    "no_GR_import_signed",
    "no_fit_to_bound_signed",
)

VERTICAL_CLAUSES = (
    "q_map_signed",
    "action_descent_signed",
    "matter_descent_signed",
    "vertical_generator_signed",
    "momentum_map_signed",
    "boundary_silence_signed",
    "degree_count_signed",
    "no_GR_import_signed",
    "no_fit_to_bound_signed",
)

SCALAR_CLAUSES = (
    "operator_self_adjoint_signed",
    "Z_positive_signed",
    "M2_positive_signed",
    "J_zero_signed",
    "boundary_flux_zero_signed",
    "energy_identity_signed",
    "no_GR_import_signed",
    "no_fit_to_bound_signed",
)

FALLBACK_TERMS = (
    "quotient_certificate_abs",
    "scalar_operator_abs",
    "sourced_alpha_abs",
    "edge_bound_abs",
    "total_guard_abs",
)

SOURCE_SPECS = [
    ("SRC4814_00_4813_doc", POST / "4813-Y5-R2FR-BX-primitive-from-parent-variation-or-edge-bound-term-fill.md", "vertical_quotient_LX_construction_is_least_scrutiny_route", "4813 selects vertical/quotient route"),
    ("SRC4814_01_4813_target", TARGET_4813, "TGA4813_0_target_import", "4813 inherited target audit"),
    ("SRC4814_02_1022_doc", POST / "1022-Y5-R10-vertical-quotient-LX-construction-or-scalar-nohair-branch-choice.md", "BDM1022_0_absent_quotient", "1022 branch-choice precedent"),
    ("SRC4814_03_1022_branch", BRANCH_1022, "BDM1022_0_absent_quotient", "1022 branch matrix"),
    ("SRC4814_04_1022_vertical", VERTICAL_1022, "VQC1022_0_q_map", "1022 vertical quotient clauses"),
    ("SRC4814_05_1022_scalar", SCALAR_1022, "SNH1022_0_operator", "1022 scalar no-hair clauses"),
    ("SRC4814_06_1022_fallback", FALLBACK_1022, "FBR1022_0_quotient_certificate", "1022 fallback source rows"),
    ("SRC4814_07_581_chain", QVT_581, "QVT581_0_parent_projection", "581 quotient theorem chain"),
    ("SRC4814_08_637_qmap", QMAP_637, "QM637_2_vertical_kernel", "637 quotient map derivation"),
    ("SRC4814_09_637_obs", OBS_637, "matter", "637 observed functor/matter descent"),
    ("SRC4814_10_590_map", DVM_590, "DVM590_3_precise_map", "590 DCdagger vertical map"),
    ("SRC4814_11_670_sourcefree", SOURCEFREE_670, "PSF670_0_operator_form", "670 positive source-free chain"),
    ("SRC4814_12_runner", RUNNER, "def branch_decision_row", "4814 executable branch-choice runner"),
]


RUNNER_TEXT = r'''from __future__ import annotations

import csv
import math
import sys
from pathlib import Path
from typing import Any


BRANCH_CLAUSES = (
    "branch_separated_signed",
    "quotient_attempt_selected_signed",
    "scalar_demoted_to_fallback_signed",
    "source_residual_last_resort_signed",
    "no_route_mixing_signed",
    "no_GR_import_signed",
    "no_fit_to_bound_signed",
)

VERTICAL_CLAUSES = (
    "q_map_signed",
    "action_descent_signed",
    "matter_descent_signed",
    "vertical_generator_signed",
    "momentum_map_signed",
    "boundary_silence_signed",
    "degree_count_signed",
    "no_GR_import_signed",
    "no_fit_to_bound_signed",
)

SCALAR_CLAUSES = (
    "operator_self_adjoint_signed",
    "Z_positive_signed",
    "M2_positive_signed",
    "J_zero_signed",
    "boundary_flux_zero_signed",
    "energy_identity_signed",
    "no_GR_import_signed",
    "no_fit_to_bound_signed",
)

FALLBACK_TERMS = (
    "quotient_certificate_abs",
    "scalar_operator_abs",
    "sourced_alpha_abs",
    "edge_bound_abs",
    "total_guard_abs",
)

FORBIDDEN_SOURCE_TOKENS = (
    "GR_IMPORT",
    "FIT_TO_BOUND",
    "BOUND_AS_SOURCE",
    "ORBITAL_GM_AS_SOURCE",
    "POST_READOUT_QUOTIENT",
    "SCALAR_NOHAIR_AS_EDGE_EXACTNESS",
    "SOURCE_FREE_BY_ASSERTION",
    "CANCEL_UNKNOWN_COMPONENTS",
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
    text = " ".join(str(row.get(field, "")) for field in ("branch_id", "clause_id", "row_id", "source_path", "equation_ref", "notes", "provenance")).upper()
    return any(token in text for token in FORBIDDEN_SOURCE_TOKENS)


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


def branch_decision_row(row: dict[str, Any]) -> dict[str, Any]:
    return clause_row(row, "branch_id", "branch_status", "branch_theorem", "missing_branch_inputs", BRANCH_CLAUSES, "FAILED_BRANCH_CHOICE_GATE", "BLOCKED_MISSING_BRANCH_CHOICE_INPUTS", "BRANCH_CHOICE_SIGNED_NONCLAIM")


def vertical_clause_row(row: dict[str, Any]) -> dict[str, Any]:
    return clause_row(row, "clause_id", "vertical_status", "vertical_theorem", "missing_vertical_inputs", VERTICAL_CLAUSES, "FAILED_VERTICAL_QUOTIENT_GATE", "BLOCKED_MISSING_VERTICAL_QUOTIENT_INPUTS", "VERTICAL_QUOTIENT_SIGNED_CONDITIONAL_NONCLAIM")


def scalar_clause_row(row: dict[str, Any]) -> dict[str, Any]:
    return clause_row(row, "clause_id", "scalar_status", "scalar_theorem", "missing_scalar_inputs", SCALAR_CLAUSES, "FAILED_SCALAR_NOHAIR_GATE", "BLOCKED_MISSING_SCALAR_NOHAIR_INPUTS", "SCALAR_NOHAIR_SIGNED_CONDITIONAL_NONCLAIM")


def fallback_value(row: dict[str, Any]) -> tuple[float | None, list[str]]:
    values: list[float] = []
    missing: list[str] = []
    for term in FALLBACK_TERMS:
        value = parse_float(row.get(term))
        if value is None or value < 0.0:
            missing.append(f"MISSING_{term}")
        else:
            values.append(value)
    if missing:
        return None, missing
    return sum(values), []


def fallback_row(row: dict[str, Any]) -> dict[str, Any]:
    row_id = str(row.get("row_id", "")).strip() or "UNNAMED_FALLBACK"
    output: dict[str, Any] = {"row_id": row_id, "quantity": row.get("quantity", ""), "valid_for_claim": False, "claim_allowed": False}
    if forbidden_source_used(row):
        output.update({"fallback_abs": "MISSING_NUMERIC_VALUE", "required_abs_max": format_float(parse_float(row.get("required_abs_max"))), "numeric_window_pass": False, "fallback_status": "FAILED_FALLBACK_SOURCE_GATE", "missing_fallback_inputs": "FORBIDDEN_FALLBACK_SOURCE", "anti_circularity_status": "FAIL_FORBIDDEN_SOURCE_USED"})
        return output
    required = parse_float(row.get("required_abs_max"))
    value, missing = fallback_value(row)
    if required is None or required <= 0.0:
        missing.append("MISSING_required_abs_max")
    if missing_text(row.get("source_path")):
        missing.append("MISSING_source_path")
    if missing_text(row.get("equation_ref")):
        missing.append("MISSING_equation_ref")
    if not bool_text(row.get("source_signed")):
        missing.append("MISSING_source_signed")
    if required is None or required <= 0.0 or value is None:
        output.update({"fallback_abs": "MISSING_NUMERIC_VALUE", "required_abs_max": format_float(required), "numeric_window_pass": False, "fallback_status": "BLOCKED_MISSING_FALLBACK_SOURCE_INPUTS", "missing_fallback_inputs": ";".join(missing), "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED"})
        return output
    passes = value <= required
    status = "FALLBACK_SOURCE_NUMERIC_WINDOW_FAIL"
    if passes:
        status = "FALLBACK_SOURCE_NUMERIC_WINDOW_PASS_SOURCE_UNSIGNED_NONCLAIM"
        if bool_text(row.get("source_signed")) and bool_text(row.get("valid_for_claim")):
            status = "FALLBACK_SOURCE_NUMERIC_WINDOW_PASS_SOURCE_SIGNED_NONCLAIM"
    output.update({"fallback_abs": format_float(value), "required_abs_max": format_float(required), "numeric_window_pass": passes, "fallback_status": status, "missing_fallback_inputs": ";".join(missing), "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED"})
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
    if len(sys.argv) != 4 or sys.argv[1] not in {"branch", "vertical", "scalar", "fallback"}:
        print("Usage: vertical_quotient_scalar_branch_choice_runner.py branch|vertical|scalar|fallback INPUT_CSV OUTPUT_CSV", file=sys.stderr)
        return 2
    rows = read_csv(Path(sys.argv[2]))
    mode = sys.argv[1]
    if mode == "branch":
        outputs = [branch_decision_row(row) for row in rows]
    elif mode == "vertical":
        outputs = [vertical_clause_row(row) for row in rows]
    elif mode == "scalar":
        outputs = [scalar_clause_row(row) for row in rows]
    else:
        outputs = [fallback_row(row) for row in rows]
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
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(column, "")) for column in columns) + " |")
    return "\n".join(lines)


def target_row() -> dict[str, str]:
    rows = read_csv(TARGET_4813)
    if not rows:
        raise RuntimeError("missing 4813 target rows")
    return {"component_expr": "abs(branch_fallback_guard)", "required_abs_max": rows[0]["required_abs_max"], "source": str(TARGET_4813)}


def source_register(timestamp: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path, needle, role in SOURCE_SPECS:
        text = read_text(path)
        rows.append({"checkpoint": CHECKPOINT, "source_id": source_id, "source_path": str(path), "exists": path.exists(), "needle": needle, "needle_found": bool(text and needle in text), "role": role, "valid_for_claim": False, "timestamp_utc": timestamp})
    return rows


def bools(names: tuple[str, ...], signed: bool) -> dict[str, bool]:
    return {name: signed for name in names}


def missing_fallback_terms() -> dict[str, str]:
    return {term: "MISSING_PARENT_VALUE" for term in FALLBACK_TERMS}


def zero_fallback_terms() -> dict[str, str]:
    return {term: "0.0" for term in FALLBACK_TERMS}


def unit_fallback_terms() -> dict[str, str]:
    values = zero_fallback_terms()
    values["quotient_certificate_abs"] = "1.0"
    return values


def strict_fallback_terms() -> dict[str, str]:
    values = zero_fallback_terms()
    values["quotient_certificate_abs"] = "10.0"
    return values


def write_runner() -> None:
    SCRIPT_DIR.mkdir(parents=True, exist_ok=True)
    RUNNER.write_text(RUNNER_TEXT, encoding="utf-8")


def write_inputs(timestamp: str, target: dict[str, str]) -> None:
    required = target["required_abs_max"]
    write_csv(TARGET_AUDIT_CSV, [{"audit_id": "TGA4814_0_target_import", "component_expr": "abs(branch_fallback_guard)", "required_abs_max": required, "source": target["source"], "derivation": "same normalized local coupling window inherited from 4813 edge-fill target", "valid_for_claim": False, "timestamp_utc": timestamp}])
    branch_rows = [
        {"branch_id": "physical_branch_choice_missing", "route": "physical_missing", **bools(BRANCH_CLAUSES, False), "no_GR_import_signed": True, "no_fit_to_bound_signed": True, "source_path": "MISSING_PARENT_BRANCH_CHOICE", "equation_ref": "MISSING_BRANCH_EQUATION", "notes": "physical branch lacks complete branch separation and selected proof route certificate", "provenance": "4814 physical branch", "valid_for_claim": False},
        {"branch_id": "quotient_vertical_selected_nonclaim", "route": "selected_least_scrutiny", **bools(BRANCH_CLAUSES, True), "source_path": str(BRANCH_1022), "equation_ref": "BDM1022_5_verdict", "notes": "branch choice is signed as workflow selection only, not a physics theorem", "provenance": "1022 branch matrix", "valid_for_claim": False},
        {"branch_id": "forbidden_route_mixing_control", "route": "forbidden_control", **bools(BRANCH_CLAUSES, True), "source_path": "SCALAR_NOHAIR_AS_EDGE_EXACTNESS_SOURCE_FREE_BY_ASSERTION", "equation_ref": "FORBIDDEN_ROUTE_MIXING", "notes": "control row must fail if scalar no-hair is used as edge exactness", "provenance": "forbidden control", "valid_for_claim": False},
    ]
    vertical_rows = [
        {"clause_id": "physical_vertical_quotient_missing", "route": "physical_missing", **bools(VERTICAL_CLAUSES, False), "no_GR_import_signed": True, "no_fit_to_bound_signed": True, "source_path": "MISSING_PARENT_Q_VX_ACTION_DESCENT", "equation_ref": "MISSING_VERTICAL_CERTIFICATE", "notes": "physical branch lacks q map, action descent, matter descent, v_X, momentum map, boundary silence and degree count", "provenance": "4814 physical branch", "valid_for_claim": False},
        {"clause_id": "vertical_quotient_unsigned", "route": "least_scrutiny_theorem_route", **bools(VERTICAL_CLAUSES, False), "q_map_signed": False, "source_path": str(VERTICAL_1022), "equation_ref": "VQC1022_0_to_VQC1022_7", "notes": "vertical quotient theorem shape exists but is unsigned for current MTS", "provenance": "1022 vertical construction", "valid_for_claim": False},
        {"clause_id": "conditional_vertical_quotient", "route": "conditional_theorem", **bools(VERTICAL_CLAUSES, True), "source_path": str(POST / "1022-Y5-R10-vertical-quotient-LX-construction-or-scalar-nohair-branch-choice.md"), "equation_ref": "VQC1022 conditional theorem", "notes": "conditional branch only", "provenance": "1022 vertical clauses", "valid_for_claim": False},
        {"clause_id": "forbidden_post_readout_quotient", "route": "forbidden_control", **bools(VERTICAL_CLAUSES, True), "source_path": "POST_READOUT_QUOTIENT_ORBITAL_GM_AS_SOURCE", "equation_ref": "FORBIDDEN_QUOTIENT", "notes": "control row must fail if q is chosen after readout", "provenance": "forbidden control", "valid_for_claim": False},
    ]
    scalar_rows = [
        {"clause_id": "physical_scalar_nohair_missing", "route": "fallback_physical_missing", **bools(SCALAR_CLAUSES, False), "no_GR_import_signed": True, "no_fit_to_bound_signed": True, "source_path": "MISSING_PARENT_SCALAR_NOHAIR", "equation_ref": "MISSING_SCALAR_NOHAIR", "notes": "physical scalar branch lacks positive operator/source-zero/boundary flux inputs", "provenance": "4814 physical branch", "valid_for_claim": False},
        {"clause_id": "scalar_nohair_unsigned_fallback", "route": "fallback_if_quotient_fails", **bools(SCALAR_CLAUSES, False), "no_GR_import_signed": True, "no_fit_to_bound_signed": True, "source_path": str(SCALAR_1022), "equation_ref": "SNH1022_0_to_SNH1022_6", "notes": "scalar no-hair route is complete as a checklist but unsigned", "provenance": "1022 scalar no-hair", "valid_for_claim": False},
        {"clause_id": "conditional_scalar_nohair", "route": "conditional_theorem", **bools(SCALAR_CLAUSES, True), "source_path": str(SCALAR_1022), "equation_ref": "SNH1022 conditional theorem", "notes": "conditional branch only", "provenance": "1022 scalar construction", "valid_for_claim": False},
        {"clause_id": "forbidden_source_free_assertion", "route": "forbidden_control", **bools(SCALAR_CLAUSES, True), "source_path": "SOURCE_FREE_BY_ASSERTION_BOUND_AS_SOURCE", "equation_ref": "FORBIDDEN_SCALAR", "notes": "control row must fail if source-free is asserted", "provenance": "forbidden control", "valid_for_claim": False},
    ]
    fallback_rows = [
        {"row_id": "physical_fallback_missing", "quantity": "branch fallback no-cancellation guard", **missing_fallback_terms(), "required_abs_max": required, "source_signed": False, "source_path": "MISSING_PARENT_FALLBACK_SOURCE_ROWS", "equation_ref": "MISSING_FALLBACK_EQUATION", "notes": "physical fallback lacks quotient certificate, scalar operator, sourced alpha, edge bound and total guard terms", "provenance": "4814 physical branch", "valid_for_claim": False},
        {"row_id": "fallback_schema_missing", "quantity": "branch fallback no-cancellation guard", **missing_fallback_terms(), "required_abs_max": required, "source_signed": False, "source_path": str(FALLBACK_1022), "equation_ref": "FBR1022_0_to_FBR1022_4", "notes": "fallback schema exists but terms are missing", "provenance": "1022 fallback rows", "valid_for_claim": False},
        {"row_id": "unit_branch_fallback_smoke", "quantity": "branch fallback no-cancellation guard", **unit_fallback_terms(), "required_abs_max": required, "source_signed": False, "source_path": str(FALLBACK_1022), "equation_ref": "unit branch fallback smoke", "notes": "unit fallback term is below current target but remains nonclaim", "provenance": "4814 smoke row", "valid_for_claim": False},
        {"row_id": "strict_branch_fallback_fail", "quantity": "branch fallback no-cancellation guard", **strict_fallback_terms(), "required_abs_max": required, "source_signed": False, "source_path": str(FALLBACK_1022), "equation_ref": "strict fail control", "notes": "control row proves oversized branch fallback fails", "provenance": "4814 control", "valid_for_claim": False},
        {"row_id": "conditional_zero_fallback", "quantity": "branch fallback no-cancellation guard", **zero_fallback_terms(), "required_abs_max": required, "source_signed": True, "source_path": str(POST / "1022-Y5-R10-vertical-quotient-LX-construction-or-scalar-nohair-branch-choice.md"), "equation_ref": "conditional theorem zero", "notes": "conditional branch only", "provenance": "1022 conditional branch", "valid_for_claim": False},
        {"row_id": "forbidden_cancellation_fallback", "quantity": "branch fallback no-cancellation guard", **zero_fallback_terms(), "required_abs_max": required, "source_signed": True, "source_path": "CANCEL_UNKNOWN_COMPONENTS_BOUND_AS_SOURCE", "equation_ref": "FORBIDDEN_FALLBACK", "notes": "control row must fail if unknown components cancel", "provenance": "forbidden control", "valid_for_claim": False},
    ]
    write_csv(BRANCH_INPUT_CSV, branch_rows)
    write_csv(VERTICAL_INPUT_CSV, vertical_rows)
    write_csv(SCALAR_INPUT_CSV, scalar_rows)
    write_csv(FALLBACK_INPUT_CSV, fallback_rows)


def run_runner() -> None:
    subprocess.run([sys.executable, str(RUNNER), "branch", str(BRANCH_INPUT_CSV), str(BRANCH_OUTPUT_CSV)], check=True)
    subprocess.run([sys.executable, str(RUNNER), "vertical", str(VERTICAL_INPUT_CSV), str(VERTICAL_OUTPUT_CSV)], check=True)
    subprocess.run([sys.executable, str(RUNNER), "scalar", str(SCALAR_INPUT_CSV), str(SCALAR_OUTPUT_CSV)], check=True)
    subprocess.run([sys.executable, str(RUNNER), "fallback", str(FALLBACK_INPUT_CSV), str(FALLBACK_OUTPUT_CSV)], check=True)


def make_output_tables() -> dict[str, list[dict[str, Any]]]:
    branch = read_csv(BRANCH_OUTPUT_CSV)
    vertical = read_csv(VERTICAL_OUTPUT_CSV)
    scalar = read_csv(SCALAR_OUTPUT_CSV)
    fallback = read_csv(FALLBACK_OUTPUT_CSV)
    obstruction = [
        {"update_id": "OBS4814_0_branch", "item": "branch choice", "status": "QUOTIENT_VERTICAL_SELECTED_NONCLAIM", "value_or_bound": "attempt quotient/vertical before scalar/source scoring", "meaning": "least post-hoc route is now selected without claiming it"},
        {"update_id": "OBS4814_1_vertical", "item": "vertical quotient theorem route", "status": "BLOCKED_MISSING_VERTICAL_QUOTIENT_INPUTS", "value_or_bound": "q, Dq[v_X], action/matter descent, momentum map, boundary silence, degree count", "meaning": "no-pole/local silence not proved"},
        {"update_id": "OBS4814_2_scalar", "item": "scalar no-hair fallback", "status": "BLOCKED_MISSING_SCALAR_NOHAIR_INPUTS", "value_or_bound": "Z_X>0, M_X^2>0, J_X=0, boundary_flux=0", "meaning": "scalar branch remains fallback and coefficient-sensitive"},
        {"update_id": "OBS4814_3_fallback", "item": "branch fallback source rows", "status": "FALLBACK_SOURCE_NUMERIC_WINDOW_PASS_SOURCE_UNSIGNED_NONCLAIM", "value_or_bound": "1.000000000000000e+00 <= 5.256633029822351e+00", "meaning": "unit fallback row passes but physical source rows are missing"},
    ]
    gates = [
        {"gate_id": "PG4814_0_branch_choice", "claim": "Branch choice is written and route-mixing is firewalled", "gate_pass": True, "reason": "quotient/vertical selected first, scalar fallback separated", "evidence": str(BRANCH_OUTPUT_CSV)},
        {"gate_id": "PG4814_1_vertical_claim", "claim": "Quotient/vertical no-pole theorem is proved", "gate_pass": False, "reason": "q/v_X/action/matter/boundary/degree certificate is missing", "evidence": str(VERTICAL_OUTPUT_CSV)},
        {"gate_id": "PG4814_2_scalar_claim", "claim": "Scalar source-free no-hair theorem is proved", "gate_pass": False, "reason": "Z_X, M_X2, J_X=0 and boundary flux inputs are missing", "evidence": str(SCALAR_OUTPUT_CSV)},
        {"gate_id": "PG4814_3_source_residual", "claim": "Fallback source residual row is claim-ready", "gate_pass": False, "reason": "fallback row terms and source paths are missing", "evidence": str(FALLBACK_OUTPUT_CSV)},
        {"gate_id": "PG4814_4_local_GR", "claim": "Newton/local-GR source coupling promotion is allowed", "gate_pass": False, "reason": "no branch has theorem-zero or valid source-bound closure", "evidence": "nonclaim firewall active"},
    ]
    firewalls = [
        {"firewall_id": "FW4814_0_no_post_readout_quotient", "rule": "q and v_X must be parent-defined before equations/readout.", "status": "ACTIVE"},
        {"firewall_id": "FW4814_1_no_scalar_edge_mix", "rule": "Scalar no-hair cannot masquerade as Noether edge exactness.", "status": "ACTIVE"},
        {"firewall_id": "FW4814_2_no_source_free_assertion", "rule": "J_X=0 and boundary_flux=0 must be signed, not asserted.", "status": "ACTIVE"},
        {"firewall_id": "FW4814_3_no_unknown_cancellation", "rule": "Fallback residuals are absolute no-cancellation rows until theorem-zero closes.", "status": "ACTIVE"},
    ]
    decisions = [
        {"decision_id": "DEC4814_0_branch_choice", "decision": "attempt_quotient_vertical_construction_first", "reason": "it can remove X before variation and avoids coefficient tuning", "next_action": NEXT_TARGET},
        {"decision_id": "DEC4814_1_no_scalar_mixing", "decision": "scalar_nohair_remains_separate_fallback", "reason": "scalar no-hair kills a physical scalar only with positive/source-free data and is not edge exactness", "next_action": "use scalar only if quotient certificate fails"},
        {"decision_id": "DEC4814_2_empirical_fallback", "decision": "score_residuals_if_theorem_routes_fail", "reason": "nonzero coupling/source terms must become alpha/lambda and R11 source rows", "next_action": "fill fallback source packs with units and source paths"},
        {"decision_id": "DEC4814_3_next", "decision": "q_vX_action_descent_certificate_is_next", "reason": "this is the first certificate that can genuinely remove local X before variation", "next_action": NEXT_TARGET},
    ]
    status = [
        {"status_id": "STATUS4814_0_branch", "status": "QUOTIENT_VERTICAL_SELECTED_NONCLAIM", "detail": "least-scrutiny route selected without physics claim"},
        {"status_id": "STATUS4814_1_vertical", "status": "VERTICAL_QUOTIENT_NOT_PROVED", "detail": "q/v_X/action/matter/boundary/degree certificate missing"},
        {"status_id": "STATUS4814_2_scalar", "status": "SCALAR_NOHAIR_FALLBACK_NOT_PROVED", "detail": "positive/source-free inputs missing"},
        {"status_id": "STATUS4814_3_next", "status": "Q_VX_ACTION_DESCENT_CERTIFICATE_OR_SCALAR_DEMOTION", "detail": NEXT_TARGET},
    ]
    next_rows = [{"route_id": "NEXT4814_0_primary", "next_target": NEXT_TARGET, "script": "scripts/Y5_R2FR_4815_q_vX_action_descent_certificate_or_scalar_nohair_demotion.py", "objective": "build q/v_X/action/matter/boundary/degree certificate; if it fails, demote to scalar no-hair/source-coefficient route", "selection_status": "selected", "success_condition": "single quotient/vertical certificate closes or scalar branch is explicitly demoted with source rows"}]
    write_csv(OBSTRUCTION_UPDATE_CSV, obstruction)
    write_csv(GATE_CSV, gates)
    write_csv(FIREWALL_CSV, firewalls)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, status)
    write_csv(NEXT_TARGET_CSV, next_rows)
    return {"branch": branch, "vertical": vertical, "scalar": scalar, "fallback": fallback, "obstruction": obstruction, "gates": gates, "firewalls": firewalls, "decisions": decisions, "status": status, "next": next_rows}


def validate() -> list[dict[str, Any]]:
    sources = read_csv(SOURCE_REGISTER_CSV)
    branch = {row["branch_id"]: row for row in read_csv(BRANCH_OUTPUT_CSV)}
    vertical = {row["clause_id"]: row for row in read_csv(VERTICAL_OUTPUT_CSV)}
    scalar = {row["clause_id"]: row for row in read_csv(SCALAR_OUTPUT_CSV)}
    fallback = {row["row_id"]: row for row in read_csv(FALLBACK_OUTPUT_CSV)}
    source_pass = all(row["exists"] == "True" and row["needle_found"] == "True" for row in sources)
    checks = [
        {"check_id": "VAL4814_0_sources", "description": "all cited sources exist and needles are found", "result": "PASS" if source_pass else "FAIL", "evidence": str(SOURCE_REGISTER_CSV)},
        {"check_id": "VAL4814_1_branch_selected", "description": "quotient/vertical branch is selected as nonclaim workflow route", "result": "PASS" if branch["quotient_vertical_selected_nonclaim"]["branch_status"] == "BRANCH_CHOICE_SIGNED_NONCLAIM" else "FAIL", "evidence": str(BRANCH_OUTPUT_CSV)},
        {"check_id": "VAL4814_2_forbidden_branch_fails", "description": "forbidden route-mixing control fails", "result": "PASS" if branch["forbidden_route_mixing_control"]["anti_circularity_status"] == "FAIL_FORBIDDEN_SOURCE_USED" else "FAIL", "evidence": str(BRANCH_OUTPUT_CSV)},
        {"check_id": "VAL4814_3_vertical_blocks", "description": "physical vertical quotient row remains blocked", "result": "PASS" if vertical["physical_vertical_quotient_missing"]["vertical_status"] == "BLOCKED_MISSING_VERTICAL_QUOTIENT_INPUTS" else "FAIL", "evidence": str(VERTICAL_OUTPUT_CSV)},
        {"check_id": "VAL4814_4_forbidden_vertical_fails", "description": "forbidden post-readout quotient control fails", "result": "PASS" if vertical["forbidden_post_readout_quotient"]["anti_circularity_status"] == "FAIL_FORBIDDEN_SOURCE_USED" else "FAIL", "evidence": str(VERTICAL_OUTPUT_CSV)},
        {"check_id": "VAL4814_5_scalar_blocks", "description": "physical scalar no-hair row remains blocked", "result": "PASS" if scalar["physical_scalar_nohair_missing"]["scalar_status"] == "BLOCKED_MISSING_SCALAR_NOHAIR_INPUTS" else "FAIL", "evidence": str(SCALAR_OUTPUT_CSV)},
        {"check_id": "VAL4814_6_forbidden_scalar_fails", "description": "forbidden source-free assertion control fails", "result": "PASS" if scalar["forbidden_source_free_assertion"]["anti_circularity_status"] == "FAIL_FORBIDDEN_SOURCE_USED" else "FAIL", "evidence": str(SCALAR_OUTPUT_CSV)},
        {"check_id": "VAL4814_7_fallback_blocks", "description": "physical fallback source row remains blocked", "result": "PASS" if fallback["physical_fallback_missing"]["fallback_status"] == "BLOCKED_MISSING_FALLBACK_SOURCE_INPUTS" else "FAIL", "evidence": str(FALLBACK_OUTPUT_CSV)},
        {"check_id": "VAL4814_8_unit_fallback_passes", "description": "unit fallback smoke row passes target window", "result": "PASS" if fallback["unit_branch_fallback_smoke"]["numeric_window_pass"] == "True" else "FAIL", "evidence": str(FALLBACK_OUTPUT_CSV)},
        {"check_id": "VAL4814_9_strict_fail", "description": "strict fallback control fails numeric target", "result": "PASS" if fallback["strict_branch_fallback_fail"]["numeric_window_pass"] == "False" and fallback["strict_branch_fallback_fail"]["fallback_status"] == "FALLBACK_SOURCE_NUMERIC_WINDOW_FAIL" else "FAIL", "evidence": str(FALLBACK_OUTPUT_CSV)},
        {"check_id": "VAL4814_10_forbidden_fallback_fails", "description": "forbidden unknown-cancellation fallback control fails", "result": "PASS" if fallback["forbidden_cancellation_fallback"]["anti_circularity_status"] == "FAIL_FORBIDDEN_SOURCE_USED" else "FAIL", "evidence": str(FALLBACK_OUTPUT_CSV)},
        {"check_id": "VAL4814_11_claim", "description": "claim register includes L-656 as nonclaim", "result": "PASS" if CLAIM_ID in read_text(CLAIMS_PATH) and DECISION in read_text(CLAIMS_PATH) else "FAIL", "evidence": str(CLAIMS_PATH)},
        {"check_id": "VAL4814_12_resume", "description": "resume points at 4815", "result": "PASS" if NEXT_TARGET in read_text(RESUME_PATH) else "FAIL", "evidence": str(RESUME_PATH)},
    ]
    checks.append({"check_id": "VAL4814_OVERALL", "description": "all 4814 branch-choice checks pass", "result": "PASS" if all(row["result"] == "PASS" for row in checks) else "FAIL", "evidence": DECISION})
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
    row = {"claim_id": CLAIM_ID, "domain": "local_gr", "claim": "vertical_quotient_scalar_branch_choice_runner", "current_evidence": "4814 selects the quotient/vertical L_X construction as the next least-scrutiny route, keeps scalar no-hair as a separate fallback, and stages no-cancellation fallback rows.", "status": "vertical_quotient_branch_choice_private_nonclaim", "next_test": NEXT_TARGET, "key_risk": "post-readout quotient; scalar no-hair as edge exactness; source-free by assertion; unknown cancellation", "sector": "local_gr", "evidence": str(DOC_PATH), "next_action": NEXT_TARGET, "risk": "missing q/v_X/action/matter/boundary/degree certificate; scalar coefficients missing; residual source rows missing", "title": "Vertical quotient L_X construction or scalar no-hair branch-choice gate", "notes": f"{MARKER}; {DECISION}; generated {timestamp}"}
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        csv.DictWriter(handle, fieldnames=list(row)).writerow(row)


def update_registers(timestamp: str) -> None:
    append_claim(timestamp)
    append_once(SPINE_PATH, MARKER, f"""

## {MARKER}

4814 selects the next local-GR route:

```text
q: Conf_parent -> Q_obs = Conf_parent / N_X
Dq[v_X] = 0
S_parent[Phi] = S_red[q(Phi)] + fixed boundary/topological terms
S_matter = Sbar_m[Obs(q(Phi)), psi, theta_A]
```

The quotient/vertical construction is preferred because it can remove the local `X` pole before variation. Scalar positive no-hair remains a separate fallback requiring `Z_X>0`, `M_X^2>0`, `J_X=0`, and boundary-flux zero; it is not allowed to masquerade as edge exactness.
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
Last checkpoint: `4814-Y5-R2FR-vertical-quotient-LX-construction-or-scalar-nohair-branch-choice.md`
Marker: `{MARKER}`

## Where we are

4814 selected the quotient/vertical route first:

```text
q: Conf_parent -> Q_obs = Conf_parent / N_X
Dq[v_X] = 0
S_parent[Phi] = S_red[q(Phi)] + fixed boundary/topological terms
S_matter = Sbar_m[Obs(q(Phi)), psi, theta_A]
```

## Live blockers

- The actual `q`, `v_X`, action descent, matter descent, boundary silence, and degree count certificate is still missing.
- Scalar no-hair remains fallback and requires its own positive/source-free proof.
- If both theorem routes fail, residuals must be scored with source-backed no-cancellation rows.

## Next target

`{NEXT_TARGET}`
""", encoding="utf-8")


def write_docs(timestamp: str, target: dict[str, str], outputs: dict[str, list[dict[str, Any]]], validation: list[dict[str, Any]]) -> None:
    sources = read_csv(SOURCE_REGISTER_CSV)
    target_rows = read_csv(TARGET_AUDIT_CSV)
    doc = f"""# 4814 - Vertical quotient L_X construction or scalar no-hair branch choice

Marker: `{MARKER}`
Generated: `{timestamp}`
Decision: `{DECISION}`

## Result

4814 makes the branch choice explicit:

```text
q: Conf_parent -> Q_obs = Conf_parent / N_X
Dq[v_X] = 0
S_parent[Phi] = S_red[q(Phi)] + fixed boundary/topological terms
S_matter = Sbar_m[Obs(q(Phi)), psi, theta_A]
required fallback guard <= {target['required_abs_max']}
```

The quotient/vertical route is selected as the least post-hoc next attempt because it can remove `X` before variation. Scalar no-hair remains a separate fallback, not an edge-exactness proof.

## Target Audit

{table(target_rows, ['audit_id', 'component_expr', 'required_abs_max', 'source', 'derivation', 'valid_for_claim', 'timestamp_utc'])}

## Source Register

{table(sources, ['source_id', 'source_path', 'exists', 'needle_found', 'role'])}

## Branch Decision Output

{table(outputs['branch'], ['branch_id', 'route', 'branch_status', 'branch_theorem', 'missing_branch_inputs', 'anti_circularity_status'])}

## Vertical Quotient Output

{table(outputs['vertical'], ['clause_id', 'route', 'vertical_status', 'vertical_theorem', 'missing_vertical_inputs', 'anti_circularity_status'])}

## Scalar No-Hair Output

{table(outputs['scalar'], ['clause_id', 'route', 'scalar_status', 'scalar_theorem', 'missing_scalar_inputs', 'anti_circularity_status'])}

## Fallback Source Output

{table(outputs['fallback'], ['row_id', 'quantity', 'fallback_abs', 'required_abs_max', 'numeric_window_pass', 'fallback_status', 'missing_fallback_inputs', 'anti_circularity_status'])}

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
    FORMAL_PATH.write_text(f"""# 830 - PPC4161 vertical quotient L_X construction or scalar no-hair branch choice

Marker: `{MARKER}`
Generated: `{timestamp}`

4814 selects the quotient/vertical route first:

```text
q: Conf_parent -> Q_obs = Conf_parent / N_X
Dq[v_X] = 0
S_parent[Phi] = S_red[q(Phi)] + fixed boundary/topological terms
```

This is nonclaim route selection, not a proof. Scalar no-hair remains fallback and source residual scoring remains last resort. Next target: `{NEXT_TARGET}`.
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
