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

CHECKPOINT = "4812"
CLAIM_ID = "L-654"
MARKER = "PPC4161_BOUNDARY_COHOMOLOGY_DOMAIN_CERTIFICATE_OR_SOURCE_PACK_FIRST_ROW_4812"
PACKET_MARKER = "PPC4161_PACKET_BOUNDARY_COHOMOLOGY_DOMAIN_CERTIFICATE_OR_SOURCE_PACK_FIRST_ROW_4812"
DECISION = "BOUNDARY_COHOMOLOGY_DOMAIN_AND_WEIGHTED_STOKES_SOURCE_ROW_GATE_NONCLAIM"
NEXT_TARGET = "4813-Y5-R2FR-BX-primitive-from-parent-variation-or-edge-bound-term-fill.md"

DOC_PATH = POST / "4812-Y5-R2FR-boundary-cohomology-domain-certificate-or-source-pack-first-row.md"
FORMAL_PATH = FORMAL / "828-PPC4161-boundary-cohomology-domain-certificate-or-source-pack-first-row.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"
RUNNER = SCRIPT_DIR / "boundary_cohomology_weighted_stokes_runner.py"

SOURCE_REGISTER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4812_SOURCE_REGISTER.csv"
DOMAIN_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4812_DOMAIN_CERTIFICATE_INPUT.csv"
DOMAIN_OUTPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4812_DOMAIN_CERTIFICATE_OUTPUT.csv"
STOKES_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4812_WEIGHTED_STOKES_INPUT.csv"
STOKES_OUTPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4812_WEIGHTED_STOKES_OUTPUT.csv"
BOUND_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4812_EDGE_BOUND_FIRST_ROW_INPUT.csv"
BOUND_OUTPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4812_EDGE_BOUND_FIRST_ROW_OUTPUT.csv"
TARGET_AUDIT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4812_TARGET_AUDIT.csv"
OBSTRUCTION_UPDATE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4812_OBSTRUCTION_UPDATE.csv"
GATE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4812_PROMOTION_GATES.csv"
FIREWALL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4812_FIREWALL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4812_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4812_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4812_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4812_VALIDATION.csv"

TARGET_4811 = SOURCE_DIR / "P8_Y5_R2FR_4811_TARGET_AUDIT.csv"
DOMAIN_1020 = SOURCE_DIR / "P8_Y5_R10_1020_BOUNDARY_DOMAIN_CERTIFICATE.csv"
STOKES_1020 = SOURCE_DIR / "P8_Y5_R10_1020_WEIGHTED_STOKES_THEOREM_AND_BOUND.csv"
BX_AUDIT_1020 = SOURCE_DIR / "P8_Y5_R10_1020_BX_PRIMITIVE_AUDIT.csv"
FIRST_ROW_1020 = SOURCE_DIR / "P8_Y5_R10_1020_SOURCE_PACK_FIRST_BOUND_ROW.csv"
EXACT_672 = SOURCE_DIR / "P8_Y5_R10_672_BOUNDARY_EXACTNESS_ATTEMPT.csv"
EDGE_671 = SOURCE_DIR / "P8_Y5_R10_671_EDGE_RESIDUAL_VECTOR.csv"

DOMAIN_CLAUSES = (
    "surface_manifold_signed",
    "boundary_class_signed",
    "relative_cohomology_signed",
    "epsilon_domain_signed",
    "kernel_weight_signed",
    "BX_primitive_signed",
    "no_GR_import_signed",
    "no_fit_to_bound_signed",
)

STOKES_CLAUSES = (
    "decomposition_signed",
    "weighted_stokes_identity_signed",
    "corner_zero_or_bound_signed",
    "harmonic_zero_or_bound_signed",
    "residual_zero_or_bound_signed",
    "kernel_derivative_zero_or_bound_signed",
    "projector_bound_signed",
    "no_GR_import_signed",
    "no_fit_to_bound_signed",
)

BOUND_TERMS = (
    "C_corner_abs",
    "norm_dS_Feps_abs",
    "norm_bX_abs",
    "harmonic_edge_abs",
    "residual_edge_abs",
    "PiM_norm_abs",
    "M_H_ref_min_abs",
)

SOURCE_SPECS = [
    ("SRC4812_00_4811_doc", POST / "4811-Y5-R2FR-boundary-exactness-projector-orthogonality-or-source-pack.md", "boundary_cohomology_domain_certificate_or_source_pack_first_row", "4811 selects boundary cohomology/domain target"),
    ("SRC4812_01_4811_target", TARGET_4811, "TGA4811_0_target_import", "4811 inherited target audit"),
    ("SRC4812_02_1020_doc", POST / "1020-Y5-R10-boundary-cohomology-domain-certificate-or-source-pack-first-row.md", "weighted-Stokes theorem", "1020 weighted-Stokes precedent"),
    ("SRC4812_03_1020_domain", DOMAIN_1020, "BDC1020_0_surface_manifold", "1020 boundary domain certificate"),
    ("SRC4812_04_1020_stokes", STOKES_1020, "ETB1020_1_weighted_Stokes_identity", "1020 weighted Stokes identity"),
    ("SRC4812_05_1020_BX", BX_AUDIT_1020, "BXP1020_2_exact_primitive", "1020 B_X primitive audit"),
    ("SRC4812_06_1020_first_row", FIRST_ROW_1020, "EDGEBOUND1020_0_formal_bound_row", "1020 first source-pack bound row"),
    ("SRC4812_07_672_exact", EXACT_672, "BE672_1_BX_exact_form", "672 exactness attempt"),
    ("SRC4812_08_671_edge", EDGE_671, "ERV671_2_Qbar_edge_XH", "671 edge residual vector"),
    ("SRC4812_09_runner", RUNNER, "def domain_certificate_row", "4812 executable domain/Stokes/bound runner"),
]


