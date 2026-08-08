from __future__ import annotations

import hashlib
import json
import sys
import time
from pathlib import Path
from typing import Any

import numpy as np
import sympy as sp
from mathics.core.definitions import Definitions
from mathics.core.parser import MathicsSingleLineFeeder, parse
from scipy.optimize import root

from Y5_R2FR_4933_c3_flow_execution import extracted_cells


sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "functional_rg" / "4933"
EXTRACTED_INPUT = SOURCE_DIR / "RHS_general_regulator_extracted.wl"
OUTPUT_JSON = SOURCE_DIR / "photon_flow_reproduction_results.json"
MARKER = "MTS_4933_PHOTON_FLOW_REPRODUCTION"

EXPECTED_EXTRACTED_HASH = "28be0c586f31fa83a0a0b888f686b5564f6af0c4f74f5888d229aa9b58a8903c"
FP1 = np.array([0.131, 0.351, 3.327, 0.00375], dtype=float)
FP1_EXPECTED_EXPONENTS = np.array(
    [1.845 + 0j, -0.239 + 0.0155j, -0.239 - 0.0155j, -0.291 + 0j], dtype=complex
)


x = sp.Symbol("x", real=True)
g, f2sq, f4, cff = sp.symbols("g f2sq f4 cff", real=True)
beta_g, beta_euler, beta_f2sq, beta_f4, beta_cff = sp.symbols(
    "beta_g beta_euler beta_f2sq beta_f4 beta_cff"
)
gamma_g, gamma_r, gamma_s = sp.symbols("gamma_g gamma_r gamma_s")
gamma_ftrace, gamma_ftl, gamma_a, gamma_df = sp.symbols(
    "gamma_ftrace gamma_ftl gamma_a gamma_df"
)

UNKNOWNS = (
    beta_g,
    beta_euler,
    beta_f2sq,
    beta_f4,
    beta_cff,
    gamma_g,
    gamma_r,
    gamma_s,
    gamma_ftrace,
    gamma_ftl,
    gamma_a,
    gamma_df,
)

COUPLINGS = (g, f2sq, f4, cff)
CC = g / (4 * sp.pi)
ETA = (beta_g - 2 * g) / g

SYMBOLS = {
    "WLCapitalDelta": x,
    "GNewtoncoupl": g,
    "GNewtoncoupldot": beta_g,
    "CCcoupl": CC,
    "F2sqcoupl": f2sq,
    "F4coupl": f4,
    "CFFcoupl": cff,
    "WLEta": ETA,
    "WLGammag": gamma_g,
    "WLGammaR": gamma_r,
    "WLGammaS": gamma_s,
    "WLGammaWLScriptCapitalF": gamma_ftrace,
    "WLGammaFsq": gamma_ftl,
    "WLGammaa": gamma_a,
    "WLGammaDF": gamma_df,
}

INTEGRAND_NAMES = (
    "RHS1int",
    "RHSRint",
    "RHSR2int",
    "RHSS2int",
    "RHSWLGothicCapitalEint",
    "RHSWLScriptCapitalFint",
    "RHSFWLCapitalDeltaFint",
    "RHSRFFint",
    "RHSSFFint",
    "RHSWLScriptCapitalFsqint",
    "RHSF4int",
    "RHSCFFint",
)


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


class PhotonRHSConverter:
    regulator_functions = {"Ra", "Rc", "RWLPhi", "RhTL", "RhTr"}
    propagator_functions = {"Ga1", "Gc1", "GWLPhi", "GhTL", "GhTr"}

    def derivative(self, orders: tuple[int, ...], function: str) -> sp.Expr:
        if orders != (1,):
            raise ValueError(f"unsupported derivative order {orders} for {function}")
        if function in self.regulator_functions:
            return sp.Integer(-1)
        if function in self.propagator_functions:
            return sp.Integer(0)
        raise ValueError(f"unsupported derivative function {function}")

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
        if name in self.regulator_functions:
            return 1 - self.convert(elements[0])
        if name in {"Ga1", "Gc1", "GWLPhi"}:
            return sp.Integer(1)
        if name in {"GhTL", "GhTr"}:
            return 1 / (1 - 2 * CC)
        return atom(expression)


def assignment_rhs(source: str) -> tuple[str, Any]:
    parsed = parse(Definitions(add_builtin=False), MathicsSingleLineFeeder(source, None))
    stack = [parsed]
    while stack:
        expression = stack.pop()
        if head_name(expression) == "Set":
            return short_name(expression.elements[0]), expression.elements[1]
        stack.extend(reversed(tuple(getattr(expression, "elements", ()))))
    raise ValueError("assignment not found")


