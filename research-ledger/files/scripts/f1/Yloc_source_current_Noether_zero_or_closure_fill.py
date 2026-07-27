from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

STATUS = "Yloc_source_current_Noether_gate_written_Ward_ownership_not_zero_no_linear_source_symmetry_needed_no_Newton_PPN_or_local_GR_pass"
CLAIM_CEILING = "Noether_Ward_source_current_gate_only_JY_BY_not_zeroed_no_Yloc_R11_EH_Newton_PPN_or_local_GR_promotion"
NEXT_TARGET = "491-Yloc-no-linear-source-symmetry-or-closure.md"

DOC_PATH = Path("490-Yloc-source-current-Noether-zero-or-closure-fill.md")
SOURCE_REGISTER_PATH = Path("source-intake/mts_residuals/P8_YLOC_SOURCE_CURRENT_SOURCE_REGISTER.csv")
NOETHER_AUDIT_PATH = Path("source-intake/mts_residuals/P8_YLOC_SOURCE_CURRENT_NOETHER_AUDIT.csv")
CURRENT_AUDIT_PATH = Path("source-intake/mts_residuals/P8_YLOC_SOURCE_CURRENT_COMPONENT_AUDIT.csv")
CLOSURE_FILL_PATH = Path("source-intake/mts_residuals/P8_YLOC_SOURCE_CURRENT_CLOSURE_FILL.csv")
VALIDATION_PATH = Path("source-intake/mts_residuals/P8_YLOC_SOURCE_CURRENT_VALIDATION.csv")
DECISION_PATH = Path("source-intake/mts_residuals/P8_YLOC_SOURCE_CURRENT_DECISION.csv")
ROUTE_UPDATE_PATH = Path("source-intake/mts_residuals/P8_YLOC_SOURCE_CURRENT_ROUTE_UPDATE.csv")

EULER_SYSTEM_PATH = Path("source-intake/mts_residuals/P8_YLOC_EULER_SYSTEM.csv")
SOURCE_DEBT_PATH = Path("source-intake/mts_residuals/P8_YLOC_SOURCE_DEBT_LEDGER.csv")
LOCAL_VECTOR_PATH = Path("source-intake/mts_residuals/P8_LOCAL_GR_RESIDUAL_VECTOR_FROM_DOMAIN_SOURCE.csv")


SOURCE_REGISTER = [
    {
        "source_file": "12-gauge-noether-origin-audit.md",
        "role": "Noether warning: identities relate equations but do not set constraints to zero by themselves",
    },
    {
        "source_file": "207-domain-projector-action-and-Bianchi-identity.md",
        "role": "formal Bianchi closure requires all projector/domain/boundary stresses retained",
    },
    {
        "source_file": "221-Noether-source-identity-or-compact-PPN-closure-map.md",
        "role": "source identity derivation template plus boundary/Bianchi conditions",
    },
    {
        "source_file": "429-Ward-Bianchi-exchange-owner-for-Poisson-source.md",
        "role": "Ward ownership gives exchange ledger but not source residual zero",
    },
    {
        "source_file": "489-local-silence-multiplet-Euler-equations-or-closure.md",
        "role": "Yloc positive no-source theorem and source-current debts",
    },
    {
        "source_file": str(EULER_SYSTEM_PATH),
        "role": "machine-readable Yloc Euler system",
    },
    {
        "source_file": str(SOURCE_DEBT_PATH),
        "role": "machine-readable source debt ledger",
    },
    {
        "source_file": str(LOCAL_VECTOR_PATH),
        "role": "local residual vector blocked by source-current rows",
    },
    {
        "source_file": "scripts/Yloc_source_current_Noether_zero_or_closure_fill.py",
        "role": "this checkpoint generator",
    },
]


