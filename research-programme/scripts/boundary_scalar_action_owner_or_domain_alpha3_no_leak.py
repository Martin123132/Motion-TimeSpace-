from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

STATUS = "boundary_scalar_action_owner_attempt_written_conditional_homogeneous_scalar_contract_not_parent_derived_boundary_alpha3_closure_only_no_local_GR_pass"
CLAIM_CEILING = "boundary_scalar_action_contract_or_closure_only_no_boundary_channel_pass_no_mu_extra_zero_PPN_Newton_or_local_GR_pass"
NEXT_TARGET = "472-domain-projector-alpha3-no-leak-or-R11-link.md"

DOC_PATH = Path("471-boundary-scalar-action-owner-or-domain-alpha3-no-leak.md")
SOURCE_REGISTER_PATH = Path("source-intake/mts_residuals/P8_BOUNDARY_SCALAR_ACTION_SOURCE_REGISTER.csv")
OWNER_ATTEMPT_PATH = Path("source-intake/mts_residuals/P8_BOUNDARY_SCALAR_ACTION_OWNER_ATTEMPT.csv")
REPAIR_LEDGER_PATH = Path("source-intake/mts_residuals/P8_BOUNDARY_SCALAR_PREMISE_REPAIR_LEDGER.csv")
CLOSURE_STATUS_PATH = Path("source-intake/mts_residuals/P8_BOUNDARY_ALPHA3_CLOSURE_STATUS.csv")
DECISION_PATH = Path("source-intake/mts_residuals/P8_BOUNDARY_SCALAR_ACTION_DECISION.csv")


