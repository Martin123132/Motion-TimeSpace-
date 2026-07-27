from __future__ import annotations

import csv
import math
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
SOURCE_WEIGHT_DOCS = ROOT / "source-intake" / "source-weight" / "docs"
MICROSCOPE_COEFFS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "coefficients"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1948"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1948-Y5-R2FR-Cassini-slip-bound-smoke-runner-or-PTF-source-fill.md"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
GENERATED_UTC = datetime.now(timezone.utc).isoformat()

SOURCES = {
    "1947_doc": ROOT / "1947-Y5-R2FR-boundary-kernel-isotropy-or-Cassini-slip-bound-inputs.md",
    "1947_validation": OUT / "P8_Y5_BRR545_1947_VALIDATION.csv",
    "1947_inputs": OUT / "P8_Y5_PARENT_QLOC_1947_CASSINI_SLIP_BOUND_INPUT_LEDGER.csv",
    "1947_schema": OUT / "P8_Y5_PARENT_QLOC_1947_CASSINI_SLIP_BOUND_RUNNER_SCHEMA.csv",
    "1947_policy": OUT / "P8_Y5_PARENT_QLOC_1947_CASSINI_BOUND_POLICY_CANDIDATES.csv",
    "1947_claims": OUT / "P8_Y5_PARENT_QLOC_1947_CLAIM_GATE.csv",
    "1944_derivation": OUT / "P8_Y5_PARENT_QLOC_1944_R11_WEAK_FIELD_POTENTIAL_DERIVATION.csv",
    "1942_web": OUT / "P8_Y5_PARENT_QLOC_1942_WEB_SOURCE_REGISTER.csv",
}

NEEDLES = {
    "1947_doc": ["RUN1947_0_slip_bound_schema", "SBI1947_1_kappa_R", "VAL1947_OVERALL"],
    "1947_validation": ["VAL1947_OVERALL", "PASS"],
    "1947_inputs": ["SBI1947_0_gamma_bound_policy", "MISSING_PROJECTED_R11_TF_AMPLITUDE"],
    "1947_schema": ["RUN1947_0_slip_bound_schema", "SCHEMA_READY_INPUTS_MISSING"],
    "1947_policy": ["CBP1947_2_abs_two_sigma_screen", "6.700000e-05"],
    "1947_claims": ["CG1947_3_numeric_slip_prediction", "FAIL_BLOCKED"],
    "1944_derivation": ["WFE1944_5_delta_gamma_source_law", "P_TF[R11_ij]"],
    "1942_web": ["WEB1942_0_CASSINI_GAMMA", "nature01997"],
}

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_1948_SOURCE_REGISTER.csv",
    "input_audit": OUT / "P8_Y5_PARENT_QLOC_1948_CASSINI_SLIP_INPUT_AUDIT.csv",
    "smoke_runner": OUT / "P8_Y5_PARENT_QLOC_1948_CASSINI_SLIP_SMOKE_RUNNER.csv",
    "failure_modes": OUT / "P8_Y5_PARENT_QLOC_1948_CASSINI_SLIP_FAILURE_MODE_LEDGER.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_1948_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_1948_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_1948_NEXT_TARGET.csv",
    "status_snapshot": OUT / "P8_Y5_PARENT_QLOC_1948_PROJECT_STATUS_SNAPSHOT.csv",
    "validation": OUT / "P8_Y5_BRR545_1948_VALIDATION.csv",
}

BRANCH_COPIES = {
    "source_weight_runner": SOURCE_WEIGHT_DOCS / "CASSINI_SLIP_SMOKE_RUNNER_1948_NONCLAIM.csv",
    "microscope_claim_gate": MICROSCOPE_COEFFS / "P8_Y5_PARENT_QLOC_1948_CLAIM_GATE_NONCLAIM.csv",
    "next_queue": QUEUE / "JR1948_R11_PTF_OR_KAPPA_CTF_SOURCE_FILL_QUEUE.csv",
    "claim_quarantine": QUARANTINE / "P8_Y5_PARENT_QLOC_1948_CLAIM_GATE.csv",
}