NOETHER_AUDIT_ROWS = [
    {
        "test_id": "N0_diffeomorphism_Ward",
        "identity_or_route": "diffeomorphism Noether/Ward identity",
        "what_it_gives": "total conservation and exchange-owner ledger",
        "what_it_does_not_give": "J_Y=0 or B_Y=0 componentwise",
        "result": "ownership_not_zero",
        "valid_for_claim": "false",
    },
    {
        "test_id": "N1_parent_response_identity",
        "identity_or_route": "parent response/displacement variation",
        "what_it_gives": "can derive source identity if Khat and Gamma_eff are conjugates of a parent response field",
        "what_it_does_not_give": "absence of local PPN hair from that response field",
        "result": "conditional_template_not_zero",
        "valid_for_claim": "false",
    },
    {
        "test_id": "N2_boundary_Ward",
        "identity_or_route": "boundary Ward/no-flux identity",
        "what_it_gives": "boundary flux has an owner and can be cancelled/fixed/retained",
        "what_it_does_not_give": "scalar marker-free no-flux for alpha3 automatically",
        "result": "boundary_owned_not_zero",
        "valid_for_claim": "false",
    },
    {
        "test_id": "N3_Bianchi_stress",
        "identity_or_route": "Bianchi identity with all stresses varied",
        "what_it_gives": "formal total stress conservation",
        "what_it_does_not_give": "projector/domain/boundary stress absence or EH-only exterior",
        "result": "conservation_not_GR",
        "valid_for_claim": "false",
    },
    {
        "test_id": "N4_no_linear_source_symmetry",
        "identity_or_route": "local-silence reflection/parity or selection rule Y_loc -> -Y_loc",
        "what_it_gives": "would forbid linear source terms J_Y Y and force homogeneous local Euler equations",
        "what_it_does_not_give": "not currently derived as a parent symmetry",
        "result": "possible_rescue_theorem_target",
        "valid_for_claim": "false",
    },
    {
        "test_id": "N5_verdict",
        "identity_or_route": "Noether alone",
        "what_it_gives": "necessary discipline: every source current must be owned",
        "what_it_does_not_give": "the required zero-current theorem",
        "result": "reject_Noether_alone_for_Yloc_zero",
        "valid_for_claim": "false",
    },
]


CURRENT_AUDIT_ROWS = [
    {
        "current_id": "J0_trace_expansion",
        "Y_component": "X_D",
        "Noether_status": "stationarity/volume identity gives conditional trace zero",
        "zero_status": "partial_conditional",
        "missing_for_zero": "parent branch/domain selector through PPN order and boundary flux ownership",
        "blocks": "coherent trace-load source",
        "valid_for_claim": "false",
    },
    {
        "current_id": "J1_boundary_flux",
        "Y_component": "Phi_boundary^i",
        "Noether_status": "boundary flux can be in Ward ledger",
        "zero_status": "not_zeroed",
        "missing_for_zero": "scalar-only stationary marker-free boundary action or no-linear-source symmetry",
        "blocks": "LRV_BOUNDARY_R7_ALPHA3",
        "valid_for_claim": "false",
    },
    {
        "current_id": "J2_domain_vector",
        "Y_component": "V_domain^i",
        "Noether_status": "covariant domain vector can be conserved",
        "zero_status": "not_zeroed",
        "missing_for_zero": "parent no-vector/domain-selector symmetry",
        "blocks": "LRV_DOMAIN_R5_ALPHA1;LRV_DOMAIN_R6_ALPHA2;LRV_DOMAIN_R7_ALPHA3",
        "valid_for_claim": "false",
    },
    {
        "current_id": "J3_domain_STF_stress",
        "Y_component": "S_TF_domain^{ij}",
        "Noether_status": "stress can be Bianchi-owned",
        "zero_status": "not_zeroed",
        "missing_for_zero": "topological/isotropic trace-only projector stress theorem",
        "blocks": "LRV_DOMAIN_R8_XI;LRV_PROJECTOR_STRESS_ACCOUNTING",
        "valid_for_claim": "false",
    },
    {
        "current_id": "J4_source_normalization",
        "Y_component": "Delta_mu_source",
        "Noether_status": "hidden source contribution can be conserved",
        "zero_status": "not_zeroed",
        "missing_for_zero": "constant measured-GM/source-normalization theorem",
        "blocks": "LRV_DOMAIN_R11_SOURCE_NORMALIZATION",
        "valid_for_claim": "false",
    },
    {
        "current_id": "J5_extra_stress_Bianchi",
        "Y_component": "nabla_mu T_extra^{mu nu}",
        "Noether_status": "total Bianchi identity can hold with retained extra stress",
        "zero_status": "retained_not_zeroed",
        "missing_for_zero": "extra stress zero/topological theorem or residual scoring",
        "blocks": "LRV_PROJECTOR_STRESS_ACCOUNTING;LRV_TOTAL_ALPHA3_GUARD",
        "valid_for_claim": "false",
    },
]


