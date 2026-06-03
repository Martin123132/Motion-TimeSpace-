from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

STATUS = "determinant_current_parent_ownership_attempt_written_shape_supported_parent_ownership_failed_demoted_to_theorem_target_no_alpha3_PPN_Newton_or_local_GR_pass"
CLAIM_CEILING = "detQ_current_parent_ownership_or_demotion_only_no_alpha3_pass_no_mu_extra_zero_PPN_Newton_or_local_GR_pass"
NEXT_TARGET = "479-R11-domain-source-normalization-zero-or-fill.md"

DOC_PATH = Path("478-determinant-current-parent-ownership-or-demotion.md")
SOURCE_REGISTER_PATH = Path("source-intake/mts_residuals/P8_DETQ_PARENT_SOURCE_REGISTER.csv")
THEOREM_ATTEMPT_PATH = Path("source-intake/mts_residuals/P8_DETQ_PARENT_THEOREM_ATTEMPT.csv")
OWNERSHIP_GATE_PATH = Path("source-intake/mts_residuals/P8_DETQ_PARENT_OWNERSHIP_GATE.csv")
ALPHA3_IMPACT_PATH = Path("source-intake/mts_residuals/P8_DETQ_ALPHA3_IMPACT.csv")
ROUTE_UPDATE_PATH = Path("source-intake/mts_residuals/P8_ALPHA3_DETQ_ROUTE_UPDATE.csv")
VALIDATION_PATH = Path("source-intake/mts_residuals/P8_DETQ_PARENT_VALIDATION.csv")
DECISION_PATH = Path("source-intake/mts_residuals/P8_DETQ_PARENT_DECISION.csv")

ALPHA3_INPUT_PATH = Path("source-intake/mts_residuals/P8_ALPHA3_BOUND_PRODUCT_INPUT.csv")
ALPHA3_EVALUATION_PATH = Path("source-intake/mts_residuals/P8_ALPHA3_BOUND_PRODUCT_EVALUATION.csv")
ALPHA3_THEOREM_GATE_PATH = Path("source-intake/mts_residuals/P8_ALPHA3_THEOREM_ZERO_GATE.csv")
R11_EXECUTABLE_VECTOR_PATH = Path("source-intake/mts_residuals/R11_nonEH_operator_vector_executable.csv")

SOURCE_REGISTER = [
    {
        "path": "275-JC-three-form-memory-current-from-Q.md",
        "role": "conditional det(Q_coh) three-form/current construction and shear-leak warning",
    },
    {
        "path": "276-coherent-domain-projector-from-parent-variables.md",
        "role": "fixed-D Q_coh projection support while physical domain selector remains open",
    },
    {
        "path": "277-domain-free-boundary-Euler-equation.md",
        "role": "free-boundary Euler route exists but is degenerate/incomplete",
    },
    {
        "path": "279-representative-selection-boundary-polarization-no-go.md",
        "role": "representative selection boundary polarization no-go and closure warning",
    },
    {
        "path": "309-MTS-boundary-projector-contract-attempt.md",
        "role": "P_MTS boundary/projector contract and parent-ownership gaps",
    },
    {
        "path": "416-binding-invariant-domain-selector-repair.md",
        "role": "best auxiliary C_exp route retained as contract rather than parent derivation",
    },
    {
        "path": "476-double-zero-memory-coupling-origin-or-coefficient-runner.md",
        "role": "p>=2 memory gate requirement; det(Q_coh) listed as conditional clue",
    },
    {
        "path": "477-alpha3-bound-product-evaluator.md",
        "role": "strict alpha3 product evaluator and no-cancellation guard",
    },
    {
        "path": str(ALPHA3_INPUT_PATH),
        "role": "current alpha3 product inputs",
    },
    {
        "path": str(ALPHA3_EVALUATION_PATH),
        "role": "current alpha3 evaluation rows",
    },
    {
        "path": str(ALPHA3_THEOREM_GATE_PATH),
        "role": "current alpha3 theorem-zero gates",
    },
    {
        "path": str(R11_EXECUTABLE_VECTOR_PATH),
        "role": "R11 executable-path vector; parseable but zero claim-valid rows",
    },
    {
        "path": "scripts/determinant_current_parent_ownership_or_demotion.py",
        "role": "this checkpoint generator",
    },
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with (ROOT / path).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], columns: list[str] | None = None) -> None:
    out = ROOT / path
    out.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fieldnames = columns or list(rows[0].keys())
    with out.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
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
        values = [str(row.get(column, "")).replace("\n", " ").replace("|", "/") for column in columns]
        lines.append("| " + " | ".join(values) + " |")
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


