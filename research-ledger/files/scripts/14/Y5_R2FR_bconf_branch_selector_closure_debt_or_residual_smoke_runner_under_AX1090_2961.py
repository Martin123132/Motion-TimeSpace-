from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_START_UTC = datetime.now(timezone.utc)

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
PARENT_ACTION = ROOT / "source-intake" / "parent-action"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"

CHECKPOINT = "2961"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
RUN_UTC = SCRIPT_START_UTC.isoformat()

DOC = ROOT / "2961-Y5-R2FR-bconf-branch-selector-closure-debt-or-residual-smoke-runner-under-AX1090.md"

SRC_2960_DOC = ROOT / "2960-Y5-R2FR-bconf-tau-projection-map-or-single-frame-closure-declaration-under-AX1090.md"
SRC_2960_NEXT = RESIDUALS / "P8_Y5_R2FR_2960_NEXT_TARGET.csv"
SRC_2960_TAU = RESIDUALS / "P8_Y5_R2FR_2960_BCONF_TAU_PROJECTION_GATE.csv"
SRC_2960_CONDITIONAL = RESIDUALS / "P8_Y5_R2FR_2960_CONDITIONAL_SCALAR_TENSOR_COUNTERMODEL_MAP.csv"
SRC_2960_CLOSURE = RESIDUALS / "P8_Y5_R2FR_2960_SINGLE_FRAME_CLOSURE_DECLARATION_NONCLAIM.csv"
SRC_2960_BOUNDS = RESIDUALS / "P8_Y5_R2FR_2960_BCONF_BOUND_ROWS_NONCLAIM.csv"
SRC_2959_FRAME = RESIDUALS / "P8_Y5_R2FR_2959_SINGLE_OBSERVED_FRAME_PARENT_ACTION_GATE.csv"
SRC_2959_BCONF = RESIDUALS / "P8_Y5_R2FR_2959_BCONF_BOUND_INTAKE_NONCLAIM.csv"
SRC_GLOBAL_COUPLING = RESIDUALS / "P8_global_coupling_superselection_CONTRACT.csv"
SRC_LOCAL_TEMPLATE = RESIDUALS / "MTS_local_residual_predictions_TEMPLATE.csv"
SRC_LOCAL_BOUNDS = LOCAL_BOUNDS / "local_bound_claims.csv"
SRC_R10_CURVE = LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2961_SOURCE_REGISTER.csv",
    "selector": RESIDUALS / "P8_Y5_R2FR_2961_BCONF_BRANCH_SELECTOR.csv",
    "closure_branch": RESIDUALS / "P8_Y5_R2FR_2961_CLOSURE_DEBT_BRANCH.csv",
    "residual_branch": RESIDUALS / "P8_Y5_R2FR_2961_RESIDUAL_BRANCH_NONCLAIM.csv",
    "smoke": RESIDUALS / "P8_Y5_R2FR_2961_SMOKE_RUNNER_STATUS.csv",
    "claims": RESIDUALS / "P8_Y5_R2FR_2961_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2961_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2961_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2961_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2961_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "selector_copy": PARENT_ACTION / "bconf_branch_selector_2961_NONCLAIM.csv",
    "residual_copy": LOCAL_BOUNDS / "bconf_residual_smoke_rows_2961_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR2961_XHAT_SOURCE_CURRENT_OR_BCONF_SMOKE_NEXT_NONCLAIM.csv",
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
    specs = [
        ("SRC2961_00_2960_doc", SRC_2960_DOC, "NEXT2960_0_2961;Validation overall: `True`", "2960 handoff"),
        ("SRC2961_01_2960_next", SRC_2960_NEXT, "NEXT2960_0_2961", "machine-readable 2961 target"),
        ("SRC2961_02_2960_tau", SRC_2960_TAU, "TAU2960_0_canonical_state;TAU2960_5_verdict", "b_conf tau gate"),
        ("SRC2961_03_2960_conditional", SRC_2960_CONDITIONAL, "CMAP2960_0_universal_scalar_tensor;CMAP2960_4_source_template", "conditional countermodel maps"),
        ("SRC2961_04_2960_closure", SRC_2960_CLOSURE, "CLOSE2960_0_statement;CLOSE2960_3_verdict", "single-frame closure declaration"),
        ("SRC2961_05_2960_bounds", SRC_2960_BOUNDS, "BROW2960_0_b_conf;BROW2960_4_source", "b_conf bound rows"),
        ("SRC2961_06_2959_frame", SRC_2959_FRAME, "SFRAME2959_0_target_clause;SFRAME2959_7_verdict", "single-frame gate"),
        ("SRC2961_07_2959_bconf", SRC_2959_BCONF, "BCI2959_1_tau_R10_conf;BCI2959_5_B_conf_envelope", "b_conf intake rows"),
        ("SRC2961_08_global_coupling", SRC_GLOBAL_COUPLING, "GS4_no_range_radial_time_dependence;GS7_scalar_branch_fallback", "global/source-current contract"),
        ("SRC2961_09_local_template", SRC_LOCAL_TEMPLATE, "R3_gamma;R10_fifth_force", "local residual template"),
        ("SRC2961_10_local_bounds", SRC_LOCAL_BOUNDS, "R1_WEP_source_charge;R2_clock_redshift;R3_gamma", "local bound anchors"),
        ("SRC2961_11_r10_curve", SRC_R10_CURVE, "R10_VECTOR_2020_REVIEW_0000;review_candidate_only", "R10 nonclaim bound curve"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, source_path, anchors, role in specs:
        found, missing = anchors_present(source_path, anchors)
        rows.append(
            add_common(
                {
                    "source_id": source_id,
                    "source_type": "local_file",
                    "source_path": str(source_path),
                    "anchors": anchors,
                    "role": role,
                    "path_exists": source_path.exists(),
                    "anchors_found": found,
                    "missing_anchors": missing,
                }
            )
        )
    return rows


def selector_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "SEL2961_0_closure_debt",
            "BCONF_CLOSURE_DEBT_BRANCH",
            "b_conf=0 by explicit single-observed-frame closure",
            True,
            False,
            False,
            "use only as an internal closure-debt branch; no theorem-zero/local-GR credit",
        ),
        (
            "SEL2961_1_residual",
            "BCONF_FINITE_RESIDUAL_BRANCH",
            "b_conf finite until canonical Xhat/source-current/tau maps are sourced",
            False,
            False,
            False,
            "use as falsifiable residual branch; no score until tau maps are real",
        ),
        (
            "SEL2961_2_dual_track_policy",
            "DUAL_TRACK_PRIVATE_POLICY",
            "carry both branches side-by-side in private audits",
            True,
            False,
            False,
            "do not choose the prettier branch as evidence; compare only after both are labelled",
        ),
        (
            "SEL2961_3_verdict",
            "NO_BRANCH_IS_DERIVED_LOCAL_GR",
            "the fork is organized, not solved",
            True,
            False,
            False,
            "local GR/Newton reduction remains unclaimed",
        ),
    ]
    return [
        add_common(
            {
                "selector_id": selector_id,
                "selector_branch": branch,
                "rule": rule,
                "branch_allowed_for_private_work": allowed,
                "theorem_zero_credit": theorem_credit,
                "local_GR_claim": local_gr,
                "policy": policy,
            }
        )
        for selector_id, branch, rule, allowed, theorem_credit, local_gr, policy in rows
    ]


