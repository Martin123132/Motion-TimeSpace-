from __future__ import annotations

import csv
import importlib.util
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CUTOFF = datetime.fromisoformat("2026-05-31T14:42:00")

STATUS = "Y5_R10_904_finite_alpha_source_provenance_and_real_bound_curve_gate_built_anchor_only_nonclaim"
CLAIM_CEILING = "source_provenance_and_anchor_only_R10_bound_gate_no_digitized_curve_no_numeric_MTS_alpha_no_R10_or_local_GR_claim"
NEXT_TARGET = "905-Y5-R10-parent-finite-alpha-input-owner-or-digitized-bound-curve-worker.md"
ANCHOR_BOUND_FILE = LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_904_SOURCE_BACKED_ANCHORS_NONCLAIM.csv"
R10_DRY_RUN_DIR = OUT / "P8_Y5_R10_904_R10_ANCHOR_DRY_RUNNER_RESULTS"

MTS_REQUIRED_COLUMNS = [
    "model_id",
    "branch_id",
    "curve_id",
    "lambda_value",
    "lambda_units",
    "alpha_predicted",
    "alpha_bound",
    "alpha_bound_source",
    "force_law_form",
    "derivation_status",
    "formula_reference",
    "source_file",
    "assumptions",
    "valid_for_claim",
    "notes",
]

BOUND_REQUIRED_COLUMNS = [
    "bound_id",
    "dataset_id",
    "lambda_value",
    "lambda_units",
    "alpha_bound",
    "alpha_bound_source",
    "digitization_method",
    "source_file",
    "valid_for_claim",
    "notes",
]

SOURCE_SPECS = [
    {
        "source_id": "903_doc",
        "path": ROOT / "903-Y5-R10-Qtr-source-cokernel-final-zero-proof-or-finite-alpha-source.md",
        "needle": "finite-alpha source acquisition",
        "role": "immediate handoff from failed Q_tr theorem promotion",
    },
    {
        "source_id": "903_validation",
        "path": OUT / "P8_Y5_BRR545_903_VALIDATION.csv",
        "needle": "V903_12_validation_rows_ready",
        "role": "prior checkpoint validation",
    },
    {
        "source_id": "903_finite_alpha_rows",
        "path": OUT / "P8_Y5_R10_903_FINITE_ALPHA_SOURCE_ROWS.csv",
        "needle": "FAS903_6",
        "role": "MTS finite alpha input debt",
    },
    {
        "source_id": "903_qtr_zero_clauses",
        "path": OUT / "P8_Y5_R10_903_QTR_ZERO_PROOF_CLAUSES.csv",
        "needle": "QZP903_7_theorem_verdict",
        "role": "conditional theorem ceiling",
    },
    {
        "source_id": "r10_runner",
        "path": ROOT / "scripts" / "R10_alpha_lambda_bound_prediction_runner.py",
        "needle": "BOUND_REQUIRED_COLUMNS",
        "role": "existing R10 alpha(lambda) comparator",
    },
    {
        "source_id": "live_bound_placeholder",
        "path": LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_DIGITIZED.csv",
        "needle": "R10_BOUND_PLACEHOLDER_0",
        "role": "live bound curve remains placeholder/nonclaim",
    },
]


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def stringify(value: object) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    return "" if value is None else str(value)


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
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
        for row in rows:
            writer.writerow({field: stringify(row.get(field, "")) for field in fields})


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def has_needle(path: Path, needle: str) -> bool:
    return path.exists() and needle in read_text(path)


