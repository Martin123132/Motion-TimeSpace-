from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

STATUS = "exchange_doublet_component_map_scored_two_conditional_routes_five_unresolved_or_retained_coefficients_no_local_GR_promotion"
CLAIM_CEILING = "component_map_and_coefficient_branch_only_no_Yloc_zero_R11_EH_Newton_PPN_or_local_GR_promotion"
NEXT_TARGET = "495-source-normalization-even-scalar-theorem-or-coefficient-fill.md"

DOC_PATH = Path("494-exchange-doublet-component-map-or-coefficient-branch.md")
SOURCE_REGISTER_PATH = Path("source-intake/mts_residuals/P8_EXCHANGE_COMPONENT_SOURCE_REGISTER.csv")
COMPONENT_MAP_PATH = Path("source-intake/mts_residuals/P8_EXCHANGE_COMPONENT_MAP_SCORE.csv")
COEFFICIENT_BRANCH_PATH = Path("source-intake/mts_residuals/P8_EXCHANGE_COMPONENT_COEFFICIENT_BRANCH.csv")
HARD_ROWS_PATH = Path("source-intake/mts_residuals/P8_EXCHANGE_COMPONENT_HARD_ROWS.csv")
GATE_TESTS_PATH = Path("source-intake/mts_residuals/P8_EXCHANGE_COMPONENT_GATE_TESTS.csv")
VALIDATION_PATH = Path("source-intake/mts_residuals/P8_EXCHANGE_COMPONENT_VALIDATION.csv")
DECISION_PATH = Path("source-intake/mts_residuals/P8_EXCHANGE_COMPONENT_DECISION.csv")
ROUTE_UPDATE_PATH = Path("source-intake/mts_residuals/P8_EXCHANGE_COMPONENT_ROUTE_UPDATE.csv")

ODD_COMPONENT_MAP_PATH = Path("source-intake/mts_residuals/P8_ODD_RESIDUAL_COMPONENT_MAP.csv")
LOCAL_VECTOR_PATH = Path("source-intake/mts_residuals/P8_LOCAL_GR_RESIDUAL_VECTOR_FROM_DOMAIN_SOURCE.csv")
DOMAIN_COEFFICIENTS_PATH = Path("source-intake/mts_residuals/P8_DOMAIN_SELECTOR_VECTOR_COEFFICIENTS.csv")
R11_VECTOR_PATH = Path("source-intake/mts_residuals/R11_nonEH_operator_vector_executable.csv")


SOURCE_REGISTER = [
    {
        "source_file": "493-odd-residual-parentization-or-closure-fill.md",
        "role": "exchange-doublet parentization contract and component-map target",
    },
    {
        "source_file": "492-silence-auxiliary-parent-action-construction-or-closure.md",
        "role": "lock/Z2 triangle",
    },
    {
        "source_file": "475-domain-selector-parent-action-clause-or-coefficient-fill.md",
        "role": "domain selector double-zero route and coefficient fallback",
    },
    {
        "source_file": "472-domain-projector-alpha3-no-leak-or-R11-link.md",
        "role": "domain alpha3/R11 source-normalization link",
    },
    {
        "source_file": "401-parent-matter-selector-theorem-attempt.md",
        "role": "selector-blind matter theorem attempt and counterexample",
    },
    {
        "source_file": "404-selector-blind-matter-axiom-origin.md",
        "role": "relational quotient/readout as best primitive target",
    },
    {
        "source_file": str(ODD_COMPONENT_MAP_PATH),
        "role": "493 odd residual component map",
    },
    {
        "source_file": str(LOCAL_VECTOR_PATH),
        "role": "active local-GR residual vector",
    },
    {
        "source_file": str(DOMAIN_COEFFICIENTS_PATH),
        "role": "domain PPN coefficient fallback rows",
    },
    {
        "source_file": str(R11_VECTOR_PATH),
        "role": "R11 non-EH operator/source-normalization ledger",
    },
    {
        "source_file": "scripts/exchange_doublet_component_map_or_coefficient_branch.py",
        "role": "this checkpoint generator",
    },
]


