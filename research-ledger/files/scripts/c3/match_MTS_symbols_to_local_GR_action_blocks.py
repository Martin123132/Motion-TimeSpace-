from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

STATUS = "MTS_symbol_to_parent_action_matching_map_written_no_symbol_fully_promoted_local_GR_branch_still_conditional"
CLAIM_CEILING = "symbol_placement_and_first_variation_map_only_no_local_GR_or_Newton_promotion"
NEXT_TARGET = "513-Gamma-Khat-q_loc-first-variation-or-demotion.md"

DOC_PATH = Path("512-match-MTS-symbols-to-local-GR-action-blocks.md")
SOURCE_REGISTER_PATH = Path("source-intake/mts_residuals/P8_MTS_SYMBOL_MATCH_SOURCE_REGISTER.csv")
SYMBOL_MAP_PATH = Path("source-intake/mts_residuals/P8_MTS_SYMBOL_TO_LOCAL_GR_ACTION_MAP.csv")
FIRST_VARIATION_GATES_PATH = Path("source-intake/mts_residuals/P8_MTS_SYMBOL_FIRST_VARIATION_GATES.csv")
KEEP_KILL_RULES_PATH = Path("source-intake/mts_residuals/P8_MTS_SYMBOL_KEEP_KILL_RULES.csv")
DECISION_PATH = Path("source-intake/mts_residuals/P8_MTS_SYMBOL_MATCH_DECISION.csv")
VALIDATION_PATH = Path("source-intake/mts_residuals/P8_MTS_SYMBOL_MATCH_VALIDATION.csv")
ROUTE_UPDATE_PATH = Path("source-intake/mts_residuals/P8_MTS_SYMBOL_MATCH_ROUTE_UPDATE.csv")

SOURCE_REGISTER = [
    {
        "source_file": "511-minimal-parent-action-local-GR-fixed-point-ansatz.md",
        "role": "minimal action blocks and fixed-point gates to map symbols into",
    },
    {
        "source_file": "510-worldtube-source-measure-glue-or-Meff-residual-runner.md",
        "role": "dressed source charge and M_eff residual runner",
    },
    {
        "source_file": "01-motion-load-route-contract.md",
        "role": "early motion-load symbol list including Gamma_eff, K_hat, q_loc, and L_cg",
    },
    {
        "source_file": "02-motion-load-local-GR-reduction.md",
        "role": "early local-GR reduction route and residual symbol list",
    },
    {
        "source_file": "137-auxiliary-geometric-memory-action-owner.md",
        "role": "auxiliary memory action owner and smooth-memory branch",
    },
    {
        "source_file": "141-consolidated-locked-memory-branch-contract.md",
        "role": "locked memory branch status as empirical EFT closure with conditional theory mechanics",
    },
    {
        "source_file": "143-domain-selector-variational-action-attempt.md",
        "role": "domain selector action attempt and chi_D warnings",
    },
    {
        "source_file": "382-parent-local-action-minimal-contract.md",
        "role": "previous minimal parent local-action contract",
    },
    {
        "source_file": "384-parent-action-first-variation-obstruction-map.md",
        "role": "first-variation obstruction map",
    },
    {
        "source_file": "476-double-zero-memory-coupling-origin-or-coefficient-runner.md",
        "role": "double-zero memory coupling origin/coefficient branch",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_DOMAIN_SELECTOR_PARENT_ACTION_CLAUSE.csv",
        "role": "domain selector parent-action clause with chi_D and chi_D^2 memory activation",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_DOMAIN_SELECTOR_PARENT_ACTION_VARIATION_CHAIN.csv",
        "role": "variation chain for lambda_D, chi_D, metric, and Ward force",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_DOMAIN_SELECTOR_PARENT_ACTION_FORKS.csv",
        "role": "keep/kill forks for selector route",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_PARENT_LOCAL_ZERO_ACTION_CLAUSE.csv",
        "role": "local-zero clause using u, h, X, Qcoh, chi_D",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_MIN_PARENT_LOCAL_GR_ACTION_BLOCKS.csv",
        "role": "511 action blocks",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_MIN_PARENT_LOCAL_GR_FIXED_POINT_CONDITIONS.csv",
        "role": "511 fixed-point conditions",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_MIN_PARENT_LOCAL_GR_RESIDUAL_VECTOR.csv",
        "role": "511 local-GR residual vector",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_WORLDTUBE_MEFF_RESIDUAL_RUNNER.csv",
        "role": "M_eff runner to connect source charge and local readout",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_CONSTANT_KAPPA_TOPOLOGICAL_ZEROFORM_CLAUSE.csv",
        "role": "topological kappa clause",
    },
    {
        "source_file": "scripts/match_MTS_symbols_to_local_GR_action_blocks.py",
        "role": "this checkpoint generator",
    },
]

