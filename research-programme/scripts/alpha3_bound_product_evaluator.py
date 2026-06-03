from __future__ import annotations

import argparse
import csv
import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

STATUS = "alpha3_bound_product_evaluator_written_boundary_and_domain_inputs_missing_no_mu_extra_PPN_Newton_or_local_GR_pass"
CLAIM_CEILING = "alpha3_bound_product_evaluator_only_no_alpha3_pass_no_mu_extra_zero_PPN_Newton_or_local_GR_pass"
NEXT_TARGET = "478-determinant-current-parent-ownership-or-demotion.md"

DOC_PATH = Path("477-alpha3-bound-product-evaluator.md")
SOURCE_REGISTER_PATH = Path("source-intake/mts_residuals/P8_ALPHA3_BOUND_SOURCE_REGISTER.csv")
THEOREM_GATE_PATH = Path("source-intake/mts_residuals/P8_ALPHA3_THEOREM_ZERO_GATE.csv")
INPUT_PATH = Path("source-intake/mts_residuals/P8_ALPHA3_BOUND_PRODUCT_INPUT.csv")
EVALUATION_PATH = Path("source-intake/mts_residuals/P8_ALPHA3_BOUND_PRODUCT_EVALUATION.csv")
TOTAL_GUARD_PATH = Path("source-intake/mts_residuals/P8_ALPHA3_TOTAL_GUARD.csv")
VALIDATION_PATH = Path("source-intake/mts_residuals/P8_ALPHA3_BOUND_VALIDATION.csv")
DECISION_PATH = Path("source-intake/mts_residuals/P8_ALPHA3_BOUND_DECISION.csv")

SCORECARD_PATH = Path("source-intake/mts_residuals/P8_MU_EXTRA_LOCAL_BOUND_SCORECARD.csv")
ALPHA3_SKELETON_PATH = Path("source-intake/mts_residuals/P8_MU_EXTRA_ALPHA3_FILL_INPUT_SKELETON.csv")
BOUNDARY_COEFFICIENTS_PATH = Path("source-intake/mts_residuals/P8_mu_extra_boundary_coefficients.csv")
DOMAIN_COEFFICIENTS_PATH = Path("source-intake/mts_residuals/P8_mu_extra_domain_projector_coefficients.csv")
DOUBLE_ZERO_INPUT_PATH = Path("source-intake/mts_residuals/P8_DOUBLE_ZERO_COEFFICIENT_RUNNER_INPUT.csv")
DOUBLE_ZERO_RESULTS_PATH = Path("source-intake/mts_residuals/P8_DOUBLE_ZERO_COEFFICIENT_RUNNER_RESULTS.csv")
R11_EXECUTABLE_VECTOR_PATH = Path("source-intake/mts_residuals/R11_nonEH_operator_vector_executable.csv")

ALPHA3_BOUND = 4e-20