def r11_claimable_rows() -> int:
    if not (ROOT / R11_EXECUTABLE_VECTOR_PATH).exists():
        return 0
    return sum(1 for row in read_csv(R11_EXECUTABLE_VECTOR_PATH) if row.get("valid_for_claim") == "true")


def build_theorem_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "step_id": "D0_fixed_domain_shape",
            "claim": "for a fixed coherent domain, the memory current can be written as a determinant/volume three-form",
            "mathematical_form": "J_C = det(Q_coh) Omega_D / V_D",
            "evidence": "275 constructs J_C conditionally from Q_coh",
            "result": "conditional_shape_pass",
            "claim_effect": "supports p>=2/p=3 memory-gate shape only",
        },
        {
            "step_id": "D1_double_zero_shape",
            "claim": "det(Q_coh) supplies stronger-than-needed local double zero",
            "mathematical_form": "Q_coh=(N_D/u3)I, integral_D J_C=(N_D/u3)^3, J_M(0)=J_M_prime(0)=0",
            "evidence": "275 says the current has the double zero",
            "result": "conditional_shape_pass",
            "claim_effect": "good clue for 476 p>=2 origin",
        },
        {
            "step_id": "D2_unprojected_shear_no_go",
            "claim": "unprojected det(Q) is local-GR safe",
            "mathematical_form": "det(XI+S)=X^3-(X/2)Tr(S^2)+det(S)",
            "evidence": "275 shows tracefree shear leaks into unprojected determinant at second order",
            "result": "fail_for_local_GR",
            "claim_effect": "must use parent-owned Q_coh projection, not raw det(Q)",
        },
        {
            "step_id": "D3_Qcoh_projection_ownership",
            "claim": "Q_coh is selected by the parent action, not by fixed-D smoothing",
            "mathematical_form": "S_parent -> P_coh Q with P_coh idempotent/self-adjoint/Ward-owned",
            "evidence": "276 supports fixed-D projection but states domain selector not parent-derived",
            "result": "not_parent_derived",
            "claim_effect": "blocks theorem-zero use",
        },
        {
            "step_id": "D4_domain_selection_ownership",
            "claim": "the physical domain D and representative are selected by an Euler/variational law",
            "mathematical_form": "delta_D S_parent = 0 selects local trivial class and FLRW active class",
            "evidence": "277 route is degenerate/incomplete; 279 says representative selection not derived",
            "result": "not_parent_derived",
            "claim_effect": "blocks alpha3 domain zero",
        },
        {
            "step_id": "D5_projector_Ward_ownership",
            "claim": "P_MTS,D and P_coh are metric-independent/topological or carry retained stress",
            "mathematical_form": "delta_g P_MTS,D=0 in local bulk or T_projector retained",
            "evidence": "309 gives conditional projector contract; parent idempotence/domain selection still fail",
            "result": "conditional_not_parent_owned",
            "claim_effect": "blocks local-GR/alpha3 promotion",
        },
        {
            "step_id": "D6_alpha3_flux_zero",
            "claim": "det(Q_coh) proves W_domain_alpha3 epsilon_domain_flux=0",
            "mathematical_form": "J_C scalar/coherent zero -> P_loc^i_mu F_domain^mu = 0",
            "evidence": "requires D3-D5 plus R11 source-normalization silence",
            "result": "fail_current_corpus",
            "claim_effect": "domain alpha3 remains not scoreable",
        },
        {
            "step_id": "D7_verdict",
            "claim": "det(Q_coh) is currently a parent-owned theorem-zero source",
            "mathematical_form": "S_parent -> det(Q_coh) -> alpha3_domain=0",
            "evidence": "shape is useful, ownership is missing",
            "result": "demote_to_theorem_target_or_closure",
            "claim_effect": "no alpha3, PPN, Newton, or local-GR pass",
        },
    ]


