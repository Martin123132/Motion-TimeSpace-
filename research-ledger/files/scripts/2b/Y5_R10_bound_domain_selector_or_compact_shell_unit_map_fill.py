from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
RUNS = ROOT / "runs"

SLUG = "Y5-R10-bound-domain-selector-or-compact-shell-unit-map-fill"
DOC_PATH = ROOT / "602-Y5-R10-bound-domain-selector-or-compact-shell-unit-map-fill.md"
SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_602_SOURCE_REGISTER.csv"
SELECTOR_ATTEMPT_PATH = RESIDUALS / "P8_Y5_R10_602_BOUND_DOMAIN_SELECTOR_DERIVATION_ATTEMPT.csv"
BRANCH_GATE_PATH = RESIDUALS / "P8_Y5_R10_602_LOCAL_FLRW_BRANCH_GATE.csv"
UNIT_MAP_FORK_PATH = RESIDUALS / "P8_Y5_R10_602_UNIT_MAP_FORK_STATUS.csv"
RUNNER_UPDATE_PATH = RESIDUALS / "P8_Y5_R10_602_RUNNER_UPDATE.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_BRR545_602_DECISION.csv"
ROUTE_UPDATE_PATH = RESIDUALS / "P8_Y5_BRR545_602_ROUTE_UPDATE.csv"
SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_602_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_602_VALIDATION.csv"

PRIOR_601_VALIDATION = RESIDUALS / "P8_Y5_BRR545_601_VALIDATION.csv"
PRIOR_601_HODGE = RESIDUALS / "P8_Y5_R10_601_RELATIVE_HODGE_PARENT_OWNERSHIP.csv"
PRIOR_601_UNIT_MAP = RESIDUALS / "P8_Y5_R10_601_COMPACT_SHELL_UNIT_MAP_SPEC.csv"

STATUS = "Y5_R10_bound_domain_selector_conditional_variation_written_parent_primitive_missing_unit_map_still_unfilled"
CLAIM_CEILING = "conditional_selector_theorem_attempt_only_no_q_loc_zero_R10_WEP_PPN_or_local_GR_pass"
NEXT_TARGET = "603-Y5-R10-parent-primitive-for-ND-or-unit-map-channel-fill.md"
COMPACT_SHELL_PROXY = "7.432631961576971e-06"

