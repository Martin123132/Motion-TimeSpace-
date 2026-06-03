from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

STATUS = "boundary_alpha3_scalar_no_flux_lemma_written_parent_owner_missing_no_numeric_coefficient_no_Newton_or_local_GR_pass"
CLAIM_CEILING = "conditional_boundary_alpha3_zero_lemma_only_no_mu_extra_zero_PPN_Newton_or_local_GR_pass"
NEXT_TARGET = "471-boundary-scalar-action-owner-or-domain-alpha3-no-leak.md"

DOC_PATH = Path("470-boundary-alpha3-zero-theorem-or-numeric-coefficient.md")
SOURCE_REGISTER_PATH = Path("source-intake/mts_residuals/P8_BOUNDARY_ALPHA3_SOURCE_REGISTER.csv")
THEOREM_PATH = Path("source-intake/mts_residuals/P8_BOUNDARY_ALPHA3_NOFLUX_THEOREM_ATTEMPT.csv")
PREMISE_PATH = Path("source-intake/mts_residuals/P8_BOUNDARY_ALPHA3_PREMISE_OWNERSHIP.csv")
COEFFICIENT_GATE_PATH = Path("source-intake/mts_residuals/P8_MU_EXTRA_BOUNDARY_ALPHA3_COEFFICIENT_GATE.csv")
BOUNDARY_COEFFICIENTS_PATH = Path("source-intake/mts_residuals/P8_mu_extra_boundary_coefficients.csv")
DECISION_PATH = Path("source-intake/mts_residuals/P8_BOUNDARY_ALPHA3_DECISION.csv")

SCORECARD_PATH = Path("source-intake/mts_residuals/P8_MU_EXTRA_LOCAL_BOUND_SCORECARD.csv")
ALPHA3_SKELETON_PATH = Path("source-intake/mts_residuals/P8_MU_EXTRA_ALPHA3_FILL_INPUT_SKELETON.csv")


