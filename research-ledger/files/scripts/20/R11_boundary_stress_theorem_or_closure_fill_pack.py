from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

STATUS = "R11_boundary_stress_theorem_stack_and_closure_fill_pack_written_no_Newton_PPN_or_local_GR_pass"
CLAIM_CEILING = "conditional_sufficient_local_silence_stack_plus_closure_fill_pack_only_no_boundary_R11_stress_or_local_GR_promotion"
NEXT_TARGET = "487-local-EH-R11-selector-theorem-attempt.md"

DOC_PATH = Path("486-R11-boundary-stress-theorem-or-closure-fill-pack.md")
SOURCE_REGISTER_PATH = Path("source-intake/mts_residuals/P8_R11_BOUNDARY_STRESS_SOURCE_REGISTER.csv")
THEOREM_STACK_PATH = Path("source-intake/mts_residuals/P8_R11_BOUNDARY_STRESS_THEOREM_STACK.csv")
CLOSURE_FILL_PACK_PATH = Path("source-intake/mts_residuals/P8_R11_BOUNDARY_STRESS_CLOSURE_FILL_PACK.csv")
PROMOTION_GATE_PATH = Path("source-intake/mts_residuals/P8_R11_BOUNDARY_STRESS_PROMOTION_GATE.csv")
VALIDATION_PATH = Path("source-intake/mts_residuals/P8_R11_BOUNDARY_STRESS_VALIDATION.csv")
DECISION_PATH = Path("source-intake/mts_residuals/P8_R11_BOUNDARY_STRESS_DECISION.csv")
ROUTE_UPDATE_PATH = Path("source-intake/mts_residuals/P8_R11_BOUNDARY_STRESS_ROUTE_UPDATE.csv")

PREMISE_REQUIREMENTS_PATH = Path("source-intake/mts_residuals/P8_LOCAL_ZERO_EXTRA_PREMISE_REQUIREMENTS.csv")
LOCAL_ZERO_DECISION_PATH = Path("source-intake/mts_residuals/P8_LOCAL_ZERO_BOUNDARY_R11_DECISION.csv")
LOCAL_GR_VECTOR_PATH = Path("source-intake/mts_residuals/P8_LOCAL_GR_RESIDUAL_VECTOR_FROM_DOMAIN_SOURCE.csv")
R11_FILL_REQUIREMENTS_PATH = Path("source-intake/mts_residuals/R11_DOMAIN_SOURCE_FILL_REQUIREMENTS.csv")
ALPHA3_TEMPLATE_PATH = Path("source-intake/mts_residuals/P8_ALPHA3_NUMERIC_PRODUCT_INPUT_TEMPLATE.csv")


SOURCE_REGISTER = [
    {
        "source_file": "470-boundary-alpha3-zero-theorem-or-numeric-coefficient.md",
        "role": "conditional scalar boundary no-flux lemma and boundary alpha3 fallback product",
    },
    {
        "source_file": "473-R11-domain-projector-operator-vector-minimum-fill.md",
        "role": "minimum R11 domain/projector vector wiring and retained coefficient rows",
    },
    {
        "source_file": "479-R11-domain-source-normalization-zero-or-fill.md",
        "role": "R11/domain source zero route rejected and fill requirements written",
    },
    {
        "source_file": "482-local-residual-vector-from-domain-source-fill.md",
        "role": "active local residual vector and local-GR blockers",
    },
    {
        "source_file": "485-boundary-no-flux-and-R11-silence-from-local-zero.md",
        "role": "shortcut rejection and extra premise list",
    },
    {
        "source_file": str(PREMISE_REQUIREMENTS_PATH),
        "role": "extra premises required after local-zero shortcut failed",
    },
    {
        "source_file": str(LOCAL_ZERO_DECISION_PATH),
        "role": "decision rows from checkpoint 485",
    },
    {
        "source_file": str(LOCAL_GR_VECTOR_PATH),
        "role": "current local residual vector to be filled or theorem-zeroed",
    },
    {
        "source_file": str(R11_FILL_REQUIREMENTS_PATH),
        "role": "domain R11/source-normalization fill requirements",
    },
    {
        "source_file": str(ALPHA3_TEMPLATE_PATH),
        "role": "boundary/domain alpha3 product template",
    },
    {
        "source_file": "scripts/R11_boundary_stress_theorem_or_closure_fill_pack.py",
        "role": "this checkpoint generator",
    },
]


