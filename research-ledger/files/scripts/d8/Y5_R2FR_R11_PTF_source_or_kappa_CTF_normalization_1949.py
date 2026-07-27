from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
SOURCE_WEIGHT_DOCS = ROOT / "source-intake" / "source-weight" / "docs"
MICROSCOPE_COEFFS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "coefficients"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1949"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1949-Y5-R2FR-R11-PTF-source-or-kappa-CTF-normalization.md"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
GENERATED_UTC = datetime.now(timezone.utc).isoformat()

SOURCES = {
    "1948_doc": ROOT / "1948-Y5-R2FR-Cassini-slip-bound-smoke-runner-or-PTF-source-fill.md",
    "1948_validation": OUT / "P8_Y5_BRR545_1948_VALIDATION.csv",
    "1948_input_audit": OUT / "P8_Y5_PARENT_QLOC_1948_CASSINI_SLIP_INPUT_AUDIT.csv",
    "1948_runner": OUT / "P8_Y5_PARENT_QLOC_1948_CASSINI_SLIP_SMOKE_RUNNER.csv",
    "1948_failures": OUT / "P8_Y5_PARENT_QLOC_1948_CASSINI_SLIP_FAILURE_MODE_LEDGER.csv",
    "1944_derivation": OUT / "P8_Y5_PARENT_QLOC_1944_R11_WEAK_FIELD_POTENTIAL_DERIVATION.csv",
    "1947_policy": OUT / "P8_Y5_PARENT_QLOC_1947_CASSINI_BOUND_POLICY_CANDIDATES.csv",
    "1947_inputs": OUT / "P8_Y5_PARENT_QLOC_1947_CASSINI_SLIP_BOUND_INPUT_LEDGER.csv",
}

NEEDLES = {
    "1948_doc": ["RUN1948_0_live_input_scan", "NEXT1948_0_primary", "VAL1948_OVERALL"],
    "1948_validation": ["VAL1948_OVERALL", "PASS"],
    "1948_input_audit": ["AUD1948_1_SBI1947_1_kappa_R", "AUD1948_5_SBI1947_6_PTF_amplitude"],
    "1948_runner": ["BLOCKED_MISSING_REQUIRED_INPUTS", "BLOCKED_THEOREM_ZERO_NOT_PARENT_SIGNED"],
    "1948_failures": ["MISSING_KAPPA_R", "MISSING_PROJECTED_R11_TF_AMPLITUDE"],
    "1944_derivation": ["WFE1944_5_delta_gamma_source_law", "DELTA_GAMMA_SOURCE_LAW_SYMBOLIC"],
    "1947_policy": ["CBP1947_2_abs_two_sigma_screen", "6.700000e-05"],
    "1947_inputs": ["SBI1947_0_gamma_bound_policy", "SBI1947_6_PTF_amplitude"],
}

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_1949_SOURCE_REGISTER.csv",
    "product_compression": OUT / "P8_Y5_PARENT_QLOC_1949_CASSINI_PRODUCT_COMPRESSION.csv",
    "coefficient_status": OUT / "P8_Y5_PARENT_QLOC_1949_KAPPA_CTF_PTF_STATUS.csv",
    "compressed_input_ledger": OUT / "P8_Y5_PARENT_QLOC_1949_COMPRESSED_SLIP_INPUT_LEDGER.csv",
    "runner_update": OUT / "P8_Y5_PARENT_QLOC_1949_COMPRESSED_RUNNER_UPDATE.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_1949_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_1949_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_1949_NEXT_TARGET.csv",
    "status_snapshot": OUT / "P8_Y5_PARENT_QLOC_1949_PROJECT_STATUS_SNAPSHOT.csv",
    "validation": OUT / "P8_Y5_BRR545_1949_VALIDATION.csv",
}