REQUIRED_NUMERIC_INPUTS = {
    "gamma_bound_policy": "SBI1947_0_gamma_bound_policy",
    "kappa_R": "SBI1947_1_kappa_R",
    "C_TF": "SBI1947_2_C_TF",
    "U_solar_frame": "SBI1947_3_U_solar_frame",
    "nabla^{-2}_local": "SBI1947_4_inverse_laplacian",
    "P_TF[R11_ij]": "SBI1947_6_PTF_amplitude",
}


def flag(value: bool) -> str:
    return "True" if value else "False"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def has_needles(path: Path, needles: list[str]) -> bool:
    if not path.exists():
        return False
    text = read_text(path)
    return all(needle in text for needle in needles)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def is_float(value: str) -> bool:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return False
    return math.isfinite(number)


def numeric_value(value: str) -> float | None:
    if is_float(value):
        return float(value)
    return None


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path in SOURCES.items():
        needles = NEEDLES[source_id]
        ok = has_needles(path, needles)
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source_id,
                "source_path": str(path),
                "purpose": "1948 Cassini slip bound smoke runner",
                "required_needles": ";".join(needles),
                "status": "EXISTS_NEEDLES_CONFIRMED" if ok else "MISSING_SOURCE_OR_NEEDLE",
                "issue": "" if ok else "source path missing or required needles absent",
                "valid_for_claim": flag(False),
                "claim_allowed": flag(False),
                "generated_utc": GENERATED_UTC,
            }
        )
    return rows


def input_audit_rows() -> list[dict[str, Any]]:
    source_rows = read_csv(SOURCES["1947_inputs"])
    by_symbol = {row["symbol"]: row for row in source_rows}
    rows: list[dict[str, Any]] = []

    for symbol, input_id in REQUIRED_NUMERIC_INPUTS.items():
        source_row = next((row for row in source_rows if row["input_id"] == input_id), None)
        value = source_row["current_value"] if source_row else "MISSING"
        numeric = numeric_value(value)
        source_status = source_row["status"] if source_row else "MISSING_INPUT_ROW"
        if numeric is not None and numeric > 0:
            status = "NUMERIC_POSITIVE_AVAILABLE_NONCLAIM"
        elif numeric is not None:
            status = "NUMERIC_AVAILABLE_SIGN_CHECK_NEEDED_NONCLAIM"
        else:
            status = source_status if source_status.startswith("MISSING") else "NONNUMERIC_OR_POLICY_ONLY"
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "audit_id": f"AUD1948_{len(rows)}_{input_id}",
                "symbol": symbol,
                "source_input_id": input_id,
                "source_status": source_status,
                "current_value": value,
                "numeric_available": flag(numeric is not None),
                "required_for_numeric_runner": flag(True),
                "audit_status": status,
                "valid_for_claim": flag(False),
                "claim_allowed": flag(False),
                "generated_utc": GENERATED_UTC,
            }
        )

    if "source_profile/worldtube" in by_symbol:
        row = by_symbol["source_profile/worldtube"]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "audit_id": f"AUD1948_{len(rows)}_source_profile",
                "symbol": "source_profile/worldtube",
                "source_input_id": row["input_id"],
                "source_status": row["status"],
                "current_value": row["current_value"],
                "numeric_available": flag(False),
                "required_for_numeric_runner": flag(False),
                "audit_status": "MISSING_PROFILE_FOR_REFINED_RUNNER",
                "valid_for_claim": flag(False),
                "claim_allowed": flag(False),
                "generated_utc": GENERATED_UTC,
            }
        )

    return rows


