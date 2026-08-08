from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
CHECKPOINT_ID = "2192"

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BRANCH_WEP = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
SOURCE_WEIGHT_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "2192-Y5-R2FR-first-q_loc-response-operator-or-component-row-fill.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2192_SOURCE_REGISTER.csv",
    "r10_response_operator": OUT / "P8_Y5_PARENT_QLOC_2192_R10_RESPONSE_OPERATOR_ROW.csv",
    "r10_component_input": OUT / "P8_Y5_PARENT_QLOC_2192_R10_COMPONENT_INPUT_ROW.csv",
    "bound_provenance": OUT / "P8_Y5_PARENT_QLOC_2192_BOUND_CURVE_PROVENANCE_AUDIT.csv",
    "dry_run": OUT / "P8_Y5_PARENT_QLOC_2192_DRY_RUN_RESULTS.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_2192_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2192_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2192_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2192_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2192_VALIDATION.csv",
}

BRANCH_COPIES = {
    "queue": QUEUE / "JR2192_FIRST_QLOC_R10_RESPONSE_ROW_NONCLAIM.csv",
    "branch_wep": BRANCH_WEP / "P8_Y5_PARENT_QLOC_2192_R10_COMPONENT_NONCLAIM.csv",
    "source_weight": SOURCE_WEIGHT_DOCS / "PARENT_QLOC_R10_RESPONSE_2192_NONCLAIM.csv",
}


def timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base_row(**kwargs: Any) -> dict[str, Any]:
    row: dict[str, Any] = {
        "timestamp_utc": timestamp(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
        "claim_allowed": False,
    }
    row.update(kwargs)
    return row


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def csv_rows_parse(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open("r", newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        return True, len(rows), "OK"
    except Exception as exc:
        return False, 0, f"{type(exc).__name__}: {exc}"


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join(["---"] * len(columns)) + " |"
    body: list[str] = []
    for row in rows:
        values = []
        for column in columns:
            values.append(str(row.get(column, "")).replace("\n", " ").replace("|", "\\|"))
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, sep, *body])


def remove_pycache() -> None:
    cache = ROOT / "scripts" / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)


def truthy(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "pass"}


