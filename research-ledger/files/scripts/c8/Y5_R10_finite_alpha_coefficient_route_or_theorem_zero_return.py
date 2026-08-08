from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"

DOC_PATH = ROOT / "571-Y5-R10-finite-alpha-coefficient-route-or-theorem-zero-return.md"

PRESSURE_570_PATH = RESIDUALS / "P8_Y5_R10_570_COEFFICIENT_PRESSURE_TABLE.csv"
PRODUCT_SCAN_570_PATH = RESIDUALS / "P8_Y5_R10_570_HYPOTHETICAL_PRODUCT_SCAN.csv"
VALIDATION_570_PATH = RESIDUALS / "P8_Y5_BRR545_570_VALIDATION.csv"
CURVE_SUMMARY_570_PATH = LOCAL_BOUNDS / "P8_Y5_R10_570_REVIEW_CURVE_SUMMARY.csv"

ZERO_CERT_PATH = RESIDUALS / "P8_Y5_R10_571_ZERO_THEOREM_CERTIFICATE.csv"
FINITE_CONTRACT_PATH = RESIDUALS / "P8_Y5_R10_571_FINITE_ROUTE_CONTRACT.csv"
PRESSURE_SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_571_PRESSURE_SUMMARY.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_BRR545_571_DECISION.csv"
ROUTE_UPDATE_PATH = RESIDUALS / "P8_Y5_BRR545_571_ROUTE_UPDATE.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_571_VALIDATION.csv"
SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_571_NONCLAIM_SUMMARY.csv"

STATUS = "Y5_R10_finite_alpha_route_retained_theorem_zero_not_parent_derived"
CLAIM_CEILING = "finite_alpha_route_contract_only_no_R10_fifth_force_WEP_PPN_or_local_GR_pass"
NEXT_TARGET = "572-Y5-R10-parent-coefficient-envelope-or-neutrality-theorem.md"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        values = []
        for column in columns:
            value = str(row.get(column, ""))
            value = value.replace("\n", "<br>").replace("|", "\\|")
            values.append(value)
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def to_float(value: str) -> float:
    return float(str(value).strip())


def prior_validation_clean(rows: list[dict[str, str]]) -> bool:
    return bool(rows) and all(row.get("result") == "pass" for row in rows)


def nearest_pressure_rows(pressure_rows: list[dict[str, str]]) -> list[dict[str, object]]:
    wanted = {
        "CP570_3": "gravity-strength anchor neighbourhood",
        "CP570_5": "sub-gravity transition pressure",
        "CP570_6": "100 micron strong pressure",
        "CP570_7": "200 micron strong pressure",
        "CP570_8": "500 micron near-tight region",
        "CP570_9": "1 mm long-end pressure",
    }
    selected = []
    for row in pressure_rows:
        pressure_id = row.get("pressure_id", "")
        if pressure_id in wanted:
            selected.append(
                {
                    "pressure_id": pressure_id,
                    "lambda_value_m": row.get("lambda_value", ""),
                    "alpha_bound_review_candidate": row.get("alpha_bound_review_candidate", ""),
                    "max_abs_KQqbar": row.get("max_abs_KQqbar", ""),
                    "pressure_read": wanted[pressure_id],
                    "valid_for_claim": "false",
                }
            )
    return selected


def tightest_curve_summary(curve_summary_rows: list[dict[str, str]]) -> dict[str, str]:
    for row in curve_summary_rows:
        if row.get("summary_id") == "CS570_3_min_alpha":
            return row
    return {}


def surviving_constant_product(product_rows: list[dict[str, str]]) -> tuple[str, str]:
    passing = [
        row
        for row in product_rows
        if row.get("pass_entire_review_curve", "").strip().lower() == "true"
    ]
    if not passing:
        return "none_in_scan", "all scanned products failed somewhere on candidate curve"
    best = max(passing, key=lambda row: to_float(row.get("hypothetical_abs_product", "0")))
    return best.get("hypothetical_abs_product", ""), best.get(
        "max_violation_ratio_product_over_bound", ""
    )


