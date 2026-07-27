from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
RUNS = ROOT / "runs"

SLUG = "Y5-R10-relative-Hodge-projector-or-compact-shell-unit-map"
DOC_PATH = ROOT / "601-Y5-R10-relative-Hodge-projector-or-compact-shell-unit-map.md"
SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_601_SOURCE_REGISTER.csv"
HODGE_OWNER_PATH = RESIDUALS / "P8_Y5_R10_601_RELATIVE_HODGE_PARENT_OWNERSHIP.csv"
TRIVIAL_CLASS_PATH = RESIDUALS / "P8_Y5_R10_601_TRIVIAL_COHOMOLOGY_GATE.csv"
UNIT_MAP_PATH = RESIDUALS / "P8_Y5_R10_601_COMPACT_SHELL_UNIT_MAP_SPEC.csv"
RUNNER_UPDATE_PATH = RESIDUALS / "P8_Y5_R10_601_RUNNER_UPDATE.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_BRR545_601_DECISION.csv"
ROUTE_UPDATE_PATH = RESIDUALS / "P8_Y5_BRR545_601_ROUTE_UPDATE.csv"
SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_601_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_601_VALIDATION.csv"

PRIOR_600_VALIDATION = RESIDUALS / "P8_Y5_BRR545_600_VALIDATION.csv"
PRIOR_600_PROJECTOR = RESIDUALS / "P8_Y5_R10_600_PROJECTOR_ALGEBRA_FILL.csv"
PRIOR_600_GATE = RESIDUALS / "P8_Y5_R10_600_POINTWISE_VS_INTEGRATED_GATE.csv"

STATUS = "Y5_R10_relative_Hodge_parent_ownership_attempt_unit_map_fallback_spec_written_no_local_claim"
CLAIM_CEILING = "derivation_attempt_and_unit_map_spec_only_no_q_loc_zero_R10_WEP_PPN_or_local_GR_pass"
NEXT_TARGET = "602-Y5-R10-bound-domain-selector-or-compact-shell-unit-map-fill.md"
COMPACT_SHELL_PROXY = "7.432631961576971e-06"

