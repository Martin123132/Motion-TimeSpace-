from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
RAB = ROOT / "source-intake" / "rab-sector"
RAB_DOCS = RAB / "docs"
RAB_RAW = RAB / "raw"
RAB_ACCEPTED = RAB / "accepted"
RAB_QUEUE = RAB / "acquisition-queue"
RAB_EXTERNAL = RAB / "external" / "r10" / "1569"
MICROSCOPE = ROOT / "source-intake" / "microscope"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1569-Y5-RAB-first-internal-ZR-or-tauR10-projection-row.md"
START_TS = datetime.now(timezone.utc).timestamp()
R10_CROSSREF = RAB_EXTERNAL / "crossref_10.1103_PhysRevLett.126.211101.json"

SOURCE_FILES = {
    "1568_doc": ROOT / "1568-Y5-RAB-parent-contract-derivation-from-MTS-primitives-or-first-live-ZR-row.md",
    "1568_validation": OUT / "P8_Y5_BRR545_1568_VALIDATION.csv",
    "1568_decision": OUT / "P8_Y5_PARENT_QLOC_1568_DECISION.csv",
    "1568_bound": OUT / "P8_Y5_PARENT_QLOC_1568_FIRST_EXTERNAL_BOUND_SOURCE_ROW.csv",
    "1568_coeff": OUT / "P8_Y5_PARENT_QLOC_1568_FIRST_INTERNAL_COEFFICIENT_ROW_STATUS.csv",
    "1567_acquisition": OUT / "P8_Y5_PARENT_QLOC_1567_LIVE_SOURCE_ACQUISITION_QUEUE.csv",
    "1567_blueprint": RAB_DOCS / "ZR1567_LIVE_FINITE_ZR_ROW_BLUEPRINT_NONCLAIM.csv",
    "1566_validator": OUT / "P8_Y5_PARENT_QLOC_1566_FINITE_ZR_VALIDATOR_RULES.csv",
    "1237_tests": OUT / "P8_Y5_R10_1237_FINITE_RESIDUAL_TEST_TRACK.csv",
    "1237_local": OUT / "P8_Y5_R10_1237_LOCAL_GR_CONNECTION_STATUS.csv",
    "r10_crossref": R10_CROSSREF,
}

