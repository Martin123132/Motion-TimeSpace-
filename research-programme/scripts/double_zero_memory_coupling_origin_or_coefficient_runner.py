from __future__ import annotations

import argparse
import csv
import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

STATUS = "double_zero_memory_origin_attempt_written_p_ge_2_condition_derived_as_needed_not_parent_derived_coefficient_runner_retained_no_PPN_Newton_or_local_GR_pass"
CLAIM_CEILING = "double_zero_memory_coupling_origin_or_coefficient_runner_only_no_selector_theorem_no_domain_channel_PPN_Newton_or_local_GR_pass"
NEXT_TARGET = "477-alpha3-bound-product-evaluator.md"

DOC_PATH = Path("476-double-zero-memory-coupling-origin-or-coefficient-runner.md")
SOURCE_REGISTER_PATH = Path("source-intake/mts_residuals/P8_DOUBLE_ZERO_MEMORY_SOURCE_REGISTER.csv")
ORIGIN_ATTEMPT_PATH = Path("source-intake/mts_residuals/P8_DOUBLE_ZERO_MEMORY_ORIGIN_ATTEMPT.csv")
VARIATION_TEST_PATH = Path("source-intake/mts_residuals/P8_DOUBLE_ZERO_MEMORY_VARIATION_TEST.csv")
POWER_GATE_PATH = Path("source-intake/mts_residuals/P8_DOUBLE_ZERO_MEMORY_POWER_GATE.csv")
RUNNER_INPUT_PATH = Path("source-intake/mts_residuals/P8_DOUBLE_ZERO_COEFFICIENT_RUNNER_INPUT.csv")
RUNNER_RESULTS_PATH = Path("source-intake/mts_residuals/P8_DOUBLE_ZERO_COEFFICIENT_RUNNER_RESULTS.csv")
COEFFICIENT_FILL_PATH = Path("source-intake/mts_residuals/P8_DOMAIN_SELECTOR_CLOSURE_COEFFICIENT_FILL.csv")
VECTOR_COEFFICIENTS_PATH = Path("source-intake/mts_residuals/P8_DOMAIN_SELECTOR_VECTOR_COEFFICIENTS.csv")
DOMAIN_COEFFICIENTS_PATH = Path("source-intake/mts_residuals/P8_mu_extra_domain_projector_coefficients.csv")
VALIDATION_PATH = Path("source-intake/mts_residuals/P8_DOUBLE_ZERO_MEMORY_VALIDATION.csv")
DECISION_PATH = Path("source-intake/mts_residuals/P8_DOUBLE_ZERO_MEMORY_DECISION.csv")

SCORECARD_PATH = Path("source-intake/mts_residuals/P8_MU_EXTRA_LOCAL_BOUND_SCORECARD.csv")
RESIDUAL_COMPONENTS_PATH = Path("runs/20260602-094500-MTS-local-residual-vector-input-contract/results/residual_components.csv")
R11_EXECUTABLE_VECTOR_PATH = Path("source-intake/mts_residuals/R11_nonEH_operator_vector_executable.csv")

SOURCE_REGISTER = [
    {
        "path": "68-chiD-gated-memory-conservation-contract.md",
        "role": "linear chi_D memory gate creates Bianchi/selector exchange term",
    },
    {
        "path": "275-JC-three-form-memory-current-from-Q.md",
        "role": "conditional determinant/coherent-volume current gives double-zero support",
    },
    {
        "path": "416-binding-invariant-domain-selector-repair.md",
        "role": "C_exp auxiliary/topological selector route retained as contract, not parent derivation",
    },
    {
        "path": "475-domain-selector-parent-action-clause-or-coefficient-fill.md",
        "role": "double-zero parent-action clause identified as sufficient but not derived",
    },
    {
        "path": str(SCORECARD_PATH),
        "role": "source-locked PPN bounds for coefficient runner",
    },
    {
        "path": str(RESIDUAL_COMPONENTS_PATH),
        "role": "residual component definitions for R5/R6/R7/R8",
    },
    {
        "path": str(R11_EXECUTABLE_VECTOR_PATH),
        "role": "R11 vector path; parseable but zero claim-valid rows",
    },
    {
        "path": "scripts/double_zero_memory_coupling_origin_or_coefficient_runner.py",
        "role": "this checkpoint generator",
    },
]

