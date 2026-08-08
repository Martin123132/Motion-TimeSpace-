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

CHECKPOINT = "4811"
CLAIM_ID = "L-653"
MARKER = "PPC4161_BOUNDARY_EXACTNESS_PROJECTOR_ORTHOGONALITY_OR_SOURCE_PACK_4811"
PACKET_MARKER = "PPC4161_PACKET_BOUNDARY_EXACTNESS_PROJECTOR_ORTHOGONALITY_OR_SOURCE_PACK_4811"
DECISION = "BOUNDARY_EXACTNESS_PROJECTOR_ORTHOGONALITY_AND_SOURCE_PACK_GATE_NONCLAIM"
NEXT_TARGET = "4812-Y5-R2FR-boundary-cohomology-domain-certificate-or-source-pack-first-row.md"

DOC_PATH = POST / "4811-Y5-R2FR-boundary-exactness-projector-orthogonality-or-source-pack.md"
FORMAL_PATH = FORMAL / "827-PPC4161-boundary-exactness-projector-orthogonality-or-source-pack.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"
RUNNER = SCRIPT_DIR / "boundary_exactness_projector_source_pack_runner.py"

SOURCE_REGISTER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4811_SOURCE_REGISTER.csv"
EXACTNESS_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4811_BOUNDARY_EXACTNESS_INPUT.csv"
EXACTNESS_OUTPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4811_BOUNDARY_EXACTNESS_OUTPUT.csv"
PROJECTOR_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4811_PROJECTOR_ORTHOGONALITY_INPUT.csv"
PROJECTOR_OUTPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4811_PROJECTOR_ORTHOGONALITY_OUTPUT.csv"
SOURCE_PACK_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4811_SOURCE_PACK_INPUT.csv"
SOURCE_PACK_OUTPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4811_SOURCE_PACK_OUTPUT.csv"
TARGET_AUDIT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4811_TARGET_AUDIT.csv"
OBSTRUCTION_UPDATE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4811_OBSTRUCTION_UPDATE.csv"
GATE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4811_PROMOTION_GATES.csv"
FIREWALL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4811_FIREWALL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4811_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4811_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4811_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4811_VALIDATION.csv"

TARGET_4810 = SOURCE_DIR / "P8_Y5_R2FR_4810_TARGET_AUDIT.csv"
BOUNDARY_671 = SOURCE_DIR / "P8_Y5_R10_671_BOUNDARY_CHARGE_OWNER_GATE.csv"
EDGE_671 = SOURCE_DIR / "P8_Y5_R10_671_EDGE_RESIDUAL_VECTOR.csv"
EXACT_672 = SOURCE_DIR / "P8_Y5_R10_672_BOUNDARY_EXACTNESS_ATTEMPT.csv"
PROJECTOR_672 = SOURCE_DIR / "P8_Y5_R10_672_PROJECTOR_ORTHOGONALITY_ATTEMPT.csv"
ZERO_DECISION_672 = SOURCE_DIR / "P8_Y5_R10_672_ZERO_OR_SOURCE_DECISION.csv"

EXACTNESS_CLAUSES = (
    "boundary_domain_signed",
    "BX_exact_signed",
    "Stokes_kernel_silent_signed",
    "proper_gauge_signed",
    "counterterm_signed",
    "cocycle_zero_signed",
    "no_GR_import_signed",
    "no_fit_to_bound_signed",
)

PROJECTOR_CLAUSES = (
    "PiM_definition_signed",
    "edge_mass_independence_signed",
    "symplectic_block_signed",
    "reference_silence_signed",
    "tau_frame_lock_signed",
    "source_measure_lock_signed",
    "no_GR_import_signed",
    "no_fit_to_bound_signed",
)

SOURCE_COMPONENTS = (
    "FB5540_abs",
    "bulk_X_abs",
    "edge_X_abs",
    "R11_abs",
    "projector_edge_abs",
)

SOURCE_SPECS = [
    ("SRC4811_00_4810_doc", POST / "4810-Y5-R2FR-sector-Lagrangian-boundary-owner-or-FB5540-source-row.md", "boundary_exactness_projector_orthogonality_or_source_pack", "4810 selects boundary exactness/projector fork"),
    ("SRC4811_01_4810_target", TARGET_4810, "TGA4810_0_target_import", "4810 inherited target audit"),
    ("SRC4811_02_1019_doc", POST / "1019-Y5-R10-boundary-exactness-projector-orthogonality-or-source-pack.md", "BE1019_0_domain", "1019 boundary/projector precedent"),
    ("SRC4811_03_671_boundary", BOUNDARY_671, "BCG671_4_projector_orthogonality", "671 boundary charge owner gate"),
    ("SRC4811_04_671_edge", EDGE_671, "ERV671_2_Qbar_edge_XH", "671 edge residual vector"),
    ("SRC4811_05_672_exact", EXACT_672, "BE672_1_BX_exact_form", "672 boundary exactness attempt"),
    ("SRC4811_06_672_projector", PROJECTOR_672, "PO672_3_mass_channel_projection", "672 projector orthogonality attempt"),
    ("SRC4811_07_672_decision", ZERO_DECISION_672, "source", "672 zero-or-source decision"),
    ("SRC4811_08_runner", RUNNER, "def exactness_row", "4811 executable boundary/projector runner"),
]


