import csv
import sys
from common import ROOT, POST, PARENT, ALGEBRA, GATE, modest, guard, digest, read, write, require, check_parent
import numpy as np
from scipy.interpolate import CubicSpline
from symbolic import identities

OUTPUT = ROOT / "verified"

SYMPLECTIC = np.array([[0., 1.], [-1., 0.]])


def norm(values):
    return max(float(np.max(abs(values))), 1e-80)


def error(values, reference):
    return norm(values - reference) / norm(reference) if np.any(values - reference) else 0.


def multiply(matrix, vector):
    return np.einsum("...ij,...j->...i", matrix, vector)


def transpose(matrix):
    return np.swapaxes(matrix, -1, -2)


def load(path):
    with np.load(path) as archive:
        return {name: archive[name].copy() for name in archive.files}


def native_modes(packet, wave, model):
    meta, terms = packet["metadata"], packet["terms"]
    checks = {}
    for species, offset, label in ((5, 4, "slow"), (6, 14, "heavy")):
        if label == "heavy" and model == "cold":
            checks["cold_absent_heavy"] = float(np.max(abs(terms[:, 6])))
            continue
        field, velocity, field_rate, velocity_rate, mass, delta, speed = meta[:, offset:offset + 7].T
        hubble, omega = meta[:, 1], meta[:, 0] * mass
        density = velocity * speed + omega**2 * field * delta
        pressure = velocity * speed - omega**2 * field * delta
        current = wave * velocity * delta
        for component, values in ((0, density), (1, current), (2, pressure)):
            checks[label + "_stress_" + str(component)] = error(values, terms[:, species, component])
        defects = packet["derivative_defect"] if species == 6 else np.zeros((len(meta), 2))
        field_error = field_rate - velocity
        velocity_error = velocity_rate + 2 * hubble * velocity + omega**2 * field
        delta_rate = speed + hubble * defects[:, 0]
        speed_rate = -2 * hubble * speed - (wave**2 + omega**2) * delta - wave * meta[:, 2] * velocity + hubble * defects[:, 1]
        density_rate = velocity_rate * speed + velocity * speed_rate + omega**2 * (
            2 * hubble * field * delta + field_rate * delta + field * delta_rate)
        current_rate = wave * (velocity_rate * delta + velocity * delta_rate)
        checks[label + "_density_rate"] = error(density_rate, terms[:, species, 3])
        checks[label + "_momentum_rate"] = error(current_rate, terms[:, species, 4])
        continuity = density_rate + hubble * (density + 3 * pressure) + wave * current + wave * meta[:, 2] * velocity**2
        momentum = current_rate + 2 * hubble * current - wave * pressure
        predicted_continuity = velocity_error * speed + omega**2 * field_error * delta + hubble * (
            velocity * defects[:, 1] + omega**2 * field * defects[:, 0])
        predicted_momentum = wave * velocity_error * delta + hubble * wave * velocity * defects[:, 0]
        checks[label + "_Ward_density"] = norm(continuity - predicted_continuity) / max(
            norm(density_rate), norm(hubble * density), norm(wave * current))
        checks[label + "_Ward_current"] = norm(momentum - predicted_momentum) / max(
            norm(current_rate), norm(hubble * current), norm(wave * pressure))
        if not np.any(continuity - predicted_continuity):
            checks[label + "_Ward_density"] = 0.
        if not np.any(momentum - predicted_momentum):
            checks[label + "_Ward_current"] = 0.
    return checks


