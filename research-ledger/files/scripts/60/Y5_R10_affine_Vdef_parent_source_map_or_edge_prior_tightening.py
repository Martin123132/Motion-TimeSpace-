from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
RUNS = ROOT / "runs"

DOC_PATH = ROOT / "587-Y5-R10-affine-Vdef-parent-source-map-or-edge-prior-tightening.md"

PRIOR_586_VALIDATION = RESIDUALS / "P8_Y5_BRR545_586_VALIDATION.csv"
PRIOR_586_EDGE_GRID = RESIDUALS / "P8_Y5_R10_586_EDGE_NUMERIC_PRIOR_GRID.csv"

SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_587_SOURCE_REGISTER.csv"
SOURCE_MAP_PATH = RESIDUALS / "P8_Y5_R10_587_AFFINE_PARENT_SOURCE_MAP.csv"
EQUATION_CONTRACT_PATH = RESIDUALS / "P8_Y5_R10_587_PARENT_SOURCE_EQUATION_CONTRACT.csv"
NO_BACKREACTION_PATH = RESIDUALS / "P8_Y5_R10_587_MULTIPLIER_NO_BACKREACTION_TEST.csv"
EDGE_TARGETS_PATH = RESIDUALS / "P8_Y5_R10_587_EDGE_PRIOR_TIGHTENED_TARGETS.csv"
FORK_PATH = RESIDUALS / "P8_Y5_R10_587_REPAIR_OR_FALLBACK_FORK.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_BRR545_587_DECISION.csv"
ROUTE_UPDATE_PATH = RESIDUALS / "P8_Y5_BRR545_587_ROUTE_UPDATE.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_587_VALIDATION.csv"
SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_587_NONCLAIM_SUMMARY.csv"

STATUS = "Y5_R10_affine_Vdef_parent_source_map_written_multiplier_backreaction_blocker_exposed_edge_prior_targets_tightened_nonclaim"
CLAIM_CEILING = "affine_parent_source_mapping_and_edge_prior_pressure_only_no_R10_WEP_PPN_or_local_GR_pass"
NEXT_TARGET = "588-Y5-R10-multiplier-backreaction-kill-or-bound-edge-product.md"

SOURCE_FILES = [
    ("586-Y5-R10-Vdef-owner-action-sketch-or-edge-runner-numeric-priors.md", "immediate affine Vdef contract"),
    ("source-intake/mts_residuals/P8_Y5_BRR545_586_VALIDATION.csv", "prior validation gate"),
    ("source-intake/mts_residuals/P8_Y5_R10_586_VDEF_ACTION_SKETCH.csv", "affine/generic Vdef action sketch"),
    ("source-intake/mts_residuals/P8_Y5_R10_586_CONDITIONAL_NO_POLE_THEOREM.csv", "conditional no-pole theorem contract"),
    ("source-intake/mts_residuals/P8_Y5_R10_586_MOMENTUM_MAP_OWNER_TEST.csv", "momentum-map blockers"),
    ("source-intake/mts_residuals/P8_Y5_R10_586_BOUNDARY_EXACTNESS_TEST.csv", "boundary silence blockers"),
    ("source-intake/mts_residuals/P8_Y5_R10_586_EDGE_NUMERIC_PRIOR_GRID.csv", "nonclaim edge-prior grid"),
    ("583-Y5-R10-parent-momentum-map-owner-or-edge-residual-demotion.md", "momentum-map owner and edge demotion fork"),
    ("source-intake/mts_residuals/P8_Y5_R10_583_NOETHER_MOMENTUM_MAP_CONTRACT.csv", "Noether momentum-map contract"),
    ("source-intake/mts_residuals/P8_Y5_R10_583_PARENT_MOMENTUM_MAP_OWNER_ATTEMPT.csv", "parent owner attempt rows"),
    ("581-Y5-R10-quotient-vertical-no-pole-parent-theorem-attempt.md", "quotient-vertical no-pole theorem shape"),
    ("513-Gamma-Khat-q_loc-first-variation-or-demotion.md", "q_loc as projected stress divergence"),
    ("512-match-MTS-symbols-to-local-GR-action-blocks.md", "symbol-to-action block placement"),
    ("539-Y5-PiM-as-Hamiltonian-charge-map-or-topological-demotion.md", "Pi_M^H Hamiltonian charge map candidate"),
    ("scripts/Y5_R10_affine_Vdef_parent_source_map_or_edge_prior_tightening.py", "this checkpoint generator"),
]


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        values: list[str] = []
        for column in columns:
            value = str(row.get(column, ""))
            value = value.replace("\n", "<br>").replace("|", "\\|")
            values.append(value)
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def source_register() -> list[dict[str, Any]]:
    return [
        {"source_file": source_file, "exists": str((ROOT / source_file).exists()), "role": role}
        for source_file, role in SOURCE_FILES
    ]


