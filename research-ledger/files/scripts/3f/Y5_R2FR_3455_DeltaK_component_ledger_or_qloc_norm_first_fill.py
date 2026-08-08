from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "3455-Y5-R2FR-DeltaK-component-ledger-or-q_loc-norm-first-fill-under-AX1090.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

SOURCES = {
    "script_3455": Path(__file__).resolve(),
    "doc_3454": ROOT / "3454-Y5-R2FR-Gamma-Khat-q_loc-placeholder-typing-or-first-active-LX-bound-under-AX1090.md",
    "next_3454": OUT / "P8_Y5_R2FR_3454_NEXT_TARGET.csv",
    "typing_3454": OUT / "P8_Y5_R2FR_3454_GK_PLACEHOLDER_TYPING.csv",
    "metric_status_3454": OUT / "P8_Y5_R2FR_3454_METRIC_RESPONSE_STATUS.csv",
    "active_bound_3454": OUT / "P8_Y5_R2FR_3454_FIRST_ACTIVE_LX_BOUND_INPUT.csv",
    "sign_lock_2975": OUT / "P8_Y5_R2FR_2975_GAMMAKHAT_SIGN_CONVENTION_LOCK.csv",
    "metric_response_776": OUT / "P8_Y5_R10_776_KGAMMA_METRIC_RESPONSE_LEDGER.csv",
    "symbol_match_1281": OUT / "P8_Y5_R10_1281_GAMMA_KHAT_SYMBOL_MATCH_AUDIT.csv",
    "variation_2207": OUT / "P8_Y5_PARENT_QLOC_2207_GAMMA_EFF_METRIC_VARIATION_ATTEMPT.csv",
    "variation_identities_2140": OUT / "P8_Y5_PARENT_QLOC_2140_GAMMAG_VARIATION_IDENTITIES.csv",
}

OUTPUTS = {
    "source_register": OUT / "P8_Y5_R2FR_3455_SOURCE_REGISTER.csv",
    "deltaK_component_ledger": OUT / "P8_Y5_R2FR_3455_DELTAK_COMPONENT_LEDGER.csv",
    "qDeltaK_norm_input": OUT / "P8_Y5_R2FR_3455_QDELTAK_NORM_INPUT.csv",
    "metric_response_promotion_status": OUT / "P8_Y5_R2FR_3455_METRIC_RESPONSE_PROMOTION_STATUS.csv",
    "residual_priority_queue": OUT / "P8_Y5_R2FR_3455_RESIDUAL_PRIORITY_QUEUE.csv",
    "promotion_gates": OUT / "P8_Y5_R2FR_3455_PROMOTION_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_R2FR_3455_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_R2FR_3455_NEXT_TARGET.csv",
    "runner_nonclaim": OUT / "P8_Y5_R2FR_3455_RUNNER_NONCLAIM.csv",
    "validation": OUT / "P8_Y5_BRR545_3455_VALIDATION.csv",
}


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def md_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    fields = list(rows[0].keys())

    def clean(value: Any) -> str:
        return str(value).replace("\n", " ").replace("|", "/")

    return "\n".join(
        [
            "| " + " | ".join(fields) + " |",
            "| " + " | ".join("---" for _ in fields) + " |",
            *["| " + " | ".join(clean(row.get(field, "")) for field in fields) + " |" for row in rows],
        ]
    )