RUNNER_TEXT = r'''from __future__ import annotations

import csv
import math
import sys
from pathlib import Path
from typing import Any


EXACTNESS_CLAUSES = (
    "boundary_domain_signed",
    "BX_exact_signed",
    "Stokes_kernel_silent_signed",
    "proper_gauge_signed",
    "counterterm_signed",
    "cocycle_zero_signed",
    "no_GR_import_signed",
    "no_fit_to_bound_signed",
)

PROJECTOR_CLAUSES = (
    "PiM_definition_signed",
    "edge_mass_independence_signed",
    "symplectic_block_signed",
    "reference_silence_signed",
    "tau_frame_lock_signed",
    "source_measure_lock_signed",
    "no_GR_import_signed",
    "no_fit_to_bound_signed",
)

SOURCE_COMPONENTS = (
    "FB5540_abs",
    "bulk_X_abs",
    "edge_X_abs",
    "R11_abs",
    "projector_edge_abs",
)

FORBIDDEN_SOURCE_TOKENS = (
    "GR_IMPORT",
    "FIT_TO_BOUND",
    "BOUND_AS_SOURCE",
    "ORBITAL_GM_AS_SOURCE",
    "REFERENCE_ONLY_ZERO",
    "SYMBOLIC_EDGE_ZERO",
    "CANCEL_UNKNOWN_COMPONENTS",
    "DELETE_EDGE_BY_DOMAIN_FIAT",
    "POST_READOUT_PROJECTOR",
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
        for field in ("clause_id", "projector_id", "pack_id", "source_path", "equation_ref", "notes", "provenance")
    ).upper()
    return any(token in source_text for token in FORBIDDEN_SOURCE_TOKENS)


def missing_clauses(row: dict[str, Any], clauses: tuple[str, ...]) -> list[str]:
    return [clause for clause in clauses if not bool_text(row.get(clause))]


def source_guard(row: dict[str, Any]) -> tuple[float | None, list[str]]:
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


def exactness_row(row: dict[str, Any]) -> dict[str, Any]:
    clause_id = str(row.get("clause_id", "")).strip() or "UNNAMED_EXACTNESS"
    output: dict[str, Any] = {"clause_id": clause_id, "route": row.get("route", ""), "valid_for_claim": False, "claim_allowed": False}
    if forbidden_source_used(row):
        output.update({"exactness_status": "FAILED_EXACTNESS_GATE", "exactness_theorem": False, "missing_exactness_inputs": "FORBIDDEN_EXACTNESS_SOURCE", "anti_circularity_status": "FAIL_FORBIDDEN_SOURCE_USED"})
        return output
    missing = missing_clauses(row, EXACTNESS_CLAUSES)
    status = "BOUNDARY_EXACTNESS_SIGNED_CONDITIONAL_NONCLAIM" if not missing else "BLOCKED_MISSING_BOUNDARY_EXACTNESS_INPUTS"
    output.update({"exactness_status": status, "exactness_theorem": not missing, "missing_exactness_inputs": ";".join(missing), "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED"})
    return output


def projector_row(row: dict[str, Any]) -> dict[str, Any]:
    projector_id = str(row.get("projector_id", "")).strip() or "UNNAMED_PROJECTOR"
    output: dict[str, Any] = {"projector_id": projector_id, "route": row.get("route", ""), "valid_for_claim": False, "claim_allowed": False}
    if forbidden_source_used(row):
        output.update({"projector_status": "FAILED_PROJECTOR_GATE", "projector_theorem": False, "missing_projector_inputs": "FORBIDDEN_PROJECTOR_SOURCE", "anti_circularity_status": "FAIL_FORBIDDEN_SOURCE_USED"})
        return output
    missing = missing_clauses(row, PROJECTOR_CLAUSES)
    status = "PROJECTOR_ORTHOGONALITY_SIGNED_CONDITIONAL_NONCLAIM" if not missing else "BLOCKED_MISSING_PROJECTOR_INPUTS"
    output.update({"projector_status": status, "projector_theorem": not missing, "missing_projector_inputs": ";".join(missing), "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED"})
    return output


def source_pack_row(row: dict[str, Any]) -> dict[str, Any]:
    pack_id = str(row.get("pack_id", "")).strip() or "UNNAMED_SOURCE_PACK"
    output: dict[str, Any] = {"pack_id": pack_id, "component_expr": row.get("component_expr", ""), "valid_for_claim": False, "claim_allowed": False}
    if forbidden_source_used(row):
        output.update({"source_pack_guard_abs": "MISSING_NUMERIC_VALUE", "required_abs_max": format_float(parse_float(row.get("required_abs_max"))), "numeric_window_pass": False, "source_pack_status": "FAILED_SOURCE_PACK_GATE", "missing_source_pack_inputs": "FORBIDDEN_SOURCE_PACK", "anti_circularity_status": "FAIL_FORBIDDEN_SOURCE_USED"})
        return output
    required = parse_float(row.get("required_abs_max"))
    direct_value = parse_float(row.get("source_pack_guard_abs"))
    computed_value, computed_missing = source_guard(row)
    value = direct_value if direct_value is not None else computed_value
    missing: list[str] = []
    if required is None or required <= 0.0:
        missing.append("MISSING_required_abs_max")
    if value is None:
        missing.extend(computed_missing or ["MISSING_source_pack_guard_abs"])
    if missing_text(row.get("source_path")):
        missing.append("MISSING_source_path")
    if missing_text(row.get("equation_ref")):
        missing.append("MISSING_equation_ref")
    if not bool_text(row.get("source_signed")):
        missing.append("MISSING_source_signed")
    if required is None or required <= 0.0 or value is None:
        output.update({"source_pack_guard_abs": "MISSING_NUMERIC_VALUE", "required_abs_max": format_float(required), "numeric_window_pass": False, "source_pack_status": "BLOCKED_MISSING_SOURCE_PACK_INPUTS", "missing_source_pack_inputs": ";".join(missing), "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED"})
        return output
    passes = value <= required
    status = "SOURCE_PACK_NUMERIC_WINDOW_FAIL"
    if passes:
        status = "SOURCE_PACK_NUMERIC_WINDOW_PASS_SOURCE_UNSIGNED_NONCLAIM"
        if bool_text(row.get("source_signed")) and bool_text(row.get("valid_for_claim")):
            status = "SOURCE_PACK_NUMERIC_WINDOW_PASS_SOURCE_SIGNED_NONCLAIM"
    output.update({"source_pack_guard_abs": format_float(value), "required_abs_max": format_float(required), "numeric_window_pass": passes, "source_pack_status": status, "missing_source_pack_inputs": ";".join(missing), "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED"})
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
    if len(sys.argv) != 4 or sys.argv[1] not in {"exactness", "projector", "source"}:
        print("Usage: boundary_exactness_projector_source_pack_runner.py exactness|projector|source INPUT_CSV OUTPUT_CSV", file=sys.stderr)
        return 2
    rows = read_csv(Path(sys.argv[2]))
    mode = sys.argv[1]
    if mode == "exactness":
        outputs = [exactness_row(row) for row in rows]
    elif mode == "projector":
        outputs = [projector_row(row) for row in rows]
    else:
        outputs = [source_pack_row(row) for row in rows]
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
    rows = read_csv(TARGET_4810)
    if not rows:
        raise RuntimeError("missing 4810 target rows")
    return {"component_expr": "abs(source_pack_guard)", "required_abs_max": rows[0]["required_abs_max"], "source": str(TARGET_4810)}


def source_register(timestamp: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path, needle, role in SOURCE_SPECS:
        text = read_text(path)
        rows.append({"checkpoint": CHECKPOINT, "source_id": source_id, "source_path": str(path), "exists": path.exists(), "needle": needle, "needle_found": bool(text and needle in text), "role": role, "valid_for_claim": False, "timestamp_utc": timestamp})
    return rows


def bools(names: tuple[str, ...], signed: bool) -> dict[str, bool]:
    return {name: signed for name in names}


def zero_components() -> dict[str, str]:
    return {component: "0.0" for component in SOURCE_COMPONENTS}


def missing_components() -> dict[str, str]:
    return {component: "MISSING_PARENT_VALUE" for component in SOURCE_COMPONENTS}


def unit_components() -> dict[str, str]:
    values = zero_components()
    values["edge_X_abs"] = "1.0"
    return values


def strict_components() -> dict[str, str]:
    values = zero_components()
    values["edge_X_abs"] = "10.0"
    return values


def write_runner() -> None:
    SCRIPT_DIR.mkdir(parents=True, exist_ok=True)
    RUNNER.write_text(RUNNER_TEXT, encoding="utf-8")


def write_inputs(timestamp: str, target: dict[str, str]) -> None:
    required = target["required_abs_max"]
    write_csv(TARGET_AUDIT_CSV, [{"audit_id": "TGA4811_0_target_import", "component_expr": "abs(source_pack_guard)", "required_abs_max": required, "source": target["source"], "derivation": "same normalized local coupling window inherited from 4810 sector-owner target", "valid_for_claim": False, "timestamp_utc": timestamp}])
    exact_rows = [
        {"clause_id": "physical_exactness_missing", "route": "physical_missing", **bools(EXACTNESS_CLAUSES, False), "no_GR_import_signed": True, "no_fit_to_bound_signed": True, "source_path": "MISSING_PARENT_BOUNDARY_EXACTNESS", "equation_ref": "MISSING_BOUNDARY_EXACTNESS_EQUATION", "notes": "physical branch lacks certified boundary domain, B_X primitive, Stokes kernel silence, counterterm and cocycle zero", "provenance": "4811 physical branch", "valid_for_claim": False},
        {"clause_id": "boundary_exactness_unsigned", "route": "Q_edge_zero_by_exact_boundary_form", **bools(EXACTNESS_CLAUSES, False), "no_GR_import_signed": True, "no_fit_to_bound_signed": True, "source_path": str(EXACT_672), "equation_ref": "BE672_0_to_BE672_6", "notes": "exactness route is written but unsigned for current MTS", "provenance": "672 exactness attempt", "valid_for_claim": False},
        {"clause_id": "conditional_boundary_exactness", "route": "conditional_theorem", **bools(EXACTNESS_CLAUSES, True), "source_path": str(POST / "1019-Y5-R10-boundary-exactness-projector-orthogonality-or-source-pack.md"), "equation_ref": "BE1019_0_to_BE1019_6", "notes": "conditional theorem shape only", "provenance": "1019 exactness clauses", "valid_for_claim": False},
        {"clause_id": "forbidden_symbolic_edge_zero", "route": "forbidden_control", **bools(EXACTNESS_CLAUSES, True), "source_path": "SYMBOLIC_EDGE_ZERO_DELETE_EDGE_BY_DOMAIN_FIAT", "equation_ref": "FORBIDDEN_EDGE_ZERO", "notes": "control row must fail if edge charge is deleted by domain fiat", "provenance": "forbidden control", "valid_for_claim": False},
    ]
    projector_rows = [
        {"projector_id": "physical_projector_missing", "route": "physical_missing", **bools(PROJECTOR_CLAUSES, False), "no_GR_import_signed": True, "no_fit_to_bound_signed": True, "source_path": "MISSING_PARENT_PROJECTOR_ORTHOGONALITY", "equation_ref": "MISSING_PROJECTOR_EQUATION", "notes": "physical branch lacks Pi_M definition, mass independence, symplectic block, reference silence and source-measure lock", "provenance": "4811 physical branch", "valid_for_claim": False},
        {"projector_id": "projector_orthogonality_unsigned", "route": "Qbar_edge_XH_zero_by_projector", **bools(PROJECTOR_CLAUSES, False), "no_GR_import_signed": True, "no_fit_to_bound_signed": True, "source_path": str(PROJECTOR_672), "equation_ref": "PO672_0_to_PO672_6", "notes": "projector route is written but unsigned for current MTS", "provenance": "672 projector attempt", "valid_for_claim": False},
        {"projector_id": "conditional_projector_orthogonality", "route": "conditional_theorem", **bools(PROJECTOR_CLAUSES, True), "source_path": str(POST / "1019-Y5-R10-boundary-exactness-projector-orthogonality-or-source-pack.md"), "equation_ref": "PO1019_0_to_PO1019_5", "notes": "conditional theorem shape only", "provenance": "1019 projector clauses", "valid_for_claim": False},
        {"projector_id": "forbidden_post_readout_projector", "route": "forbidden_control", **bools(PROJECTOR_CLAUSES, True), "source_path": "POST_READOUT_PROJECTOR_ORBITAL_GM_AS_SOURCE", "equation_ref": "FORBIDDEN_PROJECTOR_FIT", "notes": "control row must fail if Pi_M is chosen after orbital readout", "provenance": "forbidden control", "valid_for_claim": False},
    ]
    pack_rows = [
        {"pack_id": "physical_source_pack_missing", "component_expr": "abs(source_pack_guard)", "source_pack_guard_abs": "MISSING_PARENT_VALUE", **missing_components(), "M_H_ref_abs": "MISSING_PARENT_VALUE", "required_abs_max": required, "source_signed": False, "source_path": "MISSING_PARENT_SOURCE_PACK", "equation_ref": "MISSING_SOURCE_PACK_EQUATION", "notes": "physical pack lacks M_H_ref, FB5540, bulk, edge, R11 and projector-edge source rows", "provenance": "4811 physical branch", "valid_for_claim": False},
        {"pack_id": "theorem_zero_candidate_unsigned", "component_expr": "abs(source_pack_guard)", "source_pack_guard_abs": "", **zero_components(), "M_H_ref_abs": "1.0", "required_abs_max": required, "source_signed": False, "source_path": str(POST / "1019-Y5-R10-boundary-exactness-projector-orthogonality-or-source-pack.md"), "equation_ref": "RVT1019_4_verdict", "notes": "zero candidate remains source unsigned", "provenance": "1019 route verdict", "valid_for_claim": False},
        {"pack_id": "unit_edge_source_pack_smoke", "component_expr": "abs(source_pack_guard)", "source_pack_guard_abs": "", **unit_components(), "M_H_ref_abs": "1.0", "required_abs_max": required, "source_signed": False, "source_path": str(EDGE_671), "equation_ref": "unit edge_X smoke", "notes": "unit edge residual is below current target but remains nonclaim", "provenance": "671 edge vector", "valid_for_claim": False},
        {"pack_id": "strict_source_pack_fail_control", "component_expr": "abs(source_pack_guard)", "source_pack_guard_abs": "", **strict_components(), "M_H_ref_abs": "1.0", "required_abs_max": required, "source_signed": False, "source_path": str(EDGE_671), "equation_ref": "strict fail control", "notes": "control row proves the source pack rejects oversized residuals", "provenance": "4811 control", "valid_for_claim": False},
        {"pack_id": "conditional_theorem_pack_zero", "component_expr": "abs(source_pack_guard)", "source_pack_guard_abs": "", **zero_components(), "M_H_ref_abs": "1.0", "required_abs_max": required, "source_signed": True, "source_path": str(POST / "1019-Y5-R10-boundary-exactness-projector-orthogonality-or-source-pack.md"), "equation_ref": "conditional theorem pack", "notes": "conditional branch only", "provenance": "4811 conditional branch", "valid_for_claim": False},
        {"pack_id": "forbidden_unknown_cancellation_pack", "component_expr": "abs(source_pack_guard)", "source_pack_guard_abs": "0.0", **zero_components(), "M_H_ref_abs": "1.0", "required_abs_max": required, "source_signed": True, "source_path": "CANCEL_UNKNOWN_COMPONENTS_BOUND_AS_SOURCE", "equation_ref": "FORBIDDEN_SOURCE_PACK", "notes": "control row must fail if unknown components cancel or bound supplies the value", "provenance": "forbidden control", "valid_for_claim": False},
    ]
    write_csv(EXACTNESS_INPUT_CSV, exact_rows)
    write_csv(PROJECTOR_INPUT_CSV, projector_rows)
    write_csv(SOURCE_PACK_INPUT_CSV, pack_rows)


def run_runner() -> None:
    subprocess.run([sys.executable, str(RUNNER), "exactness", str(EXACTNESS_INPUT_CSV), str(EXACTNESS_OUTPUT_CSV)], check=True)
    subprocess.run([sys.executable, str(RUNNER), "projector", str(PROJECTOR_INPUT_CSV), str(PROJECTOR_OUTPUT_CSV)], check=True)
    subprocess.run([sys.executable, str(RUNNER), "source", str(SOURCE_PACK_INPUT_CSV), str(SOURCE_PACK_OUTPUT_CSV)], check=True)


def make_output_tables() -> dict[str, list[dict[str, Any]]]:
    exactness = read_csv(EXACTNESS_OUTPUT_CSV)
    projector = read_csv(PROJECTOR_OUTPUT_CSV)
    packs = read_csv(SOURCE_PACK_OUTPUT_CSV)
    obstruction = [
        {"update_id": "OBS4811_0_exactness", "item": "boundary exactness route", "status": "BLOCKED_MISSING_BOUNDARY_EXACTNESS_INPUTS", "value_or_bound": "Q_edge=0 if B_X=d_boundary b_X plus certified domain/Stokes/counterterm/cocycle", "meaning": "edge zero remains conditional, not physical evidence"},
        {"update_id": "OBS4811_1_projector", "item": "projector orthogonality route", "status": "BLOCKED_MISSING_PROJECTOR_INPUTS", "value_or_bound": "Qbar_edge_XH=Pi_M^H[Q_edge]/M_H_ref=0 if projector clauses close", "meaning": "edge source projection remains live"},
        {"update_id": "OBS4811_2_source_pack", "item": "edge/source no-cancellation pack", "status": "SOURCE_PACK_NUMERIC_WINDOW_PASS_SOURCE_UNSIGNED_NONCLAIM", "value_or_bound": "1.000000000000000e+00 <= 5.256633029822351e+00", "meaning": "unit edge smoke row fits the current window but physical source pack is missing"},
    ]
    gates = [
        {"gate_id": "PG4811_0_exactness_contract", "claim": "Boundary exactness route is executable", "gate_pass": True, "reason": "domain, B_X primitive, Stokes, gauge, counterterm and cocycle clauses are explicit", "evidence": str(EXACTNESS_OUTPUT_CSV)},
        {"gate_id": "PG4811_1_exactness_closed", "claim": "Boundary exactness kills Q_edge in current MTS", "gate_pass": False, "reason": "physical exactness clauses remain unsigned", "evidence": str(EXACTNESS_OUTPUT_CSV)},
        {"gate_id": "PG4811_2_projector_closed", "claim": "Projector orthogonality kills Qbar_edge_XH in current MTS", "gate_pass": False, "reason": "Pi_M definition, mass independence, symplectic block, reference silence and source-measure lock remain unsigned", "evidence": str(PROJECTOR_OUTPUT_CSV)},
        {"gate_id": "PG4811_3_source_pack_complete", "claim": "Complete no-cancellation source pack is claim-ready", "gate_pass": False, "reason": "physical pack lacks source-backed components", "evidence": str(SOURCE_PACK_OUTPUT_CSV)},
        {"gate_id": "PG4811_4_Newton_local_GR", "claim": "Newton/local-GR source coupling promotion is allowed", "gate_pass": False, "reason": "edge theorem-zero and source-pack fallback remain nonclaim", "evidence": "nonclaim firewall active"},
    ]
    firewalls = [
        {"firewall_id": "FW4811_0_no_edge_zero_by_fiat", "rule": "Edge charge cannot be deleted by symbolic exactness or overrestricted domain choice.", "status": "ACTIVE"},
        {"firewall_id": "FW4811_1_no_post_readout_projector", "rule": "Pi_M^H must be fixed before orbital/readout calibration.", "status": "ACTIVE"},
        {"firewall_id": "FW4811_2_no_unknown_cancellation", "rule": "FB5540, bulk, edge, R11 and projector-edge components use absolute no-cancellation scoring until split is proved.", "status": "ACTIVE"},
        {"firewall_id": "FW4811_3_no_bound_as_source", "rule": "An experimental bound cannot supply a missing MTS source coefficient.", "status": "ACTIVE"},
    ]
    decisions = [
        {"decision_id": "DEC4811_0_exactness", "decision": "boundary_exactness_is_precise_but_unsigned", "reason": "B_X exactness needs certified domain/cohomology/counterterm/cocycle clauses", "next_action": "derive boundary cohomology/domain certificate or retain source pack"},
        {"decision_id": "DEC4811_1_projector", "decision": "projector_orthogonality_is_precise_but_unsigned", "reason": "Pi_M^H[Q_edge]=0 needs fixed projector, mass independence, symplectic block and reference silence", "next_action": "derive projector definition from same parent boundary class"},
        {"decision_id": "DEC4811_2_fallback", "decision": "source_pack_required_if_edge_zero_fails", "reason": "edge residual becomes physical unless exactness/projector theorem-zero closes", "next_action": "source M_H_ref, FB5540, bulk, edge, R11 and projector-edge rows together"},
        {"decision_id": "DEC4811_3_next", "decision": "boundary_cohomology_domain_certificate_or_source_pack_first_row_is_next", "reason": "BE domain/B_X primitive are the earliest clauses that can kill Q_edge cleanly", "next_action": NEXT_TARGET},
    ]
    status = [
        {"status_id": "STATUS4811_0_exactness", "status": "BOUNDARY_EXACTNESS_ROUTE_UNSIGNED", "detail": "Q_edge=0 remains conditional"},
        {"status_id": "STATUS4811_1_projector", "status": "PROJECTOR_ORTHOGONALITY_ROUTE_UNSIGNED", "detail": "Qbar_edge_XH=0 remains conditional"},
        {"status_id": "STATUS4811_2_source", "status": "SOURCE_PACK_WINDOW_SMOKE_PASS_NONCLAIM", "detail": "1.0 <= 5.256633029822351, physical source pack missing"},
        {"status_id": "STATUS4811_3_selected_next", "status": "BOUNDARY_COHOMOLOGY_DOMAIN_CERTIFICATE_OR_SOURCE_PACK_FIRST_ROW", "detail": NEXT_TARGET},
    ]
    next_rows = [{"route_id": "NEXT4811_0_primary", "next_target": NEXT_TARGET, "script": "scripts/Y5_R2FR_4812_boundary_cohomology_domain_certificate_or_source_pack_first_row.py", "objective": "certify boundary domain/cohomology and B_X primitive, or produce first source-backed source-pack row", "selection_status": "selected", "success_condition": "Q_edge is killed by domain/exactness theorem or first source-pack row is explicit nonclaim data with source paths"}]
    write_csv(OBSTRUCTION_UPDATE_CSV, obstruction)
    write_csv(GATE_CSV, gates)
    write_csv(FIREWALL_CSV, firewalls)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, status)
    write_csv(NEXT_TARGET_CSV, next_rows)
    return {"exactness": exactness, "projector": projector, "packs": packs, "obstruction": obstruction, "gates": gates, "firewalls": firewalls, "decisions": decisions, "status": status, "next": next_rows}


def validate() -> list[dict[str, Any]]:
    sources = read_csv(SOURCE_REGISTER_CSV)
    exactness = {row["clause_id"]: row for row in read_csv(EXACTNESS_OUTPUT_CSV)}
    projector = {row["projector_id"]: row for row in read_csv(PROJECTOR_OUTPUT_CSV)}
    packs = {row["pack_id"]: row for row in read_csv(SOURCE_PACK_OUTPUT_CSV)}
    source_pass = all(row["exists"] == "True" and row["needle_found"] == "True" for row in sources)
    checks = [
        {"check_id": "VAL4811_0_sources", "description": "all cited sources exist and needles are found", "result": "PASS" if source_pass else "FAIL", "evidence": str(SOURCE_REGISTER_CSV)},
        {"check_id": "VAL4811_1_physical_exactness_blocks", "description": "physical exactness row remains blocked", "result": "PASS" if exactness["physical_exactness_missing"]["exactness_status"] == "BLOCKED_MISSING_BOUNDARY_EXACTNESS_INPUTS" else "FAIL", "evidence": str(EXACTNESS_OUTPUT_CSV)},
        {"check_id": "VAL4811_2_forbidden_exactness_fails", "description": "forbidden symbolic edge zero control fails", "result": "PASS" if exactness["forbidden_symbolic_edge_zero"]["anti_circularity_status"] == "FAIL_FORBIDDEN_SOURCE_USED" else "FAIL", "evidence": str(EXACTNESS_OUTPUT_CSV)},
        {"check_id": "VAL4811_3_physical_projector_blocks", "description": "physical projector row remains blocked", "result": "PASS" if projector["physical_projector_missing"]["projector_status"] == "BLOCKED_MISSING_PROJECTOR_INPUTS" else "FAIL", "evidence": str(PROJECTOR_OUTPUT_CSV)},
        {"check_id": "VAL4811_4_forbidden_projector_fails", "description": "forbidden post-readout projector control fails", "result": "PASS" if projector["forbidden_post_readout_projector"]["anti_circularity_status"] == "FAIL_FORBIDDEN_SOURCE_USED" else "FAIL", "evidence": str(PROJECTOR_OUTPUT_CSV)},
        {"check_id": "VAL4811_5_physical_pack_blocks", "description": "physical source pack remains blocked", "result": "PASS" if packs["physical_source_pack_missing"]["source_pack_status"] == "BLOCKED_MISSING_SOURCE_PACK_INPUTS" else "FAIL", "evidence": str(SOURCE_PACK_OUTPUT_CSV)},
        {"check_id": "VAL4811_6_unit_pack_passes", "description": "unit edge source pack smoke passes target window", "result": "PASS" if packs["unit_edge_source_pack_smoke"]["numeric_window_pass"] == "True" else "FAIL", "evidence": str(SOURCE_PACK_OUTPUT_CSV)},
        {"check_id": "VAL4811_7_strict_fail", "description": "strict source pack control fails numeric target", "result": "PASS" if packs["strict_source_pack_fail_control"]["numeric_window_pass"] == "False" and packs["strict_source_pack_fail_control"]["source_pack_status"] == "SOURCE_PACK_NUMERIC_WINDOW_FAIL" else "FAIL", "evidence": str(SOURCE_PACK_OUTPUT_CSV)},
        {"check_id": "VAL4811_8_forbidden_pack_fails", "description": "forbidden cancellation pack control fails", "result": "PASS" if packs["forbidden_unknown_cancellation_pack"]["anti_circularity_status"] == "FAIL_FORBIDDEN_SOURCE_USED" else "FAIL", "evidence": str(SOURCE_PACK_OUTPUT_CSV)},
        {"check_id": "VAL4811_9_claim", "description": "claim register includes L-653 as nonclaim", "result": "PASS" if CLAIM_ID in read_text(CLAIMS_PATH) and DECISION in read_text(CLAIMS_PATH) else "FAIL", "evidence": str(CLAIMS_PATH)},
        {"check_id": "VAL4811_10_resume", "description": "resume points at 4812", "result": "PASS" if NEXT_TARGET in read_text(RESUME_PATH) else "FAIL", "evidence": str(RESUME_PATH)},
    ]
    checks.append({"check_id": "VAL4811_OVERALL", "description": "all 4811 boundary/projector checks pass", "result": "PASS" if all(row["result"] == "PASS" for row in checks) else "FAIL", "evidence": DECISION})
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
    row = {"claim_id": CLAIM_ID, "domain": "local_gr", "claim": "boundary_exactness_projector_source_pack_runner", "current_evidence": "4811 installs boundary exactness, projector orthogonality and no-cancellation source-pack gates; unit edge residual passes the current window but remains source-unsigned.", "status": "boundary_exactness_projector_source_pack_private_nonclaim", "next_test": NEXT_TARGET, "key_risk": "symbolic edge zero; post-readout projector; unknown cancellation; bound as source", "sector": "local_gr", "evidence": str(DOC_PATH), "next_action": NEXT_TARGET, "risk": "domain fiat; projector after readout; boundary cohomology leak; edge double count; fitted source pack", "title": "Boundary exactness projector orthogonality and source-pack gate", "notes": f"{MARKER}; {DECISION}; generated {timestamp}"}
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        csv.DictWriter(handle, fieldnames=list(row)).writerow(row)


def update_registers(timestamp: str) -> None:
    append_claim(timestamp)
    append_once(SPINE_PATH, MARKER, f"""

## {MARKER}

4811 splits the edge obstruction into theorem routes and a fallback source pack:

```text
Q_edge = integral_boundary F_lambda epsilon B_X
Q_edge = 0 if B_X=d_boundary b_X on a certified closed boundary domain
Qbar_edge_XH = Pi_M^H[Q_edge] / M_H_ref = 0 if Pi_M^H is orthogonal to the edge sector
source_pack_guard = (|FB5540| + |bulk_X| + |edge_X| + |R11| + |Pi_M^H Q_edge|) / |M_H_ref|
```

Current MTS has the right theorem shape but does not yet sign the boundary domain, primitive, Stokes kernel, counterterm, cocycle, projector, or source-measure clauses. The next attack is the boundary cohomology/domain certificate.
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
Last checkpoint: `4811-Y5-R2FR-boundary-exactness-projector-orthogonality-or-source-pack.md`
Marker: `{MARKER}`

## Where we are

4811 installed the boundary exactness/projector/source-pack gate:

```text
Q_edge = integral_boundary F_lambda epsilon B_X
Q_edge = 0 if B_X=d_boundary b_X on a certified closed boundary domain
Qbar_edge_XH = Pi_M^H[Q_edge] / M_H_ref = 0 if Pi_M^H is orthogonal to the edge sector
source_pack_guard = (|FB5540| + |bulk_X| + |edge_X| + |R11| + |Pi_M^H Q_edge|) / |M_H_ref|
source_pack_guard <= 5.256633029822351
```

## Live blockers

- Boundary exactness needs a certified boundary domain/cohomology class, `B_X` primitive, Stokes kernel silence, counterterm and cocycle zero.
- Projector orthogonality needs fixed `Pi_M^H`, edge mass-independence, symplectic block, reference silence, tau lock and source-measure lock.
- If theorem-zero fails, the source pack must be complete and no-cancellation scored.

## Next target

`{NEXT_TARGET}`
""", encoding="utf-8")


def write_docs(timestamp: str, target: dict[str, str], outputs: dict[str, list[dict[str, Any]]], validation: list[dict[str, Any]]) -> None:
    sources = read_csv(SOURCE_REGISTER_CSV)
    target_rows = read_csv(TARGET_AUDIT_CSV)
    doc = f"""# 4811 - Boundary exactness projector orthogonality or source pack

Marker: `{MARKER}`
Generated: `{timestamp}`
Decision: `{DECISION}`

## Result

4811 attacks the live edge/boundary obstruction directly:

```text
Q_edge = integral_boundary F_lambda epsilon B_X
Q_edge = 0 if B_X=d_boundary b_X on a certified closed boundary domain
Qbar_edge_XH = Pi_M^H[Q_edge] / M_H_ref = 0 if Pi_M^H is orthogonal to the edge sector
source_pack_guard = (|FB5540| + |bulk_X| + |edge_X| + |R11| + |Pi_M^H Q_edge|) / |M_H_ref|
required: source_pack_guard <= {target['required_abs_max']}
```

The theorem routes are clean but still unsigned. A unit edge source-pack smoke row sits inside the current window, but physical promotion needs either theorem-zero closure or a complete no-cancellation source pack.

## Target Audit

{table(target_rows, ['audit_id', 'component_expr', 'required_abs_max', 'source', 'derivation', 'valid_for_claim', 'timestamp_utc'])}

## Source Register

{table(sources, ['source_id', 'source_path', 'exists', 'needle_found', 'role'])}

## Boundary Exactness Output

{table(outputs['exactness'], ['clause_id', 'route', 'exactness_status', 'exactness_theorem', 'missing_exactness_inputs', 'anti_circularity_status'])}

## Projector Orthogonality Output

{table(outputs['projector'], ['projector_id', 'route', 'projector_status', 'projector_theorem', 'missing_projector_inputs', 'anti_circularity_status'])}

## Source Pack Output

{table(outputs['packs'], ['pack_id', 'component_expr', 'source_pack_guard_abs', 'required_abs_max', 'numeric_window_pass', 'source_pack_status', 'missing_source_pack_inputs', 'anti_circularity_status'])}

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
    FORMAL_PATH.write_text(f"""# 827 - PPC4161 boundary exactness projector orthogonality or source pack

Marker: `{MARKER}`
Generated: `{timestamp}`

4811 turns the edge branch into the exact theorem/source-pack fork:

```text
Q_edge = integral_boundary F_lambda epsilon B_X
Q_edge = 0 if B_X=d_boundary b_X on a certified closed boundary domain
Qbar_edge_XH = Pi_M^H[Q_edge] / M_H_ref = 0 if Pi_M^H is orthogonal to the edge sector
```

Unit edge residual gives `1.0 <= 5.256633029822351`, but physical promotion remains blocked until boundary exactness/projector orthogonality is parent-signed or a complete source pack exists. Next target: `{NEXT_TARGET}`.
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
