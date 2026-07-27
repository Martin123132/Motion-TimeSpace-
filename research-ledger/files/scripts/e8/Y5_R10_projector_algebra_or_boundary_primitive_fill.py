from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
RUNS = ROOT / "runs"

SLUG = "Y5-R10-projector-algebra-or-boundary-primitive-fill"
DOC_PATH = ROOT / "600-Y5-R10-projector-algebra-or-boundary-primitive-fill.md"
SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_600_SOURCE_REGISTER.csv"
PROJECTOR_ALGEBRA_PATH = RESIDUALS / "P8_Y5_R10_600_PROJECTOR_ALGEBRA_FILL.csv"
BOUNDARY_PRIMITIVE_PATH = RESIDUALS / "P8_Y5_R10_600_BOUNDARY_PRIMITIVE_FILL.csv"
POINTWISE_GATE_PATH = RESIDUALS / "P8_Y5_R10_600_POINTWISE_VS_INTEGRATED_GATE.csv"
RUNNER_UPDATE_PATH = RESIDUALS / "P8_Y5_R10_600_RUNNER_UPDATE.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_BRR545_600_DECISION.csv"
ROUTE_UPDATE_PATH = RESIDUALS / "P8_Y5_BRR545_600_ROUTE_UPDATE.csv"
SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_600_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_600_VALIDATION.csv"

PRIOR_599_VALIDATION = RESIDUALS / "P8_Y5_BRR545_599_VALIDATION.csv"

STATUS = "Y5_R10_projector_algebra_conditional_fill_boundary_primitive_integrated_zero_pointwise_q_loc_still_open"
CLAIM_CEILING = "conditional_projector_boundary_fill_only_no_q_loc_zero_R10_WEP_PPN_or_local_GR_pass"
NEXT_TARGET = "601-Y5-R10-relative-Hodge-projector-or-compact-shell-unit-map.md"

SOURCE_FILES = [
    ("599-Y5-R10-parent-projector-boundary-zero-or-compact-shell-score.md", "immediate projector/boundary handoff"),
    ("source-intake/mts_residuals/P8_Y5_BRR545_599_VALIDATION.csv", "prior validation gate"),
    ("source-intake/mts_residuals/P8_Y5_R10_599_PARENT_PROJECTOR_OWNERSHIP_ATTEMPT.csv", "projector ownership contract"),
    ("source-intake/mts_residuals/P8_Y5_R10_599_BOUNDARY_NO_FLUX_ATTEMPT.csv", "boundary no-flux attempt"),
    ("source-intake/mts_residuals/P8_Y5_R10_599_COMPACT_SHELL_SCORE_STATUS.csv", "compact-shell score blocker"),
    ("219-compact-shell-q_loc-source-projection-attempt.md", "compact-shell q_loc identity and budget"),
    ("220-Jrel-local-trivial-representative-or-closure-bound.md", "J_rel exactness and integrated zero route"),
    ("581-Y5-R10-quotient-vertical-no-pole-parent-theorem-attempt.md", "no-pole boundary/certificate obligations"),
    ("582-Y5-R10-boundary-charge-and-constraint-algebra-no-pole-audit.md", "boundary differentiability and bracket audit"),
    ("513-Gamma-Khat-q_loc-first-variation-or-demotion.md", "q_loc stress-divergence identity"),
    ("scripts/Y5_R10_projector_algebra_or_boundary_primitive_fill.py", "this checkpoint generator"),
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
            "algebra_id": "PAF600_0_parent_complex",
            "object": "relative memory-exchange complex",
            "conditional_fill": "E_rel^0 --d_rel--> E_rel^1 --d_rel--> E_rel^2 on compact local collar, with Q_obs-owned metric/measure and boundary conditions",
            "algebra_test": "d_rel^2=0, boundary conditions are fixed before variation, ordinary GR mass flux is not in E_rel",
            "result": "conditional_fill",
            "blocker": "parent reduced complex and field content are not derived from current MTS action",
            "valid_for_claim": "false",
        },
        {
            "algebra_id": "PAF600_1_relative_Hodge_split",
            "object": "J_rel decomposition",
            "conditional_fill": "J_rel=d_rel A_rel + delta_rel C_rel + H_rel with relative boundary conditions",
            "algebra_test": "H_rel=0 by compact trivial relative cohomology or is separately bounded as a topological source row",
            "result": "conditional_split_written",
            "blocker": "relative cohomology/triviality theorem not proved for current local collars",
            "valid_for_claim": "false",
        },
        {
            "algebra_id": "PAF600_2_projector_definition",
            "object": "P_loc",
            "conditional_fill": "P_loc := Pi_exact,rel or Pi_obs depending on convention; it is an idempotent Q_obs-owned projector constructed from the relative Laplacian Green operator",
            "algebra_test": "P_loc^2=P_loc, Lie_vX(P_loc)=0, [P_loc,d_rel]=0 on the chosen relative domain",
            "result": "formal_algebra_pass_if_complex_exists",
            "blocker": "Green operator/domain data not parent-owned; zero modes/harmonic classes not excluded",
            "valid_for_claim": "false",
        },
        {
            "algebra_id": "PAF600_3_no_hidden_kernel",
            "object": "ker(P_loc)",
            "conditional_fill": "ker(P_loc) contains only exact/gauge representative exchange or explicitly retained harmonic/source rows",
            "algebra_test": "any observed residual in ker(P_loc) is routed to a residual row, not discarded",
            "result": "policy_gate_written",
            "blocker": "full unprojected q_loc vector and PPN/source map not yet filled",
            "valid_for_claim": "false",
        },
        {
            "algebra_id": "PAF600_4_pointwise_annihilation",
            "object": "P_loc d_rel J_rel",
            "conditional_fill": "If J_rel=d_rel A_rel and [P_loc,d_rel]=0 with P_loc d_rel^2=0, then P_loc d_rel J_rel=0 pointwise for the exact exchange sector",
            "algebra_test": "J_rel must be purely exact in the projected exchange sector; no harmonic/coexact/source part may remain",
            "result": "conditional_pointwise_zero_for_exact_sector_only",
            "blocker": "current MTS has not proved J_rel is purely exact; 220 retained pointwise failure",
            "valid_for_claim": "false",
        },
    ]


