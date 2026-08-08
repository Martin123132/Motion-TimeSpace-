from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_FIRST_REAL_LOCAL_BOUND_SOURCE_AND_PARENT_COEFFICIENT_BLOCKER_2565"
CHECKPOINT_ID = "2565"

ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

DOC = ROOT / "2565-Y5-R2FR-first-real-local-bound-source-and-parent-coefficient-blocker.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_NO_SHADOW_2565_SOURCE_REGISTER.csv",
    "acquisition_ledger": OUT / "P8_Y5_NO_SHADOW_2565_ACQUISITION_LEDGER.csv",
    "bound_control_rows": OUT / "P8_Y5_NO_SHADOW_2565_BOUND_CONTROL_ROWS.csv",
    "runner_input_candidates": OUT / "P8_Y5_NO_SHADOW_2565_RUNNER_INPUT_CANDIDATES.csv",
    "parent_coefficient_blocker": OUT / "P8_Y5_NO_SHADOW_2565_PARENT_COEFFICIENT_BLOCKER.csv",
    "units_baseline_validation": OUT / "P8_Y5_NO_SHADOW_2565_UNITS_BASELINE_VALIDATION.csv",
    "claim_gates": OUT / "P8_Y5_NO_SHADOW_2565_CLAIM_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_NO_SHADOW_2565_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_NO_SHADOW_2565_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_NO_SHADOW_2565_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2565_VALIDATION.csv",
}

COPY_TARGETS = {
    "bound_control_rows": LOCAL_BOUNDS / "GK_first_real_bound_control_rows_2565_NONCLAIM.csv",
    "parent_coefficient_blocker": LOCAL_BOUNDS / "GK_parent_coefficient_blocker_2565_NONCLAIM.csv",
    "acquisition_queue": QUEUE / "JR2565_FIRST_REAL_LOCAL_BOUND_PARENT_BLOCKER_NONCLAIM.csv",
}