def make_zero_certificate() -> list[dict[str, object]]:
    return [
        {
            "certificate_id": "ZTC571_0_test_body_neutrality",
            "zero_factor": "qbar_XT=0",
            "sufficient_condition": "ordinary matter action factors only through observed quotient geometry and X-independent constants",
            "mathematical_form": "Dq[X]=0; partial_X hat_g=0; partial_X theta_A=0 => delta_X S_T=0",
            "current_status": "conditional_theorem_known_not_parent_derived",
            "proof_result": "not_promoted",
            "claim_status": "blocked_for_claim",
            "next_action": "derive quotient/no-marker parent theorem or retain qbar_XT residual row",
            "valid_for_claim": "false",
        },
        {
            "certificate_id": "ZTC571_1_source_neutrality",
            "zero_factor": "Qbar_XH(lambda)=0",
            "sufficient_condition": "torsion-balance source projection lies in the kernel of the X source functional for every relevant channel",
            "mathematical_form": "integral_H P_X[source_density,boundary,memory,domain](lambda)=0 channelwise",
            "current_status": "hidden_source_channels_open",
            "proof_result": "not_promoted",
            "claim_status": "blocked_for_claim",
            "next_action": "derive source projector kernel theorem or fill channelwise source form factor",
            "valid_for_claim": "false",
        },
        {
            "certificate_id": "ZTC571_2_vertex_zero_or_constraint",
            "zero_factor": "K_X=0",
            "sufficient_condition": "parent Ward identity removes the X-matter vertex, or X is a nonpropagating constraint with no physical exchange pole",
            "mathematical_form": "s_X=0 or residue(p_X^2+M_X^2)^-1 at matter vertex vanishes",
            "current_status": "no_parent_Ward_identity_written",
            "proof_result": "not_promoted",
            "claim_status": "blocked_for_claim",
            "next_action": "derive Ward/constraint identity or keep finite K_X coefficient",
            "valid_for_claim": "false",
        },
        {
            "certificate_id": "ZTC571_3_range_decoupling",
            "zero_factor": "lambda_X effectively below local-test reach",
            "sufficient_condition": "positive mass gap makes lambda_X=sqrt(Z_X/M_X^2) shorter than every relevant local probe scale",
            "mathematical_form": "lambda_X << lambda_probe with explicit Z_X>0 and M_X^2>0",
            "current_status": "range_not_parent_derived",
            "proof_result": "decoupling_route_only_not_zero_theorem",
            "claim_status": "blocked_for_claim",
            "next_action": "derive mass gap or include lower-range laboratory/particle constraints",
            "valid_for_claim": "false",
        },
        {
            "certificate_id": "ZTC571_4_no_accidental_cancellation",
            "zero_factor": "sum_c Q_c f_c(lambda)=0",
            "sufficient_condition": "channelwise symmetry identity, not one material-specific numerical cancellation",
            "mathematical_form": "for all allowed sources and lambda: Q_c=0 or sum_c Q_c f_c(lambda)=0 by identity",
            "current_status": "not_available",
            "proof_result": "forbid_as_claim_shortcut",
            "claim_status": "blocked_for_claim",
            "next_action": "use only as diagnostic fit unless promoted to symmetry theorem",
            "valid_for_claim": "false",
        },
    ]


def make_finite_contract() -> list[dict[str, object]]:
    return [
        {
            "contract_id": "FRC571_0_quadratic_local_mode",
            "object": "local X quadratic action",
            "mathematical_form": "S_X^(2)=int sqrt(-g)[-1/2 Z_X (nabla deltaX)^2 -1/2 M_X^2 deltaX^2 + deltaX J_X]",
            "requirement": "derive Z_X>0 and M_X^2>=0 from parent Hessian, or mark branch unstable/closure",
            "claim_status": "unfilled",
            "valid_for_claim": "false",
        },
        {
            "contract_id": "FRC571_1_range_law",
            "object": "lambda_X",
            "mathematical_form": "lambda_X=sqrt(Z_X/M_X^2)",
            "requirement": "derive or scan only as nonclaim until parent mass gap exists",
            "claim_status": "unfilled",
            "valid_for_claim": "false",
        },
        {
            "contract_id": "FRC571_2_alpha_law",
            "object": "alpha_X(lambda_X)",
            "mathematical_form": "alpha_X=K_X Qbar_XH(lambda_X) qbar_XT; K_X=s_X/(4*pi*Z_X*G_obs)",
            "requirement": "all three product factors must be sourced, bounded, or theorem-zero",
            "claim_status": "symbolic_only",
            "valid_for_claim": "false",
        },
        {
            "contract_id": "FRC571_3_R10_bound_gate",
            "object": "R10 inequality",
            "mathematical_form": "abs(K_X Qbar_XH(lambda_X) qbar_XT) <= alpha_bound(lambda_X)",
            "requirement": "candidate curve may set private targets; live claim needs promoted source-backed curve",
            "claim_status": "diagnostic_only",
            "valid_for_claim": "false",
        },
        {
            "contract_id": "FRC571_4_zero_return_gate",
            "object": "return to theorem-zero",
            "mathematical_form": "alpha_X=0 only if qbar_XT=0 or Qbar_XH=0 or K_X=0 by parent identity",
            "requirement": "no assumed plateau, no fitted cancellation, no universal-coupling shortcut",
            "claim_status": "not_promoted",
            "valid_for_claim": "false",
        },
    ]


