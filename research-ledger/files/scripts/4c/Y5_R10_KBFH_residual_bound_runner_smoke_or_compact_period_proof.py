from __future__ import annotations

import csv
import math
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
DOC = ROOT / "929-Y5-R10-KBFH-residual-bound-runner-smoke-or-compact-period-proof.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
SCRIPT_START_UTC = datetime.now(timezone.utc)


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def b(value: bool) -> str:
    return "true" if value else "false"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def is_float(value: str) -> bool:
    try:
        parsed = float(value)
    except (TypeError, ValueError):
        return False
    return math.isfinite(parsed)


def has_blocker(value: str) -> bool:
    tokens = [token.strip() for token in (value or "").replace(",", ";").split(";")]
    return any(token.startswith("MISSING_") or "PLACEHOLDER" in token or token == "R10_CURVE_PLACEHOLDER" for token in tokens)


def md_table(rows: list[dict[str, object]], fields: list[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(fields) + " |"
    sep = "| " + " | ".join("---" for _ in fields) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(str(row.get(field, "")).replace("\n", " ") for field in fields) + " |")
    return "\n".join([header, sep, *body])


def source_register() -> list[dict[str, str]]:
    specs = [
        {
            "source_id": "928_doc",
            "path": "928-Y5-R10-instantiate-compact-BF-lattice-or-retain-KBFH-residual-bound-row.md",
            "role": "checkpoint that retained K_BF_H as explicit residual",
            "needle": "compact BF lattice route does not instantiate",
        },
        {
            "source_id": "928_validation",
            "path": "source-intake/mts_residuals/P8_Y5_BRR545_928_VALIDATION.csv",
            "role": "proves 928 validation passed and formalization-workbench was untouched",
            "needle": "V928_10_validation_rows_ready",
        },
        {
            "source_id": "928_residual_parameters",
            "path": "source-intake/mts_residuals/P8_Y5_R10_928_KBFH_RESIDUAL_PARAMETERS.csv",
            "role": "K_BF_H and epsilon_FM residual definitions",
            "needle": "KRES928_0_KBFH_over_kM_residual",
        },
        {
            "source_id": "928_bound_rows",
            "path": "source-intake/mts_residuals/P8_Y5_R10_928_KBFH_RESIDUAL_BOUND_ROWS.csv",
            "role": "local-bound residual prediction templates",
            "needle": "KBOUND928_10_R10_fifth_force",
        },
        {
            "source_id": "928_claim_gates",
            "path": "source-intake/mts_residuals/P8_Y5_R10_928_CLAIM_GATE.csv",
            "role": "prior claim gates forcing nonclaim status",
            "needle": "CGATE928_1_KBFH_numeric",
        },
        {
            "source_id": "928_compact_instantiation",
            "path": "source-intake/mts_residuals/P8_Y5_R10_928_COMPACT_BF_INSTANTIATION_AUDIT.csv",
            "role": "compact-period retry prerequisites",
            "needle": "INST928_0_A_M_compact_period",
        },
        {
            "source_id": "local_bound_claims",
            "path": "source-intake/local_bounds/local_bound_claims.csv",
            "role": "source-backed local bound manifest joined by 928",
            "needle": "R10_fifth_force",
        },
        {
            "source_id": "R10_curve_status",
            "path": "source-intake/local_bounds/R10_alpha_lambda_bound_curve_DIGITIZED.csv",
            "role": "R10 alpha(lambda) curve status; placeholder blocks scoring",
            "needle": "MISSING_DIGITIZED_ALPHA_BOUND",
        },
    ]
    rows = []
    for spec in specs:
        path = ROOT / spec["path"]
        exists = path.exists()
        needle_found = exists and spec["needle"] in read_text(path)
        rows.append(
            {
                **spec,
                "absolute_path": str(path),
                "exists": b(exists),
                "needle_found": b(needle_found),
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def build_smoke_evaluation(bound_rows: list[dict[str, str]], parameters: list[dict[str, str]]) -> list[dict[str, str]]:
    parameter_status = "; ".join(f"{row['symbol']}={row['current_value']}" for row in parameters)
    rows = []
    for row in bound_rows:
        upper_bound_numeric = is_float(row.get("upper_bound", ""))
        blockers = row.get("missing_inputs", "")
        valid_for_claim = row.get("valid_for_claim", "").lower() == "true"
        no_missing_inputs = not has_blocker(blockers)
        has_projection_coefficient = "MISSING_PROJECTION_COEFFICIENT" not in blockers
        has_epsilon = "MISSING_EPSILON_FM" not in blockers
        has_kbfh = "MISSING_KBFH_RESIDUAL" not in blockers
        r10_extra_ready = row["local_bound_row"] != "R10_fifth_force" or (
            "MISSING_RANGE_LAW" not in blockers
            and "MISSING_ALPHA_LAMBDA_PREDICTION" not in blockers
            and "R10_CURVE_PLACEHOLDER" not in blockers
        )
        can_score = all(
            [
                upper_bound_numeric,
                valid_for_claim,
                no_missing_inputs,
                has_projection_coefficient,
                has_epsilon,
                has_kbfh,
                r10_extra_ready,
            ]
        )
        if can_score:
            status = "ready_to_score"
            reason = "all numeric inputs present"
        elif row["local_bound_row"] == "R10_fifth_force":
            status = "blocked_R10_range_prediction_and_curve"
            reason = "R10 needs alpha(lambda), a range law, and a real digitized/source-backed bound curve"
        elif not upper_bound_numeric:
            status = "blocked_non_numeric_bound"
            reason = "bound is not a finite scalar number"
        else:
            status = "blocked_missing_residual_inputs"
            reason = "K_BF_H, epsilon_FM, and/or arena projection coefficient remain missing"
        rows.append(
            {
                "smoke_id": row["bound_row_id"].replace("KBOUND928", "SMOKE929"),
                "source_bound_row": row["bound_row_id"],
                "local_bound_row": row["local_bound_row"],
                "observable": row["observable"],
                "upper_bound": row["upper_bound"],
                "upper_bound_numeric": b(upper_bound_numeric),
                "prediction_template": row["prediction_template"],
                "parameter_status": parameter_status,
                "missing_inputs": blockers,
                "can_score": b(can_score),
                "score_status": status,
                "reason": reason,
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def build_required_input_contract(smoke_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    rows = [
        {
            "contract_id": "REQ929_0_KBFH_numeric",
            "target": "all local residual rows",
            "required_input": "numeric K_BF_H/k_M or parent-signed compact BF ratio",
            "acceptable_source": "compact A_M/B_M period lattice with source lattice, or explicit parent coefficient with units",
            "current_status": "missing",
            "blocks": "WEP; clocks; PPN; Gdot; R10",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "contract_id": "REQ929_1_epsilon_FM_numeric",
            "target": "all local residual rows",
            "required_input": "numeric epsilon_FM including A_M norm, dPiMJ leak, B_zero_flux, and normalizers",
            "acceptable_source": "weak-field parent expansion or explicit source-row coefficients with units",
            "current_status": "missing",
            "blocks": "WEP; clocks; PPN; Gdot; R10",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "contract_id": "REQ929_2_projection_coefficients",
            "target": "each local arena",
            "required_input": "C_arena_FM projection coefficient mapping epsilon_FM to the observable",
            "acceptable_source": "PPN/readout calculation or source-backed experimental projection map",
            "current_status": "missing",
            "blocks": "arena scoring",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "contract_id": "REQ929_3_R10_range_law",
            "target": "R10 fifth-force row",
            "required_input": "alpha_FM(lambda) and lambda support/range law",
            "acceptable_source": "mass-gap/mediator derivation, compact support theorem, or sourced effective Yukawa map",
            "current_status": "missing",
            "blocks": "R10 scoring",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "contract_id": "REQ929_4_R10_bound_curve",
            "target": "R10 fifth-force row",
            "required_input": "real source-backed alpha_bound(lambda) curve or machine-readable table",
            "acceptable_source": "digitized Eot-Wash/Adelberger curve with provenance or official table",
            "current_status": "placeholder_only",
            "blocks": "R10 scoring",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]
    blocked_rows = [row["local_bound_row"] for row in smoke_rows if row["can_score"] == "false"]
    rows.append(
        {
            "contract_id": "REQ929_5_current_blocked_rows",
            "target": "smoke runner status",
            "required_input": "no blocked rows if making a local-bound pass claim",
            "acceptable_source": "all rows scoreable and numerically pass bounds",
            "current_status": f"{len(blocked_rows)} blocked rows: " + "; ".join(blocked_rows),
            "blocks": "local-bound pass claim",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    )
    return rows


def build_compact_retry_audit(instantiation_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    rows = []
    for row in instantiation_rows:
        result = row.get("result", "")
        retry_allowed = result in {"fail_for_claim", "conditional_only", "not_applicable_for_KBFH_claim"}
        rows.append(
            {
                "retry_id": row["test_id"].replace("INST928", "RETRY929"),
                "source_test_id": row["test_id"],
                "needed_to_promote": row["contract_clause"],
                "current_candidate": row["current_symbol_candidate"],
                "current_result": result,
                "retry_allowed_only_with": "new parent-symbol evidence and source path" if retry_allowed else "not selected",
                "reason": row["reason"],
                "promotion_allowed_now": "false",
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def build_decisions(smoke_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    scoreable = [row for row in smoke_rows if row["can_score"] == "true"]
    return [
        {
            "decision_id": "DEC929_0_no_current_scoring",
            "decision": "do_not_score_local_bound_rows_yet",
            "reason": f"{len(scoreable)} of {len(smoke_rows)} rows are scoreable; residual parent inputs remain missing",
            "consequence": "local-GR/R10/WEP/PPN claims remain false",
            "next_action": "derive or source K_BF_H/epsilon_FM/projection coefficients",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC929_1_compact_period_route",
            "decision": "compact_period_route_not_reopened_without_new_evidence",
            "reason": "928 already showed A_M/B_M compact periods and source lattice are not instantiated in current symbol map",
            "consequence": "do not set K_BF_H/k_M to +/-1",
            "next_action": "if pursued, write parent action clauses with compact periods and same-worldtube source lattice",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC929_2_best_next_target",
            "decision": "hunt_coupling_origin_before_public_claim",
            "reason": "the coupling is now the bottleneck; tests can only constrain it after the parent/current normalization exists",
            "consequence": "next checkpoint targets derivation of the minimal K_BF_H input contract",
            "next_action": "930-Y5-R10-KBFH-coupling-origin-minimal-input-contract-or-first-scoreable-bound-row.md",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def build_claim_gates(smoke_rows: list[dict[str, str]], retry_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    all_scoreable = all(row["can_score"] == "true" for row in smoke_rows)
    any_promotion = any(row["promotion_allowed_now"] == "true" for row in retry_rows)
    return [
        {
            "gate_id": "CGATE929_0_runner_scoreable",
            "claim": "K_BF_H residual rows are numerically scoreable",
            "evidence": f"all_scoreable={b(all_scoreable)}",
            "claim_allowed": b(all_scoreable),
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE929_1_compact_ratio_promoted",
            "claim": "compact-period route promotes K_BF_H/k_M to N_B/N_H or +/-1",
            "evidence": f"any_promotion_allowed_now={b(any_promotion)}",
            "claim_allowed": b(any_promotion),
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE929_2_R10_pass",
            "claim": "R10 fifth-force branch passes alpha(lambda) bound",
            "evidence": "R10 row still lacks range law, alpha(lambda) prediction, and real curve",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE929_3_local_GR_pass",
            "claim": "local GR/Newton limit is derived from this coupling branch",
            "evidence": "runner is a residual gate only; no source-normalized parent derivation exists",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def formalization_changed_after_start() -> int:
    if not FORMALIZATION.exists():
        return -1
    count = 0
    for path in FORMALIZATION.rglob("*"):
        if not path.is_file():
            continue
        modified = datetime.fromtimestamp(path.stat().st_mtime, timezone.utc)
        if modified > SCRIPT_START_UTC:
            count += 1
    return count


def build_validation(
    sources: list[dict[str, str]],
    parameters: list[dict[str, str]],
    bound_rows: list[dict[str, str]],
    smoke_rows: list[dict[str, str]],
    contract_rows: list[dict[str, str]],
    retry_rows: list[dict[str, str]],
    decisions: list[dict[str, str]],
    claim_gates: list[dict[str, str]],
) -> list[dict[str, str]]:
    rows = []

    def add(check_id: str, ok: bool, detail: str) -> None:
        rows.append({"check_id": check_id, "result": "pass" if ok else "fail", "detail": detail, "generated_utc": stamp()})

    source_ok = all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources)
    prior_928 = read_csv(ROOT / "source-intake/mts_residuals/P8_Y5_BRR545_928_VALIDATION.csv")
    prior_928_clean = prior_928 and all(row.get("result") == "pass" for row in prior_928)
    all_params_blocked = parameters and all(row.get("valid_for_claim") == "false" and row.get("current_value", "").startswith("MISSING_") for row in parameters)
    all_bounds_blocked = bound_rows and all(row.get("valid_for_claim") == "false" and has_blocker(row.get("missing_inputs", "")) for row in bound_rows)
    no_scoreable = smoke_rows and all(row["can_score"] == "false" for row in smoke_rows)
    r10_rows = [row for row in smoke_rows if row["local_bound_row"] == "R10_fifth_force"]
    r10_blocked = len(r10_rows) == 1 and r10_rows[0]["score_status"] == "blocked_R10_range_prediction_and_curve"
    all_contract_nonclaim = contract_rows and all(row["valid_for_claim"] == "false" for row in contract_rows)
    compact_not_promoted = retry_rows and all(row["promotion_allowed_now"] == "false" for row in retry_rows)
    all_decisions_nonclaim = decisions and all(row["valid_for_claim"] == "false" for row in decisions)
    all_claim_gates_false = claim_gates and all(row["claim_allowed"] == "false" and row["valid_for_claim"] == "false" for row in claim_gates)
    fw_changed = formalization_changed_after_start()
    next_target_ok = any("930-Y5-R10-KBFH-coupling-origin" in row["next_action"] for row in decisions)

    add("V929_0_sources_exist_and_needles", source_ok, "all source paths exist and needles are present" if source_ok else "missing source path or needle")
    add("V929_1_prior_928_clean", prior_928_clean, "P8_Y5_BRR545_928_VALIDATION.csv clean")
    add("V929_2_parameters_remain_blocked", all_params_blocked, "K_BF_H and epsilon_FM have missing numeric parent inputs")
    add("V929_3_bound_rows_remain_blocked", all_bounds_blocked, "all 928 bound rows still carry explicit blockers")
    add("V929_4_no_rows_scoreable", no_scoreable, "strict smoke runner refuses to score all rows")
    add("V929_5_R10_blocked_correctly", r10_blocked, "R10 remains blocked by missing range law, alpha(lambda), and real curve")
    add("V929_6_required_contract_nonclaim", all_contract_nonclaim, "required input contract written without claim promotion")
    add("V929_7_compact_period_not_promoted", compact_not_promoted, "compact-period retry audit allows no promotion now")
    add("V929_8_decisions_nonclaim", all_decisions_nonclaim, "decision rows are explicit nonclaim")
    add("V929_9_claim_gates_false", all_claim_gates_false, "all claim gates remain false")
    add("V929_10_formalization_workbench_untouched", fw_changed == 0, f"formalization_changed_after_start={fw_changed}")
    add("V929_11_next_target_selected", next_target_ok, "930-Y5-R10-KBFH-coupling-origin-minimal-input-contract-or-first-scoreable-bound-row.md")
    add("V929_12_validation_rows_ready", True, "validation table constructed")
    return rows


def write_doc(
    sources: list[dict[str, str]],
    smoke_rows: list[dict[str, str]],
    contract_rows: list[dict[str, str]],
    retry_rows: list[dict[str, str]],
    decisions: list[dict[str, str]],
    claim_gates: list[dict[str, str]],
    validation: list[dict[str, str]],
) -> None:
    text = f"""# 929 - Y5/R10 KBFH Residual Bound Runner Smoke Or Compact Period Proof

Generated: `{stamp()}`

Status: `Y5_R10_929_strict_smoke_runner_blocks_all_KBFH_residual_rows_no_compact_period_promotion`

Claim ceiling: `nonclaim_gatekeeper_only_no_R10_WEP_PPN_Newton_or_local_GR_pass`

## Result

The strict smoke runner works, and it refuses to score every row. That is the right result at this stage.

The coupling bottleneck is now explicit:

```text
scoreable(row) requires numeric K_BF_H/k_M, numeric epsilon_FM, arena projection coefficient C_arena_FM, and a numeric/source-backed bound.
```

For R10, the row also requires `alpha_FM(lambda)`, a range law, and a real `alpha_bound(lambda)` curve. The current R10 curve file is still placeholder-only, so no fifth-force pass can be claimed.

## Source Register

{md_table(sources, ["source_id", "path", "role", "needle_found", "valid_for_claim"])}

## Smoke Evaluation

{md_table(smoke_rows, ["smoke_id", "local_bound_row", "observable", "upper_bound_numeric", "can_score", "score_status", "reason", "valid_for_claim"])}

## Required Input Contract

{md_table(contract_rows, ["contract_id", "target", "required_input", "current_status", "blocks", "valid_for_claim"])}

## Compact Period Retry Audit

{md_table(retry_rows, ["retry_id", "needed_to_promote", "current_result", "promotion_allowed_now", "reason", "valid_for_claim"])}

## Decision Ledger

{md_table(decisions, ["decision_id", "decision", "reason", "consequence", "next_action", "valid_for_claim"])}

## Claim Gates

{md_table(claim_gates, ["gate_id", "claim", "evidence", "claim_allowed", "valid_for_claim"])}

## Validation

{md_table(validation, ["check_id", "result", "detail", "generated_utc"])}

## Next Target

`930-Y5-R10-KBFH-coupling-origin-minimal-input-contract-or-first-scoreable-bound-row.md`

The cleanest next derivation route is to attack the coupling itself:

1. derive `K_BF_H/k_M` from parent current normalization, compact periods, or a same-worldtube charge theorem;
2. derive `epsilon_FM` from the weak-field residual pieces without absorbing it into `G` or `M`;
3. only then score WEP/clock/PPN/Gdot/R10 rows.
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    sources = source_register()
    parameters = read_csv(OUT / "P8_Y5_R10_928_KBFH_RESIDUAL_PARAMETERS.csv")
    bound_rows = read_csv(OUT / "P8_Y5_R10_928_KBFH_RESIDUAL_BOUND_ROWS.csv")
    instantiation_rows = read_csv(OUT / "P8_Y5_R10_928_COMPACT_BF_INSTANTIATION_AUDIT.csv")

    smoke_rows = build_smoke_evaluation(bound_rows, parameters)
    contract_rows = build_required_input_contract(smoke_rows)
    retry_rows = build_compact_retry_audit(instantiation_rows)
    decisions = build_decisions(smoke_rows)
    claim_gates = build_claim_gates(smoke_rows, retry_rows)
    validation = build_validation(sources, parameters, bound_rows, smoke_rows, contract_rows, retry_rows, decisions, claim_gates)

    write_csv(
        OUT / "P8_Y5_R10_929_SOURCE_REGISTER.csv",
        sources,
        ["source_id", "path", "absolute_path", "role", "needle", "exists", "needle_found", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_929_SMOKE_EVALUATION.csv",
        smoke_rows,
        [
            "smoke_id",
            "source_bound_row",
            "local_bound_row",
            "observable",
            "upper_bound",
            "upper_bound_numeric",
            "prediction_template",
            "parameter_status",
            "missing_inputs",
            "can_score",
            "score_status",
            "reason",
            "valid_for_claim",
            "generated_utc",
        ],
    )
    write_csv(
        OUT / "P8_Y5_R10_929_REQUIRED_INPUT_CONTRACT.csv",
        contract_rows,
        ["contract_id", "target", "required_input", "acceptable_source", "current_status", "blocks", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_929_COMPACT_PERIOD_RETRY_AUDIT.csv",
        retry_rows,
        [
            "retry_id",
            "source_test_id",
            "needed_to_promote",
            "current_candidate",
            "current_result",
            "retry_allowed_only_with",
            "reason",
            "promotion_allowed_now",
            "valid_for_claim",
            "generated_utc",
        ],
    )
    write_csv(
        OUT / "P8_Y5_R10_929_DECISION_LEDGER.csv",
        decisions,
        ["decision_id", "decision", "reason", "consequence", "next_action", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_929_CLAIM_GATE.csv",
        claim_gates,
        ["gate_id", "claim", "evidence", "claim_allowed", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_929_NEXT_TARGET.csv",
        [
            {
                "next_target": "930-Y5-R10-KBFH-coupling-origin-minimal-input-contract-or-first-scoreable-bound-row.md",
                "objective": "derive or source the minimal K_BF_H/epsilon_FM/projection inputs required before any local-bound scoring",
                "include": "parent current normalization, compact-period retry only with new evidence, weak-field residual units, first scoreable non-R10 row if derivation fails",
                "exclude": "hidden G/M absorption, +/-1 promotion without compact periods, R10 claim with placeholder curve, GitHub action, formalization-workbench edits",
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        ],
        ["next_target", "objective", "include", "exclude", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_BRR545_929_VALIDATION.csv",
        validation,
        ["check_id", "result", "detail", "generated_utc"],
    )
    write_doc(sources, smoke_rows, contract_rows, retry_rows, decisions, claim_gates, validation)

    failures = [row for row in validation if row["result"] != "pass"]
    if failures:
        raise SystemExit(f"validation failed: {failures}")
    print("Y5_R10_929_strict_smoke_runner_blocks_all_KBFH_residual_rows_no_compact_period_promotion")
    print(f"wrote {DOC}")
    print("next target: 930-Y5-R10-KBFH-coupling-origin-minimal-input-contract-or-first-scoreable-bound-row.md")


if __name__ == "__main__":
    main()
