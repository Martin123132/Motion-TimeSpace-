from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
R10 = ROOT / "source-intake" / "r10"
RAW = R10 / "raw" / "1509"
CANDIDATES = R10 / "candidates"
MICROSCOPE = ROOT / "source-intake" / "microscope"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1509-Y5-R10-RAB-acquire-reviewed-R10-bound-curve-and-tau-kernel-or-freeze-local-R10.md"
START_TS = datetime.now(timezone.utc).timestamp()

SOURCE_2020_TAR = RAW / "arxiv_2002_11761_source.tar"
SOURCE_2020_TEX = RAW / "arxiv_2002_11761_source" / "FB_ISL_pdf.tex"
SOURCE_2007_TAR = RAW / "arxiv_hep-ph_0611184_source.tar"
SOURCE_2007_TEX = RAW / "arxiv_hep-ph_0611184_source" / "kapner6.tex"
SOURCE_2003_TAR = RAW / "arxiv_hep-ph_0307284_source.tar"
SOURCE_2003_TEX = RAW / "arxiv_hep-ph_0307284_source" / "gravityreview.tex"

SOURCE_FILES = {
    "1508_validation": OUT / "P8_Y5_BRR545_1508_VALIDATION.csv",
    "1508_next": OUT / "P8_Y5_R10_1508_NEXT_TARGET.csv",
    "1508_alpha_pack": OUT / "P8_Y5_R10_1508_ALPHA_PRIOR_SOURCE_PACK.csv",
    "1508_certificate_trial": OUT / "P8_Y5_R10_1508_LX_CERTIFICATE_TRIAL.csv",
    "1508_source_ledger": OUT / "P8_Y5_R10_1508_SOURCE_ACQUISITION_LEDGER.csv",
    "source_2020_tar": SOURCE_2020_TAR,
    "source_2020_tex": SOURCE_2020_TEX,
    "source_2007_tar": SOURCE_2007_TAR,
    "source_2007_tex": SOURCE_2007_TEX,
    "source_2003_tar": SOURCE_2003_TAR,
    "source_2003_tex": SOURCE_2003_TEX,
}

EXTERNAL_SOURCES = {
    "lee_2020_arxiv": "https://arxiv.org/abs/2002.11761",
    "lee_2020_prl": "https://doi.org/10.1103/PhysRevLett.124.101101",
    "kapner_2007_arxiv": "https://arxiv.org/abs/hep-ph/0611184",
    "kapner_2007_prl": "https://doi.org/10.1103/PhysRevLett.98.021101",
    "adelberger_2003_review": "https://arxiv.org/abs/hep-ph/0307284",
}

LIVE_BOUND_CURVE = R10 / "derived" / "R10_alpha_lambda_bound_curve_DIGITIZED.csv"
LIVE_TAU_KERNEL = R10 / "derived" / "R10_delta_w_kernel_lambda.csv"

SOURCE_DOWNLOAD_LEDGER = OUT / "P8_Y5_R10_1509_SOURCE_DOWNLOAD_LEDGER.csv"
WEB_SOURCE_ANCHORS = OUT / "P8_Y5_R10_1509_WEB_SOURCE_ANCHORS.csv"
ANCHOR_CURVE = CANDIDATES / "R10_alpha_lambda_bound_curve_1509_SOURCE_ANCHORS_NONCLAIM.csv"
TAU_KERNEL_SCHEMA = CANDIDATES / "R10_delta_w_kernel_lambda_1509_SCHEMA_NONCLAIM.csv"
SUPPLEMENTAL_LEDGER = OUT / "P8_Y5_R10_1509_SUPPLEMENTAL_TABLE_HUNT_LEDGER.csv"
CLAIM_GATE = OUT / "P8_Y5_R10_1509_R10_CLAIM_GATE.csv"
FREEZE_LEDGER = OUT / "P8_Y5_R10_1509_FREEZE_OR_PROCEED_LEDGER.csv"
TARGET_BLOCKERS = OUT / "P8_Y5_R10_1509_TARGET_PROMOTION_BLOCKERS.csv"
SCORE_READINESS = OUT / "P8_Y5_R10_1509_DELTA_W_SCORE_READINESS.csv"
LOCAL_STATUS = OUT / "P8_Y5_R10_1509_LOCAL_GR_NEWTON_STATUS.csv"
REJECTION_LEDGER = OUT / "P8_Y5_R10_1509_REJECTION_LEDGER.csv"
DECISION_LEDGER = OUT / "P8_Y5_R10_1509_DECISION_LEDGER.csv"
NEXT_TARGET = OUT / "P8_Y5_R10_1509_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1509_VALIDATION.csv"

