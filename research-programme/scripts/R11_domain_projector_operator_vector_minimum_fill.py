from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

STATUS = "R11_domain_projector_operator_vector_minimum_written_parseable_actual_executable_rows_zero_no_Newton_or_local_GR_pass"
CLAIM_CEILING = "R11_domain_projector_vector_wiring_only_no_R11_pass_no_domain_channel_pass_no_mu_extra_zero_PPN_Newton_or_local_GR_pass"
NEXT_TARGET = "474-domain-selector-no-vector-theorem-or-coefficient.md"

DOC_PATH = Path("473-R11-domain-projector-operator-vector-minimum-fill.md")
SOURCE_REGISTER_PATH = Path("source-intake/mts_residuals/R11_DOMAIN_PROJECTOR_SOURCE_REGISTER.csv")
DOMAIN_VECTOR_PATH = Path("source-intake/mts_residuals/R11_DOMAIN_PROJECTOR_OPERATOR_VECTOR_MINIMUM.csv")
EXECUTABLE_VECTOR_PATH = Path("source-intake/mts_residuals/R11_nonEH_operator_vector_executable.csv")
MISSING_LEDGER_PATH = Path("source-intake/mts_residuals/R11_DOMAIN_PROJECTOR_VECTOR_MISSING_LEDGER.csv")
VALIDATION_PATH = Path("source-intake/mts_residuals/R11_DOMAIN_PROJECTOR_VECTOR_VALIDATION.csv")
DECISION_PATH = Path("source-intake/mts_residuals/R11_DOMAIN_PROJECTOR_VECTOR_DECISION.csv")

SKELETON_PATH = Path("source-intake/mts_residuals/R11_MTS_MINIMUM_EXECUTABLE_VECTOR_SKELETON.csv")
R11_LINK_PATH = Path("source-intake/mts_residuals/P8_DOMAIN_ALPHA3_R11_LINK.csv")
DOMAIN_COEFFICIENTS_PATH = Path("source-intake/mts_residuals/P8_mu_extra_domain_projector_coefficients.csv")


SCHEMA_COLUMNS = [
    "model_id",
    "branch_id",
    "vector_id",
    "operator_family",
    "coefficient_symbol",
    "coefficient_value",
    "coefficient_units",
    "normalization",
    "operator_form",
    "weak_field_map",
    "affected_rows",
    "induced_observable",
    "predicted_residual_or_bound_source",
    "derivation_status",
    "formula_reference",
    "source_file",
    "assumptions",
    "valid_for_claim",
    "notes",
]


SOURCE_REGISTER = [
    {
        "path": "463-EH-only-or-R11-executable-vector-gate.md",
        "role": "global EH/R11 fork and R11 fill queue",
    },
    {
        "path": "464-R11-executable-vector-minimum-fill-skeleton.md",
        "role": "canonical 10-family R11 skeleton and validation rules",
    },
    {
        "path": "472-domain-projector-alpha3-no-leak-or-R11-link.md",
        "role": "domain alpha3 no-leak attempt and R11-required decision",
    },
    {
        "path": str(SKELETON_PATH),
        "role": "canonical R11 19-column skeleton source",
    },
    {
        "path": str(R11_LINK_PATH),
        "role": "domain row to R11 operator link requirements",
    },
    {
        "path": str(DOMAIN_COEFFICIENTS_PATH),
        "role": "domain projector coefficient artifact from 472",
    },
    {
        "path": "source-intake/mts_residuals/R11_EXECUTABLE_VECTOR_STATUS.csv",
        "role": "global operator-family status before domain minimum fill",
    },
    {
        "path": "source-intake/mts_residuals/R11_R10_LINK_REQUIREMENTS.csv",
        "role": "R10/R11 finite-range link policy",
    },
]


DOMAIN_FAMILIES = {"vector_preferred_frame", "projector_domain_stress", "source_normalization_operator"}