NEEDLES = {
    "1568_doc": ["No internal `Z_R`, `J_R`, `B_R`, or `tau_R10` row is source-ready", "first external bound source row"],
    "1568_validation": ["VAL1568_OVERALL", "PASS"],
    "1568_decision": ["DEC1568_3_next", "NEXT_1569_FIRST_INTERNAL_ZR_OR_TAU_R10_PROJECTION_ROW"],
    "1568_bound": ["BOUND1568_R10_EOTWASH_PRL_2021", "external_arena_bound_only"],
    "1568_coeff": ["COEFF1568_4_verdict", "NO_INTERNAL_ROW_READY"],
    "1567_acquisition": ["ACQ1567_1_ZR", "ACQ1567_5_tau_R10"],
    "1567_blueprint": ["ZR1567_BLUEPRINT_TAU_R10", "MISSING_TRANSFER_KERNEL"],
    "1566_validator": ["RULE1566_1_no_missing_markers", "MISSING_MARKER_PRESENT"],
    "1237_tests": ["TEST1237_0_QR_hair", "FINITE_RESIDUAL_REQUIRED_UNLESS_FIRST_CLASS_CONSTRAINT"],
    "1237_local": ["LGR1237_5_verdict", "NOT_DERIVED"],
    "r10_crossref": ["Combined Test of the Gravitational Inverse-Square Law at the Centimeter Range", "10.1103"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1569_SOURCE_REGISTER.csv"
LOCAL_SOURCE_AUDIT = OUT / "P8_Y5_PARENT_QLOC_1569_LOCAL_SOURCE_AUDIT.csv"
ZR_ATTEMPT = OUT / "P8_Y5_PARENT_QLOC_1569_ZR_THEOREM_OR_COEFFICIENT_ATTEMPT.csv"
TAU_ATTEMPT = OUT / "P8_Y5_PARENT_QLOC_1569_TAU_R10_PROJECTION_ATTEMPT.csv"
EXTERNAL_BOUND = OUT / "P8_Y5_PARENT_QLOC_1569_EXTERNAL_R10_BOUND_METADATA_ROW.csv"
INTERNAL_ROW = OUT / "P8_Y5_PARENT_QLOC_1569_FIRST_INTERNAL_ROW_STATUS.csv"
TEMPLATE = RAB_DOCS / "ZR1569_TAU_R10_PROJECTION_ROW_TEMPLATE_NONCLAIM.csv"
QUEUE_COPY = RAB_QUEUE / "ZR1569_EXTERNAL_R10_BOUND_METADATA_ROW_NONCLAIM.csv"
RUNNER = OUT / "P8_Y5_PARENT_QLOC_1569_RUNNER_NONCLAIM.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1569_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1569_DECISION.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1569_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1569_VALIDATION.csv"

QUARANTINE = MICROSCOPE / "quarantine" / "1569"
COPY_TARGETS = {
    LOCAL_SOURCE_AUDIT: [
        QUARANTINE / "LOCAL_SOURCE_AUDIT_NONCLAIM.csv",
        BRANCH_RESIDUALS / "local_source_audit_nonclaim_1569.csv",
    ],
    ZR_ATTEMPT: [
        QUARANTINE / "ZR_THEOREM_OR_COEFFICIENT_ATTEMPT_NONCLAIM.csv",
        BRANCH_RESIDUALS / "ZR_theorem_or_coefficient_attempt_nonclaim_1569.csv",
    ],
    TAU_ATTEMPT: [
        QUARANTINE / "TAU_R10_PROJECTION_ATTEMPT_NONCLAIM.csv",
        BRANCH_RESIDUALS / "tau_R10_projection_attempt_nonclaim_1569.csv",
    ],
    EXTERNAL_BOUND: [
        QUARANTINE / "EXTERNAL_R10_BOUND_METADATA_ROW_NONCLAIM.csv",
        BRANCH_RESIDUALS / "external_R10_bound_metadata_row_nonclaim_1569.csv",
        QUEUE_COPY,
    ],
    INTERNAL_ROW: [
        QUARANTINE / "FIRST_INTERNAL_ROW_STATUS_NONCLAIM.csv",
        BRANCH_RESIDUALS / "first_internal_row_status_nonclaim_1569.csv",
    ],
    DECISION: [
        QUARANTINE / "DECISION_NONCLAIM.csv",
        BRANCH_RESIDUALS / "first_internal_ZR_tauR10_decision_nonclaim_1569.csv",
    ],
}


def flags() -> dict[str, bool]:
    return {
        "numeric_value_present": False,
        "source_backed": False,
        "score_ready": False,
        "valid_prediction_row": False,
        "valid_for_claim": False,
        "claim_allowed": False,
    }


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def source_list(*keys: str) -> str:
    return "; ".join(rel(SOURCE_FILES[key]) for key in keys)


def file_contains(path: Path, needles: list[str]) -> bool:
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8", errors="ignore")
    return all(needle in text for needle in needles)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def parse_csv(path: Path) -> bool:
    read_csv(path)
    return True


def generated_flags_false(paths: list[Path]) -> bool:
    false_values = {"", "false", "0", "no", "none", "null"}
    claim_keys = [
        "numeric_value_present",
        "source_backed",
        "score_ready",
        "valid_prediction_row",
        "valid_for_claim",
        "claim_allowed",
        "accepted_for_scoring",
        "passes_for_claim",
        "ready_for_raw",
        "ready_for_accepted",
    ]
    for path in paths:
        for row in read_csv(path):
            for key in claim_keys:
                if key in row and str(row[key]).strip().lower() not in false_values:
                    return False
    return True


def row_count(folder: Path) -> int:
    if not folder.exists():
        return 0
    total = 0
    for path in folder.glob("*.csv"):
        try:
            total += len(read_csv(path))
        except Exception:
            total += 1
    return total


def source_register_rows() -> list[dict[str, Any]]:
    rows = []
    for index, (key, path) in enumerate(SOURCE_FILES.items()):
        needles = NEEDLES[key]
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "source_id": f"SRC1569_{index}_{key}",
                "source_path": rel(path),
                "exists": path.exists(),
                "needle_found": file_contains(path, needles),
                "needles": "; ".join(needles),
                "purpose": "first internal ZR/tauR10 row attempt and external R10 metadata localization",
                **flags(),
            }
        )
    return rows