def make_boundary_rows() -> list[dict[str, str]]:
    return [
        {
            "primitive_id": "BPF600_0_relative_primitive",
            "object": "A_rel",
            "conditional_fill": "J_rel=d_rel A_rel in the memory/domain-exchange sector with A_rel|inner=A_rel|outer=0 or matched pure-gauge data",
            "would_kill": "integrated d_rel J_rel exchange through a compact stationary collar",
            "result": "conditional_integrated_zero_recovered",
            "blocker": "does not kill non-exact, harmonic, coexact, ordinary GR mass-flux, or source-measure terms",
            "valid_for_claim": "false",
        },
        {
            "primitive_id": "BPF600_1_GK_boundary_primitive",
            "object": "B_GK",
            "conditional_fill": "theta_GK(delta)-i_xi L_GK has boundary primitive B_GK fixed by the reduced action and reference subtraction",
            "would_kill": "boundary_flux in reduced Ward identity",
            "result": "not_filled",
            "blocker": "actual S_GK/Gamma/Khat metric-response match is still absent",
            "valid_for_claim": "false",
        },
        {
            "primitive_id": "BPF600_2_mass_channel_projection",
            "object": "Pi_M^H[Q_boundary]",
            "conditional_fill": "boundary primitive has zero projection into measured Hamiltonian mass/source channel",
            "would_kill": "source-measure boundary leakage",
            "result": "not_derived",
            "blocker": "source-measure projection map and weak-field normalization not filled",
            "valid_for_claim": "false",
        },
        {
            "primitive_id": "BPF600_3_alpha3_pressure",
            "object": "momentum/preferred-frame boundary flux",
            "conditional_fill": "boundary primitive is parity-even/topological or has zero preferred-frame momentum component",
            "would_kill": "alpha3-equivalent boundary pressure",
            "result": "not_derived",
            "blocker": "alpha3 coefficient map from boundary flux is missing",
            "valid_for_claim": "false",
        },
    ]