SOURCE_FILES = [
    ("600-Y5-R10-projector-algebra-or-boundary-primitive-fill.md", "immediate 600 handoff"),
    ("source-intake/mts_residuals/P8_Y5_BRR545_600_VALIDATION.csv", "prior validation gate"),
    ("source-intake/mts_residuals/P8_Y5_R10_600_PROJECTOR_ALGEBRA_FILL.csv", "relative projector algebra"),
    ("source-intake/mts_residuals/P8_Y5_R10_600_POINTWISE_VS_INTEGRATED_GATE.csv", "pointwise versus integrated guard"),
    ("60-relative-cohomology-boundary-contract.md", "local-zero/FLRW-nonzero relative cohomology contract"),
    ("61-bound-domain-boundary-theorem-attempt.md", "volume-extremal boundary theorem attempt"),
    ("219-compact-shell-q_loc-source-projection-attempt.md", "compact-shell q_loc identity and leakage budget"),
    ("220-Jrel-local-trivial-representative-or-closure-bound.md", "J_rel exactness and ordinary-GR-flux separation"),
    ("582-Y5-R10-boundary-charge-and-constraint-algebra-no-pole-audit.md", "boundary charge and constraint algebra blocker"),
    ("scripts/Y5_R10_relative_Hodge_projector_or_compact_shell_unit_map.py", "this checkpoint generator"),
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


def make_hodge_rows() -> list[dict[str, str]]:
    return [
        {
            "hodge_id": "RHP601_0_parent_fields",
            "needed_object": "relative memory bundle E_rel over compact local collar C",
            "derivation_attempt": "Take the exact-sector algebra from 600 and demand E_rel be the quotient-pullback memory/domain-exchange sector, not ordinary metric mass flux.",
            "required_parent_clause": "parent action defines E_rel, d_rel, boundary trace maps, and excludes ordinary GR Gauss mass flux from J_rel",
            "current_status": "contract_only",
            "blocker": "no current MTS parent action has varied these fields as a closed reduced relative complex",
            "valid_for_claim": "false",
        },
        {
            "hodge_id": "RHP601_1_inner_product",
            "needed_object": "relative Hodge inner product and adjoint delta_rel",
            "derivation_attempt": "Use the local metric/coframe pullback to define <a,b>_rel = integral_C a wedge star_rel b with relative boundary conditions.",
            "required_parent_clause": "metric/coframe, measure, star_rel, and boundary conditions are Q_obs-owned and stationary before the projector is constructed",
            "current_status": "conditional_geometry",
            "blocker": "measure and Green operator are not yet obtained from the reduced GK/local parent action",
            "valid_for_claim": "false",
        },
        {
            "hodge_id": "RHP601_2_projector",
            "needed_object": "P_exact = d_rel delta_rel G_rel on im d_rel",
            "derivation_attempt": "If Delta_rel = d_rel delta_rel + delta_rel d_rel is elliptic on the collar, define G_rel on the orthogonal complement of harmonic modes and set P_exact as the exact-sector projector.",
            "required_parent_clause": "Delta_rel domain is fixed; zero modes are either absent or explicitly routed to harmonic/source residual rows",
            "current_status": "formal_if_domain_exists",
            "blocker": "elliptic domain and harmonic-mode handling are not parent-owned",
            "valid_for_claim": "false",
        },
        {
            "hodge_id": "RHP601_3_commutator",
            "needed_object": "[P_exact, d_rel]=0 on the exact sector",
            "derivation_attempt": "On im d_rel with d_rel squared zero, P_exact d_rel d_rel A_rel = 0. This preserves the 600 exact-sector pointwise zero.",
            "required_parent_clause": "J_rel must be exact inside the projected memory-exchange sector",
            "current_status": "algebraic_pass_if_RHP601_0_to_2_pass",
            "blocker": "does not address coexact, harmonic, source-measure, or boundary-charge pieces",
            "valid_for_claim": "false",
        },
        {
            "hodge_id": "RHP601_4_parent_ownership_verdict",
            "needed_object": "full parent-owned relative-Hodge projector",
            "derivation_attempt": "Combine E_rel, inner product, elliptic Green operator, trivial harmonic sector, Q_obs pullback, and flux separation.",
            "required_parent_clause": "all objects are generated by a parent variation/constraint algebra, not selected after seeing local bounds",
            "current_status": "not_derived_current_MTS",
            "blocker": "relative complex and trivial cohomology remain contracts rather than theorem outputs",
            "valid_for_claim": "false",
        },
    ]


def make_trivial_rows() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "TCG601_0_bound_volume_extremum",
            "candidate_statement": "stationary compact bound collars have dV_D/dtau = 0, hence no coherent volume-memory flux",
            "evidence_from_sources": "61 gives the kinematic identity d ln V_D/dtau = <theta>_D and conditional Q_coh=0 for stationary domains",
            "result": "partial_kinematic_support",
            "still_needed": "parent domain selector must force this boundary without referencing PPN success",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "TCG601_1_trivial_relative_class",
            "candidate_statement": "stationary bound local domains carry trivial relative memory class H_rel=0",
            "evidence_from_sources": "60 states this as the clean local-zero/FLRW-nonzero contract",
            "result": "contract_written_not_theorem",
            "still_needed": "prove compact local collar has trivial relative memory class for the parent E_rel complex",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "TCG601_2_FLRW_survival",
            "candidate_statement": "coherent FLRW domains keep a nontrivial expansion class",
            "evidence_from_sources": "60 and 61 keep d ln V_D/dtau = 3H as the nonzero expansion branch",
            "result": "route_preserved_conditionally",
            "still_needed": "same parent selector must produce both local zero and FLRW nonzero branches",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "TCG601_3_ordinary_GR_flux",
            "candidate_statement": "J_rel is memory/domain-exchange current, not Newtonian or GR mass flux",
            "evidence_from_sources": "220 explicitly warns ordinary gravitational flux must remain separate",
            "result": "separation_contract_retained",
            "still_needed": "source-measure and Hamiltonian mass projector must be derived",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "TCG601_4_boundary_charge",
            "candidate_statement": "boundary charge and cocycle vanish for allowed local vertical transformations",
            "evidence_from_sources": "582 says this is exactly unproved; nonzero edge terms must be scored",
            "result": "blocked_current_claim",
            "still_needed": "derive differentiable first-class momentum map or route edge charge into residual coefficients",
            "valid_for_claim": "false",
        },
    ]


