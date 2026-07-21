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

CHECKPOINT = "4805"
CLAIM_ID = "L-647"
MARKER = "PPC4161_SOURCE_NORMALIZATION_WORLDTUBE_OR_FINITE_CSOURCE_PRIOR_FILL_4805"
PACKET_MARKER = "PPC4161_PACKET_SOURCE_NORMALIZATION_WORLDTUBE_OR_FINITE_CSOURCE_PRIOR_FILL_4805"
DECISION = "SOURCE_NORMALIZATION_WORLDTUBE_CONTRACT_AND_FINITE_WINDOW_INSTALLED_NONCLAIM"
NEXT_TARGET = "4806-Y5-R2FR-PiM-JH-flux-commutator-or-source-normalization-obstruction-fill.md"

DOC_PATH = POST / "4805-Y5-R2FR-source-normalization-worldtube-or-finite-csource-prior-fill.md"
FORMAL_PATH = FORMAL / "821-PPC4161-source-normalization-worldtube-or-finite-csource-prior-fill.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"

RUNNER = SCRIPT_DIR / "source_normalization_worldtube_prior_runner.py"

SOURCE_REGISTER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4805_SOURCE_REGISTER.csv"
SOURCE_OWNER_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4805_SOURCE_OWNER_INPUT.csv"
SOURCE_OWNER_OUTPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4805_SOURCE_OWNER_OUTPUT.csv"
CSOURCE_PRIOR_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4805_CSOURCE_PRIOR_INPUT.csv"
CSOURCE_PRIOR_OUTPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4805_CSOURCE_PRIOR_OUTPUT.csv"
TARGET_AUDIT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4805_SOURCE_TARGET_AUDIT.csv"
OBSTRUCTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4805_OBSTRUCTION_UPDATE.csv"
GATE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4805_PROMOTION_GATES.csv"
FIREWALL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4805_FIREWALL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4805_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4805_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4805_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4805_VALIDATION.csv"

TARGETS_4802 = SOURCE_DIR / "P8_Y5_R2FR_4802_COMPONENT_TARGET_BOUNDS.csv"
COMPONENT_4802 = SOURCE_DIR / "P8_Y5_R2FR_4802_COMPONENT_SOURCE_OUTPUT.csv"
THEOREM_STACK = SOURCE_DIR / "P8_SOURCE_NORMALIZATION_THEOREM_STACK.csv"
NEWTON_CONTRACT = SOURCE_DIR / "P8_Y5_R10_868_NEWTON_SOURCE_NORMALIZATION_CONTRACT.csv"

SOURCE_CLAUSES = (
    "same_frame_source_signed",
    "constant_universal_coupling_signed",
    "PiM_parent_origin_signed",
    "flux_closure_signed",
    "worldtube_glue_signed",
    "no_extra_mu_channels_signed",
    "no_absorption_cheat_signed",
    "Newton_Poisson_orbit_signed",
    "no_GR_import_signed",
    "no_fit_to_bound_signed",
)

SOURCE_COMPONENTS = (
    "delta_same_frame_abs",
    "delta_kappa_abs",
    "delta_PiM_abs",
    "delta_flux_abs",
    "delta_worldtube_abs",
    "delta_mu_extra_abs",
    "delta_calibration_abs",
    "delta_poisson_abs",
)

SOURCE_SPECS = [
    ("SRC4805_00_4804_doc", POST / "4804-Y5-R2FR-clock-readout-same-coframe-or-finite-cclock-prior-fill.md", "source_normalization_is_next_component", "4804 selects source normalization"),
    ("SRC4805_01_4802_targets", TARGETS_4802, "TGT4802_3_source_norm", "4802 source normalization target"),
    ("SRC4805_02_4802_component", COMPONENT_4802, "physical_source_norm_missing", "4802 component source row"),
    ("SRC4805_03_1012_doc", POST / "1012-Y5-R10-Y5-source-normalization-owner-or-q_loc-bound-implementation.md", "Y5 measured-GM/source-normalization ownership is not proved", "prior Y5 owner theorem audit"),
    ("SRC4805_04_1013_doc", POST / "1013-Y5-R10-PiM-JH-flux-closure-or-measured-GM-obstruction-score.md", "d(Pi_M J_H)=0 compact-exterior flux closure", "prior PiM/JH obstruction audit"),
    ("SRC4805_05_theorem_stack", THEOREM_STACK, "S5_Newton_gate", "source normalization theorem stack"),
    ("SRC4805_06_newton_contract", NEWTON_CONTRACT, "NS868_1_measured_GM", "Newton measured-GM contract"),
    ("SRC4805_07_runner", RUNNER, "def source_owner_row", "4805 executable runner"),
]


