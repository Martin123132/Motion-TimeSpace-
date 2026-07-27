from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

STATUS = "Gamma_eff_scalar_density_owner_candidate_written_response_doublet_best_route_not_current_MTS_derived_q_loc_bound_runner_spec_written"
CLAIM_CEILING = "candidate_owner_or_bound_runner_spec_only_no_q_loc_zero_local_GR_Newton_or_PPN_promotion"
NEXT_TARGET = "517-response-doublet-action-variation-ledger-or-run-q_loc-bound.md"

DOC_PATH = Path("516-Gamma-eff-scalar-density-owner-or-q_loc-bound-runner.md")
SOURCE_REGISTER_PATH = Path("source-intake/mts_residuals/P8_GAMMA_OWNER_OR_QLOC_BOUND_SOURCE_REGISTER.csv")
OWNER_CANDIDATE_PATH = Path("source-intake/mts_residuals/P8_GAMMA_OWNER_CANDIDATE_ACTION.csv")
RESPONSE_DOUBLET_CONTRACT_PATH = Path("source-intake/mts_residuals/P8_RESPONSE_DOUBLET_ACTION_CONTRACT.csv")
QLOC_BOUND_SPEC_PATH = Path("source-intake/mts_residuals/P8_QLOC_BOUND_RUNNER_SPEC.csv")
FORK_TESTS_PATH = Path("source-intake/mts_residuals/P8_GAMMA_OWNER_OR_QLOC_BOUND_FORK_TESTS.csv")
DECISION_PATH = Path("source-intake/mts_residuals/P8_GAMMA_OWNER_OR_QLOC_BOUND_DECISION.csv")
VALIDATION_PATH = Path("source-intake/mts_residuals/P8_GAMMA_OWNER_OR_QLOC_BOUND_VALIDATION.csv")
ROUTE_UPDATE_PATH = Path("source-intake/mts_residuals/P8_GAMMA_OWNER_OR_QLOC_BOUND_ROUTE_UPDATE.csv")

SOURCE_REGISTER = [
    {
        "source_file": "515-match-Gamma-eff-Khat-to-metric-response-action.md",
        "role": "current corpus match audit; no Gamma/Khat metric-response match found",
    },
    {
        "source_file": "514-construct-GK-stress-action-or-residual-bound.md",
        "role": "S_GK metric-response candidate and residual-bound branch",
    },
    {
        "source_file": "513-Gamma-Khat-q_loc-first-variation-or-demotion.md",
        "role": "q_loc stress-divergence identity",
    },
    {
        "source_file": "492-silence-auxiliary-parent-action-construction-or-closure.md",
        "role": "lock/Z2 triangle and odd residual parentization target",
    },
    {
        "source_file": "493-odd-residual-parentization-or-closure-fill.md",
        "role": "exchange-doublet parentization contract",
    },
    {
        "source_file": "494-exchange-doublet-component-map-or-coefficient-branch.md",
        "role": "component map; Y2/Y3 conditional and Y5/Y6 hard blockers",
    },
    {
        "source_file": "219-compact-shell-q_loc-source-projection-attempt.md",
        "role": "compact-shell q_loc leakage budget",
    },
    {
        "source_file": "220-Jrel-local-trivial-representative-or-closure-bound.md",
        "role": "J_rel exactness route and worst compact leakage bound",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_GK_METRIC_RESPONSE_REPAIR_OPTIONS.csv",
        "role": "515 repair options including auxiliary positive field and response doublet",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_YLOC_EULER_SYSTEM.csv",
        "role": "Yloc component list for response doublet field content",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_GK_METRIC_RESPONSE_MATCH_AUDIT.csv",
        "role": "515 failure rows to repair",
    },
    {
        "source_file": "scripts/Gamma_eff_scalar_density_owner_or_q_loc_bound_runner.py",
        "role": "this checkpoint generator",
    },
]