def closure_branch_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "CDB2961_0_rule",
            "single-observed-frame closure",
            "ordinary matter couples only to e_obs(q) and fixed representation data",
            "b_conf=0_BY_CLOSURE",
            "closure_debt",
        ),
        (
            "CDB2961_1_credit_limit",
            "theorem credit",
            "closure kills b_conf only by branch grammar, not by parent derivation",
            "NO_THEOREM_ZERO_CREDIT",
            "credit_block",
        ),
        (
            "CDB2961_2_scope_limit",
            "scope",
            "closure only addresses hidden conformal b_conf; b_dis, b_marker, b_alpha and source-current rows remain independent unless separately closed",
            "PARTIAL_CHANNEL_ONLY",
            "scope_guard",
        ),
        (
            "CDB2961_3_claim_limit",
            "claims",
            "closure branch cannot be promoted to local GR/Newton/R10/PPN evidence without parent derivation or independent score rows",
            "NO_LOCAL_GR_CLAIM",
            "claim_guard",
        ),
    ]
    return [
        add_common(
            {
                "row_id": row_id,
                "object": obj,
                "statement": statement,
                "branch_value": value,
                "role": role,
                "closure_debt": True,
                "theorem_zero_credit": False,
                "accepted_for_scoring": False,
            }
        )
        for row_id, obj, statement, value, role in rows
    ]