SYMBOL_MAP_ROWS = [
    {
        "symbol": "g_obs / g_readout",
        "aliases": "observed metric; coframe; local readout metric",
        "best_action_block": "A511_0_EH_core; A511_2_universal_matter; A511_6_metric_readout",
        "placement": "fundamental local metric/readout anchor",
        "required_first_variation": "delta_g S_parent = delta_g S_EH + silent/residual terms; same g_obs in matter and clocks",
        "current_status": "contract_anchor_not_full_MTS_derivation",
        "next_action": "derive same observed coframe/source/readout theorem and PPN expansion",
    },
    {
        "symbol": "kappa_eff / G_eff",
        "aliases": "kappa; G_eff; source normalization coupling",
        "best_action_block": "A511_1_kappa_topological",
        "placement": "global/topological coupling candidate",
        "required_first_variation": "delta_{A_3} S gives d kappa_eff=0; no matter/species/domain dependence",
        "current_status": "conditional_from_508_not_adopted_in_current_parent_action",
        "next_action": "either adopt/derive topological clause or retain G_eff drift residuals",
    },
    {
        "symbol": "A_3",
        "aliases": "topological three-form; kappa companion",
        "best_action_block": "A511_1_kappa_topological",
        "placement": "new parent topological auxiliary",
        "required_first_variation": "delta_{A_3} S_kappa_top -> d kappa_eff=0; delta_kappa gives topological companion constraint",
        "current_status": "candidate_not_original_MTS_symbol",
        "next_action": "decide whether A_3 is acceptable parent infrastructure or use residual branch",
    },
    {
        "symbol": "Gamma_eff",
        "aliases": "Gamma; Gamma_G; Gamma_kappa; effective connection/load rate",
        "best_action_block": "A511_3_extra_field_silence; A511_6_metric_readout",
        "placement": "dangerous unless derived as coupling/function/readout from parent fields",
        "required_first_variation": "show Gamma_eff = Gamma_eff(Phi,g,boundary) and partial_A Gamma_eff(Phi0)=0 or bounded",
        "current_status": "not_action_placed; residual_or_closure_symbol",
        "next_action": "build Gamma-Khat-q_loc first-variation ledger",
    },
    {
        "symbol": "K_hat^{mu nu}",
        "aliases": "Khat; K_hat; compact/boundary tensor",
        "best_action_block": "A511_5_boundary_reference; A511_3_extra_field_silence",
        "placement": "boundary/symplectic or extra-sector tensor candidate",
        "required_first_variation": "derive K_hat from theta/Q/boundary term or field equation; prove divergence contribution is exact/silent",
        "current_status": "not_action_placed; residual_or_closure_symbol",
        "next_action": "pair with Gamma_eff in q_loc first-variation attempt",
    },
    {
        "symbol": "q_loc^nu",
        "aliases": "local source-force residual; local vacuum leakage vector",
        "best_action_block": "not a field; Ward/Noether residual from A511_3/A511_5/A511_6",
        "placement": "derived residual, not fundamental",
        "required_first_variation": "q_loc^nu = P_loc(nabla^nu Gamma_eff - nabla_mu K_hat^{mu nu}) must equal on-shell Ward residual and vanish from Euler equations",
        "current_status": "not_derived_zero; plateau_axiom_forbidden",
        "next_action": "derive or demote q_loc to explicit PPN/local-bound residual",
    },
    {
        "symbol": "P_loc",
        "aliases": "local projector; selector projector",
        "best_action_block": "A511_4_domain_projector_selector; A511_6_metric_readout",
        "placement": "projector/readout operator candidate",
        "required_first_variation": "derive P_loc from parent algebra or local representative selector; no data-chosen projector",
        "current_status": "open",
        "next_action": "map P_loc to Pi_M/P_coh/domain selector or keep residual",
    },
    {
        "symbol": "Pi_M",
        "aliases": "mass projector; Q_M readout projector",
        "best_action_block": "A511_6_metric_readout; 510 worldtube charge",
        "placement": "Noether/Hamiltonian mass-projector candidate",
        "required_first_variation": "Pi_M(Phi0)=Pi_EH and partial_A Pi_M(Phi0)=0",
        "current_status": "not_parent_derived",
        "next_action": "derive from covariant phase-space charge or keep calibration residual",
    },
    {
        "symbol": "chi_D",
        "aliases": "domain selector; coherent-domain scalar selector",
        "best_action_block": "A511_4_domain_projector_selector",
        "placement": "auxiliary scalar selector if algebraic; dangerous if dynamical",
        "required_first_variation": "delta_lambda gives chi_D=Sigma_D; delta_chi and chi_D^2 coupling give lambda_D=0 on local branch",
        "current_status": "conditional_action_clause_exists_not_parent_derived",
        "next_action": "derive Sigma_local=0/trivial class or fill domain residuals",
    },
    {
        "symbol": "Qcoh / Q_coh",
        "aliases": "coherent trace-load tensor; Qcoh_mu_nu; Q_D",
        "best_action_block": "A511_4_domain_projector_selector",
        "placement": "parent load/projector variable candidate",
        "required_first_variation": "derive Qcoh from parent load/Noether/strain variable; local stationary compact branch gives Qcoh_D=0",
        "current_status": "open",
        "next_action": "prove parent ownership and local zero or demote to closure variable",
    },
    {
        "symbol": "memory / B_mem / U_mem / I_M",
        "aliases": "locked memory; memory exposure; memory amplitude",
        "best_action_block": "A511_3_extra_field_silence; A511_4_domain_projector_selector",
        "placement": "empirical EFT closure unless action-owned auxiliary sector is matched",
        "required_first_variation": "memory activation must be chi_D^2 or double-zero locally and smooth/controlled cosmologically",
        "current_status": "empirically_interesting_conditional_EFT_not_parent_derived",
        "next_action": "keep testable but do not use as local-GR proof until double-zero origin is derived",
    },
    {
        "symbol": "L_cg / ell_tr",
        "aliases": "coarse-graining scale; transition length; activation scale",
        "best_action_block": "FP511_8 local-cosmology transition control",
        "placement": "derived scale from operator spectrum/source/domain, not independent field",
        "required_first_variation": "derive from Hessian/mass gap/domain spectrum/source compactness; no arena switch",
        "current_status": "open",
        "next_action": "derive ell_tr/L_cg or retain branch-switch residual",
    },
    {
        "symbol": "u^mu / h_mu_nu / X",
        "aliases": "flow vector; spatial projector; expansion/load scalar",
        "best_action_block": "A511_4_domain_projector_selector",
        "placement": "auxiliary local-zero kinematic variables",
        "required_first_variation": "constraints fix u^2=-1 and X=nabla.u; local stationary Killing branch forces X_D=0",
        "current_status": "candidate_clause_not_parent_derived",
        "next_action": "show no preferred-frame/vector stress or retain alpha_i/xi residuals",
    },
    {
        "symbol": "M_eff / M_source / Q_M",
        "aliases": "measured GM mass factor; dressed source charge; parent mass charge",
        "best_action_block": "510 worldtube source-measure glue; A511_6 metric readout",
        "placement": "derived dressed charge, not bare matter mass",
        "required_first_variation": "Hamiltonian/Noether charge equals worldtube source measure and metric 1/r coefficient",
        "current_status": "conditional_theorem_route_not_MTS_derived",
        "next_action": "derive Pi_M current closure or use MR510 residual runner",
    },
]

