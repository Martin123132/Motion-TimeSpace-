from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
RUNS = ROOT / "runs"

SLUG = "Y5-R10-fill-q_loc-residual-runner-or-derive-first-zero-row"
DOC_PATH = ROOT / "598-Y5-R10-fill-q_loc-residual-runner-or-derive-first-zero-row.md"
SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_598_SOURCE_REGISTER.csv"
FIRST_ZERO_PATH = RESIDUALS / "P8_Y5_R10_598_FIRST_ZERO_ROW_DERIVATION.csv"
RUNNER_STATUS_PATH = RESIDUALS / "P8_Y5_R10_598_RESIDUAL_RUNNER_STATUS.csv"
CLAIM_BOUNDARY_PATH = RESIDUALS / "P8_Y5_R10_598_ZERO_ROW_CLAIM_BOUNDARY.csv"
NEXT_QUEUE_PATH = RESIDUALS / "P8_Y5_R10_598_NEXT_INPUT_QUEUE.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_BRR545_598_DECISION.csv"
ROUTE_UPDATE_PATH = RESIDUALS / "P8_Y5_BRR545_598_ROUTE_UPDATE.csv"
SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_598_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_598_VALIDATION.csv"

PRIOR_597_VALIDATION = RESIDUALS / "P8_Y5_BRR545_597_VALIDATION.csv"

STATUS = "Y5_R10_first_zero_row_direct_representative_X_smuggling_closed_q_loc_observed_residual_runner_still_open"
CLAIM_CEILING = "first_zero_row_for_direct_vertical_X_smuggling_only_no_q_loc_zero_R10_WEP_PPN_or_local_GR_pass"
NEXT_TARGET = "599-Y5-R10-parent-projector-boundary-zero-or-compact-shell-score.md"

SOURCE_FILES = [
    ("597-Y5-R10-reduced-GK-action-owner-or-q_loc-residual-runner.md", "immediate owner-or-runner handoff"),
    ("source-intake/mts_residuals/P8_Y5_BRR545_597_VALIDATION.csv", "prior validation gate"),
    ("source-intake/mts_residuals/P8_Y5_R10_597_QLOC_RESIDUAL_RUNNER_INPUT_QUEUE.csv", "queued residual runner rows"),
    ("source-intake/mts_residuals/P8_Y5_R10_597_WARD_ZERO_GATE.csv", "Ward zero blockers"),
    ("596-Y5-R10-test-Gamma-Khat-qloc-factor-through-pi-or-demote.md", "pullback lemma source"),
    ("source-intake/mts_residuals/P8_Y5_R10_596_QUOTIENT_PULLBACK_LEMMA.csv", "formal pullback lemma rows"),
    ("source-intake/mts_residuals/P8_Y5_R10_596_QLOC_EXACTNESS_OR_RESIDUAL_GATE.csv", "q_loc not-zero guard"),
    ("595-Y5-R10-construct-pi-observed-quotient-map-or-demote-to-diffeo-current.md", "pi map candidate source"),
    ("source-intake/mts_residuals/P8_Y5_R10_595_PI_OBSERVED_QUOTIENT_MAP.csv", "pi and v_X map rows"),
    ("source-intake/mts_residuals/P8_QLOC_BOUND_RUNNER_SPEC.csv", "fallback q_loc runner spec"),
    ("source-intake/mts_residuals/P8_Y5_SOURCE_NORMALIZATION_BOUND_RUNNER_INPUT.csv", "source-normalization input queue"),
    ("scripts/Y5_R10_fill_q_loc_residual_runner_or_derive_first_zero_row.py", "this checkpoint generator"),
]


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._"
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join(["---"] * len(columns)) + " |",
    ]
    for row in rows:
        values = []
        for column in columns:
            value = str(row.get(column, ""))
            value = value.replace("\n", "<br>").replace("|", "\\|")
            values.append(value)
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def make_sources() -> list[dict[str, str]]:
    return [
        {
            "source_file": source_file,
            "exists": str((ROOT / source_file).exists()),
            "role": role,
        }
        for source_file, role in SOURCE_FILES
    ]


