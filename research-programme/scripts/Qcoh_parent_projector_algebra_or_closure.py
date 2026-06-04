from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

STATUS = "Qcoh_parent_projector_algebra_written_trace_projector_pass_parent_action_missing_closure_retained_no_alpha3_PPN_Newton_or_local_GR_pass"
CLAIM_CEILING = "Qcoh_trace_projector_algebra_only_no_parent_action_ownership_no_alpha3_PPN_Newton_or_local_GR_pass"
NEXT_TARGET = "482-local-residual-vector-from-domain-source-fill.md"

DOC_PATH = Path("481-Qcoh-parent-projector-algebra-or-closure.md")
SOURCE_REGISTER_PATH = Path("source-intake/mts_residuals/P8_QCOH_PARENT_PROJECTOR_SOURCE_REGISTER.csv")
ALGEBRA_THEOREM_PATH = Path("source-intake/mts_residuals/P8_QCOH_PROJECTOR_ALGEBRA_THEOREM.csv")
PARENT_CONTRACT_PATH = Path("source-intake/mts_residuals/P8_QCOH_PARENT_ACTION_CONTRACT.csv")
ALPHA3_IMPACT_PATH = Path("source-intake/mts_residuals/P8_QCOH_ALPHA3_IMPACT.csv")
VALIDATION_PATH = Path("source-intake/mts_residuals/P8_QCOH_PROJECTOR_VALIDATION.csv")
DECISION_PATH = Path("source-intake/mts_residuals/P8_QCOH_PROJECTOR_DECISION.csv")
ROUTE_UPDATE_PATH = Path("source-intake/mts_residuals/P8_QCOH_PROJECTOR_ROUTE_UPDATE.csv")


SOURCE_REGISTER = [
    {
        "source_file": "275-JC-three-form-memory-current-from-Q.md",
        "role": "conditional det(Q_coh) current, double-zero shape, and unprojected shear-leak warning",
    },
    {
        "source_file": "276-coherent-domain-projector-from-parent-variables.md",
        "role": "fixed-domain coherent projection support and domain-selector warning",
    },
    {
        "source_file": "277-domain-free-boundary-Euler-equation.md",
        "role": "free-boundary Euler route, currently degenerate/incomplete",
    },
    {
        "source_file": "279-representative-selection-boundary-polarization-no-go.md",
        "role": "representative selection no-go unless a parent law selects the class",
    },
    {
        "source_file": "309-MTS-boundary-projector-contract-attempt.md",
        "role": "projector stress and parent-ownership contract",
    },
    {
        "source_file": "416-binding-invariant-domain-selector-repair.md",
        "role": "C_exp/domain selector retained as auxiliary contract rather than parent derivation",
    },
    {
        "source_file": "478-determinant-current-parent-ownership-or-demotion.md",
        "role": "det(Q_coh) shape supported but parent ownership rejected",
    },
    {
        "source_file": "479-R11-domain-source-normalization-zero-or-fill.md",
        "role": "R11/domain source silence rejected; fill requirements written",
    },
    {
        "source_file": "480-alpha3-numeric-product-input-template.md",
        "role": "alpha3 numeric/theorem-zero product template and no-cancellation guard",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_ALPHA3_NUMERIC_PRODUCT_INPUT_TEMPLATE.csv",
        "role": "active alpha3 product rows",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_ALPHA3_DOMAIN_SIBLING_INPUT_TEMPLATE.csv",
        "role": "domain sibling rows required before domain alpha3 can score",
    },
    {
        "source_file": "source-intake/mts_residuals/R11_DOMAIN_SOURCE_FILL_REQUIREMENTS.csv",
        "role": "R11/domain source-normalization fill contract",
    },
    {
        "source_file": "scripts/Qcoh_parent_projector_algebra_or_closure.py",
        "role": "this checkpoint generator",
    },
]