def md_table(rows: list[dict[str, object]]) -> str:
    if not rows:
        return "_No rows._"
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join("---" for _ in fields) + " |",
    ]
    for row in rows:
        values = [stringify(row.get(field, "")).replace("\n", " ").replace("|", "/") for field in fields]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def source_register_rows(generated_utc: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for spec in SOURCE_SPECS:
        path = Path(spec["path"])
        rows.append(
            {
                "source_id": spec["source_id"],
                "path": path,
                "exists": path.exists(),
                "needle_check": "pass" if has_needle(path, str(spec["needle"])) else "fail",
                "role": spec["role"],
                "valid_for_claim": False,
                "generated_utc": generated_utc,
            }
        )
    return rows


def web_source_anchor_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "web_source_id": "R10SRC904_0_Lee2020_arxiv",
            "title": "New Test of the Gravitational 1/r^2 Law at Separations down to 52 um",
            "authors": "J.G. Lee; E.G. Adelberger; T.S. Cook; S.M. Fleischer; B.R. Heckel",
            "year": 2020,
            "url": "https://arxiv.org/abs/2002.11761",
            "doi": "10.1103/PhysRevLett.124.101101",
            "source_role": "modern R10 short-range anchor",
            "usable_facts": "Yukawa form; data separations 52 um to 3.0 mm; 66 lambda values from 5 um to 9 mm; 95 percent alpha=1 threshold at 38.6 um",
            "curve_status": "figure_and_supplement_reference_only_not_digitized_here",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "web_source_id": "R10SRC904_1_EotWash_page",
            "title": "Eot-Wash Inverse Square Law current published results",
            "authors": "Eot-Wash Group",
            "year": 2023,
            "url": "https://www.npl.washington.edu/eotwash/inverse-square-law",
            "doi": "",
            "source_role": "experiment-group context and figure provenance",
            "usable_facts": "page describes 95 percent confidence constraints on Yukawa violation; axes are relative strength and characteristic range; Lee 2020 is the cited current result",
            "curve_status": "visual constraint context_only_no_machine_table",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "web_source_id": "R10SRC904_2_Kapner2007_arxiv",
            "title": "Tests of the Gravitational Inverse-Square Law below the Dark-Energy Length Scale",
            "authors": "D.J. Kapner; T.S. Cook; E.G. Adelberger; J.H. Gundlach; B.R. Heckel; C.D. Hoyle; H.E. Swanson",
            "year": 2007,
            "url": "https://arxiv.org/abs/hep-ph/0611184",
            "doi": "10.1103/PhysRevLett.98.021101",
            "source_role": "continuity anchor for older Eot-Wash bounds",
            "usable_facts": "separations 9.53 mm to 55 um; 95 percent alpha<=1 down to lambda=56 um",
            "curve_status": "older anchor_only_non_curve",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "web_source_id": "R10SRC904_3_Adelberger2003_review",
            "title": "Tests of the Gravitational Inverse-Square Law",
            "authors": "E.G. Adelberger; B.R. Heckel; A.E. Nelson",
            "year": 2003,
            "url": "https://arxiv.org/abs/hep-ph/0307284",
            "doi": "10.1146/annurev.nucl.53.041002.110503",
            "source_role": "review/continuity source for inverse-square-law formalism",
            "usable_facts": "review of experimental tests and motivations for inverse-square-law breakdown",
            "curve_status": "review_context_only_not_curve",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "web_source_id": "R10SRC904_4_APS_supplement",
            "title": "Lee 2020 APS supplemental material",
            "authors": "J.G. Lee et al.",
            "year": 2020,
            "url": "https://link.aps.org/supplemental/10.1103/PhysRevLett.124.101101",
            "doi": "10.1103/PhysRevLett.124.101101",
            "source_role": "preferred numerical curve source if accessible",
            "usable_facts": "search result states supplemental material has numerical values for Fig. 5 and fitting details",
            "curve_status": "access_attempt_blocked_403_in_shell; must acquire manually or via allowed source before claim",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def nonclaim_summary_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "what_changed": "split finite trace alpha into MTS-side parent provenance and experiment-side R10 bound-curve provenance",
            "best_partial_result": "Lee 2020 provides a source-backed alpha=1 threshold anchor at lambda=38.6 um and scan metadata, but not a local claim-grade digitized curve in this checkpoint",
            "hard_blockers": "MTS lacks Z_tr/lambda_tr/Q_tr/m/response coefficients; R10 lacks full digitized alpha(lambda) bound curve; APS supplement acquisition is blocked/unconfirmed",
            "what_is_not_claimed": "finite alpha value, R10 pass, alpha=0, Q_tr=0, local GR/Newton, or public bound satisfaction",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
    ]