DOMAIN_OVERRIDES = {
    "vector_preferred_frame": {
        "coefficient_symbol": "c_domain_vector_or_selector_marker",
        "coefficient_value": "MISSING_DOMAIN_VECTOR_ABSENCE_THEOREM_OR_NUMERIC_COEFFICIENTS",
        "coefficient_units": "dimensionless_after_preferred_frame_normalization",
        "normalization": "relative_to_observed_local_coframe_and_measured_GM",
        "operator_form": "u_D^mu, selector normal, domain velocity, or preferred-frame vector terms retained in local compact branch",
        "weak_field_map": "alpha1_domain=W_domain_alpha1*epsilon_domain_vector; alpha2_domain=W_domain_alpha2*epsilon_domain_vector; alpha3_domain includes vector/flux projection; xi_domain includes anisotropy",
        "affected_rows": "R5;R6;R7;R8;R11",
        "induced_observable": "alpha1;alpha2;alpha3;xi;operator_ledger",
        "predicted_residual_or_bound_source": "MISSING_DOMAIN_VECTOR_THEOREM_OR_COEFFICIENT_PRODUCT",
        "derivation_status": "retained_unfilled",
        "formula_reference": "472-domain-projector-alpha3-no-leak-or-R11-link.md",
        "source_file": "source-intake/mts_residuals/P8_DOMAIN_ALPHA3_R11_LINK.csv",
        "assumptions": "observed coframe fixed; no tuned cancellation; domain selector vector not parent-zeroed",
        "valid_for_claim": "false",
        "notes": "Minimum domain R11 row; blocks R5/R6/R7/R8 until no-vector theorem or coefficients exist.",
    },
    "projector_domain_stress": {
        "coefficient_symbol": "c_projector_domain_stress",
        "coefficient_value": "0_IF_PARENT_OWNS_METRIC_INDEPENDENT_TOPOLOGICAL_P_D_ELSE_MISSING_PROJECTOR_STRESS_COEFFICIENT",
        "coefficient_units": "dimensionless_after_projector_stress_normalization",
        "normalization": "relative_to_EH_operator_and_measured_GM_source_normalization",
        "operator_form": "delta_g P_D, delta_g chi_D, lambda_P constraint stress, domain wall/readout-mask stress",
        "weak_field_map": "bulk projector stress zero only for parent-owned metric-independent topological P_D; retained selector/domain stress maps to alpha1/alpha2/alpha3/xi",
        "affected_rows": "R5;R6;R7;R8;R11",
        "induced_observable": "alpha1;alpha2;alpha3;xi;operator_ledger",
        "predicted_residual_or_bound_source": "MISSING_PARENT_P_D_OWNERSHIP_OR_PROJECTOR_STRESS_BOUND",
        "derivation_status": "conditional_zero_not_parent_owned",
        "formula_reference": "348-N5-projector-stress-conservation-theorem.md;472-domain-projector-alpha3-no-leak-or-R11-link.md",
        "source_file": "source-intake/mts_residuals/P8_DOMAIN_ALPHA3_PREMISE_OWNERSHIP.csv",
        "assumptions": "topological P_D partial theorem; parent projector selection and domain selector no-vector still missing",
        "valid_for_claim": "false",
        "notes": "No-bulk-stress is conditional only; not a domain alpha3 pass.",
    },
    "source_normalization_operator": {
        "coefficient_symbol": "c_domain_source_normalization_operator",
        "coefficient_value": "MISSING_DOMAIN_MU_EXTRA_OPERATOR_ZERO_OR_NUMERIC_COEFFICIENT",
        "coefficient_units": "dimensionless_mu_extra_over_G_eff_M_eff_or_operator_units_declared",
        "normalization": "mu_extra_domain/(G_eff*M_eff) with row-wise alpha1/alpha2/alpha3/xi maps",
        "operator_form": "mu_obs = G_eff M_eff + mu_domain_projector plus derivative/vector/anisotropy source-normalization corrections",
        "weak_field_map": "R5/R6/R7/R8 maps from P8_mu_extra_domain_projector_coefficients.csv; R11 ledger tracks source-normalization operator",
        "affected_rows": "R5;R6;R7;R8;R11",
        "induced_observable": "alpha1;alpha2;alpha3;xi;operator_ledger",
        "predicted_residual_or_bound_source": "MISSING_DOMAIN_PROJECTOR_COEFFICIENT_PRODUCTS_OR_THEOREM_ZERO",
        "derivation_status": "retained_unfilled",
        "formula_reference": "472-domain-projector-alpha3-no-leak-or-R11-link.md",
        "source_file": "source-intake/mts_residuals/P8_mu_extra_domain_projector_coefficients.csv",
        "assumptions": "source normalization row cannot absorb domain vector/stress without explicit coefficient map",
        "valid_for_claim": "false",
        "notes": "Domain source-normalization operator is wired but not scoreable.",
    },
}


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
        lines.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |")
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


