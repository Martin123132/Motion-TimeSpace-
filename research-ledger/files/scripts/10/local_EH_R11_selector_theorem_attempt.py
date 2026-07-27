from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

STATUS = "local_EH_R11_selector_theorem_attempt_written_double_zero_sufficiency_lemma_operator_rows_not_selected_no_Newton_PPN_or_local_GR_pass"
CLAIM_CEILING = "conditional_double_zero_R11_selector_lemma_only_actual_R11_rows_not_parent_selected_no_EH_R11_Newton_PPN_or_local_GR_promotion"
NEXT_TARGET = "488-double-zero-R11-selector-parent-clause-or-demotion.md"

DOC_PATH = Path("487-local-EH-R11-selector-theorem-attempt.md")
SOURCE_REGISTER_PATH = Path("source-intake/mts_residuals/P8_LOCAL_EH_R11_SOURCE_REGISTER.csv")
SELECTOR_LEMMA_PATH = Path("source-intake/mts_residuals/P8_LOCAL_EH_R11_SELECTOR_LEMMA.csv")
OPERATOR_AUDIT_PATH = Path("source-intake/mts_residuals/P8_LOCAL_EH_R11_OPERATOR_AUDIT.csv")
LEAK_TESTS_PATH = Path("source-intake/mts_residuals/P8_LOCAL_EH_R11_LEAK_TESTS.csv")
VALIDATION_PATH = Path("source-intake/mts_residuals/P8_LOCAL_EH_R11_VALIDATION.csv")
DECISION_PATH = Path("source-intake/mts_residuals/P8_LOCAL_EH_R11_DECISION.csv")
ROUTE_UPDATE_PATH = Path("source-intake/mts_residuals/P8_LOCAL_EH_R11_ROUTE_UPDATE.csv")

R11_VECTOR_PATH = Path("source-intake/mts_residuals/R11_nonEH_operator_vector_executable.csv")
THEOREM_STACK_PATH = Path("source-intake/mts_residuals/P8_R11_BOUNDARY_STRESS_THEOREM_STACK.csv")
CLOSURE_FILL_PACK_PATH = Path("source-intake/mts_residuals/P8_R11_BOUNDARY_STRESS_CLOSURE_FILL_PACK.csv")


SOURCE_REGISTER = [
    {
        "source_file": "463-EH-only-or-R11-executable-vector-gate.md",
        "role": "EH-only versus R11 fork and ten operator-family ledger",
    },
    {
        "source_file": "464-R11-executable-vector-minimum-fill-skeleton.md",
        "role": "minimum R11 skeleton and missing-field validation rules",
    },
    {
        "source_file": "486-R11-boundary-stress-theorem-or-closure-fill-pack.md",
        "role": "local EH/R11 selector theorem target and closure fill pack",
    },
    {
        "source_file": "484-parent-local-zero-action-clause-attempt.md",
        "role": "local-zero input X=nabla.u and Qcoh=hX/3",
    },
    {
        "source_file": "485-boundary-no-flux-and-R11-silence-from-local-zero.md",
        "role": "proof that X_D=0 alone does not imply R11 silence",
    },
    {
        "source_file": str(R11_VECTOR_PATH),
        "role": "actual R11 operator-family rows to audit",
    },
    {
        "source_file": str(THEOREM_STACK_PATH),
        "role": "T3 local EH/R11 selector theorem target",
    },
    {
        "source_file": str(CLOSURE_FILL_PACK_PATH),
        "role": "F5 R11 source-normalization fill row",
    },
    {
        "source_file": "scripts/local_EH_R11_selector_theorem_attempt.py",
        "role": "this checkpoint generator",
    },
]