QUARANTINE = MICROSCOPE / "quarantine" / "1509"
QUAR_ANCHORS = QUARANTINE / "R10_ALPHA_BOUND_SOURCE_ANCHORS_NONCLAIM.csv"
QUAR_TAU = QUARANTINE / "R10_TAU_KERNEL_SCHEMA_NONCLAIM.csv"
QUAR_GATE = QUARANTINE / "R10_CLAIM_GATE_NONCLAIM.csv"
BRANCH_ANCHORS = BRANCH_RESIDUALS / "r10_alpha_bound_source_anchors_nonclaim_1509.csv"
BRANCH_TAU = BRANCH_RESIDUALS / "r10_tau_kernel_schema_nonclaim_1509.csv"
BRANCH_GATE = BRANCH_RESIDUALS / "r10_claim_gate_nonclaim_1509.csv"


def flags() -> dict[str, bool]:
    return {"score_ready": False, "valid_prediction_row": False, "valid_for_claim": False, "claim_allowed": False}


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
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


def text_contains(path: Path, fragments: list[str]) -> bool:
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8", errors="ignore")
    return all(fragment in text for fragment in fragments)


def generated_flags_false(paths: list[Path]) -> bool:
    false_values = {"", "false", "0", "no", "none", "null"}
    claim_keys = ["score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed", "R10_pass_for_claim"]
    for path in paths:
        for row in read_csv(path):
            for key in claim_keys:
                if key in row and str(row[key]).strip().lower() not in false_values:
                    return False
    return True


def source_download_rows() -> list[dict[str, Any]]:
    rows = []
    for source_id, path in [
        ("SRC1509_0_2020_arxiv_source", SOURCE_2020_TAR),
        ("SRC1509_1_2020_tex", SOURCE_2020_TEX),
        ("SRC1509_2_2007_arxiv_source", SOURCE_2007_TAR),
        ("SRC1509_3_2007_tex", SOURCE_2007_TEX),
        ("SRC1509_4_2003_review_source", SOURCE_2003_TAR),
        ("SRC1509_5_2003_review_tex", SOURCE_2003_TEX),
    ]:
        exists = path.exists()
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "source_id": source_id,
                "local_path": rel(path),
                "exists": exists,
                "bytes": path.stat().st_size if exists and path.is_file() else 0,
                "status": "LOCAL_SOURCE_AVAILABLE" if exists else "MISSING_LOCAL_SOURCE",
                "retrieved_or_checked_utc": datetime.now(timezone.utc).isoformat(),
                **flags(),
            }
        )
    return rows


def web_anchor_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "anchor_id": "ANCHOR1509_0_2020_grav_strength_threshold",
            "paper": "Lee et al. 2020 PRL / arXiv:2002.11761",
            "source_url": EXTERNAL_SOURCES["lee_2020_arxiv"],
            "related_doi": EXTERNAL_SOURCES["lee_2020_prl"],
            "local_source": rel(SOURCE_2020_TEX),
            "evidence": "data separations 52 um to 3.0 mm; gravitational-strength Yukawa ranges limited to <38.6 um; constraints on alpha displayed in Fig. 5 and positive/negative alpha values delegated to Supplemental Material",
            "lambda_value": "3.86000000e-05",
            "lambda_units": "m",
            "alpha_bound": "1.00000000e+00",
            "constraint_type": "alpha_equals_one_threshold_anchor",
            "curve_status": "ANCHOR_ONLY_NON_CURVE",
            "extraction_method": "source_text_anchor_not_digitized_curve",
            "confidence_level": "95_percent",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "anchor_id": "ANCHOR1509_1_2007_grav_strength_threshold",
            "paper": "Kapner et al. 2007 PRL / arXiv:hep-ph/0611184",
            "source_url": EXTERNAL_SOURCES["kapner_2007_arxiv"],
            "related_doi": EXTERNAL_SOURCES["kapner_2007_prl"],
            "local_source": rel(SOURCE_2007_TEX),
            "evidence": "inverse-square law holds with |alpha| <= 1 down to lambda = 56 um at 95 percent confidence; included only as continuity anchor older than 2020",
            "lambda_value": "5.60000000e-05",
            "lambda_units": "m",
            "alpha_bound": "1.00000000e+00",
            "constraint_type": "alpha_equals_one_threshold_anchor",
            "curve_status": "ANCHOR_ONLY_NON_CURVE",
            "extraction_method": "source_text_anchor_not_digitized_curve",
            "confidence_level": "95_percent",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "anchor_id": "ANCHOR1509_2_2003_review_context",
            "paper": "Adelberger, Heckel, Nelson 2003 review / arXiv:hep-ph/0307284",
            "source_url": EXTERNAL_SOURCES["adelberger_2003_review"],
            "related_doi": "https://doi.org/10.1146/annurev.nucl.53.041002.110503",
            "local_source": rel(SOURCE_2003_TEX),
            "evidence": "review context for inverse-square-law Yukawa constraints; not a modern bound curve row",
            "lambda_value": "MISSING_REVIEW_ROW_NOT_NUMERIC",
            "lambda_units": "m",
            "alpha_bound": "MISSING_REVIEW_ROW_NOT_NUMERIC",
            "constraint_type": "review_context_only",
            "curve_status": "NOT_A_BOUND_ROW",
            "extraction_method": "review_context",
            "confidence_level": "not_applicable",
            **flags(),
        },
    ]


