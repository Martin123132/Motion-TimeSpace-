from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from R10_alpha_lambda_bound_prediction_runner import MTS_REQUIRED_COLUMNS, run_runner


STARTED = datetime.now(timezone.utc)
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
DOC = ROOT / "1059-Y5-R10-alpha-counterterm-product-prior-source-pack-and-cross-arena-gate.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_DIR = ROOT / "runs" / "1059-alpha-counterterm-product-prior-source-pack-smoke" / "results"
MTS_TEMPLATE = OUT / "R10_alpha_lambda_curve_MTS_1059_ALPHA_PRODUCT_PRIOR_TEMPLATE_NONCLAIM.csv"
BOUND_CANDIDATE = LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def flag(value: object) -> bool:
    return str(value).strip().lower() == "true"


def source_path(path_text: str) -> Path:
    path = Path(path_text)
    if path.is_absolute():
        return path
    return ROOT / path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def md_cell(value: object) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def md_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    return "\n".join(
        [
            "| " + " | ".join(columns) + " |",
            "| " + " | ".join("---" for _ in columns) + " |",
            *["| " + " | ".join(md_cell(row.get(column, "")) for column in columns) + " |" for row in rows],
        ]
    ) + "\n"


def source_register_rows() -> list[dict[str, str]]:
    specs = [
        ("SRC1059_0_1058_next", "source-intake/mts_residuals/P8_Y5_R10_1058_NEXT_TARGET.csv", "1059-Y5-R10-alpha-counterterm-product-prior-source-pack-and-cross-arena-gate.md", "1058 handoff."),
        ("SRC1059_1_1058_prior", "source-intake/mts_residuals/P8_Y5_R10_1058_ALPHA_COUNTERTERM_PRIOR_BRANCH.csv", "ACP1058_4_counterterm_policy", "alpha counterterm prior branch."),
        ("SRC1059_2_1058_cross", "source-intake/mts_residuals/P8_Y5_R10_1058_CROSS_ARENA_ALPHA_COUNTERTERM_LINKS.csv", "CAL1058_3_cross_arena_policy", "cross-arena product links."),
        ("SRC1059_3_1052_clock", "source-intake/mts_residuals/P8_Y5_R10_1052_ALPHA_CLOCK_PRODUCT_BOUND_LEDGER.csv", "ACB1052_2", "clock product bounds."),
        ("SRC1059_4_1052_WEP", "source-intake/mts_residuals/P8_Y5_R10_1052_ALPHA_WEP_PROJECTION_LEDGER.csv", "AWP1052_0_alpha_Coulomb", "WEP alpha product target."),
        ("SRC1059_5_1052_R10", "source-intake/mts_residuals/P8_Y5_R10_1052_ALPHA_R10_PROJECTION_LEDGER.csv", "RAP1052_0_product_law", "R10 product law and missing inputs."),
        ("SRC1059_6_1053_tau", "source-intake/mts_residuals/P8_Y5_R10_1053_TAU_WEP_R10_PROJECTION_AUDIT.csv", "TPR1053_4_verdict", "tau/source projection debts."),
        ("SRC1059_7_1053_KX", "source-intake/mts_residuals/P8_Y5_R10_1053_KX_ZX_PLACEHOLDER_LEDGER.csv", "KZ1053_3_KX_R10", "K_X/Z_X placeholder ledger."),
        ("SRC1059_8_1053_beta", "source-intake/mts_residuals/P8_Y5_R10_1053_BETA_SOURCE_ALPHA_DERIVATION_AUDIT.csv", "BSA1053_5_verdict", "beta_source_alpha blocked status."),
        ("SRC1059_9_1054_prior", "source-intake/mts_residuals/P8_Y5_R10_1054_NUMERIC_PRIOR_WIDTH_LEDGER.csv", "NPW1054_0_alpha_WEP_product", "numeric product-width ledger."),
        ("SRC1059_10_1057_retained", "source-intake/mts_residuals/P8_Y5_R10_1057_RETAINED_BRANCH_LEDGER.csv", "RB1057_0_clock", "retained branch rows."),
        ("SRC1059_11_R10_bound_candidate", "source-intake/local_bounds/R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv", "R10_VECTOR_2020_REVIEW_0000", "R10 review-candidate bound curve for smoke only."),
        ("SRC1059_12_R10_runner", "scripts/R10_alpha_lambda_bound_prediction_runner.py", "MTS_REQUIRED_COLUMNS", "existing R10 runner and schema."),
    ]
    rows: list[dict[str, str]] = []
    for source_id, path_text, needle, role in specs:
        path = source_path(path_text)
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            {
                "source_id": source_id,
                "source_path": str(path),
                "exists": str(exists).lower(),
                "needle": needle,
                "needle_found": str(needle in text).lower(),
                "role": role,
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def product_prior_pack_rows() -> list[dict[str, str]]:
    return [
        {
            "pack_id": "APP1059_0_clock_YbE3E2",
            "arena": "clock",
            "product_symbol": "P_clock_alpha := b_alpha*tau_clock_time",
            "source_row": "ACB1052_2",
            "bound_or_target": "abs(P_clock_alpha) <= 2.1e-18 yr^-1 at 1sigma; 3.2e-18 yr^-1 at 2sigma",
            "units": "yr^-1",
            "score_rule": "usable only as clock product; standalone b_alpha forbidden",
            "missing_for_standalone": "tau_clock_time parent derivation; Xhat/chi_X/readout normalization",
            "score_ready": "true_nonclaim_product_only",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "pack_id": "APP1059_1_clock_AlHg",
            "arena": "clock",
            "product_symbol": "P_clock_alpha := b_alpha*tau_clock_time",
            "source_row": "ACB1052_0",
            "bound_or_target": "abs(P_clock_alpha) <= 3.9e-17 yr^-1 at 1sigma; 6.2e-17 yr^-1 at 2sigma",
            "units": "yr^-1",
            "score_rule": "weaker cross-check row; product-only",
            "missing_for_standalone": "tau_clock_time parent derivation; Xhat/chi_X/readout normalization",
            "score_ready": "true_nonclaim_product_only",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "pack_id": "APP1059_2_WEP_alpha_Coulomb",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "P_WEP_alpha := beta_source_alpha*b_alpha*tau_WEP",
            "source_row": "AWP1052_0_alpha_Coulomb",
            "bound_or_target": "abs(P_WEP_alpha) <= 4.797780522732e-05 under the alpha/Coulomb smoke convention",
            "units": "dimensionless in current WEP smoke convention",
            "score_rule": "target for a predicted product; no standalone beta_source_alpha or b_alpha",
            "missing_for_standalone": "beta_source_alpha owner; tau_WEP; full material model; shared domain rule",
            "score_ready": "target_only_nonclaim",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "pack_id": "APP1059_3_WEP_surface_binding",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "P_WEP_surface := beta_source_or_binding*b_A*tau_WEP",
            "source_row": "AWP1052_1_surface_binding",
            "bound_or_target": "abs(P_WEP_surface) <= 2.887280314062e-05 if surface/binding branch survives",
            "units": "dimensionless in current WEP smoke convention",
            "score_rule": "robust target only; not an alpha-only pass",
            "missing_for_standalone": "binding coefficient owner; tau_WEP; full composition/material convention",
            "score_ready": "target_only_nonclaim",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "pack_id": "APP1059_4_R10_finite_alpha",
            "arena": "R10_short_range",
            "product_symbol": "P_R10_alpha(lambda) := K_X^R10(lambda)*beta_s(lambda)*beta_t(lambda)+epsilon_tail(lambda)",
            "source_row": "RAP1052_0_product_law; KZ1053_3_KX_R10",
            "bound_or_target": "abs(P_R10_alpha(lambda)) <= alpha_bound(lambda) only after promoted bound curve and sourced inputs",
            "units": "dimensionless alpha(lambda)",
            "score_rule": "currently schema-only; R10 runner must reject placeholders",
            "missing_for_standalone": "lambda_X; Z_X; K_X; tau_R10; beta_s; beta_t; promoted bound curve",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def no_transfer_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "NTG1059_0_clock_to_balpha",
            "forbidden_transfer": "clock product -> standalone b_alpha",
            "reason": "tau_clock_time is product-defined but not parent-derived",
            "allowed_use": "quote abs(b_alpha*tau_clock_time) bounds only",
            "missing_to_unlock": "tau_clock_time and Xhat/chi_X normalization",
            "gate_pass": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "NTG1059_1_clock_to_WEP",
            "forbidden_transfer": "clock product -> WEP source-force product",
            "reason": "WEP uses beta_source_alpha*b_alpha*tau_WEP, not b_alpha*tau_clock_time",
            "allowed_use": "compare only after parent map relates tau_clock_time to beta_source_alpha*tau_WEP",
            "missing_to_unlock": "beta_source_alpha owner; tau_WEP; shared normalization theorem",
            "gate_pass": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "NTG1059_2_clock_to_R10",
            "forbidden_transfer": "clock product -> R10 alpha(lambda)",
            "reason": "R10 needs source/test charges and K_X/Z_X/tau_R10, not clock drift alone",
            "allowed_use": "none for R10 scoring until finite branch inputs are sourced",
            "missing_to_unlock": "beta_s; beta_t; tau_R10; K_X/Z_X; lambda_X; promoted curve",
            "gate_pass": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "NTG1059_3_WEP_to_R10",
            "forbidden_transfer": "WEP target -> R10 pass",
            "reason": "composition DeltaQ WEP target and short-range torque alpha(lambda) have different kernels",
            "allowed_use": "shared beta/tau maps only if derived in one parent convention",
            "missing_to_unlock": "R10 profile/material projection and source/test beta split",
            "gate_pass": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def projection_debt_rows() -> list[dict[str, str]]:
    return [
        {
            "debt_id": "PD1059_0_tau_clock",
            "projection": "tau_clock_time",
            "status": "PRODUCT_MAP_NOT_PARENT_DERIVED",
            "source": "TPR1053_0_clock_product",
            "blocks": "standalone b_alpha",
            "next_required_input": "derive local time/readout projection for chi_X or keep product bound",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "debt_id": "PD1059_1_beta_source_alpha",
            "projection": "beta_source_alpha",
            "status": "OWNER_NOT_DERIVED",
            "source": "BSA1053_5_verdict",
            "blocks": "WEP product prediction and beta_source standalone prior",
            "next_required_input": "theorem-zero or source-backed numeric prior in one material convention",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "debt_id": "PD1059_2_tau_WEP",
            "projection": "tau_WEP",
            "status": "DEFINITION_REQUIRED_NOT_FOUND",
            "source": "TPR1053_1_tau_WEP_definition",
            "blocks": "WEP alpha product prediction",
            "next_required_input": "lab/source/orbit/material projection tensor",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "debt_id": "PD1059_3_tau_R10",
            "projection": "tau_R10",
            "status": "DEFINITION_ONLY",
            "source": "TPR1053_2_tau_R10_definition",
            "blocks": "R10 finite branch score",
            "next_required_input": "finite-source profile integral and readout trace convention",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "debt_id": "PD1059_4_KX_ZX_lambda",
            "projection": "K_X/Z_X/lambda_X",
            "status": "SYMBOLIC_CONDITIONAL",
            "source": "KZ1053_3_KX_R10",
            "blocks": "R10 alpha(lambda) prediction",
            "next_required_input": "parent finite-range branch and R10 harmonic kernel",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def product_score_rule_rows() -> list[dict[str, str]]:
    return [
        {
            "rule_id": "PSR1059_0_product_only",
            "rule": "a row with a product_symbol may only score that exact product",
            "effect": "prevents product bound from being divided by assumed tau/source factors",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "rule_id": "PSR1059_1_no_unity_tau",
            "rule": "tau_clock, tau_WEP, and tau_R10 cannot be set to unity by convention",
            "effect": "blocks unit-rescaling shortcuts",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "rule_id": "PSR1059_2_no_cancellation",
            "rule": "counterterm components are absolute/no-cancellation until a signed parent relation exists",
            "effect": "prevents hiding WEP/R10 pressure by branch cancellation",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "rule_id": "PSR1059_3_claim_validity",
            "rule": "valid_for_claim may become true only when product prediction and bound are numeric, sourced, unit-matched, and projection-owned",
            "effect": "keeps smoke rows private/nonclaim",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC1059_0_pack_status",
            "decision": "alpha counterterm branch is now a product-prior pack",
            "because": "clock and WEP have source-backed product bounds/targets, while R10 has a schema and missing inputs",
            "next_action": "use product-only rows for future tests",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1059_1_claim_status",
            "decision": "no standalone b_alpha, beta_source_alpha, WEP pass, or R10 pass",
            "because": "tau/source/K_X/Z_X projections are not parent-derived",
            "next_action": "keep claim gates blocked",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1059_2_best_next",
            "decision": "next target is the first scoreable product-prediction runner",
            "because": "the product-prior pack exists, but MTS does not yet predict the products numerically",
            "next_action": "1060-Y5-R10-alpha-product-prediction-stub-runner-and-required-inputs.md",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def claim_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "CG1059_0_standalone_balpha",
            "claim": "standalone b_alpha is known",
            "gate_pass": "false",
            "reason": "only clock product bound exists",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1059_1_beta_source_alpha",
            "claim": "standalone beta_source_alpha is known",
            "gate_pass": "false",
            "reason": "only WEP product target exists and source owner is not derived",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1059_2_WEP",
            "claim": "WEP alpha branch passes",
            "gate_pass": "false",
            "reason": "no MTS product prediction below 4.797780522732e-05 is sourced",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1059_3_R10",
            "claim": "R10 alpha(lambda) branch passes",
            "gate_pass": "false",
            "reason": "finite branch inputs and promoted bound curve are missing",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1059_4_cross_arena",
            "claim": "clock/WEP/R10 products can be transferred",
            "gate_pass": "false",
            "reason": "shared parent normalization map is missing",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_target": "1060-Y5-R10-alpha-product-prediction-stub-runner-and-required-inputs.md",
            "objective": "build the first product-prediction runner schema for the retained alpha counterterm branch, listing exactly which numeric MTS inputs would be needed to compare clock, WEP, and R10 products without claiming a pass",
            "include": "product prediction CSV schema, required tau/source/KX inputs, strict missing-input failure modes, product-only comparison rows, runner refusal smoke",
            "exclude": "standalone b_alpha claim, guessed tau values, unity shortcuts, cancellation, public local-GR/R10/WEP/clock claim, GitHub action, formalization-workbench edits",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def mts_template_rows() -> list[dict[str, str]]:
    row = {
        "model_id": "MTS_source_normalized_Newton_branch",
        "branch_id": "alpha_product_prior_pack_template",
        "curve_id": "MTS_1059_alpha_product_prior_nonclaim",
        "lambda_value": "MISSING_R10_LAMBDA_X",
        "lambda_units": "m",
        "alpha_predicted": "MISSING_R10_PRODUCT_PREDICTION",
        "alpha_bound": "MISSING_PROMOTED_BOUND",
        "alpha_bound_source": str(BOUND_CANDIDATE),
        "force_law_form": "clock bounds b_alpha*tau_clock; WEP targets beta_source_alpha*b_alpha*tau_WEP; R10 needs K_X^R10 beta_s beta_t + epsilon_tail",
        "derivation_status": "template_invalid_product_prior_pack_nonclaim",
        "formula_reference": "P8_Y5_R10_1059_ALPHA_PRODUCT_PRIOR_PACK.csv",
        "source_file": "source-intake/mts_residuals/P8_Y5_R10_1059_ALPHA_PRODUCT_PRIOR_PACK.csv",
        "assumptions": "nonclaim placeholder; product-only; no standalone b_alpha; no tau unity; no cancellation",
        "valid_for_claim": "false",
        "notes": "Runner must refuse this row until a numeric R10 product prediction and claim-valid bound data exist.",
    }
    return [{column: row[column] for column in MTS_REQUIRED_COLUMNS}]


def runner_smoke_rows(status: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "smoke_id": "SMOKE1059_0_R10_runner_refusal",
            "valid_mts_rows": str(status.get("valid_mts_rows", "")),
            "valid_bound_rows": str(status.get("valid_bound_rows", "")),
            "comparison_rows": str(status.get("comparison_rows", "")),
            "R10_pass_for_claim": str(status.get("R10_pass_for_claim", "")).lower(),
            "claim_allowed": str(status.get("claim_allowed", "")).lower(),
            "expected_result": "reject alpha-product placeholders until prediction inputs are sourced",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def refusal_rows(status: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "refusal_id": "REF1059_0_standalone",
            "object": "standalone alpha counterterm constants",
            "current_status": "PRODUCT_ONLY_NONCLAIM",
            "refusal_status": "blocked",
            "failure_reasons": "tau/source projections missing; product rows cannot be divided into standalone constants",
            "score_eligible": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "refusal_id": "REF1059_1_cross_arena",
            "object": "clock/WEP/R10 transfer",
            "current_status": "NO_TRANSFER_WITHOUT_PARENT_MAP",
            "refusal_status": "blocked",
            "failure_reasons": "tau_clock, tau_WEP, tau_R10, beta_source, and K_X/Z_X are not related by parent theorem",
            "score_eligible": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "refusal_id": "REF1059_2_R10_runner",
            "object": "R10 alpha-product smoke row",
            "current_status": "runner_refusal_expected",
            "refusal_status": "blocked",
            "failure_reasons": f"valid_mts_rows={status.get('valid_mts_rows')}; valid_bound_rows={status.get('valid_bound_rows')}",
            "score_eligible": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def count_formalization_modified_since_start() -> int:
    if not FORMALIZATION.exists():
        return 0
    count = 0
    start_time = STARTED.timestamp()
    for path in FORMALIZATION.rglob("*"):
        try:
            if path.is_file() and path.stat().st_mtime > start_time:
                count += 1
        except OSError:
            continue
    return count


def validate_outputs(
    outputs: dict[str, Path],
    source_rows: list[dict[str, str]],
    pack_rows: list[dict[str, str]],
    transfer_rows: list[dict[str, str]],
    debt_rows: list[dict[str, str]],
    rule_rows: list[dict[str, str]],
    template_rows: list[dict[str, str]],
    runner_status: dict[str, Any],
    claim_rows: list[dict[str, str]],
    next_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    checks: list[dict[str, str]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        checks.append({"check_id": check_id, "result": "pass" if passed else "fail", "detail": detail, "generated_utc": stamp()})

    source_ok = all(flag(row.get("exists", "")) and flag(row.get("needle_found", "")) for row in source_rows)
    add("V1059_1_sources_exist_and_needles", source_ok, "every cited source path exists and every source needle was found")
    clock_ok = any(row.get("pack_id") == "APP1059_0_clock_YbE3E2" and "2.1e-18" in row.get("bound_or_target", "") for row in pack_rows)
    wep_ok = any(row.get("pack_id") == "APP1059_2_WEP_alpha_Coulomb" and "4.797780522732e-05" in row.get("bound_or_target", "") for row in pack_rows)
    add("V1059_2_product_pack_contains_clock_and_WEP", clock_ok and wep_ok, "clock and WEP product rows are present")
    r10_blocked = any(row.get("pack_id") == "APP1059_4_R10_finite_alpha" and row.get("score_ready") == "false" for row in pack_rows)
    add("V1059_3_R10_schema_blocked", r10_blocked, "R10 product row is schema-only and blocked")
    transfer_blocked = transfer_rows and all(row.get("gate_pass") == "false" for row in transfer_rows)
    add("V1059_4_transfer_gates_blocked", transfer_blocked, "all cross-arena transfer gates are blocked")
    debts_present = len(debt_rows) >= 5 and all(row.get("valid_for_claim") == "false" for row in debt_rows)
    add("V1059_5_projection_debts_present", debts_present, "tau/source/KX projection debts are explicit")
    product_rules = rule_rows and all(row.get("claim_allowed") == "false" for row in rule_rows)
    add("V1059_6_product_score_rules_nonclaim", product_rules, "product-only score rules block standalone claims")
    template_schema = set(MTS_REQUIRED_COLUMNS).issubset(set(template_rows[0].keys())) if template_rows else False
    template_nonclaim = template_schema and all(row.get("valid_for_claim") == "false" for row in template_rows)
    add("V1059_7_mts_template_schema_nonclaim", template_nonclaim, "MTS template has runner schema and no claim-valid rows")
    runner_refused = runner_status.get("valid_mts_rows") == 0 and runner_status.get("claim_allowed") is False
    add("V1059_8_runner_smoke_refuses_claim", runner_refused, "existing R10 runner refuses the 1059 placeholder rows")
    claims_blocked = claim_rows and all(row.get("gate_pass") == "false" and row.get("claim_allowed") == "false" for row in claim_rows)
    add("V1059_9_claim_gates_blocked", claims_blocked, "all standalone/WEP/R10/cross-arena claim gates remain blocked")
    next_ok = bool(next_rows) and next_rows[0].get("next_target", "").startswith("1060-Y5-R10-alpha-product")
    add("V1059_10_next_target_written", next_ok, "next target row is present")
    generated_inside = all(ROOT in path.resolve().parents or path.resolve() == ROOT for path in outputs.values())
    add("V1059_11_generated_files_in_post_checkpoint", generated_inside, "all generated files are under post-checkpoint-work")
    formalization_count = count_formalization_modified_since_start()
    add("V1059_12_formalization_untouched", formalization_count == 0, f"formalization-workbench modified-file count since script start is {formalization_count}")

    summary_pass = all(row["result"] == "pass" for row in checks)
    checks.insert(0, {"check_id": "V1059_SUMMARY", "result": "pass" if summary_pass else "fail", "detail": "1059 alpha counterterm product-prior source pack validation summary", "generated_utc": stamp()})
    return checks


def write_doc(
    source_rows: list[dict[str, str]],
    pack_rows: list[dict[str, str]],
    transfer_rows: list[dict[str, str]],
    debt_rows: list[dict[str, str]],
    rule_rows: list[dict[str, str]],
    decisions: list[dict[str, str]],
    template_rows: list[dict[str, str]],
    smoke_rows: list[dict[str, str]],
    refusal_rows_: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    validation_rows: list[dict[str, str]],
    next_rows: list[dict[str, str]],
) -> None:
    text = "\n".join(
        [
            "# 1059 Y5 R10 alpha counterterm product prior source pack and cross arena gate",
            "",
            "**Progress:** the retained alpha counterterm branch is now a product-prior source pack. Clock and WEP have concrete source-backed product bounds/targets; R10 has the finite-branch schema but remains unscoreable.",
            "",
            "**Current verdict:** useful for testing discipline, not a pass. The pack forbids standalone `b_alpha`, standalone `beta_source_alpha`, clock-to-WEP transfer, and clock-to-R10 transfer unless the missing projections are derived.",
            "",
            "**Next move:** build a product-prediction runner schema. That runner should fail until actual MTS inputs for `tau_clock`, `tau_WEP`, `tau_R10`, `beta_s/beta_t`, and `K_X/Z_X` are supplied.",
            "",
            "## Source register",
            md_table(source_rows, ["source_id", "source_path", "exists", "needle_found", "role"]),
            "",
            "## Alpha product-prior source pack",
            md_table(pack_rows, ["pack_id", "arena", "product_symbol", "bound_or_target", "units", "score_rule", "missing_for_standalone", "score_ready", "valid_for_claim"]),
            "",
            "## No-transfer gates",
            md_table(transfer_rows, ["gate_id", "forbidden_transfer", "reason", "allowed_use", "missing_to_unlock", "gate_pass", "valid_for_claim"]),
            "",
            "## Projection debt ledger",
            md_table(debt_rows, ["debt_id", "projection", "status", "source", "blocks", "next_required_input", "valid_for_claim"]),
            "",
            "## Product-only score rules",
            md_table(rule_rows, ["rule_id", "rule", "effect", "claim_allowed", "valid_for_claim"]),
            "",
            "## Decision ledger",
            md_table(decisions, ["decision_id", "decision", "because", "next_action", "valid_for_claim"]),
            "",
            "## MTS R10 smoke template",
            md_table(template_rows, ["model_id", "branch_id", "lambda_value", "alpha_predicted", "force_law_form", "derivation_status", "valid_for_claim"]),
            "",
            "## Runner smoke status",
            md_table(smoke_rows, ["smoke_id", "valid_mts_rows", "valid_bound_rows", "comparison_rows", "R10_pass_for_claim", "claim_allowed", "expected_result"]),
            "",
            "## Placeholder refusal runner",
            md_table(refusal_rows_, ["refusal_id", "object", "current_status", "refusal_status", "failure_reasons", "score_eligible", "claim_allowed"]),
            "",
            "## Claim gates",
            md_table(claim_rows, ["gate_id", "claim", "gate_pass", "reason", "claim_allowed", "valid_for_claim"]),
            "",
            "## Validation",
            md_table(validation_rows, ["check_id", "result", "detail", "generated_utc"]),
            "",
            "## Next target",
            md_table(next_rows, ["next_target", "objective", "include", "exclude", "valid_for_claim"]),
            "",
        ]
    )
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    source_rows = source_register_rows()
    pack_rows = product_prior_pack_rows()
    transfer_rows = no_transfer_gate_rows()
    debt_rows = projection_debt_rows()
    rule_rows = product_score_rule_rows()
    decisions = decision_rows()
    claim_rows = claim_gate_rows()
    next_rows = next_target_rows()
    template_rows = mts_template_rows()

    outputs: dict[str, Path] = {
        "source_register": OUT / "P8_Y5_R10_1059_SOURCE_REGISTER.csv",
        "pack": OUT / "P8_Y5_R10_1059_ALPHA_PRODUCT_PRIOR_PACK.csv",
        "transfer": OUT / "P8_Y5_R10_1059_NO_TRANSFER_GATES.csv",
        "debt": OUT / "P8_Y5_R10_1059_PROJECTION_DEBT_LEDGER.csv",
        "rules": OUT / "P8_Y5_R10_1059_PRODUCT_ONLY_SCORE_RULES.csv",
        "decisions": OUT / "P8_Y5_R10_1059_DECISION_LEDGER.csv",
        "claim_gates": OUT / "P8_Y5_R10_1059_CLAIM_GATES.csv",
        "next_target": OUT / "P8_Y5_R10_1059_NEXT_TARGET.csv",
        "mts_template": MTS_TEMPLATE,
        "runner_smoke": OUT / "P8_Y5_R10_1059_RUNNER_SMOKE_STATUS.csv",
        "placeholder_refusal": OUT / "P8_Y5_R10_1059_PLACEHOLDER_REFUSAL_RUNNER.csv",
        "validation": OUT / "P8_Y5_BRR545_1059_VALIDATION.csv",
        "doc": DOC,
    }

    write_csv(outputs["source_register"], source_rows)
    write_csv(outputs["pack"], pack_rows)
    write_csv(outputs["transfer"], transfer_rows)
    write_csv(outputs["debt"], debt_rows)
    write_csv(outputs["rules"], rule_rows)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["claim_gates"], claim_rows)
    write_csv(outputs["next_target"], next_rows)
    write_csv(outputs["mts_template"], template_rows, MTS_REQUIRED_COLUMNS)

    runner_result = run_runner(MTS_TEMPLATE, BOUND_CANDIDATE, RUN_DIR)
    runner_status = runner_result["status"]
    smoke_rows = runner_smoke_rows(runner_status)
    refusal_rows_ = refusal_rows(runner_status)
    write_csv(outputs["runner_smoke"], smoke_rows)
    write_csv(outputs["placeholder_refusal"], refusal_rows_)

    validation_rows = validate_outputs(
        outputs,
        source_rows,
        pack_rows,
        transfer_rows,
        debt_rows,
        rule_rows,
        template_rows,
        runner_status,
        claim_rows,
        next_rows,
    )
    write_csv(outputs["validation"], validation_rows)
    write_doc(
        source_rows,
        pack_rows,
        transfer_rows,
        debt_rows,
        rule_rows,
        decisions,
        template_rows,
        smoke_rows,
        refusal_rows_,
        claim_rows,
        validation_rows,
        next_rows,
    )

    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    failed = [row for row in validation_rows if row["result"] != "pass"]
    print(f"wrote {DOC}")
    print(f"validation: {'PASS' if not failed else 'FAIL'}")
    for row in failed:
        print(f"{row['check_id']}: {row['detail']}")


if __name__ == "__main__":
    main()