SELECTOR_LEMMA_ROWS = [
    {
        "lemma_id": "L0_branch_variable",
        "statement": "Let Z be the compact-local silence variable built from X_D, Qcoh_D, and any parent-owned local-zero invariants.",
        "math_condition": "Z=0 on the stationary compact comoving local branch",
        "result": "input_condition",
        "claim_status": "conditional_from_484",
        "valid_for_claim": "false",
    },
    {
        "lemma_id": "L1_single_zero_fails",
        "statement": "A non-EH term multiplied only by F(Z)=Z is not safely silent under variation.",
        "math_condition": "delta(F O)=F delta O + F_prime O delta Z; at Z=0 gives F_prime(0) O delta Z",
        "result": "leaks_if_F_prime_0_nonzero",
        "claim_status": "proved_as_warning",
        "valid_for_claim": "false",
    },
    {
        "lemma_id": "L2_double_zero_sufficient",
        "statement": "A non-EH term multiplied by a parent-owned double-zero selector is locally silent to first variation.",
        "math_condition": "F(0)=0 and F_prime(0)=0, with O finite and no independent multiplier stress",
        "result": "delta(F O)=0 on Z=0 branch",
        "claim_status": "conditional_sufficiency_lemma",
        "valid_for_claim": "false",
    },
    {
        "lemma_id": "L3_topological_escape",
        "statement": "A non-EH term may be harmless if it is exactly topological or pure boundary scalar with closed no-flux variation.",
        "math_condition": "delta_g S_top=0 in the local collar, or boundary scalar stress is trace-only and flux-closed",
        "result": "conditional_silence_route",
        "claim_status": "conditional_not_parent_global",
        "valid_for_claim": "false",
    },
    {
        "lemma_id": "L4_selector_theorem_target",
        "statement": "Local EH/R11 silence follows if every retained non-EH family is absent, double-zero selected by Z, or topological/boundary-silent.",
        "math_condition": "S_parent = S_EH + sum_A F_A(Z) O_A + S_top with F_A(0)=F_A_prime(0)=0",
        "result": "sufficient_but_not_shown_for_actual_R11_rows",
        "claim_status": "theorem_target_written",
        "valid_for_claim": "false",
    },
]


LEAK_TEST_ROWS = [
    {
        "test_id": "K0_constant_coefficient",
        "operator_form": "c O[g]",
        "selector_condition": "c independent of Z",
        "variation_result": "c delta O survives",
        "verdict": "fails_local_EH_selector",
    },
    {
        "test_id": "K1_single_zero",
        "operator_form": "Z O[g]",
        "selector_condition": "F(0)=0 but F_prime(0)=1",
        "variation_result": "O delta Z survives at Z=0",
        "verdict": "fails_unless_deltaZ_also_parent_zero",
    },
    {
        "test_id": "K2_double_zero",
        "operator_form": "Z^2 O[g]",
        "selector_condition": "F(0)=0 and F_prime(0)=0",
        "variation_result": "2Z O delta Z + Z^2 delta O = 0 at Z=0",
        "verdict": "passes_as_conditional_sufficient_class",
    },
    {
        "test_id": "K3_constraint_multiplier",
        "operator_form": "lambda Z",
        "selector_condition": "Z=0 on shell",
        "variation_result": "lambda delta Z can survive unless lambda=0 or eliminated",
        "verdict": "fails_without_multiplier_silence",
    },
    {
        "test_id": "K4_topological",
        "operator_form": "S_top",
        "selector_condition": "delta_g S_top=0 in local collar",
        "variation_result": "no bulk local operator if boundary variation is closed",
        "verdict": "passes_only_with_boundary_nohair",
    },
]


DECISION_ROWS = [
    {
        "decision_id": "D0_double_zero_lemma",
        "status": "conditional_sufficient_lemma_written",
        "meaning": "double-zero selector factors can silence non-EH operators to first variation on the local-zero branch",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D1_single_zero_policy",
        "status": "rejected",
        "meaning": "single-zero factors are not enough because first variation leaks",
        "next_action": "require F(0)=F_prime(0)=0 or another parent zero for every non-EH family",
    },
    {
        "decision_id": "D2_actual_R11_rows",
        "status": "not_selected",
        "meaning": "the current R11 rows do not yet show double-zero selector factors, topological silence, or claim-valid coefficients",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D3_promotion",
        "status": "forbidden",
        "meaning": "no EH-only, R11 silence, Newton, PPN, or local-GR pass is earned",
        "next_action": "attempt parent clause that forces the double-zero selector across R11 rows",
    },
]


