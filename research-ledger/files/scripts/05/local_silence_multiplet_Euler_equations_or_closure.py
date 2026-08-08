from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

STATUS = "local_silence_multiplet_Euler_no_source_theorem_written_sources_and_boundary_not_parent_derived_no_Newton_PPN_or_local_GR_pass"
CLAIM_CEILING = "conditional_positive_Euler_no_source_theorem_only_Yloc_sources_not_zeroed_no_EH_R11_Newton_PPN_or_local_GR_promotion"
NEXT_TARGET = "490-Yloc-source-current-Noether-zero-or-closure-fill.md"

DOC_PATH = Path("489-local-silence-multiplet-Euler-equations-or-closure.md")
SOURCE_REGISTER_PATH = Path("source-intake/mts_residuals/P8_YLOC_EULER_SOURCE_REGISTER.csv")
EULER_SYSTEM_PATH = Path("source-intake/mts_residuals/P8_YLOC_EULER_SYSTEM.csv")
NO_SOURCE_THEOREM_PATH = Path("source-intake/mts_residuals/P8_YLOC_NO_SOURCE_THEOREM.csv")
SOURCE_DEBT_PATH = Path("source-intake/mts_residuals/P8_YLOC_SOURCE_DEBT_LEDGER.csv")
VALIDATION_PATH = Path("source-intake/mts_residuals/P8_YLOC_EULER_VALIDATION.csv")
DECISION_PATH = Path("source-intake/mts_residuals/P8_YLOC_EULER_DECISION.csv")
ROUTE_UPDATE_PATH = Path("source-intake/mts_residuals/P8_YLOC_EULER_ROUTE_UPDATE.csv")

PARENT_CLAUSE_PATH = Path("source-intake/mts_residuals/P8_DOUBLE_ZERO_R11_PARENT_CLAUSE.csv")
VARIATION_PROOF_PATH = Path("source-intake/mts_residuals/P8_DOUBLE_ZERO_R11_VARIATION_PROOF.csv")
LOCAL_VECTOR_PATH = Path("source-intake/mts_residuals/P8_LOCAL_GR_RESIDUAL_VECTOR_FROM_DOMAIN_SOURCE.csv")


SOURCE_REGISTER = [
    {
        "source_file": "488-double-zero-R11-selector-parent-clause-or-demotion.md",
        "role": "composite squared selector and Y_loc parent-clause target",
    },
    {
        "source_file": "487-local-EH-R11-selector-theorem-attempt.md",
        "role": "double-zero sufficiency lemma",
    },
    {
        "source_file": "485-boundary-no-flux-and-R11-silence-from-local-zero.md",
        "role": "boundary/R11/stress shortcut rejection",
    },
    {
        "source_file": "482-local-residual-vector-from-domain-source-fill.md",
        "role": "active local residual vector",
    },
    {
        "source_file": str(PARENT_CLAUSE_PATH),
        "role": "Y_loc and Sigma_loc parent-clause rows",
    },
    {
        "source_file": str(VARIATION_PROOF_PATH),
        "role": "delta Sigma_loc proof rows from 488",
    },
    {
        "source_file": str(LOCAL_VECTOR_PATH),
        "role": "local residual components to be controlled by Y_loc",
    },
    {
        "source_file": "scripts/local_silence_multiplet_Euler_equations_or_closure.py",
        "role": "this checkpoint generator",
    },
]