def smoke_runner_rows(input_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    missing_required = [
        row["symbol"]
        for row in input_rows
        if row["required_for_numeric_runner"] == flag(True) and row["numeric_available"] != flag(True)
    ]
    available = {row["symbol"]: numeric_value(str(row["current_value"])) for row in input_rows}
    can_run_numeric = not missing_required and all(available.get(symbol) is not None for symbol in REQUIRED_NUMERIC_INPUTS)
    gamma_bound = available.get("gamma_bound_policy")

    rows: list[dict[str, Any]] = [
        {
            "branch_id": BRANCH_ID,
            "runner_id": "RUN1948_0_live_input_scan",
            "branch": "live_1947_inputs",
            "can_run_numeric": flag(can_run_numeric),
            "numeric_prediction": "NOT_EVALUATED" if not can_run_numeric else "",
            "bound_policy": f"{gamma_bound:.6e}" if gamma_bound is not None else "MISSING",
            "comparison": "NOT_EVALUATED_MISSING_INPUTS" if missing_required else "READY_FOR_EVALUATION",
            "runner_status": "BLOCKED_MISSING_REQUIRED_INPUTS" if missing_required else "READY_NONCLAIM",
            "missing_inputs": ";".join(missing_required),
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "runner_id": "RUN1948_1_theorem_zero_branch",
            "branch": "theorem_zero_P_TF",
            "can_run_numeric": flag(False),
            "numeric_prediction": "0 if P_TF[R11_ij]=0 is parent-signed",
            "bound_policy": f"{gamma_bound:.6e}" if gamma_bound is not None else "MISSING",
            "comparison": "WOULD_PASS_IF_THEOREM_SIGNED",
            "runner_status": "BLOCKED_THEOREM_ZERO_NOT_PARENT_SIGNED",
            "missing_inputs": "PARENT_SIGNED_P_TF_ZERO_THEOREM",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
    ]

    if can_run_numeric:
        kappa = available["kappa_R"]
        c_tf = available["C_TF"]
        u = available["U_solar_frame"]
        inv = available["nabla^{-2}_local"]
        ptf = available["P_TF[R11_ij]"]
        prediction = abs(-(kappa / (c_tf * u)) * inv * ptf)
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "runner_id": "RUN1948_2_numeric_comparison",
                "branch": "numeric",
                "can_run_numeric": flag(True),
                "numeric_prediction": f"{prediction:.6e}",
                "bound_policy": f"{gamma_bound:.6e}",
                "comparison": "PASS_BOUND" if prediction <= gamma_bound else "FAIL_BOUND",
                "runner_status": "NUMERIC_EVALUATED_NONCLAIM",
                "missing_inputs": "",
                "valid_for_claim": flag(False),
                "claim_allowed": flag(False),
                "generated_utc": GENERATED_UTC,
            }
        )
    else:
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "runner_id": "RUN1948_2_numeric_comparison",
                "branch": "numeric",
                "can_run_numeric": flag(False),
                "numeric_prediction": "NOT_EVALUATED",
                "bound_policy": f"{gamma_bound:.6e}" if gamma_bound is not None else "MISSING",
                "comparison": "NOT_EVALUATED_MISSING_INPUTS",
                "runner_status": "BLOCKED_MISSING_REQUIRED_INPUTS",
                "missing_inputs": ";".join(missing_required),
                "valid_for_claim": flag(False),
                "claim_allowed": flag(False),
                "generated_utc": GENERATED_UTC,
            }
        )

    return rows


