from common import *
import numpy as np
import sympy as sp


def symbolic():
    ratio, frequency = sp.symbols("q u", positive=True)
    scale = (1 + ratio**2)**sp.Rational(1, 4)
    rate = -ratio**2 / (2 * (1 + ratio**2))
    transform = sp.diag(scale, 1 / scale)
    original = sp.Matrix([[sp.Rational(3, 2), frequency], [-frequency * (1 + ratio**2), -sp.Rational(3, 2)]])
    transformed = sp.simplify(transform * original * transform.inv() + sp.diag(rate, -rate))
    growth = 1 + 1 / (2 * (1 + ratio**2))
    full_frequency = frequency * sp.sqrt(1 + ratio**2)
    expected = sp.Matrix([[growth, full_frequency], [-full_frequency, -growth]])
    mu = sp.symbols("mu", real=True)
    rotation = sp.Matrix([[0, -mu], [mu, 0]])
    checks = dict(full_frequency_generator=sp.simplify(transformed - expected),
                  determinant=sp.simplify(transform.det() - 1),
                  symmetric_generator=sp.simplify((transformed + transformed.T) / 2 - sp.diag(growth, -growth)),
                  carrier_symmetric=sp.simplify(rotation + rotation.T),
                  scale_rate=sp.simplify(-ratio * sp.diff(scale, ratio) / scale - rate))
    require(all(value == sp.zeros(2) if isinstance(value, sp.MatrixBase) else value == 0 for value in checks.values()), "full-frequency energy identities")
    return {key: str(value) for key, value in checks.items()}


def main():
    modest()
    check_parent()
    require(LABEL == "summary", "energy audit destination")
    destination = STAGE / "energy"
    destination.mkdir(exist_ok=True)
    write(destination / "inputs.json", dict(sources=frozen_sources(), numerical=GATE, algebra=ALGEBRA,
          new_ode_solves=0, constant_parent_scalar_mass=True, physical_outputs_unchanged=True))
    write(destination / "symbolic.json", symbolic())
    rows, checks, inputs = [], [], {}
    for family in ("half", "balanced", "double"):
        phase_path = STAGE / family / "phase-cancellation.json"
        phase = read(phase_path)
        require(phase["passed"], "qualified exact source equation")
        inputs[str(phase_path)] = digest(phase_path)
        errors = []
        growths, conditions = [], []
        for point in phase["rows"]:
            frequency, gamma = point["physical_omega_over_H"], point["gamma"]
            require(frequency > 0 and gamma >= 0, "positive parent oscillator")
            ratio_square = 2 * gamma / frequency
            scale = (1 + ratio_square)**.25
            rate = -ratio_square / (2 * (1 + ratio_square))
            transform = np.diag([scale, 1 / scale])
            inverse = np.diag([1 / scale, scale])
            original = np.array([[1.5, frequency], [-frequency - 2 * gamma, -1.5]])
            actual = transform @ original @ inverse + np.diag([rate, -rate])
            growth = 1 + .5 / (1 + ratio_square)
            expected_frequency = frequency * np.sqrt(1 + ratio_square)
            expected = np.array([[growth, expected_frequency], [-expected_frequency, -growth]])
            generator_error = float(np.max(abs(actual - expected))) / max(float(np.max(abs(expected))), 1e-80)
            symmetric_error = float(np.max(abs((actual + actual.T) / 2 - np.diag([growth, -growth]))))
            errors.append((generator_error, symmetric_error))
            require(1 <= growth <= 1.5, "analytic growth range")
            for angle in (0., .37, 1.1):
                direction = np.array([np.cos(angle), np.sin(angle)])
                quadratic = float(direction @ actual @ direction)
                require(quadratic <= growth + ALGEBRA, "homogeneous energy bound")
            growths.append(growth)
            conditions.append(scale**2)
        maximum = np.max(np.array(errors), axis=0)
        passed = bool(np.max(maximum) < ALGEBRA)
        checks.append(dict(name=family + ":full-frequency-energy", passed=passed, generator_error=float(maximum[0]), symmetric_error=float(maximum[1])))
        rows.append(dict(family=family, samples=len(growths), growth_range=[min(growths), max(growths)],
                         transform_condition_range=[min(conditions), max(conditions)], errors=checks[-1]))
    for path, expected in read(destination / "inputs.json")["sources"].items():
        require(digest(path) == expected, "frozen energy source")
    check_parent()
    passed = all(row["passed"] for row in checks)
    write(destination / "result.json", dict(passed=passed, reports=rows, checks=checks, input_hashes=inputs,
          new_ode_solves=0, exact_growth_bound=1.5, isolated_block_with_external_metric_input=True,
          full_feedback_bound_closed=False, same_physical_solution=True))
    print("full-frequency energy", sum(row["samples"] for row in rows), "native coefficient samples", "passed", passed, flush=True)
    require(passed, "inspect energy identity failure")


if __name__ == "__main__":
    main()

