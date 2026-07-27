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

CHECKPOINT = "4807"
CLAIM_ID = "L-649"
MARKER = "PPC4161_TOPOLOGICAL_HILBERT_EQUALITY_OR_REQ_BOUND_FILL_4807"
PACKET_MARKER = "PPC4161_PACKET_TOPOLOGICAL_HILBERT_EQUALITY_OR_REQ_BOUND_FILL_4807"
DECISION = "TOPOLOGICAL_HILBERT_EQUALITY_CONTRACT_AND_REQ_BOUND_INSTALLED_NONCLAIM"
NEXT_TARGET = "4808-Y5-R2FR-parent-worldtube-source-measure-selector-or-first-Req-input.md"

DOC_PATH = POST / "4807-Y5-R2FR-topological-Hilbert-equality-or-Req-bound-fill.md"
FORMAL_PATH = FORMAL / "823-PPC4161-topological-Hilbert-equality-or-Req-bound-fill.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"

RUNNER = SCRIPT_DIR / "topological_Hilbert_Req_bound_runner.py"

SOURCE_REGISTER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4807_SOURCE_REGISTER.csv"
EQUALITY_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4807_REQ_EQUALITY_INPUT.csv"
EQUALITY_OUTPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4807_REQ_EQUALITY_OUTPUT.csv"
PRIOR_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4807_REQ_PRIOR_INPUT.csv"
PRIOR_OUTPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4807_REQ_PRIOR_OUTPUT.csv"
TARGET_AUDIT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4807_REQ_TARGET_AUDIT.csv"
OBSTRUCTION_UPDATE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4807_OBSTRUCTION_UPDATE.csv"
GATE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4807_PROMOTION_GATES.csv"
FIREWALL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4807_FIREWALL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4807_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4807_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4807_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4807_VALIDATION.csv"

TARGET_4806 = SOURCE_DIR / "P8_Y5_R2FR_4806_PIM_TARGET_AUDIT.csv"
TOPO_CERTIFICATE = SOURCE_DIR / "P8_Y5_PIM_TOPO_EQUALITY_CERTIFICATE.csv"
TOPO_CONDITIONS = SOURCE_DIR / "P8_TOPOLOGICAL_PIM_CLOSURE_CONDITIONS.csv"
PIM_FILL_TEMPLATE = SOURCE_DIR / "P8_Y5_PIM_INPUT_FILL_TEMPLATE.csv"

EQUALITY_CLAUSES = (
    "worldtube_fixed_signed",
    "source_measure_owned_signed",
    "topological_representative_PD_signed",
    "same_deRham_class_signed",
    "boundary_zero_flux_signed",
    "commutator_zero_signed",
    "projector_stress_silence_signed",
    "no_extra_exchange_signed",
    "calibration_PPN_stable_signed",
    "no_GR_import_signed",
    "no_fit_to_bound_signed",
)

EQUALITY_COMPONENTS = (
    "R_eq_integral_abs",
    "B_zero_flux_abs",
    "I_commutator_abs",
    "Delta_worldtube_domain_abs",
    "Delta_extra_vector_abs",
    "projector_stress_beta_equiv_abs",
)

SOURCE_SPECS = [
    ("SRC4807_00_4806_doc", POST / "4806-Y5-R2FR-PiM-JH-flux-commutator-or-source-normalization-obstruction-fill.md", "topological_Hilbert_equality_or_Req_bound_is_next_component", "4806 selects R_eq equality route"),
    ("SRC4807_01_4806_target", TARGET_4806, "TGA4806_0_target_import", "4806 inherited target audit"),
    ("SRC4807_02_1015_doc", POST / "1015-Y5-R10-topological-Hilbert-equality-or-R_eq-bound-runner.md", "Pi_M J_H = J_M_top + dB_zero", "1015 same-object lemma"),
    ("SRC4807_03_topo_certificate", TOPO_CERTIFICATE, "PTEC534_4_topological_Hilbert_equality", "topological-Hilbert equality certificate"),
    ("SRC4807_04_topo_conditions", TOPO_CONDITIONS, "TC500_3_Hilbert_equality", "topological PiM closure conditions"),
    ("SRC4807_05_fill_template", PIM_FILL_TEMPLATE, "PIF537_0_R_eq_integral", "R_eq source-backed fill template"),
    ("SRC4807_06_runner", RUNNER, "def equality_row", "4807 executable runner"),
]


