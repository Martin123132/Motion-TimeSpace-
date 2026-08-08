from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

STATUS = "source_normalization_even_scalar_theorem_stack_written_exchange_odd_insufficient_R11_coefficients_retained_no_Newton_or_local_GR_promotion"
CLAIM_CEILING = "source_normalization_theorem_or_coefficient_gate_only_no_Newton_PPN_EH_R11_or_local_GR_promotion"
NEXT_TARGET = "496-R11-source-normalization-operator-vector-minimum-fill.md"

DOC_PATH = Path("495-source-normalization-even-scalar-theorem-or-coefficient-fill.md")
SOURCE_REGISTER_PATH = Path("source-intake/mts_residuals/P8_SOURCE_NORMALIZATION_SOURCE_REGISTER.csv")
THEOREM_STACK_PATH = Path("source-intake/mts_residuals/P8_SOURCE_NORMALIZATION_THEOREM_STACK.csv")
EVEN_ODD_SPLIT_PATH = Path("source-intake/mts_residuals/P8_SOURCE_NORMALIZATION_EVEN_ODD_SPLIT.csv")
CHANNEL_AUDIT_PATH = Path("source-intake/mts_residuals/P8_SOURCE_NORMALIZATION_CHANNEL_AUDIT.csv")
COEFFICIENT_FILL_PATH = Path("source-intake/mts_residuals/P8_SOURCE_NORMALIZATION_COEFFICIENT_FILL.csv")
VALIDATION_PATH = Path("source-intake/mts_residuals/P8_SOURCE_NORMALIZATION_VALIDATION.csv")
DECISION_PATH = Path("source-intake/mts_residuals/P8_SOURCE_NORMALIZATION_DECISION.csv")
ROUTE_UPDATE_PATH = Path("source-intake/mts_residuals/P8_SOURCE_NORMALIZATION_ROUTE_UPDATE.csv")

EXCHANGE_HARD_ROWS_PATH = Path("source-intake/mts_residuals/P8_EXCHANGE_COMPONENT_HARD_ROWS.csv")
EXCHANGE_COEFFICIENT_BRANCH_PATH = Path("source-intake/mts_residuals/P8_EXCHANGE_COMPONENT_COEFFICIENT_BRANCH.csv")
R11_VECTOR_PATH = Path("source-intake/mts_residuals/R11_nonEH_operator_vector_executable.csv")
LOCAL_VECTOR_PATH = Path("source-intake/mts_residuals/P8_LOCAL_GR_RESIDUAL_VECTOR_FROM_DOMAIN_SOURCE.csv")


SOURCE_REGISTER = [
    {
        "source_file": "494-exchange-doublet-component-map-or-coefficient-branch.md",
        "role": "Y5 source-normalization selected as next Newton/GR blocker",
    },
    {
        "source_file": "402-EH-source-normalization-parent-pair.md",
        "role": "same-frame EH/source-normalization conditional theorem pair",
    },
    {
        "source_file": "405-same-frame-EH-source-derived-stack-audit.md",
        "role": "local GR/Newton stack rungs and source-normalization status",
    },
    {
        "source_file": "401-parent-matter-selector-theorem-attempt.md",
        "role": "selector-blind matter conditional theorem and counterexample",
    },
    {
        "source_file": "404-selector-blind-matter-axiom-origin.md",
        "role": "selector-blind matter remains primitive/closure target",
    },
    {
        "source_file": "472-domain-projector-alpha3-no-leak-or-R11-link.md",
        "role": "domain source-normalization and alpha3/R11 coupling",
    },
    {
        "source_file": str(EXCHANGE_HARD_ROWS_PATH),
        "role": "494 hard-row ledger",
    },
    {
        "source_file": str(EXCHANGE_COEFFICIENT_BRANCH_PATH),
        "role": "494 coefficient/theorem branch",
    },
    {
        "source_file": str(R11_VECTOR_PATH),
        "role": "R11 non-EH operator/source-normalization vector",
    },
    {
        "source_file": str(LOCAL_VECTOR_PATH),
        "role": "active local residual vector",
    },
    {
        "source_file": "scripts/source_normalization_even_scalar_theorem_or_coefficient_fill.py",
        "role": "this checkpoint generator",
    },
]