def build_ownership_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "G0_fixed_D_shape",
            "requirement": "fixed-domain det(Q_coh) current has p>=2/p=3 shape",
            "current_status": "conditional_pass",
            "evidence": "275 determinant/current construction",
            "blocks_claim": "false",
            "repair_or_next": "keep as mathematical clue",
        },
        {
            "gate_id": "G1_raw_detQ_shear_safe",
            "requirement": "raw det(Q) has no tracefree-shear leakage",
            "current_status": "fail",
            "evidence": "det(XI+S)=X^3-(X/2)Tr(S^2)+det(S)",
            "blocks_claim": "true",
            "repair_or_next": "must use parent-owned coherent projection",
        },
        {
            "gate_id": "G2_Qcoh_projection_parent_owned",
            "requirement": "P_coh/Q_coh is derived from parent variables before scoring",
            "current_status": "not_derived",
            "evidence": "276 fixed-D projection only; 309 projector ownership conditional",
            "blocks_claim": "true",
            "repair_or_next": "derive projector algebra/ownership or demote closure",
        },
        {
            "gate_id": "G3_physical_domain_selected",
            "requirement": "physical D/representative is selected by parent Euler/topological law",
            "current_status": "not_derived",
            "evidence": "277 degenerate free-boundary route; 279 no-go for representative selection",
            "blocks_claim": "true",
            "repair_or_next": "derive class-selection law or retain explicit domain coefficient",
        },
        {
            "gate_id": "G4_local_zero_class",
            "requirement": "local branch has N_D=0/trivial relative class while FLRW remains active",
            "current_status": "not_parent_derived",
            "evidence": "416 retains C_exp/chi_D route as contract",
            "blocks_claim": "true",
            "repair_or_next": "derive local zero/FLRW active split",
        },
        {
            "gate_id": "G5_Ward_stress_accounting",
            "requirement": "det-current/projector/domain stress is varied, zero, or retained",
            "current_status": "conditional_open",
            "evidence": "309 and 477 require parent-premise gates before theorem-zero",
            "blocks_claim": "true",
            "repair_or_next": "write stress ledger or keep coefficient runner",
        },
        {
            "gate_id": "G6_R11_silence",
            "requirement": "domain source-normalization/R11 rows are claim-valid or theorem-zero",
            "current_status": "fail_for_claim",
            "evidence": f"R11_claimable_rows={r11_claimable_rows()}",
            "blocks_claim": "true",
            "repair_or_next": NEXT_TARGET,
        },
    ]


