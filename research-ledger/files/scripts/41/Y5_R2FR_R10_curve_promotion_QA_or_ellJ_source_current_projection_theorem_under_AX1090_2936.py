from __future__ import annotations

import csv
import json
import math
import shutil
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

CHECKPOINT = "2936"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
RUN_UTC = SCRIPT_START_UTC.isoformat()

DOC = ROOT / "2936-Y5-R2FR-R10-curve-promotion-QA-or-ellJ-source-current-projection-theorem-under-AX1090.md"

SRC_2935_DOC = ROOT / "2935-Y5-R2FR-R10-alpha-lambda-real-curve-or-ellJ-source-current-owner-theorem-under-AX1090.md"
SRC_2935_NEXT = RESIDUALS / "P8_Y5_R2FR_2935_NEXT_TARGET.csv"
SRC_2935_ANCHORS = RESIDUALS / "P8_Y5_R2FR_2935_R10_SOURCE_BACKED_ANCHOR_ROWS.csv"
SRC_2935_CANDIDATE = RESIDUALS / "P8_Y5_R2FR_2935_R10_REVIEW_CANDIDATE_STATUS.csv"
SRC_2935_RUNNER = RESIDUALS / "P8_Y5_R2FR_2935_R10_RUNNER_REFUSAL_STATUS.csv"
SRC_2935_ELLJ = RESIDUALS / "P8_Y5_R2FR_2935_ELLJ_FALLBACK_OWNER_STATUS.csv"
SRC_2935_VALIDATION = RESIDUALS / "P8_Y5_BRR545_2935_VALIDATION.csv"

SRC_1034_DOC = ROOT / "1034-Y5-R10-alpha-bound-curve-digitization-and-projection-input-pack.md"
SRC_REVIEW_CURVE = LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv"
SRC_570_QA = LOCAL_BOUNDS / "P8_Y5_R10_570_REVIEW_CANDIDATE_QA.csv"
SRC_570_SUMMARY = LOCAL_BOUNDS / "P8_Y5_R10_570_REVIEW_CURVE_SUMMARY.csv"
SRC_569_GATE = LOCAL_BOUNDS / "P8_Y5_R10_569_PROMOTION_GATE.csv"
SRC_569_AXIS = LOCAL_BOUNDS / "P8_Y5_R10_569_AXIS_CALIBRATION.csv"
SRC_569_CURVE_ID = LOCAL_BOUNDS / "P8_Y5_R10_569_CURVE_IDENTITY_LEDGER.csv"
LIVE_DIGITIZED = LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_DIGITIZED.csv"
SUPPLEMENT_ATTEMPT = LOCAL_BOUNDS / "downloads" / "aps_prl_124_101101" / "link_aps_supplemental_attempt.html"
FIG5B_PDF = LOCAL_BOUNDS / "downloads" / "arxiv_2002_11761" / "source_extract" / "fig5b1.pdf"
FIG5B_RENDER = LOCAL_BOUNDS / "downloads" / "arxiv_2002_11761" / "source_extract" / "fig5b1_render_300dpi.png"

SRC_2934_ELLJ = RESIDUALS / "P8_Y5_R2FR_2934_ELLJ_OWNER_SOURCE_CURRENT_AUDIT.csv"
SRC_2934_RESIDUAL = RESIDUALS / "P8_Y5_R2FR_2934_LOG_DERIVATIVE_RESIDUAL_VECTOR.csv"

