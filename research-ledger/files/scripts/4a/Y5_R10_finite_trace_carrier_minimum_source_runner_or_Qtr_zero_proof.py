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

STATUS = "Y5_R10_902_finite_trace_minimum_source_runner_built_Qtr_zero_escape_unsigned_claims_blocked_nonclaim"
CLAIM_CEILING = "finite_trace_runner_gate_and_Qtr_zero_escape_only_no_numeric_alpha_no_R10_PPN_WEP_clock_orbital_or_local_GR_claim"
NEXT_TARGET = "903-Y5-R10-Qtr-source-cokernel-final-zero-proof-or-finite-alpha-source.md"

ALPHA_TR_FORMULA = "alpha_tr_AB=(Q_tr^A/m_A)*(Q_tr^B/m_B)/(4*pi*Z_tr*G_obs), evaluated at lambda_tr"

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

SOURCE_SPECS = [
    {
        "source_id": "901_doc",
        "path": ROOT / "901-Y5-R10-trace-owner-local-rank-zero-certificate-or-finite-carrier-fill.md",
        "needle": "trace-owner/local-rank-zero certificate does not close",
        "role": "immediate finite-carrier runner handoff",
    },
    {
        "source_id": "901_validation",
        "path": OUT / "P8_Y5_BRR545_901_VALIDATION.csv",
        "needle": "V901_11_validation_rows_ready",
        "role": "prior checkpoint validation",
    },
    {
        "source_id": "901_finite_fill",
        "path": OUT / "P8_Y5_R10_901_FINITE_CARRIER_FILL_ROWS.csv",
        "needle": "FCF901_0_Ptr_Htr",
        "role": "finite-carrier staged source rows",
    },
    {
        "source_id": "899_source_pack",
        "path": OUT / "P8_Y5_R10_899_TRACE_RESIDUAL_SOURCE_PACK.csv",
        "needle": "RSP899_2",
        "role": "Q_tr source-pack row",
    },
    {
        "source_id": "897_source_cokernel",
        "path": ROOT / "897-Y5-R10-coupling-origin-source-cokernel-and-double-zero-hunt.md",
        "needle": "J_tr=P_tr^dagger J_parent=0",
        "role": "source-cokernel theorem target",
    },
    {
        "source_id": "873_trace_charge_zero",
        "path": ROOT / "873-Y5-R10-local-matter-trace-charge-zero-theorem-or-coefficient-fill.md",
        "needle": "chain-rule zero theorem",
        "role": "conditional Q_tr charge-zero theorem",
    },
    {
        "source_id": "896_adoption_gate",
        "path": ROOT / "896-Y5-R10-trace-action-parent-adoption-gate-and-zero-vs-finite-branch-register.md",
        "needle": "finite trace branch demoted to closure-only",
        "role": "finite branch adoption failure",
    },
    {
        "source_id": "r10_runner",
        "path": ROOT / "scripts" / "R10_alpha_lambda_bound_prediction_runner.py",
        "needle": "MTS_REQUIRED_COLUMNS",
        "role": "existing alpha(lambda) schema and comparator",
    },
    {
        "source_id": "r10_bound_placeholder",
        "path": LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_DIGITIZED.csv",
        "needle": "R10_BOUND_PLACEHOLDER_0",
        "role": "current R10 bound file remains placeholder/nonclaim",
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


def nonclaim_summary_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "what_changed": "built the minimum finite trace-carrier runner gate while preserving Q_tr=0 as the final theorem escape hatch",
            "best_partial_result": "finite branch is now mechanically runnable only as a blocked dry gate; alpha_tr cannot be produced until Z_tr, lambda_tr, Q_tr/m, and a real bound curve are source-backed",
            "hard_blockers": "P_tr/H_tr, Z_tr, lambda_tr, Q_tr/m, metric/source response, species/clock response, boundary tail, and claim-grade R10 curve remain missing or theorem-dependent",
            "what_is_not_claimed": "finite trace carrier exists, alpha_tr is numeric, Q_tr is nonzero or zero, R10/PPN/WEP/clock/orbital pass, or local GR/Newton",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
    ]


def minimum_finite_input_rows(generated_utc: str) -> list[dict[str, object]]:
    staged = read_csv(OUT / "P8_Y5_R10_901_FINITE_CARRIER_FILL_ROWS.csv")
    rows: list[dict[str, object]] = []
    for index, row in enumerate(staged):
        quantity = row["quantity"]
        blocks = {
            "P_tr,H_tr": "all finite carrier decisions",
            "Z_tr": "alpha denominator and stability sign",
            "lambda_tr": "R10/orbital finite range",
            "Q_tr_over_m_universal": "R10/orbital common-force amplitude",
            "Delta_AB_Q_tr_over_m,C_tr_clock_i,C_tr_alphaEM": "WEP/clock/EM residuals",
            "C_tr_gamma,C_tr_beta,C_tr_source,Gdot_tr": "PPN/Newton/orbital residuals",
            "alpha_tr_AB(lambda_tr)": "R10 comparator row",
            "B_tr_tail,K_perp_trace": "boundary/local projection contamination",
        }.get(quantity, "local finite trace branch")
        rows.append(
            {
                "input_id": f"FTI902_{index}",
                "quantity": quantity,
                "definition": row["definition"],
                "runner_role": blocks,
                "current_value": row["current_value"],
                "source_required": row["next_action"],
                "zero_escape": "Q_tr_zero_escape_available" if "Q_tr" in quantity or "alpha_tr" in quantity else "no_pole_or_parent_source_required",
                "claim_gate": "invalid_until_numeric_source_backed_or_theorem_zero",
                "valid_for_claim": False,
                "generated_utc": generated_utc,
            }
        )
    return rows


def qtr_zero_escape_rows(generated_utc: str) -> list[dict[str, object]]:
    rows = [
        (
            "QZE902_0_definition",
            "Q_tr^A",
            "Q_tr^A := partial_{v_tr}S_A or integral_A J_tr with J_tr=P_tr^dagger J_parent",
            "definition_ready",
            "does not decide zero/nonzero",
        ),
        (
            "QZE902_1_chain_rule",
            "matter descent",
            "if S_A=Sbar_A[q_loc(Phi),Psi_A,theta_A], Dq_loc[v_tr]=0, and Lie_vtr theta_A=0, then Q_tr^A=0",
            "conditional_valid",
            "requires parent q_loc, v_tr, and no-marker constants",
        ),
        (
            "QZE902_2_source_cokernel",
            "J_tr source-cokernel",
            "if P_tr has zero compact-local physical image or local source-cokernel pairing vanishes, then <u_tr,J_parent>=0",
            "conditional_valid",
            "requires parent P_tr/H_tr/rank-zero or explicit cokernel pairing",
        ),
        (
            "QZE902_3_no_tail",
            "boundary/readout tail",
            "P_loc J_trace=0 and P_loc dB_trace=0 must hold so boundary/readout currents do not re-enter local source terms",
            "unsigned",
            "boundary tail remains active residual if not proved",
        ),
        (
            "QZE902_4_alpha_block",
            "alpha row embargo",
            "alpha_tr_AB cannot be computed as evidence while Q_tr is MISSING_SOURCE_PROJECTION_OR_ZERO_THEOREM",
            "rule_written",
            "prevents converting a missing coupling into a tiny fitted number",
        ),
        (
            "QZE902_5_verdict",
            "Q_tr=0 theorem escape hatch",
            "the zero theorem remains mathematically clean but parent-unsigned; finite alpha rows remain invalid until Q_tr is either zero-proved or source-backed",
            "not_signed",
            "selects Q_tr source-cokernel final proof or finite alpha source next",
        ),
    ]
    return [
        {
            "escape_id": escape_id,
            "target": target,
            "mathematical_form": mathematical_form,
            "current_status": current_status,
            "blocker_or_rule": blocker_or_rule,
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
        for escape_id, target, mathematical_form, current_status, blocker_or_rule in rows
    ]


def r10_alpha_dry_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "model_id": "MTS_finite_trace_carrier",
            "branch_id": "finite_trace_missing_source",
            "curve_id": "FT902_R10_0_missing_finite_alpha",
            "lambda_value": "MISSING_LAMBDA_TR",
            "lambda_units": "m",
            "alpha_predicted": "MISSING_ALPHA_TR_REQUIRES_ZTR_QTR",
            "alpha_bound": "MISSING_BOUND_LOOKUP",
            "alpha_bound_source": "source-intake/local_bounds/R10_alpha_lambda_bound_curve_DIGITIZED.csv",
            "force_law_form": "Yukawa alpha_tr_AB exp(-r/lambda_tr)",
            "derivation_status": "MISSING_PTR_HTR_ZTR_LAMBDATR_QTR",
            "formula_reference": ALPHA_TR_FORMULA,
            "source_file": "source-intake/mts_residuals/P8_Y5_R10_902_MINIMUM_FINITE_INPUT_SCHEMA.csv",
            "assumptions": "finite branch dry row only; no numeric source-backed trace carrier",
            "valid_for_claim": False,
            "notes": "runner must reject this row until parent values are real",
            "generated_utc": generated_utc,
        },
        {
            "model_id": "MTS_finite_trace_carrier",
            "branch_id": "Qtr_zero_escape_unsigned",
            "curve_id": "FT902_R10_1_Qtr_zero_escape_unsigned",
            "lambda_value": "MISSING_NOPOLE_OR_LAMBDA_TR",
            "lambda_units": "m",
            "alpha_predicted": "MISSING_QTR_ZERO_THEOREM_NOT_SIGNED",
            "alpha_bound": "MISSING_BOUND_LOOKUP",
            "alpha_bound_source": "source-intake/local_bounds/R10_alpha_lambda_bound_curve_DIGITIZED.csv",
            "force_law_form": "alpha_tr=0 only if Q_tr=0 or no source-coupled local pole is parent-signed",
            "derivation_status": "QTR_ZERO_ESCAPE_UNSIGNED_NONCLAIM",
            "formula_reference": "alpha_tr_AB=0 if Q_tr^A=0 or no local source-coupled trace pole",
            "source_file": "source-intake/mts_residuals/P8_Y5_R10_902_QTR_ZERO_ESCAPE_HATCH.csv",
            "assumptions": "theorem escape hatch only; not a pass",
            "valid_for_claim": False,
            "notes": "keeps zero route visible without claiming it",
            "generated_utc": generated_utc,
        },
    ]