CLOSURE_FILL_ROWS = [
    {
        "fill_id": "CF0_boundary_flux",
        "current_or_boundary": "J_B^i;B_B^i",
        "theorem_zero_needed": "scalar stationary boundary no-flux or Y-boundary no-linear-source symmetry",
        "fallback_fill": "W_boundary_alpha3_epsilon_boundary_flux",
        "target_bound": "abs(alpha3_boundary) <= 4e-20",
        "source_artifact_needed": "theorem certificate or numeric product with units/source path",
        "valid_for_claim": "false",
    },
    {
        "fill_id": "CF1_domain_vector",
        "current_or_boundary": "J_V^i",
        "theorem_zero_needed": "domain no-vector selector symmetry",
        "fallback_fill": "W_domain_alpha1/alpha2/alpha3 times epsilon_domain_vector/flux",
        "target_bound": "alpha1<=1e-4; alpha2<=2e-9; alpha3<=4e-20",
        "source_artifact_needed": "theorem certificate or numeric coefficient products",
        "valid_for_claim": "false",
    },
    {
        "fill_id": "CF2_domain_STF_stress",
        "current_or_boundary": "J_S^{ij}",
        "theorem_zero_needed": "projector/domain STF stress topological or trace-only theorem",
        "fallback_fill": "W_domain_xi_epsilon_domain_anisotropy plus T_extra residual",
        "target_bound": "xi<=4e-9 or declared local residual gate",
        "source_artifact_needed": "stress ledger and numeric/theorem source",
        "valid_for_claim": "false",
    },
    {
        "fill_id": "CF3_source_normalization",
        "current_or_boundary": "J_mu",
        "theorem_zero_needed": "constant measured-GM/source-normalization Noether theorem",
        "fallback_fill": "c_domain_source_normalization_operator",
        "target_bound": "operator row has source path, units, weak-field map, no MISSING fields",
        "source_artifact_needed": "R11 executable vector or zero theorem",
        "valid_for_claim": "false",
    },
    {
        "fill_id": "CF4_extra_stress_Bianchi",
        "current_or_boundary": "nabla_mu T_extra^{mu nu}",
        "theorem_zero_needed": "extra stress vanishes/topological or conserved below PPN bounds",
        "fallback_fill": "retained T_extra residual vector",
        "target_bound": "PPN residual bounds by channel",
        "source_artifact_needed": "Bianchi stress ledger and residual score",
        "valid_for_claim": "false",
    },
]


DECISION_ROWS = [
    {
        "decision_id": "D0_Noether_alone",
        "status": "rejected_for_zero",
        "meaning": "Noether/Ward ownership is necessary but does not set J_Y=0 or B_Y=0 componentwise",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D1_possible_rescue",
        "status": "no_linear_source_symmetry_target",
        "meaning": "a parent local-silence symmetry Y_loc -> -Y_loc could forbid linear source terms and make the Euler equations homogeneous",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D2_closure_fill",
        "status": "retained_if_symmetry_fails",
        "meaning": "each source-current debt has an explicit closure/numeric fill row",
        "next_action": "fill only after theorem route fails or with sourced evidence",
    },
    {
        "decision_id": "D3_promotion",
        "status": "forbidden",
        "meaning": "no Yloc zero, EH/R11 silence, Newton, PPN, alpha3, mu_extra-zero, or local-GR pass is earned",
        "next_action": "continue derivation-first route",
    },
]