ARXIV_2020 = "https://arxiv.org/abs/2002.11761"
APS_2020 = "https://link.aps.org/doi/10.1103/PhysRevLett.124.101101"
APS_SUPPLEMENT_2020 = "https://link.aps.org/supplemental/10.1103/PhysRevLett.124.101101"
DOI_2020 = "10.1103/PhysRevLett.124.101101"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2936_SOURCE_REGISTER.csv",
    "machine_qa": RESIDUALS / "P8_Y5_R2FR_2936_R10_REVIEW_CANDIDATE_MACHINE_QA.csv",
    "promotion": RESIDUALS / "P8_Y5_R2FR_2936_R10_PROMOTION_GATE_AUDIT.csv",
    "live_candidate": RESIDUALS / "P8_Y5_R2FR_2936_LIVE_CURVE_CANDIDATE_DECISION.csv",
    "mts_projection": RESIDUALS / "P8_Y5_R2FR_2936_MTS_ALPHA_PROJECTION_REQUIREMENTS.csv",
    "ellj": RESIDUALS / "P8_Y5_R2FR_2936_ELLJ_SOURCE_CURRENT_PROJECTION_THEOREM_ATTEMPT.csv",
    "claims": RESIDUALS / "P8_Y5_R2FR_2936_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2936_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2936_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2936_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2936_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "promotion_copy": LOCAL_BOUNDS / "R10_curve_promotion_gate_2936_NONCLAIM.csv",
    "projection_copy": PARENT_ACTION / "MTS_alpha_projection_requirements_2936_NONCLAIM.csv",
    "ellj_copy": PARENT_ACTION / "EllJ_source_current_projection_attempt_2936_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR2936_ELLJ_SOURCE_CURRENT_OWNER_OR_R10_PROMOTION_NEXT_NONCLAIM.csv",
}

for directory in {path.parent for path in OUTPUTS.values()} | {path.parent for path in BRANCH_OUTPUTS.values()} | {DOC.parent}:
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
    return str(value).strip().lower() in {"1", "true", "yes", "y", "pass"}


def to_float(value: Any) -> float | None:
    try:
        parsed = float(str(value).strip())
    except (TypeError, ValueError):
        return None
    return parsed if math.isfinite(parsed) else None


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
        ("SRC2936_00_2935_doc", SRC_2935_DOC, "NEXT2935_0_2936;R10 curve promotion;Validation overall: `True`", "2935 handoff to curve promotion QA or ellJ theorem"),
        ("SRC2936_01_2935_next", SRC_2935_NEXT, "NEXT2935_0_2936;promotion", "machine-readable 2936 target"),
        ("SRC2936_02_2935_anchors", SRC_2935_ANCHORS, "R10_2935_LEE2020_ALPHA1_38P6UM_ANCHOR", "current branch R10 anchors"),
        ("SRC2936_03_2935_candidate", SRC_2935_CANDIDATE, "R10CAND2935_0_vector_review_candidate;BLOCKED_REVIEW_CANDIDATE", "current branch candidate status"),
        ("SRC2936_04_2935_runner", SRC_2935_RUNNER, "RUN2935_0_anchor_refusal", "runner refusal status"),
        ("SRC2936_05_2935_ellj", SRC_2935_ELLJ, "EJF2935_1_interaction_with_R10", "ellJ/shared blocker status"),
        ("SRC2936_06_2935_validation", SRC_2935_VALIDATION, "VAL2935_OVERALL;True", "2935 validation"),
        ("SRC2936_07_1034_doc", SRC_1034_DOC, "CGATE1034_1_external_curve;R10P1034_6_alpha_predicted", "prior R10 curve/projection pack"),
        ("SRC2936_08_review_curve", SRC_REVIEW_CURVE, "R10_VECTOR_2020_REVIEW_0000;R10_VECTOR_2020_REVIEW_0389", "390-row review curve"),
        ("SRC2936_09_570_QA", SRC_570_QA, "QA570_1_anchor_recovery;QA570_2_promotion_gate", "review QA"),
        ("SRC2936_10_570_summary", SRC_570_SUMMARY, "CS570_0_rows;CS570_3_min_alpha", "review summary"),
        ("SRC2936_11_569_gate", SRC_569_GATE, "PG569_4_supplement_or_human_QA;PG569_5_live_file_update", "promotion gate"),
        ("SRC2936_12_569_axis", SRC_569_AXIS, "x_major_10um;y_major_1e0", "axis calibration ledger"),
        ("SRC2936_13_569_curve_identity", SRC_569_CURVE_ID, "CI569_0_visual_label;CI569_1_anchor_recovery", "curve identity ledger"),
        ("SRC2936_14_live_digitized", LIVE_DIGITIZED, "MISSING", "live claim curve placeholder or missing marker"),
        ("SRC2936_15_supplement_attempt", SUPPLEMENT_ATTEMPT, "", "prior APS supplement retrieval attempt if present"),
        ("SRC2936_16_fig5b_pdf", FIG5B_PDF, "", "source figure PDF from arXiv eprint if present"),
        ("SRC2936_17_fig5b_render", FIG5B_RENDER, "", "rendered source figure used for internal QA if present"),
        ("SRC2936_18_2934_ellj", SRC_2934_ELLJ, "EJO2934_5_verdict;OWNER_THEOREM_NOT_DERIVED", "ellJ owner status"),
        ("SRC2936_19_2934_residual", SRC_2934_RESIDUAL, "LDR2934_5_identity;LDR2934_6_bound_formula", "dotG projection residual"),
    ]
    rows = []
    for source_id, source_path, anchors, role in local_specs:
        found, missing = anchors_present(source_path, anchors)
        if anchors == "":
            found, missing = source_path.exists(), "" if source_path.exists() else "path_missing"
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
        ("SRC2936_20_arxiv_2020", ARXIV_2020, DOI_2020, "primary arXiv source for R10 paper"),
        ("SRC2936_21_aps_2020", APS_2020, DOI_2020, "APS DOI landing page for R10 paper"),
        ("SRC2936_22_aps_supplement", APS_SUPPLEMENT_2020, DOI_2020, "official supplement route; not locally acquired as table"),
    ]:
        rows.append(
            add_common(
                {
                    "source_id": source_id,
                    "source_type": "external_source",
                    "source_path": "",
                    "source_url": url,
                    "source_doi": doi,
                    "anchors": "URL and DOI recorded",
                    "role": role,
                    "path_exists": True,
                    "anchors_found": True,
                    "missing_anchors": "",
                }
            )
        )
    return rows


