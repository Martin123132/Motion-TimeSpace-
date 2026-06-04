from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

STATUS = "R11_domain_source_normalization_zero_or_fill_written_zero_route_failed_fill_required_no_alpha3_PPN_Newton_or_local_GR_pass"
CLAIM_CEILING = "R11_domain_source_zero_or_fill_only_no_R11_pass_no_domain_alpha3_pass_no_mu_extra_zero_PPN_Newton_or_local_GR_pass"
NEXT_TARGET = "480-alpha3-numeric-product-input-template.md"

DOC_PATH = Path("479-R11-domain-source-normalization-zero-or-fill.md")
SOURCE_REGISTER_PATH = Path("source-intake/mts_residuals/R11_DOMAIN_SOURCE_ZERO_OR_FILL_SOURCE_REGISTER.csv")
THEOREM_ATTEMPT_PATH = Path("source-intake/mts_residuals/R11_DOMAIN_SOURCE_THEOREM_ZERO_ATTEMPT.csv")
ZERO_OR_FILL_GATE_PATH = Path("source-intake/mts_residuals/R11_DOMAIN_SOURCE_ZERO_OR_FILL_GATE.csv")
FILL_REQUIREMENTS_PATH = Path("source-intake/mts_residuals/R11_DOMAIN_SOURCE_FILL_REQUIREMENTS.csv")
VALIDATION_PATH = Path("source-intake/mts_residuals/R11_DOMAIN_SOURCE_ZERO_OR_FILL_VALIDATION.csv")
DECISION_PATH = Path("source-intake/mts_residuals/R11_DOMAIN_SOURCE_ZERO_OR_FILL_DECISION.csv")
ROUTE_UPDATE_PATH = Path("source-intake/mts_residuals/P8_ALPHA3_R11_DOMAIN_SOURCE_ROUTE_UPDATE.csv")

R11_EXECUTABLE_PATH = Path("source-intake/mts_residuals/R11_nonEH_operator_vector_executable.csv")
R11_DOMAIN_PATH = Path("source-intake/mts_residuals/R11_DOMAIN_PROJECTOR_OPERATOR_VECTOR_MINIMUM.csv")
R11_MU_EXTRA_LINK_PATH = Path("source-intake/mts_residuals/R11_MU_EXTRA_SOURCE_NORMALIZATION_LINK.csv")
DOMAIN_COEFFICIENTS_PATH = Path("source-intake/mts_residuals/P8_mu_extra_domain_projector_coefficients.csv")
DOMAIN_R11_LINK_PATH = Path("source-intake/mts_residuals/P8_DOMAIN_ALPHA3_R11_LINK.csv")
ALPHA3_PRODUCT_INPUT_PATH = Path("source-intake/mts_residuals/P8_ALPHA3_BOUND_PRODUCT_INPUT.csv")
ALPHA3_PRODUCT_EVALUATION_PATH = Path("source-intake/mts_residuals/P8_ALPHA3_BOUND_PRODUCT_EVALUATION.csv")

DOMAIN_OPERATOR_FAMILIES = {
    "vector_preferred_frame",
    "source_normalization_operator",
    "projector_domain_stress",
}

