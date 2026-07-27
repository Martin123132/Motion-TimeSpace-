from __future__ import annotations

import csv
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FORMALIZATION = ROOT.parent / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
RAB_SECTOR = ROOT / "source-intake" / "rab-sector"
RAW = RAB_SECTOR / "raw"
ACCEPTED = RAB_SECTOR / "accepted"
QUEUE = RAB_SECTOR / "acquisition-queue"
QUARANTINE = MICROSCOPE / "quarantine" / "1631"
INPUT_1631 = QUARANTINE / "input"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1631-Y5-R2FR-JR-prior-width-source-acquisition-or-tau-kernel-first-row.md"

SOURCE_FILES = {
    "1630_doc": ROOT / "1630-Y5-R2FR-action-scale-measure-owner-or-JR-prior-width-runner.md",
    "1630_validation": OUT / "P8_Y5_BRR545_1630_VALIDATION.csv",
    "1630_next": OUT / "P8_Y5_PARENT_QLOC_1630_NEXT_TARGET.csv",
    "1630_inputs": OUT / "P8_Y5_PARENT_QLOC_1630_PRIOR_WIDTH_RUNNER_INPUTS.csv",
    "1630_refusal": OUT / "P8_Y5_PARENT_QLOC_1630_PRIOR_WIDTH_REFUSAL_RUNNER.csv",
    "1629_prior_widths": OUT / "P8_Y5_PARENT_QLOC_1629_FINITE_JR_PIR_PRIOR_WIDTH_ROWS.csv",
    "jr1627_contract": QUEUE / "JR1627_FIRST_FINITE_SOURCE_ROW_CONTRACT_NONCLAIM.csv",
    "jr1628_acquisition": QUEUE / "JR1628_BOUND_ACQUISITION_LEDGER_NONCLAIM.csv",
    "jr1629_prior_widths": QUEUE / "JR1629_FINITE_JR_PIR_PRIOR_WIDTH_ROWS_NONCLAIM.csv",
    "jr1630_refusal": QUEUE / "JR1630_PRIOR_WIDTH_REFUSAL_RUNNER_NONCLAIM.csv",
    "r10_reviewed_curve": QUEUE / "R10_alpha_lambda_bound_curve_DIGITIZED_1572_REVIEWED_CANDIDATE_NONCLAIM.csv",
    "zr1568_external_bound": QUEUE / "ZR1568_FIRST_EXTERNAL_BOUND_SOURCE_ROW_NONCLAIM.csv",
    "zr1569_external_metadata": QUEUE / "ZR1569_EXTERNAL_R10_BOUND_METADATA_ROW_NONCLAIM.csv",
}