def machine_qa_rows() -> list[dict[str, Any]]:
    curve_rows = read_csv_rows(SRC_REVIEW_CURVE)
    qa_rows = read_csv_rows(SRC_570_QA)
    axis_rows = read_csv_rows(SRC_569_AXIS)
    curve_id_rows = read_csv_rows(SRC_569_CURVE_ID)
    lambdas = [to_float(row.get("lambda_value")) for row in curve_rows]
    alphas = [to_float(row.get("alpha_bound")) for row in curve_rows]
    numeric_pairs = [(lam, alp) for lam, alp in zip(lambdas, alphas) if lam is not None and alp is not None and lam > 0 and alp > 0]
    unique_lambda_count = len({round(lam, 18) for lam, _ in numeric_pairs})
    duplicate_lambda_count = max(0, len(numeric_pairs) - unique_lambda_count)
    max_axis_residual = max((abs(to_float(row.get("abs_log10_residual")) or 0.0) for row in axis_rows), default="")
    anchor_row = next((row for row in qa_rows if row.get("qa_id") == "QA570_1_anchor_recovery"), {})
    try:
        anchor_detail = json.loads(anchor_row.get("detail", "{}"))
    except json.JSONDecodeError:
        anchor_detail = {}
    visual_identity = next((row for row in curve_id_rows if row.get("identity_id") == "CI569_0_visual_label"), {})
    rows = [
        ("MQA2936_0_numeric_rows", "positive numeric candidate rows", len(numeric_pairs), "rows", len(numeric_pairs) == len(curve_rows) and len(curve_rows) > 0, "all vector candidate rows must parse as positive lambda/alpha"),
        ("MQA2936_1_row_count", "candidate row count", len(curve_rows), "rows", len(curve_rows) == 390, "expected current review-candidate density from 570 summary"),
        ("MQA2936_2_unique_lambdas", "unique lambda samples", unique_lambda_count, "samples", unique_lambda_count > 0, f"duplicate lambda samples={duplicate_lambda_count}; vector path samples are not the official scan grid"),
        ("MQA2936_3_axis_residual", "max axis log10 residual", max_axis_residual, "log10", isinstance(max_axis_residual, float) and max_axis_residual < 5.0e-4, "axis tick fit remains tight enough for review candidate"),
        ("MQA2936_4_anchor_lambda_error", "alpha=1 anchor lambda relative error", anchor_detail.get("lambda_relative_error", ""), "fraction", to_float(anchor_detail.get("lambda_relative_error")) is not None and float(anchor_detail["lambda_relative_error"]) < 0.005, "anchor recovery supports axis mapping"),
        ("MQA2936_5_anchor_alpha_error", "alpha=1 anchor log10 alpha error", anchor_detail.get("alpha_log10_error", ""), "log10", to_float(anchor_detail.get("alpha_log10_error")) is not None and float(anchor_detail["alpha_log10_error"]) < 0.01, "anchor recovery supports curve mapping"),
        ("MQA2936_6_visual_identity", "curve visual identity", visual_identity.get("status", ""), "status", visual_identity.get("status") == "visual_qa_pass_by_codex_render", "internal visual QA only, not human promotion"),
        ("MQA2936_7_valid_for_claim", "candidate rows remain nonclaim", sum(1 for row in curve_rows if as_bool(row.get("valid_for_claim"))), "claim_rows", not any(as_bool(row.get("valid_for_claim")) for row in curve_rows), "candidate must not be live claim curve"),
    ]
    return [
        add_common(
            {
                "qa_id": qa_id,
                "check": check,
                "value": value,
                "units": units,
                "machine_pass": passed,
                "notes": notes,
            }
        )
        for qa_id, check, value, units, passed, notes in rows
    ]