def integrate_litim(expression: sp.Expr) -> sp.Expr:
    cancelled = sp.cancel(expression)
    numerator, denominator = sp.fraction(cancelled)
    denominator = sp.factor(denominator)
    if denominator.has(x):
        cancelled = sp.cancel(sp.together(cancelled))
        numerator, denominator = sp.fraction(cancelled)
        denominator = sp.factor(denominator)
    if denominator.has(x):
        raise ValueError(f"nonconstant Litim denominator: {denominator}")
    polynomial = sp.Poly(sp.expand(numerator), x)
    integral = sp.Add(
        *(coefficient / (power[0] + 1) for power, coefficient in polynomial.terms())
    )
    return sp.factor(integral / denominator)


def photon_rhs() -> dict[str, sp.Expr]:
    if digest(EXTRACTED_INPUT) != EXPECTED_EXTRACTED_HASH:
        raise RuntimeError("photon RHS extraction hash mismatch")
    cells = extracted_cells(EXTRACTED_INPUT.read_text(encoding="utf-8"))
    converter = PhotonRHSConverter()
    assignments: dict[str, sp.Expr] = {}
    for index in range(4, 19):
        name, rhs_ast = assignment_rhs(cells[index])
        assignments[name] = sp.expand(converter.convert(rhs_ast))
    for name in INTEGRAND_NAMES:
        assignments[name.removesuffix("int")] = integrate_litim(assignments[name])
    assignments["RHSR2"] += assignments["RHSR2const"]
    assignments["RHSS2"] += assignments["RHSS2const"]
    assignments["RHSWLGothicCapitalE"] += assignments["RHSWLGothicCapitalEconst"]
    return assignments


def lhs_projections() -> tuple[sp.Expr, ...]:
    vacuum = 1 / (32 * sp.pi**2)
    return (
        vacuum * (4 + 2 * gamma_g),
        (beta_g - (2 + gamma_g) * g) / (16 * sp.pi * g**2) + gamma_r / (16 * sp.pi**2),
        -gamma_r / (16 * sp.pi * g),
        gamma_s / (16 * sp.pi * g),
        beta_euler,
        2 * gamma_a + gamma_ftrace / (16 * sp.pi**2),
        2 * gamma_df,
        -gamma_ftrace / (16 * sp.pi * g) + 2 * gamma_df / 3,
        gamma_ftl / (16 * sp.pi * g) + gamma_s / 2,
        beta_f2sq - 4 * f2sq + (4 * gamma_a - 2 * gamma_g) * f2sq - 2 * gamma_ftl,
        beta_f4 - 4 * f4 + (4 * gamma_a - 2 * gamma_g) * f4 + 2 * gamma_ftl,
        beta_cff - 2 * cff + (2 * gamma_a - gamma_g) * cff - gamma_df / 2,
    )


def build_system() -> tuple[sp.Matrix, sp.Matrix, dict[str, object]]:
    started = time.monotonic()
    rhs = photon_rhs()
    rhs_order = (
        rhs["RHS1"],
        rhs["RHSR"],
        rhs["RHSR2"],
        rhs["RHSS2"],
        rhs["RHSWLGothicCapitalE"],
        rhs["RHSWLScriptCapitalF"],
        rhs["RHSFWLCapitalDeltaF"],
        rhs["RHSRFF"],
        rhs["RHSSFF"],
        rhs["RHSWLScriptCapitalFsq"],
        rhs["RHSF4"],
        rhs["RHSCFF"],
    )
    equations = tuple(sp.expand(lhs - right) for lhs, right in zip(lhs_projections(), rhs_order))
    matrix, vector = sp.linear_eq_to_matrix(equations, UNKNOWNS)
    reconstruction = matrix * sp.Matrix(UNKNOWNS) - vector
    if any(sp.expand(reconstruction[index] - equations[index]) != 0 for index in range(12)):
        raise RuntimeError("photon linear-system reconstruction failed")
    return matrix, vector, {"build_seconds": time.monotonic() - started, "equations": 12, "unknowns": 12}


def numerical_solver(matrix: sp.Matrix, vector: sp.Matrix):
    matrix_function = sp.lambdify(COUPLINGS, matrix, modules="numpy", cse=True)
    vector_function = sp.lambdify(COUPLINGS, vector, modules="numpy", cse=True)

    def solve(point: np.ndarray) -> tuple[np.ndarray, float]:
        values = tuple(float(value) for value in point)
        numeric_matrix = np.asarray(matrix_function(*values), dtype=float)
        numeric_vector = np.asarray(vector_function(*values), dtype=float).reshape(12)
        return np.linalg.solve(numeric_matrix, numeric_vector), float(np.linalg.cond(numeric_matrix))

    return solve


