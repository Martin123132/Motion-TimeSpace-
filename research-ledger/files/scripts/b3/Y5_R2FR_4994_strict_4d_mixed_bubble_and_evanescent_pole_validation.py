from __future__ import annotations

import csv
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

import sympy as sp


sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
SOURCE = POST / "source-intake" / "functional_rg" / "4994"
IBP_CSV = SOURCE / "mixed_u_bubble_ibp_samples.csv"
REDUCTION_CSV = SOURCE / "strict_4d_mixed_bubble_reduction.csv"
DIMENSION_CSV = SOURCE / "evanescent_dimension_scan.csv"
POLE_CSV = SOURCE / "dimensional_basis_pole.csv"
GATE_CSV = SOURCE / "mixed_bubble_gate.csv"
RESULT_JSON = SOURCE / "strict_4d_mixed_bubble_and_evanescent_pole_results.json"
PROVENANCE = SOURCE / "PROVENANCE.md"
GENERATOR = POST / "scripts" / "Y5_R2FR_4994_strict_4d_mixed_bubble_and_evanescent_pole.py"
FORDE_SOURCE = SOURCE / "sources" / "forde_0704.1835" / "int_coeff.tex"
OUTPUT = POST / "source-intake" / "mts_residuals" / "P8_Y5_BRR545_4994_VALIDATION.csv"

MARKER = "MTS_4994_STRICT_4D_MIXED_BUBBLE_AND_EVANESCENT_POLE"

t, u, x, D, epsilon = sp.symbols("t u x D epsilon", nonzero=True)
LOCALS = {"t": t, "u": u, "x": x, "D": D, "epsilon": epsilon}


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def expression(value: str) -> sp.Expr:
    return sp.factor(sp.sympify(value.replace("^", "**"), locals=LOCALS))


def zero(value: sp.Expr) -> bool:
    return sp.factor(sp.cancel(sp.together(sp.simplify(value)))) == 0


