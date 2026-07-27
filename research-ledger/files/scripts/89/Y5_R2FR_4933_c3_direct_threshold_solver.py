from __future__ import annotations

import hashlib
import json
import math
import sys
import time
from collections import Counter
from pathlib import Path
from typing import Any

import numpy as np
import sympy as sp
from mathics.core.definitions import Definitions
from mathics.core.parser import MathicsSingleLineFeeder, parse
from scipy.optimize import root

from Y5_R2FR_4933_c3_flow_execution import extracted_cells, normalize_mathics_symbols


sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "functional_rg" / "4933"
EXTRACTED_INPUT = SOURCE_DIR / "Flow_mendeley_input_extracted.wl"
OUTPUT_JSON = SOURCE_DIR / "C3_direct_threshold_results.json"
MARKER = "MTS_4933_C3_DIRECT_THRESHOLD_SOLVER"

EXPECTED_EXTRACTED_HASH = "7a6ce0ad809f1c8932511d4652542599ea30499805d8b71a5b758443a0e797d1"
EXPECTED_SOURCE_G = 0.36418717658660363265123005959504022619
EXPECTED_SOURCE_H = 4.4900304240849397335957221303384106e-7
EXPECTED_SOURCE_EXPONENTS = (-3.8496242355726396408459976515985370, 2.2251862592254120885349977188494456)


z = sp.Symbol("z", real=True)
g = sp.Symbol("g", positive=True)
h = sp.Symbol("h", real=True)
rho = sp.Symbol("rho", positive=True)
d2 = sp.Symbol("d2")

beta_g, beta_h, beta_sigma = sp.symbols("beta_g beta_h beta_sigma")
gamma_g, gamma_r, gamma_s, gamma_r2, gamma_c2 = sp.symbols(
    "gamma_g gamma_r gamma_s gamma_r2 gamma_c2"
)
gamma_sstl, gamma_rs, gamma_cs, gamma_delta_r, gamma_delta_s = sp.symbols(
    "gamma_sstl gamma_rs gamma_cs gamma_delta_r gamma_delta_s"
)

UNKNOWNS = (
    beta_g,
    beta_h,
    beta_sigma,
    gamma_g,
    gamma_r,
    gamma_s,
    gamma_r2,
    gamma_c2,
    gamma_sstl,
    gamma_rs,
    gamma_cs,
    gamma_delta_r,
    gamma_delta_s,
)

SYMBOLS = {
    "z": z,
    "WLBeta": sp.Integer(1),
    "gammaG": gamma_g,
    "gammaR": gamma_r,
    "gammaS": gamma_s,
    "gammaR2": gamma_r2,
    "gammaC2": gamma_c2,
    "gammaSSTL": gamma_sstl,
    "gammaRS": gamma_rs,
    "gammaCS": gamma_cs,
    "gammaDeltaR": gamma_delta_r,
    "gammaDeltaS": gamma_delta_s,
    "gammaDDR": sp.Integer(0),
    "gammaS2": sp.Integer(0),
}

A_REG = 1 / (32 * sp.pi * g)
B_GHOST = 1 / (4 * sp.sqrt(sp.pi) * sp.sqrt(g))


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def short_name(symbol: Any) -> str:
    return str(getattr(symbol, "name", symbol)).split("`")[-1]


def head_name(expression: Any) -> str:
    head = getattr(expression, "head", None)
    return short_name(head) if getattr(head, "name", None) is not None else ""


def atom(expression: Any) -> sp.Expr:
    if getattr(expression, "value", None) is not None:
        value = expression.value
        if isinstance(value, int):
            return sp.Integer(value)
        if isinstance(value, float):
            return sp.Float(value)
    name = short_name(expression)
    if name == "Pi":
        return sp.pi
    if name in SYMBOLS:
        return SYMBOLS[name]
    raise ValueError(f"unsupported atom {expression!r}")


def derivative_signature(expression: Any) -> tuple[tuple[int, ...], str] | None:
    head = getattr(expression, "head", None)
    if getattr(head, "name", None) is not None:
        return None
    derivative_head = getattr(head, "head", None)
    if derivative_head is None or head_name(derivative_head) != "Derivative":
        return None
    orders = tuple(int(getattr(element, "value")) for element in derivative_head.elements)
    function_elements = tuple(getattr(head, "elements", ()))
    if len(function_elements) != 1:
        raise ValueError(f"unsupported derivative function {head!r}")
    return orders, short_name(function_elements[0])


