import csv
import os
import sys
from common import ROOT, SOURCE, PHASE, EARLY, modest, guard, require, read, write, digest
sys.path.insert(0, str(SOURCE))
from probe_analysis import physical, fields
import numpy as np


def main():
    modest()
    require(read(ROOT / "derivation-result.json")["passed"], "symbolic gate")
    require(digest(PHASE / "validation-result.json") == "1cb5560de24ae40dd6368948b27b419a5b0ae448aedc704597f5471c348f036b", "phase validation owner")
    native = read(SOURCE / "phase-resolved/tangent-native-result.json")
    rows = []
    for model in ("heavy", "cold"):
        guard()
        owner = next(row for row in native["reports"] if row["model"] == model and row["tag"] == "one")
        path = SOURCE / "phase-resolved/packets" / owner["file"]
        require(digest(path) == owner["sha256"], "source hash")
        with np.load(path) as archive:
            first, last = int(archive["original_indices"][0]), int(archive["original_indices"][-1])
            data = dict(times=archive["full_times"][first:last + 1], observer=archive["full_observer"][first:last + 1], standard=archive["full_standard"][first:last + 1], observer_names=archive["observer_names"], names=archive["names"], k=archive["k"])
            probes = archive["original_indices"] - first
        times, wave = data["times"], float(data["k"])
        state = physical(data, model)
        names = data["observer_names"].tolist()
        value = lambda name: data["observer"][:, names.index(name)]
        scale, hubble, cold = value("a_native"), value("H_native"), value("R_cdm")
        enthalpy = value("R") + value("Pbar")
        if model == "heavy":
            field, speed, mass = fields(model)
            background, velocity = field(np.log(scale)), speed(np.log(scale))
            mu = scale * mass
            selected_star = velocity * state["p"] + mu**2 * background * state["u"] + cold * state["d_c"]
            selected_current = wave * velocity * state["u"] + cold * state["theta_c"] / wave
            selected = np.column_stack([state[name] for name in ("u", "p", "d_c", "theta_c")])
            density = velocity * state["p"] + 3 * velocity**2 * state["Phi"] + mu**2 * background * state["u"]
            pressure = velocity * state["p"] + 3 * velocity**2 * state["Phi"] - mu**2 * background * state["u"]
            momentum = wave * velocity * state["u"]
            omega0 = np.sqrt(wave**2 + mu[0]**2)
            field_scale = max(abs(selected[0, 0]), abs(selected[0, 1]) / omega0, 1e-30)
            cold_scale = max(abs(state["d_c"][0]), abs(state["theta_c"][0]) / hubble[0], abs(selected_star[0]) / cold[0], 1e-30)
            normalization = np.array([field_scale, field_scale * omega0, cold_scale, max(cold_scale * hubble[0], abs(state["theta_c"][0]))])
            source_scale = max(abs(velocity[0]) * normalization[1] + mu[0]**2 * abs(background[0]) * normalization[0], cold[0] * cold_scale, 1e-30)
        else:
            background = velocity = mu = np.zeros_like(scale)
            selected_star, selected_current = cold * state["d_c"], cold * state["theta_c"] / wave
            selected = np.column_stack([state["d_c"], state["theta_c"]])
            density = cold * (state["d_c"] + 3 * state["Phi"])
            pressure = np.zeros_like(density)
            momentum = selected_current
            cold_scale = max(abs(selected[0, 0]), abs(selected[0, 1]) / hubble[0], 1e-30)
            normalization = np.array([cold_scale, max(cold_scale * hubble[0], abs(selected[0, 1]))])
            source_scale = max(cold[0] * cold_scale, 1e-30)
        input_names = np.array(["a", "H", "S", "Rc", "phi", "v", "mu", "Dext", "Qext", "Pi"])
        inputs = np.column_stack([scale, hubble, enthalpy, cold, background, velocity, mu, state["Dstar"] - selected_star, state["Q"] - selected_current, state["Pi"]])
        with (PHASE / (model + "-phase-cells.csv")).open(newline="", encoding="utf-8") as stream:
            cells = list(csv.DictReader(stream))
        boundaries = np.array([float(cells[0]["left_tau_mpc"])] + [float(row["right_tau_mpc"]) for row in cells])
        evaluation = np.unique(np.r_[times, boundaries])
        np.savez_compressed(ROOT / (model + "-inputs.npz"), times=times, input_names=input_names, inputs=inputs, initial=selected[0], normalization=normalization, source_scale=source_scale, wave=wave, boundaries=boundaries, evaluation=evaluation, probes=times[probes], model=np.array(model))
        np.savez_compressed(ROOT / (model + "-reference.npz"), times=times, state=selected, D=density, P=pressure, Q=momentum, Phi=state["Phi"], Psi=state["Psi"], Dstar_total=state["Dstar"], Q_total=state["Q"], Pi=state["Pi"])
        row = dict(model=model, original_packet=str(path), original_sha256=owner["sha256"], input_file=model + "-inputs.npz", input_sha256=digest(ROOT / (model + "-inputs.npz")), reference_file=model + "-reference.npz", reference_sha256=digest(ROOT / (model + "-reference.npz")), previous_cells_sha256=digest(PHASE / (model + "-phase-cells.csv")), points=len(times), state_dimension=selected.shape[1], initial_only=True, supplied_other_species=True, later_selected_state_not_in_inputs=True)
        rows.append(row)
        print(row, flush=True)
    write(ROOT / "input-manifest.json", dict(passed=True, pid=os.getpid(), rows=rows, source_sha256=digest(__file__), symbolic_sha256=digest(ROOT / "derivation-result.json"), frozen_protocol_sha256=digest(ROOT / "PROTOCOL.md"), notes="External histories extracted by subtracting selected source from saved total. Source preparation is conditional, not independent observed-data validation."))


if __name__ == "__main__":
    main()