ALGEBRA_ROWS = [
    {
        "step_id": "A0_spatial_split",
        "claim": "local coherent load is tested on the spatial symmetric tensor sector",
        "mathematical_form": "h_{mu nu}=g_{mu nu}+u_mu u_nu; Q_{mu nu}=h_mu^a h_nu^b Q_{ab}; Q_{mu nu}=X h_{mu nu}/3+S_{mu nu}; h^{mu nu}S_{mu nu}=0",
        "result": "definition_gate_pass",
        "proof_sketch": "any local PPN preferred-frame residual decomposes into trace scalar plus trace-free shear on the observer rest space",
        "blocks_promotion": "false",
    },
    {
        "step_id": "A1_unique_trace_projector",
        "claim": "the only SO(3)-equivariant self-adjoint idempotent coherent scalar projector is the trace projector",
        "mathematical_form": "(P_coh Q)_{mu nu}=(1/3)h_{mu nu}h^{ab}Q_{ab}",
        "result": "algebra_pass",
        "proof_sketch": "the symmetric spatial tensor representation splits into scalar trace plus spin-2 trace-free irreducibles; Schur/irreducible decomposition fixes the scalar projector",
        "blocks_promotion": "false",
    },
    {
        "step_id": "A2_idempotence_self_adjoint",
        "claim": "P_coh is a clean projector, not a smoothing knob",
        "mathematical_form": "P_coh^2=P_coh; <P_coh A,B>_h=<A,P_coh B>_h",
        "result": "algebra_pass",
        "proof_sketch": "two contractions with h return the trace part, and the h-inner-product makes trace/STF sectors orthogonal",
        "blocks_promotion": "false",
    },
    {
        "step_id": "A3_shear_exclusion",
        "claim": "the trace projector removes the raw determinant shear leak identified in 478",
        "mathematical_form": "det_h(P_coh Q)=(Tr_h Q/3)^3; P_coh(S_TF)=0",
        "result": "conditional_algebra_pass",
        "proof_sketch": "raw det(XI+S) contains STF leakage, but det(P_coh Q) depends only on the scalar trace",
        "blocks_promotion": "false",
    },
    {
        "step_id": "A4_double_zero_shape",
        "claim": "if the local coherent trace X_D is parent-forced to zero, the determinant current has the desired p=3 zero",
        "mathematical_form": "J_C proportional det_h(P_coh Q)=(X_D/3)^3; J_C(0)=J_C'(0)=J_C''(0)=0",
        "result": "conditional_shape_pass",
        "proof_sketch": "the cubic determinant automatically kills the constant, linear, and quadratic local residual in the scalar trace variable",
        "blocks_promotion": "true",
    },
    {
        "step_id": "A5_parent_action_missing",
        "claim": "the current corpus derives P_coh and X_D=0 from the parent action",
        "mathematical_form": "delta S_parent/delta P_coh=0 and delta S_parent/delta chi_D=0 force trace-only local trivial class",
        "result": "fail_for_claim",
        "proof_sketch": "available sources give fixed-domain or conditional projector contracts, not an Euler/Ward law that selects the physical coherent projector and domain",
        "blocks_promotion": "true",
    },
]