SOURCE_REGISTER = [
    {
        "path": "470-boundary-alpha3-zero-theorem-or-numeric-coefficient.md",
        "role": "boundary alpha3 scalar/no-flux lemma and missing parent ownership",
    },
    {
        "path": "472-domain-projector-alpha3-no-leak-or-R11-link.md",
        "role": "domain alpha3 no-leak attempt and R11 link requirement",
    },
    {
        "path": "473-R11-domain-projector-operator-vector-minimum-fill.md",
        "role": "R11 domain rows exist but are not claim-valid",
    },
    {
        "path": "476-double-zero-memory-coupling-origin-or-coefficient-runner.md",
        "role": "p>=2 memory gate requirement and missing numeric products",
    },
    {
        "path": str(SCORECARD_PATH),
        "role": "source-locked alpha3 bound rows",
    },
    {
        "path": str(ALPHA3_SKELETON_PATH),
        "role": "boundary/domain/total alpha3 fill skeleton",
    },
    {
        "path": str(BOUNDARY_COEFFICIENTS_PATH),
        "role": "boundary alpha3 coefficient/theorem row",
    },
    {
        "path": str(DOMAIN_COEFFICIENTS_PATH),
        "role": "domain alpha3 coefficient/theorem row",
    },
    {
        "path": str(DOUBLE_ZERO_INPUT_PATH),
        "role": "latest domain coefficient runner input template",
    },
    {
        "path": str(DOUBLE_ZERO_RESULTS_PATH),
        "role": "latest domain coefficient runner result status",
    },
    {
        "path": str(R11_EXECUTABLE_VECTOR_PATH),
        "role": "R11 vector path; parseable but zero claim-valid rows",
    },
    {
        "path": "scripts/alpha3_bound_product_evaluator.py",
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


def parse_float(value: str) -> float | None:
    try:
        stripped = value.strip()
        if not stripped or stripped.upper().startswith("MISSING") or stripped.lower() in {"symbolic", "theorem_zero"}:
            return None
        parsed = float(stripped)
    except ValueError:
        return None
    return parsed if math.isfinite(parsed) else None


def source_register_rows() -> list[dict[str, str]]:
    return [
        {
            "source_file": item["path"],
            "exists": str((ROOT / item["path"]).exists()),
            "role": item["role"],
        }
        for item in SOURCE_REGISTER
    ]


def r11_claimable_rows() -> int:
    if not (ROOT / R11_EXECUTABLE_VECTOR_PATH).exists():
        return 0
    return sum(1 for row in read_csv(R11_EXECUTABLE_VECTOR_PATH) if row.get("valid_for_claim") == "true")


def alpha3_bound_from_scorecard(channel: str) -> str:
    if not (ROOT / SCORECARD_PATH).exists():
        return "4e-20"
    rows = [
        row
        for row in read_csv(SCORECARD_PATH)
        if row.get("epsilon_channel") == channel and row.get("target_row") == "R7_alpha3"
    ]
    if len(rows) == 1 and rows[0].get("bound_value"):
        return rows[0]["bound_value"]
    return "4e-20"


def coefficient_status(path: Path, channel: str) -> dict[str, str]:
    if not (ROOT / path).exists():
        return {
            "value_or_theorem": "MISSING_COEFFICIENT_FILE",
            "premise_status": "missing",
            "source": str(path),
            "score_status": "not_scoreable",
            "valid_for_claim": "false",
        }
    matches = [
        row
        for row in read_csv(path)
        if row.get("channel") == channel and row.get("target_row") == "R7_alpha3"
    ]
    if not matches:
        return {
            "value_or_theorem": "MISSING_ALPHA3_ROW",
            "premise_status": "missing",
            "source": str(path),
            "score_status": "not_scoreable",
            "valid_for_claim": "false",
        }
    row = matches[0]
    return {
        "value_or_theorem": row.get("value_or_theorem", ""),
        "premise_status": row.get("premise_status", ""),
        "source": row.get("source", str(path)),
        "score_status": row.get("score_status", ""),
        "valid_for_claim": row.get("valid_for_claim", "false"),
    }


def build_theorem_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "TG_boundary_zero",
            "channel": "boundary_monopole_shift",
            "theorem_zero_route": "scalar stationary boundary action with no tangential vector, no normal momentum flux, full stress variation",
            "required_premises": "scalar-only boundary data; no material marker; stationary compact collar; Ward/boundary flux closure",
            "current_status": "conditional_lemma_not_parent_owned",
            "accepted_as_zero": "false",
            "blocking_reason": "470 boundary lemma is conditional and no numeric product is supplied",
        },
        {
            "gate_id": "TG_domain_zero",
            "channel": "domain_projector_mass",
            "theorem_zero_route": "p>=2 memory gate plus local zero plus topological projector plus R11 source-normalization silence",
            "required_premises": "double-zero parent origin; local b_D=0 or c_D=0; metric-independent P_MTS,D; R11 valid rows",
            "current_status": "not_parent_derived",
            "accepted_as_zero": "false",
            "blocking_reason": "476 derives p>=2 as a requirement only; local zero/topological/R11 gates remain open",
        },
        {
            "gate_id": "TG_total_cancellation",
            "channel": "combined_mu_extra_alpha3",
            "theorem_zero_route": "parent identity forcing alpha3_boundary + alpha3_domain + other channels = 0",
            "required_premises": "identity before fitting; common normalization; no post-hoc cancellation",
            "current_status": "not_present",
            "accepted_as_zero": "false",
            "blocking_reason": "policy requires individual channel pass unless parent cancellation identity is derived",
        },
    ]