SOURCE_FILES = [
    ("601-Y5-R10-relative-Hodge-projector-or-compact-shell-unit-map.md", "immediate 601 handoff"),
    ("source-intake/mts_residuals/P8_Y5_BRR545_601_VALIDATION.csv", "prior validation gate"),
    ("source-intake/mts_residuals/P8_Y5_R10_601_RELATIVE_HODGE_PARENT_OWNERSHIP.csv", "relative-Hodge parent ownership blocker"),
    ("source-intake/mts_residuals/P8_Y5_R10_601_COMPACT_SHELL_UNIT_MAP_SPEC.csv", "unit-map fallback contract"),
    ("60-relative-cohomology-boundary-contract.md", "local-zero/FLRW-nonzero relative class contract"),
    ("61-bound-domain-boundary-theorem-attempt.md", "volume-flow identity and stationary bound-domain partial theorem"),
    ("62-domain-field-chiD-action-contract.md", "chi_D selector action obligations"),
    ("63-chiD-variation-to-boundary-equation-attempt.md", "advection is not selection failure"),
    ("64-binding-invariant-domain-selector-attempt.md", "C_coh/C_exp kinematic separator"),
    ("67-auxiliary-selector-parent-contract.md", "no-independent-stress auxiliary selector route"),
    ("143-domain-selector-variational-action-attempt.md", "zero-knob action attempt and auxiliary C_coh route"),
    ("416-binding-invariant-domain-selector-repair.md", "C_exp repair and unresolved threshold/Bianchi gates"),
    ("475-domain-selector-parent-action-clause-or-coefficient-fill.md", "double-zero parent-action clause"),
    ("476-double-zero-memory-coupling-origin-or-coefficient-runner.md", "p>=2 local-silence requirement"),
    ("478-determinant-current-parent-ownership-or-demotion.md", "det(Q_coh) as best double-zero/current clue"),
    ("scripts/Y5_R10_bound_domain_selector_or_compact_shell_unit_map_fill.py", "this checkpoint generator"),
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


def make_selector_rows() -> list[dict[str, str]]:
    return [
        {
            "step_id": "BDS602_0_parent_selector_primitives",
            "object": "N_D and chi_D",
            "mathematical_form": "chi_D = N_D, with N_D a scalar/topological norm of the MTS projected boundary-memory class",
            "derivation_attempt": "Replace an empirical domain window with a parent scalar N_D built from b_D, c_D, C_exp, or det(Q_coh) only after projection by P_MTS,D.",
            "local_effect_if_true": "closed/gapped or exact local branch gives N_D=0 and chi_D=0",
            "FLRW_effect_if_true": "coherent expansion branch gives N_D>0 and chi_D>0",
            "current_status": "candidate_primitives_identified_not_parent_derived",
            "blocker": "N_D normalization, P_MTS,D ownership, and local zero class are still conditional",
            "valid_for_claim": "false",
        },
        {
            "step_id": "BDS602_1_candidate_action",
            "object": "selector action",
            "mathematical_form": "S_D = int sqrt(-g) lambda_D(chi_D-N_D) + int sqrt(-g) chi_D^p L_mem,D + S_top[P_MTS,D,J_B], p>=2",
            "derivation_attempt": "Use the 475/476 double-zero memory gate so local chi_D=0 also forces lambda_D=0 and removes hidden selector stress.",
            "local_effect_if_true": "bulk memory stress, selector force, and domain-vector leakage vanish at chi_D=0",
            "FLRW_effect_if_true": "memory sector can remain active where chi_D>0",
            "current_status": "conditional_sufficient_clause",
            "blocker": "the action clause is still stipulated as a sufficient construction, not derived from deeper MTS variables",
            "valid_for_claim": "false",
        },
        {
            "step_id": "BDS602_2_variation_lambda",
            "object": "lambda_D variation",
            "mathematical_form": "delta_lambda S_D = 0 -> chi_D - N_D = 0",
            "derivation_attempt": "The selector is no longer chosen after a fit; it is tied to a predeclared scalar/topological source.",
            "local_effect_if_true": "if parent proves N_local=0, the local branch is forced to chi_local=0",
            "FLRW_effect_if_true": "if parent proves N_FLRW>0, FLRW is not silenced",
            "current_status": "formal_variation_pass_if_ND_owned",
            "blocker": "N_D itself remains the unowned primitive",
            "valid_for_claim": "false",
        },
        {
            "step_id": "BDS602_3_variation_chi",
            "object": "chi_D variation",
            "mathematical_form": "delta_chi S_D = 0 -> lambda_D + p chi_D^(p-1)L_mem,D + chi_D^p partial_chi L_mem,D = 0",
            "derivation_attempt": "For p>=2 and chi_local=0, lambda_local=0 follows without tuning.",
            "local_effect_if_true": "constraint stress and memory stress vanish together in the local branch",
            "FLRW_effect_if_true": "lambda_D and memory stress may be nonzero in active coherent domains",
            "current_status": "formal_double_zero_pass",
            "blocker": "p>=2 is derived as a requirement, not as a parent-origin theorem",
            "valid_for_claim": "false",
        },
        {
            "step_id": "BDS602_4_boundary_embedding_variation",
            "object": "boundary level set or embedding",
            "mathematical_form": "delta_X S_top -> n_mu P_MTS,D J_B^mu = 0 for trivial/exact local class, or retained topological charge for nontrivial class",
            "derivation_attempt": "A positive projected boundary-current norm has natural no-flux boundary equations on the trivial class instead of hand-drawn local collars.",
            "local_effect_if_true": "stationary local compact shells get projected memory-boundary no-flux",
            "FLRW_effect_if_true": "nontrivial expansion class is not forced into the local no-flux representative",
            "current_status": "conditional_boundary_Euler_route",
            "blocker": "actual topological/boundary projector and variational domain labels are not parent-owned",
            "valid_for_claim": "false",
        },
        {
            "step_id": "BDS602_5_volume_flow_readout",
            "object": "coherent volume-memory channel",
            "mathematical_form": "d ln V_D/dtau = <theta>_D; local chi_D=0 projects Q_coh off, while FLRW chi_D>0 keeps d ln V_D/dtau=3H",
            "derivation_attempt": "Feed the 61 volume-flow identity through the auxiliary selector rather than declaring a plateau.",
            "local_effect_if_true": "local scalar volume-memory channel is silent in the selected bound domain",
            "FLRW_effect_if_true": "FLRW coherent expansion remains active",
            "current_status": "conditional_selector_theorem_if_BDS602_0_to_4_hold",
            "blocker": "does not prove observed q_loc=0 or kill harmonic/source/R11 rows",
            "valid_for_claim": "false",
        },
    ]


def make_branch_rows() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "LFG602_0_no_empirical_window",
            "requirement": "selector cannot use residuals, PPN success, SPARC fits, or cosmology fits",
            "current_result": "pass_contract",
            "reason": "N_D is restricted to parent scalar/topological/boundary-current ingredients",
            "blocking_issue": "ingredient ownership still missing",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "LFG602_1_local_zero",
            "requirement": "compact stationary local domains force N_D=0",
            "current_result": "not_parent_derived",
            "reason": "closed/gapped b_D=0 and exact/trivial c_D=0 remain conditional from 308/309/601",
            "blocking_issue": "local spectral gap or trivial relative class theorem",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "LFG602_2_FLRW_active",
            "requirement": "coherent FLRW domains force N_D>0 and retain expansion memory",
            "current_result": "conditional_support",
            "reason": "C_exp/det(Q_coh) give the right active shape, but Q_coh projection is not parent-owned",
            "blocking_issue": "parent-owned Q_coh/P_coh and normalization",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "LFG602_3_no_selector_stress",
            "requirement": "local branch has chi_D=lambda_D=0 and no bulk selector stress",
            "current_result": "formal_if_p_ge_2_and_Nlocal_zero",
            "reason": "double-zero memory gate kills the old linear-selector stress leak",
            "blocking_issue": "p>=2 origin and Nlocal=0 are not parent-derived together",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "LFG602_4_boundary_charge",
            "requirement": "boundary/topological charge either vanishes locally or is routed to residuals",
            "current_result": "not_derived_route_retained",
            "reason": "boundary Euler route is conditional and 582/601 keep edge charges alive",
            "blocking_issue": "momentum-map/edge-charge/nohair certificate",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "LFG602_5_R11_source_normalization",
            "requirement": "domain source-normalization operators are zero or executable",
            "current_result": "blocked",
            "reason": "475/476/478 keep R11 source-normalization as a separate blocker",
            "blocking_issue": "R11 zero-or-fill",
            "valid_for_claim": "false",
        },
    ]


