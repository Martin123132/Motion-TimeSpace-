import csv
from common import ROOT, POST, PARENT, SECOND, ALGEBRA, GATE, modest, guard, check_parent, require, read, write, digest
import numpy as np
from symbolic import identities

JPAIR = np.array([[0., 1.], [-1., 0.]])
JFULL = np.kron(np.eye(4), JPAIR)


def sup(values):
    return float(np.max(abs(values)))


def norm(values):
    return max(sup(values), 1e-80)


def multiply(matrix, vector):
    return np.einsum("...ij,...j->...i", matrix, vector)


def transpose(matrix):
    return np.swapaxes(matrix, -1, -2)


def load(path):
    with np.load(path) as archive:
        return {name: archive[name].copy() for name in archive.files}


def matrices(scale, hubble, omega_s, velocity_s, omega_h, background, mu, phase, wave):
    count = len(scale)
    carrier_scale = scale * np.sqrt(omega_h)
    rotation = np.exp(1j * phase)
    velocity_h = np.sqrt(omega_h) / scale * (background / rotation).imag
    transform = np.empty((count, 2, 2))
    transform[:, 0, 0] = np.cos(phase) / carrier_scale
    transform[:, 0, 1] = np.sin(phase) / carrier_scale
    transform[:, 1, 0] = -carrier_scale * np.sin(phase)
    transform[:, 1, 1] = carrier_scale * np.cos(phase)
    transform_rate = np.diag([-1.5, 1.5])[None] @ transform + mu[:, None, None] * (transform @ JPAIR)
    hessian = np.zeros((count, 8, 8))
    hessian[:, 0, 0] = scale**2 * (wave**2 + omega_s**2) / hubble
    hessian[:, 1, 1] = 1 / (scale**2 * hubble)
    oscillator = np.zeros((count, 2, 2))
    oscillator[:, 0, 0] = scale**2 * (wave**2 + omega_h**2) / hubble
    oscillator[:, 1, 1] = 1 / (scale**2 * hubble)
    hessian[:, 2:4, 2:4] = transpose(transform) @ oscillator @ transform + transpose(transform) @ JPAIR @ transform_rate
    hessian[:, 5, 5] = -6 / (scale**2 * hubble)
    hessian[:, 5, 7] = hessian[:, 7, 5] = 1 / (scale**2 * hubble)
    hessian[:, 6, 6] = -2 * scale**2 * wave**2 / hubble
    source_row = np.zeros((count, 8))
    source_row[:, 0] = velocity_s
    source_row[:, 2:4] = velocity_h[:, None] * transform[:, 0]
    geometry_row = np.zeros_like(source_row)
    geometry_row[:, 5], geometry_row[:, 7] = -6., 1.
    cross = (geometry_row[:, :, None] * source_row[:, None, :] + source_row[:, :, None] * geometry_row[:, None, :]) / (2 * hubble[:, None, None])
    gravity_square = -3 * scale[:, None, None]**2 / (2 * hubble[:, None, None]) * source_row[:, :, None] * source_row[:, None, :]
    hessian += cross + gravity_square

    averaged = np.zeros_like(hessian)
    for indices in ((0, 0), (1, 1), (5, 5), (5, 7), (7, 5), (6, 6)):
        averaged[:, indices[0], indices[1]] = hessian[:, indices[0], indices[1]] if indices[0] != 0 else scale**2 * (wave**2 + omega_s**2) / hubble
    gamma = wave**2 / (2 * omega_h * hubble)
    mean_frequency = omega_h / hubble - mu + gamma
    averaged[:, 2, 2] = averaged[:, 3, 3] = mean_frequency
    mean_source_row = np.zeros_like(source_row)
    mean_source_row[:, 0] = velocity_s
    mean_source_row[:, 2] = background.imag / (2 * scale**2)
    mean_source_row[:, 3] = -background.real / (2 * scale**2)
    mean_cross = (geometry_row[:, :, None] * mean_source_row[:, None, :] + mean_source_row[:, :, None] * geometry_row[:, None, :]) / (2 * hubble[:, None, None])
    mean_square = -3 * scale[:, None, None]**2 / (2 * hubble[:, None, None]) * mean_source_row[:, :, None] * mean_source_row[:, None, :]
    averaged += mean_cross + mean_square
    variance_frequency = 3 * abs(background)**2 / (16 * scale**2 * hubble)
    averaged[:, 2, 2] -= variance_frequency
    averaged[:, 3, 3] -= variance_frequency
    return hessian, averaged, gravity_square, source_row, mean_source_row, variance_frequency, transform


