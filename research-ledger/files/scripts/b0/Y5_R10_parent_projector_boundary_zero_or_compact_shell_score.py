from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
RUNS = ROOT / "runs"

SLUG = "Y5-R10-parent-projector-boundary-zero-or-compact-shell-score"
DOC_PATH = ROOT / "599-Y5-R10-parent-projector-boundary-zero-or-compact-shell-score.md"
SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_599_SOURCE_REGISTER.csv"
PROJECTOR_PATH = RESIDUALS / "P8_Y5_R10_599_PARENT_PROJECTOR_OWNERSHIP_ATTEMPT.csv"
BOUNDARY_PATH = RESIDUALS / "P8_Y5_R10_599_BOUNDARY_NO_FLUX_ATTEMPT.csv"
COMPACT_SCORE_PATH = RESIDUALS / "P8_Y5_R10_599_COMPACT_SHELL_SCORE_STATUS.csv"
FORK_PATH = RESIDUALS / "P8_Y5_R10_599_DERIVE_OR_SCORE_FORK.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_BRR545_599_DECISION.csv"
ROUTE_UPDATE_PATH = RESIDUALS / "P8_Y5_BRR545_599_ROUTE_UPDATE.csv"
SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_599_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_599_VALIDATION.csv"

PRIOR_598_VALIDATION = RESIDUALS / "P8_Y5_BRR545_598_VALIDATION.csv"

STATUS = "Y5_R10_parent_projector_and_boundary_zero_attempt_written_compact_shell_score_blocked_by_unit_map"
CLAIM_CEILING = "projector_boundary_attempt_and_compact_shell_score_blocker_only_no_q_loc_zero_R10_WEP_PPN_or_local_GR_pass"
NEXT_TARGET = "600-Y5-R10-projector-algebra-or-boundary-primitive-fill.md"