EULER_SYSTEM_ROWS = [
    {
        "component_id": "Y0_trace_expansion",
        "Y_component": "X_D",
        "candidate_Euler_equation": "L_X X_D = J_X with L_X positive on compact local domain",
        "zero_conditions": "J_X=0 and boundary flux n.grad X_D=0",
        "would_clear": "coherent trace-load source",
        "current_status": "conditional_partial_from_484",
        "valid_for_claim": "false",
    },
    {
        "component_id": "Y1_coherent_projector",
        "Y_component": "Qcoh_D - h X_D/3",
        "candidate_Euler_equation": "algebraic/constraint equation plus positive STF penalty for non-trace modes",
        "zero_conditions": "trace projector owned and STF source current zero",
        "would_clear": "LRV_QCOH_PROJECTOR_OWNERSHIP",
        "current_status": "partial_clause_stress_open",
        "valid_for_claim": "false",
    },
    {
        "component_id": "Y2_boundary_flux",
        "Y_component": "Phi_boundary^i=P_loc^i_nu n_mu K_boundary^{mu nu}",
        "candidate_Euler_equation": "boundary/collar elliptic equation L_B Phi^i = J_B^i",
        "zero_conditions": "J_B^i=0 and scalar stationary boundary no-flux/no-marker conditions",
        "would_clear": "LRV_BOUNDARY_R7_ALPHA3",
        "current_status": "not_parent_derived",
        "valid_for_claim": "false",
    },
    {
        "component_id": "Y3_domain_vector",
        "Y_component": "V_domain^i",
        "candidate_Euler_equation": "L_V V_domain^i = J_V^i",
        "zero_conditions": "domain selector carries no vector/preferred-frame source",
        "would_clear": "LRV_DOMAIN_R5_ALPHA1;LRV_DOMAIN_R6_ALPHA2;LRV_DOMAIN_R7_ALPHA3",
        "current_status": "not_parent_derived",
        "valid_for_claim": "false",
    },
    {
        "component_id": "Y4_domain_STF_stress",
        "Y_component": "S_TF_domain^{ij}",
        "candidate_Euler_equation": "L_S S_TF^{ij}=J_S^{ij}",
        "zero_conditions": "projector/domain stress is topological or isotropic trace-only",
        "would_clear": "LRV_DOMAIN_R8_XI;LRV_PROJECTOR_STRESS_ACCOUNTING",
        "current_status": "retained_debt",
        "valid_for_claim": "false",
    },
    {
        "component_id": "Y5_source_normalization",
        "Y_component": "Delta_mu_source",
        "candidate_Euler_equation": "L_mu Delta_mu = J_mu",
        "zero_conditions": "measured-GM source current is constant and no derivative/range/species leakage",
        "would_clear": "LRV_DOMAIN_R11_SOURCE_NORMALIZATION",
        "current_status": "not_parent_derived",
        "valid_for_claim": "false",
    },
    {
        "component_id": "Y6_stress_Bianchi",
        "Y_component": "nabla_mu T_extra^{mu nu}",
        "candidate_Euler_equation": "Ward identity plus retained-stress conservation equation",
        "zero_conditions": "all extra stresses vanish/topological or are conserved below PPN bounds",
        "would_clear": "LRV_PROJECTOR_STRESS_ACCOUNTING;LRV_TOTAL_ALPHA3_GUARD",
        "current_status": "retained_debt",
        "valid_for_claim": "false",
    },
]


NO_SOURCE_THEOREM_ROWS = [
    {
        "step_id": "N0_positive_operator",
        "statement": "Each Y component has a positive local quadratic action on the compact local branch.",
        "math_form": "S_Y=1/2 int_D sqrt(h)[(nabla Y)^2 + m_Y^2 Y^2] plus controlled boundary term",
        "result": "sufficient_condition",
        "valid_for_claim": "false",
    },
    {
        "step_id": "N1_Euler_equation",
        "statement": "Variation gives a local elliptic equation with source and boundary terms.",
        "math_form": "(-Delta_D + m_Y^2)Y = J_Y, with boundary n.grad Y = B_Y",
        "result": "formal_candidate",
        "valid_for_claim": "false",
    },
    {
        "step_id": "N2_integral_identity",
        "statement": "Multiply by Y and integrate over D.",
        "math_form": "int_D[(nabla Y)^2+m_Y^2Y^2]=int_D Y J_Y + int_boundary Y B_Y",
        "result": "energy_identity",
        "valid_for_claim": "false",
    },
    {
        "step_id": "N3_zero_theorem",
        "statement": "If J_Y=0 and B_Y=0 and the operator is positive, then Y=0.",
        "math_form": "left side nonnegative and equals zero, so Y=0 componentwise",
        "result": "conditional_no_source_theorem",
        "valid_for_claim": "false",
    },
    {
        "step_id": "N4_current_corpus",
        "statement": "The current corpus does not yet derive J_Y=0 and B_Y=0 for every component.",
        "math_form": "boundary/domain/R11/stress source currents remain open",
        "result": "fails_for_claim",
        "valid_for_claim": "false",
    },
]