def formalization_has_2192_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2192-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2192*",
        "*P8_Y5_BRR545_2192*",
        "*Y5_R2FR_first_q_loc_response_operator_or_component_row_fill_2192*",
        "*JR2192*",
        "*PARENT_QLOC_R10_RESPONSE_2192*",
    )
    return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "2191_doc",
            ROOT / "2191-Y5-R2FR-q_loc-component-projection-runner-and-theorem-zero-certificate.md",
            ["NEXT2191_0_2192", "QCS2191_2_R10", "RUN2191_1_R10", "VAL2191_OVERALL"],
            "2191 explicitly selects the first nonclaim q_loc response/component fill and blocks R10 until kernel, coefficient, curve, and profile inputs exist.",
        ),
        (
            "2191_component_schema",
            OUT / "P8_Y5_PARENT_QLOC_2191_QLOC_COMPONENT_SCHEMA.csv",
            ["QCS2191_2_R10", "lambda_value;q_profile_lambda;c_q_alpha_lambda;range_kernel;bound_curve_id", "MISSING_REAL_BOUND_CURVE"],
            "R10 required fields and missing-input guard for the first component row.",
        ),
        (
            "2191_projection_runner",
            OUT / "P8_Y5_PARENT_QLOC_2191_PROJECTION_RUNNER_SPEC.csv",
            ["RUN2191_1_R10", "alpha_R10_q(lambda)", "MISSING_CQ_ALPHA_LAMBDA"],
            "R10 runner contract says alpha_R10_q(lambda) is blocked until the response coefficient and range kernel are real.",
        ),
        (
            "2191_validation",
            OUT / "P8_Y5_BRR545_2191_VALIDATION.csv",
            ["VAL2191_OVERALL", "PASS", "selects first sourced response/component row next"],
            "Upstream validation confirming 2191 passed while staying nonclaim.",
        ),
        (
            "563_doc",
            ROOT / "563-Y5-R10-real-bound-curve-acquisition-and-alpha-row-smoke-runner.md",
            ["R10_ANCHOR_EOTWASH_2020_ALPHA1_38P6UM", "B563_0_no_full_bound_curve", "B563_1_no_numeric_MTS_alpha"],
            "563 supplies source-backed R10 anchor provenance and the two hard blockers: no full bound curve and no numeric MTS alpha.",
        ),
        (
            "563_blocker_ledger",
            OUT / "P8_Y5_R10_563_BLOCKER_LEDGER.csv",
            ["B563_0_no_full_bound_curve", "B563_1_no_numeric_MTS_alpha", "B563_2_anchor_rows_nonclaim_by_design"],
            "563 blocker ledger keeps R10 scoring closed.",
        ),
        (
            "563_runner_summary",
            OUT / "P8_Y5_R10_563_RUNNER_SUMMARY.csv",
            ["R10_RUNNER_563_LIVE_PLACEHOLDER_RECHECK", "R10_pass_for_claim", "False"],
            "563 runner summary proves live and smoke R10 rows remain invalid for claims.",
        ),
        (
            "563_anchor_bound_file",
            LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_ANCHOR_SMOKE.csv",
            ["R10_ANCHOR_EOTWASH_2020_ALPHA1_38P6UM", "anchor_only_non_curve", "false"],
            "Anchor-only R10 evidence file used for provenance, not scoring.",
        ),
        (
            "live_digitized_placeholder",
            LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_DIGITIZED.csv",
            ["MISSING_DIGITIZED_ALPHA_BOUND", "MISSING_NUMERIC_LAMBDA", "valid_for_claim"],
            "Live digitized-curve file is still a placeholder and must not be promoted.",
        ),
        (
            "q_loc_bound_spec",
            OUT / "P8_QLOC_BOUND_RUNNER_SPEC.csv",
            ["QB516_0_compact_shell_budget", "QB516_3_PPN_metric_tail", "QB516_4_R11_operator"],
            "Older q_loc bound spec distinguishes smoke proxies from true arena projections.",
        ),
        (
            "q_loc_trigger_ledger",
            OUT / "P8_QLOC_BOUND_TRIGGER_LEDGER.csv",
            ["BT517_0_owner_match_fails", "BT517_4_PPN_lock_missing", "score residual components directly"],
            "Trigger ledger explains why q_loc must be scored as residual components if theorem-zero fails.",
        ),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, needles, role in specs:
        text = read_text(path)
        found = [needle for needle in needles if needle in text]
        rows.append(
            base_row(
                source_id=source_id,
                source_path=str(path),
                path_exists=path.exists(),
                required_needles=";".join(needles),
                found_needles=";".join(found),
                needles_found=path.exists() and len(found) == len(needles),
                role=role,
            )
        )
    return rows


def r10_response_operator_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            response_row_id="R10RESP2192_0_first_schema_operator",
            arena="R10_short_range",
            response_operator_id="R_QLOC_TO_ALPHA_R10_TEMPLATE_2192",
            input_quantity="parent-owned q_loc component/profile row in a declared observed frame",
            output_quantity="alpha_R10_q(lambda)",
            operator_form="alpha_R10_q(lambda)=c_q_alpha(lambda)*q_profile(lambda)",
            q_loc_definition="q_loc^nu=P_loc(nabla^nu Gamma_eff - nabla_mu K_hat^{mu nu})",
            input_units="MISSING_QLOC_UNITS_PENDING_PARENT_NORMALIZATION",
            output_units="dimensionless_yukawa_alpha",
            lambda_units="m",
            source_path=str(OUT / "P8_Y5_PARENT_QLOC_2191_QLOC_COMPONENT_SCHEMA.csv"),
            supporting_sources=";".join(
                [
                    str(OUT / "P8_Y5_PARENT_QLOC_2191_PROJECTION_RUNNER_SPEC.csv"),
                    str(ROOT / "563-Y5-R10-real-bound-curve-acquisition-and-alpha-row-smoke-runner.md"),
                    str(OUT / "P8_Y5_R10_563_BLOCKER_LEDGER.csv"),
                ]
            ),
            missing_inputs="MISSING_CQ_ALPHA_LAMBDA;MISSING_Q_PROFILE_LAMBDA;MISSING_RANGE_KERNEL;MISSING_REAL_BOUND_CURVE;MISSING_QLOC_UNITS",
            theorem_zero_status="false_from_2191_certificate",
            row_status="source_backed_schema_nonclaim_not_scoreable",
            score_ready=False,
            validation_note="This is the first concrete R10 response-operator row, but it contains no invented coefficient and cannot score.",
        )
    ]