SOURCES = [
    {
        "source_id": "SRC2565_00_2564_doc",
        "source_path": ROOT / "2564-Y5-R2FR-GK-stress-bound-dry-run-and-baseline-control-runner.md",
        "needles": ["NEXT2564_0_selected", "GATE2564_1_baseline_controls", "VAL2564_OVERALL"],
        "role": "handoff selecting real local bound/control source row plus parent coefficient blocker",
    },
    {
        "source_id": "SRC2565_01_2563_missing_inputs",
        "source_path": OUT / "P8_Y5_NO_SHADOW_2563_MISSING_INPUTS_LEDGER.csv",
        "needles": ["MISS2563_0_parent_signs", "MISS2563_8_arena_kernels", "MISS2563_10_baselines"],
        "role": "active missing parent, kernel and baseline input ledger",
    },
    {
        "source_id": "SRC2565_02_R10_provenance",
        "source_path": LOCAL_BOUNDS / "P8_Y5_R10_BOUND_SOURCE_PROVENANCE.csv",
        "needles": ["EOTWASH_2020_PRL124101101", "38.6", "10.1103/PhysRevLett.124.101101"],
        "role": "source-backed R10 alpha equals one threshold provenance",
    },
    {
        "source_id": "SRC2565_03_2475_bound_candidates",
        "source_path": LOCAL_BOUNDS / "GK_first_real_local_bound_candidates_2475_NONCLAIM.csv",
        "needles": ["BOUND2475_R10_ANCHOR_ALPHA1_38P6UM", "3.86e-05", "anchor_only_non_curve"],
        "role": "previous first real R10 bound anchor candidate",
    },
    {
        "source_id": "SRC2565_04_2476_kernel_blocker",
        "source_path": LOCAL_BOUNDS / "R10_kernel_Cmetric_blocker_ledger_2476_NONCLAIM.csv",
        "needles": ["BLOCK2476_0_KR10", "BLOCK2476_1_Cmetric", "BLOCK2476_2_EGK"],
        "role": "existing blocker for R10 kernel, metric response and local residual norm",
    },
    {
        "source_id": "SRC2565_05_2476_source_map",
        "source_path": LOCAL_BOUNDS / "R10_kernel_Cmetric_source_map_2476_NONCLAIM.csv",
        "needles": ["alpha_pred(lambda)=K_R10(lambda)*C_metric*E_GK_bound", "PARENT_THEOREM_REQUIRED", "RUNNER_BLOCKED"],
        "role": "formal map shape and non-circular parent theorem warning",
    },
]


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base_row() -> dict[str, Any]:
    return {
        "timestamp_utc": stamp(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
        "claim_allowed": False,
    }


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    columns: list[str] = []
    for row in rows:
        for key in row:
            if key not in columns:
                columns.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = Path(source["source_path"])
        exists = path.exists()
        missing: list[str] = []
        if exists:
            text = read_text(path)
            missing = [needle for needle in source["needles"] if needle not in text]
        else:
            missing = list(source["needles"])
        rows.append(
            {
                **base_row(),
                "source_id": source["source_id"],
                "source_path": str(path),
                "exists": exists,
                "missing_needles": ";".join(missing),
                "source_pass": exists and not missing,
                "role": source["role"],
            }
        )
    return rows


def acquisition_ledger_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "ACQ2565_0_R10_anchor",
            "R10_short_range",
            "EOTWASH_2020_PRL124101101",
            "New Test of the Gravitational 1/r^2 Law at Separations down to 52 um",
            "https://arxiv.org/abs/2002.11761; https://doi.org/10.1103/PhysRevLett.124.101101; https://pubmed.ncbi.nlm.nih.gov/32216404/",
            "10.1103/PhysRevLett.124.101101",
            "source-backed abstract threshold; arXiv metadata inspected; local provenance already staged",
            "Newtonian gravity control fit described; 95 percent confidence gravitational-strength Yukawa interaction range less than 38.6 micrometers",
            "SOURCE_BACKED_BOUND_AND_CONTROL_METADATA",
            "external-bound side reduced; this is not an MTS prediction coefficient",
        ),
        (
            "ACQ2565_1_R10_review_curve",
            "R10_short_range",
            "R10_VECTOR_2020_REVIEW_CANDIDATE",
            "Eot-Wash 2020 Fig. 5b vector candidate",
            "local file: source-intake/local_bounds/R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv",
            "10.1103/PhysRevLett.124.101101",
            "local digitization review candidate only",
            "candidate curve exists but is not promoted because no official table or human visual QA is attached here",
            "REVIEW_CANDIDATE_NONCLAIM",
            "use only for smoke interpolation, not evidence",
        ),
        (
            "ACQ2565_2_PPN_deferred",
            "PPN_solar_system",
            "not_acquired",
            "PPN bound/control row",
            "",
            "",
            "deferred",
            "R10 selected first because source-backed threshold and baseline metadata are already locally staged",
            "BLOCKED_DEFERRED",
            "future PPN source row still needed",
        ),
    ]
    return [
        {
            **base_row(),
            "acquisition_id": acquisition_id,
            "arena": arena,
            "source_id": source_id,
            "title": title,
            "source_url": source_url,
            "doi": doi,
            "extraction_method": extraction_method,
            "acquired_content": acquired_content,
            "acquisition_status": status,
            "notes": notes,
        }
        for acquisition_id, arena, source_id, title, source_url, doi, extraction_method, acquired_content, status, notes in rows
    ]


