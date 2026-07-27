from __future__ import annotations

import csv
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_START_UTC = datetime.now(timezone.utc)

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
PARENT_ACTION = ROOT / "source-intake" / "parent-action"
FORMALIZATION = PROJECT / "formalization-workbench"

CHECKPOINT = "2935"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
RUN_UTC = SCRIPT_START_UTC.isoformat()

DOC = ROOT / "2935-Y5-R2FR-R10-alpha-lambda-real-curve-or-ellJ-source-current-owner-theorem-under-AX1090.md"

SRC_2934_DOC = ROOT / "2934-Y5-R2FR-dotG-to-kappa-projection-theorem-or-ellJ-owner-source-current-normalization-under-AX1090.md"
SRC_2934_NEXT = RESIDUALS / "P8_Y5_R2FR_2934_NEXT_TARGET.csv"
SRC_2934_TRANSFER = RESIDUALS / "P8_Y5_R2FR_2934_DOTG_BOUND_TRANSFER_SCORECARD.csv"
SRC_2934_ELLJ = RESIDUALS / "P8_Y5_R2FR_2934_ELLJ_OWNER_SOURCE_CURRENT_AUDIT.csv"
SRC_2934_VALIDATION = RESIDUALS / "P8_Y5_BRR545_2934_VALIDATION.csv"

SRC_1034_DOC = ROOT / "1034-Y5-R10-alpha-bound-curve-digitization-and-projection-input-pack.md"
SRC_1034_REVIEW_CANDIDATE = LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv"
SRC_570_QA = LOCAL_BOUNDS / "P8_Y5_R10_570_REVIEW_CANDIDATE_QA.csv"
SRC_570_SUMMARY = LOCAL_BOUNDS / "P8_Y5_R10_570_REVIEW_CURVE_SUMMARY.csv"
SRC_569_GATE = LOCAL_BOUNDS / "P8_Y5_R10_569_PROMOTION_GATE.csv"
SRC_904_ANCHORS = LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_904_SOURCE_BACKED_ANCHORS_NONCLAIM.csv"
SRC_2702_CONTRACT = RESIDUALS / "P8_Y5_R2FR_2702_R10_BOUND_CURVE_DIGITIZATION_CONTRACT.csv"
SRC_2767_SMOKE = RESIDUALS / "P8_Y5_R2FR_2767_R10_RUNNER_SMOKE_STATUS.csv"
SRC_RUNNER = ROOT / "scripts" / "R10_alpha_lambda_bound_prediction_runner.py"

ARXIV_2020 = "https://arxiv.org/abs/2002.11761"
DOI_2020 = "10.1103/PhysRevLett.124.101101"
PUBMED_2020 = "https://pubmed.ncbi.nlm.nih.gov/32216404/"
ARXIV_2007 = "https://arxiv.org/abs/hep-ph/0611184"
DOI_2007 = "10.1103/PhysRevLett.98.021101"

ANCHOR_FILE = LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_2935_SOURCE_BACKED_ANCHORS_NONCLAIM.csv"
MTS_SMOKE_FILE = RESIDUALS / "R10_alpha_lambda_curve_MTS_2935_PROJECTION_BLOCKED_NONCLAIM.csv"
RUNNER_DIR = RESIDUALS / "R10_runner_2935_anchor_refusal"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2935_SOURCE_REGISTER.csv",
    "anchors": RESIDUALS / "P8_Y5_R2FR_2935_R10_SOURCE_BACKED_ANCHOR_ROWS.csv",
    "candidate": RESIDUALS / "P8_Y5_R2FR_2935_R10_REVIEW_CANDIDATE_STATUS.csv",
    "mts_smoke": RESIDUALS / "P8_Y5_R2FR_2935_MTS_R10_PROJECTION_BLOCKED_ROWS.csv",
    "runner": RESIDUALS / "P8_Y5_R2FR_2935_R10_RUNNER_REFUSAL_STATUS.csv",
    "ellj": RESIDUALS / "P8_Y5_R2FR_2935_ELLJ_FALLBACK_OWNER_STATUS.csv",
    "claims": RESIDUALS / "P8_Y5_R2FR_2935_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2935_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2935_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2935_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2935_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "anchors_copy": LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_2935_SOURCE_BACKED_ANCHORS_NONCLAIM_COPY.csv",
    "candidate_status_copy": LOCAL_BOUNDS / "R10_review_candidate_status_2935_NONCLAIM.csv",
    "ellj_copy": PARENT_ACTION / "EllJ_source_current_owner_fallback_2935_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR2935_R10_PROMOTION_GATE_OR_ELLJ_OWNER_NEXT_NONCLAIM.csv",
}