def build_input_rows() -> list[dict[str, Any]]:
    boundary = coefficient_status(BOUNDARY_COEFFICIENTS_PATH, "boundary_monopole_shift")
    domain = coefficient_status(DOMAIN_COEFFICIENTS_PATH, "domain_projector_mass")
    return [
        {
            "input_id": "A3_boundary",
            "channel": "boundary_monopole_shift",
            "target_row": "R7_alpha3",
            "observable": "alpha3",
            "product_symbol": "W_boundary_alpha3_epsilon_boundary_flux",
            "coefficient_symbol": "W_boundary_alpha3",
            "epsilon_symbol": "epsilon_boundary_flux",
            "coefficient_value": "MISSING_NUMERIC_OR_THEOREM_ZERO",
            "epsilon_value": "MISSING_NUMERIC_OR_THEOREM_ZERO",
            "explicit_product_value": "MISSING_NUMERIC_OR_THEOREM_ZERO",
            "theorem_zero_status": boundary["value_or_theorem"],
            "premise_status": boundary["premise_status"],
            "target_bound": alpha3_bound_from_scorecard("boundary_monopole_shift"),
            "source": boundary["source"],
        },
        {
            "input_id": "A3_domain",
            "channel": "domain_projector_mass",
            "target_row": "R7_alpha3",
            "observable": "alpha3",
            "product_symbol": "W_domain_alpha3_epsilon_domain_flux",
            "coefficient_symbol": "W_domain_alpha3",
            "epsilon_symbol": "epsilon_domain_flux",
            "coefficient_value": "MISSING_NUMERIC_OR_THEOREM_ZERO",
            "epsilon_value": "MISSING_NUMERIC_OR_THEOREM_ZERO",
            "explicit_product_value": "MISSING_NUMERIC_OR_THEOREM_ZERO",
            "theorem_zero_status": domain["value_or_theorem"],
            "premise_status": domain["premise_status"],
            "target_bound": alpha3_bound_from_scorecard("domain_projector_mass"),
            "source": domain["source"],
        },
        {
            "input_id": "A3_total",
            "channel": "combined_mu_extra_alpha3",
            "target_row": "R7_alpha3",
            "observable": "alpha3",
            "product_symbol": "alpha3_mu_extra_total",
            "coefficient_symbol": "sum_of_scored_channels",
            "epsilon_symbol": "not_applicable",
            "coefficient_value": "MISSING_CHANNEL_VALUES",
            "epsilon_value": "not_applicable",
            "explicit_product_value": "MISSING_CHANNEL_VALUES",
            "theorem_zero_status": "0_ONLY_IF_EACH_CHANNEL_PASSES_OR_PARENT_CANCELLATION_IDENTITY_EXISTS",
            "premise_status": "parent_cancellation_identity_not_present",
            "target_bound": "4e-20",
            "source": str(ALPHA3_SKELETON_PATH),
        },
    ]


def evaluate_input(row: dict[str, Any], accepted_zero_channels: set[str]) -> dict[str, Any]:
    bound = parse_float(row["target_bound"])
    coefficient = parse_float(row["coefficient_value"])
    epsilon = parse_float(row["epsilon_value"])
    product = parse_float(row["explicit_product_value"])
    if row["channel"] in accepted_zero_channels:
        predicted = 0.0
        status = "pass_theorem_zero"
        pass_bound = True
        valid = True
        reason = "theorem-zero gate accepted"
    elif product is not None:
        predicted = product
        pass_bound = bound is not None and abs(product) <= bound
        status = "pass_numeric_bound" if pass_bound else "fail_numeric_bound"
        valid = pass_bound
        reason = "explicit product supplied"
    elif coefficient is not None and epsilon is not None:
        predicted = coefficient * epsilon
        pass_bound = bound is not None and abs(predicted) <= bound
        status = "pass_numeric_bound" if pass_bound else "fail_numeric_bound"
        valid = pass_bound
        reason = "coefficient and epsilon supplied"
    elif row["channel"] == "combined_mu_extra_alpha3":
        predicted = "MISSING_CHANNEL_VALUES"
        status = "not_scoreable_total_missing_channels"
        pass_bound = False
        valid = False
        reason = "individual alpha3 channels have not passed and no parent cancellation identity exists"
    else:
        predicted = "MISSING_NUMERIC_PRODUCT_OR_THEOREM_ZERO"
        status = "not_scoreable_inputs_missing"
        pass_bound = False
        valid = False
        reason = "missing numeric product and theorem-zero gate not accepted"
    return {
        "input_id": row["input_id"],
        "channel": row["channel"],
        "target_row": row["target_row"],
        "observable": row["observable"],
        "product_symbol": row["product_symbol"],
        "predicted_alpha3": predicted if isinstance(predicted, str) else f"{predicted:.12g}",
        "target_bound": row["target_bound"],
        "abs_le_bound": str(pass_bound).lower(),
        "evaluation_status": status,
        "valid_for_claim": str(valid).lower(),
        "reason": reason,
    }