def make_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "PIG600_0_exact_sector",
            "claim": "projector algebra can give pointwise zero for the exact memory-exchange sector",
            "status": "conditional_pass",
            "why": "P_loc d_rel d_rel A_rel=0 if the relative complex exists and P_loc commutes with d_rel",
            "not_enough_for": "full observed q_loc zero",
        },
        {
            "gate_id": "PIG600_1_integrated_vs_pointwise",
            "claim": "boundary primitive gives integrated compact-collar zero",
            "status": "conditional_integrated_only",
            "why": "Stokes kills exact exchange with vanishing boundary primitive",
            "not_enough_for": "pointwise PPN/local metric silence unless exact-sector projection is parent-derived",
        },
        {
            "gate_id": "PIG600_2_harmonic_source_classes",
            "claim": "harmonic/coexact/source classes vanish",
            "status": "not_derived",
            "why": "relative cohomology and source-measure projection have not been proven trivial",
            "not_enough_for": "deleting compact-shell residual rows",
        },
        {
            "gate_id": "PIG600_3_ordinary_GR_flux_separation",
            "claim": "J_rel excludes ordinary gravitational/Gauss mass flux",
            "status": "contract_only",
            "why": "220 explicitly warns ordinary mass flux must remain separate",
            "not_enough_for": "source-normalized Newton/GR",
        },
        {
            "gate_id": "PIG600_4_score_status",
            "claim": "compact-shell residual is scored",
            "status": "blocked",
            "why": "unit/projection map is still missing",
            "not_enough_for": "R10/PPN/local-bound pass",
        },
    ]


def make_runner_rows() -> list[dict[str, str]]:
    return [
        {
            "runner_id": "RU600_0_exact_exchange_sector",
            "previous_status": "open",
            "new_status": "conditional_zero_if_relative_complex_exists",
            "reason": "projector algebra kills P_loc d_rel d_rel A_rel for purely exact exchange sector",
            "still_needed": "parent relative complex and proof J_rel is purely exact in this sector",
            "valid_for_claim": "false",
        },
        {
            "runner_id": "RU600_1_integrated_boundary_exchange",
            "previous_status": "open",
            "new_status": "conditional_integrated_zero",
            "reason": "A_rel primitive with vanishing/matched boundary data recovers Stokes zero",
            "still_needed": "pointwise projection and non-exact class exclusion",
            "valid_for_claim": "false",
        },
        {
            "runner_id": "RU600_2_observed_q_loc",
            "previous_status": "still_open",
            "new_status": "still_open",
            "reason": "observed q_loc can contain non-exact/harmonic/source-measure components",
            "still_needed": "Ward zero, source-free Euler equations, boundary source-measure zero",
            "valid_for_claim": "false",
        },
        {
            "runner_id": "RU600_3_compact_shell_score",
            "previous_status": "blocked_by_missing_unit_map",
            "new_status": "blocked_by_missing_unit_map",
            "reason": "conditional algebra is not a physical numeric score",
            "still_needed": "unit/projection map from compact-shell proxy to local observables",
            "valid_for_claim": "false",
        },
    ]


def make_decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "D600_0_projector_algebra_filled_conditionally",
            "decision": "write relative projector algebra as conditional fill",
            "meaning": "P_loc can be a real algebraic projector if a parent relative complex/Hodge split exists",
            "claim_status": "conditional_not_current_MTS_claim",
            "next_target": NEXT_TARGET,
        },
        {
            "decision_id": "D600_1_exact_sector_zero_only",
            "decision": "accept pointwise zero only for purely exact exchange sector",
            "meaning": "P_loc d_rel d_rel A_rel=0 is real algebra, but J_rel exactness remains unproved",
            "claim_status": "partial_zero_contract",
            "next_target": NEXT_TARGET,
        },
        {
            "decision_id": "D600_2_boundary_primitive_integrated_only",
            "decision": "recover conditional integrated boundary zero, not full source-measure silence",
            "meaning": "boundary primitive helps, but does not close PPN/local q_loc by itself",
            "claim_status": "boundary_flux_still_open",
            "next_target": NEXT_TARGET,
        },
        {
            "decision_id": "D600_3_compact_score_still_blocked",
            "decision": "defer compact-shell score again",
            "meaning": "no unit/projection map exists yet",
            "claim_status": "score_blocked",
            "next_target": NEXT_TARGET,
        },
    ]