def anchor_curve_rows() -> list[dict[str, Any]]:
    rows = []
    for anchor in web_anchor_rows()[:2]:
        rows.append(
            {
                "bound_id": anchor["anchor_id"].replace("ANCHOR", "BOUND"),
                "lambda_value": anchor["lambda_value"],
                "lambda_units": anchor["lambda_units"],
                "alpha_bound": anchor["alpha_bound"],
                "alpha_bound_units": "dimensionless_relative_to_gravity",
                "source_url": anchor["source_url"],
                "related_doi": anchor["related_doi"],
                "local_source": anchor["local_source"],
                "extraction_method": anchor["extraction_method"],
                "curve_status": anchor["curve_status"],
                "full_curve": False,
                "valid_for_claim": False,
                "notes": "anchor only; not sufficient for interpolation, model scoring, or R10 claim",
            }
        )
    return rows


def tau_kernel_rows() -> list[dict[str, Any]]:
    return [
        {
            "kernel_id": "TAU1509_0_R10_geometry_kernel",
            "lambda_value": "MISSING_lambda_grid",
            "lambda_units": "m",
            "tau_R10": "MISSING_tau_R10",
            "geometry_terms": "MISSING_detector_attractor_finite_source_integral",
            "source_path": rel(SOURCE_2020_TEX),
            "status": "SCHEMA_ONLY_NONCLAIM",
            "valid_for_claim": False,
            "notes": "paper describes Fourier-Bessel/Yukawa torque modelling, but no reusable tau_R10(lambda) kernel was extracted here",
        }
    ]


def supplemental_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "hunt_id": "SUP1509_0_2020_supplement",
            "source": EXTERNAL_SOURCES["lee_2020_prl"],
            "local_evidence": rel(SOURCE_2020_TEX),
            "finding": "TeX says positive/negative alpha constraint values are in Supplemental Material; arXiv source bundle contains figure PDFs but no machine-readable alpha table",
            "status": "SUPPLEMENT_REQUIRED_FOR_FULL_CURVE_OR_DIGITIZE_FIG5",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "hunt_id": "SUP1509_1_2007_source",
            "source": EXTERNAL_SOURCES["kapner_2007_arxiv"],
            "local_evidence": rel(SOURCE_2007_TEX),
            "finding": "source gives alpha=1 threshold and plotted constraints, but not a modern full curve for 2020 scoring",
            "status": "CONTINUITY_ANCHOR_ONLY",
            **flags(),
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    requirements = [
        ("GATE1509_0_full_curve", "reviewed alpha_bound(lambda) full curve", "MISSING"),
        ("GATE1509_1_tau_kernel", "tau_R10(lambda) finite-source response kernel", "MISSING"),
        ("GATE1509_2_parent_alpha", "MTS alpha_predicted(lambda) from parent coefficients or zero theorem", "MISSING"),
        ("GATE1509_3_interpolation", "interpolation over overlapping lambda grid", "BLOCKED_BY_MISSING_CURVE_KERNEL"),
        ("GATE1509_4_decision", "R10/local-GR claim", "FALSE_FREEZE_LOCAL_R10_SCORE"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "requirement": requirement,
            "current_status": status,
            "effect": "R10 branch cannot score or claim until this gate closes",
            **flags(),
        }
        for gate_id, requirement, status in requirements
    ]


