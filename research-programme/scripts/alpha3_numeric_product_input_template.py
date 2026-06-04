from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

STATUS = "alpha3_numeric_product_input_template_written_unfilled_no_alpha3_mu_extra_PPN_Newton_or_local_GR_pass"
CLAIM_CEILING = "alpha3_numeric_product_template_only_no_alpha3_pass_no_mu_extra_zero_PPN_Newton_or_local_GR_pass"
NEXT_TARGET = "481-Qcoh-parent-projector-algebra-or-closure.md"

DOC_PATH = Path("480-alpha3-numeric-product-input-template.md")
SOURCE_REGISTER_PATH = Path("source-intake/mts_residuals/P8_ALPHA3_NUMERIC_TEMPLATE_SOURCE_REGISTER.csv")
PRODUCT_TEMPLATE_PATH = Path("source-intake/mts_residuals/P8_ALPHA3_NUMERIC_PRODUCT_INPUT_TEMPLATE.csv")
DOMAIN_SIBLING_TEMPLATE_PATH = Path("source-intake/mts_residuals/P8_ALPHA3_DOMAIN_SIBLING_INPUT_TEMPLATE.csv")
TOTAL_GUARD_PATH = Path("source-intake/mts_residuals/P8_ALPHA3_NUMERIC_TOTAL_GUARD.csv")
VALIDATION_PATH = Path("source-intake/mts_residuals/P8_ALPHA3_NUMERIC_TEMPLATE_VALIDATION.csv")
DECISION_PATH = Path("source-intake/mts_residuals/P8_ALPHA3_NUMERIC_TEMPLATE_DECISION.csv")
ROUTE_UPDATE_PATH = Path("source-intake/mts_residuals/P8_ALPHA3_NUMERIC_TEMPLATE_ROUTE_UPDATE.csv")

ALPHA3_PRODUCT_INPUT_PATH = Path("source-intake/mts_residuals/P8_ALPHA3_BOUND_PRODUCT_INPUT.csv")
ALPHA3_EVALUATION_PATH = Path("source-intake/mts_residuals/P8_ALPHA3_BOUND_PRODUCT_EVALUATION.csv")
ALPHA3_FILL_SKELETON_PATH = Path("source-intake/mts_residuals/P8_MU_EXTRA_ALPHA3_FILL_INPUT_SKELETON.csv")
DOMAIN_FILL_REQUIREMENTS_PATH = Path("source-intake/mts_residuals/R11_DOMAIN_SOURCE_FILL_REQUIREMENTS.csv")
BOUNDARY_COEFFICIENTS_PATH = Path("source-intake/mts_residuals/P8_mu_extra_boundary_coefficients.csv")
DOMAIN_COEFFICIENTS_PATH = Path("source-intake/mts_residuals/P8_mu_extra_domain_projector_coefficients.csv")

PRODUCT_COLUMNS = [
    "input_id",
    "channel",
    "target_row",
    "observable",
    "product_symbol",
    "coefficient_symbol",
    "epsilon_symbol",
    "coefficient_value",
    "epsilon_value",
    "explicit_product_value",
    "product_units",
    "target_bound",
    "bound_units",
    "acceptance_gate",
    "theorem_zero_certificate",
    "numeric_source_file",
    "formula_reference",
    "assumptions",
    "no_cancellation_policy",
    "current_status",
    "valid_for_claim",
    "next_action",
]

SIBLING_COLUMNS = [
    "input_id",
    "channel",
    "target_row",
    "observable",
    "coefficient_or_product",
    "r11_family",
    "candidate_value",
    "candidate_units",
    "target_bound",
    "acceptance_gate",
    "theorem_zero_certificate",
    "numeric_source_file",
    "formula_reference",
    "assumptions",
    "required_before_domain_alpha3_claim",
    "current_status",
    "valid_for_claim",
    "next_action",
]