def pullback(packet, table, wave, coarse):
    meta, native = packet["metadata"], packet["terms"][:, 6]
    scale, hubble = packet["a"], packet["H"]
    omega = scale * float(packet["mass"])
    phase, mu = packet["carrier_phase"], packet["carrier_derivative"]
    field, velocity, field_rate, velocity_rate, unused_mass, delta, speed = meta[:, 14:21].T
    rotation = np.exp(1j * phase)
    background = scale * (np.sqrt(omega) * field + 1j * velocity / np.sqrt(omega)) * rotation
    amplitude, coordinate = packet["envelope"], packet["normal_amplitude"]
    gamma = wave**2 / (2 * omega * hubble)
    coupling = wave / (2 * hubble)
    primitive = rotation**2 / (2j * mu)
    density_metric_row = omega[:, None] * np.column_stack([background.real, background.imag]) / (
        2 * wave * hubble * scale**2)[:, None]
    first_columns = np.column_stack([
        primitive * ((1.5 - 1j * gamma) * basis.conjugate()
                     + coupling * density_metric_row[:, index] * background.conjugate())
        for index, basis in enumerate((1 + 0j, 1j))])
    keep = np.unique(np.r_[np.arange(0, len(table["efold"]), 2 if coarse else 1), len(table["efold"]) - 1])
    rows = CubicSpline(table["efold"][keep], table["coefficients"][keep], axis=0)(packet["efold"])
    slots = packet["envelope_slots"]
    scalar_columns = np.column_stack([rows[:, int(np.flatnonzero(table["support"] == slot)[0])] for slot in slots])
    matrices = np.eye(2)[None] - np.stack([(first_columns + scalar_columns).real,
                                          (first_columns + scalar_columns).imag], axis=1)
    inverse = np.linalg.inv(matrices)
    core = packet["projected_state"][:, packet["core"]].copy()
    core[:, slots] = 0.
    spectator_primitive = np.sum(rows * core[:, table["support"]], axis=1)
    other_density = packet["terms"][:, :6, 0].sum(axis=1)
    eta = packet["observer"][:, 7]
    force_density = primitive * coupling * background.conjugate() / (2 * wave * hubble)
    force_eta = primitive * coupling * background.conjugate() * wave / hubble
    forcing_complex = force_density * other_density + force_eta * eta + spectator_primitive
    forcing = np.column_stack([forcing_complex.real, forcing_complex.imag])
    recovered = multiply(inverse, coordinate + forcing)
    columns = np.column_stack([force_density, force_eta, np.ones(len(scale)), 1j * np.ones(len(scale))])
    spectator_map = np.stack([columns.real, columns.imag], axis=1)
    aggregates = np.column_stack([other_density, eta, spectator_primitive.real, spectator_primitive.imag])
    carrier_scale = scale * np.sqrt(omega)
    transform = np.empty((len(scale), 2, 2))
    transform[:, 0, 0] = np.cos(phase) / carrier_scale
    transform[:, 0, 1] = np.sin(phase) / carrier_scale
    transform[:, 1, 0] = -carrier_scale * np.sin(phase)
    transform[:, 1, 1] = carrier_scale * np.cos(phase)
    derivative = np.einsum("ij,njk->nik", np.diag([-1.5, 1.5]), transform) + mu[:, None, None] * (transform @ SYMPLECTIC)
    physical_pair = multiply(transform, recovered)
    delta_row, speed_row = transform[:, 0], transform[:, 1] / scale[:, None]**2
    stress_rows = np.stack([velocity[:, None] * speed_row + (omega**2 * field)[:, None] * delta_row,
                           (wave * velocity)[:, None] * delta_row,
                           velocity[:, None] * speed_row - (omega**2 * field)[:, None] * delta_row], axis=1)
    source_matrix = stress_rows @ inverse
    sources = multiply(source_matrix, coordinate + forcing)
    naive_sources = multiply(source_matrix, coordinate)
    checks = dict(inverse=error(recovered, amplitude), spectator_aggregation=error(multiply(spectator_map, aggregates), forcing),
                  density=error(sources[:, 0], native[:, 0]), current=error(sources[:, 1], native[:, 1]),
                  pressure=error(sources[:, 2], native[:, 2]), field=error(physical_pair[:, 0], delta),
                  conjugate_momentum=error(physical_pair[:, 1], scale**2 * speed),
                  inverse_bound=float(np.max(np.maximum(np.max(np.sum(abs(inverse), axis=2), axis=1) - packet["inverse_bound"], 0))))
    area = np.linalg.det(inverse)
    scalar_form = transpose(inverse) @ SYMPLECTIC @ inverse
    checks["scalar_two_form"] = error(scalar_form, area[:, None, None] * SYMPLECTIC)
    joint = np.concatenate([inverse, inverse @ spectator_map], axis=2)
    joint_form = transpose(transform @ joint) @ SYMPLECTIC @ (transform @ joint)
    expected_form = np.empty_like(joint_form)
    expected_form[:, :2, :2] = scalar_form
    expected_form[:, :2, 2:] = scalar_form @ spectator_map
    expected_form[:, 2:, :2] = -transpose(expected_form[:, :2, 2:])
    expected_form[:, 2:, 2:] = transpose(spectator_map) @ scalar_form @ spectator_map
    checks["spectator_two_form"] = error(joint_form, expected_form)

    oscillator = np.zeros_like(transform)
    oscillator[:, 0, 0] = scale**2 * (wave**2 + omega**2) / hubble
    oscillator[:, 1, 1] = 1 / (scale**2 * hubble)
    connection = transpose(transform) @ SYMPLECTIC @ derivative
    hamiltonian = transpose(transform) @ oscillator @ transform + connection
    trace_rate = 2 * wave * meta[:, 2] / hubble
    metric_gradient = (scale**2 * velocity * trace_rate / 2)[:, None] * delta_row
    parent_from_action = multiply(SYMPLECTIC, multiply(hamiltonian, amplitude) + metric_gradient)
    native_pair_rate = np.column_stack([speed / hubble, -scale**2 * (
        (wave**2 + omega**2) * delta + wave * meta[:, 2] * velocity) / hubble])
    parent_from_native = multiply(np.linalg.inv(transform), native_pair_rate - multiply(derivative, amplitude))
    checks["carrier_action_equation"] = error(parent_from_action, parent_from_native)
    checks["carrier_connection_symmetry"] = norm(connection - transpose(connection)) / norm(connection)
    checks["carrier_symplectic"] = error(transpose(transform) @ SYMPLECTIC @ transform,
                                         np.broadcast_to(SYMPLECTIC, transform.shape))
    defects = packet["derivative_defect"]
    physical_increment = np.column_stack([defects[:, 0], scale**2 * defects[:, 1]])
    euler_pair = -multiply(SYMPLECTIC, physical_increment)
    euler_coordinate = multiply(transpose(transform @ inverse), euler_pair)
    coordinate_increment = packet["second_desired_rate"] - packet["second_full_rate"]
    predicted_euler_coordinate = -multiply(scalar_form, coordinate_increment)
    checks["Euler_coordinate_chain"] = error(euler_coordinate, predicted_euler_coordinate)
    metric_momentum = -scale**2 * velocity * delta / 2
    checks["metric_momentum_source"] = error(metric_momentum, -scale**2 * native[:, 1] / (2 * wave))
    field_error = field_rate - velocity
    actual_velocity_density = field_rate * (speed + hubble * defects[:, 0]) + omega**2 * field * delta
    background_density_increment = field_error * speed
    candidate_density_increment = hubble * field_rate * defects[:, 0]
    checks["covariant_velocity_density"] = float(np.max(abs(actual_velocity_density - native[:, 0] - background_density_increment
                                                - candidate_density_increment))) / norm(native[:, 0])
    scales = np.array([norm(native[:, 0]), norm(native[:, 1]), norm(native[:, 2])])
    ablations = dict(omit_spectator_forcing=((np.max(abs(naive_sources - sources), axis=0)) / scales).tolist(),
                     assume_canonical_area=float(np.max(abs(area - 1))),
                     omit_carrier_connection=float(np.max(abs(multiply(SYMPLECTIC, multiply(connection, amplitude))))) / norm(parent_from_native),
                     omit_metric_coupling=float(np.max(abs(multiply(SYMPLECTIC, metric_gradient)))) / norm(parent_from_native))
    diagnostics = dict(area_min=float(np.min(area)), area_max=float(np.max(area)),
                       coordinate_Euler_residual_over_parent_rate=norm(euler_coordinate) / norm(parent_from_native)
                       if np.any(euler_coordinate) else 0.,
                       covariant_truncation_density_over_density=norm(candidate_density_increment) / norm(native[:, 0])
                       if np.any(candidate_density_increment) else 0.,
                       represented_background_density_over_density=norm(background_density_increment) / norm(native[:, 0])
                       if np.any(background_density_increment) else 0.,
                       canonical_velocity_defect_over_velocity=norm(hubble * defects[:, 0]) / norm(speed)
                       if np.any(defects[:, 0]) else 0.,
                       boundary_metric_momentum_max=float(np.max(abs(metric_momentum))))
    require(np.isfinite(sources).all() and np.min(area) > 0, "finite source / nondegenerate two-form")
    return checks, ablations, diagnostics, sources