FIRST_VARIATION_GATE_ROWS = [
    {
        "gate_id": "FV512_0_metric",
        "symbols": "g_obs, g_readout",
        "must_show": "metric variation gives EH operator plus explicit residuals; same metric couples to matter",
        "current_result": "open",
        "blocks": "PPN/local_GR",
    },
    {
        "gate_id": "FV512_1_kappa",
        "symbols": "kappa_eff, A_3",
        "must_show": "topological variation gives d kappa_eff=0 and no source/domain/species labels",
        "current_result": "conditional_pass_if_508_clause_adopted",
        "blocks": "Gdot/source_normalization",
    },
    {
        "gate_id": "FV512_2_Gamma_Khat_q",
        "symbols": "Gamma_eff, K_hat, q_loc",
        "must_show": "there is an action term whose Ward residual is P_loc(nabla Gamma_eff - div K_hat), and on-shell it vanishes locally",
        "current_result": "fail_for_current_claim",
        "blocks": "local_GR_and_PPN",
    },
    {
        "gate_id": "FV512_3_domain_selector",
        "symbols": "chi_D, Qcoh, u, h, X, P_loc",
        "must_show": "auxiliary variations force local zero without kinetic/vector/domain-wall stress",
        "current_result": "conditional_clause_not_parent_derived",
        "blocks": "alpha_i_xi_R11",
    },
    {
        "gate_id": "FV512_4_memory",
        "symbols": "memory, B_mem, U_mem, I_M",
        "must_show": "memory stress is double-zero locally and action-owned cosmologically",
        "current_result": "empirical_EFT_closure_conditional",
        "blocks": "local_silence_and_unification",
    },
    {
        "gate_id": "FV512_5_mass_projector",
        "symbols": "Pi_M, Q_M, M_eff, M_source",
        "must_show": "Pi_M is the EH/Hamiltonian mass projector at the local fixed point and first variation vanishes",
        "current_result": "fail_for_current_claim",
        "blocks": "Newton_source_normalization",
    },
    {
        "gate_id": "FV512_6_transition_scale",
        "symbols": "L_cg, ell_tr",
        "must_show": "transition/activation scale follows from operator spectrum, mass gap, topology, or source compactness",
        "current_result": "open",
        "blocks": "unified_field_theory_claim",
    },
]