def finite_alpha_provenance_rows(generated_utc: str) -> list[dict[str, object]]:
    prior_rows = read_csv(OUT / "P8_Y5_R10_903_FINITE_ALPHA_SOURCE_ROWS.csv")
    rows: list[dict[str, object]] = []
    for index, row in enumerate(prior_rows):
        quantity = row["quantity"]
        if quantity in {"Z_tr", "lambda_tr", "Q_tr_over_m_universal", "alpha_tr_AB(lambda_tr)"}:
            priority = "R10_primary"
        elif "C_tr" in quantity or "Delta_AB" in quantity:
            priority = "local_arena_secondary"
        else:
            priority = "branch_decision_primary"
        rows.append(
            {
                "provenance_id": f"FAP904_{index}",
                "quantity": quantity,
                "priority": priority,
                "required_parent_input": row["required_parent_input"],
                "current_value": row["current_value"],
                "current_status": row["current_status"],
                "required_source_path": row["source_path_required"],
                "numeric_gate": "must be finite numeric with units or theorem-zero/no-pole",
                "claim_gate": "false_until_no_MISSING_markers_and_source_path_exists",
                "valid_for_claim": False,
                "generated_utc": generated_utc,
            }
        )
    return rows


def r10_bound_anchor_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "bound_id": "R10_904_LEE2020_ALPHA1_38P6UM_ANCHOR",
            "dataset_id": "Lee_Adelberger_Cook_Fleischer_Heckel_PRL124_101101_2020",
            "lambda_value": "38.6",
            "lambda_units": "um",
            "alpha_bound": "1.0",
            "alpha_bound_source": "https://arxiv.org/abs/2002.11761; doi:10.1103/PhysRevLett.124.101101",
            "digitization_method": "source_text_threshold_anchor_only_non_curve",
            "source_file": "https://arxiv.org/abs/2002.11761",
            "valid_for_claim": False,
            "notes": "source-backed alpha=1 threshold; not a digitized alpha(lambda) curve and cannot support interpolation or claim scoring",
            "confidence": "95_percent_or_2sigma_context",
            "row_type": "anchor_only_non_curve",
            "curve_claim_status": "invalid_for_claim_until_full_curve_or_supplement_table",
            "generated_utc": generated_utc,
        },
        {
            "bound_id": "R10_904_KAPNER2007_ALPHA1_56UM_ANCHOR",
            "dataset_id": "Kapner_Cook_Adelberger_Gundlach_Heckel_Hoyle_Swanson_PRL98_021101_2007",
            "lambda_value": "56",
            "lambda_units": "um",
            "alpha_bound": "1.0",
            "alpha_bound_source": "https://arxiv.org/abs/hep-ph/0611184; doi:10.1103/PhysRevLett.98.021101",
            "digitization_method": "source_text_threshold_anchor_only_non_curve",
            "source_file": "https://arxiv.org/abs/hep-ph/0611184",
            "valid_for_claim": False,
            "notes": "older alpha=1 continuity anchor; not current full curve and cannot support MTS claim scoring",
            "confidence": "95_percent",
            "row_type": "anchor_only_non_curve",
            "curve_claim_status": "invalid_for_claim_until_full_curve_or_supplement_table",
            "generated_utc": generated_utc,
        },
    ]