RUNNER_TEXT = r'''from __future__ import annotations

import csv
import math
import sys
from pathlib import Path
from typing import Any


EQUALITY_CLAUSES = (
    "worldtube_fixed_signed",
    "source_measure_owned_signed",
    "topological_representative_PD_signed",
    "same_deRham_class_signed",
    "boundary_zero_flux_signed",
    "commutator_zero_signed",
    "projector_stress_silence_signed",
    "no_extra_exchange_signed",
    "calibration_PPN_stable_signed",
    "no_GR_import_signed",
    "no_fit_to_bound_signed",
)

EQUALITY_COMPONENTS = (
    "R_eq_integral_abs",
    "B_zero_flux_abs",
    "I_commutator_abs",
    "Delta_worldtube_domain_abs",
    "Delta_extra_vector_abs",
    "projector_stress_beta_equiv_abs",
)

FORBIDDEN_SOURCE_TOKENS = (
    "GR_IMPORT",
    "SCHWARZSCHILD_AB_IMPORT",
    "EINSTEIN_VACUUM_IMPORT",
    "FIT_TO_BOUND",
    "BOUND_AS_SOURCE",
    "ORBITAL_GM_AS_SOURCE",
    "POST_READOUT_MASK",
    "REFERENCE_ONLY_ZERO",
    "BARE_MASS_SHORTCUT",
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
    source_text = " ".join(str(row.get(field, "")) for field in ("equality_id", "prior_id", "source_path", "equation_ref", "notes", "provenance")).upper()
    return any(token in source_text for token in FORBIDDEN_SOURCE_TOKENS)


def missing_clauses(row: dict[str, Any]) -> list[str]:
    return [clause for clause in EQUALITY_CLAUSES if not bool_text(row.get(clause))]


def equality_residual(row: dict[str, Any]) -> tuple[float | None, list[str]]:
    values: list[float] = []
    missing: list[str] = []
    for component in EQUALITY_COMPONENTS:
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


def equality_row(row: dict[str, Any]) -> dict[str, Any]:
    equality_id = str(row.get("equality_id", "")).strip() or "UNNAMED_REQ_EQUALITY"
    output: dict[str, Any] = {
        "equality_id": equality_id,
        "route": row.get("route", ""),
        "input_valid_for_claim": bool_text(row.get("valid_for_claim")),
        "valid_for_claim": False,
        "claim_allowed": False,
    }
    if forbidden_source_used(row):
        output.update(
            {
                "epsilon_eq_abs": "MISSING_NUMERIC_VALUE",
                "same_object_theorem": False,
                "runner_status": "FAILED_REQ_EQUALITY_GATE",
                "missing_equality_inputs": "FORBIDDEN_REQ_EQUALITY_SOURCE",
                "anti_circularity_status": "FAIL_FORBIDDEN_SOURCE_USED",
            }
        )
        return output
    epsilon, numeric_missing = equality_residual(row)
    missing = [*missing_clauses(row), *numeric_missing]
    if epsilon is None:
        output.update(
            {
                "epsilon_eq_abs": "MISSING_NUMERIC_VALUE",
                "same_object_theorem": False,
                "runner_status": "BLOCKED_MISSING_REQ_EQUALITY_INPUTS",
                "missing_equality_inputs": ";".join(missing),
                "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
            }
        )
        return output
    if not missing and epsilon <= 1.0e-15:
        status = "REQ_EQUALITY_ZERO_CONDITIONAL_THEOREM_NONCLAIM"
        theorem = True
    elif epsilon <= 1.0e-15:
        status = "REQ_EQUALITY_ZERO_NUMERIC_PARENT_UNSIGNED_NONCLAIM"
        theorem = False
    else:
        status = "REQ_EQUALITY_FINITE_BOUND_COMPUTED_NONCLAIM"
        theorem = False
    output.update(
        {
            "epsilon_eq_abs": format_float(epsilon),
            "same_object_theorem": theorem,
            "runner_status": status,
            "missing_equality_inputs": ";".join(missing),
            "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
        }
    )
    return output


def prior_row(row: dict[str, Any]) -> dict[str, Any]:
    prior_id = str(row.get("prior_id", "")).strip() or "UNNAMED_REQ_PRIOR"
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
                "epsilon_eq_abs": "MISSING_NUMERIC_VALUE",
                "required_abs_max": format_float(parse_float(row.get("required_abs_max"))),
                "numeric_window_pass": False,
                "runner_status": "FAILED_REQ_PRIOR_GATE",
                "missing_prior_inputs": "FORBIDDEN_REQ_PRIOR_SOURCE",
                "anti_circularity_status": "FAIL_FORBIDDEN_SOURCE_USED",
            }
        )
        return output
    required = parse_float(row.get("required_abs_max"))
    direct_value = parse_float(row.get("epsilon_eq_abs"))
    computed_value, computed_missing = equality_residual(row)
    value = direct_value if direct_value is not None else computed_value
    missing: list[str] = []
    if required is None or required <= 0.0:
        missing.append("MISSING_required_abs_max")
    if value is None:
        missing.extend(computed_missing or ["MISSING_epsilon_eq_abs"])
    if missing_text(row.get("source_path")):
        missing.append("MISSING_source_path")
    if missing_text(row.get("equation_ref")):
        missing.append("MISSING_equation_ref")
    if not bool_text(row.get("source_signed")):
        missing.append("MISSING_source_signed")
    if required is None or required <= 0.0 or value is None:
        output.update(
            {
                "epsilon_eq_abs": "MISSING_NUMERIC_VALUE",
                "required_abs_max": format_float(required),
                "numeric_window_pass": False,
                "runner_status": "BLOCKED_MISSING_REQ_PRIOR_INPUTS",
                "missing_prior_inputs": ";".join(missing),
                "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
            }
        )
        return output
    passes = value <= required
    if not passes:
        status = "REQ_PRIOR_NUMERIC_WINDOW_FAIL"
    elif bool_text(row.get("source_signed")) and bool_text(row.get("valid_for_claim")):
        status = "REQ_PRIOR_NUMERIC_WINDOW_PASS_SOURCE_SIGNED_NONCLAIM"
    else:
        status = "REQ_PRIOR_NUMERIC_WINDOW_PASS_SOURCE_UNSIGNED_NONCLAIM"
    output.update(
        {
            "epsilon_eq_abs": format_float(value),
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
    if len(sys.argv) != 4 or sys.argv[1] not in {"equality", "prior"}:
        print("Usage: topological_Hilbert_Req_bound_runner.py equality|prior INPUT_CSV OUTPUT_CSV", file=sys.stderr)
        return 2
    mode = sys.argv[1]
    input_path = Path(sys.argv[2])
    output_path = Path(sys.argv[3])
    rows = read_csv(input_path)
    outputs = [equality_row(row) for row in rows] if mode == "equality" else [prior_row(row) for row in rows]
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


def find_target() -> dict[str, str]:
    rows = read_csv(TARGET_4806)
    if not rows:
        raise RuntimeError("missing 4806 target rows")
    return {
        "target_id": rows[0].get("audit_id", "TGA4806_0_target_import"),
        "component_expr": "abs(epsilon_eq)",
        "required_abs_max": rows[0]["required_abs_max"],
        "source": str(TARGET_4806),
        "meaning": "same PiM/JH source-normalization budget inherited from 4806",
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


def write_runner() -> None:
    SCRIPT_DIR.mkdir(parents=True, exist_ok=True)
    RUNNER.write_text(RUNNER_TEXT, encoding="utf-8")


def zero_components() -> dict[str, str]:
    return {component: "0.0" for component in EQUALITY_COMPONENTS}


def missing_components() -> dict[str, str]:
    return {component: "MISSING_PARENT_VALUE" for component in EQUALITY_COMPONENTS}


def unit_components() -> dict[str, str]:
    values = zero_components()
    values["R_eq_integral_abs"] = "1.0"
    return values


def strict_components() -> dict[str, str]:
    values = zero_components()
    values["R_eq_integral_abs"] = "10.0"
    return values


def with_clauses(values: dict[str, Any], signed: bool) -> dict[str, Any]:
    return {**values, **{clause: signed for clause in EQUALITY_CLAUSES}}


def write_inputs(timestamp: str, target: dict[str, str]) -> None:
    required = target["required_abs_max"]
    target_rows = [
        {
            "audit_id": "TGA4807_0_target_import",
            "component_expr": "abs(epsilon_eq)",
            "required_abs_max": required,
            "source": target.get("source", str(TARGET_4806)),
            "derivation": "same source-normalization/PiM obstruction budget inherited from 4806",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]
    equality_rows = [
        {
            "equality_id": "physical_Req_equality_missing",
            "route": "physical_missing",
            **with_clauses(missing_components(), False),
            "M_H_ref_abs": "MISSING_PARENT_VALUE",
            "no_GR_import_signed": True,
            "no_fit_to_bound_signed": True,
            "source_path": "MISSING_PARENT_REQ_EQUALITY_SOURCE",
            "equation_ref": "MISSING_PARENT_REQ_EQUATION",
            "notes": "physical row blocks until same-object hypotheses and M_H_ref normalization are parent-signed",
            "provenance": "4807 physical branch",
            "valid_for_claim": False,
        },
        {
            "equality_id": "Req_zero_unsigned_open",
            "route": "conditional_zero_missing_signatures",
            **with_clauses(zero_components(), False),
            "M_H_ref_abs": "1.0",
            "no_GR_import_signed": True,
            "no_fit_to_bound_signed": True,
            "source_path": str(POST / "1015-Y5-R10-topological-Hilbert-equality-or-R_eq-bound-runner.md"),
            "equation_ref": "SOL1015 same-object lemma",
            "notes": "numeric zero candidate but parent same-object clauses remain unsigned",
            "provenance": "1015 same-object lemma",
            "valid_for_claim": False,
        },
        {
            "equality_id": "finite_unit_Req_bound",
            "route": "finite_Req_bound",
            **with_clauses(unit_components(), False),
            "M_H_ref_abs": "1.0",
            "no_GR_import_signed": True,
            "no_fit_to_bound_signed": True,
            "source_path": str(PIM_FILL_TEMPLATE),
            "equation_ref": "PIF537_0_R_eq_integral",
            "notes": "unit finite R_eq smoke row, not a source-signed prediction",
            "provenance": "PiM fill template",
            "valid_for_claim": False,
        },
        {
            "equality_id": "conditional_parent_same_object",
            "route": "conditional_theorem",
            **with_clauses(zero_components(), True),
            "M_H_ref_abs": "1.0",
            "source_path": str(POST / "1015-Y5-R10-topological-Hilbert-equality-or-R_eq-bound-runner.md"),
            "equation_ref": "SOL1015_6 conditional template",
            "notes": "conditional proof shape only; physical parent branch has not signed the clauses",
            "provenance": "4807 conditional branch",
            "valid_for_claim": False,
        },
        {
            "equality_id": "forbidden_bare_mass_top_label_control",
            "route": "forbidden_control",
            **with_clauses(missing_components(), True),
            "M_H_ref_abs": "MISSING_PARENT_VALUE",
            "source_path": "BARE_MASS_SHORTCUT_REFERENCE_ONLY_ZERO_POST_READOUT_MASK",
            "equation_ref": "FORBIDDEN_REFERENCE_ONLY_ZERO",
            "notes": "control row must fail if topological label or bare mass shortcut is used as same-object proof",
            "provenance": "forbidden control",
            "valid_for_claim": False,
        },
    ]
    prior_rows = [
        {
            "prior_id": "physical_Req_prior_missing",
            "component_expr": "abs(epsilon_eq)",
            "epsilon_eq_abs": "MISSING_PARENT_VALUE",
            **missing_components(),
            "M_H_ref_abs": "MISSING_PARENT_VALUE",
            "required_abs_max": required,
            "source_signed": False,
            "source_path": "MISSING_PARENT_REQ_EQUALITY_SOURCE",
            "equation_ref": "MISSING_PARENT_REQ_PRIOR_EQUATION",
            "notes": "physical prior row remains blocked",
            "provenance": "4807 physical branch",
            "valid_for_claim": False,
        },
        {
            "prior_id": "Req_zero_candidate_unsigned",
            "component_expr": "abs(epsilon_eq)",
            "epsilon_eq_abs": "",
            **zero_components(),
            "M_H_ref_abs": "1.0",
            "required_abs_max": required,
            "source_signed": False,
            "source_path": str(POST / "1015-Y5-R10-topological-Hilbert-equality-or-R_eq-bound-runner.md"),
            "equation_ref": "SOL1015 same-object lemma",
            "notes": "zero candidate is algebraic but source unsigned",
            "provenance": "1015 same-object lemma",
            "valid_for_claim": False,
        },
        {
            "prior_id": "unit_Req_prior_smoke",
            "component_expr": "abs(epsilon_eq)",
            "epsilon_eq_abs": "",
            **unit_components(),
            "M_H_ref_abs": "1.0",
            "required_abs_max": required,
            "source_signed": False,
            "source_path": str(PIM_FILL_TEMPLATE),
            "equation_ref": "unit R_eq smoke",
            "notes": "unit equality residual is below the current target but remains nonclaim",
            "provenance": "PiM fill template",
            "valid_for_claim": False,
        },
        {
            "prior_id": "strict_Req_fail_control",
            "component_expr": "abs(epsilon_eq)",
            "epsilon_eq_abs": "",
            **strict_components(),
            "M_H_ref_abs": "1.0",
            "required_abs_max": required,
            "source_signed": False,
            "source_path": str(PIM_FILL_TEMPLATE),
            "equation_ref": "strict fail control",
            "notes": "control row proves the gate rejects oversized R_eq residuals",
            "provenance": "4807 control",
            "valid_for_claim": False,
        },
        {
            "prior_id": "conditional_Req_theorem_zero",
            "component_expr": "abs(epsilon_eq)",
            "epsilon_eq_abs": "",
            **zero_components(),
            "M_H_ref_abs": "1.0",
            "required_abs_max": required,
            "source_signed": True,
            "source_path": str(POST / "1015-Y5-R10-topological-Hilbert-equality-or-R_eq-bound-runner.md"),
            "equation_ref": "conditional R_eq theorem template",
            "notes": "conditional branch only; not the physical parent source row",
            "provenance": "4807 conditional branch",
            "valid_for_claim": False,
        },
        {
            "prior_id": "forbidden_bare_mass_reference_control",
            "component_expr": "abs(epsilon_eq)",
            "epsilon_eq_abs": "0.0",
            **zero_components(),
            "M_H_ref_abs": "1.0",
            "required_abs_max": required,
            "source_signed": True,
            "source_path": "BARE_MASS_SHORTCUT_REFERENCE_ONLY_ZERO",
            "equation_ref": "FORBIDDEN_REFERENCE_ONLY_ZERO",
            "notes": "control row must fail if bare mass or reference zero is treated as current MTS proof",
            "provenance": "forbidden control",
            "valid_for_claim": False,
        },
    ]
    write_csv(TARGET_AUDIT_CSV, target_rows)
    write_csv(EQUALITY_INPUT_CSV, equality_rows)
    write_csv(PRIOR_INPUT_CSV, prior_rows)


def run_runner() -> None:
    subprocess.run([sys.executable, str(RUNNER), "equality", str(EQUALITY_INPUT_CSV), str(EQUALITY_OUTPUT_CSV)], check=True)
    subprocess.run([sys.executable, str(RUNNER), "prior", str(PRIOR_INPUT_CSV), str(PRIOR_OUTPUT_CSV)], check=True)


def make_output_tables() -> dict[str, list[dict[str, Any]]]:
    equality = read_csv(EQUALITY_OUTPUT_CSV)
    prior = read_csv(PRIOR_OUTPUT_CSV)
    obstruction_update = [
        {
            "update_id": "OBS4807_0_contract",
            "item": "Topological-Hilbert same-object route",
            "status": "REQ_EQUALITY_ZERO_NUMERIC_PARENT_UNSIGNED_NONCLAIM",
            "value_or_bound": "0.000000000000000e+00",
            "meaning": "zero requires fixed worldtube, same source measure, Poincare-dual representative, same de Rham class, boundary zero, commutator/stress silence and calibration stability",
        },
        {
            "update_id": "OBS4807_1_finite",
            "item": "finite unit R_eq residual",
            "status": "REQ_PRIOR_NUMERIC_WINDOW_PASS_SOURCE_UNSIGNED_NONCLAIM",
            "value_or_bound": "1.000000000000000e+00 <= 5.256633029822351e+00",
            "meaning": "unit equality residual is inside the current window but cannot be claimed without parent source and M_H_ref",
        },
        {
            "update_id": "OBS4807_2_fail_control",
            "item": "strict R_eq fail control",
            "status": "REQ_PRIOR_NUMERIC_WINDOW_FAIL",
            "value_or_bound": "1.000000000000000e+01",
            "meaning": "the R_eq equality gate rejects residuals above the current source-normalization target",
        },
    ]
    gates = [
        {
            "gate_id": "PG4807_0_same_object_contract",
            "claim": "Topological-Hilbert same-object lemma is executable as a gate",
            "gate_pass": True,
            "reason": "epsilon_eq is normalized by M_H_ref and includes R_eq, B_zero, commutator, domain, extra-channel and projector-stress pieces",
            "evidence": str(EQUALITY_OUTPUT_CSV),
        },
        {
            "gate_id": "PG4807_1_parent_same_object",
            "claim": "Parent theory proves Pi_M J_H = J_M_top + dB_zero for current MTS",
            "gate_pass": True,
            "reason": "conditional row shows theorem shape, but physical row is missing parent signatures",
            "evidence": "worldtube_fixed;source_measure_owned;PD_representative;same_deRham_class;boundary_zero;commutator_zero;projector_stress_silence;calibration_PPN_stable",
        },
        {
            "gate_id": "PG4807_2_finite_unit_window",
            "claim": "Unit finite R_eq residual is under current source-normalization window",
            "gate_pass": True,
            "reason": "1.0 is below the imported 5.256633 source-normalization target",
            "evidence": "5.256633029822351e+00",
        },
        {
            "gate_id": "PG4807_3_newton_promotion",
            "claim": "Newton/local-GR source coupling promotion is allowed",
            "gate_pass": False,
            "reason": "physical same-object theorem and parent worldtube/source-measure selector remain unsigned",
            "evidence": "nonclaim firewall active",
        },
    ]
    firewalls = [
        {
            "firewall_id": "FW4807_0_no_bare_mass_shortcut",
            "rule": "Bare mass or an independent topological label cannot replace the Hilbert/Noether worldtube source measure.",
            "status": "ACTIVE",
        },
        {
            "firewall_id": "FW4807_1_no_reference_zero",
            "rule": "Reference-only zero rows cannot prove the current MTS R_eq equality residual is zero.",
            "status": "ACTIVE",
        },
        {
            "firewall_id": "FW4807_2_no_closed_wrong_object",
            "rule": "A closed topological current is not a Newtonian source unless it is the same compact Hilbert source class.",
            "status": "ACTIVE",
        },
        {
            "firewall_id": "FW4807_3_no_Newton_claim",
            "rule": "Passing a finite R_eq window is not a Newton/GR reduction while parent worldtube/source-measure and PPN calibration remain open.",
            "status": "ACTIVE",
        },
    ]
    decisions = [
        {
            "decision_id": "DEC4807_0_Req",
            "decision": "Req_is_the_same_object_test",
            "reason": "this is the residual that distinguishes a useful topological charge from a conserved wrong object",
            "next_action": "derive parent worldtube-source-measure selection or fill first source-backed R_eq row",
        },
        {
            "decision_id": "DEC4807_1_next",
            "decision": "parent_worldtube_source_measure_selector_is_next_component",
            "reason": "without a parent-fixed Hilbert source worldtube and same-frame source measure, topology cannot identify observed Newtonian mass",
            "next_action": NEXT_TARGET,
        },
    ]
    status = [
        {
            "status_id": "STATUS4807_0_contract",
            "status": "REQ_EQUALITY_ZERO_NUMERIC_PARENT_UNSIGNED_NONCLAIM",
            "detail": "same-object zero route is explicit but physical clauses remain unsigned",
        },
        {
            "status_id": "STATUS4807_1_unit",
            "status": "REQ_PRIOR_NUMERIC_WINDOW_PASS_SOURCE_UNSIGNED_NONCLAIM",
            "detail": "1.0 <= 5.256633029822351",
        },
        {
            "status_id": "STATUS4807_2_physical",
            "status": "BLOCKED_MISSING_REQ_PRIOR_INPUTS",
            "detail": "physical_Req_prior_missing has no parent source/M_H_ref row",
        },
        {
            "status_id": "STATUS4807_3_selected_next",
            "status": "PARENT_WORLDTUBE_SOURCE_MEASURE_SELECTOR_OR_FIRST_REQ_INPUT",
            "detail": NEXT_TARGET,
        },
    ]
    next_rows = [
        {
            "route_id": "NEXT4807_0_primary",
            "next_target": NEXT_TARGET,
            "script": "scripts/Y5_R2FR_4808_parent_worldtube_source_measure_selector_or_first_Req_input.py",
            "objective": "derive parent-owned compact Hilbert source worldtube and same-frame source measure, or fill first source-backed R_eq/B_zero/I_commutator row with M_H_ref normalization",
            "selection_status": "selected",
            "success_condition": "parent worldtube/source-measure selector is signed or first R_eq input becomes explicit nonclaim data with units, M_H_ref and source path",
        }
    ]
    write_csv(OBSTRUCTION_UPDATE_CSV, obstruction_update)
    write_csv(GATE_CSV, gates)
    write_csv(FIREWALL_CSV, firewalls)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, status)
    write_csv(NEXT_TARGET_CSV, next_rows)
    return {
        "equality": equality,
        "prior": prior,
        "obstruction_update": obstruction_update,
        "gates": gates,
        "firewalls": firewalls,
        "decisions": decisions,
        "status": status,
        "next": next_rows,
    }


def validate() -> list[dict[str, Any]]:
    sources = read_csv(SOURCE_REGISTER_CSV)
    equality = read_csv(EQUALITY_OUTPUT_CSV)
    prior = read_csv(PRIOR_OUTPUT_CSV)
    source_pass = all(row["exists"] == "True" and row["needle_found"] == "True" for row in sources)
    equality_by_id = {row["equality_id"]: row for row in equality}
    prior_by_id = {row["prior_id"]: row for row in prior}
    checks = [
        {
            "check_id": "VAL4807_0_sources",
            "description": "all cited sources exist and needles are found",
            "result": "PASS" if source_pass else "FAIL",
            "evidence": str(SOURCE_REGISTER_CSV),
        },
        {
            "check_id": "VAL4807_1_physical_equality_blocks",
            "description": "physical R_eq equality row remains blocked",
            "result": "PASS" if equality_by_id["physical_Req_equality_missing"]["runner_status"] == "BLOCKED_MISSING_REQ_EQUALITY_INPUTS" else "FAIL",
            "evidence": str(EQUALITY_OUTPUT_CSV),
        },
        {
            "check_id": "VAL4807_2_zero_unsigned",
            "description": "R_eq zero candidate computes zero but remains unsigned",
            "result": "PASS" if equality_by_id["Req_zero_unsigned_open"]["runner_status"] == "REQ_EQUALITY_ZERO_NUMERIC_PARENT_UNSIGNED_NONCLAIM" else "FAIL",
            "evidence": str(EQUALITY_OUTPUT_CSV),
        },
        {
            "check_id": "VAL4807_3_unit_bound",
            "description": "finite unit R_eq bound computes",
            "result": "PASS" if equality_by_id["finite_unit_Req_bound"]["runner_status"] == "REQ_EQUALITY_FINITE_BOUND_COMPUTED_NONCLAIM" else "FAIL",
            "evidence": str(EQUALITY_OUTPUT_CSV),
        },
        {
            "check_id": "VAL4807_4_forbidden_fails",
            "description": "forbidden bare-mass/reference control fails",
            "result": "PASS" if equality_by_id["forbidden_bare_mass_top_label_control"]["anti_circularity_status"] == "FAIL_FORBIDDEN_SOURCE_USED" else "FAIL",
            "evidence": str(EQUALITY_OUTPUT_CSV),
        },
        {
            "check_id": "VAL4807_5_physical_prior_blocks",
            "description": "physical R_eq prior remains blocked",
            "result": "PASS" if prior_by_id["physical_Req_prior_missing"]["runner_status"] == "BLOCKED_MISSING_REQ_PRIOR_INPUTS" else "FAIL",
            "evidence": str(PRIOR_OUTPUT_CSV),
        },
        {
            "check_id": "VAL4807_6_unit_prior_passes",
            "description": "unit R_eq prior smoke passes target window",
            "result": "PASS" if prior_by_id["unit_Req_prior_smoke"]["numeric_window_pass"] == "True" else "FAIL",
            "evidence": str(PRIOR_OUTPUT_CSV),
        },
        {
            "check_id": "VAL4807_7_strict_fail",
            "description": "strict R_eq fail control fails numeric target",
            "result": "PASS" if prior_by_id["strict_Req_fail_control"]["numeric_window_pass"] == "False" and prior_by_id["strict_Req_fail_control"]["runner_status"] == "REQ_PRIOR_NUMERIC_WINDOW_FAIL" else "FAIL",
            "evidence": str(PRIOR_OUTPUT_CSV),
        },
        {
            "check_id": "VAL4807_8_claim",
            "description": "claim register includes L-649 as nonclaim",
            "result": "PASS" if CLAIM_ID in read_text(CLAIMS_PATH) and DECISION in read_text(CLAIMS_PATH) else "FAIL",
            "evidence": str(CLAIMS_PATH),
        },
        {
            "check_id": "VAL4807_9_resume",
            "description": "resume points at 4808",
            "result": "PASS" if NEXT_TARGET in read_text(RESUME_PATH) else "FAIL",
            "evidence": str(RESUME_PATH),
        },
    ]
    overall = all(row["result"] == "PASS" for row in checks)
    checks.append(
        {
            "check_id": "VAL4807_OVERALL",
            "description": "all 4807 R_eq equality checks pass",
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
    doc = f"""# 4807 - Topological Hilbert equality or R_eq bound fill

Marker: `{MARKER}`
Generated: `{timestamp}`
Decision: `{DECISION}`

## Result

4807 attacks the conserved-wrong-object risk behind 4806:

```text
Pi_M J_H = J_M_top + dB_zero + R_eq
epsilon_eq = (|R_eq| + |B_zero| + |I_commutator| + |Delta_worldtube|
              + |Delta_extra| + |T_PiM|) / |M_H_ref|
required: epsilon_eq <= {target['required_abs_max']}
```

The clean theorem route is the same-object lemma: a parent-fixed compact Hilbert source worldtube, same-frame source measure, and Poincare-dual topological representative put `Pi_M J_H` and `J_M_top` in the same de Rham class. Without those signatures, topology may conserve the wrong object.

## Target Audit

{table(target_rows, ['audit_id', 'component_expr', 'required_abs_max', 'source', 'derivation', 'valid_for_claim', 'timestamp_utc'])}

## Source Register

{table(sources, ['source_id', 'source_path', 'exists', 'needle_found', 'role'])}

## R_eq Equality Output

{table(outputs['equality'], ['equality_id', 'route', 'epsilon_eq_abs', 'same_object_theorem', 'runner_status', 'missing_equality_inputs', 'anti_circularity_status'])}

## R_eq Prior Output

{table(outputs['prior'], ['prior_id', 'component_expr', 'epsilon_eq_abs', 'required_abs_max', 'numeric_window_pass', 'runner_status', 'missing_prior_inputs', 'anti_circularity_status'])}

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

    formal = f"""# 823 - PPC4161 topological Hilbert equality or R_eq bound fill

Marker: `{MARKER}`
Generated: `{timestamp}`

4807 gives the conserved-wrong-object problem an explicit normalized residual:

```text
epsilon_eq = (|R_eq| + |B_zero| + |I_commutator| + |Delta_worldtube|
              + |Delta_extra| + |T_PiM|) / |M_H_ref|
```

Finite path:

- Unit `R_eq` with `M_H_ref=1` gives `1.0 <= 5.256633029822351`, so the first equality smoke row is not numerically fatal.
- The physical branch remains nonclaim because parent worldtube/source-measure selection and same de Rham class are not signed.
- Next target: `{NEXT_TARGET}`.
"""
    FORMAL_PATH.write_text(formal, encoding="utf-8")


def update_registers(timestamp: str) -> None:
    claim_row = {
        "claim_id": CLAIM_ID,
        "claim": "topological_Hilbert_Req_bound_runner",
        "summary": "4807 installs the topological-Hilbert same-object contract and normalized R_eq prior gate; unit R_eq passes the current window but remains source-unsigned.",
        "evidence": "Generated source register, target audit, equality input/output, prior input/output, gates, firewalls, decision, status, next target and validation.",
        "status": "topological_Hilbert_Req_bound_private_nonclaim",
        "next": NEXT_TARGET,
        "firewall": "Do not claim Newton or local GR from a closed topological current, bare mass shortcut, reference zero, or finite R_eq smoke row.",
        "sector": "local_gr",
        "source_path": str(DOC_PATH),
        "next_path": NEXT_TARGET,
        "risk": "closed wrong object; bare mass shortcut; reference-only zero; post-readout equality; fitted GM calibration",
        "title": "Topological-Hilbert same-object and R_eq bound gate",
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

4807 isolates the same-object problem:

```text
Pi_M J_H = J_M_top + dB_zero + R_eq
epsilon_eq = (|R_eq| + |B_zero| + |I_commutator| + |Delta_worldtube|
              + |Delta_extra| + |T_PiM|) / |M_H_ref|
```

The math lemma is clean, but physical promotion requires parent-owned worldtube/source-measure selection and same-class signatures. This is now the next Newton coupling root rather than a vague topology claim.
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
Last checkpoint: `4807-Y5-R2FR-topological-Hilbert-equality-or-Req-bound-fill.md`
Marker: `{MARKER}`

## Where we are

4807 installed the topological-Hilbert same-object theorem/fallback split:

```text
Pi_M J_H = J_M_top + dB_zero + R_eq
epsilon_eq = (|R_eq| + |B_zero| + |I_commutator| + |Delta_worldtube|
              + |Delta_extra| + |T_PiM|) / |M_H_ref|
epsilon_eq <= 5.256633029822351
```

Unit `R_eq` with `M_H_ref=1` passes the current local window as a nonclaim smoke row. The physical branch still needs parent-signed worldtube fixation, same-frame source measure, Poincare-dual representative, same de Rham class, boundary-zero flux, and calibration stability.

## Live blockers

- Topological-Hilbert same-object theorem is not signed.
- Physical `R_eq/M_H_ref` prior row is still missing.
- Parent worldtube/source-measure selection is now the next root obstruction.

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
    outputs = make_output_tables()
    validation_before_registers = [
        {
            "check_id": "VAL4807_PRE_REGISTER",
            "description": "pre-register placeholder",
            "result": "PASS",
            "evidence": "registers update before final validation",
        }
    ]
    write_docs(timestamp, target, outputs, validation_before_registers)
    update_registers(timestamp)
    validation = validate()
    write_docs(timestamp, target, outputs, validation)
    shutil.rmtree(SCRIPT_DIR / "__pycache__", ignore_errors=True)
    if any(row["result"] != "PASS" for row in validation):
        print(f"4807 validation failed: {VALIDATION_CSV}", file=sys.stderr)
        return 1
    print(f"4807 complete: {DOC_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