def blocker_rows() -> list[dict[str, Any]]:
    rows = [
        ("BLOCK1509_0", "2020 supplemental alpha table or reviewed Fig. 5 digitization missing"),
        ("BLOCK1509_1", "tau_R10(lambda) finite-source kernel missing"),
        ("BLOCK1509_2", "field-specific L_X zero theorem remains unsigned from 1508"),
        ("BLOCK1509_3", "MTS alpha_predicted(lambda) parent coefficients missing"),
        ("BLOCK1509_4", "anchor rows are not a full curve and are valid_for_claim=false"),
        ("BLOCK1509_5", "live R10 derived curve/kernel files remain intentionally absent"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "blocker_id": blocker_id,
            "blocker": blocker,
            "effect": "freeze local R10 scoring; continue source acquisition or digitization only",
            **flags(),
        }
        for blocker_id, blocker in rows
    ]


def score_readiness_rows(blockers: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "score_id": "SCORE1509_0",
            "status": "NOT_SCORE_READY",
            "missing_blockers": "; ".join(row["blocker"] for row in blockers),
            "required_before_scoring": "full reviewed alpha_bound(lambda), tau_R10(lambda), and parent alpha_predicted(lambda) rows",
            **flags(),
        }
    ]


def freeze_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "freeze_id": "FREEZE1509_0",
            "decision": "FREEZE_LOCAL_R10_SCORE_NOT_THEORY",
            "meaning": "the local R10 scoring branch is frozen as nonclaim; the broader MTS/GR derivation work remains live",
            "unfreeze_condition": "supply full alpha_bound(lambda), tau_R10(lambda), and parent alpha_predicted(lambda), or close field-specific zero theorem",
            **flags(),
        }
    ]


def local_status_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "local_status_id": "LRS1509_0",
            "object": "local R10 / short-range fifth-force branch",
            "status": "FROZEN_FOR_SCORING_NONCLAIM",
            "effect": "does not prove or disprove MTS; it blocks public local-GR/R10 claim until evidence arrives",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "local_status_id": "LRS1509_1",
            "object": "GR/Newton derivability target",
            "status": "STILL_PRIMARY_TARGET",
            "effect": "derive EH/Newton/local decoupling independently; R10 remains one empirical gate, not the whole theory",
            **flags(),
        },
    ]


def simple_rows_from_blockers(blockers: list[dict[str, Any]], prefix: str) -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            f"{prefix}_id": blocker["blocker_id"].replace("BLOCK", prefix.upper()),
            "status": "RETAIN_BLOCKER",
            "item": blocker["blocker"],
            "reason": blocker["effect"],
            **flags(),
        }
        for blocker in blockers
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1509_0_anchor_rows",
            "decision": "use source-backed anchors only as nonclaim evidence",
            "rationale": "anchors verify scale and continuity, but cannot support interpolation or model comparison",
            "next_action": "hunt supplemental table or digitize Fig. 5 under reviewed protocol",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1509_1_tau_kernel",
            "decision": "tau_R10 remains schema-only",
            "rationale": "paper describes torque modelling but no extracted reusable MTS tau kernel exists",
            "next_action": "derive or implement finite-source Yukawa kernel separately",
            **flags(),
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "next_id": "NEXT1509_0_1510",
            "next_target": "1510-Y5-R10-RAB-reviewed-figure-digitization-protocol-or-return-to-GR-derivation.md",
            "script": "scripts/Y5_R10_RAB_reviewed_figure_digitization_protocol_or_return_to_GR_derivation.py",
            "objective": "either create a reviewed digitization protocol for the R10 Fig. 5 alpha_bound(lambda) curve and tau kernel, or deliberately pivot back to parent GR/Newton derivation while R10 scoring stays frozen",
            **flags(),
        }
    ]


def copy_outputs() -> None:
    for path in [QUARANTINE, BRANCH_RESIDUALS]:
        path.mkdir(parents=True, exist_ok=True)
    for src, dst in [
        (ANCHOR_CURVE, QUAR_ANCHORS),
        (TAU_KERNEL_SCHEMA, QUAR_TAU),
        (CLAIM_GATE, QUAR_GATE),
        (ANCHOR_CURVE, BRANCH_ANCHORS),
        (TAU_KERNEL_SCHEMA, BRANCH_TAU),
        (CLAIM_GATE, BRANCH_GATE),
    ]:
        shutil.copyfile(src, dst)


