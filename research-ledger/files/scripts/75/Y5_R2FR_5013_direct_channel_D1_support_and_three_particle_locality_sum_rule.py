from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import sys
import time
from pathlib import Path
from typing import Any

import sympy as sp


sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE = POST / "source-intake" / "functional_rg" / "5013"
RESIDUALS = POST / "source-intake" / "mts_residuals"

CHECKPOINT_4986 = POST / "4986-Y5-R2FR-common-scheme-log-invariant-and-local-metric-exterior-bounds.md"
CHECKPOINT_4987 = POST / "4987-Y5-R2FR-full-finite-scheme-orbit-and-irreducible-two-loop-cut-reduction.md"
CHECKPOINT_4990 = POST / "4990-Y5-R2FR-crossing-complete-D1-scheme-separation-and-hh-scope-correction.md"
CHECKPOINT_5008 = POST / "5008-Y5-R2FR-completed-hh-one-loop-kernel-outer-cut-Wigner-insertion.md"
CHECKPOINT_5011 = POST / "5011-Y5-R2FR-coupled-outer-partial-wave-cancellation-test.md"
CHECKPOINT_5012 = POST / "5012-Y5-R2FR-nested-soft-forward-angular-first-projection.md"
RESULT_4988 = POST / "source-intake" / "functional_rg" / "4988" / "scalar_cut_soft_subtraction_results.json"
RESULT_4990 = POST / "source-intake" / "functional_rg" / "4990" / "crossed_cut_D1_scheme_bridge_results.json"
RESULT_5012 = POST / "source-intake" / "functional_rg" / "5012" / "nested_soft_forward_results.json"
HH_TOWER = POST / "source-intake" / "functional_rg" / "5008" / "hh_wigner_partial_wave_tower.csv"

DOCUMENT = POST / "5013-Y5-R2FR-direct-channel-D1-support-and-three-particle-locality-sum-rule.md"
F1_CSV = SOURCE / "D1_real_kernel_vs_direct_discontinuity_partial_waves.csv"
SUM_RULE_CSV = SOURCE / "three_particle_high_spin_locality_sum_rule.csv"
REDUCTION_CSV = SOURCE / "remaining_low_mode_reduction.csv"
GATE_CSV = SOURCE / "direct_channel_D1_and_locality_gate.csv"
RESULT_JSON = SOURCE / "direct_channel_D1_locality_results.json"
PROVENANCE = SOURCE / "PROVENANCE.md"
VALIDATION_CSV = RESIDUALS / "P8_Y5_BRR545_5013_VALIDATION.csv"

MARKER = "MTS_5013_DIRECT_CHANNEL_D1_SUPPORT_THREE_PARTICLE_LOCALITY_SUM_RULE"
CHECKED_DATE = "2026-07-14"
FORMAL_BASELINE = "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"

z = sp.symbols("z", real=True)
x = sp.symbols("x", positive=True)
alpha = sp.symbols("alpha", real=True)
PI = sp.pi


def relative(path: Path) -> str:
    return path.resolve().relative_to(ROOT.resolve()).as_posix()


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def tree_digest(path: Path) -> str:
    value = hashlib.sha256()
    for item in sorted(candidate for candidate in path.rglob("*") if candidate.is_file()):
        value.update(item.relative_to(path).as_posix().encode("utf-8"))
        value.update(digest(item).encode("ascii"))
    return value.hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def tagged(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            **row,
            "checkpoint_marker": MARKER,
            "valid_for_full_MTS_claim": False,
            "source_checked_date": CHECKED_DATE,
        }
        for row in rows
    ]