class DirectThresholdConverter:
    def __init__(self) -> None:
        self.q_count = 0
        self.q_orders: Counter[int] = Counter()
        self.q_distribution_nonzero = 0
        self.q_distribution_higher_power = 0
        self.q_max_regular_degree = 0

    def q_functional(self, order: int, argument: sp.Expr) -> sp.Expr:
        self.q_count += 1
        self.q_orders[order] += 1
        cancelled = sp.cancel(argument)
        numerator, denominator = sp.fraction(cancelled)
        denominator = sp.factor(denominator)
        if denominator.has(z) or denominator.has(d2):
            cancelled = sp.cancel(sp.together(cancelled))
            numerator, denominator = sp.fraction(cancelled)
            denominator = sp.factor(denominator)
        if denominator.has(z) or denominator.has(d2):
            raise ValueError(f"nonconstant Litim denominator in Q_{order}: {denominator}")

        numerator = sp.expand(numerator)
        regular_numerator = sp.expand(numerator.subs(d2, 0))
        distribution_coefficient = sp.expand(numerator).coeff(d2, 1)
        higher_distribution = sp.expand(numerator - regular_numerator - distribution_coefficient * d2)
        if higher_distribution != 0:
            self.q_distribution_higher_power += 1

        if order > 0:
            polynomial = sp.Poly(regular_numerator, z)
            self.q_max_regular_degree = max(self.q_max_regular_degree, polynomial.degree())
            regular = sp.Add(
                *(
                    coefficient / (power[0] + order)
                    for power, coefficient in polynomial.terms()
                )
            ) / math.factorial(order - 1)
            distribution = sp.Integer(0)
            boundary_coefficient = sp.simplify(distribution_coefficient.subs(z, 1))
            if boundary_coefficient != 0:
                self.q_distribution_nonzero += 1
                distribution = boundary_coefficient / (2 * math.factorial(order - 1))
            result = (regular + distribution) / denominator
        elif order == 0:
            if distribution_coefficient != 0:
                raise ValueError("Q_0 contains an unresolved Litim boundary distribution")
            result = regular_numerator.subs(z, 0) / denominator
        else:
            derivative_order = -order
            if distribution_coefficient != 0:
                raise ValueError(f"Q_{order} contains an unresolved Litim boundary distribution")
            result = ((-1) ** order) * sp.diff(regular_numerator / denominator, z, derivative_order).subs(z, 0)

        if self.q_count % 250 == 0:
            print(f"{MARKER}_Q_PROGRESS={self.q_count}", flush=True)
        return sp.factor(result)

    def derivative(self, orders: tuple[int, ...], function: str) -> sp.Expr:
        if function == "GN" and orders == (1,):
            return beta_g
        if function == "GGS" and orders == (1,):
            return beta_h
        if function == "SigmaEuler" and orders == (1,):
            return beta_sigma
        if function == "WLRho" and orders == (1,):
            return sp.Integer(0)
        if function == "Reg":
            if orders == (0, 1):
                return -A_REG
            if orders == (0, 2):
                return A_REG * d2
            if orders == (1, 0):
                return A_REG * ((2 - beta_g / g) * (1 - z) + 2)
        if function == "Regghc":
            if orders == (0, 1):
                return -B_GHOST
            if orders == (0, 2):
                return B_GHOST * d2
            if orders == (1, 0):
                return B_GHOST * ((1 - beta_g / (2 * g)) * (1 - z) + 2)
        raise ValueError(f"unsupported derivative Derivative{orders}[{function}]")

    def convert(self, expression: Any) -> sp.Expr:
        signature = derivative_signature(expression)
        if signature is not None:
            return self.derivative(*signature)

        name = head_name(expression)
        elements = tuple(getattr(expression, "elements", ()))
        if not name:
            return atom(expression)
        if name == "Plus":
            return sp.Add(*(self.convert(element) for element in elements))
        if name == "Times":
            return sp.Mul(*(self.convert(element) for element in elements))
        if name == "Power":
            return self.convert(elements[0]) ** self.convert(elements[1])
        if name == "Sqrt":
            return sp.sqrt(self.convert(elements[0]))
        if name == "k":
            return sp.Integer(1)
        if name == "GN":
            return g
        if name == "GGS":
            return h
        if name == "WLRho":
            return rho
        if name == "Reg":
            return A_REG * (1 - z)
        if name == "Regghc":
            return B_GHOST * (1 - z)
        if name == "Q":
            order = int(getattr(elements[0], "value"))
            return self.q_functional(order, self.convert(elements[1]))
        return atom(expression)