SOURCE_REGISTER = [
    {
        "path": "229-second-order-beta-or-boundary-scalar-owner.md",
        "role": "sufficient scalar-boundary symmetry lemma and warning that parent scalar action remains missing",
    },
    {
        "path": "309-MTS-boundary-projector-contract-attempt.md",
        "role": "projector/boundary contract requiring parent-owned scalar/coherent sector and Ward-safe stress accounting",
    },
    {
        "path": "324-CD-activity-kernel-commutation-gate.md",
        "role": "conditional route K_boundary=f(A_D) and [K_boundary,A_D]=0, with parent origin not derived",
    },
    {
        "path": "352-boundary-nohair-and-PPN-residual-vector-gate.md",
        "role": "boundary residual decomposition showing vector, shear, and flux hazards",
    },
    {
        "path": "353-boundary-nohair-theorem-attempt-or-PPN-bound-runner.md",
        "role": "boundary no-hair A1-A7 contract and A3-A7 parent gaps",
    },
    {
        "path": "356-parent-action-ward-identity-and-projector-variation.md",
        "role": "parent action Ward ledger exposes boundary force channel but does not kill it",
    },
    {
        "path": "470-boundary-alpha3-zero-theorem-or-numeric-coefficient.md",
        "role": "conditional boundary alpha3 zero lemma and premise ownership gaps",
    },
    {
        "path": "source-intake/mts_residuals/P8_BOUNDARY_ALPHA3_PREMISE_OWNERSHIP.csv",
        "role": "machine-readable premise ownership gaps from checkpoint 470",
    },
    {
        "path": "source-intake/mts_residuals/P8_mu_extra_boundary_coefficients.csv",
        "role": "partial boundary coefficient artifact with alpha3 conditional zero only",
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


def build_owner_attempt() -> list[dict[str, Any]]:
    return [
        {
            "route_id": "O0_representation_zero",
            "candidate_parent_statement": "local compact boundary carries only the l=0 scalar singlet of the active MTS sector",
            "derivation_test": "SO(3) tangent little-group: scalar homogeneous monopole cannot project onto vector/preferred-frame alpha3 channel",
            "result": "mathematical_pass_if_premise",
            "owned_by_current_corpus": "no",
            "gap": "parent action has not proved only the scalar singlet is available",
            "effect_on_boundary_alpha3": "conditional_zero_only",
        },
        {
            "route_id": "O1_homogeneous_scalar_action",
            "candidate_parent_statement": "S_boundary = integral sqrt(abs(gamma)) F(Q_B, trK, R_boundary_topological, scalar_memory) with all scalars homogeneous on the collar",
            "derivation_test": "variation gives tau_AB proportional to gamma_AB; tangential Hessian trace-free pieces vanish because D_A scalar = 0",
            "result": "conditional_pass",
            "owned_by_current_corpus": "no",
            "gap": "229 gives sufficient form but does not derive F or homogeneity from parent dynamics",
            "effect_on_boundary_alpha3": "W_boundary_alpha3_zero_if_owned",
        },
        {
            "route_id": "O2_scalar_not_enough_warning",
            "candidate_parent_statement": "arbitrary scalar boundary functional is safe",
            "derivation_test": "check nonlinear F(R_boundary, phi) terms with angularly varying scalars",
            "result": "fail_as_general_statement",
            "owned_by_current_corpus": "not_applicable",
            "gap": "D_A D_B F_R and D_A phi D_B phi can contain trace-free parts",
            "effect_on_boundary_alpha3": "requires homogeneous scalar monopole, not just scalar words",
        },
        {
            "route_id": "O3_kernel_commutation",
            "candidate_parent_statement": "K_boundary = f(A_D) and C_D/P_MTS are parent-owned, so [K_boundary,A_D]=0 and no ordinary/vector sector mixes into boundary",
            "derivation_test": "324 shows K=f(A_D) commutes and blocks cross-sector leakage if parent-owned",
            "result": "conditional_pass",
            "owned_by_current_corpus": "no",
            "gap": "324 explicitly says parent C_D and kernel commutation are not derived",
            "effect_on_boundary_alpha3": "would help kill marker/vector leakage if derived",
        },
        {
            "route_id": "O4_no_marker_fields",
            "candidate_parent_statement": "boundary state has no material marker, tangent vector, spin direction, domain velocity, or preferred frame",
            "derivation_test": "absence of vector representations removes B_0i and alpha3 source",
            "result": "needed_but_not_derived",
            "owned_by_current_corpus": "no",
            "gap": "no parent exclusion theorem for marker/vector boundary data",
            "effect_on_boundary_alpha3": "blocks promotion",
        },
        {
            "route_id": "O5_Ward_flux_closure",
            "candidate_parent_statement": "boundary normal momentum flux is zero, not merely Ward-owned",
            "derivation_test": "n_mu B_boundary^{mu i}=0 or exact cancellation before data",
            "result": "conditional_identity_only",
            "owned_by_current_corpus": "no",
            "gap": "356/429 expose boundary force channel but do not prove absence",
            "effect_on_boundary_alpha3": "blocks promotion",
        },
        {
            "route_id": "O6_constant_monopole",
            "candidate_parent_statement": "remaining boundary trace is conserved constant measured-GM monopole with no time/radial/frame derivative",
            "derivation_test": "partial_t epsilon_boundary = partial_r epsilon_boundary = partial_frame epsilon_boundary = 0",
            "result": "conditional_safe_for_alpha3",
            "owned_by_current_corpus": "no",
            "gap": "R4 beta and R9 Gdot boundary rows remain unscored",
            "effect_on_boundary_alpha3": "not enough to pass full boundary channel",
        },
        {
            "route_id": "O7_parent_owner_verdict",
            "candidate_parent_statement": "current corpus parent-derives scalar homogeneous marker-free flux-closed boundary action",
            "derivation_test": "all O0-O6 owner gaps closed without new axiom",
            "result": "fail",
            "owned_by_current_corpus": "no",
            "gap": "closure-only unless a new parent action clause supplies O0-O6",
            "effect_on_boundary_alpha3": "conditional_closure_not_scorecard_pass",
        },
    ]


def build_repair_ledger() -> list[dict[str, Any]]:
    return [
        {
            "repair_id": "R0_parent_scalar_boundary_action",
            "missing_premise": "derive the boundary action uses only homogeneous scalar shell/class data",
            "minimum_parent_clause": "S_boundary depends on Q_B, trK, Euler/topological curvature term, and scalar memory constants only",
            "would_close": "P0 scalar-only boundary data and homogeneous scalar warning",
            "current_status": "missing",
            "next_test": "write explicit parent action clause or demote to closure assumption",
        },
        {
            "repair_id": "R1_no_marker_exclusion",
            "missing_premise": "exclude tangent vector, spin marker, active-domain velocity, and preferred-frame labels",
            "minimum_parent_clause": "boundary Hilbert space has only scalar singlet representation in stationary compact local branch",
            "would_close": "P1 no material boundary marker",
            "current_status": "missing",
            "next_test": "prove representation selection from parent symmetry or add retained vector coefficient",
        },
        {
            "repair_id": "R2_full_boundary_variation",
            "missing_premise": "vary boundary metric and boundary fields without dropping stress",
            "minimum_parent_clause": "delta S_boundary produces a stress ledger with trace, shear, vector, normal flux components explicitly zero or retained",
            "would_close": "P2 full metric variation",
            "current_status": "structural_policy_only",
            "next_test": "derive stress components for candidate S_boundary",
        },
        {
            "repair_id": "R3_stationary_collar_equations",
            "missing_premise": "derive isolated compact stationary collar conditions",
            "minimum_parent_clause": "local vacuum branch has no boundary time flow, radial leakage, or angular scalar gradients",
            "would_close": "P3 stationary compact collar",
            "current_status": "branch_assumption",
            "next_test": "state branch domain and derive Euler/stationarity equations",
        },
        {
            "repair_id": "R4_flux_zero",
            "missing_premise": "Ward-owned boundary force is actually zero in local compact branch",
            "minimum_parent_clause": "n_mu B_boundary^{mu i}=0 follows from boundary Euler equations or topological exactness",
            "would_close": "P4 Ward flux closure",
            "current_status": "identity_not_absence",
            "next_test": "derive normal momentum no-flux or keep alpha3 coefficient product",
        },
        {
            "repair_id": "R5_constant_monopole_derivative_silence",
            "missing_premise": "remaining scalar boundary monopole is constant universal calibration",
            "minimum_parent_clause": "partial_t,r,frame epsilon_boundary = 0 and source/species/range independence",
            "would_close": "P5 constant monopole calibration for alpha3-adjacent rows",
            "current_status": "missing_for_full_channel",
            "next_test": "score R4_beta/R9_Gdot/R8_xi boundary rows after alpha3",
        },
    ]


def build_closure_status() -> list[dict[str, Any]]:
    return [
        {
            "item": "boundary_alpha3",
            "status": "conditional_closure_only",
            "proof_or_input": "homogeneous scalar stationary boundary with no marker fields and zero normal flux gives W_boundary_alpha3=0",
            "valid_for_scorecard": "false",
            "blocks": "PPN_alpha3_pass;mu_extra_zero;local_GR",
            "next_action": "parent-own O0-O6 or supply numeric W_boundary_alpha3 epsilon_boundary_flux",
        },
        {
            "item": "boundary_channel_total",
            "status": "not_closed",
            "proof_or_input": "alpha3 conditional route exists but beta/xi/Gdot boundary coefficients remain missing",
            "valid_for_scorecard": "false",
            "blocks": "boundary_monopole_shift_channel_pass",
            "next_action": "after alpha3, score derivative/shear/monopole rows or prove constant universal monopole",
        },
        {
            "item": "domain_alpha3",
            "status": "unaddressed_tied_pressure_row",
            "proof_or_input": "domain_projector_mass remains tied at alpha3=4e-20",
            "valid_for_scorecard": "false",
            "blocks": "combined_alpha3;local_GR",
            "next_action": NEXT_TARGET,
        },
        {
            "item": "local_GR",
            "status": "not_promoted",
            "proof_or_input": "boundary scalar action owner fails and domain row remains open",
            "valid_for_scorecard": "false",
            "blocks": "goal_completion",
            "next_action": "continue local residual derivations and empirical gates",
        },
    ]


def build_decision() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "D0_owner_attempt",
            "status": "fail_as_parent_theorem",
            "meaning": "the scalar-boundary route is mathematically coherent but not forced by the current parent corpus",
            "next_action": "do not promote boundary alpha3",
        },
        {
            "decision_id": "D1_closure_option",
            "status": "allowed_if_labelled",
            "meaning": "one may define an internal local closure branch with homogeneous scalar stationary boundary data",
            "next_action": "label it closure-only unless O0-O6 are parent-derived",
        },
        {
            "decision_id": "D2_scorecard_status",
            "status": "not_scoreable",
            "meaning": "no parent theorem and no numeric W_boundary_alpha3 epsilon_boundary_flux product",
            "next_action": "keep score_ready_rows at zero",
        },
        {
            "decision_id": "D3_domain_priority",
            "status": "move_to_domain_row",
            "meaning": "boundary alpha3 has a conditional route; tied domain alpha3 still has no no-leak attempt at this specificity",
            "next_action": NEXT_TARGET,
        },
        {
            "decision_id": "D4_claim_ceiling",
            "status": "enforced",
            "meaning": "no mu_extra zero, PPN, Newton, or local-GR pass",
            "next_action": "continue derivation gates",
        },
    ]