def failure_mode_rows(input_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in input_rows:
        if row["required_for_numeric_runner"] == flag(True) and row["numeric_available"] != flag(True):
            rows.append(
                {
                    "branch_id": BRANCH_ID,
                    "failure_id": f"FAIL1948_{len(rows)}_{row['source_input_id']}",
                    "symbol": row["symbol"],
                    "failure_mode": row["audit_status"],
                    "effect_on_runner": "numeric Cassini slip comparison blocked",
                    "required_fix": f"derive or source numeric {row['symbol']} with units and source path",
                    "valid_for_claim": flag(False),
                    "claim_allowed": flag(False),
                    "generated_utc": GENERATED_UTC,
                }
            )

    rows.append(
        {
            "branch_id": BRANCH_ID,
            "failure_id": f"FAIL1948_{len(rows)}_claim_policy",
            "symbol": "gamma_bound_policy",
            "failure_mode": "POLICY_CANDIDATE_NOT_FINAL_CLAIM_RULE",
            "effect_on_runner": "even with inputs, public claim needs explicit confidence convention",
            "required_fix": "choose and justify 1sigma/2sigma/conservative policy before public claim",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        }
    )
    return rows


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1948_0_runner_implemented",
            "claim": "Cassini slip smoke runner exists and parses live inputs.",
            "status": "PASS_NONCLAIM",
            "reason": "runner rows scan inputs and report missing required quantities",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1948_1_failure_modes_explicit",
            "claim": "Every missing numeric input has an explicit failure mode.",
            "status": "PASS_NONCLAIM",
            "reason": "failure ledger records missing kappa_R/C_TF/U/inverse-Laplacian/P_TF",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1948_2_numeric_prediction",
            "claim": "MTS predicts a numeric Cassini delta_gamma_R11.",
            "status": "FAIL_BLOCKED",
            "reason": "required numeric inputs are missing",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1948_3_theorem_zero",
            "claim": "P_TF[R11_ij]=0 is parent-signed.",
            "status": "FAIL_BLOCKED",
            "reason": "theorem-zero branch remains conditional only",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1948_4_Cassini_pass",
            "claim": "MTS passes Cassini gamma.",
            "status": "FAIL_BLOCKED",
            "reason": "no theorem-zero or numeric bounded prediction exists",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1948_5_local_GR_PPN",
            "claim": "MTS derives local GR/PPN.",
            "status": "FAIL_BLOCKED",
            "reason": "Cassini gamma remains blocked and other PPN residuals remain open",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1948_6_public_claim",
            "claim": "1948 is public-ready local-GR evidence.",
            "status": "FAIL_BLOCKED",
            "reason": "private smoke-runner checkpoint only",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1948_0_runner_status",
            "decision": "CASSINI_SMOKE_RUNNER_IMPLEMENTED_BLOCKED_AS_DESIGNED",
            "reason": "the runner now fails cleanly rather than letting a missing coefficient masquerade as a result",
            "next_action": "fill the first R11 slip numerator/normalization row or prove P_TF zero",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1948_1_primary_missing_input",
            "decision": "TARGET_P_TF_OR_KAPPA_CTF_SOURCE_FILL_NEXT",
            "reason": "without P_TF amplitude and kappa_R/C_TF normalization the runner cannot compute delta_gamma_R11",
            "next_action": "attempt to derive/source P_TF[R11_ij], kappa_R, and C_TF from the R11 operator branch",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "next_id": "NEXT1948_0_primary",
            "priority": "selected",
            "target_doc": "1949-Y5-R2FR-R11-PTF-source-or-kappa-CTF-normalization.md",
            "target_script": "scripts/Y5_R2FR_R11_PTF_source_or_kappa_CTF_normalization_1949.py",
            "objective": "derive or source the first real R11 traceless-spatial amplitude/normalization row: P_TF[R11_ij], kappa_R, and C_TF; otherwise keep Cassini runner blocked",
            "acceptance_output": "numeric/source-backed or theorem-zero P_TF/kappa_R/C_TF rows, or explicit nonclaim blocker ledger",
            "nonclaim_rule": "do not claim Cassini/local-GR pass unless 1948 runner receives real inputs or a parent-signed P_TF zero theorem",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        }
    ]