def make_route_update_rows() -> list[dict[str, str]]:
    return [
        {
            "route_id": "RU600_0_allowed",
            "allowed_after_600": "use relative projector algebra as a conditional exact-sector theorem",
            "forbidden_after_600": "claim observed q_loc=0 from exact-sector algebra",
            "next_action": NEXT_TARGET,
        },
        {
            "route_id": "RU600_1_allowed",
            "allowed_after_600": "try to prove parent relative complex/trivial cohomology next",
            "forbidden_after_600": "assume J_rel has no harmonic/coexact/source class",
            "next_action": NEXT_TARGET,
        },
        {
            "route_id": "RU600_2_allowed",
            "allowed_after_600": "build compact-shell unit map only if derivation stalls",
            "forbidden_after_600": "score 7.432631961576971e-06 as a local-bound pass",
            "next_action": NEXT_TARGET,
        },
    ]


def make_summary_rows() -> list[dict[str, str]]:
    return [
        {
            "summary_id": "S600_0",
            "claim_allowed": "false",
            "R10_pass": "false",
            "WEP_pass": "false",
            "PPN_pass": "false",
            "local_GR_pass": "false",
            "projector_status": "conditional_relative_algebra_filled",
            "boundary_status": "integrated_exact_exchange_zero_only",
            "score_status": "compact_shell_unit_map_missing",
            "best_private_read": "600 fills the clean algebraic route conditionally: a parent relative complex/Hodge split would make P_loc honest and kill the exact exchange sector. It does not prove J_rel is purely exact, does not kill harmonic/source-measure terms, and does not score the compact-shell proxy.",
            "next_target": NEXT_TARGET,
        }
    ]