TARGET_ROWS = [
    ("R5_alpha1", "alpha1", "W_domain_alpha1_epsilon_domain_vector", "epsilon_domain_vector"),
    ("R6_alpha2", "alpha2", "W_domain_alpha2_epsilon_domain_vector", "epsilon_domain_vector"),
    ("R7_alpha3", "alpha3", "W_domain_alpha3_epsilon_domain_flux", "epsilon_domain_flux"),
    ("R8_xi", "xi", "W_domain_xi_epsilon_domain_anisotropy", "epsilon_domain_anisotropy"),
    ("R11_EH_operator_ledger", "non_EH_operator_coefficients", "c_domain_source_normalization_operator", "operator_vector"),
]

FALLBACK_BOUNDS = {
    "R5_alpha1": "1e-04",
    "R6_alpha2": "2e-09",
    "R7_alpha3": "4e-20",
    "R8_xi": "4e-09",
    "R11_EH_operator_ledger": "symbolic",
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


def bound_map() -> dict[str, str]:
    bounds = dict(FALLBACK_BOUNDS)
    if (ROOT / SCORECARD_PATH).exists():
        for row in read_csv(SCORECARD_PATH):
            if row.get("epsilon_channel") == "domain_projector_mass" and row.get("target_row") in bounds:
                bounds[row["target_row"]] = row.get("bound_value") or bounds[row["target_row"]]
    if (ROOT / RESIDUAL_COMPONENTS_PATH).exists():
        for row in read_csv(RESIDUAL_COMPONENTS_PATH):
            if row.get("row_id") in bounds:
                bounds[row["row_id"]] = row.get("source_bound") or bounds[row["row_id"]]
    return bounds


def r11_claimable_rows() -> int:
    if not (ROOT / R11_EXECUTABLE_VECTOR_PATH).exists():
        return 0
    return sum(1 for row in read_csv(R11_EXECUTABLE_VECTOR_PATH) if row.get("valid_for_claim") == "true")


def parse_float(value: str) -> float | None:
    try:
        if value.strip().upper().startswith("MISSING") or value.strip().lower() in {"", "symbolic", "nan"}:
            return None
        parsed = float(value)
    except ValueError:
        return None
    if math.isfinite(parsed):
        return parsed
    return None


def numeric_bound(bound: str) -> float | None:
    return parse_float(bound)


def build_origin_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "step_id": "O0_general_gate",
            "claim": "local memory silence for S_mem = integral sqrt(-g) f(chi_D) L_mem requires a double zero at chi_D=0",
            "mathematical_form": "f(0)=0 and f_prime(0)=0",
            "evidence": "variation gives lambda_D + f_prime(chi_D)L_mem + ... = 0 and T_mem scales with f(chi_D)",
            "result": "derived_as_requirement",
            "claim_effect": "p>=2 is necessary for the 475 local-silence clause",
        },
        {
            "step_id": "O1_linear_gate_rejected",
            "claim": "linear f(chi_D)=chi_D is enough",
            "mathematical_form": "f(0)=0 but f_prime(0)=1",
            "evidence": "68 shows the Bianchi gremlin T_memory nabla chi_D and lambda_chi exchange reappears",
            "result": "fail_for_local_GR_branch",
            "claim_effect": "linear gate goes to coefficient branch",
        },
        {
            "step_id": "O2_quadratic_gate_sufficient",
            "claim": "quadratic f(chi_D)=chi_D^2 is sufficient if L_mem is finite and chi_D is auxiliary/scalar",
            "mathematical_form": "f(0)=0, f_prime(0)=0, f_second(0)=2",
            "evidence": "475 variation chain: chi_local=0 implies lambda_local=0 under double-zero coupling",
            "result": "sufficient_contract",
            "claim_effect": "works as theorem target but not parent derivation",
        },
        {
            "step_id": "O3_determinant_current_candidate",
            "claim": "coherent determinant/current route can supply a stronger zero",
            "mathematical_form": "J_C ~ det(Q_coh) ~ (N_D/u3)^3, so J_M(0)=J_M_prime(0)=0",
            "evidence": "275 derives the double-zero shape conditionally from coherent-volume 3-form kinematics",
            "result": "conditional_support_not_parent_owned",
            "claim_effect": "best current clue for origin of p>=2",
        },
        {
            "step_id": "O4_norm_square_or_Z2_candidate",
            "claim": "if chi_D is an amplitude, orientation, or boundary-class representative, action depends on its norm square",
            "mathematical_form": "f(chi_D)=|A_D|^2 or chi_D^2 under chi_D -> -chi_D symmetry",
            "evidence": "not present as a parent symmetry in current corpus",
            "result": "not_derived",
            "claim_effect": "candidate only",
        },
        {
            "step_id": "O5_topological_pairing_candidate",
            "claim": "boundary/cohomology memory may activate through a quadratic class pairing",
            "mathematical_form": "f_D ~ <J_rel,J_rel>_D or ||Pi_rel J_B||^2",
            "evidence": "308/416 keep relative-class route open but not parent-owned",
            "result": "not_derived",
            "claim_effect": "candidate only",
        },
        {
            "step_id": "O6_verdict",
            "claim": "the corpus parent-derives the double-zero memory gate",
            "mathematical_form": "S_parent -> f(chi_D) with f(0)=f_prime(0)=0",
            "evidence": "p>=2 is derived as a requirement; determinant/norm/topological routes are conditional or absent",
            "result": "fail_current_corpus",
            "claim_effect": "no selector/no-vector/local-GR promotion; coefficient runner retained",
        },
    ]


