from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
import time
from fractions import Fraction
from itertools import product
from pathlib import Path
from typing import Any

import sympy as sp


sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
SOURCE = POST / "source-intake" / "functional_rg" / "4994"
FORDE_SOURCE = SOURCE / "sources" / "forde_0704.1835" / "int_coeff.tex"
FORDE_ARCHIVE = SOURCE / "sources" / "forde_0704.1835" / "0704.1835.tar"
BOX_RESULT = SOURCE.parent / "4992" / "mixed_hphi_cut_and_full_box_completion_results.json"
TRIANGLE_RESULT = SOURCE.parent / "4993" / "universal_soft_operator_and_triangle_completion_results.json"

IBP_CSV = SOURCE / "mixed_u_bubble_ibp_samples.csv"
REDUCTION_CSV = SOURCE / "strict_4d_mixed_bubble_reduction.csv"
DIMENSION_CSV = SOURCE / "evanescent_dimension_scan.csv"
POLE_CSV = SOURCE / "dimensional_basis_pole.csv"
GATE_CSV = SOURCE / "mixed_bubble_gate.csv"
RESULT_JSON = SOURCE / "strict_4d_mixed_bubble_and_evanescent_pole_results.json"
PROVENANCE = SOURCE / "PROVENANCE.md"

MARKER = "MTS_4994_STRICT_4D_MIXED_BUBBLE_AND_EVANESCENT_POLE"
CHECKED_DATE = "2026-07-14"