for directory in {path.parent for path in OUTPUTS.values()} | {path.parent for path in BRANCH_OUTPUTS.values()} | {ANCHOR_FILE.parent, MTS_SMOKE_FILE.parent, RUNNER_DIR, DOC.parent}:
    directory.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_parses(path: Path) -> bool:
    try:
        read_csv_rows(path)
        return True
    except Exception:
        return False


def anchors_present(path: Path, anchors: str) -> tuple[bool, str]:
    if not path.exists():
        return False, anchors
    text = read_text(path)
    missing = [anchor for anchor in anchors.split(";") if anchor and anchor not in text]
    return not missing, ";".join(missing)


def add_common(row: dict[str, Any]) -> dict[str, Any]:
    row.update(
        {
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "control_only": True,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": RUN_UTC,
        }
    )
    return row


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def as_bool(value: Any) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def is_under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def md_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def md_table(rows: list[dict[str, Any]], columns: list[str] | None = None) -> str:
    if not rows:
        return "_No rows._"
    selected = columns or list(rows[0].keys())
    header = "| " + " | ".join(selected) + " |"
    separator = "| " + " | ".join("---" for _ in selected) + " |"
    body = ["| " + " | ".join(md_escape(row.get(column, "")) for column in selected) + " |" for row in rows]
    return "\n".join([header, separator, *body])