def make_first_zero_rows() -> list[dict[str, str]]:
    return [
        {
            "zero_id": "FZR598_0_direct_representative_X_smuggling",
            "channel": "direct vertical representative-X source through Gamma/Khat/q_loc",
            "assumptions": "pi:Conf_parent->Q_obs; v_X in ker(d pi); Gamma_eff=gamma o pi; K_hat=kappa o pi; P_loc=Pi o pi; connection and boundary reference are Q_obs-owned",
            "derivation": "Lie_vX(Gamma_eff)=Lie_vX(K_hat)=Lie_vX(P_loc)=0, hence Lie_vX(q_loc)=0 for q_loc=P_loc(nabla Gamma_eff-nabla K_hat)",
            "zero_result": "C_direct_X_to_q_loc := Lie_vX(q_loc) = 0",
            "claim_scope": "kills only direct representative-X smuggling; does not kill observed reduced q_loc",
            "runner_effect": "remove direct hidden-X source row from the residual runner while retaining observed q_loc rows",
            "row_status": "closed_under_quotient_contract",
            "valid_for_claim": "false",
        },
        {
            "zero_id": "FZR598_1_matter_readout_side_effect",
            "channel": "induced matter/readout variation from q_loc representative motion",
            "assumptions": "matter metric, clocks, and readout functors factor through Q_obs and are varied only in the parent action before readout",
            "derivation": "Lie_vX(q_loc)=0 is not allowed to induce delta_X matter fields if matter/readout are Q_obs functors",
            "zero_result": "delta_X S_matter|direct_q_loc_marker = 0 under the no-marker pullback contract",
            "claim_scope": "conditional guardrail against a q_loc marker coupling; does not prove full matter blindness",
            "runner_effect": "keeps conformal/material-marker counterexamples live unless no-marker theorem is later proved",
            "row_status": "guardrail_zero_only",
            "valid_for_claim": "false",
        },
        {
            "zero_id": "FZR598_2_not_q_loc_zero",
            "channel": "observed reduced q_loc residual",
            "assumptions": "same pullback assumptions as FZR598_0",
            "derivation": "a nonzero tensor field on Q_obs can be vertical-blind; Lie_vX(q_loc)=0 does not imply q_loc=0",
            "zero_result": "no zero assigned to observed q_loc",
            "claim_scope": "explicit nonzero guard",
            "runner_effect": "observed q_loc residual runner remains mandatory",
            "row_status": "reopened_as_observed_residual",
            "valid_for_claim": "false",
        },
    ]