NEEDLES = {
    "1630_doc": ["PRIOR_WIDTH_REFUSAL_RUNNER_BUILT", "VAL1630_OVERALL"],
    "1630_validation": ["VAL1630_OVERALL", "PASS"],
    "1630_next": ["1631-Y5-R2FR-JR-prior-width-source-acquisition-or-tau-kernel-first-row.md", "first source-backed finite input"],
    "1630_inputs": ["PWI1630_1_JR", "MISSING_INPUT_REJECTED"],
    "1630_refusal": ["RUN1630_7_local_GR_lock", "REFUSE_SCORING"],
    "1629_prior_widths": ["PW1629_4_tau_R10_width", "MISSING_R10_WIDTH_KERNEL"],
    "jr1627_contract": ["FJR1627_0_first_finite_JR_contract", "FINITE_JR_ROW_CONTRACT_STAGED_NONCLAIM"],
    "jr1628_acquisition": ["JRA1628_1_finite_JR_bound", "MISSING_NUMERIC_JR_SOURCE_BOUND"],
    "jr1629_prior_widths": ["PW1629_0_epsilon_RAB_source", "MISSING_RAB_SOURCE_SLOT_ZERO_OR_PRIOR_WIDTH"],
    "jr1630_refusal": ["RUN1630_0_epsilon_RAB_source", "REFUSE_SCORING"],
    "r10_reviewed_curve": ["REVIEWED_QA_CANDIDATE_NONCLAIM", "accepted_for_scoring"],
    "zr1568_external_bound": ["external_arena_bound_only", "not an MTS Z_R/J_R/B_R/tau coefficient"],
    "zr1569_external_metadata": ["external_metadata_localized_nonclaim", "not a digitized bound curve and not an MTS tau_R10 projection"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1631_SOURCE_REGISTER.csv"
INTAKE_SCAN = OUT / "P8_Y5_PARENT_QLOC_1631_INTAKE_SCAN.csv"
CANDIDATE_CLASSIFICATION = OUT / "P8_Y5_PARENT_QLOC_1631_CANDIDATE_CLASSIFICATION.csv"
FIRST_ROW_ATTEMPT = OUT / "P8_Y5_PARENT_QLOC_1631_FIRST_SOURCE_BACKED_ROW_ATTEMPT.csv"
R10_ASSET_LEDGER = OUT / "P8_Y5_PARENT_QLOC_1631_R10_BOUND_ASSET_LEDGER.csv"
BLOCKER_LEDGER = OUT / "P8_Y5_PARENT_QLOC_1631_ACQUISITION_BLOCKER_LEDGER.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1631_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1631_DECISION.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1631_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1631_VALIDATION.csv"

COPY_TARGETS = {
    INTAKE_SCAN: [
        QUARANTINE / "INTAKE_SCAN_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_intake_scan_nonclaim_1631.csv",
    ],
    CANDIDATE_CLASSIFICATION: [
        QUARANTINE / "CANDIDATE_CLASSIFICATION_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_candidate_classification_nonclaim_1631.csv",
    ],
    FIRST_ROW_ATTEMPT: [
        QUARANTINE / "FIRST_SOURCE_BACKED_ROW_ATTEMPT_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_first_source_backed_row_attempt_nonclaim_1631.csv",
    ],
    R10_ASSET_LEDGER: [
        QUARANTINE / "R10_BOUND_ASSET_LEDGER_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_R10_bound_asset_ledger_nonclaim_1631.csv",
        QUEUE / "JR1631_R10_BOUND_ASSET_LEDGER_NONCLAIM.csv",
    ],
    BLOCKER_LEDGER: [
        QUARANTINE / "ACQUISITION_BLOCKER_LEDGER_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_acquisition_blocker_ledger_nonclaim_1631.csv",
        QUEUE / "JR1631_ACQUISITION_BLOCKER_LEDGER_NONCLAIM.csv",
    ],
    CLAIM_GATE: [
        QUARANTINE / "CLAIM_GATE_CLOSED.csv",
        BRANCH_RESIDUALS / "R2FR_claim_gate_closed_1631.csv",
    ],
    NEXT_TARGET: [
        QUARANTINE / "NEXT_TARGET.csv",
        BRANCH_RESIDUALS / "R2FR_next_target_1631.csv",
    ],
}


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def file_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def all_needles_found(source_id: str) -> bool:
    text = file_text(SOURCE_FILES[source_id])
    return all(needle in text for needle in NEEDLES[source_id])


def ensure_dirs() -> None:
    for directory in [OUT, INPUT_1631, BRANCH_RESIDUALS, QUEUE, RAW, ACCEPTED]:
        directory.mkdir(parents=True, exist_ok=True)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_parses(path: Path) -> bool:
    try:
        read_csv(path)
    except Exception:
        return False
    return True


def bool_str(value: Any) -> str:
    return str(value).strip().lower()


def row_has_true_claim_flag(row: dict[str, Any]) -> bool:
    for field in ["score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed", "accepted_for_scoring", "passes_for_claim"]:
        if field in row and bool_str(row[field]) == "true":
            return True
    return False


def source_register_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "source_id": source_id,
            "source_path": rel(path),
            "exists": path.exists(),
            "required_needles": "; ".join(NEEDLES[source_id]),
            "needles_found": all_needles_found(source_id),
            "role": "1631 first finite input/tau-kernel acquisition provenance",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for source_id, path in SOURCE_FILES.items()
    ]


def intake_scan_rows() -> list[dict[str, Any]]:
    folders = [
        ("SCAN1631_0_raw", RAW, "raw_live_candidate_folder"),
        ("SCAN1631_1_accepted", ACCEPTED, "accepted_live_candidate_folder"),
        ("SCAN1631_2_queue", QUEUE, "nonclaim_acquisition_queue"),
    ]
    rows = []
    for scan_id, folder, role in folders:
        files = sorted(folder.glob("*.csv")) if folder.exists() else []
        if role == "raw_live_candidate_folder" and not files:
            status = "NO_RAW_LIVE_ROWS"
        elif role == "accepted_live_candidate_folder" and not files:
            status = "NO_ACCEPTED_LIVE_ROWS"
        else:
            status = "QUEUE_PRESENT_NONCLAIM" if files else "NO_QUEUE_ROWS"
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "scan_id": scan_id,
                "folder_path": rel(folder),
                "folder_role": role,
                "csv_count": len(files),
                "file_names": ";".join(path.name for path in files[:30]),
                "status": status,
                "accepted_source_backed_rows": 0,
                "score_ready": False,
                "valid_prediction_row": False,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def classify_queue_file(path: Path) -> tuple[str, str, str]:
    name = path.name
    text = file_text(path)
    if name.startswith("R10_alpha_lambda_bound_curve"):
        return (
            "EXTERNAL_R10_BOUND_CURVE_ASSET_NONCLAIM",
            "useful comparison asset after tau_R10 kernel exists; not an MTS coefficient or projection kernel",
            "NO_MTS_JR_QR_TO_ALPHA_KERNEL",
        )
    if name.startswith("ZR1568") or name.startswith("ZR1569"):
        return (
            "EXTERNAL_R10_BOUND_METADATA_NONCLAIM",
            "external bound provenance only; not an MTS source coefficient",
            "NO_MTS_TAU_PROJECTION",
        )
    if name.startswith("JR1630"):
        return (
            "REFUSAL_RUNNER_COPY_NONCLAIM",
            "runner output from 1630; confirms all rows refused",
            "NOT_SOURCE_EVIDENCE",
        )
    if name.startswith("JR1629"):
        return (
            "PRIOR_WIDTH_TEMPLATE_NONCLAIM",
            "finite prior-width rows are all MISSING/source-unbacked",
            "MISSING_NUMERIC_WIDTHS_AND_SOURCE_PATHS",
        )
    if name.startswith("JR1628"):
        return (
            "ACQUISITION_LEDGER_NONCLAIM",
            "names needed J_R/Pi_R/Q_R/tau inputs but supplies no live value",
            "MISSING_SOURCE_BACKED_INPUTS",
        )
    if name.startswith("JR1627"):
        return (
            "FINITE_JR_CONTRACT_NONCLAIM",
            "contract/template only; contains MISSING markers",
            "MISSING_NUMERIC_JR_ROW",
        )
    if name.startswith("ZR"):
        return (
            "ZR_BRANCH_NONCLAIM_CONTEXT",
            "adjacent Z_R branch context, not a J_R/Pi_R/Q_R/tau source row",
            "WRONG_TARGET_FOR_1631",
        )
    if "MISSING" in text or "False" in text:
        return (
            "NONCLAIM_PLACEHOLDER_OR_LEDGER",
            "contains missing markers or nonclaim flags",
            "NOT_ACCEPTABLE_SOURCE_ROW",
        )
    return (
        "UNCLASSIFIED_QUEUE_ROW",
        "requires manual review before any promotion",
        "NOT_ACCEPTED",
    )


def candidate_classification_rows() -> list[dict[str, Any]]:
    rows = []
    for index, path in enumerate(sorted(QUEUE.glob("*.csv")), start=1):
        category, use, blocker = classify_queue_file(path)
        accepted = False
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "candidate_id": f"CAND1631_{index:02d}",
                "file_path": rel(path),
                "category": category,
                "best_use": use,
                "blocker": blocker,
                "accepted_as_source_backed_input": accepted,
                "score_ready": False,
                "valid_prediction_row": False,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def first_row_attempt_rows() -> list[dict[str, Any]]:
    targets = [
        ("FRA1631_0_epsilon_RAB_source", "epsilon_RAB_source", "dimensionless source-only reciprocal scalar", "NO_SOURCE_BACKED_WIDTH_FOUND"),
        ("FRA1631_1_JR", "J_R", "source-current width or zero certificate", "NO_SOURCE_BACKED_JR_FOUND"),
        ("FRA1631_2_PiR", "Pi_R", "boundary reciprocal momentum width or zero certificate", "NO_SOURCE_BACKED_PIR_FOUND"),
        ("FRA1631_3_QR", "Q_R", "reciprocal charge width or zero certificate", "NO_SOURCE_BACKED_QR_FOUND"),
        ("FRA1631_4_tau_R10", "tau_R10[J_R/Pi_R/Q_R]", "kernel from reciprocal source/charge profile to alpha(lambda)", "R10_BOUND_ASSET_PRESENT_KERNEL_MISSING"),
        ("FRA1631_5_tau_PPN", "tau_PPN[J_R/Pi_R/Q_R]", "kernel from reciprocal hair to PPN residual vector", "NO_SOURCE_BACKED_PPN_KERNEL"),
        ("FRA1631_6_tau_clock_orbital", "tau_clock/tau_orbital[J_R/Pi_R/Q_R]", "clock/orbital source-support kernels", "NO_SOURCE_BACKED_CLOCK_ORBITAL_KERNEL"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "attempt_id": attempt_id,
            "target": target,
            "required_evidence": required,
            "attempt_result": result,
            "nearest_available_asset": "R10 reviewed bound curve" if "tau_R10" in target else "none accepted",
            "accepted_as_source_backed_input": False,
            "numeric_value_present": False,
            "source_backed": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for attempt_id, target, required, result in targets
    ]


def r10_asset_rows() -> list[dict[str, Any]]:
    reviewed = SOURCE_FILES["r10_reviewed_curve"]
    rows = read_csv(reviewed) if reviewed.exists() else []
    lambda_values = []
    alpha_values = []
    for row in rows:
        try:
            lambda_values.append(float(row["lambda_m"]))
            alpha_values.append(float(row["alpha_abs_bound"]))
        except Exception:
            continue
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "asset_id": "R10ASSET1631_0_reviewed_curve",
            "asset_path": rel(reviewed),
            "row_count": len(rows),
            "lambda_min_m": min(lambda_values) if lambda_values else "MISSING",
            "lambda_max_m": max(lambda_values) if lambda_values else "MISSING",
            "alpha_min_abs": min(alpha_values) if alpha_values else "MISSING",
            "alpha_max_abs": max(alpha_values) if alpha_values else "MISSING",
            "asset_status": "COMPARISON_BOUND_ASSET_PRESENT_NONCLAIM",
            "why_not_scoreable": "reviewed curve is an external alpha(lambda) bound; MTS tau_R10 kernel and source/charge amplitude are missing",
            "next_use": "derive tau_R10 kernel from J_R/Pi_R/Q_R profile to alpha_R(lambda), then compare later",
            "accepted_as_source_backed_input": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def blocker_rows() -> list[dict[str, Any]]:
    blockers = [
        ("BLK1631_0_live_intake", "raw/accepted live rows", "NO_RAW_OR_ACCEPTED_LIVE_ROWS", "no source-backed rows exist in live intake", "create raw row only after evidence exists"),
        ("BLK1631_1_widths", "epsilon_RAB_source/J_R/Pi_R/Q_R widths", "NO_SOURCE_BACKED_WIDTHS", "only templates, ledgers, and refusal rows exist", "source numeric widths or theorem-zero certificates"),
        ("BLK1631_2_R10_asset", "R10 bound curve", "COMPARISON_ASSET_PRESENT_NOT_MTS_KERNEL", "external reviewed curve exists but not alpha_MTS(lambda)", "derive tau_R10 kernel next"),
        ("BLK1631_3_tau_PPN", "tau_PPN kernel", "MISSING_PPN_KERNEL", "no weak-field map from reciprocal hair to PPN vector", "derive profile-to-PPN response or keep blocker"),
        ("BLK1631_4_tau_clock_orbital", "clock/orbital kernels", "MISSING_CLOCK_ORBITAL_KERNELS", "no clock/orbital source-support projection", "defer until tau_R10/J_R profile route clarified"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "blocker_id": blocker_id,
            "target": target,
            "status": status,
            "missing_for_claim": missing,
            "next_action": next_action,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for blocker_id, target, status, missing, next_action in blockers
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    claims = [
        ("CG1631_0_source_backed_row", "at least one finite input accepted", "BLOCKED", "no raw/accepted source-backed rows found"),
        ("CG1631_1_R10", "R10 alpha(lambda) comparison", "BLOCKED", "bound curve exists but MTS tau_R10 kernel/source amplitude missing"),
        ("CG1631_2_PPN", "PPN/local-GR vector comparison", "BLOCKED", "tau_PPN kernel missing"),
        ("CG1631_3_clock_orbital", "clock/orbital comparison", "BLOCKED", "tau_clock/tau_orbital kernels missing"),
        ("CG1631_4_local_GR", "derived local GR/Newton recovery", "BLOCKED", "finite branch has no accepted input and theorem branch remains blocked"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "claim": claim,
            "status": status,
            "reason": reason,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for gate_id, claim, status, reason in claims
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1631_0_intake",
            "decision": "NO_SOURCE_BACKED_JR_PRIOR_WIDTH_INPUT_FOUND",
            "reason": "raw and accepted intake are empty; queue rows are templates, ledgers, refusal outputs, or external bounds",
            "next_action": "do not score finite branch",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1631_1_r10_asset",
            "decision": "R10_BOUND_ASSET_PRESENT_BUT_TAU_KERNEL_MISSING",
            "reason": "reviewed R10 curve can become comparison data only after MTS profile-to-alpha kernel exists",
            "next_action": "derive tau_R10 from J_R/Pi_R/Q_R profile before more source hunting",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1631_2_next",
            "decision": "NEXT_1632_JR_QR_PROFILE_TO_R10_ALPHA_KERNEL_OR_SOURCE_WIDTH_BLOCKER",
            "reason": "the nearest useful asset is R10; the missing bridge is the MTS alpha(lambda) kernel",
            "next_action": "derive kernel or write blocker before any R10 scoring",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "next_target": "1632-Y5-R2FR-JR-QR-profile-to-R10-alpha-kernel-or-source-width-blocker.md",
            "script": "scripts/Y5_R2FR_JR_QR_profile_to_R10_alpha_kernel_or_source_width_blocker.py",
            "objective": "derive the mapping from a finite J_R/Pi_R/Q_R reciprocal-hair profile to alpha_R(lambda) for R10 comparison; if it cannot be derived, write the exact missing profile/source-width blocker",
            "success_condition": "either a nonclaim tau_R10 kernel contract maps J_R/Q_R/Pi_R to alpha(lambda), or a blocker ledger states the missing profile/range/source-normalization inputs",
            "do_not": "do not score against the R10 bound curve, do not invent J_R/Q_R amplitudes, do not claim local GR/Newton/R10/PPN/clock/orbital pass",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def generated_paths() -> list[Path]:
    return [
        SOURCE_REGISTER,
        INTAKE_SCAN,
        CANDIDATE_CLASSIFICATION,
        FIRST_ROW_ATTEMPT,
        R10_ASSET_LEDGER,
        BLOCKER_LEDGER,
        CLAIM_GATE,
        DECISION,
        NEXT_TARGET,
    ]


def copy_outputs() -> None:
    for source, targets in COPY_TARGETS.items():
        for target in targets:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)
    for source_id, source in SOURCE_FILES.items():
        if source.exists():
            shutil.copyfile(source, INPUT_1631 / f"{source_id}{source.suffix}")


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def validation_rows() -> list[dict[str, Any]]:
    paths = generated_paths()
    scan_rows = read_csv(INTAKE_SCAN)
    candidate_rows = read_csv(CANDIDATE_CLASSIFICATION)
    first_rows = read_csv(FIRST_ROW_ATTEMPT)
    r10_rows = read_csv(R10_ASSET_LEDGER)
    blocker_data = read_csv(BLOCKER_LEDGER)
    claim_rows = read_csv(CLAIM_GATE)
    decision_text = file_text(DECISION)
    next_text = file_text(NEXT_TARGET)
    all_rows: list[dict[str, Any]] = []
    for path in paths:
        all_rows.extend(read_csv(path))

    source_ok = all(path.exists() for path in SOURCE_FILES.values())
    needles_ok = all(all_needles_found(source_id) for source_id in SOURCE_FILES)
    raw_empty = any(row["folder_role"] == "raw_live_candidate_folder" and row["csv_count"] == "0" for row in scan_rows)
    accepted_empty = any(row["folder_role"] == "accepted_live_candidate_folder" and row["csv_count"] == "0" for row in scan_rows)
    no_candidates_accepted = all(row["accepted_as_source_backed_input"] == "False" for row in candidate_rows)
    first_attempts_blocked = all(row["accepted_as_source_backed_input"] == "False" for row in first_rows)
    r10_asset_present = any(row["asset_status"] == "COMPARISON_BOUND_ASSET_PRESENT_NONCLAIM" and row["valid_for_claim"] == "False" for row in r10_rows)
    blocker_cover = {row["target"] for row in blocker_data} == {
        "raw/accepted live rows",
        "epsilon_RAB_source/J_R/Pi_R/Q_R widths",
        "R10 bound curve",
        "tau_PPN kernel",
        "clock/orbital kernels",
    }
    claim_closed = all(row["status"] == "BLOCKED" and not row_has_true_claim_flag(row) for row in claim_rows)
    nonclaim_ok = all(not row_has_true_claim_flag(row) for row in all_rows)
    decision_next = "NEXT_1632_JR_QR_PROFILE_TO_R10_ALPHA_KERNEL_OR_SOURCE_WIDTH_BLOCKER" in decision_text
    next_selected = "1632-Y5-R2FR-JR-QR-profile-to-R10-alpha-kernel-or-source-width-blocker.md" in next_text
    branch_copies = all(target.exists() for targets in COPY_TARGETS.values() for target in targets)
    csv_ok = all(csv_parses(path) for path in paths)
    pycache_absent = not (Path(__file__).resolve().parent / "__pycache__").exists()
    formalization_clean = not any((FORMALIZATION / path.name).exists() for path in [DOC, *paths]) if FORMALIZATION.exists() else True

    checks = [
        ("VAL1631_0_sources_exist", source_ok, "all cited 1631 local source paths exist"),
        ("VAL1631_1_needles_found", needles_ok, "all required 1631 source needles found"),
        ("VAL1631_2_raw_empty", raw_empty, "raw live intake is empty"),
        ("VAL1631_3_accepted_empty", accepted_empty, "accepted live intake is empty"),
        ("VAL1631_4_no_candidates_accepted", no_candidates_accepted, "no queue candidate accepted as source-backed input"),
        ("VAL1631_5_first_attempts_blocked", first_attempts_blocked, "all first source-backed row attempts remain blocked"),
        ("VAL1631_6_r10_asset_present", r10_asset_present, "R10 comparison asset present but nonclaim"),
        ("VAL1631_7_blocker_coverage", blocker_cover, "blocker ledger covers live intake, widths, R10, PPN, clock/orbital"),
        ("VAL1631_8_claim_gates_closed", claim_closed, "all claim gates remain blocked"),
        ("VAL1631_9_nonclaim_flags", nonclaim_ok, "all generated 1631 rows remain nonclaim/non-score-ready"),
        ("VAL1631_10_decision_next", decision_next, "decision selects J_R/Q_R to R10 alpha kernel next"),
        ("VAL1631_11_next_target_selected", next_selected, "next target selected"),
        ("VAL1631_12_branch_copies", branch_copies, "branch/quarantine/acquisition queue nonclaim copies exist"),
        ("VAL1631_13_csv_parse", csv_ok, "all generated 1631 CSVs parse"),
        ("VAL1631_14_pycache_absent", pycache_absent, "scripts __pycache__ absent"),
        ("VAL1631_15_formalization_untouched", formalization_clean, "no 1631 outputs found under formalization-workbench"),
    ]
    overall = all(result for _, result, _ in checks)
    rows = [
        {
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for check_id, result, detail in checks
    ]
    rows.append(
        {
            "check_id": "VAL1631_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1631 J_R prior-width source acquisition or tau-kernel first row validation",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    return rows


def markdown_table(rows: list[dict[str, str]], fields: list[str]) -> str:
    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join("---" for _ in fields) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(field, "")).replace("\n", " ") for field in fields) + " |")
    return "\n".join(lines)


def write_doc() -> None:
    source_rows = read_csv(SOURCE_REGISTER)
    scan_rows = read_csv(INTAKE_SCAN)
    candidate_rows = read_csv(CANDIDATE_CLASSIFICATION)
    first_rows = read_csv(FIRST_ROW_ATTEMPT)
    r10_rows = read_csv(R10_ASSET_LEDGER)
    blockers = read_csv(BLOCKER_LEDGER)
    claims = read_csv(CLAIM_GATE)
    decisions = read_csv(DECISION)
    next_target = read_csv(NEXT_TARGET)
    validation = read_csv(VALIDATION)

    content = f"""# 1631 — `J_R` Prior-Width Source Acquisition Or Tau-Kernel First Row

## Status

Private checkpoint. No source-backed finite `J_R/Pi_R/Q_R` row, tau kernel, R10, PPN, clock, orbital, local-GR/Newton, or public claim is made.

## Outcome

No live finite input was found: raw and accepted intake are empty, while the queue contains templates, ledgers, refusal outputs, and external R10 bound assets. The useful near-term asset is the reviewed R10 alpha(lambda) curve, but it is comparison data only. The missing bridge is now `tau_R10`: a kernel from finite `J_R/Pi_R/Q_R` reciprocal-hair profile to `alpha_R(lambda)`.

## Source Register

{markdown_table(source_rows, ["source_id", "source_path", "exists", "needles_found"])}

## Intake Scan

{markdown_table(scan_rows, ["scan_id", "folder_role", "csv_count", "status"])}

## Candidate Classification

{markdown_table(candidate_rows, ["candidate_id", "file_path", "category", "blocker"])}

## First Source-Backed Row Attempt

{markdown_table(first_rows, ["attempt_id", "target", "attempt_result", "nearest_available_asset"])}

## R10 Bound Asset Ledger

{markdown_table(r10_rows, ["asset_id", "row_count", "lambda_min_m", "lambda_max_m", "asset_status", "why_not_scoreable"])}

## Blocker Ledger

{markdown_table(blockers, ["blocker_id", "target", "status", "next_action"])}

## Claim Gates

{markdown_table(claims, ["gate_id", "claim", "status", "reason"])}

## Decision

{markdown_table(decisions, ["decision_id", "decision", "reason", "next_action"])}

## Next Target

{markdown_table(next_target, ["next_target", "script", "objective", "success_condition"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    outputs = {
        SOURCE_REGISTER: source_register_rows(),
        INTAKE_SCAN: intake_scan_rows(),
        CANDIDATE_CLASSIFICATION: candidate_classification_rows(),
        FIRST_ROW_ATTEMPT: first_row_attempt_rows(),
        R10_ASSET_LEDGER: r10_asset_rows(),
        BLOCKER_LEDGER: blocker_rows(),
        CLAIM_GATE: claim_gate_rows(),
        DECISION: decision_rows(),
        NEXT_TARGET: next_target_rows(),
    }
    for path, rows in outputs.items():
        write_csv(path, rows)

    copy_outputs()
    remove_pycache()
    write_csv(VALIDATION, validation_rows())
    write_doc()
    remove_pycache()
    print(f"wrote {rel(DOC)}")
    print(f"validation {rel(VALIDATION)}")


if __name__ == "__main__":
    main()