def beta_coordinates(unknown_values: np.ndarray) -> np.ndarray:
    return np.array(
        [
            unknown_values[0],
            (unknown_values[2] + unknown_values[3]) / 2,
            (unknown_values[2] - unknown_values[3]) / 2,
            unknown_values[4],
        ],
        dtype=float,
    )


def essential_to_raw(point: np.ndarray) -> np.ndarray:
    return np.array([point[0], point[1] + point[2], point[1] - point[2], point[3]], dtype=float)


def stability(solve_essential, point: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    jacobian = np.zeros((4, 4), dtype=float)
    for column in range(4):
        scale = max(abs(point[column]), 1e-5)
        step = 2e-5 * scale
        plus = point.copy()
        minus = point.copy()
        plus[column] += step
        minus[column] -= step
        jacobian[:, column] = (beta_coordinates(solve_essential(plus)[0]) - beta_coordinates(solve_essential(minus)[0])) / (2 * step)
    return jacobian, -np.linalg.eigvals(jacobian)


def main() -> int:
    print(f"{MARKER}_START", flush=True)
    matrix, vector, stats = build_system()
    print(f"{MARKER}_SYSTEM_READY", flush=True)
    solve_raw = numerical_solver(matrix, vector)

    def solve(point: np.ndarray) -> tuple[np.ndarray, float]:
        return solve_raw(essential_to_raw(point))

    fp1_unknowns, fp1_condition = solve(FP1)
    fp1_beta = beta_coordinates(fp1_unknowns)
    fp1_jacobian, fp1_local_exponents = stability(solve, FP1)
    fp1_newton_correction = np.linalg.solve(fp1_jacobian, -fp1_beta)
    print(f"{MARKER}_TABLE_FP1_BETA={fp1_beta.tolist()}", flush=True)

    def beta(point: np.ndarray) -> np.ndarray:
        try:
            return beta_coordinates(solve(point)[0])
        except (np.linalg.LinAlgError, ValueError, FloatingPointError):
            return np.full(4, 1e30)

    solution = root(beta, FP1, method="hybr", options={"maxfev": 3000, "xtol": 1e-11})
    fixed_point = solution.x
    residual = beta(fixed_point)
    jacobian, exponents = stability(solve, fixed_point)
    unknown_values, condition = solve(fixed_point)

    result = {
        "marker": MARKER,
        "source": EXTRACTED_INPUT.relative_to(ROOT).as_posix(),
        "source_sha256": digest(EXTRACTED_INPUT),
        "scheme": "natural endomorphism, harmonic gauges, Litim regulator, lambda=g/(4*pi)",
        "lhs_basis": ["1", "R", "R2", "S2", "Euler", "F2", "FDeltaF", "RFF", "SFF", "F2sq", "F4", "CFF"],
        "stats": stats,
        "published_fp1": {
            "coordinates": FP1.tolist(),
            "raw_coordinates_g_f2sq_f4_cff": essential_to_raw(FP1).tolist(),
            "beta_from_reconstructed_system": fp1_beta.tolist(),
            "beta_infinity_norm": float(np.linalg.norm(fp1_beta, ord=np.inf)),
            "linear_condition_number": fp1_condition,
            "local_stability_matrix": fp1_jacobian.tolist(),
            "local_critical_exponents": [
                {"real": float(value.real), "imag": float(value.imag)}
                for value in fp1_local_exponents
            ],
            "newton_correction": fp1_newton_correction.tolist(),
            "unknown_values": {
                str(UNKNOWNS[index]): float(fp1_unknowns[index]) for index in range(12)
            },
        },
        "reconstructed_root": {
            "success": bool(solution.success),
            "message": str(solution.message),
            "coordinates": fixed_point.tolist(),
            "beta_residual": residual.tolist(),
            "distance_from_published_fp1": (fixed_point - FP1).tolist(),
            "linear_condition_number": condition,
            "stability_matrix": jacobian.tolist(),
            "critical_exponents": [
                {"real": float(value.real), "imag": float(value.imag)} for value in exponents
            ],
            "unknown_values": {str(UNKNOWNS[index]): float(unknown_values[index]) for index in range(12)},
        },
        "published_critical_exponents": [
            {"real": float(value.real), "imag": float(value.imag)} for value in FP1_EXPECTED_EXPONENTS
        ],
    }
    OUTPUT_JSON.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"{MARKER}_OUTPUT_SHA256={digest(OUTPUT_JSON)}", flush=True)
    print(f"{MARKER}_PASS", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