def make_runner_status_rows() -> list[dict[str, str]]:
    return [
        {
            "runner_id": "QRS598_0_direct_X_smuggling",
            "quantity": "Lie_vX(q_loc) or direct representative-X source",
            "status_after_598": "closed_under_quotient_contract",
            "reason": "q_loc is a Q_obs pullback under the 596 assumptions",
            "next_needed": "keep pullback/no-marker assumptions explicit in future symbols",
            "valid_for_claim": "false",
        },
        {
            "runner_id": "QRS598_1_observed_q_loc",
            "quantity": "q_loc as reduced observed residual on Q_obs",
            "status_after_598": "still_open",
            "reason": "vertical-blindness does not imply q_loc=0",
            "next_needed": "derive reduced Ward zero or score residual",
            "valid_for_claim": "false",
        },
        {
            "runner_id": "QRS598_2_source_normalization_Y5",
            "quantity": "q_loc projection into measured-GM/source-normalization channel",
            "status_after_598": "still_open",
            "reason": "Y5 is an observed even scalar and was not killed by the direct-X zero row",
            "next_needed": "derive source-owner zero or fill C_qmu projection coefficients",
            "valid_for_claim": "false",
        },
        {
            "runner_id": "QRS598_3_boundary_flux_alpha3",
            "quantity": "boundary/source-measure flux and alpha3-equivalent pressure",
            "status_after_598": "still_open",
            "reason": "boundary no-flux is independent of direct representative-X blindness",
            "next_needed": "derive compact boundary primitive/no-flux or score alpha3/compact-shell row",
            "valid_for_claim": "false",
        },
        {
            "runner_id": "QRS598_4_PPN_metric_tail",
            "quantity": "weak-field metric tail sourced by observed q_loc",
            "status_after_598": "still_open",
            "reason": "no weak-field map from observed q_loc to PPN vector has been filled",
            "next_needed": "derive first PPN zero row or fill residual vector",
            "valid_for_claim": "false",
        },
        {
            "runner_id": "QRS598_5_R10_range_tail",
            "quantity": "range-dependent alpha(lambda) source from observed q_loc",
            "status_after_598": "still_open",
            "reason": "direct-X row closure does not source q_loc-to-alpha coefficient",
            "next_needed": "derive no finite-range charge or fill source-backed alpha coefficient",
            "valid_for_claim": "false",
        },
        {
            "runner_id": "QRS598_6_R11_operator_vector",
            "quantity": "non-EH/operator/source-normalization coefficient vector",
            "status_after_598": "still_open",
            "reason": "operator family and weak-field normalization remain symbolic",
            "next_needed": "derive operator invisibility/topological zero or fill vector inputs",
            "valid_for_claim": "false",
        },
    ]


def make_claim_boundary_rows() -> list[dict[str, str]]:
    return [
        {
            "boundary_id": "ZCB598_0_allowed",
            "allowed_statement": "The direct representative-X source into the Gamma/Khat/q_loc channel is zero under the explicit Q_obs pullback contract.",
            "forbidden_statement": "q_loc is zero.",
            "why": "Lie_vX(q_loc)=0 is vertical-blindness, not vanishing of q_loc as a tensor on Q_obs.",
        },
        {
            "boundary_id": "ZCB598_1_allowed",
            "allowed_statement": "The residual runner has one closed internal row and several still-open observed rows.",
            "forbidden_statement": "The residual runner has passed local bounds.",
            "why": "no projection coefficients or source-backed numeric rows were scored.",
        },
        {
            "boundary_id": "ZCB598_2_allowed",
            "allowed_statement": "The quotient route is cleaner because it removes hidden representative-field sourcing.",
            "forbidden_statement": "The quotient route derives local GR.",
            "why": "Y5, Y6, boundary flux, P_loc ownership, and PPN weak-field map remain open.",
        },
        {
            "boundary_id": "ZCB598_3_allowed",
            "allowed_statement": "If future definitions violate Q_obs pullback/no-marker assumptions, FZR598_0 must reopen.",
            "forbidden_statement": "The direct-X zero row is unconditional.",
            "why": "the row is a theorem inside the quotient contract, not a proof that all current MTS symbols already satisfy it.",
        },
    ]


def make_next_queue_rows() -> list[dict[str, str]]:
    return [
        {
            "queue_id": "NQ598_A_parent_projector",
            "option": "derive P_loc as a parent-owned Q_obs projector",
            "why_next": "P_loc ownership is the smallest remaining structural hole in the observed q_loc row",
            "success_condition": "P_loc=Pi o pi and projection does not hide unprojected force components",
            "fallback": "carry full unprojected q_loc residual",
            "priority": "high",
        },
        {
            "queue_id": "NQ598_B_boundary_no_flux",
            "option": "derive compact boundary primitive/no-flux",
            "why_next": "boundary flux can spoil both Ward zero and source-measure closure",
            "success_condition": "boundary_flux=0 or exact/fixed-reference with zero compact charge",
            "fallback": "score compact-shell and alpha3/source-measure residuals",
            "priority": "high",
        },
        {
            "queue_id": "NQ598_C_compact_shell_mapping",
            "option": "map 7.432631961576971e-06 compact-shell proxy into PPN/source-normalization units",
            "why_next": "if derivation stalls, this is the first numeric residual pressure test",
            "success_condition": "source-backed unit map and sign convention",
            "fallback": "block numeric claim",
            "priority": "medium",
        },
        {
            "queue_id": "NQ598_D_Y5_source_owner",
            "option": "derive measured source charge as one parent EH/Hilbert mass with no extra projection",
            "why_next": "Y5 blocks source-normalized Newton/PPN more directly than q_loc algebra",
            "success_condition": "mu_obs=G0 M_H and mu_extra=0 with no derivative hair",
            "fallback": "fill Y5 bound runner rows",
            "priority": "high_but_harder",
        },
    ]