KEEP_KILL_RULE_ROWS = [
    {
        "rule_id": "KK512_0_kappa",
        "keep_route": "kappa as topological/global integration constant",
        "kill_or_demote_route": "kappa as local scalar/source/domain/radius calibration",
        "reason": "local scalar kappa reintroduces Gdot, WEP, and source-normalization hair",
    },
    {
        "rule_id": "KK512_1_q_loc",
        "keep_route": "q_loc as on-shell Ward/Noether residual that the action drives to zero",
        "kill_or_demote_route": "q_loc as an inserted local force term or plateau axiom",
        "reason": "a force residual must be varied from the parent action or carried as PPN/local-bound residual",
    },
    {
        "rule_id": "KK512_2_Gamma_Khat",
        "keep_route": "Gamma_eff and K_hat derived from parent fields, boundary terms, or symplectic current with double-zero first variation",
        "kill_or_demote_route": "Gamma_eff/K_hat chosen after readout to cancel local residuals",
        "reason": "post-readout cancellation is not a field-theory derivation",
    },
    {
        "rule_id": "KK512_3_chi_D",
        "keep_route": "auxiliary algebraic chi_D with chi_D^2 memory activation and local zero",
        "kill_or_demote_route": "linear chi_D coupling or kinetic/domain-wall selector",
        "reason": "linear/dynamical selector leaves stress and preferred-frame residuals",
    },
    {
        "rule_id": "KK512_4_memory",
        "keep_route": "memory as action-owned auxiliary/geometric sector with smooth cosmological stress and local double zero",
        "kill_or_demote_route": "memory as local hidden dark sector or fitted amplitude used to prove GR",
        "reason": "cosmology fit can stay promising, but it cannot pay local-GR debts",
    },
    {
        "rule_id": "KK512_5_mass",
        "keep_route": "M_source as dressed Hamiltonian/Noether charge",
        "kill_or_demote_route": "bare rest mass directly equated to measured gravitational mass",
        "reason": "even GR uses a dressed gravitational charge in the worldtube/surface-charge story",
    },
    {
        "rule_id": "KK512_6_scale",
        "keep_route": "ell_tr/L_cg derived from mass gap, spectrum, topology, or source compactness",
        "kill_or_demote_route": "local/cosmology/galaxy switch chosen per arena",
        "reason": "a unification claim cannot use an unowned branch switch",
    },
]

DECISION_ROWS = [
    {
        "decision_id": "D512_0",
        "decision": "symbol_map_written",
        "meaning": "each major MTS local-GR symbol now has an action placement, first-variation debt, and demotion rule",
        "claim_status": "private_workbench_useful",
    },
    {
        "decision_id": "D512_1",
        "decision": "no_symbol_fully_promotes_local_GR",
        "meaning": "some routes are viable conditionally, but no symbol currently passes action placement plus first variation plus PPN readout",
        "claim_status": "local_GR_claim_false",
    },
    {
        "decision_id": "D512_2",
        "decision": "Gamma_Khat_q_loc_is_hard_next_target",
        "meaning": "the central local vacuum residual must be varied from an action or demoted to a bounded residual",
        "claim_status": NEXT_TARGET,
    },
    {
        "decision_id": "D512_3",
        "decision": "promising_partials_preserved",
        "meaning": "topological kappa, auxiliary chi_D double-zero, dressed source charge, and memory EFT branch remain useful but conditional",
        "claim_status": "conditional_routes_not_public_claims",
    },
]