def residual_branch_rows() -> list[dict[str, Any]]:
    rows = [
        ("RES2961_0_b_conf", "b_conf", "dimensionless", "finite hidden conformal-frame coefficient", "MISSING_PRIOR_OR_FIT", "must source theorem-zero, prior, or fit value"),
        ("RES2961_1_tau_R10_conf", "tau_R10_conf", "dimensionless_projection", "maps b_conf into alpha_R10(lambda)", "MISSING_XHAT_SOURCE_TEST_LAMBDA", "needs canonical Xhat, source/test charge and lambda_X"),
        ("RES2961_2_tau_PPN_gamma_conf", "tau_PPN_gamma_conf", "dimensionless_projection", "maps b_conf into gamma_minus_1", "MISSING_FRAME_REGIME_AND_PPN_MAP", "needs scalar-tensor regime or MTS weak-field map"),
        ("RES2961_3_tau_clock_conf", "tau_clock_conf", "dimensionless_projection", "maps b_conf into clock/redshift observable", "MISSING_LOCAL_PROFILE_AND_CLOCK_FRAME", "needs local Xhat profile and frame/readout order"),
        ("RES2961_4_tau_source_conf", "tau_source_conf", "dimensionless_projection", "maps b_conf into source-current/measured-GM response", "MISSING_SOURCE_CURRENT_OWNER", "needs source-normalization theorem or residual coefficient"),
        ("RES2961_5_alpha_R10_conf", "alpha_R10_conf(lambda)", "dimensionless", "C_R10(tau_source_conf b_conf)(tau_test_conf b_conf)F_range(lambda)", "MISSING_PRODUCT_INPUTS", "runner must reject placeholders"),
        ("RES2961_6_B_conf_envelope", "B_conf", "dimensionless", "min bound from R10/PPN/clock/source projections", "MISSING_TAU_VALUES", "not score-ready"),
    ]
    source_path = ";".join(str(path) for path in [SRC_2960_BOUNDS, SRC_2960_TAU, SRC_LOCAL_BOUNDS, SRC_R10_CURVE])
    return [
        add_common(
            {
                "row_id": row_id,
                "symbol": symbol,
                "units": units,
                "definition_or_formula": formula,
                "numeric_or_theorem_value": value,
                "next_needed": needed,
                "source_path": source_path,
                "source_path_exists": all(Path(path).exists() for path in source_path.split(";")),
                "accepted_for_scoring": False,
                "no_cancellation_policy": True,
            }
        )
        for row_id, symbol, units, formula, value, needed in rows
    ]