PARENT_CONTRACT_ROWS = [
    {
        "contract_id": "C0_parent_variable",
        "requirement": "Q_{mu nu} must be an action variable or derived Noether/load tensor, not a fitted post-processor",
        "acceptance_test": "source gives S_parent and a variational equation whose weak-field variable is Q_{mu nu}",
        "current_status": "missing_explicit_parent_variable",
        "valid_for_local_GR_claim": "false",
        "next_action": "derive Q from parent action or keep Qcoh branch closure-only",
    },
    {
        "contract_id": "C1_projector_ownership",
        "requirement": "P_coh must be forced by symmetry/Ward/Euler equations before fitting",
        "acceptance_test": "P_coh=(1/3)hh is not merely chosen; parent local isotropy or a constraint removes STF modes through PPN order",
        "current_status": "algebra_known_parent_ownership_missing",
        "valid_for_local_GR_claim": "false",
        "next_action": "write parent clause that makes trace/STF decomposition dynamical rather than analytic bookkeeping",
    },
    {
        "contract_id": "C2_domain_selector",
        "requirement": "the physical domain/representative chi_D must be selected by a parent Euler/topological law",
        "acceptance_test": "delta S_parent/delta chi_D=0 selects local compact vacuum trivial class and FLRW active class without hand scales",
        "current_status": "not_derived",
        "valid_for_local_GR_claim": "false",
        "next_action": "derive domain selector or fill numeric domain coefficients",
    },
    {
        "contract_id": "C3_stress_accounting",
        "requirement": "metric variation of P_coh and chi_D must be zero/topological or explicitly retained",
        "acceptance_test": "delta_g P_coh and delta_g chi_D terms are shown to vanish or are included in the local residual vector",
        "current_status": "retained_debt",
        "valid_for_local_GR_claim": "false",
        "next_action": "produce projector/domain stress ledger before claiming Bianchi/PPN silence",
    },
    {
        "contract_id": "C4_R11_silence",
        "requirement": "source-normalization and non-EH R11 rows must vanish by theorem or be scored numerically",
        "acceptance_test": "R11/domain rows are claim-valid and have no missing/conditional debt markers",
        "current_status": "failed_in_479",
        "valid_for_local_GR_claim": "false",
        "next_action": "use 479/480 fill templates or derive R11 zero from parent equations",
    },
    {
        "contract_id": "C5_no_cancellation",
        "requirement": "alpha3 cannot be rescued by post-fit cancellation between boundary and domain channels",
        "acceptance_test": "each active alpha3 channel passes individually unless a parent identity forces exact cancellation before fitting",
        "current_status": "guard_active",
        "valid_for_local_GR_claim": "false",
        "next_action": "keep A3_BOUNDARY and A3_DOMAIN independent until theorem-zero certificates exist",
    },
]


ALPHA3_IMPACT_ROWS = [
    {
        "impact_id": "I0_trace_projector",
        "route": "P_coh trace projector",
        "what_is_earned": "raw determinant shear leak is removed at the algebra level",
        "what_is_not_earned": "parent action has not forced this as the physical projector",
        "alpha3_effect": "no alpha3 pass",
        "valid_for_claim": "false",
    },
    {
        "impact_id": "I1_cubic_current",
        "route": "det_h(P_coh Q)",
        "what_is_earned": "p=3/double-zero shape if X_D is zero",
        "what_is_not_earned": "X_D=0 local class is not derived",
        "alpha3_effect": "domain alpha3 remains template_unfilled",
        "valid_for_claim": "false",
    },
    {
        "impact_id": "I2_parent_contract",
        "route": "future parent action",
        "what_is_earned": "a finite list of conditions that would promote Qcoh from closure to theorem",
        "what_is_not_earned": "the parent action itself",
        "alpha3_effect": "fill or derive rows before PPN/Newton/local-GR language",
        "valid_for_claim": "false",
    },
    {
        "impact_id": "I3_closure_policy",
        "route": "labelled Qcoh closure",
        "what_is_earned": "usable private theorem target and possible empirical closure branch",
        "what_is_not_earned": "derived GR reduction",
        "alpha3_effect": "closure cannot count as solar-system evidence",
        "valid_for_claim": "false",
    },
]