def flow_list_ast() -> tuple[Any, ...]:
    if digest(EXTRACTED_INPUT) != EXPECTED_EXTRACTED_HASH:
        raise RuntimeError("extracted C3 source hash mismatch")
    cells = extracted_cells(EXTRACTED_INPUT.read_text(encoding="utf-8"))
    source = normalize_mathics_symbols(cells[3])
    parsed = parse(Definitions(add_builtin=False), MathicsSingleLineFeeder(source, None))
    stack = [parsed]
    while stack:
        expression = stack.pop()
        if head_name(expression) == "Set" and short_name(expression.elements[0]) == "Flow":
            rhs = expression.elements[1]
            if head_name(rhs) != "List":
                raise TypeError("Flow right-hand side is not a list")
            return tuple(rhs.elements)
        stack.extend(reversed(tuple(getattr(expression, "elements", ()))))
    raise ValueError("Flow assignment not found")


def build_linear_system() -> tuple[sp.Matrix, sp.Matrix, dict[str, object]]:
    converter = DirectThresholdConverter()
    equations = []
    started = time.monotonic()
    for index, expression in enumerate(flow_list_ast(), start=1):
        equation = sp.expand(converter.convert(expression))
        equations.append(equation)
        print(f"{MARKER}_FLOW_EQUATION_READY={index}/13", flush=True)

    matrix, rhs = sp.linear_eq_to_matrix(equations, UNKNOWNS)
    reconstruction = matrix * sp.Matrix(UNKNOWNS) - rhs
    if any(sp.expand(reconstruction[index] - equations[index]) != 0 for index in range(13)):
        raise RuntimeError("linear-system reconstruction failed")
    stats = {
        "equations": len(equations),
        "unknowns": len(UNKNOWNS),
        "q_count": converter.q_count,
        "q_orders": {str(key): value for key, value in sorted(converter.q_orders.items())},
        "q_distribution_nonzero": converter.q_distribution_nonzero,
        "q_distribution_higher_power_zeroed_by_source_rule": converter.q_distribution_higher_power,
        "q_max_regular_degree": converter.q_max_regular_degree,
        "build_seconds": time.monotonic() - started,
    }
    return matrix, rhs, stats


def numerical_solver(matrix: sp.Matrix, rhs: sp.Matrix):
    matrix_function = sp.lambdify((g, h, rho), matrix, modules="numpy", cse=True)
    rhs_function = sp.lambdify((g, h, rho), rhs, modules="numpy", cse=True)

    def solve_unknowns(g_value: float, h_value: float, rho_value: float) -> tuple[np.ndarray, float]:
        numeric_matrix = np.asarray(matrix_function(g_value, h_value, rho_value), dtype=float)
        numeric_rhs = np.asarray(rhs_function(g_value, h_value, rho_value), dtype=float).reshape(13)
        condition = float(np.linalg.cond(numeric_matrix))
        return np.linalg.solve(numeric_matrix, numeric_rhs), condition

    return solve_unknowns


def stability_data(solve_unknowns, fixed_point: np.ndarray, rho_value: float) -> tuple[np.ndarray, np.ndarray]:
    jacobian = np.zeros((2, 2), dtype=float)
    for column in range(2):
        scale = max(abs(fixed_point[column]), 1e-7 if column else 1e-5)
        step = 2e-5 * scale
        plus = fixed_point.copy()
        minus = fixed_point.copy()
        plus[column] += step
        minus[column] -= step
        beta_plus = solve_unknowns(float(plus[0]), float(plus[1]), rho_value)[0][:2]
        beta_minus = solve_unknowns(float(minus[0]), float(minus[1]), rho_value)[0][:2]
        jacobian[:, column] = (beta_plus - beta_minus) / (2 * step)
    return jacobian, -np.linalg.eigvals(jacobian)