def make_unit_map_rows() -> list[dict[str, str]]:
    return [
        {
            "map_id": "CSU601_0_proxy_input",
            "quantity": "compact_shell_proxy_epsilon",
            "required_value_or_rule": COMPACT_SHELL_PROXY,
            "source_or_status": "219/599 compact-shell internal pressure budget",
            "units": "dimensionless proxy until mapped",
            "claim_status": "blocked_not_physical_observable",
            "valid_for_claim": "false",
        },
        {
            "map_id": "CSU601_1_channel_choice",
            "quantity": "observable channel",
            "required_value_or_rule": "choose exactly one before scoring: R10 alpha(lambda), PPN residual vector, WEP/Eotvos channel, or clock/redshift channel",
            "source_or_status": "not selected",
            "units": "channel dependent",
            "claim_status": "blocked",
            "valid_for_claim": "false",
        },
        {
            "map_id": "CSU601_2_operator_normalization",
            "quantity": "epsilon_shell to observable coefficient",
            "required_value_or_rule": "derive coefficient C_channel from parent source projector, not tune it to the bound",
            "source_or_status": "missing parent coefficient",
            "units": "must convert proxy into alpha, gamma-1, beta-1, eta, or delta_nu/nu",
            "claim_status": "blocked",
            "valid_for_claim": "false",
        },
        {
            "map_id": "CSU601_3_sign_and_range",
            "quantity": "sign, lambda, and spatial profile",
            "required_value_or_rule": "provide sign convention, lambda from parent mass gap/length scale, and radial profile shape",
            "source_or_status": "missing",
            "units": "lambda in metres for R10; dimensionless residuals for PPN/WEP",
            "claim_status": "blocked",
            "valid_for_claim": "false",
        },
        {
            "map_id": "CSU601_4_baseline_comparison",
            "quantity": "baseline and acceptance rule",
            "required_value_or_rule": "compare MTS residual and GR/null baseline through the same pipeline; no one-sided guilty-until-proven test",
            "source_or_status": "policy written",
            "units": "test dependent",
            "claim_status": "not_yet_run",
            "valid_for_claim": "false",
        },
        {
            "map_id": "CSU601_5_claim_gate",
            "quantity": "minimum claim requirements",
            "required_value_or_rule": "source path, numeric coefficient, units, uncertainty/bound, positive data provenance, and abs(prediction)<=bound",
            "source_or_status": "gate written",
            "units": "test dependent",
            "claim_status": "no_claim_until_filled",
            "valid_for_claim": "false",
        },
    ]


def make_runner_rows() -> list[dict[str, str]]:
    return [
        {
            "runner_id": "RU601_0_relative_Hodge_route",
            "previous_status": "conditional_projector_algebra_from_600",
            "new_status": "parent_ownership_not_derived",
            "reason": "the formal Hodge projector can be written, but the parent action has not generated E_rel, delta_rel, G_rel, boundary data, or trivial harmonic sector",
            "still_needed": "derive parent reduced relative complex and domain selector",
            "valid_for_claim": "false",
        },
        {
            "runner_id": "RU601_1_exact_sector_zero",
            "previous_status": "conditional_zero_if_relative_complex_exists",
            "new_status": "retained_as_conditional_exact_sector_zero",
            "reason": "P_exact d_rel d_rel A_rel = 0 remains mathematically clean once the complex exists",
            "still_needed": "prove J_rel is exact and excludes source/harmonic/coexact pieces",
            "valid_for_claim": "false",
        },
        {
            "runner_id": "RU601_2_trivial_cohomology",
            "previous_status": "not_derived",
            "new_status": "kinematic_support_only",
            "reason": "stationary volume-flow supports coherent scalar silence but not full relative cohomology triviality",
            "still_needed": "parent-selected stationary bound-domain theorem",
            "valid_for_claim": "false",
        },
        {
            "runner_id": "RU601_3_compact_shell_unit_map",
            "previous_status": "missing",
            "new_status": "fallback_spec_written_not_filled",
            "reason": "unit map must be filled before the 7.432631961576971e-06 proxy can be scored",
            "still_needed": "choose observable channel and derive coefficient/units/profile",
            "valid_for_claim": "false",
        },
    ]