def r10_curve_acquisition_gate_rows(generated_utc: str) -> list[dict[str, object]]:
    rows = [
        (
            "RCG904_0_full_abs_alpha_curve",
            "full |alpha|(lambda) exclusion curve",
            "preferred",
            "not_acquired",
            "must contain multiple positive numeric lambda/alpha rows across the plotted range with extraction method and source",
        ),
        (
            "RCG904_1_positive_negative_curves",
            "+alpha and -alpha curves from supplemental material",
            "preferred_if_supplement_available",
            "not_acquired",
            "must preserve sign branch and confidence convention before conversion to |alpha| gate",
        ),
        (
            "RCG904_2_fig5_digitization",
            "digitized Fig. 5 lower panel",
            "acceptable_private_smoke_only",
            "not_done",
            "requires image source, axis calibration, digitization uncertainty, and nonclaim label until audited",
        ),
        (
            "RCG904_3_text_threshold_anchor",
            "alpha=1 threshold at 38.6 um from Lee 2020",
            "anchor_only",
            "acquired_nonclaim",
            "may sanity-check units but cannot support interpolation or claim scoring",
        ),
        (
            "RCG904_4_live_bound_file",
            "source-intake/local_bounds/R10_alpha_lambda_bound_curve_DIGITIZED.csv",
            "live_claim_file",
            "still_placeholder",
            "must not be treated as evidence until placeholder rows are replaced by full source-backed curve rows",
        ),
    ]
    return [
        {
            "gate_id": gate_id,
            "bound_artifact": artifact,
            "priority": priority,
            "current_status": status,
            "acceptance_rule": rule,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
        for gate_id, artifact, priority, status, rule in rows
    ]


def r10_alpha_dry_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "model_id": "MTS_trace_finite_alpha_source_contract",
            "branch_id": "finite_alpha_missing_parent_sources",
            "curve_id": "FT904_R10_0_missing_MTS_alpha_inputs",
            "lambda_value": "MISSING_LAMBDA_TR",
            "lambda_units": "m",
            "alpha_predicted": "MISSING_ZTR_QTR_SOURCE_INPUTS",
            "alpha_bound": "MISSING_BOUND_LOOKUP",
            "alpha_bound_source": "source-intake/local_bounds/R10_alpha_lambda_bound_curve_904_SOURCE_BACKED_ANCHORS_NONCLAIM.csv",
            "force_law_form": "Yukawa alpha_tr_AB exp(-r/lambda_tr)",
            "derivation_status": "FINITE_ALPHA_SOURCE_PROVENANCE_MISSING",
            "formula_reference": "alpha_tr_AB=(Q_tr^A/m_A)*(Q_tr^B/m_B)/(4*pi*Z_tr*G_obs)",
            "source_file": "source-intake/mts_residuals/P8_Y5_R10_904_FINITE_ALPHA_PROVENANCE_GATE.csv",
            "assumptions": "no numeric parent coefficients; bound file is anchor-only nonclaim",
            "valid_for_claim": False,
            "notes": "runner must reject this row until parent values and full bound curve are real",
            "generated_utc": generated_utc,
        },
        {
            "model_id": "MTS_trace_Qtr_zero_escape",
            "branch_id": "Qtr_zero_not_parent_signed",
            "curve_id": "FT904_R10_1_Qtr_zero_still_unsigned",
            "lambda_value": "38.6",
            "lambda_units": "um",
            "alpha_predicted": "0.0",
            "alpha_bound": "1.0",
            "alpha_bound_source": "source-intake/local_bounds/R10_alpha_lambda_bound_curve_904_SOURCE_BACKED_ANCHORS_NONCLAIM.csv",
            "force_law_form": "alpha_tr=0 only if Q_tr=0 or no local trace pole is parent-signed",
            "derivation_status": "QTR_ZERO_THEOREM_UNSIGNED_NONCLAIM",
            "formula_reference": "903 Q_tr source-cokernel theorem clauses",
            "source_file": "source-intake/mts_residuals/P8_Y5_R10_903_QTR_ZERO_PROOF_CLAUSES.csv",
            "assumptions": "numeric alpha shown only as theorem-shape smoke row; theorem is unsigned and row is invalid",
            "valid_for_claim": False,
            "notes": "prevents accidentally counting alpha=0 as a pass before theorem promotion",
            "generated_utc": generated_utc,
        },
    ]


def branch_decision_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "branch_id": "BD904_0_MTS_parent_inputs",
            "branch": "source Z_tr/lambda_tr/Q_tr/m and response coefficients",
            "decision": "dominant_blocker",
            "reason": "without MTS-side alpha(lambda) inputs, even a perfect R10 curve cannot score the theory",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "branch_id": "BD904_1_R10_bound_curve",
            "branch": "acquire full digitized/source table R10 bound curve",
            "decision": "parallel_data_blocker",
            "reason": "Lee 2020 gives source-backed anchors and figure/supplement provenance, but not a claim-grade curve in this checkpoint",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "branch_id": "BD904_2_selected_next",
            "branch": "parent finite alpha input owner or digitized curve worker",
            "decision": NEXT_TARGET,
            "reason": "next useful step must choose whether to attack MTS parent coefficients first or launch a bounded curve-digitization worker; both remain private/nonclaim",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def claim_gate_rows(generated_utc: str) -> list[dict[str, object]]:
    gates = [
        ("CGATE904_0_MTS_alpha", "numeric MTS alpha_tr(lambda_tr)", "Z_tr/lambda_tr/Q_tr/m are missing or theorem-dependent"),
        ("CGATE904_1_R10_bound_curve", "claim-grade R10 bound curve", "only anchor rows are acquired; full curve/supplement table missing"),
        ("CGATE904_2_R10_compare", "R10 comparison pass", "runner has zero valid MTS rows and zero valid bound rows"),
        ("CGATE904_3_Qtr_zero", "Q_tr=0 theorem", "903 proof remains unsigned"),
        ("CGATE904_4_local_GR", "local GR/Newton reduction", "finite trace coupling not eliminated or bounded"),
    ]
    return [
        {
            "gate_id": gate_id,
            "claim": claim,
            "claim_allowed": False,
            "blocker": blocker,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
        for gate_id, claim, blocker in gates
    ]


def next_target_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "next_target": NEXT_TARGET,
            "objective": "choose the highest-yield next worker: parent finite-alpha input owner first, or R10 digitized-bound worker if empirical plumbing is prioritized",
            "recommended_order": "parent_inputs_first_then_bound_digitization",
            "reason": "MTS alpha(lambda) is currently missing, so bound digitization alone cannot create a testable comparison",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
    ]