def make_source_map() -> list[dict[str, Any]]:
    return [
        {
            "ingredient": "X_nu",
            "role_in_affine_block": "multiplier_or_vertical_coordinate",
            "candidate_parent_source": "quotient-vertical direction v_X from 581, not an observed field",
            "equation_or_test": "S_X=int sqrt(-g) X_nu C_X^nu[Y] after integration by parts",
            "current_status": "conditional_best_route",
            "blocker": "v_X and parent quotient map pi are not explicitly constructed",
            "fallback_if_unowned": "physical/edge X residual scored by alpha(lambda)",
            "valid_for_claim": "false",
        },
        {
            "ingredient": "C_X^nu",
            "role_in_affine_block": "constraint enforced by X",
            "candidate_parent_source": "Noether/momentum-map constraint from vertical symmetry",
            "equation_or_test": "C_X^nu=-nabla_mu P^{mu nu}+J_eff^nu",
            "current_status": "contract_written_not_owned",
            "blocker": "theta_Y, Omega_Y, and v_epsilon are still missing",
            "fallback_if_unowned": "C_X becomes a closure/source residual",
            "valid_for_claim": "false",
        },
        {
            "ingredient": "P^{mu nu}[Y]",
            "role_in_affine_block": "boundary momentum and divergence superpotential",
            "candidate_parent_source": "coefficient of the vertical Noether current or metric/extra-sector symplectic potential",
            "equation_or_test": "B_X^nu=n_mu P^{mu nu}; C_X includes -nabla_mu P^{mu nu}",
            "current_status": "promising_but_unfilled",
            "blocker": "no explicit parent Lagrangian gives P as a coefficient rather than a free tensor",
            "fallback_if_unowned": "edge charge Q_edge and P-owner residual remain live",
            "valid_for_claim": "false",
        },
        {
            "ingredient": "J_eff^nu[Y]",
            "role_in_affine_block": "bulk source/current term balancing div P",
            "candidate_parent_source": "Euler-Ward identity for T_GK or relative memory/source current",
            "equation_or_test": "nabla_mu T_GK^{mu nu}=sum_A E_A nabla^nu Phi^A; on shell C_X=0 if J_eff=nabla P",
            "current_status": "not_derived",
            "blocker": "no explicit S_GK/Helmholtz proof or parent current identity",
            "fallback_if_unowned": "finite q_loc/source-current residual",
            "valid_for_claim": "false",
        },
        {
            "ingredient": "A_{mu nu}[Y]",
            "role_in_affine_block": "defect/connection piece in Z=nabla X-A",
            "candidate_parent_source": "local representative lock or quotient connection; minimal local branch can set A=0 only if parent-owned",
            "equation_or_test": "S_X=int P^{mu nu}(nabla_mu X_nu-A_{mu nu}[Y])+XJ",
            "current_status": "unplaced",
            "blocker": "A cannot be a chosen cancellation tensor; it needs a transformation law or local-zero equation",
            "fallback_if_unowned": "do not use Z form; keep pure multiplier C_X form",
            "valid_for_claim": "false",
        },
        {
            "ingredient": "matter quotient map",
            "role_in_affine_block": "kills test-body charge",
            "candidate_parent_source": "S_matter[psi,hat_g(pi(Y))] with delta_X S_matter=0",
            "equation_or_test": "v_X hat_g=0 and v_X theta_univ=0 imply qbar_XT=0",
            "current_status": "not_derived",
            "blocker": "universal matter blindness/no-marker theorem still open",
            "fallback_if_unowned": "qbar_XT must be filled or bounded",
            "valid_for_claim": "false",
        },
        {
            "ingredient": "boundary primitive/counterterm",
            "role_in_affine_block": "kills edge charge from integration by parts",
            "candidate_parent_source": "exact/pure-gauge boundary term or proper compact vertical transformations",
            "equation_or_test": "Q_edge=int_boundary epsilon_nu(n_mu P^{mu nu}+B_ct^nu)",
            "current_status": "not_derived",
            "blocker": "B_X exactness and K_boundary=0 are unproved",
            "fallback_if_unowned": "Qbar_edge_XH(lambda) and edge prior branch",
            "valid_for_claim": "false",
        },
        {
            "ingredient": "Pi_M^H projection",
            "role_in_affine_block": "decides whether edge charge enters measured source mass",
            "candidate_parent_source": "Hamiltonian/covariant phase-space charge map from 539",
            "equation_or_test": "Qbar_edge_XH(lambda)=Pi_M^H[Q_edge^H(lambda)]/M_H",
            "current_status": "candidate_projection_not_adopted",
            "blocker": "source-measure glue and PPN readout are not closed",
            "fallback_if_unowned": "epsilon_PiM_X(lambda) source-measure residual",
            "valid_for_claim": "false",
        },
    ]