def local_source_audit_rows() -> list[dict[str, Any]]:
    anchor = "Combined Test of the Gravitational Inverse-Square Law at the Centimeter Range"
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "audit_id": "LSA1569_0_crossref_metadata",
            "source_path": rel(R10_CROSSREF),
            "source_exists": R10_CROSSREF.exists(),
            "anchor": anchor,
            "anchor_found": file_contains(R10_CROSSREF, [anchor]) if R10_CROSSREF.exists() else False,
            "source_role": "external R10 metadata/provenance only",
            "not_sufficient_for": "digitized alpha(lambda) curve; MTS Z_R/J_R/B_R/tau coefficient; accepted score row",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "audit_id": "LSA1569_1_aps_fulltext",
            "source_path": "https://link.aps.org/doi/10.1103/PhysRevLett.126.211101",
            "source_exists": False,
            "anchor": "APS endpoint returned 403 in local acquisition attempt",
            "anchor_found": False,
            "source_role": "primary DOI page; not locally cached",
            "not_sufficient_for": "local source-backed digitization until accessible PDF/fulltext/table is acquired",
            **flags(),
        },
    ]


def zr_attempt_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "ZR1569_0_theorem_zero",
            "Z_R=0 from parent operator exclusion",
            "requires signed 1567 parent protection contract and 1237 primitive derivation success",
            "FAILED_CURRENT_PARENT_PROOF",
            "1237 says sorted grammar/ParentGenerate exhaustion is closure-only",
        ),
        (
            "ZR1569_1_numeric_coefficient",
            "finite Z_R value",
            "requires parent-normalized coefficient, units, source path, and source anchor",
            "MISSING_INTERNAL_COEFFICIENT",
            "no local source-backed MTS Z_R row exists",
        ),
        (
            "ZR1569_2_mass_gap",
            "M_R^2 or lambda_R=sqrt(Z_R/M_R^2)",
            "requires Hessian/range source in same normalization as Z_R",
            "MISSING_INTERNAL_RANGE",
            "external R10 alpha(lambda) bound does not supply MTS lambda_R",
        ),
        (
            "ZR1569_3_verdict",
            "first internal Z_R row",
            "theorem-zero or finite coefficient",
            "NOT_READY",
            "keep finite residual branch open but unscored",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "attempt_id": attempt_id,
            "target": target,
            "required_input": required_input,
            "status": status,
            "reason": reason,
            "source_paths": source_list("1568_coeff", "1237_local", "1567_acquisition"),
            **flags(),
        }
        for attempt_id, target, required_input, status, reason in rows
    ]


def tau_attempt_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "TAU1569_0_external_form",
            "R10 tests constrain alpha(lambda) in V=-Gm1m2/r[1+alpha exp(-r/lambda)]",
            "external comparison form",
            "FORMAL_EXTERNAL_FORM_ONLY",
            "source metadata localized; full curve/table still needed",
        ),
        (
            "TAU1569_1_internal_range",
            "lambda_R = sqrt(Z_R/M_R^2)",
            "candidate finite R_AB range if Z_R and M_R^2 are parent-normalized",
            "MISSING_ZR_MR2",
            "cannot assign lambda_R from external bound alone",
        ),
        (
            "TAU1569_2_internal_amplitude",
            "alpha_MTS(lambda_R) = tau_R10 * A_R(Z_R,M_R^2,J_R,B_R,readout)",
            "placeholder transfer structure",
            "MISSING_SOURCE_NORMALIZATION",
            "J_R/B_R/readout and geometric source kernel are not derived",
        ),
        (
            "TAU1569_3_projection_kernel",
            "tau_R10 maps finite R_AB residual variables into alpha(lambda)",
            "needed bridge from theory coefficients to R10 bound",
            "KERNEL_CONTRACT_WRITTEN_NOT_FILLED",
            "formula shape exists, but no numeric/theorem-zero kernel",
        ),
        (
            "TAU1569_4_verdict",
            "first tau_R10 row",
            "projection kernel plus local source path/anchor/units",
            "NOT_READY",
            "do not move to raw/accepted",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "projection_id": projection_id,
            "projection_piece": projection_piece,
            "role": role,
            "status": status,
            "blocking_gap": blocking_gap,
            "source_paths": source_list("1568_bound", "r10_crossref", "1567_blueprint"),
            **flags(),
        }
        for projection_id, projection_piece, role, status, blocking_gap in rows
    ]


