from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from R10_alpha_lambda_bound_prediction_runner import MTS_REQUIRED_COLUMNS, run_runner


ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = Path("source-intake/mts_residuals")
LOCAL_BOUND_DIR = Path("source-intake/local_bounds")
RUN_DIR = Path("runs/1392-R10-bulk-alpha-template-smoke")

DOC_PATH = Path("1392-Y5-R10-RAB-bulk-alpha-template-beta-kernel-tail-fill-or-zero-proof.md")
SOURCE_REGISTER_PATH = SRC_DIR / "P8_Y5_R10_1392_SOURCE_REGISTER.csv"
ZERO_ATTEMPT_PATH = SRC_DIR / "P8_Y5_R10_1392_BETA_KERNEL_TAIL_ZERO_ATTEMPT.csv"
BULK_ALPHA_TEMPLATE_PATH = SRC_DIR / "R10_alpha_lambda_curve_MTS_1392_BULK_ALPHA_TEMPLATE_NONCLAIM.csv"
TEMPLATE_REGISTER_PATH = SRC_DIR / "P8_Y5_R10_1392_BULK_ALPHA_TEMPLATE_REGISTER.csv"
RUNNER_SUMMARY_PATH = SRC_DIR / "P8_Y5_R10_1392_R10_RUNNER_SMOKE_SUMMARY.csv"
CLAIM_GATE_PATH = SRC_DIR / "P8_Y5_R10_1392_CLAIM_GATE.csv"
DECISION_LEDGER_PATH = SRC_DIR / "P8_Y5_R10_1392_DECISION_LEDGER.csv"
NEXT_TARGET_PATH = SRC_DIR / "P8_Y5_R10_1392_NEXT_TARGET.csv"
VALIDATION_PATH = SRC_DIR / "P8_Y5_BRR545_1392_VALIDATION.csv"

STATUS = (
    "bulk_alpha_template_written_runner_compatible_nonclaim_"
    "beta_kernel_tail_zero_unsigned_R10_runner_blocks"
)
CLAIM_CEILING = (
    "bulk_alpha_template_and_runner_smoke_only_no_beta_zero_no_numeric_alpha_"
    "no_R10_no_WEP_no_PPN_no_Newton_no_local_GR_pass"
)

SOURCE_ROWS = [
    {
        "source_id": "SRC1392_0_1391_doc",
        "source_path": "1391-Y5-R10-RAB-bulk-neutral-coefficient-source-pack-and-R10-kernel-gate.md",
        "required_anchor": "NEXT1391_0_1392",
        "purpose": "handoff to bulk alpha template or beta/kernel/tail zero proof",
    },
    {
        "source_id": "SRC1392_1_1391_next",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1391_NEXT_TARGET.csv",
        "required_anchor": "NEXT1391_0_1392",
        "purpose": "machine-readable 1392 target",
    },
    {
        "source_id": "SRC1392_2_1391_zero",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1391_BULK_NEUTRAL_ZERO_THEOREM_ATTEMPT.csv",
        "required_anchor": "BZT1391_4_product_zero_condition",
        "purpose": "conditional product zero route",
    },
    {
        "source_id": "SRC1392_3_1391_zero_verdict",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1391_BULK_NEUTRAL_ZERO_THEOREM_ATTEMPT.csv",
        "required_anchor": "BZT1391_5_current_verdict",
        "purpose": "bulk zero remains unsigned",
    },
    {
        "source_id": "SRC1392_4_1391_pack",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1391_BULK_NEUTRAL_COEFFICIENT_SOURCE_PACK.csv",
        "required_anchor": "BCP1391_7_pack_verdict",
        "purpose": "bulk coefficient source pack",
    },
    {
        "source_id": "SRC1392_5_1391_kernel",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1391_R10_BULK_MATERIAL_KERNEL_GATE.csv",
        "required_anchor": "R10K1391_6_verdict",
        "purpose": "R10 material-kernel gate",
    },
    {
        "source_id": "SRC1392_6_1391_runner_refusal",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1391_R10_RUNNER_REFUSAL_AUDIT.csv",
        "required_anchor": "RRF1391_3_verdict",
        "purpose": "prior runner refusal audit",
    },
    {
        "source_id": "SRC1392_7_563_runner",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_563_RUNNER_SUMMARY.csv",
        "required_anchor": "R10_RUNNER_563_ANCHOR_SMOKE_RECHECK",
        "purpose": "R10 runner must reject nonclaim smoke rows",
    },
    {
        "source_id": "SRC1392_8_anchor_bound",
        "source_path": "source-intake/local_bounds/R10_alpha_lambda_bound_curve_ANCHOR_SMOKE.csv",
        "required_anchor": "R10_ANCHOR_EOTWASH_2020_ALPHA1_38P6UM",
        "purpose": "anchor-only nonclaim bound rows",
    },
    {
        "source_id": "SRC1392_9_live_bound",
        "source_path": "source-intake/local_bounds/R10_alpha_lambda_bound_curve_DIGITIZED.csv",
        "required_anchor": "R10_BOUND_PLACEHOLDER_0",
        "purpose": "live digitized bound file remains placeholder invalid",
    },
    {
        "source_id": "SRC1392_10_runner",
        "source_path": "scripts/R10_alpha_lambda_bound_prediction_runner.py",
        "required_anchor": "MTS_REQUIRED_COLUMNS",
        "purpose": "existing R10 comparator schema and validation logic",
    },
    {
        "source_id": "SRC1392_11_this_script",
        "source_path": "scripts/Y5_R10_RAB_bulk_alpha_template_beta_kernel_tail_fill_or_zero_proof.py",
        "required_anchor": "STATUS",
        "purpose": "1392 generator",
    },
]