def source_register_rows() -> list[dict[str, Any]]:
    local_specs = [
        ("SRC2935_00_2934_doc", SRC_2934_DOC, "NEXT2934_0_2935;R10 alpha(lambda);Validation overall: `True`", "2934 selected R10 alpha curve or ellJ owner"),
        ("SRC2935_01_2934_next", SRC_2934_NEXT, "NEXT2934_0_2935;alpha(lambda)", "machine-readable 2935 target"),
        ("SRC2935_02_2934_transfer", SRC_2934_TRANSFER, "DTS2934_3_decision;R10 alpha(lambda)", "dotG transfer pushed branch to R10 or ellJ"),
        ("SRC2935_03_2934_ellj", SRC_2934_ELLJ, "EJO2934_5_verdict;OWNER_THEOREM_NOT_DERIVED", "ellJ fallback still open"),
        ("SRC2935_04_2934_validation", SRC_2934_VALIDATION, "VAL2934_OVERALL;True", "2934 validation"),
        ("SRC2935_05_1034_doc", SRC_1034_DOC, "R10B1034_0_2020_alpha1_38p6um_anchor;CS1034_0_candidate_file;CGATE1034_1_external_curve", "prior bound-curve digitization pack"),
        ("SRC2935_06_1034_candidate", SRC_1034_REVIEW_CANDIDATE, "R10_VECTOR_2020_REVIEW_0000;R10_VECTOR_2020_REVIEW_0389", "390-row vector review candidate"),
        ("SRC2935_07_570_QA", SRC_570_QA, "QA570_1_anchor_recovery;pass_review_candidate", "review candidate QA and anchor recovery"),
        ("SRC2935_08_570_summary", SRC_570_SUMMARY, "CS570_0_rows;CS570_3_min_alpha", "review candidate summary"),
        ("SRC2935_09_569_gate", SRC_569_GATE, "PG569_4_supplement_or_human_QA;blocked", "promotion gate blocking live claim curve"),
        ("SRC2935_10_904_anchors", SRC_904_ANCHORS, "R10_904_LEE2020_ALPHA1_38P6UM_ANCHOR;R10_904_KAPNER2007_ALPHA1_56UM_ANCHOR", "source-backed anchors"),
        ("SRC2935_11_2702_contract", SRC_2702_CONTRACT, "BDC2702_0_target_file;BDC2702_4_interpolation_rule;BDC2702_5_claim_policy", "bound curve contract"),
        ("SRC2935_12_2767_runner_smoke", SRC_2767_SMOKE, "SMOKE2767_0_R10_runner_refusal", "prior runner refusal"),
        ("SRC2935_13_runner_script", SRC_RUNNER, "BOUND_REQUIRED_COLUMNS;valid_for_claim_not_true;R10_pass_for_claim", "R10 runner validation logic"),
    ]
    rows = []
    for source_id, source_path, anchors, role in local_specs:
        found, missing = anchors_present(source_path, anchors)
        rows.append(
            add_common(
                {
                    "source_id": source_id,
                    "source_type": "local_file",
                    "source_path": str(source_path),
                    "source_url": "",
                    "source_doi": "",
                    "anchors": anchors,
                    "role": role,
                    "path_exists": source_path.exists(),
                    "anchors_found": found,
                    "missing_anchors": missing,
                }
            )
        )
    for source_id, url, doi, role in [
        ("SRC2935_14_arxiv_2020", ARXIV_2020, DOI_2020, "modern Eot-Wash 2020 R10 source"),
        ("SRC2935_15_pubmed_2020", PUBMED_2020, DOI_2020, "PubMed DOI/source mirror for 2020 anchor"),
        ("SRC2935_16_arxiv_2007", ARXIV_2007, DOI_2007, "older Eot-Wash continuity anchor"),
    ]:
        rows.append(
            add_common(
                {
                    "source_id": source_id,
                    "source_type": "external_primary_source",
                    "source_path": "",
                    "source_url": url,
                    "source_doi": doi,
                    "anchors": "source URL and DOI recorded; numeric anchor already present in local source-backed anchor file",
                    "role": role,
                    "path_exists": True,
                    "anchors_found": True,
                    "missing_anchors": "",
                }
            )
        )
    return rows


def anchor_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "bound_id": "R10_2935_LEE2020_ALPHA1_38P6UM_ANCHOR",
            "dataset_id": "Lee_Adelberger_Cook_Fleischer_Heckel_PRL124_101101_2020",
            "curve_id": "R10_anchor_only_EotWash_2020",
            "lambda_value": 38.6,
            "lambda_units": "um",
            "lambda_m": 38.6e-6,
            "alpha_bound": 1.0,
            "alpha_bound_units": "dimensionless",
            "alpha_bound_source": f"{ARXIV_2020}; {PUBMED_2020}; doi:{DOI_2020}",
            "digitization_method": "source_text_threshold_anchor_only_non_curve",
            "source_file": ARXIV_2020,
            "row_type": "anchor_only_non_curve",
            "confidence": "high_for_threshold_anchor_not_curve",
            "claim_use": "schema_and_smoke_only_no_interpolation",
            "notes": "alpha=1 threshold anchor; not a full alpha(lambda) curve row",
        },
        {
            "bound_id": "R10_2935_KAPNER2007_ALPHA1_56UM_ANCHOR",
            "dataset_id": "Kapner_Cook_Adelberger_Gundlach_Heckel_Hoyle_Swanson_PRL98_021101_2007",
            "curve_id": "R10_anchor_only_EotWash_2007",
            "lambda_value": 56.0,
            "lambda_units": "um",
            "lambda_m": 56.0e-6,
            "alpha_bound": 1.0,
            "alpha_bound_units": "dimensionless",
            "alpha_bound_source": f"{ARXIV_2007}; doi:{DOI_2007}",
            "digitization_method": "source_text_threshold_anchor_only_non_curve",
            "source_file": ARXIV_2007,
            "row_type": "anchor_only_non_curve",
            "confidence": "high_for_threshold_anchor_not_curve",
            "claim_use": "continuity_anchor_only_no_modern_score",
            "notes": "older alpha=1 continuity anchor; not a full modern curve row",
        },
    ]
    out = [add_common(row) for row in rows]
    write_csv(ANCHOR_FILE, out)
    write_csv(OUTPUTS["anchors"], out)
    return out


