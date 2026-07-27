from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

STATUS = "parent_worldtube_glue_theorem_attempt_built_conditional_not_yet_derived"
CLAIM_CEILING = "conditional_Noether_mass_charge_route_no_local_GR_or_Newton_promotion_yet"
NEXT_TARGET = "505-parent-Noether-mass-charge-closure-theorem-or-closure-demotion.md"

DOC_PATH = Path("504-parent-Hilbert-worldtube-glue-or-external-radial-input-plan.md")
SOURCE_REGISTER_PATH = Path("source-intake/mts_residuals/P8_PARENT_WORLDTUBE_GLUE_SOURCE_REGISTER.csv")
THEOREM_CLAUSES_PATH = Path("source-intake/mts_residuals/P8_PARENT_WORLDTUBE_GLUE_THEOREM_CLAUSES.csv")
NOETHER_CHAIN_PATH = Path("source-intake/mts_residuals/P8_PARENT_WORLDTUBE_GLUE_NOETHER_CHAIN.csv")
OBSTRUCTIONS_PATH = Path("source-intake/mts_residuals/P8_PARENT_WORLDTUBE_GLUE_OBSTRUCTIONS.csv")
EXTERNAL_PROTOCOL_PATH = Path("source-intake/mts_residuals/P8_PARENT_WORLDTUBE_GLUE_EXTERNAL_RADIAL_PROTOCOL.csv")
DECISION_PATH = Path("source-intake/mts_residuals/P8_PARENT_WORLDTUBE_GLUE_DECISION.csv")
VALIDATION_PATH = Path("source-intake/mts_residuals/P8_PARENT_WORLDTUBE_GLUE_VALIDATION.csv")
ROUTE_UPDATE_PATH = Path("source-intake/mts_residuals/P8_PARENT_WORLDTUBE_GLUE_ROUTE_UPDATE.csv")

SOURCE_REGISTER = [
    {
        "source_file": "503-fill-radial-bound-inputs-or-return-to-parent-glue.md",
        "role": "establishes that no sourced numeric radial inputs are available and derivation must be attempted",
    },
    {
        "source_file": "502-radial-bound-runner-implementation-or-Hilbert-topological-glue.md",
        "role": "defines epsilon_radial_Meff runner and no-data/no-claim state",
    },
    {
        "source_file": "501-topological-Hilbert-current-equality-or-radial-bound-runner.md",
        "role": "shows direct equality Pi_M J_H = J_M_top is not yet derived",
    },
    {
        "source_file": "500-topological-PiM-current-parent-clause-or-radial-bound-runner.md",
        "role": "topological Pi_M current route and Hilbert-equality obstruction",
    },
    {
        "source_file": "499-parent-source-identity-for-closed-PiM-flux-or-radial-template.md",
        "role": "source-current decomposition d(Pi_M J_H) = -Pi_M dJ_extra + [d,Pi_M]J_H + A_parent",
    },
    {
        "source_file": "498-source-normalization-radial-and-calibration-theorem-attempt.md",
        "role": "exact exterior source-current integral for epsilon_radial_Meff",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_RADIAL_BOUND_INPUT_AUDIT_FILL_DECISION.csv",
        "role": "decision to avoid placeholder radial scoring",
    },
    {
        "source_file": "source-intake/local_bounds/local_bound_claims.csv",
        "role": "local empirical locks that any future residual must pass",
    },
    {
        "source_file": "scripts/parent_Hilbert_worldtube_glue_or_external_radial_input_plan.py",
        "role": "this checkpoint generator",
    },
]