ROUTE_UPDATE_ROWS = [
    {
        "route_id": "RU512_0",
        "status": "MTS_symbols_mapped_to_action_blocks",
        "update": "the local-GR route is now an action-placement problem rather than a loose residual story",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "RU512_1",
        "status": "q_loc_reclassified",
        "update": "q_loc is a Ward/Noether residual to be derived or bounded, not a fundamental field or axiom",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "RU512_2",
        "status": "no_GitHub_no_promotion",
        "update": "all outputs remain private post-checkpoint work; no local-GR/Newton promotion is made",
        "next_target": NEXT_TARGET,
    },
]


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def source_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for item in SOURCE_REGISTER:
        path = ROOT / item["source_file"]
        rows.append(
            {
                "source_file": item["source_file"],
                "role": item["role"],
                "exists": path.exists(),
            }
        )
    return rows


def validation_rows(sources: list[dict[str, Any]]) -> list[dict[str, Any]]:
    missing_sources = [row["source_file"] for row in sources if row["exists"] != True]
    fully_promoted = [row for row in SYMBOL_MAP_ROWS if row["current_status"] == "promoted"]
    return [
        {
            "check_id": "V512_0_source_paths_exist",
            "result": "pass" if not missing_sources else "fail",
            "detail": f"missing={len(missing_sources)}",
        },
        {
            "check_id": "V512_1_major_symbols_mapped",
            "result": "pass",
            "detail": f"symbols={len(SYMBOL_MAP_ROWS)}",
        },
        {
            "check_id": "V512_2_first_variation_gates_present",
            "result": "pass",
            "detail": f"first_variation_gates={len(FIRST_VARIATION_GATE_ROWS)}",
        },
        {
            "check_id": "V512_3_keep_kill_rules_present",
            "result": "pass",
            "detail": f"keep_kill_rules={len(KEEP_KILL_RULE_ROWS)}",
        },
        {
            "check_id": "V512_4_no_overclaim",
            "result": "pass" if not fully_promoted else "fail",
            "detail": f"fully_promoted_symbols={len(fully_promoted)}; local_GR_claim_allowed=false",
        },
    ]


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    full_path = ROOT / path
    full_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys())
    with full_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_run_csv(results_dir: Path, filename: str, rows: list[dict[str, Any]]) -> None:
    fieldnames = list(rows[0].keys())
    with (results_dir / filename).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def markdown_table(rows: list[dict[str, Any]]) -> str:
    headers = list(rows[0].keys())
    output = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        values = []
        for header in headers:
            value = str(row.get(header, "")).replace("\n", " ").replace("|", "\\|")
            values.append(value)
        output.append("| " + " | ".join(values) + " |")
    return "\n".join(output)