def candidate_status_rows() -> list[dict[str, Any]]:
    candidate_rows = read_csv_rows(SRC_1034_REVIEW_CANDIDATE)
    qa_rows = read_csv_rows(SRC_570_QA)
    summary_rows = read_csv_rows(SRC_570_SUMMARY)
    gate_rows = read_csv_rows(SRC_569_GATE)
    anchor_qa = next((row for row in qa_rows if row.get("qa_id") == "QA570_1_anchor_recovery"), {})
    supplement_gate = next((row for row in gate_rows if row.get("gate_id") == "PG569_4_supplement_or_human_QA"), {})
    live_gate = next((row for row in gate_rows if row.get("gate_id") == "PG569_5_live_file_update"), {})
    rows = [
        {
            "candidate_id": "R10CAND2935_0_vector_review_candidate",
            "candidate_file": str(SRC_1034_REVIEW_CANDIDATE),
            "candidate_rows": len(candidate_rows),
            "lambda_range_m": f"{summary_rows[1].get('value', '')}" if len(summary_rows) > 1 else "",
            "alpha_range": f"{summary_rows[2].get('value', '')}" if len(summary_rows) > 2 else "",
            "tightest_candidate": f"{summary_rows[3].get('value', '')}" if len(summary_rows) > 3 else "",
            "anchor_recovery": anchor_qa.get("result", ""),
            "supplement_or_human_QA_gate": supplement_gate.get("result", ""),
            "live_file_update_gate": live_gate.get("result", ""),
            "promotion_status": "BLOCKED_REVIEW_CANDIDATE_NOT_LIVE_CLAIM_CURVE",
            "valid_for_claim": False,
            "notes": "review candidate is useful for private plots/smoke only; official table or human visual QA still required",
        }
    ]
    return [add_common(row) for row in rows]


def mts_smoke_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "model_id": "MTS_R2FR_2935_projection_blocked_branch",
            "branch_id": BRANCH_ID,
            "curve_id": "MTS_alpha_kappa_lambda_projection_blocked_2935",
            "lambda_value": 38.6,
            "lambda_units": "um",
            "alpha_predicted": "MISSING_PARENT_ALPHA_KAPPA_PROJECTION",
            "alpha_bound": 1.0,
            "alpha_bound_source": str(ANCHOR_FILE),
            "force_law_form": "Yukawa_potential",
            "derivation_status": "BLOCKED_PENDING_K_X_QBAR_SOURCE_TEST_CHARGE_AND_ELLJ_OWNER",
            "formula_reference": "R10_alpha_lambda_executable_curve_contract;2934 projection residual identity",
            "source_file": str(DOC),
            "assumptions": "anchor-only noncurve row; no interpolation; no claim",
            "valid_for_claim": False,
            "notes": "deliberately invalid for runner claim until MTS alpha(lambda) prediction exists",
        }
    ]
    out = [add_common(row) for row in rows]
    write_csv(MTS_SMOKE_FILE, out)
    write_csv(OUTPUTS["mts_smoke"], out)
    return out