def r10_component_input_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            component_row_id="R10COMP2192_0_2020_anchor_lambda_schema_row",
            arena="R10_short_range",
            response_operator_id="R_QLOC_TO_ALPHA_R10_TEMPLATE_2192",
            lambda_value="3.86e-5",
            lambda_units="m",
            lambda_source="EOTWASH_2020_PRL124101101_anchor_alpha_equals_1_range_less_than_38p6_um",
            q_profile_lambda="MISSING_QLOC_PROFILE",
            c_q_alpha_lambda="MISSING_CQ_ALPHA_LAMBDA",
            range_kernel="MISSING_RANGE_KERNEL",
            bound_curve_id="R10_ANCHOR_EOTWASH_2020_ALPHA1_38P6UM",
            bound_curve_status="anchor_only_non_curve_not_valid_for_claim",
            q_units="MISSING_QLOC_UNITS_PENDING_PARENT_NORMALIZATION",
            frame_convention="MISSING_OBSERVED_FRAME",
            component_profile_source="MISSING_REAL_QLOC_COMPONENT_PROFILE_SOURCE",
            source_path=str(LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_ANCHOR_SMOKE.csv"),
            supporting_sources=";".join(
                [
                    str(OUT / "P8_Y5_PARENT_QLOC_2191_QLOC_COMPONENT_SCHEMA.csv"),
                    str(OUT / "P8_Y5_R10_563_RUNNER_SUMMARY.csv"),
                    str(OUT / "P8_Y5_R10_563_BLOCKER_LEDGER.csv"),
                ]
            ),
            missing_inputs="MISSING_QLOC_PROFILE;MISSING_CQ_ALPHA_LAMBDA;MISSING_RANGE_KERNEL;MISSING_REAL_BOUND_CURVE;MISSING_QLOC_UNITS;MISSING_OBSERVED_FRAME",
            row_status="first_source_backed_lambda_schema_row_nonclaim",
            score_ready=False,
            validation_note="Positive lambda and source path are real; every physics coefficient/profile needed for alpha scoring is still absent.",
        )
    ]