THEOREM_STACK_ROWS = [
    {
        "theorem_id": "T0_local_zero_input",
        "sufficient_clause": "X=nabla_mu u^mu; Qcoh_mu_nu=(1/3)h_mu_nu X; stationary compact comoving local branch gives X_D=0",
        "would_clear": "pure coherent trace-load source",
        "current_status": "conditional_partial_available",
        "missing_for_claim": "parent selection of the compact local branch through PPN order",
        "valid_for_claim": "false",
    },
    {
        "theorem_id": "T1_boundary_scalar_no_flux",
        "sufficient_clause": "S_boundary=int_boundary sqrt(abs(gamma)) F(scalar invariants only), stationary, marker-free, Ward-flux closed",
        "would_clear": "LRV_BOUNDARY_R7_ALPHA3",
        "current_status": "conditional_tensor_lemma_known",
        "missing_for_claim": "parent proof that no tangential vector, shear, spin marker, or normal exchange survives",
        "valid_for_claim": "false",
    },
    {
        "theorem_id": "T2_domain_no_vector_selector",
        "sufficient_clause": "delta S/delta chi_D selects scalar local domains and forbids domain velocity/selector marker vectors in the observed local coframe",
        "would_clear": "LRV_DOMAIN_R5_ALPHA1;LRV_DOMAIN_R6_ALPHA2;LRV_DOMAIN_R7_ALPHA3;LRV_DOMAIN_R8_XI",
        "current_status": "not_parent_derived",
        "missing_for_claim": "zero-knob Euler/domain-selection equation with local and FLRW branches",
        "valid_for_claim": "false",
    },
    {
        "theorem_id": "T3_local_EH_R11_selector",
        "sufficient_clause": "local compact branch reduces to S_EH plus terms proportional to X, Qcoh, or topological invariants with zero local variation",
        "would_clear": "LRV_DOMAIN_R11_SOURCE_NORMALIZATION",
        "current_status": "not_derived",
        "missing_for_claim": "operator-family proof that non-EH/source-normalization coefficients vanish or are bounded below gate",
        "valid_for_claim": "false",
    },
    {
        "theorem_id": "T4_projector_stress_Bianchi",
        "sufficient_clause": "delta_g of projector, domain, boundary, and constraint sectors is zero/topological or retained as a conserved T_extra_mu_nu below PPN bounds",
        "would_clear": "LRV_PROJECTOR_STRESS_ACCOUNTING",
        "current_status": "retained_debt",
        "missing_for_claim": "metric-variation stress ledger and local Ward/Bianchi identity",
        "valid_for_claim": "false",
    },
    {
        "theorem_id": "T5_source_normalized_Newton",
        "sufficient_clause": "measured GM is the only local source normalization; no derivative hair, no frame/species leakage, no hidden calibration branch",
        "would_clear": "Newton source-normalization gate",
        "current_status": "blocked_by_R11_and_domain_rows",
        "missing_for_claim": "valid zero/bound rows for R11, boundary, domain, and stress channels",
        "valid_for_claim": "false",
    },
    {
        "theorem_id": "T6_channel_guard",
        "sufficient_clause": "boundary, domain, R11, and stress channels pass individually unless a parent Ward identity forces exact pre-fit cancellation",
        "would_clear": "LRV_TOTAL_ALPHA3_GUARD",
        "current_status": "guard_active",
        "missing_for_claim": "individual channel certificates or parent cancellation identity",
        "valid_for_claim": "false",
    },
]


