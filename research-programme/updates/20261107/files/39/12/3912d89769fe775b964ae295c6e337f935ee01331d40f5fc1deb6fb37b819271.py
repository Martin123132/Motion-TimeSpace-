import os
import time
from datetime import datetime, timezone
from common import ROOT, guard, modest, require, read, write, digest
import numpy as np
from scipy.integrate import solve_ivp
from scipy.interpolate import CubicSpline

CASES = [
    dict(tag="full", mode="full", stride=1, tolerance=2e-11, amplitude=1., fundamental=True),
    dict(tag="source2", mode="full", stride=2, tolerance=2e-11, amplitude=1., fundamental=False),
    dict(tag="source4", mode="full", stride=4, tolerance=2e-11, amplitude=1., fundamental=False),
    dict(tag="precision", mode="full", stride=1, tolerance=2e-12, amplitude=1., fundamental=False),
    dict(tag="zero", mode="full", stride=1, tolerance=2e-11, amplitude=0., fundamental=False),
    dict(tag="negative", mode="full", stride=1, tolerance=2e-11, amplitude=-1., fundamental=False),
    dict(tag="feedback-off", mode="feedback-off", stride=1, tolerance=2e-11, amplitude=1., fundamental=False),
    dict(tag="poisson", mode="poisson", stride=1, tolerance=2e-11, amplitude=1., fundamental=True),
    dict(tag="poisson-precision", mode="poisson", stride=1, tolerance=2e-12, amplitude=1., fundamental=True),
]


def coefficients(values, wave, heavy, mode, amplitude):
    scale, hubble, enthalpy, cold, background, speed, mu, density_external, momentum_external, shear = values
    density_external, momentum_external, shear = amplitude * np.array([density_external, momentum_external, shear])
    denominator = 2 * wave**2 + 3 * enthalpy
    if heavy:
        primitive = np.array([[0., 1., 0., 0.], [-wave**2 - mu**2, -2 * hubble, 0., 0.], [0., 0., 0., -1.], [0., 0., 0., -hubble]])
        coupling = np.array([4 * speed, 2 * mu**2 * background, 0., wave**2])
        slip = np.array([-speed / wave**2, mu**2 * background / wave**2, 0., -1.])
        density_row = np.array([mu**2 * background, speed, cold, 0.])
        current_row = np.array([wave * speed, 0., 0., cold / wave])
    else:
        primitive = np.array([[0., -1.], [0., -hubble]])
        coupling = np.array([0., wave**2])
        slip = np.array([0., -1.])
        density_row = np.array([cold, 0.])
        current_row = np.array([0., cold / wave])
    if mode == "poisson":
        row = -density_row / denominator
        offset = -density_external / denominator
        shear = 0.
    else:
        row = -(density_row + 3 * hubble * current_row / wave) / denominator
        offset = -(density_external + 3 * hubble * momentum_external / wave) / denominator
        if mode == "feedback-off":
            row = np.zeros_like(row)
    matrix = primitive + np.outer(coupling, row)
    forcing = coupling * offset + slip * shear
    return matrix, forcing, row, offset, shear


def outputs(values, state, wave, heavy, mode, amplitude):
    scale, hubble, enthalpy, cold, background, speed, mu, external_density, external_current, shear = values.T
    external_density, external_current, shear = amplitude * np.array([external_density, external_current, shear])
    if heavy:
        selected_star = speed * state[:, 1] + mu**2 * background * state[:, 0] + cold * state[:, 2]
        selected_current = wave * speed * state[:, 0] + cold * state[:, 3] / wave
    else:
        selected_star, selected_current = cold * state[:, 0], cold * state[:, 1] / wave
    denominator = 2 * wave**2 + 3 * enthalpy
    if mode == "poisson":
        phi = -(selected_star + external_density) / denominator
        psi = phi
    elif mode == "feedback-off":
        phi = -(external_density + 3 * hubble * external_current / wave) / denominator
        psi = phi - shear / wave**2
    else:
        phi = -(selected_star + external_density + 3 * hubble * (selected_current + external_current) / wave) / denominator
        psi = phi - shear / wave**2
    if heavy:
        density = speed * state[:, 1] + mu**2 * background * state[:, 0] + 3 * speed**2 * phi
        pressure = speed * state[:, 1] - mu**2 * background * state[:, 0] + 3 * speed**2 * phi
        momentum = wave * speed * state[:, 0]
    else:
        density = cold * (state[:, 0] + 3 * phi)
        pressure = np.zeros_like(density)
        momentum = selected_current
    return dict(D=density, P=pressure, Q=momentum, Phi=phi, Psi=psi, Dstar_total=selected_star + external_density, Q_total=selected_current + external_current, D_total=selected_star + external_density + 3 * enthalpy * phi)