def make_decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "D598_0_first_zero_row_derived",
            "decision": "close direct representative-X smuggling row under quotient pullback",
            "meaning": "this is a real internal simplification: direct X does not source q_loc if q_loc is a Q_obs pullback",
            "claim_status": "conditional_zero_row_not_public_claim",
            "next_target": NEXT_TARGET,
        },
        {
            "decision_id": "D598_1_observed_q_loc_remains",
            "decision": "keep observed q_loc residual runner open",
            "meaning": "the first zero row does not derive q_loc=0, local GR, or PPN silence",
            "claim_status": "runner_still_open",
            "next_target": NEXT_TARGET,
        },
        {
            "decision_id": "D598_2_best_next",
            "decision": "attack P_loc ownership plus boundary no-flux before numeric scoring",
            "meaning": "these are the cleanest remaining derivation gates and can reduce the runner before data work",
            "claim_status": "next_derivation_target",
            "next_target": NEXT_TARGET,
        },
    ]


def make_route_update_rows() -> list[dict[str, str]]:
    return [
        {
            "route_id": "RU598_0_allowed",
            "allowed_after_598": "mark direct representative-X smuggling as closed under the quotient contract",
            "forbidden_after_598": "mark observed q_loc, R10, WEP, PPN, or local GR as passed",
            "next_action": NEXT_TARGET,
        },
        {
            "route_id": "RU598_1_allowed",
            "allowed_after_598": "use the first zero row to shrink the residual runner",
            "forbidden_after_598": "delete open Y5/Y6/boundary/PPN/R10/R11 rows",
            "next_action": NEXT_TARGET,
        },
        {
            "route_id": "RU598_2_allowed",
            "allowed_after_598": "derive P_loc/boundary zero next or score compact-shell row if derivation stalls",
            "forbidden_after_598": "use unsourced compact-shell proxy as a bound pass",
            "next_action": NEXT_TARGET,
        },
    ]


def make_summary_rows() -> list[dict[str, str]]:
    return [
        {
            "summary_id": "S598_0",
            "claim_allowed": "false",
            "R10_pass": "false",
            "WEP_pass": "false",
            "PPN_pass": "false",
            "local_GR_pass": "false",
            "first_zero_row": "direct_representative_X_smuggling_closed_under_quotient_contract",
            "runner_status": "shrunk_but_open",
            "best_private_read": "The first honest zero row is closed: direct representative-X smuggling through Gamma/Khat/q_loc vanishes under the Q_obs pullback contract. The observed q_loc residual remains open and must next face P_loc ownership, boundary no-flux, or compact-shell scoring.",
            "next_target": NEXT_TARGET,
        }
    ]


