from datetime import datetime, timezone
from common import ROOT, CLOSURE, NATIVE, EARLY, BRANCH, ALGEBRA, modest, guard, require, check_prior, native_background, other_density, read, write, digest, load
import numpy as np
import scipy
from scipy.integrate._ivp import rk


def main():
    modest()
    check_prior()
    owner = read(CLOSURE / "readout-result.json")
    destination = ROOT / "inputs"
    destination.mkdir(exist_ok=False)
    reports = []
    for model_owner in owner["reports"]:
        guard()
        model = model_owner["model"]
        selected = next(row for row in model_owner["cases"] if row["tag"] == "G192-fine")
        source = CLOSURE / "runs" / model / selected["file"]
        require(digest(source) == selected["sha256"], "sealed source")
        packet = load(source)
        scale = packet["metadata"][:, 0]
        efold = np.log(scale)
        require(np.all(np.diff(efold) > 0) and scale[-1] < .00028, "exact domain and monotone physical grid")
        hubble = packet["metadata"][:, 1]
        fields = packet["metadata"][:, [4, 14]]
        velocities = packet["metadata"][:, [5, 15]]
        masses = packet["metadata"][0, [8, 18]]
        field_rates = packet["metadata"][:, [6, 16]]
        velocity_rates = packet["metadata"][:, [7, 17]]
        old_other = packet["observer"][:, 12:17].sum(axis=1)
        native = native_background(model)
        reproduced_other = other_density(native, scale)
        other_error = float(np.max(abs(reproduced_other - old_other)) / np.max(abs(old_other)))
        require(other_error < ALGEBRA, "native other sources mismatch")
        reconstructed_hubble = np.sqrt((reproduced_other + np.sum((velocities ** 2 + (scale[:, None] * masses * fields) ** 2) / 2, axis=1)) / 3)
        hubble_error = float(np.max(abs(reconstructed_hubble - hubble)) / np.max(abs(hubble)))
        require(hubble_error < ALGEBRA, "native source decomposition changed")
        span = efold[-1] - efold[0]
        slow_velocity_scale = max(abs(velocities[0, 0]), abs((scale[0] * masses[0]) ** 2 * fields[0, 0] / hubble[0]) * span, 1e-100)
        slow_displacement_scale = max(slow_velocity_scale / hubble[0] * span, 1e-100)
        if model == "heavy":
            heavy_displacement_scale = np.hypot(fields[0, 1], velocities[0, 1] / (scale[0] * masses[1]))
            heavy_velocity_scale = scale[0] * masses[1] * heavy_displacement_scale
            cap = float(.4 * np.min(hubble / (scale * masses[1])))
        else:
            heavy_displacement_scale = heavy_velocity_scale = 1.
            cap = float(span / 16)
        units = np.array([slow_displacement_scale, slow_velocity_scale, heavy_displacement_scale, heavy_velocity_scale, span / hubble[0]])
        initial = np.array([0., velocities[0, 0], 0., velocities[0, 1], 0.]) / units
        input_path = destination / (model + "-input.npz")
        reference_path = destination / (model + "-reference.npz")
        np.savez_compressed(input_path, efold=efold, original_scale=scale, initial_fields=fields[0], masses=masses, units=units, initial=initial, initial_time=packet["times"][0], step_cap=cap, initial_hubble=hubble[0])
        np.savez_compressed(reference_path, times=packet["times"], efold=efold, fields=fields, velocities=velocities, field_rates=field_rates, velocity_rates=velocity_rates, hubble=hubble, other_density=old_other,
                            old_delta=packet["metadata"][:, [9, 19]], old_delta_rate=packet["metadata"][:, [10, 20]])
        parameters_path = EARLY / ("runs/backgrounds/" + model + ".npz")
        report = dict(model=model, input=input_path.name, input_sha256=digest(input_path), reference=reference_path.name, reference_sha256=digest(reference_path), source=str(source), source_sha256=digest(source), original_parameter_table=str(parameters_path), original_parameter_sha256=digest(parameters_path), native_other_error=other_error, reconstructed_hubble_error=hubble_error, points=len(scale), scale_interval=[float(scale[0]), float(scale[-1])], efold_interval=[float(efold[0]), float(efold[-1])], original_time_interval=[float(packet["times"][0]), float(packet["times"][-1])], frozen_step_cap=cap, normalization_rule="initial field/velocity/mass and declared efold interval only")
        reports.append(report)
        print(model, report["scale_interval"], "source error", other_error, "cap", cap, flush=True)
        del native
    local_sources = [NATIVE.parent / "matching_common.py", BRANCH / "radiation-and-slow-field-transfer-20261007/radiation_common.py", CLOSURE / "build/native/camb/cambdll.dll", CLOSURE / "build/native/camb/results.py", CLOSURE / "build/native/camb/mts.py", CLOSURE / "background-repair-derivation.json"]
    write(ROOT / "input-result.json", dict(state="frozen", created_utc=datetime.now(timezone.utc).isoformat(), reports=reports, source_sha256=digest(__file__), protocol_sha256=digest(ROOT / "PROTOCOL.md"), previous_closeout_sha256=digest(CLOSURE / "closeout.json"), local_sources={str(path): digest(path) for path in local_sources}, scipy_version=scipy.__version__, dense_source_path=rk.__file__, dense_source_sha256=digest(rk.__file__), no_fit=True))


if __name__ == "__main__":
    main()