def bound_control_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "row_id": "BOUND2565_R10_ANCHOR_ALPHA1_38P6UM",
            "row_kind": "external_bound_anchor",
            "arena": "R10_short_range",
            "lambda_value": "3.86e-05",
            "lambda_units": "m",
            "bound_symbol": "alpha_bound",
            "bound_value": "1.0",
            "bound_units": "dimensionless",
            "confidence": "95_percent",
            "source_id": "EOTWASH_2020_PRL124101101",
            "source_path_or_url": "https://arxiv.org/abs/2002.11761",
            "doi": "10.1103/PhysRevLett.124.101101",
            "data_status": "anchor_only_non_curve",
            "external_bound_source_valid": True,
            "runner_claim_valid": False,
            "claim_blocker": "ANCHOR_ONLY_NONCURVE;MISSING_MTS_PREDICTION_COEFFICIENTS",
        },
        {
            "row_id": "CONTROL2565_R10_NEWTON_GR_ALPHA_ZERO",
            "row_kind": "matched_baseline_control_metadata",
            "arena": "R10_short_range",
            "lambda_value": "3.86e-05",
            "lambda_units": "m",
            "bound_symbol": "baseline_alpha_residual",
            "bound_value": "0.0",
            "bound_units": "dimensionless",
            "confidence": "control_metadata",
            "source_id": "EOTWASH_2020_PRL124101101",
            "source_path_or_url": "https://arxiv.org/abs/2002.11761",
            "doi": "10.1103/PhysRevLett.124.101101",
            "data_status": "baseline_control_metadata_same_alpha_lambda_parser",
            "external_bound_source_valid": True,
            "runner_claim_valid": False,
            "claim_blocker": "CONTROL_METADATA_ONLY;MISSING_MTS_PREDICTION_COEFFICIENTS",
        },
        {
            "row_id": "BOUND2565_R10_REVIEW_NEAREST_ALPHA1",
            "row_kind": "review_candidate_curve_point",
            "arena": "R10_short_range",
            "lambda_value": "3.866316691563022e-05",
            "lambda_units": "m",
            "bound_symbol": "alpha_bound",
            "bound_value": "0.9915372447041295",
            "bound_units": "dimensionless",
            "confidence": "review_candidate",
            "source_id": "R10_VECTOR_2020_REVIEW_0154",
            "source_path_or_url": str(LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv"),
            "doi": "10.1103/PhysRevLett.124.101101",
            "data_status": "review_candidate_requires_human_or_official_QA",
            "external_bound_source_valid": False,
            "runner_claim_valid": False,
            "claim_blocker": "REVIEW_CANDIDATE_NONCLAIM;MISSING_MTS_PREDICTION_COEFFICIENTS",
        },
    ]
    return [{**base_row(), **row, "valid_for_claim": False, "claim_allowed": False} for row in rows]


def runner_input_candidate_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "runner_input_id": "RUN2565_R10_ANCHOR_WITH_BASELINE",
            "arena_id": "ARENA2563_R10",
            "arena": "R10_short_range",
            "E_GK_bound": "",
            "C_metric": "",
            "K_arena": "",
            "arena_bound": "1.0",
            "units": "dimensionless",
            "bound_row_id": "BOUND2565_R10_ANCHOR_ALPHA1_38P6UM",
            "baseline_control_row_id": "CONTROL2565_R10_NEWTON_GR_ALPHA_ZERO",
            "baseline_model": "Newton_GR_alpha_zero_control",
            "baseline_pipeline_status": "PASS_CONTROL_METADATA",
            "baseline_residual": "0.0",
            "valid_for_claim": False,
            "block_reasons": "MISSING_E_GK_BOUND;MISSING_C_METRIC;MISSING_K_R10;ANCHOR_ONLY_NONCURVE",
        },
        {
            "runner_input_id": "RUN2565_R10_REVIEW_CURVE_SMOKE",
            "arena_id": "ARENA2563_R10",
            "arena": "R10_short_range",
            "E_GK_bound": "",
            "C_metric": "",
            "K_arena": "",
            "arena_bound": "0.9915372447041295",
            "units": "dimensionless",
            "bound_row_id": "BOUND2565_R10_REVIEW_NEAREST_ALPHA1",
            "baseline_control_row_id": "CONTROL2565_R10_NEWTON_GR_ALPHA_ZERO",
            "baseline_model": "Newton_GR_alpha_zero_control",
            "baseline_pipeline_status": "PASS_CONTROL_METADATA",
            "baseline_residual": "0.0",
            "valid_for_claim": False,
            "block_reasons": "MISSING_E_GK_BOUND;MISSING_C_METRIC;MISSING_K_R10;REVIEW_CANDIDATE_NONCLAIM",
        },
    ]
    return [{**base_row(), **row, "claim_allowed": False} for row in rows]