def validation_rows(generated_csvs: list[Path], anchors: list[dict[str, Any]], tau_rows: list[dict[str, Any]], gate: list[dict[str, Any]]) -> list[dict[str, Any]]:
    source_paths_exist = all(path.exists() for path in SOURCE_FILES.values())
    source_tars_nonempty = all(path.exists() and path.stat().st_size > 0 for path in [SOURCE_2020_TAR, SOURCE_2007_TAR, SOURCE_2003_TAR])
    anchor_2020_found = text_contains(SOURCE_2020_TEX, ["52~\\mu", "38.6", "Supplemental Material"])
    anchor_2007_found = text_contains(SOURCE_2007_TEX, ["|\\alpha| \\leq 1", "\\lambda = 56"])
    anchor_rows_numeric = all(float(row["lambda_value"]) > 0 and float(row["alpha_bound"]) > 0 and row["curve_status"] == "ANCHOR_ONLY_NON_CURVE" for row in anchors)
    anchor_rows_nonclaim = all(row["valid_for_claim"] is False and row["full_curve"] is False for row in anchors)
    tau_schema_nonclaim = all(row["valid_for_claim"] is False and row["status"] == "SCHEMA_ONLY_NONCLAIM" for row in tau_rows)
    claim_gate_frozen = any(row["gate_id"] == "GATE1509_4_decision" and row["current_status"] == "FALSE_FREEZE_LOCAL_R10_SCORE" for row in gate)
    live_targets_absent = not LIVE_BOUND_CURVE.exists() and not LIVE_TAU_KERNEL.exists()
    csv_parse_ok = all(parse_csv(path) for path in generated_csvs)
    flags_false = generated_flags_false(generated_csvs)
    branch_copies = all(path.exists() for path in [QUAR_ANCHORS, QUAR_TAU, QUAR_GATE, BRANCH_ANCHORS, BRANCH_TAU, BRANCH_GATE])
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    pycache_absent = not pycache.exists()
    formalization_modified = 0
    if FORMALIZATION.exists():
        formalization_modified = sum(1 for path in FORMALIZATION.rglob("*") if path.is_file() and path.stat().st_mtime > START_TS)
    checks = [
        ("VAL1509_0_local_sources", source_paths_exist, "all cited 1508 and R10 source paths exist"),
        ("VAL1509_1_source_tars_nonempty", source_tars_nonempty, "downloaded arXiv source bundles are present and nonempty"),
        ("VAL1509_2_2020_anchor_text", anchor_2020_found, "2020 source text contains 52 um, 38.6 um, and supplemental-material cues"),
        ("VAL1509_3_2007_anchor_text", anchor_2007_found, "2007 source text contains |alpha|<=1 and lambda=56 um cues"),
        ("VAL1509_4_anchor_numeric", anchor_rows_numeric, "anchor rows have positive numeric lambda and alpha values"),
        ("VAL1509_5_anchor_nonclaim", anchor_rows_nonclaim, "anchor rows are not full curves and are valid_for_claim=false"),
        ("VAL1509_6_tau_schema_nonclaim", tau_schema_nonclaim, "tau kernel remains schema-only and nonclaim"),
        ("VAL1509_7_claim_gate_frozen", claim_gate_frozen, "R10/local scoring is explicitly frozen"),
        ("VAL1509_8_live_targets_absent", live_targets_absent, "live derived R10 curve/kernel targets remain absent"),
        ("VAL1509_9_csv_parse", csv_parse_ok, "all generated 1509 CSVs parse cleanly"),
        ("VAL1509_10_branch_copies", branch_copies, "branch/quarantine nonclaim copies written"),
        ("VAL1509_11_pycache_absent", pycache_absent, "scripts __pycache__ absent after run"),
        ("VAL1509_12_formalization_untouched", formalization_modified == 0, f"formalization modified-file count since start={formalization_modified}"),
        ("VAL1509_13_claim_flags_false", flags_false, "all generated prediction/claim flags remain false"),
    ]
    overall = all(result for _, result, _ in checks)
    rows = [
        {"same_parent_branch_id": BRANCH_ID, "check_id": check_id, "result": "PASS" if result else "FAIL", "detail": detail}
        for check_id, result, detail in checks
    ]
    rows.append(
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": "VAL1509_14_overall",
            "result": "PASS" if overall else "FAIL",
            "detail": "1509 acquired local source bundles and anchor rows, but froze R10 scoring until full curve/tau/parent-alpha inputs exist"
            if overall
            else "1509 validation failed; inspect failed rows before continuing",
        }
    )
    return rows


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    output = ["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
    for row in rows:
        output.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |")
    return "\n".join(output)


def write_doc(
    downloads: list[dict[str, Any]],
    web_anchors: list[dict[str, Any]],
    anchors: list[dict[str, Any]],
    tau_rows: list[dict[str, Any]],
    gate: list[dict[str, Any]],
    freeze: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n".join(
            [
                "# 1509 - Acquire Reviewed R10 Bound Curve and Tau Kernel or Freeze Local R10",
                "",
                "## Verdict",
                "- Real R10 source bundles are now local, including the 2020 modern Eot-Wash paper source, the 2007 continuity paper source, and the 2003 review source.",
                "- The 2020 source gives strong anchor facts but says the numerical positive/negative alpha constraints are in Supplemental Material; the arXiv bundle does not provide a claim-ready curve table.",
                "- Therefore the local R10 scoring branch is frozen as nonclaim until a reviewed alpha_bound(lambda) curve, tau_R10(lambda) kernel, and parent alpha_predicted(lambda) are available.",
                "",
                "## Source Ledger",
                md_table(downloads, ["source_id", "local_path", "exists", "bytes", "status"]),
                "",
                "## Web Source Anchors",
                md_table(web_anchors, ["anchor_id", "paper", "lambda_value", "alpha_bound", "curve_status"]),
                "",
                "## Candidate Bound Rows",
                md_table(anchors, ["bound_id", "lambda_value", "alpha_bound", "curve_status", "valid_for_claim"]),
                "",
                "## Tau Kernel Schema",
                md_table(tau_rows, ["kernel_id", "lambda_value", "tau_R10", "status", "valid_for_claim"]),
                "",
                "## Claim Gate",
                md_table(gate, ["gate_id", "requirement", "current_status"]),
                "",
                "## Freeze Ledger",
                md_table(freeze, ["freeze_id", "decision", "unfreeze_condition"]),
                "",
                "## Validation",
                md_table(validation, ["check_id", "result", "detail"]),
                "",
                "## Next Target",
                md_table(next_rows, ["next_id", "next_target", "script", "objective"]),
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    CANDIDATES.mkdir(parents=True, exist_ok=True)
    downloads = source_download_rows()
    web_anchors = web_anchor_rows()
    anchors = anchor_curve_rows()
    tau_rows = tau_kernel_rows()
    supplemental = supplemental_rows()
    gate = claim_gate_rows()
    blockers = blocker_rows()
    readiness = score_readiness_rows(blockers)
    freeze = freeze_rows()
    local_rows = local_status_rows()
    rejections = simple_rows_from_blockers(blockers, "rejection")
    decisions = decision_rows()
    next_rows = next_target_rows()

    write_csv(SOURCE_DOWNLOAD_LEDGER, downloads)
    write_csv(WEB_SOURCE_ANCHORS, web_anchors)
    write_csv(ANCHOR_CURVE, anchors)
    write_csv(TAU_KERNEL_SCHEMA, tau_rows)
    write_csv(SUPPLEMENTAL_LEDGER, supplemental)
    write_csv(CLAIM_GATE, gate)
    write_csv(FREEZE_LEDGER, freeze)
    write_csv(TARGET_BLOCKERS, blockers)
    write_csv(SCORE_READINESS, readiness)
    write_csv(LOCAL_STATUS, local_rows)
    write_csv(REJECTION_LEDGER, rejections)
    write_csv(DECISION_LEDGER, decisions)
    write_csv(NEXT_TARGET, next_rows)
    copy_outputs()

    generated_csvs = [
        SOURCE_DOWNLOAD_LEDGER,
        WEB_SOURCE_ANCHORS,
        ANCHOR_CURVE,
        TAU_KERNEL_SCHEMA,
        SUPPLEMENTAL_LEDGER,
        CLAIM_GATE,
        FREEZE_LEDGER,
        TARGET_BLOCKERS,
        SCORE_READINESS,
        LOCAL_STATUS,
        REJECTION_LEDGER,
        DECISION_LEDGER,
        NEXT_TARGET,
    ]
    validation = validation_rows(generated_csvs, anchors, tau_rows, gate)
    write_csv(VALIDATION, validation)
    write_doc(downloads, web_anchors, anchors, tau_rows, gate, freeze, validation, next_rows)
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


if __name__ == "__main__":
    main()