def build_alpha3_impact_rows() -> list[dict[str, Any]]:
    return [
        {
            "impact_id": "I0_best_case_if_owned",
            "channel": "domain_projector_mass",
            "target_row": "R7_alpha3",
            "condition": "det(Q_coh) parent-owned, local N_D=0/trivial class, no shear leakage, Ward/R11 silent",
            "predicted_effect": "W_domain_alpha3 epsilon_domain_flux = 0",
            "current_status": "not_available",
            "valid_for_claim": "false",
        },
        {
            "impact_id": "I1_current_route",
            "channel": "domain_projector_mass",
            "target_row": "R7_alpha3",
            "condition": "det(Q_coh) only conditional/fixed-D shape support",
            "predicted_effect": "missing numeric product or theorem-zero source",
            "current_status": "not_scoreable",
            "valid_for_claim": "false",
        },
        {
            "impact_id": "I2_alpha3_evaluator",
            "channel": "domain_projector_mass",
            "target_row": "R7_alpha3",
            "condition": "477 evaluator requires abs(W_domain_alpha3 epsilon_domain_flux)<=4e-20 or accepted theorem-zero",
            "predicted_effect": "evaluation remains not_scoreable_inputs_missing",
            "current_status": "retained",
            "valid_for_claim": "false",
        },
        {
            "impact_id": "I3_no_cancellation",
            "channel": "combined_mu_extra_alpha3",
            "target_row": "R7_alpha3",
            "condition": "total alpha3 cannot pass through fitted cancellation",
            "predicted_effect": "boundary and domain channels must pass individually",
            "current_status": "guard_retained",
            "valid_for_claim": "false",
        },
    ]


def build_route_update_rows() -> list[dict[str, Any]]:
    return [
        {
            "route_id": "DETQ_domain_alpha3",
            "alpha3_gate": "TG_domain_zero",
            "candidate_zero_source": "det(Q_coh) coherent determinant/current",
            "accepted_as_zero": "false",
            "why_not": "fixed-D shape is conditional; parent Q_coh projection, domain selection, shear exclusion, Ward stress, and R11 silence are not derived",
            "next_action": NEXT_TARGET,
        },
        {
            "route_id": "DETQ_closure_policy",
            "alpha3_gate": "A3_domain",
            "candidate_zero_source": "det(Q_coh) closure branch",
            "accepted_as_zero": "false",
            "why_not": "may be used only as labelled closure/theorem target, not as PPN evidence",
            "next_action": "if derivation stalls, fill numeric product template",
        },
    ]


def build_validation_rows(
    sources: list[dict[str, Any]],
    theorem_rows: list[dict[str, Any]],
    gate_rows: list[dict[str, Any]],
    impact_rows: list[dict[str, Any]],
    route_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    missing_sources = sum(1 for row in sources if row["exists"] != "True")
    blocking_gates = sum(1 for row in gate_rows if row["blocks_claim"] == "true")
    claim_rows = sum(1 for row in impact_rows if row["valid_for_claim"] == "true")
    return [
        {
            "rule_id": "V478_0_sources",
            "rule": "all cited source paths exist",
            "result": "pass" if missing_sources == 0 else "fail",
            "evidence": f"missing_sources={missing_sources}",
            "claim_effect": "traceability only",
        },
        {
            "rule_id": "V478_1_shape_vs_ownership",
            "rule": "theorem attempt separates determinant shape support from parent ownership",
            "result": "pass",
            "evidence": f"theorem_rows={len(theorem_rows)}",
            "claim_effect": "no hidden promotion",
        },
        {
            "rule_id": "V478_2_blocking_gates",
            "rule": "ownership gates record all blockers",
            "result": "fail_for_claim",
            "evidence": f"blocking_gates={blocking_gates}",
            "claim_effect": "det(Q_coh) cannot be accepted as theorem-zero",
        },
        {
            "rule_id": "V478_3_alpha3_impact",
            "rule": "alpha3 impact rows remain unpromoted",
            "result": "fail_for_claim",
            "evidence": f"valid_for_claim_true={claim_rows}",
            "claim_effect": "no alpha3/PPN/local-GR pass",
        },
        {
            "rule_id": "V478_4_route_update",
            "rule": "det(Q_coh) route update explicitly rejects theorem-zero status",
            "result": "pass" if len(route_rows) == 2 and all(row["accepted_as_zero"] == "false" for row in route_rows) else "fail",
            "evidence": f"route_rows={len(route_rows)}",
            "claim_effect": "closure/theorem-target only",
        },
        {
            "rule_id": "V478_5_R11_dependency",
            "rule": "R11 source-normalization remains separate blocker",
            "result": "fail_for_claim",
            "evidence": f"R11_claimable_rows={r11_claimable_rows()}",
            "claim_effect": "next target is R11 zero-or-fill",
        },
    ]


def build_decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "D0_shape",
            "status": "useful_conditionally",
            "meaning": "det(Q_coh) gives the right p>=2/p=3 double-zero shape for the memory gate",
            "next_action": "keep as best theorem target",
        },
        {
            "decision_id": "D1_parent_ownership",
            "status": "not_derived",
            "meaning": "Q_coh projection, physical domain selection, projector ownership, and stress accounting are not parent-owned",
            "next_action": "do not accept det(Q_coh) as theorem-zero",
        },
        {
            "decision_id": "D2_alpha3",
            "status": "not_scoreable",
            "meaning": "det(Q_coh) does not yet fill W_domain_alpha3 epsilon_domain_flux or prove it zero",
            "next_action": "keep alpha3 evaluator retained",
        },
        {
            "decision_id": "D3_demotion",
            "status": "theorem_target_or_closure",
            "meaning": "det(Q_coh) may be used only as labelled closure/theorem target until ownership is derived",
            "next_action": NEXT_TARGET,
        },
        {
            "decision_id": "D4_promotion",
            "status": "forbidden",
            "meaning": "no alpha3 pass, mu_extra zero, PPN, Newtonian-limit, or local-GR pass is earned",
            "next_action": NEXT_TARGET,
        },
    ]