SOURCE_REGISTER = [
    {
        "path": "229-second-order-beta-or-boundary-scalar-owner.md",
        "role": "scalar-only compact boundary symmetry gives trace-only tangential stress as sufficient condition",
    },
    {
        "path": "352-boundary-nohair-and-PPN-residual-vector-gate.md",
        "role": "decomposes boundary residual into trace, radial, shear, vector/preferred-frame, and flux sectors",
    },
    {
        "path": "353-boundary-nohair-theorem-attempt-or-PPN-bound-runner.md",
        "role": "states class-only scalar boundary no-hair contract and records missing parent ownership",
    },
    {
        "path": "429-Ward-Bianchi-exchange-owner-for-Poisson-source.md",
        "role": "Ward/Bianchi ownership of hidden flux, but not absence",
    },
    {
        "path": "435-exterior-extra-source-nohair-owner-gate.md",
        "role": "keeps boundary/projector alpha3 exchange retained until zero or scored",
    },
    {
        "path": "469-fill-or-zero-highest-pressure-mu-extra-row.md",
        "role": "identifies R7_alpha3 as tied highest-pressure mu_extra row",
    },
    {
        "path": str(SCORECARD_PATH),
        "role": "machine-readable alpha3 scorecard bound",
    },
    {
        "path": str(ALPHA3_SKELETON_PATH),
        "role": "alpha3 fill skeleton requiring W_boundary_alpha3 epsilon_boundary_flux",
    },
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with (ROOT / path).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    out = ROOT / path
    out.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    columns = list(rows[0].keys())
    with out.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def md_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return ""
    columns = list(rows[0].keys())
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |")
    return "\n".join(lines)


def source_register_rows() -> list[dict[str, str]]:
    return [
        {
            "source_file": item["path"],
            "exists": str((ROOT / item["path"]).exists()),
            "role": item["role"],
        }
        for item in SOURCE_REGISTER
    ]


def boundary_scorecard_row() -> dict[str, str]:
    rows = [
        row
        for row in read_csv(SCORECARD_PATH)
        if row["epsilon_channel"] == "boundary_monopole_shift" and row["target_row"] == "R7_alpha3"
    ]
    if len(rows) != 1:
        raise ValueError(f"expected 1 boundary alpha3 row, found {len(rows)}")
    return rows[0]


def build_theorem_attempt() -> list[dict[str, Any]]:
    return [
        {
            "step_id": "T0_target_projection",
            "claim": "boundary contribution to alpha3 is the local preferred-momentum flux projection",
            "mathematical_form": "F_boundary_alpha3 = lim_S r^2 n_mu P_loc_nu K_boundary^{mu nu}/(G_eff M_eff)",
            "result": "definition_pass",
            "requires": "469 alpha3 skeleton and boundary scorecard row",
            "failure_if_missing": "epsilon_boundary scalar name has no physical score meaning",
        },
        {
            "step_id": "T1_scalar_boundary_action",
            "claim": "on a compact stationary collar, a scalar-only boundary action has no tangential vector or trace-free tensor stress",
            "mathematical_form": "S_boundary = integral_boundary sqrt(abs(gamma)) F(Y_scalar); tau_AB = tau gamma_AB",
            "result": "conditional_lemma_from_229",
            "requires": "F depends only on scalar shell data and no tangential memory/current/shear label",
            "failure_if_missing": "boundary stress can carry B_0i or B_TF components",
        },
        {
            "step_id": "T2_no_normal_flux_from_tangential_trace",
            "claim": "trace-only tangential shell stress has zero normal projected momentum flux",
            "mathematical_form": "n_mu P_loc_nu tau gamma_tangent^{mu nu} = 0 because n_mu gamma_tangent^{mu nu}=0",
            "result": "mathematical_pass_if_T1",
            "requires": "boundary stress is pure tangential trace and all normal exchange terms are included separately",
            "failure_if_missing": "unowned normal exchange can still source alpha3",
        },
        {
            "step_id": "T3_no_preferred_vector",
            "claim": "alpha3 needs a surviving local vector/preferred-frame or nonconserved momentum channel; scalar monopole trace has none",
            "mathematical_form": "B_0i = 0 and n_mu B^{mu i} = 0 imply W_boundary_alpha3 = 0",
            "result": "conditional_mathematical_pass",
            "requires": "stationarity, no material boundary marker, no tangential vector, and universal observed coframe",
            "failure_if_missing": "a marker/vector field can generate preferred-frame rows despite scalar mass shift",
        },
        {
            "step_id": "T4_mass_monopole_allowed",
            "claim": "a conserved scalar boundary monopole can renormalize measured GM without producing alpha3",
            "mathematical_form": "mu_boundary = constant monopole; partial_t,r,frame mu_boundary = 0; F_boundary_alpha3 = 0",
            "result": "conditional_pass",
            "requires": "constant universal calibration and derivative silence",
            "failure_if_missing": "beta, xi, and Gdot rows can remain active even if alpha3 is zero",
        },
        {
            "step_id": "T5_parent_owner_audit",
            "claim": "current corpus proves the boundary action always satisfies T1-T4",
            "mathematical_form": "parent action -> scalar-only stationary boundary class -> no vector/flux channel",
            "result": "fail_not_parent_owned",
            "requires": "class-only boundary action, no marker fields, full metric variation, Ward flux closure",
            "failure_if_missing": "conditional lemma cannot be used as a scorecard pass",
        },
        {
            "step_id": "T6_numeric_fallback",
            "claim": "if T1-T4 are not parent-owned, score boundary alpha3 numerically",
            "mathematical_form": "abs(W_boundary_alpha3 epsilon_boundary_flux) <= 4e-20",
            "result": "missing_numeric_coefficient",
            "requires": "W_boundary_alpha3, epsilon_boundary_flux, units, source path, and normalization",
            "failure_if_missing": "boundary alpha3 remains not scoreable",
        },
        {
            "step_id": "T7_conclusion",
            "claim": "boundary alpha3 is killed only conditionally, not promoted",
            "mathematical_form": "scalar_stationary_boundary => W_boundary_alpha3 = 0; current corpus !=> scalar_stationary_boundary",
            "result": "conditional_zero_lemma_no_claim",
            "requires": "premise ownership or numeric coefficient",
            "failure_if_missing": "local PPN branch remains retained",
        },
    ]


def build_premise_ownership() -> list[dict[str, Any]]:
    return [
        {
            "premise_id": "P0_scalar_only_boundary_data",
            "needed_for_zero": "boundary action uses only scalar shell invariants",
            "current_evidence": "229 derives sufficient scalar-boundary symmetry lemma",
            "owner_status": "conditional_not_parent_global",
            "blocks_claim": "true",
            "repair_route": "derive parent action excludes tangential vectors/tensors on compact stationary collars",
        },
        {
            "premise_id": "P1_no_material_boundary_marker",
            "needed_for_zero": "no hidden tangent vector, spin direction, active-domain marker, or preferred frame survives locally",
            "current_evidence": "353 lists this as A4 no material boundary marker",
            "owner_status": "not_derived",
            "blocks_claim": "true",
            "repair_route": "prove boundary class is topological/scalar or retain vector coefficient",
        },
        {
            "premise_id": "P2_full_metric_variation",
            "needed_for_zero": "boundary stress is varied and included, not dropped",
            "current_evidence": "435 forbids hidden dropped-stress fake GR routes",
            "owner_status": "policy_pass_not_zero",
            "blocks_claim": "true",
            "repair_route": "write boundary metric variation with stress ledger and no leftover flux",
        },
        {
            "premise_id": "P3_stationary_compact_collar",
            "needed_for_zero": "no time-dependent boundary flux or radial leakage",
            "current_evidence": "353 A1 requires isolated stationary compact exterior",
            "owner_status": "branch_assumption_not_universal_theorem",
            "blocks_claim": "true",
            "repair_route": "state local branch domain of validity and prove stationary collar equations",
        },
        {
            "premise_id": "P4_Ward_flux_closure",
            "needed_for_zero": "owned Ward/Bianchi identity reduces normal exchange to zero or exact cancellation before data",
            "current_evidence": "429 gives ownership but not absence",
            "owner_status": "conditional_identity_only",
            "blocks_claim": "true",
            "repair_route": "derive n_mu B_boundary^{mu i}=0 or supply coefficient",
        },
        {
            "premise_id": "P5_constant_monopole_calibration",
            "needed_for_zero": "remaining boundary trace is constant measured-GM renormalization only",
            "current_evidence": "353 identifies pure conserved monopole trace as locally safe",
            "owner_status": "conditional",
            "blocks_claim": "true",
            "repair_route": "prove derivative silence for R4/R9 rows or keep boundary coefficient artifact partial",
        },
    ]


def build_coefficient_gate() -> list[dict[str, Any]]:
    score = boundary_scorecard_row()
    return [
        {
            "gate_id": "C0_bound_lock",
            "target_row": score["target_row"],
            "observable": score["observable"],
            "bound": f"{score['bound_value']} {score['bound_units']}",
            "map": "alpha3_boundary = W_boundary_alpha3 * epsilon_boundary_flux",
            "current_input": score["predicted_input"],
            "gate_result": "pass_lock_loaded",
            "claim_status": "not_claimable",
        },
        {
            "gate_id": "C1_conditional_zero_value",
            "target_row": "R7_alpha3",
            "observable": "alpha3",
            "bound": "4e-20 dimensionless",
            "map": "if scalar_stationary_boundary premises hold, W_boundary_alpha3 = 0",
            "current_input": "CONDITIONAL_ZERO_LEMMA",
            "gate_result": "conditional_not_scoreable",
            "claim_status": "premises_not_parent_owned",
        },
        {
            "gate_id": "C2_numeric_fallback",
            "target_row": "R7_alpha3",
            "observable": "alpha3",
            "bound": "4e-20 dimensionless",
            "map": "abs(W_boundary_alpha3 * epsilon_boundary_flux) <= 4e-20",
            "current_input": "MISSING_NUMERIC_COEFFICIENT_PRODUCT",
            "gate_result": "fail_missing_input",
            "claim_status": "not_claimable",
        },
    ]


def build_boundary_coefficients() -> list[dict[str, Any]]:
    return [
        {
            "channel": "boundary_monopole_shift",
            "target_row": "R4_beta",
            "observable": "beta_minus_1",
            "coefficient_symbol": "epsilon_boundary_beta",
            "map": "beta_minus_1 ~ F_boundary_beta[epsilon_boundary]",
            "value_or_theorem": "MISSING_NUMERIC_OR_DERIVED_ZERO",
            "premise_status": "not_addressed_in_470",
            "target_bound": "7.8e-05 dimensionless",
            "score_status": "not_scoreable",
            "valid_for_claim": "false",
            "source": str(DOC_PATH),
        },
        {
            "channel": "boundary_monopole_shift",
            "target_row": "R7_alpha3",
            "observable": "alpha3",
            "coefficient_symbol": "W_boundary_alpha3_epsilon_boundary_flux",
            "map": "alpha3_boundary = W_boundary_alpha3 * epsilon_boundary_flux",
            "value_or_theorem": "0_IF_SCALAR_STATIONARY_BOUNDARY_PREMISES_ARE_PARENT_OWNED_ELSE_MISSING_NUMERIC_PRODUCT",
            "premise_status": "conditional_zero_lemma_parent_owner_missing",
            "target_bound": "4e-20 dimensionless",
            "score_status": "conditional_not_scoreable",
            "valid_for_claim": "false",
            "source": str(DOC_PATH),
        },
        {
            "channel": "boundary_monopole_shift",
            "target_row": "R8_xi",
            "observable": "xi",
            "coefficient_symbol": "epsilon_boundary_shear",
            "map": "xi ~ F_boundary_shear[epsilon_boundary]",
            "value_or_theorem": "MISSING_NUMERIC_OR_DERIVED_ZERO",
            "premise_status": "not_addressed_in_470",
            "target_bound": "symbolic/row lock from scorecard",
            "score_status": "not_scoreable",
            "valid_for_claim": "false",
            "source": str(DOC_PATH),
        },
        {
            "channel": "boundary_monopole_shift",
            "target_row": "R9_Gdot",
            "observable": "Gdot_over_G",
            "coefficient_symbol": "d_epsilon_boundary_dt",
            "map": "Gdot/G ~ d epsilon_boundary/dt",
            "value_or_theorem": "MISSING_NUMERIC_OR_DERIVED_ZERO",
            "premise_status": "not_addressed_in_470",
            "target_bound": "9.6e-15 yr^-1",
            "score_status": "not_scoreable",
            "valid_for_claim": "false",
            "source": str(DOC_PATH),
        },
    ]


def build_decision() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "D0_mathematical_lemma",
            "status": "conditional_pass",
            "meaning": "pure scalar stationary boundary stress has no normal preferred-momentum flux, so W_boundary_alpha3=0 under those premises",
            "next_action": "try to parent-own scalar stationary boundary premises",
        },
        {
            "decision_id": "D1_parent_ownership",
            "status": "fail_current_corpus",
            "meaning": "the corpus does not yet prove all boundary terms are scalar-only, stationary, marker-free, and flux-closed",
            "next_action": "derive scalar boundary action owner or retain coefficient",
        },
        {
            "decision_id": "D2_numeric_fallback",
            "status": "missing",
            "meaning": "no W_boundary_alpha3 epsilon_boundary_flux product is supplied",
            "next_action": "if theorem route fails, fill numeric coefficient product below 4e-20",
        },
        {
            "decision_id": "D3_partial_artifact",
            "status": "written",
            "meaning": "P8_mu_extra_boundary_coefficients.csv now records alpha3 conditional zero and leaves beta/xi/Gdot unscored",
            "next_action": "do not treat boundary channel as passed",
        },
        {
            "decision_id": "D4_promotion",
            "status": "forbidden",
            "meaning": "boundary alpha3, mu_extra zero, PPN, Newton, and local GR remain unpromoted",
            "next_action": "keep claim ceiling active",
        },
    ]