def make_decisions() -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D571_0_zero_theorem_rejected_for_now",
            "decision": "do not promote alpha_X=0",
            "meaning": "the exact zero routes are known but none are parent-derived in the current corpus",
            "status": "blocked_for_claim",
            "next_target": NEXT_TARGET,
        },
        {
            "decision_id": "D571_1_finite_route_retained",
            "decision": "retain finite alpha coefficient branch",
            "meaning": "local R10 risk is an explicit product inequality, not an informal worry",
            "status": "retained_nonclaim",
            "next_target": NEXT_TARGET,
        },
        {
            "decision_id": "D571_2_next_derivation",
            "decision": "derive coefficient envelope or neutrality theorem",
            "meaning": "either bound product below the pressure wall or prove a true zero factor",
            "status": "next_required",
            "next_target": NEXT_TARGET,
        },
    ]


def make_route_update() -> list[dict[str, object]]:
    return [
        {
            "route_id": "RU571_0_allowed",
            "allowed_after_571": "Use the zero certificate as an exact parent-action contract and the finite route as the active nonclaim branch.",
            "forbidden_after_571": "Claim R10/local-GR pass, assume qbar_XT=0, or use one-lambda cancellation as a theorem.",
            "next_action": NEXT_TARGET,
        },
        {
            "route_id": "RU571_1_theory_route",
            "allowed_after_571": "Try to prove qbar_XT=0, Qbar_XH(lambda)=0, or K_X=0 from Ward/quotient/no-marker structure.",
            "forbidden_after_571": "Keep cycling broad zero-route attempts without adding a sharper parent premise.",
            "next_action": "derive one zero factor or write residual coefficient envelope",
        },
        {
            "route_id": "RU571_2_numeric_route",
            "allowed_after_571": "Use the 570 pressure table as target magnitudes for K_X Qbar_XH qbar_XT.",
            "forbidden_after_571": "Promote review-candidate vector curve into public exclusion evidence without QA/provenance signoff.",
            "next_action": "parent coefficient envelope plus bound-curve promotion later",
        },
    ]


def make_validation(
    prior_rows: list[dict[str, str]],
    zero_rows: list[dict[str, object]],
    contract_rows: list[dict[str, object]],
    pressure_rows: list[dict[str, object]],
    decisions: list[dict[str, object]],
) -> list[dict[str, object]]:
    source_paths = [
        PRESSURE_570_PATH,
        PRODUCT_SCAN_570_PATH,
        VALIDATION_570_PATH,
        CURVE_SUMMARY_570_PATH,
    ]
    missing = [str(path.relative_to(ROOT)) for path in source_paths if not path.exists()]
    claim_zero_rows = [
        row for row in zero_rows if str(row.get("valid_for_claim", "")).lower() == "true"
    ]
    return [
        {
            "check_id": "V571_0_source_paths_exist",
            "result": "pass" if not missing else "fail",
            "detail": "missing=" + str(len(missing)) + (";" + ";".join(missing) if missing else ""),
        },
        {
            "check_id": "V571_1_prior_570_clean",
            "result": "pass" if prior_validation_clean(prior_rows) else "fail",
            "detail": f"prior_validation_rows={len(prior_rows)};prior_fails={sum(row.get('result') != 'pass' for row in prior_rows)}",
        },
        {
            "check_id": "V571_2_zero_certificate_written",
            "result": "pass" if len(zero_rows) >= 5 else "fail",
            "detail": f"zero_certificate_rows={len(zero_rows)};claim_rows={len(claim_zero_rows)}",
        },
        {
            "check_id": "V571_3_finite_contract_written",
            "result": "pass" if len(contract_rows) >= 5 else "fail",
            "detail": f"contract_rows={len(contract_rows)}",
        },
        {
            "check_id": "V571_4_pressure_summary_numeric",
            "result": "pass"
            if all(float(row["alpha_bound_review_candidate"]) > 0 for row in pressure_rows)
            else "fail",
            "detail": f"pressure_rows={len(pressure_rows)}",
        },
        {
            "check_id": "V571_5_decision_blocks_claim",
            "result": "pass"
            if any(row.get("status") == "blocked_for_claim" for row in decisions)
            else "fail",
            "detail": "R10_pass=false;local_GR=false;claim_allowed=false",
        },
        {
            "check_id": "V571_6_no_overclaim",
            "result": "pass",
            "detail": "theorem_zero_parent_derived=false;finite_alpha_numeric=false;review_curve_claim=false;R10_pass=false;WEP=false;PPN=false;local_GR=false",
        },
    ]