THEOREM_CLAUSES = [
    {
        "clause_id": "W504_0_worldtube_setup",
        "claim": "compact source is represented by a worldtube W and the test region is an exterior annulus A with boundaries S1 and S2 linking W",
        "mathematical_form": "A = exterior(W) between S1 and S2; no source support in A",
        "needed_from_parent_action": "definition of source support and exterior domain",
        "status": "setup_allowed",
        "failure_mode": "no clean inside/outside split means no finite-radius mass-flux theorem",
    },
    {
        "clause_id": "W504_1_covariant_parent_Noether_identity",
        "claim": "a diffeomorphism-covariant parent action supplies a Noether identity for local translations/time flow",
        "mathematical_form": "δL = E_A δφ^A + dΘ; J_ξ = Θ(φ,L_ξφ) - i_ξ L; dJ_ξ = -E_A L_ξφ",
        "needed_from_parent_action": "explicit covariant Lagrangian and boundary term Θ",
        "status": "derivable_if_parent_action_covariant",
        "failure_mode": "without an action-level Noether identity the mass current is postulated, not derived",
    },
    {
        "clause_id": "W504_2_mass_charge_form",
        "claim": "the measured mass channel should be a parent Noether/constraint charge, not an arbitrary fitted Hilbert flux",
        "mathematical_form": "Pi_M J_H is replaced or identified with dQ_M[τ] plus constraint terms fixed before readout",
        "needed_from_parent_action": "definition of Q_M[τ], Pi_M, and the source-measure map",
        "status": "not_yet_derived_best_route",
        "failure_mode": "a conserved topological current can be the wrong object unless it equals the Hilbert/source mass charge",
    },
    {
        "clause_id": "W504_3_exterior_closure_equation",
        "claim": "radial independence follows if the parent charge form is closed in the compact exterior",
        "mathematical_form": "dQ_M[τ] = C_EH + C_extra + C_projector + C_boundary + C_Lambda_sub = 0 in A",
        "needed_from_parent_action": "vacuum exterior equations, projected extra-sector silence, projector constancy, and boundary/no-flux clause",
        "status": "conditional_not_closed",
        "failure_mode": "any nonzero C term is exactly epsilon_radial_Meff source hair",
    },
    {
        "clause_id": "W504_4_worldtube_source_measure_glue",
        "claim": "the worldtube source measure and the exterior Noether charge must read the same mass",
        "mathematical_form": "M_source[W] = integral_S Q_M[τ] = M_eff before orbital fitting",
        "needed_from_parent_action": "interior-to-exterior matching or Gauss-law constraint across W",
        "status": "not_yet_derived_core_missing_piece",
        "failure_mode": "closed exterior charge exists but is not proven to be the measured source monopole",
    },
    {
        "clause_id": "W504_5_calibration_and_limits",
        "claim": "the charge must reduce to GR/Poisson/Newton in the local weak-field limit",
        "mathematical_form": "Q_M[τ] -> Komar/ADM/Gauss mass charge; ∇²Φ = 4πGρ; exterior ∇²Φ = 0",
        "needed_from_parent_action": "normalization of G_ref, τ, and weak-field metric/coframe variables",
        "status": "conditional_limit_target",
        "failure_mode": "right-looking conservation law with wrong normalization or wrong Newtonian force",
    },
]