def main() -> int:
    checks: list[dict[str, Any]] = []

    def check(name: str, passed: bool, evidence: str) -> None:
        checks.append(
            {
                "validation_id": f"VAL4994_{len(checks) + 1:03d}",
                "check": name,
                "passed": bool(passed),
                "evidence": evidence,
                "status": "PASS" if passed else "FAIL",
                "checkpoint_marker": MARKER,
            }
        )

    required = [
        IBP_CSV,
        REDUCTION_CSV,
        DIMENSION_CSV,
        POLE_CSV,
        GATE_CSV,
        RESULT_JSON,
        PROVENANCE,
        GENERATOR,
        FORDE_SOURCE,
    ]
    for path in required:
        check(f"path_exists_{path.name}", path.exists(), str(path))

    ibp = read_csv(IBP_CSV)
    reduction = read_csv(REDUCTION_CSV)
    dimension = read_csv(DIMENSION_CSV)
    poles = read_csv(POLE_CSV)
    gates = read_csv(GATE_CSV)
    result = json.loads(RESULT_JSON.read_text(encoding="utf-8"))

    for name, rows in (
        ("ibp", ibp),
        ("reduction", reduction),
        ("dimension", dimension),
        ("poles", poles),
        ("gates", gates),
    ):
        check(f"{name}_nonempty", bool(rows), str(len(rows)))
        check(
            f"{name}_marker",
            all(row.get("checkpoint_marker") == MARKER for row in rows),
            "all rows carry marker",
        )
        check(
            f"{name}_nonclaim",
            all(row.get("valid_for_full_MTS_claim") == "False" for row in rows),
            "all rows remain full-MTS nonclaim",
        )

    check("result_marker", result.get("checkpoint_marker") == MARKER, MARKER)
    check(
        "generator_hash",
        result["source_hashes"][
            "post-checkpoint-work/scripts/Y5_R2FR_4994_strict_4d_mixed_bubble_and_evanescent_pole.py"
        ]
        == digest(GENERATOR),
        digest(GENERATOR),
    )
    check(
        "source_hashes_exist",
        all((ROOT / path).exists() for path in result["source_hashes"]),
        str(len(result["source_hashes"])),
    )

    for row in ibp:
        check(
            f"box_residual_{row['sample_id']}",
            expression(row["box_residual"]) == 0,
            row["box_residual"],
        )
        check(
            f"numeric_fields_{row['sample_id']}",
            all(
                expression(row[field]).is_number
                for field in ("bubble_J_coefficient", "box_J_coefficient", "expected_box_J")
            ),
            row["topology"],
        )

    by_id = {row["reduction_id"]: row for row in reduction}
    expected = {
        "BUB4994_AC": u**3 * (11 * t**2 - 9 * t * u + 6 * u**2) / (6 * t**3),
        "BUB4994_AD": sp.Integer(0),
        "BUB4994_BC": sp.Integer(0),
        "BUB4994_BD": -u**3 * (11 * t**2 + 15 * t * u + 6 * u**2) / (6 * t**3),
        "BUB4994_TOTAL_J": -4 * u**4 / t**2,
        "BUB4994_CU": -t**2 * u**4 / 4,
    }
    for row_id, expected_value in expected.items():
        actual = expression(by_id[row_id]["bubble_J_coefficient"])
        check(f"formula_{row_id}", zero(actual - expected_value), str(actual))
        check(
            f"recorded_residual_{row_id}",
            expression(by_id[row_id]["exact_residual"]) == 0,
            by_id[row_id]["exact_residual"],
        )

    ac_rows = [row for row in ibp if row["topology"] == "AC"]
    bd_rows = [row for row in ibp if row["topology"] == "BD"]
    for topology, rows, expected_polynomial in (
        ("AC", ac_rows, x**3 * (6 * x**2 - 9 * x + 11) / 6),
        ("BD", bd_rows, -x**3 * (6 * x**2 + 15 * x + 11) / 6),
    ):
        interpolation_points = []
        held_out = []
        for row in rows:
            t_value = sp.Rational(row["t_value"])
            u_value = sp.Rational(row["u_value"])
            normalized = expression(row["bubble_J_coefficient"]) / t_value**2
            item = (u_value / t_value, sp.factor(normalized))
            if row["sample_role"] == "INTERPOLATION":
                interpolation_points.append(item)
            else:
                held_out.append(item)
        polynomial = sp.factor(sp.interpolate(interpolation_points, x))
        check(
            f"independent_interpolation_{topology}",
            zero(polynomial - expected_polynomial),
            str(polynomial),
        )
        for index, (x_value, value) in enumerate(held_out, start=1):
            check(
                f"held_out_{topology}_{index}",
                zero(polynomial.subs(x, x_value) - value),
                f"x={x_value}",
            )

    c_u = expression(result["strict_four_dimensional_mixed_u_bubble"]["C_u"])
    c_t = sp.factor(c_u.xreplace({t: u, u: t}))
    check("strict_Cu", zero(c_u + t**2 * u**4 / 4), str(c_u))
    check("crossed_Ct", zero(c_t + u**2 * t**4 / 4), str(c_t))
    for t_value in range(1, 10):
        for u_value in range(1, 10):
            substitutions = {t: sp.Rational(t_value), u: sp.Rational(u_value)}
            ac = expected["BUB4994_AC"].subs(substitutions)
            bd = expected["BUB4994_BD"].subs(substitutions)
            total = expected["BUB4994_TOTAL_J"].subs(substitutions)
            check(
                f"grid_total_{t_value}_{u_value}",
                zero(ac + bd - total),
                f"t={t_value},u={u_value}",
            )

    scan_points = [
        (sp.Rational(row["dimension"]), expression(row["C_u_dimension_slice"]))
        for row in dimension
    ]
    reconstruction = [
        point
        for point, row in zip(scan_points, dimension)
        if row["sample_role"] == "RECONSTRUCTION"
    ]
    denominator = (D - 4) * (D - 2) * (D - 1)
    coefficients = sp.symbols("b0:4")
    numerator = sum(coefficients[index] * D**index for index in range(4))
    solution = sp.solve(
        [
            sp.Eq(numerator.subs(D, dimension_value), value * denominator.subs(D, dimension_value))
            for dimension_value, value in reconstruction
        ],
        coefficients,
        dict=True,
    )[0]
    dimensional_formula = sp.factor(numerator.subs(solution) / denominator)
    expected_dimensional = -(
        27 * D**3 + 532 * D**2 - 6036 * D + 8720
    ) / (40 * (D - 4) * (D - 2) * (D - 1))
    check(
        "independent_dimension_reconstruction",
        zero(dimensional_formula - expected_dimensional),
        str(dimensional_formula),
    )
    for row, (dimension_value, value) in zip(dimension, scan_points):
        check(
            f"dimension_point_{row['scan_id']}",
            zero(dimensional_formula.subs(D, dimension_value) - value),
            row["dimension"],
        )

    residue = sp.factor(sp.limit((D - 4) * dimensional_formula, D, 4))
    finite = sp.factor(
        sp.limit(dimensional_formula - residue / (D - 4), D, 4)
    )
    check("dimension_residue", residue == sp.Rational(108, 5), str(residue))
    check("dimension_finite", finite == -sp.Rational(959, 60), str(finite))
    check(
        "epsilon_basis_pole",
        zero(residue / (-2 * epsilon) + sp.Rational(54, 5) / epsilon),
        str(residue / (-2 * epsilon)),
    )
    check("noncommuting_limit", finite != -4, f"finite={finite},strict=-4")

    pole_by_id = {row["pole_id"]: row for row in poles}
    for row_id in pole_by_id:
        check(
            f"pole_record_{row_id}",
            expression(pole_by_id[row_id]["exact_residual"]) == 0
            if row_id != "EVAN4994_05_strict4D"
            else expression(pole_by_id[row_id]["exact_residual"]) != 0,
            pole_by_id[row_id]["exact_residual"],
        )

    closed_gate_failures = [row for row in gates if row["status"] == "FAIL"]
    check("no_closed_gate_failures", not closed_gate_failures, str(closed_gate_failures))
    open_names = {row["gate"] for row in gates if row["status"] == "OPEN_NONCLAIM"}
    for gate in (
        "generic_D_all_kinematics",
        "evanescent_box_triangle_cancellation",
        "rational_remainder",
        "scalar_intermediate_s_bubble",
        "complete_one_loop_phi2h2",
        "crossing_complete_outer_hh_cut",
        "exact_all_operator_local_GR",
        "full_MTS",
    ):
        check(f"open_gate_{gate}", gate in open_names, gate)

    failed = [row for row in checks if not row["passed"]]
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(checks[0]))
        writer.writeheader()
        writer.writerows(checks)
    print(
        json.dumps(
            {
                "checkpoint_marker": MARKER,
                "checks": len(checks),
                "passed": len(checks) - len(failed),
                "failed": len(failed),
                "output": str(OUTPUT),
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
