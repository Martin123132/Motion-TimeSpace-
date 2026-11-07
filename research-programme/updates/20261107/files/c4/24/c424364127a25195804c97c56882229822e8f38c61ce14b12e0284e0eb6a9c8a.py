import os
from common import ROOT, EARLY, modest, require, read, write, digest
import numpy as np
import sympy as sp
from scipy.interpolate import CubicSpline


def load(path):
    with np.load(path) as data:
        return {name: data[name].copy() for name in data.files}


def scaled(value, reference):
    return float(np.max(abs(value)) / max(float(np.max(abs(reference))), 1e-30))


def main():
    modest()
    require(read(ROOT / "comparison-result.json")["passed"], "accepted hierarchy first")
    hubble, wave, cold, field, speed, mu, compression = sp.symbols("H k Rc phi v mu J", nonzero=True, real=True)
    density, perturbation, velocity = sp.symbols("dc h hp", real=True)
    selected_density = cold * density + mu**2 * field * perturbation + speed * velocity
    cold_rate = -selected_density / (2 * hubble) + compression
    field_rate = velocity
    velocity_rate = -2 * hubble * velocity - (wave**2 + mu**2) * perturbation + speed * cold_rate
    state = sp.Matrix([density, perturbation, velocity])
    uncoupled = sp.Matrix([[0, 0, 0], [0, 0, 1], [0, -wave**2-mu**2, -2*hubble]])
    feed = sp.Matrix([1, 0, speed])
    density_row = sp.Matrix([[cold, mu**2 * field, speed]])
    expected = (uncoupled - feed * density_row / (2 * hubble)) * state + feed * compression
    symbolic = [sp.simplify(item) for item in sp.Matrix([cold_rate, field_rate, velocity_rate]) - expected]
    require(all(item == 0 for item in symbolic), "selected action compression law")
    with np.load(EARLY / "runs/backgrounds/heavy.npz") as data:
        background_field = CubicSpline(data["heavy_efold"], data["phi_h"])
        background_velocity = CubicSpline(data["heavy_efold"], data["phidot_h"])
        mass = float(data["heavy_mass_mpc"])
    folder = ROOT / "runs-balanced/heavy"
    native, audit = load(folder / "native-reference.npz"), load(folder / "operator-audit.npz")
    names = native["observer_names"].tolist()
    observed = CubicSpline(native["times"], native["observer"], axis=0)
    selected, remaining = native["selected"], native["remaining"]
    reports = []
    for stamp, operator in zip(audit["times"], audit["matrices"]):
        row = observed(stamp)
        scale, hh, rc = [float(row[names.index(name)]) for name in ("a_native", "H_native", "R_cdm")]
        xx = operator[np.ix_(selected, selected)]
        xz = operator[np.ix_(selected, remaining)]
        zx = operator[np.ix_(remaining, selected)]
        metric_column = int(np.flatnonzero(native["mapping"][remaining] == 1)[0])
        native_hubble = -5. / xz[0, metric_column]
        native_velocity = xz[2, metric_column] / xz[0, metric_column]
        native_cold = -2 * native_hubble * xx[0, 0]
        native_mass_field = -2 * native_hubble * xx[0, 1]
        feed = np.array([1., 0., native_velocity])
        sparse = np.array([[0., 0., 0.], [0., 0., 1.], [0., -25 - (scale * mass)**2, -2 * native_hubble]])
        row_identity = scaled(xz - feed[:, None] * xz[0][None, :], xz)
        block_identity = scaled(xx - sparse - feed[:, None] * xx[0][None, :], xx)
        column_identity = scaled(native_cold * zx[:, 2] - native_velocity * zx[:, 0], native_cold * zx[:, 2])
        background_value = float(background_velocity(np.log(scale)))
        background_potential = (scale * mass)**2 * float(background_field(np.log(scale)))
        background_error = max(abs(native_velocity - background_value) / max(abs(native_velocity), abs(background_value), 1e-30), abs(native_mass_field - background_potential) / max(abs(native_mass_field), abs(background_potential), 1e-30))
        background_error = max(background_error, abs(native_hubble - hh) / abs(hh), abs(native_cold - rc) / abs(rc))
        reports.append(dict(time=float(stamp), row_rank_one_identity=row_identity, selected_block_identity=block_identity, density_channel_column_identity=column_identity, independent_background_error=background_error, independent_cdmc_density_error=abs(native_cold-rc)/abs(rc), inferred_velocity=native_velocity, background_velocity=background_value))
    kernels = []
    for fraction in (0, 25, 50):
        kernel = load(folder / f"kernel-{fraction}-fine.npz")
        rows = observed(kernel["times"])
        scales = rows[:, names.index("a_native")]
        speeds = background_velocity(np.log(scales))
        release_row = observed(float(kernel["release"]))
        release_scale, release_cold = [float(release_row[names.index(name)]) for name in ("a_native", "R_cdm")]
        release_speed = float(background_velocity(np.log(release_scale)))
        require(release_cold > 0, "regular CDM density basis on this benchmark")
        values = kernel["kernel"]
        first_row = np.column_stack([values[:, 0, 0], values[:, 0, 1], release_speed / release_cold * values[:, 0, 0]])
        predicted = np.array([1., 0., 0.])[None, :, None] * first_row[:, None, :]
        predicted[:, 2, :] = speeds[:, None] * first_row
        component_scale = np.maximum(np.max(abs(values), axis=0), 1e-30)
        reconstruction = float(np.max(np.max(abs(predicted - values), axis=0) / component_scale))
        kernels.append(dict(release_fraction=fraction/100., source_owned_two_function_reconstruction_error=reconstruction, zero_field_position_row=bool(np.count_nonzero(values[:, 1, :]) == 0), minimum_assumed_Rc=release_cold))
    symbolic_pass = all(value == 0 for value in symbolic)
    operator_pass = max(max(row["row_rank_one_identity"], row["selected_block_identity"], row["density_channel_column_identity"]) for row in reports) < 1e-10
    background_pass = max(row["independent_background_error"] for row in reports) < 2e-5
    kernel_pass = all(row["source_owned_two_function_reconstruction_error"] < 2e-5 and row["zero_field_position_row"] for row in kernels)
    output = dict(passed=symbolic_pass and operator_pass and background_pass and kernel_pass, pid=os.getpid(), symbolic=[str(value) for value in symbolic], operator_reports=reports, kernel_reports=kernels, algebra_gate=1e-10, independent_source_gate=2e-5, source_sha256=digest(__file__), comparison_sha256=digest(ROOT / "comparison-result.json"), operator_sha256=digest(folder / "operator-audit.npz"), no_fitted_coefficients=True, scope="linear scalar sector in synchronous CDM coordinates; rank-one output compression and two independent input histories on positive-Rc benchmark; not a universal scalarization of gravity or EM")
    write(ROOT / "memory-channel-algebra-result.json", output)
    print(output, flush=True)
    require(output["passed"], "action-owned memory channel test failed")


if __name__ == "__main__":
    main()