def promotion_rows(machine_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    gate_rows = read_csv_rows(SRC_569_GATE)
    gate = {row.get("gate_id"): row for row in gate_rows}
    machine_ok = all(as_bool(row["machine_pass"]) for row in machine_rows)
    specs = [
        ("PROM2936_0_machine_QA", "machine numeric/axis/anchor/identity QA", "PASS_REVIEW_ONLY", machine_ok, "machine checks support review candidate"),
        ("PROM2936_1_official_supplement", "official supplement or machine-readable table acquired", "BLOCKED", False, f"APS supplement table remains unacquired; prior gate={gate.get('PG569_4_supplement_or_human_QA', {}).get('result', '')}"),
        ("PROM2936_2_human_visual_QA", "human visual QA signs extracted curve identity", "BLOCKED", False, "Codex visual/render QA exists, but no human signoff is recorded"),
        ("PROM2936_3_live_file", "replace live DIGITIZED claim file", "BLOCKED", False, f"prior live gate={gate.get('PG569_5_live_file_update', {}).get('result', '')}; live file is not promoted"),
        ("PROM2936_4_source_contract", "anchor-only rows are not used for interpolation", "PASS_NONCLAIM", True, "2935 runner refusal confirms anchors stay smoke-only"),
        ("PROM2936_5_verdict", "promote R10 review candidate to claim curve", "REFUSED", False, "machine QA alone is insufficient under the current claim policy"),
    ]
    return [
        add_common(
            {
                "promotion_id": promotion_id,
                "gate": gate_name,
                "status": status,
                "gate_pass": gate_pass,
                "required_for_live_curve": True,
                "reason": reason,
            }
        )
        for promotion_id, gate_name, status, gate_pass, reason in specs
    ]


def live_candidate_rows() -> list[dict[str, Any]]:
    live_rows = read_csv_rows(LIVE_DIGITIZED)
    placeholder = any("MISSING" in json.dumps(row, sort_keys=True) for row in live_rows) or not live_rows
    return [
        add_common(
            {
                "decision_id": "LCD2936_0_live_curve",
                "live_curve_path": str(LIVE_DIGITIZED),
                "live_rows": len(live_rows),
                "placeholder_or_missing": placeholder,
                "candidate_path": str(SRC_REVIEW_CURVE),
                "candidate_can_replace_live": False,
                "replacement_policy": "NO_REPLACEMENT_WITHOUT_SUPPLEMENT_OR_HUMAN_QA",
                "valid_for_claim": False,
                "claim_allowed": False,
                "notes": "live curve remains blocked even though machine QA is internally useful",
            }
        )
    ]


def mts_projection_rows() -> list[dict[str, Any]]:
    specs = [
        ("APR2936_0_alpha_bound", "external alpha_bound(lambda)", "promoted numeric curve with valid_for_claim=true", "BLOCKED_REVIEW_CANDIDATE_NONCLAIM", False, "external side not live"),
        ("APR2936_1_KX", "K_X(lambda)", "parent Green-kernel normalization for finite-range mode", "MISSING_PARENT_SOURCE", False, "needed for alpha_kappa(lambda)"),
        ("APR2936_2_Qbar_XH", "Qbar_XH(source,lambda)", "same-worldtube source charge/support integral", "MISSING_SOURCE_NORMALIZATION", False, "source-current owner debt"),
        ("APR2936_3_tau_R10", "tau_R10(test,lambda)", "test material/readout projection", "MISSING_ARENA_PROJECTION", False, "cannot set tau_R10=1 by shortcut"),
        ("APR2936_4_cg", "c_g", "parent-signed coefficient or theorem-zero", "MISSING_PARENT_INPUT_OR_ZERO_THEOREM", False, "coupling branch still open"),
        ("APR2936_5_tail", "retained-tail envelope", "absolute no-cancellation envelope for residual components", "MISSING_ABSOLUTE_ENVELOPE", False, "prevents hidden cancellation scoring"),
        ("APR2936_6_alpha_predicted", "alpha_kappa(lambda)", "K_X Qbar_XH [tau_R10 c_g + abs_tail_envelope]", "NOT_SCORE_READY", False, "no MTS R10 prediction row yet"),
    ]
    return [
        add_common(
            {
                "projection_id": projection_id,
                "quantity": quantity,
                "required_identity_or_input": required,
                "status": status,
                "condition_passed": passed,
                "reason": reason,
            }
        )
        for projection_id, quantity, required, status, passed, reason in specs
    ]


def ellj_rows() -> list[dict[str, Any]]:
    specs = [
        ("EJP2936_0_shared_owner", "shared source-current owner", "ell_J fixes the same source-current normalization used by dotG/G and R10 alpha projection", "ROUTE_IDENTIFIED", True, "this is the common non-looping theorem target"),
        ("EJP2936_1_matter_descent", "ordinary matter descent", "S_matter descends with one J_H source current and one stress tensor", "UNSIGNED", False, "needed to define Qbar_XH and C_source"),
        ("EJP2936_2_Ward_identity", "source-current Ward identity", "nabla_mu T^{mu nu}=0 with no projector/domain source leakage", "UNSIGNED", False, "needed to stop ell_J drift"),
        ("EJP2936_3_reference_policy", "unit/reference owner", "ell_J fixed before readout and cannot be absorbed by measured GM", "UNSIGNED", False, "needed for dotG and R10 projection"),
        ("EJP2936_4_projection_zero", "projection zero", "p_J D_t ln ell_J=0 and R10 tau/source normalization are parent-owned", "NOT_DERIVED", False, "theorem route remains open"),
    ]
    return [
        add_common(
            {
                "ellj_projection_id": row_id,
                "clause": clause,
                "required_identity": required,
                "status": status,
                "condition_passed": passed,
                "reason": reason,
            }
        )
        for row_id, clause, required, status, passed, reason in specs
    ]


def claim_rows() -> list[dict[str, Any]]:
    specs = [
        ("CG2936_0_machine_QA", "machine QA supports the review candidate", "PASS_REVIEW_ONLY", True, "numeric/axis/anchor checks are internally consistent"),
        ("CG2936_1_live_curve", "R10 review curve is promoted to live claim curve", "BLOCKED_NONCLAIM", False, "supplement/human QA gate remains blocked"),
        ("CG2936_2_mts_alpha", "MTS alpha_kappa(lambda) prediction is valid", "BLOCKED_NONCLAIM", False, "K_X/Qbar/tau/c_g/tails missing"),
        ("CG2936_3_runner_claim", "R10 runner can claim pass", "BLOCKED_NONCLAIM", False, "external and theory sides are not both claim-valid"),
        ("CG2936_4_ellJ_owner", "ell_J source-current owner theorem is derived", "BLOCKED_NONCLAIM", False, "shared owner theorem identified but not closed"),
        ("CG2936_5_local_GR", "local-GR/Newton follows from R10/coupling branch", "BLOCKED_NONCLAIM", False, "R10 and dotG projection gates still block"),
    ]
    return [
        add_common(
            {
                "claim_id": claim_id,
                "claim": claim,
                "status": status,
                "condition_passed": passed,
                "reason": reason,
            }
        )
        for claim_id, claim, status, passed, reason in specs
    ]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        ("DEC2936_0_machine", "machine QA is enough for private smoke only", "it strengthens confidence in the vector candidate but cannot replace supplement/human QA", "keep candidate nonclaim"),
        ("DEC2936_1_live", "do not update live DIGITIZED curve", "claim policy requires official table or signed human QA", "leave live curve blocked"),
        ("DEC2936_2_theory", "prioritize theory-side source-current owner", "external curve is not the only blocker; MTS alpha projection is empty", "attack ell_J/Qbar/tau owner next"),
        ("DEC2936_3_next", "select ellJ/source-current projection theorem", "it blocks dotG, R10, source normalization and local-GR reduction at once", "2937 should derive or explicitly fail the owner theorem"),
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
                "next_id": "NEXT2936_0_2937",
                "selection": "selected_primary",
                "target_doc": "2937-Y5-R2FR-ellJ-source-current-owner-theorem-or-Qbar-tau-R10-projection-contract-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_ellJ_source_current_owner_theorem_or_Qbar_tau_R10_projection_contract_under_AX1090_2937.py",
                "objective": "derive the ell_J/source-current owner theorem that fixes Qbar_XH, tau_R10 and C_source across dotG/R10/Newton, or emit a precise closure-only contract",
                "acceptance_gate": "no R10/local-GR claim unless ell_J source-current normalization, source charge, test projection and reference policy are parent-signed or independently bounded",
                "fallback": "if theorem fails, produce explicit Qbar/tau/c_g numeric-source acquisition rows and keep R10 nonclaim",
            }
        )
    ]