def inspect(packet, wave, model):
    scale, hubble = packet["a"], packet["H"]
    meta, terms, observer = packet["metadata"], packet["terms"], packet["observer"]
    count = len(scale)
    slow_field, slow_v, slow_field_tau, slow_v_tau, slow_m, slow_d, slow_u = meta[:, 4:11].T
    omega_s = scale * slow_m
    if model == "heavy":
        heavy_field, heavy_v, heavy_field_tau, heavy_v_tau, heavy_m, heavy_d, heavy_u = meta[:, 14:21].T
        phase, mu = packet["carrier_phase"], packet["carrier_derivative"]
        omega_h = scale * heavy_m
        amplitude = packet["envelope"][:, 0] + 1j * packet["envelope"][:, 1]
        background = scale * (np.sqrt(omega_h) * heavy_field + 1j * heavy_v / np.sqrt(omega_h)) * np.exp(1j * phase)
    else:
        heavy_field = heavy_v = heavy_field_tau = heavy_v_tau = heavy_d = heavy_u = np.zeros(count)
        omega_h, phase, mu = scale.copy(), np.zeros(count), scale / hubble
        amplitude, background = np.zeros(count, complex), np.zeros(count, complex)
    density, current, pressure, density_tau, current_tau = [terms[:, :, index].sum(axis=1) for index in range(5)]
    shear = observer[:, 4]
    source = slow_v * slow_d + heavy_v * heavy_d
    metric = meta[:, 2]
    state = np.column_stack([slow_d, scale**2 * slow_u, amplitude.real, amplitude.imag, -2 * observer[:, 19],
                             scale**2 * (current / (2 * wave) - source / 2), observer[:, 7],
                             scale**2 * (2 * wave * metric + 3 * current / wave)])
    hessian, averaged, gravity_square, source_row, mean_row, variance_frequency, transform = matrices(
        scale, hubble, omega_s, slow_v, omega_h, background, mu, phase, wave)
    other_pressure = terms[:, :5, 2].sum(axis=1)
    linear = np.zeros_like(state)
    linear[:, 4] = -scale**2 / hubble * (other_pressure / 2 - shear / 3)
    linear[:, 6] = 2 * scale**2 * shear / hubble
    generated = multiply(JFULL, multiply(hessian, state) + linear)
    background_error = slow_v * (slow_v_tau + 2 * hubble * slow_v + omega_s**2 * slow_field)
    background_error += omega_s**2 * slow_field * (slow_field_tau - slow_v)
    if model == "heavy":
        background_error += heavy_v * (heavy_v_tau + 2 * hubble * heavy_v + omega_h**2 * heavy_field)
        background_error += omega_h**2 * heavy_field * (heavy_field_tau - heavy_v)
    hubble_tau = -(observer[:, 0] + 3 * observer[:, 1]) / 6 + background_error / (6 * hubble)
    metric_rate = density_tau / (2 * wave * hubble**2) + wave * observer[:, 8] / hubble**2 - metric * hubble_tau / hubble**2
    defects = packet["derivative_defect"]
    source_rate = slow_v_tau / hubble * slow_d + slow_v * slow_u / hubble
    source_rate += heavy_v_tau / hubble * heavy_d + heavy_v * (heavy_u / hubble + defects[:, 0])
    actual = np.zeros_like(state)
    actual[:, 0] = slow_u / hubble
    actual[:, 1] = -scale**2 * ((wave**2 + omega_s**2) * slow_d + wave * metric * slow_v) / hubble
    rotated_defect = np.zeros(count, complex)
    if model == "heavy":
        rotate = np.exp(1j * phase)
        gamma = wave**2 / (2 * omega_h * hubble)
        amplitude_rate = 1.5 * rotate**2 * amplitude.conjugate() - 1j * gamma * (amplitude + rotate**2 * amplitude.conjugate())
        amplitude_rate -= 1j * scale * wave * metric * heavy_v * rotate / (np.sqrt(omega_h) * hubble)
        amplitude_rate += 1j * (mu - omega_h / hubble) * amplitude
        rotated_defect = scale * rotate * (np.sqrt(omega_h) * defects[:, 0] + 1j * defects[:, 1] / np.sqrt(omega_h))
        actual[:, 2], actual[:, 3] = (amplitude_rate + rotated_defect).real, (amplitude_rate + rotated_defect).imag
    actual[:, 4], actual[:, 6] = 2 * wave * metric / hubble, observer[:, 8] / hubble
    actual[:, 5] = scale**2 * (current / wave - source + current_tau / (2 * wave * hubble) - source_rate / 2)
    actual[:, 7] = scale**2 * (2 * (2 * wave * metric + 3 * current / wave)
                                    + 2 * wave * metric_rate + 3 * current_tau / (wave * hubble))
    continuity = density_tau + hubble * (density + 3 * pressure) + wave * current + wave * metric * (observer[:, 0] + observer[:, 1])
    momentum = current_tau + 2 * hubble * current - wave * pressure + 2 * wave * shear / 3
    other_momentum = terms[:, :5, 4].sum(axis=1) + 2 * hubble * terms[:, :5, 1].sum(axis=1) - wave * other_pressure + 2 * wave * shear / 3
    predicted = np.zeros_like(state)
    predicted[:, 2], predicted[:, 3] = rotated_defect.real, rotated_defect.imag
    predicted[:, 5] = scale**2 * other_momentum / (2 * wave * hubble)
    eta_constraint = observer[:, 8] - current / (2 * wave)
    predicted[:, 6] = eta_constraint / hubble
    predicted[:, 7] = scale**2 * (continuity / hubble**2 + 3 * momentum / (wave * hubble)
                                          - 2 * wave * metric * (observer[:, 0] - 3 * hubble**2) / (3 * hubble**2)
                                          - wave * metric * background_error / (3 * hubble**3)
                                          + 2 * wave**2 * eta_constraint / hubble**2)
    active = np.arange(8) if model == "heavy" else np.array([0, 1, 4, 5, 6, 7])
    scales = np.maximum(np.maximum(np.max(abs(actual), axis=0), np.max(abs(generated), axis=0)), 1e-80)
    discrepancy = np.max(abs(actual - generated), axis=0) / scales
    accounted = np.max(abs(actual - generated - predicted), axis=0) / scales
    checks = dict(symmetry=sup(hessian - transpose(hessian)) / norm(hessian),
                  scalar_current=sup(np.sum(source_row * state, axis=1) - source) / norm(source),
                  canonical_mapping=sup((2 * wave * metric) - (state[:, 7] - 6 * state[:, 5]) / scale**2 + 3 * source) / norm(2 * wave * metric),
                  accounted_flow=float(np.max(accounted[active])))
    if model == "cold":
        checks["absent_heavy_flow"] = sup(generated[:, 2:4])
    if not np.any(state):
        checks["zero_state_flow"] = sup(generated)
    gravity_omission = multiply(JFULL, multiply(gravity_square, state))
    diagnostics = dict(raw_flow_errors=discrepancy.tolist(), accounted_flow_errors=accounted.tolist(),
                       raw_flow_within_retained_gate=bool(np.max(discrepancy[active]) < GATE),
                       omitted_gravity_square_rate_errors=(np.max(abs(gravity_omission), axis=0) / scales).tolist(),
                       source_interface="current rest-species stress; not a replacement Hamiltonian for their collision hierarchy")
    if model == "heavy":
        probes = np.unique(np.linspace(0, count - 1, 33, dtype=int))
        phase_means, coefficient_scales = [], None
        for phase_count in (16, 32):
            angle = np.tile(2 * np.pi * np.arange(phase_count) / phase_count, len(probes))
            expand = lambda values: np.repeat(values[probes], phase_count)
            sampled = matrices(expand(scale), expand(hubble), expand(omega_s), expand(slow_v), expand(omega_h),
                               expand(background), expand(mu), angle, wave)[0].reshape(len(probes), phase_count, 8, 8)
            phase_means.append(sampled.mean(axis=1))
            if phase_count == 32:
                coefficient_scales = np.maximum(np.max(abs(sampled), axis=1), 1e-80)
        checks["analytic_phase_average"] = float(np.max(abs(phase_means[-1] - averaged[probes]) / coefficient_scales))
        checks["phase_quadrature_refinement"] = float(np.max(abs(phase_means[0] - phase_means[1]) / coefficient_scales))
        mean_source = np.sum(mean_row * state, axis=1)
        mean_generated = multiply(JFULL, multiply(averaged, state) + linear)
        geometry = state[:, 7] - 6 * state[:, 5]
        mean_frequency = omega_h / hubble - mu + wave**2 / (2 * omega_h * hubble) - variance_frequency
        mean_amplitude_rate = -1j * mean_frequency * amplitude - (geometry - 3 * scale**2 * mean_source) * background / (4 * scale**2 * hubble)
        expected = mean_generated.copy()
        expected[:, 2], expected[:, 3] = mean_amplitude_rate.real, mean_amplitude_rate.imag
        expected[:, 4] = geometry / (scale**2 * hubble) - 3 * mean_source / hubble
        expected[:, 6] = state[:, 5] / (scale**2 * hubble) + mean_source / (2 * hubble)
        expected[:, 1] = -scale**2 * (wave**2 + omega_s**2) * slow_d / hubble - slow_v * geometry / (2 * hubble)
        expected[:, 1] += 3 * scale**2 * slow_v * mean_source / (2 * hubble)
        mean_scales = np.maximum(np.max(abs(mean_generated), axis=0), 1e-80)
        checks["averaged_action_equations"] = float(np.max(np.max(abs(mean_generated - expected), axis=0) / mean_scales))
        diagnostics["variance_frequency_max_Mpc0"] = float(np.max(variance_frequency))
        diagnostics["variance_over_gradient_frequency"] = float(np.max(variance_frequency / (wave**2 / (2 * omega_h * hubble))))
        diagnostics["bare_mean_instantaneous_rate_difference"] = (np.max(abs(mean_generated - generated), axis=0) / scales).tolist()
        diagnostics["mean_action_is_a_frozen_coefficient_result_not_forward_qualification"] = True
    for name, value in checks.items():
        require(np.isfinite(value) and 0 <= value < ALGEBRA, name + "=" + str(value))
    return checks, diagnostics