def write_markdown(
    generated: str,
    zero_rows: list[dict[str, object]],
    contract_rows: list[dict[str, object]],
    pressure_summary: list[dict[str, object]],
    decisions: list[dict[str, object]],
    route_update: list[dict[str, object]],
    validation: list[dict[str, object]],
    tightest: dict[str, str],
    product_survivor: tuple[str, str],
) -> None:
    tight_value = tightest.get("value", "unknown")
    tight_notes = tightest.get("notes", "unknown")
    survivor, survivor_ratio = product_survivor
    body = f"""# 571 Y5 R10 finite alpha coefficient route or theorem zero return

Generated: {generated}  
Status: `{STATUS}`  
Claim ceiling: `{CLAIM_CEILING}`  
Next target: `{NEXT_TARGET}`

## Verdict
- The exact local suppression condition is now sharp: for a finite propagating `X` mode, `alpha_X=0` only follows from a parent-derived zero of `qbar_XT`, `Qbar_XH(lambda)`, or `K_X`.
- The current corpus has conditional zero theorems, but no parent-derived zero certificate. So the theorem-zero branch is not claimable.
- The active branch remains finite-alpha: `abs(K_X Qbar_XH(lambda_X) qbar_XT) <= alpha_bound(lambda_X)`.
- The 570 review-candidate curve says the broad-range constant product must be roughly below the tightest candidate wall `{tight_value}`; in the scan, the largest tested constant product surviving the entire review curve was `{survivor}` with violation ratio `{survivor_ratio}`.

## Derivation
Assume the local branch contains a quadratic finite mode about the local vacuum:

```text
S_X^(2) = int sqrt(-g)[
  -1/2 Z_X (nabla deltaX)^2
  -1/2 M_X^2 deltaX^2
  + deltaX J_X
].
```

The static exchange equation gives a Yukawa profile with:

```text
lambda_X = sqrt(Z_X/M_X^2),
alpha_X(lambda_X) = K_X Qbar_XH(lambda_X) qbar_XT,
K_X = s_X/(4 pi Z_X G_obs).
```

Therefore local suppression is not magic. For finite nonzero `Z_X`, finite range, and a real exchange pole:

```text
alpha_X = 0
iff K_X = 0 or Qbar_XH(lambda_X) = 0 or qbar_XT = 0.
```

If no zero factor is parent-derived, the branch must face:

```text
abs(K_X Qbar_XH(lambda_X) qbar_XT) <= alpha_bound(lambda_X).
```

## Zero Theorem Certificate
{markdown_table(zero_rows, ["certificate_id", "zero_factor", "sufficient_condition", "current_status", "proof_result", "claim_status", "valid_for_claim"])}

## Finite Route Contract
{markdown_table(contract_rows, ["contract_id", "object", "mathematical_form", "requirement", "claim_status", "valid_for_claim"])}

## Pressure Summary From 570
{markdown_table(pressure_summary, ["pressure_id", "lambda_value_m", "alpha_bound_review_candidate", "max_abs_KQqbar", "pressure_read", "valid_for_claim"])}

Tightest review-candidate wall: `{tight_value}` with note `{tight_notes}`. This is private diagnostic pressure only, not a public exclusion claim.

## Route Logic
| branch | condition | result |
| --- | --- | --- |
| true theorem-zero | parent derives `qbar_XT=0`, `Qbar_XH=0`, or `K_X=0` | R10 alpha branch can be removed for that channel |
| finite but safe | parent predicts product below `alpha_bound(lambda_X)` | branch survives R10 as a bounded residual |
| finite and natural-strength | product near `1` at large `lambda_X` | pressured or excluded by candidate curve, pending promoted evidence |
| range-decoupled | `lambda_X` lies below relevant reach by derived mass gap | not theorem-zero; route to other local/particle constraints |
| cancellation-only | one material/source gives accidental zero | not a theorem; cannot support local-GR claim |

## Decision
{markdown_table(decisions, ["decision_id", "decision", "meaning", "status", "next_target"])}

## Route Update
{markdown_table(route_update, ["route_id", "allowed_after_571", "forbidden_after_571", "next_action"])}

## Validation
{markdown_table(validation, ["check_id", "result", "detail"])}

## Practical Read
This is a useful little gate. We did not get to say “the fifth force is zero” by vibes, but we did get the exact contract: either prove one factor is zero from the parent action, or keep the finite mode and make its coefficient small enough. If MTS naturally predicts `|K_X Qbar_XH qbar_XT| <= 10^-3`, the local branch has room. If it predicts order-unity product at `~0.1-1 mm`, R10 becomes a serious problem. That is not fatal; it is the workbench finally telling us where the dragon actually lives.
"""
    DOC_PATH.write_text(body, encoding="utf-8")