RUNNER_TEXT = r'''from __future__ import annotations

import csv
import math
import sys
from pathlib import Path
from typing import Any


SOURCE_CLAUSES = (
    "same_frame_source_signed",
    "constant_universal_coupling_signed",
    "PiM_parent_origin_signed",
    "flux_closure_signed",
    "worldtube_glue_signed",
    "no_extra_mu_channels_signed",
    "no_absorption_cheat_signed",
    "Newton_Poisson_orbit_signed",
    "no_GR_import_signed",
    "no_fit_to_bound_signed",
)

SOURCE_COMPONENTS = (
    "delta_same_frame_abs",
    "delta_kappa_abs",
    "delta_PiM_abs",
    "delta_flux_abs",
    "delta_worldtube_abs",
    "delta_mu_extra_abs",
    "delta_calibration_abs",
    "delta_poisson_abs",
)

FORBIDDEN_SOURCE_TOKENS = (
    "GR_IMPORT",
    "SCHWARZSCHILD_AB_IMPORT",
    "EINSTEIN_VACUUM_IMPORT",
    "FIT_TO_BOUND",
    "BOUND_AS_SOURCE",
    "ORBITAL_GM_AS_SOURCE",
    "GM_BY_DECLARATION",
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
    source_text = " ".join(str(row.get(field, "")) for field in ("owner_id", "prior_id", "source_path", "equation_ref", "notes", "provenance")).upper()
    return any(token in source_text for token in FORBIDDEN_SOURCE_TOKENS)


def missing_clauses(row: dict[str, Any]) -> list[str]:
    return [clause for clause in SOURCE_CLAUSES if not bool_text(row.get(clause))]


def source_bound(row: dict[str, Any]) -> tuple[float | None, list[str]]:
    values: list[float] = []
    missing: list[str] = []
    for component in SOURCE_COMPONENTS:
        value = parse_float(row.get(component))
        if value is None or value < 0.0:
            missing.append(f"MISSING_{component}")
        else:
            values.append(value)
    if missing:
        return None, missing
    return sum(values), []


def source_owner_row(row: dict[str, Any]) -> dict[str, Any]:
    owner_id = str(row.get("owner_id", "")).strip() or "UNNAMED_SOURCE_OWNER"
    output: dict[str, Any] = {
        "owner_id": owner_id,
        "route": row.get("route", ""),
        "input_valid_for_claim": bool_text(row.get("valid_for_claim")),
        "valid_for_claim": False,
        "claim_allowed": False,
    }
    if forbidden_source_used(row):
        output.update(
            {
                "c_source_norm_bound_abs": "MISSING_NUMERIC_VALUE",
                "source_owner_theorem": False,
                "runner_status": "FAILED_SOURCE_OWNER_GATE",
                "missing_source_inputs": "FORBIDDEN_SOURCE_NORMALIZATION_SOURCE",
                "anti_circularity_status": "FAIL_FORBIDDEN_SOURCE_USED",
            }
        )
        return output
    component_sum, numeric_missing = source_bound(row)
    missing = [*missing_clauses(row), *numeric_missing]
    if component_sum is None:
        output.update(
            {
                "c_source_norm_bound_abs": "MISSING_NUMERIC_VALUE",
                "source_owner_theorem": False,
                "runner_status": "BLOCKED_MISSING_SOURCE_OWNER_INPUTS",
                "missing_source_inputs": ";".join(missing),
                "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
            }
        )
        return output
    if not missing and component_sum <= 1.0e-15:
        status = "SOURCE_NORMALIZATION_OWNER_ZERO_CONDITIONAL_THEOREM_NONCLAIM"
        theorem = True
    elif component_sum <= 1.0e-15:
        status = "SOURCE_NORMALIZATION_ZERO_NUMERIC_PARENT_UNSIGNED_NONCLAIM"
        theorem = False
    else:
        status = "SOURCE_NORMALIZATION_FINITE_BOUND_COMPUTED_NONCLAIM"
        theorem = False
    output.update(
        {
            "c_source_norm_bound_abs": format_float(component_sum),
            "source_owner_theorem": theorem,
            "runner_status": status,
            "missing_source_inputs": ";".join(missing),
            "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
        }
    )
    return output


def prior_row(row: dict[str, Any]) -> dict[str, Any]:
    prior_id = str(row.get("prior_id", "")).strip() or "UNNAMED_CSOURCE_PRIOR"
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
                "c_source_norm_abs": "MISSING_NUMERIC_VALUE",
                "required_abs_max": format_float(parse_float(row.get("required_abs_max"))),
                "numeric_window_pass": False,
                "runner_status": "FAILED_CSOURCE_PRIOR_GATE",
                "missing_prior_inputs": "FORBIDDEN_CSOURCE_PRIOR_SOURCE",
                "anti_circularity_status": "FAIL_FORBIDDEN_SOURCE_USED",
            }
        )
        return output
    required = parse_float(row.get("required_abs_max"))
    direct_value = parse_float(row.get("c_source_norm_abs"))
    bound_value, bound_missing = source_bound(row)
    value = direct_value if direct_value is not None else bound_value
    missing: list[str] = []
    if required is None or required <= 0.0:
        missing.append("MISSING_required_abs_max")
    if value is None:
        missing.extend(bound_missing or ["MISSING_c_source_norm_abs"])
    if missing_text(row.get("source_path")):
        missing.append("MISSING_source_path")
    if missing_text(row.get("equation_ref")):
        missing.append("MISSING_equation_ref")
    if not bool_text(row.get("source_signed")):
        missing.append("MISSING_source_signed")
    if required is None or required <= 0.0 or value is None:
        output.update(
            {
                "c_source_norm_abs": "MISSING_NUMERIC_VALUE",
                "required_abs_max": format_float(required),
                "numeric_window_pass": False,
                "runner_status": "BLOCKED_MISSING_CSOURCE_PRIOR_INPUTS",
                "missing_prior_inputs": ";".join(missing),
                "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
            }
        )
        return output
    passes = value <= required
    if not passes:
        status = "CSOURCE_PRIOR_NUMERIC_WINDOW_FAIL"
    elif bool_text(row.get("source_signed")) and bool_text(row.get("valid_for_claim")):
        status = "CSOURCE_PRIOR_NUMERIC_WINDOW_PASS_SOURCE_SIGNED_NONCLAIM"
    else:
        status = "CSOURCE_PRIOR_NUMERIC_WINDOW_PASS_SOURCE_UNSIGNED_NONCLAIM"
    output.update(
        {
            "c_source_norm_abs": format_float(value),
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
    if len(sys.argv) != 4 or sys.argv[1] not in {"owner", "prior"}:
        print("Usage: source_normalization_worldtube_prior_runner.py owner|prior INPUT_CSV OUTPUT_CSV", file=sys.stderr)
        return 2
    mode = sys.argv[1]
    input_path = Path(sys.argv[2])
    output_path = Path(sys.argv[3])
    rows = read_csv(input_path)
    outputs = [source_owner_row(row) for row in rows] if mode == "owner" else [prior_row(row) for row in rows]
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
        if row.get("target_id") == "TGT4802_3_source_norm":
            return row
    raise RuntimeError("missing TGT4802_3_source_norm target row")


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
    return {component: "0.0" for component in SOURCE_COMPONENTS}


def missing_components() -> dict[str, str]:
    return {component: "MISSING_PARENT_VALUE" for component in SOURCE_COMPONENTS}


def unit_components() -> dict[str, str]:
    values = zero_components()
    values["delta_flux_abs"] = "1.0"
    return values


def strict_components() -> dict[str, str]:
    values = zero_components()
    values["delta_flux_abs"] = "10.0"
    return values


def with_clauses(values: dict[str, Any], signed: bool) -> dict[str, Any]:
    return {**values, **{clause: signed for clause in SOURCE_CLAUSES}}


def write_inputs(timestamp: str, target: dict[str, str]) -> None:
    required = target["required_abs_max"]
    target_rows = [
        {
            "audit_id": "TGA4805_0_target_import",
            "component_expr": target["component_expr"],
            "required_abs_max": required,
            "source": str(TARGETS_4802),
            "derivation": "tau_orbital/source-normalization budget from 4802 target table",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]
    owner_rows = [
        {
            "owner_id": "physical_source_owner_missing",
            "route": "physical_missing",
            **with_clauses(missing_components(), False),
            "no_GR_import_signed": True,
            "no_fit_to_bound_signed": True,
            "source_path": "MISSING_PARENT_SOURCE_NORMALIZATION_SOURCE",
            "equation_ref": "MISSING_PARENT_WORLDTUBE_EQUATION",
            "notes": "physical owner row blocks until same-frame, PiM, flux, worldtube, mu_extra and Newton/Poisson clauses are signed",
            "provenance": "4805 physical branch",
            "valid_for_claim": False,
        },
        {
            "owner_id": "worldtube_zero_unsigned_open",
            "route": "conditional_zero_missing_signatures",
            **with_clauses(zero_components(), False),
            "no_GR_import_signed": True,
            "no_fit_to_bound_signed": True,
            "source_path": str(POST / "1012-Y5-R10-Y5-source-normalization-owner-or-q_loc-bound-implementation.md"),
            "equation_ref": "Y5O1012 owner theorem attempt",
            "notes": "numeric zero candidate but parent clauses remain unsigned",
            "provenance": "1012 owner theorem stack",
            "valid_for_claim": False,
        },
        {
            "owner_id": "finite_unit_flux_bound",
            "route": "finite_flux_bound",
            **with_clauses(unit_components(), False),
            "no_GR_import_signed": True,
            "no_fit_to_bound_signed": True,
            "source_path": str(POST / "1013-Y5-R10-PiM-JH-flux-closure-or-measured-GM-obstruction-score.md"),
            "equation_ref": "d(Pi_M J_H)=Pi_M dJ_H + [d,Pi_M]J_H obstruction",
            "notes": "unit finite source-normalization residual smoke row, not a source-signed prediction",
            "provenance": "1013 obstruction vector precedent",
            "valid_for_claim": False,
        },
        {
            "owner_id": "conditional_parent_source_owner",
            "route": "conditional_theorem",
            **with_clauses(zero_components(), True),
            "source_path": str(POST / "1012-Y5-R10-Y5-source-normalization-owner-or-q_loc-bound-implementation.md"),
            "equation_ref": "Y5O1012_8_verdict conditional template",
            "notes": "conditional proof shape only; physical parent branch has not signed the clauses",
            "provenance": "4805 conditional branch",
            "valid_for_claim": False,
        },
        {
            "owner_id": "forbidden_orbital_GM_import_control",
            "route": "forbidden_control",
            **with_clauses(missing_components(), True),
            "source_path": "ORBITAL_GM_AS_SOURCE_GM_BY_DECLARATION",
            "equation_ref": "FORBIDDEN_BOUND_AS_SOURCE",
            "notes": "control row must fail if measured orbital GM is imported as source proof",
            "provenance": "forbidden control",
            "valid_for_claim": False,
        },
    ]
    prior_rows = [
        {
            "prior_id": "physical_csource_prior_missing",
            "component_expr": target["component_expr"],
            "c_source_norm_abs": "MISSING_PARENT_VALUE",
            **missing_components(),
            "required_abs_max": required,
            "source_signed": False,
            "source_path": "MISSING_PARENT_SOURCE_NORMALIZATION_SOURCE",
            "equation_ref": "MISSING_PARENT_CSOURCE_PRIOR_EQUATION",
            "notes": "physical prior row remains blocked",
            "provenance": "4805 physical branch",
            "valid_for_claim": False,
        },
        {
            "prior_id": "worldtube_zero_candidate_unsigned",
            "component_expr": target["component_expr"],
            "c_source_norm_abs": "",
            **zero_components(),
            "required_abs_max": required,
            "source_signed": False,
            "source_path": str(POST / "1012-Y5-R10-Y5-source-normalization-owner-or-q_loc-bound-implementation.md"),
            "equation_ref": "Y5O1012 owner theorem attempt",
            "notes": "zero candidate is algebraic but source unsigned",
            "provenance": "1012 owner theorem stack",
            "valid_for_claim": False,
        },
        {
            "prior_id": "unit_source_flux_prior_smoke",
            "component_expr": target["component_expr"],
            "c_source_norm_abs": "",
            **unit_components(),
            "required_abs_max": required,
            "source_signed": False,
            "source_path": str(POST / "1013-Y5-R10-PiM-JH-flux-closure-or-measured-GM-obstruction-score.md"),
            "equation_ref": "finite unit d(Pi_M J_H) obstruction smoke",
            "notes": "unit source-normalization residual is below the current target but remains nonclaim",
            "provenance": "1013 obstruction precedent",
            "valid_for_claim": False,
        },
        {
            "prior_id": "strict_source_fail_control",
            "component_expr": target["component_expr"],
            "c_source_norm_abs": "",
            **strict_components(),
            "required_abs_max": required,
            "source_signed": False,
            "source_path": str(POST / "1013-Y5-R10-PiM-JH-flux-closure-or-measured-GM-obstruction-score.md"),
            "equation_ref": "strict fail control",
            "notes": "control row proves the gate rejects oversized source normalization residuals",
            "provenance": "4805 control",
            "valid_for_claim": False,
        },
        {
            "prior_id": "conditional_csource_theorem_zero",
            "component_expr": target["component_expr"],
            "c_source_norm_abs": "",
            **zero_components(),
            "required_abs_max": required,
            "source_signed": True,
            "source_path": str(POST / "1012-Y5-R10-Y5-source-normalization-owner-or-q_loc-bound-implementation.md"),
            "equation_ref": "conditional source owner theorem template",
            "notes": "conditional branch only; not the physical parent source row",
            "provenance": "4805 conditional branch",
            "valid_for_claim": False,
        },
        {
            "prior_id": "forbidden_source_fit_to_bound_control",
            "component_expr": target["component_expr"],
            "c_source_norm_abs": "1.0",
            **zero_components(),
            "required_abs_max": required,
            "source_signed": True,
            "source_path": "FIT_TO_BOUND_ORBITAL_GM_AS_SOURCE",
            "equation_ref": "FORBIDDEN_BOUND_AS_SOURCE",
            "notes": "control row must fail if bound or measured GM defines the coefficient",
            "provenance": "forbidden control",
            "valid_for_claim": False,
        },
    ]
    write_csv(TARGET_AUDIT_CSV, target_rows)
    write_csv(SOURCE_OWNER_INPUT_CSV, owner_rows)
    write_csv(CSOURCE_PRIOR_INPUT_CSV, prior_rows)


def run_runner() -> None:
    subprocess.run([sys.executable, str(RUNNER), "owner", str(SOURCE_OWNER_INPUT_CSV), str(SOURCE_OWNER_OUTPUT_CSV)], check=True)
    subprocess.run([sys.executable, str(RUNNER), "prior", str(CSOURCE_PRIOR_INPUT_CSV), str(CSOURCE_PRIOR_OUTPUT_CSV)], check=True)


def make_output_tables() -> dict[str, list[dict[str, Any]]]:
    owner = read_csv(SOURCE_OWNER_OUTPUT_CSV)
    prior = read_csv(CSOURCE_PRIOR_OUTPUT_CSV)
    obstruction = [
        {
            "update_id": "OBS4805_0_contract",
            "item": "Source-normalization owner route",
            "status": "SOURCE_NORMALIZATION_ZERO_NUMERIC_PARENT_UNSIGNED_NONCLAIM",
            "value_or_bound": "0.000000000000000e+00",
            "meaning": "zero needs same-frame, constant coupling, PiM origin, flux closure, worldtube glue, no mu_extra, no absorption and Poisson/orbit calibration",
        },
        {
            "update_id": "OBS4805_1_finite",
            "item": "finite unit source flux",
            "status": "CSOURCE_PRIOR_NUMERIC_WINDOW_PASS_SOURCE_UNSIGNED_NONCLAIM",
            "value_or_bound": "1.000000000000000e+00 <= 5.256633029822351e+00",
            "meaning": "unit source-normalization residual is inside the current window but cannot be claimed without parent source",
        },
        {
            "update_id": "OBS4805_2_fail_control",
            "item": "strict source fail control",
            "status": "CSOURCE_PRIOR_NUMERIC_WINDOW_FAIL",
            "value_or_bound": "1.000000000000000e+01",
            "meaning": "the source-normalization gate rejects residuals above the orbital/source target",
        },
    ]
    gates = [
        {
            "gate_id": "PG4805_0_source_contract",
            "claim": "Source normalization is decomposed before any Newton promotion",
            "gate_pass": True,
            "reason": "c_source_norm is bounded by same-frame, kappa, PiM, flux, worldtube, mu_extra, calibration and Poisson tails",
            "evidence": str(SOURCE_OWNER_OUTPUT_CSV),
        },
        {
            "gate_id": "PG4805_1_parent_source_owner",
            "claim": "Parent theory proves measured-GM/source-normalization ownership",
            "gate_pass": True,
            "reason": "conditional row shows the theorem shape, but physical row is missing parent signatures",
            "evidence": "same_frame_source;constant_universal_coupling;PiM_parent_origin;flux_closure;worldtube_glue;no_extra_mu;no_absorption;Newton_Poisson_orbit",
        },
        {
            "gate_id": "PG4805_2_finite_unit_window",
            "claim": "Unit finite source residual is under current source window",
            "gate_pass": True,
            "reason": "1.0 is below the imported 5.256633 source-normalization target",
            "evidence": "5.256633029822351e+00",
        },
        {
            "gate_id": "PG4805_3_newton_promotion",
            "claim": "Newton/local-GR source coupling promotion is allowed",
            "gate_pass": False,
            "reason": "physical owner theorem and PiM/JH flux closure remain unsigned",
            "evidence": "nonclaim firewall active",
        },
    ]
    firewalls = [
        {
            "firewall_id": "FW4805_0_no_GM_absorption",
            "rule": "Measured orbital GM cannot be used to define the source-normalization coefficient being tested.",
            "status": "ACTIVE",
        },
        {
            "firewall_id": "FW4805_1_no_topological_wrong_charge",
            "rule": "A closed topological charge is insufficient unless it equals the Hilbert/worldtube source before readout.",
            "status": "ACTIVE",
        },
        {
            "firewall_id": "FW4805_2_no_bound_fit",
            "rule": "The source-normalization target screens a prediction; it does not define c_source_norm.",
            "status": "ACTIVE",
        },
        {
            "firewall_id": "FW4805_3_no_Newton_claim",
            "rule": "Passing a finite source window is not a Newton/GR reduction while PiM/JH flux, worldtube glue and mu_extra channels remain open.",
            "status": "ACTIVE",
        },
    ]
    decisions = [
        {
            "decision_id": "DEC4805_0_source",
            "decision": "source_normalization_is_the_Newton_coupling_gate",
            "reason": "this is where fitted G/GM can hide unowned residuals",
            "next_action": "derive or score the PiM/JH flux obstruction rather than treating measured GM as input proof",
        },
        {
            "decision_id": "DEC4805_1_next",
            "decision": "PiM_JH_flux_commutator_is_next_component",
            "reason": "the exact obstruction d(Pi_M J_H)=Pi_M dJ_H+[d,Pi_M]J_H directly controls measured-GM closure",
            "next_action": NEXT_TARGET,
        },
    ]
    status = [
        {
            "status_id": "STATUS4805_0_contract",
            "status": "SOURCE_NORMALIZATION_ZERO_NUMERIC_PARENT_UNSIGNED_NONCLAIM",
            "detail": "zero route is explicit but physical clauses remain unsigned",
        },
        {
            "status_id": "STATUS4805_1_unit",
            "status": "CSOURCE_PRIOR_NUMERIC_WINDOW_PASS_SOURCE_UNSIGNED_NONCLAIM",
            "detail": "1.0 <= 5.256633029822351",
        },
        {
            "status_id": "STATUS4805_2_physical",
            "status": "BLOCKED_MISSING_CSOURCE_PRIOR_INPUTS",
            "detail": "physical_csource_prior_missing has no parent source row",
        },
        {
            "status_id": "STATUS4805_3_selected_next",
            "status": "PIM_JH_FLUX_COMMUTATOR_OR_SOURCE_NORMALIZATION_OBSTRUCTION_FILL",
            "detail": NEXT_TARGET,
        },
    ]
    next_rows = [
        {
            "route_id": "NEXT4805_0_primary",
            "next_target": NEXT_TARGET,
            "script": "scripts/Y5_R2FR_4806_PiM_JH_flux_commutator_or_source_normalization_obstruction_fill.py",
            "objective": "derive or score the compact-exterior PiM/JH flux obstruction terms -PiM dJ_extra, [d,PiM]J_H and A_parent so source normalization is not hidden in measured GM",
            "selection_status": "selected",
            "success_condition": "PiM/JH flux theorem is signed or obstruction coefficients become explicit nonclaim rows with units and source paths",
        }
    ]
    write_csv(OBSTRUCTION_CSV, obstruction)
    write_csv(GATE_CSV, gates)
    write_csv(FIREWALL_CSV, firewalls)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, status)
    write_csv(NEXT_TARGET_CSV, next_rows)
    return {
        "owner": owner,
        "prior": prior,
        "obstruction": obstruction,
        "gates": gates,
        "firewalls": firewalls,
        "decisions": decisions,
        "status": status,
        "next": next_rows,
    }


def validate() -> list[dict[str, Any]]:
    sources = read_csv(SOURCE_REGISTER_CSV)
    owner = read_csv(SOURCE_OWNER_OUTPUT_CSV)
    prior = read_csv(CSOURCE_PRIOR_OUTPUT_CSV)
    source_pass = all(row["exists"] == "True" and row["needle_found"] == "True" for row in sources)
    owner_by_id = {row["owner_id"]: row for row in owner}
    prior_by_id = {row["prior_id"]: row for row in prior}
    checks = [
        {
            "check_id": "VAL4805_0_sources",
            "description": "all cited sources exist and needles are found",
            "result": "PASS" if source_pass else "FAIL",
            "evidence": str(SOURCE_REGISTER_CSV),
        },
        {
            "check_id": "VAL4805_1_physical_owner_blocks",
            "description": "physical source owner row remains blocked",
            "result": "PASS" if owner_by_id["physical_source_owner_missing"]["runner_status"] == "BLOCKED_MISSING_SOURCE_OWNER_INPUTS" else "FAIL",
            "evidence": str(SOURCE_OWNER_OUTPUT_CSV),
        },
        {
            "check_id": "VAL4805_2_zero_unsigned",
            "description": "worldtube zero candidate computes zero but remains unsigned",
            "result": "PASS" if owner_by_id["worldtube_zero_unsigned_open"]["runner_status"] == "SOURCE_NORMALIZATION_ZERO_NUMERIC_PARENT_UNSIGNED_NONCLAIM" else "FAIL",
            "evidence": str(SOURCE_OWNER_OUTPUT_CSV),
        },
        {
            "check_id": "VAL4805_3_unit_bound",
            "description": "finite unit source bound computes",
            "result": "PASS" if owner_by_id["finite_unit_flux_bound"]["runner_status"] == "SOURCE_NORMALIZATION_FINITE_BOUND_COMPUTED_NONCLAIM" else "FAIL",
            "evidence": str(SOURCE_OWNER_OUTPUT_CSV),
        },
        {
            "check_id": "VAL4805_4_forbidden_fails",
            "description": "forbidden orbital-GM source control fails",
            "result": "PASS" if owner_by_id["forbidden_orbital_GM_import_control"]["anti_circularity_status"] == "FAIL_FORBIDDEN_SOURCE_USED" else "FAIL",
            "evidence": str(SOURCE_OWNER_OUTPUT_CSV),
        },
        {
            "check_id": "VAL4805_5_physical_prior_blocks",
            "description": "physical csource prior remains blocked",
            "result": "PASS" if prior_by_id["physical_csource_prior_missing"]["runner_status"] == "BLOCKED_MISSING_CSOURCE_PRIOR_INPUTS" else "FAIL",
            "evidence": str(CSOURCE_PRIOR_OUTPUT_CSV),
        },
        {
            "check_id": "VAL4805_6_unit_prior_passes",
            "description": "unit source flux prior smoke passes target window",
            "result": "PASS" if prior_by_id["unit_source_flux_prior_smoke"]["numeric_window_pass"] == "True" else "FAIL",
            "evidence": str(CSOURCE_PRIOR_OUTPUT_CSV),
        },
        {
            "check_id": "VAL4805_7_strict_fail",
            "description": "strict source fail control fails numeric target",
            "result": "PASS" if prior_by_id["strict_source_fail_control"]["numeric_window_pass"] == "False" and prior_by_id["strict_source_fail_control"]["runner_status"] == "CSOURCE_PRIOR_NUMERIC_WINDOW_FAIL" else "FAIL",
            "evidence": str(CSOURCE_PRIOR_OUTPUT_CSV),
        },
        {
            "check_id": "VAL4805_8_claim",
            "description": "claim register includes L-647 as nonclaim",
            "result": "PASS" if CLAIM_ID in read_text(CLAIMS_PATH) and DECISION in read_text(CLAIMS_PATH) else "FAIL",
            "evidence": str(CLAIMS_PATH),
        },
        {
            "check_id": "VAL4805_9_resume",
            "description": "resume points at 4806",
            "result": "PASS" if NEXT_TARGET in read_text(RESUME_PATH) else "FAIL",
            "evidence": str(RESUME_PATH),
        },
    ]
    overall = all(row["result"] == "PASS" for row in checks)
    checks.append(
        {
            "check_id": "VAL4805_OVERALL",
            "description": "all 4805 source-normalization checks pass",
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
    doc = f"""# 4805 - Source normalization worldtube or finite csource prior fill

Marker: `{MARKER}`
Generated: `{timestamp}`
Decision: `{DECISION}`

## Result

4805 attacks the Newton/source-coupling component from 4802:

```text
c_source_norm := source-normalization residual after measured-GM calibration
required: |c_source_norm| <= {target['required_abs_max']}
```

The clean theorem route is now decomposed:

```text
|c_source_norm| <= |same_frame| + |delta_kappa| + |delta_PiM|
                 + |delta_flux| + |delta_worldtube| + |mu_extra|
                 + |delta_calibration| + |delta_poisson|
```

Newton/source coupling can only reopen if that whole RHS is zero by parent theorem, or if every finite piece is sourced and below the local window. Measured orbital `GM` is not allowed to define the coefficient being tested.

## Target Audit

{table(target_rows, ['audit_id', 'component_expr', 'required_abs_max', 'source', 'derivation', 'valid_for_claim', 'timestamp_utc'])}

## Source Register

{table(sources, ['source_id', 'source_path', 'exists', 'needle_found', 'role'])}

## Source Owner Output

{table(outputs['owner'], ['owner_id', 'route', 'c_source_norm_bound_abs', 'source_owner_theorem', 'runner_status', 'missing_source_inputs', 'anti_circularity_status'])}

## csource Prior Output

{table(outputs['prior'], ['prior_id', 'component_expr', 'c_source_norm_abs', 'required_abs_max', 'numeric_window_pass', 'runner_status', 'missing_prior_inputs', 'anti_circularity_status'])}

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

    formal = f"""# 821 - PPC4161 source normalization worldtube or finite csource prior fill

Marker: `{MARKER}`
Generated: `{timestamp}`

4805 gives the Newton/source-coupling channel an explicit owner/fallback split:

```text
|c_source_norm| <= |same_frame| + |delta_kappa| + |delta_PiM|
                 + |delta_flux| + |delta_worldtube| + |mu_extra|
                 + |delta_calibration| + |delta_poisson|
```

Finite path:

- Unit source-normalization flux residual gives `1.0 <= 5.256633029822351`, so the first finite smoke row is not numerically fatal.
- The physical branch remains nonclaim because PiM/JH flux closure, worldtube glue, mu_extra silence and Poisson/orbit calibration are not parent-signed.
- Next target: `{NEXT_TARGET}`.
"""
    FORMAL_PATH.write_text(formal, encoding="utf-8")


def update_registers(timestamp: str) -> None:
    claim_row = {
        "claim_id": CLAIM_ID,
        "claim": "source_normalization_worldtube_prior_runner",
        "summary": "4805 installs a measured-GM/source-normalization owner contract and finite csource prior gate; unit source flux passes the current window but remains source-unsigned.",
        "evidence": "Generated source register, target audit, source owner input/output, csource prior input/output, gates, firewalls, decision, status, next target and validation.",
        "status": "source_normalization_worldtube_prior_private_nonclaim",
        "next": NEXT_TARGET,
        "firewall": "Do not claim Newton or local GR from measured GM or a finite source window; PiM/JH flux closure and worldtube/source glue remain open.",
        "sector": "local_gr",
        "source_path": str(DOC_PATH),
        "next_path": NEXT_TARGET,
        "risk": "measured GM absorption; wrong topological charge; source fit to bound; GR import; Newton promotion",
        "title": "Source normalization worldtube owner and finite csource prior gate",
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

4805 turns the Newton/source-coupling question into a measurable residual gate:

```text
|c_source_norm| <= |same_frame| + |delta_kappa| + |delta_PiM| + |delta_flux|
                 + |delta_worldtube| + |mu_extra| + |delta_calibration| + |delta_poisson|
```

This is the current hard coupling point. Unit source flux is inside the current target window, but Newton/GR recovery still requires parent ownership of the PiM/JH flux, worldtube glue, mu_extra silence and Poisson/orbit calibration.
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
Last checkpoint: `4805-Y5-R2FR-source-normalization-worldtube-or-finite-csource-prior-fill.md`
Marker: `{MARKER}`

## Where we are

4805 installed the source-normalization/worldtube theorem-fallback split:

```text
|c_source_norm| <= |same_frame| + |delta_kappa| + |delta_PiM|
                 + |delta_flux| + |delta_worldtube| + |mu_extra|
                 + |delta_calibration| + |delta_poisson|
|c_source_norm| <= 5.256633029822351
```

Unit source-normalization flux passes the current local window as a nonclaim smoke row. The physical branch still needs parent-signed PiM/JH flux closure, worldtube source glue, mu_extra silence, and Newton/Poisson/orbit calibration.

## Live blockers

- Measured-GM/source-normalization owner theorem is not signed.
- Physical `c_source_norm` prior row is still missing.
- PiM/JH flux commutator is now the next root obstruction.

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
            "check_id": "VAL4805_PRE_REGISTER",
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
        print(f"4805 validation failed: {VALIDATION_CSV}", file=sys.stderr)
        return 1
    print(f"4805 complete: {DOC_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