RUNNER_TEXT = r'''from __future__ import annotations

import csv
import math
import sys
from pathlib import Path
from typing import Any


DOMAIN_CLAUSES = (
    "surface_manifold_signed",
    "boundary_class_signed",
    "relative_cohomology_signed",
    "epsilon_domain_signed",
    "kernel_weight_signed",
    "BX_primitive_signed",
    "no_GR_import_signed",
    "no_fit_to_bound_signed",
)

STOKES_CLAUSES = (
    "decomposition_signed",
    "weighted_stokes_identity_signed",
    "corner_zero_or_bound_signed",
    "harmonic_zero_or_bound_signed",
    "residual_zero_or_bound_signed",
    "kernel_derivative_zero_or_bound_signed",
    "projector_bound_signed",
    "no_GR_import_signed",
    "no_fit_to_bound_signed",
)

FORBIDDEN_SOURCE_TOKENS = (
    "GR_IMPORT",
    "FIT_TO_BOUND",
    "BOUND_AS_SOURCE",
    "ORBITAL_GM_AS_SOURCE",
    "STOKES_ZERO_WITHOUT_WEIGHT",
    "DELETE_HARMONIC_BY_ASSUMPTION",
    "CORNER_SILENCE_BY_FIAT",
    "SYMBOLIC_BX_EXACT",
    "REFERENCE_ONLY_ZERO",
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
        for field in ("certificate_id", "theorem_id", "row_id", "source_path", "equation_ref", "notes", "provenance")
    ).upper()
    return any(token in source_text for token in FORBIDDEN_SOURCE_TOKENS)


def missing_clauses(row: dict[str, Any], clauses: tuple[str, ...]) -> list[str]:
    return [clause for clause in clauses if not bool_text(row.get(clause))]


def domain_certificate_row(row: dict[str, Any]) -> dict[str, Any]:
    certificate_id = str(row.get("certificate_id", "")).strip() or "UNNAMED_DOMAIN"
    output: dict[str, Any] = {"certificate_id": certificate_id, "route": row.get("route", ""), "valid_for_claim": False, "claim_allowed": False}
    if forbidden_source_used(row):
        output.update({"domain_status": "FAILED_DOMAIN_CERTIFICATE_GATE", "domain_theorem": False, "missing_domain_inputs": "FORBIDDEN_DOMAIN_SOURCE", "anti_circularity_status": "FAIL_FORBIDDEN_SOURCE_USED"})
        return output
    missing = missing_clauses(row, DOMAIN_CLAUSES)
    status = "DOMAIN_CERTIFICATE_SIGNED_CONDITIONAL_NONCLAIM" if not missing else "BLOCKED_MISSING_DOMAIN_CERTIFICATE_INPUTS"
    output.update({"domain_status": status, "domain_theorem": not missing, "missing_domain_inputs": ";".join(missing), "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED"})
    return output


def weighted_stokes_row(row: dict[str, Any]) -> dict[str, Any]:
    theorem_id = str(row.get("theorem_id", "")).strip() or "UNNAMED_STOKES"
    output: dict[str, Any] = {"theorem_id": theorem_id, "route": row.get("route", ""), "valid_for_claim": False, "claim_allowed": False}
    if forbidden_source_used(row):
        output.update({"stokes_status": "FAILED_WEIGHTED_STOKES_GATE", "zero_theorem": False, "missing_stokes_inputs": "FORBIDDEN_STOKES_SOURCE", "anti_circularity_status": "FAIL_FORBIDDEN_SOURCE_USED"})
        return output
    missing = missing_clauses(row, STOKES_CLAUSES)
    status = "WEIGHTED_STOKES_ZERO_SIGNED_CONDITIONAL_NONCLAIM" if not missing else "BLOCKED_MISSING_WEIGHTED_STOKES_INPUTS"
    output.update({"stokes_status": status, "zero_theorem": not missing, "missing_stokes_inputs": ";".join(missing), "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED"})
    return output


def edge_bound_values(row: dict[str, Any]) -> tuple[float | None, float | None, list[str]]:
    missing: list[str] = []
    c_corner = parse_float(row.get("C_corner_abs"))
    norm_weight = parse_float(row.get("norm_dS_Feps_abs"))
    norm_bx = parse_float(row.get("norm_bX_abs"))
    harmonic = parse_float(row.get("harmonic_edge_abs"))
    residual = parse_float(row.get("residual_edge_abs"))
    pim_norm = parse_float(row.get("PiM_norm_abs"))
    mh_ref = parse_float(row.get("M_H_ref_min_abs"))
    values = {
        "C_corner_abs": c_corner,
        "norm_dS_Feps_abs": norm_weight,
        "norm_bX_abs": norm_bx,
        "harmonic_edge_abs": harmonic,
        "residual_edge_abs": residual,
        "PiM_norm_abs": pim_norm,
        "M_H_ref_min_abs": mh_ref,
    }
    for name, value in values.items():
        if value is None or value < 0.0:
            missing.append(f"MISSING_{name}")
    if mh_ref is not None and mh_ref <= 0.0:
        missing.append("MISSING_POSITIVE_M_H_ref_min_abs")
    if missing:
        return None, None, missing
    q_edge = c_corner + norm_weight * norm_bx + harmonic + residual
    qbar = pim_norm * q_edge / mh_ref
    return q_edge, qbar, []


def edge_bound_row(row: dict[str, Any]) -> dict[str, Any]:
    row_id = str(row.get("row_id", "")).strip() or "UNNAMED_EDGE_BOUND"
    output: dict[str, Any] = {"row_id": row_id, "quantity": row.get("quantity", ""), "valid_for_claim": False, "claim_allowed": False}
    if forbidden_source_used(row):
        output.update({"Q_edge_bound_abs": "MISSING_NUMERIC_VALUE", "Qbar_edge_XH_bound_abs": "MISSING_NUMERIC_VALUE", "required_abs_max": format_float(parse_float(row.get("required_abs_max"))), "numeric_window_pass": False, "bound_status": "FAILED_EDGE_BOUND_GATE", "missing_bound_inputs": "FORBIDDEN_EDGE_BOUND_SOURCE", "anti_circularity_status": "FAIL_FORBIDDEN_SOURCE_USED"})
        return output
    required = parse_float(row.get("required_abs_max"))
    q_edge, qbar, missing = edge_bound_values(row)
    if required is None or required <= 0.0:
        missing.append("MISSING_required_abs_max")
    if missing_text(row.get("source_path")):
        missing.append("MISSING_source_path")
    if missing_text(row.get("equation_ref")):
        missing.append("MISSING_equation_ref")
    if not bool_text(row.get("source_signed")):
        missing.append("MISSING_source_signed")
    if required is None or required <= 0.0 or qbar is None:
        output.update({"Q_edge_bound_abs": format_float(q_edge), "Qbar_edge_XH_bound_abs": "MISSING_NUMERIC_VALUE", "required_abs_max": format_float(required), "numeric_window_pass": False, "bound_status": "BLOCKED_MISSING_EDGE_BOUND_INPUTS", "missing_bound_inputs": ";".join(missing), "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED"})
        return output
    passes = qbar <= required
    status = "EDGE_BOUND_NUMERIC_WINDOW_FAIL"
    if passes:
        status = "EDGE_BOUND_NUMERIC_WINDOW_PASS_SOURCE_UNSIGNED_NONCLAIM"
        if bool_text(row.get("source_signed")) and bool_text(row.get("valid_for_claim")):
            status = "EDGE_BOUND_NUMERIC_WINDOW_PASS_SOURCE_SIGNED_NONCLAIM"
    output.update({"Q_edge_bound_abs": format_float(q_edge), "Qbar_edge_XH_bound_abs": format_float(qbar), "required_abs_max": format_float(required), "numeric_window_pass": passes, "bound_status": status, "missing_bound_inputs": ";".join(missing), "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED"})
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
    if len(sys.argv) != 4 or sys.argv[1] not in {"domain", "stokes", "bound"}:
        print("Usage: boundary_cohomology_weighted_stokes_runner.py domain|stokes|bound INPUT_CSV OUTPUT_CSV", file=sys.stderr)
        return 2
    rows = read_csv(Path(sys.argv[2]))
    if sys.argv[1] == "domain":
        outputs = [domain_certificate_row(row) for row in rows]
    elif sys.argv[1] == "stokes":
        outputs = [weighted_stokes_row(row) for row in rows]
    else:
        outputs = [edge_bound_row(row) for row in rows]
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
    rows = read_csv(TARGET_4811)
    if not rows:
        raise RuntimeError("missing 4811 target rows")
    return {"component_expr": "abs(Qbar_edge_XH_bound)", "required_abs_max": rows[0]["required_abs_max"], "source": str(TARGET_4811)}


def source_register(timestamp: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path, needle, role in SOURCE_SPECS:
        text = read_text(path)
        rows.append({"checkpoint": CHECKPOINT, "source_id": source_id, "source_path": str(path), "exists": path.exists(), "needle": needle, "needle_found": bool(text and needle in text), "role": role, "valid_for_claim": False, "timestamp_utc": timestamp})
    return rows


def bools(names: tuple[str, ...], signed: bool) -> dict[str, bool]:
    return {name: signed for name in names}


def missing_bound_terms() -> dict[str, str]:
    return {term: "MISSING_PARENT_VALUE" for term in BOUND_TERMS}


def zero_bound_terms() -> dict[str, str]:
    return {term: "0.0" for term in BOUND_TERMS}


def unit_bound_terms() -> dict[str, str]:
    return {
        "C_corner_abs": "0.0",
        "norm_dS_Feps_abs": "1.0",
        "norm_bX_abs": "1.0",
        "harmonic_edge_abs": "0.0",
        "residual_edge_abs": "0.0",
        "PiM_norm_abs": "1.0",
        "M_H_ref_min_abs": "1.0",
    }


def strict_bound_terms() -> dict[str, str]:
    values = unit_bound_terms()
    values["norm_dS_Feps_abs"] = "10.0"
    return values


def write_runner() -> None:
    SCRIPT_DIR.mkdir(parents=True, exist_ok=True)
    RUNNER.write_text(RUNNER_TEXT, encoding="utf-8")


def write_inputs(timestamp: str, target: dict[str, str]) -> None:
    required = target["required_abs_max"]
    write_csv(TARGET_AUDIT_CSV, [{"audit_id": "TGA4812_0_target_import", "component_expr": "abs(Qbar_edge_XH_bound)", "required_abs_max": required, "source": target["source"], "derivation": "same normalized local coupling window inherited from 4811 edge source-pack target", "valid_for_claim": False, "timestamp_utc": timestamp}])
    domain_rows = [
        {"certificate_id": "physical_domain_certificate_missing", "route": "physical_missing", **bools(DOMAIN_CLAUSES, False), "no_GR_import_signed": True, "no_fit_to_bound_signed": True, "source_path": "MISSING_PARENT_BOUNDARY_DOMAIN_CERTIFICATE", "equation_ref": "MISSING_DOMAIN_CERTIFICATE_EQUATION", "notes": "physical branch lacks surface, boundary class, cohomology, epsilon, kernel and B_X primitive certificates", "provenance": "4812 physical branch", "valid_for_claim": False},
        {"certificate_id": "domain_certificate_unsigned", "route": "weighted_Stokes_domain", **bools(DOMAIN_CLAUSES, False), "no_GR_import_signed": True, "no_fit_to_bound_signed": True, "source_path": str(DOMAIN_1020), "equation_ref": "BDC1020_0_to_BDC1020_5", "notes": "domain certificate is mapped but unsigned for current MTS", "provenance": "1020 domain certificate", "valid_for_claim": False},
        {"certificate_id": "conditional_domain_certificate", "route": "conditional_theorem", **bools(DOMAIN_CLAUSES, True), "source_path": str(POST / "1020-Y5-R10-boundary-cohomology-domain-certificate-or-source-pack-first-row.md"), "equation_ref": "BDC1020 conditional certificate", "notes": "conditional branch only", "provenance": "1020 conditional domain", "valid_for_claim": False},
        {"certificate_id": "forbidden_domain_fiat_control", "route": "forbidden_control", **bools(DOMAIN_CLAUSES, True), "source_path": "CORNER_SILENCE_BY_FIAT_DELETE_HARMONIC_BY_ASSUMPTION", "equation_ref": "FORBIDDEN_DOMAIN_FIAT", "notes": "control row must fail if corners/harmonics are erased by assumption", "provenance": "forbidden control", "valid_for_claim": False},
    ]
    stokes_rows = [
        {"theorem_id": "physical_weighted_stokes_missing", "route": "physical_missing", **bools(STOKES_CLAUSES, False), "no_GR_import_signed": True, "no_fit_to_bound_signed": True, "source_path": "MISSING_PARENT_WEIGHTED_STOKES_CERTIFICATE", "equation_ref": "MISSING_WEIGHTED_STOKES_EQUATION", "notes": "physical branch lacks decomposition, corner/harmonic/residual/kernel/projector certificates", "provenance": "4812 physical branch", "valid_for_claim": False},
        {"theorem_id": "weighted_stokes_identity_unsigned", "route": "formal_identity_bound", **bools(STOKES_CLAUSES, False), "weighted_stokes_identity_signed": True, "residual_zero_or_bound_signed": True, "projector_bound_signed": True, "no_GR_import_signed": True, "no_fit_to_bound_signed": True, "source_path": str(STOKES_1020), "equation_ref": "ETB1020_0_to_ETB1020_5", "notes": "identity and bound law are written; zero theorem clauses remain unsigned", "provenance": "1020 weighted Stokes", "valid_for_claim": False},
        {"theorem_id": "conditional_weighted_stokes_zero", "route": "conditional_zero", **bools(STOKES_CLAUSES, True), "source_path": str(POST / "1020-Y5-R10-boundary-cohomology-domain-certificate-or-source-pack-first-row.md"), "equation_ref": "ETB1020_2 zero conditions", "notes": "conditional zero theorem only", "provenance": "1020 weighted Stokes", "valid_for_claim": False},
        {"theorem_id": "forbidden_unweighted_stokes_zero", "route": "forbidden_control", **bools(STOKES_CLAUSES, True), "source_path": "STOKES_ZERO_WITHOUT_WEIGHT_REFERENCE_ONLY_ZERO", "equation_ref": "FORBIDDEN_STOKES_ZERO", "notes": "control row must fail if Stokes zero ignores kernel/corner/harmonic terms", "provenance": "forbidden control", "valid_for_claim": False},
    ]
    bound_rows = [
        {"row_id": "physical_edge_bound_missing", "quantity": "Qbar_edge_XH_bound(lambda)", **missing_bound_terms(), "required_abs_max": required, "source_signed": False, "source_path": "MISSING_PARENT_EDGE_BOUND_FIRST_ROW", "equation_ref": "MISSING_EDGE_BOUND_EQUATION", "notes": "physical first row lacks corner, kernel derivative, b_X norm, harmonic, residual, PiM norm and M_H_ref values", "provenance": "4812 physical branch", "valid_for_claim": False},
        {"row_id": "formal_edge_bound_schema_missing", "quantity": "Qbar_edge_XH_bound(lambda)", **missing_bound_terms(), "required_abs_max": required, "source_signed": False, "source_path": str(FIRST_ROW_1020), "equation_ref": "EDGEBOUND1020_0_to_EDGEBOUND1020_1", "notes": "formal schema exists but has no numeric/source-backed terms", "provenance": "1020 source-pack first row", "valid_for_claim": False},
        {"row_id": "unit_weighted_stokes_bound_smoke", "quantity": "Qbar_edge_XH_bound(lambda)", **unit_bound_terms(), "required_abs_max": required, "source_signed": False, "source_path": str(FIRST_ROW_1020), "equation_ref": "unit weighted-Stokes bound smoke", "notes": "unit derivative/primitve term is below current target but remains nonclaim", "provenance": "4812 smoke row", "valid_for_claim": False},
        {"row_id": "strict_weighted_stokes_bound_fail", "quantity": "Qbar_edge_XH_bound(lambda)", **strict_bound_terms(), "required_abs_max": required, "source_signed": False, "source_path": str(FIRST_ROW_1020), "equation_ref": "strict fail control", "notes": "control row proves oversized edge bound fails", "provenance": "4812 control", "valid_for_claim": False},
        {"row_id": "conditional_zero_edge_bound", "quantity": "Qbar_edge_XH_bound(lambda)", **zero_bound_terms(), "M_H_ref_min_abs": "1.0", "PiM_norm_abs": "1.0", "required_abs_max": required, "source_signed": True, "source_path": str(POST / "1020-Y5-R10-boundary-cohomology-domain-certificate-or-source-pack-first-row.md"), "equation_ref": "conditional weighted-Stokes zero", "notes": "conditional branch only", "provenance": "1020 conditional branch", "valid_for_claim": False},
        {"row_id": "forbidden_bound_as_source_control", "quantity": "Qbar_edge_XH_bound(lambda)", **zero_bound_terms(), "M_H_ref_min_abs": "1.0", "PiM_norm_abs": "1.0", "required_abs_max": required, "source_signed": True, "source_path": "BOUND_AS_SOURCE_FIT_TO_BOUND", "equation_ref": "FORBIDDEN_BOUND_AS_SOURCE", "notes": "control row must fail if experimental bound supplies the missing coefficient", "provenance": "forbidden control", "valid_for_claim": False},
    ]
    write_csv(DOMAIN_INPUT_CSV, domain_rows)
    write_csv(STOKES_INPUT_CSV, stokes_rows)
    write_csv(BOUND_INPUT_CSV, bound_rows)


def run_runner() -> None:
    subprocess.run([sys.executable, str(RUNNER), "domain", str(DOMAIN_INPUT_CSV), str(DOMAIN_OUTPUT_CSV)], check=True)
    subprocess.run([sys.executable, str(RUNNER), "stokes", str(STOKES_INPUT_CSV), str(STOKES_OUTPUT_CSV)], check=True)
    subprocess.run([sys.executable, str(RUNNER), "bound", str(BOUND_INPUT_CSV), str(BOUND_OUTPUT_CSV)], check=True)


def make_output_tables() -> dict[str, list[dict[str, Any]]]:
    domains = read_csv(DOMAIN_OUTPUT_CSV)
    stokes = read_csv(STOKES_OUTPUT_CSV)
    bounds = read_csv(BOUND_OUTPUT_CSV)
    obstruction = [
        {"update_id": "OBS4812_0_domain", "item": "boundary domain/cohomology certificate", "status": "BLOCKED_MISSING_DOMAIN_CERTIFICATE_INPUTS", "value_or_bound": "closed surface + fixed B_class + no harmonic edge + allowed epsilon + closed/bounded kernel", "meaning": "Stokes zero cannot be claimed without domain certificates"},
        {"update_id": "OBS4812_1_stokes", "item": "weighted-Stokes theorem", "status": "BLOCKED_MISSING_WEIGHTED_STOKES_INPUTS", "value_or_bound": "int_S F epsilon d_S b_X = corner - int_S d_S(F epsilon) wedge b_X", "meaning": "edge exactness leaves derivative/harmonic/residual terms unless they are zero or bounded"},
        {"update_id": "OBS4812_2_bound", "item": "first projected edge bound row", "status": "EDGE_BOUND_NUMERIC_WINDOW_PASS_SOURCE_UNSIGNED_NONCLAIM", "value_or_bound": "Qbar=1.000000000000000e+00 <= 5.256633029822351e+00", "meaning": "unit weighted-Stokes bound fits current window; physical terms remain missing"},
    ]
    gates = [
        {"gate_id": "PG4812_0_domain_contract", "claim": "Boundary cohomology/domain certificate is executable", "gate_pass": True, "reason": "surface, class, cohomology, epsilon, kernel and B_X primitive clauses are explicit", "evidence": str(DOMAIN_OUTPUT_CSV)},
        {"gate_id": "PG4812_1_domain_closed", "claim": "Domain certificate closes current MTS", "gate_pass": False, "reason": "physical domain clauses remain unsigned", "evidence": str(DOMAIN_OUTPUT_CSV)},
        {"gate_id": "PG4812_2_weighted_stokes_zero", "claim": "Weighted-Stokes zero kills Q_edge", "gate_pass": False, "reason": "corner, harmonic, residual and kernel derivative certificates are missing", "evidence": str(STOKES_OUTPUT_CSV)},
        {"gate_id": "PG4812_3_first_bound_row", "claim": "First source-pack bound row is claim-ready", "gate_pass": False, "reason": "physical row lacks source-backed terms", "evidence": str(BOUND_OUTPUT_CSV)},
        {"gate_id": "PG4812_4_Newton_local_GR", "claim": "Newton/local-GR source coupling promotion is allowed", "gate_pass": False, "reason": "edge domain/Stokes/bound branch remains nonclaim", "evidence": "nonclaim firewall active"},
    ]
    firewalls = [
        {"firewall_id": "FW4812_0_no_unweighted_stokes", "rule": "Stokes zero is forbidden unless kernel derivative, corner, harmonic and residual terms are zero or bounded.", "status": "ACTIVE"},
        {"firewall_id": "FW4812_1_no_harmonic_silence", "rule": "Harmonic edge modes cannot be deleted by assumption.", "status": "ACTIVE"},
        {"firewall_id": "FW4812_2_no_domain_fiat", "rule": "Boundary domain restrictions may not erase physical tau/mass/rotation charges.", "status": "ACTIVE"},
        {"firewall_id": "FW4812_3_no_bound_as_source", "rule": "Experimental bounds cannot be used as missing MTS source coefficients.", "status": "ACTIVE"},
    ]
    decisions = [
        {"decision_id": "DEC4812_0_derivation_result", "decision": "weighted_Stokes_route_sharp_but_not_closed", "reason": "corner, kernel derivative, harmonic and residual terms remain unsigned", "next_action": "derive explicit B_X primitive or fill edge-bound terms"},
        {"decision_id": "DEC4812_1_best_next_route", "decision": "BX_primitive_is_next_hard_object", "reason": "without b_X, neither the zero theorem nor the weighted bound has its central object", "next_action": NEXT_TARGET},
        {"decision_id": "DEC4812_2_fallback", "decision": "edge_bound_row_is_the_fallback_if_BX_fails", "reason": "Q_edge can be bounded term-by-term without unknown cancellation", "next_action": "source C_corner, norm_dS_Feps, norm_bX, harmonic, residual, PiM_norm and M_H_ref_min"},
        {"decision_id": "DEC4812_3_status", "decision": "no_R10_R11_or_local_GR_claim_allowed", "reason": "domain theorem and source row are still nonclaim", "next_action": NEXT_TARGET},
    ]
    status = [
        {"status_id": "STATUS4812_0_domain", "status": "DOMAIN_CERTIFICATE_UNSIGNED", "detail": "surface/cohomology/epsilon/kernel/B_X clauses remain physical blockers"},
        {"status_id": "STATUS4812_1_stokes", "status": "WEIGHTED_STOKES_BOUND_LAW_STAGED", "detail": "identity written as executable gate; zero theorem unsigned"},
        {"status_id": "STATUS4812_2_bound", "status": "EDGE_BOUND_WINDOW_SMOKE_PASS_NONCLAIM", "detail": "unit Qbar bound passes but physical terms are missing"},
        {"status_id": "STATUS4812_3_selected_next", "status": "BX_PRIMITIVE_FROM_PARENT_VARIATION_OR_EDGE_BOUND_TERM_FILL", "detail": NEXT_TARGET},
    ]
    next_rows = [{"route_id": "NEXT4812_0_primary", "next_target": NEXT_TARGET, "script": "scripts/Y5_R2FR_4813_BX_primitive_from_parent_variation_or_edge_bound_term_fill.py", "objective": "derive explicit B_X primitive from parent variation/counterterm or fill the first edge-bound term with units and source path", "selection_status": "selected", "success_condition": "b_X primitive is parent-derived or first weighted-Stokes bound term becomes explicit nonclaim data"}]
    write_csv(OBSTRUCTION_UPDATE_CSV, obstruction)
    write_csv(GATE_CSV, gates)
    write_csv(FIREWALL_CSV, firewalls)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, status)
    write_csv(NEXT_TARGET_CSV, next_rows)
    return {"domains": domains, "stokes": stokes, "bounds": bounds, "obstruction": obstruction, "gates": gates, "firewalls": firewalls, "decisions": decisions, "status": status, "next": next_rows}


def validate() -> list[dict[str, Any]]:
    sources = read_csv(SOURCE_REGISTER_CSV)
    domains = {row["certificate_id"]: row for row in read_csv(DOMAIN_OUTPUT_CSV)}
    stokes = {row["theorem_id"]: row for row in read_csv(STOKES_OUTPUT_CSV)}
    bounds = {row["row_id"]: row for row in read_csv(BOUND_OUTPUT_CSV)}
    source_pass = all(row["exists"] == "True" and row["needle_found"] == "True" for row in sources)
    checks = [
        {"check_id": "VAL4812_0_sources", "description": "all cited sources exist and needles are found", "result": "PASS" if source_pass else "FAIL", "evidence": str(SOURCE_REGISTER_CSV)},
        {"check_id": "VAL4812_1_physical_domain_blocks", "description": "physical domain certificate remains blocked", "result": "PASS" if domains["physical_domain_certificate_missing"]["domain_status"] == "BLOCKED_MISSING_DOMAIN_CERTIFICATE_INPUTS" else "FAIL", "evidence": str(DOMAIN_OUTPUT_CSV)},
        {"check_id": "VAL4812_2_forbidden_domain_fails", "description": "forbidden domain fiat control fails", "result": "PASS" if domains["forbidden_domain_fiat_control"]["anti_circularity_status"] == "FAIL_FORBIDDEN_SOURCE_USED" else "FAIL", "evidence": str(DOMAIN_OUTPUT_CSV)},
        {"check_id": "VAL4812_3_physical_stokes_blocks", "description": "physical weighted-Stokes row remains blocked", "result": "PASS" if stokes["physical_weighted_stokes_missing"]["stokes_status"] == "BLOCKED_MISSING_WEIGHTED_STOKES_INPUTS" else "FAIL", "evidence": str(STOKES_OUTPUT_CSV)},
        {"check_id": "VAL4812_4_forbidden_stokes_fails", "description": "forbidden unweighted Stokes control fails", "result": "PASS" if stokes["forbidden_unweighted_stokes_zero"]["anti_circularity_status"] == "FAIL_FORBIDDEN_SOURCE_USED" else "FAIL", "evidence": str(STOKES_OUTPUT_CSV)},
        {"check_id": "VAL4812_5_physical_bound_blocks", "description": "physical edge-bound row remains blocked", "result": "PASS" if bounds["physical_edge_bound_missing"]["bound_status"] == "BLOCKED_MISSING_EDGE_BOUND_INPUTS" else "FAIL", "evidence": str(BOUND_OUTPUT_CSV)},
        {"check_id": "VAL4812_6_schema_bound_blocks", "description": "formal schema row remains blocked", "result": "PASS" if bounds["formal_edge_bound_schema_missing"]["bound_status"] == "BLOCKED_MISSING_EDGE_BOUND_INPUTS" else "FAIL", "evidence": str(BOUND_OUTPUT_CSV)},
        {"check_id": "VAL4812_7_unit_bound_passes", "description": "unit weighted-Stokes bound smoke passes target window", "result": "PASS" if bounds["unit_weighted_stokes_bound_smoke"]["numeric_window_pass"] == "True" else "FAIL", "evidence": str(BOUND_OUTPUT_CSV)},
        {"check_id": "VAL4812_8_strict_fail", "description": "strict weighted-Stokes bound control fails numeric target", "result": "PASS" if bounds["strict_weighted_stokes_bound_fail"]["numeric_window_pass"] == "False" and bounds["strict_weighted_stokes_bound_fail"]["bound_status"] == "EDGE_BOUND_NUMERIC_WINDOW_FAIL" else "FAIL", "evidence": str(BOUND_OUTPUT_CSV)},
        {"check_id": "VAL4812_9_forbidden_bound_fails", "description": "forbidden bound-as-source control fails", "result": "PASS" if bounds["forbidden_bound_as_source_control"]["anti_circularity_status"] == "FAIL_FORBIDDEN_SOURCE_USED" else "FAIL", "evidence": str(BOUND_OUTPUT_CSV)},
        {"check_id": "VAL4812_10_claim", "description": "claim register includes L-654 as nonclaim", "result": "PASS" if CLAIM_ID in read_text(CLAIMS_PATH) and DECISION in read_text(CLAIMS_PATH) else "FAIL", "evidence": str(CLAIMS_PATH)},
        {"check_id": "VAL4812_11_resume", "description": "resume points at 4813", "result": "PASS" if NEXT_TARGET in read_text(RESUME_PATH) else "FAIL", "evidence": str(RESUME_PATH)},
    ]
    checks.append({"check_id": "VAL4812_OVERALL", "description": "all 4812 domain/Stokes checks pass", "result": "PASS" if all(row["result"] == "PASS" for row in checks) else "FAIL", "evidence": DECISION})
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
    row = {"claim_id": CLAIM_ID, "domain": "local_gr", "claim": "boundary_cohomology_weighted_stokes_runner", "current_evidence": "4812 installs the boundary cohomology/domain certificate gate and executable weighted-Stokes edge-bound row; unit projected edge bound passes the current window but remains source-unsigned.", "status": "boundary_cohomology_weighted_stokes_private_nonclaim", "next_test": NEXT_TARGET, "key_risk": "Stokes zero without closed weight; harmonic deletion; corner silence; bound-as-source", "sector": "local_gr", "evidence": str(DOC_PATH), "next_action": NEXT_TARGET, "risk": "symbolic B_X exactness; unowned boundary domain; missing b_X norm; missing harmonic/residual bound; fitted edge bound", "title": "Boundary cohomology domain and weighted-Stokes source-row gate", "notes": f"{MARKER}; {DECISION}; generated {timestamp}"}
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        csv.DictWriter(handle, fieldnames=list(row)).writerow(row)


def update_registers(timestamp: str) -> None:
    append_claim(timestamp)
    append_once(SPINE_PATH, MARKER, f"""

## {MARKER}

4812 upgrades the edge-zero route to a weighted-Stokes condition:

```text
B_X = d_S b_X + h_X + r_X
integral_S F epsilon d_S b_X = corner - integral_S d_S(F epsilon) wedge b_X
|Q_edge| <= C_corner + ||d_S(F epsilon)||_* ||b_X||_* + |harmonic_edge| + |residual_edge|
|Qbar_edge_XH| <= ||Pi_M^H|| |Q_edge| / M_H_ref_min
```

This is progress because `Q_edge=0` now requires explicit domain/cohomology/kernel/primitive certificates; otherwise the edge is bounded term-by-term. The next hard object is the explicit `b_X` primitive from the parent variation.
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
Last checkpoint: `4812-Y5-R2FR-boundary-cohomology-domain-certificate-or-source-pack-first-row.md`
Marker: `{MARKER}`

## Where we are

4812 installed the boundary cohomology/domain and weighted-Stokes gate:

```text
B_X = d_S b_X + h_X + r_X
integral_S F epsilon d_S b_X = corner - integral_S d_S(F epsilon) wedge b_X
|Q_edge| <= C_corner + ||d_S(F epsilon)||_* ||b_X||_* + |harmonic_edge| + |residual_edge|
|Qbar_edge_XH| <= ||Pi_M^H|| |Q_edge| / M_H_ref_min
```

## Live blockers

- Boundary zero needs surface/corner, boundary class, cohomology, epsilon-domain, kernel-weight and `B_X` primitive certificates.
- Weighted-Stokes zero cannot ignore corner, harmonic, residual, or kernel-derivative terms.
- The first source-pack bound row still lacks source-backed `C_corner`, `norm_dS_Feps`, `norm_bX`, harmonic, residual, `Pi_M` norm and `M_H_ref_min` values.

## Next target

`{NEXT_TARGET}`
""", encoding="utf-8")


def write_docs(timestamp: str, target: dict[str, str], outputs: dict[str, list[dict[str, Any]]], validation: list[dict[str, Any]]) -> None:
    sources = read_csv(SOURCE_REGISTER_CSV)
    target_rows = read_csv(TARGET_AUDIT_CSV)
    doc = f"""# 4812 - Boundary cohomology domain certificate or source pack first row

Marker: `{MARKER}`
Generated: `{timestamp}`
Decision: `{DECISION}`

## Result

4812 turns edge exactness into a weighted-Stokes theorem plus executable fallback bound:

```text
B_X = d_S b_X + h_X + r_X
integral_S F epsilon d_S b_X = corner - integral_S d_S(F epsilon) wedge b_X
|Q_edge| <= C_corner + ||d_S(F epsilon)||_* ||b_X||_* + |harmonic_edge| + |residual_edge|
|Qbar_edge_XH| <= ||Pi_M^H|| |Q_edge| / M_H_ref_min
required: |Qbar_edge_XH| <= {target['required_abs_max']}
```

The exact zero route is sharper but not closed. The first executable bound row shows how a future source pack must be scored without pretending Stokes alone deletes the edge.

## Target Audit

{table(target_rows, ['audit_id', 'component_expr', 'required_abs_max', 'source', 'derivation', 'valid_for_claim', 'timestamp_utc'])}

## Source Register

{table(sources, ['source_id', 'source_path', 'exists', 'needle_found', 'role'])}

## Domain Certificate Output

{table(outputs['domains'], ['certificate_id', 'route', 'domain_status', 'domain_theorem', 'missing_domain_inputs', 'anti_circularity_status'])}

## Weighted Stokes Output

{table(outputs['stokes'], ['theorem_id', 'route', 'stokes_status', 'zero_theorem', 'missing_stokes_inputs', 'anti_circularity_status'])}

## Edge Bound First Row Output

{table(outputs['bounds'], ['row_id', 'quantity', 'Q_edge_bound_abs', 'Qbar_edge_XH_bound_abs', 'required_abs_max', 'numeric_window_pass', 'bound_status', 'missing_bound_inputs', 'anti_circularity_status'])}

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
    FORMAL_PATH.write_text(f"""# 828 - PPC4161 boundary cohomology domain certificate or source pack first row

Marker: `{MARKER}`
Generated: `{timestamp}`

4812 gives the edge branch a weighted-Stokes gate:

```text
B_X = d_S b_X + h_X + r_X
|Q_edge| <= C_corner + ||d_S(F epsilon)||_* ||b_X||_* + |harmonic_edge| + |residual_edge|
|Qbar_edge_XH| <= ||Pi_M^H|| |Q_edge| / M_H_ref_min
```

Unit projected edge bound gives `1.0 <= 5.256633029822351`, but physical promotion remains blocked until `b_X`, corner, harmonic, residual, kernel, `Pi_M`, and `M_H_ref` terms are parent-derived or source-backed. Next target: `{NEXT_TARGET}`.
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