def build_doc(run_dir: Path) -> str:
    source_rows = read_csv(SOURCE_REGISTER_PATH)
    theorem_rows = read_csv(THEOREM_ATTEMPT_PATH)
    gate_rows = read_csv(OWNERSHIP_GATE_PATH)
    impact_rows = read_csv(ALPHA3_IMPACT_PATH)
    route_rows = read_csv(ROUTE_UPDATE_PATH)
    validation_rows = read_csv(VALIDATION_PATH)
    decision_rows = read_csv(DECISION_PATH)
    return f"""# 478 - Determinant Current Parent Ownership Or Demotion

Private determinant-current/domain-alpha3 checkpoint. This is not a public alpha3 pass, PPN pass, Newtonian-limit pass, local-GR derivation, cosmology result, EM result, or unified-field claim.

## 1. Purpose

Checkpoint `477` left the hardest product open:

```text
W_domain_alpha3 * epsilon_domain_flux.
```

The best current theorem-zero clue is:

```text
J_C = det(Q_coh) Omega_D / V_D.
```

This checkpoint asks whether that current is parent-owned enough to zero domain alpha3.

Short answer:

```text
The shape is good.
The ownership is not there.
So det(Q_coh) is demoted to theorem target / labelled closure, not accepted evidence.
```

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/determinant_current_parent_ownership_or_demotion.py` |
| Run directory | `{run_dir.relative_to(ROOT)}` |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## 3. Source Register

{md_table(source_rows)}

## 4. Theorem Attempt

{md_table(theorem_rows)}

The useful result:

```text
det(Q_coh) can give a p=3 double-zero memory shape.
```

The killer caveat:

```text
raw det(Q) leaks tracefree shear, so only parent-owned Q_coh is admissible.
```

## 5. Ownership Gates

{md_table(gate_rows)}

This is the round score:

```text
shape support: yes.
parent ownership: no.
alpha3 theorem-zero: no.
```

## 6. Alpha3 Impact

{md_table(impact_rows)}

So the current alpha3 evaluator remains:

```text
A3_domain = not_scoreable_inputs_missing.
```

## 7. Route Update

{md_table(route_rows)}

`det(Q_coh)` is not thrown away.

It is promoted in clarity:

```text
best theorem target / disciplined closure branch.
```

It is not promoted in claims:

```text
no alpha3, no PPN, no local GR.
```

## 8. Validation

{md_table(validation_rows)}

## 9. Decision

{md_table(decision_rows)}

## 10. Claim Ceiling

Allowed:

```text
det(Q_coh) is the best current double-zero/current-shape clue.
```

Allowed:

```text
det(Q_coh) remains a theorem target or labelled closure.
```

Forbidden:

```text
MTS parent-derives det(Q_coh) as the physical domain current.
```

Forbidden:

```text
MTS passes domain alpha3, PPN, Newton, or local GR.
```

## 11. Next Queue

| Rank | Target | Why |
| ---: | --- | --- |
| 1 | `479-R11-domain-source-normalization-zero-or-fill.md` | even a perfect determinant route still needs R11 source-normalization/operator silence |
| 2 | `480-alpha3-numeric-product-input-template.md` | if derivation stalls, make W_domain_alpha3 epsilon_domain_flux numerically fillable |
| 3 | `481-Qcoh-parent-projector-algebra-or-closure.md` | optional deeper route: try to parent-own Q_coh/P_coh itself |
"""