SOURCE_DEBT_ROWS = [
    {
        "debt_id": "S0_boundary_source",
        "source_or_boundary": "J_B^i or B_B^i",
        "missing_zero": "boundary scalar stationary marker-free Ward no-flux theorem",
        "fallback": "fill W_boundary_alpha3_epsilon_boundary_flux",
        "blocks": "LRV_BOUNDARY_R7_ALPHA3",
        "valid_for_claim": "false",
    },
    {
        "debt_id": "S1_domain_vector_source",
        "source_or_boundary": "J_V^i",
        "missing_zero": "domain selector no-vector Euler theorem",
        "fallback": "fill alpha1/alpha2/alpha3 domain vector products",
        "blocks": "LRV_DOMAIN_R5_ALPHA1;LRV_DOMAIN_R6_ALPHA2;LRV_DOMAIN_R7_ALPHA3",
        "valid_for_claim": "false",
    },
    {
        "debt_id": "S2_domain_STF_source",
        "source_or_boundary": "J_S^{ij}",
        "missing_zero": "projector/domain STF stress zero or topological stress theorem",
        "fallback": "fill xi and retained-stress residual rows",
        "blocks": "LRV_DOMAIN_R8_XI;LRV_PROJECTOR_STRESS_ACCOUNTING",
        "valid_for_claim": "false",
    },
    {
        "debt_id": "S3_source_normalization_current",
        "source_or_boundary": "J_mu",
        "missing_zero": "constant measured-GM/source-normalization Noether theorem",
        "fallback": "fill c_domain_source_normalization_operator and R11 source rows",
        "blocks": "LRV_DOMAIN_R11_SOURCE_NORMALIZATION",
        "valid_for_claim": "false",
    },
    {
        "debt_id": "S4_Bianchi_stress_current",
        "source_or_boundary": "nabla_mu T_extra^{mu nu}",
        "missing_zero": "full Ward/Bianchi stress ledger",
        "fallback": "retain and score T_extra residual vector",
        "blocks": "LRV_PROJECTOR_STRESS_ACCOUNTING;LRV_TOTAL_ALPHA3_GUARD",
        "valid_for_claim": "false",
    },
]


DECISION_ROWS = [
    {
        "decision_id": "D0_no_source_theorem",
        "status": "conditional_theorem_written",
        "meaning": "positive local Euler equations plus zero source/boundary currents force Y_loc=0",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D1_current_derivation",
        "status": "source_currents_not_zeroed",
        "meaning": "the current corpus does not yet derive the required J_Y=0 and B_Y=0 conditions",
        "next_action": "derive Noether/source-current zeros or fill closure rows",
    },
    {
        "decision_id": "D2_R11_selector",
        "status": "still_conditional",
        "meaning": "Sigma_loc double-zero suppression works only if the no-source theorem supplies Y_loc=0",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D3_promotion",
        "status": "forbidden",
        "meaning": "no EH-only, R11 silence, Newton, PPN, alpha3, mu_extra-zero, or local-GR pass is earned",
        "next_action": "do not claim; continue source-current theorem or closure fill",
    },
]


