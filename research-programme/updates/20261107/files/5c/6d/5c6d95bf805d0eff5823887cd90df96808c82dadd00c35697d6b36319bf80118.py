from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import itertools
import json
import math
from pathlib import Path
import sys

import numpy as np
import psutil
import sympy as sym


ROOT = Path(__file__).resolve().parent
PREVIOUS = ROOT.parent / "tensor-ward-20261003"
sys.path.insert(0, str(PREVIOUS))
from ward_core import WardCandidate

OUTPUT = ROOT / "results/validation"


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    if OUTPUT.exists():
        raise RuntimeError("Executed evidence must not be overwritten.")
    OUTPUT.mkdir(parents=True)
    derived = json.loads((ROOT / "results/derivation/status.json").read_text(encoding="utf-8"))
    exact_checks = []
    numerical_checks = []

    def exact(name, expression):
        assert sym.factor(expression) == 0, name
        exact_checks.append({"name": name, "passed": True})

    def close(name, actual, expected, tolerance=1e-10):
        error = float(np.max(np.abs(np.asarray(actual) - np.asarray(expected))))
        scale = max(float(np.max(np.abs(actual))), float(np.max(np.abs(expected))), 1e-12)
        assert error < tolerance * scale, (name, error, scale)
        numerical_checks.append({"name": name, "relative_error": error / scale, "passed": True})

    coefficient3 = sym.symbols("cubic_time cubic_mixed")
    coefficient4 = sym.symbols("quartic_time quartic_mixed quartic_spatial")
    for count in [3, 4]:
        amplitudes = sym.symbols(f"amplitude0:{count}")
        frequencies = sym.symbols(f"frequency0:{count}")
        spatial = [sym.symbols(f"momentum{index}_0:3") for index in range(count)]
        temporal_sum = sum(amplitudes[index] * frequencies[index] for index in range(count))
        spatial_sum = [sum(amplitudes[index] * spatial[index][axis] for index in range(count)) for axis in range(3)]
        gradient_squared = sum(component**2 for component in spatial_sum)
        if count == 3:
            polynomial = coefficient3[0] * temporal_sum**3 - coefficient3[1] * temporal_sum * gradient_squared
            expected = 6 * coefficient3[0] * sym.prod(frequencies)
            expected -= 2 * coefficient3[1] * sum(
                frequencies[index] * sum(spatial[(index + 1) % 3][axis] * spatial[(index + 2) % 3][axis]
                                         for axis in range(3)) for index in range(3))
        else:
            polynomial = (-coefficient4[0] * temporal_sum**4
                          + coefficient4[1] * temporal_sum**2 * gradient_squared
                          - coefficient4[2] * gradient_squared**2)
            expected = -24 * coefficient4[0] * sym.prod(frequencies)
            for pair in itertools.combinations(range(4), 2):
                other = [index for index in range(4) if index not in pair]
                expected += 4 * coefficient4[1] * frequencies[pair[0]] * frequencies[pair[1]] * sum(
                    spatial[other[0]][axis] * spatial[other[1]][axis] for axis in range(3))
            for pairing in [((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2))]:
                expected -= 8 * coefficient4[2] * sym.prod(
                    sum(spatial[first][axis] * spatial[second][axis] for axis in range(3))
                    for first, second in pairing)
        actual = sym.Poly(sym.expand(polynomial), *amplitudes).coeff_monomial(sym.prod(amplitudes))
        exact(f"Euclidean_vertex_{count}_combinatorics", actual - expected)

    deformation, derivative_shear = sym.symbols("deformation derivative_shear")
    pressure0, pressure1, pressure2 = sym.symbols("pressure0 pressure1 pressure2")
    volume = (1 - deformation / 2)**(-1) * (1 + deformation)**sym.Rational(-1, 2)
    density = volume * (pressure0 - deformation * pressure1 * derivative_shear / 2
                        + deformation**2 * pressure2 * derivative_shear**2 / 8)
    exact("single_shear_source", sym.diff(density, deformation).subs(deformation, 0)
          + pressure1 * derivative_shear / 2)
    exact("double_shear_contact", sym.diff(density, deformation, 2).subs(deformation, 0)
          - pressure2 * derivative_shear**2 / 4 - 3 * pressure0 / 4)

    mass, chemical, amplitude = sym.symbols("mass chemical amplitude", positive=True)
    total = mass + 4 * chemical**2
    sound_squared = mass / total
    canonical_kinetic = amplitude**2 * total / mass
    dispersive_coefficient = 2 * amplitude**2 * chemical**2 / (mass**2 * canonical_kinetic)
    exact("NLO_canonical_coefficient", dispersive_coefficient - 2 * chemical**2 / (mass * total))
    exact("NLO_two_mode_dispersion_match", 2 * dispersive_coefficient * sound_squared * (1 - sound_squared)
          - 16 * chemical**4 / total**3)
    radius, cutoff, sound = sym.symbols("radius cutoff sound", positive=True)
    volume_integral = sound * 2 * sym.pi**2 * sym.integrate(radius**3, (radius, 0, cutoff)) / (2 * sym.pi)**4
    exact("acoustic_ball_measure", volume_integral - sound * cutoff**4 / (32 * sym.pi**2))
    kernel_coefficient = sym.symbols("kernel_coefficient", positive=True)
    exact("continuum_norm_Bose_normalization", kernel_coefficient * volume_integral / (2 * sound**4)
          - kernel_coefficient * cutoff**4 / (64 * sym.pi**2 * sound**3))

    sound_float = math.sqrt(5 / 23)
    coefficients = {key: item["numeric"] for key, item in derived["canonical_coefficients"].items()}
    bounds = derived["vertex_bounds"]

    def acoustic_norm(momentum):
        return math.sqrt((momentum[0] / sound_float)**2 + float(momentum[1:] @ momentum[1:]))

    def cubic_vertex(momenta):
        temporal = 6 * coefficients["cubic_time"] * np.prod([entry[0] for entry in momenta])
        mixed = sum(momenta[index][0] * float(momenta[(index + 1) % 3][1:] @ momenta[(index + 2) % 3][1:])
                    for index in range(3))
        return temporal - 2 * coefficients["cubic_mixed"] * mixed

    def quartic_vertex(momenta):
        value = -24 * coefficients["quartic_time"] * np.prod([entry[0] for entry in momenta])
        for pair in itertools.combinations(range(4), 2):
            other = [index for index in range(4) if index not in pair]
            value += 4 * coefficients["quartic_mixed"] * momenta[pair[0]][0] * momenta[pair[1]][0] * float(
                momenta[other[0]][1:] @ momenta[other[1]][1:])
        for pairing in [((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2))]:
            value -= 8 * coefficients["quartic_spatial"] * math.prod(
                float(momenta[first][1:] @ momenta[second][1:]) for first, second in pairing)
        return value

    generator = np.random.default_rng(20261003)
    vertex_rows = []
    for fixture in range(256):
        first_three = generator.normal(size=(3, 4))
        first_three[:, 0] *= sound_float
        first_three *= 10**generator.uniform(-4, 1)
        triple = [first_three[0], first_three[1], -first_three[0] - first_three[1]]
        momenta = [*first_three, -np.sum(first_three, axis=0)]
        cubic_product = math.prod(acoustic_norm(entry) for entry in triple)
        quartic_product = math.prod(acoustic_norm(entry) for entry in momenta)
        cubic_ratio = abs(cubic_vertex(triple)) / (bounds["C3"] * cubic_product)
        quartic_ratio = abs(quartic_vertex(momenta)) / (bounds["C4"] * quartic_product)
        full = quartic_vertex(momenta)
        for companion in [1, 2, 3]:
            other = [index for index in [1, 2, 3] if index != companion]
            transfer = momenta[0] + momenta[companion]
            denominator = transfer[0]**2 + float(transfer[1:] @ transfer[1:]) * sound_float**2
            assert denominator > 0
            full -= (cubic_vertex([momenta[0], momenta[companion], -transfer])
                     * cubic_vertex([momenta[other[0]], momenta[other[1]], transfer]) / denominator)
        tree_ratio = abs(full) / (bounds["C_tree"] * quartic_product)
        assert max(cubic_ratio, quartic_ratio, tree_ratio) <= 1 + 1e-12
        vertex_rows.append({"fixture": fixture, "cubic_ratio": float(cubic_ratio),
                            "quartic_ratio": float(quartic_ratio), "tree_ratio": float(tree_ratio), "passed": True})

    def matrices(model, frequency, spatial_squared):
        shifted = frequency**2 + spatial_squared
        shifted += float(model.regulator(np.asarray(shifted)))
        mixing = 2 * model.chemical * frequency
        diagonal = shifted + model.mass_squared
        schur = shifted + mixing**2 / diagonal
        return (np.array([[1., 0.], [mixing / diagonal, 1.]]),
                np.array([[1., -mixing / diagonal], [0., 1.]]),
                np.diag([diagonal, schur]))

    for regulator in [None, 4.]:
        model = WardCandidate(regulator)
        for fixture in range(24):
            external = generator.normal(size=4) * 10**generator.uniform(-2, 1)
            internal = generator.normal(size=4) * 10**generator.uniform(-2, 1)
            transfer = external - internal
            lower_p, upper_p, diagonal_p = matrices(model, external[0], float(external[1:] @ external[1:]))
            lower_k, upper_k, diagonal_k = matrices(model, internal[0], float(internal[1:] @ internal[1:]))
            propagator_k = model.propagator(internal[0], float(internal[1:] @ internal[1:]))
            propagator_q = model.propagator(transfer[0], float(transfer[1:] @ transfer[1:]))
            arbitrary = generator.normal(size=(2, 2))
            field_vertex = lower_k @ arbitrary @ upper_k
            original = model.contract((propagator_k @ field_vertex @ propagator_k)[None], propagator_q[None])[0]
            direct = np.linalg.inv(lower_p) @ original @ np.linalg.inv(upper_p)
            reduced = np.zeros((2, 2))
            for first in range(2):
                for second in range(2):
                    left = np.linalg.inv(lower_p) @ model.cubics[:, :, first] @ np.linalg.inv(upper_k) @ np.linalg.inv(diagonal_k)
                    right = np.linalg.inv(diagonal_k) @ np.linalg.inv(lower_k) @ model.cubics[:, :, second].T @ np.linalg.inv(upper_p)
                    reduced += (left @ arbitrary @ right) * propagator_q[first, second]
            close(f"arbitrary_pair_transformed_kernel_reg{regulator}_{fixture}", reduced, direct, tolerance=2e-9)
            propagated_direct = (np.linalg.inv(diagonal_p) @ direct @ np.linalg.inv(diagonal_p))
            propagated_reduced = np.linalg.inv(diagonal_p) @ reduced @ np.linalg.inv(diagonal_p)
            close(f"propagated_kernel_reg{regulator}_{fixture}", propagated_reduced, propagated_direct, tolerance=2e-9)

    stress = {
        "quadratic_gradient_shear": 5 / 23,
        "cubic_time_gradient_shear": 360 / 460**1.5,
        "quartic_time_squared_gradient_shear": (360 - 1728 / 5) / (2 * 460**2),
        "quartic_gradient_squared_gradient_shear": -360 / (2 * 460**2),
        "double_source_contact": "P_XX * (h_ij partial_i pi partial_j pi)^2 / 4 + P * tr(h^2) / 2",
        "NLO_covariant_amplitude_elimination": "-2*v(X)^2/(m(X)^2)^2 * g^{mu nu} partial_mu X partial_nu X",
        "NLO_quadratic_canonical_beta": 2 / ((10 / 9) * (46 / 9)),
        "NLO_k4_coefficient": 16 / (46 / 9)**3,
    }
    report = {
        "state": "complete", "created_at": datetime.now(timezone.utc).isoformat(),
        "exact_checks": exact_checks, "exact_check_count": len(exact_checks),
        "kernel_checks": numerical_checks, "kernel_check_count": len(numerical_checks),
        "vertex_fixtures": vertex_rows, "vertex_fixture_count": len(vertex_rows),
        "maximum_cubic_bound_ratio": max(row["cubic_ratio"] for row in vertex_rows),
        "maximum_quartic_bound_ratio": max(row["quartic_ratio"] for row in vertex_rows),
        "maximum_tree_bound_ratio": max(row["tree_ratio"] for row in vertex_rows),
        "source_and_NLO_coefficients": stress,
        "derivation_sha256": hashlib.sha256((ROOT / "results/derivation/status.json").read_bytes()).hexdigest(),
        "numeric_fixtures_prove_continuum_bound": False,
        "proof_location": "05-Ward-remainder-and-derivative-interaction-bound.md",
        "scope": "Algebraic coefficients and analytic triangle-inequality bound with finite numerical cross-checks; NLO is a derivative expansion, not a new physical higher-time-derivative mode.",
    }
    (OUTPUT / "status.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps({"state": "complete", "exact_checks": len(exact_checks), "kernel_checks": len(numerical_checks),
                      "vertex_fixtures": len(vertex_rows), "maximum_tree_ratio": report["maximum_tree_bound_ratio"],
                      "source_and_NLO": stress}))


if __name__ == "__main__":
    main()