BRANCH_COPIES = {
    "source_weight_product": SOURCE_WEIGHT_DOCS / "CASSINI_PRODUCT_COMPRESSION_1949_NONCLAIM.csv",
    "microscope_claim_gate": MICROSCOPE_COEFFS / "P8_Y5_PARENT_QLOC_1949_CLAIM_GATE_NONCLAIM.csv",
    "next_queue": QUEUE / "JR1949_DIMENSIONLESS_STF_SOURCE_OR_ZERO_THEOREM_QUEUE.csv",
    "claim_quarantine": QUARANTINE / "P8_Y5_PARENT_QLOC_1949_CLAIM_GATE.csv",
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
                "purpose": "1949 R11 PTF source or kappa/CTF normalization",
                "required_needles": ";".join(needles),
                "status": "EXISTS_NEEDLES_CONFIRMED" if ok else "MISSING_SOURCE_OR_NEEDLE",
                "issue": "" if ok else "source path missing or required needles absent",
                "valid_for_claim": flag(False),
                "claim_allowed": flag(False),
                "generated_utc": GENERATED_UTC,
            }
        )
    return rows


def product_compression_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "compression_id": "PCOMP1949_0_start",
            "statement": "1944/1948 runner uses delta_gamma_R11 ~= -(kappa_R/(C_TF U_solar)) nabla^{-2}_local P_TF[R11_ij].",
            "result": "START_FROM_EXISTING_RUNNER_FORM",
            "runner_effect": "separate kappa_R, C_TF, U_solar, inverse-Laplacian, and P_TF inputs are sufficient but not minimal",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "compression_id": "PCOMP1949_1_define_dimensionless_slip",
            "statement": "Define S_TF := -(kappa_R/(C_TF U_solar)) nabla^{-2}_local P_TF[R11_ij].",
            "result": "OBSERVABLE_PRODUCT_DEFINED",
            "runner_effect": "Cassini gamma only needs S_TF, not each microscopic factor separately",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "compression_id": "PCOMP1949_2_acceptance_rule",
            "statement": "The local Cassini smoke comparison becomes abs(S_TF) <= gamma_bound_policy.",
            "result": "RUNNER_RULE_COMPRESSED",
            "runner_effect": "a parent theorem S_TF=0 or a direct bound on S_TF is enough for the gamma gate",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "compression_id": "PCOMP1949_3_identifiability_guard",
            "statement": "Cassini alone cannot identify kappa_R, C_TF, and P_TF separately if only their product enters the observable.",
            "result": "DO_NOT_OVERPARAMETERIZE_CASSINI_GATE",
            "runner_effect": "next work should fill S_TF directly or source a parent decomposition only if needed by other tests",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "compression_id": "PCOMP1949_4_common_mode_guard",
            "statement": "This compression only covers traceless spatial gamma slip; common-mode r^2/effective-G terms stay in Newtonian/cosmology gates.",
            "result": "SCOPE_GUARD_RECORDED",
            "runner_effect": "prevents a Cassini-safe common mode from being mislabelled as local-GR proof",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
    ]


def coefficient_status_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "status_id": "KCP1949_0_kappa_R",
            "symbol": "kappa_R",
            "current_status": "MISSING_SEPARATE_NORMALIZATION",
            "compressed_role": "absorbed into S_TF product for Cassini gamma",
            "still_needed_separately_for": "cross-test consistency, action normalization, and non-Cassini residual predictions",
            "claim_impact": "not separately fatal to Cassini smoke if S_TF is sourced directly",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "status_id": "KCP1949_1_C_TF",
            "symbol": "C_TF",
            "current_status": "MISSING_WEAK_FIELD_NORMALIZATION",
            "compressed_role": "absorbed into S_TF product after convention/gauge choice",
            "still_needed_separately_for": "deriving PPN beta/alpha residuals and comparing independent gauges",
            "claim_impact": "not separately fatal to Cassini smoke if S_TF is sourced directly",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "status_id": "KCP1949_2_PTF",
            "symbol": "P_TF[R11_ij]",
            "current_status": "MISSING_PROJECTED_R11_TF_AMPLITUDE",
            "compressed_role": "numerator of S_TF product",
            "still_needed_separately_for": "theorem-zero proof, source profile, and cross-arena predictions",
            "claim_impact": "fatal unless S_TF itself is theorem-zero or directly bounded",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "status_id": "KCP1949_3_U_and_boundary",
            "symbol": "U_solar_frame,nabla^{-2}_local",
            "current_status": "MISSING_FRAME_AND_BOUNDARY_CONVENTION",
            "compressed_role": "included in dimensionless S_TF amplitude",
            "still_needed_separately_for": "turning an operator-level source into a solar-system observable",
            "claim_impact": "fatal unless S_TF is supplied as an already projected dimensionless observable",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
    ]