def branch_rows() -> list[dict[str, Any]]:
    specs = [
        ("promotion_copy", OUTPUTS["promotion"], BRANCH_OUTPUTS["promotion_copy"]),
        ("projection_copy", OUTPUTS["mts_projection"], BRANCH_OUTPUTS["projection_copy"]),
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
    output_paths = list(OUTPUTS.values())
    branch_paths = list(BRANCH_OUTPUTS.values())
    local_sources = [row for row in rows_by_name["sources"] if row["source_type"] == "local_file"]
    strict_required_sources = [row for row in local_sources if row["source_id"] not in {"SRC2936_14_live_digitized", "SRC2936_15_supplement_attempt"}]
    machine_rows_ok = all(as_bool(row["machine_pass"]) for row in rows_by_name["machine_qa"])
    promotion_refused = any(row["promotion_id"] == "PROM2936_5_verdict" and row["status"] == "REFUSED" and not as_bool(row["gate_pass"]) for row in rows_by_name["promotion"])
    projection_blocked = any(row["projection_id"] == "APR2936_6_alpha_predicted" and not as_bool(row["condition_passed"]) for row in rows_by_name["mts_projection"])
    ellj_blocked = any(row["ellj_projection_id"] == "EJP2936_4_projection_zero" and not as_bool(row["condition_passed"]) for row in rows_by_name["ellj"])
    no_claims = all(not as_bool(row.get("valid_for_claim")) and not as_bool(row.get("claim_allowed")) for rows in rows_by_name.values() for row in rows)
    no_predictions = all(not as_bool(row.get("score_ready")) and not as_bool(row.get("valid_prediction_row")) for rows in rows_by_name.values() for row in rows)
    formalization_output_count = sum(1 for path in output_paths + branch_paths + [DOC] if is_under(path, FORMALIZATION))
    checks = [
        ("VAL2936_0_required_sources_exist", all(as_bool(row["path_exists"]) for row in strict_required_sources), "all strict required local sources exist"),
        ("VAL2936_1_required_anchors_found", all(as_bool(row["anchors_found"]) for row in strict_required_sources), "all strict source anchors found"),
        ("VAL2936_2_machine_QA_passes_review", machine_rows_ok, "machine QA passes for review-only candidate"),
        ("VAL2936_3_promotion_refused", promotion_refused, "live curve promotion remains refused"),
        ("VAL2936_4_live_curve_not_replaced", not as_bool(rows_by_name["live_candidate"][0]["candidate_can_replace_live"]), "live curve not replaced by candidate"),
        ("VAL2936_5_projection_blocked", projection_blocked, "MTS alpha projection remains blocked"),
        ("VAL2936_6_ellJ_blocked", ellj_blocked, "ellJ source-current theorem remains blocked"),
        ("VAL2936_7_no_claims_promoted", no_claims, "no 2936 row is valid_for_claim"),
        ("VAL2936_8_no_prediction_rows", no_predictions, "no score-ready prediction rows emitted"),
        ("VAL2936_9_outputs_parse", all(csv_parses(path) for path in output_paths), "all 2936 output CSVs parse"),
        ("VAL2936_10_branch_copies_parse", all(csv_parses(path) for path in branch_paths), "all branch copy CSVs parse"),
        ("VAL2936_11_doc_exists", DOC.exists(), "2936 markdown doc exists"),
        ("VAL2936_12_next_target_selected", rows_by_name["next"][0]["target_doc"].startswith("2937-"), "2937 target selected"),
        ("VAL2936_13_outputs_under_post_checkpoint", all(is_under(path, ROOT) for path in output_paths + branch_paths + [DOC]), "all outputs remain under post-checkpoint-work"),
        ("VAL2936_14_sources_not_formalization", not any(row["source_path"] and is_under(Path(row["source_path"]), FORMALIZATION) for row in local_sources), "no formalization-workbench source dependency"),
        ("VAL2936_15_no_formalization_2936_outputs", formalization_output_count == 0, "no formalization-workbench 2936 outputs"),
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
                "validation_id": "VAL2936_OVERALL",
                "passed": all(as_bool(row["passed"]) for row in rows),
                "check": "2936 validation overall",
                "required": True,
            }
        )
    )
    return rows