def make_unit_map_rows() -> list[dict[str, str]]:
    return [
        {
            "fork_id": "UMF602_0_derivation_priority",
            "route": "continue selector derivation before scoring",
            "status": "preferred_next",
            "why": "BDS602 gives a sharper parent primitive target N_D; scoring before this would be closure-only",
            "required_next_input": "derive N_D from parent boundary/current variables or explicitly demote",
            "valid_for_claim": "false",
        },
        {
            "fork_id": "UMF602_1_unit_map_not_filled",
            "route": "compact-shell unit map",
            "status": "deferred_still_blocked",
            "why": f"proxy {COMPACT_SHELL_PROXY} still has no observable channel, coefficient, sign, range, or units",
            "required_next_input": "choose R10 alpha(lambda), PPN vector, WEP, or clock channel if N_D route stalls",
            "valid_for_claim": "false",
        },
        {
            "fork_id": "UMF602_2_no_score",
            "route": "local-bound evidence",
            "status": "no_claim",
            "why": "602 is a derivation attempt, not a data/score pass",
            "required_next_input": "source-backed coefficient rows or accepted theorem-zero gates",
            "valid_for_claim": "false",
        },
    ]


def make_runner_rows() -> list[dict[str, str]]:
    return [
        {
            "runner_id": "RU602_0_bound_domain_selector",
            "previous_status": "parent_selected_stationary_bound_domain_missing",
            "new_status": "conditional_selector_variation_written",
            "reason": "an auxiliary scalar/topological selector can force chi_local=0 if N_local=0 and p>=2",
            "still_needed": "parent derivation of N_D and local zero/FLRW active branch",
            "valid_for_claim": "false",
        },
        {
            "runner_id": "RU602_1_relative_Hodge_route",
            "previous_status": "parent_ownership_not_derived",
            "new_status": "blocked_on_ND_and_P_MTS_ownership",
            "reason": "relative-Hodge/projector ownership needs the same parent projector/domain machinery",
            "still_needed": "parent-owned P_MTS,D, relative complex, and boundary inner product",
            "valid_for_claim": "false",
        },
        {
            "runner_id": "RU602_2_q_loc_zero",
            "previous_status": "observed_q_loc_still_open",
            "new_status": "still_open",
            "reason": "selector theorem would silence coherent volume/domain leakage only under premises; harmonic/source/R11/boundary pieces remain",
            "still_needed": "q_loc exchange-owner terms zeroed or bounded row by row",
            "valid_for_claim": "false",
        },
        {
            "runner_id": "RU602_3_compact_shell_unit_map",
            "previous_status": "fallback_spec_written_not_filled",
            "new_status": "still_unfilled",
            "reason": "derivation route remains live enough to attack N_D first",
            "still_needed": "observable channel and coefficient if N_D cannot be parent-derived",
            "valid_for_claim": "false",
        },
    ]