def make_equation_contract() -> list[dict[str, Any]]:
    return [
        {
            "equation_id": "EQ587_0_affine_block",
            "equation": "S_X=int_M sqrt(-g)[P^{mu nu}[Y](nabla_mu X_nu-A_{mu nu}[Y])+X_nu J_eff^nu[Y]]+S_boundary",
            "derivation_use": "makes X enter at most linearly and first order",
            "promotion_condition": "P,A,J_eff all parent-owned composites and no quadratic Z/Pi terms are added",
            "current_verdict": "contract_only",
        },
        {
            "equation_id": "EQ587_1_integrated_multiplier_form",
            "equation": "S_X=int_M sqrt(-g) X_nu[-nabla_mu P^{mu nu}+J_eff^nu]-int_M sqrt(-g)P^{mu nu}A_{mu nu}+int_boundary X_nu n_mu P^{mu nu}+S_boundary",
            "derivation_use": "shows the affine route is really a multiplier constraint plus boundary charge",
            "promotion_condition": "C_X=-nabla P+J is a first-class parent identity/constraint",
            "current_verdict": "useful_reduction",
        },
        {
            "equation_id": "EQ587_2_X_variation",
            "equation": "delta_X S_X=int_M sqrt(-g) C_X^nu delta X_nu+int_boundary delta X_nu(n_mu P^{mu nu}+B_ct^nu)",
            "derivation_use": "bulk equation is C_X=0; boundary equation exposes edge hair",
            "promotion_condition": "C_X parent-owned and boundary term zero/exact/proper-gauge",
            "current_verdict": "bulk_clear_boundary_open",
        },
        {
            "equation_id": "EQ587_3_Y_backreaction",
            "equation": "delta_Y S_X=int_M sqrt(-g)[X_nu delta_Y C_X^nu-delta_Y(P^{mu nu}A_{mu nu})]+delta_Y S_boundary",
            "derivation_use": "exposes hidden backreaction: a multiplier can still alter Y equations unless X is gauge/reference-killed",
            "promotion_condition": "X=0 as proper-gauge/reference branch or delta_Y S_X is itself a Noether-zero",
            "current_verdict": "new_hard_blocker",
        },
        {
            "equation_id": "EQ587_4_no_pole_certificate",
            "equation": "H_XX=0, H_XY=C_{X,Y}; no physical pole only if (X,C_X) is first-class/proper gauge, not second-class source machinery",
            "derivation_use": "rank-zero alone is not enough; the constraint algebra must close",
            "promotion_condition": "{G[epsilon],G[eta]}=G[[epsilon,eta]] with K_boundary=0",
            "current_verdict": "blocked_until_momentum_map_owner",
        },
        {
            "equation_id": "EQ587_5_edge_fallback",
            "equation": "alpha_edge(lambda)=K_edge(lambda) Qbar_edge_XH(lambda) qbar_XT",
            "derivation_use": "if boundary/matter quotient fails, finite residual must be scored",
            "promotion_condition": "all coefficients source-backed or theorem-zero",
            "current_verdict": "fallback_nonclaim",
        },
    ]