NOETHER_CHAIN = [
    {
        "step_id": "N504_0_variation",
        "equation": "δL = E_A δφ^A + dΘ",
        "meaning": "start from the parent action, not from a hand-named plateau current",
        "derived_status": "requires explicit parent Lagrangian",
    },
    {
        "step_id": "N504_1_diffeomorphism_current",
        "equation": "J_ξ = Θ(φ,L_ξφ) - i_ξ L, with dJ_ξ = -E_A L_ξφ",
        "meaning": "diffeomorphism invariance gives a current identity before fitting data",
        "derived_status": "formal Noether identity if action is covariant",
    },
    {
        "step_id": "N504_2_choose_local_time_flow",
        "equation": "ξ = τ in a local stationary/asymptotically inertial exterior",
        "meaning": "the mass channel is tied to the physical time-flow used by local observers",
        "derived_status": "conditional on local-vacuum/stationary branch",
    },
    {
        "step_id": "N504_3_charge_decomposition",
        "equation": "dQ_M[τ] = C_EH[E_g] + C_extra + C_projector + C_boundary + C_Lambda_sub",
        "meaning": "all ways the finite-radius mass charge can leak are named rather than hidden",
        "derived_status": "template; Q_M and C terms still need parent derivation",
    },
    {
        "step_id": "N504_4_radial_independence",
        "equation": "integral_S2 Q_M - integral_S1 Q_M = integral_A dQ_M",
        "meaning": "epsilon_radial_Meff is exactly the exterior constraint/leakage integral",
        "derived_status": "mathematical identity once Q_M is defined",
    },
    {
        "step_id": "N504_5_zero_condition",
        "equation": "C_EH = C_extra = C_projector = C_boundary = C_Lambda_sub = 0 implies epsilon_radial_Meff = 0",
        "meaning": "this is the precise no-plateau theorem route",
        "derived_status": "conditional; zero clauses not all derived",
    },
    {
        "step_id": "N504_6_source_measure_readout",
        "equation": "M_eff = M_source[W] = integral_S Q_M[τ]",
        "meaning": "the measured mass is fixed by the parent constraint, not fitted separately at each radius",
        "derived_status": "core missing glue",
    },
]

OBSTRUCTIONS = [
    {
        "obstruction_id": "O504_0_wrong_conserved_object",
        "problem": "a topological current can be closed but fail to equal the Hilbert/source mass charge",
        "fix_needed": "derive Pi_M J_H = dQ_M[τ] + exact zero-flux terms, or define the measured mass directly through Q_M with source-measure matching",
        "severity": "fatal_if_unfixed",
    },
    {
        "obstruction_id": "O504_1_projector_commutator",
        "problem": "field-dependent Pi_M gives [d,Pi_M]J_H terms in the radial derivative",
        "fix_needed": "make Pi_M covariantly constant/topological in the exterior, or retain C_projector in the bound runner",
        "severity": "fatal_for_exact_zero",
    },
    {
        "obstruction_id": "O504_2_extra_sector_stress",
        "problem": "bulk/domain/memory/non-EH terms can carry mass-channel flux in local vacuum",
        "fix_needed": "derive exterior silence/no-hair for each channel or keep channelwise numeric residuals",
        "severity": "fatal_for_local_GR_promotion",
    },
    {
        "obstruction_id": "O504_3_stationarity_or_flux",
        "problem": "nonstationary systems can radiate or exchange charge through the annulus",
        "fix_needed": "restrict theorem to local stationary/quasi-static PPN branch, or add radiation-memory flux terms",
        "severity": "branch_condition",
    },
    {
        "obstruction_id": "O504_4_calibration",
        "problem": "a closed charge with arbitrary normalization does not prove Newton's G or measured GM",
        "fix_needed": "derive weak-field normalization and Poisson/Gauss law limit",
        "severity": "fatal_for_Newton_limit",
    },
]

EXTERNAL_PROTOCOL = [
    {
        "input_id": "X504_0_R_eq",
        "required_columns": "system_id;r1;r2;R_eq_integral;norm_convention;units;source_file;assumptions;valid_for_claim",
        "use_if": "parent equality Pi_M J_H = Q_M route is not derived",
        "acceptance_rule": "must be source-backed, not a placeholder or fitted cancellation",
    },
    {
        "input_id": "X504_1_channel_flux_vector",
        "required_columns": "system_id;channel;r1;r2;I_extra_channel;units;affected_rows;source_file;assumptions;valid_for_claim",
        "use_if": "extra sectors remain active in the compact exterior",
        "acceptance_rule": "each channel must pass its own local lock without relying on cancellation",
    },
    {
        "input_id": "X504_2_radial_profile",
        "required_columns": "system_id;r1;r2;epsilon_radial_Meff;dln_mu_dlnr;bound_source;pass_fail;notes",
        "use_if": "orbital/fifth-force data are used to bound radial source hair directly",
        "acceptance_rule": "map to R4/R10/R11 and declare model/baseline dependence",
    },
]

