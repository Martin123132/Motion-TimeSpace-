from common import *
from corrector_v2 import *
from coefficients import calculate
from canonical_math import transform
import numpy as np
from scipy.interpolate import CubicSpline


def main():
    modest()
    check_parent()
    write(ROOT / "frozen-inputs.json", dict(sources={str(path): digest(path) for path in STAGE.iterdir()
                                               if path.suffix in (".py", ".ps1", ".md")}, numerical=GATE, algebra=ALGEBRA,
          physical_grid="retained original heavy " + LABEL, future_perturbation_sources=False,
          finite_difference_steps=[1e-6, 5e-7]))
    context, system, units, support, vectors, wave = initialize("contexts")
    provider = Background("heavy")
    grid = provider.efold
    require(np.array_equal(grid, system.background["efold"]), "background grid")
    exact_packet = load(TIMECHAIN / "operators" / (LABEL + ".npz"))
    require(np.array_equal(exact_packet["efold"], grid), "retained exact-map grid")
    pieces = []
    for first in range(0, len(grid), 256):
        guard()
        pieces.append(factors(provider, system, support, grid[first:first + 256], wave))
        if first % 2048 == 0:
            print("Coupled factors", first, "/", len(grid), flush=True)
    tables = {name: np.concatenate([piece[name] for piece in pieces]) for name in pieces[0]}
    del pieces
    packet = dict(efold=grid, wave=wave, support=support, vectors=vectors, units=units,
                  transform=exact_packet["transform"] * exact_packet["balance"][:, :, None] / exact_packet["balance"][:, None, :], **tables)
    np.savez_compressed(ROOT / "coupled-factors.npz", **packet)
    write(ROOT / "exact-map-input.json", dict(path=str(TIMECHAIN / "operators" / (LABEL + ".npz")), sha256=digest(TIMECHAIN / "operators" / (LABEL + ".npz"))))
    mapping = HigherOrderCorrector(packet)
    indices = np.unique(np.linspace(1, len(grid) - 3, 97, dtype=int))
    points = grid[indices] + .43 * (grid[indices + 1] - grid[indices])
    direct = factors(provider, system, support, points, wave)
    checks = {}
    for name in mapping.splines:
        predicted = mapping.splines[name](points)
        denominator = max(np.max(abs(balanced_block(direct[name], name, units, support, vectors))), 1e-80)
        checks["value_" + name] = float(np.max(abs(balanced_block(predicted - direct[name], name, units, support, vectors))) / denominator)
    derivatives = {}
    for step in (1e-6, 5e-7):
        data = {offset: factors(provider, system, support, points + offset * step, wave) for offset in (-2, -1, 1, 2)}
        derivatives[step] = {name: (data[-2][name] - 8 * data[-1][name] + 8 * data[1][name] - data[2][name]) / (12 * step)
                             for name in ("U_A", "U_B", "U_C")}
    keep = np.unique(np.r_[np.arange(0, len(grid), 2), len(grid) - 1])
    for name in ("U_A", "U_B", "U_C"):
        fine = mapping.splines[name](points, 1)
        coarse = make_interp_spline(grid[keep], tables[name][keep], k=5, axis=0)(points, 1)
        reference = derivatives[5e-7][name]
        denominator = max(np.max(abs(balanced_block(reference, name, units, support, vectors))), 1e-80)
        for label, difference in (("derivative", fine - reference), ("fd_refinement", derivatives[1e-6][name] - reference),
                                  ("grid_derivative", fine - coarse)):
            checks[label + "_" + name] = float(np.max(abs(balanced_block(difference, name, units, support, vectors))) / denominator)
    reference_mean = calculate(provider, points, wave)
    for name in ("hessian", "source", "feedback"):
        fine_mean = CubicSpline(grid, tables[name], axis=0)(points)
        coarse_mean = CubicSpline(grid[keep], tables[name][keep], axis=0)(points)
        balance = reference_mean["units"]
        if name == "hessian":
            scaling = balance[:, :, None] * balance[:, None, :]
        elif name == "source":
            scaling = balance[:, :, None] / balance[:, None, :]
        else:
            scaling = balance[:, None, :]
        denominator = max(float(np.max(abs(reference_mean[name] * scaling))), 1e-80)
        checks["mean_value_" + name] = float(np.max(abs((fine_mean - reference_mean[name]) * scaling)) / denominator)
        checks["mean_grid_" + name] = float(np.max(abs((fine_mean - coarse_mean) * scaling)) / denominator)
    algebra = {}
    max_inverse_error = 0.
    max_source_error = 0.
    max_full_operator_error = 0.
    random = np.random.default_rng(20261107)
    exact_background = provider.evaluate(points)
    exact = transform(exact_background, wave, include_fast=False)
    for index, efold in enumerate(points):
        guard()
        vector = random.normal(size=len(units)) * units
        blocks = tuple(direct["U_" + suffix][index] for suffix in ("A", "B", "C"))
        reconstructed = inverse(blocks, vector + apply(blocks, vector, support, vectors), support, vectors)
        max_inverse_error = max(max_inverse_error, float(np.max(abs((reconstructed - vector) / units)) / max(np.max(abs(vector / units)), 1e-80)))
        internal, linear, _, _ = system.source_only(float(efold), vector[8:])
        expected_linear = np.zeros(8)
        expected_linear[[4, 6]] = direct["linear"][index] @ vector[8:][support]
        max_source_error = max(max_source_error, float(np.max(abs(linear - expected_linear)) / max(np.max(abs(linear)), 1e-80)))
        coefficients = calculate(provider, np.array([efold]), wave)
        full_state = coefficients["transform"][0] @ vector[:8]
        state_rate, rest_rate = system.full_rhs(float(efold), full_state, vector[8:])
        balance = exact["balance"][index]
        transform_rate = exact["rate"][index] * balance[:, None] / balance[None, :]
        normal_rate = np.linalg.solve(coefficients["transform"][0], state_rate - transform_rate @ vector[:8])
        mean_state_rate = JFULL @ (coefficients["hessian"][0] @ vector[:8] + coefficients["source"][0] @ linear)
        mean_rest_native = internal + (vectors[:system.native_rest_size] @ (coefficients["feedback"][0] @ vector[:8])) / context["point"](float(efold))[12]
        mean_rest = system.extend_tail(float(efold), vector[8:], mean_rest_native)
        oscillating = tuple(direct["V_" + suffix][index] for suffix in ("A", "B", "C"))
        approximate = np.r_[mean_state_rate, mean_rest] + apply(oscillating, vector, support, vectors)
        original = np.r_[normal_rate, rest_rate]
        max_full_operator_error = max(max_full_operator_error, float(np.max(abs((approximate - original) / units)) / max(np.max(abs(original / units)), 1e-80)))
    algebra["inverse_roundtrip"] = max_inverse_error
    algebra["source_support"] = max_source_error
    checks["order2_full_operator"] = max_full_operator_error
    norms = np.array([infinity_norm(tuple(tables["U_" + suffix][index] for suffix in ("A", "B", "C")), units, support, vectors)
                      for index in range(len(grid))])
    check_parent()
    np.savez_compressed(ROOT / "representation-checks.npz", points=points, primitive_norm=norms,
                        **{"derivative_" + name: value for name, value in derivatives[5e-7].items()})
    passed = all(np.isfinite(value) and value < GATE for value in checks.values()) and all(value < ALGEBRA for value in algebra.values()) and float(np.max(norms)) < 1
    write(ROOT / "assembly-result.json", dict(passed=bool(passed), checks=checks, algebra=algebra,
          maximum_native_normalized_U=float(np.max(norms)),
          sampled_neumann_inverse_bound=float(1 / (1 - np.max(norms))) if np.max(norms) < 1 else None,
          inverse_bound_scope="original physical nodes only; not a continuous interval certificate",
          label=LABEL, wave=wave, native_signature=system.signature.tolist(), interpolation_order=5,
          points=len(grid), independent_probes=len(points), numerical=GATE, algebra_gate=ALGEBRA,
          packet_sha256=digest(ROOT / "coupled-factors.npz"), prospective_forward_started=False))
    print("Assembly checks", checks, algebra, "U norm", float(np.max(norms)), "passed", passed, flush=True)
    require(passed, "representation or inverse failed; preserve and inspect before forward")


if __name__ == "__main__":
    main()