CLOSURE_FILL_PACK_ROWS = [
    {
        "fill_id": "F0_boundary_alpha3",
        "channel": "boundary_monopole_shift",
        "residual_component": "LRV_BOUNDARY_R7_ALPHA3",
        "symbol_to_fill": "W_boundary_alpha3_epsilon_boundary_flux",
        "units": "dimensionless",
        "bound_or_gate": "abs(alpha3_boundary) <= 4e-20",
        "allowed_fill": "theorem_zero_or_numeric_product",
        "required_source": "scalar boundary theorem certificate or numeric source path with local frame/normalization",
        "current_status": "template_unfilled",
        "valid_for_claim": "false",
    },
    {
        "fill_id": "F1_domain_alpha1",
        "channel": "domain_projector_mass",
        "residual_component": "LRV_DOMAIN_R5_ALPHA1",
        "symbol_to_fill": "W_domain_alpha1_epsilon_domain_vector",
        "units": "dimensionless_or_declared_operator_units",
        "bound_or_gate": "abs(alpha1_domain) <= 1e-04",
        "allowed_fill": "theorem_zero_or_numeric_coefficient",
        "required_source": "domain no-vector theorem or coefficient source path",
        "current_status": "template_unfilled",
        "valid_for_claim": "false",
    },
    {
        "fill_id": "F2_domain_alpha2",
        "channel": "domain_projector_mass",
        "residual_component": "LRV_DOMAIN_R6_ALPHA2",
        "symbol_to_fill": "W_domain_alpha2_epsilon_domain_vector",
        "units": "dimensionless_or_declared_operator_units",
        "bound_or_gate": "abs(alpha2_domain) <= 2e-09",
        "allowed_fill": "theorem_zero_or_numeric_coefficient",
        "required_source": "domain no-vector theorem or coefficient source path",
        "current_status": "template_unfilled",
        "valid_for_claim": "false",
    },
    {
        "fill_id": "F3_domain_alpha3",
        "channel": "domain_projector_mass",
        "residual_component": "LRV_DOMAIN_R7_ALPHA3",
        "symbol_to_fill": "W_domain_alpha3_epsilon_domain_flux",
        "units": "dimensionless",
        "bound_or_gate": "abs(alpha3_domain) <= 4e-20",
        "allowed_fill": "theorem_zero_or_numeric_product",
        "required_source": "domain no-leak theorem plus R11/stress silence, or numeric product with assumptions",
        "current_status": "template_unfilled",
        "valid_for_claim": "false",
    },
    {
        "fill_id": "F4_domain_xi",
        "channel": "domain_projector_mass",
        "residual_component": "LRV_DOMAIN_R8_XI",
        "symbol_to_fill": "W_domain_xi_epsilon_domain_anisotropy",
        "units": "dimensionless_or_declared_operator_units",
        "bound_or_gate": "abs(xi_domain) <= 4e-09",
        "allowed_fill": "theorem_zero_or_numeric_coefficient",
        "required_source": "STF/anisotropy theorem or numeric coefficient source path",
        "current_status": "template_unfilled",
        "valid_for_claim": "false",
    },
    {
        "fill_id": "F5_R11_source_normalization",
        "channel": "R11_nonEH_operator_vector",
        "residual_component": "LRV_DOMAIN_R11_SOURCE_NORMALIZATION",
        "symbol_to_fill": "c_domain_source_normalization_operator",
        "units": "dimensionless_or_declared_operator_units",
        "bound_or_gate": "operator row has source path, units, normalization, weak-field map, and no MISSING fields",
        "allowed_fill": "EH_only_theorem_zero_or_executable_coefficient_vector",
        "required_source": "local EH/R11 selector theorem or filled R11 executable vector",
        "current_status": "template_unfilled",
        "valid_for_claim": "false",
    },
    {
        "fill_id": "F6_projector_stress",
        "channel": "projector_domain_stress",
        "residual_component": "LRV_PROJECTOR_STRESS_ACCOUNTING",
        "symbol_to_fill": "T_extra_mu_nu_or_c_projector_domain_stress",
        "units": "stress_units_or_dimensionless_residual_map_declared",
        "bound_or_gate": "zero/topological or retained residual below relevant PPN gates",
        "allowed_fill": "stress_zero_theorem_or_retained_stress_score",
        "required_source": "metric variation ledger and Ward/Bianchi closure",
        "current_status": "retained_debt",
        "valid_for_claim": "false",
    },
    {
        "fill_id": "F7_total_alpha3_guard",
        "channel": "combined_alpha3",
        "residual_component": "LRV_TOTAL_ALPHA3_GUARD",
        "symbol_to_fill": "alpha3_channel_certificates_or_parent_cancellation_identity",
        "units": "dimensionless",
        "bound_or_gate": "each active alpha3 channel passes individually unless exact parent identity enforces cancellation",
        "allowed_fill": "individual_channel_passes_or_parent_identity",
        "required_source": "boundary/domain/R11/stress certificates",
        "current_status": "guard_active",
        "valid_for_claim": "false",
    },
]