def compressed_input_ledger_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "input_id": "CSI1949_0_gamma_bound_policy",
            "symbol": "gamma_bound_policy",
            "definition": "private conservative Cassini screening threshold from 1947",
            "current_value": "6.700000e-05",
            "units": "dimensionless",
            "status": "NUMERIC_POLICY_AVAILABLE_NONCLAIM",
            "source_ref": "CBP1947_2_abs_two_sigma_screen",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "input_id": "CSI1949_1_S_TF",
            "symbol": "S_TF",
            "definition": "-(kappa_R/(C_TF U_solar)) nabla^{-2}_local P_TF[R11_ij]",
            "current_value": "MISSING",
            "units": "dimensionless",
            "status": "MISSING_COMPRESSED_SLIP_AMPLITUDE",
            "source_ref": "PCOMP1949_1_define_dimensionless_slip",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "input_id": "CSI1949_2_S_TF_zero_theorem",
            "symbol": "S_TF=0",
            "definition": "parent-signed theorem-zero route equivalent to P_TF zero or projected slip silence",
            "current_value": "NOT_PARENT_SIGNED",
            "units": "boolean/theorem",
            "status": "MISSING_PARENT_SIGNED_ZERO_THEOREM",
            "source_ref": "RUN1948_1_theorem_zero_branch",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
    ]


def runner_update_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "runner_id": "RUN1949_0_compressed_schema",
            "prediction": "delta_gamma_R11 ~= S_TF",
            "acceptance_rule": "abs(S_TF) <= gamma_bound_policy",
            "current_prediction": "MISSING_COMPRESSED_SLIP_AMPLITUDE",
            "runner_status": "SCHEMA_SIMPLIFIED_INPUTS_MISSING",
            "missing_inputs": "S_TF or parent-signed S_TF=0",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "runner_id": "RUN1949_1_theorem_zero_shortcut",
            "prediction": "S_TF=0",
            "acceptance_rule": "0 <= gamma_bound_policy",
            "current_prediction": "NOT_PARENT_SIGNED",
            "runner_status": "WOULD_PASS_IF_PARENT_SIGNED_BLOCKED",
            "missing_inputs": "parent-signed projected slip zero theorem",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1949_0_product_compression",
            "claim": "Cassini gamma slip gate can be compressed to one dimensionless S_TF product.",
            "status": "PASS_NONCLAIM",
            "reason": "algebraic compression follows from the 1944/1948 runner equation",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1949_1_overparameterization_guard",
            "claim": "Separate kappa_R/C_TF/P_TF are not individually required for a first Cassini smoke comparison if S_TF is supplied.",
            "status": "PASS_NONCLAIM",
            "reason": "only the product enters delta_gamma_R11 at this order",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1949_2_S_TF_numeric",
            "claim": "MTS supplies numeric S_TF.",
            "status": "FAIL_BLOCKED",
            "reason": "compressed slip amplitude is missing",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1949_3_S_TF_zero_theorem",
            "claim": "MTS parent signs S_TF=0.",
            "status": "FAIL_BLOCKED",
            "reason": "projected slip zero theorem remains unsigned",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1949_4_Cassini_pass",
            "claim": "MTS passes Cassini gamma.",
            "status": "FAIL_BLOCKED",
            "reason": "no numeric or theorem-zero S_TF exists",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1949_5_local_GR_PPN",
            "claim": "MTS derives local GR/PPN.",
            "status": "FAIL_BLOCKED",
            "reason": "Cassini S_TF and other PPN residuals remain open",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1949_6_public_claim",
            "claim": "1949 is public-ready Cassini/local-GR evidence.",
            "status": "FAIL_BLOCKED",
            "reason": "private compression checkpoint only",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1949_0_compression",
            "decision": "CASSINI_GATE_REDUCED_TO_S_TF",
            "reason": "the observable only sees the dimensionless projected slip product at leading weak-field order",
            "next_action": "fill S_TF directly, prove S_TF=0, or only then decompose into kappa_R/C_TF/P_TF for cross-test consistency",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1949_1_primary_target",
            "decision": "TARGET_DIMENSIONLESS_STF_SOURCE_NEXT",
            "reason": "one projected observable amplitude is a cleaner first target than three separately unidentifiable factors",
            "next_action": "derive/source S_TF from R11 local operator, or prove projected slip zero",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "next_id": "NEXT1949_0_primary",
            "priority": "selected",
            "target_doc": "1950-Y5-R2FR-dimensionless-STF-slip-source-or-zero-theorem.md",
            "target_script": "scripts/Y5_R2FR_dimensionless_STF_slip_source_or_zero_theorem_1950.py",
            "objective": "derive/source the compressed dimensionless slip amplitude S_TF or prove S_TF=0 from the local R11 branch",
            "acceptance_output": "numeric/source-backed S_TF row, parent-signed S_TF=0 theorem, or explicit blocker ledger keeping Cassini blocked",
            "nonclaim_rule": "do not claim Cassini/local-GR pass unless S_TF is numeric below bound or theorem-zero",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        }
    ]