DECISION_ROWS = [
    {
        "decision_id": "D0_algebra",
        "status": "partial_pass",
        "meaning": "the coherent trace projector is mathematically fixed and removes STF/shear leakage if used",
        "next_action": "keep P_coh=(1/3)hh as the only admissible coherent projector candidate",
    },
    {
        "decision_id": "D1_parent_ownership",
        "status": "not_derived",
        "meaning": "the corpus does not yet show the parent action forces P_coh, chi_D, and local X_D=0",
        "next_action": "write parent action clause or demote Qcoh route to labelled closure",
    },
    {
        "decision_id": "D2_alpha3",
        "status": "not_scoreable",
        "meaning": "Qcoh algebra does not fill W_domain_alpha3 epsilon_domain_flux or prove it zero",
        "next_action": "use 480 template or derive parent zero certificate",
    },
    {
        "decision_id": "D3_local_GR",
        "status": "forbidden",
        "meaning": "no PPN, Newtonian-limit, or local-GR promotion follows from this checkpoint",
        "next_action": NEXT_TARGET,
    },
]


ROUTE_UPDATE_ROWS = [
    {
        "route_id": "QCOH_trace_projector",
        "target": "raw determinant shear leak",
        "accepted": "partial_algebra_only",
        "why_not_full": "P_coh algebra is clean but not parent-owned",
        "next_action": "parent action ownership or closure label",
    },
    {
        "route_id": "QCOH_domain_alpha3",
        "target": "W_domain_alpha3 epsilon_domain_flux",
        "accepted": "false",
        "why_not_full": "requires parent-selected local trivial X_D=0, R11 silence, and stress accounting",
        "next_action": "fill 480 templates or derive theorem-zero certificate",
    },
    {
        "route_id": "QCOH_GR_Newton",
        "target": "derived local GR/Newton branch",
        "accepted": "false",
        "why_not_full": "algebra alone does not prove Bianchi conservation, measured-GM normalization, or PPN silence",
        "next_action": NEXT_TARGET,
    },
]


def source_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for source in SOURCE_REGISTER:
        path = ROOT / source["source_file"]
        rows.append(
            {
                "source_file": source["source_file"],
                "exists": str(path.exists()),
                "role": source["role"],
            }
        )
    return rows