ROUTE_UPDATE_ROWS = [
    {
        "route_id": "YLOC_SOURCE_CURRENT",
        "previous_status": "source_currents_not_zeroed",
        "new_status": "Noether_ownership_not_zero_no_linear_source_symmetry_needed",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "DOUBLE_ZERO_R11_SELECTOR",
        "previous_status": "requires_Yloc_source_current_zero",
        "new_status": "requires_no_linear_source_or_closure_fills",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "LOCAL_GR",
        "previous_status": "blocked_by_source_current_and_boundary_terms",
        "new_status": "blocked_by_unzeroed_Yloc_source_currents",
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
    euler_rows = read_csv(EULER_SYSTEM_PATH)
    source_debts = read_csv(SOURCE_DEBT_PATH)
    local_vector_rows = read_csv(LOCAL_VECTOR_PATH)
    claim_noether_rows = [row for row in NOETHER_AUDIT_ROWS if row["valid_for_claim"] == "true"]
    claim_current_rows = [row for row in CURRENT_AUDIT_ROWS if row["valid_for_claim"] == "true"]
    required_debts = {"S0_boundary_source", "S3_source_normalization_current", "S4_Bianchi_stress_current"}
    debt_ids = {row.get("debt_id", "") for row in source_debts}
    vector_components = {row.get("component_id", "") for row in local_vector_rows}
    required_components = {"LRV_BOUNDARY_R7_ALPHA3", "LRV_DOMAIN_R11_SOURCE_NORMALIZATION", "LRV_PROJECTOR_STRESS_ACCOUNTING"}

    return [
        {
            "rule_id": "V490_0_sources",
            "rule": "all cited source paths exist",
            "result": "pass" if not missing_sources else "fail",
            "evidence": f"missing_sources={len(missing_sources)}",
            "claim_effect": "traceability only",
        },
        {
            "rule_id": "V490_1_euler_loaded",
            "rule": "489 Yloc Euler rows are loaded",
            "result": "pass" if len(euler_rows) == 7 else "fail",
            "evidence": f"euler_rows={len(euler_rows)}",
            "claim_effect": "Noether audit is tied to Yloc system",
        },
        {
            "rule_id": "V490_2_source_debts_loaded",
            "rule": "source debt ledger includes boundary, source-normalization, and Bianchi debts",
            "result": "pass" if required_debts.issubset(debt_ids) else "fail",
            "evidence": ";".join(sorted(required_debts & debt_ids)),
            "claim_effect": "targets known source-current blockers",
        },
        {
            "rule_id": "V490_3_residual_coverage",
            "rule": "audit covers active local residual blockers",
            "result": "pass" if required_components.issubset(vector_components) else "fail",
            "evidence": ";".join(sorted(required_components & vector_components)),
            "claim_effect": "not a generic Noether discussion",
        },
        {
            "rule_id": "V490_4_no_Noether_zero_claim",
            "rule": "Noether/Ward rows are not promoted as zero-current proof",
            "result": "pass" if not claim_noether_rows else "fail",
            "evidence": f"claim_valid_noether_rows={len(claim_noether_rows)}",
            "claim_effect": "no fake source-current zero",
        },
        {
            "rule_id": "V490_5_no_current_claim",
            "rule": "no source-current component row is claim-valid",
            "result": "pass" if not claim_current_rows else "fail",
            "evidence": f"claim_valid_current_rows={len(claim_current_rows)}",
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
    return f"""# 490 - Yloc Source-Current Noether Zero Or Closure Fill

Private local-GR/Newton/PPN source-current checkpoint. This is not a public Yloc-zero proof, EH-only proof, R11 pass, alpha3 pass, mu_extra-zero pass, Newtonian-limit pass, PPN pass, local-GR derivation, cosmology result, EM result, or unified-field claim.

## 1. Purpose

Checkpoint `489` reduced the double-zero R11 route to a sharp condition:

```text
J_Y = 0
B_Y = 0
```

for the local-silence multiplet.

This checkpoint asks whether Noether/Ward identities already give those zeros.

Short answer:

```text
Noether/Ward gives ownership and conservation.
It does not by itself give componentwise zero source currents.
```

The possible derivation route is stronger:

```text
a parent local-silence symmetry, such as Y_loc -> -Y_loc,
that forbids linear source terms and makes the local Euler equations homogeneous.
```

That route is not yet derived.

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/Yloc_source_current_Noether_zero_or_closure_fill.py` |
| Run directory | `{run_dir.relative_to(ROOT)}` |
| Timestamp | `{timestamp}` |
| Generated UTC | `{generated_at_utc}` |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## 3. Source Register

{markdown_table(sources)}

## 4. Noether / Ward Audit

{markdown_table(NOETHER_AUDIT_ROWS)}

The no-cheat rule is:

```text
Noether identity = conservation/ownership.
Zero-current theorem = extra condition.
```

So:

```text
nabla_mu T_total^(mu nu)=0
```

does not imply:

```text
J_Y=0
B_Y=0.
```

## 5. Source-Current Component Audit

{markdown_table(CURRENT_AUDIT_ROWS)}

## 6. Closure Fill Rows If Symmetry Fails

{markdown_table(CLOSURE_FILL_ROWS)}

## 7. Validation

{markdown_table(validations)}

## 8. Decision

{markdown_table(DECISION_ROWS)}

## 9. Route Update

{markdown_table(ROUTE_UPDATE_ROWS)}

## 10. Claim Ceiling

Allowed:

```text
Noether/Ward ownership is necessary for the local branch.
Noether/Ward ownership alone does not derive Yloc source-current zeros.
A no-linear-source symmetry is now the next derivation target.
```

Forbidden:

```text
MTS has derived Y_loc=0.
MTS has derived J_Y=0 or B_Y=0.
MTS has derived EH/R11 silence.
MTS has derived Newtonian recovery or PPN recovery.
MTS has alpha3=0 or mu_extra=0.
```

## 11. Next Queue

| Priority | Target | Reason |
| --- | --- | --- |
| 1 | `{NEXT_TARGET}` | attempt the stronger parent symmetry that forbids linear Yloc source terms |
| 2 | closure fill pack | if the no-linear-source symmetry cannot be constructed |
| 3 | local PPN residual certificate | only after source currents and boundary terms are zero/bounded |
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timestamp", default=datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S"))
    args = parser.parse_args()

    generated_at_utc = datetime.now(timezone.utc).isoformat()
    run_dir = ROOT / "runs" / f"{args.timestamp}-Yloc-source-current-Noether-zero-or-closure-fill"
    run_dir.mkdir(parents=True, exist_ok=True)

    sources = source_rows()
    validations = validation_rows(sources)

    write_csv(SOURCE_REGISTER_PATH, sources)
    write_csv(NOETHER_AUDIT_PATH, NOETHER_AUDIT_ROWS)
    write_csv(CURRENT_AUDIT_PATH, CURRENT_AUDIT_ROWS)
    write_csv(CLOSURE_FILL_PATH, CLOSURE_FILL_ROWS)
    write_csv(VALIDATION_PATH, validations)
    write_csv(DECISION_PATH, DECISION_ROWS)
    write_csv(ROUTE_UPDATE_PATH, ROUTE_UPDATE_ROWS)

    doc = build_doc(args.timestamp, generated_at_utc, run_dir, sources, validations)
    (ROOT / DOC_PATH).write_text(doc, encoding="utf-8")

    missing_sources = [row["source_file"] for row in sources if row["exists"] != "True"]
    failed_validations = [row for row in validations if row["result"] == "fail"]
    claim_noether_rows = [row for row in NOETHER_AUDIT_ROWS if row["valid_for_claim"] == "true"]
    claim_current_rows = [row for row in CURRENT_AUDIT_ROWS if row["valid_for_claim"] == "true"]
    status = {
        "timestamp": args.timestamp,
        "generated_at_utc": generated_at_utc,
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "checkpoint_doc": str(DOC_PATH),
        "run_dir": str(run_dir),
        "source_register": str(ROOT / SOURCE_REGISTER_PATH),
        "noether_audit": str(ROOT / NOETHER_AUDIT_PATH),
        "current_audit": str(ROOT / CURRENT_AUDIT_PATH),
        "closure_fill": str(ROOT / CLOSURE_FILL_PATH),
        "validation": str(ROOT / VALIDATION_PATH),
        "decision": str(ROOT / DECISION_PATH),
        "route_update": str(ROOT / ROUTE_UPDATE_PATH),
        "source_rows": len(sources),
        "source_paths_missing": len(missing_sources),
        "missing_sources": missing_sources,
        "noether_audit_rows": len(NOETHER_AUDIT_ROWS),
        "current_audit_rows": len(CURRENT_AUDIT_ROWS),
        "closure_fill_rows": len(CLOSURE_FILL_ROWS),
        "failed_validation_rows": len(failed_validations),
        "claim_valid_noether_rows": len(claim_noether_rows),
        "claim_valid_current_rows": len(claim_current_rows),
        "Noether_ownership_written": True,
        "Noether_derives_JY_BY_zero": False,
        "no_linear_source_symmetry_needed": True,
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