def parent_coefficient_blocker_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "BLOCK2565_0_EGK",
            "E_GK_bound",
            "local GK stress residual norm",
            "needed before any R10 alpha prediction can be compared to the source-backed bound",
            "MISSING_PARENT_COEFFICIENTS",
            "derive from signed parent operator/no-hair theorem or provide sourced stress-bound coefficients",
        ),
        (
            "BLOCK2565_1_Cmetric",
            "C_metric",
            "stress-to-local-metric response",
            "maps GK stress residual into weak-field metric/Yukawa observable",
            "MISSING_ARENA_PROJECTION",
            "derive non-circular weak-field metric response from MTS parent action",
        ),
        (
            "BLOCK2565_2_KR10",
            "K_R10(lambda,geometry)",
            "Eot-Wash geometry/kernel map",
            "converts normalized metric/force residual into alpha(lambda) for the apparatus",
            "MISSING_ARENA_KERNEL",
            "derive or source apparatus kernel only after response variable is fixed",
        ),
        (
            "BLOCK2565_3_full_curve",
            "alpha_bound(lambda)",
            "claim-ready R10 bound curve",
            "needed for broad lambda comparison rather than one threshold anchor",
            "ANCHOR_ONLY_NONCURVE",
            "obtain official supplemental table or human-reviewed digitization before promotion",
        ),
        (
            "BLOCK2565_4_parent_sign",
            "Z_A,Z_G,m_A2,m_G2,c_AG",
            "operator signs and coercivity",
            "needed to convert stress-bound fallback into local no-hair/local-GR derivation",
            "MISSING_PARENT_SIGN_SOURCE",
            "return to parent action sign derivation; do not fit signs from R10 success",
        ),
    ]
    return [
        {
            **base_row(),
            "blocker_id": blocker_id,
            "missing_object": missing_object,
            "meaning": meaning,
            "why_needed": why_needed,
            "status": status,
            "next_action": next_action,
        }
        for blocker_id, missing_object, meaning, why_needed, status, next_action in rows
    ]