ROUTE_UPDATE_ROWS = [
    {
        "route_id": "YLOC_EULER",
        "previous_status": "Yloc_Euler_equations_missing",
        "new_status": "positive_no_source_theorem_written_sources_open",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "DOUBLE_ZERO_R11_SELECTOR",
        "previous_status": "composite_squared_parent_clause_candidate",
        "new_status": "requires_Yloc_source_current_zero",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "LOCAL_GR",
        "previous_status": "blocked_but_factorization_route_sharpened",
        "new_status": "blocked_by_source_current_and_boundary_terms",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
]


def read_csv(path: Path) -> list[dict[str, str]]:
    full_path = ROOT / path
    if not full_path.exists():
        return []
    with full_path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def source_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for row in SOURCE_REGISTER:
        exists = (ROOT / row["source_file"]).exists()
        rows.append({**row, "exists": str(exists)})
    return rows


def validation_rows(sources: list[dict[str, str]]) -> list[dict[str, str]]:
    missing_sources = [row for row in sources if row["exists"] != "True"]
    parent_rows = read_csv(PARENT_CLAUSE_PATH)
    local_vector_rows = read_csv(LOCAL_VECTOR_PATH)
    parent_has_Y = any(row.get("clause_id") == "C0_local_silence_multiplet" for row in parent_rows)
    required_components = {
        "LRV_BOUNDARY_R7_ALPHA3",
        "LRV_DOMAIN_R11_SOURCE_NORMALIZATION",
        "LRV_PROJECTOR_STRESS_ACCOUNTING",
    }
    vector_components = {row.get("component_id", "") for row in local_vector_rows}
    claim_euler_rows = [row for row in EULER_SYSTEM_ROWS if row["valid_for_claim"] == "true"]
    claim_source_debts = [row for row in SOURCE_DEBT_ROWS if row["valid_for_claim"] == "true"]

    return [
        {
            "rule_id": "V489_0_sources",
            "rule": "all cited source paths exist",
            "result": "pass" if not missing_sources else "fail",
            "evidence": f"missing_sources={len(missing_sources)}",
            "claim_effect": "traceability only",
        },
        {
            "rule_id": "V489_1_Yloc_loaded",
            "rule": "488 Y_loc parent-clause row is loaded",
            "result": "pass" if parent_has_Y else "fail",
            "evidence": "C0_local_silence_multiplet",
            "claim_effect": "Euler attempt is tied to the selector clause",
        },
        {
            "rule_id": "V489_2_residual_coverage",
            "rule": "Euler/source debt rows cover active local blockers",
            "result": "pass" if required_components.issubset(vector_components) else "fail",
            "evidence": ";".join(sorted(required_components & vector_components)),
            "claim_effect": "targets real local-GR blockers",
        },
        {
            "rule_id": "V489_3_no_source_theorem_written",
            "rule": "positive operator/no-source integral theorem is explicit",
            "result": "pass",
            "evidence": "N0_positive_operator;N2_integral_identity;N3_zero_theorem",
            "claim_effect": "conditional derivation path sharpened",
        },
        {
            "rule_id": "V489_4_no_claim_euler_rows",
            "rule": "no Y_loc Euler row is promoted as derived",
            "result": "pass" if not claim_euler_rows else "fail",
            "evidence": f"claim_valid_euler_rows={len(claim_euler_rows)}",
            "claim_effect": "no fake Y=0 theorem",
        },
        {
            "rule_id": "V489_5_no_claim_source_rows",
            "rule": "no source-current debt row is claim-valid before Noether/source proof",
            "result": "pass" if not claim_source_debts else "fail",
            "evidence": f"claim_valid_source_debt_rows={len(claim_source_debts)}",
            "claim_effect": "no local-GR promotion",
        },
    ]


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> None:
    if fieldnames is None:
        fieldnames = list(rows[0].keys()) if rows else []
    out = ROOT / path
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="", encoding="utf-8") as handle:
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