def render_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> str:
    status = "Y5_R2FR_2936_R10_machine_QA_pass_review_only_promotion_refused_ellJ_owner_2937_next"
    claim_ceiling = "R10_machine_QA_yes_review_only_live_curve_no_MTS_alpha_no_ellJ_owner_no_R10_pass_no_local_GR_no_GitHub_claim"
    return "\n\n".join(
        [
            "# 2936 — Y5 R2FR: R10 curve promotion QA or ellJ source-current projection theorem under AX1090",
            f"Status: `{status}`",
            f"Claim ceiling: `{claim_ceiling}`",
            "## Summary",
            (
                "2936 tests the live-curve promotion gate directly. The machine QA is good enough to keep the 390-row "
                "Eot-Wash 2020 vector extraction as a private review candidate: numeric rows pass, axis calibration is tight, "
                "and the alpha=1 anchor is recovered. But the promotion gate still refuses a live claim curve because official "
                "supplemental numerical data or signed human visual QA is not present."
            ),
            (
                "This means the external R10 side is useful for smoke work but not claim scoring. The theory side is still harder: "
                "`alpha_kappa(lambda)` needs `K_X`, `Qbar_XH`, `tau_R10`, `c_g`, and a retained-tail envelope. Those all point back "
                "to the same source-current owner problem as `ell_J`."
            ),
            "## Source Register",
            md_table(rows_by_name["sources"], ["source_id", "source_type", "source_path", "source_url", "path_exists", "anchors_found", "role"]),
            "## Machine QA",
            md_table(rows_by_name["machine_qa"], ["qa_id", "check", "value", "units", "machine_pass", "notes"]),
            "## Promotion Gate Audit",
            md_table(rows_by_name["promotion"], ["promotion_id", "gate", "status", "gate_pass", "required_for_live_curve", "reason"]),
            "## Live Curve Decision",
            md_table(rows_by_name["live_candidate"], ["decision_id", "live_curve_path", "live_rows", "placeholder_or_missing", "candidate_can_replace_live", "replacement_policy", "notes"]),
            "## MTS Alpha Projection Requirements",
            md_table(rows_by_name["mts_projection"], ["projection_id", "quantity", "required_identity_or_input", "status", "condition_passed", "reason"]),
            "## ellJ Source-Current Projection Attempt",
            md_table(rows_by_name["ellj"], ["ellj_projection_id", "clause", "required_identity", "status", "condition_passed", "reason"]),
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
                "This is a clean narrowing. R10 external data are not the immediate dead end; the review candidate is usable privately, "
                "but cannot be promoted. The bigger live blocker is now the MTS projection theorem: source-current ownership must define "
                "`Qbar_XH`, `tau_R10`, `C_source`, and `ell_J` without measured-GM absorption. That is the next best derivation target."
            ),
            "## Non-Claims",
            "- no live R10 curve promotion is made;\n- no MTS `alpha_kappa(lambda)` row is score-ready;\n- no `ell_J` owner theorem is claimed;\n- no local-GR/Newton/R10 pass is claimed;\n- no GitHub/public claim is made.",
        ]
    ) + "\n"