def units_baseline_validation_rows(bounds: list[dict[str, Any]], runners: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in bounds:
        lambda_ok = float(row["lambda_value"]) > 0 and row["lambda_units"] == "m"
        bound_ok = float(row["bound_value"]) >= 0 and row["bound_units"] == "dimensionless"
        source_ok = bool(row["doi"]) and bool(row["source_path_or_url"])
        rows.append(
            {
                **base_row(),
                "validation_id": f"UNITBASE2565_{row['row_id']}",
                "target_id": row["row_id"],
                "lambda_units_ok": lambda_ok,
                "bound_units_ok": bound_ok,
                "source_ok": source_ok,
                "baseline_ok": "not_applicable" if row["row_kind"] != "matched_baseline_control_metadata" else row["bound_value"] == "0.0",
                "status": "PASS_EXTERNAL_ROW_NONCLAIM" if lambda_ok and bound_ok and source_ok else "BLOCKED_BAD_EXTERNAL_ROW",
                "claim_allowed": False,
            }
        )
    for row in runners:
        baseline_ok = row["baseline_pipeline_status"] == "PASS_CONTROL_METADATA" and row["baseline_residual"] == "0.0"
        units_ok = row["units"] == "dimensionless"
        coefficients_missing = row["E_GK_bound"] == "" or row["C_metric"] == "" or row["K_arena"] == ""
        rows.append(
            {
                **base_row(),
                "validation_id": f"UNITBASE2565_{row['runner_input_id']}",
                "target_id": row["runner_input_id"],
                "lambda_units_ok": "not_applicable",
                "bound_units_ok": units_ok,
                "source_ok": True,
                "baseline_ok": baseline_ok,
                "status": "BLOCKED_MISSING_PARENT_RUNNER_COEFFICIENTS" if coefficients_missing and baseline_ok and units_ok else "FAIL_RUNNER_INPUT",
                "claim_allowed": False,
            }
        )
    return rows


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("GATE2565_0_real_bound_anchor", "A real source-backed R10 threshold bound is recorded.", "PASS_AS_BOUND_SOURCE", "Eot-Wash 2020 alpha=1 threshold anchor recorded with DOI/URLs", True, False),
        ("GATE2565_1_baseline_control", "A matched Newton/GR alpha-zero control metadata row is recorded.", "PASS_AS_CONTROL_METADATA", "same alpha-lambda parser control is now explicit", True, False),
        ("GATE2565_2_full_curve", "A claim-ready alpha(lambda) curve is acquired.", "BLOCKED", "only anchor plus review-candidate curve exists", False, False),
        ("GATE2565_3_parent_coefficients", "MTS parent coefficients are available for prediction.", "BLOCKED", "E_GK_bound, C_metric, K_R10 and signs remain missing", False, False),
        ("GATE2565_4_R10_compatibility", "MTS passes R10 local bound.", "BLOCKED", "external bound/control row exists but MTS prediction side is absent", False, False),
        ("GATE2565_5_local_GR", "local GR/PPN branch is derived.", "BLOCKED", "source acquisition does not replace parent no-hair/metric-response theorem", False, False),
        ("GATE2565_6_no_fitted_GM", "No fitted-GM or M_H_ref shortcut is used.", "PASS_GUARDRAIL", "R10 row uses alpha-bound source only, not source-mass fitting", True, False),
        ("GATE2565_7_no_GitHub", "No public/GitHub update.", "PASS_GUARDRAIL", "private checkpoint only", True, False),
    ]
    return [
        {
            **base_row(),
            "gate_id": gate_id,
            "claim": claim,
            "gate_status": gate_status,
            "reason": reason,
            "gate_pass": gate_pass,
            "claim_allowed": claim_allowed,
        }
        for gate_id, claim, gate_status, reason, gate_pass, claim_allowed in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        ("DEC2565_0_R10_first", "Use Eot-Wash 2020 as first real local bound/control row.", "source-backed alpha=1 threshold and Newton/GR control metadata are available", "external-bound side is now less hand-wavy"),
        ("DEC2565_1_keep_nonclaim", "Keep all 2565 rows nonclaim.", "anchor-only bound and missing parent coefficients cannot support MTS compatibility", "claim discipline retained"),
        ("DEC2565_2_parent_blocker", "Treat parent coefficient extraction as the active hard gap.", "external bound sourcing is no longer the limiting first issue", "next work moves back toward derivation"),
        ("DEC2565_3_next", "Try the non-circular R10 kernel/Cmetric/E_GK derivation next.", "this is the bridge from source-backed bound to actual MTS prediction", "2566 selected"),
    ]
    return [
        {
            **base_row(),
            "decision_id": decision_id,
            "decision": decision,
            "reason": reason,
            "effect": effect,
        }
        for decision_id, decision, reason, effect in rows
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            **base_row(),
            "route_id": "NEXT2565_0_selected",
            "selection_status": "selected",
            "target_file": "2566-Y5-R2FR-R10-kernel-Cmetric-EGK-derivation-or-blocker.md",
            "target_script": "scripts/Y5_R2FR_R10_kernel_Cmetric_EGK_derivation_or_blocker_2566.py",
            "task": "attempt a non-circular derivation of K_R10, C_metric and E_GK_bound from the parent/local weak-field branch; if absent, produce a blocker that routes back to parent metric-response/no-hair derivation",
            "acceptance_target": "kernel/source audit, dimensional bridge, parent coefficient status, baseline-control continuity, claim gates",
            "guardrails": "no local-GR claim; no fitted GM; no M_H_ref reuse; no plateau axiom; no GitHub",
        }
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    for target in COPY_TARGETS.values():
        target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(OUTPUTS["bound_control_rows"], COPY_TARGETS["bound_control_rows"])
    shutil.copyfile(OUTPUTS["parent_coefficient_blocker"], COPY_TARGETS["parent_coefficient_blocker"])
    shutil.copyfile(OUTPUTS["acquisition_ledger"], COPY_TARGETS["acquisition_queue"])
    source_map = {
        "bound_control_rows": OUTPUTS["bound_control_rows"],
        "parent_coefficient_blocker": OUTPUTS["parent_coefficient_blocker"],
        "acquisition_queue": OUTPUTS["acquisition_ledger"],
    }
    return [
        {
            **base_row(),
            "copy_id": copy_id,
            "source_path": str(source_map[copy_id]),
            "target_path": str(target),
            "source_exists": source_map[copy_id].exists(),
            "target_exists": target.exists(),
        }
        for copy_id, target in COPY_TARGETS.items()
    ]


def csv_row_count(path: Path) -> int:
    with path.open(newline="", encoding="utf-8") as handle:
        return len(list(csv.DictReader(handle)))