def build_doc(timestamp: str, generated_at_utc: str, run_dir: Path, sources: list[dict[str, str]], validations: list[dict[str, str]]) -> str:
    return f"""# 489 - Local Silence Multiplet Euler Equations Or Closure

Private local-GR/Newton/PPN Euler-equation checkpoint. This is not a public EH-only proof, R11 pass, alpha3 pass, mu_extra-zero pass, Newtonian-limit pass, PPN pass, local-GR derivation, cosmology result, EM result, or unified-field claim.

## 1. Purpose

Checkpoint `488` made the R11 selector less artificial:

```text
Sigma_loc = G_AB Y_loc^A Y_loc^B.
```

That works only if the parent equations actually drive:

```text
Y_loc^A = 0
```

in compact local domains.

This checkpoint writes the exact Euler/no-source theorem that would do it.

Short answer:

```text
conditional theorem written:
positive local Euler operator + zero source current + zero boundary flux => Y_loc^A=0.

not derived yet:
the current corpus does not prove all Y_loc source currents and boundary terms vanish.
```

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/local_silence_multiplet_Euler_equations_or_closure.py` |
| Run directory | `{run_dir.relative_to(ROOT)}` |
| Timestamp | `{timestamp}` |
| Generated UTC | `{generated_at_utc}` |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## 3. Source Register

{markdown_table(sources)}

## 4. Candidate Euler System

{markdown_table(EULER_SYSTEM_ROWS)}

## 5. No-Source Theorem

{markdown_table(NO_SOURCE_THEOREM_ROWS)}

The core proof is the standard positive-operator identity:

```text
(-Delta_D + m_Y^2)Y = J_Y,
n.grad Y = B_Y,
```

multiply by `Y` and integrate:

```text
int_D[(nabla Y)^2 + m_Y^2 Y^2]
= int_D Y J_Y + int_boundary Y B_Y.
```

If:

```text
J_Y=0,
B_Y=0,
m_Y^2>0,
```

then:

```text
Y=0.
```

That is the clean route to `Sigma_loc=0`.

## 6. Source Debt Ledger

{markdown_table(SOURCE_DEBT_ROWS)}

## 7. Validation

{markdown_table(validations)}

## 8. Decision

{markdown_table(DECISION_ROWS)}

## 9. Route Update

{markdown_table(ROUTE_UPDATE_ROWS)}

## 10. Claim Ceiling

Allowed:

```text
The Euler/no-source theorem for Y_loc=0 is now explicit.
If all Y_loc source currents and boundary terms vanish, the double-zero selector route can work.
```

Forbidden:

```text
MTS has derived Y_loc=0.
MTS has derived EH-only/R11 silence.
MTS has derived Newtonian recovery or PPN recovery.
MTS has alpha3=0 or mu_extra=0.
```

## 11. Next Queue

| Priority | Target | Reason |
| --- | --- | --- |
| 1 | `{NEXT_TARGET}` | derive or reject J_Y=0 and B_Y=0 from Noether/Ward/source-current identities |
| 2 | closure fill pack | if source currents remain nonzero or unowned |
| 3 | local PPN residual certificate | only after Yloc/R11/boundary/stress rows are zero/bounded |
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timestamp", default=datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S"))
    args = parser.parse_args()

    generated_at_utc = datetime.now(timezone.utc).isoformat()
    run_dir = ROOT / "runs" / f"{args.timestamp}-local-silence-multiplet-Euler-equations-or-closure"
    run_dir.mkdir(parents=True, exist_ok=True)

    sources = source_rows()
    validations = validation_rows(sources)

    write_csv(SOURCE_REGISTER_PATH, sources)
    write_csv(EULER_SYSTEM_PATH, EULER_SYSTEM_ROWS)
    write_csv(NO_SOURCE_THEOREM_PATH, NO_SOURCE_THEOREM_ROWS)
    write_csv(SOURCE_DEBT_PATH, SOURCE_DEBT_ROWS)
    write_csv(VALIDATION_PATH, validations)
    write_csv(DECISION_PATH, DECISION_ROWS)
    write_csv(ROUTE_UPDATE_PATH, ROUTE_UPDATE_ROWS)

    doc = build_doc(args.timestamp, generated_at_utc, run_dir, sources, validations)
    (ROOT / DOC_PATH).write_text(doc, encoding="utf-8")

    missing_sources = [row["source_file"] for row in sources if row["exists"] != "True"]
    failed_validations = [row for row in validations if row["result"] == "fail"]
    claim_euler_rows = [row for row in EULER_SYSTEM_ROWS if row["valid_for_claim"] == "true"]
    claim_source_debts = [row for row in SOURCE_DEBT_ROWS if row["valid_for_claim"] == "true"]
    status = {
        "timestamp": args.timestamp,
        "generated_at_utc": generated_at_utc,
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "checkpoint_doc": str(DOC_PATH),
        "run_dir": str(run_dir),
        "source_register": str(ROOT / SOURCE_REGISTER_PATH),
        "euler_system": str(ROOT / EULER_SYSTEM_PATH),
        "no_source_theorem": str(ROOT / NO_SOURCE_THEOREM_PATH),
        "source_debt": str(ROOT / SOURCE_DEBT_PATH),
        "validation": str(ROOT / VALIDATION_PATH),
        "decision": str(ROOT / DECISION_PATH),
        "route_update": str(ROOT / ROUTE_UPDATE_PATH),
        "source_rows": len(sources),
        "source_paths_missing": len(missing_sources),
        "missing_sources": missing_sources,
        "euler_system_rows": len(EULER_SYSTEM_ROWS),
        "no_source_theorem_rows": len(NO_SOURCE_THEOREM_ROWS),
        "source_debt_rows": len(SOURCE_DEBT_ROWS),
        "failed_validation_rows": len(failed_validations),
        "claim_valid_euler_rows": len(claim_euler_rows),
        "claim_valid_source_debt_rows": len(claim_source_debts),
        "positive_no_source_theorem_written": True,
        "Yloc_Euler_equations_derived": False,
        "Yloc_source_currents_zeroed": False,
        "boundary_terms_zeroed": False,
        "R11_silence_derived": False,
        "source_normalized_Newton_promoted": False,
        "PPN_promoted": False,
        "alpha3_passed": False,
        "mu_extra_zero_promoted": False,
        "local_GR_claim_allowed": False,
        "next_target": NEXT_TARGET,
    }
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