COMPONENT_MAP_ROWS = [
    {
        "component_id": "Y0_trace_expansion",
        "exchange_map_attempt": "Z_X=(X_+ - X_-)/2",
        "required_parent_identity": "local trace-load residual is antisymmetric representative data and matter trace couples only to even quotient",
        "score": "not_derived",
        "reason": "ordinary compact matter trace is exchange-even and can source scalar curvature/normalization",
        "coefficient_or_theorem_branch": "trace-load source-current closure",
        "valid_for_claim": "false",
    },
    {
        "component_id": "Y1_coherent_projector",
        "exchange_map_attempt": "Z_Q=(Qcoh_+ - Qcoh_-)/2",
        "required_parent_identity": "projector trace/STF split is parent-owned and antisymmetric nontrace modes are local-odd",
        "score": "not_derived",
        "reason": "projector ownership and topological stress theorem remain open",
        "coefficient_or_theorem_branch": "retained projector/domain stress ledger",
        "valid_for_claim": "false",
    },
    {
        "component_id": "Y2_boundary_flux",
        "exchange_map_attempt": "Z_B=([J_B]_+ - [J_B]_-)/2 projected to Phi_boundary",
        "required_parent_identity": "boundary flux is an exchange-odd relative boundary-current class and compact local domains have zero odd class",
        "score": "conditional_route",
        "reason": "this is structurally plausible but local odd boundary charge zero is not proved",
        "coefficient_or_theorem_branch": "W_boundary_alpha3_epsilon_boundary_flux",
        "valid_for_claim": "false",
    },
    {
        "component_id": "Y3_domain_vector",
        "exchange_map_attempt": "Z_V=(V_domain,+ - V_domain,-)/2 from exchange-odd domain representative",
        "required_parent_identity": "domain selector is scalar/topological and exchange-odd vector class vanishes locally",
        "score": "conditional_best",
        "reason": "475 double-zero selector is the strongest existing shape but local zero/topological selector is not derived",
        "coefficient_or_theorem_branch": "W_domain_alpha1/alpha2/alpha3 products",
        "valid_for_claim": "false",
    },
    {
        "component_id": "Y4_domain_STF_stress",
        "exchange_map_attempt": "Z_S=(S_TF,+ - S_TF,-)/2",
        "required_parent_identity": "all PPN-visible STF stress is exchange-odd and odd local charge zero",
        "score": "not_derived",
        "reason": "tidal STF and projector stress can be exchange-even/conserved",
        "coefficient_or_theorem_branch": "W_domain_xi_epsilon_domain_anisotropy plus T_extra",
        "valid_for_claim": "false",
    },
    {
        "component_id": "Y5_source_normalization",
        "exchange_map_attempt": "Z_mu=(mu_+ - mu_-)/2",
        "required_parent_identity": "observed measured GM is exchange-even and all non-EH source-normalization offsets are odd and vanish locally",
        "score": "failed_current_hard",
        "reason": "measured GM/source normalization is an observed even scalar; oddness cannot be assumed without a separate source-normalization theorem",
        "coefficient_or_theorem_branch": "c_domain_source_normalization_operator",
        "valid_for_claim": "false",
    },
    {
        "component_id": "Y6_stress_Bianchi",
        "exchange_map_attempt": "not a primary odd residual; divergence of retained stress ledger",
        "required_parent_identity": "all extra stress is odd and zero or even/topological/invisible",
        "score": "retained_debt",
        "reason": "Bianchi ownership allows conserved exchange-even extra stress",
        "coefficient_or_theorem_branch": "retained T_extra residual vector",
        "valid_for_claim": "false",
    },
]