def validation_rows(data: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, status: bool, notes: str, detail: str = "") -> None:
        rows.append({**base_row(), "check_id": check_id, "status": "PASS" if status else "FAIL", "notes": notes, "detail": detail})

    bound_rows = data["bounds"]
    runner_rows = data["runners"]
    blocker_text = ";".join(row["missing_object"] for row in data["blockers"])
    add("VAL2565_00_sources_exist", all(row["source_pass"] is True for row in data["sources"]), "all cited local source paths exist and required needles are present")
    add("VAL2565_01_real_anchor", any(row["row_id"] == "BOUND2565_R10_ANCHOR_ALPHA1_38P6UM" and row["external_bound_source_valid"] is True for row in bound_rows), "R10 alpha=1 threshold anchor recorded")
    add("VAL2565_02_anchor_units_positive", all(float(row["lambda_value"]) > 0 and float(row["bound_value"]) >= 0 for row in bound_rows), "all bound/control rows have nonnegative numeric values and positive lambda")
    add("VAL2565_03_urls_doi", any("arxiv.org/abs/2002.11761" in row["source_path_or_url"] and row["doi"] == "10.1103/PhysRevLett.124.101101" for row in bound_rows), "source URL and DOI recorded")
    add("VAL2565_04_baseline_control", any(row["row_id"] == "CONTROL2565_R10_NEWTON_GR_ALPHA_ZERO" and row["bound_value"] == "0.0" for row in bound_rows), "matched Newton/GR alpha-zero baseline control metadata recorded")
    add("VAL2565_05_runner_blocked", all(row["claim_allowed"] is False for row in runner_rows), "runner input candidates remain claim-blocked")
    add("VAL2565_06_parent_blockers", all(term in blocker_text for term in ["E_GK_bound", "C_metric", "K_R10(lambda,geometry)"]), "parent coefficient blocker ledger names E_GK, C_metric and K_R10")
    add("VAL2565_07_units_baseline_validation", all(row["claim_allowed"] is False and row["status"] != "FAIL_RUNNER_INPUT" for row in data["unitbase"]), "units and baseline validation rows pass or block as expected")
    add("VAL2565_08_claim_gates_safe", all(row["claim_allowed"] is False for row in data["gates"]), "no claim gate allows local-GR/R10 claim")
    add("VAL2565_09_next_target_written", bool(data["next"]) and data["next"][0]["route_id"] == "NEXT2565_0_selected", "2566 R10 kernel/Cmetric/EGK derivation target selected")
    add("VAL2565_10_branch_copies", all(row["source_exists"] and row["target_exists"] for row in data["copies"]), "nonclaim branch copies exist")
    markers = ("2565-Y5", "P8_Y5_NO_SHADOW_2565", "P8_Y5_BRR545_2565", "JR2565")
    formal_hits = [path for path in FORMALIZATION.rglob("*") if path.is_file() and any(marker in path.name for marker in markers)] if FORMALIZATION.exists() else []
    add("VAL2565_11_no_formalization_artifacts", not formal_hits, "no 2565 artifacts were written to formalization-workbench", ";".join(str(path) for path in formal_hits))
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        try:
            count = csv_row_count(path)
            add(f"VAL2565_CSV_{path.stem}", count > 0, f"CSV parses with {count} rows", str(path))
        except Exception as exc:
            add(f"VAL2565_CSV_{path.stem}", False, f"CSV parse failed: {exc}", str(path))
    for copy_id, path in COPY_TARGETS.items():
        try:
            count = csv_row_count(path)
            add(f"VAL2565_COPY_CSV_{copy_id}", count > 0, f"copy CSV parses with {count} rows", str(path))
        except Exception as exc:
            add(f"VAL2565_COPY_CSV_{copy_id}", False, f"copy CSV parse failed: {exc}", str(path))
    add("VAL2565_OVERALL", all(row["status"] == "PASS" for row in rows), "2565 records first real R10 bound/control source row and keeps parent coefficient gap explicit")
    return rows


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(column, "")) for column in columns) + " |")
    return "\n".join(lines)


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    sections = [
        "# 2565 Y5 R2FR First Real Local Bound Source And Parent Coefficient Blocker",
        "",
        "**Status:** first real local bound/control source row wired into the 2564 harness, but no MTS local-test claim is allowed. The R10/Eot-Wash 2020 alpha=1 threshold at lambda 38.6 micrometers is source-backed; the matched Newton/GR alpha-zero control metadata is explicit; the MTS prediction side is still blocked by missing `E_GK_bound`, `C_metric`, `K_R10`, full curve QA and parent sign data.",
        "",
        "**Meaning:** the external-bound side is no longer pure placeholder. The hard gap has moved where it belongs: deriving a non-circular local weak-field response from MTS into an R10 alpha(lambda) prediction.",
        "",
        "## Source Register",
        markdown_table(data["sources"], ["source_id", "source_path", "exists", "missing_needles", "source_pass", "role"]),
        "",
        "## Acquisition Ledger",
        markdown_table(data["acquisitions"], ["acquisition_id", "arena", "source_id", "title", "source_url", "doi", "extraction_method", "acquired_content", "acquisition_status", "notes"]),
        "",
        "## Bound And Control Rows",
        markdown_table(data["bounds"], ["row_id", "row_kind", "arena", "lambda_value", "lambda_units", "bound_symbol", "bound_value", "bound_units", "confidence", "source_id", "source_path_or_url", "doi", "data_status", "external_bound_source_valid", "runner_claim_valid", "claim_blocker", "claim_allowed"]),
        "",
        "## Runner Input Candidates",
        markdown_table(data["runners"], ["runner_input_id", "arena_id", "arena", "E_GK_bound", "C_metric", "K_arena", "arena_bound", "units", "bound_row_id", "baseline_control_row_id", "baseline_model", "baseline_pipeline_status", "baseline_residual", "block_reasons", "claim_allowed"]),
        "",
        "## Parent Coefficient Blocker",
        markdown_table(data["blockers"], ["blocker_id", "missing_object", "meaning", "why_needed", "status", "next_action"]),
        "",
        "## Units Baseline Validation",
        markdown_table(data["unitbase"], ["validation_id", "target_id", "lambda_units_ok", "bound_units_ok", "source_ok", "baseline_ok", "status", "claim_allowed"]),
        "",
        "## Claim Gates",
        markdown_table(data["gates"], ["gate_id", "claim", "gate_status", "reason", "gate_pass", "claim_allowed"]),
        "",
        "## Decision Ledger",
        markdown_table(data["decisions"], ["decision_id", "decision", "reason", "effect"]),
        "",
        "## Next Target",
        markdown_table(data["next"], ["route_id", "selection_status", "target_file", "target_script", "task", "acceptance_target", "guardrails"]),
        "",
        "## Branch Copies",
        markdown_table(data["copies"], ["copy_id", "source_path", "target_path", "source_exists", "target_exists"]),
        "",
        "## Validation",
        markdown_table(data["validations"], ["check_id", "status", "notes", "detail"]),
        "",
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    LOCAL_BOUNDS.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)
    bounds = bound_control_rows()
    runners = runner_input_candidate_rows()
    data = {
        "sources": source_register_rows(),
        "acquisitions": acquisition_ledger_rows(),
        "bounds": bounds,
        "runners": runners,
        "blockers": parent_coefficient_blocker_rows(),
        "unitbase": units_baseline_validation_rows(bounds, runners),
        "gates": claim_gate_rows(),
        "decisions": decision_rows(),
        "next": next_target_rows(),
    }
    write_csv(OUTPUTS["source_register"], data["sources"])
    write_csv(OUTPUTS["acquisition_ledger"], data["acquisitions"])
    write_csv(OUTPUTS["bound_control_rows"], data["bounds"])
    write_csv(OUTPUTS["runner_input_candidates"], data["runners"])
    write_csv(OUTPUTS["parent_coefficient_blocker"], data["blockers"])
    write_csv(OUTPUTS["units_baseline_validation"], data["unitbase"])
    write_csv(OUTPUTS["claim_gates"], data["gates"])
    write_csv(OUTPUTS["decision_ledger"], data["decisions"])
    write_csv(OUTPUTS["next_target"], data["next"])
    data["copies"] = copy_branch_outputs()
    write_csv(OUTPUTS["branch_copies"], data["copies"])
    data["validations"] = validation_rows(data)
    write_csv(OUTPUTS["validation"], data["validations"])
    write_doc(data)
    print(f"wrote {DOC}")
    for key, path in OUTPUTS.items():
        print(f"wrote {key}: {path}")
    for key, path in COPY_TARGETS.items():
        print(f"copied {key}: {path}")


if __name__ == "__main__":
    main()
