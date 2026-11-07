import os
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
import sys
from pathlib import Path
sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parent / "heldout-final-spectrum-20261019"))
import stage168_common as previous
from stage168_common import *
ROOT = Path(__file__).resolve().parent
PARENT = ROOT.parent / "heldout-final-spectrum-20261019"
PARENT_SEAL = "d82ee94c688d00a2ac23c36a983ef126b8ff57c5e9d17f6ae6f92712a82c0afd"
STARTED = datetime(2026, 10, 19, 17, 20, 3, tzinfo=timezone.utc)
FRACTION_START = .875
FRACTION_TARGET = .90625
STEP_COUNTS = [128, 256]
ROUTE = "cubic"
BASELINE = BRANCH / "infrared-source-domain-20261008/backgrounds"
SOURCE166 = BRANCH / "endpoint-twofold-response-20261019"
COLUMNS = ["baseline", "mts_join1", "mts_join2", "total_join1", "total_join2", "zero"]


def finish(folder, checks, inputs, **metadata):
    paths = {*ROOT.glob("*.py"), ROOT / "ACCEPTANCE.md", ROOT / "DERIVATION.md",
             PARENT / "results/stage-integrity.json", *map(Path, inputs)}
    for module in list(sys.modules.values()):
        name = getattr(module, "__file__", None)
        if name and Path(name).suffix == ".py" and Path(name).resolve().is_relative_to(BRANCH):
            paths.add(Path(name).resolve())
    report = dict(state="complete", count=len(checks), checks=checks,
                  all_checks_passed=all(row["passed"] for row in checks),
                  finished_utc=datetime.now(timezone.utc).isoformat(),
                  input_hashes={str(path): digest(path) for path in sorted(paths)},
                  **metadata)
    write_json(folder / "status.json", report)
    (folder / "COMPLETE").write_text("complete\n", encoding="utf-8")
    return report


def history_paths(model, count=4096):
    label = f"{model}-{ROUTE}-{count}"
    return [(SOURCE155 / "results/response" / label / "response.npz", slice(10, 12)),
            (SOURCE158 / "results/response" / label / "response.npz", slice(2, 4)),
            (SOURCE159 / "results/response" / label / "response.npz", slice(2, 4)),
            (READOUT_OWNER / "results/response" / label / "response.npz", slice(2, 4)),
            (SOURCE166 / "results/response" / label / "terminal.npz", slice(10, 12))]


def state_at(model, fraction, basis, count=4096):
    background = thermal_wave.thermal.ThermalBackground(model)
    coordinate = fraction * background.end
    inputs = []
    values = {key: None for key in ["photon", "energy", "gas"]}
    for path, selection in history_paths(model, count):
        with np.load(path) as archive:
            times = archive["coordinate"]
            index = int(np.argmin(abs(times - coordinate)))
            assert abs(times[index] - coordinate) < 1e-13
            for key in values:
                current = archive[key][index, ..., selection]
                values[key] = current.copy() if values[key] is None else values[key] + current
        inputs.append(path)
    path = BASELINE / (model + "-nonlocal-refined-6400") / "history.npz"
    with np.load(path) as archive:
        times = archive["expansion"]
        index = int(np.argmin(abs(times - coordinate)))
        assert abs(times[index] - coordinate) < 1e-13
        photon = archive["profiles"][index]
        gas = archive["temperature_scaled"][index]
        energy = basis.energy @ photon
    inputs.append(path)
    return dict(photon=np.column_stack([photon, values["photon"], photon[:, None] + values["photon"], np.zeros(96)]),
                energy=np.r_[energy, values["energy"], energy + values["energy"], 0.],
                gas=np.r_[gas, values["gas"], gas + values["gas"], 0.]), inputs


class TemperatureEquation:
    def __init__(self, model):
        self.model = model
        self.background = thermal_wave.thermal.ThermalBackground(model)
        self.ladder = infrared_ladder.InfraredLadder(BRANCH / "emitting-thermal-background-20261008/banks/infrared96-q700")
        self.basis = self.ladder.basis
        self.coordinates = EnergyCoordinates(self.basis)
        self.emission = NonlocalEmission(self.basis, self.background, "nonlocal-leading",
                                        BRANCH / "infrared-source-domain-20261008/banks/s960-i256")
        self.sources = TwofoldSources()
        self.selection = slice(0, 2) if model == "heavy" else slice(2, 4)
        self.mass_factor = linalg.lu_factor(self.coordinates.mass)
        self.inputs = [*self.ladder.inputs, *self.emission.inputs, *self.sources.inputs,
                       self.background.parent.source, self.background.native_constants]
        self.baseline = np.array([1., 0., 0., 1., 1., 0.])
        self.maximum_rewrite = 0.
        self.begin = FRACTION_START * self.background.end
        self.end = FRACTION_TARGET * self.background.end

    def encode(self, state):
        return np.vstack([state["energy"], state["photon"][self.coordinates.others],
                          state["energy"] + self.background.chi * state["gas"]])

    def decode(self, state):
        return dict(photon=self.coordinates.transform @ state[:96],
                    energy=state[0], gas=(state[96] - state[0]) / self.background.chi)

    def source(self, coordinate):
        phase = (coordinate / self.background.end - .75) / .25
        packet = self.sources.complete_packet(phase, ROUTE, "terminal", 6).select(self.selection)
        force, spectral, gas, diagnostic = self.coordinates.source(packet.high)
        self.maximum_rewrite = max(self.maximum_rewrite, diagnostic["relative_change"])
        forcing = np.column_stack([np.zeros(96), force, force, np.zeros(96)])
        return forcing

    def at(self, coordinate):
        local = self.background.at(float(coordinate))
        theta = local["thermal_parameter"]
        rate = local["coefficient"] / theta
        stiffness = self.ladder.at(theta, 0)[:96, :96] - self.emission.at(theta, "dcbr")
        projected = self.coordinates.tests @ stiffness @ self.coordinates.transform
        coupled = self.coordinates.tests @ stiffness @ self.basis.temperature
        generator = np.zeros((97, 97))
        photon = linalg.lu_solve(self.mass_factor, rate * projected)
        gas = linalg.lu_solve(self.mass_factor, rate * coupled / self.background.chi)
        generator[:96, :96] = photon
        generator[:96, 0] += gas
        generator[:96, 96] = -gas
        generator[96, 0] = 1.
        generator[96, 96] = -1.
        forcing = np.vstack([linalg.lu_solve(self.mass_factor, rate * self.source(coordinate)), -self.baseline])
        return generator, forcing, dict(theta=theta, rate=rate, stiffness=stiffness)