THEOREM_STACK_ROWS = [
    {
        "step_id": "S0_same_frame",
        "required_statement": "matter, clocks, and the EH operator use the same observed local metric/coframe",
        "math_form": "S = (1/2 kappa) int sqrt(-g_obs) R[g_obs] + S_matter[psi,g_obs] + S_extra",
        "if_derived": "source normalization is not hidden in a frame change",
        "current_status": "conditional_not_parent_derived",
        "valid_for_claim": "false",
    },
    {
        "step_id": "S1_constant_kappa",
        "required_statement": "kappa is constant, universal, and locally time/range/species independent",
        "math_form": "G_EH = kappa c^4/(8 pi), partial_t G_EH = partial_r G_EH = partial_A G_EH = 0",
        "if_derived": "no Gdot, range-dependent G, or species-dependent source normalization",
        "current_status": "not_parent_derived",
        "valid_for_claim": "false",
    },
    {
        "step_id": "S2_Gauss_law_mass",
        "required_statement": "observed mass is the EH Gauss-law/ADM source in the same frame",
        "math_form": "mu_obs = lim r^2 partial_r Phi = G_EH M_EH",
        "if_derived": "Newtonian measured GM is fixed operationally",
        "current_status": "conditional_only",
        "valid_for_claim": "false",
    },
    {
        "step_id": "S3_no_extra_long_range_charge",
        "required_statement": "boundary, domain, bulk, scalar, vector, tensor, nonlocal, torsion/nonmetricity, and projector source charges vanish/topological/bounded",
        "math_form": "mu_extra = sum_i mu_i = 0 or explicitly scored below gates",
        "if_derived": "R11 source-normalization row can close",
        "current_status": "retained_debt",
        "valid_for_claim": "false",
    },
    {
        "step_id": "S4_no_absorption_cheat",
        "required_statement": "range/time/species/radial dependence is not absorbed into measured GM calibration",
        "math_form": "partial_r mu_extra = partial_t mu_extra = partial_A mu_extra = 0, else residual row stays active",
        "if_derived": "calibration is not hiding physics",
        "current_status": "rule_written_not_satisfied",
        "valid_for_claim": "false",
    },
    {
        "step_id": "S5_Newton_gate",
        "required_statement": "all previous statements hold together",
        "math_form": "mu_obs = G_EH M_EH and c_domain_source_normalization_operator = 0",
        "if_derived": "source-normalized Newtonian branch could be promoted",
        "current_status": "fail_for_current_corpus",
        "valid_for_claim": "false",
    },
]


EVEN_ODD_SPLIT_ROWS = [
    {
        "split_id": "E0_EH_source",
        "quantity": "G_EH M_EH",
        "exchange_parity": "even_observed",
        "status": "allowed_needed",
        "why": "this is the Newtonian source, not something to kill",
        "valid_for_claim": "false",
    },
    {
        "split_id": "E1_odd_extra_source",
        "quantity": "mu_extra_odd",
        "exchange_parity": "odd",
        "status": "could_vanish_if_exchange_theorem_and_local_odd_charge_zero_hold",
        "why": "exchange can help only for genuinely odd extra source channels",
        "valid_for_claim": "false",
    },
    {
        "split_id": "E2_even_extra_source",
        "quantity": "mu_extra_even",
        "exchange_parity": "even",
        "status": "not_killed_by_exchange",
        "why": "an even scalar source-normalization offset survives Z -> -Z",
        "valid_for_claim": "false",
    },
    {
        "split_id": "E3_measured_GM_offset",
        "quantity": "c_domain_source_normalization_operator",
        "exchange_parity": "unknown_even_allowed",
        "status": "retained",
        "why": "must be theorem-zero or coefficient-filled; cannot be declared odd",
        "valid_for_claim": "false",
    },
]