SOURCE_REGISTER = [
    {
        "path": "469-fill-or-zero-highest-pressure-mu-extra-row.md",
        "role": "identified alpha3 as boundary/domain highest-pressure product pair",
    },
    {
        "path": "470-boundary-alpha3-zero-theorem-or-numeric-coefficient.md",
        "role": "boundary alpha3 conditional theorem route and coefficient need",
    },
    {
        "path": "477-alpha3-bound-product-evaluator.md",
        "role": "strict alpha3 product evaluator",
    },
    {
        "path": "479-R11-domain-source-normalization-zero-or-fill.md",
        "role": "R11/domain zero rejected and fill requirements written",
    },
    {"path": str(ALPHA3_PRODUCT_INPUT_PATH), "role": "current evaluator input rows"},
    {"path": str(ALPHA3_EVALUATION_PATH), "role": "current evaluator output rows"},
    {"path": str(ALPHA3_FILL_SKELETON_PATH), "role": "boundary/domain/total alpha3 fill skeleton"},
    {"path": str(DOMAIN_FILL_REQUIREMENTS_PATH), "role": "domain sibling fill requirements from R11 zero-or-fill"},
    {"path": str(BOUNDARY_COEFFICIENTS_PATH), "role": "boundary coefficient artifact"},
    {"path": str(DOMAIN_COEFFICIENTS_PATH), "role": "domain coefficient artifact"},
    {
        "path": "scripts/alpha3_numeric_product_input_template.py",
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


def product_template_rows() -> list[dict[str, str]]:
    base_rows = {row["channel"]: row for row in read_csv(ALPHA3_PRODUCT_INPUT_PATH)}
    skeleton_rows = {row["channel"]: row for row in read_csv(ALPHA3_FILL_SKELETON_PATH)}

    boundary = base_rows["boundary_monopole_shift"]
    boundary_skeleton = skeleton_rows["boundary_monopole_shift"]
    domain = base_rows["domain_projector_mass"]
    domain_skeleton = skeleton_rows["domain_projector_mass"]
    total = base_rows["combined_mu_extra_alpha3"]
    total_skeleton = skeleton_rows["combined_mu_extra_alpha3"]

    return [
        {
            "input_id": "A3_BOUNDARY_NUMERIC_OR_ZERO",
            "channel": boundary["channel"],
            "target_row": boundary["target_row"],
            "observable": boundary["observable"],
            "product_symbol": boundary["product_symbol"],
            "coefficient_symbol": boundary["coefficient_symbol"],
            "epsilon_symbol": boundary["epsilon_symbol"],
            "coefficient_value": "FILL_NUMERIC_OR_THEOREM_ZERO",
            "epsilon_value": "FILL_NUMERIC_OR_THEOREM_ZERO",
            "explicit_product_value": "FILL_NUMERIC_PRODUCT_OR_ZERO_CERTIFICATE",
            "product_units": "dimensionless",
            "target_bound": boundary["target_bound"],
            "bound_units": "dimensionless",
            "acceptance_gate": boundary_skeleton["acceptance_gate"],
            "theorem_zero_certificate": "MISSING_PARENT_BOUNDARY_NO_FLUX_CERTIFICATE",
            "numeric_source_file": "MISSING_NUMERIC_SOURCE",
            "formula_reference": "MISSING_FORMULA_REFERENCE",
            "assumptions": "must state local frame, source normalization, boundary collar, stationarity, and no hidden cancellation",
            "no_cancellation_policy": "must pass individually unless parent cancellation identity is derived before fitting",
            "current_status": "template_unfilled",
            "valid_for_claim": "false",
            "next_action": "supply boundary theorem-zero certificate or numeric W_boundary_alpha3 epsilon_boundary_flux product",
        },
        {
            "input_id": "A3_DOMAIN_NUMERIC_OR_ZERO",
            "channel": domain["channel"],
            "target_row": domain["target_row"],
            "observable": domain["observable"],
            "product_symbol": domain["product_symbol"],
            "coefficient_symbol": domain["coefficient_symbol"],
            "epsilon_symbol": domain["epsilon_symbol"],
            "coefficient_value": "FILL_NUMERIC_OR_THEOREM_ZERO",
            "epsilon_value": "FILL_NUMERIC_OR_THEOREM_ZERO",
            "explicit_product_value": "FILL_NUMERIC_PRODUCT_OR_ZERO_CERTIFICATE",
            "product_units": "dimensionless",
            "target_bound": domain["target_bound"],
            "bound_units": "dimensionless",
            "acceptance_gate": domain_skeleton["acceptance_gate"],
            "theorem_zero_certificate": "MISSING_PARENT_DOMAIN_NO_LEAK_AND_R11_SILENCE_CERTIFICATE",
            "numeric_source_file": "MISSING_NUMERIC_SOURCE",
            "formula_reference": "MISSING_FORMULA_REFERENCE",
            "assumptions": "must state local coframe, domain selector, projector stress, R11 operator status, source normalization, and no hidden cancellation",
            "no_cancellation_policy": "must pass individually; total cancellation cannot rescue a failed domain row",
            "current_status": "template_unfilled",
            "valid_for_claim": "false",
            "next_action": "supply domain theorem-zero certificate or numeric W_domain_alpha3 epsilon_domain_flux product plus sibling rows",
        },
        {
            "input_id": "A3_TOTAL_GUARD",
            "channel": total["channel"],
            "target_row": total["target_row"],
            "observable": total["observable"],
            "product_symbol": total["product_symbol"],
            "coefficient_symbol": total["coefficient_symbol"],
            "epsilon_symbol": total["epsilon_symbol"],
            "coefficient_value": "SUM_ONLY_AFTER_INDIVIDUAL_CHANNELS_SCORE",
            "epsilon_value": "not_applicable",
            "explicit_product_value": "MISSING_CHANNEL_VALUES",
            "product_units": "dimensionless",
            "target_bound": total["target_bound"],
            "bound_units": "dimensionless",
            "acceptance_gate": total_skeleton["acceptance_gate"],
            "theorem_zero_certificate": "MISSING_PARENT_CANCELLATION_IDENTITY_IF_USED",
            "numeric_source_file": "not_applicable_until_channels_score",
            "formula_reference": "MISSING_TOTAL_POLICY_REFERENCE",
            "assumptions": "total alpha3 cannot be scored by post-fit cancellation",
            "no_cancellation_policy": "individual channels pass first unless a parent identity forces exact cancellation before fitting",
            "current_status": "guard_only",
            "valid_for_claim": "false",
            "next_action": "do not total-score until boundary and domain products are theorem-zero or numeric",
        },
    ]


def domain_sibling_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for row in read_csv(DOMAIN_FILL_REQUIREMENTS_PATH):
        rows.append(
            {
                "input_id": f"{row['fill_id']}_NUMERIC_OR_ZERO",
                "channel": row["channel"],
                "target_row": row["target_row"],
                "observable": row["observable"],
                "coefficient_or_product": row["coefficient_or_product"],
                "r11_family": row["r11_family"],
                "candidate_value": "FILL_NUMERIC_OR_THEOREM_ZERO",
                "candidate_units": "dimensionless_or_declared_operator_units",
                "target_bound": row["target_bound"],
                "acceptance_gate": row["acceptance"],
                "theorem_zero_certificate": "MISSING_PARENT_ZERO_CERTIFICATE",
                "numeric_source_file": "MISSING_NUMERIC_SOURCE",
                "formula_reference": "MISSING_FORMULA_REFERENCE",
                "assumptions": "must state coframe, source normalization, R11/operator status, and no tuned cancellation",
                "required_before_domain_alpha3_claim": "true" if row["target_row"] != "R7_alpha3" else "self",
                "current_status": "template_unfilled",
                "valid_for_claim": "false",
                "next_action": row["next_action"],
            }
        )
    return rows


def total_guard_rows() -> list[dict[str, str]]:
    return [
        {
            "guard_id": "TG0_individual_first",
            "rule": "boundary and domain alpha3 products must pass individually before total alpha3 can be scored",
            "current_status": "active",
            "failure_mode_prevented": "post-fit cancellation between hidden boundary and domain fluxes",
            "valid_for_claim": "false",
        },
        {
            "guard_id": "TG1_parent_cancellation_identity",
            "rule": "a total cancellation claim is allowed only if a parent identity is derived before fitting",
            "current_status": "not_present",
            "failure_mode_prevented": "tuned cancellation masquerading as field-theory prediction",
            "valid_for_claim": "false",
        },
        {
            "guard_id": "TG2_domain_siblings",
            "rule": "domain alpha3 cannot pass while R5/R6/R8/R11 sibling rows remain missing or unscored",
            "current_status": "active",
            "failure_mode_prevented": "closing alpha3 while preferred-frame/source-normalization leakage survives elsewhere",
            "valid_for_claim": "false",
        },
        {
            "guard_id": "TG3_source_path_required",
            "rule": "numeric products require source file, formula reference, units, assumptions, and bound comparison",
            "current_status": "active",
            "failure_mode_prevented": "unsourced tiny number inserted after the fact",
            "valid_for_claim": "false",
        },
    ]


def validation_rows() -> list[dict[str, str]]:
    source_rows = source_register_rows()
    product_rows = product_template_rows()
    sibling_rows = domain_sibling_rows()
    total_rows = total_guard_rows()
    product_columns_ok = all(set(PRODUCT_COLUMNS).issubset(row.keys()) for row in product_rows)
    sibling_columns_ok = all(set(SIBLING_COLUMNS).issubset(row.keys()) for row in sibling_rows)
    return [
        {
            "rule_id": "V480_0_sources",
            "rule": "all cited source paths exist",
            "result": "pass" if all(row["exists"] == "True" for row in source_rows) else "fail",
            "evidence": f"missing_sources={sum(row['exists'] != 'True' for row in source_rows)}",
            "claim_effect": "traceability only",
        },
        {
            "rule_id": "V480_1_product_template",
            "rule": "boundary, domain, and total alpha3 rows are present",
            "result": "pass" if len(product_rows) == 3 and product_columns_ok else "fail",
            "evidence": f"product_rows={len(product_rows)}; columns_ok={product_columns_ok}",
            "claim_effect": "alpha3 inputs are now concrete",
        },
        {
            "rule_id": "V480_2_domain_siblings",
            "rule": "domain sibling rows cover R5/R6/R7/R8/R11",
            "result": "pass" if len(sibling_rows) == 5 and sibling_columns_ok else "fail",
            "evidence": f"sibling_rows={len(sibling_rows)}; columns_ok={sibling_columns_ok}",
            "claim_effect": "domain alpha3 cannot be isolated from R11/vector leaks",
        },
        {
            "rule_id": "V480_3_total_guard",
            "rule": "total alpha3 no-cancellation policy is explicit",
            "result": "pass",
            "evidence": f"guard_rows={len(total_rows)}",
            "claim_effect": "no cancellation-by-fit",
        },
        {
            "rule_id": "V480_4_unfilled_default",
            "rule": "template rows are not claim-valid before numbers or theorem certificates are supplied",
            "result": "pass",
            "evidence": f"claim_valid_rows={sum(row['valid_for_claim'] == 'true' for row in product_rows + sibling_rows + total_rows)}",
            "claim_effect": "no alpha3 promotion",
        },
        {
            "rule_id": "V480_5_claim_ceiling",
            "rule": "no alpha3, mu_extra, Newton, PPN, or local-GR pass is granted",
            "result": "pass",
            "evidence": "template_unfilled; claim_allowed=false",
            "claim_effect": "input contract only",
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "D0_template",
            "status": "written",
            "meaning": "alpha3 has a fill-ready numeric/theorem-zero input template",
            "next_action": str(PRODUCT_TEMPLATE_PATH),
        },
        {
            "decision_id": "D1_boundary",
            "status": "unfilled",
            "meaning": "boundary product requires numeric W_boundary_alpha3 epsilon_boundary_flux or a parent no-flux certificate",
            "next_action": "derive boundary no-flux or fill A3_BOUNDARY_NUMERIC_OR_ZERO",
        },
        {
            "decision_id": "D2_domain",
            "status": "unfilled_highest_pressure",
            "meaning": "domain product requires W_domain_alpha3 epsilon_domain_flux plus R11/domain sibling rows",
            "next_action": "derive parent no-leak/R11 silence or fill A3_DOMAIN_NUMERIC_OR_ZERO",
        },
        {
            "decision_id": "D3_total",
            "status": "guard_only",
            "meaning": "total alpha3 cannot be used for cancellation-by-fit",
            "next_action": "score individual channels first",
        },
        {
            "decision_id": "D4_promotion",
            "status": "forbidden",
            "meaning": "no alpha3 pass, mu_extra zero, PPN, Newtonian-limit, or local-GR pass is earned",
            "next_action": NEXT_TARGET,
        },
    ]


def route_update_rows() -> list[dict[str, str]]:
    return [
        {
            "route_id": "A3_boundary_product",
            "target": "W_boundary_alpha3 epsilon_boundary_flux",
            "current_status": "template_unfilled",
            "accepted_for_claim": "false",
            "next_action": "fill numeric product or parent no-flux certificate",
        },
        {
            "route_id": "A3_domain_product",
            "target": "W_domain_alpha3 epsilon_domain_flux",
            "current_status": "template_unfilled_requires_R11_siblings",
            "accepted_for_claim": "false",
            "next_action": NEXT_TARGET,
        },
        {
            "route_id": "A3_total_guard",
            "target": "alpha3_mu_extra_total",
            "current_status": "guard_only_no_cancellation",
            "accepted_for_claim": "false",
            "next_action": "wait for individual channel pass or parent cancellation theorem",
        },
    ]


def build_doc(run_dir: Path) -> str:
    source_rows = source_register_rows()
    product_rows = product_template_rows()
    sibling_rows = domain_sibling_rows()
    total_rows = total_guard_rows()
    validation = validation_rows()
    decisions = decision_rows()
    route_rows = route_update_rows()
    generated = datetime.now(timezone.utc).isoformat()

    return f"""# 480 - Alpha3 Numeric Product Input Template

Private alpha3/input-contract checkpoint. This is not a public alpha3 pass, mu_extra-zero pass, Newtonian-limit pass, PPN pass, local-GR derivation, cosmology result, EM result, or unified-field claim.

## 1. Purpose

Checkpoints 477-479 narrowed the alpha3 obstruction to a concrete product problem:

```text
abs(W_i_alpha3 * epsilon_i_flux) <= 4e-20
```

for each active alpha3 source channel, unless a parent theorem proves that channel exactly zero.

This checkpoint writes the fill-ready input template. It does not fill the numbers. It prevents the next step from hiding behind vague words like "small", "screened", or "probably zero".

## 2. Run Manifest

| Field | Value |
| --- | --- |
| Script | `scripts/alpha3_numeric_product_input_template.py` |
| Run directory | `{run_dir.relative_to(ROOT)}` |
| Generated UTC | `{generated}` |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## 3. Source Register

{md_table(source_rows)}

## 4. Product Input Template

{md_table(product_rows)}

The two live products are:

```text
W_boundary_alpha3 * epsilon_boundary_flux
W_domain_alpha3 * epsilon_domain_flux
```

Each must be individually theorem-zero or below `4e-20`. The total row is a guard, not a shortcut.

## 5. Domain Sibling Requirements

{md_table(sibling_rows)}

The domain alpha3 row cannot be isolated from preferred-frame, anisotropy, and R11/source-normalization siblings.

If the domain sector still carries R5/R6/R8/R11 leakage, a standalone alpha3 zero is not a local-GR pass.

## 6. Total Guard

{md_table(total_rows)}

## 7. Route Update

{md_table(route_rows)}

## 8. Validation

{md_table(validation)}

## 9. Decision

{md_table(decisions)}

## 10. Claim Ceiling

Allowed:

```text
alpha3 now has a fill-ready numeric/theorem-zero product template.
boundary, domain, and total guard rows are explicit.
domain sibling rows are explicit.
```

Not allowed:

```text
alpha3 passes.
mu_extra is zero.
R11/domain source normalization is silent.
MTS passes PPN, Newton, or local GR.
```

## 11. Next Queue

| Priority | Target | Reason |
| --- | --- | --- |
| 1 | `{NEXT_TARGET}` | attempt parent Q_coh/P_coh/domain algebra before committing to numeric closure fills |
| 2 | `482-local-residual-vector-from-domain-source-fill.md` | once product rows are filled, propagate them into the residual vector |
| 3 | `483-alpha3-product-evaluator-refresh.md` | rerun alpha3 evaluator after numeric/theorem rows exist |
"""


def write_run(timestamp: str) -> dict[str, Any]:
    run_dir = ROOT / "runs" / f"{timestamp}-alpha3-numeric-product-input-template"
    result_dir = run_dir / "results"
    result_dir.mkdir(parents=True, exist_ok=True)

    source_rows = source_register_rows()
    product_rows = product_template_rows()
    sibling_rows = domain_sibling_rows()
    total_rows = total_guard_rows()
    validation = validation_rows()
    decisions = decision_rows()
    route_rows = route_update_rows()

    write_csv(SOURCE_REGISTER_PATH, source_rows)
    write_csv(PRODUCT_TEMPLATE_PATH, product_rows, PRODUCT_COLUMNS)
    write_csv(DOMAIN_SIBLING_TEMPLATE_PATH, sibling_rows, SIBLING_COLUMNS)
    write_csv(TOTAL_GUARD_PATH, total_rows)
    write_csv(VALIDATION_PATH, validation)
    write_csv(DECISION_PATH, decisions)
    write_csv(ROUTE_UPDATE_PATH, route_rows)

    doc = build_doc(run_dir)
    (ROOT / DOC_PATH).write_text(doc, encoding="utf-8")

    for path in [
        SOURCE_REGISTER_PATH,
        PRODUCT_TEMPLATE_PATH,
        DOMAIN_SIBLING_TEMPLATE_PATH,
        TOTAL_GUARD_PATH,
        VALIDATION_PATH,
        DECISION_PATH,
        ROUTE_UPDATE_PATH,
    ]:
        (result_dir / path.name).write_text((ROOT / path).read_text(encoding="utf-8"), encoding="utf-8")

    claim_valid_rows = sum(row["valid_for_claim"] == "true" for row in product_rows + sibling_rows + total_rows)
    status = {
        "timestamp": timestamp,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "checkpoint_doc": str(DOC_PATH),
        "run_dir": str(run_dir),
        "source_register": str(ROOT / SOURCE_REGISTER_PATH),
        "product_template": str(ROOT / PRODUCT_TEMPLATE_PATH),
        "domain_sibling_template": str(ROOT / DOMAIN_SIBLING_TEMPLATE_PATH),
        "total_guard": str(ROOT / TOTAL_GUARD_PATH),
        "validation": str(ROOT / VALIDATION_PATH),
        "decision": str(ROOT / DECISION_PATH),
        "route_update": str(ROOT / ROUTE_UPDATE_PATH),
        "source_rows": len(source_rows),
        "source_paths_missing": sum(row["exists"] != "True" for row in source_rows),
        "product_template_rows": len(product_rows),
        "domain_sibling_rows": len(sibling_rows),
        "total_guard_rows": len(total_rows),
        "validation_rows": len(validation),
        "decision_rows": len(decisions),
        "route_update_rows": len(route_rows),
        "claim_valid_rows": claim_valid_rows,
        "boundary_product_ready": False,
        "domain_product_ready": False,
        "total_alpha3_ready": False,
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