COEFFICIENT_BRANCH_ROWS = [
    {
        "branch_id": "B0_boundary_alpha3",
        "from_component": "Y2_boundary_flux",
        "target_row": "LRV_BOUNDARY_R7_ALPHA3",
        "observable": "alpha3",
        "coefficient_or_certificate": "W_boundary_alpha3_epsilon_boundary_flux or boundary odd-charge zero theorem",
        "status": "theorem_or_numeric_required",
        "valid_for_claim": "false",
    },
    {
        "branch_id": "B1_domain_alpha1",
        "from_component": "Y3_domain_vector",
        "target_row": "LRV_DOMAIN_R5_ALPHA1",
        "observable": "alpha1",
        "coefficient_or_certificate": "W_domain_alpha1_epsilon_domain_vector or domain no-vector theorem",
        "status": "theorem_or_numeric_required",
        "valid_for_claim": "false",
    },
    {
        "branch_id": "B2_domain_alpha2",
        "from_component": "Y3_domain_vector",
        "target_row": "LRV_DOMAIN_R6_ALPHA2",
        "observable": "alpha2",
        "coefficient_or_certificate": "W_domain_alpha2_epsilon_domain_vector or domain no-vector theorem",
        "status": "theorem_or_numeric_required",
        "valid_for_claim": "false",
    },
    {
        "branch_id": "B3_domain_alpha3",
        "from_component": "Y3_domain_vector/Y2_boundary_flux/Y5_source_normalization",
        "target_row": "LRV_DOMAIN_R7_ALPHA3",
        "observable": "alpha3",
        "coefficient_or_certificate": "W_domain_alpha3_epsilon_domain_flux plus R11/source-normalization silence",
        "status": "theorem_or_numeric_required",
        "valid_for_claim": "false",
    },
    {
        "branch_id": "B4_domain_xi",
        "from_component": "Y4_domain_STF_stress/Y6_stress_Bianchi",
        "target_row": "LRV_DOMAIN_R8_XI",
        "observable": "xi",
        "coefficient_or_certificate": "W_domain_xi_epsilon_domain_anisotropy or topological/invisible stress theorem",
        "status": "theorem_or_numeric_required",
        "valid_for_claim": "false",
    },
    {
        "branch_id": "B5_R11_source_normalization",
        "from_component": "Y5_source_normalization",
        "target_row": "LRV_DOMAIN_R11_SOURCE_NORMALIZATION",
        "observable": "non_EH_operator_coefficients",
        "coefficient_or_certificate": "c_domain_source_normalization_operator or measured-GM/source-normalization theorem",
        "status": "hard_next_target",
        "valid_for_claim": "false",
    },
    {
        "branch_id": "B6_projector_stress",
        "from_component": "Y1/Y4/Y6",
        "target_row": "LRV_PROJECTOR_STRESS_ACCOUNTING",
        "observable": "Bianchi_PPN_stress",
        "coefficient_or_certificate": "topological projector stress theorem or retained T_extra vector",
        "status": "retained_debt",
        "valid_for_claim": "false",
    },
]


HARD_ROWS = [
    {
        "hard_row": "Y5_source_normalization",
        "why_hard": "Newtonian recovery depends on measured source normalization; it is naturally exchange-even, not odd",
        "cannot_use": "exchange symmetry alone",
        "needed_theorem": "observed GM is pure even EH source while all non-EH normalization operators are odd/local-zero or coefficient-bounded",
        "next_target": NEXT_TARGET,
    },
    {
        "hard_row": "Y6_stress_Bianchi",
        "why_hard": "Bianchi conservation owns extra stress but does not make it vanish",
        "cannot_use": "Noether/Ward ownership alone",
        "needed_theorem": "extra stress is topological/invisible or carried as explicit residual",
        "next_target": "T_extra topological theorem or residual scoring",
    },
    {
        "hard_row": "C2_even_matter_readout",
        "why_hard": "matter can couple to universal class metric exp(F(C_D))e under weaker premises",
        "cannot_use": "covariance or WEP words alone",
        "needed_theorem": "selector-blind observed coframe from parent quotient/readout",
        "next_target": "matter-neutrality parent proof",
    },
    {
        "hard_row": "C3_boundary_odd_charge",
        "why_hard": "compact boundary can carry a vector/odd class unless local triviality is derived",
        "cannot_use": "stationary boundary language alone",
        "needed_theorem": "local compact boundary odd class zero/no-flux",
        "next_target": "boundary odd-charge zero theorem or alpha3 fill",
    },
]


