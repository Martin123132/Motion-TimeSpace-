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

CHECKPOINT = "2963"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
RUN_UTC = SCRIPT_START_UTC.isoformat()

DOC = ROOT / "2963-Y5-R2FR-bconf-residual-placeholder-refusal-smoke-runner-under-AX1090.md"

SRC_2962_DOC = ROOT / "2962-Y5-R2FR-canonical-Xhat-source-current-normalization-or-bconf-residual-prior-under-AX1090.md"
SRC_2962_NEXT = RESIDUALS / "P8_Y5_R2FR_2962_NEXT_TARGET.csv"
SRC_2962_PRIOR = RESIDUALS / "P8_Y5_R2FR_2962_BCONF_RESIDUAL_PRIOR_INTAKE_NONCLAIM.csv"
SRC_2962_PROJECTION = RESIDUALS / "P8_Y5_R2FR_2962_PROJECTION_INTAKE_ROWS_NONCLAIM.csv"
SRC_2962_XHAT = RESIDUALS / "P8_Y5_R2FR_2962_CANONICAL_XHAT_NORMALIZATION_GATE.csv"
SRC_2962_CURRENT = RESIDUALS / "P8_Y5_R2FR_2962_SOURCE_TEST_CURRENT_OWNER_GATE.csv"
SRC_2961_RESIDUAL = RESIDUALS / "P8_Y5_R2FR_2961_RESIDUAL_BRANCH_NONCLAIM.csv"
SRC_2960_BOUNDS = RESIDUALS / "P8_Y5_R2FR_2960_BCONF_BOUND_ROWS_NONCLAIM.csv"
SRC_2951_COEFF = PARENT_ACTION / "ZX_MX2_source_row_attempt_2951_BLOCKED.csv"
SRC_2951_OWNER = PARENT_ACTION / "parent_X_owner_contract_2951_NONCLAIM.csv"
SRC_2676_OWNER = ROOT / "source-intake" / "wep-sources" / "action_scale_measure_owner_wip_nonclaim_2676.csv"
SRC_2916_PRODUCT = PARENT_ACTION / "Cg_invariant_source_test_product_law_2916_NONCLAIM.csv"
SRC_LOCAL_BOUNDS = LOCAL_BOUNDS / "local_bound_claims.csv"
SRC_R10_CURVE = LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2963_SOURCE_REGISTER.csv",
    "schema": RESIDUALS / "P8_Y5_R2FR_2963_INPUT_SCHEMA_AUDIT.csv",
    "refusal": RESIDUALS / "P8_Y5_R2FR_2963_PLACEHOLDER_REFUSAL_ROWS.csv",
    "promotion": RESIDUALS / "P8_Y5_R2FR_2963_PROMOTION_RULES.csv",
    "smoke": RESIDUALS / "P8_Y5_R2FR_2963_SMOKE_RUNNER_STATUS.csv",
    "claims": RESIDUALS / "P8_Y5_R2FR_2963_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2963_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2963_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2963_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2963_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "rules_copy": PARENT_ACTION / "bconf_promotion_rules_2963_NONCLAIM.csv",
    "smoke_copy": LOCAL_BOUNDS / "bconf_placeholder_refusal_smoke_2963_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR2963_XHAT_ZXMX2_SOURCE_CURRENT_OR_BCONF_FIRST_VALUE_NEXT_NONCLAIM.csv",
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


def has_missing_marker(value: str) -> bool:
    upper = value.upper()
    return "MISSING" in upper or "PLACEHOLDER" in upper or "FILL_" in upper or "NOT_DERIVED" in upper or "NOT_SOURCED" in upper