def source_register() -> list[dict[str, Any]]:
    roles = {
        "script_3455": "generator for this checkpoint",
        "doc_3454": "immediate Delta_K handoff",
        "next_3454": "machine-readable 3455 target",
        "typing_3454": "Gamma/Khat/q_loc typing rows",
        "metric_status_3454": "metric-response gap status",
        "active_bound_3454": "first active q_loc/DeltaK bound formulas",
        "sign_lock_2975": "canonical Delta_K convention",
        "metric_response_776": "metric response component ledger",
        "symbol_match_1281": "symbol match audit",
        "variation_2207": "formal metric variation attempts",
        "variation_identities_2140": "Gamma variation identities and countermodels",
    }
    return [
        {
            "source_id": source_id,
            "path": str(path),
            "exists": path.exists(),
            "role": roles[source_id],
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for source_id, path in SOURCES.items()
    ]


def deltaK_component_ledger() -> list[dict[str, Any]]:
    return [
        {
            "component_id": "DKC3455_0_sign_volume",
            "component": "volume/sign convention",
            "definition": "canonical T_q^{mu nu}=Gamma_eff g^{mu nu}-K_hat^{mu nu}; K_metric includes the same volume response",
            "comparison": "Delta_K_volume=0 if SIGN2975 convention is adopted consistently",
            "status": "THEOREM_ZERO_CONVENTION_COMPONENT",
            "remaining_input": "none for convention; still need live Gamma/Khat formulas",
            "feeds_QDeltaK": "0",
            "source_path": str(SOURCES["sign_lock_2975"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "component_id": "DKC3455_1_explicit_metric_dependence",
            "component": "delta_g M_AB/G_AB/potential dependence",
            "definition": "metric response of Gamma_eff internal tensors such as M_AB(g,R_even,D,...) or G_AB(Phi,g)",
            "comparison": "Delta_K_metric = K_hat_metric - K_metric_metric",
            "status": "ACTIVE_COMPONENT_FORMULA_MISSING",
            "remaining_input": "M_AB/G_AB formula, units, and tensor-slot comparison",
            "feeds_QDeltaK": "Q_DeltaK_metric",
            "source_path": str(SOURCES["metric_response_776"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "component_id": "DKC3455_2_derivative_connection_hodge",
            "component": "derivative/connection/Hodge/domain terms",
            "definition": "metric response of nabla, star, connection, projector/domain metric and integration kernel terms",
            "comparison": "Delta_K_deriv = K_hat_deriv - K_metric_deriv including integrations by parts",
            "status": "ACTIVE_COMPONENT_BOUNDARY_ACCOUNTING_OPEN",
            "remaining_input": "derivative term accounting and boundary improvement ledger",
            "feeds_QDeltaK": "Q_DeltaK_derivative",
            "source_path": str(SOURCES["metric_response_776"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "component_id": "DKC3455_3_boundary_reference",
            "component": "boundary/reference/corner improvement",
            "definition": "delta B_GK, B_ref, reference subtraction and corner response",
            "comparison": "Delta_K_boundary = K_hat_boundary - K_metric_boundary",
            "status": "ACTIVE_COMPONENT_BOUNDARY_FLUX_OPEN",
            "remaining_input": "fixed reference class or boundary no-flux theorem",
            "feeds_QDeltaK": "Q_DeltaK_boundary",
            "source_path": str(SOURCES["metric_response_776"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "component_id": "DKC3455_4_external_scalar_branch",
            "component": "external scalar branch",
            "definition": "Gamma_eff prescribed during metric variation",
            "comparison": "D_Gamma=0 by definition, but parent derivation of Gamma_eff is absent",
            "status": "VALID_NARROW_EFFECTIVE_BACKGROUND_NOT_PARENT_MTS",
            "remaining_input": "parent derivation of Gamma_eff or demote to effective background model",
            "feeds_QDeltaK": "not accepted for parent local-GR proof",
            "source_path": str(SOURCES["variation_identities_2140"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "component_id": "DKC3455_5_functional_countermodel",
            "component": "curvature/history functional branch",
            "definition": "Gamma_eff=f(R) or nonlocal H[bar R]",
            "comparison": "Gamma_eff=0 does not force derivative variation zero; f_R or kernel variation can survive",
            "status": "COUNTERMODEL_RETAINED",
            "remaining_input": "double-zero/stationary-kernel condition f_R(Phi0)=0 and kernel support silence",
            "feeds_QDeltaK": "Q_DeltaK_functional",
            "source_path": str(SOURCES["variation_identities_2140"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def qDeltaK_norm_input() -> list[dict[str, Any]]:
    return [
        {
            "input_id": "QDK3455_0_component_sum",
            "feeds": "GKB3454_1_DeltaK_bound",
            "definition": "Q_DeltaK <= Q_metric + Q_derivative + Q_boundary + Q_functional",
            "formula": "Q_DeltaK := ||P_loc nabla_mu Delta_K^{mu nu}|| <= sum_i ||P_loc nabla_mu Delta_K_i^{mu nu}||",
            "units": "stress-divergence / force-density units before response normalization",
            "filled_components": "DeltaK_volume=0",
            "missing_components": "Q_metric;Q_derivative;Q_boundary;Q_functional;P_loc_operator;domain_U;h_obs_norm",
            "current_status": "FIRST_COMPONENT_ZERO_FILLED_TOTAL_BOUND_INPUTS_MISSING",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "input_id": "QDK3455_1_ppn_gamma_envelope",
            "feeds": "GKB3454_0_q_loc_norm_bound",
            "definition": "PPN gamma response envelope for retained DeltaK residual",
            "formula": "|delta gamma_PPN| <= (c^2/(2 U_min)) N_G N_D Q_DeltaK",
            "units": "dimensionless after N_G,N_D,U_min response normalization",
            "filled_components": "symbolic envelope only",
            "missing_components": "U_min;N_G;N_D;Q_DeltaK numeric/theorem bound",
            "current_status": "SYMBOLIC_ENVELOPE_READY_NUMERIC_INPUTS_MISSING",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def metric_response_promotion_status() -> list[dict[str, Any]]:
    return [
        {
            "status_id": "MRP3455_0_convention",
            "question": "Is sign/volume convention blocking?",
            "answer": "No, this part can be consistently locked.",
            "promotion_effect": "removes a bookkeeping ambiguity only",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "status_id": "MRP3455_1_total_DeltaK",
            "question": "Is Delta_K=0 proved?",
            "answer": "No.",
            "promotion_effect": "metric-dependence, derivative/Hodge/projector, boundary/reference and functional countermodel pieces remain open",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "status_id": "MRP3455_2_local_GR",
            "question": "Can local GR/PPN reopen?",
            "answer": "Not yet.",
            "promotion_effect": "q_loc stays a retained residual until active components are zeroed or bounded",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def residual_priority_queue() -> list[dict[str, Any]]:
    return [
        {
            "priority_id": "RPQ3455_0",
            "target": "derivative/connection/Hodge DeltaK component",
            "why_first": "derivative terms are the easiest place to accidentally hide Khat mismatch and boundary improvements",
            "next_action": "write derivative-term accounting or bound Q_DeltaK_derivative",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "priority_id": "RPQ3455_1",
            "target": "boundary/reference DeltaK component",
            "why_first": "even bulk metric-response success can leak through surface/corner terms",
            "next_action": "prove GK boundary exact/no-flux or fill Q_DeltaK_boundary",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def promotion_gates() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "G3455_0_sources_exist",
            "gate": "all cited 3455 source paths exist",
            "status": "PRIVATE_CHECK_PASS",
            "blocks_claim": False,
            "needed_for_claim": "provenance only",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G3455_1_component_ledger",
            "gate": "Delta_K components are split",
            "status": "PASS_LEDGER",
            "blocks_claim": False,
            "needed_for_claim": "active components need zero/bound inputs",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G3455_2_first_component_zero",
            "gate": "volume/sign component filled",
            "status": "PASS_CONVENTION_ZERO",
            "blocks_claim": True,
            "needed_for_claim": "remaining components must close",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G3455_3_total_DeltaK",
            "gate": "Delta_K=0 or Q_DeltaK bound",
            "status": "FAIL_INPUTS_MISSING",
            "blocks_claim": True,
            "needed_for_claim": "Q_metric/Q_derivative/Q_boundary/Q_functional or zero theorems",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G3455_4_no_claim",
            "gate": "no local-GR/Newton/R10/PPN/clock/orbital pass from this checkpoint",
            "status": "ENFORCED",
            "blocks_claim": True,
            "needed_for_claim": "DeltaK/q_loc closure plus arena response",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def decision_ledger() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3455_0",
            "question": "Did Delta_K fully close?",
            "answer": "No.",
            "reason": "Only the convention/volume bookkeeping component can be filled as zero; active derivative, metric-dependence and boundary pieces remain.",
            "next_action": "attack derivative/Hodge/projector component first",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3455_1",
            "question": "Did this move the proof forward?",
            "answer": "Yes.",
            "reason": "Delta_K is now decomposed into named components with a sum-bound interface, so the next work can zero or bound pieces rather than restating a single missing tensor.",
            "next_action": "3456 derivative/Hodge/projector component accounting",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def next_target() -> list[dict[str, Any]]:
    return [
        {
            "target_doc": "3456-Y5-R2FR-DeltaK-derivative-Hodge-projector-component-or-bound-fill-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3456_DeltaK_derivative_Hodge_projector_component_or_bound_fill.py",
            "objective": "Compute or bound the derivative/connection/Hodge/projector part of Delta_K, including integration-by-parts and boundary improvement terms.",
            "start_from": "DKC3455_2_derivative_connection_hodge and QDK3455_0_component_sum",
            "success_gate": "Either Q_DeltaK_derivative=0/exact/boundary-silent, or a source-backed norm input with units is filled.",
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def runner_nonclaim() -> list[dict[str, Any]]:
    return [
        {
            "runner_id": "RUN3455_0",
            "mode": "private_nonclaim_checkpoint",
            "result": "Delta_K component ledger and first zero component plus summed bound interface",
            "claim_status": "NO_LOCAL_GR_NEWTON_R10_PPN_CLOCK_OR_ORBITAL_CLAIM",
            "reason": "active Delta_K components remain unfilled",
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]], start_utc: datetime) -> list[dict[str, Any]]:
    modified_count = 0
    if FORMALIZATION.exists():
        start_timestamp = start_utc.timestamp()
        modified_count = sum(
            1
            for checked_path in FORMALIZATION.rglob("*")
            if checked_path.is_file() and checked_path.stat().st_mtime >= start_timestamp
        )

    nonclaim_ok = True
    for rows in rows_by_name.values():
        for row in rows:
            if "valid_for_claim" in row and str(row["valid_for_claim"]).lower() != "false":
                nonclaim_ok = False
            if "claim_allowed" in row and str(row["claim_allowed"]).lower() != "false":
                nonclaim_ok = False

    parse_ok = True
    for output_name, path in OUTPUTS.items():
        if output_name == "validation":
            continue
        try:
            read_csv(path)
        except csv.Error:
            parse_ok = False

    component_statuses = {row["status"] for row in rows_by_name["deltaK_component_ledger"]}
    first_zero = [
        row for row in rows_by_name["qDeltaK_norm_input"] if row["input_id"] == "QDK3455_0_component_sum"
    ]

    validations = [
        {
            "check_id": "VAL3455_0_sources_exist",
            "condition": "all cited 3455 source paths exist",
            "passed": all(path.exists() for path in SOURCES.values()),
            "detail": f"{sum(1 for path in SOURCES.values() if path.exists())}/{len(SOURCES)} source paths exist",
        },
        {
            "check_id": "VAL3455_1_component_ledger",
            "condition": "Delta_K component ledger includes zero, active, and countermodel components",
            "passed": "THEOREM_ZERO_CONVENTION_COMPONENT" in component_statuses
            and "ACTIVE_COMPONENT_BOUNDARY_ACCOUNTING_OPEN" in component_statuses
            and "COUNTERMODEL_RETAINED" in component_statuses,
            "detail": f"component_statuses={';'.join(sorted(component_statuses))}",
        },
        {
            "check_id": "VAL3455_2_qDeltaK_bound",
            "condition": "Q_DeltaK component-sum bound row exists with first component filled",
            "passed": bool(first_zero)
            and first_zero[0]["filled_components"] == "DeltaK_volume=0"
            and "Q_metric" in first_zero[0]["missing_components"],
            "detail": first_zero[0]["current_status"] if first_zero else "missing QDeltaK row",
        },
        {
            "check_id": "VAL3455_3_no_promotion",
            "condition": "metric response is not promoted",
            "passed": any(
                row["status_id"] == "MRP3455_1_total_DeltaK" and row["answer"] == "No."
                for row in rows_by_name["metric_response_promotion_status"]
            ),
            "detail": "total DeltaK still open",
        },
        {
            "check_id": "VAL3455_4_no_claims",
            "condition": "all generated rows remain nonclaim",
            "passed": nonclaim_ok,
            "detail": "valid_for_claim=false and claim_allowed=false wherever present",
        },
        {
            "check_id": "VAL3455_5_generated_csv_parse",
            "condition": "generated CSV rows parse cleanly",
            "passed": parse_ok,
            "detail": "CSV reader pass for generated outputs present before validation write",
        },
        {
            "check_id": "VAL3455_6_next_target_3456",
            "condition": "next target is derivative/Hodge/projector DeltaK component",
            "passed": rows_by_name["next_target"][0]["target_doc"].startswith("3456-Y5-R2FR-DeltaK-derivative"),
            "detail": rows_by_name["next_target"][0]["target_doc"],
        },
        {
            "check_id": "VAL3455_7_formalization_untouched",
            "condition": "formalization-workbench modified-file count remains 0 during this run",
            "passed": modified_count == 0,
            "detail": f"modified_count_since_start={modified_count}",
        },
    ]
    validations.append(
        {
            "check_id": "VAL3455_8_overall",
            "condition": "3455 DeltaK component checkpoint is internally valid",
            "passed": all(row["passed"] for row in validations),
            "detail": "PASS" if all(row["passed"] for row in validations) else "FAIL",
        }
    )
    return validations


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    text = f"""# 3455 - DeltaK Component Ledger or q_loc Norm First Fill

## Summary
- This checkpoint splits `Delta_K = K_hat - K_metric[Gamma_eff]` instead of leaving it as one opaque tensor.
- The volume/sign convention component is now filled as a theorem-zero bookkeeping component under the canonical 2975 convention.
- The hard parts remain active: explicit metric dependence, derivative/connection/Hodge/projector response, boundary/reference terms, and functional-kernel countermodels.
- `Q_DeltaK` now has a component-sum bound row with `DeltaK_volume=0` filled and the remaining component norms named.
- No local-GR/PPN/Newton claim follows: the live tensor mismatch is smaller, but not closed.

## Source Register
{md_table(rows_by_name["source_register"])}

## DeltaK Component Ledger
{md_table(rows_by_name["deltaK_component_ledger"])}

## QDeltaK Norm Input
{md_table(rows_by_name["qDeltaK_norm_input"])}

## Metric Response Promotion Status
{md_table(rows_by_name["metric_response_promotion_status"])}

## Residual Priority Queue
{md_table(rows_by_name["residual_priority_queue"])}

## Promotion Gates
{md_table(rows_by_name["promotion_gates"])}

## Decision Ledger
{md_table(rows_by_name["decision_ledger"])}

## Next Target
{md_table(rows_by_name["next_target"])}

## Runner Nonclaim
{md_table(rows_by_name["runner_nonclaim"])}

## Validation
{md_table(rows_by_name["validation"])}

## Bottom Line
One component of `Delta_K` is cleaned up, but the important physics is still in the derivative/Hodge/projector and boundary pieces. The next best shot is to compute or bound the derivative component first, because that is where a fake metric-response match most easily hides.
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    start_utc = datetime.now(timezone.utc)
    rows_by_name = {
        "source_register": source_register(),
        "deltaK_component_ledger": deltaK_component_ledger(),
        "qDeltaK_norm_input": qDeltaK_norm_input(),
        "metric_response_promotion_status": metric_response_promotion_status(),
        "residual_priority_queue": residual_priority_queue(),
        "promotion_gates": promotion_gates(),
        "decision_ledger": decision_ledger(),
        "next_target": next_target(),
        "runner_nonclaim": runner_nonclaim(),
    }
    for output_name, rows in rows_by_name.items():
        write_csv(OUTPUTS[output_name], rows)
    rows_by_name["validation"] = validation_rows(rows_by_name, start_utc)
    write_csv(OUTPUTS["validation"], rows_by_name["validation"])
    write_doc(rows_by_name)
    failed_rows = [row for row in rows_by_name["validation"] if not row["passed"]]
    if failed_rows:
        raise SystemExit(f"3455 validation failed: {failed_rows}")
    print(f"wrote {DOC}")
    print(f"wrote {len(OUTPUTS)} csv outputs")


if __name__ == "__main__":
    main()