def external_bound_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "row_id": "EXTBOUND1569_R10_CROSSREF_PRL126_211101",
            "row_type": "external_metadata_localized_nonclaim",
            "arena": "R10",
            "quantity": "alpha(lambda) Yukawa bound source metadata",
            "source_path": rel(R10_CROSSREF),
            "source_anchor": "Combined Test of the Gravitational Inverse-Square Law at the Centimeter Range",
            "doi": "10.1103/PhysRevLett.126.211101",
            "source_url": "https://doi.org/10.1103/PhysRevLett.126.211101",
            "metadata_status": "LOCAL_CROSSREF_METADATA_PRESENT",
            "bound_curve_status": "MISSING_DIGITIZED_ALPHA_LAMBDA_CURVE",
            "why_not_scoreable": "external metadata is not a digitized bound curve and not an MTS tau_R10 projection",
            **flags(),
        }
    ]


def internal_row_status_rows() -> list[dict[str, Any]]:
    rows = [
        ("INT1569_0_ZR", "Z_R", "no theorem-zero; no source-backed coefficient", "BLOCKED"),
        ("INT1569_1_MR2", "M_R^2", "no parent Hessian/range source", "BLOCKED"),
        ("INT1569_2_JR", "J_R", "matter descent/source-current row missing", "BLOCKED"),
        ("INT1569_3_BR", "B_R_or_Pi_Rn", "boundary/corner zero or finite bound missing", "BLOCKED"),
        ("INT1569_4_tau_R10", "tau_R10", "projection kernel not filled; external bound localized only", "BLOCKED"),
        ("INT1569_5_verdict", "first internal accepted/raw row", "not ready; no row moved to raw or accepted", "NO_INTERNAL_ROW_READY"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "status_id": status_id,
            "target": target,
            "current_evidence": current_evidence,
            "status": status,
            "ready_for_raw": False,
            "ready_for_accepted": False,
            **flags(),
        }
        for status_id, target, current_evidence, status in rows
    ]


def template_rows() -> list[dict[str, Any]]:
    rows = [
        ("ZR1569_TEMPLATE_TAU_R10", "tau_R10", "MISSING_TRANSFER_KERNEL", "MISSING_DIMENSIONLESS_OR_KERNEL_UNITS", "MISSING_RAB_TO_ALPHA_NORMALIZATION", "MISSING_R10_PROJECTION_BLOCK", rel(R10_CROSSREF), "Combined Test of the Gravitational Inverse-Square Law at the Centimeter Range", "R10"),
        ("ZR1569_TEMPLATE_ZR", "Z_R", "MISSING_THEOREM_ZERO_OR_NUMERIC_VALUE", "MISSING_PARENT_UNITS", "MISSING_RAB_NORMALIZATION", "MISSING_OPERATOR_EXCLUSION_OR_COEFFICIENT_SOURCE", "MISSING_INTERNAL_SOURCE_PATH", "MISSING_INTERNAL_SOURCE_ANCHOR", "R10;PPN;clock;orbital"),
        ("ZR1569_TEMPLATE_MR2", "M_R^2", "MISSING_HESSIAN_OR_RANGE_VALUE", "MISSING_PARENT_UNITS", "MISSING_RAB_NORMALIZATION", "MISSING_PARENT_HESSIAN_BLOCK", "MISSING_INTERNAL_SOURCE_PATH", "MISSING_INTERNAL_SOURCE_ANCHOR", "R10;PPN;clock;orbital"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "row_id": row_id,
            "coefficient_symbol": coefficient_symbol,
            "coefficient_value": coefficient_value,
            "coefficient_units": coefficient_units,
            "normalization_convention": normalization_convention,
            "parent_action_block": parent_action_block,
            "source_path": source_path,
            "source_anchor": source_anchor,
            "arena_projection": arena_projection,
            "placeholder_status": "MISSING_DO_NOT_SCORE",
            **flags(),
        }
        for row_id, coefficient_symbol, coefficient_value, coefficient_units, normalization_convention, parent_action_block, source_path, source_anchor, arena_projection in rows
    ]