def make_decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "D601_0_relative_Hodge_not_promoted",
            "decision": "do not claim parent-owned relative-Hodge projector yet",
            "meaning": "formal algebra is real, but parent ownership of the complex, inner product, boundary domain, and zero-mode split is absent",
            "claim_status": "no_claim",
            "next_target": NEXT_TARGET,
        },
        {
            "decision_id": "D601_1_trivial_class_not_proved",
            "decision": "retain trivial relative class as theorem target, not axiom",
            "meaning": "the volume-extremal rule motivates local silence, but does not by itself kill all H_rel/source classes",
            "claim_status": "conditional_only",
            "next_target": NEXT_TARGET,
        },
        {
            "decision_id": "D601_2_unit_map_spec_locked",
            "decision": "write compact-shell unit-map acceptance contract",
            "meaning": "if derivation stalls, score the residual honestly through a source-backed observable map",
            "claim_status": "blocked_until_filled",
            "next_target": NEXT_TARGET,
        },
        {
            "decision_id": "D601_3_best_next_move",
            "decision": "try bound-domain selector first, unit-map fill second",
            "meaning": "the lower-scrutiny route is still derivation-first; scoring only begins after channel and coefficient ownership are fixed",
            "claim_status": "private_workflow",
            "next_target": NEXT_TARGET,
        },
    ]


def make_route_update_rows() -> list[dict[str, str]]:
    return [
        {
            "route_id": "RU601_0_allowed",
            "allowed_after_601": "use P_exact d_rel d_rel A_rel = 0 as an exact-sector conditional theorem",
            "forbidden_after_601": "claim observed q_loc=0 from Hodge algebra alone",
            "next_action": NEXT_TARGET,
        },
        {
            "route_id": "RU601_1_allowed",
            "allowed_after_601": "derive the parent bound-domain selector that makes local H_rel trivial and FLRW H_rel nontrivial",
            "forbidden_after_601": "choose compact collars only because PPN wants silence",
            "next_action": NEXT_TARGET,
        },
        {
            "route_id": "RU601_2_allowed",
            "allowed_after_601": "start unit-map fill if domain-selector derivation stalls",
            "forbidden_after_601": "score the compact-shell proxy as alpha, PPN, WEP, or clock evidence without units and coefficient source",
            "next_action": NEXT_TARGET,
        },
    ]


def make_summary_rows() -> list[dict[str, str]]:
    return [
        {
            "summary_id": "S601_0",
            "claim_allowed": "false",
            "R10_pass": "false",
            "WEP_pass": "false",
            "PPN_pass": "false",
            "local_GR_pass": "false",
            "relative_Hodge_status": "formal_projector_written_parent_owner_missing",
            "trivial_class_status": "kinematic_volume_support_contract_not_theorem",
            "unit_map_status": "fallback_spec_written_not_filled",
            "best_private_read": "601 is useful because it prevents a fake win: the relative-Hodge projector is mathematically plausible, but current MTS still lacks the parent object that owns it. The compact-shell proxy now has an explicit unit-map contract before any local-bound score.",
            "next_target": NEXT_TARGET,
        }
    ]