def prior_903_clean() -> bool:
    rows = read_csv(OUT / "P8_Y5_BRR545_903_VALIDATION.csv")
    return bool(rows) and all(row.get("result") == "pass" for row in rows)


def formalization_changed_count() -> int:
    if not FORMALIZATION.exists():
        return 0
    count = 0
    for path in FORMALIZATION.rglob("*"):
        if path.is_file() and datetime.fromtimestamp(path.stat().st_mtime) > CUTOFF:
            count += 1
    return count


def all_generated_rows_nonclaim(row_groups: list[list[dict[str, object]]]) -> bool:
    for group in row_groups:
        for row in group:
            if "valid_for_claim" in row and stringify(row["valid_for_claim"]).lower() != "false":
                return False
            if "claim_allowed" in row and stringify(row["claim_allowed"]).lower() != "false":
                return False
    return True


def anchor_rows_numeric_nonclaim(rows: list[dict[str, object]]) -> bool:
    if not rows:
        return False
    for row in rows:
        try:
            lambda_value = float(stringify(row["lambda_value"]))
            alpha_bound = float(stringify(row["alpha_bound"]))
        except ValueError:
            return False
        if lambda_value <= 0 or alpha_bound <= 0:
            return False
        if stringify(row.get("valid_for_claim")).lower() != "false":
            return False
        if row.get("row_type") != "anchor_only_non_curve":
            return False
    return True