CHANNEL_AUDIT_ROWS = [
    {
        "channel_id": "C0_boundary_topological",
        "source": "boundary/class/topological functionals",
        "risk": "boundary stress or monopole shifts measured GM/alpha3",
        "needed_zero_or_bound": "boundary no-hair/no-flux theorem or coefficient vector",
        "current_status": "retained_R11_family",
        "valid_for_claim": "false",
    },
    {
        "channel_id": "C1_domain_projector",
        "source": "domain projector mass/source normalization",
        "risk": "mu_domain_projector changes measured GM and sibling PPN rows",
        "needed_zero_or_bound": "c_domain_source_normalization_operator=0 or executable coefficient products",
        "current_status": "hard_next_target",
        "valid_for_claim": "false",
    },
    {
        "channel_id": "C2_scalar_tensor_or_R2",
        "source": "R^2/f(R)/scalar class metric",
        "risk": "gamma/beta/range-dependent source response",
        "needed_zero_or_bound": "mass/range/coupling map or derived zero coefficient",
        "current_status": "retained_R11_family",
        "valid_for_claim": "false",
    },
    {
        "channel_id": "C3_vector_preferred_frame",
        "source": "domain vector, selector normal, preferred-frame marker",
        "risk": "alpha1/alpha2/alpha3 and source-normalization leakage",
        "needed_zero_or_bound": "domain no-vector theorem or coefficient products",
        "current_status": "retained_unfilled",
        "valid_for_claim": "false",
    },
    {
        "channel_id": "C4_projector_stress",
        "source": "delta_g P_D, delta_g chi_D, domain/readout-mask stress",
        "risk": "xi, alpha_i, R11 operator ledger",
        "needed_zero_or_bound": "topological metric-independent projector or stress residual bound",
        "current_status": "conditional_zero_not_parent_owned",
        "valid_for_claim": "false",
    },
    {
        "channel_id": "C5_nonlocal_or_bulk",
        "source": "bulk X force law, nonlocal memory kernel, torsion/nonmetricity",
        "risk": "fifth force, Gdot, range dependence, WEP/source charge",
        "needed_zero_or_bound": "locality/range/source-charge theorem or coefficient vector",
        "current_status": "retained_R11_family",
        "valid_for_claim": "false",
    },
]


COEFFICIENT_FILL_ROWS = [
    {
        "fill_id": "F0_c_domain_source_normalization_operator",
        "operator": "c_domain_source_normalization_operator",
        "required_input": "derived zero or numeric coefficient with units, normalization, weak-field map, and source path",
        "blocks": "LRV_DOMAIN_R11_SOURCE_NORMALIZATION;R5;R6;R7;R8",
        "status": "missing",
        "valid_for_claim": "false",
    },
    {
        "fill_id": "F1_boundary_source_coefficients",
        "operator": "c_boundary_or_c_GB and boundary no-hair maps",
        "required_input": "boundary theorem-zero or residual bound for gamma/beta/alpha3/xi",
        "blocks": "R3;R4;R7;R8;R11",
        "status": "missing",
        "valid_for_claim": "false",
    },
    {
        "fill_id": "F2_scalar_range_coefficients",
        "operator": "c_R2_or_c_fR;F_phi_C_or_c_scalar",
        "required_input": "mass/range/coupling map for gamma, beta, Gdot, fifth force",
        "blocks": "R3;R4;R9;R10;R11",
        "status": "missing",
        "valid_for_claim": "false",
    },
    {
        "fill_id": "F3_vector_preferred_frame_coefficients",
        "operator": "c_domain_vector_or_selector_marker",
        "required_input": "domain vector absence theorem or alpha1/alpha2/alpha3/xi products",
        "blocks": "R5;R6;R7;R8;R11",
        "status": "missing",
        "valid_for_claim": "false",
    },
    {
        "fill_id": "F4_projector_stress_coefficients",
        "operator": "c_projector_domain_stress",
        "required_input": "topological projector proof or stress coefficient bound",
        "blocks": "R5;R6;R7;R8;R11",
        "status": "conditional_not_parent_owned",
        "valid_for_claim": "false",
    },
]