def arena_gate_rows(generated_utc: str) -> list[dict[str, object]]:
    rows = [
        ("AG902_0_R10", "R10_short_range", "requires Z_tr, lambda_tr, Q_tr/m, real bound curve", "blocked_missing_finite_inputs"),
        ("AG902_1_PPN", "PPN", "requires C_tr_gamma, C_tr_beta, gauge/source-normalization split", "blocked_missing_response_operator"),
        ("AG902_2_WEP_clock_EM", "WEP_clock_EM", "requires Q_tr species deltas or no-marker theorem plus clock/EM response", "blocked_missing_no_marker_or_coefficients"),
        ("AG902_3_orbital_Newton", "orbital_Newton", "requires alpha_tr, lambda_tr, C_tr_source, GM absorption/Gdot split", "blocked_missing_orbital_projection"),
        ("AG902_4_local_GR", "local_GR_Newton", "requires trace branch zero/bounded plus other q_loc/EH/source-normalization gates", "blocked_trace_branch_not_closed"),
    ]
    return [
        {
            "arena_gate_id": gate_id,
            "arena": arena,
            "requires": requires,
            "current_status": current_status,
            "runner_status": "not_claim_ready",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
        for gate_id, arena, requires, current_status in rows
    ]


def branch_decision_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "branch_id": "BD902_0_Qtr_zero_escape",
            "branch": "prove Q_tr=0/source-cokernel before alpha",
            "status": "best_next_theorem_route",
            "decision": "not_promoted",
            "reason": "mathematics is clean but parent P_tr/q_loc/matter no-marker/no-tail signatures remain unsigned",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "branch_id": "BD902_1_finite_alpha_source",
            "branch": "source finite alpha_tr(lambda_tr)",
            "status": "runner_gate_built_nonclaim",
            "decision": "not_executable",
            "reason": "Z_tr, lambda_tr, Q_tr/m, and R10 bound curve are missing or placeholder",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "branch_id": "BD902_2_selected_next",
            "branch": "Qtr source-cokernel final zero proof or finite alpha source",
            "status": "selected",
            "decision": NEXT_TARGET,
            "reason": "Q_tr is the last high-leverage coupling before any R10 alpha row can exist",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def claim_gate_rows(generated_utc: str) -> list[dict[str, object]]:
    rows = [
        ("CGATE902_0_Qtr_zero", "Q_tr=0", "source-cokernel theorem not parent-signed"),
        ("CGATE902_1_finite_alpha", "alpha_tr(lambda_tr) numeric", "Z_tr/lambda_tr/Q_tr are missing"),
        ("CGATE902_2_R10_compare", "R10 comparison pass", "MTS alpha rows and bound curve are invalid placeholders"),
        ("CGATE902_3_PPN_WEP_clock_orbital", "other local arenas pass", "response operators and species/clock/source projections missing"),
        ("CGATE902_4_local_GR", "local GR/Newton derivation", "trace branch is neither theorem-zeroed nor empirically bounded"),
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
        for gate_id, claim, blocker in rows
    ]


def next_target_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "next_target": NEXT_TARGET,
            "objective": "make one final source-cokernel attempt to prove Q_tr=0; if it fails, require real source-backed finite alpha inputs before any empirical comparison",
            "include": "J_tr=P_tr^dagger J_parent, matter descent, no-marker constants, source-cokernel pairing, finite alpha source rows, R10 bound curve blocker",
            "exclude": "fitted tiny alpha, placeholder bound curves, local-GR claim, formalization-workbench edits, GitHub action",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
    ]