SOURCE_REGISTER = [
    {
        "path": "438-R11-nonEH-coefficient-vector-contract.md",
        "role": "global non-EH/R11 operator vector contract",
    },
    {
        "path": "463-EH-only-or-R11-executable-vector-gate.md",
        "role": "EH-only versus R11 executable vector fork",
    },
    {
        "path": "464-R11-executable-vector-minimum-fill-skeleton.md",
        "role": "minimum R11 skeleton and validation rules",
    },
    {
        "path": "472-domain-projector-alpha3-no-leak-or-R11-link.md",
        "role": "domain alpha3 no-leak route and R11 dependency",
    },
    {
        "path": "473-R11-domain-projector-operator-vector-minimum-fill.md",
        "role": "minimum domain/projector R11 rows",
    },
    {
        "path": "474-domain-selector-no-vector-theorem-or-coefficient.md",
        "role": "conditional no-vector theorem target; not parent-derived",
    },
    {
        "path": "475-domain-selector-parent-action-clause-or-coefficient-fill.md",
        "role": "sufficient parent-action clause; not derived from corpus",
    },
    {
        "path": "476-double-zero-memory-coupling-origin-or-coefficient-runner.md",
        "role": "p>=2/double-zero requirement and coefficient runner",
    },
    {
        "path": "477-alpha3-bound-product-evaluator.md",
        "role": "strict alpha3 product evaluator and R11 dependency",
    },
    {
        "path": "478-determinant-current-parent-ownership-or-demotion.md",
        "role": "det(Q_coh) shape clue but no parent-owned theorem-zero",
    },
    {"path": str(R11_EXECUTABLE_PATH), "role": "current R11 executable vector file"},
    {"path": str(R11_DOMAIN_PATH), "role": "domain R11 minimum rows"},
    {"path": str(R11_MU_EXTRA_LINK_PATH), "role": "mu_extra/source-normalization to R11 link"},
    {"path": str(DOMAIN_COEFFICIENTS_PATH), "role": "domain projector coefficient rows"},
    {"path": str(DOMAIN_R11_LINK_PATH), "role": "domain alpha3 to R11 link rows"},
    {"path": str(ALPHA3_PRODUCT_INPUT_PATH), "role": "alpha3 product input rows"},
    {"path": str(ALPHA3_PRODUCT_EVALUATION_PATH), "role": "alpha3 product evaluation rows"},
    {
        "path": "scripts/R11_domain_source_normalization_zero_or_fill.py",
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


def is_true(value: str | Any) -> bool:
    return str(value).strip().lower() == "true"


def row_has_missing_or_retained_debt(row: dict[str, str]) -> bool:
    debt_markers = (
        "MISSING",
        "retained_unfilled",
        "conditional_zero_not_parent_owned",
        "not_parent_derived",
        "not_scoreable",
        "fail",
    )
    text = " | ".join(str(value) for value in row.values())
    return any(marker in text for marker in debt_markers)


def source_register_rows() -> list[dict[str, str]]:
    return [
        {
            "source_file": item["path"],
            "exists": str((ROOT / item["path"]).exists()),
            "role": item["role"],
        }
        for item in SOURCE_REGISTER
    ]


def r11_rows() -> list[dict[str, str]]:
    return read_csv(R11_EXECUTABLE_PATH)


def domain_r11_rows() -> list[dict[str, str]]:
    rows = read_csv(R11_DOMAIN_PATH)
    return [row for row in rows if row.get("operator_family") in DOMAIN_OPERATOR_FAMILIES]


def r11_claimable_rows() -> list[dict[str, str]]:
    return [row for row in r11_rows() if is_true(row.get("valid_for_claim", ""))]


def domain_claimable_rows() -> list[dict[str, str]]:
    return [row for row in domain_r11_rows() if is_true(row.get("valid_for_claim", ""))]


def domain_coefficient_rows() -> list[dict[str, str]]:
    return read_csv(DOMAIN_COEFFICIENTS_PATH)


def domain_coefficient_claimable_rows() -> list[dict[str, str]]:
    return [row for row in domain_coefficient_rows() if is_true(row.get("valid_for_claim", ""))]


def theorem_attempt_rows() -> list[dict[str, str]]:
    return [
        {
            "step_id": "Z0_EH_only_or_R11_silence",
            "claim": "domain source-normalization is zero because the exterior is EH-only or all non-EH R11 rows are silent",
            "required_identity": "S_parent -> E_MTS_munu = 0 or boundary-only through R11 in compact local branch",
            "current_evidence": "463/464/473 leave R11 executable rows parseable but unfilled; valid_for_claim rows = 0",
            "result": "fail_current_corpus",
            "claim_effect": "no R11 theorem-zero",
        },
        {
            "step_id": "Z1_no_domain_vector",
            "claim": "domain selector contributes no preferred-frame/vector source",
            "required_identity": "P_loc^i_mu F_domain^mu = 0 from parent-selected scalar/trivial local domain",
            "current_evidence": "474 gives a conditional no-vector theorem target; 475 supplies a sufficient parent-action clause but not a derived one",
            "result": "conditional_not_parent_derived",
            "claim_effect": "fill alpha1/alpha2/alpha3/xi vector products or derive parent clause",
        },
        {
            "step_id": "Z2_source_normalization_operator_zero",
            "claim": "domain projector contributes no mu_extra/source-normalization operator",
            "required_identity": "delta mu_domain = 0 and derivative hair vanish in measured-GM normalization",
            "current_evidence": "R11_MU_EXTRA_SOURCE_NORMALIZATION_LINK rows are retained_unfilled; P8 domain R11 row is not scoreable",
            "result": "fail_current_corpus",
            "claim_effect": "fill c_domain_source_normalization_operator or derive zero",
        },
        {
            "step_id": "Z3_projector_stress_zero",
            "claim": "projector/domain stress is topological and metric-independent",
            "required_identity": "delta_g P_D = 0, delta_g chi_D = 0, no domain-wall/readout-mask stress through PPN order",
            "current_evidence": "473 marks projector_domain_stress as conditional_zero_not_parent_owned; 478 keeps Q_coh/P_coh/domain ownership open",
            "result": "conditional_not_parent_derived",
            "claim_effect": "fill c_projector_domain_stress or derive parent projector ownership",
        },
        {
            "step_id": "Z4_detQ_current_zero",
            "claim": "det(Q_coh) supplies the R11/domain source zero",
            "required_identity": "parent-owned coherent current J_C selects local trivial class and FLRW active class without shear leakage",
            "current_evidence": "478 finds det(Q_coh) shape-supported but not parent-owned; raw det(Q) leaks tracefree shear",
            "result": "fail_current_corpus",
            "claim_effect": "det(Q_coh) remains theorem target, not R11 silence",
        },
        {
            "step_id": "Z5_domain_alpha3_bridge",
            "claim": "R11 silence closes the domain alpha3 row",
            "required_identity": "W_domain_alpha3 epsilon_domain_flux = 0 or abs(product) <= 4e-20",
            "current_evidence": "477/478 keep A3_domain not_scoreable_inputs_missing; R11_claimable_rows=0",
            "result": "fail_current_corpus",
            "claim_effect": "domain alpha3 remains highest-pressure fill row",
        },
        {
            "step_id": "Z6_verdict",
            "claim": "R11/domain source-normalization is theorem-zero in the current corpus",
            "required_identity": "Z0-Z5 all pass with parent-owned identities",
            "current_evidence": "all active routes remain missing, conditional, retained, or not scoreable",
            "result": "reject_zero_route_require_fill",
            "claim_effect": "write fill requirements; no alpha3, mu_extra, Newton, PPN, or local-GR pass",
        },
    ]


def fill_requirement_rows() -> list[dict[str, str]]:
    link_by_row = {row["domain_row"]: row for row in read_csv(DOMAIN_R11_LINK_PATH)}
    requirements: list[dict[str, str]] = []
    family_by_target = {
        "R5_alpha1": "vector_preferred_frame",
        "R6_alpha2": "vector_preferred_frame",
        "R7_alpha3": "vector_preferred_frame;source_normalization_operator;projector_domain_stress",
        "R8_xi": "projector_domain_stress;vector_preferred_frame",
        "R11_EH_operator_ledger": "source_normalization_operator;projector_domain_stress",
    }
    for row in domain_coefficient_rows():
        target = row["target_row"]
        link = link_by_row.get(target, {})
        requirements.append(
            {
                "fill_id": f"DSR_{target}",
                "channel": row["channel"],
                "target_row": target,
                "observable": row["observable"],
                "r11_family": family_by_target.get(target, "source_normalization_operator"),
                "coefficient_or_product": row["coefficient_symbol"],
                "current_value_or_theorem": row["value_or_theorem"],
                "current_status": row["score_status"],
                "target_bound": row["target_bound"],
                "acceptance": link.get("acceptance", "theorem-zero or numeric/source-bound fill required"),
                "required_artifact": link.get("required_artifact", str(DOMAIN_COEFFICIENTS_PATH)),
                "next_action": "derive parent zero or fill numeric coefficient/product with source path and assumptions",
                "valid_for_claim": "false",
            }
        )
    return requirements


def zero_or_fill_gate_rows() -> list[dict[str, str]]:
    r11_claimable = len(r11_claimable_rows())
    domain_claimable = len(domain_claimable_rows())
    coefficient_claimable = len(domain_coefficient_claimable_rows())
    fill_rows = len(fill_requirement_rows())
    return [
        {
            "gate_id": "G479_0_sources",
            "rule": "all cited source paths exist",
            "result": "pass" if all(row["exists"] == "True" for row in source_register_rows()) else "fail",
            "evidence": f"missing={sum(row['exists'] != 'True' for row in source_register_rows())}",
            "claim_effect": "traceability only",
        },
        {
            "gate_id": "G479_1_R11_claimable",
            "rule": "R11 executable vector has claim-valid rows for domain source silence",
            "result": "fail_for_claim",
            "evidence": f"R11_claimable_rows={r11_claimable}; domain_claimable_rows={domain_claimable}",
            "claim_effect": "R11 silence not accepted",
        },
        {
            "gate_id": "G479_2_domain_coefficients",
            "rule": "domain coefficient rows are either theorem-zero or numeric/source-bound filled",
            "result": "fail_for_claim",
            "evidence": f"domain_coefficient_claimable_rows={coefficient_claimable}",
            "claim_effect": "domain alpha3 and mu_extra rows remain not scoreable",
        },
        {
            "gate_id": "G479_3_no_missing_debt",
            "rule": "domain R11 rows contain no MISSING/retained/conditional debt markers",
            "result": "fail_for_claim",
            "evidence": f"domain_rows_with_debt={sum(row_has_missing_or_retained_debt(row) for row in domain_r11_rows())}",
            "claim_effect": "must fill or derive rows before promotion",
        },
        {
            "gate_id": "G479_4_fill_requirements",
            "rule": "missing rows are converted into explicit fill requirements",
            "result": "pass",
            "evidence": f"fill_requirement_rows={fill_rows}",
            "claim_effect": "next numeric/theorem fill step is concrete",
        },
        {
            "gate_id": "G479_5_claim_ceiling",
            "rule": "no R11/domain source result is promoted while zero route fails",
            "result": "pass",
            "evidence": "zero_route_rejected; fill_required",
            "claim_effect": "no alpha3, mu_extra, Newton, PPN, or local-GR pass",
        },
    ]


def route_update_rows() -> list[dict[str, str]]:
    return [
        {
            "route_id": "R11_domain_source_zero",
            "target": "A3_domain / domain_projector_mass",
            "accepted_as_zero": "false",
            "why_not": "R11 executable rows and domain coefficients contain missing, retained, or conditional debt markers",
            "next_action": NEXT_TARGET,
        },
        {
            "route_id": "R11_domain_source_fill",
            "target": "W_domain_alpha3 epsilon_domain_flux plus R5/R6/R8/R11 siblings",
            "accepted_as_zero": "false",
            "why_not": "zero route not parent-derived; fill template must be numeric or theorem-zero sourced",
            "next_action": "use R11_DOMAIN_SOURCE_FILL_REQUIREMENTS.csv as coefficient/product input contract",
        },
    ]


def validation_rows() -> list[dict[str, str]]:
    source_rows = source_register_rows()
    theorem_rows = theorem_attempt_rows()
    fill_rows = fill_requirement_rows()
    gates = zero_or_fill_gate_rows()
    return [
        {
            "rule_id": "V479_0_sources",
            "rule": "all cited source paths exist",
            "result": "pass" if all(row["exists"] == "True" for row in source_rows) else "fail",
            "evidence": f"missing_sources={sum(row['exists'] != 'True' for row in source_rows)}",
            "claim_effect": "traceability only",
        },
        {
            "rule_id": "V479_1_domain_rows",
            "rule": "three domain/projector R11 rows are loaded",
            "result": "pass" if len(domain_r11_rows()) == 3 else "fail",
            "evidence": f"domain_r11_rows={len(domain_r11_rows())}",
            "claim_effect": "domain source check is targeted",
        },
        {
            "rule_id": "V479_2_zero_rejected",
            "rule": "theorem-zero attempt explicitly rejects promotion",
            "result": "pass",
            "evidence": f"reject_rows={sum(row['result'].startswith(('fail', 'conditional', 'reject')) for row in theorem_rows)}",
            "claim_effect": "no hidden zero claim",
        },
        {
            "rule_id": "V479_3_fill_rows",
            "rule": "fill requirements cover all domain coefficient rows",
            "result": "pass" if len(fill_rows) == len(domain_coefficient_rows()) else "fail",
            "evidence": f"fill_rows={len(fill_rows)}; domain_coeff_rows={len(domain_coefficient_rows())}",
            "claim_effect": "next fill step is complete for domain channel",
        },
        {
            "rule_id": "V479_4_gates",
            "rule": "claim gates fail for promotion and pass for fill-contract creation",
            "result": "pass",
            "evidence": ";".join(f"{row['gate_id']}={row['result']}" for row in gates),
            "claim_effect": "claim ceiling enforced",
        },
        {
            "rule_id": "V479_5_no_promotion",
            "rule": "no alpha3, mu_extra, Newton, PPN, or local-GR promotion is granted",
            "result": "pass",
            "evidence": "claim_allowed=false for all active domain source rows",
            "claim_effect": "private zero-or-fill gate only",
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "D0_R11_zero",
            "status": "not_derived",
            "meaning": "R11/domain source-normalization silence is not theorem-zero in the current corpus",
            "next_action": "do not use R11 as alpha3/PPN evidence",
        },
        {
            "decision_id": "D1_domain_fill",
            "status": "required",
            "meaning": "domain vector/source/projector rows must be filled numerically or by theorem-zero sources",
            "next_action": str(FILL_REQUIREMENTS_PATH),
        },
        {
            "decision_id": "D2_alpha3",
            "status": "not_scoreable",
            "meaning": "W_domain_alpha3 epsilon_domain_flux remains missing or unproved zero",
            "next_action": NEXT_TARGET,
        },
        {
            "decision_id": "D3_mu_extra",
            "status": "not_zero",
            "meaning": "mu_extra/source-normalization operator is retained until c_domain_source_normalization_operator is filled or derived zero",
            "next_action": "carry retained R11 row into local residual vector",
        },
        {
            "decision_id": "D4_promotion",
            "status": "forbidden",
            "meaning": "no R11 pass, alpha3 pass, mu_extra zero, Newtonian-limit pass, PPN pass, or local-GR pass is earned",
            "next_action": NEXT_TARGET,
        },
    ]


def build_doc(run_dir: Path) -> str:
    source_rows = source_register_rows()
    theorem_rows = theorem_attempt_rows()
    gate_rows = zero_or_fill_gate_rows()
    fill_rows = fill_requirement_rows()
    validation = validation_rows()
    decisions = decision_rows()
    route_rows = route_update_rows()
    generated = datetime.now(timezone.utc).isoformat()

    return f"""# 479 - R11 Domain Source Normalization Zero Or Fill

Private R11/domain-source checkpoint. This is not a public R11 pass, alpha3 pass, mu_extra-zero pass, Newtonian-limit pass, PPN pass, local-GR derivation, cosmology result, EM result, or unified-field claim.

## 1. Purpose

Checkpoint 478 left `det(Q_coh)` in the correct place: a strong double-zero/current-shape clue, but not a parent-owned theorem-zero source.

The remaining domain-alpha3 obstruction is therefore not:

```text
find a nicer phrase for det(Q_coh)
```

It is:

```text
prove R11/domain source-normalization silence, or fill the actual coefficient/product rows.
```

This checkpoint attempts the zero route first. It fails in the current corpus. The result is useful because it turns the failure into a concrete fill contract.

## 2. Run Manifest

| Field | Value |
| --- | --- |
| Script | `scripts/R11_domain_source_normalization_zero_or_fill.py` |
| Run directory | `{run_dir.relative_to(ROOT)}` |
| Generated UTC | `{generated}` |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## 3. Source Register

{md_table(source_rows)}

## 4. Zero Attempt

{md_table(theorem_rows)}

The zero route fails for a structural reason:

```text
R11/domain source silence needs parent ownership of the operator, source normalization,
domain selector, projector stress, and local trivial class.
```

The current corpus has useful contracts for those pieces, but not the completed parent-owned identity.

## 5. Zero-Or-Fill Gates

{md_table(gate_rows)}

The gate result is:

```text
zero rejected;
fill required.
```

## 6. Fill Requirements

{md_table(fill_rows)}

These are not optional bookkeeping rows. They are the minimum rows required before the domain channel can score against alpha1/alpha2/alpha3/xi/R11.

The highest pressure row remains:

```text
W_domain_alpha3 * epsilon_domain_flux <= 4e-20
```

unless a parent theorem proves the product is exactly zero.

## 7. Route Update

{md_table(route_rows)}

## 8. Validation

{md_table(validation)}

## 9. Decision

{md_table(decisions)}

## 10. Claim Ceiling

Allowed:

```text
R11/domain source-normalization zero route has been tested and rejected in the current corpus.
The required fill rows are explicit.
The domain alpha3 obstruction is now concrete.
```

Not allowed:

```text
R11 source-normalization is silent.
W_domain_alpha3 epsilon_domain_flux is zero.
MTS passes alpha3, mu_extra zero, Newton, PPN, or local GR.
```

## 11. Next Queue

| Priority | Target | Reason |
| --- | --- | --- |
| 1 | `{NEXT_TARGET}` | turn the fill requirements into a numeric/theorem-zero input template for alpha3 and sibling rows |
| 2 | `481-Qcoh-parent-projector-algebra-or-closure.md` | optional derivation route: parent-own Q_coh/P_coh/domain selector instead of filling coefficients |
| 3 | `482-local-residual-vector-from-domain-source-fill.md` | once filled, propagate domain source rows into local residual vector |
"""


def write_run(timestamp: str) -> dict[str, Any]:
    run_dir = ROOT / "runs" / f"{timestamp}-R11-domain-source-normalization-zero-or-fill"
    result_dir = run_dir / "results"
    result_dir.mkdir(parents=True, exist_ok=True)

    source_rows = source_register_rows()
    theorem_rows = theorem_attempt_rows()
    gate_rows = zero_or_fill_gate_rows()
    fill_rows = fill_requirement_rows()
    validation = validation_rows()
    decisions = decision_rows()
    route_rows = route_update_rows()

    write_csv(SOURCE_REGISTER_PATH, source_rows)
    write_csv(THEOREM_ATTEMPT_PATH, theorem_rows)
    write_csv(ZERO_OR_FILL_GATE_PATH, gate_rows)
    write_csv(FILL_REQUIREMENTS_PATH, fill_rows)
    write_csv(VALIDATION_PATH, validation)
    write_csv(DECISION_PATH, decisions)
    write_csv(ROUTE_UPDATE_PATH, route_rows)

    doc = build_doc(run_dir)
    (ROOT / DOC_PATH).write_text(doc, encoding="utf-8")

    for path in [
        SOURCE_REGISTER_PATH,
        THEOREM_ATTEMPT_PATH,
        ZERO_OR_FILL_GATE_PATH,
        FILL_REQUIREMENTS_PATH,
        VALIDATION_PATH,
        DECISION_PATH,
        ROUTE_UPDATE_PATH,
    ]:
        (result_dir / path.name).write_text((ROOT / path).read_text(encoding="utf-8"), encoding="utf-8")

    status = {
        "timestamp": timestamp,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "checkpoint_doc": str(DOC_PATH),
        "run_dir": str(run_dir),
        "source_register": str(ROOT / SOURCE_REGISTER_PATH),
        "theorem_attempt": str(ROOT / THEOREM_ATTEMPT_PATH),
        "zero_or_fill_gate": str(ROOT / ZERO_OR_FILL_GATE_PATH),
        "fill_requirements": str(ROOT / FILL_REQUIREMENTS_PATH),
        "validation": str(ROOT / VALIDATION_PATH),
        "decision": str(ROOT / DECISION_PATH),
        "route_update": str(ROOT / ROUTE_UPDATE_PATH),
        "source_rows": len(source_rows),
        "source_paths_missing": sum(row["exists"] != "True" for row in source_rows),
        "theorem_rows": len(theorem_rows),
        "gate_rows": len(gate_rows),
        "fill_requirement_rows": len(fill_rows),
        "validation_rows": len(validation),
        "decision_rows": len(decisions),
        "route_update_rows": len(route_rows),
        "R11_claimable_rows": len(r11_claimable_rows()),
        "domain_R11_rows": len(domain_r11_rows()),
        "domain_R11_claimable_rows": len(domain_claimable_rows()),
        "domain_coefficient_rows": len(domain_coefficient_rows()),
        "domain_coefficient_claimable_rows": len(domain_coefficient_claimable_rows()),
        "domain_rows_with_debt": sum(row_has_missing_or_retained_debt(row) for row in domain_r11_rows()),
        "R11_domain_source_zero_accepted": False,
        "fill_required": True,
        "domain_alpha3_score_ready": False,
        "alpha3_passed": False,
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
    status = write_run(args.timestamp)
    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