OWNER_CANDIDATE_ROWS = [
    {
        "candidate_id": "GO516_A_response_doublet_quadratic_density",
        "action_density": "Gamma_eff = Gamma0 + 1/2 M_AB(g,R_even,D,...) Z^A Z^B + O(Z^4)",
        "field_content": "exchange doublets R_+^A,R_-^A; Z^A=(R_+^A-R_-^A)/2; R_even^A=(R_+^A+R_-^A)/2",
        "Khat_identity": "K_hat^{mu nu} := 2/sqrt(-g) delta[sqrt(-g) Gamma_eff]/delta g_{mu nu} minus volume convention",
        "why_it_could_work": "Gamma_eff is even in exchange-odd residuals, so T_GK and first variation vanish at Z=0 after Gamma0 subtraction",
        "current_status": "best_candidate_not_current_MTS_derived",
    },
    {
        "candidate_id": "GO516_B_positive_auxiliary_energy_density",
        "action_density": "Gamma_eff = V(Phi) + 1/2 G_AB(Phi) nabla Phi^A nabla Phi^B",
        "field_content": "positive auxiliary local-silence fields Phi^A",
        "Khat_identity": "K_hat is kinetic/elastic metric response of the auxiliary energy density",
        "why_it_could_work": "positive operator can force Phi=Phi0 under source-free/no-boundary conditions",
        "current_status": "candidate_but_source_current_zero_not_derived",
    },
    {
        "candidate_id": "GO516_C_topological_boundary_density",
        "action_density": "Gamma_eff from normalized boundary/topological density Q_B/Q_* or exact form",
        "field_content": "boundary/topological class variables",
        "Khat_identity": "K_hat is boundary/improvement stress response",
        "why_it_could_work": "bulk q_loc can vanish if the stress is exact/topological",
        "current_status": "candidate_but_charge_unit_and_boundary_flux_open",
    },
    {
        "candidate_id": "GO516_D_residual_bound_runner",
        "action_density": "none accepted",
        "field_content": "q_loc treated as explicit retained local residual",
        "Khat_identity": "not required",
        "why_it_could_work": "keeps route testable if derivation fails",
        "current_status": "fallback_required",
    },
]

RESPONSE_DOUBLET_CONTRACT_ROWS = [
    {
        "contract_id": "RD516_0_doublet_variables",
        "requirement": "Every physical local leakage component has parent exchange doublets R_+^A,R_-^A.",
        "test": "component map covers Y0-Y6, including source normalization and extra stress",
        "current_status": "partial_from_494_Y2_Y3_only_conditional",
    },
    {
        "contract_id": "RD516_1_even_scalar_density",
        "requirement": "Gamma_eff is an even scalar density in Z with no linear term.",
        "test": "partial_A Gamma_eff|Z=0 = 0 and Gamma0 is constant/background-subtracted",
        "current_status": "candidate_written_not_matched",
    },
    {
        "contract_id": "RD516_2_metric_response",
        "requirement": "K_hat is exactly the metric response of sqrt(-g) Gamma_eff.",
        "test": "compute delta_g Gamma_eff and compare tensor pieces to existing K_hat definitions",
        "current_status": "not_checked_current_MTS",
    },
    {
        "contract_id": "RD516_3_positive_operator",
        "requirement": "The Z sector has positive Hessian/operator after gauge/constraint removal.",
        "test": "M_AB positive and derivative operator self-adjoint positive on compact local collars",
        "current_status": "formal_candidate_only",
    },
    {
        "contract_id": "RD516_4_zero_odd_source",
        "requirement": "Matter, boundary, and source-normalization channels carry no exchange-odd local source charge.",
        "test": "J_Z=0 and B_Z=0; especially Y5 source-normalization and Y6 stress rows",
        "current_status": "not_derived_hard_block",
    },
    {
        "contract_id": "RD516_5_PPN_lock",
        "requirement": "Z^A equals the physical q_loc/PPN residual vector through the local gate, not a bookkeeping shadow.",
        "test": "Z^A=Y_loc^A through beta/gamma/alpha_i/xi/Gdot/R11 order",
        "current_status": "not_derived",
    },
    {
        "contract_id": "RD516_6_boundary_no_flux",
        "requirement": "integrations by parts and boundary metric response carry no local force/mass flux.",
        "test": "boundary term zero/fixed-reference theorem or q_loc bound row",
        "current_status": "open",
    },
]