def main():
    modest()
    check_parent()
    frozen = {str(path): digest(path) for path in ROOT.iterdir() if path.is_file() and path.suffix in (".py", ".md")}
    write(ROOT / "frozen-inputs.json", dict(sources=frozen, parent=digest(PARENT / "closeout.json"), algebra=ALGEBRA, numerical=GATE))
    symbolic = identities()
    write(ROOT / "symbolic-result.json", dict(passed=True, identities=symbolic))
    owner = read(SECOND / "prediction-result.json")
    require(owner["state"] == "complete" and len(owner["reports"]) == 6, "complete saved histories")
    output = ROOT / "records"
    output.mkdir(exist_ok=False)
    rows = []
    for family in owner["reports"]:
        for case in family["cases"]:
            guard()
            path = SECOND / "runs-second" / (family["model"] + "-" + family["label"]) / case["file"]
            require(digest(path) == case["sha256"], "packet changed")
            packet = load(path)
            checks, diagnostics = inspect(packet, family["wave"], family["model"])
            row = dict(family=family["model"] + "-" + family["label"], tag=case["tag"], wave=family["wave"],
                       packet=str(path), sha256=case["sha256"], points=len(packet["a"]), checks=checks,
                       diagnostics=diagnostics, passed=True)
            write(output / (row["family"] + "-" + row["tag"] + ".json"), row)
            rows.append(row)
            print(row["family"], row["tag"], "algebra", max(checks.values()),
                  "raw", max(diagnostics["raw_flow_errors"]), flush=True)
            del packet
    check_parent()
    write(ROOT / "result.json", dict(passed=True, state="complete", source_hashes=frozen, records=rows,
          reused_histories=len(rows), new_evolutions=0, symbolic_identity_count=len(symbolic),
          raw_all_within_retained_gate=all(row["diagnostics"]["raw_flow_within_retained_gate"] for row in rows),
          scalar_gravity_hamiltonian_constructed=True, frozen_phase_mean_derived=True,
          averaged_forward_qualification_claimed=False, collision_species_hamiltonian_invented=False))
    with (ROOT / "summary.csv").open("x", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream)
        writer.writerow(["family", "case", "max_algebra", "max_raw_flow", "raw_gate_pass", "variance_over_gradient_frequency"])
        for row in rows:
            writer.writerow([row["family"], row["tag"], max(row["checks"].values()),
                             max(row["diagnostics"]["raw_flow_errors"]), row["diagnostics"]["raw_flow_within_retained_gate"],
                             row["diagnostics"].get("variance_over_gradient_frequency", 0.)])
    print("Complete", len(rows), "saved histories", len(symbolic), "identities", flush=True)


if __name__ == "__main__":
    main()