PROMOTION_GATE_ROWS = [
    {
        "gate_id": "G0_theorem_stack_complete",
        "rule": "T0-T6 are parent-derived or replaced by scored closure rows",
        "current_result": "fail_for_claim",
        "evidence": "valid_for_claim=false for all theorem rows",
        "promotion_effect": "no local-GR promotion",
    },
    {
        "gate_id": "G1_fill_pack_complete",
        "rule": "F0-F7 have theorem-zero certificates or numeric rows with units/source paths/no MISSING fields",
        "current_result": "fail_for_claim",
        "evidence": "current_status is template_unfilled/retained_debt/guard_active",
        "promotion_effect": "no PPN residual certificate",
    },
    {
        "gate_id": "G2_alpha3_guard",
        "rule": "boundary and domain alpha3 pass individually before total alpha3 is scored",
        "current_result": "pass_as_guard_only",
        "evidence": "F7_total_alpha3_guard retained",
        "promotion_effect": "prevents hidden cancellation claim",
    },
    {
        "gate_id": "G3_R11_EH_operator",
        "rule": "local compact branch is EH-only or R11 coefficients are executable and bounded",
        "current_result": "fail_for_claim",
        "evidence": "F5_R11_source_normalization unfilled",
        "promotion_effect": "Newton/source-normalization still blocked",
    },
    {
        "gate_id": "G4_stress_Bianchi",
        "rule": "projector/domain/boundary/constraint stress is zero/topological or retained with conservation",
        "current_result": "fail_for_claim",
        "evidence": "F6_projector_stress retained_debt",
        "promotion_effect": "local Bianchi/PPN still blocked",
    },
]


DECISION_ROWS = [
    {
        "decision_id": "D0_sufficient_theorem_stack",
        "status": "written_not_derived",
        "meaning": "the exact parent-action clauses needed for local silence are now explicit",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D1_closure_fill_pack",
        "status": "written_required_if_theorem_route_fails",
        "meaning": "every active local blocker now has a theorem-zero or numeric fill row",
        "next_action": "fill only with sourced theorem/numeric evidence, not by prose",
    },
    {
        "decision_id": "D2_boundary_R11_stress",
        "status": "still_active_blockers",
        "meaning": "boundary no-flux, R11 silence, and stress/Bianchi closure remain unresolved",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D3_promotion",
        "status": "forbidden",
        "meaning": "no Newton, PPN, alpha3, mu_extra-zero, R11, or local-GR claim is earned",
        "next_action": "attempt the local EH/R11 selector theorem before numeric fallback",
    },
]