SOURCE_FILES = [
    ("598-Y5-R10-fill-q_loc-residual-runner-or-derive-first-zero-row.md", "immediate first-zero-row handoff"),
    ("source-intake/mts_residuals/P8_Y5_BRR545_598_VALIDATION.csv", "prior validation gate"),
    ("source-intake/mts_residuals/P8_Y5_R10_598_RESIDUAL_RUNNER_STATUS.csv", "open runner status"),
    ("source-intake/mts_residuals/P8_Y5_R10_598_NEXT_INPUT_QUEUE.csv", "projector/boundary next queue"),
    ("597-Y5-R10-reduced-GK-action-owner-or-q_loc-residual-runner.md", "reduced owner and runner trigger"),
    ("source-intake/mts_residuals/P8_Y5_R10_597_WARD_ZERO_GATE.csv", "Ward zero blockers"),
    ("219-compact-shell-q_loc-source-projection-attempt.md", "compact-shell q_loc projection and budget"),
    ("220-Jrel-local-trivial-representative-or-closure-bound.md", "J_rel exactness and compact-shell bound"),
    ("581-Y5-R10-quotient-vertical-no-pole-parent-theorem-attempt.md", "boundary charge and no-pole theorem conditions"),
    ("582-Y5-R10-boundary-charge-and-constraint-algebra-no-pole-audit.md", "boundary differentiability and Dirac audit"),
    ("513-Gamma-Khat-q_loc-first-variation-or-demotion.md", "q_loc stress divergence identity"),
    ("514-construct-GK-stress-action-or-residual-bound.md", "metric response action candidate"),
    ("scripts/Y5_R10_parent_projector_boundary_zero_or_compact_shell_score.py", "this checkpoint generator"),
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


def make_projector_rows() -> list[dict[str, str]]:
    return [
        {
            "projector_id": "PPO599_0_parent_definition",
            "object": "P_loc",
            "candidate_definition": "P_loc[Y]=Pi[Q_obs]=Pi o pi, chosen before readout as a parent-owned reduced tensor/projector",
            "required_test": "idempotent, covariant, Q_obs-owned, and fixed by the parent action/domain rule rather than fitted after solving",
            "derivation_result": "formal_contract_written",
            "blocker": "actual Pi algebra and parent domain rule are not yet derived",
            "valid_for_claim": "false",
        },
        {
            "projector_id": "PPO599_1_no_hidden_force",
            "object": "projection honesty",
            "candidate_definition": "ker(P_loc) may contain only unobservable representative directions or separately bounded components",
            "required_test": "P_loc R=0 cannot be used to discard an observed force component without a theorem or residual row",
            "derivation_result": "policy_gate_passes_contract_only",
            "blocker": "full unprojected q_loc residual vector is not mapped",
            "valid_for_claim": "false",
        },
        {
            "projector_id": "PPO599_2_vertical_commutation",
            "object": "vertical-blind projector",
            "candidate_definition": "Lie_vX(P_loc)=0 because P_loc=Pi o pi and d pi(v_X)=0",
            "required_test": "future Gamma/Khat/q_loc definitions keep P_loc on Q_obs, not on representative fibre data",
            "derivation_result": "conditional_zero_for_direct_X_projector_variation",
            "blocker": "does not imply P_loc annihilates observed q_loc",
            "valid_for_claim": "false",
        },
        {
            "projector_id": "PPO599_3_pointwise_annihilation",
            "object": "P_loc d_rel J_rel",
            "candidate_definition": "P_loc d_rel J_rel=0 pointwise in compact local vacuum",
            "required_test": "J_rel exact/trivial representative plus Pi annihilates the remaining memory-exchange class pointwise",
            "derivation_result": "not_derived",
            "blocker": "220 only gave conditional integrated exactness and retained pointwise failure",
            "valid_for_claim": "false",
        },
        {
            "projector_id": "PPO599_4_observed_residual",
            "object": "observed q_loc",
            "candidate_definition": "q_loc_obs=P_loc nabla_mu T_GK^{mu nu} on Q_obs",
            "required_test": "Ward zero, source-free Euler equations, boundary no-flux, and honest projection all pass",
            "derivation_result": "still_open",
            "blocker": "P_loc ownership alone cannot derive observed q_loc=0",
            "valid_for_claim": "false",
        },
    ]


def make_boundary_rows() -> list[dict[str, str]]:
    return [
        {
            "boundary_id": "BNF599_0_proper_vertical_boundary",
            "condition": "representative-X variations are compactly supported or fixed on the compact local boundary",
            "would_zero": "direct vertical-X boundary charge",
            "derivation_result": "conditional_zero_available_for_representative_X",
            "blocker": "this is not the observed q_loc/source-measure boundary flux",
            "valid_for_claim": "false",
        },
        {
            "boundary_id": "BNF599_1_reduced_GK_boundary",
            "condition": "S_GK^red boundary variation has exact/fixed-reference primitive B_GK with zero compact local charge",
            "would_zero": "boundary_flux in the reduced Ward identity",
            "derivation_result": "not_derived",
            "blocker": "B_GK is not constructed from actual Gamma/Khat metric response",
            "valid_for_claim": "false",
        },
        {
            "boundary_id": "BNF599_2_Jrel_exact_primitive",
            "condition": "J_rel=d_rel A_rel and A_rel vanishes or matches pure gauge on inner and outer compact shell boundaries",
            "would_zero": "integrated d_rel J_rel exchange through compact collar",
            "derivation_result": "conditional_integrated_zero_only",
            "blocker": "pointwise P_loc d_rel J_rel=0 not derived; ordinary GR mass flux must remain separated",
            "valid_for_claim": "false",
        },
        {
            "boundary_id": "BNF599_3_source_measure_flux",
            "condition": "no boundary/domain/projector/memory term contributes to measured source mass, alpha3, xi, Gdot, or PPN source rows",
            "would_zero": "source-measure/PPN boundary residual",
            "derivation_result": "still_open",
            "blocker": "source-measure projection and PPN map are not filled",
            "valid_for_claim": "false",
        },
    ]


def make_compact_score_rows() -> list[dict[str, str]]:
    return [
        {
            "score_id": "CSS599_0_budget_import",
            "quantity": "worst compact-shell leakage budget",
            "input_value": "7.432631961576971e-06",
            "source": "220-Jrel-local-trivial-representative-or-closure-bound.md",
            "score_status": "available_as_internal_proxy",
            "why_not_claim": "dimensionless proxy is not mapped to PPN/source-normalization/R10/R11 units",
            "valid_for_claim": "false",
        },
        {
            "score_id": "CSS599_1_unit_map",
            "quantity": "compact-shell proxy -> physical residual units",
            "input_value": "missing",
            "source": "not yet sourced",
            "score_status": "blocked",
            "why_not_claim": "no C_qmu, PPN weak-field, alpha(lambda), or source-normalization projection operator",
            "valid_for_claim": "false",
        },
        {
            "score_id": "CSS599_2_alpha3_pressure",
            "quantity": "boundary/momentum flux -> alpha3 equivalent",
            "input_value": "alpha3 lock 4e-20 where applicable",
            "source": "prior local residual locks",
            "score_status": "blocked",
            "why_not_claim": "coefficient from boundary/q_loc flux to alpha3 is not derived",
            "valid_for_claim": "false",
        },
        {
            "score_id": "CSS599_3_R10_range",
            "quantity": "q_loc/range leakage -> alpha(lambda)",
            "input_value": "missing coefficient",
            "source": "R10 runner infrastructure only",
            "score_status": "blocked",
            "why_not_claim": "real bound curve alone is useless without q_loc-to-alpha coefficient and lambda",
            "valid_for_claim": "false",
        },
        {
            "score_id": "CSS599_4_score_verdict",
            "quantity": "compact-shell score",
            "input_value": "not scored",
            "source": "this checkpoint",
            "score_status": "score_deferred",
            "why_not_claim": "derivation gates are preferred and numeric unit map is absent",
            "valid_for_claim": "false",
        },
    ]


def make_fork_rows() -> list[dict[str, str]]:
    return [
        {
            "fork_id": "F599_A_projector_derivation",
            "condition": "P_loc=Pi o pi with parent algebra, idempotence, covariance, no hidden observed-force kernel",
            "result_if_success": "projector ownership closes; observed q_loc still needs Ward/boundary zero",
            "status": "open",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "fork_id": "F599_B_boundary_primitive",
            "condition": "B_GK/A_rel compact primitive is constructed and gives zero source-measure flux",
            "result_if_success": "boundary flux row closes and compact-shell score pressure weakens",
            "status": "open",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "fork_id": "F599_C_compact_shell_score",
            "condition": "projector/boundary derivation stalls and source-backed unit map is built",
            "result_if_success": "score compact-shell residual against physical local locks",
            "status": "blocked_pending_unit_map",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
        },
    ]


def make_decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "D599_0_derivation_before_score",
            "decision": "attempt P_loc ownership and boundary no-flux before compact-shell scoring",
            "meaning": "numeric proxy is not claim-safe without a unit/projection map",
            "claim_status": "private_derivation_route",
            "next_target": NEXT_TARGET,
        },
        {
            "decision_id": "D599_1_projector_contract_written",
            "decision": "write parent projector ownership contract",
            "meaning": "P_loc must be parent-owned and honest; it cannot hide observed residuals",
            "claim_status": "contract_only",
            "next_target": NEXT_TARGET,
        },
        {
            "decision_id": "D599_2_boundary_not_closed",
            "decision": "keep boundary/source-measure flux open",
            "meaning": "proper representative-X boundary zero does not kill observed q_loc/source-measure boundary flux",
            "claim_status": "boundary_zero_false_for_current_claim",
            "next_target": NEXT_TARGET,
        },
        {
            "decision_id": "D599_3_compact_score_deferred",
            "decision": "defer compact-shell score",
            "meaning": "7.432631961576971e-06 remains an internal cage, not a physical local-bound pass",
            "claim_status": "score_blocked",
            "next_target": NEXT_TARGET,
        },
    ]