def runner_rows() -> list[dict[str, Any]]:
    rows = [
        ("RUN1569_0_sources", "load 1568/1567/1237 and local R10 metadata", "PASS", "all source register needles found"),
        ("RUN1569_1_ZR", "first internal Z_R theorem/numeric row", "FAILED_CURRENT_PARENT_PROOF", "no theorem-zero and no numeric parent coefficient"),
        ("RUN1569_2_tau_R10", "first tau_R10 projection row", "KERNEL_CONTRACT_WRITTEN_NOT_FILLED", "projection shape written, but internal source normalization and range are missing"),
        ("RUN1569_3_external_bound", "external R10 metadata row", "PASS_NONCLAIM_METADATA_LOCALIZED", "Crossref DOI metadata is local; digitized curve/table still missing"),
        ("RUN1569_4_raw_accepted", "raw/accepted finite rows", "NO_LIVE_SCORE_ROWS", f"raw_rows={row_count(RAB_RAW)}; accepted_rows={row_count(RAB_ACCEPTED)}"),
        ("RUN1569_5_claim", "R10/local GR claim", "BLOCKED_NO_CLAIM", "external bound is not an MTS prediction and internal projection is missing"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": runner_id,
            "test": test,
            "current_status": current_status,
            "detail": detail,
            **flags(),
        }
        for runner_id, test, current_status, detail in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("GATE1569_0_ZR", "Z_R theorem-zero or finite coefficient", "BLOCKED_NO_CLAIM", "no parent theorem and no source-backed coefficient"),
        ("GATE1569_1_tau_R10", "tau_R10 projection kernel", "BLOCKED_NO_CLAIM", "projection formula lacks internal source normalization"),
        ("GATE1569_2_external_bound", "external R10 bound metadata", "PASS_SOURCE_QUEUE_NONCLAIM", "metadata localized but no bound curve and no MTS prediction"),
        ("GATE1569_3_raw_accepted", "raw/accepted finite row", "BLOCKED_NO_CLAIM", "no internal row moved to raw/accepted"),
        ("GATE1569_4_local_GR", "derived local GR/Newton/R10 safety", "BLOCKED_NO_CLAIM", "theory side remains missing"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "claim_gate": claim_gate,
            "status": status,
            "reason": reason,
            "source_paths": source_list("1568_doc", "r10_crossref", "1237_tests"),
            **flags(),
        }
        for gate_id, claim_gate, status, reason in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1569_0_ZR",
            "decision": "first internal Z_R row",
            "result": "NOT_READY",
            "reason": "Z_R needs parent theorem-zero or source-backed coefficient/range",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1569_1_tau",
            "decision": "tau_R10 projection",
            "result": "KERNEL_CONTRACT_WRITTEN_NOT_FILLED",
            "reason": "formal Yukawa comparison shape exists but source normalization and internal coefficients are missing",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1569_2_bound",
            "decision": "external R10 source",
            "result": "LOCAL_METADATA_ROW_READY_NONCLAIM",
            "reason": "Crossref DOI metadata localized; full curve/table acquisition still needed",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1569_3_next",
            "decision": "next target",
            "result": "NEXT_1570_R10_CURVE_DIGITIZATION_OR_TAU_KERNEL_SOURCE_NORMALIZATION",
            "reason": "either digitize/acquire the R10 alpha(lambda) bound curve or derive the internal source-normalized tau_R10 kernel",
            **flags(),
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "next_id": "NEXT1569_0_1570",
            "next_target": "1570-Y5-RAB-R10-curve-digitization-or-tau-kernel-source-normalization.md",
            "script": "scripts/Y5_RAB_R10_curve_digitization_or_tau_kernel_source_normalization.py",
            "objective": "try to acquire/digitize a real R10 alpha(lambda) bound curve and separately derive the tau_R10 source-normalization kernel; keep both nonclaim until internal MTS coefficients and projection are real",
            "do_not": "do not treat Crossref metadata as a bound curve; do not treat external bounds as MTS coefficients; do not edit formalization-workbench",
            **flags(),
        }
    ]


def copy_outputs() -> None:
    for source, destinations in COPY_TARGETS.items():
        for destination in destinations:
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, destination)


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def formalization_modified_count_since_start() -> int:
    if not FORMALIZATION.exists():
        return 0
    return sum(1 for path in FORMALIZATION.rglob("*") if path.is_file() and path.stat().st_mtime >= START_TS)