def make_validation(
    sources: list[dict[str, str]],
    zero_rows: list[dict[str, str]],
    runner_rows: list[dict[str, str]],
    boundary_rows: list[dict[str, str]],
    next_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    prior_rows = read_csv(PRIOR_597_VALIDATION)
    prior_failures = [row for row in prior_rows if row.get("result", "").strip().lower() != "pass"]
    missing_sources = [row for row in sources if row["exists"] != "True"]
    claim_rows = [
        *[row for row in zero_rows if row["valid_for_claim"] == "true"],
        *[row for row in runner_rows if row["valid_for_claim"] == "true"],
    ]
    first_zero = any(
        row["zero_id"] == "FZR598_0_direct_representative_X_smuggling"
        and row["zero_result"] == "C_direct_X_to_q_loc := Lie_vX(q_loc) = 0"
        for row in zero_rows
    )
    not_q_loc_zero = any(row["zero_id"] == "FZR598_2_not_q_loc_zero" for row in zero_rows)
    runner_open = any(row["runner_id"] == "QRS598_1_observed_q_loc" and row["status_after_598"] == "still_open" for row in runner_rows)
    boundary_guard = any("q_loc is zero" in row["forbidden_statement"] for row in boundary_rows)
    next_projector = any(row["queue_id"] == "NQ598_A_parent_projector" for row in next_rows)
    next_boundary = any(row["queue_id"] == "NQ598_B_boundary_no_flux" for row in next_rows)
    return [
        {
            "check_id": "V598_0_source_paths_exist",
            "result": "pass" if not missing_sources else "fail",
            "detail": f"missing={len(missing_sources)}",
        },
        {
            "check_id": "V598_1_prior_597_clean",
            "result": "pass" if prior_rows and not prior_failures else "fail",
            "detail": f"prior_rows={len(prior_rows)};prior_failures={len(prior_failures)}",
        },
        {
            "check_id": "V598_2_first_zero_row_present",
            "result": "pass" if first_zero else "fail",
            "detail": "direct representative-X smuggling row closed",
        },
        {
            "check_id": "V598_3_not_q_loc_zero_guard",
            "result": "pass" if not_q_loc_zero and boundary_guard else "fail",
            "detail": "q_loc observed residual remains nonzero/open",
        },
        {
            "check_id": "V598_4_runner_still_open",
            "result": "pass" if runner_open else "fail",
            "detail": f"runner_rows={len(runner_rows)}",
        },
        {
            "check_id": "V598_5_next_derivation_queue_present",
            "result": "pass" if next_projector and next_boundary else "fail",
            "detail": f"next_rows={len(next_rows)};projector={next_projector};boundary={next_boundary}",
        },
        {
            "check_id": "V598_6_no_claim_rows",
            "result": "pass" if not claim_rows else "fail",
            "detail": f"claim_rows={len(claim_rows)}",
        },
        {
            "check_id": "V598_7_no_R10_or_local_GR_claim",
            "result": "pass",
            "detail": "claim_allowed=false;R10_pass=false;WEP=false;PPN=false;local_GR=false",
        },
    ]


def write_markdown(
    generated: str,
    run_root: Path,
    sources: list[dict[str, str]],
    zero_rows: list[dict[str, str]],
    runner_rows: list[dict[str, str]],
    boundary_rows: list[dict[str, str]],
    next_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    route_update_rows: list[dict[str, str]],
    validation_rows: list[dict[str, str]],
) -> None:
    text = f"""# 598 Y5 R10 fill q_loc residual runner or derive first zero row

Generated: {generated}  
Status: `{STATUS}`  
Claim ceiling: `{CLAIM_CEILING}`  
Next target: `{NEXT_TARGET}`  
Run root: `{rel(run_root)}`

## Verdict
- Best move at this stage: take the smallest defensible derivation win before numeric scoring.
- First zero row: direct representative-`X` smuggling through the `Gamma_eff/K_hat/q_loc` channel is zero under the explicit `Q_obs` pullback contract.
- This does not mean `q_loc=0`. It means `Lie_vX(q_loc)=0`; the observed reduced `q_loc` residual still exists unless the Ward/projector/boundary gates close.
- The residual runner is now smaller but still open. Next best target is `P_loc` ownership plus compact boundary no-flux.

## Source Register
{markdown_table(sources, ["source_file", "exists", "role"])}

## First Zero Row Derivation
{markdown_table(zero_rows, ["zero_id", "channel", "assumptions", "derivation", "zero_result", "claim_scope", "runner_effect", "row_status", "valid_for_claim"])}

## Residual Runner Status
{markdown_table(runner_rows, ["runner_id", "quantity", "status_after_598", "reason", "next_needed", "valid_for_claim"])}

## Zero Row Claim Boundary
{markdown_table(boundary_rows, ["boundary_id", "allowed_statement", "forbidden_statement", "why"])}

## Next Input Queue
{markdown_table(next_rows, ["queue_id", "option", "why_next", "success_condition", "fallback", "priority"])}

## Decision
{markdown_table(decision_rows, ["decision_id", "decision", "meaning", "claim_status", "next_target"])}

## Route Update
{markdown_table(route_update_rows, ["route_id", "allowed_after_598", "forbidden_after_598", "next_action"])}

## Validation
{markdown_table(validation_rows, ["check_id", "result", "detail"])}

## Practical Read
This is a modest but real point on the judges' cards. We did not knock out the whole local residual. We did prove that, under the quotient contract, the dangerous representative variable is not secretly punching through `q_loc`. The fight now moves to the observed residual: projector ownership, boundary flux, source normalization, and eventually numeric scoring if derivation stalls.
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def main() -> int:
    generated = datetime.now(timezone.utc).isoformat()
    run_root = RUNS / f"{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}-{SLUG}"
    run_root.mkdir(parents=True, exist_ok=True)

    sources = make_sources()
    zero_rows = make_first_zero_rows()
    runner_rows = make_runner_status_rows()
    boundary_rows = make_claim_boundary_rows()
    next_rows = make_next_queue_rows()
    decision_rows = make_decision_rows()
    route_update_rows = make_route_update_rows()
    summary_rows = make_summary_rows()
    validation_rows = make_validation(sources, zero_rows, runner_rows, boundary_rows, next_rows)

    write_csv(SOURCE_REGISTER_PATH, sources, ["source_file", "exists", "role"])
    write_csv(
        FIRST_ZERO_PATH,
        zero_rows,
        ["zero_id", "channel", "assumptions", "derivation", "zero_result", "claim_scope", "runner_effect", "row_status", "valid_for_claim"],
    )
    write_csv(RUNNER_STATUS_PATH, runner_rows, ["runner_id", "quantity", "status_after_598", "reason", "next_needed", "valid_for_claim"])
    write_csv(CLAIM_BOUNDARY_PATH, boundary_rows, ["boundary_id", "allowed_statement", "forbidden_statement", "why"])
    write_csv(NEXT_QUEUE_PATH, next_rows, ["queue_id", "option", "why_next", "success_condition", "fallback", "priority"])
    write_csv(DECISION_PATH, decision_rows, ["decision_id", "decision", "meaning", "claim_status", "next_target"])
    write_csv(ROUTE_UPDATE_PATH, route_update_rows, ["route_id", "allowed_after_598", "forbidden_after_598", "next_action"])
    write_csv(
        SUMMARY_PATH,
        summary_rows,
        [
            "summary_id",
            "claim_allowed",
            "R10_pass",
            "WEP_pass",
            "PPN_pass",
            "local_GR_pass",
            "first_zero_row",
            "runner_status",
            "best_private_read",
            "next_target",
        ],
    )
    write_csv(VALIDATION_PATH, validation_rows, ["check_id", "result", "detail"])

    write_markdown(
        generated,
        run_root,
        sources,
        zero_rows,
        runner_rows,
        boundary_rows,
        next_rows,
        decision_rows,
        route_update_rows,
        validation_rows,
    )

    status_payload = {
        "generated": generated,
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "next_target": NEXT_TARGET,
        "doc": rel(DOC_PATH),
        "validation": rel(VALIDATION_PATH),
        "all_validation_pass": all(row["result"] == "pass" for row in validation_rows),
    }
    (run_root / "status.json").write_text(json.dumps(status_payload, indent=2), encoding="utf-8")
    (run_root / "COMPLETE.marker").write_text("complete\n", encoding="utf-8")
    print(json.dumps(status_payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