def build_vector_rows() -> list[dict[str, Any]]:
    skeleton = read_csv(SKELETON_PATH)
    rows: list[dict[str, Any]] = []
    for row in skeleton:
        out = dict(row)
        out["branch_id"] = "domain_projector_R11_minimum_fill"
        out["vector_id"] = "R11_nonEH_operator_vector_executable"
        family = out["operator_family"]
        if family in DOMAIN_OVERRIDES:
            out.update(DOMAIN_OVERRIDES[family])
        else:
            out["derivation_status"] = "retained_out_of_scope_for_473"
            out["valid_for_claim"] = "false"
            out["notes"] = "Global R11 family retained from skeleton; 473 only wires the domain/projector minimum rows."
        rows.append(out)
    return rows


def domain_vector_rows(vector_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [row for row in vector_rows if row["operator_family"] in DOMAIN_FAMILIES]


def build_missing_ledger(domain_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    checks = [
        ("coefficient_value", "real numeric value or parent theorem-zero certificate"),
        ("predicted_residual_or_bound_source", "residual product, theorem-zero source, or bound envelope"),
        ("derivation_status", "derived_zero, derived_bound, fitted, closure_assumed, or retained_unfilled with source"),
        ("formula_reference", "specific file/equation defining the weak-field map"),
        ("source_file", "existing source artifact supplying the coefficient/theorem"),
    ]
    for row in domain_rows:
        for field, required in checks:
            value = row[field]
            if "MISSING_" in value or "IF_PARENT" in value or row["valid_for_claim"] != "true":
                rows.append(
                    {
                        "operator_family": row["operator_family"],
                        "missing_or_conditional_field": field,
                        "current_value": value,
                        "required_replacement": required,
                        "blocks_rows": row["affected_rows"],
                        "claim_blocked_until": "field is concrete, sourced, and row valid_for_claim=true",
                    }
                )
    return rows


def build_validation(vector_rows: list[dict[str, Any]], domain_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    all_columns_ok = all(set(SCHEMA_COLUMNS).issubset(row.keys()) for row in vector_rows)
    family_count_ok = len({row["operator_family"] for row in vector_rows}) == 10 and len(vector_rows) == 10
    generic_fill_count = sum(
        1
        for row in vector_rows
        for value in row.values()
        if isinstance(value, str) and value.startswith("fill_")
    )
    claimable_rows = [row for row in vector_rows if row["valid_for_claim"] == "true"]
    domain_claimable = [row for row in domain_rows if row["valid_for_claim"] == "true"]
    return [
        {
            "rule_id": "V473_0_schema",
            "rule": "R11 vector uses canonical 19-column schema",
            "result": "pass" if all_columns_ok else "fail",
            "evidence": f"rows={len(vector_rows)} columns={len(SCHEMA_COLUMNS)}",
            "claim_effect": "schema only, no physics claim",
        },
        {
            "rule_id": "V473_1_family_completeness",
            "rule": "All 10 global R11 families appear once in executable-path vector file",
            "result": "pass" if family_count_ok else "fail",
            "evidence": f"unique_families={len({row['operator_family'] for row in vector_rows})}",
            "claim_effect": "wiring only",
        },
        {
            "rule_id": "V473_2_no_generic_fill_placeholders",
            "rule": "No generic fill_ placeholders remain",
            "result": "pass" if generic_fill_count == 0 else "fail",
            "evidence": f"generic_fill_count={generic_fill_count}",
            "claim_effect": "explicit missing markers are allowed but block claims",
        },
        {
            "rule_id": "V473_3_actual_executable_rows",
            "rule": "Rows are executable only if valid_for_claim=true and no missing/conditional coefficient fields remain",
            "result": "fail_for_claim",
            "evidence": f"claimable_rows={len(claimable_rows)} domain_claimable_rows={len(domain_claimable)}",
            "claim_effect": "R11_domain_vector_supplied=false",
        },
        {
            "rule_id": "V473_4_domain_rows_present",
            "rule": "Domain minimum rows exist for vector, projector-domain stress, and source-normalization operator",
            "result": "pass" if len(domain_rows) == 3 else "fail",
            "evidence": ";".join(row["operator_family"] for row in domain_rows),
            "claim_effect": "domain R11 wiring exists but not scoreable",
        },
        {
            "rule_id": "V473_5_domain_alpha3_still_blocked",
            "rule": "R7 alpha3 remains blocked until W_domain_alpha3 epsilon_domain_flux is theorem-zero or numeric below 4e-20",
            "result": "fail_for_claim",
            "evidence": "projector_domain_stress and source_normalization_operator rows are conditional/missing",
            "claim_effect": "no PPN alpha3 or local-GR pass",
        },
    ]


def build_decision() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "D0_vector_file_written",
            "status": "pass_wiring",
            "meaning": "R11_nonEH_operator_vector_executable.csv now exists with the canonical 10-family schema",
            "next_action": "do not count it as an executable physics pass",
        },
        {
            "decision_id": "D1_domain_rows",
            "status": "minimum_rows_written",
            "meaning": "domain-specific R11 rows are present for vector_preferred_frame, projector_domain_stress, and source_normalization_operator",
            "next_action": "derive no-vector/no-selector theorem or fill coefficient products",
        },
        {
            "decision_id": "D2_claim_rows",
            "status": "zero",
            "meaning": "no R11 row is valid_for_claim=true",
            "next_action": "keep R11_domain_vector_supplied=false",
        },
        {
            "decision_id": "D3_alpha3",
            "status": "still_blocked",
            "meaning": "domain alpha3 still lacks W_domain_alpha3 epsilon_domain_flux or theorem-zero",
            "next_action": NEXT_TARGET,
        },
        {
            "decision_id": "D4_promotion",
            "status": "forbidden",
            "meaning": "no domain channel, mu_extra zero, PPN, Newton, or local-GR pass",
            "next_action": "continue with domain selector no-vector theorem/coefficient",
        },
    ]


def build_doc(run_dir: Path) -> str:
    source_rows = read_csv(SOURCE_REGISTER_PATH)
    domain_rows = read_csv(DOMAIN_VECTOR_PATH)
    executable_rows = read_csv(EXECUTABLE_VECTOR_PATH)
    missing_rows = read_csv(MISSING_LEDGER_PATH)
    validation_rows = read_csv(VALIDATION_PATH)
    decision_rows = read_csv(DECISION_PATH)
    compact_executable = [
        {
            "operator_family": row["operator_family"],
            "coefficient_symbol": row["coefficient_symbol"],
            "coefficient_value": row["coefficient_value"],
            "affected_rows": row["affected_rows"],
            "valid_for_claim": row["valid_for_claim"],
            "notes": row["notes"],
        }
        for row in executable_rows
    ]
    return f"""# 473 - R11 Domain Projector Operator Vector Minimum Fill

Private R11/domain-projector source-normalization checkpoint. This is not a public R11 pass, PPN pass, Newtonian-limit pass, local-GR derivation, measured-GM derivation, cosmology result, EM result, or unified-field claim.

## 1. Purpose

Checkpoint `472` showed:

```text
domain_projector_mass cannot score while the R11 operator vector is missing.
```

This checkpoint writes the minimum R11 domain/projector vector wiring.

Short answer:

```text
The R11 vector file now exists and is parseable.
It is not physics-executable yet: actual claim-valid rows = 0.
```

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/R11_domain_projector_operator_vector_minimum_fill.py` |
| Run directory | `{run_dir.relative_to(ROOT)}` |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## 3. Source Register

{md_table(source_rows)}

## 4. Domain Minimum Rows

{md_table(domain_rows)}

These are the three R11 rows that matter immediately for the domain/projector alpha3 obstruction:

```text
vector_preferred_frame,
projector_domain_stress,
source_normalization_operator.
```

The file is useful because it tells the evaluator exactly where the domain coefficients belong.

It is not claim-valid because the coefficients are still missing or conditional.

## 5. Executable-Path Vector

The expected artifact path now exists:

```text
source-intake/mts_residuals/R11_nonEH_operator_vector_executable.csv
```

Compact view:

{md_table(compact_executable)}

Important:

```text
valid_for_claim=false for all rows.
```

So the word `executable` here means:

```text
schema/file path is wired for future evaluator use,
not that MTS has passed R11.
```

## 6. Missing / Conditional Ledger

{md_table(missing_rows)}

The highest-pressure missing object remains:

```text
W_domain_alpha3 * epsilon_domain_flux
```

with:

```text
abs(W_domain_alpha3 epsilon_domain_flux) <= 4e-20
```

or a theorem-zero source.

## 7. Validation

{md_table(validation_rows)}

## 8. Decision

{md_table(decision_rows)}

Plain-English status:

```text
We have now wired the R11 domain vector path.
We have not filled the physics coefficients.
```

Boxing-score version:

```text
The judges now have the scorecard in the right format.
No points awarded yet.
```

## 9. Claim Ceiling

Allowed:

```text
R11 domain/projector vector wiring exists and is parseable.
```

Allowed:

```text
Domain/projector alpha3 remains blocked by missing no-vector/no-selector theorem or numeric coefficient product.
```

Forbidden:

```text
MTS supplies an executable R11 vector.
```

Forbidden:

```text
MTS passes domain alpha3, PPN, mu_extra zero, Newton, or local GR.
```

## 10. Next Queue

| Rank | Target | Why |
| ---: | --- | --- |
| 1 | `474-domain-selector-no-vector-theorem-or-coefficient.md` | R11 vector row says the immediate physics gap is no domain selector/preferred-frame vector |
| 2 | `475-alpha3-bound-product-evaluator.md` | only useful after boundary/domain theorem premises or numeric products exist |
| 3 | `476-R11-global-family-fill-priority-reset.md` | if we pivot back from domain rows to the full R11 family queue |
"""


def write_run(timestamp: str) -> dict[str, Any]:
    run_dir = ROOT / "runs" / f"{timestamp}-R11-domain-projector-operator-vector-minimum-fill"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    write_csv(SOURCE_REGISTER_PATH, source_register_rows())
    vector_rows = build_vector_rows()
    domain_rows = domain_vector_rows(vector_rows)
    write_csv(EXECUTABLE_VECTOR_PATH, vector_rows, SCHEMA_COLUMNS)
    write_csv(DOMAIN_VECTOR_PATH, domain_rows, SCHEMA_COLUMNS)
    write_csv(MISSING_LEDGER_PATH, build_missing_ledger(domain_rows))
    write_csv(VALIDATION_PATH, build_validation(vector_rows, domain_rows))
    write_csv(DECISION_PATH, build_decision())

    for path in [
        SOURCE_REGISTER_PATH,
        DOMAIN_VECTOR_PATH,
        EXECUTABLE_VECTOR_PATH,
        MISSING_LEDGER_PATH,
        VALIDATION_PATH,
        DECISION_PATH,
    ]:
        write_csv(Path(results_dir.relative_to(ROOT)) / path.name.lower(), read_csv(path))

    (ROOT / DOC_PATH).write_text(build_doc(run_dir), encoding="utf-8")

    source_rows = read_csv(SOURCE_REGISTER_PATH)
    missing_rows = read_csv(MISSING_LEDGER_PATH)
    validation_rows = read_csv(VALIDATION_PATH)
    decision_rows = read_csv(DECISION_PATH)
    claimable_rows = [row for row in vector_rows if row["valid_for_claim"] == "true"]
    status = {
        "timestamp": timestamp,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "checkpoint_doc": str(DOC_PATH),
        "run_dir": str(run_dir),
        "source_register": str(ROOT / SOURCE_REGISTER_PATH),
        "domain_vector": str(ROOT / DOMAIN_VECTOR_PATH),
        "executable_vector_path": str(ROOT / EXECUTABLE_VECTOR_PATH),
        "missing_ledger": str(ROOT / MISSING_LEDGER_PATH),
        "validation": str(ROOT / VALIDATION_PATH),
        "decision": str(ROOT / DECISION_PATH),
        "source_rows": len(source_rows),
        "source_paths_missing": sum(1 for row in source_rows if row["exists"] != "True"),
        "global_vector_rows": len(vector_rows),
        "domain_vector_rows": len(domain_rows),
        "missing_or_conditional_rows": len(missing_rows),
        "validation_rows": len(validation_rows),
        "decision_rows": len(decision_rows),
        "R11_vector_file_exists": True,
        "actual_executable_rows": len(claimable_rows),
        "R11_domain_vector_supplied": False,
        "domain_alpha3_score_ready": False,
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
