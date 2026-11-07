import sympy as sp
from common import ROOT, write, require


def identities():
    checks = {}

    def verify(name, value):
        if isinstance(value, sp.MatrixBase):
            good = all(sp.simplify(entry) == 0 for entry in value)
        else:
            good = sp.simplify(value) == 0
        checks[name] = bool(good)
        require(good, "symbolic identity: " + name)

    epsilon, scale, mass, alpha, trace, trace_square = sp.symbols("epsilon scale mass alpha trace trace_square", real=True)
    field, velocity, delta, speed, gradient_square, shift_gradient = sp.symbols(
        "field velocity delta speed gradient_square shift_gradient", real=True)
    volume = 1 + epsilon * trace / 2 + epsilon**2 * (trace**2 / 8 - trace_square / 4)
    kinetic = scale**2 * volume * (velocity + epsilon * speed - epsilon**2 * shift_gradient)**2 / (2 * (1 + epsilon * alpha))
    potential = -scale**4 * mass**2 * volume * (1 + epsilon * alpha) * (field + epsilon * delta)**2 / 2
    gradient = -scale**2 * epsilon**2 * gradient_square / 2
    expanded = sp.expand(sp.series(kinetic + potential + gradient, epsilon, 0, 3).removeO()).coeff(epsilon, 2)
    omega = scale * mass
    metric_only = scale**2 / 2 * (
        velocity**2 * alpha**2 - alpha * trace * (velocity**2 + omega**2 * field**2) / 2
        + (trace**2 / 8 - trace_square / 4) * (velocity**2 - omega**2 * field**2))
    proposed = scale**2 / 2 * (speed**2 - gradient_square - omega**2 * delta**2) + scale**2 * (
        (trace / 2 - alpha) * velocity * speed - (trace / 2 + alpha) * omega**2 * field * delta
        - velocity * shift_gradient) + metric_only
    verify("ADM quadratic expansion with metric-only terms", expanded - proposed)
    zero_metric = {alpha: 0, trace: 0, trace_square: 0, shift_gradient: 0}
    density = velocity * speed + omega**2 * field * delta
    pressure = velocity * speed - omega**2 * field * delta
    verify("lapse variation gives density", sp.diff(expanded, alpha).subs(zero_metric) + scale**2 * density)
    verify("trace variation gives pressure", sp.diff(expanded, trace).subs(zero_metric) - scale**2 * pressure / 2)
    verify("shift variation gives gradient current", sp.diff(expanded, shift_gradient) + scale**2 * velocity)
    verify("scalar momentum before boundary shift", sp.diff(expanded, speed) - scale**2 * (speed + (trace / 2 - alpha) * velocity))

    hubble, trace_tau, velocity_tau, speed_tau, wave = sp.symbols("hubble trace_tau velocity_tau speed_tau wave", real=True)
    background_residual = velocity_tau + 2 * hubble * velocity + omega**2 * field
    boundary_rate = scale**2 / 2 * (2 * hubble * trace * velocity * delta
                                  + trace_tau * velocity * delta + trace * velocity_tau * delta + trace * velocity * speed)
    mixed = scale**2 * trace * pressure / 2
    verify("synchronous boundary with off-shell background", mixed - boundary_rate
           + scale**2 * velocity * delta * trace_tau / 2 + scale**2 * trace * delta * background_residual / 2)
    momentum_rate = scale**2 * (speed_tau + 2 * hubble * speed + trace_tau * velocity / 2
                              + trace * velocity_tau / 2 + hubble * trace * velocity)
    delta_variation = -scale**2 * (wave**2 + omega**2) * delta - scale**2 * trace * omega**2 * field / 2
    verify("scalar Euler equation including background residual", momentum_rate - delta_variation
           - scale**2 * (speed_tau + 2 * hubble * speed + (wave**2 + omega**2) * delta
                         + velocity * trace_tau / 2 + trace * background_residual / 2))

    phase, carrier_rate = sp.symbols("phase carrier_rate", real=True)
    carrier_scale = sp.symbols("carrier_scale", positive=True)
    symplectic = sp.Matrix([[0, 1], [-1, 0]])
    rotation = sp.Matrix([[sp.cos(phase), sp.sin(phase)], [-sp.sin(phase), sp.cos(phase)]])
    transform = sp.diag(1 / carrier_scale, carrier_scale) * rotation
    transform_rate = sp.diag(-sp.Rational(3, 2), sp.Rational(3, 2)) * transform + carrier_rate * transform * symplectic
    verify("canonical carrier two-form", transform.T * symplectic * transform - symplectic)
    connection = transform.T * symplectic * transform_rate
    verify("carrier Hamiltonian connection symmetric", connection - connection.T)

    inverse = sp.Matrix(2, 2, sp.symbols("inverse00 inverse01 inverse10 inverse11", real=True))
    spectator = sp.Matrix(2, 2, sp.symbols("spectator00 spectator01 spectator10 spectator11", real=True))
    combined = inverse.row_join(inverse * spectator)
    expected = inverse.det() * symplectic
    verify("second-coordinate area factor", inverse.T * symplectic * inverse - expected)
    block = combined.T * symplectic * combined
    verify("spectator cross block", block[:2, 2:] - expected * spectator)
    verify("spectator self block", block[2:, 2:] - spectator.T * expected * spectator)

    metric_z, field_error, velocity_error, delta_defect, speed_defect = sp.symbols(
        "metric_z field_error velocity_error delta_defect speed_defect", real=True)
    actual_field_rate = velocity + field_error
    actual_velocity_rate = -2 * hubble * velocity - omega**2 * field + velocity_error
    actual_delta_rate = speed + hubble * delta_defect
    actual_speed_rate = -2 * hubble * speed - (wave**2 + omega**2) * delta - wave * metric_z * velocity + hubble * speed_defect
    density_rate = (actual_velocity_rate * speed + velocity * actual_speed_rate
                    + omega**2 * (2 * hubble * field * delta + actual_field_rate * delta + field * actual_delta_rate))
    flux = wave * velocity * delta
    flux_rate = wave * (actual_velocity_rate * delta + velocity * actual_delta_rate)
    verify("off-shell scalar continuity identity", density_rate + hubble * (density + 3 * pressure) + wave * flux
           + wave * metric_z * velocity**2 - velocity_error * speed - omega**2 * field_error * delta
           - hubble * (velocity * speed_defect + omega**2 * field * delta_defect))
    verify("off-shell scalar momentum identity", flux_rate + 2 * hubble * flux - wave * pressure
           - wave * velocity_error * delta - hubble * wave * velocity * delta_defect)
    true_density = actual_field_rate * actual_delta_rate + omega**2 * field * delta
    verify("covariant versus phase-space density", true_density - density - field_error * speed
           - hubble * (velocity + field_error) * delta_defect)
    verify("boundary metric momentum retained", sp.diff(-scale**2 * velocity * delta * trace_tau / 2, trace_tau)
           + scale**2 * velocity * delta / 2)
    return checks


if __name__ == "__main__":
    result = identities()
    write(ROOT / "symbolic-result.json", dict(passed=all(result.values()), identities=result))