QLOC_BOUND_SPEC_ROWS = [
    {
        "bound_id": "QB516_0_compact_shell_budget",
        "if_owner_fails": "use existing compact-shell leakage budget",
        "quantity": "max |P_loc d_rel J_rel| or equivalent q_loc leakage",
        "current_bound": "7.432631961576971e-06",
        "source": "220-Jrel-local-trivial-representative-or-closure-bound.md",
        "needed_before_claim": "map this dimensionless proxy into PPN/source-normalization units",
    },
    {
        "bound_id": "QB516_1_alpha3_pressure",
        "if_owner_fails": "project q_loc force into preferred-frame/momentum-flux rows",
        "quantity": "alpha3-equivalent channel",
        "current_bound": "4e-20 row lock where alpha3 applies",
        "source": "local residual templates and alpha3 ledgers",
        "needed_before_claim": "coefficient normalization from q_loc to alpha3",
    },
    {
        "bound_id": "QB516_2_Gdot_GMdot",
        "if_owner_fails": "project time component into measured-GM drift",
        "quantity": "dln_mu_obs_dt or dln_Meff_dt",
        "current_bound": "use source-normalization/Gdot ledgers, not currently filled here",
        "source": "P8_CONSTANT_GM_LOCAL_RESIDUAL_RUNNER_INPUT.csv",
        "needed_before_claim": "time component and units",
    },
    {
        "bound_id": "QB516_3_PPN_metric_tail",
        "if_owner_fails": "project spatial/tensor components into beta/gamma/xi/alpha_i residual vector",
        "quantity": "Delta_PPN from q_loc",
        "current_bound": "requires official PPN row mapping",
        "source": "P8 local residual vector rows",
        "needed_before_claim": "weak-field metric solution sourced by q_loc",
    },
    {
        "bound_id": "QB516_4_R11_operator",
        "if_owner_fails": "treat Gamma/Khat sector as retained non-EH operator/source-normalization row",
        "quantity": "c_GK_operator_vector",
        "current_bound": "symbolic until coefficient vector is filled",
        "source": "R11/non-EH operator ledgers",
        "needed_before_claim": "operator family, units, normalization, and bound comparison",
    },
]

FORK_TEST_ROWS = [
    {
        "gate_id": "F516_0_owner_candidate_written",
        "gate": "there is a coherent Gamma_eff scalar-density owner candidate",
        "result": "pass_conditional",
        "evidence": "GO516_A",
    },
    {
        "gate_id": "F516_1_owner_derived_for_current_MTS",
        "gate": "current MTS derives the response-doublet owner and metric response",
        "result": "fail_for_current_claim",
        "evidence": "RD516_0-RD516_6 remain partial/open",
    },
    {
        "gate_id": "F516_2_double_zero",
        "gate": "F_1=0 follows from even quadratic Gamma_eff",
        "result": "pass_conditional",
        "evidence": "if Gamma_eff=Gamma0+1/2 M_AB Z^A Z^B and Z=0",
    },
    {
        "gate_id": "F516_3_hard_rows",
        "gate": "Y5 source-normalization and Y6 extra stress are solved",
        "result": "fail_for_current_claim",
        "evidence": "494 marks Y5/Y6 as hard blockers",
    },
    {
        "gate_id": "F516_4_bound_runner_spec",
        "gate": "fallback q_loc residual-bound runner is specified",
        "result": "pass",
        "evidence": f"bound_rows={len(QLOC_BOUND_SPEC_ROWS)}",
    },
    {
        "gate_id": "F516_5_local_GR_claim",
        "gate": "local GR/Newton/PPN is promoted",
        "result": "fail_blocked",
        "evidence": "owner is not current-MTS-derived and bound runner is not scored",
    },
]