def build_variation_test_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_power_p": "0",
            "coupling": "f(chi_D)=1",
            "f_at_zero": "1",
            "f_prime_at_zero": "0",
            "memory_stress_at_local_zero": "nonzero",
            "lambda_at_local_zero": "0_if_no_chi_dependence",
            "verdict": "fail_memory_not_silenced",
        },
        {
            "gate_power_p": "1",
            "coupling": "f(chi_D)=chi_D",
            "f_at_zero": "0",
            "f_prime_at_zero": "1",
            "memory_stress_at_local_zero": "zero",
            "lambda_at_local_zero": "-L_mem",
            "verdict": "fail_hidden_selector_exchange",
        },
        {
            "gate_power_p": "2",
            "coupling": "f(chi_D)=chi_D^2",
            "f_at_zero": "0",
            "f_prime_at_zero": "0",
            "memory_stress_at_local_zero": "zero",
            "lambda_at_local_zero": "0",
            "verdict": "pass_as_sufficient_contract",
        },
        {
            "gate_power_p": "3",
            "coupling": "f(chi_D)=chi_D^3 or det(Q_coh)",
            "f_at_zero": "0",
            "f_prime_at_zero": "0",
            "memory_stress_at_local_zero": "zero",
            "lambda_at_local_zero": "0",
            "verdict": "pass_stronger_but_amplitude_normalization_needed",
        },
        {
            "gate_power_p": ">=2",
            "coupling": "any smooth f with Taylor coefficients a0=a1=0",
            "f_at_zero": "0",
            "f_prime_at_zero": "0",
            "memory_stress_at_local_zero": "zero",
            "lambda_at_local_zero": "0",
            "verdict": "required_general_condition",
        },
    ]


def build_power_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "P0_power_condition",
            "requirement": "memory activation has Taylor order p>=2 at chi_D=0",
            "status": "derived_as_requirement",
            "evidence": "variation test demands f(0)=f_prime(0)=0",
            "blocks_claim_if_missing": "true",
        },
        {
            "gate_id": "P1_origin_symmetry",
            "requirement": "p>=2 follows from parent symmetry, norm-square, determinant, or topological pairing",
            "status": "not_parent_derived",
            "evidence": "275 determinant route conditional; no Z2/norm-square/topological action derived",
            "blocks_claim_if_missing": "true",
        },
        {
            "gate_id": "P2_local_zero",
            "requirement": "parent proves chi_local=0 by projected spectral gap or relative triviality",
            "status": "not_parent_derived",
            "evidence": "308/416 keep local zero as selector contract",
            "blocks_claim_if_missing": "true",
        },
        {
            "gate_id": "P3_FLRW_normalization",
            "requirement": "same f(chi_D) leaves FLRW/cosmology branch active with derived amplitude normalization",
            "status": "not_parent_derived",
            "evidence": "p=2 or p=3 changes activation amplitude unless normalized by parent variables",
            "blocks_claim_if_missing": "true",
        },
        {
            "gate_id": "P4_R11_silence",
            "requirement": "domain source-normalization R11 row is zero or executable",
            "status": "fail_for_claim",
            "evidence": f"R11_claimable_rows={r11_claimable_rows()}",
            "blocks_claim_if_missing": "true",
        },
        {
            "gate_id": "P5_coefficient_runner",
            "requirement": "if p>=2 is not parent-derived, run explicit residual products against PPN bounds",
            "status": "required_fallback",
            "evidence": "coefficient runner inputs remain missing",
            "blocks_claim_if_missing": "true",
        },
    ]