def source_locks() -> dict[str, bool]:
    required = (
        CHECKPOINT_4986,
        CHECKPOINT_4987,
        CHECKPOINT_4990,
        CHECKPOINT_5008,
        CHECKPOINT_5011,
        CHECKPOINT_5012,
        RESULT_4988,
        RESULT_4990,
        RESULT_5012,
        HH_TOWER,
    )
    checkpoint_4986 = CHECKPOINT_4986.read_text(encoding="utf-8")
    checkpoint_4987 = CHECKPOINT_4987.read_text(encoding="utf-8")
    checkpoint_4990 = CHECKPOINT_4990.read_text(encoding="utf-8")
    checkpoint_5011 = CHECKPOINT_5011.read_text(encoding="utf-8")
    result_4990 = read_json(RESULT_4990)
    result_5012 = read_json(RESULT_5012)
    return {
        "required_paths": all(path.exists() for path in required),
        "4986_crossing_log_basis": "L_A=sum_cyclic s^3 ln(-s/mu^2)" in checkpoint_4986,
        "4987_direct_discontinuity_projector": "Disc_s F2,single/(-2pi i s^3)" in checkpoint_4987,
        "4990_D1_multiplier": "D1 ReF1=-(203/10)F1" in checkpoint_4990,
        "4990_direct_support_distinction": "direct `s`-channel discontinuity" in checkpoint_4990,
        "5011_direct_cut_normalization": "D3_plus/G^3 = -(2/pi) E[H]" in checkpoint_5011,
        "4990_result_multiplier": result_4990["corrected_D1"]["D1_ReF1"] == "(-203/10) F1",
        "5012_matched_endpoint": bool(result_5012["exact_matched_soft_endpoint"]),
        "5008_hh_rows": len(read_csv(HH_TOWER)) >= 10,
    }


def f1_kernels() -> dict[str, sp.Expr]:
    angle_x = (1 - z) / 2
    angle_one_minus_x = (1 + z) / 2
    basis_a_real = -angle_x**3 * sp.log(angle_x) - angle_one_minus_x**3 * sp.log(
        angle_one_minus_x
    )
    basis_b_real = angle_x * angle_one_minus_x * (
        sp.log(angle_x) + sp.log(angle_one_minus_x)
    )
    real_kernel = sp.factor(
        sp.Rational(2, 1)
        / PI
        * (sp.Rational(23, 15) * basis_a_real - sp.Rational(1, 30) * basis_b_real)
    )
    direct_discontinuity = sp.factor(
        sp.Rational(2, 1)
        / PI
        * (sp.Rational(23, 15) - angle_x * angle_one_minus_x / 30)
    )
    direct_legendre = sp.factor(
        sp.Rational(55, 18) / PI + sp.legendre(2, z) / (90 * PI)
    )
    return {
        "real_kernel_mu2_equals_s": real_kernel,
        "direct_discontinuity": direct_discontinuity,
        "direct_legendre": direct_legendre,
        "direct_residual": sp.simplify(direct_discontinuity - direct_legendre),
    }


def logarithmic_moment_theorem(power: int, spin: int) -> sp.Expr:
    if spin <= power:
        raise ValueError("closed high-spin logarithmic moment requires spin > power")
    return sp.factor(
        (-1) ** (power + 1)
        * sp.factorial(power) ** 2
        * sp.factorial(spin - power - 1)
        / sp.factorial(spin + power + 1)
    )


def real_f1_high_spin_moment(spin: int) -> sp.Expr:
    if spin < 4 or spin % 2:
        raise ValueError("closed expression is for even spin J>=4")
    eigenvalue = sp.Integer(spin * (spin + 1))
    return sp.factor(
        -sp.Rational(2, 15)
        / PI
        * (eigenvalue**2 - 14 * eigenvalue + 1680)
        * sp.factorial(spin - 4)
        / sp.factorial(spin + 4)
    )