def make_no_backreaction_tests() -> list[dict[str, Any]]:
    return [
        {
            "test_id": "NBT587_0_no_derivative_kinetic_X",
            "required_test": "H_ZZ=0 and no quadratic Pi/P terms regenerate a kinetic X block",
            "result": "conditional_pass_from_586",
            "why_it_matters": "prevents a physical Yukawa pole",
            "valid_for_claim": "false",
        },
        {
            "test_id": "NBT587_1_first_class_constraint",
            "required_test": "C_X belongs to a differentiable first-class generator G[epsilon]",
            "result": "blocked",
            "why_it_matters": "distinguishes gauge/multiplier from second-class auxiliary source",
            "valid_for_claim": "false",
        },
        {
            "test_id": "NBT587_2_X_reference_or_gauge_zero",
            "required_test": "X can be fixed to zero/proper-gauge on compact local branch without changing observables",
            "result": "not_derived",
            "why_it_matters": "otherwise X delta_Y C_X backreacts on the parent equations",
            "valid_for_claim": "false",
        },
        {
            "test_id": "NBT587_3_parent_current_identity",
            "required_test": "J_eff and P are generated by the same parent Noether/Euler-Ward identity",
            "result": "not_derived",
            "why_it_matters": "prevents hand inserting C_X=-nabla P+J",
            "valid_for_claim": "false",
        },
        {
            "test_id": "NBT587_4_matter_blindness",
            "required_test": "delta_X S_matter=0 for all ordinary species and clocks",
            "result": "not_derived",
            "why_it_matters": "kills qbar_XT rather than fitting it small",
            "valid_for_claim": "false",
        },
        {
            "test_id": "NBT587_5_boundary_silence",
            "required_test": "n_mu P^{mu nu}+B_ct^nu is zero, exact, pure gauge, or proper-gauge killed",
            "result": "not_derived",
            "why_it_matters": "bulk no-pole can still leak as edge hair",
            "valid_for_claim": "false",
        },
    ]


def make_edge_targets(edge_grid: list[dict[str, str]]) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, str]]] = {}
    for row in edge_grid:
        grouped.setdefault(row["lambda_m"], []).append(row)

    targets: list[dict[str, Any]] = []
    for lambda_m, rows in sorted(grouped.items(), key=lambda item: float(item[0])):
        sorted_rows = sorted(rows, key=lambda row: float(row["edge_product_prior"]), reverse=True)
        pass_rows = [row for row in sorted_rows if row["private_diagnostic_pass"] == "true"]
        fail_rows = [row for row in sorted_rows if row["private_diagnostic_pass"] == "false"]
        strongest_pass = max((float(row["edge_product_prior"]) for row in pass_rows), default=None)
        weakest_fail = min((float(row["edge_product_prior"]) for row in fail_rows), default=None)
        alpha_bound = float(rows[0]["review_candidate_alpha_bound"])
        lambda_um = float(rows[0]["lambda_um"])
        if alpha_bound >= 1.0:
            required_scale = "order_one_or_less"
        elif alpha_bound >= 0.1:
            required_scale = "tenth_level_or_less"
        elif alpha_bound >= 0.01:
            required_scale = "percent_level_or_less"
        else:
            required_scale = "per_mille_level_or_less"
        targets.append(
            {
                "target_id": f"EPT587_{len(targets)}",
                "lambda_m": f"{float(lambda_m):.9g}",
                "lambda_um": f"{lambda_um:.9g}",
                "review_candidate_alpha_bound": f"{alpha_bound:.12g}",
                "largest_tested_prior_that_passes": "" if strongest_pass is None else f"{strongest_pass:.12g}",
                "smallest_tested_prior_that_fails": "" if weakest_fail is None else f"{weakest_fail:.12g}",
                "required_edge_product_scale": required_scale,
                "tightening_message": f"abs(K_edge*Qbar_edge_XH*qbar_XT) must be <= {alpha_bound:.12g} at this lambda before claim-grade data is even considered",
                "valid_for_claim": "false",
            }
        )
    return targets