def runner_rows() -> list[dict[str, Any]]:
    if RUNNER_DIR.exists():
        for child in RUNNER_DIR.iterdir():
            if child.is_file():
                child.unlink()
    completed = subprocess.run(
        [
            sys.executable,
            str(SRC_RUNNER),
            "--mts-curve",
            str(MTS_SMOKE_FILE),
            "--bound-curve",
            str(ANCHOR_FILE),
            "--output-dir",
            str(RUNNER_DIR),
        ],
        cwd=str(ROOT),
        text=True,
        capture_output=True,
        check=False,
    )
    status_path = RUNNER_DIR / "R10_runner_status.json"
    status = json.loads(status_path.read_text(encoding="utf-8")) if status_path.exists() else {}
    rows = [
        {
            "runner_id": "RUN2935_0_anchor_refusal",
            "command_returncode": completed.returncode,
            "output_dir": str(RUNNER_DIR),
            "mts_rows": status.get("mts_rows", ""),
            "bound_rows": status.get("bound_rows", ""),
            "valid_mts_rows": status.get("valid_mts_rows", ""),
            "valid_bound_rows": status.get("valid_bound_rows", ""),
            "comparison_rows": status.get("comparison_rows", ""),
            "R10_pass_for_claim": status.get("R10_pass_for_claim", ""),
            "claim_allowed": status.get("claim_allowed", ""),
            "expected_refusal": True,
            "stdout": completed.stdout.strip(),
            "stderr": completed.stderr.strip(),
            "verdict": "RUNNER_REFUSED_NONCLAIM_ANCHORS_AND_MTS_PLACEHOLDER_AS_EXPECTED",
        }
    ]
    return [add_common(row) for row in rows]


def ellj_rows() -> list[dict[str, Any]]:
    specs = [
        ("EJF2935_0_owner_status", "ell_J owner theorem", "p_J D_t ln ell_J=0 from parent source-current normalization", "STILL_OPEN_FROM_2934", False, "R10 route selected first; no owner theorem promoted"),
        ("EJF2935_1_interaction_with_R10", "R10 source-test normalization", "same source-current owner must fix R10 test/source charge normalization", "ACTIVE_SHARED_BLOCKER", False, "ell_J and R10 alpha projection are not separate debts"),
        ("EJF2935_2_fallback", "fallback theorem route", "derive source-current matter descent and Ward identity before local-GR claim", "2936_FALLBACK_IF_R10_PROMOTION_BLOCKS", False, "keep theorem route alive"),
    ]
    return [
        add_common(
            {
                "ellj_fallback_id": row_id,
                "clause": clause,
                "required_identity": required_identity,
                "status": status,
                "condition_passed": condition_passed,
                "reason": reason,
            }
        )
        for row_id, clause, required_identity, status, condition_passed, reason in specs
    ]


def claim_rows() -> list[dict[str, Any]]:
    specs = [
        ("CG2935_0_anchor_rows", "source-backed R10 alpha=1 anchors exist", "PASS_NONCLAIM", "2020 and 2007 anchor rows are numeric and sourced", True),
        ("CG2935_1_review_candidate", "390-row 2020 vector review candidate exists", "PASS_REVIEW_CANDIDATE_NONCLAIM", "anchor recovery QA passed, but promotion gate remains blocked", True),
        ("CG2935_2_live_curve", "live R10 alpha(lambda) claim curve is promoted", "BLOCKED_NONCLAIM", "official supplement or human visual QA has not signed the vector candidate", False),
        ("CG2935_3_mts_prediction", "MTS alpha_kappa(lambda) prediction row is valid", "BLOCKED_NONCLAIM", "parent K_X/Qbar/source-test charge/ellJ projection still missing", False),
        ("CG2935_4_runner_pass", "R10 runner can produce a claim pass", "BLOCKED_NONCLAIM", "runner correctly refuses nonclaim anchors and placeholder MTS row", False),
        ("CG2935_5_local_GR", "R10 supports local-GR/Newton recovery claim", "BLOCKED_NONCLAIM", "external curve and MTS projection gates not both closed", False),
    ]
    return [
        add_common(
            {
                "claim_id": claim_id,
                "claim": claim,
                "status": status,
                "condition_passed": condition_passed,
                "reason": reason,
            }
        )
        for claim_id, claim, status, reason, condition_passed in specs
    ]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        ("DEC2935_0_anchor", "retain source-backed anchor rows", "they are real, useful, and safe for smoke plumbing", "copy to local_bounds with valid_for_claim=false"),
        ("DEC2935_1_candidate", "do not promote 390-row vector candidate", "QA is promising but supplement/human-visual signoff gate remains blocked", "keep review_candidate_nonclaim"),
        ("DEC2935_2_runner", "keep runner refusal as success", "a valid framework must refuse placeholder MTS predictions and anchor-only noncurves", "do not score R10 yet"),
        ("DEC2935_3_next", "attack promotion gate or ellJ owner", "either source the official curve/QA, or close the shared source-current owner theorem", "2936 should target R10 promotion QA plus source-current projection"),
    ]
    return [
        add_common(
            {
                "decision_id": decision_id,
                "decision": decision,
                "reason": reason,
                "action": action,
            }
        )
        for decision_id, decision, reason, action in specs
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "next_id": "NEXT2935_0_2936",
                "selection": "selected_primary",
                "target_doc": "2936-Y5-R2FR-R10-curve-promotion-QA-or-ellJ-source-current-projection-theorem-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_R10_curve_promotion_QA_or_ellJ_source_current_projection_theorem_under_AX1090_2936.py",
                "objective": "either close the R10 curve promotion gate by supplement/human QA, or derive the ell_J/source-current projection theorem needed for MTS alpha_kappa(lambda)",
                "acceptance_gate": "no R10 claim unless a promoted curve and a valid MTS prediction row both pass runner validation; otherwise retain nonclaim status",
                "fallback": "if curve promotion cannot close, prioritize ell_J/source-current owner theorem because it blocks both dotG and R10",
            }
        )
    ]