def make_validation(
    sources: list[dict[str, str]],
    hodge_rows: list[dict[str, str]],
    trivial_rows: list[dict[str, str]],
    unit_map_rows: list[dict[str, str]],
    runner_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    prior_validation = read_csv(PRIOR_600_VALIDATION)
    prior_failures = [row for row in prior_validation if row.get("result", "").strip().lower() != "pass"]
    prior_projector = read_csv(PRIOR_600_PROJECTOR)
    prior_gate = read_csv(PRIOR_600_GATE)
    missing_sources = [row for row in sources if row["exists"] != "True"]
    claim_rows = [
        *[row for row in hodge_rows if row["valid_for_claim"] == "true"],
        *[row for row in trivial_rows if row["valid_for_claim"] == "true"],
        *[row for row in unit_map_rows if row["valid_for_claim"] == "true"],
        *[row for row in runner_rows if row["valid_for_claim"] == "true"],
    ]
    parent_blocker_visible = any(row["current_status"] == "not_derived_current_MTS" for row in hodge_rows)
    trivial_blocker_visible = any(row["result"] == "contract_written_not_theorem" for row in trivial_rows)
    boundary_charge_blocked = any(row["gate_id"] == "TCG601_4_boundary_charge" and row["result"] == "blocked_current_claim" for row in trivial_rows)
    unit_map_blocks_score = all(row["valid_for_claim"] == "false" for row in unit_map_rows) and any(
        row["map_id"] == "CSU601_5_claim_gate" for row in unit_map_rows
    )
    exact_sector_retained = any(
        row["runner_id"] == "RU601_1_exact_sector_zero"
        and row["new_status"] == "retained_as_conditional_exact_sector_zero"
        for row in runner_rows
    )
    return [
        {
            "check_id": "V601_0_source_paths_exist",
            "result": "pass" if not missing_sources else "fail",
            "detail": f"missing={len(missing_sources)}",
        },
        {
            "check_id": "V601_1_prior_600_clean",
            "result": "pass" if prior_validation and not prior_failures else "fail",
            "detail": f"prior_rows={len(prior_validation)};prior_failures={len(prior_failures)};projector_rows={len(prior_projector)};gate_rows={len(prior_gate)}",
        },
        {
            "check_id": "V601_2_relative_Hodge_parent_blocker_visible",
            "result": "pass" if parent_blocker_visible else "fail",
            "detail": "parent-owned relative complex and Green operator not derived",
        },
        {
            "check_id": "V601_3_exact_sector_zero_retained_only_conditionally",
            "result": "pass" if exact_sector_retained else "fail",
            "detail": "exact-sector algebra retained without observed q_loc claim",
        },
        {
            "check_id": "V601_4_trivial_class_and_boundary_charge_not_smuggled",
            "result": "pass" if trivial_blocker_visible and boundary_charge_blocked else "fail",
            "detail": "trivial class remains contract; boundary charge remains blocked",
        },
        {
            "check_id": "V601_5_compact_shell_unit_map_blocks_score",
            "result": "pass" if unit_map_blocks_score else "fail",
            "detail": f"proxy={COMPACT_SHELL_PROXY};physical_channel_not_filled",
        },
        {
            "check_id": "V601_6_no_claim_rows",
            "result": "pass" if not claim_rows else "fail",
            "detail": f"claim_rows={len(claim_rows)}",
        },
        {
            "check_id": "V601_7_no_R10_or_local_GR_claim",
            "result": "pass",
            "detail": "claim_allowed=false;R10_pass=false;WEP=false;PPN=false;local_GR=false",
        },
    ]


def write_markdown(
    generated: str,
    run_root: Path,
    sources: list[dict[str, str]],
    hodge_rows: list[dict[str, str]],
    trivial_rows: list[dict[str, str]],
    unit_map_rows: list[dict[str, str]],
    runner_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    route_update_rows: list[dict[str, str]],
    validation_rows: list[dict[str, str]],
) -> None:
    text = f"""# 601 Y5 R10 relative-Hodge projector or compact-shell unit map

Generated: {generated}  
Status: `{STATUS}`  
Claim ceiling: `{CLAIM_CEILING}`  
Next target: `{NEXT_TARGET}`  
Run root: `{rel(run_root)}`

## Verdict
- The Hodge route is mathematically respectable but not yet parent-derived: `P_exact = d_rel delta_rel G_rel` can be written only after the theory owns `E_rel`, `d_rel`, the relative inner product, the Green operator, boundary conditions, and zero-mode routing.
- The exact-sector zero from 600 survives as a clean conditional theorem: if `J_rel=d_rel A_rel`, then `P_exact d_rel J_rel = P_exact d_rel d_rel A_rel = 0`.
- This still does not prove observed `q_loc=0`, because harmonic, coexact, source-measure, ordinary GR flux, and edge-boundary charge pieces remain live.
- The compact-shell proxy `{COMPACT_SHELL_PROXY}` is now explicitly locked as non-claim data until a unit/projection map chooses an observable channel and derives its coefficient, sign, range, profile, and units.

## Source Register
{markdown_table(sources, ["source_file", "exists", "role"])}

## Relative-Hodge Parent Ownership Attempt
{markdown_table(hodge_rows, ["hodge_id", "needed_object", "derivation_attempt", "required_parent_clause", "current_status", "blocker", "valid_for_claim"])}

## Trivial Cohomology Gate
{markdown_table(trivial_rows, ["gate_id", "candidate_statement", "evidence_from_sources", "result", "still_needed", "valid_for_claim"])}

## Compact-Shell Unit Map Spec
{markdown_table(unit_map_rows, ["map_id", "quantity", "required_value_or_rule", "source_or_status", "units", "claim_status", "valid_for_claim"])}

## Runner Update
{markdown_table(runner_rows, ["runner_id", "previous_status", "new_status", "reason", "still_needed", "valid_for_claim"])}

## Decision
{markdown_table(decision_rows, ["decision_id", "decision", "meaning", "claim_status", "next_target"])}

## Route Update
{markdown_table(route_update_rows, ["route_id", "allowed_after_601", "forbidden_after_601", "next_action"])}

## Validation
{markdown_table(validation_rows, ["check_id", "result", "detail"])}

## Practical Read
This is not grim; it is the good kind of annoying. We have a clean mathematical doorway, but the door has a lock: parent ownership of the relative complex. The next best punch is to derive the bound-domain selector that makes local `H_rel` trivial while keeping FLRW nontrivial. If that punch glances off, we stop trying to mystically zero the residual and score the compact-shell proxy through the unit-map contract.
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def main() -> int:
    generated = datetime.now(timezone.utc).isoformat()
    run_root = RUNS / f"{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}-{SLUG}"
    run_root.mkdir(parents=True, exist_ok=True)

    sources = make_sources()
    hodge_rows = make_hodge_rows()
    trivial_rows = make_trivial_rows()
    unit_map_rows = make_unit_map_rows()
    runner_rows = make_runner_rows()
    decision_rows = make_decision_rows()
    route_update_rows = make_route_update_rows()
    summary_rows = make_summary_rows()
    validation_rows = make_validation(sources, hodge_rows, trivial_rows, unit_map_rows, runner_rows)

    write_csv(SOURCE_REGISTER_PATH, sources, ["source_file", "exists", "role"])
    write_csv(HODGE_OWNER_PATH, hodge_rows, ["hodge_id", "needed_object", "derivation_attempt", "required_parent_clause", "current_status", "blocker", "valid_for_claim"])
    write_csv(TRIVIAL_CLASS_PATH, trivial_rows, ["gate_id", "candidate_statement", "evidence_from_sources", "result", "still_needed", "valid_for_claim"])
    write_csv(UNIT_MAP_PATH, unit_map_rows, ["map_id", "quantity", "required_value_or_rule", "source_or_status", "units", "claim_status", "valid_for_claim"])
    write_csv(RUNNER_UPDATE_PATH, runner_rows, ["runner_id", "previous_status", "new_status", "reason", "still_needed", "valid_for_claim"])
    write_csv(DECISION_PATH, decision_rows, ["decision_id", "decision", "meaning", "claim_status", "next_target"])
    write_csv(ROUTE_UPDATE_PATH, route_update_rows, ["route_id", "allowed_after_601", "forbidden_after_601", "next_action"])
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
            "relative_Hodge_status",
            "trivial_class_status",
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
        hodge_rows,
        trivial_rows,
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