def status_snapshot_rows(smoke_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    live = smoke_rows[0]
    return [
        {
            "branch_id": BRANCH_ID,
            "snapshot_id": "SNAP1948_0_project_position",
            "status": "CASSINI_SLIP_SMOKE_RUNNER_EXISTS_AND_BLOCKS_MISSING_INPUTS",
            "strongest_result": "runner detects missing kappa_R, C_TF, U_solar_frame, inverse-Laplacian boundary, and P_TF amplitude before any Cassini comparison",
            "what_improved": "Cassini local-GR gate is now executable as a discipline tool rather than prose",
            "still_missing": live["missing_inputs"],
            "claim_status": "Cassini/local-GR public claims remain blocked",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        }
    ]


def copy_branch_artifacts(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    write_csv(BRANCH_COPIES["source_weight_runner"], rows_by_name["smoke_runner"])
    write_csv(BRANCH_COPIES["microscope_claim_gate"], rows_by_name["claim_gate"])
    write_csv(BRANCH_COPIES["next_queue"], rows_by_name["next_target"])
    write_csv(BRANCH_COPIES["claim_quarantine"], rows_by_name["claim_gate"])


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def csv_has_rows(path: Path) -> bool:
    if not path.exists():
        return False
    with path.open(newline="", encoding="utf-8") as handle:
        return len(list(csv.DictReader(handle))) > 0


def formalization_1948_artifact_count() -> int:
    if not FORMALIZATION.exists():
        return 0
    return sum(1 for _ in FORMALIZATION.rglob("*1948*"))


def validation_row(validation_id: str, status: str, detail: str) -> dict[str, str]:
    return {
        "validation_id": validation_id,
        "status": status,
        "detail": detail,
        "valid_for_claim": flag(False),
        "claim_allowed": flag(False),
    }


def validate(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []

    sources_ok = all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in rows_by_name["source_register"])
    rows.append(validation_row("VAL1948_00_sources", "PASS" if sources_ok else "FAIL", "all local source paths exist and needles found" if sources_ok else "source path or needle missing"))

    input_rows = rows_by_name["input_audit"]
    gamma_rows = [row for row in input_rows if row["symbol"] == "gamma_bound_policy" and row["numeric_available"] == flag(True)]
    missing_required = [row for row in input_rows if row["required_for_numeric_runner"] == flag(True) and row["numeric_available"] != flag(True)]
    input_ok = bool(gamma_rows) and len(missing_required) >= 5
    rows.append(validation_row("VAL1948_01_input_audit", "PASS" if input_ok else "FAIL", "numeric gamma policy available and required MTS inputs missing"))

    runner_rows = rows_by_name["smoke_runner"]
    runner_ok = any(row["runner_status"] == "BLOCKED_MISSING_REQUIRED_INPUTS" for row in runner_rows) and any(row["runner_status"] == "BLOCKED_THEOREM_ZERO_NOT_PARENT_SIGNED" for row in runner_rows)
    rows.append(validation_row("VAL1948_02_runner_blocks_cleanly", "PASS" if runner_ok else "FAIL", "smoke runner blocks numeric and theorem-zero branches cleanly"))

    failure_ok = len(rows_by_name["failure_modes"]) >= len(missing_required)
    rows.append(validation_row("VAL1948_03_failure_modes", "PASS" if failure_ok else "FAIL", "failure modes recorded for missing inputs"))

    claim_rows = rows_by_name["claim_gate"]
    claim_ok = len([row for row in claim_rows if row["status"] == "PASS_NONCLAIM"]) == 2 and len([row for row in claim_rows if row["status"] == "FAIL_BLOCKED"]) == 5
    rows.append(validation_row("VAL1948_04_claim_gates", "PASS" if claim_ok else "FAIL", "runner nonclaim passes only; all claim gates blocked"))

    decision_ok = any(row["decision"] == "TARGET_P_TF_OR_KAPPA_CTF_SOURCE_FILL_NEXT" for row in rows_by_name["decision"])
    rows.append(validation_row("VAL1948_05_decision", "PASS" if decision_ok else "FAIL", "PTF/kappa/CTF source fill selected"))

    next_ok = rows_by_name["next_target"][0]["target_doc"].startswith("1949-Y5-R2FR-R11-PTF-source")
    rows.append(validation_row("VAL1948_06_next_target", "PASS" if next_ok else "FAIL", "1949 PTF/kappa/CTF target selected"))

    flags_ok = all(row.get("valid_for_claim") == flag(False) and row.get("claim_allowed") == flag(False) for table in rows_by_name.values() for row in table)
    rows.append(validation_row("VAL1948_07_claim_flags_safe", "PASS" if flags_ok else "FAIL", "claim flags all false"))

    output_paths = [path for key, path in OUTPUTS.items() if key != "validation"]
    csv_ok = all(csv_has_rows(path) for path in output_paths)
    rows.append(validation_row("VAL1948_08_csv_parse", "PASS" if csv_ok else "FAIL", "all generated CSVs parse with rows"))

    branch_ok = all(csv_has_rows(path) for path in BRANCH_COPIES.values())
    rows.append(validation_row("VAL1948_09_branch_copies", "PASS" if branch_ok else "FAIL", "; ".join(str(path) for path in BRANCH_COPIES.values())))

    pycache_absent = not (Path(__file__).resolve().parent / "__pycache__").exists()
    rows.append(validation_row("VAL1948_10_pycache_absent", "PASS" if pycache_absent else "FAIL", "scripts __pycache__ absent"))

    formalization_count = formalization_1948_artifact_count()
    rows.append(validation_row("VAL1948_11_formalization_untouched", "PASS" if formalization_count == 0 else "FAIL", f"formalization_1948_artifact_count={formalization_count}"))

    overall_ok = all(row["status"] == "PASS" for row in rows)
    rows.append(validation_row("VAL1948_OVERALL", "PASS" if overall_ok else "FAIL", "1948 Cassini slip bound smoke runner or PTF source fill"))
    return rows


def escape_cell(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return ""
    headers = list(rows[0].keys())
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(escape_cell(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines)


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    sections = [
        "# 1948 Y5 R2FR: Cassini Slip Bound Smoke Runner or PTF Source Fill",
        "",
        "## Verdict",
        "",
        "1948 turns the Cassini gamma branch into an executable discipline gate. The runner reads the 1947 input ledger, accepts the private conservative screening value `gamma_bound_policy=6.7e-5`, then refuses to evaluate `delta_gamma_R11` because the MTS-side inputs are still missing.",
        "",
        "This is good failure, not dead-end failure. The local-GR branch now has a runner that blocks precisely on `kappa_R`, `C_TF`, `U_solar_frame`, the boundary-conditioned inverse Laplacian, and `P_TF[R11_ij]`. The theorem-zero branch also blocks unless `P_TF[R11_ij]=0` is parent-signed.",
        "",
        "Next target: fill or derive the first real `P_TF/kappa_R/C_TF` row from the R11 operator branch, or prove the parent-zero theorem. Until then, no Cassini/local-GR claim.",
        "",
        "## Source Register",
        "",
        markdown_table(rows_by_name["source_register"]),
        "",
        "## Input Audit",
        "",
        markdown_table(rows_by_name["input_audit"]),
        "",
        "## Smoke Runner",
        "",
        markdown_table(rows_by_name["smoke_runner"]),
        "",
        "## Failure Mode Ledger",
        "",
        markdown_table(rows_by_name["failure_modes"]),
        "",
        "## Claim Gate",
        "",
        markdown_table(rows_by_name["claim_gate"]),
        "",
        "## Decision Ledger",
        "",
        markdown_table(rows_by_name["decision"]),
        "",
        "## Next Target",
        "",
        markdown_table(rows_by_name["next_target"]),
        "",
        "## Project Status Snapshot",
        "",
        markdown_table(rows_by_name["status_snapshot"]),
        "",
        "## Validation",
        "",
        markdown_table(rows_by_name["validation"]),
        "",
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    SOURCE_WEIGHT_DOCS.mkdir(parents=True, exist_ok=True)
    MICROSCOPE_COEFFS.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)
    QUARANTINE.mkdir(parents=True, exist_ok=True)

    input_rows = input_audit_rows()
    smoke_rows = smoke_runner_rows(input_rows)
    rows_by_name = {
        "source_register": source_register_rows(),
        "input_audit": input_rows,
        "smoke_runner": smoke_rows,
        "failure_modes": failure_mode_rows(input_rows),
        "claim_gate": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
        "status_snapshot": status_snapshot_rows(smoke_rows),
    }

    for output_key, output_path in OUTPUTS.items():
        if output_key == "validation":
            continue
        write_csv(output_path, rows_by_name[output_key])

    copy_branch_artifacts(rows_by_name)
    remove_pycache()
    rows_by_name["validation"] = validate(rows_by_name)
    write_csv(OUTPUTS["validation"], rows_by_name["validation"])
    write_doc(rows_by_name)


if __name__ == "__main__":
    main()