ROUTE_UPDATE_ROWS = [
    {
        "route_id": "LOCAL_ZERO_TRACE_ROUTE",
        "previous_status": "partial_clause_retained",
        "new_status": "input_to_sufficient_stack",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "BOUNDARY_R11_STRESS_THEOREM_ROUTE",
        "previous_status": "independent_theorem_required",
        "new_status": "sufficient_stack_written_not_derived",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "CLOSURE_FILL_ROUTE",
        "previous_status": "fallback_needed_if_theorem_fails",
        "new_status": "explicit_fill_pack_written",
        "accepted_for_claim": "false",
        "next_target": "alpha3_evaluator_refresh_after_rows_are_filled",
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
    premise_rows = read_csv(PREMISE_REQUIREMENTS_PATH)
    vector_rows = read_csv(LOCAL_GR_VECTOR_PATH)
    missing_sources = [row for row in sources if row["exists"] != "True"]
    theorem_claim_rows = [row for row in THEOREM_STACK_ROWS if row["valid_for_claim"] == "true"]
    fill_claim_rows = [row for row in CLOSURE_FILL_PACK_ROWS if row["valid_for_claim"] == "true"]
    required_components = {
        "LRV_BOUNDARY_R7_ALPHA3",
        "LRV_DOMAIN_R11_SOURCE_NORMALIZATION",
        "LRV_PROJECTOR_STRESS_ACCOUNTING",
        "LRV_TOTAL_ALPHA3_GUARD",
    }
    vector_components = {row.get("component_id", "") for row in vector_rows}
    blocker_coverage = required_components.issubset(vector_components)
    premise_ids = {row.get("premise_id", "") for row in premise_rows}
    premise_coverage = {"P1_boundary_scalar_no_flux", "P2_R11_EH_operator", "P3_stress_Bianchi"}.issubset(premise_ids)

    return [
        {
            "rule_id": "V486_0_sources",
            "rule": "all cited source paths exist",
            "result": "pass" if not missing_sources else "fail",
            "evidence": f"missing_sources={len(missing_sources)}",
            "claim_effect": "traceability only",
        },
        {
            "rule_id": "V486_1_premise_coverage",
            "rule": "485 premise requirements include boundary, R11, and stress blockers",
            "result": "pass" if premise_coverage else "fail",
            "evidence": ";".join(sorted(premise_ids)),
            "claim_effect": "sufficient stack is tied to prior audit",
        },
        {
            "rule_id": "V486_2_blocker_coverage",
            "rule": "fill pack covers active local residual blocker components",
            "result": "pass" if blocker_coverage else "fail",
            "evidence": ";".join(sorted(required_components & vector_components)),
            "claim_effect": "closure pack targets actual local-GR blockers",
        },
        {
            "rule_id": "V486_3_theorem_rows_no_claim",
            "rule": "no theorem row is promoted as derived",
            "result": "pass" if not theorem_claim_rows else "fail",
            "evidence": f"claim_valid_theorem_rows={len(theorem_claim_rows)}",
            "claim_effect": "no fake theorem pass",
        },
        {
            "rule_id": "V486_4_fill_rows_no_claim",
            "rule": "no closure fill row is claim-valid before evidence is supplied",
            "result": "pass" if not fill_claim_rows else "fail",
            "evidence": f"claim_valid_fill_rows={len(fill_claim_rows)}",
            "claim_effect": "no numeric/closure pass yet",
        },
        {
            "rule_id": "V486_5_gate_policy",
            "rule": "promotion gates explicitly fail until theorem or fill rows are valid",
            "result": "pass",
            "evidence": "G0/G1/G3/G4 fail_for_claim; G2 guard only",
            "claim_effect": "no Newton/PPN/local-GR promotion",
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
    return f"""# 486 - R11 Boundary Stress Theorem Or Closure Fill Pack

Private local-GR/Newton/PPN theorem/fill checkpoint. This is not a public R11 pass, alpha3 pass, mu_extra-zero pass, Newtonian-limit pass, PPN pass, local-GR derivation, cosmology result, EM result, or unified-field claim.

## 1. Purpose

Checkpoint `485` rejected the shortcut:

```text
X_D=0 does not imply boundary preferred-momentum no-flux,
R11/source-normalization silence, or projector stress/Bianchi closure.
```

This checkpoint does the useful next thing:

```text
write the exact sufficient theorem stack a parent action must satisfy,
and write the explicit closure/numeric fill pack if those theorem rows are not derived.
```

Short answer:

```text
The local-zero route is still worth keeping.
But the complete local-GR route now requires a boundary/R11/stress stack.
That stack is written here as a contract, not claimed as derived.
The fallback fill rows are also written explicitly.
```

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/R11_boundary_stress_theorem_or_closure_fill_pack.py` |
| Run directory | `{run_dir.relative_to(ROOT)}` |
| Timestamp | `{timestamp}` |
| Generated UTC | `{generated_at_utc}` |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## 3. Source Register

{markdown_table(sources)}

## 4. Sufficient Theorem Stack

{markdown_table(THEOREM_STACK_ROWS)}

The theorem-stack meaning is:

```text
If T0-T6 are parent-derived, then the local-zero branch can become a real local-silence route.
If any one of T1-T6 fails, the corresponding row must be closure/numeric filled.
```

The central GR-facing theorem is `T3_local_EH_R11_selector`:

```text
local compact branch -> S_EH plus X/Qcoh/topological terms only.
```

That is the cleanest way to avoid smuggling local GR.

## 5. Closure / Numeric Fill Pack

{markdown_table(CLOSURE_FILL_PACK_ROWS)}

These rows are deliberately strict:

```text
No row becomes claim-valid until it has a theorem-zero certificate
or a numeric coefficient/product with units, source path, normalization,
local frame assumptions, and no hidden cancellation.
```

The pressure points remain:

```text
W_boundary_alpha3 * epsilon_boundary_flux <= 4e-20
W_domain_alpha3 * epsilon_domain_flux <= 4e-20
c_domain_source_normalization_operator -> zero/bounded local EH/R11 ledger
T_extra_mu_nu -> zero/topological or retained below PPN gates
```

## 6. Promotion Gates

{markdown_table(PROMOTION_GATE_ROWS)}

## 7. Validation

{markdown_table(validations)}

## 8. Decision

{markdown_table(DECISION_ROWS)}

## 9. Route Update

{markdown_table(ROUTE_UPDATE_ROWS)}

## 10. Claim Ceiling

Allowed:

```text
The local-GR blocker stack has been made explicit.
The exact sufficient theorem clauses are now named.
The closure/numeric fallback rows are written.
```

Allowed:

```text
Local-zero remains a useful partial route, but it only suppresses the coherent trace-load channel.
```

Forbidden:

```text
MTS has derived local GR.
MTS has derived the Newtonian limit.
MTS passes PPN.
MTS has alpha3=0 or mu_extra=0.
The theorem stack is derived.
The closure fill pack is scored.
```

## 11. Next Queue

| Priority | Target | Reason |
| --- | --- | --- |
| 1 | `{NEXT_TARGET}` | try the core GR-facing theorem: local compact branch selects EH/R11 silence rather than closure coefficients |
| 2 | boundary scalar parent owner | derive T1 if T3 does not close boundary terms |
| 3 | alpha3 evaluator refresh | only after F0/F3 have theorem-zero certificates or numeric products |
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timestamp", default=datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S"))
    args = parser.parse_args()

    generated_at_utc = datetime.now(timezone.utc).isoformat()
    run_dir = ROOT / "runs" / f"{args.timestamp}-R11-boundary-stress-theorem-or-closure-fill-pack"
    run_dir.mkdir(parents=True, exist_ok=True)

    sources = source_rows()
    validations = validation_rows(sources)

    write_csv(SOURCE_REGISTER_PATH, sources)
    write_csv(THEOREM_STACK_PATH, THEOREM_STACK_ROWS)
    write_csv(CLOSURE_FILL_PACK_PATH, CLOSURE_FILL_PACK_ROWS)
    write_csv(PROMOTION_GATE_PATH, PROMOTION_GATE_ROWS)
    write_csv(VALIDATION_PATH, validations)
    write_csv(DECISION_PATH, DECISION_ROWS)
    write_csv(ROUTE_UPDATE_PATH, ROUTE_UPDATE_ROWS)

    doc = build_doc(args.timestamp, generated_at_utc, run_dir, sources, validations)
    (ROOT / DOC_PATH).write_text(doc, encoding="utf-8")

    missing_sources = [row["source_file"] for row in sources if row["exists"] != "True"]
    failed_validations = [row for row in validations if row["result"] == "fail"]
    claim_valid_theorem_rows = [row for row in THEOREM_STACK_ROWS if row["valid_for_claim"] == "true"]
    claim_valid_fill_rows = [row for row in CLOSURE_FILL_PACK_ROWS if row["valid_for_claim"] == "true"]
    status = {
        "timestamp": args.timestamp,
        "generated_at_utc": generated_at_utc,
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "checkpoint_doc": str(DOC_PATH),
        "run_dir": str(run_dir),
        "source_register": str(ROOT / SOURCE_REGISTER_PATH),
        "theorem_stack": str(ROOT / THEOREM_STACK_PATH),
        "closure_fill_pack": str(ROOT / CLOSURE_FILL_PACK_PATH),
        "promotion_gate": str(ROOT / PROMOTION_GATE_PATH),
        "validation": str(ROOT / VALIDATION_PATH),
        "decision": str(ROOT / DECISION_PATH),
        "route_update": str(ROOT / ROUTE_UPDATE_PATH),
        "source_rows": len(sources),
        "source_paths_missing": len(missing_sources),
        "missing_sources": missing_sources,
        "theorem_stack_rows": len(THEOREM_STACK_ROWS),
        "closure_fill_pack_rows": len(CLOSURE_FILL_PACK_ROWS),
        "promotion_gate_rows": len(PROMOTION_GATE_ROWS),
        "failed_validation_rows": len(failed_validations),
        "claim_valid_theorem_rows": len(claim_valid_theorem_rows),
        "claim_valid_fill_rows": len(claim_valid_fill_rows),
        "sufficient_theorem_stack_written": True,
        "closure_fill_pack_written": True,
        "boundary_no_flux_derived": False,
        "R11_silence_derived": False,
        "stress_Bianchi_closed": False,
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