GATE_TEST_ROWS = [
    {
        "gate_id": "G0_component_identity",
        "test": "all seven Yloc residuals map to exchange-odd parent variables through PPN order",
        "result": "fail_for_claim",
        "evidence": "claim_valid_component_rows=0; unresolved_rows=7",
        "claim_effect": "no Yloc zero",
    },
    {
        "gate_id": "G1_conditional_routes",
        "test": "component map identifies plausible theorem lanes",
        "result": "partial",
        "evidence": "Y2_boundary_flux and Y3_domain_vector are conditional routes",
        "claim_effect": "guides next derivations only",
    },
    {
        "gate_id": "G2_source_normalization",
        "test": "Y5 source-normalization is killed by exchange oddness",
        "result": "fail_for_claim",
        "evidence": "measured GM is exchange-even unless separate theorem exists",
        "claim_effect": "Newton/source-normalized GR remains blocked",
    },
    {
        "gate_id": "G3_even_stress",
        "test": "Y6 extra stress is killed by exchange oddness",
        "result": "fail_for_claim",
        "evidence": "exchange-even conserved stress remains legal",
        "claim_effect": "EH-only exterior remains blocked",
    },
    {
        "gate_id": "G4_coefficient_branch",
        "test": "all failed/conditional rows have explicit theorem-or-coefficient fallback",
        "result": "pass",
        "evidence": "coefficient_branch_rows=7",
        "claim_effect": "testability branch preserved",
    },
    {
        "gate_id": "G5_no_promotion",
        "test": "no component/coefficient row is valid_for_claim",
        "result": "pass",
        "evidence": "valid_for_claim_true=0",
        "claim_effect": "no local-GR promotion",
    },
]


DECISION_ROWS = [
    {
        "decision_id": "D0_exchange_map",
        "status": "partial_conditional_only",
        "meaning": "exchange-doublet mapping is promising for boundary/domain classes but not complete",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D1_demotions",
        "status": "coefficient_branch_retained",
        "meaning": "every unmapped row has an explicit theorem-or-coefficient fallback",
        "next_action": "do not claim local GR; test or derive rows",
    },
    {
        "decision_id": "D2_next_priority",
        "status": "Y5_source_normalization",
        "meaning": "source-normalized Newtonian recovery cannot be secured by oddness alone",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D3_promotion",
        "status": "forbidden",
        "meaning": "no Yloc zero, R11 silence, Newton, PPN, alpha3, mu_extra-zero, or local-GR pass is earned",
        "next_action": "continue derivation-first route",
    },
]