def integrate(data, case):
    times, evaluation = data["times"], data["evaluation"]
    indices = np.unique(np.r_[np.arange(0, len(times), case["stride"]), len(times) - 1])
    inputs = CubicSpline(times[indices], data["inputs"][indices], axis=0)
    normalization = data["normalization"]
    dimension = len(normalization)
    heavy = str(data["model"]) == "heavy"
    wave = float(data["wave"])
    duration = times[-1] - times[0]
    integral_scale = float(data["source_scale"]) * duration
    initial = np.r_[case["amplitude"] * data["initial"] / normalization, np.zeros(3)]
    if case["fundamental"]:
        initial = np.r_[initial, np.eye(dimension).ravel()]
    last_guard = time.monotonic()

    def rhs(stamp, solution):
        nonlocal last_guard
        if time.monotonic() - last_guard > 2:
            guard()
            last_guard = time.monotonic()
        values = inputs(stamp)
        matrix, forcing, row, offset, shear = coefficients(values, wave, heavy, case["mode"], case["amplitude"])
        state = solution[:dimension] * normalization
        rate = (matrix @ state + forcing) / normalization
        phi = row @ state + offset
        scale, hubble, enthalpy, cold, background, speed, mu = values[:7]
        if heavy:
            density = speed * state[1] + mu**2 * background * state[0] + 3 * speed**2 * phi
            pressure = speed * state[1] - mu**2 * background * state[0] + 3 * speed**2 * phi
            momentum = wave * speed * state[0]
        else:
            density, pressure, momentum = cold * (state[0] + 3 * phi), 0., cold * state[1] / wave
        derivative = np.r_[rate, np.array([density, pressure, momentum]) / integral_scale]
        if case["fundamental"]:
            normalized_matrix = matrix * normalization[np.newaxis, :] / normalization[:, np.newaxis]
            derivative = np.r_[derivative, (normalized_matrix @ solution[dimension + 3:].reshape(dimension, dimension)).ravel()]
        return derivative

    started = time.monotonic()
    solution = solve_ivp(rhs, (times[0], times[-1]), initial, method="DOP853", rtol=case["tolerance"], atol=case["tolerance"] / 100, t_eval=evaluation)
    require(solution.success and np.isfinite(solution.y).all(), "forward integration")
    states = solution.y[:dimension].T * normalization
    output = outputs(inputs(evaluation), states, wave, heavy, case["mode"], case["amplitude"])
    arrays = dict(times=evaluation, state=states, integrals=solution.y[dimension:dimension + 3].T * integral_scale, normalization=normalization, boundaries=data["boundaries"], **output)
    if case["fundamental"]:
        arrays["fundamental"] = solution.y[dimension + 3:].T.reshape(-1, dimension, dimension)
    return arrays, dict(evaluations=solution.nfev, seconds=time.monotonic() - started, success=solution.success)


def main():
    modest()
    manifest = read(ROOT / "input-manifest.json")
    require(manifest["passed"] and digest(ROOT / "PROTOCOL.md") == manifest["frozen_protocol_sha256"], "frozen inputs")
    write(ROOT / "run-config.json", dict(cases=CASES, source_sha256=digest(__file__), input_manifest_sha256=digest(ROOT / "input-manifest.json"), theory_parameter_changes=False, target_reference_read_by_runner=False))
    folder = ROOT / "predictions"
    folder.mkdir(exist_ok=False)
    reports = []
    error = None
    try:
        for owner in manifest["rows"]:
            require(digest(ROOT / owner["input_file"]) == owner["input_sha256"], "input ownership")
            with np.load(ROOT / owner["input_file"]) as archive:
                data = {name: archive[name].copy() for name in archive.files}
            for case in CASES:
                guard()
                arrays, receipt = integrate(data, case)
                filename = owner["model"] + "-" + case["tag"] + ".npz"
                np.savez_compressed(folder / filename, **arrays)
                report = dict(model=owner["model"], case=case, file=filename, sha256=digest(folder / filename), **receipt)
                write(folder / (filename + ".json"), report)
                reports.append(report)
                print(report, flush=True)
    except Exception as failure:
        error = repr(failure)
        raise
    finally:
        write(ROOT / "prediction-result.json", dict(state="complete" if error is None and len(reports) == 2 * len(CASES) else "failed", error=error, pid=os.getpid(), finished=datetime.now(timezone.utc).isoformat(), reports=reports, config_sha256=digest(ROOT / "run-config.json"), input_manifest_sha256=digest(ROOT / "input-manifest.json"), source_sha256=digest(__file__)))


if __name__ == "__main__":
    main()