def clean(value: Any) -> str:
    return str(value).replace("\n", " ").strip()


def write_csv(path: Path, rows: list[dict[str, Any]], columns: list[str] | None = None) -> None:
    full_path = ROOT / path
    full_path.parent.mkdir(parents=True, exist_ok=True)
    if columns is None:
        columns = list(rows[0].keys()) if rows else []
    with full_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        for row in rows:
            writer.writerow({column: clean(row.get(column, "")) for column in columns})


def md_table(rows: list[dict[str, Any]], columns: list[str] | None = None) -> str:
    if not rows:
        return ""
    if columns is None:
        columns = list(rows[0].keys())
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join("---" for _ in columns) + " |"
    body = [
        "| " + " | ".join(clean(row.get(column, "")).replace("|", "\\|") for column in columns) + " |"
        for row in rows
    ]
    return "\n".join([header, divider, *body])


def anchor_found(path: Path, anchor: str) -> bool:
    if not path.exists():
        return False
    return anchor in path.read_text(encoding="utf-8", errors="ignore")


def source_register_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for source in SOURCE_ROWS:
        source_path = ROOT / source["source_path"]
        rows.append(
            {
                **source,
                "exists": str(source_path.exists()),
                "anchor_found": str(anchor_found(source_path, source["required_anchor"])),
                "valid_for_claim": "False",
                "claim_allowed": "False",
            }
        )
    return rows