def smoke_rows(selector: list[dict[str, Any]], closure: list[dict[str, Any]], residual: list[dict[str, Any]]) -> list[dict[str, Any]]:
    closure_branch_count = sum(1 for row in selector if row["selector_branch"] == "BCONF_CLOSURE_DEBT_BRANCH")
    residual_branch_count = sum(1 for row in selector if row["selector_branch"] == "BCONF_FINITE_RESIDUAL_BRANCH")
    residual_valid_rows = sum(1 for row in residual if row["accepted_for_scoring"] is True and row["valid_for_claim"] is True)
    closure_theorem_credit = any(row["theorem_zero_credit"] is True for row in closure)
    rows = [
        (
            "SMOKE2961_0_schema",
            "branch selector schema",
            closure_branch_count,
            residual_branch_count,
            0,
            "PASS_SCHEMA_ONLY",
            "two branches are explicit",
        ),
        (
            "SMOKE2961_1_closure_branch",
            "closure-debt branch",
            1,
            0,
            0,
            "BLOCKED_FOR_CLAIM",
            "closure theorem credit is false",
        ),
        (
            "SMOKE2961_2_residual_branch",
            "finite residual branch",
            0,
            1,
            residual_valid_rows,
            "BLOCKED_FOR_SCORE",
            "valid residual score rows remain zero",
        ),
        (
            "SMOKE2961_3_expected",
            "claim outcome",
            closure_branch_count,
            residual_branch_count,
            residual_valid_rows,
            "CLAIM_FALSE_EXPECTED",
            f"closure_theorem_credit={closure_theorem_credit}; residual_valid_rows={residual_valid_rows}",
        ),
    ]
    return [
        add_common(
            {
                "smoke_id": smoke_id,
                "object": obj,
                "closure_branch_rows": closure_count,
                "residual_branch_rows": residual_count,
                "valid_mts_rows": valid_rows,
                "smoke_status": status,
                "notes": notes,
                "claim_allowed": False,
                "valid_for_claim": False,
            }
        )
        for smoke_id, obj, closure_count, residual_count, valid_rows, status, notes in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("CG2961_0_selector", "two-branch selector exists", True, "PRIVATE_ORGANIZATION_ONLY"),
        ("CG2961_1_closure_credit", "closure branch gives theorem-zero credit", False, "CLOSURE_DEBT_TRUE"),
        ("CG2961_2_residual_score", "finite b_conf residual branch is score-ready", False, "VALID_MTS_ROWS_ZERO"),
        ("CG2961_3_R10_PPN_clock", "R10/PPN/clock comparison allowed", False, "TAU_MAPS_PLACEHOLDER"),
        ("CG2961_4_local_GR", "local GR/Newton reduction allowed", False, "NO_LOCAL_GR_CLAIM"),
        ("CG2961_5_public", "public claim allowed", False, "PRIVATE_NONCLAIM_CHECKPOINT"),
    ]
    return [
        add_common(
            {
                "claim_gate_id": gate_id,
                "claim": claim,
                "condition_passed": passed,
                "status": status,
                "claim_allowed": False,
            }
        )
        for gate_id, claim, passed, status in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "DEC2961_0_selector",
            "b_conf route is now an explicit fork",
            "the previous loop is resolved into closure-debt versus finite-residual branches",
            "carry both branches in private work",
        ),
        (
            "DEC2961_1_closure",
            "closure branch is usable but not evidential",
            "b_conf=0 can be imposed by single-frame grammar, but closure_debt prevents local-GR claim",
            "do not present as derivation",
        ),
        (
            "DEC2961_2_residual",
            "residual branch is testable but not runnable yet",
            "b_conf and tau maps have explicit rows, but no canonical normalization/source-current owner",
            "derive Xhat/source-current owner next",
        ),
        (
            "DEC2961_3_next",
            "next target should source the finite residual branch",
            "this avoids repeating the same single-frame proof loop and moves toward empirical robustness",
            "build 2962 canonical Xhat/source-current normalization or b_conf residual prior",
        ),
    ]
    return [
        add_common(
            {
                "decision_id": decision_id,
                "decision": decision,
                "because": because,
                "next_action": action,
            }
        )
        for decision_id, decision, because, action in rows
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "next_id": "NEXT2961_0_2962",
                "priority": "selected_primary",
                "next_doc": "2962-Y5-R2FR-canonical-Xhat-source-current-normalization-or-bconf-residual-prior-under-AX1090.md",
                "next_script": "scripts/Y5_R2FR_canonical_Xhat_source_current_normalization_or_bconf_residual_prior_under_AX1090_2962.py",
                "objective": "Try to derive the canonical Xhat normalization and source/test current owner needed for the finite b_conf residual branch. If this fails, fill nonclaim b_conf prior/projection intake rows for later smoke tests.",
                "include": "Xhat normalization;lambda_X;source/test charges;tau_R10_conf;tau_PPN_gamma_conf;tau_clock_conf;tau_source_conf;b_conf prior;no-cancellation policy;claim gates",
                "exclude": "derive single-frame theorem again;b_marker full taxonomy;quotient/vertical no-pole rerun;beta prediction;direct lambda closure;alpha(lambda) scoring;I_X scoring;local-GR claim;public claim;formalization-workbench edits;GitHub action",
            }
        )
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    copies = [
        ("selector_copy", OUTPUTS["selector"], BRANCH_OUTPUTS["selector_copy"]),
        ("residual_copy", OUTPUTS["residual_branch"], BRANCH_OUTPUTS["residual_copy"]),
        ("next_copy", OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"]),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source, target in copies:
        shutil.copyfile(source, target)
        rows.append(
            add_common(
                {
                    "copy_id": copy_id,
                    "source_path": str(source),
                    "copy_path": str(target),
                    "source_exists": source.exists(),
                    "copy_exists": target.exists(),
                }
            )
        )
    return rows


def validation_rows(all_rows: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    source_rows = all_rows["sources"]
    generated_paths = list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC]
    csv_paths = list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values())
    checks = [
        ("VAL2961_0_sources_exist", all(row["path_exists"] for row in source_rows), "all cited local source paths exist", True),
        ("VAL2961_1_anchors_found", all(row["anchors_found"] for row in source_rows), "all cited source anchors found", True),
        ("VAL2961_2_two_branches", sum(1 for row in all_rows["selector"] if row["selector_branch"] in {"BCONF_CLOSURE_DEBT_BRANCH", "BCONF_FINITE_RESIDUAL_BRANCH"}) == 2, "closure and residual branches both exist", True),
        ("VAL2961_3_closure_debt", all(row["closure_debt"] is True and row["theorem_zero_credit"] is False for row in all_rows["closure_branch"]), "closure branch carries debt and no theorem credit", True),
        ("VAL2961_4_residual_nonclaim", all(row["accepted_for_scoring"] is False and row["valid_for_claim"] is False for row in all_rows["residual_branch"]), "residual branch rows remain nonclaim", True),
        ("VAL2961_5_residual_paths", all(row["source_path_exists"] is True for row in all_rows["residual_branch"]), "residual rows cite existing paths", True),
        ("VAL2961_6_smoke_blocks_claim", all(row["claim_allowed"] is False and row["valid_for_claim"] is False for row in all_rows["smoke"]), "smoke runner blocks claim", True),
        ("VAL2961_7_claims_blocked", all(row["claim_allowed"] is False for row in all_rows["claims"]) and any(row["claim_gate_id"] == "CG2961_0_selector" and row["condition_passed"] is True for row in all_rows["claims"]), "selector exists but all claims remain blocked", True),
        ("VAL2961_8_next_target_written", any(row["next_id"] == "NEXT2961_0_2962" for row in all_rows["next"]), "2962 next target selected", True),
        ("VAL2961_9_branches_exist", all(Path(row["copy_path"]).exists() for row in all_rows["branches"]), "branch copy files exist", True),
        ("VAL2961_10_csvs_parse", all(csv_parses(path) for path in csv_paths), "all generated CSV files parse", True),
        ("VAL2961_11_outputs_under_post_checkpoint", all(is_under(path, ROOT) for path in generated_paths), "all generated outputs are under post-checkpoint-work", True),
        ("VAL2961_12_formalization_clean", not any(is_under(path, FORMALIZATION) for path in generated_paths), "no 2961 outputs were written to formalization-workbench", True),
        ("VAL2961_13_doc_written", DOC.exists(), "2961 markdown checkpoint exists", True),
    ]
    overall = all(passed == required for _, passed, _, required in checks)
    rows = [
        add_common(
            {
                "validation_id": validation_id,
                "passed": passed,
                "check": check,
                "required": required,
            }
        )
        for validation_id, passed, check, required in checks
    ]
    rows.append(add_common({"validation_id": "VAL2961_OVERALL", "passed": overall, "check": "2961 validation overall", "required": True}))
    return rows


def write_markdown(all_rows: dict[str, list[dict[str, Any]]]) -> None:
    doc = f"""# 2961 - Y5 R2FR: bconf branch selector, closure debt or residual smoke runner under AX1090

Status: `Y5_R2FR_2961_bconf_two_branch_selector_written_closure_debt_or_finite_residual_nonclaim`

Claim ceiling: `no_b_conf_theorem_zero_no_bconf_score_no_R10_PPN_clock_score_no_local_GR_no_Newton_no_public_claim`

2961 stops the proof loop and makes the fork explicit:

- Branch A is the closure-debt branch: impose the single-observed-frame rule, set `b_conf=0`, but give it no theorem-zero credit.
- Branch B is the finite-residual branch: keep `b_conf` live and require canonical `Xhat`, source/test current owner, `lambda_X`, and tau maps before any score.
- The smoke runner deliberately rejects both branches as claim evidence: closure is debt, residual rows are placeholders.
- The next useful work is finite-branch sourcing, not another attempt to re-derive the same single-frame clause.

## Source Register

{md_table(all_rows["sources"], ["source_id", "source_path", "path_exists", "anchors_found", "role"])}

## Branch Selector

{md_table(all_rows["selector"], ["selector_id", "selector_branch", "rule", "branch_allowed_for_private_work", "theorem_zero_credit", "local_GR_claim", "policy"])}

## Closure-Debt Branch

{md_table(all_rows["closure_branch"], ["row_id", "object", "branch_value", "closure_debt", "theorem_zero_credit", "accepted_for_scoring", "statement"])}

## Finite Residual Branch

{md_table(all_rows["residual_branch"], ["row_id", "symbol", "numeric_or_theorem_value", "units", "accepted_for_scoring", "next_needed"])}

## Smoke Runner Status

{md_table(all_rows["smoke"], ["smoke_id", "object", "valid_mts_rows", "smoke_status", "claim_allowed", "notes"])}

## Claim Gates

{md_table(all_rows["claims"], ["claim_gate_id", "claim", "condition_passed", "status", "claim_allowed"])}

## Decision Ledger

{md_table(all_rows["decision"], ["decision_id", "decision", "because", "next_action"])}

## Next Target

{md_table(all_rows["next"], ["next_id", "priority", "next_doc", "next_script", "objective", "exclude"])}

## Branch Copies

{md_table(all_rows["branches"], ["copy_id", "source_path", "copy_path", "source_exists", "copy_exists", "valid_for_claim"])}

## Validation

{md_table(all_rows["validation"], ["validation_id", "passed", "check", "required"])}

Validation overall: `{all_rows["validation"][-1]["passed"]}`.
"""
    DOC.write_text(doc, encoding="utf-8")


def main() -> None:
    selector = selector_rows()
    closure_branch = closure_branch_rows()
    residual_branch = residual_branch_rows()
    all_rows: dict[str, list[dict[str, Any]]] = {
        "sources": source_register_rows(),
        "selector": selector,
        "closure_branch": closure_branch,
        "residual_branch": residual_branch,
        "smoke": smoke_rows(selector, closure_branch, residual_branch),
        "claims": claim_gate_rows(),
        "decision": decision_rows(),
        "next": next_target_rows(),
    }

    for key, path in OUTPUTS.items():
        if key in {"branches", "validation"}:
            continue
        write_csv(path, all_rows[key])

    all_rows["branches"] = copy_branch_outputs()
    write_csv(OUTPUTS["branches"], all_rows["branches"])

    all_rows["validation"] = validation_rows(all_rows)
    write_csv(OUTPUTS["validation"], all_rows["validation"])
    write_markdown(all_rows)

    all_rows["validation"] = validation_rows(all_rows)
    write_csv(OUTPUTS["validation"], all_rows["validation"])
    write_markdown(all_rows)

    print(f"2961 validation overall: {all_rows['validation'][-1]['passed']}")
    print(DOC)


if __name__ == "__main__":
    main()