ROUTE_UPDATE_ROWS = [
    {
        "route_id": "ODD_RESIDUAL_PARENTIZATION",
        "previous_status": "exchange_doublet_contract_written_component_map_incomplete",
        "new_status": "component_map_partial_Y2_Y3_conditional_Y5_Y6_block",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "LOCAL_NEWTON_GR",
        "previous_status": "blocked_by_component_map_source_normalization_even_stress_and_boundary_odd_charge",
        "new_status": "blocked_first_by_Y5_source_normalization_plus_Y6_stress",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "PPN_COEFFICIENT_BRANCH",
        "previous_status": "retained_unfilled",
        "new_status": "coefficient_branch_explicit_for_all_failed_exchange_rows",
        "accepted_for_claim": "false",
        "next_target": "fill numeric products only after theorem route fails or data source exists",
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
    odd_rows = read_csv(ODD_COMPONENT_MAP_PATH)
    local_vector_rows = read_csv(LOCAL_VECTOR_PATH)
    domain_coeff_rows = read_csv(DOMAIN_COEFFICIENTS_PATH)
    r11_rows = read_csv(R11_VECTOR_PATH)
    claim_component_rows = [row for row in COMPONENT_MAP_ROWS if row["valid_for_claim"] == "true"]
    claim_coefficient_rows = [row for row in COEFFICIENT_BRANCH_ROWS if row["valid_for_claim"] == "true"]
    required_components = {
        "Y0_trace_expansion",
        "Y1_coherent_projector",
        "Y2_boundary_flux",
        "Y3_domain_vector",
        "Y4_domain_STF_stress",
        "Y5_source_normalization",
        "Y6_stress_Bianchi",
    }
    component_ids = {row["component_id"] for row in COMPONENT_MAP_ROWS}
    required_targets = {
        "LRV_BOUNDARY_R7_ALPHA3",
        "LRV_DOMAIN_R5_ALPHA1",
        "LRV_DOMAIN_R6_ALPHA2",
        "LRV_DOMAIN_R7_ALPHA3",
        "LRV_DOMAIN_R8_XI",
        "LRV_DOMAIN_R11_SOURCE_NORMALIZATION",
        "LRV_PROJECTOR_STRESS_ACCOUNTING",
    }
    target_ids = {row["target_row"] for row in COEFFICIENT_BRANCH_ROWS}

    return [
        {
            "rule_id": "V494_0_sources",
            "rule": "all cited source paths exist",
            "result": "pass" if not missing_sources else "fail",
            "evidence": f"missing_sources={len(missing_sources)}",
            "claim_effect": "traceability only",
        },
        {
            "rule_id": "V494_1_inputs_loaded",
            "rule": "493 component map, local residual vector, domain coefficients, and R11 vector are loaded",
            "result": "pass" if len(odd_rows) == 7 and len(local_vector_rows) >= 7 and len(domain_coeff_rows) >= 5 and len(r11_rows) >= 5 else "fail",
            "evidence": f"odd_rows={len(odd_rows)};local_vector_rows={len(local_vector_rows)};domain_coeff_rows={len(domain_coeff_rows)};r11_rows={len(r11_rows)}",
            "claim_effect": "component map tied to active local gates",
        },
        {
            "rule_id": "V494_2_component_coverage",
            "rule": "all seven Yloc components are scored",
            "result": "pass" if required_components.issubset(component_ids) else "fail",
            "evidence": ";".join(sorted(component_ids)),
            "claim_effect": "no skipped residual",
        },
        {
            "rule_id": "V494_3_coefficient_coverage",
            "rule": "coefficient branch covers boundary alpha3, domain alpha1/alpha2/alpha3/xi, R11 source normalization, and stress",
            "result": "pass" if required_targets.issubset(target_ids) else "fail",
            "evidence": ";".join(sorted(target_ids)),
            "claim_effect": "failed theorem rows remain testable",
        },
        {
            "rule_id": "V494_4_hard_rows_identified",
            "rule": "source-normalization and extra-stress hard rows are explicit",
            "result": "pass" if len(HARD_ROWS) == 4 else "fail",
            "evidence": ";".join(row["hard_row"] for row in HARD_ROWS),
            "claim_effect": "next blocker is concrete",
        },
        {
            "rule_id": "V494_5_no_claim_rows",
            "rule": "no component or coefficient row is claim-valid",
            "result": "pass" if not claim_component_rows and not claim_coefficient_rows else "fail",
            "evidence": f"claim_component_rows={len(claim_component_rows)};claim_coefficient_rows={len(claim_coefficient_rows)}",
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


def build_doc(
    timestamp: str,
    generated_at_utc: str,
    run_dir: Path,
    sources: list[dict[str, str]],
    validations: list[dict[str, str]],
) -> str:
    return f"""# 494 - Exchange Doublet Component Map Or Coefficient Branch

Private local-GR/Newton/PPN component-map checkpoint. This is not a public Yloc-zero proof, EH-only proof, R11 pass, alpha3 pass, mu_extra-zero pass, Newtonian-limit pass, PPN pass, local-GR derivation, cosmology result, EM result, or unified-field claim.

## 1. Purpose

Checkpoint `493` found the cleanest candidate:

```text
physical residuals as exchange-odd parent variables.
```

This checkpoint tests that component-by-component and demotes unmapped rows to coefficient/theorem branches.

Short answer:

```text
Y2 boundary flux and Y3 domain vector are plausible conditional exchange routes.
Y5 source normalization and Y6 extra stress remain hard blockers.
No component is claim-valid yet.
```

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/exchange_doublet_component_map_or_coefficient_branch.py` |
| Run directory | `{run_dir.relative_to(ROOT)}` |
| Timestamp | `{timestamp}` |
| Generated UTC | `{generated_at_utc}` |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## 3. Source Register

{markdown_table(sources)}

## 4. Component Map Score

{markdown_table(COMPONENT_MAP_ROWS)}

## 5. Coefficient / Theorem Branch

{markdown_table(COEFFICIENT_BRANCH_ROWS)}

## 6. Hard Rows

{markdown_table(HARD_ROWS)}

## 7. Gate Tests

{markdown_table(GATE_TEST_ROWS)}

## 8. Validation

{markdown_table(validations)}

## 9. Decision

{markdown_table(DECISION_ROWS)}

## 10. Route Update

{markdown_table(ROUTE_UPDATE_ROWS)}

## 11. Claim Ceiling

Allowed:

```text
The exchange-doublet component map identifies Y2/Y3 as conditional derivation lanes.
All other rows remain theorem-debt or coefficient-debt.
Y5 source normalization is now the next priority for Newton/GR recovery.
```

Forbidden:

```text
MTS has derived exchange-doublet local residual zero.
MTS has derived Y_loc=0.
MTS has derived EH/R11 silence.
MTS has derived Newtonian recovery or PPN recovery.
MTS has alpha3=0 or mu_extra=0.
```

## 12. Next Queue

| Priority | Target | Reason |
| --- | --- | --- |
| 1 | `{NEXT_TARGET}` | source-normalized Newtonian recovery is blocked by an even scalar row that exchange oddness cannot simply kill |
| 2 | boundary/domain odd-charge theorem | needed before Y2/Y3 conditional routes can become zero certificates |
| 3 | extra-stress theorem or residual score | needed before EH-only local exterior can be claimed |
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timestamp", default=datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S"))
    args = parser.parse_args()

    generated_at_utc = datetime.now(timezone.utc).isoformat()
    run_dir = ROOT / "runs" / f"{args.timestamp}-exchange-doublet-component-map-or-coefficient-branch"
    run_dir.mkdir(parents=True, exist_ok=True)

    sources = source_rows()
    validations = validation_rows(sources)

    write_csv(SOURCE_REGISTER_PATH, sources)
    write_csv(COMPONENT_MAP_PATH, COMPONENT_MAP_ROWS)
    write_csv(COEFFICIENT_BRANCH_PATH, COEFFICIENT_BRANCH_ROWS)
    write_csv(HARD_ROWS_PATH, HARD_ROWS)
    write_csv(GATE_TESTS_PATH, GATE_TEST_ROWS)
    write_csv(VALIDATION_PATH, validations)
    write_csv(DECISION_PATH, DECISION_ROWS)
    write_csv(ROUTE_UPDATE_PATH, ROUTE_UPDATE_ROWS)

    doc = build_doc(args.timestamp, generated_at_utc, run_dir, sources, validations)
    (ROOT / DOC_PATH).write_text(doc, encoding="utf-8")

    missing_sources = [row["source_file"] for row in sources if row["exists"] != "True"]
    failed_validations = [row for row in validations if row["result"] == "fail"]
    claim_component_rows = [row for row in COMPONENT_MAP_ROWS if row["valid_for_claim"] == "true"]
    claim_coefficient_rows = [row for row in COEFFICIENT_BRANCH_ROWS if row["valid_for_claim"] == "true"]
    conditional_rows = [
        row for row in COMPONENT_MAP_ROWS
        if row["score"] in {"conditional_route", "conditional_best"}
    ]
    hard_block_rows = [
        row for row in COMPONENT_MAP_ROWS
        if row["score"] in {"failed_current_hard", "retained_debt"}
    ]
    status = {
        "timestamp": args.timestamp,
        "generated_at_utc": generated_at_utc,
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "checkpoint_doc": str(DOC_PATH),
        "run_dir": str(run_dir),
        "source_register": str(ROOT / SOURCE_REGISTER_PATH),
        "component_map": str(ROOT / COMPONENT_MAP_PATH),
        "coefficient_branch": str(ROOT / COEFFICIENT_BRANCH_PATH),
        "hard_rows": str(ROOT / HARD_ROWS_PATH),
        "gate_tests": str(ROOT / GATE_TESTS_PATH),
        "validation": str(ROOT / VALIDATION_PATH),
        "decision": str(ROOT / DECISION_PATH),
        "route_update": str(ROOT / ROUTE_UPDATE_PATH),
        "source_rows": len(sources),
        "source_paths_missing": len(missing_sources),
        "missing_sources": missing_sources,
        "component_map_rows": len(COMPONENT_MAP_ROWS),
        "coefficient_branch_rows": len(COEFFICIENT_BRANCH_ROWS),
        "hard_rows_count": len(HARD_ROWS),
        "gate_test_rows": len(GATE_TEST_ROWS),
        "failed_validation_rows": len(failed_validations),
        "claim_component_rows": len(claim_component_rows),
        "claim_coefficient_rows": len(claim_coefficient_rows),
        "conditional_exchange_rows": len(conditional_rows),
        "hard_block_rows": len(hard_block_rows),
        "component_map_claim_valid": False,
        "Y2_boundary_flux_conditional_route": True,
        "Y3_domain_vector_conditional_best": True,
        "Y5_source_normalization_blocks_Newton": True,
        "Y6_extra_stress_blocks_EH_only": True,
        "source_normalization_theorem_derived": False,
        "extra_stress_theorem_derived": False,
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