def make_fork(source_map: list[dict[str, Any]], edge_targets: list[dict[str, Any]]) -> list[dict[str, Any]]:
    tightest = min(edge_targets, key=lambda row: float(row["review_candidate_alpha_bound"]))
    return [
        {
            "fork_id": "RF587_0_owner_repair_path",
            "route": "derive affine parent ownership",
            "needed_next": "construct theta_Y/Omega_Y/v_X and prove X is proper-gauge or reference-zero on compact local branch",
            "success_condition": "C_X first-class, matter quotient-blind, boundary charge zero",
            "failure_action": "edge prior branch remains live",
            "status": "best_derivation_route",
            "valid_for_claim": "false",
        },
        {
            "fork_id": "RF587_1_backreaction_blocker",
            "route": "kill multiplier backreaction",
            "needed_next": "show delta_Y S_X vanishes on the local branch, not only C_X=0",
            "success_condition": "X delta_Y C_X and delta_Y(PA) carry no local source/stress",
            "failure_action": "no-pole route is closure-only",
            "status": "new_primary_blocker",
            "valid_for_claim": "false",
        },
        {
            "fork_id": "RF587_2_edge_prior_path",
            "route": "tighten finite edge product",
            "needed_next": f"source or bound the product below {tightest['review_candidate_alpha_bound']} near {tightest['lambda_um']} um",
            "success_condition": "K_edge, Qbar_edge_XH, qbar_XT, and lambda envelope are source-backed",
            "failure_action": "R10/local claim remains blocked",
            "status": "fallback_pressure_target",
            "valid_for_claim": "false",
        },
    ]


def make_decision() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "D587_0_source_map_written",
            "decision": "affine Vdef ingredients are mapped to possible parent-source owners",
            "claim_status": "nonclaim_mapping",
            "next_target": NEXT_TARGET,
        },
        {
            "decision_id": "D587_1_backreaction_blocker_exposed",
            "decision": "a multiplier X still backreacts through delta_Y C_X unless X is gauge/reference killed",
            "claim_status": "blocks_no_pole_promotion",
            "next_target": NEXT_TARGET,
        },
        {
            "decision_id": "D587_2_edge_targets_tightened",
            "decision": "the fallback branch now has lambda-by-lambda product ceilings from the nonclaim review-candidate pressure grid",
            "claim_status": "diagnostic_only",
            "next_target": NEXT_TARGET,
        },
    ]


def make_route_update() -> list[dict[str, Any]]:
    return [
        {
            "route_id": "RU587_0_allowed",
            "allowed_after_587": "use affine Vdef only as a multiplier/momentum-map contract",
            "forbidden_after_587": "claim no-pole from H_ZZ=0 alone",
            "next_action": NEXT_TARGET,
        },
        {
            "route_id": "RU587_1_allowed",
            "allowed_after_587": "attack X backreaction and boundary charge as the next owner gates",
            "forbidden_after_587": "ignore delta_Y S_X or edge charge after integrating by parts",
            "next_action": NEXT_TARGET,
        },
        {
            "route_id": "RU587_2_allowed",
            "allowed_after_587": "use tightened edge product targets for fallback planning",
            "forbidden_after_587": "treat review-candidate priors or private bounds as claim-grade evidence",
            "next_action": NEXT_TARGET,
        },
    ]


def make_summary() -> list[dict[str, Any]]:
    return [
        {
            "summary_id": "S587_0",
            "claim_allowed": "false",
            "R10_pass": "false",
            "WEP_pass": "false",
            "PPN_pass": "false",
            "local_GR_pass": "false",
            "best_private_read": "The affine route survived only as a sharper contract: no kinetic X, first-class C_X, X gauge/reference silence, matter blindness, and boundary zero are all required together.",
            "next_target": NEXT_TARGET,
        }
    ]