DECISION_ROWS = [
    {
        "decision_id": "D504_0_best_route",
        "decision": "use_parent_Noether_mass_charge_route",
        "basis": "this mirrors the GR/Newton structure: exterior field equations close a charge, rather than a plateau axiom setting radial hair to zero",
        "claim_status": "conditional_theorem_route_not_final_claim",
    },
    {
        "decision_id": "D504_1_not_yet_enough",
        "decision": "do_not_promote_local_GR_or_Newton",
        "basis": "Q_M closure, source-measure matching, projector silence, extra-sector silence, and calibration are not all derived",
        "claim_status": "local_GR_claim_allowed_false",
    },
    {
        "decision_id": "D504_2_fallback",
        "decision": "if_parent_glue_fails_use_external_radial_protocol",
        "basis": "the 502 runner is ready but cannot be scored without source-backed input rows",
        "claim_status": "numeric_branch_available_but_empty",
    },
]

ROUTE_UPDATE_ROWS = [
    {
        "route_id": "RU504_0",
        "status": "derivation_route_narrowed",
        "update": "replace arbitrary Pi_M flux proof with parent Noether mass-charge closure plus worldtube source-measure matching",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "RU504_1",
        "status": "claim_ceiling_retained",
        "update": "radial source hair is expressible as exterior constraint/leakage integral, but zero is not derived until all C terms vanish",
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
    fatal_open = [
        row["clause_id"]
        for row in THEOREM_CLAUSES
        if row["status"] in {"not_yet_derived_best_route", "not_yet_derived_core_missing_piece", "conditional_not_closed"}
    ]
    return [
        {
            "check_id": "V504_0_source_paths_exist",
            "result": "pass" if not missing_sources else "fail",
            "detail": f"missing={len(missing_sources)}",
        },
        {
            "check_id": "V504_1_theorem_not_overclaimed",
            "result": "pass",
            "detail": f"open_core_clauses={';'.join(fatal_open)}",
        },
        {
            "check_id": "V504_2_radial_zero_not_derived",
            "result": "pass",
            "detail": "epsilon_radial_Meff_zero_derived=false",
        },
        {
            "check_id": "V504_3_external_protocol_available",
            "result": "pass",
            "detail": f"protocol_rows={len(EXTERNAL_PROTOCOL)}",
        },
        {
            "check_id": "V504_4_local_GR_claim_blocked",
            "result": "pass",
            "detail": "local_GR_claim_allowed=false",
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
    return f"""# 504 — Parent Hilbert Worldtube Glue or External Radial Input Plan

Generated: {generated_at_utc}  
Run: `{rel(run_dir)}`  
Status: `{STATUS}`  
Claim ceiling: `{CLAIM_CEILING}`

## 1. Verdict

The route is **alive but conditional**.

The clean GR-like path is not:

```text
assume a local plateau;
assume Pi_M J_H is closed;
assume the topological current is the measured source mass.
```

The clean path is:

```text
derive a parent Noether/constraint mass charge Q_M[τ];
prove Q_M is closed in the compact local exterior;
prove the worldtube source measure reads the same charge;
then epsilon_radial_Meff = 0 follows as a theorem.
```

This is exactly the kind of structure GR has in its Newtonian/local exterior limit: a mass charge is radially stable because the exterior field equations/constraints close it, not because a fitted function is declared flat.

## 2. Core Equation

The next derivation should target this identity:

```text
dQ_M[τ] = C_EH[E_g] + C_extra + C_projector + C_boundary + C_Lambda_sub.
```

Then:

```text
epsilon_radial_Meff(S1,S2)
  = (1/M_ref) integral_A dQ_M[τ]
  = (1/M_ref) integral_A (C_EH + C_extra + C_projector + C_boundary + C_Lambda_sub).
```

Therefore the exact zero theorem is:

```text
C_EH = C_extra = C_projector = C_boundary = C_Lambda_sub = 0
  => epsilon_radial_Meff = 0.
```

That is the non-smuggled plateau. It either comes from the parent action or it remains a closure condition.

## 3. Source Register

{markdown_table(sources)}

## 4. Theorem Clauses

{markdown_table(THEOREM_CLAUSES)}

## 5. Noether Chain

{markdown_table(NOETHER_CHAIN)}

## 6. Obstructions

{markdown_table(OBSTRUCTIONS)}

## 7. External Radial Protocol

{markdown_table(EXTERNAL_PROTOCOL)}

## 8. Decision

{markdown_table(DECISION_ROWS)}

## 9. Validation

{markdown_table(validations)}

## 10. Route Update

{markdown_table(ROUTE_UPDATE_ROWS)}

## 11. Claim Ceiling

Allowed:

```text
MTS has a precise parent-action contract for deriving local radial source silence.
MTS has reduced epsilon_radial_Meff to a parent charge-closure/leakage identity.
MTS has identified Q_M[τ] source-measure matching as the central missing theorem.
```

Forbidden:

```text
MTS has derived local GR.
MTS has derived Newtonian recovery.
MTS has derived epsilon_radial_Meff = 0.
MTS has proven Pi_M J_H equals a closed topological current.
MTS has scored the radial-bound runner.
```

## 12. Next Target

`{NEXT_TARGET}`

Try to derive the closure equation for `Q_M[τ]` from the parent action. If that cannot be done without extra assumptions, demote the local route to closure-only and use the external radial protocol.
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timestamp", default=datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S"))
    args = parser.parse_args()

    generated_at_utc = datetime.now(timezone.utc).isoformat()
    run_dir = ROOT / "runs" / f"{args.timestamp}-parent-Hilbert-worldtube-glue-or-external-radial-input-plan"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    sources = source_rows()
    validations = validation_rows(sources)

    csv_outputs: list[tuple[Path, list[dict[str, Any]]]] = [
        (SOURCE_REGISTER_PATH, sources),
        (THEOREM_CLAUSES_PATH, THEOREM_CLAUSES),
        (NOETHER_CHAIN_PATH, NOETHER_CHAIN),
        (OBSTRUCTIONS_PATH, OBSTRUCTIONS),
        (EXTERNAL_PROTOCOL_PATH, EXTERNAL_PROTOCOL),
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
        "theorem_clauses": str(ROOT / THEOREM_CLAUSES_PATH),
        "noether_chain": str(ROOT / NOETHER_CHAIN_PATH),
        "obstructions": str(ROOT / OBSTRUCTIONS_PATH),
        "external_protocol": str(ROOT / EXTERNAL_PROTOCOL_PATH),
        "decision": str(ROOT / DECISION_PATH),
        "validation": str(ROOT / VALIDATION_PATH),
        "route_update": str(ROOT / ROUTE_UPDATE_PATH),
        "source_rows": len(sources),
        "source_paths_missing": len(missing_sources),
        "missing_sources": missing_sources,
        "theorem_clause_rows": len(THEOREM_CLAUSES),
        "open_core_clause_rows": 3,
        "failed_validation_rows": len(failed_validations),
        "parent_Noether_mass_charge_route_defined": True,
        "parent_Noether_mass_charge_closure_derived": False,
        "parent_worldtube_source_measure_glue_derived": False,
        "PiM_Hilbert_topological_equality_derived": False,
        "epsilon_radial_Meff_zero_derived": False,
        "epsilon_radial_Meff_computed": False,
        "radial_bound_scored": False,
        "mu_extra_zero_derived": False,
        "source_normalized_Newton_promoted": False,
        "PPN_promoted": False,
        "local_GR_claim_allowed": False,
        "external_radial_protocol_available": True,
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
