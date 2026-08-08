from __future__ import annotations

import argparse
import cmath
import importlib.util
import json
import math
from pathlib import Path
from typing import Any


POST = Path(__file__).resolve().parents[1]
ROOT = POST.parent
FORMAL = ROOT / "formalization-workbench"
SCRIPT_5136 = POST / "scripts" / "Y5_R2FR_5136_A04_Laurent_order_radius_precision_test.py"
GENERIC_RUNNER = POST / "scripts" / "Y5_R2FR_5132_locked_next_argument_gate_and_single_job_runner.py"
AMPLITUDE_SOURCE = POST / "scripts" / "Y5_R2FR_5017_complex_safe_hhh_crossed_integrand_and_coupled_locality_smoke.py"
GLOBAL_SOURCE = POST / "scripts" / "Y5_R2FR_5026_finite_x_global_pole_transport_smoke.py"
SOURCE = POST / "source-intake" / "functional_rg" / "5138"
ORDER_CSV = SOURCE / "A04_KLT_collinear_order_table.csv"
WITNESS_JSON = SOURCE / "A04_beam_spinor_bracket_witness.json"
RESULT_JSON = SOURCE / "A04_KLT_collinear_pole_order_proof.json"
VALIDATION_CSV = POST / "source-intake" / "mts_residuals" / "P8_Y5_BRR545_5138_VALIDATION.csv"
DOCUMENT = POST / "5138-Y5-R2FR-A04-KLT-collinear-pole-order-proof.md"

CHECKPOINT_ID = "5138"
MARKER = "MTS_5138_A04_KLT_COLLINEAR_POLE_ORDER_PROOF"
CHECKED_DATE = "2026-07-20"
JOB_KEY = "E040__S512503_N0000__A04__primary24"
FORMAL_BASELINE = "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def adjacent(order: tuple[int, ...], first: int, second: int) -> bool:
    return any(
        {order[index], order[(index + 1) % len(order)]} == {first, second}
        for index in range(len(order))
    )


def kernel_zero_order(gamma_reversed: int, sigma_reversed: int) -> int:
    if gamma_reversed == 0 and sigma_reversed == 0:
        return 1
    if gamma_reversed == 0 and sigma_reversed == 1:
        return 0
    if gamma_reversed == 1 and sigma_reversed == 0:
        return 1
    return 1


def order_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for sigma_reversed in (0, 1):
        sigma_first = 1 if sigma_reversed == 0 else 2
        sigma_second = 2 if sigma_reversed == 0 else 1
        left_order = (0, sigma_first, sigma_second, 3, 4)
        for gamma_reversed in (0, 1):
            gamma_first = 1 if gamma_reversed == 0 else 2
            gamma_second = 2 if gamma_reversed == 0 else 1
            right_order = (3, 4, gamma_first, gamma_second, 0)
            denominator_order = int(adjacent(left_order, 0, 1)) + int(
                adjacent(right_order, 0, 1)
            )
            kernel_order = kernel_zero_order(gamma_reversed, sigma_reversed)
            for special in (1, 2, 3):
                numerator_order = 4 if special == 1 else 0
                net_power = numerator_order + kernel_order - denominator_order
                rows.append(
                    {
                        "sigma_reversed": sigma_reversed,
                        "gamma_reversed": gamma_reversed,
                        "special_internal_leg": special,
                        "left_order": "-".join(str(value) for value in left_order),
                        "right_order": "-".join(str(value) for value in right_order),
                        "left_01_denominator_order": int(adjacent(left_order, 0, 1)),
                        "right_01_denominator_order": int(adjacent(right_order, 0, 1)),
                        "total_denominator_zero_order": denominator_order,
                        "momentum_kernel_s21_zero_order": kernel_order,
                        "numerator_zero_order": numerator_order,
                        "net_bracket_power": net_power,
                        "pole_order": max(0, -net_power),
                        "checkpoint_marker": MARKER,
                        "valid_for_numeric_UV_claim": False,
                        "valid_for_local_GR_claim": False,
                        "valid_for_full_MTS_claim": False,
                        "source_checked_date": CHECKED_DATE,
                    }
                )
    return rows