def import_r10_runner() -> Any:
    runner_path = ROOT / "scripts" / "R10_alpha_lambda_bound_prediction_runner.py"
    spec = importlib.util.spec_from_file_location("r10_runner_904", runner_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {runner_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_r10_dry_runner() -> dict[str, Any]:
    module = import_r10_runner()
    result = module.run_runner(
        OUT / "P8_Y5_R10_904_R10_ALPHA_DRY_ROWS.csv",
        ANCHOR_BOUND_FILE,
        R10_DRY_RUN_DIR,
    )
    return result["status"]


def validation_rows(
    generated_utc: str,
    source_rows_: list[dict[str, object]],
    web_rows_: list[dict[str, object]],
    summary_rows_: list[dict[str, object]],
    finite_rows_: list[dict[str, object]],
    bound_rows_: list[dict[str, object]],
    acquisition_rows_: list[dict[str, object]],
    dry_rows_: list[dict[str, object]],
    branch_rows_: list[dict[str, object]],
    claim_rows_: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    runner_status: dict[str, Any],
) -> list[dict[str, object]]:
    formalization_count = formalization_changed_count()
    row_groups = [
        web_rows_,
        summary_rows_,
        finite_rows_,
        bound_rows_,
        acquisition_rows_,
        dry_rows_,
        branch_rows_,
        claim_rows_,
        next_rows_,
    ]
    missing_mts_columns = [column for column in MTS_REQUIRED_COLUMNS if column not in dry_rows_[0]]
    missing_bound_columns = [column for column in BOUND_REQUIRED_COLUMNS if column not in bound_rows_[0]]
    checks = [
        {
            "check_id": "V904_0_sources_exist_and_needles",
            "result": "pass"
            if all(row["exists"] is True and row["needle_check"] == "pass" for row in source_rows_)
            else "fail",
            "detail": "all local source paths exist and needles are present",
        },
        {
            "check_id": "V904_1_prior_903_clean",
            "result": "pass" if prior_903_clean() else "fail",
            "detail": "P8_Y5_BRR545_903_VALIDATION.csv clean",
        },
        {
            "check_id": "V904_2_web_anchors_recorded_nonclaim",
            "result": "pass" if len(web_rows_) >= 5 and all(row["valid_for_claim"] is False for row in web_rows_) else "fail",
            "detail": "Lee/EotWash/Kapner/Adelberger/supplement rows recorded",
        },
        {
            "check_id": "V904_3_bound_anchor_rows_numeric_nonclaim",
            "result": "pass" if anchor_rows_numeric_nonclaim(bound_rows_) else "fail",
            "detail": f"anchor_rows={len(bound_rows_)}",
        },
        {
            "check_id": "V904_4_no_full_curve_claim",
            "result": "pass"
            if all("not_acquired" in stringify(row["current_status"]) or "nonclaim" in stringify(row["current_status"]) or "placeholder" in stringify(row["current_status"]) or "not_done" in stringify(row["current_status"]) for row in acquisition_rows_)
            else "fail",
            "detail": "full R10 curve remains unacquired/nonclaim",
        },
        {
            "check_id": "V904_5_finite_alpha_provenance_blocked",
            "result": "pass"
            if len(finite_rows_) == 8 and all(row["valid_for_claim"] is False for row in finite_rows_)
            else "fail",
            "detail": f"finite_rows={len(finite_rows_)}",
        },
        {
            "check_id": "V904_6_runner_schema_ok",
            "result": "pass" if not missing_mts_columns and not missing_bound_columns else "fail",
            "detail": "schema ok"
            if not missing_mts_columns and not missing_bound_columns
            else f"missing_mts={missing_mts_columns};missing_bound={missing_bound_columns}",
        },
        {
            "check_id": "V904_7_R10_runner_blocks_claim",
            "result": "pass"
            if runner_status.get("claim_allowed") is False
            and runner_status.get("valid_mts_rows") == 0
            and runner_status.get("valid_bound_rows") == 0
            else "fail",
            "detail": json.dumps(
                {
                    "claim_allowed": runner_status.get("claim_allowed"),
                    "valid_mts_rows": runner_status.get("valid_mts_rows"),
                    "valid_bound_rows": runner_status.get("valid_bound_rows"),
                    "blocked_or_failed_rows": runner_status.get("blocked_or_failed_rows"),
                },
                sort_keys=True,
            ),
        },
        {
            "check_id": "V904_8_claim_gates_false",
            "result": "pass" if all(row["claim_allowed"] is False for row in claim_rows_) else "fail",
            "detail": "all alpha/R10/local claims blocked",
        },
        {
            "check_id": "V904_9_all_generated_rows_nonclaim",
            "result": "pass" if all_generated_rows_nonclaim(row_groups) else "fail",
            "detail": "all generated rows keep valid_for_claim/claim_allowed false",
        },
        {
            "check_id": "V904_10_formalization_workbench_untouched",
            "result": "pass" if formalization_count == 0 else "fail",
            "detail": f"formalization_changed_after_cutoff={formalization_count}",
        },
        {
            "check_id": "V904_11_next_target_selected",
            "result": "pass" if next_rows_ and next_rows_[0]["next_target"] == NEXT_TARGET else "fail",
            "detail": NEXT_TARGET,
        },
        {
            "check_id": "V904_12_validation_rows_ready",
            "result": "pass",
            "detail": "validation table constructed",
        },
    ]
    for row in checks:
        row["generated_utc"] = generated_utc
    return checks


def write_markdown(
    path: Path,
    generated_utc: str,
    summary_rows_: list[dict[str, object]],
    source_rows_: list[dict[str, object]],
    web_rows_: list[dict[str, object]],
    finite_rows_: list[dict[str, object]],
    bound_rows_: list[dict[str, object]],
    acquisition_rows_: list[dict[str, object]],
    dry_rows_: list[dict[str, object]],
    branch_rows_: list[dict[str, object]],
    claim_rows_: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    validation_rows_: list[dict[str, object]],
) -> None:
    content = f"""# 904 - Y5/R10 Finite Alpha Source Provenance And Real Bound Curve Gate

Status: `{STATUS}`
Claim ceiling: `{CLAIM_CEILING}`
Generated UTC: `{generated_utc}`

Current result: **the R10 testing path is now split into two hard gates: MTS must source `Z_tr`, `lambda_tr`, `Q_tr/m`, and response coefficients; the experiment side must provide a real digitized/source-table `alpha(lambda)` curve.** Lee 2020 gives a source-backed `alpha=1` threshold anchor at `lambda=38.6 um`, but that is not a curve and it is not enough for interpolation, model comparison, or a pass.

## Exact 904 Finding
The evidence situation is clean now. The local trace coupling is not testable yet because the MTS-side `alpha_tr(lambda_tr)` row is still missing parent inputs. The R10 bound side has credible modern provenance, but only anchor rows were acquired here. The existing R10 runner correctly refuses the dry rows because there are zero valid MTS rows and zero valid bound rows.

## Nonclaim Summary
{md_table(summary_rows_)}

## Local Source Register
{md_table(source_rows_)}

## Web Source Anchors
{md_table(web_rows_)}

## Finite Alpha Provenance Gate
{md_table(finite_rows_)}

## R10 Bound Anchor Rows
{md_table(bound_rows_)}

## R10 Curve Acquisition Gate
{md_table(acquisition_rows_)}

## R10 Alpha Dry Rows
{md_table(dry_rows_)}

## Branch Decision
{md_table(branch_rows_)}

## Claim Gate
{md_table(claim_rows_)}

## Next Target
{md_table(next_rows_)}

## Validation
{md_table(validation_rows_)}
"""
    path.write_text(content, encoding="utf-8")


def main() -> None:
    generated_utc = now_utc()
    source_rows_ = source_register_rows(generated_utc)
    web_rows_ = web_source_anchor_rows(generated_utc)
    summary_rows_ = nonclaim_summary_rows(generated_utc)
    finite_rows_ = finite_alpha_provenance_rows(generated_utc)
    bound_rows_ = r10_bound_anchor_rows(generated_utc)
    acquisition_rows_ = r10_curve_acquisition_gate_rows(generated_utc)
    dry_rows_ = r10_alpha_dry_rows(generated_utc)
    branch_rows_ = branch_decision_rows(generated_utc)
    claim_rows_ = claim_gate_rows(generated_utc)
    next_rows_ = next_target_rows(generated_utc)

    write_csv(ANCHOR_BOUND_FILE, bound_rows_)

    initial_outputs = {
        "P8_Y5_R10_904_SOURCE_REGISTER.csv": source_rows_,
        "P8_Y5_R10_904_WEB_SOURCE_ANCHORS.csv": web_rows_,
        "P8_Y5_R10_904_NONCLAIM_SUMMARY.csv": summary_rows_,
        "P8_Y5_R10_904_FINITE_ALPHA_PROVENANCE_GATE.csv": finite_rows_,
        "P8_Y5_R10_904_R10_BOUND_ANCHOR_ROWS.csv": bound_rows_,
        "P8_Y5_R10_904_R10_CURVE_ACQUISITION_GATE.csv": acquisition_rows_,
        "P8_Y5_R10_904_R10_ALPHA_DRY_ROWS.csv": dry_rows_,
        "P8_Y5_R10_904_BRANCH_DECISION.csv": branch_rows_,
        "P8_Y5_R10_904_CLAIM_GATE.csv": claim_rows_,
        "P8_Y5_R10_904_NEXT_TARGET.csv": next_rows_,
    }
    for filename, rows in initial_outputs.items():
        write_csv(OUT / filename, rows)

    runner_status = run_r10_dry_runner()
    validation_rows_ = validation_rows(
        generated_utc,
        source_rows_,
        web_rows_,
        summary_rows_,
        finite_rows_,
        bound_rows_,
        acquisition_rows_,
        dry_rows_,
        branch_rows_,
        claim_rows_,
        next_rows_,
        runner_status,
    )
    write_csv(OUT / "P8_Y5_BRR545_904_VALIDATION.csv", validation_rows_)

    doc_path = ROOT / "904-Y5-R10-finite-alpha-source-provenance-and-real-bound-curve-gate.md"
    write_markdown(
        doc_path,
        generated_utc,
        summary_rows_,
        source_rows_,
        web_rows_,
        finite_rows_,
        bound_rows_,
        acquisition_rows_,
        dry_rows_,
        branch_rows_,
        claim_rows_,
        next_rows_,
        validation_rows_,
    )

    failed = [row for row in validation_rows_ if row["result"] != "pass"]
    print(f"wrote {doc_path}")
    print(f"wrote {OUT / 'P8_Y5_BRR545_904_VALIDATION.csv'}")
    print(f"status={STATUS}")
    if failed:
        print("failed_validation=" + ",".join(row["check_id"] for row in failed))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