def validation_rows(source_register: list[dict[str, str]]) -> list[dict[str, str]]:
    missing_sources = [row["source_file"] for row in source_register if row["exists"] != "True"]
    claim_valid_count = sum(1 for row in ALPHA3_IMPACT_ROWS if row["valid_for_claim"] == "true")
    return [
        {
            "rule_id": "V481_0_sources",
            "rule": "all cited source paths exist",
            "result": "pass" if not missing_sources else "fail",
            "evidence": f"missing_sources={len(missing_sources)}",
            "claim_effect": "traceability only",
        },
        {
            "rule_id": "V481_1_projector_algebra",
            "rule": "P_coh is idempotent, self-adjoint, and unique in the scalar trace sector",
            "result": "pass",
            "evidence": "A1/A2 algebra rows",
            "claim_effect": "projector candidate narrowed",
        },
        {
            "rule_id": "V481_2_shear_exclusion",
            "rule": "using det_h(P_coh Q) removes trace-free determinant leakage",
            "result": "conditional_pass",
            "evidence": "A3 algebra row",
            "claim_effect": "raw det(Q) remains forbidden; projected det is allowed as candidate",
        },
        {
            "rule_id": "V481_3_parent_ownership",
            "rule": "parent action forces P_coh, chi_D, local X_D=0, and stress accounting",
            "result": "fail_for_claim",
            "evidence": "C0-C4 all valid_for_local_GR_claim=false",
            "claim_effect": "Qcoh route remains closure/theorem target",
        },
        {
            "rule_id": "V481_4_alpha3_no_promotion",
            "rule": "no alpha3 impact row is claim-valid",
            "result": "pass",
            "evidence": f"claim_valid_rows={claim_valid_count}",
            "claim_effect": "no alpha3/PPN/local-GR pass",
        },
        {
            "rule_id": "V481_5_next_route",
            "rule": "failure is routed to numeric/domain residual vector rather than hidden promotion",
            "result": "pass",
            "evidence": NEXT_TARGET,
            "claim_effect": "local residual vector remains retained",
        },
    ]


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = list(rows[0].keys()) if rows else []
    with (ROOT / path).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def markdown_table(rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> str:
    if not rows:
        return ""
    if fieldnames is None:
        fieldnames = list(rows[0].keys())
    lines = [
        "| " + " | ".join(fieldnames) + " |",
        "| " + " | ".join("---" for _ in fieldnames) + " |",
    ]
    for row in rows:
        values = [str(row.get(fieldname, "")).replace("\n", " ") for fieldname in fieldnames]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def build_doc(
    timestamp: str,
    generated_at_utc: str,
    run_dir: Path,
    source_register: list[dict[str, str]],
    validations: list[dict[str, str]],
) -> str:
    return f"""# 481 - Qcoh Parent Projector Algebra Or Closure

Private Qcoh/projector checkpoint. This is not a public alpha3 pass, mu_extra-zero pass, Newtonian-limit pass, PPN pass, local-GR derivation, cosmology result, EM result, or unified-field claim.

## 1. Purpose

Checkpoint `480` left alpha3 in the honest state:

```text
fill W_boundary_alpha3 * epsilon_boundary_flux,
fill W_domain_alpha3 * epsilon_domain_flux,
or prove the relevant parent theorem-zero identities.
```

This checkpoint attacks the best derivation clue before falling back to numeric closure:

```text
Can Q_coh/P_coh be made into a parent-owned coherent projector rather than an inserted smoothing rule?
```

Short answer:

```text
The trace-projector algebra is clean.
The parent-action ownership is still missing.
So Q_coh is sharpened into an exact parent-action contract, not promoted.
```

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/Qcoh_parent_projector_algebra_or_closure.py` |
| Run directory | `{run_dir.relative_to(ROOT)}` |
| Timestamp | `{timestamp}` |
| Generated UTC | `{generated_at_utc}` |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## 3. Source Register

{markdown_table(source_register)}

## 4. Algebra Theorem Attempt

{markdown_table(ALGEBRA_ROWS)}

The useful theorem-level piece is:

```text
(P_coh Q)_mu_nu = (1/3) h_mu_nu h^ab Q_ab
```

and therefore:

```text
det_h(P_coh Q) = (Tr_h Q / 3)^3.
```

That is not nothing. It means the route does not need an arbitrary smoothing operator. The coherent scalar projector is fixed by local spatial isotropy.

But it is still only useful for physics if the parent action forces the local branch into that scalar sector before fitting.

## 5. Parent Action Contract

{markdown_table(PARENT_CONTRACT_ROWS)}

This is the exact contract a future parent action must satisfy:

```text
S_parent must contain or imply Q_mu_nu, P_coh, and chi_D such that:

1. Q_mu_nu is a variational/noether load variable.
2. P_coh=(1/3)hh is forced by local symmetry, Ward identity, or Euler constraint.
3. chi_D is selected variationally/topologically, not by hand.
4. compact local vacuum gives X_D=Tr_h Q_D=0 through PPN order.
5. FLRW/cosmological domains remain active.
6. delta_g P_coh and delta_g chi_D vanish/topologically cancel or are retained.
7. R11/source-normalization rows are theorem-zero or numerically scored.
```

If any of those fail, Qcoh remains a closure/theorem target, not a local-GR derivation.

## 6. Alpha3 Impact

{markdown_table(ALPHA3_IMPACT_ROWS)}

The strict alpha3 position after this checkpoint is:

```text
P_coh trace algebra helps remove the shear-leak objection.
It does not prove W_domain_alpha3 * epsilon_domain_flux = 0.
```

So checkpoint `480` remains live.

## 7. Route Update

{markdown_table(ROUTE_UPDATE_ROWS)}

## 8. Validation

{markdown_table(validations)}

## 9. Decision

{markdown_table(DECISION_ROWS)}

## 10. Claim Ceiling

Allowed:

```text
The coherent projector candidate is now fixed: it must be the trace projector P_coh=(1/3)hh.
Projected determinant det_h(P_coh Q) removes raw trace-free shear leakage and gives a cubic/double-zero shape if X_D is parent-forced to zero.
```

Forbidden:

```text
MTS has derived Q_coh from the parent action.
MTS has proved local X_D=0.
MTS has proved W_domain_alpha3 epsilon_domain_flux=0.
MTS passes alpha3, PPN, Newton, or local GR.
```

## 11. Next Queue

| Priority | Target | Reason |
| --- | --- | --- |
| 1 | `{NEXT_TARGET}` | propagate retained domain/source rows into the local residual vector so the local-GR failure mode is explicit |
| 2 | `483-alpha3-product-evaluator-refresh.md` | rerun alpha3 evaluator only after theorem-zero certificates or numeric products are filled |
| 3 | parent-action derivation note | attempt the actual S_parent clause that forces Q, P_coh, chi_D, R11 silence, and X_D=0 |
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timestamp", default=datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S"))
    args = parser.parse_args()

    generated_at_utc = datetime.now(timezone.utc).isoformat()
    run_dir = ROOT / "runs" / f"{args.timestamp}-Qcoh-parent-projector-algebra-or-closure"
    run_dir.mkdir(parents=True, exist_ok=True)

    sources = source_rows()
    validations = validation_rows(sources)

    write_csv(SOURCE_REGISTER_PATH, sources)
    write_csv(ALGEBRA_THEOREM_PATH, ALGEBRA_ROWS)
    write_csv(PARENT_CONTRACT_PATH, PARENT_CONTRACT_ROWS)
    write_csv(ALPHA3_IMPACT_PATH, ALPHA3_IMPACT_ROWS)
    write_csv(VALIDATION_PATH, validations)
    write_csv(DECISION_PATH, DECISION_ROWS)
    write_csv(ROUTE_UPDATE_PATH, ROUTE_UPDATE_ROWS)

    doc = build_doc(args.timestamp, generated_at_utc, run_dir, sources, validations)
    (ROOT / DOC_PATH).write_text(doc, encoding="utf-8")

    missing_sources = [row["source_file"] for row in sources if row["exists"] != "True"]
    status = {
        "timestamp": args.timestamp,
        "generated_at_utc": generated_at_utc,
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "checkpoint_doc": str(DOC_PATH),
        "run_dir": str(run_dir),
        "source_register": str(ROOT / SOURCE_REGISTER_PATH),
        "algebra_theorem": str(ROOT / ALGEBRA_THEOREM_PATH),
        "parent_contract": str(ROOT / PARENT_CONTRACT_PATH),
        "alpha3_impact": str(ROOT / ALPHA3_IMPACT_PATH),
        "validation": str(ROOT / VALIDATION_PATH),
        "decision": str(ROOT / DECISION_PATH),
        "route_update": str(ROOT / ROUTE_UPDATE_PATH),
        "source_rows": len(sources),
        "source_paths_missing": len(missing_sources),
        "missing_sources": missing_sources,
        "algebra_rows": len(ALGEBRA_ROWS),
        "parent_contract_rows": len(PARENT_CONTRACT_ROWS),
        "alpha3_impact_rows": len(ALPHA3_IMPACT_ROWS),
        "validation_rows": len(validations),
        "decision_rows": len(DECISION_ROWS),
        "route_update_rows": len(ROUTE_UPDATE_ROWS),
        "trace_projector_algebra_passed": True,
        "raw_det_shear_leak_excluded_if_projected": True,
        "parent_action_ownership_passed": False,
        "domain_selector_ownership_passed": False,
        "local_XD_zero_derived": False,
        "R11_silence_passed": False,
        "alpha3_passed": False,
        "mu_extra_zero_promoted": False,
        "Newtonian_reduction_promoted": False,
        "PPN_promoted": False,
        "local_GR_claim_allowed": False,
        "closure_retained": True,
        "next_target": NEXT_TARGET,
    }
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