DECISION_ROWS = [
    {
        "decision_id": "D516_0",
        "decision": "response_doublet_owner_is_best_theory_route",
        "meaning": "the cleanest Gamma_eff owner is a quadratic scalar density in exchange-odd parent residuals",
        "claim_status": "candidate_not_proof",
    },
    {
        "decision_id": "D516_1",
        "decision": "Y5_Y6_remain_the_hard_barrier",
        "meaning": "source normalization and extra stress cannot be killed by oddness without separate theorems",
        "claim_status": "local_GR_blocked",
    },
    {
        "decision_id": "D516_2",
        "decision": "bound_runner_must_exist",
        "meaning": "if the response-doublet owner fails, q_loc must be scored as an explicit residual with compact-shell/PPN normalization",
        "claim_status": "fallback_spec_written",
    },
    {
        "decision_id": "D516_3",
        "decision": "next_step_variation_or_bound",
        "meaning": "either compute the variation ledger for the response-doublet action or implement the q_loc bound runner",
        "claim_status": NEXT_TARGET,
    },
]

ROUTE_UPDATE_ROWS = [
    {
        "route_id": "RU516_0",
        "status": "Gamma_owner_candidate_written",
        "update": "Gamma_eff can be made a scalar density via quadratic exchange-odd response doublets if the component map is real",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "RU516_1",
        "status": "local_GR_still_blocked",
        "update": "Y5 source normalization, Y6 extra stress, metric response, and PPN lock are not derived",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "RU516_2",
        "status": "bound_runner_ready_as_fallback",
        "update": "compact-shell leakage budget and PPN/R11 mapping rows define the residual branch if derivation fails",
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
    return [
        {
            "check_id": "V516_0_source_paths_exist",
            "result": "pass" if not missing_sources else "fail",
            "detail": f"missing={len(missing_sources)}",
        },
        {
            "check_id": "V516_1_owner_candidate_present",
            "result": "pass",
            "detail": f"owner_candidates={len(OWNER_CANDIDATE_ROWS)}",
        },
        {
            "check_id": "V516_2_response_contract_present",
            "result": "pass",
            "detail": f"contract_rows={len(RESPONSE_DOUBLET_CONTRACT_ROWS)}",
        },
        {
            "check_id": "V516_3_bound_runner_spec_present",
            "result": "pass",
            "detail": f"bound_rows={len(QLOC_BOUND_SPEC_ROWS)}",
        },
        {
            "check_id": "V516_4_no_overclaim",
            "result": "pass",
            "detail": "Gamma_eff_owner_derived_for_MTS=false; q_loc_bound_runner_scored=false; local_GR_claim_allowed=false",
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
    return f"""# 516 - Gamma_eff Scalar-Density Owner or q_loc Bound Runner

Generated: {generated_at_utc}  
Run: `{rel(run_dir)}`  
Status: `{STATUS}`  
Claim ceiling: `{CLAIM_CEILING}`

## 1. Verdict

The current corpus did not already contain the `Gamma_eff/K_hat` metric-response match. So this checkpoint builds the fork:

```text
Route A: construct a real Gamma_eff scalar-density owner.
Route B: demote q_loc to an explicit residual-bound runner.
```

The best theory route is now:

```text
R_+^A, R_-^A exchange doublets
Z^A = (R_+^A - R_-^A)/2
Gamma_eff = Gamma0 + 1/2 M_AB Z^A Z^B + O(Z^4)
K_hat = metric response of Gamma_eff
```

This is attractive because the double-zero is automatic at `Z=0`:

```text
partial_A Gamma_eff|Z=0 = 0.
```

But it is still not a current MTS derivation. The doublet component map, source-normalization row Y5, extra-stress row Y6, metric response, and PPN lock remain open.

## 2. Owner Candidates

{markdown_table(OWNER_CANDIDATE_ROWS)}

## 3. Response-Doublet Contract

{markdown_table(RESPONSE_DOUBLET_CONTRACT_ROWS)}

## 4. q_loc Bound Runner Spec

{markdown_table(QLOC_BOUND_SPEC_ROWS)}

## 5. Fork Tests

{markdown_table(FORK_TEST_ROWS)}

## 6. Decision

{markdown_table(DECISION_ROWS)}

## 7. Source Register

{markdown_table(sources)}

## 8. Validation

{markdown_table(validations)}

## 9. Route Update

{markdown_table(ROUTE_UPDATE_ROWS)}

## 10. Claim Ceiling

Allowed:

```text
MTS has a coherent candidate Gamma_eff scalar-density owner based on exchange-odd response doublets.
MTS has a fallback q_loc residual-bound runner specification.
```

Forbidden:

```text
MTS has derived the Gamma_eff owner for current MTS.
MTS has derived K_hat as the metric response.
MTS has derived q_loc^nu -> 0.
MTS has derived local GR, Newtonian recovery, or PPN silence.
```

## 11. Next Target

`{NEXT_TARGET}`

Either write the variation ledger for the response-doublet action and test whether Y5/Y6 can be handled, or implement the q_loc residual-bound runner from the compact-shell/PPN rows.
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timestamp", default=datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S"))
    args = parser.parse_args()

    generated_at_utc = datetime.now(timezone.utc).isoformat()
    run_dir = ROOT / "runs" / f"{args.timestamp}-Gamma-eff-scalar-density-owner-or-q_loc-bound-runner"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    sources = source_rows()
    validations = validation_rows(sources)

    csv_outputs: list[tuple[Path, list[dict[str, Any]]]] = [
        (SOURCE_REGISTER_PATH, sources),
        (OWNER_CANDIDATE_PATH, OWNER_CANDIDATE_ROWS),
        (RESPONSE_DOUBLET_CONTRACT_PATH, RESPONSE_DOUBLET_CONTRACT_ROWS),
        (QLOC_BOUND_SPEC_PATH, QLOC_BOUND_SPEC_ROWS),
        (FORK_TESTS_PATH, FORK_TEST_ROWS),
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
    status = {
        "timestamp": args.timestamp,
        "generated_at_utc": generated_at_utc,
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "checkpoint_doc": str(DOC_PATH),
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "source_register": str(ROOT / SOURCE_REGISTER_PATH),
        "owner_candidate": str(ROOT / OWNER_CANDIDATE_PATH),
        "response_doublet_contract": str(ROOT / RESPONSE_DOUBLET_CONTRACT_PATH),
        "q_loc_bound_spec": str(ROOT / QLOC_BOUND_SPEC_PATH),
        "fork_tests": str(ROOT / FORK_TESTS_PATH),
        "decision": str(ROOT / DECISION_PATH),
        "validation": str(ROOT / VALIDATION_PATH),
        "route_update": str(ROOT / ROUTE_UPDATE_PATH),
        "source_rows": len(sources),
        "source_paths_missing": len(missing_sources),
        "missing_sources": missing_sources,
        "failed_validation_rows": len(failed_validations),
        "Gamma_eff_owner_candidate_written": True,
        "best_owner_response_doublet_quadratic_density": True,
        "Gamma_eff_owner_derived_for_MTS": False,
        "K_hat_metric_response_derived": False,
        "Y5_source_normalization_solved": False,
        "Y6_extra_stress_solved": False,
        "q_loc_bound_runner_spec_written": True,
        "q_loc_bound_runner_scored": False,
        "q_loc_zero_derived_for_MTS": False,
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
