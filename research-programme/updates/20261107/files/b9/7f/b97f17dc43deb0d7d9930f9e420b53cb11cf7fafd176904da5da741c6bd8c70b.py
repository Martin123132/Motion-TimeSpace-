import sympy as sp
from common import require


def identities():
    checks = {}

    def check(name, value):
        passed = all(sp.simplify(entry) == 0 for entry in value) if isinstance(value, sp.MatrixBase) else sp.simplify(value) == 0
        require(passed, name)
        checks[name] = bool(passed)

    scale, hubble, hubble_tau, wave = sp.symbols("scale hubble hubble_tau wave", nonzero=True, real=True)
    trace, eta, trace_tau, eta_tau = sp.symbols("trace eta trace_tau eta_tau", real=True)
    metric = sp.diag(-2 * eta, -2 * eta, trace + 4 * eta)
    metric_rate = sp.diag(-2 * eta_tau, -2 * eta_tau, trace_tau + 4 * eta_tau)
    volume2 = trace**2 / 8 - sp.trace(metric * metric) / 4
    spatial = wave**2 * (-sp.trace(metric * metric) / 8 + trace**2 / 8
                        + (trace + 4 * eta)**2 / 4 - (trace + 4 * eta) * trace / 4)
    check("ADM scalar spatial curvature", spatial - wave**2 * eta**2)
    kinetic = (sp.trace(metric_rate * metric_rate) - trace_tau**2) / 8
    check("ADM scalar metric kinetic block", kinetic - trace_tau * eta_tau - 3 * eta_tau**2)
    boundary_shape = -trace**2 / 4 + sp.trace(metric * metric) / 2
    boundary_rate = scale**2 * (hubble_tau + 2 * hubble**2) * boundary_shape + scale**2 * hubble * (
        -trace * trace_tau / 2 + sp.trace(metric * metric_rate))
    raw = scale**2 * (-3 * hubble**2 * volume2 - hubble * trace * trace_tau / 2
                     + hubble * sp.trace(metric * metric_rate) + kinetic + spatial)
    remaining = scale**2 * (kinetic + spatial + (2 * hubble_tau + hubble**2) * volume2)
    check("gravity boundary and background contact", raw - boundary_rate - remaining)

    slow_delta, heavy_delta, slow_pi, heavy_pi, momentum_h, momentum_eta = sp.symbols(
        "slow_delta heavy_delta slow_pi heavy_pi momentum_h momentum_eta", real=True)
    slow_field, heavy_field, slow_velocity, heavy_velocity, slow_rate, heavy_rate, slow_omega, heavy_omega = sp.symbols(
        "slow_field heavy_field slow_velocity heavy_velocity slow_rate heavy_rate slow_omega heavy_omega", real=True)
    source = slow_velocity * slow_delta + heavy_velocity * heavy_delta
    geometry = momentum_eta - 6 * momentum_h
    old_slow_pi = slow_pi + scale**2 * trace * slow_velocity / 2
    old_heavy_pi = heavy_pi + scale**2 * trace * heavy_velocity / 2
    old_h = momentum_h + scale**2 * source / 2
    old = (old_h * momentum_eta - 3 * old_h**2) / scale**2 - scale**2 * wave**2 * eta**2
    for delta, momentum, field, velocity, omega in (
            (slow_delta, old_slow_pi, slow_field, slow_velocity, slow_omega),
            (heavy_delta, old_heavy_pi, heavy_field, heavy_velocity, heavy_omega)):
        old += momentum**2 / (2 * scale**2) + scale**2 * (wave**2 + omega**2) * delta**2 / 2
        old += -trace * velocity * momentum / 2 + scale**2 * trace * omega**2 * field * delta / 2
        old += scale**2 * trace**2 * velocity**2 / 8
    boundary_partial = scale**2 * trace / 2 * ((slow_rate + 2 * hubble * slow_velocity) * slow_delta
                                             + (heavy_rate + 2 * hubble * heavy_velocity) * heavy_delta)
    transformed = (momentum_h * momentum_eta - 3 * momentum_h**2) / scale**2 - scale**2 * wave**2 * eta**2
    transformed += (slow_pi**2 + heavy_pi**2) / (2 * scale**2)
    transformed += scale**2 * ((wave**2 + slow_omega**2) * slow_delta**2
                               + (wave**2 + heavy_omega**2) * heavy_delta**2) / 2
    transformed += geometry * source / 2 - 3 * scale**2 * source**2 / 4
    residual = scale**2 * trace / 2 * (
        (slow_rate + 2 * hubble * slow_velocity + slow_omega**2 * slow_field) * slow_delta
        + (heavy_rate + 2 * hubble * heavy_velocity + heavy_omega**2 * heavy_field) * heavy_delta)
    check("joint boundary-generated Hamiltonian", old + boundary_partial - transformed - residual)
    trace_prediction = sp.diff(transformed, momentum_h)
    eta_prediction = sp.diff(transformed, momentum_eta)
    check("reciprocal trace flow", trace_prediction - geometry / scale**2 + 3 * source)
    check("reciprocal curvature flow", eta_prediction - momentum_h / scale**2 - source / 2)
    check("slow scalar backreaction", -sp.diff(transformed, slow_delta)
          + scale**2 * (wave**2 + slow_omega**2) * slow_delta + scale**2 * slow_velocity * trace_prediction / 2)
    check("heavy scalar backreaction", -sp.diff(transformed, heavy_delta)
          + scale**2 * (wave**2 + heavy_omega**2) * heavy_delta + scale**2 * heavy_velocity * trace_prediction / 2)
    check("free metric eta momentum", -sp.diff(transformed, eta) - 2 * scale**2 * wave**2 * eta)

    background_real, background_imag, amplitude_real, amplitude_imag, phase = sp.symbols(
        "background_real background_imag amplitude_real amplitude_imag phase", real=True)
    carrier = sp.symbols("carrier", nonzero=True)
    background = background_real + sp.I * background_imag
    amplitude = amplitude_real + sp.I * amplitude_imag
    current = background_imag * amplitude_real - background_real * amplitude_imag
    counter = (background * amplitude / carrier - sp.conjugate(background * amplitude) * carrier) / (2 * sp.I)
    fast_source = slow_velocity * slow_delta + (current + counter) / (2 * scale**2)
    mean_source = slow_velocity * slow_delta + current / (2 * scale**2)
    mean = sp.expand(fast_source).coeff(carrier, 0)
    variance = (background_real**2 + background_imag**2) * (amplitude_real**2 + amplitude_imag**2) / (8 * scale**4)
    check("mean scalar momentum source", mean - mean_source)
    check("mean-square is square plus derived variance", sp.expand(fast_source**2).coeff(carrier, 0) - mean_source**2 - variance)
    mu = sp.symbols("mu", real=True)
    frequency = heavy_omega / hubble - mu + wave**2 / (2 * heavy_omega * hubble)
    averaged = frequency * (amplitude_real**2 + amplitude_imag**2) / 2
    averaged += (geometry * mean_source / 2 - 3 * scale**2 * mean_source**2 / 4) / hubble
    averaged += -3 * (background_real**2 + background_imag**2) * (
        amplitude_real**2 + amplitude_imag**2) / (32 * scale**2 * hubble)
    generated = -sp.I * (sp.diff(averaged, amplitude_real) + sp.I * sp.diff(averaged, amplitude_imag))
    predicted = -sp.I * (frequency - 3 * (background_real**2 + background_imag**2) / (16 * scale**2 * hubble)) * amplitude
    predicted -= (geometry - 3 * scale**2 * mean_source) * background / (4 * scale**2 * hubble)
    check("averaged action generates scalar force", generated - predicted)
    check("averaged metric reciprocity", sp.diff(averaged, momentum_eta) - mean_source / (2 * hubble))
    return checks