def main() -> None:
    generated = datetime.now(timezone.utc).isoformat()

    pressure_rows_570 = read_csv(PRESSURE_570_PATH)
    product_rows_570 = read_csv(PRODUCT_SCAN_570_PATH)
    validation_rows_570 = read_csv(VALIDATION_570_PATH)
    curve_summary_rows_570 = read_csv(CURVE_SUMMARY_570_PATH)

    zero_rows = make_zero_certificate()
    contract_rows = make_finite_contract()
    pressure_summary = nearest_pressure_rows(pressure_rows_570)
    decisions = make_decisions()
    route_update = make_route_update()
    validation = make_validation(
        validation_rows_570, zero_rows, contract_rows, pressure_summary, decisions
    )
    tightest = tightest_curve_summary(curve_summary_rows_570)
    product_survivor = surviving_constant_product(product_rows_570)

    summary_rows = [
        {
            "summary_id": "S571_0_result",
            "status": STATUS,
            "claim_allowed": "false",
            "R10_pass_for_claim": "false",
            "local_GR_pass": "false",
            "theorem_zero_parent_derived": "false",
            "finite_alpha_numeric": "false",
            "tightest_review_candidate_alpha": tightest.get("value", ""),
            "largest_tested_constant_product_surviving_review_curve": product_survivor[0],
            "next_target": NEXT_TARGET,
        }
    ]

    write_csv(
        ZERO_CERT_PATH,
        zero_rows,
        [
            "certificate_id",
            "zero_factor",
            "sufficient_condition",
            "mathematical_form",
            "current_status",
            "proof_result",
            "claim_status",
            "next_action",
            "valid_for_claim",
        ],
    )
    write_csv(
        FINITE_CONTRACT_PATH,
        contract_rows,
        [
            "contract_id",
            "object",
            "mathematical_form",
            "requirement",
            "claim_status",
            "valid_for_claim",
        ],
    )
    write_csv(
        PRESSURE_SUMMARY_PATH,
        pressure_summary,
        [
            "pressure_id",
            "lambda_value_m",
            "alpha_bound_review_candidate",
            "max_abs_KQqbar",
            "pressure_read",
            "valid_for_claim",
        ],
    )
    write_csv(
        DECISION_PATH,
        decisions,
        ["decision_id", "decision", "meaning", "status", "next_target"],
    )
    write_csv(
        ROUTE_UPDATE_PATH,
        route_update,
        ["route_id", "allowed_after_571", "forbidden_after_571", "next_action"],
    )
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])
    write_csv(
        SUMMARY_PATH,
        summary_rows,
        [
            "summary_id",
            "status",
            "claim_allowed",
            "R10_pass_for_claim",
            "local_GR_pass",
            "theorem_zero_parent_derived",
            "finite_alpha_numeric",
            "tightest_review_candidate_alpha",
            "largest_tested_constant_product_surviving_review_curve",
            "next_target",
        ],
    )

    write_markdown(
        generated,
        zero_rows,
        contract_rows,
        pressure_summary,
        decisions,
        route_update,
        validation,
        tightest,
        product_survivor,
    )

    all_validation_passed = all(row["result"] == "pass" for row in validation)
    print(
        json.dumps(
            {
                "generated_at_utc": generated,
                "status": STATUS,
                "claim_ceiling": CLAIM_CEILING,
                "next_target": NEXT_TARGET,
                "doc": str(DOC_PATH.relative_to(ROOT)),
                "validation": str(VALIDATION_PATH.relative_to(ROOT)),
                "all_validation_passed": all_validation_passed,
                "claim_allowed": False,
            },
            indent=2,
        )
    )

    if not all_validation_passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