def write_run(timestamp: str) -> dict[str, Any]:
    run_dir = ROOT / "runs" / f"{timestamp}-determinant-current-parent-ownership-or-demotion"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    sources = source_register_rows()
    theorem_rows = build_theorem_attempt_rows()
    gate_rows = build_ownership_gate_rows()
    impact_rows = build_alpha3_impact_rows()
    route_rows = build_route_update_rows()
    validation_rows = build_validation_rows(sources, theorem_rows, gate_rows, impact_rows, route_rows)
    decision_rows = build_decision_rows()

    write_csv(SOURCE_REGISTER_PATH, sources)
    write_csv(THEOREM_ATTEMPT_PATH, theorem_rows)
    write_csv(OWNERSHIP_GATE_PATH, gate_rows)
    write_csv(ALPHA3_IMPACT_PATH, impact_rows)
    write_csv(ROUTE_UPDATE_PATH, route_rows)
    write_csv(VALIDATION_PATH, validation_rows)
    write_csv(DECISION_PATH, decision_rows)

    for path in [
        SOURCE_REGISTER_PATH,
        THEOREM_ATTEMPT_PATH,
        OWNERSHIP_GATE_PATH,
        ALPHA3_IMPACT_PATH,
        ROUTE_UPDATE_PATH,
        VALIDATION_PATH,
        DECISION_PATH,
    ]:
        write_csv(Path(results_dir.relative_to(ROOT)) / path.name.lower(), read_csv(path))

    (ROOT / DOC_PATH).write_text(build_doc(run_dir), encoding="utf-8")

    status = {
        "timestamp": timestamp,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "checkpoint_doc": str(DOC_PATH),
        "run_dir": str(run_dir),
        "source_register": str(ROOT / SOURCE_REGISTER_PATH),
        "theorem_attempt": str(ROOT / THEOREM_ATTEMPT_PATH),
        "ownership_gate": str(ROOT / OWNERSHIP_GATE_PATH),
        "alpha3_impact": str(ROOT / ALPHA3_IMPACT_PATH),
        "route_update": str(ROOT / ROUTE_UPDATE_PATH),
        "validation": str(ROOT / VALIDATION_PATH),
        "decision": str(ROOT / DECISION_PATH),
        "source_rows": len(sources),
        "source_paths_missing": sum(1 for row in sources if row["exists"] != "True"),
        "theorem_rows": len(theorem_rows),
        "ownership_gate_rows": len(gate_rows),
        "alpha3_impact_rows": len(impact_rows),
        "route_update_rows": len(route_rows),
        "validation_rows": len(validation_rows),
        "decision_rows": len(decision_rows),
        "R11_claimable_rows": r11_claimable_rows(),
        "detQ_shape_supported": True,
        "detQ_parent_owned": False,
        "detQ_accepted_as_theorem_zero": False,
        "domain_alpha3_score_ready": False,
        "alpha3_passed": False,
        "domain_channel_promoted": False,
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