def build_doc(run_dir: Path) -> str:
    source_rows = read_csv(SOURCE_REGISTER_PATH)
    owner_rows = read_csv(OWNER_ATTEMPT_PATH)
    repair_rows = read_csv(REPAIR_LEDGER_PATH)
    closure_rows = read_csv(CLOSURE_STATUS_PATH)
    decision_rows = read_csv(DECISION_PATH)
    return f"""# 471 - Boundary Scalar Action Owner Or Domain `alpha3` No-Leak

Private local-GR/Newton/PPN source-normalization checkpoint. This is not a public PPN pass, Newtonian-limit pass, local-GR derivation, measured-GM derivation, cosmology result, EM result, or unified-field claim.

## 1. Purpose

Checkpoint `470` found a conditional kill route for the boundary contribution to `alpha3`:

```text
homogeneous scalar stationary boundary
  -> no vector/preferred-frame flux
  -> W_boundary_alpha3 = 0.
```

This checkpoint asks the hard follow-up:

```text
Does the current parent corpus force that boundary class?
```

Short answer:

```text
No.
```

But the failure is useful: it distinguishes a legitimate local closure branch from a parent-derived local-GR theorem.

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/boundary_scalar_action_owner_or_domain_alpha3_no_leak.py` |
| Run directory | `{run_dir.relative_to(ROOT)}` |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## 3. Source Register

{md_table(source_rows)}

## 4. Key Refinement

The safe condition is not merely:

```text
boundary is scalar.
```

The safe condition is:

```text
boundary is homogeneous scalar monopole,
stationary,
marker-free,
fully varied,
and normal-flux closed.
```

Reason:

```text
an angularly varying scalar can still generate trace-free Hessian/shear terms.
```

So the parent action must do more than remove explicit vector fields. It must also remove angular scalar gradients and boundary marker labels in the compact local branch.

## 5. Owner Attempt

{md_table(owner_rows)}

Verdict:

```text
The scalar-boundary route is mathematically coherent.
The current parent corpus does not force it.
```

## 6. Repair Ledger

{md_table(repair_rows)}

The exact parent contract needed for a real promotion is:

```text
S_boundary = integral_boundary sqrt(abs(gamma)) F(Q_B, trK, chi_Euler, scalar_memory_constants)
```

with:

```text
D_A Q_B = D_A scalar_memory = 0,
no tangent vector/tensor boundary representation,
n_mu B_boundary^(mu i) = 0,
and partial_t,r,frame epsilon_boundary = 0.
```

Without those clauses, the boundary `alpha3` row is closure-only.

## 7. Closure Status

{md_table(closure_rows)}

This is the honest status:

```text
boundary alpha3 can be killed by an explicit local closure assumption,
but it is not killed by a parent theorem yet.
```

## 8. Decision

{md_table(decision_rows)}

Plain-English status:

```text
We did not smuggle the plateau axiom back in.
We found the exact boundary plateau contract and marked it as closure-only until the parent action earns it.
```

Boxing-score version:

```text
This round was not a knockout. It was footwork: we now know which punch is real and which one is still shadowboxing.
```

## 9. Claim Ceiling

Allowed:

```text
The boundary alpha3 row has a clean conditional closure: homogeneous scalar stationary boundary data imply zero preferred-frame flux.
```

Allowed:

```text
The parent action must derive homogeneous scalar boundary data, no marker fields, full variation, Ward no-flux, and constant monopole calibration before alpha3 can pass.
```

Forbidden:

```text
MTS parent-derives boundary alpha3 = 0.
```

Forbidden:

```text
MTS passes PPN alpha3, mu_extra zero, Newton, or local GR.
```

## 10. Next Queue

| Rank | Target | Why |
| ---: | --- | --- |
| 1 | `472-domain-projector-alpha3-no-leak-or-R11-link.md` | domain/projector row is tied at the same 4e-20 lock and has not received the specific no-leak attempt |
| 2 | `473-boundary-scalar-action-parent-clause-draft.md` | only if we want to propose a new parent action clause rather than mark boundary as closure-only |
| 3 | `474-alpha3-bound-product-evaluator.md` | only useful after either theorem premises or numeric coefficient products exist |
"""