def main():
    modest()
    OUTPUT.mkdir(exist_ok=False)
    check_parent()
    frozen = {str(path): digest(path) for path in ROOT.iterdir() if path.is_file() and path.suffix in (".py", ".md")}
    write(OUTPUT / "frozen-inputs.json", dict(sources=frozen, algebra=ALGEBRA, numerical=GATE,
          parent=digest(PARENT / "closeout.json"), no_new_evolutions=True))
    symbolic = identities()
    write(OUTPUT / "symbolic-result.json", dict(passed=True, identities=symbolic))
    owner = read(PARENT / "prediction-result.json")
    require(owner["state"] == "complete" and len(owner["reports"]) == 6, "six complete families")
    results = []
    for family in owner["reports"]:
        guard()
        stem = family["model"] + "-" + family["label"]
        folder = PARENT / "runs-second" / stem
        table = load(folder / "micromotion-coefficients.npz") if family["model"] == "heavy" else None
        family_sources = {}
        for case in family["cases"]:
            guard()
            path = folder / case["file"]
            require(digest(path) == case["sha256"], "packet source")
            packet = load(path)
            checks = native_modes(packet, family["wave"], family["model"])
            ablations, diagnostics = {}, {}
            if family["model"] == "heavy":
                more, ablations, diagnostics, sources = pullback(packet, table, family["wave"], case["coarse_coefficients"])
                checks.update(more)
            else:
                sources = packet["terms"][:, 0, :3].copy()
                checks["cold_zero_coordinate"] = float(np.max(abs(packet["first_amplitude"])))
                checks["cold_zero_derivative_defect"] = float(np.max(abs(packet["derivative_defect"])))
            if case["amplitude"] == 0:
                checks["zero_source"] = float(np.max(abs(sources)))
            for key, value in checks.items():
                require(np.isfinite(value) and value < ALGEBRA, stem + "/" + case["tag"] + ": " + key + "=" + str(value))
            family_sources[case["tag"]] = sources
            record = dict(family=stem, tag=case["tag"], points=len(packet["a"]), packet=str(path),
                          sha256=case["sha256"], passed=True, checks=checks, ablations=ablations, diagnostics=diagnostics)
            results.append(record)
            write(OUTPUT / (stem + "-" + case["tag"] + ".json"), record)
            print(stem, case["tag"], "passed", max(checks.values()), flush=True)
            del packet
        reference = family_sources["G192-full-fine"]
        comparison = {tag: (np.max(abs(values - reference), axis=0) /
                           np.maximum(np.max(abs(reference), axis=0), 1e-80)).tolist()
                      for tag, values in family_sources.items() if tag in ("G192-reduced-fine", "L128-full-fine")}
        write(OUTPUT / (stem + "-paired-source-comparison.json"), dict(family=stem, differences=comparison,
              normalized_each_source=True, diagnostic_only=True, no_changed_parent_qualification=True))
    check_parent()
    result = dict(state="complete", passed=True, records=results, reused_histories=len(results), new_evolutions=0,
                  algebra_gate=ALGEBRA, numerical_gate=GATE, symbolic_identity_count=len(symbolic),
                  scalar_action_pullback_verified=True, full_truncated_covariant_action_claimed=False,
                  source_hashes=frozen, parent_closeout_sha256=digest(PARENT / "closeout.json"),
                  source_semantics="parent canonical phase-space stress pulled back exactly; finite candidate Euler defects retained")
    write(OUTPUT / "result.json", result)
    with (OUTPUT / "summary.csv").open("x", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream)
        writer.writerow(["family", "case", "max_algebra_error", "area_deviation", "omitted_spectator_D", "omitted_spectator_Q",
                         "omitted_spectator_P", "covariant_truncation_D", "Euler_residual"])
        for row in results:
            ablations, diagnostics = row["ablations"], row["diagnostics"]
            writer.writerow([row["family"], row["tag"], max(row["checks"].values()), ablations.get("assume_canonical_area", 0),
                             *ablations.get("omit_spectator_forcing", [0, 0, 0]),
                             diagnostics.get("covariant_truncation_density_over_density", 0),
                             diagnostics.get("coordinate_Euler_residual_over_parent_rate", 0)])
    print("Complete:", len(results), "saved histories;", len(symbolic), "identities; no new evolutions", flush=True)


if __name__ == "__main__":
    main()