def build_evaluation_rows(input_rows: list[dict[str, Any]], theorem_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    accepted_zero_channels = {
        row["channel"]
        for row in theorem_rows
        if row["accepted_as_zero"] == "true"
    }
    return [evaluate_input(row, accepted_zero_channels) for row in input_rows]


def build_total_guard_rows(evaluation_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    individual_rows = [row for row in evaluation_rows if row["channel"] in {"boundary_monopole_shift", "domain_projector_mass"}]
    all_individual_pass = all(row["valid_for_claim"] == "true" for row in individual_rows)
    total_rows = [row for row in evaluation_rows if row["channel"] == "combined_mu_extra_alpha3"]
    total_pass = bool(total_rows and total_rows[0]["valid_for_claim"] == "true")
    return [
        {
            "guard_id": "G_total_no_cancellation_by_fit",
            "rule": "alpha3 total can pass only if each active channel passes individually or a parent cancellation identity is derived before fitting",
            "current_result": "fail_for_claim",
            "evidence": f"individual_pass={all_individual_pass}; total_pass={total_pass}",
            "claim_effect": "no total alpha3 or mu_extra-zero promotion",
        },
        {
            "guard_id": "G_boundary_channel",
            "rule": "boundary alpha3 must be theorem-zero or abs(W_boundary_alpha3 epsilon_boundary_flux)<=4e-20",
            "current_result": next(row["evaluation_status"] for row in evaluation_rows if row["channel"] == "boundary_monopole_shift"),
            "evidence": next(row["predicted_alpha3"] for row in evaluation_rows if row["channel"] == "boundary_monopole_shift"),
            "claim_effect": "boundary alpha3 retained",
        },
        {
            "guard_id": "G_domain_channel",
            "rule": "domain alpha3 must be theorem-zero or abs(W_domain_alpha3 epsilon_domain_flux)<=4e-20",
            "current_result": next(row["evaluation_status"] for row in evaluation_rows if row["channel"] == "domain_projector_mass"),
            "evidence": next(row["predicted_alpha3"] for row in evaluation_rows if row["channel"] == "domain_projector_mass"),
            "claim_effect": "domain alpha3 retained",
        },
        {
            "guard_id": "G_R11_dependency",
            "rule": "domain channel also needs R11 source-normalization/operator rows claim-valid or theorem-zero",
            "current_result": "fail_for_claim",
            "evidence": f"R11_claimable_rows={r11_claimable_rows()}",
            "claim_effect": "R11 blocks domain alpha3 promotion",
        },
    ]


def build_validation_rows(
    source_rows: list[dict[str, Any]],
    theorem_rows: list[dict[str, Any]],
    input_rows: list[dict[str, Any]],
    evaluation_rows: list[dict[str, Any]],
    guard_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    missing_sources = sum(1 for row in source_rows if row["exists"] != "True")
    claim_rows = sum(1 for row in evaluation_rows if row["valid_for_claim"] == "true")
    expected_channels = {"boundary_monopole_shift", "domain_projector_mass", "combined_mu_extra_alpha3"}
    input_channels = {row["channel"] for row in input_rows}
    return [
        {
            "rule_id": "V477_0_sources",
            "rule": "all cited source paths exist",
            "result": "pass" if missing_sources == 0 else "fail",
            "evidence": f"missing_sources={missing_sources}",
            "claim_effect": "traceability only",
        },
        {
            "rule_id": "V477_1_inputs",
            "rule": "boundary, domain, and total alpha3 inputs are present",
            "result": "pass" if input_channels == expected_channels else "fail",
            "evidence": ";".join(sorted(input_channels)),
            "claim_effect": "evaluator is complete for current alpha3 channels",
        },
        {
            "rule_id": "V477_2_bound",
            "rule": "individual alpha3 rows use 4e-20 bound",
            "result": "pass" if all(row["target_bound"] == "4e-20" for row in input_rows) else "fail",
            "evidence": ";".join(f"{row['channel']}={row['target_bound']}" for row in input_rows),
            "claim_effect": "source lock carried into evaluator",
        },
        {
            "rule_id": "V477_3_theorem_zero",
            "rule": "theorem-zero gates are explicit and not accepted without parent premises",
            "result": "pass" if len(theorem_rows) == 3 and all(row["accepted_as_zero"] == "false" for row in theorem_rows) else "fail",
            "evidence": f"theorem_rows={len(theorem_rows)} accepted={sum(1 for row in theorem_rows if row['accepted_as_zero'] == 'true')}",
            "claim_effect": "no hidden zero claim",
        },
        {
            "rule_id": "V477_4_claim_rows",
            "rule": "no alpha3 evaluation row is claim-valid with missing products",
            "result": "fail_for_claim",
            "evidence": f"valid_for_claim_true={claim_rows}",
            "claim_effect": "no alpha3/PPN/local-GR pass",
        },
        {
            "rule_id": "V477_5_total_guard",
            "rule": "total alpha3 cannot pass by cancellation-by-fit",
            "result": "pass" if len(guard_rows) == 4 else "fail",
            "evidence": f"guard_rows={len(guard_rows)}",
            "claim_effect": "total alpha3 retained",
        },
    ]


def build_decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "D0_evaluator",
            "status": "written",
            "meaning": "alpha3 now has a concrete product evaluator for boundary, domain, and total rows",
            "next_action": "fill numeric products or theorem-zero sources",
        },
        {
            "decision_id": "D1_boundary_alpha3",
            "status": "not_scoreable",
            "meaning": "boundary theorem-zero route is conditional and W_boundary_alpha3 epsilon_boundary_flux is missing",
            "next_action": "derive scalar boundary premises or supply numeric product",
        },
        {
            "decision_id": "D2_domain_alpha3",
            "status": "not_scoreable_highest_pressure",
            "meaning": "domain product W_domain_alpha3 epsilon_domain_flux is missing and R11 has zero claim-valid rows",
            "next_action": "derive determinant/current parent ownership or supply numeric product",
        },
        {
            "decision_id": "D3_total_alpha3",
            "status": "not_promoted",
            "meaning": "no cancellation-by-fit is allowed; individual channels must pass or parent identity must exist",
            "next_action": "keep total alpha3 retained",
        },
        {
            "decision_id": "D4_promotion",
            "status": "forbidden",
            "meaning": "no alpha3 pass, mu_extra zero, PPN, Newtonian-limit, or local-GR pass is earned",
            "next_action": NEXT_TARGET,
        },
    ]


def build_doc(run_dir: Path) -> str:
    source_rows = read_csv(SOURCE_REGISTER_PATH)
    theorem_rows = read_csv(THEOREM_GATE_PATH)
    input_rows = read_csv(INPUT_PATH)
    evaluation_rows = read_csv(EVALUATION_PATH)
    guard_rows = read_csv(TOTAL_GUARD_PATH)
    validation_rows = read_csv(VALIDATION_PATH)
    decision_rows = read_csv(DECISION_PATH)
    return f"""# 477 - Alpha3 Bound Product Evaluator

Private alpha3/PPN bound checkpoint. This is not a public alpha3 pass, PPN pass, Newtonian-limit pass, local-GR derivation, cosmology result, EM result, or unified-field claim.

## 1. Purpose

Checkpoint `476` wired the coefficient runner but left the hardest row unresolved:

```text
abs(W_domain_alpha3 * epsilon_domain_flux) <= 4e-20.
```

This checkpoint turns the alpha3 row into a strict evaluator.

Short answer:

```text
Evaluator yes.
Alpha3 pass no.
Boundary and domain products are still missing.
```

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/alpha3_bound_product_evaluator.py` |
| Run directory | `{run_dir.relative_to(ROOT)}` |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## 3. Source Register

{md_table(source_rows)}

## 4. The Rule

For each active alpha3 source channel:

```text
abs(W_i_alpha3 * epsilon_i_flux) <= 4e-20
```

or:

```text
theorem-zero source accepted by explicit parent-premise gates.
```

No post-fit cancellation is allowed unless a parent identity exists before scoring.

## 5. Theorem-Zero Gates

{md_table(theorem_rows)}

No theorem-zero gate is accepted in the current corpus.

## 6. Product Inputs

{md_table(input_rows)}

The domain row is still the highest pressure:

```text
W_domain_alpha3 * epsilon_domain_flux.
```

## 7. Evaluation

{md_table(evaluation_rows)}

Current result:

```text
not scoreable;
no channel passes;
valid_for_claim=false for every row.
```

## 8. Total Guard

{md_table(guard_rows)}

This stops the cheap move:

```text
boundary bad + domain bad = fitted cancellation.
```

No. Each source channel must pass unless the parent action derives a cancellation identity.

## 9. Validation

{md_table(validation_rows)}

## 10. Decision

{md_table(decision_rows)}

## 11. Claim Ceiling

Allowed:

```text
MTS has a strict alpha3 product evaluator.
```

Allowed:

```text
The exact missing products and theorem-zero gates are identified.
```

Forbidden:

```text
MTS passes alpha3.
```

Forbidden:

```text
MTS passes mu_extra zero, PPN, Newton, or local GR.
```

## 12. Next Queue

| Rank | Target | Why |
| ---: | --- | --- |
| 1 | `478-determinant-current-parent-ownership-or-demotion.md` | best current domain-alpha3 theorem-zero clue is det(Q_coh), but it is not parent-owned |
| 2 | `479-R11-domain-source-normalization-zero-or-fill.md` | R11 source-normalization still blocks domain alpha3 |
| 3 | `480-alpha3-numeric-product-input-template.md` | if derivation stalls, make the coefficient input template ready for actual numeric fitting |
"""


def write_run(timestamp: str) -> dict[str, Any]:
    run_dir = ROOT / "runs" / f"{timestamp}-alpha3-bound-product-evaluator"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    source_rows = source_register_rows()
    theorem_rows = build_theorem_gate_rows()
    input_rows = build_input_rows()
    evaluation_rows = build_evaluation_rows(input_rows, theorem_rows)
    guard_rows = build_total_guard_rows(evaluation_rows)
    validation_rows = build_validation_rows(source_rows, theorem_rows, input_rows, evaluation_rows, guard_rows)
    decision_rows = build_decision_rows()

    write_csv(SOURCE_REGISTER_PATH, source_rows)
    write_csv(THEOREM_GATE_PATH, theorem_rows)
    write_csv(INPUT_PATH, input_rows)
    write_csv(EVALUATION_PATH, evaluation_rows)
    write_csv(TOTAL_GUARD_PATH, guard_rows)
    write_csv(VALIDATION_PATH, validation_rows)
    write_csv(DECISION_PATH, decision_rows)

    for path in [
        SOURCE_REGISTER_PATH,
        THEOREM_GATE_PATH,
        INPUT_PATH,
        EVALUATION_PATH,
        TOTAL_GUARD_PATH,
        VALIDATION_PATH,
        DECISION_PATH,
    ]:
        write_csv(Path(results_dir.relative_to(ROOT)) / path.name.lower(), read_csv(path))

    (ROOT / DOC_PATH).write_text(build_doc(run_dir), encoding="utf-8")

    status = {
        "timestamp": timestamp,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "checkpoint_doc": str(DOC_PATH),
        "run_dir": str(run_dir),
        "source_register": str(ROOT / SOURCE_REGISTER_PATH),
        "theorem_gate": str(ROOT / THEOREM_GATE_PATH),
        "input": str(ROOT / INPUT_PATH),
        "evaluation": str(ROOT / EVALUATION_PATH),
        "total_guard": str(ROOT / TOTAL_GUARD_PATH),
        "validation": str(ROOT / VALIDATION_PATH),
        "decision": str(ROOT / DECISION_PATH),
        "source_rows": len(source_rows),
        "source_paths_missing": sum(1 for row in source_rows if row["exists"] != "True"),
        "theorem_gate_rows": len(theorem_rows),
        "input_rows": len(input_rows),
        "evaluation_rows": len(evaluation_rows),
        "total_guard_rows": len(guard_rows),
        "validation_rows": len(validation_rows),
        "decision_rows": len(decision_rows),
        "R11_claimable_rows": r11_claimable_rows(),
        "alpha3_bound": ALPHA3_BOUND,
        "boundary_alpha3_score_ready": False,
        "domain_alpha3_score_ready": False,
        "total_alpha3_score_ready": False,
        "alpha3_passed": False,
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