def write_run(timestamp: str) -> dict[str, Any]:
    run_dir = ROOT / "runs" / f"{timestamp}-boundary-scalar-action-owner-or-domain-alpha3-no-leak"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    write_csv(SOURCE_REGISTER_PATH, source_register_rows())
    write_csv(OWNER_ATTEMPT_PATH, build_owner_attempt())
    write_csv(REPAIR_LEDGER_PATH, build_repair_ledger())
    write_csv(CLOSURE_STATUS_PATH, build_closure_status())
    write_csv(DECISION_PATH, build_decision())

    for path in [SOURCE_REGISTER_PATH, OWNER_ATTEMPT_PATH, REPAIR_LEDGER_PATH, CLOSURE_STATUS_PATH, DECISION_PATH]:
        write_csv(Path(results_dir.relative_to(ROOT)) / path.name.lower(), read_csv(path))

    (ROOT / DOC_PATH).write_text(build_doc(run_dir), encoding="utf-8")

    source_rows = read_csv(SOURCE_REGISTER_PATH)
    owner_rows = read_csv(OWNER_ATTEMPT_PATH)
    repair_rows = read_csv(REPAIR_LEDGER_PATH)
    closure_rows = read_csv(CLOSURE_STATUS_PATH)
    decision_rows = read_csv(DECISION_PATH)
    status = {
        "timestamp": timestamp,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "checkpoint_doc": str(DOC_PATH),
        "run_dir": str(run_dir),
        "source_register": str(ROOT / SOURCE_REGISTER_PATH),
        "owner_attempt": str(ROOT / OWNER_ATTEMPT_PATH),
        "repair_ledger": str(ROOT / REPAIR_LEDGER_PATH),
        "closure_status": str(ROOT / CLOSURE_STATUS_PATH),
        "decision": str(ROOT / DECISION_PATH),
        "source_rows": len(source_rows),
        "source_paths_missing": sum(1 for row in source_rows if row["exists"] != "True"),
        "owner_attempt_rows": len(owner_rows),
        "repair_rows": len(repair_rows),
        "closure_rows": len(closure_rows),
        "decision_rows": len(decision_rows),
        "boundary_alpha3_conditional_closure": True,
        "boundary_scalar_action_parent_owned": False,
        "boundary_alpha3_score_ready": False,
        "boundary_alpha3_promoted": False,
        "boundary_channel_promoted": False,
        "domain_alpha3_still_open": True,
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