def make_decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "D602_0_conditional_selector_theorem",
            "decision": "accept BDS602 as a conditional theorem skeleton",
            "meaning": "if N_D is parent-owned and local N_D=0 while FLRW N_D>0, the auxiliary p>=2 selector gives local scalar-domain silence without a plateau axiom",
            "claim_status": "conditional_not_promoted",
            "next_target": NEXT_TARGET,
        },
        {
            "decision_id": "D602_1_missing_key",
            "decision": "do not claim parent selector derivation",
            "meaning": "the real missing key is now N_D: a parent scalar/topological primitive that owns b_D/c_D/C_exp/det(Q_coh) and its normalization",
            "claim_status": "no_claim",
            "next_target": NEXT_TARGET,
        },
        {
            "decision_id": "D602_2_unit_map_deferred",
            "decision": "defer compact-shell unit-map fill one more step",
            "meaning": "the derivation path gained a sharper target, so scoring remains fallback rather than the next default",
            "claim_status": "blocked_until_filled",
            "next_target": NEXT_TARGET,
        },
        {
            "decision_id": "D602_3_no_local_GR",
            "decision": "forbid local-GR/PPN/R10 promotion",
            "meaning": "q_loc, R11, boundary charge, and source-normalization rows remain open",
            "claim_status": "forbidden",
            "next_target": NEXT_TARGET,
        },
    ]


def make_route_update_rows() -> list[dict[str, str]]:
    return [
        {
            "route_id": "RU602_0_allowed",
            "allowed_after_602": "try to derive N_D as a parent primitive from projected boundary current/coherent determinant data",
            "forbidden_after_602": "treat N_D as an empirical threshold or arena label",
            "next_action": NEXT_TARGET,
        },
        {
            "route_id": "RU602_1_allowed",
            "allowed_after_602": "use p>=2 auxiliary selector as a sufficient local-stress-silence clause",
            "forbidden_after_602": "claim the p>=2 clause has parent origin",
            "next_action": NEXT_TARGET,
        },
        {
            "route_id": "RU602_2_allowed",
            "allowed_after_602": "switch to unit-map scoring if N_D parent origin fails",
            "forbidden_after_602": "score compact-shell proxy without observable channel and unit conversion",
            "next_action": NEXT_TARGET,
        },
    ]


def make_summary_rows() -> list[dict[str, str]]:
    return [
        {
            "summary_id": "S602_0",
            "claim_allowed": "false",
            "R10_pass": "false",
            "WEP_pass": "false",
            "PPN_pass": "false",
            "local_GR_pass": "false",
            "selector_status": "conditional_selector_variation_written_ND_parent_primitive_missing",
            "Hodge_status": "still_blocked_on_parent_projector_and_relative_complex",
            "unit_map_status": "still_unfilled_deferred",
            "best_private_read": "602 improves the derivation route by replacing the vague domain selector with a concrete missing primitive N_D. If N_D is parent-owned, the p>=2 auxiliary selector gives real local scalar-domain silence. Current MTS still has not derived N_D, P_MTS,D, R11 silence, or full q_loc zero.",
            "next_target": NEXT_TARGET,
        }
    ]