ROUTE_UPDATE_ROWS = [
    {
        "route_id": "LOCAL_EH_R11_SELECTOR",
        "previous_status": "theorem_target_named",
        "new_status": "double_zero_sufficiency_lemma_written_actual_rows_unselected",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "R11_CLOSURE_FILL",
        "previous_status": "explicit_fill_pack_written",
        "new_status": "still_required_if_selector_not_parent_derived",
        "accepted_for_claim": "false",
        "next_target": "R11 coefficient fill after theorem route fails",
    },
    {
        "route_id": "LOCAL_GR",
        "previous_status": "blocked_by_boundary_R11_stress",
        "new_status": "blocked_but_factorization_route_sharpened",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
]


SELECTOR_REQUIREMENTS = {
    "boundary_topological_terms": "topological/boundary scalar no-hair or double-zero boundary selector",
    "R2_fR_scalar_mode": "double-zero coefficient c_R2(Z)=O(Z^2), infinite-mass/no-coupling theorem, or numeric R10/PPN bound",
    "Ricci_Weyl_squared": "topological Gauss-Bonnet combination or double-zero curvature-squared coefficient",
    "scalar_tensor_class_metric": "scalar/class field fixed with F_phi_C-constant and derivatives zero, or double-zero coupling",
    "vector_preferred_frame": "no-vector selector theorem or double-zero vector coefficient",
    "torsion_nonmetricity": "Levi-Civita/no-independent-connection theorem or double-zero torsion/nonmetricity coupling",
    "bulk_X_force_law": "source charge zero plus double-zero coupling or executable finite-range bound",
    "nonlocal_memory_kernel": "compact-local kernel silence or double-zero kernel norm",
    "source_normalization_operator": "measured-GM theorem or double-zero source-normalization coefficient",
    "projector_domain_stress": "topological/metric-independent projector or double-zero retained stress coefficient",
}


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


def operator_audit_rows() -> list[dict[str, str]]:
    rows = []
    for row in read_csv(R11_VECTOR_PATH):
        coefficient_value = row.get("coefficient_value", "")
        derivation_status = row.get("derivation_status", "")
        valid_for_claim = row.get("valid_for_claim", "false")
        text = " ".join(row.values())
        has_missing = "MISSING" in text
        has_double_zero = ("double-zero" in text.lower()) or ("O(Z^2)" in text)
        has_topological_escape = "topological" in text.lower() and "conditional" in text.lower()
        selector_requirement = SELECTOR_REQUIREMENTS.get(row.get("operator_family", ""), "double-zero selector or executable coefficient")
        if valid_for_claim == "true":
            selector_status = "claim_row_already_valid"
        elif has_double_zero:
            selector_status = "mentions_double_zero_not_claim_valid"
        elif has_topological_escape:
            selector_status = "conditional_topological_not_claim_valid"
        elif has_missing:
            selector_status = "missing_selector_or_coefficient"
        else:
            selector_status = "unselected_retained"
        rows.append(
            {
                "operator_family": row.get("operator_family", ""),
                "coefficient_symbol": row.get("coefficient_symbol", ""),
                "coefficient_value": coefficient_value,
                "affected_rows": row.get("affected_rows", ""),
                "required_selector_or_fill": selector_requirement,
                "derivation_status": derivation_status,
                "selector_status": selector_status,
                "valid_for_claim": "false",
            }
        )
    return rows


def validation_rows(sources: list[dict[str, str]], audit_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    missing_sources = [row for row in sources if row["exists"] != "True"]
    r11_rows = read_csv(R11_VECTOR_PATH)
    expected_families = set(SELECTOR_REQUIREMENTS)
    present_families = {row.get("operator_family", "") for row in r11_rows}
    claim_valid_audit = [row for row in audit_rows if row["valid_for_claim"] == "true"]
    not_selected = [
        row
        for row in audit_rows
        if row["selector_status"] in {"missing_selector_or_coefficient", "conditional_topological_not_claim_valid", "unselected_retained"}
    ]
    double_zero_lemma_rows = [
        row for row in SELECTOR_LEMMA_ROWS if row["lemma_id"] == "L2_double_zero_sufficient"
    ]

    return [
        {
            "rule_id": "V487_0_sources",
            "rule": "all cited source paths exist",
            "result": "pass" if not missing_sources else "fail",
            "evidence": f"missing_sources={len(missing_sources)}",
            "claim_effect": "traceability only",
        },
        {
            "rule_id": "V487_1_R11_rows_loaded",
            "rule": "all ten R11 operator families are loaded",
            "result": "pass" if expected_families.issubset(present_families) else "fail",
            "evidence": f"operator_family_rows={len(r11_rows)}",
            "claim_effect": "selector audit covers the R11 ledger",
        },
        {
            "rule_id": "V487_2_double_zero_lemma_written",
            "rule": "single-zero leak and double-zero sufficiency are both explicit",
            "result": "pass" if double_zero_lemma_rows else "fail",
            "evidence": "L1_single_zero_fails;L2_double_zero_sufficient",
            "claim_effect": "derivation condition is sharp",
        },
        {
            "rule_id": "V487_3_actual_rows_unselected",
            "rule": "actual R11 rows are not treated as selected by the lemma",
            "result": "pass" if len(not_selected) == len(audit_rows) else "fail",
            "evidence": f"unselected_rows={len(not_selected)} of {len(audit_rows)}",
            "claim_effect": "no hidden R11 pass",
        },
        {
            "rule_id": "V487_4_no_claim_valid_rows",
            "rule": "no selector-audit row is claim-valid",
            "result": "pass" if not claim_valid_audit else "fail",
            "evidence": f"claim_valid_audit_rows={len(claim_valid_audit)}",
            "claim_effect": "no EH/R11/local-GR promotion",
        },
        {
            "rule_id": "V487_5_next_contract",
            "rule": "next target is a parent clause that forces double-zero selectors, not a prose claim",
            "result": "pass",
            "evidence": NEXT_TARGET,
            "claim_effect": "derivation-first route preserved",
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


def build_doc(
    timestamp: str,
    generated_at_utc: str,
    run_dir: Path,
    sources: list[dict[str, str]],
    audit_rows: list[dict[str, str]],
    validations: list[dict[str, str]],
) -> str:
    return f"""# 487 - Local EH/R11 Selector Theorem Attempt

Private local-GR/Newton/PPN operator-selector checkpoint. This is not a public EH-only proof, R11 pass, alpha3 pass, mu_extra-zero pass, Newtonian-limit pass, PPN pass, local-GR derivation, cosmology result, EM result, or unified-field claim.

## 1. Purpose

Checkpoint `486` named the core GR-facing target:

```text
local compact branch -> S_EH plus X/Qcoh/topological terms only.
```

This checkpoint tries to sharpen that into a real theorem condition.

The important result is:

```text
single-zero suppression is not enough.
double-zero factorization is sufficient to first variation,
provided the selector is parent-owned and no multiplier/stress term survives.
```

That gives us a serious route, but not a promotion:

```text
the current R11 rows do not yet prove those double-zero selector factors.
```

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/local_EH_R11_selector_theorem_attempt.py` |
| Run directory | `{run_dir.relative_to(ROOT)}` |
| Timestamp | `{timestamp}` |
| Generated UTC | `{generated_at_utc}` |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## 3. Source Register

{markdown_table(sources)}

## 4. Selector Lemma

{markdown_table(SELECTOR_LEMMA_ROWS)}

The key calculation is:

```text
delta[F(Z) O] = F(Z) delta O + F'(Z) O delta Z.
```

On the local branch `Z=0`:

```text
F(0)=0 alone is not enough, because F'(0) O delta Z can survive.
```

So the clean sufficient condition is:

```text
F(0)=0 and F'(0)=0.
```

In plain terms:

```text
R11 silence wants a double zero, not a single zero.
```

## 5. Leak Tests

{markdown_table(LEAK_TEST_ROWS)}

## 6. Actual R11 Operator Audit

{markdown_table(audit_rows)}

The audit result is deliberately conservative:

```text
All actual R11 rows remain not claim-valid.
```

They have not yet been shown to be absent, double-zero selected, topological, or numerically bounded.

## 7. Validation

{markdown_table(validations)}

## 8. Decision

{markdown_table(DECISION_ROWS)}

## 9. Route Update

{markdown_table(ROUTE_UPDATE_ROWS)}

## 10. Claim Ceiling

Allowed:

```text
A double-zero selector is a sufficient local-silence mechanism for non-EH operators to first variation.
Single-zero suppression is rejected as too weak.
```

Allowed:

```text
The next parent-action target is to force double-zero selector factors across the R11 operator families.
```

Forbidden:

```text
MTS has derived EH-only local GR.
MTS has derived R11 silence.
MTS has derived Newtonian recovery or PPN recovery.
The current R11 rows are claim-valid.
```

## 11. Next Queue

| Priority | Target | Reason |
| --- | --- | --- |
| 1 | `{NEXT_TARGET}` | attempt a parent clause that forces F_A(0)=F_A'(0)=0 for local R11 families |
| 2 | R11 closure coefficients | only if the double-zero parent clause cannot be constructed |
| 3 | local PPN certificate | only after R11, boundary, and stress rows are zero/bounded |
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timestamp", default=datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S"))
    args = parser.parse_args()

    generated_at_utc = datetime.now(timezone.utc).isoformat()
    run_dir = ROOT / "runs" / f"{args.timestamp}-local-EH-R11-selector-theorem-attempt"
    run_dir.mkdir(parents=True, exist_ok=True)

    sources = source_rows()
    audit_rows = operator_audit_rows()
    validations = validation_rows(sources, audit_rows)

    write_csv(SOURCE_REGISTER_PATH, sources)
    write_csv(SELECTOR_LEMMA_PATH, SELECTOR_LEMMA_ROWS)
    write_csv(OPERATOR_AUDIT_PATH, audit_rows)
    write_csv(LEAK_TESTS_PATH, LEAK_TEST_ROWS)
    write_csv(VALIDATION_PATH, validations)
    write_csv(DECISION_PATH, DECISION_ROWS)
    write_csv(ROUTE_UPDATE_PATH, ROUTE_UPDATE_ROWS)

    doc = build_doc(args.timestamp, generated_at_utc, run_dir, sources, audit_rows, validations)
    (ROOT / DOC_PATH).write_text(doc, encoding="utf-8")

    missing_sources = [row["source_file"] for row in sources if row["exists"] != "True"]
    failed_validations = [row for row in validations if row["result"] == "fail"]
    claim_valid_audit_rows = [row for row in audit_rows if row["valid_for_claim"] == "true"]
    not_selected_rows = [
        row
        for row in audit_rows
        if row["selector_status"] in {"missing_selector_or_coefficient", "conditional_topological_not_claim_valid", "unselected_retained"}
    ]
    status = {
        "timestamp": args.timestamp,
        "generated_at_utc": generated_at_utc,
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "checkpoint_doc": str(DOC_PATH),
        "run_dir": str(run_dir),
        "source_register": str(ROOT / SOURCE_REGISTER_PATH),
        "selector_lemma": str(ROOT / SELECTOR_LEMMA_PATH),
        "operator_audit": str(ROOT / OPERATOR_AUDIT_PATH),
        "leak_tests": str(ROOT / LEAK_TESTS_PATH),
        "validation": str(ROOT / VALIDATION_PATH),
        "decision": str(ROOT / DECISION_PATH),
        "route_update": str(ROOT / ROUTE_UPDATE_PATH),
        "source_rows": len(sources),
        "source_paths_missing": len(missing_sources),
        "missing_sources": missing_sources,
        "selector_lemma_rows": len(SELECTOR_LEMMA_ROWS),
        "operator_audit_rows": len(audit_rows),
        "leak_test_rows": len(LEAK_TEST_ROWS),
        "failed_validation_rows": len(failed_validations),
        "claim_valid_audit_rows": len(claim_valid_audit_rows),
        "not_selected_operator_rows": len(not_selected_rows),
        "double_zero_sufficiency_lemma_written": True,
        "single_zero_rejected": True,
        "actual_R11_rows_parent_selected": False,
        "EH_only_derived": False,
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