def build_doc(run_dir: Path) -> str:
    source_rows = read_csv(SOURCE_REGISTER_PATH)
    theorem_rows = read_csv(THEOREM_PATH)
    premise_rows = read_csv(PREMISE_PATH)
    coefficient_gate_rows = read_csv(COEFFICIENT_GATE_PATH)
    boundary_coeff_rows = read_csv(BOUNDARY_COEFFICIENTS_PATH)
    decision_rows = read_csv(DECISION_PATH)
    return f"""# 470 - Boundary `alpha3` Zero Theorem Or Numeric Coefficient

Private local-GR/Newton/PPN source-normalization checkpoint. This is not a public PPN pass, Newtonian-limit pass, local-GR derivation, measured-GM derivation, cosmology result, EM result, or unified-field claim.

## 1. Purpose

Checkpoint `469` found the current highest-pressure `mu_extra` row:

```text
boundary_monopole_shift -> R7_alpha3 <= 4e-20.
```

This checkpoint tries the theorem route first:

```text
Can the boundary contribution to alpha3 be forced to zero by scalar/stationary boundary structure?
```

Short answer:

```text
Mathematical zero lemma: yes, conditionally.
Parent-owned theorem: not yet.
Numeric coefficient fallback: missing.
```

So this is useful, but not a PPN pass.

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/boundary_alpha3_zero_theorem_or_numeric_coefficient.py` |
| Run directory | `{run_dir.relative_to(ROOT)}` |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## 3. Source Register

{md_table(source_rows)}

## 4. The Lemma

The dangerous object from `469` is:

```text
F_boundary,alpha3 = lim_S r^2 n_mu P_loc_nu K_boundary^(mu nu)/(G_eff M_eff).
```

If the compact boundary action is scalar-only:

```text
S_boundary = integral_boundary sqrt(abs(gamma)) F(Y_scalar),
```

then the tangential boundary stress has the form:

```text
tau_AB = tau gamma_AB.
```

Lifting this into the local collar gives a tangential trace stress. Since the tangent projector is orthogonal to the boundary normal:

```text
n_mu gamma_tangent^(mu nu) = 0,
```

the preferred-momentum flux projection vanishes:

```text
n_mu P_loc_nu K_boundary^(mu nu) = 0.
```

Therefore:

```text
W_boundary_alpha3 = 0
alpha3_boundary = 0
```

provided the boundary really is scalar-only, stationary, marker-free, fully varied, and flux-closed.

## 5. Theorem Attempt

{md_table(theorem_rows)}

The useful counterpunch:

```text
scalar stationary boundary monopole cannot source alpha3.
```

The reason it does not win the round yet:

```text
the parent corpus has not proved every boundary contribution is forced into that scalar stationary class.
```

## 6. Premise Ownership

{md_table(premise_rows)}

This is the exact gap:

```text
lemma proven as a conditional tensor statement;
premises not yet parent-owned.
```

## 7. Coefficient Gate

{md_table(coefficient_gate_rows)}

Partial boundary coefficient artifact:

{md_table(boundary_coeff_rows)}

This deliberately does not mark the boundary channel as passed. It only records the exact conditional zero and the fallback product needed if the premise route fails:

```text
abs(W_boundary_alpha3 epsilon_boundary_flux) <= 4e-20.
```

## 8. Decision

{md_table(decision_rows)}

Plain-English status:

```text
Boundary alpha3 is not hopeless. It has a clean zero route:
make the boundary scalar, stationary, marker-free, and flux-closed.
But that route is not parent-owned yet, so no PPN/local-GR promotion.
```

Boxing-score version:

```text
We found the counter. We have not proved the fighter can throw it every time.
```

## 9. Claim Ceiling

Allowed:

```text
If the boundary sector is scalar-only, stationary, marker-free, and flux-closed, its alpha3 contribution is zero.
```

Allowed:

```text
The remaining task is to parent-own those boundary premises or supply a numeric coefficient product below 4e-20.
```

Forbidden:

```text
MTS passes PPN alpha3.
```

Forbidden:

```text
MTS derives mu_extra=0, Newton, or local GR.
```

## 10. Next Queue

| Rank | Target | Why |
| ---: | --- | --- |
| 1 | `471-boundary-scalar-action-owner-or-domain-alpha3-no-leak.md` | decide whether to parent-own the scalar boundary premises or move to the tied domain row |
| 2 | `472-domain-projector-alpha3-no-leak-or-R11-link.md` | domain/projector row is tied at the same 4e-20 lock |
| 3 | `473-alpha3-bound-product-evaluator.md` | only useful after theorem premises or numeric products exist |
"""