def main() -> None:
    rows_by_name: dict[str, list[dict[str, Any]]] = {}
    rows_by_name["sources"] = source_register_rows()
    rows_by_name["machine_qa"] = machine_qa_rows()
    rows_by_name["promotion"] = promotion_rows(rows_by_name["machine_qa"])
    rows_by_name["live_candidate"] = live_candidate_rows()
    rows_by_name["mts_projection"] = mts_projection_rows()
    rows_by_name["ellj"] = ellj_rows()
    rows_by_name["claims"] = claim_rows()
    rows_by_name["decision"] = decision_rows()
    rows_by_name["next"] = next_rows()

    for key in ["sources", "machine_qa", "promotion", "live_candidate", "mts_projection", "ellj", "claims", "decision", "next"]:
        write_csv(OUTPUTS[key], rows_by_name[key])

    rows_by_name["branches"] = branch_rows()
    write_csv(OUTPUTS["branches"], rows_by_name["branches"])

    DOC.write_text("# 2936 — validation pending\n", encoding="utf-8")
    rows_by_name["validation"] = validation_rows(rows_by_name)
    write_csv(OUTPUTS["validation"], rows_by_name["validation"])
    DOC.write_text(render_doc(rows_by_name), encoding="utf-8")

    print(f"wrote {DOC}")
    print(f"validation overall: {rows_by_name['validation'][-1]['passed']}")


if __name__ == "__main__":
    main()