def branch_rows() -> list[dict[str, Any]]:
    specs = [
        ("anchors_copy", ANCHOR_FILE, BRANCH_OUTPUTS["anchors_copy"]),
        ("candidate_status_copy", OUTPUTS["candidate"], BRANCH_OUTPUTS["candidate_status_copy"]),
        ("ellj_copy", OUTPUTS["ellj"], BRANCH_OUTPUTS["ellj_copy"]),
        ("next_copy", OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"]),
    ]
    rows = []
    for copy_id, source_path, destination_path in specs:
        shutil.copyfile(source_path, destination_path)
        rows.append(
            add_common(
                {
                    "copy_id": copy_id,
                    "source_path": str(source_path),
                    "destination_path": str(destination_path),
                    "source_exists": source_path.exists(),
                    "destination_exists": destination_path.exists(),
                    "destination_parses": csv_parses(destination_path),
                }
            )
        )
    return rows


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    output_paths = list(OUTPUTS.values()) + [ANCHOR_FILE, MTS_SMOKE_FILE]
    branch_paths = list(BRANCH_OUTPUTS.values())
    local_sources = [row for row in rows_by_name["sources"] if row["source_type"] == "local_file"]
    external_sources = [row for row in rows_by_name["sources"] if row["source_type"] == "external_primary_source"]
    anchor_rows_valid = all(float(row["lambda_m"]) > 0 and float(row["alpha_bound"]) > 0 and row["row_type"] == "anchor_only_non_curve" for row in rows_by_name["anchors"])
    runner = rows_by_name["runner"][0]
    no_claims = all(not as_bool(row.get("valid_for_claim")) and not as_bool(row.get("claim_allowed")) for rows in rows_by_name.values() for row in rows)
    no_predictions = all(not as_bool(row.get("score_ready")) and not as_bool(row.get("valid_prediction_row")) for rows in rows_by_name.values() for row in rows)
    formalization_output_count = sum(1 for path in output_paths + branch_paths + [DOC] if is_under(path, FORMALIZATION))
    checks = [
        ("VAL2935_0_local_sources_exist", all(as_bool(row["path_exists"]) for row in local_sources), "all local sources exist"),
        ("VAL2935_1_local_anchors_found", all(as_bool(row["anchors_found"]) for row in local_sources), "all local source anchors found"),
        ("VAL2935_2_external_sources_recorded", len(external_sources) == 3 and all(row["source_url"] and row["source_doi"] for row in external_sources), "external URLs and DOIs recorded"),
        ("VAL2935_3_anchor_rows_positive_numeric", anchor_rows_valid, "anchor rows have positive numeric lambda/alpha values"),
        ("VAL2935_4_anchor_rows_nonclaim", all(not as_bool(row["valid_for_claim"]) for row in rows_by_name["anchors"]), "anchor rows remain valid_for_claim=false"),
        ("VAL2935_5_review_candidate_blocked", rows_by_name["candidate"][0]["promotion_status"] == "BLOCKED_REVIEW_CANDIDATE_NOT_LIVE_CLAIM_CURVE", "review candidate not promoted"),
        ("VAL2935_6_runner_refuses_claim", runner["command_returncode"] == 0 and not as_bool(runner["R10_pass_for_claim"]) and not as_bool(runner["claim_allowed"]), "runner refuses nonclaim anchor/MTS rows"),
        ("VAL2935_7_no_claims_promoted", no_claims, "no 2935 row is valid_for_claim"),
        ("VAL2935_8_no_prediction_rows", no_predictions, "no score-ready prediction rows emitted"),
        ("VAL2935_9_outputs_parse", all(csv_parses(path) for path in output_paths), "all 2935 output CSVs parse"),
        ("VAL2935_10_runner_outputs_parse", all(csv_parses(RUNNER_DIR / name) for name in ["R10_runner_mts_validation.csv", "R10_runner_bound_validation.csv", "R10_runner_comparison.csv"]), "runner CSV outputs parse"),
        ("VAL2935_11_branch_copies_parse", all(csv_parses(path) for path in branch_paths), "all branch copy CSVs parse"),
        ("VAL2935_12_doc_exists", DOC.exists(), "2935 markdown doc exists"),
        ("VAL2935_13_next_target_selected", rows_by_name["next"][0]["target_doc"].startswith("2936-"), "2936 target selected"),
        ("VAL2935_14_outputs_under_post_checkpoint", all(is_under(path, ROOT) for path in output_paths + branch_paths + [DOC]), "all outputs remain under post-checkpoint-work"),
        ("VAL2935_15_sources_not_formalization", not any(row["source_path"] and is_under(Path(row["source_path"]), FORMALIZATION) for row in local_sources), "no formalization-workbench source dependency"),
        ("VAL2935_16_no_formalization_2935_outputs", formalization_output_count == 0, "no formalization-workbench 2935 outputs"),
    ]
    rows = [
        add_common(
            {
                "validation_id": validation_id,
                "passed": passed,
                "check": check,
                "required": True,
            }
        )
        for validation_id, passed, check in checks
    ]
    rows.append(
        add_common(
            {
                "validation_id": "VAL2935_OVERALL",
                "passed": all(as_bool(row["passed"]) for row in rows),
                "check": "2935 validation overall",
                "required": True,
            }
        )
    )
    return rows


def render_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> str:
    status = "Y5_R2FR_2935_R10_anchors_and_review_candidate_locked_nonclaim_runner_refusal_pass_2936_next"
    claim_ceiling = "R10_source_anchors_yes_review_candidate_yes_live_curve_no_MTS_prediction_no_R10_pass_no_local_GR_no_GitHub_claim"
    return "\n\n".join(
        [
            "# 2935 — Y5 R2FR: R10 alpha(lambda) real curve or ellJ source-current owner theorem under AX1090",
            f"Status: `{status}`",
            f"Claim ceiling: `{claim_ceiling}`",
            "## Summary",
            (
                "2935 locks the R10 external side into the current coupling branch. The safe result is: "
                "source-backed `alpha=1` anchors exist, and a 390-row 2020 vector review candidate exists, "
                "but neither is promoted to a live claim curve. The runner correctly refuses the anchor-only/nonclaim "
                "bound rows and the placeholder MTS prediction row."
            ),
            (
                "This matters because the R10 route is independent pressure on the same source/coupling problem. "
                "It can test finite-range `alpha_kappa(lambda)` only after two things close together: "
                "a promoted external `alpha_bound(lambda)` curve and a parent-derived MTS `alpha_kappa(lambda)` projection."
            ),
            "## Source Register",
            md_table(rows_by_name["sources"], ["source_id", "source_type", "source_path", "source_url", "source_doi", "path_exists", "anchors_found", "role"]),
            "## Source-Backed Anchor Rows",
            md_table(rows_by_name["anchors"], ["bound_id", "dataset_id", "lambda_value", "lambda_units", "alpha_bound", "row_type", "confidence", "claim_use", "valid_for_claim"]),
            "## Review Candidate Status",
            md_table(rows_by_name["candidate"], ["candidate_id", "candidate_file", "candidate_rows", "lambda_range_m", "alpha_range", "anchor_recovery", "supplement_or_human_QA_gate", "live_file_update_gate", "promotion_status", "valid_for_claim"]),
            "## MTS Projection-Blocked Smoke Rows",
            md_table(rows_by_name["mts_smoke"], ["model_id", "curve_id", "lambda_value", "lambda_units", "alpha_predicted", "derivation_status", "valid_for_claim", "notes"]),
            "## Runner Refusal Status",
            md_table(rows_by_name["runner"], ["runner_id", "command_returncode", "mts_rows", "bound_rows", "valid_mts_rows", "valid_bound_rows", "comparison_rows", "R10_pass_for_claim", "claim_allowed", "verdict"]),
            "## ellJ Fallback Owner Status",
            md_table(rows_by_name["ellj"], ["ellj_fallback_id", "clause", "required_identity", "status", "condition_passed", "reason"]),
            "## Claim Gates",
            md_table(rows_by_name["claims"], ["claim_id", "claim", "status", "condition_passed", "reason"]),
            "## Decisions",
            md_table(rows_by_name["decision"], ["decision_id", "decision", "reason", "action"]),
            "## Next Target",
            md_table(rows_by_name["next"], ["next_id", "selection", "target_doc", "target_script", "objective", "acceptance_gate", "fallback"]),
            "## Branch Copies",
            md_table(rows_by_name["branches"], ["copy_id", "source_path", "destination_path", "source_exists", "destination_exists", "destination_parses"]),
            "## Validation",
            md_table(rows_by_name["validation"], ["validation_id", "passed", "check", "required"]),
            f"Validation overall: `{rows_by_name['validation'][-1]['passed']}`.",
            "## Bottom Line",
            (
                "This is good plumbing, not an R10 win. The external R10 side is now much less vague: anchors are real, "
                "and the private review curve is promising enough for internal smoke work. But the framework is doing the right thing by refusing a claim until "
                "the curve is promoted and the MTS `alpha_kappa(lambda)` row is derived. The shared hard target remains source-current/coupling ownership."
            ),
            "## Non-Claims",
            "- no live R10 `alpha_bound(lambda)` claim curve is promoted;\n- no MTS `alpha_kappa(lambda)` prediction is claimed;\n- no R10/local-GR/Newton pass is claimed;\n- no GitHub/public claim is made.",
        ]
    ) + "\n"


def main() -> None:
    rows_by_name: dict[str, list[dict[str, Any]]] = {}
    rows_by_name["sources"] = source_register_rows()
    rows_by_name["anchors"] = anchor_rows()
    rows_by_name["candidate"] = candidate_status_rows()
    rows_by_name["mts_smoke"] = mts_smoke_rows()
    rows_by_name["runner"] = runner_rows()
    rows_by_name["ellj"] = ellj_rows()
    rows_by_name["claims"] = claim_rows()
    rows_by_name["decision"] = decision_rows()
    rows_by_name["next"] = next_rows()

    for key in ["sources", "candidate", "runner", "ellj", "claims", "decision", "next"]:
        write_csv(OUTPUTS[key], rows_by_name[key])

    rows_by_name["branches"] = branch_rows()
    write_csv(OUTPUTS["branches"], rows_by_name["branches"])

    DOC.write_text("# 2935 — validation pending\n", encoding="utf-8")
    rows_by_name["validation"] = validation_rows(rows_by_name)
    write_csv(OUTPUTS["validation"], rows_by_name["validation"])
    DOC.write_text(render_doc(rows_by_name), encoding="utf-8")

    print(f"wrote {DOC}")
    print(f"validation overall: {rows_by_name['validation'][-1]['passed']}")


if __name__ == "__main__":
    main()
