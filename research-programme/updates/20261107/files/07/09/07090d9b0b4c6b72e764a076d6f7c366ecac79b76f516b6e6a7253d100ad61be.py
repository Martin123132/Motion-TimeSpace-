from common import *
from coefficient_loader import coefficients
from compact_adjoint import CompactAdjoint
from adjoint_operator import open_owned
from energy_map import EnergyMap
import numpy as np


def main():
    modest()
    check_parent()
    require(read(ROOT / "probe-result.json")["passed"], "completed probe")
    (ROOT / "diagnosis-contexts").mkdir(exist_ok=False)
    outputs = []
    for model in ("heavy", "cold"):
        packet = coefficients(model)
        operator = CompactAdjoint(packet)
        system = open_owned(model, "diagnosis-contexts")
        energy = EnergyMap(system)
        previous = read(ROOT / (model + "-probe.json"))
        worst = max(previous["rows"], key=lambda row: row["comparison"][1][1])
        efold = worst["efold"]
        core = operator.blocks(efold, 0)[0]
        matrix, transform, inverse, _ = energy.generator(efold, core)
        remainder = matrix[np.ix_(energy.rest, energy.rest)]
        eigenvalues, eigenvectors = np.linalg.eigh((remainder + remainder.T) / 2)
        vector = eigenvectors[:, -1]
        dominant = np.argsort(abs(vector))[-14:][::-1]
        rows = []
        for local in dominant:
            slot = int(energy.rest[local])
            raw = int(system.core[slot])
            native = int(system.context["state_map"][raw])
            rows.append(dict(slot=slot, raw=raw, native=native, unit=float(system.units[slot]),
                             diagonal_weight=float(energy.diagonal[slot]), eigenvector=float(vector[local])))
        slow = [int(np.flatnonzero(system.core == position)[0]) for position in system.owner.scalar_positions[:2]]
        point = system.context["point"](efold)
        outputs.append(dict(model=model, efold=efold, largest_rate=float(eigenvalues[-1]), dominant=rows,
                            slow_slots=slow, slow_block=core[np.ix_(slow, slow)].tolist(),
                            native_signature=system.context["signature_values"].tolist()))
        print(model, "slow slots", slow, "dominant", rows[:6], flush=True)
    write(ROOT / "rest-diagnosis.json", dict(passed=True, reports=outputs, no_model_or_tolerance_change=True))
    check_parent()


if __name__ == "__main__":
    main()