def validation_rows(generated_csvs: list[Path]) -> list[dict[str, Any]]:
    sources = read_csv(SOURCE_REGISTER)
    local_sources = read_csv(LOCAL_SOURCE_AUDIT)
    zr = read_csv(ZR_ATTEMPT)
    tau = read_csv(TAU_ATTEMPT)
    external = read_csv(EXTERNAL_BOUND)
    internal = read_csv(INTERNAL_ROW)
    template = read_csv(TEMPLATE)
    run_rows = read_csv(RUNNER)
    gate_rows = read_csv(CLAIM_GATE)
    decision_items = read_csv(DECISION)
    next_rows = read_csv(NEXT_TARGET)

    checks = [
        ("VAL1569_0_sources_exist", all(row["exists"] == "True" for row in sources), "all cited 1569 source paths exist"),
        ("VAL1569_1_needles_found", all(row["needle_found"] == "True" for row in sources), "all registered evidence needles found"),
        ("VAL1569_2_local_metadata", any(row["audit_id"] == "LSA1569_0_crossref_metadata" and row["source_exists"] == "True" and row["anchor_found"] == "True" for row in local_sources), "Crossref R10 metadata is local and anchored"),
        ("VAL1569_3_ZR_not_ready", any(row["attempt_id"] == "ZR1569_3_verdict" and row["status"] == "NOT_READY" for row in zr), "Z_R row remains not ready"),
        ("VAL1569_4_tau_contract_not_filled", any(row["projection_id"] == "TAU1569_3_projection_kernel" and row["status"] == "KERNEL_CONTRACT_WRITTEN_NOT_FILLED" for row in tau), "tau_R10 kernel contract is written but not filled"),
        ("VAL1569_5_external_bound_nonclaim", any(row["row_id"] == "EXTBOUND1569_R10_CROSSREF_PRL126_211101" and row["metadata_status"] == "LOCAL_CROSSREF_METADATA_PRESENT" for row in external), "external metadata row exists"),
        ("VAL1569_6_no_internal_row", any(row["status_id"] == "INT1569_5_verdict" and row["status"] == "NO_INTERNAL_ROW_READY" for row in internal), "no internal row is ready"),
        ("VAL1569_7_template_nonclaim", len(template) >= 3 and all("MISSING" in row["placeholder_status"] for row in template), "tau/ZR template remains nonclaim"),
        ("VAL1569_8_raw_accepted_empty", row_count(RAB_RAW) == 0 and row_count(RAB_ACCEPTED) == 0, "raw/accepted finite rows remain empty"),
        ("VAL1569_9_runner_blocks_claim", any(row["runner_id"] == "RUN1569_5_claim" and row["current_status"] == "BLOCKED_NO_CLAIM" for row in run_rows), "runner blocks local/R10 claim"),
        ("VAL1569_10_claim_gates", all(row["claim_allowed"] == "False" for row in gate_rows) and any(row["status"] == "BLOCKED_NO_CLAIM" for row in gate_rows), "claim gates remain closed"),
        ("VAL1569_11_decision_next", any(row["result"] == "NEXT_1570_R10_CURVE_DIGITIZATION_OR_TAU_KERNEL_SOURCE_NORMALIZATION" for row in decision_items), "decision selects curve digitization or tau kernel"),
        ("VAL1569_12_next_target", any("1570-Y5-RAB-R10-curve-digitization" in row["next_target"] for row in next_rows), "next target is R10 curve digitization or tau kernel"),
        ("VAL1569_13_csv_parse", all(parse_csv(path) for path in generated_csvs), "all generated 1569 CSVs parse cleanly"),
        ("VAL1569_14_claim_flags_false", generated_flags_false(generated_csvs), "all generated prediction/claim flags remain false"),
        ("VAL1569_15_branch_copies", all(destination.exists() for destinations in COPY_TARGETS.values() for destination in destinations), "branch/quarantine nonclaim copies written"),
        ("VAL1569_16_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent after run"),
        ("VAL1569_17_formalization_untouched", formalization_modified_count_since_start() == 0, "formalization modified-file count since start=0"),
    ]
    overall = all(result for _, result, _ in checks)
    rows = [
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail,
        }
        for check_id, result, detail in checks
    ]
    rows.append(
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": "VAL1569_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1569 first internal ZR or tauR10 projection row validation",
        }
    )
    return rows


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |")
    return "\n".join([header, sep, *body])


