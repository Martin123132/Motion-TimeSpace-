from common import *
from adjoint_operator import open_owned, relative, sup
from primitive_math import MetricPrimitive
import numpy as np
import sympy as sp


def symbolic_checks():
    mu, omega_h, gamma, velocity, velocity_rate, ratio, direction, drive, expansion, mixing = sp.symbols("mu omega_h gamma v vn rho c b z Y", real=True)
    phase_direction = direction * velocity
    internal = sp.I * (mu - omega_h - gamma) * phase_direction - (sp.Rational(3, 2) - sp.I * gamma) * phase_direction
    derivative = direction * (velocity_rate + (sp.Rational(1, 2) + sp.I * mu - ratio) * velocity)
    residual = derivative - internal + drive * (mixing - expansion)
    reduced = direction * (velocity_rate + (2 + sp.I * omega_h - ratio) * velocity) + drive * (mixing - expansion)
    rotation = sp.Matrix([[0, -mu], [mu, 0]])
    answers = dict(full_residual=sp.simplify(residual - reduced), carrier_rate=sp.simplify(sp.diff(residual, mu)),
                   gradient_gamma=sp.simplify(sp.diff(residual, gamma)),
                   skew_log_norm=sp.simplify(rotation + rotation.T))
    require(all(value == 0 if not isinstance(value, sp.MatrixBase) else value == sp.zeros(2) for value in answers.values()), "exact phase cancellation")
    return {key: str(value) for key, value in answers.items()}


def native_phase_probe():
    (ROOT / "phase-contexts").mkdir(exist_ok=False)
    system = open_owned("heavy", "phase-contexts")
    reference = load(POISSON / "evolution/heavy-gr.npz")
    primitive = MetricPrimitive(system, reference)
    grid = reference["efold"]
    indices = np.unique(np.linspace(2, len(grid) - 4, 97, dtype=int))
    rows = []
    internal_errors, cancellation_errors, conjugacy_errors = [], [], []
    actual_all, expected_all, internal_all = [], [], []
    for index in indices:
        guard()
        efold = float(grid[index] + .43 * (grid[index + 1] - grid[index]))
        vector, rate, denominator = primitive.vector(efold, 1.)
        full = np.zeros(len(system.units))
        full[:len(vector)] = vector
        derivative, values, rates, info, _, _ = system.evaluate(efold, full * system.units, "poisson-spatial")
        point = system.context["point"](efold)
        scale, hubble = point[10], point[12]
        velocity, velocity_rate = point[3], point[8]
        phase, mu = system.owner.phase(efold)
        omega = scale * system.background["masses"][1]
        gamma = system.wave**2 / (2 * omega * hubble)
        ratio = 3 * float(primitive.quadrature(efold, 1)) / (2 * system.wave**2 * denominator)
        coefficient = -3j * scale * np.exp(1j * phase) / (denominator * np.sqrt(omega))
        drive = -1j * scale * system.wave * velocity * np.exp(1j * phase) / (hubble * np.sqrt(omega))
        gravity = 3 * hubble * info["enthalpy"] / (2 * system.wave**2)
        mixing = -3 * (hubble + gravity) / (system.wave * denominator)
        value = complex(*(vector[system.slots] * system.units[system.slots]))
        value_rate = complex(*(rate[system.slots] * system.units[system.slots]))
        actual_operator = complex(*derivative[system.slots])
        internal = 1j * (mu - omega / hubble - gamma) * value + (1.5 - 1j * gamma) * np.exp(2j * phase) * value.conjugate()
        internal_expected = internal + drive * info["z"]
        actual = value_rate - actual_operator + drive * mixing
        expected = coefficient * (velocity_rate + (2 + 1j * omega / hubble - ratio) * velocity) + drive * (mixing - info["z"])
        actual_all.append(actual)
        expected_all.append(expected)
        internal_all.append(internal_expected)
        internal_errors.append(actual_operator - internal_expected)
        cancellation_errors.append(actual - expected)
        conjugacy_errors.append(np.exp(2j * phase) * value.conjugate() + value)
        rows.append(dict(efold=efold, mu=float(mu), gamma=float(gamma), physical_omega_over_H=float(omega / hubble),
                         actual=[actual.real, actual.imag], reduced=[expected.real, expected.imag]))
    errors = dict(native_internal_equation=relative(internal_errors, internal_all),
                  phase_gradient_cancellation=relative(cancellation_errors, actual_all),
                  phase_direction_conjugacy=relative(conjugacy_errors, actual_all))
    passed = max(errors.values()) < ALGEBRA
    report = dict(passed=passed, errors=errors, samples=len(rows), rows=rows,
                  artificial_mu_and_explicit_gamma_cancel=True, physical_omega_removed=False,
                  background_velocity_derivative_retained=True, native_model_unchanged=True)
    write(ROOT / "phase-cancellation.json", report)
    require(passed, "inspect native phase cancellation discrepancy")
    return report