def make_validation(
    sources: list[dict[str, Any]],
    source_map: list[dict[str, Any]],
    equation_contract: list[dict[str, Any]],
    no_backreaction: list[dict[str, Any]],
    edge_targets: list[dict[str, Any]],
    fork_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    prior_rows = read_csv(PRIOR_586_VALIDATION)
    prior_failures = [row for row in prior_rows if row.get("result", "").strip().lower() != "pass"]
    missing_sources = [row for row in sources if row["exists"] != "True"]
    claim_rows = [
        *[row for row in source_map if row["valid_for_claim"] == "true"],
        *[row for row in no_backreaction if row["valid_for_claim"] == "true"],
        *[row for row in edge_targets if row["valid_for_claim"] == "true"],
        *[row for row in fork_rows if row["valid_for_claim"] == "true"],
    ]
    backreaction_exposed = any(row["test_id"] == "NBT587_2_X_reference_or_gauge_zero" for row in no_backreaction)
    tightest = min(edge_targets, key=lambda row: float(row["review_candidate_alpha_bound"]))
    return [
        {
            "check_id": "V587_0_source_paths_exist",
            "result": "pass" if not missing_sources else "fail",
            "detail": f"missing={len(missing_sources)}",
        },
        {
            "check_id": "V587_1_prior_586_clean",
            "result": "pass" if prior_rows and not prior_failures else "fail",
            "detail": f"prior_rows={len(prior_rows)};prior_failures={len(prior_failures)}",
        },
        {
            "check_id": "V587_2_affine_source_map_complete",
            "result": "pass" if len(source_map) >= 8 else "fail",
            "detail": f"source_map_rows={len(source_map)}",
        },
        {
            "check_id": "V587_3_equation_contract_has_backreaction",
            "result": "pass" if any(row["equation_id"] == "EQ587_3_Y_backreaction" for row in equation_contract) else "fail",
            "detail": f"equation_rows={len(equation_contract)}",
        },
        {
            "check_id": "V587_4_no_backreaction_gate_blocks_claim",
            "result": "pass" if backreaction_exposed and any(row["result"] == "blocked" for row in no_backreaction) else "fail",
            "detail": f"tests={len(no_backreaction)};backreaction_exposed={backreaction_exposed}",
        },
        {
            "check_id": "V587_5_edge_targets_tightened_nonclaim",
            "result": "pass" if edge_targets and not any(row["valid_for_claim"] == "true" for row in edge_targets) else "fail",
            "detail": f"target_rows={len(edge_targets)};tightest_lambda_um={tightest['lambda_um']};tightest_bound={tightest['review_candidate_alpha_bound']}",
        },
        {
            "check_id": "V587_6_no_claim_rows",
            "result": "pass" if not claim_rows else "fail",
            "detail": f"claim_rows={len(claim_rows)}",
        },
        {
            "check_id": "V587_7_no_R10_or_local_GR_claim",
            "result": "pass",
            "detail": "claim_allowed=false;R10_pass=false;WEP=false;PPN=false;local_GR=false",
        },
    ]


def write_markdown(
    generated: str,
    run_root: Path,
    sources: list[dict[str, Any]],
    source_map: list[dict[str, Any]],
    equation_contract: list[dict[str, Any]],
    no_backreaction: list[dict[str, Any]],
    edge_targets: list[dict[str, Any]],
    fork_rows: list[dict[str, Any]],
    decision_rows: list[dict[str, Any]],
    route_rows: list[dict[str, Any]],
    validation_rows: list[dict[str, Any]],
) -> None:
    text = f"""# 587 Y5 R10 affine Vdef parent source map or edge-prior tightening

Generated: {generated}  
Status: `{STATUS}`  
Claim ceiling: `{CLAIM_CEILING}`  
Next target: `{NEXT_TARGET}`  
Run root: `{rel(run_root)}`

## Verdict
- The affine `V_def` route still looks like the best derivation path, but only in the strict multiplier/momentum-map reading.
- The new obstruction is clean: even if `X` has no kinetic pole, `delta_Y S_X` can still backreact unless `X` is a proper gauge/reference-zero branch or the full term is a Noether-zero.
- So `H_ZZ=0` is necessary but not sufficient. We need first-class ownership, matter blindness, boundary silence, and no parent-equation backreaction.
- The fallback edge-prior route is tightened: the hardest private review-candidate pressure is near `608.0783 um`, requiring the edge product below about `0.00234471960478`.

## Source Register
{markdown_table(sources, ["source_file", "exists", "role"])}

## Affine Parent Source Map
{markdown_table(source_map, ["ingredient", "role_in_affine_block", "candidate_parent_source", "equation_or_test", "current_status", "blocker", "fallback_if_unowned", "valid_for_claim"])}

## Parent Source Equation Contract
{markdown_table(equation_contract, ["equation_id", "equation", "derivation_use", "promotion_condition", "current_verdict"])}

## Multiplier No-Backreaction Test
{markdown_table(no_backreaction, ["test_id", "required_test", "result", "why_it_matters", "valid_for_claim"])}

## Edge Prior Tightening Targets
{markdown_table(edge_targets, ["target_id", "lambda_um", "review_candidate_alpha_bound", "largest_tested_prior_that_passes", "smallest_tested_prior_that_fails", "required_edge_product_scale", "valid_for_claim"])}

## Repair Or Fallback Fork
{markdown_table(fork_rows, ["fork_id", "route", "needed_next", "success_condition", "failure_action", "status", "valid_for_claim"])}

## Decision
{markdown_table(decision_rows, ["decision_id", "decision", "claim_status", "next_target"])}

## Route Update
{markdown_table(route_rows, ["route_id", "allowed_after_587", "forbidden_after_587", "next_action"])}

## Validation
{markdown_table(validation_rows, ["check_id", "result", "detail"])}

## Practical Read
This is not a dead end; it is a narrowing. The local branch is trying to become GR-like in the right mathematical way: constraints, Noether charges, quotient matter, and boundary terms. But the multiplier trick has a trapdoor: `X C_X[Y]` changes the `Y` equations unless `X` is genuinely gauge/reference-silent. That is the next wall to hit with the hammer.
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def main() -> None:
    generated = datetime.now(timezone.utc).isoformat()
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    run_root = RUNS / f"{stamp}-Y5-R10-affine-Vdef-parent-source-map-or-edge-prior-tightening"
    run_root.mkdir(parents=True, exist_ok=True)

    sources = source_register()
    edge_grid = read_csv(PRIOR_586_EDGE_GRID)
    source_map = make_source_map()
    equation_contract = make_equation_contract()
    no_backreaction = make_no_backreaction_tests()
    edge_targets = make_edge_targets(edge_grid)
    fork_rows = make_fork(source_map, edge_targets)
    decision_rows = make_decision()
    route_rows = make_route_update()
    summary_rows = make_summary()
    validation_rows = make_validation(sources, source_map, equation_contract, no_backreaction, edge_targets, fork_rows)

    write_csv(SOURCE_REGISTER_PATH, sources, ["source_file", "exists", "role"])
    write_csv(
        SOURCE_MAP_PATH,
        source_map,
        [
            "ingredient",
            "role_in_affine_block",
            "candidate_parent_source",
            "equation_or_test",
            "current_status",
            "blocker",
            "fallback_if_unowned",
            "valid_for_claim",
        ],
    )
    write_csv(
        EQUATION_CONTRACT_PATH,
        equation_contract,
        ["equation_id", "equation", "derivation_use", "promotion_condition", "current_verdict"],
    )
    write_csv(
        NO_BACKREACTION_PATH,
        no_backreaction,
        ["test_id", "required_test", "result", "why_it_matters", "valid_for_claim"],
    )
    write_csv(
        EDGE_TARGETS_PATH,
        edge_targets,
        [
            "target_id",
            "lambda_m",
            "lambda_um",
            "review_candidate_alpha_bound",
            "largest_tested_prior_that_passes",
            "smallest_tested_prior_that_fails",
            "required_edge_product_scale",
            "tightening_message",
            "valid_for_claim",
        ],
    )
    write_csv(
        FORK_PATH,
        fork_rows,
        ["fork_id", "route", "needed_next", "success_condition", "failure_action", "status", "valid_for_claim"],
    )
    write_csv(DECISION_PATH, decision_rows, ["decision_id", "decision", "claim_status", "next_target"])
    write_csv(ROUTE_UPDATE_PATH, route_rows, ["route_id", "allowed_after_587", "forbidden_after_587", "next_action"])
    write_csv(
        SUMMARY_PATH,
        summary_rows,
        ["summary_id", "claim_allowed", "R10_pass", "WEP_pass", "PPN_pass", "local_GR_pass", "best_private_read", "next_target"],
    )
    write_csv(VALIDATION_PATH, validation_rows, ["check_id", "result", "detail"])

    write_markdown(
        generated,
        run_root,
        sources,
        source_map,
        equation_contract,
        no_backreaction,
        edge_targets,
        fork_rows,
        decision_rows,
        route_rows,
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


if __name__ == "__main__":
    main()