def zero_attempt_rows() -> list[dict[str, str]]:
    return [
        {
            "zero_id": "BKT1392_0_beta_source_zero",
            "target": "beta_bulk,S=0",
            "attempted_derivation": "source bulk leg inherits common ordinary-matter owner and has no independent binding/source marker",
            "result": "CONDITIONAL_ZERO_ROUTE",
            "gap": "common owner, binding inheritance, and source material composition are not parent-signed",
            "template_consequence": "keep beta_bulk,S as an explicit symbolic factor",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "zero_id": "BKT1392_1_beta_test_zero",
            "target": "beta_bulk,T=0",
            "attempted_derivation": "test bulk leg inherits the same ordinary-matter owner and has no independent readout/material marker",
            "result": "CONDITIONAL_ZERO_ROUTE",
            "gap": "test material composition and binding/readout inheritance remain unsigned",
            "template_consequence": "keep beta_bulk,T as an explicit symbolic factor",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "zero_id": "BKT1392_2_kernel_finiteness",
            "target": "K_bulk,ST(lambda) is finite and convention-locked",
            "attempted_derivation": "profile kernel is a finite-size/source-test correction, not a free alpha parameter",
            "result": "KERNEL_SCHEMA_READY_NOT_FILLED",
            "gap": "source/test geometry, density profile, and lambda convention are not filled",
            "template_consequence": "K_bulk,ST(lambda) remains symbolic but required",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "zero_id": "BKT1392_3_tail_zero",
            "target": "epsilon_tail(lambda)=0",
            "attempted_derivation": "all nonbulk, boundary, binding, and projection leakage terms vanish or are separately bounded",
            "result": "TAIL_ZERO_NOT_SIGNED",
            "gap": "tail channels are not theorem-zero and no conservative envelope exists",
            "template_consequence": "epsilon_tail(lambda) remains a required symbolic/envelope term",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "zero_id": "BKT1392_4_alpha_zero_condition",
            "target": "alpha_bulk,ST(lambda)=0",
            "attempted_derivation": "if beta_bulk,S=0, beta_bulk,T=0, and epsilon_tail(lambda)=0, then alpha_bulk,ST(lambda)=0 regardless of finite K",
            "result": "EXACT_CONDITIONAL_ZERO",
            "gap": "the zero premises are unsigned",
            "template_consequence": "zero certificate shape recorded but not claim-ready",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "zero_id": "BKT1392_5_current_verdict",
            "target": "beta/kernel/tail zero proof status",
            "attempted_derivation": "compare 1391 source pack and R10 kernel gate against runner requirements",
            "result": "ZERO_PROOF_UNSIGNED_TEMPLATE_REQUIRED",
            "gap": "beta source/test, K(lambda), tail, and bound curve are not filled or theorem-zero",
            "template_consequence": "write strict nonclaim R10 alpha template and runner smoke",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def bulk_alpha_template_rows() -> list[dict[str, str]]:
    base = {
        "model_id": "MTS_source_normalized_Newton_branch",
        "branch_id": "R10_bulk_neutral_beta_kernel_tail_template",
        "curve_id": "R10_alpha_lambda_curve_MTS_1392_BULK_ALPHA_TEMPLATE_NONCLAIM",
        "lambda_units": "m",
        "alpha_predicted": "K_bulk_ST(lambda)*beta_bulk_S*beta_bulk_T+epsilon_tail(lambda)",
        "alpha_bound": "1.0",
        "force_law_form": "Yukawa_strength_ratio_bulk_source_test",
        "derivation_status": "symbolic_bulk_alpha_template_nonclaim_zero_premises_unsigned",
        "formula_reference": "1392-Y5-R10-RAB-bulk-alpha-template-beta-kernel-tail-fill-or-zero-proof.md::alpha_bulk_ST(lambda)=K_bulk_ST(lambda) beta_bulk_S beta_bulk_T + epsilon_tail(lambda)",
        "source_file": "1392-Y5-R10-RAB-bulk-alpha-template-beta-kernel-tail-fill-or-zero-proof.md",
        "assumptions": "same_frame_source_normalization;bulk_neutral_material_pair;canonical_phi_convention;no_claim_until_beta_K_tail_bound_curve_are_sourced",
        "valid_for_claim": "false",
        "beta_source_handle": "beta_bulk_S",
        "beta_test_handle": "beta_bulk_T",
        "K_lambda_handle": "K_bulk_ST(lambda)",
        "epsilon_tail_handle": "epsilon_tail(lambda)",
        "material_pair": "bulk_neutral_source__bulk_neutral_test",
        "blocking_inputs": "beta_bulk_S;beta_bulk_T;K_bulk_ST(lambda);epsilon_tail(lambda);full_R10_bound_curve",
    }
    return [
        {
            **base,
            "lambda_value": "3.86e-5",
            "alpha_bound_source": "source-intake/local_bounds/R10_alpha_lambda_bound_curve_ANCHOR_SMOKE.csv::R10_ANCHOR_EOTWASH_2020_ALPHA1_38P6UM",
            "notes": "Runner-compatible anchor-aligned row; alpha_predicted is intentionally symbolic and valid_for_claim=false.",
        },
        {
            **base,
            "lambda_value": "5.6e-5",
            "alpha_bound_source": "source-intake/local_bounds/R10_alpha_lambda_bound_curve_ANCHOR_SMOKE.csv::R10_ANCHOR_EOTWASH_2007_ALPHA1_56UM",
            "notes": "Second anchor-aligned row; anchors are provenance only, not a full claim curve.",
        },
    ]


def template_register_rows() -> list[dict[str, str]]:
    return [
        {
            "register_id": "ATR1392_0_schema",
            "artifact": str(BULK_ALPHA_TEMPLATE_PATH).replace("\\", "/"),
            "requirement": "contains every MTS_REQUIRED_COLUMNS field expected by R10_alpha_lambda_bound_prediction_runner.py",
            "current_status": "RUNNER_COMPATIBLE_SCHEMA",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "register_id": "ATR1392_1_factor_exposure",
            "artifact": str(BULK_ALPHA_TEMPLATE_PATH).replace("\\", "/"),
            "requirement": "exposes beta source, beta test, K(lambda), epsilon_tail, material pair, and blocking inputs",
            "current_status": "FACTORS_EXPOSED_SYMBOLIC",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "register_id": "ATR1392_2_claim_flags",
            "artifact": str(BULK_ALPHA_TEMPLATE_PATH).replace("\\", "/"),
            "requirement": "all rows keep valid_for_claim=false until values and provenance are real",
            "current_status": "ALL_ROWS_NONCLAIM",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "register_id": "ATR1392_3_runner_expectation",
            "artifact": str(BULK_ALPHA_TEMPLATE_PATH).replace("\\", "/"),
            "requirement": "existing runner must reject the rows because alpha_predicted is symbolic and claim flag is false",
            "current_status": "RUNNER_MUST_BLOCK",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def runner_summary_rows() -> list[dict[str, str]]:
    anchor_result = run_runner(
        ROOT / BULK_ALPHA_TEMPLATE_PATH,
        ROOT / LOCAL_BOUND_DIR / "R10_alpha_lambda_bound_curve_ANCHOR_SMOKE.csv",
        ROOT / RUN_DIR / "anchor_smoke_results",
    )["status"]
    live_result = run_runner(
        ROOT / BULK_ALPHA_TEMPLATE_PATH,
        ROOT / LOCAL_BOUND_DIR / "R10_alpha_lambda_bound_curve_DIGITIZED.csv",
        ROOT / RUN_DIR / "live_placeholder_results",
    )["status"]
    return [
        {
            "runner_id": "RUN1392_0_anchor_smoke",
            "mts_curve": anchor_result["mts_curve"],
            "bound_curve": anchor_result["bound_curve"],
            "valid_mts_rows": str(anchor_result["valid_mts_rows"]),
            "valid_bound_rows": str(anchor_result["valid_bound_rows"]),
            "comparison_rows": str(anchor_result["comparison_rows"]),
            "R10_pass_for_claim": str(anchor_result["R10_pass_for_claim"]),
            "claim_allowed": str(anchor_result["claim_allowed"]),
            "output_dir": anchor_result["output_dir"],
            "required_result": "False",
            "notes": "anchor smoke must block because MTS alpha is symbolic and anchors are nonclaim",
        },
        {
            "runner_id": "RUN1392_1_live_placeholder",
            "mts_curve": live_result["mts_curve"],
            "bound_curve": live_result["bound_curve"],
            "valid_mts_rows": str(live_result["valid_mts_rows"]),
            "valid_bound_rows": str(live_result["valid_bound_rows"]),
            "comparison_rows": str(live_result["comparison_rows"]),
            "R10_pass_for_claim": str(live_result["R10_pass_for_claim"]),
            "claim_allowed": str(live_result["claim_allowed"]),
            "output_dir": live_result["output_dir"],
            "required_result": "False",
            "notes": "live placeholder run must block because both MTS prediction and live bound curve are invalid",
        },
    ]


def claim_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "GATE1392_0_sources",
            "gate": "all cited local sources exist and anchors are present",
            "status": "PASS",
            "reason": "source register validates against local corpus",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE1392_1_zero_proof",
            "gate": "beta/kernel/tail zero proof closes",
            "status": "BLOCKED_PARENT_UNSIGNED",
            "reason": "conditional zero is exact but beta source/test and tail-zero premises are unsigned",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE1392_2_template",
            "gate": "bulk alpha template is runner-compatible",
            "status": "PASS_NONCLAIM_TEMPLATE",
            "reason": "candidate rows include required runner columns plus beta/K/tail factor handles",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE1392_3_runner",
            "gate": "existing R10 runner accepts the template for scoring",
            "status": "BLOCKED_RUNNER_REJECTS_NONCLAIM_ROWS",
            "reason": "runner smoke returns R10_pass_for_claim=false for anchor and live placeholder comparisons",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE1392_4_R10_score",
            "gate": "R10 score may be reported",
            "status": "BLOCKED_NO_NUMERIC_ALPHA_OR_CLAIM_CURVE",
            "reason": "alpha_predicted is symbolic, valid_for_claim=false, and full bound curve is absent",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE1392_5_local_claim",
            "gate": "local GR/Newton reduction can be claimed",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "1392 is a strict template/runner-smoke checkpoint, not a derived local GR limit",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC1392_0_zero_status",
            "decision": "retain zero route only as conditional theorem",
            "because": "beta_bulk,S, beta_bulk,T, and epsilon_tail are not parent-zero or bounded",
            "next_action": "fill or prove the first factor, starting with beta_bulk source/test convention",
            "claim_allowed": "False",
        },
        {
            "decision_id": "DEC1392_1_template_status",
            "decision": "write runner-compatible nonclaim alpha template",
            "because": "future R10 testing needs rows the existing comparator can parse, even before they can score",
            "next_action": "turn symbolic beta/K/tail handles into source-backed numeric or zero-certified fields",
            "claim_allowed": "False",
        },
        {
            "decision_id": "DEC1392_2_runner_status",
            "decision": "runner smoke must fail safely",
            "because": "passing with symbolic alpha or anchor-only bounds would be a false R10 claim",
            "next_action": "keep R10 blocked until numeric alpha and full bound curve both become claim-ready",
            "claim_allowed": "False",
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_id": "NEXT1392_0_1393",
            "next_doc": "1393-Y5-R10-RAB-beta-bulk-source-test-convention-or-theorem-zero.md",
            "next_script": "scripts/Y5_R10_RAB_beta_bulk_source_test_convention_or_theorem_zero.py",
            "task": "derive or source the beta_bulk source/test convention; if theorem-zero fails, create nonclaim beta source/test coefficient rows with material/provenance gates",
            "success_condition": "beta_bulk,S and beta_bulk,T are either theorem-zero under signed premises or explicit nonclaim coefficient rows with units, source/test material roles, and runner-blocking flags",
            "do_not_claim": "local GR;Newton limit;PPN pass;R10 pass;WEP pass;q_loc=0;numeric alpha(lambda);GitHub-ready result",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        }
    ]


def csv_rows(path: Path) -> list[dict[str, str]]:
    with (ROOT / path).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def validation_rows(
    sources: list[dict[str, str]],
    zero: list[dict[str, str]],
    template: list[dict[str, str]],
    register: list[dict[str, str]],
    runner_summary: list[dict[str, str]],
    gates: list[dict[str, str]],
) -> list[dict[str, str]]:
    source_pass = all(row["exists"] == "True" and row["anchor_found"] == "True" for row in sources)
    conditional_zero = any(
        row["zero_id"] == "BKT1392_4_alpha_zero_condition"
        and row["result"] == "EXACT_CONDITIONAL_ZERO"
        and row["valid_for_claim"] == "False"
        for row in zero
    )
    zero_unsigned = any(
        row["zero_id"] == "BKT1392_5_current_verdict"
        and row["result"] == "ZERO_PROOF_UNSIGNED_TEMPLATE_REQUIRED"
        and row["claim_allowed"] == "False"
        for row in zero
    )
    template_columns = set(template[0].keys()) if template else set()
    schema_ok = set(MTS_REQUIRED_COLUMNS).issubset(template_columns)
    factors_exposed = {"beta_source_handle", "beta_test_handle", "K_lambda_handle", "epsilon_tail_handle"}.issubset(
        template_columns
    )
    template_nonclaim = bool(template) and all(row["valid_for_claim"].lower() == "false" for row in template)
    alpha_symbolic = bool(template) and all("beta_bulk" in row["alpha_predicted"] for row in template)
    register_ready = any(
        row["register_id"] == "ATR1392_3_runner_expectation"
        and row["current_status"] == "RUNNER_MUST_BLOCK"
        for row in register
    )
    runner_blocks = bool(runner_summary) and all(
        row["R10_pass_for_claim"] == "False" and row["claim_allowed"] == "False" for row in runner_summary
    )
    local_claim_blocked = any(
        row["gate_id"] == "GATE1392_5_local_claim"
        and row["status"] == "BLOCKED_NO_CLAIM"
        and row["claim_allowed"] == "False"
        for row in gates
    )
    prior_1391 = csv_rows(SRC_DIR / "P8_Y5_R10_1391_CLAIM_GATE.csv")
    prior_local_blocked = any(
        row["gate_id"] == "GATE1391_5_local_claim" and row["status"] == "BLOCKED_NO_CLAIM"
        for row in prior_1391
    )
    outputs = [
        DOC_PATH,
        SOURCE_REGISTER_PATH,
        ZERO_ATTEMPT_PATH,
        BULK_ALPHA_TEMPLATE_PATH,
        TEMPLATE_REGISTER_PATH,
        RUNNER_SUMMARY_PATH,
        CLAIM_GATE_PATH,
        DECISION_LEDGER_PATH,
        NEXT_TARGET_PATH,
        VALIDATION_PATH,
        Path("scripts/Y5_R10_RAB_bulk_alpha_template_beta_kernel_tail_fill_or_zero_proof.py"),
        RUN_DIR / "anchor_smoke_results/R10_runner_status.json",
        RUN_DIR / "live_placeholder_results/R10_runner_status.json",
    ]
    formalization_touched = any("formalization-workbench" in str((ROOT / output).resolve()) for output in outputs)
    scope_ok = all((ROOT / output).resolve().is_relative_to(ROOT.resolve()) for output in outputs) and not formalization_touched
    overall = (
        source_pass
        and conditional_zero
        and zero_unsigned
        and schema_ok
        and factors_exposed
        and template_nonclaim
        and alpha_symbolic
        and register_ready
        and runner_blocks
        and local_claim_blocked
        and prior_local_blocked
        and scope_ok
    )
    return [
        {
            "validation_id": "VAL1392_0_sources",
            "check": "every cited local source path exists and anchor is found",
            "status": "PASS" if source_pass else "FAIL",
            "details": "; ".join(
                f"{row['source_id']} exists={row['exists']} anchor={row['anchor_found']}" for row in sources
            ),
        },
        {
            "validation_id": "VAL1392_1_zero_refusal",
            "check": "beta/kernel/tail zero proof is exact conditional but unsigned",
            "status": "PASS" if conditional_zero and zero_unsigned else "FAIL",
            "details": "BKT1392_4 records the exact zero condition; BKT1392_5 keeps it unsigned.",
        },
        {
            "validation_id": "VAL1392_2_template_schema",
            "check": "bulk alpha template is runner-compatible and factor-exposing",
            "status": "PASS" if schema_ok and factors_exposed and template_nonclaim and alpha_symbolic else "FAIL",
            "details": f"required_columns_ok={schema_ok}; factors_exposed={factors_exposed}; rows={len(template)}",
        },
        {
            "validation_id": "VAL1392_3_runner_blocks",
            "check": "existing R10 runner blocks the nonclaim template",
            "status": "PASS" if runner_blocks and register_ready else "FAIL",
            "details": "; ".join(
                f"{row['runner_id']} R10_pass={row['R10_pass_for_claim']} valid_mts={row['valid_mts_rows']} valid_bound={row['valid_bound_rows']}"
                for row in runner_summary
            ),
        },
        {
            "validation_id": "VAL1392_4_claim_refusal",
            "check": "R10 and local claims remain blocked",
            "status": "PASS" if local_claim_blocked and prior_local_blocked else "FAIL",
            "details": "GATE1392_5 and prior GATE1391_5 both block local GR/Newton promotion.",
        },
        {
            "validation_id": "VAL1392_5_scope",
            "check": "generated outputs stay inside post-checkpoint-work and outside formalization-workbench",
            "status": "PASS" if scope_ok else "FAIL",
            "details": f"ROOT={ROOT}; output_count={len(outputs)}; formalization_touched={formalization_touched}",
        },
        {
            "validation_id": "VAL1392_6_overall",
            "check": "overall 1392 validation",
            "status": "PASS" if overall else "FAIL",
            "details": "1392 writes a runner-compatible nonclaim bulk alpha template and verifies the R10 runner blocks it.",
        },
    ]


def write_doc(
    sources: list[dict[str, str]],
    zero: list[dict[str, str]],
    template: list[dict[str, str]],
    register: list[dict[str, str]],
    runner_summary: list[dict[str, str]],
    gates: list[dict[str, str]],
    decisions: list[dict[str, str]],
    next_target: list[dict[str, str]],
    validation: list[dict[str, str]],
) -> None:
    generated = datetime.now(timezone.utc).isoformat()
    body = f"""# 1392 - Y5 R10 RAB Bulk Alpha Template Beta Kernel Tail Fill Or Zero Proof

**Generated:** {generated}

**Current verdict:** the bulk R10 zero route is exact but unsigned. `alpha_bulk,ST(lambda)=0` follows if `beta_bulk,S=0`, `beta_bulk,T=0`, and `epsilon_tail(lambda)=0`, but those premises are not parent-signed or bounded.

**Discipline move:** create a runner-compatible nonclaim alpha template instead of scoring. The template exposes the beta source leg, beta test leg, `K_bulk,ST(lambda)`, `epsilon_tail(lambda)`, material pair, lambda units, source file, and claim flags; the existing R10 runner is required to reject it.

**Claim ceiling:** {CLAIM_CEILING}

## Source Register

{md_table(sources)}

## Beta / Kernel / Tail Zero Attempt

{md_table(zero)}

## Runner-Compatible Bulk Alpha Template

{md_table(template)}

## Template Register

{md_table(register)}

## R10 Runner Smoke Summary

{md_table(runner_summary)}

## Claim Gates

{md_table(gates)}

## Decision Ledger

{md_table(decisions)}

## Next Target

{md_table(next_target)}

## Validation

{md_table(validation)}
"""
    (ROOT / DOC_PATH).write_text(body, encoding="utf-8")


def main() -> None:
    sources = source_register_rows()
    zero = zero_attempt_rows()
    template = bulk_alpha_template_rows()
    register = template_register_rows()

    write_csv(BULK_ALPHA_TEMPLATE_PATH, template)
    runner_summary = runner_summary_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_target_rows()
    validation = validation_rows(sources, zero, template, register, runner_summary, gates)

    write_csv(SOURCE_REGISTER_PATH, sources)
    write_csv(ZERO_ATTEMPT_PATH, zero)
    write_csv(TEMPLATE_REGISTER_PATH, register)
    write_csv(RUNNER_SUMMARY_PATH, runner_summary)
    write_csv(CLAIM_GATE_PATH, gates)
    write_csv(DECISION_LEDGER_PATH, decisions)
    write_csv(NEXT_TARGET_PATH, next_target)
    write_csv(VALIDATION_PATH, validation)
    write_doc(sources, zero, template, register, runner_summary, gates, decisions, next_target, validation)

    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        raise SystemExit(f"1392 validation failed: {failed}")
    print(STATUS)
    print(ROOT / DOC_PATH)
    print(ROOT / VALIDATION_PATH)
    print(json.dumps({"runner_summary": runner_summary}, indent=2))


if __name__ == "__main__":
    main()