def relative(path: Path) -> str:
    return path.resolve().relative_to(ROOT.resolve()).as_posix()


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def normalized_text(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8", errors="replace").split())


def exact(expression: sp.Expr) -> str:
    return sp.sstr(sp.factor(sp.cancel(sp.together(sp.simplify(expression)))))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
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


def source_lock() -> dict[str, bool]:
    forde = normalized_text(FORDE_SOURCE)
    box = json.loads(BOX_RESULT.read_text(encoding="utf-8"))
    triangle = json.loads(TRIANGLE_RESULT.read_text(encoding="utf-8"))
    return {
        "forde_two_particle_parameterization": (
            "Two-particle cuts and scalar bubble coefficients" in forde
            and "J_{t,y}=1" in forde
        ),
        "forde_y_moment": (
            "\\int dt dy \\;y^m=\\frac{1}{m+1}\\int dt dy" in forde
        ),
        "forde_triple_residue_correction": (
            "The bubble coefficient" in forde
            and "eq:scalar_coeff_result" in forde
            and "sum over all triple cuts obtainable" in forde
        ),
        "box_checkpoint_complete": (
            box.get("checkpoint_marker")
            == "MTS_4992_MIXED_HPHI_CUT_AND_FULL_BOX_COMPLETION"
            and bool(box.get("four_dimensional_box_sector_complete"))
        ),
        "triangle_checkpoint_complete": (
            triangle.get("checkpoint_marker")
            == "MTS_4993_UNIVERSAL_SOFT_OPERATOR_AND_TRIANGLE_COMPLETION"
            and bool(triangle.get("triangle_sector_complete_from_IR"))
        ),
    }


class OneLoopNullNumeratorReducer:
    def __init__(
        self,
        t_value: int,
        u_value: int,
        topology: str,
        dimension: Fraction,
    ) -> None:
        self.t_value = sp.Rational(t_value)
        self.u_value = sp.Rational(u_value)
        self.topology = topology
        self.dimension = dimension
        self.distance_matrix, self.null_projections = self._kinematics()
        self._rows: list[dict[tuple[int, ...], Fraction]] = []
        self._pivots: dict[tuple[int, ...], dict[tuple[int, ...], Fraction]] = {}
        self._scalar_cache: dict[
            tuple[tuple[int, ...], tuple[int, ...]], Fraction
        ] = {}
        self._build_tensor_system()

    @staticmethod
    def _fraction(value: sp.Expr | Fraction | int) -> Fraction:
        rational = sp.Rational(value)
        return Fraction(int(sp.numer(rational)), int(sp.denom(rational)))

    @staticmethod
    def _mass_squared(matrix: sp.Matrix) -> sp.Expr:
        return sp.factor(-matrix.det())

    def _kinematics(self) -> tuple[list[list[Fraction]], list[Fraction]]:
        t_value = self.t_value
        u_value = self.u_value
        lambdas = {
            1: sp.Matrix([1, 0]),
            2: sp.Matrix([0, 1]),
            3: sp.Matrix([1, -u_value]),
            4: sp.Matrix([1, t_value]),
        }
        tildes = {
            1: sp.Matrix([-1, -1]),
            2: sp.Matrix([u_value, -t_value]),
            3: sp.Matrix([1, 0]),
            4: sp.Matrix([0, 1]),
        }
        momenta = {
            index: lambdas[index] * tildes[index].T for index in range(1, 5)
        }
        channel = momenta[1] + momenta[3]
        shifts = {
            "A": momenta[1],
            "B": momenta[3],
            "C": -momenta[2],
            "D": -momenta[4],
        }
        loop_shifts = [
            sp.zeros(2),
            channel,
            shifts[self.topology[0]],
            shifts[self.topology[1]],
        ]
        distance_matrix = [
            [
                self._fraction(
                    self._mass_squared(loop_shifts[left] - loop_shifts[right])
                )
                for right in range(4)
            ]
            for left in range(4)
        ]
        null_projections = [
            self._fraction(
                u_value * shift[0, 0] + shift[1, 0]
            )
            for shift in loop_shifts
        ]
        return distance_matrix, null_projections

    def _scaleless(self, indices: tuple[int, ...] | list[int]) -> bool:
        active = [index for index, value in enumerate(indices) if value > 0]
        if len(active) < 2:
            return True
        return all(
            self.distance_matrix[left][right] == 0
            for left in active
            for right in active
        )

    def _master(self, integral: tuple[int, ...]) -> bool:
        rank, *indices = integral
        return (
            rank == 0
            and all(value in (0, 1) for value in indices)
            and not self._scaleless(indices)
        )

    def _key(self, integral: tuple[int, ...]) -> tuple[Any, ...]:
        rank, *indices = integral
        return (
            0 if self._master(integral) else 1,
            rank,
            sum(max(0, value - 1) for value in indices),
            sum(value > 0 for value in indices),
            sum(indices),
            tuple(indices),
        )

    def _add(
        self,
        row: dict[tuple[int, ...], Fraction],
        integral: tuple[int, ...],
        coefficient: Fraction,
    ) -> None:
        if coefficient == 0:
            return
        rank, *indices = integral
        if rank < 0 or any(value < 0 for value in indices) or self._scaleless(indices):
            return
        row[integral] = row.get(integral, Fraction(0)) + coefficient
        if row[integral] == 0:
            del row[integral]

    def _ibp_rows_for_seed(
        self,
        indices: tuple[int, ...],
        rank: int,
        include_null_vector: bool,
    ) -> list[dict[tuple[int, ...], Fraction]]:
        rows: list[dict[tuple[int, ...], Fraction]] = []
        total_power = sum(indices)
        for derivative_shift in range(4):
            if indices[derivative_shift] == 0:
                continue
            row: dict[tuple[int, ...], Fraction] = {}
            self._add(
                row,
                (rank, *indices),
                self.dimension + Fraction(rank - total_power),
            )
            if rank:
                self._add(
                    row,
                    (rank - 1, *indices),
                    -Fraction(rank) * self.null_projections[derivative_shift],
                )
            for denominator, power in enumerate(indices):
                if power == 0:
                    continue
                shifted = list(indices)
                shifted[denominator] += 1
                shifted[derivative_shift] -= 1
                self._add(row, (rank, *shifted), -Fraction(power))
                raised = list(indices)
                raised[denominator] += 1
                self._add(
                    row,
                    (rank, *raised),
                    Fraction(power) * self.distance_matrix[denominator][derivative_shift],
                )
            if row:
                rows.append(row)
        if include_null_vector and rank < 4:
            row = {}
            for denominator, power in enumerate(indices):
                if power == 0:
                    continue
                raised = list(indices)
                raised[denominator] += 1
                self._add(row, (rank + 1, *raised), -Fraction(power))
                self._add(
                    row,
                    (rank, *raised),
                    Fraction(power) * self.null_projections[denominator],
                )
            if row:
                rows.append(row)
        return rows

    def _eliminate(
        self,
        rows: list[dict[tuple[int, ...], Fraction]],
    ) -> dict[tuple[int, ...], dict[tuple[int, ...], Fraction]]:
        rows.sort(key=lambda row: max(self._key(item) for item in row), reverse=True)
        pivots: dict[tuple[int, ...], dict[tuple[int, ...], Fraction]] = {}
        for row in rows:
            while row:
                candidates = [item for item in row if not self._master(item)]
                if not candidates:
                    break
                pivot = max(candidates, key=self._key)
                coefficient = row[pivot]
                if pivot in pivots:
                    for item, value in pivots[pivot].items():
                        updated = row.get(item, Fraction(0)) - coefficient * value
                        if updated:
                            row[item] = updated
                        else:
                            row.pop(item, None)
                else:
                    pivots[pivot] = {
                        item: value / coefficient for item, value in row.items()
                    }
                    break
        return pivots

    def _build_tensor_system(self) -> None:
        for indices in product(range(7), repeat=4):
            if (
                sum(indices) > 6
                or sum(value > 0 for value in indices) < 2
                or self._scaleless(indices)
            ):
                continue
            for rank in range(5):
                self._rows.extend(
                    self._ibp_rows_for_seed(indices, rank, include_null_vector=True)
                )
        self._pivots = self._eliminate(self._rows)

    def _rank_one_master_coefficients(self) -> dict[tuple[int, ...], Fraction]:
        gram = sp.Matrix(
            [
                [
                    sp.Rational(
                        self.distance_matrix[0][left]
                        + self.distance_matrix[0][right]
                        - self.distance_matrix[left][right],
                        2,
                    )
                    for right in range(1, 4)
                ]
                for left in range(1, 4)
            ]
        )
        projections = sp.Matrix(
            [sp.Rational(self.null_projections[index]) for index in range(1, 4)]
        )
        scalar_box_terms = sp.Matrix(
            [
                sp.Rational(self.distance_matrix[0][index], 2)
                for index in range(1, 4)
            ]
        )
        weights = projections.T * gram.inv()
        coefficients = {
            (0, 1, 1, 1, 1): self._fraction((weights * scalar_box_terms)[0]),
            (0, 0, 1, 1, 1): self._fraction(sum(weights[0, index] for index in range(3)) / 2),
        }
        for index in range(3):
            triangle = [0, 1, 1, 1, 1]
            triangle[index + 2] = 0
            coefficients[tuple(triangle)] = self._fraction(-weights[0, index] / 2)
        return coefficients

    def _scalar_reduce(
        self,
        start: tuple[int, ...],
        master: tuple[int, ...],
    ) -> Fraction:
        cache_key = (start, master)
        if cache_key in self._scalar_cache:
            return self._scalar_cache[cache_key]
        active = {index for index, value in enumerate(start[1:]) if value > 0}
        required = {index for index, value in enumerate(master[1:]) if value > 0}
        if not required.issubset(active):
            return Fraction(0)
        maximum_sum = sum(start[1:]) + 3
        rows: list[dict[tuple[int, ...], Fraction]] = []
        for values in product(range(maximum_sum + 1), repeat=len(active)):
            indices = [0, 0, 0, 0]
            for index, value in zip(sorted(active), values):
                indices[index] = value
            if (
                sum(indices) > maximum_sum
                or sum(value > 0 for value in indices) < 2
                or self._scaleless(indices)
            ):
                continue
            rows.extend(
                self._ibp_rows_for_seed(tuple(indices), 0, include_null_vector=False)
            )
        pivots = self._eliminate(rows)
        memo: dict[tuple[int, ...], Fraction] = {}

        def walk(integral: tuple[int, ...]) -> Fraction:
            if integral == master:
                return Fraction(1)
            sector = {index for index, value in enumerate(integral[1:]) if value > 0}
            if not required.issubset(sector) or self._master(integral):
                return Fraction(0)
            if integral in memo:
                return memo[integral]
            if integral not in pivots:
                raise RuntimeError(f"unreduced scalar integral {integral}")
            result = Fraction(0)
            for child, coefficient in pivots[integral].items():
                if child != integral:
                    result -= coefficient * walk(child)
            memo[integral] = result
            return result

        value = walk(start)
        self._scalar_cache[cache_key] = value
        return value

    def coefficient_to(self, master: tuple[int, ...]) -> Fraction:
        target = (4, 1, 1, 1, 1)
        rank_one_values = self._rank_one_master_coefficients()
        rank_one_value = rank_one_values.get(master, Fraction(0))
        memo: dict[tuple[int, ...], Fraction] = {}
        required_sector = {
            index for index, value in enumerate(master[1:]) if value > 0
        }

        def walk(integral: tuple[int, ...]) -> Fraction:
            if integral == master:
                return Fraction(1)
            if integral == (1, 1, 1, 1, 1):
                return rank_one_value
            sector = {
                index for index, value in enumerate(integral[1:]) if value > 0
            }
            if not required_sector.issubset(sector) or self._master(integral):
                return Fraction(0)
            if integral in memo:
                return memo[integral]
            if integral not in self._pivots:
                if integral[0] == 0:
                    return self._scalar_reduce(integral, master)
                raise RuntimeError(f"unreduced tensor integral {integral}")
            result = Fraction(0)
            for child, coefficient in self._pivots[integral].items():
                if child != integral:
                    result -= coefficient * walk(child)
            memo[integral] = result
            return result

        return walk(target)

    def coefficients(self) -> tuple[Fraction, Fraction]:
        bubble = (0, 1, 1, 0, 0)
        box = (0, 1, 1, 1, 1)
        return self.coefficient_to(bubble), self.coefficient_to(box)


def expected_box_j(topology: str, t_value: int, u_value: int) -> sp.Expr:
    t_symbol = sp.Rational(t_value)
    u_symbol = sp.Rational(u_value)
    s_symbol = -t_symbol - u_symbol
    return sp.factor(
        {
            "AC": u_symbol**4 * (t_symbol**4 + u_symbol**4) / (2 * t_symbol**4),
            "AD": u_symbol**4 / 2,
            "BC": u_symbol**4 / 2,
            "BD": s_symbol**4 * u_symbol**4 / (2 * t_symbol**4),
        }[topology]
    )


def fraction_to_sympy(value: Fraction) -> sp.Rational:
    return sp.Rational(value.numerator, value.denominator)


def run_reducer(
    cache: dict[tuple[int, int, str, Fraction], tuple[Fraction, Fraction]],
    t_value: int,
    u_value: int,
    topology: str,
    dimension: Fraction,
) -> tuple[Fraction, Fraction]:
    key = (t_value, u_value, topology, dimension)
    if key not in cache:
        cache[key] = OneLoopNullNumeratorReducer(
            t_value, u_value, topology, dimension
        ).coefficients()
    return cache[key]


def derive_strict_four_dimensional(
    cache: dict[tuple[int, int, str, Fraction], tuple[Fraction, Fraction]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, sp.Expr]]:
    samples = [(1, 2), (1, 3), (2, 1), (2, 3), (3, 1), (3, 2), (2, 5), (3, 4)]
    interpolation_samples = samples[:6]
    held_out_samples = samples[6:]
    rows: list[dict[str, Any]] = []
    topology_values: dict[str, list[tuple[sp.Rational, sp.Rational]]] = {
        "AC": [],
        "BD": [],
    }
    for topology in ("AC", "BD"):
        for t_value, u_value in samples:
            bubble, box = run_reducer(
                cache, t_value, u_value, topology, Fraction(4)
            )
            bubble_symbolic = fraction_to_sympy(bubble)
            box_symbolic = fraction_to_sympy(box)
            x_value = sp.Rational(u_value, t_value)
            normalized = sp.factor(bubble_symbolic / sp.Rational(t_value) ** 2)
            topology_values[topology].append((x_value, normalized))
            rows.append(
                {
                    "sample_id": f"IBP4994_D4_{topology}_{t_value}_{u_value}",
                    "dimension": "4",
                    "topology": topology,
                    "t_value": t_value,
                    "u_value": u_value,
                    "bubble_J_coefficient": exact(bubble_symbolic),
                    "box_J_coefficient": exact(box_symbolic),
                    "expected_box_J": exact(expected_box_j(topology, t_value, u_value)),
                    "box_residual": exact(
                        box_symbolic - expected_box_j(topology, t_value, u_value)
                    ),
                    "sample_role": (
                        "INTERPOLATION" if (t_value, u_value) in interpolation_samples else "HELD_OUT"
                    ),
                    "status": "EXACT_RATIONAL_IBP",
                }
            )
    for topology in ("AD", "BC"):
        for t_value, u_value in ((1, 2), (2, 3), (3, 1)):
            bubble, box = run_reducer(
                cache, t_value, u_value, topology, Fraction(4)
            )
            bubble_symbolic = fraction_to_sympy(bubble)
            box_symbolic = fraction_to_sympy(box)
            rows.append(
                {
                    "sample_id": f"IBP4994_D4_{topology}_{t_value}_{u_value}",
                    "dimension": "4",
                    "topology": topology,
                    "t_value": t_value,
                    "u_value": u_value,
                    "bubble_J_coefficient": exact(bubble_symbolic),
                    "box_J_coefficient": exact(box_symbolic),
                    "expected_box_J": exact(expected_box_j(topology, t_value, u_value)),
                    "box_residual": exact(
                        box_symbolic - expected_box_j(topology, t_value, u_value)
                    ),
                    "sample_role": "ZERO_AND_BOX_CHECK",
                    "status": "EXACT_RATIONAL_IBP",
                }
            )

    x_symbol = sp.symbols("x")
    reconstructed: dict[str, sp.Expr] = {}
    for topology in ("AC", "BD"):
        reconstructed[topology] = sp.factor(
            sp.interpolate(topology_values[topology][:6], x_symbol)
        )
    expected_x = {
        "AC": x_symbol**3 * (6 * x_symbol**2 - 9 * x_symbol + 11) / 6,
        "BD": -x_symbol**3 * (6 * x_symbol**2 + 15 * x_symbol + 11) / 6,
    }
    t_symbol, u_symbol = sp.symbols("t u", nonzero=True)
    exact_j = {
        topology: sp.factor(
            t_symbol**2 * expression.subs(x_symbol, u_symbol / t_symbol)
        )
        for topology, expression in reconstructed.items()
    }
    exact_j.update({"AD": sp.Integer(0), "BC": sp.Integer(0)})
    total_j = sp.factor(sum(exact_j.values()))
    c_u = sp.factor(t_symbol**4 * total_j / 16)
    reduction_rows = [
        {
            "reduction_id": f"BUB4994_{topology}",
            "topology": topology,
            "rank_four_integral": "J4[(<l3>[4l])^4;D0,D1,E_left,E_right]",
            "bubble_J_coefficient": exact(exact_j[topology]),
            "interpolated_x_polynomial": exact(
                reconstructed[topology]
                if topology in reconstructed
                else sp.Integer(0)
            ),
            "expected_x_polynomial": exact(
                expected_x[topology] if topology in expected_x else sp.Integer(0)
            ),
            "exact_residual": exact(
                reconstructed[topology] - expected_x[topology]
                if topology in reconstructed
                else sp.Integer(0)
            ),
            "held_out_residual": exact(
                sum(
                    (
                        reconstructed[topology].subs(x_symbol, x_value) - value
                    )
                    for x_value, value in topology_values.get(topology, [])[6:]
                )
                if topology in reconstructed
                else sp.Integer(0)
            ),
            "status": "DERIVED_STRICT_FOUR_DIMENSIONAL_IBP",
        }
        for topology in ("AC", "AD", "BC", "BD")
    ]
    reduction_rows.extend(
        [
            {
                "reduction_id": "BUB4994_TOTAL_J",
                "topology": "AC+AD+BC+BD",
                "rank_four_integral": "sum of four mixed-u-cut rank-four families",
                "bubble_J_coefficient": exact(total_j),
                "interpolated_x_polynomial": "-4*x^4",
                "expected_x_polynomial": "-4*x^4",
                "exact_residual": exact(total_j + 4 * u_symbol**4 / t_symbol**2),
                "held_out_residual": "0",
                "status": "DERIVED_STRICT_FOUR_DIMENSIONAL_IBP",
            },
            {
                "reduction_id": "BUB4994_CU",
                "topology": "I2(u)",
                "rank_four_integral": "C_u=(t^4/16) sum_topology J_topology",
                "bubble_J_coefficient": exact(c_u),
                "interpolated_x_polynomial": "-t^2*u^4/4",
                "expected_x_polynomial": "-t^2*u^4/4",
                "exact_residual": exact(c_u + t_symbol**2 * u_symbol**4 / 4),
                "held_out_residual": "0",
                "status": "STRICT_4D_MIXED_U_BUBBLE_COMPLETE",
            },
        ]
    )
    return rows, reduction_rows, {
        "J_AC": exact_j["AC"],
        "J_AD": exact_j["AD"],
        "J_BC": exact_j["BC"],
        "J_BD": exact_j["BD"],
        "J_total": total_j,
        "C_u_4D": c_u,
    }


def derive_dimension_scan(
    cache: dict[tuple[int, int, str, Fraction], tuple[Fraction, Fraction]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, sp.Expr]]:
    dimension_symbol = sp.symbols("D")
    reconstruction_dimensions = [
        Fraction(7, 2),
        Fraction(15, 4),
        Fraction(19, 5),
        Fraction(21, 5),
    ]
    validation_dimensions = [Fraction(9, 2), Fraction(5), Fraction(11, 2)]
    scan_rows: list[dict[str, Any]] = []
    values: list[tuple[sp.Rational, sp.Rational]] = []
    for dimension in reconstruction_dimensions + validation_dimensions:
        bubble_ac, box_ac = run_reducer(cache, 1, 2, "AC", dimension)
        c_u = fraction_to_sympy(bubble_ac) / 16
        values.append(
            (
                sp.Rational(dimension.numerator, dimension.denominator),
                sp.factor(c_u),
            )
        )
        scan_rows.append(
            {
                "scan_id": f"DIM4994_{dimension.numerator}_{dimension.denominator}",
                "t_value": 1,
                "u_value": 2,
                "dimension": str(dimension),
                "AC_bubble_J": exact(fraction_to_sympy(bubble_ac)),
                "AC_box_J": exact(fraction_to_sympy(box_ac)),
                "C_u_dimension_slice": exact(c_u),
                "sample_role": (
                    "RECONSTRUCTION"
                    if dimension in reconstruction_dimensions
                    else "HELD_OUT_VALIDATION"
                ),
                "status": "EXACT_RATIONAL_IBP",
            }
        )
    other_topology_residual = sp.Integer(0)
    for topology in ("AD", "BC", "BD"):
        bubble, _ = run_reducer(cache, 1, 2, topology, Fraction(5))
        other_topology_residual += fraction_to_sympy(bubble)

    denominator = (dimension_symbol - 4) * (dimension_symbol - 2) * (
        dimension_symbol - 1
    )
    coefficients = sp.symbols("a0:4")
    numerator = sum(
        coefficients[index] * dimension_symbol**index for index in range(4)
    )
    solution = sp.solve(
        [
            sp.Eq(
                numerator.subs(dimension_symbol, dimension),
                value * denominator.subs(dimension_symbol, dimension),
            )
            for dimension, value in values[:4]
        ],
        coefficients,
        dict=True,
    )[0]
    reconstructed = sp.factor(numerator.subs(solution) / denominator)
    expected = sp.factor(
        -(
            27 * dimension_symbol**3
            + 532 * dimension_symbol**2
            - 6036 * dimension_symbol
            + 8720
        )
        / (
            40
            * (dimension_symbol - 4)
            * (dimension_symbol - 2)
            * (dimension_symbol - 1)
        )
    )
    validation_residuals = [
        sp.factor(reconstructed.subs(dimension_symbol, dimension) - value)
        for dimension, value in values[4:]
    ]
    residue = sp.factor(
        sp.limit((dimension_symbol - 4) * reconstructed, dimension_symbol, 4)
    )
    finite = sp.factor(
        sp.limit(
            reconstructed - residue / (dimension_symbol - 4),
            dimension_symbol,
            4,
        )
    )
    epsilon = sp.symbols("epsilon")
    epsilon_pole = sp.factor(residue / (-2 * epsilon))
    pole_rows = [
        {
            "pole_id": "EVAN4994_01_dimension_slice",
            "kinematic_slice": "t=1,u=2",
            "quantity": "generic-D scalar-bubble coefficient C_u(D)",
            "exact_value": exact(reconstructed),
            "comparison": exact(expected),
            "exact_residual": exact(reconstructed - expected),
            "status": "EXACT_RATIONAL_RECONSTRUCTION",
        },
        {
            "pole_id": "EVAN4994_02_residue",
            "kinematic_slice": "t=1,u=2",
            "quantity": "Res_{D=4} C_u(D)",
            "exact_value": exact(residue),
            "comparison": "108/5",
            "exact_residual": exact(residue - sp.Rational(108, 5)),
            "status": "NONZERO_EVANESCENT_BASIS_POLE",
        },
        {
            "pole_id": "EVAN4994_03_finite",
            "kinematic_slice": "t=1,u=2",
            "quantity": "finite part after subtracting Res/(D-4)",
            "exact_value": exact(finite),
            "comparison": "-959/60",
            "exact_residual": exact(finite + sp.Rational(959, 60)),
            "status": "EVANESCENT_FINITE_PART_NOT_YET_PHYSICAL",
        },
        {
            "pole_id": "EVAN4994_04_epsilon",
            "kinematic_slice": "D=4-2epsilon,t=1,u=2",
            "quantity": "basis-pole term",
            "exact_value": exact(epsilon_pole),
            "comparison": "-54/(5*epsilon)",
            "exact_residual": exact(epsilon_pole + sp.Rational(54, 5) / epsilon),
            "status": "MUST_CANCEL_WITH_EVANESCENT_BOX_TRIANGLE_RATIONAL_SECTOR",
        },
        {
            "pole_id": "EVAN4994_05_strict4D",
            "kinematic_slice": "t=1,u=2",
            "quantity": "strict-four-dimensional C_u",
            "exact_value": "-4",
            "comparison": exact(finite),
            "exact_residual": exact(-4 - finite),
            "status": "NONCOMMUTING_BASIS_LIMIT_PROVED",
        },
    ]
    return scan_rows, pole_rows, {
        "dimension_slice": reconstructed,
        "expected_dimension_slice": expected,
        "held_out_residual_sum": sp.factor(sum(validation_residuals)),
        "residue_D4": residue,
        "finite_after_basis_pole": finite,
        "other_topology_D5_bubble_sum": other_topology_residual,
    }


def gate_rows(
    source_checks: dict[str, bool],
    ibp_rows: list[dict[str, Any]],
    reduction_rows: list[dict[str, Any]],
    dimension: dict[str, sp.Expr],
) -> list[dict[str, Any]]:
    closed = {
        "primary_source_lock": all(source_checks.values()),
        "exact_rank_four_ibp": len(ibp_rows) >= 22,
        "all_box_leading_singularities_reproduced": all(
            row["box_residual"] == "0" for row in ibp_rows
        ),
        "AC_formula_reconstructed": reduction_rows[0]["exact_residual"] == "0",
        "BD_formula_reconstructed": reduction_rows[3]["exact_residual"] == "0",
        "held_out_kinematics_pass": all(
            row["held_out_residual"] == "0" for row in reduction_rows[:4]
        ),
        "strict_4D_mixed_u_bubble": reduction_rows[-1]["exact_residual"] == "0",
        "generic_D_slice_reconstructed": sp.factor(
            dimension["dimension_slice"] - dimension["expected_dimension_slice"]
        )
        == 0,
        "generic_D_held_out_pass": dimension["held_out_residual_sum"] == 0,
        "generic_D_other_topologies_zero_at_anchor": (
            dimension["other_topology_D5_bubble_sum"] == 0
        ),
        "evanescent_basis_pole_detected": dimension["residue_D4"] != 0,
    }
    open_gates = {
        "generic_D_all_kinematics": "only one exact dimensional diagnostic slice is reconstructed",
        "evanescent_box_triangle_cancellation": "the 1/(D-4) basis pole must be combined with generic-D boxes and triangles",
        "rational_remainder": "no physical rational term is promoted before that cancellation",
        "scalar_intermediate_s_bubble": "the identical-scalar s-cut bubble remains to be reduced",
        "full_bubble_sector": "C_t follows by crossing but C_s still lacks its scalar-intermediate component",
        "complete_one_loop_phi2h2": "the strict-4D mixed bubble is not a complete dimensionally regulated amplitude",
        "crossing_complete_outer_hh_cut": "one-loop hard kernel remains incomplete",
        "numeric_full_K_mu_K_ang": "outer cut remains open",
        "exact_all_operator_local_GR": "not claimed",
        "full_MTS": "not claimed",
    }
    rows: list[dict[str, Any]] = []
    for name, passed in closed.items():
        rows.append(
            {
                "gate": name,
                "passed": bool(passed),
                "evidence": "exact source lock, rational IBP, or held-out reconstruction",
                "status": "PASS" if passed else "FAIL",
                "valid_for_checkpoint_claim": bool(passed),
            }
        )
    for name, evidence in open_gates.items():
        rows.append(
            {
                "gate": name,
                "passed": False,
                "evidence": evidence,
                "status": "OPEN_NONCLAIM",
                "valid_for_checkpoint_claim": False,
            }
        )
    return [
        dict(gate_id=f"GATE4994_{index:02d}_{row['gate']}", **row)
        for index, row in enumerate(rows, start=1)
    ]


def write_provenance(
    source_hashes: dict[str, str],
    source_checks: dict[str, bool],
) -> None:
    lines = [
        "# 4994 strict-4D mixed bubble and evanescent-pole provenance",
        "",
        f"Marker: {MARKER}.",
        "",
        f"Checked: {CHECKED_DATE}.",
        "",
        "## Primary method source",
        "",
        "- D. Forde, Direct extraction of one-loop integral coefficients, Phys. Rev. D 75, 125019 (2007), arXiv:0704.1835, DOI 10.1103/PhysRevD.75.125019: two-particle cut parameterization, non-vanishing y moments, and triple-residue correction required for bubble coefficients.",
        "",
        "## Inherited amplitude inputs",
        "",
        "- Checkpoint 4992 supplies the exact mixed h-phi u-cut numerator, four uncut propagators, and four scalar-box leading singularities.",
        "- Checkpoint 4993 supplies the completed four-dimensional triangle sector and fixes the boundary beyond which a generic-D result must not be mixed without evanescent completion.",
        "",
        "## Source checks",
        "",
    ]
    lines.extend(f"- {name}: {value}" for name, value in source_checks.items())
    lines.extend(["", "## SHA-256", ""])
    lines.extend(f"- {path}: {value}" for path, value in source_hashes.items())
    lines.extend(
        [
            "",
            "## Claim boundary",
            "",
            "This checkpoint derives the strict-four-dimensional mixed-u bubble coefficient and proves an evanescent scalar-basis pole on one exact generic-D kinematic slice. It deliberately does not call the finite part of that slice physical, does not claim the generic-D bubble sector complete, and does not promote a complete one-loop, outer-cut, local-GR, or full-MTS result.",
        ]
    )
    PROVENANCE.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    started = time.perf_counter()

    source_checks = source_lock()
    if not all(source_checks.values()):
        failed = [name for name, passed in source_checks.items() if not passed]
        raise RuntimeError(f"source lock failed: {failed}")

    if args.dry_run:
        print(
            json.dumps(
                {
                    "checkpoint_marker": MARKER,
                    "source_checks": source_checks,
                    "planned_strict_4D_result": "C_u=-t^2*u^4/4",
                    "planned_dimension_slice": "t=1,u=2",
                    "dry_run": True,
                },
                indent=2,
                sort_keys=True,
            )
        )
        return 0

    cache: dict[tuple[int, int, str, Fraction], tuple[Fraction, Fraction]] = {}
    ibp_rows, reduction_rows, strict = derive_strict_four_dimensional(cache)
    dimension_rows, pole_rows, dimension = derive_dimension_scan(cache)
    gates = gate_rows(source_checks, ibp_rows, reduction_rows, dimension)
    failed = [row["gate"] for row in gates if row["status"] == "FAIL"]
    if failed:
        raise RuntimeError(f"closed derivation gates failed: {failed}")

    for path, rows in (
        (IBP_CSV, ibp_rows),
        (REDUCTION_CSV, reduction_rows),
        (DIMENSION_CSV, dimension_rows),
        (POLE_CSV, pole_rows),
        (GATE_CSV, gates),
    ):
        write_csv(path, tagged(rows))

    script_path = Path(__file__).resolve()
    source_paths = [
        FORDE_SOURCE,
        FORDE_ARCHIVE,
        BOX_RESULT,
        TRIANGLE_RESULT,
        script_path,
    ]
    source_hashes = {relative(path): digest(path) for path in source_paths}
    result = {
        "checkpoint_marker": MARKER,
        "source_checks": source_checks,
        "source_hashes": source_hashes,
        "amplitude_convention": "M1=kappa^4 F/<1|3|2]^4",
        "strict_four_dimensional_mixed_u_bubble": {
            "J_AC": exact(strict["J_AC"]),
            "J_AD": exact(strict["J_AD"]),
            "J_BC": exact(strict["J_BC"]),
            "J_BD": exact(strict["J_BD"]),
            "J_total": exact(strict["J_total"]),
            "C_u": exact(strict["C_u_4D"]),
        },
        "generic_dimension_diagnostic_slice": {
            "kinematics": "t=1,u=2",
            "C_u_D": exact(dimension["dimension_slice"]),
            "residue_at_D4": exact(dimension["residue_D4"]),
            "finite_after_basis_pole_subtraction": exact(
                dimension["finite_after_basis_pole"]
            ),
            "strict_4D_value": "-4",
        },
        "strict_four_dimensional_mixed_u_bubble_complete": True,
        "generic_D_bubble_sector_complete": False,
        "evanescent_box_triangle_cancellation_complete": False,
        "complete_one_loop_phi2h2": False,
        "crossing_complete_outer_hh_cut": False,
        "numeric_full_K_mu": False,
        "numeric_full_K_ang": False,
        "exact_all_operator_local_GR": False,
        "full_MTS": False,
        "gates": {row["gate"]: bool(row["passed"]) for row in gates},
        "elapsed_seconds": time.perf_counter() - started,
        "dry_run": False,
    }
    RESULT_JSON.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    write_provenance(source_hashes, source_checks)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