def make_validation(
    sources: list[dict[str, str]],
    projector_rows: list[dict[str, str]],
    boundary_rows: list[dict[str, str]],
    gate_rows: list[dict[str, str]],
    runner_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    prior_rows = read_csv(PRIOR_599_VALIDATION)
    prior_failures = [row for row in prior_rows if row.get("result", "").strip().lower() != "pass"]
    missing_sources = [row for row in sources if row["exists"] != "True"]
    claim_rows = [
        *[row for row in projector_rows if row["valid_for_claim"] == "true"],
        *[row for row in boundary_rows if row["valid_for_claim"] == "true"],
        *[row for row in runner_rows if row["valid_for_claim"] == "true"],
    ]
    relative_complex = any(row["algebra_id"] == "PAF600_0_parent_complex" for row in projector_rows)
    pointwise_exact = any(row["algebra_id"] == "PAF600_4_pointwise_annihilation" and "exact_sector_only" in row["result"] for row in projector_rows)
    boundary_integrated = any(row["primitive_id"] == "BPF600_0_relative_primitive" and "integrated_zero" in row["result"] for row in boundary_rows)
    harmonic_guard = any(row["gate_id"] == "PIG600_2_harmonic_source_classes" and row["status"] == "not_derived" for row in gate_rows)
    score_blocked = any(row["gate_id"] == "PIG600_4_score_status" and row["status"] == "blocked" for row in gate_rows)
    observed_open = any(row["runner_id"] == "RU600_2_observed_q_loc" and row["new_status"] == "still_open" for row in runner_rows)
    return [
        {
            "check_id": "V600_0_source_paths_exist",
            "result": "pass" if not missing_sources else "fail",
            "detail": f"missing={len(missing_sources)}",
        },
        {
            "check_id": "V600_1_prior_599_clean",
            "result": "pass" if prior_rows and not prior_failures else "fail",
            "detail": f"prior_rows={len(prior_rows)};prior_failures={len(prior_failures)}",
        },
        {
            "check_id": "V600_2_relative_projector_algebra_written",
            "result": "pass" if relative_complex and pointwise_exact else "fail",
            "detail": f"projector_rows={len(projector_rows)}",
        },
        {
            "check_id": "V600_3_boundary_primitive_integrated_only",
            "result": "pass" if boundary_integrated else "fail",
            "detail": f"boundary_rows={len(boundary_rows)}",
        },
        {
            "check_id": "V600_4_harmonic_source_guard_retained",
            "result": "pass" if harmonic_guard else "fail",
            "detail": "non-exact/harmonic/source classes not killed",
        },
        {
            "check_id": "V600_5_observed_q_loc_and_score_still_open",
            "result": "pass" if observed_open and score_blocked else "fail",
            "detail": f"observed_open={observed_open};score_blocked={score_blocked}",
        },
        {
            "check_id": "V600_6_no_claim_rows",
            "result": "pass" if not claim_rows else "fail",
            "detail": f"claim_rows={len(claim_rows)}",
        },
        {
            "check_id": "V600_7_no_R10_or_local_GR_claim",
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
    gate_rows: list[dict[str, str]],
    runner_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    route_update_rows: list[dict[str, str]],
    validation_rows: list[dict[str, str]],
) -> None:
    text = f"""# 600 Y5 R10 projector algebra or boundary primitive fill

Generated: {generated}  
Status: `{STATUS}`  
Claim ceiling: `{CLAIM_CEILING}`  
Next target: `{NEXT_TARGET}`  
Run root: `{rel(run_root)}`

## Verdict
- Projector algebra can be filled conditionally: if the local memory-exchange sector is a parent relative complex with a Hodge-style split, `P_loc` can be idempotent, Q_obs-owned, and vertical-blind.
- The exact exchange sector then has a real pointwise algebraic zero: `P_loc d_rel d_rel A_rel=0`.
- Boundary primitive is also useful, but only conditionally/integrated: `J_rel=d_rel A_rel` with vanishing or matched boundary data kills integrated exact exchange through the compact collar.
- This still does not derive observed `q_loc=0`. The missing pieces are exactly the dangerous ones: prove `J_rel` is purely exact, kill harmonic/coexact/source classes, separate ordinary GR mass flux, and build a physical unit map before scoring.

## Source Register
{markdown_table(sources, ["source_file", "exists", "role"])}

## Projector Algebra Fill
{markdown_table(projector_rows, ["algebra_id", "object", "conditional_fill", "algebra_test", "result", "blocker", "valid_for_claim"])}

## Boundary Primitive Fill
{markdown_table(boundary_rows, ["primitive_id", "object", "conditional_fill", "would_kill", "result", "blocker", "valid_for_claim"])}

## Pointwise Vs Integrated Gate
{markdown_table(gate_rows, ["gate_id", "claim", "status", "why", "not_enough_for"])}

## Runner Update
{markdown_table(runner_rows, ["runner_id", "previous_status", "new_status", "reason", "still_needed", "valid_for_claim"])}

## Decision
{markdown_table(decision_rows, ["decision_id", "decision", "meaning", "claim_status", "next_target"])}

## Route Update
{markdown_table(route_update_rows, ["route_id", "allowed_after_600", "forbidden_after_600", "next_action"])}

## Validation
{markdown_table(validation_rows, ["check_id", "result", "detail"])}

## Practical Read
This is a good technical squeeze. We found a clean algebraic way the projector could be real rather than hand-wavy. But it buys a precise thing: exact-sector silence. It does not buy local GR. To make it bite harder, next we must prove the relative complex/trivial cohomology is actually the parent MTS local sector, or else build the compact-shell unit map and start scoring.
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def main() -> int:
    generated = datetime.now(timezone.utc).isoformat()
    run_root = RUNS / f"{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}-{SLUG}"
    run_root.mkdir(parents=True, exist_ok=True)

    sources = make_sources()
    projector_rows = make_projector_rows()
    boundary_rows = make_boundary_rows()
    gate_rows = make_gate_rows()
    runner_rows = make_runner_rows()
    decision_rows = make_decision_rows()
    route_update_rows = make_route_update_rows()
    summary_rows = make_summary_rows()
    validation_rows = make_validation(sources, projector_rows, boundary_rows, gate_rows, runner_rows)

    write_csv(SOURCE_REGISTER_PATH, sources, ["source_file", "exists", "role"])
    write_csv(PROJECTOR_ALGEBRA_PATH, projector_rows, ["algebra_id", "object", "conditional_fill", "algebra_test", "result", "blocker", "valid_for_claim"])
    write_csv(BOUNDARY_PRIMITIVE_PATH, boundary_rows, ["primitive_id", "object", "conditional_fill", "would_kill", "result", "blocker", "valid_for_claim"])
    write_csv(POINTWISE_GATE_PATH, gate_rows, ["gate_id", "claim", "status", "why", "not_enough_for"])
    write_csv(RUNNER_UPDATE_PATH, runner_rows, ["runner_id", "previous_status", "new_status", "reason", "still_needed", "valid_for_claim"])
    write_csv(DECISION_PATH, decision_rows, ["decision_id", "decision", "meaning", "claim_status", "next_target"])
    write_csv(ROUTE_UPDATE_PATH, route_update_rows, ["route_id", "allowed_after_600", "forbidden_after_600", "next_action"])
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
            "score_status",
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
        gate_rows,
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