def make_validation(
    sources: list[dict[str, str]],
    selector_rows: list[dict[str, str]],
    branch_rows: list[dict[str, str]],
    unit_map_rows: list[dict[str, str]],
    runner_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    prior_validation = read_csv(PRIOR_601_VALIDATION)
    prior_failures = [row for row in prior_validation if row.get("result", "").strip().lower() != "pass"]
    prior_hodge = read_csv(PRIOR_601_HODGE)
    prior_unit = read_csv(PRIOR_601_UNIT_MAP)
    missing_sources = [row for row in sources if row["exists"] != "True"]
    claim_rows = [
        *[row for row in selector_rows if row["valid_for_claim"] == "true"],
        *[row for row in branch_rows if row["valid_for_claim"] == "true"],
        *[row for row in unit_map_rows if row["valid_for_claim"] == "true"],
        *[row for row in runner_rows if row["valid_for_claim"] == "true"],
    ]
    selector_clause_written = any(row["step_id"] == "BDS602_1_candidate_action" for row in selector_rows)
    double_zero_visible = any(row["step_id"] == "BDS602_3_variation_chi" and "double_zero" in row["current_status"] for row in selector_rows)
    nd_blocker_visible = any("N_D" in row["blocker"] or row["step_id"] == "BDS602_0_parent_selector_primitives" for row in selector_rows)
    local_zero_not_claimed = any(row["gate_id"] == "LFG602_1_local_zero" and row["current_result"] == "not_parent_derived" for row in branch_rows)
    flrw_retained = any(row["gate_id"] == "LFG602_2_FLRW_active" and row["current_result"] == "conditional_support" for row in branch_rows)
    unit_map_unfilled = any(row["fork_id"] == "UMF602_1_unit_map_not_filled" and row["status"] == "deferred_still_blocked" for row in unit_map_rows)
    qloc_open = any(row["runner_id"] == "RU602_2_q_loc_zero" and row["new_status"] == "still_open" for row in runner_rows)
    return [
        {
            "check_id": "V602_0_source_paths_exist",
            "result": "pass" if not missing_sources else "fail",
            "detail": f"missing={len(missing_sources)}",
        },
        {
            "check_id": "V602_1_prior_601_clean",
            "result": "pass" if prior_validation and not prior_failures else "fail",
            "detail": f"prior_rows={len(prior_validation)};prior_failures={len(prior_failures)};hodge_rows={len(prior_hodge)};unit_rows={len(prior_unit)}",
        },
        {
            "check_id": "V602_2_selector_variation_written",
            "result": "pass" if selector_clause_written and double_zero_visible else "fail",
            "detail": f"selector_rows={len(selector_rows)};double_zero_visible={double_zero_visible}",
        },
        {
            "check_id": "V602_3_ND_parent_blocker_visible",
            "result": "pass" if nd_blocker_visible else "fail",
            "detail": "N_D primitive/normalization/projector ownership not parent-derived",
        },
        {
            "check_id": "V602_4_local_FLRW_split_not_smuggled",
            "result": "pass" if local_zero_not_claimed and flrw_retained else "fail",
            "detail": f"local_zero_not_claimed={local_zero_not_claimed};FLRW_retained={flrw_retained}",
        },
        {
            "check_id": "V602_5_q_loc_and_unit_map_still_open",
            "result": "pass" if qloc_open and unit_map_unfilled else "fail",
            "detail": f"q_loc_open={qloc_open};unit_map_unfilled={unit_map_unfilled};proxy={COMPACT_SHELL_PROXY}",
        },
        {
            "check_id": "V602_6_no_claim_rows",
            "result": "pass" if not claim_rows else "fail",
            "detail": f"claim_rows={len(claim_rows)}",
        },
        {
            "check_id": "V602_7_no_R10_or_local_GR_claim",
            "result": "pass",
            "detail": "claim_allowed=false;R10_pass=false;WEP=false;PPN=false;local_GR=false",
        },
    ]


def write_markdown(
    generated: str,
    run_root: Path,
    sources: list[dict[str, str]],
    selector_rows: list[dict[str, str]],
    branch_rows: list[dict[str, str]],
    unit_map_rows: list[dict[str, str]],
    runner_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    route_update_rows: list[dict[str, str]],
    validation_rows: list[dict[str, str]],
) -> None:
    text = f"""# 602 Y5 R10 bound-domain selector or compact-shell unit-map fill

Generated: {generated}  
Status: `{STATUS}`  
Claim ceiling: `{CLAIM_CEILING}`  
Next target: `{NEXT_TARGET}`  
Run root: `{rel(run_root)}`

## Verdict
- A real conditional selector theorem can be written: if a parent scalar/topological primitive `N_D` exists, then `chi_D=N_D` plus a `p>=2` memory gate makes local `N_D=0` branches silent without adding hidden selector stress.
- This is better than the old domain-window problem because the missing object is now exact: derive `N_D` from projected MTS boundary/current/coherent determinant data, or demote the route.
- The derivation is not complete. Current MTS has not parent-derived `N_D`, `P_MTS,D`, local trivial relative class, boundary charge silence, or R11 source-normalization silence.
- The compact-shell proxy `{COMPACT_SHELL_PROXY}` remains non-claim and unscored; unit-map fill is still the fallback, not the default.

## Selector Theorem Attempt
The candidate action is:

```text
S_D = integral sqrt(-g) lambda_D(chi_D - N_D)
    + integral sqrt(-g) chi_D^p L_mem,D
    + S_top[P_MTS,D,J_B],
with p >= 2.
```

The useful local consequence is:

```text
N_local = 0 -> chi_local = 0 -> lambda_local = 0 -> no bulk selector/memory stress.
```

The useful FLRW consequence is:

```text
N_FLRW > 0 -> chi_FLRW > 0 -> coherent expansion memory may remain active.
```

That is a proper theorem skeleton. It is not yet a parent theorem because `N_D` is not derived.

## Source Register
{markdown_table(sources, ["source_file", "exists", "role"])}

## Bound-Domain Selector Derivation Attempt
{markdown_table(selector_rows, ["step_id", "object", "mathematical_form", "derivation_attempt", "local_effect_if_true", "FLRW_effect_if_true", "current_status", "blocker", "valid_for_claim"])}

## Local-FLRW Branch Gate
{markdown_table(branch_rows, ["gate_id", "requirement", "current_result", "reason", "blocking_issue", "valid_for_claim"])}

## Unit-Map Fork Status
{markdown_table(unit_map_rows, ["fork_id", "route", "status", "why", "required_next_input", "valid_for_claim"])}

## Runner Update
{markdown_table(runner_rows, ["runner_id", "previous_status", "new_status", "reason", "still_needed", "valid_for_claim"])}

## Decision
{markdown_table(decision_rows, ["decision_id", "decision", "meaning", "claim_status", "next_target"])}

## Route Update
{markdown_table(route_update_rows, ["route_id", "allowed_after_602", "forbidden_after_602", "next_action"])}

## Validation
{markdown_table(validation_rows, ["check_id", "result", "detail"])}

## Practical Read
This is a decent move. Not checkmate, but definitely not flailing. The selector problem has been converted from "how do we choose the local box?" into "derive the scalar/topological primitive `N_D`." If `N_D` can be owned by the parent action, the local/FLRW split becomes a theorem-shaped thing rather than a hand switch. If it cannot, we stop punching the same wall and go to the unit-map scorer.
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def main() -> int:
    generated = datetime.now(timezone.utc).isoformat()
    run_root = RUNS / f"{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}-{SLUG}"
    run_root.mkdir(parents=True, exist_ok=True)

    sources = make_sources()
    selector_rows = make_selector_rows()
    branch_rows = make_branch_rows()
    unit_map_rows = make_unit_map_rows()
    runner_rows = make_runner_rows()
    decision_rows = make_decision_rows()
    route_update_rows = make_route_update_rows()
    summary_rows = make_summary_rows()
    validation_rows = make_validation(sources, selector_rows, branch_rows, unit_map_rows, runner_rows)

    write_csv(SOURCE_REGISTER_PATH, sources, ["source_file", "exists", "role"])
    write_csv(
        SELECTOR_ATTEMPT_PATH,
        selector_rows,
        ["step_id", "object", "mathematical_form", "derivation_attempt", "local_effect_if_true", "FLRW_effect_if_true", "current_status", "blocker", "valid_for_claim"],
    )
    write_csv(BRANCH_GATE_PATH, branch_rows, ["gate_id", "requirement", "current_result", "reason", "blocking_issue", "valid_for_claim"])
    write_csv(UNIT_MAP_FORK_PATH, unit_map_rows, ["fork_id", "route", "status", "why", "required_next_input", "valid_for_claim"])
    write_csv(RUNNER_UPDATE_PATH, runner_rows, ["runner_id", "previous_status", "new_status", "reason", "still_needed", "valid_for_claim"])
    write_csv(DECISION_PATH, decision_rows, ["decision_id", "decision", "meaning", "claim_status", "next_target"])
    write_csv(ROUTE_UPDATE_PATH, route_update_rows, ["route_id", "allowed_after_602", "forbidden_after_602", "next_action"])
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
            "selector_status",
            "Hodge_status",
            "unit_map_status",
            "best_private_read",
            "next_target",
        ],
    )
    write_csv(VALIDATION_PATH, validation_rows, ["check_id", "result", "detail"])

    write_markdown(
        generated,
        run_root,
        sources,
        selector_rows,
        branch_rows,
        unit_map_rows,
        runner_rows,
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