def make_route_update_rows() -> list[dict[str, str]]:
    return [
        {
            "route_id": "RU599_0_allowed",
            "allowed_after_599": "use P_loc ownership as the next theorem target",
            "forbidden_after_599": "treat P_loc projection as proof of q_loc=0",
            "next_action": NEXT_TARGET,
        },
        {
            "route_id": "RU599_1_allowed",
            "allowed_after_599": "use compact-shell budget as internal pressure only",
            "forbidden_after_599": "claim compact-shell score without physical unit map",
            "next_action": NEXT_TARGET,
        },
        {
            "route_id": "RU599_2_allowed",
            "allowed_after_599": "try to construct boundary primitive or parent projector algebra",
            "forbidden_after_599": "delete Y5/Y6/PPN/R10/R11 residual rows",
            "next_action": NEXT_TARGET,
        },
    ]


def make_summary_rows() -> list[dict[str, str]]:
    return [
        {
            "summary_id": "S599_0",
            "claim_allowed": "false",
            "R10_pass": "false",
            "WEP_pass": "false",
            "PPN_pass": "false",
            "local_GR_pass": "false",
            "projector_status": "contract_written_not_derived",
            "boundary_status": "direct_X_zero_only_observed_flux_open",
            "compact_score_status": "blocked_by_missing_unit_map",
            "best_private_read": "599 chose the right low-scrutiny route: derive projector/boundary ownership before scoring. P_loc can be made vertical-blind as a contract, and representative-X boundary charge can be proper-zero, but observed q_loc/source-measure flux is still open. Compact-shell number remains a cage, not a pass.",
            "next_target": NEXT_TARGET,
        }
    ]