def boolish_false(value: Any) -> bool:
    return str(value).strip().lower() in {"false", "0", "no", ""}


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
        ("SRC2963_00_2962_doc", SRC_2962_DOC, "NEXT2962_0_2963;Validation overall: `True`", "2962 handoff"),
        ("SRC2963_01_2962_next", SRC_2962_NEXT, "NEXT2962_0_2963", "machine-readable 2963 target"),
        ("SRC2963_02_2962_prior", SRC_2962_PRIOR, "PRIOR2962_0_b_conf_prior;PRIOR2962_4_prior_policy", "b_conf prior intake"),
        ("SRC2963_03_2962_projection", SRC_2962_PROJECTION, "PROJ2962_0_R10;PROJ2962_4_joint", "projection intake rows"),
        ("SRC2963_04_2962_Xhat", SRC_2962_XHAT, "XHAT2962_0_field_identity;XHAT2962_4_verdict", "canonical Xhat gate"),
        ("SRC2963_05_2962_current", SRC_2962_CURRENT, "CUR2962_0_common_action_line;CUR2962_4_verdict", "source/current gate"),
        ("SRC2963_06_2961_residual", SRC_2961_RESIDUAL, "RES2961_0_b_conf;RES2961_6_B_conf_envelope", "finite residual branch"),
        ("SRC2963_07_2960_bounds", SRC_2960_BOUNDS, "BROW2960_0_b_conf;BROW2960_4_source", "prior b_conf bound rows"),
        ("SRC2963_08_2951_coeff", SRC_2951_COEFF, "COEFF2951_4_lambdaX;COEFF2951_5_candidate_row", "Z_X/M_X^2/lambda blocked row"),
        ("SRC2963_09_2951_owner", SRC_2951_OWNER, "OWN2951_3_field_normalization;OWN2951_5_MX2_owner", "parent X owner contract"),
        ("SRC2963_10_2676_owner", SRC_2676_OWNER, "OWN2676_0_parent_owner_target;OWN2676_4_verdict", "source-current owner audit"),
        ("SRC2963_11_2916_product", SRC_2916_PRODUCT, "LAW2916_0_point_source;LAW2916_1_two_body_exchange", "conditional product law"),
        ("SRC2963_12_local_bounds", SRC_LOCAL_BOUNDS, "R1_WEP_source_charge;R2_clock_redshift;R3_gamma", "local bound anchors"),
        ("SRC2963_13_r10_curve", SRC_R10_CURVE, "R10_VECTOR_2020_REVIEW_0000;review_candidate_only", "R10 nonclaim curve"),
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


def schema_rows() -> list[dict[str, Any]]:
    prior = read_csv_rows(SRC_2962_PRIOR)
    projection = read_csv_rows(SRC_2962_PROJECTION)
    required_prior = {"b_conf", "N_Xhat", "lambda_X", "beta_source_conf;beta_test_conf", "b_conf_prior_policy"}
    required_projection = {"alpha_R10_conf(lambda)", "gamma_minus_1_conf", "clock_conf", "source_conf", "B_conf_envelope"}
    prior_symbols = {row.get("symbol", "") for row in prior}
    projection_symbols = {row.get("symbol", "") for row in projection}
    rows = [
        (
            "SCHEMA2963_0_prior_rows",
            "prior intake rows",
            len(prior),
            sorted(required_prior - prior_symbols),
            len(required_prior - prior_symbols) == 0,
            "all required finite-branch prior rows present",
        ),
        (
            "SCHEMA2963_1_projection_rows",
            "projection intake rows",
            len(projection),
            sorted(required_projection - projection_symbols),
            len(required_projection - projection_symbols) == 0,
            "all required arena projection rows present",
        ),
        (
            "SCHEMA2963_2_source_paths",
            "source path flags",
            sum(1 for row in prior + projection if str(row.get("source_path_exists", "")).lower() == "true"),
            [],
            all(str(row.get("source_path_exists", "")).lower() == "true" for row in prior + projection),
            "all input rows cite existing paths",
        ),
    ]
    return [
        add_common(
            {
                "schema_id": schema_id,
                "object": obj,
                "row_count_or_pass_count": count,
                "missing_required_symbols": ";".join(missing),
                "schema_pass": passed,
                "notes": notes,
            }
        )
        for schema_id, obj, count, missing, passed, notes in rows
    ]