def prior_901_clean() -> bool:
    path = OUT / "P8_Y5_BRR545_901_VALIDATION.csv"
    return path.exists() and all(row.get("result") == "pass" for row in read_csv(path))


def formalization_changed_count() -> int:
    if not FORMALIZATION.exists():
        return -1
    count = 0
    for path in FORMALIZATION.rglob("*"):
        if path.is_file():
            modified = datetime.fromtimestamp(path.stat().st_mtime)
            if modified > CUTOFF:
                count += 1
    return count


def generated_rows_nonclaim(row_groups: list[list[dict[str, object]]]) -> bool:
    for group in row_groups:
        for row in group:
            if "valid_for_claim" in row and stringify(row["valid_for_claim"]).lower() != "false":
                return False
            if "claim_allowed" in row and stringify(row["claim_allowed"]).lower() != "false":
                return False
    return True


def import_r10_runner() -> Any:
    runner_path = ROOT / "scripts" / "R10_alpha_lambda_bound_prediction_runner.py"
    spec = importlib.util.spec_from_file_location("r10_runner_902", runner_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {runner_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_r10_dry_runner() -> dict[str, Any]:
    module = import_r10_runner()
    result = module.run_runner(
        OUT / "P8_Y5_R10_902_R10_ALPHA_DRY_ROWS.csv",
        LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_DIGITIZED.csv",
        OUT / "P8_Y5_R10_902_R10_DRY_RUNNER_RESULTS",
    )
    return result["status"]


def validation_rows(
    generated_utc: str,
    source_rows_: list[dict[str, object]],
    summary_rows_: list[dict[str, object]],
    input_rows_: list[dict[str, object]],
    qzero_rows_: list[dict[str, object]],
    dry_rows_: list[dict[str, object]],
    arena_rows_: list[dict[str, object]],
    branch_rows_: list[dict[str, object]],
    claim_rows_: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    runner_status: dict[str, Any],
) -> list[dict[str, object]]:
    formalization_count = formalization_changed_count()
    row_groups = [
        summary_rows_,
        input_rows_,
        qzero_rows_,
        dry_rows_,
        arena_rows_,
        branch_rows_,
        claim_rows_,
        next_rows_,
    ]
    missing_schema_columns = [column for column in MTS_REQUIRED_COLUMNS if column not in dry_rows_[0]]
    checks = [
        {
            "check_id": "V902_0_sources_exist_and_needles",
            "result": "pass"
            if all(row["exists"] is True and row["needle_check"] == "pass" for row in source_rows_)
            else "fail",
            "detail": "all source paths exist and needles are present",
        },
        {
            "check_id": "V902_1_prior_901_clean",
            "result": "pass" if prior_901_clean() else "fail",
            "detail": "P8_Y5_BRR545_901_VALIDATION.csv clean",
        },
        {
            "check_id": "V902_2_minimum_inputs_staged_missing",
            "result": "pass" if len(input_rows_) == 8 and all("MISSING" in stringify(row["current_value"]) for row in input_rows_) else "fail",
            "detail": f"minimum_input_rows={len(input_rows_)}",
        },
        {
            "check_id": "V902_3_Qtr_zero_escape_unsigned",
            "result": "pass"
            if any(row["escape_id"] == "QZE902_5_verdict" and row["current_status"] == "not_signed" for row in qzero_rows_)
            else "fail",
            "detail": "Q_tr zero escape hatch remains theorem target only",
        },
        {
            "check_id": "V902_4_R10_dry_rows_match_schema",
            "result": "pass" if not missing_schema_columns else "fail",
            "detail": "schema ok" if not missing_schema_columns else "missing=" + ",".join(missing_schema_columns),
        },
        {
            "check_id": "V902_5_R10_dry_runner_blocks_claim",
            "result": "pass"
            if runner_status.get("claim_allowed") is False and runner_status.get("valid_mts_rows") == 0
            else "fail",
            "detail": json.dumps(
                {
                    "claim_allowed": runner_status.get("claim_allowed"),
                    "valid_mts_rows": runner_status.get("valid_mts_rows"),
                    "blocked_or_failed_rows": runner_status.get("blocked_or_failed_rows"),
                },
                sort_keys=True,
            ),
        },
        {
            "check_id": "V902_6_arena_gates_false",
            "result": "pass" if all(row["claim_allowed"] is False for row in arena_rows_) else "fail",
            "detail": "R10/PPN/WEP-clock/orbital/local-GR gates all blocked",
        },
        {
            "check_id": "V902_7_branch_selects_Qtr_next",
            "result": "pass" if any(row["decision"] == NEXT_TARGET for row in branch_rows_) else "fail",
            "detail": NEXT_TARGET,
        },
        {
            "check_id": "V902_8_claim_gates_false",
            "result": "pass" if all(row["claim_allowed"] is False for row in claim_rows_) else "fail",
            "detail": "all finite/zero/local claims remain blocked",
        },
        {
            "check_id": "V902_9_all_generated_rows_nonclaim",
            "result": "pass" if generated_rows_nonclaim(row_groups) else "fail",
            "detail": "all generated rows keep valid_for_claim/claim_allowed false",
        },
        {
            "check_id": "V902_10_formalization_workbench_untouched",
            "result": "pass" if formalization_count == 0 else "fail",
            "detail": f"formalization_changed_after_cutoff={formalization_count}",
        },
        {
            "check_id": "V902_11_route_selected",
            "result": "pass" if next_rows_ and next_rows_[0]["next_target"] == NEXT_TARGET else "fail",
            "detail": NEXT_TARGET,
        },
        {
            "check_id": "V902_12_validation_rows_ready",
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
    input_rows_: list[dict[str, object]],
    qzero_rows_: list[dict[str, object]],
    dry_rows_: list[dict[str, object]],
    arena_rows_: list[dict[str, object]],
    branch_rows_: list[dict[str, object]],
    claim_rows_: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    validation_rows_: list[dict[str, object]],
) -> None:
    content = f"""# 902 - Y5/R10 Finite Trace Carrier Minimum Source Runner Or Qtr Zero Proof

Status: `{STATUS}`
Claim ceiling: `{CLAIM_CEILING}`
Generated UTC: `{generated_utc}`

Current result: **the finite trace branch now has a minimum runner gate, but it is deliberately non-executable for claims**. The gate demands `P_tr/H_tr`, `Z_tr`, `lambda_tr`, `Q_tr/m`, response operators, boundary-tail control, and a real R10 bound curve before any `alpha_tr(lambda)` comparison. The R10 runner is dry-run only and correctly refuses the placeholder rows. The one remaining high-leverage theorem escape is `Q_tr=0` by source-cokernel/matter descent; that must be tried before turning `Q_tr` into a sourced finite coupling.

## Exact 902 Finding
This checkpoint turns the finite branch from a vague fallback into a strict evidence contract. If `Q_tr=0` closes, the R10/orbital matter amplitude vanishes without fitting a tiny coupling. If it does not close, MTS must provide real parent-derived `Z_tr`, `lambda_tr`, and `Q_tr/m` before the first numeric local fifth-force comparison is even allowed. So the finite branch is now testable in principle, but it is not evidence yet.

## Nonclaim Summary
{md_table(summary_rows_)}

## Source Register
{md_table(source_rows_)}

## Minimum Finite Input Schema
{md_table(input_rows_)}

## Qtr Zero Escape Hatch
{md_table(qzero_rows_)}

## R10 Alpha Dry Rows
{md_table(dry_rows_)}

## Arena Runner Gates
{md_table(arena_rows_)}

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
    summary_rows_ = nonclaim_summary_rows(generated_utc)
    input_rows_ = minimum_finite_input_rows(generated_utc)
    qzero_rows_ = qtr_zero_escape_rows(generated_utc)
    dry_rows_ = r10_alpha_dry_rows(generated_utc)
    arena_rows_ = arena_gate_rows(generated_utc)
    branch_rows_ = branch_decision_rows(generated_utc)
    claim_rows_ = claim_gate_rows(generated_utc)
    next_rows_ = next_target_rows(generated_utc)

    initial_outputs = {
        "P8_Y5_R10_902_SOURCE_REGISTER.csv": source_rows_,
        "P8_Y5_R10_902_NONCLAIM_SUMMARY.csv": summary_rows_,
        "P8_Y5_R10_902_MINIMUM_FINITE_INPUT_SCHEMA.csv": input_rows_,
        "P8_Y5_R10_902_QTR_ZERO_ESCAPE_HATCH.csv": qzero_rows_,
        "P8_Y5_R10_902_R10_ALPHA_DRY_ROWS.csv": dry_rows_,
        "P8_Y5_R10_902_ARENA_RUNNER_GATES.csv": arena_rows_,
        "P8_Y5_R10_902_BRANCH_DECISION.csv": branch_rows_,
        "P8_Y5_R10_902_CLAIM_GATE.csv": claim_rows_,
        "P8_Y5_R10_902_NEXT_TARGET.csv": next_rows_,
    }
    for filename, rows in initial_outputs.items():
        write_csv(OUT / filename, rows)

    runner_status = run_r10_dry_runner()
    validation_rows_ = validation_rows(
        generated_utc,
        source_rows_,
        summary_rows_,
        input_rows_,
        qzero_rows_,
        dry_rows_,
        arena_rows_,
        branch_rows_,
        claim_rows_,
        next_rows_,
        runner_status,
    )
    write_csv(OUT / "P8_Y5_BRR545_902_VALIDATION.csv", validation_rows_)

    doc_path = ROOT / "902-Y5-R10-finite-trace-carrier-minimum-source-runner-or-Qtr-zero-proof.md"
    write_markdown(
        doc_path,
        generated_utc,
        summary_rows_,
        source_rows_,
        input_rows_,
        qzero_rows_,
        dry_rows_,
        arena_rows_,
        branch_rows_,
        claim_rows_,
        next_rows_,
        validation_rows_,
    )

    failed = [row for row in validation_rows_ if row["result"] != "pass"]
    print(f"wrote {doc_path}")
    print(f"wrote {OUT / 'P8_Y5_BRR545_902_VALIDATION.csv'}")
    print(f"status={STATUS}")
    if failed:
        print("failed_validation=" + ",".join(row["check_id"] for row in failed))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
