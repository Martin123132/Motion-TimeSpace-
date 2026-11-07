from stage169_common import *
import stage169_common as first
LEGACY = BRANCH / "complete-corrected-history-20261015"
sys.path.insert(0, str(LEGACY))
from complete_history_common import compact_defect
from replay_saved_response import solve_response_trace
SOURCE147 = BRANCH / "cubic-response-step-refinement-20261016"
NATIVE_WINDOW = BRANCH / "downstream-window-transfer-20261012/results/window-transfer"


def legacy_owner(model, match):
    return LEGACY / "results" / f"feedback-{model}-m{match}"


def trace_path(model, match):
    return ROOT / "results/legacy-replay" / f"{model}-m{match}" / "trace.npz"


def sampled(archive, coordinate, keys, selection=None, time_key="coordinate"):
    times = archive[time_key]
    index = int(np.argmin(abs(times - coordinate)))
    assert abs(times[index] - coordinate) < 1e-13
    return {key: archive[key][index].copy() if selection is None else archive[key][index, ..., selection].copy() for key in keys}


def corrected_state_at(model, fraction, basis, match=20, count=4096):
    background = thermal_wave.thermal.ThermalBackground(model)
    coordinate = fraction * background.end
    components = [(SOURCE147 / "results/response" / f"{model}-4096/transfer/response.npz", slice(2, 4)),
                  *first.history_paths(model, count)]
    components[1] = (components[1][0], slice(2, 4))
    values = {key: None for key in ["photon", "energy", "gas"]}
    inputs = []
    for path, selection in components:
        with np.load(path) as archive:
            portion = sampled(archive, coordinate, values, selection)
        for key in values:
            values[key] = portion[key] if values[key] is None else values[key] + portion[key]
        inputs.append(path)
    path = NATIVE_WINDOW / f"{model}-main-1024.npz"
    with np.load(path) as archive:
        native = sampled(archive, coordinate, values, slice(0, 2))
    inputs.append(path)
    for key in values:
        values[key] += native[key]
    path = BASELINE / f"{model}-nonlocal-refined-6400/history.npz"
    with np.load(path) as archive:
        initial = sampled(archive, coordinate, ["profiles", "energy_scaled", "temperature_scaled"], time_key="expansion")
    inputs.append(path)
    path = trace_path(model, match)
    assert verify_packet(path.parent)["all_checks_passed"]
    with np.load(path) as archive:
        feedback = sampled(archive, coordinate, values, slice(0, 3))
    inputs.extend([path, path.parent / "status.json"])
    photon = np.column_stack([initial["profiles"], values["photon"]]) + feedback["photon"]
    energy = np.r_[initial["energy_scaled"], values["energy"]] + feedback["energy"]
    gas = np.r_[initial["temperature_scaled"], values["gas"]] + feedback["gas"]
    return dict(photon=np.column_stack([photon, photon[:, :1] + photon[:, 1:3], np.zeros(96)]),
                energy=np.r_[energy, energy[:1] + energy[1:3], 0.],
                gas=np.r_[gas, gas[:1] + gas[1:3], 0.]), inputs


def unresolved_carrier(model, fraction, match, reader):
    background = thermal_wave.thermal.ThermalBackground(model)
    coordinate = fraction * background.end
    candidates = [BRANCH / name / "results" / f"evolution-{model}-carry/prediction.npz" for name in
                  ["three-quarter-history-cubic-carry-20261015",
                   "seven-eighths-history-cubic-carry-20261015",
                   "complete-corrected-history-20261015"]]
    chosen = None
    for path in candidates:
        with np.load(path) as archive:
            times = archive["coordinate"]
            if times[0] - 1e-13 <= coordinate <= times[-1] + 1e-13:
                packet = sampled(archive, coordinate, ["defect"])
                packet["frequency"] = archive["frequency"].copy()
                chosen = path
                break
    assert chosen is not None
    path = legacy_owner(model, match) / "physical-source.npz"
    with np.load(path) as archive:
        projected = sampled(archive, coordinate, ["projected_replacement"])["projected_replacement"]
    raw = compact_defect(reader.frequency, packet["frequency"], packet["defect"], match / 1000.)
    carrier = raw - reader.values @ projected
    values = np.column_stack([carrier, carrier[:, :1] + carrier[:, 1:3], np.zeros(len(reader.frequency))])
    return values, (reader.measure * reader.frequency) @ values, [chosen, path]


class HybridEquation(TemperatureEquation):
    def __init__(self, model, match):
        super().__init__(model)
        self.match = match
        path = legacy_owner(model, match) / "physical-source.npz"
        with np.load(path) as archive:
            self.legacy = interpolate.interp1d(archive["coordinate"], archive["source"].sum(axis=1), axis=0, bounds_error=True)
        self.inputs.append(path)

    def source(self, coordinate):
        original = super().source(coordinate)
        spectral = self.legacy(coordinate)
        force = self.coordinates.tests @ spectral
        return original + np.column_stack([force, force[:, :1] + force[:, 1:3], np.zeros(96)])