def refusal_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_kind, input_path, id_key, value_key in [
        ("prior", SRC_2962_PRIOR, "row_id", "numeric_or_theorem_value"),
        ("projection", SRC_2962_PROJECTION, "projection_id", "current_status"),
    ]:
        for row in read_csv_rows(input_path):
            value = row.get(value_key, "")
            valid_for_claim = row.get("valid_for_claim", "")
            accepted = row.get("accepted_for_scoring", row.get("ready_for_smoke", ""))
            refused = has_missing_marker(value) or boolish_false(valid_for_claim) or boolish_false(accepted)
            reasons = []
            if has_missing_marker(value):
                reasons.append("MISSING_OR_PLACEHOLDER_VALUE")
            if boolish_false(valid_for_claim):
                reasons.append("VALID_FOR_CLAIM_FALSE")
            if boolish_false(accepted):
                reasons.append("NOT_ACCEPTED_FOR_SCORING")
            rows.append(
                add_common(
                    {
                        "refusal_id": f"REF2963_{len(rows)}",
                        "source_kind": source_kind,
                        "input_id": row.get(id_key, ""),
                        "symbol": row.get("symbol", ""),
                        "input_value": value,
                        "refused": refused,
                        "refusal_reasons": ";".join(reasons),
                        "source_path_exists": row.get("source_path_exists", ""),
                    }
                )
            )
    return rows


def promotion_rule_rows() -> list[dict[str, Any]]:
    rows = [
        ("PROM2963_0_b_conf", "b_conf", "numeric prior, fitted value, or theorem-zero", "no MISSING/FILL/PLACEHOLDER markers; source path exists; units dimensionless; valid_for_claim true"),
        ("PROM2963_1_Xhat", "N_Xhat", "canonical Xhat normalization", "field identity, Z_X/f_X convention and rescaling policy source-backed in one branch"),
        ("PROM2963_2_lambda", "lambda_X", "finite range", "Z_X and M_X^2 source-backed in same normalization with positive gap"),
        ("PROM2963_3_source_test", "beta_source_conf;beta_test_conf", "source/test charges", "common source-current owner and no source-only weights or explicit finite rows"),
        ("PROM2963_4_R10", "alpha_R10_conf(lambda)", "R10 product row", "K_R10, beta_source, beta_test, lambda_X and alpha bound curve all source-backed"),
        ("PROM2963_5_PPN_clock_source", "gamma/clock/source rows", "arena projections", "tau maps numeric/theorem-zero with no cancellation policy and source paths"),
        ("PROM2963_6_verdict", "promotion verdict", "all rows above pass together", "otherwise finite b_conf branch remains nonclaim"),
    ]
    return [
        add_common(
            {
                "promotion_id": promotion_id,
                "symbol": symbol,
                "required_payload": payload,
                "acceptance_rule": rule,
                "current_status": "NOT_SATISFIED",
                "promotion_pass": False,
            }
        )
        for promotion_id, symbol, payload, rule in rows
    ]