def write_doc(
    sources: list[dict[str, Any]],
    local_sources: list[dict[str, Any]],
    zr: list[dict[str, Any]],
    tau: list[dict[str, Any]],
    external: list[dict[str, Any]],
    internal: list[dict[str, Any]],
    template: list[dict[str, Any]],
    run_rows: list[dict[str, Any]],
    gate_rows: list[dict[str, Any]],
    decision_items: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n".join(
            [
                "# 1569 - R_AB First Internal Z_R or tau_R10 Projection Row",
                "",
                "## Verdict",
                "- The first external R10 metadata source is now localized and anchored through Crossref, but it is not a digitized `alpha(lambda)` bound curve.",
                "- The first internal MTS row still cannot be filled: `Z_R`, `M_R^2`, `J_R`, `B_R`, and `tau_R10` lack theorem-zeroes or source-backed values.",
                "- A formal `tau_R10` bridge has been written in the correct Yukawa comparison language, but the source-normalization kernel is missing.",
                "- No row was moved to raw or accepted; all rows remain private nonclaim.",
                "- No `Z_R=0`, `q_R=0`, R10, PPN, WEP, clock, orbital, local GR, or Newton claim is made.",
                "",
                "## Source Register",
                md_table(sources, ["source_id", "source_path", "exists", "needle_found", "needles"]),
                "",
                "## Local Source Audit",
                md_table(local_sources, ["audit_id", "source_path", "source_exists", "anchor", "anchor_found", "source_role", "not_sufficient_for"]),
                "",
                "## Z_R Attempt",
                md_table(zr, ["attempt_id", "target", "required_input", "status", "reason"]),
                "",
                "## tau_R10 Projection Attempt",
                md_table(tau, ["projection_id", "projection_piece", "role", "status", "blocking_gap"]),
                "",
                "## External R10 Bound Metadata Row",
                md_table(external, ["row_id", "row_type", "arena", "quantity", "source_path", "doi", "metadata_status", "bound_curve_status", "why_not_scoreable"]),
                "",
                "## First Internal Row Status",
                md_table(internal, ["status_id", "target", "current_evidence", "status", "ready_for_raw", "ready_for_accepted"]),
                "",
                "## Projection Template",
                md_table(template, ["row_id", "coefficient_symbol", "coefficient_value", "coefficient_units", "normalization_convention", "parent_action_block", "source_path", "source_anchor", "arena_projection", "placeholder_status"]),
                "",
                "## Runner",
                md_table(run_rows, ["runner_id", "test", "current_status", "detail"]),
                "",
                "## Claim Gates",
                md_table(gate_rows, ["gate_id", "claim_gate", "status", "reason"]),
                "",
                "## Decision",
                md_table(decision_items, ["decision_id", "decision", "result", "reason"]),
                "",
                "## Validation",
                md_table(validation, ["check_id", "result", "detail"]),
                "",
                "## Next Target",
                md_table(next_rows, ["next_target", "script", "objective", "do_not"]),
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> None:
    sources = source_register_rows()
    local_sources = local_source_audit_rows()
    zr = zr_attempt_rows()
    tau = tau_attempt_rows()
    external = external_bound_rows()
    internal = internal_row_status_rows()
    template = template_rows()
    run_rows = runner_rows()
    gate_rows = claim_gate_rows()
    decision_items = decision_rows()
    next_rows = next_target_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(LOCAL_SOURCE_AUDIT, local_sources)
    write_csv(ZR_ATTEMPT, zr)
    write_csv(TAU_ATTEMPT, tau)
    write_csv(EXTERNAL_BOUND, external)
    write_csv(INTERNAL_ROW, internal)
    write_csv(TEMPLATE, template)
    write_csv(RUNNER, run_rows)
    write_csv(CLAIM_GATE, gate_rows)
    write_csv(DECISION, decision_items)
    write_csv(NEXT_TARGET, next_rows)
    copy_outputs()
    remove_pycache()

    generated_csvs = [
        SOURCE_REGISTER,
        LOCAL_SOURCE_AUDIT,
        ZR_ATTEMPT,
        TAU_ATTEMPT,
        EXTERNAL_BOUND,
        INTERNAL_ROW,
        TEMPLATE,
        RUNNER,
        CLAIM_GATE,
        DECISION,
        NEXT_TARGET,
    ]
    validation = validation_rows(generated_csvs)
    write_csv(VALIDATION, validation)
    write_doc(sources, local_sources, zr, tau, external, internal, template, run_rows, gate_rows, decision_items, validation, next_rows)


if __name__ == "__main__":
    main()