def find_fixed_points(solve_unknowns, rho_value: float, seeds: list[tuple[float, float]]) -> list[dict[str, object]]:
    roots: list[dict[str, object]] = []

    def beta_pair(point: np.ndarray) -> np.ndarray:
        try:
            return solve_unknowns(float(point[0]), float(point[1]), rho_value)[0][:2]
        except (np.linalg.LinAlgError, ValueError, FloatingPointError):
            return np.array([1e30, 1e30])

    for seed in seeds:
        solution = root(beta_pair, np.asarray(seed, dtype=float), method="hybr", options={"maxfev": 1000})
        if not solution.success or not np.all(np.isfinite(solution.x)) or solution.x[0] <= 0:
            continue
        residual = beta_pair(solution.x)
        if np.linalg.norm(residual, ord=np.inf) > 1e-8:
            continue
        if any(np.linalg.norm(solution.x - np.asarray(entry["fixed_point"]), ord=np.inf) < 1e-7 for entry in roots):
            continue
        unknown_values, condition = solve_unknowns(float(solution.x[0]), float(solution.x[1]), rho_value)
        jacobian, exponents = stability_data(solve_unknowns, solution.x, rho_value)
        roots.append(
            {
                "seed": list(seed),
                "fixed_point": solution.x.tolist(),
                "beta_residual": residual.tolist(),
                "linear_condition_number": condition,
                "stability_matrix": jacobian.tolist(),
                "critical_exponents": [
                    {"real": float(value.real), "imag": float(value.imag)} for value in exponents
                ],
                "gamma_and_sigma_values": {
                    str(UNKNOWNS[index]): float(unknown_values[index]) for index in range(2, 13)
                },
            }
        )
    roots.sort(key=lambda entry: entry["fixed_point"][0])
    return roots


def main() -> int:
    print(f"{MARKER}_START", flush=True)
    matrix, rhs, stats = build_linear_system()
    print(f"{MARKER}_LINEAR_SYSTEM_READY", flush=True)
    solve_unknowns = numerical_solver(matrix, rhs)

    source_rho = 1 / (8 * math.pi)
    source_roots = find_fixed_points(
        solve_unknowns,
        source_rho,
        [(EXPECTED_SOURCE_G, EXPECTED_SOURCE_H), (0.2, 0.0), (0.35, 0.0), (0.6, 0.0)],
    )
    if not source_roots:
        raise RuntimeError("source-rho fixed point was not reproduced")
    source_match = min(
        source_roots,
        key=lambda entry: abs(entry["fixed_point"][0] - EXPECTED_SOURCE_G)
        + abs(entry["fixed_point"][1] - EXPECTED_SOURCE_H),
    )
    source_deviation = {
        "g": source_match["fixed_point"][0] - EXPECTED_SOURCE_G,
        "h": source_match["fixed_point"][1] - EXPECTED_SOURCE_H,
    }
    source_pass = abs(source_deviation["g"]) < 2e-6 and abs(source_deviation["h"]) < 2e-10
    print(f"{MARKER}_SOURCE_REPRODUCTION_PASS={source_pass}", flush=True)
    if not source_pass:
        raise RuntimeError(f"source reproduction failed: {source_deviation}")

    photon_rho = 1 / (4 * math.pi)
    photon_seeds = [
        (g_seed, h_seed)
        for g_seed in (0.08, 0.15, 0.25, 0.36, 0.5, 0.8, 1.2)
        for h_seed in (-1e-5, -1e-6, 0.0, 1e-6, 1e-5)
    ]
    photon_roots = find_fixed_points(solve_unknowns, photon_rho, photon_seeds)

    result = {
        "marker": MARKER,
        "source": EXTRACTED_INPUT.relative_to(ROOT).as_posix(),
        "source_sha256": digest(EXTRACTED_INPUT),
        "method": "direct structural Q_n evaluation of mechanically extracted Wolfram Flow equations",
        "litim_boundary_convention": "linear delta terms receive half endpoint weight; higher delta powers are zero per source SolveQInts rules",
        "stats": stats,
        "source_reproduction": {
            "rho": "1/(8*pi)",
            "expected_fixed_point": [EXPECTED_SOURCE_G, EXPECTED_SOURCE_H],
            "expected_critical_exponents": list(EXPECTED_SOURCE_EXPONENTS),
            "roots": source_roots,
            "matched_deviation": source_deviation,
            "pass": source_pass,
        },
        "photon_vacuum_law": {
            "rho": "1/(4*pi)",
            "roots": photon_roots,
            "root_count": len(photon_roots),
        },
    }
    OUTPUT_JSON.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"{MARKER}_PHOTON_ROOT_COUNT={len(photon_roots)}", flush=True)
    print(f"{MARKER}_OUTPUT_SHA256={digest(OUTPUT_JSON)}", flush=True)
    print(f"{MARKER}_PASS", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