def status_snapshot_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "snapshot_id": "SNAP1949_0_project_position",
            "status": "CASSINI_GATE_COMPRESSED_TO_DIMENSIONLESS_STF_SLIP_AMPLITUDE",
            "strongest_result": "delta_gamma_R11 ~= S_TF, where S_TF=-(kappa_R/(C_TF U_solar)) nabla^{-2}_local P_TF[R11_ij]",
            "what_improved": "the next local-GR target is one observable amplitude rather than a pile of separately unidentifiable coefficients",
            "still_missing": "numeric/source-backed S_TF or parent-signed S_TF=0 theorem",
            "claim_status": "Cassini/local-GR public claims remain blocked",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        }
    ]


def copy_branch_artifacts(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    write_csv(BRANCH_COPIES["source_weight_product"], rows_by_name["product_compression"])
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


def formalization_1949_artifact_count() -> int:
    if not FORMALIZATION.exists():
        return 0
    return sum(1 for _ in FORMALIZATION.rglob("*1949*"))


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
    rows.append(validation_row("VAL1949_00_sources", "PASS" if sources_ok else "FAIL", "all local source paths exist and needles found" if sources_ok else "source path or needle missing"))

    compression_text = "\n".join(row["result"] + " " + row["statement"] for row in rows_by_name["product_compression"])
    compression_ok = "OBSERVABLE_PRODUCT_DEFINED" in compression_text and "RUNNER_RULE_COMPRESSED" in compression_text
    rows.append(validation_row("VAL1949_01_product_compression", "PASS" if compression_ok else "FAIL", "S_TF product and runner rule defined"))

    coefficient_ok = all(row["valid_for_claim"] == flag(False) for row in rows_by_name["coefficient_status"]) and any(row["symbol"] == "P_TF[R11_ij]" for row in rows_by_name["coefficient_status"])
    rows.append(validation_row("VAL1949_02_coefficient_status", "PASS" if coefficient_ok else "FAIL", "coefficient statuses remain nonclaim and PTF tracked"))

    input_ok = any(row["symbol"] == "S_TF" and row["status"] == "MISSING_COMPRESSED_SLIP_AMPLITUDE" for row in rows_by_name["compressed_input_ledger"])
    rows.append(validation_row("VAL1949_03_compressed_inputs", "PASS" if input_ok else "FAIL", "compressed S_TF input missing as intended"))

    runner_ok = rows_by_name["runner_update"][0]["runner_status"] == "SCHEMA_SIMPLIFIED_INPUTS_MISSING"
    rows.append(validation_row("VAL1949_04_runner_update", "PASS" if runner_ok else "FAIL", "compressed runner schema remains blocked"))

    claim_rows = rows_by_name["claim_gate"]
    claim_ok = len([row for row in claim_rows if row["status"] == "PASS_NONCLAIM"]) == 2 and len([row for row in claim_rows if row["status"] == "FAIL_BLOCKED"]) == 5
    rows.append(validation_row("VAL1949_05_claim_gates", "PASS" if claim_ok else "FAIL", "only compression nonclaim gates pass; claims blocked"))

    decision_ok = any(row["decision"] == "TARGET_DIMENSIONLESS_STF_SOURCE_NEXT" for row in rows_by_name["decision"])
    rows.append(validation_row("VAL1949_06_decision", "PASS" if decision_ok else "FAIL", "dimensionless STF source selected"))

    next_ok = rows_by_name["next_target"][0]["target_doc"].startswith("1950-Y5-R2FR-dimensionless-STF-slip-source")
    rows.append(validation_row("VAL1949_07_next_target", "PASS" if next_ok else "FAIL", "1950 S_TF target selected"))

    flags_ok = all(row.get("valid_for_claim") == flag(False) and row.get("claim_allowed") == flag(False) for table in rows_by_name.values() for row in table)
    rows.append(validation_row("VAL1949_08_claim_flags_safe", "PASS" if flags_ok else "FAIL", "claim flags all false"))

    output_paths = [path for key, path in OUTPUTS.items() if key != "validation"]
    csv_ok = all(csv_has_rows(path) for path in output_paths)
    rows.append(validation_row("VAL1949_09_csv_parse", "PASS" if csv_ok else "FAIL", "all generated CSVs parse with rows"))

    branch_ok = all(csv_has_rows(path) for path in BRANCH_COPIES.values())
    rows.append(validation_row("VAL1949_10_branch_copies", "PASS" if branch_ok else "FAIL", "; ".join(str(path) for path in BRANCH_COPIES.values())))

    pycache_absent = not (Path(__file__).resolve().parent / "__pycache__").exists()
    rows.append(validation_row("VAL1949_11_pycache_absent", "PASS" if pycache_absent else "FAIL", "scripts __pycache__ absent"))

    formalization_count = formalization_1949_artifact_count()
    rows.append(validation_row("VAL1949_12_formalization_untouched", "PASS" if formalization_count == 0 else "FAIL", f"formalization_1949_artifact_count={formalization_count}"))

    overall_ok = all(row["status"] == "PASS" for row in rows)
    rows.append(validation_row("VAL1949_OVERALL", "PASS" if overall_ok else "FAIL", "1949 R11 PTF source or kappa CTF normalization"))
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
        "# 1949 Y5 R2FR: R11 PTF Source or Kappa/CTF Normalization",
        "",
        "## Verdict",
        "",
        "1949 simplifies the Cassini gamma problem. The previous runner listed `kappa_R`, `C_TF`, `U_solar_frame`, inverse-Laplacian boundary data, and `P_TF[R11_ij]` separately. That is sufficient, but for the first Cassini smoke gate it is not minimal.",
        "",
        "The observable combination is one dimensionless projected slip amplitude: `S_TF := -(kappa_R/(C_TF U_solar)) nabla^{-2}_local P_TF[R11_ij]`. The runner can therefore become `abs(S_TF) <= gamma_bound_policy`.",
        "",
        "This does not prove Cassini safety. It tightens the next target: either derive/source `S_TF` directly, prove `S_TF=0`, or later decompose it into `kappa_R/C_TF/P_TF` for cross-test consistency. Common-mode residuals remain outside this gamma-only compression.",
        "",
        "## Source Register",
        "",
        markdown_table(rows_by_name["source_register"]),
        "",
        "## Product Compression",
        "",
        markdown_table(rows_by_name["product_compression"]),
        "",
        "## Kappa/CTF/PTF Status",
        "",
        markdown_table(rows_by_name["coefficient_status"]),
        "",
        "## Compressed Input Ledger",
        "",
        markdown_table(rows_by_name["compressed_input_ledger"]),
        "",
        "## Runner Update",
        "",
        markdown_table(rows_by_name["runner_update"]),
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

    rows_by_name = {
        "source_register": source_register_rows(),
        "product_compression": product_compression_rows(),
        "coefficient_status": coefficient_status_rows(),
        "compressed_input_ledger": compressed_input_ledger_rows(),
        "runner_update": runner_update_rows(),
        "claim_gate": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
        "status_snapshot": status_snapshot_rows(),
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