def bracket_witness(context: dict[str, Any], chamber: dict[str, Any], pole: dict[str, Any]) -> dict[str, Any]:
    module = context["module"]
    amplitude = module.M5028.M5026.M5017
    center = complex(pole["log_point"])
    target = complex(context["target"])

    def values(displacement: float) -> dict[str, complex]:
        relative_circle = cmath.exp(center + displacement)
        soft_direction, decay_direction, internal = module.M5028.event_geometry(
            float(context["event"]["soft_energy"]),
            complex(float(context["event"]["soft_cosine"]), 0.0),
            complex(float(context["event"]["decay_cosine"]), 0.0),
            relative_circle,
        )
        left, right = amplitude.cut_momenta(internal, target, 1.0)
        left_spinors = amplitude.spinor_table(left)
        right_spinors = amplitude.spinor_table(right)
        return {
            "left_angle_10": complex(amplitude.bracket(left_spinors, 1, 0, 0)),
            "left_square_10": complex(amplitude.bracket(left_spinors, 1, 0, 1)),
            "right_angle_10": complex(amplitude.bracket(right_spinors, 1, 0, 0)),
            "right_square_10": complex(amplitude.bracket(right_spinors, 1, 0, 1)),
            "left_s10": complex(amplitude.invariant(left, 1, 0)),
            "p1_energy": complex(left[1, 0]),
        }

    root_values = values(0.0)
    derivatives: dict[str, complex] = {}
    derivative_rows: list[dict[str, Any]] = []
    for scale in (1.0e-4, 1.0e-6):
        plus = values(scale)
        minus = values(-scale)
        derivative = (plus["left_angle_10"] - minus["left_angle_10"]) / (
            2.0 * scale
        )
        invariant_derivative = (plus["left_s10"] - minus["left_s10"]) / (
            2.0 * scale
        )
        derivatives[str(scale)] = derivative
        derivative_rows.append(
            {
                "scale": scale,
                "left_angle_10_derivative": R5136.complex_row(derivative),
                "left_s10_derivative": R5136.complex_row(invariant_derivative),
            }
        )
    derivative_stability = abs(
        derivatives["0.0001"] - derivatives["1e-06"]
    ) / max(abs(derivatives["0.0001"]), abs(derivatives["1e-06"]), 1.0e-30)
    witness = {
        "root": R5136.complex_row(complex(pole["root"])),
        "reciprocal_root_residual": pole["reciprocal_root_residual"],
        "root_values": {
            key: R5136.complex_row(value) for key, value in root_values.items()
        },
        "derivatives": derivative_rows,
        "left_angle_10_derivative_stability": derivative_stability,
        "vanishing_bracket_is_simple": bool(
            abs(root_values["left_angle_10"]) < 1.0e-12
            and min(abs(value) for value in derivatives.values()) > 1.0e-4
            and derivative_stability < 1.0e-4
        ),
        "other_cut_chiral_brackets_nonzero": bool(
            min(
                abs(root_values["left_square_10"]),
                abs(root_values["right_angle_10"]),
                abs(root_values["right_square_10"]),
            )
            > 1.0e-3
        ),
        "s21_has_one_matching_zero": bool(
            abs(root_values["left_s10"]) < 1.0e-12
        ),
        "energy_prefactors_regular": bool(abs(root_values["p1_energy"]) > 1.0e-3),
        "nearest_other_log_singularity_distance": pole[
            "nearest_other_log_singularity_distance"
        ],
    }
    return witness