def write_run(timestamp: str) -> dict[str, Any]:
    run_dir = ROOT / "runs" / f"{timestamp}-boundary-alpha3-zero-theorem-or-numeric-coefficient"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    write_csv(SOURCE_REGISTER_PATH, source_register_rows())
    write_csv(THEOREM_PATH, build_theorem_attempt())
    write_csv(PREMISE_PATH, build_premise_ownership())
    write_csv(COEFFICIENT_GATE_PATH, build_coefficient_gate())
    write_csv(BOUNDARY_COEFFICIENTS_PATH, build_boundary_coefficients())
    write_csv(DECISION_PATH, build_decision())

    for path in [
        SOURCE_REGISTER_PATH,
        THEOREM_PATH,
        PREMISE_PATH,
        COEFFICIENT_GATE_PATH,
        BOUNDARY_COEFFICIENTS_PATH,
        DECISION_PATH,
    ]:
        write_csv(Path(results_dir.relative_to(ROOT)) / path.name.lower(), read_csv(path))

    (ROOT / DOC_PATH).write_text(build_doc(run_dir), encoding="utf-8")

    source_rows = read_csv(SOURCE_REGISTER_PATH)
    theorem_rows = read_csv(THEOREM_PATH)
    premise_rows = read_csv(PREMISE_PATH)
    coefficient_rows = read_csv(BOUNDARY_COEFFICIENTS_PATH)
    decision_rows = read_csv(DECISION_PATH)
    status = {
        "timestamp": timestamp,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "checkpoint_doc": str(DOC_PATH),
        "run_dir": str(run_dir),
        "source_register": str(ROOT / SOURCE_REGISTER_PATH),
        "theorem_attempt": str(ROOT / THEOREM_PATH),
        "premise_ownership": str(ROOT / PREMISE_PATH),
        "coefficient_gate": str(ROOT / COEFFICIENT_GATE_PATH),
        "boundary_coefficients": str(ROOT / BOUNDARY_COEFFICIENTS_PATH),
        "decision": str(ROOT / DECISION_PATH),
        "source_rows": len(source_rows),
        "source_paths_missing": sum(1 for row in source_rows if row["exists"] != "True"),
        "theorem_rows": len(theorem_rows),
        "premise_rows": len(premise_rows),
        "boundary_coefficient_rows": len(coefficient_rows),
        "decision_rows": len(decision_rows),
        "boundary_alpha3_conditional_zero_lemma": True,
        "boundary_alpha3_parent_owned": False,
        "numeric_coefficient_product_supplied": False,
        "score_ready_rows": 0,
        "boundary_alpha3_promoted": False,
        "boundary_channel_promoted": False,
        "mu_extra_zero_promoted": False,
        "Newtonian_reduction_promoted": False,
        "PPN_promoted": False,
        "local_GR_claim_allowed": False,
        "next_target": NEXT_TARGET,
    }
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    return status


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timestamp", default=datetime.now().strftime("%Y%m%d-%H%M%S"))
    args = parser.parse_args()
    print(json.dumps(write_run(args.timestamp), indent=2))


if __name__ == "__main__":
    main()