def coefficient_rows(bounds: dict[str, str]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for target_row, observable, coefficient_symbol, epsilon_symbol in TARGET_ROWS:
        if target_row == "R11_EH_operator_ledger":
            value_or_theorem = "MISSING_DOMAIN_SOURCE_NORMALIZATION_OPERATOR_ZERO_OR_EXECUTABLE_COEFFICIENT_VECTOR"
            premise_status = "double_zero_does_not_replace_R11_operator_silence"
            map_text = "R11 includes domain_projector_mass source-normalization operator coefficients and weak-field maps"
            score_status = "not_scoreable"
        elif target_row == "R7_alpha3":
            value_or_theorem = "0_IF_PARENT_DERIVES_P_GE_2_GATE_AND_LOCAL_ZERO_AND_TOPOLOGICAL_PROJECTOR_AND_R11_SILENCE_ELSE_PRODUCT_REQUIRED"
            premise_status = "p_ge_2_required_but_not_parent_derived"
            map_text = "alpha3_domain = W_domain_alpha3 * epsilon_domain_flux"
            score_status = "conditional_not_scoreable"
        elif target_row == "R8_xi":
            value_or_theorem = "0_IF_PARENT_DERIVES_P_GE_2_GATE_AND_LOCAL_STF_STRESS_ZERO_ELSE_PRODUCT_REQUIRED"
            premise_status = "p_ge_2_required_but_not_parent_derived"
            map_text = "xi_domain = W_domain_xi * epsilon_domain_anisotropy"
            score_status = "not_scoreable"
        else:
            value_or_theorem = "0_IF_PARENT_DERIVES_P_GE_2_GATE_AND_LOCAL_SCALAR_ZERO_ELSE_PRODUCT_REQUIRED"
            premise_status = "p_ge_2_required_but_not_parent_derived"
            map_text = f"{observable}_domain = {coefficient_symbol.replace('_epsilon_', ' * epsilon_')}"
            score_status = "not_scoreable"
        rows.append(
            {
                "channel": "domain_projector_mass",
                "target_row": target_row,
                "observable": observable,
                "coefficient_symbol": coefficient_symbol,
                "map": map_text,
                "value_or_theorem": value_or_theorem,
                "premise_status": premise_status,
                "target_bound": bounds.get(target_row, FALLBACK_BOUNDS[target_row]),
                "score_status": score_status,
                "valid_for_claim": "false",
                "source": str(DOC_PATH),
            }
        )
    return rows


def runner_input_rows(bounds: dict[str, str]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for target_row, observable, coefficient_symbol, epsilon_symbol in TARGET_ROWS:
        rows.append(
            {
                "target_row": target_row,
                "observable": observable,
                "coefficient_symbol": coefficient_symbol,
                "epsilon_symbol": epsilon_symbol,
                "coefficient_value": "MISSING_NUMERIC_OR_THEOREM_ZERO",
                "epsilon_value": "MISSING_NUMERIC_OR_THEOREM_ZERO",
                "predicted_residual_formula": "coefficient_value * epsilon_value" if target_row != "R11_EH_operator_ledger" else "operator_vector_required",
                "target_bound": bounds.get(target_row, FALLBACK_BOUNDS[target_row]),
                "units": "dimensionless" if target_row != "R11_EH_operator_ledger" else "operator_family",
                "input_status": "missing",
            }
        )
    return rows


def runner_result_rows(inputs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in inputs:
        coeff = parse_float(row["coefficient_value"])
        eps = parse_float(row["epsilon_value"])
        bound = numeric_bound(row["target_bound"])
        if row["target_row"] == "R11_EH_operator_ledger":
            residual = "MISSING_EXECUTABLE_OPERATOR_VECTOR"
            status = "not_scoreable_R11_required"
            pass_fail = "false"
        elif coeff is None or eps is None:
            residual = "MISSING_NUMERIC_PRODUCT"
            status = "not_scoreable_inputs_missing"
            pass_fail = "false"
        elif bound is None:
            residual_value = coeff * eps
            residual = f"{residual_value:.12g}"
            status = "not_scoreable_bound_missing"
            pass_fail = "false"
        else:
            residual_value = coeff * eps
            residual = f"{residual_value:.12g}"
            passed = abs(residual_value) <= bound
            status = "pass_bound" if passed else "fail_bound"
            pass_fail = str(passed).lower()
        rows.append(
            {
                "target_row": row["target_row"],
                "observable": row["observable"],
                "coefficient_symbol": row["coefficient_symbol"],
                "epsilon_symbol": row["epsilon_symbol"],
                "predicted_residual": residual,
                "target_bound": row["target_bound"],
                "runner_status": status,
                "pass_bound": pass_fail,
                "valid_for_claim": "false",
                "reason": "runner is wired, but double-zero origin and/or numeric products are missing",
            }
        )
    return rows


def validation_rows(
    source_rows: list[dict[str, Any]],
    origins: list[dict[str, Any]],
    variation_tests: list[dict[str, Any]],
    power_gates: list[dict[str, Any]],
    inputs: list[dict[str, Any]],
    results: list[dict[str, Any]],
    coeffs: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    missing_sources = sum(1 for row in source_rows if row["exists"] != "True")
    target_set = {row["target_row"] for row in inputs}
    coeff_target_set = {row["target_row"] for row in coeffs}
    return [
        {
            "rule_id": "V476_0_sources",
            "rule": "all cited source paths exist",
            "result": "pass" if missing_sources == 0 else "fail",
            "evidence": f"missing_sources={missing_sources}",
            "claim_effect": "traceability only",
        },
        {
            "rule_id": "V476_1_requirement",
            "rule": "p>=2 double-zero is derived as a requirement, not as a parent theorem",
            "result": "pass",
            "evidence": f"origin_rows={len(origins)} variation_tests={len(variation_tests)}",
            "claim_effect": "prevents linear gate promotion",
        },
        {
            "rule_id": "V476_2_power_gate",
            "rule": "power gates track origin, local zero, FLRW normalization, R11, and coefficient fallback",
            "result": "pass" if len(power_gates) == 6 else "fail",
            "evidence": f"power_gate_rows={len(power_gates)}",
            "claim_effect": "no hidden theorem upgrade",
        },
        {
            "rule_id": "V476_3_runner_targets",
            "rule": "coefficient runner covers R5/R6/R7/R8/R11",
            "result": "pass" if target_set == {row[0] for row in TARGET_ROWS} else "fail",
            "evidence": ";".join(sorted(target_set)),
            "claim_effect": "fallback is machine-readable",
        },
        {
            "rule_id": "V476_4_coefficients",
            "rule": "domain coefficient files are updated and unpromoted",
            "result": "pass" if coeff_target_set == {row[0] for row in TARGET_ROWS} and sum(1 for row in coeffs if row["valid_for_claim"] == "true") == 0 else "fail",
            "evidence": f"coefficient_rows={len(coeffs)} valid_for_claim_true={sum(1 for row in coeffs if row['valid_for_claim'] == 'true')}",
            "claim_effect": "no PPN/Newton/local-GR pass",
        },
        {
            "rule_id": "V476_5_runner_claim",
            "rule": "runner results do not claim evidence with missing inputs",
            "result": "fail_for_claim",
            "evidence": f"pass_bound_true={sum(1 for row in results if row['pass_bound'] == 'true')}",
            "claim_effect": "runner wired only",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "D0_double_zero_requirement",
            "status": "derived_as_requirement",
            "meaning": "local silence needs f(0)=f_prime(0)=0; linear chi_D gates are not enough",
            "next_action": "do not use linear selector for local-GR branch",
        },
        {
            "decision_id": "D1_origin",
            "status": "not_parent_derived",
            "meaning": "det(Q_coh), norm-square, and topological-pairing routes are clues, not completed parent action derivations",
            "next_action": "keep p>=2 as theorem target",
        },
        {
            "decision_id": "D2_runner",
            "status": "wired_inputs_missing",
            "meaning": "R5/R6/R7/R8/R11 coefficient runner exists but has no numeric products or theorem-zero source",
            "next_action": NEXT_TARGET,
        },
        {
            "decision_id": "D3_coefficients",
            "status": "retained",
            "meaning": "domain coefficients remain explicit and valid_for_claim=false",
            "next_action": "fill alpha3 product first because it has the hardest bound",
        },
        {
            "decision_id": "D4_promotion",
            "status": "forbidden",
            "meaning": "no domain channel, PPN, Newtonian-limit, or local-GR pass is earned",
            "next_action": NEXT_TARGET,
        },
    ]


def build_doc(run_dir: Path) -> str:
    source_rows = read_csv(SOURCE_REGISTER_PATH)
    origin_rows = read_csv(ORIGIN_ATTEMPT_PATH)
    variation_rows = read_csv(VARIATION_TEST_PATH)
    power_rows = read_csv(POWER_GATE_PATH)
    input_rows = read_csv(RUNNER_INPUT_PATH)
    result_rows = read_csv(RUNNER_RESULTS_PATH)
    coeff_rows = read_csv(COEFFICIENT_FILL_PATH)
    validation = read_csv(VALIDATION_PATH)
    decisions = read_csv(DECISION_PATH)
    compact_coeffs = [
        {
            "target_row": row["target_row"],
            "observable": row["observable"],
            "coefficient_symbol": row["coefficient_symbol"],
            "value_or_theorem": row["value_or_theorem"],
            "target_bound": row["target_bound"],
            "valid_for_claim": row["valid_for_claim"],
        }
        for row in coeff_rows
    ]
    return f"""# 476 - Double-Zero Memory Coupling Origin Or Coefficient Runner

Private memory-gate/PPN-coefficient checkpoint. This is not a public PPN pass, Newtonian-limit pass, local-GR derivation, cosmology result, EM result, or unified-field claim.

## 1. Purpose

Checkpoint `475` found the exact sufficient local-silence lock:

```text
S_mem,D = chi_D^2 L_mem,D
```

This checkpoint asks whether that double-zero shape is derived.

Short answer:

```text
p >= 2 is derived as a requirement.
The parent origin of p >= 2 is not derived.
So the coefficient runner stays active.
```

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/double_zero_memory_coupling_origin_or_coefficient_runner.py` |
| Run directory | `{run_dir.relative_to(ROOT)}` |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## 3. Source Register

{md_table(source_rows)}

## 4. Why Double Zero Is Required

For a general memory gate:

```text
S_mem,D = integral sqrt(-g) f(chi_D) L_mem,D
```

local branch silence needs:

```text
f(0) = 0,
f'(0) = 0.
```

The first zero turns off memory stress.

The second zero prevents the selector Euler equation from forcing a nonzero local multiplier/exchange term.

{md_table(variation_rows)}

So:

```text
linear chi_D is not enough;
p >= 2 is the minimum local-GR-safe memory gate.
```

## 5. Origin Attempt

{md_table(origin_rows)}

The best clue is checkpoint `275`:

```text
det(Q_coh) ~ (N_D/u3)^3
```

which is stronger than the required double zero.

But it is still conditional because `Q_coh`, the domain selector, the topological projector, and normalization are not parent-owned.

## 6. Power Gate

{md_table(power_rows)}

Practical read:

```text
We know the punch has to be slipped with p >= 2.
We do not yet know why the parent action must throw exactly that move.
```

## 7. Coefficient Runner

Input template:

{md_table(input_rows)}

Runner output:

{md_table(result_rows)}

The runner is useful because future numeric products can be dropped in and checked against:

```text
R5 alpha1 <= 1e-04,
R6 alpha2 <= 2e-09,
R7 alpha3 <= 4e-20,
R8 xi <= 4e-09.
```

Right now it scores nothing:

```text
all products are missing or R11-symbolic.
```

## 8. Updated Coefficient Rows

{md_table(compact_coeffs)}

These rows were also written to:

```text
source-intake/mts_residuals/P8_DOMAIN_SELECTOR_CLOSURE_COEFFICIENT_FILL.csv
source-intake/mts_residuals/P8_DOMAIN_SELECTOR_VECTOR_COEFFICIENTS.csv
source-intake/mts_residuals/P8_mu_extra_domain_projector_coefficients.csv
```

Important:

```text
valid_for_claim=false for every row.
```

## 9. Validation

{md_table(validation)}

## 10. Decision

{md_table(decisions)}

## 11. Claim Ceiling

Allowed:

```text
MTS has derived p >= 2 as a necessary local-silence condition for the memory gate.
```

Allowed:

```text
MTS has conditional clues for a p >= 2 origin, especially the coherent determinant/current route.
```

Forbidden:

```text
MTS parent-derives the double-zero memory coupling.
```

Forbidden:

```text
MTS passes domain alpha3, PPN, Newton, or local GR.
```

## 12. Next Queue

| Rank | Target | Why |
| ---: | --- | --- |
| 1 | `477-alpha3-bound-product-evaluator.md` | hardest immediate row is W_domain_alpha3 epsilon_domain_flux <= 4e-20 |
| 2 | `478-determinant-current-parent-ownership-or-demotion.md` | if we keep chasing derivation, Q_coh/det(Q) is the best double-zero origin clue |
| 3 | `479-R11-domain-source-normalization-zero-or-fill.md` | R11 source-normalization remains a separate blocker |
"""


def write_run(timestamp: str) -> dict[str, Any]:
    run_dir = ROOT / "runs" / f"{timestamp}-double-zero-memory-coupling-origin-or-coefficient-runner"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    sources = source_register_rows()
    bounds = bound_map()
    origins = build_origin_attempt_rows()
    variation_tests = build_variation_test_rows()
    power_gates = build_power_gate_rows()
    inputs = runner_input_rows(bounds)
    results = runner_result_rows(inputs)
    coeffs = coefficient_rows(bounds)
    validation = validation_rows(sources, origins, variation_tests, power_gates, inputs, results, coeffs)
    decisions = decision_rows()

    write_csv(SOURCE_REGISTER_PATH, sources)
    write_csv(ORIGIN_ATTEMPT_PATH, origins)
    write_csv(VARIATION_TEST_PATH, variation_tests)
    write_csv(POWER_GATE_PATH, power_gates)
    write_csv(RUNNER_INPUT_PATH, inputs)
    write_csv(RUNNER_RESULTS_PATH, results)
    write_csv(COEFFICIENT_FILL_PATH, coeffs)
    write_csv(VECTOR_COEFFICIENTS_PATH, coeffs)
    write_csv(DOMAIN_COEFFICIENTS_PATH, coeffs)
    write_csv(VALIDATION_PATH, validation)
    write_csv(DECISION_PATH, decisions)

    for path in [
        SOURCE_REGISTER_PATH,
        ORIGIN_ATTEMPT_PATH,
        VARIATION_TEST_PATH,
        POWER_GATE_PATH,
        RUNNER_INPUT_PATH,
        RUNNER_RESULTS_PATH,
        COEFFICIENT_FILL_PATH,
        VECTOR_COEFFICIENTS_PATH,
        DOMAIN_COEFFICIENTS_PATH,
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
        "origin_attempt": str(ROOT / ORIGIN_ATTEMPT_PATH),
        "variation_test": str(ROOT / VARIATION_TEST_PATH),
        "power_gate": str(ROOT / POWER_GATE_PATH),
        "runner_input": str(ROOT / RUNNER_INPUT_PATH),
        "runner_results": str(ROOT / RUNNER_RESULTS_PATH),
        "coefficient_fill": str(ROOT / COEFFICIENT_FILL_PATH),
        "domain_coefficients_updated": str(ROOT / DOMAIN_COEFFICIENTS_PATH),
        "validation": str(ROOT / VALIDATION_PATH),
        "decision": str(ROOT / DECISION_PATH),
        "source_rows": len(sources),
        "source_paths_missing": sum(1 for row in sources if row["exists"] != "True"),
        "origin_rows": len(origins),
        "variation_test_rows": len(variation_tests),
        "power_gate_rows": len(power_gates),
        "runner_input_rows": len(inputs),
        "runner_result_rows": len(results),
        "coefficient_rows": len(coeffs),
        "validation_rows": len(validation),
        "decision_rows": len(decisions),
        "R11_claimable_rows": r11_claimable_rows(),
        "p_ge_2_derived_as_requirement": True,
        "double_zero_memory_origin_parent_derived": False,
        "coefficient_runner_ready": True,
        "coefficient_runner_scoreable_now": False,
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