DECISION_ROWS = [
    {
        "decision_id": "D0_exchange_limit",
        "status": "exchange_odd_insufficient",
        "meaning": "exchange symmetry can kill odd extra sources only; measured GM and even source offsets require a separate theorem",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D1_theorem_stack",
        "status": "written_not_satisfied",
        "meaning": "same-frame EH plus constant kappa plus no extra long-range charge is the required Newton gate",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D2_coefficient_branch",
        "status": "retained",
        "meaning": "R11/source-normalization coefficients remain missing and must be filled or theorem-zeroed",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D3_promotion",
        "status": "forbidden",
        "meaning": "no Newton, PPN, source-normalization, R11, EH-only, or local-GR pass is earned",
        "next_action": "continue derivation-first route",
    },
]


ROUTE_UPDATE_ROWS = [
    {
        "route_id": "SOURCE_NORMALIZED_NEWTON",
        "previous_status": "blocked_first_by_Y5_source_normalization_plus_Y6_stress",
        "new_status": "same_frame_Gauss_law_theorem_stack_written_R11_coefficients_retained",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "ODD_RESIDUAL_PARENTIZATION",
        "previous_status": "component_map_partial_Y2_Y3_conditional_Y5_Y6_block",
        "new_status": "exchange_help_limited_to_odd_mu_extra_not_even_source_normalization",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "LOCAL_GR",
        "previous_status": "blocked_first_by_Y5_source_normalization_plus_Y6_stress",
        "new_status": "blocked_by_R11_source_normalization_coefficients_and_extra_stress",
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
    hard_rows = read_csv(EXCHANGE_HARD_ROWS_PATH)
    coeff_rows = read_csv(EXCHANGE_COEFFICIENT_BRANCH_PATH)
    r11_rows = read_csv(R11_VECTOR_PATH)
    local_rows = read_csv(LOCAL_VECTOR_PATH)
    claim_theorem_rows = [row for row in THEOREM_STACK_ROWS if row["valid_for_claim"] == "true"]
    claim_channel_rows = [row for row in CHANNEL_AUDIT_ROWS if row["valid_for_claim"] == "true"]
    claim_fill_rows = [row for row in COEFFICIENT_FILL_ROWS if row["valid_for_claim"] == "true"]
    source_norm_rows = [
        row for row in r11_rows
        if "source_normalization" in row.get("operator_family", "") or "source_normalization" in row.get("coefficient_symbol", "")
    ]
    local_source_norm = [
        row for row in local_rows
        if row.get("component_id", "") == "LRV_DOMAIN_R11_SOURCE_NORMALIZATION"
    ]

    return [
        {
            "rule_id": "V495_0_sources",
            "rule": "all cited source paths exist",
            "result": "pass" if not missing_sources else "fail",
            "evidence": f"missing_sources={len(missing_sources)}",
            "claim_effect": "traceability only",
        },
        {
            "rule_id": "V495_1_inputs_loaded",
            "rule": "494 hard rows, 494 coefficient branch, R11 vector, and local residual vector are loaded",
            "result": "pass" if len(hard_rows) >= 4 and len(coeff_rows) >= 7 and len(r11_rows) >= 5 and len(local_rows) >= 7 else "fail",
            "evidence": f"hard_rows={len(hard_rows)};coeff_rows={len(coeff_rows)};r11_rows={len(r11_rows)};local_rows={len(local_rows)}",
            "claim_effect": "source-normalization gate tied to active residuals",
        },
        {
            "rule_id": "V495_2_R11_source_row_present",
            "rule": "R11 vector includes source-normalization operator row",
            "result": "pass" if source_norm_rows else "fail",
            "evidence": f"source_norm_R11_rows={len(source_norm_rows)}",
            "claim_effect": "hard row is concretely wired",
        },
        {
            "rule_id": "V495_3_local_R11_row_present",
            "rule": "local residual vector includes LRV_DOMAIN_R11_SOURCE_NORMALIZATION",
            "result": "pass" if local_source_norm else "fail",
            "evidence": f"local_source_norm_rows={len(local_source_norm)}",
            "claim_effect": "Newton blocker is in active local vector",
        },
        {
            "rule_id": "V495_4_even_odd_split_written",
            "rule": "even observed source, odd extra source, and even extra source are separated",
            "result": "pass" if len(EVEN_ODD_SPLIT_ROWS) == 4 else "fail",
            "evidence": f"even_odd_rows={len(EVEN_ODD_SPLIT_ROWS)}",
            "claim_effect": "prevents exchange-odd overclaim",
        },
        {
            "rule_id": "V495_5_no_claim_rows",
            "rule": "no theorem, channel, or coefficient fill row is claim-valid",
            "result": "pass" if not claim_theorem_rows and not claim_channel_rows and not claim_fill_rows else "fail",
            "evidence": f"claim_theorem_rows={len(claim_theorem_rows)};claim_channel_rows={len(claim_channel_rows)};claim_fill_rows={len(claim_fill_rows)}",
            "claim_effect": "no Newton/local-GR promotion",
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
    return f"""# 495 - Source Normalization Even Scalar Theorem Or Coefficient Fill

Private Newton/source-normalization checkpoint. This is not a public Newtonian-limit proof, EH-only proof, R11 pass, PPN pass, alpha3 pass, mu_extra-zero pass, local-GR derivation, cosmology result, EM result, or unified-field claim.

## 1. Purpose

Checkpoint `494` showed that exchange-doublet oddness cannot simply kill source normalization, because observed measured `GM` is an exchange-even scalar.

This checkpoint writes the exact theorem stack needed for source-normalized Newtonian recovery and keeps the R11 coefficients retained where the theorem is missing.

Short answer:

```text
Exchange oddness can only help with odd extra source charge.
It does not kill even source-normalization offsets.
The required same-frame EH/Gauss-law/source theorem is written but not satisfied by the current corpus.
```

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/source_normalization_even_scalar_theorem_or_coefficient_fill.py` |
| Run directory | `{run_dir.relative_to(ROOT)}` |
| Timestamp | `{timestamp}` |
| Generated UTC | `{generated_at_utc}` |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## 3. Source Register

{markdown_table(sources)}

## 4. Theorem Stack

{markdown_table(THEOREM_STACK_ROWS)}

The Newton/source-normalization gate is:

```text
mu_obs = G_EH M_EH + mu_extra
```

and the branch only becomes source-normalized Newton if:

```text
mu_extra = 0
```

or every piece of `mu_extra` is explicitly bounded with units, normalization, weak-field map, and source path.

## 5. Even/Odd Split

{markdown_table(EVEN_ODD_SPLIT_ROWS)}

## 6. Source-Normalization Channel Audit

{markdown_table(CHANNEL_AUDIT_ROWS)}

## 7. Coefficient Fill

{markdown_table(COEFFICIENT_FILL_ROWS)}

## 8. Validation

{markdown_table(validations)}

## 9. Decision

{markdown_table(DECISION_ROWS)}

## 10. Route Update

{markdown_table(ROUTE_UPDATE_ROWS)}

## 11. Claim Ceiling

Allowed:

```text
The source-normalized Newton theorem stack is explicit.
Exchange oddness is insufficient for even measured-GM offsets.
R11/source-normalization coefficients remain retained until theorem-zero or numeric fill.
```

Forbidden:

```text
MTS has derived source-normalized Newtonian recovery.
MTS has derived mu_extra=0.
MTS has derived R11 silence.
MTS has derived EH-only local exterior or PPN recovery.
MTS has derived local GR.
```

## 12. Next Queue

| Priority | Target | Reason |
| --- | --- | --- |
| 1 | `{NEXT_TARGET}` | turn the R11 source-normalization operator vector into either derived-zero rows or minimum coefficient rows |
| 2 | extra-stress theorem | Y6 still blocks EH-only local exterior |
| 3 | boundary/domain odd-charge theorem | needed for Y2/Y3 conditional routes |
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timestamp", default=datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S"))
    args = parser.parse_args()

    generated_at_utc = datetime.now(timezone.utc).isoformat()
    run_dir = ROOT / "runs" / f"{args.timestamp}-source-normalization-even-scalar-theorem-or-coefficient-fill"
    run_dir.mkdir(parents=True, exist_ok=True)

    sources = source_rows()
    validations = validation_rows(sources)

    write_csv(SOURCE_REGISTER_PATH, sources)
    write_csv(THEOREM_STACK_PATH, THEOREM_STACK_ROWS)
    write_csv(EVEN_ODD_SPLIT_PATH, EVEN_ODD_SPLIT_ROWS)
    write_csv(CHANNEL_AUDIT_PATH, CHANNEL_AUDIT_ROWS)
    write_csv(COEFFICIENT_FILL_PATH, COEFFICIENT_FILL_ROWS)
    write_csv(VALIDATION_PATH, validations)
    write_csv(DECISION_PATH, DECISION_ROWS)
    write_csv(ROUTE_UPDATE_PATH, ROUTE_UPDATE_ROWS)

    doc = build_doc(args.timestamp, generated_at_utc, run_dir, sources, validations)
    (ROOT / DOC_PATH).write_text(doc, encoding="utf-8")

    missing_sources = [row["source_file"] for row in sources if row["exists"] != "True"]
    failed_validations = [row for row in validations if row["result"] == "fail"]
    claim_theorem_rows = [row for row in THEOREM_STACK_ROWS if row["valid_for_claim"] == "true"]
    claim_channel_rows = [row for row in CHANNEL_AUDIT_ROWS if row["valid_for_claim"] == "true"]
    claim_fill_rows = [row for row in COEFFICIENT_FILL_ROWS if row["valid_for_claim"] == "true"]
    missing_fill_rows = [row for row in COEFFICIENT_FILL_ROWS if row["status"] in {"missing", "conditional_not_parent_owned"}]
    status = {
        "timestamp": args.timestamp,
        "generated_at_utc": generated_at_utc,
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "checkpoint_doc": str(DOC_PATH),
        "run_dir": str(run_dir),
        "source_register": str(ROOT / SOURCE_REGISTER_PATH),
        "theorem_stack": str(ROOT / THEOREM_STACK_PATH),
        "even_odd_split": str(ROOT / EVEN_ODD_SPLIT_PATH),
        "channel_audit": str(ROOT / CHANNEL_AUDIT_PATH),
        "coefficient_fill": str(ROOT / COEFFICIENT_FILL_PATH),
        "validation": str(ROOT / VALIDATION_PATH),
        "decision": str(ROOT / DECISION_PATH),
        "route_update": str(ROOT / ROUTE_UPDATE_PATH),
        "source_rows": len(sources),
        "source_paths_missing": len(missing_sources),
        "missing_sources": missing_sources,
        "theorem_stack_rows": len(THEOREM_STACK_ROWS),
        "even_odd_split_rows": len(EVEN_ODD_SPLIT_ROWS),
        "channel_audit_rows": len(CHANNEL_AUDIT_ROWS),
        "coefficient_fill_rows": len(COEFFICIENT_FILL_ROWS),
        "failed_validation_rows": len(failed_validations),
        "claim_theorem_rows": len(claim_theorem_rows),
        "claim_channel_rows": len(claim_channel_rows),
        "claim_fill_rows": len(claim_fill_rows),
        "missing_or_conditional_fill_rows": len(missing_fill_rows),
        "source_normalization_theorem_stack_written": True,
        "exchange_odd_insufficient_for_even_mu_extra": True,
        "same_frame_EH_Gauss_law_derived": False,
        "constant_kappa_derived": False,
        "mu_extra_zero_derived": False,
        "R11_coefficients_retained": True,
        "source_normalized_Newton_promoted": False,
        "R11_silence_derived": False,
        "PPN_promoted": False,
        "alpha3_passed": False,
        "local_GR_claim_allowed": False,
        "next_target": NEXT_TARGET,
    }
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