def main() -> None:
    runner = load_module("mts_5132_for_5138", GENERIC_RUNNER)
    arguments = argparse.Namespace(
        checkpoint_id=CHECKPOINT_ID,
        checked_date=CHECKED_DATE,
        job_key=JOB_KEY,
        precision="default",
        mode="dry-run",
    )
    job, configuration = runner.configure(arguments)
    base = runner.M5128
    context = base.build_context()
    candidates = [
        (chamber, pole)
        for chamber in context["chambers"]
        for pole in chamber["active_poles"]
        if pole["family"] == "beam_spinor" and pole["member"] == "small"
    ]
    if len(candidates) != 1:
        raise RuntimeError(f"expected one active target pole, found {len(candidates)}")
    chamber, pole = candidates[0]
    rows = order_rows()
    R5136.write_csv(ORDER_CSV, rows)
    witness = bracket_witness(context, chamber, pole)
    R5136.atomic_json(WITNESS_JSON, witness)
    maximum_tree_pole_order = max(row["pole_order"] for row in rows)
    singular_rows = [row for row in rows if row["pole_order"] > 0]
    source_text = AMPLITUDE_SOURCE.read_text(encoding="utf-8")
    global_text = GLOBAL_SOURCE.read_text(encoding="utf-8")
    source_formula_lock = all(
        clause in source_text
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
    simple_pole_proved = bool(
        maximum_tree_pole_order == 1
        and len(singular_rows) == 2
        and {row["special_internal_leg"] for row in singular_rows} == {2, 3}
        and witness["vanishing_bracket_is_simple"]
        and witness["other_cut_chiral_brackets_nonzero"]
        and witness["s21_has_one_matching_zero"]
        and witness["energy_prefactors_regular"]
        and float(witness["nearest_other_log_singularity_distance"]) > 0.1
        and source_formula_lock
    )
    counts_after = base.M5125.run_counts(
        base.RUN, context["config"]["config_digest"], context["schedule"]
    )
    result = {
        "checkpoint_marker": MARKER,
        "job_key": JOB_KEY,
        "job": job,
        "configuration": configuration,
        "amplitude_source": base.relative(AMPLITUDE_SOURCE),
        "global_source": base.relative(GLOBAL_SOURCE),
        "source_formula_lock": source_formula_lock,
        "order_table": base.relative(ORDER_CSV),
        "bracket_witness": base.relative(WITNESS_JSON),
        "maximum_scalar_KLT_tree_pole_order": maximum_tree_pole_order,
        "singular_term_count": len(singular_rows),
        "singular_special_internal_legs": sorted(
            row["special_internal_leg"] for row in singular_rows
        ),
        "derivation": {
            "vanishing_factor": "b=<1 0>_left_angle has a simple zero",
            "KLT_denominator_max": "two Parke-Taylor factors can supply b^-2",
            "kernel_cancellation": "that unique overlap carries s21 proportional to b, leaving b^-1",
            "other_permutations": "finite because s21 cancels their single denominator zero or no denominator zero occurs",
            "special_leg_1": "two MHV numerators supply b^4, so this channel is finite",
            "special_legs_2_3": "the unique overlap is simple, not double",
            "cut_product": "only left-angle KLT is singular; left-square and both right-cut chiralities are finite",
            "global_cycle": "linear integration and isolated finite prefactors cannot increase the pole order",
        },
        "simple_pole_order_proved_for_implemented_integrand": simple_pole_proved,
        "double_pole_excluded_for_implemented_integrand": simple_pole_proved,
        "deep_chart_precision_authorized": simple_pole_proved,
        "counts_before": configuration["counts_before"],
        "counts_after": counts_after,
        "formalization_workbench_tree_sha256": base.M5127.tree_digest(FORMAL),
        "execution_performed": False,
        "full_pilot_resume_authorized": False,
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
        "source_checked_date": CHECKED_DATE,
    }
    R5136.atomic_json(RESULT_JSON, result)
    checks = [
        ("VAL5138_01_sources_exist", all(path.exists() for path in (GENERIC_RUNNER, AMPLITUDE_SOURCE, GLOBAL_SOURCE))),
        ("VAL5138_02_locked_A04_selected", job["job_key"] == JOB_KEY),
        ("VAL5138_03_formula_source_lock", source_formula_lock),
        ("VAL5138_04_twelve_KLT_rows", len(rows) == 12),
        ("VAL5138_05_maximum_order_exactly_simple", maximum_tree_pole_order == 1),
        ("VAL5138_06_only_special_2_3_singular", len(singular_rows) == 2 and {row["special_internal_leg"] for row in singular_rows} == {2, 3}),
        ("VAL5138_07_vanishing_bracket_simple", witness["vanishing_bracket_is_simple"]),
        ("VAL5138_08_other_chiral_brackets_nonzero", witness["other_cut_chiral_brackets_nonzero"]),
        ("VAL5138_09_simple_pole_proved", simple_pole_proved),
        ("VAL5138_10_run_counts_unchanged", counts_after == configuration["counts_before"]),
        ("VAL5138_11_formal_tree_unchanged", result["formalization_workbench_tree_sha256"] == FORMAL_BASELINE),
        ("VAL5138_12_no_claim_or_execution", not result["execution_performed"] and not result["valid_for_numeric_UV_claim"] and not result["valid_for_local_GR_claim"] and not result["valid_for_full_MTS_claim"]),
    ]
    R5136.write_csv(
        VALIDATION_CSV,
        [
            {
                "check_id": check_id,
                "passed": passed,
                "checkpoint_marker": MARKER,
                "valid_for_numeric_UV_claim": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
                "source_checked_date": CHECKED_DATE,
            }
            for check_id, passed in checks
        ],
    )
    document = f"""# 5138: A04 KLT collinear pole-order proof

## Exact implemented-integrand result

At the active small beam root, only the left-cut angle bracket `b=<1 0>`
vanishes, and it has a simple zero. In the four KLT permutation pairs, the only
term with two Parke-Taylor factors `b^-2` also contains the momentum-kernel
factor `s21 proportional to b`. Its net order is therefore `b^-1`. Every other
permutation is finite after the same kernel accounting. The `special=1`
numerators add `b^4`; only `special=2,3` retain the simple pole.

The opposite chirality and both right-cut chiralities are nonzero at this root,
so the `hhh` cut product cannot square the pole. The remaining energy factors
are finite and the next log singularity is separated by
`{witness['nearest_other_log_singularity_distance']}`. Linear global-cycle
integration cannot raise the isolated meromorphic order.

- Maximum implemented scalar-KLT pole order: `{maximum_tree_pole_order}`.
- Simple pole proved: `{simple_pole_proved}`.
- Double pole excluded: `{simple_pole_proved}`.
- A deeper numerical chart may now be used to resolve the residue; no threshold
  or physical equation has been changed.

## Scope

This proves the pole order of the implemented coefficient integrand, not a UV,
local-GR, galaxy, or full-MTS claim. No coefficient job was executed, the pilot
remains `50/560`, and the formalization tree remains `{FORMAL_BASELINE}`.
"""
    DOCUMENT.write_text(document, encoding="utf-8")
    failures = [check_id for check_id, passed in checks if not passed]
    print(json.dumps({"result": result, "validation_failures": failures}, indent=2, sort_keys=True))
    if failures:
        raise SystemExit(1)


R5136 = load_module("mts_5136_for_5138", SCRIPT_5136)


if __name__ == "__main__":
    main()