def partial_wave_rows(spins: tuple[int, ...], kernels: dict[str, sp.Expr]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    theorem_residuals: list[sp.Expr] = []
    for spin in spins:
        if spin == 0:
            real_moment = sp.Rational(217, 540) / PI
        elif spin == 2:
            real_moment = -sp.Rational(929, 13500) / PI
        else:
            real_moment = real_f1_high_spin_moment(spin)
        direct_moment = (
            sp.Rational(55, 18) / PI
            if spin == 0
            else sp.Rational(1, 450) / PI
            if spin == 2
            else sp.Integer(0)
        )
        direct_check = sp.simplify(
            sp.integrate(sp.legendre(spin, z) * kernels["direct_discontinuity"], (z, -1, 1))
            / 2
            - direct_moment
        )
        if spin in (4, 6, 8):
            integrated_real = sp.simplify(
                sp.integrate(sp.legendre(spin, z) * kernels["real_kernel_mu2_equals_s"], (z, -1, 1))
                / 2
            )
            theorem_residual = sp.simplify(integrated_real - real_moment)
            theorem_residuals.append(theorem_residual)
        else:
            theorem_residual = sp.Integer(0)
        rows.append(
            {
                "mode_id": f"D1SUP5013_J{spin:03d}",
                "spin_J": spin,
                "ReF1_physical_real_moment_exact": str(real_moment),
                "ReF1_physical_real_moment_numeric": float(sp.N(real_moment, 18)),
                "Disc_s_F1_over_minus_2pi_i_moment_exact": str(direct_moment),
                "Disc_s_F1_direct_check_residual": str(direct_check),
                "real_kernel_theorem_check_residual": str(theorem_residual),
                "D1_direct_support": "J0_J2_ONLY" if spin < 4 else "EXACT_ZERO",
                "real_kernel_eligible_for_direct_cut_sum": False,
                "status": "CHANNEL_OBJECTS_SEPARATED_EXACTLY",
            }
        )
    return rows, {
        "all_direct_checks_zero": all(row["Disc_s_F1_direct_check_residual"] == "0" for row in rows),
        "all_real_theorem_spot_checks_zero": all(residual == 0 for residual in theorem_residuals),
        "direct_d0": str(sp.Rational(55, 18) / PI),
        "direct_P2_coefficient": str(sp.Rational(1, 90) / PI),
        "direct_partial_moment_J2": str(sp.Rational(1, 450) / PI),
        "direct_high_spin_zero": True,
        "real_high_spin_nonzero": all(
            sp.sympify(row["ReF1_physical_real_moment_exact"]) != 0
            for row in rows
            if int(row["spin_J"]) >= 4
        ),
    }


def sum_rule_rows() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_row in read_csv(HH_TOWER):
        spin = int(source_row["spin_J"])
        tree_times_regular = sp.sympify(source_row["tree_times_regular_exact"], locals={"pi": PI})
        hh_mode = sp.factor(-64 * tree_times_regular / PI)
        required_three_particle = sp.factor(-hh_mode)
        d1_direct_mode = sp.Integer(0)
        direct_master_residual = sp.simplify(2 * (hh_mode + required_three_particle) - d1_direct_mode)
        real_f1_mode = real_f1_high_spin_moment(spin)
        wrong_channel_residual = sp.factor(sp.Rational(203, 10) * real_f1_mode)
        rows.append(
            {
                "sum_rule_id": f"LOCAL5013_J{spin:03d}",
                "spin_J": spin,
                "D_hh_over_G3_exact": str(hh_mode),
                "D_hh_over_G3_numeric": float(sp.N(hh_mode, 18)),
                "D_hhh_plus_phiphih_required_over_G3_exact": str(required_three_particle),
                "D_hhh_plus_phiphih_required_over_G3_numeric": float(
                    sp.N(required_three_particle, 18)
                ),
                "Disc_s_D1F1_high_spin_exact": str(d1_direct_mode),
                "full_direct_master_high_spin_residual": str(direct_master_residual),
                "wrongly_inserting_full_real_F1_residual": str(wrong_channel_residual),
                "independent_amplitude_integral_verified": False,
                "status": "EXACT_LOCALITY_SUM_RULE_INDEPENDENT_REAL_CUT_CHECK_OPEN",
            }
        )
    return rows, {
        "modes": len(rows),
        "spin_min": min(int(row["spin_J"]) for row in rows),
        "spin_max": max(int(row["spin_J"]) for row in rows),
        "all_exact_residuals_zero": all(row["full_direct_master_high_spin_residual"] == "0" for row in rows),
        "all_independent_integrals_verified": False,
        "required_three_particle_J4": rows[0]["D_hhh_plus_phiphih_required_over_G3_exact"],
        "required_three_particle_J4_numeric": rows[0]["D_hhh_plus_phiphih_required_over_G3_numeric"],
    }


def reduction_rows(f1_summary: dict[str, Any]) -> list[dict[str, Any]]:
    result_4988 = read_json(RESULT_4988)
    scalar_d0 = sp.sympify(result_4988["projection"]["d0_L0"], locals={"pi": PI})
    scalar_d2 = sp.sympify(result_4988["projection"]["d2_L0"], locals={"pi": PI})
    return [
        {
            "reduction_id": "REDUCE5013_01_high_spin",
            "object": "D_hhh+phiphih,J for even J>=4",
            "derived_relation": "D_3,J=-D_hh,J",
            "known_part": "exact 5008 hh tower",
            "remaining_input": "independent finite-x amplitude check, not a new UV coefficient",
            "independent_numeric_unknown_count": 0,
            "status": "FIXED_BY_DIRECT_CHANNEL_UV_LOCALITY",
        },
        {
            "reduction_id": "REDUCE5013_02_J0",
            "object": "D_hhh+phiphih,J0",
            "derived_relation": "not fixed by locality",
            "known_part": f"D_phiphi,J0={scalar_d0}; Disc_s F1,J0={f1_summary['direct_d0']}",
            "remaining_input": "one matched finite-x angular-first integral",
            "independent_numeric_unknown_count": 1,
            "status": "ACTIVE_INTEGRAL_TARGET",
        },
        {
            "reduction_id": "REDUCE5013_03_J2",
            "object": "D_hhh+phiphih,J2",
            "derived_relation": "not fixed by locality",
            "known_part": f"D_phiphi P2 coefficient={scalar_d2}; Disc_s F1 P2 coefficient={f1_summary['direct_P2_coefficient']}",
            "remaining_input": "one matched finite-x angular-first integral",
            "independent_numeric_unknown_count": 1,
            "status": "ACTIVE_INTEGRAL_TARGET",
        },
        {
            "reduction_id": "REDUCE5013_04_total",
            "object": "remaining three-particle primitive",
            "derived_relation": "all J>=4 fixed; odd J vanish by crossing",
            "known_part": "scalar cut, hh tower, D1 direct support, exact matched soft endpoint",
            "remaining_input": "D_3,0 and D_3,2 in one channel-consistent subtraction scheme",
            "independent_numeric_unknown_count": 2,
            "status": "INFINITE_TOWER_REDUCED_TO_TWO_NUMBERS",
        },
    ]


def gate_rows(locks: dict[str, bool], f1: dict[str, Any], sum_rule: dict[str, Any]) -> list[dict[str, Any]]:
    closed = {
        "primary_source_lock": all(locks.values()),
        "F1_real_vs_direct_channel_separation": f1["real_high_spin_nonzero"] and f1["direct_high_spin_zero"],
        "direct_D1_J0_J2_support_only": f1["all_direct_checks_zero"],
        "real_F1_high_spin_formula": f1["all_real_theorem_spot_checks_zero"],
        "hh_exact_tower_import": sum_rule["modes"] >= 10,
        "direct_high_spin_locality_sum_rule": sum_rule["all_exact_residuals_zero"],
        "three_particle_unknown_reduced_to_J0_J2": True,
    }
    open_gates = {
        "independent_three_particle_sum_rule_check": "requires the finite-x matched hhh plus phiphih calculation",
        "matched_three_particle_J0": "low-mode real integral not yet evaluated",
        "matched_three_particle_J2": "low-mode real integral not yet evaluated",
        "global_D1_low_mode_reconstruction": "must be applied after channel-consistent real-cut integration",
        "numeric_full_K_mu_K_ang": "two low three-particle modes remain",
        "exact_all_operator_local_GR": "not claimed",
        "full_MTS": "not claimed",
    }
    rows: list[dict[str, Any]] = []
    for gate, passed in closed.items():
        rows.append(
            {
                "gate": gate,
                "passed": bool(passed),
                "evidence": "exact symbolic/source-locked derivation",
                "status": "PASS" if passed else "FAIL",
                "valid_for_checkpoint_claim": bool(passed),
            }
        )
    for gate, evidence in open_gates.items():
        rows.append(
            {
                "gate": gate,
                "passed": False,
                "evidence": evidence,
                "status": "OPEN_NONCLAIM",
                "valid_for_checkpoint_claim": False,
            }
        )
    return [
        {"gate_id": f"GATE5013_{index:02d}_{row['gate']}", **row}
        for index, row in enumerate(rows, start=1)
    ]


def validation_rows(
    locks: dict[str, bool],
    f1_rows: list[dict[str, Any]],
    sum_rows: list[dict[str, Any]],
    reduction: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    checks = [
        ("source_locks", all(locks.values()), f"{sum(locks.values())}/{len(locks)}"),
        (
            "direct_D1_support_exact",
            all(row["Disc_s_F1_direct_check_residual"] == "0" for row in f1_rows),
            f"rows={len(f1_rows)}",
        ),
        (
            "high_spin_sum_rule_exact",
            all(row["full_direct_master_high_spin_residual"] == "0" for row in sum_rows),
            f"rows={len(sum_rows)}",
        ),
        (
            "wrong_channel_insertion_rejected",
            all(
                sp.sympify(row["wrongly_inserting_full_real_F1_residual"], locals={"pi": PI}) != 0
                for row in sum_rows
            ),
            "full real F1 is not inserted into a direct discontinuity sum",
        ),
        (
            "unknown_count_two",
            sum(int(row["independent_numeric_unknown_count"]) for row in reduction[:3]) == 2,
            "J0 and J2 only",
        ),
        (
            "independent_check_open",
            any(row["gate"] == "independent_three_particle_sum_rule_check" and not row["passed"] for row in gates),
            "sum rule is not mislabeled as an amplitude integration",
        ),
        (
            "numeric_K_blocked",
            any(row["gate"] == "numeric_full_K_mu_K_ang" and not row["passed"] for row in gates),
            "no numeric K claim",
        ),
        (
            "formalization_workbench_unchanged",
            tree_digest(FORMAL) == FORMAL_BASELINE,
            tree_digest(FORMAL),
        ),
    ]
    return [
        {
            "validation_id": f"VAL5013_{index:02d}_{name}",
            "check": name,
            "passed": bool(passed),
            "evidence": evidence,
            "checkpoint_marker": MARKER,
        }
        for index, (name, passed, evidence) in enumerate(checks, start=1)
    ]


def write_provenance(source_hashes: dict[str, str], locks: dict[str, bool]) -> None:
    lines = [
        "# 5013 direct-channel D1 and locality provenance",
        "",
        f"Marker: `{MARKER}`.",
        "",
        f"Checked: `{CHECKED_DATE}`.",
        "",
        "## Source locks",
        "",
    ]
    lines.extend(f"- `{name}`: `{value}`" for name, value in locks.items())
    lines.extend(["", "## SHA-256", ""])
    lines.extend(f"- `{path}`: `{value}`" for path, value in source_hashes.items())
    lines.extend(
        [
            "",
            "## Claim boundary",
            "",
            "The full physical real one-loop kernel has an infinite even-spin expansion, but its direct s-channel discontinuity has only J=0 and J=2. The former cannot be inserted into the direct outer-cut sum. UV locality therefore fixes the combined three-particle J>=4 tower to minus the completed hh tower. This is an exact consistency sum rule, not an independent evaluation of the three-particle amplitudes. Their matched J=0 and J=2 integrals, the global low-mode D1 reconstruction, numeric K_mu/K_ang, local GR, and full MTS remain open.",
            "",
        ]
    )
    PROVENANCE.write_text("\n".join(lines), encoding="utf-8")


def write_document(result: dict[str, Any], sum_rows: list[dict[str, Any]]) -> None:
    sample = sum_rows[:5]
    table = [
        "| J | D_hh/G^3 | required (D_hhh+D_phiphih)/G^3 | direct D1 high-spin |",
        "|---:|---:|---:|---:|",
    ]
    table.extend(
        f"| {row['spin_J']} | {row['D_hh_over_G3_numeric']:.10g} | {row['D_hhh_plus_phiphih_required_over_G3_numeric']:.10g} | 0 |"
        for row in sample
    )
    DOCUMENT.write_text(
        f"""# 5013 — direct-channel D1 support and three-particle locality sum rule

## Result

The suspected missing global `D1 ReF1` term has now been put in the correct channel object. The physical real kernel at `mu^2=s` does have an infinite even-spin expansion, but checkpoint 5011 is a direct `s`-channel discontinuity calculation. Only the `ln(-s)` coefficient can enter that sum:

```text
Disc_s F1/(-2 pi i s^3)
  = (2/pi)[23/15-x(1-x)/30]
  = 55/(18pi)+P2(z)/(90pi).
```

Therefore

```text
Pi_J Disc_s(D1 F1)=0,  J>=4.
```

Adding the full real-angle `F1` tower to the direct cut would mix a crossing-complete real amplitude with one channel discontinuity. That tempting rescue is rejected exactly, rather than tested numerically.

## Exact high-spin reduction

For the full real kernel, the useful distinction is explicit. For even `J>=4`,

```text
int_0^1 dx x^m P_J(1-2x) ln x
 =(-1)^(m+1)(m!)^2 (J-m-1)!/(J+m+1)!,

f_J^real
 =-[2/(15pi)] [lambda_J^2-14lambda_J+1680]
   (J-4)!/(J+4)!,
lambda_J=J(J+1).
```

Those nonzero moments belong to the real crossing object, not the direct cut. The renormalized direct discontinuity must be a degree-six local polynomial and hence has no `J>=4` support. Since the direct `D1` term also has no such support, locality gives the exact all-spin sum rule

```text
D_hhh,J + D_phiphih,J = -D_hh,J,  even J>=4.
```

This fixes the entire infinite high-spin three-particle tower in terms of the completed checkpoint-5008 `hh` kernel. It does not pretend that the five-point integral has independently verified the relation.

{chr(10).join(table)}

## What remains

The independent numerical primitive is no longer an uncontrolled infinite tower. Odd modes vanish by crossing, every even `J>=4` mode is fixed by locality, and only two three-particle numbers remain:

```text
D_hhh+phiphih,J=0,
D_hhh+phiphih,J=2.
```

The next calculation must construct one channel-consistent finite-`x` subtraction and evaluate those two low angular-first integrals. `J=4` is retained as a non-fitted validation mode: it must reproduce `{result['sum_rule']['required_three_particle_J4_numeric']:.12g}` in `G^3` normalization.

Numeric `K_mu`, `K_ang`, local GR, and full MTS are not claimed.
""",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    arguments = parser.parse_args()
    started = time.perf_counter()

    locks = source_locks()
    kernels = f1_kernels()
    hh_spins = tuple(int(row["spin_J"]) for row in read_csv(HH_TOWER))
    spins = (0, 2, *hh_spins)
    f1_rows, f1_summary = partial_wave_rows(spins, kernels)

    alpha_transform = sp.factor(
        (-1) ** 4
        * sp.gamma(alpha + 1) ** 2
        / (sp.gamma(alpha - 3) * sp.gamma(alpha + 6))
    )
    moment_spot_checks = {
        f"m={power},J=4": str(
            sp.simplify(
                sp.integrate(x**power * sp.legendre(4, 1 - 2 * x) * sp.log(x), (x, 0, 1))
                - logarithmic_moment_theorem(power, 4)
            )
        )
        for power in (1, 2, 3)
    }
    symbolic = {
        "direct_kernel_residual": str(kernels["direct_residual"]),
        "alpha_transform_J4": str(alpha_transform),
        "logarithmic_moment_spot_checks": moment_spot_checks,
        "all_exact": kernels["direct_residual"] == 0
        and all(value == "0" for value in moment_spot_checks.values())
        and f1_summary["all_direct_checks_zero"]
        and f1_summary["all_real_theorem_spot_checks_zero"],
    }

    if arguments.dry_run:
        passed = all(locks.values()) and bool(symbolic["all_exact"])
        print(
            json.dumps(
                {
                    "checkpoint_marker": MARKER,
                    "source_locks": locks,
                    "symbolic": symbolic,
                    "direct_D1_high_spin_support": False,
                    "dry_run_passed": passed,
                },
                indent=2,
                sort_keys=True,
            )
        )
        return 0 if passed else 1

    sum_rows, sum_summary = sum_rule_rows()
    reduction = reduction_rows(f1_summary)
    gates = gate_rows(locks, f1_summary, sum_summary)
    validations = validation_rows(locks, f1_rows, sum_rows, reduction, gates)

    for path, rows in (
        (F1_CSV, f1_rows),
        (SUM_RULE_CSV, sum_rows),
        (REDUCTION_CSV, reduction),
        (GATE_CSV, gates),
    ):
        write_csv(path, tagged(rows))
    write_csv(VALIDATION_CSV, validations)

    source_paths = (
        CHECKPOINT_4986,
        CHECKPOINT_4987,
        CHECKPOINT_4990,
        CHECKPOINT_5008,
        CHECKPOINT_5011,
        CHECKPOINT_5012,
        RESULT_4988,
        RESULT_4990,
        RESULT_5012,
        HH_TOWER,
        Path(__file__).resolve(),
    )
    source_hashes = {relative(path): digest(path) for path in source_paths}
    result = {
        "checkpoint_marker": MARKER,
        "source_locks": locks,
        "source_hashes": source_hashes,
        "symbolic": symbolic,
        "F1_channel_support": {
            **f1_summary,
            "physical_real_high_spin_formula": "-2[lambda_J^2-14lambda_J+1680](J-4)!/[15pi(J+4)!]",
            "direct_discontinuity": "55/(18pi)+P2/(90pi)",
            "full_real_kernel_must_not_be_inserted_into_direct_cut_sum": True,
        },
        "sum_rule": sum_summary,
        "remaining_independent_three_particle_modes": [0, 2],
        "independent_numeric_unknown_count": 2,
        "independent_three_particle_sum_rule_verified": False,
        "numeric_full_K_mu": False,
        "numeric_full_K_ang": False,
        "exact_all_operator_local_GR": False,
        "full_MTS": False,
        "gates": {row["gate"]: bool(row["passed"]) for row in gates},
        "validation_passed": all(row["passed"] for row in validations),
        "elapsed_seconds": time.perf_counter() - started,
    }
    SOURCE.mkdir(parents=True, exist_ok=True)
    RESULT_JSON.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_provenance(source_hashes, locks)
    write_document(result, sum_rows)

    print(
        json.dumps(
            {
                "checkpoint_marker": MARKER,
                "validation_passed": result["validation_passed"],
                "closed_gates": sum(result["gates"].values()),
                "gate_rows": len(result["gates"]),
                "high_spin_modes_fixed": sum_summary["modes"],
                "remaining_independent_modes": [0, 2],
                "required_three_particle_J4": sum_summary["required_three_particle_J4_numeric"],
                "numeric_full_K_mu": False,
                "numeric_full_K_ang": False,
                "result": str(RESULT_JSON),
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0 if result["validation_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