def make_validation(
    sources: list[dict[str, str]],
    projector_rows: list[dict[str, str]],
    boundary_rows: list[dict[str, str]],
    compact_rows: list[dict[str, str]],
    fork_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    prior_rows = read_csv(PRIOR_598_VALIDATION)
    prior_failures = [row for row in prior_rows if row.get("result", "").strip().lower() != "pass"]
    missing_sources = [row for row in sources if row["exists"] != "True"]
    claim_rows = [
        *[row for row in projector_rows if row["valid_for_claim"] == "true"],
        *[row for row in boundary_rows if row["valid_for_claim"] == "true"],
        *[row for row in compact_rows if row["valid_for_claim"] == "true"],
        *[row for row in fork_rows if row["valid_for_claim"] == "true"],
    ]
    projector_contract = any(row["projector_id"] == "PPO599_0_parent_definition" for row in projector_rows)
    no_hidden_force = any(row["projector_id"] == "PPO599_1_no_hidden_force" for row in projector_rows)
    boundary_open = any(row["boundary_id"] == "BNF599_3_source_measure_flux" and row["derivation_result"] == "still_open" for row in boundary_rows)
    compact_blocked = any(row["score_id"] == "CSS599_4_score_verdict" and row["score_status"] == "score_deferred" for row in compact_rows)
    unit_map_missing = any(row["score_id"] == "CSS599_1_unit_map" and row["score_status"] == "blocked" for row in compact_rows)
    fork_has_projector_boundary = all(
        any(row["fork_id"] == fork_id for row in fork_rows)
        for fork_id in ["F599_A_projector_derivation", "F599_B_boundary_primitive"]
    )
    return [
        {
            "check_id": "V599_0_source_paths_exist",
            "result": "pass" if not missing_sources else "fail",
            "detail": f"missing={len(missing_sources)}",
        },
        {
            "check_id": "V599_1_prior_598_clean",
            "result": "pass" if prior_rows and not prior_failures else "fail",
            "detail": f"prior_rows={len(prior_rows)};prior_failures={len(prior_failures)}",
        },
        {
            "check_id": "V599_2_projector_contract_present",
            "result": "pass" if projector_contract and no_hidden_force else "fail",
            "detail": f"projector_rows={len(projector_rows)}",
        },
        {
            "check_id": "V599_3_boundary_flux_retained",
            "result": "pass" if boundary_open else "fail",
            "detail": "observed source-measure boundary flux remains open",
        },
        {
            "check_id": "V599_4_compact_score_not_overclaimed",
            "result": "pass" if compact_blocked and unit_map_missing else "fail",
            "detail": "compact-shell score deferred until unit/projection map exists",
        },
        {
            "check_id": "V599_5_next_fork_present",
            "result": "pass" if fork_has_projector_boundary else "fail",
            "detail": f"fork_rows={len(fork_rows)}",
        },
        {
            "check_id": "V599_6_no_claim_rows",
            "result": "pass" if not claim_rows else "fail",
            "detail": f"claim_rows={len(claim_rows)}",
        },
        {
            "check_id": "V599_7_no_R10_or_local_GR_claim",
            "result": "pass",
            "detail": "claim_allowed=false;R10_pass=false;WEP=false;PPN=false;local_GR=false",
        },
    ]


def write_markdown(
    generated: str,
    run_root: Path,
    sources: list[dict[str, str]],
    projector_rows: list[dict[str, str]],
    boundary_rows: list[dict[str, str]],
    compact_rows: list[dict[str, str]],
    fork_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    route_update_rows: list[dict[str, str]],
    validation_rows: list[dict[str, str]],
) -> None:
    text = f"""# 599 Y5 R10 parent projector boundary zero or compact shell score

Generated: {generated}  
Status: `{STATUS}`  
Claim ceiling: `{CLAIM_CEILING}`  
Next target: `{NEXT_TARGET}`  
Run root: `{rel(run_root)}`

## Verdict
- Best route remains derivation before scoring.
- `P_loc` can be written as a parent-owned `Q_obs` projector contract, and this preserves the direct representative-`X` zero row.
- But `P_loc` ownership is not derived for current MTS, and it cannot be used to hide observed residual force components.
- Boundary no-flux also remains open: proper representative-`X` boundary zero is not the same as observed source-measure/q_loc boundary silence.
- Compact-shell score is deferred. The `7.432631961576971e-06` number is an internal pressure cage, not a physical PPN/R10/local-bound pass.

## Source Register
{markdown_table(sources, ["source_file", "exists", "role"])}

## Parent Projector Ownership Attempt
{markdown_table(projector_rows, ["projector_id", "object", "candidate_definition", "required_test", "derivation_result", "blocker", "valid_for_claim"])}

## Boundary No-Flux Attempt
{markdown_table(boundary_rows, ["boundary_id", "condition", "would_zero", "derivation_result", "blocker", "valid_for_claim"])}

## Compact Shell Score Status
{markdown_table(compact_rows, ["score_id", "quantity", "input_value", "source", "score_status", "why_not_claim", "valid_for_claim"])}

## Derive Or Score Fork
{markdown_table(fork_rows, ["fork_id", "condition", "result_if_success", "status", "next_action", "valid_for_claim"])}

## Decision
{markdown_table(decision_rows, ["decision_id", "decision", "meaning", "claim_status", "next_target"])}

## Route Update
{markdown_table(route_update_rows, ["route_id", "allowed_after_599", "forbidden_after_599", "next_action"])}

## Validation
{markdown_table(validation_rows, ["check_id", "result", "detail"])}

## Practical Read
This is boring in the good way. We are not letting a projection symbol or a small proxy number win the round for us. `P_loc` has to be parent-owned, boundary flux has to be killed or scored, and the compact-shell cage needs a real unit map before it can punch in public.
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def main() -> int:
    generated = datetime.now(timezone.utc).isoformat()
    run_root = RUNS / f"{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}-{SLUG}"
    run_root.mkdir(parents=True, exist_ok=True)

    sources = make_sources()
    projector_rows = make_projector_rows()
    boundary_rows = make_boundary_rows()
    compact_rows = make_compact_score_rows()
    fork_rows = make_fork_rows()
    decision_rows = make_decision_rows()
    route_update_rows = make_route_update_rows()
    summary_rows = make_summary_rows()
    validation_rows = make_validation(sources, projector_rows, boundary_rows, compact_rows, fork_rows)

    write_csv(SOURCE_REGISTER_PATH, sources, ["source_file", "exists", "role"])
    write_csv(PROJECTOR_PATH, projector_rows, ["projector_id", "object", "candidate_definition", "required_test", "derivation_result", "blocker", "valid_for_claim"])
    write_csv(BOUNDARY_PATH, boundary_rows, ["boundary_id", "condition", "would_zero", "derivation_result", "blocker", "valid_for_claim"])
    write_csv(COMPACT_SCORE_PATH, compact_rows, ["score_id", "quantity", "input_value", "source", "score_status", "why_not_claim", "valid_for_claim"])
    write_csv(FORK_PATH, fork_rows, ["fork_id", "condition", "result_if_success", "status", "next_action", "valid_for_claim"])
    write_csv(DECISION_PATH, decision_rows, ["decision_id", "decision", "meaning", "claim_status", "next_target"])
    write_csv(ROUTE_UPDATE_PATH, route_update_rows, ["route_id", "allowed_after_599", "forbidden_after_599", "next_action"])
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
            "projector_status",
            "boundary_status",
            "compact_score_status",
            "best_private_read",
            "next_target",
        ],
    )
    write_csv(VALIDATION_PATH, validation_rows, ["check_id", "result", "detail"])

    write_markdown(
        generated,
        run_root,
        sources,
        projector_rows,
        boundary_rows,
        compact_rows,
        fork_rows,
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