def bound_provenance_rows() -> list[dict[str, Any]]:
    anchor_rows = read_csv(LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_ANCHOR_SMOKE.csv")
    live_rows = read_csv(LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_DIGITIZED.csv")

    rows: list[dict[str, Any]] = [
        base_row(
            audit_id="BPA2192_0_live_digitized_placeholder",
            bound_file=str(LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_DIGITIZED.csv"),
            bound_id="live_digitized_file_placeholder",
            lambda_value_status="missing_or_placeholder",
            alpha_bound_status="missing_or_placeholder",
            extraction_status="not_acquired",
            usable_for_component_seed=False,
            usable_for_score=False,
            audit_status="blocked_missing_real_curve",
            detail=f"live_rows={len(live_rows)}; placeholders must remain invalid until digitized/table-sourced curve rows exist",
        )
    ]

    for index, row in enumerate(anchor_rows):
        lambda_value = row.get("lambda_value", "")
        alpha_bound = row.get("alpha_bound", "")
        lambda_positive = False
        alpha_positive = False
        try:
            lambda_positive = float(lambda_value) > 0
            alpha_positive = float(alpha_bound) > 0
        except ValueError:
            pass
        rows.append(
            base_row(
                audit_id=f"BPA2192_{index + 1}_anchor_{row.get('bound_id', 'unknown')}",
                bound_file=str(LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_ANCHOR_SMOKE.csv"),
                bound_id=row.get("bound_id", ""),
                lambda_value=lambda_value,
                lambda_units=row.get("lambda_units", ""),
                alpha_bound=alpha_bound,
                alpha_bound_source=row.get("alpha_bound_source", ""),
                digitization_method=row.get("digitization_method", ""),
                source_file=row.get("source_file", ""),
                lambda_positive=lambda_positive,
                alpha_positive=alpha_positive,
                source_backed=bool(row.get("alpha_bound_source", "")) and bool(row.get("source_file", "")),
                usable_for_component_seed=lambda_positive and alpha_positive,
                usable_for_score=False,
                audit_status="anchor_only_non_curve_valid_for_provenance_not_claim",
                detail="Anchor can seed a nonclaim schema row, but cannot replace a dense conservative alpha(lambda) bound curve.",
            )
        )
    return rows


def dry_run_rows(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    source_ok = all(row["path_exists"] and row["needles_found"] for row in rows_by_name["source_register"])
    response = rows_by_name["r10_response_operator"][0]
    component = rows_by_name["r10_component_input"][0]
    blockers = str(response["missing_inputs"]).split(";") + str(component["missing_inputs"]).split(";")
    component_lambda_ok = False
    try:
        component_lambda_ok = float(component["lambda_value"]) > 0 and component["lambda_units"] == "m"
    except ValueError:
        component_lambda_ok = False

    runner_summary = read_csv(OUT / "P8_Y5_R10_563_RUNNER_SUMMARY.csv")
    r10_claim_false = runner_summary and all(str(row.get("R10_pass_for_claim", "")).lower() == "false" for row in runner_summary)
    valid_mts_zero = runner_summary and all(str(row.get("valid_mts_rows", "")) == "0" for row in runner_summary)
    valid_bound_zero = runner_summary and all(str(row.get("valid_bound_rows", "")) == "0" for row in runner_summary)
    theorem_rows = read_csv(OUT / "P8_Y5_PARENT_QLOC_2191_THEOREM_ZERO_CERTIFICATE.csv")
    theorem_zero_false = theorem_rows and all(str(row.get("passes_now", "")).lower() == "false" for row in theorem_rows)
    scoring_blockers_present = all(
        missing in blockers
        for missing in [
            "MISSING_CQ_ALPHA_LAMBDA",
            "MISSING_QLOC_PROFILE",
            "MISSING_RANGE_KERNEL",
            "MISSING_REAL_BOUND_CURVE",
        ]
    )

    return [
        base_row(
            dryrun_id="DR2192_0_source_paths",
            check="all cited 2192 source paths and needles resolve",
            result="PASS_NONCLAIM" if source_ok else "FAIL",
            detail=f"sources_ok={source_ok}",
        ),
        base_row(
            dryrun_id="DR2192_1_first_component_lambda",
            check="first R10 component seed has positive numeric lambda in metres",
            result="PASS_NONCLAIM" if component_lambda_ok else "FAIL",
            detail=f"lambda_value={component['lambda_value']};lambda_units={component['lambda_units']}",
        ),
        base_row(
            dryrun_id="DR2192_2_scoring_guard",
            check="R10 scoring is refused while coefficient, q profile, kernel and real curve are missing",
            result="BLOCKED_EXPECTED" if scoring_blockers_present else "FAIL_UNEXPECTED_RUNNABLE",
            detail=";".join(sorted(set(blockers))),
        ),
        base_row(
            dryrun_id="DR2192_3_563_runner_still_blocks",
            check="live/smoke R10 comparator state remains blocked from 563",
            result="PASS_NONCLAIM" if r10_claim_false and valid_mts_zero and valid_bound_zero else "FAIL",
            detail=f"R10_pass_false={bool(r10_claim_false)};valid_mts_zero={bool(valid_mts_zero)};valid_bound_zero={bool(valid_bound_zero)}",
        ),
        base_row(
            dryrun_id="DR2192_4_theorem_zero_stays_false",
            check="q_loc theorem-zero certificate is not promoted by a schema row",
            result="PASS_NONCLAIM" if theorem_zero_false else "FAIL_UNEXPECTED_PROMOTION",
            detail=f"theorem_zero_false={bool(theorem_zero_false)}",
        ),
        base_row(
            dryrun_id="DR2192_5_no_score_ready_rows",
            check="no generated row is score-ready or claim-valid",
            result="PASS_NONCLAIM" if all_score_ready_false(rows_by_name) and all_claim_flags_false(rows_by_name) else "FAIL",
            detail="score_ready=false and claim flags=false required across generated rows",
        ),
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "CG2192_0_local_GR",
            "local_GR_reduction_claim",
            "BLOCKED_NONCLAIM",
            "2192 adds a response row only; q_loc theorem-zero remains false, so no local-GR claim follows.",
        ),
        (
            "CG2192_1_R10_score",
            "R10_alpha_bound_score",
            "BLOCKED_NONCLAIM",
            "No score until c_q_alpha(lambda), q_profile(lambda), range kernel, and real bound curve are all numeric and sourced.",
        ),
        (
            "CG2192_2_anchor_use",
            "Eot-Wash_anchor_use",
            "PROVENANCE_ONLY",
            "The 2020 anchor gives a source-backed lambda seed, not a claim-valid alpha(lambda) bound curve.",
        ),
        (
            "CG2192_3_scalar_proxy",
            "scalar_proxy_or_compact_shell_budget",
            "FORBIDDEN_FOR_CLAIM",
            "Older scalar/smoke q_loc budgets cannot be dressed up as R10 or PPN evidence.",
        ),
    ]
    return [base_row(gate_id=gate_id, gate=gate, status=status, implication=implication) for gate_id, gate, status, implication in specs]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "DEC2192_0_gain",
            "FIRST_R10_RESPONSE_ROW_FILLED_NONCLAIM",
            "R10 now has a concrete source-backed operator row plus one positive-lambda schema component row.",
            "selected",
        ),
        (
            "DEC2192_1_limit",
            "NO_R10_SCORE_YET",
            "The row is intentionally blocked by missing c_q_alpha(lambda), q_profile(lambda), range kernel, units/frame, and real curve.",
            "selected",
        ),
        (
            "DEC2192_2_next",
            "BOUND_CURVE_OR_COEFFICIENT_SOURCE_NEXT",
            "The fastest route to testing is now either a real dense R10 bound curve or the first parent-sourced q_loc->alpha coefficient/profile.",
            "selected",
        ),
        (
            "DEC2192_3_parallel_theory",
            "THEOREM_ZERO_ROUTE_REMAINS_OPEN",
            "A future parent action can still close q_loc=0, but 2192 does not promote that route.",
            "held_parallel",
        ),
    ]
    return [base_row(decision_id=decision_id, decision=decision, rationale=rationale, selection_status=status) for decision_id, decision, rationale, status in specs]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            route_id="NEXT2192_0_2193",
            selection_status="selected",
            target_file="2193-Y5-R2FR-q_loc-R10-bound-curve-or-coefficient-source-acquisition.md",
            target_script="scripts/Y5_R2FR_q_loc_R10_bound_curve_or_coefficient_source_acquisition_2193.py",
            objective="acquire one of the two missing real inputs for the R10 projection: either a dense source-backed alpha(lambda) bound curve or the first parent-sourced c_q_alpha/q_profile row",
            success_condition="one missing input is replaced by real sourced numeric data while the final R10 claim remains blocked unless every required input is valid",
            do_not_do="do not use anchor-only rows as a bound curve; do not invent parent coefficients; do not claim local-GR, fifth-force, Newton, PPN, or R10 pass",
        ),
        base_row(
            route_id="NEXT2192_1_2193b",
            selection_status="held_parallel",
            target_file="2193b-Y5-R2FR-parent-GK-action-owner-first-theorem-clause.md",
            target_script="scripts/Y5_R2FR_parent_GK_action_owner_first_theorem_clause_2193b.py",
            objective="try to source-sign the parent Gamma/Khat action-owner or metric-response clause so theorem-zero can advance without residual scoring",
            success_condition="one theorem-zero certificate clause becomes genuinely parent-signed or is explicitly demoted",
            do_not_do="do not use partial action ownership as a q_loc zero proof",
        ),
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    copies = [
        ("queue", OUTPUTS["r10_response_operator"], BRANCH_COPIES["queue"]),
        ("branch_wep", OUTPUTS["r10_component_input"], BRANCH_COPIES["branch_wep"]),
        ("source_weight", OUTPUTS["r10_response_operator"], BRANCH_COPIES["source_weight"]),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source, target in copies:
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        rows.append(base_row(copy_id=copy_id, source_path=str(source), target_path=str(target), copied=target.exists()))
    return rows


def all_claim_flags_false(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    for rows in rows_by_name.values():
        for row in rows:
            if truthy(row.get("claim_allowed", False)):
                return False
            if truthy(row.get("valid_for_claim", False)):
                return False
    return True


def all_score_ready_false(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    for rows in rows_by_name.values():
        for row in rows:
            if "score_ready" in row and truthy(row["score_ready"]):
                return False
            if "usable_for_score" in row and truthy(row["usable_for_score"]):
                return False
    return True


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    validations: list[dict[str, Any]] = []

    sources = rows_by_name["source_register"]
    validations.append(
        base_row(
            validation_id="VAL2192_00_sources_exist",
            status="PASS" if all(row["path_exists"] for row in sources) else "FAIL",
            detail=f"{sum(bool(row['path_exists']) for row in sources)}/{len(sources)} sources exist",
        )
    )
    validations.append(
        base_row(
            validation_id="VAL2192_01_needles_found",
            status="PASS" if all(row["needles_found"] for row in sources) else "FAIL",
            detail=f"{sum(bool(row['needles_found']) for row in sources)}/{len(sources)} source needle sets found",
        )
    )

    response_rows = rows_by_name["r10_response_operator"]
    response = response_rows[0]
    response_path = Path(response["source_path"])
    response_pass = (
        len(response_rows) == 1
        and response["arena"] == "R10_short_range"
        and response["output_units"] == "dimensionless_yukawa_alpha"
        and "c_q_alpha(lambda)*q_profile(lambda)" in response["operator_form"]
        and response_path.exists()
        and not truthy(response["score_ready"])
    )
    validations.append(
        base_row(
            validation_id="VAL2192_02_response_operator_row",
            status="PASS" if response_pass else "FAIL",
            detail=f"response_rows={len(response_rows)};source_exists={response_path.exists()};score_ready={response['score_ready']}",
        )
    )

    component_rows = rows_by_name["r10_component_input"]
    component = component_rows[0]
    try:
        lambda_positive = float(component["lambda_value"]) > 0
    except ValueError:
        lambda_positive = False
    component_path = Path(component["source_path"])
    required_missing = {
        "MISSING_QLOC_PROFILE",
        "MISSING_CQ_ALPHA_LAMBDA",
        "MISSING_RANGE_KERNEL",
        "MISSING_REAL_BOUND_CURVE",
    }
    component_missing = set(str(component["missing_inputs"]).split(";"))
    component_pass = (
        len(component_rows) == 1
        and lambda_positive
        and component["lambda_units"] == "m"
        and component_path.exists()
        and required_missing.issubset(component_missing)
        and not truthy(component["score_ready"])
    )
    validations.append(
        base_row(
            validation_id="VAL2192_03_component_row_nonclaim",
            status="PASS" if component_pass else "FAIL",
            detail=f"component_rows={len(component_rows)};lambda_positive={lambda_positive};source_exists={component_path.exists()};missing={';'.join(sorted(component_missing))}",
        )
    )

    bound_rows = rows_by_name["bound_provenance"]
    anchor_rows = [row for row in bound_rows if "anchor_" in row["audit_id"]]
    anchors_numeric = all(truthy(row.get("lambda_positive", False)) and truthy(row.get("alpha_positive", False)) for row in anchor_rows)
    no_score_curve = all(not truthy(row.get("usable_for_score", False)) for row in bound_rows)
    live_placeholder_blocked = any(row["audit_id"] == "BPA2192_0_live_digitized_placeholder" and row["audit_status"] == "blocked_missing_real_curve" for row in bound_rows)
    validations.append(
        base_row(
            validation_id="VAL2192_04_bound_provenance_nonclaim",
            status="PASS" if anchor_rows and anchors_numeric and no_score_curve and live_placeholder_blocked else "FAIL",
            detail=f"anchor_rows={len(anchor_rows)};anchors_numeric={anchors_numeric};no_score_curve={no_score_curve};live_placeholder_blocked={live_placeholder_blocked}",
        )
    )

    dry_results = {row["result"] for row in rows_by_name["dry_run"]}
    validations.append(
        base_row(
            validation_id="VAL2192_05_dryrun_blocks_scoring",
            status="PASS" if "BLOCKED_EXPECTED" in dry_results and "FAIL_UNEXPECTED_RUNNABLE" not in dry_results and "FAIL_UNEXPECTED_PROMOTION" not in dry_results else "FAIL",
            detail="dry-run refuses scoring and theorem-zero promotion",
        )
    )

    gate_statuses = {row["status"] for row in rows_by_name["claim_gate"]}
    validations.append(
        base_row(
            validation_id="VAL2192_06_claim_gate",
            status="PASS" if {"BLOCKED_NONCLAIM", "PROVENANCE_ONLY", "FORBIDDEN_FOR_CLAIM"}.issubset(gate_statuses) else "FAIL",
            detail="claim gate blocks local-GR/R10 and limits anchors to provenance",
        )
    )

    decisions = {row["decision"] for row in rows_by_name["decision"] if row["selection_status"] == "selected"}
    validations.append(
        base_row(
            validation_id="VAL2192_07_decision",
            status="PASS" if "BOUND_CURVE_OR_COEFFICIENT_SOURCE_NEXT" in decisions else "FAIL",
            detail="decision selects real bound curve or coefficient/profile source next",
        )
    )

    routes = {row["route_id"] for row in rows_by_name["next_target"] if row["selection_status"] == "selected"}
    validations.append(
        base_row(
            validation_id="VAL2192_08_next_target",
            status="PASS" if "NEXT2192_0_2193" in routes else "FAIL",
            detail="2193 acquisition target selected",
        )
    )

    validations.append(
        base_row(
            validation_id="VAL2192_09_claim_flags_false",
            status="PASS" if all_claim_flags_false(rows_by_name) else "FAIL",
            detail="all generated rows keep valid_for_claim=false and claim_allowed=false",
        )
    )
    validations.append(
        base_row(
            validation_id="VAL2192_10_score_flags_false",
            status="PASS" if all_score_ready_false(rows_by_name) else "FAIL",
            detail="no generated row is score-ready or usable_for_score",
        )
    )

    parse_details: list[str] = []
    parse_pass = True
    for name, path in OUTPUTS.items():
        if name == "validation":
            continue
        ok, count, detail = csv_rows_parse(path)
        parse_pass = parse_pass and ok and count > 0
        parse_details.append(f"{path.name}:{count if ok else detail}")
    validations.append(
        base_row(
            validation_id="VAL2192_11_csv_parse",
            status="PASS" if parse_pass else "FAIL",
            detail="; ".join(parse_details),
        )
    )

    copies = rows_by_name["branch_copies"]
    validations.append(
        base_row(
            validation_id="VAL2192_12_branch_copies",
            status="PASS" if copies and all(row["copied"] for row in copies) else "FAIL",
            detail=";".join(str(row["target_path"]) for row in copies),
        )
    )

    validations.append(
        base_row(
            validation_id="VAL2192_13_formalization_clean",
            status="PASS" if not formalization_has_2192_artifacts() else "FAIL",
            detail="formalization-workbench has no 2192 artifacts",
        )
    )

    remove_pycache()
    validations.append(
        base_row(
            validation_id="VAL2192_14_pycache_absent",
            status="PASS" if not (ROOT / "scripts" / "__pycache__").exists() else "FAIL",
            detail=str(ROOT / "scripts" / "__pycache__"),
        )
    )

    overall = "PASS" if all(row["status"] == "PASS" for row in validations) else "FAIL"
    validations.append(
        base_row(
            validation_id="VAL2192_OVERALL",
            status=overall,
            detail="2192 fills the first source-backed q_loc->R10 response/component row as nonclaim schema plumbing and keeps all scoring gates closed",
        )
    )
    return validations


def render_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> str:
    sections = [
        "# 2192 - Y5/R2FR First q_loc Response Operator Or Component Row Fill",
        "",
        "## Current Verdict",
        "",
        "2192 makes the first concrete `q_loc -> R10` row, but it is **not** a physics score.",
        "",
        "The useful move is narrow and honest: R10 now has a source-backed response-operator schema and one positive-lambda component seed from the 2020 Eot-Wash anchor. The row still refuses claims because `c_q_alpha(lambda)`, `q_profile(lambda)`, the finite-range kernel, the observed-frame q_loc units/profile, and a real dense bound curve are all missing.",
        "",
        "So this is a bridge from derivation to testing, not a pass. No local-GR, Newton, PPN, fifth-force, or R10 claim is allowed from this checkpoint.",
        "",
        "## Source Register",
        "",
        md_table(rows_by_name["source_register"], ["source_id", "source_path", "path_exists", "needles_found", "role", "valid_for_claim"]),
        "",
        "## R10 Response Operator Row",
        "",
        md_table(rows_by_name["r10_response_operator"], ["response_row_id", "arena", "response_operator_id", "output_quantity", "operator_form", "input_units", "output_units", "source_path", "missing_inputs", "row_status", "score_ready", "valid_for_claim"]),
        "",
        "## R10 Component Input Row",
        "",
        md_table(rows_by_name["r10_component_input"], ["component_row_id", "arena", "lambda_value", "lambda_units", "q_profile_lambda", "c_q_alpha_lambda", "range_kernel", "bound_curve_id", "bound_curve_status", "source_path", "missing_inputs", "score_ready", "valid_for_claim"]),
        "",
        "## Bound Curve Provenance Audit",
        "",
        md_table(rows_by_name["bound_provenance"], ["audit_id", "bound_file", "bound_id", "lambda_value", "lambda_units", "alpha_bound", "digitization_method", "usable_for_component_seed", "usable_for_score", "audit_status", "valid_for_claim"]),
        "",
        "## Dry-Run Results",
        "",
        md_table(rows_by_name["dry_run"], ["dryrun_id", "check", "result", "detail", "valid_for_claim", "claim_allowed"]),
        "",
        "## Claim Gate",
        "",
        md_table(rows_by_name["claim_gate"], ["gate_id", "gate", "status", "implication", "valid_for_claim"]),
        "",
        "## Decision Ledger",
        "",
        md_table(rows_by_name["decision"], ["decision_id", "decision", "rationale", "selection_status", "valid_for_claim"]),
        "",
        "## Next Target",
        "",
        md_table(rows_by_name["next_target"], ["route_id", "selection_status", "target_file", "target_script", "objective", "success_condition", "do_not_do", "valid_for_claim"]),
        "",
        "## Branch Copies",
        "",
        md_table(rows_by_name["branch_copies"], ["copy_id", "source_path", "target_path", "copied", "valid_for_claim"]),
        "",
        "## Validation",
        "",
        md_table(rows_by_name["validation"], ["validation_id", "status", "detail", "valid_for_claim", "claim_allowed"]),
        "",
        "## Interpretation",
        "",
        "This is a small but important step: the R10 arena now has a real row shape tied to actual source provenance instead of a floating placeholder. The harsh bit is that it still cannot test MTS because the two sides of the comparison are not both real yet.",
        "",
        "Best next attack: pick one missing side and replace it with real sourced material. Either digitize/table-source the 2020 R10 alpha(lambda) curve, or derive/source the first parent-owned `c_q_alpha(lambda)` and `q_profile(lambda)` row. Anything else would be shadow-boxing.",
        "",
    ]
    return "\n".join(sections)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rows_by_name: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register_rows(),
        "r10_response_operator": r10_response_operator_rows(),
        "r10_component_input": r10_component_input_rows(),
        "bound_provenance": bound_provenance_rows(),
        "claim_gate": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
    }

    rows_by_name["dry_run"] = dry_run_rows(rows_by_name)

    for name, rows in rows_by_name.items():
        write_csv(OUTPUTS[name], rows)

    rows_by_name["branch_copies"] = branch_copy_rows()
    write_csv(OUTPUTS["branch_copies"], rows_by_name["branch_copies"])

    rows_by_name["validation"] = validation_rows(rows_by_name)
    write_csv(OUTPUTS["validation"], rows_by_name["validation"])

    DOC.write_text(render_doc(rows_by_name), encoding="utf-8")
    remove_pycache()


if __name__ == "__main__":
    main()
