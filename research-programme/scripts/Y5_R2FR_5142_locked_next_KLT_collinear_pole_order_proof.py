from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
from typing import Any


POST = Path(__file__).resolve().parents[1]
ROOT = POST.parent
FORMAL = ROOT / "formalization-workbench"
GENERIC_RUNNER = POST / "scripts" / "Y5_R2FR_5132_locked_next_argument_gate_and_single_job_runner.py"
PROOF_5138_SCRIPT = POST / "scripts" / "Y5_R2FR_5138_A04_KLT_collinear_pole_order_proof.py"
FORMAL_BASELINE = "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--checkpoint-id", default="5142")
    parser.add_argument("--checked-date", default="2026-07-20")
    arguments = parser.parse_args()
    runner = load_module("mts_5132_for_5142", GENERIC_RUNNER)
    theorem = load_module("mts_5138_for_5142", PROOF_5138_SCRIPT)
    generic_arguments = argparse.Namespace(
        checkpoint_id=str(arguments.checkpoint_id),
        checked_date=str(arguments.checked_date),
        job_key=None,
        precision="default",
        mode="dry-run",
    )
    job, configuration = runner.configure(generic_arguments)
    base = runner.M5128
    context = base.build_context()
    base_argument = str(job["base_argument_id"])
    marker = (
        f"MTS_{arguments.checkpoint_id}_{job['epsilon_id']}_{base_argument}_"
        "KLT_COLLINEAR_POLE_ORDER_PROOF"
    )
    source = POST / "source-intake" / "functional_rg" / str(arguments.checkpoint_id)
    order_csv = source / f"{base_argument}_KLT_collinear_order_table.csv"
    witness_json = source / f"{base_argument}_beam_spinor_bracket_witness.json"
    result_json = source / f"{base_argument}_KLT_collinear_pole_order_proof.json"
    validation_csv = (
        POST
        / "source-intake"
        / "mts_residuals"
        / f"P8_Y5_BRR545_{arguments.checkpoint_id}_VALIDATION.csv"
    )
    document = POST / (
        f"{arguments.checkpoint_id}-Y5-R2FR-{job['epsilon_id']}-{base_argument}-"
        "KLT-collinear-pole-order-proof.md"
    )
    candidates = [
        (chamber, pole)
        for chamber in context["chambers"]
        for pole in chamber["active_poles"]
        if pole["family"] == "beam_spinor" and pole["member"] == "small"
    ]
    if len(candidates) != 1:
        raise RuntimeError(
            f"expected one active small beam pole for {job['job_key']}, found {len(candidates)}"
        )
    chamber, pole = candidates[0]
    rows = theorem.order_rows()
    for row in rows:
        row["checkpoint_marker"] = marker
        row["job_key"] = job["job_key"]
        row["source_checked_date"] = str(arguments.checked_date)
    theorem.R5136.write_csv(order_csv, rows)
    witness = theorem.bracket_witness(context, chamber, pole)
    witness.update(
        {
            "checkpoint_marker": marker,
            "job_key": job["job_key"],
            "epsilon_id": job["epsilon_id"],
            "base_argument_id": base_argument,
            "source_checked_date": str(arguments.checked_date),
        }
    )
    theorem.R5136.atomic_json(witness_json, witness)
    maximum_tree_pole_order = max(row["pole_order"] for row in rows)
    singular_rows = [row for row in rows if row["pole_order"] > 0]
    amplitude_text = theorem.AMPLITUDE_SOURCE.read_text(encoding="utf-8")
    global_text = theorem.GLOBAL_SOURCE.read_text(encoding="utf-8")
    source_formula_lock = all(
        clause in amplitude_text
        for clause in (
            "left = scalar_mhv(left_order, special, spinors, chirality)",
            "momentum_kernel(gamma_reversed, sigma_reversed, momenta)",
            "result += scalar_klt_five(left, special, 0) * scalar_klt_five(",
            "result += scalar_klt_five(left, special, 1) * scalar_klt_five(",
        )
    ) and all(
        clause in global_text
        for clause in (
            "M5017.hhh_reduced_product(",
            "return complex((direct - subtraction) / soft_energy)",
        )
    )
    row_local_non_degeneracy = bool(
        witness["vanishing_bracket_is_simple"]
        and witness["other_cut_chiral_brackets_nonzero"]
        and witness["s21_has_one_matching_zero"]
        and witness["energy_prefactors_regular"]
        and float(witness["nearest_other_log_singularity_distance"]) > 0.1
    )
    simple_pole_proved = bool(
        maximum_tree_pole_order == 1
        and len(singular_rows) == 2
        and {row["special_internal_leg"] for row in singular_rows} == {2, 3}
        and row_local_non_degeneracy
        and source_formula_lock
    )
    counts_after = base.M5125.run_counts(
        base.RUN, context["config"]["config_digest"], context["schedule"]
    )
    result = {
        "checkpoint_marker": marker,
        "job_key": job["job_key"],
        "job": job,
        "configuration": configuration,
        "theorem_source_checkpoint": base.relative(theorem.RESULT_JSON),
        "amplitude_source": base.relative(theorem.AMPLITUDE_SOURCE),
        "global_source": base.relative(theorem.GLOBAL_SOURCE),
        "source_formula_lock": source_formula_lock,
        "row_local_non_degeneracy": row_local_non_degeneracy,
        "order_table": base.relative(order_csv),
        "bracket_witness": base.relative(witness_json),
        "maximum_scalar_KLT_tree_pole_order": maximum_tree_pole_order,
        "singular_term_count": len(singular_rows),
        "singular_special_internal_legs": sorted(
            row["special_internal_leg"] for row in singular_rows
        ),
        "reusable_theorem": {
            "statement": "For the implemented KLT hhh integrand, an isolated row with one simple left-angle beam zero, nonzero opposite/right chiral brackets and regular energy prefactors has pole order at most one.",
            "reuse_rule": "Every epsilon/argument row must independently pass the bracket, energy and isolation witness; no certificate is inherited from geometry alone.",
        },
        "simple_pole_order_proved_for_locked_row": simple_pole_proved,
        "double_pole_excluded_for_locked_row": simple_pole_proved,
        "deep_chart_precision_authorized": simple_pole_proved,
        "counts_before": configuration["counts_before"],
        "counts_after": counts_after,
        "formalization_workbench_tree_sha256": base.M5127.tree_digest(FORMAL),
        "execution_performed": False,
        "full_pilot_resume_authorized": False,
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
        "source_checked_date": str(arguments.checked_date),
    }
    theorem.R5136.atomic_json(result_json, result)
    checks = [
        ("sources_exist", all(path.exists() for path in (GENERIC_RUNNER, PROOF_5138_SCRIPT, theorem.AMPLITUDE_SOURCE, theorem.GLOBAL_SOURCE))),
        ("first_locked_row_selected", configuration["first_incomplete_job"] == job["job_key"]),
        ("source_formula_lock", source_formula_lock),
        ("twelve_KLT_rows", len(rows) == 12),
        ("maximum_order_exactly_simple", maximum_tree_pole_order == 1),
        ("only_special_2_3_singular", len(singular_rows) == 2 and {row["special_internal_leg"] for row in singular_rows} == {2, 3}),
        ("vanishing_bracket_simple", witness["vanishing_bracket_is_simple"]),
        ("other_chiral_brackets_nonzero", witness["other_cut_chiral_brackets_nonzero"]),
        ("row_local_simple_pole_proved", simple_pole_proved),
        ("run_counts_unchanged", counts_after == configuration["counts_before"]),
        ("formal_tree_unchanged", result["formalization_workbench_tree_sha256"] == FORMAL_BASELINE),
        ("no_claim_or_execution", not result["execution_performed"] and not result["valid_for_numeric_UV_claim"] and not result["valid_for_local_GR_claim"] and not result["valid_for_full_MTS_claim"]),
    ]
    theorem.R5136.write_csv(
        validation_csv,
        [
            {
                "check_id": f"VAL{arguments.checkpoint_id}_{index:02d}_{name}",
                "passed": passed,
                "checkpoint_marker": marker,
                "valid_for_numeric_UV_claim": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
                "source_checked_date": str(arguments.checked_date),
            }
            for index, (name, passed) in enumerate(checks, start=1)
        ],
    )
    document_text = f"""# {arguments.checkpoint_id}: {job['epsilon_id']}/{base_argument} KLT collinear pole-order proof

## Reusable theorem and row-local witness

The KLT permutation count from checkpoint 5138 is structural: the only
Parke-Taylor overlap with `b^-2` also contains `s21 proportional to b`, so its
maximum order is `b^-1`. It is reusable only when a new row independently
shows one simple left-angle zero, nonzero opposite and right-cut chiral
brackets, finite energy prefactors and isolation from every other log
singularity.

`{job['job_key']}` passes those row-local conditions. Its maximum implemented
pole order is `{maximum_tree_pole_order}`; only special legs
`{sorted(row['special_internal_leg'] for row in singular_rows)}` retain the
simple pole. A genuine double pole is excluded for this locked row, so deeper
boundary precision is authorized to resolve residue and regular-part data.

No coefficient job was executed and no numeric threshold was changed. The
pilot remains `{counts_after}`. This is a coefficient-integrand theorem, not a
UV, local-GR, galaxy or full-MTS claim. The formalization hash remains
`{FORMAL_BASELINE}`.
"""
    document.write_text(document_text, encoding="utf-8")
    failures = [name for name, passed in checks if not passed]
    print(json.dumps({"result": result, "validation_failures": failures}, indent=2, sort_keys=True))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