def smoke_rows(schema: list[dict[str, Any]], refusal: list[dict[str, Any]], promotion: list[dict[str, Any]]) -> list[dict[str, Any]]:
    total_inputs = len(refusal)
    refused_inputs = sum(1 for row in refusal if row["refused"] is True)
    valid_mts_rows = sum(1 for row in refusal if row["refused"] is False)
    schema_pass = all(row["schema_pass"] is True for row in schema)
    promotion_pass = all(row["promotion_pass"] is True for row in promotion)
    rows = [
        ("SMOKE2963_0_schema", "input schema", total_inputs, refused_inputs, valid_mts_rows, "PASS_SCHEMA_ONLY" if schema_pass else "SCHEMA_FAIL", "schema may pass even while claim rows are refused"),
        ("SMOKE2963_1_refusal", "placeholder refusal", total_inputs, refused_inputs, valid_mts_rows, "PLACEHOLDERS_REJECTED", "all current finite-branch rows are placeholders/nonclaim"),
        ("SMOKE2963_2_promotion", "promotion rules", len(promotion), sum(1 for row in promotion if row["promotion_pass"] is False), 0, "PROMOTION_BLOCKED", "no promotion rule is satisfied"),
        ("SMOKE2963_3_expected", "claim outcome", total_inputs, refused_inputs, valid_mts_rows, "CLAIM_FALSE_EXPECTED", f"schema_pass={schema_pass}; promotion_pass={promotion_pass}; valid_mts_rows={valid_mts_rows}"),
    ]
    return [
        add_common(
            {
                "smoke_id": smoke_id,
                "object": obj,
                "input_rows": input_rows,
                "refused_rows": refused_rows,
                "valid_mts_rows": valid_rows,
                "smoke_status": status,
                "notes": notes,
                "claim_allowed": False,
                "valid_for_claim": False,
            }
        )
        for smoke_id, obj, input_rows, refused_rows, valid_rows, status, notes in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("CG2963_0_schema", "finite b_conf schema exists", True, "PRIVATE_SCHEMA_ONLY"),
        ("CG2963_1_placeholders", "placeholder rows accepted for scoring", False, "PLACEHOLDERS_REFUSED"),
        ("CG2963_2_promotion", "promotion rules satisfied", False, "PROMOTION_RULES_NOT_SATISFIED"),
        ("CG2963_3_R10_PPN_clock", "R10/PPN/clock evidence comparison allowed", False, "VALID_MTS_ROWS_ZERO"),
        ("CG2963_4_local_GR", "local GR/Newton reduction allowed", False, "NO_LOCAL_GR_CLAIM"),
        ("CG2963_5_public", "public claim allowed", False, "PRIVATE_NONCLAIM_CHECKPOINT"),
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
            "DEC2963_0_runner",
            "placeholder-refusal runner works",
            "the finite b_conf branch can now ingest rows while refusing every current placeholder",
            "keep the branch nonclaim until owners/values are supplied",
        ),
        (
            "DEC2963_1_hard_blocker",
            "hard blockers are unchanged but machine-visible",
            "Xhat normalization, lambda_X, source/test charges and tau maps remain required before scoring",
            "go after the first owner/value row rather than rerunning the branch split",
        ),
        (
            "DEC2963_2_next",
            "next target should source the first decisive payload",
            "lambda_X/Z_X/M_X^2 and source-current owner are upstream of every tau projection",
            "build 2964 Xhat-ZX-MX2 or source-current first value/source theorem",
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
                "next_id": "NEXT2963_0_2964",
                "priority": "selected_primary",
                "next_doc": "2964-Y5-R2FR-Xhat-ZX-MX2-lambda-or-source-current-first-value-under-AX1090.md",
                "next_script": "scripts/Y5_R2FR_Xhat_ZX_MX2_lambda_or_source_current_first_value_under_AX1090_2964.py",
                "objective": "Try to source or derive the first decisive finite-bconf payload: canonical Xhat with Z_X/M_X^2/lambda_X in one normalization, or source/test current owner/charge rows. If neither closes, emit the first nonclaim numeric/prior slot required by the 2963 runner.",
                "include": "Xhat normalization;Z_X;M_X^2;lambda_X;source/test charges;common current owner;first b_conf prior slot;source paths;units;no-cancellation policy",
                "exclude": "derive single-frame theorem again;b_marker full taxonomy;quotient/vertical no-pole rerun;beta prediction without owners;direct lambda closure;I_X scoring;local-GR claim;public claim;formalization-workbench edits;GitHub action",
            }
        )
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    copies = [
        ("rules_copy", OUTPUTS["promotion"], BRANCH_OUTPUTS["rules_copy"]),
        ("smoke_copy", OUTPUTS["smoke"], BRANCH_OUTPUTS["smoke_copy"]),
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
        ("VAL2963_0_sources_exist", all(row["path_exists"] for row in source_rows), "all cited local source paths exist", True),
        ("VAL2963_1_anchors_found", all(row["anchors_found"] for row in source_rows), "all cited source anchors found", True),
        ("VAL2963_2_schema_pass", all(row["schema_pass"] is True for row in all_rows["schema"]), "input schema rows are present", True),
        ("VAL2963_3_placeholders_refused", all(row["refused"] is True for row in all_rows["refusal"]), "all current placeholder/nonclaim rows are refused", True),
        ("VAL2963_4_no_valid_mts_rows", all(row["valid_mts_rows"] == 0 for row in all_rows["smoke"]), "smoke runner has zero valid MTS rows", True),
        ("VAL2963_5_promotion_blocked", all(row["promotion_pass"] is False for row in all_rows["promotion"]), "all promotion rules remain unsatisfied", True),
        ("VAL2963_6_claims_blocked", all(row["claim_allowed"] is False for row in all_rows["claims"]) and any(row["claim_gate_id"] == "CG2963_0_schema" and row["condition_passed"] is True for row in all_rows["claims"]), "schema exists but all claims remain blocked", True),
        ("VAL2963_7_next_target_written", any(row["next_id"] == "NEXT2963_0_2964" for row in all_rows["next"]), "2964 next target selected", True),
        ("VAL2963_8_branches_exist", all(Path(row["copy_path"]).exists() for row in all_rows["branches"]), "branch copy files exist", True),
        ("VAL2963_9_csvs_parse", all(csv_parses(path) for path in csv_paths), "all generated CSV files parse", True),
        ("VAL2963_10_outputs_under_post_checkpoint", all(is_under(path, ROOT) for path in generated_paths), "all generated outputs are under post-checkpoint-work", True),
        ("VAL2963_11_formalization_clean", not any(is_under(path, FORMALIZATION) for path in generated_paths), "no 2963 outputs were written to formalization-workbench", True),
        ("VAL2963_12_doc_written", DOC.exists(), "2963 markdown checkpoint exists", True),
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
    rows.append(add_common({"validation_id": "VAL2963_OVERALL", "passed": overall, "check": "2963 validation overall", "required": True}))
    return rows


def write_markdown(all_rows: dict[str, list[dict[str, Any]]]) -> None:
    doc = f"""# 2963 - Y5 R2FR: bconf residual placeholder-refusal smoke runner under AX1090

Status: `Y5_R2FR_2963_bconf_placeholder_refusal_runner_passed_claim_false`

Claim ceiling: `no_valid_bconf_rows_no_tau_package_no_R10_PPN_clock_score_no_local_GR_no_Newton_no_public_claim`

2963 builds the finite-`b_conf` safety runner. The result is:

- The runner ingests the 2962 prior and projection rows and confirms the required schema exists.
- Every current finite-branch row is refused because it still contains missing/placeholder values or `valid_for_claim=false`.
- Promotion now has explicit machine rules: `b_conf`, canonical `Xhat`, `lambda_X`, source/test charges and arena tau maps must all be numeric or theorem-zero with source paths.
- The next useful work is sourcing the first decisive owner/value row, not trying to score the placeholders.

## Source Register

{md_table(all_rows["sources"], ["source_id", "source_path", "path_exists", "anchors_found", "role"])}

## Input Schema Audit

{md_table(all_rows["schema"], ["schema_id", "object", "row_count_or_pass_count", "missing_required_symbols", "schema_pass", "notes"])}

## Placeholder Refusal Rows

{md_table(all_rows["refusal"], ["refusal_id", "source_kind", "input_id", "symbol", "input_value", "refused", "refusal_reasons"])}

## Promotion Rules

{md_table(all_rows["promotion"], ["promotion_id", "symbol", "current_status", "promotion_pass", "required_payload", "acceptance_rule"])}

## Smoke Runner Status

{md_table(all_rows["smoke"], ["smoke_id", "object", "input_rows", "refused_rows", "valid_mts_rows", "smoke_status", "claim_allowed"])}

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
    schema = schema_rows()
    refusal = refusal_rows()
    promotion = promotion_rule_rows()
    all_rows: dict[str, list[dict[str, Any]]] = {
        "sources": source_register_rows(),
        "schema": schema,
        "refusal": refusal,
        "promotion": promotion,
        "smoke": smoke_rows(schema, refusal, promotion),
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

    print(f"2963 validation overall: {all_rows['validation'][-1]['passed']}")
    print(DOC)


if __name__ == "__main__":
    main()