def build_doc(
    timestamp: str,
    generated_at_utc: str,
    run_dir: Path,
    sources: list[dict[str, Any]],
    validations: list[dict[str, Any]],
) -> str:
    return f"""# 512 - Match MTS Symbols to Local-GR Action Blocks

Generated: {generated_at_utc}  
Run: `{rel(run_dir)}`  
Status: `{STATUS}`  
Claim ceiling: `{CLAIM_CEILING}`

## 1. Verdict

This checkpoint keeps the 511 action route grounded in actual MTS language.

The blunt result:

```text
No major MTS symbol is fully promoted to derived local GR yet.
Several symbols have credible conditional placements.
The hardest immediate obstruction is Gamma_eff / K_hat / q_loc.
```

The useful clarification is that `q_loc^nu` should not be treated as a new field. It is a residual:

```text
q_loc^nu = P_loc(nabla^nu Gamma_eff - nabla_mu K_hat^{{mu nu}})
```

That object either comes from the parent action's Ward/Noether variation and vanishes on shell in compact local vacuum, or it is an explicit local PPN/bound residual. There is no respectable middle option.

## 2. Symbol Map

{markdown_table(SYMBOL_MAP_ROWS)}

## 3. First-Variation Gates

{markdown_table(FIRST_VARIATION_GATE_ROWS)}

## 4. Keep/Kill Rules

{markdown_table(KEEP_KILL_RULE_ROWS)}

## 5. Decision

{markdown_table(DECISION_ROWS)}

## 6. Source Register

{markdown_table(sources)}

## 7. Validation

{markdown_table(validations)}

## 8. Route Update

{markdown_table(ROUTE_UPDATE_ROWS)}

## 9. Claim Ceiling

Allowed:

```text
MTS now has a symbol-by-symbol parent-action placement map.
MTS has identified which symbols are conditional, residual, or unplaced.
MTS has a clear next first-variation target: Gamma_eff / K_hat / q_loc.
```

Forbidden:

```text
MTS has derived local GR.
MTS has derived q_loc^nu -> 0.
MTS has proved Gamma_eff or K_hat are parent-action objects.
MTS has promoted memory/cosmology success into local-GR proof.
```

## 10. Next Target

`{NEXT_TARGET}`

Try to write an action or variational identity whose Ward residual is exactly `P_loc(nabla Gamma_eff - div K_hat)`. If that cannot be done, demote the local transition route to an explicit closure/residual branch.
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timestamp", default=datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S"))
    args = parser.parse_args()

    generated_at_utc = datetime.now(timezone.utc).isoformat()
    run_dir = ROOT / "runs" / f"{args.timestamp}-match-MTS-symbols-to-local-GR-action-blocks"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    sources = source_rows()
    validations = validation_rows(sources)

    csv_outputs: list[tuple[Path, list[dict[str, Any]]]] = [
        (SOURCE_REGISTER_PATH, sources),
        (SYMBOL_MAP_PATH, SYMBOL_MAP_ROWS),
        (FIRST_VARIATION_GATES_PATH, FIRST_VARIATION_GATE_ROWS),
        (KEEP_KILL_RULES_PATH, KEEP_KILL_RULE_ROWS),
        (DECISION_PATH, DECISION_ROWS),
        (VALIDATION_PATH, validations),
        (ROUTE_UPDATE_PATH, ROUTE_UPDATE_ROWS),
    ]

    for path, rows in csv_outputs:
        write_csv(path, rows)
        write_run_csv(results_dir, path.name, rows)

    doc = build_doc(args.timestamp, generated_at_utc, run_dir, sources, validations)
    (ROOT / DOC_PATH).write_text(doc, encoding="utf-8")

    missing_sources = [row["source_file"] for row in sources if row["exists"] != True]
    failed_validations = [row for row in validations if row["result"] == "fail"]
    conditional_symbols = [
        row for row in SYMBOL_MAP_ROWS if "conditional" in row["current_status"] or "candidate" in row["current_status"]
    ]
    residual_or_unplaced_symbols = [
        row for row in SYMBOL_MAP_ROWS if "not_action_placed" in row["current_status"] or "open" == row["current_status"]
    ]
    status = {
        "timestamp": args.timestamp,
        "generated_at_utc": generated_at_utc,
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "checkpoint_doc": str(DOC_PATH),
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "source_register": str(ROOT / SOURCE_REGISTER_PATH),
        "symbol_map": str(ROOT / SYMBOL_MAP_PATH),
        "first_variation_gates": str(ROOT / FIRST_VARIATION_GATES_PATH),
        "keep_kill_rules": str(ROOT / KEEP_KILL_RULES_PATH),
        "decision": str(ROOT / DECISION_PATH),
        "validation": str(ROOT / VALIDATION_PATH),
        "route_update": str(ROOT / ROUTE_UPDATE_PATH),
        "source_rows": len(sources),
        "source_paths_missing": len(missing_sources),
        "missing_sources": missing_sources,
        "failed_validation_rows": len(failed_validations),
        "symbols_mapped": len(SYMBOL_MAP_ROWS),
        "fully_promoted_symbols": 0,
        "conditional_viable_symbols": len(conditional_symbols),
        "residual_or_unplaced_symbols": len(residual_or_unplaced_symbols),
        "Gamma_Khat_qloc_hard_next_target": True,
        "q_loc_reclassified_as_Ward_residual": True,
        "current_MTS_matched_to_action": False,
        "source_normalized_Newton_promoted": False,
        "PPN_promoted": False,
        "local_GR_claim_allowed": False,
        "next_target": NEXT_TARGET,
    }
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (run_dir / "DONE.txt").write_text(
        f"{STATUS}\nnext={NEXT_TARGET}\nlocal_GR_claim_allowed=false\n",
        encoding="utf-8",
    )
    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
